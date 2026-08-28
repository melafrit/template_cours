#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Banque de questions du jury pour une soutenance orale.

    python3 docs/generate_questions_oral.py

Produit un classeur a trois feuilles : les questions avec leur reponse
attendue, un mode d'emploi, et un tableau de suivi des passages.

DOCUMENT FORMATEUR. Il vit dans docs/, que le deploiement ne publie pas :
le communiquer aux etudiants avant l'oral viderait l'exercice de son sens.

A PERSONNALISER : la liste Q ci-dessous ne contient que trois exemples,
qui montrent la forme attendue. Toutes vos reponses doivent etre tirees
du dossier remis aux etudiants — une question dont la reponse n'est pas
dans le cours est injuste, et l'on ne s'en apercoit qu'a la correction.
"""

import os
import sys

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "docs", "Questions_oral.xlsx")

BLEU_NUIT = "1B3A5B"
BLEU_CLAIR = "D6E4F0"
GRIS_CLAIR = "F7F9FB"
JAUNE = "FEF9E7"
VERT_BG = "EAF7EF"
ROUGE_BG = "FDEDEC"

AUTEUR = "Mohamed EL AFRIT"
LICENCE = "CC BY-NC-SA 4.0"
BANDEAU = ("DOCUMENT FORMATEUR — ne pas diffuser aux étudiants. "
           "Réponses tirées du dossier remis aux étudiants.")

NIVEAUX = {
    "Accessible":    "EAF7EF",   # tout étudiant ayant travaillé doit répondre
    "Intermédiaire": "FEF9E7",   # sépare celui qui a compris de celui qui a rempli
    "Exigeant":      "FDEDEC",   # départage le haut du classement
}

# ─────────────────────────────────────────────────────────────── les questions
# ─────────────────────────────────────────────────────────────── les questions
#
# TROIS EXEMPLES, à remplacer par les vôtres. La forme compte plus que le
# nombre : une question sans « alerte » ni « relance » n'aide pas le jury en
# séance, où l'on n'a pas le temps de réfléchir à la reformulation.
#
# Répartissez les niveaux : « Accessible » vérifie l'acquis et son échec est un
# signal net ; « Intermédiaire » sépare celui qui a compris de celui qui a
# rempli ; « Exigeant » départage le haut du classement, jamais ne sanctionne.
#
Q = [
    dict(
        theme="Cadrage", niveau="Accessible",
        question="Quel est exactement le périmètre de votre travail ? "
                 "Combien d'éléments, sur quel terrain ?",
        reponse="La réponse attendue, avec les chiffres exacts du dossier. "
                "Écrivez-la comme vous voudriez l'entendre : c'est elle que "
                "vous comparerez à ce que dit l'étudiant.",
        excellente="Ce qu'un très bon candidat ajoute — un lien que les autres "
                   "ne font pas, une conséquence qu'il tire seul.",
        alerte="La réponse creuse ou fausse qui revient chaque année, et "
               "pourquoi elle est fausse. C'est ce qui sert le plus en séance.",
        relance="La question de relance, si la réponse est incomplète.",
        critere="Critère de la grille visé (n points)",
    ),
    dict(
        theme="Méthode", niveau="Intermédiaire",
        question="Pourquoi avez-vous procédé dans cet ordre ?",
        reponse="La justification attendue. Une question de méthode se corrige "
                "sur le raisonnement, pas sur le résultat.",
        excellente="Le candidat cite sa référence méthodologique et dit ce "
                   "qu'elle exige, plutôt que d'invoquer l'usage.",
        alerte="« Parce que c'est ce qui était demandé. » Réponse formelle : "
               "elle indique une méthode appliquée sans être comprise.",
        relance="Qu'est-ce qui aurait changé dans l'autre ordre ?",
        critere="Critère de la grille visé (n points)",
    ),
    dict(
        theme="Limites", niveau="Exigeant",
        question="Qu'est-ce qui, dans votre travail, reste discutable ?",
        reponse="Une limite réelle et précise, assumée. Reconnaître une limite "
                "démontre qu'on a compris la matière ; présenter un dossier "
                "comme parfait signale surtout qu'on n'en a pas vu les "
                "difficultés.",
        excellente="Le candidat dit ce qu'il a tranché malgré la limite, et "
                   "sur quel argument.",
        alerte="« Nous aurions pu approfondir. » Cela ne dit rien : ce n'est "
               "pas une limite, c'est une formule de politesse.",
        relance="Et vous avez tranché dans quel sens, finalement ?",
        critere="Critère de la grille visé (n points)",
    ),
]

COLONNES = [
    ("N°", 5),
    ("Niveau", 15),
    ("Thème", 16),
    ("Question à poser", 46),
    ("Réponse attendue", 76),
    ("Ce qui distingue une très bonne réponse", 52),
    ("Signal d'alerte", 46),
    ("Relance si la réponse reste incomplète", 38),
    ("Ligne de la grille", 26),
]


# ─────────────────────────────────────────────────────────────────── mise en forme
def entete(ws, ligne, colonne, texte, bg=BLEU_NUIT, fg="FFFFFF", taille=10):
    c = ws.cell(row=ligne, column=colonne, value=texte)
    c.font = Font(name="Calibri", bold=True, color=fg, size=taille)
    c.fill = PatternFill("solid", fgColor=bg)
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    fin = Side(style="thin", color="FFFFFF")
    c.border = Border(left=fin, right=fin, top=fin, bottom=fin)
    return c


def cellule(ws, ligne, colonne, texte="", bg=None, gras=False, italique=False,
            taille=10, align="left"):
    c = ws.cell(row=ligne, column=colonne, value=texte)
    c.font = Font(name="Calibri", bold=gras, italic=italique, size=taille)
    if bg:
        c.fill = PatternFill("solid", fgColor=bg)
    fin = Side(style="thin", color="CCCCCC")
    c.border = Border(left=fin, right=fin, top=fin, bottom=fin)
    c.alignment = Alignment(horizontal=align, vertical="top", wrap_text=True)
    return c


def bandeau(ws, derniere_colonne, titre, sous_titre):
    ws.merge_cells("A1:%s1" % derniere_colonne)
    t = ws["A1"]
    t.value = titre
    t.font = Font(name="Calibri", bold=True, size=13, color="FFFFFF")
    t.fill = PatternFill("solid", fgColor=BLEU_NUIT)
    t.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 30

    ws.merge_cells("A2:%s2" % derniere_colonne)
    a = ws["A2"]
    a.value = "%s  |  %s  |  %s" % (AUTEUR, LICENCE, BANDEAU)
    a.font = Font(name="Calibri", italic=True, size=9, color="C0392B")
    a.fill = PatternFill("solid", fgColor=JAUNE)
    a.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[2].height = 18

    ws.merge_cells("A3:%s3" % derniere_colonne)
    s = ws["A3"]
    s.value = sous_titre
    s.font = Font(name="Calibri", bold=True, size=10, color=BLEU_NUIT)
    s.fill = PatternFill("solid", fgColor=BLEU_CLAIR)
    s.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    ws.row_dimensions[3].height = 34


def hauteur(valeurs_et_largeurs, mini=54, maxi=300):
    """Hauteur de ligne estimée : openpyxl ne sait pas ajuster une cellule enroulée.

    Sans cela, les réponses longues sont tronquées à l'écran et le document est
    inutilisable pendant un oral, moment où l'on n'ouvre pas les cellules une à une.
    """
    lignes = 1
    for texte, largeur in valeurs_et_largeurs:
        if not texte:
            continue
        # ~1,05 caractère par unité de largeur Calibri 10, plus les coupures de mots
        lignes = max(lignes, -(-len(texte) // max(1, int(largeur * 1.05))) + 1)
    return max(mini, min(maxi, lignes * 13))


# ─────────────────────────────────────────────────────────────────── les feuilles
def feuille_questions(wb):
    ws = wb.active
    ws.title = "Questions"
    derniere = get_column_letter(len(COLONNES))

    bandeau(ws, derniere,
            "Soutenance — questions du jury, avec réponses attendues",
            "Posez 2 à 3 questions par étudiant, choisies d'après ce qu'il vient de présenter. "
            "Le filtre de la colonne « Niveau » permet de calibrer : Accessible pour vérifier "
            "l'acquis, Exigeant pour départager le haut du classement.")

    for i, (titre, largeur) in enumerate(COLONNES, 1):
        entete(ws, 4, i, titre)
        ws.column_dimensions[get_column_letter(i)].width = largeur
    ws.row_dimensions[4].height = 34

    for n, q in enumerate(Q, 1):
        ligne = 4 + n
        fond = GRIS_CLAIR if n % 2 == 0 else None
        cellule(ws, ligne, 1, n, bg=fond, gras=True, align="center")
        cellule(ws, ligne, 2, q["niveau"], bg=NIVEAUX[q["niveau"]], gras=True, align="center")
        cellule(ws, ligne, 3, q["theme"], bg=fond, gras=True)
        cellule(ws, ligne, 4, q["question"], bg=fond, gras=True)
        cellule(ws, ligne, 5, q["reponse"], bg=fond)
        cellule(ws, ligne, 6, q["excellente"], bg=VERT_BG)
        cellule(ws, ligne, 7, q["alerte"], bg=ROUGE_BG)
        cellule(ws, ligne, 8, q["relance"], bg=fond, italique=True)
        cellule(ws, ligne, 9, q["critere"], bg=fond, taille=9)
        ws.row_dimensions[ligne].height = hauteur([
            (q["question"], 46), (q["reponse"], 76), (q["excellente"], 52),
            (q["alerte"], 46), (q["relance"], 38),
        ])

    ws.auto_filter.ref = "A4:%s%d" % (derniere, 4 + len(Q))
    ws.freeze_panes = "E5"          # N°, niveau, thème et question restent visibles
    ws.sheet_view.zoomScale = 85
    return ws


def feuille_mode_emploi(wb):
    ws = wb.create_sheet("Mode d'emploi")
    ws.column_dimensions["A"].width = 4
    ws.column_dimensions["B"].width = 30
    ws.column_dimensions["C"].width = 110
    bandeau(ws, "C", "Comment se servir de cette banque pendant l'oral",
            "Trois minutes de lecture avant la première soutenance.")

    blocs = [
        ("Combien de questions",
         "Deux à trois par étudiant, pas davantage. Le temps de parole est de cinq minutes par "
         "personne ; les questions viennent après, et une équipe de cinq représente déjà "
         "vingt-cinq minutes d'exposé. Mieux vaut deux questions creusées qu'une rafale."),
        ("Comment les choisir",
         "Partez de ce que l'étudiant vient de présenter. S'il a exposé la phase 3, prenez les "
         "questions 13 ou 14 ; s'il a présenté le contexte, prenez la 1 ou la 4. Une question "
         "hors de sa partie reste légitime — le jury peut interroger n'importe qui sur "
         "n'importe quelle partie du dossier, et les étudiants en sont prévenus — mais elle "
         "évalue alors la connaissance du dossier, pas la maîtrise de l'exposé."),
        ("Calibrer avec la colonne Niveau",
         "Accessible : tout étudiant ayant travaillé doit répondre ; l'échec y est un signal "
         "net. Intermédiaire : sépare celui qui a compris de celui qui a rempli des champs. "
         "Exigeant : sert à départager le haut du classement, jamais à sanctionner. Ne posez "
         "une question Exigeant qu'après une réponse solide."),
        ("La relance",
         "Une seule, et seulement si la réponse est incomplète — pas si elle est fausse. Une "
         "relance après une erreur ressemble à un piège ; après une réponse partielle, elle "
         "donne sa chance. Si la relance ne débloque rien, passez : insister ne produit plus "
         "d'information sur le niveau."),
        ("Ce que vous notez",
         "La grille attribue 4 points de prestation individuelle : maîtrise du contenu présenté, "
         "capacité à répondre à une question, respect des cinq minutes. Les questions servent "
         "le deuxième point. Elles ne modifient pas les 12 points du dossier PIA, qui se notent "
         "sur l'archive exportée."),
        ("Équité entre les équipes",
         "Notez dans la feuille « Suivi » les numéros de questions posées à chacun. Sur trois "
         "heures de soutenances, la mémoire déforme : sans trace écrite, la troisième équipe "
         "reçoit des questions plus difficiles que la première, sans que personne l'ait voulu."),
        ("Réponses hors dossier",
         "Toutes les réponses attendues sont tirées du dossier de cas du chapitre 8. Si un "
         "étudiant apporte un élément extérieur — une source, une norme, un retour "
         "d'expérience — cela ne doit pas lui nuire, à condition qu'il traite d'abord le "
         "dossier. L'exercice reste borné par l'énoncé."),
        ("Diffusion",
         "Ce document ne se donne pas aux étudiants avant l'oral. Il vit dans docs/, que le "
         "script de déploiement exclut du site : il n'est pas mis en ligne. Après les "
         "soutenances, la page « Soutenance vidéo » joue le rôle de correction publique."),
    ]

    ligne = 5
    for titre, texte in blocs:
        cellule(ws, ligne, 2, titre, bg=BLEU_CLAIR, gras=True)
        cellule(ws, ligne, 3, texte)
        ws.row_dimensions[ligne].height = hauteur([(texte, 110)], mini=40)
        ligne += 1

    ws.freeze_panes = "A5"
    return ws


def feuille_suivi(wb):
    ws = wb.create_sheet("Suivi")
    colonnes = [("Équipe", 10), ("Étudiant (nom)", 26), ("Partie présentée", 30),
                ("Questions posées (n°)", 22), ("Qualité des réponses", 22),
                ("Notes du jury", 60), ("Prestation / 4", 14)]
    derniere = get_column_letter(len(colonnes))

    bandeau(ws, derniere, "Suivi des passages — une ligne par étudiant",
            "À remplir en séance. Les numéros de questions posées garantissent que toutes les "
            "équipes sont interrogées avec la même exigence.")

    for i, (titre, largeur) in enumerate(colonnes, 1):
        entete(ws, 4, i, titre)
        ws.column_dimensions[get_column_letter(i)].width = largeur
    ws.row_dimensions[4].height = 30

    for n in range(30):
        ligne = 5 + n
        for i in range(1, len(colonnes) + 1):
            cellule(ws, ligne, i, "", bg=GRIS_CLAIR if n % 2 == 0 else None)
        ws.row_dimensions[ligne].height = 26

    ws.freeze_panes = "C5"
    return ws


def main():
    wb = openpyxl.Workbook()
    feuille_questions(wb)
    feuille_mode_emploi(wb)
    feuille_suivi(wb)
    wb.save(SORTIE)

    niveaux = {}
    for q in Q:
        niveaux[q["niveau"]] = niveaux.get(q["niveau"], 0) + 1
    print("  %s" % os.path.relpath(SORTIE, RACINE).replace(os.sep, "/"))
    print("  %d questions : %s" % (
        len(Q), ", ".join("%d %s" % (n, k.lower()) for k, n in sorted(niveaux.items()))))
    print("  %d thèmes couverts" % len({q["theme"] for q in Q}))
    print("  Document formateur : docs/ est exclu du déploiement, il ne part pas en ligne.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
