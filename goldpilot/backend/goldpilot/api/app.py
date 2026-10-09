"""Service web GoldPilot (processus « web ») : API, webhook TradingView, site compilé.

Toutes les routes /api/* (sauf /api/health, /api/auth/login et le webhook) exigent une session.
Les écritures exigent l'en-tête X-GoldPilot: 1 (protection CSRF) et sont journalisées dans l'audit.
"""
from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Literal

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from sqlalchemy import desc, func, select
from sqlalchemy.exc import IntegrityError

from .. import __version__, db
from ..calendar.events import next_event, Event
from ..config import settings
from ..engine import strategy_config
from ..marketdata import tradingview as tv
from ..marketdata.contracts import active_contract, next_contract
from ..notify import messages
from ..notify.telegram import Telegram
from ..risk.rules import PROGRAMS, get_program
from ..risk.sizing import RiskSettings
from ..timeutil import fmt_ny, fmt_paris, market_phase, trading_date, utcnow
from .security import COOKIE, api_limiter, client_ip, create_session, end_session, login_limiter, require_user, verify_password, webhook_limiter

log = logging.getLogger("goldpilot.web")

app = FastAPI(title="GoldPilot", version=__version__, docs_url=None, redoc_url=None, openapi_url=None)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    if request.url.path.startswith("/api/") and not request.url.path.startswith("/api/webhooks/"):
        if not api_limiter.allow(client_ip(request)):
            return JSONResponse({"detail": "trop de requêtes"}, status_code=429)
    resp: Response = await call_next(request)
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["X-Frame-Options"] = "DENY"
    resp.headers["Referrer-Policy"] = "no-referrer"
    resp.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    resp.headers["Content-Security-Policy"] = ("default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; "
                                               "script-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'")
    if settings().production:
        resp.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    if request.url.path.startswith("/api/"):
        resp.headers["Cache-Control"] = "no-store"
    return resp


# ---------------------------------------------------------------------------------------------- outils
def iso(dt: datetime | None) -> str | None:
    return dt.isoformat() if dt else None


def sig_json(r: db.Signal) -> dict:
    return {
        "id": r.id, "cree": iso(r.created_at), "cree_paris": fmt_paris(r.created_at), "mode": r.mode, "valide": r.validated,
        "version": r.strategy_version, "contrat": r.symbol, "sens": "LONG" if r.side > 0 else "SHORT", "type_entree": r.entry_type,
        "entree": r.entry_ref, "plage": [r.entry_ref - r.entry_max_drift, r.entry_ref + r.entry_max_drift], "stop": r.stop,
        "objectif": r.target, "stop_suiveur_atr": r.trail_atr, "atr": r.atr, "contrats": r.contracts, "risque_usd": r.risk_usd,
        "rr": r.reward_risk, "validite": iso(r.valid_until), "validite_ny": fmt_ny(r.valid_until), "sortie_max": fmt_ny(r.exit_deadline),
        "justification": r.rationale, "invalidation": r.invalidation, "calendrier": r.calendar_note, "source_prix": r.price_source,
        "prix_maj": iso(r.price_ts), "statut": r.status, "raison_statut": r.status_reason,
        "simulation": {"entree": r.sim_entry, "entree_ts": iso(r.sim_entry_ts), "stop_actuel": r.sim_stop, "sortie": r.sim_exit,
                       "sortie_ts": iso(r.sim_exit_ts), "raison": r.sim_exit_reason, "r": r.sim_r, "pnl_usd": r.sim_pnl_usd},
        "execution_declaree": None if r.user_executed is None else {"executee": r.user_executed, "entree": r.user_entry,
                                                                     "sortie": r.user_exit, "contrats": r.user_contracts,
                                                                     "pnl_usd": r.user_pnl_usd, "note": r.user_note},
    }


def research_json(name: str) -> dict | None:
    p = settings().research_dir / name
    return json.loads(p.read_text()) if p.exists() else None


# ---------------------------------------------------------------------------------------------- santé
@app.get("/api/health")
def health():
    """Contrôle public minimal pour une surveillance externe (aucune donnée sensible)."""
    with db.session() as s:
        hb = s.get(db.Heartbeat, "engine")
        age = (utcnow() - hb.ts).total_seconds() if hb else None
    ok = age is not None and age < 60
    return JSONResponse({"web": "ok", "moteur": "ok" if ok else "silencieux"}, status_code=200 if ok else 503)


