---
name: creer-cours-template
description: Orchestre la création d'un cours en ligne complet à partir du template (site statique, hors-ligne, français ou bilingue FR/EN), en suivant le prompt paramétrable de l'auteur. À déclencher quand l'utilisateur veut créer / générer / construire un NOUVEAU cours ou site de cours, ou démarrer un projet de cours. Mots-clés FR — « créer un cours », « générer un cours », « nouveau cours », « site de cours », « concevoir un cours en ligne », « fabriquer un cours ». Keywords EN — « create / build / generate a course », « new course website », « design an online course », « course site from template ». Point d'entrée du pipeline ; renvoie vers les 4 skills domaine (i18n, QCM CBM, glossaire/flashcards/activités, supports imprimables).
---

# Créer un cours à partir du template

Skill **orchestrateur** : point d'entrée pour fabriquer, avec ce dépôt, un **site de cours
complet, pédagogique, hors-ligne et statique** (HTML/CSS/JS vanilla, aucun framework). La
méthode complète — paramètres, règles, étape zéro, phases et jalons — est dans
**`prompts/PROMPT-Cours-parametrable.md`**, le tronc commun ; chaque option (bilingue,
polycopié, podcasts NotebookLM, audio, évaluations, TP, Yparéo et Livrables, déploiement,
compléments) a son **module** dans `prompts/modules/`, lu avant sa phase s'il est actif.
Ce skill déroule le tronc et ses modules.

## Quand l'utiliser

Dès que l'utilisateur veut **démarrer un projet de cours** ou **générer un nouveau cours**
depuis ce template. C'est le premier réflexe : on passe par ce skill avant tout autre.

## Les exigences de l'auteur — à appliquer sans qu'il les rappelle

Elles sont détaillées dans `CLAUDE.md` (§ 2). L'essentiel :

- **Questions une à une**, avec l'outil de question à options cliquables
  (AskUserQuestion) — jamais une liste dans le texte ; recommandation en premier ;
  **chaque étape finit par une question cliquable** sur la suite.
- **Commits** au seul nom de **Mohamed Amine EL AFRIT `<elafrit.mohamed@gmail.com>`**,
  **jamais** de trailer `Co-Authored-By` ni de mention d'un outil ou d'une IA ; `git add`
  par chemins explicites ; **demander avant de commiter et pousser**, puis avant de
  **mettre en ligne**.
- **Secrets** (`outils/elevenlabs.json`, `deploiement/config.json`, `docs/acces.json`,
  `docs/acces-zones.json`) : jamais ouverts, affichés ni demandés ; recopiés tels quels
  du template vers le cours par `nouveau_cours.py`.
- **Ne rien inventer**, citer, signaler les lacunes ; ne jamais reproduire le texte ni les
  figures d'un ouvrage ; aucune date fixe dans le contenu ; rien ne souffle une réponse.
- **Quiz** : chaque proposition expliquée, deux à quatre renvois « Pour approfondir »
  (`prompts/15_explications_quiz.md`). **Schémas** expliqués élément par élément.
  **Liens externes** dans un nouvel onglet, vérifiés avant ajout.
- **Audio** : Eleven v4, accent parisien marqué, ton pédagogique et posé, **témoin
  d'abord** (`prompts/14_capsules_audio.md`).

## Déroulé

### 1. Les paramètres — Phase 0

Lire le bloc de paramètres fourni (section 3 du prompt paramétrable). Pour chaque
paramètre vide qui ne se déduit pas des sources, **une question à la fois**. Récapituler
ce qui est fourni, déduit et encore ouvert. **STOP.**

### 2. L'amorçage mécanique — étape zéro

```
cp cours.exemple.json cours.json      # Claude le remplit d'après les paramètres
python3 nouveau_cours.py --essai      # montré à l'auteur
python3 nouveau_cours.py              # crée le cours dans un dossier à part
```

