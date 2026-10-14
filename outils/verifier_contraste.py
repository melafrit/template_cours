#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vérifie le contraste des palettes de site/assets/css/palettes.css.

    python3 outils/verifier_contraste.py

Une palette n'est pas qu'une affaire de goût : une couleur d'accent mal
choisie rend un titre illisible en thème sombre, et personne ne s'en aperçoit
avant qu'un étudiant s'en plaigne. Ce script mesure, pour chaque palette et
dans les deux thèmes, les rapports de contraste des usages réels de --primary
et --accent, et échoue si l'un d'eux passe sous le seuil.

Seuils retenus (WCAG 2.1) :
  - texte normal      : 4,5:1 (niveau AA)
  - texte large/gras  : 3,0:1 (niveau AA large — titres, badges)
  - éléments non textuels (bordures, pastilles) : 3,0:1

À lancer après toute modification de palettes.css, et avant de livrer une
palette nouvelle. Sort en code 1 si un couple échoue : utilisable en CI.
"""

import io
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PALETTES = os.path.join(RACINE, "site", "assets", "css", "palettes.css")
MAIN = os.path.join(RACINE, "site", "assets", "css", "main.css")

# La console Windows n'est pas en UTF-8 par défaut : sans cela, les accents des
# messages sortent en charabia. Sans effet sur macOS et Linux.
for flux in (sys.stdout, sys.stderr):
    try:
        flux.reconfigure(encoding="utf-8")
    except Exception:
        pass


# ---------------------------------------------------------------- couleurs
def rvb(c):
    c = c.strip().lstrip("#")
    if len(c) == 3:
        c = "".join(x * 2 for x in c)
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def luminance(c):
    def canal(v):
        v /= 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (canal(x) for x in rvb(c))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contraste(a, b):
    la, lb = luminance(a), luminance(b)
    clair, sombre = max(la, lb), min(la, lb)
    return (clair + 0.05) / (sombre + 0.05)


# ---------------------------------------------------------------- lecture CSS
def bloc(texte, selecteur):
    """Les déclarations d'un bloc CSS, en {variable: valeur}."""
    m = re.search(re.escape(selecteur) + r"\s*\{(.*?)\}", texte, re.S)
    if not m:
        return {}
    d = {}
    for ligne in m.group(1).split(";"):
        if ":" in ligne:
            k, v = ligne.split(":", 1)
            d[k.strip()] = v.strip()
    return d


def fonds():
    """Les fonds et textes de la charte commune, pour les deux thèmes."""
    t = io.open(MAIN, encoding="utf-8").read()
    clair = bloc(t, ":root")
    sombre = bloc(t, '[data-theme="dark"]')
    return clair, sombre


def palettes():
    """{nom: {'clair': {...}, 'sombre': {...}}}"""
    t = io.open(PALETTES, encoding="utf-8").read()
    out = {}
    for nom in re.findall(r'html\[data-accent="([a-z]+)"\]\s*\{', t):
        out.setdefault(nom, {})
    for nom in out:
        out[nom]["clair"] = bloc(t, 'html[data-accent="%s"]' % nom)
        out[nom]["sombre"] = bloc(t, 'html[data-accent="%s"][data-theme="dark"]' % nom)
    return out


# ---------------------------------------------------------------- contrôles
# (libellé, variable testée, variable de fond, seuil)
EPREUVES = [
    ("titre en --primary sur la page",      "--primary",     "--bg-page",  4.5),
    ("titre en --primary sur une carte",    "--primary",     "--bg-card",  4.5),
    ("texte sur bouton --primary",          "--text-inverse", "--primary",  4.5),
    ("--accent en texte large sur la page", "--accent",      "--bg-page",  3.0),
    ("--accent en bordure sur une carte",   "--accent",      "--bg-card",  3.0),
    ("--primary-light sur la page",         "--primary-light", "--bg-page", 3.0),
]


def main():
    clair, sombre = fonds()
    pals = palettes()
    if not pals:
        sys.exit("Aucune palette trouvée dans %s" % PALETTES)

    echecs = []
    for nom in sorted(pals):
        print("\n%s" % nom)
        print("-" * len(nom))
        for theme, base in (("clair", clair), ("sombre", sombre)):
            vars_ = dict(base)
            vars_.update(pals[nom][theme])
            for libelle, avant, fond, seuil in EPREUVES:
                a, f = vars_.get(avant), vars_.get(fond)
                if not a or not f or not a.startswith("#") or not f.startswith("#"):
                    continue
                r = contraste(a, f)
                ok = r >= seuil
                if not ok:
                    echecs.append((nom, theme, libelle, r, seuil))
                print("  %-7s %-38s %5.2f:1  (min %.1f)  %s"
                      % (theme, libelle, r, seuil, "ok" if ok else "ECHEC"))

    print("\nBilan\n-----")
    if echecs:
        print("  %d couple(s) sous le seuil :" % len(echecs))
        for nom, theme, libelle, r, seuil in echecs:
            print("    %-10s %-7s %-38s %.2f < %.1f" % (nom, theme, libelle, r, seuil))
        print("\n  Corrigez palettes.css : assombrir la couleur en thème clair,")
        print("  l'éclaircir en thème sombre. Puis relancez.")
        return 1
    print("  %d palettes, toutes conformes en clair et en sombre." % len(pals))
    return 0


if __name__ == "__main__":
    sys.exit(main())
