#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Déploiement du site du cours vers un hébergement OVH, par SFTP (ou FTPS / FTP).

    python3 deploiement/deployer.py --essai      # simulation, rien n'est envoyé
    python3 deploiement/deployer.py              # envoi réel
    python3 deploiement/deployer.py --purge      # + suppression des fichiers obsolètes
    python3 deploiement/deployer.py --tout       # ignore le carnet, réenvoie tout
    python3 deploiement/deployer.py --adopter    # reprend un dossier déjà publié par un autre outil

DEUX FICHIERS, DEUX RÔLES.

  deploiement/config.json       les ACCÈS à l'hébergement : hôte, identifiant, mot de passe,
                                protocole. Secret, ignoré par Git, identique d'un cours à
                                l'autre : on le recopie tel quel, sans l'ouvrir.
  deploiement/destination.json  OÙ VA CE COURS : son identifiant et son répertoire distant.
                                Sans secret, versionné avec le cours, écrit par nouveau_cours.py.

Le répertoire distant ne vient JAMAIS de config.json. Recopiée d'un cours à l'autre, cette
configuration désigne encore le dossier du cours précédent : le premier envoi du nouveau cours
l'aurait écrasé, et la première purge l'aurait vidé.

LE GARDE-FOU D'IDENTITÉ. Le carnet des envois, déposé sur le serveur, porte l'identifiant du
cours. Avant d'écrire quoi que ce soit, le script vérifie que le dossier distant est vide ou
qu'il appartient à ce cours ; sinon il refuse. Un dossier publié par un autre outil — carnet
sans identifiant, ou fichiers sans carnet — ne se reprend qu'avec --adopter. Un dossier situé
À L'INTÉRIEUR d'un cours déjà publié est toujours refusé : la purge de ce cours l'effacerait.

LES PROTECTIONS DU SERVEUR. Un mot de passe (.htaccess, .htpasswd) ou un réglage d'hébergement
(.user.ini, .ovhconfig) posés côté serveur ne sont jamais écrasés ni purgés. Les zones protégées
déclarées dans destination.json — une correction de TP, par exemple — ne partent que si leur
.htaccess est déjà en ligne : deploiement/proteger_zones.py le pose.

Le transfert est INCRÉMENTAL. Capsules audio, polycopiés et schémas ne changent presque jamais :
tout réenvoyer à chaque correction de texte serait du temps perdu. On compare donc l'empreinte
SHA-256 de chaque fichier à celle du dernier envoi réussi.

La liste de ce qui part en ligne est celle de Git, limitée à site/. C'est volontaire : ce qui est
ignoré par Git — identifiants, PNG sources, fichiers temporaires — ne peut pas partir par
accident, et les outils, les fiches de production, les sources et la documentation restent au
dépôt par construction.

