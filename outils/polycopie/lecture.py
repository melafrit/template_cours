# -*- coding: utf-8 -*-
"""Une page du site → une suite de blocs.

La page se lit dans <main class="main-content"> (lxml), dans la langue du livret (sources.Langue.html : une page en
blocs data-tr ne garde que la sienne) ; ses composants — capsules et activités du moteur — se lisent tels que la page
les monte, par Chrome sans interface (navigateur.composants) : le livret imprime exactement ce que voient les
étudiants, sans les réponses. Ce module ne sait rien de Word : rendu.py transforme les blocs en paragraphes.

LES BLOCS
  Titre(niveau, contenu, ident)        h2, h3, h4
  Paragraphe(contenu, genre)           genre : texte, chapeau (p.lead)
  Liste(items, ordonnee)               items : [(contenu, sous-liste ou None)]
  Tableau(entetes, lignes, legende)    cellules : Cellule(contenu, entete) ; contenu : liste de paragraphes
  Figure(genre, source, …)             genre : schema (fichier SVG), illustration (WebP, PNG, JPEG)
  Encadre(genre, titre, blocs)         genre : retenir (div.takeaways), repere et piege (div.callout), plus_loin
                                       (details)
  Activite(genre, ident, donnees)      checkpoint, reveal, match, spotError, branch, hotspots (données du moteur,
                                       réponses comprises : c'est rendu.py qui n'en imprime aucune)
  Capsule(ident, donnees)              une capsule audio (RDCX.voice)
  Revision(ident)                      les flashcards du chapitre (div#flash-…) : un QR code dans la marge
  Code(texte)                          pre
Les médias que la page charge d'elle-même (podcast, slides, infographie du chapitre : assets/js/media.js), sa
pagination et l'encadré « Le podcast du chapitre » ne deviennent pas des blocs : l'ouverture du chapitre porte le QR
code de son épisode (outils/podcasts.py).

LE TEXTE EN LIGNE est une liste de Seg(texte, gras, italique, code, lien, exposant) ; les espaces s'y replient
comme dans un navigateur, les pictogrammes du site (émojis) s'en vont : le livret a les siens.
"""
import re
from dataclasses import dataclass, field
from typing import Optional

import lxml.html
from lxml import etree

from . import navigateur

# ── le texte en ligne ──────────────────────────────────────────────────────


@dataclass
class Seg:
    texte: str
    gras: bool = False
    italique: bool = False
    code: bool = False
    lien: Optional[str] = None
    exposant: bool = False

    def forme(self):
        return (self.gras, self.italique, self.code, self.lien, self.exposant)


EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿⬀-⯿⌀-⏿️‍⃣]")
ESPACES = re.compile(r"[ \t\r\n\f]+")


def sans_emoji(texte):
    return EMOJI.sub("", texte)


def texte_brut(contenu):
    return "".join(s.texte for s in contenu)


def replier(contenu):
    """Replie les espaces comme un navigateur, ôte les émojis, fusionne les morceaux de même forme, coupe les
    espaces de début et de fin."""
    out = []
    for s in contenu:
        if s.texte == "\n":
            out.append(Seg("\n", *s.forme()))
            continue
        t = ESPACES.sub(" ", sans_emoji(s.texte))
        if not t:
            continue
        if out and out[-1].texte != "\n" and (out[-1].texte.endswith(" ") or out[-1].texte == "") and t.startswith(" "):
            t = t[1:]
        elif out and out[-1].texte == "\n" and t.startswith(" "):
            t = t[1:]
        if not t:
            continue
        if out and out[-1].texte != "\n" and out[-1].forme() == s.forme():
            out[-1] = Seg(out[-1].texte + t, *s.forme())
        else:
            out.append(Seg(t, *s.forme()))
    while out and out[0].texte.strip() == "" and out[0].texte != "\n":
        out.pop(0)
    while out and out[0].texte == "\n":
        out.pop(0)
    if out and out[0].texte != "\n":
        out[0] = Seg(out[0].texte.lstrip(), *out[0].forme())
    while out and (out[-1].texte.strip() == "" or out[-1].texte == "\n"):
        out.pop()
    if out:
        out[-1] = Seg(out[-1].texte.rstrip(), *out[-1].forme())
    return [s for s in out if s.texte]


