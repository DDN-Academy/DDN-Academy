---
matiere: Nom complet de la matière
code: Dossier de la matière (Economie, Gestion, Statistiques, Institutions_politiques, Droit, Mathematiques…)
chapitre: Chapitre N — Titre court
titre: Titre du chapitre
sous_titre: Ce que le chapitre apprend à faire, en une ligne
resume: Sources utilisées, ce que le document corrige et ajoute au support.
date: jour mois année
duree: Apprendre — k sections × 4 pomodoros · réviser — J+1, J+3, J+7, J+21 · s'entraîner — n pomodoros
version: 1.0
sommaire: oui
---

# Modèle de cours reconstruit — structure obligatoire (Livrable 3 de la charte)

*Cette page d'introduction ne figure pas dans un vrai cours. Tout le reste en est le squelette :
titres identiques, dans le même ordre — `verifier.py` refuse un cours auquel il en manque un,
et `extraire.py` s'en sert pour produire la fiche, le formulaire et le glossaire.*

*Décision 13 (30 septembre 2026, demande de l'étudiant) : **plus de cartes Anki**. Chaque cours
contient un test directement dans le document — un QCM et des questions type examen, selon la
matière — et **tous les corrigés sont regroupés à la fin**, dans la partie « Corrigés », qui
commence sur une nouvelle page : l'étudiant se teste sans voir les réponses, puis les regarde.
Les trois premiers cours d'Institutions politiques gardent leur format d'origine (avec cartes).*

| Section | Ce qu'elle contient (charte, Livrable 3) | Protocole de la charte |
|---|---|---|
| **1 — Carte du chapitre** | Vue d'ensemble en quelques lignes · ce qui tombe à l'examen · ce qu'il faut savoir par cœur | Lue au premier pomodoro |
| **2 — Le cours reconstruit** | Tout le contenu évaluable, dans l'ordre le plus logique pour comprendre et retenir. **Chaque `## 2.k` est une section d'apprentissage** : un cycle APPRENDRE de 4 pomodoros — sa lecture active tient en 25 minutes | APPRENDRE : P1 lecture active → P2 restitution de mémoire → P3 QCM de la section → P4 exercices de la section |
| **3 — Pièges et points bonus** | Confusions classiques, erreurs fréquentes, et ce que les correcteurs récompensent pour passer d'une bonne note à 18-20 | Relu avant chaque entraînement de niveau 3 et 4 |
| **4 — Ancrage mémoriel** | 4.1 fiche de synthèse d'une page · 4.2 moyens mnémotechniques · 4.3 schéma reliant les concepts | RÉVISER |
| **5 — Teste-toi** | Sans corrigé sous les questions. Niveau 1 **QCM** (chaque question renvoie à sa section `§ 2.k`) · Niveau 2 exercices types d'examen · Niveau 3 questions pièges et cas transversaux · Niveau 4 sujet au format réel, avec barème | P3-P4 d'APPRENDRE, RÉVISER, S'ENTRAÎNER |
| **6 — Auto-évaluation** | « Si tu ne sais pas répondre à ces questions sans regarder, tu ne maîtrises pas encore le chapitre » | Fin de la révision J+7 |
| **7 — Révision en marchant** | Questions orales courtes, réponse attendue en une phrase | Hors pomodoros |
| **Annexe A — Glossaire du chapitre** | Tableau Terme · En une phrase · Définition académique → GLOSSAIRE.md | — |
| **Annexe B — Tableau de couverture** | Une ligne par élément des sources (diapositive, page, notes), ✔ / ⚠ / ✖, sans trou → contrôle qualité | — |
| **Corrigés** | Dernière partie, sur une nouvelle page (`<!--saut-->` juste avant) : réponses du QCM expliquées, corrigés étape par étape des exercices, corrigé type copie de major du sujet de niveau 4 | Après chaque test |

**Règles d'écriture (charte).** Chaque terme technique défini à sa première apparition, d'abord
simplement, puis dans la formulation exacte attendue à l'examen. Chaque formule énoncée, expliquée
terme par terme, justifiée, illustrée par un exemple chiffré. Chaque raisonnement décomposé. Les
schémas à savoir reproduire sont dessinés et commentés. Aucune digression, aucun « pour aller plus
loin » hors examen ; une analogie avec les marchés seulement si elle accélère la compréhension ou
la mémorisation. Tout point incertain est signalé, à vérifier en TD.

<!--saut-->

# 1 — Carte du chapitre

::: synthese Le chapitre en quelques lignes
La question que pose le chapitre, la réponse qu'il construit, ses étapes.
:::

**Ce qui tombe à l'examen** — …

**Ce qu'il faut savoir par cœur** — …

# 2 — Le cours reconstruit

## 2.1 — Première section d'apprentissage

**À quoi ça sert, quel problème ça résout** — toujours en tête de concept.

::: definition Terme
**En une phrase :** la version simple.
**Définition à connaître :** la version rigoureuse, celle qu'on écrit sur la copie.
:::

::: formule Nom de la formule
$$ f_i = \frac{n_i}{n} $$
Chaque terme expliqué. Puis démonstration (`::: demo`) et exemple chiffré complet (`::: exemple`).
:::

![Légende du schéma, à savoir reproduire](figures/chapitre/schema.svg)

::: piege Ce qui piège
:::

::: examen Ce qui tombe
:::

# 3 — Pièges et points bonus

# 4 — Ancrage mémoriel

## 4.1 — Fiche de synthèse

Une page imprimée, pas plus. Extraite telle quelle dans `Fiches/`.

## 4.2 — Moyens mnémotechniques

## 4.3 — Le schéma qui relie tout

# 5 — Teste-toi

*Sur une feuille, sans regarder le cours ; le corrigé est à la fin du document.*

## Niveau 1 — QCM

**1.** Question ? *(§ 2.1)*

- **a)** proposition
- **b)** proposition
- **c)** proposition
- **d)** proposition

## Niveau 2 — Exercices types d'examen

## Niveau 3 — Questions pièges et cas transversaux

## Niveau 4 — Sujet au format de l'examen

# 6 — Auto-évaluation

# 7 — Révision en marchant

1. **Question ?** → réponse attendue en une phrase.

# Annexe A — Glossaire du chapitre

| Terme | En une phrase | Définition académique |
|---|---|---|
| Terme | … | … |

# Annexe B — Tableau de couverture des sources

| № | Élément des sources | État | Où c'est traité |
|:---:|---|:---:|---|
| **1** | … | **✔** | § 2.1 |

<!--saut-->

# Corrigés

## Corrigé du niveau 1 — QCM

| Question | Réponse | Pourquoi |
|:---:|:---:|---|
| 1 | b | … |

## Corrigé du niveau 2 — Exercices types d'examen

::: correction Exercice 1
…
:::

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
| QCM | `**1.** Question ? *(§ 2.k)*` puis une liste `- **a)** …` à `- **d)** …` ; réponses dans « Corrigés » |
| Carte | `::: carte` · question · `--` · réponse · `:::` — anciens cours seulement (avant la décision 13) |

Commandes LaTeX reconnues : `\frac` `\dfrac` `\sqrt` `\text` `\bar` `\overline` `\hat` `\vec`,
exposants, indices, alphabet grec, `\times` `\cdot` `\le` `\ge` `\ne` `\approx` `\sum` `\prod`
`\int` `\partial` `\infty` `\rightarrow` `\Rightarrow` `\Leftrightarrow` `\in` …

Publication : `Semestre1/outils/publier.sh <fichier.md>`.
