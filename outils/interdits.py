# -*- coding: utf-8 -*-
"""Les interdits du cours : ce qui n'apparaît jamais hors de sa place (CLAUDE.md, § 2 ; prompt paramétrable, règle 8).

Le sujet du TP, ses chiffres, les mots d'une épreuve confidentielle : un exemple du cours qui les reprendrait — même
pour illustrer une méthode — soufflerait une réponse. outils/verifier_interdits.py les cherche partout où le cours
se publie (pages et jumelles anglaises, données du site, scripts des capsules audio, contenu des polycopiés), hors
des pages où ils sont chez eux (PERMIS). Vides dans le gabarit : chaque cours remplit les siens, dès le cadrage.

MOTS     mots ou expressions ; cherchés sans tenir compte de la casse ni des accents, en mots entiers.
NOMBRES  nombres (12, 99.95, 12000) ; cherchés avec virgule ou point, séparateurs de milliers compris, et en
         toutes lettres, en français et en anglais, de 0 à 99 (les scripts audio écrivent les nombres).
MOTIFS   les cas particuliers : [("nom", r"expression régulière")], cherchés tels quels.
PERMIS   chemins depuis la racine du site (site/) où les interdits sont chez eux : une page (« tp.html ») ou un
         dossier (« correction/ ») ; leurs jumelles sous en/ le sont aussi.

Exemple, pour un TP sur une flotte de vélos en libre-service :
    MOTS = ["vélos en libre-service", "station de recharge"]
    NOMBRES = [99.5, 450]
    MOTIFS = [("plafond d'arrêt du TP", r"(?<!\\d)45\\s?min")]
    PERMIS = ["tp.html", "correction/"]
"""

MOTS = []
NOMBRES = []
MOTIFS = []
PERMIS = []
