#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""La série de podcasts du cours (module 03) : la source unique de ses épisodes, dans les deux langues.

    python3 outils/podcasts.py    # contrôle la source et dit, épisode par épisode, ce qui est en ligne

Un épisode : num ; nom, celui de ses fichiers (sans langue ni extension) ; voix, « notebooklm » (les deux voix de
NotebookLM) ou « auteur » (la voix clonée de l'auteur, ElevenLabs : la mention du pied de la page le dit alors) ;
page, la page du cours qu'il accompagne (depuis la racine des pages de sa langue), qui porte son encadré « Le podcast
du chapitre » (fragment podcast-N), ou None ; et, en français et en anglais : titre ; court, son libellé dans le
sommaire ; page_nom, le nom de sa page dans « À lire avec l'épisode » ; etiquette et accroche, l'étiquette et la
phrase de l'encadré ; couvre, ce qu'il couvre (deux ou trois phrases) ; retenir, ce qu'il faut en retenir (trois à
cinq points, autant dans les deux langues). Les textes s'écrivent d'après le script ou le prompt de l'épisode : rien
d'inventé, aucune réponse aux exercices ni aux QCM ; l'auteur les vérifie à l'écoute.

Les fichiers, <lg> valant fr ou en :
  Podcasts/<lg>/<nom>.<wav|m4a|mp3|mp4|aac|ogg|webm>  l'épisode brut, déposé par l'auteur : jamais versionné ni publié
  Podcasts/<lg>/<nom>.pdf                              son diaporama brut
  site/assets/media/podcasts/<nom>.<lg>.mp3            l'épisode publié : mono, 64 kbit/s, 44,1 kHz
  site/assets/media/podcasts/<nom>.<lg>.pdf            le diaporama publié, à télécharger
  site/assets/media/podcasts/diaporamas/<nom>.<lg>/    ses diapositives : diapo-01.webp…, vignette-01.webp…
L'épisode d'un chapitre se nomme chapitre-<N>-podcast : le lecteur du chapitre (assets/js/media.js) joue le même
fichier. outils/generer_podcasts.py fait le passage du brut au publié ; outils/generer_fragments.py écrit, d'après ce
fichier, la page site/podcasts.html (fragments podcasts, podcasts-etat, podcasts-mention) et les encadrés des pages
(fragments podcast-N). Les durées et les dimensions se lisent dans les fichiers publiés, sans ffprobe ni Pillow.

