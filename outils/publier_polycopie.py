#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publie le polycopié sur le site (module 02) : le PDF du livret, la vignette de sa couverture, la fiche de sa page.

    python3 outils/publier_polycopie.py                     # le livret français → site/livret/livret.fr.pdf
    python3 outils/publier_polycopie.py --anglais           # le livret anglais → site/livret/livret.en.pdf
    python3 outils/publier_polycopie.py [--anglais] --essai # les contrôles, et ce qui changerait : rien n'est écrit
                                                            # (code 1 s'il reste quelque chose à publier)
    option : --pdf <chemin>   publie ce PDF de travail plutôt que celui de Polycopie/

Le polycopié se fabrique dans Polycopie/ (outils/generer_polycopie.py : Word et PDF de travail), un dossier jamais
publié (hors de site/). Ce script en tire la version publiée, la seule téléchargeable :

  1. il contrôle le PDF de travail : il existe, s'ouvre sans mot de passe, porte le titre du livret et la langue de son
     catalogue (fr-FR, en-US), compte entre PAGES_MIN et PAGES_MAX pages et pèse au plus TAILLE_MAX ;
  2. il le copie dans site/livret/ (livret.fr.pdf, livret.en.pdf) — jamais dans un dossier « polycopie/ » : Windows
     ne distingue pas la casse, ce serait l'espace de travail Polycopie/ ;
  3. il rend la page 1, la couverture, en vignette WebP légère : site/livret/couverture.<langue>.webp ;
  4. il écrit l'inventaire site/livret/livret.json (pages, poids, titre, dimensions de la vignette de chaque langue),
     puis lance outils/generer_fragments.py, qui réécrit la fiche de la page site/polycopie.html (fragments
     livret-couverture, livret-fiche, livret-auteur : outils/polycopie/page.py). Tant que le livret anglais n'est pas
     publié, la page anglaise propose le livret français, marqué hreflang="fr".

Rien ne s'écrit qui ne change : une seconde passe ne touche à rien. Repris, en générique et bilingue, du cours
d'architecture logicielle.
"""
import argparse
import io
import json
import os
import shutil
import subprocess
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "outils"))

for flux in (sys.stdout, sys.stderr):
    try:
        flux.reconfigure(encoding="utf-8")
    except Exception:
        pass

from polycopie import page as PAGE  # noqa: E402
from polycopie.sources import SITE_LOCAL, TRAVAIL, Langue  # noqa: E402

PAGES_MIN, PAGES_MAX = 4, 800
TAILLE_MAX = 40 << 20                        # au plus 40 Mo : le livret se télécharge aussi sur un téléphone
VIGNETTE = 480                               # largeur de la vignette en pixels : 240 px affichés, deux fois plus denses
QUALITE = 80                                 # qualité WebP de la vignette
LANGUE_PDF = {"fr": "fr-FR", "en": "en-US"}


def source_par_defaut(langue):
    """Le PDF de travail du livret complet d'une langue (sortie de generer_polycopie.py, sans --temoin)."""
    import generer_polycopie as GP
    return os.path.join(TRAVAIL, "Polycopie-" + GP.nom_de_fichier(langue.L["titre"])
                        + ("-en" if langue.code == "en" else "") + ".pdf")


def normal(s):
    return (s or "").replace("’", "'").strip()


# ── 1. le contrôle du PDF de travail ───────────────────────────────────────
def controler(pdf, langue):
    """Les caractéristiques du PDF de travail (pages, octets, titre) ; SystemExit s'il ne convient pas."""
    import fitz
    if not os.path.isfile(pdf):
        raise SystemExit(f"✗ PDF de travail introuvable : {pdf} — générez-le d'abord "
                         f"(python3 outils/generer_polycopie.py{' --anglais' if langue.code == 'en' else ''}).")
    octets = os.path.getsize(pdf)
    with fitz.open(pdf) as d:
        if d.needs_pass:
            raise SystemExit(f"✗ {pdf} : protégé par un mot de passe.")
        pages, titre = d.page_count, normal(d.metadata.get("title"))
        lang = d.xref_get_key(d.pdf_catalog(), "Lang")
    erreurs = []
    if not PAGES_MIN <= pages <= PAGES_MAX:
        erreurs.append(f"{pages} pages, de {PAGES_MIN} à {PAGES_MAX} attendues")
    if octets > TAILLE_MAX:
        erreurs.append(f"{octets / 1048576:.1f} Mo, au plus {TAILLE_MAX >> 20} Mo")
    if lang != ("string", LANGUE_PDF[langue.code]):
        erreurs.append(f"langue du PDF {lang[1]!r}, {LANGUE_PDF[langue.code]!r} attendue")
    if titre != normal(langue.L["titre"]):
        erreurs.append(f"titre « {titre} », « {langue.L['titre']} » attendu")
    if erreurs:
        raise SystemExit(f"✗ {pdf} ne se publie pas : " + " ; ".join(erreurs))
    return dict(pages=pages, octets=octets, titre=langue.L["titre"])


