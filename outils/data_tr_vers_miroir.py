#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fait passer un cours en blocs data-tr au site miroir : chaque page bilingue devient une page française et sa
jumelle anglaise, sous site/en/ (docs/I18N.md).

    python3 outils/data_tr_vers_miroir.py --essai   # ce qui serait fait, sans rien écrire
    python3 outils/data_tr_vers_miroir.py           # convertit

Pour chaque page de site/ (hors site/en/ et site/assets/) qui porte des blocs data-tr :
- la page française garde ses blocs data-tr="fr", sans l'attribut, et perd les anglais ; elle se déclare
  <html lang="fr" data-lang="fr" data-langues="fr"> ;
- sa jumelle site/en/<même chemin> garde les blocs anglais et perd les français ; elle se déclare en anglais ;
  ses chemins vers les fichiers partagés descendent d'un cran, ses liens vers les autres pages converties restent
  tels quels ; elle charge la liste des pages traduites (langues-data.js) juste après i18n.js ;
- un attribut à version anglaise (data-step-titre-en…) donne sa valeur à la jumelle et quitte les deux pages.

Les scripts des pages ne changent pas, sauf leurs chemins de fichiers dans les jumelles : les objets TEXTES = { fr,
en } et les attributs data-i18n-*-fr/-en restent, le moteur choisit la langue de la page (outils/miroir.py). Le
titre d'un chapitre vient de course-data.js ; un autre titre qui mêle les deux langues se coupe au « / », ou se
réduit au titre du cours ; sinon il reste à traduire, et l'outil le dit. Rien ne s'écrit si une page contient un
bloc mal fermé.

La conversion appelle ensuite generer_langues.py et generer_nav_sections.py ; restent liens_langues.py,
hreflang.py, verifier_parite.py, verifier_liens.py, verifier_i18n.py, et la recette au navigateur.
Le gabarit garde sa démonstration en blocs data-tr, le modèle de secours : l'outil refuse d'y tourner.
"""
import argparse
import glob
import importlib.util
import io
import os
import posixpath
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(RACINE, "site")
sys.path.insert(0, os.path.join(RACINE, "outils"))
import miroir  # noqa: E402

for flux in (sys.stdout, sys.stderr):
    try:
        flux.reconfigure(encoding="utf-8")
    except Exception:
        pass


def titres_du_cours():
    """(titre du cours (fr, en), {fichier : (titre fr, titre en, numéro)}) d'après site/assets/js/course-data.js."""
    try:
        src = io.open(os.path.join(SITE, "assets", "js", "course-data.js"), encoding="utf-8").read()
    except OSError:
        return None, {}
    m = re.search(r"\btitle:\s*\{\s*fr:\s*\"([^\"]*)\",\s*en:\s*\"([^\"]*)\"", src)
    cours = (m.group(1), m.group(2)) if m else None
    chapitres = {}
    for m in re.finditer(r"num:\s*'([^']+)'[^}]*?file:\s*'([^']+)'[^}]*?title:\s*\{\s*fr:\s*\"([^\"]*)\",\s*en:\s*"
                         r"\"([^\"]*)\"", src, flags=re.S):
        chapitres[m.group(2)] = (m.group(3), m.group(4), m.group(1))
    return cours, chapitres


def couper_titre(t, rel, cours, chapitres):
    """(titre fr, titre en, d'où il vient) pour une page bilingue, ou None si l'outil ne sait pas le couper : il
    n'invente pas de traduction. Un chapitre prend son titre dans course-data.js ; « A / B » se coupe au « / » ; un
    titre qui porte le titre du cours dans les deux langues se réduit à chacun."""
    m = re.search(r"<title>(.*?)</title>", t, flags=re.S)
    if not m:
        return None
    titre = " ".join(m.group(1).split())
    f = posixpath.basename(rel)
    if rel.startswith("chapitres/") and f in chapitres:
        fr, en, num = chapitres[f]
        return "Chapitre %s — %s" % (num, fr), "Chapter %s — %s" % (num, en), "course-data.js"
    if " / " in titre:
        a, b = (x.strip() for x in titre.rsplit(" / ", 1))
        if a and b:
            return a, b, "coupé au « / »"
    if cours and cours[0] in titre and cours[1] in titre:
        return cours[0], cours[1], "le titre du cours, course-data.js"
    return None


