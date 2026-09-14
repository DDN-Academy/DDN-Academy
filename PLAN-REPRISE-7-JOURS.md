# PLAN DE REPRISE — 7 JOURS
**Lundi 14 → Dimanche 20 septembre 2026**

---

## LA VÉRITÉ EN 5 LIGNES

1. Tes créneaux (12h30-14h, 18h30-20h) **n'ont aucun avantage en intraday** — vérifié sur 21 ans.
2. La seule approche qui tient dans ta vie : **le swing sur graphique journalier**, 15 min par jour à 19h.
3. Testé sur l'or : **25 combinaisons de paramètres sur 25 sont rentables hors échantillon.** L'avantage est réel.
4. Sur 1 seul marché : 15 trades/an → trop lent. Sur **5 marchés** : ~75 trades/an → exploitable.
5. Même en faisant tout bien : **~4,5 mois pour passer un challenge**, pas 3 semaines. Tout plan qui te promet mieux te ment.

---

## 1. LE SYSTÈME

### Les marchés (5, choisis pour être décorrélés)
| # | Marché | Pourquoi |
|---|--------|----------|
| 1 | **Or** (XAUUSD) | Le seul que j'ai backtesté : PF 1,47 sur 22 ans |
| 2 | **EUR/USD** | Devise majeure, spread faible |
| 3 | **Indice US** (US500 ou Nasdaq) | Tendances longues et propres |
| 4 | **Pétrole** (WTI) | Décorrélé des trois autres |
| 5 | **GBP/USD** ou **Cuivre** | Complète la diversification |

> **Honnêteté** : je n'ai pu backtester que l'or (c'est la seule donnée que j'avais). Le principe multi-marchés est la fondation de toute l'industrie du trend following depuis 40 ans — mais applique-le d'abord en démo et vérifie chaque marché toi-même.

### Les règles (identiques sur les 5 marchés)

**Filtre de tendance**
- Clôture d'hier **au-dessus** de l'EMA 200 journalière → tu n'as le droit que d'**acheter**
- Clôture d'hier **en-dessous** → tu n'as le droit que de **vendre**
- Jamais l'inverse. Aucune exception.