La démonstration : un épisode, le podcast du chapitre 1, dit par la voix de l'auteur (son script :
docs/prompts/Capsules_du_cours_demo.md). nouveau_cours.py vide la liste pour un cours créé. Repris, en générique et
bilingue, du cours d'architecture logicielle.
"""
import html
import io
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(RACINE, "site")
MEDIA = "assets/media/podcasts"                 # depuis la racine du site : les médias servent aux deux langues
LANGUES = ("fr", "en")
VOIX = ("notebooklm", "auteur")
# Les formats d'un épisode brut : ceux que .gitignore tient hors du dépôt.
EXTENSIONS_AUDIO = (".wav", ".m4a", ".mp3", ".mp4", ".aac", ".ogg", ".webm")

EPISODES = [
    dict(num=1, nom="chapitre-1-podcast", voix="auteur", page="chapitres/01-cadrage.html",
         titre={"fr": "Chapitre 1 · Cadrer son cours", "en": "Chapter 1 · Scoping your course"},
         court={"fr": "Chapitre 1", "en": "Chapter 1"},
         page_nom={"fr": "le chapitre 1 en ligne", "en": "chapter 1 online"},
         etiquette={"fr": "Le podcast du chapitre", "en": "The chapter podcast"},
         accroche={"fr": "Quelques minutes pour poser ce que le chapitre va vous demander de décider : à écouter "
                         "avant de le lire.",
                   "en": "A few minutes to set out what the chapter will ask you to decide: listen before you "
                         "read it."},
         couvre={"fr": "Trois décisions à prendre avant d'écrire la première ligne, dans un ordre qui n'est pas "
                       "négociable : pour qui, pour quoi faire, autour de quoi. Le public d'abord, décrit par ses "
                       "prérequis réellement acquis, son temps disponible et ses contraintes matérielles ; puis les "
                       "objectifs, qui disent ce que l'apprenant sera capable de faire ; enfin le fil rouge, qui "
                       "répond à « à quoi cela va-t-il me servir ? » et sert d'arbitre quand il faut couper.",
                 "en": "Three decisions to make before writing a single line, in an order that is not negotiable: "
                       "for whom, to do what, around what. The audience first, described by the prerequisites "
                       "actually acquired, the time available and the practical constraints; then the objectives, "
                       "which state what the learner will be able to do; finally the through-line, which answers "
                       "“what will this be used for?” and acts as the arbiter when you must cut."},
         retenir={"fr": ["Un cours mal cadré se répare mal.",
                         "Le public d'abord : ses prérequis, son temps, ses contraintes matérielles.",
                         "Un objectif se prouve par un exercice : sinon, il est mal écrit.",
                         "Le fil rouge sert d'arbitre quand il faut couper.",
                         "Sauter le cadrage ne fait pas gagner de temps : cela le déplace vers la refonte."],
                  "en": ["A badly scoped course is hard to repair.",
                         "Audience first: its prerequisites, its time, its practical constraints.",
                         "An objective is proven by an exercise: otherwise, it is badly written.",
                         "The through-line acts as the arbiter when you must cut.",
                         "Skipping scoping does not save time: it moves the time to the rewrite."]}),
]

LIBELLES = {
    "fr": dict(
        episode="Épisode {n}", lecteur="Épisode {n} — {titre}",
        couvre="Ce que couvre l'épisode", retenir="À retenir", lire_avec="À lire avec l'épisode :",
        a_venir="Épisode à venir", voix_auteur="voix clonée de l'auteur",
        telecharger_mp3="Télécharger l'épisode (MP3, {poids})", telecharger_pdf="Télécharger le diaporama (PDF)",
        diapos="{n} diapositive{s} · {poids}",
        un="{n} épisode", plusieurs="{n} épisodes", vide="Aucun épisode pour l'instant",
        etat_aucun="{episodes} · bientôt en ligne", etat_partiel="{episodes} · {n} en ligne",
        etat_tous="{episodes} en ligne", etat_duree=" · {duree} d'écoute",
        renvoi_ecouter="Écouter l'épisode {n}", renvoi_voir="Voir la page Podcasts", renvoi_a_venir="à venir",
        mention_notebooklm="🤖 Voix générées par intelligence artificielle, avec NotebookLM, à partir du cours de "
                           "{auteur}.",
        mention_auteur="🤖 Voix clonée de {auteur}, générée par intelligence artificielle (ElevenLabs), à partir de "
                       "son cours.",
        mention_mixte="🤖 Voix générées par intelligence artificielle, à partir du cours de {auteur} : avec NotebookLM "
                      "et, pour {liste}, avec la voix clonée de l'auteur (ElevenLabs).",
        un_episode="l'épisode {n}", des_episodes="les épisodes {liste}", et="et"),
    "en": dict(
        episode="Episode {n}", lecteur="Episode {n} — {titre}",
        couvre="What the episode covers", retenir="Key takeaways", lire_avec="Read with the episode:",
        a_venir="Episode coming soon", voix_auteur="the author's cloned voice",
        telecharger_mp3="Download the episode (MP3, {poids})", telecharger_pdf="Download the slides (PDF)",
        diapos="{n} slide{s} · {poids}",
        un="{n} episode", plusieurs="{n} episodes", vide="No episodes yet",
        etat_aucun="{episodes} · coming soon", etat_partiel="{episodes} · {n} online",
        etat_tous="{episodes} online", etat_duree=" · {duree} of listening",
        renvoi_ecouter="Listen to episode {n}", renvoi_voir="See the Podcasts page", renvoi_a_venir="coming soon",
        mention_notebooklm="🤖 Voices generated by artificial intelligence, with NotebookLM, from the course by "
                           "{auteur}.",
        mention_auteur="🤖 The cloned voice of {auteur}, generated by artificial intelligence (ElevenLabs), from the "
                       "course.",
        mention_mixte="🤖 Voices generated by artificial intelligence, from the course by {auteur}: with NotebookLM "
                      "and, for {liste}, with the author's cloned voice (ElevenLabs).",
        un_episode="episode {n}", des_episodes="episodes {liste}", et="and"),
}

# Une balise de bloc : deux rendus qui en contiennent s'enveloppent dans des <div data-tr>, sinon des <span>.
BLOCS = re.compile(r"<(?:p|div|ul|ol|li|h[1-6]|nav|audio|section)\b", re.I)
# Le nom d'un fragment de la série : podcasts, podcasts-etat, podcasts-mention, podcast-N.
FRAGMENT = re.compile(r"podcasts(?:-(etat|mention))?$|podcast-(\d+)$")


# ── les textes ──────────────────────────────────────────────────────────────
def insecables(s):
    """Les espaces insécables du français : avant « : ; ? ! », à l'intérieur des guillemets, entre un nombre et son
    unité, après « chapitre », « épisode », « étape » suivis d'un numéro."""
    if not s:
        return s
    s = re.sub(r" ([:;?!»])", "\u00a0\\1", s)
    s = s.replace("« ", "«\u00a0")
    s = re.sub(r"(\d) (min|h|s|Mo|Ko|Go|%)(?![\w])", "\\1\u00a0\\2", s)
    return re.sub(r"\b([Cc]hapitre|[ÉéEe]pisode|[ÉéEe]tape)s? (\d)", lambda m: m.group(0).replace(" ", "\u00a0"), s)


