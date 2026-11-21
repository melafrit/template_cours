# Capsules de l'accueil anglais · cours de démonstration

**Neuf capsules en anglais** sur la jumelle anglaise de l'accueil (`site/en/index.html`), mêmes conteneurs que
l'accueil français : la bienvenue (`voix-bienvenue`), une par filière (`voix-bienvenue-eadl`, `voix-bienvenue-eris`),
une en tête de chaque section (`voix-section-1` à `voix-section-6`). Chacune traduit le texte français validé par
l'auteur (`Capsules_accueil.md`), dans le vocabulaire anglais de la démonstration : program, through-line, workshop,
deliverables, graded quiz.

Cette fiche est la **source unique** des pistes anglaises : `outils/generer_audio.py` y lit les scripts, et
`outils/synchroniser_capsules.py` reporte les transcriptions dans le script des capsules de `en/index.html`.

## ⚠️ À lire avant de générer

- **Témoin : la capsule 1**, comme en français. Son texte est validé seul, avant les huit autres ; sa piste est
  générée seule, écoutée sur le lecteur de la page, avant la série (lot 9).
- **Modèle : Eleven v4**, la voix de l'auteur, sans accent ajouté sur les pistes anglaises (le clone a le sien ;
  `voix_id_en` pour une autre voix). « speaking slowly » dans chaque balise, comme en français.
- **Sources.** Les textes français validés, et les formulations anglaises déjà publiées : l'accueil anglais, les
  sous-titres des chapitres anglais, l'atelier anglais, la consigne du QCM et le bandeau des filières en anglais.
- **Écriture pour la voix.** Nombres en lettres ; « E.A.D.L. » et « Eris », comme dans les capsules anglaises du
  cours d'étude d'avant-projet. La transcription garde l'orthographe d'affichage (« EADL », « ERIS », « chapter 1 »).
- **Génération**, une fois le texte validé : `python outils/generer_audio.py --fichier accueil-capsule-en.mp3 --temoin`.

## 📋 Récapitulatif · les neuf fichiers

Tous dans `site/assets/media/voix/`. Les noms sont fixés : la page anglaise les appelle déjà.

| # | Conteneur | Nom exact du fichier | Affichée | État |
|---|---|---|---|---|
| 1 | `voix-bienvenue` | `accueil-capsule-en.mp3` | toujours | témoin, texte validé |
| 2 | `voix-bienvenue-eadl` | `accueil-capsule-eadl-en.mp3` | filière EADL choisie | texte validé |
| 3 | `voix-bienvenue-eris` | `accueil-capsule-eris-en.mp3` | filière ERIS choisie | texte validé |
| 4 | `voix-section-1` | `accueil-section-1-capsule-en.mp3` | « The path » | texte validé |
| 5 | `voix-section-2` | `accueil-section-2-capsule-en.mp3` | « The through-line » | texte validé |
| 6 | `voix-section-3` | `accueil-section-3-capsule-en.mp3` | « What you produce » | texte validé |
| 7 | `voix-section-4` | `accueil-section-4-capsule-en.mp3` | « Assessment » | texte validé |
| 8 | `voix-section-5` | `accueil-section-5-capsule-en.mp3` | « What this site demonstrates » | texte validé |
| 9 | `voix-section-6` | `accueil-section-6-capsule-en.mp3` | « Before you start » | texte validé |

---

## Capsule 1 · Welcome to the demo course (témoin)

- **Nom exact du fichier :** `accueil-capsule-en.mp3`
- **Emplacement exact :** `site/assets/media/voix/accueil-capsule-en.mp3` (accueil anglais, conteneur `voix-bienvenue`)
- **Durée visée :** ≈ 1 min 25 (229 mots parlés, tolérance 1 min 05 → 2 min 00)

- [x] Texte lu et validé par l'auteur (21 novembre 2026)
- [ ] Témoin écouté et validé par l'auteur
- [ ] Capsule générée, contrôlée et déposée

**▶️ Script ElevenLabs**

