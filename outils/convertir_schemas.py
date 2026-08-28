#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convertit en WebP les schémas déposés en PNG.

    python3 outils/convertir_schemas.py

Les PNG restent sur votre disque — ils sont ignorés par Git, et c'est voulu :
un lot de six schémas pèse 7 Mo en PNG contre 0,5 Mo en WebP, et un fichier
poussé une fois reste dans l'historique du dépôt pour toujours, même supprimé
ensuite. Seul le WebP est versionné.

Réglages identiques à ceux des chapitres déjà convertis — qualité 82,
méthode 6 — pour que tous les schémas du cours aient le même rendu.

Ne retouche que ce qui en a besoin : un PNG dont le WebP existe déjà et est
plus récent est laissé tranquille.
"""

import glob
import os
import subprocess
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Le site vit dans site/, pas a la racine : celle-ci porte aussi les outils,
# les fiches de production et la documentation, qui ne sont pas publies.
SITE = os.path.join(RACINE, "site")
SCHEMAS = os.path.join(SITE, "assets", "media", "schemas")
QUALITE = 82
METHODE = 6


def humain(n):
    return "%.1f Mo" % (n / 1048576.0) if n >= 1048576 else "%.0f Ko" % (n / 1024.0)


def convertisseur():
    """('pillow', None) ou ('cwebp', chemin), ou (None, None) si rien n'est là."""
    try:
        from PIL import Image  # noqa: F401
        return "pillow", None
    except ImportError:
        pass
    for nom in ("cwebp",):
        try:
            subprocess.check_output([nom, "-version"], stderr=subprocess.STDOUT)
            return "cwebp", nom
        except (OSError, subprocess.CalledProcessError):
            continue
    return None, None


def convertir(outil, binaire, src, dst):
    if outil == "pillow":
        from PIL import Image
        with Image.open(src) as im:
            im.convert("RGB").save(dst, "WEBP", quality=QUALITE, method=METHODE)
    else:
        subprocess.check_output(
            [binaire, "-q", str(QUALITE), "-m", str(METHODE), src, "-o", dst],
            stderr=subprocess.STDOUT)


def main():
    if not os.path.isdir(SCHEMAS):
        sys.exit("Répertoire introuvable : %s" % SCHEMAS)

    outil, binaire = convertisseur()
    if not outil:
        sys.exit(
            "Aucun convertisseur disponible.\n"
            "Installez l'un des deux, puis relancez :\n"
            "    python3 -m pip install --user pillow\n"
            "    brew install webp")

    pngs = sorted(glob.glob(os.path.join(SCHEMAS, "*.png")))
    if not pngs:
        print("  Aucun PNG dans assets/media/schemas/ : rien à convertir.")
        return 0

    print("  Convertisseur : %s\n" % outil)
    faits, sautes, avant, apres = 0, 0, 0, 0
    for src in pngs:
        dst = os.path.splitext(src)[0] + ".webp"
        nom = os.path.basename(dst)
        if os.path.isfile(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
            sautes += 1
            continue
        try:
            convertir(outil, binaire, src, dst)
        except Exception as e:
            print("  ÉCHEC  %-50s %s" % (nom, e))
            continue
        a, b = os.path.getsize(src), os.path.getsize(dst)
        avant += a
        apres += b
        faits += 1
        print("  %-50s %8s -> %8s   -%2.0f %%" % (nom, humain(a), humain(b), 100 * (1 - b / float(a))))

    print("")
    if faits:
        print("  %d converti(s) : %s -> %s  (-%.0f %%)"
              % (faits, humain(avant), humain(apres), 100 * (1 - apres / float(avant))))
    if sautes:
        print("  %d déjà à jour, laissé(s) tel(s) quel(s)." % sautes)
    if faits:
        print("\n  À pousser — seuls les WebP sont versionnés :")
        print("      git add assets/media/schemas/")
        print("      git commit -m \"schemas du chapitre N\"")
        print("      git push")
    return 0


if __name__ == "__main__":
    sys.exit(main())
