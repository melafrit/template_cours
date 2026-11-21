#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fabrique un nouveau cours à partir de ce template.

    cp cours.exemple.json cours.json      # puis remplissez-le
    python3 nouveau_cours.py              # crée le cours dans le dossier « sortie »

    python3 nouveau_cours.py --essai      # dit ce qu'il ferait, sans rien écrire
    python3 nouveau_cours.py --config autre.json --sortie ../ailleurs
    python3 nouveau_cours.py --ecraser    # accepte un dossier de sortie non vide, dont il garde
                                          # les fichiers locaux (secrets, carnets, destination)

CE QUE FAIT CE SCRIPT — et ce qu'il ne fait pas.

Il met en place la MÉCANIQUE : l'arborescence, la charte, la navigation, les
squelettes de chapitres, les outils, la documentation. Il ne rédige AUCUN
contenu pédagogique. Le contenu s'écrit ensuite, avec la skill
« creer-cours-template », qui commence par lire vos documents de référence
déposés dans sources/ et vous pose ses questions de cadrage une à une.

Cette séparation est volontaire. Un script qui inventerait des chapitres
produirait un cours générique, et un cours générique ne sert personne.

LE CHAPITRE VITRINE EST CONSERVÉ, sous le nom `_modele.html`. Il n'apparaît
pas dans la navigation — l'underscore le signale — mais il reste consultable
et surtout copiable : c'est le seul endroit où l'on voit les sept composants
appelés pour de vrai, avec le motif bilingue à recopier.
"""

import argparse
import datetime
import fnmatch
import importlib.util
import io
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

RACINE = os.path.dirname(os.path.abspath(__file__))
CONFIG_DEFAUT = os.path.join(RACINE, "cours.json")

# La console Windows n'est pas en UTF-8 par défaut : sans cela, les accents des
# messages sortent en charabia. Sans effet sur macOS et Linux.
for flux in (sys.stdout, sys.stderr):
    try:
        flux.reconfigure(encoding="utf-8")
    except Exception:
        pass
MODELE = os.path.join(RACINE, "cours.exemple.json")

PALETTES = ("marine", "emeraude", "prune", "ardoise", "bordeaux")

# Ce qui est copié tel quel dans le nouveau cours. CLAUDE.md suit à part
# (contrat_du_cours) : ses passages propres au template en sont retirés.
COPIER = ["site", "outils", "prompts", "docs", ".claude", "deploiement", "tools",
          "demarrer.py", "demarrer.bat", "demarrer.command",
          ".gitattributes", ".gitignore", ".editorconfig",
          ".rgignore",      # cache les secrets aux recherches (Grep ignore le .gitignore, pas ce fichier)
          "LICENSE", "LICENSE-CONTENT.md"]

# Jamais recopié avec l'arborescence : secrets, carnets d'envoi, sorties
# régénérables, réglages locaux. Les deux secrets utiles à un nouveau cours
# suivent à part, octet pour octet et sans être ouverts (SECRETS_LOCAUX).
REGENERABLES = ("__pycache__", "*.pyc", "_tmp*", "out", "manifeste.json.tmp")
# Ce qui appartient au cours et que le template ne fournit jamais : --ecraser le laisse en place (garder_locaux).
LOCAUX = ("elevenlabs.json", "*.config.json", "config.json", "manifeste.json", "known_hosts", "destination.json",
          "quarantaine", "acces.json", "acces-zones.json", "Cahier_de_texte*.docx", "settings.local.json")
NE_PAS_COPIER = shutil.ignore_patterns(*(REGENERABLES + LOCAUX))

# Les secrets qui servent à tous les cours de l'auteur — la clé ElevenLabs et sa
# voix, les accès à l'hébergement — se recopient tels quels dans le nouveau
# cours, en local : jamais ouverts, jamais affichés, et seulement si le
# .gitignore du cours les exclut. La destination, elle, est propre à chaque
# cours : deploiement/destination.json, écrit d'après le bloc « publication ».
# (chemin, bloc qui le rend utile, motifs du .gitignore qui doivent l'exclure)
SECRETS_LOCAUX = [
    ("outils/elevenlabs.json", None, ("**/elevenlabs.json", "outils/elevenlabs.json")),
    ("deploiement/config.json", "deploiement", ("deploiement/config.json",)),
]

# Racines d'hébergement : un cours ne s'y publie jamais (voir deploiement/deployer.py).
RACINES_HEBERGEMENT = ("/", "/www", "/htdocs", "/public_html")

# Les passages du CLAUDE.md propres au template, retirés du contrat d'un cours créé.
BLOC_GABARIT = re.compile(r"\n?<!-- gabarit:debut -->.*?<!-- gabarit:fin -->\n?", re.S)

# Les passages des pages qui renvoient au polycopié complet, retirés d'un cours sans bloc « livret ».
BLOC_LIVRET = re.compile(r"<!-- livret:debut -->.*?<!-- livret:fin -->", re.S)

# Pages et dossiers retirés quand le bloc correspondant est à false.
BLOCS = {
    "qcm":                 ["site/QCM"],
    "glossaire":           ["site/glossaire.html", "site/assets/js/glossaire-data.js",
                            "site/assets/js/glossaire-tooltip.js", "site/assets/js/glossaire-emplois.js",
                            "outils/glossaire_emplois.py"],
    "flashcards":          ["site/assets/js/flashcards.js", "site/assets/js/flashcards-data.js"],
    "activites":           ["site/activites.html"],
    "polycopies":          ["site/polycopies.html", "site/assets/polycopies", "tools/generate_polycopies.py"],
    "atelier":             ["site/atelier", "site/atelier.html"],
    "documents_formateur": ["docs/generate_cahier_de_texte.py",
                            "docs/generate_questions_oral.py"],
    "deploiement":         ["deploiement"],
    "podcasts":            ["site/podcasts.html", "site/assets/js/podcasts.js", "outils/podcasts.py",
                            "outils/generer_podcasts.py"],
    "livret":              ["site/polycopie.html", "site/livret", "outils/generer_polycopie.py",
                            "outils/publier_polycopie.py", "outils/polycopie", "outils/livret.py"],
}

# Un bloc absent de cours.json est actif, sauf ceux-ci : la série de podcasts (module 03) et le polycopié (module
# 02) ne s'ajoutent que demandés, sans quoi un cours créé avec un ancien cours.json gagnerait une page vide dans son
# menu.
BLOCS_INACTIFS_PAR_DEFAUT = {"podcasts", "livret"}


def bloc_actif(c, cle):
    """Vrai si le bloc cle est actif pour le cours c (cours.json, « blocs »)."""
    return bool((c.get("blocs") or {}).get(cle, cle not in BLOCS_INACTIFS_PAR_DEFAUT))


# Le générateur ne fabrique que des cours en site miroir (décision de l'auteur du 21 novembre 2026). Chaque page
# naît dans la langue racine du cours, la première de « langues » ; les autres langues viennent ensuite, page par
# page, en jumelles (outils/creer_jumelle.py), une fois la racine stable. La démonstration a ses pages françaises à
# la racine et leurs jumelles anglaises sous en/ : un cours anglais part de celles-ci.
RACINES = ("fr", "en")
DOSSIERS_LANGUE = ("en", "ar")      # les jumelles de la démonstration : jamais recopiées dans un cours


def racine(c):
    """La langue racine du cours : la première de « langues »."""
    return (c.get("langues") or ["fr"])[0]


def texte(d, lg):
    """Le texte de d ({fr, en, …}) dans la langue lg, à défaut en français."""
    d = d or {}
    return str(d.get(lg) or d.get("fr") or "")


def att(s):
    """Un texte utilisable dans un attribut HTML."""
    return str(s).replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


def h(s):
    """Un texte utilisable dans le corps d'une page."""
    return str(s).replace("&", "&amp;").replace("<", "&lt;")


# L'encadré « Le podcast du chapitre » du chapitre vitrine : il mène à l'épisode de la démonstration, qu'un cours créé
# n'a pas. Le modèle et les squelettes gardent, à sa place, un repère si le cours a une série.
ENCADRE_PODCAST = re.compile(r"[ \t]*<!-- L'encadré « Le podcast du chapitre »[^\n]*-->\n"
                             r"[ \t]*<!-- FRAGMENT:podcast-\d+ -->.*?<!-- /FRAGMENT:podcast-\d+ -->\n", re.S)
REPERE_PODCAST = ("      <!-- Ici, l'encadré « Le podcast du chapitre », si un épisode de la série accompagne ce "
                  "chapitre : prompts/modules/03-podcasts-notebooklm.md (fragment podcast-N). -->\n")


# Contenu de DEMONSTRATION, retire de tout cours cree — sauf --avec-demo.
# Le squelette de chapitre etait deja vide ; ces fichiers-la ne l'etaient pas.
# Pages propres au TEMPLATE, retirees de tout cours cree : elles parlent du
# template lui-meme, pas de la matiere enseignee.
DEMO_FICHIERS = [
    "site/about.html",
]

DEMO_DOSSIERS = [
    "site/assets/media/voix",
    "site/assets/media/schemas",
    "site/assets/media/podcasts",
    "site/assets/media/infographies",
    "site/assets/media/slides",
    "site/assets/polycopies",
    "site/livret",
]

SQUELETTE_QCM_QUESTIONS = """/* =================================================================
   questions.js — Banque de questions BILINGUE (FR/EN)
   FICHIER À REMPLIR. Deux exemples montrent la forme attendue.

   Règles à tenir : une question porte sur ce que le chapitre enseigne
   REELLEMENT ; les positions des bonnes reponses sont equilibrees ; les
   distracteurs sont plausibles. Voir corrections.js pour la cle.
   ================================================================= */
window.QCM_QUESTIONS = {
  meta: {
    titre: { fr: 'QCM — %(titre_fr)s', en: 'Quiz — %(titre_en)s' },
    formation: { fr: '%(titre_fr)s', en: '%(titre_en)s' },
    annee_academique: '',
    auteur: '%(auteur)s',
    nombre_questions: 2,
    note_sur: 20
  },
  questions: [
    {
      id: 'Q01', chapitre: 1, difficulte: 'vert',
      enonce: { fr: 'Premiere question ?', en: 'First question?' },
      propositions: [
        { fr: 'Proposition A', en: 'Option A' },
        { fr: 'Proposition B', en: 'Option B' },
        { fr: 'Proposition C', en: 'Option C' },
        { fr: 'Proposition D', en: 'Option D' }
      ]
    },
    {
      id: 'Q02', chapitre: 1, difficulte: 'jaune',
      enonce: { fr: 'Deuxieme question ?', en: 'Second question?' },
      propositions: [
        { fr: 'Proposition A', en: 'Option A' },
        { fr: 'Proposition B', en: 'Option B' },
        { fr: 'Proposition C', en: 'Option C' },
        { fr: 'Proposition D', en: 'Option D' }
      ]
    }
  ]
};
"""

SQUELETTE_QCM_CORRECTIONS = """/* =================================================================
   corrections.js — Cle de correction BILINGUE (FR/EN)
   FICHIER À REMPLIR. Les identifiants doivent CORRESPONDRE a questions.js.

   L'explication est la partie utile : dire pourquoi les autres propositions
   etaient credibles, et ou le raisonnement derape.
   ================================================================= */
window.QCM_CORRECTIONS = {
  corrections: [
    {
      id: 'Q01', chapitre: 1, difficulte: 'vert', bonne_reponse_index: 0,
      explication: {
        fr: 'Pourquoi A est juste, et pourquoi les autres ne le sont pas.',
        en: 'Why A is right, and why the others are not.'
      }
    },
    {
      id: 'Q02', chapitre: 1, difficulte: 'jaune', bonne_reponse_index: 1,
      explication: {
        fr: 'L explication de la deuxieme question.',
        en: 'The explanation for the second question.'
      }
    }
  ]
};
"""

SQUELETTE_FLASHCARDS = """/* =================================================================
   flashcards-data.js — Cartes de revision, par chapitre
   FICHIER À REMPLIR. Une carte pose une question, pas une definition :
   « Qu'est-ce qui distingue X de Y ? » se revise ; « X : definition »
   se relit sans rien apprendre.
   ================================================================= */
window.RDC_FLASHCARDS = {
  "1": [
    { front: { fr: 'Question de revision ?', en: 'Revision question?' },
      back:  { fr: 'La reponse, en une phrase.', en: 'The answer, in one sentence.' },
      ref:   'Chapitre 1' }
  ]
};
"""

