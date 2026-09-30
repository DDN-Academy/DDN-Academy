---
matiere: Techniques statistiques
chapitre: Chapitre 2 — Résumer pour informer
titre: Fiche — Résumer pour informer — position, dispersion et concentration d'une distribution
sous_titre: La page à savoir par cœur, puis les questions à se poser en marchant
resume: Extraite automatiquement du cours Statistiques_Ch02_Resumer_pour_informer.md. Ne pas modifier ici : corriger le cours, puis republier.
date: 30 septembre 2026
sommaire: non
---

# La fiche de synthèse

| | L'essentiel à savoir par cœur |
|---|---|
| **Mode** | La modalité la plus fréquente · en classes : **densité** $d = f / a$, **classe modale** = plus forte densité · **histogramme** : bornes en abscisse, densité en ordonnée, **aire = fréquence**, somme des aires = 1 |
| **Moyenne** | Brutes $\frac{1}{N} \sum x_i$ · distribution $\frac{1}{N} \sum n_i x_i = \sum f_i x_i$ · classes : centres · groupes $\sum \frac{N_k}{N} m_k$ (démo : $\sum_{i \in k} x_i = N_k m_k$) · $\sum x_i = N m$ (masse salariale) · $\sum (x_i - m) = 0$ · $m_{aX+b} = a m_X + b$ · sensible aux extrêmes |
| **Médiane** | Coupe la population en deux moitiés · brutes : trier, rang $(N + 1)/2$, ou moyenne des deux rangs centraux · distribution : $F(x_j) = 50$ % → $x_j$ ; sinon interpolation $x_a + (x_b - x_a) \frac{0,5 - F(x_a)}{F(x_b) - F(x_a)}$ · non linéaire, non agrégeable, robuste · étalée à droite : méd < moy |
| **Quantiles** | $Q_1, Q_3$ ; $D_1 \dots D_9$ ; $C_1 \dots C_{99}$ · $F(q) = α$, $q = F^{-1}(α)$ · même interpolation avec α |
| **Dispersion (quantiles)** | Étendue max − min · $C_{99} - C_1$, $D_9 - D_1$ (80 % centraux), $Q_3 - Q_1$ (50 % centraux), rapports $D_9 / D_1$ · boîte à moustaches : médiane, $Q_1$-$Q_3$, moustaches ($D_1$-$D_9$ ou 1,5 × IQR) |
| **Variance** | $EAM = \frac{1}{N} \sum \lvert x_i - m \rvert$ · $\sigma^2 = \frac{1}{N} \sum (x_i - m)^2 = \frac{1}{N} \sum x_i^2 - m^2$ (Koenig) · distribution : $\sum f_i (x_i - m)^2$ · $\sigma = \sqrt{\sigma^2}$ · $V(a + X) = V(X)$, $V(aX) = a^2 V(X)$ · $CV = \sigma / m$ sans unité |
| **Tchebychev** | $m \pm k\sigma$ contient au moins $1 - 1/k^2$ : 75 % (k = 2), 89 % (k = 3), 99 % (k = 10) · symétrique : au plus $1/(2k^2)$ de chaque côté · finance : σ = volatilité |
| **Groupes** | $\sigma^2 = \frac{1}{N} \sum N_k (\sigma_k^2 + m_k^2) - m^2$ · $V_{intra} = \sum \frac{N_k}{N} \sigma_k^2$ · $V_{inter} = \sum \frac{N_k}{N} (m_k - m)^2$ · total = intra + inter |
| **Concentration** | Répartition de la **somme** (revenus oui, tailles non) · part $= N_k m_k / \sum N_j m_j$ · **Lorenz** : part cumulée du total selon part cumulée de la population ; diagonale = égalité · **Gini** $= 2 \times$ aire de concentration $= 1 - \sum (b + B) h$ ; 0 égalité, 1 concentration maximale |

<!--saut-->

# Révision en marchant

