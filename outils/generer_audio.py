#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère les capsules audio manquantes avec l'API ElevenLabs, en Eleven v4.

    python3 outils/generer_audio.py --essai                    # ce qui serait généré, sans dépenser
    python3 outils/generer_audio.py --temoin --limite 1        # UN témoin, à écouter avant toute série
    python3 outils/generer_audio.py --fichier chapitre-2-capsule-fr.mp3 --temoin
    python3 outils/generer_audio.py --chapitre 6               # un chapitre à la fois
    python3 outils/generer_audio.py                            # tout ce qui manque (après le témoin)

EN ELEVEN V4, TOUJOURS. C'est le modèle de toutes les pistes : il interprète les
balises de jeu entre crochets ([measured], [warm, encouraging]…). Une
configuration restée sur un autre modèle est corrigée à la volée ; --modele
permet encore d'en essayer un autre, sur un témoin. Chaque balise reçoit l'accent
retenu par l'auteur (ACCENTS : « strong Parisian French accent » pour une piste
française), ajouté au moment de la synthèse : il n'est pas écrit dans les
scripts. Le ton et l'écriture des scripts sont décrits dans
prompts/14_capsules_audio.md.

UN TÉMOIN D'ABORD. Une série se paie d'avance et s'écoute après : une voix mal
réglée gâche toutes les pistes à la fois. --temoin produit une prise à côté, dans
outils/quarantaine/temoins/<modèle>/, sans rien déposer ni remplacer. Tant
qu'aucun témoin n'existe pour le modèle, une série de plusieurs pistes est
refusée (--serie pour passer outre, en connaissance de cause).

Les scripts ne sont pas écrits ici : ils viennent des fiches de production de
`docs/prompts/`, qui restent la source unique. Le nom du fichier attendu par la
page sert de clé : ce que la page réclame est ce qui est généré, et rien d'autre.

CHAQUE PRISE EST CONTRÔLÉE AVANT D'ÊTRE DÉPOSÉE. Une capsule est un jour partie
en ligne à 67 mots par minute au lieu de 145 — le même texte étiré sur le double
du temps, faute d'un réglage. Personne ne l'avait entendue. Le script mesure
donc durée, débit et silences ; ce qui sort des clous va en quarantaine avec la
raison, jamais dans le site.

