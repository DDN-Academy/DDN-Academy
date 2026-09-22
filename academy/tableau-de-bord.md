# Tableau de bord — pilotage du semestre

Support du **mode stratégie** : décider chaque semaine où va le temps de travail.
Les cases entre crochets sont à remplir ; rien n'y est présumé.

---

## 1. Matières du semestre

Six matières, **30 crédits**, répartis en trois BCC (source : diapositive 3 du cours de
Principes d'économie). Les crédits sont désormais connus ; **les coefficients de pondération
CC/CT, les dates et les formats d'épreuve restants ne sont pas supposés.**

| Matière | Crédits | BCC | Format de l'épreuve | Date | Niveau /5 | Chapitres traités | État V2 |
|---|:---:|:---:|---|---|:---:|---|---|
| **Principes d'économie** | **6** | 1 | **CT 1 h 30, questions de cours + exercices** · CC = examen de TD en présentiel | *[date]* | *[ ]* | **1** — Introduction générale ✔ | ✅ **V2** |
| **Principes de gestion** | **6** | 1 | **CT = QCM** (pas de points négatifs, une mauvaise alternative annule une bonne, ≥ 2 correctes par question) · CC = écrit en TD à mi-semestre · note = $ \max(\text{CT}\ ;\ \tfrac{1}{3}\text{CC}+\tfrac{2}{3}\text{CT}) $ | *[date]* | *[ ]* | **2** — CM 1 ✔, CM 2 ✔ | ✅ **V2** |
| **Techniques statistiques** | **5** | 2 | *[non donné par le support — hypothèse : écrit, exercices d'application + questions de cours, sans document]* | *[date]* | *[ ]* | **2 / 4** — CHAP 1 ✔, CHAP 2 ; restent « évolutions temporelles » et « croiser » | 🟡 **CHAP 1 en V2**, CHAP 2 à refaire |
| **Institutions politiques** | **6** ¹ | 2 | *[format non donné par le support — hypothèse : écrit, questions de cours et question développée]* | *[date]* | *[ ]* | **1** — Partie 1, chapitre 1 « L'État » ✔ | ✅ **V2** |
| **Introduction au droit** | **6** ¹ | 2 | *[à confirmer]* | *[date]* | *[ ]* | **0** — aucun cours transmis | — |
| **Mathématiques 1** | **5** | 3 | *[à confirmer]* | *[date]* | *[ ]* | **0** — aucun cours transmis | — |
| Ecri+ | 1 | 3 | — | — | — | — | — |
| GoFluent | 1 | 3 | — | — | — | — | — |

¹ **Introduction au droit** et **Institutions politiques** forment ensemble l'unité
« Environnement des organisations », dotée de **6 crédits** au total — la répartition interne
entre les deux enseignements n'est pas donnée par le support.

**Constat au 22 septembre 2026.** Deux matières sur six n'ont reçu aucun document :
**introduction au droit** et **mathématiques 1**, soit **11 crédits sur 30** à l'aveugle.
C'est le déséquilibre le plus coûteux du tableau : une matière à niveau 1 ou 2 offre
mécaniquement le meilleur rendement horaire (section 2).

---

## 1 bis. Charge de lecture par chapitre

Depuis la refonte V2 du 15 septembre 2026, le critère est la **charge de lecture** — blocs 0,
1, 2 et 5 — plafonnée à **35 pages**. Le reste se pratique ou se consulte et ne compte pas.

| Chapitre | Format | Pages totales | **À lire** | Sous le plafond ? |
|---|:---:|:---:|:---:|:---:|
| `economie-01-introduction-generale` | **V2** | 65 | **34** | ✅ |
| `gestion-01-introduction-au-management` | **V2** | 54 | **25** | ✅ |
| `gestion-02-qui-doit-etre-roi` | **V2** | 46 | **23** | ✅ |
| `institutions-01-l-etat` | **V2** | 67 | **35** | ✅ *(au plafond)* |
| `stats-01-presenter-pour-informer` | **V2** | 59 | **23** | ✅ |
| `stats-02-resumer-pour-informer` | V1 | 73 | 27 | ❌ à refaire |

*La version intégrale de `institutions-01` (V1, 142 p.) a été supprimée : la V2 fusionne les deux
sources dans un document unique, et ses numéros de paragraphes ne correspondaient plus. Elle
reste récupérable dans l'historique git.*

**Ordre de refonte retenu**, par crédits décroissants puis par lourdeur : économie 01 ✔ ·
gestion 01 ✔ · gestion 02 ✔ · institutions 01 ✔ · stats 01 ✔ · **reste : stats 02**
(27 pages à lire).

**Cinq chapitres sur six sont en V2.** Reste le chapitre 2 de Techniques statistiques.

**Principes de gestion est désormais intégralement couvert en V2** : les deux CM transmis sont
refondus, et la stratégie de QCM est commune aux deux documents.

**Techniques statistiques CHAP 1 est en V2 depuis le 22 septembre 2026** : 59 pages dont
**23 à lire**, 68 cartes, les **cinq exercices que le support pose sans corrigé** traités en
série B, **quatre anomalies** vérifiées à l'image et un tableau de couverture des
**33 diapositives** — 9 ✔, 24 ⚠, 0 ✖. **Le format d'épreuve reste inconnu** : la série D
repose sur une hypothèse explicite, annoncée au bloc 0.

---

## 1 ter. Couverture réelle du programme — le vrai risque

Les documents existants sont complets **par rapport aux supports transmis** (garantie n° 1 de
`SYSTEME.md`, § 0 bis). Mais **les supports transmis ne couvrent pas encore le programme.**
Voici l'écart, sans arrondi favorable.

| Matière | Crédits | Au programme | Couvert | Reste |
|---|:---:|---|:---:|---|
| **Principes de gestion** | 6 | **10 séances de CM** (syllabus du CM 1) | **2** | **8 séances** |
| **Principes d'économie** | 6 | **Introduction + Partie 1 macro + Partie 2 micro** | **1** (l'introduction) | **Les deux parties de fond** |
| **Techniques statistiques** | 5 | **≥ 4 chapitres** (le chapitre 4 est annoncé au chapitre 1) | **2** | **≥ 2 chapitres** |
| **Institutions politiques** | 6 ¹ | Partie 1, **étendue inconnue** | **1 chapitre** | Inconnu · + la **Section III** absente |
| **Introduction au droit** | 6 ¹ | **Inconnu** | **0** | **Tout** |
| **Mathématiques 1** | 5 | **Inconnu** | **0** | **Tout** |

**Le constat à retenir : 11 crédits sur 30 — Introduction au droit et Mathématiques 1 —
n'ont reçu aucun document.** Et sur les 19 crédits couverts, la couverture va de 20 % (gestion)
à 50 % (statistiques).

::: piege Ce que cela signifie concrètement
Les cinq documents V2 produits sont **intégralement fiables sur leur périmètre** : le tableau de
couverture de chacun le prouve ligne à ligne. Mais **leur périmètre représente aujourd'hui une
fraction du semestre**.

**Aucune méthode ne compense un chapitre non transmis.** C'est le premier facteur de risque du
dispositif, et c'est le seul que l'envoi d'un fichier suffit à supprimer. La liste priorisée
est à la **section 12 de `SYSTEME.md`**.
:::

---

## 2. Règle d'arbitrage

Le temps disponible est fini. Il va là où un point de moyenne coûte le moins d'heures.

> **Priorité = coefficient × (5 − niveau actuel) × urgence**

où le facteur d'urgence dépend de l'échéance :

| Échéance | Facteur d'urgence |
|---|:---:|
| Moins de 7 jours | 3 |
| 8 à 21 jours | 2 |
| Plus de 21 jours | 1 |

On traite la priorité la plus élevée d'abord. Trois conséquences, contre-intuitives mais
mécaniques :

1. **Un coefficient élevé déjà maîtrisé (niveau 4-5) ne rapporte presque plus rien.**
   Passer de 16 à 17 coûte plus d'heures que passer de 8 à 12 ailleurs.
2. **Une matière à faible coefficient très faible reste prioritaire** si l'écart au
   niveau maximal est grand et l'échéance proche : c'est le produit qui décide, pas
   l'intuition.
3. **L'urgence ne remplace jamais le coefficient**, elle le multiplie. Une matière à
   coefficient 1 qui tombe demain ne passe pas devant un coefficient 6 qui tombe dans dix jours.

> **Révision de l'arbitrage — chaque dimanche.** Les niveaux évoluent, les échéances se
> rapprochent, l'ordre change. Un tableau de bord non mis à jour produit de mauvaises
> décisions avec l'apparence de la méthode.

---

## 3. Suivi de la répétition espacée — protocole V2 à huit séances

Depuis la refonte du 15 septembre 2026, chaque document impose **huit séances sur trois
semaines**, jamais plus de 45 à 50 minutes d'affilée : **S1** découverte (J0, bloc 2 lu une
fois) · **S2** ancrage (J+1, bloc 1 + série A) · **S3** rappel (J+2, les seuls échecs + bloc 3)
· **S4** méthode (J+4, série B chronométrée) · **S5** consolidation (J+7, série A à froid +
bloc 5) · **S6** maîtrise (J+12, série C rédigée) · **S7** simulation (J+18, série D à la durée
réelle) · **S8** veille (bloc 1 + bloc 5 seuls).

