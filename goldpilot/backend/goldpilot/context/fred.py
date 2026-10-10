"""Contexte macroéconomique : rendements réels, taux nominaux et dollar américain, via l'API officielle FRED.

INFORMATION DE CONTEXTE UNIQUEMENT (cahier des charges § 2 et § 6 « Taux obligataires et rendements réels »,
« Dollar américain ») : ces valeurs ne sont lues ni par la stratégie, ni par le moteur de risque, et ne peuvent donc
ni créer, ni bloquer, ni dimensionner un signal. Elles sont affichées sur une page secondaire du site.

Source : FRED (Federal Reserve Economic Data), Federal Reserve Bank of St. Louis.
- Point d'accès utilisé : ``GET https://api.stlouisfed.org/fred/series/observations``
  (documentation : https://fred.stlouisfed.org/docs/api/fred/series_observations.html), paramètres
  ``series_id``, ``api_key`` (clé gratuite liée à un compte fred.stlouisfed.org), ``file_type=json``,
  ``observation_start``, ``sort_order=asc``. Réponse : ``{"observations": [{"date": "AAAA-MM-JJ", "value": "1.85"}, …]}``.
  Une valeur manquante (jour férié, donnée non publiée) vaut ``"."``. En cas d'erreur, FRED renvoie un code HTTP
  4xx/5xx, avec en JSON un champ ``error_message`` (format d'erreur lu dans la documentation, non observé ici).
- Limite publiée (sources secondaires) : 120 requêtes par minute et par clé. GoldPilot fait 3 requêtes toutes les 6 h.
- Conditions d'utilisation : https://fred.stlouisfed.org/docs/api/terms_of_use.html — à relire avant la mise en
  production (elles n'ont pas pu être consultées depuis le serveur de développement, voir plus bas). D'après un
  extrait des mentions légales (https://fred.stlouisfed.org/legal/) obtenu par recherche web, il est interdit de
  laisser entendre que la Federal Reserve Bank of St. Louis approuve le produit : le site cite donc simplement la
  source et le lien de chaque série.
- Pas de téléchargement sans clé (``fredgraph.csv``) ni de lecture des pages web : faute d'avoir pu vérifier que les
  conditions l'autorisent pour cet usage, seule l'API officielle avec clé est utilisée. Sans clé, le contexte est
  simplement marqué indisponible ; aucune valeur n'est jamais inventée.

VÉRIFICATIONS — honnêtement : depuis le bac à sable de développement, fred.stlouisfed.org et api.stlouisfed.org sont
bloqués par le proxy sortant (HTTP 403 au CONNECT) ; aucune requête réelle n'a donc pu être faite. Le format de
réponse ci-dessus vient de la documentation officielle ; le code est testé avec des réponses simulées
(tests/test_macro_context.py). Premier appel réel avec une vraie clé : NON TESTÉ, à vérifier sur la page du site.

Sécurité : la clé passe dans l'URL (exigence de l'API). Elle n'apparaît jamais dans les messages d'erreur produits
ici (seuls le type d'erreur, le code HTTP et le message FRED expurgé sont repris) et un filtre retire
``api_key=…`` des lignes de journal de la bibliothèque httpx (qui journalise l'URL complète au niveau INFO).
"""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone

import httpx

API_URL = "https://api.stlouisfed.org/fred/series/observations"
SOURCE = "FRED — Federal Reserve Bank of St. Louis"
NOTE = "Information de contexte uniquement : non utilisée par la stratégie ni par le moteur de risque."
TIMEOUT_S = 10.0
# Fenêtre demandée : assez large pour trouver 6 valeurs valides (variation sur 5 jours ouvrés) malgré les jours fériés
# et le décalage de publication hebdomadaire de l'indice dollar (H.10).
LOOKBACK_DAYS = 45
KEY_MISSING = "FRED_API_KEY non défini (clé gratuite à demander sur fred.stlouisfed.org)"
REPLAY = ("Rejeu historique : contexte macro non récupéré (les valeurs du jour ne correspondraient pas "
          "aux dates rejouées)")
NOT_YET = "Pas encore récupéré par le moteur (démarrage en cours ou moteur arrêté)"
USER_AGENT = "GoldPilot/1.0 (tableau de bord personnel, contexte macro)"