Rien n'est jamais écrasé sans --force, et la clé n'est jamais affichée.
"""

import argparse
import glob
import io
import json
import os
import re
import ssl
import subprocess
import sys
import urllib.error
import urllib.request

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Le site vit dans site/, pas a la racine : celle-ci porte aussi les outils,
# les fiches de production et la documentation, qui ne sont pas publies.
SITE = os.path.join(RACINE, "site")
CONFIG = os.path.join(RACINE, "outils", "elevenlabs.json")
MODELE = os.path.join(RACINE, "outils", "elevenlabs.exemple.json")
QUARANTAINE = os.path.join(RACINE, "outils", "quarantaine")
BASE = "https://api.elevenlabs.io/v1"
GABARITS = {"a-remplir", "sk_a-remplir", ""}
MODELE_V4 = "eleven_v4"

# Seuils de référence, calibrés sur la voix clonée de l'auteur (prises validées
# des cours précédents, octobre 2026).
#
# DÉBIT — le plancher de 115 venait d'une voix plus rapide ; celle-ci, plus
# posée, a donné des prises correctes à 112. Un faux positif finit par pousser à
# désactiver le contrôle, ce qui est bien pire : plancher à 105, assez bas pour
# cette voix, assez haut pour rattraper l'incident qui a motivé ces contrôles
# (une prise à 67 mots par minute). En Eleven v4, la voix parle plus vite (165 à
# 185 mots par minute mesurés) : le plafond monte alors à 190.
#
# SILENCE — 3,6 s. Sur une capsule de deux minutes, une respiration marquée fait
# couramment 3,1 à 3,4 s : une intention de mise en voix, pas un défaut. Au-delà,
# l'auditeur croit que la lecture s'est arrêtée.
#
# DURÉE — en Eleven v4, la fenêtre de chaque piste se déduit de ses mots, entre
# le débit plafond et le débit plancher. Les bornes ci-dessous ne servent qu'aux
# autres modèles, ou à une fiche qui déclare sa propre tolérance.
#
# Ils vivent ICI, dans le code, et non dans la configuration. Une première
# version les avait placés dans elevenlabs.json : une configuration copiée avant
# un recalibrage gardait les anciennes valeurs, et rejetait de bonnes prises sans
# que personne ne comprenne pourquoi. La configuration peut toujours les
# surcharger, mais elle doit alors le faire sciemment — le script le signale.
SEUILS = {
    "mots_par_minute_min": 105,
    "mots_par_minute_max": 175,
    "duree_min_s": 55,
    "duree_max_s": 145,
    "silence_max_s": 3.6,
}
PLAFOND_V4 = 190

# L'accent, en Eleven v4, par langue de piste. L'auteur a retenu, à l'écoute de
# deux témoins, la prise où chaque balise de jeu porte la formulation marquée :
# « natural Parisian French accent » ne s'entendait pas assez. La documentation
# d'Eleven v4 range les balises d'accent parmi les balises expérimentales : à
# réécouter si la voix ou le modèle changent.
#
# Une piste anglaise (fichier en -en.mp3) ne reçoit pas d'accent ajouté : un
# clone français qui lit l'anglais a déjà le sien, et lui en demander un
# « parisien marqué » en ferait une caricature. Le témoin tranche ; la
# configuration peut surcharger ces valeurs (clé « accent »), et le script le
# signale.
ACCENT_V4 = "strong Parisian French accent"
ACCENTS = {"fr": ACCENT_V4, "en": ""}

for flux in (sys.stdout, sys.stderr):
    try:
        flux.reconfigure(encoding="utf-8")
    except Exception:
        pass


def avec_accent(script, accent):
    """« [measured] » devient « [measured, strong Parisian French accent] », pour chaque balise
    du script ; une balise qui parle déjà d'accent reste telle quelle. Sans accent, rien ne change."""
    if not accent:
        return script
    return re.sub(r"\[([^\]]+)\]",
                  lambda m: m.group(0) if "accent" in m.group(1).lower()
                  else "[%s, %s]" % (m.group(1), accent),
                  script)


def langue_piste(nom):
    """« fr » ou « en », d'après le suffixe du fichier — chapitre-1-capsule-en.mp3 pour une capsule,
    chapitre-1-podcast.en.mp3 pour un podcast ; une piste sans suffixe est française."""
    m = re.search(r"[-.](fr|en)\.mp3$", nom)
    return m.group(1) if m else "fr"


# ---------------------------------------------------------------- réseau
def contexte_ssl():
    """Python sur macOS n'utilise pas le trousseau du système : certifi le supplée."""
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return ssl.create_default_context()


CTX = contexte_ssl()


def aide_certificat(e):
    if "CERTIFICATE_VERIFY_FAILED" not in str(e):
        return ""
    return ("\n      Python n'a pas de magasin de certificats utilisable. Installez-le :"
            "\n          python3 -m pip install --upgrade certifi")


def synthese(cfg, texte, voix):
    """Renvoie les octets MP3, ou lève une exception explicite."""
    url = "%s/text-to-speech/%s?output_format=%s" % (
        BASE, voix, cfg.get("format_sortie", "mp3_44100_128"))
    r = cfg.get("reglages", {})
    modele = cfg.get("modele", MODELE_V4)
    corps = {
        "text": texte,
        "model_id": modele,
        "voice_settings": {
            "stability": r.get("stabilite", 0.5),
            "similarity_boost": r.get("similarite", 0.8),
        },
    }
    # Eleven v4 n'a ni « style » ni « renfort du locuteur » (GET /v1/models) : on
    # ne les envoie pas. Les autres modèles les gardent.
    if not modele.startswith("eleven_v4"):
        corps["voice_settings"]["style"] = r.get("style", 0.1)
        corps["voice_settings"]["use_speaker_boost"] = bool(r.get("renfort_locuteur", True))
    if r.get("vitesse") not in (None, 1.0):
        corps["voice_settings"]["speed"] = r["vitesse"]
    req = urllib.request.Request(
        url, data=json.dumps(corps).encode("utf-8"),
        headers={"xi-api-key": cfg["cle_api"], "Content-Type": "application/json",
                 "Accept": "audio/mpeg", "User-Agent": "cours-template/1.0"})
    with urllib.request.urlopen(req, timeout=180, context=CTX) as rep:
        return rep.read()


