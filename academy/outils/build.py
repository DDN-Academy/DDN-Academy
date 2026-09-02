#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build.py — convertit un chapitre écrit en Markdown étendu (syntaxe DDN Academy)
en un fichier HTML autonome, lisible à l'écran et prêt à imprimer en A4.

    python3 academy/outils/build.py academy/chapitres/micro-ch1.md
    python3 academy/outils/build.py fichier.md -o /chemin/sortie.html

Aucune dépendance externe : bibliothèque standard Python uniquement.
Le HTML produit embarque sa feuille de style : il fonctionne hors ligne,
s'envoie par mail, et s'exporte en PDF via Ctrl/Cmd+P -> « Enregistrer en PDF »
(ou via academy/outils/make.sh, qui pilote un navigateur sans interface).

--------------------------------------------------------------------------
SYNTAXE RECONNUE
--------------------------------------------------------------------------
En-tête (facultatif, en tout début de fichier, entre deux lignes « --- ») :
    matiere, chapitre, titre, sous_titre, resume, date, duree, version,
    sommaire (oui/non)

Titres            # (h1) ## (h2) ### (h3) #### (h4)   — h2/h3 alimentent le sommaire
Emphase           **gras**  *italique*  `code`  ==surligné==  [texte](url)
Listes            « - » à puces, « 1. » numérotées, imbrication par 2 espaces
Tableaux          | a | b |  puis  |---|---:|   (« :---: » centre, « ---: » aligne à droite)
Citation          > texte
Filet             ---
Saut de page      <!--saut-->
Maths en ligne    $r = \\frac{P_1 - P_0}{P_0}$
Maths centrées    $$ ... $$  (sur ses propres lignes)

Encadrés :
    ::: definition Élasticité-prix
    contenu…
    :::
Types disponibles : definition, formule, demo, exemple, piege, examen,
methode, correction, marche, synthese, objectif, carte.

Le type « carte » produit une carte de révision ; la question et la réponse
sont séparées par une ligne contenant seulement « -- » :
    ::: carte
    Que mesure l'élasticité-prix de la demande ?
    --
    La sensibilité de la quantité demandée à une variation du prix…
    :::