# ---------------------------------------------------------------------------------------------- auth
class Login(BaseModel):
    password: str = Field(min_length=1, max_length=200)


@app.post("/api/auth/login")
def login(body: Login, request: Request, response: Response):
    ip = client_ip(request)
    if not login_limiter.allow(ip):
        raise HTTPException(429, "trop de tentatives, réessaie dans 15 minutes")
    stored = settings().admin_password_hash
    if not stored or not verify_password(body.password, stored):
        with db.session() as s:
            db.audit(s, "inconnu", "connexion_refusee", {"ip": ip})
        raise HTTPException(401, "mot de passe incorrect")
    token = create_session(ip)
    response.set_cookie(COOKIE, token, httponly=True, secure=settings().production, samesite="strict",
                        max_age=settings().session_hours * 3600, path="/")
    with db.session() as s:
        db.audit(s, "utilisateur", "connexion", {"ip": ip})
    return {"ok": True}


@app.post("/api/auth/logout")
def logout(request: Request, response: Response):
    end_session(request.cookies.get(COOKIE))
    response.delete_cookie(COOKIE, path="/")
    return {"ok": True}


@app.get("/api/auth/me")
def me(user: str = Depends(require_user)):
    return {"user": user}


# ---------------------------------------------------------------------------------------------- tableau de bord
@app.get("/api/dashboard")
def dashboard(user: str = Depends(require_user)):
    now = utcnow()
    st = settings()
    conf = strategy_config.load_production()
    with db.session() as s:
        hb = s.get(db.Heartbeat, "engine")
        hb_age = (now - hb.ts).total_seconds() if hb else None
        mode = db.kv_get(s, "engine_mode") or {}
        detail = hb.detail if hb else {}
        last_bar = s.execute(select(db.Bar).order_by(desc(db.Bar.ts)).limit(1)).scalars().first()
        notif_on = bool(db.kv_get(s, "notifications", True))
        last_notif = s.execute(select(db.Notification).where(db.Notification.status.in_(["envoye", "echec"]))
                               .order_by(desc(db.Notification.id)).limit(1)).scalars().first()
        failed = s.execute(select(func.count(db.Notification.id)).where(db.Notification.status == "echec",
                                                                         db.Notification.created_at >= now - timedelta(days=1))).scalar()
        last_sig = s.execute(select(db.Signal).order_by(desc(db.Signal.created_at)).limit(1)).scalars().first()
        open_sig = s.execute(select(db.Signal).where(db.Signal.status.in_(["EN_ATTENTE", "ACTIF"])).order_by(desc(db.Signal.created_at))).scalars().first()
        last_dec = s.execute(select(db.Decision).order_by(desc(db.Decision.bar_ts)).limit(1)).scalars().first()
        evs = [Event(e.source, e.uid, e.title, e.impact, e.ts, e.source_url) for e in s.execute(
            select(db.EconomicEvent).where(db.EconomicEvent.ts >= now - timedelta(minutes=30), db.EconomicEvent.ts <= now + timedelta(days=14))).scalars()]
        program = get_program(db.kv_get(s, "program", "flex_50k_challenge"))
        paper = db.kv_get(s, "paper_account")
        upd = s.execute(select(db.AccountUpdate).order_by(desc(db.AccountUpdate.created_at)).limit(1)).scalars().first()
        rs = RiskSettings(**(db.kv_get(s, "risk_settings") or (conf or {}).get("risk_settings_default", {})))
        incidents = s.execute(select(db.Incident).where(db.Incident.resolved_at.is_(None)).order_by(desc(db.Incident.created_at)).limit(5)).scalars().all()
        trading_mode = db.kv_get(s, "trading_mode", "simulation")
        user_mode = db.kv_get(s, "user_mode", "actif")
        halt = db.kv_get(s, "halt")
    engine_alive = hb_age is not None and hb_age < 60
    data_age = (now - (last_bar.ts + timedelta(minutes=last_bar.minutes))).total_seconds() if last_bar else None
    contract = active_contract(trading_date(now))
    nxt = next_event(evs, now)
    tg_ok = bool(st.telegram_bot_token and st.telegram_chat_id)
    eng_mode = mode.get("mode") if engine_alive else "arrete"
    labels = {"actif": "Surveille le marché", "pause": "En pause (suspendu par toi)", "securise": "Mode sécurisé : aucun signal",
              "arret": "Arrêt de sécurité", "prechauffage": "Préchauffage (historique insuffisant)", "arrete": "Moteur arrêté",
              "demarrage": "Démarrage"}
    status = {
        "connexion": {"ok": engine_alive, "texte": "Serveur et moteur en ligne" if engine_alive else "Moteur injoignable (aucun signe de vie depuis plus d'une minute)"},
        "donnees": {"ok": bool(engine_alive and mode.get("qualite") == "ok"),
                    "texte": ("Données à jour" if mode.get("qualite") == "ok" else "; ".join(mode.get("problemes") or ["Données indisponibles"])) if engine_alive else "Inconnu (moteur arrêté)",
                    "age_s": data_age, "source": {"tradingview": "TradingView (webhook)", "databento": "Databento", "replay": "Rejeu historique (simulation)"}.get(st.data_source, st.data_source)},
        "moteur": {"ok": eng_mode == "actif", "etat": eng_mode, "texte": labels.get(eng_mode, eng_mode), "arret": halt},
        "notifications": {"ok": notif_on and tg_ok and not failed, "active": notif_on, "configure": tg_ok, "echecs_24h": failed,
                          "texte": ("Telegram non configuré" if not tg_ok else "Désactivées par toi" if not notif_on else
                                    f"{failed} échec(s) d'envoi sur 24 h" if failed else "Opérationnelles"),
                          "derniere": iso(last_notif.sent_at) if last_notif else None},
    }
    market = {
        "instrument": contract.label(), "contrat": contract.code, "tradingview": contract.tradingview, "tradovate": contract.short_code,
        "prochain_roll": contract.roll_date.isoformat(), "contrat_suivant": next_contract(contract).code,
        "prix": detail.get("last_price"), "prix_maj": detail.get("last_bar_end"), "seance": market_phase(now),
        "regime": (last_dec.context or {}).get("regime") if last_dec else None,
        "ecart_moyenne_atr": (last_dec.context or {}).get("z") if last_dec else None,
        "prochaine_annonce": {"titre": nxt.title, "quand": fmt_paris(nxt.ts), "ny": fmt_ny(nxt.ts)} if nxt else None,
    }
    trading = {
        "setup": ("Signal en cours" if open_sig else "Aucun setup valide : les conditions ne sont pas réunies"),
        "signal_en_cours": sig_json(open_sig) if open_sig else None,
        "dernier_signal": sig_json(last_sig) if last_sig else None,
        "derniere_analyse": {"heure": fmt_ny(last_dec.bar_ts + timedelta(minutes=15)), "resultat": last_dec.summary,
                             "raisons": last_dec.reasons} if last_dec else None,
        "strategie": {"version": conf["version"] if conf else None, "validee": bool(conf and conf.get("validated")),
                      "verdict": conf.get("verdict") if conf else "Aucune stratégie configurée"},
        "mode_trading": trading_mode, "mode_utilisateur": user_mode,
        "risque": {"par_trade_usd": rs.risk_per_trade_usd, "perte_jour_max_usd": rs.daily_loss_stop_usd,
                   "trades_jour_max": rs.max_trades_per_day, "programme": program.label,
                   "perte_max_programme": program.max_loss, "objectif": program.profit_target},
        "compte_simule": paper,
        "compte_reel": ({"solde": upd.balance, "maj": fmt_paris(upd.created_at), "plancher": None} if upd else None),
    }
    return {"maintenant": iso(now), "statut": status, "marche": market, "trading": trading,
            "incidents": [{"gravite": i.severity, "message": i.message, "depuis": fmt_paris(i.created_at)} for i in incidents]}


