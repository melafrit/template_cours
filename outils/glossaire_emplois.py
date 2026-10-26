#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Où le cours emploie-t-il chaque terme du glossaire ? Écrit site/assets/js/glossaire-emplois.js, que lit la page
du glossaire : sous chaque terme, « Où en parle-t-on ? » mène aux sections qui l'emploient.

    python3 outils/glossaire_emplois.py           # écrit le fichier, s'il change
    python3 outils/glossaire_emplois.py --essai   # dit s'il est à jour, sans rien écrire ; code 1 sinon

LES TERMES : site/assets/js/glossaire-data.js (window.GLOSSARY). Un terme peut porter deux champs facultatifs :
  alias  : {fr: [...], en: [...]} — d'autres formes du même terme (un sigle, un synonyme) ;
  exclus : {fr: [...], en: [...]} — des expressions où le mot ne désigne pas la notion (« mise en service »).
UN ENDROIT : une section d'une page, désignée par son ancre — un h2 ou un h3 qui porte un id ; le texte qui précède
la première ancre forme le haut de la page. Seul compte le contenu de <main>, hors code, schémas, boutons,
navigation, éléments masqués, et hors des blocs de l'autre langue.
UN EMPLOI : une forme du terme entre deux limites de mot — son intitulé sans parenthèse, ses alias, leurs pluriels
(français ou anglais) —, hors des expressions écartées.
LES LANGUES : le français sur les pages françaises et les blocs data-tr="fr", l'anglais sur les jumelles de en/ et
les blocs data-tr="en". Les chemins partent de la racine de la langue : la page du glossaire de chaque langue y
mène directement.
NE COMPTENT PAS : les pages d'EXCLUES — le glossaire lui-même, les pages qui donnent des réponses — et les zones
protégées de deploiement/destination.json. Repris, en générique, du cours d'architecture logicielle.
"""
import argparse
import glob
import io
import json
import os
import re
import sys
import unicodedata
from html.parser import HTMLParser

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(RACINE, "site")
SORTIE = os.path.join(SITE, "assets", "js", "glossaire-emplois.js")

for flux in (sys.stdout, sys.stderr):
    try:
        flux.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Chemins depuis la racine de la langue : une page, ou un dossier (terminé par /). « À propos » présente le template,
# pas le cours ; la correction et le tableau de bord du QCM donnent des réponses, que la fenêtre ne doit pas souffler ;
# la page Podcasts résume des épisodes, qui renvoient au cours sans l'expliquer ; la page Polycopié présente le livret,
# pas les notions.
EXCLUES = ("glossaire.html", "about.html", "QCM/correction/", "QCM/dashboard/", "podcasts.html", "polycopie.html")
BALISES_SAUTEES = {"script", "style", "pre", "code", "svg", "button", "nav", "template", "noscript", "select",
                   "textarea"}
CLASSES_SAUTEES = {"sr-only", "chapter-pagination", "chapter-nav"}
VIDES = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
ARRETS = {"de", "du", "des", "à", "au", "aux", "en", "par", "pour", "sur", "sans", "entre", "la", "le", "les", "et",
          "ou", "dans", "avec"}
ARRETS_EN = {"of", "for", "to", "in", "on", "with", "between", "per", "by", "from", "and", "or", "as", "at", "into",
             "&", "vs", "versus", "the", "a", "an"}
IRREGULIERS_EN = {"matrix": "matrices", "index": "indexes", "analysis": "analyses", "criterion": "criteria",
                  "datum": "data", "child": "children", "person": "people"}
FINALES_SANS_PLURIEL_EN = ("ly", "ing", "able", "ible", "less")


# ── les termes ───────────────────────────────────────────────────────────────
def lire_glossaire(site=SITE):
    """window.GLOSSARY de glossaire-data.js, lu comme du JSON : clés citées, virgules finales retirées."""
    src = io.open(os.path.join(site, "assets", "js", "glossaire-data.js"), encoding="utf-8").read()
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    debut = src.index("[", src.index("window.GLOSSARY ") if "window.GLOSSARY " in src else src.index("window.GLOSSARY"))
    prof, i, fin = 0, debut, None                       # le crochet qui ferme le tableau, hors des chaînes
    while i < len(src):
        c = src[i]
        if c == '"':
            i = re.compile(r'"(?:[^"\\]|\\.)*"').match(src, i).end()
            continue
        prof += {"[": 1, "]": -1}.get(c, 0)
        if prof == 0:
            fin = i + 1
            break
        i += 1
    corps = src[debut:fin]
    morceaux, i = [], 0
    for m in re.finditer(r'"(?:[^"\\]|\\.)*"', corps):             # les chaînes restent telles quelles
        hors = corps[i:m.start()]
        hors = re.sub(r"([{,]\s*)([A-Za-z_]\w*)\s*:", r'\1"\2":', hors)
        morceaux.append(re.sub(r",(\s*[}\]])", r"\1", hors))
        morceaux.append(m.group(0))
        i = m.end()
    fin = re.sub(r"([{,]\s*)([A-Za-z_]\w*)\s*:", r'\1"\2":', corps[i:])
    morceaux.append(re.sub(r",(\s*[}\]])", r"\1", fin))
    return json.loads("".join(morceaux))


def ancre(fr):
    """L'ancre d'un terme dans la page du glossaire, comme la calcule son script : « g-objectif-pedagogique »."""
    s = (fr or "").lower().replace("œ", "oe").replace("æ", "ae")
    s = "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    return "g-" + re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def norm(s):
    """Minuscules, parenthèse retirée, espaces resserrés."""
    return re.sub(r"\s+", " ", re.sub(r"\s*\(.*?\)\s*", " ", (s or "").lower())).strip()


def _pluriel_mot(m):
    if not m or not m[-1].isalpha() or m[-1] in "sxz":
        return m
    if m.endswith(("au", "eu")):
        return m + "x"
    if m.endswith("al"):
        return m[:-2] + "aux"
    return m + "s"


def pluriels_fr(forme, sigles=()):
    """Les pluriels plausibles d'une forme française : accord jusqu'au premier mot-outil, ou du seul nom de tête."""
    mots = forme.split(" ")
    accord, tete, actif = [], [], True
    for i, m in enumerate(mots):
        if actif and (m in ARRETS or m.startswith(("d'", "l'", "qu'")) or not m[:1].isalpha()
                      or any(ch.isdigit() for ch in m) or "/" in m):
            actif = False
        variable = actif and m not in sigles
        p = (m.rpartition("-")[0] + "-" + _pluriel_mot(m.rpartition("-")[2])) if "-" in m else _pluriel_mot(m)
        accord.append(p if variable else m)
        tete.append(p if variable and i == 0 else m)
    return {" ".join(accord), " ".join(tete)} - {forme}


def _pluriel_mot_en(m):
    if not m or not m[-1].isalpha():
        return m
    if m in IRREGULIERS_EN:
        return IRREGULIERS_EN[m]
    if m in IRREGULIERS_EN.values() or m.endswith(FINALES_SANS_PLURIEL_EN) or (m.endswith("ed") and not m.endswith("eed")):
        return m
    if m.endswith("ss") or m.endswith(("x", "z", "ch", "sh")):
        return m + "es"
    if m.endswith("s"):
        return m
    if m.endswith("y") and len(m) > 1 and m[-2] not in "aeiou":
        return m[:-1] + "ies"
    return m + "s"


def pluriels_en(forme, sigles=()):
    """Le pluriel anglais plausible d'une forme : celui du nom de tête, avant le premier mot-outil."""
    if "/" in forme:
        return set()
    mots = forme.split(" ")
    tete = len(mots) - 1
    for i, m in enumerate(mots[1:], 1):
        if m in ARRETS_EN:
            tete = i - 1
            break
    m = mots[tete]
    if not m[:1].isalpha() or any(ch.isdigit() for ch in m) or m in sigles or "'" in m:
        return set()
    neuf = (m.rpartition("-")[0] + "-" + _pluriel_mot_en(m.rpartition("-")[2])) if "-" in m else _pluriel_mot_en(m)
    return {" ".join(mots[:tete] + [neuf] + mots[tete + 1:])} - {forme}


