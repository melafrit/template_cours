# -*- coding: utf-8 -*-
"""L'export du polycopié par Microsoft Word (Windows, pywin32).

  1. Word ouvre le document que python-docx a écrit, en mode Page ;
  2. tous les champs sont mis à jour, deux fois (la table des matières occupe ses pages, puis les numéros se
     recalent) : table des matières, PAGEREF du mini-sommaire, STYLEREF des en-têtes, index ; puis la pagination ;
  3. un schéma large qui ouvre une page alors que la précédente s'arrête tôt, faute de place pour lui, est réduit
     juste assez pour y tenir (jamais sous 70 % de sa largeur) ;
  4. la marge est rangée page par page : chaque zone garde la place la plus proche de la ligne de son ancre où elle
     ne déborde pas de la zone de texte et ne chevauche ni une autre zone, ni un schéma large et sa légende ; Word la
     fixe alors par rapport à la page ;
  5. le Word est enregistré (champs à jour : l'auteur l'ouvre sans rien recalculer), puis le PDF est exporté avec
     ses signets (titres) et ses balises d'accessibilité ; enfin la langue du PDF (/Lang) est posée.

Un seul export par Word à la fois sur le poste : le verrou (création exclusive) est pris avant d'ouvrir Word et
supprimé ensuite, même en cas d'erreur.
"""
import os
import time

POINTS_CM = 72 / 2.54
WD_PAGE = 3                   # Information : numéro de la page
WD_HAUT_PAGE = 6              # Information : position verticale depuis le haut de la page (points)
REL_PAGE = 1                  # RelativeVerticalPosition : la page
REL_PARAGRAPHE = 2
REL_LIGNE = 3                 # … la ligne de l'ancre
LEGENDE = 27                  # la légende d'un schéma large, sous lui (une ligne et ses espaces), en points
REDUCTION_MINI = 0.70


def prendre_verrou(verrou, attente=5, limite=3600):
    """Attend que le verrou soit libre, puis le crée (création exclusive) : un seul export par Word à la fois."""
    os.makedirs(os.path.dirname(os.path.abspath(verrou)), exist_ok=True)
    debut = time.time()
    while True:
        try:
            os.close(os.open(verrou, os.O_CREAT | os.O_EXCL | os.O_WRONLY))
            return
        except FileExistsError:
            if time.time() - debut > limite:
                raise SystemExit(f"Verrou toujours pris après {limite // 60} min : {verrou}")
            print(f"  · Word est occupé (verrou {os.path.basename(verrou)}) : nouvel essai dans {attente} s")
            time.sleep(attente)


def exporter(docx, pdf, verrou=None, journal=print, largeur_texte_cm=13.6):
    """Met à jour les champs, ajuste les schémas, range la marge, enregistre le Word et exporte le PDF. Rend un
    compte rendu."""
    docx, pdf = os.path.abspath(docx), os.path.abspath(pdf)
    if verrou:
        prendre_verrou(verrou)
    compte = {}
    try:
        try:
            import pythoncom
            import win32com.client as w32
        except ImportError:
            raise SystemExit("L'export par Word demande Windows, Microsoft Word et pywin32 : relancez avec --sans-pdf "
                             "pour le Word seul.")
        pythoncom.CoInitialize()
        word = w32.DispatchEx("Word.Application")
        word.Visible = False
        word.DisplayAlerts = 0
        try:
            doc = word.Documents.Open(docx, ReadOnly=False, AddToRecentFiles=False, Visible=False)
            try:
                doc.ActiveWindow.View.Type = 3              # wdPrintView : les positions de la page
            except Exception:
                pass
            mettre_a_jour(doc)
            compte["figures"] = ajuster_figures(doc, largeur_texte_cm, journal)
            if compte["figures"]:
                mettre_a_jour(doc)
            compte["marge"] = ajuster_marge(doc, largeur_texte_cm, journal)
            mettre_a_jour(doc, legere=True)
            compte["pages"] = doc.ComputeStatistics(2)       # wdStatisticPages
            compte["champs"] = doc.Fields.Count
            doc.Save()
            doc.ExportAsFixedFormat(OutputFileName=pdf, ExportFormat=17, OpenAfterExport=False, OptimizeFor=0,
                                    Range=0, Item=0, IncludeDocProps=True, KeepIRM=True, CreateBookmarks=1,
                                    DocStructureTags=True, BitmapMissingFonts=True, UseISO19005_1=False)
            doc.Close(False)
        finally:
            word.Quit()
    finally:
        if verrou:
            try:
                os.remove(verrou)
            except FileNotFoundError:
                pass
    return compte


