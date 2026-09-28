# Mémoire du dépôt

Ce dépôt contient plusieurs projets. **Le travail universitaire vit dans `Semestre1/`** — suivi
d'un étudiant de L1 Économie-Gestion (AMU, FEG), examens du 7 au 18 décembre 2026. Les autres
dossiers (trading, `dania/`, `demos/`, `studio-3d/`…) sont sans rapport : ne pas y toucher.

**`academy/` est une archive** de tout le travail antérieur à la charte du 28 septembre 2026
(soir) : versions 1 et 2 des chapitres, et `academy/version3/` (six cours, planning, analyse,
tableau de bord faits sous la consigne précédente). Ne plus y travailler ni s'en servir comme
référence.

## La consigne — à suivre à la lettre

`Semestre1/CHARTE.md` reproduit à l'identique la consigne permanente de l'étudiant : **elle fait
foi.** Elle impose un déroulement en trois étapes — l'étape en cours est notée dans
`Semestre1/TABLEAU_DE_BORD.md`, § 1 :

1. **Réception, matière par matière** : à chaque matière reçue (cours de la fac + documents de la
   marraine), ranger les documents, les analyser, faire un **court bilan** — chapitres identifiés,
   format probable de l'examen, documents manquants — puis **attendre** la matière suivante.
2. **« Toutes les matières sont envoyées »** : analyse globale (Livrable 1) et emploi du temps
   complet (Livrable 2).
3. **Seulement ensuite** : produire les cours reconstruits (Livrable 3), dans l'ordre du planning.

**Ne jamais produire un cours avant l'étape 3.**

## Au début de CHAQUE session sur les études — avant toute autre action

1. Lire **`Semestre1/TABLEAU_DE_BORD.md`** puis **`Semestre1/PLANNING.md`**.
2. Relire au besoin `Semestre1/CHARTE.md` ; les arbitrages pris pour l'appliquer sont dans
   `TABLEAU_DE_BORD.md`, section « Décisions prises ».

## À la fin de CHAQUE session

Mettre à jour `TABLEAU_DE_BORD.md` et `PLANNING.md` (et `SOURCES.md` si un document a été reçu).
Commiter et pousser.

## Produire et publier

- Un cours = `Semestre1/<Matiere>/Cours/<Matiere>_ChNN_<Sujet>.md`.
- Outils dans `Semestre1/outils/` : `publier.sh <fichier.md>` (PDF, cartes Anki, fiche, formulaire,
  glossaire), `graphes.py` (figures SVG), `planning.py`. **Avant l'étape 3**, adapter
  `MODELE_COURS.md`, `verifier.py` et `extraire.py` à la structure du Livrable 3 de la charte
  (carte · cours · pièges et points bonus · ancrage · entraînement en 4 niveaux · auto-évaluation,
  plus les questions de marche) ; **avant l'étape 2**, adapter `planning.py` au calendrier 7 j/7
  (4 pomodoros par jour du 1er au 15 octobre, 8 du 16 octobre au 15 novembre, 12 du 16 novembre au
  6 décembre : 560 au total).
- **Ne jamais éditer à la main un fichier dérivé** : corriger la source, republier.

## Règles fixes

- Git : développer, commiter et pousser **uniquement** sur `claude/personal-tutor-econ-finance-h4q17d`
  (`git push -u origin claude/personal-tutor-econ-finance-h4q17d`). Pas de pull request sans demande.
- **Le dépôt est public** (celui du mentorat DDN Academy, avec un site GitHub Pages en ligne : ne
  jamais le passer en privé). Ne jamais y pousser les supports de la faculté ni les notes de la
  marraine : ils vont dans `Semestre1/<Matiere>/Sources/`, exclu par `.gitignore`, et sont
  inscrits dans `SOURCES.md`. Le conteneur étant éphémère, ces originaux disparaissent en fin de
  session. Un dépôt privé dédié au semestre a été proposé à l'étudiant (voir le tableau de bord,
  alertes) : ne le créer qu'avec son accord explicite.
- Recalculer chaque chiffre, ne rien inventer ; un point incertain est signalé comme tel.
