#!/usr/bin/env python3
# Figures du cours Institutions politiques Ch01 — lancer : python3 figures.py (écrit les .svg à côté)
import os, sys
ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ICI, "..", "..", "..", "..", "outils"))
from graphes import Schema, _t, BLEU, ROUGE, VERT, ORANGE, GRIS, NOIR, VIOLET
F = lambda n: os.path.join(ICI, n)


def marqueur(s, ident, coul):
    s.el.append('<defs><marker id="%s" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="%s"/></marker></defs>' % (ident, coul))


def trait(s, x1, y1, x2, y2, coul=GRIS, ep=1.6, tirets=None, fleche=None):
    d = ' stroke-dasharray="%s"' % tirets if tirets else ""
    m = ' marker-end="url(#%s)"' % fleche if fleche else ""
    s.el.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s%s/>' % (x1, y1, x2, y2, coul, ep, d, m))


# 1. Le plan du chapitre : trois questions (diapositive 1)
s = Schema(700, 250)
s.boite("etat", 200, 12, 300, 50, "L'ÉTAT\n« l'institutionnalisation du pouvoir politique »", ROUGE, "#fbecea", 12.5)
col = [("quand", 12, "QUAND ? — l'origine", "Rousseau : le pacte social\nl'État VOULU\nWeber : l'évolution naturelle\nl'État SUBI", VIOLET, "#f3eef8"),
       ("quoi", 244, "QUOI ? — les éléments", "le territoire — matériel\nla population — personnel\nun pouvoir politique organisé\n— formel et abstrait", BLEU, "#f3f7fb"),
       ("comment", 476, "COMMENT ? — les formes", "État simple : l'État unitaire\n(déconcentré, décentralisé, régional)\nÉtat composé : la confédération\net l'État fédéral", VERT, "#eef6ee")]
for nom, x, t, d, c, f in col:
    s.boite(nom, x, 110, 212, 104, t + "\n" + d, c, f, 11)
    s.fleche("etat", "b", nom, "h", GRIS)
s.texte(350, 238, "Diapositive 1 : « Réponse à trois questions : QUAND · QUOI · COMMENT ⟹ 3 paragraphes »", 10.5, GRIS, italique=True)
s.enregistrer(F("plan.svg"))

# 2. Les espaces de l'État : coupe schématique (échelle non respectée)
s = Schema(720, 330)
xc, xt, xz, xf, ymer = 170, 262, 560, 708, 190
# espace extra-atmosphérique et espace aérien souverain (au-dessus de la terre et de la mer territoriale)
s.el.append('<rect x="12" y="30" width="%d" height="36" fill="#f4f4f4" stroke="none"/>' % (xf - 12))
s.texte(360, 53, "espace extra-atmosphérique : exclu, il reste libre", 11, GRIS, gras=True)
s.el.append('<rect x="12" y="70" width="%d" height="%d" fill="#e8f0f8" stroke="%s" stroke-dasharray="4 3"/>' % (xt - 12, ymer - 70, BLEU))
s.texte((12 + xt) / 2, 92, "espace aérien", 11.5, BLEU, gras=True)
s.texte((12 + xt) / 2, 107, "souverain", 11.5, BLEU, gras=True)
s.texte((xt + xf) / 2, 100, "au-dessus de la ZEE et de la haute mer : survol libre", 10, GRIS, italique=True)
# terre, mer, fond
s.el.append('<polygon points="12,%d %d,%d %d,300 12,300" fill="#e9dcc7" stroke="#8d6e63" stroke-width="1.4"/>' % (ymer - 30, xc, ymer - 30, xc))
s.el.append('<rect x="%d" y="%d" width="%d" height="95" fill="#d7e8f5" stroke="none"/>' % (xc, ymer, xf - xc))
s.el.append('<polygon points="%d,%d %d,236 %d,236 %d,300 %d,300 %d,300" fill="#cdb89a" stroke="#8d6e63" stroke-width="1.2"/>' % (xc, ymer, xc + 30, 420, 470, xf, xc))
s.texte(90, 218, "territoire terrestre", 11.5, "#6d4c41", gras=True)
s.texte(90, 234, "surface, sol et sous-sol", 10, "#6d4c41")
s.texte(330, 260, "plateau continental", 10.5, "#6d4c41", gras=True)
s.texte(330, 274, "(prolongement immergé du continent)", 9.5, "#6d4c41")
s.texte(470, 290, "talus", 9.5, "#6d4c41", italique=True)
# bornes
for x in (xc, xt, xz):
    trait(s, x, 118, x, ymer + 40, NOIR, 1.2, "3 2")
