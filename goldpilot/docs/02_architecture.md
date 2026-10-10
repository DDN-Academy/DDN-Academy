# 02 — Architecture technique

Mis à jour le 10 octobre 2026 pour correspondre au code (`backend/goldpilot/`).

## Vue d'ensemble

```
 TradingView (ton graphique MGC daté, 1 min)     Calendrier officiel        Contexte (information seulement)
 script Pine v6 « GoldPilot Bridge »             BLS .ics / BEA / FOMC      FRED (taux réels, taux, dollar)
        │  webhook JSON chaque minute (HTTPS + jeton)      │                      │
        ▼                                                   ▼                      ▼
 ┌──────────────── service « web » (FastAPI) ───────────┐   ┌──────── service « engine » (worker Python) ───────┐
 │ /api/webhooks/tradingview : valide (jeton, IP,       │   │ 1. lit les nouvelles barres 1 min (base)            │
 │   taille, schéma), déduplique, enregistre, répond 200│   │ 2. contrôle qualité (fraîcheur, retard, contrat,    │
 │ /api/* : tableau de bord, signaux, journal, réglages │   │    saut de prix)                                    │
 │ sert le site (React compilé)                         │   │ 3. agrège en barres de décision de 15 min           │
 │ authentification, limites de débit, en-têtes sécu   │   │ 4. stratégie : contexte → setup → invalidation      │
 └──────────────────────┬───────────────────────────────┘   │ 5. moteur de risque (prioritaire, peut tout bloquer)│
                        │      PostgreSQL (SQLite en dev)    │ 6. calendrier / horaires / coûts / compte           │
                        └────────────► (état + journal) ◄────┤ 7. cycle de vie des signaux et position simulée     │
                                                             │ 8. notifications Telegram idempotentes              │
                                                             │ 9. journal d'audit de chaque décision               │
                                                             │ + contrôle croisé TradingView, seuils de suspension │
                                                             └─────────────────────────────────────────────────────┘
                                         Telegram ──► ton téléphone
```

