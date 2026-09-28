#!/usr/bin/env python3
# Figures du cours Gestion Ch02 — lancer : python3 figures.py (écrit les .svg à côté)
import os, sys
ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ICI, "..", "..", "..", "..", "outils"))
from graphes import Schema, _t, BLEU, ROUGE, VERT, ORANGE, GRIS, NOIR, VIOLET
F = lambda n: os.path.join(ICI, n)

# 1. La pyramide de Maslow (diapositive 8), de la base au sommet
s = Schema(700, 330)
niveaux = [("1 — Physiologiques", "manger, boire, s'habiller, respirer, dormir, se laver", "#e8f0f8"),
           ("2 — Sécurité", "un toit, un lieu sécure, un emploi stable, une assurance maladie, une retraite", "#dfe9f4"),
           ("3 — Amour et appartenance", "famille, amis, groupe, communauté", "#d4e2f0"),
           ("4 — Estime", "estime de soi, reconnaissance, réussite, respect des autres", "#c7d9ec"),
           ("5 — Accomplissement de soi", "s'épanouir, exprimer son potentiel, sa créativité", "#b9cfe6")]
base_y, h, cx, demi_base, demi_haut = 300, 56, 150, 140, 16
for k, (titre, detail, fond) in enumerate(niveaux):
    y1, y0 = base_y - k * h, base_y - (k + 1) * h
    w1 = demi_base - (demi_base - demi_haut) * k / 5
    w0 = demi_base - (demi_base - demi_haut) * (k + 1) / 5
    s.el.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s" stroke="%s" stroke-width="1.4"/>' % (
        cx - w1, y1, cx + w1, y1, cx + w0, y0, cx - w0, y0, fond, BLEU))
    s.el.append(_t(cx, (y0 + y1) / 2 + 4, titre.split(" — ")[0], 13, BLEU, gras=True))
    s.el.append(_t(cx + w1 + 14, (y0 + y1) / 2 - 3, titre.split(" — ")[1], 11.5, BLEU, "start", gras=True))
    s.el.append(_t(cx + w1 + 14, (y0 + y1) / 2 + 12, detail, 9.5, NOIR, "start"))
s.el.append(_t(250, base_y + 20, "Lecture de bas en haut : un niveau devient motivant quand les précédents sont globalement satisfaits", 10, GRIS, italique=True))
s.enregistrer(F("maslow.svg"))

# 2. La matrice SWOT (diapositive 17)
s = Schema(560, 300)
x0, y0, L, H = 130, 50, 200, 110
cases = [(0, 0, "S — Strengths", "Forces", VERT, "#eef6ee"), (1, 0, "W — Weaknesses", "Faiblesses", ROUGE, "#fbecea"),
         (0, 1, "O — Opportunities", "Opportunités", VERT, "#eef6ee"), (1, 1, "T — Threats", "Menaces", ROUGE, "#fbecea")]
for i, j, a, b, c, f in cases:
    s.boite("c%d%d" % (i, j), x0 + i * L, y0 + j * H, L - 8, H - 8, "%s\n%s" % (a, b), c, f, 12.5)
s.texte(x0 + L / 2 - 4, 38, "Favorable", 12, VERT, gras=True)
s.texte(x0 + 3 * L / 2 - 4, 38, "Défavorable", 12, ROUGE, gras=True)
s.texte(64, y0 + H / 2 - 4, "INTERNE", 12, BLEU, gras=True)
s.texte(64, y0 + H / 2 + 12, "ce que l'organisation est", 9, GRIS)
s.texte(64, y0 + 3 * H / 2 - 4, "EXTERNE", 12, ORANGE, gras=True)
s.texte(64, y0 + 3 * H / 2 + 12, "ce qu'elle subit", 9, GRIS)
s.texte(x0 + L - 4, y0 + 2 * H + 20, "PESTEL (six facteurs externes) alimente la ligne du bas", 10.5, ORANGE, italique=True)
s.enregistrer(F("swot.svg"))

# 3. Le partage de la valeur ajoutée entre six parties prenantes (diapositives 23 à 25)
s = Schema(660, 410)
s.boite("va", 230, 156, 200, 64, "VALEUR AJOUTÉE\nchiffre d'affaires\n− consommations intermédiaires", ROUGE, "#fbecea", 11.5)
pp = [("etat", 13, 12, "L'État\nreçoit : impôts et taxes\napporte : infrastructures\net personnel formé"),
      ("banq", 230, 12, "Banques et prêteurs\nreçoivent : intérêts\napportent : financement\npar l'emprunt"),
      ("orga", 447, 12, "Organismes sociaux\nreçoivent : cotisations\napportent : protection\nsociale des salariés"),
      ("sal", 13, 300, "Salariés\nreçoivent : salaires\napportent : travail,\ncompétences, savoir-faire"),
      ("act", 230, 300, "Actionnaires\nreçoivent : dividendes\napportent : financement\nde l'activité (propriétaires)"),
      ("ent", 447, 300, "L'entreprise elle-même\nreçoit : réserves\nqui autofinancent\nses investissements")]