log = logging.getLogger("goldpilot.context.fred")


@dataclass(frozen=True)
class Serie:
    id: str
    nom: str
    unite: str
    decimales: int
    frequence: str
    pourquoi: str

    @property
    def url(self) -> str:
        return f"https://fred.stlouisfed.org/series/{self.id}"


SERIES: tuple[Serie, ...] = (
    Serie(
        "DFII10", "Taux réel américain 10 ans (TIPS)", "%", 2,
        "quotidienne (jours ouvrés), publication H.15 de la Fed, en général le jour ouvré suivant",
        # https://fred.stlouisfed.org/series/DFII10
        "Rendement réel des obligations indexées sur l'inflation (TIPS) à 10 ans. Le gold ne rapporte aucun intérêt : "
        "le rendement réel mesure ce que l'on renonce à gagner en le détenant. Relation historiquement plutôt inverse, "
        "mais instable selon les périodes : simple repère, aucune règle de trading n'en est tirée.",
    ),
    Serie(
        "DGS10", "Taux nominal américain 10 ans", "%", 2,
        "quotidienne (jours ouvrés), publication H.15 de la Fed, en général le jour ouvré suivant",
        # https://fred.stlouisfed.org/series/DGS10
        "Rendement nominal du Trésor américain à 10 ans. Avec le taux réel, il permet de lire l'inflation anticipée "
        "par le marché (écart nominal − réel) : distingue une hausse des taux due à l'inflation d'une hausse réelle.",
    ),
    Serie(
        "DTWEXBGS", "Dollar américain — indice large nominal (Fed)", "indice (janv. 2006 = 100)", 4,
        "valeurs quotidiennes publiées une fois par semaine (H.10 de la Fed) : la dernière valeur peut dater "
        "d'une semaine ou plus",
        # https://fred.stlouisfed.org/series/DTWEXBGS
        "Valeur du dollar face à un large panier de devises pondéré par le commerce extérieur (Federal Reserve). "
        "Le gold est coté en dollars : un dollar plus fort renchérit le métal pour les autres devises. L'indice DXY "
        "d'ICE n'est pas diffusé par FRED ; cet indice officiel de la Fed est son équivalent public.",
    ),
)


class FredError(Exception):
    """Erreur FRED dont le message est sûr à afficher et à journaliser (jamais d'URL ni de clé)."""


def redact(text: str, api_key: str = "") -> str:
    """Retire toute clé FRED d'un texte (paramètre ``api_key=…`` et valeur exacte de la clé)."""
    text = re.sub(r"(api_key=)[^&\s\"'>]+", r"\1***", text)
    if api_key:
        text = text.replace(api_key, "***")
    return text


class _RedactKeyFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        try:
            msg = record.getMessage()
        except Exception:  # pragma: no cover - message mal formé : laissé tel quel
            return True
        if "api_key=" in msg:
            record.msg, record.args = redact(msg), ()
        return True


_FILTER = _RedactKeyFilter()
for _name in ("httpx", "httpcore"):
    if _FILTER not in logging.getLogger(_name).filters:
        logging.getLogger(_name).addFilter(_FILTER)


def unavailable(probleme: str, maj: str | None = None) -> dict:
    """Contexte « indisponible » au format du contrat d'API (/api/dashboard → marche.contexte_macro)."""
    return {"disponible": False, "maj": maj, "source": SOURCE, "note": NOTE, "probleme": probleme, "series": []}


def parse_value(raw) -> float | None:
    """« . » (convention FRED pour une valeur manquante), vide ou illisible → None ; jamais remplacé par 0."""
    if raw is None:
        return None
    raw = str(raw).strip()
    if raw in ("", "."):
        return None
    try:
        v = float(raw)
    except ValueError:
        return None
    return v if v == v and v not in (float("inf"), float("-inf")) else None


