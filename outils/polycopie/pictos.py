# -*- coding: utf-8 -*-
"""Les dessins du livret : les pictogrammes des encadrés et de la marge, et la composition de la page de garde.
Des SVG au trait, que images.py fait photographier par Chrome sans interface puis colore (bleu nuit, doré, brique) :
un pictogramme se lit aussi en noir et blanc, c'est lui qui distingue un encadré.

Chaque pictogramme tient dans une grille de 24 × 24, trait de 1,7, bouts et angles arrondis. Les pictogrammes sont
repris du cours d'architecture logicielle ; la page de garde est propre au gabarit.
"""

TRAIT = 'fill="none" stroke="#000" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"'
PLEIN = 'fill="#000" stroke="none"'

PICTOS = {
    # À retenir : une clé.
    "cle": f'<g {TRAIT}><circle cx="7.5" cy="12" r="4.2"/><path d="M11.7 12H21M17.6 12v3.6M20.6 12v2.6"/></g>',
    # Exemple et scène UrbanHub : la ville.
    "ville": (f'<g {TRAIT}><path d="M2.5 21h19"/><rect x="4" y="11" width="5" height="10" rx=".6"/>'
              '<rect x="9" y="4.5" width="6" height="16.5" rx=".6"/><rect x="15" y="8.5" width="5" height="12.5" rx=".6"/>'
              '<path d="M11.5 8h1M11.5 11h1M11.5 14h1M11.5 17h1M6 14h1M6 17h1M17 12h1M17 15h1"/></g>'),
    # Attention, piège : le triangle d'alerte.
    "alerte": (f'<g {TRAIT}><path d="M12 3.6 21.6 20H2.4z"/><path d="M12 9.6v4.6"/></g>'
               f'<circle cx="12" cy="17.1" r="1.05" {PLEIN}/>'),
    # Activité : le crayon.
    "crayon": f'<g {TRAIT}><path d="M15.6 4.4l4 4L9 19l-5 1 1-5z"/><path d="M13.4 6.6l4 4M5 15l4 4"/></g>',
    # Pour aller plus loin : les livres.
    "livres": (f'<g {TRAIT}><rect x="3.5" y="4" width="4.4" height="16" rx=".7"/>'
               '<rect x="8.9" y="6" width="4.4" height="14" rx=".7"/><path d="M14.6 6.9l3.9-1.1 3.6 13.4-3.9 1.1z"/>'
               '<path d="M3.5 8h4.4M8.9 9.6h4.4"/></g>'),
    # Écouter : le casque.
    "casque": (f'<g {TRAIT}><path d="M4 15.5V12a8 8 0 0116 0v3.5"/><rect x="2.8" y="14" width="4.4" height="6.6" rx="1.6"/>'
               '<rect x="16.8" y="14" width="4.4" height="6.6" rx="1.6"/></g>'),
    # Podcast : le micro sur son pied (la capsule, l'arceau, la tige et le socle).
    "micro": (f'<g {TRAIT}><rect x="9" y="2.8" width="6" height="11.4" rx="3"/><path d="M5.6 11.2a6.4 6.4 0 0012.8 0"/>'
              '<path d="M12 17.6v3.4M8.6 21h6.8"/></g>'),
    # Point de contrôle, corrigé : la case cochée.
    "coche": f'<g {TRAIT}><rect x="3.5" y="3.5" width="17" height="17" rx="3"/><path d="M7.8 12.4l2.9 2.9 5.6-6.1"/></g>',
    # Repère : la boussole.
    "boussole": (f'<g {TRAIT}><circle cx="12" cy="12" r="9"/><path d="M15.6 8.4l-2.3 4.9-4.9 2.3 2.3-4.9z"/></g>'
                 f'<circle cx="12" cy="12" r=".9" {PLEIN}/>'),
    # Lire ce schéma : l'œil.
    "oeil": (f'<g {TRAIT}><path d="M2.4 12c3-5.6 16.2-5.6 19.2 0-3 5.6-16.2 5.6-19.2 0z"/>'
             '<circle cx="12" cy="12" r="3.1"/></g>'),
    # Scènes : le courriel, la réunion (notes), l'incident (cloche), le relevé.
    "enveloppe": f'<g {TRAIT}><rect x="3" y="5.5" width="18" height="13" rx="2"/><path d="M3.6 7.2 12 13l8.4-5.8"/></g>',
    "notes": (f'<g {TRAIT}><rect x="5" y="4" width="14" height="17" rx="2"/><rect x="9" y="2.4" width="6" height="3.2" rx="1"/>'
              '<path d="M8.6 10h6.8M8.6 13.5h6.8M8.6 17h4.4"/></g>'),
    "cloche": (f'<g {TRAIT}><path d="M6 16.4V11a6 6 0 0112 0v5.4l1.6 1.6H4.4z"/><path d="M10 20.6a2 2 0 004 0"/></g>'),
    "releve": (f'<g {TRAIT}><rect x="4" y="3.5" width="16" height="17" rx="2"/><path d="M8 15.4l3-3.2 2.6 2.1 3.4-4.6"/></g>'),
    # Glossaire : le livre ouvert.
    "glossaire": (f'<g {TRAIT}><path d="M12 6.6C10 5 6.5 4.5 3 5v14c3.5-.5 7 0 9 1.6 2-1.6 5.5-2.1 9-1.6V5c-3.5-.5-7 0-9 1.6z"/>'
                  '<path d="M12 6.6v14"/></g>'),
    # En ligne : l'écran.
    "ecran": f'<g {TRAIT}><rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8.5 20h7M12 16v4"/></g>',
    # Le téléphone (mode d'emploi des QR codes).
    "telephone": f'<g {TRAIT}><rect x="7" y="2.5" width="10" height="19" rx="2.2"/><path d="M11 18.4h2"/></g>',
    # Encouragement : l'étoile à quatre branches.
    "etincelle": f'<path d="M12 3l1.9 7.1L21 12l-7.1 1.9L12 21l-1.9-7.1L3 12l7.1-1.9z" {PLEIN}/>',
    # Objectifs : la cible.
    "cible": (f'<g {TRAIT}><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5.3"/></g>'
              f'<circle cx="12" cy="12" r="1.8" {PLEIN}/>'),
    # Sommaire : la liste.
    "liste": (f'<g {TRAIT}><path d="M9 7h11M9 12h11M9 17h11"/></g><circle cx="5" cy="7" r="1.15" {PLEIN}/>'
              f'<circle cx="5" cy="12" r="1.15" {PLEIN}/><circle cx="5" cy="17" r="1.15" {PLEIN}/>'),
    # Code, prompt.
    "code": f'<g {TRAIT}><path d="M8.5 7.5 4 12l4.5 4.5M15.5 7.5 20 12l-4.5 4.5M13.6 5l-3.2 14"/></g>',
    # Mise en situation : la bulle et sa question.
    "question": (f'<g {TRAIT}><path d="M4 5h16a1.6 1.6 0 011.6 1.6v9.3a1.6 1.6 0 01-1.6 1.6h-9.6L6 21v-3.5H4a1.6 1.6 0 '
                 '01-1.6-1.6V6.6A1.6 1.6 0 014 5z"/><path d="M9.9 9.4a2.1 2.1 0 112.9 1.9c-.6.3-.8.6-.8 1.3"/></g>'
                 f'<circle cx="12" cy="14.9" r=".95" {PLEIN}/>'),
    # Fiche mémo, flashcards, Boîte à outils.
    "fiche": (f'<g {TRAIT}><path d="M6 3h8.5L19 7.5V21H6z"/><path d="M14.5 3v4.5H19M9 12h7M9 15h7M9 18h4"/></g>'),
    "cartes": (f'<g {TRAIT}><rect x="3" y="7" width="13" height="10" rx="1.6" transform="rotate(-8 9.5 12)"/>'
               '<rect x="8" y="8" width="13" height="10" rx="1.6"/></g>'),
    "boite": (f'<g {TRAIT}><rect x="3" y="8.5" width="18" height="11.5" rx="1.6"/><path d="M8.5 8.5V6.2a1.2 1.2 0 011.2-1.2'
              'h4.6a1.2 1.2 0 011.2 1.2v2.3M3 13h18M11 12v2.2h2V12"/></g>'),
    # Le TP et les schémas : l'horaire d'une étape, ce dont on part, la méthode (la clé), la notation (les formes),
    # un dépôt, une correction protégée, une note, les schémas de l'étape, un document à télécharger.
    "horloge": f'<g {TRAIT}><circle cx="12" cy="12" r="9"/><path d="M12 7v5.2l3.4 2"/></g>',
    "entree": (f'<g {TRAIT}><path d="M12 3.2v9.3M8.4 9 12 12.5 15.6 9"/>'
               '<path d="M3.5 13.5h4.6l1.5 2.6h4.8l1.5-2.6h4.6v5.8a1.4 1.4 0 01-1.4 1.4H4.9a1.4 1.4 0 01-1.4-1.4z"/></g>'),
    "outil": (f'<g {TRAIT}><path d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.4-3.4a6 6 0 01-7.9 7.9l-6.4 6.4a2.1 2.1 '
              '0 01-3-3l6.4-6.4a6 6 0 017.9-7.9z"/></g>'),
    "forme": (f'<g {TRAIT}><circle cx="7.4" cy="7.6" r="3.9"/><rect x="13.2" y="3.7" width="7.4" height="7.4" rx="1"/>'
              '<path d="M12 13.4l4.4 7.2H7.6z"/></g>'),
    "envoi": (f'<g {TRAIT}><path d="M12 14.2V3.6M8.4 7.2 12 3.6l3.6 3.6"/>'
              '<path d="M4 13.2v6a1.3 1.3 0 001.3 1.3h13.4a1.3 1.3 0 001.3-1.3v-6"/></g>'),
    "cadenas": (f'<g {TRAIT}><rect x="5" y="10.5" width="14" height="10" rx="2"/><path d="M8.2 10.5V7.6a3.8 3.8 0 017.6 0'
                'v2.9"/></g><circle cx="12" cy="15.4" r="1.25" ' + PLEIN + '/>'),
    "ampoule": (f'<g {TRAIT}><path d="M9.2 17.6h5.6M10.2 20.6h3.6"/><path d="M12 3a6 6 0 00-3.7 10.7c.8.7 1.2 1.5 1.2 2.4'
                'h5c0-.9.4-1.7 1.2-2.4A6 6 0 0012 3z"/></g>'),
    "equerre": (f'<g {TRAIT}><path d="M4 3.5v17h17z"/><path d="M8.2 11.5v5h5z"/><path d="M4 7.5h1.8M4 11.5h1.8M4 '
                '15.5h1.8"/></g>'),
    "telecharger": (f'<g {TRAIT}><path d="M12 3.6v10.6M8.4 10.6 12 14.2l3.6-3.6"/>'
                    '<path d="M4 15.2v4a1.3 1.3 0 001.3 1.3h13.4a1.3 1.3 0 001.3-1.3v-4"/></g>'),
}


