# -*- coding: utf-8 -*-
"""La page d'accueil : les boutons de son bandeau et les cartes de ses chapitres.

outils/generer_fragments.py écrit ces deux fragments dans les pages, dans la langue de chacune :

    <!-- FRAGMENT:accueil-boutons -->…<!-- /FRAGMENT:accueil-boutons -->
    <!-- FRAGMENT:cartes-chapitres -->…<!-- /FRAGMENT:cartes-chapitres -->

accueil-boutons    « Commencer le chapitre 1 », vers le premier chapitre de course-data.js, puis les boutons de
                   BOUTONS. Une adresse externe s'ouvre dans un nouvel onglet, et le dit aux lecteurs d'écran.
cartes-chapitres   une carte par chapitre de course-data.js : son numéro et sa durée (referentiel.DUREES), son
                   titre, le sous-titre de sa page, et son illustration si elle est déposée
                   (site/assets/media/illustrations/chapitre-<N>-carte.webp) ; l'emoji du chapitre sinon.

Les adresses vivent ici, jamais dans la page : un cours créé remplace BOUTONS, et la page suit. Une page jumelle
(en/, ar/) mène aux jumelles qui existent, et aux pages de la langue racine sinon, marquées hreflang.

Décision de l'auteur du 21 novembre 2026 (lot 3) : dans la démonstration, le dépôt sur Livrables, l'application de
tous ses cours, et le QCM de la démonstration, qui ne prépare aucune épreuve réelle. Les épreuves d'un bloc
viendront avec le bloc école (lot 2), un bouton par filière.
"""
import html
import io
import json
import os
import posixpath
import re

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(RACINE, "site")
FRAGMENT = re.compile(r"^(accueil-boutons|cartes-chapitres)$")
INDENT = "      "

# Les boutons du bandeau, après « Commencer le chapitre 1 ».
#   href     une adresse externe (https://…) ou une page du site, depuis sa racine ;
#   phare    le cercle d'accent, pour le bouton qui sert le plus (le dépôt, à chaque échéance) ;
#   filiere  l'id d'une filière de course-data.js, pour un bouton propre à une filière (les épreuves de son bloc).
BOUTONS = [
    {"ico": "📥", "href": "https://livrables.elafrit.com/", "phare": True,
     "titre": {"fr": "Déposer mes livrables", "en": "Submit my deliverables"},
     "detail": {"fr": "livrables.elafrit.com", "en": "livrables.elafrit.com"}},
    {"ico": "📝", "href": "QCM/index.html",
     "titre": {"fr": "QCM d'évaluation", "en": "Assessment quiz"},
     "detail": {"fr": "noté, à degré de certitude", "en": "graded, certainty-based"}},
]

# Les libellés que les fragments écrivent eux-mêmes. L'arabe viendra avec la page d'accueil arabe (lot 4), d'après
# docs/LEXIQUE-ar.md ; d'ici là, une page arabe reçoit le français.
LIBELLES = {
    "fr": {"commencer": "Commencer le chapitre %s", "fleche": "→", "onglet": " (nouvel onglet)",
           "chapitre": "Chapitre %s", "chapitres": "Les chapitres du cours"},
    "en": {"commencer": "Start chapter %s", "fleche": "→", "onglet": " (opens in a new tab)",
           "chapitre": "Chapter %s", "chapitres": "The course chapters"},
}

_CHAINE = r"(?:\"((?:[^\"\\]|\\.)*)\"|'((?:[^'\\]|\\.)*)')"
_CHAPITRE = re.compile(r"\{\s*num:\s*" + _CHAINE + r"\s*,\s*ico:\s*" + _CHAINE + r"\s*,\s*file:\s*" + _CHAINE
                       + r"\s*,\s*title:\s*\{(?P<titres>[^}]*)\}\s*\}", re.S)
_TITRE = re.compile(r"\b(fr|en|ar)\s*:\s*" + _CHAINE)


def _js(double, simple):
    """La valeur d'une chaîne JavaScript, entre guillemets doubles ou simples."""
    if double is not None:
        return json.loads('"%s"' % double)
    return json.loads('"%s"' % simple.replace("\\'", "'").replace('"', '\\"'))


def texte(s):
    """Un texte à poser entre deux balises : seuls &, < et > s'échappent (l'apostrophe reste une apostrophe)."""
    return html.escape(s, quote=False)


def libelle(langue, cle):
    return LIBELLES.get(langue, LIBELLES["fr"])[cle]


def racine():
    """La langue de la racine du site : celle de site/index.html."""
    t = io.open(os.path.join(SITE, "index.html"), encoding="utf-8").read()
    m = re.search(r'<html\b[^>]*\blang="([a-z]{2})"', t)
    return m.group(1) if m else "fr"


def chapitres():
    """[(num, ico, fichier, {langue: titre})], dans l'ordre de course-data.js."""
    src = io.open(os.path.join(SITE, "assets", "js", "course-data.js"), encoding="utf-8").read()
    bloc = re.search(r"\bchapters\s*:\s*\[(.*?)\n\s*\]", src, re.S)
    out = []
    for m in _CHAPITRE.finditer(bloc.group(1) if bloc else ""):
        g = m.groups()
        titres = {t.group(1): _js(t.group(2), t.group(3)) for t in _TITRE.finditer(m.group("titres"))}
        out.append((_js(g[0], g[1]), _js(g[2], g[3]), _js(g[4], g[5]), titres))
    return out


