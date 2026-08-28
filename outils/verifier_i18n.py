#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vérifie la cohérence du bilingue FR/EN du site.

    python3 outils/verifier_i18n.py

Quatre contrôles, dans l'ordre où ils font mal quand on les oublie :

1. PARITÉ DES CLÉS d'interface (ui-labels.js) — une clé présente en
   français et absente en anglais donne un bouton en français au milieu
   d'une page anglaise. Personne ne le voit avant un étudiant.

2. CLÉS APPELÉES MAIS NON DÉFINIES — un T('etapes.suivant') au lieu de
   T('etapes.suivante') affiche littéralement « etapes.suivant » à l'écran.

3. BLOCS data-tr DÉPAREILLÉS dans les pages — un titre traduit dont le
   paragraphe ne l'est pas laisse un trou en anglais. Le script compte
   les blocs de chaque langue par page et signale les écarts.

4. TITRES DIVERGENTS entre course-data.js et les pages — un chapitre
   renommé dans sa page mais pas dans les données affiche deux titres
   différents. On ne regarde pas le menu en lisant un chapitre : cela
   peut tenir des mois.

Sort en code 1 si un contrôle échoue : utilisable en CI ou en pré-commit.
"""

import io
import os
import re
import sys
import glob

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(RACINE, "site")
LABELS = os.path.join(SITE, "assets", "js", "ui-labels.js")


def cles_du_bloc(source, langue):
    """Les clés déclarées dans le bloc fr: {...} ou en: {...}."""
    m = re.search(r"\n  " + langue + r":\s*\{(.*?)\n  \}", source, re.S)
    if not m:
        return set()
    return set(re.findall(r"'([a-zA-Z][\w.]*)'\s*:", m.group(1)))


def cles_appelees():
    """Les clés réellement passées à T() dans les moteurs."""
    out = {}
    for f in sorted(glob.glob(os.path.join(SITE, "assets", "js", "*.js"))):
        if os.path.basename(f) == "ui-labels.js":
            continue
        t = io.open(f, encoding="utf-8").read()
        for k in re.findall(r"\bT\(\s*'([^']+)'\s*\)", t):
            out.setdefault(k, []).append(os.path.basename(f))
    return out


def blocs_data_tr():
    """{page: (nb_fr, nb_en)} — les blocs jumelés de contenu rédigé."""
    out = {}
    for f in sorted(glob.glob(os.path.join(SITE, "**", "*.html"), recursive=True)):
        t = io.open(f, encoding="utf-8").read()
        fr = len(re.findall(r'data-tr="fr"', t))
        en = len(re.findall(r'data-tr="en"', t))
        if fr or en:
            out[os.path.relpath(f, SITE).replace(os.sep, "/")] = (fr, en)
    return out


def titres_divergents():
    """[(fichier, titre des donnees, titre de la page)] pour chaque ecart.

    Un chapitre renomme dans sa page mais pas dans course-data.js affiche
    deux titres differents — et cela ne se voit pas, puisqu'on ne regarde
    pas le menu en lisant un chapitre.
    """
    data_js = os.path.join(SITE, "assets", "js", "course-data.js")
    if not os.path.isfile(data_js):
        return []
    data = io.open(data_js, encoding="utf-8").read()
    motif = (r"file: '(\d\d-[a-z0-9-]+\.html)',\s*\n\s*"
             r"title: \{ fr: \"([^\"]+)\", en: \"([^\"]+)\" \}")
    out = []
    for m in re.finditer(motif, data):
        fichier, dfr, den = m.groups()
        page = os.path.join(SITE, "chapitres", fichier)
        if not os.path.isfile(page):
            out.append((fichier, "%s / %s" % (dfr, den), "page absente"))
            continue
        h = io.open(page, encoding="utf-8").read()
        t1 = re.search(r'<h1 class="chapter-title">(.*?)</h1>', h, re.S)
        if not t1:
            continue
        pfr = re.search(r'data-tr="fr">(.*?)</span>', t1.group(1), re.S)
        pen = re.search(r'data-tr="en">(.*?)</span>', t1.group(1), re.S)
        pfr = pfr.group(1).strip() if pfr else ""
        pen = pen.group(1).strip() if pen else ""
        if (dfr, den) != (pfr, pen):
            out.append((fichier, "%s / %s" % (dfr, den), "%s / %s" % (pfr, pen)))
    return out


def main():
    if not os.path.isfile(LABELS):
        sys.exit("ui-labels.js est introuvable : %s" % LABELS)
    src = io.open(LABELS, encoding="utf-8").read()
    fr, en = cles_du_bloc(src, "fr"), cles_du_bloc(src, "en")
    echecs = 0

    print("1. Parité des clés d'interface")
    print("   -----------------------------")
    sans_en = sorted(fr - en)
    sans_fr = sorted(en - fr)
    if sans_en:
        echecs += 1
        print("   %d clé(s) sans traduction anglaise :" % len(sans_en))
        for k in sans_en:
            print("      %s" % k)
    if sans_fr:
        echecs += 1
        print("   %d clé(s) anglaise(s) sans équivalent français :" % len(sans_fr))
        for k in sans_fr:
            print("      %s" % k)
    if not sans_en and not sans_fr:
        print("   %d clés, appariées dans les deux langues." % len(fr))

    print("\n2. Clés appelées par les moteurs")
    print("   -----------------------------")
    appelees = cles_appelees()
    inconnues = {k: v for k, v in appelees.items() if k not in fr}
    if inconnues:
        echecs += 1
        print("   %d clé(s) appelée(s) mais non définie(s) :" % len(inconnues))
        for k, fichiers in sorted(inconnues.items()):
            print("      %-34s (%s)" % (k, ", ".join(sorted(set(fichiers)))))
    else:
        print("   %d clés appelées, toutes définies." % len(appelees))
    inutilisees = sorted(fr - set(appelees))
    if inutilisees:
        print("   %d clé(s) définie(s) mais jamais appelée(s) — sans gravité,"
              % len(inutilisees))
        print("   mais c'est souvent le signe d'un moteur pas encore branché :")
        print("      %s" % ", ".join(inutilisees[:12]))

    print("\n3. Blocs data-tr des pages")
    print("   -----------------------------")
    ecarts = []
    for page, (a, b) in blocs_data_tr().items():
        if a != b:
            ecarts.append((page, a, b))
    if ecarts:
        echecs += 1
        print("   %d page(s) au contenu dépareillé :" % len(ecarts))
        for page, a, b in ecarts:
            print("      %-44s fr=%d  en=%d" % (page, a, b))
    else:
        print("   Toutes les pages ont autant de blocs français qu'anglais.")

    print("\n4. Titres : donnees du cours et pages")
    print("   -----------------------------")
    derives = titres_divergents()
    if derives:
        echecs += 1
        print("   %d titre(s) divergent(s) entre course-data.js et les pages :"
              % len(derives))
        for f, a, b in derives:
            print("      %s" % f)
            print("         donnees : %s" % a)
            print("         page    : %s" % b)
        print("   Le menu et la page afficheraient deux titres differents.")
    else:
        print("   Les titres du menu correspondent a ceux des pages.")

    print("\nBilan\n-----")
    if echecs:
        print("  %d contrôle(s) en échec." % echecs)
        return 1
    print("  Bilingue cohérent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
