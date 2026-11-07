# -*- coding: utf-8 -*-
"""Les QR codes du livret : segno, correction d'erreur M, PNG nets pour l'impression.

Un QR code porte toujours une adresse absolue (sources.SITE pour le site du cours) ; aucune adresse ne s'imprime sous
lui. Le registre garde chaque QR code posé — son adresse, sa légende, sa place — pour le contrôle et le rapport :
chaque adresse doit répondre 200, et son ancre (#…) exister dans la page (glossaire : parmi les ancres que la page
calcule, g-…). Sans adresse publique du cours (sources.ADRESSE vide), la vérification en ligne n'a pas lieu ; les
ancres, elles, se vérifient toujours dans les fichiers du site.

UN SITE PROTÉGÉ (fiche du livret, « site_protege ») répond 401 à qui n'a pas d'identifiants, et la chaîne ne
s'authentifie jamais : une adresse du site se vérifie dans le dépôt — le fichier existe, part avec le site (suivi par
Git), n'est ni la correction ni un dossier de travail, et son ancre existe dans la page. Une page que
destination.json tient hors ligne (« exclure ») est signalée, sans bloquer : en ligne, sa version précédente demeure.
Une adresse hors du site doit répondre 200 en ligne ; un site qui refuse les robots (403…) est ouvert par Chrome sans
interface, comme un étudiant l'ouvrirait.

Taille : environ 2,2 cm dans la marge ; le PNG compte environ 600 points par pouce à cette taille, un module entier de
pixels par module du code (aucun flou à l'impression). Couleur : la plus foncée de la charte (gabarit.PRIMAIRE_FONCE)
sur blanc (contraste > 15).
"""
import concurrent.futures
import hashlib
import os
import re
import urllib.error
import urllib.request

import segno

from . import gabarit as G
from .sources import CACHE, SITE, exclu, publie

# Les réponses d'un site qui refuse les robots, et les titres d'une page d'erreur ou de refus.
REFUS_ROBOTS = (401, 403, 406, 429, 503)
PAGE_ERREUR = re.compile(r"access denied|forbidden|not found|page introuvable|erreur|error|attention required|"
                         r"just a moment|un instant|captcha|\b40\d\b|\b50\d\b", re.I)
# Ce qu'une adresse du site ne vise jamais : la correction protégée, les dossiers de travail (jamais en ligne).
JAMAIS = ("correction/", "QCM/correction/", "en/correction/", "en/QCM/correction/", "docs/", "outils/",
          "Polycopie/", "deploiement/")

FONCE = "#" + G.PRIMAIRE_FONCE
DPI = 600
ENTETES = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/130.0 Safari/537.36 (verification du polycopie)",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8"}


