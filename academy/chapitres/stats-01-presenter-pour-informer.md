---
matiere: Techniques statistiques — L1 Portail, Division A, AMU
chapitre: Chapitre 1 — Présenter pour informer
titre: Présenter pour informer
sous_titre: La démarche de l'étude statistique, le vocabulaire de la statisticienne, et la présentation des données sans perte d'information
resume: Ce document reconstruit intégralement le premier chapitre de Techniques statistiques. Il couvre les 33 diapositives du support : les six étapes d'une étude statistique, le vocabulaire fondamental et la typologie des variables, puis toutes les façons de présenter une distribution — série brute, effectifs, fréquences, fréquences cumulées, et les cinq familles de diagrammes. Les questions posées en amphithéâtre y sont intégralement traitées, et les données du cours ont été recalculées une à une.
date: 4 septembre 2026
duree: première lecture 2 h 30 — maîtrise complète ≈ 7 h réparties sur 3 semaines
version: 1.0
sommaire: oui
---

# Chapitre 1 — Présenter pour informer

Ce document remplace le support de cours. Les 33 diapositives y sont couvertes, sans
exception : le **tableau de couverture** en annexe permet de le vérifier ligne par ligne.
Toutes les questions posées à l'amphithéâtre — dont les réponses n'existaient que dans
l'oral — sont traitées, et **chaque chiffre du support a été recalculé**.

<!--saut-->

## 1. Carte du chapitre

### 1.1 — Vue d'ensemble

Ce chapitre répond à une question simple et redoutable : **comment transformer des données
brutes en information utilisable pour décider ?** La statistique descriptive n'est pas un
exercice de calcul, c'est une chaîne qui part d'un besoin de décision et qui aboutit à un
rapport. Le chapitre parcourt cette chaîne en trois temps. D'abord la **méthode** : les six
étapes d'une étude statistique, de la formulation de la problématique à la prise de
décision, avec un principe qui commande tout le reste — chaque choix technique découle de
la problématique, jamais l'inverse. Ensuite le **vocabulaire** : population, unité
statistique, effectif, variable, modalité, et la typologie des variables en deux types et
quatre sous-types, sans laquelle aucun traitement n'est possible puisque le type de
variable détermine les traitements autorisés. Enfin la **présentation** : comment exposer
une distribution sans rien perdre de l'information — série brute, tableau d'effectifs,
fréquences, fréquences cumulées — et comment choisir le diagramme qui répond à la question
posée. C'est la **première étape** de toute analyse : les chapitres suivants résumeront
(CHAP 2), suivront l'évolution dans le temps (CHAP 3) et croiseront les variables (CHAP 4).

### 1.2 — Les idées maîtresses

Huit affirmations. Si vous ne deviez retenir que cela du chapitre, ce serait cela.

1. **La chaîne est : besoin de décider → besoin d'information → étude statistique.** La
   statistique ne se déclenche pas toute seule ; elle répond à une décision à prendre.
2. **Tous les choix techniques sont guidés par le type de problématique.** C'est le message
   du schéma des six étapes : toutes les flèches de retour pointent vers l'étape 1.
3. **Une problématique vague rend l'étude impossible.** « Faites-moi une enquête de
   satisfaction » n'est pas une commande exploitable.
4. **Le type de variable détermine tout ce qu'on a le droit de faire ensuite.** Deux types
   (qualitative, quantitative), quatre sous-types (nominale, ordinale, discrète, continue).
5. **Une variable qualitative peut être codée par des nombres sans devenir quantitative.**
   Le codage n'est pas la nature de la variable.
6. **Présenter n'est pas résumer.** Série brute, tableau d'effectifs, fréquences et
   fréquences cumulées se transforment l'un en l'autre **sans perte d'information** ; le
   résumé (moyenne, écart-type) viendra au chapitre 2, et lui, il perd de l'information.
7. **Le choix du diagramme est dicté par la comparaison que l'on veut faire voir**, non par
   l'esthétique : effectifs ou structure, une catégorie dans le temps ou une année en
   coupe.
8. **Ce n'est pas le rapport statistique qui décide.** La décision est politique ; le
   rapport l'éclaire. Toute information non informative au regard de la problématique doit
   être bannie.

### 1.3 — Prérequis

Le chapitre mobilise quatre outils qu'il n'enseigne pas. Ils sont enseignés ici.

::: methode Prérequis 1 — Proportion, fréquence, pourcentage
Une **proportion** est un quotient entre une partie et un tout : elle vaut entre 0 et 1.
Un **pourcentage** est la même chose exprimée pour cent : on multiplie la proportion par 100.

$$ \text{proportion} = \frac{\text{effectif de la partie}}{\text{effectif total}}
\qquad \text{pourcentage} = \text{proportion} \times 100 $$

Si 33 étudiants sur 87 ont exactement un frère ou une sœur, la proportion vaut
$ 33/87 = 0{,}3793 $, soit **37,93 %**, arrondi à **37,9 %**.

**Trois vérifications réflexes**, à faire systématiquement :
1. la somme de toutes les proportions d'une distribution vaut **1** (100 %) ;
2. une proportion est toujours comprise entre 0 et 1 : un résultat négatif ou supérieur
   à 1 signale une erreur de calcul ;
3. si la somme des pourcentages affichés vaut 99,9 % ou 100,1 %, ce n'est **pas** une
   erreur : c'est l'effet des **arrondis**. On l'écrit en note de tableau.
:::

::: methode Prérequis 2 — Le signe somme Σ
La diapositive 23 emploie le symbole $ \sum $ sans l'avoir introduit. C'est une simple
abréviation d'une addition.

$$ \sum_{i=1}^{p} n_i = n_1 + n_2 + \ldots + n_p $$

Lecture, de gauche à droite : « somme, pour $ i $ allant de 1 jusqu'à $ p $, des
$ n_i $ ». Trois éléments à identifier :

- l'**indice de sommation** ($ i $) : le compteur ; il n'existe qu'à l'intérieur de la
  somme ;
- les **bornes** (de 1 à $ p $) : où le compteur commence et où il s'arrête ;
- le **terme général** ($ n_i $) : ce que l'on additionne à chaque tour.

**Exemple chiffré.** Avec $ n_1 = 11 $, $ n_2 = 33 $, $ n_3 = 23 $ :
$ \sum_{i=1}^{3} n_i = 11 + 33 + 23 = 67 $.

**Piège classique :** $ p $ est le nombre de **modalités**, pas le nombre d'individus.
Dans l'exemple des 87 étudiants, il y a $ n = 87 $ individus mais seulement $ p = 11 $
modalités observées.
:::

::: methode Prérequis 3 — Ensemble dénombrable et non dénombrable
La distinction sert à séparer le quantitatif **discret** du quantitatif **continu**, et le
support l'emploie sans la définir.

- Un ensemble est **dénombrable** quand on peut énumérer ses éléments un par un, en les
  numérotant, même s'ils sont en nombre infini. Les entiers naturels 0, 1, 2, 3… sont
  dénombrables. **On compte.**
- Un ensemble est **non dénombrable** quand, entre deux valeurs, il en existe toujours une
  infinité d'autres qu'on ne peut pas énumérer. Les nombres réels d'un intervalle sont non
  dénombrables. **On mesure.**

**Le test pratique en examen** : entre deux valeurs voisines de la variable, une valeur
intermédiaire a-t-elle un sens ?
- Nombre d'enfants : entre 2 et 3, rien. → **discrète**.
- Taille en centimètres : entre 179 et 180, il y a 179,4 ; entre 179,4 et 179,5, il y a
  179,43… → **continue**.

**Nuance à connaître :** une taille mesurée au centimètre près *paraît* prendre des valeurs
entières. La variable reste **continue** : c'est l'**instrument de mesure** qui est
discret, pas la grandeur mesurée. Le critère porte sur la nature de la grandeur, jamais sur
la précision de l'appareil.
:::

::: methode Prérequis 4 — Lire un tableau statistique
Un tableau publié se lit dans un ordre fixe. Cet ordre est la première chose que vérifie un
correcteur.

1. **Le titre** : de quoi parle-t-on ?
2. **Le champ** : sur qui porte l'information ? (« France hors Mayotte, familles vivant en
   ménage ordinaire ayant au moins un enfant mineur »)
3. **L'unité** : en quoi sont exprimés les nombres ? (« en milliers » change tout)
4. **La source** et sa date.
5. **Les en-têtes** de lignes et de colonnes : où est la variable, où sont les
   sous-populations ?
6. **Une cellule**, enfin — et jamais avant les cinq points précédents.

**Phrase de lecture type**, à réutiliser telle quelle :
> « En [année], [effectif ou pourcentage] des [unités statistiques] du champ [champ]
> présentaient la modalité [modalité] de la variable [variable]. »
:::

### 1.4 — Lien avec la finance de marché

Ce chapitre n'est pas un préliminaire administratif : c'est **exactement** la boîte à
outils du travail quotidien sur les marchés.

::: marche
- **La distribution des effectifs, c'est l'histogramme des rendements.** Ranger les
  variations quotidiennes d'un actif par classes et compter combien tombent dans chacune,
  c'est construire une distribution observée — l'objet même du §3 de ce chapitre.
- **La fréquence cumulée, c'est la fonction de répartition empirique** — et donc le
  **quantile**. « 5 % des séances ont produit une perte supérieure à 2,3 % » est une
  lecture de fréquence cumulée. C'est la définition opérationnelle de la *Value at Risk* :
  la VaR à 95 % est le quantile à 5 % de la distribution des pertes. Vous saurez la
  calculer à la fin de ce chapitre, avant même d'avoir vu le mot.
- **« Présenter sans perte d'information » contre « résumer ».** Un backtest résumé à sa
  moyenne et à son écart-type efface précisément ce qui compte : les queues de
  distribution, les séries de pertes, la forme. Le chapitre 2 apprendra à résumer ; ce
  chapitre-ci apprend **ce que le résumé fait disparaître**. C'est la même erreur que juger
  une stratégie sur son rendement moyen sans regarder son *drawdown*.
- **Population et échantillon.** La dernière diapositive annonce la statistique
  inférentielle : déduire les propriétés d'une population à partir d'un échantillon tiré au
  hasard. C'est le problème central du backtest — un historique n'est qu'un échantillon de
  tous les marchés possibles, et en tirer des conclusions générales est un acte
  d'inférence, avec son risque d'erreur.
- **« Ce n'est pas le rapport statistique qui décide. »** La décision reste au décideur,
  informée par les chiffres et contrainte par autre chose — le coût, le mandat, le risque
  toléré. C'est très exactement la frontière entre un signal et une prise de position.
:::

<!--saut-->
## 2. Le cours reconstruit

L'ordre suit celui du support. Deux ajouts : les **réponses aux questions posées en
amphithéâtre** — elles n'existaient que dans l'oral — et la **vérification systématique des
chiffres**, qui a révélé une anomalie dans les données du cours (§2.3.4).

::: objectif Le programme annoncé par le support (diapositive 2)
**Contenu du chapitre**
- Découvrir la démarche de la statisticienne.
- Définitions essentielles : variables et type, population et unités statistiques.
- Présenter de façon pertinente les informations contenues dans les données.

**Plan du chapitre**
1. Réaliser une étude statistique.
2. Communiquer : le vocabulaire de la statisticienne.
3. Communiquer : la présentation des données.

*Remarque de forme : le titre de la section 2 est écrit « vocabulaire de la
statisticienne » dans le plan (diapo 2) et « vocabulaire du statisticien » sur la
diapositive de section (diapo 11). Aucune conséquence sur le fond.*
:::

### 2.1 — Section 1 : réaliser une étude statistique

#### 2.1.1 Pourquoi une étude statistique existe

::: formule La chaîne fondatrice
> **Besoin de décider → Besoin d'information → Étude statistique**
:::

Le sens de lecture est capital et se lit de gauche à droite : **on ne fait pas une étude
parce qu'on a des données, on la fait parce qu'on a une décision à prendre.** La décision
crée un besoin d'information ; le besoin d'information justifie l'étude. Inverser cet ordre
— partir des données disponibles pour chercher ce qu'on pourrait en dire — produit des
rapports inutiles.

Le support donne quatre exemples. Chacun illustre un type de décision différent.

| Exemple du support | La décision qui est en jeu derrière |
|---|---|
| Identifier les **populations à risque** afin d'optimiser une campagne de prévention | Où affecter un budget de santé publique limité |
| Connaître l'**évolution démographique** pour planifier le financement du système de retraite | Comment calibrer cotisations et prestations sur trente ans |
| Prévoir la **répartition d'une population selon des zones géographiques** pour planifier d'éventuels quotas de médecins | Combien de praticiens autoriser, et où |
| **Localiser des prospects** dans le but d'optimiser la ventilation des forces de vente | Où envoyer les commerciaux |

::: examen
Les deux premiers exemples relèvent de la **décision publique**, les deux derniers de la
**décision d'entreprise**. Le message est que la démarche statistique est **la même** dans
les deux cas — c'est la problématique qui change, pas la méthode. Une question de cours
peut demander de « donner deux exemples de situations appelant une étude statistique » :
donnez-en un de chaque camp.
:::

#### 2.1.2 Les six étapes d'une étude statistique (diapositive 4)

**La diapositive 4 ne contient aucun texte : c'est une image.** Voici ce qu'elle
représente, intégralement.

Six boîtes se succèdent, reliées par une flèche horizontale qui va de la gauche vers la
droite :

```
   [1] Quel type   →  [2] Choix des  →  [3] Choix de la  →  [4] Campagne  →  [5] Traitement      →  [6] Prise
       de problé-        données à         méthode de           de mesures      (présentation,          de
       matique ?         observer          recueil des                          résumé, etc.)       décision
                                           données                              des données
        ▲   ▲   ▲   ▲   ▲
        └───┴───┴───┴───┴──── flèches de retour, venant des étapes 2, 3, 4, 5 et 6

        « Tous les choix sont guidés par le type de problématique »
```

::: examen Le vrai contenu du schéma : les flèches de retour
La lecture naïve est « six étapes dans l'ordre ». C'est la moitié du message. L'autre
moitié est portée par les **cinq flèches de retour** qui remontent de chacune des étapes
suivantes vers l'étape 1, et par la légende encadrée : **« Tous les choix sont guidés par
le type de problématique »**.

Autrement dit : à chaque étape, on ne choisit pas « la meilleure méthode dans l'absolu »,
on choisit **celle qui répond à la problématique**. Il n'existe pas de bonne méthode de
recueil en soi, ni de bon diagramme en soi. Il n'y a que des méthodes **adaptées ou non à
la question posée**.

C'est la phrase à replacer dans toute copie de méthodologie, et le principe qui reviendra
au §2.3.7 pour le choix des diagrammes.
:::

#### 2.1.3 Étape 1 — Quel type de problématique ? (diapositive 5)

La question à poser au **donneur d'ordre** de l'étude : *quel type de problématique
l'intéresse ?*

**L'exemple du support.** Un directeur d'hypermarché demande une enquête de satisfaction
auprès de sa clientèle. Le support tranche : **« cette demande est beaucoup trop vague »**,
et énumère quatre problématiques possibles, toutes compatibles avec la demande initiale :

1. modifier la **mise en place des produits en rayon** ?
2. améliorer l'**affichage** des produits ?
3. mieux répondre aux attentes des clients en matière de **choix des produits** ?
4. mieux définir les attentes en matière d'**horaires d'ouverture** et de **conseil** ?

::: demo Pourquoi une demande vague rend l'étude impossible — et non seulement imprécise
Ce n'est pas une question de confort : chacune des quatre problématiques impose des choix
**incompatibles** aux étapes suivantes.

| Si la problématique est… | Étape 2 : qui observer ? | Étape 3 : comment recueillir ? |
|---|---|---|
| La mise en place en rayon | Les clients **en magasin**, au moment de l'achat | Observation directe des parcours, expérimentation sur un rayon test |
| Les horaires d'ouverture | Aussi les **non-clients** — ceux qui ne viennent pas parce que c'est fermé | Enquête téléphonique ou en ligne, hors magasin |

Interroger des clients **présents en magasin** sur les horaires d'ouverture ne peut pas
répondre à la question : par construction, on n'interroge que ceux pour qui les horaires
conviennent déjà. **La population à observer dépend de la problématique** ; se tromper de
problématique, c'est se tromper de population, et aucun traitement ultérieur ne rattrape
cette erreur.
:::

::: piege
La faute la plus fréquente sur cette étape, en copie : répondre « il faut préciser la
demande » sans montrer **pourquoi**. Le point n'est pas la précision pour elle-même, c'est
que **les étapes 2 à 6 sont indéterminées** tant que l'étape 1 ne l'est pas.
:::

#### 2.1.4 Étape 2 — Choix des données à observer : *qui ?* (diapositive 6)

La question de l'étape 2 est **« Qui ? »**. Le support énonce trois exigences :

- une fois défini l'**objet d'étude**,
- il faut définir sur quels **individus** ou **unités statistiques** les observations vont
  être réalisées,
- la **population** concernée devra être **définie, délimitée** — et **on connaît parfois
  sa taille, mais pas toujours**.

::: definition Définir et délimiter une population
**Définir** une population, c'est énoncer le critère d'appartenance : *qui* en fait partie.
**Délimiter**, c'est fixer les bornes concrètes — géographiques, temporelles, d'âge — qui
rendent le critère applicable.

Exemple : « les clients de l'hypermarché » est une définition. « Les personnes ayant
effectué au moins un achat dans le magasin de La Valentine entre le 1<sup>er</sup> janvier
et le 30 juin 2026 » est une population **délimitée** : on sait, pour chaque personne, dire
si elle en fait partie ou non.
:::

::: examen La remarque la plus importante de la diapositive
**« Parfois on connaît sa taille, mais pas toujours. »** Cette incise annonce toute la
statistique inférentielle (diapositive 33). Quand la taille de la population est inconnue
ou la population inaccessible — les clients potentiels, les fraudeurs, les électeurs du
prochain scrutin — on ne peut pas l'observer exhaustivement : il faudra **échantillonner**,
et accepter une marge d'erreur. Repérer cette phrase montre que vous avez vu le fil qui
relie la première section à la dernière diapositive.
:::

#### 2.1.5 Étape 3 — Choix de la méthode de recueil (diapositive 7)

La question : **comment obtenir les informations ?** Le support donne **quatre** méthodes.

| Méthode | Définition du support | Ce qu'elle permet | Sa limite |
|---|---|---|---|
| **Expérimentation** | On dispose d'un protocole permettant l'observation directe de l'impact d'une **variable de contrôle** sur une **variable d'observation** | Établir un lien de cause à effet, puisqu'on fait varier une seule chose | Coûteuse, souvent impossible en sciences sociales, artificielle |
| **Observation ou enquête qualitative** | On observe de façon **extensive** un **petit nombre** d'individus | Comprendre en profondeur des mécanismes, faire émerger des hypothèses | Ne permet pas de généraliser : trop peu d'individus |
| **Données de seconde main** | On réutilise des informations **disponibles par ailleurs** | Immédiat et peu coûteux (Insee, Ministères, bases internes) | Les données n'ont pas été produites pour votre problématique |
| **Enquête quantitative** | Travail **sur-mesure** : on collecte l'information utile par enquête, questionnaire, etc. | Colle exactement à la problématique, permet de quantifier | **L'option la plus coûteuse** (diapositive 8) |

::: methode Comment choisir — la grille de décision reconstruite
Le support liste les méthodes sans dire comment trancher. Les quatre questions à se poser,
dans l'ordre :

1. **Cherche-t-on une cause ou une description ?** Une cause → expérimentation. Une
   description → les trois autres.
2. **Cherche-t-on à comprendre ou à mesurer ?** Comprendre des mécanismes → qualitative.
   Mesurer une ampleur → quantitative.
3. **L'information existe-t-elle déjà ?** Si oui, données de seconde main : c'est presque
   toujours à essayer **en premier**, parce que c'est gratuit et immédiat.
4. **Le budget permet-il le sur-mesure ?** Si oui, et si les trois réponses précédentes
   l'exigent : enquête quantitative.

