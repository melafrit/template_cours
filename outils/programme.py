# -*- coding: utf-8 -*-
"""Le programme et les échéances de l'accueil, écrits d'après outils/seances.py.

outils/generer_fragments.py écrit ces deux fragments dans la langue de chaque page :

    <!-- FRAGMENT:programme -->…<!-- /FRAGMENT:programme -->    une ligne par séance : jour, moment, horaires ;
                                                                les chapitres (titres et liens de course-data.js),
                                                                l'atelier et le travail ; ce qu'il faut rendre
    <!-- FRAGMENT:echeances -->…<!-- /FRAGMENT:echeances -->    une ligne par livrable : son échéance, sa notation
    duree-cours, nb-seances, nb-seances-lettres                  la durée du cours en jours (« 2 jours »), le nombre de
                                                                séances, en chiffres ou en lettres (carte « Durée »)

Le programme vit sur l'accueil (décision de l'auteur du 22 novembre 2026) : dans « Le parcours », sous les cartes des
chapitres, et les échéances dans « Ce que vous produisez ». Aucune date réelle : « Jour 1 », « le dimanche qui suit le
Jour 2 ». Une page française reçoit les espaces insécables de sa typographie.
"""
import html
import importlib.util
import os
import re

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRAGMENT = re.compile(r"^(programme|echeances|duree-cours|nb-seances|nb-seances-lettres)$")
INDENT = "      "
NB = " "

LIBELLES = {
    "fr": {"jour": "Jour %s", "seance": "Séance", "programme": "Au programme", "rendre": "À rendre",
           "chapitre": "Chapitre %s", "atelier": "Atelier", "rien": "Rien à rendre", "a": "à",
           "legende": "Le programme, séance par séance", "livrable": "Livrable", "echeance": "Échéance",
           "notation": "Notation", "legende_ech": "Les échéances", "non_notee": "Obligatoire, non notée",
           "coef": "Coefficient %s, sur %s", "grille": ", grille de %d critères", "le": "%s, à %s",
           "a_rediger": "À rédiger dans outils/seances.py : les séances, le travail à faire, les livrables et leurs "
                        "échéances."},
    "en": {"jour": "Day %s", "seance": "Session", "programme": "On the agenda", "rendre": "Due",
           "chapitre": "Chapter %s", "atelier": "Workshop", "rien": "Nothing due", "a": "at",
           "legende": "The schedule, session by session", "livrable": "Deliverable", "echeance": "Deadline",
           "notation": "Grading", "legende_ech": "Deadlines", "non_notee": "Required, not graded",
           "coef": "Weight %s, out of %s", "grille": ", rubric of %d criteria", "le": "%s, at %s",
           "a_rediger": "To be written in outils/seances.py: the sessions, the work to do, the deliverables and their "
                        "deadlines."},
}
ICONES = {"matin": "☀️", "apres-midi": "🌇"}


