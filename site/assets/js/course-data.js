/* =================================================================
   course-data.js — Données du cours (source unique de vérité)
   À PERSONNALISER pour votre propre cours. Titres/libellés bilingues { fr, en }.
   Template de site de cours — Mohamed EL AFRIT (MIT / CC BY 4.0)
   ================================================================= */
window.COURSE = {
  title: { fr: "Concevoir un cours en ligne", en: "Designing an online course", ar: "تصميم مقرّر إلكتروني" },
  subtitle: {
    fr: "Un cours-démo qui enseigne comment fabriquer un cours en ligne efficace, en utilisant les fonctionnalités qu'il démontre.",
    en: "A demo course that teaches how to build an effective online course, using the very features it showcases.",
    ar: "مقرّر تجريبي يعلّم كيف يُصنع مقرّر إلكتروني فعّال، مستعملًا الوظائف نفسها التي يعرضها."
  },
  author: "Mohamed EL AFRIT",
  license: { fr: "Code MIT · Contenu CC BY 4.0", en: "Code MIT · Content CC BY 4.0", ar: "الشيفرة MIT · المحتوى CC BY 4.0" },
  chapters: [
    { num: '1', ico: '🎯', file: '01-cadrage.html',
      title: { fr: "Cadrer son cours", en: "Scoping your course", ar: "تأطير المقرّر" } },
    { num: '2', ico: '🧱', file: '02-structurer.html',
      title: { fr: "Structurer le contenu", en: "Structuring the content", ar: "هيكلة المحتوى" } },
    { num: '3', ico: '🎬', file: '03-multimedia.html',
      title: { fr: "Créer les ressources", en: "Creating the resources", ar: "إنشاء الموارد" } }
  ],
  resources: [
    { ico: '📘', href: 'polycopie.html',    label: { fr: "Polycopié", en: "Course book", ar: "المطبوعة" } },
    { ico: '📄', href: 'polycopies.html',
      label: { fr: "Fiches de synthèse", en: "Summary sheets", ar: "البطاقات التلخيصية" } },
    { ico: '🎙️', href: 'podcasts.html',     label: { fr: "Podcasts", en: "Podcasts", ar: "البودكاست" } },
    { ico: '📚', href: 'glossaire.html',   label: { fr: "Glossaire bilingue", en: "Bilingual glossary", ar: "مسرد المصطلحات" } },
    { ico: '🧩', href: 'activites.html',     label: { fr: "Activités interactives", en: "Interactive activities", ar: "الأنشطة التفاعلية" } },
    { ico: '📝', href: 'QCM/index.html',     label: { fr: "QCM d'évaluation", en: "Assessment quiz", ar: "اختبار الاختيار من متعدّد" } },
    { ico: '🧵', href: 'atelier.html',       label: { fr: "Atelier fil rouge", en: "Capstone workshop", ar: "ورشة المشروع التطبيقي" } }
  ]
};
