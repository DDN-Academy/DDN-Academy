# 01 — Environnement, sources officielles, données et accès nécessaires

Date de vérification de toutes les sources : **9 octobre 2026**.

Méthode : les sites FundedNext, TradingView, CME, Databento, Telegram, BLS et Réserve fédérale sont
**bloqués par la politique réseau de l'environnement de développement** (seuls PyPI, npm, GitHub et
Docker Hub sont joignables). Les pages officielles ont donc été consultées par l'outil de recherche
web, qui renvoie des extraits de ces pages. Chaque règle reste à reconfirmer dans ton tableau de bord
FundedNext. Les règles qui se contredisent d'une page officielle à l'autre sont signalées.

## 1. Environnement de développement constaté

| Élément | Constat |
|---|---|
| Outils | Python 3.13, Node 22, Docker 29 (images Docker Hub téléchargeables), PostgreSQL 16 local |
| Réseau | PyPI, npm, GitHub, Docker Hub : OK. FundedNext, TradingView, CME, Telegram, fournisseurs de données : bloqués |
| Données du dépôt | `data/xau_15m_2004_2025.csv` (XAUUSD 15 min, 480 717 barres), `data/xauusd_5m_2025.csv` (XAUUSD 5 min, 50 000 barres) |
| Travaux existants liés à l'or | `backtest_gold.py`, `strategie-gold.html`, `prompt_risk_management.md` |
| Publication | `.github/workflows/deploy.yml` publie **tout le dépôt** sur GitHub Pages à chaque push sur `main` : rien de secret ne doit jamais être commité |

Conséquence : aucune connexion temps réel (TradingView, Telegram, flux de prix) ne peut être testée
depuis cet environnement. Ces intégrations sont testées contre des serveurs simulés locaux et
signalées comme « non vérifiées en conditions réelles » tant que tu ne les as pas activées.

## 2. Ta configuration (réponses du 9 octobre 2026)

| Question | Réponse | Conséquence |
|---|---|---|
| Programme | **FundedNext Futures Flex 50K** | Instrument : **MGC** (Micro Gold COMEX) |
| Plateforme d'exécution | **TradingView et Tradovate** | Exécution manuelle depuis TradingView connecté à Tradovate |
| Source de données | **TradingView seul** (ton abonnement) | Flux de prix envoyé par un script Pine via webhook |
| Abonnement TradingView | **Gratuit** | **Incompatible avec le choix précédent** : voir section 6 |

## 3. FundedNext Futures — Flex 50K

