# -*- coding: utf-8 -*-
"""Les pièces communes du site miroir (docs/I18N.md, partie A) : mettre une page dans une seule langue, déclarer
sa langue, réécrire ses chemins pour sa jumelle sous en/. Servent à outils/data_tr_vers_miroir.py et à
outils/creer_jumelle.py ; aucune n'écrit de fichier.

Une page française X.html a sa jumelle anglaise en/X.html, un dossier plus bas : ses chemins vers les fichiers
partagés (assets/, médias, documents) descendent d'un cran, ses liens vers une page qui a, elle aussi, sa jumelle
restent tels quels. Les scripts, les styles et les commentaires ne sont jamais touchés, sauf les chemins de fichiers
des scripts d'une jumelle.
"""
import os
import posixpath
import re

OUVRANTE = re.compile(r'<([a-zA-Z][a-zA-Z0-9]*)\b[^>]*?\sdata-tr="(fr|en)"[^>]*>')
BALISE = re.compile(r"<[a-zA-Z][a-zA-Z0-9]*\b[^>]*>")
VIDES = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
# Les zones que la mise en langue ne touche pas : scripts, styles, commentaires.
INTACT = re.compile(r"<script\b.*?</script>|<style\b.*?</style>|<!--.*?-->", re.S | re.I)
ATTRIBUT_URL = re.compile(r'(\s(?:href|src|poster|data-src|action)=")([^"]*)(")', re.I)
SRCSET = re.compile(r'(\ssrcset=")([^"]*)(")', re.I)
CHAINE_CHEMIN = re.compile(
    r"""(["'])((?:\.\./|\./)*[A-Za-z0-9_][A-Za-z0-9_./%-]*\.(?:html|mp3|m4a|wav|ogg|pdf|png|jpe?g|webp|svg|gif|"""
    r"""docx|xlsx|pptx|zip|json|txt|vtt))(#[^"']*)?\1""")
SCRIPT = re.compile(r"(<script\b[^>]*>)(.*?)(</script>)", re.S | re.I)
# Un attribut à version anglaise : data-step-titre="…" data-step-titre-en="…". Les attributs data-i18n-*-fr/-en,
# eux, restent : i18n.js choisit leur valeur d'après la langue de la page.
ATTR_EN = re.compile(r'\sdata-((?!i18n-)[a-z][a-z0-9-]*?)-en="([^"]*)"')
# La marque d'une jumelle préparée par creer_jumelle.py et pas encore traduite : verifier_parite.py la refuse.
A_TRADUIRE = "<!-- À TRADUIRE : jumelle préparée par outils/creer_jumelle.py — retirer cette ligne une fois la page traduite -->"


class ErreurBloc(ValueError):
    """Un bloc data-tr sans fermeture : la page ne se coupe pas sans risque."""


def fin_element(t, tag, debut):
    """L'indice qui suit la fermeture de l'élément <tag> ouvert à debut, imbrications du même nom comprises."""
    prof = 0
    for m in re.finditer(r"<(/?)%s\b[^>]*>" % re.escape(tag), t[debut:], flags=re.I):
        if m.group(0).endswith("/>") and not m.group(1):
            continue
        prof += -1 if m.group(1) else 1
        if prof == 0:
            return debut + m.end()
    return -1


def attributs_dans_la_langue(balise, langue):
    """Une balise ouvrante : en anglais, data-X prend la valeur de data-X-en ; data-X-en disparaît dans les deux
    langues."""
    paires = [(m.group(1), m.group(2)) for m in ATTR_EN.finditer(balise)]
    if not paires:
        return balise
    balise = ATTR_EN.sub("", balise)
    if langue == "en":
        for nom, valeur in paires:
            motif = re.compile(r'(\sdata-%s=")[^"]*(")' % re.escape(nom))
            if motif.search(balise):
                balise = motif.sub(lambda m: m.group(1) + valeur + m.group(2), balise, count=1)
            else:
                fin = len(balise) - (2 if balise.endswith("/>") else 1)
                balise = balise[:fin] + ' data-%s="%s"' % (nom, valeur) + balise[fin:]
    return balise


def garder_langue_html(t, langue):
    """Un morceau de HTML sans script : les blocs de l'autre langue retirés (la ligne avec eux s'ils l'occupaient
    seuls), l'attribut data-tr ôté des autres, les attributs à version anglaise réglés."""
    autre = "en" if langue == "fr" else "fr"
    out, i = [], 0
    while True:
        m = OUVRANTE.search(t, i)
        if not m:
            break
        tag, lg = m.group(1).lower(), m.group(2)
        if lg == autre:
            fin = m.end() if tag in VIDES else fin_element(t, tag, m.start())
            if fin < 0:
                raise ErreurBloc('<%s data-tr="%s"> sans fermeture : « %s »' % (tag, lg, t[m.start():m.start() + 80]))
            debut_ligne = t.rfind("\n", 0, m.start()) + 1
            fin_ligne = t.find("\n", fin)
            fin_ligne = len(t) if fin_ligne < 0 else fin_ligne
            if not t[debut_ligne:m.start()].strip() and not t[fin:fin_ligne].strip() and debut_ligne >= i:
                out.append(t[i:debut_ligne])
                i = min(len(t), fin_ligne + 1)
            else:
                out.append(t[i:m.start()])
                i = fin
        else:
            out.append(t[i:m.start()])
            out.append(re.sub(r'\s+data-tr="%s"' % lg, "", m.group(0), count=1))
            i = m.end()
    out.append(t[i:])
    return BALISE.sub(lambda m: attributs_dans_la_langue(m.group(0), langue), "".join(out))