def page_pictos(noms, cellule=256, colonnes=8):
    """Une page HTML qui aligne les pictogrammes en grille (noir sur blanc), pour une seule photographie."""
    lignes = (len(noms) + colonnes - 1) // colonnes
    cases = []
    for i, nom in enumerate(noms):
        x, y = (i % colonnes) * cellule, (i // colonnes) * cellule
        cases.append(f'<svg style="position:absolute;left:{x}px;top:{y}px" width="{cellule}" height="{cellule}" '
                     f'viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">{PICTOS[nom]}</svg>')
    html = ("<!DOCTYPE html><html><head><meta charset='utf-8'><style>html,body{margin:0;background:#fff}"
            "body{position:relative}</style></head><body>" + "".join(cases) + "</body></html>")
    return html, colonnes * cellule, lignes * cellule


# ── la page de garde ───────────────────────────────────────────────────────
def composition_garde(largeur=2100, hauteur=1350, primaire="#1B3A5B", accent="#9C7A22", clair="#EAF0F6"):
    """La composition de la page de garde, sans texte (elle sert aux deux langues) : sur un fond très clair quadrillé
    comme une page de cahier, le chemin d'un cours — l'apprenant, les chapitres en cartes reliées par un chemin doré,
    le livret ouvert à l'arrivée — et, dans une marge à droite, les QR codes du livret, esquissés. Unités : dixièmes
    de millimètre (2100 = 21 cm)."""
    P, O = primaire, accent
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {largeur} {hauteur}" width="{largeur}" height="{hauteur}">',
         f'<rect width="{largeur}" height="{hauteur}" fill="{clair}"/>']
    # Le quadrillage : fin tous les 5 mm, appuyé tous les 25 mm.
    for x in range(0, largeur + 1, 50):
        s.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{hauteur}" stroke="#D3DEEA" stroke-width="{2.2 if x % 250 == 0 else 1}"/>')
    for y in range(0, hauteur + 1, 50):
        s.append(f'<line x1="0" y1="{y}" x2="{largeur}" y2="{y}" stroke="#D3DEEA" stroke-width="{2.2 if y % 250 == 0 else 1}"/>')
    # La marge du livret, à droite : un filet, et des QR codes esquissés à hauteur de leurs paragraphes.
    s.append(f'<line x1="1560" y1="120" x2="1560" y2="1180" stroke="{P}" stroke-width="3" stroke-opacity=".35" '
             f'stroke-dasharray="14 10"/>')
    for k, y in enumerate((210, 560, 900)):
        x0, cote = 1660, 190
        s.append(f'<rect x="{x0}" y="{y}" width="{cote}" height="{cote}" rx="14" fill="#FFFFFF" stroke="{P}" '
                 f'stroke-width="5"/>')
        for (cx, cy) in ((x0 + 22, y + 22), (x0 + cote - 72, y + 22), (x0 + 22, y + cote - 72)):
            s.append(f'<rect x="{cx}" y="{cy}" width="50" height="50" rx="6" fill="none" stroke="{P}" stroke-width="7"/>'
                     f'<rect x="{cx + 15}" y="{cy + 15}" width="20" height="20" rx="3" fill="{P}"/>')
        for (mx, my) in ((96, 96), (124, 110), (96, 136), (140, 140), (110, 158), (150, 96), (82, 122)):
            s.append(f'<rect x="{x0 + mx}" y="{y + my}" width="16" height="16" rx="2" fill="{O if k == 1 else P}" '
                     f'fill-opacity="{0.95 if k == 1 else 0.7}"/>')
        s.append(f'<rect x="{x0 + 20}" y="{y + cote + 26}" width="150" height="11" rx="5.5" fill="{P}" fill-opacity=".45"/>')
    # Le chemin doré : de l'apprenant au livret, par les chapitres.
    chemin = ("M 300 640 C 420 640, 430 470, 560 470 L 640 470 C 760 470, 760 760, 880 760 L 960 760 "
              "C 1080 760, 1080 520, 1200 520 L 1290 520")
    s.append(f'<path d="{chemin}" fill="none" stroke="{O}" stroke-width="9" stroke-linecap="round" '
             f'stroke-linejoin="round"/>')
    # L'apprenant.
    s.append(f'<circle cx="210" cy="640" r="92" fill="#FFFFFF" stroke="{P}" stroke-width="5"/>'
             f'<circle cx="210" cy="610" r="28" fill="none" stroke="{P}" stroke-width="6"/>'
             f'<path d="M158 690 a52 48 0 0 1 104 0" fill="none" stroke="{P}" stroke-width="6" stroke-linecap="round"/>')

    def carte(x, y, numero_focal=False):
        trait = O if numero_focal else P
        out = [f'<rect x="{x}" y="{y}" width="200" height="150" rx="16" fill="#FFFFFF" stroke="{trait}" '
               f'stroke-width="{7 if numero_focal else 5}"/>',
               f'<circle cx="{x + 40}" cy="{y + 40}" r="18" fill="{trait}"/>']
        for k, lw in enumerate((120, 150, 90)):
            out.append(f'<rect x="{x + 30}" y="{y + 78 + 22 * k}" width="{lw}" height="10" rx="5" fill="{P}" '
                       f'fill-opacity="{0.75 if k == 0 else 0.35}"/>')
        return "".join(out)

    # Les chapitres, en cartes posées sur le chemin.
    s.append(carte(500, 395))
    s.append(carte(820, 685, numero_focal=True))
    s.append(carte(1140, 445))
    # Le livret ouvert, à l'arrivée du chemin : deux pages, quelques lignes.
    for x in (1300, 1410):
        s.append(f'<path d="M{x} 480 q55 -24 110 0 v170 q-55 -24 -110 0 z" fill="#FFFFFF" stroke="{O}" '
                 f'stroke-width="7" stroke-linejoin="round"/>')
        for k in range(4):
            s.append(f'<rect x="{x + 18}" y="{500 + 32 * k}" width="{72 - 14 * (k % 2)}" height="8" rx="4" '
                     f'fill="{P}" fill-opacity="{0.7 if k == 0 else 0.35}"/>')
    # Un trait doré au pied de la composition.
    s.append(f'<line x1="0" y1="{hauteur - 3}" x2="{largeur}" y2="{hauteur - 3}" stroke="{O}" stroke-width="6"/>')
    s.append("</svg>")
    return "\n".join(s)
