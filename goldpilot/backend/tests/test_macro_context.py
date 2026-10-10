"""Contexte macro FRED : analyse des réponses, erreurs, clé jamais exposée, stockage moteur et forme du tableau de bord.

Aucun accès réseau : toutes les réponses FRED sont simulées avec httpx.MockTransport.
"""
from __future__ import annotations

import logging
from datetime import timedelta
from pathlib import Path

import httpx
import pytest

from goldpilot import db
from goldpilot.config import settings
from goldpilot.context import fred

from .conftest import utc

KEY = "abcdef0123456789abcdef0123456789"  # fausse clé (format FRED : 32 caractères)
NOW = utc(2026, 10, 10, 12, 0)
CONTRACT_KEYS = {"disponible", "maj", "source", "note", "probleme", "series"}
SERIE_KEYS = {"id", "nom", "valeur", "unite", "date", "variation_5j", "url"}

# Valeurs fictives propres aux tests (ce ne sont PAS des données FRED réelles).
OBS = {
    "DFII10": [("2026-09-30", "1.90"), ("2026-10-01", "1.92"), ("2026-10-02", "."), ("2026-10-05", "1.88"),
               ("2026-10-06", "1.87"), ("2026-10-07", "1.86"), ("2026-10-08", "1.85"), ("2026-10-09", ".")],
    "DGS10": [("2026-10-06", "4.10"), ("2026-10-07", "4.12"), ("2026-10-08", "4.15")],
    "DTWEXBGS": [("2026-09-25", "120.5000"), ("2026-09-26", "120.7000"), ("2026-09-29", "120.6000"),
                 ("2026-09-30", "120.9000"), ("2026-10-01", "121.0000"), ("2026-10-02", "121.3848")],
}


def body(sid: str) -> dict:
    return {"realtime_start": "2026-10-10", "realtime_end": "2026-10-10", "units": "lin", "count": len(OBS[sid]),
            "observations": [{"realtime_start": "2026-10-10", "realtime_end": "2026-10-10", "date": d, "value": v}
                             for d, v in OBS[sid]]}


def mock_client(handler) -> httpx.Client:
    return httpx.Client(transport=httpx.MockTransport(handler))


def ok_handler(calls: list | None = None):
    def h(request: httpx.Request) -> httpx.Response:
        if calls is not None:
            calls.append(request)
        return httpx.Response(200, json=body(request.url.params["series_id"]))
    return h


# ---------------------------------------------------------------------------------------------- analyse
def test_parse_value_missing_never_zero():
    assert fred.parse_value(".") is None
    assert fred.parse_value("") is None
    assert fred.parse_value(None) is None
    assert fred.parse_value("n/a") is None
    assert fred.parse_value("NaN") is None
    assert fred.parse_value(" 1.85 ") == 1.85
    assert fred.parse_value("-0.12") == -0.12


def test_build_context_parses_series_and_request_parameters():
    calls: list[httpx.Request] = []
    ctx = fred.build_context(KEY, client=mock_client(ok_handler(calls)), now=NOW)
    assert set(ctx) == CONTRACT_KEYS
    assert ctx["disponible"] is True and ctx["probleme"] is None
    assert ctx["maj"] == NOW.isoformat() and ctx["source"] == fred.SOURCE and ctx["note"] == fred.NOTE
    assert [r.url.params["series_id"] for r in calls] == ["DFII10", "DGS10", "DTWEXBGS"]
    for r in calls:
        assert str(r.url).startswith(fred.API_URL + "?")
        assert r.url.params["api_key"] == KEY and r.url.params["file_type"] == "json"
        assert r.url.params["observation_start"] == (NOW.date() - timedelta(days=fred.LOOKBACK_DAYS)).isoformat()
        assert r.url.params["sort_order"] == "asc"
    by = {s["id"]: s for s in ctx["series"]}
    for s in ctx["series"]:
        assert set(s) == SERIE_KEYS and s["url"] == f"https://fred.stlouisfed.org/series/{s['id']}"
    # DFII10 : dernière valeur VALIDE (le « . » du 09/10 est ignoré), variation sur 5 valeurs valides en arrière
    assert by["DFII10"]["valeur"] == 1.85 and by["DFII10"]["date"] == "2026-10-08" and by["DFII10"]["unite"] == "%"
    assert by["DFII10"]["variation_5j"] == pytest.approx(1.85 - 1.90)  # 1.90 = 5 valeurs valides avant 1.85
    assert by["DFII10"]["nom"] == "Taux réel américain 10 ans (TIPS)"
    # DGS10 : moins de 6 valeurs valides → variation inconnue (None), jamais inventée
    assert by["DGS10"]["valeur"] == 4.15 and by["DGS10"]["variation_5j"] is None
    assert by["DTWEXBGS"]["valeur"] == 121.3848 and by["DTWEXBGS"]["variation_5j"] == pytest.approx(0.8848)


def test_summarize_all_missing_is_an_error():
    with pytest.raises(fred.FredError):
        fred.summarize(fred.SERIES[0], [("2026-10-08", None), ("2026-10-09", None)])


