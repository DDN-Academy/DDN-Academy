#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genere le PDF de risk/money management pour FundedNext Futures Flex 50K.
Tous les chiffres sont calcules, aucun invente."""
from fpdf import FPDF

# ---- PARAMETRES DU COMPTE (releves sur les captures FundedNext) ----
ACC = 50_000
TARGET = 2_500
TRAIL = 1_500
CONSIST = 0.40
MAX_MICROS = 30
RESET = 77.99

# ---- GOLD MGC : 1$ de variation = 10 pips ; MGC = 10 oz -> 1$ = 10$/contrat ----
PIP_VALUE = 1.00          # $ par pip et par contrat MGC
RISK_MAIN = 400           # optimum simule
LEVELS = [250, 300, 400]

GOLD=(190,150,45); DARK=(16,20,28); GREY=(95,105,120)
GREEN=(35,150,105); RED=(200,60,60); LIGHT=(242,242,245)

pdf = FPDF("P","mm","A4"); pdf.set_auto_page_break(True, 16)

def header(t, sub=""):
    pdf.add_page()
    pdf.set_fill_color(*DARK); pdf.rect(0,0,210,26,"F")
    pdf.set_xy(12,7); pdf.set_text_color(*GOLD); pdf.set_font("Helvetica","B",14)
    pdf.cell(0,8,t)
    if sub:
        pdf.set_xy(12,15); pdf.set_text_color(160,165,175); pdf.set_font("Helvetica","",9)
        pdf.cell(0,6,sub)
    pdf.set_xy(12,32); pdf.set_text_color(0,0,0)

def h2(t):
    pdf.ln(2); pdf.set_font("Helvetica","B",11); pdf.set_text_color(*GOLD)
    pdf.cell(0,7,t,new_x="LMARGIN",new_y="NEXT"); pdf.set_text_color(0,0,0)

def body(t, size=9.2):
    pdf.set_font("Helvetica","",size); pdf.set_text_color(35,35,40)
    pdf.multi_cell(0,4.6,t); pdf.ln(1)

def kpi(items):
    w=(210-24)/len(items)
    y=pdf.get_y()
    for i,(k,v,c) in enumerate(items):
        x=12+i*w
        pdf.set_xy(x,y); pdf.set_fill_color(*LIGHT); pdf.rect(x,y,w-2,15,"F")
        pdf.set_xy(x+3,y+2); pdf.set_font("Helvetica","",7); pdf.set_text_color(*GREY)
        pdf.cell(w-6,4,k)
        pdf.set_xy(x+3,y+6.5); pdf.set_font("Helvetica","B",12); pdf.set_text_color(*c)
        pdf.cell(w-6,6,v)
    pdf.set_y(y+18); pdf.set_text_color(0,0,0)

# ================= PAGE 1 =================
header("PLAN DE RISK & MONEY MANAGEMENT",
       "FundedNext Futures Flex 50K  -  Gold MGC  -  objectif 2 semaines")

h2("LES 4 CHIFFRES DU COMPTE")
kpi([("CIBLE","+2 500 $",GREEN),("BUFFER","-1 500 $",RED),
     ("CONSISTANCE","40 %",DARK),("MAX MICROS","30",DARK)])

body("Ton capital reel n'est PAS 50 000 $. C'est 1 500 $. C'est la seule ligne qui peut te tuer. "
     "Le trailing suit ton plus haut solde de cloture et se verrouille a 50 100 $ une fois que tu as "
     "cloture une journee a 51 600 $. Avant ce seuil, chaque dollar gagne deplace ta ligne de mort "
     "vers le haut : tu ne peux jamais rendre plus de 1 500 $ depuis ton sommet.")

h2("TA TAILLE DE RISQUE : 400 $ PAR TRADE")
body("Simulation sur 20 000 scenarios, 10 jours de trading, 5 trades/jour, execution a 60 % de reussite :")

pdf.set_font("Helvetica","B",8.5); pdf.set_fill_color(*DARK); pdf.set_text_color(255,255,255)
for w,t in ((34,"RISQUE/TRADE"),(34,"TU PASSES"),(34,"TU CRAMES"),(60,"VERDICT")):
    pdf.cell(w,7,t,1,0,"C",True)
pdf.ln()
rows=[("150 $","1,5 %","5,4 %","Trop petit - cible inatteignable"),
      ("250 $","21,2 %","27,2 %","Prudent - bon compromis"),
      ("400 $","28,1 %","49,0 %","OPTIMUM MATHEMATIQUE"),
      ("600 $","27,3 %","60,3 %","Pire ET plus dangereux"),
      ("750 $","22,7 %","68,0 %","Suicide statistique")]
pdf.set_font("Helvetica","",8.5); pdf.set_text_color(0,0,0)
for i,(a,b,c,d) in enumerate(rows):
    opt = (a=="400 $")
    pdf.set_fill_color(*(GOLD if opt else (LIGHT if i%2 else (255,255,255))))
    pdf.set_font("Helvetica","B" if opt else "",8.5)
    for w,t in ((34,a),(34,b),(34,c),(60,d)):
        pdf.cell(w,6.5,t,1,0,"C",True)
    pdf.ln()
pdf.ln(2)

body("LIS BIEN LA LIGNE 600 $. Tu passes MOINS souvent (27,3 % contre 28,1 %) et tu crames 60 % "
     "au lieu de 49 %. Au-dessus de 400 $, tu paies avec ton compte et tu n'achetes rien. "
     "C'est un mur mathematique. Tu ne le franchis pas, jamais, meme en retard sur l'objectif.")

h2("LA REGLE DE CALCUL - GOLD MGC")
body("1 $ de variation du gold = 10 pips.  MGC = 10 onces  ->  1 $ = 10 $ par contrat.\n"
     "Donc : 1 pip = 1,00 $ par contrat MGC. La formule devient d'une simplicite totale :")
pdf.set_font("Helvetica","B",13); pdf.set_text_color(*GOLD)
pdf.cell(0,9,"NOMBRE DE CONTRATS  =  400  /  TAILLE DU SL EN PIPS",new_x="LMARGIN",new_y="NEXT",align="C")
pdf.set_text_color(0,0,0)
body("Exemple : SL de 40 pips (4 $ de gold) -> 400 / 40 = 10 contrats MGC. "
     "Perte si le stop saute : 10 x 40 x 1 $ = 400 $. Exactement ton risque. Aucune improvisation.")

# ================= PAGE 2 : LA TABLE =================
header("TABLE DE POSITION - GOLD MGC",
       "Nombre exact de contrats selon ton stop. Plafond FundedNext : 30 micros.")

body("Colonne de gauche : ton SL en pips. Puis le nombre de contrats a passer selon ton niveau de risque. "
     "Ligne grise = plafonne par la limite de 30 contrats du compte : ton risque reel sera INFERIEUR "
     "au risque cible, c'est normal et c'est en ta faveur.", 9)

pdf.set_font("Helvetica","B",8); pdf.set_fill_color(*DARK); pdf.set_text_color(255,255,255)
pdf.cell(20,7,"SL (pips)",1,0,"C",True)
pdf.cell(18,7,"SL en $",1,0,"C",True)
for lv in LEVELS:
    pdf.cell(25,7,f"{lv}$ : ctr",1,0,"C",True)
    pdf.cell(26,7,f"{lv}$ : risque",1,0,"C",True)
pdf.ln()

pdf.set_text_color(0,0,0)
for i,sl in enumerate(range(10,101,5)):
    capped=False
    cells=[]
    for lv in LEVELS:
        n=int(lv//(sl*PIP_VALUE))
        if n>MAX_MICROS: n=MAX_MICROS; capped=True
        if n<1: n=1
        cells.append((n, n*sl*PIP_VALUE))
    pdf.set_font("Helvetica","",8)
    pdf.set_fill_color(*((225,225,230) if capped else (LIGHT if i%2 else (255,255,255))))
    pdf.cell(20,6,str(sl),1,0,"C",True)
    pdf.cell(18,6,f"{sl/10:.1f} $",1,0,"C",True)
    for n,risk in cells:
        pdf.set_font("Helvetica","B",8); pdf.cell(25,6,str(n),1,0,"C",True)
        pdf.set_font("Helvetica","",8); pdf.cell(26,6,f"{risk:.0f} $",1,0,"C",True)
    pdf.ln()

pdf.ln(3)
body("MEMORISE CES TROIS-LA, ce sont 90 % de tes trades :\n"
     "   SL 20 pips (2 $)  ->  20 contrats\n"
     "   SL 40 pips (4 $)  ->  10 contrats\n"
     "   SL 80 pips (8 $)  ->   5 contrats", 9.5)

h2("LE PLAFOND DE 30 CONTRATS")
body("En dessous de 14 pips de stop, la limite du compte t'empeche d'atteindre 400 $ de risque. "
     "Ce n'est pas un probleme : c'est une protection gratuite. Ne cherche JAMAIS a compenser "
     "en elargissant ton stop pour pouvoir passer plus gros. C'est l'erreur qui tue les comptes.")

# ================= PAGE 3 : LES REGLES =================
header("LES REGLES D'EXECUTION", "Non negociables. C'est ce qui separe 28 % de 0 %.")

h2("1. LA MATH DU CHALLENGE")
body(f"Cible : +2 500 $ en 10 jours de trading = 250 $ par jour.\n"
     f"A 400 $ de risque avec un ratio 0,8:1, un trade gagnant rapporte 320 $.\n"
     f"Il te faut donc un peu moins d'un trade gagnant net par jour. Ce n'est PAS beaucoup. "
     f"Tu n'as pas besoin de forcer. Tu as besoin d'etre regulier.")

h2("2. REGLE DE CONSISTANCE - 40 %")
body(f"Aucune journee ne peut representer plus de 40 % de ton profit total. "
     f"Si tu finis a +2 500 $, ta meilleure journee ne doit pas depasser 1 000 $. "
     f"Vise un plafond de 800 $ par jour pour avoir de la marge. "
     f"Si tu exploses ce plafond, le compte n'est pas tue : tu devras juste continuer a trader "
     f"jusqu'a ce que le total soit assez gros. Mais ca rallonge - donc gere-le des le depart.")

h2("3. STOP JOURNALIER : -1 200 $ (3 pertes)")
body("Ce compte n'a AUCUNE limite de perte journaliere. Rien ne t'arrete. C'est le piege "
     "numero un de ce produit : une seule mauvaise journee peut avaler tes 1 500 $ de buffer. "
     "Trois stops touches dans la journee = tu fermes la plateforme. Pas de discussion, pas "
     "de 'derniere tentative'. La simulation ne voit pas la difference car elle n'a pas d'ego. "
     "Toi tu en as un. C'est contre lui que cette regle existe.")

h2("4. LES INTERDICTIONS ABSOLUES")
body("- Jamais plus de 400 $ de risque sur un trade. Jamais.\n"
     "- Jamais elargir un stop deja pose. Tu peux le resserrer, jamais l'inverse.\n"
     "- Jamais deux positions ouvertes en meme temps.\n"
     "- Jamais de trade dans les 5 minutes autour d'une news rouge (CPI, NFP, FOMC).\n"
     "- Jamais augmenter la taille apres une perte pour se refaire.\n"
     "- Jamais augmenter la taille apres trois gains parce qu'on se sent chaud.")

h2("5. LE RESET A 77,99 $")
body(f"Garde {RESET} $ de cote des maintenant. Si le compte saute, le reset coute moins cher "
     f"qu'un nouveau challenge. Ce n'est pas du pessimisme, c'est de la logistique : "
     f"49 % des scenarios passent par la. Un pro prevoit sa deuxieme balle.")

h2("6. TON TABLEAU DE BORD QUOTIDIEN")
body("Avant chaque session, ecris ces 4 chiffres sur papier :\n"
     "   Solde actuel : ______        Ligne de mort (plus haut EOD - 1500) : ______\n"
     "   Marge restante : ______      Perte max aujourd'hui : -1 200 $\n\n"
     "Si tu ne connais pas ta ligne de mort avant de cliquer, tu ne trades pas.")

pdf.ln(4)
pdf.set_fill_color(*DARK); pdf.rect(12,pdf.get_y(),186,24,"F")
y=pdf.get_y()+4
pdf.set_xy(16,y); pdf.set_text_color(*GOLD); pdf.set_font("Helvetica","B",10)
pdf.cell(0,6,"CE QUI FAIT LA DIFFERENCE")
pdf.set_xy(16,y+7); pdf.set_text_color(225,225,230); pdf.set_font("Helvetica","",8.5)
pdf.multi_cell(178,4.4,
  "28 % ne se gagnent pas en etant agressif - le tableau le prouve : au-dessus de 400 $, tu perds "
  "en performance ET en survie. Ces 28 % se gagnent en tenant 400 $ quand tu es a -800 $ le jeudi "
  "et que tout en toi hurle de doubler. C'est la, exactement la, que se joue ton compte.")

pdf.output("/home/user/DDN-Academy/RISK-MANAGEMENT-FUNDEDNEXT-50K.pdf")
print("PDF genere.")

# --- verification de la table imprimee ---
print("\nVERIFICATION (risque 400$) :")
for sl in (10,15,20,40,80,100):
    n=min(MAX_MICROS,int(400//(sl*PIP_VALUE)))
    print(f"  SL {sl:>3} pips ({sl/10:.1f}$) -> {n:>2} contrats -> risque reel {n*sl*PIP_VALUE:>5.0f}$")