"""

import argparse
import html as _html
import os
import re
import sys
import unicodedata
from datetime import date

# =========================================================================
#  Symboles mathématiques : nom LaTeX -> caractère
# =========================================================================
SYMBOLES = {
    # minuscules grecques
    "alpha": "α", "beta": "β", "gamma": "γ", "delta": "δ", "epsilon": "ε",
    "varepsilon": "ε", "zeta": "ζ", "eta": "η", "theta": "θ", "vartheta": "ϑ",
    "iota": "ι", "kappa": "κ", "lambda": "λ", "mu": "μ", "nu": "ν", "xi": "ξ",
    "pi": "π", "rho": "ρ", "sigma": "σ", "tau": "τ", "upsilon": "υ",
    "phi": "φ", "varphi": "φ", "chi": "χ", "psi": "ψ", "omega": "ω",
    # majuscules grecques
    "Gamma": "Γ", "Delta": "Δ", "Theta": "Θ", "Lambda": "Λ", "Xi": "Ξ",
    "Pi": "Π", "Sigma": "Σ", "Phi": "Φ", "Psi": "Ψ", "Omega": "Ω",
    # opérateurs et relations
    "times": "×", "div": "÷", "cdot": "·", "pm": "±", "mp": "∓",
    "le": "≤", "leq": "≤", "ge": "≥", "geq": "≥", "ne": "≠", "neq": "≠",
    "approx": "≈", "simeq": "≃", "sim": "∼", "equiv": "≡", "propto": "∝",
    "ll": "≪", "gg": "≫", "infty": "∞", "partial": "∂", "nabla": "∇",
    "sum": "∑", "prod": "∏", "int": "∫", "iint": "∬", "oint": "∮",
    "forall": "∀", "exists": "∃", "nexists": "∄", "in": "∈", "notin": "∉",
    "subset": "⊂", "subseteq": "⊆", "supset": "⊃", "supseteq": "⊇",
    "cup": "∪", "cap": "∩", "setminus": "∖", "emptyset": "∅", "varnothing": "∅",
    "mathbb{R}": "ℝ",
    # flèches
    "rightarrow": "→", "to": "→", "leftarrow": "←", "gets": "←",
    "Rightarrow": "⇒", "implies": "⇒", "Leftarrow": "⇐",
    "leftrightarrow": "↔", "Leftrightarrow": "⇔", "iff": "⇔",
    "mapsto": "↦", "uparrow": "↑", "downarrow": "↓", "nearrow": "↗", "searrow": "↘",
    # divers
    "ldots": "…", "cdots": "⋯", "dots": "…", "prime": "′", "circ": "∘",
    "degree": "°", "deg": "°", "euro": "€", "star": "★", "bullet": "•",
    "langle": "⟨", "rangle": "⟩", "lfloor": "⌊", "rfloor": "⌋",
    "lceil": "⌈", "rceil": "⌉", "perp": "⊥", "angle": "∠", "therefore": "∴",
    "log": "log", "ln": "ln", "exp": "exp", "min": "min", "max": "max",
    "sin": "sin", "cos": "cos", "tan": "tan", "lim": "lim",
}

# relations et opérateurs binaires : l'espace qui les suit est conservé
# (« a \le b » -> « a ≤ b »), contrairement aux lettres grecques (« \Delta Q » -> « ΔQ »)
RELATIONS = {
    "times", "div", "cdot", "pm", "mp", "le", "leq", "ge", "geq", "ne", "neq",
    "approx", "simeq", "sim", "equiv", "propto", "ll", "gg", "in", "notin",
    "subset", "subseteq", "supset", "supseteq", "cup", "cap", "setminus",
    "rightarrow", "to", "leftarrow", "gets", "Rightarrow", "implies", "Leftarrow",
    "leftrightarrow", "Leftrightarrow", "iff", "mapsto", "perp", "therefore",
}

# opérateurs à composer en romain (non italique) à l'intérieur d'une formule
DROITS = set("0123456789+-−=<>()[]{}|/,;:!?%€$ …·×÷±≤≥≠≈≡∝∞∑∏∫→←⇒⇐↔⇔∈∉⊂⊆∪∩∅°'")


# =========================================================================
#  Utilitaires
# =========================================================================
def esc(txt):
    """Échappe le HTML."""
    return _html.escape(txt, quote=False)


def slug(txt):
    """Identifiant d'ancre : sans accent, minuscules, tirets."""
    txt = re.sub(r"<[^>]+>", "", txt)
    txt = unicodedata.normalize("NFKD", txt)
    txt = "".join(c for c in txt if not unicodedata.combining(c))
    txt = re.sub(r"[^A-Za-z0-9]+", "-", txt).strip("-").lower()
    return txt or "section"


def _arg(src, i):
    """Lit l'argument LaTeX qui commence à l'indice i. Retourne (contenu, i_suivant)."""
    while i < len(src) and src[i] == " ":
        i += 1
    if i >= len(src):
        return "", i
    if src[i] == "{":
        prof, j = 0, i
        while j < len(src):
            if src[j] == "{":
                prof += 1
            elif src[j] == "}":
                prof -= 1
                if prof == 0:
                    return src[i + 1:j], j + 1
            j += 1
        return src[i + 1:], len(src)
    return src[i], i + 1


