# Architecture du template de site de cours

Document technique pour développeurs. But : comprendre l'organisation du site et l'**étendre** (ajouter un chapitre, des médias, une question de QCM, un terme de glossaire, une activité, changer le thème) sans rien casser.

Le site (`site/`) est **100 % statique** : HTML + CSS + JavaScript *vanilla*, aucun build, aucune dépendance npm, aucun framework. Il est **bilingue FR/EN** (une seule bascule agit sur tout) et **fonctionne hors-ligne** (ouverture directe d'un fichier en `file://`). Les données du cours vivent dans des fichiers JS (`window.XXX = …`) ; les « moteurs » JS les lisent et génèrent l'interface.

---

## 1. Arborescence de `site/`

```
site/
├── index.html                  # Accueil (présentation + vitrine des fonctionnalités)
├── cours.html                  # Sommaire : grille des chapitres + ressources
├── glossaire.html              # Glossaire bilingue filtrable (rendu JS depuis GLOSSARY)
├── activites.html              # Démos des 3 patrons d'activités de tools.js
├── atelier.html                # Atelier « fil rouge » (page de contenu statique)
├── podcasts.html               # La série de podcasts : lecteur, résumé, diapositives (module 03)
├── about.html                  # À propos / crédits / licences
│
├── chapitres/                  # Une page HTML par chapitre
│   ├── 01-cadrage.html         # ← CHAPITRE MODÈLE : copier celui-ci pour en créer un
│   ├── 02-structurer.html
│   ├── 03-multimedia.html
│   ├── 04-evaluer.html
│   └── 05-accessibilite-diffusion.html
│
├── QCM/                        # Module QCM autonome (4 pages + logique partagée)
│   ├── index.html              # QCM noté « conditions d'examen » (export CSV signé)
│   ├── entrainement.html       # Mode entraînement (correction immédiate)
│   ├── correction/index.html   # Dépôt d'un CSV → note + correction détaillée
│   ├── dashboard/index.html    # Espace formateur : consolide plusieurs CSV (export XLSX)
│   ├── qcm-core.js             # MOTEUR : barème CBM, SHA-256, CSV, scoring (partagé)
│   ├── questions.js            # DONNÉES : banque de questions bilingue
│   └── corrections.js          # DONNÉES : clé de correction + explications
│
└── assets/
    ├── css/
    │   ├── main.css            # Design system : variables (:root), thème, layout, a11y
    │   └── components.css      # Composants : callouts, cartes, glossaire, contrat i18n
    ├── js/
    │   ├── i18n.js             # MOTEUR : bascule FR/EN (cœur du template), racine du site
    │   ├── langue.js           # MOTEUR : bouton FR / EN du site miroir (chargé par navigation.js)
    │   ├── langues-data.js     # DONNÉES ⚙️ : pages qui ont leur jumelle anglaise sous en/
    │   ├── navigation.js       # MOTEUR : arbre de nav, thème, progression, sidebar
    │   ├── nav-sections.js     # DONNÉES : sous-sections (ancres) par chapitre
    │   ├── accessibility.js    # MOTEUR : panneau ♿ (taille texte, police DYS, skip-link)
    │   ├── media.js            # MOTEUR : chargement auto podcast/slides/infographie/polycopié
    │   ├── podcasts.js         # MOTEUR : bande des diapositives et visionneuse de la page Podcasts
    │   ├── flashcards.js       # MOTEUR : FlashcardDeck (cartes de révision)
    │   ├── flashcards-data.js  # DONNÉES : cartes par chapitre
    │   ├── glossaire-tooltip.js# MOTEUR : surligne les termes du glossaire dans le texte
    │   ├── glossaire-data.js   # DONNÉES : termes du glossaire (FR/EN, def, ex)
    │   ├── course-data.js      # DONNÉES : chapitres + ressources (source unique)
    │   ├── tools.js            # MOTEUR : 3 patrons d'activités interactives
    │   ├── animations.js       # MOTEUR : révélation au défilement + détails divers
    │   └── quiz.js             # (présent dans le dépôt, non inclus par les pages actuelles)
    └── media/                  # Médias par chapitre (déposés à la main, voir §4.2)
        ├── podcasts/           # chapitre-<N>-podcast.<langue>.mp3 ; diaporamas/ de la série (module 03)
        ├── slides/             # chapitre-<N>-slides.pdf
        └── infographies/       # chapitre-<N>-infographie.png
```

> **Notes d'état réel du dépôt :**
> - Les dossiers `assets/media/*` sont **vides** par défaut (vous déposez vos fichiers). Voir §4.2.
> - `media.js` référence aussi `assets/polycopies/chapitre-<N>-polycopie.pdf|.docx` et `assets/player.html` (pop-out du lecteur audio) : ces emplacements sont **optionnels** et **absents par défaut**. Le code dégrade proprement (rien ne s'affiche si le fichier n'existe pas).
> - `atelier/templates/` existe (vide) ; `atelier.html` est une page de contenu statique.
> - `assets/js/quiz.js` est présent mais **n'est référencé par aucune page** : la logique de quiz active est celle de `QCM/qcm-core.js` + les scripts inline des pages QCM.

---

## 2. Rôle de chaque moteur JS et fichier de données

### 2.1 Le contrat bilingue (à comprendre AVANT tout le reste)

Trois mécanismes coexistent ; un développeur qui ajoute du contenu doit choisir le bon :

1. **Contenu rédigé en HTML** — deux blocs jumelés, l'inactif est masqué *en CSS* :
   ```html
   <span data-tr="fr">Bonjour</span><span data-tr="en">Hello</span>
   ```
   Règles CSS responsables (dans `components.css`) :
   ```css
   html[data-lang="fr"] [data-tr="en"] { display: none !important; }
   html[data-lang="en"] [data-tr="fr"] { display: none !important; }
   ```
   `i18n.js` ne touche pas à ces nœuds : il bascule l'attribut `data-lang` sur `<html>`, et le CSS fait le reste.

2. **Attributs traduisibles** (`aria-label`, `title`, `alt`, `placeholder`) — déclarés en double, échangés par `i18n.js` :
   ```html
   <input data-i18n-ph-fr="Rechercher…" data-i18n-ph-en="Search…" placeholder="Rechercher…">
   <img data-i18n-alt-fr="…" data-i18n-alt-en="…" alt="…">
   ```

3. **UI générée en JS** (nav, QCM, lecteurs, flashcards, activités) — chaque moteur définit ses libellés `{ fr:{…}, en:{…} }`, lit la langue via `TPLI18N.lang()`, et **se ré-affiche** sur l'évènement `tpl:langchange`.

**API publique de `i18n.js`** (objet global `window.TPLI18N`) :

| Méthode | Effet |
|---|---|
| `TPLI18N.lang()` | renvoie `'fr'` ou `'en'` (langue courante) |
| `TPLI18N.set('en')` | change la langue, persiste, émet `tpl:langchange` |
| `TPLI18N.toggle()` | bascule FR↔EN |
| `TPLI18N.refresh(root)` | ré-applique les attributs i18n après injection dynamique de HTML |
| `TPLI18N.supported()` | `['fr','en']` |

`i18n.js` injecte aussi le bouton 🌐 dans `.header-right`, choisit la langue initiale (localStorage `tpl-lang` → langue navigateur → `lang` du document), et applique tout *le plus tôt possible* pour éviter un flash de la mauvaise langue.

### 2.2 Moteurs JS

| Fichier | Rôle | Lit | Persiste (localStorage) |
|---|---|---|---|
| **i18n.js** | Cœur bilingue : bascule FR/EN, bouton 🌐, évènement `tpl:langchange` ; calcule la racine du site (`window.TPL_RACINE`), où les moteurs prennent leurs médias. Une page qui déclare une seule langue (`data-langues`) n'a pas de bouton 🌐. | `data-lang`, `data-langues` du `<html>` | `tpl-lang` |
| **langue.js** | Site miroir (`docs/I18N.md`, partie A) : le bouton FR / EN ouvre la jumelle de la page et s'y replace sur le bloc lu. Chargé par `navigation.js` sur les pages d'une seule langue ; absent si la jumelle n'existe pas. | `TPL_LANGUES` | `tpl-lang` (et `tpl-bascule` en session) |
| **navigation.js** | Construit l'arbre de nav (`#nav-tree`) depuis `window.COURSE` + `window.RDC_SECTIONS` ; gère le **thème** clair/sombre (bouton 🌙/☀️), la **progression** (chapitres terminés, barre, marquage auto au scroll), la **sidebar mobile** et la **barre de lecture**. | `COURSE`, `RDC_SECTIONS` | `tpl-theme`, `tpl-done` |
| **accessibility.js** | Bouton ♿ + panneau : taille du texte (`--fs-scale`), police « lecture adaptée » DYS (Atkinson Hyperlegible, chargée à la demande), skip-link « Aller au contenu ». | — | `rdc-a11y` |
| **media.js** | Sur une page de chapitre `NN-…html`, déduit le numéro `N` et **charge automatiquement** podcast / slides PDF / infographie / polycopié s'ils existent. Construit le lecteur audio personnalisé (±10 s, mini-lecteur flottant déplaçable, pop-out), les popups plein écran (slides, image, polycopié). | fichiers de `assets/media/` et `assets/polycopies/` | — |
| **podcasts.js** | Page Podcasts (module 03) : dessine sous chaque épisode la bande de ses diapositives (vignettes) et ouvre la visionneuse plein écran — ×, Échap, flèches, Début, Fin, glissé, focus gardé dans la fenêtre puis rendu à la vignette. Libellés dans la langue du conteneur. | `data-dossier`, `data-nombre`, `data-episode` des `.pod-diapos` | — |
| **flashcards.js** | Classe `FlashcardDeck(containerId, cards, key)` : carte recto/verso, navigation, « su / à revoir », mélange, barre de progression. Supporte `**gras**` dans les textes. | tableau passé à l'instanciation (souvent `RDC_FLASHCARDS[n]`) | `rdc-flash-<key>` |
| **glossaire-tooltip.js** | Dans les chapitres, repère la 1re occurrence des termes de `window.GLOSSARY` (langue courante) hors titres/liens/code, et y attache une info-bulle (terme + def + exemple + lien glossaire). Re-scanne au changement de langue. | `GLOSSARY` | — |
| **tools.js** | Objet global `window.TPLActivities` : 3 fabriques d'activités interactives pilotées par config (voir §4.5). | config passée à l'appel | — |
| **animations.js** | Révélation des sections au défilement (IntersectionObserver → classe `.visible`, seuil nul : une section plus haute que l'écran apparaît aussi sur téléphone), waveform podcast décorative, encarts repliables, galerie de slides-images (lit `data-slides`). | `data-slides` | — |
| **QCM/qcm-core.js** | `window.QCMCore` : barème **CBM**, SHA-256 autonome (compatible `file://`), construction/lecture/**signature** du CSV, **scoring**, calcul de la note /20, rappel de barème HTML bilingue. Partagé par les 4 pages QCM. | — | — |

### 2.2 bis — Le moteur pédagogique et l'audio

Ces moteurs ont été ajoutés après la première version du template. Ils portent
tout ce qui rend un chapitre interactif.

| Fichier | Rôle | Lit | Persiste (localStorage) |
|---|---|---|---|
| **ui-labels.js** | `window.UI_LABELS` + l'accesseur `T('cle')` : **tous** les textes d'interface fabriqués en JavaScript, en FR et EN. Un libellé écrit en dur dans un moteur est un défaut : il ne se traduira pas. | `TPLI18N.lang()` | — |
| **interactions.js** | `window.RDCX` — le moteur pédagogique. Sept composants : `checkpoint` (point de contrôle ; avec `pourquoi` et `approfondir`, il explique chaque proposition écartée et propose des renvois — internes dans l'onglet, externes dans un nouvel onglet signalé aux lecteurs d'écran), `reveal` (révélation d'une réponse), `spotError` (repérage d'erreurs dans un document), `match` (appariement), `branch` (scénario à embranchements), `hotspots` (schéma à points chauds), `voice` (capsule audio). Plus `steps` (lecture par étapes), `sommaire` (barre de sommaire collante) et le **repli de l'en-tête de chapitre**, montés automatiquement. | attributs `data-step`, `data-sommaire-titre` des sections | `rdc-step-<N>`, `rdc-entete-<page>` |
| **playlist.js** | Panneau latéral rassemblant les pistes du cours, avec enchaînement automatique et tiroir sur mobile. **Filtre par langue** : une piste marquée `langue` n'apparaît que dans cette langue. | `RDC_PLAYLIST` | `rdc-playlist-ouverte` |
| **quiz.js** | Quiz simple en cours de chapitre (distinct du QCM noté, qui vit dans `site/QCM/`). | config passée à l'appel | — |

**`palettes.css`** complète `main.css` : il ne redéfinit que les huit variables
d'identité (`--primary*`, `--accent*`), en thème clair **et** sombre, pour
chacune des cinq palettes. Il se charge **après** `main.css`, et la palette se
choisit par `data-accent` sur `<html>`.

#### Le contrat des composants RDCX

Les moteurs reçoivent des **chaînes**, pas des objets `{fr, en}` : ils ignorent
que le site puisse être bilingue, et c'est ce qui les garde simples. Le bilingue
se règle dans la page :

1. tout le contenu dans un objet `TEXTES = { fr: {…}, en: {…} }` ;
2. une fonction `monter()` qui **vide les conteneurs** puis remonte tout avec la
   langue active — sans le vidage, changer de langue empilerait deux exemplaires
   du même exercice ;
3. `monter()` rejoué sur `tpl:langchange`.

Modèle complet et commenté : `site/chapitres/_modele.html`.

#### Audio bilingue

Un seul appel `RDCX.voice` par chapitre, mais **une source par langue**,
déclarée dans `TEXTES` sous `capsuleSrc`. Convention :
`chapitre-<N>-capsule-<langue>.mp3`. Sans le suffixe de langue, l'auditeur
anglophone entend du français.

La transcription affichée est **générée** depuis la fiche de production par
`outils/synchroniser_capsules.py` : ne pas l'écrire à la main dans la page.

---

### 2.3 Fichiers de données (à personnaliser)

| Fichier | Variable globale | Forme | Consommé par |
|---|---|---|---|
| **course-data.js** | `window.COURSE` | `{ title, subtitle, author, license, chapters:[{num,ico,file,title}], resources:[{ico,href,label}] }` (libellés `{fr,en}`) | navigation.js, pages |
| **nav-sections.js** ⚙️ | `window.RDC_SECTIONS` | `{ "<num>": [{ id, t:{fr,en} }] }` — une entrée par `<h2 id>` du chapitre | navigation.js (sous-menu pliable) |
| **glossaire-data.js** | `window.GLOSSARY` | `[{ fr, en, def:{fr,en}, ex:{fr,en}, alias?:{fr:[],en:[]}, exclus?:{fr:[],en:[]} }]` | glossaire.html, glossaire-tooltip.js, outils/glossaire_emplois.py |
| **glossaire-emplois.js** ⚙️ | `window.GLOSSARY_EMPLOIS` | `{ fr:{ "g-…": [{ p, a, page, section, n }] }, en:{…} }` — où le cours emploie chaque terme, par langue | glossaire.html (« Où en parle-t-on ? ») |
| **flashcards-data.js** | `window.RDC_FLASHCARDS` | `{ "<num>": [{ front:{fr,en}, back:{fr,en}, ref }] }` | pages de chapitre (instanciation `FlashcardDeck`) |
| **QCM/questions.js** | `window.QCM_QUESTIONS` | `{ meta:{…}, questions:[{ id, chapitre, difficulte, enonce:{fr,en}, propositions:[{fr,en}×4] }] }` | pages QCM |
| **QCM/corrections.js** | `window.QCM_CORRECTIONS` | `{ corrections:[{ id, chapitre, difficulte, bonne_reponse_index, explication:{fr,en} }] }` | entrainement, correction, dashboard |
| **playlist-data.js** ⚙️ | `window.RDC_PLAYLIST` | `{ "<num>": { titre, page, pistes:[{ type, titre, src, duree, present, langue }] } }` | playlist.js |
| **langues-data.js** ⚙️ | `window.TPL_LANGUES` | `["chapitres/01-x.html", …]` — les pages qui ont leur jumelle sous `en/` (vide hors site miroir) | langue.js, navigation.js, glossaire-tooltip.js |

**⚙️ = fichier GÉNÉRÉ.** `langues-data.js` est produit par `outils/generer_langues.py`
d'après les fichiers de `site/en/` ; `glossaire-emplois.js`, par
`outils/glossaire_emplois.py` d'après les termes du glossaire et les pages ; `playlist-data.js`, par
`outils/generer_playlist.py` d'après les pages et les fichiers audio réels ;
`nav-sections.js`, par `outils/generer_nav_sections.py` d'après les `<h2 id>` des
chapitres (`nouveau_cours.py` le lance à la création du cours). Les corriger à la
main donne l'illusion d'avoir résolu le problème jusqu'à la régénération
suivante, qui écrase tout sans prévenir.

**Les fragments.** Un chiffre du cas ne s'écrit pas dans une page : il vient de
`outils/referentiel.py` (`VALEURS`, `DUREES`, fragments composés), et
`outils/generer_fragments.py` le réécrit entre des marqueurs
`<!-- FRAGMENT:nom -->…<!-- /FRAGMENT:nom -->`, dans la langue de la page ou du bloc
`data-tr` qui l'entoure. Le contenu entre deux marqueurs est donc généré, lui aussi.
La page Podcasts et les encadrés « Le podcast du chapitre » en sont aussi (fragments
`podcasts`, `podcasts-etat`, `podcasts-mention`, `podcast-N`) : leur source est
`outils/podcasts.py`, et `outils/generer_podcasts.py` publie les fichiers qu'ils
annoncent (MP3 mono à 64 kbit/s, PDF, diapositives WebP), à partir des dépôts de
`Podcasts/`, jamais versionnés.

**Source unique de vérité.** `course-data.js` pilote l'arbre de navigation *partout*. `nav-sections.js` reflète les `<h2 id>` réels de chaque chapitre : relancer `outils/generer_nav_sections.py` après tout ajout, retrait ou renommage de section (`--essai` dit s'il est à jour, sans rien écrire). Les `id` de questions (`Q01`…) doivent **correspondre** entre `questions.js` et `corrections.js`.

---

## 3. Ordre d'inclusion des scripts dans une page (et pourquoi)

Les scripts sont chargés **sans `defer`/`async`**, en bas du `<body>`, donc dans l'ordre d'écriture. Cet ordre encode les **dépendances** : un fichier de données doit être chargé *avant* le moteur qui le lit, et `i18n.js` doit venir *en premier* pour que `TPLI18N` existe quand les autres moteurs s'initialisent.

**Page de chapitre (ordre complet, depuis `01-cadrage.html`) :**

```html
<script src="../assets/js/i18n.js"></script>          <!-- 1. expose TPLI18N (requis par tous) -->
<script src="../assets/js/course-data.js"></script>   <!-- 2. données : COURSE -->
<script src="../assets/js/nav-sections.js"></script>  <!-- 3. données : RDC_SECTIONS -->
<script src="../assets/js/navigation.js"></script>    <!-- 4. lit COURSE + RDC_SECTIONS -->
<script src="../assets/js/accessibility.js"></script> <!-- 5. panneau ♿ -->
<script src="../assets/js/media.js"></script>         <!-- 6. médias du chapitre -->
<script src="../assets/js/glossaire-data.js"></script><!-- 7. données : GLOSSARY -->
<script src="../assets/js/glossaire-tooltip.js"></script><!-- 8. lit GLOSSARY -->
<script src="../assets/js/flashcards.js"></script>    <!-- 9. expose FlashcardDeck -->
<script src="../assets/js/flashcards-data.js"></script><!-- 10. données : RDC_FLASHCARDS -->
<script src="../assets/js/animations.js"></script>    <!-- 11. effets visuels (dernier) -->
<script>
  new FlashcardDeck('flash-ch1', (window.RDC_FLASHCARDS || {})['1'] || [], 'ch1');
</script>
```

**Règles d'ordre à respecter :**
- `i18n.js` **toujours en premier**.
- Chaque fichier `*-data.js` **avant** le moteur qui le consomme : `course-data.js` + `nav-sections.js` avant `navigation.js` ; `glossaire-data.js` avant `glossaire-tooltip.js`. (`flashcards-data.js` peut suivre `flashcards.js` car le deck est instancié plus bas, dans le `<script>` inline.)
- `animations.js` en dernier (purement décoratif).
- Le **bloc inline** d'instanciation/configuration vient après tous les `src`.

**Variantes selon la page :**
- **index/cours/glossaire/activites/atelier/about** : pas de `media.js` ni de tooltip de glossaire (sauf glossaire qui charge `glossaire-data.js` pour son rendu propre). Ex. minimal (accueil) : `i18n → course-data → navigation → accessibility → animations`. (`nav-sections.js` est ajouté quand on veut le sous-menu pliable dans la sidebar.)
- **glossaire.html** : `… glossaire-data.js` puis un `<script>` inline qui rend la grille filtrable.
- **activites.html** : `… tools.js` puis un `<script>` inline avec les 3 configs.
- **QCM (index / entrainement)** : `i18n → nav-sections → navigation → accessibility → qcm-core.js → questions.js [→ corrections.js] → <script inline>`. `corrections.js` n'est chargé que là où il faut corriger (entraînement, correction, dashboard), pas dans le QCM « examen ».
- **QCM/dashboard** : charge en plus `xlsx.full.min.js` depuis un CDN (export Excel) — **seule dépendance réseau réelle** ; elle ne sert qu'au formateur et n'empêche pas le reste de fonctionner hors-ligne.

---

## 4. Recettes pas-à-pas

### 4.1 Ajouter un chapitre

1. **Copier le modèle** `site/chapitres/01-cadrage.html` vers `site/chapitres/06-mon-chapitre.html`. Le préfixe numérique `NN-` est **obligatoire** : `media.js` en extrait le numéro `N`.
2. **Déclarer le chapitre** dans `assets/js/course-data.js`, à la fin du tableau `chapters` :
   ```js
   { num: '6', ico: '🚀', file: '06-mon-chapitre.html',
     title: { fr: "Mon titre", en: "My title" } }
   ```
   La navigation, la barre de progression et le compteur `x/total` se mettent à jour automatiquement.
3. **Adapter le contenu** du nouveau fichier : `<title>`, badge, titre, objectifs, sections. Chaque section de contenu utilise `<section class="content-section">` et chaque sous-titre un `<h2 id="ch6-sN">` **unique**.
4. **Déclarer les sous-sections** dans `assets/js/nav-sections.js` pour le sous-menu pliable :
   ```js
   "6": [
     { id: "ch6-s1", t: { fr: "1. …", en: "1. …" } },
     { id: "ch6-s2", t: { fr: "2. …", en: "2. …" } }
   ]
   ```
   Les `id` doivent correspondre **exactement** aux `<h2 id>` de la page.
5. **Mettre à jour les liens de pagination** dans le chapitre précédent (`…05….html` : bouton « Suivant ») et dans le nouveau (« Précédent »/« Suivant »).
6. (Optionnel) **Flashcards** : ajouter une clé `"6"` dans `flashcards-data.js`, et instancier en bas de la page :
   ```js
   new FlashcardDeck('flash-ch6', (window.RDC_FLASHCARDS || {})['6'] || [], 'ch6');
   ```
   (penser au `<div id="flash-ch6"></div>` dans la page.)
7. (Optionnel) Ajouter une carte sur `cours.html` (`concept-grid`) si vous voulez l'exposer dans le sommaire.

### 4.2 Ajouter / charger des médias d'un chapitre (podcast, slides, infographie, polycopié)

`media.js` fonctionne **par convention de nommage**. Aucun code à écrire : déposez le fichier au bon endroit, avec le bon nom (`<N>` = numéro du chapitre).

| Média | Emplacement et nom | Section HTML attendue dans le chapitre |
|---|---|---|
| Podcast | `assets/media/podcasts/chapitre-<N>-podcast.mp3` (ou `.m4a`) | `<section class="podcast-section">…</section>` |
| Slides | `assets/media/slides/chapitre-<N>-slides.pdf` | `<section class="slides-section" data-slides="[]">…</section>` |
| Infographie | `assets/media/infographies/chapitre-<N>-infographie.png` | `<section class="infographie-section">…</section>` |
| Polycopié | `assets/polycopies/chapitre-<N>-polycopie.pdf` (+ `.docx`) | aucun — bouton injecté dans `.chapter-nav` |

Détails utiles :
- Le **modèle** `01-cadrage.html` contient déjà ces trois `<section>` avec un texte de remplacement (« déposez un fichier… »). Si le média existe, `media.js` remplace le placeholder ; sinon, le placeholder reste (aucune erreur visible).
- Pour les **slides**, gardez `data-slides="[]"` : c'est le mode PDF géré par `media.js`. (Le mode « galerie d'images » d'`animations.js` ne s'active que si `data-slides` contient un tableau d'URL non vide — usage alternatif.)
- **En `http(s)`**, `media.js` fait un `fetch HEAD` pour vérifier l'existence du fichier avant d'afficher. **En `file://`**, la vérification est impossible : l'aperçu est activé d'office (PDF/infographie). C'est pourquoi `preload='auto'` est utilisé pour l'audio (fichier entièrement *seekable* en local).
- La **série de podcasts** (module 03, bloc `podcasts`) réutilise ces fichiers : l'épisode nommé `chapitre-<N>-podcast` joue, sur la page Podcasts, le MP3 que lit le chapitre ; ses diapositives et ses textes viennent de `outils/podcasts.py` et de `outils/generer_podcasts.py`, et l'encadré « Le podcast du chapitre » (fragment `podcast-N`) y mène depuis l'en-tête du chapitre.
- Le **pop-out** du lecteur audio ouvre `assets/player.html` (à fournir si vous voulez cette fonction ; absent par défaut, le reste du lecteur fonctionne sans).

### 4.3 Ajouter une question au QCM

Une question = **deux** entrées synchronisées par le même `id`.

1. Dans `QCM/questions.js`, ajouter dans `questions` :
   ```js
   {
     id: 'Q13', chapitre: 2, difficulte: 'orange',  // vert|jaune|orange|rouge (indicatif, n'affecte pas la note)
     enonce: { fr: "Énoncé ?", en: "Statement?" },
     propositions: [
       { fr: "Proposition A", en: "Option A" },
       { fr: "Proposition B", en: "Option B" },
       { fr: "Proposition C", en: "Option C" },
       { fr: "Proposition D", en: "Option D" }
     ]
   }
   ```
   Réponse **unique** par question. 4 propositions par convention.
2. Dans `QCM/corrections.js`, ajouter l'entrée correspondante (même `id`) :
   ```js
   {
     id: 'Q13', chapitre: 2, difficulte: 'orange',
     bonne_reponse_index: 1,   // index 0..3 dans le tableau propositions
     explication: { fr: "Pourquoi B est correct.", en: "Why B is correct." }
   }
   ```
3. Mettre à jour `meta.nombre_questions` dans `questions.js` (cohérence d'affichage). La note `/20` se recalcule seule : `note = score_brut ÷ (3 × nb_questions) × 20`, bornée à `[0;20]`.

> **Compatibilité des CSV déjà soumis :** le nombre et l'ordre des questions entrent dans la **signature SHA-256** des fichiers exportés. Modifier la banque **invalide les CSV produits avec l'ancienne version**. Figez la banque pendant une session d'examen.

**Barème CBM** (rappel, défini dans `qcm-core.js`) :

| Certitude déclarée | Bonne réponse | Mauvaise réponse |
|---|---|---|
| Élevée | +3 | −3 |
| Moyenne | +2 | −2 |
| Faible | +1 | 0 |

### 4.4 Ajouter un terme au glossaire

Une seule édition suffit — le terme apparaît **à la fois** dans la page glossaire **et** en info-bulle dans les chapitres.

Dans `assets/js/glossaire-data.js`, ajouter au tableau `window.GLOSSARY` :
```js
{ fr: "terme français", en: "english term",
  def: { fr: "Définition FR.", en: "Definition EN." },
  ex:  { fr: "Exemple FR.",    en: "Example EN." } }
```
- `glossaire.html` régénère sa grille (recherche FR+EN, compteur, suit la bascule de langue).
- `glossaire-tooltip.js` repère automatiquement la **1re occurrence** du terme (dans la langue courante) dans le texte des chapitres et y greffe l'info-bulle. Pour ne lier qu'une sélection de termes, ajoutez `curated: true` aux entrées voulues et décommentez le filtre dans `curated()` (`glossaire-tooltip.js`). Des **alias** (variantes orthographiques → entrée canonique) se règlent dans l'objet `ALIASES` du même fichier.

### 4.5 Ajouter une activité interactive (les 3 patrons de `tools.js`)

`window.TPLActivities` expose 3 fabriques. Schéma commun : un `<div id="…"></div>` dans la page + un appel JS qui le remplit. Tout est piloté par des libellés `{ fr, en }`, le `**gras**` est supporté, et l'activité se ré-affiche au changement de langue.

**Patron 1 — `decisionWizard(id, cfg)`** : assistant pas-à-pas (Oui mène au résultat de l'étape, Non passe à l'étape suivante ; `fallback` si on dit Non partout).
```js
TPLActivities.decisionWizard('mon-wizard', {
  icon: '🧭', title: { fr: "…", en: "…" },
  steps: [
    { q: { fr: "Question 1 ?", en: "Question 1?" },
      result: { name: { fr: "Résultat", en: "Result" }, detail: { fr: "Détail", en: "Detail" } } }
  ],
  fallback: { name: { fr: "Sinon…", en: "Otherwise…" }, detail: { fr: "…", en: "…" } }
});
```

**Patron 2 — `checklist(id, cfg)`** : cases à cocher → verdict selon le nombre coché (`{n}` est remplacé par le compte). Les `verdicts` sont évalués du `min` le plus haut au plus bas.
```js
TPLActivities.checklist('ma-checklist', {
  icon: '☑️', title: { fr: "…", en: "…" }, intro: { fr: "Cochez :", en: "Tick:" },
  items: [ { fr: "Item 1", en: "Item 1" }, { fr: "Item 2", en: "Item 2" } ],
  verdicts: [
    { min: 2, cls: 'rdc-tier-1', msg: { fr: "🟢 OK — {n}/2.", en: "🟢 OK — {n}/2." } },
    { min: 0, cls: '',           msg: { fr: "⚪ {n}/2.",       en: "⚪ {n}/2." } }
  ]
});
```

**Patron 3 — `classifier(id, cfg)`** : ranger des exemples dans des catégories ; feedback immédiat + score.
```js
TPLActivities.classifier('mon-quiz', {
  icon: '🗂️', title: { fr: "…", en: "…" },
  categories: [ { key: 'good', label: { fr: "Bon", en: "Good" } },
                { key: 'bad',  label: { fr: "Mauvais", en: "Bad" } } ],
  items: [ { ex: { fr: "Exemple", en: "Example" }, cat: 'good',
             why: { fr: "Parce que…", en: "Because…" } } ]
});
```
Penser à charger `assets/js/tools.js` dans la page (voir `activites.html` pour le modèle complet). Les activités réutilisent les classes CSS `.rdc-*` déjà présentes dans `components.css`.

### 4.6 Changer le thème (variables CSS)

Tout le design system est centralisé dans `assets/css/main.css`, sous forme de **variables CSS**. Deux blocs : `:root` (thème clair) et `[data-theme="dark"]` (thème sombre). `navigation.js` bascule l'attribut `data-theme` sur `<html>` et le persiste (`tpl-theme`).

Variables principales (extraits réels) :
```css
:root {
  --primary: #1b3a5b;              /* couleur institutionnelle */
  --accent:  #c2a14d;              /* doré (accents, focus) */
  --bg-page: #ffffff;  --bg-card: #ffffff;  --bg-card-alt: #f4f6f9;
  --text-primary: #16202e;
  --border: #dde3ec;
  --success: #2f8f5b;  --error: #c0392b;  --info: #2f6f9f;
  --font-display: 'Sora', system-ui, sans-serif;     /* titres / UI */
  --font-body: 'Source Serif 4', Georgia, serif;     /* texte courant */
  --header-height: 64px;
}
[data-theme="dark"] {
  --primary: #4a7fb5;  --accent: #d9bd72;
  --bg-page: #0e1c2f;  --bg-card: #122438;  --text-primary: #e6ecf3;
  --border: #233649;  /* … */
}
```
Pour **rebrander** : modifiez `--primary`, `--accent` et les `--bg-*`/`--text-*` dans **les deux** blocs. Pour changer les polices : modifiez `--font-display`/`--font-body` (et le `<link>` Google Fonts dans le `<head>` des pages, ou des polices locales pour le hors-ligne strict — voir §5).

> **À ne pas redéfinir à la légère :** `--fs-scale` (piloté par le panneau ♿ : `html { font-size: calc(100% * var(--fs-scale,1)); }`) et la surcharge `html.a11y-dys` (police Atkinson Hyperlegible + interlignes). Ces deux mécanismes assurent l'accessibilité ; gardez-les fonctionnels.

---

## 5. Hors-ligne et déploiement

### Fonctionnement hors-ligne

- Le site est **statique et sans build**. Tout l'état utilisateur (langue, thème, progression, réponses de QCM/flashcards, réglages d'accessibilité) vit dans **`localStorage`** ; aucun serveur n'est requis.
- **Ouverture directe en `file://`** : prévue et gérée. `media.js` détecte le protocole : en `file://` il ne tente pas de `fetch HEAD` (qui échouerait) et active directement les aperçus ; le SHA-256 du QCM est une implémentation **autonome** (pas de `crypto.subtle`, qui est indisponible/instable hors contexte sécurisé).
- **Dépendances réseau résiduelles** (non bloquantes) :
  - **Google Fonts** (Sora, Source Serif 4, JetBrains Mono) via `<link>` dans chaque `<head>`, et **Atkinson Hyperlegible** chargée à la demande par `accessibility.js`. Sans réseau, le navigateur retombe sur les polices système (`system-ui`, Georgia…). Pour un **hors-ligne strict**, télécharger ces polices en local et remplacer les `<link>`/l'URL d'`accessibility.js`.
  - **xlsx.full.min.js** (CDN) uniquement sur `QCM/dashboard/` (export Excel formateur). Le reste du module QCM fonctionne sans.
- **Workflow QCM 100 % hors-ligne** : l'étudiant passe le QCM (`QCM/index.html`), télécharge un **CSV signé**, l'envoie au formateur ; la **correction** (`QCM/correction/`) et le **dashboard** (`QCM/dashboard/`) relisent ces CSV et **vérifient la signature** localement, sans aucun appel réseau (hormis le CDN xlsx du dashboard).

### Déploiement (hébergement statique)

Le livrable à publier est le **contenu du dossier `site/`** (il devient la racine du site).

- **Hébergement OVH (l'usage de l'auteur)** : `deploiement/deployer.py`, en SFTP. Les accès
  viennent de `deploiement/config.json` (local, recopié d'un cours à l'autre), la
  destination de `deploiement/destination.json` (versionné, propre au cours). Envoi
  incrémental par carnet déposé sur le serveur au nom du cours ; garde-fou qui refuse le
  dossier d'un autre cours ; `.htaccess`, `.htpasswd`, `.user.ini`, `.ovhconfig` jamais
  écrasés ; zones protégées publiées après leur protection
  (`deploiement/proteger_zones.py`). Mode d'emploi : `deploiement/LISEZMOI.md` ; tests hors
  ligne : `deploiement/tester_deployer.py`.

- **GitHub Pages.** Deux options :
  1. *Branche + dossier* : dans **Settings → Pages**, servir depuis une branche, en pointant le dossier `/site` (si Pages propose `/ (root)` ou `/docs` seulement, déplacer le contenu de `site/` à la racine de la branche de publication, ou utiliser un workflow GitHub Actions qui publie `site/`).
  2. *Workflow Actions* : uploader `site/` comme artefact Pages.
  Les chemins sont **relatifs** (`assets/…`, `../assets/…`), donc le site marche sous un sous-chemin de projet (`https://<user>.github.io/<repo>/`).
- **Tout autre hébergement statique** (Netlify, Cloudflare Pages, S3, Nginx, Apache…) : déposer le contenu de `site/` ; définir `index.html` comme document par défaut. Aucune configuration serveur particulière n'est nécessaire (pas de réécriture d'URL, pas de backend).
- **Distribution hors-ligne** : zipper le dossier `site/` ; le destinataire ouvre `site/index.html`. Pour les médias, déposer les fichiers attendus dans `assets/media/` (et `assets/polycopies/`) avant de zipper, en respectant la convention de nommage du §4.2.
