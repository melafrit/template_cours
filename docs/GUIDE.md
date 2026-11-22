# Guide d'utilisation pas à pas

> **Quand l'utiliser :** dès que vous démarrez un cours avec ce dépôt, gardez ce guide ouvert. Il explique, phase par phase, **quel prompt lancer, quoi préparer, ce que Claude vous renvoie, et où coller le résultat dans le template**. C'est le mode d'emploi opérationnel de la bibliothèque `prompts/`.

Ce dépôt est un **template réutilisable de site de cours** : un site statique HTML/CSS/JavaScript vanilla, hors-ligne, thémable, en une à trois langues (français, anglais, arabe, chaque page avec ses jumelles au même chemin). Vous ne le remplissez pas à la main : vous le fabriquez **avec Claude**, en enchaînant les prompts du dossier `prompts/`, chacun produisant un livrable que vous déposez dans l'arborescence du site.

> **Le chemin le plus court :** remplissez le bloc de paramètres de [`prompts/PROMPT-Cours-parametrable.md`](../prompts/PROMPT-Cours-parametrable.md) et demandez à Claude de **créer le cours**. Il amorce le cours, pose ses questions une à une et déroule les phases ci-dessous avec leurs jalons. Ce guide détaille chaque étape.

Double licence du dépôt : **MIT** pour le code, **CC BY 4.0** pour le contenu et les prompts. Auteur du template : **Mohamed Amine EL AFRIT**.

---

## 0. Avant de commencer

### 0.1 Le principe fondamental

**On ne génère pas un cours en un seul prompt.** Un cours exact, progressif, motivant, évalué et accessible se construit **étape par étape**, chaque étape consommant la sortie de la précédente. Quatre règles gouvernent tout le dépôt :

1. **Le cadrage d'abord, toujours.** Rien ne se génère tant que le périmètre n'est pas figé. C'est le rôle du prompt `01`, appelé par le prompt paramétrable, qui pose ses questions **une à une** et produit la **fiche de cadrage** réutilisée par tous les prompts suivants.
2. **Exactitude non négociable.** Chaque prompt de contenu demande à Claude d'**analyser les documents de référence AVANT de rédiger**, de **ne rien inventer** et de **citer ses sources**. En cas de lacune, Claude le signale plutôt que de combler le vide.
3. **Un livrable par prompt.** Chaque prompt a une sortie claire et vérifiable. On valide une étape avant de passer à la suivante.
4. **Le template pilote la forme.** Les prompts connaissent les fonctionnalités du site et produisent des sorties qui s'y insèrent directement, sans bricolage.

> **Règle d'or :** commencez toujours par le cadrage. Le prompt paramétrable l'ouvre par le prompt `01`, que vous pouvez aussi lancer seul. Sauter cette étape, c'est s'exposer à des chapitres incohérents, un fil rouge bancal et des QCM hors-sujet.

> **Avec Claude Code :** ce dépôt embarque des *skills* (`.claude/skills/`) qui appliquent **automatiquement** les conventions du template. Ouvrez le dépôt dans Claude Code et demandez simplement « **créer un cours** » : l'orchestrateur `creer-cours-template` prend le relais (cadrage question par question, pipeline en 4 phases), et les skills de domaine (bilinguisme, QCM CBM, glossaire/flashcards/activités, supports imprimables) s'activent au besoin. Voir [`.claude/skills/README.md`](../.claude/skills/README.md).

### 0.2 Ce qu'il faut réunir une bonne fois

Avant le premier prompt, rassemblez :

- **Vos documents de référence** (`{{DOCUMENTS_DE_REFERENCE}}`) : textes de loi, supports existants, rapports, normes, articles. C'est la **source de vérité** ; sans eux, l'exigence d'exactitude ne peut pas jouer et Claude risque de combler les vides. Joignez-les réellement à la conversation (fichiers, copier-coller, liens).
- **Une idée de** sujet, public, niveau, durée, langues (français seul **ou** français + anglais) et fil rouge. Ces éléments peuvent rester « à définir avec toi » : `01` vous aidera à les trancher.

### 0.3 Les placeholders

Tous les prompts utilisent la notation `{{NOM_DU_PLACEHOLDER}}`. Remplissez-les **une fois** (idéalement dans la fiche de cadrage produite par `01`), puis réutilisez les mêmes valeurs partout :

