#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Le classeur d'import de l'application Livrables, d'après outils/seances.py et outils/sessions.py.

    python3 outils/generer_classeur_livrables.py                  # la session par défaut
    python3 outils/generer_classeur_livrables.py --session demo
    python3 outils/generer_classeur_livrables.py --essai          # contrôle, dit ce qui changerait ; code 1 si périmé

Les cinq feuilles que l'application attend (docs/PROMPT-CLASSEUR-IA.md de l'application), dans cet ordre, aux
en-têtes exacts, sans ligne vide ni colonne en trop : Matières, Séances, Livrables, Critères, Ressources. La matière
s'écrit sur trois niveaux, « Année › Promotion › Nom » (U+203A entouré d'espaces) ; les échéances en heure locale,
« AAAA-MM-JJ HH:MM ». La colonne Contenu des séances reprend le cahier de texte (outils/generer_cahier_de_texte.py) :
c'est la voie à suivre quand l'auteur n'a pas accès à Yparéo (décision du 22 novembre 2026).

Un classeur par session, donc par promotion : deux matières nouvelles dans un même fichier se prenaient pour des
doublons (constaté le 27 septembre 2026 dans le cours CDWFS/ASRC). Les liens viennent du site publié
(deploiement/destination.json) : sans adresse connue, les ressources et les liens de consignes restent vides plutôt
qu'inventés. Sorties, jamais versionnées :

    docs/Import_Livrables_<session>.xlsx             le classeur
    docs/Import_Livrables_<session>_reglages.txt     ce que l'import ne porte pas : les réglages à faire à la main