```
[warm, encouraging, speaking slowly] Hello, and welcome to this demo course. It teaches you how to design an online course… and it does so with the very tools it presents.

[thoughtful, speaking slowly] So you are reading a course about building one, while you build your own. That is its through-line: in the workshop, each chapter directly feeds a deliverable of your project.

[measured, speaking slowly] The path has three chapters, in the order in which a course is designed. In the first, you scope your course: for whom, to do what, and around what. In the second, you structure it, in which order and in what pieces. In the third, you create its resources, choosing the right format for each intention: a text, an audio or a diagram.

[engaged, speaking slowly] By the end of the workshop, you submit five deliverables: a scoping sheet, a plan, one fully written chapter, a quiz and a glossary. Together, they form the complete skeleton of a course ready to deliver. The graded quiz, for its part, asks you for an answer to each question… and your level of certainty.

[serious, measured, speaking slowly] This course is shared by two programs, E.A.D.L. and Eris. Some examples change with yours: until you choose, both versions are shown.

[warm, encouraging, speaking slowly] Now choose your program, at the top of the page: a presentation tailored to your track is waiting for you just below. Then open chapter one, with the workshop alongside. Let's get started!
```

**📄 Transcription affichée sur la page**

```
Hello, and welcome to this demo course. It teaches you how to design an online course, and it does so with the very tools it presents. So you are reading a course about building one, while you build your own. That is its through-line: in the workshop, each chapter directly feeds a deliverable of your project. The path has three chapters, in the order in which a course is designed. In the first, you scope your course: for whom, to do what, and around what. In the second, you structure it, in which order and in what pieces. In the third, you create its resources, choosing the right format for each intention: a text, an audio or a diagram. By the end of the workshop, you submit five deliverables: a scoping sheet, a plan, one fully written chapter, a quiz and a glossary. Together, they form the complete skeleton of a course ready to deliver. The graded quiz, for its part, asks you for an answer to each question and your level of certainty. This course is shared by two programs, EADL and ERIS. Some examples change with yours: until you choose, both versions are shown. Now choose your program, at the top of the page: a presentation tailored to your track is waiting for you just below. Then open chapter 1, with the workshop alongside. Let's get started!
```

---

## Capsule 2 · In EADL: your through-line

- **Nom exact du fichier :** `accueil-capsule-eadl-en.mp3`
- **Emplacement exact :** `site/assets/media/voix/accueil-capsule-eadl-en.mp3` (accueil anglais, conteneur `voix-bienvenue-eadl`)
- **Durée visée :** ≈ 39 s (104 mots parlés, tolérance 0 min 30 → 1 min 05)

- [x] Texte lu et validé par l'auteur (21 novembre 2026)
- [ ] Capsule générée, contrôlée et déposée

**▶️ Script ElevenLabs**

```
[warm, encouraging, speaking slowly] You have chosen E.A.D.L., the Expert in Software Architecture and Development program.

[thoughtful, speaking slowly] In this course, your program changes two things: the color of the page, and some examples. Take the through-line… in E.A.D.L., it can be an application that learners design chapter after chapter. Every architecture notion then applies to a real decision.

[measured, speaking slowly] The examples specific to Eris have faded away… you now read only those of your program. The rest of the course is shared by both.

[warm, encouraging, speaking slowly] You can change your program at any time, at the top of the page. And if you click yours again, both versions are shown once more.
```

**📄 Transcription affichée sur la page**

```
You have chosen EADL, the Expert in Software Architecture and Development program. In this course, your program changes two things: the color of the page, and some examples. Take the through-line. In EADL, it can be an application that learners design chapter after chapter. Every architecture notion then applies to a real decision. The examples specific to ERIS have faded away, and you now read only those of your program. The rest of the course is shared by both. You can change your program at any time, at the top of the page. And if you click yours again, both versions are shown once more.
```

---

## Capsule 3 · In ERIS: your through-line

- **Nom exact du fichier :** `accueil-capsule-eris-en.mp3`
- **Emplacement exact :** `site/assets/media/voix/accueil-capsule-eris-en.mp3` (accueil anglais, conteneur `voix-bienvenue-eris`)
- **Durée visée :** ≈ 41 s (109 mots parlés, tolérance 0 min 30 → 1 min 05)

- [x] Texte lu et validé par l'auteur (21 novembre 2026)
- [ ] Capsule générée, contrôlée et déposée

**▶️ Script ElevenLabs**