def classes(el):
    return set((el.get("class") or "").split())


SAUTES = {"script", "style", "button", "noscript", "template", "svg", "img", "nav", "input", "select", "textarea"}
CLASSES_SAUTEES = {"callout-icon", "ico", "sr-only", "podcast-icon", "slides-icon"}
BLOCS_INTERNES = {"p", "div", "ul", "ol", "li", "table", "tr", "section", "figure", "h1", "h2", "h3", "h4", "h5",
                  "blockquote", "details", "summary", "pre", "aside"}
# Ce que la page montre d'elle-même et que le livret ne reprend pas en blocs (voir l'en-tête du module).
SECTIONS_SAUTEES = {"podcast-section", "slides-section", "infographie-section", "chapter-pagination", "pod-renvoi"}


def en_ligne(el, forme=None, garder=frozenset()):
    """Le texte en ligne d'un élément : ses morceaux, avec leur forme. Les blocs imbriqués sont séparés par un saut
    de ligne double (rendu.py en fait des paragraphes) ; garder : des classes à ne pas sauter."""
    forme = dict(forme or {})
    out = []

    def texte(t):
        if t:
            out.append(Seg(t, forme.get("gras", False), forme.get("italique", False), forme.get("code", False),
                           forme.get("lien"), forme.get("exposant", False)))

    texte(el.text)
    for enfant in el:
        if isinstance(enfant, (etree._Comment, etree._ProcessingInstruction)) or not isinstance(enfant.tag, str):
            texte(enfant.tail)
            continue
        tag = enfant.tag.lower()
        if tag in SAUTES or (classes(enfant) & CLASSES_SAUTEES - set(garder)) or enfant.get("hidden") is not None \
                or enfant.get("aria-hidden") == "true":
            texte(enfant.tail)
            continue
        if tag == "br":
            out.append(Seg("\n", *[forme.get(k, False) for k in ("gras", "italique", "code")],
                           forme.get("lien"), forme.get("exposant", False)))
            texte(enfant.tail)
            continue
        sous = dict(forme)
        if tag in ("strong", "b"):
            sous["gras"] = True
        elif tag in ("em", "i", "cite"):
            sous["italique"] = True
        elif tag in ("code", "kbd", "samp"):
            sous["code"] = True
        elif tag == "a":
            sous["lien"] = enfant.get("href")
        elif tag == "sup":
            sous["exposant"] = True
        morceaux = en_ligne(enfant, sous, garder)
        if tag in BLOCS_INTERNES and out and morceaux:
            out.append(Seg("\n\n"))
        out.extend(morceaux)
        texte(enfant.tail)
    return out


def ligne(el, garder=frozenset()):
    """Le texte en ligne replié d'un élément."""
    return replier(en_ligne(el, garder=garder))


def chaine(el):
    """Le texte brut replié d'un élément."""
    return texte_brut(ligne(el)).strip()


def paragraphes(contenu):
    """Coupe un texte en ligne aux sauts doubles (blocs imbriqués d'une cellule) : liste de textes en ligne."""
    out, courant = [], []
    for s in contenu:
        if s.texte == "\n\n":
            if courant:
                out.append(replier(courant))
            courant = []
        else:
            courant.append(s)
    if courant:
        out.append(replier(courant))
    return [p for p in out if p]


# ── les blocs ──────────────────────────────────────────────────────────────
@dataclass
class Titre:
    niveau: int
    contenu: list
    ident: Optional[str] = None


@dataclass
class Paragraphe:
    contenu: list
    genre: str = "texte"


