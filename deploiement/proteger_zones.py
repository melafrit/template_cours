#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pose la protection par identifiant et mot de passe des zones protégées du site.

    python3 deploiement/proteger_zones.py --hors-ligne   # construit et contrôle, sans se connecter
    python3 deploiement/proteger_zones.py --essai        # se connecte, construit, contrôle, n'envoie rien
    python3 deploiement/proteger_zones.py                # envoie .htaccess et .htpasswd, relit, vérifie

UNE ZONE, c'est un dossier du site placé derrière un mot de passe : la correction d'un TP, la
partie réservée au formateur. Elle se déclare à deux endroits, qui doivent concorder :

  deploiement/destination.json   « zones_protegees » : le déployeur ne publie le contenu d'une
                                 zone qu'une fois sa protection en ligne ;
  docs/acces-zones.json          les comptes (identifiant, mot de passe) et, pour chaque zone,
                                 ceux qu'elle admet. Ignoré par Git par défaut : voir .gitignore.

POURQUOI UN SCRIPT À PART. Le déployeur n'envoie ni ne supprime jamais un .htaccess ou un
.htpasswd : une protection posée côté serveur survit ainsi à chaque publication. C'est donc ce
script qui les pose, avec le chemin absolu qu'attend Apache (AuthUserFile), lu par SFTP.

ORDRE À RESPECTER pour une première mise en ligne : la protection d'abord, le contenu ensuite.
La zone n'est ainsi jamais lisible sans mot de passe, pas même une minute.

CHANGER UN MOT DE PASSE : modifiez docs/acces-zones.json, puis relancez ce script.

