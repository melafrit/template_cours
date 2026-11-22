#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Écrit site/assets/js/nav-sections.js (window.RDC_SECTIONS) d'après les <h2 id> des chapitres.

    python3 outils/generer_nav_sections.py           # écrit le fichier s'il change
    python3 outils/generer_nav_sections.py --essai   # n'écrit rien ; code 1 si le fichier n'est pas à jour

Les chapitres sont ceux de site/assets/js/course-data.js (num, file) ; chacun donne ses sections, une par <h2 id="…">
de son fichier, dans l'ordre de la page. Le libellé vient des blocs data-tr du titre ({fr, en}), sinon de son texte.
nouveau_cours.py le lance à la création d'un cours : sans lui, un cours créé gardait dans son menu les sections du
cours de démonstration. À relancer après tout ajout, retrait ou renommage de section.
"""
import html
import io
import json
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Les langues du site miroir ; la racine est celle que déclare l'accueil, les autres vivent dans leur dossier.
LANGUES = ("fr", "en", "ar")

ENTETE = """/* =================================================================
   nav-sections.js — Sous-sections de chaque chapitre, pour le menu
   FICHIER GÉNÉRÉ par outils/generer_nav_sections.py, d'après les titres
   <h2 id> des pages de chapitre : ne pas le modifier à la main.
   ================================================================= */
"""


def _texte(fragment):
    """Le texte lisible d'un fragment HTML : balises ôtées, entités décodées, espaces resserrés."""
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", fragment))).strip()


def chapitres(racine):
    """[(num, fichier)] d'après course-data.js, dans l'ordre du cours."""
    chemin = os.path.join(racine, "site", "assets", "js", "course-data.js")
    src = io.open(chemin, encoding="utf-8").read()
    bloc = src.split("chapters", 1)[1].split("]", 1)[0]
    return re.findall(r"num:\s*['\"]([^'\"]+)['\"][^}]*?file:\s*['\"]([^'\"]+)['\"]", bloc, flags=re.S)


def sections(chemin):
    """[{t, id}] : chaque <h2 id> du chapitre ; t vaut {fr, en} si le titre est bilingue."""
    src = io.open(chemin, encoding="utf-8").read()
    src = re.sub(r"<script\b.*?</script>", "", src, flags=re.S | re.I)
    out = []
    for m in re.finditer(r'<h2\b[^>]*\bid="([^"]+)"[^>]*>(.*?)</h2>', src, flags=re.S | re.I):
        ident, corps = m.group(1), m.group(2)
        langues = dict((lg, _texte(t)) for lg, t in re.findall(r'data-tr="(fr|en)"[^>]*>(.*?)</span>', corps, flags=re.S))
        titre = langues if len(langues) == 2 else (next(iter(langues.values())) if langues else _texte(corps))
        out.append({"t": titre, "id": ident})
    return out


def langue_racine(racine):
    """La langue des pages de la racine du site : celle que déclare l'accueil, le français à défaut."""
    try:
        t = io.open(os.path.join(racine, "site", "index.html"), encoding="utf-8").read()
    except OSError:
        return "fr"
    m = re.search(r'<html\b[^>]*\blang="([a-z]{2})', t)
    return m.group(1) if m and m.group(1) in LANGUES else "fr"


def produire(racine):
    """Le texte de nav-sections.js pour le site de racine. En site miroir (docs/I18N.md), le titre d'une section dans
    une autre langue vient de la jumelle site/<langue>/chapitres/<fichier>, à identifiant égal."""
    lr = langue_racine(racine)
    donnees = {}
    for num, fichier in chapitres(racine):
        p = os.path.join(racine, "site", "chapitres", fichier)
        if not os.path.isfile(p):
            continue
        secs = sections(p)
        for lg in LANGUES:
            jumelle = os.path.join(racine, "site", lg, "chapitres", fichier)
            if lg == lr or not os.path.isfile(jumelle):
                continue
            traduits = {s["id"]: s["t"] for s in sections(jumelle)}
            for s in secs:
                t = traduits.get(s["id"])
                t = (t.get(lg) or t.get("fr")) if isinstance(t, dict) else t
                if t:
                    s["t"] = dict(s["t"]) if isinstance(s["t"], dict) else {lr: s["t"]}
                    s["t"][lg] = t
        donnees[num] = secs
    return ENTETE + "window.RDC_SECTIONS = " + json.dumps(donnees, ensure_ascii=False, indent=1) + ";\n"


def generer(racine, essai=False):
    """Écrit nav-sections.js s'il change ; rend (à jour avant ?, nombre de chapitres, nombre de sections)."""
    cible = os.path.join(racine, "site", "assets", "js", "nav-sections.js")
    texte = produire(racine)
    actuel = io.open(cible, encoding="utf-8").read() if os.path.isfile(cible) else ""
    donnees = json.loads(texte.split("window.RDC_SECTIONS = ", 1)[1].rstrip().rstrip(";"))
    a_jour = actuel == texte
    if not a_jour and not essai:
        with io.open(cible, "w", encoding="utf-8", newline="\n") as f:
            f.write(texte)
    return a_jour, len(donnees), sum(len(v) for v in donnees.values())


def main():
    essai = "--essai" in sys.argv[1:]
    a_jour, nch, nsec = generer(RACINE, essai)
    etat = "à jour" if a_jour else ("PAS À JOUR — rien écrit" if essai else "écrit")
    print("nav-sections.js : %d chapitre(s), %d section(s), %s" % (nch, nsec, etat))
    return 1 if (essai and not a_jour) else 0


if __name__ == "__main__":
    sys.exit(main())