def poser_titre(t, titre):
    return re.sub(r"<title>.*?</title>", lambda m: "<title>%s</title>" % titre, t, count=1, flags=re.S)


def charger_module(nom):
    spec = importlib.util.spec_from_file_location(nom, os.path.join(RACINE, "outils", nom + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--essai", action="store_true", help="dit ce qui serait fait, sans rien écrire")
    args = ap.parse_args()
    if os.path.exists(os.path.join(RACINE, "nouveau_cours.py")):
        sys.exit("Le gabarit garde sa démonstration en blocs data-tr, le modèle de secours : lancez cet outil dans "
                 "un cours (docs/I18N.md).")

    pages = sorted(os.path.relpath(p, SITE).replace("\\", "/")
                   for p in glob.glob(os.path.join(SITE, "**", "*.html"), recursive=True))
    pages = [p for p in pages if not p.startswith(("en/", "assets/"))]
    textes = {p: io.open(os.path.join(SITE, *p.split("/")), encoding="utf-8").read() for p in pages}
    bilingues = [p for p in pages if miroir.bilingue(textes[p])]
    jumelles = set(bilingues) | {os.path.relpath(p, os.path.join(SITE, "en")).replace("\\", "/")
                                 for p in glob.glob(os.path.join(SITE, "en", "**", "*.html"), recursive=True)}
    cours, chapitres = titres_du_cours()

    ecrits, rapports, erreurs = {}, [], []
    for rel in bilingues:
        t = textes[rel]
        try:
            fr = miroir.declarer(miroir.garder_langue(t, "fr"), "fr")
            en = miroir.declarer(miroir.garder_langue(t, "en"), "en")
        except miroir.ErreurBloc as e:
            erreurs.append("%s : %s" % (rel, e))
            continue
        en = miroir.reloger(en, rel, jumelles, SITE)
        en, liste = miroir.charger_liste(en)
        coupe = couper_titre(t, rel, cours, chapitres)
        if coupe:
            fr, en = poser_titre(fr, coupe[0]), poser_titre(en, coupe[1])
        rapports.append((rel, coupe, liste))
        ecrits[os.path.join(SITE, *rel.split("/"))] = fr
        ecrits[os.path.join(SITE, "en", *rel.split("/"))] = en

    for rel in pages:
        if rel not in bilingues:
            print("  · %s : sans bloc anglais, laissée telle quelle (pas de jumelle)" % rel)
    for rel, coupe, liste in rapports:
        print("  ✓ %s → en/%s" % (rel, rel))
        print("      titre : %s" % ("« %s » / « %s » (%s)" % coupe if coupe else "inchangé, à traduire à la main"))
        if not liste:
            print("      ✗ i18n.js introuvable : la liste des pages traduites n'est pas chargée par la jumelle")
    for e in erreurs:
        print("  ✗", e)
    if erreurs:
        sys.exit("%d page(s) en erreur : rien n'est écrit." % len(erreurs))
    print("%d page(s) bilingue(s) → %d page(s) française(s) et %d jumelle(s) anglaise(s)%s."
          % (len(bilingues), len(bilingues), len(bilingues), " (essai : rien n'est écrit)" if args.essai else ""))
    if args.essai or not bilingues:
        return 0

    for chemin, texte in ecrits.items():
        os.makedirs(os.path.dirname(chemin), exist_ok=True)
        with io.open(chemin, "w", encoding="utf-8", newline="\n") as f:
            f.write(texte)
    _a_jour, traduites = charger_module("generer_langues").generer()
    print("langues-data.js : %d page(s) traduite(s)" % len(traduites))
    _a_jour, nch, nsec = charger_module("generer_nav_sections").generer(RACINE)
    print("nav-sections.js : %d chapitre(s), %d section(s)" % (nch, nsec))
    print("Ensuite : liens_langues.py, hreflang.py, verifier_parite.py, verifier_liens.py, verifier_i18n.py, et la "
          "recette au navigateur.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
