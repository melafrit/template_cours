#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Les balises hreflang des pages jumelles du site miroir (docs/I18N.md, partie A).

    python3 outils/hreflang.py           # pose, met à jour ou retire les blocs
    python3 outils/hreflang.py --essai   # les liste sans rien écrire ; code 1 s'il y a à faire

Une page publique qui a sa jumelle — la page française et sa traduction sous en/, au même chemin — annonce ses deux
versions aux moteurs de recherche, dans son <head>, par un bloc que délimitent deux commentaires :

    <!-- hreflang : les versions française et anglaise de la page (outils/hreflang.py) -->
    <link rel="alternate" hreflang="fr" href="https://…/cours/chapitres/01-x.html">
    <link rel="alternate" hreflang="en" href="https://…/cours/en/chapitres/01-x.html">
    <link rel="alternate" hreflang="x-default" href="https://…/cours/chapitres/01-x.html">
    <!-- /hreflang -->

Les deux pages portent le même bloc, juste avant </head> : chacune se nomme et nomme l'autre (les moteurs ignorent
une annonce sans retour) ; la version par défaut, x-default, est la française. Les adresses sont absolues, sous
l'adresse publique du cours (« url » de deploiement/destination.json) ; une page index.html s'y annonce par son
dossier. Sans adresse publique, l'outil ne pose rien et le dit.

Ne sont jamais touchées : les zones protégées (« zones_protegees » de destination.json, et leurs jumelles sous en/),
ni une page noindex ou de redirection (meta refresh) ; une telle page qui porterait un bloc est signalée, pas
corrigée. Une page qui porte un bloc sans avoir (ou sans plus avoir) de jumelle publique le perd. Une page ne
s'écrit que si elle change : une seconde passe ne change rien.

L'ordre de génération : en dernier, après tout ce qui crée ou retire une page (data_tr_vers_miroir, creer_jumelle,
generer_langues, liens_langues, generer_nav_sections, generer_playlist). Un générateur qui réécrit une page entière
passe son texte par garder(), qui lui rend le bloc que portait la page remplacée. Son --essai fait partie des
contrôles avant mise en ligne. Repris du cours d'architecture logicielle.
"""
import argparse
import io
import json
import os
import re
import sys
import time
from html import escape
from urllib.parse import quote

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(RACINE, "site")
sys.path.insert(0, os.path.join(RACINE, "outils"))

DEBUT = "<!-- hreflang : les versions française et anglaise de la page (outils/hreflang.py) -->"
FIN = "<!-- /hreflang -->"
OUVERTURE = re.compile(r"<!-- hreflang\b[^>]*-->")
FERMETURE = re.compile(re.escape(FIN))
BLOC = re.compile(r"[ \t]*<!-- hreflang\b[^>]*-->.*?" + re.escape(FIN) + r"[ \t]*(?:\r?\n)?", re.S)
FIN_TETE = re.compile(r"</head\s*>", re.I)
META = re.compile(r"<meta\b[^>]*>", re.I)


def destination():
    """(adresse publique terminée par /, ou "" ; zones protégées) d'après deploiement/destination.json."""
    try:
        d = json.load(io.open(os.path.join(RACINE, "deploiement", "destination.json"), encoding="utf-8"))
    except (OSError, ValueError):
        return "", ()
    url = str(d.get("url") or "").strip()
    zones = tuple(z.strip("/") + "/" for z in d.get("zones_protegees") or [] if str(z).strip("/"))
    return (url.rstrip("/") + "/" if url else ""), zones


ADRESSE, PROTEGEES = destination()


def chemin(rel):
    return os.path.join(SITE, *rel.split("/"))


def lire(rel):
    with io.open(chemin(rel), encoding="utf-8", newline="") as fh:
        return fh.read()


def jumelles(rel):
    """(française, anglaise) : les deux versions d'une page, chemins depuis la racine du site."""
    fr = rel[3:] if rel.startswith("en/") else rel
    return fr, "en/" + fr