def texte(ep, cle, lg):
    """Un texte de l'épisode dans la langue, espaces insécables posés en français."""
    s = (ep.get(cle) or {}).get(lg) or ""
    return insecables(s) if lg == "fr" else s


def retenir(ep, lg):
    return [insecables(r) if lg == "fr" else r for r in (ep.get("retenir") or {}).get(lg) or []]


def libelle(cle, lg, **valeurs):
    """Un libellé de la page ou des encadrés ; en français, un nombre reste attaché à ce qu'il compte."""
    s = LIBELLES[lg][cle].format(**valeurs)
    if lg != "fr":
        return s
    return re.sub(r"(\d) (diapositives?|épisodes?|en ligne)", "\\1\u00a0\\2", insecables(s))


def esc(s):
    """Un texte prêt pour le HTML, attributs entre guillemets compris ; l'espace insécable s'écrit &nbsp;, visible
    dans le source."""
    return html.escape(str(s), quote=True).replace("&#x27;", "'").replace("\u00a0", "&nbsp;")


def auteur():
    """L'auteur du cours, lu dans site/assets/js/course-data.js (author), d'un seul tenant."""
    try:
        src = io.open(os.path.join(SITE, "assets", "js", "course-data.js"), encoding="utf-8").read()
    except OSError:
        return ""
    m = re.search(r"\bauthor:\s*['\"]([^'\"]+)['\"]", src)
    return m.group(1).replace(" ", "\u00a0") if m else ""


def liste_nums(nums, lg):
    """« l'épisode 3 », « les épisodes 3, 5 et 7 » ; « episode 3 », « episodes 3, 5, and 7 »."""
    nums = [str(n) for n in nums]
    if len(nums) == 1:
        return libelle("un_episode", lg, n=nums[0])
    et = LIBELLES[lg]["et"]
    suite = (" %s " % et).join(nums) if len(nums) == 2 else \
        ", ".join(nums[:-1]) + ("," if lg == "en" else "") + " %s " % et + nums[-1]
    return libelle("des_episodes", lg, liste=suite)


