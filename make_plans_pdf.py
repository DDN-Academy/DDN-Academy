#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Plans de risk & money management - parametres reels du trader.
400$/trade, RR 2, 1 trade/jour, 5j/semaine. Tous chiffres issus des simulations."""
from fpdf import FPDF

ACC=50_000; TARGET=2_500; TRAIL=1_500; LOCK=ACC+100
RISK=400; RR=2; WIN=RISK*RR; PIP=1.00; MAXC=30
LOCKBAL=ACC+TRAIL+100   # 51 600 : solde EOD qui verrouille le trailing

GOLD=(190,150,45); DARK=(16,20,28); GREY=(95,105,120)
GREEN=(30,140,95); RED=(195,55,55); LIGHT=(243,243,246); AMBER=(200,140,30)

pdf=FPDF("P","mm","A4"); pdf.set_auto_page_break(True,16)

def header(t,sub=""):
    pdf.add_page(); pdf.set_fill_color(*DARK); pdf.rect(0,0,210,26,"F")
    pdf.set_xy(12,7); pdf.set_text_color(*GOLD); pdf.set_font("Helvetica","B",14); pdf.cell(0,8,t)
    if sub:
        pdf.set_xy(12,15); pdf.set_text_color(160,165,175); pdf.set_font("Helvetica","",9); pdf.cell(0,6,sub)
    pdf.set_xy(12,32); pdf.set_text_color(0,0,0)
def h2(t,c=GOLD):
    pdf.ln(1.5); pdf.set_font("Helvetica","B",11); pdf.set_text_color(*c)
    pdf.cell(0,7,t,new_x="LMARGIN",new_y="NEXT"); pdf.set_text_color(0,0,0)
def body(t,s=9.2):
    pdf.set_font("Helvetica","",s); pdf.set_text_color(35,35,40)
    pdf.multi_cell(0,4.6,t); pdf.ln(1)
def box(title,text,col=DARK,h=22):
    y=pdf.get_y(); pdf.set_fill_color(*col); pdf.rect(12,y,186,h,"F")
    pdf.set_xy(16,y+3.5); pdf.set_text_color(*GOLD); pdf.set_font("Helvetica","B",10); pdf.cell(0,5,title)
    pdf.set_xy(16,y+10); pdf.set_text_color(228,228,233); pdf.set_font("Helvetica","",8.5)
    pdf.multi_cell(178,4.3,text)
    pdf.set_y(y+h+3); pdf.set_text_color(0,0,0)
def table(headers,widths,rows,hl=None):
    pdf.set_font("Helvetica","B",8); pdf.set_fill_color(*DARK); pdf.set_text_color(255,255,255)
    for w,t in zip(widths,headers): pdf.cell(w,7,t,1,0,"C",True)
    pdf.ln(); pdf.set_text_color(0,0,0)
    for i,r in enumerate(rows):
        is_hl = hl is not None and i==hl
        pdf.set_fill_color(*(GOLD if is_hl else (LIGHT if i%2 else (255,255,255))))
        pdf.set_font("Helvetica","B" if is_hl else "",8)
        for w,t in zip(widths,r): pdf.cell(w,6.3,str(t),1,0,"C",True)
        pdf.ln()
    pdf.ln(2)

# ======================= PAGE 1 : RISK MANAGEMENT =======================
header("PLAN DE RISK MANAGEMENT","400 $/trade  -  RR 2  -  1 trade/jour  -  5 jours/semaine")

box("LA SEULE CHOSE A COMPRENDRE AVANT DE CLIQUER",
    "Ton capital n'est pas 50 000 $. C'est 1 500 $. A 400 $ par trade, tu encaisses TROIS pertes "
    "consecutives. La quatrieme (1 600 $) depasse le buffer et tue le compte. Tout ce plan existe "
    "pour t'empecher d'arriver a cette quatrieme perte.",h=20)

h2("REGLE 1 - LA TAILLE DE POSITION")
body("MGC = 10 onces. 1 $ de gold = 10 pips = 10 $ par contrat. Donc 1 pip = 1,00 $ par contrat.")
pdf.set_font("Helvetica","B",13); pdf.set_text_color(*GOLD)
pdf.cell(0,9,"CONTRATS  =  400  /  SL EN PIPS",new_x="LMARGIN",new_y="NEXT",align="C")
pdf.set_text_color(0,0,0)
rows=[]
for sl in (10,15,20,25,30,40,50,60,80,100):
    n=min(MAXC,max(1,int(RISK//(sl*PIP))))
    risk=n*sl*PIP
    rows.append((f"{sl}", f"{sl/10:.1f} $", f"{n}", f"{risk:.0f} $", f"+{risk*RR:.0f} $",
                 "PLAFOND 30" if n==MAXC and RISK//(sl*PIP)>MAXC else ""))
table(["SL pips","SL en $","CONTRATS","Risque","Gain si RR2","Note"],
      [24,24,28,28,32,50],rows)

h2("REGLE 2 - REDUCTION APRES 2 PERTES  (la regle qui te sauve)")
body("Apres DEUX pertes consecutives, tu passes a 200 $ de risque (donc moitie moins de contrats) "
     "jusqu'au prochain trade gagnant. Des que tu gagnes, tu reviens a 400 $.")
table(["Methode","Tu passes","Tu crames"],[86,50,50],
      [("400 $ fixe","69,1 %","27,5 %"),
       ("400 $ puis 200 $ apres 2 pertes","70,0 %","19,7 %")],hl=1)
body("Simulation 40 000 scenarios, 4 semaines, 50 % de gagnants. Tu passes PLUS souvent et tu crames "
     "BEAUCOUP moins. Cette regle ne coute rien, elle rapporte. C'est la seule martingale honnete "
     "qui existe : reduire quand ca va mal, jamais augmenter.")

h2("REGLE 3 - LES ARRETS")
body("1 trade par jour. Pris ou pas pris. Perdu = la journee est finie, tu fermes la plateforme.\n"
     "3 pertes dans la semaine (-1 200 $) = semaine terminee, tu ne retouches pas avant lundi.\n"
     "Pas de setup valide = pas de trade. Une journee sans trade est une journee reussie.")

h2("REGLE 4 - LES INTERDITS")
body("- Jamais plus de 400 $ de risque. Jamais, meme en retard sur l'objectif.\n"
     "- Jamais elargir un stop deja pose. Le resserrer : oui. L'elargir : jamais.\n"
     "- Jamais deux positions ouvertes.\n"
     "- Jamais de trade a moins de 5 minutes d'une news rouge (CPI, NFP, FOMC).\n"
     "- Jamais un deuxieme trade pour se refaire apres une perte.\n"
     "- Jamais monter la taille apres une serie de gains.")

# ======================= PAGE 2 : MONEY MANAGEMENT =======================
header("PLAN DE MONEY MANAGEMENT","Le chemin de 50 000 $ a 52 500 $")

h2("LES DEUX PHASES DU COMPTE")
box("TA PREMIERE MISSION N'EST PAS 2 500 $. ELLE EST 1 600 $.",
    "Le trailing suit ton plus haut solde de cloture et se VERROUILLE definitivement a 50 100 $ "
    "des que tu clotures une journee a 51 600 $. Avant ce seuil tu es mortel. Apres, ton plancher "
    "est fige a 50 100 $ : tu ne peux plus perdre le compte, seulement rendre du profit. "
    "Deux trades gagnants nets et tu changes de monde.",h=24)

table(["PHASE","Solde","Etat","Ce que tu fais"],[30,40,40,76],
      [("1 - DANGER","50 000 -> 51 600","Trailing mobile","400 $, reduction stricte apres 2 pertes"),
       ("2 - SECURISE","51 600 -> 52 500","Plancher 50 100 $","400 $, tu ne peux plus mourir")])

h2("COMBIEN DE GAGNANTS TE FAUT-IL")
body("Gain +800 $, perte -400 $, cible +2 500 $ :")
table(["Duree","Trades","Gagnants requis","Taux requis","Tu passes (a 50%)"],
      [30,26,40,36,54],
      [("2 semaines","10","6 / 10","60 %","44,6 %"),
       ("3 semaines","15","8 / 15","53 %","61,1 %"),
       ("4 semaines","20","9 / 20","45 %","69,1 %"),
       ("6 semaines","30","13 / 30","43 %","71,3 %")],hl=2)

box("LE LEVIER LE PLUS PUISSANT DE TOUT CE PLAN",
    "Passer de 2 a 4 semaines fait tomber le taux de reussite requis de 60 % a 45 %. "
    "A 50 % de gagnants, tes chances montent de 44,6 % a 69,1 %. Tu n'as rien change a ton trading : "
    "tu as juste arrete de courir. Le delai est ton pire ennemi, pas le marche. "
    "Vise 4 semaines. Si ca vient en 2, tant mieux - mais ne trade JAMAIS pour tenir un calendrier.",
    col=(40,30,10),h=26)

h2("REGLE DE CONSISTANCE 40 % - DEJA GAGNEE")
body(f"Ton meilleur jour possible est +800 $. Sur une cible de 2 500 $, cela fait 32 %. "
     f"Tu es sous la limite de 40 % par construction. Ton choix d'un seul trade par jour "
     f"a elimine ce probleme avant qu'il existe. Ne prends jamais deux trades gagnants "
     f"le meme jour : 1 600 $ sur un jour te ferait exploser la regle.")

h2("BUDGET ET RESET")
body(f"Mets {77.99:.2f} $ de cote des maintenant pour le reset. 20 a 28 % des scenarios y passent. "
     f"Ce n'est pas du pessimisme, c'est de la logistique : un reset coute moins cher qu'un "
     f"nouveau challenge, et un pro prevoit toujours sa deuxieme balle.")

# ======================= PAGE 3 : EXECUTION =======================
header("EXECUTION QUOTIDIENNE","La routine qui transforme les probabilites en resultat")

h2("AVANT CHAQUE SESSION - 4 CHIFFRES SUR PAPIER")
body("   Solde actuel              : ______________\n"
     "   Plus haut solde EOD       : ______________\n"
     "   LIGNE DE MORT (EOD-1500)  : ______________\n"
     "   Risque du jour (400/200)  : ______________\n\n"
     "Si tu ne connais pas ta ligne de mort, tu ne cliques pas. C'est non negociable.")

h2("LA SEQUENCE DU TRADE")
body("1. Le setup est-il 100 % conforme a mon plan ? Sinon -> pas de trade, journee finie.\n"
     "2. Je mesure mon SL en pips.\n"
     "3. Contrats = 400 / SL en pips  (ou 200 / SL si je suis a 2 pertes consecutives).\n"
     "4. Je verifie que TP = 2 x SL. Si le TP n'est pas atteignable, je ne prends pas le trade.\n"
     "5. J'entre avec SL ET TP poses simultanement. Bracket complet ou rien.\n"
     "6. Je ne touche plus a rien. Le trade vit ou meurt seul.\n"
     "7. Resultat note dans le journal. Plateforme fermee.")

h2("TES CRENEAUX")
body("12h30-14h et/ou 18h30-20h. Un seul trade par jour, dans l'un des deux. "
     "Si le premier creneau ne donne rien de conforme, tu peux regarder le second. "
     "Si aucun ne donne rien : zero trade, et c'est une bonne journee. "
     "Le systeme ne te paie pas pour cliquer, il te paie pour attendre.")

h2("JOURNAL - 6 COLONNES, 30 SECONDES")
table(["Date","Sens","SL pips","Contrats","Resultat","Plan suivi ?"],
      [30,26,30,30,34,36],
      [("__/__","","","","+800 / -400","OUI / NON"),
       ("__/__","","","","+800 / -400","OUI / NON"),
       ("__/__","","","","+800 / -400","OUI / NON"),
       ("__/__","","","","+800 / -400","OUI / NON")])
body("La derniere colonne est la seule qui compte vraiment. Un trade perdant avec le plan suivi "
     "est un BON trade. Un trade gagnant hors plan est un trade rate - il t'apprend a desobeir, "
     "et c'est ca qui finira par te couter le compte.")

pdf.ln(2)
box("CE QUI SE JOUE VRAIMENT",
    "A 50 % de gagnants sur 4 semaines avec la reduction apres 2 pertes : 70 % de reussite. "
    "Ce chiffre n'est pas gagne par de l'agressivite - il est gagne le jeudi ou tu es a -800 $, "
    "ou tu as deja perdu deux fois, et ou tu passes quand meme a 200 $ au lieu de doubler. "
    "Ce jour-la, seul devant ton ecran, c'est la que ton compte se decide. Pas ailleurs.",h=26)

pdf.output("/home/user/DDN-Academy/PLANS-RISK-MONEY-MANAGEMENT.pdf")
print("PDF genere : PLANS-RISK-MONEY-MANAGEMENT.pdf")

print("\nVERIF TABLE (risque 400$, RR2) :")
for sl in (10,20,40,80,100):
    n=min(MAXC,max(1,int(RISK//(sl*PIP)))); r=n*sl*PIP
    print(f"  SL {sl:>3} pips -> {n:>2} contrats -> risque {r:>5.0f}$ -> gain RR2 +{r*RR:.0f}$")
print(f"\nVERIF VERROU : solde EOD {LOCKBAL} -> seuil {LOCKBAL-TRAIL} = plancher verrouille {LOCK}")
print(f"VERIF CONSISTANCE : meilleur jour {WIN}$ / cible {TARGET}$ = {WIN/TARGET:.0%} (limite 40%)")
