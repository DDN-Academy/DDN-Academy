#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extraire.py — dérive d'un cours reconstruit tout ce qui doit en découler.

    python3 Semestre1/outils/extraire.py Semestre1/<Matiere>/Cours/<cours>.md

Le cours est l'unique source de vérité. Ce script (ré)écrit, et affiche un chemin par ligne :
  1. <Matiere>/Anki/<cours>.csv            toutes les cartes « ::: carte » du cours
  2. <Matiere>/Fiches/<cours>_Fiche.md      la section « 4.1 — Fiche de synthèse »
                                            + la section « 7 — Révision en marchant »
  3. <Matiere>/Fiches/<Matiere>_Formulaire.md   tous les encadrés « ::: formule » de tous
                                            les cours de la matière, dans l'ordre des chapitres
  4. Semestre1/GLOSSAIRE.md                 les tableaux « Annexe A — Glossaire du chapitre »
                                            de tous les cours de toutes les matières

Conventions attendues dans un cours (voir Semestre1/outils/MODELE_COURS.md) :
  en-tête   matiere, code, chapitre, titre …
  titres    « # 4 — Ancrage mémoriel », « ## 4.1 — Fiche de synthèse »,
            « # 7 — Révision en marchant », « # Annexe A — Glossaire du chapitre »
