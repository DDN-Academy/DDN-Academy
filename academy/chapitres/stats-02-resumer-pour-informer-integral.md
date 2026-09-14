---
matiere: Techniques statistiques — L1 Portail, Division A, AMU
chapitre: Chapitre 2 — Résumer pour informer
titre: Résumer pour informer — version intégrale
sous_titre: Version longue de référence — à consulter quand un point du cours résiste, pas à lire d'un bout à l'autre
resume: Ce document reconstruit intégralement le deuxième chapitre de Techniques statistiques. Il couvre les 70 diapositives du support : les indicateurs de position (mode, classe modale, histogramme, moyenne, médiane), de dispersion (étendue, quantiles, boxplot, écart absolu moyen, variance, écart-type, Koenig, décomposition intra/inter) et de concentration (part de l'agrégat, courbe de Lorenz, indice de Gini), plus l'application en finance où l'écart-type devient la volatilité. Les quatorze questions posées en amphithéâtre y sont corrigées et tous les chiffres du support recalculés.
date: 10 septembre 2026
duree: première lecture 4 h — maîtrise complète ≈ 12 h réparties sur 3 semaines
version: 1.0
sommaire: oui
---

# Chapitre 2 — Résumer pour informer

Ce document remplace le support de cours. Les 70 diapositives y sont couvertes, sans
exception : le **tableau de couverture** en annexe permet de le vérifier ligne par ligne.
Les quatorze questions posées à l'amphithéâtre sont **intégralement corrigées**, chaque formule
est démontrée et illustrée par un calcul complet, et **tous les chiffres du support ont été
recalculés** — ce qui a révélé deux points à signaler.

<!--saut-->

## 1. Carte du chapitre

### 1.1 — Vue d'ensemble

Le chapitre 1 apprenait à **présenter** une distribution sans rien perdre. Celui-ci apprend
à la **résumer** — donc à perdre volontairement de l'information, en échange d'une capacité
de comparaison et de décision. Le support l'annonce dès la première ligne : « les données
contiennent souvent trop d'informations ; dans ce cas, la synthèse s'impose ». Résumer une
distribution, c'est répondre à trois questions successives. **Où se situe la série ?** — les
indicateurs de position : mode, moyenne, médiane. **Comment les données sont-elles réparties
autour de ce centre ?** — les indicateurs de dispersion : étendue, écarts inter-quantiles,
écart absolu moyen, variance, écart-type, coefficient de variation. **Comment la somme des
données se répartit-elle entre les individus ?** — les indicateurs de concentration : part
de l'agrégat, courbe de Lorenz, indice de Gini. Chacune de ces trois questions est
indépendante : deux séries peuvent avoir la même moyenne et des dispersions opposées, ou la
même dispersion et des concentrations différentes. Le chapitre se referme sur une règle qui
vaut pour tout le cours : **le choix des indicateurs dépend du type de données, mais aussi
de ce que l'on veut en faire.**

### 1.2 — Les idées maîtresses

1. **Résumer, c'est perdre de l'information volontairement** — et il faut savoir laquelle
   on perd. C'est l'opposé exact du chapitre 1.
2. **Trois familles d'indicateurs, trois questions distinctes** : position, dispersion,
   concentration. Aucune ne remplace les autres.
3. **Pour une variable continue découpée en classes, la classe modale se lit sur la
   densité — jamais sur l'effectif ni sur la fréquence.** C'est le point que le support met
   en rouge.
4. **Dans un histogramme, l'aire d'un rectangle est la fréquence de la classe** — et la
   somme des aires vaut 1. C'est ce qui distingue un histogramme d'un diagramme en colonnes.
5. **La moyenne est linéaire et sensible aux valeurs extrêmes ; la médiane n'est ni l'une ni
   l'autre.** C'est pourquoi on publie des revenus **médians**.
6. **La variance n'est pas linéaire** : $ V(aX + b) = a^2 V(X) $. Ajouter une constante ne
   change rien, multiplier multiplie par le carré.
7. **L'écart-type est interprétable parce qu'il a l'unité des données** — et l'inégalité de
   Bienaymé-Tchebychev lui donne un sens chiffré : au moins 75 % des observations dans
   $ m \pm 2\sigma $.
8. **En finance, l'écart-type porte un nom : la volatilité.** Le couple
   (rentabilité moyenne, volatilité) est le double indicateur du risque.
9. **Dispersion et concentration ne mesurent pas la même chose** : la dispersion regarde la
   répartition des **observations**, la concentration la répartition de la **somme**.
10. **La courbe de Lorenz et l'indice de Gini résument l'inégalité** — et quand deux courbes
    se croisent, les indicateurs peuvent se contredire.

### 1.3 — Prérequis

::: methode Prérequis 1 — Ce qu'il faut avoir retenu du chapitre 1
Cinq notions sont utilisées sans être rappelées :

- **Population, unités statistiques, effectif total $ N $** ; **variable $ X $**,
  **modalités $ x_i $**, $ i = 1, \ldots, p $.
- **Effectifs $ n_i $** et **fréquences $ f_i = n_i / N $**, avec $ \sum f_i = 1 $.
- **Fréquences cumulées $ F(x_k) = \sum_{i=1}^{k} f_i $** — croissantes, de $ f_1 $ à 1.
  **Tout le calcul des quantiles repose dessus.**
- **Type de variable** : qualitative (nominale, ordinale) / quantitative (discrète,
  continue). **Le type détermine les indicateurs autorisés** — c'est le fil du chapitre.
- **Série brute (*raw data*) contre distribution** : les formules diffèrent selon la
  présentation des données. Le support y revient explicitement (diapo 56).
:::

::: methode Prérequis 2 — Les notations mathématiques employées
| Symbole | Lecture | Où il sert |
|---|---|---|
| $ \sum_{i=1}^{N} x_i $ | Somme des $ x_i $ pour $ i $ de 1 à $ N $ | Moyenne sur données brutes |
| $ \sum_{i=1}^{p} n_i x_i $ | Somme sur les **modalités**, pondérée par les effectifs | Moyenne sur distribution |
| $ \|x_i - m\| $ | **Valeur absolue** de l'écart : sa grandeur, sans son signe | Écart absolu moyen |
| $ (x_i - m)^2 $ | Carré de l'écart : positif, et qui **pénalise davantage les grands écarts** | Variance |
| $ \sqrt{\ } $ | Racine carrée : rend à la variance l'unité des données | Écart-type |
| $ m $, $ \sigma^2 $, $ \sigma $ | Moyenne, variance, écart-type | Partout |

**Le piège d'indice, présent dans tout le chapitre :** l'indice $ i $ désigne tantôt une
**observation** (formules sur données brutes, $ i $ va de 1 à $ N $), tantôt une **modalité**
(formules sur distribution, $ i $ va de 1 à $ p $). Le support le rappelle deux fois. Lire
la borne de la somme suffit à savoir dans quel cas on est.
:::

::: methode Prérequis 3 — Opérateur linéaire et interpolation linéaire
**Un opérateur linéaire** transforme $ Y = aX + b $ en $ m_Y = a\,m_X + b $ : la
transformation « traverse » l'opérateur. La moyenne l'est ; la médiane et la variance ne le
sont pas.

**L'interpolation linéaire** consiste à estimer une valeur intermédiaire en supposant que la
variation est **régulière** entre deux points connus. Si l'on connaît deux points
$ (x_a, F_a) $ et $ (x_b, F_b) $ et que l'on cherche le $ x $ correspondant à une valeur
$ F $ comprise entre les deux :

$$ x \approx x_a + (x_b - x_a) \times \frac{F - F_a}{F_b - F_a} $$

**Lecture :** on part de $ x_a $ et on avance sur le segment $ [x_a ; x_b] $ d'une fraction
égale à la **part du chemin déjà parcourue en ordonnée**. C'est le principe unique de toutes
les formules de médiane et de quantiles du chapitre.
:::

### 1.4 — Lien avec la finance de marché

Ce chapitre est, littéralement, le cours de gestion du risque que vous pratiquez déjà.

::: marche
- **L'écart-type EST la volatilité.** Le support le dit explicitement (diapo 45) : sur une
  série de rentabilités journalières, l'écart-type mesure la volatilité. Tout ce que le
  chapitre démontre sur $ \sigma $ — non-linéarité, formule de Koenig, insensibilité à
  l'ajout d'une constante — vaut donc pour la volatilité.
- **Le couple (moyenne, écart-type) est le couple (rendement, risque).** La diapositive 46 le
  formule ainsi : « on va donc avoir un **double indicateur** qui nous donnera nos chances de
  succès ». C'est le fondement de toute la théorie moderne du portefeuille.
- **Les quantiles sont la *Value at Risk*.** Le quantile d'ordre 5 % de la distribution des
  rentabilités est la perte que l'on ne dépasse que 5 fois sur 100. Le chapitre vous apprend
  à le calculer par interpolation.
- **L'inégalité de Bienaymé-Tchebychev est un majorant du risque sans hypothèse de loi.**
  Elle vaut pour **toute** distribution, y compris à queues épaisses — contrairement à la
  règle « 95 % dans $ m \pm 2\sigma $ » qui suppose la normalité et qui, sur des rendements
  réels, sous-estime gravement les extrêmes. Retenez cette différence : c'est l'une des
  causes documentées des grandes pertes de marché.
- **Le coefficient de variation $ \sigma / m $ est l'inverse d'un ratio de Sharpe simplifié.**
  Comparer deux stratégies dont les rendements moyens diffèrent exige de rapporter le risque
  au rendement — c'est exactement ce que fait le CV, et c'est pourquoi le support insiste sur
  le fait qu'il est **sans unité**.
- **La décomposition intra/inter est celle du risque spécifique et du risque systématique.**
  La variance totale d'un ensemble se décompose en dispersion **à l'intérieur** des groupes
  et dispersion **entre** les groupes : c'est la structure même de l'analyse de la
  performance d'un portefeuille par secteurs.
:::

<!--saut-->
## 2. Le cours reconstruit

L'ordre suit celui du support. Trois ajouts : les **quatorze questions posées à
l'amphithéâtre** sont corrigées, les **tableaux présentés sous forme d'image** sont
restitués en texte, et **tous les chiffres sont recalculés**.

::: objectif Le programme annoncé (diapositive 2)
> Les données contiennent souvent **trop d'informations** (trop de variables, de modalités,
> etc.). Dans ce cas, **la synthèse s'impose**.

**Contenu :** les différentes façons de résumer la distribution d'un caractère statistique
**quantitatif**.

**Plan :**
1. **Indicateurs de position** (moyenne, mode) : *où se situe la série de données ?*
2. **Indicateurs de dispersion** (écart-type, variance) : *comment les données sont-elles
   réparties ?*
3. **Indicateurs de concentration** (mesure des inégalités) : *comment la somme des données
   se répartit-elle ?*
:::

::: examen Le mot le plus important de la diapositive : « quantitatif »
Le chapitre porte sur le résumé d'un caractère **quantitatif**. C'est une restriction, et
elle est logique : on ne peut pas calculer la moyenne d'une variable qualitative
(chapitre 1, test de la moyenne). **Une seule exception traverse le chapitre : le mode**,
qui existe pour tout type de variable, y compris nominale.

Le plan lui-même est une réponse en trois questions, qu'il faut savoir énoncer :
**où ? comment réparties ? comment la somme se répartit-elle ?**
:::

### 2.1 — Résumer la position des données

#### 2.1.1 Les trois indicateurs de position (diapositive 3)

::: definition Les trois résumés en une seule valeur
- **Le mode** : la **modalité qui présente la fréquence la plus élevée** (ou l'effectif le
  plus fort).
- **La moyenne** : l'**indicateur de tendance centrale le plus connu**. Elle se calcule en
  **divisant la somme des observations par le nombre d'observations**.
- **La médiane** : plus spécialisée, elle indique un **centre de rang**.
:::

::: demo Trois « centres » qui ne coïncident pas, et pourquoi
Ces trois indicateurs répondent à la même question — « où se situe la série ? » — par trois
définitions incompatibles du centre.

| Indicateur | Ce qu'il maximise ou équilibre | Sur quoi il porte |
|---|---|---|
| **Mode** | La **fréquence** : la valeur la plus souvent observée | Les **effectifs** |
| **Moyenne** | L'**équilibre des écarts** : la somme des écarts à la moyenne est nulle | Les **valeurs** |
| **Médiane** | L'**équilibre des rangs** : autant d'individus au-dessus qu'en dessous | Les **rangs** |

**Conséquence immédiate :** sur une distribution symétrique, les trois coïncident ; sur une
distribution asymétrique — la distribution des revenus, par exemple — ils divergent, et
l'écart entre eux **mesure l'asymétrie**. C'est pourquoi le support précise que la médiane
est « très utilisée pour les distributions de revenu » (diapo 20).
:::

#### 2.1.2 Le mode : première illustration (diapositives 4 et 5)

**Le tableau du support** — Distribution des logements selon le type en Outre-mer,
recensement de la population 2023.

| Type de logement | Guadeloupe | Martinique | Guyane | Réunion |
|---|---:|---:|---:|---:|
| Habitation de fortune | 1 098 | 790 | 3 698 | 1 867 |
| Case traditionnelle | 2 322 | 578 | 1 798 | 23 062 |
| Maison ou immeuble en bois | 8 363 | 6 086 | 11 841 | 12 913 |
| **Maison ou immeuble en dur** | **168 050** | **164 290** | **71 089** | **321 445** |
| **Ensemble** | **179 833** | **171 743** | **88 425** | **359 288** |

::: correction Les trois questions posées, corrigées
**1. Population, unités statistiques, taille, caractères, types et sous-types.**
- **Population** : l'ensemble des **logements** des quatre territoires d'Outre-mer recensés
  en 2023.
- **Unités statistiques** : **un logement**.
- **Taille** : elle est donnée **par territoire** — 179 833 en Guadeloupe, 171 743 en
  Martinique, 88 425 en Guyane, 359 288 à La Réunion. Pour l'ensemble :
  $ N = 799\,289 $ logements.
- **Les caractères statistiques — il y en a deux :**
  - le **type de logement**, **qualitatif nominal**, à 4 modalités (habitation de fortune,
    case traditionnelle, maison ou immeuble en bois, maison ou immeuble en dur) ;
  - la **zone géographique**, **qualitative nominale**, à 4 modalités (les quatre
    territoires).

**2. A-t-on ici la représentation d'une distribution au sens classique du terme ?**
**Non.** Une distribution associe **un** effectif à chaque modalité d'**une seule** variable.
Ici, deux variables sont croisées : le tableau contient **quatre distributions juxtaposées**,
une par territoire. C'est exactement la situation « plusieurs distributions d'un même
caractère statistique » du chapitre 1 — la **zone géographique** joue le rôle de variable de
**découpage**, le **type de logement** celui de variable **étudiée**.

**3. Quel est le mode de la distribution « type de logement » ?**
**« Maison ou immeuble en dur »** — dans les quatre territoires, et donc aussi pour
l'ensemble. C'est la modalité au plus fort effectif, très loin devant les autres : elle
représente à elle seule de 80 % (Guyane) à près de 94 % (Guadeloupe) des logements.
:::

::: piege Un détail de rigueur : les colonnes ne bouclent pas exactement
Recomptons les colonnes : Guadeloupe donne exactement 179 833 ✔ ; Martinique donne 171 744
contre 171 743 annoncés ; Guyane 88 426 contre 88 425 ; La Réunion 359 287 contre 359 288.

**Trois écarts de une unité — ce n'est pas une erreur, c'est un effet d'arrondi.** Les
données de recensement sont des **estimations pondérées**, arrondies à l'unité ligne par
ligne ; la somme des arrondis ne redonne pas l'arrondi de la somme. C'est exactement le
phénomène observé au chapitre 1 sur les pourcentages qui totalisent 100,1 %.

**Ce qu'il faut en faire :** le signaler si l'on refait le calcul, et surtout **ne pas
corriger le total** : c'est le total publié qui fait foi.
:::

**La représentation graphique (diapositive 5).** Le support projette un **diagramme en barres
horizontales groupées** : quatre groupes, un par territoire, et dans chaque groupe quatre
barres, une par type de logement, avec les effectifs affichés en bout de barre. Le support
commente : « on constate qu'il y a en fait **4 diagrammes colonnes horizontales juxtaposés**
pour chaque valeur du caractère statistique *zone géographique* ».

::: examen
Ce commentaire fait le lien avec le chapitre 1 : c'est un **diagramme groupé**, et le
groupement se fait **par territoire**, donc l'œil compare les **types de logement** à
l'intérieur de chaque territoire. Si la question portait sur l'évolution d'un type de
logement d'un territoire à l'autre, il faudrait grouper par **type de logement**.
:::

#### 2.1.3 Le mode d'une variable continue : amplitude, densité, classe modale (diapositives 6 à 9)

**La deuxième illustration** porte sur les **effectifs des personnes incarcérées suivant la
classe d'âge**. La diapositive 6 en donne un diagramme en colonnes groupées par année (2005,
2010, 2015, 2020), une couleur par classe d'âge, et pose « les mêmes questions que
précédemment ».

**Le tableau (diapositive 7)** — Effectifs des personnes incarcérées suivant la classe d'âge
en 2020 :

| Classe d'âge | Effectif | Fréquence | Amplitude | Densité d'observations |
|---|---:|---:|---:|---:|
| De 16 ans à moins de 18 ans | 819 | 819/79 788 | 2 | 0,0051 |
| De 18 ans à moins de 21 ans | 5 361 | 0,067 | 3 | 0,0224 |
| De 21 ans à moins de 25 ans | 11 444 | 0,143 | 4 | 0,0359 |
| **De 25 ans à moins de 30 ans** | 14 950 | 0,187 | 5 | **0,0375** |
| De 30 ans à moins de 40 ans | 23 979 | 0,301 | 10 | 0,0301 |
| De 40 ans à moins de 50 ans | 13 413 | 0,168 | 10 | 0,0168 |
| De 50 ans à moins de 60 ans | 6 501 | 0,081 | 10 | 0,0081 |
| 60 ans ou plus | 3 321 | 0,042 | 20 | 0,0021 |
| **Ensemble** | **79 788** | | | |

::: definition Amplitude, densité, classe modale (diapositive 8)
La distribution d'un caractère quantitatif **continu** peut être représentée en
**discrétisant** ce caractère sous forme de **classes**.

**Dans ce cas la classe modale est définie à partir de la densité — et non à partir de la
fréquence ni de l'effectif de la classe !** *(mis en rouge dans le support)*

- **L'amplitude de classe** correspond à la **valeur maximale moins la valeur minimale** de
  la variable pour la classe considérée.
- **La densité d'une classe** est le **rapport entre la fréquence de la classe et
  l'amplitude de la classe**.
- **La classe modale** est la classe qui a la **densité d'observations la plus élevée**.
:::

::: formule Les deux formules de la diapositive
$$ \text{amplitude} = x_{\max} - x_{\min} \qquad
\text{densité} = \frac{\text{fréquence de la classe}}{\text{amplitude de la classe}} $$
:::

::: demo Pourquoi la densité et non l'effectif — la démonstration par le tableau
C'est le point que le support met en rouge, et il se démontre sur ses propres chiffres.

**Étape 1 — ce que dit l'effectif.** La classe la plus nombreuse est « de 30 à moins de
40 ans », avec **23 979** personnes (fréquence 0,301). Conclusion naïve : ce serait la classe
modale.

**Étape 2 — pourquoi cette conclusion est fausse.** Cette classe couvre **10 années**, alors
que « de 25 à moins de 30 ans » n'en couvre que **5**. À densité égale, une classe deux fois
plus large contient deux fois plus de monde : son effectif élevé vient en partie de sa
**largeur**, pas de sa **concentration**.

**Étape 3 — neutraliser la largeur.** C'est exactement ce que fait la densité : on divise la
fréquence par l'amplitude, ce qui donne une **fréquence par année d'âge**.
- « 30 à 40 ans » : $ 0{,}301 / 10 = 0{,}0301 $ par an.
- « 25 à 30 ans » : $ 0{,}187 / 5 = 0{,}0374 $ par an — le support affiche 0,0375, écart
  d'arrondi sur la fréquence.

**Conclusion : la classe modale est « de 25 ans à moins de 30 ans »**, avec la densité la
plus forte (0,0375), et non la classe la plus nombreuse. **Le support le confirme
diapositive 9.**

**La règle à retenir :** dès que les classes n'ont **pas la même amplitude**, comparer des
effectifs revient à comparer des choses de tailles différentes. Seule la densité est
comparable.
:::

::: exemple Vérifions deux lignes du tableau
**Ligne 1 — « de 16 à moins de 18 ans ».** Le support laisse volontairement la fréquence sous
forme de fraction : $ 819 / 79\,788 = 0{,}01026 $. Amplitude : $ 18 - 16 = 2 $ ans. Densité :
$ 0{,}01026 / 2 = 0{,}00513 $, soit **0,0051** ✔

**Dernière ligne — « 60 ans ou plus ».** Fréquence : $ 3\,321/79\,788 = 0{,}0416 $, soit
0,042 ✔ Amplitude : **20**. Or la classe est **ouverte** — « 60 ans ou plus » n'a pas de
borne supérieure. Le support a donc **fixé** conventionnellement la borne à 80 ans.
Densité : $ 0{,}042 / 20 = 0{,}0021 $ ✔

**Le point de méthode :** une **classe ouverte** oblige à choisir une borne pour calculer
amplitude et densité. Ce choix est **conventionnel** et doit être signalé — il influence la
densité de cette classe, mais ici pas la conclusion, la classe étant de loin la moins dense.
:::

**La densité en graphique (diapositive 9).** Le support reprend le diagramme en colonnes
groupées de la diapositive 6, mais **en densité** au lieu des effectifs, pour les quatre
années. Il conclut : « la classe modale est la tranche d'âge de **25 à 30 ans** » et
« cette figure est **plus informative** ; mieux vaut tracer un **histogramme** ».

#### 2.1.4 L'histogramme (diapositives 10 et 11)

::: definition L'histogramme
- Un histogramme se construit en mettant **en abscisse les limites des classes** et **en
  ordonnée la densité des classes**.
- **La classe modale correspond au rectangle le plus haut** de l'histogramme.
- **L'aire de chaque rectangle correspond à la fréquence de la classe.**
:::

