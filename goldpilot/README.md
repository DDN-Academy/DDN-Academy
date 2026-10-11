# GoldPilot

Centre de commande personnel pour le trading de l'or : GoldPilot analyse automatiquement le **Micro Gold
(MGC, COMEX)** à partir de ton graphique TradingView, applique un moteur de risque adapté au challenge
**FundedNext Futures Flex 50K**, et t'envoie des alertes **Telegram** sur ton téléphone. L'exécution reste
**manuelle** (Tradovate) ; GoldPilot ne passe aucun ordre.

> ## Statut : STRATÉGIE NON VALIDÉE — SIMULATION UNIQUEMENT
> Aucune stratégie n'a satisfait les critères de validation fixés à l'avance
> ([rapport de validation](docs/04_rapport_de_validation.md)). Toutes les alertes sont marquées
> « SIMULATION — NE PAS EXÉCUTER SUR LE COMPTE ». Le mode réel est verrouillé par le serveur et exige en
> plus une confirmation écrite de FundedNext. Voir les [limites](docs/08_limites.md).

## Comment ça marche

```
TradingView (script Pine « GoldPilot Bridge », graphique 1 min du MGC daté)
   │ webhook JSON chaque minute (HTTPS + jeton secret)
   ▼
site « web » (FastAPI) ──► base PostgreSQL ◄── « engine » (moteur Python)
   │ tableau de bord React                       qualité des données → stratégie S1 → moteur de risque
   ▼                                              → signaux simulés → alertes Telegram → journal
ton navigateur                                                         │
                                                                       ▼
                                                               ton téléphone
```

Détails : [architecture](docs/02_architecture.md).

## Documentation