def duree_texte(secondes, lg):
    """2 min, 1 h 02 (français) ; 2 min, 1 hr 2 min (anglais), insécables."""
    m = max(1, int(secondes / 60 + 0.5))
    if m < 60:
        return "%d\u00a0min" % m
    h, m = divmod(m, 60)
    if lg == "fr":
        return "%d\u00a0h\u00a0%02d" % (h, m)
    return "%d\u00a0hr" % h + (" %d\u00a0min" % m if m else "")


def poids_texte(octets, lg):
    """1,1 Mo (français) ; 1.1 MB (anglais)."""
    x = octets / 1048576
    t = ("%.1f" % x) if x < 100 else ("%.0f" % x)
    return t.replace(".", ",") + "\u00a0Mo" if lg == "fr" else t + "\u00a0MB"


# ── les fichiers publiés ────────────────────────────────────────────────────
def fichiers(ep, lg):
    """Les adresses publiées d'un épisode, depuis la racine du site : son MP3, son diaporama, ses diapositives."""
    nom = "%s.%s" % (ep["nom"], lg)
    return {"mp3": "%s/%s.mp3" % (MEDIA, nom), "pdf": "%s/%s.pdf" % (MEDIA, nom),
            "diapos": "%s/diaporamas/%s" % (MEDIA, nom)}


def chemin(rel):
    return os.path.join(SITE, *rel.split("/"))


def disponible(ep, lg):
    """Vrai si l'épisode est publié dans la langue : son MP3 est en place."""
    return os.path.isfile(chemin(fichiers(ep, lg)["mp3"]))


_DEBITS = {1: (0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320),
           2: (0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160)}
_FREQUENCES = {3: (44100, 48000, 32000), 2: (22050, 24000, 16000), 0: (11025, 12000, 8000)}


def duree_mp3(p):
    """La durée d'un MP3 en secondes, lue dans ses en-têtes : le nombre de trames de l'en-tête Xing, Info ou VBRI
    s'il y en a un, sinon la taille et le débit (débit constant). None si le fichier est illisible."""
    try:
        taille = os.path.getsize(p)
        with open(p, "rb") as f:
            tete, debut = f.read(10), 0
            if tete[:3] == b"ID3" and len(tete) == 10:
                debut = 10 + ((tete[6] & 0x7F) << 21 | (tete[7] & 0x7F) << 14 | (tete[8] & 0x7F) << 7 | (tete[9] & 0x7F))
                if tete[5] & 0x10:
                    debut += 10
            f.seek(debut)
            d = f.read(16384)
    except OSError:
        return None
    for i in range(len(d) - 4):
        if d[i] != 0xFF or d[i + 1] & 0xE0 != 0xE0:
            continue
        version, couche = (d[i + 1] >> 3) & 3, (d[i + 1] >> 1) & 3       # version 3 : MPEG-1 ; couche 1 : Layer III
        indice_debit, indice_freq = d[i + 2] >> 4, (d[i + 2] >> 2) & 3
        if version == 1 or couche != 1 or indice_debit in (0, 15) or indice_freq == 3:
            continue
        debit = _DEBITS[1 if version == 3 else 2][indice_debit] * 1000
        freq, mono = _FREQUENCES[version][indice_freq], d[i + 3] >> 6 == 3
        echantillons = 1152 if version == 3 else 576
        x = i + 4 + ((17 if mono else 32) if version == 3 else (9 if mono else 17))
        if d[x:x + 4] in (b"Xing", b"Info") and int.from_bytes(d[x + 4:x + 8], "big") & 1:
            return int.from_bytes(d[x + 8:x + 12], "big") * echantillons / freq
        if d[i + 36:i + 40] == b"VBRI":
            return int.from_bytes(d[i + 50:i + 54], "big") * echantillons / freq
        return (taille - debut - i) * 8 / debit
    return None


