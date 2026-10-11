# 02 — Architecture technique

Mis à jour le 11 octobre 2026 pour correspondre au code (`backend/goldpilot/`).

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
| Secrets | variables d'environnement (`.env` hors Git, droits 600) | Jamais dans le code ni dans le dépôt : la branche `main`/`master` du dépôt est publiée sur GitHub Pages (GoldPilot vit sur `claude/goldpilot` et ne doit pas y être fusionné, `05` § 4) | Gestionnaire de secrets cloud : utile à plus grande échelle |

## Modules du code (`backend/goldpilot/`)

| Module | Rôle |
|---|---|
| `marketdata/` | réception des barres (webhook TradingView `tradingview.py`, Databento optionnel `databento_feed.py`, rejeu historique `replay.py`), contrôle qualité `quality.py`, calendrier des échéances MGC `contracts.py` (mois actifs février, avril, juin, août, octobre, décembre : roll août → octobre → décembre) |
| `research/` (+ dossier `research/` racine) | chargement des données historiques, moteur de backtest, simulateur d'exécution, métriques, Monte-Carlo |
| `strategy/` | indicateurs causaux, setups S1/S2, invalidations — code unique recherche/production |
| `risk/` | règles FundedNext (valeur, source, statut de chaque règle : `rules.py`), état du compte, dimensionnement, contrôles bloquants (`engine.py`) |
| `signals/` | cycle de vie (en attente → actif → clôturé / annulé / expiré), position simulée, stop suiveur, sorties |
| `calendar/` | événements économiques officiels, fenêtres de restriction |
| `notify/` | textes des alertes (`messages.py`), envoi Telegram idempotent avec réessais (`telegram.py`) |
| `context/` | contexte macro FRED (`fred.py`) : **information seulement**, jamais lu par la stratégie ni le risque |
| `api/` | routes HTTP (`app.py`), authentification, webhooks, sécurité (`security.py`) |
| `engine/` | orchestration temps réel (`runner.py`), configuration de production (`strategy_config.py`) |
| `timeutil.py` | heures New York/Paris, séances, **jours fériés et clôtures anticipées CME** (métaux), dernière réouverture du marché |
| `config.py` | toutes les variables d'environnement (liste commentée : `deploy/.env.example`) |

## Source des prix

Une seule source pilote les décisions et le suivi des signaux (`engine/runner.py`, `source_filter`) :
`DATA_SOURCE=tradingview` (par défaut) → barres du webhook TradingView ; `DATA_SOURCE=databento` → barres
Databento, les barres TradingView ne servant plus qu'au **contrôle croisé des prix** (clôture comparée
minute par minute ; écart supérieur à **1,00 $**, seuil de prudence non validé, `CROSS_CHECK_TOL` →
incident « Sources de prix en désaccord »). **Aucune bascule automatique** d'une source à l'autre : si la
source principale tombe, le moteur passe en mode sécurisé. Une barre arrivée **après une barre plus
récente** (renvoi tardif) n'est jamais appliquée au suivi des signaux ; elle complète seulement le créneau
de 15 minutes encore ouvert.

## Horaires du marché (`timeutil.py`)

* Séance CME de l'or : 18:00 → 17:00 New York, pause quotidienne 17:00-18:00, week-end fermé.
* **Jours fériés CME (métaux)** : fermeture complète (Jour de l'an, Vendredi saint, Noël) ou arrêt
  anticipé à 13:00 New York (MLK, Presidents' Day, Memorial Day, Juneteenth, Independence Day, Labor Day,
  Thanksgiving) ou clôture anticipée à 13:45 New York (lendemain de Thanksgiving, veille de Noël). La page
  d'accueil affiche alors « fermé (jour férié) » ou « fermé (clôture anticipée) ». Ces dates ont été
  calculées par règle à partir de sources consultées le 11/10/2026 et sont **à vérifier chaque année** sur
  le calendrier officiel <https://www.cmegroup.com/trading-hours.html> (horaires 2026-2027 non confirmés sur
  la page officielle ; le 1er janvier 2027 est traité comme fermé, choix prudent).
