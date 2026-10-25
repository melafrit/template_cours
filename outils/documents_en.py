# -*- coding: utf-8 -*-
"""Les documents à télécharger du cours et leurs jumeaux anglais (site miroir, docs/I18N.md).

DOCUMENTS : {chemin du document français : chemin du document anglais}, depuis la racine du site (site/). Les
générateurs anglais écrivent à ces adresses ; outils/liens_langues.py fait pointer les liens des pages anglaises vers
le jumeau anglais dès qu'il existe — sinon le lien garde le document français, marqué hreflang="fr". Un document
d'une zone protégée a son jumeau dans la zone jumelle, sous en/, protégée de même.

Exemple :
    "assets/polycopies/Livret-du-cours.pdf": "en/assets/polycopies/Course-Book.pdf",
"""

DOCUMENTS = {
}


def jumeau(chemin_fr):
    """Le chemin anglais d'un document français (depuis la racine du site), ou None."""
    return DOCUMENTS.get(chemin_fr.replace("\\", "/"))
