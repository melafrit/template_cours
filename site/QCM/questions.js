/* =================================================================
   questions.js — Banque de questions BILINGUE (FR/EN) du QCM-démo
   Thème : « Concevoir un cours en ligne » (5 chapitres)
   Template de cours — M. EL AFRIT (CC BY-NC-SA 4.0)

   Format attendu par les pages (index / entrainement / correction / dashboard) :
     { id, chapitre, difficulte, enonce:{fr,en}, propositions:[{fr,en}×4] }
   Réponse UNIQUE par question. Voir corrections.js pour la clé + explications.
   ================================================================= */
window.QCM_QUESTIONS = {
  meta: {
    titre: {
      fr: 'QCM — Concevoir un cours en ligne',
      en: 'Quiz — Designing an online course'
    },
    formation: {
      fr: 'Démo du template de cours',
      en: 'Course template demo'
    },
    annee_academique: '2025-2026',
    auteur: 'Mohamed EL AFRIT',
    nombre_questions: 12,
    note_sur: 20
  },
  questions: [
    /* ---------- Chapitre 1 — Cadrer ---------- */
    {
      id: 'Q01', chapitre: 1, difficulte: 'vert',
      enonce: {
        fr: 'Quel est le tout premier élément à définir quand on cadre un cours en ligne ?',
        en: 'What is the very first element to define when framing an online course?'
      },
      propositions: [
        { fr: 'Les objectifs pédagogiques visés', en: 'The intended learning objectives' },
        { fr: 'La couleur du thème graphique', en: 'The colour of the visual theme' },
        { fr: 'Le format des fichiers vidéo', en: 'The video file format' },
        { fr: 'Le nom de la plateforme d\'hébergement', en: 'The name of the hosting platform' }
      ]
    },
    {
      id: 'Q02', chapitre: 1, difficulte: 'jaune',
      enonce: {
        fr: 'Un objectif pédagogique « bien formulé » s\'appuie de préférence sur…',
        en: 'A well-formulated learning objective is preferably based on…'
      },
      propositions: [
        { fr: 'une intention vague comme « sensibiliser au sujet »', en: 'a vague intention such as "raise awareness of the topic"' },
        { fr: 'un verbe d\'action observable et mesurable', en: 'an observable, measurable action verb' },
        { fr: 'le nombre total de diapositives prévues', en: 'the total number of planned slides' },
        { fr: 'la durée exacte de chaque vidéo en secondes', en: 'the exact length of each video in seconds' }
      ]
    },
    /* ---------- Chapitre 2 — Structurer ---------- */
    {
      id: 'Q03', chapitre: 2, difficulte: 'vert',
      enonce: {
        fr: 'À quoi sert un découpage en modules et séquences dans un cours en ligne ?',
        en: 'What is the purpose of splitting an online course into modules and units?'
      },
      propositions: [
        { fr: 'À augmenter mécaniquement le temps total de visionnage', en: 'To mechanically increase total watch time' },
        { fr: 'À masquer la progression réelle de l\'apprenant', en: 'To hide the learner\'s actual progress' },
        { fr: 'À rendre la progression claire et gérable par étapes', en: 'To make progression clear and manageable step by step' },
        { fr: 'À supprimer le besoin de tout objectif pédagogique', en: 'To remove the need for any learning objective' }
      ]
    },
    {
      id: 'Q04', chapitre: 2, difficulte: 'orange',
      enonce: {
        fr: 'L\'« alignement pédagogique » (constructive alignment) désigne la cohérence entre…',
        en: '"Constructive alignment" refers to the consistency between…'
      },
      propositions: [
        { fr: 'la longueur des vidéos et la taille des images', en: 'video length and image size' },
        { fr: 'le budget du projet et le nombre d\'inscrits', en: 'the project budget and the number of enrolments' },
        { fr: 'la marque de la plateforme et celle du créateur', en: 'the platform brand and the creator\'s brand' },
        { fr: 'objectifs, activités d\'apprentissage et évaluations', en: 'objectives, learning activities and assessments' }
      ]
    },
    /* ---------- Chapitre 3 — Multimédia ---------- */
    {
      id: 'Q05', chapitre: 3, difficulte: 'jaune',
      enonce: {
        fr: 'D\'après le principe de redondance (Mayer), il vaut généralement mieux éviter de…',
        en: 'According to the redundancy principle (Mayer), it is generally best to avoid…'
      },
      propositions: [
        { fr: 'lire à voix haute un texte déjà affiché mot pour mot à l\'écran', en: 'reading aloud text already shown word-for-word on screen' },
        { fr: 'illustrer une explication orale par un schéma simple', en: 'illustrating a spoken explanation with a simple diagram' },
        { fr: 'commenter une animation pendant qu\'elle se déroule', en: 'narrating an animation while it plays' },
        { fr: 'segmenter une longue vidéo en courtes capsules', en: 'segmenting a long video into short clips' }
      ]
    },
    {
      id: 'Q06', chapitre: 3, difficulte: 'orange',
      enonce: {
        fr: 'Pour un sous-titrage vidéo réutilisable et éditable, quel format privilégier ?',
        en: 'For reusable, editable video subtitles, which format should you favour?'
      },
      propositions: [
        { fr: 'Du texte « incrusté » (burned-in) directement dans l\'image', en: 'Text "burned-in" directly into the image' },
        { fr: 'Un fichier de sous-titres séparé (.srt / .vtt)', en: 'A separate subtitle file (.srt / .vtt)' },
        { fr: 'Une capture d\'écran du texte au format PNG', en: 'A screenshot of the text as a PNG image' },
        { fr: 'Un enregistrement audio supplémentaire du texte', en: 'An extra audio recording of the text' }
      ]
    },
    /* ---------- Chapitre 4 — Évaluer ---------- */
    {
      id: 'Q07', chapitre: 4, difficulte: 'vert',
      enonce: {
        fr: 'Quelle est la principale finalité d\'une évaluation « formative » ?',
        en: 'What is the main purpose of a "formative" assessment?'
      },
      propositions: [
        { fr: 'Classer définitivement les apprenants entre eux', en: 'To rank learners against each other once and for all' },
        { fr: 'Délivrer la note finale et le certificat', en: 'To deliver the final grade and the certificate' },
        { fr: 'Donner un retour pour aider l\'apprenant à progresser', en: 'To give feedback that helps the learner improve' },
        { fr: 'Réduire le nombre de questions à corriger', en: 'To reduce the number of questions to grade' }
      ]
    },
    {
      id: 'Q08', chapitre: 4, difficulte: 'rouge',
      enonce: {
        fr: 'Un bon distracteur dans une question à choix multiple devrait surtout être…',
        en: 'A good distractor in a multiple-choice question should above all be…'
      },
      propositions: [
        { fr: 'manifestement absurde pour être vite éliminé', en: 'obviously absurd so it is quickly ruled out' },
        { fr: 'systématiquement plus court que la bonne réponse', en: 'systematically shorter than the correct answer' },
        { fr: 'systématiquement plus long que la bonne réponse', en: 'systematically longer than the correct answer' },
        { fr: 'plausible et fondé sur une erreur fréquente', en: 'plausible and based on a common misconception' }
      ]
    },
    /* ---------- Chapitre 5 — Accessibilité & diffusion ---------- */
    {
      id: 'Q09', chapitre: 5, difficulte: 'jaune',
      enonce: {
        fr: 'Quel attribut HTML fournit une alternative textuelle à une image pour les lecteurs d\'écran ?',
        en: 'Which HTML attribute provides a text alternative to an image for screen readers?'
      },
      propositions: [
        { fr: 'L\'attribut alt', en: 'The alt attribute' },
        { fr: 'L\'attribut title seul', en: 'The title attribute alone' },
        { fr: 'L\'attribut href', en: 'The href attribute' },
        { fr: 'L\'attribut style', en: 'The style attribute' }
      ]
    },
    {
      id: 'Q10', chapitre: 5, difficulte: 'orange',
      enonce: {
        fr: 'Pour respecter le critère de contraste WCAG AA sur du texte normal, le ratio minimal est…',
        en: 'To meet the WCAG AA contrast criterion for normal text, the minimum ratio is…'
      },
      propositions: [
        { fr: '1:1', en: '1:1' },
        { fr: '4,5:1', en: '4.5:1' },
        { fr: '1,2:1', en: '1.2:1' },
        { fr: '2:1', en: '2:1' }
      ]
    },
    /* ---------- Chapitre 4 (suite) — Notation CBM ---------- */
    {
      id: 'Q11', chapitre: 4, difficulte: 'rouge',
      enonce: {
        fr: 'Dans la notation CBM de ce QCM, une réponse FAUSSE donnée en certitude « Élevée » rapporte…',
        en: 'In this quiz\'s CBM scoring, a WRONG answer given with "High" certainty earns…'
      },
      propositions: [
        { fr: '0 point (réponse simplement ignorée)', en: '0 points (the answer is simply ignored)' },
        { fr: '+3 points car vous aviez osé répondre', en: '+3 points because you dared to answer' },
        { fr: '−3 points (pénalité maximale du barème)', en: '−3 points (the scale\'s maximum penalty)' },
        { fr: '−1 point quelle que soit la certitude choisie', en: '−1 point regardless of the certainty chosen' }
      ]
    },
    /* ---------- Chapitre 1 (suite) — Cadrer (public cible) ---------- */
    {
      id: 'Q12', chapitre: 1, difficulte: 'rouge',
      enonce: {
        fr: 'Définir le « public cible » d\'un cours en amont sert avant tout à…',
        en: 'Defining a course\'s "target audience" upfront serves above all to…'
      },
      propositions: [
        { fr: 'gonfler artificiellement le nombre d\'inscrits annoncé', en: 'artificially inflate the announced enrolment figures' },
        { fr: 'choisir aléatoirement les couleurs de l\'interface', en: 'randomly choose the interface colours' },
        { fr: 'rallonger systématiquement la durée du cours', en: 'systematically lengthen the course duration' },
        { fr: 'adapter le niveau, le ton et les exemples aux apprenants', en: 'tailor the level, tone and examples to the learners' }
      ]
    }
  ]
};
