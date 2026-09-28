#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verifier.py — contrôle qualité automatique d'un document avant publication.

    python3 Semestre1/outils/verifier.py <fichier.md>

Erreurs bloquantes (code de sortie 1) :
  encadrés « ::: » non équilibrés ou de type inconnu · carte sans séparateur « -- » unique ·
  ligne de tableau irrégulière · en-tête de tableau vide · « $ » impair sur une ligne ·
  figure introuvable · (cours) section obligatoire absente · (cours) trou de numérotation
  dans le tableau de couverture.
Informations : nombre de cartes, de formules, de termes de glossaire, bilan ✔ / ⚠ / ✖.
"""
import os
import re
import sys

CONNUS = {"definition", "formule", "demo", "exemple", "piege", "examen", "methode",
          "correction", "marche", "synthese", "objectif", "carte"}
SECTIONS_COURS = [r"^# 1 — Carte du chapitre", r"^# 2 — Le cours reconstruit",
                  r"^# 3 — Points de vigilance", r"^# 4 — Ancrage mémoriel",
                  r"^## 4\.1 — Fiche de synthèse", r"^## 4\.2 — Cartes de révision",
                  r"^## 4\.3 — Moyens mnémotechniques", r"^## 4\.4 — Le schéma qui relie tout",
                  r"^# 5 — Entraînement", r"^## Niveau 1\b", r"^## Niveau 2\b", r"^## Niveau 3\b",
                  r"^## Niveau 4\b", r"^# 6 — Auto-évaluation", r"^# 7 — Révision en marchant",
                  r"^# Annexe A — Glossaire du chapitre", r"^# Annexe B — Tableau de couverture"]


def main():
    chemin = sys.argv[1]
    L = open(chemin, encoding="utf-8").read().split("\n")
    err, info = [], []
    dossier = os.path.dirname(os.path.abspath(chemin))

    prof, pile = 0, []
    for i, l in enumerate(L, 1):
        s = l.strip()
        if s.startswith(":::"):
            r = s[3:].strip()
            if r:
                t = r.split()[0].lower()
                if t not in CONNUS:
                    err.append("L%d : type d'encadré inconnu « %s »" % (i, t))
                prof += 1
                pile.append(i)
            else:
                prof -= 1
                if prof < 0:
                    err.append("L%d : « ::: » fermant en trop" % i)
                    prof = 0
                else:
                    pile.pop()
    if prof:
        err.append("encadré(s) non fermé(s), ouverts aux lignes %s" % pile)

    i, cartes = 0, 0
    while i < len(L):
        if re.match(r"^\s*:::\s*carte\b", L[i]):
            cartes += 1
            j, d, sep = i + 1, 1, 0
            while j < len(L):
                s = L[j].strip()
                if s.startswith(":::"):
                    d += 1 if s[3:].strip() else -1
                    if d == 0:
                        break
                if s == "--" and d == 1:
                    sep += 1
                j += 1
            if sep != 1:
                err.append("L%d : carte avec %d séparateur(s) « -- »" % (i + 1, sep))
            i = j
        i += 1

    enbloc = False
    i = 0
    while i < len(L):
        if L[i].strip().startswith("```"):
            enbloc = not enbloc
        if (not enbloc and L[i].strip().startswith("|") and i + 1 < len(L)
                and re.match(r"^\s*\|[\s:\-|]+\|\s*$", L[i + 1])):
            n = len(re.findall(r"(?<!\\)\|", L[i]))
            if re.match(r"^\s*\|(\s*\|)+\s*$", L[i]):
                err.append("L%d : en-tête de tableau vide" % (i + 1))
            j = i
            while j < len(L) and L[j].strip().startswith("|"):
                k = len(re.findall(r"(?<!\\)\|", L[j]))
                if k != n:
                    err.append("L%d : ligne de tableau irrégulière (%d « | » au lieu de %d)" % (j + 1, k, n))
                j += 1
            i = j
            continue
        i += 1

    enbloc = False
    for i, l in enumerate(L, 1):
        if l.strip().startswith("```"):
            enbloc = not enbloc
            continue
        if enbloc or l.strip().startswith("$$"):
            continue
        if len(re.findall(r"(?<!\\)\$", l)) % 2:
            err.append("L%d : nombre impair de « $ » (formule coupée sur deux lignes ?)" % i)
        m = re.match(r"^!\[.*?\]\(([^)\s]+)\)\s*$", l.strip())
        if m and not os.path.isfile(os.path.join(dossier, m.group(1))):
            err.append("L%d : figure introuvable « %s »" % (i, m.group(1)))

    if "/Cours/" in os.path.abspath(chemin).replace("\\", "/"):
        texte = "\n".join(L)
        for motif in SECTIONS_COURS:
            if not re.search(motif, texte, re.M):
                err.append("section obligatoire absente : %s" % motif.replace("^", "").replace("\\", ""))
        # couverture : numérotation continue
        m = re.search(r"^# Annexe B — Tableau de couverture.*?$(.*)", texte, re.M | re.S)
        if m:
            nums = [int(x) for x in re.findall(r"^\|\s*\**(\d+)\**\s*\|", m.group(1), re.M)]
            if nums:
                attendu = list(range(1, max(nums) + 1))
                manquants = sorted(set(attendu) - set(nums))
                if manquants:
                    err.append("couverture : numéros absents %s" % manquants)
                zone = m.group(1)
                info.append("couverture : %d lignes · ✔ %d · ⚠ %d · ✖ %d" % (
                    len(nums),
                    len(re.findall(r"^\|[^\n]*\|\s*\**✔\**\s*\|", zone, re.M)),
                    len(re.findall(r"^\|[^\n]*\|\s*\**⚠\**\s*\|", zone, re.M)),
                    len(re.findall(r"^\|[^\n]*\|\s*\**✖\**\s*\|", zone, re.M))))
        info.append("formules : %d" % len(re.findall(r"^\s*:::\s*formule\b", texte, re.M)))
        g = re.search(r"^# Annexe A — Glossaire du chapitre.*?$(.*?)^# ", texte, re.M | re.S)
        if g:
            info.append("glossaire : %d termes" % max(0, len([x for x in g.group(1).splitlines() if x.strip().startswith("|")]) - 2))
    info.insert(0, "cartes : %d" % cartes)

    nom = os.path.basename(chemin)
    for x in info:
        print("  %s — %s" % (nom, x))
    if err:
        print("ÉCHEC DU CONTRÔLE — %s : %d erreur(s)" % (nom, len(err)))
        for e in err:
            print("  - " + e)
        sys.exit(1)
    print("  %s — contrôle OK" % nom)


if __name__ == "__main__":
    main()
