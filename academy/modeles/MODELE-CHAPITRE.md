---
matiere: Matière
chapitre: Chapitre 0 — modèle
titre: Squelette d'un chapitre — format V2 « Machine à 18 »
sous_titre: Gabarit imposé et référence complète de la syntaxe de rédaction
resume: Ce fichier sert deux usages : il fixe la structure obligatoire de tout chapitre produit depuis la refonte V2 du 15 septembre 2026, et il documente chaque élément de mise en forme reconnu par la chaîne de production. Il se compile tel quel — c'est aussi le test de la chaîne.
date: 15 septembre 2026
duree: à renseigner
version: 2.0
sommaire: oui
---

# Le format V2 en un coup d'œil

Sept blocs, ordre imposé, aucun facultatif. Le document est construit **dans l'ordre
d'utilisation par l'étudiant**, pas dans l'ordre logique de la discipline.
**La charte complète fait foi : `academy/SYSTEME.md`.**

| Bloc | Nom | Usage | Volume |
|:---:|---|---|---|
| **0** | Le contrat | lu 1× | 1 p. |
| **1** | Le noyau | **appris**, relu 5× | 6-10 p. |
| **2** | Le cours qui explique | lu 1× | 15-25 p. |
| **3** | Les automatismes | consulté | 3-6 p. |
| **4** | La banque d'examen | **pratiqué** | libre |
| **5** | Pièges et points volés | relu 2× | 2-4 p. |
| **6** | Annexe — tableau de couverture | vérifié | libre |

**Plafond de lecture : blocs 0 + 1 + 2 + 5 ≤ 35 pages.** Au-delà malgré une écriture serrée :
deux fichiers, `<chapitre>.md` et `<chapitre>-integral.md`, mêmes numéros de paragraphes,
renvois « ➔ intégrale § X ».

<!--saut-->

# Bloc 0 — Le contrat

## Ce qui t'attend à l'examen

*Nature, durée, barème, pondération. **Si le format n'est pas connu, l'hypothèse retenue est
écrite explicitement ici**, et la demande d'information figure au bloc 6.*

## Le budget de révision

*Tableau des huit séances (S1 à S8), avec date relative, durée en minutes et contenu exact.
Total attendu : 4 h 30 à 5 h par chapitre.*

## Ce que chaque bloc rapporte

| Ce que tu sais | Note atteignable |
|---|:---:|
| Le **bloc 1**, parfaitement | ≈ 12/20 |
| + le **bloc 2** compris | ≈ 15/20 |
| + le **bloc 4** travaillé | ≈ 18/20 |
| + le **bloc 5** | 18 à 20/20 |

## Mode d'emploi des sept blocs

*Tableau : bloc · pages · usage · combien de fois. Suivi d'un encadré `synthese` donnant la
charge réelle : total des pages, dont combien à lire, dont combien à apprendre.*

<!--saut-->

# Bloc 1 — Le noyau

> *Tout ce qui tombera, et rien d'autre. Aucune prose : tableaux, listes numérotées, formules
> encadrées, définitions d'une à trois lignes. Chaque définition est rédigée dans la
> formulation exacte à recopier en copie.*

## N1 — *Première notion*

::: definition À savoir mot pour mot
*La définition, dans la forme exacte à restituer. Attribution si elle existe.*
:::

## N2 — *Deuxième notion*

*Etc. Numéroter N1, N2, N3… : le bloc 2 et le bloc 4 y renvoient.*

::: piege La distinction qui sépare 14 de 18
*Le point de confusion classique, avec le critère net qui le tranche.*
:::

## N*n* — Les chiffres à savoir

| Chiffre | Ce qu'il mesure | Source |
|---:|---|:---:|

## N*n+1* — Les auteurs, sources et dates

| Nom | Ce qu'il apporte | Repère |
|---|---|---|

<!--saut-->

# Bloc 2 — Le cours qui explique

> *Se lit une seule fois. Sa fonction n'est pas d'être su : c'est de rendre le bloc 1
> compréhensible, donc mémorisable. Chaque section renvoie au point du noyau qu'elle éclaire.*

## 2.1 — *Premier concept* ➔ noyau N1

**À quoi ça sert.** *Le problème concret que la notion résout.*
**D'où ça vient.** *Origine, auteur, contexte, lorsqu'ils éclairent.*

::: definition *Terme*
**En langage simple :** *…*
**Formulation académique :** *…*
:::

::: formule *Nom de la formule*
$$ e_{p} = \frac{\Delta Q / Q}{\Delta P / P} $$

- $ \Delta Q $ : *signification, unité.*
- *Chaque symbole, sans exception.*
:::

::: demo Pourquoi cette formule et pas une autre
1. *Étape 1.*
2. *Étape 2 — aucune étape ne suppose un calcul non montré.*
:::

::: exemple Calcul complet
*Un seul exemple, celui qui peut tomber, calculs intermédiaires apparents.*
:::

::: marche Le même raisonnement sur les marchés
*Uniquement lorsque l'analogie est réelle — jamais forcée.*
:::

<!--saut-->

# Bloc 3 — Les automatismes

## 3.1 — Le minutage de l'épreuve

| Phase | Durée | Ce que tu fais |
|---|---:|---|
| Lecture | 5 min | *…* |
| Production | *…* | *Minutes par point du barème.* |
| Relecture | 5 min | *…* |