def publique(texte):
    """Faux pour une page noindex ou de redirection (meta refresh) : les balises <meta> de son <head> le disent."""
    fin = FIN_TETE.search(texte)
    for m in META.finditer(texte[:fin.start()] if fin else texte):
        balise = m.group(0).lower()
        if re.search(r"""\bhttp-equiv\s*=\s*["']?refresh""", balise):
            return False
        if re.search(r"""\bname\s*=\s*["']?robots\b""", balise) and "noindex" in balise:
            return False
    return True


def intouchable(rel, texte):
    """Vrai pour une page que l'outil ne touche jamais : zone protégée, page noindex ou de redirection."""
    return bool(PROTEGEES) and jumelles(rel)[0].startswith(PROTEGEES) or not publique(texte)


def paire(rel):
    """(française, anglaise) si la page rel a une jumelle publique, None sinon."""
    fr, en = jumelles(rel)
    if PROTEGEES and fr.startswith(PROTEGEES):
        return None
    autre = en if rel == fr else fr
    if not os.path.isfile(chemin(autre)) or not publique(lire(autre)):
        return None
    return fr, en


def adresse(rel):
    """L'adresse publique d'une page : celle du cours, suivie du chemin ; une page index.html, par son dossier."""
    if rel == "index.html" or rel.endswith("/index.html"):
        rel = rel[:-len("index.html")]
    return ADRESSE + quote(rel, safe="/")


def bloc(fr, en, nl="\n"):
    lignes = [DEBUT] + ['<link rel="alternate" hreflang="%s" href="%s">' % (langue, escape(adresse(rel), quote=True))
                        for langue, rel in (("fr", fr), ("en", en), ("x-default", fr))] + [FIN]
    return nl.join(lignes)


def poser(texte, rel):
    """Le texte de la page rel avec le bloc qui lui revient : celui de sa paire si elle a une jumelle publique, aucun
    sinon. Une page intouchable est rendue telle quelle."""
    if intouchable(rel, texte):
        return texte
    nu = BLOC.sub("", texte)
    p = paire(rel)
    fin = FIN_TETE.search(nu)
    if not p or not fin:
        return nu
    nl = "\r\n" if "\r\n" in nu else "\n"
    debut_ligne = nu.rfind("\n", 0, fin.start()) + 1
    if nu[debut_ligne:fin.start()].strip():               # </head> n'est pas seul sur sa ligne
        return nu[:fin.start()] + nl + bloc(*p, nl=nl) + nl + nu[fin.start():]
    return nu[:debut_ligne] + bloc(*p, nl=nl) + nl + nu[debut_ligne:]


def garder(chemin_page, texte):
    """Pour un générateur qui réécrit une page entière, juste avant de l'écrire : la page neuve reçoit le bloc que
    portait la page qu'elle remplace, recalculé. Une page qui n'en portait pas reste sans : seul hreflang.py en pose."""
    try:
        with io.open(chemin_page, encoding="utf-8", newline="") as fh:
            ancien = fh.read()
    except OSError:
        return texte
    if not OUVERTURE.search(ancien) or not ADRESSE:
        return texte
    return poser(texte, os.path.relpath(os.path.abspath(chemin_page), SITE).replace(os.sep, "/"))


def pages_du_site():
    """Les pages HTML du site, chemins depuis sa racine : tout sauf assets/ et les dossiers cachés ou temporaires."""
    for dossier, sous, fichiers in os.walk(SITE):
        rel = os.path.relpath(dossier, SITE).replace(os.sep, "/")
        sous[:] = sorted(d for d in sous if not d.startswith((".", "_")) and not (rel == "." and d == "assets"))
        for f in sorted(fichiers):
            if f.endswith(".html") and not f.startswith((".", "_")):
                yield f if rel == "." else rel + "/" + f


