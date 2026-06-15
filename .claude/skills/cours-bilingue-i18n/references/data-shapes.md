# Formes exactes des données bilingues

Les fichiers de données ne contiennent **pas** de HTML jumelé : ils portent des **objets
`{ fr, en }`** que les moteurs résolvent à l'affichage via le helper `L()`. Chaque global est
déclaré sous la forme `window.XXX = …` et lu par un moteur dédié.

**Règle d'or.** Tout champ **affiché à l'utilisateur** est un objet `{ fr, en }` (les deux clés
présentes). Tout champ **technique** (id, fichier, index, ancre, icône, href, ref) reste une
**chaîne neutre**. En cas de doute : si le texte change à la bascule de langue, il est bilingue.

---

## `window.COURSE` — `assets/js/course-data.js`
Source unique de vérité de la navigation, lue **partout** (arbre de nav, progression, compteur).

```js
window.COURSE = {
  title:    { fr: "Concevoir un cours en ligne", en: "Designing an online course" },
  subtitle: { fr: "Sous-titre…",                 en: "Subtitle…" },
  author:   "Mohamed EL AFRIT",                  // neutre
  license:  { fr: "CC BY 4.0",                    en: "CC BY 4.0" },
  chapters: [
    { num: '1', ico: '🎯', file: '01-cadrage.html',   // num/ico/file = neutres
      title: { fr: "Cadrer son cours", en: "Scoping your course" } }
  ],
  resources: [
    { ico: '📚', href: 'glossaire.html',              // ico/href = neutres
      label: { fr: "Glossaire bilingue", en: "Bilingual glossary" } }
  ]
};
```
Bilingues : `title`, `subtitle`, `license`, `chapters[].title`, `resources[].label`.
Neutres : `author`, `chapters[].num/ico/file`, `resources[].ico/href`.

---

## `window.RDC_SECTIONS` — `assets/js/nav-sections.js`
Sous-sections (ancres) par chapitre, pour le sous-menu pliable de la sidebar. **Une entrée par
`<h2 id>` réel** du chapitre ; `id` = l'ancre, `t` = le titre bilingue.

```js
window.RDC_SECTIONS = {
  "1": [
    { id: "ch1-s1", t: { fr: "1. Pourquoi cadrer avant de produire",
                         en: "1. Why scope before producing" } },
    { id: "ch1-s2", t: { fr: "2. …", en: "2. …" } }
  ]
};
```
Bilingue : `t`. Neutre : `id` (ancre `#chN-sM`).

---

## `window.GLOSSARY` — `assets/js/glossaire-data.js`
Tableau de termes. Ici `fr`/`en` portent **le terme lui-même** dans chaque langue ; `def`/`ex` sont
eux-mêmes des objets `{ fr, en }`.

```js
window.GLOSSARY = [
  { fr: "objectif pédagogique", en: "learning objective",
    def: { fr: "Ce que l'apprenant doit être capable de FAIRE à la fin…",
           en: "What the learner should be able to DO at the end…" },
    ex:  { fr: "« À la fin du chapitre, l'apprenant rédige… »",
           en: "\"By the end of the chapter, the learner writes…\"" } }
];
```
Bilingues : `def`, `ex` (chacun `{fr,en}`). Particularité : `fr` / `en` = le terme dans chaque langue.

---

## `window.RDC_FLASHCARDS` — `assets/js/flashcards-data.js`
Cartes de révision par chapitre. `front`/`back` bilingues (le `back` accepte `**gras**`, interprété
par `flashcards.js`, **pas** de HTML) ; `ref` = chaîne neutre (ex. `"art. 5"`).

```js
window.RDC_FLASHCARDS = {
  "1": [
    { front: { fr: "Qu'est-ce qu'un objectif pédagogique ?",
               en: "What is a learning objective?" },
      back:  { fr: "Ce que l'apprenant doit savoir **faire** à la fin…",
               en: "What the learner must be able to **do** at the end…" },
      ref: "" }
  ]
};
```
Bilingues : `front`, `back`. Neutre : `ref`.

---

## `window.QCM_QUESTIONS` — `QCM/questions.js`
Banque de questions. `enonce` et chaque `propositions[]` (4 par convention) sont bilingues, ainsi
que `meta.titre` / `meta.formation`.

```js
window.QCM_QUESTIONS = {
  meta: { titre: { fr: "QCM", en: "Quiz" }, formation: { fr: "…", en: "…" },
          auteur: "Mohamed EL AFRIT", annee_academique: "2025-2026", nombre_questions: 60 },
  questions: [
    { id: 'Q01', chapitre: 1, difficulte: 'vert',         // id/chapitre/difficulte = neutres
      enonce: { fr: 'Quel est le tout premier élément à définir…',
                en: 'What is the very first element to define…' },
      propositions: [
        { fr: 'Les objectifs pédagogiques visés', en: 'The intended learning objectives' },
        { fr: 'La couleur du thème graphique',     en: 'The colour of the visual theme' },
        { fr: '…', en: '…' },
        { fr: '…', en: '…' }
      ] }
  ]
};
```
Bilingues : `enonce`, chaque `propositions[]`, `meta.titre`, `meta.formation`.
Neutres : `id`, `chapitre`, `difficulte`, `meta.auteur`, `meta.annee_academique`, `meta.nombre_questions`.

---

## `window.QCM_CORRECTIONS` — `QCM/corrections.js`
Clé de correction, **appariée par `id`** à `questions.js`. La bonne réponse est un **index** (0..3),
l'explication est bilingue.

```js
window.QCM_CORRECTIONS = {
  corrections: [
    { id: 'Q01', chapitre: 1, difficulte: 'vert', bonne_reponse_index: 0,
      explication: { fr: 'On part toujours des objectifs pédagogiques…',
                     en: 'You always start from the learning objectives…' } }
  ]
};
```
Bilingue : `explication`. Neutres : `id`, `chapitre`, `difficulte`, `bonne_reponse_index`.

---

## Sources uniques de vérité (à ne jamais désynchroniser)
- **`course-data.js` pilote la navigation partout** : arbre de nav, barre de progression, compteur
  `x/total`. C'est le seul endroit où déclarer un chapitre.
- **`nav-sections.js` doit refléter les `<h2 id>` réels** de chaque chapitre : chaque `id` de
  section doit correspondre **exactement** à une ancre `<h2 id="chN-sM">` de la page, sinon le
  sous-menu pointe dans le vide.
- **Les `id` de questions (`Q01`…) doivent correspondre** entre `questions.js` et `corrections.js` :
  une question = deux entrées synchronisées par le même `id`. Le nombre et l'ordre des questions
  entrent dans la signature SHA-256 des CSV : figez la banque pendant une session d'examen.

> Template de site de cours — **Mohamed EL AFRIT** · code MIT, contenu & prompts CC BY 4.0.
