#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Teste hors ligne le garde-fou d'identité et les protections du déployeur.

    python3 deploiement/tester_deployer.py

Aucune connexion, aucun envoi : un faux serveur, tenu en mémoire, remplace
l'hébergement, et des fichiers temporaires remplacent config.json et
destination.json — les vrais ne sont jamais ouverts. Chaque cas rejoue une
situation réelle : un cours neuf, un cours déjà publié, le dossier d'un autre
cours, un dossier publié par un ancien déployeur, un dossier logé dans un
autre cours, une zone protégée sans sa protection.

Code de sortie 1 au premier écart : à lancer après toute modification de
deployer.py.
"""
import contextlib
import ftplib
import io
import json
import os
import shutil
import sys
import tempfile

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import deployer as D  # noqa: E402

for flux in (sys.stdout, sys.stderr):
    try:
        flux.reconfigure(encoding="utf-8")
    except Exception:
        pass


class FauxServeur(object):
    """Les opérations FTP dont le déployeur se sert, sur un dictionnaire {chemin: octets}."""

    def __init__(self, fichiers=None, dossiers=None):
        self.fichiers = dict(fichiers or {})
        self.dossiers = set(dossiers or [])
        for chemin in self.fichiers:
            self._parents(chemin)

    def _parents(self, chemin):
        parties = chemin.strip("/").split("/")[:-1]
        for i in range(1, len(parties) + 1):
            self.dossiers.add("/" + "/".join(parties[:i]))

    @staticmethod
    def _chemin(commande):
        return commande.split(" ", 1)[1]

    def retrbinary(self, commande, rappel):
        chemin = self._chemin(commande)
        if chemin not in self.fichiers:
            raise ftplib.error_perm("550 fichier absent")
        rappel(self.fichiers[chemin])

    def storbinary(self, commande, fichier, blocksize=8192, callback=None):
        chemin = self._chemin(commande)
        if os.path.dirname(chemin) not in self.dossiers:
            raise ftplib.error_perm("553 dossier absent")
        self.fichiers[chemin] = fichier.read()

    def mkd(self, chemin):
        if chemin in self.dossiers:
            raise ftplib.error_perm("550 existe déjà")
        self.dossiers.add(chemin)

    def mlsd(self, chemin):
        chemin = chemin.rstrip("/")
        if chemin not in self.dossiers:
            raise ftplib.error_perm("550 dossier absent")
        noms = {}
        for f in self.fichiers:
            if f.startswith(chemin + "/"):
                reste = f[len(chemin) + 1:]
                noms[reste.split("/")[0]] = "dir" if "/" in reste else "file"
        for d in self.dossiers:
            if d.startswith(chemin + "/") and "/" not in d[len(chemin) + 1:]:
                noms.setdefault(d[len(chemin) + 1:], "dir")
        return [(n, {"type": t}) for n, t in sorted(noms.items())]

    def nlst(self, chemin):
        return [n for n, _f in self.mlsd(chemin)]

    def delete(self, chemin):
        del self.fichiers[chemin]

    def quit(self):
        pass

    close = quit


def carnet(cours=None, fichiers=None):
    donnees = {"fichiers": fichiers or {}}
    if cours:
        donnees["cours"] = cours
    return json.dumps(donnees).encode("utf-8")


BASE = "/www/teaching/demo/nouveau-cours"
CARNET = BASE + "/" + D.MANIFESTE_DISTANT
PROTEGE = ".htaccess"


class Banc(object):
    """Un dépôt temporaire : site/, config.json et destination.json factices."""

    def __init__(self, zones=(), fichiers_site=None):
        self.dossier = tempfile.mkdtemp(prefix="tester-deployer-")
        self.site = os.path.join(self.dossier, "site")
        os.makedirs(os.path.join(self.site, "chapitres"))
        self.fichiers_site = fichiers_site or {
            "index.html": "<h1>Accueil</h1>",
            "chapitres/01-intro.html": "<h1>Chapitre 1</h1>",
            "correction/index.html": "<h1>Correction</h1>",
            "correction/formateur/index.html": "<h1>Formateur</h1>",
        }
        for rel, texte in self.fichiers_site.items():
            chemin = os.path.join(self.site, rel.replace("/", os.sep))
            os.makedirs(os.path.dirname(chemin), exist_ok=True)
            with open(chemin, "w", encoding="utf-8") as f:
                f.write(texte)
        self.config = os.path.join(self.dossier, "config.json")
        with open(self.config, "w", encoding="utf-8") as f:
            json.dump({"hote": "serveur.test", "identifiant": "essai", "motdepasse": "essai",
                       "protocole": "sftp", "repertoire_distant": "/www/cours-precedent"}, f)
        self.destination = os.path.join(self.dossier, "destination.json")
        with open(self.destination, "w", encoding="utf-8") as f:
            json.dump({"cours": "nouveau-cours", "repertoire_distant": BASE,
                       "zones_protegees": list(zones)}, f)
        self.manifeste = os.path.join(self.dossier, "manifeste.json")

    @contextlib.contextmanager
    def actif(self, serveur):
        """Branche le déployeur sur ce banc et ce faux serveur, puis rétablit tout."""
        sauve = (D.RACINE, D.CONFIG, D.DESTINATION, D.MANIFESTE, D.connecter, D.fichiers_suivis)
        D.RACINE, D.CONFIG, D.DESTINATION, D.MANIFESTE = (self.site, self.config,
                                                          self.destination, self.manifeste)
        D.connecter = lambda c, jr: serveur
        D.fichiers_suivis = lambda: sorted(self.fichiers_site)
        try:
            yield
        finally:
            (D.RACINE, D.CONFIG, D.DESTINATION, D.MANIFESTE, D.connecter, D.fichiers_suivis) = sauve

    def nettoyer(self):
        shutil.rmtree(self.dossier, ignore_errors=True)


def lancer(banc, serveur, *options):
    """Le code de sortie de main(), sa sortie écrite étant gardée pour le diagnostic."""
    tampon = io.StringIO()
    with banc.actif(serveur), contextlib.redirect_stdout(tampon):
        try:
            code = D.main(list(options))
        except SystemExit as e:
            code = e.code
    return code, tampon.getvalue()


ECARTS = []


def verifier(nom, condition, detail=""):
    print("  %s %s" % ("✓" if condition else "✗", nom))
    if not condition:
        ECARTS.append(nom)
        if detail:
            print("      " + detail.strip().replace("\n", "\n      "))


def cas_garde():
    print("\nGarde-fou d'identité")
    banc = Banc()
    try:
        s = FauxServeur()
        code, sortie = lancer(banc, s)
        verifier("dossier absent : premier envoi accepté, carnet au nom du cours", code == D.OK
                 and json.loads(s.fichiers[CARNET])["cours"] == "nouveau-cours"
                 and BASE + "/index.html" in s.fichiers, sortie)
        verifier("le répertoire de config.json est ignoré (rien dans /www/cours-precedent)",
                 not any(f.startswith("/www/cours-precedent") for f in s.fichiers)
                 and "il est ignoré" in sortie, sortie)

        code, sortie = lancer(banc, s)
        verifier("deuxième envoi : dossier reconnu, rien à envoyer", code == D.OK
                 and "appartient à ce cours" in sortie and "déjà à jour" in sortie, sortie)

        s = FauxServeur({CARNET: carnet("autre-cours"), BASE + "/index.html": b"autre"})
        code, sortie = lancer(banc, s)
        verifier("dossier d'un autre cours : refusé, rien écrit", code == D.REFUS
                 and s.fichiers[BASE + "/index.html"] == b"autre", sortie)
        code, sortie = lancer(banc, s, "--adopter")
        verifier("dossier d'un autre cours : refusé même avec --adopter", code == D.REFUS, sortie)

        s = FauxServeur({CARNET: carnet(None, {"index.html": {"sha": "x", "taille": 1}}),
                         BASE + "/index.html": b"ancien"})
        code, sortie = lancer(banc, s)
        verifier("carnet sans identifiant (ancien déployeur) : refusé", code == D.REFUS
                 and "--adopter" in sortie, sortie)
        code, sortie = lancer(banc, s, "--adopter")
        verifier("… repris avec --adopter, le carnet porte désormais ce cours", code == D.OK
                 and json.loads(s.fichiers[CARNET])["cours"] == "nouveau-cours", sortie)

        s = FauxServeur({CARNET: b"{ pas du json"})
        code, sortie = lancer(banc, s)
        verifier("carnet illisible : refusé", code == D.REFUS, sortie)

        s = FauxServeur({BASE + "/page.html": b"inconnu"})
        code, sortie = lancer(banc, s)
        verifier("dossier occupé sans carnet : refusé", code == D.REFUS and "page.html" in sortie, sortie)

        s = FauxServeur({BASE + "/" + PROTEGE: b"Require valid-user", BASE + "/.ovhconfig": b"x"})
        code, sortie = lancer(banc, s)
        verifier("dossier qui ne contient que des protections : accepté comme vide", code == D.OK
                 and s.fichiers[BASE + "/" + PROTEGE] == b"Require valid-user", sortie)

        s = FauxServeur({"/www/teaching/demo/" + D.MANIFESTE_DISTANT: carnet("cours-parent")})
        code, sortie = lancer(banc, s)
        verifier("dossier logé dans un cours publié : refusé", code == D.REFUS
                 and "cours-parent" in sortie, sortie)
        code, sortie = lancer(banc, s, "--adopter")
        verifier("… refusé même avec --adopter", code == D.REFUS, sortie)

        code, sortie = lancer(banc, FauxServeur(), "--adopter", "--purge")
        verifier("--adopter et --purge ensemble : refusés avant toute connexion",
                 code not in (D.OK, None) and "ne se combinent pas" in str(sortie) + str(code), sortie)

        s = FauxServeur({CARNET: carnet("autre-cours")})
        code, sortie = lancer(banc, s, "--essai")
        verifier("la simulation signale le refus (code 3)", code == D.REFUS, sortie)
    finally:
        banc.nettoyer()


def cas_protections():
    print("\nProtections du serveur")
    banc = Banc(fichiers_site={"index.html": "<h1>Accueil</h1>", ".htaccess": "local",
                               "aide/.user.ini": "local"})
    try:
        s = FauxServeur({CARNET: carnet("nouveau-cours"), BASE + "/.htaccess": b"serveur",
                         BASE + "/aide/.user.ini": b"serveur", BASE + "/vieux.html": b"obsolete"})
        code, sortie = lancer(banc, s, "--purge-confirme")
        verifier("un .htaccess local ne remplace jamais celui du serveur",
                 s.fichiers[BASE + "/.htaccess"] == b"serveur", sortie)
        verifier("la purge garde les protections et supprime le reste",
                 BASE + "/aide/.user.ini" in s.fichiers and BASE + "/vieux.html" not in s.fichiers
                 and CARNET in s.fichiers, sortie)
    finally:
        banc.nettoyer()


def cas_zones():
    print("\nZones protégées")
    banc = Banc(zones=["correction/", "correction/formateur/"])
    try:
        s = FauxServeur()
        code, sortie = lancer(banc, s)
        envoyes = [f for f in s.fichiers if f.startswith(BASE + "/correction/")]
        verifier("sans protection en ligne, la zone reste au dépôt, le reste part",
                 code == D.OK and not envoyes and BASE + "/index.html" in s.fichiers, sortie)
        notes = json.loads(s.fichiers[CARNET])["fichiers"]
        verifier("le carnet ne note pas la zone retenue", not any(r.startswith("correction/")
                                                                 for r in notes), sortie)

        s.fichiers[BASE + "/correction/.htaccess"] = b"AuthUserFile x\nRequire valid-user"
        code, sortie = lancer(banc, s)
        verifier("zone formateur encore ouverte : son contenu reste retenu",
                 BASE + "/correction/formateur/index.html" not in s.fichiers
                 and BASE + "/correction/index.html" in s.fichiers, sortie)

        s.fichiers[BASE + "/correction/formateur/.htaccess"] = b"AuthUserFile y\nRequire valid-user"
        code, sortie = lancer(banc, s)
        verifier("les deux zones protégées : tout part", code == D.OK
                 and BASE + "/correction/formateur/index.html" in s.fichiers, sortie)
    finally:
        banc.nettoyer()


def cas_destination():
    print("\nDestination")
    banc = Banc()
    try:
        for valeur, attendu in (("/www", "racine"), ("/", "racine"), ("/www/chemin/du-cours", "modèle"),
                                ("/www/a/../b", "..")):
            with open(banc.destination, "w", encoding="utf-8") as f:
                json.dump({"cours": "nouveau-cours", "repertoire_distant": valeur}, f)
            code, sortie = lancer(banc, FauxServeur())
            verifier("répertoire « %s » refusé" % valeur, code not in (D.OK, None)
                     and attendu in str(code), str(code))
        with open(banc.destination, "w", encoding="utf-8") as f:
            json.dump({"cours": "Mon Cours", "repertoire_distant": BASE}, f)
        code, _ = lancer(banc, FauxServeur())
        verifier("identifiant de cours invalide refusé", "minuscules" in str(code), str(code))
        os.remove(banc.destination)
        code, _ = lancer(banc, FauxServeur())
        verifier("sans destination.json : refus", "destination.json" in str(code), str(code))
    finally:
        banc.nettoyer()


def main():
    cas_garde()
    cas_protections()
    cas_zones()
    cas_destination()
    print()
    if ECARTS:
        print("%d écart(s) : %s" % (len(ECARTS), " ; ".join(ECARTS)))
        return 1
    print("Tous les cas sont conformes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