def taille_webp(p):
    """(largeur, hauteur) d'une image WebP, lues dans son en-tête ; None si illisible."""
    try:
        with open(p, "rb") as f:
            d = f.read(30)
    except OSError:
        return None
    if len(d) < 30 or d[:4] != b"RIFF" or d[8:12] != b"WEBP":
        return None
    if d[12:16] == b"VP8X":
        return 1 + int.from_bytes(d[24:27], "little"), 1 + int.from_bytes(d[27:30], "little")
    if d[12:16] == b"VP8 ":
        return int.from_bytes(d[26:28], "little") & 0x3FFF, int.from_bytes(d[28:30], "little") & 0x3FFF
    if d[12:16] == b"VP8L":
        b = int.from_bytes(d[21:25], "little")
        return (b & 0x3FFF) + 1, ((b >> 14) & 0x3FFF) + 1
    return None


def nom_image(sorte, i, n):
    """diapo-01.webp, vignette-12.webp : deux chiffres au moins (assets/js/podcasts.js suit la même règle)."""
    return "%s-%0*d.webp" % (sorte, max(2, len(str(n))), i)


def diaporama(ep, lg):
    """Le diaporama publié d'un épisode : n diapositives, dimensions de la première (grande, vignette), poids du PDF
    (None s'il n'est pas publié) ; None sans diapositives."""
    f = fichiers(ep, lg)
    dossier = chemin(f["diapos"])
    if not os.path.isdir(dossier):
        return None
    n = len([x for x in os.listdir(dossier) if re.match(r"diapo-\d+\.webp$", x)])
    if not n:
        return None
    pdf = chemin(f["pdf"])
    return dict(n=n, grande=taille_webp(os.path.join(dossier, nom_image("diapo", 1, n))),
                vignette=taille_webp(os.path.join(dossier, nom_image("vignette", 1, n))),
                pdf=os.path.getsize(pdf) if os.path.isfile(pdf) else None)


# ── le rendu ────────────────────────────────────────────────────────────────
def contexte(rel):
    """Les chemins d'une page, donnée depuis la racine du site (« chapitres/01-x.html », « en/podcasts.html ») :
    base, vers la racine des pages de sa langue ; racine, vers celle du site, où sont les médias."""
    profondeur = rel.count("/")
    racine = "../" * profondeur
    return {"base": "../" * (profondeur - 1) if rel.startswith("en/") else racine, "racine": racine}


def par_langue(rendu, langue):
    """rendu(lg) dans la langue de la page ; sur une page en blocs data-tr (« fr+en »), les deux, chacun dans son
    bloc — une seule fois s'ils se confondent."""
    if langue != "fr+en":
        return rendu(langue)
    fr, en = rendu("fr"), rendu("en")
    if fr == en:
        return fr
    b = "div" if BLOCS.search(fr + en) else "span"
    return '<%s data-tr="fr">%s</%s><%s data-tr="en">%s</%s>' % (b, fr, b, b, en, b)