def maths(src):
    """Traduit un sous-ensemble de LaTeX en HTML. L'entrée est déjà échappée."""
    out, i, n = [], 0, len(src)
    tampon = []  # caractères « droits » en attente

    def vider():
        if tampon:
            out.append('<span class="op">%s</span>' % "".join(tampon))
            tampon.clear()

    while i < n:
        # entités HTML issues de l'échappement (&lt; &gt; &amp;)
        m = re.match(r"&[a-zA-Z]+;|&#\d+;", src[i:])
        if m:
            tampon.append(m.group(0))
            i += len(m.group(0))
            continue

        c = src[i]

        if c == "\\":
            m = re.match(r"\\([A-Za-z]+)", src[i:])
            if m:
                nom = m.group(1)
                i += len(m.group(0))
                if nom in ("frac", "dfrac", "tfrac"):
                    a, i = _arg(src, i)
                    b, i = _arg(src, i)
                    vider()
                    out.append('<span class="frac"><span class="num">%s</span>'
                               '<span class="den">%s</span></span>'
                               % (maths(a), maths(b)))
                elif nom == "sqrt":
                    a, i = _arg(src, i)
                    vider()
                    out.append('<span class="rac">&radic;<span class="sous">%s</span></span>'
                               % maths(a))
                elif nom in ("text", "mathrm", "operatorname", "textrm"):
                    a, i = _arg(src, i)
                    vider()
                    out.append('<span class="txt">%s</span>' % a)
                elif nom in ("mathbf", "bm"):
                    a, i = _arg(src, i)
                    vider()
                    out.append("<b>%s</b>" % maths(a))
                elif nom in ("bar", "overline"):
                    a, i = _arg(src, i)
                    vider()
                    out.append('<span style="text-decoration:overline">%s</span>' % maths(a))
                elif nom == "hat":
                    a, i = _arg(src, i)
                    vider()
                    out.append("%s&#770;" % maths(a))
                elif nom == "tilde":
                    a, i = _arg(src, i)
                    vider()
                    out.append("%s&#771;" % maths(a))
                elif nom == "vec":
                    a, i = _arg(src, i)
                    vider()
                    out.append("%s&#8407;" % maths(a))
                elif nom == "mathbb":
                    a, i = _arg(src, i)
                    vider()
                    out.append('<span class="op">%s</span>'
                               % {"R": "ℝ", "N": "ℕ", "Z": "ℤ", "Q": "ℚ", "E": "𝔼"}.get(a, a))
                elif nom in SYMBOLES:
                    tampon.append(SYMBOLES[nom])
                    if nom not in RELATIONS:
                        while i < n and src[i] == " ":  # « \Delta Q » -> « ΔQ »
                            i += 1
                elif nom in ("left", "right", "displaystyle", "limits"):
                    pass
                elif nom in ("quad", "qquad"):
                    tampon.append("&emsp;")
                else:  # commande non gérée : on affiche son nom en romain
                    vider()
                    out.append('<span class="txt">%s</span>' % nom)
                    while i < n and src[i] == " ":
                        i += 1
                continue
            suivant = src[i + 1] if i + 1 < n else ""
            i += 2
            if suivant == ",":
                tampon.append("&thinsp;")
            elif suivant in (" ", ";", ":"):
                tampon.append(" ")
            elif suivant == "!":
                pass
            else:
                tampon.append(suivant)
            continue

        if c in "^_":
            a, i = _arg(src, i + 1)
            vider()
            balise = "sup" if c == "^" else "sub"
            out.append("<%s>%s</%s>" % (balise, maths(a), balise))
            continue

        if c in "{}":
            i += 1
            continue

        if c in DROITS:
            tampon.append("\u2212" if c == "-" else c)  # vrai signe moins
            i += 1
            continue

        vider()
        out.append(c)  # lettre : italique par héritage de .math
        i += 1

    vider()
    return "".join(out)


