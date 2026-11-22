#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Les balises hreflang des pages jumelles du site miroir (docs/I18N.md, partie A).

    python3 outils/hreflang.py           # pose, met à jour ou retire les blocs
    python3 outils/hreflang.py --essai   # les liste sans rien écrire ; code 1 s'il y a à faire

Une page publique qui a au moins une jumelle (la page de la racine et ses traductions sous en/, ar/…, au même
chemin) annonce toutes ses versions aux moteurs de recherche, dans son <head>, par un bloc que délimitent deux
commentaires :

    <!-- hreflang : les versions de la page dans chaque langue (outils/hreflang.py) -->
    <link rel="alternate" hreflang="fr" href="https://…/cours/chapitres/01-x.html">
    <link rel="alternate" hreflang="en" href="https://…/cours/en/chapitres/01-x.html">
    <link rel="alternate" hreflang="ar" href="https://…/cours/ar/chapitres/01-x.html">
    <link rel="alternate" hreflang="x-default" href="https://…/cours/chapitres/01-x.html">
    <!-- /hreflang -->

Toutes les versions portent le même bloc, juste avant </head> : chacune se nomme et nomme les autres (les moteurs
ignorent une annonce sans retour). La version par défaut, x-default, est celle de la racine, dans la langue de
l'accueil (generer_langues.py) ; une langue dont la page manque, ou n'est pas publique, n'y figure pas. Les adresses
sont absolues, sous l'adresse publique du cours (« url » de deploiement/destination.json) ; une page index.html
s'y annonce par son dossier. Sans adresse publique, l'outil ne pose rien et le dit.

Ne sont jamais touchées : les zones protégées (« zones_protegees » de destination.json, et leurs jumelles dans
chaque langue), ni une page noindex ou de redirection (meta refresh) ; une telle page qui porterait un bloc est
signalée, pas corrigée. Une page qui porte un bloc sans avoir (ou sans plus avoir) de jumelle publique le perd, de
même qu'une jumelle dont la page de la racine n'est pas publique. Une page ne s'écrit que si elle change : une
seconde passe ne change rien. Un cours créé n'hérite d'aucun bloc de la démonstration (nouveau_cours.py les
retire) ; ce script pose les siens, sous son adresse.

L'ordre de génération : en dernier, après tout ce qui crée ou retire une page (data_tr_vers_miroir, creer_jumelle,
generer_langues, liens_langues, generer_nav_sections, generer_playlist). Un générateur qui réécrit une page entière
passe son texte par garder(), qui lui rend le bloc que portait la page remplacée. Son --essai fait partie des
contrôles avant mise en ligne. Repris du cours d'architecture logicielle ; étendu à toutes les langues du site
miroir le 23 novembre 2026.
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
import generer_langues as GL                      # noqa: E402  la langue racine et les langues du gabarit

DEBUT = "<!-- hreflang : les versions de la page dans chaque langue (outils/hreflang.py) -->"
FIN = "<!-- /hreflang -->"
OUVERTURE = re.compile(r"<!-- hreflang\b[^>]*-->")
FERMETURE = re.compile(re.escape(FIN))
BLOC = re.compile(r"[ \t]*<!-- hreflang\b[^>]*-->.*?" + re.escape(FIN) + r"[ \t]*(?:\r?\n)?", re.S)
FIN_TETE = re.compile(r"</head\s*>", re.I)
META = re.compile(r"<meta\b[^>]*>", re.I)
# La langue des pages de la racine, puis celles des jumelles, dans l'ordre du choix de langue.
LANGUE_RACINE = GL.langue_racine(SITE)
AUTRES = tuple(lg for lg in GL.LANGUES if lg != LANGUE_RACINE)


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


def version(rel):
    """(chemin à la racine, langue) d'une page ; « ar/chapitres/01-x.html » donne (« chapitres/01-x.html », « ar »)."""
    for lg in AUTRES:
        if rel.startswith(lg + "/"):
            return rel[len(lg) + 1:], lg
    return rel, LANGUE_RACINE


def dans(base, lg):
    """Le chemin de la version <lg> d'une page de la racine."""
    return base if lg == LANGUE_RACINE else lg + "/" + base


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
    """Vrai pour une page que l'outil ne touche jamais : zone protégée, dans toute langue, ou page noindex ou de
    redirection."""
    return bool(PROTEGEES) and version(rel)[0].startswith(PROTEGEES) or not publique(texte)


def groupe(rel):
    """[(langue, chemin)] : les versions publiques de la page rel, la racine d'abord, quand elle en a au moins deux,
    dont celle de la racine ; None sinon."""
    base = version(rel)[0]
    if PROTEGEES and base.startswith(PROTEGEES):
        return None
    versions = [(lg, dans(base, lg)) for lg in (LANGUE_RACINE,) + AUTRES]
    versions = [(lg, r) for lg, r in versions if os.path.isfile(chemin(r)) and publique(lire(r))]
    if len(versions) < 2 or versions[0][0] != LANGUE_RACINE:
        return None
    return versions