def _histoires(doc):
    """Toutes les « histoires » du document : corps, en-têtes, pieds, zones de texte."""
    for rng in doc.StoryRanges:
        while rng is not None:
            yield rng
            try:
                rng = rng.NextStoryRange
            except Exception:
                rng = None


def mettre_a_jour(doc, legere=False):
    for _ in range(1 if legere else 2):
        for rng in _histoires(doc):
            try:
                rng.Fields.Update()
            except Exception:
                pass
        for t in doc.TablesOfContents:
            t.Update()
        for x in doc.Indexes:
            x.Update()
        doc.Repaginate()
    for t in doc.TablesOfContents:
        t.UpdatePageNumbers()
    doc.Fields.Update()


def _larges(doc, largeur_texte_cm):
    seuil = largeur_texte_cm * POINTS_CM + 20
    out = []
    for ish in doc.InlineShapes:
        try:
            if ish.Width > seuil:
                out.append(ish)
        except Exception:
            continue
    return out


def ajuster_figures(doc, largeur_texte_cm, journal=print):
    """Un schéma large qui ouvre une page quand la précédente s'arrête tôt faute de place : Word le réduit juste
    assez (voir l'en-tête du module). Rend la liste des retouches."""
    texte_pt = largeur_texte_cm * POINTS_CM
    retouches = []
    for ish in _larges(doc, largeur_texte_cm):
        try:
            if not (ish.Title or "").startswith("poly:schema"):
                continue
            rng = ish.Range
            para = rng.Paragraphs(1)
            page = rng.Information(WD_PAGE)
            sec = rng.Sections(1).PageSetup
            if rng.Information(WD_HAUT_PAGE) > sec.TopMargin + para.SpaceBefore + 24:
                continue                                     # le schéma n'ouvre pas sa page
            prec = para.Previous(1)
            if prec is None or prec.Range.Information(WD_PAGE) != page - 1:
                continue
            fin = prec.Range.Duplicate
            fin.MoveEnd(1, -1)                               # sans la marque de paragraphe (wdCharacter)
            fin.Collapse(0)                                  # wdCollapseEnd : le dernier caractère
            if fin.Information(WD_PAGE) != page - 1:
                continue
            bas = fin.Information(WD_HAUT_PAGE) + max(15.0, prec.LineSpacing) + prec.SpaceAfter
            libre = sec.PageHeight - sec.BottomMargin - bas - para.SpaceBefore - LEGENDE - 6
            echelle = libre / ish.Height
            if echelle >= 1:
                continue
            if echelle < REDUCTION_MINI:
                retouches.append(f"page {page} : schéma gardé entier ({echelle:.0%} de sa largeur aurait été nécessaire)")
                continue
            largeur = ish.Width * echelle
            ish.LockAspectRatio = -1
            ish.Width = largeur
            debord = max(0.0, largeur - texte_pt)
            para.RightIndent = -debord                       # retrait extérieur (retraits en miroir)
            suivant = para.Next(1)
            if suivant is not None:
                suivant.RightIndent = -debord                # la légende, à la même largeur
            doc.Repaginate()
            retouches.append(f"page {page} : schéma réduit à {echelle:.0%} pour tenir en page {page - 1}")
        except Exception as e:                               # une figure qui résiste ne bloque pas l'export
            retouches.append(f"schéma non ajusté ({e.__class__.__name__})")
    for r in retouches:
        journal("  · figure, " + r)
    return retouches


