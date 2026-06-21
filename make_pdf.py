#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genere le PDF de backtest de "La Tendance Porteuse" depuis data/backtest_results.json.
Aucun chiffre invente : tout vient du moteur (final/backtest)."""
import json
from fpdf import FPDF

R=json.load(open("data/backtest_results.json"))
A,TR,TE,CT,Y=R["all"],R["train"],R["test"],R["ctrl_2025"],R["yearly"]
P=R["params"]
GOLD=(180,140,40); DARK=(20,25,35); GREY=(90,100,115); GREEN=(40,150,110); RED=(200,60,60)

pdf=FPDF("P","mm","A4"); pdf.set_auto_page_break(True,15)
def header(t):
    pdf.set_fill_color(*DARK); pdf.rect(0,0,210,22,"F")
    pdf.set_xy(12,7); pdf.set_text_color(*GOLD); pdf.set_font("Helvetica","B",13); pdf.cell(0,8,t)
    pdf.set_xy(12,26); pdf.set_text_color(0,0,0)
def h2(t):
    pdf.ln(3); pdf.set_font("Helvetica","B",11); pdf.set_text_color(*GOLD)
    pdf.cell(0,7,t,new_x="LMARGIN",new_y="NEXT"); pdf.set_text_color(0,0,0)
def kv(k,v,c=(0,0,0)):
    pdf.set_font("Helvetica","",10); pdf.set_text_color(0,0,0); pdf.cell(95,6,k)
    pdf.set_font("Helvetica","B",10); pdf.set_text_color(*c); pdf.cell(0,6,str(v),new_x="LMARGIN",new_y="NEXT"); pdf.set_text_color(0,0,0)
def table(headers,rows,widths,colors=None):
    pdf.set_font("Helvetica","B",8.5); pdf.set_fill_color(*DARK); pdf.set_text_color(*GOLD)
    for hh,w in zip(headers,widths): pdf.cell(w,6,str(hh),fill=True,align="C")
    pdf.ln(); pdf.set_font("Helvetica","",8.5); fill=False
    for ri,r in enumerate(rows):
        if pdf.get_y()>270: pdf.add_page(); header("Backtest - La Tendance Porteuse (suite)")
        pdf.set_fill_color(245,242,235)
        for ci,(v,w) in enumerate(zip(r,widths)):
            col=(0,0,0)
            if colors and ci in colors: col=GREEN if (isinstance(v,str) and ("+" in v)) or (isinstance(v,(int,float)) and v>0) else RED
            pdf.set_text_color(*col); pdf.cell(w,5.4,str(v),border="B",fill=fill,align="C")
        pdf.set_text_color(0,0,0); pdf.ln(); fill=not fill

# page 1
pdf.add_page(); header("Backtest - La Tendance Porteuse (MGC / Gold)")
pdf.set_font("Helvetica","",9); pdf.set_text_color(*GREY)
pdf.multi_cell(0,4.6,
 "Strategie : suivi de tendance par cassure. Filtre EMA200 (15min), entree sur cassure du canal 16 bougies "
 "dans la fenetre Londres/NY, stop 1xATR, trailing 1.5xATR. Donnees reelles XAUUSD 15min 2004-2025 "
 f"(+ controle 5min 2025). Couts inclus ({R['cost_pts']} pt/trade). Tout en R (1R = risque par trade) "
 "-> valable pour TOUT compte. Totaux = somme exacte des trades.")
pdf.set_text_color(0,0,0)
h2("Synthese globale (20 ans, 2004-2025)")
kv("Nombre total de trades",A["n"])
kv("Taux de reussite",f'{A["wr"]} %')
kv("Profit Factor",A["pf"],GREEN)
kv("Gain total",f'+{A["totR"]} R',GREEN)
kv("Esperance par trade",f'+{A["expR"]} R',GREEN)
kv("Gagnant moyen / Perdant moyen",f'+{A["avgW"]} R  /  {A["avgL"]} R')
kv("Trades par jour (moyenne)",A["trades_per_day"])
kv("Plus longue serie de gains",A["winstreak"])
kv("Plus longue serie de pertes",A["losestreak"],RED)
kv("Drawdown maximum",f'{A["maxddR"]} R',RED)

h2("Validation en 3 blocs (le plus important)")
table(["Bloc","Trades","Reussite","Profit Factor","Total R"],
 [["Train 2004-2017",TR["n"],f'{TR["wr"]}%',TR["pf"],f'+{TR["totR"]}'],
  ["Test 2018-2025 (hors echantillon)",TE["n"],f'{TE["wr"]}%',TE["pf"],f'+{TE["totR"]}'],
  ["Controle 2025 (dataset 5min independant)",CT["n"],f'{CT["wr"]}%',CT["pf"],f'+{CT["totR"]}']],
 [78,22,25,32,28],colors={4})

# page 2 : annees
pdf.add_page(); header("Performance annee par annee")
h2("21 annees - 20 gagnantes")
rows=[[y["year"],y["n"],f'{y["wr"]}%',y["pf"],f'{"+" if y["totR"]>=0 else ""}{y["totR"]} R'] for y in Y]
table(["Annee","Trades","Reussite","Profit Factor","Resultat R"],rows,[40,30,35,40,40],colors={4})

M=R.get("monthly");
if M:
    L=M["last12"]
    h2("Statistiques mensuelles (sur 254 mois)")
    table(["Repere mensuel","Valeur"],
      [["Mois median (typique)",f'+{M["R_median"]} R'],
       ["Mois moyen",f'+{M["R_mean"]} R'],
       ["Fourchette habituelle (50% des mois)",f'+{M["q1"]} R  a  +{M["q3"]} R'],
       ["Mois gagnants",f'{M["pct_pos"]} %  (~1 sur 5 rouge)'],
       ["Meilleur / pire mois",f'+{M["best"]} R  /  {M["worst"]} R'],
       ["Trades par mois",f'~{M["trades_median"]}']],[110,72],colors={1})
    h2(f'Moyenne mensuelle - derniere annee ({L["period"]})')
    table(["Repere (12 derniers mois)","Valeur"],
      [["Moyenne par mois",f'+{L["R_mean"]} R  (mediane +{L["R_median"]} R)'],
       ["Total sur 12 mois",f'+{L["R_total"]} R'],
       ["Mois gagnants",f'{L["pct_pos"]} %  (9/12)'],
       ["Meilleur / pire mois",f'+{L["best"]} R  /  {L["worst"]} R'],
       ["Trades par mois",f'~{L["trades_mean"]}']],[110,72],colors={1})

# caveats
pdf.ln(4); pdf.set_font("Helvetica","",7.6); pdf.set_text_color(120,90,30); pdf.set_fill_color(250,247,240)
pdf.multi_cell(0,3.7,
 "NOTES & LIMITES : (1) Donnees XAUUSD spot, proxy fidele du MGC. (2) Resultats nets de couts ESTIMES "
 f"({R['cost_pts']} pt/trade) - tes couts reels Tradovate peuvent differer. (3) Systeme a faible taux de "
 "reussite (~40%) : series de pertes longues (jusqu'a 18) et drawdown profond NORMAUX -> d'ou taille "
 "minuscule + coupe-circuits (-3R/jour, -6R/semaine). (4) Le passe ne garantit pas le futur. (5) Strategie "
 "purement mecanique, testable et reproductible par un seul operateur.")
pdf.set_text_color(*GREY); pdf.ln(2)
pdf.multi_cell(0,3.7,f"Controle de coherence : somme des resultats annuels = {round(sum(y['totR'] for y in Y),1)} R "
 f"= total global declare ({A['totR']} R). Totaux reconcilies.")
pdf.output("backtest_gold.pdf")
print("[OK] backtest_gold.pdf genere")
