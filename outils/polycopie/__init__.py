# -*- coding: utf-8 -*-
"""Le polycopié du cours (module 02) : un livret Word et PDF tiré des pages du site, relié au site par ses QR codes.

  sources     où sont les choses : le site, ses pages dans chaque langue, l'adresse publique, le glossaire
  libelles    les textes que le livret écrit de lui-même, dans les deux langues (la fiche du cours : outils/livret.py)
  navigateur  Chrome sans interface : les photographies (schémas, pictogrammes, garde) et les composants des pages
  lecture     une page du site → des blocs (titres, paragraphes, listes, tableaux, figures, encadrés, activités)
  gabarit     la page : A4, marges en miroir, styles, en-têtes et pieds
  ooxml       les briques Word que python-docx ne fournit pas : champs, signets, zones de la marge, liens
  pictos      les pictogrammes au trait et la composition de la page de garde
  images      l'atelier des images : photographies, illustrations, schémas numérotés
  qr          les QR codes (segno) et la vérification de leurs adresses
  rendu       les blocs → le document Word : texte, marge, encadrés, activités sur papier
  pages       les pages que le site n'a pas : garde, mentions, auteur, mode d'emploi, table, ouvertures, glossaire, index
  word        l'export par Microsoft Word : champs à jour, marge rangée, PDF
  controles   les contrôles du Word et du PDF
  page        la page « 📘 Polycopié » du site : ses fragments (couverture, fiche, présentation de l'auteur), que
              outils/generer_fragments.py écrit ; léger, il n'importe ni python-docx ni PyMuPDF

Les deux scripts : outils/generer_polycopie.py compose le livret (Polycopie/, jamais publié), outils/publier_polycopie.py
le publie (site/livret/). Un cours sans glossaire n'a pas de livret : le livret imprime le glossaire, l'index et les
définitions de la marge (sources.Langue.glossaire refuse) ; la page, elle, s'écrit toujours.

Les règles du livret : aucune réponse imprimée (les activités se corrigent en ligne, derrière leur QR code) ; aucune
adresse imprimée hors des mentions légales ; chaque QR code et sa légende sont des liens vers la même adresse, sans
rien changer à l'impression ; un encadré se reconnaît à son pictogramme, à son libellé et à son filet, même en noir
et blanc. Repris, en générique et bilingue, du cours d'architecture logicielle.
"""
