---
matiere: Techniques statistiques
chapitre: Chapitre 2 — Résumer pour informer
titre: Fiche — Résumer pour informer
sous_titre: La page à savoir par cœur, puis les questions à se poser en marchant
resume: Extraite automatiquement du cours Statistiques_Ch02_Resumer_pour_informer.md. Ne pas modifier ici : corriger le cours, puis republier.
date: 28 septembre 2026
sommaire: non
---

# La fiche de synthèse

::: synthese Chapitre 2 « Résumer pour informer » — l'essentiel sur deux pages
**LE PROJET DU CHAPITRE.** Présenter (chapitre 1) conserve **toute** l'information. Résumer
en **perd volontairement** pour produire quelques chiffres décisionnels. Trois familles :
**position** (où ?), **dispersion** (à quel point c'est étalé ?), **concentration** (comment
le total se partage-t-il ?).

**① POSITION — LE MODE.** La modalité de **fréquence maximale**. Variable continue → **classe
modale**. ⚠ Si les amplitudes sont **inégales**, la classe modale est celle de **densité
maximale** : $ d_i = f_i / a_i $ avec $ a_i = b_{sup} - b_{inf} $. **Histogramme :** hauteur =
densité, et **c'est l'aire qui représente la fréquence** ($ d_i \times a_i = f_i $).

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
**Boxplot** : boîte de $ Q_1 $ à $ Q_3 $, trait à la médiane, moustaches selon une convention à préciser
(1,5 × IQR, D1 et D9…).

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

<!--saut-->

<!--saut-->

# Révision en marchant

> Hors pomodoros. Question à voix haute, réponse en une phrase, puis vérification. Une réponse
> hésitante revient le lendemain.

1. **Présenter ou résumer ?** → Présenter garde tout ; résumer perd volontairement pour décider.
2. **Les trois familles ?** → Position, dispersion, concentration : où, comment étalé, à qui le total.
3. **Le mode ?** → La modalité la plus fréquente — le seul indicateur de position d'une nominale.
4. **La classe modale, classes inégales ?** → Celle de plus forte densité, pas de plus gros effectif.
5. **La densité ?** → La fréquence divisée par l'amplitude.
6. **L'aire d'un rectangle d'histogramme ?** → La fréquence de la classe ; la somme des aires vaut un.
7. **Classe modale des incarcérés en 2020 ?** → 25 à 30 ans, densité 0,0375.
8. **Les trois écritures de la moyenne ?** → Données brutes, distribution, agrégation.
9. **La somme des écarts à la moyenne ?** → Zéro — d'où la valeur absolue ou le carré.
10. **La moyenne est-elle linéaire ?** → Oui : moyenne de aX plus b égale a fois m plus b.
11. **Moyenne de moyennes ?** → Seulement pondérée par les effectifs des groupes.
12. **Somme, moyenne, effectif ?** → La somme égale l'effectif fois la moyenne.
13. **Moyenne ou médiane face aux extrêmes ?** → La moyenne bouge, la médiane résiste.
14. **La médiane s'agrège-t-elle ?** → Jamais : 1-2-3 et 100-200-300 donnent 51,5, pas 101.
15. **L'hypothèse de l'interpolation ?** → Une répartition uniforme dans l'intervalle.
16. **Médiane des familles en 2008 ?** → 0,09 par la formule, 1 enfant au sens du rang : le dire.
17. **Médiane moins que moyenne ?** → Distribution étalée à droite.
18. **Un quantile ?** → L'inverse de la fonction de répartition.
19. **Q3 moins Q1 ?** → L'étalement des 50 % centraux.
20. **D9 sur D1, niveau de vie 2024 ?** → 3,48.
21. **UC ?** → Unité de consommation : 1, puis 0,5, puis 0,3.
22. **Les moustaches d'un boxplot ?** → Une convention à préciser : 1,5 fois l'écart interquartile, ou D1 et D9.
23. **CSP la plus dispersée ?** → Les cadres, D9 sur D1 égal à 3,2.
24. **Variance ou écart-type ?** → La variance est au carré ; l'écart-type est dans l'unité.
25. **Écart-type des 20 âges ?** → 7,36 ans, que le support ne calcule pas.
26. **EAM ou écart-type, lequel est le plus grand ?** → L'écart-type, toujours.
27. **Bienaymé-Tchebychev à deux écarts-types ?** → Au moins 75 %, quelle que soit la loi.
28. **L'écart-type en finance ?** → La volatilité.
29. **Koenig ?** → La moyenne des carrés moins le carré de la moyenne.
30. **Ajouter une constante ?** → La variance ne bouge pas.
31. **Multiplier par a ?** → Variance fois a au carré, écart-type fois valeur absolue de a.
32. **Le coefficient de variation ?** → Écart-type sur moyenne, sans unité.
33. **Variance du cas 4 ?** → 20,8, et non 10,4 comme le support.
34. **Intra et inter ?** → Dans les groupes, entre les groupes ; leur somme fait la variance.
35. **Concentration, condition ?** → Que la somme de la variable ait un sens.
36. **La part de l'agrégat ?** → Fréquence fois moyenne de classe sur moyenne générale.
37. **Pourquoi N disparaît ?** → Il est au numérateur et au dénominateur.
38. **Part du premier quintile, 2005 puis 2021 ?** → 11,2 %, puis 3,9 %.
39. **La courbe de Lorenz ?** → La part cumulée du total contre la part cumulée de la population, rangée par ordre croissant.
40. **La pente de Lorenz ?** → La moyenne de la classe sur la moyenne générale.
41. **Deux courbes qui se croisent ?** → Les indicateurs peuvent se contredire.
42. **Le Gini ?** → Deux fois l'aire entre la diagonale et la courbe.
43. **Cumuls en pour cent ?** → Diviser la somme des trapèzes par 10 000.
44. **Gini des salaires 2005, 2021 ?** → 0,247 puis 0,356.
45. **La dernière phrase du chapitre ?** → Le choix dépend du type de données et de ce qu'on veut en faire.

<!--saut-->