SQUELETTE_GLOSSAIRE = """/* =================================================================
   glossaire-data.js — Glossaire BILINGUE
   FICHIER À REMPLIR. GLOSSARY_CURATED liste les termes rendus interactifs
   dans les chapitres : au-dela d'une quinzaine, la page se couvre de
   pointilles et plus personne ne clique.
   ================================================================= */
window.GLOSSARY = [
  { fr: "terme a definir", en: "term to define",
    def: { fr: "La definition, en une ou deux phrases.",
           en: "The definition, in one or two sentences." },
    ex:  { fr: "Un exemple concret.", en: "A concrete example." } }
];

window.GLOSSARY_CURATED = ["terme a definir"];

window.GLOSSARY_ALIASES = {};
"""

SQUELETTE_PLAYLIST = """/* =================================================================
   playlist-data.js — index des pistes audio
   FICHIER GENERE — ne pas modifier a la main :
       python3 outils/generer_playlist.py
   ================================================================= */
window.RDC_PLAYLIST = {};
"""

SQUELETTE_POLYCOPIES = {
    "1": {
        "title": {"fr": "Titre du chapitre", "en": "Chapter title"},
        "subtitle": {"fr": "Polycopie de synthese", "en": "Summary handout"},
        "blocks": [
            ["p", {"fr": "Introduction du polycopie, a rediger.",
                   "en": "Handout introduction, to be written."}],
            ["h2", {"fr": "1. Premiere partie", "en": "1. First part"}],
            ["p", {"fr": "Le contenu de la premiere partie. Le gras s ecrit avec "
                         "des **asterisques**.",
                   "en": "The content of the first part. Bold uses **asterisks**."}],
            ["takeaways", [{"fr": "Ce qu il faut retenir.",
                            "en": "What to remember."}]],
        ],
    }
}


def renommer_identite(sortie, c):
    """Substitue l'identite du cours creee a celle de la demonstration.

    Titre de l'onglet, meta-description, auteur des metadonnees, badge et pied
    de page : rien de tout cela n'est dans le corps du texte, donc rien de tout
    cela n'etait purge. Un cours de cybersecurite s'annoncait « Concevoir un
    cours en ligne » dans la barre d'onglets du navigateur.
    """
    lg = racine(c)
    tfr = c["titre"]["fr"]
    ten = c["titre"].get("en") or tfr
    titre = texte(c["titre"], lg)
    st = texte(c.get("sous_titre"), lg)
    auteur = c["auteur"]

    # Le nom court de l'en-tête et son pictogramme : « Concevoir un cours » et
    # « Ce » restaient en tête de chaque page d'un cours créé. Par défaut, la
    # partie du titre qui précède le deux-points, et ses deux premières lettres.
    court = str((c.get("titre_court") or {}).get(lg) or re.split(r"\s?:\s", titre)[0]).strip()
    logo = str(c.get("logo") or re.sub(r"[\W_]", "", court)[:2] or "Co")
    licence = texte(c.get("licence"), lg).strip()
    picto = ('<span class="logo-icon">C<span class="acc">e</span></span>',
             '<span class="logo-icon">%s<span class="acc">%s</span></span>' % (h(logo[:1]), h(logo[1:2])))

    # Les variantes longues d'abord : « ... efficace » contient « ... » tout court.
    paires = [
        ("Concevoir un cours en ligne efficace", tfr),
        ("Designing an effective online course", ten),
        ("Concevoir un cours en ligne", tfr),
        ("Designing an online course", ten),
        ("Cours-démo", "Cours"),
        ("cours-démo", "cours"),
        ("Demo course", "Course"),
        ("demo course", "course"),
        ("Mohamed EL AFRIT", auteur),
    ]

    desc = ("%s. %s" % (titre, st)).strip().strip(".") + "."
    touchees = 0
    for f in sorted(glob.glob(os.path.join(sortie, "site", "**", "*.html"),
                              recursive=True)):
        s = io.open(f, encoding="utf-8").read()
        avant = s

        # La meta-description des chapitres est deja reecrite par le squelette ;
        # celle des autres pages parlait encore de la demonstration.
        if os.sep + "chapitres" + os.sep not in f:
            s = re.sub(r'<meta name="description" content="[^"]*">',
                       lambda m: '<meta name="description" content="%s">' % att(desc), s)
        s = re.sub(r'<meta name="author" content="[^"]*">',
                   lambda m: '<meta name="author" content="%s">' % att(auteur), s)

        # Le sous-titre de l'accueil s'écrit dans son bandeau (accueil_squelette). Les autres pages gardent le leur :
        # les squelettes, les pages vidées et le glossaire reçoivent le leur (squelette_chapitre, purger_demo).

        # L'en-tête : nom court et pictogramme du cours, à la place de ceux de la démonstration, dans sa langue.
        s = re.sub(r'(class="site-logo">.*?)<span>(?:Concevoir un cours|Design a course)</span>',
                   lambda m: '%s<span>%s</span>' % (m.group(1), h(court)), s, count=1, flags=re.S)
        s = s.replace(*picto)

        # Le pied de page : la licence de cours.json, pas celle de la démonstration.
        if licence:
            s = re.sub(r'<span class="cc-badges">[^<]*</span>',
                       lambda m: '<span class="cc-badges">%s</span>' % h(licence), s)
            s = re.sub(r'\s*<span> (?:Code sous licence MIT, contenu sous licence Creative Commons BY 4\.0\.'
                       r'|Code under MIT license, content under Creative Commons BY 4\.0\.)</span>', "", s)

        for a, b in paires:
            s = s.replace(a, b)

        if s != avant:
            ecrire(f, s)
            touchees += 1
    return touchees


def fin_div(t, debut):
    """L'indice qui suit la balise </div> refermant la <div> ouverte à `debut`, ou -1."""
    prof = 0
    for m in re.finditer(r"<div\b|</div>", t[debut:]):
        prof += 1 if m.group(0) != "</div>" else -1
        if prof == 0:
            return debut + m.end()
    return -1


PAGE_A_REDIGER = """    <div class="callout warning">
      <div class="callout-icon">✏️</div>
      <div class="callout-content">
        <h4>%s</h4>
        <p>%s</p>
      </div>
    </div>"""
TITRE_A_REDIGER = {"fr": "Page à rédiger", "en": "Page to be written"}

# Les pages de démonstration vidées : (fichier, titre, consigne), dans chaque langue racine possible.
PAGES_DEMO = [
    ("site/atelier.html", {"fr": "Atelier fil rouge", "en": "Capstone workshop"},
     {"fr": "L'énoncé de l'atelier fil rouge, ses livrables et ses modèles téléchargeables "
            "(prompts/11_atelier_templates.md). Le contenu de démonstration a été retiré ; "
            "l'atelier complet reste consultable dans le template (site/atelier.html).",
      "en": "The capstone workshop brief, its deliverables and downloadable templates "
            "(prompts/11_atelier_templates.md). The demo content has been removed; the full "
            "workshop remains in the template (site/atelier.html)."}),
    ("site/activites.html", {"fr": "Activités interactives", "en": "Interactive activities"},
     {"fr": "Les activités du cours (prompts/05_activites_interactives.md), construites avec les "
            "patrons de assets/js/tools.js. Les exemples de démonstration ont été retirés ; ils "
            "restent dans le template (site/activites.html).",
      "en": "The course activities (prompts/05_activites_interactives.md), built with the patterns "
            "of assets/js/tools.js. The demo examples have been removed; they remain in the "
            "template (site/activites.html)."}),
]

# L'accueil d'un cours créé (lot 3, 21 novembre 2026) : la structure de l'accueil de la démonstration, validé par
# l'auteur, et des consignes « À rédiger » à la place de sa prose. Les chiffres, les boutons et les cartes des chapitres
# viennent des fragments (referentiel.py, outils/accueil.py, course-data.js) ; « Ce que démontre ce site », propre à la
# démonstration, n'y est pas. Une section ajoutée à l'accueil de la démonstration s'ajoute ici aussi.
ACCUEIL = {
    "fr": {
        "aller": "Aller au contenu", "sommaire": "Sommaire", "voix": "Capsules d'accueil",
        "pastille": "À rédiger : diplôme, bloc et module",
        "cartes": [("Durée", "<!-- FRAGMENT:duree-totale -->…<!-- /FRAGMENT:duree-totale -->",
                    "La lecture des <!-- FRAGMENT:nb-chapitres-lettres -->…<!-- /FRAGMENT:nb-chapitres-lettres -->"
                    " chapitres"),
                   ("Épreuve préparée", "À rédiger", "Les compétences et les critères visés"),
                   ("Ce que vous produisez", "À rédiger", "Les livrables, et où les déposer"),
                   ("Fil rouge", "À rédiger", "Le cas qui traverse tout le cours")],
        "sections": [("parcours", "Le parcours",
                      "À rédiger : une phrase qui présente l'enchaînement des chapitres."),
                     ("fil-rouge", "Le fil rouge",
                      "À rédiger : le cas, le projet ou le scénario qui traverse tout le cours."),
                     ("livrables", "Ce que vous produisez",
                      "À rédiger : les livrables du cours, leurs échéances et où les déposer."),
                     ("evaluation", "L'évaluation",
                      "À rédiger : comment l'apprenant est évalué (épreuve, QCM, critères).")],
        "conseils": ("avant-de-commencer", "Avant de commencer",
                     "À rédiger : trois ou quatre conseils pour bien commencer le cours."),
        "exemple": "<strong>En %s</strong>, à rédiger : l'exemple propre à cette filière.",
        "polycopie": ("Le polycopié", "Tout le cours en un seul livret, à lire hors ligne ; ses QR codes vous "
                                      "ramènent au bon endroit du site."),
        "podcasts": ("Les podcasts", "Des épisodes pour découvrir un chapitre avant de le lire, ou le réviser loin "
                                     "de l'écran."),
        "flottant": "Chapitre 1", "bienvenue": "Bienvenue dans le cours", "filiere": "En %s",
        "pied": "Cours « %s » · Auteur : ",
    },
    "en": {
        "aller": "Skip to content", "sommaire": "Contents", "voix": "Welcome audio",
        "pastille": "To be written: degree, block and module",
        "cartes": [("Duration", "<!-- FRAGMENT:duree-totale -->…<!-- /FRAGMENT:duree-totale -->",
                    "Reading time for the <!-- FRAGMENT:nb-chapitres-lettres -->…<!-- /FRAGMENT:nb-chapitres-lettres -->"
                    " chapters"),
                   ("Assessment prepared", "To be written", "The competences and criteria covered"),
                   ("What you produce", "To be written", "The deliverables, and where to submit them"),
                   ("Through-line", "To be written", "The case that runs across the whole course")],
        "sections": [("parcours", "The path", "To be written: one sentence presenting how the chapters follow on."),
                     ("fil-rouge", "The through-line",
                      "To be written: the case, project or scenario that runs across the whole course."),
                     ("livrables", "What you produce",
                      "To be written: the course deliverables, their deadlines and where to submit them."),
                     ("evaluation", "Assessment",
                      "To be written: how the learner is assessed (exam, quiz, criteria).")],
        "conseils": ("avant-de-commencer", "Before you start",
                     "To be written: three or four tips to start the course well."),
        "exemple": "<strong>In %s</strong>, to be written: the example specific to this program.",
        "polycopie": ("The course book", "The whole course in a single book, to read offline; its QR codes take you "
                                         "back to the right spot on the website."),
        "podcasts": ("The podcasts", "Episodes to discover a chapter before reading it, or to revise it away from "
                                     "the screen."),
        "flottant": "Chapter 1", "bienvenue": "Welcome to the course", "filiere": "In %s",
        "pied": "Course \"%s\" · Author: ",
    },
}

SOUS_TITRE_PAGE = {"fr": "À rédiger : une phrase qui présente cette page.",
                   "en": "To be written: one sentence introducing this page."}
SOUS_TITRE_CHAPITRE = {"fr": "À rédiger : une ou deux phrases qui disent ce que ce chapitre permet de faire.",
                       "en": "To be written: one or two sentences saying what this chapter enables."}
SOUS_TITRE_GLOSSAIRE = {"fr": "Les termes clés du cours, avec leur équivalent dans l'autre langue, une définition et un "
                              "exemple. Tapez un mot pour filtrer la liste.",
                        "en": "The key terms of the course, with their equivalent in the other language, a definition "
                              "and an example. Type a word to filter the list."}