def fetch_observations(client: httpx.Client, api_key: str, series_id: str, start: date) -> list[tuple[str, float | None]]:
    """Observations (date, valeur ou None) d'une série, par date croissante. Lève FredError (message sûr)."""
    params = {"series_id": series_id, "api_key": api_key, "file_type": "json",
              "observation_start": start.isoformat(), "sort_order": "asc"}
    try:
        r = client.get(API_URL, params=params, timeout=TIMEOUT_S)
    except httpx.TimeoutException:
        raise FredError(f"délai de {TIMEOUT_S:.0f} s dépassé") from None
    except httpx.HTTPError as e:  # réseau, DNS, TLS, proxy… : str(e) peut contenir l'URL, donc jamais repris
        raise FredError(f"erreur réseau ({type(e).__name__})") from None
    if r.status_code != 200:
        detail = ""
        try:
            body = r.json()
            if isinstance(body, dict) and body.get("error_message"):
                detail = " : " + redact(str(body["error_message"]), api_key)[:200]
        except ValueError:
            pass
        raise FredError(f"HTTP {r.status_code}{detail}")
    try:
        data = r.json()
    except ValueError:
        raise FredError("réponse illisible (JSON attendu)") from None
    obs = data.get("observations") if isinstance(data, dict) else None
    if not isinstance(obs, list):
        raise FredError("réponse sans observations")
    out = []
    for o in obs:
        if isinstance(o, dict) and isinstance(o.get("date"), str):
            out.append((o["date"], parse_value(o.get("value"))))
    return out


def summarize(serie: Serie, obs: list[tuple[str, float | None]]) -> dict:
    """Dernière valeur valide et variation sur 5 jours ouvrés.

    variation_5j = dernière valeur valide − valeur valide 5 observations plus tôt (valeurs « . » ignorées) ; pour ces
    séries quotidiennes de jours ouvrés, cela couvre environ une semaine. Même unité que la série (points de %
    pour les taux, points d'indice pour le dollar). None s'il n'y a pas 6 valeurs valides."""
    valid = [(d, v) for d, v in obs if v is not None]
    if not valid:
        raise FredError("aucune valeur publiée sur la période")
    d, v = valid[-1]
    var = round(v - valid[-6][1], serie.decimales) if len(valid) >= 6 else None
    return {"id": serie.id, "nom": serie.nom, "valeur": round(v, serie.decimales), "unite": serie.unite, "date": d,
            "variation_5j": var, "url": serie.url}


def build_context(api_key: str, *, client: httpx.Client | None = None, now: datetime | None = None,
                  series: tuple[Serie, ...] = SERIES) -> dict:
    """Interroge FRED et renvoie le contexte au format du contrat. Ne lève jamais d'exception réseau.

    - clé absente : aucune requête, ``disponible`` False avec le problème explicite ;
    - certaines séries en erreur : les autres sont affichées, ``probleme`` liste les séries manquantes ;
    - toutes en erreur : ``disponible`` False, ``maj`` None (l'appelant conserve la date du dernier succès)."""
    if not api_key:
        return unavailable(KEY_MISSING)
    now = now or datetime.now(timezone.utc)
    start = now.date() - timedelta(days=LOOKBACK_DAYS)
    own = client is None
    client = client or httpx.Client(timeout=TIMEOUT_S, headers={"User-Agent": USER_AGENT})
    rows, errors = [], []
    try:
        for serie in series:
            try:
                rows.append(summarize(serie, fetch_observations(client, api_key, serie.id, start)))
            except FredError as e:
                errors.append(f"{serie.id} ({redact(str(e), api_key)})")
    finally:
        if own:
            client.close()
    if not rows:
        return unavailable("FRED injoignable ou en erreur : " + "; ".join(errors))
    return {"disponible": True, "maj": now.astimezone(timezone.utc).isoformat(), "source": SOURCE, "note": NOTE,
            "probleme": ("Série(s) indisponible(s) : " + "; ".join(errors)) if errors else None, "series": rows}


def dashboard_view(raw: dict | None) -> dict:
    """Valeur stockée (KV « macro_context ») → forme exacte du contrat, même si la base est vide ou ancienne."""
    if not isinstance(raw, dict):
        return unavailable(NOT_YET)
    base = {**unavailable(NOT_YET), "probleme": None}
    out = {k: raw.get(k, base[k]) for k in base}
    out["source"], out["note"] = SOURCE, NOTE
    out["disponible"] = bool(out["disponible"])
    out["series"] = out["series"] if isinstance(out["series"], list) else []
    return out


def read_for_dashboard() -> dict:
    """Lecture pour /api/dashboard (session de base de données propre, lecture seule)."""
    from .. import db

    with db.session() as s:
        return dashboard_view(db.kv_get(s, "macro_context"))
