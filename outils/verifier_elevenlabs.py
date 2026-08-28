#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vérifie la configuration ElevenLabs avant toute génération.

    python3 outils/verifier_elevenlabs.py

Trois questions, auxquelles il vaut mieux répondre avant de dépenser des
crédits :

  1. la clé fonctionne-t-elle ?
  2. quel est l'identifiant de mon clone vocal ? — l'interface du site bouge,
     l'API non : elle donne la liste exacte, à copier telle quelle ;
  3. le modèle v3 est-il accessible ? Lui seul interprète les balises entre
     crochets. Sur les autres modèles elles seraient lues à voix haute, et les
     prises inutilisables.

Affiche aussi le quota restant, pour savoir si les 37 pistes tiennent.

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
# Le site vit dans site/, pas a la racine : celle-ci porte aussi les outils,
# les fiches de production et la documentation, qui ne sont pas publies.
SITE = os.path.join(RACINE, "site")
CONFIG = os.path.join(RACINE, "outils", "elevenlabs.json")
MODELE = os.path.join(RACINE, "outils", "elevenlabs.exemple.json")
BASE = "https://api.elevenlabs.io/v1"
GABARITS = {"a-remplir", "sk_a-remplir", ""}

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
        "User-Agent": "cours-reglementation/1.0",
    })
    with urllib.request.urlopen(req, timeout=30, context=CTX) as r:
        return json.loads(r.read().decode("utf-8"))


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

    # --- quota
    util = abo.get("character_count")
    plafond = abo.get("character_limit")
    if isinstance(util, int) and isinstance(plafond, int):
        reste = max(0, plafond - util)
        print("  offre : %s" % abo.get("tier", "?"))
        print("  quota : %s / %s caractères utilisés — il reste %s"
              % (format(util, ","), format(plafond, ","), format(reste, ",")))
        besoin = 51205
        if reste < besoin:
            print("  /!\\ les 37 pistes restantes demandent environ %s caractères :"
                  % format(besoin, ","))
            print("      le quota actuel n'y suffit pas. Générez par chapitre, ou attendez"
                  " le renouvellement.")
        else:
            print("  les 37 pistes restantes (environ %s caractères) tiennent dans ce quota."
                  % format(besoin, ","))

    # --- modèles
    print("\nModèles disponibles\n-------------------")
    voulu = str(c.get("modele", "")).strip()
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
        if "v3" in mid:
            marque = "   <-- interprète les balises"
        if mid == voulu:
            marque += "   <-- votre configuration"
        print("  %-34s %s%s" % (mid, (m.get("name") or "")[:30], marque))

    # Le modèle configuré prime s'il est disponible : plusieurs variantes de v3
    # coexistent (narration, conversationnel) et elles ne se valent pas. Ne
    # suggérer un remplacement que si le modèle voulu est réellement absent.
    v3 = [m for m in dispo if "v3" in m]
    if voulu and voulu in dispo:
        print("\n  « %s » est disponible : rien à changer." % voulu)
        if "v3" not in voulu:
            print("  /!\\ ce modèle n'est pas un v3 : les balises entre crochets seraient")
            print("      lues à voix haute. Les modèles v3 de la liste : %s"
                  % (", ".join(v3) or "aucun"))
    elif v3:
        print("\n  /!\\ « %s » ne figure pas dans la liste." % (voulu or "(vide)"))
        print("      Modèles v3 disponibles : %s" % ", ".join(v3))
        print("      Pour de la narration, préférez « eleven_v3 » à la variante")
        print("      conversationnelle, dont le débit et les intonations diffèrent.")
    else:
        print("\n  /!\\ AUCUN modèle v3 dans cette liste.")
        print("      Les balises [warmly], [pause]… seraient lues à voix haute ou ignorées.")
        print("      Continuez à générer depuis l'interface du site, où v3 est disponible.")

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