# Le sous-titre du sommaire racontait la démonstration (« vous saurez concevoir un cours en ligne ») : il garde le
# nombre de chapitres, un fragment que generer_fragments.py écrit, et demande le reste.
SOUS_TITRE_SOMMAIRE = {
    "fr": "Le parcours se compose de <!-- FRAGMENT:nb-chapitres-lettres -->…<!-- /FRAGMENT:nb-chapitres-lettres --> "
          "chapitres. À rédiger : ce que l'apprenant saura faire à la fin du cours.",
    "en": "The path is made of <!-- FRAGMENT:nb-chapitres-lettres -->…<!-- /FRAGMENT:nb-chapitres-lettres --> "
          "chapters. To be written: what the learner will be able to do by the end of the course.",
}


def sous_titre(t, texte_html):
    """Le sous-titre de l'en-tête d'une page (<p class="chapter-subtitle">), remplacé par texte_html."""
    return re.sub(r'(<p class="chapter-subtitle">).*?(</p>)',
                  lambda m: '%s\n        <span>%s</span>\n      %s' % (m.group(1), texte_html, m.group(2)),
                  t, count=1, flags=re.S)


def vider_page(chemin, titre, consigne, lg):
    """Garde l'en-tête d'une page de démonstration, remplace son contenu par un repère.

    L'atelier racontait « Concevez votre propre cours en ligne » et les activités
    demandaient « quel format d'évaluation ? » dans un cours de cybersécurité :
    aucune n'était vidée, et rien ne le signalait.
    """
    s = io.open(chemin, encoding="utf-8").read()
    m = re.search(r'<div class="chapter-header">', s)
    fin = fin_div(s, m.start()) if m else -1
    fm = s.find("</main>", fin) if fin > 0 else -1
    if fm < 0:
        return False
    s = s[:fin] + "\n\n" + PAGE_A_REDIGER % (TITRE_A_REDIGER[lg], h(consigne)) + "\n\n  " + s[fm:]
    s = re.sub(r'(<h1 class="chapter-title">).*?(</h1>)',
               lambda x: '%s<span>%s</span>%s' % (x.group(1), h(titre), x.group(2)), s, count=1, flags=re.S)
    s = sous_titre(s, SOUS_TITRE_PAGE[lg])
    # les appels de démonstration ne trouveraient plus leurs conteneurs
    s = re.sub(r'<script>\s*TPLActivities\..*?</script>\s*', "", s, flags=re.S)
    ecrire(chemin, s)
    return True


# Les libellés de la navigation d'un chapitre, dans chaque langue racine possible.
NAV = {
    "sommaire": {"fr": "← Sommaire", "en": "← Contents"},
    "precedent": {"fr": "← Précédent", "en": "← Previous"},
    "suivant": {"fr": "Suivant →", "en": "Next →"},
    "accueil": {"fr": "← Accueil", "en": "← Home"},
    "qcm": {"fr": "QCM d'évaluation", "en": "Assessment quiz"},
    "cours": {"fr": "Sommaire du cours", "en": "Course contents"},
}


def typo_fr(t):
    """L'espace insécable du français, sur un balisage sans script : avant : ; ? ! et dans « »."""
    t = re.sub(r" ([:;?!])", "\u00a0\\1", t)
    return t.replace("« ", "«\u00a0").replace(" »", "\u00a0»")


def accueil_squelette(c, demo):
    """L'accueil d'un cours créé, dans sa langue racine : la structure de celui de la démonstration (demo, son texte,
    dont il reprend le script de tête de la filière), sa prose remplacée par des consignes."""
    lg = racine(c)
    A = ACCUEIL[lg]
    titre, st = texte(c["titre"], lg), texte(c.get("sous_titre"), lg)
    filieres = c.get("filieres") or []
    multi = len(filieres) > 1
    tete = re.search(r"<script>/\* La filière mémorisée.*?</script>", demo, re.S)
    premier = c["chapitres"][0]["fichier"]

    cartes = "\n".join('        <div class="info-card"><div class="label">%s</div><div class="value">%s</div>'
                       '<div class="meta">%s</div></div>' % carte for carte in A["cartes"])
    voix = ['    <div id="voix-bienvenue"></div>']
    capsules = [("voix-bienvenue", "accueil-capsule-%s.mp3" % lg, A["bienvenue"])]
    for f in (filieres if multi else []):
        voix.append('    <div class="voix-filiere only-%s"><div id="voix-bienvenue-%s"></div></div>' % (f["id"], f["id"]))
        capsules.append(("voix-bienvenue-%s" % f["id"], "accueil-capsule-%s-%s.mp3" % (f["id"], lg),
                         A["filiere"] % f["code"]))

    sections = []
    for n, (ident, nom, consigne) in enumerate(A["sections"], 1):
        bloc = ['  <section class="landing-section" id="%s" aria-labelledby="titre-%s">' % (ident, ident),
                '    <div class="section-title"><span class="num">%02d</span><h2 id="titre-%s">%s</h2>'
                '<span class="line" aria-hidden="true"></span></div>' % (n, ident, h(nom)),
                '    <div class="section-voix" id="voix-section-%d"></div>' % n,
                '    <p class="lead">%s</p>' % h(consigne)]
        if ident == "parcours":
            bloc.append("    <!-- FRAGMENT:cartes-chapitres --><!-- /FRAGMENT:cartes-chapitres -->")
        if ident == "fil-rouge" and multi:
            bloc += ['    <div class="exemple-filiere only-%s"><p>%s</p></div>' % (f["id"], A["exemple"] % h(f["code"]))
                     for f in filieres]
        bloc.append("  </section>")
        sections.append("\n".join(bloc))
        capsules.append(("voix-section-%d" % n, "accueil-section-%d-capsule-%s.mp3" % (n, lg), nom))

    n = len(A["sections"]) + 1
    ident, nom, consigne = A["conseils"]
    supports = []
    for cle, page, ico in (("livret", "polycopie.html", "📘"), ("podcasts", "podcasts.html", "🎙️")):
        if bloc_actif(c, cle):
            nom_s, texte_s = A["polycopie" if cle == "livret" else "podcasts"]
            supports.append('        <a class="support-carte" href="%s"><span class="support-ico" aria-hidden="true">%s'
                            '</span><span><strong>%s</strong><span class="support-texte">%s</span></span></a>'
                            % (page, ico, h(nom_s), h(texte_s)))
    conseils = ['  <section class="conseils" id="%s" aria-labelledby="titre-%s">' % (ident, ident),
                '    <div class="landing-section conseils-inner">',
                '      <div class="section-title"><span class="num">%02d</span><h2 id="titre-%s">%s</h2>'
                '<span class="line" aria-hidden="true"></span></div>' % (n, ident, h(nom)),
                '      <div class="section-voix" id="voix-section-%d"></div>' % n,
                '      <p class="lead">%s</p>' % h(consigne)]
    if supports:
        conseils += ['      <div class="accueil-supports">'] + supports + ['      </div>']
    conseils += ["    </div>", "  </section>"]
    capsules.append(("voix-section-%d" % n, "accueil-section-%d-capsule-%s.mp3" % (n, lg), nom))

    corps = """<body class="page-accueil">
<a class="skip-link" href="#contenu">%(aller)s</a>

<header class="site-header">
  <div class="header-left">
    <button class="sidebar-toggle" aria-label="Menu">☰</button>
    <a href="index.html" class="site-logo"><span class="logo-icon">C<span class="acc">e</span></span>
      <span>%(court_demo)s</span></a>
  </div>
  <div class="header-right">
    <a href="cours.html" class="chapter-nav-btn"><span aria-hidden="true">🗂️</span> <span>%(sommaire)s</span></a>
    <button class="theme-toggle" aria-label="Thème">🌙</button>
  </div>
</header>

<aside class="sidebar">
  <div class="sidebar-progress"><div class="sidebar-progress-bar"></div></div>
  <div class="sidebar-content"><ul class="nav-tree" id="nav-tree"></ul></div>
</aside>

<main id="contenu" class="accueil">

  <!-- Le bandeau. Pour colorer un mot du titre, entourez-le de <em>. Les boutons viennent de outils/accueil.py,
       les chiffres du référentiel (outils/referentiel.py). -->
  <section class="landing-header" id="presentation" aria-labelledby="titre-accueil">
    <div class="landing-inner">
      <p class="eyebrow"><span class="dot" aria-hidden="true"></span><span>%(pastille)s</span></p>
      <h1 id="titre-accueil">%(titre)s</h1>
      <p class="subtitle">%(st)s</p>
      <!-- FRAGMENT:accueil-boutons --><!-- /FRAGMENT:accueil-boutons -->
      <div class="info-grid">
%(cartes)s
      </div>
    </div>
  </section>

  <section class="landing-section accueil-voix" id="bienvenue" aria-label="%(voix)s">
%(voix_html)s
  </section>

%(sections)s

%(conseils)s

</main>

<footer class="site-footer">
  <p><span>%(pied)s</span><a href="#">%(auteur)s</a></p>
  <p class="license"><span class="cc-badges">%(licence)s</span></p>
</footer>

<a class="fab-cours" data-chapitre="1" href="chapitres/%(premier)s"><span aria-hidden="true">🚀</span> <span>%(flottant)s</span> <span aria-hidden="true">→</span></a>
""" % {"aller": A["aller"], "sommaire": A["sommaire"], "voix": A["voix"], "pastille": h(A["pastille"]),
           "court_demo": "Concevoir un cours" if lg == "fr" else "Design a course", "titre": h(titre), "st": h(st),
           "cartes": cartes, "voix_html": "\n".join(voix), "sections": "\n\n".join(sections),
           "conseils": "\n".join(conseils), "pied": A["pied"] % h(titre), "auteur": h(c["auteur"]),
           "licence": h(texte(c.get("licence"), lg).strip() or "MIT · CC BY 4.0"), "premier": premier,
           "flottant": A["flottant"]}
    if lg == "fr":
        corps = typo_fr(corps)

    tete_html = """<!DOCTYPE html>
<html lang="%(lg)s" data-lang="%(lg)s" data-langues="%(lg)s" data-accent="%(palette)s">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="icon" href="favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<title>%(titre)s</title>
<meta name="description" content="%(titre)s">
<meta name="author" content="%(auteur)s">
%(tete)s
<link rel="stylesheet" href="assets/css/fonts.css">
<link rel="stylesheet" href="assets/css/main.css">
<link rel="stylesheet" href="assets/css/palettes.css">
<link rel="stylesheet" href="assets/css/components.css">
<link rel="stylesheet" href="assets/css/interactions.css">
<link rel="stylesheet" href="assets/css/filieres.css">
</head>

""" % {"lg": lg, "palette": c["palette"], "titre": h(titre), "auteur": att(c["auteur"]),
       "tete": tete.group(0) if tete else ""}

    liste = ",\n".join("    { id: '%s', src: V + '%s', titre: %s }" % (i, nom, json.dumps(t, ensure_ascii=False))
                       for i, nom, t in capsules)
    scripts = """
<script src="assets/js/i18n.js"></script>
<script src="assets/js/ui-labels.js"></script>
<script src="assets/js/course-data.js"></script>
<script src="assets/js/nav-sections.js"></script>
<script src="assets/js/navigation.js"></script>
<script src="assets/js/accessibility.js"></script>
<script src="assets/js/media-data.js"></script>
<script src="assets/js/media.js"></script>
<script src="assets/js/animations.js"></script>
<script src="assets/js/interactions.js"></script>
<script src="assets/js/playlist-data.js"></script>
<script src="assets/js/playlist.js"></script>
<script>
/* Les capsules de l'accueil : celle d'accueil, celle de chaque filière, puis une en tête de chaque section. Chaque
   piste se dépose sous ce nom dans assets/media/voix/ ; tant qu'elle manque, le lecteur l'annonce « bientôt
   disponible ». Les textes : la fiche des capsules de l'accueil (prompts/14_capsules_audio.md). */
(function () {
  'use strict';
  var V = 'assets/media/voix/';
  var CAPSULES = [
%s
  ];
  function monter() {
    CAPSULES.forEach(function (c) {
      var el = document.getElementById(c.id);
      if (!el) return;
      el.innerHTML = '';
      RDCX.voice(c.id, { src: c.src, titre: c.titre, duree: c.duree || '', transcription: c.transcription || '' });
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', monter);
  else monter();
})();
</script>
</body>
</html>
""" % liste
    return tete_html + corps + scripts


# Les boutons de l'accueil de la démonstration (le dépôt sur Livrables, son QCM) ne valent pas pour un cours créé : il
# n'a que « Commencer le chapitre 1 » tant que son auteur n'en déclare pas (le bloc école les écrira, lot 2).
BOUTONS_VIDES = ("# À remplir : le dépôt sur Livrables, les épreuves de chaque filière… (le bloc école les écrira).\n"
                 "# Tant que la liste est vide, le bandeau n'a que « Commencer le chapitre 1 ».\n"
                 "BOUTONS = []\n")


