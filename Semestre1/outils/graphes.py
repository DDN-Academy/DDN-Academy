#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
graphes.py — petits graphiques SVG sans dépendance, pour les cours.

Deux outils :
  Repere(...)   un repère cartésien : droites, courbes, points projetés, zones, flèches
  barres(...)   diagrammes en colonnes : simples, groupées, empilées, empilées à 100 %

Chaque script de figure d'un chapitre vit dans <Matiere>/Cours/figures/<chapitre>/
et écrit ses .svg à côté de lui ; le cours les appelle par « ![légende](figures/…/x.svg) ».
"""
from xml.sax.saxutils import escape

BLEU, ROUGE, VERT, ORANGE, GRIS, NOIR, VIOLET = "#1f4e79", "#b3261e", "#2e7d32", "#c26a00", "#8c929c", "#1d2330", "#6a3d9a"
PALETTE = [BLEU, ORANGE, VERT, ROUGE, VIOLET, "#00838f", "#8d6e63"]
POLICE = "font-family=\"-apple-system,'Segoe UI',Helvetica,Arial,sans-serif\""


def _t(x, y, txt, taille=12, couleur=NOIR, ancre="middle", gras=False, italique=False, rot=None):
    style = ' font-weight="600"' if gras else ""
    style += ' font-style="italic"' if italique else ""
    tr = ' transform="rotate(%s %.1f %.1f)"' % (rot, x, y) if rot is not None else ""
    return '<text x="%.1f" y="%.1f" font-size="%s" fill="%s" text-anchor="%s" %s%s%s>%s</text>' % (
        x, y, taille, couleur, ancre, POLICE, style, tr, escape(str(txt)))


class Repere:
    def __init__(self, xmin, xmax, ymin, ymax, largeur=520, hauteur=360, marges=(56, 24, 30, 48)):
        self.xmin, self.xmax, self.ymin, self.ymax = xmin, xmax, ymin, ymax
        self.W, self.H = largeur, hauteur
        self.g, self.h, self.b = marges[0], marges[1], marges[3]
        self.hh = marges[2]
        self.el = []

    def X(self, x):
        return self.g + (x - self.xmin) / (self.xmax - self.xmin) * (self.W - self.g - self.h)

    def Y(self, y):
        return self.H - self.b - (y - self.ymin) / (self.ymax - self.ymin) * (self.H - self.b - self.hh)

    def axes(self, etiq_x, etiq_y, graduations_x=(), graduations_y=(), origine="0"):
        x0, y0 = self.X(self.xmin), self.Y(self.ymin)
        self.el.append('<defs><marker id="fl" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="%s"/></marker></defs>' % NOIR)
        self.el.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.4" marker-end="url(#fl)"/>' % (x0, y0, self.W - self.h + 6, y0, NOIR))
        self.el.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.4" marker-end="url(#fl)"/>' % (x0, y0, x0, self.hh - 8, NOIR))
        self.el.append(_t(self.W - self.h + 4, y0 + 30, etiq_x, 12, NOIR, "end", italique=True))
        self.el.append(_t(x0 - 8, self.hh - 14, etiq_y, 12, NOIR, "start", italique=True))
        if origine:
            self.el.append(_t(x0 - 8, y0 + 14, origine, 11, GRIS, "end"))
        for v, lab in graduations_x:
            self.el.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s"/>' % (self.X(v), y0, self.X(v), y0 + 4, NOIR))
            self.el.append(_t(self.X(v), y0 + 16, lab, 11, NOIR))
        for v, lab in graduations_y:
            self.el.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s"/>' % (x0 - 4, self.Y(v), x0, self.Y(v), NOIR))
            self.el.append(_t(x0 - 7, self.Y(v) + 4, lab, 11, NOIR, "end"))
        return self

    def courbe(self, pts, couleur=BLEU, epaisseur=2.4, pointille=False, etiquette=None, pos="fin", decal=(6, -6)):
        d = " ".join("%s%.1f,%.1f" % ("M" if k == 0 else "L", self.X(x), self.Y(y)) for k, (x, y) in enumerate(pts))
        dash = ' stroke-dasharray="6 4"' if pointille else ""
        self.el.append('<path d="%s" fill="none" stroke="%s" stroke-width="%s"%s stroke-linecap="round"/>' % (d, couleur, epaisseur, dash))
        if etiquette:
            x, y = pts[-1] if pos == "fin" else pts[0]
            self.el.append(_t(self.X(x) + decal[0], self.Y(y) + decal[1], etiquette, 12, couleur, "start", gras=True))
        return self

    def droite(self, x1, y1, x2, y2, **kw):
        return self.courbe([(x1, y1), (x2, y2)], **kw)

    def point(self, x, y, etiquette=None, couleur=NOIR, decal=(8, -8), projeter=True, lab_x=None, lab_y=None):
        if projeter:
            for a in [('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-dasharray="3 3"/>' % (self.X(x), self.Y(y), self.X(x), self.Y(self.ymin), GRIS)),
                      ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-dasharray="3 3"/>' % (self.X(x), self.Y(y), self.X(self.xmin), self.Y(y), GRIS))]:
                self.el.append(a)
            if lab_x:
                self.el.append(_t(self.X(x), self.Y(self.ymin) + 16, lab_x, 11, NOIR))
            if lab_y:
                self.el.append(_t(self.X(self.xmin) - 7, self.Y(y) + 4, lab_y, 11, NOIR, "end"))
        self.el.append('<circle cx="%.1f" cy="%.1f" r="4" fill="%s"/>' % (self.X(x), self.Y(y), couleur))
        if etiquette:
            self.el.append(_t(self.X(x) + decal[0], self.Y(y) + decal[1], etiquette, 12, couleur, "start", gras=True))
        return self

    def zone(self, pts, couleur=BLEU, opacite=0.18, etiquette=None, ou=None):
        d = " ".join("%.1f,%.1f" % (self.X(x), self.Y(y)) for x, y in pts)
        self.el.append('<polygon points="%s" fill="%s" fill-opacity="%s" stroke="none"/>' % (d, couleur, opacite))
        if etiquette and ou:
            self.el.append(_t(self.X(ou[0]), self.Y(ou[1]), etiquette, 11, couleur, gras=True))
        return self

    def fleche(self, x1, y1, x2, y2, couleur=ROUGE, etiquette=None, decal=(0, -8)):
        self.el.append('<defs><marker id="f%s" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="%s"/></marker></defs>' % (couleur[1:], couleur))
        self.el.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2" marker-end="url(#f%s)"/>' % (self.X(x1), self.Y(y1), self.X(x2), self.Y(y2), couleur, couleur[1:]))
        if etiquette:
            self.el.append(_t((self.X(x1) + self.X(x2)) / 2 + decal[0], (self.Y(y1) + self.Y(y2)) / 2 + decal[1], etiquette, 11, couleur, gras=True))
        return self

    def texte(self, x, y, txt, couleur=NOIR, taille=12, ancre="middle", gras=False):
        self.el.append(_t(self.X(x), self.Y(y), txt, taille, couleur, ancre, gras))
        return self

    def svg(self, titre=None):
        t = _t(self.W / 2, 16, titre, 13, NOIR, gras=True) if titre else ""
        return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">%s%s</svg>' % (
            self.W, self.H, self.W, self.H, t, "".join(self.el))

    def enregistrer(self, chemin, titre=None):
        with open(chemin, "w", encoding="utf-8") as f:
            f.write(self.svg(titre))
        return chemin


def barres(chemin, categories, series, mode="simple", titre=None, etiq_y="", largeur=560, hauteur=340,
           valeurs=True, fmt="{:g}", legende=True, couleurs=None, ymax=None):
    """categories : libellés de l'axe horizontal ; series : liste de (nom, [valeurs]).
    mode : 'simple' (1 série), 'groupe', 'empile', 'cent' (empilé à 100 %)."""
    couleurs = couleurs or PALETTE
    g, d, h, b = 56, 16, 34 if titre else 16, 70 if legende and len(series) > 1 else 46
    _f = fmt if callable(fmt) else fmt.format
    W, H = largeur, hauteur
    n = len(categories)
    if mode == "cent":
        totaux = [sum(s[1][k] for s in series) for k in range(n)]
        series = [(nom, [v / totaux[k] * 100 for k, v in enumerate(vals)]) for nom, vals in series]
    if mode in ("empile", "cent"):
        haut = max(sum(s[1][k] for s in series) for k in range(n))
    else:
        haut = max(max(v) for _, v in series)
    top = ymax or (100 if mode == "cent" else haut * 1.12)
    Y = lambda v: H - b - v / top * (H - b - h)
    el = ['<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="1.3"/>' % (g, Y(0), W - d, Y(0), NOIR),
          '<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="1.3"/>' % (g, Y(0), g, h - 4, NOIR)]
    for k in range(5):
        v = top * k / 4
        el.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#e3e6ea"/>' % (g, Y(v), W - d, Y(v)))
        el.append(_t(g - 6, Y(v) + 4, _f(round(v, 1)) if mode != "cent" else "%d %%" % round(v), 10, GRIS, "end"))
    if etiq_y:
        el.append(_t(14, (H - b + h) / 2, etiq_y, 11, NOIR, rot=-90))
    pas = (W - g - d) / n
    for k, cat in enumerate(categories):
        x0 = g + k * pas
        if mode in ("simple", "groupe"):
            m = len(series)
            lb = pas * 0.72 / m
            for j, (nom, vals) in enumerate(series):
                v = vals[k]
                x = x0 + pas * 0.14 + j * lb
                el.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>' % (x, Y(v), lb - 2, Y(0) - Y(v), couleurs[j % len(couleurs)]))
                if valeurs:
                    el.append(_t(x + (lb - 2) / 2, Y(v) - 4, _f(v), 9.5 if m > 2 else 10.5, NOIR))
        else:
            cumul = 0
            lb = pas * 0.6
            x = x0 + pas * 0.2
            for j, (nom, vals) in enumerate(series):
                v = vals[k]
                el.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" stroke="#fff" stroke-width="0.8"/>' % (x, Y(cumul + v), lb, Y(cumul) - Y(cumul + v), couleurs[j % len(couleurs)]))
                if valeurs and (Y(cumul) - Y(cumul + v)) > 13:
                    el.append(_t(x + lb / 2, (Y(cumul) + Y(cumul + v)) / 2 + 4, _f(round(v, 1)), 10, "#ffffff", gras=True))
                cumul += v
        el.append(_t(x0 + pas / 2, Y(0) + 15, cat, 10.5, NOIR))
    if legende and len(series) > 1:
        x, y = g, H - 22
        for j, (nom, _) in enumerate(series):
            el.append('<rect x="%.1f" y="%.1f" width="11" height="11" fill="%s"/>' % (x, y - 9, couleurs[j % len(couleurs)]))
            el.append(_t(x + 15, y, nom, 10.5, NOIR, "start"))
            x += 22 + 6.4 * len(nom)
            if x > W - 120:
                x, y = g, y + 16
    t = _t(W / 2, 18, titre, 12.5, NOIR, gras=True) if titre else ""
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">%s%s</svg>' % (W, H, W, H, t, "".join(el))
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(svg)
    return chemin


class Schema:
    """Schéma de boîtes reliées par des flèches (coordonnées en pixels)."""

    def __init__(self, largeur=620, hauteur=360):
        self.W, self.H = largeur, hauteur
        self.b, self.el = {}, []

    def boite(self, nom, x, y, l, h, texte, couleur=BLEU, fond=None, taille=11.5, gras_premiere=True):
        fond = fond or "#ffffff"
        self.b[nom] = (x, y, l, h)
        self.el.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="7" fill="%s" stroke="%s" stroke-width="1.6"/>' % (x, y, l, h, fond, couleur))
        lignes = texte.split("\n")
        y0 = y + h / 2 - (len(lignes) - 1) * (taille + 3) / 2 + taille / 3
        for k, li in enumerate(lignes):
            self.el.append(_t(x + l / 2, y0 + k * (taille + 3), li, taille, couleur if k == 0 else NOIR, gras=(k == 0 and gras_premiere)))
        return self

    def _ancre(self, nom, cote):
        x, y, l, h = self.b[nom]
        return {"h": (x + l / 2, y), "b": (x + l / 2, y + h), "g": (x, y + h / 2), "d": (x + l, y + h / 2)}[cote]

    def fleche(self, a, ca, b, cb, couleur=GRIS, etiquette=None, courbe=0):
        x1, y1 = self._ancre(a, ca)
        x2, y2 = self._ancre(b, cb)
        mid = ""
        if courbe:
            mx, my = (x1 + x2) / 2 + courbe, (y1 + y2) / 2 - abs(courbe) / 2
            d = "M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (x1, y1, mx, my, x2, y2)
        else:
            d = "M%.1f,%.1f L%.1f,%.1f" % (x1, y1, x2, y2)
        self.el.append('<defs><marker id="s%s" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="%s"/></marker></defs>' % (couleur[1:], couleur))
        self.el.append('<path d="%s" fill="none" stroke="%s" stroke-width="1.8" marker-end="url(#s%s)"/>' % (d, couleur, couleur[1:]))
        if etiquette:
            self.el.append(_t((x1 + x2) / 2 + (courbe or 0) / 2, (y1 + y2) / 2 - 5, etiquette, 10.5, couleur, gras=True))
        return self

    def texte(self, x, y, txt, taille=11, couleur=NOIR, ancre="middle", gras=False, italique=False):
        self.el.append(_t(x, y, txt, taille, couleur, ancre, gras, italique))
        return self

    def enregistrer(self, chemin, titre=None):
        t = _t(self.W / 2, 18, titre, 13, NOIR, gras=True) if titre else ""
        with open(chemin, "w", encoding="utf-8") as f:
            f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">%s%s</svg>' % (self.W, self.H, self.W, self.H, t, "".join(self.el)))
        return chemin


def frise(chemin, debut, fin, periodes, evenements, largeur=640, hauteur=250, titre=None, pas=10):
    """Frise chronologique. periodes : [(a, b, libellé, couleur)] ; evenements : [(année, libellé, haut=True)]."""
    g, d = 30, 20
    W, H = largeur, hauteur
    yl = H / 2 + 10
    X = lambda a: g + (a - debut) / (fin - debut) * (W - g - d)
    el = ['<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="2"/>' % (g, yl, W - d, yl, NOIR)]
    for a in range(debut - debut % pas + pas, fin + 1, pas):
        el.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s"/>' % (X(a), yl - 4, X(a), yl + 4, NOIR))
        el.append(_t(X(a), yl + 17, a, 9.5, GRIS))
    for k, (a, b, lib, coul) in enumerate(periodes):
        yb = yl + 26 + (k % 2) * 30
        el.append('<rect x="%.1f" y="%.1f" width="%.1f" height="14" rx="3" fill="%s" fill-opacity="0.85"/>' % (X(a), yb, max(3, X(b) - X(a)), coul))
        el.append(_t((X(a) + X(b)) / 2, yb + 27, "%s (%d-%d)" % (lib, a, b), 10, coul, gras=True))
    hauts = [e for e in evenements if e[2]]
    for k, (a, lib, haut) in enumerate(evenements):
        niveau = hauts.index((a, lib, haut)) if haut else 0
        y2 = yl - 20 - niveau * 19 if haut else yl + 90
        el.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-dasharray="2 2"/>' % (X(a), yl, X(a), y2 + 3, GRIS))
        el.append('<circle cx="%.1f" cy="%.1f" r="3.5" fill="%s"/>' % (X(a), yl, ROUGE))
        a_droite = X(a) > W * 0.55
        el.append(_t(X(a) + (-5 if a_droite else 5), y2, "%d — %s" % (a, lib), 10, NOIR, "end" if a_droite else "start"))
    t = _t(W / 2, 16, titre, 12.5, NOIR, gras=True) if titre else ""
    with open(chemin, "w", encoding="utf-8") as f:
        f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">%s%s</svg>' % (W, H, W, H, t, "".join(el)))
    return chemin
