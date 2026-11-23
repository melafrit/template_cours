/* =================================================================
   glossaire-data.js · Données du glossaire BILINGUE (à personnaliser)
   Structure : { fr, en, ar, def:{fr,en,ar}, ex:{fr,en,ar}, alias:{ar:[…]} }
   (terme, définition et exemple dans chaque langue) ; alias donne les
   autres formes d'un terme dans une langue (glossaire-tooltip.js).
   Template de site de cours · Mohamed EL AFRIT (MIT / CC BY 4.0)
   ================================================================= */
window.GLOSSARY = [
  { fr: "objectif pédagogique", en: "learning objective", ar: "الهدف البيداغوجي",
    def: { fr: "Ce que l'apprenant doit être capable de FAIRE à la fin d'une séquence, formulé avec un verbe d'action observable.",
           en: "What the learner should be able to DO at the end of a sequence, written with an observable action verb.",
           ar: "ما ينبغي أن يكون المتعلّم قادرًا على فعله في نهاية وحدة تعلّمية، مصوغًا بفعل إجرائي قابل للملاحظة." },
    ex: { fr: "« À la fin du chapitre, l'apprenant rédige un objectif pédagogique mesurable. »",
          en: "\"By the end of the chapter, the learner writes a measurable learning objective.\"",
          ar: "«في نهاية الفصل، يصوغ المتعلّم هدفًا بيداغوجيًا قابلًا للقياس.»" }, alias: { ar: ["الأهداف البيداغوجية", "هدف بيداغوجي"] } },
  { fr: "public cible", en: "target audience", ar: "الفئة المستهدفة",
    def: { fr: "Le groupe d'apprenants visé, avec ses prérequis, son niveau et ses contraintes.",
           en: "The intended group of learners, with their prerequisites, level and constraints.",
           ar: "مجموعة المتعلّمين المقصودة، بمكتسباتها القبلية ومستواها وقيودها." },
    ex: { fr: "Étudiants de master débutants en pédagogie numérique.",
          en: "Master's students new to digital pedagogy.",
          ar: "طلبة ماستر مبتدئون في البيداغوجيا الرقمية." } },
  { fr: "syllabus", en: "syllabus", ar: "توصيف المقرّر",
    def: { fr: "Le plan détaillé du cours : chapitres, objectifs, durées et évaluation.",
           en: "The detailed course plan: chapters, objectives, durations and assessment.",
           ar: "الخطة المفصّلة للمقرّر: الفصول والأهداف والمدد والتقييم." },
    ex: { fr: "Le syllabus liste cinq chapitres et un atelier final.",
          en: "The syllabus lists five chapters and a final workshop.",
          ar: "يذكر توصيف المقرّر خمسة فصول وورشة ختامية." } },
  { fr: "fil rouge", en: "through-line", ar: "المشروع التطبيقي",
    def: { fr: "Un scénario ou projet continu qui traverse tout le cours et donne du sens aux chapitres.",
           en: "A continuous scenario or project that runs through the whole course and connects the chapters.",
           ar: "سيناريو أو مشروع متواصل يرافق المقرّر كلّه ويمنح الفصول معناها." },
    ex: { fr: "Le fil rouge : concevoir, pas à pas, son propre cours en ligne.",
          en: "The through-line: building your own online course, step by step.",
          ar: "المشروع التطبيقي: تصميم مقرّركم الإلكتروني خطوة خطوة." } },
  { fr: "prérequis", en: "prerequisites", ar: "المكتسبات القبلية",
    def: { fr: "Les connaissances ou compétences supposées acquises avant de commencer.",
           en: "The knowledge or skills assumed before starting.",
           ar: "المعارف أو المهارات التي يُفترض اكتسابها قبل البدء." },
    ex: { fr: "Prérequis : savoir éditer un document texte.",
          en: "Prerequisite: being able to edit a text document.",
          ar: "المكتسبات القبلية: القدرة على تحرير مستند نصي." } },
  { fr: "accroche", en: "hook", ar: "المدخل التحفيزي",
    def: { fr: "Une introduction brève qui motive l'apprenant en montrant l'utilité du chapitre.",
           en: "A short opening that motivates the learner by showing why the chapter matters.",
           ar: "مقدّمة قصيرة تحفّز المتعلّم بإبراز فائدة الفصل." },
    ex: { fr: "Une accroche par une question concrète ou un cas réel.",
          en: "A hook using a concrete question or a real case.",
          ar: "مدخل تحفيزي بسؤال ملموس أو بحالة واقعية." } },
  { fr: "évaluation formative", en: "formative assessment", ar: "التقويم التكويني",
    def: { fr: "Une évaluation en cours d'apprentissage, destinée à donner du feedback, pas à noter.",
           en: "Assessment during learning, meant to give feedback rather than a grade.",
           ar: "تقييم أثناء التعلّم، غايته تقديم التغذية الراجعة لا وضع علامة." },
    ex: { fr: "Un quiz d'entraînement avec correction immédiate.",
          en: "A practice quiz with immediate feedback.",
          ar: "اختبار تدريبي مع تصحيح فوري." } },
  { fr: "évaluation sommative", en: "summative assessment", ar: "التقويم الإجمالي",
    def: { fr: "Une évaluation finale qui mesure et certifie les acquis.",
           en: "A final assessment that measures and certifies learning.",
           ar: "تقييم ختامي يقيس المكتسبات ويُثبتها." },
    ex: { fr: "Le QCM noté de fin de cours.",
          en: "The graded end-of-course quiz.",
          ar: "اختبار الاختيار من متعدّد المنقَّط في نهاية المقرّر." } },
  { fr: "QCM", en: "multiple-choice quiz", ar: "اختبار الاختيار من متعدّد",
    def: { fr: "Questionnaire à choix multiples ; ici noté par degré de certitude (CBM).",
           en: "A multiple-choice questionnaire; here graded by degree of certainty (CBM).",
           ar: "استبيان بأسئلة متعدّدة الاختيارات، يُنقَّط هنا حسب درجة اليقين (CBM)." },
    ex: { fr: "Le QCM propose quatre réponses et une seule est correcte.",
          en: "The quiz offers four answers and only one is correct.",
          ar: "يقترح الاختبار أربع إجابات، واحدة منها فقط صحيحة." } },
  { fr: "flashcard", en: "flashcard", ar: "بطاقة المراجعة",
    def: { fr: "Une carte recto-verso de révision active (question d'un côté, réponse de l'autre).",
           en: "A two-sided active-recall card (question on one side, answer on the other).",
           ar: "بطاقة ذات وجهين للمراجعة النشطة: سؤال على وجه، وجواب على الآخر." },
    ex: { fr: "Réviser les définitions clés avec des flashcards.",
          en: "Reviewing key definitions with flashcards.",
          ar: "مراجعة التعريفات الأساسية ببطاقات المراجعة." }, alias: { ar: ["بطاقات المراجعة"] } },
  { fr: "accessibilité", en: "accessibility", ar: "إمكانية الوصول",
    def: { fr: "La capacité d'un contenu à être utilisé par tous, y compris en situation de handicap.",
           en: "The ability of content to be used by everyone, including people with disabilities.",
           ar: "قدرة المحتوى على أن يستعمله الجميع، بمن فيهم ذوو الإعاقة." },
    ex: { fr: "Contraste suffisant, navigation au clavier, police lisible.",
          en: "Sufficient contrast, keyboard navigation, readable font.",
          ar: "تباين كافٍ، وتنقّل بلوحة المفاتيح، وخطّ مقروء." } },
  { fr: "micro-apprentissage", en: "microlearning", ar: "التعلّم المصغّر",
    def: { fr: "Découper le contenu en petites unités courtes et autonomes.",
           en: "Breaking content into short, self-contained units.",
           ar: "تقسيم المحتوى إلى وحدات صغيرة قصيرة ومستقلّة." },
    ex: { fr: "Des sections de 5 minutes plutôt qu'un long bloc.",
          en: "Five-minute sections rather than one long block.",
          ar: "أقسام من 5 دقائق بدل كتلة طويلة واحدة." } }
];

