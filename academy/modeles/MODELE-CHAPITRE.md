---
matiere: Microéconomie
chapitre: Chapitre 0 — modèle
titre: Squelette d'un chapitre reconstruit
sous_titre: Gabarit imposé et référence complète de la syntaxe de rédaction
resume: Ce fichier sert deux usages : il fixe la structure obligatoire de tout chapitre produit, et il documente chaque élément de mise en forme reconnu par la chaîne de production. Il se compile tel quel — c'est aussi le test de la chaîne.
date: 2 septembre 2026
duree: à renseigner (temps de travail estimé)
version: 1.0
sommaire: oui
---

# Squelette d'un chapitre reconstruit

Les six sections ci-dessous sont **obligatoires** et dans cet ordre. Les passages en
*italique* sont des consignes de rédaction : ils disparaissent du document final.

<!--saut-->

## 1. Carte du chapitre

### Vue d'ensemble

*Dix lignes exactement : de quoi parle ce cours, pourquoi il existe, quel problème
économique il résout, où il s'insère dans la discipline, ce qu'il permettra de faire
au chapitre suivant.*

### Les idées maîtresses

*Cinq à dix affirmations, formulées de façon retenable — pas des thèmes, des propositions.*

1. *Idée 1 — énoncée comme une phrase complète que l'on pourrait défendre à l'oral.*
2. *Idée 2.*

### Prérequis

*Tout prérequis manquant est enseigné ici, brièvement mais complètement. Ne jamais se
contenter de le nommer.*

::: methode Rappel — variation relative et point de pourcentage
Une variation relative se calcule toujours par rapport à la valeur de départ :

$$ \text{variation relative} = \frac{V_1 - V_0}{V_0} $$

Passer de 4 % à 6 %, c'est **+2 points de pourcentage**, mais **+50 %** en variation
relative ($ (6-4)/4 = 0{,}5 $). Confondre les deux coûte des points à chaque copie.
:::

### Lien avec la finance de marché

::: marche
*Le pont vers les marchés, uniquement lorsqu'il est réel — jamais forcé. Exemple type :
l'élasticité de la demande est au producteur ce que le delta est au détenteur d'option —
une sensibilité locale, valable pour de petites variations, et qui se déforme dès que
l'on s'éloigne du point de mesure.*
:::

<!--saut-->

## 2. Le cours reconstruit

*Contenu intégral du support d'origine, réorganisé dans l'ordre pédagogiquement optimal.
Signaler explicitement lorsqu'on s'écarte de l'ordre de l'enseignant, et pourquoi.*

### 2.1 — Premier concept

**À quoi ça sert.** *Le problème concret que la notion résout.*
**D'où ça vient.** *Origine, auteur, contexte historique lorsqu'il éclaire.*

::: definition Élasticité-prix de la demande
**En langage simple :** de combien de pour cent la quantité demandée bouge lorsque le
prix bouge de 1 %.

**Formulation académique :** rapport de la variation relative de la quantité demandée
à la variation relative du prix qui l'a provoquée, les autres déterminants étant
supposés constants (*ceteris paribus*).
:::

::: formule Élasticité-prix
$$ e_{p} = \frac{\Delta Q / Q}{\Delta P / P} = \frac{\Delta Q}{\Delta P} \times \frac{P}{Q} $$

- $ \Delta Q $ : variation absolue de la quantité demandée, en unités.
- $ \Delta P $ : variation absolue du prix, en euros.
- $ P/Q $ : rapport évalué **au point de départ** — l'élasticité dépend du point où on la mesure.

Le signe est négatif pour un bien normal : prix et quantité varient en sens opposé.
On raisonne le plus souvent sur la valeur absolue $ |e_p| $.
:::

::: demo Pourquoi le rapport de deux variations relatives, et non de deux variations absolues
1. Une variation absolue dépend des unités : passer de 100 à 110 kg n'est pas comparable
   à passer de 2 à 2,2 €.
2. Diviser chaque variation par sa valeur de départ élimine les unités : le résultat est
   un nombre pur.
3. Le rapport de deux nombres purs est donc comparable entre biens, entre pays, entre époques.
4. C'est exactement la raison pour laquelle on compare des rendements en pourcentage, et
   non en euros gagnés.
:::

::: exemple Calcul complet
Le prix passe de 20 € à 22 €, la quantité demandée de 500 à 450 unités.

1. $ \Delta P = 22 - 20 = 2 $ € ; $ \Delta P / P = 2/20 = 0{,}10 $ soit +10 %.
2. $ \Delta Q = 450 - 500 = -50 $ ; $ \Delta Q / Q = -50/500 = -0{,}10 $ soit −10 %.
3. $ e_p = -0{,}10 / 0{,}10 = -1 $.
4. Lecture : $ |e_p| = 1 $ — élasticité **unitaire**. La recette totale passe de
   $ 20 \times 500 = 10\,000 $ € à $ 22 \times 450 = 9\,900 $ €, soit −1 %.
   L'élasticité unitaire ne garantit la stabilité *exacte* de la recette que pour une
   variation infinitésimale du prix. Sur une variation discrète, il subsiste un terme du
   second ordre : $ \Delta R = P\,\Delta Q + Q\,\Delta P + \Delta P\,\Delta Q $, dont les
   deux premiers termes se compensent ici ($ -1\,000 + 1\,000 $) et dont le troisième vaut
   $ 2 \times (-50) = -100 $ € — exactement l'écart constaté.