def _medias(ep, lg, ctx):
    """Le lecteur d'un épisode et son état, ou « Épisode à venir » ; puis ses diapositives et son PDF."""
    n, f, racine = ep["num"], fichiers(ep, lg), ctx["racine"]
    titre = texte(ep, "titre", lg)
    l = []
    if disponible(ep, lg):
        p, src = chemin(f["mp3"]), racine + f["mp3"]
        d = duree_mp3(p)
        etat = (['<span class="pod-duree">⏱ %s</span>' % esc(duree_texte(d, lg))] if d else []) + \
            (['<span class="pod-voix">🎙️ %s</span>' % esc(libelle("voix_auteur", lg))] if ep["voix"] == "auteur" else []) + \
            ['<a class="pod-telecharger" href="%s" download>%s</a>' % (
                src, esc(libelle("telecharger_mp3", lg, poids=poids_texte(os.path.getsize(p), lg))))]
        l.append('<div class="pod-etat">%s</div>' % "".join(etat))
        l.append('<audio class="pod-lecteur" controls preload="none" src="%s" aria-label="%s"></audio>' % (
            src, esc(libelle("lecteur", lg, n=n, titre=titre))))
    else:
        l.append('<div class="pod-etat pod-etat-attente"><span class="pod-a-venir">⏳ %s</span></div>'
                 % esc(libelle("a_venir", lg)))
    d = diaporama(ep, lg)
    if d:
        attrs = 'data-dossier="%s%s/" data-nombre="%d"' % (racine, f["diapos"], d["n"])
        attrs += "".join(' data-%s="%dx%d"' % ((k,) + d[k]) for k in ("grande", "vignette") if d[k])
        l.append('<div class="pod-diapos" %s data-episode="%s"></div>' % (
            attrs, esc(libelle("lecteur", lg, n=n, titre=titre))))
        if d["pdf"] is not None:
            detail = libelle("diapos", lg, n=d["n"], s="s" if d["n"] > 1 else "", poids=poids_texte(d["pdf"], lg))
            l.append('<div class="pod-pdf"><a href="%s%s" download>📑 %s</a> <span class="pod-poids">%s</span></div>'
                     % (racine, f["pdf"], esc(libelle("telecharger_pdf", lg)), esc(detail)))
    return "\n".join(l)


def _textes(ep, lg, ctx):
    """Ce que couvre l'épisode, ce qu'il faut en retenir, et la page à lire avec lui."""
    l = ['<h3>%s</h3>' % esc(libelle("couvre", lg)),
         '<p>%s</p>' % esc(texte(ep, "couvre", lg)),
         '<h3>%s</h3>' % esc(libelle("retenir", lg)),
         '<ul class="pod-retenir">%s</ul>' % "".join("<li>%s</li>" % esc(r) for r in retenir(ep, lg))]
    if ep.get("page"):
        l.append('<p class="pod-liens">%s <a href="%s%s">%s</a></p>' % (
            esc(libelle("lire_avec", lg)), ctx["base"], esc(ep["page"]), esc(texte(ep, "page_nom", lg))))
    return "\n".join(l)


def section(ep, langue, ctx):
    """La section d'un épisode sur la page Podcasts ; son titre porte l'ancre episode-N, une seule fois même sur une
    page en blocs data-tr : c'est elle que visent les encadrés."""
    n = ep["num"]
    sommaire = {lg: "%d · %s" % (n, texte(ep, "court", lg)) for lg in LANGUES}
    attrs = ' data-sommaire-titre="%s"' % esc(sommaire["en" if langue == "en" else "fr"])
    if langue == "fr+en":
        attrs += ' data-sommaire-titre-en="%s"' % esc(sommaire["en"])
    titre = par_langue(lambda lg: esc(libelle("lecteur", lg, n=n, titre=texte(ep, "titre", lg))), langue)
    return "\n".join([
        '<section class="content-section pod-episode"%s>' % attrs,
        '<h2 id="episode-%d">%s</h2>' % (n, titre),
        '<div class="pod-media">%s</div>' % par_langue(lambda lg: _medias(ep, lg, ctx), langue),
        '<div class="pod-texte">%s</div>' % par_langue(lambda lg: _textes(ep, lg, ctx), langue),
        '</section>'])


def liste(langue, ctx):
    """La liste des épisodes de la page Podcasts, ou une ligne qui dit qu'il n'y en a pas encore."""
    if not EPISODES:
        return '<p class="pod-aucun">%s</p>' % par_langue(lambda lg: esc(libelle("vide", lg)) + ".", langue)
    return "\n".join(section(ep, langue, ctx) for ep in sorted(EPISODES, key=lambda e: e["num"]))