* **Réouverture de 18:00** : la fraîcheur des données est mesurée depuis la plus récente des deux dates,
  fin de la dernière barre ou dernière réouverture du marché (après la pause, le week-end ou un jour
  férié) : la réouverture ne déclenche pas de faux mode sécurisé.

## États du moteur (affichés tels quels sur le site)

Source : `engine/runner.py` (`_update_mode`, `_performance_guard`, `_governance`, `main`) et
`marketdata/quality.py`. L'état est recalculé **avant chaque décision de 15 minutes** (jamais l'état du
passage précédent).

* **Préchauffage** : moins de 45 barres de 15 minutes du contrat actif disponibles ; aucun signal.
* **Actif** (« Surveille le marché ») : le moteur analyse chaque barre de 15 minutes et peut émettre un signal.
* **En pause** : tu as cliqué « Suspendre les signaux » ; reprise par « Reprendre les signaux ».
* **Mode sécurisé** (automatique, pendant les heures de marché) : un problème **bloquant** de données —
  aucune donnée reçue ; données périmées (dernière barre terminée depuis plus de 3 minutes, comptées depuis
  la réouverture si elle est plus récente) ; contrat reçu différent du contrat actif ; retard médian des
  webhooks supérieur à 3 minutes (forfait temps réel absent ?) ; saut de prix anormal (plus de 15 fois
  l'amplitude médiane entre deux barres). Effets : les signaux **non entrés** sont annulés (signaux en
  attente **et** signaux actifs dont l'entrée simulée n'a pas eu lieu) avec l'alerte « Signal annulé — ne
  pas entrer » ; une position simulée déjà ouverte reste suivie, mais tu reçois « Ne plus entrer » si sa
  fenêtre d'entrée était encore ouverte et « Position ouverte, données interrompues » (surveille-la sur
  Tradovate, heure limite de fermeture rappelée) ; un incident est ouvert et l'alerte « Mode sécurisé :
  aucun signal » est envoyée. Retour automatique quand les données redeviennent bonnes (« Données
  rétablies »). Une heure incomplète (moins de 75 % des barres) est seulement « dégradée ».
* **Arrêt de sécurité** (aucun signal ; reprise **manuelle** obligatoire) : déclenché
  1. quand les signaux clôturés de la version en cours franchissent un **seuil de suspension pré-établi** —
     drawdown ≤ −27,27 R ou série de 17 pertes (`production.json`, `seuils_suspension`) — avec incident
     critique et alerte « Arrêt de sécurité ». Reprise par le bouton de la page d'accueil
     (`POST /api/engine/resume-after-halt`) : un **point de reprise** est enregistré et les seuils sont
     ensuite **recomptés uniquement sur les trades clôturés après la reprise** (sinon l'ancien drawdown
     redéclencherait l'arrêt aussitôt) ;
  2. quand la **version de stratégie** en service diffère de la version approuvée (gouvernance, voir
     ci-dessous) : alerte « Arrêt de sécurité : nouvelle version de stratégie ». Le bouton de reprise est
     alors refusé ; seule l'approbation de la version lève cet arrêt ;
  3. affiché aussi quand aucune stratégie n'est configurée (`research/output/final/production.json` absent).
* **Erreur interne du moteur** : une exception dans la boucle annule la transaction, **restaure l'état en
  mémoire** (les mêmes barres sont retraitées au passage suivant, aucune décision de 15 min perdue), ouvre
  un incident critique et envoie « Erreur du moteur » ; aucun signal n'est produit tant que l'erreur se
  répète ; « Moteur rétabli » est envoyé au retour à la normale (reprise automatique, pas un arrêt de sécurité).

Ce qui **n'est pas** un changement d'état mais un refus de signal par le moteur de risque (`risk/engine.py`) :
limite de perte journalière interne, nombre de trades ou de pertes du jour, verrouillage de consistance,
compte violé, coussin insuffisant, **horaires** (sortie prévue au plus tard à min(15:45 New York, clôture
réelle du CME − 25 min) : 12:35 New York un jour d'arrêt à 13:00, 13:20 un jour de clôture à 13:45 ; aucun
signal un jour férié fermé), annonce économique proche (pas d'entrée si la fenêtre [annonce − 10 min ;
annonce + 15 min] chevauche les 30 prochaines minutes), prix sorti de la plage d'entrée, doublon, une
position à la fois. La **taille** est calculée sur la **pire entrée** de la plage acceptable (entrée prévue
± 0,5 ATR, du côté opposé au stop) : même en entrant au bord de la plage, le risque ne dépasse pas le
budget. Un état du compte inconnu n'est pas bloquant : le moteur applique une hypothèse prudente et
l'écrit dans la décision. Si le calendrier BLS en ligne est injoignable, un incident est ouvert et les
dates officielles intégrées sont utilisées.

