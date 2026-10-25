#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fabrique un nouveau cours à partir de ce template.

    cp cours.exemple.json cours.json      # puis remplissez-le
    python3 nouveau_cours.py              # crée le cours dans le dossier « sortie »

    python3 nouveau_cours.py --essai      # dit ce qu'il ferait, sans rien écrire
    python3 nouveau_cours.py --config autre.json --sortie ../ailleurs
    python3 nouveau_cours.py --ecraser    # accepte un dossier de sortie non vide

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
import importlib.util
import io
import glob
import json
import os
import re
import shutil
import sys

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
NE_PAS_COPIER = shutil.ignore_patterns(
    "__pycache__", "*.pyc", "_tmp*", "elevenlabs.json", "*.config.json", "config.json",
    "manifeste.json", "manifeste.json.tmp", "known_hosts", "destination.json", "quarantaine",
    "acces.json", "acces-zones.json", "Cahier_de_texte*.docx", "out", "settings.local.json")

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

# Pages et dossiers retirés quand le bloc correspondant est à false.
BLOCS = {
    "qcm":                 ["site/QCM"],
    "glossaire":           ["site/glossaire.html", "site/assets/js/glossaire-data.js",
                            "site/assets/js/glossaire-tooltip.js"],
    "flashcards":          ["site/assets/js/flashcards.js", "site/assets/js/flashcards-data.js"],
    "activites":           ["site/activites.html"],
    "polycopies":          ["site/assets/polycopies", "tools/generate_polycopies.py"],
    "atelier":             ["site/atelier", "site/atelier.html"],
    "documents_formateur": ["docs/generate_cahier_de_texte.py",
                            "docs/generate_questions_oral.py"],
    "deploiement":         ["deploiement"],
}


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
    tfr = c["titre"]["fr"]
    bi = "en" in (c.get("langues") or [])
    ten = c["titre"].get("en", tfr) if bi else tfr
    st = c.get("sous_titre") or {}
    sfr = st.get("fr", "")
    sen = st.get("en", sfr)
    auteur = c["auteur"]

    def att(s):
        """Un texte utilisable dans un attribut HTML."""
        return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")

    # Le nom court de l'en-tête et son pictogramme : « Concevoir un cours » et
    # « Ce » restaient en tête de chaque page d'un cours créé. Par défaut, la
    # partie du titre qui précède « : », et ses deux premières lettres.
    court = c.get("titre_court") or {}
    cfr = str(court.get("fr") or tfr.split(" : ")[0]).strip()
    cen = str(court.get("en") or (ten.split(": ")[0] if bi else cfr)).strip()
    logo = str(c.get("logo") or re.sub(r"[\W_]", "", cfr)[:2] or "Co")
    lic = c.get("licence") or {}
    lfr = str(lic.get("fr", "")).strip()
    len_ = str(lic.get("en", lfr)).strip()
    marque = ('<span data-tr="fr">Concevoir un cours</span><span data-tr="en">Design a course</span>',
              '<span data-tr="fr">%s</span><span data-tr="en">%s</span>' % (att(cfr), att(cen)))
    picto = ('<span class="logo-icon">C<span class="acc">e</span></span>',
             '<span class="logo-icon">%s<span class="acc">%s</span></span>' % (att(logo[:1]), att(logo[1:2])))

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

    desc_fr = ("%s. %s" % (tfr, sfr)).strip().strip(".") + "."
    touchees = 0
    for f in sorted(glob.glob(os.path.join(sortie, "site", "**", "*.html"),
                              recursive=True)):
        s = io.open(f, encoding="utf-8").read()
        avant = s

        # La meta-description des chapitres est deja reecrite par le squelette ;
        # celle des autres pages parlait encore de la demonstration.
        if os.sep + "chapitres" + os.sep not in f:
            s = re.sub(r'<meta name="description" content="[^"]*">',
                       '<meta name="description" content="%s">' % att(desc_fr), s)
        s = re.sub(r'<meta name="author" content="[^"]*">',
                   '<meta name="author" content="%s">' % att(auteur), s)

        # Le sous-titre de l'accueil : de la prose propre a la demonstration.
        if sfr:
            s = re.sub(
                r'(<p class="chapter-subtitle">\s*)<span data-tr="fr">.*?</span>\s*'
                r'<span data-tr="en">.*?</span>',
                lambda m: '%s<span data-tr="fr">%s</span>\n          '
                          '<span data-tr="en">%s</span>' % (m.group(1), sfr, sen),
                s, flags=re.S)

        # L'en-tête : nom court et pictogramme du cours.
        s = s.replace(*marque).replace(*picto)

        # Le pied de page : la licence de cours.json, pas celle de la démonstration.
        if lfr:
            s = re.sub(r'<span class="cc-badges">[^<]*</span>',
                       lambda m: '<span class="cc-badges"><span data-tr="fr">%s</span>'
                                 '<span data-tr="en">%s</span></span>' % (att(lfr), att(len_)), s)
            s = re.sub(r'\s*<span data-tr="fr"> Code sous licence MIT, contenu sous licence Creative '
                       r'Commons BY 4\.0\.</span>\s*<span data-tr="en"> Code under MIT license, content '
                       r'under Creative Commons BY 4\.0\.</span>', "", s)

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
        <h4><span data-tr="fr">Page à rédiger</span><span data-tr="en">Page to be written</span></h4>
        <p><span data-tr="fr">%s</span><span data-tr="en">%s</span></p>
      </div>
    </div>"""

# Les pages de démonstration vidées : (fichier, titre fr, titre en, consigne fr, consigne en)
PAGES_DEMO = [
    ("site/atelier.html", "Atelier fil rouge", "Capstone workshop",
     "L'énoncé de l'atelier fil rouge, ses livrables et ses modèles téléchargeables "
     "(prompts/11_atelier_templates.md). Le contenu de démonstration a été retiré ; "
     "l'atelier complet reste consultable dans le template (site/atelier.html).",
     "The capstone workshop brief, its deliverables and downloadable templates "
     "(prompts/11_atelier_templates.md). The demo content has been removed; the full "
     "workshop remains in the template (site/atelier.html)."),
    ("site/activites.html", "Activités interactives", "Interactive activities",
     "Les activités du cours (prompts/05_activites_interactives.md), construites avec les "
     "patrons de assets/js/tools.js. Les exemples de démonstration ont été retirés ; ils "
     "restent dans le template (site/activites.html).",
     "The course activities (prompts/05_activites_interactives.md), built with the patterns "
     "of assets/js/tools.js. The demo examples have been removed; they remain in the "
     "template (site/activites.html)."),
]

SECTION_ACCUEIL = """<section class="content-section">
      <h2><span data-tr="fr">Ce que vous saurez faire</span><span data-tr="en">What you will be able to do</span></h2>
      <p><span data-tr="fr">À rédiger : trois à cinq objectifs du cours, chacun avec un verbe d'action observable.</span><span data-tr="en">To be written: three to five course objectives, each with an observable action verb.</span></p>
    </section>"""


def vider_page(chemin, titre_fr, titre_en, consigne_fr, consigne_en):
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
    s = s[:fin] + "\n\n" + PAGE_A_REDIGER % (consigne_fr, consigne_en) + "\n\n  " + s[fm:]
    s = re.sub(r'(<h1 class="chapter-title">).*?(</h1>)',
               lambda x: '%s<span data-tr="fr">%s</span><span data-tr="en">%s</span>%s'
                         % (x.group(1), titre_fr, titre_en, x.group(2)), s, count=1, flags=re.S)
    # les appels de démonstration ne trouveraient plus leurs conteneurs
    s = re.sub(r'<script>\s*TPLActivities\..*?</script>\s*', "", s, flags=re.S)
    ecrire(chemin, s)
    return True


def recoudre_liens(sortie, c):
    """Fait pointer tous les liens de chapitre vers les chapitres DECLARES.

    Sans cela, l'accueil, le sommaire, l'atelier et la pagination des squelettes
    menaient encore aux chapitres de la demonstration : des liens morts sur les
    pages les plus visitees.
    """
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
    bi = "en" in (c.get("langues") or [])
    qcm = os.path.isfile(os.path.join(sortie, "site", "QCM", "index.html"))

    def h(x):
        return str(x).replace("&", "&amp;").replace("<", "&lt;")

    def deux(fr, en):
        return '<span data-tr="fr">%s</span><span data-tr="en">%s</span>' % (h(fr), h(en if bi else fr))

    for i, ch in enumerate(chaps):
        p = os.path.join(sortie, "site", "chapitres", ch["fichier"])
        if not os.path.isfile(p):
            continue
        s = io.open(p, encoding="utf-8").read()
        avant = chaps[i - 1] if i > 0 else None
        apres = chaps[i + 1] if i + 1 < len(chaps) else None
        prec = avant["fichier"] if avant else "../index.html"
        if apres:
            suiv, titre_suiv = apres["fichier"], deux(apres["titre"]["fr"],
                                                      apres["titre"].get("en") or apres["titre"]["fr"])
        elif qcm:
            suiv, titre_suiv = "../QCM/index.html", deux("QCM d'évaluation", "Assessment quiz")
        else:
            suiv, titre_suiv = "../cours.html", deux("Sommaire du cours", "Course contents")
        entete = ('<nav class="chapter-nav">\n'
                  '      <a href="../cours.html" class="chapter-nav-btn">%s</a>\n' % deux("← Sommaire", "← Contents")
                  + ('      <a href="%s" class="chapter-nav-btn">%s</a>\n' % (prec, deux("← Précédent", "← Previous"))
                     if avant else "")
                  + '      <a href="%s" class="chapter-nav-btn">%s</a>\n    </nav>' % (suiv, deux("Suivant →", "Next →")))
        pied = ('<nav class="chapter-pagination">\n'
                '      <a href="%s" class="pagination-link prev">\n'
                '        <span class="pagination-label">%s</span>\n' % (
                    prec, deux("← Précédent", "← Previous") if avant else deux("← Accueil", "← Home"))
                + ('        <span class="pagination-title">%s</span>\n'
                   % deux(avant["titre"]["fr"], avant["titre"].get("en") or avant["titre"]["fr"])
                   if avant else "")
                + '      </a>\n'
                  '      <a href="%s" class="pagination-link next">\n'
                  '        <span class="pagination-label">%s</span>\n'
                  '        <span class="pagination-title">%s</span>\n'
                  '      </a>\n    </nav>' % (suiv, deux("Suivant →", "Next →"), titre_suiv))
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


def regenerer_sommaire(sortie, c):
    """Reecrit la grille de chapitres de cours.html depuis les chapitres declares.

    Ces cartes portent une prose propre a chaque chapitre : gardees telles
    quelles, un cours de droit aurait annonce « Cadrer son cours » et renvoye
    vers une page inexistante.
    """
    F = os.path.join(sortie, "site", "cours.html")
    if not os.path.isfile(F):
        return 0
    t = io.open(F, encoding="utf-8").read()
    m = re.search(r'(<div class="concept-grid">)(.*?)(\n\s*</div>\s*\n\s*</section>)',
                  t, re.S)
    if not m:
        return 0

    bi = "en" in (c.get("langues") or [])
    cartes = []
    for ch in c["chapitres"]:
        tfr = ch["titre"]["fr"]
        ten = ch["titre"].get("en", tfr) if bi else tfr
        cartes.append(
            '\n          <div class="concept-card">\n'
            '            <div class="concept-card-header">\n'
            '              <span class="concept-card-emoji">%s</span>\n'
            '              <span class="concept-card-title">'
            '<span data-tr="fr">%s · %s</span>'
            '<span data-tr="en">%s · %s</span></span>\n'
            '            </div>\n'
            '            <p><span data-tr="fr">A rediger : deux lignes qui disent ce que '
            'ce chapitre permet de faire.</span>'
            '<span data-tr="en">To be written: two lines saying what this chapter '
            'enables.</span></p>\n'
            '            <p style="margin-top:.75rem">'
            '<a class="btn btn-primary" href="chapitres/%s">'
            '<span data-tr="fr">Ouvrir le chapitre %s &rarr;</span>'
            '<span data-tr="en">Open chapter %s &rarr;</span></a></p>\n'
            '          </div>\n'
            % (ch.get("ico", "\U0001f4d8"), ch.get("num", ""), tfr,
               ch.get("num", ""), ten, ch["fichier"], ch.get("num", ""), ch.get("num", "")))

    t = t[:m.start(2)] + "".join(cartes) + t[m.end(2):]
    ecrire(F, t)
    return len(cartes)


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
    # et le lien qui y menait, sinon il resterait mort dans chaque pied de page
    for f in glob.glob(os.path.join(sortie, "site", "**", "*.html"), recursive=True):
        s = io.open(f, encoding="utf-8").read()
        if "about.html" not in s:
            continue
        s = re.sub(r' · <a href="[^"]*about\.html">.*?</a>', "", s, flags=re.S)
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

    # la fiche de capsules du cours de demonstration n'a rien a faire ici
    fiche = os.path.join(sortie, "docs", "prompts", "Capsules_du_cours_demo.md")
    if os.path.isfile(fiche):
        os.remove(fiche)
        retires += 1

    # l'accueil presentait les fonctionnalites du template, pas le cours
    acc = os.path.join(sortie, "site", "index.html")
    if os.path.isfile(acc):
        s = io.open(acc, encoding="utf-8").read()
        neuf = re.sub(r'<section class="content-section">\s*<h2><span data-tr="fr">Ce que démontre ce site'
                      r'</span>.*?</section>', lambda m: SECTION_ACCUEIL, s, count=1, flags=re.S)
        if neuf != s:
            ecrire(acc, neuf)
            remplaces += 1

    # l'atelier et les activites de la demonstration
    for rel, tfr, ten, cfr, cen in PAGES_DEMO:
        p = os.path.join(sortie, rel.replace("/", os.sep))
        if os.path.isfile(p) and vider_page(p, tfr, ten, cfr, cen):
            remplaces += 1

    return retires, remplaces


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
        elif bloc and not (c.get("blocs") or {}).get(bloc, True):
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
              "est dans `prompts/PROMPT-Cours-parametrable.md`."
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
    if not langues or langues[0] not in ("fr", "en"):
        griefs.append("« langues » doit commencer par « fr » ou « en ».")
    for l in langues:
        if l not in ("fr", "en"):
            griefs.append("langue non gérée : %r (seuls fr et en le sont)" % l)

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
def course_data(c):
    """Le fichier de données du cours, source unique de la navigation."""
    bi = "en" in (c.get("langues") or [])

    def paire(d, defaut=""):
        fr = (d or {}).get("fr", defaut)
        en = (d or {}).get("en", fr) if bi else fr
        return '{ fr: %s, en: %s }' % (json.dumps(fr, ensure_ascii=False),
                                       json.dumps(en, ensure_ascii=False))

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
        "  chapters: [",
    ]
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
    if b.get("glossaire", True):
        res.append(("📚", "glossaire.html", "Glossaire bilingue", "Bilingual glossary"))
    if b.get("qcm", True):
        res.append(("📝", "QCM/index.html", "QCM d'évaluation", "Assessment quiz"))
    if b.get("polycopies", True):
        res.append(("📄", "polycopies.html", "Polycopiés", "Handouts"))
    if b.get("activites", True):
        res.append(("🧩", "activites.html", "Activités interactives", "Interactive activities"))
    if b.get("atelier", True):
        res.append(("🧵", "atelier.html", "Atelier fil rouge", "Capstone workshop"))
    for ico, href, fr, en in res:
        lignes.append('    { ico: "%s", href: "%s", label: { fr: "%s", en: "%s" } },'
                      % (ico, href, fr, en if bi else fr))
    if lignes[-1].endswith(","):
        lignes[-1] = lignes[-1][:-1]
    lignes += ["  ]", "};", ""]
    return "\n".join(lignes)


PLACEHOLDER = {
    "fr": "À rédiger. Remplacez ce paragraphe par le contenu du chapitre.",
    "en": "To be written. Replace this paragraph with the chapter content.",
}


def vider_prose(t):
    """Remplace le texte des paragraphes et des listes par un repère visible.

    On garde la structure — sections, listes, encadrés, appels de composants —
    et on retire le contenu. Un squelette qui conserverait la prose du chapitre
    vitrine ferait courir un vrai risque : une section oubliée à la relecture
    partirait en ligne en parlant d'autre chose que du cours.
    """
    def remplacer(m):
        lang = m.group(1)
        return '<span data-tr="%s">%s</span>' % (lang, PLACEHOLDER[lang])

    # les objectifs du chapitre : ils sont dans l'en-tete, donc hors de la
    # plage traitee plus bas, et ils portaient les objectifs de la demonstration
    o = t.find('<div class="chapter-objectives">')
    if o > -1:
        of = t.index("</div>", t.index("</ul>", o))
        t = t[:o] + re.sub(r'<span data-tr="(fr|en)">(?:(?!</span>).)*?</span>',
                           remplacer, t[o:of], flags=re.S) + t[of:]

    # uniquement dans le corps, et uniquement les blocs de prose
    debut = t.index("<!-- ============ 1 ============ -->")
    fin = t.index("<nav class=\"chapter-pagination\">")
    corps = t[debut:fin]
    corps = re.sub(r'<span data-tr="(fr|en)">(?:(?!</span>).)*?</span>',
                   remplacer, corps, flags=re.S)

    # Les titres de section : un repère court et numéroté, pas le paragraphe de remplissage — ils s'affichent dans
    # la page et dans le menu (outils/generer_nav_sections.py les y reporte).
    def titre(m):
        titre.n += 1
        return ('<h2%s><span data-tr="fr">%d. Titre de section à rédiger</span>'
                '<span data-tr="en">%d. Section title to be written</span></h2>' % (m.group(1), titre.n, titre.n))
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


def squelette_chapitre(c, ch, modele):
    """Un chapitre vide mais complet : structure, appels de composants, reperes.

    On part du chapitre vitrine plutot que d'un gabarit separe : ainsi le
    squelette ne peut pas diverger du moteur reel, puisqu'il EST le chapitre
    reel, vide de son contenu.
    """
    bi = "en" in (c.get("langues") or [])
    t = modele
    tfr = ch["titre"]["fr"]
    ten = ch["titre"].get("en", tfr) if bi else tfr

    t = t.replace("Chapitre 1 — Cadrer son cours / Scoping your course",
                  "Chapitre %s — %s" % (ch.get("num", ""), tfr))
    t = t.replace('data-accent="marine"', 'data-accent="%s"' % c["palette"])
    t = t.replace(">Cadrer son cours<", ">%s<" % tfr)
    t = t.replace(">Scoping your course<", ">%s<" % ten)
    t = t.replace(">Chapitre 1<", ">Chapitre %s<" % ch.get("num", ""))
    t = t.replace(">Chapter 1<", ">Chapter %s<" % ch.get("num", ""))
    t = t.replace("RDCX.steps({ chapitre: '1' })",
                  "RDCX.steps({ chapitre: '%s' })" % ch.get("num", "1"))

    # La meta-description decrivait le chapitre de demonstration : elle part
    # dans les moteurs de recherche et dans les apercus de partage.
    t = re.sub(r'<meta name="description" content="[^"]*">',
               '<meta name="description" content="Chapitre %s — %s. %s">'
               % (ch.get("num", ""), tfr, c["titre"]["fr"]), t, count=1)

    # Les titres d'etapes et de sommaire sont des ATTRIBUTS, pas des blocs
    # data-tr : le vidage de la prose ne les voit pas.
    def num_section(m):
        num_section.n += 1
        return '%s="Section %d"' % (m.group(1), num_section.n)
    num_section.n = 0
    t = re.sub(r'(data-step-titre)="[^"]*"', num_section, t)
    num_section.n = 0
    t = re.sub(r'(data-sommaire-titre)="[^"]*"', num_section, t)

    # le contenu des composants : les cles restent, les valeurs sont videes
    d = t.index("  var TEXTES = {")
    f = t.index("  function textes()", d)
    t = t[:d] + textes_vides(c) + "\n" + t[f:]

    # la prose des sections
    t = vider_prose(t)

    avert = (
        '\n    <div class="callout warning">\n'
        '      <div class="callout-icon">✏️</div>\n'
        '      <div class="callout-content">\n'
        '        <h4>Chapitre à rédiger</h4>\n'
        '        <p>Ce squelette vient de <code>nouveau_cours.py</code>. Il conserve la\n'
        '        structure et les appels de composants du chapitre vitrine, mais son\n'
        '        contenu est vide : rien de la démonstration ne peut survivre par\n'
        '        inadvertance. L\'exemple entièrement rempli reste consultable dans\n'
        '        <code>chapitres/_modele.html</code>. Supprimez cet encadré une fois le\n'
        '        chapitre écrit.</p>\n'
        '      </div>\n'
        '    </div>\n')
    t = t.replace('    <!-- ============ Médias du chapitre ============ -->',
                  avert + '\n    <!-- ============ Médias du chapitre ============ -->', 1)
    return t


def depouiller_langue(t, garder):
    """Retire les blocs de la langue non retenue, pour un cours monolingue."""
    autre = "en" if garder == "fr" else "fr"
    t = re.sub(r'<span data-tr="%s">.*?</span>' % autre, "", t, flags=re.S)
    t = re.sub(r'\sdata-tr="%s"' % garder, "", t)
    return t


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
    ap.add_argument("--ecraser", action="store_true", help="accepte un dossier non vide")
    ap.add_argument("--avec-demo", action="store_true",
                    help="conserve les medias et le contenu du cours de demonstration")
    args = ap.parse_args()

    c = charger(args.config)
    valider(c)

    sortie = os.path.abspath(os.path.join(RACINE, args.sortie or c.get("sortie", "../cours")))
    bi = "en" in c["langues"]
    langue = c["langues"][0]

    print("\nCours à créer\n-------------")
    print("  titre     : %s" % c["titre"]["fr"])
    print("  slug      : %s" % c["slug"])
    print("  palette   : %s" % c["palette"])
    print("  langues   : %s" % (", ".join(c["langues"]) + ("" if bi else "  (monolingue)")))
    print("  chapitres : %d" % len(c["chapitres"]))
    for ch in c["chapitres"]:
        print("      %-3s %-28s %s" % (ch.get("num", "?"), ch["fichier"], ch["titre"]["fr"][:40]))
    actifs = [k for k, v in (c.get("blocs") or {}).items() if v]
    print("  blocs     : %s" % (", ".join(sorted(actifs)) or "aucun"))
    print("  sortie    : %s" % sortie)
    distant = (c.get("publication") or {}).get("repertoire_distant")
    if (c.get("blocs") or {}).get("deploiement", True):
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
        print("\n  Secrets locaux :")
        for rel, quoi in copier_secrets(sortie, c, essai=True):
            print("      %-26s %s" % (rel, quoi))
        print("\n  Simulation : rien n'a été écrit.")
        return 0

    print("\nCréation\n--------")
    if not os.path.isdir(sortie):
        os.makedirs(sortie)

    for nom in COPIER:
        src = os.path.join(RACINE, nom)
        if not os.path.exists(src):
            continue
        dst = os.path.join(sortie, nom)
        if os.path.isdir(src):
            if os.path.isdir(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst, ignore=NE_PAS_COPIER)
        else:
            shutil.copy2(src, dst)
    print("  arborescence copiée (%d entrées)" % len(COPIER))

    # --- le contrat de travail du cours, lu par Claude à chaque ouverture
    ecrire(os.path.join(sortie, "CLAUDE.md"), contrat_du_cours(c))
    print("  CLAUDE.md écrit : les exigences de l'auteur s'appliquent à ce cours")

    # --- blocs désactivés
    retires = 0
    for cle, chemins in BLOCS.items():
        if (c.get("blocs") or {}).get(cle, True):
            continue
        for rel in chemins:
            p = os.path.join(sortie, rel.replace("/", os.sep))
            if os.path.isdir(p):
                shutil.rmtree(p); retires += 1
            elif os.path.isfile(p):
                os.remove(p); retires += 1
    if retires:
        print("  %d élément(s) retiré(s) pour les blocs désactivés" % retires)

    # --- chapitre vitrine conservé comme modèle
    chap = os.path.join(sortie, "site", "chapitres")
    vitrine = os.path.join(chap, "01-cadrage.html")
    modele_src = io.open(vitrine, encoding="utf-8").read() if os.path.isfile(vitrine) else ""
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
            # Un cours monolingue le déclare sur <html> : i18n.js n'y pose alors pas
            # de bouton de bascule, et n'accepte que cette langue.
            t = re.sub(r'<html lang="[a-z]{2}" data-lang="[a-z]{2}"(?: data-langues="[a-z ]*")?',
                       '<html lang="%s" data-lang="%s"%s'
                       % (langue, langue, "" if bi else ' data-langues="%s"' % langue), t)
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

    # --- cours monolingue : l'autre langue se retire EN DERNIER. Retirée plus tôt,
    #     elle emportait les repères data-tr dont se servent le renommage (sous-titre
    #     de l'accueil et du sommaire), le recousage (boutons « Suivant ») et le
    #     sommaire, qui réécrit ses cartes dans les deux langues : un cours en
    #     français seul gardait la prose de la démonstration et des liens morts.
    if not bi:
        d = 0
        for f in glob.glob(os.path.join(sortie, "site", "**", "*.html"), recursive=True):
            t = io.open(f, encoding="utf-8").read()
            neuf = depouiller_langue(t, langue).replace(" · PDF · français et anglais", " · PDF")
            if neuf != t:
                ecrire(f, neuf)
                d += 1
        print("  %d page(s) dépouillée(s) de la langue non retenue" % d)

    # --- le menu : les sections des chapitres du cours, lues dans leurs <h2 id>. Sans cela, le cours gardait
    #     dans son menu les sections du cours de démonstration (nav-sections.js n'était produit par aucun outil).
    spec = importlib.util.spec_from_file_location("generer_nav_sections",
                                                  os.path.join(RACINE, "outils", "generer_nav_sections.py"))
    gns = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gns)
    _a_jour, nch, nsec = gns.generer(sortie)
    print("  nav-sections.js régénéré : %d chapitre(s), %d section(s)" % (nch, nsec))

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
    print("     la skill suit prompts/PROMPT-Cours-parametrable.md, lit vos sources et")
    print("     vous pose ses questions de cadrage, une à une.")
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
`prompts/PROMPT-Cours-parametrable.md` : elle lit d'abord vos sources, puis
vous pose ses questions **une à une**, et ne rédige rien tant que le cadrage
n'est pas validé.

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
