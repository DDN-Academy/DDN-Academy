"""Textes des alertes Telegram (HTML). Chaque alerte de trading contient tous les éléments exigés :
instrument et contrat exacts, date/heure avec fuseau, sens, entrée (prix ou plage), type d'entrée, stop,
sortie (objectif fixe ou règle de sortie exacte), rendement/risque, risque en $, taille, validité,
condition d'annulation, justification, calendrier économique, source et heure du prix, mode.
"""
from __future__ import annotations

from datetime import datetime
from html import escape

from ..timeutil import fmt_ny, fmt_paris


def p(x: float | None) -> str:
    return "—" if x is None else f"{x:,.1f}".replace(",", " ")


def usd(x: float | None) -> str:
    return "—" if x is None else f"{x:,.0f} $".replace(",", " ")


def header(mode: str, validated: bool) -> str:
    if mode == "reel" and validated:
        return ""
    return ("🧪 <b>SIMULATION — NE PAS EXÉCUTER SUR LE COMPTE</b>\n"
            "<i>Stratégie non validée pour l'argent réel : signal destiné au suivi papier.</i>\n\n")


def new_signal(sig, contract_label: str, historical_rr: float | None, next_event_txt: str) -> str:
    side = "ACHAT (LONG) ⬆️" if sig.side > 0 else "VENTE (SHORT) ⬇️"
    lo, hi = sig.entry_ref - sig.entry_max_drift, sig.entry_ref + sig.entry_max_drift
    if sig.target is not None:
        exit_txt = f"<b>Take-profit :</b> {p(sig.target)}"
        rr_txt = f"{sig.reward_risk:.2f}" if sig.reward_risk else "—"
    else:
        exit_txt = (f"<b>Take-profit :</b> aucun objectif fixe — sortie par <b>stop suiveur</b> à {sig.trail_atr:g} ATR "
                    f"({p(sig.trail_atr * sig.atr)} $) de l'extrême atteint, mis à jour toutes les 15 min (je t'envoie chaque "
                    f"nouveau niveau), et fermeture au plus tard à {fmt_ny(sig.exit_deadline)}"
                    if sig.trail_atr else f"<b>Take-profit :</b> aucun objectif fixe — fermeture à {fmt_ny(sig.exit_deadline)}")
        rr_txt = (f"pas d'objectif fixe ; rapport gain moyen / perte moyenne historique ≈ {historical_rr:.2f}"
                  if historical_rr else "pas d'objectif fixe")
    entry_kind = "immédiate (au marché)" if sig.entry_type == "market" else f"conditionnelle (ordre {sig.entry_type} à {p(sig.entry_ref)})"
    return (
        header(sig.mode, sig.validated)
        + f"🟡 <b>GOLD — SIGNAL {'LONG' if sig.side > 0 else 'SHORT'}</b>\n"
        f"<b>Instrument :</b> {escape(contract_label)}\n"
        f"<b>Heure :</b> {fmt_paris(sig.created_at)} — {fmt_ny(sig.created_at)}\n"
        f"<b>Sens :</b> {side}\n"
        f"<b>Entrée :</b> {entry_kind} — plage acceptable {p(lo)} – {p(hi)}\n"
        f"<b>Stop-loss :</b> {p(sig.stop)}\n"
        f"{exit_txt}\n"
        f"<b>Rendement/risque :</b> {rr_txt}\n"
        f"<b>Taille :</b> {sig.contracts} contrat(s) MGC\n"
        f"<b>Risque estimé :</b> {usd(sig.risk_usd)} (stop + glissement + commission)\n"
        f"<b>Validité :</b> jusqu'à {fmt_ny(sig.valid_until)} ({fmt_paris(sig.valid_until)})\n"
        f"<b>Annulation :</b> {escape(sig.invalidation)}\n"
        f"<b>Pourquoi :</b> {escape(sig.rationale)}\n"
        f"<b>Calendrier :</b> {escape(sig.calendar_note or next_event_txt)}\n"
        f"<b>Prix :</b> {escape(sig.price_source)}, dernière mise à jour {fmt_ny(sig.price_ts)}\n"
        f"<i>Réf. {sig.id[:8]} — {escape(sig.strategy_version)}</i>"
    )


def status_change(sig, title: str, detail: str) -> str:
    return (header(sig.mode, sig.validated) + f"<b>{escape(title)}</b> — signal {'LONG' if sig.side > 0 else 'SHORT'} {escape(sig.symbol)} "
            f"(réf. {sig.id[:8]})\n{escape(detail)}")


def stop_update(sig, new_stop: float, price: float) -> str:
    return (header(sig.mode, sig.validated) + f"🔧 <b>Déplacer le stop</b> — {escape(sig.symbol)} {'LONG' if sig.side > 0 else 'SHORT'} "
            f"(réf. {sig.id[:8]})\nNouveau stop : <b>{p(new_stop)}</b> (prix actuel {p(price)})")


def system_alert(title: str, detail: str, at: datetime) -> str:
    return f"⚠️ <b>{escape(title)}</b>\n{escape(detail)}\n<i>{fmt_paris(at)}</i>"


def test_message(at: datetime) -> str:
    return f"✅ <b>GoldPilot</b> — notification de test reçue.\n{fmt_paris(at)}"