::: demo La démonstration du support, ligne à ligne
$$ \text{Aire} = \text{Base} \times \text{Hauteur} = \text{Amplitude} \times \text{Densité}
\qquad (1) $$
$$ \text{Aire} = \text{Amplitude} \times \frac{\text{Fréquence}}{\text{Amplitude}}
= \text{Fréquence} \qquad (2) $$

**Lecture pas à pas.** (1) L'aire d'un rectangle est le produit de sa base par sa hauteur ;
ici la base est l'**amplitude** de la classe et la hauteur sa **densité**. (2) Or la densité
est **par définition** la fréquence divisée par l'amplitude ; en substituant, l'amplitude se
simplifie et il reste la **fréquence**.

**Conséquence, énoncée par le support : la somme des aires vaut 1**, puisque la somme des
fréquences vaut 1 (propriété démontrée au chapitre 1).
:::

::: piege Histogramme et diagramme en colonnes — la confusion la plus coûteuse du chapitre
| | **Diagramme en colonnes** | **Histogramme** |
|---|---|---|
| **Variable** | Qualitative ou quantitative **discrète** | Quantitative **continue**, découpée en classes |
| **En ordonnée** | L'**effectif** ou la **fréquence** | La **densité** |
| **Ce qui porte l'information** | La **hauteur** | L'**aire** |
| **Espaces entre les barres** | Oui — les modalités sont séparées | **Non** — les classes sont contiguës |
| **Largeur des barres** | Arbitraire et constante | **L'amplitude de la classe** — donc variable |

**La conséquence pratique :** dans un histogramme à classes d'amplitudes inégales, mettre
l'**effectif** en ordonnée produit un graphique **faux**, qui gonfle visuellement les classes
larges. C'est précisément l'erreur que la démarche des diapositives 6 à 11 corrige, étape par
étape.
:::

**L'histogramme du support (diapositive 11).** Il porte en abscisse les âges de 0 à 85 ans,
en ordonnée la densité de 0 à 0,050. On y lit immédiatement la forme de la distribution :
une montée rapide entre 16 et 25 ans, un **maximum sur la classe 25-30 ans** (le rectangle le
plus haut), puis une décroissance régulière — la queue s'étirant jusqu'à la classe très large
et très peu dense des 60 ans et plus. Le support conclut : « la classe modale, correspondant
au rectangle le plus haut (densité la plus forte), est la classe **de 25 à 30 ans** ».

<!--saut-->
#### 2.1.5 La moyenne arithmétique (diapositive 12)

::: formule La moyenne sur données brutes
$$ m = \frac{1}{N} \sum_{i=1}^{N} x_i = \frac{1}{N}(x_1 + x_2 + \ldots + x_N) \qquad (3) $$

- $ N $ : le **nombre d'observations** (l'effectif total).
- $ x_i $ : la valeur observée pour la **i-ème unité statistique** de la base.
- **L'indice $ i $ renvoie ici au numéro d'observation**, pas au numéro de modalité.

Ce calcul correspond à celui obtenu à partir de **données brutes** (*raw data*).
:::

Le support ajoute l'avertissement décisif : **si les données sont disponibles uniquement
sous forme de distribution — modalités et effectifs — alors la formule est différente.**

#### 2.1.6 La moyenne à partir d'une distribution (diapositive 13)

::: formule Les deux écritures équivalentes
Pour un caractère $ X $ à $ p $ modalités, d'effectifs $ n_i $ et de fréquences $ f_i $ —
**ici l'indice $ i $ renvoie au numéro de modalité** :

$$ m = \frac{1}{N} \sum_{i=1}^{p} n_i x_i \qquad (4) $$

ou, en plaçant le $ N $ dans la somme, de façon équivalente à partir des fréquences :

$$ m = \sum_{i=1}^{p} \frac{n_i}{N} x_i = \sum_{i=1}^{p} f_i x_i \qquad (5) $$
:::

::: demo Pourquoi ces formules sont la même que la (3) — et comment passer de l'une à l'autre
**Le raisonnement.** Dans une série brute, une modalité qui apparaît $ n_i $ fois est
additionnée $ n_i $ fois. Plutôt que d'écrire $ x_i + x_i + \ldots + x_i $ ($ n_i $ fois),
on écrit directement $ n_i x_i $. La somme des $ N $ observations devient donc une somme
sur les $ p $ modalités, **pondérée par les effectifs** — c'est la formule (4).

**Le passage de (4) à (5)** est purement algébrique :

$$ \frac{1}{N} \sum n_i x_i = \sum \frac{n_i}{N} x_i = \sum f_i x_i $$

puisque $ f_i = n_i/N $ par définition.

**La moyenne est donc une moyenne pondérée par les fréquences.** C'est la lecture à retenir :
chaque modalité compte à hauteur de sa fréquence.

**Contrôle de cohérence, systématique :** puisque $ \sum f_i = 1 $, la moyenne est
nécessairement **comprise entre la plus petite et la plus grande modalité**. Un résultat qui
sort de cet intervalle signale une erreur de calcul.
:::

::: exemple Les deux formules sur un même exemple
Reprenons les 87 étudiants du chapitre 1 (nombre de frères et sœurs) :
0 → 11 ; 1 → 33 ; 2 → 23 ; 3 → 7 ; 4 → 3 ; 5 → 4 ; 6 → 1 ; 7 → 2 ; 9 → 1 ; 13 → 1 ; 14 → 1.

**Par la formule (4)** :
$$ \sum n_i x_i = 0(11) + 1(33) + 2(23) + 3(7) + 4(3) + 5(4) + 6(1) + 7(2) + 9(1) + 13(1) + 14(1) $$
$ = 0 + 33 + 46 + 21 + 12 + 20 + 6 + 14 + 9 + 13 + 14 = 188 $.
Donc $ m = 188/87 = \mathbf{2{,}16} $ frères et sœurs.

**Par la formule (5)** : $ 0(0{,}1264) + 1(0{,}3793) + 2(0{,}2644) + \ldots = 2{,}16 $ ✔

**Contrôle :** $ 0 \le 2{,}16 \le 14 $ ✔ La moyenne est bien dans l'intervalle des modalités.

**Lecture :** « Les 87 étudiants de la promotion déclarent en moyenne 2,16 frères et sœurs. »
Notez que **la moyenne n'est pas une valeur observable** : personne n'a 2,16 frères et sœurs.
C'est un résumé, pas une observation.
:::

#### 2.1.7 La moyenne par agrégation (diapositives 14 et 15)

::: formule La moyenne d'une population à partir des moyennes de ses sous-populations
Soient $ K $ sous-populations **disjointes** d'effectifs $ n_k $, avec
$ N = \sum_{k=1}^{K} n_k $, et de moyennes respectives $ m_k $. Alors :

$$ m = \sum_{k=1}^{K} \frac{n_k}{N}\, m_k \qquad (6) $$

Il s'agit d'une **moyenne pondérée par la part de la sous-population dans la population
entière**, $ n_k / N $.
:::

::: piege L'avertissement du support, à ne pas manquer
> « **Attention aux confusions** car il s'agit de la fréquence du caractère statistique qui
> **scinde la population en sous-groupes** et non de la fréquence du caractère statistique
> $ X $ qui nous intéresse. »

**Traduction.** Deux variables sont en jeu. La variable **étudiée** $ X $ (le salaire, par
exemple) et la variable **de découpage** (la catégorie, la région, l'année). Les poids
$ n_k/N $ de la formule (6) sont les fréquences de la **variable de découpage**.

**L'erreur type :** pondérer par les fréquences de $ X $ au lieu des effectifs des groupes.
Le repère infaillible : **on pondère toujours par des effectifs de population, jamais par des
valeurs de la variable étudiée.**
:::

::: demo Pourquoi une moyenne de moyennes simple est fausse
Deux groupes : 900 salariés à 2 000 € et 100 salariés à 4 000 €.

- **Moyenne des moyennes (fausse)** : $ (2\,000 + 4\,000)/2 = 3\,000 $ €.
- **Moyenne pondérée (juste)** : $ \frac{900}{1000}(2\,000) + \frac{100}{1000}(4\,000) = 1\,800 + 400 = \mathbf{2\,200} $ €.

**L'écart est de 800 €**, soit 36 %. La moyenne simple traite les deux groupes comme s'ils
avaient le même poids, alors que l'un est neuf fois plus nombreux. **Une moyenne de moyennes
n'est valable que si les groupes ont le même effectif** — cas rarissime.
:::

#### 2.1.8 Propriété 1 : la somme des écarts à la moyenne est nulle (diapositive 16)

::: demo La démonstration du support, étape par étape
$$ \sum_{i=1}^{N} (x_i - m) = \sum_{i=1}^{N} x_i - Nm = \sum_{i=1}^{N} x_i - N \frac{\sum_{i=1}^{N} x_i}{N} = 0 \qquad (7) $$

1. On distribue la somme : la somme d'une différence est la différence des sommes. Le terme
   $ m $ étant constant, le sommer $ N $ fois donne $ Nm $.
2. On remplace $ m $ par sa définition : $ m = \frac{1}{N}\sum x_i $, donc
   $ Nm = \sum x_i $ — « **$ N $ fois la moyenne correspond à la somme des observations** »,
   comme l'écrit le support.
3. Il reste $ \sum x_i - \sum x_i = 0 $.

**Ce que cela signifie**, dans les termes du support : « les écarts positifs ou négatifs à la
moyenne **se compensent avec la même force** ». La moyenne est le **point d'équilibre** de la
distribution — au sens physique du centre de gravité.

**Corollaire donné par le support :** si la distribution est **symétrique**, l'axe de
symétrie correspond à la moyenne, **et la moyenne correspond à la médiane**.
:::

::: examen La conséquence pratique la plus importante
Puisque la somme des écarts est **toujours nulle**, l'écart moyen à la moyenne ne peut pas
servir d'indicateur de dispersion : il vaudrait zéro pour toutes les séries.

**C'est précisément pourquoi il faut passer par la valeur absolue** (l'écart absolu moyen)
**ou par le carré** (la variance). Cette propriété n'est pas une curiosité : elle
**justifie l'existence** de tous les indicateurs de la partie 2 du chapitre.
:::

#### 2.1.9 Propriété 2 : la moyenne est un opérateur linéaire (diapositive 17)

::: formule Linéarité
$$ \text{si } Y = aX + b \text{ alors } m_Y = a\,m_X + b \qquad (8) $$

- Multiplier toutes les valeurs par $ a $ multiplie la moyenne par $ a $.
- Ajouter $ b $ à toutes les valeurs augmente la moyenne de $ b $.
- **A fortiori**, la moyenne de la somme de deux variables est la somme des moyennes.
:::

::: exemple Les trois usages concrets
1. **Changement d'unité.** Des salaires mensuels moyens de 2 955 € donnent une moyenne
   annuelle de $ 12 \times 2\,955 = 35\,460 $ € — sans recalculer quoi que ce soit.
2. **Augmentation uniforme.** Si tous les salaires augmentent de 50 €, la moyenne augmente
   de 50 € exactement.
3. **Augmentation en pourcentage.** Une hausse de 3 % pour tous s'écrit $ Y = 1{,}03\,X $ :
   la moyenne est multipliée par 1,03.

**Attention à la limite :** la linéarité vaut pour une transformation **appliquée à toutes
les observations**. Augmenter seulement certains salaires n'est pas une transformation
linéaire, et la propriété ne s'applique pas.
:::

#### 2.1.10 Application : les salaires des fonctionnaires (diapositive 18)

**Le tableau du support** — Salaires mensuels nets moyens des fonctionnaires en 2022 et 2023 :

| | Fréquence 2022 (%) | Fréquence 2023 (%) | Salaire moyen 2022 (€) | Salaire moyen 2023 (€) |
|---|---:|---:|---:|---:|
| Catégorie A | 68,4 | 68,7 | 3 193 | 3 373 |
| Catégorie B | 18,7 | 18,9 | 2 632 | 2 720 |
| Catégorie C | 12,9 | 12,4 | 2 161 | 2 283 |
| **Titulaires A + B + C** | **100,0** | **100,0** | **2 955** | **3 116** |

*Champ : agents fonctionnaires en France (hors Mayotte). Source : Insee, Système
d'information sur les agents des services publics (Siasp).*

::: correction Les deux questions posées, corrigées
**Question 1 — calculez le salaire mensuel net moyen en 2022 et en 2023.**

C'est un calcul **par agrégation** (formule 6) : les catégories A, B, C sont trois
sous-populations, les fréquences sont leurs **poids**, les salaires moyens leurs
**moyennes de groupe**.

**2022 :**
$$ m = 0{,}684 \times 3\,193 + 0{,}187 \times 2\,632 + 0{,}129 \times 2\,161 $$
$$ = 2\,184{,}0 + 492{,}2 + 278{,}8 = \mathbf{2\,955{,}0}\ \text{€} $$
Le résultat **coïncide exactement** avec la ligne « Titulaires A + B + C » du tableau ✔

**2023 :**
$$ m = 0{,}687 \times 3\,373 + 0{,}189 \times 2\,720 + 0{,}124 \times 2\,283 $$
$$ = 2\,317{,}3 + 514{,}1 + 283{,}1 = \mathbf{3\,114{,}4}\ \text{€} $$
Le tableau annonce **3 116 €** : un écart de **1,6 €**, soit 0,05 %. Il s'explique par
l'**arrondi des fréquences à une décimale** — les vraies parts ne sont pas exactement 68,7 /
18,9 / 12,4. **Il faut le signaler, pas le masquer.**

**Contrôles.** Les fréquences totalisent 100,0 % dans les deux colonnes ✔ Les moyennes
obtenues sont comprises entre le minimum (2 161 €) et le maximum (3 193 €) des moyennes de
groupe ✔

**Question 2 — sachant qu'il y a 1,8 million d'agents des services de l'État en 2023,
calculez la masse salariale.**

La masse salariale est la **somme** des salaires, c'est-à-dire — propriété utilisée dans
tout le chapitre — **la moyenne multipliée par l'effectif** :
$$ \text{masse salariale} = N \times m = 1\,800\,000 \times 3\,116 = 5\,608\,800\,000\ \text{€} $$

Soit **5,61 milliards d'euros par mois**, et $ \times 12 = $ **67,3 milliards d'euros par
an**.

**Précisions attendues d'une bonne copie :** il s'agit de la masse salariale **nette**
(les salaires du tableau sont nets), **mensuelle** avant multiplication par 12, et pour le
**champ** indiqué — agents fonctionnaires en France hors Mayotte. Sans ces trois précisions,
le chiffre n'est pas interprétable.
:::

::: examen La relation à retenir absolument
$$ \sum_{i=1}^{N} x_i = N \times m $$
**La somme d'une variable est sa moyenne multipliée par l'effectif.** Cette relation servira
trois fois dans le chapitre : ici pour la masse salariale, à la diapositive 57 pour la
variance par agrégation, et à la diapositive 60 pour la part de l'agrégat — le support la
rappelle d'ailleurs explicitement à cet endroit.
:::

#### 2.1.11 Propriété 3 : la moyenne est sensible aux valeurs extrêmes (diapositive 19)

::: definition Ce que dit le support
- « Deux écarts à la moyenne de 5 comptent autant qu'un écart de 10. » En prenant l'exemple
  des notes : **pour quelqu'un qui a une moyenne de 10/20, avoir un 0/20 est aussi pénalisant
  qu'avoir deux 5/20.**
- Pour une distribution **non bornée** et **étalée à droite**, **il suffit d'un écart
  important pour décaler la moyenne de façon non négligeable**. Exemple : **la distribution
  de revenu**.
- **En cas de dissymétrie et de valeurs extrêmes, la médiane est un indicateur beaucoup plus
  stable.**
:::

::: exemple La démonstration chiffrée que le support suggère sans la faire
Dix salariés d'une petite entreprise, salaires mensuels en euros :
1 800, 1 850, 1 900, 1 950, 2 000, 2 050, 2 100, 2 200, 2 300, 2 500.

- **Moyenne** : $ 20\,650 / 10 = 2\,065 $ € ; **médiane** : entre le 5<sup>e</sup> et le
  6<sup>e</sup> rang, soit $ (2\,000 + 2\,050)/2 = 2\,025 $ €.

Le dirigeant, qui se verse **20 000 €**, rejoint l'effectif :
- **Nouvelle moyenne** : $ 40\,650/11 = 3\,695 $ € — elle bondit de **1 630 €, soit +79 %**.
- **Nouvelle médiane** : le rang central des 11 valeurs est le 6<sup>e</sup>, soit
  **2 050 €** — elle bouge de **25 €**.

**Conclusion.** Une seule observation extrême sur onze déplace la moyenne de 79 % et la
médiane de 1,2 %. **Aucun des onze salariés ne gagne 3 695 €** : la moyenne ne décrit plus
personne. C'est exactement pourquoi l'Insee publie des revenus **médians**, et pourquoi la
diapositive 24 s'intitule « revenus salariaux **médians** ».
:::

<!--saut-->
#### 2.1.12 La médiane (diapositive 20)

::: definition La médiane
> C'est la **valeur (modalité) de la variable statistique $ X $ qui coupe la distribution de
> $ X $ en 2 parts égales**, de telle sorte que **la moitié de la population présente un
> caractère inférieur à la médiane** tandis que **l'autre moitié présente un caractère
> supérieur**.

Trois précisions du support :
- Elle s'applique à un caractère **quantitatif ou qualitatif ordonné**.
- **À l'inverse de la moyenne, cet indicateur n'a pas la propriété de linéarité.**
- En économie-gestion, elle est **très utilisée pour les distributions de revenu**.
:::

::: examen Les trois précisions sont trois questions d'examen
1. **« Quantitatif ou qualitatif ordonné »** — la médiane a besoin d'un **ordre**, pas de
   nombres. On peut donc calculer la médiane d'une appréciation (insuffisant < passable <
   bien < très bien), alors qu'on ne peut pas en calculer la moyenne. **C'est la seule
   différence de champ entre moyenne et médiane, et elle est régulièrement testée.**
2. **« Pas de linéarité »** — conséquence majeure, exploitée à la diapositive 24 : on **ne
   peut pas** agréger des médianes de sous-groupes comme on agrège des moyennes.
3. **« Très utilisée pour les distributions de revenu »** — parce que ces distributions sont
   asymétriques et à valeurs extrêmes (propriété 3 de la moyenne).
:::

#### 2.1.13 Calcul de la médiane sur données brutes (diapositive 21)

::: methode L'algorithme
- **Il n'y a pas de formule de calcul.**
- L'algorithme repose sur un **tri préalable** de la série brute.
- La médiane est **la valeur de $ X $ de l'individu correspondant au rang central**.
- **En cas de nombre pair de rangs**, la médiane se situe **à mi-chemin entre les valeurs
  des rangs situés juste autour du rang central**.
:::

::: exemple Les deux cas, en pratique
**$ N $ impair — 7 valeurs : 3, 5, 8, 9, 12, 15, 40.**
Rang central : $ (7+1)/2 = 4^{\text{e}} $ → **médiane = 9**.

**$ N $ pair — 8 valeurs : 3, 5, 8, 9, 12, 15, 22, 40.**
Rangs centraux : 4<sup>e</sup> et 5<sup>e</sup>, soit 9 et 12 → médiane
$ = (9+12)/2 = \mathbf{10{,}5} $.

**Remarquez** que dans le second cas la médiane **n'est pas une valeur observée** — comme la
moyenne. Et que la valeur extrême 40 n'a **aucune influence** sur le résultat : elle occupe
le dernier rang, quelle que soit sa grandeur. C'est toute la robustesse de la médiane.
:::

#### 2.1.14 Application : les densités de population en Union européenne (diapositives 22 et 23)

**Le tableau du support** — Densité de population en Union européenne à 15 et à 25, en
habitants par km².

| Union européenne à 15 (2003) | Densité | Rang | 10 nouveaux pays (2004) | Densité | Rang |
|---|---:|:---:|---|---:|:---:|
| Finlande | 15 | 1 | Estonie | 31 | 1 |
| Suède | 20 | 2 | Lettonie | 36 | 2 |
| Irlande | 57 | 3 | Lituanie | 54 | 3 |
| Espagne | 82 | 4 | Chypre | 97 | 4 |
| Grèce | 83 | 5 | **Slovénie** | **99** | **5** |
| Autriche | 98 | 6 | **Hongrie** | **109** | **6** |
| France métropolitaine | 108 | 7 | Slovaquie | 110 | 7 |
| **Portugal** | **113** | **8** | Pologne | 119 | 8 |
| Danemark | 125 | 9 | République tchèque | 129 | 9 |
| Italie | 190 | 10 | Malte | 1 246 | 10 |
| Luxembourg | 193 | 11 | | | |
| Allemagne | 231 | 12 | | | |
| Royaume-Uni | 242 | 13 | | | |
| Belgique | 341 | 14 | | | |
| Pays-Bas | 397 | 15 | | | |

*Source : Tableaux de l'économie française (TEF), Insee 2004-2005, p. 11, d'après 2003, fiche
de données sur la population mondiale, Population Reference Bureau (PRB).*

::: correction Question 1 — éléments statistiques, médiane et phrase d'interprétation
**Éléments statistiques.**
- **Population** : les **pays** membres de l'Union européenne — 15 pays pour l'UE de 2003,
  10 nouveaux entrants en 2004, 25 au total.
- **Unités statistiques** : **un pays**. *(Point de vigilance : ce ne sont pas des
  habitants — chaque pays compte pour un, quelle que soit sa population.)*
- **Effectif total** : $ N = 15 $, $ N = 10 $ ou $ N = 25 $ selon le champ retenu.
- **Caractère statistique** : la **densité de population** (habitants par km²),
  **quantitatif continu**.