# ---------------------------------------------------------------------------------------------- erreurs
def test_key_absent_makes_no_request():
    calls: list = []
    ctx = fred.build_context("", client=mock_client(ok_handler(calls)), now=NOW)
    assert calls == []
    assert ctx == fred.unavailable(fred.KEY_MISSING)
    assert ctx["probleme"] == "FRED_API_KEY non défini (clé gratuite à demander sur fred.stlouisfed.org)"


def test_http_error_message_never_contains_key():
    def h(request):
        return httpx.Response(400, json={"error_code": 400, "error_message": f"Bad Request. api_key={KEY} is not registered ({KEY})"})
    ctx = fred.build_context(KEY, client=mock_client(h), now=NOW)
    assert ctx["disponible"] is False and ctx["series"] == [] and ctx["maj"] is None
    assert "HTTP 400" in ctx["probleme"] and "Bad Request" in ctx["probleme"]
    assert KEY not in repr(ctx)


def test_server_error_without_json_body():
    ctx = fred.build_context(KEY, client=mock_client(lambda r: httpx.Response(503, text="<html>down</html>")), now=NOW)
    assert ctx["disponible"] is False and "HTTP 503" in ctx["probleme"]


def test_invalid_json_and_missing_observations():
    ctx = fred.build_context(KEY, client=mock_client(lambda r: httpx.Response(200, text="pas du json")), now=NOW)
    assert "réponse illisible" in ctx["probleme"]
    ctx = fred.build_context(KEY, client=mock_client(lambda r: httpx.Response(200, json={"foo": 1})), now=NOW)
    assert "réponse sans observations" in ctx["probleme"]


def test_timeout_and_network_errors_never_contain_key():
    def timeout(request):
        raise httpx.ReadTimeout(f"timed out on {request.url}", request=request)

    def network(request):
        raise httpx.ConnectError(f"cannot connect to {request.url}", request=request)

    for handler, expected in ((timeout, "délai de 10 s dépassé"), (network, "erreur réseau (ConnectError)")):
        ctx = fred.build_context(KEY, client=mock_client(handler), now=NOW)
        assert ctx["disponible"] is False and expected in ctx["probleme"]
        assert KEY not in repr(ctx) and "api_key" not in ctx["probleme"]


def test_timeout_is_ten_seconds():
    seen = []

    def h(request):
        seen.append(request.extensions.get("timeout"))
        return httpx.Response(200, json=body(request.url.params["series_id"]))
    fred.build_context(KEY, client=mock_client(h), now=NOW)
    assert seen and all(t == {"connect": 10.0, "read": 10.0, "write": 10.0, "pool": 10.0} for t in seen)


def test_partial_failure_keeps_other_series():
    def h(request):
        if request.url.params["series_id"] == "DGS10":
            return httpx.Response(500, json={"error_code": 500, "error_message": "Internal Server Error"})
        return httpx.Response(200, json=body(request.url.params["series_id"]))
    ctx = fred.build_context(KEY, client=mock_client(h), now=NOW)
    assert ctx["disponible"] is True
    assert [s["id"] for s in ctx["series"]] == ["DFII10", "DTWEXBGS"]
    assert ctx["probleme"].startswith("Série(s) indisponible(s) : DGS10 (HTTP 500")


def test_httpx_log_lines_are_redacted(caplog):
    caplog.set_level(logging.INFO, logger="httpx")
    fred.build_context(KEY, client=mock_client(ok_handler()), now=NOW)
    assert "HTTP Request" in caplog.text  # httpx journalise bien l'URL…
    assert KEY not in caplog.text and "api_key=***" in caplog.text  # … mais sans la clé


def test_redact():
    assert fred.redact(f"https://x/y?series_id=A&api_key={KEY}&file_type=json") == "https://x/y?series_id=A&api_key=***&file_type=json"
    assert fred.redact(f"clé {KEY} vue", KEY) == "clé *** vue"


# ---------------------------------------------------------------------------------------------- isolement
def test_strategy_and_risk_never_read_macro_context():
    """§ 2 : les autres marchés ne servent qu'à l'information ; aucun module de décision n'importe ce contexte."""
    root = Path(fred.__file__).resolve().parents[1]
    for pkg in ("strategy", "risk", "signals"):
        for f in (root / pkg).rglob("*.py"):
            src = f.read_text(encoding="utf-8")
            assert "from ..context" not in src and "goldpilot.context" not in src and "macro_context" not in src, f


# ---------------------------------------------------------------------------------------------- moteur
@pytest.fixture
def engine_with_key(env, monkeypatch):
    monkeypatch.setenv("FRED_API_KEY", KEY)
    settings.cache_clear()
    from goldpilot.engine.runner import Engine

    clock = {"now": NOW}
    eng = Engine(clock=lambda: clock["now"])
    eng.macro_async = False
    handler = {"h": ok_handler()}
    real = fred.build_context
    monkeypatch.setattr(fred, "build_context", lambda key, **kw: real(key, client=mock_client(lambda r: handler["h"](r)), now=clock["now"]))
    return eng, clock, handler