for nom, x, y, txt in pp:
    s.boite(nom, x, y, 200, 78, txt, BLEU, "#f3f7fb", 10)
for nom in ("etat", "banq", "orga"):
    s.fleche("va", "h", nom, "b", GRIS)
for nom in ("sal", "act", "ent"):
    s.fleche("va", "b", nom, "h", GRIS)
s.texte(330, 402, "Chaque partie prenante reçoit une part ET apporte une contribution", 10.5, NOIR, italique=True)
s.enregistrer(F("va.svg"))

# 4. Le circuit économique (diapositive 27, rapport Oxfam France) — deux flux par partenaire
s = Schema(720, 380)
s.boite("E", 310, 20, 100, 300, "ENTREPRISES", ROUGE, "#fbecea", 13)
gauche = [("four", 40, "Fournisseurs", "biens et services", "paiements"),
          ("etat", 150, "États", "cadre, subventions, crédits d'impôt", "impôt et taxes"),
          ("banq", 260, "Banques et prêteurs", "prêts", "remboursements et intérêts")]
droite = [("sal", 40, "Salarié·e·s", "apport de travail", "salaires, traitements, cotisations"),
          ("cli", 150, "Client·e·s", "paiements (chiffre d'affaires)", "ventes de biens et services"),
          ("act", 260, "Actionnaires", "capital social", "versements (dividendes)")]
def fl(x1, x2, y, coul):
    s.el.append('<defs><marker id="m%s" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="%s"/></marker></defs>' % (coul[1:], coul))
    s.el.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.8" marker-end="url(#m%s)"/>' % (x1, y, x2, y, coul, coul[1:]))
for nom, yc, titre, vers, depuis in gauche:
    s.boite(nom, 10, yc - 22, 130, 44, titre, BLEU, "#f3f7fb", 11.5)
    fl(140, 308, yc - 6, VERT); s.texte(224, yc - 11, vers, 9.5, VERT, gras=True)
    fl(310, 142, yc + 8, ORANGE); s.texte(224, yc + 21, depuis, 9.5, ORANGE, gras=True)
for nom, yc, titre, vers, depuis in droite:
    s.boite(nom, 580, yc - 22, 130, 44, titre, BLEU, "#f3f7fb", 11.5)
    fl(580, 412, yc - 6, VERT); s.texte(496, yc - 11, vers, 9.5, VERT, gras=True)
    fl(410, 578, yc + 8, ORANGE); s.texte(496, yc + 21, depuis, 9.5, ORANGE, gras=True)
s.boite("bourse", 580, 318, 130, 30, "Bourse", GRIS, "#f4f4f4", 11)
s.el.append('<line x1="645" y1="282" x2="645" y2="318" stroke="%s" stroke-width="1.6" stroke-dasharray="3 2"/>' % GRIS)
s.texte(575, 362, "plus-values ou moins-values entre actionnaires — aucun flux avec l'entreprise", 9.5, GRIS, "end", italique=True)
s.texte(250, 12, "vert : vers l'entreprise", 10, VERT, gras=True)
s.texte(470, 12, "orange : depuis l'entreprise", 10, ORANGE, gras=True)
s.enregistrer(F("circuit.svg"))

# 5. Les quatre capitaux (diapositive 42)
s = Schema(600, 280)
caps = [(0, 0, "Capital financier", "du point de vue économique", ORANGE, "#fdf3e6"),
        (1, 0, "Capital humain", "RH, potentiel de développement,\nsavoir attaché", VERT, "#eef6ee"),
        (0, 1, "Capital technique", "brevets, dessins, modèles,\ncode source, propriété intellectuelle", VIOLET, "#f3eef8"),
        (1, 1, "Relationnel et réputationnel", "« Qualité » : relations durables avec\nfournisseurs, clients, partenaires", BLEU, "#f3f7fb")]
for i, j, t, d, c, f in caps:
    s.boite("k%d%d" % (i, j), 20 + i * 290, 36 + j * 118, 270, 104, "%s\n%s" % (t, d), c, f, 12)
s.texte(300, 20, "Qu'est-ce qui fait la richesse d'une organisation ?", 12, NOIR, gras=True)
s.enregistrer(F("capitaux.svg"))

# 6. Avec qui travailler pour pérenniser (diapositive 45)
s = Schema(560, 250)
s.boite("act", 20, 20, 240, 60, "Actionnaires", BLEU, "#f3f7fb", 12.5)
s.boite("sal", 300, 20, 240, 60, "Salariés", BLEU, "#f3f7fb", 12.5)
s.boite("ops", 20, 150, 240, 70, "Fonctions opérationnelles\net recherche et développement (R&D)", ROUGE, "#fbecea", 12)
s.boite("cli", 300, 150, 240, 70, "Clients, public, partenaires", BLEU, "#f3f7fb", 12.5)
s.fleche("ops", "d", "cli", "g", ROUGE)
s.fleche("ops", "h", "sal", "b", ROUGE, courbe=0)
s.enregistrer(F("parties_prenantes.svg"))
print("figures écrites")
