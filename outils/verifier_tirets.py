#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vérifie que rien de ce qui se publie ne porte de tiret cadratin (CLAUDE.md, § 2, « Le contenu »).

    python3 outils/verifier_tirets.py              # code 1 s'il en reste
    python3 outils/verifier_tirets.py --tous       # chaque extrait, pas seulement les premiers de chaque fichier
    python3 outils/verifier_tirets.py --dossier X  # un autre dossier que site/ (un cours rangé autrement)

Cherche le tiret cadratin (« — », et ses entités &mdash; et &#8212;) et le tiret demi-cadratin entre deux espaces
(« – », qui en tient lieu) dans tout ce que l'apprenant lit : le texte des pages de site/ et de leurs jumelles
anglaises, les chaînes de leurs scripts (données des composants, transcriptions des capsules, libellés de
ui-labels.js, glossaire, flashcards, QCM), les `content:` des feuilles de style. Ne compte pas ce que personne ne lit :
les commentaires HTML, JavaScript et CSS. Le signe moins (−) et le tiret demi-cadratin collé entre deux nombres
(« 10–20 ») restent permis. Les fichiers secrets ne sont jamais ouverts.

Repris, en générique, du cours d'étude d'avant-projet (EADL et ERIS), où l'auteur a demandé le 3 novembre 2026 de ne
plus voir « les tirets cadratins et les autres caractéristiques de textes générés par IA » ; les autres marques
(phrases-chocs sans verbe, antithèses réflexes, triades par habitude…) ne se mesurent pas : elles se relisent.
"""
import argparse
import glob
import io
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRETS = {"elevenlabs.json", "config.json", "acces.json", "acces-zones.json", "known_hosts"}
TIRET = re.compile(r"—|&mdash;|&#8212;|&#x2014;|(?<=\s)–(?=\s)")

for flux in (sys.stdout, sys.stderr):
    try:
        flux.reconfigure(encoding="utf-8")
    except Exception:
        pass


# Après ces caractères (ou ces mots), une barre oblique ouvre une expression régulière, pas une division.
AVANT_REGEX = set("(,=:[!&|?{};+-*%<>~^")
MOTS_REGEX = ("return", "typeof", "case", "do", "else", "in", "of", "void", "yield", "await")
CONSOLE = re.compile(r"console\.\w+\(\s*$")


def _fin_regex(src, i):
    """L'indice qui suit l'expression régulière ouverte en i (sa barre de fin, puis ses drapeaux) : une classe […]
    peut contenir une barre ; un échappement saute le caractère suivant."""
    j, n, classe = i + 1, len(src), False
    while j < n and src[j] != "\n":
        if src[j] == "\\":
            j += 2
            continue
        if src[j] == "[":
            classe = True
        elif src[j] == "]":
            classe = False
        elif src[j] == "/" and not classe:
            j += 1
            while j < n and src[j].isalpha():
                j += 1
            return j
        j += 1
    return j


def morceaux_js(src):
    """Le code JavaScript découpé en [(genre, texte)] : 'commentaire', 'chaine', 'console' (une chaîne passée à
    console.log, que l'apprenant ne voit pas) ou 'code', par un petit lexeur qui connaît les chaînes '…', "…", `…`, les
    deux formes de commentaire et les expressions régulières (une barre oblique qui suit un opérateur, une
    parenthèse ou un mot comme return), dont un guillemet n'ouvre aucune chaîne."""
    out, i, n, debut = [], 0, len(src), 0
    while i < n:
        c = src[i]
        if src.startswith("//", i) or src.startswith("/*", i):
            fin = src.find("\n", i) if src.startswith("//", i) else src.find("*/", i + 2)
            fin = n if fin < 0 else (fin if src.startswith("//", i) else fin + 2)
            out += [("code", src[debut:i]), ("commentaire", src[i:fin])]
            i = debut = fin
        elif c == "/":
            avant = src[debut:i].rstrip()
            mot = re.search(r"(\w+)$", avant)
            if not avant and not out or (avant[-1:] in AVANT_REGEX) or (mot and mot.group(1) in MOTS_REGEX) or \
                    (not avant and out and out[-1][0] in ("commentaire",)):
                i = _fin_regex(src, i)
            else:
                i += 1
        elif c in "'\"`":
            j = i + 1
            while j < n and src[j] != c:
                j += 2 if src[j] == "\\" else 1
            genre = "console" if CONSOLE.search(src[max(0, i - 40):i]) else "chaine"
            out += [("code", src[debut:i]), (genre, src[i:j + 1])]
            i = debut = j + 1
        else:
            i += 1
    out.append(("code", src[debut:]))
    return out


def lisible(chemin, texte):
    """Ce que l'apprenant lit dans un fichier publié : le texte sans les commentaires (et, pour un script, ses seules
    chaînes ; pour une feuille de style, ses seuls `content:`)."""
    if chemin.endswith(".js"):
        return "\n".join(t for g, t in morceaux_js(texte) if g == "chaine")
    if chemin.endswith(".css"):
        sans = re.sub(r"/\*.*?\*/", "", texte, flags=re.S)
        return "\n".join(re.findall(r"content\s*:\s*[^;}]+", sans))
    morceaux = []

    def script(m):
        morceaux.append("\n".join(t for g, t in morceaux_js(m.group(2)) if g == "chaine"))
        return ""

    def style(m):
        morceaux.append("\n".join(re.findall(r"content\s*:\s*[^;}]+", re.sub(r"/\*.*?\*/", "", m.group(1), flags=re.S))))
        return ""

    sans = re.sub(r"<!--.*?-->", "", texte, flags=re.S)
    sans = re.sub(r"<script([^>]*)>(.*?)</script>", script, sans, flags=re.S | re.I)
    sans = re.sub(r"<style[^>]*>(.*?)</style>", style, sans, flags=re.S | re.I)
    return sans + "\n" + "\n".join(morceaux)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dossier", default=os.path.join(RACINE, "site"), help="le dossier publié (site/ par défaut)")
    ap.add_argument("--tous", action="store_true", help="chaque extrait trouvé")
    args = ap.parse_args()
    fichiers = sorted(f for motif in ("**/*.html", "**/*.js", "**/*.css")
                      for f in glob.glob(os.path.join(args.dossier, motif), recursive=True)
                      if os.path.basename(f) not in SECRETS)
    total, touches = 0, 0
    for f in fichiers:
        with io.open(f, encoding="utf-8", errors="replace") as fh:
            texte = lisible(f, fh.read())
        trouves = list(TIRET.finditer(texte))
        if not trouves:
            continue
        total += len(trouves)
        touches += 1
        print("%s : %d" % (os.path.relpath(f, RACINE).replace(os.sep, "/"), len(trouves)))
        for m in trouves if args.tous else trouves[:3]:
            extrait = re.sub(r"\s+", " ", texte[max(0, m.start() - 50):m.end() + 40]).strip()
            print("    …%s…" % extrait)
    print("%d fichier(s) lus, %d tiret(s) dans %d fichier(s)." % (len(fichiers), total, touches))
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
