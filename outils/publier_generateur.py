#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Écrit site/generateur/ : la copie publiée du générateur de prompt (generateur/), que le site de démonstration du
gabarit sert dans une zone protégée par mot de passe.

    python3 outils/publier_generateur.py           # écrit la copie si elle change
    python3 outils/publier_generateur.py --essai   # n'écrit rien ; code 1 si la copie ne suit pas generateur/

La page de travail reste generateur/index.html, ouverte d'un double clic. site/generateur/ en est la copie, à ne
jamais modifier à la main : la page, ses deux scripts et le modèle des valeurs. Deux écarts seulement, posés ici.
<html> porte data-publiee, et la page charge valeurs.exemple.js à la place de valeurs.local.js : ce fichier garde
l'adresse de l'auteur et ses chemins, il ne se publie jamais (ignoré par Git, où qu'il soit). page.js, dans la copie,
garde alors les valeurs habituelles dans le navigateur.

LA ZONE. « generateur/ » se déclare dans « zones_protegees » de deploiement/destination.json et dans
docs/acces-zones.json ; deploiement/proteger_zones.py pose la protection, et le déployeur ne publie la copie qu'une
fois la protection en ligne. Aucun cours créé ne la reçoit : nouveau_cours.py retire site/generateur/ et cet outil.

À relancer après toute retouche de generateur/ (après node generateur/essai_generateur.js). Décision de l'auteur du
23 novembre 2026 : une rubrique du site pour le générateur, son accès protégé par mot de passe.
"""
import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(RACINE, "generateur")
COPIE = os.path.join(RACINE, "site", "generateur")

for flux in (sys.stdout, sys.stderr):
    try:
        flux.reconfigure(encoding="utf-8")
    except Exception:
        pass

FICHIERS = ("index.html", "generateur.js", "page.js", "valeurs.exemple.js")

# Les écarts de la copie, chacun attendu une fois exactement dans generateur/index.html.
ECARTS = (
    (b'<html lang="fr">', b'<html lang="fr" data-publiee>'),
    (b'<script src="valeurs.local.js"></script>', b'<script src="valeurs.exemple.js"></script>'),
)


def contenu(nom):
    """Les octets attendus dans la copie : ceux de generateur/, fins de ligne comprises, écarts posés."""
    with open(os.path.join(SOURCE, nom), "rb") as f:
        octets = f.read()
    if nom == "index.html":
        for avant, apres in ECARTS:
            if octets.count(avant) != 1:
                sys.exit("generateur/index.html : %r trouvé %d fois au lieu d'une ; la copie n'est pas écrite."
                         % (avant.decode("utf-8"), octets.count(avant)))
            octets = octets.replace(avant, apres)
    return octets


def meme_texte(a, b):
    """Les fins de ligne ne comptent pas : Git range les deux fichiers en LF, et une copie de travail peut tenir l'un
    en CRLF et l'autre en LF après une mise à jour qui n'a touché que la page (autocrlf, sous Windows)."""
    return a.replace(b"\r\n", b"\n") == b.replace(b"\r\n", b"\n")


def main():
    essai = "--essai" in sys.argv[1:]
    attendus = {nom: contenu(nom) for nom in FICHIERS}
    presents = sorted(os.listdir(COPIE)) if os.path.isdir(COPIE) else []
    # Un fichier de trop serait publié tel quel avec la copie (valeurs.local.js déposé à la main, par exemple).
    en_trop = [n for n in presents if n not in FICHIERS]
    ecarts = []
    for nom, octets in attendus.items():
        chemin = os.path.join(COPIE, nom)
        if not os.path.isfile(chemin) or not meme_texte(open(chemin, "rb").read(), octets):
            ecarts.append(nom)
    if en_trop:
        print("site/generateur/ contient des fichiers que la copie n'a pas : %s. Retirez-les : ils seraient "
              "publiés avec elle." % ", ".join(en_trop))
    if not ecarts:
        print("site/generateur/ (%d fichiers), à jour" % len(FICHIERS))
        return 1 if en_trop else 0
    if essai:
        print("site/generateur/ : PAS À JOUR, rien écrit (%s)" % ", ".join(ecarts))
        return 1
    os.makedirs(COPIE, exist_ok=True)
    for nom in ecarts:
        with open(os.path.join(COPIE, nom), "wb") as f:
            f.write(attendus[nom])
    print("site/generateur/ : écrit (%s)" % ", ".join(ecarts))
    return 1 if en_trop else 0


if __name__ == "__main__":
    sys.exit(main())