**Deux termes à ne pas confondre dans l'expérimentation :** la **variable de contrôle** est
celle que l'expérimentateur fait varier volontairement ; la **variable d'observation** est
celle dont il mesure la réaction. On agit sur la première pour observer la seconde.
:::

#### 2.1.6 Étape 4 — Campagne de mesures (diapositive 8)

Le support pose le cadre en une phrase : **en cas de choix d'enquête quantitative, c'est
l'option la plus coûteuse.** La campagne de mesures doit définir trois choses.

| Question | Ce qu'elle recouvre |
|---|---|
| **Combien** de personnes enquêter ? | La taille de l'échantillon : plus il est grand, plus la mesure est précise, plus elle coûte cher |
| **Quand** les enquêter ? | Le moment conditionne la réponse — un client interrogé un samedi après-midi et un mardi matin n'est pas le même |
| **Comment** les enquêter ? | Le canal : en face-à-face, par téléphone, en ligne, par voie postale — chacun atteint une population différente |

::: marche
« Combien, quand, comment » est un arbitrage **coût / précision**, exactement de même
nature qu'en gestion du risque : chaque unité de précision supplémentaire se paie, et le
gain marginal décroît. Doubler la taille d'un échantillon ne divise pas l'erreur par deux —
elle décroît en $ 1/\sqrt{n} $ ; il faut **quadrupler** l'échantillon pour diviser l'erreur
par deux. *(Ce résultat relève de la statistique inférentielle et sera démontré plus tard
dans le cursus ; il est cité ici pour montrer la nature de l'arbitrage, pas à restituer en
examen sur ce chapitre.)*
:::

#### 2.1.7 Étape 5 — Traitement des données (diapositive 9)

> « Une fois les données récoltées, vient le moment de **les faire parler**. »

Le support précise : **c'est l'objet du cours de Techniques statistiques**. Et il pose la
règle qui commande tous les traitements :

::: formule La règle du traitement
**Tous les traitements doivent être orientés pour extraire l'information répondant à la
problématique et utile à la prise de décision.**
:::

Quatre familles de traitements sont annoncées — c'est le **programme du cours entier**, à
connaître dès maintenant :

| Traitement | Ce qu'il fait | Où |
|---|---|---|
| **Présenter** les données **sans perte d'information** | Réorganiser sans rien jeter : tableaux, distributions, diagrammes | **CHAP 1 — ce chapitre** |
| **Résumer** l'information contenue dans les données, **variable par variable** | Réduire une distribution à quelques nombres : position, dispersion | CHAP 2 |
| S'intéresser aux **évolutions temporelles** | Suivre une variable dans le temps : séries, indices, taux de croissance | CHAP 3 |
| **Croiser** les informations de **plusieurs variables** | Étudier les liens entre variables : tableaux croisés, corrélation | CHAP 4 |

::: examen La distinction structurante du cours
**Présenter (CHAP 1) ≠ résumer (CHAP 2).** Présenter conserve **toute** l'information :
on peut reconstruire les données de départ. Résumer en **perd** volontairement : une
moyenne ne permet pas de retrouver la distribution.

Cette opposition est la clé de lecture du chapitre. Chaque fois que le support écrit
« sans perte d'information », il oppose implicitement le chapitre 1 au chapitre 2.
:::

#### 2.1.8 Étape 6 — Prise de décision (diapositive 10)

::: definition Ce que doit contenir un rapport statistique
Le support en donne la composition exacte :
- le **résultat des traitements statistiques**, bien sûr,
- mais aussi les **éléments méthodologiques** — les choix réalisés quant aux méthodes
  statistiques utilisées,
- le tout **orienté selon la problématique**, vers la prise de décision.
:::

Deux principes achèvent la section, et ce sont les deux plus cités en examen.

**Principe 1 — « Toute information inutile (non informative au regard de la problématique)
doit être bannie. »** Un rapport n'est pas un exercice d'exhaustivité. Un tableau qui
n'éclaire aucune décision **nuit** au rapport : il dilue l'attention du lecteur. Le critère
d'inclusion n'est pas « est-ce vrai ? » mais « est-ce que cela aide à décider ? ».

**Principe 2 — « Ce n'est pas le rapport statistique qui décide. »** Le support est
explicite : **toute décision est politique** et repose sur les informations collectées et
présentées dans le rapport, **ainsi que d'autres considérations ou contraintes comme le
coût**.

::: demo Pourquoi la statistique ne décide pas — le raisonnement complet
1. Une statistique établit **ce qui est** : des effectifs, des fréquences, des évolutions.
2. Une décision énonce **ce qu'il faut faire**. Elle suppose donc un **critère de choix** —
   une préférence, un objectif, une contrainte budgétaire.
3. Aucun tableau de chiffres ne contient de critère de choix : le passage de « ce qui est »
   à « ce qu'il faut faire » exige un jugement, extérieur aux données.
4. Ce jugement relève du décideur — d'où le mot **politique** employé par le support, au
   sens de « qui relève du gouvernement de la cité », et non au sens partisan.

**Formulation à retenir :** la statistique **éclaire** la décision, elle ne la **remplace**
pas. Une copie qui écrit « les chiffres montrent qu'il faut faire X » commet exactement
l'erreur que la diapositive 10 dénonce.
:::

<!--saut-->

### 2.2 — Section 2 : le vocabulaire de la statisticienne

#### 2.2.1 Les cinq définitions fondamentales (diapositive 11)

Tout le reste du cours repose sur ces cinq mots. Ils sont donnés dans l'ordre logique : on
part de l'ensemble, on descend vers l'élément, puis on décrit l'élément.

::: definition Le vocabulaire de base
- **Population** : l'**ensemble (mathématique) étudié**.
- **Individus** ou **unités statistiques** : les **éléments** de cette population.
- **Taille de la population** ou **effectif total** : le **nombre** d'individus ou d'unités
  statistiques.
- **Variable statistique** ou **caractère statistique** : une **application** associant à
  chaque individu une valeur.
- **Modalités** : les **valeurs prises** par une variable statistique.

**Convention d'écriture du cours :** les **variables** sont notées en **majuscule**, leurs
**valeurs prises** en **minuscule**.
:::

::: demo « Une application » : pourquoi ce mot et pas un autre
Le support écrit qu'une variable est une **application**. Le terme est mathématique et
lourd de conséquences.

Une application associe à **chaque** élément de l'ensemble de départ **une et une seule**
valeur dans l'ensemble d'arrivée. Traduit ici :

$$ X : \text{Population} \rightarrow \text{Modalités} $$

1. **« À chaque individu »** : aucun individu n'est laissé sans valeur. En pratique, les
   non-réponses doivent donc être traitées explicitement — soit exclues de la population,
   soit constituées en modalité « non renseigné ».
2. **« Une seule valeur »** : un individu ne peut pas présenter deux modalités à la fois
   pour une même variable. Si un questionnaire autorise plusieurs réponses (« quels sports
   pratiquez-vous ? »), ce n'est **pas une variable** au sens du cours, mais **plusieurs**
   variables binaires — une par sport.

C'est la raison pour laquelle les modalités d'une variable doivent toujours être
**exhaustives** (tout individu en a une) et **exclusives** (il n'en a qu'une).
:::

::: piege La confusion à éliminer immédiatement
**Variable ≠ modalité.** La variable est la **question posée** ; les modalités sont les
**réponses possibles**.

- Variable : « nombre de frères et sœurs ». Modalités : 0, 1, 2, 3…
- Variable : « sexe ». Modalités : « homme », « femme », « autre ».

Écrire « la modalité *nombre d'enfants* » est une faute qui se voit immédiatement, et qui
coûte des points à chaque occurrence.
:::

#### 2.2.2 Application : l'enquête « Vécu et ressenti en matière de sécurité » (diapositive 12)

Le support présente la répartition des infractions déclarées en France en 2024 et **pose
une question à l'amphithéâtre**. La réponse n'existe que dans l'oral du cours : la voici.

**Le tableau du support**

| Atteinte déclarée | Nombre d'infractions |
|---|---:|
| Actes de vandalisme contre la voiture | 2 893 000 |
| Vols ou tentatives de vol d'objet dans ou sur la voiture | 1 544 000 |
| Vols ou tentatives de vol avec effraction de la résidence principale | 1 516 000 |
| Actes de vandalisme contre le logement | 1 141 000 |
| Vols ou tentatives de vol de vélo | 853 000 |
| Vols sans effraction de la résidence principale | 616 000 |
| Vols ou tentatives de vol de voiture | 549 000 |
| Vols ou tentatives de vol de deux-roues motorisés | 264 000 |
| **Ensemble** | **9 376 000** |

*Champ : France métropolitaine, Martinique, Guadeloupe et La Réunion. Diffusion Insee.*

::: correction La question posée : population, unités statistiques, effectif total, variable, modalités
**Population.** L'ensemble des **infractions déclarées** en 2024 sur le champ indiqué
(France métropolitaine, Martinique, Guadeloupe, La Réunion).

**Unités statistiques.** **Une infraction déclarée.** C'est l'objet qui est compté ; chaque
ligne du tableau dénombre des infractions, pas des personnes.

**Effectif total.** $ n = 9\,376\,000 $ infractions. **Vérification par recomptage :**
$ 2\,893 + 1\,544 + 1\,516 + 1\,141 + 853 + 616 + 549 + 264 = 9\,376 $ (en milliers). ✔ La
ligne « Ensemble » est bien la somme des huit modalités.

**Variable.** Une seule : le **type d'atteinte déclarée**. Elle est **qualitative
nominale** — ses modalités sont des mots, et il n'existe aucun ordre qui ait un sens entre
« vandalisme contre la voiture » et « vol de vélo ».

**Modalités.** Les **huit** types d'atteinte listés.
:::

::: piege Deux pièges que cette illustration tend
**Piège 1 — l'unité statistique.** Il est tentant de répondre « la population, ce sont les
ménages français » ou « les personnes interrogées ». C'est faux **ici** : le tableau
totalise 9 376 000 **infractions**, pas 9 376 000 personnes. Un même ménage peut avoir subi
deux atteintes et compter deux fois. **Le test décisif : ce que compte la ligne
« Ensemble » est l'unité statistique.**

**Piège 2 — le classement décroissant.** Les modalités sont rangées de la plus fréquente à
la moins fréquente. Cet ordre est un **choix de présentation**, il ne rend pas la variable
ordinale. Une variable est ordinale quand l'ordre est **intrinsèque aux modalités**
(« mauvais < moyen < bon »), pas quand il résulte des effectifs observés.
:::

#### 2.2.3 Les types de variables (diapositive 13)

::: definition Deux types, quatre sous-types
**Les modalités de la variable qualitative ne sont pas des nombres.**
- **Nominale** : il **n'est pas possible** de classer les modalités selon un ordre qui a du
  sens.
- **Ordinale** : il **est possible** de classer les modalités selon un ordre qui a du sens.

**Les modalités de la variable quantitative sont des nombres.**
- **Discrète** : les modalités relèvent du **comptage** (ensemble dénombrable).
- **Continue** : les modalités relèvent de la **mesure** (ensemble non dénombrable).

**Avertissement du support :** *attention aux confusions, une variable qualitative peut
être codée dans une base de données sous forme de nombre, un mot valant un chiffre.*
:::

::: demo L'arbre de décision — comment trancher en trois questions
Pour qualifier n'importe quelle variable, posez ces trois questions **dans cet ordre**.

1. **Les modalités sont-elles des nombres qui ont un sens numérique ?**
   → Non : variable **qualitative**, aller en 2. Oui : **quantitative**, aller en 3.
2. **Les modalités peuvent-elles être classées selon un ordre qui a du sens ?**
   → Non : **qualitative nominale**. Oui : **qualitative ordinale**.
3. **Les valeurs relèvent-elles du comptage ou de la mesure ?**
   → Comptage : **quantitative discrète**. Mesure : **quantitative continue**.

**Le mot « qui ont un sens numérique » à l'étape 1 est décisif** : c'est lui qui bloque le
piège du codage.
:::

::: piege Le piège du codage numérique — développé
Une base de données code souvent le sexe par 1 = homme, 2 = femme. Le codage ne transforme
pas la nature de la variable. Le test qui tranche : **les opérations arithmétiques ont-elles
un sens ?**

- Sur des codes 1/2 : la moyenne vaut 1,5. Que signifie « le sexe moyen vaut 1,5 » ?
  **Rien.** → Variable **qualitative nominale**, codée numériquement.
- Sur un nombre d'enfants : la moyenne vaut 1,8 enfant. Cela a un sens. → Variable
  **quantitative**.

**Formulation à retenir** : un nombre qui n'est qu'une **étiquette** ne rend pas la
variable quantitative. La conséquence est lourde : on n'a pas le droit de calculer une
moyenne sur une variable qualitative, même codée en chiffres — c'est l'erreur
d'interprétation la plus répandue en statistique appliquée.
:::

::: piege Le cas limite : l'ordinale codée
« Qualité du service » codée 1 = mauvaise, 2 = plutôt mauvaise, 3 = plutôt bonne, 4 = très
bonne. L'ordre est réel, donc la variable est **qualitative ordinale**. Mais les écarts
entre codes **n'ont pas de sens** : rien ne garantit que l'écart entre « mauvaise » et
« plutôt mauvaise » soit le même qu'entre « plutôt bonne » et « très bonne ». On peut donc
**classer** les réponses, mais pas les **additionner**. C'est la frontière exacte entre
ordinale et quantitative, et c'est un excellent sujet de question piège.
:::

#### 2.2.4 Illustration des quatre types (diapositive 14)

Le support donne un exemple par sous-type — mais **sans indiquer le type** de chacun. Le
voici, complété et justifié.

| Caractère (variable) | Modalités données par le support | Type | Pourquoi |
|---|---|---|---|
| **Sexe** | « homme », « femme », « autre » | **Qualitative nominale** | Modalités non numériques, aucun ordre qui ait un sens |
| **Qualité du service** | « mauvaise », « plutôt mauvaise », « plutôt bonne », « très bonne » | **Qualitative ordinale** | Modalités non numériques, mais un ordre incontestable du pire au meilleur |
| **Nombre d'enfants** | 0, 1, 2, 3, 4, 5 | **Quantitative discrète** | Nombres issus d'un **comptage** ; entre 2 et 3, aucune valeur possible |
| **Taille en cm** | 179, 182, 183, 165, 148, 205, etc. | **Quantitative continue** | Nombres issus d'une **mesure** ; entre 179 et 180 il existe une infinité de valeurs |

::: examen
Cette diapositive est un exercice déguisé : les quatre exemples couvrent exactement les
quatre sous-types, dans l'ordre du tableau de la diapositive 13. **Une question d'examen
très probable donne quatre variables nouvelles et demande de les qualifier.** Entraînez-vous
sur : code postal, note sur 20, mention au baccalauréat, chiffre d'affaires, catégorie
socioprofessionnelle, âge, tranche d'âge, numéro de téléphone. *(Réponses au §5, niveau 2,
exercice 1.)*
:::

<!--saut-->
### 2.3 — Section 3 : la présentation des données

#### 2.3.1 Deux façons de présenter une variable (diapositive 15)

::: definition Les deux présentations, sans perte d'information
Il y a **deux grandes façons** de présenter une variable **sans perte d'information** :

- sous forme de **série** ou **données brutes** (en anglais : *raw data*) ;
- sous forme de **distribution observée des effectifs** (en anglais : *frequencies*).

**Le passage de l'une à l'autre demande un traitement** qui nécessite, dans le cas
quantitatif ou qualitatif ordinal : **un tri des modalités, puis un comptage des effectifs**.
:::

::: demo Pourquoi « sans perte d'information », et pourquoi le tri ne s'applique pas au nominal
**Pourquoi il n'y a pas de perte.** À partir du tableau des effectifs, on peut reconstruire
une série brute équivalente : il suffit d'écrire 11 fois la valeur 0, 33 fois la valeur 1,
etc. On ne retrouve pas l'**ordre** dans lequel les étudiants ont répondu — mais cet ordre
n'est pas de l'information statistique : il ne dit rien sur la variable étudiée. Tout ce
qui est statistiquement pertinent est conservé.

**Pourquoi le tri est réservé au quantitatif et au qualitatif ordinal.** Trier suppose un
ordre. Pour une variable **nominale**, aucun ordre n'a de sens : on peut compter les
effectifs, mais l'ordre des lignes du tableau est un pur choix de présentation (par ordre
alphabétique, par effectif décroissant…). C'est très exactement ce que fait le tableau des
infractions de la diapositive 12, rangé par effectif décroissant.
:::

#### 2.3.2 La distribution observée des effectifs (diapositive 16)

::: definition Distribution observée des effectifs
Une **distribution observée des effectifs** **associe à chaque modalité** d'une variable
statistique **l'effectif observé correspondant**.

L'**effectif d'une modalité** est le **nombre d'individus présentant une modalité donnée**
du caractère statistique.

La représentation d'une telle distribution peut être **un tableau** ou **un diagramme
colonne**.

**Il n'y a pas de perte d'information ; il s'agit souvent de l'étape n° 1 d'une analyse
statistique.**
:::

Notez la construction du mot : une distribution est une **application de second niveau**.
La variable associe une modalité à chaque individu ; la distribution associe un effectif à
chaque modalité. On passe de l'individu à la modalité, puis de la modalité au nombre.

#### 2.3.3 L'exemple des 87 étudiants (diapositives 17 à 20)

**L'énoncé.** Mini-enquête : **87 étudiants** d'une promotion ont répondu à la question
*« Combien avez-vous de frères et sœurs ? »*. Dans la population de l'ensemble des 87
étudiants — **taille de la population = 87 unités statistiques** — le caractère statistique
est **quantitatif discret**.

**Étape 1 — la série brute (diapositive 17).** Les 87 réponses, dans l'ordre où elles ont
été collectées :

```
 2   2   5   2    3   1   1   1    1   2   1   1   0   2   2
 5   1   4   2    2   1   0   2    2   1   2   1   1   2   1
 3   1   2   1    0   0   1   3   13   2   1   1   2   1   1
 1   6   1   3    1   0   1   5    7   2   1   2   2   3   0
 3   2   2   7   14   9   5   4    1   0   1   2   1   3   2
 1   2   2   0    4   1   0   1    0   1   1   1
```

**Étape 2 — la série ordonnée (diapositive 18).** On trie. La lecture devient possible :
on voit immédiatement le minimum (0), le maximum (14), et la concentration sur les petites
valeurs.

```
 0   1   1   1   2   2   2    5
 0   1   1   1   2   2   3    5
 0   1   1   1   2   2   3    5
 0   1   1   1   2   2   3    5
 0   1   1   1   2   2   3    6
 0   1   1   1   2   2   3    7
 0   1   1   1   2   2   3    7
 0   1   1   1   2   2   3    9
 0   1   1   1   2   2   4   13
 0   1   1   1   2   2   4   14
 0   1   1   1   2   2   4
```

**Étape 3 — le tableau de distribution (diapositive 19).** On compte.

| Nombre de frères et sœurs | Effectif |
|---|---:|
| 0 | 11 |
| 1 | 33 |
| 2 | 23 |
| 3 | 7 |
| 4 | 3 |
| 5 | 4 |
| 6 | 1 |
| 7 | 2 |
| 9 | 1 |
| 13 | 1 |
| 14 | 1 |
| **Ensemble** | **87** |

**Étape 4 — le diagramme colonne (diapositive 20).** La diapositive présente un diagramme
en colonnes : en abscisse, **toutes les valeurs entières de 0 à 14** ; en ordonnée,
l'effectif, gradué de 0 à 35 par pas de 5. Les colonnes décroissent fortement après la
valeur 1 (la plus haute, à 33), et les valeurs 8, 10, 11 et 12 apparaissent **avec une
colonne de hauteur nulle**.

::: examen Le détail du diagramme qui vaut un point
Les modalités 8, 10, 11 et 12 **n'existent pas dans les données** — aucun étudiant ne les a
déclarées — et pourtant elles **figurent sur l'axe**, avec une colonne vide.

