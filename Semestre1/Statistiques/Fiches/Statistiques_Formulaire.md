---
matiere: Techniques statistiques
titre: Formulaire cumulatif — Techniques statistiques
sous_titre: Toutes les formules de tous les chapitres, dans l'ordre du cours
resume: Généré automatiquement à partir des encadrés « formule » des cours. 19 formule(s).
sommaire: oui
---

## Chapitre 1 — Présenter pour informer

::: formule Fréquence d'une modalité
$$ f_k = \frac{n_k}{N} $$

- $f_k$ : la **fréquence** de la modalité $x_k$ ;
- $n_k$ : son **effectif** ;
- *N* : l'**effectif total** (la taille de la population).

La fréquence d'une modalité est la **proportion d'individus** qui présentent cette modalité dans la population totale. C'est un nombre entre 0 et 1, qu'on exprime souvent **en pourcentage** (on multiplie par 100).

**Propriétés** : les effectifs s'additionnent pour donner l'effectif total, et les fréquences pour donner 1 :

$$ \sum_{k=1}^{K} n_k = n_1 + n_2 + \dots + n_K = N \qquad \sum_{k=1}^{K} f_k = f_1 + f_2 + \dots + f_K = 1 = 100\ \% $$

**Pourquoi la somme des fréquences vaut 1** : $\sum f_k = \sum \frac{n_k}{N} = \frac{1}{N} \sum n_k = \frac{N}{N} = 1$.
:::

