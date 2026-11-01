#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Écrit site/assets/js/media-data.js (window.TPL_MEDIAS) : les médias réellement déposés dans le site.

    python3 outils/generer_medias.py           # écrit le fichier s'il change
    python3 outils/generer_medias.py --essai   # n'écrit rien ; code 1 si le fichier n'est pas à jour

media.js ne sait pas, à lui seul, quels médias existent : il les demandait au serveur, et chaque média absent — le
podcast sous ses quatre noms possibles, les diapositives, l'infographie, la fiche de synthèse — laissait une erreur
404 dans la console de chaque chapitre. Avec cette liste, il ne demande que ce qui est là ; sans elle (un cours qui
ne l'a pas encore), il sonde comme avant.

La liste se périme dès qu'un média est déposé, renommé ou retiré, et un média absent de la liste ne s'affiche pas :
elle se régénère après chaque dépôt. nouveau_cours.py et outils/generer_podcasts.py la relancent ; --essai la
contrôle (CLAUDE.md, § 6).
"""
import io
import json
import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Les dossiers que lit media.js (relatifs à site/), leur clé dans TPL_MEDIAS et les extensions qu'il y cherche. Le
# reste — les diapositives WebP de la page Podcasts, un fichier de travail — n'a rien à faire dans la liste.
DOSSIERS = (
    ("podcasts", "assets/media/podcasts", (".mp3", ".m4a")),
    ("slides", "assets/media/slides", (".pdf",)),
    ("infographies", "assets/media/infographies", (".png",)),
    ("polycopies", "assets/polycopies", (".pdf", ".docx")),
)

ENTETE = """/* =================================================================
   media-data.js — Les médias déposés dans le site, par dossier
   FICHIER GÉNÉRÉ par outils/generer_medias.py, d'après les fichiers de
   site/assets/media/ et site/assets/polycopies/ : ne pas le modifier à
   la main. media.js n'y demande au serveur que ce qui est là.
   ================================================================= */
"""


def produire(racine):
    """(texte de media-data.js, {clé: [fichiers]}) : pour chaque dossier, ses médias de chapitre, triés."""
    donnees = {}
    for cle, rel, extensions in DOSSIERS:
        dossier = os.path.join(racine, "site", *rel.split("/"))
        noms = os.listdir(dossier) if os.path.isdir(dossier) else []
        donnees[cle] = sorted(f for f in noms if f.startswith("chapitre-") and f.lower().endswith(extensions)
                              and os.path.isfile(os.path.join(dossier, f)))
    return ENTETE + "window.TPL_MEDIAS = " + json.dumps(donnees, ensure_ascii=False, indent=1) + ";\n", donnees


def generer(racine, essai=False):
    """Écrit media-data.js s'il change ; rend (à jour avant ?, {clé: nombre de fichiers})."""
    cible = os.path.join(racine, "site", "assets", "js", "media-data.js")
    texte, donnees = produire(racine)
    actuel = io.open(cible, encoding="utf-8").read() if os.path.isfile(cible) else ""
    a_jour = actuel == texte
    if not a_jour and not essai:
        with io.open(cible, "w", encoding="utf-8", newline="\n") as f:
            f.write(texte)
    return a_jour, {cle: len(v) for cle, v in donnees.items()}


def main():
    essai = "--essai" in sys.argv[1:]
    a_jour, nombres = generer(RACINE, essai)
    etat = "à jour" if a_jour else ("PAS À JOUR — rien écrit" if essai else "écrit")
    print("media-data.js : %s — %s" % (", ".join("%s %d" % (c, n) for c, n in nombres.items()), etat))
    return 1 if (essai and not a_jour) else 0


if __name__ == "__main__":
    sys.exit(main())
