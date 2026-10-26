# -*- coding: utf-8 -*-
"""Les briques Word que python-docx ne fournit pas.

Champs (TOC, TC, PAGEREF, STYLEREF, PAGE, XE, INDEX), signets, bordures et trames de paragraphe et de cellule,
images en ligne, image ancrée à la page (garde), et la pièce maîtresse de la marge : une zone de texte ancrée sur la
ligne qu'elle sert, centrée dans la marge extérieure (wp:anchor, positionH relativeFrom="outsideMargin",
positionV relativeFrom="line"), qui porte un QR code et sa légende. Word la place à droite sur une page
impaire, à gauche sur une page paire ; allowOverlap="0" lui interdit de chevaucher sa voisine.

Les éléments s'insèrent dans l'ordre que fixe le schéma (ORDRES) : Word refuse parfois un document dont les
propriétés sont dans le désordre.

LES LIENS. Un QR code et sa légende mènent, d'un clic dans le PDF, à l'adresse que porte le QR code, sans que rien ne
change à l'impression : ni bleu, ni soulignement (les runs gardent leur mise en forme, jamais le style
« Hyperlink »), aucune adresse écrite. L'image reçoit un a:hlinkClick (dans wp:docPr et pic:cNvPr) — seul moyen,
dans une zone de texte, que Word exporte son lien — et son run, comme le texte de la légende, va dans un
w:hyperlink (lien_xml pour du XML de runs, lier pour les runs d'un paragraphe). La relation (externe) est celle que
rend doc.part.relate_to(url, RT.HYPERLINK, is_external=True) : une seule par adresse. Un champ (PAGEREF, XE…), une
zone ancrée ou un signet restent hors du lien : un renvoi « (p. n) » demeure un lien interne.
"""
from xml.sax.saxutils import escape

from docx.oxml import parse_xml
from docx.oxml.ns import qn

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "pic": "http://schemas.openxmlformats.org/drawingml/2006/picture",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "wps": "http://schemas.microsoft.com/office/word/2010/wordprocessingShape",
    "wp14": "http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing",
    "w14": "http://schemas.microsoft.com/office/word/2010/wordml",
}
DECL = " ".join(f'xmlns:{k}="{v}"' for k, v in NS.items())
EMU_CM = 360000


def emu(cm):
    return int(round(cm * EMU_CM))


def twips(cm):
    """Centimètres → vingtièmes de point (dxa)."""
    return int(round(cm * 1440 / 2.54))


def esc(texte):
    return escape(texte or "", {'"': "&quot;"})


def xml(fragment):
    """Un fragment XML (balises w:, wp:, a:…) → élément lxml, les espaces de noms déclarés."""
    fragment = fragment.strip()
    i = fragment.index(" ") if " " in fragment.split(">")[0] else fragment.index(">")
    if fragment[i - 1] == "/":
        i -= 1
    return parse_xml(fragment[:i] + " " + DECL + fragment[i:])