def ecrire(rel, texte):
    """Écrit une page telle quelle (fins de ligne comprises). Windows retient parfois un fichier qu'on vient de lire
    (antivirus, indexation) : on réessaie quelques fois."""
    for essai in range(6):
        try:
            with io.open(chemin(rel), "w", encoding="utf-8", newline="") as fh:
                fh.write(texte)
            return
        except OSError:
            if essai == 5:
                raise
            time.sleep(0.3 * (essai + 1))


def liste_publiee():
    """La liste des pages traduites telle que site/assets/js/langues-data.js la publie (None si illisible)."""
    try:
        texte = io.open(os.path.join(SITE, "assets", "js", "langues-data.js"), encoding="utf-8").read()
        return json.loads(re.search(r"window\.TPL_LANGUES\s*=\s*(\[.*?\]);", texte, re.S).group(1))
    except (OSError, AttributeError, ValueError):
        return None


def main():
    for flux in (sys.stdout, sys.stderr):
        try:
            flux.reconfigure(encoding="utf-8")
        except Exception:
            pass
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--essai", action="store_true", help="liste ce qui est à faire, sans rien écrire")
    args = ap.parse_args()
    import generer_langues as GL                      # la liste des pages traduites, déduite des fichiers de en/
    traduites = GL.pages_traduites(SITE)
    if not ADRESSE:
        print("Adresse publique inconnue (« url » de deploiement/destination.json) : aucun bloc hreflang posé. "
              "%d page(s) traduite(s) l'attendent." % len(traduites))
        return 0
    paires = [fr for fr in traduites if not intouchable(fr, lire(fr)) and paire(fr)]
    ecartees = sorted(set(traduites) - set(paires))
    a_faire, anomalies, portent = [], [], 0
    for rel in pages_du_site():
        texte = lire(rel)
        n_ouv, n_ferm = len(OUVERTURE.findall(texte)), len(FERMETURE.findall(texte))
        if intouchable(rel, texte):
            if n_ouv or n_ferm:
                anomalies.append("%s : page protégée, noindex ou de redirection qui porte un bloc hreflang — à "
                                 "retirer à la main (l'outil n'y touche pas)" % rel)
            continue
        if n_ouv != n_ferm or n_ouv > 1:
            anomalies.append("%s : bloc hreflang mal formé (%d ouverture(s), %d fermeture(s)) — à réparer à la main"
                             % (rel, n_ouv, n_ferm))
            continue
        if not FIN_TETE.search(texte) and paire(rel):
            anomalies.append("%s : pas de </head>, où poser le bloc" % rel)
            continue
        neuf = poser(texte, rel)
        portent += bool(OUVERTURE.search(neuf))
        if neuf == texte:
            continue
        action = ("bloc mis à jour" if n_ouv and OUVERTURE.search(neuf) else "bloc retiré (plus de jumelle publique)"
                  if n_ouv else "bloc posé")
        a_faire.append((rel, action))
        if not args.essai:
            ecrire(rel, neuf)
    for rel, action in a_faire:
        print("  %s : %s" % (rel, action))
    for x in anomalies:
        print("  ✗", x)
    print("%d paire(s) de pages jumelles publiques, soit %d pages%s." % (
        len(paires), 2 * len(paires),
        " ; écartée(s), car protégée(s) ou non publique(s) : " + ", ".join(ecartees) if ecartees else ""))
    publiee = liste_publiee()
    if publiee is not None and publiee != traduites:
        print("  · site/assets/js/langues-data.js ne suit plus les fichiers de en/ : python3 outils/generer_langues.py")
    if a_faire:
        print("%d page(s) %s." % (len(a_faire), "à mettre à jour" if args.essai else "mise(s) à jour"))
    if anomalies:
        print("%d page(s) à reprendre à la main (✗ ci-dessus)." % len(anomalies))
    if not a_faire and not anomalies:
        print("Rien à faire : %d page(s) portent leur bloc." % portent)
    return 1 if anomalies or (args.essai and a_faire) else 0


if __name__ == "__main__":
    sys.exit(main())