Pièges de l'application : l'import ne supprime jamais rien ; le titre d'un livrable est une clé, et le corriger après
un import crée un livrable de plus ; la case « Livrable bonus, facultatif » rend un livrable non dû, elle ne le sort
pas seulement de la moyenne ; le type « QCM » est celui d'un QCM corrigé par l'application, d'après un corrigé à
lettres fixes, et ne convient pas au QCM du site, qui mélange ses propositions.
"""
import argparse
import importlib.util
import io
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEP = " › "
ENTETES = {
    "Matières": ["Promotion", "Nom", "Code", "Coefficient", "Volume horaire", "Couleur", "Enseignant", "Description"],
    "Séances": ["Matière", "Numéro", "Date", "Heure début", "Heure fin", "Titre", "Contenu", "Modalité"],
    "Livrables": ["Matière", "Séance", "Titre", "Type", "Échéance", "Description", "Format demandé", "Lien consignes",
                  "Mode de notation", "Note max", "Coefficient", "Bonus", "Bonus points max", "Bonus description",
                  "Rappels", "Publié", "Ordre"],
    "Critères": ["Matière", "Séance", "Livrable", "Critère", "Description", "Points"],
    "Ressources": ["Matière", "Séance", "Titre", "Type", "Lien", "Description"],
}
TYPES_RESSOURCES = ("Document", "Lien", "Vidéo", "Dépôt de code", "Exercice", "Autre")

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


def construire(nom_session=None):
    """{feuille: [lignes]} du classeur, et la liste des écarts relevés en le construisant."""
    CT = module("generer_cahier_de_texte")
    c = CT.contexte(nom_session)
    S, SE, s, typo = c["S"], c["SE"], c["s"], CT.typo
    ecarts = []
    m = s["matiere"]
    matiere = SEP.join([s["promotion"], m["nom"]])
    site = c["site"].rstrip("/") + "/" if c["site"] else ""

    def adresse(page):
        return site + page if site else ""

    def date_seance(n):
        return SE.date_du_jour(s, S.SEANCES[n - 1]["jour"])

    def phrases(texte):
        return len(re.findall(r"[.!?](?:\s|$)", texte))

    # getattr : un cours créé avant le classeur n'a ni DESCRIPTION ni RESSOURCES dans son seances.py.
    description = " ".join((getattr(S, "DESCRIPTION", "") or "").split())
    if not 3 <= phrases(description) <= 6:
        ecarts.append("description de la matière (DESCRIPTION, outils/seances.py) : %d phrase(s), l'application en "
                      "attend trois à six" % phrases(description))
    feuilles = {f: [] for f in ENTETES}
    feuilles["Matières"].append([s["promotion"], m["nom"], m.get("code", ""), 1, m.get("volume_horaire", ""),
                                 m["couleur"], "", typo(description)])
    for i, se in enumerate(S.SEANCES, 1):
        debut, fin = S.HORAIRES[se["moment"]]
        _entete, tetes, contenu, travail = CT.texte_seance(i, c)
        texte = "\n".join(contenu + ["Travail à faire :"] + travail)
        feuilles["Séances"].append([matiere, i, date_seance(i).isoformat(), debut, fin, typo(" ; ".join(tetes)),
                                    typo(texte), "presentiel"])
    for ordre, (cle, l) in enumerate(S.LIVRABLES.items(), 1):
        q, n = l["quand"], l.get("notation", {})
        d = SE.date_du_repere(s, S.REPERES[q["repere"]]) if "repere" in q else SE.date_du_jour(s, q["jour"])
        titre = typo(S.texte(l["titre"], c["langue"]))
        if d < date_seance(l["seance"]):
            ecarts.append("livrable %s : échéance avant sa séance" % cle)
        consignes = " ".join((l.get("consignes") or "").split())
        if not 5 <= phrases(consignes) <= 10:
            ecarts.append("livrable %s : consignes de %d phrase(s), l'application en attend cinq à dix"
                          % (cle, phrases(consignes)))
        grille = n.get("mode") == "grille"
        feuilles["Livrables"].append([
            matiere, l["seance"], titre, l["type"], "%s %s" % (d.isoformat(), q["heure"]), typo(consignes),
            typo(l.get("format", "")), adresse(l["page"]) if l.get("page") else "", "grille" if grille else "global",
            n.get("note_max", 20), n.get("coef", 1), "non", 0, "", "oui", "oui", ordre])
        for critere, points, description in (l.get("criteres") or []) if grille else []:
            feuilles["Critères"].append([matiere, l["seance"], titre, typo(critere), typo(description), points])
    if site:
        feuilles["Ressources"].append([matiere, "", "Le site du cours", "Lien", site,
                                       typo("Le cours complet : les chapitres, l'atelier, le QCM, le glossaire et les "
                                            "supports.")])
        for i, se in enumerate(S.SEANCES, 1):
            for num in se.get("chapitres", []):
                fichier, titre = c["titres"].get(str(num), ("", ""))
                if fichier:
                    resume, _obj = CT.chapitre(fichier)
                    premiere = re.split(r"(?<=[.!?])\s", resume)[0] if resume else ""
                    feuilles["Ressources"].append([matiere, i, typo("Chapitre %d · %s" % (num, titre)), "Document",
                                                   adresse("chapitres/" + fichier), typo(premiere)])
        for r in getattr(S, "RESSOURCES", []):
            if r["type"] not in TYPES_RESSOURCES:
                ecarts.append("ressource %r : type %r inconnu" % (r["titre"], r["type"]))
            feuilles["Ressources"].append([matiere, r["seance"] or "", typo(r["titre"]), r["type"], adresse(r["page"]),
                                           typo(r["description"])])
    else:
        ecarts.append("adresse du site inconnue (deploiement/destination.json, « url ») : ressources et liens de "
                      "consignes restent vides, jamais inventés")
    return feuilles, ecarts, c


def liste(titres):
    """« A », « A » et « B », « A », « B » et « C »."""
    t = ["« %s »" % x for x in titres]
    return t[0] if len(t) == 1 else ", ".join(t[:-1]) + " et " + t[-1]


def reglages(c, nom_classeur, feuilles):
    """Le texte des réglages à faire à la main, que l'import ne porte pas.

    Chaque phrase suit ce que fait l'application (son docs/GUIDE-ENSEIGNANT.md et son code, relus le 22 novembre
    2026) : la moyenne ne compte que les livrables notés ; « Livrable bonus, facultatif » rend un livrable non dû ;
    un rendu est un lien tant que « Autoriser les fichiers joints » n'est pas cochée ; un livrable de type QCM porte
    un bloc de configuration que l'import ignore."""
    S = c["S"]
    noms = (("Matières", "matière"), ("Séances", "séance"), ("Livrables", "livrable"), ("Critères", "critère"),
            ("Ressources", "ressource"))
    compte = ", ".join("%d %s%s" % (len(feuilles[f]), nom, "" if len(feuilles[f]) < 2 else "s") for f, nom in noms)
    site = c["site"].rstrip("/") + "/" if c["site"] else ""
    lignes = ["Réglages à faire à la main dans l'application Livrables, après l'import de %s" % nom_classeur,
              "Généré par outils/generer_classeur_livrables.py d'après outils/seances.py : l'import ne porte pas ces "
              "réglages.", "",
              "- Avant de confirmer, relisez l'aperçu. Un premier import annonce des créations (%s). Un réimport "
              "n'annonce que des mises à jour : une création y trahit une clé ratée (la promotion, le nom de la "
              "matière, un numéro de séance ou le titre d'un livrable)." % compte]
    fichiers = [S.texte(l["titre"], c["langue"]) for l in S.LIVRABLES.values() if l.get("fichiers_joints")]
    if fichiers:
        lignes.append("- Cochez « Autoriser les fichiers joints » sur %s : %s rendu est un fichier. Par défaut, "
                      "l'application n'accepte qu'un lien vers l'espace en ligne de l'étudiant, et l'import ne porte "
                      "pas cette case." % (liste(fichiers), "son" if len(fichiers) == 1 else "leur"))
    for l in S.LIVRABLES.values():
        titre, n = S.texte(l["titre"], c["langue"]), l.get("notation", {})
        if not n.get("notee"):
            lignes.append("- Le livrable « %s » est obligatoire et non noté. Ne lui saisissez aucune note : "
                          "l'application ne compte dans la moyenne que les livrables notés. Ne cochez pas « Livrable "
                          "bonus, facultatif » : il ne serait plus dû, et ceux qui ne l'ont pas rendu sortiraient du "
                          "compteur des manquants." % titre)
        if l["type"] == "QCM":
            lignes.append("- « %s » est un QCM corrigé par l'application. Réglez son bloc QCM (comment se passe "
                          "l'épreuve, le corrigé, le barème), que l'import ne porte pas." % titre)
        elif (l.get("page") or "").startswith("QCM/"):
            # Le QCM du site : sa note vient du tableau de bord du gabarit (site/QCM/dashboard/), pas de l'application.
            lignes.append("- « %s » se passe sur le site du cours. Sa note se calcule dans le tableau de bord du QCM%s, "
                          "où vous déposez les fichiers CSV des étudiants, puis se saisit dans l'application."
                          % (titre, " (%sQCM/dashboard/)" % site if site else ""))
    lignes.append("- Un réimport ne supprime rien. Un livrable dont le titre a changé devient un livrable de plus : "
                  "retirez l'ancien à la main.")
    return "\n".join(lignes) + "\n"