# ── l'ordre des enfants (schéma WordprocessingML) ──────────────────────────
ORDRES = {
    "pPr": ["pStyle", "keepNext", "keepLines", "pageBreakBefore", "framePr", "widowControl", "numPr",
            "suppressLineNumbers", "pBdr", "shd", "tabs", "suppressAutoHyphens", "kinsoku", "wordWrap",
            "overflowPunct", "topLinePunct", "autoSpaceDE", "autoSpaceDN", "bidi", "adjustRightInd", "snapToGrid",
            "spacing", "ind", "contextualSpacing", "mirrorIndents", "suppressOverlap", "jc", "textDirection",
            "textAlignment", "textboxTightWrap", "outlineLvl", "divId", "cnfStyle", "rPr", "sectPr", "pPrChange"],
    "rPr": ["rStyle", "rFonts", "b", "bCs", "i", "iCs", "caps", "smallCaps", "strike", "dstrike", "outline",
            "shadow", "emboss", "imprint", "noProof", "snapToGrid", "vanish", "webHidden", "color", "spacing", "w",
            "kern", "position", "sz", "szCs", "highlight", "u", "effect", "bdr", "shd", "fitText", "vertAlign",
            "rtl", "cs", "em", "lang", "eastAsianLayout", "specVanish", "oMath"],
    "tcPr": ["cnfStyle", "tcW", "gridSpan", "hMerge", "vMerge", "tcBorders", "shd", "noWrap", "tcMar",
             "textDirection", "tcFitText", "vAlign", "hideMark"],
    "tblPr": ["tblStyle", "tblpPr", "tblOverlap", "bidiVisual", "tblStyleRowBandSize", "tblStyleColBandSize",
              "tblW", "jc", "tblCellSpacing", "tblInd", "tblBorders", "shd", "tblLayout", "tblCellMar", "tblLook",
              "tblCaption", "tblDescription"],
    "trPr": ["cnfStyle", "divId", "gridBefore", "gridAfter", "wBefore", "wAfter", "cantSplit", "trHeight",
             "tblHeader", "tblCellSpacing", "jc", "hidden"],
    "sectPr": ["headerReference", "footerReference", "footnotePr", "endnotePr", "type", "pgSz", "pgMar",
               "paperSrc", "pgBorders", "lnNumType", "pgNumType", "cols", "formProt", "vAlign", "noEndnote",
               "titlePg", "textDirection", "bidi", "rtlGutter", "docGrid", "printerSettings", "sectPrChange"],
    "settings": ["writeProtection", "view", "zoom", "removePersonalInformation", "removeDateAndTime",
                 "doNotDisplayPageBoundaries", "displayBackgroundShape", "printPostScriptOverText",
                 "printFractionalCharacterWidth", "printFormsData", "embedTrueTypeFonts", "embedSystemFonts",
                 "saveSubsetFonts", "saveFormsData", "mirrorMargins", "alignBordersAndEdges",
                 "bordersDoNotSurroundHeader", "bordersDoNotSurroundFooter", "gutterAtTop", "hideSpellingErrors",
                 "hideGrammaticalErrors", "activeWritingStyle", "proofState", "formsDesign", "attachedTemplate",
                 "linkStyles", "stylePaneFormatFilter", "stylePaneSortMethod", "documentType", "mailMerge",
                 "revisionView", "trackRevisions", "doNotTrackMoves", "doNotTrackFormatting", "documentProtection",
                 "autoFormatOverride", "styleLockTheme", "styleLockQFSet", "defaultTabStop", "autoHyphenation",
                 "consecutiveHyphenLimit", "hyphenationZone", "doNotHyphenateCaps", "showEnvelope",
                 "summaryLength", "clickAndTypeStyle", "defaultTableStyle", "evenAndOddHeaders",
                 "bookFoldRevPrinting", "bookFoldPrinting", "bookFoldPrintingSheets",
                 "drawingGridHorizontalSpacing", "drawingGridVerticalSpacing", "displayHorizontalDrawingGridEvery",
                 "displayVerticalDrawingGridEvery", "doNotUseMarginsForDrawingGridOrigin",
                 "drawingGridHorizontalOrigin", "drawingGridVerticalOrigin", "doNotShadeFormData",
                 "noPunctuationKerning", "characterSpacingControl", "printTwoOnOne", "strictFirstAndLastChars",
                 "noLineBreaksAfter", "noLineBreaksBefore", "savePreviewPicture", "doNotValidateAgainstSchema",
                 "saveInvalidXml", "ignoreMixedContent", "alwaysShowPlaceholderText", "doNotDemarcateInvalidXml",
                 "saveXmlDataOnly", "useXSLTWhenSaving", "saveThroughXslt", "showXMLTags",
                 "alwaysMergeEmptyNamespace", "updateFields", "hdrShapeDefaults", "footnotePr", "endnotePr",
                 "compat", "docVars", "rsids", "mathPr", "attachedSchema", "themeFontLang", "clrSchemeMapping",
                 "doNotIncludeSubdocsInStats", "doNotAutoCompressPictures", "forceUpgrade", "captions",
                 "readModeInkLockDown", "smartTagType", "schemaLibrary", "shapeDefaults", "doNotEmbedSmartTags",
                 "decimalSymbol", "listSeparator"],
}