s.texte(xc, 314, "côte", 10.5, NOIR, gras=True)
s.texte(xt, 314, "12 milles", 10.5, NOIR, gras=True)
s.texte(xz, 314, "200 milles", 10.5, NOIR, gras=True)
s.texte((xc + xt) / 2, 134, "mer", 11, BLEU, gras=True)
s.texte((xc + xt) / 2, 148, "territoriale", 11, BLEU, gras=True)
s.texte((xc + xt) / 2, 162, "comme sur terre", 9.5, NOIR)
s.texte((xt + xz) / 2, 134, "zone économique exclusive — « mer patrimoniale »", 11, ORANGE, gras=True)
s.texte((xt + xz) / 2, 150, "188 milles de plus : pêche, pétrole, richesses sous-marines", 9.5, NOIR)
s.texte((xt + xz) / 2, 164, "réservés à l'État riverain ; la navigation reste libre", 9.5, NOIR)
s.texte((xz + xf) / 2, 134, "haute mer", 11, VERT, gras=True)
s.texte((xz + xf) / 2, 150, "ouverte à tous :", 9.5, NOIR)
s.texte((xz + xf) / 2, 164, "principe de liberté", 9.5, NOIR)
s.texte(360, 20, "Échelle non respectée · 1 mille marin = 1 852 m · 12 + 188 = 200 milles = 370,4 km", 10.5, GRIS, italique=True)
s.enregistrer(F("espaces.svg"))

# 3. Nation et État : trois configurations
s = Schema(720, 250)
def etat(x, y, l, h, nom):
    s.el.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#f3f7fb" stroke="%s" stroke-width="1.8"/>' % (x, y, l, h, BLEU))
    if nom:
        s.el.append(_t(x + l / 2, y + h - 8, nom, 9.5, BLEU, gras=True))
def nation(cx, cy, rx, ry, nom):
    s.el.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" fill-opacity="0.18" stroke="%s" stroke-width="1.8" stroke-dasharray="6 3"/>' % (cx, cy, rx, ry, ORANGE, ORANGE))
    if nom:
        s.el.append('<rect x="%.1f" y="%.1f" width="%.1f" height="15" rx="3" fill="#ffffff" fill-opacity="0.92"/>' % (cx - 3.2 * len(nom) - 4, cy - 8, 6.4 * len(nom) + 8))
        s.el.append(_t(cx, cy + 4, nom, 10, ORANGE, gras=True))
