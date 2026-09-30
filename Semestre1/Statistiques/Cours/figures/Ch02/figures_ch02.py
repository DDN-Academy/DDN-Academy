#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Figures du cours n° 2 de Techniques statistiques — résumer pour informer.

    python3 Semestre1/Statistiques/Cours/figures/Ch02/figures_ch02.py

Écrit à côté de ce script :
  histogramme_incarceres.svg   histogramme à classes inégales (personnes incarcérées, 2020)
  asymetrie.svg                moyenne et médiane selon la forme de la distribution
  interpolation.svg            la médiane par interpolation linéaire (familles, 2008)
  cas_dispersion.svg           les quatre classes de 50 élèves, même moyenne, dispersions différentes
  boxplot_salaires.svg         boîtes à moustaches des salaires par catégorie socio-professionnelle
  ibt.svg                      l'inégalité de Bienaymé-Tchebychev : m ± 2σ et m ± 3σ
  rentabilites.svg             22 rentabilités journalières et l'intervalle m ± 2σ
  lorenz.svg                   courbes de Lorenz des salaires, 2005 et 2021
  gini_trapezes.svg            l'indice de Gini de 2005 : aire de concentration et trapèzes
  schema_chapitre.svg          le schéma qui relie tout le chapitre (section 4.4)
