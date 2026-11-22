#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Le cahier de texte Yparéo du cours, d'après outils/seances.py et outils/sessions.py.

    python3 outils/generer_cahier_de_texte.py                  # la session par défaut
    python3 outils/generer_cahier_de_texte.py --session demo
    python3 outils/generer_cahier_de_texte.py --essai          # dit ce qui changerait ; code 1 si un cahier est périmé

Un bloc par séance : la ligne de la séance (jour, date, moment, horaires), ses chapitres, puis CONTENU DE LA SÉANCE
(le sous-titre et les objectifs de chaque chapitre, lus dans sa page ; l'atelier) et TRAVAIL À FAIRE (le travail, ce
qu'il faut rendre et quand, le support). Dans Yparéo, chaque bloc se copie dans le champ du même nom. Sans accès à
Yparéo, le même texte part dans l'application Livrables : la feuille Séances du classeur d'import le reprend
(colonne Contenu), par texte_seance().

« Avec ou sans accès » (décision de l'auteur du 22 novembre 2026) : les deux. La version sans identifiants sort
toujours ; celle qui porte les identifiants du site sort aussi quand docs/acces.json existe (jamais lu à l'écran,
jamais versionné), dans un fichier que le .gitignore et le .rgignore écartent :

    docs/Cahier_de_texte.txt, .docx                              sans identifiants
    docs/Cahier_de_texte_avec_identifiants.txt, .docx            avec, si docs/acces.json existe

Le texte est en UTF-8, en fins de ligne Windows (le Bloc-notes et le copier-coller dans Yparéo), avec les espaces
insécables du français ; ni tiret cadratin ni date dans le contenu du site, les dates ne vivant qu'ici. Un fichier
n'est réécrit que si son contenu change (le Word est comparé sans ses métadonnées de date).
"""
import argparse
import datetime
import html
import importlib.util
import io
import json
import os
import re
import sys
import zipfile

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(RACINE, "site")
NB = " "
TRAIT = "─" * 72
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre",
        "décembre"]
JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]

for flux in (sys.stdout, sys.stderr):
    try:
        flux.reconfigure(encoding="utf-8")
    except Exception:
        pass


def module(nom):
    spec = importlib.util.spec_from_file_location(nom, os.path.join(RACINE, "outils", nom + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# ---------------------------------------------------------------- lecture des sources
def typo(s):
    """Les espaces insécables du français : avant : ; ? ! et dans « »."""
    s = re.sub(r" ([:;?!])", NB + r"\1", s)
    return s.replace("« ", "«" + NB).replace(" »", NB + "»")


def date_longue(d):
    return "%s %d %s %d" % (JOURS[d.weekday()], d.day, MOIS[d.month - 1], d.year)


def heure(hhmm):
    h, m = hhmm.split(":")
    return "%d%sh%s%s" % (int(h), NB, NB, m)


def texte_page(fragment):
    """Le texte brut d'un morceau de page : sans balises ni commentaires, espaces réduits."""
    sans = re.sub(r"<!--.*?-->", "", fragment, flags=re.S)
    return " ".join(html.unescape(re.sub(r"<[^>]+>", "", sans)).split())


def chapitre(fichier):
    """(sous-titre, [objectifs]) de la page d'un chapitre, dans la langue racine."""
    t = io.open(os.path.join(SITE, "chapitres", fichier), encoding="utf-8").read()
    st = re.search(r'<p class="chapter-subtitle">(.*?)</p>', t, re.S)
    obj = re.search(r'<div class="chapter-objectives">.*?<ul>(.*?)</ul>', t, re.S)
    objectifs = [texte_page(li) for li in re.findall(r"<li>(.*?)</li>", obj.group(1), re.S)] if obj else []
    return (texte_page(st.group(1)) if st else ""), objectifs


def adresse_du_site():
    """L'adresse publique du cours (deploiement/destination.json, « url ») ; vide si elle n'est pas connue."""
    p = os.path.join(RACINE, "deploiement", "destination.json")
    if not os.path.isfile(p):
        return ""
    try:
        return str(json.load(io.open(p, encoding="utf-8")).get("url") or "")
    except ValueError:
        return ""


def lire_acces():
    """Les identifiants du site (docs/acces.json), ou None. Jamais affichés : ils ne vont que dans le fichier écarté."""
    p = os.path.join(RACINE, "docs", "acces.json")
    if not os.path.isfile(p):
        return None
    d = json.load(io.open(p, encoding="utf-8"))
    return d if d.get("login") and d.get("motdepasse") else None


# ---------------------------------------------------------------- composition (sans python-docx)
def contexte(nom_session=None):
    S, SE, A = module("seances"), module("sessions"), module("accueil")
    s = SE.session(nom_session)
    langue = S.ECOLE.get("langue", "fr")
    titres = {num: (fichier, t.get(langue) or t.get("fr", "")) for num, _i, fichier, t in A.chapitres()}
    src = io.open(os.path.join(SITE, "assets", "js", "course-data.js"), encoding="utf-8").read()
    auteur = re.search(r"\bauthor:\s*[\"']([^\"']+)[\"']", src)
    return {"S": S, "SE": SE, "s": s, "nom": nom_session or SE.SESSION_PAR_DEFAUT, "langue": langue,
            "titres": titres, "auteur": auteur.group(1) if auteur else "", "site": adresse_du_site()}


def echeance(l, c):
    """« le lundi 11 janvier 2027 à 17 h 00 » : la date réelle d'un livrable, d'après sa session."""
    q, S, SE = l["quand"], c["S"], c["SE"]
    d = SE.date_du_repere(c["s"], S.REPERES[q["repere"]]) if "repere" in q else SE.date_du_jour(c["s"], q["jour"])
    return "le %s à %s" % (date_longue(d), heure(q["heure"]))


def texte_seance(i, c, acces=None):
    """Le bloc d'une séance (i, à partir de 1) : (entête, [chapitres], contenu, travail), en lignes de texte."""
    S, s = c["S"], c["S"].SEANCES[i - 1]
    debut, fin = S.HORAIRES[s["moment"]]
    d = c["SE"].date_du_jour(c["s"], s["jour"])
    entete = "Jour %d · %s · %s, de %s à %s · séance %d sur %d" % (
        s["jour"], date_longue(d), S.texte(S.MOMENTS[s["moment"]], c["langue"]), heure(debut), heure(fin), i,
        len(S.SEANCES))
    tetes, contenu = [], []
    for n in s.get("chapitres", []):
        fichier, titre = c["titres"].get(str(n), ("", ""))
        tetes.append("Chapitre %d · %s" % (n, titre))
        if fichier:
            resume, objectifs = chapitre(fichier)
            if resume:
                contenu.append(resume)
            if objectifs:
                contenu.append("Objectifs du chapitre %d :" % n)
                contenu += ["- " + o for o in objectifs]
    if s.get("etiquette"):
        tetes.append(S.texte(s["etiquette"], c["langue"]))
    if s.get("atelier"):
        atelier = S.texte(s["atelier"], c["langue"]).rstrip(".")
        # La seule première lettre : lower() sur toute la phrase écrivait « le qcm ».
        contenu.append("Atelier : %s." % (atelier[:1].lower() + atelier[1:]))
    travail = []
    if s.get("travail"):
        travail.append(S.texte(s["travail"], c["langue"]))
    for e in s.get("echeances", []):
        l = S.LIVRABLES[e]
        travail.append("%s, à rendre %s sur l'application Livrables (%s)." % (
            S.texte(l["titre"], c["langue"]), echeance(l, c), S.LIENS.get("livrables", "")))
    if not s.get("echeances"):
        travail.append("Rien à rendre pour cette séance.")
    site = c["site"] or "l'adresse communiquée en séance"
    if acces:
        travail.append("Support : le site du cours, %s, identifiant %s, mot de passe %s." % (
            acces.get("site") or site, acces["login"], acces["motdepasse"]))
    else:
        travail.append("Support : le site du cours, %s, %s." % (
            site, "identifiants communiqués en séance" if lire_acces() else "en accès libre"))
    return entete, tetes, contenu, travail


def texte_cahier(c, acces=None):
    """Le cahier entier, en texte : l'en-tête et un bloc par séance."""
    S, s = c["S"], c["s"]
    jours = sorted(s["jours"])
    premier, dernier = c["SE"].date_du_jour(s, jours[0]), c["SE"].date_du_jour(s, jours[-1])
    lignes = ["Cahier de texte · %s" % s["matiere"]["nom"],
              "Promotion %s · session %s · %d séances, du %s au %s" % (
                  s["promotion"], c["nom"], len(S.SEANCES), date_longue(premier), date_longue(dernier)),
              "Formateur : %s" % c["auteur"],
              "Mode d'emploi. Pour chaque séance, copiez le bloc CONTENU DE LA SÉANCE dans le champ Contenu d'Yparéo, "
              "et le bloc TRAVAIL À FAIRE dans le champ Travail à faire. Sans accès à Yparéo, le même texte part dans "
              "l'application Livrables, par le classeur d'import (feuille Séances, colonne Contenu).",
              "Généré par outils/generer_cahier_de_texte.py d'après outils/seances.py et outils/sessions.py : ne pas le "
              "modifier à la main."]
    for i in range(1, len(S.SEANCES) + 1):
        entete, tetes, contenu, travail = texte_seance(i, c, acces)
        lignes += ["", TRAIT, entete] + tetes + ["", "CONTENU DE LA SÉANCE"] + contenu + ["", "TRAVAIL À FAIRE"] + travail
    return typo("\n".join(lignes)) + "\n"


# ---------------------------------------------------------------- le Word
def docx_cahier(c, acces=None):
    """Le cahier en Word (octets) : la même matière que le texte, mise en titres et en paragraphes."""
    import docx                                     # chargé ici seulement : le texte n'en dépend pas
    from docx.shared import Pt
    S, s = c["S"], c["s"]
    doc = docx.Document()
    doc.styles["Normal"].font.size = Pt(10.5)
    doc.core_properties.author = c["auteur"]
    doc.core_properties.title = "Cahier de texte · %s" % s["matiere"]["nom"]
    doc.add_heading(typo("Cahier de texte · %s" % s["matiere"]["nom"]), 0)
    jours = sorted(s["jours"])
    infos = [("Promotion", s["promotion"]), ("Session", c["nom"]), ("Formateur", c["auteur"]),
             ("Jours", ", ".join(date_longue(c["SE"].date_du_jour(s, j)) for j in jours)),
             ("Dépôts", S.LIENS.get("livrables", "")), ("Site du cours", c["site"] or "communiqué en séance")]
    table = doc.add_table(rows=0, cols=2)
    table.style = "Light Grid Accent 1"
    for cle, valeur in infos:
        ligne = table.add_row().cells
        ligne[0].text, ligne[1].text = cle, typo(valeur)
    for i in range(1, len(S.SEANCES) + 1):
        entete, tetes, contenu, travail = texte_seance(i, c, acces)
        doc.add_heading(typo(entete), 1)
        for t in tetes:
            doc.add_paragraph().add_run(typo(t)).bold = True
        doc.add_heading("Contenu de la séance", 2)
        for t in contenu:
            if t.startswith("- "):
                doc.add_paragraph(typo(t[2:]), style="List Bullet")
            else:
                doc.add_paragraph(typo(t))
        doc.add_heading("Travail à faire", 2)
        for t in travail:
            doc.add_paragraph(typo(t))
    tampon = io.BytesIO()
    doc.save(tampon)
    return tampon.getvalue()


def parties_docx(octets):
    """Le contenu d'un Word, sans ses métadonnées de date : deux enregistrements identiques se comparent égaux."""
    with zipfile.ZipFile(io.BytesIO(octets)) as z:
        return {n: z.read(n) for n in z.namelist() if n != "docProps/core.xml"}


def a_jour(chemin, octets, docx=False):
    if not os.path.isfile(chemin):
        return None                                     # absent : rien de périmé
    actuel = io.open(chemin, "rb").read()
    return parties_docx(actuel) == parties_docx(octets) if docx else actuel == octets


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--session", help="la session de outils/sessions.py (par défaut, SESSION_PAR_DEFAUT)")
    ap.add_argument("--essai", action="store_true", help="dit ce qui changerait, sans rien écrire")
    args = ap.parse_args()
    # Un cours qui vient d'être créé n'a ni séance ni session : on le dit, sans trace d'exception.
    if not module("seances").SEANCES:
        print("  ✗ outils/seances.py n'a encore aucune séance : rien à mettre au cahier")
        print("Cahier de texte : NON écrit")
        return 1
    try:
        c = contexte(args.session)
    except KeyError as e:
        print("  ✗ outils/sessions.py : %s" % (e.args[0] if e.args else "session absente"))
        print("Cahier de texte : NON écrit")
        return 1
    ecarts = ["outils/seances.py : " + e for e in c["S"].verifier()]
    ecarts += ["outils/sessions.py : " + e for e in c["SE"].verifier()]
    if ecarts:
        for e in ecarts:
            print("  ✗", e)
        print("Cahier de texte : NON écrit")
        return 1
    acces = lire_acces()
    versions = [("Cahier_de_texte", None)] + ([("Cahier_de_texte_avec_identifiants", acces)] if acces else [])
    perimes = 0
    for base, ident in versions:
        texte = texte_cahier(c, ident).replace("\n", "\r\n").encode("utf-8")
        for ext, octets, est_docx in (("txt", texte, False), ("docx", docx_cahier(c, ident), True)):
            rel = "docs/%s.%s" % (base, ext)
            chemin = os.path.join(RACINE, rel)
            etat = a_jour(chemin, octets, est_docx)
            if etat is True:
                print("  %-50s à jour" % rel)
                continue
            if args.essai:
                print("  %-50s %s" % (rel, "à créer" if etat is None else "PÉRIMÉ"))
                perimes += etat is False
                continue
            io.open(chemin, "wb").write(octets)
            print("  %-50s %s" % (rel, "écrit" if etat is None else "réécrit"))
    print("Cahier de texte : session %s, %d séance(s)%s" % (
        c["nom"], len(c["S"].SEANCES), "" if acces else " ; sans docs/acces.json, la version avec identifiants n'est pas produite"))
    return 1 if args.essai and perimes else 0


if __name__ == "__main__":
    sys.exit(main())
