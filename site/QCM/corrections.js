/* =================================================================
   corrections.js — Clé de correction BILINGUE (FR/EN) du QCM-démo
   Thème : « Concevoir un cours en ligne » (3 chapitres)
   Template de site de cours — Mohamed EL AFRIT (MIT / CC BY 4.0)

   Format attendu par les pages (entrainement / correction / dashboard) :
     { id, chapitre, difficulte, bonne_reponse_index, explication:{fr,en} }
   bonne_reponse_index : index (0..3) de la bonne proposition dans questions.js.

   Équilibre des positions : 2×A (0), 3×B (1), 2×C (2), 2×D (3).

   L'EXPLICATION EST LA PARTIE UTILE. Une correction qui se contente de
   désigner la bonne réponse n'apprend rien : elle confirme ou elle infirme.
   Ce qu'il faut écrire, c'est pourquoi les autres propositions étaient
   crédibles et où le raisonnement dérape — c'est là que l'étudiant se corrige.

   Les identifiants doivent CORRESPONDRE à ceux de questions.js.
   ================================================================= */
window.QCM_CORRECTIONS = {
  corrections: [

    {
      id: 'Q01', chapitre: 1, difficulte: 'vert', bonne_reponse_index: 1,
      explication: {
        fr: 'Le public. Tant qu\'on ignore qui apprend, on ne peut ni fixer un objectif atteignable, ni juger si un fil rouge parlera. Les deux autres décisions viennent ensuite — et elles se prennent mieux. C\'est contre-intuitif : la tentation est de commencer par les objectifs, qui semblent plus « sérieux ».',
        en: 'The audience. Until you know who is learning, you can neither set a reachable objective nor judge whether a through-line will land. The other two decisions come next — and they come out better. It is counter-intuitive: the temptation is to start with objectives, which feel more "serious".'
      }
    },
    {
      id: 'Q02', chapitre: 1, difficulte: 'jaune', bonne_reponse_index: 2,
      explication: {
        fr: 'Seule cette description donne des prérequis, un temps disponible et une contrainte matérielle — trois informations dont on peut déduire la longueur des séquences et le format des ressources. « Master 2 », « motivé », « hétérogène » ne permettent aucune décision : ce sont des étiquettes, pas des contraintes.',
        en: 'Only this description gives prerequisites, available time and a practical constraint — three facts from which sequence length and resource format can be inferred. "Master\'s", "motivated", "heterogeneous" support no decision at all: they are labels, not constraints.'
      }
    },
    {
      id: 'Q03', chapitre: 1, difficulte: 'orange', bonne_reponse_index: 0,
      explication: {
        fr: 'La vérifiabilité ne tient ni à l\'importance de la notion, ni à la concision, ni à la présence d\'un verbe : « comprendre » et « connaître » sont des verbes, et ne s\'observent pas. Elle tient à l\'existence d\'une preuve observable. Le test pratique : si vous ne pouvez pas décrire l\'exercice, l\'objectif est mal écrit.',
        en: 'Verifiability rests neither on the importance of the notion, nor on brevity, nor on the presence of a verb: "understand" and "know" are verbs, and cannot be observed. It rests on the existence of observable proof. The practical test: if you cannot describe the exercise, the objective is badly written.'
      }
    },

    {
      id: 'Q04', chapitre: 2, difficulte: 'jaune', bonne_reponse_index: 3,
      explication: {
        fr: 'La vérification. On écrit volontiers la question et le contenu — ce sont les parties qu\'on maîtrise. La vérification demande d\'imaginer ce qui prouverait l\'acquis, ce qui est plus difficile : c\'est donc elle qu\'on saute. Sans elle, personne ne sait si la séquence a servi, pas même l\'apprenant.',
        en: 'The check. We readily write the question and the content — those are the parts we master. The check requires imagining what would prove learning, which is harder: so it is the one we skip. Without it, nobody knows whether the sequence worked — not even the learner.'
      }
    },
    {
      id: 'Q05', chapitre: 2, difficulte: 'vert', bonne_reponse_index: 1,
      explication: {
        fr: 'Ni la durée, ni le support, ni le format ne font le micro-apprentissage : c\'est l\'autonomie de la séquence. Un chapitre coupé en tranches de cinq minutes reste un chapitre coupé. Le test : si l\'apprenant s\'arrête là, en ressort-il avec quelque chose d\'utilisable ?',
        en: 'Neither duration, nor device, nor format makes micro-learning: it is the autonomy of the sequence. A chapter sliced into five-minute pieces is still a sliced chapter. The test: if the learner stops there, do they leave with something usable?'
      }
    },
    {
      id: 'Q06', chapitre: 2, difficulte: 'orange', bonne_reponse_index: 2,
      explication: {
        fr: 'L\'ordre des prérequis. Ordonner par importance est l\'erreur la plus commune : on ouvre par ce qui compte le plus, donc par ce qui suppose tout le reste acquis. L\'ordre de difficulté s\'en rapproche mais ne s\'y confond pas : une notion peut être simple et pourtant supposer une autre notion.',
        en: 'The order of prerequisites. Ordering by importance is the most common mistake: you open with what matters most, hence with what assumes everything else. Ordering by difficulty comes close but is not the same: a notion can be simple and still assume another one.'
      }
    },

    {
      id: 'Q07', chapitre: 3, difficulte: 'vert', bonne_reponse_index: 0,
      explication: {
        fr: 'Le texte. Un chiffre exact se vérifie, se cite, se recopie — trois choses impossibles avec de l\'audio sans le réécouter, et personne ne réécoute. « Les trois à la fois » est le piège : le doublon coûte du temps de production et de l\'attention, sans rien ajouter. L\'audio aurait sa place pour dire pourquoi cette durée est si courte.',
        en: 'Text. An exact figure gets verified, quoted, copied — three things impossible with audio without listening again, and nobody listens again. "All three at once" is the trap: duplication costs production time and attention while adding nothing. Audio would have its place to say why the period is so short.'
      }
    },
    {
      id: 'Q08', chapitre: 3, difficulte: 'jaune', bonne_reponse_index: 1,
      explication: {
        fr: 'Un schéma montre ce que le texte ne peut pas dire. Celui qui résume le paragraphe, ou qui en reprend les termes, est un doublon : il occupe de la place et fatigue. Et l\'agrément visuel n\'est pas un objectif pédagogique — une image agréable qui n\'apporte pas d\'information est une image de trop.',
        en: 'A diagram shows what text cannot say. One that summarises the paragraph, or reuses its terms, is duplication: it takes space and tires the reader. And visual pleasantness is not a teaching objective — a pleasant image carrying no information is one image too many.'
      }
    },
    {
      id: 'Q09', chapitre: 3, difficulte: 'rouge', bonne_reponse_index: 3,
      explication: {
        fr: 'C\'est le point que l\'on comprend le plus tard. Une transcription sert au sourd, mais aussi au voyageur sans écouteurs, à celui qui cherche un mot précis, et au moteur de recherche. La réduire à une obligation réglementaire ou à un public unique manque l\'essentiel : l\'accessibilité élargit les usages pour tous. Elle ne remplace pas non plus la capsule — le ton et l\'intention ne se transcrivent pas.',
        en: 'This is the point people grasp last. A transcript serves the deaf person, but also the traveller without headphones, the one hunting for a specific word, and the search engine. Reducing it to a legal duty or to a single audience misses the point: accessibility widens usage for everyone. Nor does it replace the capsule — tone and intent do not transcribe.'
      }
    }
  ]
};
