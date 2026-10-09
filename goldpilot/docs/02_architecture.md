# 02 — Architecture technique

## Vue d'ensemble

```
 TradingView (ton graphique MGC actif)          Calendrier officiel        Contexte
 script Pine v6 « GoldPilot Bridge »            BLS .ics / BEA / FOMC      FRED (taux, dollar)
        │  webhook JSON chaque minute (HTTPS + jeton)      │                      │
        ▼                                                   ▼                      ▼
 ┌──────────────── service « web » (FastAPI) ───────────┐   ┌──────── service « engine » (worker Python) ───────┐
 │ /api/webhooks/tradingview : valide, déduplique,      │   │ 1. lit les nouvelles barres 1 min (base)            │
 │   enregistre en < 50 ms, répond 200                  │   │ 2. contrôle qualité (fraîcheur, trous, contrat)     │
 │ /api/* : tableau de bord, signaux, journal, réglages │   │ 3. agrège en barres de décision                     │
 │ sert le site (React compilé)                         │   │ 4. contexte → setup → déclencheur → invalidation    │
 │ authentification, limites de débit, en-têtes sécu   │   │ 5. moteur de risque (prioritaire, peut tout bloquer)│
 └──────────────────────┬───────────────────────────────┘   │ 6. calendrier / restrictions / coûts                │
                        │            PostgreSQL              │ 7. cycle de vie des signaux (attente → actif → clos)│
                        └────────────► (état + journal) ◄────┤ 8. notifications Telegram idempotentes              │
                                                             │ 9. journal d'audit de chaque décision               │
                                                             │ chien de garde : mode sécurisé si anomalie          │
                                                             └─────────────────────────────────────────────────────┘
                                         Telegram ──► ton téléphone
```

Le site web et le moteur sont deux processus distincts issus de la même image Docker : si le site
plante, le moteur continue ; si le moteur plante, le site affiche l'état « moteur arrêté » en rouge.
Ils communiquent uniquement par la base PostgreSQL (simple, durable, inspectable).

## Choix et justifications

| Domaine | Choix | Pourquoi (fiabilité, latence, coût, maintenance) | Alternatives écartées |
|---|---|---|---|
| Moteur quantitatif | Python 3.12, pandas/numpy | Le **même code** sert au backtest et à la production : aucune divergence recherche/réel | Réécrire la stratégie en TypeScript : double maintenance, risque d'écart |
| API + webhooks | FastAPI | Validation stricte des données (pydantic), rapide (< 50 ms par webhook, TradingView coupe à 3 s) | Django (plus lourd), Node (deux langages côté serveur) |
| Moteur temps réel | Processus Python séparé, boucle événementielle 1 s | Isolé du web ; redémarre seul (Docker `restart: always`) ; état entièrement en base | Celery/Redis : pièces en plus sans bénéfice à ce volume (1 barre/minute) |
| Base de données | PostgreSQL 16 + migrations Alembic | Transactions, contraintes d'unicité (idempotence), sauvegardes `pg_dump` standard | SQLite (accès concurrents web + moteur moins sûrs), base temps réel spécialisée (inutile : ~1 400 barres/jour) |
| Interface | React + TypeScript (Vite), compilée en fichiers statiques servis par FastAPI | Typage, composants simples, une seule origine (pas de CORS), aucun serveur Node en production | Next.js : rendu serveur inutile pour un tableau de bord privé, un service de plus à maintenir |
| Notifications | Bot Telegram | Gratuit, notification fiable sur iPhone/Android sans installation spéciale, historique consultable | Web Push (iPhone : uniquement si le site est ajouté à l'écran d'accueil), SMS (payant), e-mail (lent) |
| HTTPS | Caddy (certificats Let's Encrypt automatiques) | Zéro configuration manuelle de certificats, renouvellement automatique | Nginx + certbot (plus de manipulations) |
| Déploiement | Docker Compose sur un VPS | Fonctionne 24 h/24 sans ton ordinateur ; reproductible ; sauvegardes quotidiennes | Hébergement « serverless » (pas de processus permanent), ordinateur personnel (s'éteint) |
| Secrets | variables d'environnement (`.env` hors Git, droits 600) | Jamais dans le code ni dans le dépôt (publié sur GitHub Pages) | Gestionnaire de secrets cloud : utile à plus grande échelle, documenté en option |

## Modules du code (`backend/goldpilot/`)

| Module | Rôle |
|---|---|
| `marketdata/` | réception des barres (webhook TradingView, Databento optionnel, rejeu historique), contrôle qualité, agrégation, calendrier des échéances MGC |
| `research/` (+ dossier `research/` racine) | chargement des données historiques, moteur de backtest, métriques, Monte-Carlo |
| `strategy/` | indicateurs causaux, détection du régime, setups, déclencheurs, invalidations — code unique recherche/production |
| `risk/` | règles FundedNext Flex 50K (sources et statut), état du compte, dimensionnement, coupe-circuits |
| `signals/` | cycle de vie, idempotence, suivi des positions simulées, gestion des sorties |
| `calendar/` | événements économiques officiels, fenêtres de restriction |
| `notify/` | Telegram (envoi idempotent, réessais, journal) |
| `api/` | routes HTTP, authentification, webhooks, sécurité |
| `engine/` | orchestration temps réel, chien de garde, modes (préchauffage, actif, pause, sécurisé, arrêté) |

## États du système (affichés tels quels sur le site)

* **Préchauffage** : pas assez d'historique reçu pour calculer les indicateurs ; aucun signal.
* **Actif** : toutes les conditions sont réunies ; le moteur peut émettre des signaux.
* **En pause** : tu as suspendu la génération de signaux.
* **Mode sécurisé** (automatique) : données périmées, contrat incorrect, anomalie de prix, calendrier
  indisponible avant une annonce majeure, état du compte inconnu trop longtemps… Aucun signal ; les
  signaux en attente sont annulés et tu es prévenu.
* **Arrêt de sécurité** (automatique, reprise manuelle obligatoire) : erreur interne, dégradation des
  performances au-delà des seuils pré-établis, limite de perte interne atteinte.

## Mode simulation et mode réel

Par défaut tout fonctionne en **simulation** : les alertes sont marquées « SIMULATION » et ne doivent pas
être exécutées. Le passage en mode réel est une décision distincte, protégée par confirmation, refusée
tant que la stratégie n'a pas satisfait les critères de validation (voir le rapport de validation).
