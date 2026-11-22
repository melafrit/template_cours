/* =================================================================
   ui-labels.js — Tous les textes d'interface des moteurs, FR, EN et AR
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
   Toujours dans chaque langue, à la même place dans chaque bloc.
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
    'lecteur.aEnregistrer': 'Capsule à enregistrer, fichier attendu :',
    'lecteur.prevu': '(prévu)',
    'lecteur.capsule': 'Capsule audio',
    'lecteur.aVenir': 'Capsule audio bientôt disponible.',
    'lecteur.aVenirTranscription': 'Capsule audio bientôt disponible. En attendant, lisez sa transcription.',
    'lecteur.fichierAttendu': 'Fichier attendu\u00a0: ',

    /* ---- playlist ---- */
    'playlist.titre': 'Pistes audio',
    'playlist.fermer': 'Fermer la playlist',
    'playlist.basculer': 'Afficher ou masquer les pistes audio',
    'playlist.aEnregistrer': 'Piste à enregistrer',
    'playlist.sections': 'Afficher ou masquer les sections',
    'playlist.lire': 'Lire\u00a0: ',
    'playlist.aria': 'Pistes audio du cours',

    /* ---- étapes de lecture ---- */
    'etapes.etape': 'Étape',
    'etapes.suivante': 'Étape suivante ›',
    'etapes.terminer': 'Terminer le chapitre ›',
    'etapes.voirResultat': 'Voir le résultat ›',
    'etapes.termine': 'Terminé',
    'etapes.chapitreTermine': 'Chapitre terminé',
    'etapes.lectureContinue': 'Lecture continue : toutes les étapes sont affichées.',
    'etapes.revenirPremiere': '↺ Revenir à la première étape',
    'etapes.aRevoir': 'À revoir avant le chapitre suivant',
    'etapes.aucuneARevoir': 'Aucune étape à revoir : les points de contrôle sont complets.',
    'etapes.sansControle': 'Ce chapitre ne comporte pas de point de contrôle.',
    'etapes.pointsControle': 'Points de contrôle du chapitre :',
    'etapes.valideesToutes': 'étapes validées : le chapitre est parcouru en entier.',
    'etapes.valideesPartiel': 'étapes validées ; les autres restent ouvertes.',
    'etapes.maitrise': '(chapitre maîtrisé)',
    'etapes.relisez': 'Relisez la section',
    'etapes.tout': 'Tout afficher',
    'etapes.retour': '↩ Revenir au parcours',
    'etapes.precedent': '‹ Précédent',
    'etapes.suivant': 'Suivant ›',
    'etapes.sur': '/',
    'etapes.reste': '⏱ reste ≈',
    'etapes.surN': 'sur',
    'etapes.parcours': 'Parcours du chapitre',
    'etapes.bilan': 'Bilan',
    'etapes.bonnesReponses': 'bonnes réponses.',
    'etapes.reprendre': 'Reprendre où vous en étiez : section',
    'etapes.reprendreTitre': '\u00a0:\u00a0«\u00a0{t}\u00a0»',
    'etapes.masquerReprise': 'Masquer la proposition de reprise',
    'objectifs.compte1': '{n} / {total} objectif coché',
    'objectifs.compteN': '{n} / {total} objectifs cochés',
    'progression.aria': 'Progression dans le chapitre',
    'progression.valeur': 'Section {n} sur {total}',
    'progression.etiquette': 'Section {n} / {total}',
    'progression.section': 'Section {n}',

    /* ---- point de contrôle ---- */
    'controle.titre': 'Point de contrôle',
    'controle.question': 'Question',
    'controle.avantDeLire': 'Avant de lire, que pensez-vous ?',
    'controle.votreHypothese': 'Votre hypothèse, avant de regarder :',
    'controle.placeholder': "Écrivez ce que vous pensez, même incertain : c'est l'essai qui fait apprendre.",
    'controle.reveler': 'Révéler la réponse',
    'controle.laReponse': 'La réponse',
    'controle.votreReponse': 'Votre réponse',
    'controle.acquis': "C'est acquis : vous pouvez poursuivre.",
    'controle.propositions': 'Propositions de réponse',
    'controle.valide': '(validée)',
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
    'controle.votreChoix': '(votre choix)',
    'controle.approfondir': '📚 Pour approfondir :',
    'controle.indice': 'Indice\u00a0:',
    'controle.repondreDabord': "Répondez d'abord, même approximativement.",
    'controle.pourquoi': 'Pourquoi\u00a0:',
    'lien.nouvelOnglet': '(nouvel onglet)',

    /* ---- repérage d'erreurs ---- */
    'erreurs.titre': 'Repérez les erreurs',
    'erreurs.bilan': "Vous savez maintenant relire ce type de document d'un œil critique.",
    'erreurs.compte1': '{n} / {total} erreur trouvée',
    'erreurs.compteN': '{n} / {total} erreurs trouvées',
    'erreurs.erreur': '⚠ Erreur.',
    'erreurs.correct': 'Celui-ci est correct.',
    'erreurs.ailleurs': 'Cherchez ailleurs.',
    'erreurs.toutes': '🎯 Toutes les erreurs sont repérées.',

    /* ---- appariement ---- */
    'match.consigne': 'Associez chaque élément',
    'match.aide': 'Cliquez un élément à gauche, puis son correspondant à droite.',
    'match.paires': 'paires trouvées',
    'match.trouvee': 'trouvée',
    'match.sur': 'sur',
    'match.compte1': '{n} / {total} paire trouvée',
    'match.compteN': '{n} / {total} paires trouvées',
    'match.colonneA': 'Colonne A',
    'match.colonneB': 'Colonne B',
    'match.toutes': '🎯 Toutes les paires sont trouvées.',
    'match.bonne': '✅ Bonne association.',
    'match.mauvaise': '❌ Ces deux-là ne vont pas ensemble.',
    'match.reessayez': 'Réessayez.',

    /* ---- scénario à embranchements ---- */
    'scenario.decisions': 'Décisions possibles',
    'scenario.rejouer': '↺ Rejouer le cas',
    'scenario.vosDecisions': 'Vos décisions',
    'scenario.nonNote': "Ce cas n'est pas noté : il sert à mesurer les conséquences de chaque décision.",
    'scenario.consequence': 'Conséquence',
    'scenario.titre': 'Cas pratique',
    'scenario.conclure': 'Conclure ›',
    'scenario.bilan': 'Bilan',
    'scenario.sansRisque': 'sans risque',

    /* ---- sommaire ---- */
    'sommaire.titre': 'Sommaire',

    /* ---- glossaire ---- */
    'glossaire.voir': '→ Voir au glossaire',
    'glossaire.fermerBulle': 'Fermer la définition',

    /* ---- flashcards ---- */
    'flash.question': 'Question',
    'flash.reponse': 'Réponse',
    'flash.aria': 'Carte de révision\u00a0: cliquer pour retourner',
    'flash.retourner': '↺ Cliquer pour retourner',
    'flash.jeSavais': '✓ Je savais',
    'flash.carte': 'Carte',
    'flash.etatSu': '✓ su',
    'flash.etatRevoir': '↻ à revoir',
    'flash.precedente': 'Carte précédente',
    'flash.suivante': 'Carte suivante',
    'flash.aRevoir': 'À revoir ↻',
    'flash.acquis': 'Acquis ✓',
    'flash.reinitialiser': '↺ Réinitialiser mes réponses',
    'flash.melanger': '🔀 Mélanger',
    'flash.compteARevoir': '· ↻ à revoir',

    /* ---- quiz ---- */
    'quiz.titre': 'Quiz express · vérifiez vos acquis',
    'quiz.score': 'Score :',
    'quiz.bonne': '✅ Bonne réponse.',
    'quiz.mauvaise': '❌ Réponse incorrecte.',

    /* ---- accessibilité ---- */
    'a11y.titre': "Réglages d'accessibilité et de lecture",
    'a11y.court': 'Réglages de lecture',
    'a11y.allerContenu': 'Aller au contenu',
    'a11y.confort': 'Confort de lecture',
    'a11y.taille': 'Taille du texte',
    'a11y.reduire': 'Réduire le texte',
    'a11y.agrandir': 'Agrandir le texte',
    'a11y.dys': 'Lecture adaptée (DYS)',
    'a11y.dysActiver': 'Activer la lecture adaptée',
    'a11y.dysAide': 'Police « Atkinson Hyperlegible » + espacement renforcé.',
    'a11y.reinitialiser': '↺ Réinitialiser',
    'langue.groupe': 'Langue de la page',
    'filiere.groupe': 'Votre filière',
    'filiere.question': 'Quelle est votre filière ?',
    'filiere.explication': "Le cours est commun, mais certains exemples changent selon votre filière. Tant que "
      + "vous n'avez pas choisi, les deux versions s'affichent.",

    /* ---- médias ---- */
    'media.slidesPleinEcran': 'Agrandir les slides en plein écran',
    'media.infographie': 'Infographie de synthèse',
    'media.polycopie': '📄 Fiche de synthèse',
    'media.fiche': 'Fiche de synthèse',
    'media.chapitre': 'chapitre',
    'media.ouvrir': 'Ouvrir ↗',
    'media.fermer': 'Fermer',
    'media.agrandir': '⤢ Agrandir',
    'media.slides': 'Slides',
    'media.slidesPleinEcranTitre': 'Slides plein écran',
    'media.ouvrirOnglet': 'Ouvrir dans un onglet ↗',
    'media.podcast': 'Podcast',
    'media.lecturePause': 'Lecture / Pause',
    'media.reculer': 'Reculer de 10 secondes',
    'media.avancer': 'Avancer de 10 secondes',
    'media.telecharger': "Télécharger l'épisode",
    'media.telechargerTitre': "Télécharger l'épisode (MP3)",
    'media.fenetre': 'Ouvrir dans une fenêtre indépendante',
    'media.fenetreCourt': 'Fenêtre indépendante',
    'media.fermerLecteur': 'Fermer le lecteur',

    /* ---- schémas à points chauds ---- */
    'schema.titre': 'Schéma du cours',
    'schema.fermer': 'Fermer',
    'schema.fermerInfo': "Fermer l'info-bulle",
    'schema.aDeposer': 'Schéma à déposer',
    'schema.fichierAttendu': 'Fichier attendu\u00a0:',
    'schema.chemin': 'Chemin\u00a0:',
    'schema.pointsLisibles': 'Les points du schéma restent lisibles ci-dessous.',

    /* ---- activités interactives (tools.js) ---- */
    'activite.question': 'Question',
    'activite.sur': '/',
    'activite.oui': 'Oui',
    'activite.non': 'Non',
    'activite.resultat': 'Résultat',
    'activite.recommencer': '↺ Recommencer',
    'activite.score': 'Score',
    'activite.scoreFinal': 'Score\u00a0: ',
    'activite.suivant': 'Suivant ›',
    'activite.citationDebut': '«\u00a0',
    'activite.citationFin': '\u00a0»',

    /* ---- navigation ---- */
    'nav.accueil': 'Accueil du cours',
    'nav.chapitres': 'Chapitres',
    'nav.ressources': 'Ressources',
    'nav.reinitialiser': '↺ Réinitialiser ma progression',
    'nav.reinitialiserTitre': 'Effacer les chapitres marqués comme terminés',
    'nav.sections': 'Afficher ou masquer les sections',
    'nav.marquerFait': 'Marquer ce chapitre comme terminé',
    'nav.marquerAnnuler': '✓ Chapitre terminé (cliquez pour annuler)',
    'nav.reinitialiserConfirme': 'Réinitialiser votre progression (chapitres terminés) ?',
    'nav.enFrancais': 'Page encore en français',
    'nav.enAnglais': 'Page encore en anglais',
    'nav.enArabe': 'Page encore en arabe',
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
    'lecteur.aEnregistrer': 'Capsule not recorded yet, expected file:',
    'lecteur.prevu': '(planned)',
    'lecteur.capsule': 'Audio capsule',
    'lecteur.aVenir': 'Audio capsule coming soon.',
    'lecteur.aVenirTranscription': 'Audio capsule coming soon. Read its transcript in the meantime.',
    'lecteur.fichierAttendu': 'Expected file: ',

    /* ---- playlist ---- */
    'playlist.titre': 'Audio tracks',
    'playlist.fermer': 'Close the playlist',
    'playlist.basculer': 'Show or hide the audio tracks',
    'playlist.aEnregistrer': 'Track not recorded yet',
    'playlist.sections': 'Show or hide the sections',
    'playlist.lire': 'Play: ',
    'playlist.aria': 'Course audio tracks',

    /* ---- reading steps ---- */
    'etapes.etape': 'Step',
    'etapes.suivante': 'Next step ›',
    'etapes.terminer': 'Finish the chapter ›',
    'etapes.voirResultat': 'See the result ›',
    'etapes.termine': 'Done',
    'etapes.chapitreTermine': 'Chapter completed',
    'etapes.lectureContinue': 'Continuous reading: every step is shown.',
    'etapes.revenirPremiere': '↺ Back to the first step',
    'etapes.aRevoir': 'To review before the next chapter',
    'etapes.aucuneARevoir': 'Nothing to review: every checkpoint is complete.',
    'etapes.sansControle': 'This chapter has no checkpoint.',
    'etapes.pointsControle': 'Chapter checkpoints:',
    'etapes.valideesToutes': 'steps completed: the whole chapter has been read.',
    'etapes.valideesPartiel': 'steps completed; the others remain open.',
    'etapes.maitrise': '(chapter mastered)',
    'etapes.relisez': 'Re-read section',
    'etapes.tout': 'Show all',
    'etapes.retour': '↩ Back to the guided path',
    'etapes.precedent': '‹ Previous',
    'etapes.suivant': 'Next ›',
    'etapes.sur': '/',
    'etapes.reste': '⏱ approx. left',
    'etapes.surN': 'of',
    'etapes.parcours': 'Chapter path',
    'etapes.bilan': 'Summary',
    'etapes.bonnesReponses': 'correct answers.',
    'etapes.reprendre': 'Pick up where you left off: section',
    'etapes.reprendreTitre': ': “{t}”',
    'etapes.masquerReprise': 'Hide the resume suggestion',
    'objectifs.compte1': '{n} / {total} objective checked',
    'objectifs.compteN': '{n} / {total} objectives checked',
    'progression.aria': 'Chapter progress',
    'progression.valeur': 'Section {n} of {total}',
    'progression.etiquette': 'Section {n} / {total}',
    'progression.section': 'Section {n}',

    /* ---- checkpoint ---- */
    'controle.titre': 'Checkpoint',
    'controle.question': 'Question',
    'controle.avantDeLire': 'Before reading, what do you think?',
    'controle.votreHypothese': 'Your hypothesis, before looking:',
    'controle.placeholder': 'Write what you think, even unsure: trying is what makes it stick.',
    'controle.reveler': 'Reveal the answer',
    'controle.laReponse': 'The answer',
    'controle.votreReponse': 'Your answer',
    'controle.acquis': 'Got it: you can move on.',
    'controle.propositions': 'Suggested answers',
    'controle.valide': '(completed)',
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
    'controle.votreChoix': '(your choice)',
    'controle.approfondir': '📚 To go further:',
    'controle.indice': 'Hint:',
    'controle.repondreDabord': 'Answer first, even roughly.',
    'controle.pourquoi': 'Why:',
    'lien.nouvelOnglet': '(opens in a new tab)',

    /* ---- spot the errors ---- */
    'erreurs.titre': 'Spot the errors',
    'erreurs.bilan': 'You can now read this kind of document with a critical eye.',
    'erreurs.compte1': '{n} / {total} error found',
    'erreurs.compteN': '{n} / {total} errors found',
    'erreurs.erreur': '⚠ Error.',
    'erreurs.correct': 'This one is correct.',
    'erreurs.ailleurs': 'Look elsewhere.',
    'erreurs.toutes': '🎯 All the errors have been spotted.',

    /* ---- matching ---- */
    'match.consigne': 'Match each item',
    'match.aide': 'Click an item on the left, then its counterpart on the right.',
    'match.paires': 'pairs found',
    'match.trouvee': 'found',
    'match.sur': 'of',
    'match.compte1': '{n} / {total} pair found',
    'match.compteN': '{n} / {total} pairs found',
    'match.colonneA': 'Column A',
    'match.colonneB': 'Column B',
    'match.toutes': '🎯 All the pairs have been found.',
    'match.bonne': '✅ Correct match.',
    'match.mauvaise': "❌ These two don't go together.",
    'match.reessayez': 'Try again.',

    /* ---- branching scenario ---- */
    'scenario.decisions': 'Possible decisions',
    'scenario.rejouer': '↺ Replay the case',
    'scenario.vosDecisions': 'Your decisions',
    'scenario.nonNote': 'This case is not graded: it shows the consequences of each decision.',
    'scenario.consequence': 'Consequence',
    'scenario.titre': 'Case study',
    'scenario.conclure': 'Conclude ›',
    'scenario.bilan': 'Summary',
    'scenario.sansRisque': 'risk-free',

    /* ---- contents ---- */
    'sommaire.titre': 'Contents',

    /* ---- glossary ---- */
    'glossaire.voir': '→ See in the glossary',
    'glossaire.fermerBulle': 'Close the definition',

    /* ---- flashcards ---- */
    'flash.question': 'Question',
    'flash.reponse': 'Answer',
    'flash.aria': 'Review card: click to flip',
    'flash.retourner': '↺ Click to flip',
    'flash.jeSavais': '✓ I knew it',
    'flash.carte': 'Card',
    'flash.etatSu': '✓ known',
    'flash.etatRevoir': '↻ to review',
    'flash.precedente': 'Previous card',
    'flash.suivante': 'Next card',
    'flash.aRevoir': 'Review again ↻',
    'flash.acquis': 'Got it ✓',
    'flash.reinitialiser': '↺ Reset my answers',
    'flash.melanger': '🔀 Shuffle',
    'flash.compteARevoir': '· ↻ to review',

    /* ---- quiz ---- */
    'quiz.titre': 'Quick quiz · check what you have learnt',
    'quiz.score': 'Score:',
    'quiz.bonne': '✅ Correct.',
    'quiz.mauvaise': '❌ Incorrect.',

    /* ---- accessibility ---- */
    'a11y.titre': 'Accessibility and reading settings',
    'a11y.court': 'Reading settings',
    'a11y.allerContenu': 'Skip to content',
    'a11y.confort': 'Reading comfort',
    'a11y.taille': 'Text size',
    'a11y.reduire': 'Decrease text size',
    'a11y.agrandir': 'Increase text size',
    'a11y.dys': 'Easy reading (DYS)',
    'a11y.dysActiver': 'Turn on easy reading',
    'a11y.dysAide': '“Atkinson Hyperlegible” font + wider spacing.',
    'a11y.reinitialiser': '↺ Reset',
    'langue.groupe': 'Page language',
    'filiere.groupe': 'Your program',
    'filiere.question': 'Which program are you in?',
    'filiere.explication': 'The course is shared, but some examples change with your program. Until you choose, '
      + 'both versions are shown.',

    /* ---- media ---- */
    'media.slidesPleinEcran': 'Open the slides full screen',
    'media.infographie': 'Summary infographic',
    'media.polycopie': '📄 Summary sheet',
    'media.fiche': 'Summary sheet',
    'media.chapitre': 'chapter',
    'media.ouvrir': 'Open ↗',
    'media.fermer': 'Close',
    'media.agrandir': '⤢ Enlarge',
    'media.slides': 'Slides',
    'media.slidesPleinEcranTitre': 'Full-screen slides',
    'media.ouvrirOnglet': 'Open in a new tab ↗',
    'media.podcast': 'Podcast',
    'media.lecturePause': 'Play / Pause',
    'media.reculer': 'Back 10 seconds',
    'media.avancer': 'Forward 10 seconds',
    'media.telecharger': 'Download the episode',
    'media.telechargerTitre': 'Download the episode (MP3)',
    'media.fenetre': 'Open in a separate window',
    'media.fenetreCourt': 'Separate window',
    'media.fermerLecteur': 'Close the player',

    /* ---- hotspot diagrams ---- */
    'schema.titre': 'Course diagram',
    'schema.fermer': 'Close',
    'schema.fermerInfo': 'Close the tooltip',
    'schema.aDeposer': 'Diagram to be added',
    'schema.fichierAttendu': 'Expected file:',
    'schema.chemin': 'Path:',
    'schema.pointsLisibles': "The diagram's points remain readable below.",

    /* ---- interactive activities (tools.js) ---- */
    'activite.question': 'Question',
    'activite.sur': '/',
    'activite.oui': 'Yes',
    'activite.non': 'No',
    'activite.resultat': 'Result',
    'activite.recommencer': '↺ Restart',
    'activite.score': 'Score',
    'activite.scoreFinal': 'Score: ',
    'activite.suivant': 'Next ›',
    'activite.citationDebut': '“',
    'activite.citationFin': '”',

    /* ---- navigation ---- */
    'nav.accueil': 'Course home',
    'nav.chapitres': 'Chapters',
    'nav.ressources': 'Resources',
    'nav.reinitialiser': '↺ Reset my progress',
    'nav.reinitialiserTitre': 'Clear chapters marked as done',
    'nav.sections': 'Show or hide the sections',
    'nav.marquerFait': 'Mark this chapter as done',
    'nav.marquerAnnuler': '✓ Chapter done (click to undo)',
    'nav.reinitialiserConfirme': 'Reset your progress (completed chapters)?',
    'nav.enFrancais': 'Page still in French',
    'nav.enAnglais': 'Page still in English',
    'nav.enArabe': 'Page still in Arabic',
    'nav.menu': 'Menu',
    'nav.theme': 'Toggle the theme',
    'nav.langue': 'Passer en français',
    'nav.sommaire': '← Contents',
    'nav.precedent': '← Previous',
    'nav.suivant': 'Next →'
  },

  /* L'arabe (site miroir, ar/), d'après docs/LEXIQUE-ar.md. Les chevrons ‹ › sont des caractères « miroirs » :
     le navigateur les retourne de lui-même dans une page de droite à gauche, et « › » y garde son sens de
     « suivant ». Les flèches → ←, elles, ne se retournent pas : elles sont inversées ici. */
  ar: {
    /* ---- lecteur audio et capsules ---- */
    'lecteur.lire': 'تشغيل الكبسولة الصوتية',
    'lecteur.pause': 'إيقاف الكبسولة مؤقتًا',
    'lecteur.progression': 'تقدّم الكبسولة',
    'lecteur.transcriptionAfficher': 'إظهار النص المكتوب',
    'lecteur.transcriptionMasquer': 'إخفاء النص المكتوب',
    'lecteur.aEnregistrer': 'كبسولة قيد التسجيل، الملف المنتظَر:',
    'lecteur.prevu': '(مُبرمَجة)',
    'lecteur.capsule': 'كبسولة صوتية',
    'lecteur.aVenir': 'الكبسولة الصوتية متاحة قريبًا.',
    'lecteur.aVenirTranscription': 'الكبسولة الصوتية متاحة قريبًا. اقرؤوا نصّها المكتوب في الأثناء.',
    'lecteur.fichierAttendu': 'الملف المنتظَر: ',

    /* ---- playlist ---- */
    'playlist.titre': 'المقاطع الصوتية',
    'playlist.fermer': 'إغلاق قائمة التشغيل',
    'playlist.basculer': 'إظهار المقاطع الصوتية أو إخفاؤها',
    'playlist.aEnregistrer': 'مقطع قيد التسجيل',
    'playlist.sections': 'إظهار الأقسام أو إخفاؤها',
    'playlist.lire': 'تشغيل: ',
    'playlist.aria': 'المقاطع الصوتية للمقرّر',

    /* ---- étapes de lecture ---- */
    'etapes.etape': 'الخطوة',
    'etapes.suivante': 'الخطوة التالية ›',
    'etapes.terminer': 'إنهاء الفصل ›',
    'etapes.voirResultat': 'عرض النتيجة ›',
    'etapes.termine': 'مُنجَز',
    'etapes.chapitreTermine': 'تمّ إنجاز الفصل',
    'etapes.lectureContinue': 'قراءة متواصلة: جميع الخطوات معروضة.',
    'etapes.revenirPremiere': '↺ العودة إلى الخطوة الأولى',
    'etapes.aRevoir': 'للمراجعة قبل الفصل التالي',
    'etapes.aucuneARevoir': 'لا خطوة للمراجعة: الوقفات التقييمية مكتملة.',
    'etapes.sansControle': 'لا يتضمّن هذا الفصل وقفة تقييمية.',
    'etapes.pointsControle': 'الوقفات التقييمية للفصل:',
    'etapes.valideesToutes': 'خطوات مُنجَزة: تمّت قراءة الفصل كاملًا.',
    'etapes.valideesPartiel': 'خطوات مُنجَزة، والبقية ما زالت مفتوحة.',
    'etapes.maitrise': '(الفصل متقَن)',
    'etapes.relisez': 'أعيدوا قراءة القسم',
    'etapes.tout': 'عرض الكلّ',
    'etapes.retour': '↩ العودة إلى المسار',
    'etapes.precedent': '‹ السابق',
    'etapes.suivant': 'التالي ›',
    'etapes.sur': '/',
    'etapes.reste': '⏱ المتبقّي ≈',
    'etapes.surN': 'من',
    'etapes.parcours': 'مسار الفصل',
    'etapes.bilan': 'الحصيلة',
    'etapes.bonnesReponses': 'إجابات صحيحة.',
    'etapes.reprendre': 'استئناف القراءة من حيث توقّفتم: القسم',
    'etapes.reprendreTitre': ': «{t}»',
    'etapes.masquerReprise': 'إخفاء اقتراح الاستئناف',
    'objectifs.compte1': 'الأهداف المُنجَزة: {n} / {total}',
    'objectifs.compteN': 'الأهداف المُنجَزة: {n} / {total}',
    'progression.aria': 'التقدّم في الفصل',
    'progression.valeur': 'القسم {n} من {total}',
    'progression.etiquette': 'القسم {n} / {total}',
    'progression.section': 'القسم {n}',

    /* ---- point de contrôle ---- */
    'controle.titre': 'وقفة تقييمية',
    'controle.question': 'السؤال',
    'controle.avantDeLire': 'قبل القراءة، ما رأيكم؟',
    'controle.votreHypothese': 'فرضيّتكم، قبل الاطّلاع على الجواب:',
    'controle.placeholder': 'اكتبوا ما تظنّونه، ولو لم تكونوا متأكّدين: المحاولة هي التي تُعلّم.',
    'controle.reveler': 'إظهار الجواب',
    'controle.laReponse': 'الجواب',
    'controle.votreReponse': 'جوابكم',
    'controle.acquis': 'تمّ الاكتساب: يمكنكم المتابعة.',
    'controle.propositions': 'الاقتراحات',
    'controle.valide': '(صحيح)',
    'controle.suivante': 'السؤال التالي ›',
    'controle.termine': 'مُنجَز',
    'controle.recommencer': '↺ إعادة المحاولة',
    'controle.relireSection': 'أعيدوا قراءة القسم',
    'controle.avantDeContinuer': 'قبل المتابعة.',
    'controle.relireCette': 'أعيدوا قراءة هذا القسم قبل المتابعة.',
    /* explication complète : pourquoi les autres propositions, et où approfondir */
    'controle.exact': '✅ صحيح.',
    'controle.non': '❌ لا',
    'controle.bonneReponse': 'الجواب الصحيح هو',
    'controle.pourquoiPas': 'لماذا ليست الاقتراحات الأخرى؟',
    'controle.proposition': 'الاقتراح',
    'controle.deuxPoints': ': ',
    'controle.votreChoix': '(اختياركم)',
    'controle.approfondir': '📚 للتعمّق:',
    'controle.indice': 'تلميح:',
    'controle.repondreDabord': 'أجيبوا أولًا، ولو على وجه التقريب.',
    'controle.pourquoi': 'السبب:',
    'lien.nouvelOnglet': '(علامة تبويب جديدة)',

    /* ---- repérage d'erreurs ---- */
    'erreurs.titre': 'حدّدوا الأخطاء',
    'erreurs.bilan': 'أصبحتم الآن قادرين على قراءة هذا النوع من الوثائق بعين ناقدة.',
    'erreurs.compte1': 'الأخطاء المكتشَفة: {n} / {total}',
    'erreurs.compteN': 'الأخطاء المكتشَفة: {n} / {total}',
    'erreurs.erreur': '⚠ خطأ.',
    'erreurs.correct': 'هذه العبارة صحيحة.',
    'erreurs.ailleurs': 'ابحثوا في موضع آخر.',
    'erreurs.toutes': '🎯 تمّ تحديد جميع الأخطاء.',

    /* ---- appariement ---- */
    'match.consigne': 'اربطوا كلّ عنصر بما يقابله',
    'match.aide': 'انقروا على عنصر في اليمين، ثم على ما يقابله في اليسار.',
    'match.paires': 'أزواج مكتشَفة',
    'match.trouvee': 'مكتشَف',
    'match.sur': 'من',
    'match.compte1': 'الأزواج المكتشَفة: {n} / {total}',
    'match.compteN': 'الأزواج المكتشَفة: {n} / {total}',
    'match.colonneA': 'العمود أ',
    'match.colonneB': 'العمود ب',
    'match.toutes': '🎯 تمّ إيجاد جميع الأزواج.',
    'match.bonne': '✅ ربط صحيح.',
    'match.mauvaise': '❌ هذان العنصران لا يتطابقان.',
    'match.reessayez': 'حاولوا من جديد.',

    /* ---- scénario à embranchements ---- */
    'scenario.decisions': 'القرارات الممكنة',
    'scenario.rejouer': '↺ إعادة الحالة',
    'scenario.vosDecisions': 'قراراتكم',
    'scenario.nonNote': 'هذه الحالة غير منقَّطة: إنها تُبيّن عواقب كلّ قرار.',
    'scenario.consequence': 'العاقبة',
    'scenario.titre': 'حالة تطبيقية',
    'scenario.conclure': 'الخلاصة ›',
    'scenario.bilan': 'الحصيلة',
    'scenario.sansRisque': 'دون مخاطرة',

    /* ---- sommaire ---- */
    'sommaire.titre': 'المحتويات',

    /* ---- glossaire ---- */
    'glossaire.voir': '← انظر في مسرد المصطلحات',
    'glossaire.fermerBulle': 'إغلاق التعريف',

    /* ---- flashcards ---- */
    'flash.question': 'السؤال',
    'flash.reponse': 'الجواب',
    'flash.aria': 'بطاقة مراجعة: انقروا لقلبها',
    'flash.retourner': '↺ انقروا لقلب البطاقة',
    'flash.jeSavais': '✓ كنت أعرف',
    'flash.carte': 'البطاقة',
    'flash.etatSu': '✓ معروفة',
    'flash.etatRevoir': '↻ للمراجعة',
    'flash.precedente': 'البطاقة السابقة',
    'flash.suivante': 'البطاقة التالية',
    'flash.aRevoir': 'للمراجعة ↻',
    'flash.acquis': 'مكتسَبة ✓',
    'flash.reinitialiser': '↺ إعادة ضبط إجاباتي',
    'flash.melanger': '🔀 خلط البطاقات',
    'flash.compteARevoir': '· ↻ للمراجعة',

    /* ---- quiz ---- */
    'quiz.titre': 'اختبار سريع · تحقّقوا من مكتسباتكم',
    'quiz.score': 'النتيجة:',
    'quiz.bonne': '✅ إجابة صحيحة.',
    'quiz.mauvaise': '❌ إجابة غير صحيحة.',

    /* ---- accessibilité ---- */
    'a11y.titre': 'إعدادات إمكانية الوصول والقراءة',
    'a11y.court': 'إعدادات القراءة',
    'a11y.allerContenu': 'الانتقال إلى المحتوى',
    'a11y.confort': 'راحة القراءة',
    'a11y.taille': 'حجم النص',
    'a11y.reduire': 'تصغير النص',
    'a11y.agrandir': 'تكبير النص',
    'a11y.dys': 'القراءة الميسّرة (DYS)',
    'a11y.dysActiver': 'تفعيل القراءة الميسّرة',
    'a11y.dysAide': 'خطّ أوضح وتباعد أكبر بين الأسطر والكلمات.',
    'a11y.reinitialiser': '↺ إعادة الضبط',
    'langue.groupe': 'لغة الصفحة',
    'filiere.groupe': 'تخصّصكم',
    'filiere.question': 'ما تخصّصكم؟',
    'filiere.explication': 'المقرّر مشترك، لكنّ بعض الأمثلة تتغيّر حسب تخصّصكم. وما دمتم لم تختاروا، تُعرض '
      + 'النسختان معًا.',

    /* ---- médias ---- */
    'media.slidesPleinEcran': 'عرض الشرائح بملء الشاشة',
    'media.infographie': 'إنفوجرافيك تلخيصي',
    'media.polycopie': '📄 البطاقة التلخيصية',
    'media.fiche': 'البطاقة التلخيصية',
    'media.chapitre': 'الفصل',
    'media.ouvrir': 'فتح ↖',
    'media.fermer': 'إغلاق',
    'media.agrandir': '⤢ تكبير',
    'media.slides': 'الشرائح',
    'media.slidesPleinEcranTitre': 'الشرائح بملء الشاشة',
    'media.ouvrirOnglet': 'فتح في علامة تبويب ↖',
    'media.podcast': 'البودكاست',
    'media.lecturePause': 'تشغيل / إيقاف مؤقت',
    'media.reculer': 'الرجوع 10 ثوانٍ',
    'media.avancer': 'التقدّم 10 ثوانٍ',
    'media.telecharger': 'تنزيل الحلقة',
    'media.telechargerTitre': 'تنزيل الحلقة (MP3)',
    'media.fenetre': 'فتح في نافذة مستقلّة',
    'media.fenetreCourt': 'نافذة مستقلّة',
    'media.fermerLecteur': 'إغلاق المشغّل',

    /* ---- schémas à points chauds ---- */
    'schema.titre': 'مخطّط المقرّر',
    'schema.fermer': 'إغلاق',
    'schema.fermerInfo': 'إغلاق النافذة التوضيحية',
    'schema.aDeposer': 'مخطّط ينبغي إيداعه',
    'schema.fichierAttendu': 'الملف المنتظَر:',
    'schema.chemin': 'المسار:',
    'schema.pointsLisibles': 'تبقى نقاط المخطّط مقروءة أدناه.',

    /* ---- activités interactives (tools.js) ---- */
    'activite.question': 'السؤال',
    'activite.sur': '/',
    'activite.oui': 'نعم',
    'activite.non': 'لا',
    'activite.resultat': 'النتيجة',
    'activite.recommencer': '↺ إعادة المحاولة',
    'activite.score': 'النتيجة',
    'activite.scoreFinal': 'النتيجة: ',
    'activite.suivant': 'التالي ›',
    'activite.citationDebut': '«',
    'activite.citationFin': '»',

    /* ---- navigation ---- */
    'nav.accueil': 'الصفحة الرئيسية للمقرّر',
    'nav.chapitres': 'الفصول',
    'nav.ressources': 'الموارد',
    'nav.reinitialiser': '↺ إعادة ضبط تقدّمي',
    'nav.reinitialiserTitre': 'مسح الفصول المؤشَّر عليها بأنها مُنجَزة',
    'nav.sections': 'إظهار الأقسام أو إخفاؤها',
    'nav.marquerFait': 'التأشير على هذا الفصل بأنه مُنجَز',
    'nav.marquerAnnuler': '✓ الفصل مُنجَز (انقروا للإلغاء)',
    'nav.reinitialiserConfirme': 'هل تريدون إعادة ضبط تقدّمكم (الفصول المُنجَزة)؟',
    'nav.enFrancais': 'صفحة ما زالت بالفرنسية',
    'nav.enAnglais': 'صفحة ما زالت بالإنجليزية',
    'nav.enArabe': 'صفحة ما زالت بالعربية',
    'nav.menu': 'القائمة',
    'nav.theme': 'تغيير المظهر',
    'nav.langue': 'التبديل إلى الإنجليزية',
    'nav.sommaire': '→ المحتويات',
    'nav.precedent': '→ السابق',
    'nav.suivant': 'التالي ←'
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
