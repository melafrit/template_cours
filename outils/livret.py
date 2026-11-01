# -*- coding: utf-8 -*-
"""La fiche du polycopié du cours (module 02) : ce que le livret ne peut pas tirer du site.

Le titre, le sous-titre et l'auteur viennent de site/assets/js/course-data.js, sauf à les remplacer ici ; les
chapitres aussi. Le reste se décide avec l'auteur, une question à la fois (prompts/modules/02-polycopie.md) :

  pied_couverture  le pied de la page de garde (le cursus, le bloc), dans les deux langues
  categorie        la catégorie des propriétés du Word et du PDF
  annee            l'année du copyright : la seule date imprimée dans le livret
  presentation     « À propos de l'auteur », validée par l'auteur et imprimée mot pour mot ; le livret refuse de
                   s'écrire dans une langue où elle manque
  fiction          la phrase des mentions légales qui dit le cas fictif, s'il y en a un
  adresses         {langue : {domaine : (nom dans le texte, légende du QR code)}} : aucune adresse ne s'imprime, un
                   lien dont le texte est une adresse prend ce nom, et son QR code va dans la marge
  produits         les noms de produits qui ont la forme d'une adresse (« draw.io ») et restent écrits
  minuscules       les noms qui gardent leur minuscule initiale en vedette (glossaire, index, marge)
  temoin           les numéros des chapitres du témoin (generer_polycopie.py --temoin)
  edition          la mention d'édition, dans les deux langues (« Deuxième édition ») : un livret qui remplace le
                   précédent sous le même nom le dit ; la page Polycopié du site affiche la même ; à défaut,
                   « Première édition »
  site_texte       la phrase des mentions qui présente le site (à défaut, celle des libellés)
  couleurs         la palette du site, si elle n'est pas le bleu nuit et le doré du gabarit : primaire, primaire_fonce,
                   accent, accent_fonce (et, au besoin, encre, ardoise, filet, fond_primaire, fond_accent, fond_gris,
                   fond_piege, brique), en hexadécimal ; vérifier le contraste sur blanc (polycopie.gabarit.contraste)
  site_protege     True si tout le site demande des identifiants : les QR codes du site se vérifient alors dans le
                   dépôt (la chaîne ne s'authentifie jamais), et les mentions disent où trouver ses identifiants
  acces            où l'étudiant trouve ses identifiants (« repris dans le cahier de texte »), dans les deux
                   langues — jamais les identifiants eux-mêmes ; à défaut, la phrase des libellés

La démonstration : la présentation de l'auteur dit ce qu'elle doit devenir ; nouveau_cours.py la vide pour un cours
créé, que l'auteur remplit avant le premier livret.
"""

LIVRET = dict(
    titre=None,                       # None : le titre du cours (course-data.js)
    sous_titre=None,                  # None : son sous-titre
    pied_couverture={"fr": "Cours de démonstration · Template de site de cours",
                     "en": "Demo course · Course website template"},
    categorie={"fr": "Template de site de cours", "en": "Course website template"},
    annee=2026,
    presentation={
        "fr": ("Ce texte présente l'auteur du cours : son parcours, ce qu'il enseigne et ce qui l'a conduit à écrire "
               "ce cours. Dans un cours créé depuis le gabarit, l'auteur l'écrit et le valide dans outils/livret.py ; "
               "le livret l'imprime alors mot pour mot."),
        "en": ("This text introduces the author of the course: their background, what they teach, and what led them "
               "to write this course. In a course created from the template, the author writes and approves it in "
               "outils/livret.py; the course book then prints it word for word."),
    },
    fiction={"fr": "", "en": ""},
    adresses={"fr": {}, "en": {}},
    produits=(),
    minuscules=(),
    temoin=["1"],
)
