# academy/ — atelier de tutorat

Chaîne complète qui transforme un cours de faculté en document d'apprentissage
autonome : structuré, exhaustif, imprimable, révisable.

Le principe est fixé une fois pour toutes dans **[SYSTEME.md](SYSTEME.md)** : le document
produit remplace le support d'origine. Rien n'y est supposé connu, rien n'y est reporté.

---

## Marche à suivre

1. **Déposer le cours** dans `cours-source/` (voir [le mode d'emploi](cours-source/README.md)),
   ou le transmettre directement dans la conversation.
2. **Confirmation en trois lignes** : matière et chapitre identifiés, notions couvertes,
   zones elliptiques repérées dans le support d'origine.
3. **Production du chapitre** dans `chapitres/<matiere>-<numero>-<sujet>.md`, selon le
   squelette imposé de [`modeles/MODELE-CHAPITRE.md`](modeles/MODELE-CHAPITRE.md).
4. **Compilation** :

   ```bash
   academy/outils/make.sh academy/chapitres/micro-01-offre-demande.md
   ```

   Produit dans `export/` un HTML autonome (lisible partout, hors ligne) et un
   PDF A4 paginé, pied de page numéroté.

---

## Arborescence

| Dossier | Contenu |
|---|---|
| `cours-source/` | Supports bruts : PDF, diapositives, photos de tableau, polycopiés, notes, retranscriptions |
| `chapitres/` | Documents produits, en Markdown étendu — la source de vérité |
| `export/` | HTML + PDF générés (régénérables à tout moment) |
| `modeles/` | Squelette imposé d'un chapitre et référence complète de la syntaxe |
| `outils/` | `build.py` (Markdown → HTML), `pdf.cjs` (HTML → PDF), `make.sh` (les deux), `theme.css` |
| `SYSTEME.md` | Charte de fonctionnement : structure obligatoire, exigences, contrôle qualité |
| `tableau-de-bord.md` | Coefficients, échéances, niveau par matière — pilotage des priorités |

---

## Outils

`outils/build.py` n'utilise que la bibliothèque standard de Python : aucune installation.
Le HTML produit embarque sa feuille de style — il s'ouvre partout, s'envoie par mail,
et s'imprime directement (`Ctrl` / `Cmd` + `P` → « Enregistrer en PDF »).

`outils/pdf.cjs` s'appuie sur Playwright pour obtenir la pagination. En son absence,
`make.sh` bascule automatiquement sur l'impression directe de Chromium ; à défaut, il
indique la marche à suivre manuelle. Aucune de ces étapes n'est bloquante.

```bash
academy/outils/make.sh <chapitre.md>          # HTML + PDF
python3 academy/outils/build.py <chapitre.md> # HTML seul
```

---

## Deux points d'attention

**Publication.** Le dépôt est déployé sur GitHub Pages depuis la branche `main`
(`.github/workflows/deploy.yml` publie la racine du dépôt). Tout ce qui est fusionné dans
`main` devient donc accessible publiquement, `academy/` compris. Si les documents doivent
rester privés, il faut soit les garder hors de `main`, soit restreindre le chemin publié
dans le workflow. Rien n'a été modifié en ce sens : c'est une décision à prendre.

**Les fichiers d'`export/` sont dérivés.** On corrige toujours le `.md` dans `chapitres/`,
puis on recompile. Corriger le HTML ou le PDF à la main revient à perdre la correction à
la compilation suivante.
