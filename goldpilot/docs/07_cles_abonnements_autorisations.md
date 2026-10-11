# 07 — Clés API, abonnements et autorisations

Liste complète de ce dont GoldPilot a besoin hors du code : à quoi ça sert, si c'est obligatoire, et
combien ça coûte.

> **Rien n'est à acheter maintenant.** La stratégie n'est pas validée (`04_rapport_de_validation.md`) :
> les seules dépenses qui auraient un sens aujourd'hui sont celles qui permettent la **validation
> prospective en simulation** (étape D du cahier des charges) : serveur, domaine, TradingView payant +
> données COMEX temps réel. C'est toi qui décides ; GoldPilot n'engage aucune dépense.

**Prix indicatifs, vérifiés le 10/10/2026 par recherche web.** Les pages officielles de TradingView,
FundedNext, CME et Databento ne sont pas joignables directement depuis l'environnement de travail (accès
bloqué) : les chiffres viennent d'extraits de ces pages renvoyés par le moteur de recherche, ou de sources
secondaires quand c'est indiqué. Les sources se contredisent parfois (hausses de prix 2026). **Vérifie
toujours le prix sur la page officielle au moment de payer.**

---

## 1. Tableau récapitulatif

| # | Élément | À quoi il sert | Obligatoire ? | Coût indicatif (10/10/2026) |
|---|---|---|---|---|
| 1 | Serveur (VPS Linux) | faire tourner le site et le moteur 24 h/24 | **oui** | ≈ 4,50 à 10 € HT/mois, adresse IPv4 comprise (détail dans `05`, § 1) |
| 2 | Nom de domaine | adresse HTTPS du site et du webhook | **oui** | ≈ 5 à 8 € HT/an pour un `.fr` (4,99 € la 1re année, ≈ 7,79 € au renouvellement) |
| 3 | Abonnement TradingView payant | envoi des webhooks (prix MGC chaque minute) | **oui** | Essential ≈ 12,95 $/mois (annuel) à 14,95 $/mois (mensuel) |
| 4 | Double authentification TradingView | exigée par TradingView pour les webhooks | **oui** | gratuit |
| 5 | Données temps réel CME/COMEX sur TradingView | prix sans retard de 10 min | **oui** | 9,95 $/mois (non professionnel) |
| 6 | Bot Telegram | alertes sur ton téléphone | **oui** (sinon aucune alerte) | gratuit |
| 7 | Secrets du serveur (mot de passe, clés) | sécurité du site et du webhook | **oui** | gratuit (générés sur le serveur) |
| 8 | Confirmation écrite de FundedNext | lever la règle « signaux externes » | **oui avant tout usage réel** | gratuit |
| 9 | Taux de commission MGC FundedNext/Tradovate | remplacer l'hypothèse de 2 $ | **oui avant tout usage réel** | gratuit (information à obtenir) |
| 10 | Challenge FundedNext Flex 50K | le compte d'évaluation | non (tu l'as déjà choisi) | ≈ 134 $ selon des sources tierces, non officiel |
| 11 | Add-on TradingView côté Tradovate/FundedNext | trader depuis les graphiques TradingView | facultatif | ≈ 10 $/mois selon des sources tierces, à vérifier |
| 12 | Clé FRED | contexte macro affiché (information seulement) | facultatif | gratuit |
| 13 | Databento | source de prix principale indépendante (TradingView réduit au contrôle croisé), historique MGC réel | facultatif | live CME : 199 $/mois + frais de licence CME à vérifier ; historique : à l'usage, 125 $ de crédits offerts |
| 14 | Confirmation des licences de données (TradingView, CME) | vérifier que le traitement automatique et le stockage des prix CME reçus par webhook sont permis | **oui avant de dépendre du webhook** | gratuit (question au support) |

---

## 2. Détail

