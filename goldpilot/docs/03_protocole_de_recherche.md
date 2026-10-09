# 03 — Protocole de recherche (pré-enregistré avant tout backtest des candidats)

Rédigé le 9 octobre 2026, après l'étude exploratoire sur l'entraînement uniquement
(`research/output/etude_exploratoire/etude.md`) et **avant** tout backtest des candidats ci-dessous.
La date du commit Git qui introduit ce fichier fait foi ; toute modification ultérieure est tracée.

## 0. Transparence préalable

Ces mêmes fichiers de données ont été explorés lors d'une session de travail antérieure, abandonnée à
ta demande (stratégies de cassure, 168 configurations testées sur 2011-2021 ; une famille de cassure
évaluée à titre exploratoire sur 2022-2025). Les candidats ci-dessous sont **différents** et dérivent de
l'étude exploratoire de cette session. Pour rester honnête sur les tests multiples, le Deflated Sharpe
Ratio est calculé en comptant **aussi** ces 168 essais antérieurs.

## 1. Données et découpage

* XAUUSD spot (proxy du MGC : dynamique intraday quasi identique, niveau de prix différent de la base
  de portage). Barres de 15 min en UTC selon `backend/goldpilot/research/conventions.json`.
* Entraînement : 01/05/2011 → 31/12/2018 ; validation : 01/01/2019 → 31/12/2021 ;
  **test final : 01/01/2022 → 28/10/2025**, exécuté une seule fois, sur les seules configurations éligibles.
* Walk-forward : fenêtres glissantes de 3 ans, test sur l'année suivante, années de test 2014 → 2021.
* Contrôle de résolution : février → octobre 2025 rejoué avec exécution sur barres de 5 minutes.

## 2. Modèle de coûts (MGC, conditions actuelles)

Les coûts d'un contrat MGC sont fixes en dollars par once (tick de 0,10 $, commission par contrat) alors
que la volatilité de l'or évolue avec son prix. Le système sera utilisé avec un or autour de 4 000 $ :
le coût pertinent est donc le coût **rapporté au prix actuel**. Modèle principal = coûts proportionnels
au prix, calibrés sur 4 000 $ :

| Composant | à 4 000 $ | en fraction du prix |
|---|---|---|
| Commission + frais aller-retour (hypothèse 2 $/contrat, à remplacer par le tarif FundedNext réel) | 0,20 $/oz | 0,50 pb |
| Demi-spread à chaque exécution au marché ou stop | 0,05 $/oz | 0,125 pb |
| Glissement sur ordre stop (sortie au stop) | 0,10 $/oz | 0,25 pb |
| Glissement si la barre a une amplitude > 3 ATR | 0,30 $/oz | 0,75 pb |

Tests de stress obligatoires et publiés : coûts × 2 ; coûts fixes de 0,50 $/oz aux prix historiques
(beaucoup plus pénalisants avant 2020).

## 3. Règles d'exécution simulée (prudentes)

* Décision à la clôture d'une barre ; entrée au marché à l'ouverture de la barre suivante (+ demi-spread).
* Toute la barre d'entrée est postérieure à l'entrée : si son extrême défavorable atteint le stop, le stop est touché.
* Stop atteint par un gap : sortie à l'ouverture (pire prix). Stop et objectif dans la même barre : stop d'abord.
* Stop suiveur mis à jour à la clôture de chaque barre, effectif à partir de la suivante.
* Sortie temporelle à l'ouverture de la première barre ≥ heure de sortie ; aucune position après 15:45
  New York (FundedNext ferme à 16:10 New York).
* Une seule position à la fois.

## 4. Candidats (hypothèses issues de l'étude exploratoire)

### S1 — Extension de séance (momentum de « journée de tendance »)
Hypothèse : quand le prix s'est fortement éloigné de sa moyenne de séance pendant Londres ou New York,
des flux directionnels persistants sont à l'œuvre ; le mouvement tend à se prolonger (étude : +0,14 à
+0,20 ATR sur 2 h, t ≈ 6-7, 7 années sur 8 positives).

* Moyenne de séance SM = moyenne des prix typiques (H+L+C)/3 depuis 18:00 New York ; z = (C − SM) / ATR(40).
* Décision sur les barres qui clôturent entre 03:00 et 13:00 New York.
* Achat si z franchit +k (z > k et z précédent ≤ k), premier franchissement haussier du jour ; vente symétrique.
  Au plus un achat et une vente par jour.