# =========================================================================
#  Niveau « en ligne »
# =========================================================================
RE_CODE = re.compile(r"(`+)(.+?)\1")
RE_MATH = re.compile(r"(?<!\\)\$(?!\$)([^$\n]+?)\$(?!\d)")
RE_SIGNE_MATH = re.compile(r"[\\^_{}=<>/+\u00d7\u00f7\u2264\u2265\u2260\u2192\u21d2]")
RE_LIEN = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
RE_GRAS = re.compile(r"\*\*(.+?)\*\*", re.S)
RE_ITAL = re.compile(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", re.S)
RE_SURL = re.compile(r"==(.+?)==")
# balises HTML simples tolérées dans le texte source (exposants, indices, retours)
RE_BALISES = re.compile(r"&lt;(/?)(sup|sub|br|small|abbr)&gt;")
RE_AUTOLIEN = re.compile(r"&lt;(https?://[^\s&<>]+)&gt;")


def inline(txt):
    """Applique les transformations « en ligne » à un fragment de texte brut."""
    txt = esc(txt)
    coffre = []

    def garder(html_frag):
        coffre.append(html_frag)
        return "\x00%d\x00" % (len(coffre) - 1)

    txt = RE_CODE.sub(lambda m: garder("<code>%s</code>" % m.group(2).strip()), txt)
    def _math(m):
        contenu = m.group(1).strip()
        # « $ ... $ » n'est pris pour des maths que si le contenu porte un signe
        # mathématique, ou s'il est très court ($Q$, $e_p$). Un montant en dollars
        # écrit au fil du texte reste donc intact.
        if not contenu or not (RE_SIGNE_MATH.search(contenu) or len(contenu) <= 4):
            return m.group(0)
        return garder('<span class="math">%s</span>' % maths(contenu))

    txt = RE_MATH.sub(_math, txt)
    txt = RE_LIEN.sub(lambda m: garder('<a href="%s">%s</a>' % (m.group(2), m.group(1))), txt)
    txt = RE_GRAS.sub(lambda m: "<strong>%s</strong>" % m.group(1), txt)
    txt = RE_SURL.sub(lambda m: "<mark>%s</mark>" % m.group(1), txt)
    txt = RE_ITAL.sub(lambda m: "<em>%s</em>" % m.group(1), txt)
    txt = txt.replace("\\$", "$")
    # quelques balises HTML simples restent utilisables dans le texte source
    txt = RE_BALISES.sub(lambda m: "<%s%s>" % (m.group(1), m.group(2)), txt)
    # liens automatiques : <https://exemple.fr>
    txt = RE_AUTOLIEN.sub(lambda m: '<a href="%s">%s</a>' % (m.group(1), m.group(1)), txt)
    txt = re.sub(r"\x00(\d+)\x00", lambda m: coffre[int(m.group(1))], txt)
    return txt


# =========================================================================
#  Niveau « bloc »
# =========================================================================
RE_TITRE = re.compile(r"^(#{1,4})\s+(.*)$")
RE_ITEM = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")
RE_SEP_TAB = re.compile(r"^\|?[\s:|-]*-[\s:|-]*\|?$")
RE_FILET = re.compile(r"^(-{3,}|\*{3,}|_{3,})$")

ETIQUETTES = {
    "definition": "Définition",
    "formule": "Formule clé",
    "demo": "Démonstration",
    "exemple": "Exemple chiffré",
    "piege": "Piège fréquent",
    "examen": "Point d'examen",
    "methode": "Méthode",
    "correction": "Corrigé",
    "marche": "Analogie — marchés financiers",
    "synthese": "Synthèse",
    "objectif": "Objectifs",
}


class Rendu:
    def __init__(self):
        self.sommaire = []          # (niveau, texte, ancre)
        self._ancres = {}

    # -- ancres uniques ---------------------------------------------------
    def ancre(self, texte):
        base = slug(texte)
        self._ancres[base] = self._ancres.get(base, 0) + 1
        return base if self._ancres[base] == 1 else "%s-%d" % (base, self._ancres[base])

    # -- listes -----------------------------------------------------------
    def _liste(self, lignes):
        items = []
        for ligne in lignes:
            m = RE_ITEM.match(ligne)
            if m:
                items.append([len(m.group(1).expandtabs(4)),
                              bool(re.match(r"\d", m.group(2))),
                              [m.group(3)]])
            elif items and ligne.strip():
                items[-1][2].append(ligne.strip())
        if not items:
            return ""

        def bloc(pos, niveau):
            ordonnee = items[pos][1]
            balise = "ol" if ordonnee else "ul"
            morceaux = ["<%s>" % balise]
            while pos < len(items):
                indent, ord_i, contenu = items[pos]
                if indent < niveau:
                    break
                if indent > niveau:
                    sous, pos = bloc(pos, indent)
                    if len(morceaux) > 1 and morceaux[-1].endswith("</li>"):
                        morceaux[-1] = morceaux[-1][:-5] + sous + "</li>"
                    else:
                        morceaux.append("<li>%s</li>" % sous)
                    continue
                if ord_i != ordonnee:
                    break
                texte = " ".join(contenu).strip()
                m_case = re.match(r"^\[( |x|X)\]\s+(.*)$", texte)
                if m_case:
                    coche = "cochee" if m_case.group(1).lower() == "x" else "vide"
                    morceaux.append('<li class="tache %s">%s</li>'
                                    % (coche, inline(m_case.group(2))))
                else:
                    morceaux.append("<li>%s</li>" % inline(texte))
                pos += 1
            morceaux.append("</%s>" % balise)
            return "".join(morceaux), pos

        html_liste, _ = bloc(0, items[0][0])
        return html_liste

    # -- tableaux ---------------------------------------------------------
    def _tableau(self, lignes):
        def cellules(ligne):
            ligne = ligne.strip()
            # les tubes situés dans un fragment de code ne séparent pas les colonnes
            ligne = re.sub(
                r"(`+)(.+?)\1",
                lambda m: m.group(1)
                + m.group(2).replace("\\|", "\x01").replace("|", "\x01")
                + m.group(1),
                ligne)
            if ligne.startswith("|"):
                ligne = ligne[1:]
            if ligne.endswith("|") and not ligne.endswith("\\|"):
                ligne = ligne[:-1]
            return [c.strip().replace("\\|", "|").replace("\x01", "|")
                    for c in re.split(r"(?<!\\)\|", ligne)]

        entete = cellules(lignes[0])
        aligns = []
        for spec in cellules(lignes[1]):
            spec = spec.strip()
            if spec.startswith(":") and spec.endswith(":"):
                aligns.append(" class=\"c\"")
            elif spec.endswith(":"):
                aligns.append(" class=\"r\"")
            else:
                aligns.append("")
        while len(aligns) < len(entete):
            aligns.append("")

        out = ["<table><thead><tr>"]
        for j, c in enumerate(entete):
            out.append("<th%s>%s</th>" % (aligns[j], inline(c)))
        out.append("</tr></thead><tbody>")
        for ligne in lignes[2:]:
            cs = cellules(ligne)
            out.append("<tr>")
            for j, c in enumerate(cs):
                a = aligns[j] if j < len(aligns) else ""
                out.append("<td%s>%s</td>" % (a, inline(c)))
            out.append("</tr>")
        out.append("</tbody></table>")
        return "".join(out)

    # -- encadrés ---------------------------------------------------------
    def _encadre(self, type_, titre, corps):
        if type_ == "carte":
            if "--" in [l.strip() for l in corps]:
                coupe = [l.strip() for l in corps].index("--")
                q, r = corps[:coupe], corps[coupe + 1:]
            else:
                q, r = corps[:1], corps[1:]
            return ('<div class="carte"><div class="q">%s</div><div class="r">%s</div></div>'
                    % (self.blocs(q), self.blocs(r)))
        etiquette = esc(ETIQUETTES.get(type_, type_.capitalize()))
        if titre:
            etiquette = "%s — %s" % (etiquette, inline(titre))
        return ('<div class="bloc %s"><span class="etiquette">%s</span>%s</div>'
                % (type_, etiquette, self.blocs(corps)))

    # -- boucle principale -------------------------------------------------
    def blocs(self, lignes):
        out = []
        i, n = 0, len(lignes)
        while i < n:
            brute = lignes[i]
            s = brute.strip()

            if not s:
                i += 1
                continue

            # saut de page
            if re.fullmatch(r"<!--\s*saut\s*-->", s):
                out.append('<div class="saut"></div>')
                i += 1
                continue

            # commentaire HTML sur une ligne : ignoré
            if s.startswith("<!--") and s.endswith("-->"):
                i += 1
                continue

            # encadré :::
            if s.startswith(":::"):
                m = re.match(r"^:::\s*([A-Za-z]+)\s*(.*)$", s)
                if m:
                    type_, titre = m.group(1).lower(), m.group(2).strip()
                    prof, corps, i = 1, [], i + 1
                    while i < n:
                        t = lignes[i].strip()
                        if t.startswith(":::"):
                            if re.match(r"^:::\s*[A-Za-z]+", t):
                                prof += 1
                                corps.append(lignes[i])
                            else:
                                prof -= 1
                                if prof == 0:
                                    i += 1
                                    break
                                corps.append(lignes[i])
                        else:
                            corps.append(lignes[i])
                        i += 1
                    out.append(self._encadre(type_, titre, corps))
                    continue
                i += 1
                continue

            # bloc de code
            if s.startswith("```"):
                corps, i = [], i + 1
                while i < n and not lignes[i].strip().startswith("```"):
                    corps.append(lignes[i])
                    i += 1
                i += 1
                out.append("<pre><code>%s</code></pre>" % esc("\n".join(corps)))
                continue

            # maths centrées
            if s.startswith("$$"):
                reste = s[2:].strip()
                if reste.endswith("$$") and len(reste) > 2:
                    corps = [reste[:-2]]
                    i += 1
                else:
                    corps = [reste] if reste else []
                    i += 1
                    while i < n and not lignes[i].strip().startswith("$$"):
                        corps.append(lignes[i].strip())
                        i += 1
                    i += 1
                expr = " ".join(x for x in corps if x)
                out.append('<div class="math math-display">%s</div>' % maths(esc(expr)))
                continue

            # titres
            m = RE_TITRE.match(s)
            if m:
                niveau, texte = len(m.group(1)), m.group(2).strip()
                contenu = inline(texte)
                if niveau in (2, 3):
                    a = self.ancre(texte)
                    self.sommaire.append((niveau, contenu, a))
                    out.append('<h%d id="%s">%s</h%d>' % (niveau, a, contenu, niveau))
                else:
                    out.append("<h%d>%s</h%d>" % (niveau, contenu, niveau))
                i += 1
                continue

            # filet horizontal
            if RE_FILET.fullmatch(s):
                out.append("<hr>")
                i += 1
                continue

            # tableau
            if "|" in s and i + 1 < n and RE_SEP_TAB.fullmatch(lignes[i + 1].strip()) \
               and "-" in lignes[i + 1]:
                bloc_tab = [lignes[i], lignes[i + 1]]
                i += 2
                while i < n and "|" in lignes[i] and lignes[i].strip():
                    bloc_tab.append(lignes[i])
                    i += 1
                out.append(self._tableau(bloc_tab))
                continue

            # citation
            if s.startswith(">"):
                corps = []
                while i < n and lignes[i].strip().startswith(">"):
                    corps.append(re.sub(r"^\s*>\s?", "", lignes[i]))
                    i += 1
                out.append("<blockquote>%s</blockquote>" % self.blocs(corps))
                continue

            # liste
            if RE_ITEM.match(brute):
                corps = []
                while i < n:
                    l = lignes[i]
                    if l.strip() == "":
                        j = i + 1
                        if j < n and (RE_ITEM.match(lignes[j]) or lignes[j].startswith(("  ", "\t"))):
                            corps.append("")
                            i += 1
                            continue
                        break
                    if RE_ITEM.match(l) or l.startswith(("  ", "\t")):
                        corps.append(l)
                        i += 1
                        continue
                    break
                out.append(self._liste(corps))
                continue

            # paragraphe
            corps = []
            while i < n:
                l = lignes[i]
                t = l.strip()
                if not t or t.startswith((":::", "```", ">", "#", "$$", "<!--")) \
                   or RE_ITEM.match(l) or RE_FILET.fullmatch(t):
                    break
                if "|" in t and i + 1 < n and RE_SEP_TAB.fullmatch(lignes[i + 1].strip()) \
                   and "-" in lignes[i + 1]:
                    break
                corps.append(t)
                i += 1
            if corps:
                out.append("<p>%s</p>" % inline(" ".join(corps)))
        return "".join(out)


# =========================================================================
#  En-tête, couverture, sommaire, assemblage
# =========================================================================
def lire_entete(texte):
    """Extrait l'en-tête « --- clé: valeur --- » s'il est présent."""
    meta = {}
    lignes = texte.splitlines()
    if lignes and lignes[0].strip() == "---":
        for k, ligne in enumerate(lignes[1:], start=1):
            if ligne.strip() == "---":
                return meta, "\n".join(lignes[k + 1:])
            m = re.match(r"^([A-Za-z_]+)\s*:\s*(.*)$", ligne)
            if m:
                meta[m.group(1).lower()] = m.group(2).strip().strip('"').strip("'")
    return meta, texte


MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
        "août", "septembre", "octobre", "novembre", "décembre"]


