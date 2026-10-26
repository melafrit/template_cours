# -*- coding: utf-8 -*-
"""Les textes propres au polycopié, dans les deux langues.

Tout ce que le livret écrit de lui-même est ici : les mentions légales, le mode d'emploi, les titres des pages du
livret, les libellés des encadrés que la page du site ne porte pas, les légendes des QR codes, les consignes des
activités sur papier. Le reste vient des pages du site, dans leur langue : un intertitre ou un encadré « À retenir »
garde le libellé de sa page.

Ce qui change d'un cours à l'autre n'est PAS ici, mais dans sa fiche, outils/livret.py : le titre et le sous-titre
(ceux du cours, par défaut), le pied de la couverture, l'année du copyright, la présentation de l'auteur, la clause
d'un cas fictif, les adresses à nommer. L(langue) assemble les deux.

Règles d'écriture : vouvoiement (« you ») ; aucune date hors du copyright ; aucune adresse imprimée sous un QR code ;
les libellés d'encadré s'écrivent en capitales dans le texte même (« À RETENIR ») : la mise en capitales par Word
ôterait les accents des majuscules françaises. Les textes de remplacement des images (« alt ») et les textes
provisoires des champs sont ici aussi : le PDF balisé les lit dans la langue du livret.
"""
import copy

