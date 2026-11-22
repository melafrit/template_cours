# -*- coding: utf-8 -*-
"""Le programme du cours : ses séances, le travail à faire, ses livrables et leurs échéances (le bloc école).

Source unique, décidée par l'auteur le 21 et le 22 novembre 2026 (lot 2), de :
  - le programme et les échéances de l'accueil (fragments programme et echeances, outils/programme.py) ;
  - le cahier de texte Yparéo, avec et sans les identifiants du site ;
  - le classeur d'import de l'application Livrables (sa feuille Séances porte aussi le texte de chaque séance : la
    voie à suivre quand l'auteur n'a pas accès à Yparéo) ;
  - les boutons de l'accueil : le dépôt sur Livrables, les épreuves de chaque filière.

AUCUNE DATE ICI. Le contenu dit « Jour 1 », « Jour 2 » ; les dates réelles et les promotions vivent dans
outils/sessions.py (versionné dans un cours, fictif dans le gabarit public). Une échéance se donne par un jour du
cours et une heure, ou par un repère (« le dimanche qui suit le Jour 2 ») que sessions.py date.

LES LANGUES. Un texte affiché sur le site s'écrit dans chaque langue du cours : {"fr": …, "en": …} (l'arabe
facultatif, le français par défaut). Ce que lisent Yparéo et l'application Livrables est dans la langue de l'école
(ECOLE["langue"]).

Le cours de démonstration (décision de l'auteur du 22 novembre 2026) : deux jours, quatre séances, une version de
travail le Jour 1 (obligatoire, non notée), le QCM noté le Jour 2, le dossier final noté sur la grille des six
critères de l'atelier. Les coefficients reprennent ceux du cours d'étude d'avant-projet.

    python3 outils/seances.py      # contrôle la cohérence (verifier) ; code 1 si un écart
"""
import io
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- l'école
ECOLE = {
    "langue": "fr",            # la langue d'Yparéo et de l'application Livrables
    "format": "2j",            # un seul format : pas de bascule (prompt paramétrable, « formats »)
}
HORAIRES = {"matin": ("09:00", "12:30"), "apres-midi": ("13:30", "17:00")}
MOMENTS = {"matin": {"fr": "matin", "en": "morning"}, "apres-midi": {"fr": "après-midi", "en": "afternoon"}}
LIENS = {"livrables": "https://livrables.elafrit.com/"}

# Les filières qui préparent une épreuve : leur diplôme, leur bloc, leur module, la page de leurs épreuves. Les
# identifiants sont ceux de course-data.js. Vide : le cours ne prépare aucune épreuve d'un bloc (c'est le cas de la
# démonstration). Exemple :
#   "eadl": {"diplome": {"fr": "Master 1 EADL"}, "bloc": {"fr": "Bloc 1"}, "module": "FM04", "epreuve": "EC01",
#            "epreuves": {"url": "https://…", "titre": {"fr": "Épreuves du Bloc 1"}}},
FILIERES = {}

# ---------------------------------------------------------------- les séances
# Une séance est une demi-journée. chapitres : les numéros de course-data.js, chacun placé une fois ; etiquette : le
# nom d'une séance sans chapitre ; atelier : ce que l'atelier y fait avancer ; travail : le travail à faire ;
# echeances : les livrables qu'elle annonce (clés de LIVRABLES).
SEANCES = [
    {"jour": 1, "moment": "matin", "chapitres": [1],
     "atelier": {"fr": "La fiche de cadrage", "en": "The scoping sheet"},
     "travail": {"fr": "Commencer la fiche de cadrage : le public cible, les prérequis, trois à cinq objectifs "
                       "mesurables, le fil rouge.",
                 "en": "Start the scoping sheet: the target audience, the prerequisites, three to five measurable "
                       "learning objectives, the through-line."},
     "echeances": []},
    {"jour": 1, "moment": "apres-midi", "chapitres": [2],
     "atelier": {"fr": "Le plan", "en": "The plan"},
     "travail": {"fr": "Découper le cours en modules et en séquences, avec la durée estimée de chacune.",
                 "en": "Break the course down into modules and sequences, with an estimated duration for each."},
     "echeances": ["travail"]},
    {"jour": 2, "moment": "matin", "chapitres": [3],
     "atelier": {"fr": "Le chapitre rédigé", "en": "The written chapter"},
     "travail": {"fr": "Rédiger un chapitre complet, illustré, avec une accroche et un « à retenir ».",
                 "en": "Write one complete chapter, illustrated, with a hook and a \"key takeaways\" box."},
     "echeances": []},
    {"jour": 2, "moment": "apres-midi", "chapitres": [],
     "etiquette": {"fr": "Atelier et QCM noté", "en": "Workshop and graded quiz"},
     "atelier": {"fr": "Le QCM et le glossaire", "en": "The quiz and the glossary"},
     "travail": {"fr": "Écrire le QCM de cinq questions, chacune avec sa bonne réponse et sa justification, et le "
                       "glossaire de dix termes ; puis passer le QCM noté.",
                 "en": "Write the five-question quiz, each question with its correct answer and its justification, "
                       "and the ten-term glossary; then take the graded quiz."},
     "echeances": ["qcm", "final"]},
]