```
[warm, encouraging, speaking slowly] You have chosen Eris, the Expert in Networks, Infrastructure and Security program.

[thoughtful, speaking slowly] In this course, your program changes two things: the color of the page, and some examples. Take the through-line… in Eris, it can be the infrastructure of a fictional company, which learners secure chapter after chapter. Every notion then applies to a device or a rule.

[measured, speaking slowly] The examples specific to E.A.D.L. have faded away… you now read only those of your program. The rest of the course is shared by both.

[warm, encouraging, speaking slowly] You can change your program at any time, at the top of the page. And if you click yours again, both versions are shown once more.
```

**📄 Transcription affichée sur la page**

```
You have chosen ERIS, the Expert in Networks, Infrastructure and Security program. In this course, your program changes two things: the color of the page, and some examples. Take the through-line. In ERIS, it can be the infrastructure of a fictional company, which learners secure chapter after chapter. Every notion then applies to a device or a rule. The examples specific to EADL have faded away, and you now read only those of your program. The rest of the course is shared by both. You can change your program at any time, at the top of the page. And if you click yours again, both versions are shown once more.
```

---

## Capsule 4 · The path

- **Nom exact du fichier :** `accueil-section-1-capsule-en.mp3`
- **Emplacement exact :** `site/assets/media/voix/accueil-section-1-capsule-en.mp3` (accueil anglais, conteneur `voix-section-1`)
- **Durée visée :** ≈ 55 s (146 mots parlés, tolérance 0 min 40 → 1 min 25)

- [x] Texte lu et validé par l'auteur (21 novembre 2026)
- [ ] Capsule générée, contrôlée et déposée

**▶️ Script ElevenLabs**

```
[thoughtful, speaking slowly] A badly scoped course is hard to repair: you notice on the third session, when it is too late to start over. That is why the path starts there.

[measured, speaking slowly] Chapter one sets out the three decisions to make before writing a single line. It also doubles as a showcase… every engine component is exercised there at least once.

[measured, speaking slowly] Chapter two starts from that scoping. What remains is deciding in which order, and in what pieces. This is where the difference is made between a course people finish and one they abandon at chapter three.

[measured, speaking slowly] Chapter three chooses the formats. Text, audio, diagram: each has its own intention, and confusing them is expensive, in production time as well as in lost attention.

[warm, encouraging, speaking slowly] Each card, below, opens its chapter and gives its reading time. Follow them in order… it is the order in which a course is designed.
```

**📄 Transcription affichée sur la page**

```
A badly scoped course is hard to repair: you notice on the third session, when it is too late to start over. That is why the path starts there. Chapter 1 sets out the three decisions to make before writing a single line. It also doubles as a showcase, since every engine component is exercised there at least once. Chapter 2 starts from that scoping. What remains is deciding in which order, and in what pieces. This is where the difference is made between a course people finish and one they abandon at chapter three. Chapter 3 chooses the formats. Text, audio, diagram: each has its own intention, and confusing them is expensive, in production time as well as in lost attention. Each card, below, opens its chapter and gives its reading time. Follow them in order, the order in which a course is designed.
```

---

## Capsule 5 · The through-line

- **Nom exact du fichier :** `accueil-section-2-capsule-en.mp3`
- **Emplacement exact :** `site/assets/media/voix/accueil-section-2-capsule-en.mp3` (accueil anglais, conteneur `voix-section-2`)
- **Durée visée :** ≈ 51 s (135 mots parlés, tolérance 0 min 40 → 1 min 25)

- [x] Texte lu et validé par l'auteur (21 novembre 2026)
- [ ] Capsule générée, contrôlée et déposée

**▶️ Script ElevenLabs**

```
[curious, speaking slowly] At every chapter, a learner asks the same question: what will this be used for? The through-line answers it in advance.

[thoughtful, speaking slowly] A through-line is a case, a project or a scenario that runs across the whole course. This demo course's through-line is yours… you build a course while reading a course about building one.

[measured, speaking slowly] The idea fits in one sentence. Pick a topic you know well, and turn it, step by step, into a coherent mini online course. The workshop goes with you: each chapter there directly feeds a deliverable of your project.

[engaged, speaking slowly] Depending on your program, an example shows you what a through-line would look like in your field: an application to design in E.A.D.L., a company's infrastructure to secure in Eris.

[warm, encouraging, speaking slowly] Open the workshop now… and keep it beside you, chapter after chapter.
```

**📄 Transcription affichée sur la page**