def adresse(rel):
    """L'adresse publique d'une page : celle du cours, suivie du chemin ; une page index.html, par son dossier."""
    if rel == "index.html" or rel.endswith("/index.html"):
        rel = rel[:-len("index.html")]
    return ADRESSE + quote(rel, safe="/")


def bloc(versions, nl="\n"):
    lignes = [DEBUT] + ['<link rel="alternate" hreflang="%s" href="%s">' % (langue, escape(adresse(rel), quote=True))
                        for langue, rel in versions + [("x-default", versions[0][1])]] + [FIN]
    return nl.join(lignes)


def poser(texte, rel):
    """Le texte de la page rel avec le bloc qui lui revient : celui de ses versions si elle a une jumelle publique,
    aucun sinon. Une page intouchable est rendue telle quelle."""
    if intouchable(rel, texte):
        return texte
    nu = BLOC.sub("", texte)
    g = groupe(rel)
    fin = FIN_TETE.search(nu)
    if not g or not fin:
        return nu
    nl = "\r\n" if "\r\n" in nu else "\n"
    debut_ligne = nu.rfind("\n", 0, fin.start()) + 1
    if nu[debut_ligne:fin.start()].strip():               # </head> n'est pas seul sur sa ligne
        return nu[:fin.start()] + nl + bloc(g, nl=nl) + nl + nu[fin.start():]
    return nu[:debut_ligne] + bloc(g, nl=nl) + nl + nu[debut_ligne:]


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
    """(langue racine, {langue : pages}) tels que site/assets/js/langues-data.js les publie (None si illisible)."""
    try:
        texte = io.open(os.path.join(SITE, "assets", "js", "langues-data.js"), encoding="utf-8").read()
        miroir = json.loads(re.search(r"window\.TPL_MIROIR\s*=\s*(\{.*\});", texte, re.S).group(1))
        return miroir.get("racine"), miroir.get("pages", {})
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
    racine, pages = GL.pages_par_langue(SITE)          # les pages traduites, déduites des dossiers de langue
    traduites = sorted({p for liste in pages.values() for p in liste})
    if not ADRESSE:
        print("Adresse publique inconnue (« url » de deploiement/destination.json) : aucun bloc hreflang posé. "
              "%d page(s) traduite(s) l'attendent." % len(traduites))
        return 0
    groupes = [g for g in (groupe(base) for base in traduites if not intouchable(base, lire(base))) if g]
    ecartees = sorted(set(traduites) - {g[0][1] for g in groupes})
    a_faire, anomalies, portent = [], [], 0
    for rel in pages_du_site():
        texte = lire(rel)
        n_ouv, n_ferm = len(OUVERTURE.findall(texte)), len(FERMETURE.findall(texte))
        if intouchable(rel, texte):
            if n_ouv or n_ferm:
                anomalies.append("%s : page protégée, noindex ou de redirection qui porte un bloc hreflang, à "
                                 "retirer à la main (l'outil n'y touche pas)" % rel)
            continue
        if n_ouv != n_ferm or n_ouv > 1:
            anomalies.append("%s : bloc hreflang mal formé (%d ouverture(s), %d fermeture(s)), à réparer à la main"
                             % (rel, n_ouv, n_ferm))
            continue
        if not FIN_TETE.search(texte) and groupe(rel):
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
    print("%d groupe(s) de pages jumelles publiques, soit %d pages (%s)%s." % (
        len(groupes), sum(len(g) for g in groupes),
        ", ".join("%s %d" % (lg, sum(1 for g in groupes for l, _r in g if l == lg))
                  for lg in (LANGUE_RACINE,) + AUTRES if any(l == lg for g in groupes for l, _r in g)),
        " ; écartée(s), car protégée(s) ou non publique(s) : " + ", ".join(ecartees) if ecartees else ""))
    publiee = liste_publiee()
    if publiee is not None and publiee != (racine, pages):
        print("  · site/assets/js/langues-data.js ne suit plus les dossiers de langue : python3 outils/generer_langues.py")
    if a_faire:
        print("%d page(s) %s." % (len(a_faire), "à mettre à jour" if args.essai else "mise(s) à jour"))
    if anomalies:
        print("%d page(s) à reprendre à la main (✗ ci-dessus)." % len(anomalies))
    if not a_faire and not anomalies:
        print("Rien à faire : %d page(s) portent leur bloc." % portent)
    return 1 if anomalies or (args.essai and a_faire) else 0


if __name__ == "__main__":
    sys.exit(main())
