---
matiere: Techniques statistiques
titre: Formulaire cumulatif — Techniques statistiques
sous_titre: Toutes les formules de tous les chapitres, dans l'ordre du cours
resume: Généré automatiquement à partir des encadrés « formule » des cours. 22 formule(s).
sommaire: oui
---

## Chapitre 1 — Présenter pour informer

::: formule Diapositive 23 — à savoir écrire
- Le caractère statistique est noté **$ X $**, les modalités **$ x_i $** sont **ordonnées** de
  $ i = 1, \ldots, p $.
- À chaque modalité $ x_i $ correspond un **effectif $ n_i $**, et l'**effectif total** vaut

$$ n = \sum_{i=1}^{p} n_i = n_1 + n_2 + \ldots + n_p $$

- Les **fréquences** $ f_i $, pour $ i = 1, \ldots, p $, se calculent ainsi :

$$ f_i = \frac{n_i}{n} $$

- Les **fréquences cumulées** $ F_k $, pour $ k = 1, \ldots, p $, sont telles que :

$$ F_k = \sum_{i=1}^{k} f_i $$
:::

::: formule Le symbole Σ, si tu ne l'as jamais manipulé
$ \sum_{i=1}^{p} n_i $ se lit **« somme des $ n_i $ pour $ i $ allant de 1 à $ p $ »**, et
signifie exactement $ n_1 + n_2 + \ldots + n_p $.

- **$ i $** est un **compteur** : il prend successivement les valeurs 1, 2, …, $ p $.
- **Le nombre du bas** dit où il commence, **celui du haut** où il s'arrête.
- **Le nom du compteur est sans importance** : $ \sum_{i=1}^{p} n_i $ et
  $ \sum_{k=1}^{p} n_k $ désignent le même nombre.

**Les deux formules du chapitre se lisent alors sans effort :**
$ n = \sum_{i=1}^{p} n_i $ — *l'effectif total est la somme de tous les effectifs*.
$ F_k = \sum_{i=1}^{k} f_i $ — *la fréquence cumulée au rang $ k $ est la somme des
fréquences **jusqu'à** $ k $*. La borne haute est $ k $, pas $ p $ : c'est tout ce qui
distingue un cumul partiel d'un total.
:::

::: formule Les propriétés des fréquences — à connaître et à savoir démontrer
$$ \sum_{i=1}^{p} f_i = 1 = 100\ \% \qquad F_p = 100\ \% \qquad F_{k+1} \geq F_k \qquad f_k = F_k - F_{k-1} \ \text{avec} \ F_0 = 0 $$

Démonstrations : Statistiques Ch01, § 2.3.4. Elles servent de contrôle à chaque tableau construit.
:::

::: formule Taux de variation et points de pourcentage — les deux outils pour commenter un tableau par année
Le support compare des années **sans donner l'outil de la comparaison**. Il est indispensable dès
qu'on commente un tableau comme celui-ci — et c'est l'objet annoncé du chapitre 3,
« évolutions temporelles ».

$$ t = \frac{V_{\text{arrivée}} - V_{\text{départ}}}{V_{\text{départ}}} \times 100 $$

- **$ V_{\text{départ}} $** : la valeur à la date de départ — **c'est le dénominateur**.
- **$ V_{\text{arrivée}} $** : la valeur à la date d'arrivée.
- **$ t $** : la variation **rapportée au point de départ**, en pour cent.

*Pourquoi cette formule :* une hausse de 16 237 personnes ne dit rien seule ; rapportée aux
73 834 de départ, elle devient comparable à n'importe quelle autre évolution.

**Application :** $ t = \dfrac{90\,071 - 73\,834}{73\,834} \times 100 = \dfrac{16\,237}{73\,834} \times 100 = +21{,}99\ \% $,
soit **+22,0 %** de personnes écrouées entre 2020 et 2023.

**L'écart entre deux pourcentages se dit en points de pourcentage.** Les condamnés détenus
représentent 56,3 % des écroués en 2020 et 57,5 % en 2023 : leur part augmente de **1,2 point**
— pas de 1,2 %. Le taux de variation de cette part serait, sur les valeurs arrondies, $ 1{,}2 / 56{,}3 = +2{,}1\ \% $.
**Les deux chiffres sont vrais et ne disent pas la même chose.**
:::

## Chapitre 2 — Résumer pour informer

::: formule Les deux formules de la diapositive
$$ \text{amplitude} = x_{\max} - x_{\min} \qquad
\text{densité} = \frac{\text{fréquence de la classe}}{\text{amplitude de la classe}} $$
:::

::: formule La moyenne sur données brutes
$$ m = \frac{1}{N} \sum_{i=1}^{N} x_i = \frac{1}{N}(x_1 + x_2 + \ldots + x_N) \qquad (3) $$

- $ N $ : le **nombre d'observations** (l'effectif total).
- $ x_i $ : la valeur observée pour la **i-ème unité statistique** de la base.
- **L'indice $ i $ renvoie ici au numéro d'observation**, pas au numéro de modalité.

Ce calcul correspond à celui obtenu à partir de **données brutes** (*raw data*).
:::