def vider_boutons_accueil(sortie):
    """BOUTONS = [] dans outils/accueil.py du cours ; vrai si le fichier a changé."""
    p = os.path.join(sortie, "outils", "accueil.py")
    if not os.path.isfile(p):
        return False
    t = io.open(p, encoding="utf-8").read()
    neuf = re.sub(r"^BOUTONS = \[\n.*?^\]\n", lambda m: BOUTONS_VIDES, t, count=1, flags=re.S | re.M)
    if neuf != t:
        ecrire(p, neuf)
    return neuf != t


def recoudre_liens(sortie, c):
    """Fait pointer tous les liens de chapitre vers les chapitres DECLARES.

    Sans cela, l'accueil, le sommaire, l'atelier et la pagination des squelettes
    menaient encore aux chapitres de la demonstration : des liens morts sur les
    pages les plus visitees.
    """
    lg = racine(c)
    chaps = c["chapitres"]
    premier = chaps[0]["fichier"]
    recousus = 0

    # --- repli statique des boutons « commencer »
    for rel in ("site/index.html", "site/cours.html", "site/atelier.html"):
        p = os.path.join(sortie, rel.replace("/", os.sep))
        if not os.path.isfile(p):
            continue
        s = io.open(p, encoding="utf-8").read()
        neuf = re.sub(r'(data-chapitre="1" href=")chapitres/\d\d-[a-z0-9-]+\.html"',
                      r'\1chapitres/%s"' % premier, s)
        if neuf != s:
            ecrire(p, neuf)
            recousus += 1

    # --- navigation des squelettes : réécrite d'après l'ordre déclaré. Les deux blocs
    #     (boutons de l'en-tête, pagination du pied) sont refaits en entier : recousus
    #     par motifs, ils gardaient les libellés du chapitre vitrine (« ← Accueil »,
    #     « Structurer le contenu ») et, faute de « \g<1> », un nom de fichier qui
    #     commence par un chiffre devenait un caractère octal : « \101-… » donnait
    #     « A-… », et le lien disparaissait sans qu'aucun vérificateur ne le voie.
    qcm = os.path.isfile(os.path.join(sortie, "site", "QCM", "index.html"))

    def un(cle):
        return h(NAV[cle][lg])

    def titre(ch):
        return h(texte(ch["titre"], lg))

    for i, ch in enumerate(chaps):
        p = os.path.join(sortie, "site", "chapitres", ch["fichier"])
        if not os.path.isfile(p):
            continue
        s = io.open(p, encoding="utf-8").read()
        avant = chaps[i - 1] if i > 0 else None
        apres = chaps[i + 1] if i + 1 < len(chaps) else None
        prec = avant["fichier"] if avant else "../index.html"
        if apres:
            suiv, titre_suiv = apres["fichier"], titre(apres)
        elif qcm:
            suiv, titre_suiv = "../QCM/index.html", un("qcm")
        else:
            suiv, titre_suiv = "../cours.html", un("cours")
        entete = ('<nav class="chapter-nav">\n'
                  '      <a href="../cours.html" class="chapter-nav-btn">%s</a>\n' % un("sommaire")
                  + ('      <a href="%s" class="chapter-nav-btn">%s</a>\n' % (prec, un("precedent"))
                     if avant else "")
                  + '      <a href="%s" class="chapter-nav-btn">%s</a>\n    </nav>' % (suiv, un("suivant")))
        pied = ('<nav class="chapter-pagination">\n'
                '      <a href="%s" class="pagination-link prev">\n'
                '        <span class="pagination-label">%s</span>\n' % (
                    prec, un("precedent") if avant else un("accueil"))
                + ('        <span class="pagination-title">%s</span>\n' % titre(avant) if avant else "")
                + '      </a>\n'
                  '      <a href="%s" class="pagination-link next">\n'
                  '        <span class="pagination-label">%s</span>\n'
                  '        <span class="pagination-title">%s</span>\n'
                  '      </a>\n    </nav>' % (suiv, un("suivant"), titre_suiv))
        s = re.sub(r'<nav class="chapter-nav">.*?</nav>', lambda m: entete, s, count=1, flags=re.S)
        s = re.sub(r'<nav class="chapter-pagination">.*?</nav>', lambda m: pied, s, count=1, flags=re.S)
        ecrire(p, s)
        recousus += 1

    # --- le modele : sa pagination ne mene plus nulle part, on la ramene a l'accueil
    p = os.path.join(sortie, "site", "chapitres", "_modele.html")
    if os.path.isfile(p):
        s = io.open(p, encoding="utf-8").read()
        s = re.sub(r'(<a href=")\d\d-[a-z0-9-]+\.html(")', r'\1../index.html\2', s)
        ecrire(p, s)
        recousus += 1

    return recousus


CARTE = {"texte": {"fr": "À rédiger : deux lignes qui disent ce que ce chapitre permet de faire.",
                   "en": "To be written: two lines saying what this chapter enables."},
         "bouton": {"fr": "Ouvrir le chapitre %s &rarr;", "en": "Open chapter %s &rarr;"}}


def regenerer_sommaire(sortie, c):
    """Reecrit la grille de chapitres de cours.html depuis les chapitres declares.

    Ces cartes portent une prose propre a chaque chapitre : gardees telles
    quelles, un cours de droit aurait annonce « Cadrer son cours » et renvoye
    vers une page inexistante. Le sous-titre de la page devient un repère : il
    promettait qu'on saurait « concevoir un cours en ligne ».
    """
    F = os.path.join(sortie, "site", "cours.html")
    if not os.path.isfile(F):
        return 0
    t = io.open(F, encoding="utf-8").read()
    m = re.search(r'(<div class="concept-grid">)(.*?)(\n\s*</div>\s*\n\s*</section>)',
                  t, re.S)
    if not m:
        return 0

    lg = racine(c)
    cartes = []
    for ch in c["chapitres"]:
        num = h(ch.get("num", ""))
        cartes.append(
            '\n          <div class="concept-card">\n'
            '            <div class="concept-card-header">\n'
            '              <span class="concept-card-emoji">%s</span>\n'
            '              <span class="concept-card-title">%s · %s</span>\n'
            '            </div>\n'
            '            <p>%s</p>\n'
            '            <p style="margin-top:.75rem">'
            '<a class="btn btn-primary" href="chapitres/%s">%s</a></p>\n'
            '          </div>\n'
            % (ch.get("ico", "\U0001f4d8"), num, h(texte(ch["titre"], lg)), CARTE["texte"][lg],
               ch["fichier"], CARTE["bouton"][lg] % num))

    t = t[:m.start(2)] + "".join(cartes) + t[m.end(2):]
    t = sous_titre(t, SOUS_TITRE_SOMMAIRE[lg])
    ecrire(F, t)
    return len(cartes)


def vider_fiche_livret(sortie):
    """outils/livret.py (bloc « livret ») : la fiche du livret de démonstration perd ce qui parlait du template — le
    pied de la couverture, la catégorie, la présentation de l'auteur, que l'auteur écrit et valide (module 02) ;
    l'année devient celle de la création. Vrai si la fiche a changé."""
    f = os.path.join(sortie, "outils", "livret.py")
    if not os.path.isfile(f):
        return False
    s = io.open(f, encoding="utf-8").read()
    neuf = s
    for cle, suivante in (("pied_couverture", "categorie"), ("categorie", "annee"), ("presentation", "fiction")):
        neuf = re.sub(r"(^    %s=).*?(?=^    %s=)" % (cle, suivante),
                      lambda m: m.group(1) + '{"fr": "", "en": ""},\n', neuf, count=1, flags=re.S | re.M)
    neuf = re.sub(r"^    annee=\d{4},", "    annee=%d," % datetime.date.today().year, neuf, count=1, flags=re.M)
    if neuf != s:
        ecrire(f, neuf)
    return neuf != s


def purger_demo(sortie, c):
    """Retire le contenu de demonstration et remet des squelettes a la place.

    Le squelette de chapitre etait deja vide, mais les medias, le QCM, les
    flashcards, le glossaire et les polycopies ne l'etaient pas : un cours de
    cybersecurite serait arrive avec des capsules parlant de pedagogie.
    """
    retires = 0
    for rel in DEMO_DOSSIERS:
        d = os.path.join(sortie, rel.replace("/", os.sep))
        if not os.path.isdir(d):
            continue
        for f in os.listdir(d):
            p = os.path.join(d, f)
            if os.path.isfile(p):
                os.remove(p)
                retires += 1

    for rel in DEMO_FICHIERS:
        p = os.path.join(sortie, rel.replace("/", os.sep))
        if os.path.isfile(p):
            os.remove(p)
            retires += 1
    # et le lien qui y menait, sinon il resterait mort dans chaque pied de page ; et, dans les pages, les passages
    # propres au template (<!-- gabarit:debut --> … <!-- gabarit:fin -->), qui expliquent son outillage
    for f in glob.glob(os.path.join(sortie, "site", "**", "*.html"), recursive=True):
        s = io.open(f, encoding="utf-8").read()
        if "about.html" not in s and "<!-- gabarit:debut -->" not in s:
            continue
        s = re.sub(r' · <a href="[^"]*about\.html">.*?</a>', "", s, flags=re.S)
        s = BLOC_GABARIT.sub("\n", s)
        io.open(f, "w", encoding="utf-8", newline="\n").write(s)

    js = os.path.join(sortie, "site", "assets", "js")
    qcm = os.path.join(sortie, "site", "QCM")
    remplaces = 0
    subs = {"titre_fr": c["titre"]["fr"],
            "titre_en": c["titre"].get("en", c["titre"]["fr"]),
            "auteur": c["auteur"]}
    for chemin, contenu in (
            (os.path.join(qcm, "questions.js"), SQUELETTE_QCM_QUESTIONS % subs),
            (os.path.join(qcm, "corrections.js"), SQUELETTE_QCM_CORRECTIONS),
            (os.path.join(js, "flashcards-data.js"), SQUELETTE_FLASHCARDS),
            (os.path.join(js, "glossaire-data.js"), SQUELETTE_GLOSSAIRE),
            (os.path.join(js, "playlist-data.js"), SQUELETTE_PLAYLIST)):
        if os.path.isfile(chemin):
            ecrire(chemin, contenu)
            remplaces += 1

    pc = os.path.join(sortie, "tools", "polycopies_content.json")
    if os.path.isfile(pc):
        ecrire(pc, json.dumps(SQUELETTE_POLYCOPIES, ensure_ascii=False, indent=2) + "\n")
        remplaces += 1

    if vider_fiche_livret(sortie):
        remplaces += 1

    # le sous-titre du glossaire nommait la matière de la démonstration
    lg = racine(c)
    glo = os.path.join(sortie, "site", "glossaire.html")
    if os.path.isfile(glo):
        s = io.open(glo, encoding="utf-8").read()
        neuf = sous_titre(s, SOUS_TITRE_GLOSSAIRE[lg])
        if neuf != s:
            ecrire(glo, neuf)
            remplaces += 1

    # les fiches de capsules du cours de demonstration (ses chapitres, son accueil) n'ont rien a faire ici
    for nom in ("Capsules_du_cours_demo.md", "Capsules_accueil.md"):
        fiche = os.path.join(sortie, "docs", "prompts", nom)
        if os.path.isfile(fiche):
            os.remove(fiche)
            retires += 1

    # l'accueil : la structure de celui de la démonstration, sans sa prose ni « Ce que démontre ce site » ; ses
    # boutons (outils/accueil.py) repartent vides
    acc = os.path.join(sortie, "site", "index.html")
    if os.path.isfile(acc):
        ecrire(acc, accueil_squelette(c, io.open(acc, encoding="utf-8").read()))
        remplaces += 1
    if vider_boutons_accueil(sortie):
        remplaces += 1

    # l'atelier et les activites de la demonstration
    for rel, titre, consigne in PAGES_DEMO:
        p = os.path.join(sortie, rel.replace("/", os.sep))
        if os.path.isfile(p) and vider_page(p, titre[lg], consigne[lg], lg):
            remplaces += 1

    return retires, remplaces


def fichiers_locaux(sortie):
    """Les fichiers et dossiers propres au cours (LOCAUX) sous les dossiers que la création recopie, en chemins
    relatifs à la sortie. Ils ne sont jamais ouverts : seuls leurs noms servent."""
    trouves = []
    for nom in COPIER:
        racine = os.path.join(sortie, nom)
        if not os.path.isdir(racine):
            continue
        for dossier, sous, fichiers in os.walk(racine):
            for n in list(sous) + fichiers:
                if any(fnmatch.fnmatch(n, m) for m in LOCAUX):
                    trouves.append(os.path.relpath(os.path.join(dossier, n), sortie).replace(os.sep, "/"))
            sous[:] = [s for s in sous if not any(fnmatch.fnmatch(s, m) for m in LOCAUX)]
    return sorted(trouves)