# ---------------------------------------------------------------------------------------------- actions
class ModeBody(BaseModel):
    mode: Literal["actif", "pause"]


@app.post("/api/engine/mode")
def set_mode(body: ModeBody, user: str = Depends(require_user)):
    with db.session() as s:
        db.kv_set(s, "user_mode", body.mode)
        db.audit(s, user, "mode_utilisateur", {"mode": body.mode})
    return {"ok": True}


@app.post("/api/engine/resume-after-halt")
def resume_after_halt(user: str = Depends(require_user)):
    with db.session() as s:
        h = db.kv_get(s, "halt")
        db.kv_set(s, "halt", None)
        db.resolve_incident(s, "performance", "degradation")
        db.audit(s, user, "reprise_apres_arret", {"arret": h})
    return {"ok": True}


class Toggle(BaseModel):
    active: bool


@app.post("/api/notifications/toggle")
def toggle_notif(body: Toggle, user: str = Depends(require_user)):
    with db.session() as s:
        db.kv_set(s, "notifications", body.active)
        db.audit(s, user, "notifications", {"actives": body.active})
    return {"ok": True}


@app.post("/api/notifications/test")
def test_notif(user: str = Depends(require_user)):
    st = settings()
    tg = Telegram(st.telegram_bot_token, st.telegram_chat_id)
    ok, err = tg.send_now(messages.test_message(utcnow()))
    with db.session() as s:
        db.audit(s, user, "test_notification", {"ok": ok, "erreur": err})
    if not ok:
        raise HTTPException(502, f"échec de l'envoi : {err}")
    return {"ok": True}