Dépendance : paramiko pour le SFTP (python3 -m pip install paramiko) ; FTP et FTPS n'utilisent
que la bibliothèque standard. Testé depuis macOS comme depuis Windows. Tests hors ligne du
garde-fou et des protections : python3 deploiement/tester_deployer.py
"""

import argparse
import fnmatch
import ftplib
import hashlib
import io
import json
import os
import re
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
# de production, les sources et la documentation restent au depot. Dans les
# cours dont ce template est issu, le site etait la racine et il fallait donc
# une longue liste d'exclusions ; ici la separation est structurelle.
RACINE = os.path.join(DEPOT, "site")
DOSSIER = os.path.join(DEPOT, "deploiement")
CONFIG = os.path.join(DOSSIER, "config.json")
DESTINATION = os.path.join(DOSSIER, "destination.json")
MANIFESTE = os.path.join(DOSSIER, "manifeste.json")
CONNUS = os.path.join(DOSSIER, "known_hosts")

# Le manifeste de référence vit SUR le serveur, pas sur le poste qui envoie.
# Sinon chaque machine tient sa propre comptabilité : la première publication
# depuis un poste neuf réexpédie les centaines de Mo déjà en ligne, faute de
# savoir ce que l'autre poste a déjà déposé. Ici, Mac et PC lisent le même
# carnet. Le fichier local ne sert plus que de secours si le serveur est
# injoignable.
MANIFESTE_DISTANT = ".deploiement-manifeste.json"

# Protections plancher, ajoutées à celles de la configuration : même une
# configuration incomplète ne doit pas pouvoir faire tomber le mot de passe du
# cours ni les réglages PHP de l'hébergement. Un motif sans « / » vise le nom
# du fichier dans n'importe quel dossier.
PROTEGES_TOUJOURS = (".htaccess", ".htpasswd", ".user.ini", ".ovhconfig")

# Exclusions plancher, relatives à site/ : du code ou des reliquats de poste
# n'ont rien à faire sur un serveur, quelle que soit la configuration.
EXCLUS_TOUJOURS = ("*.py", "*.pyc", ".DS_Store", "Thumbs.db", "desktop.ini", "_tmp*")

# Valeurs des modèles : si elles sont encore là, le fichier n'a pas été rempli.
GABARITS = {"a-remplir", "", "ftp.exemple.ovh.net", "votre-identifiant", "votre-mot-de-passe",
            "mon-cours", "/www/chemin/du-cours"}

# Racines d'hébergement : un cours ne s'y publie jamais, une purge y effacerait
# tout ce que ce dépôt ne connaît pas.
RACINES_HEBERGEMENT = ("/", "/www", "/htdocs", "/public_html")

# Codes de sortie, pour un lancement non interactif.
OK, ECHECS, CONNEXION, REFUS = 0, 1, 2, 3


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
def lire_json(chemin, modele):
    if not os.path.isfile(chemin):
        sys.exit("Fichier absent : %s\n"
                 "Copiez le modèle puis renseignez-le :\n"
                 "    cp %s %s" % (chemin, modele, chemin))
    with open(chemin, encoding="utf-8") as f:
        try:
            return json.load(f)
        except ValueError as e:
            sys.exit("Fichier illisible (%s) : %s" % (os.path.basename(chemin), e))


def charger_config():
    """Les accès (config.json) et la destination (destination.json), réunis."""
    c = lire_json(CONFIG, os.path.join(DOSSIER, "config.exemple.json"))
    for cle in ("hote", "identifiant", "motdepasse"):
        if cle not in c:
            sys.exit("config.json : la clé « %s » manque." % cle)
        if str(c[cle]).strip() in GABARITS:
            sys.exit("config.json : « %s » est resté sur la valeur du modèle." % cle)
    c["repertoire_distant_ignore"] = bool(str(c.pop("repertoire_distant", "")).strip())

    c.setdefault("tls", True)
    # « sftp » (SSH), « ftps » (FTP chiffré) ou « ftp ». Sans la clé, les
    # anciennes configurations gardent leur comportement : tls vaut ftps.
    c.setdefault("protocole", "ftps" if c["tls"] else "ftp")
    c["protocole"] = str(c["protocole"]).lower()
    if c["protocole"] not in ("sftp", "ftps", "ftp"):
        sys.exit("config.json : « protocole » doit valoir sftp, ftps ou ftp.")
    c["tls"] = c["protocole"] == "ftps"
    c.setdefault("port", 22 if c["protocole"] == "sftp" else 21)
    if c["protocole"] == "sftp" and int(c["port"]) == 21:
        c["port"] = 22                    # le port 21 est celui du FTP, jamais du SSH
    c.setdefault("passif", True)
    c.setdefault("delai", 30)

    d = charger_destination()
    c["cours"] = d["cours"]
    c["repertoire_distant"] = d["repertoire_distant"]
    c["url"] = d.get("url", "")
    c["zones"] = d["zones_protegees"]
    c["exclure"] = sorted(set(c.get("exclure", [])) | set(d.get("exclure", [])) | set(EXCLUS_TOUJOURS))
    c["proteger"] = sorted(set(c.get("proteger", [])) | set(d.get("proteger", []))
                           | set(PROTEGES_TOUJOURS))
    return c


def charger_destination():
    """Où va CE cours. Refuse tôt et clairement plutôt que de viser au hasard."""
    d = lire_json(DESTINATION, os.path.join(DOSSIER, "destination.exemple.json"))
    for cle in ("cours", "repertoire_distant"):
        if str(d.get(cle, "")).strip() in GABARITS:
            sys.exit("destination.json : « %s » est vide ou resté sur la valeur du modèle." % cle)
    cours = str(d["cours"]).strip()
    if not re.match(r"^[a-z0-9][a-z0-9-]*$", cours):
        sys.exit("destination.json : « cours » ne doit contenir que des minuscules, chiffres et "
                 "tirets (lu : %r)." % cours)
    distant = "/" + str(d["repertoire_distant"]).strip().strip("/")
    if distant in RACINES_HEBERGEMENT:
        sys.exit("destination.json : « repertoire_distant » (%s) est une racine d'hébergement. "
                 "Visez un sous-répertoire dédié au cours." % distant)
    if ".." in distant.split("/"):
        sys.exit("destination.json : « repertoire_distant » ne doit pas contenir « .. ».")
    zones = []
    for z in d.get("zones_protegees") or []:
        z = str(z).strip().strip("/")
        if not z or ".." in z.split("/"):
            sys.exit("destination.json : zone protégée invalide : %r" % z)
        zones.append(z + "/")
    d["cours"], d["repertoire_distant"], d["zones_protegees"] = cours, distant, sorted(set(zones))
    return d


# ---------------------------------------------------------------- inventaire local
def fichiers_suivis():
    """Chemins relatifs à site/, suivis par Git, en séparateurs POSIX."""
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


def protege(chemin, motifs):
    """Vrai pour un fichier que le serveur garde quoi qu'il arrive.
    Un motif sans « / » vise le nom du fichier dans n'importe quel dossier."""
    nom = chemin.rsplit("/", 1)[-1]
    for m in motifs:
        if ("/" not in m and fnmatch.fnmatch(nom, m)) or fnmatch.fnmatch(chemin, m):
            return True
    return False