def garder_locaux(sortie, nom, recopier):
    """--ecraser : remplace le dossier « nom » de la sortie par celui du template (recopier()), mais laisse en place
    ses fichiers locaux. Ils passent le temps de la copie dans un abri caché de la sortie elle-même (même disque,
    aucune copie hors du cours), puis reviennent à leur chemin. [chemins gardés]"""
    gardes = [r for r in fichiers_locaux(sortie) if r.split("/")[0] == nom]
    abri = tempfile.mkdtemp(prefix=".ecraser-", dir=sortie) if gardes else None
    for rel in gardes:
        cible = os.path.join(abri, rel.replace("/", os.sep))
        os.makedirs(os.path.dirname(cible), exist_ok=True)
        shutil.move(os.path.join(sortie, rel.replace("/", os.sep)), cible)
    try:
        shutil.rmtree(os.path.join(sortie, nom))
        recopier()
    finally:
        for rel in gardes:
            dst = os.path.join(sortie, rel.replace("/", os.sep))
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.move(os.path.join(abri, rel.replace("/", os.sep)), dst)
        if abri:
            shutil.rmtree(abri)
    return gardes


def copier_secrets(sortie, c, essai=False):
    """Recopie en local les secrets communs à tous les cours, sans les ouvrir.

    [(chemin, ce qui a été fait)]. Un secret n'est copié que si le .gitignore du
    nouveau cours l'exclut : sinon, le premier « git add . » le publierait.
    """
    gi = os.path.join(sortie if not essai else RACINE, ".gitignore")
    regles = set()
    if os.path.isfile(gi):
        regles = {l.strip() for l in io.open(gi, encoding="utf-8") if l.strip()}
    bilan = []
    for rel, bloc, motifs in SECRETS_LOCAUX:
        src = os.path.join(RACINE, rel.replace("/", os.sep))
        if not os.path.isfile(src):
            bilan.append((rel, "absent du template : à déposer à la main"))
        elif bloc and not bloc_actif(c, bloc):
            bilan.append((rel, "bloc « %s » désactivé : non copié" % bloc))
        elif not regles & set(motifs):
            bilan.append((rel, "NON copié : le .gitignore du cours ne l'exclut pas"))
        elif essai:
            bilan.append((rel, "serait copié en local, ignoré par Git"))
        else:
            dst = os.path.join(sortie, rel.replace("/", os.sep))
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src, dst)
            bilan.append((rel, "copié en local, ignoré par Git — contenu non affiché"))
    return bilan


def destination_json(c):
    """deploiement/destination.json : où ce cours se publie. Sans secret, versionné.

    Le répertoire distant ne vient jamais de deploiement/config.json : recopiée
    d'un cours à l'autre, cette configuration désigne le dossier du cours
    précédent, et le premier envoi l'aurait écrasé.
    """
    p = c.get("publication") or {}
    d = {
        "_lisez_moi": "Où ce cours se publie — écrit par nouveau_cours.py d'après cours.json. "
                      "Sans secret : versionné avec le cours. Les accès à l'hébergement sont dans "
                      "deploiement/config.json (local, ignoré par Git). Voir deploiement/LISEZMOI.md.",
        "cours": c["slug"],
        "repertoire_distant": str(p.get("repertoire_distant") or "/www/chemin/du-cours"),
        "url": str(p.get("url") or ""),
        "zones_protegees": list(p.get("zones_protegees") or []),
    }
    return json.dumps(d, ensure_ascii=False, indent=2) + "\n"


def contrat_du_cours(c):
    """Le CLAUDE.md du nouveau cours : celui du template, sans ses passages propres au template.

    Claude le lit à chaque ouverture du dossier : les exigences de l'auteur — dialogue,
    secrets, Git, audio, quiz, publication — s'y appliquent sans qu'on ait à les rappeler.
    """
    t = io.open(os.path.join(RACINE, "CLAUDE.md"), encoding="utf-8").read()
    t = BLOC_GABARIT.sub("\n", t)
    entete = ("# %s — contrat de travail\n\n"
              "Le site du cours « %s » (identifiant `%s`), créé à partir du template de\n"
              "cours. Ce fichier est lu à chaque ouverture : il dit ce qu'il faut savoir\n"
              "avant de toucher à quoi que ce soit. La méthode de création, avec ses jalons,\n"
              "est dans `prompts/PROMPT-Cours-parametrable.md` et ses modules\n"
              "(`prompts/modules/`, un par option)."
              % (c["titre"]["fr"], c["titre"]["fr"], c["slug"]))
    t = re.sub(r"^# .*$", lambda m: entete, t, count=1, flags=re.M)
    # Les sections retirées laissaient un trou dans la numérotation : on renumérote.
    rang = [0]

    def renumeroter(m):
        rang[0] += 1
        return "## %d. " % rang[0]
    t = re.sub(r"^## \d+\. ", renumeroter, t, flags=re.M)
    return re.sub(r"\n{3,}", "\n\n", t)


# ---------------------------------------------------------------- lecture
def charger(chemin):
    if not os.path.isfile(chemin):
        sys.exit("Configuration absente : %s\n    cp %s %s"
                 % (chemin, os.path.relpath(MODELE, os.getcwd()), "cours.json"))
    with io.open(chemin, encoding="utf-8") as f:
        try:
            c = json.load(f)
        except ValueError as e:
            sys.exit("cours.json n'est pas un JSON valide : %s" % e)
    return c


def valider(c):
    """Refuse tôt et clairement plutôt que de produire un cours à moitié faux."""
    griefs = []

    slug = str(c.get("slug", "")).strip()
    if not slug or slug == "mon-cours":
        griefs.append("« slug » est vide ou resté sur la valeur du modèle.")
    elif not re.match(r"^[a-z0-9][a-z0-9-]*$", slug):
        griefs.append("« slug » ne doit contenir que des minuscules, chiffres et tirets : %r" % slug)

    for cle in ("titre", "sous_titre"):
        v = c.get(cle)
        if not isinstance(v, dict) or not str(v.get("fr", "")).strip():
            griefs.append("« %s.fr » est vide." % cle)

    if c.get("palette") not in PALETTES:
        griefs.append("« palette » doit valoir l'une de %s (lu : %r)"
                      % (", ".join(PALETTES), c.get("palette")))

    langues = c.get("langues") or []
    if langues and langues[0] == "ar":
        griefs.append("l'arabe ne peut pas encore être la langue racine : la démonstration n'a pas toutes ses pages en "
                      "arabe (lot 4). Mettez-le après la racine : [\"fr\", \"ar\"].")
    elif not langues or langues[0] not in RACINES:
        griefs.append("« langues » doit commencer par la langue racine du cours, %s : la démonstration n'existe "
                      "encore que dans ces langues." % " ou ".join("« %s »" % l for l in RACINES))
    for l in langues:
        if l not in ("fr", "en", "ar"):
            griefs.append("langue non gérée : %r (fr, en et ar le sont)" % l)

    # Les filières d'un cours commun (décision de l'auteur du 21 novembre 2026) : une liste, vide ou d'une seule
    # entrée pour un cours sans bascule. Chaque filière : id, code (le sigle affiché), palette, nom et court.
    filieres = c.get("filieres") or []
    if not isinstance(filieres, list):
        griefs.append("« filieres » doit être une liste (vide pour un cours sans filière).")
        filieres = []
    vues = set()
    for f in filieres:
        f = f if isinstance(f, dict) else {}
        ident = str(f.get("id", ""))
        if not re.match(r"^[a-z0-9][a-z0-9-]*$", ident) or ident in vues:
            griefs.append("filière %r : « id » doit être unique, en minuscules, chiffres et tirets." % ident)
        vues.add(ident)
        if not str(f.get("code", "")).strip():
            griefs.append("filière %s : « code », le sigle affiché, est vide." % ident)
        if f.get("palette") not in PALETTES:
            griefs.append("filière %s : « palette » doit valoir l'une de %s (lu : %r)."
                          % (ident, ", ".join(PALETTES), f.get("palette")))
        for cle in ("nom", "court"):
            if not str((f.get(cle) or {}).get(racine(c), "")).strip():
                griefs.append("filière %s : « %s.%s » est vide." % (ident, cle, racine(c)))
    if len(set(langues)) != len(langues):
        griefs.append("« langues » nomme deux fois la même langue.")

    chapitres = c.get("chapitres") or []
    if not chapitres:
        griefs.append("« chapitres » est vide : un cours sans chapitre n'a pas d'objet.")
    vus = set()
    for ch in chapitres:
        f = ch.get("fichier", "")
        if not re.match(r"^\d{2}-[a-z0-9-]+\.html$", f):
            griefs.append("nom de fichier de chapitre invalide : %r "
                          "(attendu : 01-quelque-chose.html)" % f)
        if f in vus:
            griefs.append("deux chapitres portent le même fichier : %r" % f)
        vus.add(f)
        if not str((ch.get("titre") or {}).get("fr", "")).strip():
            griefs.append("chapitre %s : titre français vide." % ch.get("num", "?"))

    if not str(c.get("auteur", "")).strip() or c.get("auteur") == "Prénom NOM":
        griefs.append("« auteur » est vide ou resté sur la valeur du modèle.")

    if c.get("logo") is not None and not (1 <= len(str(c["logo"])) <= 2):
        griefs.append("« logo » : une ou deux lettres (lu : %r)." % c["logo"])

    if bloc_actif(c, "livret") and not bloc_actif(c, "glossaire"):
        griefs.append("le bloc « livret » demande le bloc « glossaire » : le polycopié imprime le glossaire, "
                      "les définitions dans la marge et l'index.")

    # La destination de publication : facultative à la création, mais jamais une
    # racine d'hébergement — une purge y effacerait tous les autres cours.
    distant = str((c.get("publication") or {}).get("repertoire_distant") or "").strip()
    if distant:
        norme = "/" + distant.strip("/")
        if norme in RACINES_HEBERGEMENT or ".." in norme.split("/"):
            griefs.append("« publication.repertoire_distant » (%s) doit être un dossier propre au "
                          "cours, pas une racine d'hébergement." % distant)
        else:
            c["publication"]["repertoire_distant"] = norme

    if griefs:
        print("\nLa configuration ne permet pas de générer le cours :\n")
        for g in griefs:
            print("  - %s" % g)
        print("\n  Corrigez cours.json puis relancez. Le modèle commenté est dans "
              "cours.exemple.json.")
        sys.exit(1)


# ---------------------------------------------------------------- écriture
# Les libellés des ressources du menu, dans chaque langue (l'arabe d'après docs/LEXIQUE-ar.md).
RESSOURCES = {
    "polycopie.html": ("📘", "Polycopié", "Course book", "المطبوعة"),
    "glossaire.html": ("📚", "Glossaire bilingue", "Bilingual glossary", "مسرد المصطلحات"),
    "QCM/index.html": ("📝", "QCM d'évaluation", "Assessment quiz", "اختبار الاختيار من متعدّد"),
    "polycopies.html": ("📄", "Fiches de synthèse", "Summary sheets", "البطاقات التلخيصية"),
    "podcasts.html": ("🎙️", "Podcasts", "Podcasts", "البودكاست"),
    "activites.html": ("🧩", "Activités interactives", "Interactive activities", "الأنشطة التفاعلية"),
    "atelier.html": ("🧵", "Atelier fil rouge", "Capstone workshop", "ورشة المشروع التطبيقي"),
}