@app.post("/api/notifications/detect-chat")
def detect_chat(user: str = Depends(require_user)):
    st = settings()
    if not st.telegram_bot_token:
        raise HTTPException(400, "TELEGRAM_BOT_TOKEN n'est pas défini sur le serveur")
    try:
        return {"conversations": Telegram(st.telegram_bot_token, "").detect_chat_id()}
    except Exception as e:
        raise HTTPException(502, f"Telegram injoignable : {type(e).__name__}") from None


# ---------------------------------------------------------------------------------------------- signaux
@app.get("/api/signals")
def signals(limit: int = 50, statut: str | None = None, user: str = Depends(require_user)):
    with db.session() as s:
        q = select(db.Signal).order_by(desc(db.Signal.created_at)).limit(min(max(limit, 1), 500))
        if statut:
            q = q.where(db.Signal.status == statut)
        return {"signaux": [sig_json(r) for r in s.execute(q).scalars()]}


@app.get("/api/signals/{sid}")
def signal_detail(sid: str, user: str = Depends(require_user)):
    with db.session() as s:
        r = s.get(db.Signal, sid)
        if not r:
            raise HTTPException(404, "signal inconnu")
        evs = s.execute(select(db.SignalEvent).where(db.SignalEvent.signal_id == sid).order_by(db.SignalEvent.ts)).scalars().all()
        dec = s.execute(select(db.Decision).where(db.Decision.signal_id == sid)).scalars().first()
        return {"signal": sig_json(r), "evenements": [{"heure": fmt_paris(e.ts), "type": e.kind, "detail": e.detail} for e in evs],
                "controles_risque": dec.risk_checks if dec else []}


class Execution(BaseModel):
    executee: bool
    entree: float | None = Field(default=None, gt=0, lt=100_000)
    sortie: float | None = Field(default=None, gt=0, lt=100_000)
    contrats: int | None = Field(default=None, ge=1, le=30)
    note: str = Field(default="", max_length=500)


@app.post("/api/signals/{sid}/execution")
def declare_execution(sid: str, body: Execution, user: str = Depends(require_user)):
    with db.session() as s:
        r = s.get(db.Signal, sid)
        if not r:
            raise HTTPException(404, "signal inconnu")
        r.user_executed, r.user_entry, r.user_exit, r.user_contracts, r.user_note = body.executee, body.entree, body.sortie, body.contrats, body.note
        if body.executee and body.entree and body.sortie and body.contrats:
            r.user_pnl_usd = (body.sortie - body.entree) * r.side * 10.0 * body.contrats
        s.add(db.SignalEvent(signal_id=sid, kind="execution_declaree", detail=body.model_dump()))
        db.audit(s, user, "execution_declaree", {"signal": sid})
    return {"ok": True}


