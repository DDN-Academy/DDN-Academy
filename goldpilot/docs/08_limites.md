# 08 — Limites qui empêchent encore une utilisation réelle

Liste explicite (cahier des charges § 19). Chaque point indique où il est vérifiable et ce qui le lèverait.
État au 11/10/2026.

## A. Bloquants pour l'argent réel

1. **Stratégie non validée.** Aucune famille n'a satisfait les critères pré-enregistrés ; l'évaluation
   2022-2025 du candidat S1 donne +0,061 R par trade avec un IC95 [−0,076 ; +0,207] : non distinguable de
   zéro (`research/output/selection/selection.md`, `research/output/final/final.md`). Le mode réel est
   verrouillé par le serveur (`api/app.py`, `put_trading_mode`). *Levée* : validation prospective
   (`04_rapport_de_validation.md`, § 12), puis éventuellement un nouveau protocole pré-enregistré.
2. **Aucun paper trading sur le flux MGC réel n'a eu lieu** (étape D du cahier des charges) : il exige
   les abonnements du point 3.
3. **TradingView gratuit incompatible.** Ton plan actuel (gratuit, `docs/01` § 2) n'envoie pas de webhooks
   et reçoit les prix COMEX avec 10 minutes de retard. Il faut un plan payant avec webhooks, la double
   authentification et les données COMEX temps réel (`07_cles_abonnements_autorisations.md`).
4. **Confirmation écrite de FundedNext absente.** La règle « signaux externes » est contradictoire avec
   l'usage d'un outil personnel (`docs/01` § 3 ; `backend/goldpilot/risk/rules.py`, statut
   « contradictoire ») ; le contrôle « Règles incertaines » (`risk/engine.py`) bloque tout signal réel
   tant qu'elle n'est pas déclarée.
5. **Commission MGC inconnue.** Hypothèse de 2 $ par contrat aller-retour (`production.json`,
   `risk/rules.py` règle « Commission MGC », statut « inconnue »). Avec des coûts doublés, l'espérance de
   validation devient négative (−0,017 R).

## B. Ce que le système ne peut pas savoir

6. **Aucune connexion au courtier.** GoldPilot ne se connecte ni à Tradovate ni à FundedNext : il ne peut
   **pas confirmer qu'un ordre a été rempli**, ni connaître ta position réelle, ton prix réel ou ton solde.
   Les positions affichées sont **simulées** ; tes exécutions sont « déclarées par toi — non confirmées
   par le courtier ». Le solde réel n'est connu que si tu le déclares (Réglages › Compte réel FundedNext) ;
   sinon le moteur applique une hypothèse prudente (coussin de 300 $, `engine/runner.py`,
   `_account_for_risk`).
7. **Pas de take-profit fixe.** La stratégie S1 sort par **stop suiveur** (3 ATR derrière le meilleur prix
   atteint, mis à jour toutes les 15 min) ou par **sortie temporelle** (au plus tard 15:30 New York).
   C'est la règle qui a été testée ; un objectif fixe n'a jamais été testé et l'inventer présenterait comme
   fiable une sortie qui ne l'est pas. L'alerte l'indique en toutes lettres (« Take-profit : aucun objectif
   fixe — sortie par stop suiveur… », `notify/messages.py`) et donne le rapport gain moyen / perte moyenne
   historique (≈ 1,98). Conséquence pratique : tu dois **déplacer ton stop toi-même** à chaque alerte
   « Déplacer le stop », ce qui demande d'être disponible pendant la position.

## C. Données et recherche

8. **Le rejeu et toute la recherche utilisent du XAUUSD spot**, pas le contrat MGC (`data/*.csv`) : prix
   différents (base de portage), volume = ticks du courtier, année 2025 trouée
   (`research/output/audit/audit.md`). L'écart XAUUSD ↔ MGC (base, corrélation intraday, horaires,
   liquidité, spread) **n'a jamais été mesuré** : comparaison qualitative des trois instruments dans
   `docs/01` § 4 bis. *Levée possible* : historique MGC Databento (crédits offerts).
9. **Pause autour des annonces non testée historiquement** : aucun calendrier économique historique
   (`docs/03` § 8).
10. **Calendrier BEA et dates de secours intégrés jusqu'à fin 2026** (`calendar/events.py` : FOMC jusqu'à
    décembre 2027, BLS et BEA jusqu'à décembre 2026). Le calendrier BLS est synchronisé depuis le fichier
    iCalendar officiel en production (non testé : accès bloqué en développement) ; les dates BEA doivent
    être complétées chaque trimestre (ajout manuel possible dans Réglages › Calendrier économique).
11. **Peu de trades** : ~8,3 par mois attendus (`production.json`). Des mois de suivi seront nécessaires
    avant toute conclusion statistique ; la revue hebdomadaire du samedi conclut « échantillon trop petit »
    tant qu'il y a moins de 30 trades simulés (`engine/runner.py`, `_periodic_review`).

## D. Intégrations non testées en conditions réelles