def empreinte(absolu):
    h = hashlib.sha256()
    with open(absolu, "rb") as f:
        for bloc in iter(lambda: f.read(262144), b""):
            h.update(bloc)
    return h.hexdigest()


# ---------------------------------------------------------------- manifeste
def lire_manifeste(cours):
    """Le carnet local, s'il est bien celui de ce cours."""
    if not os.path.isfile(MANIFESTE):
        return {}
    try:
        with open(MANIFESTE, encoding="utf-8") as f:
            donnees = json.load(f)
    except ValueError:
        return {}
    if donnees.get("cours") not in (None, cours):
        return {}
    return donnees.get("fichiers", {})


def nom_poste():
    """Nom de la machine, pour savoir d'où est parti le dernier envoi."""
    try:
        import socket
        return socket.gethostname()
    except Exception:
        return os.environ.get("COMPUTERNAME") or "?"


def corps_manifeste(fichiers, c):
    return {"cours": c["cours"], "hote": c["hote"], "repertoire_distant": c["repertoire_distant"],
            "horodatage": time.strftime("%Y-%m-%d %H:%M:%S"),
            "dernier_envoi_depuis": nom_poste(),
            "fichiers": fichiers}


def ecrire_manifeste(fichiers, c):
    tmp = MANIFESTE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(corps_manifeste(fichiers, c), f, ensure_ascii=False, indent=1)
    os.replace(tmp, MANIFESTE)


