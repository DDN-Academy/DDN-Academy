#!/usr/bin/env python3
# Figures du cours Gestion Ch01 — lancer : python3 figures.py (écrit les .svg à côté)
import os, sys
ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ICI, "..", "..", "..", "..", "outils"))
from graphes import Schema, Repere, frise, BLEU, ROUGE, VERT, ORANGE, GRIS, NOIR, VIOLET

# 1. Frise chronologique de la conférence inaugurale
frise(os.path.join(ICI, "frise.svg"), 1855, 1925,
      [(1861, 1865, "Sécession", GRIS), (1865, 1901, "Gilded Age", ORANGE), (1890, 1920, "Ère Progressiste", BLEU)],
      [(1887, "Wilson, The Study of Administration", True), (1911, "Taylor, les 5 principes", True),
       (1912, "élection de Wilson", True), (1913, "Fed · droits de douane", True), (1914, "Clayton Antitrust Act", True)],
      largeur=660, hauteur=300, pas=5,
      titre=None)

# 2. Des trois maux aux quatre naissances
s = Schema(660, 330)
s.boite("maux", 200, 10, 260, 62, "Gilded Age : trois maux\ncrises et insuffisances du marché\nurbanisation et pollution · barons voleurs", ROUGE, "#fbecea", 11)
s.boite("pol", 40, 110, 240, 50, "Voie POLITIQUE\njustice sociale · syndicats · droits", VIOLET)
s.boite("tech", 380, 110, 240, 50, "Voie TECHNIQUE\nles naissances du management", BLEU)
s.fleche("maux", "b", "pol", "h", ROUGE)
s.fleche("maux", "b", "tech", "h", ROUGE)
n = [("n1", "① Management\nscientifique\n(l'entreprise)"), ("n2", "② Public\nadministration\n(l'État)"),
     ("n3", "③ Sciences sanitaires,\nhome economics\n(le foyer)"), ("n4", "④ Conservation,\nGospel of Efficiency\n(la nature)")]
for k, (nom, txt) in enumerate(n):
    s.boite(nom, 20 + k * 160, 220, 140, 70, txt, VERT if k == 0 else BLEU, "#f3f7fb", 10.5)
    s.fleche("tech", "b", nom, "h", BLEU)
s.texte(330, 318, "Une seule des quatre naissances concerne l'entreprise : le management naît partout à la fois.", 10.5, NOIR, italique=True)
s.enregistrer(os.path.join(ICI, "naissances.svg"))

# 3. La boucle de Ford
s = Schema(560, 300)
s.boite("a", 200, 12, 160, 48, "Chaîne de montage\ncadence imposée", BLEU)
s.boite("b", 380, 120, 160, 48, "Standardisation\nprix de revient ↓", BLEU)
s.boite("c", 200, 228, 160, 48, "Salaires ↑\nfidélisation", VERT)
s.boite("d", 20, 120, 160, 48, "Consommation\nde masse", ORANGE)
s.fleche("a", "d", "b", "h", GRIS, courbe=30)
s.fleche("b", "b", "c", "d", GRIS, courbe=30)
s.fleche("c", "g", "d", "b", GRIS, courbe=30)
s.fleche("d", "h", "a", "g", GRIS, courbe=30)
s.texte(280, 150, "produire plus vite →", 10.5, NOIR, italique=True)
s.texte(280, 166, "moins cher → payer plus →", 10.5, NOIR, italique=True)
s.texte(280, 182, "vendre plus", 10.5, NOIR, italique=True)
s.enregistrer(os.path.join(ICI, "ford.svg"))

# 4. La carte des organisations
s = Schema(660, 380)
s.texte(390, 22, "BUT LUCRATIF", 11.5, NOIR, gras=True)
s.texte(390, 36, "faire du profit", 10, GRIS, italique=True)
s.texte(560, 22, "BUT NON LUCRATIF", 11.5, NOIR, gras=True)
s.texte(560, 36, "« se concentre sur sa survie »", 10, GRIS, italique=True)
s.texte(70, 110, "SECTEUR", 11.5, NOIR, gras=True)
s.texte(70, 124, "PRIVÉ", 11.5, NOIR, gras=True)
s.texte(70, 270, "SECTEUR", 11.5, NOIR, gras=True)
s.texte(70, 284, "PUBLIC", 11.5, NOIR, gras=True)
s.boite("ep", 300, 50, 180, 130, "Entreprise privée\ncapitaux + main-d'œuvre\nsalariée · statut juridique\n(SARL, SAS, SA…)\npeut être à mission", BLEU, "#eef4fa", 10.5)
s.boite("as", 490, 50, 150, 130, "Association\nloi 1901, ≥ 2 membres\nbénéfice non interdit,\nnon partagé", VERT, "#eef7ee", 10.5)
s.boite("epub", 300, 210, 180, 130, "Entreprise publique\n≥ 51 % du capital\ndétenu par une\nadministration", ORANGE, "#fdf3e7", 10.5)
s.boite("adm", 490, 210, 150, 130, "Administrations\nÉtat · collectivités\n3 fonctions publiques\n+ associations financées\npar le secteur public", ORANGE, "#fdf3e7", 10.5)
s.texte(390, 362, "Le SERVICE public (activité d'intérêt général) traverse la frontière : délégation de service public à des entreprises privées.", 10, ROUGE, italique=True)
s.enregistrer(os.path.join(ICI, "organisations.svg"))

# 5. Espérance d'une coche au QCM
r = Repere(0, 1, -1, 1, largeur=460, hauteur=300, marges=(56, 24, 30, 44))
r.axes("p : probabilité que l'alternative soit juste", "gain espéré", [(0.25, "0,25"), (0.5, "0,5"), (0.75, "0,75"), (1, "1")], [(-1, "−1"), (-0.5, "−0,5"), (0.5, "+0,5"), (1, "+1")], origine="0")
r.droite(0, 0, 1, 0, couleur=GRIS, epaisseur=1)
r.zone([(0, 0), (0.5, 0), (0, -1)], ROUGE, 0.15)
r.zone([(0.5, 0), (1, 0), (1, 1)], VERT, 0.15)
r.droite(0, -1, 1, 1, couleur=BLEU, etiquette="E = 2p − 1", decal=(-110, 4))
r.point(0.5, 0, "seuil p = ½", ROUGE, decal=(6, 16), projeter=False)
r.texte(0.2, -0.3, "s'abstenir", ROUGE, 11, gras=True)
r.texte(0.78, 0.3, "cocher", VERT, 11, gras=True)
r.enregistrer(os.path.join(ICI, "coche.svg"))
print("5 figures écrites")