# ---------------------------------------------------------------- mesures
def duree_ffprobe(chemin):
    try:
        brut = subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", chemin], stderr=subprocess.STDOUT)
        return float(brut.decode().strip())
    except Exception:
        return None


def duree_entete(chemin):
    """Durée estimée d'après l'en-tête de la première trame MP3.

    Sert de secours quand ffprobe est absent : nos fichiers sont en débit
    constant, la taille divisée par le débit donne une valeur suffisante pour
    juger qu'une prise dure une minute ou trois.
    """
    DEBITS = [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 0]
    ECH = {0: 44100, 1: 48000, 2: 32000}
    with open(chemin, "rb") as f:
        donnees = f.read(200000)
    taille = os.path.getsize(chemin)
    debut = 0
    if donnees[:3] == b"ID3":
        t = donnees[6:10]
        debut = 10 + ((t[0] & 0x7F) << 21 | (t[1] & 0x7F) << 14 | (t[2] & 0x7F) << 7 | (t[3] & 0x7F))
    for i in range(debut, min(len(donnees) - 4, debut + 8192)):
        if donnees[i] == 0xFF and (donnees[i + 1] & 0xE0) == 0xE0:
            debit = DEBITS[(donnees[i + 2] >> 4) & 0x0F]
            ech = ECH.get((donnees[i + 2] >> 2) & 0x03)
            if debit and ech:
                return (taille - debut) * 8.0 / (debit * 1000)
    return None


def silences(chemin, seuil_s):
    """Durées des silences dépassant le seuil. None si ffmpeg est absent.

    On renvoie les durées, pas seulement leur nombre : savoir qu'un silence
    fait 2,3 s ou 6 s change ce qu'on décide d'en faire.
    """
    try:
        p = subprocess.run(
            ["ffmpeg", "-hide_banner", "-nostats", "-i", chemin,
             "-af", "silencedetect=noise=-35dB:d=%s" % seuil_s, "-f", "null", "-"],
            capture_output=True, timeout=120)
        sortie = (p.stderr or b"").decode("utf-8", "replace")
        return [float(x) for x in re.findall(r"silence_duration: ([\d.]+)", sortie)]
    except Exception:
        return None