def etat(lg):
    """La ligne d'état de l'en-tête de la page : « 1 épisode en ligne · 2 min d'écoute »."""
    total = len(EPISODES)
    if not total:
        return esc(libelle("vide", lg))
    publies = [ep for ep in EPISODES if disponible(ep, lg)]
    nb = libelle("un" if total == 1 else "plusieurs", lg, n=total)
    if not publies:
        s = libelle("etat_aucun", lg, episodes=nb)
    elif len(publies) == total:
        s = libelle("etat_tous", lg, episodes=nb)
    else:
        s = libelle("etat_partiel", lg, episodes=nb, n=len(publies))
    durees = [duree_mp3(chemin(fichiers(ep, lg)["mp3"])) for ep in publies]
    if publies and all(durees):
        s += libelle("etat_duree", lg, duree=duree_texte(sum(durees), lg))
    return esc(s)


def mention(lg):
    """La mention des voix générées par intelligence artificielle, au pied de la page."""
    if not EPISODES:
        return ""
    par_auteur = sorted(ep["num"] for ep in EPISODES if ep["voix"] == "auteur")
    if not par_auteur:
        m = libelle("mention_notebooklm", lg, auteur=auteur())
    elif len(par_auteur) == len(EPISODES):
        m = libelle("mention_auteur", lg, auteur=auteur())
    else:
        m = libelle("mention_mixte", lg, auteur=auteur(), liste=liste_nums(par_auteur, lg))
    return '<p class="pod-mention">%s</p>' % esc(m)


def renvoi(num, lg, ctx):
    """L'encadré qui mène d'une page du cours à son épisode, sur la page Podcasts : son étiquette, le titre de
    l'épisode, sa phrase, et le lien — « Écouter l'épisode N » s'il est publié, « Voir la page Podcasts » et la marque
    « à venir » sinon. C'est un <nav> : un renvoi, que la fenêtre « Où en parle-t-on ? » du glossaire ne compte pas.
    KeyError si l'épisode n'existe pas ou n'a pas de page du cours."""
    ep = next((e for e in EPISODES if e["num"] == num), None)
    if ep is None or not ep.get("page"):
        raise KeyError("épisode %d absent de outils/podcasts.py, ou sans page du cours" % num)
    dispo = disponible(ep, lg)
    etiquette = esc(texte(ep, "etiquette", lg))
    lien = libelle("renvoi_ecouter", lg, n=num) if dispo else libelle("renvoi_voir", lg)
    marque = "" if dispo else '<span class="pod-renvoi-a-venir">%s</span>' % esc(libelle("renvoi_a_venir", lg))
    return ('<nav class="pod-renvoi%s" aria-label="%s"><span class="pod-renvoi-ico" aria-hidden="true">🎙️</span>'
            '<span class="pod-renvoi-corps"><span class="pod-renvoi-etiquette">%s</span>'
            '<span class="pod-renvoi-titre">%s</span><span class="pod-renvoi-texte">%s</span></span>'
            '<span class="pod-renvoi-action">%s<a class="pod-renvoi-lien" href="%spodcasts.html#episode-%d">%s'
            '<span aria-hidden="true"> →</span></a></span></nav>') % (
        "" if dispo else " pod-renvoi-attente", etiquette, etiquette,
        esc(libelle("lecteur", lg, n=num, titre=texte(ep, "titre", lg))), esc(texte(ep, "accroche", lg)),
        marque, ctx["base"], num, esc(lien))


def rendre(nom, langue, rel):
    """Le contenu d'un fragment de la série pour la page rel (depuis la racine du site), ou None si nom n'en est pas
    un. langue : fr, en, ou « fr+en » pour la liste sur une page en blocs data-tr. KeyError : épisode inconnu."""
    m = FRAGMENT.match(nom)
    if not m:
        return None
    ctx = contexte(rel)
    if m.group(2):
        return renvoi(int(m.group(2)), langue, ctx)
    if m.group(1) == "etat":
        return etat(langue)
    if m.group(1) == "mention":
        return mention(langue)
    return "\n" + liste(langue, ctx) + "\n"


