# Compléments de recherche

> **complément a posteriori (non pré-enregistré, ne change pas le verdict).** Calculés après coup ; ils ne servent ni à choisir ni à modifier la stratégie.

Candidat : `S1|F=True,k=5.0,s=2.5,t=3.0`, coûts de base. Risque par trade pour les montants : 250 $ (profil par défaut, `production.json`), 1 R = ce risque exactement (arrondi au contrat entier ignoré).

## A. Métriques complémentaires (§ 4)

| Période | n | espérance R | espérance $ | IC95 $ | drawdown max R | durée max DD (j) | durée médiane DD (j) | nb DD | DD en cours à la fin |
|---|---|---|---|---|---|---|---|---|---|
| walk_forward_2014_2021 | 790 | +0.081 | +20.19 | [-4.82 ; +45.85] | -19.2 | 424 | 25 | 26 | oui (37 j) |
| exploratoire_2022_2025 | 327 | +0.061 | +15.23 | [-18.95 ; +51.81] | -15.3 | 232 | 13 | 14 | oui (23 j) |

Durée d'un drawdown = jours de trading passés sous le précédent sommet d'équité (journées sans trade comprises).

**walk_forward_2014_2021 — par séance (heure d'entrée, New York)**

| Groupe | n | espérance R | espérance $ | taux de gain |
|---|---|---|---|---|
| Londres | 353 | +0.068 | +16.88 | 34% |
| New York après-midi | 26 | -0.266 | -66.53 | 35% |
| New York matin | 411 | +0.114 | +28.52 | 40% |

**walk_forward_2014_2021 — par régime de volatilité**

| Groupe | n | espérance R | espérance $ | taux de gain |
|---|---|---|---|---|
| faible | 427 | +0.166 | +41.55 | 40% |
| forte | 131 | -0.030 | -7.58 | 35% |
| moyenne | 232 | -0.014 | -3.45 | 34% |

**exploratoire_2022_2025 — par séance (heure d'entrée, New York)**

| Groupe | n | espérance R | espérance $ | taux de gain |
|---|---|---|---|---|
| Londres | 129 | -0.025 | -6.15 | 29% |
| New York après-midi | 17 | -0.099 | -24.78 | 35% |
| New York matin | 181 | +0.137 | +34.22 | 40% |

**exploratoire_2022_2025 — par régime de volatilité**

| Groupe | n | espérance R | espérance $ | taux de gain |
|---|---|---|---|---|
| faible | 125 | +0.233 | +58.15 | 41% |
| forte | 88 | +0.044 | +11.02 | 36% |
| moyenne | 114 | -0.114 | -28.60 | 29% |

Régime : tercile de la moyenne sur 20 journées de l'amplitude relative (H−L)/C, connue la veille, parmi les 250 journées précédentes (calcul causal).

## B. Délai d'exécution manuelle (§ 3.7)

Période : 2025-02-13 20:30:00+00:00 → 2025-10-28 14:20:00+00:00 ; exécution sur barres de 5 minutes. 1 et 3 min tombent à l'intérieur d'une barre de 5 min : prix d'entrée inconnu, encadré par une estimation interpolée (ouverture → clôture) et une borne prudente (extrême défavorable de la barre). 0 et 5 min : ouverture exacte d'une barre de 5 min.

| Délai | Prix d'entrée | n | espérance R | IC95 R | drawdown max R | glissement d'entrée moyen ($/oz) |
|---|---|---|---|---|---|---|
| 0 min | exact | 55 | +0.126 | [-0.142 ; +0.393] | -5.4 | +0.037 |
| 1 min | interpole | 55 | +0.107 | [-0.151 ; +0.373] | -5.5 | +0.270 |
| 1 min | pire | 55 | -0.202 | [-0.453 ; +0.066] | -15.4 | +3.792 |
| 3 min | interpole | 55 | +0.068 | [-0.179 ; +0.334] | -5.7 | +0.736 |
| 3 min | pire | 55 | -0.202 | [-0.453 ; +0.066] | -15.4 | +3.792 |
| 5 min | exact | 55 | +0.045 | [-0.195 ; +0.301] | -6.1 | +1.215 |

## C. Combinaisons d'unités de temps (§ 5) — 2011-2021 uniquement

| Variante | entraînement 2011-18 : n / espérance R | validation 2019-21 : n / espérance R / PF | total 2011-21 : espérance R [IC95] |
|---|---|---|---|
| décision 15 min + filtre de volatilité journalière (configuration de production) | 684 / +0.142 | 264 / +0.030 / 1.06 | +0.111 [+0.021 ; +0.205] |
| décision 15 min, sans contexte journalier | 992 / +0.086 | 378 / +0.003 / 1.01 | +0.063 [-0.011 ; +0.137] |
| décision 15 min + filtre journalier + contexte de tendance 1 h (EMA 20) | 657 / +0.105 | 263 / +0.034 / 1.07 | +0.084 [-0.005 ; +0.177] |
| décision 30 min (mêmes paramètres en nombre de barres) + filtre journalier | 360 / +0.179 | 131 / +0.138 / 1.42 | +0.168 [+0.067 ; +0.269] |

Aucune variante n'est adoptée : la production reste inchangée (pas de modification silencieuse, § 17).