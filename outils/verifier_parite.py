#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""La parité des pages jumelles du site miroir : chaque page anglaise de site/en/ a la même structure que sa page
française (docs/I18N.md, partie A).

    python3 outils/verifier_parite.py              # toutes les pages de site/en/
    python3 outils/verifier_parite.py PAGE.html    # une seule page (chemin depuis la racine du site, sans en/)

Le bouton FR / EN (site/assets/js/langue.js) retrouve le paragraphe lu par son rang dans la suite des blocs de la
page ; il faut donc, de part et d'autre, la même suite : mêmes titres, paragraphes, éléments de liste, figures,
tableaux, images, dans le même ordre, avec les mêmes identifiants. Le contrôle compare aussi les composants
(RDCX.<type>('<conteneur>', …) : même suite, chaque conteneur présent dans la page), les marqueurs de fragments
(<!-- FRAGMENT:… -->), la langue déclarée (<html lang="en">), et refuse une jumelle préparée par creer_jumelle.py
qui porte encore sa marque « À TRADUIRE ». Sont signalés à part, sans compter comme écart : des mots accentués dans
le texte d'une page anglaise (un nom propre en porte parfois), un titre d'onglet identique à celui de la page
française. Code 1 s'il y a un écart. Repris du cours d'architecture logicielle.
"""
import glob
import io
import os
import re
import sys
from html.parser import HTMLParser

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

BLOCS = {"h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "dt", "dd", "figure", "table", "pre", "blockquote",
         "summary", "img"}
COMPOSANT = re.compile(r"RDCX\.([A-Za-z]+)\(\s*['\"]([^'\"]+)['\"]")
ACCENTS = re.compile(r"\b\w*[éèêëàâîïôûùçœÉÈÊÀÂÎÔÛÇŒ]\w*\b")
NOMS = {"fr": "français", "en": "anglais", "ar": "arabe"}
ARABE = re.compile(r"[\u0600-\u06FF]")
LATIN = re.compile(r"[A-Za-zÀ-ÿ]{3,}")


class Structure(HTMLParser):
    """La suite des blocs du contenu principal : (balise, identifiant), et un extrait du texte qui suit."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocs = []
        self.texte = []

    def handle_starttag(self, tag, attrs):
        if tag in BLOCS:
            self.blocs.append([tag, dict(attrs).get("id") or "", ""])

    def handle_data(self, data):
        self.texte.append(data)
        if self.blocs and len(self.blocs[-1][2]) < 60:
            self.blocs[-1][2] += " ".join(data.split())[:60]


def contenu_principal(texte):
    """La zone que lit le bouton FR / EN : .main-content, ou <main> sur les pages qui n'en ont pas."""
    debut = texte.find('<main class="main-content"')
    if debut < 0:
        debut = texte.find("<main")
    fin = texte.rfind("</main>")
    if debut < 0 or fin < 0:
        return texte
    return texte[debut:fin]


def sans_scripts(html):
    """Le texte lisible seulement : ni scripts, ni styles, ni en-tête (une page sans <main> se lit entière)."""
    return re.sub(r"<script\b.*?</script>|<style\b.*?</style>|<head\b.*?</head>", "", html, flags=re.S | re.I)


def titre(texte):
    m = re.search(r"<title>(.*?)</title>", texte, flags=re.S)
    return " ".join(m.group(1).split()) if m else ""


def composants(texte):
    """La suite des composants appelés par la page (type, conteneur), et ceux dont le conteneur manque."""
    appels = COMPOSANT.findall(texte)
    manquants = [c for _t, c in appels if 'id="%s"' % c not in texte]
    return appels, manquants