C'est volontaire et c'est correct : pour une variable **quantitative**, l'axe des abscisses
est un **axe numérique**, et les distances doivent y être respectées. Supprimer les
modalités d'effectif nul rapprocherait visuellement 7 et 9, 7 et 13, et **déformerait la
forme de la distribution**.

Corollaire : pour une variable **qualitative**, il n'y a pas d'axe numérique, donc pas de
modalité vide à représenter, et l'ordre des colonnes est libre.
:::

#### 2.3.4 Vérification des données — une anomalie dans le support

::: piege Recomptage : la série brute et le tableau ne coïncident pas
J'ai recompté, valeur par valeur, la série brute reproduite ci-dessus (relevée sur la
diapositive 17 elle-même, et non sur une transcription).

| Modalité | Effectif obtenu en recomptant **la série brute** (diapo 17) | Effectif de **la série ordonnée** (diapo 18) et du **tableau** (diapo 19) |
|:---:|:---:|:---:|
| 0 | **10** | **11** |
| 1 | 33 | 33 |
| 2 | **24** | **23** |
| 3 | 7 | 7 |
| 4 | 3 | 3 |
| 5 | 4 | 4 |
| 6 | 1 | 1 |
| 7 | 2 | 2 |
| 9 | 1 | 1 |
| 13 | 1 | 1 |
| 14 | 1 | 1 |
| **Total** | **87** | **87** |

Les deux colonnes totalisent bien 87 : il ne manque aucune donnée. Mais **la série brute
contient un « 2 » de trop et un « 0 » de moins** par rapport à la série ordonnée et au
tableau, qui, eux, **concordent parfaitement entre eux**.

**Conclusion :** l'erreur est dans la **série brute de la diapositive 17** — l'un de ses
« 2 » devrait être un « 0 ». Le tableau des effectifs de la diapositive 19, lui, est
cohérent avec la série ordonnée de la diapositive 18.

**Conduite à tenir.** En examen, **utilisez le tableau du cours** (0 → 11 ; 2 → 23) :
c'est lui qui fait foi pour la correction, et il est cohérent avec la série ordonnée. Mais
signalez la coquille à l'enseignante — c'est une remarque qui montre que vous avez
réellement refait les calculs, ce que presque personne ne fait.

**Ce que cet incident enseigne** — et c'est la vraie leçon : *trier puis compter* n'est pas
une formalité. Le contrôle élémentaire consiste toujours à vérifier que **la somme des
effectifs égale l'effectif total** ; ici, ce contrôle passe dans les deux cas (87 = 87) et
ne suffit donc pas. Le seul contrôle qui détecte l'écart est le **recomptage modalité par
modalité**.
:::

#### 2.3.5 Répartition, fréquences et fréquences cumulées (diapositive 21)

::: definition Fréquence et fréquence cumulée
La distribution d'une variable statistique peut aussi se représenter sous forme de
**répartition des fréquences** : on associe à chaque modalité de la variable une
**fréquence**.

- La **fréquence** d'une modalité est la **proportion d'individus présentant une modalité
  donnée** du caractère statistique **dans la population totale** (en pourcent de la
  population).
- Un **camembert** ou un **diagramme en barres** peuvent être choisis pour une telle
  représentation.
- Pour un caractère **quantitatif**, la **fréquence cumulée** d'une modalité est la
  **proportion d'individus présentant une modalité donnée ou inférieure** dans la
  population.
:::

::: piege Pourquoi la fréquence cumulée est réservée au quantitatif — et une nuance
Le support précise « pour un caractère quantitatif », et la raison est logique : cumuler
suppose de parcourir les modalités **dans un ordre**. Sans ordre, « les modalités
inférieures » ne veut rien dire — on ne peut pas dire qu'un vol de vélo est « inférieur » à
un acte de vandalisme.

**Nuance à connaître :** le cumul a également un sens pour une variable **qualitative
ordinale** (« au plus *plutôt bonne* »), puisque l'ordre y est défini. La restriction du
support au quantitatif est une **simplification pédagogique** ; retenez la formulation du
cours, mais comprenez que le critère réel est l'existence d'un ordre, pas la nature
numérique des modalités.
:::

::: exemple Effectifs, fréquences et fréquences cumulées de l'exemple des 87 étudiants
Le support s'arrête aux effectifs. Voici la distribution complète — c'est l'exercice type
de l'examen.

| Modalité $ x_i $ | Effectif $ n_i $ | Fréquence $ f_i $ (%) | Fréquence cumulée $ F_i $ (%) |
|---:|---:|---:|---:|
| 0 | 11 | 12,64 | 12,64 |
| 1 | 33 | 37,93 | 50,57 |
| 2 | 23 | 26,44 | 77,01 |
| 3 | 7 | 8,05 | 85,06 |
| 4 | 3 | 3,45 | 88,51 |
| 5 | 4 | 4,60 | 93,10 |
| 6 | 1 | 1,15 | 94,25 |
| 7 | 2 | 2,30 | 96,55 |
| 9 | 1 | 1,15 | 97,70 |
| 13 | 1 | 1,15 | 98,85 |
| 14 | 1 | 1,15 | 100,00 |
| **Ensemble** | **87** | **100,00** | — |

**Détail de trois calculs, pour la méthode :**
1. $ f_1 = n_1 / n = 11/87 = 0{,}1264 $, soit **12,64 %** — la fréquence de la modalité 0.
2. $ f_2 = 33/87 = 0{,}3793 $, soit **37,93 %**.
3. $ F_3 = f_1 + f_2 + f_3 = 12{,}64 + 37{,}93 + 26{,}44 = 77{,}01 $ **%**.

**Trois phrases de lecture, à savoir produire :**
- *Fréquence :* « 37,93 % des 87 étudiants de la promotion déclarent avoir exactement un
  frère ou une sœur. »
- *Fréquence cumulée :* « 77,01 % des étudiants déclarent **au plus** deux frères et
  sœurs. »
- *Complément :* « Autrement dit, 22,99 % en déclarent **au moins trois** — car
  $ 100 - 77{,}01 = 22{,}99 $. »
:::

::: marche
La dernière ligne est exactement la mécanique d'un quantile. Lue à l'envers, la colonne des
fréquences cumulées répond à : « en dessous de quelle valeur se situent 5 % des
observations ? » Sur une distribution de rendements quotidiens, cette valeur porte un nom :
la *Value at Risk* à 95 %. Le calcul est le même que celui que vous venez de faire — la
seule différence est l'objet mesuré.
:::

#### 2.3.6 Illustration : la distribution du nombre d'enfants (diapositive 22)

**Le tableau du support**

| Modalités $ x_i $ | Effectifs $ n_i $ (en milliers) | Fréquences $ f_i $ (%) | Fréquences cumulées $ F(x_i) $ (%) |
|---|---:|---:|---:|
| 0 enfant | 8 225 | 48,0 | 48,0 |
| 1 enfant | 3 821 | 22,3 | 70,3 |
| 2 enfants | 3 449 | 20,1 | 90,4 |
| 3 enfants | 1 241 | 7,2 | 97,7 |
| 4 enfants et plus | 396 | 2,3 | 100,0 |
| **Ensemble** | **17 132** | **100,0** | — |

::: correction La question posée : population, caractère statistique, unités statistiques, et comment ces chiffres ont été calculés
**Population.** L'ensemble des **familles** enquêtées : 17 132 **milliers** de familles,
soit environ **17,1 millions** de familles.

**Unités statistiques.** **Une famille.**

**Effectif total.** $ n = 17\,132 $ milliers.

**Caractère statistique.** Le **nombre d'enfants** de la famille. Il est **quantitatif
discret**… avec une réserve, développée dans l'encadré suivant.

**Comment ont été calculés ces chiffres ?**
- **Les fréquences** : $ f_i = n_i / n $, exprimé en pourcentage.
  Vérification : $ 8\,225 / 17\,132 = 0{,}4801 $ → **48,0 %** ✔ ;
  $ 3\,821/17\,132 = 0{,}2230 $ → **22,3 %** ✔ ;
  $ 3\,449/17\,132 = 0{,}2013 $ → **20,1 %** ✔ ;
  $ 1\,241/17\,132 = 0{,}0724 $ → **7,2 %** ✔ ;
  $ 396/17\,132 = 0{,}0231 $ → **2,3 %** ✔.
- **Les fréquences cumulées** : $ F_k = f_1 + f_2 + \ldots + f_k $.
  $ 48{,}0 $ ; $ 48{,}0 + 22{,}3 = 70{,}3 $ ; $ + 20{,}1 = 90{,}4 $ ; $ + 7{,}2 = 97{,}7 $ ;
  $ + 2{,}3 = 100{,}0 $ ✔.
- **Contrôle de cohérence** : la somme des effectifs vaut
  $ 8\,225 + 3\,821 + 3\,449 + 1\,241 + 396 = 17\,132 $ ✔, et la dernière fréquence cumulée
  vaut exactement 100,0 % ✔.
:::

::: piege Trois remarques que le support laisse de côté
**1. « 17 132 familles » ou 17 132 **milliers** de familles ?** Le texte de la diapositive
annonce « enquête menée auprès de 17 132 familles », mais l'en-tête de colonne précise
« effectifs $ n_i $ **en milliers** ». Les deux ne peuvent pas être vrais simultanément :
la lecture correcte est **17 132 milliers de familles**, soit 17,1 millions — l'ordre de
grandeur d'un recensement, pas d'une enquête de terrain. **Retenez l'unité de la colonne.**

**2. La dernière modalité, « 4 enfants et plus », est une classe ouverte.** Ce n'est pas
une valeur unique mais un **regroupement**. Conséquence importante pour la suite du cours :
on ne peut pas calculer de moyenne exacte à partir de ce tableau, puisqu'on ignore ce que
vaut réellement « et plus ».

**3. Le caractère est-il vraiment discret ?** Oui, le nombre d'enfants relève du comptage.
Mais **regroupé en classes** comme ici, le tableau se manipule comme une distribution en
classes. La nuance sera exploitée au chapitre 2.
:::

#### 2.3.7 Formalisation (diapositive 23)

::: formule Les notations du cours
- Le caractère statistique est noté $ X $ ; les modalités $ x_i $ sont ordonnées de
  $ i = 1, \ldots, p $.
- À chaque modalité $ x_i $ correspond un effectif $ n_i $, et l'effectif total vaut
  $$ n = \sum_{i=1}^{p} n_i = n_1 + n_2 + \ldots + n_p $$
- Les **fréquences** $ f_i $, pour $ i = 1, \ldots, p $, sont calculées ainsi :
  $$ f_i = \frac{n_i}{n} $$
- Les **fréquences cumulées** $ F_k $, pour $ k = 1, \ldots, p $, sont telles que :
  $$ F_k = \sum_{i=1}^{k} f_i $$
:::

**Chaque symbole, un par un** — le support ne les explicite pas :

| Symbole | Ce qu'il désigne | Attention |
|:---:|---|---|
| $ X $ | La **variable** (majuscule, par convention du cours) | Ce n'est pas un nombre |
| $ x_i $ | La **i-ème modalité** (minuscule) | Les modalités sont **ordonnées** : $ x_1 < x_2 < \ldots < x_p $ |
| $ i $ | L'**indice** de la modalité, de 1 à $ p $ | Il ne numérote pas les individus |
| $ p $ | Le **nombre de modalités** | À ne jamais confondre avec $ n $ |
| $ n_i $ | L'**effectif** de la modalité $ x_i $ | Un nombre d'individus, donc entier |
| $ n $ | L'**effectif total** | $ n = \sum n_i $ |
| $ f_i $ | La **fréquence** de la modalité $ x_i $ | Entre 0 et 1 (ou en %) |
| $ F_k $ | La **fréquence cumulée** jusqu'à la modalité $ x_k $ | Croissante, de $ f_1 $ à 1 |

::: demo Trois propriétés à savoir démontrer
**Propriété 1 — la somme des fréquences vaut 1.**
$$ \sum_{i=1}^{p} f_i = \sum_{i=1}^{p} \frac{n_i}{n} = \frac{1}{n} \sum_{i=1}^{p} n_i = \frac{n}{n} = 1 $$
*Justification de chaque étape :* on remplace $ f_i $ par sa définition ; comme $ n $ ne
dépend pas de $ i $, on le sort de la somme ; la somme des effectifs vaut $ n $ par
définition ; le quotient vaut 1. **En pourcentage : 100 %.**

**Propriété 2 — la dernière fréquence cumulée vaut 1.**
$ F_p = \sum_{i=1}^{p} f_i = 1 $ d'après la propriété 1. C'est le **contrôle systématique**
d'un tableau de fréquences cumulées : la dernière ligne doit valoir 100 % (aux arrondis
près).

**Propriété 3 — les fréquences cumulées sont croissantes.**
$ F_k - F_{k-1} = f_k \ge 0 $, puisqu'une fréquence est toujours positive ou nulle. Donc
$ F_k \ge F_{k-1} $ : **la suite des fréquences cumulées ne peut jamais décroître.** Une
colonne de fréquences cumulées qui diminue signale immédiatement une erreur de calcul.
:::

::: examen
Le support annonce : *« À présent amusons-nous à mettre les notations mathématiques en
adéquation avec l'illustration de la diapo 21 »* — il s'agit du **tableau des 17 132
milliers de familles** (diapositive 22 dans la numérotation du PDF). La correspondance :
$ p = 5 $ modalités ; $ x_1 = 0 $ enfant, …, $ x_5 = $ 4 enfants et plus ;
$ n_1 = 8\,225 $ ; $ n = 17\,132 $ ; $ f_1 = n_1/n = 48{,}0 $ % ; $ F_3 = 90{,}4 $ %.

**Sachez faire cet aller-retour dans les deux sens** : d'un tableau vers les notations, et
d'une formule vers sa traduction en français. C'est la compétence la plus régulièrement
testée sur ce chapitre.
:::

<!--saut-->
#### 2.3.8 Plusieurs distributions d'un même caractère (diapositive 24)

::: definition Le principe de la comparaison
- Il arrive **fréquemment** que **plusieurs distributions statistiques d'un même caractère**
  soient présentées **simultanément**, dans une **optique comparative**.
- Plusieurs **populations** (ou **sous-populations**) sont définies **selon une autre
  variable** — par année, par zone géographique, etc.
- Il y a en fait **une distribution par sous-population**. Ces distributions sont
  présentées **juxtaposées**.
- **Le but d'une telle présentation est la comparaison de la répartition de la variable
  entre sous-populations.**
:::

::: demo Ce qui se passe réellement : deux variables, pas une
Une comparaison de distributions met en jeu **deux variables**, et c'est ce que le support
dit en une ligne (« sous-populations définies selon une autre variable »).

1. La variable **étudiée** — celle dont on regarde la distribution : la catégorie pénale,
   le nombre d'enfants.
2. La variable **de découpage** — celle qui définit les sous-populations : l'année, la
   région, le sexe.

On construit alors **une distribution de la première variable à l'intérieur de chaque
modalité de la seconde**, et on les juxtapose. C'est déjà, en germe, le croisement de deux
variables qui fera l'objet du **chapitre 4** : ici on se contente de juxtaposer et de
comparer visuellement.

**Conséquence pratique immédiate :** on ne compare que ce qui est comparable. Si les
sous-populations n'ont pas la même taille, la comparaison des **effectifs** est trompeuse
et il faut comparer les **fréquences**. C'est exactement la raison d'être du diagramme
empilé à 100 % (§2.3.11).
:::

#### 2.3.9 Premier exemple : les personnes écrouées en France (diapositive 25)

**Le tableau du support** — Distribution des personnes écrouées en France, par année.

| Catégorie | 2020 | 2021 | 2022 | 2023 |
|---|---:|---:|---:|---:|
| Prévenus détenus | 17 692 | 18 486 | 18 779 | 19 755 |
| Condamnés-prévenus détenus | 2 405 | 2 613 | 2 908 | 3 117 |
| Condamnés détenus | 41 553 | 47 246 | 49 338 | 51 746 |
| Condamnés non détenus | 12 184 | 13 644 | 14 286 | 15 453 |
| **Total des personnes écrouées** | **73 834** | **81 989** | **85 311** | **90 071** |

*Source : Ministère de la justice.*

::: correction La question posée : population, sous-populations, caractère, type
**Population.** L'ensemble des **personnes écrouées en France**. *(Être « écroué » signifie
être inscrit au registre d'écrou d'un établissement pénitentiaire — ce qui n'implique pas
nécessairement d'être détenu, comme le montre la dernière catégorie.)*

**Unités statistiques.** **Une personne écrouée.**

**Sous-populations.** Les personnes écrouées **de chaque année** : 2020, 2021, 2022, 2023.
La variable de découpage est donc l'**année**.

**Caractère statistique étudié.** La **catégorie pénale** de la personne écrouée, à quatre
modalités : prévenus détenus, condamnés-prévenus détenus, condamnés détenus, condamnés non
détenus.

**Type.** **Qualitative nominale.** Les modalités sont des situations juridiques, non des
nombres, et aucun ordre naturel ne les hiérarchise.

**Contrôle des données.** La somme des quatre catégories redonne exactement le total de
chaque année : $ 17\,692 + 2\,405 + 41\,553 + 12\,184 = 73\,834 $ ✔ ; de même pour 2021
(81 989), 2022 (85 311) et 2023 (90 071) ✔.
:::

::: methode Lire la structure derrière les modalités — remarque hors support
Les quatre modalités croisent en réalité deux dimensions : le **statut judiciaire**
(prévenu, c'est-à-dire en attente de jugement / condamné) et la **détention** (détenu / non
détenu). On devrait donc attendre quatre combinaisons — mais « prévenu non détenu »
n'existe pas ici, puisqu'une personne prévenue et libre n'est pas écrouée. C'est la
population elle-même qui exclut cette modalité.

Repérer ce genre de structure aide à mémoriser une nomenclature et à ne pas confondre les
catégories.
:::

::: examen Ce que dit la dernière puce de la diapositive
Le support écrit : *« Le choix du diagramme colonne groupé dépend de la comparaison [qui]
est au centre de l'analyse… »* — la phrase est tronquée sur la diapositive, mais le sens
est sans ambiguïté et c'est **la règle du chapitre** : **le diagramme ne se choisit pas
pour lui-même, il se choisit en fonction de la comparaison que l'on veut faire voir.**
C'est la déclinaison graphique du principe des six étapes : tous les choix sont guidés par
la problématique.
:::

#### 2.3.10 Les deux diagrammes en colonnes groupées (diapositives 26 et 27)

Les deux diagrammes contiennent **exactement les mêmes chiffres**. Seul le **groupement**
change — et il change complètement ce que l'œil perçoit.

::: definition Diagramme en colonnes groupées 1 — groupement par catégorie (diapo 26)
**Titre du support :** « Évolution, pour chaque catégorie, du nombre de personnes écrouées
en France ».

**Construction.** Quatre groupes en abscisse, un par **catégorie pénale**. Dans chaque
groupe, quatre colonnes, une par **année** (2020, 2021, 2022, 2023, distinguées par un
dégradé de bleus, du plus foncé au plus clair). Axe des ordonnées : effectifs, de 0 à
60 000.

**Ce que l'œil voit immédiatement :** l'**évolution dans le temps, catégorie par
catégorie** — chaque groupe montre quatre barres qui montent régulièrement.
:::

::: definition Diagramme en colonnes groupées 2 — groupement par année (diapo 27)
**Titre du support :** « Évolution, pour chaque année, des catégories de personnes écrouées
en France ».

**Construction.** Quatre groupes en abscisse, un par **année**. Dans chaque groupe, quatre
colonnes, une par **catégorie**.

**Ce que l'œil voit immédiatement :** la **structure de la population une année donnée** —
et la comparaison de cette structure d'une année à l'autre.
:::

::: examen La règle de choix — à savoir énoncer et appliquer
Le support la donne en une phrase par diapositive :

| Si la question porte sur… | Grouper par… | Le regard compare alors… |
|---|---|---|
| **« l'évolution des effectifs de chaque catégorie »** | **catégorie** (diapo 26) | Les **années** entre elles, à l'intérieur d'une catégorie |
| **« l'évolution de la structure des effectifs »** | **année** (diapo 27) | Les **catégories** entre elles, à l'intérieur d'une année |