| Règle | Valeur | Statut | Source |
|---|---|---|---|
| Objectif de profit (challenge) | 2 500 $ | confirmée | [Flex rules](https://helpfutures.fundednext.com/en/articles/17229829-fundednext-futures-flex-challenge-all-rules), [page Flex](https://fundednext.com/futures/flex) |
| Perte maximale (MLL) | 1 500 $, trailing sur le plus haut solde de **fin de journée** | confirmée | idem |
| Verrouillage du plancher | le plancher cesse de monter à **50 100 $** | confirmée pour Flex | idem |
| Mise à jour du plancher | une fois par jour (fin de journée), pas en temps réel | confirmée | [objectifs futures](https://fundednext.com/general-rules/futures/trading-objectives) |
| Perte latente | une perte flottante qui atteint le plancher viole le compte **immédiatement** | confirmée | idem |
| Limite de perte journalière | **aucune** | confirmée | [Flex rules](https://helpfutures.fundednext.com/en/articles/17229829-fundednext-futures-flex-challenge-all-rules) |
| Consistance | challenge seulement : aucun jour > 40 % de l'objectif (1 000 $) ; sinon l'objectif devient meilleur jour ÷ 0,40 (pas une violation) | confirmée | idem |
| Contrats | 3 mini **ou 30 micros** (ratio 1:10), fixé à la création | confirmée | idem |
| Durée | pas de limite | confirmée | idem |
| Horaires | positions fermées **au plus tard à 15:10 CT** (16:10 New York), sinon fermeture automatique ; reprise 17:00 CT ; pas d'overnight ni de week-end | confirmée | [overnight](https://helpfutures.fundednext.com/en/articles/14268506-does-fundednext-futures-allow-overnight-and-weekend-trade-holding), [plateformes](https://fundednext.com/general-rules/futures/trading-platforms) |
| Annonces économiques | trading autorisé sur tous les modèles futures (NFP, CPI, FOMC inclus) | confirmée | [règles générales futures](https://fundednext.com/general-rules/futures/what-is-allowed) |
| Bots / IA | autorisés (pas d'abus de latence, pas d'HFT, pas de tick scalping) | confirmée | [EA futures](https://helpfutures.fundednext.com/en/articles/14298560-is-the-usage-of-automated-trading-systems-eas-and-bots-allowed-in-fundednext-futures) |
| **Signaux externes** | **interdit** de s'abonner à un service de signaux ou d'utiliser des signaux externes ; interdit de copier une autre personne | confirmée | [stratégies interdites](https://helpfutures.fundednext.com/en/articles/14298337-what-are-the-prohibited-trading-strategies-of-fundednext-futures) |
| Autres interdits | spoofing, layering, grille, wash trading, arbitrage de latence, couverture corrélée, trading en marché gappé/illiquide, à moins de 2 % des limites de prix CME, micro-scalping (< 10 s) | confirmée | idem |
| Commissions | taux « tout compris » par contrat, facturé à l'entrée et à la sortie ; **taux MGC non publié** | inconnue | [commissions](https://helpfutures.fundednext.com/en/articles/17230203-how-do-commissions-work-in-futures-trading) |
| Compte financé Flex | pas de consistance ; 5 « benchmark days » ≥ 200 $ + ≥ 500 $ de profit dans le cycle ; retrait 250 $ à 1 500 $ par cycle ; part 95 % ; le premier retrait ramène le plancher à 50 100 $ | confirmée | [Flex funded](https://helpfutures.fundednext.com/en/articles/17229848-fundednext-futures-flex-fundednext-account-all-rules) |
| Rapid / Bolt | plus vendus depuis le 10/07/2026 ; comptes actifs fermés à la transition | confirmée | [réinitialisations](https://helpfutures.fundednext.com/en/articles/14260538-what-are-the-reset-conditions-and-fees-at-fundednext-futures) |

**Point de conformité à faire confirmer par écrit au support FundedNext** : ce système est un outil
personnel que tu as fait construire pour toi seul (non vendu, non partagé). Il ne s'agit ni d'un
service de signaux tiers ni de copie d'une autre personne, mais la règle « external signals » est
rédigée largement. **Demande une confirmation écrite avant d'utiliser le système sur le compte.**

## 4. Contrats COMEX

| | MGC (Micro Gold) | GC (Gold) |
|---|---|---|
| Taille | 10 onces | 100 onces |
| Tick | 0,10 $ = **1 $ par contrat** | 0,10 $ = 10 $ par contrat |
| Horaires CME | dimanche 17:00 → vendredi 16:00 CT, pause quotidienne 16:00-17:00 CT | idem |
| Mois cotés | février, avril, juin, août, octobre, décembre | idem |
| Mois actifs (liquidité) | février, avril, juin, août, décembre (octobre ajouté comme mois « lead » en 2026) | idem |
| Fin de négociation | 3e dernier jour ouvré du mois de livraison | idem |
| Règlement | physique (ACE) ; les comptes FundedNext sont intraday uniquement | physique |

Sources : [spécifications MGC](https://www.cmegroup.com/markets/metals/precious/e-micro-gold.contractSpecs.html),
[fiche or CME](https://www.cmegroup.com/trading/metals/files/fact-card-gold-futures-options.pdf),
[règlement chapitre 113](https://www.cmegroup.com/rulebook/COMEX/1a/113.pdf).

Pourquoi MGC et pas GC : avec une perte maximale de 1 500 $, un stop de 10 $ coûte 1 000 $ par contrat
GC (inacceptable) mais 100 $ par contrat MGC, ce qui permet un dimensionnement fin.
Pourquoi pas XAUUSD : ton programme est futures ; XAUUSD (spot/CFD) ne sert ici qu'aux données historiques.

## 5. TradingView — possibilités réelles

| Capacité | Réalité vérifiée | Source |
|---|---|---|
| API pour lire ton compte, tes graphiques, tes indicateurs | **n'existe pas** (API REST réservée aux brokers) | [support API](https://www.tradingview.com/support/solutions/43000474413-i-need-access-to-your-api-in-order-to-get-data-or-indicator-values/) |
| Serveur MCP officiel | bêta, Essential minimum, données **différées**, ne crée pas de webhooks, pas de lecture des indicateurs | [MCP docs](https://www.tradingview.com/mcp/docs) |
| Webhooks d'alertes | POST HTTP ; **2FA obligatoire** ; plan payant ; ports 80/443 seulement ; délai max 3 s ; renvoi jusqu'à 3 fois sur erreur 5xx ; pas d'IPv6 | [webhooks](https://www.tradingview.com/support/solutions/43000529348-how-to-configure-webhook-alerts/), [renvoi](https://www.tradingview.com/support/solutions/43000735201-webhook-resubmission/) |
| IP d'envoi | 52.89.214.238, 34.212.75.30, 54.218.53.128, 52.32.178.7 | idem |
| Authentification | certificat client TLS (CN = webhook-server@tradingview.com) ; pas de mot de passe dans le message | [authentification](https://www.tradingview.com/support/solutions/43000680459-webhook-authentication/) |
| Données CME/COMEX | **différées de 10 min** sans forfait ; temps réel CME/CBOT/COMEX/NYMEX : **9,95 $/mois** (non-pro) | [CME sur TradingView](https://www.tradingview.com/cme/) |
| Pine Script v6 | `alert()` avec `alert.freq_once_per_bar_close` ; `request.security(..., expr[1], lookahead_on)` pour éviter le repaint | [alertes Pine](https://www.tradingview.com/pine-script-docs/concepts/alerts/), [repainting](https://www.tradingview.com/pine-script-docs/concepts/repainting/) |
| Connexion Tradovate/FundedNext dans TradingView | supportée par FundedNext ; selon des guides tiers, un add-on TradingView côté FundedNext/Tradovate peut être requis | [plateformes FundedNext](https://helpfutures.fundednext.com/en/articles/17225732-what-trading-platforms-does-fundednext-futures-offer) |

Architecture retenue : un script Pine v6 installé sur le graphique du contrat MGC actif envoie, à la
clôture de chaque barre d'une minute, un message JSON signé d'un jeton secret au serveur. Le serveur
valide, stocke et contrôle ces barres, puis prend **seul** ses décisions. Le script Pine affiche aussi
les niveaux du système pour vérification visuelle. On ne te demande jamais ton mot de passe TradingView.

## 6. Incompatibilité à lever (seule action bloquante pour le temps réel)

Avec un compte TradingView **gratuit** : pas de webhooks, et données COMEX différées de 10 minutes.
Pour que « TradingView seul » fonctionne réellement, il faut :
1. un abonnement **Essential** ou supérieur (prix sur https://www.tradingview.com/pricing/) ;
2. la **double authentification** activée ;
3. le forfait temps réel **CME/COMEX (9,95 $/mois non-pro)**, sinon les prix reçus auraient 10 minutes
   de retard et le système refuserait d'émettre des signaux.

Limite assumée : avec TradingView comme unique source, une panne de TradingView coupe les données.
Le système le détecte (données périmées) et passe en mode sécurisé (aucun signal). Pour supprimer ce
point de défaillance unique, un flux indépendant est prêt à brancher (voir section 7).

## 7. Données, API et services : besoins, coûts, alternatives

| Besoin | Solution retenue | Coût | Alternative | Statut |
|---|---|---|---|---|
| Prix MGC temps réel | Script Pine → webhook (ton choix) | Essential + 9,95 $/mois | Databento Standard CME **199 $/mois** (flux officiel indépendant, [annonce prix](https://databento.com/blog/updates-to-subscription-pricing)) ; API Tradovate : licence CME estimée 290-500 $/mois par des utilisateurs ([forum](https://community.tradovate.com/t/is-cme-sub-vendor-requirement-for-api-access-is-290-per-month/6215)) — déconseillé | à activer par toi |
| Historique MGC (validation sur le vrai contrat) | Databento historique à l'usage | dès 0,50 $/Go ; **125 $ de crédits offerts** à l'inscription ([crédits](https://docs.databento.com/knowledge-base/new-users/usage-based-pricing-and-data-credits)) | — | optionnel, recommandé |
| Historique pour la recherche | fichiers XAUUSD du dépôt | 0 $ | — | disponible |
| Calendrier économique | BLS (fichier iCalendar officiel), BEA (calendrier officiel), FOMC (Réserve fédérale) | 0 $ | fournisseurs payants | intégré |
| Taux, dollar (contexte) | FRED (DGS10, DFII10, DTWEXBGS), clé gratuite, usage personnel | 0 $ | — | clé à créer |
| Notifications téléphone | Bot Telegram | 0 $ | Web Push (iPhone : uniquement si le site est ajouté à l'écran d'accueil, iOS ≥ 16.4) | bot à créer |
| Hébergement 24 h/24 | VPS Linux avec Docker | quelques €/mois | PaaS | à louer par toi |

Sources calendrier : [BLS iCalendar](https://www.bls.gov/help/hlpical.htm) (`https://www.bls.gov/schedule/news_release/bls.ics`),
[calendrier BEA](https://www.bea.gov/news/schedule), [calendrier FOMC](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm)
(2026 : 27-28 janv., 17-18 mars, 28-29 avr., 16-17 juin, 28-29 juil., 15-16 sept., **27-28 oct.**, 8-9 déc. ;
2027 : 26-27 janv., 16-17 mars, 27-28 avr., 8-9 juin, 27-28 juil., 14-15 sept., 26-27 oct., 7-8 déc. ;
communiqué à 14:00 et conférence à 14:30, heure de New York).
Sources Telegram : [Bot API](https://core.telegram.org/bots/api), [FAQ limites](https://core.telegram.org/bots/faq)
(texte ≤ 4 096 caractères, ~1 message/s par conversation). Web Push iOS :
[WebKit](https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/).

## 8. Ce que je ne peux pas obtenir moi-même (à faire par toi, détaillé dans le guide d'installation)

1. Passer TradingView en Essential + 2FA + forfait temps réel COMEX (section 6).
2. Créer un bot Telegram (gratuit, 2 minutes) et me donner son jeton via la configuration du serveur.
3. Louer un serveur (VPS) et un nom de domaine, ou me dire lequel tu as.
4. Obtenir le taux de commission MGC « tout compris » affiché par FundedNext/Tradovate.
5. Demander au support FundedNext une **confirmation écrite** que l'usage d'un outil d'alerte personnel est conforme.
6. Optionnel : clé FRED gratuite ; compte Databento (125 $ de crédits) pour valider la stratégie sur le vrai MGC.
