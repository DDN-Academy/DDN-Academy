# Captures d'écran du site (mobile, 390 × 844)

Ces images sont produites automatiquement par `npm run captures` (dans `goldpilot/frontend`, après `npm run build`),
à partir du serveur de test isolé des tests de bout en bout (`frontend/e2e/start-backend.sh`).

**Toutes les données visibles sont FICTIVES** (jeu de test `frontend/e2e/seed.py`, libellé « test ») : prix, signaux,
incidents, séries macro et état du compte simulé ne proviennent pas du marché. Les résultats de recherche de la page
Statistiques (verdict, sélection, test final, Monte-Carlo) sont, eux, lus dans `research/output/`.
Le serveur de test utilise la source « TradingView » sans webhook réel et sans Telegram : c'est pourquoi les
notifications apparaissent « non configurées ».

| Fichier | Page |
| --- | --- |
| `connexion.png` | Connexion (mot de passe seul) |
| `accueil.png` | Accueil |
| `signal.png` | Détail d'un signal (clôturé, exécution déclarée) |
| `historique.png` | Historique des signaux |
| `statistiques.png` | Statistiques |
| `journal.png` | Journal (onglet Décisions) |
| `parametres.png` | Réglages (script Pine affiché) |
| `aide.png` | Aide |