| Placeholder | Signification |
|-------------|---------------|
| `{{SUJET_DU_COURS}}` | Intitulé et thème du cours. |
| `{{PUBLIC_CIBLE}}` | À qui s'adresse le cours. |
| `{{NIVEAU}}` | Niveau de prérequis attendu. |
| `{{DUREE}}` | Volume horaire ou durée totale. |
| `{{LANGUES}}` | `français seul` **OU** `français + anglais`. |
| `{{DOCUMENTS_DE_REFERENCE}}` | Sources faisant autorité, à analyser **avant** de rédiger. |
| `{{FIL_ROUGE}}` | Cas pratique continu traversant le cours. |
| `{{NB_CHAPITRES}}` | Nombre de chapitres prévus. |
| `{{AUTEUR}}` | Auteur·rice du cours. |
| `{{LICENCE}}` | Licence du contenu produit. |
| `{{CONTRAINTES}}` | Limites, exclusions, ton, exigences spécifiques. |

> **Astuce :** conservez votre fiche de cadrage dans le dépôt (par ex. `docs/cadrage.md`). Elle devient la mémoire du projet : quand un prompt réclame `{{FIL_ROUGE}}` ou `{{NB_CHAPITRES}}`, vous copiez la valeur depuis la fiche au lieu de la réinventer.

### 0.4 L'arborescence cible

Vos livrables atterrissent dans cette structure (déjà créée, vide au départ) :

```
template_cours/
├── prompts/        ← le prompt paramétrable, ses modules et les seize prompts de production
├── docs/           ← ce guide + votre fiche de cadrage
├── site/
│   ├── index.html              ← page d'accueil
│   ├── en/, ar/                ← les jumelles des autres langues, au même chemin
│   ├── chapitres/              ← une page HTML par chapitre
│   ├── QCM/                    ← QCM web
│   │   ├── correction/         ← page de dépôt d'un CSV
│   │   └── dashboard/          ← tableau de bord multi-CSV
│   ├── atelier.html            ← l'atelier fil rouge
│   ├── atelier/templates/      ← ses modèles téléchargeables, si le cours en fabrique (prompt 11)
│   └── assets/
│       ├── css/                ← thème (variables CSS)
│       ├── js/                 ← moteur QCM, flashcards, glossaire, i18n…
│       └── media/
│           ├── podcasts/       ← audio par chapitre
│           ├── slides/         ← PDF des slides
│           └── infographies/   ← images d'infographie
└── tools/          ← scripts Python (polycopiés, templates, QCM papier)
```

---

## 0 bis. Amorcer la mécanique avant d'écrire

**Le plus simple** : dans le gabarit, la page `generateur/index.html`, ouverte d'un double clic, fabrique le prompt
de lancement à coller dans Claude Code. Il renvoie au tronc et aux modules actifs par leur chemin, et donne le bloc
de paramètres rempli de vos valeurs habituelles. Pour un dossier de cours déjà préparé, il garde les documents en
place et les fait exclure de Git avant tout (`generateur/LISEZMOI.md`). Claude se charge ensuite de ce qui suit.

Le squelette d'un cours ne s'écrit pas à la main :

```bash
cp cours.exemple.json cours.json     # puis remplissez-le
python3 nouveau_cours.py --essai     # ce qu'il ferait, sans rien écrire
python3 nouveau_cours.py             # crée le cours dans le dossier « sortie »
```

Le script produit l'arborescence, la charte, la navigation, les squelettes de
chapitres, les outils et le déployeur. **Il ne rédige aucun contenu** : c'est le
rôle des phases qui suivent. Il écrit aussi :

- `CLAUDE.md` : le contrat de travail du cours, avec les exigences de l'auteur ;
- `deploiement/destination.json` : où ce cours se publie (bloc `publication` de
  `cours.json`) ; le déployeur refuse le dossier d'un autre cours ;
- les **secrets communs** : `outils/elevenlabs.json` et `deploiement/config.json`,
  recopiés tels quels depuis le template, en local, ignorés par Git ;
- le **bloc école** de `cours.json` : les boutons de l'accueil (`outils/accueil.py`),
  les épreuves de chaque filière (`FILIERES`, dans `outils/seances.py`) et les
  sessions (`outils/sessions.py`), avec la promotion et la matière exactes de
  l'application Livrables et les dates réelles. Une session restée sur l'exemple
  du modèle est signalée.

Il **retire aussi le contenu de démonstration** : capsules, schémas, polycopiés,
QCM et glossaire du cours-démo ne partent pas dans votre cours. À leur place,
des squelettes qui montrent la forme. Le chapitre vitrine, lui, est conservé
sous `site/chapitres/_modele.html` : c'est le seul endroit où les composants
sont appelés pour de vrai. **On copie depuis là.**

Vos documents de référence vont dans `sources/`, hors dépôt. C'est eux que
Claude lit avant de poser la moindre question.

## 1. La boucle « questions une à une » du prompt maître