LIBELLES = {
    "fr": dict(
        langue_word="fr-FR", lcid=1036,
        sujet_temoin="Témoin de mise en page du polycopié",
        sujet="Polycopié du cours",
        maj_champs="mettre à jour les champs",
        alt=dict(garde="Page de garde", picto="Pictogramme", qr="QR code — {legende} : {url}"),
        mentions=dict(
            edition="Première édition",
            copyright="© {annee} {auteur} — Tous droits réservés.",
            usage=("L'usage personnel et pédagogique de ce polycopié par les étudiants est autorisé. Toute autre "
                   "reproduction ou diffusion, intégrale ou partielle, par quelque procédé que ce soit, est soumise "
                   "à l'accord écrit de l'auteur."),
            marques="Les marques et les noms de produits cités appartiennent à leurs propriétaires respectifs.",
            site_titre="Le cours en ligne",
            site_texte="Les capsules audio, les activités corrigées sur-le-champ, les flashcards et le QCM :",
        ),
        a_propos="À propos de l'auteur",
        mode_emploi=dict(
            titre="Comment utiliser ce polycopié",
            intro=("Ce polycopié reprend le cours en ligne : ses chapitres, chacun ouvert sur son sommaire, puis un "
                   "glossaire et un index. Il se lit seul, crayon en main ; le site le prolonge là où le papier "
                   "s'arrête : écouter, manipuler, s'entraîner."),
            renvois="Quand le texte renvoie à une autre partie du livret, il en donne la page : « (p. 12) ».",
            marge_titre="La marge est à vous",
            marge=("La grande marge extérieure sert à deux choses : vos notes — questions, reformulations, "
                   "croquis — et les QR codes. Chacun ouvre, au bon endroit, la ressource en ligne qui prolonge le "
                   "paragraphe voisin. Visez-le avec l'appareil photo de votre téléphone ; à l'écran, cliquez le QR "
                   "code ou sa légende."),
            qr=[("casque", "ÉCOUTER", "la capsule audio de la section : l'essentiel, raconté en une à deux minutes."),
                ("micro", "PODCAST", "l'épisode du podcast du chapitre, pour l'écouter avant de lire ou pour "
                                     "réviser."),
                ("glossaire", "GLOSSAIRE", "un terme du cours, défini dans la marge ; en ligne, ses emplois dans "
                                           "le cours."),
                ("crayon", "ACTIVITÉ EN LIGNE", "l'exercice de l'encadré voisin, corrigé dès que vous répondez."),
                ("coche", "CORRIGÉ EN LIGNE", "les réponses d'une série, expliquées une à une."),
                ("ecran", "EN LIGNE", "une page du site : le chapitre, une ressource, une page d'un autre site.")],
            reponses_titre="Les réponses sont en ligne",
            reponses=("Aucune réponse n'est imprimée. Cherchez d'abord sur papier, puis scannez le QR code de "
                      "l'activité : chaque réponse y est expliquée, la bonne comme les autres."),
            encadres_titre="Les encadrés",
            encadres=("Chaque encadré se reconnaît à son pictogramme, à son libellé et à son filet, même imprimé "
                      "en noir et blanc."),
            legende=[("retenir", "l'essentiel d'un chapitre, à savoir par cœur."),
                     ("repere", "une définition ou une règle à garder en tête."),
                     ("piege", "l'erreur la plus fréquente, et comment l'éviter."),
                     ("activite", "un exercice à faire sur papier, puis à vérifier en ligne."),
                     ("controle", "quelques questions pour vérifier que l'essentiel est acquis."),
                     ("plus_loin", "un approfondissement facultatif."),
                     ("lecture", "un schéma du cours, expliqué élément par élément.")],
            site_titre="Le site du cours",
            site=("Le site et ce livret se répondent : les chapitres y portent les mêmes titres et les mêmes "
                  "sections. Les schémas s'y agrandissent, les activités s'y corrigent, les capsules s'y écoutent."),
        ),

        # Les titres des pages du livret.
        toc="Table des matières",
        chapitre="Chapitre {n}",
        chapitre_toc="Chapitre {n} · {titre}",
        glossaire=dict(
            titre="Glossaire",
            intro=("Les termes du cours, tels que les définit le glossaire du site, chacun avec son équivalent "
                   "anglais et sa définition."),
            intro_temoin=("Dans ce témoin : les termes que le chapitre emploie. Le livret complet reprend les {n} "
                          "termes du glossaire du site."),
            en_ligne="Le glossaire en ligne",
        ),
        index=dict(
            titre="Index",
            intro="Les termes du glossaire, avec les pages où le cours les emploie ; en gras, la page où la marge les "
                  "définit.",
        ),

        # La page d'ouverture d'un chapitre.
        ouverture=dict(sommaire="DANS CE CHAPITRE", duree="Durée : {duree}", retenir="À retenir"),

        # La marge : les libellés et les légendes des QR codes (aucune adresse imprimée).
        marge=dict(
            ecouter="ÉCOUTER",
            podcast="PODCAST",
            glossaire="GLOSSAIRE",
            activite="ACTIVITÉ EN LIGNE",
            corrige="CORRIGÉ EN LIGNE",
            reponse="RÉPONSE EN LIGNE",
            reviser="RÉVISER",
            en_ligne="EN LIGNE",
            chapitre_en_ligne="Le chapitre {n}",
            cours="Le cours en ligne",
            flashcards="Les flashcards du chapitre",
            schema="Le schéma interactif",
            duree="{m} min {s:02d}",
        ),

        # Les encadrés que la page du site ne nomme pas.
        encadres=dict(
            retenir="À RETENIR",
            repere="REPÈRE",
            piege="ATTENTION, PIÈGE",
            activite="ACTIVITÉ",
            controle="POINT DE CONTRÔLE",
            plus_loin="POUR ALLER PLUS LOIN",
            lecture="LIRE CE SCHÉMA, ÉLÉMENT PAR ÉLÉMENT",
            situation="AVANT DE LIRE",
            erreurs="REPÉRER LES ERREURS",
            objectifs="OBJECTIFS DU CHAPITRE",
        ),

        # Les activités sur papier : la consigne du site parle de clics, celle du livret de crayon.
        papier=dict(
            controle="Une seule réponse par question ; vérifiez ensuite avec le corrigé en ligne.",
            reveal="Écrivez votre réponse, puis comparez-la avec celle du site.",
            reveal_choix="Choisissez votre réponse, puis comparez-la avec celle du site.",
            match="Associez chaque élément de gauche à une lettre de droite.",
            branch="Pour chaque situation, choisissez ce que vous feriez ; la suite se lit en ligne.",
            erreurs="Cochez les passages qui contiennent une erreur ; la correction est en ligne.",
            indice="Indice",
            clic=("clique", "cliquez", "glissez", "faites glisser", "survolez", "touchez"),
        ),
        schema="Schéma",
        tableau="Tableau",
        illustration="Illustration",
        renvoi_page="p. {n}",                 # « (p. 12) » : un renvoi à une autre partie du livret
    ),

    # L'anglais : anglais américain, titres en Title Case. Le polycopié s'y nomme « course book ».
    "en": dict(
        langue_word="en-US", lcid=1033,
        sujet_temoin="Layout sample of the course book",
        sujet="Course book",
        maj_champs="update the fields",
        alt=dict(garde="Cover", picto="Icon", qr="QR code — {legende}: {url}"),
        mentions=dict(
            edition="First edition",
            copyright="© {annee} {auteur} — All rights reserved.",
            usage=("Students may use this course book for personal and educational purposes. Any other reproduction "
                   "or distribution, in whole or in part, in any form or by any means, requires the prior written "
                   "permission of the author."),
            marques=("All trademarks and product names mentioned in this book are the property of their respective "
                     "owners."),
            site_titre="The online course",
            site_texte="Audio capsules, activities with instant feedback, flashcards, and the quiz:",
        ),
        a_propos="About the Author",
        mode_emploi=dict(
            titre="How to Use This Course Book",
            intro=("This course book contains the online course: its chapters, each opening with its contents, then "
                   "a glossary and an index. You can work through it on its own, pencil in hand; the website picks "
                   "up where paper leaves off, so you can listen, experiment, and practice."),
            renvois="When the text refers to another part of the book, it gives its page, like this: (p. 12).",
            marge_titre="The margin is yours",
            marge=("The wide outer margin has two uses: your notes — questions, rephrasings, sketches — and the QR "
                   "codes. Each code opens, at the right spot, the online resource that extends the paragraph next "
                   "to it: just point your phone’s camera at it. On screen, click the code or its caption."),
            qr=[("casque", "LISTEN", "the section’s audio capsule: the essentials, told in one to two minutes."),
                ("micro", "PODCAST", "the chapter’s podcast episode, to listen to before you read or to review."),
                ("glossaire", "GLOSSARY", "a course term, defined in the margin; online, every place the course uses "
                                          "it."),
                ("crayon", "ONLINE ACTIVITY", "the exercise in the nearby box, with feedback as soon as you answer."),
                ("coche", "ANSWERS ONLINE", "the answers to a set of questions, explained one by one."),
                ("ecran", "ONLINE", "a page of the site: the chapter, a resource, a page on another site.")],
            reponses_titre="The answers are online",
            reponses=("No answers are printed. Work on paper first, then scan the activity’s QR code: every answer is "
                      "explained there, the correct one and the others alike."),
            encadres_titre="The boxes",
            encadres=("You can recognize each box by its icon, its label, and its border, even when it is printed in "
                      "black and white."),
            legende=[("retenir", "the essentials of a chapter, to know by heart."),
                     ("repere", "a definition or a rule to keep in mind."),
                     ("piege", "the most common mistake, and how to avoid it."),
                     ("activite", "an exercise to do on paper, then to check online."),
                     ("controle", "a few questions to make sure you have the essentials down."),
                     ("plus_loin", "optional further reading."),
                     ("lecture", "a course diagram, explained element by element.")],
            site_titre="The course website",
            site=("The website and this book mirror each other: the chapters have the same titles and the same "
                  "sections. There, you can enlarge the diagrams, get feedback on the activities, and listen to the "
                  "capsules."),
        ),
        toc="Contents",
        chapitre="Chapter {n}",
        chapitre_toc="Chapter {n} · {titre}",
        glossaire=dict(
            titre="Glossary",
            intro=("The course terms, as the site’s glossary defines them, each one with its French equivalent and "
                   "its definition."),
            intro_temoin=("In this sample: the terms the chapter uses. The complete book contains all {n} terms of "
                          "the site’s glossary."),
            en_ligne="The glossary online",
        ),
        index=dict(
            titre="Index",
            intro=("The glossary terms, with the pages where the course uses them; in bold, the page where the "
                   "margin defines each one."),
        ),
        ouverture=dict(sommaire="IN THIS CHAPTER", duree="Duration: {duree}", retenir="Key takeaways"),
        marge=dict(
            ecouter="LISTEN",
            podcast="PODCAST",
            glossaire="GLOSSARY",
            activite="ONLINE ACTIVITY",
            corrige="ANSWERS ONLINE",
            reponse="ANSWER ONLINE",
            reviser="REVIEW",
            en_ligne="ONLINE",
            chapitre_en_ligne="Chapter {n}",
            cours="The online course",
            flashcards="The chapter’s flashcards",
            schema="The interactive diagram",
            duree="{m} min {s:02d} s",
        ),
        encadres=dict(
            retenir="KEY TAKEAWAYS",
            repere="KEY CONCEPT",
            piege="PITFALL",
            activite="ACTIVITY",
            controle="CHECKPOINT",
            plus_loin="GOING FURTHER",
            lecture="READING THIS DIAGRAM, ELEMENT BY ELEMENT",
            situation="BEFORE YOU READ",
            erreurs="SPOT THE ERRORS",
            objectifs="CHAPTER OBJECTIVES",
        ),
        papier=dict(
            controle="One answer per question; then check your answers online.",
            reveal="Write your answer, then compare it with the one on the site.",
            reveal_choix="Choose your answer, then compare it with the one on the site.",
            match="Match each item on the left with a letter on the right.",
            branch="For each situation, choose what you would do; what happens next is online.",
            erreurs="Check the passages that contain an error; the correction is online.",
            indice="Hint",
            clic=("click", "drag", "hover", "tap"),
        ),
        schema="Diagram",
        tableau="Table",
        illustration="Illustration",
        renvoi_page="p. {n}",
    ),
}