* Filtre F (optionnel) : pas de trade si l'amplitude relative (H−L)/C de la veille est dans le tiers
  supérieur des 250 journées précédentes (hypothèse : en volatilité extrême, les prolongements échouent plus souvent).
* Stop initial : entrée ∓ s × ATR ; stop suiveur : plus haut (plus bas) depuis l'entrée ∓ t × ATR ; sortie au plus tard à 15:30.
* Grille : k ∈ {3, 4, 5} ; s ∈ {1,5 ; 2,5} ; t ∈ {2 ; 3} ; F ∈ {non, oui} → **24 configurations**.

### S2 — Continuité Londres → New York
Hypothèse : la direction prise pendant Londres (02:00 → 08:00) se prolonge pendant la matinée de New
York (étude : +0,32 ATR, t = 2,4 — piste plus faible, testée car économiquement plausible : les flux
européens et américains se succèdent dans le même sens).

* À la clôture de 08:00 : m = (C(08:00) − C(02:00)) / ATR. Si |m| ≥ q, entrée dans le sens de m.
* Stop initial s × ATR. Sortie E : « 12:00 » (sortie à 12:00) ou « suivi » (stop suiveur 3 ATR, sortie à 15:30).
* Grille : q ∈ {2, 4} ; s ∈ {2, 3} ; E ∈ {12:00, suivi} → **8 configurations**.

### Écartés par l'étude exploratoire (non testés)
Retour à la moyenne en Londres et cassures asiatiques (effets réels mais inférieurs aux coûts), range
d'ouverture New York et balayage du plus haut/bas de la veille (aucun effet significatif).
Volume profile et carnet d'ordres : données indisponibles (volume = ticks du broker). Dollar et taux
intraday : non disponibles historiquement ; utilisés uniquement comme contexte affiché.

## 5. Critères d'éligibilité (base de coûts principale)

Pour chaque famille, la configuration de production est celle qui maximise la statistique t de
l'espérance en R (n ≥ 30) sur 2011-2021. La famille est éligible si **toutes** les conditions suivantes sont remplies :

1. Walk-forward 2014-2021 (re-sélection annuelle par la même règle) : espérance > 0 et borne basse
   de l'intervalle de confiance bootstrap (par journées) unilatéral à 95 % > 0.
2. Validation 2019-2021 de la configuration de production : espérance > 0 et profit factor ≥ 1,10.
3. Coûts × 2 sur la validation : espérance ≥ 0.
4. Au moins 60 % des années 2011-2021 positives.
5. Au moins 70 % des configurations voisines (un paramètre décalé d'un cran) positives sur l'entraînement.
6. Deflated Sharpe Ratio ≥ 0,90 avec N = 32 + 168 = 200 essais.

## 6. Test final (une seule exécution)

Configuration éligible (et combinaison S1 + S2 si les deux le sont, une position à la fois) :
espérance > 0 avec borne basse unilatérale à 95 % > 0 ; profit factor ≥ 1,10 ; drawdown maximal
inférieur au 95e centile Monte-Carlo issu de 2011-2021. En cas d'échec : « STRATÉGIE NON VALIDÉE »,
simulation uniquement.

## 7. Profil de risque (Monte-Carlo, règles Flex 50K)

Rééchantillonnage de journées entières (jours sans trade inclus), règles Flex 50K (objectif 2 500 $,
plancher trailing fin de journée 1 500 $ verrouillé à 50 100 $, consistance 40 % = objectif relevé,
30 micros max, contrats entiers, clôture 16:10), horizon 120 jours de trading, 10 000 trajectoires.
Grille de risque par trade : 75, 100, 125, 150, 200, 250 $. Profil par défaut : celui qui maximise la
probabilité de réussite sous la contrainte P(violation avant réussite) ≤ 20 % ; à égalité, le plus faible.

## 8. Restrictions non testables historiquement (sécurité ajoutée en production)

Pas de nouvelle entrée de 10 min avant à 15 min après une annonce américaine majeure (NFP, CPI, PCE,
PIB, FOMC) : le calendrier historique n'est pas disponible, ce filtre n'est donc pas inclus dans les
backtests ; il ne peut que retirer des trades.

## 9. Validation prospective (seule voie vers le mode réel)

Paper trading sur le flux MGC réel : au moins 60 jours de trading, espérance > 0 avec borne basse
unilatérale à 95 % > 0 sur les signaux paper, glissement réel ≤ glissement supposé, résultats au-dessus
du 5e centile Monte-Carlo. Le passage au réel reste une décision manuelle de l'utilisateur.
