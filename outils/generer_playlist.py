#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construit assets/js/playlist-data.js à partir des pages de chapitre.

La playlist doit connaître les pistes de TOUS les chapitres, y compris ceux que
l'on n'est pas en train de lire. Elle ne peut donc pas les découvrir dans le
document courant : il lui faut un index. Ce script le fabrique, pour qu'il ne
puisse pas diverger des pages.

    python3 outils/generer_playlist.py

L'ordre des pistes est celui du document — podcast d'abord, puis les capsules
telles qu'elles apparaissent en descendant la page. C'est l'ordre dans lequel
la lecture automatique enchaînera.

Les durées viennent de ffprobe quand le fichier existe, sinon de la durée
annoncée dans l'appel RDCX.voice. Une piste non encore enregistrée figure dans
la playlist, grisée : l'étudiant voit ce qui arrive.
"""

import glob
import io
import json
import os
import re
import subprocess
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Le site vit dans site/, pas a la racine : celle-ci porte aussi les outils,
# les fiches de production et la documentation, qui ne sont pas publies.
SITE = os.path.join(RACINE, "site")
SORTIE = os.path.join(SITE, "assets", "js", "playlist-data.js")


def duree_reelle(chemin):
    """mm:ss d'après le fichier, ou None si ffprobe est absent ou le fichier aussi."""
    if not os.path.isfile(chemin):
        return None
    try:
        brut = subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", chemin],
            stderr=subprocess.STDOUT)
    except (OSError, subprocess.CalledProcessError):
        return None
    try:
        s = int(float(brut.decode().strip()))
    except ValueError:
        return None
    return "%d:%02d" % (s // 60, s % 60)


def texte_langue(html, langue="fr"):
    """Le texte d'UNE langue dans un fragment bilingue.

    Sans cela, retirer les balises d'un titre jumele colle les deux versions :
    « Cadrer son coursScoping your course ».
    """
    m = re.findall(r'<span data-tr="%s"[^>]*>(.*?)</span>' % langue, html, re.S)
    if m:
        return texte(" ".join(m))
    return texte(html)


def texte(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html)).strip()


def pistes_du_chapitre(n, chemin_page):
    """n vaut None pour une page hors chapitre : elle n'a pas de podcast."""
    t = io.open(chemin_page, encoding="utf-8").read()
    pistes = []

    # --- le podcast : posé par media.js d'après le nom, pas écrit dans la page
    # Le podcast existe par langue : « chapitre-1-podcast.fr.mp3 ». On indexe
    # chaque langue trouvee, et on retombe sur le nom sans suffixe pour un
    # cours monolingue.
    for langue in (("fr", "en", None) if n else ()):
        for ext in ("mp3", "m4a", "wav"):
            suffixe = ("." + langue) if langue else ""
            rel = "assets/media/podcasts/chapitre-%d-podcast%s.%s" % (n, suffixe, ext)
            if not os.path.isfile(os.path.join(SITE, rel)):
                continue
            titre = t.find('class="podcast-title"')
            lib = "Podcast du chapitre"
            if titre > -1:
                m = re.search(r'class="podcast-title"[^>]*>(.*?)</',
                              t[titre - 40:titre + 400], re.S)
                if m:
                    lib = texte_langue(m.group(1), langue or "fr") or lib
            pistes.append({"type": "podcast", "titre": lib, "src": rel,
                           "duree": duree_reelle(os.path.join(SITE, rel)) or "",
                           "present": True, "langue": langue})
            break

    # --- les capsules, dans l'ordre où leurs conteneurs apparaissent
    reglages = {}
    for m in re.finditer(
            r"RDCX\.voice\('([^']+)',\s*\{(.*?)\n\s*\}\);", t, re.S):
        cid, corps = m.group(1), m.group(2)
        src = re.search(r"src:\s*'([^']+)'", corps)
        ttl = re.search(r'titre:\s*(\x27|")(.*?)\1\s*,', corps, re.S)
        dur = re.search(r"duree:\s*(\x27|\")([^\x27\"]*)\1", corps)
        reglages[cid] = {
            "src": (src.group(1) if src else "").replace("../", ""),
            "titre": texte(ttl.group(2)).replace("**", "") if ttl else cid,
            "duree": dur.group(2) if dur else "",
        }

    # « capsule-<nom> » ouvre une page hors chapitre, où la numérotation
    # voix-N-N / ouverture-N-N n'a pas de sens.
    # Capsules bilingues : un seul appel RDCX.voice sert deux fichiers, la
    # source venant de TEXTES. On lit donc TEXTES, sinon elles sont invisibles.
    for m in re.finditer(r'capsuleSrc: "([^"]+)"', t):
        chemin = m.group(1).replace("../", "")
        suite = t[m.end():m.end() + 400]
        ttl = re.search(r'capsuleTitre: "([^"]*)"', suite)
        lg = re.search(r"-(fr|en)\.mp3$", chemin)
        absolu = os.path.join(SITE, chemin.replace("/", os.sep))
        pistes.append({
            "type": "ouverture",
            "titre": ttl.group(1) if ttl else os.path.basename(chemin),
            "src": chemin,
            "duree": duree_reelle(absolu) or "",
            "present": os.path.isfile(absolu),
            "langue": lg.group(1) if lg else None,
            "ancre": "capsule-%s" % (n or ""),
        })

    for m in re.finditer(r'id="((?:voix|ouverture)-\d+-\d+|capsule-[a-z0-9-]+)"', t):
        cid = m.group(1)
        r = reglages.get(cid)
        if not r or not r["src"]:
            continue
        absolu = os.path.join(SITE, r["src"].replace("/", os.sep))
        pistes.append({
            "type": "ouverture" if cid.startswith(("ouverture", "capsule")) else "voix",
            "titre": r["titre"],
            "src": r["src"],
            "duree": duree_reelle(absolu) or r["duree"],
            "present": os.path.isfile(absolu),
            "ancre": cid,
        })
    return pistes