**Médianes** — la série étant déjà triée, il suffit de lire le rang central.
- **UE à 15** : $ N = 15 $, impair ; rang central $ (15+1)/2 = 8 $ → **médiane = 113
  hab/km², le Portugal** (que le support met d'ailleurs en gras).
- **10 nouveaux pays** : $ N = 10 $, pair ; rangs centraux 5 et 6, soit la **Slovénie (99)**
  et la **Hongrie (109)** — toutes deux en gras dans le support → médiane
  $ = (99 + 109)/2 = \mathbf{104} $ hab/km².
- **UE à 25** : en fusionnant et triant les 25 valeurs, le rang central est le 13<sup>e</sup>
  → **médiane = 109 hab/km², la Hongrie**.

**Phrase d'interprétation.**
> « En 2003, la moitié des quinze pays de l'Union européenne avaient une densité de
> population inférieure à **113 habitants par km²**, et l'autre moitié une densité
> supérieure. »
:::

::: correction Question 2 — densité moyenne dans chaque cas, et l'effet de Malte
**Les moyennes.**
- **UE à 15** : $ (15 + 20 + 57 + 82 + 83 + 98 + 108 + 113 + 125 + 190 + 193 + 231 + 242 + 341 + 397)/15 = 2\,295/15 = \mathbf{153{,}0} $ hab/km².
- **10 nouveaux pays** : $ (31 + 36 + 54 + 97 + 99 + 109 + 110 + 119 + 129 + 1\,246)/10 = 2\,030/10 = \mathbf{203{,}0} $ hab/km².
- **UE à 25** : $ (2\,295 + 2\,030)/25 = 4\,325/25 = \mathbf{173{,}0} $ hab/km².

**Le constat qui doit sauter aux yeux.** Chez les 10 nouveaux pays, la **moyenne (203) est
presque le double de la médiane (104)**. Neuf pays sur dix ont une densité inférieure à 130 ;
la moyenne est pourtant à 203. **C'est Malte, avec 1 246 hab/km², qui tire à elle seule la
moyenne vers le haut** — illustration parfaite de la propriété 3 de la diapositive 19.

**Si la densité de Malte est divisée par 2** (1 246 → 623) :

| | Avant | Après | Variation |
|---|---:|---:|---|
| **Médiane** des 10 nouveaux | 104 | **104** | **inchangée** |
| **Moyenne** des 10 nouveaux | 203,0 | **140,7** | **−62,3, soit −31 %** |
| **Médiane** de l'UE à 25 | 109 | **109** | **inchangée** |
| **Moyenne** de l'UE à 25 | 173,0 | **148,1** | **−24,9, soit −14 %** |

**Pourquoi la médiane ne bouge pas.** Malte reste le **dernier rang** après division par
deux (623 > 397, le maximum de l'UE15). Or la médiane ne dépend **que du rang** de
l'observation, pas de sa valeur. Tant que Malte reste au-dessus du rang central, on peut
modifier sa densité comme on veut — la médiane est identique.

**Pourquoi la moyenne s'effondre.** La moyenne dépend de **toutes les valeurs** :
diviser 1 246 par deux retire 623 de la somme, soit $ 623/10 = 62{,}3 $ de la moyenne des dix
nouveaux pays.

**C'est la démonstration la plus nette du chapitre** de ce que signifie « la moyenne est
sensible aux valeurs extrêmes, la médiane est robuste ». À savoir refaire.
:::

#### 2.1.15 Application : les revenus salariaux médians par catégorie (diapositive 24)

**Le graphique du support** — Revenus salariaux **médians** annuels, en euros, des salariés
d'un secteur privé en France métropolitaine en 2023 (diagramme en barres horizontales) :

| Catégorie socioprofessionnelle | Revenu salarial médian annuel |
|---|---:|
| Cadres | 45 552 € |
| Professions intermédiaires | 29 640 € |
| Ouvriers | 23 148 € |
| Employés | 22 572 € |

::: correction Question 1 — éléments statistiques et interprétation
- **Population** : les **salariés** d'un secteur privé en France métropolitaine en 2023.
- **Unités statistiques** : **un salarié**.
- **Sous-populations** : les quatre **catégories socioprofessionnelles**.
- **Caractère statistique** : le **revenu salarial annuel**, **quantitatif continu**.
- **Ce qui est représenté** : non pas une distribution, mais **un indicateur de position — la
  médiane — calculé séparément pour chaque sous-population**.

**Interprétation.**
> « En 2023, la moitié des cadres de ce secteur en France métropolitaine ont perçu un revenu
> salarial annuel inférieur à 45 552 €, l'autre moitié un revenu supérieur. »

**Lecture d'ensemble :** le revenu médian des cadres est **environ le double** de celui des
employés (45 552 contre 22 572, soit un rapport de 2,02). Ouvriers et employés sont très
proches (23 148 contre 22 572, soit 2,6 % d'écart) ; les professions intermédiaires se
situent à mi-chemin.
:::

::: correction Question 2 — peut-on calculer le salaire médian de l'ensemble à partir des parts des CSP ?
**Non.** Et c'est **la** question de la diapositive.

**Pourquoi.** La médiane **n'est pas un opérateur linéaire** — le support l'énonce
diapositive 20. Contrairement à la moyenne, elle ne peut pas être agrégée en pondérant les
médianes de sous-groupes par leurs effectifs. Écrire
$ \text{med} = \sum \frac{n_k}{N}\,\text{med}_k $ serait **faux**.

**La raison profonde :** la médiane dépend du **rang** de chaque observation dans la
distribution **d'ensemble**. Fusionner deux groupes redistribue tous les rangs ; la position
centrale du groupe fusionné n'a aucune raison de se situer entre les positions centrales des
groupes.

**Contre-exemple qui le prouve en trois lignes.** Groupe A : 1, 2, 3 → médiane 2. Groupe B :
100, 200, 300 → médiane 200. Moyenne pondérée des médianes (effectifs égaux) :
$ (2 + 200)/2 = 101 $. **Médiane réelle** de l'ensemble {1, 2, 3, 100, 200, 300} : entre le
3<sup>e</sup> et le 4<sup>e</sup> rang, soit $ (3 + 100)/2 = \mathbf{51{,}5} $. **101 ≠ 51,5.**

**Ce qu'il faudrait pour répondre :** la **distribution complète** des salaires de l'ensemble
de la population — ou au minimum les fréquences cumulées — et non les seules médianes par
catégorie.
:::

#### 2.1.16 Calcul de la médiane à partir d'une distribution (diapositive 25)

::: formule Interpolation linéaire
Lorsque les données sont présentées sous forme de distribution intégrant les **fréquences
cumulées** :
- **si on dispose d'une valeur de $ X $ telle que $ F(x_j) = 50\ \% $, alors la médiane vaut
  $ x_j $** ;
- **dans le cas contraire, on procède par interpolation linéaire.** Si $ F(x_a) < 50\ \% $ et
  $ F(x_b) > 50\ \% $ :

$$ \text{med} \approx x_a + \frac{(x_b - x_a)\,(0{,}5 - F(x_a))}{F(x_b) - F(x_a)} \qquad (9) $$
:::

::: demo Lire la formule plutôt que la mémoriser
La formule est l'interpolation linéaire du §1.3, appliquée à $ F $ :

1. On part de $ x_a $, la dernière modalité **avant** que la fréquence cumulée franchisse
   50 %.
2. On avance sur le segment $ [x_a ; x_b] $ d'une fraction égale à
   $ \dfrac{0{,}5 - F(x_a)}{F(x_b) - F(x_a)} $ : c'est **la part du chemin restant à
   parcourir en ordonnée pour atteindre 50 %, rapportée au chemin total du segment**.
3. Si $ F(x_a) $ vaut déjà 50 %, la fraction est nulle : on reste en $ x_a $ — cohérent avec
   la première règle.

**L'hypothèse cachée, à savoir énoncer :** l'interpolation suppose que les individus sont
**uniformément répartis** à l'intérieur de l'intervalle $ [x_a ; x_b] $. C'est une hypothèse
raisonnable pour une variable **continue découpée en classes**, beaucoup moins pour une
variable **discrète** — voir l'application suivante.
:::

#### 2.1.17 Application : les familles selon le nombre d'enfants (diapositive 26)

**Le tableau du support** — Distribution des familles en France selon le nombre d'enfants :

| Modalités | Effectifs (milliers) en 2008 | Effectifs (milliers) en 2023 |
|---|---:|---:|
| 0 enfant | 8 225 | 9 340 |
| 1 enfant | 3 821 | 4 085 |
| 2 enfants | 3 449 | 3 594 |
| 3 enfants | 1 241 | 1 219 |
| 4 enfants | 396 | 442 |
| **Ensemble** | **17 132** | **18 680** |

::: examen Une confirmation qui vaut d'être notée
Ce tableau est **exactement celui du chapitre 1, diapositive 22** — les cinq effectifs de
2008 sont identiques. Le chapitre 1 ne datait pas cette enquête ; **le chapitre 2 la date
explicitement de 2008**, ce qui confirme la déduction faite alors par comparaison avec le
diagramme de la diapositive 31. Les deux chapitres se recoupent : c'est un bon réflexe de le
vérifier.
:::

::: correction Les deux questions posées, corrigées
**Question 1 — les éléments statistiques.**
- **Population** : les **familles** en France, en 2008 puis en 2023.
- **Unités statistiques** : **une famille**.
- **Effectif total** : 17 132 **milliers** de familles en 2008, 18 680 milliers en 2023.
  *(Attention à l'unité : des milliers, soit 17,1 puis 18,7 millions de familles.)*
- **Sous-populations** : les deux **années** — variable de découpage.
- **Caractère statistique** : le **nombre d'enfants**, **quantitatif discret**.
- **Contrôle** : $ 8\,225 + 3\,821 + 3\,449 + 1\,241 + 396 = 17\,132 $ ✔ et
  $ 9\,340 + 4\,085 + 3\,594 + 1\,219 + 442 = 18\,680 $ ✔

**Question 2 — fréquences cumulées et médiane.**

| Modalité | $ f_i $ 2008 (%) | $ F_i $ 2008 (%) | $ f_i $ 2023 (%) | $ F_i $ 2023 (%) |
|---:|---:|---:|---:|---:|
| 0 enfant | 48,0 | **48,0** | 50,0 | **50,0** |
| 1 enfant | 22,3 | 70,3 | 21,9 | 71,9 |
| 2 enfants | 20,1 | 90,4 | 19,2 | 91,1 |
| 3 enfants | 7,2 | 97,7 | 6,5 | 97,6 |
| 4 enfants | 2,3 | 100,0 | 2,4 | 100,0 |

*Détail : $ 8\,225/17\,132 = 48{,}0\ \% $ ; $ 9\,340/18\,680 = 50{,}0\ \% $ — exactement la
moitié.*

**Médiane 2023.** $ F(0) = 50{,}0\ \% $ : on est dans le **premier cas** de la formule — il
existe une modalité telle que $ F(x_j) = 50\ \% $. Donc **la médiane vaut 0 enfant**.
Lecture : *« en 2023, la moitié des familles de France n'avaient aucun enfant »*.

**Médiane 2008.** $ F(0) = 48{,}0\ \% < 50\ \% $ et $ F(1) = 70{,}3\ \% > 50\ \% $ : on est
dans le **second cas**. En appliquant la formule (9) avec $ x_a = 0 $, $ x_b = 1 $ :

$$ \text{med} \approx 0 + \frac{(1 - 0)(0{,}50 - 0{,}480)}{0{,}703 - 0{,}480}
= \frac{0{,}020}{0{,}223} = 0{,}09 $$
:::

::: piege Le résultat 0,09 enfant doit vous alerter — et voici pourquoi
**Aucune famille n'a 0,09 enfant.** Le nombre d'enfants est une variable **quantitative
discrète**, et l'interpolation linéaire suppose une répartition **continue et uniforme**
entre 0 et 1 enfant — ce qui n'a aucun sens ici : il n'existe rien entre zéro et un enfant.

**Les deux lectures, et celle qu'il faut retenir :**

| Méthode | Résultat 2008 | Statut |
|---|---|---|
| **Interpolation** (formule 9 du cours) | 0,09 enfant | La formule du cours, appliquée mécaniquement |
| **Rang central** (définition de la diapo 21) | **1 enfant** | Le rang central est le 8 566<sup>e</sup> millier ; les 8 225 premiers ont 0 enfant, donc le rang central tombe dans « 1 enfant » |

**Conduite à tenir en examen :** appliquez **la formule du cours** — c'est elle qui est
enseignée et corrigée — mais **ajoutez la phrase qui montre que vous en connaissez la
limite** : « l'interpolation suppose une répartition continue ; le caractère étant discret,
la médiane au sens du rang central vaut 1 enfant ». C'est exactement ce qui distingue une
copie mécanique d'une copie qui comprend.

**Le même avertissement vaut pour 2023 :** le cas $ F = 50\ \% $ pile est un cas limite ; au
sens du rang central avec $ N $ pair, on obtiendrait $ (0+1)/2 = 0{,}5 $. Le cours tranche
pour **0 enfant**, et c'est cette réponse qu'il faut donner.
:::

::: examen Ce que le tableau raconte, au-delà du calcul
Entre 2008 et 2023, la part des familles **sans enfant** passe de 48,0 % à 50,0 % — elle
franchit la barre de la moitié. Celle des familles de **3 enfants** recule de 7,2 % à 6,5 %.
**La médiane bascule de « 1 enfant » à « 0 enfant »** : c'est un basculement de structure que
la moyenne aurait masqué. Une question de commentaire peut porter là-dessus ; la réponse
mobilise les fréquences **et** l'indicateur de position.
:::

<!--saut-->
### 2.2 — Résumer la dispersion des données

#### 2.2.1 Pourquoi la position ne suffit pas : les quatre cas (diapositive 27)

::: definition L'expérience de pensée du support
Une classe de **50 élèves**, dont la **moyenne est 12/20** dans les quatre cas :

- **Cas n° 1** : les 50 élèves ont obtenu 12/20.
- **Cas n° 2** : 5 élèves ont 7, 5 ont 8, 5 ont 9, 5 ont 10, 5 ont 11, 5 ont 13, 5 ont 14,
  5 ont 15, 5 ont 16, 5 ont 17.
- **Cas n° 3** : 20 élèves ont eu 6, 20 élèves ont eu 18 et 10 élèves ont eu 12.
- **Cas n° 4** : 5 élèves ont eu 4, 10 ont eu 8, 10 ont eu 10, 10 ont eu 14, 10 ont eu 16 et
  5 ont eu 20.

**Dans quel cas la distribution des notes est-elle la plus dispersée ?**

Le support conclut : « il y a **plusieurs façons d'envisager la mesure de la dispersion**
d'une série de données — point de référence, pondération de la valeur des écarts, pondération
des effectifs, etc. »
:::

::: demo Vérifions d'abord que les quatre cas ont bien la même moyenne
C'est le point de départ de toute la partie 2 : **la position ne dit rien de la dispersion**.

- Cas 1 : $ 50 \times 12 / 50 = 12 $ ✔
- Cas 2 : $ 5(7+8+9+10+11+13+14+15+16+17)/50 = 5 \times 120/50 = 12 $ ✔
- Cas 3 : $ (20 \times 6 + 20 \times 18 + 10 \times 12)/50 = 600/50 = 12 $ ✔
- Cas 4 : $ (5 \times 4 + 10 \times 8 + 10 \times 10 + 10 \times 14 + 10 \times 16 + 5 \times 20)/50 = 600/50 = 12 $ ✔

**Quatre classes, une seule moyenne, quatre réalités radicalement différentes** : dans la
première, personne n'est en difficulté ; dans la troisième, la classe est coupée en deux
blocs qui ne se ressemblent pas. **Un enseignant qui ne connaîtrait que la moyenne ne verrait
aucune différence.** C'est exactement la limite du chapitre sur la position.
:::

#### 2.2.2 L'étendue (diapositive 28)

::: definition L'étendue
> L'étendue d'une série est la **différence entre le maximum et le minimum** de la série.

- Exemple du support : les notes dans une classe vont de 3 à 17 → **l'étendue vaut 14**.
- Il s'agit d'une **amplitude calculée sur l'intégralité de la série**.
- Cet indicateur, **très simple, ne rend compte que des extrêmes**.
- Il est donc **par définition sensible aux grandeurs extrêmes**.
:::

::: exemple Les étendues des quatre cas
| | Minimum | Maximum | **Étendue** |
|---|---:|---:|---:|
| Cas 1 | 12 | 12 | **0** |
| Cas 2 | 7 | 17 | **10** |
| Cas 3 | 6 | 18 | **12** |
| Cas 4 | 4 | 20 | **16** |

**Selon l'étendue, le cas 4 est le plus dispersé.** Retenez ce classement : les indicateurs
suivants ne donneront **pas tous la même réponse**, et c'est précisément la leçon du support.
:::

#### 2.2.3 Les écarts inter-quantiles (diapositive 29)

::: definition L'écart inter-centiles et ses variantes
> L'écart inter-centiles correspond à un indicateur d'**étendue d'une distribution tronquée**
> (on a enlevé des données les 1 % les plus faibles et les 1 % les plus forts). C'est la
> différence entre le centile **C99** et le centile **C1**.

- De façon équivalente, l'**écart inter-déciles D9 − D1**, auquel cas c'est **20 % de la
  population qui est sortie** de l'indicateur.
- Ou l'**écart inter-quartile Q3 − Q1**, qui s'intéresse à l'amplitude entre le maximum et
  le minimum des **50 % de la population situés au centre** de la distribution, autour de la
  médiane.
- Les écarts inter-quantiles peuvent aussi se calculer **de façon relative**, c'est-à-dire
  **sous forme de ratio** : D9/D1, etc.
:::

::: demo Pourquoi tronquer, et ce que change le passage à l'écart relatif
**Pourquoi tronquer.** L'étendue est fondée sur deux observations seulement, les plus
atypiques de la série. Une seule valeur aberrante — une erreur de saisie, un cas
exceptionnel — la fait exploser. **Tronquer les extrêmes rend l'indicateur robuste** : c'est
la même idée que la médiane, appliquée à la dispersion.

**Combien on retire :**
| Indicateur | Part de la population exclue | Ce qui reste |
|---|:---:|---|
| Étendue | 0 % | Toute la série, extrêmes compris |
| C99 − C1 | **2 %** (1 % de chaque côté) | 98 % du centre |
| D9 − D1 | **20 %** (10 % de chaque côté) | 80 % du centre |
| Q3 − Q1 | **50 %** (25 % de chaque côté) | La **moitié centrale** |

**Écart absolu ou ratio ?** L'écart D9 − D1 s'exprime **dans l'unité des données** (des
euros) ; le ratio D9/D1 est **sans unité**. Conséquence pratique majeure : **seul le ratio
permet de comparer des populations de niveaux très différents**. Comparer l'écart D9 − D1 des
cadres et des employés mélange l'inégalité et le niveau de salaire ; comparer D9/D1 isole
l'inégalité. On retrouvera cette idée avec le **coefficient de variation** (§2.2.13).
:::

#### 2.2.4 Les quantiles (diapositives 30 et 31)

::: definition Les quantiles, généralisation de la médiane
> Les quantiles se comprennent comme une **généralisation de la notion de médiane**.

| Quantiles | Nombre de parts égales | Points de découpe |
|---|:---:|---|
| **Médiane** | 2 | 50 % en dessous, 50 % au-dessus |
| **Quartiles** | 4 | 25 % sous Q1, 25 % entre Q1 et Q2, 25 % entre Q2 et Q3, 25 % au-dessus de Q3 |
| **Déciles** | 10 | 10 % sous D1, …, 10 % au-dessus de D9 |
| **Centiles** | 100 | 1 % sous C1, …, 1 % au-dessus de C99 |
:::

::: definition Interprétation d'un quantile
> Le quantile d'ordre $ x\ \% $ correspond au **niveau de la variable $ X $ tel que
> $ x\ \% $ de la population dispose d'une modalité de la variable inférieure à $ q $**.

- Le quantile d'ordre 10 % est le premier décile **D1**.
- Le quantile d'ordre 50 % est la **médiane**.
- Le quantile d'ordre 75 % est le troisième quartile **Q3**.
- Le quantile d'ordre 4 % est le quatrième centile **C4**.
- **Si $ q $ est le quantile d'ordre $ \alpha\ \% $, alors $ \alpha\ \% $ de la population a
  une valeur de $ X $ inférieure à $ q $.**

**Et le support ajoute la formulation la plus profonde du chapitre :**
> Il s'agit aussi de **l'inverse de la fonction de répartition empirique**. Si
> $ F(q) = \alpha $ alors $ q = F^{-1}(\alpha) $.
:::

::: demo « L'inverse de la fonction de répartition » — ce que cela signifie vraiment
Le chapitre 1 a construit les **fréquences cumulées** $ F $ : on part d'une **valeur** et on
obtient une **proportion**. « Quelle part de la population a au plus 2 frères et sœurs ? »
→ $ F(2) = 77\ \% $.

Le quantile fait **exactement le trajet inverse** : on part d'une **proportion** et on obtient
une **valeur**. « Quelle valeur laisse 77 % de la population en dessous ? » → 2.

$$ F : \text{valeur} \longrightarrow \text{proportion}
\qquad\qquad F^{-1} : \text{proportion} \longrightarrow \text{valeur} $$

**Ce sont deux lectures de la même colonne** — celle des fréquences cumulées — dans un sens
puis dans l'autre. C'est pourquoi le calcul des quantiles (diapositive 33) est la même
interpolation que celui de la médiane (diapositive 25) : la médiane **est** le quantile
d'ordre 50 %.
:::

::: marche
$ F^{-1} $ est l'outil quotidien de la gestion du risque. La *Value at Risk* à 99 % sur un
horizon d'un jour est le **quantile d'ordre 1 %** de la distribution des variations
quotidiennes : la perte qui n'est dépassée qu'un jour sur cent. Vous savez désormais la
calculer par interpolation. La suite du raisonnement — pourquoi ce quantile est
systématiquement sous-estimé sur données réelles — tient aux **queues épaisses** des
distributions financières, et c'est là que l'inégalité de Bienaymé-Tchebychev (§2.2.10)
devient précieuse : elle, elle ne suppose aucune loi.
:::

#### 2.2.5 Application des indicateurs aux quatre cas (diapositive 32)

::: definition Les résultats donnés par le support
- **Cas n° 1** : **tous les indicateurs sont à 0** (aucune dispersion).
- **Cas n° 2** : l'étendue vaut $ 17 - 7 = 10 $ ; $ D9 - D1 = 16 - 7 = 9 $ ;
  $ Q3 - Q1 = 14{,}5 - 8{,}5 = 6 $.
- **Cas n° 3** : l'étendue vaut $ 18 - 6 = 12 $ ; **calcul des déciles par interpolation
  difficile car choix à faire sur le support**.
- **Cas n° 4** : l'étendue vaut $ 20 - 4 = 16 $ ; $ D9 - D1 = 16 - 4 = 12 $ ;
  $ Q3 - Q1 = 14{,}5 - 7 = 7{,}5 $.

**Conclusion du support : « on constate que les indicateurs ne vont pas tous dans le même
sens, loin de là ! »**
:::

::: examen La phrase la plus importante de la partie 2
« Les indicateurs ne vont pas tous dans le même sens. » Regardons :

| | Étendue | D9 − D1 | Q3 − Q1 |
|---|---:|---:|---:|
| Cas 2 | 10 | 9 | **6** |
| Cas 3 | **12** | *(indéterminé)* | *(indéterminé)* |
| Cas 4 | **16** | **12** | 7,5 |

Selon l'**étendue**, le cas 4 est le plus dispersé. Mais le cas 3 — deux blocs à 6 et 18 —
est visiblement le plus **polarisé**, et c'est lui qui aura la plus forte **variance**
(§2.2.12). **Chaque indicateur mesure une idée différente de la dispersion :** l'étendue
mesure l'écartement des extrêmes, l'écart inter-quantiles la largeur du centre, la variance
l'éloignement moyen à la moyenne.

**Ce que dit le support sur le cas 3, et qu'il faut comprendre :** « choix à faire sur le
support ». Avec seulement trois valeurs distinctes (6, 12, 18), un décile tombe *à
l'intérieur* d'un bloc d'observations identiques ; l'interpolation exige alors de décider
quelle largeur attribuer à ce bloc — une convention, non un calcul. **C'est une limite des
quantiles sur les distributions très discrètes**, à savoir signaler.
:::

#### 2.2.6 Calcul d'un quantile à partir d'une distribution (diapositive 33)

::: formule Le quantile d'ordre α %
Lorsque les données sont présentées sous forme de distribution intégrant les fréquences
cumulées :
- **si** on dispose d'une valeur de $ X $ telle que $ F(x_j) = \alpha\ \% $, **alors le
  quantile vaut $ x_j $** ;
- **sinon**, par interpolation linéaire, si $ F(x_a) < \alpha\ \% $ et $ F(x_b) > \alpha\ \% $ :

$$ Q_{\alpha\%} \approx x_a + \frac{(x_b - x_a)\,(\alpha\% - F(x_a))}{F(x_b) - F(x_a)} \qquad (10) $$
:::

::: examen C'est la formule (9), avec α à la place de 50 %
Comparez les formules (9) et (10) : elles sont **identiques**, à ceci près que $ 0{,}5 $ est
remplacé par $ \alpha\% $. **Il n'y a donc qu'une seule formule à retenir dans tout le
chapitre**, celle de l'interpolation linéaire — la médiane en est le cas particulier
$ \alpha = 50\ \% $.

**Méthode en trois temps, valable pour tous les quantiles :**
1. Construire la colonne des **fréquences cumulées**.
2. Repérer les deux modalités qui **encadrent** $ \alpha\ \% $.
3. Appliquer l'interpolation.
:::

#### 2.2.7 Interpréter des quantiles : le niveau de vie (diapositives 34 et 35)

**Le tableau du support** — Répartition du niveau de vie en France, Enquête Revenus Fiscaux
et Sociaux :

| Indicateur | Niveau de vie en 2024 (€ par UC) |
|---|---:|
| D1 | 13 970 |
| D2 | 17 700 |
| D3 | 20 980 |
| D4 | 23 880 |
| **D5** | **26 740** |
| D6 | 29 880 |
| D7 | 33 680 |
| D8 | 38 780 |
| D9 | 48 580 |
| C95 (ou P95) | 61 220 |

::: methode « € par UC » — un sigle non explicité par le support
**UC = unité de consommation.** On ne compare pas directement les revenus de deux ménages de
tailles différentes : un couple avec deux enfants n'a pas besoin de quatre fois le revenu
d'une personne seule pour vivre aussi bien, parce que certaines dépenses sont partagées —
logement, chauffage, équipement.

Le **niveau de vie** rapporte donc le revenu du ménage à un nombre d'**unités de
consommation** qui pondère ses membres (par convention courante : 1 pour le premier adulte,
0,5 pour les autres personnes de 14 ans et plus, 0,3 pour les enfants de moins de 14 ans).
**Tous les membres d'un même ménage ont ainsi le même niveau de vie.** C'est ce qui rend les
déciles comparables d'un ménage à l'autre.
:::

::: correction Interpréter ces quantiles — ce que l'oral développe
**Trois phrases de lecture à savoir produire :**
> « En 2024, **10 % des personnes** ont un niveau de vie **inférieur à 13 970 €** par unité
> de consommation. » *(D1)*
> « La moitié de la population a un niveau de vie inférieur à **26 740 €** — c'est la
> **médiane**. » *(D5)*
> « **5 % des personnes** ont un niveau de vie **supérieur à 61 220 €**. » *(C95, lu par
> complément)*

**Le rapport inter-décile :** $ D9/D1 = 48\,580 / 13\,970 = \mathbf{3{,}48} $. Lecture : les
10 % les plus aisés ont un niveau de vie **au moins 3,5 fois supérieur** au plafond des 10 %
les plus modestes.

**L'asymétrie, que le support demande de déduire des écarts.** Calculons les écarts entre
déciles successifs :

| Écart | Valeur (€) | | Écart | Valeur (€) |
|---|---:|---|---|---:|
| D2 − D1 | 3 730 | | D6 − D5 | 3 140 |
| D3 − D2 | 3 280 | | D7 − D6 | 3 800 |
| D4 − D3 | 2 900 | | D8 − D7 | 5 100 |
| D5 − D4 | 2 860 | | D9 − D8 | **9 800** |
| | | | C95 − D9 | **12 640** |

**Les écarts se resserrent jusqu'au milieu de la distribution (minimum de 2 860 € entre D4 et
D5), puis s'écartent brutalement vers le haut** : le passage de D8 à D9 vaut à lui seul plus
de trois fois le passage de D4 à D5, et les cinq derniers centiles couvrent 12 640 €.

**C'est la signature d'une distribution étalée à droite** — asymétrique positive. Elle
confirme la propriété 3 de la moyenne : sur une telle distribution, **la moyenne est
supérieure à la médiane**, et c'est pourquoi on publie des niveaux de vie **médians**.
:::

::: piege Une incohérence de la diapositive 35 — à connaître
La diapositive 35, intitulée **« Revenus déclarés par déciles et centiles des individus
retraités, année 2008 »**, affiche un graphique dont le titre interne est « Niveau de vie par
UC (en €) » et dont les **dix valeurs sont exactement celles du tableau de la diapositive
34** (13 970, 17 700, …, 61 220), lesquelles portent sur **le niveau de vie de l'ensemble de
la population en 2024**.

**Le titre de la diapositive et les données affichées ne correspondent donc pas.** Il s'agit
très probablement d'un titre resté d'une version antérieure du diaporama.

**Conduite à tenir :** retenez les **valeurs** et la **méthode de lecture** — c'est cela qui
est enseigné — et signalez à l'enseignante l'écart de titre. Ne construisez surtout pas une
interprétation « sur les retraités en 2008 » à partir de ces chiffres.
:::

#### 2.2.8 La représentation graphique : le *boxplot* (diapositives 36 et 37)

::: definition La boîte à moustaches
> Le graphique **boxplot** ou **boîte à moustaches** permet une **représentation résumée de
> la distribution** d'un caractère statistique.

- **Au centre de la boîte** : la **médiane**.
- **Les contours de la boîte** : les **1<sup>er</sup> et 3<sup>e</sup> quartiles**.
- **Les moustaches** : **peuvent varier selon les logiciels** — 1,5 fois l'écart
  interquartile, déciles 1 et 9, etc.
- Ce graphique permet de **visualiser assez bien les asymétries** des distributions ; il est
  **intéressant pour comparer plusieurs distributions**.
:::

**Le schéma du support (diapositive 37)** porte les annotations suivantes : la boîte est
bornée par $ Q_1 $ et $ Q_3 $, coupée par un trait vertical marqué **Mé** (la médiane) ; la
largeur de la boîte est notée **IQR = Q₃ − Q₁** ; une flèche indique **1,5 × IQR** au-delà de
$ Q_3 $ ; les moustaches se terminent par un trait vertical ; et un point isolé, à droite,
est étiqueté **« valeur atypique »**. L'axe horizontal est gradué de 30 à 80.

::: demo Lire un boxplot en quatre informations
| Ce que l'on regarde | Ce que cela dit |
|---|---|
| **La position du trait central** | La médiane — où se situe la distribution |
| **La largeur de la boîte** (IQR) | La dispersion des **50 % centraux** |
| **La position du trait central *dans* la boîte** | L'**asymétrie** : décalé à gauche → distribution étalée à droite |
| **Les points au-delà des moustaches** | Les **valeurs atypiques** (*outliers*) |

**Sur le schéma du support**, la médiane est légèrement décalée vers la droite de la boîte, et
la moustache droite est plus longue que la gauche, avec une valeur atypique isolée vers 80.

**La règle des 1,5 × IQR**, très répandue, mérite d'être connue : les moustaches s'arrêtent à
la dernière observation située à moins de $ 1{,}5 \times \text{IQR} $ du bord de la boîte ;
au-delà, les points sont tracés individuellement comme atypiques. **Mais le support prévient
que la convention varie selon les logiciels** — d'où la nécessité de toujours préciser, en
légende, ce que représentent les moustaches.
:::

::: marche
Le boxplot est l'outil standard de comparaison de distributions de rendements entre actifs,
périodes ou stratégies : il montre d'un coup d'œil la médiane, la dispersion centrale,
l'asymétrie et les points extrêmes. Sur des séries financières, **la queue des observations
atypiques est précisément l'information la plus importante** — celle qu'un résumé par
moyenne et écart-type efface.
:::

#### 2.2.9 Interpréter des quantiles par catégorie (diapositive 38)

**Le tableau du support** — salaires, source Insee, tous salariés en France hors Mayotte
(* les chefs d'entreprise salariés sont inclus dans les cadres) :

| | Ensemble | Cadres* | Professions intermédiaires | Employés | Ouvriers |
|---|---:|---:|---:|---:|---:|
| D1 | 1 440 | 2 240 | 1 640 | 1 380 | 1 380 |
| Q1 | 1 660 | 2 810 | 1 940 | 1 510 | 1 570 |
| D5 | 2 090 | 3 620 | 2 360 | 1 730 | 1 830 |
| Q3 | 2 880 | 4 930 | 2 890 | 2 060 | 2 200 |
| D9 | 4 160 | 7 060 | 3 590 | 2 520 | 2 630 |
| **D9 − D1** | **2 720** | **4 820** | **1 950** | **1 140** | **1 250** |
| **D9/D1** | **2,9** | **3,2** | **2,2** | **1,8** | **1,9** |

::: correction La question posée : dans quelle CSP les salaires sont-ils le plus dispersés ? Le moins ?
**Les deux indicateurs concordent ici**, ce qui n'est pas toujours le cas :

- **Les plus dispersés : les cadres.** Écart absolu le plus élevé
  ($ D9 - D1 = 4\,820 $ €) **et** ratio le plus élevé ($ D9/D1 = 3{,}2 $).
- **Les moins dispersés : les employés.** Écart absolu le plus faible (1 140 €) **et** ratio
  le plus faible (1,8).

**Vérification des calculs du tableau :** cadres $ 7\,060 - 2\,240 = 4\,820 $ ✔ et
$ 7\,060/2\,240 = 3{,}15 \to 3{,}2 $ ✔ ; employés $ 2\,520 - 1\,380 = 1\,140 $ ✔ et
$ 2\,520/1\,380 = 1{,}83 \to 1{,}8 $ ✔

**Pourquoi il faut regarder les deux indicateurs.** L'écart absolu mélange **inégalité** et
**niveau** : les cadres gagnent plus, donc leurs écarts en euros sont mécaniquement plus
grands. Le ratio neutralise le niveau. Ici les deux classements coïncident, ce qui **renforce**
la conclusion ; s'ils divergeaient, il faudrait dire lequel répond à la question posée.
:::

::: examen Le détail que presque personne ne relève — et qui vaut beaucoup
**L'écart inter-décile de l'ensemble (2 720 €) est supérieur à celui de trois CSP sur
quatre**, et son ratio (2,9) est supérieur à celui de toutes les CSP sauf les cadres.

**Pourquoi ?** Parce que la dispersion de l'ensemble contient **deux sources** : la
dispersion **à l'intérieur** de chaque catégorie **et** l'écart **entre** les catégories —
un ouvrier médian gagne 1 830 €, un cadre médian 3 620 €, soit le double.

**C'est exactement la décomposition intra / inter de la diapositive 58**, rencontrée ici sans
être nommée. Un total peut être plus inégalitaire que chacune de ses parties, parce que les
parties diffèrent entre elles. Faire ce rapprochement dans une copie montre qu'on a lu le
chapitre comme un tout.
:::

<!--saut-->
#### 2.2.10 Les indicateurs fondés sur les écarts à la moyenne (diapositives 39 à 41)

::: definition Le plan de la seconde moitié (diapositive 39)
> La notion de dispersion ayant un **contour flou**, il y a de multiples façons de la définir
> et de la mesurer.

**Après** les indicateurs fondés sur les écarts entre 2 indicateurs — étendue, écart ou
ratio interdéciles, écart ou ratio interquartiles — viennent **les indicateurs qui comparent
l'ensemble des valeurs à la moyenne** : l'**écart absolu moyen**, la **variance**,
l'**écart-type**.
:::

::: demo La différence de nature entre les deux familles
| | **Première famille** (étendue, quantiles) | **Seconde famille** (EAM, variance, écart-type) |
|---|---|---|
| **Combien d'observations utilisées** | **Deux** (les deux bornes) | **Toutes** |
| **Point de référence** | Aucun — on compare deux quantiles entre eux | **La moyenne** |
| **Robustesse** | Forte pour les quantiles, nulle pour l'étendue | **Faible** : hérite de la sensibilité de la moyenne |
| **Information utilisée** | Les **rangs** | Les **valeurs** |

**Conséquence à retenir :** une série peut avoir un faible écart inter-quartile — un centre
très resserré — et une variance élevée, si quelques observations sont très éloignées.
**Les deux familles ne sont pas redondantes : elles se complètent.**
:::

::: definition Le principe du calcul (diapositive 40)
Le calcul peut se faire à partir de **données brutes** ou de données **représentées sous
forme de distribution**.
- **Il y a donc plusieurs formules pour un même concept**, selon la façon dont les données
  sont présentées.
- Sur **données brutes** : une moyenne fondée sur **$ N $ écarts calculés observation par
  observation**.
- Sur **distribution** : une moyenne calculée sur l'ensemble des **$ p $ modalités**,
  **pondérée par les effectifs** observés pour chaque modalité.
:::

::: formule Les trois colonnes du tableau de calcul (diapositive 41)
Soit $ m_X $ la moyenne de $ X $, et $ i = 1, \ldots, N $ observations $ x_i $ :

| Colonne | Contenu | Notation |
|:---:|---|---|
| (1) | La série **ordonnée** | $ x_i $ |
| (2) | L'**écart à la moyenne** | $ y_i = x_i - m_X $ |
| (3) | L'**écart absolu** à la moyenne | $ z_i = \|x_i - m_X\| $ |
| (4) | Le **carré de l'écart** à la moyenne | $ w_i = (x_i - m_X)^2 $ |

« C'est ainsi que l'on obtient un tableau de calcul contenant **$ N $ lignes**. »
:::

#### 2.2.11 Le tableau de calcul en pratique (diapositives 42 et 43)

**Le tableau du support** porte sur une **série de 20 âges**. En voici le contenu intégral :

| $ x_i $ | $ y_i = x_i - m_X $ | $ z_i = \|x_i - m_X\| $ | $ w_i = (x_i - m_X)^2 $ |
|---:|---:|---:|---:|
| 30,0 | −17,9 | 17,9 | 320,4 |
| 36,0 | −11,9 | 11,9 | 141,6 |
| 41,0 | −6,9 | 6,9 | 47,6 |
| 42,0 | −5,9 | 5,9 | 34,8 |
| 42,0 | −5,9 | 5,9 | 34,8 |
| 44,0 | −3,9 | 3,9 | 15,2 |
| 46,0 | −1,9 | 1,9 | 3,6 |
| 47,0 | −0,9 | 0,9 | 0,8 |
| 47,0 | −0,9 | 0,9 | 0,8 |
| 47,0 | −0,9 | 0,9 | 0,8 |
| 48,0 | 0,1 | 0,1 | 0,0 |
| 49,0 | 1,1 | 1,1 | 1,2 |
| 50,0 | 2,1 | 2,1 | 4,4 |
| 52,0 | 4,1 | 4,1 | 16,8 |
| 52,0 | 4,1 | 4,1 | 16,8 |
| 54,0 | 6,1 | 6,1 | 37,2 |
| 55,0 | 7,1 | 7,1 | 50,4 |
| 57,0 | 9,1 | 9,1 | 82,8 |
| 58,0 | 10,1 | 10,1 | 102,0 |
| 61,0 | 13,1 | 13,1 | 171,6 |
| **$ m_X = 47{,}9 $** | **$ m_Y = 0{,}0 $** | **$ m_Z = 5{,}7 $** | **$ m_W = 54{,}2 $** |

::: formule Les trois indicateurs, lus au bas des colonnes (diapositive 43)
**Colonne 3 — l'écart absolu moyen :**
$$ \text{EAM} = \frac{1}{N} \sum_{i=1}^{N} |x_i - m_X| = 5{,}7 $$
Lecture du support : « **les âges s'écartent en moyenne de l'âge moyen (47,9 ans) de
5,7 années** ».

**Colonne 4 — la variance :**
$$ \sigma^2 = V(X) = \frac{1}{N} \sum_{i=1}^{N} (x_i - m_X)^2 = 54{,}2 $$
« La variance vaut 54,2, elle **n'est pas d'une interprétation aisée** puisque les écarts
d'âge sont mesurés **au carré**. »

**L'écart-type :**
$$ \sigma = \sqrt{V(X)} = \sqrt{\frac{1}{N} \sum_{i=1}^{N} (x_i - m_X)^2} $$
« **est ici interprétable puisque mesuré en années** ».
:::

::: exemple Vérification intégrale des quatre colonnes
J'ai recalculé la série complète : 30, 36, 41, 42, 42, 44, 46, 47, 47, 47, 48, 49, 50, 52,
52, 54, 55, 57, 58, 61.

- **$ N = 20 $** observations ✔
- **Moyenne** : somme $ = 958 $, donc $ m = 958/20 = \mathbf{47{,}9} $ ✔
- **Colonne 2** : moyenne des écarts $ = \mathbf{0{,}0} $ ✔ — c'est la **propriété 1** de la
  diapositive 16, vérifiée numériquement.
- **Colonne 3** : $ \text{EAM} = \mathbf{5{,}70} $ ✔
- **Colonne 4** : $ \sigma^2 = \mathbf{54{,}19} $, arrondi à **54,2** ✔
- **Écart-type** : $ \sigma = \sqrt{54{,}19} = \mathbf{7{,}36} $ ans — **le support ne le
  calcule pas, il faut le faire.**

**Lecture complète, à savoir produire :**
> « L'âge moyen est de 47,9 ans, avec un écart-type de 7,4 ans. Les âges s'écartent donc de
> l'âge moyen d'environ 7 ans en ordre de grandeur. »
:::

::: piege EAM et écart-type : pourquoi 5,7 et 7,4 diffèrent
Les deux mesurent « l'écart moyen », et pourtant ils ne donnent pas le même nombre.
**L'écart-type est toujours supérieur ou égal à l'écart absolu moyen.**

**La raison** : le carré **pénalise davantage les grands écarts**. Un écart de 17,9 ans
contribue $ 17{,}9 $ à l'EAM mais $ 320{,}4 $ à la variance, soit **56 fois plus** que
l'écart de 0,1 an — alors qu'il n'est que 179 fois plus grand en valeur absolue… mais 32 000
fois plus grand une fois élevé au carré. **L'élévation au carré donne un poids
disproportionné aux observations éloignées.**

**Pourquoi alors préférer l'écart-type à l'EAM, qui est plus intuitif ?** Trois raisons, dont
la première est celle du cours :
1. La variance possède des **propriétés algébriques** que la valeur absolue n'a pas : formule
   de Koenig, décomposition intra/inter, additivité. On ne saurait rien démontrer avec l'EAM.
2. L'écart-type intervient dans l'**inégalité de Bienaymé-Tchebychev** (§2.2.12), qui lui
   donne une interprétation chiffrée.
3. C'est la convention universelle en finance et en économétrie.
:::

#### 2.2.12 L'interprétation de l'écart-type : l'inégalité de Bienaymé-Tchebychev (diapositive 44)

::: formule L'inégalité
> C'est l'inégalité d'**Irénée-Jules Bienaymé** et **Pafnouti Tchebychev** qui va permettre
> d'interpréter l'écart-type en lien avec la moyenne.

**Pour $ k > 1 $, l'intervalle $ [m - k\sigma\ ;\ m + k\sigma] $ contient au moins
$ 1 - 1/k^2 $ des observations.**

| $ k $ | $ 1 - 1/k^2 $ | Énoncé |
|:---:|:---:|---|
| **2** | 0,75 | **Au moins 75 %** des observations sont dans $ m \pm 2\sigma $ |
| **3** | ≈ 0,89 | **Au moins 89 %** des observations sont dans $ m \pm 3\sigma $ |

« C'est **très pratique quand on ne nous donne qu'une moyenne et un écart-type** pour résumer
des données. »
:::

::: demo Ce que l'inégalité apporte, et ce qu'elle n'apporte pas
**Ce qu'elle apporte — une garantie sans hypothèse.** Elle est vraie pour **n'importe quelle
distribution** : symétrique ou non, à une ou plusieurs bosses, à queues épaisses. C'est
extrêmement rare en statistique, et c'est ce qui en fait un outil de sécurité.

**Application sur la série des âges** ($ m = 47{,}9 $, $ \sigma = 7{,}36 $) :
- $ m \pm 2\sigma = [33{,}2\ ;\ 62{,}6] $ → au moins **75 %** des âges, soit 15 personnes sur
  20, y sont. *(Vérification : 19 des 20 âges y sont, soit 95 % — l'inégalité est bien
  respectée, et largement.)*
- $ m \pm 3\sigma = [25{,}8\ ;\ 70{,}0] $ → au moins **89 %**. *(En fait 100 % ici.)*

**Ce qu'elle n'apporte pas — la précision.** Le mot « **au moins** » est essentiel :
l'inégalité donne un **minorant**, pas une valeur. Sur la série des âges, elle garantit 75 %
là où la réalité est à 95 %. **Elle ne se trompe jamais, mais elle est très prudente.**

**Et le piège à éviter absolument :** ne confondez pas ces bornes avec la fameuse règle
« 95 % dans $ m \pm 2\sigma $ », qui suppose une distribution **normale**. Bienaymé-Tchebychev
ne suppose rien et donne 75 % ; la loi normale suppose beaucoup et donne 95 %. **Sur des
données réelles — en particulier financières — la première est fiable, la seconde optimiste.**
:::

::: marche
Cette différence est l'une des causes documentées des grandes pertes de marché : les modèles
de risque calibrés sur l'hypothèse normale attribuent aux mouvements extrêmes des
probabilités infinitésimales, alors que les rendements réels présentent des **queues
épaisses**. Bienaymé-Tchebychev, qui ne suppose aucune loi, fournit une borne toujours
valable — au prix d'être très large. Retenir cette opposition « borne universelle mais large
contre estimation précise mais conditionnelle » est plus utile, pour un professionnel du
risque, que n'importe quelle formule du chapitre.
:::

#### 2.2.13 Application en finance : l'écart-type devient la volatilité (diapositives 45 à 48)

::: definition Le cadre posé par le support
> L'écart-type, très utilisé, **s'interprète comme un indicateur de volatilité des séries
> financières**.

- **La rentabilité journalière est le taux de variation entre le prix du jour et celui de la
  veille.**
- **Le risque associé peut se calculer sur un intervalle de jours** (par exemple ici
  22 jours).
- **On va donc avoir un double indicateur qui nous donnera nos chances de succès.**
:::

**La diapositive 45** projette un graphique à deux courbes sur la période : le **prix de
l'action à la clôture en euros** (qui progresse d'environ 26 € à 40 €) et la **rentabilité
journalière à la clôture en %**, qui oscille autour de zéro entre environ −7 % et +7 %.

::: formule La rentabilité journalière
$$ r_t = \frac{P_t - P_{t-1}}{P_{t-1}} \times 100 $$
où $ P_t $ est le prix de clôture du jour et $ P_{t-1} $ celui de la veille.
:::

**Le tableau du support (diapositive 47)** — Prix et rentabilité de l'action, extrait :

| Date | Prix à la clôture (€) | Rentabilité à la clôture (%) |
|---|---:|---:|
| 22/08/12 | 35,02 | *incalculable* |
| 23/08/12 | 34,78 | −0,685 |
| 24/08/12 | 34,18 | −1,725 |
| 27/08/12 | 34,90 | 2,106 |
| 28/08/12 | 34,53 | −1,060 |
| … | … | … |
| 06/09/12 | 37,15 | 5,480 |
| … | … | … |
| 20/09/12 | 38,92 | −1,543 |

::: exemple Vérifions trois lignes — et comprenons la première
**Première ligne : « incalculable ».** Le 22/08 est la première date de la série : il n'y a
pas de veille, donc pas de $ P_{t-1} $. **Une série de $ n $ prix ne donne que $ n - 1 $
rentabilités.** C'est une remarque de méthode qui vaut aussi pour les taux de croissance du
chapitre 3.

**Vérifications :**
- 23/08 : $ (34{,}78 - 35{,}02)/35{,}02 = -0{,}006853 $ → **−0,685 %** ✔
- 24/08 : $ (34{,}18 - 34{,}78)/34{,}78 = -0{,}017251 $ → **−1,725 %** ✔
- 27/08 : $ (34{,}90 - 34{,}18)/34{,}18 = +0{,}021065 $ → **+2,106 %** ✔

**Notez que les dates sautent le week-end** : du 24/08 (vendredi) au 27/08 (lundi). La
« rentabilité journalière » est donc une rentabilité **par séance de bourse**, pas par jour
calendaire.
:::

**Le tableau de synthèse (diapositive 48)** — Rentabilité journalière moyenne (en %) et
volatilité (en %), année 2012 :

| | Du 23/05 au 21/06 | Du 22/06 au 23/07 | Du 24/07 au 22/08 | Du 23/08 au 21/09 | Du 23/05 au 21/09 |
|---|---:|---:|---:|---:|---:|
| **Jours** | 22 | 22 | 22 | 22 | **88** |
| **Rentabilité journalière moyenne** | 0,372 | −0,307 | 1,244 | 0,587 | 0,474 |
| **Volatilité (écart-type)** | 2,555 | 3,374 | 3,128 | 1,954 | 2,861 |

::: piege Les conclusions de la diapositive 48 ne se reconstruisent pas — signalé, non masqué
Le support tire du tableau trois conclusions, reproduites ici **mot pour mot** :

> « Il y a **99 % de chances de faire des gains en période 1, 2, 3, 5**.
> Si l'on veut être plus prudent et s'assurer des gains **999 fois sur 1000**, il ne fallait
> pas investir en **période 1, 2, 4, 5**.
> Bien entendu **rien ne garantit une rentabilité journalière positive à 100 %**. »

**Le calcul qui les produit n'est pas montré, et je ne parviens pas à le reconstruire à
partir de l'inégalité de la diapositive 44.** Voici la vérification, pour que vous puissiez
la refaire.

L'inégalité de Bienaymé-Tchebychev exige **$ k > 1 $**. Pour garantir un gain, il faudrait
que la borne basse $ m - k\sigma $ soit positive, donc que $ k < m/\sigma $. Or :

| Période | $ m $ | $ \sigma $ | $ k_{\max} = m/\sigma $ | Exploitable ? |
|---|---:|---:|---:|---|
| 1 (23/05-21/06) | 0,372 | 2,555 | **0,15** | Non : $ k \le 1 $ |
| 2 (22/06-23/07) | **−0,307** | 3,374 | — | Moyenne **négative** |
| 3 (24/07-22/08) | 1,244 | 3,128 | **0,40** | Non |
| 4 (23/08-21/09) | 0,587 | 1,954 | **0,30** | Non |
| 5 (23/05-21/09) | 0,474 | 2,861 | **0,17** | Non |

**Dans les cinq périodes, $ m/\sigma < 1 $** : l'inégalité ne fournit aucune garantie de gain,
à aucun seuil de confiance. Et la période 2, dont la rentabilité moyenne est **négative**,
figure pourtant dans la liste des périodes à « 99 % de chances de gains » — ce qui est
difficile à concilier avec n'importe quel calcul fondé sur la moyenne.

**Conduite à tenir — et c'est important :**
1. **Retenez ce qui est solide et enseigné** : la rentabilité journalière est un taux de
   variation ; l'écart-type des rentabilités est la **volatilité** ; le couple
   (rentabilité moyenne, volatilité) forme le **double indicateur** rendement / risque ; et
   Bienaymé-Tchebychev permet d'encadrer une distribution sans hypothèse de loi.
2. **Demandez à l'enseignante le détail du calcul des trois conclusions.** Il existe
   peut-être une étape faite « dans Excel » (le support l'indique : « on poursuit dans
   Excel… ») qui n'apparaît pas sur la diapositive — par exemple un raisonnement sur la
   rentabilité **cumulée** sur 22 séances plutôt que sur la rentabilité journalière.
3. **Ne reproduisez pas ces conclusions en examen sans le calcul qui les fonde.** Une copie
   qui affirme « 99 % de chances de gains » sans démonstration est indéfendable ; une copie
   qui écrit « la période 3 présente la meilleure rentabilité moyenne (1,244 %) mais aussi
   une volatilité élevée (3,128 %) ; la période 4 offre le meilleur rapport rendement/risque
   avec 0,587 % pour une volatilité de 1,954 % » est exacte et vérifiable.
:::

::: exemple Ce que le tableau permet de dire, rigoureusement
**Comparons les périodes par le rapport rentabilité / volatilité** — un rapport sans unité,
directement inspiré du coefficient de variation de la diapositive 53 :

| Période | $ m $ (%) | $ \sigma $ (%) | $ m/\sigma $ | Lecture |
|---|---:|---:|---:|---|
| 1 | 0,372 | 2,555 | 0,15 | Rendement faible, risque moyen |
| 2 | −0,307 | 3,374 | **< 0** | **Rendement négatif** et risque le plus élevé |
| 3 | 1,244 | 3,128 | **0,40** | **Meilleur rendement**, risque élevé |
| 4 | 0,587 | 1,954 | 0,30 | Rendement correct, **risque le plus faible** |
| 5 (ensemble) | 0,474 | 2,861 | 0,17 | La moyenne des quatre sous-périodes |

**Deux observations solides :**
1. **La période 2 est la seule à rentabilité négative**, et c'est aussi la plus volatile :
   elle est dominée par toutes les autres.
2. **La volatilité de l'ensemble (2,861) n'est pas la moyenne des volatilités des
   sous-périodes** — laquelle vaut $ (2{,}555 + 3{,}374 + 3{,}128 + 1{,}954)/4 = 2{,}753 $.
   **L'écart-type ne s'agrège pas linéairement**, et c'est précisément le problème que pose
   la diapositive 49.
:::

#### 2.2.14 Le problème de l'agrégation et la formule de Koenig (diapositives 49 et 50)

::: definition Le problème posé (diapositive 49)
- **La moyenne (arithmétique) peut se calculer par groupe** — c'est un opérateur linéaire.
- **L'écart-type n'est pas linéaire.**
- **On ne peut pas calculer facilement la volatilité annuelle.**
- **… mais il y a un moyen.**
:::

::: formule Les propriétés de la variance (diapositive 50)
**1. Formule de Koenig.** La variance se calcule aussi comme :
$$ V(X) = \frac{1}{N} \sum_{i=1}^{N} x_i^2 - m_X^2 $$
*(« la moyenne des carrés moins le carré de la moyenne »)*

**2. Invariance par translation.** Si j'ajoute le même nombre $ a $ à toutes les valeurs de
$ X $, **la variance est inchangée** : $ V(a + X) = V(X) $.

**3. Non-linéarité.** Si je multiplie tous les éléments par $ a $, **la variance est
multipliée par $ a^2 $** : $ V(aX) = a^2 V(X) $.

**4. Corollaire :** $ V(-X) = V(X) $.
:::

::: demo Pourquoi ces trois propriétés, et pourquoi elles règlent le problème
**Koenig — pourquoi elle est utile.** La formule de définition exige de connaître la moyenne
**avant** de pouvoir calculer chaque écart : deux passages sur les données. La formule de
Koenig ne demande que **deux sommes** — celle des $ x_i $ et celle des $ x_i^2 $ — calculables
en un seul passage. **C'est ce qui rend l'agrégation possible** (diapositive 57) : il suffit
de transmettre deux nombres par groupe.

*Vérification sur la série des âges :* moyenne des carrés $ = 2\,348{,}1 $ ; carré de la
moyenne $ = 47{,}9^2 = 2\,294{,}41 $ ; différence $ = \mathbf{54{,}19} $ — identique au calcul
par les écarts ✔

**Invariance par translation — la démonstration.** Si $ Y = X + a $, alors
$ m_Y = m_X + a $ (linéarité de la moyenne), donc
$ y_i - m_Y = (x_i + a) - (m_X + a) = x_i - m_X $ : **les écarts sont inchangés**, donc la
variance aussi. **Traduction concrète : ajouter 6 points à toutes les notes déplace la
distribution sans la déformer.**

**Non-linéarité — la démonstration.** Si $ Y = aX $, alors $ m_Y = a\,m_X $, donc
$ y_i - m_Y = a(x_i - m_X) $, et en élevant au carré : $ (y_i - m_Y)^2 = a^2 (x_i - m_X)^2 $.
D'où $ V(aX) = a^2 V(X) $. **Sur l'écart-type**, cela donne
$ \sigma_{aX} = |a| \, \sigma_X $ — l'écart-type, lui, est multiplié par $ |a| $, et c'est ce
qui le rend interprétable.

**Corollaire $ V(-X) = V(X) $ :** avec $ a = -1 $, $ a^2 = 1 $. Retourner une série ne change
pas sa dispersion — évident intuitivement, et démontré en une ligne.
:::

**Les illustrations du support (diapositives 51 et 52).** Deux graphiques superposent la
distribution de **115 notes** et sa transformée :
- **Diapositive 51 — 115 notes augmentées de 6 points.** La distribution initiale, de moyenne
  **7,25**, est translatée vers la droite ; la nouvelle moyenne est **13,25**
  ($ 7{,}25 + 6 $). **La forme est rigoureusement identique** : même hauteurs, mêmes écarts.
  **La variance est inchangée.**
- **Diapositive 52 — 115 notes multipliées par 2.** La moyenne passe de **7,25** à **14,50**
  ($ 7{,}25 \times 2 $), mais **la distribution s'étale** : les barres s'écartent les unes des
  autres. **La variance est multipliée par 4**, l'écart-type par 2.

::: examen Les deux graphiques disent tout — savoir les décrire vaut une démonstration
Placez côte à côte les deux illustrations : **l'une translate, l'autre dilate.**
- Ajouter une constante → la distribution **glisse** → moyenne décalée, **dispersion
  identique**.
- Multiplier par une constante → la distribution **s'étire** → moyenne multipliée,
  **dispersion multipliée par le carré** (variance) ou par la constante (écart-type).

**Application immédiate en notation :** ajouter 2 points à toute une classe ne réduit pas
les écarts entre élèves ; multiplier les notes par 1,2 les augmente. **Deux façons de
« remonter » une classe, deux effets opposés sur l'inégalité des notes.**
:::

#### 2.2.15 Le coefficient de variation (diapositive 53)

::: formule Le coefficient de variation
- Les mesures de la variance et de l'écart-type sont **sensibles à la conversion d'unités de
  mesure** (changement de monnaie, de métrique, etc.).
- Le coefficient de variation est **exprimé sans unité**, en pourcentage.
- Il permet des **comparaisons d'indicateurs de dispersion entre caractères mesurés
  différemment**.

$$ CV = \frac{\sigma_X}{m_X} $$
:::

::: demo Pourquoi il faut un indicateur sans unité — la démonstration par l'exemple
**Le problème.** Un écart-type de 500 est-il grand ? Impossible de répondre sans savoir de
quoi il s'agit.
- Sur des salaires mensuels de moyenne 2 000 € : $ CV = 500/2\,000 = 25\ \% $ — dispersion
  considérable.
- Sur des salaires annuels de moyenne 24 000 € : $ CV = 500/24\,000 = 2{,}1\ \% $ — dispersion
  faible.

**Le même nombre décrit deux réalités opposées.** La propriété 3 de la variance l'explique :
passer du mensuel à l'annuel multiplie les valeurs par 12, donc l'écart-type par 12. Le CV,
lui, est **invariant** par ce changement d'unité : $ CV_{aX} = |a|\sigma_X / (a\,m_X) = CV_X $.

**Les deux usages :**
1. Comparer la dispersion de **deux variables différentes** — des salaires et des âges, par
   exemple, ce qu'aucun écart-type ne permet.
2. Comparer la dispersion de **deux populations de niveaux très différents** — même logique
   que le ratio D9/D1 contre l'écart D9 − D1 (§2.2.3).
:::

::: marche
$ \sigma / m $ est exactement l'inverse d'un **ratio de Sharpe** simplifié — lequel rapporte
le rendement excédentaire à la volatilité, $ (m - r_f)/\sigma $. La logique est identique :
**un rendement ne se juge jamais seul, il se rapporte au risque pris pour l'obtenir.** Le
tableau du §2.2.13 en donne l'application : la période 3 a le meilleur rendement brut, la
période 4 le meilleur rapport rendement/risque. Ce sont deux réponses à deux questions
différentes.
:::

#### 2.2.16 La variance à partir d'une distribution (diapositives 54 à 56)

::: formule Les quatre écritures équivalentes
Lorsqu'on n'a pas les données brutes mais un **tableau de distribution** — $ p $ modalités,
effectifs $ n_i $, fréquences $ f_i $, l'indice $ i $ renvoyant au **numéro de modalité** :

**À partir des effectifs :**
$$ \sigma^2 = \frac{1}{N} \sum_{i=1}^{p} n_i (x_i - m)^2 = \frac{1}{N} \sum_{i=1}^{p} n_i x_i^2 - m^2 \qquad (11) $$

**À partir des fréquences :**
$$ \sigma^2 = \sum_{i=1}^{p} f_i (x_i - m)^2 = \sum_{i=1}^{p} f_i x_i^2 - m^2 \qquad (12) $$
:::

::: examen Quatre formules, une seule idée
Les quatre écritures ne sont **pas quatre formules à mémoriser** : ce sont deux choix
indépendants.
1. **Effectifs ou fréquences ?** $ \frac{1}{N}\sum n_i \ldots $ ou $ \sum f_i \ldots $ —
   simple passage de $ n_i $ à $ f_i = n_i/N $.
2. **Écarts ou Koenig ?** $ \sum (x_i - m)^2 $ ou $ \sum x_i^2 - m^2 $.

$ 2 \times 2 = 4 $ écritures, **une seule variance**. En pratique : Koenig avec les
fréquences est le plus rapide à la main, les écarts sont plus sûrs quand la moyenne tombe
juste.
:::

::: piege Le résultat du cas n° 4 (diapositive 55) est erroné — vérification complète
Le support donne, pour les quatre cas de l'introduction :
> Cas 1 : $ \sigma^2 = 0 $ et $ \sigma = 0 $ — Cas 2 : $ \sigma^2 = 11 $ et
> $ \sigma = 3{,}3 $ — Cas 3 : $ \sigma^2 = 28{,}8 $ et $ \sigma = 5{,}4 $ — Cas 4 :
> $ \sigma^2 = 10{,}4 $ et $ \sigma = 3{,}2 $.

**J'ai refait les quatre calculs. Les trois premiers sont exacts ; le quatrième ne l'est pas.**

**Cas 2** (5 élèves à chacune des notes 7, 8, 9, 10, 11, 13, 14, 15, 16, 17) :
$ \sigma^2 = \frac{5}{50}[25+16+9+4+1+1+4+9+16+25] = \frac{5 \times 110}{50} = \mathbf{11} $ ✔
$ \sigma = 3{,}32 $ ✔

**Cas 3** (20 à 6, 20 à 18, 10 à 12) :
$ \sigma^2 = \frac{20(36) + 20(36) + 10(0)}{50} = \frac{1\,440}{50} = \mathbf{28{,}8} $ ✔
$ \sigma = 5{,}37 $ ✔

**Cas 4** (5 à 4, 10 à 8, 10 à 10, 10 à 14, 10 à 16, 5 à 20) :
$$ \sigma^2 = \frac{5(4-12)^2 + 10(8-12)^2 + 10(10-12)^2 + 10(14-12)^2 + 10(16-12)^2 + 5(20-12)^2}{50} $$
$$ = \frac{5(64) + 10(16) + 10(4) + 10(4) + 10(16) + 5(64)}{50} = \frac{320+160+40+40+160+320}{50} = \frac{1\,040}{50} = \mathbf{20{,}8} $$
d'où $ \sigma = \sqrt{20{,}8} = \mathbf{4{,}56} $.

**La valeur du support (10,4) est exactement la moitié de 20,8** — l'écart évoque une division
par 100 au lieu de 50, ou une somme partielle.

**Ce que l'erreur change — et c'est pourquoi il faut le savoir.** Le classement des
dispersions n'est pas le même :

| | Variance du support | Variance recalculée |
|---|---:|---:|
| Cas 1 | 0 | 0 |
| Cas 2 | 11 | 11 |
| Cas 3 | 28,8 | 28,8 |
| Cas 4 | *10,4* | **20,8** |
| **Classement** | 3 > 2 > 4 > 1 | **3 > 4 > 2 > 1** |

La réponse à la question d'introduction — « dans quel cas la distribution est-elle la plus
dispersée ? » — reste **le cas 3** dans les deux versions. Mais la place relative des cas 2 et
4 s'inverse. **Et le classement corrigé est cohérent avec l'étendue** (cas 4 : 16 contre cas
2 : 10), ce qui n'était pas le cas de la version du support.

**Conduite à tenir :** refaites le calcul, il prend deux minutes ; signalez-le à
l'enseignante. Si la question tombe en examen, présentez le calcul détaillé — un résultat
justifié ligne à ligne ne peut pas être compté faux.
:::

::: methode Choisir la bonne formule (diapositive 56)
> Pour déterminer quel type de calcul adopter, il faut identifier **les éléments statistiques
> et le mode de représentation des données** choisies :
> - **données brutes** (*raw data*) : toutes les observations individuelles sont disponibles ;
> - **données sous forme de distribution** : toutes les modalités sont disponibles ainsi que
>   les effectifs et les fréquences ;
> - **données présentées sous forme agrégée par sous-groupes** : certains indicateurs peuvent
>   être agrégés si l'on dispose de suffisamment d'informations.

**L'arbre de décision, à appliquer avant tout calcul :**

| Ce dont je dispose | Formule de la moyenne | Formule de la variance |
|---|---|---|
| Les $ N $ observations | $ \frac{1}{N}\sum_{i=1}^{N} x_i $ (3) | $ \frac{1}{N}\sum (x_i - m)^2 $ |
| Modalités + effectifs | $ \frac{1}{N}\sum_{i=1}^{p} n_i x_i $ (4) | $ \frac{1}{N}\sum n_i x_i^2 - m^2 $ (11) |
| Modalités + fréquences | $ \sum f_i x_i $ (5) | $ \sum f_i x_i^2 - m^2 $ (12) |
| Moyennes et variances par groupe | $ \sum \frac{n_k}{N} m_k $ (6) | Agrégation par Koenig (§2.2.17) |

**C'est la question à se poser en premier devant un exercice** : de quelle forme sont mes
données ? Se tromper de formule est l'erreur la plus fréquente en devoir.
:::

#### 2.2.17 La variance par agrégation (diapositive 57)

::: formule La variance agrégée par la formule de Koenig
Soient $ K $ sous-groupes d'effectifs $ N_k $, de moyennes $ m_{X_k} $ et de variances
$ \sigma_k^2 $, avec $ \sum_{k=1}^{K} N_k = N $ :

- **Moyenne agrégée** : $ m_X = \frac{1}{N} \sum_{k=1}^{K} N_k\, m_{X_k} $
- **Pour chaque groupe**, la formule de Koenig donne :
  $ \sum_{i=1}^{N_k} x_i^2 = [\sigma_k^2 + m_{X_k}^2]\, N_k $
- **Au niveau agrégé** : $ \sum_{i=1}^{N} x_i^2 = \sum_{k=1}^{K} \sum_{i=1}^{N_k} x_i^2 $
- **D'où la variance agrégée** :
$$ \sigma^2 = \frac{1}{N} \sum_{k=1}^{K} \left[\sigma_k^2 + m_{X_k}^2\right] N_k - m_X^2 $$
:::

::: demo La chaîne du raisonnement, maillon par maillon
Le support enchaîne quatre lignes sans les commenter. Voici pourquoi chacune est nécessaire.

1. **Le problème.** La variance globale demande $ \sum x_i^2 $ sur toute la population — or on
   ne dispose que d'indicateurs par groupe, pas des observations.
2. **Koenig retourné.** Pour un groupe $ k $, $ \sigma_k^2 = \frac{1}{N_k}\sum x_i^2 - m_k^2 $.
   En isolant la somme des carrés : $ \sum_{i \in k} x_i^2 = (\sigma_k^2 + m_k^2) N_k $.
   **C'est le maillon décisif : la somme des carrés d'un groupe se reconstitue à partir de sa
   moyenne, de sa variance et de son effectif — trois nombres.**
3. **On additionne les groupes.** La somme des carrés sur toute la population est la somme des
   sommes de carrés des groupes, ces derniers étant **disjoints**.
4. **On applique Koenig à l'ensemble.** $ \sigma^2 = \frac{1}{N}\sum x_i^2 - m_X^2 $, où la
   somme a été reconstituée à l'étape 3.

**C'était l'annonce de la diapositive 49** : « on ne peut pas calculer facilement la
volatilité annuelle… mais il y a un moyen ». **Le moyen, c'est Koenig.** Il faut connaître,
pour chaque période, **trois nombres seulement** : l'effectif, la moyenne, la variance.
:::

#### 2.2.18 Corollaire : la décomposition de la variance (diapositive 58)

::: formule Variance intra, variance inter, variance totale
> La connaissance des variances par groupe et de la variance globale permet de mesurer
> l'importance des variations dites **intra** et **inter** groupes dans la variation totale.

**Variance intra-groupe** — la dispersion **à l'intérieur** des groupes :
$$ V_{\text{intra}} = \sum_{k=1}^{K} \frac{N_k}{N}\, \sigma_k^2 $$

**Variance inter-groupe** — la dispersion **des moyennes entre** groupes :
$$ V_{\text{inter}} = \sum_{k=1}^{K} \frac{N_k}{N} (m_{X_k} - m_X)^2 = \sum_{k=1}^{K} \frac{N_k}{N} m_{X_k}^2 - m_X^2 $$

**Et la relation fondamentale :**
$$ \boxed{\ \sigma^2 = V_{\text{intra}} + V_{\text{inter}}\ } $$
:::

::: demo Ce que la décomposition signifie — et pourquoi c'est l'outil le plus puissant du chapitre
**L'idée.** Deux personnes peuvent différer pour deux raisons : parce qu'elles
n'appartiennent pas au même groupe (un cadre et un ouvrier), ou parce qu'à l'intérieur de
leur groupe elles ne sont pas identiques (deux cadres). **La variance totale additionne
exactement ces deux sources.**

| Composante | Ce qu'elle mesure | Question à laquelle elle répond |
|---|---|---|
| $ V_{\text{intra}} $ | La dispersion **moyenne** à l'intérieur des groupes | « Les membres d'un même groupe se ressemblent-ils ? » |
| $ V_{\text{inter}} $ | La dispersion **des moyennes** de groupe autour de la moyenne générale | « Les groupes diffèrent-ils entre eux ? » |

**Deux cas extrêmes, à savoir décrire :**
- $ V_{\text{inter}} \approx 0 $ : les groupes ont la même moyenne — **le découpage
  n'explique rien**, toute la dispersion est interne.
- $ V_{\text{intra}} \approx 0 $ : chaque groupe est homogène — **le découpage explique
  tout**, connaître le groupe d'un individu suffit à prédire sa valeur.

**Le rapport $ V_{\text{inter}} / \sigma^2 $ mesure donc le pouvoir explicatif du découpage.**
C'est ce rapport qui deviendra, au chapitre 4 et en économétrie, le **rapport de
corrélation** puis le **R²**.

**Application immédiate au tableau de la diapositive 38 :** l'écart inter-décile de
l'ensemble (2 720 €) dépasse celui de trois CSP sur quatre précisément parce qu'il
**contient la composante inter** — l'écart entre un cadre médian à 3 620 € et un employé
médian à 1 730 €. On mesurait déjà la décomposition, sans la nommer.
:::

::: marche
En gestion de portefeuille, c'est la décomposition du risque : la variance d'un ensemble de
positions se sépare en risque **spécifique** (intra — ce qui bouge à l'intérieur de chaque
secteur) et risque **systématique** (inter — ce qui fait bouger les secteurs les uns par
rapport aux autres). La diversification agit sur le premier, jamais sur le second. C'est la
même algèbre, appliquée à un autre objet.
:::

<!--saut-->
### 2.3 — Résumer la concentration des données

::: objectif Ce que cette troisième famille ajoute
La position dit **où** se situe la distribution. La dispersion dit **à quel point elle
s'étale**. La concentration répond à une troisième question, qui n'est ni l'une ni l'autre :
**comment le total se partage-t-il entre les individus ?**

Trois notions à maîtriser à la fin de cette section : la **part de l'agrégat**, la **courbe
de Lorenz**, l'**indice de Gini**. Et une chose que le support ne dit jamais : **ces
indicateurs ne s'appliquent pas à toutes les variables quantitatives.**
:::

#### 2.3.1 Concentration et dispersion : deux questions différentes (diapositive 59)

Le support pose la question sous forme de « points communs et différences ». Reprenons-la
proprement, parce que la confusion entre les deux familles est l'une des plus fréquentes en
examen.

::: definition Dispersion et concentration
**La dispersion** s'intéresse à la **répartition des observations** d'une variable : les
valeurs sont-elles serrées autour de la moyenne, ou éparpillées ? Elle raisonne sur les
$ x_i $ eux-mêmes.

**La concentration** s'intéresse à la **répartition de la somme** de la variable : sur
combien d'individus le total est-il concentré ? Elle raisonne sur les parts
$ x_i / \sum_j x_j $.

**Le point commun :** les deux familles servent à **mesurer des inégalités** d'un caractère
statistique quantitatif. Ce sont deux angles d'attaque du même phénomène.
:::

::: piege La condition d'existence que le support signale en une ligne et qu'il faut prendre au sérieux
> « Si la somme des revenus fait sens, ce n'est pas le cas de tous les caractères
> statistiques quantitatifs (exemple : la taille) ! »

**Cette phrase est une condition d'application, pas une remarque anecdotique.**

La concentration se calcule à partir de **l'agrégat**, c'est-à-dire la somme
$ \sum_{i=1}^{N} x_i $. Pour que les indicateurs de concentration aient un sens, il faut que
cette somme désigne **un objet réel**.

| Variable | Somme sur la population | Cette somme a-t-elle un sens ? | Concentration calculable ? |
|---|---|---|---|
| Salaire | La **masse salariale** | Oui : c'est un montant que l'on verse réellement | **Oui** |
| Patrimoine | Le **patrimoine total** du pays | Oui : c'est un stock de richesse existant | **Oui** |
| Chiffre d'affaires | Le CA total du secteur | Oui : c'est la taille du marché | **Oui** |
| Émissions de CO₂ | Les émissions totales | Oui : c'est ce qui arrive dans l'atmosphère | **Oui** |
| Taille (cm) | La somme des tailles | **Non** : additionner des tailles ne produit rien | **Non** |
| Note sur 20 | La somme des notes | **Non** : aucun objet ne correspond à ce total | **Non** |
| Température | La somme des températures | **Non** | **Non** |
| Âge | La somme des âges | **Non** (aucun objet réel) | **Non** |

**La règle en une phrase :** la concentration exige une variable **extensive et additive** —
une variable dont le total est lui-même une grandeur économique. La dispersion, elle,
s'applique à **toute** variable quantitative.

**Erreur d'examen classique :** calculer un Gini sur des notes ou sur des âges. Le calcul
« marche » numériquement — rien dans l'algèbre ne l'empêche — mais **le résultat ne
s'interprète pas**. Un correcteur exigeant sanctionne l'absence de vérification préalable.
:::

::: synthese Le tableau de départage
| | Dispersion | Concentration |
|---|---|---|
| **Objet du raisonnement** | Les valeurs $ x_i $ | Les parts $ x_i / \sum x_j $ |
| **Question posée** | Les individus se ressemblent-ils ? | Le total est-il concentré sur quelques-uns ? |
| **Référence** | La moyenne $ m_X $ | L'agrégat $ \sum x_i $ |
| **Indicateurs** | Étendue, écarts inter-quantiles, EAM, variance, écart-type, CV | Part de l'agrégat, courbe de Lorenz, indice de Gini |
| **Unité du résultat** | Celle de $ X $ (sauf CV, sans unité) | Sans unité (des parts, des %) |
| **Condition d'application** | Variable quantitative | Variable quantitative **dont la somme fait sens** |
| **Phrase-type d'interprétation** | « L'écart-type vaut 7,4 ans » | « Les 20 % les moins payés perçoivent 3,9 % de la masse salariale » |
:::

<!--saut-->

#### 2.3.2 La part de l'agrégat (diapositive 60)

::: definition L'agrégat et sa part
**L'agrégat** d'un caractère $ X $ est la **somme de $ X $ sur toute la population** :
$ \sum_{i=1}^{N} x_i $. Dans le cas des salaires, cet agrégat porte un nom que tu connais
déjà : la **masse salariale**.

**La part de l'agrégat de la classe $ k $** est la fraction de ce total détenue par les
individus de la classe $ k $ :

$$ p_k = \frac{\text{somme de } X \text{ sur la classe } k}{\text{somme de } X \text{ sur toute la population}} $$
:::

Le support énonce ensuite une relation qu'il présente comme « utile à savoir ». Elle n'est
pas seulement utile : **c'est elle qui rend tout le calcul possible.** Elle mérite donc une
démonstration.

::: formule La somme = la moyenne × l'effectif
$$ \sum_{i=1}^{N_k} x_i = N_k \, m_{X_k} $$

où $ N_k $ est l'effectif de la classe $ k $ et $ m_{X_k} $ la moyenne de $ X $ dans
cette classe.

**En mots :** la somme d'une variable sur un groupe est égale à la moyenne du groupe
multipliée par la taille du groupe. Dans le cas des salaires :

$$ \text{masse salariale de la classe} = \text{salaire moyen de la classe} \times \text{effectif de la classe} $$
:::

::: demo La démonstration, en une ligne
Par définition, la moyenne de la classe $ k $ est :

$$ m_{X_k} = \frac{1}{N_k} \sum_{i=1}^{N_k} x_i $$

Il suffit de multiplier les deux membres par $ N_k $ :

$$ N_k \, m_{X_k} = \sum_{i=1}^{N_k} x_i $$

C'est tout. **La relation n'est rien d'autre que la définition de la moyenne lue à
l'envers** — et c'est précisément pour cela qu'elle est si puissante : elle transforme une
information *moyenne* (que l'on publie toujours) en une information *totale* (que l'on
publie rarement).
:::

Reste la difficulté annoncée par le support : dans le tableau qui suit, **les effectifs ne
sont pas connus**. On ne connaît que des **proportions** (20 % par classe) et des
**moyennes**. Le support affirme que le calcul reste possible et suggère de « poser
l'effectif total à 1 ». Voici pourquoi cette astuce est légitime.

::: demo Pourquoi l'effectif total disparaît du calcul
Écrivons la part de la classe $ k $ avec la relation qu'on vient de démontrer :

$$ p_k = \frac{N_k \, m_{X_k}}{\sum_{j=1}^{K} N_j \, m_{X_j}} $$

Or l'effectif d'une classe s'écrit $ N_k = f_k N $, où $ f_k $ est la **fréquence** de la
classe et $ N $ l'effectif total. En remplaçant :

$$ p_k = \frac{f_k N \, m_{X_k}}{\sum_{j=1}^{K} f_j N \, m_{X_j}} = \frac{N \cdot f_k \, m_{X_k}}{N \cdot \sum_{j=1}^{K} f_j \, m_{X_j}} $$

Le facteur $ N $ est **commun au numérateur et au dénominateur** : il se simplifie.

$$ \boxed{\; p_k = \frac{f_k \, m_{X_k}}{\sum_{j=1}^{K} f_j \, m_{X_j}} = \frac{f_k \, m_{X_k}}{m_X} \;} $$

**Deux conséquences à retenir.**

1. **La part de l'agrégat ne dépend que des fréquences et des moyennes de classe.** L'effectif
   total est inutile — d'où l'astuce « poser $ N = 1 $ », qui n'est pas une approximation
   mais une simplification exacte.
2. Le dénominateur $ \sum_j f_j m_{X_j} $ **est la moyenne générale** $ m_X $ — c'est la
   formule de la moyenne par agrégation, vue en 2.1.7.

On retrouve donc :

$$ p_k = f_k \times \frac{m_{X_k}}{m_X} $$

**La part d'une classe est sa fréquence multipliée par son avantage relatif de moyenne.** Une
classe qui rassemble 20 % des salariés et dont le salaire moyen vaut 2 fois la moyenne
générale détient $ 0{,}20 \times 2 = 40 \% $ de la masse salariale.
:::

::: methode Calculer une part de l'agrégat — les quatre étapes
1. **Vérifier que la somme de $ X $ a un sens.** Sinon, s'arrêter là.
2. **Partir du tableau des fréquences** de $ X $, avec la moyenne de chaque classe. Si les
   classes sont données par leurs bornes et que la moyenne n'est pas fournie, prendre le
   **centre de classe** (et le dire).
3. **Calculer $ f_k \times m_{X_k} $ pour chaque classe**, puis leur somme — qui est la
   moyenne générale $ m_X $.
4. **Diviser chaque produit par cette somme**, et exprimer en pourcentage. **Contrôle
   obligatoire : la somme des parts doit faire 100 %** (aux arrondis près).
:::

<!--saut-->

#### 2.3.3 Illustration : les salaires en France en 2005 (diapositive 61)

Le support donne le tableau suivant. Je le reproduis intégralement, puis je reconstruis
chaque colonne — y compris celles que le support affiche sans dire d'où elles viennent.

**Classes de salaires dans les entreprises en France en 2005**

| (1) Proportion de salariés en % | (2) Borne inférieure du salaire | (3) Borne supérieure du salaire | (4) Estimation du salaire moyen de la classe | (5) Part de la masse salariale en % |
|---|---|---|---|---|
| 20 | 11 000 | 12 894 | 11 947 | 11,2 |
| 20 | 12 894 | 15 555 | 14 225 | 13,3 |
| 20 | 15 555 | 19 098 | 17 327 | 16,2 |
| 20 | 19 098 | 25 818 | 22 458 | 21,1 |
| 20 | 25 818 | 55 600 | 40 709 | 38,2 |
| **Ensemble** | | | **21 333** | **100** |

::: piege Colonne (4) : d'où sortent ces « estimations » ? Le support ne le dit jamais
Le support intitule la colonne « estimation du salaire moyen de la classe » sans indiquer la
méthode. **Vérifions-la par le calcul :**

| Classe | Bornes | Centre de classe $ \frac{\text{borne inf} + \text{borne sup}}{2} $ | Valeur du support |
|---|---|---|---|
| 1 | 11 000 – 12 894 | $ (11\,000 + 12\,894)/2 = 11\,947{,}0 $ | 11 947 ✔ |
| 2 | 12 894 – 15 555 | $ (12\,894 + 15\,555)/2 = 14\,224{,}5 $ | 14 225 ✔ |
| 3 | 15 555 – 19 098 | $ (15\,555 + 19\,098)/2 = 17\,326{,}5 $ | 17 327 ✔ |
| 4 | 19 098 – 25 818 | $ (19\,098 + 25\,818)/2 = 22\,458{,}0 $ | 22 458 ✔ |
| 5 | 25 818 – 55 600 | $ (25\,818 + 55\,600)/2 = 40\,709{,}0 $ | 40 709 ✔ |

**Conclusion : la colonne (4) est le centre de chaque classe.** Le support applique donc
**l'hypothèse de répartition uniforme à l'intérieur des classes** — exactement l'hypothèse
déjà utilisée pour la médiane (§ 2.1.16) et pour la moyenne à partir d'une distribution
(§ 2.1.6). **Il fallait le dire, et tu dois le dire dans une copie.**

**Et il faut en mesurer la fragilité.** Les quatre premières classes sont étroites
(1 894 €, 2 661 €, 3 543 €, 6 720 €) : l'hypothèse y est bénigne. La cinquième est large de
**29 782 €**, soit 16 fois la première. Or, à l'intérieur de la tranche haute des salaires,
les effectifs ne sont pas répartis uniformément : ils sont **massés près de la borne
inférieure** et se raréfient vers le haut (distribution étalée à droite, § 2.1.11). La
vraie moyenne de cette classe est donc **vraisemblablement inférieure à 40 709 €**, et par
conséquent **la part de 38,2 % surestime probablement la concentration réelle**. Je dis
« vraisemblablement » et non « certainement » : sans les données individuelles, je ne peux
pas quantifier l'écart. **Signaler cette limite est exactement ce qui distingue une copie
excellente d'une copie moyenne.**
:::

::: correction Reconstruction complète de la colonne (5)
**Étape 1 — L'agrégat.** Les classes ont toutes la même fréquence $ f_k = 0{,}20 $. La
moyenne générale vaut donc :

$$ m_X = \sum_{k=1}^{5} f_k \, m_{X_k} = 0{,}20 \times (11\,947 + 14\,225 + 17\,327 + 22\,458 + 40\,709) $$

Somme des cinq moyennes : $ 11\,947 + 14\,225 = 26\,172 $ ; $ + 17\,327 = 43\,499 $ ;
$ + 22\,458 = 65\,957 $ ; $ + 40\,709 = \mathbf{106\,666} $.

$$ m_X = 0{,}20 \times 106\,666 = \mathbf{21\,333{,}2 \; \text{€}} $$

**Le support annonce 21 333 € ✔.**

::: piege
**Pourquoi ici la moyenne générale est la moyenne *simple* des cinq moyennes de classe.**
Uniquement parce que les cinq classes ont **le même poids** (20 % chacune). C'est le cas ici
parce que les classes sont des **quintiles**, construits pour contenir chacun un cinquième
de la population. **Si les fréquences étaient inégales, il faudrait impérativement pondérer**
— c'est précisément le piège de l'agrégation vu en § 2.1.7.
:::

**Étape 2 — Les parts.** Comme tous les $ f_k $ valent 0,20, ils se simplifient eux aussi :

$$ p_k = \frac{0{,}20 \times m_{X_k}}{0{,}20 \times 106\,666} = \frac{m_{X_k}}{106\,666} $$

| Classe | $ m_{X_k} $ | $ p_k = m_{X_k} / 106\,666 $ | En % | Support |
|---|---|---|---|---|
| 1 | 11 947 | 0,112003 | **11,20 %** | 11,2 ✔ |
| 2 | 14 225 | 0,133360 | **13,34 %** | 13,3 ✔ |
| 3 | 17 327 | 0,162441 | **16,24 %** | 16,2 ✔ |
| 4 | 22 458 | 0,210545 | **21,05 %** | 21,1 ✔ |
| 5 | 40 709 | 0,381650 | **38,17 %** | 38,2 ✔ |
| **Total** | 106 666 | **1,000000** | **100,00 %** | 100 ✔ |

**Le contrôle de somme est vérifié : les cinq parts totalisent exactement 100 %.**

**Étape 3 — L'interprétation, phrase par phrase.**
- Les **20 % les moins payés** perçoivent **11,2 %** de la masse salariale : un peu plus de la
  moitié de ce qu'ils toucheraient dans une répartition parfaitement égalitaire (20 %).
- Les **20 % les mieux payés** en perçoivent **38,2 %**, soit **près du double** de la part
  égalitaire, et **3,4 fois** la part des 20 % du bas.
- La classe médiane (la 3ᵉ) détient 16,2 %, encore en dessous de 20 % : **la médiane est
  sous la moyenne**, signature d'une distribution étalée à droite — cohérent avec tout ce
  qu'on a établi sur les salaires au § 2.2.7.
:::

<!--saut-->

#### 2.3.4 Illustration : les mêmes salaires en 2021 (diapositive 62)

**Classes de salaires dans les entreprises en France en 2021**

| (1) Proportion de salariés en % | (2) Borne inférieure du salaire | (3) Borne supérieure du salaire | (4) Estimation du salaire moyen de la classe | (5) Part de la masse salariale en % |
|---|---|---|---|---|
| 20 | 1 333 | 6 709 | 4 021 | 3,9 |
| 20 | 6 709 | 15 110 | 10 910 | 10,6 |
| 20 | 15 110 | 22 942 | 19 026 | 18,4 |
| 20 | 22 942 | 32 124 | 27 533 | 26,7 |
| 20 | 32 124 | 51 490 | 41 807 | 40,5 |
| **Ensemble** | | | **20 659** | **100** |

::: correction Reconstruction complète — même méthode, mêmes contrôles
**Vérification de la colonne (4) — centres de classe :**
$ (1\,333+6\,709)/2 = 4\,021{,}0 $ ✔ · $ (6\,709+15\,110)/2 = 10\,909{,}5 $ ✔ ·
$ (15\,110+22\,942)/2 = 19\,026{,}0 $ ✔ · $ (22\,942+32\,124)/2 = 27\,533{,}0 $ ✔ ·
$ (32\,124+51\,490)/2 = 41\,807{,}0 $ ✔ — **même hypothèse de répartition uniforme.**

**L'agrégat :** $ 4\,021 + 10\,910 = 14\,931 $ ; $ + 19\,026 = 33\,957 $ ;
$ + 27\,533 = 61\,490 $ ; $ + 41\,807 = \mathbf{103\,297} $.

$$ m_X = 0{,}20 \times 103\,297 = \mathbf{20\,659{,}4 \; \text{€}} $$

**Le support annonce 20 659 € ✔.**

**Les parts :** $ p_k = m_{X_k} / 103\,297 $.

| Classe | $ m_{X_k} $ | $ p_k $ | En % | Support |
|---|---|---|---|---|
| 1 | 4 021 | 0,038926 | **3,89 %** | 3,9 ✔ |
| 2 | 10 910 | 0,105617 | **10,56 %** | 10,6 ✔ |
| 3 | 19 026 | 0,184187 | **18,42 %** | 18,4 ✔ |
| 4 | 27 533 | 0,266542 | **26,65 %** | 26,7 ✔ |
| 5 | 41 807 | 0,404726 | **40,47 %** | 40,5 ✔ |
| **Total** | 103 297 | **1,000000** | **100,00 %** | 100 ✔ |
:::

::: piege Un détail d'arrondi que le support ne signale pas — et qui va se propager
Additionne les cinq pourcentages **arrondis** du support :

$$ 3{,}9 + 10{,}6 + 18{,}4 + 26{,}7 + 40{,}5 = \mathbf{100{,}1} $$

**Pas 100,0.** Le tableau affiche pourtant « Ensemble : 100 ». Il n'y a **aucune erreur de
fond** : les parts exactes totalisent bien 1, mais chacune a été arrondie **vers le haut**
au dixième (3,893 → 3,9 ; 10,562 → 10,6 ; 18,419 → 18,4 ; 26,654 → 26,7 ; 40,473 → 40,5), et
cinq arrondis vers le haut produisent un excédent de 0,1.

**Pourquoi je te le signale :** parce que cet excédent **se propage au tableau des cumuls**
de la diapositive 65 (voir § 2.3.6) et modifie le Gini à la troisième décimale. En examen,
**écris toujours si tu cumules des valeurs arrondies ou des valeurs exactes** — la différence
est petite mais un correcteur exigeant la voit.
:::

<!--saut-->

#### 2.3.5 Comparaison 2005 / 2021 : les inégalités ont-elles augmenté ? (diapositive 63)

Le support pose la question et affiche le tableau. **Il ne donne pas la réponse.** La voici,
construite.

**Comparaison des agrégats de salaire entre 2005 et 2021**

| Proportion de salariés en % | Part de la masse salariale en % en 2005 | Part de la masse salariale en % en 2021 | Variation en points |
|---|---|---|---|
| 20 (les moins payés) | 11,2 | 3,9 | **− 7,3** |
| 20 | 13,3 | 10,6 | **− 2,7** |
| 20 (médians) | 16,2 | 18,4 | **+ 2,2** |
| 20 | 21,1 | 26,7 | **+ 5,6** |
| 20 (les mieux payés) | 38,2 | 40,5 | **+ 2,3** |
| **Ensemble** | **100,0** | **100,0** | **0,0** |

::: correction La réponse complète à la question de la diapositive
**1. Le sens de l'évolution est sans ambiguïté : les inégalités ont augmenté.**

Les deux quintiles du bas **perdent** (− 7,3 et − 2,7 points), les trois quintiles du haut
**gagnent** (+ 2,2, + 5,6 et + 2,3 points). Le transfert net des deux premiers vers les trois
derniers est de **10,0 points de masse salariale** — un dixième de toute la masse salariale
a changé de mains entre quintiles.

::: piege
**La somme des variations doit être nulle**, et elle l'est :
$ -7{,}3 - 2{,}7 + 2{,}2 + 5{,}6 + 2{,}3 = 0{,}1 $ … à 0,1 près, résidu de l'excédent
d'arrondi identifié en § 2.3.4. **C'est un contrôle mécanique : les parts totalisant 100 %
les deux années, ce qu'un quintile gagne, un autre le perd nécessairement.** Si tes
variations ne totalisent pas 0, tu as une erreur de calcul.
:::

**2. L'ampleur : la lecture en variation relative est bien plus parlante.**

| Quintile | 2005 | 2021 | Variation relative |
|---|---|---|---|
| 1ᵉʳ | 11,2 | 3,9 | $ 3{,}9/11{,}2 - 1 = -65{,}2\,\% $ — **la part est divisée par 2,9** |
| 2ᵉ | 13,3 | 10,6 | $ -20{,}3\,\% $ |
| 3ᵉ | 16,2 | 18,4 | $ +13{,}6\,\% $ |
| 4ᵉ | 21,1 | 26,7 | $ +26{,}5\,\% $ |
| 5ᵉ | 38,2 | 40,5 | $ +6{,}0\,\% $ |

**Le fait marquant n'est pas l'envol du haut — le dernier quintile ne gagne que 6 % — mais
l'effondrement du bas : la part du premier quintile est divisée par près de trois.**

**3. Le rapport entre extrêmes.**
- 2005 : $ 38{,}2 / 11{,}2 = \mathbf{3{,}41} $ — le quintile du haut perçoit 3,4 fois la
  masse du quintile du bas.
- 2021 : $ 40{,}5 / 3{,}9 = \mathbf{10{,}38} $ — il en perçoit **plus de 10 fois** autant.

**Le rapport a été multiplié par 3.** C'est le chiffre à retenir.
:::

::: piege La prudence méthodologique obligatoire — et une limite que je ne peux pas lever
Avant de conclure « les inégalités salariales ont explosé en France entre 2005 et 2021 »,
**regarde les bornes des deux tableaux :**

| | 2005 | 2021 |
|---|---|---|
| Borne inférieure de la 1ʳᵉ classe | 11 000 € | **1 333 €** |
| Borne supérieure de la dernière | 55 600 € | **51 490 €** |
| Salaire moyen d'ensemble | 21 333 € | **20 659 €** |

**Trois anomalies apparentes :**
1. Le plancher passe de 11 000 € à 1 333 € — **il est divisé par 8** en seize ans.
2. Le plafond **baisse** (55 600 → 51 490).
3. Le salaire moyen **baisse en euros courants** (21 333 → 20 659), alors qu'entre 2005 et
   2021 les salaires nominaux en France ont nettement augmenté.

**Ces trois faits ne sont pas compatibles avec deux mesures du même champ.** L'explication
la plus probable est un **changement de champ statistique** : le tableau 2005 semble porter
sur des salaires en équivalent temps plein (ou sur les seuls postes à temps complet en année
pleine), le tableau 2021 sur l'ensemble des postes — y compris temps partiels et années
incomplètes, qui produisent mécaniquement de très petits salaires annuels.

**Je dois être explicite : je ne peux pas le vérifier.** Le support n'indique ni la source,
ni le champ, ni la définition exacte du salaire (net ou brut, annuel, en EQTP ou tous
postes). **Je ne dispose que des deux tableaux.**

**Ce qu'il faut donc écrire en examen :** « Les données montrent une forte hausse de la
concentration de la masse salariale entre 2005 et 2021. Cette hausse doit toutefois être
interprétée avec prudence : la baisse simultanée du plancher, du plafond et du salaire moyen
en euros courants suggère un changement de champ entre les deux millésimes. Une partie de
l'écart mesuré pourrait donc être un artefact de mesure et non une évolution réelle. »

**Cette phrase-là vaut des points.** Elle prouve que tu ne calcules pas en aveugle. Le
raisonnement est le même qu'en finance : avant de comparer deux performances, on vérifie que
les deux séries couvrent le même périmètre, la même devise et le même traitement des
dividendes. **Une comparaison de chiffres non homogènes ne vaut rien, même parfaitement
calculée.**
:::

<!--saut-->

#### 2.3.6 La courbe de Lorenz (diapositives 64 à 66)

::: definition La courbe de Lorenz
La **courbe de Lorenz** représente la **part cumulée de la variable $ X $** en fonction de la
**fréquence cumulée de la population**, les individus étant classés **par valeur croissante
de $ X $**.

- **En abscisse :** la fréquence cumulée de la population, notée $ F $ — de 0 % à 100 %.
- **En ordonnée :** la part cumulée de l'agrégat de $ X $, notée $ L(F) $ — de 0 % à 100 %.

Dans le cas des salaires, la courbe met en correspondance la **part cumulée de la masse
salariale** et la **part cumulée de la population salariée**. Elle se lit directement en une
phrase :

> « Les **…** % des salariés les moins payés perçoivent **…** % de la masse salariale. »
:::

::: piege Le classement par ordre croissant est une condition, pas un détail
Le support écrit la définition sans préciser que les individus doivent être **rangés par
valeur croissante de $ X $**. Sans cette condition, la courbe n'a aucune propriété : elle
n'est ni convexe, ni située sous la diagonale, et le Gini calculé dessus n'a plus de sens.

**C'est le classement croissant qui fait toute la construction.** Dans les tableaux des
diapositives 61 et 62, il est déjà satisfait : les classes de salaires sont rangées du plus
bas au plus haut. Vérifie-le systématiquement avant de cumuler.
:::

**Tableau de calcul (diapositive 65).** On cumule les parts calculées en § 2.3.3 et § 2.3.4.

**Agrégats cumulés des salaires, années 2005 et 2021**

| Part cumulée des salariés en % | Part cumulée de la masse salariale en % en 2005 | Part cumulée de la masse salariale en % en 2021 |
|---|---|---|
| 20 | 11,2 | 3,9 |
| 40 | 24,5 | 14,5 |
| 60 | 40,7 | 32,9 |
| 80 | 61,8 | 59,6 |
| 100 | 100,0 | 100,0 |

::: correction Reconstruction des cumuls, ligne par ligne
**2005** — on additionne 11,2 · 13,3 · 16,2 · 21,1 · 38,2 :

| Ligne | Calcul | Cumul |
|---|---|---|
| 20 % | 11,2 | **11,2** ✔ |
| 40 % | 11,2 + 13,3 | **24,5** ✔ |
| 60 % | 24,5 + 16,2 | **40,7** ✔ |
| 80 % | 40,7 + 21,1 | **61,8** ✔ |
| 100 % | 61,8 + 38,2 | **100,0** ✔ |

**2021** — on additionne 3,9 · 10,6 · 18,4 · 26,7 · 40,5 :

| Ligne | Calcul | Cumul |
|---|---|---|
| 20 % | 3,9 | **3,9** ✔ |
| 40 % | 3,9 + 10,6 | **14,5** ✔ |
| 60 % | 14,5 + 18,4 | **32,9** ✔ |
| 80 % | 32,9 + 26,7 | **59,6** ✔ |
| 100 % | 59,6 + 40,5 | **100,1** ⚠ — le support écrit **100,0** |

**Le support a cumulé les parts *arrondies*, puis a forcé la dernière ligne à 100,0.** C'est
l'excédent d'arrondi de 0,1 identifié en § 2.3.4. Ce n'est pas une faute : c'est une
convention d'affichage. Mais elle a une conséquence chiffrée que je détaille en § 2.3.8 —
elle décale le Gini d'environ 0,0006. **Négligeable pour la conclusion, à mentionner pour la
rigueur.**

**Le même effet existe en 2005** : les cumuls exacts sont 11,200 · 24,536 · **40,780** ·
61,835 · 100,000. Le support affiche 40,7 parce qu'il a cumulé 11,2 + 13,3 + 16,2 = 40,7,
alors que l'arrondi du cumul exact donnerait 40,8. **Retiens la règle : cumuler des arrondis
n'est pas la même chose qu'arrondir des cumuls.**
:::

<!--saut-->

**Le graphe (diapositive 66).** Le support affiche les deux courbes. Le voici reconstruit,
avec l'élément que le support **omet et sans lequel la figure ne se lit pas : la diagonale
d'égalité parfaite.**

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

  Part cumulée de la masse salariale (ordonnée)
  en fonction de la part cumulée des salariés (abscisse)

  . . .  diagonale d'égalité parfaite (L(F) = F)
  o o o  courbe de Lorenz 2005   —  O = points calculés (20/40/60/80 %)
  * * *  courbe de Lorenz 2021   —  # = points calculés (20/40/60/80 %)
```

::: piege La diagonale manque sur le graphe du support
La figure de la diapositive 66 affiche les deux courbes **sans la diagonale**. Or **toute la
lecture d'une courbe de Lorenz consiste à mesurer son écart à la diagonale.** Sans elle, on
voit deux courbes croissantes et convexes, et rien d'autre.

**Réflexe à acquérir : quand tu traces une courbe de Lorenz, tu traces d'abord la
diagonale.** Un correcteur qui voit une courbe de Lorenz sans droite d'égalité sait que le
concept n'est pas compris.
:::

::: demo Les quatre propriétés de la courbe de Lorenz — toutes démontrables
**Propriété 1 — Elle part de (0 ; 0) et arrive à (100 ; 100).**
En 0 % de la population, on a cumulé 0 % de la masse : $ L(0) = 0 $. En 100 % de la
population, on a cumulé toute la masse : $ L(100) = 100 $. **Ce sont deux points imposés :
si ta courbe ne passe pas par eux, tu as une erreur de cumul.**

**Propriété 2 — Elle est croissante.**
Passer de la fréquence cumulée $ F_k $ à $ F_{k+1} $ ajoute la part $ p_{k+1} \ge 0 $ : un
cumul de quantités positives ne peut pas décroître. **Une courbe de Lorenz qui redescend est
mathématiquement impossible.**

**Propriété 3 — Sa pente sur la classe $ k $ vaut $ m_{X_k} / m_X $.**
C'est le résultat le plus utile de toute la section, et le support ne l'énonce pas. Sur le
segment correspondant à la classe $ k $ :

$$ \text{pente} = \frac{\Delta L}{\Delta F} = \frac{p_k}{f_k} = \frac{f_k \, m_{X_k} / m_X}{f_k} = \frac{m_{X_k}}{m_X} $$

**Lecture :** en chaque point, la pente de la courbe de Lorenz est le **rapport entre le
salaire moyen local et le salaire moyen général**. Trois conséquences immédiates :
- **Pente < 1** ⇔ la classe gagne moins que la moyenne ⇔ la courbe s'écarte de la diagonale.
- **Pente = 1** ⇔ la classe gagne exactement la moyenne ⇔ la courbe est parallèle à la
  diagonale : c'est le point **le plus bas** par rapport à la diagonale, donc l'endroit où
  l'écart est maximal.
- **Pente > 1** ⇔ la classe gagne plus que la moyenne ⇔ la courbe revient vers la diagonale.

*Vérification sur 2005 :* pentes $ = 11\,947/21\,333 = 0{,}56 $ ; $ 14\,225/21\,333 = 0{,}67 $ ;
$ 17\,327/21\,333 = 0{,}81 $ ; $ 22\,458/21\,333 = 1{,}05 $ ; $ 40\,709/21\,333 = 1{,}91 $.
La pente franchit 1 **entre le 3ᵉ et le 4ᵉ quintile** : c'est là que se situe le salaire
moyen, et c'est là que l'écart à la diagonale est maximal (à 60 % : $ 60 - 40{,}7 = 19{,}3 $
points, contre 18,2 à 80 % et 15,5 à 40 %). ✔

**Propriété 4 — Elle est convexe, et située sous la diagonale.**
La convexité découle de la propriété 3 : les classes étant rangées par $ m_{X_k} $ croissant,
les pentes $ m_{X_k}/m_X $ sont croissantes — **une courbe dont la pente croît est convexe**.
Et comme elle relie (0 ; 0) à (100 ; 100) en étant convexe, **elle passe nécessairement sous
la corde qui joint ces deux points, c'est-à-dire sous la diagonale**.

**Le cas limite :** si tout le monde gagne la même chose, toutes les pentes valent 1, la
courbe **est** la diagonale. **La diagonale est donc la courbe de Lorenz de l'égalité
parfaite** — d'où son nom de « droite d'égalité ».
:::

::: exemple Les phrases de lecture à savoir produire
À partir du tableau des cumuls, **quatre phrases par année**, toutes construites sur le même
moule :

**2005**
- Les **20 %** des salariés les moins payés perçoivent **11,2 %** de la masse salariale.
- Les **40 %** les moins payés en perçoivent **24,5 %**.
- Les **60 %** les moins payés en perçoivent **40,7 %** — donc les **40 % les mieux payés en
  perçoivent 59,3 %**.
- Les **80 %** les moins payés en perçoivent **61,8 %** — donc les **20 % les mieux payés en
  perçoivent 38,2 %**.

**2021**
- Les **20 %** les moins payés perçoivent **3,9 %** de la masse salariale.
- Les **40 %** les moins payés en perçoivent **14,5 %**.
- Les **60 %** les moins payés en perçoivent **32,9 %** — les **40 % du haut en perçoivent
  67,1 %**.
- Les **80 %** les moins payés en perçoivent **59,6 %** — les **20 % du haut en perçoivent
  40,4 %**.

::: piege
**Le complément à 100 se lit toujours par le haut.** $ 100 - L(80) $ n'est pas « la part des
20 % du bas » mais **la part des 20 % du haut**. Inverser les deux est l'erreur de lecture la
plus fréquente. **Repère mental : la courbe de Lorenz se lit toujours en partant des plus
pauvres ; tout ce qui reste au-dessus appartient aux plus riches.**
:::
:::

<!--saut-->

#### 2.3.7 Interpréter et comparer deux courbes de Lorenz (diapositive 67)

::: definition Les trois énoncés du support, reformulés
1. **Plus la courbe s'éloigne de la diagonale, plus la concentration est forte** et plus les
   inégalités sont prégnantes.
2. **Si une courbe est partout plus éloignée de la diagonale qu'une autre**, l'inégalité est
   accrue **pour tous les ordres de quantiles** : tous les indicateurs d'inégalité
   convergent alors vers la même conclusion. On dit que la première distribution est
   **dominée au sens de Lorenz** par la seconde.
3. **Si les deux courbes se croisent**, on peut encore mesurer l'aire séparant chaque courbe
   de la diagonale (c'est l'indice de Gini), mais **des indicateurs différents peuvent alors
   donner des conclusions contradictoires**.
:::

::: demo Pourquoi la dominance de Lorenz est un résultat fort — et pourquoi le croisement casse tout
**Le cas de la dominance.** Si $ L_A(F) \le L_B(F) $ pour **toutes** les valeurs de $ F $,
alors pour n'importe quel seuil que tu choisisses — les 10 % du bas, les 25 % du bas, la
moitié du bas — la distribution A donne toujours moins que B. **Aucun choix d'indicateur ne
peut inverser la conclusion**, parce que tout indicateur d'inégalité usuel se construit à
partir de ces parts cumulées. C'est ce que signifie « tous les indicateurs convergent ».

**Le cas du croisement.** Si les courbes se croisent, A est plus inégalitaire **en bas** de
la distribution et B plus inégalitaire **en haut** (ou l'inverse). Le classement dépend alors
de **ce à quoi l'indicateur choisi accorde du poids**.

**Contre-exemple chiffré, à savoir produire.** Deux pays, cinq quintiles, parts de la masse
salariale :

| Quintile | Pays A | Pays B | Cumul A | Cumul B |
|---|---|---|---|---|
| 1ᵉʳ | 4 | 8 | 4 | 8 |
| 2ᵉ | 12 | 10 | 16 | 18 |
| 3ᵉ | 20 | 15 | 36 | 33 |
| 4ᵉ | 28 | 22 | 64 | 55 |
| 5ᵉ | 36 | 45 | 100 | 100 |
| **Total** | **100** | **100** | | |

Les cumuls se croisent : A est en dessous à 20 % (4 < 8) mais au-dessus à 60 % (36 > 33) et
à 80 % (64 > 55). **Les courbes se croisent entre 40 % et 60 %.**

Conclusion selon l'indicateur retenu :
- **Rapport inter-quintile** $ Q_5/Q_1 $ : A = $ 36/4 = 9{,}0 $ ; B = $ 45/8 = 5{,}6 $ →
  **A est plus inégalitaire.**
- **Part du quintile supérieur** : A = 36 % ; B = 45 % → **B est plus inégalitaire.**

**Deux indicateurs, deux réponses opposées, sur les mêmes données.** C'est exactement ce que
prévient le support. **La leçon : en cas de croisement, on ne tranche pas — on décrit les
deux phénomènes.**
:::

::: correction Application au cas 2005 / 2021 : y a-t-il croisement ?
On compare les cumuls point par point :

| $ F $ | $ L_{2005} $ | $ L_{2021} $ | $ L_{2021} - L_{2005} $ |
|---|---|---|---|
| 20 % | 11,2 | 3,9 | **− 7,3** |
| 40 % | 24,5 | 14,5 | **− 10,0** |
| 60 % | 40,7 | 32,9 | **− 7,8** |
| 80 % | 61,8 | 59,6 | **− 2,2** |
| 100 % | 100,0 | 100,0 | 0,0 |

**La différence est négative à chaque point intérieur : la courbe 2021 est partout sous la
courbe 2005. Il n'y a pas de croisement.**

**Conclusion, formulée comme en examen :** « La courbe de Lorenz de 2021 est partout située
en dessous de celle de 2005 : la distribution de 2021 est dominée au sens de Lorenz par celle
de 2005. La concentration de la masse salariale s'est donc accrue, et cette conclusion est
robuste — tous les indicateurs d'inégalité usuels donneront le même verdict. »

**Note l'endroit où l'écart est maximal : à 40 %** (− 10,0 points). L'aggravation ne se joue
donc pas dans le haut de la distribution (où l'écart n'est que de − 2,2 points à 80 %) mais
**dans la première moitié** — cohérent avec l'effondrement de la part du premier quintile
identifié en § 2.3.5.
:::

<!--saut-->

#### 2.3.8 L'indice de Gini (diapositives 68 et 69)

La courbe de Lorenz est une image. **L'indice de Gini est le nombre qui la résume.**

::: definition L'indice de Gini
Géométriquement, l'indice de Gini **correspond à 2 fois l'aire comprise entre la courbe de
Lorenz et la diagonale**. Cette aire est appelée **aire de concentration**.

$$ G = 2 \times \mathcal{A} \qquad \text{avec } \mathcal{A} = \text{aire entre la diagonale et la courbe} $$

- **Plus $ G $ est proche de 1**, plus la concentration (l'inégalité) est **forte**.
- **Plus $ G $ est proche de 0**, plus la concentration (l'inégalité) est **faible**.
:::

::: formule La formule de calcul (diapositive 69)
$$ G = 2 \left[ \frac{1}{2} - \sum \frac{(b + B) \cdot h}{2} \right] $$

où, pour chaque tranche : $ b $ est la **petite base** (la valeur cumulée à gauche), $ B $ la
**grande base** (la valeur cumulée à droite) et $ h $ la **hauteur** — c'est-à-dire la
largeur de la tranche en abscisse.
:::

::: demo D'où vient cette formule — la construction complète
Le support donne la formule sans la construire. Elle repose sur trois idées enchaînées.

**Idée 1 — L'aire du carré unité vaut 1.** La courbe de Lorenz vit dans un carré de côté 1
(ou 100 %). L'aire totale du carré vaut $ 1 \times 1 = 1 $.

**Idée 2 — L'aire sous la diagonale vaut 1/2.** La diagonale coupe le carré en deux triangles
rectangles isocèles identiques. L'aire du triangle sous la diagonale vaut donc
$ \frac{1 \times 1}{2} = \frac{1}{2} $.

**Idée 3 — L'aire de concentration est une soustraction.** L'aire entre la diagonale et la
courbe s'obtient en retirant, du triangle sous la diagonale, l'aire située **sous la
courbe** :

$$ \mathcal{A} = \underbrace{\frac{1}{2}}_{\text{aire sous la diagonale}} - \underbrace{\mathcal{B}}_{\text{aire sous la courbe de Lorenz}} $$

**Idée 4 — L'aire sous la courbe se découpe en trapèzes.** Entre deux points consécutifs de
la courbe, celle-ci est un **segment de droite**. La surface comprise entre ce segment,
l'axe des abscisses et les deux verticales est donc **un trapèze**. Rappel de l'aire d'un
trapèze :

$$ \text{aire} = \frac{(\text{petite base} + \text{grande base}) \times \text{hauteur}}{2} = \frac{(b + B) \cdot h}{2} $$

En sommant sur toutes les tranches : $ \mathcal{B} = \sum \frac{(b+B) \cdot h}{2} $.

**Assemblage final :**

$$ G = 2\mathcal{A} = 2 \left[ \frac{1}{2} - \sum \frac{(b+B) \cdot h}{2} \right] $$

**C'est exactement la formule du support — mais maintenant tu sais pourquoi.**
:::

::: piege LE piège de calcul du chapitre : l'unité des aires
Le support affiche, sur le graphe de la diapositive 68, un trapèze avec $ b = 40{,}7 $,
$ B = 61{,}8 $, $ h = 20 $ et l'aire **1 025**. Puis il écrit
$ \mathcal{A} = 0{,}5 - \text{aire des trapèzes} $.

**Ces deux nombres ne sont pas dans la même unité, et si tu les soustrais tels quels tu
obtiens une aberration.**

- Le 1 025 est calculé avec des **axes gradués en pourcentages** (de 0 à 100). Il est donc
  exprimé en « points de pourcentage au carré ». Dans cette unité, **le carré entier vaut
  $ 100 \times 100 = 10\,000 $**, et le triangle sous la diagonale vaut **5 000**.
- Le 0,5 de la formule est exprimé en **fractions** (de 0 à 1), unité dans laquelle **le carré
  vaut 1**.

**Il faut donc ramener les trapèzes à l'unité « fraction » en divisant par 10 000** — ou, de
manière équivalente, appliquer la formule avec des cumuls exprimés en fractions (0,112 au
lieu de 11,2) et des hauteurs de 0,20 au lieu de 20.

$$ \boxed{\; \mathcal{A} = \frac{1}{2} - \frac{\sum (b+B) \cdot h / 2}{10\,000} \quad \text{si les cumuls sont en \%} \;} $$

**Test de cohérence à faire systématiquement :** l'aire de concentration doit toujours être
comprise **entre 0 et 0,5**, et le Gini **entre 0 et 1**. Si tu obtiens $ 0{,}5 - 3\,764 $,
tu sais immédiatement que tu as oublié la conversion.
:::

::: correction Calcul complet du Gini 2005
**Les cumuls (diapositive 65) :** 0 → 11,2 → 24,5 → 40,7 → 61,8 → 100,0. Chaque tranche a
une hauteur $ h = 20 $ (en abscisse, chaque quintile occupe 20 points de pourcentage).

| Tranche | $ b $ (cumul gauche) | $ B $ (cumul droit) | $ h $ | Aire $ = (b+B) \times h / 2 $ |
|---|---|---|---|---|
| 0 → 20 % | 0,0 | 11,2 | 20 | $ (0 + 11{,}2) \times 20 / 2 = \mathbf{112{,}0} $ |
| 20 → 40 % | 11,2 | 24,5 | 20 | $ (11{,}2 + 24{,}5) \times 20 / 2 = \mathbf{357{,}0} $ |
| 40 → 60 % | 24,5 | 40,7 | 20 | $ (24{,}5 + 40{,}7) \times 20 / 2 = \mathbf{652{,}0} $ |
| 60 → 80 % | 40,7 | 61,8 | 20 | $ (40{,}7 + 61{,}8) \times 20 / 2 = \mathbf{1\,025{,}0} $ |
| 80 → 100 % | 61,8 | 100,0 | 20 | $ (61{,}8 + 100{,}0) \times 20 / 2 = \mathbf{1\,618{,}0} $ |
| **Somme** | | | | $ \mathbf{3\,764{,}0} $ |

**Le trapèze 60 → 80 % vaut 1 025 — c'est exactement la valeur affichée sur le graphe du
support ✔.** La méthode est donc validée.

**Conversion :** $ 3\,764 / 10\,000 = 0{,}3764 $.

**Aire de concentration :** $ \mathcal{A} = 0{,}5 - 0{,}3764 = \mathbf{0{,}1236} $.

**Indice de Gini :** $ G_{2005} = 2 \times 0{,}1236 = \mathbf{0{,}2472} $.
:::

::: correction Calcul complet du Gini 2021
**Les cumuls :** 0 → 3,9 → 14,5 → 32,9 → 59,6 → 100,0, avec $ h = 20 $.

| Tranche | $ b $ | $ B $ | $ h $ | Aire $ = (b+B) \times h / 2 $ |
|---|---|---|---|---|
| 0 → 20 % | 0,0 | 3,9 | 20 | $ (0 + 3{,}9) \times 10 = \mathbf{39{,}0} $ |
| 20 → 40 % | 3,9 | 14,5 | 20 | $ (3{,}9 + 14{,}5) \times 10 = \mathbf{184{,}0} $ |
| 40 → 60 % | 14,5 | 32,9 | 20 | $ (14{,}5 + 32{,}9) \times 10 = \mathbf{474{,}0} $ |
| 60 → 80 % | 32,9 | 59,6 | 20 | $ (32{,}9 + 59{,}6) \times 10 = \mathbf{925{,}0} $ |
| 80 → 100 % | 59,6 | 100,0 | 20 | $ (59{,}6 + 100{,}0) \times 10 = \mathbf{1\,596{,}0} $ |
| **Somme** | | | | $ \mathbf{3\,218{,}0} $ |

**Conversion :** $ 3\,218 / 10\,000 = 0{,}3218 $.

**Aire de concentration :** $ \mathcal{A} = 0{,}5 - 0{,}3218 = \mathbf{0{,}1782} $.

**Indice de Gini :** $ G_{2021} = 2 \times 0{,}1782 = \mathbf{0{,}3564} $.

::: piege
**Astuce de calcul :** puisque $ h = 20 $ pour toutes les tranches,
$ (b+B) \times 20 / 2 = (b+B) \times 10 $. **Multiplier par 10 au lieu de diviser par 2 après
avoir multiplié par 20** : deux opérations en moins par ligne, et autant d'erreurs évitées.
:::
:::

::: exemple Le résultat, et sa lecture
| | 2005 | 2021 | Évolution |
|---|---|---|---|
| Aire sous la courbe | 0,3764 | 0,3218 | − 0,0546 |
| Aire de concentration $ \mathcal{A} $ | 0,1236 | 0,1782 | **+ 0,0546** |
| **Indice de Gini** | **0,2472** | **0,3564** | **+ 0,1092** |
| En variation relative | | | **+ 44,2 %** |

**Les trois phrases à écrire :**
1. « L'indice de Gini des salaires passe de **0,247 en 2005 à 0,356 en 2021**, soit une hausse
   de **près de 11 points**, ou **+ 44 % en relatif**. »
2. « La concentration de la masse salariale s'est donc **fortement accrue** sur la période. »
3. « Ce diagnostic est **cohérent avec la courbe de Lorenz**, qui est partout plus éloignée de
   la diagonale en 2021 qu'en 2005 (dominance de Lorenz, § 2.3.7) : il n'y a pas de
   croisement, donc pas de risque de contradiction entre indicateurs. »

**Et la réserve méthodologique du § 2.3.5 reste entière :** une partie de cette hausse peut
provenir d'un changement de champ entre les deux millésimes. Le Gini mesure ce qu'on lui
donne à mesurer.
:::

::: piege L'écart entre le Gini « du tableau » et le Gini exact
Si l'on refait les deux calculs avec les parts **non arrondies** (§ 2.3.3 et § 2.3.4) au lieu
des cumuls arrondis du support, on obtient :

| | Gini calculé sur le tableau du support | Gini calculé sur les parts exactes | Écart |
|---|---|---|---|
| 2005 | 0,2472 | **0,2466** | 0,0006 |
| 2021 | 0,3564 | **0,3570** | 0,0006 |
| Hausse | + 0,1092 | **+ 0,1104** | 0,0012 |

**Trois enseignements.**
1. **L'écart est de l'ordre du millième** : il ne change **aucune** conclusion. Un Gini
   s'annonce à trois décimales au plus, souvent à deux.
2. **Il va dans le sens qui sous-estime la hausse** : le calcul du support donne + 0,1092 là
   où le calcul exact donne + 0,1104. L'arrondi n'a donc pas fabriqué le résultat.
3. **La bonne pratique** : mener les calculs intermédiaires avec le maximum de décimales et
   n'arrondir qu'au dernier moment. **En examen, si tu utilises le tableau fourni, tu utilises
   ses valeurs — et tu écris une ligne pour dire que les arrondis affectent la 3ᵉ décimale.**
:::

::: demo Pourquoi $ 0 \le G \le 1 $ — les deux bornes démontrées
**Borne inférieure : $ G = 0 $ ⇔ égalité parfaite.**
Si tout le monde a la même valeur, chaque tranche de $ f $ % de la population détient $ f $ %
de l'agrégat : la courbe **est** la diagonale. L'aire entre les deux est nulle, donc
$ \mathcal{A} = 0 $ et $ G = 0 $.

*Vérification par la formule :* les cumuls sont 20 · 40 · 60 · 80 · 100, d'où les trapèzes
$ (0+20)\times10 = 200 $ ; $ (20+40)\times10 = 600 $ ; $ (40+60)\times10 = 1\,000 $ ;
$ (60+80)\times10 = 1\,400 $ ; $ (80+100)\times10 = 1\,800 $ ; somme $ = 5\,000 $.
$ \mathcal{A} = 0{,}5 - 5\,000/10\,000 = 0 $, donc $ G = 0 $ ✔

**Borne supérieure : $ G \to 1 $ ⇔ concentration totale.**
Si **un seul individu** détient tout l'agrégat, la courbe reste collée à l'axe horizontal
($ L = 0 $) sur toute la population sauf le dernier individu, puis saute à 100 %. L'aire sous
la courbe tend vers 0, donc $ \mathcal{A} \to 0{,}5 $ et $ G \to 1 $.

::: piege
**Précision que l'on attend d'une excellente copie : avec une population finie de $ N $
individus, le maximum n'est pas exactement 1 mais $ \frac{N-1}{N} $.** Le dernier individu
occupe en effet une largeur $ 1/N $ non nulle, sous laquelle subsiste un petit triangle
d'aire $ \frac{1}{2N} $. On a alors
$ \mathcal{A} = \frac{1}{2} - \frac{1}{2N} $ et $ G = 1 - \frac{1}{N} $.
Pour $ N = 100 $, le maximum atteignable vaut 0,99 ; pour $ N \to \infty $, il tend vers 1.
**En pratique on retient 0 ≤ G ≤ 1 ; savoir d'où vient la nuance est un bonus.**
:::
:::

::: exemple Des ordres de grandeur pour interpréter un Gini
Un Gini nu ne dit rien : il faut une échelle de comparaison. **Ordres de grandeur usuels pour
le revenu disponible des ménages** (à retenir comme repères, pas comme chiffres exacts — ils
varient selon l'année, la source et le concept mesuré) :

| Situation | Gini approximatif |
|---|---|
| Pays nordiques (Danemark, Norvège, Suède) | 0,25 – 0,28 |
| France, Allemagne, Pays-Bas | 0,29 – 0,32 |
| Royaume-Uni, Italie | 0,33 – 0,36 |
| États-Unis | 0,38 – 0,41 |
| Brésil, Colombie | 0,48 – 0,54 |
| Afrique du Sud | ≈ 0,63 |

::: piege
**Trois précautions avant toute comparaison de Gini.**
1. **Le concept mesuré change tout.** Le Gini du **patrimoine** est toujours bien plus élevé
   que celui du **revenu** (le patrimoine peut être nul ou négatif, pas le revenu du travail) :
   en France, on est autour de 0,3 pour le revenu disponible et **au-delà de 0,6** pour le
   patrimoine. Comparer les deux n'a aucun sens.
2. **Avant ou après redistribution ?** Le Gini des revenus **primaires** (avant impôts et
   prestations) est nettement supérieur au Gini du revenu **disponible**. La différence entre
   les deux mesure précisément l'effet redistributif du système socio-fiscal.
3. **Le Gini est peu sensible aux extrêmes.** Il réagit surtout aux transferts autour du
   **milieu** de la distribution et beaucoup moins à ce qui se passe dans le tout dernier
   centile. C'est pourquoi on l'accompagne toujours d'indicateurs de queue : **rapport
   D9/D1** et **part du 1 % le plus riche**. Un Gini stable peut parfaitement masquer un
   décrochage du sommet.

**Nos deux valeurs (0,247 et 0,356) portent sur les *salaires*, pas sur le revenu
disponible : elles ne sont pas directement comparables aux chiffres du tableau ci-dessus.**
Les salaires excluent les revenus du capital, les prestations sociales et l'impôt.
:::
:::

::: marche La concentration, en salle de marché
Le raisonnement de Lorenz-Gini s'applique tel quel dès qu'on partage un total.

**1. La concentration d'un portefeuille.** Trie tes positions par poids croissant, cumule :
tu obtiens la courbe de Lorenz de ton exposition. Un portefeuille dont 20 % des lignes
portent 80 % du risque a un Gini élevé — c'est une **concentration**, donc une fragilité.
L'indicateur standard du métier est l'**indice de Herfindahl-Hirschman**
$ HHI = \sum_i w_i^2 $ (somme des carrés des poids), qui répond à la même question par une
autre algèbre : $ HHI = 1/n $ pour $ n $ positions équipondérées, et tend vers 1 quand tout
est sur une ligne. **Un mandat de gestion impose presque toujours un plafond de HHI ou un
poids maximal par ligne : c'est une contrainte de concentration.**

**2. La concentration du P&L.** Trie tes trades par résultat croissant et cumule. Presque tous
les track records révèlent la même chose : **une petite minorité de trades fait la totalité
du résultat**. Ce n'est pas anormal — c'est la signature d'une stratégie à espérance positive
et asymétrie droite. **Ce qui est dangereux, c'est l'inverse :** un P&L dont la concentration
vient de quelques **pertes** énormes compensées par beaucoup de petits gains — le profil
« ramasser des pièces devant un rouleau compresseur ». **La courbe de Lorenz de ton P&L
distingue les deux en un coup d'œil ; la moyenne, non.**

**3. La concentration du marché.** Part des dix premières capitalisations dans un indice,
part des trois premiers courtiers sur un carnet d'ordres, part des deux premiers clients dans
le chiffre d'affaires d'une société que tu analyses : **c'est la même part de l'agrégat**. En
analyse crédit, la concentration clientèle est un facteur de risque explicitement noté.

**Le lien conceptuel avec la dispersion est le même que dans tout le chapitre :** l'écart-type
te dit de combien les positions varient, le Gini te dit si le total repose sur quelques-unes.
**Deux questions différentes, deux outils différents, et aucun ne remplace l'autre.**
:::

<!--saut-->

### 2.4 — Récapitulons (diapositive 70)

Le support conclut en trois lignes : tu sais résumer une distribution à l'aide d'indicateurs
de **position** (mode, moyenne, médiane), de **dispersion** (EAM, variance, écart-type,
coefficient de variation) et de **concentration** (courbe de Lorenz, indice de Gini), et
**le choix dépend du type de données mais aussi de ce que l'on veut en faire**.

Cette conclusion est juste, mais elle est trop courte pour servir de récapitulatif. Voici le
tableau complet du chapitre.

::: synthese Les treize indicateurs du chapitre, en un tableau
| Famille | Indicateur | Formule | Ce qu'il mesure | Unité | Sensible aux extrêmes ? | Quand le choisir |
|---|---|---|---|---|---|---|
| **Position** | Mode | Modalité de fréquence max (ou densité max si classes inégales) | La valeur la plus fréquente | Celle de $ X $ | Non | Seul indicateur valable pour une variable **qualitative** |
| | Moyenne | $ m_X = \frac{1}{N}\sum x_i $ | Le centre de gravité | Celle de $ X $ | **Oui, fortement** | Distribution symétrique ; calculs ultérieurs (linéarité, agrégation) |
| | Médiane | $ F(\text{Me}) = 0{,}5 $ | La valeur qui coupe l'effectif en deux | Celle de $ X $ | Non | Distribution asymétrique ; présence de valeurs extrêmes |
| **Dispersion** | Étendue | $ x_{\max} - x_{\min} $ | L'amplitude totale | Celle de $ X $ | **Oui, totalement** | Première approche, jamais seule |
| | Écart inter-quartile | $ Q_3 - Q_1 $ | L'étalement des 50 % centraux | Celle de $ X $ | Non | Accompagne la médiane ; base du *boxplot* |
| | Écart inter-décile | $ D_9 - D_1 $ | L'étalement des 80 % centraux | Celle de $ X $ | Peu | Comparaisons de niveaux de vie |
| | EAM | $ \frac{1}{N}\sum \|x_i - m_X\| $ | L'écart moyen à la moyenne | Celle de $ X $ | Oui | Interprétation directe ; peu utilisé car non dérivable |
| | Variance | $ \frac{1}{N}\sum (x_i - m_X)^2 $ | La dispersion quadratique | **Celle de $ X $ au carré** | **Oui, très** | Étape de calcul, décompositions |
| | Écart-type | $ \sigma = \sqrt{V} $ | La dispersion, en unité lisible | Celle de $ X $ | **Oui, très** | **L'indicateur de référence** ; volatilité en finance |
| | Coefficient de variation | $ CV = \sigma / m_X $ | La dispersion **relative** | **Sans unité** | Oui | Comparer des séries d'unités ou d'échelles différentes |
| **Concentration** | Part de l'agrégat | $ p_k = f_k m_{X_k}/m_X $ | La part du total détenue par une classe | Sans unité (%) | — | Première lecture des inégalités |
| | Courbe de Lorenz | $ L(F) $ = part cumulée de $ X $ | Le partage complet du total | Sans unité | — | Comparer deux distributions (dominance) |
| | Indice de Gini | $ G = 2\left[\frac{1}{2} - \sum\frac{(b+B)h}{2}\right] $ | La concentration en **un** nombre | **Sans unité, entre 0 et 1** | Peu (milieu surtout) | Résumer, classer, suivre une évolution |
:::

::: methode L'arbre de décision : quel indicateur, quand ?
**Question 1 — Quel est le type de la variable ?**
- **Qualitative** → **mode uniquement**. Ni moyenne, ni médiane, ni variance, ni Gini.
- **Quantitative ordinale** (rangs, échelles) → mode et médiane ; **pas de moyenne** au sens
  strict.
- **Quantitative cardinale** → tout est permis. Passe à la question 2.

**Question 2 — Que veux-tu décrire ?**
- **Le niveau typique** → position. Passe à la question 3.
- **L'homogénéité de la population** → dispersion. Passe à la question 4.
- **Le partage d'un total** → concentration. Vérifie d'abord que la somme fait sens
  (§ 2.3.1), puis part de l'agrégat → Lorenz → Gini.

**Question 3 — La distribution est-elle symétrique ?**
- **Oui** → moyenne (et médiane ≈ moyenne, ce qui le confirme).
- **Non, ou valeurs extrêmes présentes** → **médiane**, en donnant aussi la moyenne pour
  montrer l'asymétrie. **Écart médiane / moyenne = diagnostic d'asymétrie.**

**Question 4 — Compares-tu des séries de même unité et de même ordre de grandeur ?**
- **Oui** → **écart-type**.
- **Non** (unités différentes, ou moyennes très différentes) → **coefficient de variation**.
- **Tu veux résister aux valeurs extrêmes** → écarts inter-quantiles et *boxplot*.

**Question 5 — Le résultat doit-il être agrégé ou décomposé ?**
- **Agrégation de moyennes** → moyenne pondérée par les effectifs (§ 2.1.7).
- **Agrégation de variances** → Koenig, ou décomposition intra/inter (§ 2.2.17 et § 2.2.18).
- **Jamais** d'agrégation de médianes ni de Gini (§ 2.1.15).
:::

::: piege La phrase du support à ne pas lire trop vite
> « Le choix d'indicateurs dépend du type de données **mais aussi de ce que l'on veut en
> faire**. »

**La seconde moitié de la phrase est la plus importante, et c'est celle qu'on oublie.** Le
type de données élimine des indicateurs (on ne calcule pas une moyenne de couleurs).
**L'objectif, lui, tranche entre ceux qui restent.**

Trois exemples où les données autorisent tout et où seul l'objectif décide :
- **Décrire le salaire « typique » d'une profession** → médiane (l'asymétrie rend la moyenne
  trompeuse).
- **Calculer la masse salariale à provisionner** → moyenne (× effectif : c'est la seule qui
  ait la propriété d'agrégation).
- **Vérifier qu'aucun salarié n'est décroché** → écarts inter-déciles et part du premier
  quintile.

**Mêmes données, trois indicateurs différents, trois questions différentes. Un correcteur
attend que tu justifies ton choix — pas que tu calcules tout.**
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
aucune ✖.** Les 24 ⚠ ne signalent aucune lacune de ce document : elles marquent les endroits
où le support d'origine était elliptique (images non commentées, questions posées sans
réponse, méthode implicite), incohérent ou erroné — et où la reconstruction est explicitement
signalée à l'endroit exact.

**Les quatre anomalies de fond** — diapositives **35** (titre erroné), **43** (écart-type
jamais calculé), **48** (conclusion non démontrable) et **55** (variance fausse d'un facteur
2) — sont récapitulées au § 3.4.
