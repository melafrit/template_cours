#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dessine les deux schémas du cours de démonstration, en FR et en EN.

    python3 outils/generer_schemas_demo.py

POURQUOI DESSINER PLUTÔT QUE GÉNÉRER

Ces deux schémas sont des diagrammes **structurels** : des boîtes, des flèches,
un ordre. Un dessin par script est net, reproductible, et suit exactement la
palette du cours — trois choses qu'une image générée ne garantit pas. Il se
corrige aussi en une ligne quand le texte du chapitre évolue.

Pour un schéma d'illustration, en revanche — une scène, une métaphore, un objet
réel — la génération d'image reste la bonne voie. Le critère : si le schéma se
décrit par « des cases et des flèches », dessinez-le.

BILINGUE

Le texte est cuit dans l'image : il faut donc une image par langue. Même
convention que les capsules audio :

    chapitre-<N>-schema-1-<slug>.<langue>.webp

La page choisit d'après la langue lue, comme pour les capsules et les
polycopiés.

FORMAT

1672 × 941 (16:9), WebP qualité 82 — la convention du cours dont ce template
est issu. À cette taille, un schéma reste lisible en plein écran sans peser.
"""

import io
import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("Pillow est requis :  pip install Pillow")

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "site", "assets", "media", "schemas")

L, H = 1672, 941

# Palette « marine » de palettes.css, en clair. Un schéma s'affiche sur les deux
# thèmes : on garde donc un fond clair et un contraste élevé, plutôt qu'un fond
# transparent qui deviendrait illisible en thème sombre.
FOND = (247, 249, 251)
PRIMAIRE = (27, 58, 91)
PRIMAIRE_CLAIR = (45, 93, 138)
ACCENT = (175, 143, 60)
TEXTE = (22, 32, 46)
SECOND = (60, 74, 92)
BORD = (221, 227, 236)
BLANC = (255, 255, 255)
VERT = (47, 143, 91)
ROUGE = (192, 57, 43)


def police(taille, gras=False):
    chemin = "C:/Windows/Fonts/segoeui%s.ttf" % ("b" if gras else "")
    for p in (chemin, "/System/Library/Fonts/Helvetica.ttc",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf" % ("-Bold" if gras else "")):
        if os.path.isfile(p):
            return ImageFont.truetype(p, taille)
    return ImageFont.load_default()


def enrouler(d, texte, fonte, largeur):
    """Découpe un texte pour qu'il tienne dans une largeur donnée."""
    mots, lignes, courante = texte.split(), [], ""
    for m in mots:
        essai = (courante + " " + m).strip()
        if d.textlength(essai, font=fonte) <= largeur:
            courante = essai
        else:
            if courante:
                lignes.append(courante)
            courante = m
    if courante:
        lignes.append(courante)
    return lignes


def bloc_texte(d, texte, fonte, x, y, largeur, couleur, interligne=8, centre=True):
    lignes = enrouler(d, texte, fonte, largeur)
    haut = fonte.size + interligne
    for i, l in enumerate(lignes):
        w = d.textlength(l, font=fonte)
        px = x + (largeur - w) / 2 if centre else x
        d.text((px, y + i * haut), l, font=fonte, fill=couleur)
    return len(lignes) * haut


def boite(d, x, y, w, h, remplissage, bordure, rayon=18, epaisseur=3):
    d.rounded_rectangle([x, y, x + w, y + h], radius=rayon,
                        fill=remplissage, outline=bordure, width=epaisseur)


def fleche(d, x1, y, x2, couleur, epaisseur=5):
    d.line([(x1, y), (x2 - 18, y)], fill=couleur, width=epaisseur)
    d.polygon([(x2, y), (x2 - 20, y - 12), (x2 - 20, y + 12)], fill=couleur)


def cartouche(d, titre, sous_titre):
    """Bandeau de titre commun aux deux schémas."""
    d.rectangle([0, 0, L, 132], fill=PRIMAIRE)
    d.text((70, 34), titre, font=police(42, True), fill=BLANC)
    d.text((70, 88), sous_titre, font=police(24), fill=(200, 214, 232))


