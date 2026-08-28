#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Déploiement du site du cours vers un hébergement OVH, par FTP.

    python3 deploiement/deployer.py --essai      # simulation, rien n'est envoyé
    python3 deploiement/deployer.py              # envoi réel
    python3 deploiement/deployer.py --purge      # + suppression des fichiers obsolètes
    python3 deploiement/deployer.py --tout       # ignore le manifeste, réenvoie tout

Le transfert est INCRÉMENTAL. Le site pèse plus de 300 Mo, dont l'essentiel en
podcasts et en slides qui ne changent jamais : tout réenvoyer à chaque
publication prendrait des dizaines de minutes pour rien. On compare donc
l'empreinte SHA-256 de chaque fichier à celle du dernier envoi réussi.

La liste de ce qui part en ligne est celle de Git. C'est volontaire : ce qui est
ignoré par Git — identifiants, PNG sources, fichiers temporaires — ne peut pas
partir par accident. Les exclusions de la configuration retirent ensuite ce qui
est suivi mais n'a rien à faire sur le serveur (docs de production, générateurs).

Aucune dépendance : tout vient de la bibliothèque standard de Python 3.
Testé pour un usage depuis macOS comme depuis Windows.
"""

import argparse
import fnmatch
import ftplib
import hashlib
import io
import json
import os
import ssl
import subprocess
import sys
import time

# La console Windows n'est pas en UTF-8 par défaut : sans cela, les accents des
# messages sortent en charabia. Sans effet sur macOS et Linux, déjà en UTF-8.
for flux in (sys.stdout, sys.stderr):
    try:
        flux.reconfigure(encoding="utf-8")
    except Exception:
        pass

DEPOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Ce qui part en ligne, c'est site/ — et rien d'autre. Les outils, les fiches
# de production, les sources et la documentation restent au depot. Dans le
# cours dont ce template est issu, le site etait la racine et il fallait donc
# une longue liste d'exclusions ; ici la separation est structurelle.
RACINE = os.path.join(DEPOT, "site")
DOSSIER = os.path.join(DEPOT, "deploiement")
CONFIG = os.path.join(DOSSIER, "config.json")
MANIFESTE = os.path.join(DOSSIER, "manifeste.json")

# Le manifeste de référence vit SUR le serveur, pas sur le poste qui envoie.
# Sinon chaque machine tient sa propre comptabilité : la première publication
# depuis un poste neuf réexpédie les 340 Mo déjà en ligne, faute de savoir
# ce que l'autre poste a déjà déposé. Ici, Mac et PC lisent le même carnet.
# Le fichier local ne sert plus que de secours si le serveur est injoignable.
MANIFESTE_DISTANT = ".deploiement-manifeste.json"

# Valeurs du modèle : si elles sont encore là, la configuration n'a pas été remplie.
GABARITS = {"a-remplir", "", "ftp.exemple.ovh.net", "votre-identifiant", "votre-mot-de-passe"}


# ---------------------------------------------------------------- affichage
def humain(n):
    for unite in ("o", "Ko", "Mo", "Go"):
        if n < 1024 or unite == "Go":
            return "%.1f %s" % (n, unite) if unite != "o" else "%d o" % n
        n /= 1024.0


def duree(s):
    s = int(s)
    return "%d min %02d s" % (s // 60, s % 60) if s >= 60 else "%d s" % s


class Journal(object):
    """Sorties lisibles, et jamais un mot de passe dedans."""

    def __init__(self, essai):
        self.essai = essai

    def titre(self, t):
        print("\n%s\n%s" % (t, "-" * len(t)))

    def info(self, t):
        print("  " + t)

    def action(self, t):
        print(("  [simulation] " if self.essai else "  ") + t)

    def alerte(self, t):
        print("  /!\\ " + t)


# ---------------------------------------------------------------- configuration
def charger_config():
    if not os.path.isfile(CONFIG):
        modele = os.path.join(DOSSIER, "config.exemple.json")
        sys.exit(
            "Configuration absente : %s\n"
            "Copiez le modèle puis renseignez-le :\n"
            "    cp %s %s" % (CONFIG, modele, CONFIG))
    with open(CONFIG, encoding="utf-8") as f:
        try:
            c = json.load(f)
        except ValueError as e:
            sys.exit("Configuration illisible (%s) : %s" % (CONFIG, e))

    obligatoires = ("hote", "identifiant", "motdepasse", "repertoire_distant")
    for cle in obligatoires:
        if cle not in c:
            sys.exit("Configuration : la clé « %s » manque." % cle)
        if str(c[cle]).strip() in GABARITS:
            sys.exit("Configuration : « %s » est resté sur la valeur du modèle." % cle)

    distant = "/" + str(c["repertoire_distant"]).strip().strip("/")
    # Garde-fou : --purge sur la racine du serveur effacerait le site entier,
    # y compris ce que ce dépôt ne connaît pas.
    if distant in ("/", "/www", "/htdocs", "/public_html"):
        sys.exit("Configuration : « repertoire_distant » (%s) est une racine "
                 "d'hébergement. Visez un sous-répertoire dédié au cours." % distant)
    c["repertoire_distant"] = distant
    c.setdefault("port", 21)
    c.setdefault("tls", True)
    c.setdefault("passif", True)
    c.setdefault("exclure", [])
    c.setdefault("delai", 30)
    return c


# ---------------------------------------------------------------- inventaire local
def fichiers_suivis():
    """Chemins relatifs suivis par Git, en séparateurs POSIX."""
    try:
        sortie = subprocess.check_output(
            ["git", "-C", RACINE, "ls-files"], stderr=subprocess.STDOUT)
    except (OSError, subprocess.CalledProcessError):
        sys.exit("Git est introuvable, ou ce dossier n'est pas un dépôt.\n"
                 "Le script s'appuie sur « git ls-files » pour savoir quoi publier.")
    out = []
    for ligne in sortie.decode("utf-8").splitlines():
        ligne = ligne.strip()
        if ligne and os.path.isfile(os.path.join(RACINE, ligne)):
            out.append(ligne)
    return out


def exclu(chemin, motifs):
    for m in motifs:
        if fnmatch.fnmatch(chemin, m) or chemin.startswith(m.rstrip("*").rstrip("/") + "/"):
            return True
    return False


def empreinte(absolu):
    h = hashlib.sha256()
    with open(absolu, "rb") as f:
        for bloc in iter(lambda: f.read(262144), b""):
            h.update(bloc)
    return h.hexdigest()


# ---------------------------------------------------------------- manifeste
def lire_manifeste():
    if not os.path.isfile(MANIFESTE):
        return {}
    try:
        with open(MANIFESTE, encoding="utf-8") as f:
            return json.load(f).get("fichiers", {})
    except ValueError:
        return {}


def ecrire_manifeste(fichiers, hote, distant):
    tmp = MANIFESTE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(corps_manifeste(fichiers, hote, distant), f, ensure_ascii=False, indent=1)
    os.replace(tmp, MANIFESTE)


def nom_poste():
    """Nom de la machine, pour savoir d'où est parti le dernier envoi."""
    try:
        import socket
        return socket.gethostname()
    except Exception:
        return os.environ.get("COMPUTERNAME") or "?"