def _nom_local(el):
    return el.tag.split("}")[-1]


def poser(parent, enfant, ordre=None):
    """Place enfant dans parent à sa place dans le schéma ; remplace un enfant de même nom (w: seulement)."""
    ordre = ordre or ORDRES[_nom_local(parent)]
    nom = _nom_local(enfant)
    for ancien in parent.findall(qn("w:" + nom)) if enfant.tag.startswith("{" + NS["w"]) else []:
        parent.remove(ancien)
    rang = ordre.index(nom) if nom in ordre else len(ordre)
    for i, el in enumerate(parent):
        n = _nom_local(el)
        if n in ordre and ordre.index(n) > rang:
            parent.insert(i, enfant)
            return enfant
    parent.append(enfant)
    return enfant


def ppr(paragraphe):
    """Le w:pPr d'un paragraphe python-docx (ou d'un élément w:p)."""
    p = getattr(paragraphe, "_p", paragraphe)
    return p.get_or_add_pPr()


# ── propriétés de paragraphe ───────────────────────────────────────────────
def filet(val="single", sz=4, space=4, color="1B3A5B"):
    """Une bordure : sz en huitièmes de point, space en points."""
    return dict(val=val, sz=sz, space=space, color=color)


def bordures_paragraphe(paragraphe, **cotes):
    """Bordures de paragraphe : top, left, bottom, right, between = filet(...)."""
    pbdr = xml("<w:pBdr/>")
    for cote in ("top", "left", "bottom", "right", "between"):
        f = cotes.get(cote)
        if f:
            pbdr.append(xml(f'<w:{cote} w:val="{f["val"]}" w:sz="{f["sz"]}" w:space="{f["space"]}" '
                            f'w:color="{f["color"]}"/>'))
    poser(ppr(paragraphe), pbdr)


def trame_paragraphe(paragraphe, fond):
    poser(ppr(paragraphe), xml(f'<w:shd w:val="clear" w:color="auto" w:fill="{fond}"/>'))


def retrait_miroir(paragraphe):
    """Les retraits gauche et droit deviennent intérieur et extérieur : un retrait négatif « extérieur » fait
    déborder le paragraphe dans la grande marge, à droite des pages impaires, à gauche des pages paires."""
    poser(ppr(paragraphe), xml("<w:mirrorIndents/>"))


def niveau_plan(paragraphe, niveau):
    poser(ppr(paragraphe), xml(f'<w:outlineLvl w:val="{niveau}"/>'))


def sans_coupure(paragraphe):
    poser(ppr(paragraphe), xml("<w:suppressAutoHyphens/>"))


def tabulation(paragraphe, position_cm, alignement="right", points=False):
    tabs = xml("<w:tabs/>")
    leader = ' w:leader="dot"' if points else ""
    tabs.append(xml(f'<w:tab w:val="{alignement}"{leader} w:pos="{twips(position_cm)}"/>'))
    poser(ppr(paragraphe), tabs)


# ── propriétés de caractère (XML de w:rPr, pour les zones de texte et les champs) ──
def rpr_xml(police=None, taille=None, gras=False, italique=False, couleur=None, espacement=None, position=None,
            masque=False, langue=None):
    """Le XML d'un w:rPr : taille en points, espacement (interlettrage) en points, position en points."""
    e = []
    if police:
        e.append(f'<w:rFonts w:ascii="{police}" w:hAnsi="{police}" w:cs="{police}" w:eastAsia="{police}"/>')
    if gras:
        e.append("<w:b/><w:bCs/>")
    if italique:
        e.append("<w:i/><w:iCs/>")
    if masque:
        e.append("<w:vanish/>")
    if couleur:
        e.append(f'<w:color w:val="{couleur}"/>')
    if espacement:
        e.append(f'<w:spacing w:val="{int(round(espacement * 20))}"/>')
    if position:
        e.append(f'<w:position w:val="{int(round(position * 2))}"/>')
    if taille:
        e.append(f'<w:sz w:val="{int(round(taille * 2))}"/><w:szCs w:val="{int(round(taille * 2))}"/>')
    if langue:
        e.append(f'<w:lang w:val="{langue}"/>')
    return "<w:rPr>" + "".join(e) + "</w:rPr>" if e else ""


