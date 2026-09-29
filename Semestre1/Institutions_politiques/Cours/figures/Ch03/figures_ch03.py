#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Figures du cours n° 3 d'Institutions politiques — la constitution.

    python3 Semestre1/Institutions_politiques/Cours/figures/Ch03/figures_ch03.py

Écrit à côté de ce script :
  hierarchie_normes.svg   la pyramide des normes en France et les deux contrôles
  deux_pouvoirs.svg       pouvoir constituant originaire et pouvoir constituant dérivé
  article89.svg           la procédure de révision de l'article 89
  qpc.svg                 la question prioritaire de constitutionnalité, du procès à l'abrogation
  deux_modeles.svg        les deux modèles de justice constitutionnelle, sur quatre critères
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


def poly(points, fond, bord, trait=1.4):
    pts = " ".join("%.1f,%.1f" % p for p in points)
    return '<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s"/>' % (pts, fond, bord, trait)


def cercle(x, y, r, fond, bord, trait=1.4):
    return '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%s"/>' % (x, y, r, fond, bord, trait)


def boite(x, y, w, h, titre, lignes, fond, bord, couleur_titre=None, taille=11.5, pas=15, t_titre=13):
    el = [rect(x, y, w, h, fond, bord)]
    el.append(txt(x + w / 2, y + 22, titre, t_titre, couleur_titre or bord, gras=True))
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


# ------------------------------------------------------------------ 1. la hiérarchie des normes
def hierarchie_normes():
    el = []
    W = 700
    cx, haut, h = 300, 14, 58          # sommet de la pyramide, hauteur d'un étage
    niveaux = [
        ("CONSTITUTION", "et bloc de constitutionnalité", F_BLEU, BLEU),
        ("TRAITÉS", "au-dessus des lois (art. 55)", F_VERT, VERT),
        ("LOIS", "votées par le Parlement", F_ORANGE, ORANGE),
        ("RÈGLEMENTS", "décrets, arrêtés", F_GRIS, GRIS),
        ("ACTES INDIVIDUELS", "décisions administratives", "#ffffff", GRIS),
    ]
    demi = lambda y: 38 + (y - haut) * 0.86          # demi-largeur de la pyramide à la hauteur y
    for k, (t1, t2, fo, bo) in enumerate(niveaux):
        y0, y1 = haut + k * h, haut + (k + 1) * h
        el.append(poly([(cx - demi(y0), y0), (cx + demi(y0), y0), (cx + demi(y1), y1), (cx - demi(y1), y1)], fo, bo))
        el.append(txt(cx, y0 + 26, t1, 12.5, bo if bo != GRIS else NOIR, gras=True))
        el.append(txt(cx, y0 + 43, t2, 10.5, NOIR, italique=True))
    # les contrôles, à droite
    xd = 560
    for y, l1, l2, c in ((haut + h * 1.5, "contrôle de constitutionnalité", "le Conseil constitutionnel", BLEU),
                         (haut + h * 3, "contrôle de légalité", "le juge administratif", ORANGE)):
        el.append(ligne(xd - 70, y + 34, xd - 70, y - 30, c, 1.8, fleche=True))
        el.append(txt(xd - 58, y - 2, l1, 11.5, c, "start", gras=True))
        el.append(txt(xd - 58, y + 14, l2, 11, NOIR, "start"))
    el.append(txt(xd - 58, haut + h * 1.5 + 30, "(art. 54 pour les traités)", 10.5, GRIS, "start", italique=True))
    # la règle, à gauche
    el.append(txt(20, 150, "Chaque norme doit", 11.5, NOIR, "start"))
    el.append(txt(20, 166, "respecter la norme", 11.5, NOIR, "start"))
    el.append(txt(20, 182, "**supérieure**", 11.5, NOIR, "start"))
    el.append(txt(20, 202, "(Kelsen)", 11, GRIS, "start", italique=True))
    el.append(txt(W / 2, haut + 5 * h + 26, "Bloc de constitutionnalité : la Constitution de 1958 et son Préambule — Déclaration de 1789, Préambule de 1946, Charte de 2004",
                  10.5, GRIS, italique=True))
    svg("hierarchie_normes.svg", W, haut + 5 * h + 36, el)