def course_data(c):
    """Le fichier de données du cours, source unique de la navigation."""
    langues = c.get("langues") or ["fr"]

    def paire(d, defaut=""):
        """{ fr, en[, ar] } : l'anglais retombe sur le français si le cours ne l'a pas ; l'arabe ne s'écrit que si le
        cours le déclare et que cours.json le donne."""
        fr = (d or {}).get("fr", defaut)
        en = (d or {}).get("en", fr) if "en" in langues else fr
        texte = '{ fr: %s, en: %s' % (json.dumps(fr, ensure_ascii=False), json.dumps(en, ensure_ascii=False))
        if "ar" in langues and (d or {}).get("ar"):
            texte += ', ar: %s' % json.dumps(d["ar"], ensure_ascii=False)
        return texte + ' }'

    lignes = [
        "/* =================================================================",
        "   course-data.js — Données du cours (source unique de vérité)",
        "",
        "   FICHIER GÉNÉRÉ par nouveau_cours.py d'après cours.json.",
        "   Vous pouvez l'éditer à la main ensuite : c'est ce fichier qui fait foi",
        "   pour la navigation, pas cours.json, qui n'a servi qu'à l'amorçage.",
        "",
        "   %s — %s" % (c["auteur"], c.get("licence", {}).get("fr", "")),
        "   ================================================================= */",
        "window.COURSE = {",
        "  title: %s," % paire(c.get("titre")),
        "  subtitle: %s," % paire(c.get("sous_titre")),
        "  author: %s," % json.dumps(c["auteur"], ensure_ascii=False),
        "  license: %s," % paire(c.get("licence")),
    ]
    # Les filières : la bascule de filiere.js et le masquage de filieres.css (outils/generer_filieres.py), dès deux.
    # Une seule s'écrit aussi, pour les pages qui la nomment : sans deux filières, ni bascule ni masquage.
    filieres = c.get("filieres") or []
    if filieres:
        lignes.append("  filieres: [")
        for f in filieres:
            lignes.append("    { id: %s, code: %s, palette: %s%s,"
                          % (json.dumps(f["id"]), json.dumps(f["code"], ensure_ascii=False), json.dumps(f["palette"]),
                             ", rncp: %s" % json.dumps(str(f["rncp"])) if f.get("rncp") else ""))
            lignes.append("      nom: %s," % paire(f.get("nom")))
            lignes.append("      court: %s }," % paire(f.get("court")))
        lignes[-1] = lignes[-1][:-1]
        lignes.append("  ],")
    lignes.append("  chapters: [")
    for ch in c["chapitres"]:
        lignes.append("    { num: %s, ico: %s, file: %s,"
                      % (json.dumps(str(ch.get("num", "")), ensure_ascii=False),
                         json.dumps(ch.get("ico", "📘"), ensure_ascii=False),
                         json.dumps(ch["fichier"], ensure_ascii=False)))
        lignes.append("      title: %s }," % paire(ch.get("titre")))
    if lignes[-1].endswith(","):
        lignes[-1] = lignes[-1][:-1]
    lignes.append("  ],")

    lignes.append("  resources: [")
    res = []
    b = c.get("blocs", {})
    if bloc_actif(c, "livret"):
        res.append("polycopie.html")
    if b.get("glossaire", True):
        res.append("glossaire.html")
    if b.get("qcm", True):
        res.append("QCM/index.html")
    if b.get("polycopies", True):
        res.append("polycopies.html")
    if bloc_actif(c, "podcasts"):
        res.append("podcasts.html")
    if b.get("activites", True):
        res.append("activites.html")
    if b.get("atelier", True):
        res.append("atelier.html")
    for href in res:
        ico, fr, en, ar = RESSOURCES[href]
        lignes.append('    { ico: "%s", href: "%s", label: %s },' % (ico, href, paire({"fr": fr, "en": en, "ar": ar})))
    if lignes[-1].endswith(","):
        lignes[-1] = lignes[-1][:-1]
    lignes += ["  ]", "};", ""]
    return "\n".join(lignes)


PLACEHOLDER = {
    "fr": "À rédiger. Remplacez ce paragraphe par le contenu du chapitre.",
    "en": "To be written. Replace this paragraph with the chapter content.",
}
TITRE_SECTION = {"fr": "%d. Titre de section à rédiger", "en": "%d. Section title to be written"}
OBJECTIF = {"fr": "À rédiger : un objectif du chapitre, avec un verbe d'action observable.",
            "en": "To be written: a chapter objective, with an observable action verb."}

# Le texte d'un chapitre de la démonstration vit dans des <span> sans attribut : ce sont ses anciens blocs
# bilingues, dont la conversion au site miroir n'a ôté que l'attribut data-tr. Le chapitre vitrine n'en a pas
# d'autres (vérifié sur la démo d'avant la conversion).
PROSE = re.compile(r"<span>(?:(?!</span>).)*?</span>", re.S)


def vider_prose(t, lg):
    """Remplace le texte des paragraphes et des listes par un repère visible.

    On garde la structure — sections, listes, encadrés, appels de composants —
    et on retire le contenu. Un squelette qui conserverait la prose du chapitre
    vitrine ferait courir un vrai risque : une section oubliée à la relecture
    partirait en ligne en parlant d'autre chose que du cours.
    """
    def remplacer(m):
        return "<span>%s</span>" % PLACEHOLDER[lg]

    # les objectifs du chapitre : ils sont dans l'en-tete, donc hors de la
    # plage traitee plus bas, et ils portaient les objectifs de la demonstration.
    # Seule leur liste se vide : l'en-tête « Objectifs du chapitre » devenait
    # lui aussi un repère de paragraphe.
    o = t.find('<div class="chapter-objectives">')
    if o > -1:
        u = t.index("<ul>", o)
        uf = t.index("</ul>", u)
        t = t[:u] + PROSE.sub(lambda m: "<span>%s</span>" % OBJECTIF[lg], t[u:uf]) + t[uf:]

    # uniquement dans le corps, et uniquement les blocs de prose
    debut = t.index("<!-- ============ 1 ============ -->")
    fin = t.index("<nav class=\"chapter-pagination\">")
    corps = PROSE.sub(remplacer, t[debut:fin])

    # Les titres de section : un repère court et numéroté, pas le paragraphe de remplissage — ils s'affichent dans
    # la page et dans le menu (outils/generer_nav_sections.py les y reporte).
    def titre(m):
        titre.n += 1
        return '<h2%s><span>%s</span></h2>' % (m.group(1), TITRE_SECTION[lg] % titre.n)
    titre.n = 0
    corps = re.sub(r"<h2\b([^>]*)>.*?</h2>", titre, corps, flags=re.S)
    return t[:debut] + corps + t[fin:]


def textes_vides(c):
    """Le bloc TEXTES du chapitre, réduit à des repères.

    On conserve les clés et le motif — c'est ce qui s'apprend — et on vide les
    valeurs. Le chapitre vitrine reste consultable dans _modele.html pour voir
    un exemple rempli.
    """
    return """  var TEXTES = {
    /* Le motif bilingue : tout le contenu des composants ici, une fois par
       langue, et monter() est rejoue au changement de langue. Un exemple
       entierement rempli se trouve dans chapitres/_modele.html. */
    fr: {
      capsuleTitre: "Titre de la capsule d'ouverture",
      capsuleTrans: "Transcription de la capsule — a rediger.",
      revealQ: "Question posee avant la lecture ?",
      revealIndice: "Un indice qui oriente sans donner la reponse.",
      revealOptions: ["Premiere proposition.", "Deuxieme proposition.", "Troisieme proposition."],
      revealReponse: "La reponse, et surtout POURQUOI c'est celle-la.",
      checkTitre: "Point de controle",
      checkQ1: "Premiere question ?",
      checkO1: ["Proposition A.", "Proposition B.", "Proposition C."],
      checkE1: "Pourquoi B est juste, et pourquoi les autres ne le sont pas.",
      checkQ2: "Deuxieme question ?",
      checkO2: ["Proposition A.", "Proposition B.", "Proposition C."],
      checkE2: "L'explication de la deuxieme question.",
      /* Pourquoi chaque autre proposition ne convient pas (vide pour la bonne
         reponse), et deux a quatre renvois vers l'endroit exact qui repond :
         prompts/15_explications_quiz.md. */
      checkP1: ["Pourquoi A ne convient pas — a rediger.", "", "Pourquoi C ne convient pas — a rediger."],
      checkA1: [["Section 2 de ce chapitre", "#ch1-s2"], ["Section 1 de ce chapitre", "#ch1-s1"]],
      checkP2: ["Pourquoi A ne convient pas — a rediger.", "", "Pourquoi C ne convient pas — a rediger."],
      checkA2: [["Section 3 de ce chapitre", "#ch1-s3"], ["Section 1 de ce chapitre", "#ch1-s1"]],
      matchConsigne: "Reliez chaque element a son correspondant.",
      matchG: "Colonne de gauche",
      matchD: "Colonne de droite",
      matchPaires: [["Element 1", "Correspondant 1"], ["Element 2", "Correspondant 2"]],
      spotConsigne: "Reperez les affirmations qui posent probleme.",
      spotIntro: "Titre du document a relire",
      spotFrags: [
        ["Une affirmation fausse.", true, "Pourquoi elle est fausse."],
        ["Une affirmation juste.", false, ""]
      ],
      branchTitre: "Titre du cas",
      branchIntro: "La situation, en deux phrases.",
      branchSituation: "Ce qu'il faut decider.",
      branchQuestion: "Quelle est votre decision ?",
      branchOptions: [
        ["Premiere option.", false, "Ce qu'elle produit, et pourquoi c'est un probleme."],
        ["Deuxieme option.", true, "Pourquoi c'est la bonne."]
      ],
      branchLibelle: "Consequence",
      schemaAlt: "Description du schema, pour qui ne le voit pas.",
      schemaLegende: "Schema 1 — ce qu'il montre et ce qu'il faut en retenir.",
      /* Le schema et ses points chauds : absents, monter() s'arretait sur
         « X.schemaPoints.map » et ni le parcours par etapes ni le sommaire
         n'etaient montes. Chaque point : [x %, y %, titre, explication]. */
      schemaSrc: "",
      schemaPoints: [[50, 50, "Premier element du schema", "Ce qu'il represente, et comment le lire — a rediger."]]
    },
    en: {
      capsuleTitre: "Opening capsule title",
      capsuleTrans: "Capsule transcript — to be written.",
      revealQ: "Question asked before reading?",
      revealIndice: "A hint that points without giving the answer.",
      revealOptions: ["First option.", "Second option.", "Third option."],
      revealReponse: "The answer, and above all WHY it is that one.",
      checkTitre: "Checkpoint",
      checkQ1: "First question?",
      checkO1: ["Option A.", "Option B.", "Option C."],
      checkE1: "Why B is right, and why the others are not.",
      checkQ2: "Second question?",
      checkO2: ["Option A.", "Option B.", "Option C."],
      checkE2: "The explanation for the second question.",
      checkP1: ["Why A does not fit — to be written.", "", "Why C does not fit — to be written."],
      checkA1: [["Section 2 of this chapter", "#ch1-s2"], ["Section 1 of this chapter", "#ch1-s1"]],
      checkP2: ["Why A does not fit — to be written.", "", "Why C does not fit — to be written."],
      checkA2: [["Section 3 of this chapter", "#ch1-s3"], ["Section 1 of this chapter", "#ch1-s1"]],
      matchConsigne: "Match each item with its counterpart.",
      matchG: "Left column",
      matchD: "Right column",
      matchPaires: [["Item 1", "Counterpart 1"], ["Item 2", "Counterpart 2"]],
      spotConsigne: "Spot the statements that are a problem.",
      spotIntro: "Title of the document to review",
      spotFrags: [
        ["A false statement.", true, "Why it is false."],
        ["A correct statement.", false, ""]
      ],
      branchTitre: "Case title",
      branchIntro: "The situation, in two sentences.",
      branchSituation: "What must be decided.",
      branchQuestion: "What is your decision?",
      branchOptions: [
        ["First option.", false, "What it produces, and why that is a problem."],
        ["Second option.", true, "Why this is the right one."]
      ],
      branchLibelle: "Consequence",
      schemaAlt: "Description of the diagram, for those who cannot see it.",
      schemaLegende: "Diagram 1 — what it shows and what to take from it.",
      schemaSrc: "",
      schemaPoints: [[50, 50, "First element of the diagram", "What it represents, and how to read it — to be written."]]
    }
  };
"""


TITRE_CHAPITRE = {"fr": "Chapitre %s : %s", "en": "Chapter %s: %s"}
AVERTISSEMENT_SQUELETTE = {
    "fr": ("Chapitre à rédiger",
           "Ce squelette vient de <code>nouveau_cours.py</code>. Il conserve la\n"
           "        structure et les appels de composants du chapitre vitrine, mais son\n"
           "        contenu est vide : rien de la démonstration ne peut survivre par\n"
           "        inadvertance. L'exemple entièrement rempli reste consultable dans\n"
           "        <code>chapitres/_modele.html</code>. Supprimez cet encadré une fois le\n"
           "        chapitre écrit."),
    "en": ("Chapter to be written",
           "This skeleton comes from <code>nouveau_cours.py</code>. It keeps the\n"
           "        structure and the component calls of the showcase chapter, but its\n"
           "        content is empty: nothing from the demo can survive by accident.\n"
           "        The fully written example remains available in\n"
           "        <code>chapitres/_modele.html</code>. Delete this box once the\n"
           "        chapter is written."),
}