**Entrée — ordre stop, jamais à la main**
- **Achat** : ordre stop d'achat placé au **plus-haut des 20 derniers jours**
- **Vente** : ordre stop de vente placé au **plus-bas des 20 derniers jours**
- ⚠️ L'ordre se déclenche tout seul quand le prix touche le niveau. **Tu n'attends pas la clôture.** (J'ai testé la version « attendre la clôture » : elle est perdante. PF 0,92.)

**Stop initial**
- À **1 × ATR(14) journalier** de ton entrée. Posé en même temps que l'ordre d'entrée, jamais après.

**Sortie**
- **Trailing stop à 1,5 × ATR**, ajusté une fois par jour, uniquement dans le sens du profit.
- Aucune sortie manuelle. Aucun objectif de gain. Le trailing décide, pas toi.

### Ce que ces règles ont produit (or, 2004-2025, 326 trades)
```
Réussite        39,0 %          Gagnant moyen   +1,88 R
Profit Factor    1,47           Perdant moyen   -0,82 R
Espérance     +0,236 R/trade    Drawdown max    -15,2 R
17 années positives sur 21      Pire série      8 pertes d'affilée
```

---

## 2. MONEY MANAGEMENT

### La règle de taille
```
Risque par trade = 1 % du capital       (jamais plus, jamais "juste cette fois")
Taille = (capital × 1%) ÷ (ATR14 en points × valeur du point)
```

### Les coupe-circuits
| Seuil | Action |
|---|---|
| **3 positions ouvertes** | Plus aucune nouvelle entrée |
| **−6 % sur le mois** | Arrêt total jusqu'au mois suivant + audit écrit |
| **8 pertes d'affilée** | Normal (déjà vu dans le backtest). Tu continues. |
| **−10 % sur le compte** | Arrêt définitif du projet, retour en démo |

### Pourquoi 1 % et pas 3 %
| Risque | Réussite challenge | Durée |
|---|---|---|
| 1 % | **87,4 %** | 18 mois (1 marché) / ~4,5 mois (5 marchés) |
| 3 % | 64,0 % | 3 mois — **1 chance sur 3 de tout perdre** |

Avec 500 € et zéro revenu, tu ne peux pas te permettre un pari à 36 % d'échec.

---

## 3. LES 7 JOURS (1h-1h30/jour, 0 € dépensé)

### LUNDI — L'audit brutal (1h)
Le seul jour où tu regardes en arrière. Écris :
- Combien perdu au total sur l'année 1 : ________
- Sur combien de trades environ : ________
- Ton pire trade, et **ce qui l'a déclenché** : ________
- Combien de fois tu as augmenté la taille après une perte : ________
- La règle que tu as violée le plus souvent : ________

**Sans ces 5 chiffres, tu répètes l'année 1.**

### MARDI — Le contrat d'argent (1h)
Écris et signe :
> « L'argent qui a le droit de toucher le trading : **______ €**.
> Cet argent est perdu d'avance dans ma tête. Si je le perds, ma vie ne change pas.
> Je ne rajouterai jamais un euro pour "me refaire".
> Condition pour débloquer ces fonds : **avoir un revenu régulier + 50 trades démo documentés.** »

Avec zéro revenu aujourd'hui, le montant honnête est **0 €**. Les 500 € restent ta marge de survie.

### MERCREDI — Le vrai chantier : le revenu (1h30)
**C'est ici que se joue ton année, pas sur un graphique.**
- Liste 5 pistes de revenu activables sous 30 jours
- Choisis-en 2
- Fais le premier geste concret aujourd'hui (un message, une candidature, une annonce)

Le trading avec l'argent du loyer produit exactement les décisions qui t'ont coûté l'année 1. **Le revenu n'est pas un à-côté du plan : c'en est la condition.**

### JEUDI — Installation (1h)
- Ouvre un compte **démo** (TradingView + ton broker)
- Crée 5 graphiques journaliers, un par marché
- Sur chacun : EMA 200, ATR(14), et les lignes plus-haut/plus-bas 20 jours
- Sauvegarde le modèle de graphique

### VENDREDI — La routine de 15 minutes (1h)
Écris ta checklist et exécute-la une fois pour de vrai :
1. Pour chaque marché : noter EMA200, plus-haut 20j, plus-bas 20j, ATR14
2. Le prix est-il au-dessus ou en-dessous de l'EMA200 ? → sens autorisé
3. Placer/mettre à jour les ordres stop d'entrée
4. Ajuster le trailing des positions ouvertes
5. Fermer l'ordinateur

**Chrono en main. Si ça prend plus de 20 min, simplifie.**

### SAMEDI — L'entraînement (1h30)
Remonte les **12 derniers mois** sur chaque graphique journalier. À la main, repère chaque signal qu'aurait donné le système. Note-les. Tu vas voir de tes yeux les 8 pertes d'affilée — **c'est le but**. Tu dois les avoir vues avant de les vivre.

### DIMANCHE — Critères go/no-go (1h)
Écris à froid ce qui devra être **vrai** avant de risquer un centime :
- [ ] J'ai un revenu régulier
- [ ] J'ai 50 trades démo documentés
- [ ] Mon taux de respect des règles est > 95 %
- [ ] Mon Profit Factor démo est > 1,2
- [ ] Je peux perdre le montant du challenge sans que ma vie change

**Tant que ces 5 cases ne sont pas cochées, aucun euro ne sort.**

---

## 4. LA PROP FIRM — LAQUELLE, QUAND, COMBIEN

### Le type qu'il te faut
Tu fais du **swing** : tu gardes des positions plusieurs jours. Donc :
- ❌ **PAS de prop firm futures** (Topstep, MyFundedFutures…) — elles imposent d'être à plat chaque soir. Incompatible.
- ✅ **Prop firm forex/CFD** — elles autorisent le maintien overnight et week-end.

### Les critères de choix (dans cet ordre)
1. **Ancienneté réelle** — au moins 5 ans d'existence et de paiements prouvés
2. **Pas de limite de temps** sur le challenge — indispensable, ton système est lent
3. **Maintien overnight ET week-end autorisé** — sinon ton système ne marche pas
4. **Le moins cher possible** — ton budget doit couvrir 2-3 tentatives

> ⚠️ **Je n'ai pas pu vérifier les tarifs et règles actuels** : le proxy réseau de mon environnement bloque les sites de prop firms. Les prix et règles changent tous les mois. **Vérifie ces 4 points toi-même, à la source, avant de payer.** Ne te fie à aucun comparatif en ligne : ils sont presque tous affiliés.

### Le budget (sur 500 €)
```
Challenge le plus petit      ~100-150 €   ← une seule tentative à la fois
Réserve 2e tentative         ~150 €
Réserve 3e tentative         ~150 €
JAMAIS dépensé               ~50-100 €
```
**Ne prends jamais un gros compte "parce que le gain serait plus gros".** Le petit compte te donne 3 essais. Le gros t'en donne un.

### QUAND acheter
Pas une date. **Les 5 cases du dimanche.** Toutes cochées, sinon rien.

---

## 5. LES 6 RÈGLES QUI TE PROTÈGENT DE TOI-MÊME

1. **Une seule stratégie.** Tu ne changes rien pendant 100 trades. Le saut de stratégie est ce qui tue les traders qui reviennent.
2. **Taille fixe.** 1 %. Jamais augmentée après un gain, jamais après une perte.
3. **Ordres posés, écran fermé.** Tu ne regardes pas le marché en journée. C'est tout l'intérêt du swing.
4. **Tout est journalisé.** Chaque trade : date, marché, sens, entrée, stop, sortie, R, règles respectées O/N.
5. **Une revue par semaine**, le dimanche, 20 minutes. Tu regardes ton taux de respect des règles — **pas ton argent**.
6. **Les 8 pertes d'affilée arriveront.** Elles sont dans le backtest. Le jour où elles arrivent, tu ne changes rien.

---

## CE QUE CE PLAN NE PROMET PAS

Il ne promet pas que tu seras rentable cette année. Avec 15-75 trades par an, il faut **12 mois pour savoir** si ton exécution est bonne, et ~4,5 mois au mieux pour passer un challenge.

Ce plan promet une seule chose : **que tu ne reperdes pas l'argent que tu n'as pas.**

C'est la seule promesse qui valait la peine d'être tenue cette année.
