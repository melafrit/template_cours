# 📚 Template de site de cours — *Course Site Template*

> **FR** — Un template pour fabriquer des **sites de cours pédagogiques complets et bilingues (FR/EN)**, avec l'aide de **Claude**.
> **EN** — A template to build **complete, bilingual (FR/EN) educational course websites**, with the help of **Claude**.

<p align="center">
  <img alt="Code license: MIT" src="https://img.shields.io/badge/code-MIT-blue.svg">
  <img alt="Content license: CC BY 4.0" src="https://img.shields.io/badge/contenu%20%26%20prompts-CC%20BY%204.0-lightgrey.svg">
  <img alt="Stack" src="https://img.shields.io/badge/stack-HTML%20%C2%B7%20CSS%20%C2%B7%20JS%20vanilla-orange.svg">
  <img alt="Offline" src="https://img.shields.io/badge/hors%20ligne-oui-success.svg">
  <img alt="Bilingue" src="https://img.shields.io/badge/bilingue-FR%20%2F%20EN-9cf.svg">
  <img alt="Accessibilité" src="https://img.shields.io/badge/a11y-pris%20en%20charge-brightgreen.svg">
</p>

---

## 🌐 Langue / Language

- [🇫🇷 Version française](#-version-française)
- [🇬🇧 English version](#-english-version)

---

# 🇫🇷 Version française

## 🧭 Sommaire

- [Présentation](#présentation)
- [Fonctionnalités](#-fonctionnalités)
- [Structure du dépôt](#-structure-du-dépôt)
- [Démarrage rapide](#-démarrage-rapide)
  - [Voie A — Générer un nouveau cours avec Claude](#voie-a--générer-un-nouveau-cours-avec-claude)
  - [Voie B — Lancer le site en local](#voie-b--lancer-le-site-en-local)
- [Bonnes pratiques](#-bonnes-pratiques)
- [Licences](#-licences)
- [Crédit](#-crédit)

## Présentation

Ce dépôt est un **template réutilisable** pour produire, chapitre après chapitre, un **site de cours pédagogique complet** : pages de cours, podcasts, slides, infographies, QCM noté, flashcards, glossaire interactif, ateliers, polycopiés imprimables, et plus encore.

Le cœur du template, c'est une **bibliothèque de prompts** (`prompts/`) pensée pour travailler **avec Claude** : vous décrivez votre cours une fois (sujet, public, sources), puis vous déroulez les prompts dans l'ordre pour générer un site cohérent, **bilingue FR/EN de bout en bout**.

Le site produit est **statique** (HTML/CSS/JavaScript *vanilla*, **aucun framework**), **fonctionne hors-ligne**, et adopte un design **sobre et institutionnel**, entièrement thémable via des variables CSS.

> 💡 Le dossier `site/` est une **implémentation de référence bilingue**, fournie comme **démo** : un cours déjà fabriqué que vous pouvez ouvrir, explorer et prendre comme modèle.

## ✨ Fonctionnalités

Tout ce que le template (et donc les prompts) sait produire :

- **🌍 Bilingue FR/EN partout** — bascule de langue (bouton 🌐) sur les pages de cours, la navigation, le QCM, les ateliers et le glossaire. Mécanisme : attribut `data-lang` sur `<html>`, blocs FR/EN alternés masqués en CSS, et dictionnaire i18n pour l'interface générée en JavaScript.
- **🧱 Site statique sans framework** — HTML/CSS/JS *vanilla*, hors-ligne, thémable par variables CSS, polices Google Fonts.
- **🧭 Navigation latérale** — menu de gauche avec **sous-menu pliable** des sections de chaque chapitre (ancres cliquables).
- **🎧 Podcast par chapitre** — lecteur audio personnalisé : lecture, ±10 s, **mini-lecteur flottant déplaçable**, *pop-out*, téléchargement.
- **🖥️ Slides** — au format PDF, affichées en **popup plein écran**.
- **🖼️ Infographie** — en **lightbox** avec zoom.
- **📝 QCM d'évaluation (notation CBM)** — *Certainty-Based Marking* : pour chaque question, l'étudiant indique sa certitude (Élevée **+3/−3**, Moyenne **+2/−2**, Faible **+1/0**). Note /20 = `score_brut ÷ (3 × nb_questions) × 20`. Modes **Examen** et **Entraînement**. **Export CSV signé en SHA-256** (intégrité, fonctionne hors-ligne). Questions à réponse **unique**, positions des bonnes réponses équilibrées, distracteurs débiaisés.
- **✅ Correction & tableau de bord** — page de **correction** (dépôt d'un CSV) et **tableau de bord** (plusieurs CSV).
- **🃏 Flashcards** — révision par chapitre (recto/verso, « su / à revoir », persistance `localStorage`).
- **📖 Glossaire bilingue interactif** — les termes sont **auto-surlignés** dans le texte des chapitres, avec **info-bulle au survol** (définition + exemple, FR/EN) reliée à la page glossaire.
- **♿ Accessibilité** — panneau de réglages persistant : taille du texte (A+/A−), police « lecture adaptée » **Atkinson Hyperlegible** (dyslexie), lien « aller au contenu », respect de `prefers-reduced-motion`.
- **🧩 Activités interactives flexibles** — patrons réutilisables : assistant de décision pas-à-pas, quiz-classificateur à feedback, calculateur/simulateur, checklist à score, fiches-résumés — **à choisir selon le sujet**.
- **📄 Polycopiés de synthèse** — par chapitre, générés en **DOCX + PDF** (Python : `python-docx` + `fpdf2`).
- **🖨️ QCM papier imprimable (DOCX)** — page de garde + consignes + barème CBM avec exemples + questions en 2 colonnes + grille de réponses + corrigé formateur.
- **🧵 Atelier « fil rouge »** — un scénario continu qui traverse tout le cours, avec livrables, templates téléchargeables et corrigé.
- **🔗 Intégration NotebookLM** — une fiche de cours (DOCX) à fournir à NotebookLM, et des prompts pour générer infographie / slides / podcast par chapitre.

## 🗂️ Structure du dépôt

```text
template_cours/
├── prompts/   # Bibliothèque de prompts à dérouler avec Claude (commencer par 01)
├── site/      # Implémentation de référence bilingue — DÉMO (HTML/CSS/JS, hors-ligne)
├── tools/     # Scripts Python (polycopiés DOCX/PDF, QCM papier, utilitaires)
├── docs/      # Documentation, guides d'utilisation et conventions
└── README.md  # Ce fichier
```

## 🚀 Démarrage rapide

Deux voies, selon ce que vous voulez faire.

### Voie A — Générer un nouveau cours avec Claude

1. Ouvrez le dossier **`prompts/`** et commencez par le prompt **`01`** (cadrage du cours).
2. Complétez les **placeholders** entre `{{ }}` — par exemple `{{SUJET_DU_COURS}}`, `{{PUBLIC_CIBLE}}`, `{{NIVEAU}}`, `{{DUREE}}`, `{{LANGUES}}`, `{{DOCUMENTS_DE_REFERENCE}}`, `{{FIL_ROUGE}}`, `{{NB_CHAPITRES}}`, `{{AUTEUR}}`, `{{LICENCE}}`, `{{CONTRAINTES}}`.
3. Collez le prompt dans Claude, **fournissez vos documents de référence**, puis **déroulez les prompts suivants dans l'ordre** (chapitres, QCM, glossaire, ateliers, exports…).
4. Déposez les fichiers produits dans `site/` et **vérifiez le rendu dans le navigateur** (voir Voie B).

> 🎯 Chaque prompt précise *quand l'utiliser*, ses placeholders, le bloc à copier et des conseils. Suivez l'ordre numéroté.

### Voie B — Lancer le site en local

Le site étant **statique**, il suffit d'ouvrir une page — mais un **petit serveur statique** est recommandé (certains chargements, comme les PDF ou le CSV, se comportent mieux via `http://` que via `file://`).

**Option simple** — ouvrez directement le fichier :

```text
site/index.html   (double-clic, ou « Ouvrir avec » votre navigateur)
```

**Option recommandée** — un serveur statique local depuis le dossier `site/` :

```bash
# Python 3
python -m http.server 8000

# ou Node.js
npx serve .
```

Puis ouvrez **http://localhost:8000** dans votre navigateur.

## 💡 Bonnes pratiques

- **Commencez par le cadrage.** Le prompt `01` aligne sujet, public, niveau, durée, langues et fil rouge. Tout le reste en découle.
- **Fidélité aux sources.** Demandez à Claude d'**analyser en détail vos documents de référence avant de générer**, de **ne rien inventer** et de **citer ses sources**. La rigueur prime sur la fluidité.
- **Itérez.** Générez un chapitre, relisez, ajustez le prompt, régénérez. Le template est fait pour des passes successives.
- **Vérifiez au navigateur.** Testez la **bascule FR/EN**, le QCM (export/correction), les info-bulles du glossaire, le panneau d'accessibilité et l'affichage des slides/infographies.
- **Restez cohérent.** Réutilisez les mêmes placeholders d'un prompt à l'autre pour garder un cours homogène.

## 📜 Licences

Ce dépôt est sous **double licence** :

- **Code** (le template de site et les scripts) → **MIT**.
- **Contenu et prompts** (la bibliothèque de prompts, la documentation, le contenu pédagogique de démo) → **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

> En cas de réutilisation, **créditez Mohamed EL AFRIT** et indiquez les éventuelles modifications (CC BY 4.0).

## 🙏 Crédit

Créé par **Mohamed EL AFRIT** — ingénieur pédagogique & juriste en droit du numérique.
Template conçu pour fabriquer des sites de cours **avec l'aide de Claude**.

---

# 🇬🇧 English version

## 🧭 Table of contents

- [Overview](#overview)
- [Features](#-features)
- [Repository structure](#-repository-structure)
- [Quick start](#-quick-start)
  - [Path A — Generate a new course with Claude](#path-a--generate-a-new-course-with-claude)
  - [Path B — Run the site locally](#path-b--run-the-site-locally)
- [Best practices](#-best-practices)
- [Licenses](#-licenses)
- [Credit](#-credit)

## Overview

This repository is a **reusable template** to produce, chapter by chapter, a **complete educational course website**: course pages, podcasts, slides, infographics, a graded quiz, flashcards, an interactive glossary, workshops, printable handouts, and more.

At its heart is a **prompt library** (`prompts/`) designed to work **with Claude**: describe your course once (subject, audience, sources), then run the prompts in order to generate a coherent site that is **bilingual FR/EN throughout**.

The resulting site is **static** (HTML/CSS/JavaScript *vanilla*, **no framework**), **works offline**, and uses a **clean, institutional** design, fully themeable through CSS variables.

> 💡 The `site/` folder is a **bilingual reference implementation**, provided as a **demo**: a ready-made course you can open, explore and use as a model.

## ✨ Features

Everything the template (and therefore the prompts) can produce:

- **🌍 Bilingual FR/EN everywhere** — language toggle (🌐 button) across course pages, navigation, quiz, workshops and glossary. Mechanism: a `data-lang` attribute on `<html>`, alternating FR/EN blocks hidden via CSS, and an i18n dictionary for the JavaScript-generated UI.
- **🧱 Static, framework-free site** — *vanilla* HTML/CSS/JS, offline, themeable via CSS variables, Google Fonts.
- **🧭 Side navigation** — left menu with a **collapsible sub-menu** of each chapter's sections (clickable anchors).
- **🎧 Per-chapter podcast** — custom audio player: play, ±10 s, **draggable floating mini-player**, pop-out, download.
- **🖥️ Slides** — in PDF format, shown in a **full-screen popup**.
- **🖼️ Infographic** — in a **lightbox** with zoom.
- **📝 Graded quiz (CBM scoring)** — *Certainty-Based Marking*: for each question the student states their certainty (High **+3/−3**, Medium **+2/−2**, Low **+1/0**). Score out of 20 = `raw_score ÷ (3 × n_questions) × 20`. **Exam** and **Practice** modes. **SHA-256-signed CSV export** (integrity, works offline). **Single-answer** questions, balanced correct-answer positions, debiased distractors.
- **✅ Marking & dashboard** — a **marking page** (drop a CSV) and a **dashboard** (multiple CSVs).
- **🃏 Flashcards** — per-chapter revision (front/back, "known / to review", `localStorage` persistence).
- **📖 Interactive bilingual glossary** — glossary terms are **auto-highlighted** in chapter text, with a **hover tooltip** (definition + example, FR/EN) linked to the glossary page.
- **♿ Accessibility** — persistent settings panel: text size (A+/A−), "easy-reading" font **Atkinson Hyperlegible** (dyslexia), "skip to content" link, respect for `prefers-reduced-motion`.
- **🧩 Flexible interactive activities** — reusable patterns: step-by-step decision wizard, feedback classifier quiz, calculator/simulator, scored checklist, summary cards — **chosen to fit the subject**.
- **📄 Synthesis handouts** — per chapter, generated as **DOCX + PDF** (Python: `python-docx` + `fpdf2`).
- **🖨️ Printable paper quiz (DOCX)** — cover page + instructions + CBM scoring guide with examples + two-column questions + answer grid + instructor key.
- **🧵 "Red thread" workshop** — a continuous scenario running through the whole course, with deliverables, downloadable templates and a model answer.
- **🔗 NotebookLM integration** — a course sheet (DOCX) to feed NotebookLM, plus prompts to generate infographic / slides / podcast per chapter.

## 🗂️ Repository structure

```text
template_cours/
├── prompts/   # Prompt library to run with Claude (start with 01)
├── site/      # Bilingual reference implementation — DEMO (HTML/CSS/JS, offline)
├── tools/     # Python scripts (DOCX/PDF handouts, paper quiz, utilities)
├── docs/      # Documentation, usage guides and conventions
└── README.md  # This file
```

## 🚀 Quick start

Two paths, depending on what you want to do.

### Path A — Generate a new course with Claude

1. Open the **`prompts/`** folder and start with prompt **`01`** (course framing).
2. Fill in the **placeholders** in `{{ }}` — e.g. `{{SUJET_DU_COURS}}`, `{{PUBLIC_CIBLE}}`, `{{NIVEAU}}`, `{{DUREE}}`, `{{LANGUES}}`, `{{DOCUMENTS_DE_REFERENCE}}`, `{{FIL_ROUGE}}`, `{{NB_CHAPITRES}}`, `{{AUTEUR}}`, `{{LICENCE}}`, `{{CONTRAINTES}}`.
3. Paste the prompt into Claude, **provide your reference documents**, then **run the following prompts in order** (chapters, quiz, glossary, workshops, exports…).
4. Drop the generated files into `site/` and **check the result in the browser** (see Path B).

> 🎯 Each prompt states *when to use it*, its placeholders, the block to copy and some tips. Follow the numbered order.

### Path B — Run the site locally

Since the site is **static**, simply opening a page works — but a **small static server** is recommended (some loads, such as PDFs or CSVs, behave better over `http://` than `file://`).

**Simple option** — open the file directly:

```text
site/index.html   (double-click, or "Open with" your browser)
```

**Recommended option** — a local static server from the `site/` folder:

```bash
# Python 3
python -m http.server 8000

# or Node.js
npx serve .
```

Then open **http://localhost:8000** in your browser.

## 💡 Best practices

- **Start with framing.** Prompt `01` aligns subject, audience, level, duration, languages and red thread. Everything else follows.
- **Stay faithful to the sources.** Ask Claude to **analyse your reference documents in detail before generating**, to **invent nothing** and to **cite its sources**. Accuracy comes before fluency.
- **Iterate.** Generate a chapter, review, adjust the prompt, regenerate. The template is built for successive passes.
- **Check in the browser.** Test the **FR/EN toggle**, the quiz (export/marking), glossary tooltips, the accessibility panel and the slides/infographic display.
- **Stay consistent.** Reuse the same placeholders across prompts to keep the course coherent.

## 📜 Licenses

This repository is **dual-licensed**:

- **Code** (the site template and scripts) → **MIT**.
- **Content and prompts** (the prompt library, documentation, demo course content) → **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

> When reusing, **credit Mohamed EL AFRIT** and indicate any changes (CC BY 4.0).

## 🙏 Credit

Created by **Mohamed EL AFRIT** — instructional designer & digital-law jurist.
Template designed to build course websites **with the help of Claude**.

---

<p align="center"><sub>© Mohamed EL AFRIT — Code: MIT · Contenu &amp; prompts / Content &amp; prompts: CC BY 4.0</sub></p>