## 3.2 — Gabarit 1 : « Définissez… »

*Format imposé : « On te demande X → tu fais 1, 2, 3. » Un gabarit par type de question
repérable dans la matière.*

::: correction Exemple appliqué
*Une réponse modèle complète, suivie de la raison pour laquelle elle prend le maximum.*
:::

## 3.*n* — Les phrases qui rapportent

| Situation | La phrase |
|---|---|

## 3.*n+1* — Les recettes de calcul

::: formule Les calculs du chapitre
*Toutes les formules opératoires, numérotées.*
:::

<!--saut-->

# Bloc 4 — La banque d'examen

> *Ne se lit pas : se fait. Document fermé, réponse produite de mémoire, puis vérification.*

## Série A — Flash

::: carte
*La question.*
--
*La réponse, complète mais brève.*
:::

## Série B — Application chiffrée

### B1 — *Titre* *(n minutes)*

*L'énoncé.*

::: correction Corrigé B1
*Chaque étape justifiée, jamais le seul résultat.*
:::

## Série C — Réflexion

::: correction Corrigé C1 — copie de major
*Réponse rédigée au niveau attendu d'une excellente copie.*
:::

## Série D — Simulation d'examen

::: methode Conditions de passation
*Format, durée et barème réels. Minutage conseillé.*
:::

*Le sujet complet.*

::: correction Barème détaillé et corrigé « copie de major »
*Barème appliqué ligne à ligne, puis la copie, puis « ce qui ferait perdre des points ».*
:::

::: examen Grille de report
| Partie | Points | Obtenus |
|---|:---:|:---:|

**Décision.** *Seuil 16/20 et conduite à tenir selon le résultat.*
:::

<!--saut-->

# Bloc 5 — Pièges et points volés

## 5.1 — Les erreurs du support

| № | Ce que dit le support | Ce qui est exact | Conduite en examen |
|:---:|---|---|---|

## 5.2 — Les confusions classiques

| № | Ne pas confondre | Le critère qui sépare |
|:---:|---|---|

## 5.3 — Les points volés

*Ce que la copie à 18 contient et que la copie à 14 n'a pas, chacun formulé prêt à l'emploi.*

## 5.4 — Les fautes qui coûtent le plus cher

::: piege À relire la veille
*Cinq maximum, les plus coûteuses.*
:::

<!--saut-->

# Bloc 6 — Annexe : tableau de couverture du support

> *Une ligne par diapositive, page, photo ou section. **Aucun numéro manquant** — un trou
> dans la numérotation serait un trou dans le traitement.*

| # | Élément du support | Nature | Traité dans | État |
|:---:|---|---|---|:---:|
| 1 | *Diapo 1 — titre et plan* | *plan* | *Bloc 2, § 2.0* | ✔ |
| 2 | *Diapo 2 — formule posée sans démonstration* | *ellipse orale* | *Bloc 2, § 2.1* | ⚠ |
| 3 | *Photo 2 — bas du tableau illisible* | *source* | *—* | ✖ |

**Bilan : *n* éléments inventoriés — *a* ✔, *b* ⚠, *c* ✖.**

**Légende.** ✔ traité intégralement — ⚠ traité, mais support incomplet : la reconstruction
est signalée à l'endroit exact — ✖ impossible à traiter, donnée manquante.

::: piege Demandes ouvertes
*Un ✖ n'est jamais silencieux. Chacun est repris ici, avec la demande précise.*
:::

---

## Référence de syntaxe

*Cette dernière partie ne figure pas dans un vrai chapitre : elle documente la chaîne.*

| Élément | Écriture |
|---|---|
| Titres | `#` `##` `###` `####` — `##` et `###` alimentent le sommaire |
| Emphase | `**gras**`, `*italique*`, `==surligné==`, et le code entre accents graves |
| Lien | `[texte](url)` |
| Listes | `-` à puces, `1.` numérotées, imbrication par deux espaces |
| Tableau | `\| a \| b \|` puis `\|---\|---:\|` (`:---:` centre, `---:` aligne à droite) |
| Citation | `> texte` |
| Filet | `---` |
| Saut de page | `<!--saut-->` |
| Maths en ligne | `$ e_p = \frac{\Delta Q}{\Delta P} \times \frac{P}{Q} $` |
| Maths centrées | `$$ ... $$` sur leurs propres lignes |
| Encadré | `::: type Titre libre` … `:::` |
| Carte de révision | `::: carte` … `--` … `:::` |

Types d'encadrés : `definition`, `formule`, `demo`, `exemple`, `piege`, `examen`,
`methode`, `correction`, `marche`, `synthese`, `objectif`, `carte`.

Commandes LaTeX reconnues : `\frac` `\dfrac` `\sqrt` `\text` `\mathrm` `\mathbf`
`\bar` `\overline` `\hat` `\vec` `\mathbb`, exposants `^{}`, indices `_{}`, l'alphabet
grec complet, et les symboles usuels (`\times` `\cdot` `\le` `\ge` `\ne` `\approx`
`\sum` `\prod` `\int` `\partial` `\infty` `\rightarrow` `\Rightarrow` `\in` `\cup`
`\cap` …). Pour un nom de plusieurs lettres, utiliser `\text{VAN}` afin qu'il reste droit.

Compilation :

```bash
academy/outils/make.sh academy/modeles/MODELE-CHAPITRE.md
```