## Cycle de vie des signaux à l'horloge (`signals/manager.py`, `on_clock`)

Le suivi simulé avance normalement à chaque barre. Si les barres n'arrivent plus (flux coupé, marché
arrêté), l'horloge prend le relais 3 minutes après l'échéance : un signal jamais entré dont la validité est
écoulée passe **Expiré** ; une position simulée ouverte dont l'heure limite de sortie est passée est
**clôturée « sortie temporelle (sans données) »** avec l'alerte « Fermer la position maintenant ». Le prix
de sortie étant inconnu, **aucun résultat n'est inventé** : prix de sortie, R et P&L restent vides (ce trade
n'entre pas dans les calculs en R : seuils de suspension, revue hebdomadaire).

## Compte simulé (suivi papier)

Le compte simulé applique les règles FundedNext Flex 50K aux signaux simulés : plancher trailing en fin
de journée et **perte latente** : à chaque barre, la perte flottante au pire extrême de la barre (plus bas
pour un achat, plus haut pour une vente) est comparée au plancher ; si elle l'atteint, le compte simulé
est marqué **violé** et l'alerte « Compte simulé : perte maximale atteinte (latente) » est envoyée
(`engine/runner.py`, `_check_floating_loss`).

## Gouvernance des versions et revue périodique

* **Approbation des versions** (`_governance`, `GET /api/strategy/governance`, `POST /api/strategy/approve`) :
  à la première mise en service, la version de `production.json` est enregistrée comme approuvée
  (« initialisation »). Si une nouvelle version est déployée, le moteur se met en **arrêt de sécurité**
  (type « version ») jusqu'à ce que tu compares puis approuves cette version dans **Réglages › Gouvernance
  de la stratégie**, en recopiant exactement la phrase **« J'APPROUVE CETTE VERSION »**. Le serveur refuse
  (409) toute version autre que celle en service. L'approbation est journalisée (Journal › Audit). Approuver
  une version **ne la valide pas** : le mode réel reste verrouillé.
* **Revue hebdomadaire** (`_periodic_review`) : chaque **samedi** (date de New York), le moteur calcule
  sur les trades simulés clôturés de la version en service : nombre de trades, espérance en R, borne basse
  unilatérale à 95 %, drawdown maximal, plus longue série de pertes, taux de gain, comparés aux résultats
  de la recherche et aux seuils de suspension. Résultat sur la page Statistiques et dans Réglages ›
  Gouvernance, et alerte Telegram « Revue hebdomadaire des performances ». En dessous de 30 trades, la
  conclusion est « échantillon trop petit pour conclure ». **Information seulement : la stratégie n'est
  jamais modifiée automatiquement.**

## Protections transversales