Le prompt maître `01_cadrage_maitre.md`, que le prompt paramétrable appelle à sa phase de cadrage, mène un **dialogue cadré** : il pose ses questions une à une et n'avance qu'avec vos réponses.

### Ce qui se passe quand vous le lancez

1. **Étape 1 · Analyse documentaire.** Claude commence par produire une **synthèse de lecture** de vos documents : périmètre couvert (et ce qui manque), concepts clés, découpage thématique naturel, termes candidats au glossaire, points de vigilance (zones floues, redondances, éléments potentiellement obsolètes). Il termine par : « Voici ce que j'ai compris. Je vais maintenant te poser quelques questions de cadrage, une par une. »

2. **Étape 2 · Cadrage interactif.** Claude pose **UNE seule question à la fois**, puis **attend votre réponse** avant la suivante. Chaque question arrive avec deux à quatre **options cliquables** ; la première est la **recommandation**, fondée sur l'analyse. Les questions couvrent, dans l'ordre : langues → public → niveau et objectifs → durée → nombre et découpage des chapitres → fil rouge → évaluation (QCM, CBM, flashcards, QCM papier) → activités interactives → identité visuelle → multimédia et NotebookLM → contraintes (accessibilité, hors-ligne, polycopiés) → périmètre de l'itération.

3. **Étape 3 · Validation.** Quand le cadrage est suffisant, Claude présente un **récapitulatif** et vous demande, par une question cliquable, de le valider ou d'en corriger un point. Il **n'avance pas** sans votre accord clair.

4. **Étape 4 · Livrables de cadrage** (après validation seulement) : trois blocs nets.
   - **A) Fiche de cadrage** : tableau de toutes les décisions + liste des hypothèses et points à vérifier.
   - **B) Plan du site** : arborescence complète des pages, en précisant pour chacune ses langues (la racine, puis ses jumelles).
   - **C) Feuille de route des prompts** : la liste **ordonnée** des prompts suivants à lancer, avec leurs placeholders **déjà pré-remplis** depuis la fiche de cadrage, pour enchaîner sans ressaisir le contexte.

### Comment bien jouer cette boucle

- **Répondez d'un clic** : l'option recommandée vient en premier. Le champ « Autre » vous laisse écrire votre réponse quand votre besoin sort du cadre.
- **Une question = une réponse.** Ne devancez pas Claude en répondant à dix questions d'un coup : le dialogue séquentiel existe pour que chaque décision affine la suivante.
- **Ne sautez jamais l'étape de validation.** La fiche de cadrage est le **contrat de référence** de tout le reste : elle pré-remplit les placeholders des prompts ultérieurs (langues, fil rouge, nombre de chapitres…).
- **Tranchez les langues tôt.** Chaque langue ajoutée donne à chaque page sa jumelle (QCM, glossaire et atelier compris), écrite une fois la langue racine stable (module 01). Ce choix conditionne tous les prompts suivants.
- **Sauvegardez la sortie** dans `docs/cadrage.md` avant de passer à la phase 2.

---

## 2. Les quatre phases de production

Le pipeline se déroule en **quatre phases**. Vous pouvez itérer à l'intérieur d'une phase (régénérer un chapitre, retoucher un QCM) sans tout reprendre, mais **ne sautez pas une phase en avant** sans avoir validé la précédente.

| Phase | Objectif | Prompts |
|-------|----------|---------|
| **1 · Cadrage & architecture** | Décider quoi enseigner, à qui, dans quel ordre. | `01`, `02` |
| **2 · Contenu pédagogique** | Rédiger le cœur du cours + le vocabulaire. | `03`, `04`, `06`, `06b` |
| **3 · Évaluation & activités** | Vérifier les acquis, faire pratiquer. | `05`, `07`, `08`, `11`, `15` |
| **4 · Médias & supports** | Fabriquer les supports téléchargeables et l'écosystème média, puis auditer. | `09`, `10`, `12`, `13`, `14` |

> La numérotation des fichiers (`01` → `15`) reflète l'ordre **recommandé** de lecture, mais l'enchaînement réel suit les dépendances de contenu décrites ci-dessous. Quand un doute survient, fiez-vous à la **feuille de route** produite par `01`, qui ordonne les prompts pour *votre* cours précis.

---

## Phase 1 · Cadrage & architecture

*On décide quoi enseigner, à qui, comment, et dans quel ordre.*

### `01_cadrage_maitre.md` · Prompt maître de cadrage