def _module(nom):
    spec = importlib.util.spec_from_file_location(nom, os.path.join(RACINE, "outils", nom + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def libelle(langue, cle):
    return LIBELLES.get(langue, LIBELLES["fr"])[cle]


def t(s):
    return html.escape(s, quote=False)


def typo_fr(s):
    """Les espaces insécables du français : avant : ; ? ! et dans « »."""
    s = re.sub(r" ([:;?!])", NB + r"\1", s)
    return s.replace("« ", "«" + NB).replace(" »", NB + "»")


def heure(hhmm, langue):
    """« 09:00 » : « 9 h 00 » en français, « 9:00 » ailleurs."""
    h, m = hhmm.split(":")
    return ("%d%sh%s%s" % (int(h), NB, NB, m)) if langue == "fr" else "%d:%s" % (int(h), m)


def quand(l, S, langue):
    """L'échéance d'un livrable, en toutes lettres : « Jour 1 à 17 h 00 », « Le dimanche qui suit le Jour 2, à 23 h 59 »."""
    q = l["quand"]
    if "repere" in q:
        lib = S.texte(S.REPERES[q["repere"]]["libelle"], langue)
        return libelle(langue, "le") % (lib[:1].upper() + lib[1:], heure(q["heure"], langue))
    return "%s %s %s" % (libelle(langue, "jour") % q["jour"], libelle(langue, "a"), heure(q["heure"], langue))


def notation(l, langue):
    n = l.get("notation", {})
    if not n.get("notee"):
        return libelle(langue, "non_notee")
    s = libelle(langue, "coef") % (n["coef"], n["note_max"])
    if n.get("mode") == "grille":
        s += libelle(langue, "grille") % len(l.get("criteres", []))
    return s


def programme(langue, page):
    S, A = _module("seances"), _module("accueil")
    rac = A.racine()
    chapitres = {num: (fichier, titres) for num, _ico, fichier, titres in A.chapitres()}
    L = lambda cle: libelle(langue, cle)
    lignes = ['<div class="schedule-wrap programme-wrap" role="region" aria-label="%s" tabindex="0">' % t(L("legende")),
              '<table class="schedule programme">',
              '  <caption class="sr-only">%s</caption>' % t(L("legende")),
              '  <thead><tr><th scope="col">%s</th><th scope="col">%s</th><th scope="col">%s</th></tr></thead>'
              % (L("seance"), L("programme"), L("rendre")),
              "  <tbody>"]
    for s in S.SEANCES:
        debut, fin = S.HORAIRES[s["moment"]]
        jour = ('<th scope="row" data-label="%s"><div class="dj-cell">' % L("seance") + '<div class="dj-icon" aria-hidden="true">%s</div><div>'
                '<div class="dj-tag">%s</div><div class="dj-num">%s</div><div class="horaire">%s</div></div></div></th>'
                % (ICONES.get(s["moment"], ""), L("jour") % s["jour"], t(S.texte(S.MOMENTS[s["moment"]], langue)),
                   "%s %s %s" % (heure(debut, langue), "à" if langue == "fr" else "to", heure(fin, langue))))
        quoi = []
        for n in s.get("chapitres", []):
            fichier, titres = chapitres.get(str(n), (None, {}))
            if not fichier:
                continue
            chemin, lg = A.cible("chapitres/" + fichier, langue, rac)
            titre = titres.get(langue) or titres.get(rac) or titres.get("fr", "")
            quoi.append('<p class="title-cell"><a href="%s"%s>%s · %s</a></p>'
                        % (A.lien(chemin, page), ' hreflang="%s"' % lg if lg != langue else "",
                           L("chapitre") % n, t(titre)))
        if s.get("etiquette"):
            quoi.append('<p class="title-cell">%s</p>' % t(S.texte(s["etiquette"], langue)))
        if s.get("atelier"):
            quoi.append("<p><strong>%s :</strong> %s</p>" % (L("atelier"), t(S.texte(s["atelier"], langue))))
        if s.get("travail"):
            quoi.append("<p>%s</p>" % t(S.texte(s["travail"], langue)))
        rendre = ['<p><span aria-hidden="true">📤</span> <strong>%s</strong><br>%s</p>'
                  % (t(S.texte(S.LIVRABLES[e]["titre"], langue)), t(quand(S.LIVRABLES[e], S, langue)))
                  for e in s.get("echeances", [])] or ['<p class="text-muted">%s</p>' % L("rien")]
        lignes.append("    <tr>%s<td class=\"content-cell\" data-label=\"%s\">%s</td>"
                      "<td class=\"content-cell\" data-label=\"%s\">%s</td></tr>"
                      % (jour, L("programme"), "".join(quoi), L("rendre"), "".join(rendre)))
    lignes += ["  </tbody>", "</table>", "</div>"]
    return lignes


def echeances(langue):
    S = _module("seances")
    L = lambda cle: libelle(langue, cle)
    lignes = ['<div class="schedule-wrap" role="region" aria-label="%s" tabindex="0">' % t(L("legende_ech")),
              '<table class="content-table echeances">',
              '  <caption class="sr-only">%s</caption>' % t(L("legende_ech")),
              '  <thead><tr><th scope="col">%s</th><th scope="col">%s</th><th scope="col">%s</th></tr></thead>'
              % (L("livrable"), L("echeance"), L("notation")),
              "  <tbody>"]
    for l in S.LIVRABLES.values():
        lignes.append("    <tr><td>%s</td><td>%s</td><td>%s</td></tr>"
                      % (t(S.texte(l["titre"], langue)), t(quand(l, S, langue)), t(notation(l, langue))))
    lignes += ["  </tbody>", "</table>", "</div>"]
    return lignes


JOURS = {"fr": ("jour", "jours"), "en": ("day", "days")}


def rendre(nom, langue, page, en_lettres=None, **_):
    """Le contenu du fragment nom, dans la langue, pour la page page (chemin depuis la racine du site)."""
    if nom in ("duree-cours", "nb-seances", "nb-seances-lettres"):
        S = _module("seances")
        if not S.SEANCES:
            raise KeyError("outils/seances.py n'a encore aucune séance")
        if nom == "duree-cours":
            n = len({s["jour"] for s in S.SEANCES})
            un, plusieurs = JOURS.get(langue, JOURS["fr"])
            return "%d%s%s" % (n, NB, un if n == 1 else plusieurs)
        n = len(S.SEANCES)
        return en_lettres(n, langue) if nom == "nb-seances-lettres" and en_lettres else str(n)
    if not _module("seances").SEANCES:
        # Un cours qui vient d'être créé : la place est prête, le programme reste à écrire.
        lignes = ['<p class="callout-a-rediger">%s</p>' % t(libelle(langue, "a_rediger"))]
    elif nom == "programme":
        lignes = programme(langue, page)
    elif nom == "echeances":
        lignes = echeances(langue)
    else:
        raise KeyError(nom)
    corps = "\n" + "\n".join(INDENT + l for l in lignes) + "\n" + INDENT
    return typo_fr(corps) if langue == "fr" else corps