def controler(chemin, mots, seuils):
    """(griefs, durée, débit) — griefs vide si la prise est conforme."""
    griefs = []
    d = duree_ffprobe(chemin) or duree_entete(chemin)
    if d is None:
        return ["durée non mesurable (ni ffprobe ni en-tête exploitable)"], 0, 0
    if d < seuils["duree_min_s"]:
        griefs.append("trop courte : %d s" % d)
    if d > seuils["duree_max_s"]:
        griefs.append("trop longue : %d min %02d s" % (d // 60, d % 60))
    debit = mots / d * 60 if d else 0
    if debit < seuils["mots_par_minute_min"]:
        griefs.append("débit trop lent : %d mots/min" % debit)
    elif debit > seuils["mots_par_minute_max"]:
        griefs.append("débit trop rapide : %d mots/min — reprenez une fois ; si elle le reste, "
                      "ajoutez « speaking slowly » à chaque balise du script" % debit)
    trous = silences(chemin, seuils["silence_max_s"])
    if trous:
        griefs.append("silence de %s s" % " et ".join("%.1f" % x for x in trous))
    return griefs, d, debit


# ---------------------------------------------------------------- inventaire
def etiquette(n):
    """« ch3 » pour un chapitre, « page » pour une page hors chapitre."""
    return "ch%d" % n if n else "page"


def pages_a_scruter():
    """Les chapitres, puis les pages racine et du QCM qui portent des capsules.

    Une page qui n'est pas un chapitre peut porter une capsule (l'accueil, une
    soutenance, le QCM) : limiter la recherche à chapitres/0*.html rendait ses
    pistes invisibles au générateur.
    """
    pages = [(int(os.path.basename(p)[:2]), p)
             for p in sorted(glob.glob(os.path.join(SITE, "chapitres", "[0-9][0-9]-*.html")))]
    for p in (sorted(glob.glob(os.path.join(SITE, "*.html")))
              + sorted(glob.glob(os.path.join(SITE, "QCM", "*.html")))):
        if "RDCX.voice(" in io.open(p, encoding="utf-8").read():
            pages.append((0, p))
    return pages


def pistes_attendues():
    """[(chapitre, conteneur, nom_fichier, titre)] dans l'ordre des pages, sans doublon.

    Le chapitre vaut 0 pour une page qui n'en est pas un — ce que --chapitre
    exclut naturellement, et qu'etiquette() sait afficher.
    """
    out = []
    for n, page in pages_a_scruter():
        t = io.open(page, encoding="utf-8").read()
        for m in re.finditer(r"RDCX\.voice\('([^']+)',\s*\{(.*?)\n\s*\}\);", t, re.S):
            cid, corps = m.group(1), m.group(2)
            src = re.search(r"src:\s*'([^']+)'", corps)
            ttl = re.search(r'titre:\s*(\x27|")(.*?)\1\s*,', corps, re.S)
            if not src:
                continue
            titre = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", ttl.group(2))).strip() if ttl else cid
            out.append((n, cid, src.group(1).split("/")[-1], titre.replace("**", "")))
        # capsules bilingues, dont la source vient de TEXTES et non d'un litteral
        out.extend(capsules_bilingues(page, n))
    # les podcasts ne sont declares dans aucune page : ils viennent des fiches
    out.extend(podcasts_des_fiches())
    # Une même capsule peut figurer sur deux pages : on ne la garde qu'une fois,
    # sinon elle serait générée — et facturée — deux fois.
    vus, uniques = set(), []
    for piste in out:
        if piste[2] not in vus:
            vus.add(piste[2])
            uniques.append(piste)
    return uniques


def capsules_bilingues(page, n):
    """Les capsules declarees par langue dans le bloc TEXTES d'une page.

    Sur une page bilingue, l'appel RDCX.voice est unique et sa source vient
    d'une variable : on la lit donc a la source, dans TEXTES, ou chaque langue
    declare son propre fichier.
    """
    t = io.open(page, encoding="utf-8").read()
    out = []
    for m in re.finditer(r'capsuleSrc: "([^"]+)"', t):
        chemin = m.group(1)
        # le titre de la meme langue, declare juste apres
        suite = t[m.end():m.end() + 400]
        ttl = re.search(r'capsuleTitre: "([^"]*)"', suite)
        titre = ttl.group(1) if ttl else os.path.basename(chemin)
        cid = "capsule-%d" % n
        out.append((n, cid, chemin.split("/")[-1], titre))
    return out


def blocs_des_fiches():
    """[(nom_fichier, bloc)] : chaque fiche de docs/prompts découpée par « Nom exact du fichier »."""
    out = []
    for fiche in sorted(glob.glob(os.path.join(RACINE, "docs", "prompts", "*.md"))):
        t = io.open(fiche, encoding="utf-8").read()
        for m in re.finditer(
                r"\*\*Nom exact du fichier :\*\*\s*`([^`]+)`(.*?)(?=\*\*Nom exact du fichier :\*\*|\Z)",
                t, re.S):
            out.append((m.group(1), m.group(2)))
    return out


def podcasts_des_fiches():
    """Les podcasts, qui ne sont declares dans aucune page.

    media.js les cherche par convention de nommage — il n'y a donc rien a lire
    dans le HTML. La fiche de production, elle, donne l'emplacement exact : on
    part de la.
    """
    out = []
    for nom, bloc in blocs_des_fiches():
        n = re.match(r"chapitre-(\d+)-podcast\.", nom)
        if not n or "media/podcasts" not in bloc:
            continue
        titre = re.search(r"^## (.+)$", bloc, re.M)
        out.append((int(n.group(1)), "podcast-%s" % n.group(1), nom,
                    titre.group(1).strip() if titre else nom))
    return out


def scripts_des_fiches():
    """{nom_fichier: script ElevenLabs} — les fiches sont la source unique."""
    d = {}
    for nom, bloc in blocs_des_fiches():
        sc = re.search(r"\*\*▶️ Script ElevenLabs\*\*\s*\n+```\n(.*?)\n```", bloc, re.S)
        if sc and nom.endswith(".mp3"):
            d[nom] = sc.group(1).strip()
    return d


def tolerances_des_fiches():
    """{nom_fichier: (duree_min_s, duree_max_s)} lue dans les fiches.

    Une fiche peut declarer sa propre fenetre, sous la forme
    « tolerance 3 min 15 → 4 min 15 » : elle s'applique alors, quel que soit le
    modele. Le debit et les silences, eux, restent controles a l'identique.
    """
    d = {}
    for nom, bloc in blocs_des_fiches():
        tol = re.search(r"tol[ée]rance\s*(\d+)\s*min\s*(\d+)\s*(?:→|->)\s*(\d+)\s*min\s*(\d+)", bloc)
        if tol and nom.endswith(".mp3"):
            a = int(tol.group(1)) * 60 + int(tol.group(2))
            b = int(tol.group(3)) * 60 + int(tol.group(4))
            d[nom] = (a, b)
    return d


def mots_parles(script):
    """Mots réellement prononcés : les balises entre crochets n'en sont pas."""
    return len(re.sub(r"\[[^\]]+\]", " ", script).split())


# ---------------------------------------------------------------- configuration
def charger():
    if not os.path.isfile(CONFIG):
        sys.exit("Configuration absente : %s\n"
                 "    cp %s %s" % (CONFIG, MODELE, CONFIG))
    with io.open(CONFIG, encoding="utf-8") as f:
        c = json.load(f)
    for cle in ("cle_api", "voix_id"):
        if str(c.get(cle, "")).strip() in GABARITS:
            sys.exit("Configuration : « %s » est resté sur la valeur du modèle." % cle)
    # Les seuils et l'accent de référence viennent du code ; la configuration ne
    # fait que les surcharger, clé par clé, et jamais en silence.
    seuils, ecarts = dict(SEUILS), []
    for cle, val in (c.get("controles") or {}).items():
        if cle in SEUILS and val != SEUILS[cle]:
            ecarts.append("%s : %s au lieu de %s" % (cle, val, SEUILS[cle]))
        seuils[cle] = val
    accents = dict(ACCENTS)
    surcharge = c.get("accent")
    if isinstance(surcharge, str):
        surcharge = {"fr": surcharge}
    for langue, val in (surcharge or {}).items():
        if val != ACCENTS.get(langue):
            ecarts.append("accent %s : « %s » au lieu de « %s »" % (langue, val, ACCENTS.get(langue, "")))
        accents[langue] = val
    if ecarts:
        print("\n  /!\\ Votre configuration modifie les réglages de référence :")
        for e in ecarts:
            print("      %s" % e)
        print("      Retirez les blocs « controles » et « accent » de outils/elevenlabs.json pour")
        print("      revenir aux valeurs de référence, calibrées et retenues à l'écoute.")
    c["controles"], c["accents"] = seuils, accents
    c.setdefault("dossier_sortie", "assets/media/voix")
    return c


def temoins_existants(modele):
    dossier = os.path.join(QUARANTAINE, "temoins", modele)
    return sorted(glob.glob(os.path.join(dossier, "**", "*.mp3"), recursive=True))


# ---------------------------------------------------------------- programme
def main():
    ap = argparse.ArgumentParser(description="Génère les capsules audio manquantes (Eleven v4).")
    ap.add_argument("--essai", action="store_true", help="liste et coût, sans appeler l'API")
    ap.add_argument("--chapitre", type=int, help="ne traiter qu'un chapitre")
    ap.add_argument("--fichier", help="ne traiter que ce fichier (nom exact du MP3)")
    ap.add_argument("--limite", type=int, help="s'arrêter après N pistes")
    ap.add_argument("--force", action="store_true", help="régénérer même si le fichier existe")
    ap.add_argument("--temoin", action="store_true",
                    help="produire une prise témoin dans outils/quarantaine/temoins/, sans rien déposer ni remplacer")
    ap.add_argument("--serie", action="store_true",
                    help="autoriser une série sans témoin préalable pour ce modèle")
    ap.add_argument("--modele", help="un autre modèle que eleven_v4, à essayer sur un témoin")
    ap.add_argument("--vitesse", type=float,
                    help="la vitesse de la voix (0,7 à 1,2) ; sans effet sur Eleven v4, qui l'ignore")
    ap.add_argument("--sans-accent", action="store_true", dest="sans_accent",
                    help="en Eleven v4, ne pas ajouter d'accent aux balises de jeu")
    ap.add_argument("--accent", help="en Eleven v4, une autre formulation de l'accent des pistes "
                                     "françaises, à essayer sur un témoin (défaut : « %s »)" % ACCENT_V4)
    args = ap.parse_args()

    cfg = charger()
    if args.modele:
        cfg["modele"] = args.modele
    elif not str(cfg.get("modele", "")).startswith("eleven_v4"):
        # Toutes les pistes en Eleven v4, avec l'accent retenu : une configuration
        # restée sur un autre modèle ne fait plus partir une prise sans accent.
        print("  (modèle de la configuration « %s » remplacé par %s)" % (cfg.get("modele"), MODELE_V4))
        cfg["modele"] = MODELE_V4
    if args.vitesse is not None:
        cfg.setdefault("reglages", {})["vitesse"] = args.vitesse
    v4 = cfg["modele"].startswith("eleven_v4")
    if v4:
        cfg["controles"]["mots_par_minute_max"] = max(cfg["controles"]["mots_par_minute_max"], PLAFOND_V4)
    if args.accent:
        cfg["accents"]["fr"] = args.accent

    sortie = os.path.join(SITE, cfg["dossier_sortie"])
    if args.temoin:
        # Un témoin s'écoute avant toute série : il ne remplace jamais une prise en ligne.
        sortie = os.path.join(QUARANTAINE, "temoins", cfg["modele"])
        args.force = True
    scripts = scripts_des_fiches()
    tolerances = tolerances_des_fiches()
    seuils_base = cfg["controles"]

    travail, sans_script = [], []
    for n, cid, nom, titre in pistes_attendues():
        if args.chapitre and n != args.chapitre:
            continue
        if args.fichier and nom != args.fichier:
            continue
        dossier = (os.path.join(SITE, "assets", "media", "podcasts")
                   if "-podcast." in nom and not args.temoin else sortie)
        if os.path.exists(os.path.join(dossier, nom)) and not args.force:
            continue
        sc = scripts.get(nom)
        if not sc:
            sans_script.append((n, nom))
            continue
        langue = langue_piste(nom)
        accent = "" if (args.sans_accent or not v4) else cfg["accents"].get(langue, "")
        voix = cfg.get("voix_id_en") if langue == "en" and cfg.get("voix_id_en") else cfg["voix_id"]
        # La fenêtre de durée : celle de la fiche si elle en déclare une ; en v4,
        # celle que donnent ses mots entre les débits plafond et plancher.
        m = mots_parles(sc)
        if nom in tolerances:
            fenetre = tolerances[nom]
        elif v4:
            fenetre = (int(m * 60 / seuils_base["mots_par_minute_max"]),
                       int(m * 60 / seuils_base["mots_par_minute_min"]) + 1)
        else:
            fenetre = (seuils_base["duree_min_s"], seuils_base["duree_max_s"])
        travail.append((n, nom, titre, avec_accent(sc, accent), m, accent, voix, fenetre, dossier))
    if args.limite:
        travail = travail[:args.limite]

    print("\nÀ générer\n---------")
    if sans_script:
        print("  /!\\ %d piste(s) sans script dans les fiches :" % len(sans_script))
        for n, nom in sans_script[:5]:
            print("      %-4s %s" % (etiquette(n), nom))
    if not travail:
        print("  rien à faire : toutes les pistes demandées sont déjà en place.")
        return 0

    total_car = sum(len(t[3]) for t in travail)
    for n, nom, _titre, sc, mots, accent, _v, _f, _d in travail:
        print("  %-4s %-46s %5d car.  %3d mots%s" % (etiquette(n), nom[:46], len(sc), mots,
                                                   "" if accent else "  (sans accent ajouté)"))
    print("\n  %d piste(s), %s caractères" % (len(travail), format(total_car, ",")))
    print("  modèle « %s », vitesse %s%s%s" % (
        cfg["modele"], cfg.get("reglages", {}).get("vitesse", 1.0),
        ", accent « %s » (pistes françaises)" % cfg["accents"].get("fr") if v4 and not args.sans_accent else "",
        " — témoin, rien n'est déposé" if args.temoin else ""))

    if len(travail) > 1 and not args.temoin and not args.serie and not temoins_existants(cfg["modele"]):
        print("\n  /!\\ Aucun témoin pour « %s » dans ce cours : écoutez-en un avant toute série."
              % cfg["modele"])
        print("      python3 outils/generer_audio.py --temoin --limite 1")
        print("      (puis relancez ; --serie passe outre, en connaissance de cause)")
        if not args.essai:
            return 2

    if args.essai:
        print("\n  Simulation : aucun appel, aucun crédit consommé.")
        return 0

    os.makedirs(QUARANTAINE, exist_ok=True)

    print("\nGénération\n----------")
    deposes, rejetes, echecs = [], [], []
    for i, (n, nom, titre, sc, mots, _accent, voix, fenetre, dossier) in enumerate(travail, 1):
        print("  [%d/%d] %s  %s" % (i, len(travail), etiquette(n), nom))
        try:
            audio = synthese(cfg, sc, voix)
        except urllib.error.HTTPError as e:
            detail = ""
            try:
                detail = e.read().decode("utf-8", "replace")[:300]
            except Exception:
                pass
            print("      ÉCHEC HTTP %s  %s" % (e.code, detail))
            echecs.append((nom, "HTTP %s %s" % (e.code, detail)))
            continue
        except urllib.error.URLError as e:
            print("      ÉCHEC réseau : %s%s" % (e.reason, aide_certificat(e)))
            echecs.append((nom, str(e.reason)))
            continue

        tmp = os.path.join(QUARANTAINE, nom)
        with open(tmp, "wb") as f:
            f.write(audio)

        seuils = dict(seuils_base)
        seuils["duree_min_s"], seuils["duree_max_s"] = fenetre
        print("      fenêtre de durée : %d:%02d → %d:%02d"
              % (fenetre[0] // 60, fenetre[0] % 60, fenetre[1] // 60, fenetre[1] % 60))
        griefs, d, debit = controler(tmp, mots, seuils)
        if griefs:
            print("      REJETÉE — %s" % " ; ".join(griefs))
            print("      conservée pour écoute : outils/quarantaine/%s" % nom)
            rejetes.append((nom, griefs))
            continue
        # Un podcast ne va pas dans le meme dossier qu'une capsule : media.js
        # et l'index de playlist le cherchent dans podcasts/. Sans ce routage,
        # il atterrissait dans voix/ et restait invisible des deux cotes. Et le
        # dossier n'existe pas tant qu'aucune piste n'y a ete deposee : sans
        # makedirs, la premiere prise conforme, deja payee, echouait au depot.
        os.makedirs(dossier, exist_ok=True)
        os.replace(tmp, os.path.join(dossier, nom))
        print("      déposée — %d:%02d, %d mots/min" % (d // 60, d % 60, debit))
        deposes.append(nom)

    print("\nBilan\n-----")
    print("  %d déposée(s), %d rejetée(s), %d échec(s)" % (len(deposes), len(rejetes), len(echecs)))
    if rejetes:
        print("\n  Les prises rejetées attendent dans outils/quarantaine/ :")
        for nom, g in rejetes:
            print("    %-46s %s" % (nom[:46], " ; ".join(g)))
        print("  Écoutez-les. Si elles conviennent, déplacez-les dans site/%s." % cfg["dossier_sortie"])
    if args.temoin:
        if deposes:
            print("\n  Témoin(s) à écouter, rien n'a été déposé ni remplacé : %s"
                  % os.path.relpath(sortie, RACINE))
        return 1 if echecs else 0
    if deposes:
        print("\n  Pensez à régénérer l'index de la playlist :")
        print("      python3 outils/generer_playlist.py")
    return 1 if echecs else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n  interrompu. Les pistes déjà déposées sont conservées ; relancez pour la suite.")
        sys.exit(130)