def _run(eng, now):
    with db.session() as s:
        eng._macro_context(s, now)


def _state():
    with db.session() as s:
        ctx = db.kv_get(s, "macro_context")
        inc = s.query(db.Incident).filter(db.Incident.component == "contexte", db.Incident.code == "fred").all()
        return ctx, [(i.severity, i.resolved_at is None) for i in inc]


def test_engine_stores_context_and_handles_failure_then_recovery(engine_with_key):
    eng, clock, handler = engine_with_key
    _run(eng, NOW)
    ctx, inc = _state()
    assert set(ctx) == CONTRACT_KEYS and ctx["disponible"] is True and len(ctx["series"]) == 3 and inc == []
    first_maj = ctx["maj"]

    # Échec complet 6 h plus tard : indisponible, date du dernier succès conservée, incident « avertissement »
    handler["h"] = lambda r: httpx.Response(500, json={"error_message": "boom"})
    clock["now"] = NOW + timedelta(hours=5, minutes=59)
    _run(eng, clock["now"])
    assert _state()[0]["disponible"] is True  # pas encore l'heure
    clock["now"] = NOW + timedelta(hours=6)
    _run(eng, clock["now"])
    ctx, inc = _state()
    assert ctx["disponible"] is False and ctx["series"] == [] and ctx["maj"] == first_maj
    assert "HTTP 500" in ctx["probleme"] and KEY not in repr(ctx)
    assert inc == [("avertissement", True)]
    with db.session() as s:
        msg = s.query(db.Incident).filter(db.Incident.code == "fred").one().message
    assert KEY not in msg and "les signaux ne sont pas affectés" in msg

    # Nouvel essai 30 min après un échec ; succès → incident résolu
    handler["h"] = ok_handler()
    clock["now"] = NOW + timedelta(hours=6, minutes=30)
    _run(eng, clock["now"])
    ctx, inc = _state()
    assert ctx["disponible"] is True and ctx["maj"] == clock["now"].isoformat() and inc == [("avertissement", False)]


def test_engine_tick_runs_macro_without_blocking_decisions(engine_with_key):
    eng, clock, _ = engine_with_key
    eng.startup()
    eng.tick()
    ctx, _ = _state()
    assert ctx["disponible"] is True


def test_engine_thread_mode(engine_with_key):
    eng, clock, _ = engine_with_key
    eng.macro_async = True
    _run(eng, NOW)
    assert eng.macro_thread is not None
    eng.macro_thread.join(5)
    assert _state()[0] is None  # le fil ne touche pas à la base
    _run(eng, NOW + timedelta(seconds=2))  # passage suivant de la boucle : enregistrement
    assert _state()[0]["disponible"] is True and eng.macro_thread is None


def test_engine_without_key_and_in_replay_makes_no_request(env, monkeypatch):
    from goldpilot.engine.runner import Engine

    def boom(*a, **k):
        raise AssertionError("aucune requête FRED attendue")
    monkeypatch.setattr(fred, "build_context", boom)
    monkeypatch.delenv("FRED_API_KEY", raising=False)
    settings.cache_clear()
    eng = Engine(clock=lambda: NOW)
    _run(eng, NOW)
    ctx, inc = _state()
    assert ctx == fred.unavailable(fred.KEY_MISSING) and inc == []

    monkeypatch.setenv("DATA_SOURCE", "replay")
    monkeypatch.setenv("FRED_API_KEY", KEY)
    settings.cache_clear()
    eng = Engine(clock=lambda: NOW)
    _run(eng, NOW)
    ctx, inc = _state()
    assert ctx["disponible"] is False and ctx["probleme"].startswith("Rejeu historique") and inc == []


# ---------------------------------------------------------------------------------------------- API
def test_dashboard_contract_shape(auth):
    d = auth.get("/api/dashboard").json()["marche"]["contexte_macro"]
    assert set(d) == CONTRACT_KEYS
    assert d["disponible"] is False and d["probleme"] == fred.NOT_YET and d["series"] == [] and d["maj"] is None
    assert d["source"] == "FRED — Federal Reserve Bank of St. Louis"
    assert d["note"] == "Information de contexte uniquement : non utilisée par la stratégie ni par le moteur de risque."

    ctx = fred.build_context(KEY, client=mock_client(ok_handler()), now=NOW)
    with db.session() as s:
        db.kv_set(s, "macro_context", ctx)
    d = auth.get("/api/dashboard").json()["marche"]["contexte_macro"]
    assert d == ctx
    assert all(set(x) == SERIE_KEYS for x in d["series"])
    assert KEY not in auth.get("/api/dashboard").text


def test_dashboard_view_tolerates_old_or_partial_values():
    assert fred.dashboard_view(None) == fred.unavailable(fred.NOT_YET)
    v = fred.dashboard_view({"disponible": 1, "series": "x"})
    assert set(v) == CONTRACT_KEYS and v["disponible"] is True and v["series"] == [] and v["probleme"] is None