**La règle générale**, qui vaut pour tout diagramme groupé : **ce que l'on met en groupe est
ce que l'on veut voir comme un bloc ; ce que l'on met à l'intérieur du groupe est ce que
l'on veut comparer.** L'œil compare spontanément les barres **voisines** — donc celles qui
sont dans le même groupe.
:::

::: exemple Ce que chacun des deux diagrammes permet de dire
**Avec le diagramme 1 (groupé par catégorie).** « Entre 2020 et 2023, les condamnés détenus
passent de 41 553 à 51 746, soit **+10 193 personnes (+24,5 %)** ; c'est la catégorie qui
progresse le plus en volume. »

**Avec le diagramme 2 (groupé par année).** « En 2020 comme en 2023, les condamnés détenus
représentent la catégorie la plus nombreuse — **56,3 % du total en 2020, 57,5 % en 2023** —
tandis que les condamnés-prévenus détenus restent marginaux, autour de **3 %**. »

Le premier énoncé est une **évolution** ; le second une **structure**. Les deux sont vrais,
tirés du même tableau, et répondent à deux questions différentes.
:::

#### 2.3.11 Second exemple : le nombre d'enfants par famille (diapositives 28 à 31)

**Le tableau du support** — Distribution du nombre d'enfants par famille (en milliers), par
année.

| Nombre d'enfants mineurs | 1990 | 1999 | 2007 | 2012 | 2017 | 2023 |
|---|---:|---:|---:|---:|---:|---:|
| 1 enfant | 3 353,7 | 3 418,3 | 3 565,0 | 3 614,8 | 3 590,7 | 3 578,3 |
| 2 enfants | 2 800,5 | 2 841,1 | 2 996,3 | 3 074,1 | 3 101,1 | 3 039,0 |
| 3 enfants | 1 087,1 | 1 033,5 | 1 015,2 | 1 022,3 | 1 012,2 | 956,2 |
| 4 enfants ou plus | 410,9 | 334,5 | 296,9 | 296,1 | 310,7 | 308,4 |
| **Ensemble** | **7 652,2** | **7 627,5** | **7 873,5** | **8 007,3** | **8 014,7** | **7 881,9** |

*Champ : France hors Mayotte, familles vivant en ménage ordinaire ayant au moins un enfant
mineur. Unité : milliers de familles. Source : Insee, recensements de la population.*

::: correction Les questions posées : population, sous-populations, caractère, type, et une phrase de lecture
**Population.** Les **familles vivant en ménage ordinaire, ayant au moins un enfant
mineur**, en France hors Mayotte. Le **champ** est ici essentiel : les familles sans enfant
mineur sont **exclues** par construction.

**Unités statistiques.** **Une famille.**

**Sous-populations.** Les familles de chaque **année de recensement** : 1990, 1999, 2007,
2012, 2017, 2023. Variable de découpage : l'**année**.

**Caractère statistique.** Le **nombre d'enfants mineurs** de la famille.

**Type.** **Quantitative discrète** — un comptage. Avec la même réserve que précédemment :
la dernière modalité, « 4 enfants ou plus », est une **classe ouverte**, ce qui interdit
tout calcul exact de moyenne.

**Exemple de lecture.** *« En 2023, 3 578,3 milliers de familles — soit environ 3,58
millions — vivant en ménage ordinaire en France hors Mayotte et comptant au moins un enfant
mineur avaient exactement un enfant mineur. »*

**Contrôle.** La somme de chaque colonne redonne bien la ligne « Ensemble », au dixième
près : pour 1999, $ 3\,418{,}3 + 2\,841{,}1 + 1\,033{,}5 + 334{,}5 = 7\,627{,}4 $ contre
7 627,5 annoncé — l'écart de 0,1 vient des **arrondis** des données publiées, et non d'une
erreur.
:::

::: piege Le champ interdit une comparaison qui vient naturellement à l'esprit
Il est tentant de rapprocher ce tableau de celui de la diapositive 22 (17 132 milliers de
familles, dont **48 % sans enfant**). **C'est illégitime :** les deux populations ne sont
pas les mêmes. Celui-ci exclut les familles sans enfant mineur ; l'autre les inclut.

**Règle générale : avant toute comparaison de deux tableaux, comparez d'abord leurs
champs.** Deux distributions ne se comparent que si elles portent sur des populations
définies de la même façon. C'est l'erreur d'interprétation la plus fréquente sur données
publiées, et elle passe complètement inaperçue si l'on ne lit pas les notes de bas de
tableau.
:::

::: definition Diagramme empilé — en effectifs (diapositive 29)
**Titre du support :** « Évolution du nombre d'enfants par type de famille, par année ».
Le support précise : **« la hauteur de l'empilement correspond à l'ensemble des enfants
chaque année »**.

**Construction.** Une colonne par année (1990, 1999, 2007, 2012, 2017, 2023). Chaque
colonne est découpée en quatre segments superposés — 1 enfant, 2 enfants, 3 enfants,
4 enfants ou plus — dont la **hauteur est proportionnelle à l'effectif**, les valeurs étant
inscrites dans les segments (3 354 / 2 801 / 1 087 / 411 pour 1990, etc.).

**Ce que l'œil voit :** **deux informations à la fois** — la **hauteur totale** de chaque
colonne (l'effectif total de l'année) **et** la composition interne.
:::

::: definition Diagramme empilé à 100 % (diapositive 30)
Le support énonce le principe : *« Dans une optique comparative des structures des familles
dans le temps, on peut procéder à un empilement à 100 %, ce qui revient à prendre **les
fréquences et non les effectifs**, par année. »*

**Titre du support :** « Répartition du nombre d'enfants par famille, par année ».

**Construction.** Toutes les colonnes ont la **même hauteur** (100 %). Chaque segment
représente la **fréquence** de la modalité **dans l'année considérée**.

| Année | 1 enfant | 2 enfants | 3 enfants | 4 enfants ou plus |
|---|---:|---:|---:|---:|
| 1990 | 43,8 | 36,6 | 14,2 | 5,4 |
| 1999 | 44,8 | 37,2 | 13,5 | 4,4 |
| 2007 | 45,3 | 38,1 | 12,9 | 3,8 |
| 2012 | 45,1 | 38,4 | 12,8 | 3,7 |
| 2017 | 44,8 | 38,7 | **12,6** | 3,9 |
| 2023 | 45,4 | 38,6 | 12,1 | 3,9 |
:::

::: correction Les deux questions posées sur la diapositive 30
**1. Écrire une phrase de lecture.**
> « En 2017, **12,6 %** des familles vivant en ménage ordinaire en France hors Mayotte et
> comptant au moins un enfant mineur avaient **exactement trois enfants mineurs**. »

Les trois éléments obligatoires d'une phrase de lecture : **l'année** (la sous-population),
**la valeur avec son unité** (12,6 %), et **la modalité complète avec son champ** (trois
enfants mineurs, parmi les familles ayant au moins un enfant mineur).

**2. Comment a été calculé le chiffre 12,6 ?**
C'est la **fréquence** de la modalité « 3 enfants » **dans la sous-population de l'année
2017** :

$$ f_{3\text{ enfants, }2017} = \frac{n_{3\text{ enfants, }2017}}{n_{2017}} = \frac{1\,012{,}2}{8\,014{,}7} = 0{,}12629\ldots $$

soit **12,63 %**, arrondi à **12,6 %**.

**Les deux erreurs à ne pas commettre :**
- diviser par l'effectif total **de toutes les années** confondues : chaque colonne est
  ramenée à 100 % **séparément** ;
- diviser par l'effectif d'une autre année. Le dénominateur est **toujours** l'effectif de
  la sous-population à laquelle appartient le numérateur.
:::

::: examen Empilé simple ou empilé à 100 % — la règle de choix
| Si la question porte sur… | Diagramme | Ce qu'on perd |
|---|---|---|
| Les **volumes** et leur évolution (« combien de familles ? ») | **Empilé en effectifs** (diapo 29) | La comparaison des structures est difficile à l'œil, car les colonnes n'ont pas la même hauteur |
| La **structure** et son évolution (« quelle part ? ») | **Empilé à 100 %** (diapo 30) | **Toute information sur les volumes** : une colonne de 100 % peut représenter 8 millions de familles ou 800 |

**La conséquence la plus importante :** un empilement à 100 % peut montrer une part
**stable** alors que les effectifs **s'effondrent**, ou une part qui **baisse** alors que
l'effectif **augmente**. C'est le procédé de présentation le plus trompeur du chapitre —
et c'est pourquoi on ne le publie jamais sans donner, à côté, l'effectif total de chaque
colonne.
:::

::: exemple Le piège rendu concret sur les données du cours
Entre 2017 et 2023, la part des familles à 3 enfants passe de 12,6 % à 12,1 % : **−0,5
point**. Mais l'effectif, lui, passe de 1 012,2 à 956,2 milliers de familles :
**−56 000 familles, soit −5,5 %**.

Le diagramme à 100 % suggère une quasi-stabilité ; les effectifs révèlent une baisse dix
fois plus marquée en proportion. **Les deux lectures sont exactes** : elles ne répondent
simplement pas à la même question. La phrase à retenir : *une part stable dans un total qui
diminue signifie un effectif qui diminue.*
:::

::: definition Le diagramme de la diapositive 31
**Titre du support :** « Répartition du nombre d'enfants par famille, par année ». Le
support précise : **« ce diagramme colonne a le même contenu informationnel que le tableau
précédent »**.

**Construction.** Cinq colonnes, une par année — **1975, 1982, 1990, 1999, 2008** — toutes
de même hauteur (empilement à 100 %), en **cinq** segments, car cette fois la modalité
**« 0 enfant »** est présente.

| Année | 0 enfant | 1 enfant | 2 enfants | 3 enfants | 4 enfants et plus |
|---|---:|---:|---:|---:|---:|
| 1975 | 37,0 | 25,3 | 20,2 | 9,8 | 7,7 |
| 1982 | 38,4 | 25,1 | 22,1 | 9,4 | 5,0 |
| 1990 | 42,1 | 23,8 | 21,7 | 8,8 | 3,5 |
| 1999 | 45,8 | 22,8 | 20,5 | 8,0 | 2,9 |
| 2008 | **48,0** | **22,3** | **20,1** | **7,2** | **2,3** |
:::

::: methode Résoudre l'ambiguïté : de quel « tableau précédent » s'agit-il ?
Le renvoi est ambigu : le tableau qui précède immédiatement (diapositive 28) porte sur
1990-2023 et **exclut** les familles sans enfant, alors que ce diagramme couvre 1975-2008 et
**inclut** la modalité « 0 enfant ».

**La colonne 2008 tranche la question.** Ses cinq valeurs — 48,0 ; 22,3 ; 20,1 ; 7,2 ;
2,3 — sont **exactement** les fréquences du tableau de la **diapositive 22** (les 17 132
milliers de familles). Le renvoi désigne donc ce tableau-là, et non celui de la diapositive
28.

**Ce que cette identification apprend en plus du cours :** l'enquête de la diapositive 22
porte sur l'année **2008**, information que la diapositive ne donnait pas. Le diagramme de
la diapositive 31 en est la **série longue** : il montre l'évolution, sur trente-trois ans,
de la répartition dont la diapositive 22 ne donnait qu'une coupe.

*(Il s'agit d'une déduction établie par comparaison des chiffres, non d'une information
écrite dans le support. Elle est cohérente à la décimale près sur les cinq modalités.)*

**Lecture d'ensemble.** Entre 1975 et 2008, la part des familles sans enfant passe de
37,0 % à 48,0 % (**+11 points**) tandis que celle des familles de quatre enfants et plus
tombe de 7,7 % à 2,3 % (**divisée par plus de trois**). Contrôle : chaque colonne totalise
100 % (99,9 % en 1990 et 2008, effet d'arrondi).
:::

#### 2.3.12 Les règles de présentation (diapositive 32)

::: formule Le principe
**La présentation des données sous forme de tableau ou de graphique sert à informer,
c'est-à-dire donner une forme, une signification à des données** (le plus souvent
numériques brutes). **Les tableaux ou graphiques produisent de l'information, ils sont des
outils de communication.** Il est **primordial de les choisir et de les intituler à bon
escient** pour que l'information utile passe.
:::

**Les quatre règles du support**, et ce qu'elles interdisent concrètement :

| Règle | Ce qu'elle exige | Ce qu'elle interdit |
|---|---|---|
| **Intitulés précis** | Des titres explicites, sans noms de variables ou de modalités obscurs | « VAR_03 », « CSP4 », « Q12b » — les noms de colonnes de la base de données |
| **Lisibles par un non-spécialiste** | Un lecteur non statisticien doit comprendre | Le jargon technique dans un titre de graphique |
| **Compréhension immédiate ou simplifiée au maximum** ; si complexité : **note de lecture** en bas de tableau | Une phrase de lecture pour tout tableau non trivial | Laisser le lecteur deviner comment lire une cellule |
| **Indiquer les unités de mesure, la population, les choix méthodologiques** | Champ, unité, source, méthode | Un tableau de nombres sans unité — le cas de « 17 132 » de la diapositive 22 |

::: examen L'origine du mot « informer »
Le support insiste : informer, c'est **« donner une forme »**. Le mot vient du latin
*informare*, « façonner, donner une forme ». Ce n'est pas une coquetterie
étymologique — c'est la thèse du chapitre : **des données brutes ne sont pas de
l'information ; elles le deviennent quand une présentation leur donne une forme
interprétable.** Le titre du chapitre, « Présenter pour informer », dit exactement cela.

C'est une phrase d'introduction ou de conclusion parfaite pour une copie.
:::

### 2.4 — Remarques conclusives (diapositive 33)

::: synthese Le bilan du chapitre, selon le support
- Nous venons de voir les **principales étapes d'une étude statistique**.
- Nous avons appris à présenter la distribution d'un caractère statistique d'une population
  **en effectifs, en fréquences ou en fréquences cumulées**.
- Il s'agit souvent de la **première étape** de différents traitements de statistique
  descriptive, étudiés dans les chapitres suivants.
:::

**L'ouverture.** Le support conclut sur une limite de tout ce qui précède :

> « Nous ne disposons pas toujours de l'information exhaustive sur une population
> d'intérêt. Il faut parfois tirer aléatoirement un échantillon. Les techniques
> statistiques permettant de déduire des éléments d'une population à partir d'un
> échantillon aléatoire relèvent de la **statistique inférentielle**. »

::: definition Statistique descriptive et statistique inférentielle
| | **Statistique descriptive** | **Statistique inférentielle** |
|---|---|---|
| **Sur quoi elle porte** | La population **observée en entier** (ou les données dont on dispose, prises pour elles-mêmes) | Une **population** que l'on n'observe pas, à partir d'un **échantillon** |
| **Ce qu'elle produit** | Une **description certaine** de ce qui a été observé | Une **estimation**, assortie d'une **marge d'erreur** et d'un **degré de confiance** |
| **Le risque** | Aucun risque d'erreur d'inférence : on décrit ce qu'on a | Un risque de se tromper, que l'on **quantifie** |
| **Où** | Ce cours, chapitres 1 à 4 | La suite du cursus |

**Le mot clé est « aléatoirement ».** Un échantillon ne permet de conclure sur la population
que s'il a été **tiré au hasard** : c'est le tirage aléatoire qui rend l'échantillon
représentatif *en probabilité* et qui autorise le calcul d'une marge d'erreur. Un
échantillon de volontaires ou de personnes faciles à atteindre ne le permet pas.
:::

::: marche
La distinction descriptive / inférentielle est **le** problème du backtest. Décrire la
performance passée d'une stratégie sur 2004-2025 est de la statistique **descriptive** :
c'est exact, sans risque d'erreur, et cela ne dit rien de l'avenir. Affirmer que cette
performance se reproduira est une **inférence** — on traite l'historique comme un
échantillon tiré de l'ensemble des marchés possibles. Et cet échantillon n'est
précisément **pas** tiré au hasard : il est daté, contingent, marqué par des régimes de
marché particuliers. C'est pourquoi la découpe en périodes d'apprentissage et de contrôle
(*train / test*) existe : c'est une tentative de rétablir les conditions d'une inférence
valide. Vous manipulez déjà cette distinction ; ce cours lui donne son nom.
:::

<!--saut-->
## 3. Points de vigilance

### 3.1 — Les confusions classiques

Douze couples de notions voisines. Pour chacun, **le critère qui tranche**.

| Notion A | Notion B | Le critère qui les sépare |
|---|---|---|
| **Variable** | **Modalité** | La variable est la **question posée** ; la modalité est la **réponse possible**. « Nombre d'enfants » est la variable, « 3 » une modalité |
| **Individu** | **Population** | L'individu est l'**élément**, la population l'**ensemble**. Le test : ce que compte la ligne « Ensemble » d'un tableau est l'individu |
| **Effectif $ n_i $** | **Fréquence $ f_i $** | L'effectif est un **nombre d'individus** (entier) ; la fréquence une **proportion** ($ f_i = n_i/n $, entre 0 et 1) |
| **Fréquence** | **Fréquence cumulée** | La fréquence répond à « **exactement** cette modalité » ; la cumulée à « **au plus** cette modalité » |
| **Effectif total $ n $** | **Nombre de modalités $ p $** | $ n $ compte les **individus**, $ p $ les **valeurs distinctes**. Pour les 87 étudiants : $ n = 87 $, $ p = 11 $ |
| **Qualitative nominale** | **Qualitative ordinale** | L'existence d'un **ordre qui a du sens** entre les modalités |
| **Qualitative codée en chiffres** | **Quantitative** | La **moyenne a-t-elle un sens ?** « Sexe moyen = 1,5 » n'en a pas → qualitative |
| **Quantitative discrète** | **Quantitative continue** | **Compter** ou **mesurer**. Entre deux valeurs voisines, une valeur intermédiaire a-t-elle un sens ? |
| **Série brute** | **Distribution des effectifs** | La série liste **un individu par case** ; la distribution liste **une modalité par ligne** avec son effectif. On passe de l'une à l'autre par **tri puis comptage**, sans perte |
| **Présenter (CHAP 1)** | **Résumer (CHAP 2)** | Présenter **conserve toute** l'information ; résumer en **perd** volontairement |
| **Diagramme groupé par catégorie** | **Diagramme groupé par année** | Ce qui est **dans le même groupe** est ce que l'œil compare. Groupé par catégorie → on voit l'**évolution** ; groupé par année → on voit la **structure** |
| **Empilé en effectifs** | **Empilé à 100 %** | Le premier conserve les **volumes** (hauteurs inégales) ; le second ne montre que la **structure** (hauteurs égales) et **détruit** l'information de volume |
| **Statistique descriptive** | **Statistique inférentielle** | La descriptive **décrit ce qui a été observé** ; l'inférentielle **estime** ce qu'on n'a pas observé, à partir d'un échantillon **aléatoire**, avec une marge d'erreur |

### 3.2 — Les erreurs que commet la majorité des étudiants

1. **Confondre l'unité statistique avec « les gens ».** Dans le tableau des infractions, la
   population n'est pas faite de personnes mais d'**infractions**. Le test : ce que totalise
   la ligne « Ensemble ».
2. **Calculer une moyenne sur une variable qualitative codée en chiffres.** Un code n'est
   pas une quantité.
3. **Oublier la ligne « Ensemble » ou le total dans un tableau.** C'est l'unique contrôle
   qui détecte une erreur de comptage — et il n'est pas suffisant (§2.3.4).
4. **Diviser par le mauvais dénominateur** dans un empilé à 100 % : chaque colonne est
   ramenée à 100 % **avec son propre total**.
5. **Comparer deux tableaux dont les champs diffèrent** — familles avec et sans enfant, par
   exemple. Lire le champ **avant** les chiffres.
6. **Lire une part comme un volume.** Une part stable dans un total qui baisse est un
   effectif qui baisse.
7. **Écrire « les chiffres montrent qu'il faut… ».** Le rapport statistique n'a jamais
   décidé de rien : la décision est politique (diapositive 10).