def garder_langue(t, langue):
    """La page entière dans une seule langue : scripts, styles et commentaires restent intacts."""
    morceaux, i = [], 0
    for m in INTACT.finditer(t):
        morceaux.append(garder_langue_html(t[i:m.start()], langue))
        morceaux.append(m.group(0))
        i = m.end()
    morceaux.append(garder_langue_html(t[i:], langue))
    return "".join(morceaux)


def bilingue(t):
    """Vrai si la page porte des blocs data-tr anglais, hors scripts."""
    return 'data-tr="en"' in INTACT.sub("", t)


def declarer(t, langue):
    """<html> déclare la langue de la page, et elle seule : i18n.js n'y pose alors pas de bouton 🌐, et
    navigation.js y charge le bouton FR / EN du site miroir."""
    def balise(m):
        b = m.group(0)
        for nom in ("lang", "data-lang", "data-langues"):
            b = re.sub(r'\s%s="[^"]*"' % nom, "", b)
        return b[:5] + ' lang="%s" data-lang="%s" data-langues="%s"' % (langue, langue, langue) + b[5:]
    return re.sub(r"<html\b[^>]*>", balise, t, count=1)


def reloger(t, rel, jumelles, site):
    """Les chemins de la page française rel (depuis la racine du site), réécrits pour sa jumelle sous en/. Une page
    de jumelles (l'ensemble des pages qui ont, ou auront, leur jumelle) reste au même chemin relatif ; tout autre
    fichier du site descend d'un cran."""
    dossier = posixpath.dirname(rel)
    dossier_en = posixpath.join("en", dossier) if dossier else "en"

    def nouveau(chemin):
        if not chemin or re.match(r"^(?:[a-z][a-z0-9+.-]*:|//|#|/|\{)", chemin, re.I):
            return chemin
        fichier, suite = re.match(r"([^?#]*)(.*)$", chemin, flags=re.S).groups()
        cible = posixpath.normpath(posixpath.join(dossier, fichier))
        if cible.startswith(".."):
            return chemin                                # hors du site : on n'y touche pas
        if cible in jumelles:
            return chemin                                # la jumelle anglaise de la page citée
        return posixpath.relpath(cible, dossier_en) + suite

    def attribut(m):
        return m.group(1) + nouveau(m.group(2)) + m.group(3)

    def srcset(m):
        parties = []
        for morceau in m.group(2).split(","):
            mots = morceau.strip().split()
            if mots:
                mots[0] = nouveau(mots[0])
            parties.append(" ".join(mots))
        return m.group(1) + ", ".join(parties) + m.group(3)

    def script(m):
        def chaine(mm):
            chemin = mm.group(2)
            cible = posixpath.normpath(posixpath.join(dossier, chemin))
            # Un chemin de fichier du site : un fichier qui existe, ou un média partagé encore à produire (une
            # capsule pas encore enregistrée vit déjà sous assets/). Une autre chaîne n'est pas touchée.
            if cible.startswith("..") or not (cible.startswith("assets/")
                                              or os.path.exists(os.path.join(site, *cible.split("/")))):
                return mm.group(0)
            return mm.group(1) + nouveau(chemin) + (mm.group(3) or "") + mm.group(1)
        return m.group(1) + CHAINE_CHEMIN.sub(chaine, m.group(2)) + m.group(3)

    morceaux, i = [], 0
    for m in INTACT.finditer(t):
        morceaux.append(SRCSET.sub(srcset, ATTRIBUT_URL.sub(attribut, t[i:m.start()])))
        bloc = m.group(0)
        if bloc[:7].lower() == "<script":
            if re.match(r"<script\b[^>]*\ssrc=", bloc, re.I):
                bloc = ATTRIBUT_URL.sub(attribut, bloc, count=1)
            bloc = SCRIPT.sub(script, bloc)
        morceaux.append(bloc)
        i = m.end()
    morceaux.append(SRCSET.sub(srcset, ATTRIBUT_URL.sub(attribut, t[i:])))
    return "".join(morceaux)


def charger_liste(t):
    """(texte, trouvé) : la jumelle charge la liste des pages traduites juste après i18n.js — son menu et le lien de
    son glossaire en ont besoin dès le premier affichage."""
    if "langues-data.js" in t:
        return t, True
    m = re.search(r'<script src="([^"]*)assets/js/i18n\.js"></script>', t)
    if not m:
        return t, False
    return t[:m.end()] + '\n<script src="%sassets/js/langues-data.js"></script>' % m.group(1) + t[m.end():], True
