#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vérifie la configuration ElevenLabs avant toute génération.

    python3 outils/verifier_elevenlabs.py

Trois questions, auxquelles il vaut mieux répondre avant de dépenser des
crédits :

  1. la clé fonctionne-t-elle ?
  2. quel est l'identifiant de mon clone vocal ? — l'interface du site bouge,
     l'API non : elle donne la liste exacte, à copier telle quelle ;
  3. Eleven v4 est-il accessible ? C'est le modèle de toutes les pistes : il
     interprète les balises de jeu entre crochets et l'accent ajouté par
     outils/generer_audio.py. Sur un modèle qui ne les comprend pas, elles
     seraient lues à voix haute, et les prises inutilisables.

Affiche aussi le quota restant, et ce que demandent les pistes encore à
générer : on sait avant de lancer si la série tient.

Aucune génération, aucun crédit consommé. La clé n'est jamais affichée.
Sans dépendance : urllib suffit.
"""

import io
import json
import os
import ssl
import sys
import urllib.error
import urllib.request

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG = os.path.join(RACINE, "outils", "elevenlabs.json")
MODELE = os.path.join(RACINE, "outils", "elevenlabs.exemple.json")
BASE = "https://api.elevenlabs.io/v1"
GABARITS = {"a-remplir", "sk_a-remplir", ""}
VOULU = "eleven_v4"

for flux in (sys.stdout, sys.stderr):
    try:
        flux.reconfigure(encoding="utf-8")
    except Exception:
        pass


def charger():
    if not os.path.isfile(CONFIG):
        sys.exit("Configuration absente : %s\n"
                 "Copiez le modèle puis renseignez-le :\n"
                 "    cp %s %s" % (CONFIG, MODELE, CONFIG))
    with io.open(CONFIG, encoding="utf-8") as f:
        try:
            return json.load(f)
        except ValueError as e:
            sys.exit("Configuration illisible : %s" % e)


def contexte_ssl():
    """Magasin de certificats fiable, quelle que soit l'installation de Python.

    Sur macOS, Python n'utilise pas le trousseau du système : une installation
    venue de python.org sans son « Install Certificates.command » échoue avec
    CERTIFICATE_VERIFY_FAILED. Le paquet certifi, présent dès qu'on a installé
    quoi que ce soit avec pip, porte le magasin qu'il faut : on le prend quand
    il est là, sinon on retombe sur le comportement par défaut.
    """
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return ssl.create_default_context()


CTX = contexte_ssl()


def appeler(chemin, cle):
    req = urllib.request.Request(BASE + chemin, headers={
        "xi-api-key": cle,
        "Accept": "application/json",
        "User-Agent": "cours-template/1.0",
    })
    with urllib.request.urlopen(req, timeout=30, context=CTX) as r:
        return json.loads(r.read().decode("utf-8"))


def besoin_du_cours():
    """(pistes, caractères) encore à générer, accent compris — ce que coûtera la série."""
    sys.path.insert(0, os.path.join(RACINE, "outils"))
    try:
        import generer_audio as G
    except Exception:
        return None
    scripts = G.scripts_des_fiches()
    sortie = os.path.join(G.SITE, "assets", "media", "voix")
    n, car = 0, 0
    for _n, _cid, nom, _t in G.pistes_attendues():
        dossier = os.path.join(G.SITE, "assets", "media", "podcasts") if "-podcast." in nom else sortie
        if nom in scripts and not os.path.exists(os.path.join(dossier, nom)):
            n += 1
            car += len(G.avec_accent(scripts[nom], G.ACCENTS.get(G.langue_piste(nom), "")))
    return n, car


def main():
    c = charger()
    cle = str(c.get("cle_api", "")).strip()
    if cle in GABARITS:
        sys.exit("La clé API est restée sur la valeur du modèle.\n"
                 "Renseignez « cle_api » dans %s." % CONFIG)

    print("\nConnexion\n---------")
    try:
        abo = appeler("/user/subscription", cle)
    except urllib.error.HTTPError as e:
        if e.code == 401:
            sys.exit("  Clé refusée (401). Vérifiez-la, ou créez-en une nouvelle :\n"
                     "  https://elevenlabs.io/app/settings/api-keys")
        sys.exit("  Erreur HTTP %s : %s" % (e.code, e.reason))
    except urllib.error.URLError as e:
        raison = str(e.reason)
        if "CERTIFICATE_VERIFY_FAILED" in raison:
            sys.exit(
                "  Connexion impossible : votre installation de Python n'a pas de magasin\n"
                "  de certificats utilisable. C'est fréquent sur macOS — Python n'utilise\n"
                "  pas le trousseau du système.\n\n"
                "  Installez le magasin, puis relancez :\n"
                "      python3 -m pip install --upgrade certifi\n\n"
                "  Si Python vient de python.org, exécutez aussi, une fois pour toutes :\n"
                "      open \"/Applications/Python %s/Install Certificates.command\""
                % ("%d.%d" % (sys.version_info.major, sys.version_info.minor)))
        sys.exit("  Connexion impossible : %s" % raison)
    print("  clé acceptée.")

    # --- quota, et ce que demandent les pistes qui manquent
    util = abo.get("character_count")
    plafond = abo.get("character_limit")
    if isinstance(util, int) and isinstance(plafond, int):
        reste = max(0, plafond - util)
        print("  offre : %s" % abo.get("tier", "?"))
        print("  quota : %s / %s caractères utilisés — il reste %s"
              % (format(util, ","), format(plafond, ","), format(reste, ",")))
        besoin = besoin_du_cours()
        if besoin and besoin[0]:
            n, car = besoin
            verdict = "tiennent dans ce quota" if car <= reste else "NE tiennent PAS dans ce quota"
            print("  les %d piste(s) à générer (≈ %s caractères, accent compris) %s."
                  % (n, format(car, ","), verdict))
            if car > reste:
                print("      Générez par chapitre (--chapitre), ou attendez le renouvellement.")
        elif besoin:
            print("  aucune piste à générer : toutes celles que les pages réclament sont en place.")

    # --- modèles
    print("\nModèles disponibles\n-------------------")
    configure = str(c.get("modele", "")).strip()
    dispo = []
    try:
        modeles = appeler("/models", cle)
    except urllib.error.HTTPError as e:
        modeles = []
        print("  liste indisponible (HTTP %s)." % e.code)
    for m in modeles if isinstance(modeles, list) else []:
        mid = m.get("model_id", "?")
        dispo.append(mid)
        marque = ""
        if mid == VOULU:
            marque = "   <-- le modèle de toutes les pistes"
        if mid == configure and mid != VOULU:
            marque += "   <-- votre configuration"
        print("  %-34s %s%s" % (mid, (m.get("name") or "")[:30], marque))

    if VOULU in dispo:
        print("\n  « %s » est disponible : le générateur l'utilisera." % VOULU)
        if configure and configure != VOULU:
            print("  Votre configuration indique « %s » : le générateur la corrige à la volée." % configure)
            print("  Pour ne plus voir ce message, mettez « modele » à « %s »." % VOULU)
    elif dispo:
        print("\n  /!\\ « %s » ne figure pas dans la liste de votre compte." % VOULU)
        print("      Les balises de jeu et l'accent ne seraient pas interprétés. N'essayez un autre")
        print("      modèle que sur un témoin : python3 outils/generer_audio.py --temoin --limite 1"
              " --modele <modèle>")

    # --- voix
    print("\nVos voix\n--------")
    try:
        voix = appeler("/voices", cle).get("voices", [])
    except urllib.error.HTTPError as e:
        sys.exit("  liste des voix indisponible (HTTP %s)." % e.code)
    if not voix:
        print("  aucune voix trouvée.")
    clones = []
    for v in voix:
        cat = v.get("category", "")
        vid = v.get("voice_id", "?")
        nom = v.get("name", "?")
        marque = ""
        if cat in ("professional", "cloned"):
            clones.append((nom, vid, cat))
            marque = "   <-- votre clone"
        print("  %-26s %-24s %s%s" % (nom[:26], vid, cat, marque))

    actuel = str(c.get("voix_id", "")).strip()
    print("")
    if len(clones) == 1 and actuel in GABARITS:
        nom, vid, _cat = clones[0]
        print("  Un seul clone trouvé : « %s »." % nom)
        print("  Reportez cet identifiant dans %s :" % os.path.relpath(CONFIG, RACINE))
        print("      \"voix_id\": \"%s\"" % vid)
    elif actuel in GABARITS:
        print("  Reportez l'identifiant de votre clone dans « voix_id ».")
    else:
        connu = [v for v in voix if v.get("voice_id") == actuel]
        if connu:
            print("  Configuration : « %s » — voix trouvée sur votre compte." % connu[0].get("name"))
        else:
            print("  /!\\ « voix_id » ne correspond à aucune voix de la liste ci-dessus.")

    print("\nAucun crédit n'a été consommé.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