def run_xml(texte, rpr=""):
    morceaux = []
    for i, ligne in enumerate((texte or "").split("\n")):
        if i:
            morceaux.append("<w:br/>")
        if ligne:
            morceaux.append(f'<w:t xml:space="preserve">{esc(ligne)}</w:t>')
    return f"<w:r>{rpr}{''.join(morceaux)}</w:r>"


def para_xml(runs, jc=None, avant=0, apres=0, interligne=None, style=None, retrait_g=None, retrait_d=None,
             garder=False):
    """Le XML d'un paragraphe (pour l'intérieur d'une zone de texte) : interligne exact en points."""
    p = []
    if style:
        p.append(f'<w:pStyle w:val="{style}"/>')
    if garder:
        p.append("<w:keepNext/>")
    p.append("<w:suppressAutoHyphens/>")
    ligne = f' w:line="{int(round(interligne * 20))}" w:lineRule="exact"' if interligne else ""
    p.append(f'<w:spacing w:before="{int(avant * 20)}" w:after="{int(apres * 20)}"{ligne}/>')
    if retrait_g is not None or retrait_d is not None:
        p.append(f'<w:ind w:left="{twips(retrait_g or 0)}" w:right="{twips(retrait_d or 0)}"/>')
    if jc:
        p.append(f'<w:jc w:val="{jc}"/>')
    return "<w:p><w:pPr>" + "".join(p) + "</w:pPr>" + "".join(runs) + "</w:p>"


# ── champs ─────────────────────────────────────────────────────────────────
def champ_xml(instruction, resultat="", rpr=""):
    """Les runs d'un champ complexe ; resultat : le texte affiché avant la mise à jour par Word."""
    runs = [f'<w:r>{rpr}<w:fldChar w:fldCharType="begin"/></w:r>',
            f'<w:r>{rpr}<w:instrText xml:space="preserve"> {esc(instruction)} </w:instrText></w:r>']
    if resultat is not None:
        runs.append(f'<w:r>{rpr}<w:fldChar w:fldCharType="separate"/></w:r>')
        if resultat:
            runs.append(run_xml(resultat, rpr))
    runs.append(f'<w:r>{rpr}<w:fldChar w:fldCharType="end"/></w:r>')
    return runs


def ajouter_champ(paragraphe, instruction, resultat="", rpr=""):
    """Ajoute un champ en fin de paragraphe (python-docx ou w:p)."""
    p = getattr(paragraphe, "_p", paragraphe)
    for r in champ_xml(instruction, resultat, rpr):
        p.append(xml(r))


def guillemets_champ(texte):
    """Un texte entre guillemets droits dans une instruction de champ (TC, XE)."""
    return '"' + (texte or "").replace('"', '\\"') + '"'


# ── signets ────────────────────────────────────────────────────────────────
def signet(paragraphe, nom, ident):
    """Un signet qui entoure tout le contenu du paragraphe (cible des champs PAGEREF)."""
    p = getattr(paragraphe, "_p", paragraphe)
    debut = xml(f'<w:bookmarkStart w:id="{ident}" w:name="{nom}"/>')
    pp = p.find(qn("w:pPr"))
    if pp is not None:
        pp.addnext(debut)
    else:
        p.insert(0, debut)
    p.append(xml(f'<w:bookmarkEnd w:id="{ident}"/>'))


# ── cellules et tableaux ───────────────────────────────────────────────────
def _tcpr(cellule):
    return cellule._tc.get_or_add_tcPr()


