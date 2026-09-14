---
matiere: Techniques statistiques — L1 Portail, Division A, AMU
chapitre: Chapitre 2 — Résumer pour informer
titre: Résumer pour informer
sous_titre: Position, dispersion, concentration — cours resserré et système de révision
resume: Ce document reconstruit le deuxième chapitre de Techniques statistiques et couvre les 70 diapositives du support, sans exception. Les quatorze questions posées en amphithéâtre y sont corrigées, chaque formule est démontrée et illustrée par un calcul complet, et tous les chiffres du support ont été recalculés — ce qui a révélé quatre anomalies, signalées à l'endroit exact. Le cours tient en une trentaine de pages ; le reste est un système de révision destiné à être consulté et pratiqué, non lu. Une version intégrale, deux fois plus développée, accompagne ce document pour les points qui résistent.
date: 10 septembre 2026
duree: lecture du cours 2 h — maîtrise complète ≈ 12 h réparties sur 3 semaines
version: 2.0
sommaire: oui
---

# Chapitre 2 — Résumer pour informer

::: methode Ce que contient ce document, et comment on s'en sert
Les **70 diapositives** du support y sont couvertes sans exception — le **tableau de
couverture** en annexe permet de le vérifier ligne par ligne. Les **quatorze questions** posées
à l'amphithéâtre sont intégralement corrigées, et **tous les chiffres ont été recalculés**.

| Partie | Pages | Ce que tu en fais |
|---|:---:|---|
| **§ 1 — Carte** | **2** | Tu la lis **une fois**, avant tout le reste |
| **§ 2 — Le cours** | **18** | Tu le lis **deux fois** : une fois pour comprendre, une fois stylo en main |
| **§ 3 — Vigilance** | **4** | Tu le relis **avant l'examen** |
| **§ 4 — Ancrage** | 12 | Tu ne le **lis pas** : fiche, 65 cartes et schéma se **consultent**, en boucle |
| **§ 5 — Entraînement** | 28 | Tu le **fais**, tu ne le lis pas — 10 exercices et une simulation de 2 h |
| **§ 6 + annexe** | 6 | Contrôle final et preuve de couverture |

**La charge de lecture réelle est de 27 pages** — pour un chapitre de 70 diapositives. **Les
46 pages restantes ne se lisent pas : elles se consultent et se pratiquent.**

**Un second fichier accompagne celui-ci :** ***Résumer pour informer — version intégrale***.
Même contenu, deux fois plus développé : chaque démonstration détaillée, chaque tableau de
calcul ligne par ligne, chaque vérification refaite sous tes yeux. **Tu ne le lis jamais d'un
bout à l'autre — tu l'ouvres quand un point de ce cours-ci résiste.** Les renvois
« ➔ intégrale § X » t'y conduisent, aux mêmes numéros de paragraphes.
:::

<!--saut-->

## 1. Carte du chapitre

### 1.1 — Vue d'ensemble

Le chapitre 1 apprenait à **présenter** une distribution **sans rien perdre**. Celui-ci apprend
à la **résumer** — donc à **perdre volontairement** de l'information, en échange d'une capacité
de comparaison et de décision. **La perte est le prix de la décision** : on ne décide pas devant
1 200 nombres.

**Trois familles d'indicateurs, trois questions :**

| Famille | Question | Indicateurs |
|---|---|---|
| **Position** | **Où** se situe la distribution ? | Mode · Moyenne · Médiane |
| **Dispersion** | **À quel point** est-elle étalée ? | Étendue · écarts inter-quantiles · EAM · variance · écart-type · coefficient de variation |
| **Concentration** | Comment le **total** se partage-t-il ? | Part de l'agrégat · courbe de Lorenz · indice de Gini |

### 1.2 — Les dix idées maîtresses

1. **Résumer, c'est perdre de l'information à dessein.** Tout le chapitre consiste à choisir
   *quoi* perdre.
2. **La position seule ne suffit jamais** : deux distributions de même moyenne peuvent être
   radicalement différentes. Une moyenne sans dispersion est une information incomplète — et en
   finance, dangereuse.
3. **Dès que les classes ont des amplitudes inégales, il faut raisonner en densité**, pas en
   effectif. C'est vrai pour le mode comme pour l'histogramme, où **l'aire représente
   l'effectif**.
4. **La somme des écarts à la moyenne est nulle.** C'est de ce fait que découle toute la section
   dispersion : il faut casser les signes, par la valeur absolue (EAM) ou par le carré
   (variance).
5. **La variance est une étape, l'écart-type est la réponse.** La variance est en unité au
   carré, donc ininterprétable.
6. **Koenig rend l'agrégation possible** : deux sommes suffisent à transmettre un groupe.
7. **Ce qui repose sur des sommes s'agrège ; ce qui repose sur des rangs ne s'agrège pas.**
   Moyenne et variance oui ; médiane, quantiles et Gini non.
8. **La concentration n'existe que si la somme de la variable a un sens.** Salaires oui, notes
   et âges non.
9. **La courbe de Lorenz se lit par sa distance à la diagonale**, et sa pente en chaque point
   vaut $ m_{X_k}/m_X $.
10. **Le choix de l'indicateur dépend du type de données ET de l'objectif.** C'est la seconde
    moitié de la phrase qu'on oublie.

### 1.3 — Prérequis, enseignés ici