@dataclass
class Liste:
    items: list
    ordonnee: bool = False


@dataclass
class Cellule:
    contenu: list               # liste de paragraphes (chacun un texte en ligne)
    entete: bool = False


@dataclass
class Tableau:
    entetes: list               # lignes d'en-tête : [[Cellule]]
    lignes: list                # [[Cellule]]
    legende: list = field(default_factory=list)


@dataclass
class Figure:
    genre: str                  # schema, illustration
    source: str                 # chemin local
    legende: list = field(default_factory=list)
    numero: str = ""
    ident: Optional[str] = None
    alt: str = ""


@dataclass
class Encadre:
    genre: str
    titre: list = field(default_factory=list)
    blocs: list = field(default_factory=list)
    etiquette: Optional[str] = None


@dataclass
class Activite:
    genre: str
    ident: str
    donnees: dict


@dataclass
class Capsule:
    ident: str
    donnees: dict


@dataclass
class Revision:
    ident: str


@dataclass
class Code:
    texte: str


@dataclass
class Page:
    """Une page lue : son adresse (depuis la racine du site), ses blocs et ce que porte son en-tête."""
    rel: str
    blocs: list
    titre: str = ""
    sous_titre: list = field(default_factory=list)
    objectifs_titre: str = ""
    objectifs: list = field(default_factory=list)
    duree: str = ""
    badge: str = ""
    capsule_ouverture: Optional[Capsule] = None
    sections: list = field(default_factory=list)     # (ident, titre) des h2
    retenir: Optional[str] = None                    # l'ident de l'encadré « À retenir »
    retenir_titre: str = ""
    activites: dict = field(default_factory=dict)    # ident → (genre, données)
    idents: set = field(default_factory=set)         # les ancres de la page que le livret signe (renvois de pages)


def fragment(el, nom):
    """Le texte d'un fragment (<!-- FRAGMENT:nom -->…<!-- /FRAGMENT:nom -->) dans un élément."""
    for c in el.iter(etree.Comment):
        if c.text and c.text.strip() == f"FRAGMENT:{nom}":
            return (c.tail or "").strip()
    return ""