::: formule Fréquence cumulée
$$ F_k = f_1 + f_2 + \dots + f_k = \sum_{i=1}^{k} f_i \qquad \text{d'où} \qquad F_k = F_{k-1} + f_k $$

- $F_k$, qu'on note aussi $F(x_k)$ : la **fréquence cumulée** de la modalité $x_k$ ;
- on l'obtient en ajoutant les fréquences **de la première modalité jusqu'à** $x_k$ ;
- en pratique, **de proche en proche** : chaque fréquence cumulée est la précédente plus la fréquence de la ligne.

La fréquence cumulée d'une modalité est la **proportion d'individus présentant cette modalité ou une modalité inférieure**. Elle n'a de sens que si les modalités **peuvent être rangées** : variable **quantitative** ou **qualitative ordinale** — jamais nominale. La dernière vaut toujours **1 = 100 %**.
:::

## Chapitre 2 — Résumer pour informer

::: formule L'aire d'un rectangle est la fréquence de la classe
$$ \text{Aire} = \text{Base} \times \text{Hauteur} = a \times d = a \times \frac{f}{a} = f $$

- *a* : l'amplitude de la classe (la base du rectangle) ;
- *d* : la densité de la classe (sa hauteur) ;
- *f* : la fréquence de la classe.

**Conséquence** : la **somme des aires vaut 1** (100 %), puisque la somme des fréquences vaut 1 : $\sum_{k=1}^{8} f_k = 1$ (séance 2). **Exemple** : pour la 4ᵉ classe d'âge, aire = 5 × 0,0375 = **0,187** = sa fréquence ; pour la 6ᵉ (40-50 ans), aire = 10 × 1,68 % = **0,168**.
:::

::: formule Moyenne arithmétique sur données brutes
$$ m = \frac{1}{N} \sum_{i=1}^{N} x_i = \frac{1}{N} (x_1 + x_2 + \dots + x_N) $$

- *N* : le nombre d'observations ;
- $x_i$ : la valeur de la $i$-ième observation — **l'indice *i* renvoie au numéro d'observation**, c'est-à-dire à la $i$-ième unité statistique de la base de données.

C'est l'indicateur de tendance centrale le plus connu : on **divise la somme des observations par leur nombre**.
:::

::: formule Moyenne d'une distribution
$$ m = \frac{1}{N} \sum_{i=1}^{p} n_i x_i \qquad \text{ou, de façon équivalente,} \qquad m = \sum_{i=1}^{p} \frac{n_i}{N} x_i = \sum_{i=1}^{p} f_i x_i $$

- *p* : le nombre de **modalités** — ici, **l'indice *i* renvoie au numéro de modalité** ;
- $n_i$ : l'effectif de la modalité $x_i$ ; $f_i = n_i / N$ : sa fréquence.

La première forme part des **effectifs** (formule 4 du cours), la seconde des **fréquences** (formule 5) : on a simplement fait entrer le $\frac{1}{N}$ dans la somme.
:::

::: formule Moyenne par agrégation
$$ m = \sum_{k=1}^{K} \frac{N_k}{N} m_k = \frac{1}{N} \sum_{k=1}^{K} N_k m_k \qquad \text{avec} \qquad N = \sum_{k=1}^{K} N_k $$

- *K* : le nombre de sous-populations **disjointes** ;
- $N_k$ : l'effectif du groupe *k* ; $m_k$ : la moyenne de *X* dans ce groupe.

C'est une **moyenne pondérée** des moyennes de groupe, chacune pesant **la part de son groupe dans la population**, $N_k / N$. Cette part est parfois donnée sous forme de **fréquence** $f_k$.
:::

::: formule Propriété 1 — la somme des écarts à la moyenne est nulle
$$ \sum_{i=1}^{N} (x_i - m) = \sum_{i=1}^{N} x_i - N m = \sum_{i=1}^{N} x_i - N \times \frac{\sum x_i}{N} = 0 $$

*N* fois la moyenne, c'est la somme des observations. Les **écarts positifs et négatifs se compensent exactement** : la moyenne est le **point d'équilibre** de la distribution. C'est pourquoi on ne peut pas mesurer la dispersion par la moyenne des écarts (elle vaut toujours 0) : il faudra des valeurs absolues ou des carrés (section 2.5). Si la distribution est **symétrique**, l'axe de symétrie passe par la moyenne, et **la moyenne égale la médiane**.
:::

::: formule Propriété 2 — la moyenne est linéaire
$$ \text{si } Y = aX + b \text{ alors } m_Y = a\, m_X + b $$

- **multiplier** toutes les valeurs par *a* multiplie la moyenne par *a* (convertir des euros en dollars) ;
- **ajouter** *b* à toutes les valeurs augmente la moyenne de *b* (6 points de bonus pour tous : la moyenne monte de 6) ;
- à plus forte raison, **la moyenne d'une somme de deux variables est la somme de leurs moyennes**.

**Démonstration** : $m_Y = \frac{1}{N} \sum (a x_i + b) = a \times \frac{1}{N} \sum x_i + \frac{1}{N} \times N b = a\, m_X + b$.
:::

::: formule Médiane d'une distribution
**Cas 1** — s'il existe une modalité $x_j$ telle que $F(x_j) = 50$ %, alors **la médiane vaut $x_j$**.

**Cas 2** — sinon, on procède par **interpolation linéaire** entre les deux modalités qui encadrent 50 % : si $F(x_a) < 50$ % et $F(x_b) > 50$ %,

$$ med \approx x_a + \frac{(x_b - x_a)(0,5 - F(x_a))}{F(x_b) - F(x_a)} $$

- $x_a$, $x_b$ : les modalités (ou, pour des classes, les **bornes supérieures** des classes) juste avant et juste après le passage de 50 % ;
- $F(x_a)$, $F(x_b)$ : leurs fréquences cumulées ;
- la fraction $\frac{0,5 - F(x_a)}{F(x_b) - F(x_a)}$ dit **quelle proportion du chemin** de $F(x_a)$ à $F(x_b)$ il faut parcourir pour atteindre 50 % ; on parcourt la **même proportion** du chemin de $x_a$ à $x_b$.
:::

::: formule Quantile d'ordre α par interpolation linéaire
Si une modalité $x_j$ vérifie $F(x_j) = α$, le quantile vaut $x_j$ ; sinon, si $F(x_a) < α < F(x_b)$ :

$$ Q_α \approx x_a + \frac{(x_b - x_a)(α - F(x_a))}{F(x_b) - F(x_a)} $$

C'est la formule de la médiane, avec α à la place de 0,5. **Attention à l'écriture** : au tableau de la séance 3, le facteur $(x_b - x_a)$ est écrit au dénominateur ; il **multiplie** — le résultat était juste parce que $x_b - x_a = 1$.
:::

::: formule Variance à partir d'une distribution
$$ \sigma^2 = \frac{1}{N} \sum_{i=1}^{p} n_i (x_i - m)^2 = \frac{1}{N} \sum_{i=1}^{p} n_i x_i^2 - m^2 $$
$$ \sigma^2 = \sum_{i=1}^{p} f_i (x_i - m)^2 = \sum_{i=1}^{p} f_i x_i^2 - m^2 $$

- *p* modalités, d'effectifs $n_i$ et de fréquences $f_i$ ; **l'indice *i* renvoie au numéro de modalité** ;
- chaque carré d'écart est **pondéré** par l'effectif (ou la fréquence) de sa modalité ;
- la seconde égalité de chaque ligne est la **formule de Koenig** (ci-dessous).
:::

::: formule Formule de Koenig
$$ V(X) = \frac{1}{N} \sum_{i=1}^{N} x_i^2 - m^2 $$

**La variance est la moyenne des carrés moins le carré de la moyenne.** C'est souvent plus rapide à calculer, et c'est l'outil pour **agréger** des variances (section 2.6).
:::

::: formule Changer d'origine ou d'unité
$$ V(a + X) = V(X) \qquad V(aX) = a^2\, V(X) \qquad V(-X) = V(X) $$

- **ajouter le même nombre *a*** à toutes les valeurs **ne change pas la variance** : tous les écarts à la moyenne restent les mêmes ;
- **multiplier** toutes les valeurs par *a* **multiplie la variance par $a^2$** — la variance **n'est pas linéaire** ; l'écart-type, lui, est multiplié par $\lvert a \rvert$ ;
- en corollaire, $V(-X) = (-1)^2 V(X) = V(X)$.
:::

::: formule Coefficient de variation
$$ CV = \frac{\sigma(X)}{m_X} $$

Il est **sans unité** et s'exprime **en pourcentage**. Il permet de comparer la dispersion de variables d'unités ou de niveaux différents : des revenus en dollars et en yens, des poids de naissance et des tailles. Exemple : l'écart-type des âges (7,36 ans) rapporté à leur moyenne (47,9 ans) donne $CV \approx 15,4$ %.
:::

::: formule Inégalité de Bienaymé-Tchebychev
Pour tout $k > 1$, l'intervalle $[m - k\sigma ; m + k\sigma]$ contient **au moins une proportion** $1 - \frac{1}{k^2}$ des observations — donc **au plus** $\frac{1}{k^2}$ des observations sont en dehors.

| *k* | Au moins dans $m \pm k\sigma$ | Au plus en dehors |
|:---:|:---:|:---:|
| 2 | $1 - 1/4 =$ **75 %** | 25 % |
| 3 | $1 - 1/9 \approx$ **89 %** | 11 % |
| 10 | $1 - 1/100 =$ **99 %** | 1 % |

Elle est vraie **pour toute distribution**, quelle que soit sa forme : c'est une **garantie minimale** — en pratique, la proportion réelle est souvent bien plus forte. Irénée-Jules **Bienaymé** et Pafnouti **Tchebychev** l'ont établie au XIXᵉ siècle.
:::

::: formule Variance par agrégation
$K$ groupes d'effectifs $N_k$, de moyennes $m_k$ et de variances $\sigma_k^2$ ; $N = \sum N_k$ et $m = \frac{1}{N} \sum N_k m_k$ :

$$ \sigma^2 = \frac{1}{N} \sum_{k=1}^{K} N_k \left( \sigma_k^2 + m_k^2 \right) - m^2 $$
:::

::: formule Variance totale = variance intra-groupe + variance inter-groupe
$$ \sigma^2 = V_{intra} + V_{inter} $$
$$ V_{intra} = \sum_{k=1}^{K} \frac{N_k}{N} \sigma_k^2 \qquad V_{inter} = \sum_{k=1}^{K} \frac{N_k}{N} (m_k - m)^2 = \sum_{k=1}^{K} \frac{N_k}{N} m_k^2 - m^2 $$

- la **variance intra-groupe** est la **moyenne pondérée des variances des groupes** : la dispersion **à l'intérieur** des groupes ;
- la **variance inter-groupe** est la **variance des moyennes des groupes** autour de la moyenne générale : la dispersion **entre** les groupes.

**Attention, erreur du support** : la diapositive 58 écrit $V_{intra} = \sum \frac{N_k}{N} \sigma_k$ — **sans le carré**. C'est bien la moyenne des **variances** $\sigma_k^2$, comme au tableau de la séance 4.
:::

::: formule Part de l'agrégat d'une classe
$$ \text{somme de } X \text{ dans la classe } k = \sum_{i \in k} x_i = N_k\, m_k \qquad \text{part de la classe } k = \frac{N_k\, m_k}{\sum_{j} N_j\, m_j} $$

Pour des salaires, la somme s'appelle la **masse salariale** : **salaire moyen de la classe × effectif de la classe**. Si l'on ne connaît que les **proportions** de la population, on peut poser l'effectif total égal à 1 : dans le calcul des parts, *N* disparaît.
:::

::: formule Calcul de l'indice de Gini par les trapèzes
$$ G = 2 \left[ \frac{1}{2} - \sum \frac{(b + B)\, h}{2} \right] = 1 - \sum (b + B)\, h $$

- $\frac{1}{2}$ : l'aire sous la diagonale ;
- sous la courbe de Lorenz, l'aire se découpe en **trapèzes**, un par classe : $b$ et $B$ sont les parts cumulées **au début et à la fin** de la classe (la petite et la grande base), $h$ est la **part de la population de la classe** (la hauteur, en proportion) ;
- aire de concentration $= \frac{1}{2} - \sum$ aires des trapèzes ; Gini = 2 × aire de concentration.
:::
