#!/usr/bin/env python3
# Figures du cours Statistiques Ch02 — lancer : python3 figures.py (écrit les .svg à côté)
import os, sys
ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ICI, "..", "..", "..", "..", "outils"))
from graphes import Repere, Schema, barres, _t, BLEU, ROUGE, VERT, ORANGE, GRIS, NOIR, VIOLET, PALETTE
F = lambda n: os.path.join(ICI, n)
virg = lambda v, d=1: ("%.*f" % (d, v)).replace(".", ",")
esp = lambda v: "{:,.0f}".format(v).replace(",", " ")

def rect(R, x0, x1, y, coul, op=0.85, contour="#ffffff"):
    R.el.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" fill-opacity="%s" stroke="%s" stroke-width="1"/>' % (
        R.X(x0), R.Y(y), R.X(x1) - R.X(x0), R.Y(0) - R.Y(y), coul, op, contour))

# 1. Logements en Outre-mer (diapositives 4 et 5) — une distribution par territoire
barres(F("logements.svg"), ["Guadeloupe", "Martinique", "Guyane", "La Réunion"],
       [("habitation de fortune", [1098, 790, 3698, 1867]), ("case traditionnelle", [2322, 578, 1798, 23062]),
        ("maison ou immeuble en bois", [8363, 6086, 11841, 12913]), ("maison ou immeuble en dur", [168050, 164290, 71089, 321445])],
       mode="groupe", etiq_y="nombre de logements", valeurs=False, fmt=esp, ymax=350000, largeur=620)

# 2-3. Personnes incarcérées en 2020 (diapositives 6 à 11) : le faux et le vrai histogramme
bornes = [16, 18, 21, 25, 30, 40, 50, 60, 80]
eff = [819, 5361, 11444, 14950, 23979, 13413, 6501, 3321]
N = sum(eff)
R = Repere(10, 85, 0, 26000, largeur=620, hauteur=300, marges=(64, 20, 26, 44))
R.axes("âge (ans)", "effectif", [(v, str(v)) for v in (16, 20, 30, 40, 50, 60, 80)], [(v, esp(v)) for v in (0, 5000, 10000, 15000, 20000, 25000)], origine="")
for k, e in enumerate(eff):
    rect(R, bornes[k], bornes[k + 1], e, ORANGE if k == 4 else GRIS, 0.75)
R.texte(35, 25000, "la classe 30-40 ans paraît modale… à tort", ORANGE, 11, gras=True)
R.texte(70, 6200, "classe de 20 ans : aire exagérée", GRIS, 10)
R.enregistrer(F("histogramme_faux.svg"))
R = Repere(10, 85, 0, 0.042, largeur=620, hauteur=300, marges=(64, 20, 26, 44))
R.axes("âge (ans)", "densité", [(v, str(v)) for v in (16, 20, 30, 40, 50, 60, 80)], [(v, virg(v, 2)) for v in (0, 0.01, 0.02, 0.03, 0.04)], origine="")
for k, e in enumerate(eff):
    d = e / N / (bornes[k + 1] - bornes[k])
    rect(R, bornes[k], bornes[k + 1], d, ROUGE if k == 3 else BLEU, 0.8)
    R.texte((bornes[k] + bornes[k + 1]) / 2, d + 0.0012, virg(d, 4), NOIR, 9)
R.texte(52, 0.037, "classe modale : 25-30 ans (densité 0,0375)", ROUGE, 11, gras=True)
R.enregistrer(F("histogramme.svg"))

# 4. Les quatre cas de la diapositive 27 : même moyenne (12), dispersions différentes
cas = [("Cas 1", {12: 50}), ("Cas 2", {v: 5 for v in (7, 8, 9, 10, 11, 13, 14, 15, 16, 17)}),
       ("Cas 3", {6: 20, 12: 10, 18: 20}), ("Cas 4", {4: 5, 8: 10, 10: 10, 14: 10, 16: 10, 20: 5})]
