---
matiere: Nom complet de la matière
code: Dossier de la matière (Economie, Gestion, Statistiques, Institutions_politiques, Droit, Mathematiques…)
chapitre: Chapitre N — Titre court
titre: Titre du chapitre
sous_titre: Ce que le chapitre apprend à faire, en une ligne
resume: Sources utilisées, nombre d'éléments couverts, ce que le document ajoute au support.
date: jour mois année
duree: Apprentissage — k sections × 4 pomodoros · révisions J+1, J+3, J+7, J+21
version: 3.0
sommaire: oui
---

# Modèle de cours reconstruit — structure obligatoire

*Cette page d'introduction ne figure pas dans un vrai cours. Tout le reste en est le squelette :
titres identiques, dans le même ordre — `verifier.py` refuse un cours auquel il en manque un,
et `extraire.py` s'en sert pour produire la fiche, les cartes Anki, le formulaire et le glossaire.*

| Section | Ce qu'elle contient | Protocole de la charte |
|---|---|---|
| **1 — Carte du chapitre** | Vue d'ensemble en 10 lignes · idées maîtresses · prérequis · lien finance · ce qui servira au TAGE MAGE | Lue au premier pomodoro |
| **2 — Le cours reconstruit** | Tout le contenu, ordre pédagogique. **Chaque `## 2.k` est une section d'apprentissage** : un cycle APPRENDRE P1 → P4, soit 25 min de lecture active | APPRENDRE |
| **3 — Points de vigilance** | Confusions, erreurs fréquentes, copie moyenne contre copie à 18-20 | Relu avant chaque examen blanc |
| **4 — Ancrage mémoriel** | 4.1 fiche d'une page · 4.2 cartes · 4.3 moyens mnémotechniques · 4.4 schéma qui relie tout | RÉVISER |
| **5 — Entraînement** | Niveau 1 questions de cours · Niveau 2 exercices types · Niveau 3 réflexion et pièges · Niveau 4 sujet au format réel, barème, copie de major | P4 d'APPRENDRE puis S'ENTRAÎNER |
| **6 — Auto-évaluation** | « Si tu ne sais pas répondre sans regarder, tu ne maîtrises pas le chapitre » | Fin de J+7 |
| **7 — Révision en marchant** | Questions orales courtes, réponse attendue en une phrase | Hors pomodoros |
| **Annexe A — Glossaire du chapitre** | Tableau Terme · En une phrase · Définition académique → GLOSSAIRE.md | — |
| **Annexe B — Tableau de couverture** | Une ligne par diapositive/page du support, ✔ / ⚠ / ✖, sans trou → contrôle qualité | — |

<!--saut-->

# 1 — Carte du chapitre

::: synthese Le chapitre en dix lignes
Dix lignes au plus : la question que pose le chapitre, la réponse qu'il construit, les étapes.
:::

**Les idées maîtresses à retenir absolument**

1. …

**Prérequis** — ce qu'il faut savoir avant, et où c'est enseigné (dans ce document si absent ailleurs).

::: marche Le lien avec la finance
Seulement quand il est réel.
:::

**Pour plus tard** — notions utiles au TAGE MAGE (calcul, logique) ou à la culture financière.

# 2 — Le cours reconstruit

## 2.1 — Première section d'apprentissage

**À quoi ça sert, d'où ça vient, quel problème ça résout** — toujours en tête de concept.

::: definition Terme
**En une phrase :** la version simple.
**Définition académique :** la version rigoureuse, celle qu'on recopie en copie.
:::

::: formule Nom de la formule
$$ f_i = \frac{n_i}{n} $$
Chaque terme expliqué. Puis démonstration (`::: demo`) et exemple chiffré complet (`::: exemple`).
:::

![Légende du graphique, à savoir reproduire](figures/chapitre/graphe.svg)

::: piege Ce qui piège
:::

::: examen Ce qui tombe
:::

# 3 — Points de vigilance

# 4 — Ancrage mémoriel

## 4.1 — Fiche de synthèse

Une page imprimée, pas plus. Extraite telle quelle dans `Fiches/`.

## 4.2 — Cartes de révision

::: carte
Question ?
--
Réponse.
:::

## 4.3 — Moyens mnémotechniques

## 4.4 — Le schéma qui relie tout

# 5 — Entraînement

## Niveau 1 — Questions de cours

## Niveau 2 — Exercices types d'examen

## Niveau 3 — Réflexion, cas transversaux, questions pièges

## Niveau 4 — Sujet au format de l'examen

# 6 — Auto-évaluation

# 7 — Révision en marchant

1. **Question ?** → réponse attendue en une phrase.

# Annexe A — Glossaire du chapitre

| Terme | En une phrase | Définition académique |
|---|---|---|
| Terme | … | … |

# Annexe B — Tableau de couverture du support

| № | Élément du support | État | Où c'est traité |
|:---:|---|:---:|---|
| **1** | … | **✔** | § 2.1 |

<!--saut-->

# Référence de syntaxe

| Élément | Écriture |
|---|---|
| Titres | `#` `##` `###` `####` — `##` et `###` alimentent le sommaire |
| Emphase | `**gras**`, `*italique*`, `==surligné==`, code entre accents graves |
| Listes | `-` à puces, `1.` numérotées, imbrication par deux espaces |
| Tableau | `\| a \| b \|` puis `\|---\|---:\|` — jamais d'en-tête vide |
| Saut de page | `<!--saut-->` |
| Maths en ligne | `$ f_i = n_i / n $` — **toujours sur une seule ligne** |
| Maths centrées | `$$ ... $$` sur leurs propres lignes |
| Figure | `![légende](figures/<chapitre>/<nom>.svg)` sur sa propre ligne |
| Encadré | `::: type Titre` … `:::` — types : `definition` `formule` `demo` `exemple` `piege` `examen` `methode` `correction` `marche` `synthese` `objectif` `carte` |
| Carte | `::: carte` · question · `--` · réponse · `:::` |

Commandes LaTeX reconnues : `\frac` `\dfrac` `\sqrt` `\text` `\bar` `\overline` `\hat` `\vec`,
exposants, indices, alphabet grec, `\times` `\cdot` `\le` `\ge` `\ne` `\approx` `\sum` `\prod`
`\int` `\partial` `\infty` `\rightarrow` `\Rightarrow` `\Leftrightarrow` `\in` …

Publication : `Semestre1/outils/publier.sh <fichier.md>`.