def _chevauche(a1, a2, blocs, ecart):
    return any(a1 < b2 + ecart and a2 > b1 - ecart for b1, b2 in blocs)


def ajuster_marge(doc, largeur_texte_cm, journal=print, ecart=4.0):
    """Range les zones de la marge, page par page (voir l'en-tête du module). Rend la liste des retouches."""
    zones, obstacles = {}, {}
    for s in doc.Shapes:
        if not s.Name.startswith("Marge"):
            continue
        a = s.Anchor
        page = a.Information(WD_PAGE)
        sec = a.Sections(1).PageSetup
        relatif = s.RelativeVerticalPosition
        if relatif == REL_LIGNE:
            haut = a.Information(WD_HAUT_PAGE) + s.Top
        elif relatif == REL_PARAGRAPHE:
            debut = a.Paragraphs(1).Range.Duplicate
            debut.Collapse(1)                                # wdCollapseStart
            haut = debut.Information(WD_HAUT_PAGE) + s.Top
        else:
            haut = s.Top
        zones.setdefault(page, []).append(dict(forme=s, haut=haut, h=s.Height,
                                                limite=sec.PageHeight - sec.BottomMargin, sommet=sec.TopMargin))
    # Les schémas larges et leur légende débordent dans la marge : des obstacles.
    for ish in _larges(doc, largeur_texte_cm):
        try:
            rng = ish.Range
            page = rng.Information(WD_PAGE)
            haut = rng.Information(WD_HAUT_PAGE)
            obstacles.setdefault(page, []).append((haut, haut + ish.Height + LEGENDE))
        except Exception:
            continue
    retouches = []
    for page, liste in zones.items():
        liste.sort(key=lambda z: z["haut"])
        poses = []
        for z in liste:
            blocs = obstacles.get(page, []) + poses
            voulu, h = z["haut"], z["h"]
            candidats = ([voulu, z["limite"] - h, z["sommet"]] + [b2 + ecart for _, b2 in blocs]
                         + [b1 - ecart - h for b1, _ in blocs])
            valables = [c for c in candidats if c >= z["sommet"] and c + h <= z["limite"]
                        and not _chevauche(c, c + h, blocs, ecart - 0.5)]
            if valables:
                choix = min(valables, key=lambda c: abs(c - voulu))
            else:
                choix = min(max(voulu, z["sommet"]), z["limite"] - h)
            poses.append((choix, choix + h))
            if abs(choix - voulu) > 0.5:
                f = z["forme"]
                f.RelativeVerticalPosition = REL_PAGE
                f.Top = choix
                retouches.append(f"page {page} : « {f.Name} » {voulu:.0f} → {choix:.0f} pt")
    for r in retouches:
        journal("  · marge, " + r)
    return retouches


def fixer_langue(pdf, langue):
    """Pose /Lang (fr-FR, en-US) dans le catalogue du PDF : Word écrit « en » même pour un document français. Une mise
    à jour incrémentale : seul l'objet catalogue est réécrit. Rend True si le PDF a changé."""
    import fitz
    with fitz.open(pdf) as d:
        catalogue = d.pdf_catalog()
        if d.xref_get_key(catalogue, "Lang") == ("string", langue):
            return False
        d.xref_set_key(catalogue, "Lang", fitz.get_pdf_str(langue))
        d.saveIncr()
    with fitz.open(pdf) as d:
        lu = d.xref_get_key(d.pdf_catalog(), "Lang")
    if lu != ("string", langue):
        raise SystemExit(f"Langue du PDF non fixée : {pdf} porte {lu[1]!r}, {langue!r} attendue")
    return True