# ------------------------------------------------------------------ 2. les deux pouvoirs constituants
def deux_pouvoirs():
    el = []
    W = 700
    x0, xl, xr, wl = 10, 150, 430, 270
    el.append(rect(xl, 8, wl, 34, F_ORANGE, ORANGE, r=6))
    el.append(txt(xl + wl / 2, 30, "POUVOIR CONSTITUANT ORIGINAIRE", 12.5, ORANGE, gras=True))
    el.append(rect(xr, 8, wl, 34, F_BLEU, BLEU, r=6))
    el.append(txt(xr + wl / 2, 30, "POUVOIR CONSTITUANT DÉRIVÉ", 12.5, BLEU, gras=True))
    lignes = [
        ("Ce qu'il fait", ["**établir** une constitution", "nouvelle"], ["**réviser** la constitution", "en vigueur"]),
        ("Quand ?", ["révolution · guerre · effondrement", "d'un régime · naissance d'un État"], ["pour **adapter** la constitution", "à l'évolution de la société"]),
        ("Comment ?", ["**librement** : octroi, pacte,", "assemblée constituante, référendum"], ["selon la **procédure prévue** :", "en France, l'**article 89**"]),
        ("Limites ?", ["**aucune** :", "il est inconditionné"], ["**procédure**, **temps** (al. 4, art. 7),", "**fond** (al. 5 : forme républicaine)"]),
        ("En France", ["1791 · 1814 · 1830 · 1848 ·", "1875 · 1946 · **1958**"], ["**25 révisions** depuis 1958 :", "2000, 2008, 2024…"]),
    ]
    for k, (lab, g, d) in enumerate(lignes):
        y = 50 + k * 54
        el.append(rect(x0, y, 132, 46, F_GRIS, GRIS, r=6, trait=1))
        el.append(txt(x0 + 66, y + 28, lab, 12, NOIR, gras=True))
        for x, l in ((xl, g), (xr, d)):
            el.append(rect(x, y, wl, 46, "#ffffff", GRIS, r=6, trait=0.8))
            for j, s in enumerate(l):
                el.append(txt(x + wl / 2, y + 19 + j * 16, s, 11.5))
    svg("deux_pouvoirs.svg", W, 50 + 5 * 54 + 4, el)


# ------------------------------------------------------------------ 3. l'article 89
def article89():
    el = []
    W = 700
    el += boite(40, 8, 290, 62, "PROJET de révision", ["le **Président**, sur proposition", "du **Premier ministre**"], F_BLEU, BLEU, pas=16)
    el += boite(370, 8, 290, 62, "PROPOSITION de révision", ["des **membres du Parlement**", "(députés ou sénateurs)"], F_ORANGE, ORANGE, pas=16)
    el.append(txt(W / 2, 90, "① L'INITIATIVE (al. 1)", 11, GRIS, italique=True))
    el.append(ligne(185, 70, 300, 104, GRIS, 1.4, fleche=True))
    el.append(ligne(515, 70, 400, 104, GRIS, 1.4, fleche=True))
    el += boite(130, 106, 440, 62, "VOTE DES DEUX ASSEMBLÉES EN TERMES IDENTIQUES", ["Assemblée nationale et Sénat : le même texte, mot pour mot —", "chacune peut bloquer la révision (al. 2)"], F_GRIS, NOIR, pas=16)
    el.append(txt(W / 2, 188, "② LE VOTE", 11, GRIS, italique=True))
    # deux voies d'approbation
    el.append(ligne(260, 168, 175, 208, BLEU, 1.6, fleche=True))
    el.append(ligne(440, 168, 525, 208, GRIS, 1.6, fleche=True))
    el.append(txt(30, 190, "projet seulement, si le", 10.5, BLEU, "start", italique=True))
    el.append(txt(30, 203, "Président le décide", 10.5, BLEU, "start", italique=True))
    el += boite(40, 212, 270, 72, "CONGRÈS (al. 3)", ["le Parlement réuni à Versailles :", "**3/5 des suffrages exprimés**"], F_BLEU, BLEU, pas=17)
    el += boite(390, 212, 270, 72, "RÉFÉRENDUM (al. 2)", ["le principe — et obligatoire", "pour une **proposition**"], F_VERT, VERT, pas=17)
    el.append(txt(W / 2, 304, "③ L'APPROBATION", 11, GRIS, italique=True))
    el.append(ligne(175, 284, 300, 320, GRIS, 1.4, fleche=True))
    el.append(ligne(525, 284, 400, 320, GRIS, 1.4, fleche=True))
    el.append(rect(230, 322, 240, 34, "#ffffff", NOIR, r=8, trait=1.8))
    el.append(txt(W / 2, 344, "RÉVISION DÉFINITIVE", 13, NOIR, gras=True))
    el.append(rect(40, 370, 620, 40, F_ROUGE, ROUGE, r=6, trait=1.2))
    el.append(txt(W / 2, 386, "**Jamais** quand l'intégrité du territoire est atteinte (al. 4) ni pendant l'intérim de la présidence (art. 7) ;", 11, ROUGE))
    el.append(txt(W / 2, 402, "**jamais** contre la forme républicaine du Gouvernement (al. 5)", 11, ROUGE))
    svg("article89.svg", W, 416, el)