Les mots de passe partent sur le serveur chiffrés par bcrypt (format $2y$, celui d'Apache).
Dépendance : bcrypt (python3 -m pip install bcrypt). Ce script n'affiche jamais un mot de passe.
"""
import argparse
import io
import json
import os
import sys
import urllib.error
import urllib.request

ICI = os.path.dirname(os.path.abspath(__file__))
DEPOT = os.path.dirname(ICI)
ACCES = os.path.join(DEPOT, "docs", "acces-zones.json")
MODELE = os.path.join(DEPOT, "docs", "acces-zones.exemple.json")
sys.path.insert(0, ICI)
import deployer as D  # noqa: E402  — sa configuration et sa connexion, sans les recopier ici

# Chemin fictif du compte, pour construire et contrôler les fichiers sans connexion.
RACINE_FICTIVE = "/chemin/absolu/du/compte"


def charger_acces():
    """Les comptes et les zones, contrôlés avant tout envoi."""
    if not os.path.isfile(ACCES):
        sys.exit("Fichier absent : %s\nCopiez le modèle puis renseignez-le :\n    cp %s %s"
                 % (os.path.relpath(ACCES, DEPOT), os.path.relpath(MODELE, DEPOT),
                    os.path.relpath(ACCES, DEPOT)))
    with io.open(ACCES, encoding="utf-8") as f:
        a = json.load(f)
    comptes, zones = a.get("comptes") or {}, a.get("zones") or []
    if not comptes or not zones:
        sys.exit("acces-zones.json : « comptes » et « zones » sont tous deux requis.")
    vus = set()
    for qui, compte in comptes.items():
        ident, mdp = str(compte.get("identifiant", "")).strip(), str(compte.get("mot_de_passe", ""))
        if not ident or not mdp or ident in D.GABARITS or mdp in ("a-remplir", "mot-de-passe"):
            sys.exit("acces-zones.json : identifiant ou mot de passe « %s » manquant." % qui)
        if ":" in ident:
            sys.exit("acces-zones.json : l'identifiant « %s » ne doit pas contenir « : »." % qui)
        if ident in vus:
            sys.exit("acces-zones.json : deux comptes portent le même identifiant (« %s »)." % qui)
        vus.add(ident)
    for z in zones:
        dossier = str(z.get("dossier", "")).strip().strip("/")
        if not dossier or ".." in dossier.split("/"):
            sys.exit("acces-zones.json : zone sans dossier valide : %r" % z)
        if not z.get("comptes") or any(q not in comptes for q in z["comptes"]):
            sys.exit("acces-zones.json : la zone « %s » admet un compte inconnu ou aucun." % dossier)
        z["dossier"] = dossier
        z.setdefault("nom", "Zone protégée")
    return a


def empreinte(mot_de_passe):
    """bcrypt au format d'Apache ($2y$ : le même algorithme que $2b$, sous le préfixe qu'Apache reconnaît)."""
    import bcrypt
    h = bcrypt.hashpw(mot_de_passe.encode("utf-8"), bcrypt.gensalt(rounds=10)).decode("ascii")
    return "$2y$" + h[4:]


def correspond(mot_de_passe, h):
    import bcrypt
    return bcrypt.checkpw(mot_de_passe.encode("utf-8"), ("$2b$" + h[4:]).encode("ascii"))


def htaccess(nom, chemin_htpasswd):
    return "\n".join([
        "# Zone protégée, posée par deploiement/proteger_zones.py.",
        "# Ne pas modifier à la main : changez docs/acces-zones.json, puis relancez le script.",
        'AuthName "%s"' % nom.replace('"', "'"),
        "AuthType Basic",
        'AuthUserFile "%s"' % chemin_htpasswd,
        "Require valid-user",
        "Options -Indexes",
        '<FilesMatch "^\\.ht">',
        "  Require all denied",
        "</FilesMatch>",
        ""])


def fichiers(acces, racine_absolue):
    """{chemin relatif à la racine du site : texte} — un .htaccess et un .htpasswd par zone."""
    out = {}
    for z in acces["zones"]:
        lignes = "".join("%s:%s\n" % (acces["comptes"][q]["identifiant"],
                                      empreinte(acces["comptes"][q]["mot_de_passe"]))
                         for q in z["comptes"])
        out["%s/.htpasswd" % z["dossier"]] = lignes
        out["%s/.htaccess" % z["dossier"]] = htaccess(
            z["nom"], "%s/%s/.htpasswd" % (racine_absolue.rstrip("/"), z["dossier"]))
    return out


def controler(acces, contenus):
    """Chaque empreinte correspond à son mot de passe ; chaque zone admet exactement ses comptes."""
    pb = []
    for z in acces["zones"]:
        lignes = [l for l in contenus["%s/.htpasswd" % z["dossier"]].splitlines() if l]
        admis = {l.split(":", 1)[0]: l.split(":", 1)[1] for l in lignes}
        attendus = {acces["comptes"][q]["identifiant"]: acces["comptes"][q]["mot_de_passe"]
                    for q in z["comptes"]}
        if set(admis) != set(attendus):
            pb.append("%s : comptes %s au lieu de %s" % (z["dossier"], sorted(admis), sorted(attendus)))
        for ident, mdp in attendus.items():
            if ident in admis and not correspond(mdp, admis[ident]):
                pb.append("%s : l'empreinte de « %s » ne correspond pas à son mot de passe"
                          % (z["dossier"], ident))
    return pb


def concordance(acces, zones_destination):
    """Les zones des deux fichiers doivent être les mêmes : une zone protégée ici mais non
    déclarée au déployeur verrait son contenu partir avant sa protection ; l'inverse resterait
    retenue pour toujours."""
    ici = {z["dossier"] + "/" for z in acces["zones"]}
    la = set(zones_destination)
    pb = ["zone « %s » absente de destination.json (zones_protegees)" % z for z in sorted(ici - la)]
    pb += ["zone « %s » déclarée dans destination.json mais sans comptes dans acces-zones.json" % z
           for z in sorted(la - ici)]
    return pb


def statut_sans_identifiant(url):
    """Le code HTTP d'une adresse demandée SANS identifiant : 401 attendu pour une zone protégée."""
    try:
        with urllib.request.urlopen(urllib.request.Request(url, method="GET"), timeout=30) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except urllib.error.URLError as e:
        return "injoignable (%s)" % e.reason