"""
import csv
import glob
import io
import os
import re
import sys
import unicodedata

ICI = os.path.dirname(os.path.abspath(__file__))
SEMESTRE = os.path.dirname(ICI)


def lire(chemin):
    with open(chemin, encoding="utf-8") as f:
        return f.read()


def entete(texte):
    meta, corps = {}, texte
    l = texte.splitlines()
    if l and l[0].strip() == "---":
        for k, ligne in enumerate(l[1:], 1):
            if ligne.strip() == "---":
                corps = "\n".join(l[k + 1:])
                break
            m = re.match(r"^([A-Za-z_]+)\s*:\s*(.*)$", ligne)
            if m:
                meta[m.group(1).lower()] = m.group(2).strip()
    return meta, corps


def section(corps, titre_regex, niveau):
    """Contenu d'une section de titre donné, jusqu'au prochain titre de niveau <= niveau."""
    lignes = corps.splitlines()
    debut = None
    for i, l in enumerate(lignes):
        m = re.match(r"^(#{1,6})\s+(.*)$", l)
        if m and len(m.group(1)) == niveau and re.search(titre_regex, m.group(2)):
            debut = i + 1
            continue
        if debut is not None and m and len(m.group(1)) <= niveau:
            return "\n".join(lignes[debut:i]).strip("\n")
    return "\n".join(lignes[debut:]).strip("\n") if debut is not None else ""


def encadres(corps, type_):
    """Liste (titre, corps) des encadrés ::: type_ (imbrication gérée)."""
    res, lignes, i = [], corps.splitlines(), 0
    while i < len(lignes):
        m = re.match(r"^\s*:::\s*([A-Za-z]+)\s*(.*)$", lignes[i])
        if m and m.group(1).lower() == type_:
            titre, prof, contenu, i = m.group(2).strip(), 1, [], i + 1
            while i < len(lignes):
                t = lignes[i].strip()
                if t.startswith(":::"):
                    if re.match(r"^:::\s*[A-Za-z]+", t):
                        prof += 1
                    else:
                        prof -= 1
                        if prof == 0:
                            break
                contenu.append(lignes[i])
                i += 1
            res.append((titre, "\n".join(contenu).strip("\n")))
        i += 1
    return res


# ---------------------------------------------------------------- Anki
def vers_html_anki(txt):
    txt = txt.strip()
    txt = re.sub(r"\$\$(.+?)\$\$", lambda m: r"\[" + m.group(1).strip() + r"\]", txt, flags=re.S)
    txt = re.sub(r"(?<!\\)\$(.+?)(?<!\\)\$", lambda m: r"\(" + m.group(1).strip() + r"\)", txt)
    txt = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", txt, flags=re.S)
    txt = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", txt, flags=re.S)
    txt = re.sub(r"==(.+?)==", r"<u>\1</u>", txt)
    lignes = []
    for l in txt.splitlines():
        l = l.rstrip()
        if re.match(r"^\s*[-*]\s+", l):
            l = "• " + re.sub(r"^\s*[-*]\s+", "", l)
        lignes.append(l)
    return "<br>".join(x for x in lignes if x is not None)


def anki(chemin, meta, corps):
    cartes = []
    for _, c in encadres(corps, "carte"):
        if "\n--\n" not in "\n" + c + "\n":
            continue
        parties = re.split(r"^\s*--\s*$", c, maxsplit=1, flags=re.M)
        cartes.append((vers_html_anki(parties[0]), vers_html_anki(parties[1])))
    dossier = os.path.join(os.path.dirname(os.path.dirname(chemin)), "Anki")
    os.makedirs(dossier, exist_ok=True)
    sortie = os.path.join(dossier, os.path.splitext(os.path.basename(chemin))[0] + ".csv")
    tampon = io.StringIO()
    tampon.write("#separator:Semicolon\n#html:true\n")
    tampon.write("#deck:Semestre1::%s\n" % meta.get("code", "Matiere"))
    tampon.write("#columns:Question;Réponse;Matière;Chapitre\n")
    w = csv.writer(tampon, delimiter=";", quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
    for q, r in cartes:
        w.writerow([q, r, meta.get("matiere", ""), meta.get("chapitre", "")])
    with open(sortie, "w", encoding="utf-8") as f:
        f.write(tampon.getvalue())
    return sortie, len(cartes)


# ---------------------------------------------------------------- Fiche
def fiche(chemin, meta, corps):
    synthese = section(corps, r"^4\.1\b", 2)
    marche = section(corps, r"^7\b", 1)
    dossier = os.path.join(os.path.dirname(os.path.dirname(chemin)), "Fiches")
    os.makedirs(dossier, exist_ok=True)
    base = os.path.splitext(os.path.basename(chemin))[0]
    sortie = os.path.join(dossier, base + "_Fiche.md")
    out = ["---",
           "matiere: %s" % meta.get("matiere", ""),
           "chapitre: %s" % meta.get("chapitre", ""),
           "titre: Fiche — %s" % meta.get("titre", base),
           "sous_titre: La page à savoir par cœur, puis les questions à se poser en marchant",
           "resume: Extraite automatiquement du cours %s. Ne pas modifier ici : corriger le cours, puis republier." % (base + ".md"),
           "date: %s" % meta.get("date", ""),
           "sommaire: non",
           "---", "",
           "# La fiche de synthèse", "", synthese or "*[section 4.1 absente du cours]*", "",
           "<!--saut-->", "",
           "# Révision en marchant", "", marche or "*[section 7 absente du cours]*", ""]
    with open(sortie, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    return sortie


# ---------------------------------------------------------------- Formulaire
def formulaire(chemin, meta):
    dossier_cours = os.path.dirname(chemin)
    matiere_dir = os.path.dirname(dossier_cours)
    code = meta.get("code") or os.path.basename(matiere_dir)
    blocs, total = [], 0
    for c in sorted(glob.glob(os.path.join(dossier_cours, "*.md"))):
        m2, corps2 = entete(lire(c))
        forms = encadres(corps2, "formule")
        if not forms:
            continue
        blocs.append("## %s" % (m2.get("chapitre") or os.path.basename(c)))
        blocs.append("")
        for titre, contenu in forms:
            total += 1
            blocs += ["::: formule %s" % titre, contenu, ":::", ""]
    sortie = os.path.join(matiere_dir, "Fiches", "%s_Formulaire.md" % code)
    out = ["---",
           "matiere: %s" % meta.get("matiere", code),
           "titre: Formulaire cumulatif — %s" % meta.get("matiere", code),
           "sous_titre: Toutes les formules de tous les chapitres, dans l'ordre du cours",
           "resume: Généré automatiquement à partir des encadrés « formule » des cours. %d formule(s)." % total,
           "sommaire: oui",
           "---", ""]
    out += blocs if blocs else ["*Aucune formule dans les cours de cette matière à ce jour.*", ""]
    with open(sortie, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    return sortie


# ---------------------------------------------------------------- Glossaire
def cle_tri(t):
    t = re.sub(r"[*`_]", "", t).strip().lower()
    t = unicodedata.normalize("NFD", t)
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"^(l'|la |le |les |un |une )", "", t)


def cellules(ligne):
    ligne = ligne.strip()
    if ligne.startswith("|"):
        ligne = ligne[1:]
    if ligne.endswith("|"):
        ligne = ligne[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", ligne)]


def glossaire():
    entrees = []
    for c in sorted(glob.glob(os.path.join(SEMESTRE, "*", "Cours", "*.md"))):
        meta, corps = entete(lire(c))
        g = section(corps, r"^Annexe A\b", 1)
        lignes = [l for l in g.splitlines() if l.strip().startswith("|")]
        for l in lignes[2:]:
            cel = cellules(l)
            if len(cel) >= 3 and cel[0]:
                entrees.append((cel[0], cel[1], cel[2], meta.get("matiere", ""), meta.get("chapitre", "")))
    entrees.sort(key=lambda e: cle_tri(e[0]))
    out = ["---",
           "titre: Glossaire cumulatif — Semestre 1",
           "sous_titre: Tous les termes techniques, toutes matières, par ordre alphabétique",
           "resume: Généré automatiquement à partir de l'annexe A de chaque cours. %d terme(s). Ne pas modifier ici : corriger le cours, puis republier." % len(entrees),
           "sommaire: non",
           "---", ""]
    lettre = None
    for terme, simple, acad, mat, chap in entrees:
        l0 = cle_tri(terme)[:1].upper() or "#"
        if l0 != lettre:
            lettre = l0
            out += ["", "## %s" % lettre, "", "| Terme | En une phrase | Définition académique | Où |", "|---|---|---|---|"]
        out.append("| %s | %s | %s | %s — %s |" % (terme, simple, acad, mat, chap))
    if not entrees:
        out.append("*Aucun terme pour l'instant.*")
    sortie = os.path.join(SEMESTRE, "GLOSSAIRE.md")
    with open(sortie, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    return sortie


def main():
    if len(sys.argv) != 2:
        sys.exit("usage : extraire.py <cours.md>")
    chemin = os.path.abspath(sys.argv[1])
    meta, corps = entete(lire(chemin))
    csv_, n = anki(chemin, meta, corps)
    sys.stderr.write("Anki : %d cartes\n" % n)
    print(csv_)
    print(fiche(chemin, meta, corps))
    print(formulaire(chemin, meta))
    print(glossaire())


if __name__ == "__main__":
    main()