@app.post("/api/signals/{sid}/cancel")
def cancel_signal(sid: str, user: str = Depends(require_user)):
    with db.session() as s:
        r = s.get(db.Signal, sid)
        if not r or r.status not in ("EN_ATTENTE", "ACTIF"):
            raise HTTPException(400, "signal non annulable")
        if r.sim_entry is not None:
            raise HTTPException(400, "la position simulée est déjà ouverte : elle sera suivie jusqu'à sa sortie")
        r.status, r.status_reason = "ANNULE", "annulé par toi"
        s.add(db.SignalEvent(signal_id=sid, kind="annule", detail={"par": "utilisateur"}))
        db.audit(s, user, "annulation_signal", {"signal": sid})
    return {"ok": True}


# ---------------------------------------------------------------------------------------------- journal
@app.get("/api/journal")
def journal(type: Literal["decisions", "incidents", "notifications", "webhooks", "audit"] = "decisions", limit: int = 100,
            user: str = Depends(require_user)):
    lim = min(max(limit, 1), 500)
    with db.session() as s:
        if type == "decisions":
            rows = s.execute(select(db.Decision).order_by(desc(db.Decision.bar_ts)).limit(lim)).scalars()
            return {"lignes": [{"heure": fmt_paris(d.bar_ts + timedelta(minutes=15)), "resultat": d.outcome, "resume": d.summary,
                                "raisons": d.reasons, "contexte": d.context, "controles": d.risk_checks, "signal": d.signal_id,
                                "version": d.strategy_version} for d in rows]}
        if type == "incidents":
            rows = s.execute(select(db.Incident).order_by(desc(db.Incident.created_at)).limit(lim)).scalars()
            return {"lignes": [{"heure": fmt_paris(i.created_at), "gravite": i.severity, "composant": i.component, "message": i.message,
                                "resolu": fmt_paris(i.resolved_at) if i.resolved_at else None} for i in rows]}
        if type == "notifications":
            rows = s.execute(select(db.Notification).order_by(desc(db.Notification.id)).limit(lim)).scalars()
            return {"lignes": [{"heure": fmt_paris(n.created_at), "type": n.kind, "statut": n.status, "essais": n.attempts,
                                "erreur": n.error, "texte": n.text} for n in rows]}
        if type == "webhooks":
            rows = s.execute(select(db.WebhookLog).order_by(desc(db.WebhookLog.id)).limit(lim)).scalars()
            return {"lignes": [{"heure": fmt_paris(w.received_at), "ip": w.ip, "type": w.kind, "accepte": w.accepted, "raison": w.reason}
                               for w in rows]}
        rows = s.execute(select(db.Audit).order_by(desc(db.Audit.id)).limit(lim)).scalars()
        return {"lignes": [{"heure": fmt_paris(a.ts), "acteur": a.actor, "action": a.action, "detail": a.detail} for a in rows]}


# ---------------------------------------------------------------------------------------------- statistiques
@app.get("/api/stats")
def stats(user: str = Depends(require_user)):
    with db.session() as s:
        closed = s.execute(select(db.Signal).where(db.Signal.status == "CLOTURE").order_by(db.Signal.created_at)).scalars().all()
    rs = [r.sim_r for r in closed if r.sim_r is not None]
    paper = None
    if rs:
        import numpy as np

        a = np.array(rs)
        eq = np.cumsum(a)
        paper = {"n": len(a), "esperance_R": float(a.mean()), "taux_de_gain": float((a > 0).mean()), "total_R": float(a.sum()),
                 "drawdown_max_R": float((eq - np.maximum.accumulate(np.r_[0, eq])[1:]).min()),
                 "pnl_usd": float(sum(r.sim_pnl_usd or 0 for r in closed)),
                 "courbe": [{"date": r.created_at.date().isoformat(), "R": float(x)} for r, x in zip(closed, eq)]}
    return {"production": strategy_config.load_production(), "selection": research_json("selection/selection.json"),
            "test_final": research_json("final/final.json"), "monte_carlo": research_json("final/montecarlo.json"),
            "paper": paper}


