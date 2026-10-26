# -*- coding: utf-8 -*-
"""La page « 📘 Polycopié » du site (site/polycopie.html) : ce qu'en écrivent les fragments.

  livret-couverture  la vignette de la couverture (site/livret/couverture.<langue>.webp), ou une place réservée
  livret-fiche       le titre, le sous-titre, l'auteur, le bouton de téléchargement et le format (PDF, pages, poids,
                     langue) ; tant que le livret anglais n'est pas publié, la page anglaise propose le français
                     (hreflang="fr") ; sans livret publié, la fiche dit qu'il paraîtra ici
  livret-auteur      la présentation de l'auteur (outils/livret.py), mot pour mot

outils/generer_fragments.py les écrit d'après ce module ; outils/publier_polycopie.py publie le PDF, sa vignette et
site/livret/livret.json (pages, poids, dimensions de la vignette de chaque langue), que ce module lit : il reste léger
(ni PyMuPDF, ni python-docx), comme tout ce que lance le générateur des fragments.
"""
import html
import io
import json
import os
import re
import unicodedata

from .sources import SITE_LOCAL, Langue

FRAGMENT = re.compile(r"livret-(couverture|fiche|auteur)$")
DOSSIER = "livret"                      # jamais « polycopie/ » : Windows confondrait avec Polycopie/, l'espace de travail
INVENTAIRE = os.path.join(SITE_LOCAL, DOSSIER, "livret.json")

TEXTES = {
    "fr": dict(bouton="📘 Télécharger le polycopié", format="PDF · {pages} pages · {poids} · {langue}",
               langues={"fr": "en français", "en": "en anglais"}, alt="Couverture du polycopié{edition} : « {titre} »",
               edition=" (édition anglaise)", a_venir="Le polycopié paraîtra ici.", premiere="Première édition",
               fichier="Polycopie", poids=lambda o: ("%.1f Mo" % (o / 1048576)).replace(".", ",")),
    "en": dict(bouton="📘 Download the course book", format="PDF · {pages} pages · {poids} · {langue}",
               langues={"fr": "in French", "en": "in English"}, alt="Cover of the course book{edition}: “{titre}”",
               edition=" (French edition)", a_venir="The course book will appear here.", premiere="First edition",
               fichier="Course-book", poids=lambda o: "%.1f MB" % (o / 1048576)),
}


def esc(s):
    return html.escape(str(s), quote=True).replace("&#x27;", "'")


def nom_de_fichier(titre, lg="fr"):
    """Le nom proposé au téléchargement, dans la langue du livret : « Polycopie-Concevoir-un-cours-en-ligne.pdf »,
    « Course-book-Designing-an-online-course.pdf »."""
    s = unicodedata.normalize("NFD", titre or "livret")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return TEXTES[lg]["fichier"] + "-" + (re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-")[:60] or "livret") + ".pdf"


def fichiers(lg):
    """Les adresses publiées du livret d'une langue, depuis la racine du site : son PDF et sa vignette."""
    return {"pdf": f"{DOSSIER}/livret.{lg}.pdf", "vignette": f"{DOSSIER}/couverture.{lg}.webp"}


def inventaire():
    try:
        return json.load(io.open(INVENTAIRE, encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def publie(lg):
    """Le livret publié d'une langue (pages, octets, titre, taille de la vignette, adresses), ou None."""
    info = inventaire().get(lg)
    f = fichiers(lg)
    if not info or not all(os.path.isfile(os.path.join(SITE_LOCAL, *f[k].split("/"))) for k in f):
        return None
    return dict(info, code=lg, **f)


def _racine(rel):
    return "../" * rel.count("/")


def _propose(lg):
    """Le livret que propose une page de cette langue : le sien, sinon (page anglaise) le français."""
    return publie(lg) or (publie("fr") if lg == "en" else None)


def rendre(nom, langue, rel):
    """Le contenu d'un fragment de la page Polycopié, pour la page rel et la langue (fr ou en), ou None si nom n'en
    est pas un."""
    m = FRAGMENT.match(nom)
    if not m:
        return None
    sorte, t, racine = m.group(1), TEXTES[langue], _racine(rel)
    L = Langue(langue).L
    livret = _propose(langue)
    autre = livret is not None and livret["code"] != langue
    if sorte == "couverture":
        if not livret:
            return '<figure class="poly-couverture poly-a-venir"></figure>'
        largeur, hauteur = livret.get("taille", [480, 679])
        alt = t["alt"].format(edition=t["edition"] if autre else "", titre=livret.get("titre") or L["titre"])
        return (f'<figure class="poly-couverture"><img src="{racine}{livret["vignette"]}" width="{largeur}" '
                f'height="{hauteur}" alt="{esc(alt)}"></figure>')
    if sorte == "auteur":
        texte = re.sub(r"\s+", " ", str((Langue(langue).livret.get("presentation") or {}).get(langue, ""))).strip()
        return f"<p>{esc(texte)}</p>" if texte else ""
    # la fiche
    morceaux = [f'<p class="poly-titre">{esc(L["titre"])}</p>']
    if L["sous_titre"]:
        morceaux.append(f'<p class="poly-sous-titre">{esc(L["sous_titre"])}</p>')
    ligne = " · ".join(x for x in (L["auteur"], L["pied_couverture"], t["premiere"]) if x)
    morceaux.append(f'<p class="poly-auteur">{esc(ligne)}</p>')
    if not livret:
        morceaux.append(f'<p class="poly-format">{esc(t["a_venir"])}</p>')
        return "".join(morceaux)
    marque = ' hreflang="fr"' if autre else ""
    fmt = t["format"].format(pages=livret["pages"], poids=t["poids"](livret["octets"]),
                             langue=t["langues"][livret["code"]])
    fmt = " · ".join(esc(x).replace(" ", "&nbsp;") for x in fmt.split(" · "))
    titre_fichier = nom_de_fichier(livret.get("titre") or L["titre"], livret["code"])
    morceaux.append(f'<p class="poly-telecharger"><a class="btn btn-primary" href="{racine}{livret["pdf"]}" '
                    f'download="{esc(titre_fichier)}"{marque}>{esc(t["bouton"])}</a></p>')
    morceaux.append(f'<p class="poly-format">{fmt}</p>')
    return "".join(morceaux)
