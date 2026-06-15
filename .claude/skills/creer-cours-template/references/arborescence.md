# Carte de `site/` + ordre d'inclusion des scripts

Carte condensée : **où vit chaque fichier**. Pour le détail complet (rôle de chaque moteur, formes de données), voir `docs/ARCHITECTURE.md` §1–§2.

```text
site/
├── index.html            # Accueil (présentation + vitrine des fonctionnalités)
├── cours.html            # Sommaire : grille des chapitres + ressources
├── glossaire.html        # Glossaire bilingue filtrable (rendu JS depuis GLOSSARY)
├── activites.html        # Démos des 3 patrons d'activités de tools.js
├── atelier.html          # Atelier « fil rouge » (contenu statique)
├── about.html            # À propos / crédits / licences
├── chapitres/
│   ├── 01-cadrage.html   # ← CHAPITRE MODÈLE : copier celui-ci (préfixe NN- obligatoire)
│   └── 0N-….html
├── QCM/
│   ├── index.html        # QCM noté « examen » (export CSV signé SHA-256)
│   ├── entrainement.html # Mode entraînement (correction immédiate)
│   ├── correction/index.html  # Dépôt d'un CSV → note + correction
│   ├── dashboard/index.html   # Formateur : consolide plusieurs CSV (export XLSX)
│   ├── qcm-core.js       # MOTEUR : barème CBM, SHA-256, CSV, scoring (partagé)
│   ├── questions.js      # DONNÉES : banque bilingue
│   └── corrections.js    # DONNÉES : clé + explications
└── assets/
    ├── css/{main.css, components.css}   # variables/thème/layout/a11y ; composants + contrat i18n
    ├── js/
    │   ├── i18n.js              # MOTEUR bilingue (TPLI18N) — cœur du template
    │   ├── navigation.js        # MOTEUR : nav, thème, progression, sidebar
    │   ├── nav-sections.js      # DONNÉES : sous-sections (ancres) par chapitre
    │   ├── accessibility.js     # MOTEUR : panneau ♿
    │   ├── media.js             # MOTEUR : podcast/slides/infographie/polycopié auto
    │   ├── course-data.js       # DONNÉES : COURSE (chapitres + ressources, source unique)
    │   ├── glossaire-data.js    # DONNÉES : GLOSSARY
    │   ├── glossaire-tooltip.js # MOTEUR : auto-surlignage des termes
    │   ├── flashcards.js        # MOTEUR : FlashcardDeck
    │   ├── flashcards-data.js   # DONNÉES : RDC_FLASHCARDS
    │   ├── tools.js             # MOTEUR : 3 patrons d'activités (TPLActivities)
    │   └── animations.js        # MOTEUR : effets au défilement (dernier)
    └── media/{podcasts,slides,infographies}/   # médias par chapitre (déposés à la main, vides par défaut)
```

## Ordre d'inclusion des scripts (page de chapitre)

Les scripts sont chargés **sans `defer`/`async`**, en bas du `<body>` : l'ordre encode les dépendances. Détail et variantes (index, glossaire, activités, QCM) dans `docs/ARCHITECTURE.md` §3.

1. `i18n.js` — **toujours en premier** (expose `TPLI18N`, requis par tous les moteurs).
2. `course-data.js` puis `nav-sections.js` — **données avant** leur moteur.
3. `navigation.js` — lit `COURSE` + `RDC_SECTIONS`.
4. `accessibility.js`, puis `media.js`.
5. `glossaire-data.js` **avant** `glossaire-tooltip.js`.
6. `flashcards.js` puis `flashcards-data.js`.
7. `animations.js` — **en dernier** (purement décoratif).
8. **Bloc inline** d'instanciation/config (ex. `new FlashcardDeck(...)`) — **après** tous les `src`.

> Règle générale : un fichier `*-data.js` doit venir **avant** le moteur qui le lit ; `i18n.js` d'abord ; `animations.js` en dernier ; le `<script>` inline en toute fin.

## Recettes rapides

Quatre gestes courants. Détail complet : `docs/ARCHITECTURE.md` §4.

**Ajouter un chapitre** (→ §4.1)
- Copier `chapitres/01-cadrage.html` vers `chapitres/0N-mon-chapitre.html` (préfixe `NN-` **obligatoire** : `media.js` en extrait le numéro).
- Déclarer le chapitre dans `assets/js/course-data.js` (tableau `chapters`, libellés `{fr,en}`).
- Renseigner les `<h2 id>` du chapitre dans `assets/js/nav-sections.js` (sous-menu pliable).
- Adapter `<title>`, badge, titre, objectifs, sections.

**Ajouter une question au QCM** (→ §4.3 ; skill `cours-qcm-cbm`)
- Ajouter l'entrée dans `QCM/questions.js` (`enonce`/`propositions` en `{fr,en}`, réponse **unique**).
- Ajouter la correction **de même `id`** dans `QCM/corrections.js` (`bonne_reponse_index`, `explication` `{fr,en}`).
- Vérifier l'équilibre des positions de bonnes réponses et le débiaisage des distracteurs.

**Ajouter un terme au glossaire** (→ §4.4 ; skill `cours-glossaire-flashcards-activites`)
- Ajouter `{ fr, en, def:{fr,en}, ex:{fr,en} }` dans `assets/js/glossaire-data.js`.
- L'auto-surlignage (1re occurrence) et la page `glossaire.html` se mettent à jour seuls.

**Ajouter une activité interactive** (→ §4.5 ; skill `cours-glossaire-flashcards-activites`)
- Choisir l'un des 3 patrons de `tools.js` (`TPLActivities`) adapté au sujet.
- L'instancier via un `<script>` inline avec sa config (libellés `{fr,en}`), après les `src`.

> Template de site de cours — **Mohamed EL AFRIT** · code MIT, contenu & prompts CC BY 4.0.