::: definition Les six notions du chapitre 1 à avoir en tête
| Notion | Rappel |
|---|---|
| **Effectif $ n_i $ / fréquence $ f_i $** | $ f_i = n_i/n $ ; $ \sum f_i = 1 $ |
| **Fréquence cumulée $ F_k $** | $ F_k = \sum_{i \le k} f_i $ ; **croissante**, $ F_p = 1 $. Répond à « **au plus** cette modalité » |
| **Fonction de répartition** | L'application $ x \mapsto F(x) $. **Les quantiles en sont l'inverse** |
| **Série brute / distribution** | Un individu par case / une modalité par ligne avec son effectif |
| **Variable discrète / continue** | Comptage / mesure. **La continue impose des classes**, donc des amplitudes |
| **Classe, borne, amplitude** | $ [b_{inf} ; b_{sup}[ $ ; amplitude $ a_i = b_{sup} - b_{inf} $ |
:::

### 1.4 — Lien avec la finance de marché

::: marche Les cinq traductions, à connaître par cœur
| Statistique | Finance de marché |
|---|---|
| **Moyenne** | Rendement espéré |
| **Écart-type** | **VOLATILITÉ** — annualisée en multipliant par $ \sqrt{252} $ sur des rendements quotidiens, $ \sqrt{12} $ sur des mensuels |
| **Quantile** | **Value at Risk** — la VaR à 99 % est le centile d'ordre 1 de la distribution des pertes |
| **Rapport $ m/\sigma $** | Structure du **ratio de Sharpe** — donc **le coefficient de variation en est l'inverse** |
| **Décomposition intra / inter** | **Risque spécifique / risque systématique.** La diversification agit sur l'intra, jamais sur l'inter |
| **Lorenz et Gini** | **Concentration d'un portefeuille** (parent de l'indice de Herfindahl $ HHI = \sum w_i^2 $) ou d'un P&L |

**Le point à retenir :** une stratégie à 8 % de rendement moyen avec $ \sigma = 3\,\% $ et une
autre à 8 % avec $ \sigma = 40\,\% $ ne se gèrent pas de la même façon. **La moyenne décrit
l'espérance ; l'écart-type décrit ce qu'il faut survivre pour l'atteindre.**
:::

<!--saut-->

## 2. Le cours

### 2.1 — Résumer la position (diapositives 3 à 26)

#### 2.1.1 Les trois indicateurs de position (d. 3)

::: definition Mode, moyenne, médiane
| Indicateur | Définition | Utilisable sur |
|---|---|---|
| **Mode** | La modalité de **fréquence maximale** | **Toute** variable, y compris **qualitative** — c'est le seul dans ce cas |
| **Moyenne** | Le **centre de gravité** : elle utilise **toutes les valeurs** | Quantitative cardinale |
| **Médiane** | Le **centre de l'effectif** : elle n'utilise que **le rang** | Quantitative, et ordinale |
:::

#### 2.1.2 Le mode et la classe modale (d. 4 à 9)

::: definition Mode, classe modale, amplitude, densité
**Mode** = modalité de fréquence maximale. **Variable continue → « classe modale »** :
l'indicateur désigne un **intervalle**, pas une valeur. *Dire « le mode est [20 ; 30[ » est un
abus de langage sanctionné.*

$$ a_i = b_{sup} - b_{inf} \qquad d_i = \frac{n_i}{a_i} $$

⚠ **Dès que les amplitudes sont inégales, la classe modale est celle de densité maximale, pas
d'effectif maximal.** Une classe deux fois plus large contient mécaniquement plus d'individus
sans être plus dense.
:::

::: correction Les deux illustrations du support, corrigées
**① Logements en Outre-mer, recensement 2023 (d. 4-5) — trois questions posées, aucune réponse.**

| Type de logement | Guadeloupe | Martinique | Guyane | Réunion |
|---|---:|---:|---:|---:|
| Habitation de fortune | 1 098 | 790 | 3 698 | 1 867 |
| Case traditionnelle | 2 322 | 578 | 1 798 | 23 062 |
| Maison ou immeuble en bois | 8 363 | 6 086 | 11 841 | 12 913 |
| **Maison ou immeuble en dur** | **168 050** | **164 290** | **71 089** | **321 445** |
| **Ensemble** | **179 833** | **171 743** | **88 425** | **359 288** |

**Q1 — Éléments statistiques.** Population : les **logements** des quatre territoires en 2023.
Unité : **un logement**. Taille : par territoire, et $ N = 799\,289 $ pour l'ensemble.
**Deux caractères, tous deux qualitatifs nominaux** : le **type de logement** (4 modalités) et
la **zone géographique** (4 modalités).
**Q2 — Est-ce une distribution au sens classique ? Non.** Une distribution associe un effectif à
chaque modalité d'**une seule** variable ; ici **quatre distributions sont juxtaposées**, une par
territoire. La zone géographique est la variable de **découpage**, le type de logement la
variable **étudiée**.
**Q3 — Le mode :** « **maison ou immeuble en dur** », dans les quatre territoires — de **80 %**
(Guyane) à près de **94 %** (Guadeloupe) des logements.
⚠ *Trois colonnes ne bouclent pas à une unité près (Martinique 171 744 recalculé contre 171 743
annoncés ; Guyane 88 426 contre 88 425 ; Réunion 359 287 contre 359 288). **Ce n'est pas une
erreur mais un effet d'arrondi** : la somme des arrondis n'est pas l'arrondi de la somme. **Ne
corrige pas le total publié ; signale-le.***

**② Personnes incarcérées par tranche d'âge (d. 6-9) — le cas des amplitudes inégales.**
Le support passe d'un diagramme en effectifs à un diagramme en **densités**, et la classe modale
change. **C'est l'exemple qui justifie toute la notion.** ➔ intégrale § 2.1.3 pour le tableau
recalculé ligne par ligne.
:::

#### 2.1.3 L'histogramme (d. 10-11)

::: formule L'aire représente l'effectif
Dans un **histogramme**, la **hauteur** porte la **densité** et **l'aire porte l'effectif** :
$$ \text{aire} = d_i \times a_i = \frac{n_i}{a_i} \times a_i = n_i $$

| | **Histogramme** | **Diagramme en barres** |
|---|---|---|
| Hauteur | **Densité** | **Effectif** |
| Ce qui représente l'effectif | **L'aire** | La hauteur |
| Quand l'employer | Variable **continue**, classes | Variable discrète ou qualitative |

⚠ **Porter les effectifs en hauteur avec des amplitudes inégales produit une figure fausse** :
l'aire vaut alors $ n_i \times a_i $, et les classes larges paraissent surreprésentées.
**Contrôle : la somme des aires doit redonner l'effectif total.**
:::

#### 2.1.4 La moyenne : trois écritures (d. 12 à 15)

::: formule Les trois formules, et leur équivalence
$$ m_X = \frac{1}{N}\sum_{i=1}^{N} x_i \qquad m_X = \sum_{i=1}^{p} f_i x_i \qquad m_X = \sum_{k=1}^{K} \frac{N_k}{N}\, m_{X_k} $$
**(1) données brutes · (2) distribution · (3) agrégation.** *Ce sont trois regroupements de la
même somme :* $ \frac{1}{N}\sum n_i x_i = \sum \frac{n_i}{N} x_i = \sum f_i x_i $.

⚠ **L'avertissement du support sur l'agrégation, à ne pas manquer :** « il s'agit de la
fréquence du caractère qui **scinde la population en sous-groupes** et non de la fréquence du
caractère $ X $ qui nous intéresse ». **On pondère toujours par des effectifs de population,
jamais par des valeurs de la variable étudiée.**

**L'erreur type — la moyenne simple des moyennes :** deux groupes de 900 et 100 personnes
gagnant 2 000 € et 4 000 €. Moyenne simple $ = 3\,000 $ € ✖ ;
moyenne pondérée $ = \frac{900}{1000}(2\,000) + \frac{100}{1000}(4\,000) = 1\,800 + 400 = \mathbf{2\,200} $ € ✔
:::

#### 2.1.5 Les trois propriétés de la moyenne (d. 16, 17, 19) et l'application (d. 18)

::: formule Les trois propriétés
**① La somme des écarts à la moyenne est nulle.**
$$ \sum_{i=1}^{N}(x_i - m_X) = \sum x_i - N m_X = N m_X - N m_X = 0 $$
**⚠ C'est la propriété qui commande toute la section dispersion** : un indicateur fondé sur la
moyenne des écarts vaudrait **0 pour toute distribution**. D'où les valeurs absolues et les
carrés.

**② La moyenne est un opérateur linéaire :** $ m_{aX+b} = a\,m_X + b $.
**C'est elle qui autorise l'agrégation** — ce que l'écart-type ne permettra pas.

**③ La moyenne est sensible aux valeurs extrêmes.** Elle utilise **la valeur** de chaque
observation ; la médiane n'utilise que **le rang**. « Deux écarts de 5 comptent autant qu'un
écart de 10. »
:::

::: correction Application : les salaires des fonctionnaires (d. 18) — deux questions, aucune réponse
| | Fréq. 2022 (%) | Fréq. 2023 (%) | Salaire moyen 2022 (€) | Salaire moyen 2023 (€) |
|---|---:|---:|---:|---:|
| Catégorie A | 68,4 | 68,7 | 3 193 | 3 373 |
| Catégorie B | 18,7 | 18,9 | 2 632 | 2 720 |
| Catégorie C | 12,9 | 12,4 | 2 161 | 2 283 |
| **Titulaires A+B+C** | **100,0** | **100,0** | **2 955** | **3 116** |

**Q1 — Le salaire moyen**, par agrégation (formule 3), les fréquences étant les **poids** :
**2022 :** $ 0{,}684(3\,193) + 0{,}187(2\,632) + 0{,}129(2\,161) = 2\,184{,}0 + 492{,}2 + 278{,}8 = \mathbf{2\,955{,}0} $ € — **coïncide exactement** avec le tableau ✔
**2023 :** $ 0{,}687(3\,373) + 0{,}189(2\,720) + 0{,}124(2\,283) = 2\,317{,}3 + 514{,}1 + 283{,}1 = \mathbf{3\,114{,}4} $ €
⚠ **Le tableau annonce 3 116 € : un écart de 1,6 €, soit 0,05 %**, expliqué par l'**arrondi des
fréquences à une décimale**. **Il faut le signaler, pas le masquer.**

**Q2 — La masse salariale**, avec 1,8 million d'agents :
$$ \sum x_i = N \times m = 1\,800\,000 \times 3\,116 = 5\,608\,800\,000 \text{ €} $$
soit **5,61 milliards d'euros par mois** et **67,3 milliards par an**.
*Précisions attendues : masse **nette**, **mensuelle** avant multiplication, **champ** agents
fonctionnaires en France hors Mayotte.*

::: examen
**La relation à retenir absolument :** $ \sum_{i=1}^{N} x_i = N \times m $ — **la somme est la
moyenne multipliée par l'effectif.** Elle sert **trois fois** dans le chapitre : ici, à la
diapositive 57 (variance par agrégation) et à la diapositive 60 (part de l'agrégat).
:::
:::

#### 2.1.6 La médiane (d. 20 à 26)

::: formule Définition et calcul
**Deux définitions équivalentes :** la valeur qui partage la population **ordonnée** en deux
effectifs égaux ; ou la valeur $ Me $ telle que $ F(Me) = 0{,}5 $.

**Sur données brutes — trier d'abord, toujours.**
$ N $ **impair** → valeur de rang $ \frac{N+1}{2} $.
$ N $ **pair** → **moyenne des valeurs de rang $ \frac{N}{2} $ et $ \frac{N}{2}+1 $** : il
n'existe pas d'observation centrale.

**Sur une distribution groupée — interpolation linéaire**, sous hypothèse de répartition
uniforme dans la classe :
$$ Me = b_{inf} + a \times \frac{0{,}5 - F(b_{inf})}{F(b_{sup}) - F(b_{inf})} $$

**Le diagnostic d'asymétrie — deux chiffres suffisent :**
$ Me < m_X $ → **étalée à droite** (salaires, patrimoines) · $ Me > m_X $ → étalée à gauche ·
$ Me \approx m_X $ → symétrique.
:::

::: correction Les densités de population en Union européenne (d. 22-23) — trois questions
**Q1 — Les médianes.** **UE à 15** (15 pays, impair, rang 8) : **113** hab/km², le Portugal.
**10 nouveaux pays** (pair, moyenne des rangs 5 et 6 — Slovénie 99 et Hongrie 109) : **104**.
**UE à 25** (25 pays, rang 13) : **109**, la Hongrie.

**Q2 — Les moyennes.** UE15 : **153,0** · 10 nouveaux : **203,0** · UE25 : **173,0** hab/km².
⚠ **Compare : la moyenne des 10 nouveaux pays (203,0) dépasse celle de l'UE15 (153,0), alors que
leur médiane est plus basse (104 contre 113).** C'est Malte, à 1 246 hab/km², qui tire la moyenne
— illustration directe de la propriété ③.

**Q3 — Si la densité de Malte est divisée par 2 ?**
**Les médianes sont inchangées** — Malte reste la valeur la plus haute, son **rang** ne change
pas. **Les moyennes chutent** : **− 31 %** pour les 10 nouveaux pays, **− 14 %** pour l'UE25.
**C'est la démonstration en une ligne de la différence entre rang et valeur.**
:::

::: correction Les revenus médians par CSP (d. 24) — la question qui compte
| Catégorie socioprofessionnelle | Revenu salarial médian annuel |
|---|---:|
| Cadres | 45 552 € |
| Professions intermédiaires | 29 640 € |
| Ouvriers | 23 148 € |
| Employés | 22 572 € |

**« Si je dispose de la part des CSP, puis-je calculer le salaire médian de l'ensemble ? »
NON — et jamais, quels que soient les poids.**

**Contre-exemple, à savoir produire en trois lignes :**
$ A = \{1;2;3\} $ donne $ Me_A = 2 $ ; $ B = \{100;200;300\} $ donne $ Me_B = 200 $.
Moyenne des médianes $ = \mathbf{101} $.
Vraie médiane de $ A \cup B = \{1;2;3;100;200;300\} $ : $ (3+100)/2 = \mathbf{51{,}5} $.
**Écart d'un facteur 2.**

**La raison :** la médiane dépend de **la position relative de toutes les valeurs** — information
détruite par le résumé en médianes de groupe. **Ce qui repose sur des rangs ne s'agrège pas.**
:::

::: correction Les familles selon le nombre d'enfants (d. 26) — deux questions, et un résultat aberrant
| Modalités | Effectifs (milliers) 2008 | 2023 |
|---|---:|---:|
| 0 enfant | 8 225 | 9 340 |
| 1 enfant | 3 821 | 4 085 |
| 2 enfants | 3 449 | 3 594 |
| 3 enfants | 1 241 | 1 219 |
| 4 enfants | 396 | 442 |
| **Ensemble** | **17 132** | **18 680** |

**Q1 — Éléments :** population = les **familles** en France ; unité = **une famille** ; variable
= nombre d'enfants, **quantitative discrète**.
*(Ce tableau est exactement celui du chapitre 1, diapositive 22 — le chapitre 2 le **date**
explicitement de 2008, ce qui confirme la déduction faite alors.)*

**Q2 — Fréquences cumulées et médiane.**
**2023 :** $ F(0) = 9\,340/18\,680 = \mathbf{50{,}0\,\%} $ **exactement** → la médiane est
**0 enfant**.
**2008 :** $ F(0) = 8\,225/17\,132 = 48{,}0\,\% $ ; $ F(1) = 70{,}3\,\% $. La classe médiane est
donc « 1 enfant », et la **médiane vaut 1 enfant**.

::: piege
**L'interpolation linéaire donne ici 0,09 enfant — et ce résultat est aberrant.**
$$ 0 + \frac{(1-0)(0{,}50 - 0{,}480)}{0{,}703 - 0{,}480} = \frac{0{,}020}{0{,}223} = 0{,}09 $$
**Pourquoi c'est faux :** l'interpolation suppose une **répartition uniforme à l'intérieur de la
classe**, ce qui n'a aucun sens pour une variable **discrète** — il n'existe pas de famille à
0,09 enfant. **Sur une variable discrète, on applique la règle du rang, pas l'interpolation.**
**Retiens le réflexe : un résultat non interprétable signale une hypothèse mal placée.**
:::
:::

<!--saut-->

### 2.2 — Résumer la dispersion (diapositives 27 à 58)

#### 2.2.1 Pourquoi la position ne suffit pas, et l'étendue (d. 27-28)

::: definition Les quatre cas, et le premier indicateur
Le support ouvre sur **quatre séries de même moyenne** et de formes radicalement différentes.
**Une moyenne sans dispersion est une information incomplète.**

$$ \text{étendue} = x_{\max} - x_{\min} $$
**Faiblesse :** elle ne dépend que des **deux valeurs extrêmes** — donc totalement détruite par
une valeur aberrante, et muette sur la répartition entre les bornes. **Première approche, jamais
seule.**
:::

#### 2.2.2 Quantiles et écarts inter-quantiles (d. 29 à 33)

::: formule Définition, familles, écarts
**Le quantile d'ordre $ p $ est la valeur $ Q_p $ telle que $ F(Q_p) = p $ : c'est l'INVERSE de
la fonction de répartition**, $ Q_p = F^{-1}(p) $. Une proportion $ p $ de la population a une
valeur inférieure ou égale à $ Q_p $.

| Famille | Parts | Valeurs qui les délimitent |
|---|:---:|:---:|
| **Quartiles** $ Q_1, Q_2, Q_3 $ | 4 | **3** |
| **Déciles** $ D_1 $ à $ D_9 $ | 10 | **9** |
| **Centiles** $ C_1 $ à $ C_{99} $ | 100 | **99** |

**Règle : $ n $ parts se délimitent par $ n-1 $ valeurs.** Et $ Q_1 = D_{2{,}5} $ ·
$ Q_3 = D_{7{,}5} $ · $ Me = Q_2 = D_5 $.

**Les trois écarts inter-quantiles :**
| Écart | Ce qu'il décrit | Unité |
|---|---|---|
| $ Q_3 - Q_1 $ — **inter-quartile** | L'étalement des **50 % centraux** | Celle de $ X $ |
| $ D_9 - D_1 $ — **inter-décile** | L'étalement des **80 % centraux** | Celle de $ X $ |
| $ D_9 / D_1 $ — **rapport inter-décile** | Le même en **relatif** | **Sans unité** — comparable entre populations |
| $ C_{99} - C_1 $ — **inter-centile** | Les 98 % centraux | Celle de $ X $ |

⚠ **Écart inter-quartile** = un **nombre** ($ Q_3 - Q_1 $) ; **intervalle inter-quartile** = un
**intervalle** ($ [Q_1 ; Q_3] $). Ne pas confondre.

**Sur une distribution, le quantile s'obtient par interpolation linéaire**, exactement comme la
médiane : $ Q_p = b_{inf} + a \times \dfrac{p - F(b_{inf})}{F(b_{sup}) - F(b_{inf})} $.
:::

#### 2.2.3 Interpréter des quantiles, et le boxplot (d. 34 à 38)

::: correction Le niveau de vie (d. 34) et le boxplot (d. 36-37)
**Le rapport inter-décile : $ D_9/D_1 = \mathbf{3{,}48} $** — « les 10 % les plus aisés ont un
niveau de vie au moins **3,48 fois** supérieur à celui des 10 % les plus modestes ».

⚠ **L'information la plus riche est dans les écarts entre déciles successifs**, qui **croissent**
régulièrement : **3 730 → 2 860 → 9 800 → 12 640 €**. **Des écarts croissants prouvent
l'étalement à droite** de la distribution : le haut est bien plus étalé que le bas.

::: piege
**Incohérence du support (d. 35).** La diapositive s'intitule « **retraités, année 2008** »
alors que **le tableau affiché est celui des niveaux de vie de 2024** de la diapositive 34.
**Erreur de titre**, signalée.
:::

**Le *boxplot* :** boîte de $ Q_1 $ à $ Q_3 $ (les **50 % centraux**), **trait intérieur à la
médiane**, **moustaches** jusqu'aux extrêmes — ou aux déciles selon la convention, **qu'il faut
préciser**. On y lit d'un coup d'œil **le niveau** (position du trait), **la dispersion**
(largeur de la boîte) et **l'asymétrie** : *si le trait n'est pas au centre de la boîte, la
distribution est asymétrique.*
:::

::: correction Les quantiles par CSP (d. 38) — « dans quelle CSP les salaires sont-ils le plus dispersés ? »
| | Ensemble | Cadres | Prof. interm. | Employés | Ouvriers |
|---|---:|---:|---:|---:|---:|
| $ D_1 $ | 1 440 | 2 240 | 1 640 | 1 380 | 1 380 |
| $ Q_1 $ | 1 660 | 2 810 | 1 940 | 1 510 | 1 570 |
| $ D_5 $ | 2 090 | 3 620 | 2 360 | 1 730 | 1 830 |
| $ Q_3 $ | 2 880 | 4 930 | 2 890 | 2 060 | 2 200 |
| $ D_9 $ | 4 160 | 7 060 | 3 590 | 2 520 | 2 630 |
| **$ D_9 - D_1 $** | **2 720** | **4 820** | 1 950 | **1 140** | 1 250 |
| **$ D_9 / D_1 $** | 2,9 | **3,2** | 2,2 | **1,8** | 1,9 |

**Réponse : les cadres sont les plus dispersés** — en absolu (**4 820 €**) comme en relatif
(**3,2**) ; **les employés les moins dispersés** (**1 140 €** et **1,8**). *Les deux indicateurs
concordent ; s'ils divergeaient, il faudrait dire lequel répond à la question posée.*

::: piege
**Le fait remarquable, que le support ne commente pas :** l'écart inter-décile de l'**Ensemble**
(2 720 €) **dépasse celui de trois CSP sur quatre**. Comment un ensemble peut-il être plus
dispersé que la plupart de ses parties ?
**Parce qu'il contient la composante INTER** — l'écart entre un cadre médian à 3 620 € et un
employé médian à 1 730 €. **On mesure ici, sans la nommer, la décomposition intra/inter du
§ 2.2.9.**
:::
:::

<!--saut-->

#### 2.2.4 EAM, variance, écart-type (d. 39 à 43)

::: formule Les trois indicateurs d'écart à la moyenne
$$ EAM = \frac{1}{N}\sum_{i=1}^{N} \lvert x_i - m_X \rvert \qquad V(X) = \sigma^2 = \frac{1}{N}\sum_{i=1}^{N}(x_i - m_X)^2 \qquad \sigma = \sqrt{V(X)} $$

**Pourquoi la valeur absolue ou le carré ?** Parce que **la somme des écarts simples est nulle**
(propriété ① de la moyenne) : sans eux, l'indicateur vaudrait 0 pour toute distribution.
**Pourquoi la racine ?** Parce que la variance est en **unité au carré**, donc
**ininterprétable**. **L'écart-type est la réponse ; la variance est une étape.**
**Pourquoi le carré a gagné sur la valeur absolue ?** Parce qu'il est **dérivable partout** —
toute la statistique qui suit (moindres carrés, régression, R²) en dépend.
**Et toujours :** $ EAM \le \sigma $, le carré pénalisant davantage les grands écarts.
:::

::: correction La série des 20 âges (d. 42-43) — et l'omission du support
Le tableau de calcul du support donne, pour cette série :
$$ m = \mathbf{47{,}9} \text{ ans} \qquad EAM = \mathbf{5{,}7} \text{ ans} \qquad \sigma^2 = \mathbf{54{,}19} \text{ ans}^2 $$

::: piege
**⚠ Le support s'arrête à la variance. L'écart-type n'y figure jamais :**
$$ \sigma = \sqrt{54{,}19} = \mathbf{7{,}36} \text{ ans} $$
**C'est pourtant le seul chiffre interprétable.** « La variance vaut 54,19 ans² » ne dit rien à
personne ; « l'écart-type vaut 7,4 ans autour d'une moyenne de 47,9 ans » se lit immédiatement.
**Ne rends jamais une copie qui s'arrête à la variance.**

*Contrôle de cohérence : $ EAM = 5{,}7 \le \sigma = 7{,}36 $ ✔, rapport 1,29.*
:::
:::

#### 2.2.5 Interpréter l'écart-type : Bienaymé-Tchebychev (d. 44) et la finance (d. 45-48)

::: formule L'inégalité de Bienaymé-Tchebychev
$$ P\big(\lvert X - m \rvert \ge k\sigma\big) \le \frac{1}{k^2} \qquad \textbf{avec } k > 1 $$
**Au moins $ 1 - 1/k^2 $ des observations se situent dans $ [\,m - k\sigma \,;\, m + k\sigma\,] $.**

| $ k $ | Au moins… dans l'intervalle |
|:---:|:---:|
| 2 | **75 %** |
| 3 | **88,9 %** |
| 4 | **93,75 %** |

**Sa force et sa faiblesse sont la même chose : elle est valable QUELLE QUE SOIT LA LOI**, donc
**très lâche**. Sous hypothèse de normalité, $ \pm 2\sigma $ contiendrait environ 95 % des
observations, contre 75 % garantis ici.
⚠ **Elle ne dit RIEN pour $ k \le 1 $** : la borne vaudrait $ \ge 1 $, c'est-à-dire « au moins
0 % ».
:::

::: piege L'application en finance (d. 45-48) : les conclusions du support ne se reconstruisent pas
Le support conclut à « **99 % de chances de faire des gains en périodes 1, 2, 3 et 5** ».
**Cette conclusion n'est pas démontrable avec les outils du chapitre**, pour deux raisons :

**① Bienaymé-Tchebychev exige $ k > 1 $**, et dans **les cinq périodes** on a
$ m/\sigma < 1 $ : aucun $ k $ admissible ne permet d'encadrer le gain.
**② La période 2 a une moyenne négative** — on ne peut pas y conclure à un gain probable.

**Ce que tu dois faire :** **signaler**, ne pas recopier. Une copie qui affirme « 99 % de chances
de gains » **sans démonstration est indéfendable** ; une copie qui écrit « l'inégalité de
Bienaymé-Tchebychev exige $ k > 1 $, condition non satisfaite ici, la conclusion ne peut donc
être établie par cette voie » **vaut des points**. ➔ intégrale § 2.2.13 pour le détail par
période.

**Ce qui reste vrai et exigible :** **l'écart-type devient la volatilité**, et elle s'annualise
en **multipliant par $ \sqrt{252} $** (rendements quotidiens) ou **$ \sqrt{12} $** (mensuels) —
jamais par 252 ni par 12, **puisque ce sont les variances qui s'additionnent**. *Et une série de
$ n $ prix ne donne que $ n-1 $ rentabilités.*
:::

#### 2.2.6 Koenig et les propriétés de la variance (d. 49 à 52)

::: formule Le problème, et sa solution
**Le problème (d. 49) :** la moyenne se calcule par groupe — elle est linéaire. **L'écart-type,
non.** On ne peut donc pas calculer facilement la volatilité annuelle à partir des volatilités
mensuelles… « mais il y a un moyen ».

**① Formule de Koenig** — « la moyenne des carrés moins le carré de la moyenne » :
$$ V(X) = \frac{1}{N}\sum_{i=1}^{N} x_i^2 - m_X^2 $$
**Pourquoi elle est utile :** la formule de définition exige de connaître $ m_X $ **avant** de
calculer les écarts — **deux passages** sur les données. Koenig ne demande que **deux sommes**,
$ \sum x_i $ et $ \sum x_i^2 $, calculables **en un seul passage**. **C'est ce qui rend
l'agrégation possible : deux nombres suffisent à transmettre un groupe.**
⚠ **Contrôle instantané :** la variance étant positive, $ \overline{x^2} \ge (\overline{x})^2 $.
**Une variance négative signale une inversion.**

**② Invariance par translation :** $ V(X + a) = V(X) $.
*Si $ Y = X+a $ alors $ m_Y = m_X + a $, donc $ y_i - m_Y = x_i - m_X $ : les écarts sont
inchangés.* **Ajouter 6 points à toutes les notes déplace la distribution sans la déformer.**

**③ Non-linéarité :** $ V(aX) = a^2 V(X) $, donc $ \sigma_{aX} = \lvert a \rvert\,\sigma_X $.
*Si $ Y = aX $ alors $ y_i - m_Y = a(x_i - m_X) $, et au carré $ a^2 (x_i - m_X)^2 $.*
⚠ **L'erreur classique : écrire $ V(aX) = a\,V(X) $.** Retiens :
**$ a $ ajouté ne change rien, $ a $ multiplié change au carré.**

**④ Corollaire :** $ V(-X) = V(X) $, avec $ a = -1 $.
:::

#### 2.2.7 Le coefficient de variation (d. 53)

::: formule Un indicateur relatif, sans unité
$$ CV = \frac{\sigma}{m_X} $$
**Indispensable dès qu'on compare des séries d'unités ou d'ordres de grandeur différents.** Un
écart-type de 500 € ne signifie pas la même chose autour d'une moyenne de 1 000 € ($ CV = 0{,}5 $)
et de 100 000 € ($ CV = 0{,}005 $).
**En finance : $ CV $ est l'inverse du rapport $ m/\sigma $, c'est-à-dire du ratio de Sharpe
sans taux sans risque.**
:::

#### 2.2.8 La variance sur une distribution, et le choix de la formule (d. 54 à 56)

::: formule La formule, et l'anomalie du support
$$ V(X) = \sum_{i=1}^{p} f_i (x_i - m_X)^2 = \frac{1}{N}\sum_{i=1}^{p} n_i (x_i - m_X)^2 $$
**Chaque écart au carré est pondéré par l'effectif de sa modalité** — l'oubli de la pondération
est l'erreur numéro un sur ce calcul.

::: piege
**⚠ ANOMALIE : le résultat du cas n° 4 (d. 55) est erroné.**
Le support annonce une variance de **10,4** et un écart-type de **3,2**.
**Le recalcul donne $ \sigma^2 = \mathbf{20{,}8} $ et $ \sigma = \sqrt{20{,}8} = \mathbf{4{,}56} $**
— **exactement le double** : une division par 2 en trop.
**Conséquence : le classement des cas 2 et 4 par dispersion est inversé.**
➔ intégrale § 2.2.16 pour la vérification complète, ligne par ligne.

**Formulation qui rapporte en examen :** « En appliquant $ V = \frac{1}{N}\sum n_i(x_i-m)^2 $
j'obtiens 20,8 et non 10,4. L'écart d'un facteur 2 suggère une division supplémentaire par 2. Je
retiens 20,8, soit $ \sigma = 4{,}56 $, ce qui modifie le classement des cas 2 et 4. »
:::

**L'arbre du choix de la formule (d. 56) :**
**Données brutes ?** → définition, ou **Koenig** si tu dois agréger ensuite.
**Distribution ?** → $ \sum f_i (x_i - m)^2 $, ou Koenig : $ \sum f_i x_i^2 - m^2 $.
**Plusieurs groupes ?** → **agrégation par Koenig**, ou **décomposition intra/inter**.
:::

#### 2.2.9 Agrégation et décomposition intra / inter (d. 57-58)

::: formule Le corollaire le plus important du chapitre
$$ \sigma^2 = V_{\text{intra}} + V_{\text{inter}} $$
$$ V_{\text{intra}} = \sum_{k=1}^{K} \frac{N_k}{N}\,\sigma_k^2 \qquad V_{\text{inter}} = \sum_{k=1}^{K} \frac{N_k}{N}\,(m_{X_k} - m_X)^2 $$

| Composante | Ce qu'elle mesure | Question |
|---|---|---|
| $ V_{\text{intra}} $ | La dispersion **moyenne à l'intérieur** des groupes | « Les membres d'un même groupe se ressemblent-ils ? » |
| $ V_{\text{inter}} $ | La dispersion **des moyennes** de groupe | « Les groupes diffèrent-ils entre eux ? » |

**Deux cas extrêmes :** $ V_{\text{inter}} \approx 0 $ → les groupes ont la même moyenne, **le
découpage n'explique rien** ; $ V_{\text{intra}} \approx 0 $ → chaque groupe est homogène, **le
découpage explique tout**.

**Le rapport $ V_{\text{inter}}/\sigma^2 $ mesure le POUVOIR EXPLICATIF du découpage.** C'est lui
qui deviendra, au chapitre 4 puis en économétrie, le **rapport de corrélation** puis le **R²**.

::: marche
**En gestion de portefeuille, c'est la décomposition du risque :** risque **spécifique**
(intra — ce qui bouge à l'intérieur de chaque secteur) et risque **systématique** (inter — ce qui
fait bouger les secteurs entre eux). **La diversification agit sur le premier, jamais sur le
second.** Même algèbre, autre objet.
:::
:::

<!--saut-->

### 2.3 — Résumer la concentration (diapositives 59 à 69)

#### 2.3.1 Concentration et dispersion : deux questions différentes (d. 59)

::: definition La distinction, et la condition d'existence
| | **Dispersion** | **Concentration** |
|---|---|---|
| Objet du raisonnement | Les **valeurs** $ x_i $ | Les **parts** $ x_i / \sum x_j $ |
| Question | Les individus se ressemblent-ils ? | Le total est-il concentré sur quelques-uns ? |
| Référence | La **moyenne** | L'**agrégat** $ \sum x_i $ |
| Condition d'application | Variable quantitative | Variable quantitative **dont la somme fait sens** |

**Point commun : les deux mesurent des inégalités.** Ce sont deux angles sur le même phénomène.

::: piege
**La condition d'existence, que le support signale en une ligne et qu'il faut prendre au
sérieux :** « si la somme des revenus fait sens, ce n'est pas le cas de tous les caractères
statistiques quantitatifs (**exemple : la taille**) ! »

| Variable | Sa somme est… | Concentration ? |
|---|---|:---:|
| Salaire | La **masse salariale** | **Oui** |
| Patrimoine · chiffre d'affaires · émissions de CO₂ | Un stock ou un flux réel | **Oui** |
| **Taille · note · température · âge** | **Rien** | **Non** |

**La règle : la concentration exige une variable EXTENSIVE et ADDITIVE.** Un Gini sur des notes
se calcule numériquement mais **ne s'interprète pas** — et l'absence de vérification préalable
est sanctionnée.
:::
:::

#### 2.3.2 La part de l'agrégat (d. 60)

::: formule La relation fondatrice, et la simplification de N
**L'agrégat** = la somme de $ X $ sur la population. Pour les salaires : la **masse salariale**.

$$ \sum_{i=1}^{N_k} x_i = N_k \, m_{X_k} $$
*Démonstration en une ligne : c'est la définition de la moyenne multipliée par $ N_k $.*
**« La somme = la moyenne × l'effectif »** — c'est ce qui transforme une information *moyenne*
(toujours publiée) en information *totale* (rarement publiée).

**La part de l'agrégat de la classe $ k $ :**
$$ p_k = \frac{N_k m_{X_k}}{\sum_j N_j m_{X_j}} = \frac{f_k m_{X_k}}{\sum_j f_j m_{X_j}} = \frac{f_k\, m_{X_k}}{m_X} = f_k \times \frac{m_{X_k}}{m_X} $$

**Pourquoi l'effectif total disparaît :** $ N_k = f_k N $, et le facteur $ N $ est **commun au
numérateur et au dénominateur**. **Poser $ N = 1 $ n'est donc pas une approximation mais une
simplification exacte** — le support le suggère sans le démontrer.
**Et la troisième écriture est la plus parlante :** la part d'une classe est **sa fréquence
multipliée par son avantage relatif de moyenne**. Une classe de 20 % des salariés dont le salaire
moyen vaut 2 fois la moyenne détient $ 0{,}20 \times 2 = 40\,\% $ de la masse.

**Contrôle obligatoire : la somme des parts doit valoir 100 %.**
:::

#### 2.3.3 Les salaires en 2005 et 2021 (d. 61 à 63)

::: correction Les deux tableaux, recalculés
**2005** — classes de salaires (quintiles, donc $ f_k = 0{,}20 $ pour tous) :

| Proportion (%) | Borne inf. | Borne sup. | Salaire moyen | Part de la masse (%) |
|---:|---:|---:|---:|---:|
| 20 | 11 000 | 12 894 | 11 947 | **11,2** |
| 20 | 12 894 | 15 555 | 14 225 | **13,3** |
| 20 | 15 555 | 19 098 | 17 327 | **16,2** |
| 20 | 19 098 | 25 818 | 22 458 | **21,1** |
| 20 | 25 818 | 55 600 | 40 709 | **38,2** |
| **Ensemble** | | | **21 333** | **100,0** |

**La moyenne générale.** Les classes ayant le **même poids**, elle est la moyenne **simple** des
cinq moyennes : $ \sum m_k = 106\,666 $, donc $ m_X = 0{,}20 \times 106\,666 = \mathbf{21\,333{,}2} $ € ✔
⚠ **Ce n'est vrai QUE parce que les classes sont des quintiles.** Avec des fréquences inégales,
il faudrait pondérer.
**Les parts.** Les $ f_k $ se simplifiant aussi : $ p_k = m_{X_k}/106\,666 $ → **11,20 · 13,34 ·
16,24 · 21,05 · 38,17 %**, total **100,00 %** ✔

::: piege
**La colonne « estimation du salaire moyen » n'est jamais expliquée par le support : c'est le
CENTRE DE CLASSE.** Vérification : $ (11\,000+12\,894)/2 = 11\,947 $ ✔, et ainsi des cinq.
**Le support applique donc l'hypothèse de répartition uniforme dans les classes — il fallait le
dire, et tu dois le dire.**
**Et il faut en mesurer la fragilité :** les quatre premières classes sont étroites (1 894 à
6 720 €) ; **la cinquième est large de 29 782 €**. Or les hauts salaires sont **massés près de
la borne inférieure** : la vraie moyenne de cette classe est **vraisemblablement inférieure** à
40 709 €, donc **la part de 38,2 % surestime probablement la concentration**. *Je dis
« vraisemblablement » : sans les données individuelles, l'écart n'est pas quantifiable.*
**Signaler cette limite est ce qui distingue une copie excellente.**
:::

**2021** — mêmes classes, autre millésime :

| Proportion (%) | Borne inf. | Borne sup. | Salaire moyen | Part (%) |
|---:|---:|---:|---:|---:|
| 20 | 1 333 | 6 709 | 4 021 | **3,9** |
| 20 | 6 709 | 15 110 | 10 910 | **10,6** |
| 20 | 15 110 | 22 942 | 19 026 | **18,4** |
| 20 | 22 942 | 32 124 | 27 533 | **26,7** |
| 20 | 32 124 | 51 490 | 41 807 | **40,5** |
| **Ensemble** | | | **20 659** | **100** |

$ \sum m_k = 103\,297 $, donc $ m_X = \mathbf{20\,659{,}4} $ € ✔ ; parts exactes **3,89 · 10,56 ·
18,42 · 26,65 · 40,47 %**.
⚠ **Détail d'arrondi que le support ne signale pas :**
$ 3{,}9 + 10{,}6 + 18{,}4 + 26{,}7 + 40{,}5 = \mathbf{100{,}1} $, et non 100,0. Les cinq valeurs
ont été arrondies **vers le haut**. **Cet excédent se propage au tableau des cumuls et décale le
Gini d'environ 0,0006.** Négligeable, à mentionner.
:::

::: correction La comparaison 2005 / 2021 (d. 63) — la question posée, sans réponse dans le support
| Quintile | 2005 | 2021 | Variation | En relatif |
|---|---:|---:|---:|---|
| 1ᵉʳ (les moins payés) | 11,2 | 3,9 | **− 7,3** | **− 65 %** — la part est **divisée par 2,9** |
| 2ᵉ | 13,3 | 10,6 | − 2,7 | − 20 % |
| 3ᵉ | 16,2 | 18,4 | + 2,2 | + 14 % |
| 4ᵉ | 21,1 | 26,7 | **+ 5,6** | **+ 27 %** |
| 5ᵉ (les mieux payés) | 38,2 | 40,5 | + 2,3 | + 6 % |

**① Le sens est sans ambiguïté : les inégalités ont augmenté.** Les deux quintiles du bas
perdent, les trois du haut gagnent — **10 points de masse salariale ont changé de mains**.
*Contrôle mécanique : la somme des variations doit être nulle, et elle l'est à 0,1 près.*
**② Le fait marquant n'est pas l'envol du haut (+ 6 % seulement) mais l'effondrement du bas.**
**③ Le rapport entre extrêmes :** $ 38{,}2/11{,}2 = \mathbf{3{,}41} $ en 2005 contre
$ 40{,}5/3{,}9 = \mathbf{10{,}38} $ en 2021 — **multiplié par 3**.

::: piege
**La prudence méthodologique obligatoire — et une limite que je ne peux pas lever.**
Le plancher passe de **11 000 à 1 333 €** (÷ 8), le plafond **baisse** (55 600 → 51 490) et le
salaire moyen **baisse en euros courants** (21 333 → 20 659) alors que les salaires nominaux ont
augmenté sur la période. **Ces trois faits ne sont pas compatibles avec deux mesures du même
champ.**
**L'explication la plus probable : un changement de champ statistique** — 2005 sur des postes en
équivalent temps plein, 2021 sur l'ensemble des postes, temps partiels et années incomplètes
compris. **Je ne peux pas le vérifier :** le support n'indique ni source, ni champ, ni définition.
**À écrire en examen :** « La hausse de concentration est nette, mais la baisse simultanée du
plancher, du plafond et du salaire moyen en euros courants suggère un changement de champ entre
les deux millésimes ; une partie de l'écart pourrait être un artefact de mesure. »
*Même réflexe qu'en finance : avant de comparer deux performances, on vérifie le périmètre, la
devise et le traitement des dividendes.*
:::
:::

<!--saut-->

#### 2.3.4 La courbe de Lorenz (d. 64 à 67)

::: definition Définition, construction, propriétés
**En abscisse la fréquence cumulée de la POPULATION ; en ordonnée la part cumulée de l'AGRÉGAT**,
les individus étant **rangés par valeur croissante de $ X $**.
⚠ **Le classement croissant est une condition, pas un détail** : sans lui la courbe n'est ni
convexe, ni sous la diagonale, et le Gini n'a plus de sens. Le support ne le précise pas.

**Phrase-type de lecture :** « les **…** % des salariés les moins payés perçoivent **…** % de la
masse salariale ».

**Le tableau des cumuls (d. 65) :**

| Part cumulée des salariés (%) | Masse cumulée 2005 (%) | Masse cumulée 2021 (%) |
|---:|---:|---:|
| 20 | **11,2** | **3,9** |
| 40 | **24,5** | **14,5** |
| 60 | **40,7** | **32,9** |
| 80 | **61,8** | **59,6** |
| 100 | 100,0 | 100,0 |

⚠ **Le support cumule des valeurs ARRONDIES.** En 2005, le cumul exact à 60 % vaut 40,78 → 40,8,
mais $ 11{,}2+13{,}3+16{,}2 = 40{,}7 $. En 2021, le dernier cumul donne 100,1, forcé à 100,0.
**Cumuler des arrondis n'est pas arrondir des cumuls — écris toujours ce que tu fais.**

**LES QUATRE PROPRIÉTÉS, toutes démontrables :**
**①** Elle passe par **(0 ; 0) et (100 ; 100)** — *deux points imposés : si ta courbe ne les
traverse pas, tu as une erreur de cumul.*
**②** Elle est **croissante** — *on cumule des parts positives.*
**③ Sa PENTE sur la classe $ k $ vaut $ m_{X_k}/m_X $** — le résultat le plus utile, et le
support ne l'énonce pas :
$$ \text{pente} = \frac{\Delta L}{\Delta F} = \frac{p_k}{f_k} = \frac{f_k m_{X_k}/m_X}{f_k} = \frac{m_{X_k}}{m_X} $$
**Pente < 1** → la classe gagne moins que la moyenne, la courbe s'écarte de la diagonale.
**Pente = 1** → elle gagne exactement la moyenne : **c'est le point où l'écart à la diagonale est
maximal**. **Pente > 1** → la courbe revient vers la diagonale.
*Vérification 2005 : pentes 0,56 · 0,67 · 0,81 · 1,05 · 1,91 — la pente franchit 1 entre le 3ᵉ et
le 4ᵉ quintile, et c'est bien là que l'écart est maximal (19,3 points à $ F = 60 $).* ✔
**④** Elle est **convexe** — *les pentes croissent, les classes étant ordonnées* — **donc située
sous la diagonale**, qui relie ses deux extrémités.
**Cas limite :** si tout le monde gagne la même chose, toutes les pentes valent 1 : **la courbe
EST la diagonale. La diagonale est la courbe de Lorenz de l'égalité parfaite.**
:::

**Le graphe (d. 66).** Le support affiche les deux courbes **sans la diagonale** — or c'est
l'écart à la diagonale qui porte toute l'information. **Le voici reconstruit, diagonale
comprise.**

```
100%|                                                           .*
    |                                                          .*
    |                                                        ..*
    |                                                      .. *
    |                                                   ...  *
    |                                                 ..    *
 80%|                                               ..     *
    |                                              .      *
    |                                           ...      *
    |                                          .        *
    |                                       ...        *
    |                                      .         O*
 60%|                                   ...         o#
    |                                  .          o**
    |                               ...         oo*
    |                              .          oo**
    |                           ...         oo *
    |                         ..          oo **
 40%|                       ..          oO  *
    |                      .         ooo  **
    |                   ...        oo    #
    |                  .        ooo    **
    |               ...       oo    ***
    |              .       ooO    **
 20%|           ...     ooo     **
    |          .     ooo      **
    |        ..   ooo     ***#
    |      .. oooO     ***
    |   ...ooo     ****
    |  oooo******#*
  0%|******
    +-------------------------------------------------------------
    0%          20%         40%         60%         80%        100%

  . . .  diagonale d'égalité parfaite (L(F) = F)
  o o o  courbe de Lorenz 2005   —  O = points calculés (20/40/60/80 %)
  * * *  courbe de Lorenz 2021   —  # = points calculés (20/40/60/80 %)
```

::: definition Interpréter, et comparer deux courbes (d. 67)
**① Plus la courbe s'éloigne de la diagonale, plus la concentration est forte.**
**② DOMINANCE DE LORENZ.** Si une courbe est **partout** plus éloignée, l'inégalité est accrue
**pour tous les ordres de quantiles** : **tous les indicateurs convergent**, aucun choix
d'indicateur ne peut inverser la conclusion.
**③ SI LES COURBES SE CROISENT**, l'une est plus inégalitaire **en bas**, l'autre **en haut** :
**des indicateurs différents peuvent donner des conclusions opposées.**

**Contre-exemple chiffré, à savoir produire.** Deux pays, parts par quintile :

| Quintile | Pays A | Pays B | Cumul A | Cumul B |
|---|---:|---:|---:|---:|
| 1ᵉʳ | 4 | 8 | 4 | 8 |
| 2ᵉ | 12 | 10 | 16 | 18 |
| 3ᵉ | 20 | 15 | 36 | 33 |
| 4ᵉ | 28 | 22 | 64 | 55 |
| 5ᵉ | 36 | 45 | 100 | 100 |

Les cumuls **se croisent** entre 40 % et 60 %. Alors : **rapport $ Q_5/Q_1 $** → A = 9,0, B = 5,6,
**A plus inégalitaire** ; **part du quintile supérieur** → A = 36 %, B = 45 %, **B plus
inégalitaire**. **Deux indicateurs, deux réponses opposées, mêmes données.**

**APPLICATION À 2005 / 2021 : y a-t-il croisement ?**

| $ F $ | 2005 | 2021 | Différence |
|---:|---:|---:|---:|
| 20 % | 11,2 | 3,9 | − 7,3 |
| 40 % | 24,5 | 14,5 | **− 10,0** |
| 60 % | 40,7 | 32,9 | − 7,8 |
| 80 % | 61,8 | 59,6 | − 2,2 |

**La différence est négative partout : la courbe 2021 est partout sous celle de 2005. Pas de
croisement — il y a dominance de Lorenz, et la conclusion est robuste.**
⚠ **Note où l'écart est maximal : à 40 % (− 10,0 points).** **L'aggravation se joue dans la
première moitié**, pas dans le haut — cohérent avec l'effondrement du premier quintile.
:::

#### 2.3.5 L'indice de Gini (d. 68-69)

::: formule Définition, construction, et LE piège du chapitre
**Géométriquement, le Gini est le DOUBLE de l'aire comprise entre la diagonale et la courbe**
(l'« aire de concentration ») :
$$ G = 2 \times \mathcal{A} \qquad\text{avec}\qquad G = 2\left[\frac{1}{2} - \sum \frac{(b+B)\cdot h}{2}\right] $$

**D'où vient la formule — quatre étapes :** ① le carré unité a une aire de **1** ; ② la diagonale
le coupe en deux, l'aire sous elle vaut **1/2** ; ③ l'aire de concentration s'obtient en
retirant l'aire **sous la courbe** : $ \mathcal{A} = \frac{1}{2} - \mathcal{B} $ ; ④ entre deux
points la courbe est un **segment**, donc l'aire sous elle se découpe en **trapèzes**, d'aire
$ \frac{(b+B)h}{2} $ — $ b $ petite base, $ B $ grande base, $ h $ largeur de tranche.

::: piege
**LE piège de calcul du chapitre : l'unité des aires.**
Le support affiche sur le graphe un trapèze d'aire **1 025** (avec $ b = 40{,}7 $, $ B = 61{,}8 $,
$ h = 20 $) puis écrit $ \mathcal{A} = 0{,}5 - \text{aire des trapèzes} $. **Ces deux nombres ne
sont pas dans la même unité.**
Le 1 025 est calculé sur des **axes gradués en pourcentages** : dans cette unité **le carré vaut
$ 100 \times 100 = 10\,000 $**. Le 0,5 est en **fractions**, unité où le carré vaut 1.
$$ \boxed{\;\mathcal{A} = \frac{1}{2} - \frac{\sum (b+B)h/2}{10\,000}\quad\text{si les cumuls sont en \%}\;}$$
**Contrôle systématique : $ \mathcal{A} \in [0 ; 0{,}5] $ et $ G \in [0 ; 1] $.** Si tu obtiens
$ 0{,}5 - 3\,764 $, tu as oublié la conversion.
:::
:::

::: correction Le calcul complet, les deux années
**Astuce :** $ h = 20 $ pour toutes les tranches, donc aire $ = (b+B) \times 10 $.

| Tranche | 2005 : $ b $ → $ B $ | Aire | 2021 : $ b $ → $ B $ | Aire |
|---|---|---:|---|---:|
| 0 → 20 | 0 → 11,2 | **112,0** | 0 → 3,9 | **39,0** |
| 20 → 40 | 11,2 → 24,5 | **357,0** | 3,9 → 14,5 | **184,0** |
| 40 → 60 | 24,5 → 40,7 | **652,0** | 14,5 → 32,9 | **474,0** |
| 60 → 80 | 40,7 → 61,8 | **1 025,0** | 32,9 → 59,6 | **925,0** |
| 80 → 100 | 61,8 → 100,0 | **1 618,0** | 59,6 → 100,0 | **1 596,0** |
| **Somme** | | **3 764,0** | | **3 218,0** |

*Le trapèze 60 → 80 % vaut 1 025 — exactement la valeur affichée par le support ✔ : la méthode
est validée.*

$$ \mathcal{A}_{2005} = 0{,}5 - 0{,}3764 = 0{,}1236 \;\Rightarrow\; G_{2005} = \mathbf{0{,}2472} $$
$$ \mathcal{A}_{2021} = 0{,}5 - 0{,}3218 = 0{,}1782 \;\Rightarrow\; G_{2021} = \mathbf{0{,}3564} $$

**Les trois phrases à écrire :** ① « L'indice de Gini passe de **0,247 en 2005 à 0,356 en
2021**, soit **+ 11 points** ou **+ 44 % en relatif**. » ② « La concentration de la masse
salariale s'est donc **fortement accrue**. » ③ « Ce diagnostic est **cohérent avec la courbe de
Lorenz**, partout plus éloignée de la diagonale en 2021 : **dominance**, donc **aucun risque de
contradiction entre indicateurs**. » **Et la réserve sur le changement de champ reste entière.**

*Avec les parts non arrondies on obtiendrait 0,2466 et 0,3570 — l'écart d'arrondi n'affecte que
la troisième décimale et ne change aucune conclusion.*
:::

::: definition Les bornes, et comment interpréter un Gini
**$ G = 0 $ ⇔ égalité parfaite.** *Cumuls 20/40/60/80/100 → trapèzes 200+600+1 000+1 400+1 800
= 5 000 → $ \mathcal{A} = 0{,}5 - 0{,}5 = 0 $* ✔ **La courbe est la diagonale.**
**$ G \to 1 $ ⇔ concentration totale** — un seul individu détient tout.
⚠ *Précision d'excellente copie : avec $ N $ individus, le maximum vaut $ \frac{N-1}{N} $, non 1
— le dernier individu occupe une largeur $ 1/N $ sous laquelle subsiste un triangle d'aire
$ \frac{1}{2N} $.*

**Ordres de grandeur, pour le revenu disponible des ménages** — repères, pas chiffres exacts :
nordiques 0,25-0,28 · **France, Allemagne 0,29-0,32** · Royaume-Uni, Italie 0,33-0,36 ·
États-Unis 0,38-0,41 · Brésil 0,48-0,54 · Afrique du Sud ≈ 0,63.

::: piege
**Trois précautions avant toute comparaison de Gini.**
**① Le concept mesuré change tout** — le Gini du **patrimoine** (> 0,6 en France) est bien
supérieur à celui du **revenu** (≈ 0,3) : le patrimoine peut être nul ou négatif.
**② Avant ou après redistribution ?** L'écart entre le Gini des revenus **primaires** et celui du
revenu **disponible** mesure l'effet du système socio-fiscal.
**③ Le Gini est peu sensible aux extrêmes** : il réagit surtout aux transferts autour du
**milieu**. Un Gini stable peut masquer un décrochage du dernier centile — d'où
l'accompagnement systématique par le **rapport $ D_9/D_1 $** et la **part du 1 % le plus riche**.
**⚠ Nos deux valeurs portent sur les SALAIRES, pas sur le revenu disponible : elles ne sont pas
comparables aux repères ci-dessus.**
:::

::: marche
**La concentration en salle de marché.** Trie tes positions par poids croissant et cumule : tu
obtiens la courbe de Lorenz de ton exposition. L'indicateur du métier est l'**indice de
Herfindahl-Hirschman** $ HHI = \sum_i w_i^2 $ — $ 1/n $ pour $ n $ lignes équipondérées, et il
tend vers 1 quand tout est sur une ligne. **Un mandat de gestion impose presque toujours un
plafond de HHI ou un poids maximal par ligne.**
**Et sur le P&L :** presque tous les *track records* montrent qu'**une minorité de trades fait la
totalité du résultat** — ce n'est pas anormal, c'est la signature d'une asymétrie droite. **Ce
qui est dangereux, c'est l'inverse** : une concentration venant de quelques **pertes** énormes
compensées par beaucoup de petits gains. **La courbe de Lorenz de ton P&L distingue les deux en
un coup d'œil ; la moyenne, non.**
:::
:::

<!--saut-->

### 2.4 — Récapitulons (diapositive 70)

::: synthese Les treize indicateurs du chapitre, en un tableau
| Famille | Indicateur | Formule | Unité | Sensible aux extrêmes ? | Quand le choisir |
|---|---|---|---|:---:|---|
| **Position** | Mode | Fréquence max (ou **densité** max si classes inégales) | Celle de $ X $ | Non | Seul indicateur valable sur une variable **qualitative** |
| | Moyenne | $ \frac{1}{N}\sum x_i $ | Celle de $ X $ | **Oui** | Distribution symétrique ; calculs ultérieurs (linéarité, agrégation) |
| | Médiane | $ F(\text{Me}) = 0{,}5 $ | Celle de $ X $ | **Non** | Distribution asymétrique ; valeurs extrêmes |
| **Dispersion** | Étendue | $ x_{\max}-x_{\min} $ | Celle de $ X $ | **Totalement** | Première approche, jamais seule |
| | Écart inter-quartile | $ Q_3-Q_1 $ | Celle de $ X $ | Non | Accompagne la médiane ; base du *boxplot* |
| | Écart inter-décile | $ D_9-D_1 $ · $ D_9/D_1 $ | Celle de $ X $ · **sans unité** | Peu | Comparaisons de niveaux de vie |
| | EAM | $ \frac{1}{N}\sum \|x_i-m_X\| $ | Celle de $ X $ | Oui | Lisible, mais **non dérivable** |
| | Variance | $ \frac{1}{N}\sum (x_i-m_X)^2 $ | **Au carré** | **Très** | **Étape de calcul**, décompositions |
| | Écart-type | $ \sigma=\sqrt{V} $ | Celle de $ X $ | **Très** | **L'indicateur de référence** — volatilité en finance |
| | Coefficient de variation | $ CV=\sigma/m_X $ | **Sans unité** | Oui | Comparer des séries d'unités ou d'échelles différentes |
| **Concentration** | Part de l'agrégat | $ p_k=f_k m_{X_k}/m_X $ | Sans unité | — | Première lecture des inégalités |
| | Courbe de Lorenz | $ L(F) $ = part cumulée | Sans unité | — | Comparer deux distributions (dominance) |
| | Indice de Gini | $ 2\left[\frac12-\sum\frac{(b+B)h}{2}\right] $ | **Sans unité, [0;1]** | Peu (milieu) | Résumer, classer, suivre une évolution |
:::

::: methode L'arbre de décision : quel indicateur, quand ?
**Q1 — Type de variable ?** **Qualitative** → **mode uniquement**. **Ordinale** → mode et
médiane, **pas de moyenne**. **Cardinale** → tout est permis, va en Q2.
**Q2 — Que veux-tu décrire ?** Le **niveau typique** → position (Q3). L'**homogénéité** →
dispersion (Q4). Le **partage d'un total** → concentration, **après avoir vérifié que la somme
fait sens**.
**Q3 — La distribution est-elle symétrique ?** **Oui** → moyenne. **Non, ou valeurs extrêmes** →
**médiane**, en donnant aussi la moyenne : **l'écart entre les deux est le diagnostic
d'asymétrie**.
**Q4 — Mêmes unités et mêmes ordres de grandeur ?** **Oui** → écart-type. **Non** → **coefficient
de variation**. **Résister aux extrêmes** → écarts inter-quantiles et *boxplot*.
**Q5 — Faut-il agréger ?** Moyenne → pondérée. Variance → **Koenig** ou intra/inter. **Médiane,
quantiles et Gini : JAMAIS.**

::: piege
**La phrase du support qu'on lit trop vite :** « le choix d'indicateurs dépend du type de données
**mais aussi de ce que l'on veut en faire** ». **La seconde moitié est la plus importante.** Le
type de données **élimine** ; l'objectif **tranche** entre ceux qui restent.
*Mêmes données, trois objectifs, trois indicateurs :* décrire le salaire typique d'une profession
→ **médiane** ; calculer la masse salariale à provisionner → **moyenne** (seule à s'agréger) ;
vérifier qu'aucun salarié n'est décroché → **écarts inter-déciles**.
**Un correcteur attend que tu justifies ton choix — pas que tu calcules tout.**
:::
:::
<!--saut-->

## 3. Points de vigilance

### 3.1 — Les confusions classiques

Vingt couples de notions voisines. Pour chacun, **le critère qui tranche**.

| Notion A | Notion B | Le critère qui les sépare |
|---|---|---|
| **Présenter** (chapitre 1) | **Résumer** (chapitre 2) | Présenter **conserve toute** l'information ; résumer en **perd volontairement** pour produire un petit nombre de chiffres |
| **Mode** | **Classe modale** | Le mode est une **valeur** (variable discrète) ; la classe modale est un **intervalle** (variable continue). On ne dit jamais « le mode est [20 ; 30[ » |
| **Effectif le plus élevé** | **Densité la plus élevée** | Quand les classes ont des **amplitudes inégales**, la classe modale est celle de **densité maximale**, pas d'effectif maximal |
| **Amplitude** | **Densité** | L'amplitude est la **largeur** de la classe ($ b_{sup} - b_{inf} $) ; la densité est l'effectif **rapporté** à cette largeur ($ n_i / a_i $) |
| **Hauteur d'un histogramme** | **Hauteur d'un diagramme en barres** | Dans un histogramme, c'est la **densité** et c'est **l'aire** qui représente l'effectif ; dans un diagramme en barres, la hauteur **est** l'effectif |
| **Moyenne** | **Médiane** | La moyenne est le **centre de gravité** (elle utilise toutes les valeurs) ; la médiane est le **centre de l'effectif** (elle n'utilise que le rang) |
| **Médiane** | **Classe médiane** | Même distinction que mode / classe modale : la classe médiane est l'intervalle **qui contient** la médiane, qu'on obtient ensuite par interpolation |
| **Moyenne simple** | **Moyenne pondérée** | On pondère dès que les groupes **n'ont pas le même effectif**. La moyenne simple des moyennes est **fausse** dans ce cas |
| **Quantile** | **Quartile / décile / centile** | Le quantile est le **genre** ; quartile (4 parts), décile (10), centile (100) sont les **espèces** |
| **$ Q_1 $** | **$ D_1 $** | $ Q_1 $ laisse **25 %** de l'effectif en dessous, $ D_1 $ en laisse **10 %**. $ Q_1 = D_{2{,}5} $ |
| **Étendue** | **Écart inter-quartile** | L'étendue utilise **les deux extrêmes** (donc totalement sensible aux valeurs aberrantes) ; l'inter-quartile ne décrit que les **50 % centraux** |
| **Écart inter-quartile** | **Intervalle inter-quartile** | Le premier est **un nombre** ($ Q_3 - Q_1 $) ; le second est **un intervalle** ($ [Q_1 ; Q_3] $) |
| **EAM** | **Écart-type** | L'EAM moyenne des **valeurs absolues** des écarts ; l'écart-type passe par les **carrés**. L'écart-type est toujours ≥ EAM |
| **Variance** | **Écart-type** | La variance est dans l'**unité au carré** (donc ininterprétable) ; l'écart-type est la **racine** de la variance, dans l'unité de $ X $ |
| **Écart-type** | **Coefficient de variation** | L'écart-type est **absolu** (avec une unité) ; le CV est **relatif** (sans unité), donc seul comparable entre séries d'unités différentes |
| **Variance intra** | **Variance inter** | L'intra est la moyenne des variances **dans** les groupes ; l'inter est la variance **des moyennes** de groupe. Somme des deux = variance totale |
| **Dispersion** | **Concentration** | La dispersion décrit la répartition **des observations** ; la concentration décrit la répartition **de la somme** |
| **Part de l'agrégat** | **Fréquence** | La fréquence est la part de la **population** ; la part de l'agrégat est la part de la **masse** (des salaires, du patrimoine…) |
| **Courbe de Lorenz** | **Fonction de répartition** | La courbe de Lorenz met la **part cumulée de $ X $** en ordonnée ; la fonction de répartition met la **fréquence cumulée** en ordonnée, avec $ X $ en abscisse. Ce ne sont pas les mêmes axes |
| **Indice de Gini** | **Aire de concentration** | Le Gini est **le double** de l'aire de concentration. Confondre les deux divise le résultat par 2 |

### 3.2 — Les erreurs que commet la majorité des étudiants

1. **Confondre l'effectif et la densité pour trouver la classe modale.** Dès que les
   amplitudes diffèrent, il faut diviser. C'est l'erreur la plus fréquente du § 2.1.3.
2. **Faire la moyenne des moyennes sans pondérer.** Elle n'est exacte que si tous les groupes
   ont le même effectif — ce qui est rare. Deux classes de 10 et 30 élèves ne se moyennent
   pas à parts égales.
3. **Faire la moyenne des médianes.** Ce n'est jamais valable, même avec les bons poids. La
   médiane **ne s'agrège pas** — le contre-exemple $ \{1;2;3\} \cup \{100;200;300\} $ du
   § 2.1.15 le prouve en trois lignes.
4. **Oublier de trier avant de chercher une médiane.** La médiane est définie sur la série
   **ordonnée**. Sur la série brute, elle n'a aucun sens.
5. **Se tromper de rang médian pour un effectif pair.** Avec $ N $ pair, il n'y a pas
   d'observation centrale : la médiane est **la moyenne des deux valeurs de rang $ N/2 $ et
   $ N/2 + 1 $**.
6. **Donner la variance comme réponse finale.** La variance est une **étape**. La réponse
   qu'on interprète est l'**écart-type**, avec son unité. Le support de la diapositive 43
   s'arrête lui-même à la variance : il faut aller jusqu'à $ \sigma = 7{,}36 $.
7. **Oublier le carré dans les propriétés.** $ V(aX) = a^2 V(X) $ et non $ aV(X) $ ; en
   revanche $ \sigma_{aX} = \lvert a \rvert \sigma_X $. Confondre les deux niveaux est
   sanctionné à chaque fois.
8. **Croire qu'ajouter une constante change la dispersion.** $ V(X + a) = V(X) $. Ajouter
   6 points à toutes les notes ne change **rien** à l'écart-type.
9. **Appliquer Bienaymé-Tchebychev avec $ k \le 1 $.** L'inégalité ne dit rien pour
   $ k \le 1 $ : elle donnerait « au moins 0 % », ce qui est vide de sens. C'est exactement le
   problème de la diapositive 48 (§ 2.2.13).
10. **Comparer des écarts-types de séries d'unités ou d'échelles différentes.** Il faut alors
    le **coefficient de variation**. Comparer la volatilité en euros d'une action à 10 € et
    d'une action à 1 000 € n'a aucun sens.
11. **Utiliser Koenig sans élever la moyenne au carré.** $ V = \overline{x^2} - m^2 $, et non
    $ \overline{x^2} - m $. L'homogénéité dimensionnelle suffit à détecter l'erreur.
12. **Calculer une concentration sur une variable dont la somme n'a pas de sens.** Un Gini
    sur des notes ou sur des âges se calcule numériquement mais **ne s'interprète pas**.
13. **Oublier de diviser les aires de trapèzes par 10 000** quand les cumuls sont en
    pourcentages. Le résultat sort alors complètement de l'intervalle [0 ; 1] — et **ce
    contrôle-là est immédiat**.
14. **Confondre le complément à 100 par le haut et par le bas** dans la lecture d'une courbe
    de Lorenz. $ 100 - L(80) $ est la part **des 20 % les mieux payés**.
15. **Cumuler des valeurs déjà arrondies sans le dire.** L'erreur se propage ; elle est
    minime, mais un correcteur exigeant attend la mention.
16. **Comparer deux distributions sans vérifier l'homogénéité des champs.** Le cas 2005 / 2021
    du § 2.3.5 en est l'illustration parfaite : les bornes trahissent un changement de
    périmètre.
17. **Conclure « les inégalités ont augmenté » à partir de deux courbes qui se croisent.** En
    cas de croisement, deux indicateurs peuvent donner des réponses opposées (§ 2.3.7).
18. **Interpréter un écart-type sans le rapporter à la moyenne.** « σ = 500 € » ne dit rien
    tant qu'on ne sait pas si la moyenne est 1 000 € ou 100 000 €.
19. **Prendre le centre de classe pour la vraie moyenne sans le signaler.** C'est une
    **hypothèse** (répartition uniforme dans la classe), et elle est d'autant plus fragile
    que la classe est large.
20. **Oublier que la somme des écarts à la moyenne est nulle.** C'est précisément pour cela
    qu'on prend des valeurs absolues (EAM) ou des carrés (variance) — et non par goût de la
    complication.

### 3.3 — Ce qui sépare une copie moyenne d'une excellente copie

| La copie moyenne | La copie excellente |
|---|---|
| Donne le mode | Vérifie d'abord si les amplitudes sont égales, **calcule les densités** si elles ne le sont pas, et parle de **classe modale** pour une variable continue |
| Trace un histogramme | Rappelle que **c'est l'aire qui représente l'effectif**, et le démontre : $ \text{densité} \times \text{amplitude} = \text{effectif} $ |
| Calcule une moyenne | **Pondère** par les effectifs, vérifie l'ordre de grandeur, et signale que la moyenne est sensible aux extrêmes |
| Donne la médiane | Précise le **rang** utilisé, dit si l'effectif est pair ou impair, et **compare médiane et moyenne** pour diagnostiquer l'asymétrie |
| Calcule $ Q_1 $ et $ Q_3 $ | Définit le quantile comme **l'inverse de la fonction de répartition** ($ F(Q_p) = p $) et sait interpoler dans une classe |
| Calcule la variance | **Va jusqu'à l'écart-type**, donne son unité, et le rapporte à la moyenne (coefficient de variation) |
| Applique Koenig | **Justifie** pourquoi on l'utilise : un seul passage sur les données, donc agrégation possible avec deux nombres par groupe |
| Cite Bienaymé-Tchebychev | Vérifie que **$ k > 1 $**, précise que la borne est **valable quelle que soit la loi**, et donc **très lâche** en pratique |
| Calcule une variance par groupe | Écrit la **décomposition intra / inter**, interprète le rapport $ V_{inter}/\sigma^2 $ comme **pouvoir explicatif du découpage**, et annonce le lien avec le R² |
| Calcule des parts de masse salariale | Vérifie que **la somme fait 100 %** et démontre que **l'effectif total se simplifie** |
| Trace une courbe de Lorenz | **Trace d'abord la diagonale**, justifie la **convexité** par la pente $ m_{X_k}/m_X $, et écrit une phrase de lecture complète |
| Calcule un Gini | **Contrôle l'unité des aires**, vérifie que le résultat est dans [0 ; 1], et donne un **repère de comparaison** |
| Conclut « les inégalités ont augmenté » | Vérifie qu'il n'y a **pas de croisement** des courbes (dominance de Lorenz), puis **signale le risque de changement de champ** entre les deux millésimes |
| Reprend les chiffres du support | **Recalcule** et signale les incohérences — comme la variance du cas 4 (diapositive 55) ou les conclusions non reconstructibles de la diapositive 48 |
| S'arrête au calcul | Termine par **une phrase d'interprétation** avec l'unité, la sous-population et le champ |

### 3.4 — Les quatre anomalies du support à connaître

Ce chapitre contient quatre points où le support d'origine est fautif, incomplet ou
non reconstructible. **Les connaître te protège :** si l'un d'eux tombe à l'examen, tu sauras
que ce n'est pas toi qui te trompes.

| Diapositive | Ce que le support affiche | Ce que donne le recalcul | Statut |
|---|---|---|---|
| **55** (cas 4) | Variance = 10,4 ; écart-type = 3,2 | Variance = **20,8** ; écart-type = **4,56** | **Erreur.** Le support a divisé une fois de trop par 2. Conséquence : **le classement des cas 2 et 4 par dispersion est inversé** (§ 2.2.16) |
| **48** (Sayna) | « 99 % de chances de faire des gains en périodes 1, 2, 3, 5 » | **Non reconstructible.** Bienaymé-Tchebychev exige $ k > 1 $, or $ m/\sigma < 1 $ dans les cinq périodes ; de plus la période 2 a une moyenne **négative** | **Conclusion non démontrable** avec les seuls outils du chapitre (§ 2.2.13) |
| **35** | Titre « retraités, année 2008 » | Le tableau affiché est celui des **niveaux de vie de 2024** de la diapositive 34 | **Erreur de titre** (§ 2.2.7) |
| **43** | S'arrête à la variance (54,19) | L'écart-type $ \sigma = \sqrt{54{,}19} = \mathbf{7{,}36} $ ans n'est **jamais calculé** | **Omission** : c'est pourtant le seul chiffre interprétable (§ 2.2.11) |

::: piege Comment traiter une erreur du support en examen
**Ne recopie jamais un chiffre faux « parce qu'il est dans le cours ».** Mais ne te contente
pas non plus de le corriger en silence.

**La formulation qui rapporte des points :** « En appliquant la formule
$ V = \frac{1}{N}\sum n_i(x_i - m)^2 $, j'obtiens 20,8 et non 10,4. L'écart d'un facteur 2
suggère une division supplémentaire par 2 dans le calcul du support. Je retiens 20,8, soit
$ \sigma = 4{,}56 $, ce qui modifie le classement des cas 2 et 4. »

**Tu montres trois choses en trois lignes :** que tu sais calculer, que tu contrôles tes
résultats, et que tu mesures les conséquences d'une erreur. **C'est exactement le profil
qu'on attend d'un analyste.**
:::

<!--saut-->

## 4. Système d'ancrage mémoriel

### 4.1 — Fiche de synthèse

::: synthese Chapitre 2 « Résumer pour informer » — l'essentiel sur deux pages
**LE PROJET DU CHAPITRE.** Présenter (chapitre 1) conserve **toute** l'information. Résumer
en **perd volontairement** pour produire quelques chiffres décisionnels. Trois familles :
**position** (où ?), **dispersion** (à quel point c'est étalé ?), **concentration** (comment
le total se partage-t-il ?).

**① POSITION — LE MODE.** La modalité de **fréquence maximale**. Variable continue → **classe
modale**. ⚠ Si les amplitudes sont **inégales**, la classe modale est celle de **densité
maximale** : $ d_i = n_i / a_i $ avec $ a_i = b_{sup} - b_{inf} $. **Histogramme :** hauteur =
densité, et **c'est l'aire qui représente l'effectif** ($ d_i \times a_i = n_i $).

**① POSITION — LA MOYENNE.** Trois écritures du même objet :
$ m_X = \frac{1}{N}\sum_{i=1}^{N} x_i $ (données brutes) ·
$ m_X = \sum_{i=1}^{p} f_i x_i $ (distribution) ·
$ m_X = \sum_{k=1}^{K} \frac{N_k}{N} m_{X_k} $ (agrégation).
**Trois propriétés :** ① $ \sum (x_i - m_X) = 0 $ — la somme des écarts est nulle ;
② **linéarité** $ m_{aX+b} = a\,m_X + b $ ; ③ **sensibilité aux valeurs extrêmes**.

**① POSITION — LA MÉDIANE.** La valeur qui **partage l'effectif en deux** : $ F(Me) = 0{,}5 $.
$ N $ impair → valeur de rang $ (N+1)/2 $ ; $ N $ pair → **moyenne** des rangs $ N/2 $ et
$ N/2+1 $. Sur une distribution : classe médiane puis **interpolation linéaire**.
⚠ **La médiane ne s'agrège JAMAIS.**

**DIAGNOSTIC D'ASYMÉTRIE.** $ Me < m_X $ → distribution **étalée à droite** (salaires,
patrimoines). $ Me > m_X $ → étalée à gauche. $ Me \approx m_X $ → symétrique.

**② DISPERSION — LES INDICATEURS D'ÉCART ENTRE POSITIONS.**
**Étendue** $ = x_{\max} - x_{\min} $ (totalement sensible aux extrêmes).
**Quantile** $ Q_p $ : la valeur telle que $ F(Q_p) = p $ — c'est **l'inverse de la fonction
de répartition**. Quartiles (4 parts), déciles (10), centiles (100).
**Écart inter-quartile** $ = Q_3 - Q_1 $ (50 % centraux) · **inter-décile**
$ = D_9 - D_1 $ (80 % centraux) · **rapport inter-décile** $ = D_9/D_1 $ (sans unité).
**Boxplot** : boîte de $ Q_1 $ à $ Q_3 $, trait à la médiane, moustaches aux extrêmes.

**② DISPERSION — LES INDICATEURS D'ÉCART À LA MOYENNE.**
$$ EAM = \frac{1}{N}\sum \lvert x_i - m_X \rvert \qquad \sigma^2 = V(X) = \frac{1}{N}\sum (x_i - m_X)^2 \qquad \sigma = \sqrt{V(X)} $$
**Koenig :** $ V(X) = \frac{1}{N}\sum x_i^2 - m_X^2 $ (« moyenne des carrés moins carré de la
moyenne ») — **un seul passage sur les données, donc agrégation possible**.
**Propriétés :** $ V(X + a) = V(X) $ · $ V(aX) = a^2 V(X) $ · $ \sigma_{aX} = \lvert a \rvert \sigma_X $ · $ V(-X) = V(X) $.
**Coefficient de variation** $ CV = \sigma / m_X $ — **sans unité**, seul comparable entre
séries d'échelles différentes.
**Bienaymé-Tchebychev :** $ P(\lvert X - m \rvert \ge k\sigma) \le 1/k^2 $, **valable quelle
que soit la loi**, donc **très lâche**. ⚠ **Ne dit rien pour $ k \le 1 $.**
**Décomposition :** $ \sigma^2 = V_{intra} + V_{inter} $ avec
$ V_{intra} = \sum \frac{N_k}{N}\sigma_k^2 $ et
$ V_{inter} = \sum \frac{N_k}{N}(m_{X_k} - m_X)^2 $. Le rapport $ V_{inter}/\sigma^2 $ mesure
le **pouvoir explicatif du découpage**.

**③ CONCENTRATION — LA CONDITION D'EXISTENCE.** Elle n'existe que si **la somme de $ X $ a
un sens** (salaires → masse salariale ✔ ; tailles, notes, âges ✖).

**③ CONCENTRATION — LA PART DE L'AGRÉGAT.**
$ \sum_{i=1}^{N_k} x_i = N_k m_{X_k} $ (« la somme = la moyenne × l'effectif »), d'où
$$ p_k = \frac{N_k m_{X_k}}{\sum_j N_j m_{X_j}} = \frac{f_k m_{X_k}}{m_X} = f_k \times \frac{m_{X_k}}{m_X} $$
**L'effectif total se simplifie** : le calcul est possible à $ N $ inconnu.

**③ CONCENTRATION — LORENZ ET GINI.** La **courbe de Lorenz** met la **part cumulée de
$ X $** (ordonnée) en face de la **fréquence cumulée de la population** (abscisse),
individus **rangés par $ X $ croissant**. Elle part de (0;0), arrive à (100;100), est
**croissante** et **convexe**, et sa **pente sur la classe $ k $ vaut $ m_{X_k}/m_X $**. La
**diagonale** est la courbe de l'**égalité parfaite**.
**Dominance de Lorenz :** une courbe partout plus éloignée de la diagonale → **tous** les
indicateurs concluent à plus d'inégalité. **Croisement** → conclusions possiblement
contradictoires.
$$ G = 2 \times \mathcal{A} = 2\left[\frac{1}{2} - \sum \frac{(b+B)h}{2}\right], \qquad 0 \le G \le 1 $$
⚠ **Si les cumuls sont en %, diviser la somme des trapèzes par 10 000.**
$ G = 0 $ → égalité parfaite · $ G \to 1 $ → concentration totale (max exact $ = (N-1)/N $).

**LES CHIFFRES DU CHAPITRE À CONNAÎTRE.** Âges (diapo 42-43) : $ m = 47{,}9 $ ;
$ EAM = 5{,}7 $ ; $ \sigma^2 = 54{,}19 $ ; $ \sigma = \mathbf{7{,}36} $.
Niveau de vie 2024 : $ D_9/D_1 = \mathbf{3{,}48} $.
Salaires : $ G_{2005} = \mathbf{0{,}2472} $ → $ G_{2021} = \mathbf{0{,}3564} $ (**+ 44 %**).
Part du 1ᵉʳ quintile : **11,2 % → 3,9 %** (divisée par 2,9).

**LE CHOIX DE L'INDICATEUR.** Type de données **puis** objectif. Asymétrie → médiane.
Agrégation → moyenne. Unités différentes → CV. Partage d'un total → Lorenz et Gini.
:::

<!--saut-->

### 4.2 — Cartes de révision

Soixante-cinq cartes couvrant l'intégralité du chapitre. **Utilisation : cache la réponse,
formule la tienne à voix haute, puis compare. Une carte n'est acquise que si tu produis la
réponse complète, pas si tu la reconnais.**

**Le projet du chapitre**

::: carte
Quelle est la différence de nature entre « présenter » (chapitre 1) et « résumer »
(chapitre 2) ?
--
**Présenter conserve toute l'information** (série brute, distribution des effectifs :
aucune donnée n'est perdue). **Résumer en perd volontairement** : on remplace $ N $ valeurs
par quelques chiffres. **La perte est le prix de la décision** — on ne décide pas devant
1 200 nombres.
:::

::: carte
Quelles sont les trois familles d'indicateurs du chapitre, et la question de chacune ?
--
**Position** : où se situe la distribution ? (mode, moyenne, médiane).
**Dispersion** : à quel point est-elle étalée ? (étendue, écarts inter-quantiles, EAM,
variance, écart-type, CV).
**Concentration** : comment le total se partage-t-il ? (part de l'agrégat, Lorenz, Gini).
:::

**Le mode**

::: carte
Définissez le mode.
--
La **modalité de fréquence (ou d'effectif) maximale**. C'est **le seul indicateur de position
calculable sur une variable qualitative**.
:::

::: carte
Pourquoi parle-t-on de « classe modale » et non de « mode » pour une variable continue ?
--
Parce qu'une variable continue est regroupée en **classes** : l'indicateur désigne donc un
**intervalle**, pas une valeur. Dire « le mode est [20 ; 30[ » est un abus de langage
sanctionné.
:::

::: carte
Comment détermine-t-on la classe modale quand les classes ont des **amplitudes inégales** ?
--
Par la **densité maximale**, pas par l'effectif maximal :
$$ d_i = \frac{n_i}{a_i} \qquad \text{avec } a_i = b_{sup} - b_{inf} $$
Une classe deux fois plus large contient mécaniquement plus d'individus sans être plus
« dense ».
:::

::: carte
Dans un histogramme, que représentent la hauteur et l'aire d'un rectangle ?
--
La **hauteur** représente la **densité** $ d_i = n_i/a_i $. **L'aire représente l'effectif** :
$ \text{aire} = d_i \times a_i = \frac{n_i}{a_i} \times a_i = n_i $.
**C'est la propriété fondamentale de l'histogramme**, et elle le distingue du diagramme en
barres où la hauteur *est* l'effectif.
:::

::: carte
Que se passe-t-il si l'on trace un histogramme en portant les effectifs en hauteur avec des
classes d'amplitudes inégales ?
--
**La figure ment.** Les classes larges paraissent surreprésentées, puisque leur aire vaut
$ n_i \times a_i $ au lieu de $ n_i $. La forme de la distribution est déformée
proportionnellement aux amplitudes.
:::

**La moyenne**

::: carte
Donnez les trois écritures de la moyenne arithmétique et le cas d'usage de chacune.
--
① **Données brutes** : $ m_X = \frac{1}{N}\sum_{i=1}^{N} x_i $.
② **Distribution** : $ m_X = \sum_{i=1}^{p} f_i x_i $ (ou $ \frac{1}{N}\sum n_i x_i $).
③ **Agrégation** : $ m_X = \sum_{k=1}^{K} \frac{N_k}{N} m_{X_k} $.
**Les trois donnent le même nombre** : ce sont trois regroupements de la même somme.
:::

::: carte
Énoncez et démontrez la première propriété de la moyenne.
--
**La somme des écarts à la moyenne est nulle :** $ \sum_{i=1}^{N}(x_i - m_X) = 0 $.
*Démonstration :* $ \sum (x_i - m_X) = \sum x_i - N m_X = N m_X - N m_X = 0 $, puisque
$ \sum x_i = N m_X $ par définition de la moyenne.
**Conséquence :** on ne peut pas mesurer la dispersion par la moyenne des écarts — d'où les
valeurs absolues (EAM) et les carrés (variance).
:::

::: carte
Énoncez la propriété de linéarité de la moyenne et ce qu'elle autorise.
--
$ m_{aX + b} = a\,m_X + b $.
**Elle autorise l'agrégation** : la moyenne d'un ensemble se reconstruit à partir des
moyennes de ses parties, pondérées par les effectifs. **C'est ce que l'écart-type ne permet
pas** (d'où Koenig).
:::

::: carte
Pourquoi la moyenne est-elle sensible aux valeurs extrêmes, et la médiane non ?
--
La moyenne utilise **la valeur** de chaque observation : une valeur très grande pèse
proportionnellement à sa taille. La médiane n'utilise que **le rang** : remplacer la plus
grande valeur par une valeur dix fois plus grande **ne change pas son rang**, donc ne change
pas la médiane.
:::

::: carte
Quand la moyenne d'un ensemble est-elle égale à la moyenne simple des moyennes de groupe ?
--
**Uniquement si tous les groupes ont le même effectif.** Sinon il faut pondérer :
$ m_X = \sum \frac{N_k}{N} m_{X_k} $. C'est le cas des tableaux de quintiles (20 % chacun),
où la pondération est uniforme — mais c'est une exception, pas la règle.
:::

**La médiane et les quantiles**

::: carte
Définissez la médiane de deux façons.
--
**Définition par le partage :** la valeur qui partage la population **ordonnée** en deux
parties d'effectifs égaux — 50 % en dessous, 50 % au-dessus.
**Définition par la fonction de répartition :** la valeur $ Me $ telle que
$ F(Me) = 0{,}5 $.
:::

::: carte
Comment calcule-t-on la médiane sur données brutes selon la parité de $ N $ ?
--
**Trier d'abord**, toujours.
$ N $ **impair** → la valeur de rang $ \frac{N+1}{2} $.
$ N $ **pair** → **la moyenne des valeurs de rang $ \frac{N}{2} $ et $ \frac{N}{2}+1 $**
(il n'existe pas d'observation centrale).
:::

::: carte
Comment obtient-on la médiane à partir d'une distribution groupée en classes ?
--
① Calculer les **fréquences cumulées**. ② Repérer la **classe médiane** : la première dont
la fréquence cumulée atteint ou dépasse 0,5. ③ **Interpoler linéairement** dans cette classe,
sous l'hypothèse de répartition uniforme :
$$ Me = b_{inf} + a \times \frac{0{,}5 - F(b_{inf})}{F(b_{sup}) - F(b_{inf})} $$
:::

::: carte
Peut-on calculer la médiane d'un ensemble à partir des médianes de ses sous-groupes ?
--
**Non, jamais** — même avec les bons poids.
*Contre-exemple :* $ A = \{1;2;3\} $ ($ Me = 2 $), $ B = \{100;200;300\} $ ($ Me = 200 $).
Moyenne des médianes = 101. Vraie médiane de $ A \cup B = \{1;2;3;100;200;300\} $ :
$ (3+100)/2 = \mathbf{51{,}5} $. **Écart d'un facteur 2.**
La médiane dépend de **la position relative de toutes les valeurs**, information détruite par
le résumé en médianes de groupe.
:::

::: carte
Que signifie l'écart entre médiane et moyenne d'une distribution ?
--
$ Me < m_X $ → distribution **étalée à droite** : quelques très grandes valeurs tirent la
moyenne vers le haut (salaires, patrimoines, capitalisations).
$ Me > m_X $ → **étalée à gauche**.
$ Me \approx m_X $ → **symétrique**.
**C'est le diagnostic d'asymétrie le moins coûteux qui existe : deux chiffres.**
:::

::: carte
Définissez un quantile d'ordre $ p $.
--
La valeur $ Q_p $ telle que $ F(Q_p) = p $ : **une proportion $ p $ de la population a une
valeur inférieure ou égale à $ Q_p $**. Formellement, **le quantile est l'inverse de la
fonction de répartition** : $ Q_p = F^{-1}(p) $.
:::

::: carte
Quartiles, déciles, centiles : quelle est la logique commune, et combien de valeurs
définissent chaque famille ?
--
On découpe la population ordonnée en parts d'effectifs égaux.
**Quartiles** : 4 parts → **3 valeurs** ($ Q_1, Q_2 = Me, Q_3 $).
**Déciles** : 10 parts → **9 valeurs** ($ D_1 $ à $ D_9 $).
**Centiles** : 100 parts → **99 valeurs**.
**Règle : $ n $ parts se délimitent par $ n - 1 $ valeurs.**
:::

::: carte
Que valent $ Q_1 $ et $ Q_3 $ exprimés en déciles ? Et $ Me $ ?
--
$ Q_1 = D_{2{,}5} $ · $ Q_3 = D_{7{,}5} $ · $ Me = Q_2 = D_5 $.
**Tous les quantiles appartiennent à la même famille** : seuls les ordres changent.
:::

**Les indicateurs de dispersion**

::: carte
Pourquoi un indicateur de position ne suffit-il jamais à résumer une distribution ?
--
Parce que **deux distributions de même moyenne peuvent être radicalement différentes**
(les quatre cas de la diapositive 27). La position dit **où** ; il faut la dispersion pour
dire **à quel point les individus se ressemblent**. Une moyenne sans dispersion est une
information incomplète — et en finance, dangereuse.
:::

::: carte
Définissez l'étendue et donnez sa faiblesse.
--
$ \text{étendue} = x_{\max} - x_{\min} $.
**Faiblesse : elle ne dépend que des deux valeurs extrêmes**, donc elle est totalement
détruite par une valeur aberrante et ne dit rien de la répartition entre les deux bornes.
:::

::: carte
Citez les trois écarts inter-quantiles usuels et ce que chacun décrit.
--
**Écart inter-quartile** $ Q_3 - Q_1 $ : l'étalement des **50 % centraux**.
**Écart inter-décile** $ D_9 - D_1 $ : l'étalement des **80 % centraux**.
**Rapport inter-décile** $ D_9 / D_1 $ : le même en **relatif**, donc **sans unité** et
comparable entre populations.
:::

::: carte
Décrivez la construction d'un *boxplot* et ce qu'on y lit immédiatement.
--
**Boîte** de $ Q_1 $ à $ Q_3 $ (les 50 % centraux), **trait intérieur** à la **médiane**,
**moustaches** jusqu'aux valeurs extrêmes (ou aux déciles selon la convention).
**Lecture immédiate :** le niveau (position du trait), la dispersion (largeur de la boîte),
et **l'asymétrie** — si le trait n'est pas au centre de la boîte, la distribution est
asymétrique.
:::

::: carte
Écrivez la formule de l'écart absolu moyen et expliquez pourquoi on prend la valeur absolue.
--
$$ EAM = \frac{1}{N}\sum_{i=1}^{N} \lvert x_i - m_X \rvert $$
**On prend la valeur absolue parce que la somme des écarts simples est nulle** (propriété 1
de la moyenne) : sans valeur absolue, l'indicateur vaudrait 0 pour **toute** distribution.
:::

::: carte
Écrivez la variance et l'écart-type. Pourquoi passe-t-on de l'une à l'autre ?
--
$$ V(X) = \sigma^2 = \frac{1}{N}\sum_{i=1}^{N}(x_i - m_X)^2 \qquad \sigma = \sqrt{V(X)} $$
**Le carré résout le problème du signe** (comme la valeur absolue) mais **change l'unité** :
la variance est en unité **au carré**, donc ininterprétable. **La racine ramène l'indicateur
dans l'unité de $ X $** : c'est l'écart-type qu'on interprète et qu'on communique.
:::

::: carte
Pourquoi préfère-t-on la variance à l'EAM, alors que l'EAM est plus intuitif ?
--
Parce que **le carré est dérivable partout, la valeur absolue non**. Toute la statistique qui
suit — moindres carrés, régression, décomposition intra/inter, R² — repose sur la
dérivabilité. **L'EAM est plus lisible ; la variance est plus maniable, et c'est elle qui a
gagné.**
:::

::: carte
Énoncez la formule de Koenig et dites pourquoi elle est utile.
--
$$ V(X) = \frac{1}{N}\sum_{i=1}^{N} x_i^2 - m_X^2 $$
« La moyenne des carrés moins le carré de la moyenne. »
**Utilité :** la formule de définition exige de connaître $ m_X $ **avant** de calculer les
écarts — deux passages sur les données. Koenig ne demande que **deux sommes**
($ \sum x_i $ et $ \sum x_i^2 $), calculables en **un seul passage**. **C'est ce qui rend
l'agrégation possible : deux nombres suffisent à transmettre un groupe.**
:::

::: carte
Donnez les trois propriétés de la variance et leur traduction sur l'écart-type.
--
① **Invariance par translation** : $ V(X + a) = V(X) $ — ajouter une constante déplace la
distribution sans la déformer.
② **Non-linéarité** : $ V(aX) = a^2 V(X) $, donc
$ \sigma_{aX} = \lvert a \rvert \sigma_X $.
③ **Corollaire** : $ V(-X) = V(X) $.
**L'erreur classique : écrire $ V(aX) = aV(X) $.**
:::

::: carte
Énoncez l'inégalité de Bienaymé-Tchebychev et ses deux conditions d'usage.
--
$$ P\big(\lvert X - m \rvert \ge k\sigma\big) \le \frac{1}{k^2} $$
**Condition 1 : $ k > 1 $** — pour $ k \le 1 $ la borne est ≥ 1 et ne dit rien.
**Condition 2 : aucune** sur la loi — et c'est sa force **et** sa faiblesse : valable pour
toute distribution, donc **très lâche**. Pour $ k = 2 $ elle garantit 75 % ; une loi normale
donnerait 95 %.
:::

::: carte
Définissez le coefficient de variation et dites quand il est indispensable.
--
$$ CV = \frac{\sigma}{m_X} $$
**Sans unité.** Il est indispensable dès qu'on compare des séries d'**unités différentes**
ou d'**ordres de grandeur différents** : un écart-type de 500 € ne signifie pas la même chose
autour d'une moyenne de 1 000 € (CV = 0,5) et de 100 000 € (CV = 0,005).
:::

::: carte
Écrivez la variance calculée à partir d'une distribution.
--
$$ V(X) = \sum_{i=1}^{p} f_i (x_i - m_X)^2 = \frac{1}{N}\sum_{i=1}^{p} n_i (x_i - m_X)^2 $$
**Chaque écart au carré est pondéré par l'effectif de sa modalité.** L'oubli de la
pondération est l'erreur numéro un sur ce calcul.
:::

::: carte
Écrivez la décomposition intra / inter de la variance.
--
$$ \sigma^2 = V_{intra} + V_{inter} $$
$$ V_{intra} = \sum_{k=1}^{K} \frac{N_k}{N}\,\sigma_k^2 \qquad V_{inter} = \sum_{k=1}^{K} \frac{N_k}{N}\,(m_{X_k} - m_X)^2 $$
**Intra** = dispersion **à l'intérieur** des groupes. **Inter** = dispersion **des moyennes**
de groupe.
:::

::: carte
Que mesure le rapport $ V_{inter} / \sigma^2 $, et quels sont ses deux cas extrêmes ?
--
Il mesure le **pouvoir explicatif du découpage en groupes** — la part de la dispersion totale
qu'explique l'appartenance à un groupe.
$ V_{inter} \approx 0 $ → les groupes ont la même moyenne : **le découpage n'explique rien**.
$ V_{intra} \approx 0 $ → chaque groupe est homogène : **le découpage explique tout**.
**C'est l'ancêtre du rapport de corrélation puis du R².**
:::

**La concentration**

::: carte
Quelle est la différence entre dispersion et concentration ?
--
La **dispersion** s'intéresse à la répartition **des observations** ($ x_i $ autour de
$ m_X $). La **concentration** s'intéresse à la répartition **de la somme** (quelle part du
total chaque groupe détient-il ?).
**Point commun :** les deux mesurent des inégalités. **Ce sont deux angles sur le même
phénomène, pas deux versions du même outil.**
:::

::: carte
Quelle condition une variable doit-elle remplir pour qu'on puisse en mesurer la
concentration ? Donnez deux exemples de chaque côté.
--
**Sa somme doit désigner un objet réel** (variable extensive et additive).
**Oui** : salaires (→ masse salariale), patrimoine (→ patrimoine total), chiffre d'affaires,
émissions de CO₂.
**Non** : taille, note, température, âge — additionner ces valeurs ne produit rien.
**Le calcul reste numériquement possible ; le résultat ne s'interprète pas.**
:::

::: carte
Qu'est-ce que l'agrégat d'une variable ? Comment se calcule-t-il par groupe ?
--
L'**agrégat** est la **somme de $ X $** sur la population : $ \sum_{i=1}^{N} x_i $. Pour les
salaires, c'est la **masse salariale**.
Par groupe : $ \sum_{i=1}^{N_k} x_i = N_k\, m_{X_k} $ — **« la somme = la moyenne ×
l'effectif »**, qui n'est que la définition de la moyenne multipliée par $ N_k $.
:::

::: carte
Écrivez la part de l'agrégat d'une classe, sous ses trois formes équivalentes.
--
$$ p_k = \frac{N_k\,m_{X_k}}{\sum_j N_j\,m_{X_j}} = \frac{f_k\,m_{X_k}}{m_X} = f_k \times \frac{m_{X_k}}{m_X} $$
**Troisième forme, la plus parlante :** la part d'une classe est **sa fréquence multipliée
par son avantage relatif de moyenne**.
:::

::: carte
Pourquoi peut-on calculer les parts de l'agrégat sans connaître l'effectif total ?
--
Parce que $ N_k = f_k N $ : le facteur $ N $ apparaît au numérateur **et** au dénominateur et
**se simplifie**.
$$ p_k = \frac{f_k N m_{X_k}}{\sum_j f_j N m_{X_j}} = \frac{f_k m_{X_k}}{\sum_j f_j m_{X_j}} $$
**Poser $ N = 1 $ n'est donc pas une approximation : c'est une simplification exacte.**
:::

::: carte
Quel contrôle doit-on faire systématiquement après avoir calculé des parts de l'agrégat ?
--
**Leur somme doit valoir 100 %** (aux arrondis près). Si elle ne les vaut pas, il y a une
erreur — sauf écart de l'ordre du dixième, imputable aux arrondis, **qu'il faut alors
signaler**.
:::

::: carte
Définissez la courbe de Lorenz : que porte-t-on sur chaque axe, et dans quel ordre range-t-on
les individus ?
--
**Abscisse :** la **fréquence cumulée de la population**. **Ordonnée :** la **part cumulée de
l'agrégat de $ X $**.
**Les individus doivent être rangés par valeur croissante de $ X $** — sans cette condition,
la courbe n'a aucune des propriétés qui la rendent utile.
:::

::: carte
Énoncez les quatre propriétés de la courbe de Lorenz.
--
① Elle **part de (0 ; 0) et arrive à (100 ; 100)**.
② Elle est **croissante** (on cumule des parts positives).
③ Sa **pente sur la classe $ k $ vaut $ m_{X_k}/m_X $**.
④ Elle est **convexe** (les pentes croissent puisque les classes sont ordonnées), donc
**située sous la diagonale**.
:::

::: carte
Que représente la pente de la courbe de Lorenz en un point, et que signifie une pente
égale à 1 ?
--
$$ \text{pente} = \frac{p_k}{f_k} = \frac{m_{X_k}}{m_X} $$
C'est le **rapport entre la moyenne locale et la moyenne générale**.
**Pente < 1** → la classe gagne moins que la moyenne, la courbe s'écarte de la diagonale.
**Pente = 1** → la classe gagne exactement la moyenne : **c'est le point où l'écart à la
diagonale est maximal**.
**Pente > 1** → la courbe revient vers la diagonale.
:::

::: carte
Que représente la diagonale sur un graphe de Lorenz, et pourquoi ?
--
**La courbe de Lorenz de l'égalité parfaite.** Si tout le monde a la même valeur, toutes les
pentes valent $ m_{X_k}/m_X = 1 $ : la courbe **est** la diagonale, et $ f $ % de la
population détient exactement $ f $ % du total.
**Sans elle, une courbe de Lorenz ne se lit pas** — c'est l'écart à la diagonale qui porte
toute l'information.
:::

::: carte
Écrivez la phrase-type de lecture d'un point de la courbe de Lorenz, puis appliquez-la à
$ L(20) = 3{,}9 $ en 2021.
--
**Moule :** « Les **…** % des salariés les moins payés perçoivent **…** % de la masse
salariale. »
**Application :** « En 2021, les **20 %** des salariés les moins payés perçoivent **3,9 %**
de la masse salariale » — contre 11,2 % en 2005.
:::

::: carte
$ L(80) = 61{,}8 $. Quelle est la part des 20 % les mieux payés ? Quelle erreur guette ici ?
--
$ 100 - 61{,}8 = \mathbf{38{,}2\,\%} $ pour **les 20 % les mieux payés**.
**L'erreur :** lire le complément comme la part des 20 % du **bas**. **La courbe de Lorenz se
lit toujours en partant des plus pauvres ; ce qui reste au-dessus appartient aux plus
riches.**
:::

::: carte
Qu'est-ce que la dominance de Lorenz, et qu'autorise-t-elle à conclure ?
--
Une distribution est **dominée au sens de Lorenz** par une autre si sa courbe est **partout**
plus éloignée de la diagonale. Dans ce cas, **tous les indicateurs d'inégalité usuels
convergent vers la même conclusion** — quel que soit l'ordre de quantile considéré, la
première distribution est plus inégalitaire. **La conclusion est alors robuste au choix de
l'indicateur.**
:::

::: carte
Que se passe-t-il quand deux courbes de Lorenz se croisent ?
--
L'une est plus inégalitaire **en bas** de la distribution, l'autre **en haut**. **Le
classement dépend alors de l'indicateur choisi**, et deux indicateurs peuvent donner des
réponses opposées sur les mêmes données. **On ne tranche pas : on décrit les deux
phénomènes.**
:::

::: carte
Définissez l'indice de Gini géométriquement.
--
**Le double de l'aire comprise entre la diagonale et la courbe de Lorenz** (l'« aire de
concentration ») :
$$ G = 2 \times \mathcal{A} $$
Proche de **1** → concentration (inégalité) **forte**. Proche de **0** → concentration
**faible**.
:::

::: carte
Écrivez la formule de calcul du Gini et expliquez d'où vient chaque terme.
--
$$ G = 2\left[\frac{1}{2} - \sum \frac{(b+B)\cdot h}{2}\right] $$
$ \frac{1}{2} $ = **aire du triangle sous la diagonale** (le carré unité vaut 1, la diagonale
le coupe en deux).
$ \sum \frac{(b+B)h}{2} $ = **aire sous la courbe**, découpée en **trapèzes** (la courbe est
un segment entre deux points consécutifs) — $ b $ petite base, $ B $ grande base, $ h $
largeur de la tranche.
:::

::: carte
Quel est le piège d'unité du calcul du Gini, et quel contrôle le détecte ?
--
**Si les cumuls sont exprimés en pourcentages (0 à 100), les aires de trapèzes sont en
« points de % au carré » et le carré entier vaut 10 000 — il faut donc diviser la somme des
trapèzes par 10 000** avant de la soustraire à 0,5.
**Contrôle :** l'aire de concentration doit être dans [0 ; 0,5] et le Gini dans [0 ; 1]. Un
résultat comme $ 0{,}5 - 3\,764 $ signale immédiatement l'oubli.
:::

::: carte
Démontrez que $ G = 0 $ en cas d'égalité parfaite.
--
Si tout le monde a la même valeur, les cumuls sont 20 · 40 · 60 · 80 · 100. Les trapèzes
valent 200 · 600 · 1 000 · 1 400 · 1 800, soit **5 000**.
$ \mathcal{A} = 0{,}5 - 5\,000/10\,000 = 0 $, donc $ G = 0 $.
**Géométriquement : la courbe est la diagonale, l'aire entre les deux est nulle.**
:::

::: carte
Pourquoi le Gini maximal d'une population de $ N $ individus vaut-il $ (N-1)/N $ et non 1 ?
--
Parce que le dernier individu — celui qui détient tout — occupe une largeur $ 1/N $ **non
nulle** en abscisse. Sous ce dernier segment subsiste un triangle d'aire $ \frac{1}{2N} $.
D'où $ \mathcal{A} = \frac{1}{2} - \frac{1}{2N} $ et $ G = 1 - \frac{1}{N} $.
**Pour $ N \to \infty $, $ G \to 1 $.** En pratique on retient $ 0 \le G \le 1 $.
:::

::: carte
Citez trois précautions avant de comparer deux indices de Gini.
--
① **Le concept mesuré** : Gini du patrimoine (> 0,6 en France) ≫ Gini du revenu (≈ 0,3). Ce
ne sont pas les mêmes objets.
② **Avant ou après redistribution** : le Gini des revenus primaires est bien supérieur à
celui du revenu disponible ; l'écart mesure l'effet du système socio-fiscal.
③ **Le champ** : même définition, même population, même période — sinon la comparaison est
un artefact.
:::

::: carte
Pourquoi accompagne-t-on toujours un Gini d'autres indicateurs ?
--
Parce qu'il est **peu sensible aux extrêmes** : il réagit surtout aux transferts autour du
**milieu** de la distribution. Un Gini stable peut masquer un décrochage du dernier centile.
**On l'accompagne du rapport $ D_9/D_1 $ et de la part du 1 % le plus riche.**
:::

**Les applications chiffrées du chapitre**

::: carte
Série des 20 âges (diapositives 42-43) : donnez la moyenne, l'EAM, la variance et
l'écart-type.
--
$ m = 47{,}9 $ ans · $ EAM = 5{,}7 $ ans · $ \sigma^2 = 54{,}19 $ ans² ·
$ \sigma = \sqrt{54{,}19} = \mathbf{7{,}36} $ ans.
**⚠ Le support s'arrête à la variance : l'écart-type, seul chiffre interprétable, n'y figure
pas.**
:::

::: carte
Niveau de vie 2024 : que vaut le rapport inter-décile et comment se lit-il ?
--
$ D_9/D_1 = \mathbf{3{,}48} $ : **les 10 % les plus aisés ont un niveau de vie au moins 3,48
fois supérieur à celui des 10 % les plus modestes.**
Les écarts entre déciles successifs croissent (3 730 → 2 860 → 9 800 → 12 640 €), ce qui
**prouve l'étalement à droite** de la distribution.
:::

::: carte
Salaires 2005 : quelle part de la masse salariale détient chaque quintile, et que vaut le
Gini ?
--
Parts : **11,2 · 13,3 · 16,2 · 21,1 · 38,2 %**. Cumuls : 11,2 · 24,5 · 40,7 · 61,8 · 100,0.
Trapèzes : 112 · 357 · 652 · **1 025** · 1 618 → somme **3 764**.
$ \mathcal{A} = 0{,}5 - 0{,}3764 = 0{,}1236 $ → $ G_{2005} = \mathbf{0{,}2472} $.
:::

::: carte
Salaires 2021 : mêmes questions.
--
Parts : **3,9 · 10,6 · 18,4 · 26,7 · 40,5 %**. Cumuls : 3,9 · 14,5 · 32,9 · 59,6 · 100,0.
Trapèzes : 39 · 184 · 474 · 925 · 1 596 → somme **3 218**.
$ \mathcal{A} = 0{,}5 - 0{,}3218 = 0{,}1782 $ → $ G_{2021} = \mathbf{0{,}3564} $.
:::

::: carte
Comment ont évolué les inégalités salariales entre 2005 et 2021, et quelle réserve doit
accompagner la réponse ?
--
**Hausse forte et robuste** : $ G $ passe de 0,247 à 0,356 (**+ 44 %**) ; la part du premier
quintile est **divisée par 2,9** (11,2 % → 3,9 %) ; le rapport entre quintiles extrêmes passe
de **3,4 à 10,4**. La courbe 2021 est **partout** sous celle de 2005 → **dominance de
Lorenz**, donc pas de contradiction possible entre indicateurs.
**Réserve :** le plancher (11 000 → 1 333 €), le plafond (55 600 → 51 490 €) et le salaire
moyen en euros courants (21 333 → 20 659 €) **baissent tous les trois**, ce qui suggère un
**changement de champ** entre les deux millésimes. Une partie de l'écart mesuré peut être un
artefact.
:::

**Les anomalies du support**

::: carte
Diapositive 55, cas 4 : quelle est l'erreur du support et quelle en est la conséquence ?
--
Le support annonce une variance de **10,4** et un écart-type de **3,2**. Le recalcul donne
$ \sigma^2 = \mathbf{20{,}8} $ et $ \sigma = \mathbf{4{,}56} $ — **exactement le double** :
une division par 2 en trop.
**Conséquence : le classement des cas 2 et 4 par dispersion est inversé.**
:::

::: carte
Diapositive 48 : pourquoi les conclusions du support ne sont-elles pas reconstructibles ?
--
Elles annoncent « 99 % de chances de faire des gains » via Bienaymé-Tchebychev. Or
l'inégalité **exige $ k > 1 $**, et ici $ m/\sigma < 1 $ dans **les cinq périodes** : aucun
$ k $ admissible ne permet la conclusion. De plus **la période 2 a une moyenne négative**.
**Conclusion non démontrable avec les outils du chapitre.**
:::

**Méthode et transfert**

::: carte
Donnez l'arbre de décision : quel indicateur choisir ?
--
① **Type de variable** : qualitative → mode seul ; quantitative → tout est ouvert.
② **Objectif** : niveau typique → position ; homogénéité → dispersion ; partage d'un total →
concentration (après vérification que la somme fait sens).
③ **Symétrie** : symétrique → moyenne ; asymétrique ou valeurs extrêmes → **médiane**.
④ **Unités comparables ?** oui → écart-type ; non → **coefficient de variation**.
⑤ **Faut-il agréger ?** moyenne oui ; variance via Koenig ou intra/inter ; **médiane et Gini
jamais**.
:::

::: carte
Traduisez les indicateurs du chapitre en vocabulaire de finance de marché.
--
**Écart-type = volatilité** (annualisée par $ \sigma\sqrt{252} $ sur des rendements
quotidiens).
**Quantile = VaR** : la VaR à 99 % est le centile d'ordre 1 de la distribution des pertes.
**$ m/\sigma $ ≈ ratio de Sharpe** (sans taux sans risque) — donc **CV ≈ son inverse**.
**Décomposition intra/inter = risque spécifique / risque systématique** : la diversification
agit sur l'intra, jamais sur l'inter.
**Lorenz-Gini = concentration d'un portefeuille** (parent de l'indice de Herfindahl
$ HHI = \sum w_i^2 $) **ou d'un P&L**.
:::

::: carte
Pourquoi une moyenne sans écart-type est-elle dangereuse en finance ?
--
Parce que **deux stratégies de même rendement moyen peuvent avoir des profils de risque
opposés**. Un rendement moyen de 8 % avec $ \sigma = 3\,\% $ et le même avec
$ \sigma = 40\,\% $ ne se gèrent pas de la même façon : la seconde peut ruiner un compte
avant que la moyenne ne se réalise. **La moyenne décrit l'espérance ; l'écart-type décrit ce
qu'il faut survivre pour l'atteindre.**
:::

<!--saut-->

### 4.3 — Moyens mnémotechniques

::: methode Les huit ancrages du chapitre
**① « P-D-C » — les trois familles, dans l'ordre du cours.**
**P**osition (où ?) → **D**ispersion (à quel point étalé ?) → **C**oncentration (comment le
total se partage ?). **Trois lettres, trois questions, trois sections.**

**② « MO-MÉ-MÉ » — les trois indicateurs de position.**
**MO**de · **MÉ**diane · **MÉ**dium (la moyenne, le « milieu » de gravité). Et leur ordre de
robustesse aux valeurs extrêmes : **mode et médiane résistent, moyenne non**.

**③ « L'AIRE FAIT L'EFFECTIF » — l'histogramme.**
Dans un **hist**ogramme, on **hisse** la **densité** et on lit **l'aire**. Dans un diagramme
en **barres**, la **barre** est l'effectif. **Un seul mot à retenir : dès qu'il y a des
classes, il y a des aires.**

**④ « ZÉRO, DONC CARRÉ » — pourquoi la variance existe.**
La somme des écarts à la moyenne vaut **zéro** → il faut casser les signes → **valeur
absolue** (EAM, lisible mais non dérivable) ou **carré** (variance, dérivable donc gagnante).
**Le zéro est la cause de tout le reste.**

**⑤ « KOENIG : LA MOYENNE DES CARRÉS MOINS LE CARRÉ DE LA MOYENNE. »**
La phrase est sa propre formule. Ordre à ne pas inverser : **c'est toujours le gros moins le
petit**, puisque la variance est positive — donc $ \overline{x^2} \ge (\overline{x})^2 $.
**Vérification instantanée : si tu obtiens une variance négative, tu as inversé.**

**⑥ « a AJOUTÉ NE CHANGE RIEN, a MULTIPLIÉ CHANGE AU CARRÉ. »**
$ V(X+a) = V(X) $ · $ V(aX) = a^2V(X) $ · $ \sigma_{aX} = \lvert a \rvert \sigma_X $.
**Image : translater une figure ne la déforme pas ; l'agrandir la déforme dans les deux
dimensions, donc au carré.**

**⑦ « INTRA DANS, INTER ENTRE. »**
$ V_{\text{intra}} $ = dispersion **dans** les groupes. $ V_{\text{inter}} $ = dispersion
**entre** les groupes. Et le total est la somme :
$ \sigma^2 = V_{\text{intra}} + V_{\text{inter}} $.
**En finance : intra = spécifique (diversifiable), inter = systématique (non
diversifiable).**

**⑧ « LORENZ SOUS LA DIAGONALE, GINI DOUBLE DE L'AIRE. »**
La courbe est **toujours** sous la diagonale (convexité). Le Gini est le **double** de l'aire
qui les sépare — **le « 2 » est la faute la plus fréquente : sans lui, on divise le résultat
par deux.** Et l'aire des trapèzes se divise par **10 000** quand les cumuls sont en %.
:::

::: methode Trois contrôles à faire systématiquement — ils détectent 90 % des erreurs
| Contrôle | Ce qu'il vérifie | Ce qu'il détecte |
|---|---|---|
| **La somme des fréquences fait 1** (et celle des parts fait 100 %) | La cohérence de la distribution | Une modalité oubliée, un effectif mal reporté |
| **L'indicateur est dans le bon intervalle** | $ 0 \le G \le 1 $ · $ \sigma \ge 0 $ · $ EAM \le \sigma $ · $ x_{\min} \le Me \le x_{\max} $ | Le piège des unités du Gini, un signe perdu, une racine oubliée |
| **L'ordre de grandeur est plausible** | Le résultat comparé à la moyenne et à l'étendue | Une erreur de facteur 10, une division en trop (le cas 4 de la diapositive 55) |

**Le troisième est le plus important et le plus négligé.** Un écart-type supérieur à
l'étendue est impossible. Un écart-type de 7,36 sur une série d'âges de moyenne 47,9 est
plausible ; un écart-type de 73,6 ne l'est pas.
:::

<!--saut-->

### 4.4 — Schéma récapitulatif

```
                    RÉSUMER UNE DISTRIBUTION
                              |
        +---------------------+---------------------+
        |                     |                     |
   1. POSITION          2. DISPERSION        3. CONCENTRATION
     « Où ? »        « Étalé comment ? »   « Le total, à qui ? »
        |                     |                     |
        |                     |            [ la somme de X
        |                     |              a-t-elle un sens ? ]
        |                     |                  NON -> STOP
        |                     |                  OUI  |
        |                     |                       |
   +----+----+       +--------+--------+         +----+----+
   |    |    |       |                 |         |         |
 MODE  MÉD  MOY   écarts entre     écarts à    PART DE   LORENZ
   |    |    |     positions       la moyenne  L'AGRÉGAT   |
   |    |    |        |                 |         |      GINI
   |    |    |    étendue            EAM         p_k = f_k m_k / m
   |    |    |    Q3 - Q1            VARIANCE      |
   |    |    |    D9 - D1            ÉCART-TYPE    v
   |    |    |    D9 / D1            CV        courbe cumulée
   |    |    |    boxplot                      |
   |    |    |                                 v
   |    |    |                            G = 2 x aire
   |    |    |
   |    |    +-- 3 écritures : brute / distribution / agrégation
   |    |    +-- 3 propriétés : somme des écarts = 0 ; linéarité ;
   |    |                       sensible aux extrêmes
   |    +------- F(Me) = 0,5 ; interpolation ; NE S'AGRÈGE PAS
   +------------ densité si amplitudes inégales ; aire = effectif


```

**Le fil qui relie toute la section « dispersion » :**

```
   LE FIL QUI RELIE TOUT : la somme des écarts à la moyenne est NULLE
        |                                 |
        v                                 v
   valeur absolue -> EAM            carré -> VARIANCE -> ÉCART-TYPE
                                              |
                              +---------------+---------------+
                              |               |               |
                          KOENIG        PROPRIÉTÉS      DÉCOMPOSITION
                     E(X²) - m²      V(X+a) = V(X)     s² = intra + inter
                     (1 passage)     V(aX) = a²V(X)          |
                              |                              v
                              +--> AGRÉGATION POSSIBLE   pouvoir explicatif
                                                          du découpage -> R²


```

**Et la traduction en salle de marché :**

```
   CE QUE CHAQUE FAMILLE DEVIENT EN FINANCE DE MARCHÉ
   ---------------------------------------------------
   moyenne .............. rendement espéré
   écart-type ........... VOLATILITÉ  (annualisée : s x racine(252))
   quantile ............. VALUE AT RISK
   m / s ................ ratio de Sharpe   (donc CV = son inverse)
   intra / inter ........ risque spécifique / risque systématique
   Lorenz - Gini ........ concentration d'un portefeuille (cf. Herfindahl)
```

<!--saut-->

## 5. Entraînement progressif

::: objectif Comment utiliser cette partie
**Quatre niveaux, dans l'ordre, sans en sauter.** Le niveau 1 vérifie que tu sais *dire* ; le
niveau 2 que tu sais *calculer* ; le niveau 3 que tu sais *raisonner* ; le niveau 4 que tu
sais *composer* dans les conditions de l'examen.

**Règle absolue : traite chaque exercice sur papier, entièrement, avant de lire la
correction.** Lire une correction sans avoir cherché ne produit qu'une illusion de
compétence — c'est exactement ce qui fait échouer les étudiants qui « ont l'impression de
comprendre le cours ».
:::

### Niveau 1 — Restitution

**Vingt-deux questions. Réponds sans rien regarder, puis compare.**

**Q1.** Quelle est la différence de nature entre « présenter » et « résumer » des données ?

**Q2.** Citez les trois familles d'indicateurs et la question à laquelle chacune répond.

**Q3.** Définissez le mode. Sur quel type de variable est-il le seul indicateur de position
disponible ?

**Q4.** Comment détermine-t-on la classe modale lorsque les classes ont des amplitudes
inégales ? Donnez la formule.

**Q5.** Dans un histogramme, que représentent la hauteur et l'aire d'un rectangle ?
Démontrez-le.

**Q6.** Donnez les trois écritures de la moyenne arithmétique.

**Q7.** Énoncez et démontrez la propriété « la somme des écarts à la moyenne est nulle ».
Quelle conséquence a-t-elle sur la construction des indicateurs de dispersion ?

**Q8.** Comment calcule-t-on la médiane sur données brutes selon la parité de l'effectif ?

**Q9.** Peut-on calculer la médiane d'un ensemble à partir des médianes de ses sous-groupes ?
Justifiez par un contre-exemple.

**Q10.** Que conclut-on de la comparaison entre médiane et moyenne ?

**Q11.** Définissez un quantile d'ordre $ p $ à l'aide de la fonction de répartition.

**Q12.** Combien de valeurs délimitent les quartiles ? les déciles ? les centiles ?

**Q13.** Citez les trois écarts inter-quantiles usuels et ce que chacun décrit.

**Q14.** Décrivez la construction d'un *boxplot* et les trois informations qu'on y lit.

**Q15.** Écrivez l'EAM, la variance et l'écart-type. Pourquoi passe-t-on de la variance à
l'écart-type ?

**Q16.** Énoncez la formule de Koenig et expliquez pourquoi elle rend l'agrégation possible.

**Q17.** Donnez les trois propriétés de la variance et leur traduction sur l'écart-type.

**Q18.** Énoncez l'inégalité de Bienaymé-Tchebychev et ses conditions d'usage.

**Q19.** Écrivez la décomposition intra / inter et dites ce que mesure le rapport
$ V_{inter}/\sigma^2 $.

**Q20.** Quelle condition une variable doit-elle remplir pour qu'on puisse mesurer sa
concentration ? Donnez un exemple de chaque côté.

**Q21.** Définissez la courbe de Lorenz et énoncez ses quatre propriétés.

**Q22.** Écrivez la formule du Gini, expliquez d'où vient chaque terme et donnez le piège
d'unité.

::: correction Réponses attendues
**Q1.** Présenter **conserve toute** l'information (série brute, distribution des effectifs).
Résumer en **perd volontairement** pour produire quelques chiffres décisionnels. La perte est
le prix de la décision.

**Q2.** **Position** — où se situe la distribution ? **Dispersion** — à quel point est-elle
étalée ? **Concentration** — comment le total se partage-t-il ?

**Q3.** La modalité de **fréquence maximale**. C'est le **seul indicateur de position
calculable sur une variable qualitative**.

**Q4.** Par la **densité maximale** : $ d_i = n_i/a_i $ avec $ a_i = b_{sup} - b_{inf} $. Une
classe plus large contient mécaniquement plus d'individus sans être plus dense.

**Q5.** Hauteur = **densité** ; aire = **effectif**. Démonstration :
$ \text{aire} = d_i \times a_i = \frac{n_i}{a_i} \times a_i = n_i $.

**Q6.** $ m_X = \frac{1}{N}\sum x_i $ (brutes) · $ m_X = \sum f_i x_i $ (distribution) ·
$ m_X = \sum \frac{N_k}{N} m_{X_k} $ (agrégation).

**Q7.** $ \sum(x_i - m_X) = \sum x_i - N m_X = N m_X - N m_X = 0 $. **Conséquence :** un
indicateur de dispersion fondé sur la moyenne des écarts vaudrait 0 pour toute distribution —
d'où le passage aux **valeurs absolues** (EAM) ou aux **carrés** (variance).

**Q8.** Trier d'abord. $ N $ impair → valeur de rang $ (N+1)/2 $. $ N $ pair → **moyenne des
valeurs de rang $ N/2 $ et $ N/2+1 $**.

**Q9.** **Non.** Contre-exemple : $ \{1;2;3\} $ (Me = 2) et $ \{100;200;300\} $ (Me = 200) →
moyenne des médianes = 101, vraie médiane de la réunion = $ (3+100)/2 = 51{,}5 $.

**Q10.** $ Me < m $ → étalée à **droite** ; $ Me > m $ → étalée à **gauche** ;
$ Me \approx m $ → **symétrique**.

**Q11.** $ Q_p $ est la valeur telle que $ F(Q_p) = p $ : le quantile est **l'inverse de la
fonction de répartition**, $ Q_p = F^{-1}(p) $.

**Q12.** **3** valeurs pour les quartiles, **9** pour les déciles, **99** pour les centiles.
Règle : $ n $ parts ⇒ $ n-1 $ valeurs.

**Q13.** $ Q_3 - Q_1 $ (50 % centraux) · $ D_9 - D_1 $ (80 % centraux) · $ D_9/D_1 $ (le même
en relatif, **sans unité**).

**Q14.** Boîte de $ Q_1 $ à $ Q_3 $, trait à la **médiane**, moustaches aux extrêmes. On y lit
le **niveau**, la **dispersion** et **l'asymétrie** (trait décentré dans la boîte).

**Q15.** $ EAM = \frac{1}{N}\sum \lvert x_i - m \rvert $ ·
$ V = \frac{1}{N}\sum (x_i - m)^2 $ · $ \sigma = \sqrt{V} $. On passe à l'écart-type parce que
la variance est en **unité au carré**, donc ininterprétable.

**Q16.** $ V(X) = \frac{1}{N}\sum x_i^2 - m_X^2 $. Elle ne demande que **deux sommes**
calculables en **un seul passage** ; il suffit donc de transmettre deux nombres par groupe
pour reconstituer la variance de l'ensemble.

**Q17.** $ V(X+a) = V(X) $ · $ V(aX) = a^2V(X) $ · $ V(-X) = V(X) $. Sur l'écart-type :
$ \sigma_{aX} = \lvert a \rvert \sigma_X $.

**Q18.** $ P(\lvert X - m \rvert \ge k\sigma) \le 1/k^2 $, **avec $ k > 1 $** et **sans aucune
hypothèse sur la loi** — d'où une borne valable partout mais **très lâche**.

**Q19.** $ \sigma^2 = V_{intra} + V_{inter} $ avec
$ V_{intra} = \sum \frac{N_k}{N}\sigma_k^2 $ et
$ V_{inter} = \sum \frac{N_k}{N}(m_{X_k}-m_X)^2 $. Le rapport $ V_{inter}/\sigma^2 $ mesure le
**pouvoir explicatif du découpage**.

**Q20.** **Sa somme doit avoir un sens** (variable extensive). Oui : salaire → masse salariale.
Non : taille, note, âge.

**Q21.** Abscisse = fréquence cumulée de la population ; ordonnée = part cumulée de l'agrégat ;
individus rangés par $ X $ **croissant**. Propriétés : ① passe par (0;0) et (100;100) ;
② croissante ; ③ pente $ = m_{X_k}/m_X $ ; ④ convexe donc **sous la diagonale**.

**Q22.** $ G = 2\left[\frac{1}{2} - \sum\frac{(b+B)h}{2}\right] $. Le $ \frac{1}{2} $ est
l'aire du triangle sous la diagonale ; la somme est l'aire sous la courbe découpée en
trapèzes ; le facteur 2 vient de la définition $ G = 2\mathcal{A} $. **Piège d'unité :**
si les cumuls sont en %, **diviser la somme des trapèzes par 10 000**.
:::

<!--saut-->

### Niveau 2 — Application chiffrée

#### Exercice 2.1 — Classe modale et histogramme

Une entreprise répartit ses 500 salariés selon leur ancienneté (en années) :

| Ancienneté | Effectif |
|---|---|
| [0 ; 2[ | 120 |
| [2 ; 5[ | 150 |
| [5 ; 10[ | 130 |
| [10 ; 20[ | 100 |
| **Total** | **500** |

**a.** Quelle classe a l'effectif le plus élevé ?
**b.** Calculez les amplitudes et les densités.
**c.** Quelle est la classe modale ? Commentez l'écart avec la réponse de la question a.
**d.** Quelles hauteurs porteriez-vous sur un histogramme ?

::: correction Corrigé de l'exercice 2.1
**a.** La classe **[2 ; 5[**, avec 150 salariés.

**b.** Amplitude $ a_i = b_{sup} - b_{inf} $ ; densité $ d_i = n_i / a_i $.

| Classe | $ n_i $ | $ a_i $ | $ d_i = n_i/a_i $ |
|---|---|---|---|
| [0 ; 2[ | 120 | 2 | $ 120/2 = \mathbf{60{,}0} $ |
| [2 ; 5[ | 150 | 3 | $ 150/3 = \mathbf{50{,}0} $ |
| [5 ; 10[ | 130 | 5 | $ 130/5 = \mathbf{26{,}0} $ |
| [10 ; 20[ | 100 | 10 | $ 100/10 = \mathbf{10{,}0} $ |

**c.** La classe modale est **[0 ; 2[**, de densité 60 — **et non [2 ; 5[**. La classe [2 ; 5[
compte plus de salariés (150 contre 120) **uniquement parce qu'elle est plus large** (3 ans
contre 2). Rapportée à sa largeur, elle est **moins dense**.
**Formulation attendue :** « L'ancienneté la plus fréquente se situe dans les deux premières
années : la densité y est de 60 salariés par année d'ancienneté, contre 50 dans la classe
suivante. »

**d.** **Les densités : 60 · 50 · 26 · 10.** Porter les effectifs (120 · 150 · 130 · 100)
donnerait une figure fausse : la dernière classe, dix fois plus large que la première,
occuperait une aire de $ 100 \times 10 = 1\,000 $ au lieu de 100.

**Contrôle :** $ \sum d_i \times a_i = 60(2) + 50(3) + 26(5) + 10(10) = 120 + 150 + 130 + 100 = 500 $ ✔
:::

#### Exercice 2.2 — Position et dispersion sur une distribution discrète

Le nombre de transactions exécutées chaque jour par un *desk*, observé sur 60 jours :

| Transactions $ x_i $ | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| Nombre de jours $ n_i $ | 5 | 12 | 18 | 14 | 8 | 3 |

**a.** Vérifiez l'effectif total et calculez les fréquences cumulées.
**b.** Calculez la moyenne.
**c.** Déterminez la médiane, $ Q_1 $, $ Q_3 $ et l'écart inter-quartile.
**d.** Calculez l'EAM.
**e.** Calculez la variance **par la formule de définition puis par Koenig**, et l'écart-type.
**f.** Calculez le coefficient de variation et vérifiez que $ EAM \le \sigma $.
**g.** Que conclut-on de la comparaison entre médiane et moyenne ?

::: correction Corrigé de l'exercice 2.2
**a.** $ N = 5+12+18+14+8+3 = \mathbf{60} $ ✔

| $ x_i $ | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| $ n_i $ | 5 | 12 | 18 | 14 | 8 | 3 |
| Cumul $ N_i $ | 5 | 17 | 35 | 49 | 57 | 60 |
| $ F_i $ | 0,0833 | 0,2833 | 0,5833 | 0,8167 | 0,9500 | 1,0000 |

**b.** $ \sum n_i x_i = 0(5) + 1(12) + 2(18) + 3(14) + 4(8) + 5(3) = 0+12+36+42+32+15 = 137 $.
$$ m_X = \frac{137}{60} = \mathbf{2{,}2833} \approx 2{,}28 \text{ transactions par jour} $$

**c.** $ N = 60 $ est **pair** : la médiane est la moyenne des valeurs de rang **30** et
**31**. Le cumul atteint 35 à $ x = 2 $ : les rangs 18 à 35 valent tous 2. Donc
$ Me = \frac{2+2}{2} = \mathbf{2} $.
$ Q_1 $ : première valeur dont $ F \ge 0{,}25 $ → $ F(1) = 0{,}2833 $ → $ Q_1 = \mathbf{1} $.
$ Q_3 $ : première valeur dont $ F \ge 0{,}75 $ → $ F(2) = 0{,}5833 $ (insuffisant),
$ F(3) = 0{,}8167 $ → $ Q_3 = \mathbf{3} $.
Écart inter-quartile $ = 3 - 1 = \mathbf{2} $ transactions.

**d.** $ \sum n_i \lvert x_i - m \rvert $ avec $ m = 2{,}2833 $ :

| $ x_i $ | $ \lvert x_i - m \rvert $ | $ n_i $ | Produit |
|---|---|---|---|
| 0 | 2,2833 | 5 | 11,4167 |
| 1 | 1,2833 | 12 | 15,4000 |
| 2 | 0,2833 | 18 | 5,1000 |
| 3 | 0,7167 | 14 | 10,0333 |
| 4 | 1,7167 | 8 | 13,7333 |
| 5 | 2,7167 | 3 | 8,1500 |
| **Total** | | **60** | **63,8333** |

$$ EAM = \frac{63{,}8333}{60} = \mathbf{1{,}0639} \text{ transaction} $$

**e. Par définition :** $ \sum n_i (x_i - m)^2 $ :

| $ x_i $ | $ (x_i - m)^2 $ | $ n_i $ | Produit |
|---|---|---|---|
| 0 | 5,2136 | 5 | 26,0681 |
| 1 | 1,6469 | 12 | 19,7633 |
| 2 | 0,0803 | 18 | 1,4450 |
| 3 | 0,5136 | 14 | 7,1906 |
| 4 | 2,9469 | 8 | 23,5756 |
| 5 | 7,3803 | 3 | 22,1408 |
| **Total** | | **60** | **100,1833** |

$$ V(X) = \frac{100{,}1833}{60} = \mathbf{1{,}6697} $$

**Par Koenig :** $ \sum n_i x_i^2 = 0(5) + 1(12) + 4(18) + 9(14) + 16(8) + 25(3) $
$ = 0 + 12 + 72 + 126 + 128 + 75 = 413 $.
$$ V(X) = \frac{413}{60} - \left(\frac{137}{60}\right)^2 = 6{,}8833 - 5{,}2136 = \mathbf{1{,}6697} $$
**Les deux méthodes donnent le même résultat ✔** — et Koenig a demandé **une seule
colonne supplémentaire** au lieu de deux.

$$ \sigma = \sqrt{1{,}6697} = \mathbf{1{,}2922} \text{ transaction} $$

**f.** $ CV = \dfrac{1{,}2922}{2{,}2833} = \mathbf{0{,}566} $, soit **56,6 %** : la dispersion
représente plus de la moitié du niveau moyen — l'activité du *desk* est **très irrégulière**.
Contrôle : $ EAM = 1{,}064 \le \sigma = 1{,}292 $ ✔ (l'écart-type est toujours ≥ EAM).

**g.** $ Me = 2 < m = 2{,}28 $ : la distribution est **légèrement étalée à droite**. Les
journées à 4 ou 5 transactions tirent la moyenne au-dessus de la valeur centrale, sans
déplacer la médiane. **L'écart est faible (0,28) : l'asymétrie existe mais reste modérée.**
:::

<!--saut-->

#### Exercice 2.3 — Décomposition intra / inter

Une salle de marché comprend deux *desks* :

| *Desk* | Effectif $ N_k $ | P&L moyen annuel $ m_k $ (k€) | Écart-type $ \sigma_k $ (k€) |
|---|---|---|---|
| A — *flow* | 30 | 12 | 5 |
| B — *prop* | 20 | 22 | 8 |

**a.** Calculez le P&L moyen de la salle.
**b.** Calculez $ V_{intra} $, $ V_{inter} $, puis $ \sigma^2 $ et $ \sigma $.
**c.** Quelle part de la dispersion totale l'appartenance à un *desk* explique-t-elle ?
**d.** Interprétez.

::: correction Corrigé de l'exercice 2.3
**a.** $ N = 30 + 20 = 50 $ ; poids $ 30/50 = 0{,}6 $ et $ 20/50 = 0{,}4 $.
$$ m_X = 0{,}6 \times 12 + 0{,}4 \times 22 = 7{,}2 + 8{,}8 = \mathbf{16 \text{ k€}} $$

**b.**

$$ V_{intra} = 0{,}6 \times 5^2 + 0{,}4 \times 8^2 = 0{,}6(25) + 0{,}4(64) = 15 + 25{,}6 = \mathbf{40{,}6} $$
$$ V_{inter} = 0{,}6 (12-16)^2 + 0{,}4 (22-16)^2 = 0{,}6(16) + 0{,}4(36) = 9{,}6 + 14{,}4 = \mathbf{24{,}0} $$
$$ \sigma^2 = 40{,}6 + 24{,}0 = \mathbf{64{,}6} \qquad \sigma = \sqrt{64{,}6} = \mathbf{8{,}04 \text{ k€}} $$

**c.** $ \dfrac{V_{inter}}{\sigma^2} = \dfrac{24{,}0}{64{,}6} = \mathbf{0{,}372} $, soit
**37,2 %**.

**d.** **Interprétation en trois temps.**
① L'écart-type de la salle (8,04 k€) est **supérieur à celui de chaque *desk* pris
séparément** (5 et 8) : c'est la composante **inter** qui l'explique — les deux *desks* n'ont
pas la même moyenne.
② **37,2 % de la dispersion des P&L s'explique par l'appartenance à un *desk*** ; les 62,8 %
restants sont de la variabilité **entre traders d'un même *desk***.
③ **Conséquence managériale :** connaître le *desk* d'un trader ne permet de prédire qu'un
tiers de la variabilité de son P&L. **L'essentiel se joue à l'intérieur des équipes** — un
argument contre une politique de rémunération fondée uniquement sur le *desk* d'affectation.
:::

#### Exercice 2.4 — Part de l'agrégat, Lorenz et Gini

Le patrimoine net de 1 000 ménages, réparti en **quintiles** (200 ménages par quintile) :

| Quintile | Patrimoine moyen (k€) |
|---|---|
| 1ᵉʳ (le plus modeste) | 20 |
| 2ᵉ | 60 |
| 3ᵉ | 120 |
| 4ᵉ | 200 |
| 5ᵉ (le plus aisé) | 600 |

**a.** Peut-on mesurer la concentration de cette variable ? Justifiez.
**b.** Calculez le patrimoine moyen d'ensemble.
**c.** Calculez la part de l'agrégat de chaque quintile. Contrôlez la somme.
**d.** Construisez le tableau des cumuls et calculez les pentes de la courbe de Lorenz.
**e.** Calculez l'indice de Gini.
**f.** Écrivez trois phrases de lecture.

::: correction Corrigé de l'exercice 2.4
**a.** **Oui.** La somme des patrimoines a un sens : c'est le **patrimoine total** des
1 000 ménages, une grandeur économique réelle. La condition d'additivité est remplie.

**b.** Les quintiles ont tous le même poids (0,20), donc la moyenne générale est la **moyenne
simple** des cinq moyennes :
$$ S = 20+60+120+200+600 = 1\,000 \qquad m_X = \frac{1\,000}{5} = \mathbf{200 \text{ k€}} $$

**c.** $ p_k = \dfrac{f_k m_k}{m_X} = \dfrac{0{,}20 \, m_k}{200} = \dfrac{m_k}{1\,000} $ :

| Quintile | $ m_k $ | $ p_k $ | En % |
|---|---|---|---|
| 1 | 20 | 0,02 | **2 %** |
| 2 | 60 | 0,06 | **6 %** |
| 3 | 120 | 0,12 | **12 %** |
| 4 | 200 | 0,20 | **20 %** |
| 5 | 600 | 0,60 | **60 %** |
| **Total** | 1 000 | **1,00** | **100 %** ✔ |

**d.** Cumuls et pentes $ = m_k / m_X $ :

| $ F $ (%) | Part cumulée (%) | Pente du segment | Lecture |
|---|---|---|---|
| 0 | 0,0 | — | — |
| 20 | **2,0** | $ 20/200 = 0{,}10 $ | très en dessous de la moyenne |
| 40 | **8,0** | $ 60/200 = 0{,}30 $ | en dessous |
| 60 | **20,0** | $ 120/200 = 0{,}60 $ | en dessous |
| 80 | **40,0** | $ 200/200 = \mathbf{1{,}00} $ | **exactement à la moyenne** |
| 100 | **100,0** | $ 600/200 = 3{,}00 $ | trois fois la moyenne |

**Le 4ᵉ quintile a une pente égale à 1 : son segment est parallèle à la diagonale.** L'écart
à la diagonale y est donc **constant et maximal** : à $ F = 60 $, $ 60 - 20 = 40 $ points ; à
$ F = 80 $, $ 80 - 40 = 40 $ points. **C'est la vérification directe de la propriété 3 de la
courbe de Lorenz.**

**e.** Trapèzes, tous de hauteur $ h = 20 $ (donc aire $ = (b+B) \times 10 $) :

| Tranche | $ b $ | $ B $ | Aire |
|---|---|---|---|
| 0 → 20 | 0 | 2 | $ 2 \times 10 = \mathbf{20} $ |
| 20 → 40 | 2 | 8 | $ 10 \times 10 = \mathbf{100} $ |
| 40 → 60 | 8 | 20 | $ 28 \times 10 = \mathbf{280} $ |
| 60 → 80 | 20 | 40 | $ 60 \times 10 = \mathbf{600} $ |
| 80 → 100 | 40 | 100 | $ 140 \times 10 = \mathbf{1\,400} $ |
| **Somme** | | | **2 400** |

$$ \mathcal{A} = 0{,}5 - \frac{2\,400}{10\,000} = 0{,}5 - 0{,}24 = 0{,}26 \qquad G = 2 \times 0{,}26 = \mathbf{0{,}52} $$

**Contrôle : $ 0 \le 0{,}52 \le 1 $ ✔**

**f.** ① « Les **20 %** des ménages les plus modestes détiennent **2 %** du patrimoine
total. » ② « Les **40 %** les plus modestes n'en détiennent que **8 %**, tandis que les
**20 %** les plus aisés en détiennent **60 %** — soit **30 fois plus** que le premier
quintile. » ③ « L'indice de Gini vaut **0,52** : la concentration est forte, ce qui est
caractéristique du patrimoine, bien plus concentré que le revenu. »
:::

<!--saut-->

### Niveau 3 — Maîtrise

**Ces six exercices ne se résolvent pas en appliquant une formule. Ils exigent de
comprendre pourquoi les formules sont ce qu'elles sont.**

#### Exercice 3.1 — Démontrer que $ EAM \le \sigma $

On a vérifié numériquement, à l'exercice 2.2, que l'EAM était inférieur à l'écart-type.
**Démontrez que c'est toujours vrai.**

*Indication : appliquez l'inégalité de Cauchy-Schwarz
$ \left(\sum a_i b_i\right)^2 \le \left(\sum a_i^2\right)\left(\sum b_i^2\right) $ en posant
$ a_i = \lvert x_i - m \rvert $ et $ b_i = 1 $.*

::: correction Corrigé de l'exercice 3.1
Posons $ d_i = \lvert x_i - m_X \rvert \ge 0 $. Par définition :
$$ EAM = \frac{1}{N}\sum_{i=1}^{N} d_i \qquad \sigma^2 = \frac{1}{N}\sum_{i=1}^{N} d_i^2 $$
*(car $ (x_i - m)^2 = \lvert x_i - m \rvert^2 = d_i^2 $).*

**Cauchy-Schwarz** avec $ a_i = d_i $ et $ b_i = 1 $ :
$$ \left(\sum_{i=1}^{N} d_i \times 1\right)^2 \le \left(\sum_{i=1}^{N} d_i^2\right)\left(\sum_{i=1}^{N} 1^2\right) = \left(\sum d_i^2\right) \times N $$

Or $ \sum d_i = N \times EAM $ et $ \sum d_i^2 = N \sigma^2 $. En remplaçant :
$$ (N \times EAM)^2 \le N\sigma^2 \times N \quad \Longrightarrow \quad N^2 EAM^2 \le N^2 \sigma^2 \quad \Longrightarrow \quad EAM^2 \le \sigma^2 $$

Les deux quantités étant positives, on peut prendre la racine :
$$ \boxed{\; EAM \le \sigma \;} $$

**Cas d'égalité.** Cauchy-Schwarz est une égalité si et seulement si les vecteurs
$ (d_i) $ et $ (1) $ sont **colinéaires**, c'est-à-dire si **tous les $ d_i $ sont égaux** :
tous les individus sont à la même distance de la moyenne. C'est le cas d'une série ne prenant
que **deux valeurs, symétriques autour de la moyenne et d'effectifs égaux** — par exemple
$ \{-3; -3; 3; 3\} $ : $ m = 0 $, $ EAM = 3 $, $ \sigma = 3 $.

**Interprétation.** L'écart-type est toujours **au moins aussi grand** que l'EAM parce que le
carré **pénalise davantage les grands écarts** : une observation à 10 unités de la moyenne
compte 10 fois plus qu'une observation à 1 unité dans l'EAM, mais **100 fois plus** dans la
variance. **C'est pourquoi l'écart-type est plus sensible aux valeurs extrêmes que l'EAM** —
et c'est aussi pourquoi, en gestion des risques, il sous-estime rarement le danger.

**Vérification sur l'exercice 2.2 :** $ EAM = 1{,}0639 \le \sigma = 1{,}2922 $ ✔ — le rapport
$ \sigma/EAM = 1{,}21 $.
:::

#### Exercice 3.2 — Moyenne = médiane implique-t-il la symétrie ?

On lit souvent que « si la moyenne égale la médiane, la distribution est symétrique ».
**Démontrez que c'est faux** en construisant un contre-exemple explicite.

::: correction Corrigé de l'exercice 3.2
**Contre-exemple :** la série $ \{0 \, ; \, 4 \, ; \, 5 \, ; \, 5 \, ; \, 11\} $.

**Moyenne :** $ (0+4+5+5+11)/5 = 25/5 = \mathbf{5} $.
**Médiane :** $ N = 5 $ impair, valeur de rang $ (5+1)/2 = 3 $ → série triée
$ \{0 \,;\, 4 \,;\, 5 \,;\, 5 \,;\, 11\} $ → $ Me = \mathbf{5} $.
**Donc $ m = Me = 5 $.**

**Et pourtant la série n'est pas symétrique.** Les écarts à la moyenne valent
$ -5 ; -1 ; 0 ; 0 ; +6 $. Pour une série symétrique, l'ensemble des écarts serait invariant
par changement de signe — or $ -5 $ n'a pas de contrepartie $ +5 $, et $ +6 $ pas de
contrepartie $ -6 $.

**Conclusion rigoureuse :**
- « Distribution symétrique » **⟹** « $ m = Me $ » : **vrai**.
- « $ m = Me $ » **⟹** « distribution symétrique » : **faux**. La réciproque n'est pas
  valable.
- **L'égalité $ m = Me $ est donc une condition nécessaire, pas suffisante.**

**Ce qu'il faut écrire en examen :** « L'écart entre moyenne et médiane est un **indice**
d'asymétrie, pas une **preuve** de symétrie quand il est nul. Deux asymétries opposées
peuvent se compenser. »

**Pourquoi cela compte en finance.** Une distribution de rendements peut avoir une moyenne
égale à sa médiane et rester **fortement asymétrique** : beaucoup de petits gains compensés
par quelques pertes rares mais énormes. C'est le profil de risque le plus dangereux qui soit,
et **ni la moyenne ni la médiane ne le révèlent**. Il faut regarder la **distribution
entière** — d'où les *boxplots*, les quantiles extrêmes et, plus tard, les mesures
d'asymétrie.
:::

<!--saut-->

#### Exercice 3.3 — Prime forfaitaire ou augmentation proportionnelle ?

On reprend les données de l'exercice 2.4 (patrimoines moyens par quintile : 20 · 60 · 120 ·
200 · 600 k€, $ m = 200 $, $ G = 0{,}52 $).

L'État hésite entre deux mesures :
- **Mesure A :** verser **100 k€ à chaque ménage** (forfait identique pour tous).
- **Mesure B :** augmenter **tous les patrimoines de 10 %** (mesure proportionnelle).

**a.** Calculez le nouveau Gini dans chaque cas.
**b.** Démontrez le résultat général dans chaque cas.
**c.** Que conclure ?

::: correction Corrigé de l'exercice 3.3
**a. Mesure A — le forfait de 100 k€.**

Nouvelles moyennes : 120 · 160 · 220 · 300 · 700. Total $ = 1\,500 $, donc
$ m' = 1\,500/5 = 300 $ k€.

| Quintile | $ m'_k $ | $ p'_k = m'_k/1\,500 $ | En % | Cumul |
|---|---|---|---|---|
| 1 | 120 | 0,0800 | 8,00 | **8,00** |
| 2 | 160 | 0,1067 | 10,67 | **18,67** |
| 3 | 220 | 0,1467 | 14,67 | **33,33** |
| 4 | 300 | 0,2000 | 20,00 | **53,33** |
| 5 | 700 | 0,4667 | 46,67 | **100,00** |

Trapèzes ($ h = 20 $, donc aire $ = (b+B) \times 10 $) : 80 · 266,67 · 520 · 866,67 ·
1 533,33 → **somme = 3 266,67**.
$$ \mathcal{A} = 0{,}5 - 0{,}326667 = 0{,}173333 \qquad G_A = \mathbf{0{,}347} $$
**Le Gini chute de 0,52 à 0,347, soit une baisse d'exactement un tiers.**

**Mesure B — l'augmentation de 10 %.**

Nouvelles moyennes : 22 · 66 · 132 · 220 · 660. Total $ = 1\,100 $, $ m' = 220 $ k€.
Parts : $ 22/1\,100 = 2\,\% $ · $ 66/1\,100 = 6\,\% $ · $ 132/1\,100 = 12\,\% $ ·
$ 220/1\,100 = 20\,\% $ · $ 660/1\,100 = 60\,\% $.
**Ce sont exactement les parts de départ.** La courbe de Lorenz est **identique**, donc
$$ G_B = \mathbf{0{,}52} \quad \text{— inchangé.} $$

**b. Les deux démonstrations.**

**Mesure B (proportionnelle) — le Gini est invariant d'échelle.**
Si $ x'_i = a x_i $ avec $ a > 0 $, alors $ m'_k = a m_k $ et $ m' = a m $, donc
$$ p'_k = \frac{f_k \, m'_k}{m'} = \frac{f_k \, a \, m_k}{a \, m} = \frac{f_k m_k}{m} = p_k $$
**Toutes les parts sont inchangées, donc la courbe de Lorenz et le Gini aussi.**
**Le Gini est un indicateur *relatif* : il ne voit pas les niveaux, seulement les
proportions.**

**Mesure A (forfaitaire) — le Gini est réduit dans un rapport connu.**
Si $ x'_i = x_i + c $ avec $ c > 0 $, alors $ m' = m + c $, et les **écarts entre individus
sont inchangés** : $ x'_i - x'_j = x_i - x_j $.
Or l'indice de Gini admet une écriture équivalente à sa définition géométrique :
$$ G = \frac{\Delta}{2 m} \qquad \text{avec} \qquad \Delta = \frac{1}{N^2}\sum_{i=1}^{N}\sum_{j=1}^{N} \lvert x_i - x_j \rvert $$
où $ \Delta $ est la **différence absolue moyenne** entre deux individus tirés au hasard.
Comme $ \Delta $ est inchangé et $ m $ augmenté de $ c $ :
$$ G' = \frac{\Delta}{2(m+c)} = G \times \frac{m}{m+c} $$

*Vérification numérique :* $ \Delta = 2mG = 2 \times 200 \times 0{,}52 = \mathbf{208} $.
Après la mesure : $ G' = 208/(2 \times 300) = 0{,}3467 $ ✔ — **exactement la valeur trouvée
par les trapèzes.** Et $ G \times \frac{m}{m+c} = 0{,}52 \times \frac{200}{300} = 0{,}52 \times \frac{2}{3} = 0{,}3467 $ ✔

::: piege
**La formule $ G = \Delta/(2m) $ n'est pas au programme du chapitre** — le support ne donne
que la définition géométrique. Je te la donne parce qu'elle **démontre en trois lignes** ce
que les trapèzes ne montrent que numériquement, et parce qu'elle éclaire ce que le Gini
mesure vraiment : **l'écart typique entre deux individus tirés au hasard, rapporté au niveau
moyen**. **En examen, utilise la méthode des trapèzes** — mais si tu cites cette identité en
remarque, elle vaut des points.
:::

**c. Conclusion.**
| | Effet sur le niveau moyen | Effet sur le Gini |
|---|---|---|
| **Forfait de $ c $** | $ m \to m + c $ | $ G \to G \times \frac{m}{m+c} $ — **baisse** |
| **Hausse de $ a\,\% $** | $ m \to a\,m $ | $ G \to G $ — **inchangé** |

**Une mesure forfaitaire réduit toujours les inégalités relatives ; une mesure
proportionnelle ne les modifie jamais.** C'est le fondement mathématique d'un débat de
politique économique permanent — chèque énergie forfaitaire contre baisse proportionnelle
de la TVA, augmentation générale en euros contre augmentation en pourcentage.

**Et la limite à signaler :** en valeur **absolue**, la mesure B donne 60 k€ au dernier
quintile et 2 k€ au premier — **l'écart absolu se creuse de 58 k€** alors que le Gini ne
bouge pas. **Le Gini mesure l'inégalité relative, pas l'écart absolu. Ne jamais confondre
les deux.**
:::

<!--saut-->

#### Exercice 3.4 — Deux courbes qui se croisent

Deux pays, chacun décrit par les parts de revenu de ses cinq quintiles :

| Quintile | Pays X (%) | Pays Y (%) |
|---|---|---|
| 1ᵉʳ | 10 | 2 |
| 2ᵉ | 10 | 13 |
| 3ᵉ | 10 | 20 |
| 4ᵉ | 10 | 25 |
| 5ᵉ | 60 | 40 |

**a.** Construisez les cumuls et montrez que les deux courbes de Lorenz se croisent.
**b.** Calculez les deux indices de Gini.
**c.** Calculez le rapport $ Q_5/Q_1 $ et la part du quintile supérieur dans chaque pays.
**d.** Quel pays est « le plus inégalitaire » ? Rédigez la conclusion attendue.

::: correction Corrigé de l'exercice 3.4
**a.** Cumuls :

| $ F $ (%) | Pays X | Pays Y | $ X - Y $ |
|---|---|---|---|
| 20 | 10 | 2 | **+ 8** |
| 40 | 20 | 15 | **+ 5** |
| 60 | 30 | 35 | **− 5** |
| 80 | 40 | 60 | **− 20** |
| 100 | 100 | 100 | 0 |

**Le signe de l'écart change entre 40 % et 60 % : les deux courbes se croisent.** Y est
au-dessous de X dans le bas de la distribution (donc plus inégalitaire pour les plus pauvres)
et au-dessus dans le haut (donc moins inégalitaire pour la classe moyenne supérieure).

**b.** Trapèzes ($ h = 20 $, aire $ = (b+B) \times 10 $) :

| Tranche | X | Y |
|---|---|---|
| 0 → 20 | $ (0+10)\times10 = 100 $ | $ (0+2)\times10 = 20 $ |
| 20 → 40 | $ (10+20)\times10 = 300 $ | $ (2+15)\times10 = 170 $ |
| 40 → 60 | $ (20+30)\times10 = 500 $ | $ (15+35)\times10 = 500 $ |
| 60 → 80 | $ (30+40)\times10 = 700 $ | $ (35+60)\times10 = 950 $ |
| 80 → 100 | $ (40+100)\times10 = 1\,400 $ | $ (60+100)\times10 = 1\,600 $ |
| **Somme** | **3 000** | **3 240** |

$ \mathcal{A}_X = 0{,}5 - 0{,}300 = 0{,}200 \Rightarrow G_X = \mathbf{0{,}400} $
$ \mathcal{A}_Y = 0{,}5 - 0{,}324 = 0{,}176 \Rightarrow G_Y = \mathbf{0{,}352} $
**Selon le Gini, X est plus inégalitaire que Y.**

**c.**
| Indicateur | Pays X | Pays Y | Verdict |
|---|---|---|---|
| Rapport $ Q_5/Q_1 $ | $ 60/10 = \mathbf{6{,}0} $ | $ 40/2 = \mathbf{20{,}0} $ | **Y bien plus inégalitaire** |
| Part du quintile supérieur | **60 %** | **40 %** | **X plus inégalitaire** |
| Indice de Gini | **0,400** | **0,352** | **X plus inégalitaire** |

**d. La conclusion attendue.**

> « Les deux courbes de Lorenz se croisent entre 40 % et 60 % : **il n'y a pas de dominance
> de Lorenz**, et les indicateurs ne peuvent donc pas converger mécaniquement. C'est
> précisément ce que l'on observe. Le rapport $ Q_5/Q_1 $, qui met l'accent sur les
> **extrêmes**, désigne Y comme plus inégalitaire (20 contre 6), parce que son premier
> quintile ne perçoit que 2 % du revenu. La part du quintile supérieur et l'indice de Gini,
> qui pèsent davantage la **structure d'ensemble**, désignent X (60 % contre 40 % ;
> $ G = 0{,}400 $ contre 0,352). **Les deux réponses sont exactes : elles ne mesurent pas la
> même chose.** X concentre le revenu au sommet ; Y laisse ses plus pauvres avec presque
> rien. Une réponse unique au classement des deux pays exigerait de fixer d'abord ce que
> l'on juge prioritaire — le sort des plus pauvres ou la part du sommet — ce qui est un
> **choix normatif, pas statistique**. »

**C'est cette dernière phrase qui distingue une excellente copie.** Le statisticien décrit ;
il ne tranche pas un arbitrage de valeurs sans le dire.
:::

<!--saut-->

#### Exercice 3.5 — Volatilité, annualisation et Bienaymé-Tchebychev

Les rendements mensuels d'un fonds sur douze mois, en pourcentage :

```
+2,1   -1,4   +3,2   +0,8   -2,6   +4,1
+1,5   -0,7   +2,9   -3,1   +1,8   +2,4
```

**a.** Calculez le rendement moyen mensuel.
**b.** Calculez la variance (par Koenig) et l'écart-type mensuel.
**c.** Annualisez le rendement et la volatilité. *(Rappel : la volatilité s'annualise en
multipliant par $ \sqrt{12} $ pour des données mensuelles.)*
**d.** Calculez le coefficient de variation et le rapport $ m/\sigma $ annualisé.
**e.** Appliquez Bienaymé-Tchebychev avec $ k = 2 $, puis confrontez la borne aux données
observées. Que constatez-vous ?

::: correction Corrigé de l'exercice 3.5
**a.** $ \sum x_i = 2{,}1 - 1{,}4 + 3{,}2 + 0{,}8 - 2{,}6 + 4{,}1 + 1{,}5 - 0{,}7 + 2{,}9 - 3{,}1 + 1{,}8 + 2{,}4 = \mathbf{11{,}0} $
$$ m = \frac{11{,}0}{12} = \mathbf{0{,}9167\,\%} \text{ par mois} $$

**b.** $ \sum x_i^2 = 4{,}41 + 1{,}96 + 10{,}24 + 0{,}64 + 6{,}76 + 16{,}81 + 2{,}25 + 0{,}49 + 8{,}41 + 9{,}61 + 3{,}24 + 5{,}76 = \mathbf{70{,}58} $

$$ V = \frac{70{,}58}{12} - (0{,}9167)^2 = 5{,}8817 - 0{,}8403 = \mathbf{5{,}0414} $$
$$ \sigma = \sqrt{5{,}0414} = \mathbf{2{,}2453\,\%} \text{ par mois} $$

**c.** Rendement annualisé (somme des douze mois, approximation additive) :
$ 12 \times 0{,}9167 = \mathbf{11{,}0\,\%} $.
Volatilité annualisée : $ \sigma_{an} = 2{,}2453 \times \sqrt{12} = 2{,}2453 \times 3{,}4641 = \mathbf{7{,}78\,\%} $.

::: piege
**Pourquoi $ \sqrt{12} $ et non 12 ?** Parce que **les variances s'additionnent, pas les
écarts-types** — c'est la propriété $ V(aX) = a^2V(X) $ appliquée à une somme de mois
indépendants : $ V_{an} = 12 \, V_{mens} $, donc
$ \sigma_{an} = \sqrt{12}\,\sigma_{mens} $. **C'est exactement le « moyen » annoncé par la
diapositive 49 du support : la volatilité ne s'agrège pas linéairement.**
*(L'hypothèse d'indépendance des rendements mensuels est une convention de marché ; elle est
approximative mais universellement utilisée.)*
:::

**d.** $ CV = \dfrac{2{,}2453}{0{,}9167} = \mathbf{2{,}449} $ — **la dispersion vaut près de
2,5 fois le rendement moyen mensuel.**
Rapport $ m/\sigma $ mensuel $ = 0{,}4083 $ ; annualisé
$ = 0{,}4083 \times \sqrt{12} = \mathbf{1{,}414} $.
**Lecture :** ce rapport est la structure du **ratio de Sharpe** (sans taux sans risque). Une
valeur de 1,41 est bonne. **Et le CV en est l'inverse** : $ 1/2{,}449 = 0{,}408 $ ✔ —
la même information, lue à l'envers.

**e.** Avec $ k = 2 $ : Bienaymé-Tchebychev garantit que **au moins $ 1 - 1/4 = 75\,\% $** des
observations se trouvent dans l'intervalle
$$ [\, m - 2\sigma \; ; \; m + 2\sigma \,] = [\, 0{,}9167 - 4{,}4906 \; ; \; 0{,}9167 + 4{,}4906 \,] = [\, -3{,}57\,\% \; ; \; +4{,}41\,\% \,] $$

**Confrontation aux données :** le minimum observé est $ -3{,}1 $ et le maximum $ +4{,}1 $ —
**les douze mois, soit 100 %, sont dans l'intervalle.**

**Ce qu'il faut constater et écrire :** « La borne garantit 75 % ; on observe 100 %.
L'inégalité est donc **très lâche**, ce qui est normal : elle est valable **quelle que soit
la loi** de la variable, y compris pour les distributions les plus défavorables. Son intérêt
n'est pas la précision mais l'**universalité** — elle donne une garantie sans rien supposer.
Si l'on acceptait l'hypothèse de normalité, l'intervalle à $ \pm 2\sigma $ contiendrait
environ 95 % des observations, ce qui serait bien plus informatif mais reposerait sur une
hypothèse invérifiable sur douze points. »

**En gestion des risques, c'est exactement l'arbitrage quotidien :** une borne robuste et
large, ou une borne étroite qui suppose une loi que le marché ne respecte pas dans les
crises.
:::

#### Exercice 3.6 — Que peut-on agréger ?

Une administration publie, pour chacune des trois régions d'un territoire, le tableau
suivant :

| Région | Effectif $ N_k $ | Revenu moyen $ m_k $ | Revenu médian | Écart-type $ \sigma_k $ | Gini $ G_k $ |
|---|---|---|---|---|---|
| A | 400 | 24 000 | 21 000 | 9 000 | 0,28 |
| B | 350 | 31 000 | 27 500 | 14 000 | 0,33 |
| C | 250 | 19 000 | 18 000 | 6 000 | 0,22 |

**Pour chacune des quatre grandeurs, dites si l'on peut calculer la valeur d'ensemble à
partir de ce tableau seul. Si oui, calculez-la. Si non, expliquez précisément ce qui manque.**

::: correction Corrigé de l'exercice 3.6
$ N = 400 + 350 + 250 = 1\,000 $ ; poids $ 0{,}40 $ · $ 0{,}35 $ · $ 0{,}25 $.

**① Le revenu moyen — OUI, calculable.** La moyenne est un opérateur linéaire :
$$ m = 0{,}40(24\,000) + 0{,}35(31\,000) + 0{,}25(19\,000) = 9\,600 + 10\,850 + 4\,750 = \mathbf{25\,200 \text{ €}} $$

**② Le revenu médian — NON.** La médiane **ne s'agrège pas**, quels que soient les poids
(§ 2.1.15). Elle dépend de la **position relative de toutes les observations**, information
détruite par le résumé en trois médianes. **Ce qu'il faudrait : les distributions complètes**
(ou au moins les fonctions de répartition) des trois régions, pour reconstituer la
distribution d'ensemble puis y chercher le rang médian.
*(On peut seulement encadrer : la médiane d'ensemble est comprise entre 18 000 et 27 500 €.)*

**③ L'écart-type — OUI, calculable, via la décomposition intra / inter.**

$$ V_{intra} = 0{,}40(9\,000)^2 + 0{,}35(14\,000)^2 + 0{,}25(6\,000)^2 $$
$ = 0{,}40 \times 81 \times 10^6 + 0{,}35 \times 196 \times 10^6 + 0{,}25 \times 36 \times 10^6 $
$ = 32{,}4 \times 10^6 + 68{,}6 \times 10^6 + 9{,}0 \times 10^6 = \mathbf{110{,}0 \times 10^6} $

Écarts des moyennes à 25 200 : $ -1\,200 $ · $ +5\,800 $ · $ -6\,200 $.
$$ V_{inter} = 0{,}40(1\,200)^2 + 0{,}35(5\,800)^2 + 0{,}25(6\,200)^2 $$
$ = 0{,}40 \times 1{,}44 \times 10^6 + 0{,}35 \times 33{,}64 \times 10^6 + 0{,}25 \times 38{,}44 \times 10^6 $
$ = 0{,}576 \times 10^6 + 11{,}774 \times 10^6 + 9{,}610 \times 10^6 = \mathbf{21{,}96 \times 10^6} $

$$ \sigma^2 = 110{,}0 \times 10^6 + 21{,}96 \times 10^6 = 131{,}96 \times 10^6 \qquad \sigma = \mathbf{11\,487 \text{ €}} $$

**Remarque à faire :** $ V_{inter}/\sigma^2 = 21{,}96/131{,}96 = \mathbf{16{,}6\,\%} $ — la
région d'appartenance n'explique qu'un sixième de la dispersion des revenus. **L'essentiel
des inégalités est intra-régional.**

**④ Le Gini d'ensemble — NON.** Comme la médiane, le Gini repose sur le **classement de tous
les individus** : la courbe de Lorenz d'ensemble exige de fusionner les trois populations et
de les réordonner. Trois indices régionaux n'y suffisent pas.
**Ce qu'il faudrait :** les distributions complètes, ou au minimum les parts de l'agrégat par
quantile de chaque région **plus** les masses de revenu régionales.
**Et un raisonnement à connaître :** le Gini d'ensemble est **supérieur** à la moyenne
pondérée des Gini régionaux, parce qu'à l'inégalité interne de chaque région s'ajoute
l'inégalité **entre** régions — même mécanique que la composante inter de la variance.

::: synthese La règle générale à retenir
| Grandeur | S'agrège ? | Pourquoi |
|---|---|---|
| Somme, effectif | **Oui** | Additivité directe |
| Moyenne | **Oui** (pondérée) | Opérateur **linéaire** |
| Variance, écart-type | **Oui** | Via **Koenig** ou intra/inter — deux nombres par groupe suffisent |
| Médiane, quantiles | **Non** | Dépendent du **rang**, pas de la valeur |
| Gini, courbe de Lorenz | **Non** | Dépendent du **classement complet** de la population |
| Mode | **Non** | Le mode d'ensemble peut n'être le mode d'aucun groupe |
**Le critère unificateur : ce qui repose sur des sommes s'agrège ; ce qui repose sur des rangs
ne s'agrège pas.**
:::
:::

<!--saut-->

### Niveau 4 — Simulation d'examen

::: methode Conditions de passation
**Le support ne donne aucune indication sur le format ni sur la durée de l'épreuve.** La
simulation retient le format le plus courant pour un chapitre de cette densité : **2 heures**,
sur **20 points**, **calculatrice autorisée, documents interdits**. Ce chapitre étant plus
lourd que le chapitre 1 (trois familles d'indicateurs, plusieurs démonstrations), la durée
retenue est supérieure aux 1 h 30 du chapitre précédent. **Ajuste ces paramètres dès que les
modalités réelles seront annoncées.**

Chronomètre lancé. **Répartition du temps conseillée :** 25 min pour la partie A, 45 min pour
la partie B, 30 min pour la partie C, 15 min pour la partie D, **5 min de relecture** — et la
relecture n'est pas optionnelle : c'est là que se rattrapent les erreurs d'unité et de somme.
:::

#### Sujet

**PARTIE A — Questions de cours (5 points)**

**A.1** *(1,5 pt)* Énoncez la propriété « la somme des écarts à la moyenne est nulle » et
démontrez-la. Expliquez en deux phrases pourquoi cette propriété **oblige** à construire les
indicateurs de dispersion à partir de valeurs absolues ou de carrés.

**A.2** *(1,5 pt)* Énoncez la formule de Koenig. Démontrez, à partir d'elle, que
$ \overline{x^2} \ge (\overline{x})^2 $. Expliquez en une phrase pourquoi cette formule rend
possible l'agrégation des variances.

**A.3** *(1 pt)* Un étudiant calcule l'indice de Gini de la variable « note obtenue au
partiel » sur les 1 200 étudiants de la promotion. Le calcul aboutit à $ G = 0{,}14 $.
Commentez.

**A.4** *(1 pt)* Deux courbes de Lorenz se croisent. Peut-on conclure que l'une des deux
distributions est plus inégalitaire que l'autre ? Justifiez.

**PARTIE B — Position et dispersion (7 points)**

Les salaires mensuels nets des 200 salariés d'une PME se répartissent ainsi :

| Salaire mensuel net (€) | Effectif |
|---|---|
| [1 200 ; 1 600[ | 40 |
| [1 600 ; 2 000[ | 50 |
| [2 000 ; 2 800[ | 60 |
| [2 800 ; 4 400[ | 50 |
| **Total** | **200** |

**B.1** *(1 pt)* Déterminez la classe modale. Justifiez votre méthode.

**B.2** *(1 pt)* Calculez le salaire moyen. Précisez l'hypothèse que vous utilisez.

**B.3** *(1,5 pt)* Calculez la médiane par interpolation linéaire.

**B.4** *(1,5 pt)* Calculez $ Q_1 $ et $ Q_3 $, puis l'écart inter-quartile.

**B.5** *(1,5 pt)* Calculez la variance et l'écart-type.

**B.6** *(0,5 pt)* Calculez le coefficient de variation et commentez la forme de la
distribution en une phrase argumentée.

**PARTIE C — Concentration (5 points)**

On s'intéresse maintenant au partage de la **masse salariale** de cette même PME.

**C.1** *(0,5 pt)* Justifiez qu'il est légitime de mesurer la concentration de cette variable.

**C.2** *(1,5 pt)* Calculez la part de la masse salariale détenue par chaque classe. Arrondissez
au dixième et contrôlez la somme.

**C.3** *(1 pt)* Construisez le tableau des cumuls nécessaire à la courbe de Lorenz.
**Attention aux hauteurs de tranche.**

**C.4** *(1,5 pt)* Calculez l'indice de Gini.

**C.5** *(0,5 pt)* Rédigez deux phrases d'interprétation.

**PARTIE D — Application (3 points)**

Les rendements mensuels d'un fonds sur six mois, en pourcentage :

```
+3,2   -1,8   +2,4   +0,6   -2,2   +1,8
```

**D.1** *(1 pt)* Calculez le rendement moyen mensuel et l'écart-type mensuel (par Koenig).

**D.2** *(1 pt)* Annualisez les deux grandeurs. Justifiez le facteur d'annualisation de la
volatilité par une propriété du cours.

**D.3** *(1 pt)* Un gérant affirme : « La volatilité annuelle est de 7 %, donc le fonds ne
peut pas perdre plus de 7 % sur une année. » Réfutez cette affirmation en mobilisant
précisément le cours.

<!--saut-->

#### Corrigé — copie de major, avec barème détaillé

::: correction PARTIE A (5 points)
**A.1** *(1,5 pt)*

> **Énoncé** *(0,5 pt)* : pour toute série $ (x_1, \dots, x_N) $ de moyenne $ m_X $,
> $ \sum_{i=1}^{N}(x_i - m_X) = 0 $.
>
> **Démonstration** *(0,5 pt)* : par linéarité de la somme,
> $ \sum_{i=1}^{N}(x_i - m_X) = \sum_{i=1}^{N} x_i - N m_X $. Or, par définition de la
> moyenne, $ m_X = \frac{1}{N}\sum x_i $, donc $ \sum x_i = N m_X $. D'où
> $ \sum (x_i - m_X) = N m_X - N m_X = 0 $.
>
> **Conséquence** *(0,5 pt)* : un indicateur de dispersion défini comme la moyenne des écarts
> à la moyenne vaudrait donc **0 pour toute distribution**, y compris la plus dispersée — il
> ne mesurerait rien. Il faut donc **supprimer les signes** avant de moyenner : soit par la
> valeur absolue (écart absolu moyen), soit par le carré (variance), le carré ayant l'avantage
> décisif d'être **dérivable partout**.

**A.2** *(1,5 pt)*

> **Énoncé** *(0,5 pt)* : $ V(X) = \frac{1}{N}\sum_{i=1}^{N} x_i^2 - m_X^2 $, soit « la
> moyenne des carrés moins le carré de la moyenne ».
>
> **Démonstration de l'inégalité** *(0,5 pt)* : la variance est une moyenne de carrés, donc
> $ V(X) \ge 0 $. En reportant dans Koenig :
> $ \overline{x^2} - (\overline{x})^2 \ge 0 $, donc $ \overline{x^2} \ge (\overline{x})^2 $.
> **L'égalité a lieu si et seulement si $ V(X) = 0 $**, c'est-à-dire si tous les $ x_i $ sont
> égaux.
>
> **Agrégation** *(0,5 pt)* : Koenig ne fait intervenir que $ \sum x_i $ et $ \sum x_i^2 $ ;
> il suffit donc de **transmettre deux nombres par groupe** (plus son effectif) pour
> reconstituer la variance de l'ensemble, sans jamais revenir aux données individuelles.

**A.3** *(1 pt)*

> Le calcul est **numériquement possible mais dépourvu de sens** *(0,5 pt)*. La mesure de
> concentration porte sur la répartition de la **somme** de la variable ; elle exige donc que
> cette somme désigne un objet réel. Or **la somme des notes de 1 200 étudiants ne correspond
> à aucune grandeur** : ce n'est pas un stock que l'on se partagerait. La note est une variable
> quantitative, mais **non extensive** *(0,5 pt)*.
>
> **Ce qu'il fallait faire** : mesurer la **dispersion** des notes (écart-type, écarts
> inter-quartiles), qui elle est parfaitement définie, et non leur concentration.

**A.4** *(1 pt)*

> **Non, pas de manière univoque** *(0,5 pt)*. Le croisement signifie que l'une des
> distributions est plus inégalitaire dans le **bas** de la distribution et l'autre dans le
> **haut**. Il n'y a donc **pas de dominance de Lorenz**, et le classement dépend du poids que
> l'indicateur choisi accorde à chaque zone : le rapport $ D_9/D_1 $ privilégie les extrêmes,
> l'indice de Gini la structure d'ensemble *(0,5 pt)*.
>
> **Deux indicateurs peuvent donc classer les deux distributions en sens opposé, sans que
> l'un des deux soit faux.** La réponse consiste à décrire les deux phénomènes, et à préciser
> que trancher exigerait un **critère normatif** extérieur à la statistique.
:::

<!--saut-->

::: correction PARTIE B (7 points)
**B.1 — Classe modale** *(1 pt)*

> Les classes ayant des **amplitudes inégales**, la classe modale est celle de **densité
> maximale**, et non d'effectif maximal *(0,25 pt pour l'avoir dit)*. On rapporte chaque
> effectif à une amplitude de référence de **400 €** :
>
> | Classe | $ n_i $ | $ a_i $ (€) | $ d_i $ (effectif par tranche de 400 €) |
> |---|---|---|---|
> | [1 200 ; 1 600[ | 40 | 400 | $ 40 \times \frac{400}{400} = \mathbf{40{,}0} $ |
> | [1 600 ; 2 000[ | 50 | 400 | $ \mathbf{50{,}0} $ |
> | [2 000 ; 2 800[ | 60 | 800 | $ 60 \times \frac{400}{800} = \mathbf{30{,}0} $ |
> | [2 800 ; 4 400[ | 50 | 1 600 | $ 50 \times \frac{400}{1\,600} = \mathbf{12{,}5} $ |
>
> **La classe modale est [1 600 ; 2 000[** *(0,5 pt)*, de densité 50, **alors que l'effectif
> maximal est celui de [2 000 ; 2 800[** (60 salariés) *(0,25 pt pour la remarque)*. Cette
> dernière ne doit son effectif qu'à une amplitude deux fois plus grande.

**B.2 — Salaire moyen** *(1 pt)*

> **Hypothèse** *(0,25 pt)* : les salariés sont supposés **uniformément répartis à l'intérieur
> de chaque classe** ; on retient donc le **centre de classe** comme valeur représentative.
>
> | Classe | Centre $ c_i $ | $ n_i $ | $ f_i $ | $ f_i c_i $ |
> |---|---|---|---|---|
> | [1 200 ; 1 600[ | 1 400 | 40 | 0,20 | 280 |
> | [1 600 ; 2 000[ | 1 800 | 50 | 0,25 | 450 |
> | [2 000 ; 2 800[ | 2 400 | 60 | 0,30 | 720 |
> | [2 800 ; 4 400[ | 3 600 | 50 | 0,25 | 900 |
> | **Total** | | **200** | **1,00** | **2 350** |
>
> $$ m_X = \sum f_i c_i = \mathbf{2\,350 \text{ €}} \quad (0{,}75 \text{ pt}) $$

**B.3 — Médiane** *(1,5 pt)*

> Fréquences cumulées *(0,5 pt)* : 0,20 · 0,45 · **0,75** · 1,00.
> La médiane est la valeur telle que $ F(Me) = 0{,}50 $. Elle se situe donc dans la classe
> **[2 000 ; 2 800[**, où $ F $ passe de 0,45 à 0,75 *(0,25 pt)*.
>
> Interpolation linéaire *(0,75 pt)* :
> $$ Me = 2\,000 + 800 \times \frac{0{,}50 - 0{,}45}{0{,}75 - 0{,}45} = 2\,000 + 800 \times \frac{0{,}05}{0{,}30} = 2\,000 + 133{,}33 = \mathbf{2\,133{,}3 \text{ €}} $$
>
> **Contrôle : $ 2\,000 \le 2\,133{,}3 < 2\,800 $ ✔** — la médiane appartient bien à sa classe.

**B.4 — Quartiles** *(1,5 pt)*

> $ Q_1 $ : $ F = 0{,}25 $ tombe dans **[1 600 ; 2 000[** (F passe de 0,20 à 0,45).
> $$ Q_1 = 1\,600 + 400 \times \frac{0{,}25 - 0{,}20}{0{,}45 - 0{,}20} = 1\,600 + 400 \times 0{,}20 = \mathbf{1\,680 \text{ €}} \quad (0{,}5 \text{ pt}) $$
>
> $ Q_3 $ : $ F(2\,800) = 0{,}75 $ **exactement** — aucune interpolation n'est nécessaire.
> $$ Q_3 = \mathbf{2\,800 \text{ €}} \quad (0{,}5 \text{ pt, dont } 0{,}25 \text{ pour avoir vu que la borne est atteinte pile}) $$
>
> **Écart inter-quartile** $ = 2\,800 - 1\,680 = \mathbf{1\,120 \text{ €}} $ *(0,5 pt)*.
> **Lecture : les 50 % de salariés situés au centre de la distribution sont répartis sur une
> plage de 1 120 €.**

**B.5 — Variance et écart-type** *(1,5 pt)*

> **Par la formule de définition** *(1 pt)* :
>
> | $ c_i $ | $ c_i - m $ | $ (c_i - m)^2 $ | $ f_i $ | $ f_i (c_i - m)^2 $ |
> |---|---|---|---|---|
> | 1 400 | − 950 | 902 500 | 0,20 | 180 500 |
> | 1 800 | − 550 | 302 500 | 0,25 | 75 625 |
> | 2 400 | + 50 | 2 500 | 0,30 | 750 |
> | 3 600 | + 1 250 | 1 562 500 | 0,25 | 390 625 |
> | **Total** | | | **1,00** | **647 500** |
>
> $$ V(X) = \mathbf{647\,500 \text{ €}^2} $$
>
> **Vérification par Koenig** *(bonus de rigueur)* :
> $ \sum f_i c_i^2 = 0{,}20(1\,960\,000) + 0{,}25(3\,240\,000) + 0{,}30(5\,760\,000) + 0{,}25(12\,960\,000) $
> $ = 392\,000 + 810\,000 + 1\,728\,000 + 3\,240\,000 = 6\,170\,000 $ ;
> $ m^2 = 2\,350^2 = 5\,522\,500 $ ;
> $ V = 6\,170\,000 - 5\,522\,500 = 647\,500 $ ✔
>
> $$ \sigma = \sqrt{647\,500} = \mathbf{804{,}7 \text{ €}} \quad (0{,}5 \text{ pt}) $$
>
> **⚠ Ne jamais s'arrêter à la variance : 647 500 « euros au carré » ne s'interprète pas.**

**B.6 — Coefficient de variation et commentaire** *(0,5 pt)*

> $$ CV = \frac{804{,}7}{2\,350} = \mathbf{0{,}342} \quad \text{soit } 34{,}2\,\% $$
>
> **Commentaire attendu :** « La dispersion représente 34 % du salaire moyen : l'éventail
> salarial est **modérément ouvert**. Surtout, $ Me = 2\,133 \text{ €} < m = 2\,350 \text{ €} $ :
> la distribution est **étalée vers la droite**. Une minorité de salaires élevés — la classe
> [2 800 ; 4 400[ regroupe un quart des salariés sur une amplitude quatre fois supérieure à
> celle de la première classe — tire la moyenne au-dessus de la valeur centrale. **La médiane
> décrit donc mieux le salarié typique que la moyenne.** »
:::

<!--saut-->

::: correction PARTIE C (5 points)
**C.1 — Légitimité** *(0,5 pt)*

> La somme des salaires a un sens économique précis : c'est la **masse salariale** de la PME,
> montant qu'elle verse effectivement chaque mois. La variable est **extensive et additive** :
> la mesure de concentration est donc légitime. *(À l'inverse, une concentration d'âges ou de
> notes n'aurait pas de sens.)*

**C.2 — Parts de la masse salariale** *(1,5 pt)*

> $ p_k = \dfrac{f_k c_k}{m_X} $, avec $ m_X = 2\,350 $ € — les produits $ f_k c_k $ ont déjà
> été calculés en B.2.
>
> | Classe | $ f_k c_k $ | $ p_k = f_k c_k / 2\,350 $ | En % (arrondi) |
> |---|---|---|---|
> | [1 200 ; 1 600[ | 280 | 0,11915 | **11,9** |
> | [1 600 ; 2 000[ | 450 | 0,19149 | **19,1** |
> | [2 000 ; 2 800[ | 720 | 0,30638 | **30,6** |
> | [2 800 ; 4 400[ | 900 | 0,38298 | **38,3** |
> | **Total** | **2 350** | **1,00000** | **99,9** ⚠ |
>
> **Contrôle et remarque attendue** *(0,25 pt)* : la somme des parts **exactes** vaut
> exactement 100 %, mais la somme des parts **arrondies au dixième** vaut 99,9 %. **Il s'agit
> d'un écart d'arrondi, non d'une erreur** : chacune des quatre valeurs a été arrondie vers le
> bas. Je poursuis avec les valeurs arrondies en signalant que le résultat final en sera
> affecté à la troisième décimale.

**C.3 — Tableau des cumuls** *(1 pt)*

> ⚠ **Les classes n'ont pas la même fréquence** : les hauteurs de tranche ne sont donc **pas**
> toutes égales à 20 comme dans le cas des quintiles *(0,25 pt pour l'avoir repéré)*.
>
> | Classe | $ f_k $ (%) | Cumul de population (%) | $ p_k $ (%) | Cumul de masse (%) |
> |---|---|---|---|---|
> | [1 200 ; 1 600[ | 20 | **20** | 11,9 | **11,9** |
> | [1 600 ; 2 000[ | 25 | **45** | 19,1 | **31,0** |
> | [2 000 ; 2 800[ | 30 | **75** | 30,6 | **61,6** |
> | [2 800 ; 4 400[ | 25 | **100** | 38,3 | **99,9 → 100,0** |
>
> **Hauteurs de tranche : $ h_1 = 20 $, $ h_2 = 25 $, $ h_3 = 30 $, $ h_4 = 25 $**
> *(0,75 pt)*. Leur somme fait bien 100 ✔

**C.4 — Indice de Gini** *(1,5 pt)*

> | Tranche | $ b $ | $ B $ | $ h $ | Aire $ = (b+B)h/2 $ |
> |---|---|---|---|---|
> | 0 → 20 | 0,0 | 11,9 | 20 | $ 11{,}9 \times 10 = \mathbf{119{,}00} $ |
> | 20 → 45 | 11,9 | 31,0 | 25 | $ 42{,}9 \times 12{,}5 = \mathbf{536{,}25} $ |
> | 45 → 75 | 31,0 | 61,6 | 30 | $ 92{,}6 \times 15 = \mathbf{1\,389{,}00} $ |
> | 75 → 100 | 61,6 | 100,0 | 25 | $ 161{,}6 \times 12{,}5 = \mathbf{2\,020{,}00} $ |
> | **Somme** | | | **100** | **4 064,25** |
>
> **Conversion d'unité** *(0,5 pt — c'est le point le plus souvent perdu)* : les cumuls étant
> exprimés en pourcentages, le carré de référence vaut $ 100 \times 100 = 10\,000 $ :
> $$ \mathcal{A} = 0{,}5 - \frac{4\,064{,}25}{10\,000} = 0{,}5 - 0{,}406425 = 0{,}093575 $$
> $$ G = 2 \times 0{,}093575 = \mathbf{0{,}187} \quad (0{,}5 \text{ pt}) $$
>
> **Contrôles** *(0,5 pt)* : $ 0 \le 0{,}187 \le 1 $ ✔ ; la somme des hauteurs fait 100 ✔.
> *(Avec les parts non arrondies, on obtiendrait 0,186 : l'écart d'arrondi annoncé en C.2
> affecte bien la troisième décimale, sans conséquence sur l'interprétation.)*

**C.5 — Interprétation** *(0,5 pt)*

> ① « Les **20 %** de salariés les moins payés perçoivent **11,9 %** de la masse salariale,
> tandis que les **25 %** les mieux payés en perçoivent **38,3 %** — soit un rapport de
> **3,2 pour 1**. »
> ② « L'indice de Gini vaut **0,187**, valeur **faible** : la masse salariale de cette PME est
> peu concentrée. C'est cohérent avec un coefficient de variation modéré (34 %) et avec
> l'absence de très hauts salaires — la distribution est bornée à 4 400 €. **Cette
> concentration est bien inférieure à celle observée sur l'ensemble des salaires français
> (G = 0,356 en 2021)**, ce qui s'explique par l'homogénéité d'une population d'entreprise
> unique. »
:::

<!--saut-->

::: correction PARTIE D (3 points)
**D.1 — Moyenne et écart-type mensuels** *(1 pt)*

> $ \sum x_i = 3{,}2 - 1{,}8 + 2{,}4 + 0{,}6 - 2{,}2 + 1{,}8 = \mathbf{4{,}0} $
> $$ m = \frac{4{,}0}{6} = \mathbf{0{,}667\,\%} \text{ par mois} \quad (0{,}25 \text{ pt}) $$
>
> $ \sum x_i^2 = 10{,}24 + 3{,}24 + 5{,}76 + 0{,}36 + 4{,}84 + 3{,}24 = \mathbf{27{,}68} $
> $$ V = \frac{27{,}68}{6} - (0{,}667)^2 = 4{,}6133 - 0{,}4444 = \mathbf{4{,}1689} \quad (0{,}5 \text{ pt}) $$
> $$ \sigma = \sqrt{4{,}1689} = \mathbf{2{,}042\,\%} \text{ par mois} \quad (0{,}25 \text{ pt}) $$

**D.2 — Annualisation** *(1 pt)*

> **Rendement** *(0,25 pt)* : $ 12 \times 0{,}667 = \mathbf{8{,}0\,\%} $ par an (approximation
> additive, usuelle pour de petits rendements).
>
> **Volatilité** *(0,25 pt)* : $ \sigma_{an} = 2{,}042 \times \sqrt{12} = 2{,}042 \times 3{,}464 = \mathbf{7{,}07\,\%} $.
>
> **Justification** *(0,5 pt)* : la propriété $ V(aX) = a^2 V(X) $ montre que **les variances,
> et non les écarts-types, se cumulent**. Le rendement annuel étant la somme de douze
> rendements mensuels supposés indépendants, sa variance vaut $ 12 \, V_{mens} $, donc son
> écart-type vaut $ \sqrt{12}\,\sigma_{mens} $. **Multiplier l'écart-type par 12 reviendrait à
> confondre la variance et l'écart-type — c'est l'erreur exacte que la propriété interdit.**

**D.3 — Réfutation** *(1 pt)*

> **L'affirmation est fausse pour trois raisons distinctes, à énoncer séparément.**
>
> **① L'écart-type n'est pas une borne, c'est une moyenne.** *(0,4 pt)* La volatilité mesure
> l'écart **typique** des rendements à leur moyenne, pas leur écart **maximal**. Rien dans sa
> définition n'interdit une réalisation à $ -3\sigma $ ou $ -5\sigma $.
>
> **② Le seul résultat du cours qui borne les écarts est l'inégalité de Bienaymé-Tchebychev —
> et c'est une borne de *probabilité*, pas de *valeur*.** *(0,4 pt)* Elle affirme
> $ P(\lvert X - m \rvert \ge k\sigma) \le 1/k^2 $ pour $ k > 1 $ : avec $ k = 3 $, au plus
> 11 % des observations s'écartent de plus de $ 3\sigma $ — soit ici plus de 21 points de
> rendement. **Elle autorise donc explicitement des pertes très supérieures à 7 %.**
>
> **③ La perte maximale n'est pas bornée par la volatilité mais par la nature de l'actif.**
> *(0,2 pt)* Pour un fonds sans effet de levier, la perte maximale est de 100 % ; avec levier,
> elle peut la dépasser. La volatilité est **muette** sur ce point.
>
> **La formulation correcte** serait : « La volatilité annuelle est de 7,07 %. Sous hypothèse
> de normalité — non vérifiée ici sur six observations —, environ deux tiers des années
> auraient un rendement dans un intervalle de $ \pm 7 $ points autour de 8 %. Sans cette
> hypothèse, Bienaymé-Tchebychev garantit seulement qu'au plus 25 % des années s'écartent de
> plus de deux volatilités, soit plus de 14 points. »
:::

::: examen Grille de notation et seuils
| Partie | Points | Ce qui est vérifié |
|---|---|---|
| A — Cours | 5 | Les démonstrations, et la capacité à **refuser un calcul illégitime** (A.3) |
| B — Position et dispersion | 7 | La densité, l'interpolation, la variance **jusqu'à l'écart-type**, le diagnostic d'asymétrie |
| C — Concentration | 5 | Les parts, **les hauteurs de tranche inégales**, la conversion d'unité du Gini |
| D — Application | 3 | L'annualisation en $ \sqrt{12} $ et la distinction borne / moyenne |
| **Total** | **20** | |

**Les cinq points qui font basculer une copie :**
① avoir calculé les **densités** en B.1 au lieu de lire l'effectif maximal ;
② avoir poussé jusqu'à l'**écart-type** en B.5 ;
③ avoir vu que les **hauteurs de tranche sont inégales** en C.3 ;
④ avoir **divisé par 10 000** en C.4 ;
⑤ avoir refusé le calcul du Gini sur des notes en A.3.

**Barème d'auto-évaluation :** moins de 10 → reprends la partie 2 en entier. Entre 10 et 13 →
tu maîtrises les calculs mais pas les justifications : reprends les encadrés **Démonstration**.
Entre 14 et 17 → niveau solide ; travaille les **Points de vigilance** (§ 3). Au-dessus de
17 → **c'est le niveau attendu pour viser les 3 % de tête**. Maintiens-le par le protocole
de révision du § 6.3.
:::

<!--saut-->

## 6. Auto-évaluation finale

### 6.1 — Liste de contrôle

> Si l'une de ces questions reste sans réponse **sans regarder le document**, le chapitre
> n'est pas maîtrisé.

- [ ] J'explique la différence de nature entre « présenter » et « résumer », et je nomme les
      trois familles d'indicateurs avec leur question propre.
- [ ] Je définis le mode et j'explique pourquoi il faut parler de **classe modale** pour une
      variable continue.
- [ ] Je calcule une densité, je détermine une classe modale à amplitudes inégales, et
      j'explique en une phrase pourquoi l'effectif maximal ne suffit pas.
- [ ] Je démontre que **l'aire d'un rectangle d'histogramme est l'effectif** de sa classe.
- [ ] J'écris les **trois** formules de la moyenne et je dis dans quel cas chacune s'emploie.
- [ ] Je démontre que la somme des écarts à la moyenne est nulle et j'en tire la
      justification de l'EAM et de la variance.
- [ ] J'énonce la linéarité de la moyenne et j'explique pourquoi elle autorise l'agrégation.
- [ ] Je calcule une médiane sur données brutes (cas pair **et** impair) et sur une
      distribution par interpolation linéaire.
- [ ] Je démontre par un contre-exemple que **la médiane ne s'agrège pas**.
- [ ] Je déduis l'asymétrie d'une distribution de la comparaison entre médiane et moyenne,
      **et je sais que la réciproque est fausse**.
- [ ] Je définis un quantile comme **l'inverse de la fonction de répartition** et j'interpole
      un quantile dans une classe.
- [ ] Je cite les trois écarts inter-quantiles et je construis un *boxplot*.
- [ ] J'écris l'EAM, la variance et l'écart-type, et j'explique pourquoi on **ne s'arrête
      jamais à la variance**.
- [ ] J'énonce Koenig, je la démontre utile pour l'agrégation, et je l'applique sans erreur
      de signe.
- [ ] Je donne les **trois propriétés de la variance** et leur traduction sur l'écart-type.
- [ ] J'énonce Bienaymé-Tchebychev, **avec la condition $ k > 1 $**, et j'explique pourquoi
      la borne est lâche.
- [ ] Je définis le coefficient de variation et je dis dans quels cas l'écart-type ne suffit
      pas.
- [ ] J'écris la décomposition intra/inter et j'interprète le rapport
      $ V_{inter}/\sigma^2 $.
- [ ] Je vérifie qu'une variable est **additive** avant tout calcul de concentration, et je
      donne deux exemples de chaque côté.
- [ ] Je démontre que $ \sum x_i = N_k m_k $ et que **l'effectif total se simplifie** dans le
      calcul des parts.
- [ ] Je construis une courbe de Lorenz, j'en énonce les **quatre propriétés** et je démontre
      que sa pente vaut $ m_{X_k}/m_X $.
- [ ] Je calcule un indice de Gini **sans oublier la division par 10 000** et je contrôle
      qu'il est dans [0 ; 1].
- [ ] J'explique ce qu'est la **dominance de Lorenz** et ce qui se passe quand deux courbes
      se croisent.
- [ ] Je récite l'arbre de décision : quel indicateur, dans quelle situation, et pourquoi.
- [ ] Je cite les **quatre anomalies du support** (diapositives 35, 43, 48, 55) et je dis ce
      que donne le recalcul.
- [ ] Je traduis chaque indicateur en vocabulaire de finance de marché : volatilité, VaR,
      Sharpe, risque spécifique et systématique, concentration de portefeuille.

### 6.2 — Grille de vérification chiffrée

| Épreuve | Conditions | Seuil | Résultat obtenu | Décision si sous le seuil |
|---|---|:---:|:---:|---|
| Niveau 1 — restitution | Sans document | 100 % | *…… / 22* | Reprendre la section du §2 correspondante, refaire les cartes le jour même |
| Niveau 2 — application | Chronométré, sans document | 80 % | *…… %* | Refaire les exercices ratés à J+1, **sans regarder le corrigé avant d'avoir cherché** |
| Niveau 3 — maîtrise | Sans document | 4 sur 6 | *…… / 6* | Approfondissement ciblé sur la notion en cause |
| Niveau 4 — simulation | 2 h, sans document | 14/20 | *…… / 20* | Nouvelle simulation à J+7 avec d'autres données chiffrées |
| Exposé blanc | À voix haute, 10 min, sans notes | Aucun blocage | *oui / non* | Le point de blocage **est** la notion mal comprise |

**Lecture des échecs.** Échec au niveau 1 → défaut de **mémorisation**. Échec au niveau 2
alors que le 1 est acquis → défaut de **méthode de calcul**. Échec au niveau 3 alors que le
2 est acquis → défaut de **compréhension**. Échec au niveau 4 alors que 1, 2 et 3 sont acquis
→ défaut de **gestion du temps ou de rédaction**, pas de connaissance. **Quatre causes,
quatre traitements différents — ne les confonds pas.**

::: methode L'exposé blanc pour ce chapitre — le plan à tenir en 10 minutes
1. **(1 min)** Le projet : présenter conserve, résumer perd — et pourquoi cette perte est
   nécessaire. Les trois familles et leur question.
2. **(2 min)** La position : mode et classe modale (avec la densité), les trois écritures de
   la moyenne et ses trois propriétés, la médiane et l'interpolation. **Le diagnostic
   d'asymétrie en une phrase.**
3. **(4 min)** La dispersion : pourquoi la position ne suffit pas ; quantiles et écarts
   inter-quantiles ; **la somme des écarts est nulle donc valeur absolue ou carré** ; EAM,
   variance, écart-type ; Koenig et les trois propriétés, démontrées à voix haute ;
   Bienaymé-Tchebychev avec sa condition ; le coefficient de variation ; la décomposition
   intra/inter.
4. **(2 min)** La concentration : la condition d'additivité, la part de l'agrégat et la
   simplification de $ N $, la courbe de Lorenz avec ses quatre propriétés, le Gini avec le
   piège d'unité.
5. **(1 min)** La clôture : l'arbre de décision, et la traduction en finance de marché.

**Règle : si tu bloques plus de 5 secondes sur un point, note-le et continue. Le point noté
est ta prochaine séance de travail.**
:::

### 6.3 — Protocole de révision daté

Document produit le **10 septembre 2026**. Les échéances sont donc :

| Échéance | Date | Durée | Ce qui est révisé |
|---|---|:---:|---|
| **J+1** | 11 septembre 2026 | 25 min | Fiche de synthèse (§4.1) + les 65 cartes (§4.2) + relecture du schéma (§4.4) |
| **J+3** | 13 septembre 2026 | 35 min | Cartes échouées à J+1 + niveau 1 complet, chronométré + les huit ancrages (§4.3) |
| **J+7** | 17 septembre 2026 | 60 min | Liste de contrôle à froid (§6.1) + exercices 2.2, 2.4 et 3.3 + relecture intégrale des points de vigilance (§3) |
| **J+21** | 1ᵉʳ octobre 2026 | 2 h 15 | Simulation d'examen complète (niveau 4) en 2 h, puis auto-correction au barème |

**Règle de décision.** Une carte échouée **deux fois de suite** relève de la compréhension,
pas de la mémoire : reprends la section du §2 correspondante, et non la carte.

**Règle d'entretien.** Ce chapitre est **le socle calculatoire de toute la suite du cours** :
le chapitre 3 (évolutions temporelles) et le chapitre 4 (croisement de variables) supposent
la moyenne, la variance et la décomposition intra/inter acquises. **Une révision de 15 minutes
avant chaque nouveau chapitre est un investissement, pas une perte de temps.**

<!--saut-->

## Annexe — Tableau de couverture du support d'origine

Preuve de complétude, vérifiable en deux minutes. Le support d'origine — *CHAPITRE 2 :
Résumer pour informer*, Hélène Couprie, **70 diapositives** — est inventorié ci-dessous
**diapositive par diapositive**, sans trou de numérotation.

**Légende.** ✔ traité intégralement — ⚠ traité, mais support d'origine incomplet, ambigu ou
erroné : la reconstruction est signalée à l'endroit exact — ✖ impossible à traiter, donnée
manquante.

| # | Élément du support d'origine | Nature | Traité dans | État |
|:---:|---|---|---|:---:|
| 1 | Page de titre : « CHAPITRE 2 : Résumer pour informer », Hélène Couprie | titre | En-tête du document | ✔ |
| 2 | Contenu et plan du chapitre (3 sections) | plan | §2, encadré d'ouverture | ✔ |
| 3 | Section 1 : résumer la position — mode, moyenne, médiane | plan de section | §2.1.1 | ✔ |
| 4 | Illustration pour le mode : logements en Outre-mer, recensement 2023 — **3 questions posées, aucune réponse** | tableau + questions | §2.1.2 : les 3 questions corrigées ; écart d'arrondi de ±1 sur trois colonnes signalé | ⚠ |
| 5 | Illustration pour le mode : diagramme en barres horizontales groupées | image non commentée | §2.1.2 : figure décrite et interprétée, lien avec le chapitre 1 rétabli | ⚠ |
| 6 | Deuxième illustration : personnes incarcérées par tranche d'âge (graphique) | image non commentée | §2.1.3 : figure décrite, piège de la lecture directe explicité | ⚠ |
| 7 | Deuxième illustration : le tableau des personnes incarcérées | tableau | §2.1.3 : amplitudes et densités recalculées ligne par ligne | ✔ |
| 8 | Définitions : amplitude, densité, classe modale | définitions | §2.1.3 : les trois définies simple puis académique, avec démonstration | ✔ |
| 9 | Deuxième illustration : le même graphique avec la densité en ordonnée | image non commentée | §2.1.3 : comparaison des deux figures, effet de la correction montré | ⚠ |
| 10 | Histogramme : définitions | définitions | §2.1.4 | ✔ |
| 11 | Deuxième illustration : l'histogramme | image non commentée | §2.1.4 : démonstration « aire = effectif », contrôle de la somme des aires | ⚠ |
| 12 | La moyenne arithmétique (données brutes) | formule | §2.1.5 : énoncée, expliquée terme à terme, illustrée | ✔ |
| 13 | Calcul de la moyenne à partir d'une distribution | formule | §2.1.6 : les deux écritures ($ n_i $ et $ f_i $) démontrées équivalentes | ✔ |
| 14 | Calcul de la moyenne par agrégation | formule | §2.1.7 : démonstration complète | ✔ |
| 15 | Calcul par agrégation (suite) : l'avertissement sur la variable de découpage | mise en garde | §2.1.7 : traduite et transformée en repère opératoire | ✔ |
| 16 | Propriété 1 : la somme des écarts à la moyenne est nulle | propriété | §2.1.8 : démontrée, et conséquence tirée pour toute la section 2 | ✔ |
| 17 | Propriété 2 : la moyenne est un opérateur linéaire | propriété | §2.1.9 : démontrée | ✔ |
| 18 | Illustration : salaires des fonctionnaires 2022-2023 — **2 questions posées, aucune réponse** | tableau + questions | §2.1.10 : les 2 questions corrigées ; **écart de 1,6 € sur 2023 (3 114,4 recalculé contre 3 116 annoncé)** expliqué par l'arrondi des fréquences | ⚠ |
| 19 | Propriété 3 : la moyenne est sensible aux valeurs extrêmes | propriété | §2.1.11 : illustrée numériquement | ✔ |
| 20 | La médiane : définition | définition | §2.1.12 : deux définitions équivalentes | ✔ |
| 21 | Calcul de la médiane sur données brutes | méthode | §2.1.13 : cas pair et impair traités séparément | ✔ |
| 22 | Illustration : densités de population UE15 / UE25 — **1 question posée, aucune réponse** | tableau + question | §2.1.14 : médianes des trois ensembles calculées et interprétées | ⚠ |
| 23 | Illustration (suite) — **2 questions posées, aucune réponse** | questions | §2.1.14 : les 3 moyennes calculées ; effet de la division par 2 de Malte démontré sur médianes **et** moyennes | ⚠ |
| 24 | Illustration : revenus salariaux médians par CSP (graphique) — **2 questions posées, aucune réponse** | image + questions | §2.1.15 : questions corrigées ; **démonstration par contre-exemple que la médiane ne s'agrège pas** | ⚠ |
| 25 | Calcul de la médiane à partir d'une distribution | méthode | §2.1.16 : interpolation linéaire démontrée, pas seulement énoncée | ✔ |
| 26 | Illustration : familles selon le nombre d'enfants — **2 questions posées, aucune réponse** | tableau + questions | §2.1.17 : questions corrigées ; **l'interpolation donne 0,09 enfant pour 2008, résultat aberrant expliqué et remplacé par la règle du rang** | ⚠ |
| 27 | Section 2 : indicateurs de dispersion — les quatre cas d'introduction | plan de section | §2.2.1 : les quatre cas décrits et comparés | ✔ |
| 28 | L'étendue | définition | §2.2.2 : définie, limite explicitée | ✔ |
| 29 | Écart inter-centiles $ C_1 - C_{99} $ | définition | §2.2.3 : replacé dans la famille des écarts inter-quantiles | ✔ |
| 30 | Les quantiles | définition | §2.2.4 : définition par $ F^{-1} $ reconstruite | ✔ |
| 31 | Interprétation d'un quantile | méthode | §2.2.4 : phrases-types de lecture produites | ✔ |
| 32 | Application aux cas de l'introduction | application | §2.2.5 : les quatre cas recalculés | ✔ |
| 33 | Calcul d'un quantile d'ordre α % à partir d'une distribution | méthode | §2.2.6 : interpolation démontrée | ✔ |
| 34 | Interprétons quelques quantiles : niveau de vie 2024 | tableau | §2.2.7 : $ D_9/D_1 = 3{,}48 $ recalculé, écarts entre déciles successifs analysés | ✔ |
| 35 | « Version alternative » | tableau | §2.2.7 : **le titre annonce « retraités, année 2008 » alors que le tableau affiché est celui des niveaux de vie 2024 de la diapositive 34** — incohérence signalée | ⚠ |
| 36 | Représentation graphique : le *boxplot* | définition | §2.2.8 : construction détaillée, conventions des moustaches précisées | ✔ |
| 37 | Exemple d'un *boxplot* | image non commentée | §2.2.8 : figure décrite et reliée aux quantiles calculés | ⚠ |
| 38 | Interprétons des quantiles, encore : quantiles par CSP — **1 question posée, aucune réponse** | tableau + question | §2.2.9 : question corrigée ; **explication de l'écart inter-décile de l'ensemble supérieur à celui de 3 CSP sur 4** (composante inter) | ⚠ |
| 39 | Section 2 (suite) : indicateurs de dispersion | plan | §2.2.10 | ✔ |
| 40 | Calcul des indicateurs : EAM, variance, écart-type | formules | §2.2.10 : les trois énoncées, expliquées et justifiées l'une par l'autre | ✔ |
| 41 | Tableau de calcul de la moyenne des écarts sur données brutes | méthode | §2.2.10 : structure du tableau expliquée colonne par colonne | ✔ |
| 42 | Illustration du tableau de calcul : série de 20 âges | tableau | §2.2.11 : tableau intégralement recalculé ($ m = 47{,}9 $ ; $ EAM = 5{,}7 $) | ✔ |
| 43 | Calcul des indicateurs sur données brutes : résultats | résultats | §2.2.11 : **le support s'arrête à la variance (54,19) et ne calcule jamais l'écart-type** — $ \sigma = 7{,}36 $ ans ajouté, seul chiffre interprétable | ⚠ |
| 44 | Interprétation de l'écart-type : inégalité de Bienaymé-Tchebychev | théorème | §2.2.12 : énoncée avec sa condition $ k > 1 $, appliquée et commentée | ✔ |
| 45 | Application en finance (introduction) | application | §2.2.13 | ✔ |
| 46 | Application en finance 1/3 : la série des rendements | application | §2.2.13 : données reprises et recalculées | ✔ |
| 47 | Application en finance 2/3 : moyennes et écarts-types par période | application | §2.2.13 : tous les chiffres vérifiés | ✔ |
| 48 | Application en finance 3/3 : « 99 % de chances de faire des gains en périodes 1, 2, 3, 5 » | conclusions | §2.2.13 : **conclusions non reconstructibles** — Bienaymé-Tchebychev exige $ k > 1 $ or $ m/\sigma < 1 $ dans les cinq périodes, et la période 2 a une moyenne négative. Signalé, non masqué | ⚠ |
| 49 | Calculs d'agrégats : le problème posé | problématisation | §2.2.14 : les quatre points reformulés | ✔ |
| 50 | Propriétés de la variance : Koenig, translation, non-linéarité, corollaire | propriétés | §2.2.14 : les quatre démontrées, utilité de Koenig expliquée | ✔ |
| 51 | Illustration des propriétés : effet d'une translation (+ 6 points) | image non commentée | §2.2.14 : figure décrite, propriété vérifiée numériquement | ⚠ |
| 52 | Illustration des propriétés : effet d'une multiplication (× 2) | image non commentée | §2.2.14 : figure décrite, $ \sigma_{aX} = \lvert a \rvert \sigma_X $ vérifiée | ⚠ |
| 53 | Coefficient de variation | définition | §2.2.15 : défini, cas d'usage précisés, lien avec le ratio de Sharpe | ✔ |
| 54 | Calcul de la variance à partir d'une distribution | formule | §2.2.16 : pondération par les effectifs démontrée | ✔ |
| 55 | Illustration : cas n° 1 à 4 | tableau | §2.2.16 : **la variance du cas 4 annoncée à 10,4 vaut en réalité 20,8 ($ \sigma = 4{,}56 $ et non 3,2) — une division par 2 en trop, qui inverse le classement des cas 2 et 4.** Vérification complète fournie | ⚠ |
| 56 | Choix de la formule de calcul | méthode | §2.2.16 : arbre de décision reconstruit | ✔ |
| 57 | Calcul de la variance par agrégation (via Koenig) | formule | §2.2.17 : démonstration complète | ✔ |
| 58 | Corollaire : décomposition de la variance intra / inter | corollaire | §2.2.18 : les deux formules démontrées, cas extrêmes décrits, lien avec le R² annoncé | ✔ |
| 59 | Section 3 : résumer la concentration — dispersion contre concentration | plan de section | §2.3.1 : distinction reconstruite, **condition d'additivité transformée en règle opératoire avec tableau de cas** | ✔ |
| 60 | Calcul de la part de l'agrégat ; relation $ \sum x_i = N_k m_{X_k} $ | méthode | §2.3.2 : relation démontrée ; **démonstration que l'effectif total se simplifie**, ce que le support pose sans le prouver | ✔ |
| 61 | Illustration : classes de salaires en France en 2005 | tableau | §2.3.3 : colonne (5) intégralement recalculée. **La colonne (4) « estimation du salaire moyen » n'est jamais expliquée : il s'agit du centre de classe** — hypothèse identifiée, vérifiée sur les cinq classes, et sa fragilité sur la classe haute discutée | ⚠ |
| 62 | Illustration : les mêmes classes en 2021 | tableau | §2.3.4 : recalcul complet. **La somme des cinq parts arrondies vaut 100,1 et non 100,0** — excédent d'arrondi identifié et suivi jusqu'au Gini | ⚠ |
| 63 | Illustration : comparaison 2005 / 2021 — **1 question posée, aucune réponse** | tableau + question | §2.3.5 : réponse complète (variations en points, en relatif, rapport entre extrêmes de 3,4 à 10,4) **et réserve méthodologique sur le changement probable de champ, que je ne peux pas lever avec les seules données du support** | ⚠ |
| 64 | Courbe de Lorenz : définition | définition | §2.3.6 : définie ; **la condition de classement croissant, absente du support, est ajoutée et justifiée** | ✔ |
| 65 | Tableau de calcul de la courbe de Lorenz (cumuls 2005 et 2021) | tableau | §2.3.6 : cumuls refaits ligne par ligne. **Le support cumule des valeurs arrondies** (d'où 40,7 au lieu de 40,8 en 2005, et 100,1 ramené à 100,0 en 2021) — effet quantifié | ⚠ |
| 66 | Graphe de la courbe de Lorenz, 2005 et 2021 | image non commentée | §2.3.6 : figure reconstruite en intégralité — **la diagonale d'égalité, absente du support, est ajoutée**, sans quoi la figure ne se lit pas. Les quatre propriétés de la courbe sont démontrées | ⚠ |
| 67 | Interprétation de la courbe de Lorenz ; dominance ; croisement | interprétation | §2.3.7 : les trois énoncés reformulés et démontrés ; **contre-exemple chiffré du croisement construit** ; absence de croisement vérifiée sur 2005/2021 | ✔ |
| 68 | Calcul du GINI, année 2005 : graphe avec l'aire de concentration et un trapèze (1 025) | image | §2.3.8 : calcul complet des cinq trapèzes (le 1 025 du support retrouvé ✔). **Le piège d'unité — diviser par 10 000 quand les cumuls sont en % — n'est pas signalé par le support** : il l'est ici, avec son contrôle | ⚠ |
| 69 | Calcul de l'indice de GINI : définition géométrique, bornes, formule | formule | §2.3.8 : formule **démontrée** en quatre étapes (carré unité, triangle, soustraction, trapèzes) ; bornes 0 et 1 démontrées, raffinement $ (N-1)/N $ ajouté | ✔ |
| 70 | Récapitulons | synthèse | §2.4 : tableau complet des treize indicateurs + arbre de décision en cinq questions | ✔ |

**Bilan de couverture : 70 diapositives inventoriées, 70 traitées — dont 46 ✔ et 24 ⚠, et
aucune ✖.**

**La colonne « Traité dans » renvoie aux paragraphes de ce document.** Chacun existe aussi, deux
fois plus développé, dans ***Résumer pour informer — version intégrale*** : mêmes numéros, mêmes
titres. **Quand un point de ce cours-ci ne suffit pas, ouvre l'intégrale au même numéro.** Les 24 ⚠ ne signalent aucune lacune de ce document : elles marquent les endroits
où le support d'origine était elliptique (images non commentées, questions posées sans
réponse, méthode implicite), incohérent ou erroné — et où la reconstruction est explicitement
signalée à l'endroit exact.

**Les quatre anomalies de fond** — diapositives **35** (titre erroné), **43** (écart-type
jamais calculé), **48** (conclusion non démontrable) et **55** (variance fausse d'un facteur
2) — sont récapitulées au § 3.4.
