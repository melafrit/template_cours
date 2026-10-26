# -*- coding: utf-8 -*-
"""Chrome (ou Edge) sans interface, pour deux besoins du livret.

LES PHOTOGRAPHIES : un schéma SVG du site, la planche des pictogrammes, la composition de la page de garde
deviennent des PNG haute définition (--screenshot), avec un profil temporaire ; le PNG est ramené à la taille
attendue (largeur × hauteur × échelle).

LES COMPOSANTS D'UNE PAGE : les activités et les capsules du moteur (assets/js/interactions.js) reçoivent leurs
textes au chargement — l'objet TEXTES de la page, des .map… —, qu'un lecteur du source ne verrait pas. Ouverte avec
« ?polycopie=<langue> », la page écrit la configuration de chacun dans <script type="application/json"
id="rdcx-donnees"> ; Chrome rend la page ainsi chargée (--dump-dom), et le livret lit exactement ce que voient les
étudiants, dans la langue du livret.
"""
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

CHROMES = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
           r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
           r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
           r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
           "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
COMMUNS = ["--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run", "--no-default-browser-check",
           "--allow-file-access-from-files"]
DONNEES = re.compile(r'<script type="application/json" id="rdcx-donnees">(.*?)</script>', re.S)


def chrome():
    """Le chemin de Chrome ou d'Edge ; SystemExit s'il n'y en a pas."""
    for c in CHROMES:
        if os.path.exists(c):
            return c
    for nom in ("google-chrome", "chromium", "chromium-browser", "chrome", "msedge"):
        trouve = shutil.which(nom)
        if trouve:
            return trouve
    raise SystemExit("Chrome ou Edge introuvable : le livret en a besoin pour ses images et pour lire les activités "
                     "des pages.")


def photographier(travaux):
    """Chaque travail (adresse, sortie, largeur, hauteur, échelle) → une photographie PNG à la taille attendue."""
    from PIL import Image
    if not travaux:
        return 0
    navigateur = chrome()
    with tempfile.TemporaryDirectory(prefix="polycopie-chrome-") as profil:
        for i, (url, sortie, largeur, hauteur, echelle) in enumerate(travaux, 1):
            os.makedirs(os.path.dirname(sortie), exist_ok=True)
            subprocess.run([navigateur] + COMMUNS + [f"--user-data-dir={profil}",
                                                     f"--force-device-scale-factor={echelle:g}",
                                                     f"--window-size={largeur},{hauteur}",
                                                     "--virtual-time-budget=6000", f"--screenshot={sortie}", url],
                           check=True, capture_output=True, timeout=120)
            attendu = (round(largeur * echelle), round(hauteur * echelle))
            with Image.open(sortie) as im:
                im.load()
                taille = im.size
                rogne = (im.crop((0, 0, min(taille[0], attendu[0]), min(taille[1], attendu[1])))
                         if taille[0] > attendu[0] or taille[1] > attendu[1] else None)
            if taille[0] < attendu[0] - 2 or taille[1] < attendu[1] - 2:
                raise SystemExit(f"PNG trop petit : {sortie} {taille}, {attendu} attendus")
            if rogne is not None:
                rogne.save(sortie)
            if i % 25 == 0:
                print(f"  … {i} / {len(travaux)} PNG")
    return len(travaux)


def composants(chemin_page, langue):
    """{identifiant : (sorte, configuration)} des composants que la page monte (voice, reveal, checkpoint, match,
    spotError, branch, hotspots), tels que la page les calcule dans la langue (fr ou en)."""
    url = Path(os.path.abspath(chemin_page)).as_uri() + f"?polycopie={langue}"
    with tempfile.TemporaryDirectory(prefix="polycopie-chrome-") as profil:
        r = subprocess.run([chrome()] + COMMUNS + [f"--user-data-dir={profil}", "--virtual-time-budget=8000",
                                                   "--dump-dom", url],
                           capture_output=True, timeout=120)
    dom = r.stdout.decode("utf-8", "replace")
    m = DONNEES.search(dom)
    if not m:
        if "RDCX." in open(chemin_page, encoding="utf-8").read():
            raise SystemExit(f"Les composants de {chemin_page} sont illisibles : la page ne rend pas leurs données "
                             "(assets/js/interactions.js, « ?polycopie »).")
        return {}
    d = json.loads(m.group(1))
    if d.get("langue") and d["langue"] != langue:
        raise SystemExit(f"{chemin_page} : composants rendus en « {d['langue']} », « {langue} » attendu.")
    return {ident: (c.get("sorte"), c.get("config") or {}) for ident, c in (d.get("composants") or {}).items()}