* **Webhook TradingView durci** (`api/app.py`, `marketdata/tradingview.py`, `api/security.py`) : adresse IP
  d'envoi vérifiée, message limité à 4 096 octets, JSON strict (NaN et Infinity refusés), schéma fermé,
  jeton comparé en temps constant et jamais journalisé, prix et volumes bornés, horodatages plausibles
  (2010-2100, pas plus de 2 min dans le futur, pas plus de 3 jours dans le passé), barre sur une minute
  ronde, contrat MGC daté uniquement, doublons ignorés. Les messages **refusés** sont limités par adresse IP
  (au-delà, ils ne sont plus journalisés) et les messages **authentifiés** ont leur propre budget : comme
  TradingView envoie depuis 4 adresses partagées par tous ses utilisateurs, un tiers ne peut pas faire
  refuser tes vraies barres. Une erreur d'écriture du journal ne transforme jamais la réponse en erreur 500.
* **Contrôle croisé TradingView ↔ moteur** (`engine/runner.py`, `_check_mirrors`) : le script Pine calcule
  de son côté les franchissements de la stratégie S1 et les envoie comme signaux « miroir ». Le moteur les
  compare à ses propres décisions ; un désaccord (ou un signal du moteur non confirmé par TradingView)
  ouvre un incident et envoie « Contrôle croisé TradingView en désaccord ». Le miroir n'est **jamais
  décisionnel**.
* **Garde anti-alerte périmée** (`notify/telegram.py`, `deliver_pending`) : au moment de l'envoi, une
  alerte de signal ou de déplacement de stop n'est pas envoyée si le signal n'est plus exploitable
  (clôturé, annulé, expiré, validité dépassée, prix sorti de la plage, « ne plus entrer ») ; une alerte de
  nouveau signal n'est pas envoyée non plus si le moteur est en mode sécurisé, en arrêt de sécurité ou en
  pause. Elle est marquée « périmée ». Envoi idempotent (clé unique par notification), jusqu'à 5 essais
  avec attente progressive (≈ 3 minutes au total).
* **Niveaux dans les alertes** : chaque signal enregistre les niveaux de contexte (plus haut / plus bas de la
  veille et de la séance, dernier sommet / creux de 15 minutes, distance au prix en ATR) ; l'alerte
  Telegram les affiche sur une ligne « Niveaux : » (`notify/messages.py`, `levels_line`).
* **Tuile « Notifications »** de l'accueil (`frontend/src/lib/status.ts`) : verte (« Opérationnelles »)
  **seulement** si Telegram est configuré, les notifications sont actives et le **dernier envoi a réussi**
  sans nouvel essai en cours ; orange si non configurées, désactivées par toi ou **jamais vérifiées**
  (aucun envoi encore tenté : utilise « Tester une notification ») ; rouge (« En erreur ») si le dernier
  envoi a échoué (ou échoue encore pendant les nouveaux essais). Si le serveur ne répond plus, l'état est « inconnu »,
  jamais vert.
* **Contexte macro** (`context/fred.py`) : taux réels, taux nominaux et dollar (FRED), rafraîchi toutes
  les 6 h si `FRED_API_KEY` est défini ; affiché sur la page Statistiques ; **sans effet** sur les signaux
  (vérifié par `tests/test_macro_context.py`).
* **Rappel de roll** : alerte « Changement d'échéance à venir » 3 jours ouvrés avant la date de roll
  (5 jours ouvrés avant le premier jour d'avis). Mois actifs : février, avril, juin, août, octobre,
  décembre (roll août → octobre → décembre).

## Mode simulation et mode réel

Par défaut tout fonctionne en **simulation** : les alertes sont marquées « SIMULATION — NE PAS EXÉCUTER
SUR LE COMPTE ». Le passage en mode réel (`PUT /api/settings/trading-mode`) est refusé tant que :
1. la stratégie n'est pas validée (`production.json`, `"validated": false` aujourd'hui) ;
2. tu n'as pas déclaré la **confirmation écrite de FundedNext** avec sa référence (règle « signaux
   externes » marquée « contradictoire » dans `risk/rules.py`) ; même en mode réel, le contrôle
   « Règles incertaines » du moteur de risque bloque tout signal réel sans cette confirmation ;
3. la phrase exacte « JE CONFIRME LE PASSAGE EN REEL » n'est pas saisie.
Retirer la confirmation FundedNext repasse automatiquement en simulation.