```
At every chapter, a learner asks the same question: what will this be used for? The through-line answers it in advance. A through-line is a case, a project or a scenario that runs across the whole course. This demo course's through-line is yours, since you build a course while reading a course about building one. The idea fits in one sentence. Pick a topic you know well, and turn it, step by step, into a coherent mini online course. The workshop goes with you: each chapter there directly feeds a deliverable of your project. Depending on your program, an example shows you what a through-line would look like in your field: an application to design in EADL, a company's infrastructure to secure in ERIS. Open the workshop now, and keep it beside you, chapter after chapter.
```

---

## Capsule 6 · What you produce

- **Nom exact du fichier :** `accueil-section-3-capsule-en.mp3`
- **Emplacement exact :** `site/assets/media/voix/accueil-section-3-capsule-en.mp3` (accueil anglais, conteneur `voix-section-3`)
- **Durée visée :** ≈ 54 s (143 mots parlés, tolérance 0 min 40 → 1 min 25)

- [x] Texte lu et validé par l'auteur (21 novembre 2026)
- [ ] Capsule générée, contrôlée et déposée

**▶️ Script ElevenLabs**

```
[confident, warm, speaking slowly] By the end of the workshop, you will have built a real course, ready to publish. It comes in five deliverables.

[measured, speaking slowly] First, a scoping sheet: the target audience, the prerequisites, three to five measurable learning objectives, and the through-line. Then a plan, which breaks the course down into modules and sequences, with an estimated duration for each.

[measured, speaking slowly] Next, one fully written chapter: a complete sequence, illustrated, with a hook and a key takeaways box. Finally, a five-question quiz, each question with its correct answer and its justification, and a ten-term glossary, each term with its definition and, where possible, an example.

[thoughtful, speaking slowly] The format is free… a text document, a PDF, or a few pages modeled on this site. What matters is the consistency across the five.

[warm, encouraging, speaking slowly] The workshop details each deliverable and its success criteria… start with the scoping sheet, alongside chapter one.
```

**📄 Transcription affichée sur la page**

```
By the end of the workshop, you will have built a real course, ready to publish. It comes in five deliverables. First, a scoping sheet: the target audience, the prerequisites, 3 to 5 measurable learning objectives, and the through-line. Then a plan, which breaks the course down into modules and sequences, with an estimated duration for each. Next, one fully written chapter: a complete sequence, illustrated, with a hook and a "key takeaways" box. Finally, a 5-question quiz, each question with its correct answer and its justification, and a 10-term glossary, each term with its definition and, where possible, an example. The format is free, whether a text document, a PDF, or a few pages modeled on this site. What matters is the consistency across the five. The workshop details each deliverable and its success criteria. Start with the scoping sheet, alongside chapter 1.
```

---

## Capsule 7 · Assessment

- **Nom exact du fichier :** `accueil-section-4-capsule-en.mp3`
- **Emplacement exact :** `site/assets/media/voix/accueil-section-4-capsule-en.mp3` (accueil anglais, conteneur `voix-section-4`)
- **Durée visée :** ≈ 48 s (129 mots parlés, tolérance 0 min 40 → 1 min 25)

- [x] Texte lu et validé par l'auteur (21 novembre 2026)
- [ ] Capsule générée, contrôlée et déposée

**▶️ Script ElevenLabs**

```
[curious, speaking slowly] In this course, the graded quiz asks you for two things on each question: an answer, and your level of certainty.

[measured, speaking slowly] The marking follows that certainty. A correct answer earns three points if you were certain, two if you were fairly sure, one if you were guessing. A wrong answer, for its part, costs three points with high certainty, two with medium certainty… and nothing if you said you were guessing.

[thoughtful, speaking slowly] The scoring therefore rewards clear judgment: better to admit a doubt than to bet blindly. The correction is explained, question by question.

[engaged, speaking slowly] Before the quiz, two tools help you practice. In the chapters, checkpoints test your reading and explain each answer. At the end of each chapter, flashcards recap the essentials.

[warm, encouraging, speaking slowly] Use them… before you take the quiz.
```

**📄 Transcription affichée sur la page**