# ------------------------------------------------------------------ 4. la QPC
def qpc():
    el = []
    W = 700
    el += boite(110, 8, 480, 62, "UN PROCÈS EN COURS", ["une partie soutient qu'une **loi** porte atteinte", "aux **droits et libertés** que la Constitution garantit"], F_GRIS, NOIR, pas=16)
    el.append(ligne(350, 70, 350, 92, GRIS, 1.4, fleche=True))
    el += boite(110, 94, 480, 98, "LE JUGE DU PROCÈS — 1er filtre", ["la loi est **applicable au litige** ;", "elle n'a **pas déjà été jugée conforme** ;", "la question n'est **pas dépourvue de sérieux**", "→ il transmet sans délai"], F_ORANGE, ORANGE, pas=15)
    el.append(ligne(270, 192, 190, 220, GRIS, 1.4, fleche=True))
    el.append(ligne(430, 192, 510, 220, GRIS, 1.4, fleche=True))
    for x, t, o in ((40, "CONSEIL D'ÉTAT", "ordre administratif"), (370, "COUR DE CASSATION", "ordre judiciaire")):
        el += boite(x, 222, 290, 68, t, ["%s — 2e filtre" % o, "**3 mois** : question **nouvelle** ou **sérieuse** ?"], F_ORANGE, ORANGE, taille=11, pas=16)
    el.append(ligne(185, 290, 300, 322, GRIS, 1.4, fleche=True))
    el.append(ligne(515, 290, 400, 322, GRIS, 1.4, fleche=True))
    el += boite(170, 324, 360, 50, "CONSEIL CONSTITUTIONNEL", ["**3 mois** pour statuer (art. 61-1)"], F_BLEU, BLEU, pas=15)
    el.append(ligne(270, 374, 200, 400, GRIS, 1.4, fleche=True))
    el.append(ligne(430, 374, 500, 400, GRIS, 1.4, fleche=True))
    el += boite(40, 402, 300, 50, "CONFORME", ["la loi continue de s'appliquer"], F_VERT, VERT, pas=15)
    el += boite(360, 402, 300, 50, "NON CONFORME : ABROGATION", ["immédiate ou différée, **pour tous** (art. 62)"], F_ROUGE, ROUGE, pas=15)
    svg("qpc.svg", W, 460, el)