### 1 et 2 — Serveur et nom de domaine
Voir [`05_deploiement_et_exploitation.md`](05_deploiement_et_exploitation.md), § 1 et 2 : minimum 2 Go
de mémoire, adresse **IPv4** (TradingView n'envoie pas vers IPv6), offres Hetzner CX23, OVHcloud VPS‑1,
Scaleway DEV1‑S avec leurs sources.
Nom de domaine `.fr` : création à partir de 4,99 € HT la première année chez OVHcloud selon
[lafabriquedunet](https://www.lafabriquedunet.fr/logiciels/tendances/quel-est-le-prix-dun-nom-de-domaine)
(juillet 2026) ; renouvellement plus cher (≈ 7,79 € HT selon une source non officielle). Page officielle :
<https://www.ovhcloud.com/fr/domains/>. Sources secondaires, à vérifier.

### 3 — Abonnement TradingView payant (obligatoire)
* Le plan gratuit n'envoie pas de webhooks : « Feature available to paid users only »
  ([annonce TradingView](https://www.tradingview.com/blog/en/webhooks-for-alerts-now-available-14054/)).
  Les sources tierces divergent sur le plan minimum (Essential selon certaines, Plus selon d'autres) :
  le site et `docs/01` indiquent Essential ; **vérifie sur la page des plans que « Webhook » est inclus
  avant de payer**.
* Prix relevés sur la [page des tarifs](https://www.tradingview.com/pricing/) (copie de la page
  vieille d'environ 5 mois selon le moteur de recherche) : Essential 12,95 $, Plus 29,95 $, Premium
  59,95 $ par mois en facturation annuelle ; 14,95 $, 34,95 $, 69,95 $ en facturation mensuelle selon les
  données de la même page et une [source tierce de septembre 2026](https://chartinglens.com/blog/tradingview-price-increase-2026).
* **Expiration des alertes** : 2 mois maximum, sauf Premium et Ultimate qui permettent une alerte sans
  fin ([aide TradingView](https://www.tradingview.com/support/solutions/43000688759-i-upgraded-to-the-premium-plan-but-my-alerts-still-expiring-in-2-months/)).
  Avec Essential, il faudra **recréer l'alerte GoldPilot au moins tous les 2 mois** (de toute façon
  nécessaire à chaque roll du contrat, environ tous les 2 mois).
* Exigences techniques des webhooks : ports 80/443 uniquement, réponse en 3 secondes, IPv4, adresses
  d'envoi publiées ([webhooks](https://www.tradingview.com/support/solutions/43000529348-how-to-configure-webhook-alerts/),
  [port](https://www.tradingview.com/support/solutions/43000529314-i-cannot-send-webhook-to-a-url-with-a-port-number/)) —
  GoldPilot les respecte (Caddy en HTTPS sur 443, réponse en quelques millisecondes).

### 4 — Double authentification TradingView (obligatoire, gratuit)
« Webhook alerts are only allowed when 2-factor authentication is enabled »
([configurer la 2FA](https://www.tradingview.com/support/solutions/43000572460-how-to-configure-2fa/)).

### 5 — Données temps réel CME/COMEX sur TradingView (obligatoire)
* Sans abonnement, les données CME Group sont **différées de 10 minutes** ; le forfait CME, CBOT, COMEX,
  NYMEX temps réel est annoncé à **9,95 $/mois** pour les non-professionnels
  ([page CME de TradingView](https://www.tradingview.com/cme/)). Les plans TradingView ne couvrent pas ces
  frais de bourse ([acheter des données](https://www.tradingview.com/support/solutions/43000471705-how-to-purchase-additional-market-data/)).
  Des sources tierces citent d'autres montants (≈ 7 $, ou un total plan + CME de 22,90 €/mois vu depuis
  l'Europe) : vérifie le prix affiché dans ton compte (avatar › Paramètres et facturation › Abonnements ›
  Données de marché en temps réel).
* Si ton compte Tradovate donne déjà droit aux données CME, TradingView indique qu'il n'est pas
  nécessaire de les payer deux fois
  ([données via le courtier](https://www.tradingview.com/support/solutions/43000479666-how-can-i-get-real-time-data-from-exchanges-that-i-have-already-purchased-with-my-broker/)) ;
  **à vérifier** : on ne sait pas si un compte d'évaluation FundedNext ouvre ce droit, ni si ces données
  alimentent les alertes webhook.
* Sans données temps réel, GoldPilot détecte le retard (« données en retard … forfait temps réel COMEX
  absent ? ») et passe en mode sécurisé : aucun signal.

### 6 — Bot Telegram (gratuit)
Créé avec @BotFather ([API Telegram Bot](https://core.telegram.org/bots/api), gratuite). Deux valeurs
sur le serveur : `TELEGRAM_BOT_TOKEN` (secret) et `TELEGRAM_CHAT_ID` (trouvé avec le bouton « Détecter mon
identifiant » de Réglages). Procédure : `06_guide_utilisateur.md`, étape 2.

### 7 — Secrets du serveur (gratuits)
Générés sur le serveur par `deploy/scripts/init-secrets.sh` (voir `05`, § 5), jamais dans Git :
`SECRET_KEY`, `TV_WEBHOOK_TOKEN` (à recopier dans le script Pine), `POSTGRES_PASSWORD`, et
`ADMIN_PASSWORD_HASH` (ton mot de passe du site, au moins 12 caractères, stocké haché). Liste complète
commentée : `deploy/.env.example`.

### 8 — Confirmation écrite de FundedNext (obligatoire avant tout usage réel)
Les règles FundedNext Futures interdisent de « s'abonner à un service de signaux ou d'utiliser des signaux
externes » ([stratégies interdites](https://helpfutures.fundednext.com/en/articles/14298337-what-are-the-prohibited-trading-strategies-of-fundednext-futures)),
tout en autorisant les bots et outils automatisés
([EA et bots](https://helpfutures.fundednext.com/en/articles/14298560-is-the-usage-of-automated-trading-systems-eas-and-bots-allowed-in-fundednext-futures)).
GoldPilot est un outil personnel construit pour toi seul, mais la règle est rédigée largement. Le code
la marque **« contradictoire »** (`backend/goldpilot/risk/rules.py`, règle « Signaux externes ») et le moteur
de risque la rend **bloquante en mode réel** tant que tu n'as pas déclaré une confirmation écrite
(`backend/goldpilot/risk/engine.py`, contrôle « Règles incertaines ») ; voir aussi `docs/01`, § 3.
À faire : écrire au support FundedNext, décrire l'outil (alertes générées par ton propre logiciel, exécution
manuelle par toi seul, non partagé, non vendu), obtenir une réponse **écrite**, puis saisir sa référence
dans Réglages › Mode de trading.

### 9 — Commission MGC (information à obtenir)
FundedNext facture un taux « tout compris » par contrat à l'entrée et à la sortie, mais le taux MGC n'est
pas publié ([commissions](https://helpfutures.fundednext.com/en/articles/17230203-how-do-commissions-work-in-futures-trading)).
GoldPilot suppose **2 $ par contrat aller-retour** (`production.json`). Relève le vrai taux dans ton
espace FundedNext ou Tradovate et reporte-le dans Réglages › Risque ; s'il est nettement plus élevé, les
résultats de recherche (déjà non concluants) sont encore moins bons.

### 10 — Challenge FundedNext Flex 50K
Prix non trouvé sur une page officielle. Sources tierces : ≈ 134 $ hors code promo
([tradecopia](https://tradecopia.com/propfirms/fundednext-futures), [fundedtrading](https://fundedtrading.com/propfirm/fundednext-futures/)),
69,99 $ en offre de lancement (probablement expirée). Aucun frais d'activation selon ces sources. **Non
vérifié** : seul le prix affiché au paiement fait foi. À ne pas racheter pour GoldPilot tant que la
stratégie n'est pas validée.

### 11 — Tradovate et add-on TradingView (facultatif)
FundedNext fournit le compte Tradovate. Pour passer des ordres depuis les graphiques TradingView, un
**add-on TradingView** doit être activé dans Tradovate (section Add-Ons), selon l'aide FundedNext citée
par la recherche et un guide tiers ([guide](https://blog.pickmytrade.trade/fundednext-futures-tradovate-connection-guide/)) ;
prix ≈ 10 $/mois selon des témoignages ([forum Tradovate](https://community.tradovate.com/t/tradovate-to-tradingview-market-data-question/2215)),
**non vérifié**. Ce n'est pas nécessaire pour GoldPilot : tu peux exécuter directement dans Tradovate.
GoldPilot ne se connecte pas à Tradovate : l'API Tradovate demanderait une licence de données CME
(estimée 290-500 $/mois par des utilisateurs, `docs/01`, § 7) — déconseillé.

### 12 — Clé FRED (facultative, gratuite)
Clé gratuite liée à un compte sur <https://fredaccount.stlouisfed.org> ([conditions](https://fred.stlouisfed.org/docs/api/terms_of_use.html)).
À placer dans `FRED_API_KEY`. Sert uniquement à afficher taux réels, taux nominaux et dollar sur la page
Statistiques ; **n'influence jamais** un signal. Premier appel réel non testé.

### 13 — Databento (facultatif)
* **Flux temps réel** (`DATA_SOURCE=databento`) : Databento devient la **source principale** des prix
  (décisions du moteur et suivi des signaux). Les barres TradingView, si l'alerte reste active, ne pilotent
  plus rien : elles servent uniquement au **contrôle croisé** (clôture comparée minute par minute ; écart
  supérieur à **1,00 $** → incident « Sources de prix en désaccord » et alerte Telegram ; seuil de prudence
  de 10 ticks, **hypothèse non validée**, `engine/runner.py`, `CROSS_CHECK_TOL`). Il n'y a **aucune bascule
  automatique** : si Databento tombe, le moteur passe en mode sécurisé, il ne repasse pas sur TradingView
  (`08_limites.md`, n° 20). La dépendance unique change donc de fournisseur, elle ne disparaît pas.
* Le paiement à l'usage n'existe plus pour le temps réel CME ; formule Standard CME **199 $/mois** depuis le
  22/06/2026 ([annonce Databento](https://databento.com/blog/updates-to-subscription-pricing),
  [plans CME](https://databento.com/blog/introducing-new-cme-pricing-plans)). Les frais de licence CME
  pour un utilisateur non professionnel : **à vérifier** avec Databento avant souscription (montants
  contradictoires selon les sources, voir `docs/01` § 9 « Licences des données »).
* **Historique MGC** (pour valider la stratégie sur le vrai contrat au lieu du XAUUSD) : à l'usage, avec
  **125 $ de crédits offerts** à l'inscription ([tarifs](https://databento.com/pricing)).
* Le connecteur GoldPilot pour Databento n'a **jamais été testé** contre le service réel.

### 14 — Licences des données (à faire confirmer)
Selon un extrait des [conditions d'utilisation TradingView](https://www.tradingview.com/policies/), les
données, **alertes et webhooks compris**, sont accordées pour un usage d'affichage personnel ; l'usage
« hors affichage » (traitement automatique) est interdit. GoldPilot calcule des signaux automatiquement à
partir des barres reçues et les stocke : **demande au support TradingView une confirmation écrite** que cet
usage personnel est permis, et fais préciser ton statut CME (non professionnel, affichage ou hors
affichage). Analyse complète : `docs/01` § 9 ; limite n° 27 de `08_limites.md`.

---

## 3. Ordre conseillé (quand tu décideras d'avancer)

1. Écrire à FundedNext pour la **confirmation écrite** et le **taux de commission MGC** (gratuit, peut
   prendre du temps : à lancer en premier).
   Écrire aussi au support TradingView pour la **licence des données** (élément 14).
2. Louer le **serveur** et le **nom de domaine**, puis déployer (`05`).
3. Créer le **bot Telegram** et tester une notification.
4. Passer TradingView en **plan payant avec webhooks**, activer la **2FA**, souscrire les **données
   COMEX temps réel**.
5. Installer le **script Pine** et l'**alerte** ; vérifier Journal › Webhooks (`06`).
6. Facultatif : clé **FRED** ; compte **Databento** (crédits offerts) pour l'historique MGC.
7. Laisser tourner en **simulation** au moins 60 jours de trading et suivre les critères du rapport de
   validation (§ 12). Le mode réel reste une décision distincte.
