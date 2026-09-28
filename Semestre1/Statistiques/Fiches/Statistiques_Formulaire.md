---
matiere: Techniques statistiques
titre: Formulaire cumulatif — Techniques statistiques
sous_titre: Toutes les formules de tous les chapitres, dans l'ordre du cours
resume: Généré automatiquement à partir des encadrés « formule » des cours. 4 formule(s).
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