def lire_carnet(ftp, dossier):
    """Le carnet déposé dans `dossier` : (« absent » | « illisible » | « ok », données)."""
    tampon = io.BytesIO()
    try:
        ftp.retrbinary("RETR " + dossier.rstrip("/") + "/" + MANIFESTE_DISTANT, tampon.write)
    except ftplib.all_errors:
        # 550 en FTP, fichier absent en SFTP — ou dossier illisible : dans les
        # deux cas, aucun carnet que l'on puisse prendre en compte.
        return "absent", None
    try:
        donnees = json.loads(tampon.getvalue().decode("utf-8"))
        if not isinstance(donnees, dict):
            raise ValueError("pas un objet JSON")
    except (ValueError, UnicodeDecodeError):
        return "illisible", None
    return "ok", donnees


def ecrire_manifeste_distant(ftp, fichiers, c, jr):
    brut = json.dumps(corps_manifeste(fichiers, c), ensure_ascii=False, indent=1).encode("utf-8")
    try:
        ftp.storbinary("STOR " + c["repertoire_distant"] + "/" + MANIFESTE_DISTANT, io.BytesIO(brut))
        return True
    except ftplib.all_errors as e:
        jr.alerte("le carnet distant n'a pas pu être mis à jour (%s).\n"
                  "      Le prochain envoi renverra peut-être des fichiers déjà en ligne." % e)
        return False


# ---------------------------------------------------------------- garde-fou
def ancetres(distant):
    """/www/a/b/c → ['/www/a/b', '/www/a', '/www'] : les dossiers qui contiennent la cible."""
    parties = [p for p in distant.strip("/").split("/") if p]
    return ["/" + "/".join(parties[:i]) for i in range(len(parties) - 1, 0, -1)]


def lister_entrees(ftp, chemin):
    """Les noms présents dans `chemin` (sans descendre), ou None si le dossier n'existe pas.

    Un dossier qui existe mais ne se lit pas lève une erreur, au lieu de passer
    pour absent : on ne publie pas à l'aveugle dans un dossier qu'on ne voit pas.
    """
    try:
        return [n for n, _f in ftp.mlsd(chemin) if n not in (".", "..")]
    except FileNotFoundError:
        return None                       # SFTP : le dossier n'existe pas
    except ftplib.error_perm:
        pass                              # FTP : dossier absent, ou serveur sans MLSD
    try:
        noms = ftp.nlst(chemin)
    except ftplib.error_perm:
        return None                       # 550 : le dossier n'existe pas
    return [n.rsplit("/", 1)[-1] for n in noms if n.rsplit("/", 1)[-1] not in (".", "..")]


def garde_identite(ftp, c, adopter):
    """(autorisé, message, fichiers du carnet distant ou None).

    Un dossier distant se publie s'il est vide, absent, ou déjà marqué au nom de
    ce cours. Tout autre cas demande une décision humaine : un cours écrasé par
    un autre ne se voit qu'une fois en ligne, par les étudiants.
    """
    base, cours = c["repertoire_distant"], c["cours"]

    for a in ancetres(base):
        etat, donnees = lire_carnet(ftp, a)
        if etat != "absent":
            autre = (donnees or {}).get("cours") or "sans identifiant"
            return (False, "le dossier visé est À L'INTÉRIEUR d'un site déjà publié dans %s "
                           "(cours « %s ») : sa prochaine purge l'effacerait. Choisissez un "
                           "dossier à part dans destination.json." % (a, autre), None)

    etat, donnees = lire_carnet(ftp, base)
    if etat == "ok":
        autre = donnees.get("cours")
        if autre == cours:
            return True, "dossier distant reconnu : il appartient à ce cours.", donnees.get("fichiers", {})
        if autre:
            return (False, "le dossier distant appartient au cours « %s », pas à « %s ». "
                           "Vérifiez destination.json." % (autre, cours), None)
        if adopter:
            return True, "dossier repris (--adopter) : le carnet portera désormais ce cours.", \
                donnees.get("fichiers", {})
        return (False, "le dossier distant porte un carnet SANS identifiant de cours : un site y a "
                       "été publié par un autre outil. Si c'est bien ce cours, relancez avec "
                       "--adopter.", None)
    if etat == "illisible":
        if adopter:
            return True, "dossier repris (--adopter), carnet illisible : tout sera renvoyé.", {}
        return (False, "le carnet du dossier distant est illisible : impossible de savoir à quel "
                       "cours il appartient. Si c'est bien ce cours, relancez avec --adopter.", None)

    try:
        noms = lister_entrees(ftp, base)
    except ftplib.all_errors as e:
        return False, "le dossier distant existe peut-être, mais ne se lit pas (%s)." % e, None
    if noms is None:
        return True, "dossier distant absent : il sera créé (premier envoi).", None
    occupants = sorted(n for n in noms if not protege(n, c["proteger"]))
    if not occupants:
        return True, "dossier distant vide : premier envoi.", None
    if adopter:
        return True, "dossier repris (--adopter) : %d élément(s) déjà présent(s)." % len(occupants), None
    return (False, "le dossier distant n'est pas vide et n'a pas de carnet (%s%s) : un autre site "
                   "y vit peut-être. Si c'est bien ce cours, relancez avec --adopter."
            % (", ".join(occupants[:5]), "…" if len(occupants) > 5 else ""), None)


