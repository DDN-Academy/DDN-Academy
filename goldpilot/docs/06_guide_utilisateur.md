# 06 — Guide utilisateur

Ce guide s'adresse à toi, utilisateur de GoldPilot, sans connaissances techniques. Il explique ce que fait
le système, comment le mettre en route une première fois, et comment l'utiliser au quotidien.

> **À lire d'abord.** La stratégie de GoldPilot **n'est pas validée** (voir
> [`04_rapport_de_validation.md`](04_rapport_de_validation.md)). Toutes les alertes sont des alertes de
> **SIMULATION** : **ne les exécute pas sur ton compte FundedNext.** Le mode réel est verrouillé dans le site.

---

## 1. Ce que fait GoldPilot, et ce qu'il ne fait pas

**Il fait :**
* reçoit chaque minute le prix du **Micro Gold (MGC, COMEX)** depuis ton graphique TradingView ;
* analyse le marché toutes les 15 minutes avec la stratégie S1 « extension de séance », vérifie les données,
  le calendrier économique (NFP, CPI, PCE, PIB, FOMC) et ton budget de risque FundedNext Flex 50K ;
* t'envoie une alerte **Telegram** sur ton téléphone quand toutes les conditions sont réunies, puis les
  consignes de gestion (déplacer le stop, ne plus entrer, fermer) ;
* suit chaque signal comme une **position simulée** et tient un journal complet de toutes ses décisions ;
* se met en sécurité tout seul (aucun signal) si les données deviennent douteuses.

**Il ne fait pas :**
* il ne passe **aucun ordre** : tu exécutes toi-même sur Tradovate (et seulement le jour où le mode réel
  sera autorisé) ;
* il ne voit **pas** ton compte Tradovate/FundedNext : il ne sait pas si tu as réellement pris un trade,
  à quel prix, ni ton solde réel (tu peux les déclarer dans le site) ;
* il ne garantit aucun gain ; il ne lit pas les actualités ; il ne trade que l'or (MGC).

---

## 2. Première mise en route (dans cet ordre)

### Étape 1 — Mettre le site en ligne
Suis [`05_deploiement_et_exploitation.md`](05_deploiement_et_exploitation.md) : serveur (VPS), nom de
domaine, fichier `.env`, démarrage. À la fin tu dois pouvoir ouvrir `https://ton-domaine` et te connecter
avec ton mot de passe. Les coûts sont listés dans [`07_cles_abonnements_autorisations.md`](07_cles_abonnements_autorisations.md).

### Étape 2 — Créer ton bot Telegram (gratuit, 5 minutes)
1. Dans Telegram, ouvre **@BotFather**, envoie `/newbot`, choisis un nom : BotFather te donne un **jeton**.
2. Mets ce jeton dans la variable `TELEGRAM_BOT_TOKEN` du fichier `.env` du serveur, puis redémarre
   (`05_deploiement_et_exploitation.md`, section 6).
3. Ouvre la conversation avec ton nouveau bot et envoie-lui un message (par exemple « bonjour »).
4. Sur le site : **Réglages › Notifications Telegram › « Détecter mon identifiant »**. Un numéro s'affiche.
5. Copie ce numéro dans `TELEGRAM_CHAT_ID` du `.env`, puis redémarre.
6. Clique sur **« Tester une notification »** : tu dois recevoir « GoldPilot — notification de test reçue ».

Le site ne peut pas écrire lui-même ces deux valeurs : elles restent sur le serveur et ne sont jamais
affichées.