**Les dates ci-dessous sont calculées depuis la date de production de chaque document V2.**
`stats-01` est volontairement décalé d'un jour sur `institutions-01`, tous deux produits le
22 septembre : les faire démarrer le même jour mettait 3 heures sur une seule soirée.

| Chapitre | J0 | S2 | S3 | S4 | S5 | S6 | S7 *(simulation)* | S8 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Économie — introduction générale** | ☐ 15 sept. | ☐ 16 | ☐ 17 | ☐ 19 | ☐ **22** | ☐ 27 | ☐ **3 oct.** *(1 h 30)* | ☐ veille |
| **Gestion — CM 1, management** | ☐ 20 sept. | ☐ 21 | ☐ **22** | ☐ 24 | ☐ 27 | ☐ 2 oct. | ☐ **8 oct.** *(45 min)* | ☐ veille |
| **Gestion — CM 2, qui doit être roi ?** | ☐ 21 sept. | ☐ **22** | ☐ 23 | ☐ 25 | ☐ 28 | ☐ 3 oct. | ☐ **9 oct.** *(45 min)* | ☐ veille |
| **Institutions politiques — l'État** | ☐ **22 sept.** | ☐ 23 | ☐ 24 | ☐ 26 | ☐ 29 | ☐ 4 oct. | ☐ **10 oct.** *(1 h)* | ☐ veille |
| **Techniques statistiques — CHAP 1** | ☐ **23 sept.** | ☐ 24 | ☐ 25 | ☐ 27 | ☐ 30 | ☐ 5 oct. | ☐ **11 oct.** *(1 h)* | ☐ veille |