8. **Supprimer d'un diagramme quantitatif les modalités d'effectif nul.** Cela déforme la
   forme de la distribution : l'axe des abscisses est un axe numérique.
9. **Confondre le tri et le comptage.** « Trier puis compter » est une séquence en deux
   temps ; sauter le tri sur une variable quantitative conduit aux oublis exacts de la
   diapositive 17.
10. **Donner une phrase de lecture incomplète.** Une lecture correcte comporte toujours la
    **sous-population** (l'année), la **valeur avec son unité**, et la **modalité avec son
    champ**.

### 3.3 — Ce qui sépare une copie moyenne d'une excellente copie

| La copie moyenne | La copie excellente |
|---|---|
| Énumère les six étapes | Cite les six étapes **et** la légende du schéma : « tous les choix sont guidés par le type de problématique », en montrant sur un exemple que changer la problématique change la population à observer |
| Dit qu'une variable est « quantitative » | Précise **discrète ou continue** et **justifie** par le critère comptage / mesure |
| Calcule une fréquence | Vérifie que **la somme fait 100 %** et le **signale**, ou explique l'écart par les arrondis |
| Donne un chiffre | Écrit une **phrase de lecture complète** : sous-population, valeur, unité, modalité, champ |
| Choisit un diagramme | **Justifie** le choix par la comparaison que la problématique met au centre |
| Utilise un empilé à 100 % | Rappelle qu'il **détruit l'information de volume** et donne l'effectif total à côté |
| S'arrête aux données du cours | **Recalcule** et signale une incohérence quand il y en a une — comme celle du §2.3.4 |
| Termine sur les diagrammes | Ouvre sur la **statistique inférentielle** et sur la condition du tirage **aléatoire** |

<!--saut-->

## 4. Système d'ancrage mémoriel

### 4.1 — Fiche de synthèse

::: synthese Chapitre 1 « Présenter pour informer » — l'essentiel sur une page
**LA CHAÎNE.** Besoin de décider → besoin d'information → étude statistique.

**LES 6 ÉTAPES.** ① Quel type de **problématique** ? ② Choix des données à observer :
**qui** ? ③ Choix de la **méthode de recueil** : expérimentation · observation ou enquête
qualitative · données de seconde main · enquête quantitative. ④ **Campagne de mesures** :
combien, quand, comment (l'option la plus coûteuse). ⑤ **Traitement** : présenter (CHAP 1),
résumer (CHAP 2), évolutions temporelles (CHAP 3), croiser (CHAP 4). ⑥ **Prise de
décision** : le rapport contient les résultats **et** la méthodologie ; toute information
non informative est bannie ; **ce n'est pas le rapport qui décide, la décision est
politique**. → **Tous les choix sont guidés par le type de problématique.**

**LE VOCABULAIRE.** **Population** : l'ensemble étudié. **Individus / unités statistiques** :
ses éléments. **Taille / effectif total** : leur nombre. **Variable (ou caractère)** :
une **application** associant à chaque individu **une** valeur ; notée en **majuscule**.
**Modalités** : les valeurs prises ; notées en **minuscule**.

**LES TYPES.** Qualitative (modalités **non numériques**) → **nominale** (pas d'ordre) /
**ordinale** (ordre qui a du sens). Quantitative (modalités **numériques**) → **discrète**
(comptage, dénombrable) / **continue** (mesure, non dénombrable). ⚠ Une qualitative codée
en chiffres reste qualitative — test : *la moyenne a-t-elle un sens ?*

**PRÉSENTER SANS PERTE.** Deux formes : **série brute** (*raw data*) et **distribution
observée des effectifs** (*frequencies*). Passage : **tri des modalités, puis comptage**
(quantitatif ou qualitatif ordinal). Représentations : **tableau** ou **diagramme colonne**.

**LES FORMULES.** $ n = \sum_{i=1}^{p} n_i $ · $ f_i = \dfrac{n_i}{n} $ ·
$ F_k = \sum_{i=1}^{k} f_i $. Propriétés : $ \sum f_i = 1 $ ; $ F_p = 1 $ ; $ F $ est
**croissante**. **Fréquence** = « exactement cette modalité » ; **fréquence cumulée** =
« **au plus** cette modalité » (réservée par le cours au **quantitatif**).

**PLUSIEURS DISTRIBUTIONS.** Sous-populations définies par une **autre variable** (année,
zone…), distributions **juxtaposées**, **but = comparer**. Quatre diagrammes :
**groupé par catégorie** (voir l'évolution de chaque catégorie) · **groupé par année**
(voir la structure de chaque année) · **empilé en effectifs** (volumes **et** composition) ·
**empilé à 100 %** (structures seules, **volumes détruits**). Règle : *ce qui est dans le
même groupe est ce que l'œil compare.*

**PRÉSENTER, C'EST INFORMER** = donner une **forme**. Intitulés précis · lisibles par un
non-spécialiste · compréhension immédiate ou note de lecture · **unités, population, choix
méthodologiques** indiqués.

**OUVERTURE.** Population non observable en entier → **échantillon tiré aléatoirement** →
**statistique inférentielle** (estimation + marge d'erreur), par opposition à la
**statistique descriptive** de ce cours.
:::

### 4.2 — Cartes de révision

Quarante-cinq cartes couvrant l'intégralité du chapitre.

**La démarche**

::: carte
Quelle est la chaîne qui justifie l'existence d'une étude statistique ?
--
**Besoin de décider → besoin d'information → étude statistique.** On ne fait pas une étude
parce qu'on a des données, mais parce qu'on a une **décision à prendre**.
:::

::: carte
Citez les six étapes d'une étude statistique.
--
① Quel type de **problématique** ? ② Choix des **données à observer** (qui ?) ③ Choix de la
**méthode de recueil** ④ **Campagne de mesures** ⑤ **Traitement** des données ⑥ **Prise de
décision**.
:::

::: carte
Que disent les flèches de retour du schéma des six étapes ?
--
Elles remontent de chaque étape vers l'étape 1, et portent la légende : **« Tous les choix
sont guidés par le type de problématique. »** Il n'existe pas de bonne méthode dans
l'absolu : seulement des méthodes adaptées, ou non, à la question posée.
:::

::: carte
Pourquoi « faites-moi une enquête de satisfaction » est-il une commande inexploitable ?
--
Parce que la demande est **trop vague** : elle est compatible avec des problématiques qui
imposent des choix **incompatibles** aux étapes suivantes (rayon, affichage, choix des
produits, horaires et conseil). Interroger les clients **en magasin** sur les horaires
d'ouverture ne peut pas répondre à la question, puisqu'on n'interroge que ceux à qui les
horaires conviennent.
:::

::: carte
Quelles sont les quatre méthodes de recueil des données, et laquelle est la plus coûteuse ?
--
**Expérimentation** (protocole mesurant l'effet d'une variable de contrôle sur une variable
d'observation) · **observation ou enquête qualitative** (peu d'individus, observés de façon
extensive) · **données de seconde main** (réutilisation d'informations existantes) ·
**enquête quantitative** (travail sur-mesure) — **c'est cette dernière qui est la plus
coûteuse**.
:::

::: carte
Que doit définir une campagne de mesures ?
--
**Combien** de personnes enquêter, **quand** les enquêter, **comment** les enquêter.
:::

::: carte
Quelles sont les quatre familles de traitements annoncées, et à quel chapitre chacune ?
--
**Présenter sans perte d'information (CHAP 1)** · **résumer variable par variable (CHAP 2)**
· **évolutions temporelles (CHAP 3)** · **croiser plusieurs variables (CHAP 4)**.
:::

::: carte
Que doit contenir un rapport statistique, et qui décide ?
--
Le **résultat des traitements** **et** les **éléments méthodologiques**, le tout orienté
selon la problématique. Toute information **non informative** au regard de la problématique
doit être **bannie**. **Ce n'est pas le rapport qui décide** : toute décision est
**politique** et repose aussi sur d'autres considérations, comme le coût.
:::

::: carte
Pourquoi une statistique ne peut-elle pas décider à la place du décideur ?
--
Parce qu'elle établit **ce qui est**, alors qu'une décision énonce **ce qu'il faut faire** —
ce qui suppose un **critère de choix** (préférence, objectif, contrainte) qu'aucun tableau
de chiffres ne contient. La statistique **éclaire** la décision, elle ne la remplace pas.
:::

**Le vocabulaire**

::: carte
Définissez : population, individu, effectif total.
--
**Population** : l'**ensemble (mathématique) étudié**. **Individus** ou **unités
statistiques** : les **éléments** de cette population. **Taille de la population** ou
**effectif total** : leur **nombre**.
:::

::: carte
Qu'est-ce qu'une variable statistique, et pourquoi le cours la définit-il comme une
« application » ?
--
Une **application associant à chaque individu une valeur**. Le mot « application » impose
deux contraintes : **chaque** individu reçoit une valeur (les non-réponses doivent être
traitées) et **une seule** (les modalités sont **exhaustives et exclusives**). Une question
à réponses multiples n'est donc pas une variable, mais **plusieurs** variables binaires.
:::

::: carte
Quelle est la convention d'écriture du cours pour les variables et leurs valeurs ?
--
Les **variables** sont notées en **majuscule** ($ X $), leurs **valeurs prises** —
les **modalités** — en **minuscule** ($ x_i $).
:::

::: carte
Quelle est la différence entre une variable et une modalité ?
--
La **variable** est la **question posée** (« nombre de frères et sœurs ») ; les
**modalités** sont les **réponses possibles** (0, 1, 2, 3…).
:::

::: carte
Quels sont les deux types et les quatre sous-types de variables ?
--
**Qualitative** (modalités **non numériques**) : **nominale** (pas d'ordre qui ait du sens)
et **ordinale** (ordre qui a du sens). **Quantitative** (modalités **numériques**) :
**discrète** (comptage, ensemble dénombrable) et **continue** (mesure, ensemble non
dénombrable).
:::

::: carte
Comment savoir si une variable codée en chiffres est réellement quantitative ?
--
**Test : la moyenne a-t-elle un sens ?** Si le sexe est codé 1/2, « sexe moyen = 1,5 » ne
signifie rien → la variable est **qualitative nominale codée numériquement**. Un nombre qui
n'est qu'une **étiquette** ne rend pas la variable quantitative.
:::

::: carte
Discrète ou continue : quel est le test ?
--
**Compter ou mesurer.** Entre deux valeurs voisines, une valeur intermédiaire a-t-elle un
sens ? Nombre d'enfants : entre 2 et 3, rien → **discrète**. Taille : entre 179 et 180, une
infinité de valeurs → **continue**. La précision de l'instrument ne change pas la nature de
la grandeur.
:::

::: carte
Une variable ordinale codée 1, 2, 3, 4 est-elle quantitative ?
--
**Non.** L'ordre est réel, mais les **écarts entre codes n'ont pas de sens** : rien ne
garantit que l'écart « mauvaise → plutôt mauvaise » vaille l'écart « plutôt bonne → très
bonne ». On peut **classer**, pas **additionner**. Elle reste **qualitative ordinale**.
:::

::: carte
Enquête sur les infractions (diapo 12) : population, unités, effectif total, variable, type ?
--
**Population** : l'ensemble des **infractions déclarées** en 2024 sur le champ Insee.
**Unités** : **une infraction**. **Effectif total** : **9 376 000** infractions (somme
vérifiée des huit modalités). **Variable** : le **type d'atteinte déclarée**, **qualitative
nominale**. **Modalités** : les **huit** types listés.
:::

::: carte
Pourquoi le classement décroissant d'un tableau ne rend-il pas la variable ordinale ?
--
Parce que l'ordre y résulte des **effectifs observés**, et non des modalités elles-mêmes.
Une variable est ordinale quand l'ordre est **intrinsèque aux modalités** (« mauvais <
moyen < bon »). Ranger par fréquence est un **choix de présentation**.
:::

**Présenter une distribution**

::: carte
Quelles sont les deux façons de présenter une variable sans perte d'information, et comment
passe-t-on de l'une à l'autre ?
--
La **série brute** (*raw data*) et la **distribution observée des effectifs**
(*frequencies*). Le passage exige un traitement : **tri des modalités, puis comptage des
effectifs** — dans le cas quantitatif ou qualitatif ordinal.
:::

::: carte
Qu'est-ce qu'une distribution observée des effectifs ? Qu'est-ce que l'effectif d'une
modalité ?
--
Une distribution observée des effectifs **associe à chaque modalité l'effectif observé
correspondant**. L'**effectif d'une modalité** est le **nombre d'individus présentant cette
modalité**. Représentation : **tableau** ou **diagramme colonne**. **Sans perte
d'information** — c'est souvent l'**étape n° 1** d'une analyse.
:::

::: carte
Pourquoi le tri ne s'applique-t-il pas aux variables nominales ?
--
Parce que trier suppose un **ordre**, et qu'aucun ordre n'a de sens entre des modalités
nominales. On peut compter leurs effectifs, mais l'ordre des lignes du tableau reste un pur
**choix de présentation**.
:::

::: carte
Sur un diagramme en colonnes d'une variable quantitative, pourquoi représenter les
modalités d'effectif nul ?
--
Parce que l'axe des abscisses est un **axe numérique** : les distances doivent être
respectées. Supprimer les modalités vides (8, 10, 11, 12 dans l'exemple des 87 étudiants)
rapprocherait visuellement des valeurs éloignées et **déformerait la forme de la
distribution**.
:::

::: carte
Définissez la fréquence et la fréquence cumulée.
--
La **fréquence** d'une modalité est la **proportion d'individus présentant cette modalité**
dans la population totale (en % de la population). La **fréquence cumulée** d'une modalité
est la proportion d'individus présentant **cette modalité ou une modalité inférieure** —
autrement dit « **au plus** ». Le cours la réserve au caractère **quantitatif**.
:::

::: carte
Quelles représentations le cours associe-t-il à une répartition en fréquences ?
--
Un **camembert** ou un **diagramme en barres**.
:::

::: carte
Écrivez les quatre formules du cours.
--
$$ n = \sum_{i=1}^{p} n_i \qquad f_i = \frac{n_i}{n} \qquad F_k = \sum_{i=1}^{k} f_i $$
avec $ X $ le caractère, $ x_i $ les modalités ordonnées pour $ i = 1, \ldots, p $.
:::

::: carte
Que valent $ n $ et $ p $, et pourquoi ne faut-il pas les confondre ?
--
$ n $ est l'**effectif total** — le nombre d'**individus**. $ p $ est le nombre de
**modalités** — le nombre de **valeurs distinctes**. Dans l'exemple des 87 étudiants :
$ n = 87 $ mais $ p = 11 $.
:::

::: carte
Démontrez que la somme des fréquences vaut 1.
--
$$ \sum_{i=1}^{p} f_i = \sum_{i=1}^{p} \frac{n_i}{n} = \frac{1}{n}\sum_{i=1}^{p} n_i = \frac{n}{n} = 1 $$
On remplace $ f_i $ par sa définition, on sort $ n $ de la somme (il ne dépend pas de
$ i $), et la somme des effectifs vaut $ n $. En pourcentage : **100 %**.
:::

::: carte
Pourquoi les fréquences cumulées sont-elles nécessairement croissantes ?
--
Parce que $ F_k - F_{k-1} = f_k \ge 0 $ : une fréquence est toujours positive ou nulle.
Une colonne de fréquences cumulées qui **diminue** signale donc immédiatement une **erreur
de calcul**. Et $ F_p = 1 $ (100 %) est le contrôle final du tableau.
:::

::: carte
Sur 87 étudiants, 33 déclarent un frère ou une sœur et 23 en déclarent deux ; 11 n'en ont
aucun. Calculez $ F $ pour la modalité 2 et interprétez.
--
$ F(2) = (11 + 33 + 23)/87 = 67/87 = 0{,}7701 $, soit **77,01 %**. Lecture : **77,01 % des
étudiants déclarent au plus deux frères et sœurs** — donc 22,99 % en déclarent au moins
trois.
:::

::: carte
Tableau des 17 132 milliers de familles : population, unités, caractère, type, et comment
les fréquences ont été calculées ?
--
**Population** : les familles enquêtées (17 132 **milliers**, soit ≈ 17,1 millions).
**Unités** : une **famille**. **Caractère** : le **nombre d'enfants**, **quantitatif
discret** (dernière modalité en **classe ouverte**). **Fréquences** : $ f_i = n_i/n $ —
$ 8\,225/17\,132 = 48{,}0 $ % ; **fréquences cumulées** : sommes successives — 48,0 ; 70,3 ;
90,4 ; 97,7 ; 100,0.
:::

::: carte
Pourquoi ne peut-on pas calculer une moyenne exacte à partir du tableau du nombre d'enfants ?
--
Parce que la dernière modalité, « **4 enfants et plus** », est une **classe ouverte** : on
ignore la valeur réelle des observations qu'elle contient.
:::

**Comparer plusieurs distributions**

::: carte
Qu'est-ce qu'une comparaison de plusieurs distributions d'un même caractère, et quelles
variables met-elle en jeu ?
--
Plusieurs **sous-populations** sont définies **selon une autre variable** (année, zone
géographique…) ; il y a **une distribution par sous-population**, présentées
**juxtaposées**, dans le but de **comparer la répartition** entre sous-populations. Deux
variables sont donc en jeu : la variable **étudiée** et la variable de **découpage**.
:::

::: carte
Personnes écrouées (diapo 25) : population, sous-populations, caractère, type ?
--
**Population** : les personnes **écrouées en France**. **Unités** : une personne écrouée.
**Sous-populations** : les années **2020, 2021, 2022, 2023**. **Caractère** : la **catégorie
pénale** (prévenus détenus, condamnés-prévenus détenus, condamnés détenus, condamnés non
détenus), **qualitative nominale**.
:::

::: carte
Quelle est la règle de choix entre un diagramme groupé par catégorie et un diagramme groupé
par année ?
--
**Ce qui est dans le même groupe est ce que l'œil compare.** Grouper par **catégorie** →
on voit l'**évolution dans le temps de chaque catégorie**. Grouper par **année** → on voit
la **structure** de chaque année. Le choix dépend de la comparaison que la problématique
met au centre.
:::

::: carte
Distribution du nombre d'enfants par famille (diapo 28) : population, sous-populations,
caractère, type ? Donnez une phrase de lecture.
--
**Population** : les **familles vivant en ménage ordinaire ayant au moins un enfant
mineur**, France hors Mayotte. **Sous-populations** : les années 1990, 1999, 2007, 2012,
2017, 2023. **Caractère** : le **nombre d'enfants mineurs**, **quantitatif discret**.
Lecture : « En 2023, **3 578,3 milliers de familles** du champ avaient **exactement un
enfant mineur**. »
:::

::: carte
Qu'est-ce qu'un diagramme empilé en effectifs, et que montre la hauteur totale ?
--
Chaque colonne représente une sous-population ; les segments superposés représentent les
**effectifs** de chaque modalité. La **hauteur totale** correspond à l'**effectif total de
la sous-population** — ici, l'ensemble des familles de l'année. Il montre donc **volumes et
composition** simultanément.
:::

::: carte
Qu'est-ce qu'un diagramme empilé à 100 %, et que perd-on en l'utilisant ?
--
Toutes les colonnes ont la **même hauteur** : on représente les **fréquences** et non les
effectifs, **par sous-population**. On perd **toute l'information de volume** : une colonne
peut représenter 8 millions de familles ou 800. C'est pourquoi on donne toujours l'effectif
total à côté.
:::

::: carte
Comment a été calculé le chiffre 12,6 % (3 enfants, 2017) ?
--
C'est la **fréquence** de la modalité « 3 enfants » **dans la sous-population 2017** :
$ 1\,012{,}2 / 8\,014{,}7 = 0{,}1263 $, soit **12,63 %**, arrondi à **12,6 %**. Le
dénominateur est **toujours** l'effectif de la sous-population du numérateur.
:::

::: carte
Entre 2017 et 2023, la part des familles à 3 enfants passe de 12,6 % à 12,1 %. Que dire de
l'effectif ?
--
Il baisse bien davantage en proportion : de **1 012,2 à 956,2 milliers**, soit **−56 000
familles (−5,5 %)** contre −0,5 point de part. **Une part quasi stable dans un total qui
diminue signifie un effectif qui diminue.**
:::

::: carte
Pourquoi ne peut-on pas comparer le tableau des 17 132 milliers de familles et celui du
nombre d'enfants mineurs par année ?
--
Parce que **les champs diffèrent** : le premier inclut les familles **sans enfant** (48 %
de l'effectif), le second ne retient que les familles ayant **au moins un enfant mineur**.
Avant toute comparaison de deux tableaux, on compare d'abord leurs **champs**.
:::

**Communiquer et conclure**

::: carte
Quelles sont les quatre règles de présentation d'un tableau ou d'un graphique ?
--
**Intitulés précis** (pas de noms de variables ou de modalités obscurs) · **lisibles par un
non-spécialiste** · **compréhension immédiate** ou simplifiée au maximum, avec une **note de
lecture** en bas de tableau en cas de complexité · **indiquer les unités de mesure, la
population et les choix méthodologiques**.
:::

::: carte
Que signifie « informer » selon le cours ?
--
**Donner une forme, une signification à des données** (le plus souvent numériques brutes).
Les tableaux et graphiques **produisent de l'information** : ce sont des **outils de
communication**. D'où le titre du chapitre : « Présenter pour informer ».
:::

::: carte
Qu'est-ce que la statistique inférentielle, et à quelle condition est-elle valide ?
--
L'ensemble des techniques permettant de **déduire des éléments d'une population à partir
d'un échantillon**. Condition : l'échantillon doit être **tiré aléatoirement** — c'est le
hasard du tirage qui permet de calculer une **marge d'erreur**. Elle s'oppose à la
**statistique descriptive**, qui décrit ce qui a été observé, sans risque d'inférence.
:::

::: carte
Les trois éléments obligatoires d'une phrase de lecture ?
--
**La sous-population** (l'année, la zone), **la valeur avec son unité** (12,6 % ; 3 578,3
milliers), et **la modalité avec son champ** (exactement trois enfants mineurs, parmi les
familles ayant au moins un enfant mineur, France hors Mayotte).
:::

### 4.3 — Moyens mnémotechniques

::: methode Les six étapes — « Problématique, Qui, Comment, Combien, Traiter, Décider »
Six mots, dans l'ordre, qui redonnent les six étapes :

| Mot | Étape |
|---|---|
| **Problématique** | ① Quel type de problématique ? |
| **Qui** | ② Choix des données à observer |
| **Comment** | ③ Choix de la méthode de recueil |
| **Combien** | ④ Campagne de mesures (combien, quand, comment) |
| **Traiter** | ⑤ Traitement des données |
| **Décider** | ⑥ Prise de décision |

Et la légende du schéma, à réciter juste après : **tous les choix sont guidés par le type
de problématique.**
:::

::: methode Les quatre types de variables — deux questions, jamais quatre
Ne mémorisez pas quatre étiquettes : mémorisez **deux questions successives**.

1. **Mots ou nombres ?** Mots → qualitative. Nombres → quantitative.
2. Si **mots** : *un ordre a-t-il du sens ?* Non → **nominale**. Oui → **ordinale**.
   Si **nombres** : *compte-t-on ou mesure-t-on ?* Compter → **discrète**. Mesurer →
   **continue**.

Et la question de contrôle, qui sauve du piège du codage : **la moyenne a-t-elle un sens ?**
:::

::: methode Fréquence et fréquence cumulée — « exactement » contre « au plus »
- $ f_i $ répond à : « quelle part présente **exactement** cette modalité ? »
- $ F_k $ répond à : « quelle part présente **au plus** cette modalité ? »

Deux mots à retenir : **exactement / au plus**. Ils suffisent à ne jamais se tromper de
colonne dans un tableau.
:::

::: methode Les notations — $ n $ comme individus, $ p $ comme possibilités
$ n $ compte les **individus** (l'effectif) ; $ p $ compte les **possibilités**, c'est-à-dire
les modalités. Et $ i $ est l'indice qui parcourt les modalités — **jamais** les individus.
:::

::: methode Le choix du diagramme — « le groupe est un bloc, l'intérieur se compare »
L'œil compare spontanément les barres **voisines**. Donc : ce que vous placez **à
l'intérieur d'un groupe** est ce que le lecteur comparera ; ce que vous placez **en
groupes** est ce qu'il verra comme des blocs distincts.

Et pour les empilés : **effectifs = volumes conservés ; 100 % = structure seule, volumes
détruits.**
:::

::: methode Les contrôles de cohérence — les trois vérifications réflexes
Avant de rendre un tableau, toujours vérifier :
1. $ \sum n_i = n $ — la somme des effectifs égale l'effectif total ;
2. $ \sum f_i = 100 $ % — aux arrondis près, et le dire si l'écart apparaît ;
3. $ F $ **croissante** et $ F_p = 100 $ % — la dernière fréquence cumulée boucle à 100.

Ces trois contrôles prennent dix secondes et attrapent l'essentiel des erreurs de calcul.
:::

### 4.4 — Schéma récapitulatif

```
              BESOIN DE DÉCIDER
                     |
              BESOIN D'INFORMATION
                     |
              ÉTUDE STATISTIQUE
                     |
   +-----------------+---------------------+
   |                 |                     |
 SECTION 1        SECTION 2            SECTION 3
 LA DÉMARCHE      LE VOCABULAIRE       LA PRÉSENTATION
   |                 |                     |
 6 ÉTAPES         POPULATION            SANS PERTE D'INFORMATION
 1 Problématique     |  (ensemble)         |
 2 Qui ?          INDIVIDUS             +--> SÉRIE BRUTE (raw data)
 3 Comment ?         |  (éléments)      |         |
 4 Combien ?      EFFECTIF TOTAL n      |    tri + comptage
 5 Traiter           |                  |         v
 6 Décider        VARIABLE X            +--> DISTRIBUTION DES EFFECTIFS
   |                 |  (application)             |
   |              MODALITÉS x(i)         +--------+---------+
   |                 |                   |                  |
   |          +------+------+        EFFECTIFS n(i)    FRÉQUENCES f(i)=n(i)/n
   |          |             |            |             FRÉQ. CUMULÉES F(k)
   |     QUALITATIVE   QUANTITATIVE      |                  |
   |     (mots)        (nombres)      tableau         camembert / barres
   |       |               |          diagramme
   |   nominale        discrète       colonne
   |   ordinale        continue
   |                                        PLUSIEURS SOUS-POPULATIONS
   |                                                 |
   |                                +----------------+----------------+
   |                                |                                 |
   |                          COLONNES GROUPÉES               DIAGRAMMES EMPILÉS
   |                          par catégorie -> évolution      effectifs -> volumes
   |                          par année     -> structure      100 %     -> structure
   |                                                 |
   +---> « TOUS LES CHOIX SONT GUIDÉS PAR LE TYPE DE PROBLÉMATIQUE » <---+
                                 |
                    PRÉSENTER POUR INFORMER
             (intitulés, lisibilité, unités, champ, méthode)
                                 |
                    OUVERTURE : population non observable
                    -> échantillon ALÉATOIRE
                    -> STATISTIQUE INFÉRENTIELLE
```

**Les liens du schéma, énoncés un par un.**

| Lien | Ce qu'il affirme |
|---|---|
| Décider → information → étude | L'étude est **causée** par une décision à prendre, jamais par la disponibilité de données |
| Les 6 étapes → la légende | Chaque étape est un **choix**, et tous les choix découlent de l'étape 1 |
| Population → individus → variable → modalités | Une **cascade** : l'ensemble, ses éléments, ce qu'on mesure sur eux, les valeurs obtenues |
| Variable → 2 types → 4 sous-types | Le type **détermine les traitements autorisés** en aval |
| Série brute ↔ distribution | Aller-retour **sans perte**, par tri puis comptage |
| Effectifs → fréquences → fréquences cumulées | Trois lectures de la **même** distribution, de plus en plus synthétiques, toutes **sans perte** |
| Une distribution → plusieurs sous-populations | Le passage de la **description** à la **comparaison** — et l'annonce du chapitre 4 |
| Comparaison → quatre diagrammes | Le **type de comparaison** commande le diagramme, pas l'inverse |
| Tout → « présenter pour informer » | Présenter, c'est **donner une forme** : sans forme, les données ne sont pas de l'information |
| Descriptive → inférentielle | Quand la population n'est pas observable en entier, il faut **échantillonner au hasard** et accepter une marge d'erreur |

<!--saut-->
## 5. Entraînement progressif

### Niveau 1 — Restitution

Répondez sans regarder le document.

1. Énoncez la chaîne qui justifie l'existence d'une étude statistique.
2. Citez les six étapes d'une étude statistique, dans l'ordre.
3. Quelle est la légende du schéma des six étapes, et que signifient les flèches de retour ?
4. Citez les quatre méthodes de recueil des données. Laquelle est la plus coûteuse ?
5. Que doit définir une campagne de mesures ?
6. Citez les quatre familles de traitements et le chapitre correspondant.
7. Que doit contenir un rapport statistique ? Qui décide, et pourquoi ?
8. Définissez : population, individu, effectif total, variable, modalité.
9. Pourquoi le cours définit-il la variable comme une « application » ? Deux conséquences.
10. Quels sont les deux types et les quatre sous-types de variables ? Donnez le critère de
    chaque bifurcation.
11. Comment savoir si une variable codée en chiffres est réellement quantitative ?
12. Quelles sont les deux façons de présenter une variable sans perte d'information ?
    Comment passe-t-on de l'une à l'autre ?
13. Définissez la distribution observée des effectifs et l'effectif d'une modalité.
14. Définissez la fréquence, puis la fréquence cumulée. À quel type de variable le cours
    réserve-t-il la seconde, et pourquoi ?
15. Écrivez les formules de $ n $, $ f_i $ et $ F_k $.
16. Démontrez que $ \sum f_i = 1 $ et que $ F $ est croissante.
17. Qu'est-ce qu'une présentation de plusieurs distributions d'un même caractère ? Quelles
    variables met-elle en jeu ?
18. Quelle est la règle de choix entre un diagramme groupé par catégorie et un diagramme
    groupé par année ?
19. Quelle est la différence entre un diagramme empilé en effectifs et un empilé à 100 % ?
    Que perd-on avec le second ?
20. Citez les quatre règles de présentation d'un tableau ou d'un graphique.
21. Que signifie « informer », selon le cours ?
22. Qu'est-ce que la statistique inférentielle ? À quelle condition est-elle valide ?

::: correction Corrigé du niveau 1
1. **Besoin de décider → besoin d'information → étude statistique.**
2. ① Problématique ② Choix des données à observer (qui ?) ③ Choix de la méthode de recueil
   ④ Campagne de mesures ⑤ Traitement ⑥ Prise de décision.
3. **« Tous les choix sont guidés par le type de problématique. »** Les flèches remontent de
   chaque étape vers l'étape 1 : aucun choix technique n'est bon dans l'absolu, il n'est bon
   que **relativement à la question posée**.
4. **Expérimentation · observation ou enquête qualitative · données de seconde main ·
   enquête quantitative.** La plus coûteuse : l'**enquête quantitative**.
5. **Combien** de personnes enquêter, **quand**, **comment**.
6. Présenter sans perte (**CHAP 1**) · résumer variable par variable (**CHAP 2**) ·
   évolutions temporelles (**CHAP 3**) · croiser plusieurs variables (**CHAP 4**).
7. Le **résultat des traitements** et les **éléments méthodologiques**, orientés selon la
   problématique ; toute information non informative est **bannie**. **Ce n'est pas le
   rapport qui décide** : la décision est **politique**, car passer de « ce qui est » à
   « ce qu'il faut faire » exige un critère de choix qu'aucun tableau ne contient.
8. **Population** : l'ensemble étudié. **Individu / unité statistique** : ses éléments.
   **Effectif total** : leur nombre. **Variable** : une application associant à chaque
   individu une valeur. **Modalités** : les valeurs prises.
9. Parce qu'une application associe à **chaque** individu **une et une seule** valeur.
   Conséquences : les **non-réponses** doivent être explicitement traitées, et les modalités
   doivent être **exhaustives et exclusives** — une question à réponses multiples n'est pas
   une variable mais plusieurs.
10. **Qualitative** (modalités non numériques) → **nominale** / **ordinale**, critère :
    *existe-t-il un ordre qui a du sens ?* **Quantitative** (modalités numériques) →
    **discrète** / **continue**, critère : *compte-t-on ou mesure-t-on ?*
11. **Test de la moyenne** : a-t-elle un sens ? « Sexe moyen = 1,5 » n'en a pas → la
    variable reste qualitative.
12. **Série brute** et **distribution observée des effectifs**. Passage : **tri des
    modalités, puis comptage des effectifs**.
13. Elle **associe à chaque modalité l'effectif observé correspondant** ; l'**effectif d'une
    modalité** est le nombre d'individus qui la présentent.
14. **Fréquence** : proportion d'individus présentant une modalité donnée, dans la
    population totale. **Fréquence cumulée** : proportion présentant cette modalité **ou une
    modalité inférieure**. Le cours la réserve au **quantitatif**, car cumuler suppose un
    **ordre** sur les modalités.
15. $ n = \sum_{i=1}^{p} n_i $ ; $ f_i = n_i/n $ ; $ F_k = \sum_{i=1}^{k} f_i $.
16. $ \sum f_i = \sum n_i/n = (1/n)\sum n_i = n/n = 1 $. Et
    $ F_k - F_{k-1} = f_k \ge 0 $, donc $ F $ est croissante.
17. Plusieurs **sous-populations**, définies **selon une autre variable**, chacune avec sa
    distribution, **juxtaposées** pour être **comparées**. Deux variables : celle qu'on
    **étudie** et celle qui **découpe**.
18. **Ce qui est dans le même groupe est ce que l'œil compare.** Groupé par catégorie → on
    voit l'**évolution** ; groupé par année → on voit la **structure**.
19. L'empilé en effectifs conserve les **volumes** (hauteurs inégales) ; l'empilé à 100 %
    n'affiche que la **structure** (hauteurs égales) et **détruit toute information de
    volume**.
20. **Intitulés précis · lisibles par un non-spécialiste · compréhension immédiate ou note
    de lecture · unités, population et choix méthodologiques indiqués.**
21. **Donner une forme, une signification à des données** brutes. Les tableaux et graphiques
    **produisent** de l'information.
22. Les techniques permettant de **déduire des éléments d'une population à partir d'un
    échantillon**. Condition : l'échantillon doit être **tiré aléatoirement**.
:::

### Niveau 2 — Application

**Exercice 1 — Qualifier huit variables.** Pour chacune, donnez le type et le sous-type, et
**justifiez par le critère**.

a) code postal — b) note sur 20 — c) mention au baccalauréat — d) chiffre d'affaires annuel
— e) catégorie socioprofessionnelle — f) âge en années révolues — g) tranche d'âge
(« 18-24 », « 25-34 »…) — h) numéro de téléphone.

::: correction Corrigé de l'exercice 1
| Variable | Type | Justification par le critère |
|---|---|---|
| **a) Code postal** | **Qualitative nominale** | Ce sont des chiffres, mais des **étiquettes** : la moyenne de deux codes postaux n'a aucun sens, et 13100 n'est pas « supérieur » à 13001 |
| **b) Note sur 20** | **Quantitative continue** | Elle relève de la **mesure** d'une performance ; une note de 12,5 ou 12,75 a un sens. *(Si le barème n'admet que des entiers, on la traite en pratique comme discrète : signalez-le, c'est ce qu'attend un correcteur exigeant.)* |
| **c) Mention au baccalauréat** | **Qualitative ordinale** | Modalités non numériques (passable, assez bien, bien, très bien) mais **ordonnées** : l'ordre a du sens |
| **d) Chiffre d'affaires annuel** | **Quantitative continue** | Grandeur **mesurée** ; entre 1,2 M€ et 1,3 M€, une infinité de valeurs |
| **e) Catégorie socioprofessionnelle** | **Qualitative nominale** | Modalités non numériques, aucun ordre qui ait un sens — même si l'Insee les numérote |
| **f) Âge en années révolues** | **Quantitative discrète** *(par convention)* | L'âge est une grandeur **continue** par nature ; « en années révolues », il relève du **comptage** et se traite comme discret. **Justifier ce choix est le vrai attendu** |
| **g) Tranche d'âge** | **Qualitative ordinale** | Les modalités sont des **classes**, non des nombres, et elles sont **ordonnées**. *(On la traite aussi comme une quantitative regroupée en classes selon l'usage — mais elle n'est plus une variable numérique.)* |
| **h) Numéro de téléphone** | **Qualitative nominale** | Pure **étiquette** : ni ordre ni opération arithmétique n'ont de sens |