# ---------------------------------------------------------------- les livrables
# Les types de l'application Livrables (docs/PROMPT-CLASSEUR-IA.md de l'application), et « QCM », que l'application
# accepte pour un livrable qui porte la configuration d'un QCM.
TYPES = ("Dossier / Rapport", "Code source (dépôt Git)", "Présentation (slides)", "Soutenance orale",
         "Maquette / Design", "Vidéo / Démonstration", "Veille / Article", "Cahier des charges", "Exercice / TP",
         "Autre", "QCM")

# Les repères : une échéance hors des jours du cours, que sessions.py date.
REPERES = {"dimanche-suivant": {"apres_jour": 2, "jour_semaine": 6,      # lundi = 0 … dimanche = 6
                                "libelle": {"fr": "le dimanche qui suit le Jour 2",
                                            "en": "the Sunday after Day 2"}}}

# Les livrables, dans l'ordre d'affichage. seance : le numéro (à partir de 1) de la séance qui l'introduit ; quand :
# un jour du cours et une heure, ou un repère et une heure. Une version de travail est obligatoire et non notée
# (décision de l'auteur du 22 novembre 2026) : due, rappelée, signalée manquante, hors de la moyenne.
LIVRABLES = {
    "travail": {
        "titre": {"fr": "Version de travail : fiche de cadrage et plan", "en": "Work version: scoping sheet and plan"},
        "type": "Dossier / Rapport", "seance": 2, "quand": {"jour": 1, "heure": "17:00"},
        "notation": {"notee": False},
    },
    "qcm": {
        "titre": {"fr": "QCM noté", "en": "Graded quiz"},
        "type": "QCM", "seance": 4, "quand": {"jour": 2, "heure": "17:00"},
        "notation": {"notee": True, "note_max": 20, "coef": 1, "mode": "global"},
    },
    "final": {
        "titre": {"fr": "Dossier final : les cinq livrables", "en": "Final folder: the five deliverables"},
        "type": "Dossier / Rapport", "seance": 4, "quand": {"repere": "dimanche-suivant", "heure": "23:59"},
        "notation": {"notee": True, "note_max": 20, "coef": 2, "mode": "grille"},
        # Les six critères de réussite de l'atelier (atelier.html, section 5), dans la langue de l'école.
        "criteres": [
            ("Cohérence", 4, "Le QCM et le chapitre rédigé portent bien sur les objectifs de la fiche de cadrage."),
            ("Objectifs mesurables", 4, "Chaque objectif emploie un verbe d'action observable, pas un « comprendre » "
                                        "flou."),
            ("Complétude", 3, "Les cinq livrables sont présents : cinq questions de QCM, dix termes de glossaire."),
            ("Justesse", 3, "Chaque bonne réponse du QCM est exacte et accompagnée d'une justification."),
            ("Accessibilité", 3, "Titres hiérarchisés, textes alternatifs prévus, langage clair et lisible."),
            ("Motivation", 3, "Une accroche ouvre le chapitre et le fil rouge donne du sens à l'ensemble."),
        ],
    },
}


# ---------------------------------------------------------------- lecture
def texte(d, langue, defaut="fr"):
    """Le texte d'un champ {fr, en, ar} dans la langue, le français à défaut ; une chaîne telle quelle."""
    if isinstance(d, dict):
        return d.get(langue) or d.get(defaut) or next(iter(d.values()), "")
    return d or ""


def chapitres_du_cours():
    """Les numéros des chapitres, dans l'ordre de site/assets/js/course-data.js."""
    src = io.open(os.path.join(RACINE, "site", "assets", "js", "course-data.js"), encoding="utf-8").read()
    bloc = re.search(r"\bchapters\s*:\s*\[(.*?)\n\s*\]", src, re.S)
    return re.findall(r"num:\s*['\"]([^'\"]+)['\"]", bloc.group(1) if bloc else "")


def numero(seance):
    """Le numéro d'une séance (à partir de 1), dans l'ordre de SEANCES."""
    return SEANCES.index(seance) + 1