# ── le contrôle ─────────────────────────────────────────────────────────────
def controler():
    """[message] pour chaque défaut de la source."""
    out, vus = [], set()
    for ep in EPISODES:
        n = ep.get("num")
        if not isinstance(n, int) or n in vus:
            out.append("épisode %r : numéro absent ou en double" % (n,))
        vus.add(n)
        if not re.match(r"[a-z0-9][a-z0-9-]*$", ep.get("nom") or ""):
            out.append("épisode %s : nom de fichier « %s » invalide (minuscules, chiffres, tirets)" % (n, ep.get("nom")))
        if ep.get("voix") not in VOIX:
            out.append("épisode %s : voix « %s » inconnue (%s)" % (n, ep.get("voix"), ", ".join(VOIX)))
        cles = ("titre", "court", "couvre", "retenir") + (("page_nom", "etiquette", "accroche") if ep.get("page") else ())
        for cle in cles:
            for lg in LANGUES:
                if not (ep.get(cle) or {}).get(lg):
                    out.append("épisode %s : %s[%s] manque" % (n, cle, lg))
        r = ep.get("retenir") or {}
        if len(r.get("fr") or []) != len(r.get("en") or []):
            out.append("épisode %s : pas autant de points à retenir en français qu'en anglais" % n)
        if ep.get("page") and not os.path.isfile(chemin(ep["page"])):
            out.append("épisode %s : page %s introuvable" % (n, ep["page"]))
    return out


def places_manquantes():
    """[message] pour chaque marqueur absent ou répété : la liste des épisodes sur la page Podcasts (fragment
    podcasts), l'encadré de chaque épisode sur sa page du cours (fragment podcast-N) — dans chaque langue où la page
    existe, sa jumelle anglaise (en/…) comprise sur un site miroir."""
    out = []
    places = [(rel, "podcasts", "la liste des épisodes") for rel in ("podcasts.html", "en/podcasts.html")]
    for ep in EPISODES:
        if ep.get("page"):
            places += [(rel, "podcast-%d" % ep["num"], "l'encadré de l'épisode %d" % ep["num"])
                       for rel in (ep["page"], "en/" + ep["page"])]
    for rel, nom, quoi in places:
        if not os.path.isfile(chemin(rel)):
            continue
        n = io.open(chemin(rel), encoding="utf-8").read().count("<!-- FRAGMENT:%s -->" % nom)
        if n != 1:
            out.append("site/%s : %s %s — <!-- FRAGMENT:%s --><!-- /FRAGMENT:%s -->%s, puis python3 "
                       "outils/generer_fragments.py" % (rel, quoi, "manque" if not n else "se répète", nom, nom,
                                                       "" if nom == "podcasts" else " à la fin de son en-tête"))
    return out


def main():
    for flux in (sys.stdout, sys.stderr):
        try:
            flux.reconfigure(encoding="utf-8")
        except Exception:
            pass
    defauts = controler() + places_manquantes()
    for ep in sorted(EPISODES, key=lambda e: e.get("num") or 0):
        etats = []
        for lg in LANGUES:
            if disponible(ep, lg):
                d = duree_mp3(chemin(fichiers(ep, lg)["mp3"]))
                diapos = diaporama(ep, lg)
                etats.append("%s en ligne%s%s" % (lg, " (%s)" % duree_texte(d, "fr").replace("\u00a0", " ") if d else "",
                                                  ", %d diapositives" % diapos["n"] if diapos else ""))
            else:
                etats.append("%s à venir" % lg)
        print("  épisode %s — %s : %s" % (ep.get("num"), texte(ep, "titre", "fr").replace("\u00a0", " "),
                                          " ; ".join(etats)))
    for d in defauts:
        print("  ✗", d)
    print("%d épisode(s), %d défaut(s)." % (len(EPISODES), len(defauts)))
    return 1 if defauts else 0


if __name__ == "__main__":
    sys.exit(main())
