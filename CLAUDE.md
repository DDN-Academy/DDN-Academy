# Mémoire du dépôt

Ce dépôt contient plusieurs projets. **Le travail universitaire vit dans `Semestre1/`** — suivi
d'un étudiant de L1 Économie-Gestion (AMU, FEG), examens du 7 au 18 décembre 2026. Les autres
dossiers (trading, `dania/`, `demos/`, `studio-3d/`…) sont sans rapport : ne pas y toucher.

## Au début de CHAQUE session sur les études — avant toute autre action

1. Lire **`Semestre1/TABLEAU_DE_BORD.md`** puis **`Semestre1/PLANNING.md`**.
2. La consigne permanente de l'étudiant est **`Semestre1/CHARTE.md`** : elle fait foi.
3. Les arbitrages pris pour l'appliquer sont dans `TABLEAU_DE_BORD.md`, section « Décisions prises ».

## À la fin de CHAQUE session

Mettre à jour `TABLEAU_DE_BORD.md` (produit, fait, reste, alertes) et, si l'avancement ou une
donnée a changé, `Semestre1/planning.json` puis régénérer le planning :
`python3 Semestre1/outils/planning.py`. Commiter et pousser.

## Produire et publier

- Un cours = `Semestre1/<Matiere>/Cours/<Matiere>_ChNN_<Sujet>.md`, sur le modèle
  `Semestre1/outils/MODELE_COURS.md` (structure obligatoire et syntaxe).
- Publier : `Semestre1/outils/publier.sh <fichier.md>` → contrôle qualité, PDF à côté du .md et,
  pour un cours, cartes Anki (CSV), fiche + questions de marche, formulaire de la matière,
  glossaire cumulatif. **Ne jamais éditer à la main un fichier dérivé** : corriger le cours, republier.
- Graphiques : `Semestre1/outils/graphes.py` (SVG sans dépendance), un script par chapitre dans
  `<Matiere>/Cours/figures/<chapitre>/`.

## Règles fixes

- Git : développer, commiter et pousser **uniquement** sur `claude/personal-tutor-econ-finance-h4q17d`
  (`git push -u origin claude/personal-tutor-econ-finance-h4q17d`). Pas de pull request sans demande.
- **Le dépôt est public.** Ne jamais y pousser les supports originaux de la faculté ni les notes
  manuscrites de tiers : ils vont dans `Semestre1/<Matiere>/Sources/`, exclu par `.gitignore`.
  Le conteneur étant éphémère, ces originaux disparaissent en fin de session : `SOURCES.md`
  consigne pour chacun ce qui a été reçu et ce qui en a été tiré.
- Recalculer chaque chiffre, ne rien inventer ; un point incertain est signalé comme tel.
