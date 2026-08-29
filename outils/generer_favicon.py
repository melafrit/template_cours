#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fabrique le favicon du cours, dans sa palette.

    python3 outils/generer_favicon.py            # depuis la palette des pages
    python3 outils/generer_favicon.py --palette emeraude --initiales RD

POURQUOI

Sans favicon, le navigateur demande `/favicon.ico`, ne le trouve pas, et
inscrit un 404 dans la console à chaque page. Ce n'est pas grave, mais c'est un
bruit permanent qui masque les vrais défauts : on finit par ne plus regarder la
console du tout.

Et un onglet sans icône se retrouve mal quand l'étudiant en a quinze d'ouverts.

CE QU'IL PRODUIT

    site/favicon.svg          net à toute taille, c'est celui que les
                              navigateurs modernes utilisent
    site/favicon-32.png       repli pour les navigateurs anciens
    site/apple-touch-icon.png écran d'accueil iOS, 180 × 180

Puis il pose les balises `<link>` dans toutes les pages, si elles manquent.

LES INITIALES sont tirées du titre du cours : deux lettres, la première de
chacun des deux premiers mots significatifs. « Cybersécurité des systèmes
d'information » donne « CS ». Passez --initiales pour imposer autre chose.
"""

import argparse
import io
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(RACINE, "site")

# Les couples (fond, lettre) de chaque palette, repris de palettes.css.
# Le fond est le --primary du thème clair : c'est lui qui identifie le cours.
PALETTES = {
    "marine":   ("#1b3a5b", "#af8f3c"),
    "emeraude": ("#14503f", "#b5713a"),
    "prune":    ("#4a2352", "#b06a7a"),
    "ardoise":  ("#33475c", "#c05f2c"),
    "bordeaux": ("#5c1f2b", "#a8823f"),
}

MOTS_VIDES = {"le", "la", "les", "de", "des", "du", "un", "une", "et", "aux",
              "the", "of", "a", "an", "and", "to", "for", "in"}


def palette_des_pages():
    """La palette réellement posée sur les pages, ou « marine » par défaut."""
    for f in ("index.html", "cours.html"):
        p = os.path.join(SITE, f)
        if os.path.isfile(p):
            m = re.search(r'data-accent="([a-z]+)"', io.open(p, encoding="utf-8").read())
            if m and m.group(1) in PALETTES:
                return m.group(1)
    return "marine"


def initiales_du_cours():
    p = os.path.join(SITE, "assets", "js", "course-data.js")
    if not os.path.isfile(p):
        return "C"
    m = re.search(r'title:\s*\{\s*fr:\s*"([^"]+)"', io.open(p, encoding="utf-8").read())
    if not m:
        return "C"
    mots = [w for w in re.findall(r"[A-Za-zÀ-ÿ]+", m.group(1))
            if w.lower() not in MOTS_VIDES]
    return "".join(w[0].upper() for w in mots[:2]) or "C"


def svg(fond, lettre_couleur, initiales):
    """Un carré arrondi, les initiales dedans, la dernière en couleur d'accent.

    Écrit à la main plutôt que dessiné : à 16 px, un SVG reste net là où un PNG
    redimensionné bave, et le fichier fait moins d'un kilooctet.
    """
    if len(initiales) == 1:
        texte = ('<text x="32" y="44" font-family="Segoe UI,Helvetica,Arial,sans-serif" '
                 'font-size="34" font-weight="700" fill="#ffffff" text-anchor="middle">'
                 '%s</text>' % initiales[0])
    else:
        texte = ('<text x="32" y="43" font-family="Segoe UI,Helvetica,Arial,sans-serif" '
                 'font-size="30" font-weight="700" text-anchor="middle">'
                 '<tspan fill="#ffffff">%s</tspan>'
                 '<tspan fill="%s">%s</tspan></text>'
                 % (initiales[0], lettre_couleur, initiales[1]))
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
            '<rect width="64" height="64" rx="14" fill="%s"/>%s</svg>' % (fond, texte))


def png(fond, lettre_couleur, initiales, taille):
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return None
    im = Image.new("RGBA", (taille, taille), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    r = int(taille * 0.22)
    d.rounded_rectangle([0, 0, taille - 1, taille - 1], radius=r, fill=fond)

    def fonte(px):
        for p in ("C:/Windows/Fonts/segoeuib.ttf",
                  "/System/Library/Fonts/Helvetica.ttc",
                  "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
            if os.path.isfile(p):
                return ImageFont.truetype(p, px)
        return ImageFont.load_default()

    f = fonte(int(taille * 0.46))
    largeurs = [d.textlength(c, font=f) for c in initiales]
    x = (taille - sum(largeurs)) / 2
    y = taille * 0.24
    for i, c in enumerate(initiales):
        d.text((x, y), c, font=f, fill="#ffffff" if i == 0 else lettre_couleur)
        x += largeurs[i]
    return im


BALISES = ('<link rel="icon" href="%sfavicon.svg" type="image/svg+xml">\n'
           '<link rel="icon" href="%sfavicon-32.png" sizes="32x32">\n'
           '<link rel="apple-touch-icon" href="%sapple-touch-icon.png">')


def poser_balises():
    """Ajoute les <link> dans chaque page qui ne les a pas."""
    n = 0
    for dossier, _, fichiers in os.walk(SITE):
        for f in fichiers:
            if not f.endswith(".html"):
                continue
            p = os.path.join(dossier, f)
            t = io.open(p, encoding="utf-8").read()
            if 'rel="icon"' in t:
                continue
            profondeur = os.path.relpath(p, SITE).count(os.sep)
            prefixe = "../" * profondeur
            ancre = '<meta name="viewport"'
            if ancre not in t:
                continue
            i = t.index("\n", t.index(ancre)) + 1
            t = t[:i] + (BALISES % (prefixe, prefixe, prefixe)) + "\n" + t[i:]
            io.open(p, "w", encoding="utf-8", newline="\n").write(t)
            n += 1
    return n


def main():
    ap = argparse.ArgumentParser(description="Fabrique le favicon du cours.")
    ap.add_argument("--palette", choices=sorted(PALETTES))
    ap.add_argument("--initiales")
    args = ap.parse_args()

    pal = args.palette or palette_des_pages()
    fond, accent = PALETTES[pal]
    ini = (args.initiales or initiales_du_cours())[:2].upper()

    print("\nFavicon\n-------")
    print("  palette   : %s  (%s / %s)" % (pal, fond, accent))
    print("  initiales : %s" % ini)

    io.open(os.path.join(SITE, "favicon.svg"), "w", encoding="utf-8",
            newline="\n").write(svg(fond, accent, ini) + "\n")
    print("  site/favicon.svg")

    manque_pillow = False
    # favicon.ico : le navigateur le demande a la racine d'office, meme avec les
    # balises <link>. Sans lui, un 404 s'inscrit dans la console a chaque page.
    ico = png(fond, accent, ini, 64)
    if ico is not None:
        ico.save(os.path.join(SITE, "favicon.ico"), "ICO",
                 sizes=[(16, 16), (32, 32), (48, 48)])
        print("  site/favicon.ico")
    for nom, taille in (("favicon-32.png", 32), ("apple-touch-icon.png", 180)):
        im = png(fond, accent, ini, taille)
        if im is None:
            manque_pillow = True
            continue
        im.save(os.path.join(SITE, nom), "PNG")
        print("  site/%s" % nom)
    if manque_pillow:
        print("  /!\\ Pillow absent : seuls les PNG manquent, le SVG suffit aux "
              "navigateurs modernes.")

    n = poser_balises()
    print("\n  %d page(s) ont reçu les balises <link>." % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
