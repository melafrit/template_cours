# -*- coding: utf-8 -*-
"""Où sont les choses : le site, ses pages dans chaque langue, l'adresse publique, le cours, le glossaire.

Le livret ne recopie rien : il lit les pages du site (site/), le cours tel que le décrit site/assets/js/course-data.js
(titre, auteur, chapitres), le glossaire du site (glossaire-data.js, lu comme outils/glossaire_emplois.py le lit) et
la fiche du livret (outils/livret.py). Une page bilingue en blocs data-tr se lit dans la langue du livret
(outils/miroir.py, garder_langue) ; sur un site miroir, la page anglaise est sa jumelle sous site/en/.

L'ADRESSE PUBLIQUE est l'« url » de deploiement/destination.json, comme pour outils/hreflang.py : un QR code porte
toujours une adresse absolue de ce site. Sans elle (le gabarit lui-même, un cours pas encore en ligne), les QR codes
portent l'adresse d'exemple EXEMPLE et la vérification en ligne n'a pas lieu : le livret le dit.
"""
import io
import json
import os
import re
import sys
from urllib.parse import urljoin, urlsplit

from . import libelles

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SITE_LOCAL = os.path.join(RACINE, "site")
OUTILS = os.path.join(RACINE, "outils")
if OUTILS not in sys.path:
    sys.path.insert(0, OUTILS)

import miroir  # noqa: E402
try:
    import glossaire_emplois as GE  # noqa: E402
except ImportError:                    # un cours sans glossaire : la page Polycopié s'écrit (generer_fragments.py),
    GE = None                          # le livret, lui, refuse de se composer (Langue.glossaire)

TRAVAIL = os.path.join(RACINE, "Polycopie")            # l'espace de travail du livret : jamais publié
CACHE = os.path.join(TRAVAIL, "_cache")                # images et QR codes regénérables (non versionnés)
EXEMPLE = "https://example.org/cours/"                 # example.org : un domaine réservé aux exemples (RFC 2606)


def adresse_publique():
    """L'adresse publique du cours, terminée par « / » (« url » de deploiement/destination.json), ou ""."""
    try:
        d = json.load(io.open(os.path.join(RACINE, "deploiement", "destination.json"), encoding="utf-8"))
    except (OSError, ValueError):
        return ""
    url = str(d.get("url") or "").strip()
    return url.rstrip("/") + "/" if url else ""


ADRESSE = adresse_publique()
SITE = ADRESSE or EXEMPLE


# ── le cours (course-data.js) et la fiche du livret ────────────────────────
def js_vers_json(texte):
    """Un littéral d'objet JavaScript simple → du JSON : commentaires ôtés, chaînes entre apostrophes mises entre
    guillemets, clés citées, virgules finales retirées."""
    out, i, n = [], 0, len(texte)
    while i < n:
        c = texte[i]
        if texte.startswith("/*", i):
            i = texte.index("*/", i) + 2
            continue
        if texte.startswith("//", i):
            fin = texte.find("\n", i)
            i = n if fin < 0 else fin
            continue
        if c in "\"'":
            j, morceau = i + 1, []
            while texte[j] != c:
                if texte[j] == "\\":
                    morceau.append(texte[j:j + 2])
                    j += 2
                    continue
                morceau.append('\\"' if texte[j] == '"' else texte[j])
                j += 1
            corps = "".join(morceau).replace("\\'", "'")
            out.append('"' + corps + '"')
            i = j + 1
            continue
        out.append(c)
        i += 1
    s = "".join(out)
    morceaux, i = [], 0
    for m in re.finditer(r'"(?:[^"\\]|\\.)*"', s):
        hors = re.sub(r"([{,]\s*)([A-Za-z_]\w*)\s*:", r'\1"\2":', s[i:m.start()])
        morceaux.append(re.sub(r",(\s*[}\]])", r"\1", hors))
        morceaux.append(m.group(0))
        i = m.end()
    fin = re.sub(r"([{,]\s*)([A-Za-z_]\w*)\s*:", r'\1"\2":', s[i:])
    morceaux.append(re.sub(r",(\s*[}\]])", r"\1", fin))
    return json.loads("".join(morceaux))


def donnees_cours():
    """window.COURSE de site/assets/js/course-data.js : title, subtitle, author, chapters [{num, file, title}]."""
    src = io.open(os.path.join(SITE_LOCAL, "assets", "js", "course-data.js"), encoding="utf-8").read()
    debut = src.index("{", src.index("window.COURSE"))
    prof, i = 0, debut
    while i < len(src):
        c = src[i]
        if c in "\"'":
            m = re.compile(r'"(?:[^"\\]|\\.)*"' if c == '"' else r"'(?:[^'\\]|\\.)*'").match(src, i)
            i = m.end()
            continue
        if src.startswith("/*", i):
            i = src.index("*/", i) + 2
            continue
        prof += {"{": 1, "}": -1}.get(c, 0)
        if prof == 0:
            return js_vers_json(src[debut:i + 1])
        i += 1
    raise SystemExit("course-data.js : l'objet window.COURSE ne se ferme pas.")