def L(langue, cours=None, livret=None):
    """Les libellés d'une langue (fr ou en), complétés par le cours (course-data.js : titre, sous-titre, auteur) et
    par sa fiche (outils/livret.py)."""
    try:
        out = copy.deepcopy(LIBELLES[langue])
    except KeyError:
        raise ValueError(f"langue inconnue : {langue!r} (fr ou en)") from None
    cours, livret = cours or {}, livret or {}

    def choix(valeur, defaut=""):
        if isinstance(valeur, dict):
            return valeur.get(langue) or valeur.get("fr") or defaut
        return valeur if valeur else defaut

    out["titre"] = choix(livret.get("titre"), choix(cours.get("title")))
    out["sous_titre"] = choix(livret.get("sous_titre"), choix(cours.get("subtitle")))
    out["auteur"] = livret.get("auteur") or cours.get("author", "")
    out["pied_couverture"] = choix(livret.get("pied_couverture"))
    out["categorie"] = choix(livret.get("categorie"))
    out["mots_cles"] = choix(livret.get("mots_cles"), out["titre"])
    out["annee"] = livret.get("annee", "")
    out["mentions"]["copyright"] = out["mentions"]["copyright"].format(annee=out["annee"], auteur=out["auteur"])
    out["mentions"]["fiction"] = choix(livret.get("fiction"))
    out["adresses"] = (livret.get("adresses") or {}).get(langue, {})
    out["produits"] = tuple(livret.get("produits") or ())
    out["minuscules"] = tuple(livret.get("minuscules") or ())
    return out