# ---------------------------------------------------------------------------------------------- réglages
@app.get("/api/settings")
def get_settings(user: str = Depends(require_user)):
    st = settings()
    conf = strategy_config.load_production() or {}
    with db.session() as s:
        rs = db.kv_get(s, "risk_settings") or conf.get("risk_settings_default") or RiskSettings().to_dict()
        prog_key = db.kv_get(s, "program", "flex_50k_challenge")
        trading_mode = db.kv_get(s, "trading_mode", "simulation")
    contract = active_contract(trading_date(utcnow()))
    return {
        "risque": rs, "programme": prog_key, "programmes": {k: p.to_dict() for k, p in PROGRAMS.items()},
        "mode_trading": trading_mode, "strategie_validee": bool(conf.get("validated")),
        "tradingview": {"url_webhook": f"{st.public_base_url}/api/webhooks/tradingview", "jeton_defini": bool(st.tv_webhook_token),
                        "symbole": contract.tradingview, "unite": "1 minute"},
        "telegram": {"configure": bool(st.telegram_bot_token and st.telegram_chat_id), "jeton_defini": bool(st.telegram_bot_token)},
        "source_donnees": st.data_source,
    }


@app.put("/api/settings/risk")
def put_risk(body: dict, user: str = Depends(require_user)):
    try:
        rs = RiskSettings(**body)
    except TypeError as e:
        raise HTTPException(422, f"champ inconnu : {e}") from None
    errs = rs.validate()
    if errs:
        raise HTTPException(422, " ".join(errs))
    with db.session() as s:
        old = db.kv_get(s, "risk_settings")
        db.kv_set(s, "risk_settings", rs.to_dict())
        db.audit(s, user, "parametres_risque", {"avant": old, "apres": rs.to_dict()})
    return {"ok": True}


class ProgramBody(BaseModel):
    programme: str


@app.put("/api/settings/program")
def put_program(body: ProgramBody, user: str = Depends(require_user)):
    if body.programme not in PROGRAMS:
        raise HTTPException(422, "programme inconnu")
    with db.session() as s:
        db.kv_set(s, "program", body.programme)
        db.audit(s, user, "programme", {"programme": body.programme})
    return {"ok": True}


class TradingModeBody(BaseModel):
    mode: Literal["simulation", "reel"]
    confirmation: str = ""


@app.put("/api/settings/trading-mode")
def put_trading_mode(body: TradingModeBody, user: str = Depends(require_user)):
    conf = strategy_config.load_production() or {}
    if body.mode == "reel":
        if not conf.get("validated"):
            raise HTTPException(409, "Refusé : la stratégie n'a pas satisfait les critères de validation. Le mode réel reste verrouillé.")
        if body.confirmation != "JE CONFIRME LE PASSAGE EN REEL":
            raise HTTPException(422, "Confirmation exacte requise : « JE CONFIRME LE PASSAGE EN REEL »")
    with db.session() as s:
        db.kv_set(s, "trading_mode", body.mode)
        db.audit(s, user, "mode_trading", {"mode": body.mode})
    return {"ok": True}


class AccountBody(BaseModel):
    solde: float = Field(gt=0, lt=1_000_000)
    plus_haut_fin_de_jour: float | None = Field(default=None, gt=0, lt=1_000_000)
    meilleur_jour: float | None = Field(default=None, ge=0, lt=1_000_000)
    note: str = Field(default="", max_length=300)


@app.post("/api/account")
def post_account(body: AccountBody, user: str = Depends(require_user)):
    with db.session() as s:
        s.add(db.AccountUpdate(balance=body.solde, hwm_eod=body.plus_haut_fin_de_jour, best_day=body.meilleur_jour, note=body.note))
        db.audit(s, user, "etat_compte", body.model_dump())
    return {"ok": True}


@app.get("/api/calendar")
def calendar(user: str = Depends(require_user)):
    now = utcnow()
    with db.session() as s:
        rows = s.execute(select(db.EconomicEvent).where(db.EconomicEvent.ts >= now - timedelta(hours=2)).order_by(db.EconomicEvent.ts).limit(60)).scalars()
        st = db.kv_get(s, "calendar_status")
        return {"statut": st, "evenements": [{"titre": e.title, "impact": e.impact, "paris": fmt_paris(e.ts), "new_york": fmt_ny(e.ts),
                                              "source": e.source_url} for e in rows]}


