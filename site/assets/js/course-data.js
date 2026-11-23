/* =================================================================
   course-data.js · Données du cours (source unique de vérité)
   À PERSONNALISER pour votre propre cours. Titres/libellés bilingues { fr, en }.
   Template de site de cours · Mohamed EL AFRIT (MIT / CC BY 4.0)
   ================================================================= */
window.COURSE = {
  title: { fr: "Concevoir un cours en ligne", en: "Designing an online course", ar: "تصميم مقرّر إلكتروني" },
  subtitle: {
    fr: "Un cours-démo qui enseigne comment fabriquer un cours en ligne efficace, en utilisant les fonctionnalités qu'il démontre.",
    en: "A demo course that teaches how to build an effective online course, using the very features it showcases.",
    ar: "مقرّر تجريبي يعلّم كيف يُصنع مقرّر إلكتروني فعّال، مستعملًا الوظائف نفسها التي يعرضها."
  },
  author: "Mohamed EL AFRIT",
  /* Les filières d'un cours commun (décision de l'auteur du 21 novembre 2026) : la bascule de filiere.js et le
     masquage du contenu propre à chacune (classes only-<id>, filieres.css généré par outils/generer_filieres.py).
     Une seule filière, ou aucune : pas de bascule. palette : celle de palettes.css que prend l'accent quand la
     filière est choisie. Intitulés et numéros RNCP : ceux du cours EADL. */
  filieres: [
    { id: 'eadl', code: 'EADL', palette: 'emeraude', rncp: '39765',
      nom: { fr: "Expert en Architecture et Développement Logiciel", en: "Expert in Software Architecture and Development",
             ar: "خبير في معمارية البرمجيات وتطويرها" },
      court: { fr: "Architecture et développement logiciel", en: "Software architecture and development",
               ar: "معمارية البرمجيات وتطويرها" } },
    { id: 'eris', code: 'ERIS', palette: 'prune', rncp: '39781',
      nom: { fr: "Expert Réseaux, Infrastructures et Sécurité", en: "Expert in Networks, Infrastructure and Security",
             ar: "خبير في الشبكات والبنى التحتية والأمن" },
      court: { fr: "Réseaux, infrastructures, sécurité", en: "Networks, infrastructure, security",
               ar: "الشبكات والبنى التحتية والأمن" } }
  ],
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
    { ico: '🧵', href: 'atelier.html',       label: { fr: "Atelier fil rouge", en: "Capstone workshop", ar: "ورشة المشروع التطبيقي" } },
    /* Une rubrique du gabarit, pas du cours : la copie publiée du générateur de prompt, dans une zone protégée par
       mot de passe (outils/publier_generateur.py). Un cours créé écrit sa propre liste. */
    { ico: '🔒', href: 'generateur/index.html', label: { fr: "Générateur de prompt", en: "Prompt generator", ar: "مولّد الموجّهات" } }
  ]
};