def trame_cellule(cellule, fond):
    poser(_tcpr(cellule), xml(f'<w:shd w:val="clear" w:color="auto" w:fill="{fond}"/>'))


def bordures_cellule(cellule, **cotes):
    """Bordures de cellule : top, left (start), bottom, right (end) = filet(...) ; None = aucune."""
    b = xml("<w:tcBorders/>")
    for cote in ("top", "left", "bottom", "right"):
        f = cotes.get(cote)
        if f:
            b.append(xml(f'<w:{cote} w:val="{f["val"]}" w:sz="{f["sz"]}" w:space="0" w:color="{f["color"]}"/>'))
        else:
            b.append(xml(f'<w:{cote} w:val="nil"/>'))
    poser(_tcpr(cellule), b)


def marges_cellule(cellule, haut=0.1, gauche=0.2, bas=0.1, droite=0.2):
    m = xml("<w:tcMar/>")
    for cote, v in (("top", haut), ("left", gauche), ("bottom", bas), ("right", droite)):
        m.append(xml(f'<w:{cote} w:w="{twips(v)}" w:type="dxa"/>'))
    poser(_tcpr(cellule), m)


def alignement_vertical(cellule, val="center"):
    poser(_tcpr(cellule), xml(f'<w:vAlign w:val="{val}"/>'))


def largeur_cellule(cellule, cm):
    poser(_tcpr(cellule), xml(f'<w:tcW w:w="{twips(cm)}" w:type="dxa"/>'))


def tableau_sans_bordures(tableau):
    pr = tableau._tbl.tblPr
    b = xml("<w:tblBorders/>")
    for cote in ("top", "left", "bottom", "right", "insideH", "insideV"):
        b.append(xml(f'<w:{cote} w:val="nil"/>'))
    poser(pr, b)


def tableau_largeurs(tableau, largeurs_cm, retrait_cm=0.0):
    """Largeur fixe du tableau et de chaque colonne (grille et cellules), mise en page fixe."""
    tbl = tableau._tbl
    pr = tbl.tblPr
    poser(pr, xml(f'<w:tblW w:w="{twips(sum(largeurs_cm))}" w:type="dxa"/>'))
    poser(pr, xml('<w:tblLayout w:type="fixed"/>'))
    poser(pr, xml(f'<w:tblInd w:w="{twips(retrait_cm)}" w:type="dxa"/>'))
    poser(pr, xml('<w:tblCellMar><w:left w:w="0" w:type="dxa"/><w:right w:w="0" w:type="dxa"/></w:tblCellMar>'))
    grille = tbl.tblGrid
    for i, col in enumerate(grille.findall(qn("w:gridCol"))):
        if i < len(largeurs_cm):
            col.set(qn("w:w"), str(twips(largeurs_cm[i])))
    for ligne in tableau.rows:
        for i, c in enumerate(ligne.cells):
            if i < len(largeurs_cm):
                largeur_cellule(c, largeurs_cm[i])


def ligne_insecable(ligne):
    poser(ligne._tr.get_or_add_trPr(), xml("<w:cantSplit/>"))


def ligne_entete(ligne):
    poser(ligne._tr.get_or_add_trPr(), xml("<w:tblHeader/>"))


def hauteur_ligne(ligne, cm, regle="atLeast"):
    poser(ligne._tr.get_or_add_trPr(), xml(f'<w:trHeight w:val="{twips(cm)}" w:hRule="{regle}"/>'))


# ── images ─────────────────────────────────────────────────────────────────
def _clic(balise, attributs, lien=None):
    """Les propriétés non visuelles d'une image (wp:docPr, pic:cNvPr) ; lien : le r:id d'une relation de lien
    hypertexte, qui rend l'image cliquable (a:hlinkClick)."""
    if not lien:
        return f"<{balise} {attributs}/>"
    return f'<{balise} {attributs}><a:hlinkClick r:id="{lien}"/></{balise}>'


