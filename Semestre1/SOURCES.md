---
titre: Inventaire des sources
sous_titre: Tout ce qui a été reçu, ce qui en a été tiré, et ce qui manque — par matière
resume: Mis à jour à chaque document reçu. Les originaux de la faculté ne sont jamais commités — le dépôt est public — ; ils se déposent dans Semestre1/<Matiere>/Sources/, exclu par .gitignore, et disparaissent en fin de session. Ce fichier est donc la trace durable de chaque source.
date: 28 septembre 2026
sommaire: oui
---

# Règles de tenue

| Règle | Pourquoi |
|---|---|
| Un original reçu va dans `<Matiere>/Sources/`, **jamais dans git** | Le dépôt est **public** : on n'y publie ni les supports des enseignants ni les notes d'un tiers |
| Il est inscrit ici **le jour même** : nature, volume, date, cours qui l'exploite | Le conteneur de travail est effacé à chaque fin de session : ce fichier est la seule trace |
| Une note manuscrite est **transcrite intégralement** avant d'être exploitée | Consigne de la charte ; la transcription peut être commitée si elle ne contient que du contenu de cours |
| Deux sources qui se contredisent : la contradiction est **signalée dans le cours**, avec la source retenue et la raison | Consigne de la charte |
| **Annales et fiches de TD priment** pour calibrer le niveau et le format | Consigne de la charte : elles montrent ce que l'enseignant attend réellement |

# 1 — Documents reçus

**Six supports, sept documents, tous reçus en septembre 2026.** Chacun a été reconstruit en septembre
diapositive par diapositive, avec un tableau de couverture sans trou. **Les fichiers originaux ne
sont plus disponibles** : ils étaient dans un conteneur de travail précédent, effacé depuis. Les
reconstructions vérifiées servent de référence, et chaque tableau de couverture est repris dans
l'annexe B du nouveau cours.

| Matière | Document reçu | Nature | Volume | Enseignant(e) | Cours reconstruit | Couverture vérifiée |
|---|---|---|:---:|---|---|---|
| **Principes d'économie** | « 26-27 Partie 1 intro » | Diapositives de CM — introduction générale | **53 diapositives** | non nommé sur le support | `Economie/Cours/Economie_Ch01_Introduction_generale` | 53 lignes · 34 ✔ · 19 ⚠ · 0 ✖ |
| **Principes de gestion** | CM 1 — Introduction au management | Diapositives de CM | **49 diapositives** | Pr. Agulhon (coordination CM, Aix) | `Gestion/Cours/Gestion_Ch01_Introduction_au_management` | 49 lignes · 24 ✔ · 25 ⚠ · 0 ✖ |
| **Principes de gestion** | CM 2 — Actionnaire, client, salarié ou public : qui doit être roi ? | Diapositives de CM | **50 diapositives** | *idem* | `Gestion/Cours/Gestion_Ch02_Qui_doit_etre_roi` | 50 lignes · 26 ✔ · 24 ⚠ · 0 ✖ |
| **Techniques statistiques** | CHAPITRE 1 — Présenter pour informer | Diapositives de CM | **33 diapositives** | Hélène Couprie, L1 Portail Division A | `Statistiques/Cours/Statistiques_Ch01_Presenter_pour_informer` | 33 lignes · 9 ✔ · 24 ⚠ · 0 ✖ |
| **Techniques statistiques** | CHAPITRE 2 — Résumer pour informer | Diapositives de CM | **70 diapositives** | *idem* | `Statistiques/Cours/Statistiques_Ch02_Resumer_pour_informer` | 70 diapositives couvertes · 4 anomalies du support |
| **Institutions politiques** | Polycopié — M. Verpeaux, *Droit constitutionnel 1*, Leçon 1 « L'État et le pouvoir politique », UNJF | Cours rédigé | **16 pages** | — | `Institutions_politiques/Cours/Institutions_politiques_Ch01_L_Etat` | fusionné avec la ligne suivante |
| **Institutions politiques** | Diapositives « L'État » | Diapositives de CM | **10 diapositives** | signées S.H. | *idem* | 27 éléments · 12 ✔ · 14 ⚠ · **1 ✖** (Section III annoncée, absente) |
| Introduction au droit | — | — | **rien** | — | — | — |
| Mathématiques 1 | — | — | **rien** | — | — | — |
| Ecri+ | — | — | **rien** | — | — | — |
| GoFluent | — | — | **rien** | — | — | — |