# ── la lecture ─────────────────────────────────────────────────────────────
class Lecteur:
    def __init__(self, langue, rel, composants=None):
        self.langue = langue
        self.rel = rel
        self.chemin = langue.fichier(rel)
        self.texte = langue.html(rel)
        self.rdcx = composants if composants is not None else navigateur.composants(self.chemin, langue.code)
        racine = lxml.html.fromstring(self.texte)
        mains = racine.xpath('//main[contains(concat(" ", normalize-space(@class), " "), " main-content ")]')
        if not mains:
            raise SystemExit(f"Pas de <main class=\"main-content\"> dans {rel}")
        self.main = mains[0]
        self.compte = 0                     # un numéro pour les identifiants qui manquent (encadrés « À retenir »)

    def local(self, href):
        """Le fichier local d'une ressource liée par la page (src d'une image)."""
        return self.langue.locale(self.langue.resoudre(href, self.rel))

    # ── la page ────────────────────────────────────────────────────────────
    def lire(self):
        page = Page(rel=self.rel, blocs=[], activites=self.rdcx)
        blocs = []
        for el in self.main:
            if not isinstance(el.tag, str):
                continue
            c = classes(el)
            if "chapter-header" in c:
                self._entete(el, page)
            elif c & SECTIONS_SAUTEES:
                continue
            else:
                blocs.extend(self.blocs_de_element(el))
        # La capsule qui précède la première section ouvre le chapitre.
        premier_titre = next((i for i, b in enumerate(blocs) if isinstance(b, Titre) and b.niveau == 2), len(blocs))
        for i, b in enumerate(blocs[:premier_titre]):
            if isinstance(b, Capsule) and page.capsule_ouverture is None:
                page.capsule_ouverture = b
                blocs[i] = None
        page.blocs = [b for b in blocs if b is not None]
        page.sections = [(b.ident, texte_brut(b.contenu)) for b in page.blocs
                         if isinstance(b, Titre) and b.niveau == 2 and b.ident]
        for b in page.blocs:
            if isinstance(b, Encadre) and b.genre == "retenir":
                page.retenir, page.retenir_titre = b.etiquette, texte_brut(b.titre)
        page.idents = idents_signes(page.blocs)
        return page

    def _entete(self, el, page):
        t = el.xpath('.//*[contains(@class,"chapter-title")]')
        page.titre = chaine(t[0]) if t else ""
        s = el.xpath('.//*[contains(@class,"chapter-subtitle")]')
        page.sous_titre = ligne(s[0]) if s else []
        page.duree = next((fragment(el, n) for n in [c.text.strip()[9:] for c in el.iter(etree.Comment)
                           if c.text and c.text.strip().startswith("FRAGMENT:duree-")]), "")
        badge = el.xpath('.//*[contains(@class,"chapter-badge")]')
        page.badge = chaine(badge[0]) if badge else ""
        obj = el.xpath('.//*[contains(@class,"chapter-objectives")]')
        if obj:
            h = obj[0].find(".//h3")
            page.objectifs_titre = chaine(h) if h is not None else ""
            page.objectifs = [ligne(li) for li in obj[0].iter("li")]

    # ── les blocs ──────────────────────────────────────────────────────────
    def blocs_de(self, conteneur):
        out = []
        for el in conteneur:
            if isinstance(el.tag, str):
                out.extend(self.blocs_de_element(el))
        return out

    def blocs_de_element(self, el):
        tag, c = el.tag.lower(), classes(el)
        if tag in ("script", "style", "template", "noscript", "nav", "button") or el.get("hidden") is not None \
                or c & SECTIONS_SAUTEES:
            return []
        ident = el.get("id")
        if tag in ("h2", "h3", "h4", "h5"):
            return [Titre(int(tag[1]), ligne(el), ident)]
        if tag == "p":
            contenu = ligne(el)
            return [Paragraphe(contenu, "chapeau" if "lead" in c else "texte")] if contenu else []
        if tag in ("ul", "ol"):
            return [self._liste(el, tag == "ol")]
        if tag == "table":
            return [self._tableau(el)]
        if tag == "pre":
            return [Code(el.text_content().rstrip("\n"))]
        if tag == "figure":
            return self._figure(el)
        if tag == "details":
            return [self._details(el)]
        if tag in ("div", "section", "aside", "blockquote"):
            if ident and ident in self.rdcx and not len(el):
                genre, donnees = self.rdcx[ident]
                return [Capsule(ident, donnees) if genre == "voice" else Activite(genre, ident, donnees)]
            if ident and ident.startswith("flash-") and not len(el):
                return [Revision(ident)]
            if "table-scroll" in c:
                t = el.find(".//table")
                return [self._tableau(t)] if t is not None else []
            if "callout" in c:
                return [self._callout(el, c)]
            if "takeaways" in c:
                return [self._retenir(el)]
            return self.blocs_de(el)
        if tag in ("span", "a", "strong", "em"):
            contenu = ligne(el)
            return [Paragraphe(contenu)] if contenu else []
        return []

    def _liste(self, el, ordonnee):
        items = []
        for li in el:
            if not isinstance(li.tag, str) or li.tag.lower() != "li":
                continue
            sous = [x for x in li if isinstance(x.tag, str) and x.tag.lower() in ("ul", "ol")]
            for x in sous:
                li.remove(x)
            sous_liste = self._liste(sous[0], sous[0].tag.lower() == "ol") if sous else None
            items.append((ligne(li), sous_liste))
        return Liste(items, ordonnee)

    def _tableau(self, t):
        entetes, lignes = [], []
        legende = t.find("caption")
        for tr in t.iter("tr"):
            parent = tr.getparent().tag.lower()
            cellules = [Cellule(paragraphes(en_ligne(td)), td.tag.lower() == "th")
                        for td in tr if isinstance(td.tag, str) and td.tag.lower() in ("td", "th")]
            (entetes if parent == "thead" else lignes).append(cellules)
        return Tableau(entetes, lignes, ligne(legende) if legende is not None else [])

    def _figure(self, el):
        cap = el.find("figcaption")
        legende = ligne(cap) if cap is not None else []
        img = el.find(".//img")
        if img is None:
            return []
        src = (img.get("src") or "").strip()
        chemin = self.local(src) if src else ""         # adresse vide : une image pas encore produite (rendu.py)
        if chemin is None:                               # hors du site : non imprimée
            return []
        genre = "schema" if src.split("?")[0].lower().endswith(".svg") else "illustration"
        return [Figure(genre, chemin, legende, "", el.get("id"), img.get("alt") or "")]

    def _details(self, el):
        resume = el.find("summary")
        titre = ligne(resume) if resume is not None else []
        blocs = [b for x in el if x is not resume and isinstance(x.tag, str) for b in self.blocs_de_element(x)]
        return Encadre("plus_loin", titre, blocs)

    def _callout(self, el, c):
        contenu = el.xpath('./*[contains(@class,"callout-content")]')
        corps = contenu[0] if contenu else el
        h = corps.find("h4")
        titre = ligne(h) if h is not None else []
        if h is not None:
            corps.remove(h)
        genre = "piege" if ("warning" in c or "danger" in c) else "repere"
        return Encadre(genre, titre, self.blocs_de(corps))

    def _retenir(self, el):
        h = el.find(".//h3")
        titre = ligne(h) if h is not None else []
        corps = el.xpath('.//*[contains(@class,"takeaways-body")]')
        self.compte += 1
        ident = el.get("id") or f"retenir-{self.compte}"
        return Encadre("retenir", titre, self.blocs_de(corps[0]) if corps else [], etiquette=ident)


