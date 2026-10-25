#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vérifie qu'aucun interdit du cours n'apparaît hors de sa place (outils/interdits.py).

    python3 outils/verifier_interdits.py

Cherche les MOTS, les NOMBRES et les MOTIFS de outils/interdits.py dans tout ce qui se publie ou devient un média :
les pages de site/ et leurs jumelles anglaises, les scripts et données du site (glossaire, flashcards, QCM,
playlist, menus), les fiches des capsules audio (docs/prompts/), le contenu des polycopiés
(tools/polycopies_content.json). Les pages et dossiers de PERMIS — le TP, sa correction protégée — en sont exclus,
avec leurs jumelles sous en/. Les fichiers secrets ne sont jamais ouverts.

Un mot se cherche sans tenir compte de la casse ni des accents, en mot entier ; un nombre, avec virgule ou point,
séparateurs de milliers compris, et en toutes lettres (français et anglais, de 0 à 99). Repris, en générique, du
contrôle des chiffres du TP du cours d'architecture logicielle. Code 1 si un interdit est trouvé.
"""
import glob
import io
import os
import re
import sys
import unicodedata

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(RACINE, "site")
sys.path.insert(0, os.path.join(RACINE, "outils"))
import interdits as I  # noqa: E402

for flux in (sys.stdout, sys.stderr):
    try:
        flux.reconfigure(encoding="utf-8")
    except Exception:
        pass

SOURCES = ["site/**/*.html", "site/**/*.js", "docs/prompts/**/*.md", "tools/polycopies_content.json"]
SECRETS = {"elevenlabs.json", "config.json", "acces.json", "acces-zones.json", "known_hosts"}

_UNITES = ["zéro", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf", "dix", "onze", "douze",
           "treize", "quatorze", "quinze", "seize"]
_DIZAINES = {2: "vingt", 3: "trente", 4: "quarante", 5: "cinquante", 6: "soixante"}
_UNITS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
          "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
_TENS = {2: "twenty", 3: "thirty", 4: "forty", 5: "fifty", 6: "sixty", 7: "seventy", 8: "eighty", 9: "ninety"}


def en_lettres(n):
    """0 à 99 en toutes lettres (orthographe traditionnelle) : 45 → « quarante-cinq », 95 → « quatre-vingt-quinze »."""
    if n < 17:
        return _UNITES[n]
    if n < 20:
        return "dix-" + _UNITES[n - 10]
    d, u = divmod(n, 10)
    if d in (7, 9):
        base, reste = ("soixante" if d == 7 else "quatre-vingt"), 10 + u
        return base + (" et " if reste == 11 and d == 7 else "-") + en_lettres(reste)
    base = "quatre-vingt" if d == 8 else _DIZAINES[d]
    if u == 0:
        return base + ("s" if d == 8 else "")
    return base + (" et " if u == 1 and d != 8 else "-") + _UNITES[u]


def in_words(n):
    """0 à 99 en toutes lettres anglaises : 45 → « forty-five »."""
    if n < 20:
        return _UNITS[n]
    d, u = divmod(n, 10)
    return _TENS[d] + ("-" + _UNITS[u] if u else "")


def sans_accents(s):
    """Minuscules, sans accents, un caractère pour un caractère : les positions restent celles du texte d'origine."""
    out = []
    for c in s:
        b = unicodedata.normalize("NFD", c)
        b = "".join(x for x in b if unicodedata.category(x) != "Mn") or c
        out.append(b[0].lower() if len(b[0].lower()) == 1 else c)
    return "".join(out)


def chiffres(n):
    """Le nombre écrit sans séparateur, au point décimal : 99.95 → « 99.95 », « 12 000 » → « 12000 »."""
    if isinstance(n, str):
        n = float(re.sub(r"[\s  ]", "", n).replace(",", "."))
    if isinstance(n, float):
        return ("%.10f" % n).rstrip("0").rstrip(".")
    return str(n)


