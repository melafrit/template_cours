#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reporte les capsules de la fiche de production dans les pages de chapitre.

    python3 outils/synchroniser_capsules.py
    python3 outils/synchroniser_capsules.py --essai   # dit ce qu'il changerait

POURQUOI CE SCRIPT EXISTE

Une capsule audio vit à deux endroits : le script, dans la fiche de production,
et la transcription, affichée sous le lecteur. Ce sont deux versions du même
texte — l'une balisée pour la synthèse vocale, l'autre lisible. Tenues à la
main, elles divergent dès la première correction : on retouche le script,
on régénère l'audio, et la transcription continue d'afficher l'ancienne
version. Personne ne s'en aperçoit, puisqu'on ne lit pas la transcription
d'une capsule qu'on vient d'écouter.

La fiche est donc la source unique. Ce script en extrait les transcriptions et
les écrit dans les pages, avec le nom de fichier audio correspondant.

CONVENTION DE NOMMAGE

    chapitre-<N>-capsule-<langue>.mp3

Le suffixe de langue n'est pas décoratif : une page bilingue doit servir la
capsule de la langue affichée. Sans lui, l'auditeur anglophone entend du
français.
LES FICHES : toutes celles de docs/prompts/ dont le nom commence par
« Capsules » (Capsules_du_cours_demo.md dans le template, Capsules_chapitres.md
dans un cours…). Seules les capsules d'ouverture de chapitre, nommées selon la
convention ci-dessus, sont reportées ici ; une capsule d'un autre genre (schéma,
TP) se synchronise avec l'outil de sa page.
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
FICHES = os.path.join(RACINE, "docs", "prompts", "Capsules*.md")

for flux in (sys.stdout, sys.stderr):
    try:
        flux.reconfigure(encoding="utf-8")
    except Exception:
        pass


def capsules_de_la_fiche():
    """{(chapitre, langue): {'fichier', 'transcription', 'duree'}}"""
    fiches = sorted(glob.glob(FICHES))
    if not fiches:
        sys.exit("Aucune fiche de capsules dans docs/prompts/ (Capsules*.md).")
    t = "\n---\n".join(io.open(f, encoding="utf-8").read() for f in fiches)
    out = {}
    blocs = re.split(r"\n---\n", t)
    for b in blocs:
        m = re.search(r"\*\*Nom exact du fichier :\*\*\s*`([^`]+)`", b)
        if not m:
            continue
        nom = m.group(1)
        n = re.match(r"chapitre-(\d+)-capsule-(fr|en)\.mp3$", nom)
        if not n:
            # podcasts, schémas, TP… : d'autres genres, qui ne vivent pas dans TEXTES
            continue
        tr = re.search(r"\*\*📄 Transcription affichée sur la page\*\*\s*\n+```\n(.*?)\n```",
                       b, re.S)
        if not tr:
            print("  /!\\ %s : pas de transcription dans la fiche" % nom)
            continue
        d = re.search(r"Durée visée :\*\*\s*≈\s*(\d+)\s*s", b)
        secondes = int(d.group(1)) if d else 0
        out[(n.group(1), n.group(2))] = {
            "fichier": nom,
            "transcription": " ".join(x.strip() for x in tr.group(1).strip().split("\n\n")),
            "duree": "%d:%02d" % (secondes // 60, secondes % 60) if secondes else "",
        }
    return out


def injecter(page, chap, caps, essai):
    """Écrit src, durée et transcription dans le bloc TEXTES de la page."""
    t = io.open(page, encoding="utf-8").read()
    avant = t

    for langue in ("fr", "en"):
        c = caps.get((chap, langue))
        if not c:
            continue
        rel = "../assets/media/voix/" + c["fichier"]

        # capsuleSrc : on l'ajoute s'il manque, on le met à jour sinon
        bloc = re.search(r"\n    %s: \{(.*?)\n    \}" % langue, t, re.S)
        if not bloc:
            print("  /!\\ %s : bloc « %s » introuvable" % (os.path.basename(page), langue))
            continue
        corps = bloc.group(1)
        neuf = corps
        if "capsuleSrc:" in neuf:
            neuf = re.sub(r'capsuleSrc: "[^"]*"', 'capsuleSrc: %s' % json.dumps(rel), neuf)
        else:
            neuf = re.sub(r'(\n      capsuleTitre:)',
                          '\n      capsuleSrc: %s,\\1' % json.dumps(rel), neuf, count=1)
        neuf = re.sub(r'capsuleTrans: "(?:[^"\\]|\\.)*"',
                      'capsuleTrans: %s' % json.dumps(c["transcription"], ensure_ascii=False),
                      neuf)
        t = t.replace(corps, neuf, 1)

    # l'appel RDCX.voice doit lire la source de la langue active
    t = re.sub(r"src: '\.\./assets/media/voix/chapitre-\d+-capsule[^']*'",
               "src: X.capsuleSrc", t)
    d = caps.get((chap, "fr"), {}).get("duree")
    if d:
        t = re.sub(r"(RDCX\.voice\('capsule-\d+', \{[^}]*?duree: )'[^']*'",
                   r"\g<1>'%s'" % d, t, flags=re.S)

    if t == avant:
        return False
    if not essai:
        io.open(page, "w", encoding="utf-8", newline="\n").write(t)
    return True


def main():
    ap = argparse.ArgumentParser(description="Synchronise les capsules avec la fiche.")
    ap.add_argument("--essai", action="store_true")
    args = ap.parse_args()

    caps = capsules_de_la_fiche()
    print("\nFiche\n-----")
    for (ch, lg), c in sorted(caps.items()):
        print("  ch%s %s  %-32s %s  %d mots"
              % (ch, lg, c["fichier"], c["duree"] or "  —  ",
                 len(c["transcription"].split())))

    print("\nPages\n-----")
    touchees = 0
    for f in sorted(os.listdir(os.path.join(SITE, "chapitres"))):
        m = re.match(r"^(\d{2})-", f)
        if not m:
            continue
        chap = str(int(m.group(1)))
        if not any(k[0] == chap for k in caps):
            continue
        page = os.path.join(SITE, "chapitres", f)
        if injecter(page, chap, caps, args.essai):
            touchees += 1
            print("  %-28s mis à jour" % f)
        else:
            print("  %-28s déjà à jour" % f)

    if args.essai:
        print("\n  Simulation : rien n'a été écrit.")
    else:
        print("\n  %d page(s) modifiée(s)." % touchees)
        print("  Générez ensuite les capsules :  python3 outils/generer_audio.py --essai")
    return 0


if __name__ == "__main__":
    sys.exit(main())