*`stats-02` et son intégrale restent en V1 : ils ne suivent pas encore ce protocole et seront
replanifiés à leur refonte.*

### La charge réelle, jour par jour

| Date | Ce que tu fais | Total |
|:---:|---|:---:|
| **22 sept.** | Éco **S5** (35) · Gestion 1 **S3** (25) · Gestion 2 **S2** (35) · Institutions **S1** (50) | **2 h 25** |
| **23 sept.** | Gestion 2 **S3** (25) · Institutions **S2** (40) · Stats **S1** (45) | **1 h 50** |
| **24 sept.** | Gestion 1 **S4** (40) · Institutions **S3** (25) · Stats **S2** (30) | **1 h 35** |
| **25 sept.** | Gestion 2 **S4** (40) · Stats **S3** (25) | **1 h 05** |
| **26 sept.** | Institutions **S4** (40) | **40 min** |
| **27 sept.** | Éco **S6** (45) · Gestion 1 **S5** (35) · Stats **S4** (40) | **2 h** |
| **28 sept.** | Gestion 2 **S5** (35) | **35 min** |
| **29 sept.** | Institutions **S5** (35) | **35 min** |
| **30 sept.** | Stats **S5** (35) | **35 min** |
| **2 oct.** | Gestion 1 **S6** (40) | **40 min** |
| **3 oct.** | Éco **S7** — simulation 1 h 30 · Gestion 2 **S6** (40) | **2 h 10** |
| **4 oct.** | Institutions **S6** (45) | **45 min** |
| **5 oct.** | Stats **S6** (40) | **40 min** |
| **8 · 9 · 10 · 11 oct.** | Les quatre simulations restantes, une par soir | **45 · 45 · 60 · 60 min** |

