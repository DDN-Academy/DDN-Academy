#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Figures du cours n° 1 de Techniques statistiques — présenter pour informer.

    python3 Semestre1/Statistiques/Cours/figures/Ch01/figures_ch01.py

Écrit à côté de ce script :
  etapes.svg                les six étapes d'une étude statistique
  types_variables.svg       les deux types et les quatre sous-types de variables
  brute_distribution.svg    de la série brute au tableau de distribution
  freres_soeurs.svg         diagramme en colonnes : nombre de frères et sœurs de 87 étudiants
  familles_cumulees.svg     diagramme des fréquences cumulées (familles, 2008)
  ecroues_categorie.svg     colonnes groupées par catégorie (personnes écrouées, 2020-2023)
  ecroues_annee.svg         colonnes groupées par année (les mêmes données)
  familles_empile.svg       colonnes empilées : familles selon le nombre d'enfants mineurs (milliers)
  familles_cent.svg         colonnes empilées à 100 % : les mêmes données en fréquences
  bac_colonnes.svg          corrigé TD : âge d'obtention du bac (fréquences)
  lien_social_cumule.svg    corrigé TD : fréquences cumulées de la qualité du lien social
  schema_chapitre.svg       le schéma qui relie tout le chapitre (section 4.4)
Tous les graphiques sont à l'échelle ; les valeurs affichées sont celles du cours.
"""
import os
from xml.sax.saxutils import escape

ICI = os.path.dirname(os.path.abspath(__file__))
POLICE = "font-family=\"-apple-system,'Segoe UI',Helvetica,Arial,sans-serif\""
NOIR, GRIS, BLEU, ORANGE, VERT, ROUGE, VIOLET = "#1d2330", "#6b7280", "#1f4e79", "#b35c00", "#2e7d32", "#b3261e", "#6a3d9a"
F_BLEU, F_ORANGE, F_VERT, F_GRIS, F_ROUGE = "#e8eef6", "#fdf0e0", "#e6f2e7", "#f1f2f4", "#fbe9e7"
SERIES = ["#1f4e79", "#4f81bd", "#9dc3e6", "#c26a00", "#2e7d32", "#8c929c"]


def txt(x, y, s, taille=12, couleur=NOIR, ancre="middle", gras=False, italique=False, rot=None):
    """Texte ; les segments entre ** ** sont mis en gras."""
    st = (' font-weight="700"' if gras else "") + (' font-style="italic"' if italique else "")
    tr = ' transform="rotate(%s %.1f %.1f)"' % (rot, x, y) if rot is not None else ""
    morceaux = str(s).split("**")
    corps = "".join(('<tspan font-weight="700">%s</tspan>' % escape(m)) if k % 2 else escape(m)
                    for k, m in enumerate(morceaux) if m)
    return '<text x="%.1f" y="%.1f" font-size="%s" fill="%s" text-anchor="%s" %s%s%s>%s</text>' % (
        x, y, taille, couleur, ancre, POLICE, st, tr, corps)


def rect(x, y, w, h, fond, bord, r=8, trait=1.4, pointille=False):
    d = ' stroke-dasharray="5 4"' if pointille else ""
    return '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (
        x, y, w, h, r, fond, bord, trait, d)


def ligne(x1, y1, x2, y2, couleur=GRIS, trait=1.4, fleche=False, pointille=False):
    m = ' marker-end="url(#fl)"' if fleche else ""
    d = ' stroke-dasharray="5 4"' if pointille else ""
    return '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s%s/>' % (
        x1, y1, x2, y2, couleur, trait, m, d)


def chemin(d, couleur=GRIS, trait=1.4, fleche=False, pointille=False, fond="none"):
    m = ' marker-end="url(#fl)"' if fleche else ""
    p = ' stroke-dasharray="5 4"' if pointille else ""
    return '<path d="%s" fill="%s" stroke="%s" stroke-width="%s"%s%s/>' % (d, fond, couleur, trait, m, p)


def boite(x, y, w, h, titre, lignes, fond, bord, couleur_titre=None, taille=11.5, pas=15, taille_titre=13):
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
    """Nombre à la française : espace des milliers, virgule décimale, arrondi au plus proche."""
    from decimal import Decimal, ROUND_HALF_UP
    n = float(Decimal(str(n)).quantize(Decimal(1).scaleb(-dec), rounding=ROUND_HALF_UP))
    return ("{:,.%df}" % dec).format(n).replace(",", " ").replace(".", ",")


# ------------------------------------------------------------------ axes communs
def axes_colonnes(el, g, h, W, H, b, top, pas_grad, fmt, etiq_y):
    """Axe vertical gradué de 0 à top, grille légère ; renvoie la fonction Y."""
    Y = lambda v: H - b - v / top * (H - b - h)
    v = 0
    while v <= top + 1e-9:
        el.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#e3e6ea"/>' % (g, Y(v), W - 16, Y(v)))
        el.append(txt(g - 6, Y(v) + 4, fmt(v), 10, GRIS, "end"))
        v += pas_grad
    el.append(ligne(g, Y(0), W - 16, Y(0), NOIR, 1.3))
    el.append(ligne(g, Y(0), g, h - 6, NOIR, 1.3))
    if etiq_y:
        el.append(txt(g - 6, h - 12, etiq_y, 10.5, NOIR, "start", italique=True))
    return Y


def legende(el, x, y, noms, couleurs, W):
    for j, nom in enumerate(noms):
        el.append('<rect x="%.1f" y="%.1f" width="11" height="11" fill="%s"/>' % (x, y - 9, couleurs[j]))
        el.append(txt(x + 15, y, nom, 10.5, NOIR, "start"))
        x += 30 + 6.2 * len(nom)
        if x > W - 110 and j < len(noms) - 1:
            x, y = 64, y + 17


# ------------------------------------------------------------------ 1. les six étapes
def etapes():
    el = []
    W, H = 800, 238
    noms = [("1. Quel type de", "problématique ?"), ("2. Choix des", "données"),
            ("3. Méthode de", "recueil"), ("4. Campagne", "de mesures"),
            ("5. Traitement", "des données"), ("6. Prise de", "décision")]
    sous = [("pour quoi faire ?", ""), ("qui ? quelle", "population ?"), ("comment obtenir", "l'information ?"),
            ("combien, quand,", "comment ?"), ("présenter, résumer,", "évolutions, croiser"), ("le rapport informe,", "le décideur tranche")]
    w, h, y0, x0, gap = 116, 104, 20, 12, 15
    for k, (a, b) in enumerate(noms):
        x = x0 + k * (w + gap)
        fond, bord = (BLEU, BLEU) if k == 0 else (F_BLEU, BLEU)
        el.append(rect(x, y0, w, h, fond, bord))
        coul = "#ffffff" if k == 0 else BLEU
        el.append(txt(x + w / 2, y0 + 26, a, 12, coul, gras=True))
        el.append(txt(x + w / 2, y0 + 42, b, 12, coul, gras=True))
        el.append(ligne(x + 14, y0 + 54, x + w - 14, y0 + 54, "#ffffff" if k == 0 else "#c9d3e3", 1))
        for i, s in enumerate(sous[k]):
            if s:
                el.append(txt(x + w / 2, y0 + 72 + 15 * i, s, 10.5, "#ffffff" if k == 0 else GRIS, italique=True))
        if k < 5:
            el.append(ligne(x + w + 1, y0 + h / 2, x + w + gap - 1, y0 + h / 2, NOIR, 1.6, fleche=True))
    xs = [x0 + k * (w + gap) + w / 2 for k in range(1, 5)]
    base = y0 + h
    for x in xs:
        el.append(ligne(x, base, x, base + 30, ORANGE, 1.4))
    el.append(chemin("M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f" % (xs[-1], base + 30, x0 + w / 2, base + 30, x0 + w / 2, base + 3), ORANGE, 1.8, fleche=True))
    el.append(rect(250, base + 48, 300, 32, F_ORANGE, ORANGE))
    el.append(txt(400, base + 69, "Tous les choix sont guidés par la problématique", 12, ORANGE, gras=True))
    svg("etapes.svg", W, H, el)


# ------------------------------------------------------------------ 2. types de variables
def types_variables():
    el = []
    W, H = 720, 330
    el.append(rect(250, 14, 220, 46, BLEU, BLEU))
    el.append(txt(360, 36, "Variable statistique X", 13.5, "#ffffff", gras=True))
    el.append(txt(360, 52, "(ou caractère statistique)", 11, "#ffffff"))
    for (x, titre, s1, coul, fond) in [(70, "QUALITATIVE", "les modalités sont des mots", BLEU, F_BLEU),
                                         (430, "QUANTITATIVE", "les modalités sont des nombres", VERT, F_VERT)]:
        el.append(rect(x, 96, 220, 50, fond, coul))
        el.append(txt(x + 110, 118, titre, 13.5, coul, gras=True))
        el.append(txt(x + 110, 136, s1, 11, NOIR, italique=True))
        el.append(ligne(360, 60, x + 110, 94, GRIS, 1.4, fleche=True))
    feuilles = [(10, 70, "nominale", "aucun ordre qui ait un sens", "sexe, nationalité,", "couleur des yeux", BLEU, F_BLEU),
                (190, 70, "ordinale", "un ordre qui a un sens", "satisfaction, mention,", "échelle de 1 à 5", BLEU, F_BLEU),
                (370, 430, "discrète", "comptage (dénombrable)", "nombre d'enfants,", "nombre de langues", VERT, F_VERT),
                (550, 430, "continue", "mesure (non dénombrable)", "taille, poids,", "revenu, durée", VERT, F_VERT)]
    for x, xp, titre, crit, ex1, ex2, coul, fond in feuilles:
        el.append(rect(x, 196, 160, 118, "#ffffff", coul))
        el.append(txt(x + 80, 220, titre, 13, coul, gras=True))
        el.append(txt(x + 80, 242, crit, 10.5, NOIR))
        el.append(ligne(x + 18, 254, x + 142, 254, "#d8dce4", 1))
        el.append(txt(x + 80, 274, ex1, 10.5, GRIS, italique=True))
        el.append(txt(x + 80, 291, ex2, 10.5, GRIS, italique=True))
        el.append(ligne(xp + 110, 146, x + 80, 194, GRIS, 1.4, fleche=True))
    svg("types_variables.svg", W, H, el)


# ------------------------------------------------------------------ 3. de la série brute à la distribution
def brute_distribution():
    el = []
    W, H = 720, 250
    el += boite(14, 30, 200, 190, "Série brute", ["une ligne = un individu", "dans l'ordre du recueil", "", "2 · 2 · 5 · 2 · 3 · 1 · 1 …", "5 · 1 · 4 · 2 · 2 · 1 · 0 …", "N = 87 valeurs"], F_GRIS, GRIS, NOIR, 11.5, 19)
    el += boite(260, 30, 200, 190, "Série ordonnée", ["les mêmes valeurs,", "triées", "", "0  0  0 …  (11 fois)", "1  1  1 …  (33 fois)", "… jusqu'à 14"], F_BLEU, BLEU, BLEU, 11.5, 19)
    el += boite(506, 30, 200, 190, "Distribution", ["une ligne = une modalité", "avec son effectif", "", "0 → 11 · 1 → 33", "2 → 23 · 3 → 7 · …", "Ensemble : 87"], F_VERT, VERT, VERT, 11.5, 19)
    el.append(ligne(216, 125, 256, 125, NOIR, 1.6, fleche=True))
    el.append(txt(236, 112, "trier", 11, NOIR, gras=True))
    el.append(ligne(462, 125, 502, 125, NOIR, 1.6, fleche=True))
    el.append(txt(482, 112, "compter", 11, NOIR, gras=True))
    el.append(txt(360, 244, "Aucune information n'est perdue : on peut toujours revenir en arrière (sauf l'ordre du recueil).", 11, GRIS, italique=True))
    svg("brute_distribution.svg", W, H, el)


# ------------------------------------------------------------------ 4. frères et sœurs
def freres_soeurs():
    el = []
    W, H, g, h, b = 640, 330, 52, 34, 58
    eff = {0: 11, 1: 33, 2: 23, 3: 7, 4: 3, 5: 4, 6: 1, 7: 2, 8: 0, 9: 1, 10: 0, 11: 0, 12: 0, 13: 1, 14: 1}
    Y = axes_colonnes(el, g, h, W, H, b, 35, 5, lambda v: "%d" % v, "Effectif (nombre d'étudiants)")
    pas = (W - g - 16) / 15
    for k, x in enumerate(range(15)):
        x0 = g + k * pas + pas * 0.2
        v = eff[x]
        if v:
            el.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>' % (x0, Y(v), pas * 0.6, Y(0) - Y(v), BLEU))
            el.append(txt(x0 + pas * 0.3, Y(v) - 4, v, 10.5, NOIR))
        el.append(txt(g + k * pas + pas / 2, Y(0) + 15, x, 10.5, NOIR))
    el.append(txt((W + g) / 2, H - 22, "Nombre de frères et sœurs (modalités de X)", 11.5, NOIR, gras=True))
    el.append(txt((W + g) / 2, H - 6, "Une colonne par modalité ; les modalités 8, 10, 11 et 12 ont un effectif nul.", 10.5, GRIS, italique=True))
    svg("freres_soeurs.svg", W, H, el)


# ------------------------------------------------------------------ diagramme en escalier des fréquences cumulées
def escalier(nom, modalites, cumuls, titre_x, note, W=620, H=330):
    el = []
    g, h, b, d = 52, 34, 58, 16
    Y = axes_colonnes(el, g, h, W, H, b, 100, 20, lambda v: "%d %%" % v, "Fréquence cumulée F")
    n = len(modalites)
    pas = (W - g - d - 30) / (n + 0.5)
    X = lambda k: g + 30 + k * pas
    for k, (m, F) in enumerate(zip(modalites, cumuls)):
        x1 = X(k)
        x2 = X(k + 1) if k < n - 1 else X(k) + pas * 0.8
        el.append(ligne(x1, Y(F), x2, Y(F), BLEU, 2.6))
        el.append('<circle cx="%.1f" cy="%.1f" r="3.6" fill="%s"/>' % (x1, Y(F), BLEU))
        if k < n - 1:
            el.append('<circle cx="%.1f" cy="%.1f" r="3.6" fill="#ffffff" stroke="%s" stroke-width="1.6"/>' % (x2, Y(F), BLEU))
            el.append(ligne(x2, Y(F), x2, Y(cumuls[k + 1]), BLEU, 1, pointille=True))
        el.append(txt(x1 + 4, Y(F) - 7, fr(F, 2).rstrip("0").rstrip(",") + " %", 10.5, BLEU, "start", gras=True))
        el.append(ligne(x1, Y(0), x1, Y(0) + 4, NOIR, 1))
        el.append(txt(x1, Y(0) + 16, m, 10.5, NOIR))
    el.append(ligne(g, Y(0), X(0), Y(0), BLEU, 2.6))
    el.append(ligne(g, Y(50), W - d, Y(50), ROUGE, 1, pointille=True))
    el.append(txt(W - d - 2, Y(50) - 5, "50 %", 10.5, ROUGE, "end", gras=True))
    el.append(txt((W + g) / 2, H - 22, titre_x, 11.5, NOIR, gras=True))
    el.append(txt((W + g) / 2, H - 6, note, 10.5, GRIS, italique=True))
    svg(nom, W, H, el)


def familles_cumulees():
    escalier("familles_cumulees.svg", ["0", "1", "2", "3", "4 et +"], [48.0, 70.3, 90.4, 97.7, 100.0],
             "Nombre d'enfants — familles en France, 2008",
             "Lecture : F(1) = 70,3 % — 70,3 % des familles ont 1 enfant ou moins.")


# ------------------------------------------------------------------ colonnes groupées
def groupees(nom, categories, series, noms_series, etiq_y, top, pas_grad, note, W=660, H=350, valeurs=False):
    el = []
    g, h, b = 62, 40, 84
    Y = axes_colonnes(el, g, h, W, H, b, top, pas_grad, lambda v: fr(v), etiq_y)
    n, m = len(categories), len(series)
    pas = (W - g - 16) / n
    for k, cat in enumerate(categories):
        x0 = g + k * pas
        lb = pas * 0.76 / m
        for j in range(m):
            v = series[j][k]
            x = x0 + pas * 0.12 + j * lb
            el.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>' % (x, Y(v), lb - 2, Y(0) - Y(v), SERIES[j]))
            if valeurs:
                el.append(txt(x + (lb - 2) / 2, Y(v) - 4, fr(v), 9, NOIR))
        for i, morceau in enumerate(cat.split("\n")):
            el.append(txt(x0 + pas / 2, Y(0) + 15 + 13 * i, morceau, 10.5, NOIR))
    legende(el, g, H - 30, noms_series, SERIES, W)
    el.append(txt((W + g) / 2, H - 6, note, 10.5, GRIS, italique=True))
    svg(nom, W, H, el)


ECROUES = {"Prévenus détenus": [17692, 18486, 18779, 19755], "Condamnés-prévenus détenus": [2405, 2613, 2908, 3117],
           "Condamnés détenus": [41553, 47246, 49338, 51746], "Condamnés non détenus": [12184, 13644, 14286, 15453]}
ANNEES_E = ["2020", "2021", "2022", "2023"]


def ecroues_categorie():
    cats = ["Prévenus\ndétenus", "Condamnés-prévenus\ndétenus", "Condamnés\ndétenus", "Condamnés\nnon détenus"]
    series = [[ECROUES[c][a] for c in ECROUES] for a in range(4)]
    groupees("ecroues_categorie.svg", cats, series, ANNEES_E, "Personnes écrouées", 60000, 10000,
             "Groupement par catégorie : on lit l'évolution de chaque catégorie d'une année à l'autre.")


def ecroues_annee():
    series = [ECROUES[c] for c in ECROUES]
    groupees("ecroues_annee.svg", ANNEES_E, series, list(ECROUES), "Personnes écrouées", 60000, 10000,
             "Groupement par année : on lit la structure de chaque année, puis son évolution.")


# ------------------------------------------------------------------ colonnes empilées
FAM = {"1990": [3353.7, 2800.5, 1087.1, 410.9], "1999": [3418.3, 2841.1, 1033.5, 334.5], "2007": [3565.0, 2996.3, 1015.2, 296.9],
       "2012": [3614.8, 3074.1, 1022.3, 296.1], "2017": [3590.7, 3101.1, 1012.2, 310.7], "2023": [3578.3, 3039.0, 956.2, 308.4]}
TOT = {"1990": 7652.2, "1999": 7627.5, "2007": 7873.5, "2012": 8007.3, "2017": 8014.7, "2023": 7881.9}
NOMS_F = ["1 enfant", "2 enfants", "3 enfants", "4 enfants ou plus"]


def empilees(nom, cent, W=660, H=360):
    el = []
    g, h, b = 62, 40, 70
    top, pas_g = (100, 20) if cent else (9000, 1500)
    Y = axes_colonnes(el, g, h, W, H, b, top, pas_g, (lambda v: "%d %%" % v) if cent else (lambda v: fr(v)),
                      "Part des familles" if cent else "Familles (en milliers)")
    n = len(FAM)
    pas = (W - g - 16) / n
    for k, (an, vals) in enumerate(FAM.items()):
        x = g + k * pas + pas * 0.22
        lb = pas * 0.56
        cum = 0
        tot = TOT[an]
        for j, v in enumerate(vals):
            vv = v / tot * 100 if cent else v
            el.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" stroke="#ffffff" stroke-width="0.8"/>' % (x, Y(cum + vv), lb, Y(cum) - Y(cum + vv), SERIES[j]))
            if Y(cum) - Y(cum + vv) > 13:
                lab = fr(vv, 1) if cent else fr(v)
                el.append(txt(x + lb / 2, (Y(cum) + Y(cum + vv)) / 2 + 4, lab, 9.8, "#ffffff" if j < 1 or j == 3 else NOIR, gras=True))
            else:
                el.append(txt(x + lb + 4, (Y(cum) + Y(cum + vv)) / 2 + 3, fr(vv, 1) if cent else fr(v), 9, NOIR, "start"))
            cum += vv
        if not cent:
            el.append(txt(x + lb / 2, Y(cum) - 5, fr(tot, 1), 10, NOIR, gras=True))
        el.append(txt(x + lb / 2, Y(0) + 15, an, 10.5, NOIR))
    legende(el, g, H - 26, NOMS_F, SERIES, W)
    el.append(txt((W + g) / 2, H - 6, ("Chaque colonne vaut 100 % : on compare des structures." if cent else
                                        "La hauteur d'une colonne = le nombre total de familles de l'année (en gras)."), 10.5, GRIS, italique=True))
    svg(nom, W, H, el)


# ------------------------------------------------------------------ corrigés de TD
def bac_colonnes():
    el = []
    W, H, g, h, b = 660, 340, 52, 34, 70
    mods = ["< 18", "18", "19", "20", "21", "22", "23", "24", "25", "26 et +"]
    vals = [8.7, 68.3, 15.8, 3.8, 1.3, 0.7, 0.4, 0.2, 0.2, 1.2]
    Y = axes_colonnes(el, g, h, W, H, b, 70, 10, lambda v: "%d %%" % v, "Fréquence (en %)")
    pas = (W - g - 16) / len(mods)
    for k, (m, v) in enumerate(zip(mods, vals)):
        x = g + k * pas + pas * 0.18
        el.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>' % (x, Y(v), pas * 0.64, Y(0) - Y(v), BLEU))
        el.append(txt(x + pas * 0.32, Y(v) - 4, fr(v, 1), 10.5, NOIR))
        el.append(txt(g + k * pas + pas / 2, Y(0) + 15, m, 10.5, NOIR))
    el.append(txt((W + g) / 2, H - 38, "Âge d'obtention du bac (en années)", 11.5, NOIR, gras=True))
    el.append(txt((W + g) / 2, H - 22, "Étudiants en cours d'études au printemps 2020, répondants à l'enquête (n = 60 014)", 10.5, GRIS, italique=True))
    el.append(txt((W + g) / 2, H - 7, "Échelle : 1 cm pour 10 % en ordonnée. Source : OVE, Conditions de vie des étudiants 2020.", 10.5, GRIS, italique=True))
    svg("bac_colonnes.svg", W, H, el)


def lien_social_cumule():
    escalier("lien_social_cumule.svg", ["1", "2", "3", "4", "5"], [12.5, 25.0, 37.5, 68.75, 100.0],
             "Qualité du lien social (échelle de 1 à 5) — 16 salariés",
             "Lecture : F(3) = 37,5 % — 37,5 % des salariés jugent la qualité de leur lien social à 3 ou moins.")


# ------------------------------------------------------------------ schéma du chapitre
def schema_chapitre():
    el = []
    W, H = 760, 400
    el.append(rect(280, 14, 200, 52, BLEU, BLEU))
    el.append(txt(380, 36, "PRÉSENTER", 14, "#ffffff", gras=True))
    el.append(txt(380, 54, "sans perte d'information", 11, "#ffffff"))
    blocs = [
        (14, 100, 232, 128, "1. L'étude statistique", ["6 étapes, guidées par", "la problématique : problème,", "données, recueil, mesures,", "traitement, décision"], ORANGE, F_ORANGE),
        (264, 100, 232, 128, "2. Le vocabulaire", ["population · unité · N", "caractère X · modalités x", "quali. nominal / ordinal", "quanti. discret / continu"], BLEU, F_BLEU),
        (514, 100, 232, 128, "3. La distribution", ["série brute → trier → compter", "effectif n · fréquence f = n / N", "fréq. cumulée F = « ou moins »", "Σ n = N · Σ f = 1"], VERT, F_VERT),
    ]
    for x, y, w, hh, t, ls, c, f in blocs:
        el += boite(x, y, w, hh, t, ls, f, c, c, 11.5, 19)
        el.append(ligne(380, 66, x + w / 2, y - 2, GRIS, 1.4, fleche=True))
    el += boite(14, 262, 360, 124, "4. Représenter une distribution", ["colonnes ou barres (quali., quanti. discret)", "camembert : angle = f × 360°", "fréquences cumulées : diagramme en escalier", "une phrase de lecture sous chaque tableau"], F_BLEU, BLEU, BLEU, 11.5, 19)
    el += boite(392, 262, 354, 124, "5. Comparer des sous-populations", ["colonnes groupées : par catégorie", "(évolution) ou par année (structure)", "empilées : les totaux", "empilées à 100 % : les structures"], F_GRIS, NOIR, NOIR, 11.5, 19)
    el.append(ligne(630, 230, 569, 260, GRIS, 1.4, fleche=True))
    el.append(ligne(630, 230, 194, 260, GRIS, 1.4, fleche=True))
    svg("schema_chapitre.svg", W, H, el)


if __name__ == "__main__":
    etapes()
    types_variables()
    brute_distribution()
    freres_soeurs()
    familles_cumulees()
    ecroues_categorie()
    ecroues_annee()
    empilees("familles_empile.svg", False)
    empilees("familles_cent.svg", True)
    bac_colonnes()
    lien_social_cumule()
    schema_chapitre()