# ─────────────────────────────────────────────────── schéma 1 : les décisions
def schema_decisions(langue):
    T = {
        "fr": {
            "titre": "Les trois décisions de cadrage",
            "sous": "Chacune restreint le champ de la suivante — c'est ce qui rend le cadrage utile.",
            "etapes": [
                ("1. LE PUBLIC", "Prérequis réellement acquis, temps disponible, contraintes matérielles.",
                 "→ restreint les objectifs atteignables"),
                ("2. LES OBJECTIFS", "Ce que l'apprenant sera capable de FAIRE. Vérifiable ou inexistant.",
                 "→ impose le type d'activités"),
                ("3. LE FIL ROUGE", "Le cas ou le projet qui traverse tout le cours.",
                 "→ décide l'ordre des chapitres"),
            ],
            "pied": "Sauter une décision ne fait pas gagner de temps : cela le déplace vers la refonte.",
        },
        "en": {
            "titre": "The three scoping decisions",
            "sous": "Each narrows the field of the next — that is what makes scoping useful.",
            "etapes": [
                ("1. THE AUDIENCE", "Prerequisites actually acquired, time available, practical constraints.",
                 "→ narrows the reachable objectives"),
                ("2. THE OBJECTIVES", "What the learner will be able to DO. Verifiable, or non-existent.",
                 "→ dictates the kind of activities"),
                ("3. THE THROUGH-LINE", "The case or project running across the whole course.",
                 "→ decides the order of chapters"),
            ],
            "pied": "Skipping a decision does not save time: it moves the time to the rewrite.",
        },
    }[langue]

    im = Image.new("RGB", (L, H), FOND)
    d = ImageDraw.Draw(im)
    cartouche(d, T["titre"], T["sous"])

    f_titre, f_corps, f_petit = police(30, True), police(23), police(21, True)
    bw, bh, y = 430, 300, 260
    ecart = (L - 3 * bw - 140) / 2
    for i, (titre, corps, effet) in enumerate(T["etapes"]):
        x = 70 + i * (bw + ecart)
        boite(d, x, y, bw, bh, BLANC, PRIMAIRE_CLAIR)
        d.rounded_rectangle([x, y, x + bw, y + 66], radius=18, fill=PRIMAIRE)
        d.rectangle([x, y + 48, x + bw, y + 66], fill=PRIMAIRE)
        w = d.textlength(titre, font=f_titre)
        d.text((x + (bw - w) / 2, y + 18), titre, font=f_titre, fill=BLANC)
        bloc_texte(d, corps, f_corps, x + 30, y + 100, bw - 60, TEXTE)
        d.line([(x + 40, y + bh - 78), (x + bw - 40, y + bh - 78)], fill=BORD, width=2)
        bloc_texte(d, effet, f_petit, x + 30, y + bh - 58, bw - 60, ACCENT)
        if i < 2:
            fleche(d, x + bw + 16, y + bh / 2, x + bw + ecart - 16, PRIMAIRE_CLAIR)

    d.rounded_rectangle([70, 700, L - 70, 800], radius=16,
                        fill=(238, 242, 247), outline=BORD, width=2)
    bloc_texte(d, T["pied"], police(26), 110, 730, L - 220, SECOND)
    return im