def controler(feuilles, c):
    """Les règles de l'application, vérifiées sur les lignes du classeur."""
    S, ecarts = c["S"], []
    numeros = {ligne[1] for ligne in feuilles["Séances"]}
    for ligne in feuilles["Livrables"]:
        if ligne[1] not in numeros:
            ecarts.append("livrable %r : séance %r absente de la feuille Séances" % (ligne[2], ligne[1]))
        if ligne[3] not in S.TYPES:
            ecarts.append("livrable %r : type %r hors de la liste de l'application" % (ligne[2], ligne[3]))
        if not ligne[10] or ligne[10] <= 0:
            ecarts.append("livrable %r : coefficient strictement positif attendu" % ligne[2])
        if ligne[8] == "grille":
            pts = [cr[5] for cr in feuilles["Critères"] if cr[2] == ligne[2]]
            if not 4 <= len(pts) <= 6 or sum(pts) != ligne[9]:
                ecarts.append("livrable %r : %d critère(s) pour %d points (4 à 6, total %s attendus)"
                              % (ligne[2], len(pts), sum(pts), ligne[9]))
    for feuille, lignes in feuilles.items():
        for ligne in lignes:
            if len(ligne) != len(ENTETES[feuille]):
                ecarts.append("%s : une ligne de %d colonnes pour %d en-têtes" % (feuille, len(ligne),
                                                                              len(ENTETES[feuille])))
            for v in ligne:
                if isinstance(v, str) and (v.startswith("=") or "—" in v):
                    ecarts.append("%s : %r commence par « = » ou porte un tiret cadratin" % (feuille, v[:40]))
    for ligne in feuilles["Séances"] + feuilles["Livrables"] + feuilles["Critères"] + feuilles["Ressources"]:
        if ligne[0].count(SEP) != 2:
            ecarts.append("matière %r : trois niveaux « Année › Promotion › Nom » attendus" % ligne[0])
            break
    return ecarts