def seance_du_chapitre(n):
    """La séance qui traite le chapitre n, ou None."""
    for s in SEANCES:
        if int(n) in s.get("chapitres", []):
            return s
    return None


# ---------------------------------------------------------------- contrôle
def verifier():
    """Les écarts de cohérence du programme : une liste de messages, vide si tout va. Un programme vide (un cours qui
    vient d'être créé) n'est pas incohérent : il reste à écrire, et les pages le disent."""
    ecarts = []
    if not SEANCES:
        return ecarts
    chapitres = [int(n) for n in chapitres_du_cours() if str(n).isdigit()]
    places = [c for s in SEANCES for c in s.get("chapitres", [])]
    for c in chapitres:
        if places.count(c) != 1:
            ecarts.append("chapitre %d placé %d fois dans SEANCES (une fois attendue)" % (c, places.count(c)))
    for c in places:
        if c not in chapitres:
            ecarts.append("chapitre %d placé dans SEANCES, absent de course-data.js" % c)
    if places != sorted(places):
        ecarts.append("les chapitres ne suivent pas l'ordre de course-data.js : %s" % places)
    jours = sorted({s["jour"] for s in SEANCES})
    for i, s in enumerate(SEANCES, 1):
        if s.get("moment") not in HORAIRES:
            ecarts.append("séance %d : moment %r inconnu (%s)" % (i, s.get("moment"), ", ".join(HORAIRES)))
        if not s.get("chapitres") and not s.get("etiquette"):
            ecarts.append("séance %d : ni chapitre ni étiquette" % i)
        for e in s.get("echeances", []):
            if e not in LIVRABLES:
                ecarts.append("séance %d : échéance %r absente de LIVRABLES" % (i, e))
    cles = [(s["jour"], s.get("moment")) for s in SEANCES]
    if len(set(cles)) != len(cles):
        ecarts.append("deux séances occupent la même demi-journée")
    for cle, l in LIVRABLES.items():
        if l.get("type") not in TYPES:
            ecarts.append("livrable %s : type %r hors de la liste de l'application" % (cle, l.get("type")))
        if not 1 <= int(l.get("seance") or 0) <= len(SEANCES):
            ecarts.append("livrable %s : séance %r inexistante" % (cle, l.get("seance")))
        q = l.get("quand", {})
        if "repere" in q and q["repere"] not in REPERES:
            ecarts.append("livrable %s : repère %r inconnu" % (cle, q["repere"]))
        if "jour" in q and q["jour"] not in jours:
            ecarts.append("livrable %s : Jour %r hors du cours" % (cle, q["jour"]))
        if "jour" in q and l.get("seance") and q["jour"] < SEANCES[int(l["seance"]) - 1]["jour"]:
            ecarts.append("livrable %s : échéance avant la séance qui l'introduit" % cle)
        if not re.match(r"^\d{2}:\d{2}$", str(q.get("heure", ""))):
            ecarts.append("livrable %s : heure %r (HH:MM attendu)" % (cle, q.get("heure")))
        n = l.get("notation", {})
        if n.get("notee"):
            if not n.get("coef") or n["coef"] <= 0:
                ecarts.append("livrable %s : coefficient strictement positif attendu" % cle)
            if n.get("mode") == "grille":
                cr = l.get("criteres", [])
                if not 4 <= len(cr) <= 6:
                    ecarts.append("livrable %s : %d critères (4 à 6 attendus)" % (cle, len(cr)))
                if sum(p for _c, p, _d in cr) != n.get("note_max"):
                    ecarts.append("livrable %s : les critères totalisent %d, pas %s" % (cle, sum(p for _c, p, _d in cr),
                                                                                       n.get("note_max")))
        for lg, t in (l.get("titre") or {}).items():
            if "—" in t or " – " in t:
                ecarts.append("livrable %s : tiret cadratin dans le titre (%s) ; un titre déjà importé ne se "
                              "corrige plus" % (cle, lg))
    annonces = [e for s in SEANCES for e in s.get("echeances", [])]
    for cle in LIVRABLES:
        if annonces.count(cle) != 1:
            ecarts.append("livrable %s annoncé par %d séance(s) (une attendue)" % (cle, annonces.count(cle)))
    return ecarts


if __name__ == "__main__":
    for flux in (sys.stdout, sys.stderr):
        try:
            flux.reconfigure(encoding="utf-8")
        except Exception:
            pass
    e = verifier()
    for m in e:
        print("  ✗", m)
    print("Programme : %d séance(s), %d livrable(s), %s" % (len(SEANCES), len(LIVRABLES),
                                                            "cohérent" if not e else "%d écart(s)" % len(e)))
    sys.exit(1 if e else 0)