| Document | Contenu |
|---|---|
| [01 — Environnement, sources et accès](docs/01_environnement_sources_et_acces.md) | règles FundedNext Flex 50K, contrats COMEX, comparaison XAU/USD-GC-MGC, possibilités réelles de TradingView, services nécessaires, licences des données, banques centrales et géopolitique |
| [02 — Architecture](docs/02_architecture.md) | composants, choix techniques, source des prix, jours fériés CME, modes du moteur, gouvernance des versions |
| [03 — Protocole de recherche](docs/03_protocole_de_recherche.md) | protocole pré-enregistré, critères de validation |
| [04 — Rapport de validation](docs/04_rapport_de_validation.md) | résultats honnêtes, Monte-Carlo, tests exécutés, ce qui reste à faire ; [§ 14 compléments a posteriori](docs/04_rapport_de_validation.md#14-compléments-a-posteriori-ajoutés-le-11102026) (durée des drawdowns, résultats par séance et par régime, espérance en dollars, délai d'exécution) |
| [05 — Déploiement et exploitation](docs/05_deploiement_et_exploitation.md) | mise en ligne sur un serveur, sauvegardes, mises à jour, pannes, approbation d'une nouvelle version, revue du samedi |
| [06 — Guide utilisateur](docs/06_guide_utilisateur.md) | première mise en route (Telegram, TradingView) et usage quotidien |
| [07 — Clés, abonnements et autorisations](docs/07_cles_abonnements_autorisations.md) | tout ce qu'il faut obtenir, obligatoire ou non, coûts indicatifs |
| [08 — Limites](docs/08_limites.md) | ce qui empêche encore une utilisation réelle |
| [Captures d'écran](docs/captures/README.md) | pages du site (données fictives) |

## Structure du dépôt

| Dossier | Contenu |
|---|---|
| `backend/goldpilot/` | code Python : `api/` (site et webhooks), `engine/` (moteur temps réel), `strategy/`, `risk/` (règles FundedNext, dimensionnement, contrôles), `signals/`, `marketdata/` (TradingView, Databento, rejeu, contrats MGC, qualité), `calendar/`, `notify/` (Telegram), `context/` (FRED, information seulement), `research/` (backtest, Monte-Carlo), `config.py` (toutes les variables d'environnement) |
| `backend/tests/` | tests pytest |
| `backend/migrations/` | migrations de base de données (Alembic) |
| `frontend/` | site React + TypeScript (Vite) ; `src/` pages et composants, `e2e/` tests de bout en bout Playwright |
| `pine/` | script Pine v6 `goldpilot_bridge.pine` à installer sur TradingView (non testé sur TradingView) |
| `research/` | scripts et résultats de recherche (`research/output/` : audit, étude exploratoire, sélection, évaluation finale, Monte-Carlo, configuration de production) |
| `deploy/` | Docker Compose, Caddy (HTTPS), `.env.example` commenté, scripts de secrets, sauvegarde, restauration |
| `Dockerfile` | image unique pour le site et le moteur |
| `docs/` | documentation (ci-dessus) |

## Démarrage rapide en développement (sans aucun secret)

Prérequis : Python 3.12+ et Node 22. Le mode « rejeu » rejoue des barres historiques **XAUUSD** (exercice
de la chaîne logicielle uniquement, ce ne sont ni des prix MGC ni des prix actuels).

```bash
# 1. Installation
cd goldpilot/backend
pip install -e ".[dev,research]"
cd ../frontend
npm ci
npm run build            # produit frontend/dist, servi par le serveur Python
cd ../backend

# 2. Configuration de développement (base SQLite locale, rejeu historique, aucun secret réel)
export APP_ENV=development DATABASE_URL=sqlite:////tmp/goldpilot-dev.db DATA_SOURCE=replay \
       REPLAY_FROM=2025-09-01 REPLAY_SPEED=0 TV_ENFORCE_IP=false TV_WEBHOOK_TOKEN=dev-token-0123456789abcdefghij \
       ADMIN_PASSWORD_HASH="$(python -c 'from goldpilot.api.security import hash_password; print(hash_password("motdepasse-dev-123"))')"
python -c "from goldpilot import db; db.init(create=True)"

# 3. Lancement : le moteur rejoue l'historique à pleine vitesse puis garde une horloge virtuelle figée
python -m goldpilot.engine.runner &
python -m uvicorn goldpilot.api.app:app --port 8000 &
```

Ouvre <http://localhost:8000> ; mot de passe de développement : `motdepasse-dev-123`.
Pour l'API : toute écriture exige l'en-tête `X-GoldPilot: 1` et le cookie de session.
Commandes utiles : `python -m goldpilot.cli check` (vérifie la configuration), `python -m goldpilot.cli secret`
(génère un secret), `python -m goldpilot.cli hash-password`, `python -m goldpilot.cli research-summary`.

Vérifié le 10/10/2026 : avec ces commandes, `/api/health` répond `{"web":"ok","moteur":"ok"}`, la connexion
fonctionne et le tableau de bord affiche le moteur « Surveille le marché » avec l'horloge du rejeu.

Production : jamais avec ces réglages (le serveur refuse de démarrer en production avec `DATA_SOURCE=replay`,
SQLite ou des secrets trop courts). Suivre [05 — Déploiement](docs/05_deploiement_et_exploitation.md) : sur un serveur neuf, une seule commande suffit (`deploy/installer.sh`, § 2 bis).

## Tests

```bash
cd goldpilot/backend && python -m pytest -q -p no:cacheprovider   # 279 tests, ~3 min
cd goldpilot/frontend && npm test                                  # 36 tests unitaires (Vitest)
cd goldpilot/frontend && npm run build && npm run test:e2e        # 68 tests de bout en bout (Playwright)
cd goldpilot/frontend && npm run captures                          # régénère docs/captures/
```

Résultats de la dernière exécution et contenu de chaque fichier de tests :
[rapport de validation, § 10](docs/04_rapport_de_validation.md).
Le workflow `.github/workflows/goldpilot-ci.yml` (à la racine du dépôt) relance ces contrôles sur GitHub.

## Sécurité

Aucun secret dans le code ni dans Git : la branche `main`/`master` du dépôt est publiée sur GitHub Pages
(`.github/workflows/deploy.yml`) ; GoldPilot vit sur la branche `claude/goldpilot` et ne doit pas y être
fusionné ([05 — Déploiement, § 4](docs/05_deploiement_et_exploitation.md)). Tous les secrets sont des
variables d'environnement sur le serveur (`deploy/.env.example`). On ne te demande jamais ton mot de passe
TradingView, Tradovate ou FundedNext.
