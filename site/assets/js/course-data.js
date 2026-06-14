/* =================================================================
   course-data.js — Données du cours (source unique de vérité)
   À PERSONNALISER pour votre propre cours. Titres/libellés bilingues { fr, en }.
   Template de site de cours — Mohamed EL AFRIT (MIT / CC BY 4.0)
   ================================================================= */
window.COURSE = {
  title: { fr: "Concevoir un cours en ligne", en: "Designing an online course" },
  subtitle: {
    fr: "Un cours-démo qui enseigne comment fabriquer un cours en ligne efficace — en utilisant les fonctionnalités qu'il démontre.",
    en: "A demo course that teaches how to build an effective online course — using the very features it showcases."
  },
  author: "Mohamed EL AFRIT",
  license: { fr: "Code MIT · Contenu CC BY 4.0", en: "Code MIT · Content CC BY 4.0" },
  chapters: [
    { num: '1', ico: '🎯', file: '01-cadrage.html',
      title: { fr: "Cadrer son cours", en: "Scoping your course" } },
    { num: '2', ico: '🧱', file: '02-structurer.html',
      title: { fr: "Structurer le contenu", en: "Structuring the content" } },
    { num: '3', ico: '🎬', file: '03-multimedia.html',
      title: { fr: "Créer des ressources multimédias", en: "Creating multimedia resources" } },
    { num: '4', ico: '📝', file: '04-evaluer.html',
      title: { fr: "Évaluer les apprenants", en: "Assessing learners" } },
    { num: '5', ico: '♿', file: '05-accessibilite-diffusion.html',
      title: { fr: "Accessibilité & diffusion", en: "Accessibility & delivery" } }
  ],
  resources: [
    { ico: '📚', href: 'glossaire.html',    label: { fr: "Glossaire bilingue", en: "Bilingual glossary" } },
    { ico: '🧩', href: 'activites.html',     label: { fr: "Activités interactives", en: "Interactive activities" } },
    { ico: '📝', href: 'QCM/index.html',     label: { fr: "QCM d'évaluation", en: "Assessment quiz" } },
    { ico: '🧵', href: 'atelier.html',       label: { fr: "Atelier fil rouge", en: "Capstone workshop" } }
  ]
};
