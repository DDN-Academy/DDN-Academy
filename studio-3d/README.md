# Studio 17 m² — visite 3D interactive AVANT / APRÈS

Reconstitution en 3D d'un studio meublé de 17 m² à Aix-en-Provence, avec bascule
instantanée entre l'état actuel et l'état après relooking. Pensé pour un
**locataire**, budget **150 à 400 €**, sans aucun travaux lourd.

---

## Lancer le site

**Le plus simple : double-cliquer sur `index.html`.**
Three.js est embarqué dans `vendor/three.min.js`, donc la page fonctionne hors
ligne et directement en `file://`, sans serveur ni installation.

Si vous préférez un serveur local (recommandé si vous modifiez le fichier, pour
éviter le cache du navigateur) :

```bash
cd studio-3d
python3 -m http.server 8000
# puis ouvrir http://localhost:8000
```

Aucun `npm install`, aucune étape de build. Un seul fichier de code :
`index.html` (HTML + CSS + JavaScript + géométrie 3D).

### Structure

```
studio-3d/
├── index.html          ← tout le site : interface, modèle 3D, logique budget
├── vendor/
│   └── three.min.js    ← Three.js r128 (copie locale, repli CDN automatique)
└── README.md
```

---

## Commandes

| Action | Desktop | Mobile |
|---|---|---|
| Basculer AVANT / APRÈS | bouton en haut à droite, ou **barre d'espace** | bouton en haut à droite |
| Vue orbite | glisser pour tourner, molette pour zoomer | glisser, pincer pour zoomer |
| Vue première personne | **ZQSD** ou flèches pour marcher, souris pour regarder | joystick tactile, glisser pour regarder |
| Ouvrir une fiche | cliquer un point ambré, ou le nom d'un poste dans le budget | idem |
| Fermer une fiche | croix, ou **Échap** | croix |

La bascule AVANT / APRÈS **conserve la position de la caméra** et ne recharge
rien : la transition est un fondu de ~0,4 s sur les matériaux, les objets et
l'éclairage.

---

## Panneau budget

Chaque poste est une case à cocher : la décocher **retire l'élément de la scène
3D en temps réel** et met à jour le total.

| # | Poste | Prix | Priorité | Réversible |
|---|---|---|---|---|
| 1 | Désencombrement + gaine passe-câbles | 10 € | 1 | oui |
| 2 | Éclairage chaud 2700K (LED, lampes, ampoules) | 60 € | 2 | oui |
| 3 | Grand tapis anthracite | 60 € | 3 | oui |
| 4 | Linge de lit uni foncé + coussins | 70 € | 4 | oui |
| 5 | Peinture mur d'accent anthracite | 40 € | 5 | **non — accord propriétaire** |
| 6 | Décoration (cadres noirs, plante, miroir) | 55 € | 6 | oui |
| 7 | Boîtes de rangement fermées + meuble TV bas | 90 € | 7 | oui |

**Presets** — Minimal **130 €** (postes 1-2-3) · Recommandé **295 €**
(postes 1 à 6) · Complet **385 €** (tout).

---

## Ajuster les dimensions une fois vos murs mesurés

Tout est regroupé dans l'objet **`CONFIG`**, en tête du bloc `<script>` de
`index.html` (cherchez `██  CONFIG`). Rien d'autre à toucher : la géométrie et
les collisions se recalculent seules au rechargement de la page.

Repère utilisé : **X** vers la droite, **Z** de la fenêtre (Z = 0) vers l'entrée,
**Y** vers le haut. Unité : le **mètre**. Les rectangles `{x0, z0, x1, z1}`
donnent l'**axe des murs**, pas la face intérieure.

### Ce qu'on ajuste en premier

```js
hauteurPlafond : 2.50,                              // mesurez du sol au plafond
piece    : { x0:0.00, z0:0.00, x1:3.40, z1:3.60 },  // pièce principale
salleEau : { x0:3.40, z0:0.00, x1:4.60, z1:2.10 },  // salle d'eau
couloir  : { x0:3.40, z0:2.10, x1:4.60, z1:3.60 },  // entrée + placard
```

Puis les ouvertures, où `u` est la distance depuis le début du mur et `y0`/`y1`
le bas et le haut de l'ouverture :

```js
fenetreFond   : { u0:0.55, u1:2.15, y0:0.95, y1:2.15 },  // largeur et allège
porteEntree   : { u0:3.65, u1:4.45, y0:0.00, y1:2.10 },
```

Enfin le mobilier, chaque meuble par son emprise au sol :

```js
lit      : { x0:2.00, x1:3.38, z0:0.25, z1:2.25, hDosseret:0.86 },
kitchen  : { x0:1.00, x1:2.45, z0:3.00, z1:3.55, h:0.90 },
tapis    : { x0:0.62, x1:1.98, z0:0.55, z1:2.60 },
```

Les couleurs sont dans `CONFIG.avant` (état actuel, relevé sur les photos) et
`CONFIG.apres` (état rénové), au format hexadécimal `0xRRGGBB`. L'intensité des
deux ambiances se règle dans `CONFIG.lumiere`.

---

## Hypothèses prises faute de mesures

Aucune cote n'était lisible sur les photos. Ces valeurs sont des estimations
plausibles, à corriger dans `CONFIG` :

- **Plan en L** (pièce principale + couloir d'entrée avec placard + salle
  d'eau) déduit des cinq photos. Surface nette modélisée ≈ 16,2 m², soit
  ≈ 17 m² murs compris.
- **Proportions** calées sur la largeur standard d'un lit gigogne IKEA Hemnes
  (1,40 m), visible sur la photo de la chambre, et sur les lames de carrelage.
- **Hauteur sous plafond 2,50 m**, standard d'une résidence des années 80-90.
- **Fenêtre d'angle à deux vantaux**, allège à 0,95 m.
- **Kitchenette** jamais visible en entier : figurée en niche de 1,45 m au fond
  de la pièce principale.
- **Mobilier** modélisé en primitives stylisées (pas de modèles importés) :
  les volumes et les couleurs sont fidèles, pas les détails.

---

## Parti pris de la direction artistique

Le style des inspirations (chambre masculine sombre, LED chaudes, textiles unis)
a été appliqué **de façon mesurée**, parce que 17 m² tout en noir deviennent
étroits et sombres :

- **un seul mur d'accent anthracite**, celui derrière le lit, lambris bas
  compris ; les trois autres murs restent clairs ;
- la chaleur vient de **l'éclairage** (2700K, halos indirects) et des
  **matières**, pas du noir généralisé ;
- **le sol est identique dans les deux modes** — carrelage imitation parquet
  clair, propriété du bailleur, non modifiable. Il est assombri visuellement par
  le grand tapis charbon, et par rien d'autre ;
- **tout le mobilier existant est conservé** : lit gigogne, commode, étagère
  colonne, meuble vasque. Seuls changent textiles, boîtes, éclairage et déco ;
- en mode APRÈS, **aucun carton, sac, vêtement en vrac ni câble apparent** :
  c'est le poste n°1, à 10 €.

Un seul poste n'est pas réversible : la peinture du mur d'accent. Elle demande
l'accord écrit du propriétaire, souvent accordé, parfois déductible du loyer —
et un retour en blanc à la sortie s'il refuse.