Tous les graphiques sont à l'échelle ; les valeurs affichées sont celles du cours.
"""
import os
from decimal import Decimal, ROUND_HALF_UP
from xml.sax.saxutils import escape

ICI = os.path.dirname(os.path.abspath(__file__))
POLICE = "font-family=\"-apple-system,'Segoe UI',Helvetica,Arial,sans-serif\""
NOIR, GRIS, BLEU, ORANGE, VERT, ROUGE, VIOLET = "#1d2330", "#6b7280", "#1f4e79", "#b35c00", "#2e7d32", "#b3261e", "#6a3d9a"
F_BLEU, F_ORANGE, F_VERT, F_GRIS, F_ROUGE = "#e8eef6", "#fdf0e0", "#e6f2e7", "#f1f2f4", "#fbe9e7"


def txt(x, y, s, taille=12, couleur=NOIR, ancre="middle", gras=False, italique=False, rot=None):
    """Texte ; les segments entre ** ** sont mis en gras."""
    st = (' font-weight="700"' if gras else "") + (' font-style="italic"' if italique else "")
    tr = ' transform="rotate(%s %.1f %.1f)"' % (rot, x, y) if rot is not None else ""
    morceaux = str(s).split("**")
    corps = "".join(('<tspan font-weight="700">%s</tspan>' % escape(m)) if k % 2 else escape(m)
                    for k, m in enumerate(morceaux) if m)
    return '<text x="%.1f" y="%.1f" font-size="%s" fill="%s" text-anchor="%s" %s%s%s>%s</text>' % (
        x, y, taille, couleur, ancre, POLICE, st, tr, corps)


def rect(x, y, w, h, fond, bord, r=8, trait=1.4, pointille=False, opacite=None):
    d = ' stroke-dasharray="5 4"' if pointille else ""
    o = ' fill-opacity="%s"' % opacite if opacite is not None else ""
    return '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s"%s stroke="%s" stroke-width="%s"%s/>' % (
        x, y, w, h, r, fond, o, bord, trait, d)


def ligne(x1, y1, x2, y2, couleur=GRIS, trait=1.4, fleche=False, pointille=False):
    m = ' marker-end="url(#fl)"' if fleche else ""
    d = ' stroke-dasharray="5 4"' if pointille else ""
    return '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s%s/>' % (
        x1, y1, x2, y2, couleur, trait, m, d)


def chemin(d, couleur=GRIS, trait=1.4, fleche=False, pointille=False, fond="none", opacite=None):
    m = ' marker-end="url(#fl)"' if fleche else ""
    p = ' stroke-dasharray="5 4"' if pointille else ""
    o = ' fill-opacity="%s"' % opacite if opacite is not None else ""
    return '<path d="%s" fill="%s"%s stroke="%s" stroke-width="%s"%s%s/>' % (d, fond, o, couleur, trait, m, p)


def point(x, y, couleur=BLEU, r=3.6, plein=True):
    return '<circle cx="%.1f" cy="%.1f" r="%s" fill="%s" stroke="%s" stroke-width="1.6"/>' % (
        x, y, r, couleur if plein else "#ffffff", couleur)


def boite(x, y, w, h, titre, lignes, fond, bord, couleur_titre=None, taille=11.5, pas=19, taille_titre=13):
    el = [rect(x, y, w, h, fond, bord)]
    el.append(txt(x + w / 2, y + 22, titre, taille_titre, couleur_titre or bord, gras=True))
    for k, l in enumerate(lignes):
        el.append(txt(x + w / 2, y + 42 + k * pas, l, taille, NOIR))
    return el


def svg(nom, largeur, hauteur, elements):
    defs = ('<defs><marker id="fl" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
            'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="%s"/></marker></defs>' % GRIS)
    contenu = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">\n'
               '<rect x="0" y="0" width="%d" height="%d" fill="#ffffff"/>\n%s\n%s\n</svg>\n'
               % (largeur, hauteur, largeur, hauteur, largeur, hauteur, defs, "\n".join(elements)))
    with open(os.path.join(ICI, nom), "w", encoding="utf-8") as f:
        f.write(contenu)
    print(os.path.join(ICI, nom))


def fr(n, dec=0):
    """Nombre à la française, arrondi au plus proche."""
    n = float(Decimal(str(n)).quantize(Decimal(1).scaleb(-dec), rounding=ROUND_HALF_UP))
    return ("{:,.%df}" % dec).format(n).replace(",", " ").replace(".", ",")


class Axes:
    """Repère simple : X(x), Y(y) ; graduations et grille légère."""

    def __init__(self, el, x0, x1, y0, y1, g, d, h, b, W, H):
        self.el, self.x0, self.x1, self.y0, self.y1 = el, x0, x1, y0, y1
        self.g, self.d, self.h, self.b, self.W, self.H = g, d, h, b, W, H

    def X(self, x):
        return self.g + (x - self.x0) / (self.x1 - self.x0) * (self.W - self.g - self.d)

    def Y(self, y):
        return self.H - self.b - (y - self.y0) / (self.y1 - self.y0) * (self.H - self.b - self.h)

    def cadre(self, gx, gy, fx, fy, etiq_x, etiq_y, grille=True):
        el = self.el
        for v in gy:
            if grille:
                el.append(ligne(self.g, self.Y(v), self.W - self.d, self.Y(v), "#e3e6ea", 1))
            el.append(txt(self.g - 6, self.Y(v) + 4, fy(v), 10, GRIS, "end"))
        for v in gx:
            el.append(ligne(self.X(v), self.Y(self.y0), self.X(v), self.Y(self.y0) + 4, NOIR, 1))
            el.append(txt(self.X(v), self.Y(self.y0) + 16, fx(v), 10.5, NOIR))
        el.append(ligne(self.g, self.Y(self.y0), self.W - self.d + 4, self.Y(self.y0), NOIR, 1.3))
        el.append(ligne(self.g, self.Y(self.y0), self.g, self.h - 8, NOIR, 1.3))
        el.append(txt(self.g - 4, self.h - 14, etiq_y, 10.5, NOIR, "start", italique=True))
        el.append(txt(self.W - self.d, self.Y(self.y0) + 32, etiq_x, 10.5, NOIR, "end", italique=True))


# ------------------------------------------------------------------ 1. histogramme
def histogramme_incarceres():
    el = []
    W, H = 680, 380
    A = Axes(el, 10, 85, 0, 4.2, 58, 20, 36, 70, W, H)
    classes = [(16, 18, 819), (18, 21, 5361), (21, 25, 11444), (25, 30, 14950), (30, 40, 23979), (40, 50, 13413), (50, 60, 6501), (60, 80, 3321)]
    N = sum(c[2] for c in classes)
    A.cadre([16, 18, 21, 25, 30, 40, 50, 60, 80], [0, 1, 2, 3, 4], lambda v: "%d" % v, lambda v: "%d %%" % v,
            "Âge (en années)", "Densité (en % par année d'âge)")
    for a, b, n in classes:
        f = n / N * 100
        d = f / (b - a)
        modal = (a == 25)
        der = (a == 60)
        el.append(rect(A.X(a), A.Y(d), A.X(b) - A.X(a), A.Y(0) - A.Y(d), F_ORANGE if modal else F_BLEU, ORANGE if modal else BLEU, 0, 1.6, pointille=der))
        el.append(txt((A.X(a) + A.X(b)) / 2, A.Y(d) - 5, fr(d, 2), 10, ORANGE if modal else BLEU, gras=True))
    # aire de la classe modale
    el.append(txt(A.X(27.5), A.Y(1.95), "aire =", 10, ORANGE, gras=True))
    el.append(txt(A.X(27.5), A.Y(1.6), "18,7 %", 10, ORANGE, gras=True))
    el.append(txt(A.X(70), A.Y(1.0), "classe ouverte :", 10, GRIS, italique=True))
    el.append(txt(A.X(70), A.Y(0.72), "60-80 par convention", 10, GRIS, italique=True))
    el.append(txt(W / 2 + 20, H - 12, "Chaque rectangle : largeur = amplitude, hauteur = densité, aire = fréquence. Classe modale : 25-30 ans (en orange).", 10.5, GRIS, italique=True))
    svg("histogramme_incarceres.svg", W, H, el)


# ------------------------------------------------------------------ 2. asymétrie
def courbe_densite(el, x0, y0, w, h, fonction, n=80, couleur=BLEU):
    pts = []
    for k in range(n + 1):
        t = k / n
        pts.append((x0 + t * w, y0 - fonction(t) * h))
    d = "M%.1f,%.1f " % (x0, y0) + " ".join("L%.1f,%.1f" % p for p in pts) + " L%.1f,%.1f Z" % (x0 + w, y0)
    el.append(chemin(d, couleur, 1.8, fond=F_BLEU))
    return pts


def asymetrie():
    import math
    el = []
    W, H = 700, 270
    # symétrique
    x0, y0, w, h = 30, 200, 300, 150
    courbe_densite(el, x0, y0, w, h, lambda t: math.exp(-((t - 0.5) ** 2) / 0.02))
    el.append(ligne(x0, y0, x0 + w, y0, NOIR, 1.3))
    el.append(ligne(x0 + w / 2, y0, x0 + w / 2, y0 - h - 6, ROUGE, 1.6, pointille=True))
    el.append(txt(x0 + w / 2, y0 + 18, "médiane = moyenne", 12, ROUGE, gras=True))
    el.append(txt(x0 + w / 2, 26, "Distribution symétrique", 13, BLEU, gras=True))
    # étalée à droite
    x0 = 380
    f = lambda t: (t / 0.18) * math.exp(1 - t / 0.18) if t > 0 else 0
    courbe_densite(el, x0, y0, w, h, f)
    el.append(ligne(x0, y0, x0 + w, y0, NOIR, 1.3))
    xmed, xmoy = x0 + w * 0.30, x0 + w * 0.36
    el.append(ligne(xmed, y0, xmed, y0 - h * 0.86, VERT, 1.6, pointille=True))
    el.append(ligne(xmoy, y0, xmoy, y0 - h * 0.74, ROUGE, 1.6, pointille=True))
    el.append(txt(xmed - 4, y0 + 18, "médiane", 11.5, VERT, "end", gras=True))
    el.append(txt(xmoy + 4, y0 + 18, "< moyenne", 11.5, ROUGE, "start", gras=True))
    el.append(txt(x0 + w / 2, 26, "Distribution étalée à droite", 13, BLEU, gras=True))
    el.append(txt(x0 + w * 0.78, y0 - 112, "valeurs extrêmes :", 10.5, ORANGE, gras=True))
    el.append(txt(x0 + w * 0.78, y0 - 98, "elles tirent la moyenne", 10.5, ORANGE))
    el.append(ligne(x0 + w * 0.82, y0 - 92, x0 + w * 0.88, y0 - 30, ORANGE, 1.2, fleche=True))
    el.append(txt(W / 2, H - 16, "Exemple type d'une distribution étalée à droite : les revenus. La médiane résiste aux valeurs extrêmes, la moyenne non.", 10.5, GRIS, italique=True))
    svg("asymetrie.svg", W, H, el)


# ------------------------------------------------------------------ 3. interpolation
def interpolation():
    el = []
    W, H = 680, 280
    xa, xb = 90, 610
    yF, yX = 90, 200
    t_med = (0.5 - 0.48) / (0.703 - 0.48)
    xm = xa + t_med * (xb - xa)
    # droite des fréquences cumulées
    el.append(txt(xa, yF - 42, "Fréquences cumulées F", 12, BLEU, "start", gras=True))
    el.append(ligne(xa, yF, xb, yF, BLEU, 2.4))
    for x, lab in [(xa, "F(x_A) = 0,48"), (xb, "F(x_B) = 0,703")]:
        el.append(ligne(x, yF - 8, x, yF + 8, BLEU, 1.6))
        el.append(txt(x, yF - 14, lab, 11.5, BLEU, gras=True))
    el.append(ligne(xm, yF - 8, xm, yF + 8, ROUGE, 2.2))
    el.append(txt(xm + 6, yF + 22, "0,5 : la médiane", 11.5, ROUGE, "start", gras=True))
    # droite des modalités
    el.append(txt(xa, yX + 46, "Nombre d'enfants x", 12, VERT, "start", gras=True))
    el.append(ligne(xa, yX, xb, yX, VERT, 2.4))
    for x, lab in [(xa, "x_A = 0"), (xb, "x_B = 1")]:
        el.append(ligne(x, yX - 8, x, yX + 8, VERT, 1.6))
        el.append(txt(x, yX + 24, lab, 11.5, VERT, gras=True))
    el.append(ligne(xm, yX - 8, xm, yX + 8, ROUGE, 2.2))
    el.append(txt(xm + 6, yX - 14, "Med ≈ 0,089", 11.5, ROUGE, "start", gras=True))
    el.append(ligne(xm, yF + 34, xm, yX - 26, ROUGE, 1.4, fleche=True, pointille=True))
    el.append(txt(xm + 16, (yF + yX) / 2 + 4, "même proportion du chemin : (0,5 − 0,48) / (0,703 − 0,48) = 0,02 / 0,223 ≈ 0,089", 11, ROUGE, "start"))
    el.append(txt(W / 2, H - 10, "Med ≈ x_A + (x_B − x_A) × (0,5 − F(x_A)) / (F(x_B) − F(x_A)) = 0 + 1 × 0,089 ≈ 0,089 enfant (méthode du cours)", 11, NOIR, gras=True))
    svg("interpolation.svg", W, H, el)


# ------------------------------------------------------------------ 4. les quatre cas
def cas_dispersion():
    el = []
    W, H = 720, 400
    cas = [("Cas 1 : σ = 0", {12: 50}), ("Cas 2 : σ ≈ 3,32", {7: 5, 8: 5, 9: 5, 10: 5, 11: 5, 13: 5, 14: 5, 15: 5, 16: 5, 17: 5}),
           ("Cas 3 : σ ≈ 5,37", {6: 20, 12: 10, 18: 20}), ("Cas 4 : σ ≈ 4,56", {4: 5, 8: 10, 10: 10, 14: 10, 16: 10, 20: 5})]
    for k, (titre, d) in enumerate(cas):
        cx, cy = (k % 2) * 360, (k // 2) * 190
        g, x0, y0, w, h = cx + 40, cx + 40, cy + 160, 300, 118
        el.append(txt(cx + 190, cy + 24, titre, 12.5, BLEU, gras=True))
        top = 50 if k == 0 else 20
        for v in (0, top):
            el.append(txt(x0 - 6, y0 - v / top * h + 4, "%d" % v, 9.5, GRIS, "end"))
        el.append(ligne(x0, y0, x0 + w, y0, NOIR, 1.2))
        el.append(ligne(x0, y0, x0, y0 - h - 4, NOIR, 1.2))
        for note in range(0, 21, 2):
            X = x0 + note / 20 * w
            el.append(ligne(X, y0, X, y0 + 3, NOIR, 1))
            el.append(txt(X, y0 + 14, note, 9.5, NOIR))
        for note, n in d.items():
            X = x0 + note / 20 * w
            el.append(rect(X - 5, y0 - n / top * h, 10, n / top * h, BLEU, BLEU, 0, 0.5))
        Xm = x0 + 12 / 20 * w
        el.append(ligne(Xm, y0, Xm, y0 - h - 2, ROUGE, 1.4, pointille=True))
        el.append(txt(Xm + 4, y0 - h + 2, "m = 12", 10, ROUGE, "start", gras=True))
    el.append(txt(W / 2, H - 8, "Même moyenne (12/20), même effectif (50 élèves) : seule la dispersion change. Hauteur = nombre d'élèves.", 10.5, GRIS, italique=True))
    svg("cas_dispersion.svg", W, H, el)


# ------------------------------------------------------------------ 5. boîtes à moustaches
def boxplot_salaires():
    el = []
    W, H = 700, 330
    S = [("Ensemble", 1440, 1660, 2090, 2880, 4160), ("Cadres", 2240, 2810, 3620, 4930, 7060),
         ("Prof. intermédiaires", 1640, 1940, 2360, 2890, 3590), ("Employés", 1380, 1510, 1730, 2060, 2520),
         ("Ouvriers", 1380, 1570, 1830, 2200, 2630)]
    A = Axes(el, 1000, 7500, 0, 5.6, 150, 20, 20, 74, W, H)
    for v in range(1000, 7501, 1000):
        el.append(ligne(A.X(v), 20, A.X(v), A.Y(0), "#e3e6ea", 1))
        el.append(txt(A.X(v), A.Y(0) + 16, fr(v), 10, NOIR))
    el.append(ligne(A.g, A.Y(0), W - 20, A.Y(0), NOIR, 1.3))
    el.append(txt(W - 20, A.Y(0) + 34, "Salaire mensuel net (en euros)", 10.5, NOIR, "end", italique=True))
    for k, (nom, d1, q1, d5, q3, d9) in enumerate(S):
        y = A.Y(5 - k)
        coul = ORANGE if nom == "Cadres" else BLEU
        el.append(txt(A.g - 10, y + 4, nom, 11, NOIR, "end", gras=(nom == "Cadres")))
        el.append(ligne(A.X(d1), y, A.X(q1), y, coul, 1.6))
        el.append(ligne(A.X(q3), y, A.X(d9), y, coul, 1.6))
        el.append(ligne(A.X(d1), y - 8, A.X(d1), y + 8, coul, 1.6))
        el.append(ligne(A.X(d9), y - 8, A.X(d9), y + 8, coul, 1.6))
        el.append(rect(A.X(q1), y - 14, A.X(q3) - A.X(q1), 28, F_ORANGE if nom == "Cadres" else F_BLEU, coul, 2, 1.6))
        el.append(ligne(A.X(d5), y - 14, A.X(d5), y + 14, ROUGE, 2.4))
    el.append(txt(W / 2 + 40, H - 22, "Moustaches : D1 et D9 · boîte : Q1 et Q3 · trait rouge : la médiane D5.", 10.5, GRIS, italique=True))
    el.append(txt(W / 2 + 40, H - 7, "Plus la boîte et les moustaches sont longues, plus les salaires sont dispersés.", 10.5, GRIS, italique=True))
    svg("boxplot_salaires.svg", W, H, el)


# ------------------------------------------------------------------ 6. Bienaymé-Tchebychev
def ibt():
    el = []
    W, H = 700, 230
    x0, x1, y = 60, 640, 120
    X = lambda k: (x0 + x1) / 2 + k * 80
    el.append(ligne(x0, y, x1, y, NOIR, 1.6, fleche=True))
    for k, lab in [(-3, "m − 3σ"), (-2, "m − 2σ"), (0, "m"), (2, "m + 2σ"), (3, "m + 3σ")]:
        el.append(ligne(X(k), y - 7, X(k), y + 7, NOIR, 1.6))
        el.append(txt(X(k), y + 24, lab, 12, NOIR, gras=(k == 0)))
    el.append(rect(X(-2), y - 40, X(2) - X(-2), 26, F_BLEU, BLEU, 4))
    el.append(txt(X(0), y - 22, "au moins 75 % des observations (k = 2)", 12, BLEU, gras=True))
    el.append(rect(X(-3), y - 76, X(3) - X(-3), 26, F_VERT, VERT, 4))
    el.append(txt(X(0), y - 58, "au moins 1 − 1/9 ≈ 89 % des observations (k = 3)", 12, VERT, gras=True))
    el.append(txt(X(-2.5) - 40, y + 60, "au plus 25 % en dehors de m ± 2σ ;", 11, ORANGE, "middle"))
    el.append(txt(X(2.5) + 40, y + 60, "si la distribution est symétrique,", 11, ORANGE, "middle"))
    el.append(txt(X(-2.5) - 40, y + 76, "au plus 11 % en dehors de m ± 3σ", 11, ORANGE, "middle"))
    el.append(txt(X(2.5) + 40, y + 76, "au plus la moitié de chaque côté", 11, ORANGE, "middle"))
    svg("ibt.svg", W, H, el)


# ------------------------------------------------------------------ 7. rentabilités
def rentabilites():
    el = []
    W, H = 700, 330
    prix = [35.02, 34.78, 34.18, 34.90, 34.53, 34.31, 33.84, 34.56, 34.87, 34.51, 35.22, 37.15, 37.78, 38.17, 39.01, 38.92, 38.31, 39.99, 40.20, 39.54, 39.53, 38.92, 39.67]
    r = [(prix[i] - prix[i - 1]) / prix[i - 1] * 100 for i in range(1, len(prix))]
    m = sum(r) / len(r)
    s = (sum((x - m) ** 2 for x in r) / len(r)) ** 0.5
    A = Axes(el, 0, 23, -4.5, 6, 58, 20, 30, 56, W, H)
    for v in (-4, -2, 0, 2, 4, 6):
        el.append(ligne(A.g, A.Y(v), W - 20, A.Y(v), "#e3e6ea", 1))
        el.append(txt(A.g - 6, A.Y(v) + 4, "%d %%" % v, 10, GRIS, "end"))
    el.append(rect(A.g, A.Y(m + 2 * s), W - 20 - A.g, A.Y(m - 2 * s) - A.Y(m + 2 * s), F_VERT, VERT, 0, 1, pointille=True, opacite=0.6))
    el.append(ligne(A.g, A.Y(m), W - 20, A.Y(m), ROUGE, 1.4, pointille=True))
    el.append(txt(A.g + 6, A.Y(m) - 5, "m = 0,587 %", 10.5, ROUGE, "start", gras=True))
    el.append(txt(W - 22, A.Y(m + 2 * s) - 5, "m + 2σ = 4,49 %", 10.5, VERT, "end", gras=True))
    el.append(txt(W - 22, A.Y(m - 2 * s) + 14, "m − 2σ = −3,32 %", 10.5, VERT, "end", gras=True))
    for k, v in enumerate(r):
        x = A.X(k + 1)
        dedans = m - 2 * s <= v <= m + 2 * s
        c = BLEU if dedans else ORANGE
        y1, y2 = (A.Y(v), A.Y(0)) if v >= 0 else (A.Y(0), A.Y(v))
        el.append(rect(x - 8, y1, 16, y2 - y1, c, c, 0, 0.5))
    el.append(ligne(A.g, A.Y(0), W - 20, A.Y(0), NOIR, 1.2))
    el.append(ligne(A.g, A.Y(-4.5), A.g, 24, NOIR, 1.2))
    for k in (1, 5, 10, 15, 20, 22):
        el.append(txt(A.X(k), A.Y(-4.5) + 14, k, 9.5, NOIR))
    el.append(txt(A.g - 2, 18, "Rentabilité journalière (en %)", 10.5, NOIR, "start", italique=True))
    el.append(txt(W / 2 + 20, H - 22, "Jours de cotation, du 23 août au 21 septembre 2012 (22 rentabilités). En orange : le seul jour hors de m ± 2σ (+5,48 %).", 10.5, GRIS, italique=True))
    el.append(txt(W / 2 + 20, H - 7, "21 jours sur 22 (95 %) sont dans l'intervalle : au moins 75 % l'étaient, selon Bienaymé-Tchebychev.", 10.5, GRIS, italique=True))
    svg("rentabilites.svg", W, H, el)


# ------------------------------------------------------------------ 8. Lorenz
def lorenz():
    el = []
    W, H = 560, 440
    A = Axes(el, 0, 100, 0, 100, 64, 30, 30, 64, W, H)
    A.cadre([0, 20, 40, 60, 80, 100], [0, 20, 40, 60, 80, 100], lambda v: "%d %%" % v, lambda v: "%d %%" % v,
            "Part cumulée des salariés", "Part cumulée de la masse salariale")
    el.append(ligne(A.X(0), A.Y(0), A.X(100), A.Y(100), GRIS, 1.4, pointille=True))
    el.append(txt(A.X(55), A.Y(62), "égalité parfaite", 10.5, GRIS, italique=True, rot=-39))
    for pts, coul, nom, dx, dy in [([0, 11.2, 24.5, 40.7, 61.8, 100], BLEU, "2005", -46, -10), ([0, 3.9, 14.5, 32.9, 59.6, 100], ORANGE, "2021", 10, 22)]:
        d = " ".join("%s%.1f,%.1f" % ("M" if k == 0 else "L", A.X(20 * k), A.Y(v)) for k, v in enumerate(pts))
        el.append(chemin(d, coul, 2.6))
        for k, v in enumerate(pts):
            el.append(point(A.X(20 * k), A.Y(v), coul))
            if 0 < k < 5:
                el.append(txt(A.X(20 * k) + (-8 if nom == "2005" else 9), A.Y(v) + (-8 if nom == "2005" else 4), fr(v, 1), 10, coul, "end" if nom == "2005" else "start", gras=True))
        el.append(txt(A.X(50) + dx, A.Y(pts[3] - 6) + dy, nom, 12.5, coul, gras=True))
    el.append(txt(W / 2 + 20, H - 12, "La courbe de 2021 est partout plus loin de la diagonale : inégalités plus fortes.", 10.5, GRIS, italique=True))
    svg("lorenz.svg", W, H, el)


def gini_trapezes():
    el = []
    W, H = 560, 440
    A = Axes(el, 0, 100, 0, 100, 64, 30, 30, 64, W, H)
    pts = [0, 11.2, 24.5, 40.7, 61.8, 100]
    # aire de concentration
    d = "M%.1f,%.1f " % (A.X(0), A.Y(0)) + " ".join("L%.1f,%.1f" % (A.X(20 * k), A.Y(v)) for k, v in enumerate(pts)) + " Z"
    el.append(chemin(d, ROUGE, 0.5, fond="#f4c7c3", opacite=0.9))
    # un trapèze mis en évidence : de 60 à 80 %
    tr = "M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f L%.1f,%.1f Z" % (A.X(60), A.Y(0), A.X(60), A.Y(40.7), A.X(80), A.Y(61.8), A.X(80), A.Y(0))
    el.append(chemin(tr, BLEU, 1.8, fond=F_BLEU, opacite=0.9))
    A.cadre([0, 20, 40, 60, 80, 100], [0, 20, 40, 60, 80, 100], lambda v: "%d %%" % v, lambda v: "%d %%" % v,
            "Part cumulée des salariés", "Part cumulée de la masse salariale")
    el.append(ligne(A.X(0), A.Y(0), A.X(100), A.Y(100), NOIR, 1.4))
    dd = " ".join("%s%.1f,%.1f" % ("M" if k == 0 else "L", A.X(20 * k), A.Y(v)) for k, v in enumerate(pts))
    el.append(chemin(dd, BLEU, 2.4))
    for k, v in enumerate(pts):
        el.append(point(A.X(20 * k), A.Y(v), BLEU))
    el.append(txt(A.X(70), A.Y(28), "trapèze :", 11, BLEU, gras=True))
    el.append(txt(A.X(70), A.Y(22), "b = 40,7 ; B = 61,8", 10.5, BLEU))
    el.append(txt(A.X(70), A.Y(16), "h = 20", 10.5, BLEU))
    el.append(txt(A.X(70), A.Y(9), "aire = 0,1025", 10.5, BLEU, gras=True))
    el.append(txt(A.X(30), A.Y(52), "aire de", 11, ROUGE, gras=True))
    el.append(txt(A.X(30), A.Y(46), "concentration", 11, ROUGE, gras=True))
    el.append(ligne(A.X(35), A.Y(43), A.X(46), A.Y(36), ROUGE, 1.2, fleche=True))
    el.append(txt(W / 2 + 20, H - 12, "Gini = 2 × aire de concentration = 2 × (0,5 − somme des aires des trapèzes) ≈ 0,247", 10.5, NOIR, gras=True))
    svg("gini_trapezes.svg", W, H, el)


# ------------------------------------------------------------------ schéma du chapitre
def schema_chapitre():
    el = []
    W, H = 780, 450
    el.append(rect(290, 12, 200, 52, BLEU, BLEU))
    el.append(txt(390, 34, "RÉSUMER", 14, "#ffffff", gras=True))
    el.append(txt(390, 52, "une distribution en quelques nombres", 10.5, "#ffffff"))
    blocs = [
        (10, 96, 245, 330, "1. Position : où ?", ["**mode** : la plus fréquente", "classes : la plus forte densité", "(d = f / a ; histogramme)", "**moyenne** : 3 formules", "brutes · distribution · groupes", "linéaire, sensible aux extrêmes", "**médiane** : F = 50 %", "rang central ou interpolation", "**quantiles** Q1, Q3, D1, D9", "étalée à droite : méd < moy"], BLEU, F_BLEU),
        (267, 96, 245, 330, "2. Dispersion : comment ?", ["**étendue** : max − min", "**D9 − D1**, **Q3 − Q1**, D9/D1", "boîte à moustaches", "**EAM** = moyenne des |x − m|", "**variance** σ² (Koenig)", "V(aX + b) = a² V(X)", "**σ** dans l'unité de X", "**CV** = σ / m, sans unité", "**Tchebychev** : m ± kσ ⊃ 1 − 1/k²", "V = V intra + V inter"], ORANGE, F_ORANGE),
        (524, 96, 245, 330, "3. Concentration : à qui ?", ["la **somme** de X se partage", "part de l'agrégat :", "effectif × moyenne / total", "**courbe de Lorenz** :", "part cumulée de la masse", "selon la part cumulée des individus", "loin de la diagonale : inégal", "**Gini** = 2 × aire de concentration", "= 1 − Σ (b + B) × h", "0 égalité · 1 concentration max."], VERT, F_VERT),
    ]
    for x, y, w, hh, t, ls, c, f in blocs:
        el += boite(x, y, w, hh, t, ls, f, c, c, 11, 27)
        el.append(ligne(390, 64, x + w / 2, y - 2, GRIS, 1.4, fleche=True))
    svg("schema_chapitre.svg", W, H, el)


# ------------------------------------------------------------------ corrigés de TD
def histogramme_scolarises():
    el = []
    W, H = 680, 360
    A = Axes(el, 0, 32, 0, 8, 58, 20, 36, 64, W, H)
    cl = [(2, 6, 2499939), (6, 12, 4187564), (12, 15, 3286073), (15, 18, 2410309), (18, 22, 2194176), (22, 30, 765961)]
    N = sum(c[2] for c in cl)
    A.cadre([2, 6, 12, 15, 18, 22, 30], [0, 2, 4, 6, 8], lambda v: "%d" % v, lambda v: "%d %%" % v,
            "Âge (en années)", "Densité (en % par année d'âge)")
    for a, b, n in cl:
        d = n / N * 100 / (b - a)
        modal = (a == 12)
        el.append(rect(A.X(a), A.Y(d), A.X(b) - A.X(a), A.Y(0) - A.Y(d), F_ORANGE if modal else F_BLEU, ORANGE if modal else BLEU, 0, 1.6))
        el.append(txt((A.X(a) + A.X(b)) / 2, A.Y(d) - 5, fr(d, 2), 10, ORANGE if modal else BLEU, gras=True))
        el.append(txt((A.X(a) + A.X(b)) / 2, A.Y(d / 2) + 4, fr(n / N * 100, 1) + " %", 9.5, NOIR))
    el.append(txt(W / 2 + 20, H - 10, "Dans chaque rectangle : la fréquence (= son aire). Classe modale : 12-15 ans (en orange).", 10.5, GRIS, italique=True))
    svg("histogramme_scolarises.svg", W, H, el)


def lorenz_simple(nom, courbes, titre_x, titre_y, note, pop_points=None):
    el = []
    W, H = 560, 440
    A = Axes(el, 0, 100, 0, 100, 64, 30, 30, 64, W, H)
    A.cadre([0, 20, 40, 60, 80, 100], [0, 20, 40, 60, 80, 100], lambda v: "%d %%" % v, lambda v: "%d %%" % v, titre_x, titre_y)
    el.append(ligne(A.X(0), A.Y(0), A.X(100), A.Y(100), GRIS, 1.4, pointille=True))
    for xs, ys, coul, lab, pos in courbes:
        d = " ".join("%s%.1f,%.1f" % ("M" if k == 0 else "L", A.X(x), A.Y(y)) for k, (x, y) in enumerate(zip(xs, ys)))
        el.append(chemin(d, coul, 2.6))
        for k, (x, y) in enumerate(zip(xs, ys)):
            el.append(point(A.X(x), A.Y(y), coul))
            if 0 < k < len(xs) - 1 and y > 0:
                el.append(txt(A.X(x) + (-8 if pos == "haut" else 9), A.Y(y) + (-8 if pos == "haut" else 4), fr(y, 1), 10, coul, "end" if pos == "haut" else "start", gras=True))
        k = len(xs) // 2
        el.append(txt(A.X(xs[k]) + (-30 if pos == "haut" else 30), A.Y(ys[k]) + (-26 if pos == "haut" else 30), lab, 12.5, coul, gras=True))
    el.append(txt(W / 2 + 20, H - 12, note, 10.5, GRIS, italique=True))
    svg(nom, W, H, el)


def lorenz_corriges():
    lorenz_simple("lorenz_pays_a.svg", [([0, 20, 40, 60, 80, 100], [0, 0, 12.5, 25, 62.5, 100], BLEU, "Pays A", "haut")],
                  "Part cumulée des habitants", "Part cumulée du revenu total",
                  "Pays A : les 40 % les plus pauvres ont 12,5 % du revenu ; Gini = 0,40.")
    lorenz_simple("lorenz_bce.svg", [([0, 20, 40, 60, 80, 90, 100], [0, 4.35, 13.85, 28.64, 51.32, 67.93, 100], BLEU, "Revenu", "haut"),
                                     ([0, 20, 40, 60, 80, 90, 100], [0, 0, 2.32, 11.13, 30.69, 48.27, 100], ORANGE, "Patrimoine", "bas")],
                  "Part cumulée des ménages", "Part cumulée du total",
                  "Le patrimoine (Gini ≈ 0,66) est bien plus concentré que le revenu (Gini ≈ 0,42).")


if __name__ == "__main__":
    histogramme_incarceres()
    asymetrie()
    interpolation()
    cas_dispersion()
    boxplot_salaires()
    ibt()
    rentabilites()
    lorenz()
    gini_trapezes()
    schema_chapitre()
    histogramme_scolarises()
    lorenz_corriges()