```
In this course, the graded quiz asks you for two things on each question: an answer, and your level of certainty. The marking follows that certainty. A correct answer earns 3 points if you were certain, 2 if you were fairly sure, 1 if you were guessing. A wrong answer, for its part, costs 3 points with high certainty, 2 with medium certainty, and nothing if you said you were guessing. The scoring therefore rewards clear judgment: better to admit a doubt than to bet blindly. The correction is explained, question by question. Before the quiz, two tools help you practice. In the chapters, checkpoints test your reading and explain each answer. At the end of each chapter, flashcards recap the essentials. Use them before you take the quiz.
```

---

## Capsule 8 · What this site demonstrates

- **Nom exact du fichier :** `accueil-section-5-capsule-en.mp3`
- **Emplacement exact :** `site/assets/media/voix/accueil-section-5-capsule-en.mp3` (accueil anglais, conteneur `voix-section-5`)
- **Durée visée :** ≈ 49 s (130 mots parlés, tolérance 0 min 40 → 1 min 25)

- [x] Texte lu et validé par l'auteur (21 novembre 2026)
- [ ] Capsule générée, contrôlée et déposée

**▶️ Script ElevenLabs**

```
[confident, warm, speaking slowly] This site plays two roles. It teaches you how to design a course… and it shows, page after page, what the template can do.

[measured, speaking slowly] It speaks three languages: French and English across the site, Arabic for chapter one, right to left. When you switch language, you find the passage you were reading.

[measured, speaking slowly] It serves two programs, and it gives each chapter its media: an audio capsule with its transcript, interactive diagrams, a podcast player.

[thoughtful, speaking slowly] The quiz uses certainty-based marking, with its correction and its dashboard. The glossary highlights its terms in the text: hover over one, and a tooltip gives its definition and an example. Flashcards and interactive activities complete the set.

[warm, encouraging, speaking slowly] Finally, the accessibility panel adjusts text size, font and motion… so that everyone can read in good conditions.
```

**📄 Transcription affichée sur la page**

```
This site plays two roles. It teaches you how to design a course, and it shows, page after page, what the template can do. It speaks three languages: French and English across the site, Arabic for chapter 1, right to left. When you switch language, you find the passage you were reading. It serves two programs, and it gives each chapter its media: an audio capsule with its transcript, interactive diagrams, a podcast player. The quiz uses certainty-based marking, with its correction and its dashboard. The glossary highlights its terms in the text: hover over one, and a tooltip gives its definition and an example. Flashcards and interactive activities complete the set. Finally, the accessibility panel adjusts text size, font and motion, so that everyone can read in good conditions.
```

---

## Capsule 9 · Before you start

- **Nom exact du fichier :** `accueil-section-6-capsule-en.mp3`
- **Emplacement exact :** `site/assets/media/voix/accueil-section-6-capsule-en.mp3` (accueil anglais, conteneur `voix-section-6`)
- **Durée visée :** ≈ 52 s (139 mots parlés, tolérance 0 min 40 → 1 min 25)

- [x] Texte lu et validé par l'auteur (21 novembre 2026)
- [ ] Capsule générée, contrôlée et déposée

**▶️ Script ElevenLabs**

```
[warm, encouraging, speaking slowly] Four tips before you start.

[measured, speaking slowly] Start with chapter one. It sets out the three decisions to make before writing, and it doubles as a showcase: every component is used in it.

[measured, speaking slowly] Open the workshop alongside… each chapter there feeds directly into one deliverable of your project.

[measured, speaking slowly] Adjust the display to suit you: dark theme, text size and font are set at the top of the page, in the accessibility panel.

[thoughtful, speaking slowly] And review before the quiz: each chapter's flashcards recap the essentials.

[engaged, speaking slowly] Two resources follow you away from the screen. The course book gathers the whole course in a single book, to read offline; its Q.R. codes take you back to the right spot on the website. The podcasts let you discover a chapter before reading it, or revise it away from the screen… on the train, or while walking.
```

**📄 Transcription affichée sur la page**

```
Four tips before you start. Start with chapter 1. It sets out the three decisions to make before writing, and it doubles as a showcase: every component is used in it. Open the workshop alongside, since each chapter there feeds directly into one deliverable of your project. Adjust the display to suit you: dark theme, text size and font are set at the top of the page, in the accessibility panel. And review before the quiz: each chapter's flashcards recap the essentials. Two resources follow you away from the screen. The course book gathers the whole course in a single book, to read offline; its QR codes take you back to the right spot on the website. The podcasts let you discover a chapter before reading it, or revise it away from the screen, on the train or while walking.
```
