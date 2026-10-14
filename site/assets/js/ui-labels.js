/* =================================================================
   ui-labels.js — Tous les textes d'interface des moteurs, FR et EN
   Template de site de cours — Mohamed EL AFRIT (MIT / CC BY 4.0)

   POURQUOI CE FICHIER EXISTE
   Les moteurs (interactions.js, media.js, playlist.js…) fabriquent de
   l'interface en JavaScript : boutons, états, messages de progression.
   Ces textes ne peuvent pas être jumelés en data-tr comme le contenu
   rédigé, puisqu'ils n'existent pas dans le HTML. Ils vivent donc ici,
   dans un dictionnaire unique — et non éparpillés dans huit fichiers,
   où l'on en oublie toujours un en ajoutant un composant.

   COMMENT S'EN SERVIR DANS UN MOTEUR
       html += '<button>' + T('lecteur.lire') + '</button>';
   T() renvoie la chaîne de la langue active, et retombe sur le français
   si la clé manque en anglais — un libellé français vaut mieux qu'un
   bouton vide.

   QUAND LA LANGUE CHANGE
   i18n.js émet « tpl:langchange ». Les moteurs qui affichent du texte
   doivent s'y abonner et se redessiner :
       document.addEventListener('tpl:langchange', redessiner);

   AJOUTER UNE CLÉ
   Toujours dans les deux langues, à la même place dans les deux blocs.
   `python3 outils/verifier_i18n.py` signale les clés dépareillées.

   CE QUI N'A PAS SA PLACE ICI
   Le contenu pédagogique (il est dans les pages, jumelé en data-tr), les
   termes du glossaire (glossaire-data.js), et tout libellé propre à une
   matière. « Conséquence juridique » était écrit en dur dans le moteur
   de scénario : il est désormais passé en option par la page, parce
   qu'un cours de biologie n'a pas de conséquences juridiques.
   ================================================================= */

