---
name: creer-cours-template
description: Orchestre la création d'un cours en ligne complet à partir du template (site statique bilingue FR/EN, hors-ligne). À déclencher quand l'utilisateur veut créer / générer / construire un NOUVEAU cours ou site de cours, ou démarrer un projet de cours. Mots-clés FR — « créer un cours », « générer un cours », « nouveau cours », « site de cours », « concevoir un cours en ligne », « fabriquer un cours ». Keywords EN — « create / build / generate a course », « new course website », « design an online course », « course site from template ». Point d'entrée du pipeline en 4 phases ; renvoie vers les 4 skills domaine (i18n, QCM CBM, glossaire/flashcards/activités, supports imprimables).
---

# Créer un cours à partir du template

Skill **orchestrateur** : point d'entrée pour fabriquer, avec ce dépôt, un **site de cours complet, pédagogique, bilingue FR/EN, hors-ligne et statique** (HTML/CSS/JS vanilla, aucun framework). Il pilote le pipeline et délègue le détail à 4 skills domaine + à la documentation du dépôt.

## Quand l'utiliser

Dès que l'utilisateur veut **démarrer un projet de cours** ou **générer un nouveau cours / site de cours** depuis ce template. C'est le premier réflexe : on passe par ce skill avant tout autre.

## Règle d'or

**TOUJOURS commencer par le cadrage.** On ne génère **aucun** contenu (page, chapitre, QCM, glossaire, activité, support) tant que le périmètre n'est pas fixé et **validé** par l'utilisateur. Le cadrage se fait avec `prompts/01_cadrage_maitre.md`, dont la sortie — la **fiche de cadrage** — alimente tout le reste. Sauter cette étape = chapitres incohérents, fil rouge bancal, QCM hors-sujet.

## Méthode de cadrage

Claude conduit le cadrage exactement comme `prompts/01_cadrage_maitre.md` le prescrit :

- **Analyse documentaire d'abord.** Lire en détail les `{{DOCUMENTS_DE_REFERENCE}}` AVANT de poser la moindre question ou de rédiger. Les documents sont la **source de vérité** : ne **rien inventer**, **citer** chaque source (titre / section / page), signaler les **lacunes** (« information absente des documents ») et les contradictions plutôt que combler le vide.
- **Questions UNE À UNE.** Poser les questions de cadrage **séquentiellement**, une seule à la fois, puis attendre la réponse. Chaque question propose une **recommandation par défaut** et des **options numérotées** (réponse possible d'un simple chiffre), avec une option « Autre (précise) ».
- **Trancher la langue tôt.** Demander explicitement **« français seul »** OU **« français + anglais »**. Ce choix conditionne TOUT (chaque page, la navigation, le QCM, le glossaire, les ateliers existent dans les deux langues si bilingue). Voir le skill `cours-bilingue-i18n`.
- **Proposer des activités adaptées au sujet** et clarifier les besoins : QCM CBM (combien de questions ? QCM papier ?), **flashcards**, **fiches-résumés**, **checklist à score**, **assistant de décision**, **calculateur**, **quiz-classificateur**… Ne proposer que ce qui colle au sujet.
- **Valider avant de produire.** Présenter un récapitulatif et demander « Valides-tu ce cadrage ? ». N'avancer vers la génération qu'après un « oui » clair, puis produire les 3 livrables de cadrage : **fiche de cadrage**, **plan du site**, **feuille de route des prompts**.

## Pipeline en 4 phases

1. **Cadrage & architecture** — fiche de cadrage, plan/syllabus, fil rouge.
2. **Contenu pédagogique** — chapitres bilingues, relecture, glossaire.
3. **Évaluation & activités** — QCM CBM, activités interactives, flashcards, atelier fil rouge.
4. **Supports & diffusion** — polycopiés DOCX/PDF, QCM papier, pack NotebookLM, QA accessibilité.

> Détail des phases ↔ fichiers `prompts/` exacts : voir `references/workflow.md`.

## Conventions imposées par le template

- **Bilingue FR/EN partout** (si bilingue retenu) : contenu en blocs `data-tr`, UI JS via `window.TPLI18N`, données en forme `{fr, en}`. → skill **`cours-bilingue-i18n`** et `docs/I18N.md`.
- **Hors-ligne & statique** : HTML/CSS/JS vanilla, thémable par variables CSS, polices Google Fonts ; tout fonctionne en `file://`. → `docs/ARCHITECTURE.md` §5.
- **Ordre d'inclusion des scripts** strict (i18n d'abord, données avant leur moteur, animations en dernier). → `references/arborescence.md` et `docs/ARCHITECTURE.md` §3.

Skills domaine à mobiliser selon la tâche :

- **`cours-bilingue-i18n`** — conventions bilingues (data-tr, TPLI18N, formes de données).
- **`cours-qcm-cbm`** — banque QCM à notation CBM (`questions.js` + `corrections.js`).
- **`cours-glossaire-flashcards-activites`** — glossaire auto-surligné, flashcards, `TPLActivities`.
- **`cours-supports-imprimables`** — générateurs Python des polycopiés et du QCM papier.

Docs de référence du dépôt : `docs/ARCHITECTURE.md`, `docs/I18N.md`, `docs/GUIDE.md`, `docs/CHECKLIST.md`, et `prompts/00_README_prompts.md`.

## Auteur & commits

**IMPORTANT.** Tous les commits du cours doivent être au nom de **Mohamed EL AFRIT `<elafrit.mohamed@gmail.com>`**, **JAMAIS** au nom de Claude/Anthropic. **Ne jamais** ajouter de trailer `Co-Authored-By` ni aucun crédit Claude/Anthropic dans les commits, le contenu, les prompts ou la documentation. Le template, ses prompts et son contenu sont attribués à l'auteur, pas à l'outil.

## Fichiers de référence joints

- `references/workflow.md` — pipeline en 4 phases mappé aux fichiers `prompts/` réels + tableau des placeholders communs.
- `references/arborescence.md` — carte condensée de `site/`, ordre d'inclusion des scripts, recettes rapides (chapitre, QCM, glossaire, activité).

> Template de site de cours — **Mohamed EL AFRIT** · code MIT, contenu & prompts CC BY 4.0.