**Le fil rouge :** trois des huit variables (a, e, h) sont des **nombres qui n'en sont pas**.
C'est exactement l'avertissement de la diapositive 13.
:::

**Exercice 2 — Construire une distribution complète.** Quarante clients d'une enseigne ont
été interrogés sur leur nombre de visites en magasin au cours du mois écoulé. Série brute :

```
2 0 1 3 2 1 0 2 4 1   1 2 0 5 2 1 3 2 1 0
2 1 4 2 0 1 2 3 1 2   0 1 2 1 3 2 0 1 2 1
```

1. Identifiez la population, les unités statistiques, l'effectif total, la variable et son
   type.
2. Construisez le tableau de la distribution : effectifs, fréquences, fréquences cumulées.
3. Vérifiez vos calculs par les trois contrôles de cohérence.
4. Écrivez une phrase de lecture pour $ f $ de la modalité 2 et pour $ F $ de la modalité 2.
5. Quelle part des clients est venue **au moins trois fois** ?

::: correction Corrigé détaillé de l'exercice 2
**1. Identification.**
- Population : les **40 clients interrogés** de l'enseigne.
- Unités statistiques : **un client**.
- Effectif total : $ n = 40 $.
- Variable : le **nombre de visites en magasin au cours du mois écoulé**.
- Type : **quantitative discrète** — un **comptage** ; entre 2 et 3 visites, rien.

**2. Tri puis comptage.** On trie les 40 valeurs, puis on compte modalité par modalité.

| $ x_i $ | $ n_i $ | $ f_i $ (%) | $ F_i $ (%) |
|---:|---:|---:|---:|
| 0 | 7 | 17,5 | 17,5 |
| 1 | 13 | 32,5 | 50,0 |
| 2 | 13 | 32,5 | 82,5 |
| 3 | 4 | 10,0 | 92,5 |
| 4 | 2 | 5,0 | 97,5 |
| 5 | 1 | 2,5 | 100,0 |
| **Ensemble** | **40** | **100,0** | — |

*Détail de deux calculs :* $ f_1 = 7/40 = 0{,}175 = 17{,}5 $ % ;
$ F_3 = 17{,}5 + 32{,}5 + 32{,}5 = 82{,}5 $ %.

**3. Les trois contrôles.**
- $ \sum n_i = 7+13+13+4+2+1 = 40 = n $ ✔
- $ \sum f_i = 17{,}5+32{,}5+32{,}5+10+5+2{,}5 = 100{,}0 $ % ✔
- $ F $ croissante et $ F_6 = 100{,}0 $ % ✔

**4. Phrases de lecture.**
- *Fréquence :* « **32,5 %** des 40 clients interrogés sont venus **exactement deux fois**
  en magasin au cours du mois écoulé. »
- *Fréquence cumulée :* « **82,5 %** des clients interrogés sont venus **au plus deux
  fois**. »

**5. Au moins trois visites.** Deux méthodes, même résultat :
- par complément : $ 100 - F(2) = 100 - 82{,}5 = \mathbf{17{,}5} $ % ;
- par addition directe : $ 10{,}0 + 5{,}0 + 2{,}5 = \mathbf{17{,}5} $ % ✔

**La méthode par complément est celle à privilégier en examen** : un seul calcul, et elle
utilise la colonne des fréquences cumulées, déjà construite.
:::

