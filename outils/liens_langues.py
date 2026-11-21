#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Les liens des jumelles du site miroir, toujours branchés (docs/I18N.md, partie A).

    python3 outils/liens_langues.py           # réécrit les liens qui doivent changer
    python3 outils/liens_langues.py --essai   # les liste sans rien écrire ; code 1 s'il y en a

Une jumelle de site/<langue>/ (en/, ar/…) vise les jumelles, dans sa langue, des pages qu'elle cite. Tant qu'une
jumelle manque (chaque langue se publie lot par lot), le lien part vers la page de la racine, marqué de sa langue
(hreflang="fr") : la feuille de style y ajoute la mention « FR ». Dès que la jumelle existe, il revient vers elle. La
règle ne dépend que des fichiers présents : relancer l'outil après chaque lot suffit.

Sont traités : les attributs href des liens <a>, et, dans les scripts de la page, les chaînes qui sont des chemins
relatifs de pages (les renvois « Pour approfondir » des activités). Les fichiers partagés (assets/) ne bougent pas.
Les documents à télécharger suivent la même règle en anglais, d'après la table de outils/documents_en.py ; une autre
langue garde les documents de la racine. Repris du cours d'architecture logicielle, étendu à plusieurs langues le
21 novembre 2026.
"""
import argparse
import glob
import io
import os
import posixpath
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(RACINE, "site")
sys.path.insert(0, os.path.join(RACINE, "outils"))
import documents_en as DOC  # noqa: E402
import generer_langues  # noqa: E402

DOCUMENTS = tuple({os.path.splitext(c)[1] for c in DOC.DOCUMENTS})          # .pdf, .docx, .zip…
DOCUMENTS_FR = {en: fr for fr, en in DOC.DOCUMENTS.items()}                 # document anglais → son jumeau français

for flux in (sys.stdout, sys.stderr):
    try:
        flux.reconfigure(encoding="utf-8")
    except Exception:
        pass

LIEN = re.compile(r'<a\b([^>]*?)\bhref="([^"]+)"([^>]*)>')
CHAINE_JS = re.compile(r'(["\'])((?:\.\./)*[A-Za-z0-9_./-]+\.html(?:#[^"\']*)?)\1')
SCRIPT = re.compile(r"(<script\b[^>]*>)(.*?)(</script>)", re.S)


def existe(rel):
    return os.path.isfile(os.path.join(SITE, *rel.split("/")))


def corriger(dossier_page, href, lg, racine):
    """Le lien corrigé (ou None s'il est bon) et la langue de sa cible (lg, racine, ou None si ce n'est pas une
    page), pour une jumelle de la langue lg."""
    if re.match(r"^[a-z]+:|^#|^//", href):
        return None, None
    chemin, _, ancre = href.partition("#")
    chemin, _, requete = chemin.partition("?")
    suite = ("?" + requete if requete else "") + ("#" + ancre if ancre else "")
    if DOCUMENTS and chemin.endswith(DOCUMENTS):
        return corriger_document(dossier_page, chemin, suite) if lg == "en" else (None, None)
    if not chemin.endswith(".html"):
        return None, None
    cible = posixpath.normpath(posixpath.join(dossier_page, chemin))
    if cible.startswith(lg + "/"):
        if existe(cible):
            return None, lg
        r = cible[len(lg) + 1:]
        if existe(r):
            return posixpath.relpath(r, dossier_page) + suite, racine
        return None, None                                   # ni l'une ni l'autre : verifier_liens le signalera
    if not cible.startswith("../") and existe(lg + "/" + cible):
        return posixpath.relpath(lg + "/" + cible, dossier_page) + suite, lg
    return None, racine if existe(cible) else None


def corriger_document(dossier_page, chemin, suite):
    """La même règle pour un document à télécharger (outils/documents_en.py) : le jumeau anglais s'il existe, sinon
    le français, marqué. Un document sans jumeau prévu ne bouge pas, sans marque."""
    cible = posixpath.normpath(posixpath.join(dossier_page, chemin))
    if cible in DOCUMENTS_FR:                                   # un document anglais
        if existe(cible):
            return None, "en"
        return posixpath.relpath(DOCUMENTS_FR[cible], dossier_page) + suite, "fr"
    en = DOC.DOCUMENTS.get(cible)
    if not en:
        return None, None
    if existe(en):
        return posixpath.relpath(en, dossier_page) + suite, "en"
    return None, "fr"


def traiter(page, lg, racine):
    rel = os.path.relpath(page, SITE).replace("\\", "/")
    dossier = posixpath.dirname(rel)
    texte = io.open(page, encoding="utf-8").read()
    changes = []
    marque_racine = 'hreflang="%s"' % racine

    def lien(m):
        avant, href, apres = m.group(1), m.group(2), m.group(3)
        neuf, langue = corriger(dossier, href, lg, racine)
        attrs = avant + apres
        marque = marque_racine in attrs
        if neuf:
            changes.append("%s → %s" % (href, neuf))
            href = neuf
        if langue == racine and not marque:
            apres = apres + " " + marque_racine
        elif langue == lg and marque:
            avant, apres = avant.replace(" " + marque_racine, ""), apres.replace(" " + marque_racine, "")
        return '<a' + avant + 'href="' + href + '"' + apres + '>'

    def script(m):
        def chaine(mm):
            neuf, _langue = corriger(dossier, mm.group(2), lg, racine)
            if not neuf:
                return mm.group(0)
            changes.append("%s → %s (script)" % (mm.group(2), neuf))
            return mm.group(1) + neuf + mm.group(1)
        return m.group(1) + CHAINE_JS.sub(chaine, m.group(2)) + m.group(3)

    neuf = SCRIPT.sub(script, LIEN.sub(lien, texte))
    return rel, texte, neuf, changes


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--essai", action="store_true", help="liste les liens à corriger sans rien écrire")
    args = ap.parse_args()
    racine = generer_langues.langue_racine(SITE)
    total = 0
    for lg in generer_langues.LANGUES:
        if lg == racine:
            continue
        for page in sorted(glob.glob(os.path.join(SITE, lg, "**", "*.html"), recursive=True)):
            rel, ancien, neuf, changes = traiter(page, lg, racine)
            if neuf == ancien:
                continue
            total += max(1, len(changes))
            print("  %s : %d lien(s)" % (rel, len(changes)) + ("" if changes else " (marques hreflang)"))
            for c in changes[:8]:
                print("      ", c)
            if len(changes) > 8:
                print("       … et %d autres" % (len(changes) - 8))
            if not args.essai:
                io.open(page, "w", encoding="utf-8", newline="\n").write(neuf)
    print("%d lien(s) %s." % (total, "à corriger" if args.essai else "corrigé(s)"))
    return 1 if (args.essai and total) else 0


if __name__ == "__main__":
    sys.exit(main())
