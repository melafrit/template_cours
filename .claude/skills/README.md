# Skills Claude Code — *template_cours*

> Index des **Skills** livrés avec le template de site de cours.

## Qu'est-ce que ce dossier ?

Ce dossier regroupe des **Skills Claude Code** embarqués **avec** le template. Lorsqu'on ouvre
ce dépôt dans Claude Code, Claude **applique automatiquement les conventions du template** pendant
qu'il génère ou étend un cours — sans qu'il faille les lui rappeler à chaque fois.

Un Skill est un fichier `SKILL.md` doté d'un **frontmatter YAML** (`name` + `description`).
Claude **charge un skill quand la demande de l'utilisateur correspond à sa `description`** :
les mots-déclencheurs y sont bilingues (français **et** anglais) pour que le skill se déclenche
quelle que soit la formulation. Les détails approfondis vivent dans les fichiers `references/`
de chaque skill et **renvoient** aux docs du dépôt plutôt que de les dupliquer.

## Les 5 skills

| Dossier (`name`) | Rôle (une ligne) | Se déclenche quand… |
| --- | --- | --- |
| **`creer-cours-template`** | Orchestrateur / point d'entrée pour générer un cours complet. | On demande de **« créer un cours »** / *« create a course »*, lancer/échafauder un nouveau cours à partir du template. |
| **`cours-bilingue-i18n`** | Conventions bilingues FR/EN (`data-tr`, `TPLI18N`, formes de données). | On ajoute/traduit du contenu **bilingue**, gère le sélecteur de langue, structure les données i18n (*bilingual, translation, FR/EN*). |
| **`cours-qcm-cbm`** | QCM avec **Certainty-Based Marking** (`questions.js` + `corrections.js`). | On crée/édite un **QCM**, un quiz, une banque de questions, le barème de confiance (*MCQ, quiz, CBM*). |
| **`cours-glossaire-flashcards-activites`** | Infobulles de glossaire, flashcards, `TPLActivities`. | On ajoute un **glossaire**, des **flashcards**, des activités interactives (*glossary tooltips, flashcards, activities*). |
| **`cours-supports-imprimables`** | Générateurs Python des supports papier (polycopiés + QCM papier). | On produit des **supports imprimables**, polycopiés, PDF/DOCX, QCM papier (*printable handouts, polycopié*). |

## Point d'entrée

Commencez par demander à Claude de **« créer un cours »** (ou *« create a course »*) : cela active
**`creer-cours-template`**, l'orchestrateur. Les **4 skills de domaine** s'activent ensuite
**au besoin**, selon la tâche (bilingue, QCM, glossaire/activités, supports imprimables).

## Articulation avec le reste du dépôt

Ces skills **complètent** (sans les remplacer) la bibliothèque **`prompts/`** — utilisée pour
**rédiger du contenu au fil de la discussion** — et les **`docs/`**
([`ARCHITECTURE.md`](../../docs/ARCHITECTURE.md), [`I18N.md`](../../docs/I18N.md),
[`GUIDE.md`](../../docs/GUIDE.md), [`CHECKLIST.md`](../../docs/CHECKLIST.md)),
**référence humaine** du template.

## Emplacement & versionnage

Le **`.gitignore`** ignore tout `.claude/` (config locale de l'éditeur/IDE) **mais désigne
explicitement `.claude/skills/`** pour le réintégrer : ces skills sont **livrés avec le template**,
tandis que le reste de la config `.claude/` locale reste ignoré.

---

> Template de site de cours — **Mohamed EL AFRIT** · code MIT, contenu & prompts CC BY 4.0.