def protection_en_place(ftp, base, zone):
    """Vrai si le .htaccess de la zone est en ligne et demande un mot de passe."""
    tampon = io.BytesIO()
    try:
        ftp.retrbinary("RETR %s/%s.htaccess" % (base.rstrip("/"), zone), tampon.write)
    except ftplib.all_errors:
        return False
    texte = tampon.getvalue()
    return b"AuthUserFile" in texte and b"Require valid-user" in texte


def retenir_zones(a_envoyer, zones, ftp, base):
    """(à envoyer, retenus, zones sans protection) : un fichier d'une zone protégée ne part que si
    chaque zone qui le contient est protégée en ligne — la protection d'abord, le contenu ensuite."""
    concernees = sorted({z for rel, _a, _t in a_envoyer for z in zones if rel.startswith(z)})
    manquantes = [z for z in concernees if not (ftp and protection_en_place(ftp, base, z))]
    if not manquantes:
        return a_envoyer, [], []
    garde = [x for x in a_envoyer if not any(x[0].startswith(z) for z in manquantes)]
    retenus = [x for x in a_envoyer if any(x[0].startswith(z) for z in manquantes)]
    return garde, retenus, manquantes


# ---------------------------------------------------------------- connexion
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


class SFTPCommeFTP(object):
    """Le SFTP (SSH), présenté avec les quelques opérations FTP dont le script
    se sert : le reste du déploiement — carnet, garde-fou, comparaison, purge —
    ne sait pas par quel canal passent les fichiers.

    POURQUOI LE SFTP. L'hébergement mutualisé OVH refuse le FTPS (« 500 This
    security scheme is not implemented ») mais ouvre SSH : c'est la seule voie
    où mot de passe et contenus ne circulent pas en clair.

    LES CHEMINS. En FTP, OVH enferme l'utilisateur à la racine de son compte :
    « /www/… » y désigne le site. En SFTP, la racine est celle du serveur et le
    compte vit dans un dossier personnel. Un chemin absolu dont le premier
    dossier n'existe pas à la racine du serveur est donc lu à partir du dossier
    personnel : la même destination sert aux deux protocoles.

    L'EMPREINTE DU SERVEUR est retenue au premier contact dans
    deploiement/known_hosts, puis exigée : un serveur qui change d'empreinte
    fait échouer la connexion au lieu de recevoir le mot de passe.
    """

    def __init__(self, c, jr):
        import paramiko
        self.client = paramiko.SSHClient()
        if os.path.isfile(CONNUS):
            self.client.load_host_keys(CONNUS)
        nouveau = []

        class Retenir(paramiko.MissingHostKeyPolicy):
            def missing_host_key(self, client, hote, cle):
                client.get_host_keys().add(hote, cle.get_name(), cle)
                client.save_host_keys(CONNUS)
                nouveau.append((cle.get_name(), cle.get_fingerprint().hex(":")))

        self.client.set_missing_host_key_policy(Retenir())
        try:
            self.client.connect(c["hote"], port=int(c["port"]), username=c["identifiant"],
                                password=c["motdepasse"], timeout=c["delai"],
                                banner_timeout=c["delai"], auth_timeout=c["delai"],
                                allow_agent=False, look_for_keys=False)
        except paramiko.BadHostKeyException as e:
            raise OSError("l'empreinte du serveur a changé depuis le dernier envoi (%s). "
                          "Vérifiez auprès d'OVH avant de supprimer deploiement/known_hosts." % e)
        except paramiko.AuthenticationException:
            raise OSError("identifiant ou mot de passe refusé par le serveur SSH")
        except paramiko.SSHException as e:
            raise OSError("échec de la connexion SSH : %s" % e)
        if nouveau:
            jr.info("empreinte du serveur retenue (%s %s) dans deploiement/known_hosts"
                    % nouveau[0])
        self.sftp = self.client.open_sftp()
        self.maison = self.sftp.normalize(".")
        self._racine = None

    def _reel(self, chemin):
        """Chemin du serveur correspondant à un chemin « à la FTP »."""
        if self._racine is None:
            premier = "/" + chemin.strip("/").split("/")[0]
            try:
                self.sftp.stat(premier)
                self._racine = ""                 # le chemin existe tel quel
            except IOError:
                self._racine = self.maison        # lu depuis le dossier personnel
        if not self._racine:
            return chemin
        return self._racine.rstrip("/") + "/" + chemin.lstrip("/")

    @staticmethod
    def _chemin(commande):
        return commande.split(" ", 1)[1] if " " in commande else commande

    def retrbinary(self, commande, rappel):
        try:
            with self.sftp.open(self._reel(self._chemin(commande)), "rb") as f:
                while True:
                    bloc = f.read(262144)
                    if not bloc:
                        break
                    rappel(bloc)
        except FileNotFoundError:
            raise ftplib.error_perm("550 fichier absent")

    def storbinary(self, commande, fichier, blocksize=262144, callback=None):
        with self.sftp.open(self._reel(self._chemin(commande)), "wb") as f:
            f.set_pipelined(True)
            while True:
                bloc = fichier.read(blocksize)
                if not bloc:
                    break
                f.write(bloc)
                if callback:
                    callback(bloc)

    def mkd(self, chemin):
        reel = self._reel(chemin)
        try:
            self.sftp.mkdir(reel)
        except IOError:
            try:
                self.sftp.stat(reel)
            except IOError:
                raise
            raise ftplib.error_perm("550 existe déjà")

    def mlsd(self, chemin):
        import stat as st
        for a in self.sftp.listdir_attr(self._reel(chemin)):
            yield a.filename, {"type": "dir" if st.S_ISDIR(a.st_mode) else "file"}

    def delete(self, chemin):
        self.sftp.remove(self._reel(chemin))

    def quit(self):
        self.close()

    def close(self):
        try:
            self.sftp.close()
        finally:
            self.client.close()