### Étape 3 — Préparer TradingView
Il n'existe **pas d'API** TradingView permettant de « connecter » ton compte ; GoldPilot reçoit les prix
grâce à une alerte TradingView qui appelle le site (un « webhook »). Il te faut :
1. un **abonnement TradingView payant** : le plan gratuit n'envoie pas de webhooks ;
2. la **double authentification (2FA)** activée : TradingView n'autorise les webhooks qu'avec la 2FA
   ([aide TradingView — webhooks](https://www.tradingview.com/support/solutions/43000529348-how-to-configure-webhook-alerts/),
   [configurer la 2FA](https://www.tradingview.com/support/solutions/43000572460-how-to-configure-2fa/)) ;
3. les **données temps réel CME/COMEX** : sans elles, les prix COMEX ont 10 minutes de retard et GoldPilot
   les refuse ([CME sur TradingView](https://www.tradingview.com/cme/),
   [acheter des données](https://www.tradingview.com/support/solutions/43000471705-how-to-purchase-additional-market-data/)).

### Étape 4 — Installer le script et l'alerte TradingView
1. Ouvre le graphique du **contrat MGC daté** en cours, en unité **1 minute**. Le contrat exact est affiché
   sur la page d'accueil du site (bloc « État du marché ») et dans Réglages › TradingView. Au 10/10/2026
   c'est **`COMEX:MGCZ2026`** (MGCZ6 sur Tradovate), jusqu'au roll du 20/11/2026.
   **N'utilise jamais `MGC1!`** (contrat continu) : le script l'affiche en rouge et le serveur refuse.
2. Ouvre l'**éditeur Pine** (« Pine Editor »), colle le script copié depuis **Réglages › TradingView ›
   « Afficher le script Pine » / « Copier le script »** (fichier `pine/goldpilot_bridge.pine`), enregistre-le
   puis ajoute-le au graphique. Il s'appelle **« GoldPilot Bridge »**.
3. Dans les paramètres de l'indicateur, renseigne **« Jeton secret (TV_WEBHOOK_TOKEN du serveur) »** avec la
   valeur de `TV_WEBHOOK_TOKEN` de ton `.env`. Laisse les autres réglages par défaut
   (« Symbole continu pour l'historique journalier » = `COMEX:MGC1!`, « Seuil d'extension k (ATR) » = 5).
4. Crée **une seule** alerte :
   * **Condition** : « GoldPilot Bridge », puis la première option **« Any alert() function call »**
     (en français probablement « Tout appel de la fonction alert() » — libellé français à vérifier à
     l'écran) ([aide TradingView — alertes sur alert()](https://www.tradingview.com/support/solutions/43000597494-alerts-on-alert-function/),
     [FAQ Pine — alertes](https://www.tradingview.com/pine-script-docs/faq/alerts/)) ;
   * la fréquence et le contenu du message sont fixés par le script : ne les modifie pas ;
   * onglet **Notifications** : coche **« Webhook URL »** (URL du webhook) et colle l'adresse affichée dans
     **Réglages › TradingView › « Adresse du webhook »** (de la forme `https://ton-domaine/api/webhooks/tradingview`).
     TradingView n'accepte que les ports 80 et 443 et attend une réponse en moins de 3 secondes
     ([port](https://www.tradingview.com/support/solutions/43000529314-i-cannot-send-webhook-to-a-url-with-a-port-number/),
     [erreurs de webhook](https://www.tradingview.com/support/solutions/43000776894-what-do-errors-mean-when-sending-webhooks/)) ;
   * **expiration** : sur les plans autres que Premium et Ultimate, une alerte expire au bout de 2 mois
     maximum ([aide TradingView](https://www.tradingview.com/support/solutions/43000688759-i-upgraded-to-the-premium-plan-but-my-alerts-still-expiring-in-2-months/)).
     Note la date d'expiration et **recrée l'alerte avant** (sinon le site passera en mode sécurisé
     « données périmées »). Information de sources web, à vérifier dans ton compte.
5. **Vérifie** sur le site : **Journal › Webhooks** doit montrer des messages « Accepté » chaque minute
   pendant les heures de marché. Réglages › TradingView doit afficher « Webhooks reçus ». En cas de refus,
   la raison est écrite (jeton incorrect, adresse IP non autorisée, contrat incorrect…).

Limites connues : une alerte déclenchée plus de 15 fois en 3 minutes est arrêtée par TradingView (le script
est conçu pour rester en dessous) ; **le script n'a jamais été testé sur TradingView** par son auteur
(voir `08_limites.md`) : seule la réception constatée dans Journal › Webhooks fait foi.

### Étape 5 — Vérifier les réglages
* **Réglages › Programme FundedNext** : « FundedNext Futures Flex 50K — Challenge » (par défaut).
* **Réglages › Risque** : profil par défaut 250 $ par trade, 500 $ de perte journalière interne, 3 trades
  et 2 pertes par jour au maximum (justification dans le rapport de validation, § 7).
* **Réglages › Mode de trading** : « Simulation » (le mode réel est verrouillé).
* **Réglages › Compte réel FundedNext** : tu peux y déclarer ton solde ; sans déclaration, le site le dit.

---

## 3. Utilisation quotidienne

### La page d'accueil
Le bandeau du haut résume tout :
* **« Système opérationnel »** (vert) : serveur, données, moteur et notifications fonctionnent ;
* **« Système partiellement opérationnel »** (orange) : un élément demande ton attention (pause,
  notifications non configurées, préchauffage…) ;
* **« Système en panne »** / **« Serveur injoignable »** (rouge) : aucun signal fiable ; les derniers prix
  sont masqués.

Quatre tuiles : **Connexion**, **Données de marché** (source et âge de la dernière barre), **Moteur de
stratégie** et **Notifications (Telegram)**. États du moteur :

| État | Signification |
|---|---|
| Actif | il surveille le marché et peut émettre un signal |
| Préchauffage | pas encore assez d'historique (45 barres de 15 min) ; aucun signal |
| En pause | tu as cliqué « Suspendre les signaux » ; « Reprendre les signaux » pour relancer |
| Mode sécurisé | données douteuses (périmées, en retard, mauvais contrat, saut de prix anormal) : aucun signal, les signaux en attente sont annulés ; reprise automatique quand les données redeviennent bonnes |
| Arrêt de sécurité | performances dégradées au-delà des seuils pré-établis (ou aucune stratégie configurée) : reprise **manuelle** par le bouton de la page d'accueil, après lecture du journal |
| Arrêté | le moteur ne donne plus signe de vie depuis plus d'une minute |

Plus bas : **État du marché** (contrat, prix, séance, régime, prochaine annonce, prochain roll) et
**État du trading** (« Aucun setup valide : les conditions ne sont pas réunies » ou le **signal en cours**,
dernière analyse et ses raisons, risque, compte simulé). Les incidents ouverts s'affichent en haut.

### Quand une alerte de signal arrive
Chaque alerte commence par **« 🧪 SIMULATION — NE PAS EXÉCUTER SUR LE COMPTE »** tant que la stratégie
n'est pas validée. Elle contient : contrat exact, heure (Paris et New York), sens LONG/SHORT, entrée
(immédiate au marché, avec une **plage acceptable**), stop-loss, sortie, rendement/risque, nombre de
contrats MGC, risque estimé en dollars, validité, condition d'annulation, justification, calendrier
économique, source et heure du prix, référence du signal.

**En simulation : ne fais rien sur ton compte.** Tu peux ouvrir le signal sur le site pour suivre la
position simulée et apprendre comment il se comporte.

**Pourquoi « Take-profit : aucun objectif fixe » ?** La stratégie S1 a été testée avec une sortie par
**stop suiveur** (3 ATR derrière le meilleur prix atteint, mis à jour toutes les 15 minutes) et une
**sortie au plus tard à 15:30 New York**. Inventer un objectif fixe qui n'a pas été testé serait présenter
comme validé quelque chose qui ne l'est pas : l'alerte indique donc la règle de sortie exacte et le
rapport gain moyen / perte moyenne historique (≈ 1,98, `production.json`).

### Les alertes de suivi
| Alerte | Ce qu'elle veut dire |
|---|---|
| **Entrée déclenchée** | la position simulée est ouverte au prix indiqué |
| **Déplacer le stop** | nouveau niveau du stop suiveur (toutes les 15 min si le prix progresse) |
| **Ne plus entrer** | le prix est sorti de la plage d'entrée prévue : si tu n'es pas entré, laisse passer |
| **Annonce imminente** | une annonce majeure arrive dans moins de 15 min alors qu'une position est active : vérifie ton stop |
| **Fermer la position maintenant** | heure limite de sortie atteinte (sortie temporelle) |
| **Position sortie** | le stop (ou stop suiveur) a été touché : résultat simulé en R et en dollars |
| **Signal expiré** / **Signal annulé** | plus rien à faire ; la raison est indiquée |

GoldPilot n'envoie **jamais** une alerte de signal devenue inexploitable (signal clos, validité dépassée,
prix hors plage) : elle est marquée « périmée » dans Journal › Alertes.

### Déclarer ce que tu as fait
Sur la page du signal, carte **« Déclarer mon exécution »** : indique si tu l'as exécuté, ton prix
d'entrée, de sortie et le nombre de contrats. Le site l'affiche comme **« déclaré par toi — non confirmé
par le courtier »** et compare tes prix à ceux prévus (page Statistiques › Qualité d'exécution). Tu peux
aussi **annuler** un signal tant que sa position simulée n'est pas ouverte.

### Changement de contrat (roll)
Le MGC change d'échéance environ tous les deux mois. GoldPilot t'envoie l'alerte **« Changement d'échéance
à venir »** 3 jours ouvrés avant la date de roll (prochain : **20/11/2026**, MGCZ2026 → **MGCG2027**).
À cette date : ouvre le graphique du nouveau contrat en 1 minute, ajoute le script, saisis le jeton et
**recrée l'alerte** (puis supprime l'ancienne) ; change aussi de contrat sur Tradovate. Si tu oublies, le
site passe en mode sécurisé (« contrat reçu … différent du contrat actif »).

### Incidents, mode sécurisé, contrôle croisé
* Les incidents s'affichent sur l'accueil et dans **Journal › Incidents**, et la plupart déclenchent une
  alerte Telegram (« Mode sécurisé : aucun signal », « Données rétablies », « Erreur du moteur »,
  « Moteur rétabli », « Arrêt de sécurité »).
* **« Contrôle croisé TradingView en désaccord »** : le script TradingView et le moteur n'ont pas vu la même
  chose (barres perdues ou décalées). Ce contrôle ne décide jamais ; il te dit d'être prudent et de
  vérifier Journal › Webhooks.
* Si le serveur tombe, la procédure est dans `05_deploiement_et_exploitation.md`, section 14.

---

## 4. Le mode réel (verrouillé)
Le passage en réel est refusé par le serveur tant que : (1) la stratégie n'est pas validée selon le
protocole, (2) tu n'as pas déclaré dans **Réglages › Mode de trading** la **confirmation écrite de
FundedNext** (avec sa référence) que l'usage de cet outil personnel est autorisé, (3) tu n'as pas tapé
exactement « JE CONFIRME LE PASSAGE EN REEL ». Les deux premières conditions ne sont pas remplies
aujourd'hui. Voir `08_limites.md`.

## 5. Les autres pages
* **Historique** : tous les signaux, filtrables par statut (en attente, actif, clôturé, annulé, expiré).
* **Statistiques** : verdict de la recherche, suivi papier, qualité d'exécution, Monte-Carlo, contexte
  macro (taux et dollar via FRED, **information seulement**, jamais utilisé pour décider).
* **Journal** : Décisions, Incidents, Alertes, Webhooks, Contrôle croisé, Audit.
* **Aide** : résumé de ce guide dans le site.
* Captures d'écran (données fictives) : [`captures/`](captures/README.md).