**Exercice 3 — Calculs inverses.**
a) Dans une population de 1 240 individus, une modalité a une fréquence de 12,5 %. Quel est
son effectif ?
b) Une modalité regroupe 348 individus et représente 29 % de la population. Quel est
l'effectif total ?
c) Dans un tableau à quatre modalités, on lit $ F_1 = 18 $ %, $ F_2 = 47 $ %,
$ F_3 = 81 $ %. Retrouvez les quatre fréquences $ f_1 $ à $ f_4 $.

::: correction Corrigé de l'exercice 3
**a)** De $ f_i = n_i/n $ on tire $ n_i = f_i \times n $ :
$ n_i = 0{,}125 \times 1\,240 = \mathbf{155} $ individus.

**b)** De la même relation, $ n = n_i / f_i = 348 / 0{,}29 = \mathbf{1\,200} $ individus.
*Contrôle :* $ 348/1\,200 = 0{,}29 $ ✔

**c)** Puisque $ F_k = F_{k-1} + f_k $, on a $ f_k = F_k - F_{k-1} $ :
- $ f_1 = F_1 = \mathbf{18} $ %
- $ f_2 = 47 - 18 = \mathbf{29} $ %
- $ f_3 = 81 - 47 = \mathbf{34} $ %
- $ f_4 = 100 - 81 = \mathbf{19} $ % *(car $ F_4 = 100 $ % nécessairement)*

*Contrôle :* $ 18 + 29 + 34 + 19 = 100 $ % ✔ **La dernière fréquence s'obtient toujours par
complément à 100 : c'est le point que la majorité des copies rate.**
:::

**Exercice 4 — Part et volume.** Une enseigne classe ses clients en quatre segments. Voici
les effectifs de 2019 et 2024.

| Segment | 2019 | 2024 |
|---|---:|---:|
| Occasionnels | 420 | 560 |
| Réguliers | 310 | 395 |
| Fidèles | 180 | 150 |
| Premium | 90 | 55 |

1. Calculez la structure (en %) de chaque année.
2. Que devient le segment « Fidèles », en part et en effectif ?
3. Un directeur commente : « la part des Fidèles n'a perdu que 5 points, ce n'est pas
   grave ». Que lui répondez-vous ?
4. Quel diagramme choisiriez-vous pour appuyer votre réponse, et pourquoi ?

::: correction Corrigé de l'exercice 4
**1. Structures.** Totaux : 2019 → $ 420+310+180+90 = 1\,000 $ ; 2024 →
$ 560+395+150+55 = 1\,160 $.

| Segment | 2019 (%) | 2024 (%) | Écart (points) |
|---|---:|---:|---:|
| Occasionnels | 42,0 | 48,3 | +6,3 |
| Réguliers | 31,0 | 34,1 | +3,1 |
| **Fidèles** | **18,0** | **12,9** | **−5,1** |
| Premium | 9,0 | 4,7 | −4,3 |
| **Total** | **100,0** | **100,0** | — |

**2. Le segment Fidèles.** En **part** : de 18,0 % à 12,9 %, soit **−5,1 points**. En
**effectif** : de 180 à 150 clients, soit **−30 clients, c'est-à-dire −16,7 %**.

**3. Réponse au directeur.** Deux arguments.
- La baisse de part **sous-estime** la baisse réelle en apparence, mais la vraie
  information est ailleurs : **le segment perd un sixième de ses clients** (−16,7 %) dans un
  total qui, lui, **augmente de 16 %**. La perte de part combine donc deux mouvements de
  sens opposé.
- Surtout, un **point de part n'est pas une unité homogène** : il ne dit rien du volume tant
  qu'on ne connaît pas le total. Ici, 5 points de part valent 30 clients ; sur une base dix
  fois plus grande, ils en vaudraient 300.

**4. Quel diagramme.** Un **diagramme empilé en effectifs** (et non à 100 %), parce que la
problématique porte simultanément sur le **volume** et sur la **structure**. Un empilé à
100 % masquerait précisément l'information qui fonde la réponse : que le total croît
pendant que le segment recule. **Ou, mieux encore, les deux côte à côte** — la structure
pour la part, les effectifs pour le volume.
:::

**Exercice 5 — Choisir le diagramme.** Pour chacune de ces quatre problématiques, dites
quel diagramme choisir parmi : *colonnes groupées par catégorie*, *colonnes groupées par
sous-population*, *empilé en effectifs*, *empilé à 100 %* — et justifiez en une phrase.

a) « Le nombre de condamnés détenus a-t-il augmenté entre 2020 et 2023 ? »
b) « La composition de la population carcérale s'est-elle déformée entre 2020 et 2023 ? »
c) « Combien de familles au total, et comment se répartissent-elles selon le nombre
d'enfants, chaque année ? »
d) « La part des familles nombreuses recule-t-elle sur trente ans ? »

::: correction Corrigé de l'exercice 5
**a) Colonnes groupées par catégorie.** La question porte sur l'**évolution d'une catégorie
donnée** : il faut que les quatre années soient **côte à côte à l'intérieur du groupe
« condamnés détenus »**, pour que l'œil les compare directement.

**b) Colonnes groupées par sous-population (par année)** — ou empilé à 100 %. La question
porte sur la **structure** et sa déformation : il faut voir, année par année, le poids
relatif des catégories.

**c) Empilé en effectifs.** La question demande **deux choses à la fois** : le total (la
hauteur de la colonne) **et** la composition (les segments). C'est exactement ce que fait
l'empilé en effectifs, et lui seul.

**d) Empilé à 100 %.** La question ne porte que sur des **parts** (« la part des familles
nombreuses »), sur une longue période. L'empilement à 100 % est le plus lisible — à
condition de rappeler les effectifs totaux à côté, faute de quoi on ne saurait pas si le
recul de la part correspond à un recul du nombre.

**La règle qui produit ces quatre réponses est unique** : *tous les choix sont guidés par le
type de problématique.*
:::

### Niveau 3 — Maîtrise

**Question 1.** « Présenter des données, c'est déjà les interpréter. » Discutez, en vous
appuyant sur au moins trois éléments précis du chapitre.

**Question 2.** Un tableau publié indique : « Champ : France hors Mayotte, familles vivant
en ménage ordinaire ayant au moins un enfant mineur. Unité : milliers. » Expliquez, en
quatre points, pourquoi chacune de ces mentions est indispensable, et donnez un exemple
d'erreur commise en leur absence.

**Question 3 (question piège).** Un étudiant écrit : « la variable *note obtenue au
contrôle*, codée de 0 à 20, est quantitative discrète, donc je peux calculer sa moyenne ;
la variable *appréciation*, codée 1 = insuffisant, 2 = passable, 3 = bien, 4 = très bien,
est aussi codée en chiffres, donc je peux aussi calculer sa moyenne. » Où est l'erreur, et
que peut-on faire, exactement, avec chacune des deux variables ?

**Question 4.** Vous devez présenter à un directeur commercial la répartition de son chiffre
d'affaires par région, pour cinq régions et trois années. Décrivez la présentation que vous
retenez — tableau, diagramme, intitulés, mentions obligatoires — et **justifiez chaque
choix** par le cours.

::: correction Corrigé du niveau 3 — question 1
**Thèse : oui, et le chapitre en administre trois preuves.**

**I — La présentation est un choix, et tout choix oriente.**
Le chapitre montre que les mêmes chiffres produisent des lectures différentes selon la
présentation. Les diapositives 26 et 27 contiennent **strictement les mêmes données** sur
les personnes écrouées ; groupées par catégorie, elles racontent une **hausse** ; groupées
par année, elles racontent une **structure stable**. Le statisticien qui choisit le
groupement choisit ce que le lecteur verra en premier.

**II — Certaines présentations détruisent de l'information.**
L'empilement à 100 % (diapositive 30) supprime toute information de volume. Une part de
12,6 % peut correspondre à un effectif en hausse ou en baisse ; le diagramme ne permet pas
de trancher. **Choisir cette représentation, c'est décider que le volume n'est pas le
sujet** — ce qui est une interprétation.

**III — Le cours l'assume explicitement.**
La diapositive 32 énonce que les tableaux et graphiques « **produisent de l'information** »
et sont « des **outils de communication** », et que « informer » signifie « **donner une
forme** ». Une donnée brute ne signifie rien ; c'est la mise en forme qui la rend
interprétable. Il n'existe donc pas de présentation neutre.

**Nuance à apporter — c'est ce qui distingue une excellente copie.** « Interpréter » n'est
pas « déformer ». Le chapitre insiste sur le fait que ces présentations se font **sans
perte d'information** : on peut toujours reconstruire les données. L'orientation est dans
la **mise en évidence**, pas dans la falsification. D'où la contrepartie exigée par la
diapositive 32 : indiquer les **unités, la population, les choix méthodologiques** — c'est
ce qui permet au lecteur de refaire lui-même une autre lecture.

**Conclusion.** Présenter, c'est interpréter — et c'est légitime **à condition que
l'interprétation soit rendue vérifiable** par la mention des choix effectués. La
transparence méthodologique n'est pas une formalité : c'est ce qui distingue une
présentation d'une manipulation.
:::

::: correction Corrigé du niveau 3 — question 2
| Mention | Pourquoi elle est indispensable | Erreur commise en son absence |
|---|---|---|
| **« France hors Mayotte »** | Délimite géographiquement la population (étape 2 de la démarche) | Comparer ce tableau à un autre incluant Mayotte, et attribuer à une évolution réelle un simple changement de périmètre |
| **« familles vivant en ménage ordinaire »** | Exclut les personnes vivant en collectivité (foyers, casernes, établissements) | Croire que le total couvre toutes les familles de France |
| **« ayant au moins un enfant mineur »** | Exclut les familles sans enfant mineur — soit près de la moitié du total dans le tableau de la diapositive 22 | **L'erreur exacte du §2.3.11** : rapprocher ce tableau de celui des 17 132 milliers de familles et conclure à une chute du nombre de familles sans enfant, alors qu'elles sont simplement exclues du champ |
| **« Unité : milliers »** | Fixe l'ordre de grandeur | Lire « 3 578,3 familles » au lieu de 3,58 millions — exactement l'ambiguïté que crée la diapositive 22 en annonçant « 17 132 familles » |

**Synthèse attendue :** ces quatre mentions constituent la **définition et la délimitation
de la population** (étape 2) plus l'**unité de mesure** (diapositive 32). Sans elles, le
tableau reste lisible mais devient **incomparable** — et la comparaison est précisément
l'usage principal qu'on fait des données publiées.
:::

::: correction Corrigé du niveau 3 — question 3
**L'erreur est dans la seconde moitié de la phrase**, et elle porte sur la nature de la
variable, pas sur le codage.

**La variable *note*.** Les nombres de 0 à 20 sont de véritables **quantités** : l'écart
entre 8 et 10 est le même qu'entre 16 et 18, et une note de 12,5 a un sens. La moyenne est
donc licite. *(Sur son sous-type : la note relève d'une **mesure** de performance, donc
techniquement d'une variable **continue** ; si le barème n'admet que des entiers, on la
traite en pratique comme **discrète**. Signaler cette nuance est ce qu'attend un correcteur
exigeant.)*

**La variable *appréciation*.** Les codes 1 à 4 sont des **étiquettes ordonnées**. L'ordre
est réel — insuffisant < passable < bien < très bien — mais **les écarts n'ont aucun sens** :
rien ne garantit que passer d'« insuffisant » à « passable » représente le même progrès que
passer de « bien » à « très bien ». C'est une variable **qualitative ordinale**, et
**calculer sa moyenne n'a pas de sens** : « appréciation moyenne = 2,7 » ne désigne aucune
appréciation.

**Ce qu'on peut faire, exactement, avec chacune :**

| Opération | Note | Appréciation |
|---|:---:|:---:|
| Compter les effectifs par modalité | oui | oui |
| Calculer des fréquences | oui | oui |
| **Ordonner** les modalités | oui | **oui** (elle est ordinale) |
| Calculer des **fréquences cumulées** | oui | **oui** — l'ordre suffit |
| Calculer une **moyenne** | **oui** | **non** |
| Calculer un **écart** entre deux modalités | oui | **non** |

**La formulation à retenir :** le **test du codage** n'est pas « y a-t-il des chiffres ? »
mais « **les opérations arithmétiques ont-elles un sens ?** ». Et il faut distinguer deux
seuils : l'**ordre** autorise le cumul et la médiane ; seule la **quantité** autorise la
moyenne et les écarts.
:::

::: correction Corrigé du niveau 3 — question 4
**La démarche à montrer, avant toute réponse technique :** partir de la problématique. Que
veut le directeur commercial ? Deux problématiques distinctes se cachent derrière la
demande.

**A. « Où est mon chiffre d'affaires, et comment évolue-t-il ? »** → question de **volume**.
**B. « Mon poids par région se déforme-t-il ? »** → question de **structure**.

Ne pouvant trancher, on **présente les deux**, en le disant.

**1. Un tableau, d'abord.** Cinq lignes (régions) × trois colonnes (années), plus une ligne
« Ensemble ». Le tableau est la **présentation sans perte** ; il permet de retrouver
n'importe quel chiffre. Il porte : titre explicite, **unité** (« en milliers d'euros »),
**champ** (« chiffre d'affaires hors taxes, périmètre France, hors ventes en ligne »),
**source** et **date d'extraction**.

**2. Un diagramme empilé en effectifs**, une colonne par année, cinq segments par colonne.
Il répond à la problématique A : la **hauteur** donne le chiffre d'affaires total, les
**segments** la contribution de chaque région.

**3. Si et seulement si la question porte sur la structure**, un second diagramme **empilé
à 100 %**, en rappelant les totaux annuels sous les colonnes — sans quoi le lecteur ne
saurait pas si une part stable recouvre un volume en hausse ou en baisse.

**4. Le choix de ne pas faire.** Un **camembert par année** obligerait à comparer des
secteurs entre trois graphiques séparés : l'œil ne sait pas comparer des angles d'une figure
à l'autre. Le cours réserve le camembert à **une** répartition, pas à une comparaison de
répartitions.

**5. Les mentions obligatoires** (diapositive 32) : intitulés précis — « Chiffre d'affaires
hors taxes par région, 2022-2024 » et non « CA_REG » ; lisibilité par un non-spécialiste ;
**note de lecture** sous le tableau : *« Lecture : en 2024, la région Sud a réalisé 4 250
milliers d'euros de chiffre d'affaires hors taxes, soit 23,1 % du total. »*

**La phrase qui doit apparaître dans la copie :** le choix de la présentation **découle de
la problématique**, et non l'inverse.
:::

<!--saut-->
### Niveau 4 — Simulation d'examen

::: methode Conditions de passation
**Le support ne donne aucune indication sur le format ni sur la durée de l'épreuve.** La
simulation retient le format le plus courant pour un premier chapitre de statistique
descriptive : **1 h 30**, sur **20 points**, avec des questions de cours et deux exercices
chiffrés. **Calculatrice autorisée, documents interdits.** Ajustez ces paramètres dès que
les modalités réelles seront annoncées.

Chronomètre lancé. Répartition du temps conseillée : 20 min pour la partie A, 35 min pour
la partie B, 30 min pour la partie C, 5 min de relecture.
:::

#### Sujet

**PARTIE A — Questions de cours (6 points)**

**A.1** *(2 pts)* Citez les six étapes d'une étude statistique et énoncez le principe qui
relie chaque étape à la première.

**A.2** *(2 pts)* Définissez la fréquence et la fréquence cumulée. Démontrez que la somme
des fréquences vaut 1 et que la suite des fréquences cumulées est croissante.

**A.3** *(1 pt)* Une enquête code la variable « niveau de satisfaction » ainsi : 1 = très
insatisfait, 2 = insatisfait, 3 = satisfait, 4 = très satisfait. Quel est le type de cette
variable ? Peut-on en calculer la moyenne ? Justifiez.

**A.4** *(1 pt)* Qu'est-ce qu'un diagramme empilé à 100 % permet de voir, et qu'est-ce qu'il
détruit ?

**PARTIE B — Construction d'une distribution (7 points)**

Cinquante ménages d'un quartier ont été interrogés sur le nombre de personnes composant le
ménage. Série brute :

```
2 1 4 3 2 1 2 5 3 2   1 2 3 2 1 4 2 3 1 2
2 3 1 2 6 2 1 3 2 4   1 2 2 1 3 2 5 1 2 3
2 1 4 2 3 1 2 2 1 2
```

**B.1** *(2 pts)* Identifiez la population, les unités statistiques, l'effectif total, la
variable et son type — en justifiant le sous-type.

**B.2** *(3 pts)* Construisez le tableau complet de la distribution : modalités, effectifs,
fréquences, fréquences cumulées. Effectuez les trois contrôles de cohérence.

**B.3** *(1 pt)* Écrivez une phrase de lecture pour la fréquence de la modalité 2, puis pour
la fréquence cumulée de la modalité 3.

**B.4** *(1 pt)* Quelle part des ménages compte **au moins quatre personnes** ? Donnez les
deux méthodes de calcul.

**PARTIE C — Comparaison de deux distributions (7 points)**

Une commune a recensé la composition de ses ménages en 2015 et en 2024.

| Nombre de personnes | 2015 | 2024 |
|---|---:|---:|
| 1 personne | 1 240 | 1 560 |
| 2 personnes | 2 180 | 2 460 |
| 3 personnes | 860 | 700 |
| 4 personnes ou plus | 320 | 180 |
| **Ensemble** | **4 600** | **4 900** |

**C.1** *(1 pt)* Identifiez la population, les sous-populations, la variable de découpage et
la variable étudiée.

**C.2** *(2 pts)* Calculez la structure de chaque année, en pourcentage. Vérifiez vos
résultats.

**C.3** *(2 pts)* Que devient la modalité « 3 personnes », en part et en effectif ? Rédigez
une phrase de commentaire qui rende compte des deux.

**C.4** *(1 pt)* Un élu déclare : « les ménages de quatre personnes ou plus ne représentent
plus que 3,7 % : leur nombre s'est effondré. » L'affirmation est-elle correctement
justifiée ? Que faut-il vérifier ?

**C.5** *(1 pt)* Quel diagramme retenez-vous pour présenter ce tableau au conseil municipal ?
Justifiez par la problématique et indiquez les mentions obligatoires.

::: correction Corrigé type — « copie de major », avec le barème
**PARTIE A (6 pts)**

**A.1 (2 pts)** ① Quel type de **problématique** ? ② Choix des **données à observer**
(qui ?) ③ Choix de la **méthode de recueil** ④ **Campagne de mesures** ⑤ **Traitement** des
données ⑥ **Prise de décision**. *(1 pt pour les six étapes dans l'ordre.)*
Principe : **« tous les choix sont guidés par le type de problématique »** — les flèches de
retour du schéma remontent de chaque étape vers l'étape 1 ; aucune méthode n'est bonne dans
l'absolu, seulement adaptée ou non à la question posée. *(1 pt.)*

**A.2 (2 pts)** La **fréquence** $ f_i = n_i/n $ est la proportion d'individus présentant
**exactement** la modalité $ x_i $. La **fréquence cumulée** $ F_k = \sum_{i=1}^{k} f_i $
est la proportion présentant la modalité $ x_k $ **ou une modalité inférieure** — « au
plus ». *(0,5 pt.)*
$$ \sum_{i=1}^{p} f_i = \sum_{i=1}^{p}\frac{n_i}{n} = \frac{1}{n}\sum_{i=1}^{p} n_i = \frac{n}{n} = 1 $$
*(0,75 pt : 0,25 par étape — définition, sortie de $ n $, somme des effectifs.)*
$ F_k - F_{k-1} = f_k \ge 0 $ car une fréquence est positive ou nulle, donc
$ F_k \ge F_{k-1} $ : la suite est croissante. *(0,75 pt.)*

**A.3 (1 pt)** Variable **qualitative ordinale** *(0,5 pt)* : les modalités sont des
appréciations, non des quantités, mais elles sont **ordonnées**. **On ne peut pas calculer
sa moyenne** *(0,5 pt)* : les codes sont des étiquettes ordonnées et **les écarts entre eux
n'ont pas de sens** — rien ne garantit que l'écart 1→2 vaille l'écart 3→4. On peut en
revanche compter, calculer des fréquences, et cumuler, puisque l'ordre est défini.

**A.4 (1 pt)** Il permet de voir la **structure** de chaque sous-population et sa
déformation dans le temps, toutes les colonnes étant ramenées à la même hauteur. Il
**détruit toute information de volume** : une colonne de 100 % peut représenter n'importe
quel effectif total. D'où la règle : toujours indiquer les effectifs totaux à côté.

---

**PARTIE B (7 pts)**

**B.1 (2 pts)**
- Population : les **50 ménages interrogés** du quartier *(0,5)*.
- Unités statistiques : **un ménage** *(0,5)*.
- Effectif total : $ n = 50 $ *(0,25)*.
- Variable : le **nombre de personnes composant le ménage** *(0,25)*.
- Type : **quantitative discrète** *(0,5)* — les modalités sont des nombres issus d'un
  **comptage** ; entre 2 et 3 personnes, aucune valeur intermédiaire n'a de sens.

**B.2 (3 pts)** Méthode : **tri des modalités, puis comptage des effectifs**.

| $ x_i $ | $ n_i $ | $ f_i $ (%) | $ F_i $ (%) |
|---:|---:|---:|---:|
| 1 | 13 | 26,0 | 26,0 |
| 2 | 21 | 42,0 | 68,0 |
| 3 | 9 | 18,0 | 86,0 |
| 4 | 4 | 8,0 | 94,0 |
| 5 | 2 | 4,0 | 98,0 |
| 6 | 1 | 2,0 | 100,0 |
| **Ensemble** | **50** | **100,0** | — |

*(2 pts pour le tableau : 1 pt effectifs exacts, 0,5 fréquences, 0,5 cumulées.)*
Détail d'un calcul : $ f_2 = 21/50 = 0{,}42 = 42{,}0 $ %.
**Contrôles** *(1 pt)* : $ \sum n_i = 13+21+9+4+2+1 = 50 = n $ ✔ ;
$ \sum f_i = 100{,}0 $ % ✔ ; $ F $ croissante et $ F_6 = 100{,}0 $ % ✔.

**B.3 (1 pt)**
- « **42,0 %** des 50 ménages interrogés du quartier sont composés d'**exactement deux
  personnes**. » *(0,5)*
- « **86,0 %** des ménages interrogés comptent **au plus trois personnes**. » *(0,5)*

**B.4 (1 pt)** **14,0 %**.
- Par complément : $ 100 - F(3) = 100 - 86{,}0 = 14{,}0 $ % *(0,5)*.
- Par addition : $ 8{,}0 + 4{,}0 + 2{,}0 = 14{,}0 $ % *(0,5)*. Les deux concordent ✔

---

**PARTIE C (7 pts)**

**C.1 (1 pt)** Population : les **ménages de la commune**. Unités : **un ménage**.
Sous-populations : les ménages de **2015** et ceux de **2024**. Variable de **découpage** :
l'**année** ; variable **étudiée** : le **nombre de personnes du ménage** (quantitative
discrète, dernière modalité en **classe ouverte**).

**C.2 (2 pts)**

| Nombre de personnes | 2015 (%) | 2024 (%) | Écart (points) |
|---|---:|---:|---:|
| 1 personne | 27,0 | 31,8 | +4,8 |
| 2 personnes | 47,4 | 50,2 | +2,8 |
| **3 personnes** | **18,7** | **14,3** | **−4,4** |
| 4 personnes ou plus | 7,0 | 3,7 | −3,3 |
| **Total** | **100,1** | **100,0** | — |

Détail : $ 1\,240/4\,600 = 0{,}2696 \rightarrow 27{,}0 $ % ;
$ 860/4\,600 = 0{,}1870 \rightarrow 18{,}7 $ %.
**Contrôle** : la colonne 2015 totalise **100,1 %** — l'écart de 0,1 point est un **effet
d'arrondi**, et il doit être **signalé**, non corrigé en silence. *(1 pt structure exacte,
0,5 détail d'au moins un calcul, 0,5 contrôle et mention de l'arrondi.)*