def valeurs(chemin):
    """{feuille: [lignes]} d'un classeur existant, en-têtes compris ; None s'il n'existe pas."""
    if not os.path.isfile(chemin):
        return None
    import openpyxl
    wb = openpyxl.load_workbook(chemin, read_only=True)
    return {f: [list(r) for r in wb[f].iter_rows(values_only=True)] for f in wb.sheetnames}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--session", help="la session de outils/sessions.py (par défaut, SESSION_PAR_DEFAUT)")
    ap.add_argument("--essai", action="store_true", help="contrôle et dit ce qui changerait, sans rien écrire")
    args = ap.parse_args()
    if not module("seances").SEANCES:
        print("  ✗ outils/seances.py n'a encore aucune séance : rien à mettre au classeur")
        print("Classeur Livrables : NON écrit")
        return 1
    try:
        feuilles, ecarts, c = construire(args.session)
    except KeyError as e:
        print("  ✗ outils/sessions.py : %s" % (e.args[0] if e.args else "session absente"))
        print("Classeur Livrables : NON écrit")
        return 1
    bloquants = [e for e in ecarts + controler(feuilles, c) + c["S"].verifier() + c["SE"].verifier()
                 if "restent vides" not in e]
    for e in ecarts + controler(feuilles, c):
        print("  %s %s" % ("·" if "restent vides" in e else "✗", e))
    if bloquants:
        print("Classeur Livrables : NON écrit")
        return 1
    nom = "Import_Livrables_%s" % c["nom"]
    xlsx = os.path.join(RACINE, "docs", nom + ".xlsx")
    txt = os.path.join(RACINE, "docs", nom + "_reglages.txt")
    # Une case vide s'écrit vide, pas en chaîne vide : relue, elle vaut None, et la comparaison de --essai tient.
    attendu = {f: [ENTETES[f]] + [[None if v == "" else v for v in ligne] for ligne in lignes]
               for f, lignes in feuilles.items()}
    texte = reglages(c, nom + ".xlsx", feuilles).replace("\n", "\r\n").encode("utf-8")
    etat_x = valeurs(xlsx)
    etat_t = io.open(txt, "rb").read() if os.path.isfile(txt) else None
    perime = (etat_x is not None and etat_x != attendu) or (etat_t is not None and etat_t != texte)
    resume = ", ".join("%s %d" % (f, len(l)) for f, l in feuilles.items())
    if args.essai:
        for rel, etat, egal in (("docs/%s.xlsx" % nom, etat_x, etat_x == attendu),
                                ("docs/%s_reglages.txt" % nom, etat_t, etat_t == texte)):
            print("  %-50s %s" % (rel, "à créer" if etat is None else ("à jour" if egal else "PÉRIMÉ")))
        print("Classeur Livrables : session %s (%s)" % (c["nom"], resume))
        return 1 if perime else 0
    import openpyxl
    from openpyxl.styles import Font
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for f, lignes in attendu.items():
        ws = wb.create_sheet(f)
        for ligne in lignes:
            ws.append(ligne)
        for cellule in ws[1]:
            cellule.font = Font(bold=True)
        for colonne in ws.columns:
            ws.column_dimensions[colonne[0].column_letter].width = min(60, max(10, max(
                len(str(v.value or "")) for v in colonne) // 3 + 8))
    if etat_x != attendu:
        wb.save(xlsx)
        print("  %-50s %s" % ("docs/%s.xlsx" % nom, "écrit" if etat_x is None else "réécrit"))
    else:
        print("  %-50s à jour" % ("docs/%s.xlsx" % nom))
    if etat_t != texte:
        io.open(txt, "wb").write(texte)
        print("  %-50s %s" % ("docs/%s_reglages.txt" % nom, "écrit" if etat_t is None else "réécrit"))
    else:
        print("  %-50s à jour" % ("docs/%s_reglages.txt" % nom))
    print("Classeur Livrables : session %s (%s)" % (c["nom"], resume))
    return 0


if __name__ == "__main__":
    sys.exit(main())