def meme_contenu(a, b):
    if not (os.path.isfile(a) and os.path.isfile(b)) or os.path.getsize(a) != os.path.getsize(b):
        return False
    with open(a, "rb") as fa, open(b, "rb") as fb:
        while True:
            x, y = fa.read(1 << 20), fb.read(1 << 20)
            if x != y:
                return False
            if not x:
                return True


def rendre_vignette(pdf):
    """La page 1 du PDF en WebP de VIGNETTE pixels de large : rendue deux fois plus grande, puis réduite (le texte de
    la couverture reste net). Le même PDF donne toujours les mêmes octets. Rend (octets, (largeur, hauteur))."""
    import fitz
    from PIL import Image
    with fitz.open(pdf) as d:
        p = d[0]
        zoom = 2 * VIGNETTE / p.rect.width
        pix = p.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
    image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    image = image.resize((VIGNETTE, round(VIGNETTE * image.height / image.width)), Image.LANCZOS)
    tampon = io.BytesIO()
    image.save(tampon, "WEBP", quality=QUALITE, method=6)
    return tampon.getvalue(), image.size


def chemin(rel):
    return os.path.join(SITE_LOCAL, *rel.split("/"))


def publier(pdf, langue, carac, essai):
    """Copie le PDF, écrit sa vignette et l'inventaire, s'ils changent ; rend la liste de ce qui a changé (ou
    changerait)."""
    f = PAGE.fichiers(langue.code)
    changes = []
    if not meme_contenu(pdf, chemin(f["pdf"])):
        changes.append("site/" + f["pdf"])
        if not essai:
            os.makedirs(os.path.dirname(chemin(f["pdf"])), exist_ok=True)
            shutil.copyfile(pdf, chemin(f["pdf"]))
            if not meme_contenu(pdf, chemin(f["pdf"])):
                raise SystemExit(f"✗ copie incomplète : site/{f['pdf']}")
    image, taille = rendre_vignette(pdf)
    ancienne = open(chemin(f["vignette"]), "rb").read() if os.path.isfile(chemin(f["vignette"])) else None
    if image != ancienne:
        changes.append(f"site/{f['vignette']} ({len(image) // 1024} Ko)")
        if not essai:
            with open(chemin(f["vignette"]), "wb") as sortie:
                sortie.write(image)
    inventaire = PAGE.inventaire()
    neuf = dict(inventaire, **{langue.code: dict(carac, taille=list(taille))})
    if neuf != inventaire:
        changes.append("site/livret/livret.json")
        if not essai:
            with io.open(PAGE.INVENTAIRE, "w", encoding="utf-8", newline="\n") as sortie:
                json.dump(neuf, sortie, ensure_ascii=False, indent=1, sort_keys=True)
                sortie.write("\n")
    return changes


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--anglais", action="store_true", help="le livret anglais")
    ap.add_argument("--essai", action="store_true", help="contrôles seuls : rien n'est écrit")
    ap.add_argument("--pdf", help="le PDF de travail à publier (par défaut, celui de Polycopie/)")
    args = ap.parse_args()
    langue = Langue("en" if args.anglais else "fr")
    pdf = os.path.abspath(args.pdf) if args.pdf else source_par_defaut(langue)
    carac = controler(pdf, langue)
    changes = publier(pdf, langue, carac, args.essai)
    for c in changes:
        print(("  à publier : " if args.essai else "  écrit : ") + c)
    if not args.essai:
        r = subprocess.run([sys.executable, os.path.join(RACINE, "outils", "generer_fragments.py")],
                           capture_output=True, text=True, encoding="utf-8", errors="replace",
                           env=dict(os.environ, PYTHONIOENCODING="utf-8"))
        print("  fragments : " + ((r.stdout.strip().splitlines() or ["…"])[-1]))
    if not changes:
        print("  rien à publier : le livret, sa vignette et son inventaire sont à jour.")
    if not PAGE.publie("en") and not (args.anglais and not args.essai):
        print("  · le livret anglais n'est pas publié : la page anglaise propose le livret français (hreflang=\"fr\").")
    return 1 if args.essai and changes else 0


if __name__ == "__main__":
    sys.exit(main())
