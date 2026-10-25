# -*- coding: utf-8 -*-
"""Le référentiel du cours : la source unique de ses chiffres (CLAUDE.md, § 2 ; module 09, § 1).

Un chiffre ne s'écrit jamais à la main dans une page : la page marque l'endroit, et outils/generer_fragments.py y
écrit la valeur, dans la langue de la page ou du bloc qui l'entoure :

    ~<!-- FRAGMENT:duree-1 -->30 min<!-- /FRAGMENT:duree-1 -->
    <!-- FRAGMENT:val-places -->12 000<!-- /FRAGMENT:val-places --> places

DUREES     minutes de lecture de chaque chapitre, par numéro (celui de course-data.js) : fragments duree-N et
           duree-totale (« 30 min », « 1 h 20 »).
VALEURS    les chiffres et noms du cas : fragment val-<clé>. Une valeur est un nombre (12000 → « 12 000 » en
           français, « 12,000 » en anglais), un couple (99.9, "%") → « 99,9 % » / « 99.9% », un texte, ou un dict
           {"fr": …, "en": …}.
FRAGMENTS  les fragments composés (tableau, liste) : nom → fonction(langue) qui rend le HTML.
verifier   les contrôles de cohérence du cas, lancés avant toute écriture : une liste de messages, vide si tout va.

Le générateur fournit aussi nb-chapitres et nb-chapitres-lettres (« 3 », « trois » / « three »), d'après
site/assets/js/course-data.js. Ce fichier porte les valeurs du cours de démonstration ; nouveau_cours.py le vide
pour un cours créé.
"""

# Le cours de démonstration : trois chapitres, de 30, 25 et 25 minutes.
DUREES = {"1": 30, "2": 25, "3": 25}

VALEURS = {}

FRAGMENTS = {}


def verifier():
    """Les contrôles de cohérence du cas : [message] pour chaque écart."""
    return ["DUREES[%r] : %r n'est pas une durée en minutes" % (n, d)
            for n, d in DUREES.items() if not isinstance(d, int) or d <= 0]