class Registre:
    def __init__(self, langue):
        self.langue = langue
        self.dossier = os.path.join(CACHE, "qr")
        os.makedirs(self.dossier, exist_ok=True)
        self.poses = []            # dict(url, etiquette, texte, place, png)
        self.statuts = {}
        self.avertissements = []   # ce qui se signale sans bloquer (une page tenue hors ligne, un site sans robots)
        self.a_venir = set()       # adresses des capsules sans piste, prévues (rendu.capsule_prevue)

    def fabriquer(self, url, taille_cm=2.2, bordure=0):
        """Le PNG du QR code d'une adresse (gardé en cache) ; rend son chemin."""
        if not re.match(r"https?://", url):
            raise ValueError(f"QR code sans adresse absolue : {url!r}")
        cle = hashlib.sha1(f"{url}|{taille_cm}|{bordure}|{FONCE}".encode("utf-8")).hexdigest()[:16]
        sortie = os.path.join(self.dossier, f"qr-{cle}.png")
        if not os.path.exists(sortie):
            code = segno.make(url, error="m", micro=False, boost_error=False)
            modules = code.symbol_size(border=bordure)[0]
            echelle = max(4, round(taille_cm / 2.54 * DPI / modules))
            code.save(sortie, kind="png", scale=echelle, border=bordure, dark=FONCE, light="#FFFFFF", dpi=DPI)
        return sortie

    def poser(self, url, etiquette, texte, place, taille_cm=2.2, bordure=0):
        png = self.fabriquer(url, taille_cm, bordure)
        self.poses.append(dict(url=url, etiquette=etiquette, texte=texte, place=place, png=png))
        return png

    # ── la vérification ────────────────────────────────────────────────────
    def verifier(self, en_ligne=True, protege=False):
        """Vérifie chaque adresse posée : la réponse du serveur (200) et l'ancre ; sur un site protégé, les adresses
        du site dans le dépôt (voir l'en-tête du module). Rend la liste des erreurs ; les signalements, qui ne
        bloquent pas, vont dans self.avertissements."""
        urls = sorted({p["url"] for p in self.poses})
        erreurs, self.avertissements = [], []
        # Les capsules à venir (rendu.capsule_prevue) : l'adresse prévue d'une piste pas encore enregistrée. Son
        # fichier n'existe pas encore, elle ne se vérifie donc pas ici ; elle se teste après l'enregistrement
        # (generer_polycopie.py --essai : « capsules à venir : 0 »). Le verifier ne tait qu'une adresse prévue,
        # jamais un autre fichier absent.
        for url in (u for u in urls if u in self.a_venir):
            self.statuts[url] = "capsule à venir : adresse prévue, à tester après l'enregistrement"
        urls = [u for u in urls if u not in self.a_venir]
        du_site = [u for u in urls if u.startswith(SITE)]
        externes = [u for u in urls if not u.startswith(SITE)]
        if protege:
            for url in du_site:
                rel = self.langue.rel_site(url)
                fichier = self.langue.locale(url)
                if any(rel.startswith(j) for j in JAMAIS):
                    erreurs.append(f"{url} : le livret ne mène jamais là ({rel.split('/')[0]}/)")
                elif not fichier or not os.path.isfile(fichier):
                    erreurs.append(f"{url} : fichier absent du dépôt")
                elif publie(rel) is False:
                    erreurs.append(f"{url} : fichier non suivi par Git, que le déployeur n'envoie pas")
                else:
                    x = exclu(rel)
                    if x:
                        self.avertissements.append(f"{url} : tenu hors ligne par destination.json (« {x} ») — en "
                                                   "ligne, sa version précédente demeure, s'il y en a une")
                    self.statuts[url] = "site protégé : vérifié dans le dépôt"
            a_tester = externes
        else:
            a_tester = urls
        if en_ligne and a_tester:
            refus = []
            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
                for url, statut in zip(a_tester, pool.map(statut_http, a_tester)):
                    if statut in REFUS_ROBOTS and not url.startswith(SITE):
                        refus.append((url, statut))
                    elif statut != 200:
                        erreurs.append(f"{url} : réponse {statut}")
                    self.statuts[url] = statut
            # Un site qui refuse les robots (403…) : la page s'ouvre-t-elle dans un navigateur ? Chrome sans
            # interface, une adresse après l'autre (un seul navigateur piloté à la fois).
            from . import navigateur
            for url, statut in refus:
                titre = navigateur.titre(url)
                if titre and not PAGE_ERREUR.search(titre):
                    self.statuts[url] = f"{statut} aux robots ; ouverte par Chrome sans interface : « {titre} »"
                    self.avertissements.append(f"{url} : {self.statuts[url]}")
                else:
                    erreurs.append(f"{url} : réponse {statut}, et Chrome sans interface "
                                   + (f"ouvre « {titre} »" if titre else "n'ouvre rien"))
        for url in urls:
            probleme = ancre_absente(url, self.langue)
            if probleme:
                erreurs.append(f"{url} : {probleme}")
        return erreurs


def statut_http(url, delai=25, essais=3):
    """Le code de réponse d'une adresse : une indisponibilité passagère (429, 5xx, réseau) est retentée deux fois,
    à quelques secondes d'intervalle ; seule la dernière réponse compte."""
    import time
    statut = None
    for k in range(essais):
        statut = _statut_http(url, delai)
        if statut == 200 or not (statut in (429, 500, 502, 503, 504) or str(statut).startswith("erreur")):
            return statut
        time.sleep(4 * (k + 1))
    return statut


def _statut_http(url, delai=25):
    """Le code de réponse d'une adresse (sans son ancre) : HEAD, puis GET si le serveur refuse HEAD (certains
    répondent 404 ou 403 à HEAD et 200 à GET)."""
    adresse = url.split("#", 1)[0]
    for methode in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(adresse, method=methode, headers=ENTETES)
            with urllib.request.urlopen(req, timeout=delai) as r:
                if methode == "HEAD" and r.status != 200:
                    continue
                return r.status
        except urllib.error.HTTPError as e:
            if methode == "HEAD" and e.code in (400, 403, 404, 405, 429, 501):
                continue
            return e.code
        except Exception as e:                                 # réseau, délai
            if methode == "HEAD":
                continue
            return f"erreur ({e.__class__.__name__})"
    return "?"


def ancre_absente(url, langue):
    """Rien si l'adresse n'a pas d'ancre ou si l'ancre existe ; sinon, ce qui ne va pas."""
    if not url.startswith(SITE):
        return None
    adresse, _, ancre = url.partition("#")
    fichier = langue.locale(adresse)
    if not fichier or not os.path.exists(fichier):
        return "page absente du site"
    if not ancre:
        return None
    if os.path.basename(fichier) == "glossaire.html":
        termes = {e["ancre"] for e in langue.glossaire()}
        return None if ancre in termes else f"ancre #{ancre} absente du glossaire"
    with open(fichier, encoding="utf-8") as f:
        texte = f.read()
    if re.search(r'\bid="%s"' % re.escape(ancre), texte):
        return None
    return f"ancre #{ancre} absente de la page"