def formes(intitule, alias, langue):
    """Les formes d'un terme dans une langue, en minuscules : l'intitulé, les alias, leurs pluriels."""
    if not intitule:
        return []
    sigles = {m.lower() for m in re.findall(r"\b[A-Z][A-Z0-9]+\b", intitule)}
    base = {norm(intitule)} | {norm(a) for a in alias or [] if norm(a)}
    regle = pluriels_en if langue == "en" else pluriels_fr
    out = set(base)
    for f in base:
        out |= regle(f, sigles)
    return sorted(out, key=lambda f: (-len(f), f))


def motif(liste):
    if not liste:
        return None
    corps = "|".join(re.escape(f) for f in sorted(set(liste), key=lambda f: (-len(f), f)))
    return re.compile(r"(?<![\w-])(?:%s)(?![\w-])" % corps)


def normaliser(texte):
    texte = texte.replace("’", "'").replace("‘", "'").replace(" ", " ").replace(" ", " ")
    return re.sub(r"\s+", " ", texte).strip().lower()


def compter(texte, m_formes, m_exclus):
    """Le nombre d'emplois dans un texte normalisé, hors des expressions écartées."""
    if m_formes is None:
        return 0
    zones = [(x.start(), x.end()) for x in m_exclus.finditer(texte)] if m_exclus else []
    return sum(1 for m in m_formes.finditer(texte) if not any(m.start() < b and m.end() > a for a, b in zones))