def couverture(meta):
    aujourdhui = date.today()
    d = meta.get("date") or "%d %s %d" % (aujourdhui.day, MOIS[aujourdhui.month - 1], aujourdhui.year)
    lignes = ['<section class="couverture">', '<div class="filet-haut"></div>']
    if meta.get("matiere"):
        lignes.append('<div class="matiere">%s</div>' % esc(meta["matiere"]))
    if meta.get("chapitre"):
        lignes.append('<div class="chapitre">%s</div>' % esc(meta["chapitre"]))
    lignes.append("<h1>%s</h1>" % inline(meta.get("titre", "Chapitre")))
    if meta.get("sous_titre"):
        lignes.append('<div class="sous-titre">%s</div>' % inline(meta["sous_titre"]))
    if meta.get("resume"):
        lignes.append('<div class="resume">%s</div>' % inline(meta["resume"]))
    meta_items = ['<span><b>Date</b> · %s</span>' % esc(d)]
    if meta.get("duree"):
        meta_items.append('<span><b>Travail estimé</b> · %s</span>' % esc(meta["duree"]))
    if meta.get("niveau"):
        meta_items.append('<span><b>Niveau</b> · %s</span>' % esc(meta["niveau"]))
    if meta.get("version"):
        meta_items.append('<span><b>Version</b> · %s</span>' % esc(meta["version"]))
    lignes.append('<div class="meta">%s</div>' % "".join(meta_items))
    lignes.append('<div class="avertissement">Document de travail autonome — il remplace '
                  'le support de cours original, qu\'il n\'est pas nécessaire de relire. '
                  'Toute notion évoquée dans le cours y est définie, démontrée et illustrée.</div>')
    lignes.append("</section>")
    return "".join(lignes)