# ────────────────────────────────────────────── schéma 2 : chaîne de production
def schema_chaine(langue):
    T = {
        "fr": {
            "titre": "La chaîne de production d'une ressource",
            "sous": "Le contrôle se place avant la publication, jamais après.",
            "etapes": [
                ("SCRIPT ÉCRIT", "Avec sa durée visée. C'est lui qu'on corrige, pas l'enregistrement."),
                ("GÉNÉRATION", "Par l'API, en série. Aucune décision à ce stade."),
                ("CONTRÔLE", "Durée, débit, silences. Contraste et texte alternatif pour les images."),
            ],
            "ok": "PUBLICATION",
            "ok_txt": "La ressource part en ligne.",
            "ko": "QUARANTAINE",
            "ko_txt": "Conservée pour écoute, avec la raison du rejet. Jamais en ligne.",
            "pied": "Une ressource déjà en ligne ne se relit plus : c'est pourquoi le contrôle vient avant.",
        },
        "en": {
            "titre": "The production chain of a resource",
            "sous": "The check sits before publication, never after.",
            "etapes": [
                ("WRITTEN SCRIPT", "With its target duration. This is what you fix, not the recording."),
                ("GENERATION", "Through the API, in bulk. No decision at this stage."),
                ("CHECK", "Duration, pace, silences. Contrast and alt text for images."),
            ],
            "ok": "PUBLICATION",
            "ok_txt": "The resource goes online.",
            "ko": "QUARANTINE",
            "ko_txt": "Kept for listening, with the reason for rejection. Never online.",
            "pied": "A resource already online is no longer re-read: that is why the check comes first.",
        },
    }[langue]

    im = Image.new("RGB", (L, H), FOND)
    d = ImageDraw.Draw(im)
    cartouche(d, T["titre"], T["sous"])

    f_titre, f_corps, f_petit = police(28, True), police(22), police(21)
    bw, bh, y = 400, 230, 230
    ecart = 88
    for i, (titre, corps) in enumerate(T["etapes"]):
        x = 70 + i * (bw + ecart)
        boite(d, x, y, bw, bh, BLANC, PRIMAIRE_CLAIR)
        d.rounded_rectangle([x, y, x + bw, y + 62], radius=18, fill=PRIMAIRE)
        d.rectangle([x, y + 44, x + bw, y + 62], fill=PRIMAIRE)
        w = d.textlength(titre, font=f_titre)
        d.text((x + (bw - w) / 2, y + 16), titre, font=f_titre, fill=BLANC)
        bloc_texte(d, corps, f_corps, x + 28, y + 92, bw - 56, TEXTE)
        if i < 2:
            fleche(d, x + bw + 14, y + bh / 2, x + bw + ecart - 14, PRIMAIRE_CLAIR)

    # le centre du bloc CONTRÔLE : c'est de là que part le bus
    xc = 70 + 2 * (bw + ecart) + bw / 2

    # --- les deux issues du contrôle ---------------------------------------
    # Centrées sur la largeur de l'image, et non sous le bloc CONTRÔLE : placées
    # relativement à lui puis rabattues dans le cadre, elles se chevauchaient.
    bw2, gap = 460, 140
    x_ok = (L - (2 * bw2 + gap)) // 2
    x_ko = x_ok + bw2 + gap
    c_ok, c_ko = x_ok + bw2 // 2, x_ko + bw2 // 2
    y_bus = y + bh + 70
    y_bas = y + bh + 150

    d.line([(xc, y + bh), (xc, y_bus)], fill=PRIMAIRE_CLAIR, width=5)

    def coche(cx, cy, r, couleur):
        """Un ✓ dessiné : la police n'a pas le glyphe, il sortait en carré vide."""
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=couleur)
        d.line([(cx - r * 0.42, cy + r * 0.04), (cx - r * 0.10, cy + r * 0.38),
                (cx + r * 0.46, cy - r * 0.36)], fill=BLANC, width=6, joint="curve")

    def croix(cx, cy, r, couleur):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=couleur)
        e = r * 0.40
        d.line([(cx - e, cy - e), (cx + e, cy + e)], fill=BLANC, width=6)
        d.line([(cx + e, cy - e), (cx - e, cy + e)], fill=BLANC, width=6)

    for x0, centre, couleur, dessin, titre, txt in (
            (x_ok, c_ok, VERT, coche, T["ok"], T["ok_txt"]),
            (x_ko, c_ko, ROUGE, croix, T["ko"], T["ko_txt"])):
        # le trait : depuis le bus, jusqu'au haut de l'encadré
        d.line([(xc, y_bus), (centre, y_bus)], fill=couleur, width=4)
        d.line([(centre, y_bus), (centre, y_bas - 22)], fill=couleur, width=4)
        d.polygon([(centre, y_bas - 4), (centre - 12, y_bas - 26),
                   (centre + 12, y_bas - 26)], fill=couleur)

        boite(d, x0, y_bas, bw2, 180, BLANC, couleur)
        dessin(x0 + 56, y_bas + 52, 26, couleur)
        d.text((x0 + 100, y_bas + 34), titre, font=f_titre, fill=couleur)
        bloc_texte(d, txt, f_petit, x0 + 30, y_bas + 96, bw2 - 60, TEXTE, centre=False)

    bloc_texte(d, T["pied"], police(24), 110, 860, L - 220, SECOND)
    return im


def main():
    if not os.path.isdir(SORTIE):
        os.makedirs(SORTIE)
    plan = [
        ("chapitre-1-schema-1-trois-decisions", schema_decisions),
        ("chapitre-3-schema-1-chaine-production", schema_chaine),
    ]
    print("\nSchémas\n-------")
    for slug, fabrique in plan:
        for langue in ("fr", "en"):
            im = fabrique(langue)
            chemin = os.path.join(SORTIE, "%s.%s.webp" % (slug, langue))
            im.save(chemin, "WEBP", quality=82, method=6)
            print("  %-46s %dx%d  %d Ko"
                  % (os.path.basename(chemin), im.width, im.height,
                     os.path.getsize(chemin) // 1024))
    print("\n  %d fichiers dans site/assets/media/schemas/" % (len(plan) * 2))
    print("  Les coordonnées des points chauds se règlent dans les pages, en %.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
