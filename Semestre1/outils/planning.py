#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
planning.py — génère Semestre1/PLANNING.md à partir de Semestre1/planning.json.

    python3 Semestre1/outils/planning.py            # écrit PLANNING.md (+ bilan à l'écran)
    python3 Semestre1/outils/planning.py --bilan    # bilan de capacité seulement

Chaque jour, dans cet ordre (charte : Livrable 2 et protocole de rattrapage) :
  1. marge du dimanche : la moitié des pomodoros du jour ;
  2. engagements fixes : examen blanc (puis correction le lendemain), préparation de contrôle
     continu (J-2 et J-1), préparation de TD (la veille ; le samedi pour un TD du lundi),
     consolidation de TD (le jour même), plateformes Ecri+ et GoFluent (samedi) ;
  3. révisions espacées dues — J+1, J+3, J+7, J+21 après la fin d'apprentissage d'un chapitre —
     à raison de deux par pomodoro (cartes Anki dues + restitution de deux fiches + correction) ;
  4. le reste va aux six matières au prorata ECTS × difficulté, par blocs de deux pomodoros :
     APPRENDRE (P1 lecture active · P2 restitution Feynman · P3 cartes · P4 exercices niveau 1)
     tant qu'un chapitre disponible reste à apprendre et que la date limite d'apprentissage
     n'est pas passée ; sinon S'ENTRAÎNER (niveaux 2, 3, 4 du chapitre). Du 16 novembre au
     6 décembre, apprentissage et entraînement alternent dans chaque matière.
