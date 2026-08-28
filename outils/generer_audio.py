#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère les capsules audio manquantes avec l'API ElevenLabs.

    python3 outils/generer_audio.py --essai            # ce qui serait généré, sans dépenser
    python3 outils/generer_audio.py --chapitre 6       # un chapitre à la fois
    python3 outils/generer_audio.py --limite 1         # une seule piste, pour écouter
    python3 outils/generer_audio.py                    # tout ce qui manque

Les scripts ne sont pas écrits ici : ils viennent des fiches de production de
`docs/prompts/`, qui restent la source unique. Le nom du fichier attendu par la
page sert de clé : ce que la page réclame est ce qui est généré, et rien d'autre.

CHAQUE PRISE EST CONTRÔLÉE AVANT D'ÊTRE DÉPOSÉE. Une capsule du chapitre 5 est
partie en ligne à 67 mots par minute au lieu de 145 — le même texte étiré sur le
double du temps, faute d'un réglage. Personne ne l'avait entendue. Le script
mesure donc durée, débit et silences ; ce qui sort des clous va en quarantaine
avec la raison, jamais dans le site.

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

# Seuils de référence, mesurés sur les prises validées du cours : débit de 121 à
# 165 mots par minute, durées de 1 min 07 à 2 min 12, aucun silence au-delà de
# 2,1 s. Les bornes ajoutent une marge à ces extrêmes.
#
# Ils vivent ICI, dans le code, et non dans la configuration. Une première
# version les avait placés dans elevenlabs.json : une configuration copiée avant
# un recalibrage gardait les anciennes valeurs, et rejetait de bonnes prises sans
# que personne ne comprenne pourquoi. La configuration peut toujours les
# surcharger, mais elle doit alors le faire sciemment — le script le signale.
SEUILS = {
    "mots_par_minute_min": 115,
    "mots_par_minute_max": 175,
    "duree_min_s": 55,
    "duree_max_s": 145,
    "silence_max_s": 3.0,
}

for flux in (sys.stdout, sys.stderr):
    try:
        flux.reconfigure(encoding="utf-8")
    except Exception:
        pass


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