# a) État-nation
etat(30, 40, 180, 130, "un État")
nation(120, 98, 82, 50, "une nation")
s.texte(120, 196, "① L'État-nation", 12, NOIR, gras=True)
s.texte(120, 212, "la nation « s'incarne dans une", 9.5, NOIR)
s.texte(120, 225, "réalité juridique » — un projet", 9.5, NOIR)
# b) nation écartelée
for k, nom in enumerate(["Turquie", "Irak", "Iran", "Syrie"]):
    etat(262 + (k % 2) * 92, 34 + (k // 2) * 72, 88, 68, nom)
nation(360, 104, 70, 42, "nation kurde")
s.texte(360, 196, "② Une nation écartelée", 12, NOIR, gras=True)
s.texte(360, 212, "entre plusieurs États : Kurdes,", 9.5, NOIR)
s.texte(360, 225, "deux Corées, Allemagne 1945-1990", 9.5, NOIR)
# c) État multinational
etat(510, 40, 180, 130, "un État")
nation(560, 76, 40, 26, "")
nation(640, 76, 40, 26, "")
nation(600, 118, 44, 22, "")
s.texte(600, 30, "plusieurs nations", 10, ORANGE, gras=True)
s.texte(600, 196, "③ Un État multinational", 12, NOIR, gras=True)
s.texte(600, 212, "Autriche-Hongrie jusqu'en 1918,", 9.5, NOIR)
s.texte(600, 225, "URSS jusqu'en 1991, Canada, Belgique", 9.5, NOIR)
s.texte(360, 16, "rectangle plein : un État (réalité juridique) · ovale en tirets : une nation (sentiment d'appartenance)", 10, GRIS, italique=True)
s.enregistrer(F("nation_etat.svg"))

# 4. Le paradoxe de la soumission de l'État au droit, et ses trois réponses
s = Schema(700, 300)
s.boite("pb", 150, 12, 400, 58, "LE PARADOXE\nl'État souverain crée le droit :\ncomment le droit pourrait-il le lier ?", ROUGE, "#fbecea", 11.5)
s.boite("dn", 12, 110, 320, 86, "① Le droit naturel\nun droit « constaté et non pas créé », au-dessus de l'État\nAntigone : peut justifier la désobéissance\nlimites : contenu flou ; la souveraineté n'est plus illimitée", VIOLET, "#f3eef8", 10)
s.boite("al", 368, 110, 320, 86, "② L'autolimitation\n« patere legem quam fecisti »\nl'État se lie lui-même en posant la règle\nlimite : celui qui se lie peut se délier", BLEU, "#f3f7fb", 10)
s.boite("rep", 130, 222, 440, 66, "③ La réponse n'est pas strictement juridique, mais politique\nl'État de droit : « récent, fragile, loin d'être universel »\n+ la légitimité : un pouvoir accepté par les gouvernés", VERT, "#eef6ee", 10.5)
s.fleche("pb", "b", "dn", "h", GRIS)
s.fleche("pb", "b", "al", "h", GRIS)
s.fleche("dn", "b", "rep", "h", GRIS)
s.fleche("al", "b", "rep", "h", GRIS)
s.enregistrer(F("paradoxe.svg"))

# 5. Déconcentration et décentralisation : qui nomme, qui contrôle
s = Schema(720, 330)
s.texte(180, 22, "DÉCONCENTRATION", 13, BLEU, gras=True)
s.texte(180, 38, "« le même marteau, un manche raccourci »", 10, BLEU, italique=True)
s.boite("etat1", 60, 52, 240, 52, "L'État (le gouvernement)\ncentre unique de décision", BLEU, "#f3f7fb", 11)
s.boite("pref", 60, 190, 240, 62, "Préfet, recteur, procureur…\nune AUTORITÉ DE L'ÉTAT\ndans une circonscription administrative", BLEU, "#f3f7fb", 10.5)
s.fleche("etat1", "b", "pref", "h", BLEU)
s.texte(186, 132, "nomme et révoque (les personnes)", 10, BLEU, "start", gras=True)
s.texte(186, 148, "injonction, réformation (les actes)", 10, BLEU, "start", gras=True)
s.texte(186, 164, "= contrôle HIÉRARCHIQUE", 10, BLEU, "start", gras=True)
s.texte(180, 276, "aucune autonomie : un agent de l'État", 10.5, NOIR, italique=True)
trait(s, 360, 16, 360, 300, GRIS, 1, "4 3")
s.texte(540, 22, "DÉCENTRALISATION", 13, VERT, gras=True)
s.texte(540, 38, "« le marteau a changé de main »", 10, VERT, italique=True)
s.boite("elec", 390, 52, 130, 52, "Les électeurs\nlocaux", VERT, "#eef6ee", 11)
s.boite("loi", 560, 52, 150, 52, "La loi nationale\nfixe le domaine\n(article 72 al. 3)", GRIS, "#f4f4f4", 10.5)
s.boite("coll", 390, 190, 170, 62, "Conseil élu d'une\nCOLLECTIVITÉ TERRITORIALE\npersonne morale distincte", VERT, "#eef6ee", 10.5)
s.boite("etat2", 590, 190, 120, 62, "L'État\n(le préfet)", GRIS, "#f4f4f4", 11)
s.fleche("elec", "b", "coll", "h", VERT, "élisent")
s.fleche("loi", "b", "coll", "h", GRIS)
marqueur(s, "cl", ORANGE)
trait(s, 590, 232, 562, 232, ORANGE, 1.8, "5 3", "cl")
s.texte(650, 270, "contrôle de légalité (tutelle) :", 9.5, ORANGE, gras=True)
s.texte(650, 284, "la conformité au droit,", 9.5, ORANGE)
s.texte(650, 298, "jamais l'opportunité", 9.5, ORANGE)
s.texte(475, 276, "autonomie juridique et financière,", 10, NOIR, italique=True)
s.texte(475, 290, "pas l'indépendance", 10, NOIR, italique=True)
s.texte(360, 322, "Le test : qui peut révoquer celui qui décide ? L'État → déconcentration · les électeurs → décentralisation", 11, ROUGE, gras=True)
s.enregistrer(F("deconcentration.svg"))

# 6. Les formes d'État sur une échelle d'autonomie (« des différences de degré »)
s = Schema(720, 290)
marqueur(s, "ax", NOIR)
trait(s, 30, 150, 700, 150, NOIR, 2, None, "ax")
s.texte(34, 140, "autonomie croissante des entités →", 10.5, NOIR, "start", gras=True)
formes = [(70, "unitaire", "centralisé", "", BLEU), (170, "unitaire", "déconcentré", "préfets", BLEU),
          (270, "unitaire", "décentralisé", "France", BLEU), (380, "État", "régional", "Italie, Espagne", BLEU),
          (500, "État", "fédéral", "États-Unis, Allemagne", VERT), (630, "confédération", "d'États", "CEI, Commonwealth", ORANGE)]
for x, a, b, ex, c in formes:
    s.el.append('<circle cx="%d" cy="150" r="6" fill="%s"/>' % (x, c))
    s.texte(x, 176, a, 11, c, gras=True)
    s.texte(x, 190, b, 11, c, gras=True)
    if ex:
        s.texte(x, 206, ex, 9.5, NOIR, italique=True)
# l'Union européenne, entre fédération et confédération
s.el.append('<rect x="551" y="143" width="28" height="14" rx="3" fill="%s"/>' % VIOLET)
s.texte(565, 128, "Union européenne", 10, VIOLET, gras=True)
s.texte(565, 116, "« des originalités multiples »", 9, VIOLET, italique=True)
# familles et source du partage
def accolade(x1, x2, y, txt, c):
    trait(s, x1, y, x2, y, c, 1.6)
    trait(s, x1, y, x1, y + 8, c, 1.6)
    trait(s, x2, y, x2, y + 8, c, 1.6)
    s.texte((x1 + x2) / 2, y - 7, txt, 11, c, gras=True)
accolade(46, 404, 72, "ÉTAT SIMPLE (un seul État)", BLEU)
accolade(470, 700, 72, "ÉTAT COMPOSÉ (union d'États)", VERT)
s.texte(170, 236, "compétences fixées par la LOI", 10.5, BLEU, gras=True)
s.texte(440, 236, "partage inscrit dans la CONSTITUTION", 10.5, VERT, gras=True)
s.texte(640, 236, "un TRAITÉ", 10.5, ORANGE, gras=True)
s.texte(360, 272, "« Il existe plus de différences de degré entre toutes ces formes d'États que des différences de nature »", 11, ROUGE, gras=True)
s.texte(360, 30, "Les formes d'État, rangées par autonomie croissante des entités qui les composent", 12, NOIR, gras=True)
s.enregistrer(F("formes.svg"))

# 7. L'État fédéral : deux étages et trois principes
s = Schema(720, 360)
s.boite("fed", 90, 44, 400, 84, "ÉTAT FÉDÉRAL — la Fédération\nConstitution fédérale · compétence d'ATTRIBUTION (énumérée)\nseul sujet international : diplomatie, armée, monnaie, nationalité\nchambre du peuple + chambre des États", VERT, "#eef6ee", 10.5)
for k, nom in enumerate("ABC"):
    s.boite("f" + nom, 40 + k * 170, 232, 150, 78, "État fédéré %s\nConstitution, parlement,\ntribunaux, exécutif\ncompétence de DROIT COMMUN" % nom, BLEU, "#f3f7fb", 10)
    s.fleche("f" + nom, "h", "fed", "b", ORANGE)
s.boite("part", 548, 118, 162, 124, "PARTICIPATION\nla seconde chambre\n(Sénat, Bundesrat)\nla désignation de l'exécutif\nla révision : aux États-Unis,\n⅔ du Congrès puis ¾ des\nÉtats fédérés, soit 38", ORANGE, "#fdf3e6", 10)
s.texte(454, 186, "les États fédérés", 10, ORANGE, "start", italique=True)
s.texte(454, 200, "participent →", 10, ORANGE, "start", italique=True)
s.texte(360, 24, "SUPERPOSITION : un nouvel État se superpose aux États membres — « il les englobe mais ne les absorbe pas »", 10.5, VERT, gras=True)
s.texte(360, 334, "AUTONOMIE : tout se dédouble — deux territoires, deux citoyennetés (fédérale et fédérée), deux Constitutions", 10.5, BLEU, gras=True)
s.texte(360, 352, "Le partage est protégé par une juridiction constitutionnelle (Cour suprême, Cour constitutionnelle allemande)", 10, GRIS, italique=True)
s.enregistrer(F("federal.svg"))

# 8. Frise chronologique en deux bandes — placement automatique des étiquettes, sans croisement
def bande(nom, debut, fin, pas, evts, periodes, titre, hauteur=300, niveaux=8, seuil=0.6):
    W, g, d = 720, 24, 24
    X = lambda a: g + (a - debut) / (fin - debut) * (W - g - d)
    larg = lambda lib: 5.2 * len(lib) + 8
    def compatible(cote, niv, x, x1, x2, places):
        if x1 < 2 or x2 > W - 2:
            return False
        for c2, n2, xe, a1, a2 in places:
            if c2 != cote:
                continue
            if n2 == niv and not (x2 + 6 < a1 or x1 - 6 > a2):
                return False  # deux étiquettes au même niveau se chevauchent
            if n2 < niv and a1 - 3 <= x <= a2 + 3:
                return False  # le trait du nouvel événement traverserait une étiquette plus basse
            if n2 > niv and x1 - 3 <= xe <= x2 + 3:
                return False  # le trait d'un événement déjà placé traverserait la nouvelle étiquette
        return True
    gauche_ = sorted([e for e in evts if X(e[0]) <= W * seuil], key=lambda e: -e[0])
    droite_ = sorted([e for e in evts if X(e[0]) > W * seuil], key=lambda e: e[0])
    ordre = gauche_ + droite_
    def geo(e):
        x = X(e[0]); dr = x > W * seuil
        return x, dr, ((x - larg(e[1]), x) if dr else (x, x + larg(e[1])))
    def cherche(k, places):  # recherche en profondeur, niveaux bas d'abord
        if k == len(ordre):
            return places
        x, dr, (x1, x2) = geo(ordre[k])
        for niv in range(1, niveaux + 1):
            for cote in (1, -1):
                if compatible(cote, niv, x, x1, x2, places):
                    r = cherche(k + 1, places + [(cote, niv, x, x1, x2)])
                    if r:
                        return r
        return None
    places = cherche(0, [])
    assert places, ("pas de placement possible", nom)
    haut = max([n for c0, n, *_ in places if c0 > 0] or [0])
    bas = max([n for c0, n, *_ in places if c0 < 0] or [0])
    yl = 34 + haut * 16 + 8
    s = Schema(W, int(yl + 30 + bas * 16 + 6))
    for (a, lib, c), (cote, niv, x, x1, x2) in zip(ordre, places):
        droite = x > W * seuil
        y2 = yl - 10 - (niv - 1) * 16 if cote > 0 else yl + 30 + (niv - 1) * 16
        trait(s, x, yl, x, y2 + (3 if cote > 0 else -10), GRIS, 0.8, "2 2")
        s.el.append('<circle cx="%.1f" cy="%.1f" r="3.2" fill="%s"/>' % (x, yl, c))
        s.el.append(_t(x + (-3 if droite else 3), y2, lib, 9.5, c, "end" if droite else "start"))
    trait(s, g, yl, W - d, yl, NOIR, 2)
    for a0 in range(debut - debut % pas + pas, fin + 1, pas):
        if a0 > debut:
            trait(s, X(a0), yl - 4, X(a0), yl + 4, NOIR, 1)
            s.el.append(_t(X(a0), yl + 13, a0, 8.5, GRIS))
    for a0, b0, c in periodes:
        s.el.append('<rect x="%.1f" y="%.1f" width="%.1f" height="7" rx="2" fill="%s" fill-opacity="0.85"/>' % (X(a0), yl - 3.5, max(3, X(b0) - X(a0)), c))
    s.el.append(_t(W / 2, 16, titre, 12, NOIR, gras=True))
    s.enregistrer(F(nom))

bande("frise1.svg", 1560, 1930, 50, [
    (1566, "1566 — édit de Moulins : domaine inaliénable", BLEU),
    (1576, "1576 — Bodin, De la République : la souveraineté", VIOLET),
    (1778, "1778-1787 — Confédération des États-Unis", ORANGE),
    (1789, "1789 — principe des nationalités ; conception moderne de l'État", VIOLET),
    (1791, "1791 « Le Royaume est un et indivisible » ; 1792 la République", BLEU),
    (1800, "17 févr. 1800 (28 pluviôse an VIII) — les préfets", BLEU),
    (1815, "1815 — traité de Vienne ; 1815-1866 Confédération germanique", ORANGE),
    (1848, "1848 — Suisse fédérale ; révolutions : les nationalités renaissent", VERT),
    (1871, "1871 — fin de la Confédération de l'Allemagne du Nord", ORANGE),
    (1918, "1918 — fin de l'Autriche-Hongrie", VIOLET),
    (1919, "1919 — traité de Versailles", VIOLET),
    (1924, "1924 — droit d'Alsace-Moselle", BLEU)],
    [(1778, 1787, ORANGE), (1815, 1866, ORANGE)],
    "De l'édit de Moulins au droit d'Alsace-Moselle (1566-1924)", 290)

bande("frise2.svg", 1930, 2015, 10, [
    (1933, "1933 — IIIᵉ Reich", VIOLET),
    (1940, "1940-1944 — Vichy", ROUGE),
    (1944.6, "9 août 1944 — ordonnance de rétablissement de la légalité républicaine", ROUGE),
    (1945, "1945 — 51 États à l'ONU", NOIR),
    (1947, "1947 — « Paris et le désert français »", BLEU),
    (1951, "1951 et 1957 — les Communautés européennes", ORANGE),
    (1958, "1958 — la Constitution", BLEU),
    (1971, "1971 — Bangladesh", NOIR),
    (1982, "2 mars 1982 — acte I", BLEU),
    (1990, "1990 — réunification allemande", VIOLET),
    (1991, "1991 — fin de l'URSS ; la CEI", ORANGE),
    (1992, "1992 — Maastricht (7 févr.) ; art. 88-3", ORANGE),
    (1997, "1997 · 2001 · 2007 — Amsterdam, Nice, Lisbonne", ORANGE),
    (2003, "28 mars 2003 — acte II", BLEU),
    (2010, "2010 — acte III", BLEU),
    (2011, "2011 — Sud-Soudan : 193 États", NOIR)],
    [(1940, 1944.6, ROUGE)],
    "Du IIIᵉ Reich au Sud-Soudan (1933-2011)", 300, 8, 0.5)
print("figures écrites")