1. **Les trois questions du chapitre ?** → Où se situe la série ? Comment les données se répartissent-elles ? Comment la somme se répartit-elle ?
2. **Le mode ?** → La modalité la plus fréquente.
3. **L'amplitude d'une classe ?** → La borne supérieure moins la borne inférieure.
4. **La densité d'une classe ?** → Sa fréquence divisée par son amplitude.
5. **La classe modale ?** → La classe de plus forte densité, pas de plus fort effectif.
6. **La classe modale des personnes incarcérées en 2020 ?** → De 25 à moins de 30 ans.
7. **En ordonnée d'un histogramme ?** → La densité.
8. **Où se lit la fréquence dans un histogramme ?** → Dans l'aire du rectangle.
9. **La somme des aires d'un histogramme ?** → 1, soit 100 %.
10. **La moyenne sur données brutes ?** → La somme des valeurs divisée par N.
11. **La moyenne d'une distribution ?** → La somme des effectifs fois les modalités, divisée par N ; ou la somme des fréquences fois les modalités.
12. **Une classe, dans le calcul de la moyenne ?** → On la remplace par son centre.
13. **La moyenne de plusieurs groupes ?** → Les moyennes des groupes, pondérées par la part de chaque groupe.
14. **330 élèves à 12 et 270 élèves à 10 ?** → 11,1, et non 11.
15. **La somme d'une variable ?** → L'effectif fois la moyenne.
16. **La somme des écarts à la moyenne ?** → Zéro.
17. **Si Y = aX + b ?** → La moyenne de Y vaut a fois celle de X, plus b.
18. **Une distribution étalée à droite ?** → Médiane inférieure à la moyenne.
19. **La médiane ?** → La valeur qui coupe la population en deux moitiés.
20. **La médiane de N valeurs, N impair ?** → La valeur de rang (N + 1)/2.
21. **Et si N est pair ?** → La moyenne des deux valeurs centrales.
22. **La médiane s'agrège-t-elle ?** → Non : elle n'est pas linéaire.
23. **Si une fréquence cumulée vaut exactement 50 % ?** → La médiane est cette modalité.
24. **Sinon ?** → Interpolation linéaire : la même proportion du chemin.
25. **Pour des classes, les deux valeurs de l'interpolation ?** → Les bornes supérieures des classes.
26. **Le quantile d'ordre α ?** → La valeur sous laquelle se trouve une part α de la population.
27. **Le troisième quartile ?** → Le quantile d'ordre 75 %.
28. **Le premier décile du niveau de vie en 2024 ?** → 13 970 € : 10 % des personnes vivent avec moins.
29. **L'étendue ?** → Le maximum moins le minimum.
30. **L'écart inter-déciles ?** → L'amplitude des 80 % centraux.
31. **L'écart inter-quartile ?** → L'amplitude des 50 % centraux.
32. **Un rapport D9 sur D1 de 3,2 chez les cadres ?** → Les 10 % les mieux payés gagnent au moins 3,2 fois plus que les 10 % les moins bien payés.
33. **La boîte à moustaches ?** → La médiane au centre, Q1 et Q3 aux bords, les moustaches au-delà.
34. **L'écart absolu moyen ?** → La moyenne des écarts à la moyenne, en valeur absolue.
35. **La variance ?** → La moyenne des carrés des écarts à la moyenne.
36. **Koenig ?** → La moyenne des carrés moins le carré de la moyenne.
37. **L'unité de la variance ?** → L'unité de la variable, au carré.
38. **L'écart-type ?** → La racine de la variance, dans l'unité de la variable.
39. **Ajouter le même nombre à toutes les valeurs ?** → La variance ne change pas.
40. **Multiplier toutes les valeurs par a ?** → La variance est multipliée par a au carré.
41. **Le coefficient de variation ?** → L'écart-type divisé par la moyenne, sans unité.
42. **Bienaymé-Tchebychev avec k = 2 ?** → Au moins 75 % des observations dans m ± 2σ.
43. **Avec k = 3 ?** → Au moins 89 %.
44. **Avec k = 10 ?** → Au moins 99 %.
45. **La variance du cas n° 4 ?** → 20,8, et non 10,4.
46. **La volatilité ?** → L'écart-type des rentabilités : le risque.
47. **La variance de plusieurs groupes ?** → La moyenne pondérée des (variance + moyenne au carré) des groupes, moins le carré de la moyenne.
48. **La variance intra-groupe ?** → La moyenne pondérée des variances des groupes.
49. **La variance inter-groupe ?** → La variance des moyennes des groupes.
50. **Dispersion ou concentration ?** → La répartition des observations, ou celle de la somme.
51. **La courbe de Lorenz ?** → La part cumulée du total en fonction de la part cumulée de la population.
52. **La diagonale du graphique de Lorenz ?** → L'égalité parfaite.
53. **L'indice de Gini ?** → Deux fois l'aire de concentration : 1 moins la somme des (b + B) × h.
54. **Le Gini des salaires en 2005 et en 2021 ?** → 0,25 puis 0,36 : les inégalités ont augmenté.