**Ce que les supports ont appris sur la maquette** (diapositive 3 du cours d'économie, diapositive 21
du CM 1 de gestion) : 30 crédits en trois BCC ; Principes d'économie 30 h de CM et 12 h de TD,
CT de 1 h 30 « questions de cours + exercices » et CC en TD ; Principes de gestion CT en QCM,
CC écrit en TD à mi-semestre, note = max(CT ; ⅓ CC + ⅔ CT). Ton groupe : **L1 Portail,
Division A**, site d'Aix (Pauliane) — scolarité : **Virginie Bamas**.

<!--saut-->

# 2 — Ce qui manque, par ordre d'urgence

::: piege Les quatre demandes de cette semaine — chacune débloque des points
| № | Ce qu'il me faut | Ce que ça débloque |
|:---:|---|---|
| **1** | **Tous les supports de Mathématiques 1** parus depuis la rentrée — y compris la mise à niveau | 5 ECTS, la matière la plus difficile du semestre, **zéro document** : tu vas en TD de maths chaque semaine sans cours |
| **2** | **Tous les supports d'Introduction au droit** | La moitié de l'unité « Environnement des organisations » (6 ECTS), **zéro document** |
| **3** | **Ton emploi du temps de TD** (jours, heures, matières) | Le planning suppose un TD par matière et par semaine, à des jours fixés au hasard : **toutes les préparations et consolidations de TD en dépendent** |
| **4** | **Les modalités de contrôle des connaissances (MCC)** et le **calendrier des examens** — sur Ametice ou auprès de la scolarité | Format, durée et coefficients des épreuves de Stats, Maths, Droit, Institutions, Ecri+ et GoFluent ; dates des contrôles continus ; ordre des épreuves du 7 au 18 décembre |
:::

| Priorité | Ce qui manque | Matière | Crédits en jeu | Où le trouver |
|:---:|---|---|:---:|---|
| **5** | Les CM parus depuis ceux que j'ai : **CM 3 à 5 de gestion** (déjà faits en amphi), la **Partie 1 d'économie**, le **chapitre 3 de statistiques**, la **suite d'Institutions politiques** et la **Section III** annoncée et absente du polycopié | Toutes | 22 | Ametice |
| **6** | **Les fiches de TD** — énoncés, puis corrections — au fil des séances | Toutes | — | Tes TD |
| **7** | **Les documents de ta marraine** — annales et corrigés d'abord, puis notes de CM, puis fiches | Toutes | — | Ta marraine ; photos acceptées, je transcris |
| **8** | Les **modalités d'Ecri+ et de GoFluent** : heures ou activités exigées, tests, dates limites | Ecri+, GoFluent | 2 | Ametice / plateformes |
| **9** | Le **nom du manuel de référence** d'économie (annoncé, non nommé, diapositive 9) | Économie | — | L'enseignant, un camarade |
| **10** | Les **questions Wooclap** posées en amphi, ou une photo des notes d'un camarade | Toutes | — | Seule trace de ce sur quoi l'enseignant insiste |
| **11** | *Facultatif* : les **fichiers originaux des six supports déjà traités**, pour un second contrôle croisé | Économie, Gestion, Stats, Institutions | — | Ametice |

# 3 — Journal des réceptions

| Date | Document | Matière | Déposé dans `Sources/` | Traité dans |
|---|---|---|:---:|---|
| septembre 2026 | Les sept documents du § 1 | Économie, Gestion, Stats, Institutions | non conservés | cours reconstruits, versions 1 et 2 ; reconstruits au format du 28 septembre (version 3) |
