# 04 — Rapport de validation (cahier des charges § 16, étape E)

Rédigé le 10 octobre 2026. Chaque chiffre cite le fichier dont il est tiré ; rien n'est arrondi « à
l'avantage » de la stratégie.

> **Verdict : STRATÉGIE NON VALIDÉE.** Aucune famille de stratégies n'a satisfait les critères
> pré-enregistrés. GoldPilot fonctionne **uniquement en simulation** : les alertes portent la mention
> « SIMULATION — NE PAS EXÉCUTER SUR LE COMPTE » et le mode réel est verrouillé dans le site.
> Source : `research/output/final/production.json` (`"validated": false`) et `research/output/selection/selection.md`.

---

## 1. Protocole suivi

Le protocole complet est dans [`03_protocole_de_recherche.md`](03_protocole_de_recherche.md). Il a été
écrit **avant** tout backtest des candidats (commit Git `5306e9d` du 09/10/2026 à 18:28 UTC), et sa
section 10 (« suite » après l'échec de la sélection) a été ajoutée **avant** toute lecture de la période
2022-2025 (commit `dbd6736` à 23:50 UTC, résultats 2022-2025 publiés au commit `7108a4e` à 23:52 UTC).

Résumé :
* données : XAUUSD spot en barres de 15 minutes, **proxy non mesuré** du MGC (aucune donnée MGC n'a été
  comparée : base de portage, corrélation intraday, horaires et liquidité non mesurés ; les résultats ne
  sont pas transposables tels quels au MGC — voir § 2 et `08_limites.md`) ;
* découpage chronologique : entraînement 01/05/2011 → 31/12/2018, validation 2019 → 2021,
  test 01/01/2022 → 28/10/2025 ; walk-forward avec années de test 2014 → 2021 ;
* coûts proportionnels au prix calibrés sur un or à 4 000 $ (commission supposée 2 $/contrat aller-retour,
  demi-spread, glissement sur stop et en marché rapide), plus deux tests de stress (coûts × 2, coûts fixes) ;
* exécution simulée prudente (entrée à l'ouverture de la barre suivante, stop d'abord si stop et objectif
  dans la même barre, sortie au pire prix en cas de gap, aucune position après 15:45 New York) ;
* 2 familles candidates, 32 configurations ; Deflated Sharpe Ratio calculé avec 200 essais (32 + 168
  essais d'une session antérieure abandonnée, déclarés par transparence).

## 2. Audit des données

Source : `research/output/audit/audit.md`.

| Fichier | Barres | Période | Contrôles |
|---|---|---|---|
| `data/xau_15m_2004_2025.csv` | 480 717 | 11/06/2004 → 30/09/2025 | ordre croissant, 0 doublon, 0 OHLC incohérent, 0 prix ≤ 0 ; 98,26 % d'intervalles réguliers |
| `data/xauusd_5m_2025.csv` | 50 000 | 13/02/2025 → 28/10/2025 | mêmes contrôles, 99,63 % d'intervalles réguliers, aucun trou > 4 jours |

Constats importants :
* le volume est un **nombre de ticks du courtier**, pas un volume d'échange : aucune stratégie de volume
  n'a été testée ;
* 6 trous de plus de 4 jours dans le fichier 15 min, dont **4 en 2025** (jusqu'à 80,8 jours entre le
  11/07/2025 et le 30/09/2025) : l'année 2025 est incomplète dans ce fichier ;
* fuseau horaire déduit : heure New York = heure du fichier − 6 h (2004-06 → 2011-03) puis − 7 h
  (2011-04 → 2025-07) ; recoupement 15 min / 5 min sur 6 399 barres communes : écart médian de clôture
  0,13 $, 99e centile 8,40 $.

## 3. Étude exploratoire (entraînement seulement)

Source : `research/output/etude_exploratoire/etude.md` (2011-05 → 2018-12). Coût aller-retour médian
≈ 0,114 ATR de 15 min. Pistes retenues : continuité Londres → New York matin (+0,319 ATR, t = 2,4) et
prolongement des fortes extensions de séance (+0,14 à +0,20 ATR sur 2 h, t ≈ 6-7, chiffres rappelés dans
`docs/03` § 4). Pistes écartées : retour à la moyenne en Londres et cassures asiatiques (effets réels mais
inférieurs aux coûts), range d'ouverture New York, balayage du plus haut/bas de la veille.

## 4. Sélection sur 2011-2021 : aucune famille éligible

Source : `research/output/selection/selection.md`.

| Critère pré-enregistré (`docs/03` § 5) | S1 — extension de séance `S1|F=True,k=5.0,s=2.5,t=3.0` | S2 — Londres → New York `S2|E=suivi,q=2.0,s=3.0` |
|---|---|---|
| 1. Walk-forward 2014-2021 : espérance > 0 et borne basse unilatérale 95 % > 0 | ✘ n = 790, +0,081 R, IC95 [−0,019 ; +0,183], borne basse −0,003 | ✘ n = 840, +0,045 R, IC95 [−0,042 ; +0,137], borne basse −0,030 |
| 2. Validation 2019-2021 : espérance > 0 et PF ≥ 1,10 | ✘ +0,030 R, PF 1,06 | ✘ +0,001 R, PF 1,00 |
| 3. Coûts × 2 sur la validation ≥ 0 | ✘ −0,017 R | ✘ −0,038 R |
| 4. ≥ 60 % d'années positives | ✔ 73 % | ✔ 91 % |
| 5. ≥ 70 % de voisins positifs | ✔ 100 % | ✔ 100 % |
| 6. DSR (200 essais) ≥ 0,90 | ✘ 0,005 | ✘ 0,001 |

Conséquence (protocole § 6) : **aucun test final confirmatoire** n'a été exécuté. Le candidat de
simulation est S1 (meilleure borne basse du walk-forward), choisi par la règle fixée à l'avance au § 10 de `docs/03`.

## 5. Évaluation exploratoire 2022-2025 (non confirmatoire)

Source : `research/output/final/final.md` et `final.json`. Candidat `S1|F=True,k=5.0,s=2.5,t=3.0`.

| Coûts | Trades | Espérance (R) | Profit factor | Taux de gain | Drawdown max (R) |
|---|---|---|---|---|---|
| base | 327 | +0,061 | 1,15 | 35 % | −15,3 |
| coûts × 2 | 327 | +0,020 | 1,05 | 35 % | −17,1 |
| coûts fixes | 327 | +0,025 | 1,06 | 35 % | −17,4 |

* **IC95 de l'espérance (base) : [−0,076 ; +0,207] R** ; borne unilatérale basse −0,055 R. Le résultat
  n'est **pas distinguable de zéro**.
* Par année : 2022 +0,102 R (74 trades), 2023 +0,101 R (101), **2024 −0,029 R (83)**, 2025 +0,067 R (69).
* Par sens (`final.json`) : achats 186 trades, +0,070 R ; ventes 141 trades, +0,049 R.
* Contrôle de résolution (13/02/2025 → 28/10/2025, 55 trades) : barres 15 min +0,125 R ; exécution sur
  barres 5 min +0,126 R (t = 0,92). L'exécution plus fine ne change pas le résultat, mais 55 trades ne
  permettent aucune conclusion.
* Durée des drawdowns, espérance en dollars, résultats par séance et par régime de volatilité, effet d'un
  délai d'exécution manuelle et autres combinaisons d'unités de temps : voir § 14 (compléments a posteriori).

## 6. Monte-Carlo FundedNext Flex 50K

Source : `research/output/final/montecarlo.json` (résumé dans `final.md`). Rééchantillonnage de journées
entières des 790 trades walk-forward S1 2014-2021 (2 068 journées), règles Flex 50K (objectif 2 500 $,
plancher trailing de fin de journée 1 500 $ verrouillé à 50 100 $, consistance 40 %, 30 micros maximum,
contrats entiers), or à 4 000 $, horizon 120 jours de trading, 10 000 trajectoires.

| Risque par trade | P(réussite en 120 j) | P(violation) | P(toujours en cours) | Trades moyens | Profit médian | 5e centile du profit |
|---|---|---|---|---|---|---|
| 75 $ | 0,01 % | 0,0 % | 99,99 % | 8 | +72 $ | −284 $ |
| 100 $ | 0,2 % | 0,0 % | 99,8 % | 26 | +213 $ | −627 $ |
| 125 $ | 1,2 % | 0,0 % | 98,8 % | 36 | +285 $ | −885 $ |
| 150 $ | 3,3 % | 0,0 % | 96,7 % | 39 | +284 $ | −996 $ |
| 200 $ | 8,3 % | 0,0 % | 91,6 % | 37 | +191 $ | −1 054 $ |
| 250 $ | **10,7 %** | 0,0 % | 89,3 % | 36 | +146 $ | −1 069 $ |

Contrôles publiés à côté (même fichier) : avec les trades 2022-2025, P(réussite) à 250 $ = **6,7 %** ;
avec un or à 4 500 $ (5 000 trajectoires), 9,8 %.

Lecture honnête :
* dans **environ 9 cas sur 10**, le challenge n'est ni réussi ni perdu au bout de 120 jours : l'avantage
  estimé est trop faible pour atteindre 2 500 $ ;
* P(violation) = 0,0 % à tous les niveaux : le dimensionnement plafonne chaque risque à 20 % du coussin
  restant et l'arrêt journalier interne coupe les mauvaises journées (paramètres de `production.json`).
  Ce chiffre dépend entièrement de l'hypothèse que la distribution historique des trades se reproduit ;
  il ne garantit rien ;
* explication probable du faible nombre de trades à 75 $ : avec un stop à 2,5 ATR, un seul contrat MGC
  dépasse souvent ce budget et le trade est refusé (contrats entiers uniquement).

Compte financé (252 jours, 5 000 trajectoires, 250 $ par trade) : aucune violation simulée, probabilité
d'au moins un retrait 56,3 %, retrait moyen payé 627 $ (médiane 471 $), 5e centile du profit −1 124 $.

## 7. Profil de risque par défaut et pourquoi

Règle fixée à l'avance (`docs/03` § 7) : le risque qui maximise P(réussite) sous la contrainte
P(violation avant réussite) ≤ 20 %. Résultat : **250 $ par trade** (`montecarlo.json` → `profil_retenu`,
« contrainte respectée »). Paramètres par défaut appliqués par le moteur (`production.json` →
`risk_settings_default`) :

| Paramètre | Valeur | Rôle |
|---|---|---|
| Risque par trade | 250 $ | plafond du risque d'un signal (stop + glissement + commission) |
| Fraction maximale du coussin | 0,20 | un trade ne risque jamais plus de 20 % de la distance au plancher |
| Arrêt journalier interne | 500 $ | plus de signal après 500 $ de pertes dans la journée (FundedNext n'a pas de limite journalière en Flex) |
| Trades par jour | 3 | |
| Pertes par jour | 2 | |
| Verrouillage de consistance | 0,8 | plus de signal quand le profit du jour atteint 80 % de 1 000 $ (40 % de l'objectif) |
| Marge de sécurité | 100 $ | le risque + 100 $ ne doit jamais atteindre le plancher |
| Glissement supposé | 0,30 $/once | |
| Commission | 2 $ par contrat aller-retour | **hypothèse** : le tarif MGC de FundedNext n'est pas publié |
| Contrats maximum | 30 micros | limite Flex 50K |

Ces valeurs sont modifiables dans Réglages ; le serveur refuse les valeurs hors bornes
(`backend/goldpilot/risk/sizing.py`, `RiskSettings.validate`). Rappel : avec P(réussite) ≈ 10 % en
120 jours, ce profil n'est **pas** une promesse de réussite ; c'est le moins mauvais compromis mesuré.

## 8. Seuils de suspension automatique

Source : `production.json` → `seuils_suspension` (dérivés de `montecarlo.json` → `suspension`, 100 trades
tirés des trades walk-forward) :
* drawdown ≤ **−27,27 R** (1er centile ; médiane −10,9 R, 5e centile −21,4 R) ;
* série de **17 pertes** consécutives (99e centile ; 95e centile : 13).

Le moteur (`engine/runner.py`, `_performance_guard`) recalcule ces deux mesures sur les signaux clôturés
de la version en cours à chaque clôture ; si un seuil est franchi, il passe en **Arrêt de sécurité**
(incident critique, alerte Telegram), et seule une reprise manuelle sur la page d'accueil le relance.

## 9. Preuve de parité moteur temps réel = backtest

Test `backend/tests/test_e2e_parity.py` : le moteur de production complet (base de données, agrégation
des barres, stratégie, moteur de risque, simulateur d'exécution, cycle de vie des signaux, file des
notifications) rejoue le fichier 5 minutes du 01/06/2025 22:00 UTC au 21/06/2025, puis le résultat est
comparé au backtest de recherche sur la même période. Il vérifie exactement ceci : l'historique journalier
est chargé ; plus de 1 000 barres de 15 minutes sont analysées et journalisées, chaque absence de trade
avec sa raison ; **l'indicateur de décision z**, tel que le moteur l'enregistre (arrondi à 0,01), concorde
avec le z du backtest (écart ≤ 0,011) sur chaque barre de décision à partir du 03/06/2025 (plus de 800
barres contrôlées) — les autres indicateurs (ATR, moyenne de séance, rang de volatilité de la veille) ne
sont **pas** comparés séparément ; à partir du 03/06/2025, les **signaux** du moteur et les trades du
backtest sont en même nombre et identiques un à un (sens, prix d'entrée et de sortie simulés, résultat en
R à 1e-9 près, motif de sortie), sans aucun refus du moteur de risque (paramètres de risque volontairement
permissifs pour ce test) ; une notification est mise en file pour chaque signal. Résultat : **réussi**
dans l'exécution du § 10.

Limite : cette parité porte sur des barres XAUUSD rejouées, pas sur un flux MGC réel venant de
TradingView. Le contrôle croisé TradingView ↔ moteur (`test_mirror.py`, voir `02_architecture.md`) est la protection prévue
en production, non testée sur TradingView.

## 10. Tests techniques exécutés (étape A)

### Exécution du 10/10/2026

| Suite | Commande | Résultat |
|---|---|---|
| Backend (pytest) | `cd goldpilot/backend && python -m pytest -q -p no:cacheprovider` | **187 tests réussis, 0 échec**, 1 avertissement (dépréciation dans la bibliothèque Starlette, sans effet) ; lancé le 10/10/2026 à 23:21 UTC, terminé à 23:24 UTC, durée 201,65 s (Python 3.13.16, pytest 9.1.1) |
| Frontend (Vitest) | `cd goldpilot/frontend && npm test` | **24 tests réussis** (2 fichiers), lancé le 10/10/2026 à 23:23 UTC, 0,77 s |
| Frontend de bout en bout (Playwright) | `npm run test:e2e` | **non exécuté dans le cadre de ce rapport** (suite écrite par une autre étape du projet ; voir son propre compte rendu) |

### Ce que vérifie chaque fichier de tests

Backend (`goldpilot/backend/tests/`) :

| Fichier | Ce qui est vérifié |
|---|---|
| `test_api.py` | connexion par mot de passe, limite d'essais, cookie de session (drapeaux, seul le hachage en base), déconnexion, expiration ; en-tête anti-CSRF `X-GoldPilot` obligatoire pour toute écriture ; en-têtes de sécurité ; le tableau de bord n'est **jamais vert** si un composant est en panne ; validation des réglages de risque et du programme ; **mode réel verrouillé** tant que la stratégie n'est pas validée, et exigeant la confirmation FundedNext + la phrase exacte ; déclaration d'exécution (libellé, P&L) ; annulation seulement avant l'entrée simulée ; filtres, journal, statistiques, calendrier manuel avec fuseau obligatoire ; script Pine servi ; aucun secret exposé |
| `test_causality.py` | absence de fuite du futur : ajouter des barres futures ne change ni les indicateurs passés ni les décisions passées |
| `test_e2e_parity.py` | parité moteur temps réel = backtest (§ 9) |
| `test_execution.py` | chaque règle d'exécution prudente : entrée au marché à l'ouverture suivante + demi-spread, barre d'entrée entièrement postérieure, gap, expiration, stop avant objectif dans la même barre, sortie au gap, sortie temporelle et changement de jour, stop suiveur qui ne recule jamais, symétrie vente, une position à la fois, glissement en marché rapide et commission, coûts proportionnels au prix |
| `test_macro_context.py` | contexte FRED (réponses simulées, aucun accès réseau) : valeur manquante jamais remplacée par 0, erreurs HTTP/réseau/délai sans jamais citer la clé, délai de 10 s, échec partiel, journaux expurgés, **la stratégie et le risque ne lisent jamais ce contexte**, stockage par le moteur, absence de requête sans clé ou en rejeu, format du tableau de bord |
| `test_market_basics.py` | échéances MGC et dates de roll, jours ouvrés, symboles TradingView, journée de trading à 18:00 New York, heures d'été, phases de marché, calendrier (fenêtre de blocage, dates FOMC/BEA intégrées, lecture du fichier iCalendar BLS), contrôle qualité des données (périmées, contrat incorrect, flux en retard, heure incomplète, saut anormal, barres 5 min) |
| `test_mirror.py` | contrôle croisé TradingView ↔ moteur : concordance, désaccord (incident + alerte), résolution, décision absente, signal du moteur non confirmé par TradingView |
| `test_notify.py` | alerte Telegram : présence de **chaque champ exigé** (§ 11 du cahier des charges), bandeau SIMULATION, formulations, troncature, erreurs sans jeton, idempotence, notifications désactivées, réessais avec attente progressive, **une alerte périmée n'est jamais envoyée** |
| `test_risk.py` | règles Flex 50K (plancher fin de journée et verrouillage, perte latente, consistance, compte financé, source et statut de chaque règle) ; dimensionnement (valeur réelle MGC, coussin, plafond de contrats, refus si un contrat est trop risqué, perte du jour) ; **chaque contrôle bloquant** du moteur de risque, dont « Règles incertaines » bloquant en réel sans confirmation écrite |
| `test_webhook.py` | webhook TradingView : jeton, liste d'adresses IP, débit, taille, JSON, horodatages futurs ou non ronds, jeton jamais journalisé, historique journalier, signaux miroir, idempotence (renvoi TradingView), mesure du retard |

Frontend (`goldpilot/frontend/`) :

| Fichier | Ce qui est vérifié |
|---|---|
| `src/lib/format.test.ts` (10 tests) | formats français (virgule, espaces, signe moins, dollars, R, %), valeurs absentes, durées, texte des notifications sans HTML interprété, heures New York / Paris en été et en hiver |
| `src/lib/status.test.ts` (14 tests) | jamais de vert sans `ok=true` (serveur injoignable, données en panne, mode sécurisé, arrêt, pause, notifications), vocabulaire exact des statuts de signaux, distinction position simulée / exécution déclarée, annulation, redirection interne, « connecté » TradingView seulement avec des webhooks récents |
| `e2e/auth.spec.ts` | redirection vers la connexion, mauvais / bon mot de passe, déconnexion, écriture sans en-tête refusée, session expirée |
| `e2e/accueil.spec.ts` | états de la page d'accueil (aucun vert sans signe de vie, serveur injoignable, bandeau rejeu, blocs marché/trading/incidents, bandeau SIMULATION), suspendre/reprendre, notifications on/off, test de notification sans Telegram |
| `e2e/pages.spec.ts` | aucune erreur console, titre et bandeau SIMULATION sur chaque page, navigation mobile/ordinateur, onglets du journal, page Statistiques (verdict NON VALIDÉE, Monte-Carlo, suivi papier, contexte macro) |
| `e2e/reglages.spec.ts` | risque invalide refusé et valeur valide conservée, mode réel refusé, référence obligatoire pour la confirmation FundedNext, programme, TradingView et Telegram |
| `e2e/signaux.spec.ts` | historique filtré par statut, détail avec tous les champs § 11, contrôles du risque, déclaration d'exécution « déclaré par toi — non confirmé par le courtier », annulation |
| `e2e/captures.spec.ts` | production des captures d'écran de `docs/captures/` (données fictives) |

## 11. Paper trading en temps réel (étape D) : non réalisé

Aucun paper trading sur le flux MGC réel n'a eu lieu : il exige l'abonnement TradingView payant, les
données COMEX temps réel et le serveur en ligne (voir `07_cles_abonnements_autorisations.md`). Le mode
« rejeu » de développement (`DATA_SOURCE=replay`) rejoue des barres XAUUSD historiques : il exerce la
chaîne logicielle mais **n'est pas** un paper trading et ne mesure aucun retard réel.

## 12. Ce qui reste à satisfaire avant tout argent réel

Critères prospectifs fixés à l'avance (`docs/03` § 9 et § 10, point 5), mesurés sur les signaux émis en
simulation à partir du **flux MGC réel** :
1. au moins **60 jours de trading** de paper trading ;
2. espérance > 0 avec **borne basse unilatérale à 95 % > 0** sur ces signaux ;
3. **glissement réel ≤ glissement supposé** (0,30 $/once ; l'onglet Statistiques compare les prix prévus
   et ceux que tu déclares) ;
4. résultats **au-dessus du 5e centile** de la distribution Monte-Carlo ;
5. puis, en plus : **confirmation écrite de FundedNext** (règle « signaux externes »), tarif réel de
   commission MGC, et ta décision manuelle explicite dans Réglages.

Note sur la quantité de données (calcul) : au rythme attendu de 8,26 trades par mois (`production.json` →
`trades_par_mois_attendus`), 60 jours de trading (≈ 2,9 mois de 21 jours) donnent **≈ 24 trades**. Pour
que la borne basse unilatérale à 95 % soit positive quand l'espérance observée vaut μ avec un écart-type σ
par trade, il faut n > (1,645 × σ / μ)². Avec les écarts-types des échantillons complets :
* période exploratoire 2022-2025 (`final.json` → `exploratoire_base`, 327 trades) : σ = 1,316 R,
  μ = +0,061 R → n > (1,645 × 1,316 / 0,061)² ≈ **1 262 trades**, soit ≈ 153 mois (≈ 13 ans) ;
* walk-forward 2014-2021 (`final.json` → `walk_forward_S1`, 790 trades) : σ = 1,423 R, μ = +0,081 R →
  n > (1,645 × 1,423 / 0,081)² ≈ **840 trades**, soit ≈ 102 mois (≈ 8,5 ans).

Ce calcul suppose que l'espérance observée tombe exactement sur μ ; pour avoir 80 % de chances d'y
parvenir si μ est la vraie espérance, il faudrait n ≈ ((1,645 + 0,842) × σ / μ)², soit ≈ 2 880 trades
(2022-2025) ou ≈ 1 920 trades (walk-forward). (L'ancienne version de cette note utilisait σ ≈ 1 R, tiré des
seuls 55 trades du contrôle de résolution : chiffre le moins représentatif, qui sous-estimait le besoin
d'environ 1,7 fois.) Le critère n° 2 ne sera donc vraisemblablement pas atteint rapidement :
c'est voulu, la règle protège ton argent. Toute nouvelle stratégie devra suivre un nouveau protocole
pré-enregistré.

## 13. Erreurs et limites observées

* Stratégie non validée ; 2024 négative sur la période exploratoire ; espérance négative en validation
  si les coûts doublent.
* Données de recherche **XAUUSD spot** (pas MGC), volume = ticks, année 2025 trouée.
* Commission MGC inconnue (hypothèse 2 $).
* Le calendrier économique historique n'existe pas : la pause autour des annonces n'est pas dans les
  backtests (elle ne peut que retirer des trades).
* Intégrations réelles **non testées** : réception d'un vrai webhook TradingView, script Pine sur
  TradingView, envoi Telegram réel, Databento, FRED.
* Liste complète : [`08_limites.md`](08_limites.md).

## 14. Compléments a posteriori (ajoutés le 11/10/2026)

> **Complément a posteriori (non pré-enregistré, ne change pas le verdict).** Ces calculs ont été faits
> après coup, en réponse à une revue de conformité au cahier des charges (§ 3.7, § 4 et § 5), après avoir vu
> les résultats ci-dessus. Ils ne servent ni à choisir ni à modifier la stratégie : la configuration de
> production reste `S1|F=True,k=5.0,s=2.5,t=3.0` et le verdict reste **NON VALIDÉE**. Méthode :
> `docs/03` § 11. Script : `research/05_complements.py` (durée d'exécution ≈ 45 s). Chiffres :
> `research/output/complements/complements.json` (tableaux bruts dans `complements.md`). Coûts de base.

### 14.1 Durée des drawdowns et espérance en dollars (cahier des charges § 4)

Montants en dollars au risque par défaut de **250 $ par trade** (`production.json`), en supposant 1 R =
250 $ exactement (arrondi au nombre entier de contrats ignoré ; coûts inclus, car les R sont nets).
Durée d'un drawdown = nombre de **jours de trading** passés sous le précédent sommet de la courbe des
gains (journées sans trade comprises) ; la médiane inclut le drawdown encore ouvert en fin de période.

| Période | Trades | Espérance (R) | Espérance par trade à 250 $ | IC95 en $ | Drawdown max (R / $ à risque constant) | Durée max d'un drawdown | Durée médiane | Drawdowns | En cours à la fin |
|---|---|---|---|---|---|---|---|---|---|
| Walk-forward 2014-2021 | 790 | +0,081 | **+20 $** | [−5 $ ; +46 $] | −19,2 R / −4 801 $ | **424 jours** | 25 jours | 26 | oui, 37 jours (2 068 jours au total) |
| Exploratoire 2022-2025 | 327 | +0,061 | **+15 $** | [−19 $ ; +52 $] | −15,3 R / −3 836 $ | **232 jours** | 13 jours | 14 | oui, 23 jours (997 jours au total) |

Lecture : l'espérance vaut **environ +15 à +20 $ par trade** à 250 $ de risque, mais l'intervalle de
confiance inclut des valeurs négatives. Le plus long drawdown du walk-forward a duré **424 jours de
trading (≈ 1 an et 8 mois)** : même si l'avantage historique était réel, des périodes de plus d'un an sans
nouveau sommet sont normales pour cette stratégie. Le drawdown en dollars est théorique (risque constant de
250 $) : en pratique, le dimensionnement réduit le risque quand le coussin au-dessus du plancher diminue (§ 6-7).

### 14.2 Résultats par séance et par régime de volatilité (cahier des charges § 3.5 et § 4)

Séance = heure d'entrée en New York (Londres : 03:00-08:00 ; New York matin : 08:00-12:00 ; après-midi :
après 12:00 ; S1 ne décide pas en séance asiatique). Régime = tercile, parmi les 250 journées précédentes,
de la moyenne sur 20 journées de l'amplitude relative (H−L)/C **connue la veille** (calcul causal ; à ne
pas confondre avec le filtre F, qui porte sur la seule veille).

| Séance (heure d'entrée, New York) | Walk-forward 2014-2021 : n / espérance R / $ | Exploratoire 2022-2025 : n / espérance R / $ |
|---|---|---|
| Londres | 353 / +0,068 / +17 $ | 129 / −0,025 / −6 $ |
| New York matin | 411 / +0,114 / +29 $ | 181 / +0,137 / +34 $ |
| New York après-midi | 26 / −0,266 / −67 $ | 17 / −0,099 / −25 $ |

| Régime de volatilité | Walk-forward 2014-2021 : n / espérance R / $ | Exploratoire 2022-2025 : n / espérance R / $ |
|---|---|---|
| faible | 427 / +0,166 / +42 $ | 125 / +0,233 / +58 $ |
| moyenne | 232 / −0,014 / −3 $ | 114 / −0,114 / −29 $ |
| forte | 131 / −0,030 / −8 $ | 88 / +0,044 / +11 $ |

Lecture prudente : la matinée de New York est positive sur les deux périodes ; Londres est positive sur
2014-2021 mais négative sur 2022-2025 ; l'après-midi compte trop peu de trades pour conclure. Les
journées de **faible** volatilité portent l'essentiel du résultat sur les deux périodes, les journées de
volatilité moyenne sont négatives sur les deux. Ces découpages ont été faits **après** avoir vu les
résultats, sur des sous-échantillons petits : ils ne justifient **aucun** filtre supplémentaire (ce serait
ajuster la stratégie aux données). Ils pourront servir d'hypothèses à un futur protocole pré-enregistré.

### 14.3 Délai d'exécution manuelle (cahier des charges § 3.7)

Rejeu du contrôle de résolution (13/02/2025 → 28/10/2025, exécution sur barres de 5 minutes) avec une
entrée retardée après la décision (clôture de la barre de 15 min). À 1 et 3 min, le prix exact n'est pas
connu (il tombe au milieu d'une barre de 5 min) : il est encadré par une estimation interpolée et une borne
prudente, le pire prix de cette barre (la même barre pour 1 et 3 min, d'où des lignes identiques).

| Délai après la décision | Prix d'entrée | Trades | Espérance (R) | IC95 (R) | Drawdown max (R) | Écart moyen d'entrée vs clôture de décision ($/once) |
|---|---|---|---|---|---|---|
| 0 min | exact (ouverture 5 min) | 55 | +0,126 | [−0,142 ; +0,393] | −5,4 | 0,04 |
| 1 min | estimé (interpolé) | 55 | +0,107 | [−0,151 ; +0,373] | −5,5 | 0,27 |
| 1 min | borne prudente (pire prix de la barre) | 55 | −0,202 | [−0,453 ; +0,066] | −15,4 | 3,79 |
| 3 min | estimé (interpolé) | 55 | +0,068 | [−0,179 ; +0,334] | −5,7 | 0,74 |
| 3 min | borne prudente (pire prix de la barre) | 55 | −0,202 | [−0,453 ; +0,066] | −15,4 | 3,79 |
| 5 min | exact (ouverture 5 min) | 55 | +0,045 | [−0,195 ; +0,301] | −6,1 | 1,21 |

Lecture : à 55 trades, aucun de ces résultats n'est distinguable de zéro, mais le sens est net. S1 entre
**dans le sens d'un mouvement en cours** : chaque minute perdue se paie. Avec 5 minutes de retard (prix
exact), l'espérance passe de +0,126 à **+0,045 R** (environ deux tiers de l'avantage perdus) et le prix
d'entrée s'écarte en moyenne de **1,21 $/once** de la clôture de décision, contre 0,04 $ sans délai et
0,30 $/once de glissement supposé dans les réglages de risque (`slippage_allowance_oz`). Dans le cas
défavorable (pire prix de la première barre de 5 min), l'espérance devient négative (−0,202 R).
Conséquence pratique : si la stratégie était un jour validée, il faudrait entrer **dans la minute** qui suit
l'alerte ; ce test n'inclut pas la règle « ne pas entrer si le prix s'est écarté de plus de 0,5 ATR », qui
écarterait une partie des entrées tardives. Le délai réel (alerte → saisie sur Tradovate) n'a jamais été
mesuré (aucun paper trading n'a eu lieu, § 11).

### 14.4 Combinaisons d'unités de temps (cahier des charges § 5)

Unités de temps effectivement utilisées et pourquoi : **15 minutes** pour la décision (seule résolution
disponible sur tout l'historique 2004-2025 ; le fichier 5 min ne couvre que 2025) ; **journalier** comme
contexte, par le filtre F (amplitude de la veille), testé oui/non dans la grille pré-enregistrée ;
**5 minutes** pour le seul contrôle d'exécution. Aucune autre combinaison n'avait été testée avant le
choix. Contrôle de robustesse a posteriori sur **2011-2021 uniquement** (aucune donnée 2022-2025 lue),
avec les paramètres de production :

| Combinaison | Entraînement 2011-2018 : n / espérance R | Validation 2019-2021 : n / espérance R / PF | 2011-2021 : espérance R [IC95] |
|---|---|---|---|
| décision 15 min + filtre de volatilité journalière (configuration de production) | 684 / +0,142 | 264 / +0,030 / 1,06 | +0,111 [+0,021 ; +0,205] |
| décision 15 min, sans contexte journalier | 992 / +0,086 | 378 / +0,003 / 1,01 | +0,063 [−0,011 ; +0,137] |
| décision 15 min + filtre journalier + contexte de tendance 1 h (EMA 20) | 657 / +0,105 | 263 / +0,034 / 1,07 | +0,084 [−0,005 ; +0,177] |
| décision 30 min (mêmes paramètres en nombre de barres) + filtre journalier | 360 / +0,179 | 131 / +0,138 / 1,42 | +0,168 [+0,067 ; +0,269] |

Lecture :
* la ligne de référence reproduit exactement la sélection (684 et 264 trades, +0,142 et +0,030 R) ; son
  intervalle sur 2011-2021 est positif, mais c'est la période même où la configuration a été choisie
  (résultat optimiste par construction ; le critère pré-enregistré était le walk-forward, qui a échoué) ;
* retirer le contexte journalier dégrade le résultat ; ajouter un contexte de tendance 1 h ne l'améliore
  pas (+0,084 R contre +0,111 R sur 2011-2021) ;
* la décision sur **30 minutes** donne un meilleur résultat sur 2011-2021 (+0,168 R, validation 2019-2021
  +0,138 R, PF 1,42, mais 2 fois moins de trades). **Ce n'est pas une validation** : variante trouvée après
  coup, l'une des deux variantes nouvelles de ce contrôle (tendance 1 h, 30 min), non comptées dans le
  Deflated Sharpe Ratio, avec des paramètres
  choisis en 15 min, et jamais testée sur 2022-2025. Elle n'est **pas** adoptée (pas de modification
  silencieuse, cahier des charges § 17) ; c'est une piste pour un futur protocole pré-enregistré, à évaluer
  sur des données non vues.