# ------------------------------------------------------------------ 5. les deux modèles
def deux_modeles():
    el = []
    W = 700
    xa, xb = 250, 530                   # extrémités de chaque axe
    # légende
    el.append(cercle(40, 20, 7, F_ORANGE, ORANGE, 1.8))
    el.append(txt(54, 25, "modèle américain", 11.5, ORANGE, "start", gras=True))
    el.append(rect(213, 13, 14, 14, F_BLEU, BLEU, r=2, trait=1.8))
    el.append(txt(234, 25, "modèle européen", 11.5, BLEU, "start", gras=True))
    el.append(rect(380, 16, 26, 8, F_VERT, VERT, r=3, trait=1.4))
    el.append(txt(414, 25, "France depuis la QPC (2010)", 11.5, VERT, "start", gras=True))
    criteres = [
        ("L'ORGANE", "qui contrôle ?", "diffus", "tous les juges", "concentré", "une seule cour", "droite"),
        ("LE MOMENT", "quand ?", "a posteriori", "loi en vigueur", "a priori", "avant l'entrée en vigueur", "les deux"),
        ("LA NATURE", "comment ?", "concret", "dans un procès", "abstrait", "la loi en elle-même", "droite"),
        ("L'EFFET", "pour qui ?", "relatif", "les parties", "absolu", "tout le monde", "droite"),
    ]
    for k, (nom, q, g, g2, d, d2, fr) in enumerate(criteres):
        y = 70 + k * 62
        el.append(txt(20, y + 4, nom, 12, NOIR, "start", gras=True))
        el.append(txt(20, y + 20, q, 10.5, GRIS, "start", italique=True))
        el.append(ligne(xa, y, xb, y, GRIS, 1.6))
        el.append(txt(xa - 12, y + 4, g, 12, ORANGE, "end", gras=True))
        el.append(txt(xa - 12, y + 19, g2, 10, GRIS, "end", italique=True))
        el.append(txt(xb + 12, y + 4, d, 12, BLEU, "start", gras=True))
        el.append(txt(xb + 12, y + 19, d2, 10, GRIS, "start", italique=True))
        # repère France (QPC)
        if fr == "les deux":
            el.append(rect(xa, y + 9, xb - xa, 8, F_VERT, VERT, r=3, trait=1.4))
        else:
            el.append(rect(xb - 26, y + 9, 26, 8, F_VERT, VERT, r=3, trait=1.4))
        el.append(cercle(xa, y, 7, F_ORANGE, ORANGE, 1.8))
        el.append(rect(xb - 7, y - 7, 14, 14, F_BLEU, BLEU, r=2, trait=1.8))
    el.append(txt(W / 2, 324, "Américain : Marbury v. Madison (1803) · européen : Kelsen, Autriche (1920) · la QPC n'ajoute que l'a posteriori", 10.5, GRIS, italique=True))
    svg("deux_modeles.svg", W, 334, el)


# ------------------------------------------------------------------ 6. le schéma du chapitre
def schema_chapitre():
    el = []
    W = 700
    cx, cy = 350, 214
    el.append(ligne(cx, cy, cx, 290, GRIS, 1.6))
    el += boite(8, 10, 318, 170, "§ 1 — LA NOTION", [
        "la **norme suprême** : Kelsen, la pyramide",
        "**matérielle** : les règles sur le pouvoir",
        "**formelle** : le texte à procédure spéciale",
        "**écrite** ou **coutumière** (Royaume-Uni)",
        "coutume praeter legem ou contra legem",
        "**souple** ou **rigide** (art. 89 ; art. V)"], F_VERT, VERT, taille=11, pas=18)
    el += boite(374, 10, 318, 170, "§ 2 — ÉLABORATION ET RÉVISION", [
        "**originaire** : créer — révolution, guerre,",
        "effondrement ; octroi, pacte, assemblée,",
        "référendum (1958), les deux (1946)",
        "**dérivé** : réviser — art. 89 : projet ou",
        "proposition ; vote identique ; référendum",
        "ou Congrès (3/5) · limites : al. 4, al. 5",
        "25 révisions · 1962 : l'article 11"], F_ORANGE, ORANGE, taille=11, pas=17)
    el.append(rect(cx - 112, cy - 32, 224, 64, F_BLEU, BLEU, r=10, trait=2))
    el.append(txt(cx, cy - 6, "LA CONSTITUTION", 17, BLEU, gras=True))
    el.append(txt(cx, cy + 16, "la norme suprême de l'État", 11, NOIR, italique=True))
    el += boite(100, 290, 500, 148, "§ 3 — LA PROTECTION", [
        "**politique** : le Président (art. 5) — mais 1962 ; impeachment ; Haute Cour",
        "**modèle américain** (Marbury, 1803) : diffus, a posteriori, concret, relatif",
        "**modèle européen** (Kelsen, 1920) : concentré, a priori, abstrait, absolu",
        "**France** : le Conseil constitutionnel ; la **QPC** (2008-2010) ajoute l'a posteriori",
        "→ l'**État de droit**"], F_BLEU, BLEU, taille=11, pas=18)
    svg("schema_chapitre.svg", W, 446, el)


if __name__ == "__main__":
    hierarchie_normes()
    deux_pouvoirs()
    article89()
    qpc()
    deux_modeles()
    schema_chapitre()
