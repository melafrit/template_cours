#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Réécrit, dans les pages, les fragments tirés du référentiel du cours (outils/referentiel.py).

    python3 outils/generer_fragments.py           # réécrit les fragments qui ont changé
    python3 outils/generer_fragments.py --essai   # dit ce qui n'est plus à jour, sans rien écrire ; code 1 alors

Une page marque un fragment ainsi :
    <!-- FRAGMENT:nom -->…<!-- /FRAGMENT:nom -->
Entre les deux marqueurs, on ne touche à rien à la main : tout est réécrit ici. Un même fragment peut figurer dans
plusieurs pages, et plusieurs fois dans une page.

La langue : celle du bloc data-tr qui entoure le marqueur (un fragment dans <span data-tr="en"> s'écrit en anglais) ;
sinon celle de la page (data-langues, une page du site miroir ou d'un cours monolingue) ; sinon, sur une page en
blocs data-tr, les deux, dans leurs blocs — une seule fois si elles se confondent (« 3 », « 30 min »). Les nombres
s'écrivent à la française (12 000 ; 99,9 %) ou à l'anglaise (12,000 ; 99.9%).

Fragments connus :
  nb-chapitres          le nombre de chapitres                ← site/assets/js/course-data.js
  nb-chapitres-lettres  le même, en lettres (« trois »)       ← course-data.js
  duree-N               la durée de lecture du chapitre N     ← referentiel.DUREES (« 30 min », « 1 h 20 »)
  duree-totale          la somme des durées des chapitres     ← referentiel.DUREES
  val-<clé>             un chiffre ou un nom du cas           ← referentiel.VALEURS
  <nom>                 un fragment composé                   ← referentiel.FRAGMENTS

Un fragment inconnu, ou dont la valeur manque, est signalé ; sa place reçoit « … » et --essai échoue. Les contrôles
de referentiel.verifier() passent avant toute écriture. Repris, en générique, du cours d'architecture logicielle.
"""
import argparse
import glob
import html
import importlib.util
import io
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(RACINE, "site")
sys.path.insert(0, os.path.join(RACINE, "outils"))

for flux in (sys.stdout, sys.stderr):
    try:
        flux.reconfigure(encoding="utf-8")
    except Exception:
        pass

MARQUEUR = re.compile(r"(<!-- FRAGMENT:(?P<nom>[a-z0-9-]+) -->)(?P<corps>.*?)(<!-- /FRAGMENT:(?P=nom) -->)", re.S)
JETON = re.compile(r"<!--.*?-->|<script\b.*?</script>|<style\b.*?</style>|<(/?)([a-zA-Z][a-zA-Z0-9]*)\b([^>]*?)(/?)>",
                   re.S | re.I)
VIDES = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
BLOCS = re.compile(r"<(?:p|div|ul|ol|li|table|section|figure|h[1-6]|dl|blockquote|pre)\b", re.I)
INSECABLE = " "
MANQUE = "…"
_UNITES = ["zéro", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf", "dix", "onze", "douze",
           "treize", "quatorze", "quinze", "seize"]
_DIZAINES = {2: "vingt", 3: "trente", 4: "quarante", 5: "cinquante", 6: "soixante"}
_UNITS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
          "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
_TENS = {2: "twenty", 3: "thirty", 4: "forty", 5: "fifty", 6: "sixty", 7: "seventy", 8: "eighty", 9: "ninety"}


class Manque(Exception):
    """Un fragment inconnu, ou dont la valeur manque au référentiel."""


def charger_referentiel():
    spec = importlib.util.spec_from_file_location("referentiel", os.path.join(RACINE, "outils", "referentiel.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def chapitres():
    """Les numéros des chapitres, dans l'ordre de site/assets/js/course-data.js."""
    src = io.open(os.path.join(SITE, "assets", "js", "course-data.js"), encoding="utf-8").read()
    bloc = src.split("chapters", 1)[1].split("]", 1)[0]
    return re.findall(r"num:\s*['\"]([^'\"]+)['\"]", bloc)


def en_lettres(n, langue):
    """0 à 99 en toutes lettres : 45 → « quarante-cinq » / « forty-five »."""
    if langue == "en":
        if n < 20:
            return _UNITS[n]
        d, u = divmod(n, 10)
        return _TENS[d] + ("-" + _UNITS[u] if u else "")
    if n < 17:
        return _UNITES[n]
    if n < 20:
        return "dix-" + _UNITES[n - 10]
    d, u = divmod(n, 10)
    if d in (7, 9):
        base, reste = ("soixante" if d == 7 else "quatre-vingt"), 10 + u
        return base + (" et " if reste == 11 and d == 7 else "-") + en_lettres(reste, langue)
    base = "quatre-vingt" if d == 8 else _DIZAINES[d]
    if u == 0:
        return base + ("s" if d == 8 else "")
    return base + (" et " if u == 1 and d != 8 else "-") + _UNITES[u]


def nombre(x, langue):
    """12000 → « 12 000 » (insécable) / « 12,000 » ; 99.9 → « 99,9 » / « 99.9 »."""
    if isinstance(x, float) and x.is_integer():
        x = int(x)
    txt = "{:,}".format(x) if isinstance(x, int) else ("{:,.10f}".format(x).rstrip("0").rstrip("."))
    if langue == "en":
        return txt
    return txt.replace(",", "\x00").replace(".", ",").replace("\x00", INSECABLE)


def duree(minutes, langue):
    """30 → « 30 min » ; 80 → « 1 h 20 » ; 120 → « 2 h »."""
    if minutes < 60:
        return "%d min" % minutes
    h, m = divmod(minutes, 60)
    return "%d h" % h + (" %02d" % m if m else "")


def valeur(v, langue):
    """Une valeur de referentiel.VALEURS, écrite dans la langue."""
    if isinstance(v, dict):
        return html.escape(str(v.get(langue, v.get("fr", ""))))
    if isinstance(v, tuple):
        n, unite = v
        if langue == "en":
            return nombre(n, langue) + ("" if unite == "%" else " ") + html.escape(unite)
        return nombre(n, langue) + INSECABLE + html.escape(unite)
    if isinstance(v, (int, float)):
        return nombre(v, langue)
    return html.escape(str(v))


def rendre(nom, langue, ref, nums):
    """Le contenu du fragment nom, dans une langue ; Manque s'il est inconnu ou incomplet."""
    durees = getattr(ref, "DUREES", {}) or {}
    if nom == "nb-chapitres":
        return str(len(nums))
    if nom == "nb-chapitres-lettres":
        return en_lettres(len(nums), langue) if len(nums) < 100 else str(len(nums))
    if nom == "duree-totale":
        manquants = [n for n in nums if n not in durees]
        if manquants:
            raise Manque("DUREES sans le(s) chapitre(s) %s" % ", ".join(manquants))
        return duree(sum(durees[n] for n in nums), langue)
    if nom.startswith("duree-"):
        n = nom[len("duree-"):]
        if n not in durees:
            raise Manque("DUREES[%r] manque" % n)
        return duree(durees[n], langue)
    if nom.startswith("val-"):
        cle = nom[len("val-"):]
        valeurs = getattr(ref, "VALEURS", {}) or {}
        if cle not in valeurs:
            raise Manque("VALEURS[%r] manque" % cle)
        return valeur(valeurs[cle], langue)
    fabriques = getattr(ref, "FRAGMENTS", {}) or {}
    if nom in fabriques:
        return fabriques[nom](langue)
    raise Manque("fragment inconnu")


def langues_de_page(t):
    m = re.search(r'<html\b[^>]*\bdata-langues="([^"]*)"', t)
    return m.group(1).split() if m else ["fr", "en"]


def contextes(t):
    """{position d'un marqueur ouvrant : langue du bloc data-tr qui l'entoure, ou None}."""
    pile, out = [], {}
    for m in JETON.finditer(t):
        j = m.group(0)
        if j.startswith("<!--"):
            if j.startswith("<!-- FRAGMENT:"):
                out[m.start()] = next((lg for _tag, lg in reversed(pile) if lg), None)
            continue
        if j.lower().startswith(("<script", "<style")):
            continue
        ferme, tag, attrs, auto = m.group(1), (m.group(2) or "").lower(), m.group(3) or "", m.group(4)
        if ferme:
            while pile:
                haut, _lg = pile.pop()
                if haut == tag:
                    break
        elif tag not in VIDES and not auto:
            lg = re.search(r'\sdata-tr="(fr|en)"', attrs)
            pile.append((tag, lg.group(1) if lg else None))
    return out


def regenerer(t, ref, nums, manques, rel):
    """Le texte de la page, fragments réécrits ; les manques s'ajoutent à la liste."""
    langues, ctx = langues_de_page(t), contextes(t)

    def un(nom, langue):
        try:
            return rendre(nom, langue, ref, nums)
        except Manque as e:
            manques.append("%s : %s — %s" % (rel, nom, e))
            return MANQUE

    def remplacer(m):
        nom, lg = m.group("nom"), ctx.get(m.start())
        if lg or len(langues) == 1:
            corps = un(nom, lg or langues[0])
        else:
            fr, en = un(nom, "fr"), un(nom, "en")
            if fr == en:
                corps = fr
            else:
                balise = "div" if BLOCS.search(fr + en) else "span"
                corps = '<%s data-tr="fr">%s</%s><%s data-tr="en">%s</%s>' % (balise, fr, balise, balise, en, balise)
        return m.group(1) + corps + m.group(4)

    return MARQUEUR.sub(remplacer, t)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--essai", action="store_true", help="dit ce qui n'est plus à jour, sans rien écrire")
    args = ap.parse_args()
    ref = charger_referentiel()
    ecarts = ref.verifier() if hasattr(ref, "verifier") else []
    if ecarts:
        print("Référentiel incohérent (outils/referentiel.py) — rien n'est écrit :")
        for e in ecarts:
            print("  ✗", e)
        return 1
    nums = chapitres()
    a_jour, changees, manques, n = 0, [], [], 0
    for chemin in sorted(glob.glob(os.path.join(SITE, "**", "*.html"), recursive=True)):
        t = io.open(chemin, encoding="utf-8", newline="").read()
        if "<!-- FRAGMENT:" not in t:
            continue
        rel = os.path.relpath(chemin, SITE).replace("\\", "/")
        n += len(MARQUEUR.findall(t))
        neuf = regenerer(t, ref, nums, manques, rel)
        if neuf == t:
            a_jour += 1
            continue
        changees.append(rel)
        if not args.essai:
            with io.open(chemin, "w", encoding="utf-8", newline="") as f:
                f.write(neuf)
    for rel in changees:
        print("  %s : %s" % (rel, "à mettre à jour" if args.essai else "fragments réécrits"))
    for m in manques:
        print("  ✗", m)
    print("%d fragment(s) dans %d page(s) : %d à jour, %d %s%s." % (
        n, a_jour + len(changees), a_jour, len(changees), "à mettre à jour" if args.essai else "réécrite(s)",
        " ; %d manque(s)" % len(manques) if manques else ""))
    return 1 if manques or (args.essai and changees) else 0


if __name__ == "__main__":
    sys.exit(main())