W, H = 640, 420
el = []
for k, (nom, dist) in enumerate(cas):
    ox, oy = 20 + (k % 2) * 315, 20 + (k // 2) * 200
    R = Repere(0, 20, 0, 50, largeur=300, hauteur=180, marges=(38, 10, 24, 30))
    R.axes("note", "élèves", [(v, str(v)) for v in (0, 4, 8, 12, 16, 20)], [(v, str(v)) for v in (25, 50)], origine="")
    for v, n in dist.items():
        R.el.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>' % (R.X(v - 0.35), R.Y(n), R.X(0.7) - R.X(0), R.Y(0) - R.Y(n), BLEU))
    R.el.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.6" stroke-dasharray="4 3"/>' % (R.X(12), R.Y(0), R.X(12), R.Y(50), ROUGE))
    R.el.append(_t(R.X(20), 30, nom, 12, NOIR, "end", gras=True))
    el.append('<g transform="translate(%d,%d)">%s</g>' % (ox, oy, "".join(R.el)))
el.append(_t(W / 2, H - 4, "trait rouge : la moyenne, 12/20 dans les quatre cas", 11, ROUGE, italique=True))
open(F("quatre_cas.svg"), "w", encoding="utf-8").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">%s</svg>' % (W, H, W, H, "".join(el)))

# 5. Niveau de vie 2024 (diapositive 34) : les déciles sur un axe — l'écartement vers le haut
R = Repere(10000, 65000, 0, 1, largeur=640, hauteur=170, marges=(20, 20, 20, 44))
R.el.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.4"/>' % (R.X(10000), R.Y(0.3), R.X(65000), R.Y(0.3), NOIR))
q = [("D1", 13970), ("D2", 17700), ("D3", 20980), ("D4", 23880), ("D5", 26740), ("D6", 29880), ("D7", 33680), ("D8", 38780), ("D9", 48580), ("C95", 61220)]
for k, (nom, v) in enumerate(q):
    c = ROUGE if nom == "D5" else BLEU
    R.el.append('<circle cx="%.1f" cy="%.1f" r="4.5" fill="%s"/>' % (R.X(v), R.Y(0.3), c))
    R.el.append(_t(R.X(v), R.Y(0.3) - 12 - (k % 2) * 14, nom, 10.5, c, gras=True))
    R.el.append(_t(R.X(v), R.Y(0.3) + 16 + (k % 2) * 13, esp(v), 9, NOIR))
R.el.append(_t(R.X(37500), R.Y(0.95), "niveau de vie en € par UC — les déciles se resserrent au centre puis s'écartent vers le haut", 10.5, GRIS, italique=True))
R.enregistrer(F("niveau_de_vie.svg"))

# 6. Boîtes à moustaches par CSP (diapositive 38) — moustaches aux déciles D1 et D9
csp = [("Ensemble", 1440, 1660, 2090, 2880, 4160), ("Cadres", 2240, 2810, 3620, 4930, 7060), ("Prof. intermédiaires", 1640, 1940, 2360, 2890, 3590),
       ("Employés", 1380, 1510, 1730, 2060, 2520), ("Ouvriers", 1380, 1570, 1830, 2200, 2630)]
W, H = 640, 300
g, d = 150, 20
X = lambda v: g + (v - 1000) / (7500 - 1000) * (W - g - d)
el = []
for k, (nom, d1, q1, me, q3, d9) in enumerate(csp):
    y = 30 + k * 48
    c = ROUGE if k == 0 else BLEU
    el.append(_t(g - 10, y + 5, nom, 11.5, c, "end", gras=True))
    el.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="1.4"/>' % (X(d1), y, X(q1), y, c))
    el.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="1.4"/>' % (X(q3), y, X(d9), y, c))
    for v in (d1, d9):
        el.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="1.4"/>' % (X(v), y - 8, X(v), y + 8, c))
    el.append('<rect x="%.1f" y="%d" width="%.1f" height="24" fill="%s" fill-opacity="0.15" stroke="%s" stroke-width="1.5"/>' % (X(q1), y - 12, X(q3) - X(q1), c, c))
    el.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="2.6"/>' % (X(me), y - 12, X(me), y + 12, c))
yb = 30 + 5 * 48 - 10
el.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s"/>' % (g, yb, W - d, yb, NOIR))
for v in range(1000, 7501, 1000):
    el.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s"/>' % (X(v), yb, X(v), yb + 4, NOIR))
    el.append(_t(X(v), yb + 16, esp(v), 10, NOIR))
el.append(_t((g + W - d) / 2, yb + 34, "salaire mensuel net (€) — boîte : Q1 à Q3 · trait : médiane · moustaches : D1 et D9", 10.5, GRIS, italique=True))
open(F("boxplot_csp.svg"), "w", encoding="utf-8").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">%s</svg>' % (W, H, W, H + 10, "".join(el)))

# 7. Le schéma du boxplot (diapositive 37)
W, H = 620, 170
X = lambda v: 40 + (v - 25) / (85 - 25) * (W - 80)
q1, me, q3 = 45, 52, 60
iqr = q3 - q1
el = ['<line x1="%.1f" y1="80" x2="%.1f" y2="80" stroke="%s" stroke-width="1.5"/>' % (X(33), X(q1), BLEU),
      '<line x1="%.1f" y1="80" x2="%.1f" y2="80" stroke="%s" stroke-width="1.5"/>' % (X(q3), X(70), BLEU),
      '<line x1="%.1f" y1="70" x2="%.1f" y2="90" stroke="%s" stroke-width="1.5"/>' % (X(33), X(33), BLEU),
      '<line x1="%.1f" y1="70" x2="%.1f" y2="90" stroke="%s" stroke-width="1.5"/>' % (X(70), X(70), BLEU),
      '<rect x="%.1f" y="62" width="%.1f" height="36" fill="%s" fill-opacity="0.15" stroke="%s" stroke-width="1.6"/>' % (X(q1), X(q3) - X(q1), BLEU, BLEU),
      '<line x1="%.1f" y1="62" x2="%.1f" y2="98" stroke="%s" stroke-width="2.8"/>' % (X(me), X(me), ROUGE),
      '<circle cx="%.1f" cy="80" r="4.5" fill="none" stroke="%s" stroke-width="1.8"/>' % (X(80), ROUGE)]
el += [_t(X(q1), 56, "Q1", 11, BLEU, gras=True), _t(X(me), 56, "Mé", 11, ROUGE, gras=True), _t(X(q3), 56, "Q3", 11, BLEU, gras=True),
       _t(X(80), 66, "valeur atypique", 10, ROUGE, gras=True), _t((X(q1) + X(q3)) / 2, 116, "IQR = Q3 − Q1", 10.5, BLEU),
       _t(X(61), 106, "moustache : jusqu'à 1,5 × IQR au plus", 9.5, GRIS, "start"),
       '<line x1="40" y1="140" x2="%d" y2="140" stroke="%s"/>' % (W - 40, NOIR)]
for v in range(30, 81, 10):
    el += ['<line x1="%.1f" y1="140" x2="%.1f" y2="144" stroke="%s"/>' % (X(v), X(v), NOIR), _t(X(v), 157, str(v), 10, NOIR)]
open(F("boxplot_schema.svg"), "w", encoding="utf-8").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">%s</svg>' % (W, H, W, H, "".join(el)))

# 8. Volatilité par période (diapositive 48) — la période 2 a une rentabilité moyenne négative
per = ["23/05-21/06", "22/06-23/07", "24/07-22/08", "23/08-21/09", "ensemble"]
mo = [0.372, -0.307, 1.244, 0.587, 0.474]; vo = [2.555, 3.374, 3.128, 1.954, 2.861]
R = Repere(0, 5, -0.8, 4, largeur=620, hauteur=320, marges=(56, 16, 20, 64))
for v in (-0.5, 0, 1, 2, 3, 4):
    R.el.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s"/>' % (R.X(0), R.Y(v), R.X(5), R.Y(v), NOIR if v == 0 else "#e3e6ea"))
    R.el.append(_t(R.X(0) - 6, R.Y(v) + 4, virg(v, 1) + " %", 10, GRIS, "end"))
for k in range(5):
    for j, (val, coul) in enumerate([(mo[k], VERT), (vo[k], ROUGE)]):
        x0 = k + 0.18 + j * 0.32
        y0, y1 = (0, val) if val >= 0 else (val, 0)
        R.el.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>' % (R.X(x0), R.Y(y1), R.X(x0 + 0.3) - R.X(x0), R.Y(y0) - R.Y(y1), coul))
        R.el.append(_t(R.X(x0 + 0.15), (R.Y(val) - 5) if val >= 0 else (R.Y(val) + 13), virg(val, 3), 9.5, coul, gras=True))
    R.el.append(_t(R.X(k + 0.5), R.Y(-0.8) + 14, per[k], 10.5, NOIR))
R.el.append('<rect x="60" y="%d" width="11" height="11" fill="%s"/>' % (320 - 28, VERT)); R.el.append(_t(75, 320 - 19, "rentabilité journalière moyenne (%)", 10.5, NOIR, "start"))
R.el.append('<rect x="330" y="%d" width="11" height="11" fill="%s"/>' % (320 - 28, ROUGE)); R.el.append(_t(345, 320 - 19, "volatilité = écart-type des rentabilités (%)", 10.5, NOIR, "start"))
R.enregistrer(F("volatilite.svg"))

# 9. Translation et dilatation (propriétés de la variance, diapositives 50 à 52) — illustrées sur le cas 4
dist = {4: 5, 8: 10, 10: 10, 14: 10, 16: 10, 20: 5}
W, H = 640, 330
el = []
for k, (nom, f, coul) in enumerate([("X (cas 4) : m = 12, σ = 4,56", lambda v: v, BLEU), ("X + 6 : m = 18, σ = 4,56 (inchangé)", lambda v: v + 6, VERT),
                                     ("2X : m = 24, σ = 9,12 (doublé)", lambda v: 2 * v, ORANGE)]):
    R = Repere(0, 42, 0, 12, largeur=640, hauteur=105, marges=(50, 16, 16, 26))
    R.axes("", "", [(v, str(v)) for v in range(0, 43, 6)] if k == 2 else [], [], origine="")
    for v, n in dist.items():
        x = f(v)
        R.el.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>' % (R.X(x - 0.35), R.Y(n), R.X(0.7) - R.X(0), R.Y(0) - R.Y(n), coul))
    m = f(12)
    R.el.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.6" stroke-dasharray="4 3"/>' % (R.X(m), R.Y(0), R.X(m), R.Y(12), ROUGE))
    R.el.append(_t(R.X(42), 22, nom, 11, coul, "end", gras=True))
    el.append('<g transform="translate(0,%d)">%s</g>' % (k * 105, "".join(R.el)))
open(F("translation_dilatation.svg"), "w", encoding="utf-8").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">%s</svg>' % (W, H, W, H, "".join(el)))

# 10. Parts de la masse salariale par quintile, 2005 et 2021 (diapositives 61 à 63)
barres(F("parts_quintiles.svg"), ["1er quintile", "2e", "3e", "4e", "5e quintile"],
       [("2005", [11.2, 13.3, 16.2, 21.1, 38.2]), ("2021", [3.9, 10.6, 18.4, 26.7, 40.5])],
       mode="groupe", etiq_y="% de la masse salariale", fmt=lambda v: virg(v), ymax=45, largeur=600, couleurs=[BLEU, ROUGE])

# 11. Courbes de Lorenz 2005 et 2021, avec la diagonale (diapositive 66)
def lorenz(chemin, courbes, titre_x="part cumulée des salariés (%)", titre_y="part cumulée de la masse salariale (%)", trapezes=None):
    R = Repere(0, 100, 0, 100, largeur=460, hauteur=440, marges=(56, 24, 26, 48))
    R.axes(titre_x, titre_y, [(v, str(v)) for v in range(0, 101, 20)], [(v, str(v)) for v in range(20, 101, 20)], origine="")
    for v in range(20, 101, 20):
        R.el.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#e3e6ea"/>' % (R.X(0), R.Y(v), R.X(100), R.Y(v)))
    if trapezes:
        pts, coul = trapezes
        for k in range(len(pts) - 1):
            (x0, y0), (x1, y1) = pts[k], pts[k + 1]
            R.zone([(x0, 0), (x0, y0), (x1, y1), (x1, 0)], coul, 0.10 + 0.07 * (k % 2))
        R.zone([(0, 0)] + pts + [(100, 100)], ROUGE, 0.0)
        R.zone([(0, 0), (100, 100)] + list(reversed(pts)), ROUGE, 0.22, "aire de concentration", (57, 49))
        R.texte(70, 22, "trapèze : (40,7 + 61,8) × 20 / 2 = 1 025", NOIR, 10)
    R.droite(0, 0, 100, 100, couleur=GRIS, epaisseur=1.8, pointille=True)
    R.texte(80, 90, "égalité parfaite", GRIS, 10.5)
    for pts, coul, nom, dec in courbes:
        R.courbe(pts, couleur=coul, epaisseur=2.4)
        for x, y in pts[1:-1]:
            R.el.append('<circle cx="%.1f" cy="%.1f" r="3.5" fill="%s"/>' % (R.X(x), R.Y(y), coul))
        R.texte(dec[0], dec[1], nom, coul, 11.5, gras=True) if dec[0] > 20 else R.el.append(_t(R.X(dec[0]), R.Y(dec[1]), nom, 11.5, coul, "start", gras=True))
    R.enregistrer(chemin)
L05 = [(0, 0), (20, 11.2), (40, 24.5), (60, 40.7), (80, 61.8), (100, 100)]
L21 = [(0, 0), (20, 3.9), (40, 14.5), (60, 32.9), (80, 59.6), (100, 100)]
lorenz(F("lorenz.svg"), [(L05, BLEU, "2005", (43, 36)), (L21, ROUGE, "2021", (70, 42))])
lorenz(F("gini_trapezes.svg"), [(L05, BLEU, "Lorenz 2005", (30, 6))], trapezes=(L05, BLEU))
# 12. Deux courbes qui se croisent (pays A et B du contre-exemple)
lorenz(F("lorenz_croisement.svg"), [([(0, 0), (20, 4), (40, 16), (60, 36), (80, 64), (100, 100)], BLEU, "pays A", (18, 92)),
                                    ([(0, 0), (20, 8), (40, 18), (60, 33), (80, 55), (100, 100)], ORANGE, "pays B", (18, 84))],
       titre_x="part cumulée de la population (%)", titre_y="part cumulée du revenu (%)")
print("figures écrites")
