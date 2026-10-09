# Évaluation finale (exploratoire) et Monte-Carlo

Candidat de simulation : `S1|F=True,k=5.0,s=2.5,t=3.0` — **NON VALIDÉE. Sur 2011-2021, aucune famille n'a satisfait les critères pré-enregistrés : espérance walk-forward S1 +0.081 R par trade (IC95 -0.019 ; +0.183), non distinguable de zéro après correction des tests multiples, et négative si les coûts doublent. Le système fonctionne en SIMULATION uniquement ; le passage au réel exige une validation prospective.**

## 2022-01-01 → 2025-10-28 (exploratoire, non confirmatoire)

| Coûts | n | espérance R | PF | taux de gain | drawdown max R |
|---|---|---|---|---|---|
| base | 327 | +0.061 | +1.15 | +0.35 | -15.3 |
| couts_x2 | 327 | +0.020 | +1.05 | +0.35 | -17.1 |
| couts_fixes | 327 | +0.025 | +1.06 | +0.35 | -17.4 |

IC95 de l'espérance (base) : [-0.076 ; +0.207] ; borne unilatérale basse -0.055

Par année :

- 2022 : n=74, espérance +0.102 R
- 2023 : n=101, espérance +0.101 R
- 2024 : n=83, espérance -0.029 R
- 2025 : n=69, espérance +0.067 R

Contrôle de résolution (2025-02-13 20:30:00+00:00 → 2025-10-28 14:20:00+00:00) : barres 15 min n=55, espérance +0.125 R ; exécution 5 min n=55, espérance +0.126 R

## Monte-Carlo Flex 50K (challenge, 120 jours, trades walk-forward 2014-2021, or à 4 000 $)

| Risque/trade | P(réussite) | P(violation) | P(en cours) | jours médians | objectif relevé | trades moyens |
|---|---|---|---|---|---|---|
| 75 $ | 0.0% | 0.0% | 100.0% | 107.0 | 0.0% | 8 |
| 100 $ | 0.2% | 0.0% | 99.8% | 106.0 | 0.0% | 26 |
| 125 $ | 1.2% | 0.0% | 98.8% | 98.0 | 0.0% | 36 |
| 150 $ | 3.3% | 0.0% | 96.7% | 95.5 | 0.0% | 39 |
| 200 $ | 8.3% | 0.0% | 91.6% | 85.0 | 9.4% | 37 |
| 250 $ | 10.7% | 0.0% | 89.3% | 77.0 | 19.0% | 36 |

Même chose avec les trades 2022-2025 (exploratoire) :

| Risque/trade | P(réussite) | P(violation) |
|---|---|---|
| 75 $ | 0.0% | 0.0% |
| 100 $ | 0.0% | 0.0% |
| 125 $ | 0.1% | 0.0% |
| 150 $ | 0.9% | 0.0% |
| 200 $ | 3.8% | 0.0% |
| 250 $ | 6.7% | 0.0% |

Profil retenu : **250 $ par trade** (P(réussite) maximale sous P(violation) ≤ 20 % (trades walk-forward)).
Compte financé (252 jours) : survie {'21': 1.0, '63': 1.0, '126': 1.0, '252': 1.0}, probabilité d'au moins un retrait 56.3%, retraits moyens 627 $.
Seuils de suspension automatique : drawdown ≤ -27.27 R ou série de 17 pertes.