:::

::: piege
Calculer l'élasticité avec la valeur d'arrivée au dénominateur au lieu de la valeur de
départ. Le résultat change, et le correcteur le voit immédiatement. Sauf consigne
contraire, $ P $ et $ Q $ sont pris **au point initial**.
:::

::: examen
Une question sur trois porte sur le lien élasticité / recette totale. À retenir sous
forme de règle : $ |e_p| > 1 $ → baisser le prix augmente la recette ; $ |e_p| < 1 $ →
baisser le prix la diminue ; $ |e_p| = 1 $ → recette maximale.
:::

### 2.2 — Deuxième concept

*Même architecture : utilité, origine, définition, formule, démonstration, exemple chiffré,
piège, point d'examen.*

<!--saut-->

## 3. Points de vigilance

### 3.1 — Confusions classiques

| Notion A | Notion B | Le critère qui les sépare |
|---|---|---|
| *Déplacement **le long de** la courbe* | *Déplacement **de** la courbe* | *Le prix a-t-il changé, ou un autre déterminant ?* |
| *Variation en points* | *Variation en pourcentage* | *Rapport à la valeur de départ ou non* |

### 3.2 — Erreurs de la majorité des étudiants

*Trois à six erreurs précises, constatées sur ce chapitre, avec leur correction.*

### 3.3 — Ce qui sépare une copie moyenne d'une excellente copie

*Ce que fait le major et que les autres ne font pas : nommer les hypothèses, justifier le
signe, interpréter économiquement le résultat, discuter la limite du modèle.*

<!--saut-->

## 4. Système d'ancrage mémoriel

### 4.1 — Fiche de synthèse (une page)

::: synthese L'essentiel du chapitre
*Condensé autosuffisant : les définitions, les formules, les résultats, les conditions
d'application. Doit tenir sur une page imprimée et permettre une révision de 10 minutes.*
:::

### 4.2 — Cartes de révision

::: carte
Que mesure exactement l'élasticité-prix de la demande ?
--
La variation relative de la quantité demandée provoquée par une variation relative du
prix de 1 %, toutes choses égales par ailleurs. C'est un nombre sans unité, mesuré en un
point précis de la courbe.
:::

::: carte
Pourquoi divise-t-on par la valeur de départ et non par la valeur d'arrivée ?
--
Pour que le rapport soit indépendant des unités et du sens de la variation, et donc
comparable d'un bien à l'autre. La convention fixe le point de mesure au point initial.
:::

*Une carte par notion. Aucun trou : toute notion du chapitre doit apparaître dans au
moins une carte.*

### 4.3 — Moyens mnémotechniques

*Pour chaque liste ou classification à retenir : un procédé, expliqué, pas une simple
suite de lettres.*

### 4.4 — Schéma récapitulatif

```
                  [ Notion centrale ]
                   /              \
        [ Branche 1 ]            [ Branche 2 ]
         /       \                  /       \
   [ notion ] [ notion ]      [ notion ] [ notion ]
```

*Décrire ensuite en une phrase chaque lien du schéma : ce qui relie deux notions n'est
jamais évident.*

<!--saut-->

## 5. Entraînement progressif

### Niveau 1 — Restitution

1. *Question de cours vérifiant une définition.*
2. *Question vérifiant un mécanisme.*

::: correction Corrigé du niveau 1
*Réponse complète et rédigée, telle qu'elle serait attendue sur une copie.*
:::

### Niveau 2 — Application

**Exercice 1.** *Énoncé chiffré de type examen, avec toutes les données nécessaires.*

::: correction Corrigé détaillé de l'exercice 1
1. *Étape 1 — ce qu'on cherche et pourquoi cette formule.*
2. *Étape 2 — application numérique, calcul apparent.*
3. *Étape 3 — résultat, unité, interprétation économique.*

*Le résultat seul ne vaut rien : chaque étape est justifiée.*
:::

### Niveau 3 — Maîtrise

*Questions de réflexion, cas transversaux, questions pièges, sujet de dissertation ou
d'analyse. Corrigés rédigés au niveau d'une excellente copie.*

### Niveau 4 — Simulation d'examen

::: methode Conditions de passation
*Format et durée réels du partiel. Chronomètre lancé, aucun document, aucune interruption.*
:::

**Sujet.** *Épreuve complète, avec barème détaillé par question.*

::: correction Corrigé type — « copie de major »
*Copie complète, rédigée, avec le barème appliqué point par point et la justification de
chaque point attribué.*
:::

<!--saut-->

## 6. Auto-évaluation finale

### 6.1 — Liste de contrôle

> Si l'une de ces questions reste sans réponse **sans regarder le document**, le chapitre
> n'est pas maîtrisé.

- [ ] *Question de contrôle 1*
- [ ] *Question de contrôle 2*

### 6.2 — Protocole de révision daté

| Échéance | Durée | Ce qui est révisé |
|---|---|---|
| J+1 | 20 min | *Fiche de synthèse + toutes les cartes + un exercice de niveau 2* |
| J+3 | 30 min | *Cartes échouées à J+1 + deux exercices chronométrés* |
| J+7 | 45 min | *Liste de contrôle à froid + un exercice de niveau 3* |
| J+21 | 60 min | *Simulation d'examen complète + auto-correction au barème* |

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
