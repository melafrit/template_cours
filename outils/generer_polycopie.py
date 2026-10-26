#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Le polycopié du cours (module 02) : des pages du site au livret Word, puis au PDF par Word.

    python3 outils/generer_polycopie.py --temoin               # le témoin : Polycopie/temoin/Polycopie-temoin.docx
                                                              # et son PDF
    python3 outils/generer_polycopie.py --temoin --essai       # contrôles seuls : lecture des pages, adresses des
                                                              # QR codes ; rien n'est écrit
    python3 outils/generer_polycopie.py --temoin --anglais     # le témoin anglais (Polycopie-temoin-en)
    python3 outils/generer_polycopie.py --verrou <fichier> --apercus <dossier>
                                                              # le livret complet : Polycopie/Polycopie-<titre>.docx
                                                              # et .pdf
    options : --verrou <fichier>   l'export par Word attend ce verrou et le tient (ou VERROU_WORD)
              --sans-pdf           le Word seul, sans passer par Word (champs non calculés)
              --hors-ligne         sans vérifier les adresses en ligne (les ancres le sont toujours)
              --apercus <dossier>  chaque page du PDF en PNG, et les planches en vis-à-vis
              --images             refait toutes les images (pictogrammes, garde, schémas)
              --sortie <chemin>    écrit ailleurs (chemin sans extension)

LE TÉMOIN : la page de garde ; les mentions légales ; « À propos de l'auteur » (outils/livret.py, mot pour mot) ;
« Comment utiliser ce polycopié » ; la table des matières ; l'ouverture des chapitres du témoin (outils/livret.py,
« temoin ») et ces chapitres ; le glossaire des termes qu'ils emploient ; l'index. LE LIVRET : les mêmes pages
liminaires, tous les chapitres de course-data.js, le glossaire entier, l'index. La chaîne est la même : seule la
liste des chapitres change.