def squelette_chapitre(c, ch, modele):
    """Un chapitre vide mais complet : structure, appels de composants, reperes.

    On part du chapitre vitrine plutot que d'un gabarit separe : ainsi le
    squelette ne peut pas diverger du moteur reel, puisqu'il EST le chapitre
    reel, vide de son contenu.
    """
    lg = racine(c)
    t = modele
    titre = texte(ch["titre"], lg)
    num = str(ch.get("num", ""))

    # Le titre de l'onglet se remplace en entier, quel qu'il soit : cherché mot pour mot, il a cessé d'être reconnu
    # quand le chapitre vitrine a quitté ses tirets (ea1cc23), et chaque squelette s'annonçait « Chapitre 1 : Cadrer
    # son cours » dans la barre d'onglets.
    t = re.sub(r"<title>.*?</title>", lambda m: "<title>%s</title>" % h(TITRE_CHAPITRE[lg] % (num, titre)),
               t, count=1, flags=re.S)
    t = t.replace('data-accent="marine"', 'data-accent="%s"' % c["palette"])
    t = re.sub(r'(<h1 class="chapter-title">).*?(</h1>)',
               lambda m: '%s<span>%s</span>%s' % (m.group(1), h(titre), m.group(2)), t, count=1, flags=re.S)
    t = t.replace(">Chapitre 1<", ">Chapitre %s<" % num)
    t = t.replace(">Chapter 1<", ">Chapter %s<" % num)
    # Le badge « Chapitre vitrine » ne dit rien d'un squelette.
    t = re.sub(r'\s*<span class="pill navy"><span>(?:Chapitre vitrine|Showcase chapter)</span></span>', "", t)
    t = t.replace("RDCX.steps({ chapitre: '1' })",
                  "RDCX.steps({ chapitre: '%s' })" % (num or "1"))
    # La durée de l'en-tête est un fragment du référentiel (outils/generer_fragments.py) : celui du chapitre.
    t = re.sub(r"FRAGMENT:duree-\d+ ", "FRAGMENT:duree-%s " % (num or "1"), t)

    # Le sous-titre de l'en-tête : l'accroche du chapitre de démonstration.
    t = sous_titre(t, SOUS_TITRE_CHAPITRE[lg])

    # La meta-description decrivait le chapitre de demonstration : elle part
    # dans les moteurs de recherche et dans les apercus de partage.
    t = re.sub(r'<meta name="description" content="[^"]*">',
               lambda m: '<meta name="description" content="%s">'
                         % att("%s. %s" % (TITRE_CHAPITRE[lg] % (num, titre), texte(c["titre"], lg))), t, count=1)

    # Les titres d'etapes et de sommaire sont des ATTRIBUTS, pas de la prose :
    # le vidage de la prose ne les voit pas.
    def num_section(m):
        num_section.n += 1
        return '%s="Section %d"' % (m.group(1), num_section.n)
    for nom in ("data-step-titre", "data-sommaire-titre"):
        num_section.n = 0
        t = re.sub(r'(%s)="[^"]*"' % re.escape(nom), num_section, t)

    # le contenu des composants : les cles restent, les valeurs sont videes
    d = t.index("  var TEXTES = {")
    f = t.index("  function textes()", d)
    t = t[:d] + textes_vides(c) + "\n" + t[f:]

    # Les exemples propres à une filière (le témoin de la bascule, classes only-<id>) : un squelette n'en garde pas, le
    # cours déclarera ses propres filières. _modele.html, lui, les garde comme exemple.
    t = re.sub(r"\n[ \t]*<!-- Le témoin de la bascule de filière[^\n]*-->", "", t)
    t = re.sub(r'\n[ \t]*<div class="exemple-filiere only-[a-z0-9-]+">.*?</div>', "", t, flags=re.S)

    # la prose des sections
    t = vider_prose(t, lg)

    titre_avert, texte_avert = AVERTISSEMENT_SQUELETTE[lg]
    avert = (
        '\n    <div class="callout warning">\n'
        '      <div class="callout-icon">✏️</div>\n'
        '      <div class="callout-content">\n'
        '        <h4>%s</h4>\n'
        '        <p>%s</p>\n'
        '      </div>\n'
        '    </div>\n' % (titre_avert, texte_avert))
    t = t.replace('    <!-- ============ Médias du chapitre ============ -->',
                  avert + '\n    <!-- ============ Médias du chapitre ============ -->', 1)
    return t


def referentiel_vide():
    """Le référentiel du template (outils/referentiel.py), sans les valeurs du cours de démonstration."""
    t = io.open(os.path.join(RACINE, "outils", "referentiel.py"), encoding="utf-8").read()
    t = re.sub(r"\n# Le cours de démonstration[^\n]*\n", "\n", t)
    return re.sub(r"^(DUREES|VALEURS|FRAGMENTS) = .*$", lambda m: "%s = {}" % m.group(1), t, flags=re.M)


def promouvoir_jumelles(site, langue):
    """Un cours dont la langue racine n'est pas celle de la démonstration (le français) part de ses jumelles : chaque
    page <langue>/X.html prend la place de X.html, ses chemins remontés d'un cran (outils/miroir.py, remonter). Une
    page sans jumelle resterait en français : la démonstration les a toutes en anglais. Le nombre de pages prises."""
    base = os.path.join(site, langue)
    spec = importlib.util.spec_from_file_location("miroir", os.path.join(RACINE, "outils", "miroir.py"))
    miroir = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(miroir)
    n = 0
    for p in sorted(glob.glob(os.path.join(base, "**", "*.html"), recursive=True)):
        rel = os.path.relpath(p, base).replace(os.sep, "/")
        t = io.open(p, encoding="utf-8").read()
        ecrire(os.path.join(site, *rel.split("/")), miroir.remonter(t, rel, langue, site))
        n += 1
    return n


def ecrire(chemin, contenu):
    d = os.path.dirname(chemin)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    io.open(chemin, "w", encoding="utf-8", newline="\n").write(contenu)