def connecter(c, jr):
    adresse = "%s:%s" % (c["hote"], c["port"])
    if c["protocole"] == "sftp":
        ftp = SFTPCommeFTP(c, jr)
        jr.info("connecté à %s en SFTP (chiffré)" % adresse)
        return ftp
    if c["tls"]:
        # FTPS explicite : sans lui, identifiants comme contenus circulent en
        # clair sur le réseau.
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
def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Déploie le site du cours vers l'hébergement OVH (SFTP, FTPS ou FTP).")
    ap.add_argument("--essai", action="store_true",
                    help="simulation : affiche ce qui serait envoyé, n'envoie rien")
    ap.add_argument("--tout", action="store_true",
                    help="ignore le carnet et réenvoie tous les fichiers")
    ap.add_argument("--purge", action="store_true",
                    help="supprime en ligne les fichiers absents du dépôt (demande confirmation)")
    ap.add_argument("--purge-confirme", action="store_true", dest="purge_confirme",
                    help="purge sans poser de question — pour un lancement non interactif")
    ap.add_argument("--adopter", action="store_true",
                    help="reprend un dossier distant publié par un autre outil (jamais avec --purge)")
    args = ap.parse_args(argv)
    if args.purge_confirme:
        args.purge = True
    if args.adopter and args.purge:
        sys.exit("--adopter et --purge ne se combinent pas : adoptez d'abord le dossier, "
                 "vérifiez le site, puis purgez lors d'un envoi suivant.")

    jr = Journal(args.essai)
    c = charger_config()
    base = c["repertoire_distant"]

    jr.titre("Destination")
    jr.info("cours « %s » → %s" % (c["cours"], base))
    if c["repertoire_distant_ignore"]:
        jr.info("config.json désigne aussi un répertoire distant : il est ignoré, "
                "la destination vient de destination.json.")
    if c["zones"]:
        jr.info("zones protégées : %s" % ", ".join(c["zones"]))

    jr.titre("Inventaire")
    tous = fichiers_suivis()
    retenus = [f for f in tous
               if not exclu(f, c["exclure"]) and not protege(f, c["proteger"])]
    jr.info("%d fichiers de site/ suivis par Git, %d retenus après exclusions"
            % (len(tous), len(retenus)))

    # --- on se connecte AVANT de comparer, y compris en simulation et avec --tout :
    #     le garde-fou et le carnet de référence sont sur le serveur. Sans
    #     connexion, une simulation retombe sur le carnet local, en le disant.
    jr.titre("Connexion")
    ftp = None
    try:
        ftp = connecter(c, jr)
    except ftplib.all_errors as e:
        if not args.essai:
            jr.alerte("connexion impossible : %s%s" % (e, diagnostic(e)))
            return CONNEXION
        jr.alerte("connexion impossible (%s).%s" % (e, diagnostic(e)))
        jr.info("simulation poursuivie d'après le carnet local, qui peut être en retard ;")
        jr.info("le garde-fou d'identité n'a PAS pu être vérifié.")

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

    carnet = None
    if ftp:
        jr.titre("Garde-fou")
        autorise, message, carnet = garde_identite(ftp, c, args.adopter)
        if not autorise:
            jr.alerte("envoi refusé : " + message)
            jr.info("rien n'a été envoyé ni supprimé.")
            raccrocher()
            return REFUS
        jr.info(message)

    if args.tout:
        manifeste = {}
        jr.info("option --tout : le carnet est ignoré, tout sera renvoyé.")
    elif carnet is not None:
        manifeste = carnet
        jr.info("carnet lu sur le serveur : %d fichiers déjà en ligne." % len(manifeste))
    else:
        manifeste = lire_manifeste(c["cours"]) if not ftp else {}
        jr.info("aucun carnet sur le serveur%s (%d entrées)."
                % (" : lecture du carnet local" if not ftp else "", len(manifeste)))

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
    jr.info("%d inchangés, %d à envoyer (%s)" % (inchanges, len(a_envoyer), humain(poids)))

    # --- les zones protégées ne partent jamais sans leur protection en ligne :
    #     leurs fichiers restent ici, le reste du site part. Le carnet ne les
    #     note pas, le déploiement suivant les enverra une fois la zone protégée.
    a_envoyer, retenus_zones, manquantes = retenir_zones(a_envoyer, c["zones"], ftp, base)
    for rel, _a, _t in retenus_zones:
        courant.pop(rel, None)
        if rel in manifeste:
            courant[rel] = manifeste[rel]
    if manquantes:
        poids = sum(t for _r, _a, t in a_envoyer)
        jr.alerte("protection absente en ligne (%s) : %d fichier(s) de zone protégée ne partent "
                  "pas. Lancez d'abord : python3 deploiement/proteger_zones.py"
                  % (", ".join(manquantes), len(retenus_zones)))

    if not a_envoyer and not args.purge:
        jr.info("le site en ligne est déjà à jour.")
        raccrocher()
        return OK

    if args.essai:
        jr.titre("Simulation")
        for rel, _a, taille in a_envoyer[:40]:
            jr.action("%s  (%s)" % (rel, humain(taille)))
        if len(a_envoyer) > 40:
            jr.info("… et %d autres fichiers" % (len(a_envoyer) - 40))
        jr.info("destination : %s%s" % (c["hote"], base))
        jr.info("rien n'a été envoyé.")
        raccrocher()
        return OK

    connus = set()
    envoyes, echecs, cumul = 0, [], 0
    depart = time.time()

    try:
        assurer_repertoire(ftp, base, connus)
        # Le carnet part AVANT le premier fichier : le dossier porte le nom du
        # cours dès sa création, et un premier envoi interrompu ne laisse pas un
        # dossier anonyme que le garde-fou refuserait ensuite à son propre cours.
        ecrire_manifeste_distant(ftp, manifeste, c, jr)
        jr.titre("Envoi")
        for i, (rel, absolu, taille) in enumerate(a_envoyer, 1):
            cible = base + "/" + rel
            assurer_repertoire(ftp, cible.rsplit("/", 1)[0], connus)
            jr.info("[%d/%d] %s  (%s)" % (i, len(a_envoyer), rel, humain(taille)))
            try:
                envoyer(ftp, absolu, cible, taille, jr)
                envoyes += 1
                cumul += taille
                # Carnet tenu au fil de l'eau : une coupure au milieu de 300 Mo
                # ne doit pas obliger à tout réenvoyer. Le local est gratuit, on
                # l'écrit à chaque fichier ; le distant coûte un aller-retour, on
                # le publie tous les 25 fichiers et à la fin.
                partiel = dict(manifeste)
                partiel.update({r: courant[r] for r, _a, _t in a_envoyer[:i]})
                ecrire_manifeste(partiel, c)
                if i % 25 == 0:
                    ecrire_manifeste_distant(ftp, partiel, c, jr)
            except ftplib.all_errors as e:
                echecs.append((rel, str(e)))
                jr.alerte("échec sur %s : %s" % (rel, e))

        # ---- purge éventuelle
        if args.purge:
            jr.titre("Fichiers obsolètes en ligne")
            distants = lister_distant(ftp, base, jr)
            locaux = set(retenus)
            gardes = sorted(d for d in distants if d and protege(d, c["proteger"]))
            # le carnet n'est pas un fichier du site : il ne doit jamais être purgé
            obsoletes = sorted(d for d in distants
                               if d and d not in locaux and d != MANIFESTE_DISTANT
                               and d not in gardes)
            for g in gardes:
                jr.info("conservé (protégé) : %s" % g)
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
            ecrire_manifeste_distant(ftp, courant, c, jr)
    finally:
        raccrocher()

    if not echecs:
        ecrire_manifeste(courant, c)

    jr.titre("Bilan")
    jr.info("%d fichiers envoyés, %s en %s" % (envoyes, humain(cumul), duree(time.time() - depart)))
    if echecs:
        jr.alerte("%d échec(s) — ces fichiers seront repris au prochain lancement :" % len(echecs))
        for rel, e in echecs[:10]:
            jr.info("%s : %s" % (rel, e))
        return ECHECS
    jr.info("site à jour sur %s%s" % (c["hote"], base))
    if c["url"]:
        jr.info("à vérifier : %s" % c["url"])
    return OK


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n  interrompu. Les fichiers déjà envoyés sont notés : "
              "relancez pour reprendre où vous en étiez.")
        sys.exit(130)