def ecarts(fr_t, en_t, lg="en", racine="fr"):
    """(nombre de blocs de la page de la racine, écarts, avertissements sur sa jumelle dans la langue lg). Les noms
    des variables gardent l'histoire de l'outil : fr pour la racine, en pour la jumelle."""
    out = []
    a_n, b_n = NOMS.get(racine, racine), NOMS.get(lg, lg)
    s_fr, s_en = Structure(), Structure()
    s_fr.feed(sans_scripts(contenu_principal(fr_t)))
    s_en.feed(sans_scripts(contenu_principal(en_t)))
    for i in range(max(len(s_fr.blocs), len(s_en.blocs))):
        a = s_fr.blocs[i] if i < len(s_fr.blocs) else None
        b = s_en.blocs[i] if i < len(s_en.blocs) else None
        if not a or not b or a[0] != b[0] or a[1] != b[1]:
            out.append("bloc %d : %s %s, %s %s" % (
                i + 1, a_n, "<%s%s> « %s »" % (a[0], " #" + a[1] if a[1] else "", a[2]) if a else "rien", b_n,
                "<%s%s> « %s »" % (b[0], " #" + b[1] if b[1] else "", b[2]) if b else "rien"))
            break                                    # la suite est décalée : le premier écart suffit
    if len(s_fr.blocs) != len(s_en.blocs):
        out.append("%d blocs en %s, %d en %s" % (len(s_fr.blocs), a_n, len(s_en.blocs), b_n))
    (c_fr, _m), (c_en, manquants) = composants(fr_t), composants(en_t)
    if c_fr != c_en:
        out.append("composants : %s" % next(("%s / %s" % (x, y) for x, y in zip(c_fr, c_en) if x != y),
                                            "%d en %s, %d en %s" % (len(c_fr), a_n, len(c_en), b_n)))
    if manquants:
        out.append("conteneur(s) absent(s) de la page en %s : %s" % (b_n, ", ".join(manquants)))
    f_fr = re.findall(r"<!-- FRAGMENT:([a-z0-9-]+) -->", fr_t)
    f_en = re.findall(r"<!-- FRAGMENT:([a-z0-9-]+) -->", en_t)
    if f_fr != f_en:
        out.append("fragments : %d en %s, %d en %s" % (len(f_fr), a_n, len(f_en), b_n))
    if not re.search(r'<html[^>]*\blang="%s"' % lg, en_t):
        out.append('la page en %s ne déclare pas <html lang="%s">' % (b_n, lg))
    if lg in miroir.DROITE_A_GAUCHE and not re.search(r'<html[^>]*\bdir="rtl"', en_t):
        out.append('la page en %s ne déclare pas <html dir="rtl">' % b_n)
    if miroir.A_TRADUIRE in en_t:
        out.append("jumelle préparée par creer_jumelle.py, encore à traduire (marque « À TRADUIRE »)")
    avis = []
    mots = sorted(set(ACCENTS.findall(" ".join(s_en.texte)))) if lg == "en" else []
    if lg == "ar":
        # Un bloc sans aucune lettre arabe, mais avec des mots latins : un texte resté en français ? Un terme français
        # rappelé entre parenthèses ne compte pas, son bloc ayant aussi de l'arabe.
        sans = [b for b in s_en.blocs if b[2] and not ARABE.search(b[2]) and LATIN.search(b[2])]
        if sans:
            avis.append("%d bloc(s) sans lettre arabe (texte resté en français ?), dont « %s »" % (len(sans), sans[0][2]))
    if mots:
        avis.append("mots accentués dans la page anglaise (texte français restant ?) : %s"
                    % ", ".join(mots[:12]) + (" …" if len(mots) > 12 else ""))
    if titre(en_t) and titre(en_t) == titre(fr_t):
        avis.append("titre d'onglet identique à celui de la page en %s (à traduire ?) : « %s »" % (a_n, titre(en_t)))
    return len(s_fr.blocs), out, avis


def main():
    """Chaque jumelle de chaque dossier de langue (en/, ar/…), ou les seules pages nommées, dans chaque langue où
    elles ont une jumelle."""
    racine = generer_langues.langue_racine(SITE)
    demandees = sys.argv[1:]
    total, n_pages = 0, 0
    for lg in generer_langues.LANGUES:
        base = os.path.join(SITE, lg)
        if lg == racine or not os.path.isdir(base):
            continue
        cibles = demandees or sorted(os.path.relpath(p, base).replace("\\", "/")
                                     for p in glob.glob(os.path.join(base, "**", "*.html"), recursive=True))
        for rel in cibles:
            fr_p, en_p = os.path.join(SITE, *rel.split("/")), os.path.join(base, *rel.split("/"))
            if demandees and not os.path.isfile(en_p):
                continue                         # une page nommée n'a pas forcément sa jumelle dans chaque langue
            n_pages += 1
            if not os.path.isfile(fr_p):
                print("✗ %s/%s — page de la racine absente" % (lg, rel))
                total += 1
                continue
            n, out, avis = ecarts(io.open(fr_p, encoding="utf-8").read(), io.open(en_p, encoding="utf-8").read(),
                                  lg, racine)
            print(("✓ " if not out else "✗ ") + "%s/%s — %d blocs" % (lg, rel, n))
            for e in out:
                print("     ", e)
            for a in avis:
                print("      ·", a)
            total += len(out)
    print("%d page(s), %d écart(s)" % (n_pages, total))
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