def idents_signes(blocs):
    """Les ancres d'une page que le livret pose en signets (cibles des renvois « p. n ») : intertitres, activités,
    « À retenir »."""
    out = set()

    def voir(liste):
        for b in liste:
            if isinstance(b, (Titre, Activite)) and getattr(b, "ident", None):
                out.add(b.ident)
            if isinstance(b, Encadre):
                if b.genre == "retenir" and b.etiquette:
                    out.add(b.etiquette)
                voir(b.blocs)
    voir(blocs)
    return out


def lire_page(langue, rel):
    return Lecteur(langue, rel).lire()


def texte_visible(page):
    """Tout le texte qu'une page montre à l'étudiant (hors données des activités) : sert aux contrôles, pour ne pas
    prendre pour une réponse imprimée une phrase que le chapitre dit lui-même."""
    morceaux = [page.titre, texte_brut(page.sous_titre)] + [texte_brut(o) for o in page.objectifs]

    def blocs(liste):
        for b in liste:
            if isinstance(b, (Titre, Paragraphe)):
                morceaux.append(texte_brut(b.contenu))
            elif isinstance(b, Liste):
                for contenu, sous in b.items:
                    morceaux.append(texte_brut(contenu))
                    if sous:
                        blocs([sous])
            elif isinstance(b, Tableau):
                morceaux.append(texte_brut(b.legende))
                for rang in b.entetes + b.lignes:
                    morceaux.extend(texte_brut(p) for c in rang for p in c.contenu)
            elif isinstance(b, Figure):
                morceaux.append(texte_brut(b.legende))
            elif isinstance(b, Encadre):
                morceaux.append(texte_brut(b.titre))
                blocs(b.blocs)
            elif isinstance(b, Code):
                morceaux.append(b.texte)

    blocs(page.blocs)
    return "\n".join(m for m in morceaux if m)
