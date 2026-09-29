#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Figures du chapitre 1 d'Institutions politiques — l'État.

    python3 Semestre1/Institutions_politiques/Cours/figures/Ch01/figures_ch01.py

Écrit à côté de ce script :
  trois_elements.svg   les trois éléments constitutifs de l'État
  espaces.svg          territoire terrestre, maritime et aérien (coupe schématique)
  formes.svg           des formes d'État, du plus unifié à l'union la plus lâche
  schema_chapitre.svg  le schéma qui relie tout le chapitre (section 4.4)
"""
import os
from xml.sax.saxutils import escape

ICI = os.path.dirname(os.path.abspath(__file__))
POLICE = "font-family=\"-apple-system,'Segoe UI',Helvetica,Arial,sans-serif\""
NOIR, GRIS, BLEU, ORANGE, VERT, ROUGE = "#1d2330", "#6b7280", "#1f4e79", "#b35c00", "#2e7d32", "#b3261e"
F_BLEU, F_ORANGE, F_VERT, F_GRIS, F_SABLE, F_MER, F_AIR = (
    "#e8eef6", "#fdf0e0", "#e6f2e7", "#f1f2f4", "#efe3cf", "#d6e6f5", "#eef6fc")


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


# ------------------------------------------------------------------ 1. les trois éléments
def trois_elements():
    el = []
    el += boite(215, 12, 250, 62, "L'ÉTAT", ["personne morale de droit public"], F_BLEU, BLEU)
    cases = [
        (10, "LE TERRITOIRE", ["élément matériel", "surface, sol, sous-sol,", "mer territoriale, espace aérien", "délimité par des frontières"], F_SABLE, ORANGE),
        (233, "LA POPULATION", ["élément humain", "les nationaux, rattachés", "à l'État par la nationalité", "(+ les étrangers, administrés)"], F_VERT, VERT),
        (456, "LA SOUVERAINETÉ", ["élément politique", "un pouvoir suprême,", "indivisible et perpétuel,", "interne et externe"], F_BLEU, BLEU),
    ]
    for x, t, l, fo, bo in cases:
        el += boite(x, 140, 214, 110, t, l, fo, bo)
        el.append(ligne(x + 107, 140, 340, 78, GRIS, 1.4, fleche=True))
    el.append(txt(340, 282, "Trois éléments cumulatifs : s'il en manque un seul, il n'y a pas d'État.", 12.5, ROUGE, gras=True))
    svg("trois_elements.svg", 680, 296, el)


# ------------------------------------------------------------------ 2. les espaces
def espaces():
    el = []
    W = 700
    # bandes verticales
    el.append(rect(10, 10, W - 20, 44, F_GRIS, GRIS, r=4, trait=1))
    el.append(txt(W / 2, 30, "Espace extra-atmosphérique : libre, nul ne peut se l'approprier (traité de 1967)", 12, NOIR, gras=True))
    el.append(txt(W / 2, 46, "— hors de toute souveraineté —", 11, GRIS, italique=True))
    # espace aérien : souverain au-dessus de la terre et de la mer territoriale (x 10 → 330)
    el.append(rect(10, 62, 320, 96, F_AIR, BLEU, r=4, trait=1.2))
    el.append(txt(170, 96, "ESPACE AÉRIEN SOUVERAIN", 12.5, BLEU, gras=True))
    el.append(txt(170, 114, "au-dessus du territoire terrestre", 11.5))
    el.append(txt(170, 129, "et de la mer territoriale", 11.5))
    el.append(txt(170, 147, "(convention de Chicago, 1944 ; drones compris)", 10.5, GRIS, italique=True))
    el.append(rect(336, 62, W - 346, 96, "#ffffff", GRIS, r=4, trait=1, pointille=True))
    el.append(txt(336 + (W - 346) / 2, 106, "Au-dessus de la ZEE et de la haute mer :", 11.5, GRIS))
    el.append(txt(336 + (W - 346) / 2, 123, "survol libre pour tous les États", 11.5, GRIS, gras=True))
    # sol et mer
    el.append(rect(10, 170, 220, 120, F_SABLE, ORANGE, r=0, trait=1.2))
    el.append(txt(120, 192, "TERRITOIRE TERRESTRE", 12.5, ORANGE, gras=True))
    el.append(txt(120, 212, "la surface", 11.5))
    el.append(ligne(18, 226, 222, 226, ORANGE, 0.8, pointille=True))
    el.append(txt(120, 246, "le sol", 11.5))
    el.append(ligne(18, 258, 222, 258, ORANGE, 0.8, pointille=True))
    el.append(txt(120, 278, "le sous-sol", 11.5))
    # zones maritimes (échelle non respectée)
    zones = [
        (230, 100, "MER", "TERRITORIALE", ["jusqu'à 12 milles", "souveraineté", "(passage inoffensif)"], "#b9d3ec", BLEU),
        (330, 240, "ZONE ÉCONOMIQUE", "EXCLUSIVE (ZEE)", ["jusqu'à 200 milles", "droits souverains sur les", "ressources ; navigation libre"], F_MER, BLEU),
        (570, W - 580, "HAUTE", "MER", ["au-delà de 200 milles", "liberté", "pour tous"], "#f4f8fc", GRIS),
    ]
    for x, w, t1, t2, l, fo, bo in zones:
        el.append(rect(x, 170, w, 120, fo, bo, r=0, trait=1.2))
        el.append(txt(x + w / 2, 190, t1, 11.5, bo, gras=True))
        el.append(txt(x + w / 2, 204, t2, 11.5, bo, gras=True))
        for k, s in enumerate(l):
            el.append(txt(x + w / 2, 228 + k * 17, s, 11, NOIR, gras=(k == 1)))
    # distances
    for x, lab1, lab2 in [(230, "côte", "(lignes de base)"), (330, "12 milles", "= 22,2 km"), (570, "200 milles", "= 370,4 km")]:
        el.append(ligne(x, 290, x, 306, NOIR, 1.2))
        el.append(txt(x, 320, lab1, 11.5, NOIR, gras=True))
        el.append(txt(x, 335, lab2, 11, GRIS))
    el.append(txt(W - 12, 356, "1 mille marin = 1 852 m · échelle non respectée", 10.5, GRIS, "end", italique=True))
    svg("espaces.svg", W, 364, el)


# ------------------------------------------------------------------ 3. les formes
def formes():
    el = []
    W, x0, g = 700, 6, 10
    noms = [("État unitaire", "centralisé", "modèle théorique", 96),
            ("État unitaire", "déconcentré", "préfets (1800)", 96),
            ("État unitaire", "décentralisé", "France (1982)", 96),
            ("État", "régional", "Italie, Espagne", 96),
            ("État", "fédéral", "États-Unis, Allemagne", 128),
            ("Confédération", "d'États", "Suisse avant 1848", 128)]
    couleurs = [(F_BLEU, BLEU)] * 4 + [(F_VERT, VERT), (F_ORANGE, ORANGE)]
    el.append(ligne(x0, 26, W - 8, 26, GRIS, 1.4, fleche=True))
    el.append(txt(x0, 18, "le pouvoir le plus concentré", 11, GRIS, "start", italique=True))
    el.append(txt(W - 8, 18, "l'union la plus lâche", 11, GRIS, "end", italique=True))
    xs, x = [], x0
    for k, (a, b, ex, w) in enumerate(noms):
        fo, bo = couleurs[k]
        el.append(rect(x, 40, w, 74, fo, bo))
        el.append(txt(x + w / 2, 62, a, 11.5, bo, gras=True))
        el.append(txt(x + w / 2, 78, b, 11.5, bo, gras=True))
        el.append(txt(x + w / 2, 102, ex, 10.5, NOIR, italique=True))
        xs.append((x, x + w))
        x += w + g
    xs1 = xs[4][0] - g / 2
    xs2 = xs[5][0] - g / 2
    for xx in (xs1, xs2):
        el.append(ligne(xx, 34, xx, 200, ROUGE, 1.3, pointille=True))

    def cat(xa, xb, lignes, coul):
        el.append(ligne(xa + 4, 128, xb - 4, 128, coul, 2))
        el.append(ligne(xa + 4, 122, xa + 4, 134, coul, 2))
        el.append(ligne(xb - 4, 122, xb - 4, 134, coul, 2))
        for k, (t, gras) in enumerate(lignes):
            el.append(txt((xa + xb) / 2, 150 + k * 15, t, 11.5 if gras else 11, coul if gras else NOIR, gras=gras))
    cat(x0, xs1, [("UN SEUL ÉTAT", True), ("une seule Constitution, une seule souveraineté", False)], BLEU)
    cat(xs1, xs2, [("UN ÉTAT FAIT", True), ("D'ÉTATS", True), ("créé par une", False), ("Constitution", False)], VERT)
    cat(xs2, W - 4, [("PAS UN ÉTAT", True), ("une association", False), ("d'États, créée", False), ("par un traité", False)], ORANGE)
    el.append(txt(xs1 - 8, 222, "① un seul État, ou un État fait d'États ?", 11, ROUGE, "end", gras=True))
    el.append(txt(xs2 - 8, 240, "② Constitution ou traité ?", 11, ROUGE, "end", gras=True))
    svg("formes.svg", W, 250, el)


# ------------------------------------------------------------------ 4. le schéma du chapitre
def schema_chapitre():
    el = []
    W = 700
    cx, cy = 345, 225
    el.append(ligne(cx, cy, 140, 95, GRIS, 1.6))
    el.append(ligne(cx, cy, 570, 105, GRIS, 1.6))
    el.append(ligne(cx, cy, cx, 280, GRIS, 1.6))
    el += boite(12, 20, 250, 150, "QUAND ? — l'origine", [
        "**Contrat social** (Rousseau, 1762) :",
        "l'État voulu, né d'un pacte",
        "critique : fiction, unanimité",
        "**Évolution naturelle** (Weber) :",
        "l'État subi, né des conflits",
        "critique : nie la volonté"], F_ORANGE, ORANGE, taille=11, pas=16)
    el += boite(450, 10, 242, 190, "QUOI ? — 3 éléments", [
        "**Territoire** : surface, sol, sous-sol,",
        "mer territoriale (12 milles), air",
        "**Population** : les nationaux",
        "(droit du sang, droit du sol)",
        "**Souveraineté** : suprême, indivisible,",
        "perpétuelle ; interne et externe",
        "titulaires : un seul, quelques-uns,",
        "le peuple"], F_VERT, VERT, taille=11, pas=17)
    el.append(rect(cx - 95, cy - 32, 190, 64, F_BLEU, BLEU, r=10, trait=2))
    el.append(txt(cx, cy - 6, "L'ÉTAT", 17, BLEU, gras=True))
    el.append(txt(cx, cy + 16, "personne morale", 11.5, NOIR, italique=True))
    el += boite(125, 280, 440, 132, "COMMENT ? — 2 formes", [
        "**État fédéral** : superposition, autonomie, participation",
        "**État unitaire** : déconcentration (agents nommés, hiérarchie),",
        "décentralisation (collectivités élues, contrôle de légalité)",
        "→ variante très décentralisée : l'État régional",
        "≠ **confédération** : un traité entre États, pas un État"], F_BLEU, BLEU, taille=11, pas=17)
    svg("schema_chapitre.svg", W, 420, el)


if __name__ == "__main__":
    trois_elements()
    espaces()
    formes()
    schema_chapitre()
