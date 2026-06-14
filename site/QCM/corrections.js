/* =================================================================
   corrections.js — Clé de correction BILINGUE (FR/EN) du QCM-démo
   Thème : « Concevoir un cours en ligne » (5 chapitres)
   Template de cours — M. EL AFRIT (CC BY-NC-SA 4.0)

   Format attendu par les pages (entrainement / correction / dashboard) :
     { id, chapitre, difficulte, bonne_reponse_index, explication:{fr,en} }
   bonne_reponse_index : index (0..3) de la bonne proposition dans questions.js.
   Équilibre des index : 3×0 (A), 3×1 (B), 3×2 (C), 3×3 (D).
   ================================================================= */
window.QCM_CORRECTIONS = {
  corrections: [
    {
      id: 'Q01', chapitre: 1, difficulte: 'vert', bonne_reponse_index: 0,
      explication: {
        fr: 'On part toujours des objectifs pédagogiques : ce que l\'apprenant devra savoir faire. Le reste (thème, formats, plateforme) en découle.',
        en: 'You always start from the learning objectives: what the learner must be able to do. Everything else (theme, formats, platform) follows from them.'
      }
    },
    {
      id: 'Q02', chapitre: 1, difficulte: 'jaune', bonne_reponse_index: 1,
      explication: {
        fr: 'Un objectif s\'exprime avec un verbe d\'action observable et mesurable (ex. « identifier », « calculer »), pour qu\'on puisse vérifier s\'il est atteint.',
        en: 'An objective is written with an observable, measurable action verb (e.g. "identify", "calculate"), so its attainment can be checked.'
      }
    },
    {
      id: 'Q03', chapitre: 2, difficulte: 'vert', bonne_reponse_index: 2,
      explication: {
        fr: 'Le découpage en modules et séquences rend la progression claire et gérable : l\'apprenant avance par étapes courtes et repérables.',
        en: 'Splitting into modules and units makes progression clear and manageable: the learner advances in short, trackable steps.'
      }
    },
    {
      id: 'Q04', chapitre: 2, difficulte: 'orange', bonne_reponse_index: 3,
      explication: {
        fr: 'L\'alignement pédagogique (Biggs) vise la cohérence entre objectifs, activités d\'apprentissage et évaluations : les trois doivent se répondre.',
        en: 'Constructive alignment (Biggs) seeks consistency between objectives, learning activities and assessments: all three must match.'
      }
    },
    {
      id: 'Q05', chapitre: 3, difficulte: 'jaune', bonne_reponse_index: 0,
      explication: {
        fr: 'Le principe de redondance déconseille de lire à voix haute un texte déjà affiché mot pour mot : cela surcharge la mémoire de travail.',
        en: 'The redundancy principle warns against reading aloud text already shown word-for-word: it overloads working memory.'
      }
    },
    {
      id: 'Q06', chapitre: 3, difficulte: 'orange', bonne_reponse_index: 1,
      explication: {
        fr: 'Un fichier .srt / .vtt séparé reste éditable, traduisible et activable/désactivable, contrairement à un texte incrusté dans l\'image.',
        en: 'A separate .srt / .vtt file stays editable, translatable and toggleable, unlike text burned into the image.'
      }
    },
    {
      id: 'Q07', chapitre: 4, difficulte: 'vert', bonne_reponse_index: 2,
      explication: {
        fr: 'L\'évaluation formative sert à donner un retour en cours d\'apprentissage pour aider l\'apprenant à progresser, sans enjeu de note finale.',
        en: 'Formative assessment provides feedback during learning to help the learner improve, with no final-grade stakes.'
      }
    },
    {
      id: 'Q08', chapitre: 4, difficulte: 'rouge', bonne_reponse_index: 3,
      explication: {
        fr: 'Un bon distracteur est plausible et reflète une erreur fréquente. Jouer sur la longueur (toujours plus court/long) est un biais à éviter.',
        en: 'A good distractor is plausible and reflects a common misconception. Relying on length (always shorter/longer) is a bias to avoid.'
      }
    },
    {
      id: 'Q09', chapitre: 5, difficulte: 'jaune', bonne_reponse_index: 0,
      explication: {
        fr: 'L\'attribut alt fournit l\'alternative textuelle restituée par les lecteurs d\'écran ; title ne suffit pas et n\'est pas fiable pour cet usage.',
        en: 'The alt attribute provides the text alternative read out by screen readers; title alone is not sufficient nor reliable for this purpose.'
      }
    },
    {
      id: 'Q10', chapitre: 5, difficulte: 'orange', bonne_reponse_index: 1,
      explication: {
        fr: 'WCAG 2.1 niveau AA exige un contraste d\'au moins 4,5:1 pour le texte normal (3:1 pour le grand texte).',
        en: 'WCAG 2.1 level AA requires a contrast of at least 4.5:1 for normal text (3:1 for large text).'
      }
    },
    {
      id: 'Q11', chapitre: 4, difficulte: 'rouge', bonne_reponse_index: 2,
      explication: {
        fr: 'Barème CBM : en certitude Élevée, une bonne réponse vaut +3 mais une mauvaise coûte −3. C\'est tout l\'intérêt : ne déclarez « Élevée » que si vous êtes sûr.',
        en: 'CBM scale: at High certainty a correct answer is worth +3 but a wrong one costs −3. That is the point: only declare "High" when you are sure.'
      }
    },
    {
      id: 'Q12', chapitre: 1, difficulte: 'rouge', bonne_reponse_index: 3,
      explication: {
        fr: 'Connaître le public cible permet d\'adapter le niveau, le ton et les exemples : un même contenu ne se conçoit pas pareil pour des débutants ou des experts.',
        en: 'Knowing the target audience lets you tailor the level, tone and examples: the same content is not designed the same way for beginners or experts.'
      }
    }
  ]
};