# ---------------------------------------------------------------- programme
def main():
    ap = argparse.ArgumentParser(description="Crée un cours à partir du template.")
    ap.add_argument("--config", default=CONFIG_DEFAUT)
    ap.add_argument("--sortie", help="remplace le champ « sortie » de la configuration")
    ap.add_argument("--essai", action="store_true", help="n'écrit rien, dit ce qu'il ferait")
    ap.add_argument("--ecraser", action="store_true",
                    help="accepte un dossier non vide ; ses fichiers locaux (LOCAUX) restent en place")
    ap.add_argument("--avec-demo", action="store_true",
                    help="conserve les medias et le contenu du cours de demonstration")
    args = ap.parse_args()

    c = charger(args.config)
    valider(c)

    sortie = os.path.abspath(os.path.join(RACINE, args.sortie or c.get("sortie", "../cours")))
    langue = racine(c)

    print("\nCours à créer\n-------------")
    print("  titre     : %s" % c["titre"]["fr"])
    print("  slug      : %s" % c["slug"])
    print("  palette   : %s" % c["palette"])
    print("  langues   : %s  (racine : %s%s)" % (", ".join(c["langues"]), langue,
                                               " ; les autres en pages jumelles, ensuite"
                                               if len(c["langues"]) > 1 else ""))
    filieres = c.get("filieres") or []
    print("  filières  : %s" % (" · ".join(f["code"] for f in filieres) + ("" if len(filieres) > 1
                                                                          else "  (une seule : pas de bascule)")
                                 if filieres else "aucune"))
    print("  chapitres : %d" % len(c["chapitres"]))
    for ch in c["chapitres"]:
        print("      %-3s %-28s %s" % (ch.get("num", "?"), ch["fichier"], ch["titre"]["fr"][:40]))
    actifs = [k for k, v in (c.get("blocs") or {}).items() if v]
    print("  blocs     : %s" % (", ".join(sorted(actifs)) or "aucun"))
    print("  sortie    : %s" % sortie)
    distant = (c.get("publication") or {}).get("repertoire_distant")
    if bloc_actif(c, "deploiement"):
        print("  publication : %s" % (distant or "à renseigner (destination.json) avant le premier envoi"))

    # Le template n'est jamais sa propre sortie : y écrire écraserait son site de
    # démonstration et ses squelettes de référence.
    s, r = os.path.normcase(sortie), os.path.normcase(RACINE)
    if s == r or r.startswith(s + os.sep) or s.startswith(r + os.sep):
        sys.exit("\n  La sortie désigne le template lui-même, un dossier qui le contient ou un "
                 "dossier qu'il contient : %s\n  Choisissez un dossier à part." % sortie)
    if os.path.isdir(sortie) and os.listdir(sortie) and not args.ecraser:
        sys.exit("\n  Le dossier de sortie n'est pas vide : %s\n"
                 "  Relancez avec --ecraser si c'est voulu." % sortie)

    if args.essai:
        if args.ecraser and os.path.isdir(sortie):
            locaux = fichiers_locaux(sortie)
            print("\n  --ecraser garderait en place %d fichier(s) local(aux) du cours%s"
                  % (len(locaux), " :" if locaux else "."))
            for rel in locaux:
                print("      %s" % rel)
        print("\n  Secrets locaux :")
        for rel, quoi in copier_secrets(sortie, c, essai=True):
            print("      %-26s %s" % (rel, quoi))
        print("\n  Simulation : rien n'a été écrit.")
        return 0

    print("\nCréation\n--------")
    if not os.path.isdir(sortie):
        os.makedirs(sortie)

    gardes = []
    for nom in COPIER:
        src = os.path.join(RACINE, nom)
        if not os.path.exists(src):
            continue
        dst = os.path.join(sortie, nom)
        if os.path.isdir(src):
            if os.path.isdir(dst):
                # --ecraser : les secrets, carnets d'envoi et réglages du cours ne viennent pas du template ;
                # supprimés avec leur dossier, ils seraient perdus (deploiement/known_hosts l'a été).
                gardes += garder_locaux(sortie, nom, lambda: shutil.copytree(src, dst, ignore=NE_PAS_COPIER))
            else:
                shutil.copytree(src, dst, ignore=NE_PAS_COPIER)
        else:
            shutil.copy2(src, dst)
    print("  arborescence copiée (%d entrées)" % len(COPIER))
    if gardes:
        print("  fichiers locaux du cours gardés en place (non ouverts) : %s" % ", ".join(gardes))

    # --- la langue racine. Un cours anglais prend à la racine les jumelles anglaises de la démonstration ; puis les
    #     dossiers de jumelles partent tous : recopiés, ils apportaient seize pages de la démonstration, déclarées
    #     dans la mauvaise langue. Les autres langues du cours viennent ensuite, page par page, avec
    #     outils/creer_jumelle.py, une fois la racine stable.
    site = os.path.join(sortie, "site")
    if langue != "fr":
        print("  %d page(s) de la démonstration prises en « %s »" % (promouvoir_jumelles(site, langue), langue))
    for d in DOSSIERS_LANGUE:
        if os.path.isdir(os.path.join(site, d)):
            shutil.rmtree(os.path.join(site, d))
    # La liste des pages traduites : vide, faute de jumelles (celle de la démonstration en nommait seize, et le
    # bouton des langues aurait mené à des pages absentes).
    r = subprocess.run([sys.executable, os.path.join(sortie, "outils", "generer_langues.py")],
                       capture_output=True, text=True, encoding="utf-8")
    print("  langues-data.js : %s" % ("aucune page traduite pour l'instant" if r.returncode == 0
                                      else "NON écrit (%s)" % (r.stderr.strip() or r.stdout.strip())[-160:]))

    # --- le contrat de travail du cours, lu par Claude à chaque ouverture
    ecrire(os.path.join(sortie, "CLAUDE.md"), contrat_du_cours(c))
    print("  CLAUDE.md écrit : les exigences de l'auteur s'appliquent à ce cours")

    # --- blocs désactivés
    retires = 0
    for cle, chemins in BLOCS.items():
        if bloc_actif(c, cle):
            continue
        for rel in chemins:
            p = os.path.join(sortie, rel.replace("/", os.sep))
            if os.path.isdir(p):
                shutil.rmtree(p); retires += 1
            elif os.path.isfile(p):
                os.remove(p); retires += 1
    if retires:
        print("  %d élément(s) retiré(s) pour les blocs désactivés" % retires)
    if not bloc_actif(c, "livret"):
        for f in glob.glob(os.path.join(sortie, "site", "**", "*.html"), recursive=True):
            s = io.open(f, encoding="utf-8").read()
            if "<!-- livret:debut -->" in s:
                ecrire(f, BLOC_LIVRET.sub("", s))

    # --- la série de podcasts part vide : l'épisode de la démonstration accompagnait son chapitre 1
    serie = os.path.join(sortie, "outils", "podcasts.py")
    if os.path.isfile(serie):
        s = io.open(serie, encoding="utf-8").read()
        neuf = re.sub(r"^EPISODES = \[\n.*?^\]\n", "EPISODES = []\n", s, count=1, flags=re.S | re.M)
        if neuf != s:
            ecrire(serie, neuf)
            print("  outils/podcasts.py : la série part vide — ses épisodes s'y déclarent (module 03)")

    # --- chapitre vitrine conservé comme modèle
    chap = os.path.join(sortie, "site", "chapitres")
    vitrine = os.path.join(chap, "01-cadrage.html")
    modele_src = io.open(vitrine, encoding="utf-8").read() if os.path.isfile(vitrine) else ""
    modele_src = ENCADRE_PODCAST.sub(REPERE_PODCAST if bloc_actif(c, "podcasts") else "", modele_src)
    for f in os.listdir(chap):
        os.remove(os.path.join(chap, f))
    if modele_src:
        ecrire(os.path.join(chap, "_modele.html"), modele_src)
        print("  chapitre vitrine conservé : site/chapitres/_modele.html")

    # --- squelettes de chapitres
    for ch in c["chapitres"]:
        ecrire(os.path.join(chap, ch["fichier"]), squelette_chapitre(c, ch, modele_src))
    print("  %d squelette(s) de chapitre écrit(s)" % len(c["chapitres"]))

    # --- données du cours
    ecrire(os.path.join(sortie, "site", "assets", "js", "course-data.js"), course_data(c))
    print("  course-data.js généré")

    # --- palette et langue sur toutes les pages
    n = 0
    for dossier, _, fichiers in os.walk(os.path.join(sortie, "site")):
        for f in fichiers:
            if not f.endswith(".html"):
                continue
            p = os.path.join(dossier, f)
            t = io.open(p, encoding="utf-8").read()
            avant = t
            t = re.sub(r'data-accent="[a-z]+"', 'data-accent="%s"' % c["palette"], t)
            # Chaque page déclare sa langue, la racine du cours : i18n.js n'y pose pas de bouton 🌐 et n'accepte
            # qu'elle ; navigation.js y chargera le bouton des langues dès qu'une jumelle existera.
            t = re.sub(r'<html lang="[a-z]{2}" data-lang="[a-z]{2}"(?: data-langues="[a-z ]*")?',
                       '<html lang="%s" data-lang="%s" data-langues="%s"' % (langue, langue, langue), t)
            if t != avant:
                io.open(p, "w", encoding="utf-8", newline="\n").write(t)
                n += 1
    print("  %d page(s) mise(s) à la palette « %s »" % (n, c["palette"]))

    # --- purge du contenu de demonstration
    if args.avec_demo:
        print("  contenu de demonstration CONSERVE (--avec-demo)")
    else:
        r, s = purger_demo(sortie, c)
        print("  contenu de demonstration retire : %d media(s), %d fichier(s) "
              "remis a l'etat de squelette" % (r, s))
        if bloc_actif(c, "livret"):
            print("  outils/livret.py : la fiche du polycopié part vide — l'auteur y écrit sa présentation, "
                  "imprimée mot pour mot (module 02)")

    # --- l'identite : titre d'onglet, description, auteur, pied de page
    i = renommer_identite(sortie, c)
    print("  %d page(s) renommee(s) au nom du cours" % i)

    # --- les liens de chapitre : ils pointaient vers la demonstration
    r = recoudre_liens(sortie, c)
    print("  %d fichier(s) recousu(s) sur les chapitres declares" % r)

    # --- le sommaire : ses cartes portent la prose du cours de demonstration
    k = regenerer_sommaire(sortie, c)
    if k:
        print("  cours.html : %d carte(s) de chapitre regeneree(s)" % k)

    # --- un cours qui n'a pas le français ET l'anglais ne promet pas des fiches « français et anglais »
    if not ("fr" in c["langues"] and "en" in c["langues"]):
        for f in glob.glob(os.path.join(sortie, "site", "**", "*.html"), recursive=True):
            t = io.open(f, encoding="utf-8").read()
            neuf = t.replace(" · PDF · français et anglais", " · PDF").replace(" · PDF · French and English", " · PDF")
            if neuf != t:
                ecrire(f, neuf)

    # --- le menu : les sections des chapitres du cours, lues dans leurs <h2 id>. Sans cela, le cours gardait
    #     dans son menu les sections du cours de démonstration (nav-sections.js n'était produit par aucun outil).
    spec = importlib.util.spec_from_file_location("generer_nav_sections",
                                                  os.path.join(RACINE, "outils", "generer_nav_sections.py"))
    gns = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gns)
    _a_jour, nch, nsec = gns.generer(sortie)
    print("  nav-sections.js régénéré : %d chapitre(s), %d section(s)" % (nch, nsec))

    # --- les filières : filieres.css suit celles que course_data() a écrites d'après cours.json (aucune règle sans
    #     deux filières) ; celui de la démonstration masquait ses filières EADL et ERIS.
    r = subprocess.run([sys.executable, os.path.join(sortie, "outils", "generer_filieres.py")],
                       capture_output=True, text=True, encoding="utf-8")
    print("  %s" % ((r.stdout.strip().splitlines() or ["filieres.css : non écrit"])[-1]))

    # --- les médias : la liste de ceux que le cours a vraiment (ceux de la démonstration sont partis avec elle). Celle
    #     de la démonstration ferait demander au serveur des fichiers absents — une erreur 404 par chapitre.
    spec = importlib.util.spec_from_file_location("generer_medias", os.path.join(RACINE, "outils", "generer_medias.py"))
    gm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gm)
    _a_jour, nombres = gm.generer(sortie)
    print("  media-data.js régénéré : %s" % ", ".join("%s %d" % (cle, n) for cle, n in nombres.items()))

    # --- les fragments : le référentiel du cours part vide (celui de la démonstration portait ses durées), et les
    #     pages reçoivent les valeurs du cours — son vrai nombre de chapitres, « … » pour une durée à renseigner.
    ecrire(os.path.join(sortie, "outils", "referentiel.py"), referentiel_vide())
    r = subprocess.run([sys.executable, os.path.join(sortie, "outils", "generer_fragments.py")],
                       capture_output=True, text=True, encoding="utf-8")
    manques = r.stdout.count("✗")
    print("  fragments écrits%s" % (" — %d à renseigner dans outils/referentiel.py (durées des chapitres)" % manques
                                    if manques else ""))

    # --- « Où en parle-t-on ? » : les emplois des termes du glossaire du cours (celui de la démonstration en avait
    #     d'autres). Le générateur se relance après chaque retouche d'une page.
    emplois = os.path.join(sortie, "outils", "glossaire_emplois.py")
    if os.path.isfile(emplois):
        r = subprocess.run([sys.executable, emplois], capture_output=True, text=True, encoding="utf-8")
        print("  %s" % ((r.stdout.strip().splitlines() or ["glossaire-emplois.js : non écrit"])[-1]))

    # --- sources et bibliographie : le mode d'emploi et la bibliographie à remplir,
    #     jamais les documents d'un autre cours, restés sous droits dans sources/
    src_dir = os.path.join(sortie, "sources")
    os.makedirs(src_dir, exist_ok=True)
    for nom in ("README.md", "bibliographie.md"):
        if not os.path.isfile(os.path.join(src_dir, nom)):
            shutil.copy2(os.path.join(RACINE, "sources", nom), os.path.join(src_dir, nom))
    print("  sources/ prêt — déposez-y vos documents de référence")

    # --- la destination de publication et les secrets locaux
    if os.path.isdir(os.path.join(sortie, "deploiement")):
        ecrire(os.path.join(sortie, "deploiement", "destination.json"), destination_json(c))
        print("  deploiement/destination.json écrit (cours « %s »%s)"
              % (c["slug"], "" if distant else ", répertoire distant à renseigner"))
    for rel, quoi in copier_secrets(sortie, c):
        print("  %-26s %s" % (rel, quoi))

    # --- mémo de démarrage
    ecrire(os.path.join(sortie, "DEMARRER-ICI.md"), memo(c, sortie))
    print("  DEMARRER-ICI.md écrit")

    print("\nEt maintenant\n-------------")
    print("  1. Déposez vos documents de référence dans sources/")
    print("  2. Complétez sources/bibliographie.md")
    print("  3. Ouvrez le dossier avec Claude Code et demandez « créer le cours » :")
    print("     la skill suit prompts/PROMPT-Cours-parametrable.md et ses modules,")
    print("     lit vos sources et vous pose ses questions de cadrage, une à une.")
    print("  4. Pour voir le site : python3 demarrer.py")
    return 0


def memo(c, sortie):
    return """# %s

Cours créé à partir du template, le squelette est en place. Ce fichier dit
quoi faire ensuite ; vous pouvez le supprimer une fois le cours démarré.

## 1. Déposez vos sources

Tout ce sur quoi le cours doit s'appuyer va dans `sources/` : référentiel,
supports existants, articles, normes, notes. **Ce dossier n'est pas versionné** —
vos documents d'ayants droit ne partent pas dans le dépôt. Seules la
bibliographie et le mode d'emploi le sont.

Complétez ensuite `sources/bibliographie.md` : c'est la trace publiable de ce
sur quoi le cours repose.

## 2. Faites le cadrage avec Claude

Ouvrez ce dossier avec Claude Code et demandez-lui de **créer le cours**. La
skill `creer-cours-template` prend la main et suit
`prompts/PROMPT-Cours-parametrable.md` et ses modules (`prompts/modules/`) :
elle lit d'abord vos sources, puis vous pose ses questions **une à une**, et ne
rédige rien tant que le cadrage n'est pas validé.

Règle qu'elle applique et qu'il faut connaître : les documents sont la source
de vérité. Ce qui n'y figure pas est signalé comme lacune, jamais comblé
d'invention. Les autres exigences — dialogue, Git, secrets, audio, quiz,
publication — sont dans `CLAUDE.md`, que Claude lit à chaque ouverture.

## 2 bis. Secrets et publication

- `outils/elevenlabs.json` (clé ElevenLabs et voix) et `deploiement/config.json`
  (accès à l'hébergement) ont été **recopiés tels quels depuis le template**,
  s'ils y étaient. Ils restent locaux, ignorés par Git, et ne s'ouvrent pas.
- `deploiement/destination.json` dit **où ce cours se publie** : identifiant
  `%s`, répertoire distant à vérifier avant le premier envoi. Le déployeur
  refuse d'écrire dans le dossier d'un autre cours.

```
python3 deploiement/deployer.py --essai   # ce qui partirait, garde-fou compris
```

## 2 ter. Audio

Toutes les pistes se génèrent en **Eleven v4**, avec l'accent retenu par
l'auteur. Écoutez **un témoin** avant toute série :

```
python3 outils/generer_audio.py --temoin --limite 1
```

## 3. Le contenu de démonstration a été retiré

Les capsules audio, les schémas, les polycopiés, le QCM, les flashcards et le
glossaire du cours de démonstration **ne sont pas dans ce dossier** : ils
parlaient d'autre chose que de votre sujet. À leur place, des squelettes qui
montrent la forme attendue.

Pour les revoir, le cours de démonstration reste intact dans le template. Et si
vous vouliez les garder, `nouveau_cours.py --avec-demo` les conserve.

## 4. Écrivez les chapitres

Les squelettes sont dans `site/chapitres/`. Le chapitre vitrine du template est
conservé sous `site/chapitres/_modele.html` : c'est le seul endroit où les sept
composants sont appelés pour de vrai, avec le motif bilingue. Copiez depuis là.

## 5. Vérifiez souvent

```
python3 demarrer.py                  # le site, sans cache
python3 outils/verifier_i18n.py      # bilingue cohérent
python3 outils/verifier_contraste.py # palettes lisibles en clair et en sombre
python3 outils/verifier_liens.py     # liens et renvois « Pour approfondir »
```

## Repères

- Titre : %s
- Identifiant : `%s`
- Auteur : %s
- Palette : `%s`
- Langues : %s
- Chapitres déclarés : %d
- Dossier : `%s`
""" % (c["titre"]["fr"], c["slug"], c["titre"]["fr"], c["slug"], c["auteur"], c["palette"],
       " et ".join(c["langues"]), len(c["chapitres"]), sortie)


if __name__ == "__main__":
    sys.exit(main())