def _graphique_image(rid, cx, cy, ident, nom, lien=None):
    cnvpr = _clic("pic:cNvPr", f'id="{ident}" name="{esc(nom)}"', lien)
    return ('<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            f'<pic:pic><pic:nvPicPr>{cnvpr}<pic:cNvPicPr/></pic:nvPicPr>'
            f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic>')


def image_en_ligne_xml(rid, largeur_cm, hauteur_cm, ident, nom, descr="", titre="", lien=None):
    """Le XML d'une image en ligne (wp:inline), à placer dans un w:r/w:drawing ; titre : la nature de l'image, que
    word.py relit (« poly:schema », « poly:dd ») ; lien : le r:id d'une relation de lien hypertexte (a:hlinkClick)."""
    cx, cy = emu(largeur_cm), emu(hauteur_cm)
    t = f' title="{esc(titre)}"' if titre else ""
    return (f'<wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{cx}" cy="{cy}"/>'
            '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
            + _clic("wp:docPr", f'id="{ident}" name="{esc(nom)}" descr="{esc(descr)}"{t}', lien)
            + '<wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>'
            f'{_graphique_image(rid, cx, cy, ident, nom, lien)}</wp:inline>')


def run_image_xml(rid, largeur_cm, hauteur_cm, ident, nom, descr="", position=None, titre="", lien=None):
    """Le run d'une image en ligne ; lien : l'image devient cliquable (a:hlinkClick) — l'appelant met en outre le run
    dans un w:hyperlink (lien_xml, lier), comme le fait Word."""
    pos = f'<w:rPr><w:position w:val="{int(round(position * 2))}"/></w:rPr>' if position else ""
    return (f"<w:r>{pos}<w:drawing>{image_en_ligne_xml(rid, largeur_cm, hauteur_cm, ident, nom, descr, titre, lien)}"
            "</w:drawing></w:r>")


# ── liens hypertextes ──────────────────────────────────────────────────────
def lien_xml(runs, lien):
    """Des runs (XML) dans un w:hyperlink vers la relation lien ; sans lien, les runs tels quels."""
    corps = "".join(runs)
    return f'<w:hyperlink r:id="{lien}" w:history="1">{corps}</w:hyperlink>' if lien else corps


def _hors_lien(run, dans_champ):
    """Un run qui ne va jamais dans un lien : une marque ou l'instruction d'un champ, le résultat d'un champ (un
    renvoi « (p. n) » reste un lien interne), une zone ancrée (wp:anchor)."""
    return (dans_champ or run.find(qn("w:fldChar")) is not None or run.find(qn("w:instrText")) is not None
            or run.find(".//" + qn("wp:anchor")) is not None)


def lier(paragraphe, lien):
    """Met dans un w:hyperlink (relation lien) les runs ordinaires d'un paragraphe (python-docx ou w:p), sans toucher
    à leur mise en forme : chaque suite de runs contigus devient un lien ; un champ complexe (PAGEREF, XE…), une zone
    ancrée, un signet ou un lien déjà posé coupent la suite et restent dehors. Rend le nombre de liens posés."""
    if not lien:
        return 0
    p = getattr(paragraphe, "_p", paragraphe)
    groupes, courant, champ = [], [], 0
    for el in list(p):
        ordinaire = False
        if el.tag == qn("w:r"):
            marque = el.find(qn("w:fldChar"))
            ordinaire = not _hors_lien(el, champ)
            if marque is not None:
                genre = marque.get(qn("w:fldCharType"))
                champ += 1 if genre == "begin" else (-1 if genre == "end" else 0)
        if ordinaire:
            courant.append(el)
        elif courant:
            groupes.append(courant)
            courant = []
    if courant:
        groupes.append(courant)
    for groupe in groupes:
        enveloppe = xml(f'<w:hyperlink r:id="{lien}" w:history="1"/>')
        groupe[0].addprevious(enveloppe)
        for el in groupe:
            enveloppe.append(el)
    return len(groupes)


def image_page_xml(rid, largeur_cm, hauteur_cm, x_cm, y_cm, ident, nom, descr="", derriere=True):
    """Une image ancrée à la page (coordonnées depuis le coin haut gauche de la feuille), derrière le texte."""
    cx, cy = emu(largeur_cm), emu(hauteur_cm)
    return (f'<w:r><w:drawing><wp:anchor distT="0" distB="0" distL="0" distR="0" simplePos="0" '
            f'relativeHeight="{100 + ident}" behindDoc="{1 if derriere else 0}" locked="1" layoutInCell="0" '
            'allowOverlap="1"><wp:simplePos x="0" y="0"/>'
            f'<wp:positionH relativeFrom="page"><wp:posOffset>{emu(x_cm)}</wp:posOffset></wp:positionH>'
            f'<wp:positionV relativeFrom="page"><wp:posOffset>{emu(y_cm)}</wp:posOffset></wp:positionV>'
            f'<wp:extent cx="{cx}" cy="{cy}"/><wp:effectExtent l="0" t="0" r="0" b="0"/><wp:wrapNone/>'
            f'<wp:docPr id="{ident}" name="{esc(nom)}" descr="{esc(descr)}"/>'
            '<wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>'
            f'{_graphique_image(rid, cx, cy, ident, nom)}</wp:anchor></w:drawing></w:r>')


def zone_marge_xml(ident, nom, descr, largeur_cm, hauteur_cm, contenu, decalage_cm=0.0):
    """Une zone de texte centrée dans la marge extérieure, alignée sur la ligne de son ancre (décalée de decalage_cm
    vers le bas), sans habillage : elle ne gêne pas le texte. L'ancre est le point du texte où se place ce run : le
    début d'un paragraphe, la fin d'un terme du glossaire, un lien ; Word met la zone sur la page et à la hauteur de
    cette ligne, même si le paragraphe a commencé plus tôt. Word ajuste sa hauteur à son contenu (spAutoFit)."""
    cx, cy = emu(largeur_cm), emu(hauteur_cm)
    return (f'<w:r><w:drawing><wp:anchor distT="0" distB="0" distL="0" distR="0" simplePos="0" '
            f'relativeHeight="{2000 + ident}" behindDoc="0" locked="0" layoutInCell="0" allowOverlap="0">'
            '<wp:simplePos x="0" y="0"/>'
            '<wp:positionH relativeFrom="outsideMargin"><wp:align>center</wp:align></wp:positionH>'
            f'<wp:positionV relativeFrom="line"><wp:posOffset>{emu(decalage_cm)}</wp:posOffset></wp:positionV>'
            f'<wp:extent cx="{cx}" cy="{cy}"/><wp:effectExtent l="0" t="0" r="0" b="0"/><wp:wrapNone/>'
            f'<wp:docPr id="{ident}" name="{esc(nom)}" descr="{esc(descr)}"/><wp:cNvGraphicFramePr/>'
            '<a:graphic><a:graphicData uri="http://schemas.microsoft.com/office/word/2010/wordprocessingShape">'
            '<wps:wsp><wps:cNvSpPr txBox="1"/><wps:spPr>'
            f'<a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></wps:spPr>'
            f'<wps:txbx><w:txbxContent>{"".join(contenu)}</w:txbxContent></wps:txbx>'
            '<wps:bodyPr rot="0" vert="horz" wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" anchor="t" '
            'anchorCtr="0"><a:spAutoFit/></wps:bodyPr></wps:wsp></a:graphicData></a:graphic>'
            '<wp14:sizeRelH relativeFrom="margin"><wp14:pctWidth>0</wp14:pctWidth></wp14:sizeRelH>'
            '<wp14:sizeRelV relativeFrom="margin"><wp14:pctHeight>0</wp14:pctHeight></wp14:sizeRelV>'
            '</wp:anchor></w:drawing></w:r>')


class Compteur:
    """Les identifiants uniques du document : images et formes (docPr), signets."""

    def __init__(self, depart=1000):
        self.n = depart

    def __call__(self):
        self.n += 1
        return self.n
