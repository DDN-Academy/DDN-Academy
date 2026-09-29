#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Figures du cours n° 2 d'Institutions politiques — la démocratie.

    python3 Semestre1/Institutions_politiques/Cours/figures/Ch02/figures_ch02.py

Écrit à côté de ce script :
  formes_democratie.svg   les trois formes de la démocratie
  resultat_election.svg   des inscrits aux suffrages exprimés, et les seuils des législatives (à l'échelle)
  legislatives.svg        les deux tours des élections législatives
  proportionnelle.svg     le même vote, deux répartitions (plus fort reste, plus forte moyenne)
  schema_chapitre.svg     le schéma qui relie tout le chapitre (section 4.4)
"""
import os
from xml.sax.saxutils import escape

ICI = os.path.dirname(os.path.abspath(__file__))
POLICE = "font-family=\"-apple-system,'Segoe UI',Helvetica,Arial,sans-serif\""
NOIR, GRIS, BLEU, ORANGE, VERT, ROUGE = "#1d2330", "#6b7280", "#1f4e79", "#b35c00", "#2e7d32", "#b3261e"
F_BLEU, F_ORANGE, F_VERT, F_GRIS, F_ROUGE = "#e8eef6", "#fdf0e0", "#e6f2e7", "#f1f2f4", "#fbe9e7"


def txt(x, y, s, taille=12, couleur=NOIR, ancre="middle", gras=False, italique=False):
    """Texte ; les segments entre ** ** sont mis en gras."""
    st = (' font-weight="700"' if gras else "") + (' font-style="italic"' if italique else "")
    morceaux = s.split("**")
    corps = "".join(('<tspan font-weight="700">%s</tspan>' % escape(m)) if k % 2 else escape(m)
                    for k, m in enumerate(morceaux) if m)
    return '<text x="%.1f" y="%.1f" font-size="%s" fill="%s" text-anchor="%s" %s%s>%s</text>' % (
        x, y, taille, couleur, ancre, POLICE, st, corps)


def rect(x, y, w, h, fond, bord, r=8, trait=1.4, pointille=False):
    d = ' stroke-dasharray="5 4"' if pointille else ""
    return '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (
        x, y, w, h, r, fond, bord, trait, d)


def ligne(x1, y1, x2, y2, couleur=GRIS, trait=1.4, fleche=False, pointille=False):
    m = ' marker-end="url(#fl)"' if fleche else ""
    d = ' stroke-dasharray="5 4"' if pointille else ""
    return '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s%s/>' % (
        x1, y1, x2, y2, couleur, trait, m, d)


def cercle(x, y, r, fond, bord, trait=1.2):
    return '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%s"/>' % (x, y, r, fond, bord, trait)


def boite(x, y, w, h, titre, lignes, fond, bord, couleur_titre=None, taille=11.5, pas=15):
    el = [rect(x, y, w, h, fond, bord)]
    el.append(txt(x + w / 2, y + 22, titre, 13, couleur_titre or bord, gras=True))
    for k, l in enumerate(lignes):
        el.append(txt(x + w / 2, y + 42 + k * pas, l, taille, NOIR))
    return el


def svg(nom, largeur, hauteur, elements):
    defs = ('<defs><marker id="fl" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
            'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="%s"/></marker></defs>' % GRIS)
    corps = "\n".join(elements)
    contenu = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">\n%s\n%s\n</svg>\n'
               % (largeur, hauteur, largeur, hauteur, defs, corps))
    with open(os.path.join(ICI, nom), "w", encoding="utf-8") as f:
        f.write(contenu)
    print(os.path.join(ICI, nom))


def fr(n, dec=0):
    """Nombre à la française : espace des milliers, virgule décimale."""
    s = ("{:,.%df}" % dec).format(n).replace(",", " ").replace(".", ",")
    return s


# ------------------------------------------------------------------ 1. les trois formes
def formes_democratie():
    el = []
    W = 700
    cols = [
        (8, "DÉMOCRATIE DIRECTE", F_ORANGE, ORANGE,
         ["le peuple **décide lui-même**", "des lois et des décisions"],
         ["Landsgemeinde suisses", "(Glaris, Appenzell R.-I.)", "référendum, initiative,", "révocation (recall)"]),
        (240, "SEMI-REPRÉSENTATIVE", F_VERT, VERT,
         ["des **élus** décident, et le peuple", "**peut décider lui-même**"],
         ["dite aussi « semi-directe »", "**la France** : art. 3 —", "« par ses représentants et", "par la voie du référendum »"]),
        (472, "DÉMOCRATIE REPRÉSENTATIVE", F_BLEU, BLEU,
         ["le peuple **élit des représentants**", "qui **décident en son nom**"],
         ["Sieyès (1789) :", "« le peuple ne peut parler,", "ne peut agir que par", "ses représentants »"]),
    ]
    for x, titre, fo, bo, principe, ex in cols:
        w = 220
        el.append(rect(x, 10, w, 250, fo, bo))
        el.append(txt(x + w / 2, 34, titre, 12.5, bo, gras=True))
        # schéma : le peuple (rond) et, le cas échéant, les élus (carré)
        py = 92
        for k in range(5):
            el.append(cercle(x + 70 + k * 20, py, 7, "#ffffff", bo))
        el.append(txt(x + w / 2, py + 26, "le peuple", 10.5, GRIS, italique=True))
        for k, l in enumerate(principe):
            el.append(txt(x + w / 2, 150 + k * 16, l, 11.5))
        for k, l in enumerate(ex):
            el.append(txt(x + w / 2, 196 + k * 15, l, 10.5))
    # la flèche du plus direct au plus indirect
    el.append(ligne(20, 282, W - 20, 282, GRIS, 1.4, fleche=True))
    el.append(txt(20, 300, "le peuple décide seul", 11, GRIS, "start", italique=True))
    el.append(txt(W / 2, 300, "les deux à la fois", 11, GRIS, italique=True))
    el.append(txt(W - 20, 300, "les élus décident seuls", 11, GRIS, "end", italique=True))
    svg("formes_democratie.svg", W, 312, el)


# ------------------------------------------------------------------ 2. résultat d'une élection, à l'échelle
def resultat_election():
    """Exemple du cours : 100 000 inscrits, 60 000 votants, 1 500 blancs, 500 nuls, 58 000 exprimés."""
    el = []
    W, x0, larg = 700, 20, 660          # 660 px = 100 000 inscrits
    k = larg / 100000.0
    inscrits, abst, blancs, nuls = 100000, 40000, 1500, 500
    exprimes = inscrits - abst - blancs - nuls
    # barre des inscrits
    y1 = 40
    el.append(txt(x0, y1 - 10, "INSCRITS : 100 000", 12, NOIR, "start", gras=True))
    el.append(rect(x0, y1, larg, 30, F_GRIS, GRIS, r=3, trait=1))
    # barre décomposée : exprimés | blancs | nuls | abstention
    y2 = 110
    el.append(txt(x0, y2 - 10, "Ce que deviennent les inscrits", 12, NOIR, "start", gras=True))
    xa = x0
    morceaux = [(exprimes, F_BLEU, BLEU, "exprimés : 58 000"), (blancs, "#ffffff", GRIS, ""),
                (nuls, "#ffffff", GRIS, ""), (abst, F_GRIS, GRIS, "abstention : 40 000 (40 %)")]
    for v, fo, bo, lab in morceaux:
        w = v * k
        el.append(rect(xa, y2, w, 30, fo, bo, r=0, trait=1))
        if lab:
            el.append(txt(xa + w / 2, y2 + 20, lab, 11.5, bo if bo != GRIS else NOIR, gras=True))
        xa += w
    xb = x0 + exprimes * k
    el.append(ligne(xb + 6.6, y2 + 30, xb + 40, y2 + 52, GRIS, 1))
    el.append(txt(xb + 42, y2 + 56, "blancs 1 500 + nuls 500", 10.5, GRIS, "start", italique=True))
    # accolade des votants
    el.append(ligne(x0, y2 + 38, x0 + 60000 * k, y2 + 38, NOIR, 1.2))
    el.append(ligne(x0, y2 + 33, x0, y2 + 43, NOIR, 1.2))
    el.append(ligne(x0 + 60000 * k, y2 + 33, x0 + 60000 * k, y2 + 43, NOIR, 1.2))
    el.append(txt(x0 + 30000 * k, y2 + 56, "votants : 60 000", 11.5, NOIR, gras=True))
    # les seuils
    y3 = 205
    el.append(txt(x0, y3 - 12, "Les trois seuils des législatives, sur la même échelle", 12, NOIR, "start", gras=True))
    seuils = [
        (12500, ORANGE, "12,5 % des inscrits = 12 500 voix", "pour se maintenir au second tour"),
        (25000, ROUGE, "25 % des inscrits = 25 000 voix", "l'une des deux conditions du 1er tour"),
        (29001, BLEU, "majorité absolue des exprimés = 29 001 voix", "l'autre condition du 1er tour"),
    ]
    for j, (v, c, l1, l2) in enumerate(seuils):
        y = y3 + j * 44
        el.append(rect(x0, y, v * k, 20, "#ffffff", c, r=0, trait=1.4))
        el.append(ligne(x0 + v * k, y - 4, x0 + v * k, y + 24, c, 2))
        el.append(txt(x0 + v * k + 8, y + 10, l1, 11.5, c, "start", gras=True))
        el.append(txt(x0 + v * k + 8, y + 24, l2, 10.5, GRIS, "start", italique=True))
    el.append(txt(W - 12, 350, "Longueurs proportionnelles au nombre de voix · exemple du § 2.2", 10.5, GRIS, "end", italique=True))
    svg("resultat_election.svg", W, 358, el)


# ------------------------------------------------------------------ 3. les législatives
def legislatives():
    el = []
    W = 700
    el += boite(230, 8, 240, 50, "1er TOUR", [], F_GRIS, NOIR)
    el.append(txt(350, 50, "577 circonscriptions, un député chacune", 11, GRIS, italique=True))
    el.append(ligne(350, 58, 350, 84, GRIS, 1.4, fleche=True))
    # question 1
    el.append(rect(150, 86, 400, 52, "#ffffff", BLEU, r=8, trait=1.6))
    el.append(txt(350, 106, "Un candidat a-t-il **plus de 50 % des exprimés**", 12))
    el.append(txt(350, 124, "**et** au moins **25 % des inscrits** ?", 12))
    el.append(ligne(550, 112, 598, 112, VERT, 1.6, fleche=True))
    el.append(txt(574, 104, "oui", 11, VERT, gras=True))
    el += boite(600, 88, 92, 48, "ÉLU", ["au 1er tour"], F_VERT, VERT)
    el.append(ligne(350, 138, 350, 164, GRIS, 1.4, fleche=True))
    el.append(txt(362, 156, "non", 11, ROUGE, "start", gras=True))
    # question 2
    el.append(rect(150, 166, 400, 52, "#ffffff", ORANGE, r=8, trait=1.6))
    el.append(txt(350, 186, "Qui a obtenu au moins **12,5 % des inscrits** ?", 12))
    el.append(txt(350, 204, "(les inscrits, pas les exprimés)", 10.5, GRIS, italique=True))
    # trois cas
    cas = [(20, "2 candidats ou plus", ["ils peuvent se maintenir :", "duel, ou triangulaire", "sauf désistement"]),
           (250, "1 seul candidat", ["il se maintient, avec", "le deuxième du 1er tour"]),
           (480, "aucun candidat", ["les deux premiers", "du 1er tour se maintiennent"])]
    for x, t, l in cas:
        el.append(ligne(350, 218, x + 100, 246, GRIS, 1.2, fleche=True))
        el += boite(x, 248, 200, 76, t, l, F_ORANGE, ORANGE, taille=11, pas=14)
    el.append(ligne(350, 324, 350, 346, GRIS, 1.4, fleche=True))
    el.append(rect(150, 348, 400, 44, F_BLEU, BLEU, r=8, trait=1.6))
    el.append(txt(350, 368, "2d TOUR : est élu celui qui a **le plus de voix**", 12.5, BLEU))
    el.append(txt(350, 384, "la majorité relative suffit (art. L. 126 et L. 162 du Code électoral)", 10.5, GRIS, italique=True))
    svg("legislatives.svg", W, 400, el)


# ------------------------------------------------------------------ 4. la proportionnelle, deux méthodes
def proportionnelle():
    """Exemple du cours : 5 sièges, A 47 000, B 16 000, C 15 800, D 12 000, E 9 200."""
    el = []
    W = 700
    listes = [("A", 47000), ("B", 16000), ("C", 15800), ("D", 12000), ("E", 9200)]
    pfr = {"A": 2, "B": 1, "C": 1, "D": 1, "E": 0}
    pfm = {"A": 3, "B": 1, "C": 1, "D": 0, "E": 0}
    x0, larg = 108, 290                 # 290 px = 50 000 voix
    k = larg / 50000.0
    el.append(txt(12, 22, "Voix (100 000 exprimés, 5 sièges)", 12, NOIR, "start", gras=True))
    el.append(txt(470, 22, "Plus fort reste", 12, ORANGE, "middle", gras=True))
    el.append(txt(610, 22, "Plus forte moyenne", 12, BLEU, "middle", gras=True))
    # graduation du quotient
    for q in (20000, 40000):
        xq = x0 + q * k
        el.append(ligne(xq, 30, xq, 262, ROUGE, 1, pointille=True))
        el.append(txt(xq, 278, "%s" % fr(q), 10.5, ROUGE))
    el.append(txt(x0 + 20000 * k, 292, "quotient Q = 20 000 voix : 1 siège", 10.5, ROUGE, italique=True))
    for j, (nom, v) in enumerate(listes):
        y = 40 + j * 44
        el.append(txt(20, y + 18, nom, 13, NOIR, gras=True))
        el.append(txt(x0 - 8, y + 18, fr(v), 11, NOIR, "end"))
        el.append(rect(x0, y, v * k, 26, F_GRIS, GRIS, r=2, trait=1))
        for cx, n, c, fo in ((470, pfr[nom], ORANGE, F_ORANGE), (610, pfm[nom], BLEU, F_BLEU)):
            if n == 0:
                el.append(txt(cx, y + 18, "0", 11.5, GRIS))
            for s in range(n):
                el.append(cercle(cx - (n - 1) * 11 + s * 22, y + 13, 9, fo, c, 1.6))
    el.append(txt(470, 262, "A 2 · B 1 · C 1 · D 1", 11, ORANGE, gras=True))
    el.append(txt(610, 262, "A 3 · B 1 · C 1", 11, BLEU, gras=True))
    el.append(txt(470, 280, "avantage aux petites listes", 10.5, GRIS, italique=True))
    el.append(txt(610, 280, "avantage aux grandes listes", 10.5, GRIS, italique=True))
    svg("proportionnelle.svg", W, 302, el)


# ------------------------------------------------------------------ 5. le schéma du chapitre
def schema_chapitre():
    el = []
    W = 700
    cx, cy = 350, 210
    el.append(ligne(cx, cy, 150, 110, GRIS, 1.6))
    el.append(ligne(cx, cy, 560, 110, GRIS, 1.6))
    el.append(ligne(cx, cy, cx, 290, GRIS, 1.6))
    el += boite(8, 10, 300, 168, "EXERCER LE POUVOIR : 3 FORMES", [
        "**directe** : le peuple décide (Landsgemeinde)",
        "**représentative** : des élus décident",
        "(Sieyès : souveraineté nationale ;",
        "Rousseau : souveraineté populaire)",
        "**semi-représentative** : les deux",
        "**France** : art. 3, art. 27 ; référendum",
        "de l'art. 11 (8 fois) et de l'art. 89"], F_ORANGE, ORANGE, taille=11, pas=17)
    el += boite(392, 10, 300, 168, "QUI VOTE ? QUI EST ÉLU ?", [
        "**électorat** : suffrage universel",
        "(1848, 1944, 1974) ; nationalité, âge,",
        "droits civiques ; inscription ; art. 88-3",
        "**éligibilité** : 18 ans (24 au Sénat) ;",
        "inéligibilité ≠ incompatibilité ; parité",
        "**suffrage** : universel, égal, secret",
        "exprimés = votants − blancs − nuls"], F_VERT, VERT, taille=11, pas=17)
    el.append(rect(cx - 110, cy - 32, 220, 64, F_BLEU, BLEU, r=10, trait=2))
    el.append(txt(cx, cy - 6, "LA DÉMOCRATIE", 17, BLEU, gras=True))
    el.append(txt(cx, cy + 16, "le pouvoir du peuple — art. 2 al. 5", 11, NOIR, italique=True))
    el += boite(110, 290, 480, 140, "DES VOIX AUX SIÈGES : 3 MODES DE SCRUTIN", [
        "**majoritaire** : 1 tour (Royaume-Uni) ; 2 tours (législatives : 50 % des",
        "exprimés + 25 % des inscrits, puis 12,5 % des inscrits) — stabilité",
        "**proportionnel** : quotient, plus fort reste, plus forte moyenne — représentativité",
        "**mixte** : prime majoritaire (municipales 50 %, régionales 25 %)",
        "Duverger (1951) : 1 tour → 2 partis ; 2 tours → alliances ; RP → multipartisme"],
        F_BLEU, BLEU, taille=11, pas=18)
    svg("schema_chapitre.svg", W, 440, el)


if __name__ == "__main__":
    formes_democratie()
    resultat_election()
    legislatives()
    proportionnelle()
    schema_chapitre()