Le script met en place l'arborescence, la charte, la navigation, les squelettes de
chapitres, les outils et le déployeur ; il écrit `CLAUDE.md` et
`deploiement/destination.json` ; il recopie en local les secrets communs. Il ne rédige
**aucun** contenu.

Vérifier dans sa sortie : secrets « copiés en local, ignorés par Git », destination au nom
du cours, chapitre vitrine conservé (`site/chapitres/_modele.html`). Puis initialiser le
dépôt Git du cours (privé), et le journal : `docs/01-Decisions-de-conception.md`,
`docs/02-Etat-d-avancement.md`.

### 3. Les sources et le cadrage — Phase 1

- **Les documents de référence vivent dans `sources/`** du cours (non versionnés — droit
  d'auteur ; `sources/bibliographie.md`, lui, l'est et se complète au fil de l'eau).
- **Lire tous les documents AVANT** la moindre question de fond.
- Conduire le cadrage comme `prompts/01_cadrage_maitre.md` le prescrit : analyse
  documentaire, questions une à une, **langue tranchée tôt** (français seul ou bilingue :
  le bilingue double la rédaction et l'audio), activités adaptées au sujet.
- Présenter un récapitulatif et attendre un « oui » clair. **STOP.**

### 4. La production — Phases 2 à 11

Suivre les phases du prompt paramétrable, avec leurs jalons : référentiel du cas,
squelette, chapitres (STOP après le premier), TP et correction protégée, évaluations
expliquées, audio (témoin, STOP, série), illustrations, Yparéo et Livrables, déploiement,
documentation de reprise.

> Détail des phases ↔ fichiers `prompts/` : voir `references/workflow.md`.

## Conventions imposées par le template

- **Bilingue** (si retenu) : contenu en blocs `data-tr`, libellés des moteurs via `T()`
  (`ui-labels.js`), contenu des composants dans `TEXTES = { fr, en }`. → skill
  **`cours-bilingue-i18n`** et `docs/I18N.md`.
- **Hors-ligne & statique** : HTML/CSS/JS vanilla ; tout fonctionne sans serveur. →
  `docs/ARCHITECTURE.md` §5.
- **Copier depuis `_modele.html`** plutôt qu'écrire de mémoire. **Ordre d'inclusion des
  scripts** strict. → `references/arborescence.md`.
- **Vérifier** : `outils/verifier_i18n.py`, `verifier_contraste.py`, `verifier_liens.py`
  (renvois compris), et le navigateur (clair, sombre, 1280 et 375 px, console vide).
- **Publier** : `deploiement/deployer.py --essai` d'abord ; la destination vient de
  `destination.json` ; le garde-fou refuse le dossier d'un autre cours.

Skills domaine à mobiliser selon la tâche :

- **`cours-bilingue-i18n`** — conventions bilingues (data-tr, TPLI18N, formes de données).
- **`cours-qcm-cbm`** — banque QCM à notation CBM (`questions.js` + `corrections.js`).
- **`cours-glossaire-flashcards-activites`** — glossaire, flashcards, activités.
- **`cours-supports-imprimables`** — polycopiés et QCM papier.

Docs de référence du dépôt : `CLAUDE.md`, `prompts/PROMPT-Cours-parametrable.md` et
`prompts/modules/`, `docs/ARCHITECTURE.md`, `docs/I18N.md`, `docs/GUIDE.md`, `docs/CHECKLIST.md`,
`deploiement/LISEZMOI.md` et `prompts/00_README_prompts.md`.

## Fichiers de référence joints

- `references/workflow.md` — les phases mappées aux fichiers `prompts/` réels + tableau des
  placeholders communs.
- `references/arborescence.md` — carte condensée de `site/`, ordre d'inclusion des
  scripts, recettes rapides (chapitre, QCM, glossaire, activité).

> Template de site de cours — **Mohamed Amine EL AFRIT** · code MIT, contenu & prompts CC BY 4.0.
