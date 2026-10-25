#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Écrit site/assets/js/langues-data.js : la liste des pages qui ont leur jumelle anglaise (site miroir).

    python3 outils/generer_langues.py           # écrit la liste, seulement si elle change
    python3 outils/generer_langues.py --essai   # l'affiche sans rien écrire ; code 1 si le fichier n'est pas à jour

Le site miroir (docs/I18N.md, partie A) : chaque page française X.html a sa jumelle anglaise en/X.html. Le bouton
FR / EN (site/assets/js/langue.js) ne s'affiche que sur une page qui a sa jumelle, et le menu d'une page anglaise
renvoie à la page française tant que la jumelle manque : la version anglaise se publie lot par lot. La liste se
déduit des fichiers de site/en/ — chemin depuis la racine du site, sans le préfixe de langue. Une page anglaise sans
page française au même chemin arrête l'outil : chaque page de en/ traduit une page du site.

À relancer après tout ajout ou retrait d'une page de site/en/. Repris du cours d'architecture logicielle.
"""
import argparse
import glob
import io
import json
import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(RACINE, "site")
EN = os.path.join(SITE, "en")
SORTIE = os.path.join(SITE, "assets", "js", "langues-data.js")

for flux in (sys.stdout, sys.stderr):
    try:
        flux.reconfigure(encoding="utf-8")
    except Exception:
        pass


def pages_traduites(site=SITE):
    """Les chemins (depuis la racine du site) des pages qui ont leur jumelle sous en/, triés."""
    en = os.path.join(site, "en")
    out = []
    for p in glob.glob(os.path.join(en, "**", "*.html"), recursive=True):
        rel = os.path.relpath(p, en).replace("\\", "/")
        if not os.path.exists(os.path.join(site, *rel.split("/"))):
            sys.exit("en/%s n'a pas de jumelle française (%s) : chaque page anglaise traduit une page du site."
                     % (rel, rel))
        out.append(rel)
    return sorted(out)


def produire(pages):
    return ("/* =================================================================\n"
            "   langues-data.js — Les pages qui ont leur jumelle anglaise sous en/\n"
            "   FICHIER GÉNÉRÉ par outils/generer_langues.py, d'après les fichiers de\n"
            "   site/en/ : ne pas le modifier à la main. Vide pour un cours sans\n"
            "   version anglaise, ou en blocs data-tr (docs/I18N.md).\n"
            "   ================================================================= */\n"
            "window.TPL_LANGUES = %s;\n" % json.dumps(pages, ensure_ascii=False, indent=1))


def generer(site=SITE, essai=False):
    """Écrit langues-data.js s'il change ; rend (à jour avant ?, pages traduites)."""
    pages = pages_traduites(site)
    texte = produire(pages)
    sortie = os.path.join(site, "assets", "js", "langues-data.js")
    ancien = io.open(sortie, encoding="utf-8").read() if os.path.exists(sortie) else None
    a_jour = ancien == texte
    if not a_jour and not essai:
        with io.open(sortie, "w", encoding="utf-8", newline="\n") as f:
            f.write(texte)
    return a_jour, pages


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--essai", action="store_true", help="n'écrit rien ; code 1 si le fichier n'est pas à jour")
    args = ap.parse_args()
    a_jour, pages = generer(essai=args.essai)
    print("langues-data.js : %d page(s) traduite(s) — %s"
          % (len(pages), "à jour" if a_jour else ("PAS À JOUR — rien écrit" if args.essai else "écrit")))
    return 1 if (args.essai and not a_jour) else 0


if __name__ == "__main__":
    sys.exit(main())