Les étapes : lire les pages (polycopie/lecture.py ; les composants par Chrome sans interface), composer le Word
(polycopie/pages.py, rendu.py), contrôler les adresses des QR codes et les règles du livret, puis faire mettre à jour
tous les champs par Word, ranger la marge, enregistrer le Word et exporter le PDF (polycopie/word.py), dont la langue
est enfin fixée. Dans le PDF, chaque QR code et le texte qui le décrit sont des liens vers l'adresse qu'il porte ; le
contrôle liens_des_qr le vérifie à chaque génération. Le dossier Polycopie/ n'est jamais publié (hors de site/).
Repris, en générique et bilingue, du cours d'architecture logicielle.
"""
import argparse
import os
import re
import sys
import time
import unicodedata

ICI = os.path.dirname(os.path.abspath(__file__))
if ICI not in sys.path:
    sys.path.insert(0, ICI)

for flux in (sys.stdout, sys.stderr):
    try:
        flux.reconfigure(encoding="utf-8")
    except Exception:
        pass

from polycopie import controles as C  # noqa: E402
from polycopie import gabarit as G  # noqa: E402
from polycopie import images, lecture, pages, qr, rendu  # noqa: E402
from polycopie.sources import ADRESSE, RACINE, SITE, TRAVAIL, Langue  # noqa: E402


def nom_de_fichier(titre):
    s = unicodedata.normalize("NFD", titre or "livret")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-")[:60] or "livret"


def cibles(r, lues):
    """Les renvois de pages : chaque adresse du site que le livret contient (une page lue et ses ancres, le
    glossaire) → le signet qui la porte dans le livret."""
    langue = r.langue
    for rel, page in lues.items():
        url = langue.url(rel)
        r.cibles[url] = pages.signet_page(rel)
        for ident in page.idents:
            r.cibles[(url, ident)] = rendu.signet_nom(ident)
    r.cibles[langue.url("glossaire.html")] = "poly_page_glossaire"


def composer(langue, chapitres, temoin, atelier, registre, journal=print):
    """Le document Word du livret (ou du témoin) ; rend (document, rendu, pages lues)."""
    L = langue.L
    doc = G.nouveau_document(langue, L["titre"], L["sujet_temoin"] if temoin else L["sujet"])
    r = rendu.Rendu(doc, langue, atelier, registre)
    r.preparer_pictos()
    lues = {}
    for num, rel, _titre in chapitres:
        lues[rel] = lecture.lire_page(langue, rel)
        journal(f"lu : {rel} — {len(lues[rel].blocs)} blocs, {len(lues[rel].sections)} sections, "
                f"{len(lues[rel].activites)} composants")
    cibles(r, lues)
    pages.couverture(r)
    pages.mentions(r)
    pages.a_propos(r)
    pages.mode_emploi(r)
    pages.table_des_matieres(r)
    for num, rel, _titre in chapitres:
        pages.ouverture(r, lues[rel], num)
        r.blocs(lues[rel].blocs)
        r.page = None
    entrees = langue.glossaire()
    choisies = [e for e in entrees if e["ancre"] in r.termes_vus] if temoin else entrees
    pages.glossaire(r, choisies, temoin=temoin, total=len(entrees))
    pages.index(r)
    manquants = sorted(set(r.renvois) - r.signets_poses)
    if manquants:
        raise SystemExit(f"Renvois de pages sans signet : {manquants[:12]}")
    return doc, r, lues


def main():
    ap = argparse.ArgumentParser(description="Le polycopié du cours : Word, puis PDF par Word.")
    ap.add_argument("--temoin", action="store_true", help="le témoin de mise en page")
    ap.add_argument("--anglais", action="store_true", help="le livret anglais")
    ap.add_argument("--essai", action="store_true", help="contrôles seuls, sans rien écrire")
    ap.add_argument("--sans-pdf", action="store_true", help="le Word seul, sans l'export par Word")
    ap.add_argument("--hors-ligne", action="store_true", help="sans vérifier les adresses en ligne")
    ap.add_argument("--apercus", help="dossier des aperçus PNG des pages du PDF")
    ap.add_argument("--images", action="store_true", help="refait toutes les images")
    ap.add_argument("--verrou", default=os.environ.get("VERROU_WORD"),
                    help="fichier verrou à tenir pendant l'export par Word (un seul export à la fois sur le poste)")
    ap.add_argument("--sortie", help="écrit ailleurs (chemin sans extension)")
    args = ap.parse_args()
    debut = time.time()
    langue = Langue("en" if args.anglais else "fr")
    tous = langue.chapitres()
    if not tous:
        raise SystemExit("Aucun chapitre dans site/assets/js/course-data.js.")
    if args.temoin:
        voulus = [str(n) for n in (langue.livret.get("temoin") or [tous[0][0]])]
        chapitres = [c for c in tous if c[0] in voulus] or tous[:1]
    else:
        chapitres = tous
    suffixe = "-en" if args.anglais else ""
    base = args.sortie or (os.path.join(TRAVAIL, "temoin", "Polycopie-temoin" + suffixe) if args.temoin else
                           os.path.join(TRAVAIL, "Polycopie-" + nom_de_fichier(langue.L["titre"]) + suffixe))
    if not ADRESSE:
        print(f"Adresse publique inconnue (« url » de deploiement/destination.json) : les QR codes portent l'adresse "
              f"d'exemple {SITE} — aucune vérification en ligne.")
    atelier = images.Atelier(langue, forcer=args.images)
    registre = qr.Registre(langue)
    doc, r, lues = composer(langue, chapitres, args.temoin, atelier, registre)

    # Les adresses des QR codes : chacune répond 200 (en ligne), chaque ancre existe ; aucune correction protégée.
    en_ligne = bool(ADRESSE) and not args.hors_ligne
    erreurs = registre.verifier(en_ligne=en_ligne)
    erreurs += [f"{p['url']} : une correction protégée ne s'ouvre jamais depuis le livret" for p in registre.poses
                if "/correction/" in p["url"]]
    print(f"QR codes : {len(registre.poses)} posés, {len({p['url'] for p in registre.poses})} adresses"
          + (", vérifiées en ligne" if en_ligne else ", ancres vérifiées dans le site") + f" ; {len(erreurs)} erreur(s)")
    for e in erreurs:
        print("  ✗", e)
    for a in (j for j in r.journal if j.get("genre") in ("schema absent", "image absente")):
        quoi = "schéma absent du site, non imprimé" if a["genre"] == "schema absent" else "image absente du site, " \
                                                                                        "non imprimée"
        print(f"  · {quoi} : {a['source']} ({a['lieu']})")
    if args.essai:
        print("Essai : rien n'est écrit." if not erreurs else "Essai : des adresses sont à corriger.")
        sys.exit(1 if erreurs else 0)
    if erreurs:
        raise SystemExit("Polycopié refusé : un QR code mène à une adresse qui ne répond pas, ou à une ancre absente.")

    os.makedirs(os.path.dirname(base), exist_ok=True)
    docx, pdf = base + ".docx", base + ".pdf"
    doc.save(docx)
    print(f"Word écrit : {os.path.relpath(docx, RACINE)}")

    # Les règles du livret, dans le texte du Word : aucune adresse imprimée hors des mentions, aucune réponse.
    reponses = [x for p in lues.values() for x in C.reponses_des_activites(p.activites)]
    visibles = "\n".join(lecture.texte_visible(p) for p in lues.values())
    ecarts = C.regles(docx, reponses, autorises=(langue.url("").rstrip("/"),), visibles=visibles,
                      produits=langue.L.get("produits", ()))
    print(f"règles du livret : {len(ecarts)} écart(s)")
    for e in ecarts:
        print("  ✗", e)
    if ecarts:
        raise SystemExit("Polycopié refusé : le texte enfreint une règle du livret.")

    if not args.sans_pdf:
        from polycopie import word
        compte = word.exporter(docx, pdf, args.verrou, largeur_texte_cm=G.TEXTE)
        mal_calcules = C.champs_du_pdf(pdf)
        print(f"champs mal calculés dans le PDF : {len(mal_calcules)}")
        for x in mal_calcules[:20]:
            print("  ✗", x)
        word.fixer_langue(pdf, langue.L["langue_word"])
        n, apercus = C.pdf(pdf, args.apercus)
        print(f"PDF écrit : {os.path.relpath(pdf, RACINE)} — {n} pages ; marge : {len(compte.get('marge', []))} "
              f"retouche(s) ; figures : {len(compte.get('figures', []))} ; champs : {compte.get('champs')}")
        lu = C.lire_docx(docx)
        print(f"Word relu : {lu['paragraphes']} paragraphes, {lu['tableaux']} tableaux, {lu['images']} images en "
              f"ligne, {lu['sections']} sections ; champs {lu['champs']}")
        faibles = [x for x in C.images_pdf(pdf) if x[3] < 200]
        if faibles:
            print(f"images sous 200 ppp dans le PDF : {faibles[:8]}")
        urls = [q["url"] for q in registre.poses]
        trouves, inconnus = C.qr_du_pdf(pdf, urls)
        jamais = sorted(set(urls) - {u for _, u in trouves})
        print(f"QR codes relus dans le PDF : {len(trouves)} ; illisibles ou inconnus : {len(inconnus)} ; "
              f"adresses jamais imprimées : {len(jamais)}")
        for x in inconnus + jamais:
            print("  ✗", x)
        liens = C.liens_des_qr(pdf, urls)
        nl = liens["liens"]
        print(f"liens des QR codes : {liens['qr']} QR codes ; annotations : {nl['qr']} sur les QR codes, "
              f"{nl['legendes']} sur leurs légendes, {nl['autres']} autre(s), {nl['internes']} internes ; "
              f"{len(liens['anomalies'])} anomalie(s)")
        for x in liens["anomalies"]:
            print("  ✗", x)
        if apercus:
            print(f"aperçus : {len(apercus)} pages en PNG dans {args.apercus}")
    print(f"fait en {time.time() - debut:.0f} s")


if __name__ == "__main__":
    main()
