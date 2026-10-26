# -*- coding: utf-8 -*-
"""Les images du livret, toutes dans Polycopie/_cache/ (regénérables, non versionnées).

LES SCHÉMAS SVG du site, jamais redessinés : Chrome sans interface les photographie (navigateur.photographier), à
l'échelle 3 ; un schéma s'imprime sur 17,3 cm, plus de 450 points par pouce, un trait net.

LES ILLUSTRATIONS (WebP, PNG, JPEG du site) deviennent des JPEG à 300 points par pouce ; UN SCHÉMA À ZONES (le
composant hotspots du moteur) reçoit, à la place de ses zones cliquables, des pastilles numérotées que l'encadré
« Lire ce schéma » explique une à une. LES PICTOGRAMMES (pictos.py) sont photographiés noir sur blanc, en une seule
page, puis colorés avec une transparence tirée du gris : la même forme sert en bleu nuit, en doré ou en brique. LA PAGE
DE GARDE est photographiée de même.

Un fichier déjà fait est gardé s'il est plus récent que sa source ; le nom d'une image tirée d'un texte (pictogramme,
garde, pastilles) porte l'empreinte de ce texte : une retouche du site donne une nouvelle image.
"""
import hashlib
import os
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from . import gabarit as G
from . import navigateur
from . import pictos
from .sources import CACHE


def _empreinte(*morceaux):
    h = hashlib.sha1()
    for m in morceaux:
        h.update(str(m).encode("utf-8"))
    return h.hexdigest()[:12]


def _a_refaire(sortie, *sources):
    if not os.path.exists(sortie):
        return True
    t = os.path.getmtime(sortie)
    return any(os.path.exists(s) and os.path.getmtime(s) > t for s in sources)


def _rgb(hexa):
    return tuple(int(hexa[k:k + 2], 16) for k in (0, 2, 4))


