/* =================================================================
   questions.js — Banque de questions BILINGUE (FR/EN) du QCM-démo
   Thème : « Concevoir un cours en ligne » (3 chapitres)
   Template de site de cours — Mohamed EL AFRIT (MIT / CC BY 4.0)

   Format attendu par les pages (index / entrainement / correction / dashboard) :
     { id, chapitre, difficulte, enonce:{fr,en}, propositions:[{fr,en}×4] }
   Réponse UNIQUE par question. Voir corrections.js pour la clé + explications.

   RÈGLES QUE CE FICHIER RESPECTE, ET QU'IL FAUT TENIR EN L'ÉTENDANT :

   - Chaque question porte sur ce que le chapitre enseigne RÉELLEMENT. Une
     question dont la réponse n'est pas dans le cours est injuste, et l'on ne
     s'en aperçoit qu'à la correction, quand toute la promotion se trompe.
   - Les positions des bonnes réponses sont ÉQUILIBRÉES. Ici : 2×A, 3×B, 2×C,
     2×D. Sans cela, l'étudiant qui coche toujours la même lettre est avantagé.
   - Les distracteurs sont plausibles, jamais absurdes. Une proposition
     manifestement fausse ne teste rien : elle réduit le QCM à trois choix.
   - Difficulté : vert (tout étudiant ayant lu doit répondre), jaune, orange,
     rouge (départage le haut du classement).
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
    nombre_questions: 9,
    note_sur: 20
  },
  questions: [

    /* ---------- Chapitre 1 — Cadrer son cours ---------- */
    {
      id: 'Q01', chapitre: 1, difficulte: 'vert',
      enonce: {
        fr: 'Parmi les trois décisions de cadrage, laquelle se prend en premier ?',
        en: 'Of the three scoping decisions, which one comes first?'
      },
      propositions: [
        { fr: 'Choisir le fil rouge, pour donner sa cohérence au cours', en: 'Choosing the through-line, to hold the course together' },
        { fr: 'Définir le public cible, avec ses prérequis et ses contraintes', en: 'Defining the target audience, with its prerequisites and constraints' },
        { fr: 'Rédiger les objectifs pédagogiques', en: 'Writing the learning objectives' },
        { fr: 'Fixer le nombre de chapitres et leur durée', en: 'Setting the number of chapters and their duration' }
      ]
    },
    {
      id: 'Q02', chapitre: 1, difficulte: 'jaune',
      enonce: {
        fr: 'Quelle description d\'un public cible permet réellement de prendre des décisions ?',
        en: 'Which description of a target audience actually supports decisions?'
      },
      propositions: [
        { fr: 'Des étudiants de deuxième année de master', en: 'Second-year master\'s students' },
        { fr: 'Un public motivé, curieux et disponible', en: 'A motivated, curious and available audience' },
        { fr: 'Des professionnels sans bagage technique, deux heures par semaine, souvent sur téléphone', en: 'Professionals with no technical background, two hours a week, often on a phone' },
        { fr: 'Un public hétérogène, aux profils variés', en: 'A heterogeneous audience, with varied profiles' }
      ]
    },
    {
      id: 'Q03', chapitre: 1, difficulte: 'orange',
      enonce: {
        fr: 'À quelle condition un objectif pédagogique est-il vérifiable ?',
        en: 'Under what condition is a learning objective verifiable?'
      },
      propositions: [
        { fr: 'On peut décrire l\'exercice qui prouverait qu\'il est atteint', en: 'You can describe the exercise that would prove it reached' },
        { fr: 'Il porte sur une notion importante du programme', en: 'It covers an important notion of the syllabus' },
        { fr: 'Il est formulé en une seule phrase', en: 'It is written in a single sentence' },
        { fr: 'Il commence par un verbe, quel qu\'il soit', en: 'It starts with a verb, whichever one' }
      ]
    },

    /* ---------- Chapitre 2 — Structurer le contenu ---------- */
    {
      id: 'Q04', chapitre: 2, difficulte: 'jaune',
      enonce: {
        fr: 'Une séquence de cours porte trois éléments. Lequel manque le plus souvent ?',
        en: 'A course sequence carries three parts. Which one is most often missing?'
      },
      propositions: [
        { fr: 'La question qui la motive', en: 'The question that motivates it' },
        { fr: 'Le contenu qui y répond', en: 'The content that answers it' },
        { fr: 'Le titre de la séquence', en: 'The title of the sequence' },
        { fr: 'La vérification qui prouve qu\'elle a porté', en: 'The check that proves it landed' }
      ]
    },
    {
      id: 'Q05', chapitre: 2, difficulte: 'vert',
      enonce: {
        fr: 'Qu\'est-ce qui distingue le micro-apprentissage d\'un chapitre simplement découpé ?',
        en: 'What distinguishes micro-learning from a chapter merely sliced up?'
      },
      propositions: [
        { fr: 'La durée : moins de dix minutes par séquence', en: 'Duration: under ten minutes per sequence' },
        { fr: 'L\'autonomie : la séquence se suffit à elle-même', en: 'Autonomy: the sequence stands on its own' },
        { fr: 'Le support : la séquence se lit sur téléphone', en: 'The device: the sequence can be read on a phone' },
        { fr: 'Le format : la séquence est en vidéo plutôt qu\'en texte', en: 'The format: the sequence is video rather than text' }
      ]
    },
    {
      id: 'Q06', chapitre: 2, difficulte: 'orange',
      enonce: {
        fr: 'Sur quel critère faut-il ordonner les notions d\'un cours ?',
        en: 'On what criterion should the notions of a course be ordered?'
      },
      propositions: [
        { fr: 'Leur importance : on commence par ce qui compte le plus', en: 'Their importance: start with what matters most' },
        { fr: 'Leur difficulté : de la plus simple à la plus complexe', en: 'Their difficulty: from simplest to most complex' },
        { fr: 'Leurs prérequis : on commence par ce qui rend le reste possible', en: 'Their prerequisites: start with what makes the rest possible' },
        { fr: 'Leur ordre chronologique dans la discipline', en: 'Their chronological order within the discipline' }
      ]
    },

    /* ---------- Chapitre 3 — Créer les ressources ---------- */
    {
      id: 'Q07', chapitre: 3, difficulte: 'vert',
      enonce: {
        fr: 'Vous devez transmettre une durée de conservation exacte — quinze minutes. Quel format choisir ?',
        en: 'You must convey an exact retention period — fifteen minutes. Which format should you choose?'
      },
      propositions: [
        { fr: 'Le texte : un chiffre exact doit pouvoir être relu', en: 'Text: an exact figure must be re-readable' },
        { fr: 'Une capsule audio : la voix retient l\'attention', en: 'An audio capsule: a voice holds attention' },
        { fr: 'Un schéma : la représentation visuelle marque mieux', en: 'A diagram: a visual representation sticks better' },
        { fr: 'Les trois à la fois, pour maximiser la mémorisation', en: 'All three at once, to maximise retention' }
      ]
    },
    {
      id: 'Q08', chapitre: 3, difficulte: 'jaune',
      enonce: {
        fr: 'Qu\'attend-on d\'un schéma placé à côté d\'un paragraphe ?',
        en: 'What is expected of a diagram placed beside a paragraph?'
      },
      propositions: [
        { fr: 'Qu\'il résume le paragraphe, pour qui ne le lira pas', en: 'That it summarises the paragraph, for those who will not read it' },
        { fr: 'Qu\'il montre ce que le texte ne peut pas dire : un ordre, une proportion, un flux', en: 'That it shows what text cannot say: an order, a proportion, a flow' },
        { fr: 'Qu\'il illustre le propos par une image agréable', en: 'That it illustrates the point with a pleasant image' },
        { fr: 'Qu\'il reprenne les mêmes termes que le texte, pour la cohérence', en: 'That it reuses the same terms as the text, for consistency' }
      ]
    },
    {
      id: 'Q09', chapitre: 3, difficulte: 'rouge',
      enonce: {
        fr: 'Quelle affirmation décrit le mieux l\'apport d\'une transcription sous une capsule audio ?',
        en: 'Which statement best describes what a transcript under an audio capsule brings?'
      },
      propositions: [
        { fr: 'Elle satisfait une obligation réglementaire d\'accessibilité', en: 'It satisfies a regulatory accessibility requirement' },
        { fr: 'Elle sert aux personnes sourdes, et à elles seules', en: 'It serves deaf people, and only them' },
        { fr: 'Elle remplace la capsule pour qui préfère lire', en: 'It replaces the capsule for those who prefer reading' },
        { fr: 'Elle rend la ressource utilisable dans plus de situations, pour tout le monde', en: 'It makes the resource usable in more situations, for everyone' }
      ]
    }
  ]
};