- **Quand :** tout au début, avant tout autre prompt.
- **À préparer :** vos `{{DOCUMENTS_DE_REFERENCE}}` (joints à la conversation) et au moins le `{{SUJET_DU_COURS}}`. Le reste peut rester « à définir avec toi ».
- **Ce que Claude renvoie :** la boucle décrite en section 1 → analyse documentaire, cadrage question par question, validation, puis **fiche de cadrage + plan du site + feuille de route**.
- **Intégration :** enregistrez la **fiche de cadrage** dans `docs/cadrage.md` et le **plan du site** comme référence d'arborescence. Ces deux documents alimentent tous les prompts suivants. Rien à coller dans le site à ce stade : on cadre, on ne code pas.

### `02_plan_syllabus.md` · Plan & syllabus détaillé

- **Quand :** juste après la fiche de cadrage validée.
- **À préparer :** la fiche de cadrage et les `{{DOCUMENTS_DE_REFERENCE}}`.
- **Ce que Claude renvoie :** le **syllabus complet**, liste ordonnée des chapitres avec, pour chacun, objectifs mesurables, durée, notions-clés, place dans le fil rouge, idées d'activités interactives et termes de glossaire pressentis. Le syllabus inclut l'**arborescence des sections** (les ancres de la navigation latérale pliable).
- **Intégration :** c'est le document pivot de la phase 2. Conservez-le (par ex. `docs/syllabus.md`). Il pilote la rédaction de chaque chapitre, le QCM, les flashcards, le glossaire et l'atelier. Servez-vous des sections listées pour créer le squelette des pages dans `site/chapitres/`.

---

## Phase 2 · Contenu pédagogique

*On rédige le cœur du cours, chapitre par chapitre, avec le vocabulaire associé.*

### `03_chapitre.md` · Rédaction d'un chapitre

- **Quand :** une fois le syllabus arrêté. **À lancer une fois par chapitre.**
- **À préparer :** le syllabus, les `{{DOCUMENTS_DE_REFERENCE}}`, le numéro du chapitre visé, et le rappel du `{{FIL_ROUGE}}` et de `{{LANGUES}}`.
- **Ce que Claude renvoie :** un **chapitre complet en HTML**, prêt à coller dans une page du template : accroche motivante, objectifs, sections avec encadrés, exemples reliés au fil rouge, termes de glossaire mis en évidence, encadré « À retenir ». Le chapitre s'écrit dans la langue racine ; ses jumelles (anglais, arabe) viennent une fois la racine stable (site miroir, module 01).
- **Intégration :** complétez le squelette de chapitre que `nouveau_cours.py` a créé dans `site/chapitres/`, sur le modèle du chapitre vitrine `_modele.html`, et collez-y le bloc HTML. Vérifiez que les ancres de section correspondent au sous-menu de navigation. Répétez pour chaque chapitre.

### `04_relecture_pedagogique.md` · Relecture & amélioration

- **Quand :** après avoir rédigé un chapitre (brouillon ou version « presque finie »), ou sur un contenu existant à remettre à niveau. Sert aussi d'audit qualité avant publication.
- **À préparer :** le texte du chapitre à relire + les `{{DOCUMENTS_DE_REFERENCE}}` pour vérifier les faits.
- **Ce que Claude renvoie :** une relecture critique sur la clarté, la motivation, l'**exactitude des faits/dates/références**, la progression, les exemples et l'équilibre, avec des propositions d'amélioration ciblées, **avant** réécriture.
- **Intégration :** appliquez les corrections retenues directement dans le HTML du chapitre concerné dans `site/chapitres/`. Bouclez `03` → `04` autant de fois que nécessaire jusqu'à stabilisation du chapitre.

### `06_glossaire.md` · Glossaire bilingue + info-bulles

- **Quand :** une fois les chapitres rédigés (ou bien avancés) ; on ne peut décider quels termes surligner qu'en connaissant le vocabulaire réellement employé.
- **À préparer :** les chapitres rédigés et la fiche de cadrage.
- **Ce que Claude renvoie :** le **glossaire bilingue FR/EN** (termes + définitions + exemples) **et** la liste curatée des termes à **auto-surligner** dans le texte des chapitres.
- **Intégration :** alimentez la page `glossaire.html` (recherche + filtre alphabétique) et le mécanisme d'info-bulles (`assets/js/glossaire-data.js` pour les données, `assets/js/glossaire-tooltip.js` pour le survol). Une fois en place, les termes s'auto-surlignent dans les chapitres avec une info-bulle (définition + exemple, FR/EN) reliée à la page glossaire.

> **Flashcards :** si votre cadrage prévoit des flashcards de révision (recto/verso, « su / à revoir », persistance localStorage), générez-les à partir des chapitres et du glossaire, puis alimentez le jeu de cartes par chapitre du template. Cohérence garantie si vous le faites après le glossaire.

---