**C.3 (2 pts)** La modalité « 3 personnes » perd **4,4 points de part** (18,7 % → 14,3 %)
*(0,5)* et **160 ménages en effectif** (860 → 700), soit **−18,6 %** *(0,5)*.
Commentaire attendu *(1 pt)* :
> « Entre 2015 et 2024, les ménages de trois personnes reculent à la fois en nombre — de
> 860 à 700, soit une baisse de 18,6 % — et en part — de 18,7 % à 14,3 %, soit 4,4 points.
> Le recul en part sous-estime le phénomène, puisqu'il s'inscrit dans un total en hausse de
> 6,5 % (4 600 à 4 900 ménages) : la part diminue **parce que** l'effectif baisse **et**
> que le total augmente. »

**C.4 (1 pt)** L'affirmation est **mal justifiée**. Une **part** ne dit rien du **nombre**
tant qu'on ne connaît pas le total *(0,5)*. Il faut vérifier l'**effectif** : ici,
320 → 180, soit **−140 ménages (−43,8 %)**. La conclusion de l'élu se trouve exacte, mais
**pour une raison qu'il n'a pas donnée** : c'est le calcul en effectif qui l'établit, pas la
part *(0,5)*. Une part peut chuter alors que l'effectif progresse, si le total progresse
plus vite.

**C.5 (1 pt)** **Un diagramme empilé en effectifs**, une colonne par année *(0,5)* : la
problématique d'un conseil municipal porte à la fois sur le **volume** (combien de ménages,
pour dimensionner écoles et services) et sur la **structure** (quelle composition). L'empilé
en effectifs montre les deux ; un empilé à 100 % masquerait la hausse du nombre total de
ménages.
**Mentions obligatoires** *(0,5)* : titre explicite (« Composition des ménages de la
commune, 2015 et 2024 »), **unité** (nombre de ménages), **champ** (ménages de la commune),
**source** et date, et une **note de lecture** : *« Lecture : en 2024, 700 ménages de la
commune étaient composés de trois personnes, soit 14,3 % de l'ensemble. »*

---

**Les cinq points qui font la différence sur cette épreuve.** A.2 (la démonstration écrite,
pas seulement la formule) · A.3 (refuser la moyenne sur une ordinale) · B.1 (justifier le
sous-type par comptage/mesure, pas l'affirmer) · C.2 (signaler l'arrondi à 100,1 % au lieu
de le masquer) · C.4 (démonter le raisonnement de l'élu tout en reconnaissant que sa
conclusion est exacte).
:::

<!--saut-->

## 6. Auto-évaluation finale

### 6.1 — Liste de contrôle

> Si l'une de ces questions reste sans réponse **sans regarder le document**, le chapitre
> n'est pas maîtrisé.

- [ ] J'énonce la chaîne « décider → information → étude » et j'explique son sens de lecture.
- [ ] Je cite les six étapes dans l'ordre et la légende du schéma.
- [ ] Je montre, sur l'exemple de l'hypermarché, pourquoi une problématique vague rend les
      étapes suivantes indéterminées.
- [ ] Je cite les quatre méthodes de recueil, avec pour chacune ce qu'elle permet et sa limite.
- [ ] Je cite les quatre familles de traitements et le chapitre correspondant.
- [ ] J'explique pourquoi ce n'est pas le rapport statistique qui décide.
- [ ] Je définis population, individu, effectif total, variable, modalité — sans hésiter.
- [ ] J'explique pourquoi la variable est définie comme une **application**, et j'en tire
      deux conséquences.
- [ ] Je qualifie n'importe quelle variable en deux questions, et je résiste au piège du
      codage numérique.
- [ ] Je distingue série brute et distribution, et je nomme le traitement qui fait passer de
      l'une à l'autre.
- [ ] J'écris $ n $, $ f_i $ et $ F_k $ de mémoire, et je démontre $ \sum f_i = 1 $ et la
      croissance de $ F $.
- [ ] Je construis un tableau complet à partir d'une série brute et j'effectue les trois
      contrôles.
- [ ] Je calcule un effectif à partir d'une fréquence, et une fréquence à partir de deux
      fréquences cumulées.
- [ ] J'écris une phrase de lecture complète : sous-population, valeur, unité, modalité, champ.
- [ ] Je choisis entre les quatre diagrammes en justifiant par la problématique.
- [ ] J'explique ce que l'empilement à 100 % détruit, et je sais démonter un raisonnement
      qui confond part et volume.
- [ ] Je cite les quatre règles de présentation et j'explique ce que signifie « informer ».
- [ ] Je distingue statistique descriptive et inférentielle, et je nomme la condition du
      tirage aléatoire.

### 6.2 — Grille de vérification chiffrée

| Épreuve | Conditions | Seuil | Résultat obtenu | Décision si sous le seuil |
|---|---|:---:|:---:|---|
| Niveau 1 — restitution | Sans document | 100 % | *…… / 22* | Reprendre la section du §2 correspondante, refaire la carte le jour même |
| Niveau 2 — application | Chronométré, sans document | 80 % | *…… %* | Refaire les exercices ratés à J+1, sans regarder le corrigé avant d'avoir cherché |
| Niveau 3 — maîtrise | Sans document | 3 sur 4 | *…… / 4* | Approfondissement sur la notion en cause |
| Niveau 4 — simulation | 1 h 30, sans document | 14/20 | *…… / 20* | Nouvelle simulation à J+7 avec d'autres données |
| Exposé blanc | À voix haute, 10 min, sans notes | Aucun blocage | *oui / non* | Le point de blocage **est** la notion mal comprise |

**Lecture des échecs.** Échec au niveau 1 → défaut de **mémorisation**. Échec au niveau 2
alors que le 1 est acquis → défaut de **méthode de calcul**. Échec au niveau 3 alors que le
2 est acquis → défaut de **compréhension**. Trois causes, trois traitements.

::: methode L'exposé blanc pour ce chapitre — le plan à tenir en 10 minutes
1. **(2 min)** La démarche : la chaîne, les six étapes, le principe des flèches de retour.
2. **(2 min)** Le vocabulaire : les cinq définitions, puis les deux questions qui donnent
   les quatre types de variables.
3. **(4 min)** La présentation : série brute → tri et comptage → distribution ; effectifs,
   fréquences, fréquences cumulées, avec les trois formules et les deux propriétés
   démontrées à voix haute.
4. **(2 min)** La comparaison : sous-populations, les quatre diagrammes et leur règle de
   choix ; puis « présenter, c'est informer » et l'ouverture inférentielle.
:::

### 6.3 — Protocole de révision daté

Document produit le **4 septembre 2026**. Les échéances sont donc :

| Échéance | Date | Durée | Ce qui est révisé |
|---|---|:---:|---|
| **J+1** | 5 septembre 2026 | 20 min | Fiche de synthèse (§4.1) + les 45 cartes (§4.2) + relecture du schéma (§4.4) |
| **J+3** | 7 septembre 2026 | 30 min | Cartes échouées à J+1 + niveau 1 complet, chronométré |
| **J+7** | 11 septembre 2026 | 45 min | Liste de contrôle à froid (§6.1) + exercices 2, 3 et 4 du niveau 2 + relecture des points de vigilance (§3) |
| **J+21** | 25 septembre 2026 | 90 min | Simulation d'examen complète (niveau 4) en 1 h 30, puis auto-correction au barème |

**Règle de décision.** Une carte échouée **deux fois de suite** relève de la compréhension,
pas de la mémoire : reprenez la section du §2 correspondante, et non la carte.

<!--saut-->

## Annexe — Tableau de couverture du support d'origine

Preuve de complétude, vérifiable en deux minutes. Le support d'origine — *CHAPITRE 1 :
Présenter pour informer*, Hélène Couprie, 33 diapositives — est inventorié ci-dessous
**diapositive par diapositive**, sans trou de numérotation.

**Légende.** ✔ traité intégralement — ⚠ traité, mais support d'origine incomplet, ambigu ou
erroné : la reconstruction est signalée à l'endroit exact — ✖ impossible à traiter, donnée
manquante.

| # | Élément du support d'origine | Nature | Traité dans | État |
|:---:|---|---|---|:---:|
| 1 | Page de titre : « CHAPITRE 1 : Présenter pour informer », Hélène Couprie, Portail L1 – DIV A, 2026-27 | titre | En-tête du document | ✔ |
| 2 | Contenu et plan du chapitre (3 sections) | plan | §2, encadré d'ouverture — y compris l'écart « statisticienne / statisticien » | ✔ |
| 3 | Section 1 ; chaîne « décider → information → étude » ; 4 exemples | problématisation | §2.1.1, avec la décision sous-jacente à chaque exemple | ✔ |
| 4 | **Les 6 étapes d'une étude statistique** — schéma **sans aucun texte** | image non commentée | §2.1.2 : schéma redessiné, flèches de retour et légende explicitées | ✔ |
| 5 | Étape 1 : quel type de problématique ? Exemple de l'hypermarché, 4 pistes | méthode | §2.1.3, avec la démonstration de l'indétermination des étapes suivantes | ✔ |
| 6 | Étape 2 : choix des données à observer — « qui ? » | méthode | §2.1.4, « définir / délimiter » explicité, incise sur la taille inconnue commentée | ✔ |
| 7 | Étape 3 : les 4 méthodes de recueil | méthode | §2.1.5, tableau avec apports et limites + grille de décision reconstruite | ✔ |
| 8 | Étape 4 : campagne de mesures — combien, quand, comment | méthode | §2.1.6 | ✔ |
| 9 | Étape 5 : traitement des données ; les 4 chapitres du cours | méthode + programme | §2.1.7, tableau des quatre traitements | ✔ |
| 10 | Étape 6 : prise de décision ; contenu du rapport ; « la décision est politique » | méthode | §2.1.8, avec la démonstration du passage « ce qui est » → « ce qu'il faut faire » | ✔ |
| 11 | Section 2 : les 5 définitions ; convention majuscule/minuscule | définitions | §2.2.1, « application » démontré terme à terme | ✔ |
| 12 | Illustration Insee « Vécu et ressenti en matière de sécurité » 2024 + **question posée** | exercice oral | §2.2.2 : tableau reproduit, question **entièrement corrigée**, total recalculé | ✔ |
| 13 | Types de variables : 2 types, 4 sous-types ; avertissement sur le codage | définitions | §2.2.3, arbre de décision + double piège du codage | ✔ |
| 14 | Illustration : 4 exemples de variables **sans indication de type** | exercice implicite | §2.2.4 : type et justification ajoutés pour les quatre | ✔ |
| 15 | Section 3 : 2 façons de présenter ; tri puis comptage | définitions | §2.3.1, avec la raison de la restriction au quantitatif/ordinal | ✔ |
| 16 | Distribution observée des effectifs ; effectif d'une modalité | définition | §2.3.2 | ✔ |
| 17 | **Série brute** des 87 étudiants | données | §2.3.3, série reproduite — **et recomptée** au §2.3.4 | ⚠ |
| 18 | Série ordonnée | données | §2.3.3, reproduite et vérifiée (87 valeurs, effectifs conformes au tableau) | ✔ |
| 19 | Tableau de la distribution des effectifs | données | §2.3.3 et §2.3.4 | ✔ |
| 20 | Diagramme en colonnes de la distribution | graphique non commenté | §2.3.3 : construction décrite, **rôle des modalités d'effectif nul** expliqué | ✔ |
| 21 | Répartition ; fréquence ; camembert ou barres ; fréquence cumulée | définitions | §2.3.5, avec la nuance sur le qualitatif ordinal | ✔ |
| 22 | Tableau des 17 132 (milliers de) familles + **question posée** | exercice oral | §2.3.6 : question corrigée, **toutes les fréquences recalculées**, ambiguïté de l'unité signalée | ⚠ |
| 23 | Formalisation : $ X $, $ x_i $, $ n_i $, $ n $, $ f_i $, $ F_k $ ; renvoi à « la diapo 21 » | notations | §2.3.7 : chaque symbole explicité, 3 propriétés démontrées, renvoi résolu | ✔ |
| 24 | Plusieurs distributions d'un même caractère : principe | définition | §2.3.8, avec la mise en évidence des deux variables en jeu | ✔ |
| 25 | Tableau des personnes écrouées 2020-2023 + **questions posées** | exercice oral | §2.3.9 : questions corrigées, totaux recalculés, structure des modalités explicitée | ✔ |
| 26 | Diagramme colonnes groupées 1 — groupement par catégorie | graphique | §2.3.10, construction et lecture décrites | ✔ |
| 27 | Diagramme colonnes groupées 2 — groupement par année | graphique | §2.3.10, avec la règle de choix entre les deux | ✔ |
| 28 | Tableau du nombre d'enfants par famille 1990-2023 + **questions posées** | exercice oral | §2.3.11 : questions corrigées, colonnes vérifiées, piège du champ signalé | ✔ |
| 29 | Diagramme de type empilé (effectifs) | graphique | §2.3.11 | ✔ |
| 30 | Diagramme empilé à 100 % + **2 questions posées** (phrase de lecture, calcul du 12,6) | exercice oral | §2.3.11 : les deux questions corrigées, calcul refait, piège part/volume démontré | ✔ |
| 31 | Diagramme colonne 1975-2008 ; « même contenu que le tableau précédent » | graphique + renvoi ambigu | §2.3.11 : valeurs relevées à haute résolution, **renvoi identifié** par comparaison des chiffres | ⚠ |
| 32 | Les 4 règles de présentation ; « informer = donner une forme » | méthode | §2.3.12, avec ce que chaque règle interdit | ✔ |
| 33 | Remarques conclusives ; ouverture sur la statistique inférentielle | synthèse | §2.4, tableau descriptive / inférentielle | ✔ |

::: piege Les trois ⚠ — ce qui a été vérifié, corrigé ou reconstruit
**Diapositive 17 — la série brute ne correspond pas au tableau.** Recomptée valeur par
valeur (sur l'image d'origine, pas sur une transcription), elle donne **10 zéros et 24
deux**, alors que la série ordonnée (diapo 18) et le tableau (diapo 19), **cohérents entre
eux**, donnent **11 zéros et 23 deux**. L'un des « 2 » de la série brute devrait être un
« 0 ». Les deux comptages totalisent bien 87. **Conduite à tenir :** utiliser le tableau du
cours en examen, et signaler la coquille à l'enseignante. Traité au §2.3.4.

**Diapositive 22 — l'unité.** Le texte annonce « enquête menée auprès de 17 132 familles »
alors que l'en-tête de colonne indique « effectifs en **milliers** ». La lecture correcte
est **17 132 milliers de familles**, soit environ 17,1 millions. Traité au §2.3.6.

**Diapositive 31 — le renvoi « le tableau précédent ».** Le tableau qui précède
immédiatement (diapo 28) ne correspond ni aux années ni aux modalités du diagramme. La
comparaison des chiffres établit que le renvoi désigne **le tableau de la diapositive 22** :
la colonne 2008 en reproduit exactement les cinq fréquences. Cette identification date de
2008 l'enquête de la diapositive 22 — information absente du support. Traité au §2.3.11,
avec mention explicite qu'il s'agit d'une déduction.

**Aucun ✖ : aucune donnée du support n'était illisible ou manquante.** Les 33 diapositives
sont couvertes.
:::

---

::: synthese Ce document est-il complet ?
Les douze contrôles de la charte (`academy/SYSTEME.md`, section 9) ont été passés :
définitions posées, notations expliquées symbole par symbole, formules démontrées et
illustrées par des exemples chiffrés intégraux, prérequis enseignés (proportion, signe
somme, dénombrabilité, lecture de tableau), **les six questions posées à l'amphithéâtre
intégralement corrigées**, six sections obligatoires présentes, quatre niveaux
d'entraînement corrigés, 45 cartes couvrant l'ensemble des notions, **tous les chiffres du
support recalculés** — ce qui a révélé trois anomalies, toutes signalées et localisées —
et un tableau de couverture des 33 diapositives sans trou de numérotation.

**La relecture du support d'origine n'est pas nécessaire.**
:::