window.UI_LABELS = {

  fr: {
    /* ---- lecteur audio et capsules ---- */
    'lecteur.lire': 'Lire la capsule audio',
    'lecteur.pause': 'Mettre la capsule en pause',
    'lecteur.progression': 'Progression de la capsule',
    'lecteur.transcriptionAfficher': 'Afficher la transcription',
    'lecteur.transcriptionMasquer': 'Masquer la transcription',
    'lecteur.aEnregistrer': 'Capsule à enregistrer — fichier attendu :',
    'lecteur.prevu': '(prévu)',
    'lecteur.capsule': 'Capsule audio',

    /* ---- playlist ---- */
    'playlist.titre': 'Pistes audio',
    'playlist.fermer': 'Fermer la playlist',
    'playlist.basculer': 'Afficher ou masquer les pistes audio',
    'playlist.aEnregistrer': 'Piste à enregistrer',
    'playlist.sections': 'Afficher ou masquer les sections',

    /* ---- étapes de lecture ---- */
    'etapes.etape': 'Étape',
    'etapes.suivante': 'Étape suivante ›',
    'etapes.terminer': 'Terminer le chapitre ›',
    'etapes.voirResultat': 'Voir le résultat ›',
    'etapes.termine': 'Terminé',
    'etapes.chapitreTermine': 'Chapitre terminé',
    'etapes.lectureContinue': 'Lecture continue — toutes les étapes sont affichées.',
    'etapes.revenirPremiere': '↺ Revenir à la première étape',
    'etapes.aRevoir': 'À revoir avant le chapitre suivant',
    'etapes.aucuneARevoir': 'Aucune étape à revoir : les points de contrôle sont complets.',
    'etapes.sansControle': 'Ce chapitre ne comporte pas de point de contrôle.',
    'etapes.pointsControle': 'Points de contrôle du chapitre :',
    'etapes.valideesToutes': 'étapes validées — le chapitre est parcouru en entier.',
    'etapes.valideesPartiel': 'étapes validées — les autres restent ouvertes.',
    'etapes.maitrise': '— chapitre maîtrisé.',
    'etapes.relisez': 'Relisez la section',
    'etapes.tout': 'Tout afficher',
    'etapes.retour': '↩ Revenir au parcours',
    'etapes.precedent': '‹ Précédent',
    'etapes.suivant': 'Suivant ›',
    'etapes.sur': '/',
    'etapes.reste': '⏱ reste ≈',
    'etapes.surN': 'sur',

    /* ---- point de contrôle ---- */
    'controle.titre': 'Point de contrôle',
    'controle.avantDeLire': 'Avant de lire — que pensez-vous ?',
    'controle.votreHypothese': 'Votre hypothèse, avant de regarder :',
    'controle.placeholder': "Écrivez ce que vous pensez — même incertain : c'est l'essai qui fait apprendre.",
    'controle.reveler': 'Révéler la réponse',
    'controle.laReponse': 'La réponse',
    'controle.votreReponse': 'Votre réponse',
    'controle.acquis': "C'est acquis : vous pouvez poursuivre.",
    'controle.propositions': 'Propositions de réponse',
    'controle.valide': '— validée',
    'controle.suivante': 'Question suivante ›',
    'controle.termine': 'Terminé',
    'controle.recommencer': '↺ Recommencer',
    'controle.relireSection': 'Relisez la section',
    'controle.avantDeContinuer': 'avant de continuer.',
    'controle.relireCette': 'Relisez cette section avant de continuer.',
    /* explication complète : pourquoi les autres propositions, et où approfondir */
    'controle.exact': '✅ Exact.',
    'controle.non': '❌ Non',
    'controle.bonneReponse': 'la bonne réponse est',
    'controle.pourquoiPas': 'Pourquoi pas les autres ?',
    'controle.proposition': 'Proposition',
    'controle.deuxPoints': ' : ',
    'controle.votreChoix': '— votre choix',
    'controle.approfondir': '📚 Pour approfondir :',
    'lien.nouvelOnglet': '(nouvel onglet)',

    /* ---- repérage d'erreurs ---- */
    'erreurs.titre': 'Repérez les erreurs',
    'erreurs.bilan': "Vous savez maintenant relire ce type de document d'un œil critique.",

    /* ---- appariement ---- */
    'match.consigne': 'Associez chaque élément',
    'match.aide': 'Cliquez un élément à gauche, puis son correspondant à droite.',
    'match.paires': 'paires trouvées',
    'match.trouvee': 'trouvée',
    'match.sur': 'sur',

    /* ---- scénario à embranchements ---- */
    'scenario.decisions': 'Décisions possibles',
    'scenario.rejouer': '↺ Rejouer le cas',
    'scenario.vosDecisions': 'Vos décisions',
    'scenario.nonNote': "Ce cas n'est pas noté : il sert à mesurer les conséquences de chaque décision.",
    'scenario.consequence': 'Conséquence',

    /* ---- sommaire et en-tête pliable ---- */
    'sommaire.titre': 'Sommaire',
    'entete.replier': 'Objectifs et ressources du chapitre',

    /* ---- glossaire ---- */
    'glossaire.voir': '→ Voir au glossaire',

    /* ---- flashcards ---- */
    'flash.question': 'Question',
    'flash.reponse': 'Réponse',
    'flash.precedente': 'Carte précédente',
    'flash.suivante': 'Carte suivante',
    'flash.aRevoir': 'À revoir ↻',
    'flash.acquis': 'Acquis ✓',
    'flash.reinitialiser': '↺ Réinitialiser mes réponses',
    'flash.melanger': '🔀 Mélanger',
    'flash.compteARevoir': '· ↻ à revoir',

    /* ---- quiz ---- */
    'quiz.bonne': '✅ Bonne réponse.',
    'quiz.mauvaise': '❌ Réponse incorrecte.',

    /* ---- accessibilité ---- */
    'a11y.titre': "Réglages d'accessibilité et de lecture",
    'a11y.court': 'Réglages de lecture',

    /* ---- médias ---- */
    'media.slidesPleinEcran': 'Agrandir les slides en plein écran',
    'media.infographie': 'Infographie de synthèse',
    'media.polycopie': '📄 Polycopié',

    /* ---- schémas à points chauds ---- */
    'schema.titre': 'Schéma du cours',
    'schema.fermer': 'Fermer',

    /* ---- navigation ---- */
    'nav.accueil': 'Accueil du cours',
    'nav.chapitres': 'Chapitres',
    'nav.ressources': 'Ressources',
    'nav.reinitialiser': '↺ Réinitialiser ma progression',
    'nav.reinitialiserTitre': 'Effacer les chapitres marqués comme terminés',
    'nav.sections': 'Afficher ou masquer les sections',
    'nav.marquerFait': 'Marquer ce chapitre comme terminé',
    'nav.marquerAnnuler': '✓ Chapitre terminé — cliquez pour annuler',
    'nav.reinitialiserConfirme': 'Réinitialiser votre progression (chapitres terminés) ?',
    'nav.menu': 'Menu',
    'nav.theme': 'Basculer le thème',
    'nav.langue': 'Switch to English',
    'nav.sommaire': '← Sommaire',
    'nav.precedent': '← Précédent',
    'nav.suivant': 'Suivant →'
  },

  en: {
    /* ---- audio player and capsules ---- */
    'lecteur.lire': 'Play the audio capsule',
    'lecteur.pause': 'Pause the capsule',
    'lecteur.progression': 'Capsule progress',
    'lecteur.transcriptionAfficher': 'Show transcript',
    'lecteur.transcriptionMasquer': 'Hide transcript',
    'lecteur.aEnregistrer': 'Capsule not recorded yet — expected file:',
    'lecteur.prevu': '(planned)',
    'lecteur.capsule': 'Audio capsule',

    /* ---- playlist ---- */
    'playlist.titre': 'Audio tracks',
    'playlist.fermer': 'Close the playlist',
    'playlist.basculer': 'Show or hide the audio tracks',
    'playlist.aEnregistrer': 'Track not recorded yet',
    'playlist.sections': 'Show or hide the sections',

    /* ---- reading steps ---- */
    'etapes.etape': 'Step',
    'etapes.suivante': 'Next step ›',
    'etapes.terminer': 'Finish the chapter ›',
    'etapes.voirResultat': 'See the result ›',
    'etapes.termine': 'Done',
    'etapes.chapitreTermine': 'Chapter completed',
    'etapes.lectureContinue': 'Continuous reading — every step is shown.',
    'etapes.revenirPremiere': '↺ Back to the first step',
    'etapes.aRevoir': 'To review before the next chapter',
    'etapes.aucuneARevoir': 'Nothing to review: every checkpoint is complete.',
    'etapes.sansControle': 'This chapter has no checkpoint.',
    'etapes.pointsControle': 'Chapter checkpoints:',
    'etapes.valideesToutes': 'steps completed — the whole chapter has been read.',
    'etapes.valideesPartiel': 'steps completed — the others remain open.',
    'etapes.maitrise': '— chapter mastered.',
    'etapes.relisez': 'Re-read section',
    'etapes.tout': 'Show all',
    'etapes.retour': '↩ Back to the guided path',
    'etapes.precedent': '‹ Previous',
    'etapes.suivant': 'Next ›',
    'etapes.sur': '/',
    'etapes.reste': '⏱ approx. left',
    'etapes.surN': 'of',

    /* ---- checkpoint ---- */
    'controle.titre': 'Checkpoint',
    'controle.avantDeLire': 'Before reading — what do you think?',
    'controle.votreHypothese': 'Your hypothesis, before looking:',
    'controle.placeholder': 'Write what you think — even unsure: trying is what makes it stick.',
    'controle.reveler': 'Reveal the answer',
    'controle.laReponse': 'The answer',
    'controle.votreReponse': 'Your answer',
    'controle.acquis': 'Got it: you can move on.',
    'controle.propositions': 'Suggested answers',
    'controle.valide': '— completed',
    'controle.suivante': 'Next question ›',
    'controle.termine': 'Done',
    'controle.recommencer': '↺ Start again',
    'controle.relireSection': 'Review section',
    'controle.avantDeContinuer': 'before moving on.',
    'controle.relireCette': 'Review this section before moving on.',
    /* full explanation: why not the other options, and where to go further */
    'controle.exact': '✅ Correct.',
    'controle.non': '❌ No',
    'controle.bonneReponse': 'the right answer is',
    'controle.pourquoiPas': 'Why not the others?',
    'controle.proposition': 'Option',
    'controle.deuxPoints': ': ',
    'controle.votreChoix': '— your choice',
    'controle.approfondir': '📚 To go further:',
    'lien.nouvelOnglet': '(opens in a new tab)',

    /* ---- spot the errors ---- */
    'erreurs.titre': 'Spot the errors',
    'erreurs.bilan': 'You can now read this kind of document with a critical eye.',

    /* ---- matching ---- */
    'match.consigne': 'Match each item',
    'match.aide': 'Click an item on the left, then its counterpart on the right.',
    'match.paires': 'pairs found',
    'match.trouvee': 'found',
    'match.sur': 'of',

    /* ---- branching scenario ---- */
    'scenario.decisions': 'Possible decisions',
    'scenario.rejouer': '↺ Replay the case',
    'scenario.vosDecisions': 'Your decisions',
    'scenario.nonNote': 'This case is not graded: it shows the consequences of each decision.',
    'scenario.consequence': 'Consequence',

    /* ---- contents and collapsible header ---- */
    'sommaire.titre': 'Contents',
    'entete.replier': 'Chapter objectives and resources',

    /* ---- glossary ---- */
    'glossaire.voir': '→ See in the glossary',

    /* ---- flashcards ---- */
    'flash.question': 'Question',
    'flash.reponse': 'Answer',
    'flash.precedente': 'Previous card',
    'flash.suivante': 'Next card',
    'flash.aRevoir': 'Review again ↻',
    'flash.acquis': 'Got it ✓',
    'flash.reinitialiser': '↺ Reset my answers',
    'flash.melanger': '🔀 Shuffle',
    'flash.compteARevoir': '· ↻ to review',

    /* ---- quiz ---- */
    'quiz.bonne': '✅ Correct.',
    'quiz.mauvaise': '❌ Incorrect.',

    /* ---- accessibility ---- */
    'a11y.titre': 'Accessibility and reading settings',
    'a11y.court': 'Reading settings',

    /* ---- media ---- */
    'media.slidesPleinEcran': 'Open the slides full screen',
    'media.infographie': 'Summary infographic',
    'media.polycopie': '📄 Handout',

    /* ---- hotspot diagrams ---- */
    'schema.titre': 'Course diagram',
    'schema.fermer': 'Close',

    /* ---- navigation ---- */
    'nav.accueil': 'Course home',
    'nav.chapitres': 'Chapters',
    'nav.ressources': 'Resources',
    'nav.reinitialiser': '↺ Reset my progress',
    'nav.reinitialiserTitre': 'Clear chapters marked as done',
    'nav.sections': 'Show or hide the sections',
    'nav.marquerFait': 'Mark this chapter as done',
    'nav.marquerAnnuler': '✓ Chapter done — click to undo',
    'nav.reinitialiserConfirme': 'Reset your progress (completed chapters)?',
    'nav.menu': 'Menu',
    'nav.theme': 'Toggle the theme',
    'nav.langue': 'Passer en français',
    'nav.sommaire': '← Contents',
    'nav.precedent': '← Previous',
    'nav.suivant': 'Next →'
  }
};

/* Accesseur global. Volontairement tolérant : une clé absente en anglais
   retombe sur le français, une clé inconnue renvoie la clé elle-même — on
   voit alors immédiatement laquelle manque, au lieu d'un bouton vide. */
window.T = function (cle) {
  var lang = (window.TPLI18N && window.TPLI18N.lang && window.TPLI18N.lang()) || 'fr';
  var table = window.UI_LABELS[lang] || window.UI_LABELS.fr;
  var v = table[cle];
  if (v == null) v = window.UI_LABELS.fr[cle];
  return v == null ? cle : v;
};
