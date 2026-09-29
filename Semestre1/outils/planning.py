#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
planning.py — le planning glissant du semestre (Livrable 2 de la charte).

    python3 Semestre1/outils/planning.py           # écrit Semestre1/PLANNING.md, affiche le bilan
    python3 Semestre1/outils/planning.py --bilan   # bilan seulement

Lit Semestre1/planning.json. Un chapitre n'est planifié que si son cours reconstruit existe :
le planning grandit à mesure que les cours arrivent (amendement du 29 septembre). Il ne contient
que des données réelles ; ce qui manque est listé dans PLANNING.md.

Chaque jour de préparation, du 1er octobre au 6 décembre, dans cet ordre :
  1. la marge du dimanche : la moitié des pomodoros du jour ;
  2. les engagements fixes, dès que leurs dates sont connues : examen blanc (correction le
     lendemain), préparation de contrôle continu (J-2 et J-1), préparation de TD (la veille ;
     le samedi pour un TD du lundi), consolidation de TD (le jour même) ;
  3. les révisions espacées dues — J+1, J+3, J+7, J+21 après la fin de l'apprentissage d'un
     chapitre, puis tous les 21 jours —, deux chapitres par pomodoro ;
  4. l'entraînement dû — niveau 2 à J+2, niveau 3 à J+4, niveau 4 à J+8 —, un pomodoro par jour ;
  5. l'apprentissage — cycles APPRENDRE P1 → P4, une section du cours par cycle — ; deux
     chapitres de matières différentes sont entrelacés quand c'est possible ;
  6. le reste : créneaux réservés aux prochains cours.
