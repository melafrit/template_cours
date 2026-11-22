#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Écrit site/assets/css/filieres.css : le masquage du contenu propre à une filière, d'après les filières déclarées
dans site/assets/js/course-data.js (COURSE.filieres).

    python3 outils/generer_filieres.py           # écrit le fichier s'il change
    python3 outils/generer_filieres.py --essai   # n'écrit rien ; code 1 si le fichier n'est pas à jour

Un cours commun à deux filières (EADL et ERIS, CDWFS et ASRC…) porte dans ses pages le contenu des deux : un bloc
propre à une filière a la classe only-<id> (only-eadl, only-eris). Quand l'étudiant a choisi sa filière, <html> porte
data-filiere="<id>" (posé avant l'affichage par trois lignes en tête de page, puis par assets/js/filiere.js), et ce
fichier masque le contenu des autres. Sans choix, les deux versions restent affichées, étiquetées de leur sigle et
bordées de la couleur de leur filière : c'est la vue du formateur en groupe mixte. La couleur est le --primary de la
palette de la filière (palettes.css), vérifiée en contraste, en clair comme en sombre. Sans choix toujours, deux
mentions accolées en ligne, comme la pastille de l'accueil, sont séparées d'une barre (le modèle du cours EADL).

Un sélecteur CSS ne peut pas comparer la filière de <html> à la classe d'un bloc : les règles s'écrivent donc pour
les filières du cours, d'où ce générateur. Une seule filière, ou aucune : le fichier n'a pas de règle, et filiere.js
ne pose pas de bascule. À relancer après tout changement des filières de course-data.js ; nouveau_cours.py le lance
à la création d'un cours. Décision de l'auteur du 21 novembre 2026 (lot 1 du grand chantier), d'après la bascule du
cours EADL.
"""
import argparse
import io
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

for flux in (sys.stdout, sys.stderr):
    try:
        flux.reconfigure(encoding="utf-8")
    except Exception:
        pass

ENTETE = """/* =================================================================
   filieres.css — Le contenu propre à une filière (classes only-<id>)
   FICHIER GÉNÉRÉ par outils/generer_filieres.py, d'après les filières de
   site/assets/js/course-data.js : ne pas le modifier à la main. Une
   filière choisie (html[data-filiere]) masque le contenu des autres ;
   sans choix, chaque version s'affiche, étiquetée et bordée de la couleur
   de sa filière (le --primary de sa palette, palettes.css).
   ================================================================= */
"""


def filieres(racine):
    """[(id, sigle, palette)] d'après COURSE.filieres de course-data.js, dans l'ordre déclaré."""
    src = io.open(os.path.join(racine, "site", "assets", "js", "course-data.js"), encoding="utf-8").read()
    m = re.search(r"\bfilieres\s*:\s*\[(.*?)\n\s*\]", src, flags=re.S)
    if not m:
        return []
    out = []
    for e in re.finditer(r"\{\s*id:\s*['\"]([a-z0-9-]+)['\"]\s*,\s*code:\s*['\"]([^'\"]+)['\"]\s*,\s*palette:\s*"
                         r"['\"]([a-z]+)['\"]", m.group(1)):
        out.append(e.groups())
    return out


def couleurs(racine, palette):
    """(--primary clair, --primary sombre) de la palette, d'après palettes.css ; None si la palette est inconnue."""
    src = io.open(os.path.join(racine, "site", "assets", "css", "palettes.css"), encoding="utf-8").read()
    clair = re.search(r'html\[data-accent="%s"\]\s*\{[^}]*?--primary:\s*([^;]+);' % re.escape(palette), src)
    sombre = re.search(r'html\[data-accent="%s"\]\[data-theme="dark"\]\s*\{[^}]*?--primary:\s*([^;]+);'
                       % re.escape(palette), src)
    return (clair.group(1).strip(), sombre.group(1).strip()) if clair and sombre else None


def produire(racine):
    """Le texte de filieres.css, et les erreurs (palette inconnue)."""
    liste, erreurs = filieres(racine), []
    if len(liste) < 2:
        return ENTETE + "/* Une seule filière, ou aucune : rien à masquer. */\n", erreurs
    ids = [f[0] for f in liste]
    lignes = ["/* Une filière choisie : le contenu des autres disparaît. Un sélecteur par ligne. */"]
    morceaux = ['html[data-filiere="%s"] .only-%s' % (f, g) for f in ids for g in ids if g != f]
    lignes.append(",\n".join(morceaux) + " { display: none !important; }")
    lignes.append("")
    lignes.append("/* Le sigle et la couleur de chaque filière : ceux de l'étiquette, sans filière choisie. */")
    sombres = []
    for ident, sigle, palette in liste:
        c = couleurs(racine, palette)
        if not c:
            erreurs.append("filière %s : palette « %s » inconnue de palettes.css" % (ident, palette))
            continue
        lignes.append('.only-%s { --f-etiquette: "%s"; --f-couleur: %s; }' % (ident, sigle.replace('"', ""), c[0]))
        sombres.append('html[data-theme="dark"] .only-%s { --f-couleur: %s; }' % (ident, c[1]))
    lignes += sombres
    lignes.append("")
    lignes.append("/* Sans filière choisie, chaque bloc propre à une filière s'affiche étiqueté : la vue du formateur. */")
    blocs = ",\n".join("html:not([data-filiere]) %s.only-%s" % (balise, ident)
                       for ident in ids for balise in ("div", "section", "aside"))
    lignes.append(blocs + " {\n  position: relative; border-inline-start: 4px solid var(--f-couleur);\n"
                  "  padding-inline-start: var(--space-4); margin-top: var(--space-6);\n}")
    avant = ",\n".join("html:not([data-filiere]) %s.only-%s::before" % (balise, ident)
                       for ident in ids for balise in ("div", "section", "aside"))
    lignes.append(avant + " {\n  content: var(--f-etiquette); position: absolute; top: -1.4em; inset-inline-start: 0;\n"
                  "  font-family: var(--font-display); font-size: var(--fs-xs); font-weight: 700;\n"
                  "  color: var(--f-couleur); background: var(--bg-card); border: 1px solid var(--f-couleur);\n"
                  "  padding: 0 8px; border-radius: var(--radius-sm); line-height: 1.6;\n}")
    lignes.append("")
    lignes.append("/* En ligne, deux mentions accolées (<span class=\"only-a\">…</span><span class=\"only-b\">…</span>,\n"
                  "   la pastille de l'accueil) se liraient d'un seul tenant sans filière choisie : une barre les sépare. */")
    paires = ",\n".join("html:not([data-filiere]) span.only-%s + span.only-%s::before" % (f, g)
                        for f in ids for g in ids if g != f)
    lignes.append(paires + " {\n  content: \" / \"; font-weight: 400;\n}")
    return ENTETE + "\n".join(lignes) + "\n", erreurs


def generer(racine=RACINE, essai=False):
    """Écrit filieres.css s'il change ; rend (à jour avant ?, nombre de filières, erreurs)."""
    cible = os.path.join(racine, "site", "assets", "css", "filieres.css")
    texte, erreurs = produire(racine)
    actuel = io.open(cible, encoding="utf-8").read() if os.path.isfile(cible) else ""
    a_jour = actuel == texte
    if not a_jour and not essai and not erreurs:
        with io.open(cible, "w", encoding="utf-8", newline="\n") as f:
            f.write(texte)
    return a_jour, len(filieres(racine)), erreurs


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--essai", action="store_true", help="n'écrit rien ; code 1 si le fichier n'est pas à jour")
    args = ap.parse_args()
    a_jour, n, erreurs = generer(essai=args.essai)
    for e in erreurs:
        print("  ✗", e)
    if erreurs:
        print("filieres.css : NON écrit")
        return 1
    print("filieres.css : %d filière(s), %s" % (n, "à jour" if a_jour else ("PAS À JOUR (rien écrit)" if args.essai
                                                                         else "écrit")))
    return 1 if (args.essai and not a_jour) else 0


if __name__ == "__main__":
    sys.exit(main())