def corps_manifeste(fichiers, hote, distant):
    return {"hote": hote, "repertoire_distant": distant,
            "horodatage": time.strftime("%Y-%m-%d %H:%M:%S"),
            "dernier_envoi_depuis": nom_poste(),
            "fichiers": fichiers}


def lire_manifeste_distant(ftp, base, jr):
    """Le carnet tel que le serveur le connaît. None si absent ou illisible."""
    tampon = io.BytesIO()
    try:
        ftp.retrbinary("RETR " + base + "/" + MANIFESTE_DISTANT, tampon.write)
    except ftplib.error_perm:
        return None                       # 550 : pas encore de carnet, première fois
    except ftplib.all_errors as e:
        jr.alerte("carnet distant illisible (%s)" % e)
        return None
    try:
        donnees = json.loads(tampon.getvalue().decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        jr.alerte("carnet distant corrompu : il sera reconstruit.")
        return None
    return donnees.get("fichiers", {})


def ecrire_manifeste_distant(ftp, base, fichiers, hote, jr):
    brut = json.dumps(corps_manifeste(fichiers, hote, base),
                      ensure_ascii=False, indent=1).encode("utf-8")
    try:
        ftp.storbinary("STOR " + base + "/" + MANIFESTE_DISTANT, io.BytesIO(brut))
        return True
    except ftplib.all_errors as e:
        jr.alerte("le carnet distant n'a pas pu être mis à jour (%s).\n"
                  "      Le prochain envoi renverra peut-être des fichiers déjà en ligne." % e)
        return False


# ---------------------------------------------------------------- FTP
def contexte_ssl():
    """Magasin de certificats fiable, quelle que soit l'installation de Python.

    Sur macOS, Python n'utilise pas le trousseau du système : une installation
    venue de python.org sans son « Install Certificates.command » échoue avec
    CERTIFICATE_VERIFY_FAILED. Le paquet certifi porte le magasin qu'il faut.
    """
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return ssl.create_default_context()



def diagnostic(e):
    """Message utile quand l'échec vient du magasin de certificats."""
    if "CERTIFICATE_VERIFY_FAILED" not in str(e):
        return ""
    return ("\n      Votre installation de Python n'a pas de magasin de certificats"
            "\n      utilisable — fréquent sur macOS. Installez-le puis relancez :"
            "\n          python3 -m pip install --upgrade certifi"
            "\n      Si Python vient de python.org, exécutez aussi, une fois :"
            "\n          open \"/Applications/Python %d.%d/Install Certificates.command\""
            % (sys.version_info.major, sys.version_info.minor))


def connecter(c, jr):
    adresse = "%s:%s" % (c["hote"], c["port"])
    if c["tls"]:
        # FTPS explicite : OVH le propose, et sans lui identifiants comme
        # contenus circulent en clair sur le réseau.
        ftp = ftplib.FTP_TLS(context=contexte_ssl(), timeout=c["delai"])
    else:
        ftp = ftplib.FTP(timeout=c["delai"])
    ftp.connect(c["hote"], int(c["port"]))
    ftp.login(c["identifiant"], c["motdepasse"])
    if c["tls"]:
        ftp.prot_p()                      # chiffre aussi le canal de données
    ftp.set_pasv(bool(c["passif"]))
    try:
        ftp.encoding = "utf-8"
        ftp.sendcmd("OPTS UTF8 ON")
    except Exception:
        pass                              # serveur sans UTF-8 : on continue
    jr.info("connecté à %s en %s" % (adresse, "FTPS" if c["tls"] else "FTP (non chiffré)"))
    return ftp


def assurer_repertoire(ftp, chemin, connus):
    """Crée l'arborescence distante si besoin. `connus` évite de réessayer."""
    if chemin in connus:
        return
    parties = [p for p in chemin.strip("/").split("/") if p]
    courant = ""
    for p in parties:
        courant += "/" + p
        if courant in connus:
            continue
        try:
            ftp.mkd(courant)
        except ftplib.error_perm as e:
            # 550 = existe déjà, ce n'est pas une erreur ici
            if not str(e).startswith("550"):
                raise
        connus.add(courant)
    connus.add(chemin)


def envoyer(ftp, absolu, distant, taille, jr):
    envoye = [0]
    largeur = 28

    def bloc(donnees):
        envoye[0] += len(donnees)
        if taille > 1048576:              # barre seulement pour les gros fichiers
            part = envoye[0] / float(taille)
            plein = int(part * largeur)
            sys.stdout.write("\r    [%s%s] %3d %%"
                             % ("#" * plein, "." * (largeur - plein), int(part * 100)))
            sys.stdout.flush()

    with open(absolu, "rb") as f:
        ftp.storbinary("STOR " + distant, f, blocksize=262144, callback=bloc)
    if taille > 1048576:
        sys.stdout.write("\r" + " " * (largeur + 12) + "\r")
        sys.stdout.flush()


def lister_distant(ftp, base, jr):
    """Tous les fichiers présents sous `base`, en chemins relatifs."""
    trouves = []

    def descendre(chemin):
        entrees = []
        try:
            entrees = list(ftp.mlsd(chemin))
        except Exception:
            try:
                noms = ftp.nlst(chemin)
            except Exception:
                return
            for n in noms:
                nom = n.rsplit("/", 1)[-1]
                if nom in (".", ".."):
                    continue
                # sans MLSD, on distingue dossier et fichier en essayant d'entrer
                sous = chemin + "/" + nom
                try:
                    ftp.cwd(sous)
                    descendre(sous)
                except ftplib.error_perm:
                    trouves.append(sous)
            return
        for nom, faits in entrees:
            if nom in (".", ".."):
                continue
            sous = chemin + "/" + nom
            if faits.get("type") == "dir":
                descendre(sous)
            elif faits.get("type") == "file":
                trouves.append(sous)

    descendre(base)
    n = len(base)
    return [t[n:].lstrip("/") for t in trouves]


# ---------------------------------------------------------------- programme
def main():
    ap = argparse.ArgumentParser(
        description="Déploie le site du cours vers l'hébergement OVH par FTP.")
    ap.add_argument("--essai", action="store_true",
                    help="simulation : affiche ce qui serait envoyé, n'envoie rien")
    ap.add_argument("--tout", action="store_true",
                    help="ignore le manifeste et réenvoie tous les fichiers")
    ap.add_argument("--purge", action="store_true",
                    help="supprime en ligne les fichiers absents du dépôt (demande confirmation)")
    ap.add_argument("--purge-confirme", action="store_true", dest="purge_confirme",
                    help="purge sans poser de question — pour un lancement non interactif")
    args = ap.parse_args()
    if args.purge_confirme:
        args.purge = True

    jr = Journal(args.essai)
    c = charger_config()
    base = c["repertoire_distant"]

    jr.titre("Inventaire")
    tous = fichiers_suivis()
    retenus = [f for f in tous if not exclu(f, c["exclure"])]
    jr.info("%d fichiers suivis par Git, %d retenus après exclusions"
            % (len(tous), len(retenus)))

    # --- on se connecte AVANT de comparer, y compris en simulation : le carnet
    #     de référence est sur le serveur, et une simulation qui devine ne sert
    #     à rien. Sans connexion on retombe sur le carnet local, en le disant.
    ftp = None
    if not args.tout:
        jr.titre("Connexion")
        try:
            ftp = connecter(c, jr)
        except ftplib.all_errors as e:
            if not args.essai:
                jr.alerte("connexion impossible : %s%s" % (e, diagnostic(e)))
                return 2
            jr.alerte("connexion impossible (%s).%s" % (e, diagnostic(e)))
            jr.info("simulation poursuivie d'après le carnet local, qui peut être en retard.")

    if args.tout:
        manifeste = {}
        jr.info("option --tout : le carnet est ignoré, tout sera renvoyé.")
    else:
        manifeste = lire_manifeste_distant(ftp, base, jr) if ftp else None
        if manifeste is None:
            manifeste = lire_manifeste()
            jr.info("aucun carnet sur le serveur : lecture du carnet local (%d entrées)."
                    % len(manifeste))
        else:
            jr.info("carnet lu sur le serveur : %d fichiers déjà en ligne." % len(manifeste))

    jr.titre("Comparaison")
    a_envoyer, inchanges, poids = [], 0, 0
    courant = {}
    for rel in retenus:
        absolu = os.path.join(RACINE, rel.replace("/", os.sep))
        taille = os.path.getsize(absolu)
        sha = empreinte(absolu)
        courant[rel] = {"sha": sha, "taille": taille}
        if manifeste.get(rel, {}).get("sha") == sha:
            inchanges += 1
        else:
            a_envoyer.append((rel, absolu, taille))
            poids += taille

    jr.info("%d inchangés, %d à envoyer (%s)"
            % (inchanges, len(a_envoyer), humain(poids)))

    def raccrocher():
        if not ftp:
            return
        try:
            ftp.quit()
        except Exception:
            try:
                ftp.close()
            except Exception:
                pass

    if not a_envoyer and not args.purge:
        jr.info("le site en ligne est déjà à jour.")
        raccrocher()
        return 0

    if args.essai:
        jr.titre("Simulation")
        for rel, _a, taille in a_envoyer[:40]:
            jr.action("%s  (%s)" % (rel, humain(taille)))
        if len(a_envoyer) > 40:
            jr.info("… et %d autres fichiers" % (len(a_envoyer) - 40))
        jr.info("destination : %s%s" % (c["hote"], base))
        jr.info("rien n'a été envoyé.")
        raccrocher()
        return 0

    if ftp is None:                       # cas --tout : la connexion reste à ouvrir
        jr.titre("Connexion")
        try:
            ftp = connecter(c, jr)
        except ftplib.all_errors as e:
            jr.alerte("connexion impossible : %s%s" % (e, diagnostic(e)))
            return 2

    connus = set()
    envoyes, echecs, cumul = 0, [], 0
    depart = time.time()

    try:
        assurer_repertoire(ftp, base, connus)
        jr.titre("Envoi")
        for i, (rel, absolu, taille) in enumerate(a_envoyer, 1):
            cible = base + "/" + rel
            assurer_repertoire(ftp, cible.rsplit("/", 1)[0], connus)
            jr.info("[%d/%d] %s  (%s)" % (i, len(a_envoyer), rel, humain(taille)))
            try:
                envoyer(ftp, absolu, cible, taille, jr)
                envoyes += 1
                cumul += taille
                # Carnet tenu au fil de l'eau : une coupure au milieu de 340 Mo
                # ne doit pas obliger à tout réenvoyer. Le local est gratuit, on
                # l'écrit à chaque fichier ; le distant coûte un aller-retour FTP,
                # on le publie tous les 25 fichiers et à la fin.
                partiel = dict(manifeste)
                partiel.update({r: courant[r] for r, _a, _t in a_envoyer[:i]})
                ecrire_manifeste(partiel, c["hote"], base)
                if i % 25 == 0:
                    ecrire_manifeste_distant(ftp, base, partiel, c["hote"], jr)
            except ftplib.all_errors as e:
                echecs.append((rel, str(e)))
                jr.alerte("échec sur %s : %s" % (rel, e))

        # ---- purge éventuelle
        if args.purge:
            jr.titre("Fichiers obsolètes en ligne")
            distants = lister_distant(ftp, base, jr)
            locaux = set(retenus)
            # le carnet n'est pas un fichier du site : il ne doit jamais être purgé
            obsoletes = sorted(d for d in distants
                               if d and d not in locaux and d != MANIFESTE_DISTANT)
            if not obsoletes:
                jr.info("aucun.")
            else:
                for o in obsoletes:
                    jr.info(o)
                if args.purge_confirme:
                    rep = "oui"
                    jr.info("--purge-confirme : suppression sans question.")
                else:
                    rep = input("\n  Supprimer ces %d fichiers en ligne ? [oui/NON] "
                                % len(obsoletes)).strip().lower()
                if rep == "oui":
                    for o in obsoletes:
                        try:
                            ftp.delete(base + "/" + o)
                            jr.action("supprimé : %s" % o)
                        except ftplib.all_errors as e:
                            jr.alerte("suppression impossible (%s) : %s" % (o, e))
                else:
                    jr.info("suppression annulée.")

        if not echecs:
            ecrire_manifeste_distant(ftp, base, courant, c["hote"], jr)
    finally:
        raccrocher()

    if not echecs:
        ecrire_manifeste(courant, c["hote"], base)

    jr.titre("Bilan")
    jr.info("%d fichiers envoyés, %s en %s" % (envoyes, humain(cumul), duree(time.time() - depart)))
    if echecs:
        jr.alerte("%d échec(s) — ces fichiers seront repris au prochain lancement :" % len(echecs))
        for rel, e in echecs[:10]:
            jr.info("%s : %s" % (rel, e))
        return 1
    jr.info("site à jour sur %s%s" % (c["hote"], base))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n  interrompu. Les fichiers déjà envoyés sont notés : "
              "relancez pour reprendre où vous en étiez.")
        sys.exit(130)