def cible(chemin, langue, rac):
    """(chemin depuis la racine du site, langue de la page visée) : la jumelle dans la langue si elle existe."""
    if langue != rac and os.path.isfile(os.path.join(SITE, langue, chemin)):
        return langue + "/" + chemin, langue
    return chemin, rac


def lien(chemin, page):
    """Le chemin relatif de la page page (depuis la racine du site) vers chemin."""
    return posixpath.relpath(chemin, posixpath.dirname(page) or ".")


def resume(fichier, langue, rac):
    """Le sous-titre de la page du chapitre, en texte brut : celui de la jumelle dans la langue, sinon de la racine."""
    chemin, _lg = cible("chapitres/" + fichier, langue, rac)
    p = os.path.join(SITE, chemin)
    if not os.path.isfile(p):
        return ""
    m = re.search(r'<p class="chapter-subtitle">(.*?)</p>', io.open(p, encoding="utf-8").read(), re.S)
    if not m:
        return ""
    texte = re.sub(r"<!--.*?-->", "", m.group(1), flags=re.S)
    return " ".join(html.unescape(re.sub(r"<[^>]+>", "", texte)).split())


def boutons(langue, page, rac):
    chs = chapitres()
    lignes = ['<div class="landing-actions">']
    if chs:
        chemin, lg = cible("chapitres/" + chs[0][2], langue, rac)
        lignes.append(
            '  <a class="header-cta" data-chapitre="1" href="%s"%s><span aria-hidden="true">🚀</span> <span>%s</span> '
            '<span aria-hidden="true">%s</span></a>'
            % (lien(chemin, page), ' hreflang="%s"' % lg if lg != langue else "",
               texte(libelle(langue, "commencer") % chs[0][0]), libelle(langue, "fleche")))
    for b in BOUTONS:
        externe = b["href"].startswith(("http://", "https://"))
        if externe:
            href, attrs = b["href"], ' target="_blank" rel="noopener noreferrer"'
        else:
            chemin, lg = cible(b["href"], langue, rac)
            href, attrs = lien(chemin, page), (' hreflang="%s"' % lg if lg != langue else "")
        titre = b["titre"].get(langue) or b["titre"].get(rac) or b["titre"]["fr"]
        detail = b["detail"].get(langue) or b["detail"].get(rac) or b["detail"]["fr"]
        classes = "header-cta cta-externe" + (" cta-phare" if b.get("phare") else "")
        a = ('<a class="%s" href="%s"%s><span class="cta-ico" aria-hidden="true">%s</span><span class="cta-textes">'
             '<span class="cta-titre">%s</span><span class="cta-url">%s%s</span></span>%s</a>'
             % (classes, html.escape(href), attrs, b["ico"], texte(titre), texte(detail),
                ' <span aria-hidden="true">↗</span>' if externe else "",
                '<span class="sr-only">%s</span>' % texte(libelle(langue, "onglet")) if externe else ""))
        if b.get("filiere"):
            a = '<span class="only-%s">%s</span>' % (b["filiere"], a)
        lignes.append("  " + a)
    lignes.append("</div>")
    return "\n" + "\n".join(INDENT + l for l in lignes) + "\n" + INDENT


def cartes(langue, page, rac, durees, duree):
    lignes = ['<nav class="cartes-chapitres" aria-label="%s">' % html.escape(libelle(langue, "chapitres"))]
    for num, ico, fichier, titres in chapitres():
        chemin, lg = cible("chapitres/" + fichier, langue, rac)
        image = "assets/media/illustrations/chapitre-%s-carte.webp" % num
        if os.path.isfile(os.path.join(SITE, image)):
            visuel = '<span class="cch-image" aria-hidden="true"><img src="%s" alt="" loading="lazy"></span>' \
                     % lien(image, page)
        else:
            visuel = '<span class="cch-image absente" aria-hidden="true"><span class="cch-emoji">%s</span></span>' % ico
        numero = libelle(langue, "chapitre") % num
        if durees is not None and num in durees and duree is not None:
            numero += " · " + duree(durees[num], langue)
        titre = titres.get(langue) or titres.get(rac) or titres.get("fr", "")
        resume_ = resume(fichier, langue, rac)
        lignes.append('  <a class="carte-chapitre" href="%s"%s>' % (lien(chemin, page),
                                                                    ' hreflang="%s"' % lg if lg != langue else ""))
        lignes.append("    " + visuel)
        lignes.append('    <span class="cch-texte"><span class="cch-num">%s</span><span class="cch-titre">%s</span>%s'
                      '</span>' % (numero, texte(titre),
                                   '<span class="cch-resume">%s</span>' % texte(resume_) if resume_ else ""))
        lignes.append("  </a>")
    lignes.append("</nav>")
    return "\n" + "\n".join(INDENT + l for l in lignes) + "\n" + INDENT


def rendre(nom, langue, page, durees=None, duree=None):
    """Le contenu du fragment nom, dans la langue, pour la page page (chemin depuis la racine du site)."""
    rac = racine()
    if nom == "accueil-boutons":
        return boutons(langue, page, rac)
    if nom == "cartes-chapitres":
        return cartes(langue, page, rac, durees, duree)
    raise KeyError(nom)