def main(argv=None):
    ap = argparse.ArgumentParser(description="Protection par mot de passe des zones du site.")
    ap.add_argument("--essai", action="store_true", help="se connecte, construit et contrôle, n'envoie rien")
    ap.add_argument("--hors-ligne", action="store_true", dest="hors_ligne",
                    help="construit et contrôle sans se connecter, avec un chemin de compte fictif")
    ap.add_argument("--racine-absolue", dest="racine_absolue",
                    help="chemin absolu du site sur le serveur, si le protocole n'est pas SFTP")
    args = ap.parse_args(argv)

    acces = charger_acces()
    dest = D.charger_destination()
    pb = concordance(acces, dest["zones_protegees"])
    if pb:
        sys.exit("Zones discordantes :\n  " + "\n  ".join(pb))

    if args.hors_ligne:
        contenus = fichiers(acces, RACINE_FICTIVE)
        pb = controler(acces, contenus)
        if pb:
            sys.exit("Protection refusée :\n  " + "\n  ".join(pb))
        print("✓ %d zone(s) construite(s) hors ligne ; empreintes bcrypt contrôlées" % len(acces["zones"]))
        for z in acces["zones"]:
            print("  %s/ : %s" % (z["dossier"], ", ".join(acces["comptes"][q]["identifiant"]
                                                         for q in z["comptes"])))
        print("Hors ligne : rien n'a été envoyé.")
        return 0

    c = D.charger_config()
    jr = D.Journal(args.essai)
    ftp = D.connecter(c, jr)
    try:
        if args.racine_absolue:
            racine, masque = args.racine_absolue, (lambda t: t)
        elif hasattr(ftp, "maison"):
            maison = ftp.maison
            racine = ftp._reel(c["repertoire_distant"])         # le chemin absolu qu'attend Apache
            masque = (lambda t: t.replace(maison, "<dossier personnel>")) if maison else (lambda t: t)
        else:
            sys.exit("Le chemin absolu du site n'est connu qu'en SFTP : passez à « protocole »: "
                     "« sftp », ou indiquez --racine-absolue.")
        autorise, message, carnet = D.garde_identite(ftp, c, adopter=False)
        if not autorise:
            sys.exit("Protection refusée : " + message)
        contenus = fichiers(acces, racine)
        pb = controler(acces, contenus)
        if pb:
            sys.exit("Protection refusée :\n  " + "\n  ".join(pb))
        print("✓ %d zone(s) construite(s) ; empreintes bcrypt contrôlées" % len(acces["zones"]))
        for z in acces["zones"]:
            print("  %s/ : %s  →  %s/%s/.htpasswd"
                  % (z["dossier"], ", ".join(acces["comptes"][q]["identifiant"] for q in z["comptes"]),
                     masque(racine), z["dossier"]))
        if args.essai:
            print("Simulation : rien n'a été envoyé.")
            return 0
        base = c["repertoire_distant"].rstrip("/")
        connus = set()
        if carnet is None:
            # Premier passage, avant tout contenu : le dossier reçoit d'abord le carnet au nom
            # du cours. Sans lui, le déployeur y verrait des dossiers sans carnet et refuserait
            # d'y publier ce cours même.
            D.assurer_repertoire(ftp, base, connus)
            D.ecrire_manifeste_distant(ftp, {}, c, jr)
        for z in acces["zones"]:
            D.assurer_repertoire(ftp, base + "/" + z["dossier"], connus)
        for rel, texte in contenus.items():
            ftp.storbinary("STOR %s/%s" % (base, rel), io.BytesIO(texte.encode("utf-8")))
            relu = io.BytesIO()
            ftp.retrbinary("RETR %s/%s" % (base, rel), relu.write)
            if relu.getvalue().decode("utf-8") != texte:
                sys.exit("Relecture différente pour %s : envoi à refaire" % rel)
            print("  envoyé et relu : %s" % rel)
    finally:
        try:
            ftp.quit()
        except Exception:
            pass

    print("\nVérification sans identifiant (401 attendu) :")
    for z in acces["zones"]:
        url = z.get("verifier") or (dest.get("url", "").rstrip("/") + "/" + z["dossier"] + "/"
                                    if dest.get("url") else "")
        if not url:
            print("  (pas d'adresse pour %s/ : ajoutez « url » à destination.json)" % z["dossier"])
            continue
        code = statut_sans_identifiant(url)
        print("  %s  %s%s" % (code, url, "" if code == 401 else "   ← la zone n'est PAS protégée"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