**Total restant : 19 h 05 réparties sur trois semaines**, plus les cinq séances S8 (1 h 45 au
total) à placer la veille de chaque épreuve. **Aucune soirée ne dépasse 2 h 25.**

**Deux règles qui priment sur le calendrier :**
1. **Une carte ratée deux fois de suite n'est pas un problème de mémoire, c'est un problème de
   compréhension.** Elle déclenche un retour au bloc 2 sur cette notion, pas une relecture.
2. **Une séance sautée se rattrape le lendemain, jamais en doublant la suivante.** L'espacement
   fait le travail ; l'entassement le défait.

**Ordre conseillé à l'intérieur d'une soirée chargée :** **cartes de gestion d'abord**
(mémorisation pure, la plus rapide) · **institutions politiques ensuite** (définitions et
textes à citer) · **économie puis statistiques en dernier** (calculs et graphiques, qui
demandent du papier).

### Le seul chapitre encore en deux fichiers

`stats-02` existe en **cours** — celui qu'on lit — et en **version intégrale**, qu'on ouvre
ponctuellement quand un point résiste. **Les numéros de paragraphes sont identiques dans les
deux.** Tous les autres chapitres sont en fichier unique depuis la refonte V2.

| Chapitre | Fichier à lire | Charge de lecture | Version intégrale |
|---|---|:---:|:---:|
| Stats — CHAP 2 « Résumer pour informer » | `stats-02-resumer-pour-informer` | **27 p.** | 112 p. |

---

## 4. Objectif à trois ans — AST2, Master Finance EDHEC

Ce que la L1 construit dès maintenant :

- **Le dossier académique** : moyennes générales et, lorsqu'il est communiqué, le rang
  dans la promotion. C'est la part la plus lourde et la seule qui ne se rattrape pas —
  une note de L1 est définitive.
- **La régularité** : une progression L1 → L2 → L3 lisible pèse davantage qu'un semestre
  brillant isolé.
- **L'anglais** : le niveau se prépare sur trois ans, pas trois semaines. Test de langue
  et entretien éventuel en anglais.
- **Les expériences** : stages, associations, projets. Une expérience de marché
  documentée et chiffrée est un différenciateur réel — à condition d'être présentée
  comme un travail méthodique, pas comme un pari.
- **Le récit de candidature** : cohérence entre le parcours, les expériences et le
  projet professionnel.

> **À vérifier, non supposé.** Les modalités exactes d'admission (voie AST concernée,
> test requis — TAGE MAGE, GMAT ou autre —, score de langue attendu, calendrier) doivent
> être relevées sur le site de l'EDHEC pour l'année de candidature, puis reportées ici.
> Elles évoluent d'une année sur l'autre et ne sont pas reproduites de mémoire dans ce
> document.

| Élément à confirmer | Source | Vérifié le | Exigence relevée |
|---|---|---|---|
| Voie d'admission AST2 | *[site EDHEC]* | *[date]* | *[ ]* |
| Test d'admission | *[ ]* | *[ ]* | *[ ]* |
| Niveau d'anglais exigé | *[ ]* | *[ ]* | *[ ]* |
| Calendrier de candidature | *[ ]* | *[ ]* | *[ ]* |