def sommaire_html(entrees):
    if not entrees:
        return ""
    out = ['<nav class="sommaire"><h2>Sommaire</h2><ol>']
    for niveau, texte, ancre in entrees:
        out.append('<li class="n%d"><a href="#%s">%s</a></li>' % (niveau, ancre, texte))
    out.append("</ol></nav>")
    return "".join(out)


GABARIT = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titre}</title>
<style>
{css}
</style>
</head>
<body>
<div class="bandeau">DDN Academy — {matiere} &nbsp;·&nbsp; <b>Ctrl / Cmd + P → Enregistrer en PDF</b></div>
<main class="feuille">
{couverture}
{sommaire}
{corps}
</main>
</body>
</html>
"""


def construire(chemin_md, chemin_css=None):
    with open(chemin_md, encoding="utf-8") as f:
        texte = f.read()
    meta, corps_md = lire_entete(texte)

    if not meta.get("titre"):
        m = re.search(r"^#\s+(.*)$", corps_md, re.M)
        meta["titre"] = m.group(1).strip() if m else os.path.basename(chemin_md)

    rendu = Rendu()
    corps = rendu.blocs(corps_md.splitlines())

    chemin_css = chemin_css or os.path.join(os.path.dirname(os.path.abspath(__file__)), "theme.css")
    with open(chemin_css, encoding="utf-8") as f:
        css = f.read()

    veut_sommaire = meta.get("sommaire", "oui").lower() not in ("non", "no", "false", "0")
    return GABARIT.format(
        titre=esc(re.sub(r"<[^>]+>", "", meta["titre"])),
        matiere=esc(meta.get("matiere", "Économie · Gestion · Finance")),
        css=css,
        couverture=couverture(meta),
        sommaire=sommaire_html(rendu.sommaire) if veut_sommaire else "",
        corps=corps,
    )


def main():
    p = argparse.ArgumentParser(description="Chapitre Markdown -> HTML prêt à imprimer.")
    p.add_argument("source", help="fichier .md du chapitre")
    p.add_argument("-o", "--sortie", help="fichier .html de destination")
    p.add_argument("--css", help="feuille de style à utiliser")
    args = p.parse_args()

    if not os.path.isfile(args.source):
        sys.exit("Fichier introuvable : %s" % args.source)

    sortie = args.sortie
    if not sortie:
        racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        base = os.path.splitext(os.path.basename(args.source))[0] + ".html"
        sortie = os.path.join(racine, "export", base)
    os.makedirs(os.path.dirname(os.path.abspath(sortie)), exist_ok=True)

    with open(sortie, "w", encoding="utf-8") as f:
        f.write(construire(args.source, args.css))
    print(sortie)


if __name__ == "__main__":
    main()