# ── les pages ────────────────────────────────────────────────────────────────
class Decoupe(HTMLParser):
    """Le texte de <main> dans une langue, découpé en endroits : [ancre, libellé, morceaux] ; et le titre h1."""

    def __init__(self, langue):
        super().__init__(convert_charrefs=True)
        self.langue = langue
        self.main = 0
        self.saut = None
        self.capture = None
        self.h1 = None
        self.endroits = [["", "", []]]

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "main":
            self.main += 1
            return
        if not self.main:
            return
        if self.saut:
            if tag == self.saut[0] and tag not in VIDES:
                self.saut[1] += 1
            return
        classes = set((a.get("class") or "").split())
        autre = a.get("data-tr") and a.get("data-tr") != self.langue
        if (tag in BALISES_SAUTEES or "hidden" in a or a.get("aria-hidden") == "true" or classes & CLASSES_SAUTEES
                or autre):
            if tag not in VIDES:
                self.saut = [tag, 1]
            return
        if tag in ("h2", "h3") and a.get("id"):
            self.endroits.append([a["id"], "", []])
            self.capture = [tag, []]
        elif tag == "h1" and self.h1 is None:
            self.capture = ["h1", []]

    def handle_endtag(self, tag):
        if tag == "main":
            self.main -= 1
            return
        if not self.main:
            return
        if self.saut:
            if tag == self.saut[0]:
                self.saut[1] -= 1
                if not self.saut[1]:
                    self.saut = None
            return
        if self.capture and tag == self.capture[0]:
            texte = re.sub(r"\s+", " ", " ".join(self.capture[1])).strip()
            if tag == "h1":
                self.h1 = texte
            else:
                self.endroits[-1][1] = texte
            self.capture = None

    def handle_data(self, data):
        if not self.main or self.saut:
            return
        self.endroits[-1][2].append(data)
        if self.capture:
            self.capture[1].append(data)


def chapitres(site=SITE):
    """[(fichier, numéro, {fr, en})] d'après site/assets/js/course-data.js, dans l'ordre du cours."""
    src = io.open(os.path.join(site, "assets", "js", "course-data.js"), encoding="utf-8").read()
    return [(m.group(2), m.group(1), {"fr": m.group(3), "en": m.group(4)})
            for m in re.finditer(r"num:\s*'([^']+)'[^}]*?file:\s*'([^']+)'[^}]*?title:\s*\{\s*fr:\s*\"([^\"]*)\","
                                 r"\s*en:\s*\"([^\"]*)\"", src, flags=re.S)]


def zones_protegees():
    try:
        d = json.load(io.open(os.path.join(RACINE, "deploiement", "destination.json"), encoding="utf-8"))
    except (OSError, ValueError):
        return ()
    return tuple(str(z).strip("/") + "/" for z in d.get("zones_protegees") or [] if str(z).strip("/"))