::: formule Les deux écritures équivalentes
Pour un caractère $ X $ à $ p $ modalités, d'effectifs $ n_i $ et de fréquences $ f_i $ —
**ici l'indice $ i $ renvoie au numéro de modalité** :

$$ m = \frac{1}{N} \sum_{i=1}^{p} n_i x_i \qquad (4) $$

ou, en plaçant le $ N $ dans la somme, de façon équivalente à partir des fréquences :

$$ m = \sum_{i=1}^{p} \frac{n_i}{N} x_i = \sum_{i=1}^{p} f_i x_i \qquad (5) $$
:::

::: formule La moyenne d'une population à partir des moyennes de ses sous-populations
Soient $ K $ sous-populations **disjointes** d'effectifs $ n_k $, avec
$ N = \sum_{k=1}^{K} n_k $, et de moyennes respectives $ m_k $. Alors :

$$ m = \sum_{k=1}^{K} \frac{n_k}{N}\, m_k \qquad (6) $$

Il s'agit d'une **moyenne pondérée par la part de la sous-population dans la population
entière**, $ n_k / N $.
:::

::: formule Linéarité
$$ \text{si } Y = aX + b \text{ alors } m_Y = a\,m_X + b \qquad (8) $$

- Multiplier toutes les valeurs par $ a $ multiplie la moyenne par $ a $.
- Ajouter $ b $ à toutes les valeurs augmente la moyenne de $ b $.
- **A fortiori**, la moyenne de la somme de deux variables est la somme des moyennes.
:::

::: formule Interpolation linéaire
Lorsque les données sont présentées sous forme de distribution intégrant les **fréquences
cumulées** :
- **si on dispose d'une valeur de $ X $ telle que $ F(x_j) = 50\ \% $, alors la médiane vaut
  $ x_j $** ;
- **dans le cas contraire, on procède par interpolation linéaire.** Si $ F(x_a) < 50\ \% $ et
  $ F(x_b) > 50\ \% $ :

$$ \text{med} \approx x_a + \frac{(x_b - x_a)\,(0{,}5 - F(x_a))}{F(x_b) - F(x_a)} \qquad (9) $$
:::

::: formule Le quantile d'ordre α %
Lorsque les données sont présentées sous forme de distribution intégrant les fréquences
cumulées :
- **si** on dispose d'une valeur de $ X $ telle que $ F(x_j) = \alpha\ \% $, **alors le
  quantile vaut $ x_j $** ;
- **sinon**, par interpolation linéaire, si $ F(x_a) < \alpha\ \% $ et $ F(x_b) > \alpha\ \% $ :

$$ Q_{\alpha\%} \approx x_a + \frac{(x_b - x_a)\,(\alpha\% - F(x_a))}{F(x_b) - F(x_a)} \qquad (10) $$
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

::: formule La rentabilité journalière
$$ r_t = \frac{P_t - P_{t-1}}{P_{t-1}} \times 100 $$
où $ P_t $ est le prix de clôture du jour et $ P_{t-1} $ celui de la veille.
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

::: formule Le coefficient de variation
- Les mesures de la variance et de l'écart-type sont **sensibles à la conversion d'unités de
  mesure** (changement de monnaie, de métrique, etc.).
- Le coefficient de variation est **exprimé sans unité**, en pourcentage.
- Il permet des **comparaisons d'indicateurs de dispersion entre caractères mesurés
  différemment**.

$$ CV = \frac{\sigma_X}{m_X} $$
:::

::: formule Les quatre écritures équivalentes
Lorsqu'on n'a pas les données brutes mais un **tableau de distribution** — $ p $ modalités,
effectifs $ n_i $, fréquences $ f_i $, l'indice $ i $ renvoyant au **numéro de modalité** :

**À partir des effectifs :**
$$ \sigma^2 = \frac{1}{N} \sum_{i=1}^{p} n_i (x_i - m)^2 = \frac{1}{N} \sum_{i=1}^{p} n_i x_i^2 - m^2 \qquad (11) $$

**À partir des fréquences :**
$$ \sigma^2 = \sum_{i=1}^{p} f_i (x_i - m)^2 = \sum_{i=1}^{p} f_i x_i^2 - m^2 \qquad (12) $$
:::

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

::: formule La somme = la moyenne × l'effectif
$$ \sum_{i=1}^{N_k} x_i = N_k \, m_{X_k} $$

où $ N_k $ est l'effectif de la classe $ k $ et $ m_{X_k} $ la moyenne de $ X $ dans
cette classe.

**En mots :** la somme d'une variable sur un groupe est égale à la moyenne du groupe
multipliée par la taille du groupe. Dans le cas des salaires :

$$ \text{masse salariale de la classe} = \text{salaire moyen de la classe} \times \text{effectif de la classe} $$
:::

::: formule La formule de calcul (diapositive 69)
$$ G = 2 \left[ \frac{1}{2} - \sum \frac{(b + B) \cdot h}{2} \right] $$

où, pour chaque tranche : $ b $ est la **petite base** (la valeur cumulée à gauche), $ B $ la
**grande base** (la valeur cumulée à droite) et $ h $ la **hauteur** — c'est-à-dire la
largeur de la tranche en abscisse.
:::