def synthese(cfg, texte):
    """Renvoie les octets MP3, ou lève une exception explicite."""
    url = "%s/text-to-speech/%s?output_format=%s" % (
        BASE, cfg["voix_id"], cfg.get("format_sortie", "mp3_44100_128"))
    r = cfg.get("reglages", {})
    corps = {
        "text": texte,
        "model_id": cfg.get("modele", "eleven_v3"),
        "voice_settings": {
            "stability": r.get("stabilite", 0.5),
            "similarity_boost": r.get("similarite", 0.8),
            "style": r.get("style", 0.1),
            "use_speaker_boost": bool(r.get("renfort_locuteur", True)),
        },
    }
    if r.get("vitesse") not in (None, 1.0):
        corps["voice_settings"]["speed"] = r["vitesse"]
    req = urllib.request.Request(
        url, data=json.dumps(corps).encode("utf-8"),
        headers={"xi-api-key": cfg["cle_api"], "Content-Type": "application/json",
                 "Accept": "audio/mpeg", "User-Agent": "cours-reglementation/1.0"})
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
    if d < seuils.get("duree_min_s", 55):
        griefs.append("trop courte : %d s" % d)
    if d > seuils.get("duree_max_s", 125):
        griefs.append("trop longue : %d min %02d s" % (d // 60, d % 60))
    debit = mots / d * 60 if d else 0
    if debit < seuils.get("mots_par_minute_min", 130):
        griefs.append("débit trop lent : %d mots/min" % debit)
    elif debit > seuils.get("mots_par_minute_max", 165):
        griefs.append("débit trop rapide : %d mots/min" % debit)
    seuil_sil = seuils.get("silence_max_s", SEUILS["silence_max_s"])
    trous = silences(chemin, seuil_sil)
    if trous:
        griefs.append("silence de %s s" % " et ".join("%.1f" % x for x in trous))
    return griefs, d, debit


# ---------------------------------------------------------------- inventaire
def etiquette(n):
    """« ch3 » pour un chapitre, « page » pour une page hors chapitre."""
    return "ch%d" % n if n else "page"


def pages_a_scruter():
    """Les huit chapitres, puis les pages racine qui portent des capsules.

    La soutenance vidéo n'est pas un chapitre mais porte une capsule : la
    limiter à chapitres/0*.html rendait sa piste invisible au générateur.
    """
    pages = [(int(os.path.basename(p)[:2]), p)
             for p in sorted(glob.glob(os.path.join(SITE, "chapitres", "0*.html")))]
    for p in sorted(glob.glob(os.path.join(SITE, "*.html"))):
        if "RDCX.voice(" in io.open(p, encoding="utf-8").read():
            pages.append((0, p))
    return pages


def pistes_attendues():
    """[(chapitre, conteneur, nom_fichier, titre)] dans l'ordre des pages.

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
    return out


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


def scripts_des_fiches():
    """{nom_fichier: script ElevenLabs} — les fiches sont la source unique."""
    d = {}
    for fiche in sorted(glob.glob(os.path.join(RACINE, "docs", "prompts", "*.md"))):
        t = io.open(fiche, encoding="utf-8").read()
        for m in re.finditer(
                r"\*\*Nom exact du fichier :\*\*\s*`([^`]+)`(.*?)(?=\*\*Nom exact du fichier :\*\*|\Z)",
                t, re.S):
            nom, bloc = m.group(1), m.group(2)
            sc = re.search(r"\*\*▶️ Script ElevenLabs\*\*\s*\n+```\n(.*?)\n```", bloc, re.S)
            if sc and nom.endswith(".mp3"):
                d[nom] = sc.group(1).strip()
    return d


def tolerances_des_fiches():
    """{nom_fichier: (duree_min_s, duree_max_s)} lue dans les fiches.

    Les seuils du code sont calibres sur des capsules de 1 a 2 minutes. Une
    piste longue les depasse par construction et serait rejetee pour « trop
    longue ». Une fiche peut donc declarer sa propre fenetre, sous la forme
    « tolerance 3 min 15 → 4 min 15 », et c'est elle qui s'applique alors.
    Le debit et les silences, eux, restent controles a l'identique.
    """
    d = {}
    for fiche in sorted(glob.glob(os.path.join(RACINE, "docs", "prompts", "*.md"))):
        t = io.open(fiche, encoding="utf-8").read()
        for m in re.finditer(
                r"\*\*Nom exact du fichier :\*\*\s*`([^`]+)`(.*?)(?=\*\*Nom exact du fichier :\*\*|\Z)",
                t, re.S):
            nom, bloc = m.group(1), m.group(2)
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
    # Les seuils de référence viennent du code ; la configuration ne fait que
    # les surcharger, clé par clé, et jamais en silence.
    surcharges = c.get("controles") or {}
    seuils = dict(SEUILS)
    ecarts = []
    for cle, val in surcharges.items():
        if cle in SEUILS and val != SEUILS[cle]:
            ecarts.append("%s : %s au lieu de %s" % (cle, val, SEUILS[cle]))
        seuils[cle] = val
    if ecarts:
        print("\n  /!\\ Votre configuration modifie les seuils de contrôle :")
        for e in ecarts:
            print("      %s" % e)
        print("      Retirez le bloc « controles » de outils/elevenlabs.json pour")
        print("      revenir aux valeurs de référence, calibrées sur les prises du cours.")
    c["controles"] = seuils
    c.setdefault("dossier_sortie", "assets/media/voix")
    return c


# ---------------------------------------------------------------- programme
def main():
    ap = argparse.ArgumentParser(description="Génère les capsules audio manquantes.")
    ap.add_argument("--essai", action="store_true", help="liste et coût, sans appeler l'API")
    ap.add_argument("--chapitre", type=int, help="ne traiter qu'un chapitre")
    ap.add_argument("--limite", type=int, help="s'arrêter après N pistes")
    ap.add_argument("--force", action="store_true", help="régénérer même si le fichier existe")
    args = ap.parse_args()

    cfg = charger()
    sortie = os.path.join(SITE, cfg["dossier_sortie"])
    scripts = scripts_des_fiches()
    tolerances = tolerances_des_fiches()

    travail, sans_script = [], []
    for n, cid, nom, titre in pistes_attendues():
        if args.chapitre and n != args.chapitre:
            continue
        if os.path.exists(os.path.join(sortie, nom)) and not args.force:
            continue
        sc = scripts.get(nom)
        if not sc:
            sans_script.append((n, nom))
            continue
        travail.append((n, nom, titre, sc))
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

    total_car = sum(len(s) for _n, _f, _t, s in travail)
    for n, nom, titre, sc in travail:
        print("  %-4s %-46s %5d car.  %3d mots" % (etiquette(n), nom[:46], len(sc), mots_parles(sc)))
    print("\n  %d piste(s), %s caractères" % (len(travail), format(total_car, ",")))
    print("  voix « %s », modèle « %s »" % (cfg["voix_id"], cfg.get("modele")))

    if args.essai:
        print("\n  Simulation : aucun appel, aucun crédit consommé.")
        return 0

    if not os.path.isdir(QUARANTAINE):
        os.makedirs(QUARANTAINE)

    print("\nGénération\n----------")
    deposes, rejetes, echecs = [], [], []
    for i, (n, nom, titre, sc) in enumerate(travail, 1):
        print("  [%d/%d] %s  %s" % (i, len(travail), etiquette(n), nom))
        try:
            audio = synthese(cfg, sc)
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

        seuils = dict(cfg["controles"])
        if nom in tolerances:
            seuils["duree_min_s"], seuils["duree_max_s"] = tolerances[nom]
            print("      fenêtre déclarée par la fiche : %d:%02d → %d:%02d"
                  % (seuils["duree_min_s"] // 60, seuils["duree_min_s"] % 60,
                     seuils["duree_max_s"] // 60, seuils["duree_max_s"] % 60))
        griefs, d, debit = controler(tmp, mots_parles(sc), seuils)
        if griefs:
            print("      REJETÉE — %s" % " ; ".join(griefs))
            print("      conservée pour écoute : outils/quarantaine/%s" % nom)
            rejetes.append((nom, griefs))
            continue
        os.replace(tmp, os.path.join(sortie, nom))
        print("      déposée — %d:%02d, %d mots/min" % (d // 60, d % 60, debit))
        deposes.append(nom)

    print("\nBilan\n-----")
    print("  %d déposée(s), %d rejetée(s), %d échec(s)" % (len(deposes), len(rejetes), len(echecs)))
    if rejetes:
        print("\n  Les prises rejetées attendent dans outils/quarantaine/ :")
        for nom, g in rejetes:
            print("    %-46s %s" % (nom[:46], " ; ".join(g)))
        print("  Écoutez-les. Si elles conviennent, déplacez-les dans %s." % cfg["dossier_sortie"])
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