def fiche_livret():
    """La fiche du livret du cours (outils/livret.py, LIVRET), ou un dictionnaire vide."""
    chemin = os.path.join(OUTILS, "livret.py")
    if not os.path.isfile(chemin):
        return {}
    import importlib.util
    spec = importlib.util.spec_from_file_location("livret", chemin)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return dict(getattr(module, "LIVRET", {}) or {})


# ── la langue ──────────────────────────────────────────────────────────────
class Langue:
    """Ce qui change d'une langue à l'autre : la page à lire (sa jumelle sous en/, ou la page bilingue réduite à la
    langue), son adresse publique, les libellés du livret, le glossaire."""

    def __init__(self, code):
        if code not in ("fr", "en"):
            raise ValueError(f"langue inconnue : {code!r} (fr ou en)")
        self.code = code
        self.cours = donnees_cours()
        self.livret = fiche_livret()
        self.L = libelles.L(code, self.cours, self.livret)
        self._glossaire = None

    # ── les pages ──────────────────────────────────────────────────────────
    def jumelle(self, rel):
        """Vrai si la page (depuis la racine du site, ancre ôtée) a une jumelle anglaise sous site/en/ (site miroir)."""
        page = rel.split("#", 1)[0] or "index.html"
        return self.code == "en" and os.path.isfile(os.path.join(SITE_LOCAL, "en", *page.split("/")))

    def fichier(self, rel):
        """Le fichier local d'une page du site dans cette langue (« chapitres/01-….html »)."""
        page = rel.split("#", 1)[0]
        base = os.path.join(SITE_LOCAL, "en") if self.jumelle(page) else SITE_LOCAL
        return os.path.join(base, *page.split("/"))

    def html(self, rel):
        """Le HTML d'une page, dans cette langue : une page bilingue (blocs data-tr) ne garde que la sienne."""
        texte = io.open(self.fichier(rel), encoding="utf-8").read()
        if miroir.bilingue(texte):
            texte = miroir.garder_langue(texte, self.code)
        return texte

    def url(self, rel):
        """L'adresse publique absolue d'une page du site, dans cette langue (sa jumelle sous en/ s'il y en a une)."""
        rel = rel.lstrip("/")
        return SITE + ("en/" if self.jumelle(rel) else "") + rel

    def resoudre(self, href, page_rel):
        """L'adresse absolue d'un lien lu dans une page (href relatif à cette page, ou déjà absolu)."""
        return urljoin(self.url(page_rel), href)

    def locale(self, url):
        """Le fichier local que désigne une adresse du site (None pour une adresse hors du site)."""
        if not url.startswith(SITE):
            return None
        chemin = urlsplit(url).path[len(urlsplit(SITE).path):]
        return os.path.join(SITE_LOCAL, *chemin.split("/"))

    # ── le cours ───────────────────────────────────────────────────────────
    def chapitres(self):
        """[(numéro, page depuis la racine du site, titre dans la langue)], dans l'ordre de course-data.js."""
        out = []
        for ch in self.cours.get("chapters", []):
            titre = ch.get("title") or {}
            out.append((str(ch.get("num", "")), "chapitres/" + ch["file"],
                        titre.get(self.code) or titre.get("fr", "") if isinstance(titre, dict) else titre))
        return out

    # ── le glossaire du site ───────────────────────────────────────────────
    def glossaire(self):
        """Les entrées du glossaire, dans cette langue : terme, fr, en, définition, ancre (g-…), alias, exclus."""
        if GE is None:
            raise SystemExit("✗ Le livret imprime le glossaire du cours — en fin de livret, dans la marge, dans "
                             "l'index — : outils/glossaire_emplois.py manque (bloc « glossaire » de nouveau_cours.py).")
        if self._glossaire is None:
            out = []
            for e in GE.lire_glossaire(SITE_LOCAL):
                d, a, x = e.get("def") or {}, e.get("alias") or {}, e.get("exclus") or {}
                out.append(dict(terme=e.get(self.code) or e.get("fr", ""), fr=e.get("fr", ""), en=e.get("en", ""),
                                definition=d.get(self.code) or d.get("fr", ""), ancre=GE.ancre(e.get("fr", "")),
                                alias=a.get(self.code, []) if isinstance(a, dict) else [],
                                exclus=x.get(self.code, []) if isinstance(x, dict) else []))
            self._glossaire = out
        return self._glossaire


def presentation_auteur(langue):
    """Le texte de « À propos de l'auteur », dans la langue : celui de la fiche du livret (outils/livret.py,
    « presentation »), mot pour mot. Le livret refuse de s'écrire sans lui plutôt que d'imprimer un texte que
    l'auteur n'a pas validé."""
    texte = (fiche_livret().get("presentation") or {}).get(langue, "")
    if not str(texte).strip():
        raise SystemExit(f"Présentation de l'auteur absente ({langue}) : outils/livret.py, LIVRET[\"presentation\"]"
                         f"[\"{langue}\"] — le texte validé par l'auteur, qui s'imprime mot pour mot.")
    return re.sub(r"\s+", " ", str(texte)).strip()
