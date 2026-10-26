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
- [Skills Claude Code](#-skills-claude-code)
- [Démarrage rapide](#-démarrage-rapide)
  - [Voie A — Générer un nouveau cours avec Claude](#voie-a--générer-un-nouveau-cours-avec-claude)
  - [Voie B — Lancer le site en local](#voie-b--lancer-le-site-en-local)
  - [Voie C — Vérifier](#voie-c--vérifier)
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

- **🌍 Bilingue FR/EN partout** — bascule de langue (bouton 🌐) sur les pages de cours, la navigation, le QCM, les ateliers et le glossaire. Mécanisme : attribut `data-lang` sur `<html>`, blocs FR/EN alternés masqués en CSS, et dictionnaire i18n pour l'interface générée en JavaScript. Pour un nouveau cours, le modèle retenu est désormais le **site miroir** : chaque page française a sa jumelle anglaise sous `en/`, écrite une fois le français stable, avec ses outils — bouton qui garde la position, préparation des jumelles, conversion d'un cours en blocs alternés, liens, `hreflang`, contrôle de parité ; les blocs alternés restent en secours (`docs/I18N.md`).
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
- **📘 Polycopié** — tout le cours en un **livret A4, Word et PDF**, tiré des pages du site : page de garde, mentions légales, présentation de l'auteur, mini-sommaire à chaque chapitre, schémas expliqués, activités devenues exercices sur papier, glossaire, index ; dans la grande marge, des **QR codes cliquables** vers les capsules, les définitions et les corrections en ligne — aucune réponse imprimée. Sa page **📘 Polycopié** le fait télécharger (module 02 ; `outils/generer_polycopie.py`, `outils/publier_polycopie.py`).
- **📄 Fiches de synthèse** — par chapitre, générées en **DOCX + PDF** (Python : `python-docx` + `fpdf2`).
- **🖨️ QCM papier imprimable (DOCX)** — page de garde + consignes + barème CBM avec exemples + questions en 2 colonnes + grille de réponses + corrigé formateur.
- **🧵 Atelier « fil rouge »** — un scénario continu qui traverse tout le cours, avec livrables, templates téléchargeables et corrigé.
- **🔗 Intégration NotebookLM** — une fiche de cours (DOCX) à fournir à NotebookLM, et des prompts pour générer infographie / slides / podcast par chapitre ; ou une série de podcasts enchaînés et leurs diaporamas, tirés du polycopié, avec leur page sur le site (module 03). La page **🎙️ Podcasts** est fournie : par épisode, un lecteur, un résumé et ses diapositives, une visionneuse plein écran, un encadré dans chaque chapitre ; `outils/generer_podcasts.py` convertit les épisodes (MP3 mono, 64 kbit/s) et rend les diapositives.
- **🧠 Moteur de composants pédagogiques (`RDCX`)** — point de contrôle, révélation d'une réponse, repérage d'erreurs dans un document, appariement, scénario à embranchements, schéma à points chauds, capsule audio. Tous appelés pour de vrai dans `site/chapitres/_modele.html`, à copier depuis là.
- **📖 Lecture par étapes** — un chapitre se parcourt section par section, avec une barre de progression, un mode « tout afficher » et une reprise là où l'on s'était arrêté.
- **🎵 Playlist latérale** — toutes les pistes audio du cours, enchaînement automatique, tiroir sur mobile, et **filtrage par langue** : un lecteur francophone ne voit pas les capsules anglaises.
- **🗣️ Chaîne audio ElevenLabs (Eleven v4)** — script écrit dans une fiche de production, génération par l'API avec votre voix clonée et l'accent retenu à l'écoute, **un témoin écouté avant toute série**, **contrôle qualité avant dépôt** (durée, débit, silences) et mise en quarantaine de ce qui sort des clous. Une capsule par langue.
- **💬 Quiz qui expliquent l'erreur** — chaque point de contrôle dit pourquoi la bonne réponse est juste, **pourquoi chacune des autres ne l'est pas**, et propose des renvois « Pour approfondir » vers l'endroit exact du cours ; le vérificateur de liens contrôle chaque renvoi, fichier et ancre.
- **🎨 Palettes vérifiées** — charte commune à tous vos cours, couleur d'accent choisie dans `cours.json` parmi cinq palettes contrôlées en contraste, en thème clair **et** sombre.
- **🚀 Amorçage en une commande** — `nouveau_cours.py` fabrique l'arborescence complète d'un nouveau cours à partir d'un fichier de configuration commenté, avec son contrat de travail (`CLAUDE.md`), sa destination de publication, et vos secrets recopiés en local.
- **📋 Prompt paramétrable** — `prompts/PROMPT-Cours-parametrable.md` : un tronc commun (un bloc de paramètres, la méthode de l'amorçage à la mise en ligne, ses jalons) et un module par option dans `prompts/modules/` — bilingue, polycopié, podcasts NotebookLM, audio, évaluations, TP, Yparéo et Livrables, déploiement, compléments. Un module sert aussi seul, sur un cours existant.
- **🔐 Déploiement OVH sûr** — SFTP, envoi incrémental, **garde-fou qui refuse d'écraser le dossier d'un autre cours**, protections du serveur jamais touchées, zones protégées (correction de TP) publiées après leur mot de passe. Testé hors ligne.

## 🗂️ Structure du dépôt

```text
template_cours/
├── CLAUDE.md          # Contrat de travail — lu par Claude à chaque ouverture
├── cours.exemple.json # Modèle de configuration d'un nouveau cours (commenté)
├── nouveau_cours.py   # Fabrique un cours à partir de cours.json
├── demarrer.py|bat|command  # Lance le site en local, sans cache
├── sources/           # VOS documents de référence — hors dépôt (droit d'auteur)
├── site/              # Le site lui-même : cours de démonstration à 3 chapitres
├── outils/            # Audio ElevenLabs, playlist, schémas, vérificateurs
├── tools/             # Polycopiés DOCX/PDF, QCM papier
├── deploiement/       # Déploiement SFTP vers OVH, garde-fou, zones protégées, tests hors ligne
├── prompts/           # Prompt paramétrable + bibliothèque de prompts de rédaction
├── docs/              # Architecture, guide, i18n, bonnes pratiques, checklist, recette
└── .claude/skills/    # Skills Claude Code livrés avec le template
```

> 🔒 **Secrets.** `outils/elevenlabs.json` (clé et voix ElevenLabs) et `deploiement/config.json` (accès à l'hébergement) vivent **uniquement sur votre poste**, ignorés par Git ; le dépôt n'en contient que les modèles `*.exemple.json`. `nouveau_cours.py` les recopie tels quels dans chaque nouveau cours. Le répertoire distant, lui, est propre à chaque cours : `deploiement/destination.json`.

## 🤖 Skills Claude Code

Le template embarque des **Skills Claude Code** dans **`.claude/skills/`**. Quand on ouvre ce dépôt dans **Claude Code**, ces skills se chargent automatiquement : Claude applique alors **les conventions du template** (bilinguisme, QCM CBM, glossaire, formes de données…) pendant qu'il génère ou étend un cours — sans qu'on ait à les lui rappeler.

| Skill | Se déclenche quand… |
|---|---|
| **`creer-cours-template`** | on veut **créer / générer un nouveau cours** → orchestre le cadrage (questions une à une) et le pipeline en 4 phases. |
| **`cours-bilingue-i18n`** | on ajoute/traduit du contenu **bilingue FR/EN** (`data-tr`, `TPLI18N`, formes de données). |
| **`cours-qcm-cbm`** | on crée/édite le **QCM** à notation CBM (`questions.js` + `corrections.js`). |
| **`cours-glossaire-flashcards-activites`** | on ajoute **glossaire**, **flashcards** ou **activités interactives**. |
| **`cours-supports-imprimables`** | on génère les **supports imprimables** (polycopiés, QCM papier). |

> Point d'entrée : demandez simplement à Claude de **« créer un cours »**. Les autres skills s'activent au besoin. Détails dans [`.claude/skills/README.md`](.claude/skills/README.md). Ces skills **complètent** la bibliothèque `prompts/` (rédaction au fil de la discussion) et les `docs/` (référence humaine).

## 🚀 Démarrage rapide

Deux voies, selon ce que vous voulez faire.

### Voie A — Créer un nouveau cours

**0. Le plus court : le prompt paramétrable.** Remplissez le bloc de paramètres de
[`prompts/PROMPT-Cours-parametrable.md`](prompts/PROMPT-Cours-parametrable.md) — ce
que vous ignorez reste vide — et demandez à Claude de **créer le cours** depuis ce
template. Il fait lui-même les étapes ci-dessous, en vous posant ses questions une
à une, et s'arrête à chaque jalon.

**1. Amorcer la mécanique.**

```bash
cp cours.exemple.json cours.json     # puis remplissez-le : titre, palette, chapitres, publication…
python3 nouveau_cours.py --essai     # ce qu'il ferait, sans rien écrire
python3 nouveau_cours.py             # crée le cours dans le dossier « sortie »
```

Le script produit l'arborescence, la charte, la navigation, les squelettes de
chapitres et le déployeur ; il écrit le `CLAUDE.md` et la destination de
publication du cours, et recopie vos secrets en local. **Il ne rédige aucun
contenu** — c'est voulu : un script qui inventerait des chapitres produirait un
cours générique.

**2. Déposer vos sources.** Référentiel, supports existants, articles, normes vont
dans `sources/`. Ce dossier est **exclu du dépôt** — ces documents ne vous
appartiennent pas et l'historique Git ne s'efface pas. Complétez
`sources/bibliographie.md` au fur et à mesure.

**3. Cadrer avec Claude.** Ouvrez le dossier du nouveau cours avec Claude Code et
demandez-lui de **créer le cours**. Il lit vos sources, puis pose ses questions
**une à une**, et ne rédige rien avant que vous ayez validé le cadrage.

**4. Écrire les chapitres.** Le chapitre vitrine est conservé sous
`site/chapitres/_modele.html` : c'est le seul endroit où tous les composants sont
appelés pour de vrai. Copiez depuis là.

### Voie B — Lancer le site en local

Double-cliquez **`demarrer.bat`** (Windows) ou **`demarrer.command`** (macOS), ou
bien :

```bash
python3 demarrer.py
```

Le navigateur s'ouvre sur la page d'accueil. Si le port est pris, le lanceur
passe au suivant.

> ⚠️ Le lanceur **désactive le cache**, et c'est sa raison d'être : avec un
> serveur ordinaire, le navigateur ressert l'ancien JavaScript après une
> modification, et l'on cherche un défaut qui n'existe pas. Si malgré tout un
> changement ne semble pas prendre, changez de port — certains navigateurs
> gardent le script en mémoire.

### Voie C — Vérifier

```bash
python3 outils/verifier_i18n.py       # clés dépareillées, blocs FR/EN déséquilibrés
python3 outils/verifier_contraste.py  # palettes lisibles en clair et en sombre
python3 outils/verifier_liens.py      # href, src et renvois « Pour approfondir » qui ne mènent nulle part
python3 deploiement/tester_deployer.py  # garde-fou et protections du déployeur, hors ligne
```

> 🧪 À la réception du template, ou après toute modification du moteur, déroulez [`docs/RECETTE.md`](docs/RECETTE.md) : vingt minutes, trois tests. Le dernier — générer un cours vide — est le seul qui vous dise ce que vous recevrez réellement en démarrant un nouveau cours.

## 💡 Bonnes pratiques

- **Commencez par le cadrage.** Le prompt `01` aligne sujet, public, niveau, durée, langues et fil rouge. Tout le reste en découle.
- **Fidélité aux sources.** Demandez à Claude d'**analyser en détail vos documents de référence avant de générer**, de **ne rien inventer** et de **citer ses sources**. La rigueur prime sur la fluidité.
- **Itérez.** Générez un chapitre, relisez, ajustez le prompt, régénérez. Le template est fait pour des passes successives.
- **Vérifiez au navigateur.** Testez la **bascule FR/EN**, le QCM (export/correction), les info-bulles du glossaire, le panneau d'accessibilité et l'affichage des slides/infographies.
- **Restez cohérent.** Réutilisez les mêmes placeholders d'un prompt à l'autre pour garder un cours homogène.
- **Ne modifiez jamais un fichier généré.** L'index de playlist, l'index des sections et les transcriptions de capsules sont produits par des scripts : les corriger à la main donne l'illusion d'avoir résolu le problème jusqu'à la régénération suivante.

> 📘 Le détail — et surtout **les raisons** — dans [`docs/BONNES_PRATIQUES.md`](docs/BONNES_PRATIQUES.md). Chaque point y vient d'un défaut réellement rencontré.

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
- [Claude Code skills](#-claude-code-skills)
- [Quick start](#-quick-start)
  - [Path A — Generate a new course with Claude](#path-a--generate-a-new-course-with-claude)
  - [Path B — Run the site locally](#path-b--run-the-site-locally)
  - [Path C — Verify](#path-c--verify)
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

- **🌍 Bilingual FR/EN everywhere** — language toggle (🌐 button) across course pages, navigation, quiz, workshops and glossary. Mechanism: a `data-lang` attribute on `<html>`, alternating FR/EN blocks hidden via CSS, and an i18n dictionary for the JavaScript-generated UI. For a new course, the chosen model is now the **mirror site**: every French page gets its English twin under `en/`, written once the French is stable, with its tools — a toggle that keeps your place, twin scaffolding, conversion of an alternating-blocks course, links, `hreflang`, parity check; alternating blocks remain the fallback (`docs/I18N.md`).
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
- **📘 Course book** — the whole course in one **A4 book, Word and PDF**, drawn from the site's pages: cover page, legal notice, author introduction, a contents list for each chapter, explained diagrams, activities turned into paper exercises, glossary, index; in the wide margin, **clickable QR codes** to the audio capsules, definitions and online answers — no answers printed. Its **📘 Course book** page offers the download (module 02; `outils/generer_polycopie.py`, `outils/publier_polycopie.py`).
- **📄 Summary sheets** — per chapter, generated as **DOCX + PDF** (Python: `python-docx` + `fpdf2`).
- **🖨️ Printable paper quiz (DOCX)** — cover page + instructions + CBM scoring guide with examples + two-column questions + answer grid + instructor key.
- **🧵 "Red thread" workshop** — a continuous scenario running through the whole course, with deliverables, downloadable templates and a model answer.
- **🔗 NotebookLM integration** — a course sheet (DOCX) to feed NotebookLM, plus prompts to generate infographic / slides / podcast per chapter; or a chained podcast series with its slide decks, drawn from the course book, with its own page on the site (module 03). The **🎙️ Podcasts** page is included: per episode, a player, a summary and its slides, a full-screen viewer, a box in each chapter; `outils/generer_podcasts.py` converts the episodes (64 kbit/s mono MP3) and renders the slides.
- **🗣️ ElevenLabs audio chain (Eleven v4)** — scripts written in a production sheet, generated with your cloned voice and the accent chosen by ear, **one test take listened to before any batch**, and **quality control before publishing** (duration, pace, silences).
- **💬 Quizzes that explain the mistake** — every checkpoint says why the right answer is right, **why each of the others is not**, and links to the exact place in the course to go further; the link checker verifies each link, file and anchor.
- **📋 Parametrizable prompt** — `prompts/PROMPT-Cours-parametrable.md`: a common core (a parameter block, the method from bootstrapping to going live, its milestones) and one module per option in `prompts/modules/` — bilingual site, course book, NotebookLM podcasts, audio, assessments, lab, school tools, deployment, extras (in French). A module also works on its own, on an existing course.
- **🔐 Safe OVH deployment** — SFTP, incremental upload, **a guard that refuses to overwrite another course's folder**, server-side protections never touched, password-protected zones published only once protected. Tested offline.

## 🗂️ Repository structure

```text
template_cours/
├── CLAUDE.md          # Working contract — read by Claude on every session
├── cours.exemple.json # Commented configuration model for a new course
├── nouveau_cours.py   # Builds a course from cours.json
├── demarrer.py|bat|command  # Runs the site locally, cache disabled
├── sources/           # YOUR reference documents — outside the repo (copyright)
├── site/              # The site itself: a 3-chapter demo course
├── outils/            # ElevenLabs audio, playlist, diagrams, verifiers
├── tools/             # DOCX/PDF handouts, printable quiz
├── deploiement/       # SFTP deployment to OVH, identity guard, protected zones, offline tests
├── prompts/           # Parametrizable prompt + writing prompt library
├── docs/              # Architecture, guide, i18n, best practices, checklist, acceptance tests
└── .claude/skills/    # Claude Code skills shipped with the template
```

> 🔒 **Secrets.** `outils/elevenlabs.json` (ElevenLabs key and voice) and `deploiement/config.json` (hosting access) live **only on your machine**, ignored by Git; the repository only holds the `*.exemple.json` models. `nouveau_cours.py` copies them as-is into each new course. The remote folder is specific to each course: `deploiement/destination.json`.

## 🤖 Claude Code skills

The template ships with **Claude Code Skills** in **`.claude/skills/`**. When you open this repository in **Claude Code**, the skills load automatically: Claude then applies **the template's conventions** (bilingualism, CBM quiz, glossary, data shapes…) while generating or extending a course — without you having to restate them.

| Skill | Triggers when… |
|---|---|
| **`creer-cours-template`** | you want to **create / generate a new course** → orchestrates framing (one question at a time) and the 4-phase pipeline. |
| **`cours-bilingue-i18n`** | you add/translate **bilingual FR/EN** content (`data-tr`, `TPLI18N`, data shapes). |
| **`cours-qcm-cbm`** | you create/edit the **CBM-scored quiz** (`questions.js` + `corrections.js`). |
| **`cours-glossaire-flashcards-activites`** | you add a **glossary**, **flashcards** or **interactive activities**. |
| **`cours-supports-imprimables`** | you generate the **printable supports** (handouts, paper quiz). |

> Entry point: just ask Claude to **"create a course"**. The other skills activate as needed. Details in [`.claude/skills/README.md`](.claude/skills/README.md). These skills **complement** the `prompts/` library (authoring via chat) and the `docs/` (human reference).

## 🚀 Quick start

Two paths, depending on what you want to do.

### Path A — Generate a new course with Claude

0. **Shortest route:** fill in the parameter block of [`prompts/PROMPT-Cours-parametrable.md`](prompts/PROMPT-Cours-parametrable.md) and ask Claude to **create the course** from this template. It runs `nouveau_cours.py`, asks its questions one at a time and stops at each milestone. The steps below are the manual equivalent.
1. Open the **`prompts/`** folder and start with prompt **`01`** (course framing).
2. Fill in the **placeholders** in `{{ }}` — e.g. `{{SUJET_DU_COURS}}`, `{{PUBLIC_CIBLE}}`, `{{NIVEAU}}`, `{{DUREE}}`, `{{LANGUES}}`, `{{DOCUMENTS_DE_REFERENCE}}`, `{{FIL_ROUGE}}`, `{{NB_CHAPITRES}}`, `{{AUTEUR}}`, `{{LICENCE}}`, `{{CONTRAINTES}}`.
3. Paste the prompt into Claude, **provide your reference documents**, then **run the following prompts in order** (chapters, quiz, glossary, workshops, exports…).
4. Drop the generated files into `site/` and **check the result in the browser** (see Path B).

> 🎯 Each prompt states *when to use it*, its placeholders, the block to copy and some tips. Follow the numbered order.

### Path B — Run the site locally

Use the bundled launcher. Double-click it in Finder or Explorer, or run:

```bash
./demarrer.command     # macOS
demarrer.bat           # Windows
python3 demarrer.py    # anywhere
```

It serves `site/` on **http://localhost:8765**, opens your browser, and falls back to the next free port if 8765 is taken.

> ⚠️ Prefer it over a plain `python -m http.server`. The launcher **disables caching** and answers **in parallel** — two defects it exists to prevent: a browser serving stale JavaScript after an edit, so you hunt a bug that no longer exists; and a single open tab freezing every other client, silently. If a change still refuses to show, switch ports: some browsers keep the script in memory regardless.

### Path C — Verify

```bash
python3 outils/verifier_i18n.py       # unpaired keys, unbalanced FR/EN blocks
python3 outils/verifier_contraste.py  # palettes readable in light and dark
python3 outils/verifier_liens.py      # href, src and "go further" links pointing nowhere
python3 deploiement/tester_deployer.py  # deployment guard and protections, offline
```

> 🧪 When you first receive the template, or after any engine change, work through [`docs/RECETTE.md`](docs/RECETTE.md) (in French): twenty minutes, three tests. The last one — generating an empty course — is the only one that tells you what you will actually get when starting a new course.

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