Le site web et le moteur sont deux processus distincts issus de la même image Docker : si le site
plante, le moteur continue ; si le moteur plante, le site affiche « Moteur injoignable » / « Arrêté »
(aucun signe de vie depuis plus d'une minute). Ils communiquent uniquement par la base de données
(simple, durable, inspectable).

## Choix et justifications

| Domaine | Choix | Pourquoi (fiabilité, latence, coût, maintenance) | Alternatives écartées |
|---|---|---|---|
| Moteur quantitatif | Python 3.12+, pandas/numpy | Le **même code** sert au backtest et à la production (parité vérifiée par `tests/test_e2e_parity.py`) | Réécrire la stratégie en TypeScript : double maintenance, risque d'écart |
| API + webhooks | FastAPI | Validation stricte des données (pydantic) ; le webhook enregistre et répond immédiatement (TradingView coupe à 3 s) | Django (plus lourd), Node (deux langages côté serveur) |
| Moteur temps réel | Processus Python séparé, boucle toutes les 2 s | Isolé du web ; redémarre seul (Docker `restart`) ; état entièrement en base | Celery/Redis : pièces en plus sans bénéfice à ce volume (1 barre/minute) |
| Base de données | PostgreSQL 16 + migrations Alembic en production ; SQLite pour le développement et les tests | Transactions, contraintes d'unicité (idempotence), sauvegardes `pg_dump` standard ; le serveur refuse de démarrer en production sans PostgreSQL | SQLite en production (accès concurrents web + moteur moins sûrs) |
| Interface | React + TypeScript (Vite), compilée en fichiers statiques servis par FastAPI | Typage, composants simples, une seule origine (pas de CORS), aucun serveur Node en production | Next.js : rendu serveur inutile pour un tableau de bord privé |
| Notifications | Bot Telegram | Gratuit, notification fiable sur iPhone/Android sans installation spéciale, historique consultable | Web Push (iPhone : uniquement si le site est ajouté à l'écran d'accueil), SMS (payant), e-mail (lent) |
| HTTPS | Caddy (certificats Let's Encrypt automatiques) | Zéro configuration manuelle de certificats, renouvellement automatique | Nginx + certbot (plus de manipulations) |
| Déploiement | Docker Compose sur un VPS | Fonctionne 24 h/24 sans ton ordinateur ; reproductible ; sauvegardes quotidiennes | Hébergement « serverless » (pas de processus permanent), ordinateur personnel (s'éteint) |
| Secrets | variables d'environnement (`.env` hors Git, droits 600) | Jamais dans le code ni dans le dépôt (publié sur GitHub Pages) | Gestionnaire de secrets cloud : utile à plus grande échelle |

## Modules du code (`backend/goldpilot/`)

| Module | Rôle |
|---|---|
| `marketdata/` | réception des barres (webhook TradingView `tradingview.py`, Databento optionnel `databento_feed.py`, rejeu historique `replay.py`), contrôle qualité `quality.py`, calendrier des échéances MGC `contracts.py` |
| `research/` (+ dossier `research/` racine) | chargement des données historiques, moteur de backtest, simulateur d'exécution, métriques, Monte-Carlo |
| `strategy/` | indicateurs causaux, setups S1/S2, invalidations — code unique recherche/production |
| `risk/` | règles FundedNext (valeur, source, statut de chaque règle : `rules.py`), état du compte, dimensionnement, contrôles bloquants (`engine.py`) |
| `signals/` | cycle de vie (en attente → actif → clôturé / annulé / expiré), position simulée, stop suiveur, sorties |
| `calendar/` | événements économiques officiels, fenêtres de restriction |
| `notify/` | textes des alertes (`messages.py`), envoi Telegram idempotent avec réessais (`telegram.py`) |
| `context/` | contexte macro FRED (`fred.py`) : **information seulement**, jamais lu par la stratégie ni le risque |
| `api/` | routes HTTP (`app.py`), authentification, webhooks, sécurité (`security.py`) |
| `engine/` | orchestration temps réel (`runner.py`), configuration de production (`strategy_config.py`) |
| `config.py` | toutes les variables d'environnement (liste commentée : `deploy/.env.example`) |

## États du moteur (affichés tels quels sur le site)

Source : `engine/runner.py` (`_update_mode`, `_performance_guard`, `main`) et `marketdata/quality.py`.

* **Préchauffage** : moins de 45 barres de 15 minutes du contrat actif disponibles ; aucun signal.
* **Actif** (« Surveille le marché ») : le moteur analyse chaque barre de 15 minutes et peut émettre un signal.
* **En pause** : tu as cliqué « Suspendre les signaux » ; reprise par « Reprendre les signaux ».
* **Mode sécurisé** (automatique, pendant les heures de marché) : un problème **bloquant** de données —
  aucune donnée reçue ; données périmées (dernière barre terminée depuis plus de 3 minutes) ; contrat reçu
  différent du contrat actif ; retard médian des webhooks supérieur à 3 minutes (forfait temps réel absent ?) ;
  saut de prix anormal (plus de 15 fois l'amplitude médiane entre deux barres). Les signaux **en attente**
  sont annulés (une position simulée déjà ouverte continue d'être suivie), un incident est ouvert et une
  alerte « Mode sécurisé : aucun signal » est envoyée. Retour automatique quand les données redeviennent
  bonnes (« Données rétablies »). Une heure incomplète (moins de 75 % des barres) est seulement « dégradée ».
* **Arrêt de sécurité** (reprise **manuelle** obligatoire, bouton de la page d'accueil) : déclenché
  (1) quand les signaux clôturés de la version en cours franchissent un **seuil de suspension
  pré-établi** — drawdown ≤ −27,27 R ou série de 17 pertes (`production.json`, `seuils_suspension`) —
  avec incident critique et alerte « Arrêt de sécurité » ; (2) affiché aussi quand aucune stratégie n'est
  configurée (`research/output/final/production.json` absent).
* **Erreur interne du moteur** : une exception dans la boucle ouvre un incident critique et envoie
  « Erreur du moteur » ; aucun signal n'est produit tant que l'erreur se répète ; « Moteur rétabli » est
  envoyé au retour à la normale (reprise automatique, pas un arrêt de sécurité).

Ce qui **n'est pas** un changement d'état mais un refus de signal par le moteur de risque (`risk/engine.py`) :
limite de perte journalière interne, nombre de trades ou de pertes du jour, verrouillage de consistance,
compte violé, coussin insuffisant, horaires FundedNext, annonce économique proche (pas d'entrée si la
fenêtre [annonce − 10 min ; annonce + 15 min] chevauche les 30 prochaines minutes), prix sorti de la plage
d'entrée, doublon, une position à la fois. Un état du compte inconnu n'est pas bloquant : le moteur applique
une hypothèse prudente et l'écrit dans la décision. Si le calendrier BLS en ligne est injoignable, un
incident est ouvert et les dates officielles intégrées sont utilisées.

## Protections transversales

* **Contrôle croisé TradingView ↔ moteur** (`engine/runner.py`, `_check_mirrors`) : le script Pine calcule
  de son côté les franchissements de la stratégie S1 et les envoie comme signaux « miroir ». Le moteur les
  compare à ses propres décisions ; un désaccord (ou un signal du moteur non confirmé par TradingView)
  ouvre un incident et envoie « Contrôle croisé TradingView en désaccord ». Le miroir n'est **jamais
  décisionnel**.
* **Garde anti-alerte périmée** (`notify/telegram.py`, `deliver_pending`) : au moment de l'envoi, une
  alerte de signal ou de déplacement de stop n'est pas envoyée si le signal n'est plus exploitable
  (clôturé, annulé, expiré, validité dépassée, prix sorti de la plage) ; elle est marquée « périmée ».
  Envoi idempotent (clé unique par notification), jusqu'à 5 essais avec attente progressive.
* **Contexte macro** (`context/fred.py`) : taux réels, taux nominaux et dollar (FRED), rafraîchi toutes
  les 6 h si `FRED_API_KEY` est défini ; affiché sur la page Statistiques ; **sans effet** sur les signaux
  (vérifié par `tests/test_macro_context.py`).
* **Rappel de roll** : alerte « Changement d'échéance à venir » 3 jours ouvrés avant la date de roll
  (5 jours ouvrés avant le premier jour d'avis).

## Mode simulation et mode réel

Par défaut tout fonctionne en **simulation** : les alertes sont marquées « SIMULATION — NE PAS EXÉCUTER
SUR LE COMPTE ». Le passage en mode réel (`PUT /api/settings/trading-mode`) est refusé tant que :
1. la stratégie n'est pas validée (`production.json`, `"validated": false` aujourd'hui) ;
2. tu n'as pas déclaré la **confirmation écrite de FundedNext** avec sa référence (règle « signaux
   externes » marquée « contradictoire » dans `risk/rules.py`) ; même en mode réel, le contrôle
   « Règles incertaines » du moteur de risque bloque tout signal réel sans cette confirmation ;
3. la phrase exacte « JE CONFIRME LE PASSAGE EN REEL » n'est pas saisie.
Retirer la confirmation FundedNext repasse automatiquement en simulation.
