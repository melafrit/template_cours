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
import io
import json
import os
import re
import shutil
import sys

RACINE = os.path.dirname(os.path.abspath(__file__))
CONFIG_DEFAUT = os.path.join(RACINE, "cours.json")
MODELE = os.path.join(RACINE, "cours.exemple.json")

PALETTES = ("marine", "emeraude", "prune", "ardoise", "bordeaux")

# Ce qui est copié tel quel dans le nouveau cours.
COPIER = ["site", "outils", "prompts", "docs", ".claude",
          "demarrer.py", "demarrer.bat", "demarrer.command",
          ".gitattributes", ".gitignore", ".editorconfig",
          "LICENSE", "LICENSE-CONTENT.md"]

# Pages et dossiers retirés quand le bloc correspondant est à false.
BLOCS = {
    "qcm":                 ["site/QCM"],
    "glossaire":           ["site/glossaire.html", "site/assets/js/glossaire-data.js",
                            "site/assets/js/glossaire-tooltip.js"],
    "flashcards":          ["site/assets/js/flashcards.js", "site/assets/js/flashcards-data.js"],
    "polycopies":          ["site/assets/polycopies", "tools/generate_polycopies.py"],
    "atelier":             ["site/atelier", "site/atelier.html"],
    "documents_formateur": ["docs/generate_cahier_de_texte.py",
                            "docs/generate_questions_oral.py"],
    "deploiement":         ["deploiement"],
}


# Contenu de DEMONSTRATION, retire de tout cours cree — sauf --avec-demo.
# Le squelette de chapitre etait deja vide ; ces fichiers-la ne l'etaient pas.
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

    return retires, remplaces


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
      schemaLegende: "Schema 1 — ce qu'il montre et ce qu'il faut en retenir."
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
      schemaLegende: "Diagram 1 — what it shows and what to take from it."
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

    if os.path.isdir(sortie) and os.listdir(sortie) and not args.ecraser:
        sys.exit("\n  Le dossier de sortie n'est pas vide : %s\n"
                 "  Relancez avec --ecraser si c'est voulu." % sortie)

    if args.essai:
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
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        else:
            shutil.copy2(src, dst)
    print("  arborescence copiée (%d entrées)" % len(COPIER))

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
        t = squelette_chapitre(c, ch, modele_src)
        if not bi:
            t = depouiller_langue(t, langue)
        ecrire(os.path.join(chap, ch["fichier"]), t)
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
            t = re.sub(r'<html lang="[a-z]{2}" data-lang="[a-z]{2}"',
                       '<html lang="%s" data-lang="%s"' % (langue, langue), t)
            if not bi:
                t = depouiller_langue(t, langue)
            if t != avant:
                io.open(p, "w", encoding="utf-8", newline="\n").write(t)
                n += 1
    print("  %d page(s) mise(s) à la palette « %s »%s"
          % (n, c["palette"], "" if bi else " et dépouillée(s) de l'anglais"))

    # --- purge du contenu de demonstration
    if args.avec_demo:
        print("  contenu de demonstration CONSERVE (--avec-demo)")
    else:
        r, s = purger_demo(sortie, c)
        print("  contenu de demonstration retire : %d media(s), %d fichier(s) "
              "remis a l'etat de squelette" % (r, s))

    # --- sources et bibliographie
    src_dir = os.path.join(sortie, "sources")
    if not os.path.isdir(src_dir):
        shutil.copytree(os.path.join(RACINE, "sources"), src_dir)
    print("  sources/ prêt — déposez-y vos documents de référence")

    # --- mémo de démarrage
    ecrire(os.path.join(sortie, "DEMARRER-ICI.md"), memo(c, sortie))
    print("  DEMARRER-ICI.md écrit")

    print("\nEt maintenant\n-------------")
    print("  1. Déposez vos documents de référence dans sources/")
    print("  2. Complétez sources/bibliographie.md")
    print("  3. Ouvrez le dossier avec Claude Code et demandez « créer le cours » :")
    print("     la skill lira vos sources et vous posera ses questions de cadrage.")
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
skill `creer-cours-template` prend la main : elle lit d'abord vos sources, puis
vous pose ses questions **une à une**, et ne rédige rien tant que le cadrage
n'est pas validé.

Règle qu'elle applique et qu'il faut connaître : les documents sont la source
de vérité. Ce qui n'y figure pas est signalé comme lacune, jamais comblé
d'invention.

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
```

## Repères

- Titre : %s
- Auteur : %s
- Palette : `%s`
- Langues : %s
- Chapitres déclarés : %d
- Dossier : `%s`
""" % (c["titre"]["fr"], c["titre"]["fr"], c["auteur"], c["palette"],
       " et ".join(c["langues"]), len(c["chapitres"]), sortie)


if __name__ == "__main__":
    sys.exit(main())