def pages(site=SITE):
    """[(langue, chemin depuis la racine de la langue, fichier)] : chaque page, dans chacune de ses langues."""
    exclues = EXCLUES + zones_protegees()
    out = []
    for f in sorted(glob.glob(os.path.join(site, "**", "*.html"), recursive=True)):
        rel = os.path.relpath(f, site).replace("\\", "/")
        if rel.startswith("assets/"):
            continue
        t = io.open(f, encoding="utf-8").read()
        m = re.search(r'<html\b[^>]*\bdata-langues="([^"]*)"', t)
        langues = m.group(1).split() if m else ["fr", "en"]
        if rel.startswith("en/"):
            rel, langues = rel[3:], ["en"]
        if any(rel == x or (x.endswith("/") and rel.startswith(x)) for x in exclues):
            continue
        out += [(lg, rel, f) for lg in langues]
    return out


def calculer(site=SITE):
    """{langue : {ancre du terme : [endroit…]}} ; un endroit : {p, a, page, section, n}."""
    termes = lire_glossaire(site)
    chaps = chapitres(site)
    rang = {"chapitres/" + f: i for i, (f, _n, _t) in enumerate(chaps)}
    titres = {"chapitres/" + f: (n, t) for f, n, t in chaps}
    regles = {}
    for lg in ("fr", "en"):
        regles[lg] = [(ancre(t.get("fr")), motif(formes(t.get(lg), (t.get("alias") or {}).get(lg), lg)),
                       motif([normaliser(x) for x in (t.get("exclus") or {}).get(lg) or []])) for t in termes]
    out = {"fr": {}, "en": {}}
    lues = sorted(pages(site), key=lambda x: (rang.get(x[1], len(rang)), x[1], x[0]))
    for lg, rel, chemin in lues:
        d = Decoupe(lg)
        d.feed(io.open(chemin, encoding="utf-8").read())
        if rel in titres:
            n, t = titres[rel]
            libelle = ("Chapter %s — %s" if lg == "en" else "Chapitre %s — %s") % (n, t.get(lg) or t["fr"])
        else:
            libelle = d.h1 or rel
        for ancre_endroit, section, morceaux in d.endroits:
            texte = normaliser(" ".join(morceaux))
            if not texte:
                continue
            for cle, m_formes, m_exclus in regles[lg]:
                k = compter(texte, m_formes, m_exclus)
                if k:
                    out[lg].setdefault(cle, []).append({"p": rel, "a": ancre_endroit, "page": libelle,
                                                        "section": section, "n": k})
    return termes, out


def produire(emplois):
    return ("/* =================================================================\n"
            "   glossaire-emplois.js — Où le cours emploie chaque terme du glossaire\n"
            "   FICHIER GÉNÉRÉ par outils/glossaire_emplois.py, d'après les pages du\n"
            "   site : ne pas le modifier à la main. Lu par glossaire.html, sous\n"
            "   chaque terme (« Où en parle-t-on ? »). Par langue, l'ancre du terme\n"
            "   (g-…) donne ses endroits : p, la page depuis la racine de la langue ;\n"
            "   a, l'ancre de la section ; page et section, leurs libellés ; n, le\n"
            "   nombre d'emplois.\n"
            "   ================================================================= */\n"
            "window.GLOSSARY_EMPLOIS = %s;\n" % json.dumps(emplois, ensure_ascii=False, indent=1, sort_keys=True))


def generer(site=SITE, essai=False):
    """(à jour avant ?, nombre de termes, termes employés en français, en anglais)."""
    termes, emplois = calculer(site)
    texte = produire(emplois)
    sortie = os.path.join(site, "assets", "js", "glossaire-emplois.js")
    ancien = io.open(sortie, encoding="utf-8").read() if os.path.exists(sortie) else None
    a_jour = ancien == texte
    if not a_jour and not essai:
        with io.open(sortie, "w", encoding="utf-8", newline="\n") as f:
            f.write(texte)
    return a_jour, len(termes), len(emplois["fr"]), len(emplois["en"])


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--essai", action="store_true", help="dit si le fichier est à jour, sans rien écrire")
    args = ap.parse_args()
    a_jour, n, fr, en = generer(essai=args.essai)
    print("glossaire-emplois.js : %d terme(s) ; employés dans le cours : %d en français, %d en anglais — %s"
          % (n, fr, en, "à jour" if a_jour else ("PAS À JOUR — rien écrit" if args.essai else "écrit")))
    return 1 if (args.essai and not a_jour) else 0


if __name__ == "__main__":
    sys.exit(main())