/* -----------------------------------------------------------------
   Termes rendus interactifs dans les chapitres

   glossaire-tooltip.js survole le texte des sections et pose une
   info-bulle sur ces termes-là uniquement. On ne met pas tout le
   glossaire : au-delà d'une quinzaine de termes par chapitre, la page
   se couvre de pointillés et plus personne ne clique.

   Choisissez les notions distinctives, celles dont la définition change
   la compréhension du passage. Les mots courants n'ont rien à faire ici.

   La recherche porte sur le mot entier, dans la forme écrite ici : un
   pluriel employé par les pages s'y ajoute (« objectifs pédagogiques »),
   et GLOSSARY_ALIASES le rattache à son entrée. Une page anglaise trouve
   seule le pluriel régulier et les formes de alias.en.
   ----------------------------------------------------------------- */
window.GLOSSARY_CURATED = [
  "objectif pédagogique", "public cible", "syllabus",
  "fil rouge", "prérequis", "accroche",
  "évaluation formative", "évaluation sommative", "flashcard",
  "accessibilité", "micro-apprentissage",
  "objectifs pédagogiques", "évaluations formatives", "évaluations sommatives", "flashcards"
];

/* Variantes d'écriture qui doivent pointer vers la même entrée : pluriels,
   synonymes, formes abrégées. Une variante n'a d'info-bulle que si elle
   figure aussi dans GLOSSARY_CURATED, qui dit quelles formes chercher ;
   cette table dit à quelle entrée chacune renvoie. */
window.GLOSSARY_ALIASES = {
  "objectifs pédagogiques": "objectif pédagogique",
  "évaluations formatives": "évaluation formative",
  "évaluations sommatives": "évaluation sommative",
  "flashcards": "flashcard"
};
