#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Écrit site/assets/js/langues-data.js : la langue de la racine du site miroir, et, pour chaque autre langue, les
pages qui y ont leur jumelle.

    python3 outils/generer_langues.py           # écrit la liste, seulement si elle change
    python3 outils/generer_langues.py --essai   # l'affiche sans rien écrire ; code 1 si le fichier n'est pas à jour

Le site miroir (docs/I18N.md, partie A) : chaque page X.html de la racine, écrite dans la langue racine du cours, a
ses jumelles <langue>/X.html (en/X.html, ar/X.html…). Le choix de langue de l'en-tête (site/assets/js/langue.js) ne
propose une langue que si la page y existe, et le menu d'une jumelle renvoie à la page de la racine tant que sa
traduction manque : chaque langue se publie lot par lot. La langue racine est celle que déclare l'accueil
(<html lang>) ; les listes se déduisent des dossiers de langue de site/, chemins depuis la racine du site, sans le
dossier de langue. Une jumelle sans page au même chemin à la racine arrête l'outil : chaque jumelle traduit une page
du site.

À relancer après tout ajout ou retrait d'une jumelle. Repris du cours d'architecture logicielle, étendu à plusieurs
langues le 21 novembre 2026 (l'arabe s'y ajoute, de droite à gauche).
"""
import argparse
import glob
import io
import json
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(RACINE, "site")
SORTIE = os.path.join(SITE, "assets", "js", "langues-data.js")
# Les langues que le gabarit sait servir, dans l'ordre du choix de langue ; l'arabe s'écrit de droite à gauche.
LANGUES = ("fr", "en", "ar")

for flux in (sys.stdout, sys.stderr):
    try:
        flux.reconfigure(encoding="utf-8")
    except Exception:
        pass


def langue_racine(site=SITE):
    """La langue des pages de la racine : celle que déclare l'accueil, le français à défaut."""
    try:
        t = io.open(os.path.join(site, "index.html"), encoding="utf-8").read()
    except OSError:
        return "fr"
    m = re.search(r'<html\b[^>]*\blang="([a-z]{2})', t)
    return m.group(1) if m and m.group(1) in LANGUES else "fr"


def pages_par_langue(site=SITE):
    """(langue racine, {langue : pages qui y ont leur jumelle}) : une entrée par dossier de langue non vide."""
    racine = langue_racine(site)
    pages = {}
    for lg in LANGUES:
        dossier = os.path.join(site, lg)
        if lg == racine or not os.path.isdir(dossier):
            continue
        liste = []
        for p in glob.glob(os.path.join(dossier, "**", "*.html"), recursive=True):
            rel = os.path.relpath(p, dossier).replace("\\", "/")
            if not os.path.exists(os.path.join(site, *rel.split("/"))):
                sys.exit("%s/%s n'a pas de page à la racine (%s) : chaque jumelle traduit une page du site."
                         % (lg, rel, rel))
            liste.append(rel)
        if liste:
            pages[lg] = sorted(liste)
    return racine, pages


def pages_traduites(site=SITE, langue="en"):
    """Les pages qui ont leur jumelle dans <langue>/, triées (creer_jumelle.py, hreflang.py)."""
    return pages_par_langue(site)[1].get(langue, [])


def resume(racine, pages):
    """Une ligne pour la console : « racine fr ; en 16 page(s), ar 1 page(s) »."""
    return "racine %s ; %s" % (racine, ", ".join("%s %d page(s)" % (lg, len(p)) for lg, p in pages.items())
                               or "aucune jumelle")


def produire(racine, pages):
    return ("/* =================================================================\n"
            "   langues-data.js · Les pages du site miroir et leurs jumelles\n"
            "   FICHIER GÉNÉRÉ par outils/generer_langues.py, d'après les dossiers\n"
            "   de langue de site/ (en/, ar/…) : ne pas le modifier à la main.\n"
            "   racine : la langue des pages de la racine ; pages : pour chaque\n"
            "   autre langue, les pages qui y ont leur jumelle. Vide pour un cours\n"
            "   sans jumelles, ou en blocs data-tr (docs/I18N.md).\n"
            "   ================================================================= */\n"
            "window.TPL_MIROIR = %s;\n"
            % json.dumps({"racine": racine, "pages": pages}, ensure_ascii=False, indent=1))


def generer(site=SITE, essai=False):
    """Écrit langues-data.js s'il change ; rend (à jour avant ?, langue racine, {langue : pages})."""
    racine, pages = pages_par_langue(site)
    texte = produire(racine, pages)
    sortie = os.path.join(site, "assets", "js", "langues-data.js")
    ancien = io.open(sortie, encoding="utf-8").read() if os.path.exists(sortie) else None
    a_jour = ancien == texte
    if not a_jour and not essai:
        with io.open(sortie, "w", encoding="utf-8", newline="\n") as f:
            f.write(texte)
    return a_jour, racine, pages


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--essai", action="store_true", help="n'écrit rien ; code 1 si le fichier n'est pas à jour")
    args = ap.parse_args()
    a_jour, racine, pages = generer(essai=args.essai)
    print("langues-data.js : %s, %s"
          % (resume(racine, pages), "à jour" if a_jour else ("PAS À JOUR, rien écrit" if args.essai else "écrit")))
    return 1 if (args.essai and not a_jour) else 0


if __name__ == "__main__":
    sys.exit(main())
