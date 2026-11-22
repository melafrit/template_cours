# -*- coding: utf-8 -*-
"""Les sessions du cours : les dates réelles de ses jours, et la promotion de chaque session.

Les seules dates du dépôt (décision de l'auteur du 22 novembre 2026, lot 2). Le contenu des pages dit « Jour 1 » ;
le cahier de texte Yparéo (outils/generer_cahier_de_texte.py) et le classeur d'import Livrables lisent ici les dates.
Ce fichier se versionne dans un cours, dont le dépôt est privé ; dans le gabarit public, les dates de la
démonstration sont fictives.

Une session : la date de chacun de ses jours (« AAAA-MM-JJ », un par jour de outils/seances.py), sa promotion telle
que l'application Livrables la nomme (« Année › Promotion ») et la matière (nom, code, couleur, volume horaire).

    python3 outils/sessions.py      # contrôle les dates ; code 1 si un écart
"""
import datetime
import importlib.util
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SESSIONS = {
    "demo": {
        "jours": {1: "2027-01-11", 2: "2027-01-12"},          # fictives : un lundi et le mardi qui suit
        "promotion": "2026-2027 › Démonstration du gabarit",
        "matiere": {"nom": "Concevoir un cours en ligne", "code": "DEMO", "couleur": "#1b3a5b", "volume_horaire": 14},
    },
}
SESSION_PAR_DEFAUT = "demo"


def _seances():
    spec = importlib.util.spec_from_file_location("seances", os.path.join(RACINE, "outils", "seances.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def session(nom=None):
    """La session nom (celle par défaut sinon) ; KeyError si elle n'existe pas."""
    nom = nom or SESSION_PAR_DEFAUT
    if nom not in SESSIONS:
        raise KeyError("session %r inconnue (sessions : %s)" % (nom, ", ".join(SESSIONS) or "aucune"))
    return SESSIONS[nom]


def date_du_jour(s, jour):
    """La date (datetime.date) du Jour jour de la session s."""
    return datetime.date.fromisoformat(s["jours"][jour])


def date_du_repere(s, repere):
    """La date d'un repère de seances.REPERES : le premier jour de la semaine voulu après le jour donné."""
    d = date_du_jour(s, repere["apres_jour"]) + datetime.timedelta(days=1)
    while d.weekday() != repere["jour_semaine"]:
        d += datetime.timedelta(days=1)
    return d


def verifier():
    """Les écarts des sessions : une liste de messages, vide si tout va."""
    ecarts = []
    jours = sorted({s["jour"] for s in _seances().SEANCES})
    if SESSION_PAR_DEFAUT and SESSION_PAR_DEFAUT not in SESSIONS:
        ecarts.append("SESSION_PAR_DEFAUT %r absente de SESSIONS" % SESSION_PAR_DEFAUT)
    for nom, s in SESSIONS.items():
        dates = []
        for j in jours:
            if j not in s.get("jours", {}):
                ecarts.append("session %s : pas de date pour le Jour %d" % (nom, j))
                continue
            try:
                d = date_du_jour(s, j)
            except ValueError:
                ecarts.append("session %s : date du Jour %d illisible (%r, AAAA-MM-JJ attendu)" % (nom, j, s["jours"][j]))
                continue
            if d.weekday() >= 5:
                ecarts.append("session %s : le Jour %d tombe un %s" % (nom, j, ("samedi", "dimanche")[d.weekday() - 5]))
            dates.append(d)
        if dates != sorted(dates) or len(set(dates)) != len(dates):
            ecarts.append("session %s : les dates des jours ne se suivent pas" % nom)
        if not re.match(r"^\S.* › \S.*$", s.get("promotion", "")):
            ecarts.append("session %s : promotion %r (« Année › Promotion » attendu)" % (nom, s.get("promotion")))
        m = s.get("matiere", {})
        if not m.get("nom") or not re.match(r"^#[0-9a-fA-F]{6}$", m.get("couleur", "")):
            ecarts.append("session %s : matière sans nom, ou couleur hors du format #rrggbb" % nom)
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
    print("Sessions : %d, %s" % (len(SESSIONS), "cohérentes" if not e else "%d écart(s)" % len(e)))
    sys.exit(1 if e else 0)