class ManualEvent(BaseModel):
    titre: str = Field(min_length=3, max_length=200)
    quand: datetime


@app.post("/api/calendar")
def add_event(body: ManualEvent, user: str = Depends(require_user)):
    if body.quand.tzinfo is None:
        raise HTTPException(422, "indiquer le fuseau horaire")
    with db.session() as s:
        s.add(db.EconomicEvent(source="manuel", uid=f"manuel-{body.quand.isoformat()}-{body.titre}"[:200], title=body.titre,
                               impact="fort", ts=body.quand, source_url="saisi manuellement"))
        db.audit(s, user, "evenement_manuel", body.model_dump(mode="json"))
    return {"ok": True}


# ---------------------------------------------------------------------------------------------- webhook TradingView
@app.post("/api/webhooks/tradingview")
async def tradingview_webhook(request: Request):
    st = settings()
    ip = client_ip(request)
    received = utcnow()

    def log_row(kind: str, accepted: bool, reason: str, payload: dict):
        safe = {k: v for k, v in payload.items() if k != "token"} if isinstance(payload, dict) else {}
        with db.session() as s:
            s.add(db.WebhookLog(ip=ip, kind=kind, accepted=accepted, reason=reason, payload=safe))

    if not webhook_limiter.allow(ip):
        return JSONResponse({"ok": False, "raison": "débit excessif"}, status_code=429)
    if st.tv_enforce_ip and ip not in st.tv_ip_allowlist:
        log_row("?", False, "adresse IP non autorisée", {})
        return JSONResponse({"ok": False}, status_code=403)
    raw = await request.body()
    if len(raw) > tv.MAX_BODY:
        log_row("?", False, "message trop volumineux", {})
        return JSONResponse({"ok": False}, status_code=413)
    try:
        payload = json.loads(raw)
    except ValueError:
        log_row("?", False, "JSON invalide", {})
        return JSONResponse({"ok": False, "raison": "JSON invalide"}, status_code=400)
    try:
        msg = tv.parse(payload, st.tv_webhook_token, received)
    except tv.Rejected as e:
        log_row(str(payload.get("kind", "?")) if isinstance(payload, dict) else "?", False, e.reason, payload if isinstance(payload, dict) else {})
        return JSONResponse({"ok": False, "raison": e.reason}, status_code=e.status)
    sym = msg.ticker.split(":")[-1].upper()
    try:
        with db.session() as s:
            if isinstance(msg, tv.BarMsg):
                s.add(db.Bar(source="tradingview", symbol=sym, ts=tv.ms_to_dt(msg.t), minutes=1, open=msg.o, high=msg.h, low=msg.l,
                             close=msg.c, volume=msg.vol, received_at=received, processed=False))
            else:
                s.add(db.MirrorSignal(symbol=sym, bar_ts=tv.ms_to_dt(msg.t), side=msg.side, price=msg.price))
    except IntegrityError:
        return {"ok": True, "doublon": True}  # renvoi TradingView : déjà enregistré
    delay = tv.delay_of(msg, received).total_seconds() if isinstance(msg, tv.BarMsg) else None
    log_row(msg.kind, True, f"retard {delay:.0f} s" if delay is not None else "", payload)
    return {"ok": True}


@app.get("/api/setup/pine")
def pine_script(user: str = Depends(require_user)):
    p = Path(__file__).resolve().parents[3] / "pine" / "goldpilot_bridge.pine"
    return Response(p.read_text() if p.exists() else "// script introuvable", media_type="text/plain; charset=utf-8")


# ---------------------------------------------------------------------------------------------- site
_front = settings().frontend_dir
if _front.exists():
    app.mount("/assets", StaticFiles(directory=_front / "assets"), name="assets")

    @app.get("/{path:path}", include_in_schema=False)
    def spa(path: str):
        if path.startswith("api/"):
            raise HTTPException(404)
        f = _front / path
        if path and f.is_file() and _front in f.resolve().parents:
            return FileResponse(f)
        return FileResponse(_front / "index.html")


def create_app() -> FastAPI:
    st = settings()
    probs = st.startup_problems()
    if probs:
        raise SystemExit("Configuration refusée :\n- " + "\n- ".join(probs))
    db.init()
    return app
