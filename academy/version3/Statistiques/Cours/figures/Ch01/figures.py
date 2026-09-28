#!/usr/bin/env python3
# Figures du cours Statistiques Ch01 — lancer : python3 figures.py
import os, sys
ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ICI, "..", "..", "..", "..", "outils"))
from graphes import Schema, barres, BLEU, ROUGE, VERT, ORANGE, GRIS, NOIR, VIOLET, PALETTE
F = lambda n: os.path.join(ICI, n)
esp = lambda v: "{:,.0f}".format(v).replace(",", " ")
virg = lambda v: ("%.1f" % v).replace(".", ",")

# 1. Les six étapes et la phrase qui les commande
s = Schema(660, 180)
et = ["① Quel type de\nproblématique ?", "② Choix des\ndonnées\nà observer", "③ Choix de la\nméthode\nde recueil", "④ Campagne\nde mesures", "⑤ Traitement\ndes données", "⑥ Prise de\ndécision"]
for k, t in enumerate(et):
    s.boite("e%d" % k, 12 + k * 108, 16, 96, 60, t, ROUGE if k == 0 else BLEU, "#fbecea" if k == 0 else "#f3f7fb", 10)
    if k:
        s.fleche("e%d" % (k - 1), "d", "e%d" % k, "g", GRIS)
# le retour : chaque étape 2 à 6 redescend sur une ligne commune qui remonte vers l'étape 1
s.el.append('<defs><marker id="rr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="%s"/></marker></defs>' % ROUGE)
x0, yb = 12 + 48, 108
for k in range(1, 6):
    xk = 12 + k * 108 + 48
    s.el.append('<line x1="%.1f" y1="76" x2="%.1f" y2="%d" stroke="%s" stroke-width="1.4"/>' % (xk, xk, yb, ROUGE))
s.el.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="1.4"/>' % (12 + 5 * 108 + 48, yb, x0, yb, ROUGE))
s.el.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="78" stroke="%s" stroke-width="1.6" marker-end="url(#rr)"/>' % (x0, yb, x0, ROUGE))
s.texte(330, 126, "chaque étape se justifie par la problématique", 10, ROUGE, italique=True)
s.texte(330, 164, "« Tous les choix sont guidés par le type de problématique. »", 12, ROUGE, gras=True)
s.enregistrer(F("etapes.svg"))

# 2. La distribution des 87 étudiants
barres(F("freres.svg"), ["0", "1", "2", "3", "4", "5", "6", "7", "9", "13", "14"],
       [("effectif", [11, 33, 23, 7, 3, 4, 1, 2, 1, 1, 1])], etiq_y="nombre d'étudiants", ymax=40, couleurs=[BLEU])

# 3. Les familles selon le nombre d'enfants (diapositive 22)
barres(F("familles.svg"), ["0", "1", "2", "3", "4 et plus"],
       [("fréquence (%)", [48.0, 22.3, 20.1, 7.2, 2.3])], etiq_y="% des familles", fmt=lambda v: virg(v), ymax=60, couleurs=[VERT])

# 4-5. Personnes écrouées : groupement par catégorie, puis par année
cat = ["Prévenus dét.", "Cond.-prév. dét.", "Condamnés dét.", "Cond. non dét."]
ans = {"2020": [17692, 2405, 41553, 12184], "2021": [18486, 2613, 47246, 13644],
       "2022": [18779, 2908, 49338, 14286], "2023": [19755, 3117, 51746, 15453]}
barres(F("ecroues_categorie.svg"), cat, [(a, v) for a, v in ans.items()], mode="groupe",
       etiq_y="personnes écrouées", fmt=esp, valeurs=False, ymax=60000, largeur=600)
barres(F("ecroues_annee.svg"), list(ans), [(cat[i], [ans[a][i] for a in ans]) for i in range(4)], mode="groupe",
       etiq_y="personnes écrouées", fmt=esp, valeurs=False, ymax=60000, largeur=600)

# 6-7. Enfants par famille : empilé, puis empilé à 100 %
annees = ["1990", "1999", "2007", "2012", "2017", "2023"]
ser = [("1 enfant", [3353.7, 3418.3, 3565.0, 3614.8, 3590.7, 3578.3]), ("2 enfants", [2800.5, 2841.1, 2996.3, 3074.1, 3101.1, 3039.0]),
       ("3 enfants", [1087.1, 1033.5, 1015.2, 1022.3, 1012.2, 956.2]), ("4 ou plus", [410.9, 334.5, 296.9, 296.1, 310.7, 308.4])]
barres(F("enfants_empile.svg"), annees, ser, mode="empile", etiq_y="milliers de familles", fmt=esp, ymax=9000, largeur=600)
barres(F("enfants_100.svg"), annees, ser, mode="cent", etiq_y="% des familles", fmt=virg, largeur=600)

# 8. Diapositive 31 : familles selon le nombre d'enfants, 1975-2008 (fréquences lues à l'image)
barres(F("familles_1975_2008.svg"), ["1975", "1982", "1990", "1999", "2008"],
       [("0 enfant", [37.0, 38.4, 42.1, 45.8, 48.0]), ("1", [25.3, 25.1, 23.8, 22.8, 22.3]), ("2", [20.2, 22.1, 21.7, 20.5, 20.1]),
        ("3", [9.8, 9.4, 8.8, 8.0, 7.2]), ("4 et plus", [7.7, 5.0, 3.5, 2.9, 2.3])], mode="cent", etiq_y="% des familles", fmt=virg, largeur=600)

# 9. Infractions déclarées en 2024, par type (diapositive 12)
barres(F("infractions.svg"), ["Vand. voiture", "Vol dans voit.", "Cambriolage", "Vand. logem.", "Vol vélo", "Vol s. effr.", "Vol voiture", "Vol 2-roues"],
       [("infractions", [2893000, 1544000, 1516000, 1141000, 853000, 616000, 549000, 264000])],
       etiq_y="nombre d'infractions", fmt=lambda v: virg(v / 1e6) + " M", ymax=3200000, largeur=620, couleurs=[BLEU])
print("figures écrites")
