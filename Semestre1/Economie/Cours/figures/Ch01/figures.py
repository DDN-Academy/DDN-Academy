#!/usr/bin/env python3
# Figures du cours Économie Ch01 — lancer : python3 figures.py
import os, sys
ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ICI, "..", "..", "..", "..", "outils"))
from graphes import Repere, barres, BLEU, ROUGE, VERT, ORANGE, GRIS, NOIR, VIOLET

def base(titre_x="L — quantité de travail", titre_y="W — salaire", xmax=80, ymax=12):
    return Repere(0, xmax, 0, ymax, largeur=520, hauteur=340).axes(titre_x, titre_y, origine="0")

D = lambda L: 10 - 0.1 * L      # demande de travail : décroissante
S = lambda L: 2 + 0.1 * L       # offre de travail : croissante

# Cas 1 — équilibre
r = base()
r.courbe([(0, D(0)), (80, D(80))], BLEU, etiquette="Demande (entreprises)", decal=(-150, -10))
r.courbe([(0, S(0)), (80, S(80))], VERT, etiquette="Offre (individus)", decal=(-130, 16))
r.point(40, 6, "E", NOIR, lab_x="L*", lab_y="W*")
r.enregistrer(os.path.join(ICI, "cas1.svg"))

# Cas 2 — le RSA fait plancher au-dessus de W*
r = base()
r.courbe([(0, D(0)), (80, D(80))], BLEU, etiquette="Demande", decal=(-70, -10))
r.courbe([(0, S(0)), (80, S(80))], VERT, pointille=True)
r.courbe([(0, 8), (60, 8), (80, S(80))], VERT, etiquette="Offre effective", decal=(-120, -12))
r.point(40, 6, None, GRIS, lab_x="L*", lab_y="W*")
r.point(20, 8, "A", BLEU, decal=(-4, -10), lab_x="La", lab_y="RSA")
r.point(60, 8, "O", VERT, decal=(4, -10), lab_x="Lo")
r.fleche(20, 9.3, 60, 9.3, ROUGE, "chômage involontaire = Lo − La", decal=(0, -6))
r.fleche(60, 9.3, 20, 9.3, ROUGE)
r.enregistrer(os.path.join(ICI, "cas2.svg"))

# Cas 3 — l'offre se déplace vers le haut et la gauche
r = base()
r.courbe([(0, D(0)), (80, D(80))], BLEU, etiquette="Demande", decal=(-70, -10))
r.courbe([(0, S(0)), (80, S(80))], VERT, pointille=True, etiquette="Offre initiale", decal=(-100, 18))
r.courbe([(0, 4), (80, 12)], VERT, etiquette="Nouvelle offre", decal=(-120, -10))
r.point(40, 6, "E", GRIS, decal=(8, 14), lab_x="L*", lab_y="W*")
r.point(30, 7, "E'", NOIR, decal=(-22, -8), lab_x="L*rsa", lab_y="W*rsa")
r.fleche(55, 7.5, 45, 8.5, ROUGE, "l'offre recule", decal=(30, -4))
r.enregistrer(os.path.join(ICI, "cas3.svg"))

# Cas 4a — faible qualification : RSA au-dessus de W*
r = base()
r.courbe([(0, 7), (70, 0)], BLEU, etiquette="Demande", decal=(-60, -24))
r.courbe([(0, 1), (80, 9)], VERT, pointille=True)
r.courbe([(0, 5.5), (45, 5.5), (80, 9)], VERT, etiquette="Offre effective", decal=(-110, -12))
r.point(30, 4, None, GRIS, lab_x="L*", lab_y="W*")
r.point(15, 5.5, "A", BLEU, decal=(-4, -10), lab_x="La", lab_y="RSA")
r.point(45, 5.5, "O", VERT, decal=(4, -10), lab_x="Lo")
r.texte(40, 11, "Faible qualification : le plancher mord", ROUGE, 12, gras=True)
r.enregistrer(os.path.join(ICI, "cas4a.svg"))

# Cas 4b — haute qualification : RSA en dessous de W*
r = base(ymax=16)
r.courbe([(0, 14), (80, 6)], BLEU, etiquette="Demande", decal=(-60, 20))
r.courbe([(0, 6), (80, 14)], VERT, etiquette="Offre", decal=(-40, -8))
r.point(40, 10, "E", NOIR, lab_x="L*", lab_y="W*")
r.droite(0, 5.5, 80, 5.5, couleur=ROUGE, pointille=True)
r.texte(8, 4.4, "RSA", ROUGE, 11, ancre="start", gras=True)
r.texte(40, 2, "Haute qualification : le plancher ne mord pas", VERT, 12, gras=True)
r.enregistrer(os.path.join(ICI, "cas4b.svg"))

# Dépenses de protection sociale par habitant, France / UE, 2021
cats = ["Vieillesse", "Santé", "Famille", "Emploi", "Pauvreté", "Logement"]
barres(os.path.join(ICI, "depenses.svg"), cats,
       [("Moyenne UE", [4550, 3800, 850, 600, 250, 100]), ("France", [5300, 4550, 850, 900, 500, 250])],
       mode="groupe", etiq_y="euros par habitant et par an", fmt=lambda v: "{:,.0f}".format(v).replace(",", " "), ymax=6000,
       couleurs=[GRIS, BLEU])

# L'écart France − UE, décomposé
barres(os.path.join(ICI, "ecart.svg"), cats, [("Écart France − UE (€)", [750, 750, 0, 300, 250, 150])],
       mode="simple", etiq_y="écart en euros par habitant", fmt="{:g}", ymax=800, couleurs=[ROUGE])

# Profil par âge des allocataires du RSA
barres(os.path.join(ICI, "rsa_age.svg"), ["< 25", "25-29", "30-39", "40-49", "50-59", "60-64", "≥ 65"],
       [("part des allocataires (%)", [4, 17, 30, 22, 19, 7, 2])], mode="simple",
       etiq_y="% des allocataires", fmt="{:g} %", ymax=40, couleurs=[BLEU])

# Coût d'opportunité en taux : frontière de production (40 x ou 120 y)
r = Repere(0, 50, 0, 140, largeur=440, hauteur=320).axes("bien x", "bien y", [(20, "20"), (40, "40")], [(60, "60"), (120, "120")])
r.droite(0, 120, 40, 0, couleur=BLEU)
r.point(0, 120, None, BLEU, projeter=False)
r.point(40, 0, None, BLEU, projeter=False)
r.point(20, 60, "(20 ; 60)", NOIR, decal=(8, -6))
r.texte(27, 118, "toutes les combinaisons possibles", BLEU, 11, gras=True)
r.texte(27, 104, "des ressources de l'usine", BLEU, 11)
r.texte(33, 70, "pente = −3 :", ROUGE, 11, gras=True)
r.texte(33, 57, "1 x de plus = 3 y de moins", ROUGE, 11, gras=True)
r.enregistrer(os.path.join(ICI, "frontiere.svg"))
print("figures écrites")