## Phase 3 · Évaluation & activités

*On vérifie les acquis et on fait pratiquer.*

### `05_activites_interactives.md` · Activités interactives sur mesure

- **Quand :** après avoir défini le squelette du cours et au moins un chapitre.
- **À préparer :** la fiche de cadrage, les chapitres concernés, le fil rouge.
- **Ce que Claude renvoie :** Claude **propose d'abord** les patrons les plus pertinents pour *votre* sujet (assistant de décision pas à pas, quiz-classificateur à feedback, calculateur/simulateur, checklist à score, fiches-résumés), **clarifie** le besoin avec vous (une question à la fois), puis **génère** le contenu/les données de l'activité choisie en **HTML/JS vanilla + i18n FR/EN**.
- **Intégration :** insérez le bloc HTML/JS dans la page du chapitre visé (ou une page d'activité dédiée) et déclarez les libellés dans le dictionnaire i18n. Choisissez les activités **selon le sujet** : pas de gadget générique.

### `07_qcm_banque.md` · Banque de QCM (CBM)

- **Quand :** après avoir rédigé le contenu du ou des chapitres concernés, pour que les questions collent à ce qui a été enseigné.
- **À préparer :** les chapitres, leurs objectifs, `{{NB_CHAPITRES}}` et le nombre de questions souhaité par chapitre.
- **Ce que Claude renvoie :** une **banque de QCM à notation CBM**, questions à **réponse unique**, **positions des bonnes réponses équilibrées** (ex. 25 % / 25 % / 25 % / 25 %), **distracteurs débiaisés** (la bonne réponse n'est jamais systématiquement la plus longue). Difficulté indicative seulement.
- **Intégration :** chargez la banque dans le moteur de QCM du template. Vous obtenez les modes **Examen** et **Entraînement**, l'**export CSV signé en SHA-256** (intégrité, hors-ligne), la page de **correction** (`site/QCM/correction/`, dépôt d'un CSV) et le **tableau de bord** (`site/QCM/dashboard/`, plusieurs CSV). Rappel du barème : certitude Élevée +3/−3, Moyenne +2/−2, Faible +1/0 ; note /20 = score_brut ÷ (3 × nb_questions) × 20.

### `08_qcm_papier.md` · QCM papier imprimable (DOCX)

- **Quand :** après avoir validé la banque de questions (`07`).
- **À préparer :** la banque de QCM validée.
- **Ce que Claude renvoie :** le rapport de contrôle de la banque, puis la **version papier** du même QCM, que produit le script du gabarit (`tools/generate_qcm_papier.py`). Pour chaque langue, trois fichiers **DOCX noir et blanc compacts** : `QCM_questions.<langue>.docx` (page de garde, consignes, barème CBM **avec exemples chiffrés**, questions en **2 colonnes**), `QCM_grille_reponses.<langue>.docx` (grille A/B/C/D et certitude F/M/É, seul document ramassé) et `QCM_corrige.<langue>.docx`, le **corrigé du formateur**. Le prompt n'écrit aucun script.
- **Intégration :** les fichiers sortent dans `tools/out/`, que Git ignore, et le corrigé n'est jamais publié. Imprimez les questions et la grille pour les sessions sans écran. Une épreuve dont la banque ne se publie pas suit le module 05, sur le modèle du cours CDWFS.

### `11_atelier_templates.md` · Atelier fil rouge + templates

- **Quand :** une fois le plan arrêté et le fil rouge défini, en cohérence avec le QCM.
- **À préparer :** le scénario fil rouge, le plan, `{{FIL_ROUGE}}`.
- **Ce que Claude renvoie :** l'**atelier fil rouge** complet (mission, livrables, critères d'évaluation, **templates téléchargeables** (DOCX/XLSX) que l'étudiant complète, et **corrigé formateur**) plus le **contenu HTML** intégrable dans la page « Atelier » et les **scripts Python** qui fabriquent les fichiers.
- **Intégration :** collez le contenu pédagogique dans `site/atelier.html`, déposez les modèles générés dans `site/atelier/templates/` (le cours crée ce dossier), et rangez les scripts Python dans `tools/`.

### `15_explications_quiz.md` · Expliquer chaque proposition

- **Quand :** dès qu'une question à choix est écrite (point de contrôle, mini-quiz, QCM d'entraînement) ou en lot sur des questions existantes.
- **À préparer :** les questions, la page ou la fiche de chacune, les ancres réelles des pages (`id` des `h2`, `h3`, figures), la bibliographie vérifiée.
- **Ce que Claude renvoie :** pour chaque question, **une raison par proposition écartée** (l'idée fausse qui la rend tentante) et **deux à quatre renvois** « Pour approfondir » vers l'endroit exact du cours ou une référence externe déjà vérifiée.
- **Intégration :** `pourquoi` et `approfondir` dans l'appel `RDCX.checkpoint` (dans `TEXTES` pour une page bilingue, comme dans `_modele.html`) ; puis `python3 outils/verifier_liens.py` contrôle chaque renvoi, fichier et ancre.

---

## Phase 4 · Médias & supports, puis audit

*On fabrique les supports imprimables/téléchargeables, on prépare l'écosystème média, et on contrôle la qualité.*

### `14_capsules_audio.md` · Capsules audio (Eleven v4)

- **Quand :** une fois les pages et les schémas stabilisés ; une capsule reformule pour l'oreille ce que la page dit déjà.
- **À préparer :** la liste des capsules (page, conteneur, nom exact du fichier), `outils/elevenlabs.json` en place (recopié depuis le template).
- **Ce que Claude renvoie :** une **fiche de production** `docs/prompts/Capsules_*.md` au format que lit le générateur : script balisé (une balise de jeu par paragraphe, « speaking slowly » pour une capsule explicative, jamais l'accent, ajouté par le générateur), transcription d'affichage, témoin désigné.
- **Intégration :** `python3 outils/verifier_elevenlabs.py`, puis `python3 outils/generer_audio.py --temoin …` (**l'auteur écoute le témoin**), puis la série, `outils/synchroniser_capsules.py` et `outils/generer_playlist.py`.

### `12_polycopies.md` · Polycopiés de synthèse (DOCX + PDF)

- **Quand :** une fois les chapitres rédigés et stabilisés.
- **À préparer :** les chapitres et leurs « à retenir ».
- **Ce que Claude renvoie :** **par chapitre**, un polycopié de synthèse académique (mini-sommaire, encadrés colorés, tableau récapitulatif, « à retenir ») exporté simultanément en **DOCX et PDF** via un **script Python unique** (`tools/generate_polycopies.py`, basé sur `python-docx` + `fpdf2`).
- **Intégration :** placez `generate_polycopies.py` dans `tools/`, lancez-le (`python tools/generate_polycopies.py`), puis proposez les DOCX/PDF en téléchargement par chapitre. Les polycopiés doivent rester **strictement cohérents** avec le contenu du site.

### `09_notebooklm_fiche.md` · Fiche de cours pour NotebookLM

- **Quand :** une fois la structure et les contenus des chapitres existants.
- **À préparer :** les chapitres et le plan.
- **Ce que Claude renvoie :** **un document de synthèse unique et dense** (à exporter en `.docx`) à déposer dans **NotebookLM comme source principale**. Sa fidélité et sa densité conditionnent directement la qualité des médias générés ensuite.
- **Intégration :** exportez en `.docx`, déposez-la dans NotebookLM comme source. Enchaînez avec `10`.

### `10_notebooklm_18prompts.md` · Prompts NotebookLM (infographie / slides / podcast)

- **Quand :** une fois les chapitres existants (au moins leur plan détaillé) et la fiche `09` déposée dans NotebookLM.
- **À préparer :** les chapitres, déposés comme sources dans le notebook (les prompts *pilotent* la génération, ils ne remplacent pas les sources).
- **Ce que Claude renvoie :** un **générateur de prompts** : pour chaque chapitre, 3 prompts NotebookLM autonomes (infographie de synthèse, slides, podcast en dialogue pédagogique), prêts à coller, dans les limites de NotebookLM : 4 800 caractères pour le podcast, 3 700 pour les slides, retours à la ligne compris.
- **Intégration :** collez chaque prompt dans NotebookLM, récupérez les médias, puis rangez-les :
  - le **podcast** audio → `site/assets/media/podcasts/` (lecteur personnalisé : lecture, ±10 s, mini-lecteur flottant déplaçable, pop-out, téléchargement) ;
  - les **slides** PDF → `site/assets/media/slides/` (popup plein écran) ;
  - l'**infographie** → `site/assets/media/infographies/` (lightbox avec zoom).

  Puis lancez `python3 outils/generer_medias.py` : la page ne charge que les médias de sa liste (`media-data.js`), et un média déposé sans cette étape ne s'affiche pas.

### `13_accessibilite_qa.md` · Accessibilité & contrôle qualité

- **Quand :** à la toute fin, une fois toutes les pages, le QCM, les ateliers, le glossaire et les médias en place. À relancer après chaque correction majeure et juste avant publication.
- **À préparer :** le site assemblé (toutes les pages et tous les médias).
- **Ce que Claude renvoie :** une **passe d'audit complète puis de correction** : accessibilité (WCAG / RGAA), responsive mobile, **cohérence bilingue FR/EN**, validité des liens, **intégrité du QCM**, vérification des médias. Vérifie aussi le panneau de réglages d'accessibilité (taille du texte A+/A−, police « lecture adaptée » Atkinson Hyperlegible, lien « aller au contenu », respect de `prefers-reduced-motion`, persistance).
- **Intégration :** appliquez les correctifs proposés dans les fichiers du site, puis **revérifiez au navigateur** (section 3).

---

## 2 bis. Le moteur pédagogique à votre disposition

Un chapitre n'est pas qu'un texte. `interactions.js` expose `window.RDCX` :

| Composant | Ce qu'il fait |
|---|---|
| `checkpoint` | Point de contrôle : questions à choix, avec l'explication de chaque proposition et des renvois « Pour approfondir » |
| `reveal` | Une question posée AVANT la lecture, dont on révèle la réponse |
| `spotError` | Repérer les affirmations fausses dans un document |
| `match` | Relier deux colonnes |
| `branch` | Un scénario à embranchements, avec les conséquences de chaque décision |
| `hotspots` | Un schéma annoté de points cliquables |
| `voice` | Une capsule audio, avec sa transcription |
| `steps` | La lecture par étapes, section par section, non appelée par défaut : les sections sont dans le menu de gauche |
| `sommaire` | La barre de sommaire collante, non appelée par défaut : les sections sont dans le menu de gauche |

Choisissez selon l'intention, pas selon la nouveauté : un `checkpoint` après
une notion difficile vaut mieux qu'un `branch` plaqué là où rien ne se décide.

## 2 ter. L'école : le programme, le cahier de texte et le classeur Livrables

*Pour un cours donné dans une école qui tient ses séances dans Yparéo et recueille les livrables dans l'application Livrables (module 07, `prompts/modules/07-ypareo-livrables.md`). On y vient une fois les chapitres, l'atelier et les évaluations arrêtés.*

**Le programme ne porte aucune date.** `outils/seances.py` le décrit : les séances en demi-journées (« Jour 1, matin »), le travail à faire, les livrables avec leurs échéances et leur notation, la description de la matière et les ressources. Les dates réelles vivent dans `outils/sessions.py`, une session par promotion, avec la promotion et la matière écrites exactement comme dans l'application. `nouveau_cours.py` les y a mises d'après le bloc école de `cours.json` ; la session d'exemple du modèle se remplace avant tout usage.

| Ce qu'on obtient | Commande | Ce qu'elle lit |
|---|---|---|
| Le programme et les échéances de l'accueil | `python3 outils/generer_fragments.py` | `outils/seances.py` |
| Le cahier de texte Yparéo, en `.txt` et en `.docx` | `python3 outils/generer_cahier_de_texte.py` | `seances.py`, `sessions.py`, les pages des chapitres |
| Le classeur d'import Livrables et ses réglages | `python3 outils/generer_classeur_livrables.py --session <nom>` | `seances.py`, `sessions.py`, le cahier, `deploiement/destination.json` |
| La pastille et les boutons des épreuves de l'accueil | `python3 outils/generer_fragments.py` | `FILIERES`, dans `seances.py` |

**Les contrôles.** `python3 outils/seances.py` vérifie le programme (chaque chapitre placé une fois, chaque échéance après sa séance, des grilles qui totalisent la note maximale) et `FILIERES`. `python3 outils/sessions.py` vérifie les dates : une par jour du programme, un jour ouvré, dans l'ordre. Les deux générateurs ont un `--essai` qui signale un document périmé, sans rien écrire.

**Le cahier de texte.** Un bloc par séance, « CONTENU DE LA SÉANCE » puis « TRAVAIL À FAIRE ». La version sans identifiants sort toujours. Celle qui porte les identifiants du site sort quand `docs/acces.json` existe, et ne quitte jamais le poste. Sans accès à Yparéo, le même texte part dans l'application Livrables, colonne Contenu de la feuille Séances.

**Le classeur Livrables.** Un classeur par promotion, car deux matières nouvelles dans un même fichier se prennent pour des doublons. Les liens viennent du site publié ; sans adresse connue, ils restent vides. À côté du classeur, `docs/Import_Livrables_<session>_reglages.txt` liste ce que l'import ne porte pas :

- la case « Autoriser les fichiers joints », sans laquelle l'étudiant ne rend qu'un lien ;
- la version de travail, jamais notée, et jamais cochée « Livrable bonus, facultatif », qui la rendrait non due ;
- la note d'un QCM passé sur le site, calculée dans son tableau de bord puis saisie dans l'application.

**L'import.** L'auteur relit l'aperçu avant de confirmer : un premier import annonce des créations, un réimport des mises à jour seulement. L'import ne supprime jamais rien, et le titre d'un livrable sert de clé. Un titre changé crée donc un livrable de plus, à retirer à la main.

## 3. La vérification au navigateur (incontournable)

Aucun livrable n'est « terminé » tant que vous ne l'avez pas **ouvert dans un navigateur** et essayé. Le site est statique et hors-ligne : ouvrez `site/index.html` directement, ou servez le dossier en local. À chaque intégration, contrôlez :

- **Bouton des langues** : il mène à la jumelle de la page, au même endroit de lecture. Chaque jumelle est entière dans sa langue, interface comprise (libellés de `ui-labels.js`), et l'arabe se lit de droite à gauche.
- **Navigation latérale** : le sous-menu pliable des sections s'ouvre/se ferme, et chaque ancre amène à la bonne section.
- **Glossaire** : les termes sont **auto-surlignés** dans les chapitres, l'info-bulle au survol affiche définition + exemple (FR/EN) et renvoie à la page glossaire.
- **Médias** : le podcast lit, avance/recule de ±10 s, le mini-lecteur flottant se déplace et se détache ; les slides s'ouvrent en popup plein écran ; l'infographie s'agrandit en lightbox.
- **QCM** : les modes Examen/Entraînement fonctionnent, la notation CBM calcule la note /20, l'export CSV est signé (SHA-256), la page de correction et le tableau de bord acceptent les CSV, **le tout hors-ligne**, sans serveur.
- **Flashcards** : recto/verso, statut « su / à revoir » persistant après rechargement (localStorage).
- **Accessibilité** : A+/A−, police « lecture adaptée », lien « aller au contenu », `prefers-reduced-motion` respecté, réglages persistants.
- **Responsive** : réduisez la fenêtre (ou mode mobile des outils de dev) ; la mise en page tient.

> **Boucle de qualité :** repérez un défaut → corrigez le fichier (ou régénérez le livrable via le prompt concerné) → **rechargez la page** → revérifiez. Le prompt `13` automatise l'audit, mais **rien ne remplace l'œil sur la page réelle**.

---

## 4. Récapitulatif du pipeline

```
Phase 1 · Cadrage & architecture
  01  Prompt maître (questions une à une) ........ fiche de cadrage + plan + feuille de route
  02  Plan & syllabus ........................... syllabus + arborescence des sections

Phase 2 · Contenu pédagogique
  03  Chapitre (1 par chapitre) ................. HTML (langue racine) → site/chapitres/
  04  Relecture pédagogique ..................... corrections appliquées au HTML
  06  Glossaire + info-bulles ................... glossaire.html + glossaire-data.js / -tooltip.js
      (+ flashcards si prévues)
  06b « Où en parle-t-on ? » .................... alias, sens écartés → glossaire_emplois.py

Phase 3 · Évaluation & activités
  05  Activités interactives .................... HTML/JS vanilla + i18n dans les chapitres
  07  Banque QCM (CBM) .......................... moteur QCM + correction/ + dashboard/
  08  QCM papier (DOCX) ......................... questions + grille + corrigé → tools/
  11  Atelier fil rouge + templates ............. site/atelier.html + site/atelier/templates/ + tools/
  15  Explications des quiz ..................... pourquoi + approfondir → verifier_liens.py

Phase 4 · Médias & supports, puis audit
  14  Capsules audio (Eleven v4) ................ fiche → témoin → série → playlist
  12  Polycopiés (DOCX + PDF) ................... tools/generate_polycopies.py
  09  Fiche NotebookLM .......................... .docx → source NotebookLM
  10  Prompts NotebookLM ........................ médias → assets/media/{podcasts,slides,infographies}
  13  Accessibilité & QA ........................ audit + corrections → VÉRIFIER AU NAVIGATEUR

L'école (module 07, si le cours en relève)
      outils/seances.py ......................... le programme, sans date → accueil
      outils/sessions.py ........................ promotions, matières, dates réelles
      generer_cahier_de_texte.py ................ cahier de texte Yparéo (.txt, .docx)
      generer_classeur_livrables.py ............. classeur d'import et réglages → l'auteur importe

Mise en ligne
      deploiement/deployer.py --essai ........... destination.json, garde-fou, puis envoi (après accord)
```

> **À chaque étape :** un seul livrable, validé avant de continuer ; exactitude vérifiée contre les documents de référence ; et un passage au navigateur avant de déclarer l'étape close.

---

> **Auteur du template :** Mohamed Amine EL AFRIT · **Licence :** CC BY 4.0 (contenu et prompts), MIT (code).