def motif_nombre(n):
    """Le motif d'un nombre en chiffres : virgule ou point décimal, séparateurs de milliers (espace, insécable,
    point, virgule) tolérés."""
    entier, _, decimales = chiffres(n).partition(".")
    groupes = []
    while len(entier) > 3:
        groupes.insert(0, entier[-3:])
        entier = entier[:-3]
    groupes.insert(0, entier)
    txt = "[\\s  .,]?".join(groupes)
    if decimales:
        txt += "[,.]" + decimales
    return re.compile(r"(?<![\d,.])" + txt + r"(?![\d]|[,.]\d)")


def motifs_en_lettres(n):
    """Les motifs d'un nombre en toutes lettres, en français et en anglais (0 à 99, et leurs décimales)."""
    entier, _, decimales = chiffres(n).partition(".")
    if int(entier) > 99 or (decimales and int(decimales) > 99):
        return []
    fr = en_lettres(int(entier)) + (" virgule " + en_lettres(int(decimales)) if decimales else "")
    en = re.escape(in_words(int(entier)))
    if decimales:
        en += " point (?:%s|%s)" % (re.escape(" ".join(_UNITS[int(c)] for c in decimales)),
                                    re.escape(in_words(int(decimales))))
    return [re.compile(r"(?<![\w-])" + re.escape(sans_accents(fr)) + r"(?![\w-])"),
            re.compile(r"(?<![\w-])" + en + r"(?![\w-])", re.I)]


def regles():
    """[(nom, motif, sur le texte sans accents ?)] d'après outils/interdits.py."""
    out = []
    for mot in I.MOTS:
        m = sans_accents(mot.strip())
        if m:
            out.append(("mot interdit « %s »" % mot, re.compile(r"(?<!\w)" + re.escape(m) + r"(?!\w)"), True))
    for n in I.NOMBRES:
        out.append(("nombre interdit %s" % n, motif_nombre(n), False))
        for m in motifs_en_lettres(n):
            out.append(("nombre interdit %s, en lettres" % n, m, True))
    for nom, rx in I.MOTIFS:
        out.append((nom, re.compile(rx), False))
    return out


def permis(rel_site):
    """Vrai pour une page ou un dossier de PERMIS (chemin depuis site/), et pour sa jumelle sous en/."""
    p = rel_site[3:] if rel_site.startswith("en/") else rel_site
    return any(p == x or (x.endswith("/") and p.startswith(x)) for x in I.PERMIS)


def fichiers():
    vus = set()
    for motif in SOURCES:
        for chemin in sorted(glob.glob(os.path.join(RACINE, *motif.split("/")), recursive=True)):
            if chemin in vus or os.path.basename(chemin) in SECRETS or not os.path.isfile(chemin):
                continue
            vus.add(chemin)
            rel = os.path.relpath(chemin, RACINE).replace("\\", "/")
            if rel.startswith("site/") and permis(rel[5:]):
                continue
            yield chemin, rel


def main():
    r = regles()
    if not r:
        print("Aucun interdit déclaré (outils/interdits.py) : rien à contrôler.")
        return 0
    trouves, n = [], 0
    for chemin, rel in fichiers():
        n += 1
        texte = io.open(chemin, encoding="utf-8").read()
        plat = sans_accents(texte)
        for nom, motif, sur_plat in r:
            for m in motif.finditer(plat if sur_plat else texte):
                ligne = texte.count("\n", 0, m.start()) + 1
                trouves.append("%s:%d — %s : « %s »" % (rel, ligne, nom, texte[m.start():m.end()]))
    if trouves:
        print("Interdits trouvés hors de leur place (%d fichier(s) lus) :" % n)
        for t in trouves:
            print("  ✗", t)
        return 1
    print("Aucun interdit hors de sa place : %d règle(s), %d fichier(s) lus, %d page(s) ou dossier(s) permis."
          % (len(r), n, len(I.PERMIS)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