12. **Script Pine non testé sur TradingView** (`pine/goldpilot_bridge.pine`, en-tête) : compilation,
    envoi des alertes, historique journalier et signaux miroir n'ont jamais été observés sur TradingView.
    Seule la réception visible dans Journal › Webhooks fera foi.
13. **Réception d'un vrai webhook TradingView** non testée (simulée dans `tests/test_webhook.py` et lors du
    test de déploiement, `05`).
14. **Envoi Telegram réel** non testé (simulé dans `tests/test_notify.py`).
15. **Databento** : connecteur écrit d'après le client officiel, **jamais testé** contre le service réel
    (`marketdata/databento_feed.py`) ; abonnement payant requis.
16. **FRED** : jamais appelé réellement (accès bloqué depuis l'environnement de développement) et
    nécessite une clé gratuite (`context/fred.py`). Information de contexte uniquement.
17. **Certificat HTTPS Let's Encrypt réel, surveillance externe** : non testés (`05`, introduction).
18. **Les prix (TradingView, VPS, FundedNext, Databento) viennent de recherches web**, souvent de sources
    secondaires ; à reconfirmer (`07`).

## E. Fonctionnement et exploitation

19. **Un seul utilisateur** : un seul mot de passe, pas de comptes multiples (`api/security.py`).
20. **Une seule source de prix pilote le moteur, sans bascule automatique.** Par défaut c'est TradingView :
    si TradingView ou ton alerte tombe, le moteur passe en mode sécurisé et n'émet plus de signal. Avec
    `DATA_SOURCE=databento`, Databento devient la source principale et TradingView ne sert plus qu'au
    contrôle croisé des prix (écart de clôture > 1,00 $ sur la même minute → incident ; seuil de prudence
    **non validé**, `CROSS_CHECK_TOL`) ; si Databento tombe, mode sécurisé, sans repli sur TradingView. Le
    connecteur Databento n'a jamais été testé contre le service réel (n° 15).
21. **Alertes TradingView à recréer** : à chaque roll du contrat (environ tous les 2 mois, rappel Telegram
    3 jours ouvrés avant) et, hors Premium/Ultimate, avant leur expiration de 2 mois (aide TradingView,
    voir `07` § 3). Le site ne peut pas le faire à ta place.
22. **Une seule position à la fois, MGC uniquement**, entrées uniquement au marché ; aucune sortie
    partielle ni break-even (non validés).
23. **Pas d'exécution automatique** : volontaire (cahier des charges § 12) ; aucune intégration
    officielle d'ordre n'est implémentée.
24. **Seuils de suspension calculés sur les trades historiques** (−27,27 R ou 17 pertes consécutives) :
    ils protègent contre une dégradation extrême, pas contre une stratégie simplement sans avantage. Après
    une reprise manuelle, ils sont recomptés **à partir de la reprise** : une dégradation lente peut donc
    redémarrer de zéro à chaque reprise.
25. **Règles FundedNext vérifiées le 09/10/2026** par recherche web (sites officiels inaccessibles
    directement) : à reconfirmer dans ton espace FundedNext ; elles peuvent changer.
26. **Limiteurs de débit en mémoire** (connexion, webhook) : remis à zéro à chaque redémarrage du site.
27. **Licences des données non confirmées** (`docs/01` § 9). Selon un extrait de ses conditions, TradingView
    accorde ses données, alertes et webhooks compris, pour un usage d'**affichage** et interdit l'usage
    « hors affichage » (traitement automatique) ; le CME facture séparément l'usage hors affichage. Le
    calcul automatique de signaux à partir des barres envoyées par webhook et leur stockage en base
    pourraient donc ne **pas** être autorisés. *Levée* : confirmation écrite de TradingView (et, avec
    Databento, de Databento/CME). L'origine et la licence des fichiers `data/*.csv` sont inconnues :
    recherche personnelle uniquement, ne pas les publier.
28. **Banques centrales et géopolitique non couvertes** (`docs/01` § 10) : seuls les décisions et conférences
    du FOMC et les statistiques BLS/BEA bloquent les entrées. Discours, minutes du FOMC, autres banques
    centrales et événements géopolitiques ne sont pas surveillés (ajout manuel possible dans Réglages ›
    Calendrier économique).
29. **Jours fériés et clôtures anticipées du CME calculés par règle** (`timeutil.py`) d'après des sources
    consultées le 11/10/2026 (page officielle non joignable) : dates 2026-2027 **à vérifier** chaque année sur
    <https://www.cmegroup.com/trading-hours.html>.
30. **Sortie temporelle sans données** : si les prix n'arrivent plus à l'heure limite, la position simulée
    est clôturée « sortie temporelle (sans données) » sans prix ni résultat (aucun P&L inventé) ; ces trades
    manquent dans les statistiques en R, qui peuvent donc être incomplètes.
31. **Très sensible au délai d'exécution manuelle** : avec 5 minutes de retard, l'espérance du contrôle
    de résolution passe de +0,126 à +0,045 R et l'entrée s'écarte en moyenne de 1,21 $/once du prix de
    décision, contre 0,30 $/once de glissement supposé (`docs/04` § 14.3). Il faudrait entrer dans la
    minute ; ton délai réel n'a jamais été mesuré.
