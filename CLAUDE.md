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
foi**, avec l'amendement ci-dessous, qui prime sur son déroulement en trois étapes.

**Amendement du 29 septembre — cours au fil de l'eau (demande de l'étudiant).** Les profs publient
les cours au fil du semestre : l'étudiant n'aura jamais « toutes les matières » d'un coup. Donc :

1. **Chaque cours reçu** (support de la fac, avec les documents de la marraine qui s'y rapportent)
   est rangé, sauvegardé et analysé, **puis reconstruit aussitôt** au format du Livrable 3, publié
   en PDF avec ses cartes Anki, et envoyé à l'étudiant.
2. **Le planning (Livrable 2) est glissant** : régénéré à chaque cours reçu et à chaque bilan du
   dimanche, à partir du 1er octobre, en respectant exactement le volume de la charte.
3. **L'analyse globale (Livrable 1)** se complète matière par matière ; la preuve que tout tient
   dans les 560 pomodoros est refaite à chaque nouvelle matière.

Toutes les autres règles de la charte restent intactes : tout su par cœur avant le 7 décembre,
protocoles, révisions J+1 · J+3 · J+7 · J+21, entrelacement, contrôle qualité. Le mode en vigueur
est rappelé dans `Semestre1/TABLEAU_DE_BORD.md`, § 1.

Ordre des envois annoncé le 29 septembre : d'abord les notes de la marraine (reçues pour les
Institutions politiques), puis les cours des matières, **en commençant par les Institutions
politiques**.

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
  glossaire), `graphes.py` (figures SVG), `planning.py` (planning glissant, lu dans
  `Semestre1/planning.json`). `MODELE_COURS.md`, `verifier.py` et `extraire.py` suivent la
  structure du Livrable 3 de la charte (carte · cours · pièges et points bonus · ancrage ·
  entraînement en 4 niveaux · auto-évaluation, plus les questions de marche) ; `planning.py` suit
  le calendrier 7 j/7 (4 pomodoros par jour du 1er au 15 octobre, 8 du 16 octobre au 15 novembre,
  12 du 16 novembre au 6 décembre : 560 au total).
- **Ne jamais éditer à la main un fichier dérivé** : corriger la source, republier.
- **L'étudiant ne va jamais sur GitHub.** Ce qu'il doit travailler lui est **envoyé directement
  dans la conversation** (outil `SendUserFile`), avec une phrase simple qui dit quoi en faire —
  **un seul fichier par cours : le PDF du cours**, qui contient déjà la fiche, les cartes et les
  questions de marche ; le planning en PDF quand il change ; le CSV Anki seulement s'il le demande
  (le 29 septembre, il avait pris le CSV pour le cours). Vérifier que chaque envoi est bien arrivé :
  le service renvoie parfois des erreurs, il faut alors réessayer. Ses propres documents sont dans
  sa page privée « Dossier <Matière> ».

## Règles fixes

- Git : développer, commiter et pousser **uniquement** sur `claude/personal-tutor-econ-finance-h4q17d`
  (`git push -u origin claude/personal-tutor-econ-finance-h4q17d`). Pas de pull request sans demande.
- **Le dépôt est public** (celui du mentorat DDN Academy, avec un site GitHub Pages en ligne : ne
  jamais le passer en privé). Ne jamais y pousser les supports de la faculté ni les notes de la
  marraine : ils vont dans `Semestre1/<Matiere>/Sources/`, exclu par `.gitignore`, et sont
  inscrits dans `SOURCES.md`. Le conteneur étant éphémère, ces originaux disparaissent en fin de
  session : **une copie de sauvegarde de chaque document est publiée dans un artefact privé
  claude.ai, un par matière (« Dossier <Matière> »)**, dont l'adresse est notée dans `SOURCES.md` ;
  l'analyse de chaque envoi y est jointe (`analyse.md`), jamais dans le dépôt public. Une session
  suivante récupère un fichier avec l'outil Artifact (`read`, `path` ou `paths`), puis republie le
  dossier (même `url`) quand un document s'ajoute.
  Pas de dépôt GitHub privé : Claude n'a pas le droit d'en créer (403) et l'étudiant a décliné le
  29 septembre — ne plus le lui proposer.
- Recalculer chaque chiffre, ne rien inventer ; un point incertain est signalé comme tel.
