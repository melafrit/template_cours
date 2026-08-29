#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cherche les liens morts du site.

    python3 outils/verifier_liens.py
    python3 outils/verifier_liens.py --site ../mon-cours/site

POURQUOI

C'est le défaut le plus coûteux du template, et le seul qu'aucun des deux
autres vérificateurs n'attrape.

Le site de démonstration parle de « concevoir un cours en ligne ». Ses pages
citent ses propres chapitres — `01-cadrage.html`, `02-structurer.html` — et
`nouveau_cours.py` les remplace par les chapitres déclarés dans `cours.json`.
Chaque fois qu'une page échappait à ce recousage, un cours créé partait avec un
lien vers une page inexistante. C'est arrivé quatre fois, sur quatre familles de
liens différentes : le bouton « commencer » de l'accueil, les cartes du
sommaire, la pagination des chapitres, le pied de page.

Aucune ne se voit à la relecture. Toutes se voient en une seconde ici.

CE QU'IL CONTRÔLE

Les `href` et les `src` qui désignent un fichier du site : pages, images,
feuilles de style, scripts, PDF, audio. Les liens externes, les ancres seules,
`mailto:`, `tel:`, `javascript:` et les `data:` sont ignorés — ils ne sont pas
vérifiables hors ligne.

Les cibles construites en JavaScript ne sont pas visibles ici : les boutons
`data-chapitre`, par exemple, reçoivent leur `href` à l'exécution. C'est
volontaire, et c'est justement ce qui les met à l'abri.
"""

import argparse
import io
import os
import re
import sys
from urllib.parse import unquote

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# href="..." et src="...", en simples ou doubles guillemets.
LIEN = re.compile(r'(?:href|src)\s*=\s*(["\'])(.*?)\1', re.I | re.S)

# Ce qui ne désigne pas un fichier du site.
IGNORE = re.compile(r'^\s*(?:https?:|//|mailto:|tel:|javascript:|data:|#|\{)', re.I)


def liens_de(page, site):
    """Les cibles locales citées par une page, résolues en chemins de disque."""
    t = io.open(page, encoding="utf-8", errors="replace").read()
    dossier = os.path.dirname(page)
    vus = []
    for _, brut in LIEN.findall(t):
        cible = brut.strip()
        if not cible or IGNORE.match(cible):
            continue
        # On laisse tomber l'ancre et la chaîne de requête : le fichier seul compte.
        chemin = unquote(cible.split("#", 1)[0].split("?", 1)[0])
        if not chemin:
            continue
        base = site if chemin.startswith("/") else dossier
        reel = os.path.normpath(os.path.join(base, chemin.lstrip("/")))
        vus.append((cible, reel))
    return vus


def main():
    ap = argparse.ArgumentParser(description="Cherche les liens morts du site.")
    ap.add_argument("--site", default=os.path.join(RACINE, "site"),
                    help="dossier du site à contrôler (défaut : site/)")
    args = ap.parse_args()

    site = os.path.abspath(args.site)
    if not os.path.isdir(site):
        sys.exit("Dossier introuvable : %s" % site)

    pages = []
    for dossier, _, fichiers in os.walk(site):
        for f in sorted(fichiers):
            if f.endswith(".html"):
                pages.append(os.path.join(dossier, f))

    print("\nLiens du site\n-------------")
    print("  %d page(s) analysée(s) dans %s" % (len(pages), os.path.relpath(site, RACINE)))

    morts = []
    total = 0
    for p in sorted(pages):
        for cible, reel in liens_de(p, site):
            total += 1
            if not os.path.exists(reel):
                morts.append((os.path.relpath(p, site), cible))

    print("  %d lien(s) local(aux) contrôlé(s)" % total)

    if not morts:
        print("\nBilan\n-----\n  Aucun lien mort.")
        return 0

    print("\n  %d lien(s) mort(s) :\n" % len(morts))
    courante = None
    for page, cible in morts:
        if page != courante:
            print("    %s" % page.replace(os.sep, "/"))
            courante = page
        print("        -> %s" % cible)

    print("\nBilan\n-----")
    print("  %d lien(s) mort(s). Dans un cours créé, la cause est presque" % len(morts))
    print("  toujours la même : une famille de liens que recoudre_liens()")
    print("  de nouveau_cours.py ne connaît pas encore.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
