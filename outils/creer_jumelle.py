#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prépare la jumelle anglaise d'une page française du site miroir, à traduire (docs/I18N.md, partie A).

    python3 outils/creer_jumelle.py chapitres/01-x.html [autres pages…]   # chemins depuis la racine du site
    python3 outils/creer_jumelle.py --essai chapitres/01-x.html           # ce qui serait fait, sans rien écrire

Pour chaque page française X.html, l'outil écrit site/en/X.html : la même page, déclarée en anglais
(<html lang="en" data-langues="en">), ses chemins vers les fichiers partagés descendus d'un cran, ses liens vers les
pages qui ont une jumelle gardés tels quels (les autres mènent à la page française : liens_langues.py les marque),
la liste des pages traduites chargée après i18n.js — et, en tête de son contenu, la marque « À TRADUIRE ». Le texte,
lui, reste français : la traduction suit, bloc pour bloc, sans rien ajouter ni retirer (le bouton FR / EN retrouve
le paragraphe lu par son rang). verifier_parite.py refuse la jumelle tant que la marque est là.

La page française reçoit data-langues="fr" si elle ne l'a pas : navigation.js y charge alors le bouton FR / EN.
Une page en blocs data-tr se convertit avec data_tr_vers_miroir.py, pas avec cet outil ; une jumelle qui existe
déjà n'est jamais écrasée. Ensuite : generer_langues.py et liens_langues.py, que l'outil lance lui-même.
"""
import argparse
import importlib.util
import io
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(RACINE, "site")
sys.path.insert(0, os.path.join(RACINE, "outils"))
import generer_langues  # noqa: E402
import miroir  # noqa: E402

for flux in (sys.stdout, sys.stderr):
    try:
        flux.reconfigure(encoding="utf-8")
    except Exception:
        pass


def marquer(t):
    """La marque « À TRADUIRE », juste après l'ouverture du contenu principal (ou de <body>)."""
    m = re.search(r"<main\b[^>]*>", t) or re.search(r"<body\b[^>]*>", t)
    if not m:
        return miroir.A_TRADUIRE + "\n" + t
    return t[:m.end()] + "\n" + miroir.A_TRADUIRE + t[m.end():]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("pages", nargs="+", help="chemins des pages françaises, depuis la racine du site")
    ap.add_argument("--essai", action="store_true", help="dit ce qui serait fait, sans rien écrire")
    args = ap.parse_args()
    if os.path.exists(os.path.join(RACINE, "nouveau_cours.py")):
        sys.exit("Le gabarit garde sa démonstration en blocs data-tr : lancez cet outil dans un cours (docs/I18N.md).")

    demandees = [p.replace("\\", "/").lstrip("./") for p in args.pages]
    jumelles = set(generer_langues.pages_traduites(SITE)) | set(demandees)
    ecrits, erreurs = {}, []
    for rel in demandees:
        fr_p, en_p = os.path.join(SITE, *rel.split("/")), os.path.join(SITE, "en", *rel.split("/"))
        if rel.startswith(("en/", "assets/")) or not rel.endswith(".html"):
            erreurs.append("%s : une page française du site, hors en/ et assets/" % rel)
            continue
        if not os.path.isfile(fr_p):
            erreurs.append("%s : page introuvable" % rel)
            continue
        if os.path.exists(en_p):
            erreurs.append("en/%s existe déjà : jamais écrasée" % rel)
            continue
        t = io.open(fr_p, encoding="utf-8").read()
        if miroir.bilingue(t):
            erreurs.append("%s : page en blocs data-tr — data_tr_vers_miroir.py la convertit" % rel)
            continue
        if 'data-langues="fr"' not in t:
            ecrits[fr_p] = miroir.declarer(t, "fr")
        en, liste = miroir.charger_liste(miroir.reloger(miroir.declarer(t, "en"), rel, jumelles, SITE))
        ecrits[en_p] = marquer(en)
        print("  ✓ %s → en/%s%s" % (rel, rel, "" if liste else " (✗ i18n.js introuvable : liste non chargée)"))
    for e in erreurs:
        print("  ✗", e)
    if erreurs:
        sys.exit("%d page(s) en erreur : rien n'est écrit." % len(erreurs))
    if args.essai:
        print("Essai : %d fichier(s) seraient écrits." % len(ecrits))
        return 0
    for chemin, texte in ecrits.items():
        os.makedirs(os.path.dirname(chemin), exist_ok=True)
        with io.open(chemin, "w", encoding="utf-8", newline="\n") as f:
            f.write(texte)
    _a_jour, traduites = generer_langues.generer(SITE)
    print("langues-data.js : %d page(s) traduite(s)" % len(traduites))
    spec = importlib.util.spec_from_file_location("liens_langues", os.path.join(RACINE, "outils", "liens_langues.py"))
    liens = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(liens)
    sys.argv = [sys.argv[0]]
    liens.main()
    print("À traduire maintenant, bloc pour bloc, puis retirer la marque « À TRADUIRE » ; verifier_parite.py dira "
          "quand la jumelle est prête.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