Contrôle : chaque jour consomme exactement sa capacité, et le total vaut 560 pomodoros.
"""
import json
import os
import re
import sys
from collections import defaultdict
from datetime import date, timedelta

ICI = os.path.dirname(os.path.abspath(__file__))
SEM = os.path.dirname(ICI)
JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
MOIS = ["", "janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
        "septembre", "octobre", "novembre", "décembre"]
ETAPES = ["P1 lecture active", "P2 restitution de mémoire", "P3 cartes de la section", "P4 exercices de niveau 1"]
REVISIONS = (1, 3, 7, 21)
BOUCLE = 21
ENTRAINEMENT = [(2, "niveau 2", "exercices types d'examen, chronométrés ; correction avec le corrigé ; chaque erreur analysée", 1),
                (4, "niveau 3", "questions pièges et cas transversaux ; correction ; chaque erreur analysée", 1),
                (8, "niveau 4", "sujet au format de l'examen — P1 partie 1 → P2 partie 2 : introduction rédigée et plan détaillé → P3 correction au barème, avec la copie de major", 3)]


def D(s):
    return date.fromisoformat(s)


def fr(d, jour=True):
    s = "%s %s" % ("1er" if d.day == 1 else d.day, MOIS[d.month])
    return ("%s %s" % (JOURS[d.weekday()], s)) if jour else s


def sections_du_cours(chemin):
    """Les sections d'apprentissage « ## 2.k — Titre » d'un cours reconstruit."""
    res = []
    for l in open(chemin, encoding="utf-8"):
        m = re.match(r"^## 2\.(\d+)\s+—\s+(.*)$", l.rstrip())
        if m:
            res.append((int(m.group(1)), m.group(2).strip()))
    return res


class Planificateur:
    def __init__(self, cfg):
        self.cfg = cfg
        self.mat = cfg["matieres"]
        self.debut, self.finp = D(cfg["debut"]), D(cfg["fin_preparation"])
        self.jours = [self.debut + timedelta(k) for k in range((self.finp - self.debut).days + 1)]
        self.alertes, self.chap = [], []
        av = cfg.get("avancement", {})
        for k, c in enumerate(cfg["chapitres"]):
            chemin = os.path.join(SEM, c["fichier"])
            if not os.path.isfile(chemin):
                self.alertes.append("%s : cours reconstruit introuvable (%s) — chapitre non planifié." % (c["id"], c["fichier"]))
                continue
            secs = sections_du_cours(chemin)
            if not secs:
                self.alertes.append("%s : aucune section « ## 2.k » dans le cours — chapitre non planifié." % c["id"])
                continue
            ch = dict(c, rang=k, sections=secs, total=4 * len(secs), dispo=D(c["dispo"]),
                      fait=av.get(c["id"], {}).get("etapes_faites", 0), fin=None, debut_app=None,
                      revs=[], ents=[])
            if av.get(c["id"], {}).get("appris_le"):
                ch["fin"] = D(av[c["id"]]["appris_le"])
                ch["fait"] = ch["total"]
            self.chap.append(ch)
        self.plan = defaultdict(list)
        self.revs = defaultdict(list)
        self.ents = []
        self.appris = defaultdict(int)
        for ch in self.chap:
            if ch["fin"]:
                self.programmer(ch)

    # ---------------------------------------------------------------- outils
    def capacite(self, d):
        for p in self.cfg["capacite"]:
            if D(p["du"]) <= d <= D(p["au"]):
                return p["p"]
        return 0

    def court(self, m):
        return self.mat[m]["court"] if m in self.mat else m

    def numero(self, ch):
        return "Ch" + ch["id"].split("_Ch")[1]

    def ajouter(self, d, m, ch, t, det, p):
        self.plan[d].append({"m": m, "ch": ch, "t": t, "det": det, "p": p})

    def programmer(self, ch):
        """Révisions espacées et entraînement, à partir de la fin de l'apprentissage."""
        f = ch["fin"]
        ecarts = list(REVISIONS)
        while f + timedelta(ecarts[-1] + BOUCLE) <= self.finp:
            ecarts.append(ecarts[-1] + BOUCLE)
        for j in ecarts:
            dd = f + timedelta(j)
            if dd <= self.finp:
                ch["revs"].append((j, dd))
                self.revs[dd].append((ch, j))
        for j, niv, quoi, p in ENTRAINEMENT:
            item = {"ch": ch, "niv": niv, "quoi": quoi, "p": p, "des": f + timedelta(j)}
            ch["ents"].append(item)
            self.ents.append(item)

    def pistes(self, d):
        """Un chapitre apprenable par matière, la matière la moins servie d'abord."""
        vus, res = set(), []
        for ch in sorted(self.chap, key=lambda c: (c.get("ordre", 1000), c["dispo"], c["rang"])):
            m = ch["matiere"]
            if m in vus or ch["fait"] >= ch["total"] or ch["dispo"] > d:
                continue
            vus.add(m)
            res.append(ch)
        return sorted(res, key=lambda c: (self.appris[c["matiere"]] / max(1, self.mat[c["matiere"]]["ects"]), c["rang"]))

    def etape(self, ch, d):
        k = ch["fait"]
        ch["debut_app"] = ch["debut_app"] or d
        ch["fait"] += 1
        self.appris[ch["matiere"]] += 1
        num, titre = ch["sections"][k // 4]
        if ch["fait"] >= ch["total"]:
            ch["fin"] = d
            self.programmer(ch)
        return num, titre, ETAPES[k % 4]

    # ---------------------------------------------------------------- une journée
    def jour(self, d):
        C = self.capacite(d)
        libre = C
        if d.weekday() == self.cfg["marge"]["jour"]:
            mg = int(C * self.cfg["marge"]["part"])
            self.ajouter(d, "—", "—", "MARGE", "rattrapage des pomodoros manqués de la semaine ; si rien à rattraper : cartes Anki en avance", mg)
            libre -= mg
        # engagements fixes
        for eb in self.cfg.get("examens_blancs", []):
            dd, m = D(eb["date"]), eb["matiere"]
            if dd == d:
                self.ajouter(d, m, "programme appris", "EXAMEN BLANC", "conditions réelles : durée exacte, sans document", eb["p"])
                libre -= eb["p"]
            if dd + timedelta(1) == d:
                self.ajouter(d, m, "examen blanc de la veille", "EXAMEN BLANC", "correction au barème, analyse de chaque erreur ; copie envoyée", 1)
                libre -= 1
        for cc in self.cfg.get("controles_continus", []):
            dd, m = D(cc["date"]), cc["matiere"]
            for k in (1, 2):
                if dd - timedelta(k) == d:
                    self.ajouter(d, m, "programme du contrôle", "PRÉPARATION DE CC", "contrôle du %s (%s)" % (fr(dd), cc.get("nature", "")), 2)
                    libre -= 2
            if dd == d:
                self.ajouter(d, m, "—", "CONTRÔLE CONTINU", "%s — en séance, hors pomodoros" % cc.get("nature", ""), 0)
        for td in self.cfg.get("td", []):
            m, jt = td["matiere"], td["jour"]
            actif = lambda x: x.weekday() == jt and D(td["du"]) <= x <= D(td["au"])
            veille = d + timedelta(2 if d.weekday() == 5 else 1)
            if d.weekday() != 6 and actif(veille) and veille <= self.finp:
                self.ajouter(d, m, "fiche du TD de %s" % JOURS[veille.weekday()], "PRÉPARATION DE TD", "exercices de la fiche tentés seul ; notions à revoir notées", 1)
                libre -= 1
            if actif(d):
                self.ajouter(d, m, "TD du jour", "CONSOLIDATION DE TD", "exercices corrigés refaits de mémoire ; attentes du chargé de TD notées", 1)
                libre -= 1
        # révisions espacées dues
        dues = self.revs.pop(d, [])
        while dues and libre > 0:
            paquet, dues = dues[:2], dues[2:]
            mats = list(dict.fromkeys(self.court(ch["matiere"]) for ch, _ in paquet))
            self.ajouter(d, " + ".join(mats), " + ".join("%s J+%d" % (self.numero(ch), j) for ch, j in paquet), "RÉVISER",
                         "cartes Anki dues → fiche de synthèse restituée de mémoire sur feuille blanche → correction des oublis", 1)
            libre -= 1
        if dues:
            self.revs[d + timedelta(1)] = dues + self.revs[d + timedelta(1)]
            self.alertes.append("%s : %d révision(s) reportée(s) au lendemain faute de place." % (fr(d), len(dues)))
        # entraînement dû : un exercice par jour, s'il tient dans la place restante
        prets = [x for x in self.ents if x["des"] <= d and x["p"] <= libre]
        if prets:
            x = prets[0]
            self.ents.remove(x)
            self.ajouter(d, x["ch"]["matiere"], self.numero(x["ch"]), "S'ENTRAÎNER",
                         "§ 5, %s — %s" % (x["niv"], x["quoi"]), x["p"])
            libre -= x["p"]
        # apprentissage
        pistes = self.pistes(d)
        tour = 0
        while libre > 0 and pistes:
            parts = [2, 2] if (len(pistes) >= 2 and libre >= 4) else [libre]
            for ch, n in zip(pistes, parts):
                for _ in range(min(n, libre)):
                    if ch["fait"] >= ch["total"]:
                        break
                    num, titre, etp = self.etape(ch, d)
                    self.ajouter(d, ch["matiere"], self.numero(ch), "APPRENDRE", (num, titre, etp), 1)
                    libre -= 1
            pistes = self.pistes(d)
            tour += 1
            if tour > 20:
                break
        if libre > 0:
            self.ajouter(d, "—", "—", "EN ATTENTE", "réservé à tes prochains cours (tant qu'il est vide : cartes Anki dues, puis questions de marche)", libre)
        total = sum(b["p"] for b in self.plan[d])
        if total != C:
            self.alertes.append("%s : %d pomodoros planifiés pour une capacité de %d." % (fr(d), total, C))

    def lancer(self):
        for d in self.jours:
            self.jour(d)
        return self


# ==================================================================== rendu
def semaines(P, n):
    lundi = P.debut - timedelta(P.debut.weekday())
    res = []
    while len(res) < n and lundi <= P.finp:
        res.append([lundi + timedelta(k) for k in range(7) if P.debut <= lundi + timedelta(k) <= P.finp])
        lundi += timedelta(7)
    return res


def blocs_affiches(P, d):
    """Regroupe les pomodoros d'apprentissage consécutifs d'un même chapitre."""
    res = []
    for b in P.plan[d]:
        prec = res[-1] if res else None
        if b["t"] == "APPRENDRE" and prec and prec["t"] == "APPRENDRE" and prec["ch"] == b["ch"] and prec["m"] == b["m"]:
            prec["items"].append(b["det"])
            prec["p"] += b["p"]
        else:
            x = dict(b)
            x["items"] = [b["det"]]
            res.append(x)
    for x in res:
        if x["t"] == "APPRENDRE":
            groupes = []
            for num, titre, etp in x["items"]:
                if groupes and groupes[-1][0] == num:
                    groupes[-1][2].append(etp)
                else:
                    groupes.append((num, titre, [etp]))
            x["det"] = " · ".join("**§ 2.%d** %s — %s" % (num, titre, " → ".join(e)) for num, titre, e in groupes)
    return res


def rendu(P):
    cfg = P.cfg
    maj = D(cfg["mise_a_jour"])
    o = []
    A = o.append
    A("---")
    A("titre: Planning du semestre — planning glissant")
    A("sous_titre: Livrable 2 — l'emploi du temps jour par jour, en pomodoros, recalculé à chaque cours reçu")
    A("resume: Généré par Semestre1/outils/planning.py à partir de Semestre1/planning.json, le %s %d. Ne pas modifier à la main : corriger les données, puis régénérer." % (fr(maj, False), maj.year))
    A("date: %s %d" % (fr(maj, False), maj.year))
    A("sommaire: non")
    A("---")
    A("")
    A("# Comment lire ce planning")
    A("")
    A("- **Il est glissant.** Les profs publient les cours au fil du semestre : chaque fois que tu m'en envoies un, je le reconstruis, je l'ajoute ici et je te renvoie le planning recalculé. Il est aussi recalculé à chaque bilan du dimanche.")
    A("- **Chaque jour, suis les lignes dans l'ordre**, sans rien décider : elles disent la matière, le chapitre, le type de travail, la section du cours et le nombre de pomodoros.")
    A("- **Un pomodoro** = 25 minutes de travail + 5 minutes de pause ; une pause longue de 20 minutes toutes les 4 sessions.")
    A("- **« En attente »** = un créneau réservé aux cours que tu vas m'envoyer. Tant qu'il est vide : cartes Anki dues, puis les questions de marche du dernier chapitre, à voix haute.")
    A("- **En marchant**, hors pomodoros : les questions de la section 7 du dernier cours appris.")
    A("")
    # volume
    A("# Ton volume horaire — fixe, vérifié")
    A("")
    A("| Période | Par jour | Jours | Pomodoros | Heures |")
    A("|---|:---:|:---:|:---:|:---:|")
    tj, tp = 0, 0
    for p in cfg["capacite"]:
        a, b = D(p["du"]), D(p["au"])
        n = (b - a).days + 1
        tj += n
        tp += n * p["p"]
        A("| Du %s au %s | %d h = %d pomodoros | %d | %d | %d |" % (fr(a, False), fr(b, False), p["p"] // 2, p["p"], n, n * p["p"], n * p["p"] // 2))
    A("| **Total avant le 7 décembre** | | **%d** | **%d** | **%d** |" % (tj, tp, tp // 2))
    A("| Du 7 au 18 décembre | révisions ciblées entre les épreuves, selon le calendrier d'examens | | | |")
    A("")
    typ = defaultdict(int)
    for d in P.jours:
        for b in P.plan[d]:
            typ[b["t"]] += b["p"]
    total = sum(typ.values())
    A("**Où en est la répartition des %d pomodoros** : %s." % (total, " · ".join(
        "%s %d" % (k.lower(), v) for k, v in sorted(typ.items(), key=lambda x: -x[1]) if v)))
    A("")
    # protocoles
    A("# Ce que tu fais dans chaque pomodoro")
    A("")
    A("| Type | Déroulé exact |")
    A("|---|---|")
    A("| **APPRENDRE** | Un cycle de 4 pomodoros par section `§ 2.k` du cours : **P1** lecture active, crayon en main · **P2** restitution de mémoire, cours fermé, à l'écrit ou à voix haute · **P3** cartes de la section · **P4** exercices de niveau 1 |")
    A("| **RÉVISER** | Cartes Anki dues · puis la fiche de synthèse du chapitre, restituée de mémoire sur une feuille blanche · puis comparaison et correction des oublis |")
    A("| **S'ENTRAÎNER** | Les exercices du niveau indiqué (§ 5 du cours), chronométrés · correction avec le corrigé · chaque erreur classée : connaissance, méthode ou inattention |")
    A("| **EXAMEN BLANC** | Conditions réelles : durée exacte, sans document, téléphone éteint · correction le lendemain, puis tu m'envoies ta copie |")
    A("| **MARGE** | Le dimanche : rattrapage des pomodoros manqués de la semaine ; si rien à rattraper, cartes Anki en avance |")
    A("| **EN ATTENTE** | Réservé à tes prochains cours ; tant qu'il est vide : cartes Anki dues, puis questions de marche du dernier chapitre, à voix haute |")
    A("")
    A("**Relecture passive interdite** : rappel actif, restitution, révisions à J+1, J+3, J+7 et J+21 puis en boucle, entrelacement des matières dès que tu en as plusieurs.")
    A("")
    A("::: methode Si tu rates des pomodoros")
    A("1. **D'abord les révisions espacées dues** : elles perdent leur valeur si elles attendent.")
    A("2. **Ensuite les chapitres à fort coefficient.**")
    A("3. **La marge du dimanche** absorbe le reste. On ne décale jamais tout en bloc : dis-le au bilan du dimanche, je recalcule.")
    A(":::")
    A("")
    # chapitres
    A("# Les chapitres reçus — apprentissage, révisions, entraînement")
    A("")
    A("| Chapitre | Sections | Apprentissage | J+1 | J+3 | J+7 | J+21 | Puis | Entraînement au plus tôt (niveaux 2 · 3 · 4) |")
    A("|---|:---:|---|---|---|---|---|---|---|")
    for ch in P.chap:
        rv = dict(ch["revs"])
        cols = [fr(rv[j], False) if j in rv else "—" for j in REVISIONS]
        suite = ", ".join(fr(dd, False) for j, dd in ch["revs"] if j not in REVISIONS) or "—"
        app = ("du %s au %s" % (fr(ch["debut_app"], False), fr(ch["fin"], False))) if ch["fin"] and ch["debut_app"] else (
            "appris le %s" % fr(ch["fin"], False) if ch["fin"] else "en cours")
        ents = " · ".join(fr(x["des"], False) for x in ch["ents"]) or "—"
        A("| %s %s — %s | %d | %s | %s | %s | %s |" % (P.court(ch["matiere"]), P.numero(ch), ch["titre"], len(ch["sections"]), app, " | ".join(cols), suite, ents))
    A("")
    A("*L'entraînement se place au premier créneau libre à partir de ces dates ; le niveau 4 demande trois pomodoros d'affilée.*")
    A("")
    # semaines
    n = cfg.get("semaines_detaillees", 2)
    A("# L'emploi du temps, semaine par semaine")
    A("")
    for sem in semaines(P, n):
        tp = sum(b["p"] for d in sem for b in P.plan[d])
        A("## Du %s au %s — %d pomodoros" % (fr(sem[0]), fr(sem[-1]), tp))
        A("")
        A("| Jour | Matière | Chapitre | Travail | Détail | P |")
        A("|---|---|---|---|---|:---:|")
        for d in sem:
            premier = True
            for b in blocs_affiches(P, d):
                A("| %s | %s | %s | %s | %s | %s |" % (
                    "**%s** · %d P" % (fr(d), P.capacite(d)) if premier else "",
                    P.court(b["m"]), b["ch"], b["t"], b["det"], b["p"] if b["p"] else "—"))
                premier = False
        A("")
    reste = [d for d in P.jours if d > semaines(P, n)[-1][-1]]
    if reste:
        A("*La suite — du %s au 6 décembre — se remplit à mesure que tes cours arrivent ; les révisions déjà prévues sont dans le tableau des chapitres.*" % fr(reste[0]))
        A("")
    # ce qui manque
    A("# Ce qu'il me faut pour compléter le planning")
    A("")
    A("| Ce qui manque | Pourquoi |")
    A("|---|---|")
    A("| **Les cours déjà publiés dans les autres matières** | Pour les reconstruire et remplir les créneaux « en attente », en alternant les matières |")
    A("| **Ton emploi du temps de TD** | Chaque TD est précédé d'une préparation et suivi d'une consolidation |")
    A("| **Les dates des contrôles continus** | Chacun est préparé spécifiquement |")
    A("| **Le calendrier des examens** (du 7 au 18 décembre) et leurs modalités | Pour l'ordre des révisions finales et le format des examens blancs |")
    A("")
    A("# Alertes")
    A("")
    for a in P.alertes or ["Aucune."]:
        A("- " + a)
    A("")
    return "\n".join(o) + "\n"


def main():
    cfg = json.load(open(os.path.join(SEM, "planning.json"), encoding="utf-8"))
    P = Planificateur(cfg).lancer()
    cap = sum(P.capacite(d) for d in P.jours)
    fait = sum(b["p"] for d in P.jours for b in P.plan[d])
    print("capacité : %d pomodoros · planifiés : %d · chapitres : %d · alertes : %d" % (cap, fait, len(P.chap), len(P.alertes)))
    for a in P.alertes:
        print("  -", a)
    if cap != fait:
        sys.exit("ÉCHEC : le planning ne consomme pas exactement la capacité.")
    if "--bilan" in sys.argv:
        return
    sortie = os.path.join(SEM, "PLANNING.md")
    with open(sortie, "w", encoding="utf-8") as f:
        f.write(rendu(P))
    print(sortie)


if __name__ == "__main__":
    main()