Période d'examens : révision de la prochaine épreuve, veille allégée (arrêt 21 h), sommeil protégé.
"""
import copy
import json
import math
import os
import sys
from collections import defaultdict
from datetime import date, timedelta

ICI = os.path.dirname(os.path.abspath(__file__))
SEM = os.path.dirname(ICI)
JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
MOIS = ["", "janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
        "septembre", "octobre", "novembre", "décembre"]
ETAPES = ["P1 lecture active", "P2 restitution Feynman", "P3 cartes de la section", "P4 exercices niveau 1"]
NIVEAUX = {"N2": "niveau 2 — exercices types chronométrés", "N3": "niveau 3 — réflexion, cas, pièges",
           "N4": "niveau 4 — sujet au format de l'examen"}


def D(s):
    return date.fromisoformat(s)


def fr(d, jour=True):
    s = "%s %s" % ("1er" if d.day == 1 else d.day, MOIS[d.month])
    return ("%s %s" % (JOURS[d.weekday()], s)) if jour else s


def sections_reelles(ch):
    f = ch.get("fichier")
    p = os.path.join(SEM, f) if f else None
    if not p or not os.path.isfile(p):
        return None
    n = sum(1 for l in open(p, encoding="utf-8") if l.startswith("## 2.") and l[5:6].isdigit())
    return n or None


class Planificateur:
    def __init__(self, cfg):
        self.cfg, self.mat, self.c = cfg, cfg["matieres"], cfg["couts"]
        self.debut, self.finp, self.fin = D(cfg["debut"]), D(cfg["fin_preparation"]), D(cfg["examens_fin"])
        self.limite = D(cfg.get("apprentissage_jusqu_au", cfg["fin_preparation"]))
        self.jours = [self.debut + timedelta(k) for k in range((self.fin - self.debut).days + 1)]
        self.cours = [m for m, v in self.mat.items() if not v.get("plateforme")]
        self.poids = {m: self.mat[m]["ects"] * self.mat[m].get("difficulte", 1) for m in self.cours}
        self.chap = []
        av = cfg.get("avancement", {})
        for ch in cfg["chapitres"]:
            ch = dict(ch)
            r = sections_reelles(ch)
            ch["estime"] = not r
            if r:
                ch["sections"] = r
            ch["dispo"] = D(ch["dispo"])
            ch["cycle"] = self.c["app_par_section"]
            if not self.mat[ch["matiere"]].get("exercices") and self.c.get("app_par_section_memoire"):
                ch["cycle"] = self.c["app_par_section_memoire"]
            ch["total"] = ch["sections"] * ch["cycle"]
            a = av.get(ch["id"], {})
            ch["fait"] = a.get("etapes_faites", 0)
            ch["fin"] = D(a["appris_le"]) if a.get("appris_le") else None
            ch["debut_app"] = None
            ch["revs"] = []
            self.chap.append(ch)
        cumul = defaultdict(int)
        for ch in self.chap:
            m = ch["matiere"]
            cumul[m] += ch["total"]
            ch["virtuel"] = cumul[m] / self.poids.get(m, 1)
        self.plan = defaultdict(list)
        self.revs = defaultdict(list)
        self.train = defaultdict(list)
        self.utilise = defaultdict(int)
        self.flex = defaultdict(int)
        self.alertes = []
        self.examens = {m: D(v["examen"]["date"]) for m, v in self.mat.items() if v.get("examen")}
        self.limites = {m: min(self.limite, self.examens[m] - timedelta(10)) for m in self.examens}
        self.vac = [(D(v["du"]), D(v["au"])) for v in cfg.get("vacances", [])]
        self.ccs = {(m, D(cc["date"])) for m in self.cours for cc in self.mat[m].get("cc", [])}
        for ch in self.chap:
            if ch["fin"]:
                self.programmer(ch)

    def capacite(self, d):
        for p in self.cfg["capacite"]:
            if D(p["du"]) <= d <= D(p["au"]):
                return p["p"]
        return 0

    def jour_td(self, m, d):
        td = self.mat[m].get("td")
        return bool(td and d.weekday() == td["jour"] and D(td["debut"]) <= d <= D(td["fin"])
                    and not any(a <= d <= b for a, b in self.vac))

    def ajouter(self, d, m, ch, t, det, p, flex=False):
        self.plan[d].append({"m": m, "ch": ch, "t": t, "det": det, "p": p})
        self.utilise[m] += p
        if flex:
            self.flex[m] += p

    def libelle(self, cid):
        for ch in self.chap:
            if ch["id"] == cid:
                return "Ch%s — %s" % (cid.split("_Ch")[1], ch["titre"])
        return cid

    # -------------------------------------------------------- apprentissage / révisions
    def prochain_chapitre(self, m, d):
        if d > self.limites.get(m, self.limite):
            return None
        for ch in self.chap:
            if ch["matiere"] == m and ch["fait"] < ch["total"] and ch["dispo"] <= d:
                return ch
        return None

    def file_apprentissage(self, d):
        """Chapitres apprenables aujourd'hui, dans l'ordre de la file pondérée (un par matière)."""
        vus, res = set(), []
        for ch in sorted(self.chap, key=lambda c: (c["fait"] == 0, c.get("ordre", 1000 + c["virtuel"]))):
            m = ch["matiere"]
            if m in vus or ch["fait"] >= ch["total"] or ch["dispo"] > d:
                continue
            if d > self.limites.get(m, self.limite) or d >= self.examens.get(m, self.fin):
                continue
            if self.prochain_chapitre(m, d) is not ch:
                continue
            vus.add(m)
            res.append(ch)
        return res

    def etape(self, ch, d):
        k = ch["fait"]
        ch["debut_app"] = ch["debut_app"] or d
        ch["fait"] += 1
        if ch["fait"] >= ch["total"]:
            ch["fin"] = d
            self.programmer(ch)
        if ch["cycle"] == 3:
            noms = ["P1 lecture active", "P2 restitution Feynman + cartes", "P3 questions de niveau 1"]
        else:
            noms = ETAPES
        return "§ 2.%d — %s" % (k // ch["cycle"] + 1, noms[k % ch["cycle"]])

    def programmer(self, ch):
        for j in (1, 3, 7, 21):
            dd = ch["fin"] + timedelta(j)
            if dd > self.finp:
                ch["revs"].append((j, None))
                continue
            ch["revs"].append((j, dd))
            self.revs[dd].append((ch, j))
        m = ch["matiere"]
        grille = self.c["entrainement_exercices"] if self.mat[m].get("exercices") else self.c["entrainement_memoire"]
        for niv, dec in (("N2", 2), ("N3", 4), ("N4", 8)):
            for _ in range(grille[niv]):
                self.train[m].append({"ch": ch, "niv": niv, "des": ch["fin"] + timedelta(dec)})

    # -------------------------------------------------------- une journée de préparation
    def jour(self, d):
        C = self.capacite(d)
        libre = C
        if d.weekday() == self.cfg["marge"]["jour"]:
            mg = int(C * self.cfg["marge"]["part"])
            self.plan[d].append({"m": "—", "ch": "—", "t": "MARGE",
                                 "det": "demi-journée de rattrapage ; si rien à rattraper : cartes Anki", "p": mg})
            libre -= mg
        for eb in self.cfg["examens_blancs"]:
            dd, m = D(eb["date"]), eb["matiere"]
            appris = [ch for ch in self.chap if ch["matiere"] == m and ch["fin"] and ch["fin"] < dd]
            if eb["type"] == "partiel":
                if not appris:
                    if dd == d:
                        self.alertes.append("%s : examen blanc partiel de %s impossible — aucun chapitre appris à cette date." % (fr(d), self.mat[m]["nom"]))
                    continue
                perim = ", ".join("Ch" + ch["id"].split("_Ch")[1] for ch in appris)
                if dd == d:
                    self.ajouter(d, m, perim, "EXAMEN BLANC", "partiel, conditions réelles, sans document", self.c["eb_partiel"]["p"])
                    libre -= self.c["eb_partiel"]["p"]
                if dd + timedelta(1) == d:
                    self.ajouter(d, m, "examen blanc de la veille", "EXAMEN BLANC", "correction au corrigé, analyse de chaque erreur", self.c["eb_partiel"]["correction"])
                    libre -= self.c["eb_partiel"]["correction"]
            else:
                p = self.mat[m]["examen"]["duree_p"]
                if not appris:  # un examen blanc sans chapitre appris ne mesure rien : on le signale au lieu de le placer
                    if dd == d:
                        self.alertes.append("%s : examen blanc complet de %s sans objet — aucun chapitre appris à cette date ; à déplacer dans planning.json." % (fr(d), self.mat[m]["nom"]))
                    continue
                perim = ", ".join("Ch" + ch["id"].split("_Ch")[1] for ch in appris)
                if dd == d:
                    self.ajouter(d, m, perim, "EXAMEN BLANC", "complet, durée réelle (%d P), sans document" % p, p)
                    libre -= p
                if dd + timedelta(1) == d:
                    self.ajouter(d, m, "examen blanc de la veille", "EXAMEN BLANC", "correction de correcteur, note estimée, lacunes nommées", self.c["eb_complet_correction"])
                    libre -= self.c["eb_complet_correction"]
        for m in self.cours:
            for cc in self.mat[m].get("cc", []):
                dd = D(cc["date"])
                prep = cc.get("preparation", self.c["cc_preparation"])
                for k, p in enumerate(reversed(prep)):
                    if dd - timedelta(k + 1) == d:
                        self.ajouter(d, m, "programme du contrôle", "PRÉPARATION CC", "contrôle continu du %s (%s)" % (fr(dd), cc["nature"]), p)
                        libre -= p
                if dd == d:
                    self.plan[d].append({"m": m, "ch": "—", "t": "CONTRÔLE CONTINU", "det": cc["nature"] + " — en séance, hors pomodoros", "p": 0})
            veille = d + timedelta(2 if d.weekday() == 5 else 1)
            if (d.weekday() != 6 and self.jour_td(m, veille) and veille <= self.finp
                    and (m, veille) not in self.ccs):
                self.ajouter(d, m, "fiche du TD de %s" % JOURS[veille.weekday()], "PRÉPARATION DE TD", "exercices de la fiche tentés seul ; notions à revoir listées", self.c["td_preparation"])
                libre -= self.c["td_preparation"]
            if self.jour_td(m, d) and (m, d) not in self.ccs:
                self.ajouter(d, m, "TD du jour", "TD — CONSOLIDATION", "exercices corrigés refaits de mémoire ; attentes du chargé de TD notées", self.c["td_consolidation"])
                libre -= self.c["td_consolidation"]
        for m, v in self.mat.items():
            if v.get("plateforme") and d.weekday() == v["jour"]:
                self.ajouter(d, m, "plateforme en ligne", "S'ENTRAÎNER", "activités de la semaine", self.c["plateforme_hebdo"])
                libre -= self.c["plateforme_hebdo"]
        dues, vus = [], {}
        for ch, j in self.revs.pop(d, []):
            if ch["id"] in vus:
                k = vus[ch["id"]]
                self.alertes.append("%s : la révision J+%d de %s, reportée, est fusionnée avec sa J+%d du jour — une révision perdue." % (fr(d), min(j, dues[k][1]), ch["id"], max(j, dues[k][1])))
                dues[k] = (ch, max(j, dues[k][1]))
                continue
            vus[ch["id"]] = len(dues)
            dues.append((ch, j))
        if dues:
            place = max(0, libre) * self.c["revisions_par_pomodoro"]
            if len(dues) > place:
                report = dues[place:]
                dues = dues[:place]
                self.revs[d + timedelta(1)] = report + self.revs[d + timedelta(1)]
                self.alertes.append("%s : %d révision(s) reportée(s) au lendemain faute de place." % (fr(d), len(report)))
            k = self.c["revisions_par_pomodoro"]
            for i in range(0, len(dues), k):
                paquet = dues[i:i + k]
                mats = []
                for ch, _ in paquet:
                    if ch["matiere"] not in mats:
                        mats.append(ch["matiere"])
                self.ajouter(d, " + ".join(self.mat[x]["court"] for x in mats),
                             " + ".join("Ch%s J+%d" % (ch["id"].split("_Ch")[1], j) for ch, j in paquet),
                             "RÉVISER", "Anki dues → fiche(s) restituée(s) de mémoire → correction des oublis", 1)
                libre -= 1
        if libre < 0:
            self.alertes.append("%s : engagements fixes supérieurs à la capacité de %d pomodoro(s)." % (fr(d), -libre))
        periode_c = d >= D(self.cfg["capacite"][-1]["du"])
        W = sum(self.poids.values())
        pistes = self.file_apprentissage(d)[:2 if libre >= 4 else 1]
        # part d'entraînement : nulle en octobre, un tiers du 1er au 15 novembre, la moitié ensuite
        part_ent = 0.0 if d < D(self.cfg["capacite"][1]["du"]) else (0.25 if not periode_c else 0.4)
        dispo_ent = sum(1 for m in self.cours for x in self.train[m] if x["des"] <= d and d < self.examens.get(m, self.fin))
        n_ent = min(int(round(libre * part_ent)), dispo_ent) if pistes else 0
        n_app = libre - n_ent
        # apprentissage : pistes servies à tour de rôle par blocs de deux
        k, jour_ch = 0, defaultdict(int)
        plafond = self.c.get("apprendre_max_par_chapitre_et_jour", 4)
        while n_app > 0 and pistes:
            ch = pistes[k % len(pistes)]
            for _ in range(min(2, n_app)):
                if ch["fait"] >= ch["total"] or jour_ch[ch["id"]] >= plafond:
                    break
                self.ajouter(d, ch["matiere"], ch["id"], "APPRENDRE", self.etape(ch, d), 1, True)
                jour_ch[ch["id"]] += 1
                n_app -= 1
                libre -= 1
            pistes = [c for c in pistes if c["fait"] < c["total"] and jour_ch[c["id"]] < plafond]
            if not pistes:
                deja = set(jour_ch)
                pistes = [c for c in self.file_apprentissage(d) if c["id"] not in deja][:1]
            k += 1
        n_app = 0
        # entraînement (et reliquat) au prorata des poids, parmi les matières qui ont de quoi s'entraîner
        tot = sum(self.flex.values())
        while libre > 0:
            cands = []
            for m in self.cours:
                tr = [x for x in self.train[m] if x["des"] <= d and d < self.examens.get(m, self.fin)]
                if tr:
                    cands.append((self.poids[m] / W * (tot + 2) - self.flex[m], self.poids[m], m, tr))
            if not cands:
                appris = [ch for ch in self.chap if ch["fin"]]
                if appris:
                    self.plan[d].append({"m": "—", "ch": "chapitres déjà appris", "t": "S'ENTRAÎNER",
                                         "det": "entraînement transversal : exercices mélangés des chapitres appris", "p": libre})
                else:
                    self.plan[d].append({"m": "—", "ch": "—", "t": "MARGE", "det": "rien d'apprenable : cartes Anki, ou avance sur le chapitre suivant dès réception", "p": libre})
                break
            cands.sort(key=lambda x: (-x[0], -x[1]))
            _, _, m, tr = cands[0]
            for _ in range(min(2, libre)):
                tr = [x for x in self.train[m] if x["des"] <= d]
                if not tr:
                    break
                x = tr[0]
                self.train[m].remove(x)
                self.ajouter(d, m, x["ch"]["id"], "S'ENTRAÎNER", NIVEAUX[x["niv"]] + " ; correction ; analyse des erreurs", 1, True)
                libre -= 1
                tot += 1

    def periode_examens(self):
        ordre = sorted((v, m) for m, v in self.examens.items())
        for d in self.jours:
            if d <= self.finp:
                continue
            auj = [m for dd, m in ordre if dd == d]
            suiv = [(dd, m) for dd, m in ordre if dd > d]
            if auj:
                m = auj[0]
                self.plan[d].append({"m": m, "ch": "—", "t": "ÉPREUVE", "det": self.mat[m]["examen"]["nature"], "p": 0})
                if suiv:
                    dd, m2 = suiv[0]
                    self.plan[d].append({"m": m2, "ch": "fiches + formulaire", "t": "RÉVISER", "det": "le soir, après l'épreuve : lancement de la suivante (%s)" % fr(dd), "p": 3})
            elif suiv:
                dd, m2 = suiv[0]
                if (dd - d).days == 1:
                    self.plan[d].append({"m": m2, "ch": "fiches, points de vigilance, formulaire", "t": "VEILLE D'EXAMEN", "det": "révision express des points qui tombent le plus ; arrêt à 21 h, 7 à 8 h de sommeil", "p": 6})
                else:
                    self.plan[d].append({"m": m2, "ch": "tout le programme", "t": "RÉVISER", "det": "cartes Anki, fiches restituées de mémoire, un sujet corrigé refait", "p": 6})
                    if len(suiv) > 1:
                        dd3, m3 = suiv[1]
                        self.plan[d].append({"m": m3, "ch": "fiches", "t": "RÉVISER", "det": "entretien de l'épreuve d'après (%s)" % fr(dd3), "p": 2})

    def lancer(self):
        for d in self.jours:
            if d <= self.finp:
                self.jour(d)
        self.periode_examens()
        # charte : « au moins deux examens blancs complets par matière avant le 7 décembre »
        for m in self.examens:
            n = sum(1 for eb in self.cfg["examens_blancs"] if eb["matiere"] == m and eb["type"] == "complet"
                    and D(eb["date"]) <= self.finp
                    and any(ch["matiere"] == m and ch["fin"] and ch["fin"] < D(eb["date"]) for ch in self.chap))
            if n < 2:
                self.alertes.append("%s : %d examen(s) blanc(s) complet(s) avant le 7 décembre — la charte en exige au moins deux." % (self.mat[m]["nom"], n))
        return self


def bilan(P):
    cap = sum(P.capacite(d) for d in P.jours if d <= P.finp)
    appris = [ch for ch in P.chap if ch["fin"]]
    non = [ch for ch in P.chap if not ch["fin"]]
    manque = sum(ch["total"] - ch["fait"] for ch in non)
    return {"cap": cap, "appris": len(appris), "total": len(P.chap), "manque": manque,
            "sections": sum(ch["sections"] for ch in P.chap)}


def scenario(cfg, oct_p=None, nov1_p=None, memoire3=False):
    c2 = copy.deepcopy(cfg)
    if memoire3:
        c2["couts"]["app_par_section_memoire"] = 3
    if oct_p:
        c2["capacite"][0]["p"] = oct_p
    if nov1_p:
        c2["capacite"][1]["p"] = nov1_p
    return bilan(Planificateur(c2).lancer())


# =========================================================================== rendu
def rendu(P, cfg, scen):
    o = []
    A = o.append
    maj = D(cfg["mise_a_jour"])
    A("---")
    A("titre: Planning du semestre — du 1er octobre au 18 décembre 2026")
    A("sous_titre: Livrable 2 — l'emploi du temps jour par jour, en pomodoros")
    A("resume: Généré par Semestre1/outils/planning.py à partir de Semestre1/planning.json, mis à jour le %s. Ne pas modifier à la main : corriger les données, puis régénérer. Il se relit au début de chaque session." % fr(maj, False))
    A("date: %s %d" % (fr(maj, False), maj.year))
    A("sommaire: oui")
    A("---")
    A("")
    b = bilan(P)
    A("# Lire d'abord")
    A("")
    A("## L'alerte de départ — le volume dépasse la capacité" + (" : ce qui est sacrifié" if cfg.get("decision_horaire") else ""))
    A("")
    A("::: piege %d chapitres sur %d tiennent dans ton plan horaire au protocole complet" % (b["appris"], b["total"]))
    A("**Capacité avant le 7 décembre : %d pomodoros.** Les %d pomodoros annoncés comptent le 7 décembre, qui est déjà un jour d'examen." % (b["cap"], b["cap"] + 12))
    A("")
    A("**Volume estimé du programme : %d chapitres, %d sections d'apprentissage**, soit %d pomodoros d'APPRENDRE au protocole P1 → P4 — avant révisions, TD, contrôles et examens blancs." % (b["total"], b["sections"], b["sections"] * 4))
    A("")
    A("**Résultat de la simulation :** avec 4 pomodoros par jour en octobre, **%d chapitres sont appris à temps, %d ne le sont pas** (%d pomodoros d'apprentissage manquants). « À temps » : au plus tard dix jours avant l'épreuve de la matière, et le %s au plus tard — pour que les révisions J+1, J+3 et J+7 aient lieu avant elle." % (b["appris"], b["total"] - b["appris"], b["manque"], fr(P.limite, False)))
    A("")
    dec = cfg.get("decision_horaire")
    if dec:
        A("**Ta décision du %s : ton plan horaire est maintenu tel quel** — %s. Ce planning le respecte exactement, et le protocole de la charte n'est pas allégé : chaque section se travaille en quatre pomodoros, P1 → P4." % (fr(D(dec["date"]), False), dec["plan"]))
        A("")
        A("**Ce qui est sacrifié, matière par matière** — le choix suit la pondération ECTS × difficulté, et la date de parution estimée de chaque chapitre :")
        A("")
        A("| Matière | ECTS | Chapitres appris à temps | Chapitres hors capacité | Pomodoros d'apprentissage manquants |")
        A("|---|:---:|:---:|---|:---:|")
        for m in P.cours:
            chs = [ch for ch in P.chap if ch["matiere"] == m]
            if not chs:
                continue
            hors = [ch for ch in chs if not ch["fin"]]
            A("| %s | %s | %d / %d | %s | %d |" % (P.mat[m]["nom"], P.mat[m]["ects"], len(chs) - len(hors), len(chs),
              ", ".join("Ch" + ch["id"].split("_Ch")[1] for ch in hors) or "—", sum(ch["total"] - ch["fait"] for ch in hors)))
        A("")
        A("**Ce qui peut encore réduire le sacrifice sans ajouter une heure :** recevoir vite les supports — 30 chapitres sur 36 sont des estimations, et un chapitre réel peut être plus court que prévu (il peut aussi être plus long) ; ne perdre aucun pomodoro, la marge du dimanche absorbant les imprévus ; les questions de marche de chaque cours, révision gratuite hors pomodoros. **Le planning est recalculé à chaque bilan du dimanche**, et je te dis à chaque fois ce qui est sacrifié.")
        A("")
    else:
        A("| Scénario | Octobre | 1er-15 nov. | Chapitres appris | Apprentissage manquant |")
        A("|---|:---:|:---:|:---:|:---:|")
        for nom, s, o_, n_ in scen:
            A("| %s | %s | %s | **%d / %d** | %d P |" % (nom, o_, n_, s["appris"], s["total"], s["manque"]))
        A("")
        A("**Ce que ça veut dire :** le goulot est **octobre**. C'est le mois où tu ne vas plus en amphi — tu libères environ 12 à 15 h par semaine — et c'est celui où ton plan est le plus bas. **Recommandation : passer octobre à 4 h par jour.** Tant que tu ne l'as pas décidé, ce planning respecte exactement ton plan (2 h/jour) et place les chapitres qui ne tiennent pas en « hors capacité », en bas du document.")
        A("")
    A("**Deux inconnues peuvent faire bouger ce chiffre dans les deux sens :** le nombre réel de chapitres de Mathématiques, Droit, Institutions politiques et des parties 1-2 d'Économie (estimé, rien n'a été reçu), et le nombre réel de TD par semaine (5 supposés).")
    A(":::")
    A("")
    A("## Les hypothèses en vigueur — à remplacer dès que tu as l'information")
    A("")
    A("| Donnée | Hypothèse retenue | Ce qu'il me faut |")
    A("|---|---|---|")
    tds = []
    for m in P.cours:
        td = P.mat[m].get("td")
        if td:
            tds.append("%s le %s" % (P.mat[m]["court"], JOURS[td["jour"]]))
    A("| **Horaires de TD** | un TD par semaine et par matière : %s ; pas de TD pendant les vacances de la Toussaint (26-30 octobre) ; Institutions politiques sans TD | ton emploi du temps de TD |" % ", ".join(tds))
    ccl = []
    for m in P.cours:
        for cc in P.mat[m].get("cc", []):
            ccl.append("%s : %s" % (P.mat[m]["court"], fr(D(cc["date"]))))
    A("| **Contrôles continus** | %s — les seuls dont l'existence est connue ; dates supposées | les dates réelles, et ceux des autres matières |" % " · ".join(ccl))
    ex = " · ".join("%s %s" % (P.mat[m]["court"], fr(dd)) for dd, m in sorted((v, k) for k, v in P.examens.items()))
    A("| **Calendrier des épreuves** | %s | le calendrier officiel |" % ex)
    A("| **Chapitres à venir** | nombre et date de disponibilité estimés par matière (tableau « Les chapitres ») | chaque support dès sa parution, et les notes de ta marraine |")
    A("| **Examens** | durées supposées : Éco 1 h 30 (connue), Gestion 1 h, Stats 1 h 30, Maths et Institutions 2 h, Droit 1 h 30 | les modalités de contrôle des connaissances |")
    A("| **Ecri+ et GoFluent** | un pomodoro par semaine chacun, le samedi | leurs modalités d'évaluation |")
    A("")
    A("## Les protocoles — ce que tu fais dans chaque pomodoro")
    A("")
    A("| Type | Déroulé exact |")
    A("|---|---|")
    A("| **APPRENDRE** | Un cycle de 4 pomodoros par section `§ 2.k` du cours : **P1** lecture active (crayon en main, questions en marge) · **P2** restitution de mémoire, Feynman, à l'écrit ou à voix haute, cours fermé · **P3** cartes de la section · **P4** exercices de niveau 1 |")
    A("| **RÉVISER** | Cartes Anki dues (toutes matières) · puis la fiche du chapitre restituée de mémoire sur feuille blanche · puis comparaison et correction des oublis. Deux chapitres par pomodoro |")
    A("| **S'ENTRAÎNER** | Exercices chronométrés du niveau indiqué · correction avec le corrigé détaillé · chaque erreur classée : connaissance, méthode ou inattention |")
    A("| **EXAMEN BLANC** | Conditions réelles : durée exacte, sans document, téléphone éteint · correction le lendemain, au barème, puis tu m'envoies la copie |")
    A("| **PRÉPARATION DE TD** | Les exercices de la fiche tentés seul avant la séance · la liste des notions à revoir |")
    A("| **TD — CONSOLIDATION** | Le soir du TD : les exercices corrigés refaits de mémoire · les attentes du chargé de TD notées dans `<Matière>/TD/` |")
    A("| **MARGE** | Rattrapage des pomodoros manqués dans la semaine ; si rien à rattraper, cartes Anki en avance |")
    A("")
    A("**Relecture passive interdite.** Rappel actif, restitution Feynman, espacement J+1 · J+3 · J+7 · J+21, entrelacement des matières dans la journée, sujets d'examen dès le mois de novembre. **Les 15 000 pas** : questions de la section 7 de chaque cours, en plus des pomodoros.")
    A("")
    A("::: methode Si tu rates des pomodoros — le protocole de rattrapage")
    A("1. **D'abord les révisions espacées dues** : elles perdent leur valeur si elles attendent.")
    A("2. **Ensuite l'apprentissage des matières à fort coefficient** : Économie, Gestion (6 ECTS), puis Statistiques et Mathématiques (5).")
    A("3. **La marge du dimanche** absorbe le reste. On ne décale jamais tout le planning en bloc.")
    A("4. Au-delà d'une marge, dis-le au bilan du dimanche : je régénère le planning et **je te dis ce qui est sacrifié**.")
    A(":::")
    A("")
    # --- répartition
    A("## La répartition entre matières")
    A("")
    A("| Matière | ECTS | Poids ECTS × difficulté | Part visée de l'apprentissage et de l'entraînement | Obtenue | Pomodoros au total, TD et révisions compris |")
    A("|---|:---:|:---:|:---:|:---:|:---:|")
    tot_all = sum(b2["p"] for d in P.jours if d <= P.finp for b2 in P.plan[d])
    W = sum(P.poids.values())
    par_m = defaultdict(float)
    court = {v["court"]: k for k, v in P.mat.items()}
    for d in P.jours:
        if d <= P.finp:
            for b2 in P.plan[d]:
                parts = b2["m"].split(" + ")
                for part in parts:
                    k = court.get(part, part if part in P.mat else None)
                    par_m[k or "—"] += b2["p"] / len(parts)
    tf = sum(P.flex.values()) or 1
    for m in P.cours:
        A("| %s | %s | %.2f | %.0f %% | %.0f %% | %d |" % (P.mat[m]["nom"], P.mat[m]["ects"], P.poids[m], 100 * P.poids[m] / W, 100 * P.flex[m] / tf, round(par_m[m])))
    for m, v in P.mat.items():
        if v.get("plateforme"):
            A("| %s | %s | — | — | — | %d |" % (v["nom"], v["ects"], round(par_m[m])))
    marge = sum(b2["p"] for d in P.jours if d <= P.finp for b2 in P.plan[d] if b2["t"] == "MARGE")
    transv = round(par_m["—"]) - marge
    if transv:
        A("| *Entraînement transversal, toutes matières* | — | — | — | — | %d |" % transv)
    A("| *Marge* | — | — | — | — | %d |" % marge)
    A("| **Total avant le 7 décembre** | **30** | | **100 %%** | **100 %%** | **%d** |" % tot_all)
    A("")
    A("*Les TD, révisions et examens blancs pèsent le même poids pour chaque matière qui en a : la pondération ECTS × difficulté s'applique à l'apprentissage et à l'entraînement, qui sont les seuls créneaux libres.*")
    A("")
    typ = defaultdict(int)
    for d in P.jours:
        if d <= P.finp:
            for b2 in P.plan[d]:
                typ[b2["t"]] += b2["p"]
    A("| Type de travail | Pomodoros | Part |")
    A("|---|:---:|:---:|")
    for k, v in sorted(typ.items(), key=lambda x: -x[1]):
        if v:
            A("| %s | %d | %.0f %% |" % (k, v, 100 * v / tot_all))
    A("")
    # --- chapitres
    A("## Les chapitres — apprentissage et révisions espacées")
    A("")
    A("| Chapitre | Statut | Sections | Disponible | Appris du → au | J+1 | J+3 | J+7 | J+21 |")
    A("|---|---|:---:|---|---|---|---|---|---|")
    for ch in P.chap:
        st = "reçu" if ch["statut"] == "recu" else "à recevoir"
        sec = "%d%s" % (ch["sections"], " *(est.)*" if ch["estime"] else "")
        if ch["fin"]:
            app = "%s → **%s**" % (fr(ch["debut_app"], False) if ch["debut_app"] else "avant", fr(ch["fin"], False))
            rv = {j: (fr(dd, False) if dd else "*veille d'examen*") for j, dd in ch["revs"]}
            cols = [rv.get(j, "—") for j in (1, 3, 7, 21)]
        else:
            app = "**hors capacité** (%d/%d étapes)" % (ch["fait"], ch["total"])
            cols = ["—"] * 4
        A("| %s %s | %s | %s | %s | %s | %s |" % (P.mat[ch["matiere"]]["court"], P.libelle(ch["id"]), st, sec, fr(ch["dispo"], False), app, " | ".join(cols)))
    A("")
    A("<!--saut-->")
    A("")
    # --- semaines
    A("# L'emploi du temps, semaine par semaine")
    A("")
    lundi = P.debut - timedelta(P.debut.weekday())
    while lundi <= P.fin:
        dim = lundi + timedelta(6)
        jours = [lundi + timedelta(k) for k in range(7) if P.debut <= lundi + timedelta(k) <= P.fin]
        tp = sum(b2["p"] for d in jours for b2 in P.plan[d])
        A("## Semaine du %s au %s — %d pomodoros" % (fr(lundi, False), fr(dim, False), tp))
        A("")
        A("| Jour | Matière | Chapitre | Travail | Détail | P |")
        A("|---|---|---|---|---|:---:|")
        for d in jours:
            blocs = []
            for b2 in P.plan[d]:
                prec = blocs[-1] if blocs else None
                if (prec and prec["m"] == b2["m"] and prec["ch"] == b2["ch"] and prec["t"] == b2["t"]
                        and b2["t"] in ("APPRENDRE", "S'ENTRAÎNER")):
                    prec["items"].append(b2["det"])
                    prec["p"] += b2["p"]
                else:
                    x = dict(b2)
                    x["items"] = [b2["det"]]
                    blocs.append(x)
            for x in blocs:
                if x["t"] == "APPRENDRE":
                    groupes = []
                    for it in x["items"]:
                        sec, etp = it.split(" — ", 1)
                        if groupes and groupes[-1][0] == sec:
                            groupes[-1][1].append(etp)
                        else:
                            groupes.append((sec, [etp]))
                    x["det"] = " · ".join("%s — %s" % (sec, " → ".join(e)) for sec, e in groupes)
                elif x["t"] == "S'ENTRAÎNER" and len(x["items"]) > 1:
                    x["det"] = " · ".join(dict.fromkeys(i.split(" ; ")[0] for i in x["items"])) + " ; correction ; analyse des erreurs"
            tj = sum(b2["p"] for b2 in P.plan[d])
            premier = True
            for b2 in blocs:
                ch = b2["ch"]
                if "_Ch" in ch:
                    ch = "Ch" + ch.split("_Ch")[1]
                m = b2["m"]
                m = P.mat[m]["court"] if m in P.mat else m
                A("| %s | %s | %s | %s | %s | %s |" % ("**%s** · %d P" % (fr(d), tj) if premier else "", m, ch, b2["t"], b2["det"], b2["p"] if b2["p"] else "—"))
                premier = False
            if not blocs:
                A("| **%s** | — | — | — | — | — |" % fr(d))
        A("")
        lundi += timedelta(7)
    # --- hors capacité et alertes
    A("<!--saut-->")
    A("")
    A("# Ce qui ne tient pas, et les alertes")
    A("")
    non = [ch for ch in P.chap if not ch["fin"]]
    A("## Les chapitres hors capacité au rythme actuel")
    A("")
    if non:
        A("| Chapitre | Disponible le | Pomodoros d'apprentissage faits | Manquants | Soit |")
        A("|---|---|:---:|:---:|:---:|")
        for ch in non:
            r = ch["total"] - ch["fait"]
            A("| %s %s | %s | %d / %d | %d | %d h %02d |" % (P.mat[ch["matiere"]]["court"], P.libelle(ch["id"]), fr(ch["dispo"], False), ch["fait"], ch["total"], r, (r * 25) // 60, (r * 25) % 60))
        tot_r = sum(ch["total"] - ch["fait"] for ch in non)
        A("| **Total** | | | **%d** | **%d h %02d** |" % (tot_r, (tot_r * 25) // 60, (tot_r * 25) % 60))
    else:
        A("*Aucun : tout le programme estimé tient dans la capacité.*")
    A("")
    A("## Alertes de la simulation")
    A("")
    for a in P.alertes or ["Aucune."]:
        A("- " + a)
    A("")
    return "\n".join(o) + "\n"


def main():
    cfg = json.load(open(os.path.join(SEM, "planning.json"), encoding="utf-8"))
    P = Planificateur(cfg).lancer()
    b = bilan(P)
    scen = [("**Ton plan**", b, "4 P/j", "8 P/j"),
            ("Octobre à 3 h/jour", scenario(cfg, 6), "6 P/j", "8 P/j"),
            ("**Octobre à 4 h/jour** — recommandé", scenario(cfg, 8), "8 P/j", "8 P/j"),
            ("Octobre à 4 h, 1er-15 nov. à 6 h", scenario(cfg, 8, 12), "8 P/j", "12 P/j")]
    for nom, s, _, _ in scen:
        print("%-40s appris %2d/%d · manque %d P" % (nom.replace("*", ""), s["appris"], s["total"], s["manque"]))
    print("alertes :", len(P.alertes))
    if "--bilan" in sys.argv:
        for a in P.alertes:
            print("  ", a)
        return
    with open(os.path.join(SEM, "PLANNING.md"), "w", encoding="utf-8") as f:
        f.write(rendu(P, cfg, scen))
    print(os.path.join(SEM, "PLANNING.md"))


if __name__ == "__main__":
    main()