def main():
    chapitres = {}
    total, presents = 0, 0
    for page in sorted(glob.glob(os.path.join(SITE, "chapitres", "0*.html"))):
        nom = os.path.basename(page)
        n = int(nom[:2])
        t = io.open(page, encoding="utf-8").read()
        m = re.search(r'<h1[^>]*class="chapter-title"[^>]*>(.*?)</h1>', t, re.S)
        titre = texte_langue(m.group(1)) if m else "Chapitre %d" % n
        pistes = pistes_du_chapitre(n, page)
        chapitres[str(n)] = {"titre": titre, "page": "chapitres/" + nom, "pistes": pistes}
        total += len(pistes)
        presents += sum(1 for p in pistes if p["present"])
        print("  ch%d  %-52s %2d pistes (%d enregistrées)"
              % (n, titre[:52], len(pistes), sum(1 for p in pistes if p["present"])))

    # --- les pages hors chapitre : même index, clé et rang explicites, pour
    #     qu'aucune ne se fasse passer pour un neuvième chapitre.
    # Le libellé console est distinct de la pastille : une console Windows en
    # cp1252 ne sait pas écrire un émoji et le script s'arrêtait dessus.
    for nom, cle, num, ordre, lib in [
            ("about.html", "apropos", "ℹ", 9, "apr")]:
        page = os.path.join(SITE, nom)
        if not os.path.isfile(page):
            continue
        t = io.open(page, encoding="utf-8").read()
        m = re.search(r'<h1[^>]*class="chapter-title"[^>]*>(.*?)</h1>', t, re.S)
        titre = texte_langue(m.group(1)) if m else nom
        pistes = pistes_du_chapitre(None, page)
        if not pistes:
            continue
        chapitres[cle] = {"titre": titre, "page": nom, "num": num,
                          "ordre": ordre, "pistes": pistes}
        total += len(pistes)
        presents += sum(1 for p in pistes if p["present"])
        print("  %-4s %-52s %2d pistes (%d enregistrées)"
              % (lib, titre[:52], len(pistes), sum(1 for p in pistes if p["present"])))

    entete = (
        "/* =================================================================\n"
        "   playlist-data.js — index des pistes audio, tous chapitres\n"
        "   Cours \"Réglementation des données et conformité\"\n"
        "   Auteur : Mohamed EL AFRIT — CC BY-NC-SA 4.0\n\n"
        "   FICHIER GÉNÉRÉ — ne pas modifier à la main.\n"
        "   Régénérer après tout ajout de capsule ou de podcast :\n"
        "       python3 outils/generer_playlist.py\n\n"
        "   L'ordre des pistes est celui du document : c'est celui dans lequel\n"
        "   la lecture automatique enchaîne.\n"
        "   ================================================================= */\n"
        "window.RDC_PLAYLIST = ")
    with io.open(SORTIE, "w", encoding="utf-8", newline="\n") as f:
        f.write(entete)
        f.write(json.dumps(chapitres, ensure_ascii=False, indent=1))
        f.write(";\n")

    print("\n  %s" % os.path.relpath(SORTIE, RACINE).replace(os.sep, "/"))
    print("  %d pistes indexées, %d enregistrées, %d à venir"
          % (total, presents, total - presents))
    return 0


if __name__ == "__main__":
    sys.exit(main())