def place_libre(gris, x, y, rayon, deja=(), portee=7):
    """La place d'une pastille : au point (x, y) s'il est sur un fond uni, sinon la place unie la plus proche, à moins
    de portee rayons, sans toucher une pastille déjà posée — le texte que la zone désigne reste lisible. Sans place
    unie à portée, le point lui-même. Un demi-rayon de blanc entoure la pastille : collée au texte, elle se lirait
    comme une lettre de plus."""
    import math
    from PIL import ImageStat
    l, h = gris.size
    marge = rayon + rayon // 2 + 2

    def libre(cx, cy):
        if cx - marge < 0 or cy - marge < 0 or cx + marge > l or cy + marge > h:
            return False
        if any(math.hypot(cx - a, cy - b) < 2 * rayon + 4 for a, b in deja):
            return False
        return ImageStat.Stat(gris.crop((int(cx - marge), int(cy - marge), int(cx + marge), int(cy + marge)))).stddev[0] < 5

    pas = max(2, rayon // 2)
    for d in range(0, portee * rayon + 1, pas):
        n = max(1, int(2 * math.pi * d / pas))
        for k in range(n):
            a = math.pi / 2 + 2 * math.pi * k / n            # en commençant sous le point
            cx, cy = x + d * math.cos(a), y + d * math.sin(a)
            if libre(cx, cy):
                return cx, cy
    return x, y


class Atelier:
    """Rassemble les photographies à faire, puis les fait d'un coup (Chrome sans interface)."""

    def __init__(self, langue, forcer=False):
        self.langue = langue
        self.forcer = forcer
        self.dossier = os.path.join(CACHE, langue.code)
        os.makedirs(self.dossier, exist_ok=True)
        self.travaux = []          # (url, sortie, largeur, hauteur, échelle)

    def _ajouter(self, url, sortie, largeur, hauteur, echelle, sources=()):
        if self.forcer or _a_refaire(sortie, *sources):
            self.travaux.append((url, sortie, int(largeur), int(hauteur), echelle))
        return sortie

    def photographier(self):
        """Fait toutes les photographies en attente ; rend leur nombre."""
        n = navigateur.photographier(self.travaux)
        self.travaux = []
        return n

    # ── les schémas SVG du site ────────────────────────────────────────────
    def schema_fichier(self, chemin_svg, echelle=3):
        """Un schéma (fichier SVG du site) → PNG ; rend (chemin, largeur, hauteur) en px CSS."""
        with open(chemin_svg, encoding="utf-8") as f:
            entete = re.search(r"<svg\b[^>]*>", f.read()).group(0)
        vue = re.search(r'viewBox="\s*[-\d.]+\s+[-\d.]+\s+([\d.]+)\s+([\d.]+)"', entete)
        if vue:
            largeur, hauteur = round(float(vue.group(1))), round(float(vue.group(2)))
        else:
            largeur = round(float(re.search(r'width="([\d.]+)', entete).group(1)))
            hauteur = round(float(re.search(r'height="([\d.]+)', entete).group(1)))
        nom = os.path.splitext(os.path.basename(chemin_svg))[0]
        sortie = os.path.join(self.dossier, "schemas", f"{nom}@{echelle}.png")
        self._ajouter(Path(chemin_svg).as_uri(), sortie, largeur, hauteur, echelle, [chemin_svg])
        return sortie, largeur, hauteur

    # ── les illustrations et les schémas à zones ───────────────────────────
    def illustration(self, chemin):
        """Une illustration du site (WebP, PNG, JPEG) → JPEG à 300 points par pouce ; rend (chemin, largeur, hauteur)
        en pixels."""
        nom = os.path.splitext(os.path.basename(chemin))[0]
        sortie = os.path.join(self.dossier, "illustrations", nom + ".jpg")
        os.makedirs(os.path.dirname(sortie), exist_ok=True)
        if self.forcer or _a_refaire(sortie, chemin):
            with Image.open(chemin) as im:
                fond = Image.new("RGB", im.size, (255, 255, 255))
                rgba = im.convert("RGBA")
                fond.paste(rgba, (0, 0), rgba)
                fond.save(sortie, "JPEG", quality=92, optimize=True, dpi=(300, 300))
        with Image.open(sortie) as im:
            return sortie, im.size[0], im.size[1]

    def schema_zones(self, chemin, points):
        """Un schéma à zones cliquables (RDCX.hotspots) → JPEG où chaque zone devient une pastille numérotée, à sa
        place (x, y en pourcentage de l'image), dans l'ordre des points ; rend (chemin, largeur, hauteur)."""
        source, largeur, hauteur = self.illustration(chemin)
        if not points:
            return source, largeur, hauteur
        cle = _empreinte(os.path.basename(chemin), os.path.getmtime(chemin), points, "pastilles-v3")
        sortie = os.path.join(self.dossier, "illustrations", f"{os.path.splitext(os.path.basename(chemin))[0]}"
                                                               f"-zones-{cle}.jpg")
        if self.forcer or not os.path.exists(sortie):
            with Image.open(source) as im:
                im = im.convert("RGB")
            dessin = ImageDraw.Draw(im)
            # Une pastille petite (2,8 mm imprimée sur 17,3 cm), cernée de blanc : elle cache le moins possible du
            # texte que la zone désigne. Un schéma dont les zones portent leur numéro n'en reçoit aucune (rendu.py).
            rayon = max(11, round(largeur * 0.0085))
            try:
                police = ImageFont.truetype("segoeuib.ttf", round(rayon * 1.25))
            except OSError:
                police = ImageFont.load_default()
            gris, poses = im.convert("L"), []
            for k, p in enumerate(points, 1):
                x, y = float(p.get("x", 0)) / 100 * largeur, float(p.get("y", 0)) / 100 * hauteur
                x, y = place_libre(gris, x, y, rayon, poses)
                poses.append((x, y))
                boite = (x - rayon, y - rayon, x + rayon, y + rayon)
                dessin.ellipse(boite, fill=_rgb(G.PRIMAIRE), outline=(255, 255, 255), width=max(2, rayon // 4))
                dessin.text((x, y), str(k), fill=(255, 255, 255), font=police, anchor="mm")
            im.save(sortie, "JPEG", quality=92, optimize=True, dpi=(300, 300))
        return sortie, largeur, hauteur

    # ── les pictogrammes ───────────────────────────────────────────────────
    def pictos(self, demandes, cellule=256):
        """{(nom, couleur)} → {(nom, couleur): chemin du PNG transparent} ; une seule photographie pour tous."""
        noms = sorted({n for n, _ in demandes})
        html, largeur, hauteur = pictos.page_pictos(noms, cellule)
        cle = _empreinte(html)
        dossier = os.path.join(CACHE, "pictos")
        os.makedirs(dossier, exist_ok=True)
        planche = os.path.join(dossier, f"planche-{cle}.png")
        sorties = {d: os.path.join(dossier, f"{d[0]}-{d[1]}-{cle}.png") for d in demandes}
        if self.forcer or any(not os.path.exists(s) for s in sorties.values()):
            if not os.path.exists(planche) or self.forcer:
                page = os.path.join(dossier, f"planche-{cle}.html")
                with open(page, "w", encoding="utf-8", newline="\n") as f:
                    f.write(html)
                navigateur.photographier([(Path(page).as_uri(), planche, largeur, hauteur, 1)])
            with Image.open(planche) as im:
                gris = im.convert("L")
            colonnes = largeur // cellule
            for (nom, couleur), sortie in sorties.items():
                i = noms.index(nom)
                x, y = (i % colonnes) * cellule, (i // colonnes) * cellule
                case = gris.crop((x, y, x + cellule, y + cellule))
                alpha = case.point(lambda v: 255 - v)
                img = Image.new("RGBA", case.size, _rgb(couleur) + (0,))
                img.putalpha(alpha)
                img.save(sortie)
        return sorties

    # ── la page de garde ───────────────────────────────────────────────────
    def garde(self, largeur_mm=210, hauteur_mm=135):
        """La composition de la page de garde (PNG), photographiée à 400 points par pouce environ."""
        svg = pictos.composition_garde(largeur_mm * 10, hauteur_mm * 10, "#" + G.PRIMAIRE, "#" + G.ACCENT,
                                       "#" + G.FOND_PRIMAIRE)
        cle = _empreinte(svg)
        dossier = os.path.join(CACHE, "garde")
        os.makedirs(dossier, exist_ok=True)
        sortie = os.path.join(dossier, f"garde-{cle}.png")
        if self.forcer or not os.path.exists(sortie):
            page = os.path.join(dossier, f"garde-{cle}.html")
            l, h = largeur_mm * 5, hauteur_mm * 5            # px CSS ; échelle 3,2 → 3 360 px sur 21 cm
            html = ("<!DOCTYPE html><html><head><meta charset='utf-8'><style>html,body{margin:0;background:#fff}"
                    f"svg{{display:block;width:{l}px;height:{h}px}}</style></head><body>{svg}</body></html>")
            with open(page, "w", encoding="utf-8", newline="\n") as f:
                f.write(html)
            navigateur.photographier([(Path(page).as_uri(), sortie, l, h, 3.2)])
        return sortie
