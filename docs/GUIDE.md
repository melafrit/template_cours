# Guide d'utilisation pas à pas

> **Quand l'utiliser :** dès que vous démarrez un cours avec ce dépôt, gardez ce guide ouvert. Il explique, phase par phase, **quel prompt lancer, quoi préparer, ce que Claude vous renvoie, et où coller le résultat dans le template**. C'est le mode d'emploi opérationnel de la bibliothèque `prompts/`.

Ce dépôt est un **template réutilisable de site de cours** : un site statique HTML/CSS/JavaScript vanilla, hors-ligne, thémable et bilingue (FR/EN). Vous ne le remplissez pas à la main : vous le fabriquez **avec Claude**, en enchaînant les 13 prompts du dossier `prompts/`, chacun produisant un livrable que vous déposez dans l'arborescence du site.

Double licence du dépôt : **MIT** pour le code, **CC BY 4.0** pour le contenu et les prompts. Auteur du template : **Mohamed EL AFRIT**.

---

## 0. Avant de commencer

### 0.1 Le principe fondamental

**On ne génère pas un cours en un seul prompt.** Un cours exact, progressif, motivant, évalué et accessible se construit **étape par étape**, chaque étape consommant la sortie de la précédente. Quatre règles gouvernent tout le dépôt :

1. **Le cadrage d'abord, toujours.** Rien ne se génère tant que le périmètre n'est pas figé. C'est le rôle du prompt `01`, qui pose ses questions **une à une** et produit la **fiche de cadrage** réutilisée par tous les prompts suivants.
2. **Exactitude non négociable.** Chaque prompt de contenu demande à Claude d'**analyser les documents de référence AVANT de rédiger**, de **ne rien inventer** et de **citer ses sources**. En cas de lacune, Claude le signale plutôt que de combler le vide.
3. **Un livrable par prompt.** Chaque prompt a une sortie claire et vérifiable. On valide une étape avant de passer à la suivante.
4. **Le template pilote la forme.** Les prompts connaissent les fonctionnalités du site et produisent des sorties qui s'y insèrent directement, sans bricolage.

> **Règle d'or :** commencez **TOUJOURS** par `01_cadrage_maitre.md`. Sauter cette étape, c'est s'exposer à des chapitres incohérents, un fil rouge bancal et des QCM hors-sujet.

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
├── prompts/        ← les 13 prompts à lancer (ne pas modifier en usage normal)
├── docs/           ← ce guide + votre fiche de cadrage
├── site/
│   ├── index.html              ← page d'accueil
│   ├── chapitres/              ← une page HTML par chapitre
│   ├── QCM/                    ← QCM web
│   │   ├── correction/         ← page de dépôt d'un CSV
│   │   └── dashboard/          ← tableau de bord multi-CSV
│   ├── atelier/
│   │   └── templates/          ← gabarits téléchargeables de l'atelier
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

## 1. La boucle « questions une à une » du prompt maître

C'est le point le plus important du guide, parce que c'est là que tout se joue. Le prompt maître `01_cadrage_maitre.md` ne fonctionne **pas** comme une commande qu'on lance et qu'on oublie : c'est un **dialogue cadré**.

### Ce qui se passe quand vous le lancez

1. **Étape 1 — Analyse documentaire.** Claude commence par produire une **synthèse de lecture** de vos documents : périmètre couvert (et ce qui manque), concepts clés, découpage thématique naturel, termes candidats au glossaire, points de vigilance (zones floues, redondances, éléments potentiellement obsolètes). Il termine par : « Voici ce que j'ai compris. Je vais maintenant te poser quelques questions de cadrage, une par une. »

2. **Étape 2 — Cadrage interactif.** Claude pose **UNE seule question à la fois**, puis **attend votre réponse** avant la suivante. Chaque question vient avec une **recommandation par défaut** fondée sur l'analyse, et des **options numérotées** que vous choisissez d'un simple chiffre. Les questions couvrent, dans l'ordre : langues → public → niveau et objectifs → durée → nombre et découpage des chapitres → fil rouge → évaluation (QCM, CBM, flashcards, QCM papier) → activités interactives → identité visuelle → multimédia et NotebookLM → contraintes (accessibilité, hors-ligne, polycopiés) → périmètre de l'itération.

3. **Étape 3 — Validation.** Quand le cadrage est suffisant, Claude présente un **récapitulatif** et demande explicitement : « Valides-tu ce cadrage ? (oui / je corrige tel point) ». Il **n'avance pas** sans votre « oui » clair.

4. **Étape 4 — Livrables de cadrage** (après validation seulement) : trois blocs nets.
   - **A) Fiche de cadrage** : tableau de toutes les décisions + liste des hypothèses et points à vérifier.
   - **B) Plan du site** : arborescence complète des pages, en précisant pour chacune si elle est bilingue.
   - **C) Feuille de route des prompts** : la liste **ordonnée** des prompts suivants à lancer, avec leurs placeholders **déjà pré-remplis** depuis la fiche de cadrage, pour enchaîner sans ressaisir le contexte.

### Comment bien jouer cette boucle

- **Répondez par un chiffre** quand des options numérotées sont proposées : plus rapide, moins d'ambiguïté. Utilisez « Autre (précise) » dès que votre besoin sort du cadre.
- **Une question = une réponse.** Ne devancez pas Claude en répondant à dix questions d'un coup : le dialogue séquentiel existe pour que chaque décision affine la suivante.
- **Ne sautez jamais l'étape de validation.** La fiche de cadrage est le **contrat de référence** de tout le reste : elle pré-remplit les placeholders des prompts ultérieurs (langues, fil rouge, nombre de chapitres…).
- **Tranchez le bilingue tôt.** Un cours `français + anglais` double le travail de contenu (chaque page, QCM, glossaire, atelier doit exister dans les deux langues). Ce choix conditionne tous les prompts suivants.
- **Sauvegardez la sortie** dans `docs/cadrage.md` avant de passer à la phase 2.

---

## 2. Les quatre phases de production

Le pipeline se déroule en **quatre phases**. Vous pouvez itérer à l'intérieur d'une phase (régénérer un chapitre, retoucher un QCM) sans tout reprendre, mais **ne sautez pas une phase en avant** sans avoir validé la précédente.

| Phase | Objectif | Prompts |
|-------|----------|---------|
| **1 — Cadrage & architecture** | Décider quoi enseigner, à qui, dans quel ordre. | `01`, `02` |
| **2 — Contenu pédagogique** | Rédiger le cœur du cours + le vocabulaire. | `03`, `04`, `06` |
| **3 — Évaluation & activités** | Vérifier les acquis, faire pratiquer. | `05`, `07`, `08`, `11` |
| **4 — Médias & supports** | Fabriquer les supports téléchargeables et l'écosystème média, puis auditer. | `09`, `10`, `12`, `13` |

> La numérotation des fichiers (`01` → `13`) reflète l'ordre **recommandé** de lecture, mais l'enchaînement réel suit les dépendances de contenu décrites ci-dessous. Quand un doute survient, fiez-vous à la **feuille de route** produite par `01`, qui ordonne les prompts pour *votre* cours précis.

---

## Phase 1 — Cadrage & architecture

*On décide quoi enseigner, à qui, comment, et dans quel ordre.*

### `01_cadrage_maitre.md` — Prompt maître de cadrage

- **Quand :** tout au début, avant tout autre prompt.
- **À préparer :** vos `{{DOCUMENTS_DE_REFERENCE}}` (joints à la conversation) et au moins le `{{SUJET_DU_COURS}}`. Le reste peut rester « à définir avec toi ».
- **Ce que Claude renvoie :** la boucle décrite en section 1 → analyse documentaire, cadrage question par question, validation, puis **fiche de cadrage + plan du site + feuille de route**.
- **Intégration :** enregistrez la **fiche de cadrage** dans `docs/cadrage.md` et le **plan du site** comme référence d'arborescence. Ces deux documents alimentent tous les prompts suivants. Rien à coller dans le site à ce stade : on cadre, on ne code pas.

### `02_plan_syllabus.md` — Plan & syllabus détaillé

- **Quand :** juste après la fiche de cadrage validée.
- **À préparer :** la fiche de cadrage et les `{{DOCUMENTS_DE_REFERENCE}}`.
- **Ce que Claude renvoie :** le **syllabus complet** — liste ordonnée des chapitres avec, pour chacun, objectifs mesurables, durée, notions-clés, place dans le fil rouge, idées d'activités interactives et termes de glossaire pressentis. Le syllabus inclut l'**arborescence des sections** (les ancres de la navigation latérale pliable).
- **Intégration :** c'est le document pivot de la phase 2. Conservez-le (par ex. `docs/syllabus.md`). Il pilote la rédaction de chaque chapitre, le QCM, les flashcards, le glossaire et l'atelier. Servez-vous des sections listées pour créer le squelette des pages dans `site/chapitres/`.

---

## Phase 2 — Contenu pédagogique

*On rédige le cœur du cours, chapitre par chapitre, avec le vocabulaire associé.*

### `03_chapitre.md` — Rédaction d'un chapitre

- **Quand :** une fois le syllabus arrêté. **À lancer une fois par chapitre.**
- **À préparer :** le syllabus, les `{{DOCUMENTS_DE_REFERENCE}}`, le numéro du chapitre visé, et le rappel du `{{FIL_ROUGE}}` et de `{{LANGUES}}`.
- **Ce que Claude renvoie :** un **chapitre complet en HTML**, prêt à coller dans une page du template : accroche motivante, objectifs, sections avec encadrés, exemples reliés au fil rouge, termes de glossaire mis en évidence, encadré « À retenir ». Si le cours est bilingue, la **version anglaise en parallèle** (blocs FR/EN alternés, masqués en CSS, pilotés par la bascule 🌐).
- **Intégration :** créez `site/chapitres/chapitre-N.html` à partir du gabarit de page du template et collez-y le bloc HTML. Vérifiez que les ancres de section correspondent au sous-menu de navigation. Répétez pour chaque chapitre.

### `04_relecture_pedagogique.md` — Relecture & amélioration

- **Quand :** après avoir rédigé un chapitre (brouillon ou version « presque finie »), ou sur un contenu existant à remettre à niveau. Sert aussi d'audit qualité avant publication.
- **À préparer :** le texte du chapitre à relire + les `{{DOCUMENTS_DE_REFERENCE}}` pour vérifier les faits.
- **Ce que Claude renvoie :** une relecture critique sur la clarté, la motivation, l'**exactitude des faits/dates/références**, la progression, les exemples et l'équilibre — avec des propositions d'amélioration ciblées, **avant** réécriture.
- **Intégration :** appliquez les corrections retenues directement dans le HTML du chapitre concerné dans `site/chapitres/`. Bouclez `03` → `04` autant de fois que nécessaire jusqu'à stabilisation du chapitre.

### `06_glossaire.md` — Glossaire bilingue + info-bulles

- **Quand :** une fois les chapitres rédigés (ou bien avancés) — on ne peut décider quels termes surligner qu'en connaissant le vocabulaire réellement employé.
- **À préparer :** les chapitres rédigés et la fiche de cadrage.
- **Ce que Claude renvoie :** le **glossaire bilingue FR/EN** (termes + définitions + exemples) **et** la liste curatée des termes à **auto-surligner** dans le texte des chapitres.
- **Intégration :** alimentez la page `glossaire.html` (recherche + filtre alphabétique) et le mécanisme d'info-bulles (`assets/js/glossaire-data.js` pour les données, `assets/js/glossaire-tooltip.js` pour le survol). Une fois en place, les termes s'auto-surlignent dans les chapitres avec une info-bulle (définition + exemple, FR/EN) reliée à la page glossaire.

> **Flashcards :** si votre cadrage prévoit des flashcards de révision (recto/verso, « su / à revoir », persistance localStorage), générez-les à partir des chapitres et du glossaire, puis alimentez le jeu de cartes par chapitre du template. Cohérence garantie si vous le faites après le glossaire.

---

## Phase 3 — Évaluation & activités

*On vérifie les acquis et on fait pratiquer.*

### `05_activites_interactives.md` — Activités interactives sur mesure

- **Quand :** après avoir défini le squelette du cours et au moins un chapitre.
- **À préparer :** la fiche de cadrage, les chapitres concernés, le fil rouge.
- **Ce que Claude renvoie :** Claude **propose d'abord** les patrons les plus pertinents pour *votre* sujet (assistant de décision pas-à-pas, quiz-classificateur à feedback, calculateur/simulateur, checklist à score, fiches-résumés), **clarifie** le besoin avec vous (une question à la fois), puis **génère** le contenu/les données de l'activité choisie en **HTML/JS vanilla + i18n FR/EN**.
- **Intégration :** insérez le bloc HTML/JS dans la page du chapitre visé (ou une page d'activité dédiée) et déclarez les libellés dans le dictionnaire i18n. Choisissez les activités **selon le sujet** : pas de gadget générique.

### `07_qcm_banque.md` — Banque de QCM (CBM)

- **Quand :** après avoir rédigé le contenu du ou des chapitres concernés, pour que les questions collent à ce qui a été enseigné.
- **À préparer :** les chapitres, leurs objectifs, `{{NB_CHAPITRES}}` et le nombre de questions souhaité par chapitre.
- **Ce que Claude renvoie :** une **banque de QCM à notation CBM** — questions à **réponse unique**, **positions des bonnes réponses équilibrées** (ex. 25 % / 25 % / 25 % / 25 %), **distracteurs débiaisés** (la bonne réponse n'est jamais systématiquement la plus longue). Difficulté indicative seulement.
- **Intégration :** chargez la banque dans le moteur de QCM du template. Vous obtenez les modes **Examen** et **Entraînement**, l'**export CSV signé en SHA-256** (intégrité, hors-ligne), la page de **correction** (`site/QCM/correction/`, dépôt d'un CSV) et le **tableau de bord** (`site/QCM/dashboard/`, plusieurs CSV). Rappel du barème : certitude Élevée +3/−3, Moyenne +2/−2, Faible +1/0 ; note /20 = score_brut ÷ (3 × nb_questions) × 20.

### `08_qcm_papier.md` — QCM papier imprimable (DOCX)

- **Quand :** après avoir validé la banque de questions (`07`).
- **À préparer :** la banque de QCM validée.
- **Ce que Claude renvoie :** la **version papier** du même QCM, en fichiers **DOCX noir & blanc compacts** : `QCM_questions.docx` (page de garde + consignes + barème CBM **avec exemples chiffrés** + questions en **2 colonnes**), `QCM_grille_reponses.docx` (grille A/B/C/D + certitude F/M/É, seul document ramassé), et le **corrigé formateur**.
- **Intégration :** placez le script de génération dans `tools/` et les DOCX produits parmi les ressources téléchargeables. Imprimez pour les sessions sans écran.

### `11_atelier_templates.md` — Atelier fil rouge + templates

- **Quand :** une fois le plan arrêté et le fil rouge défini, en cohérence avec le QCM.
- **À préparer :** le scénario fil rouge, le plan, `{{FIL_ROUGE}}`.
- **Ce que Claude renvoie :** l'**atelier fil rouge** complet — mission, livrables, critères d'évaluation, **templates téléchargeables** (DOCX/XLSX) que l'étudiant complète, et **corrigé formateur** — plus le **contenu HTML** intégrable dans la page « Atelier » et les **scripts Python** qui fabriquent les fichiers.
- **Intégration :** collez le contenu pédagogique dans `site/atelier/`, déposez les gabarits générés dans `site/atelier/templates/`, et rangez les scripts Python dans `tools/`.

---

## Phase 4 — Médias & supports, puis audit

*On fabrique les supports imprimables/téléchargeables, on prépare l'écosystème média, et on contrôle la qualité.*

### `12_polycopies.md` — Polycopiés de synthèse (DOCX + PDF)

- **Quand :** une fois les chapitres rédigés et stabilisés.
- **À préparer :** les chapitres et leurs « à retenir ».
- **Ce que Claude renvoie :** **par chapitre**, un polycopié de synthèse académique (mini-sommaire, encadrés colorés, tableau récapitulatif, « à retenir ») exporté simultanément en **DOCX et PDF** via un **script Python unique** (`tools/generate_polycopies.py`, basé sur `python-docx` + `fpdf2`).
- **Intégration :** placez `generate_polycopies.py` dans `tools/`, lancez-le (`python tools/generate_polycopies.py`), puis proposez les DOCX/PDF en téléchargement par chapitre. Les polycopiés doivent rester **strictement cohérents** avec le contenu du site.

### `09_notebooklm_fiche.md` — Fiche de cours pour NotebookLM

- **Quand :** une fois la structure et les contenus des chapitres existants.
- **À préparer :** les chapitres et le plan.
- **Ce que Claude renvoie :** **un document de synthèse unique et dense** (à exporter en `.docx`) à déposer dans **NotebookLM comme source principale**. Sa fidélité et sa densité conditionnent directement la qualité des médias générés ensuite.
- **Intégration :** exportez en `.docx`, déposez-la dans NotebookLM comme source. Enchaînez avec `10`.

### `10_notebooklm_18prompts.md` — Prompts NotebookLM (infographie / slides / podcast)

- **Quand :** une fois les chapitres existants (au moins leur plan détaillé) et la fiche `09` déposée dans NotebookLM.
- **À préparer :** les chapitres, déposés comme sources dans le notebook (les prompts *pilotent* la génération, ils ne remplacent pas les sources).
- **Ce que Claude renvoie :** un **générateur de prompts** : pour chaque chapitre, 3 prompts NotebookLM autonomes (infographie de synthèse, slides, podcast en dialogue pédagogique), prêts à coller, chacun ≤ 5200 caractères.
- **Intégration :** collez chaque prompt dans NotebookLM, récupérez les médias, puis rangez-les :
  - le **podcast** audio → `site/assets/media/podcasts/` (lecteur personnalisé : lecture, ±10 s, mini-lecteur flottant déplaçable, pop-out, téléchargement) ;
  - les **slides** PDF → `site/assets/media/slides/` (popup plein écran) ;
  - l'**infographie** → `site/assets/media/infographies/` (lightbox avec zoom).

### `13_accessibilite_qa.md` — Accessibilité & contrôle qualité

- **Quand :** à la toute fin, une fois toutes les pages, le QCM, les ateliers, le glossaire et les médias en place. À relancer après chaque correction majeure et juste avant publication.
- **À préparer :** le site assemblé (toutes les pages et tous les médias).
- **Ce que Claude renvoie :** une **passe d'audit complète puis de correction** : accessibilité (WCAG / RGAA), responsive mobile, **cohérence bilingue FR/EN**, validité des liens, **intégrité du QCM**, vérification des médias. Vérifie aussi le panneau de réglages d'accessibilité (taille du texte A+/A−, police « lecture adaptée » Atkinson Hyperlegible, lien « aller au contenu », respect de `prefers-reduced-motion`, persistance).
- **Intégration :** appliquez les correctifs proposés dans les fichiers du site, puis **revérifiez au navigateur** (section 3).

---

## 3. La vérification au navigateur (incontournable)

Aucun livrable n'est « terminé » tant que vous ne l'avez pas **ouvert dans un navigateur** et essayé. Le site est statique et hors-ligne : ouvrez `site/index.html` directement, ou servez le dossier en local. À chaque intégration, contrôlez :

- **Bascule de langue 🌐** : tout le contenu visible bascule FR ↔ EN (pages, navigation, QCM, ateliers, glossaire). Aucun bloc orphelin ne reste dans la mauvaise langue. L'attribut `data-lang` sur `<html>` change bien, et les libellés d'UI générés en JS suivent le dictionnaire i18n.
- **Navigation latérale** : le sous-menu pliable des sections s'ouvre/se ferme, et chaque ancre amène à la bonne section.
- **Glossaire** : les termes sont **auto-surlignés** dans les chapitres, l'info-bulle au survol affiche définition + exemple (FR/EN) et renvoie à la page glossaire.
- **Médias** : le podcast lit, avance/recule de ±10 s, le mini-lecteur flottant se déplace et se détache ; les slides s'ouvrent en popup plein écran ; l'infographie s'agrandit en lightbox.
- **QCM** : les modes Examen/Entraînement fonctionnent, la notation CBM calcule la note /20, l'export CSV est signé (SHA-256), la page de correction et le tableau de bord acceptent les CSV — **le tout hors-ligne**, sans serveur.
- **Flashcards** : recto/verso, statut « su / à revoir » persistant après rechargement (localStorage).
- **Accessibilité** : A+/A−, police « lecture adaptée », lien « aller au contenu », `prefers-reduced-motion` respecté, réglages persistants.
- **Responsive** : réduisez la fenêtre (ou mode mobile des outils de dev) ; la mise en page tient.

> **Boucle de qualité :** repérez un défaut → corrigez le fichier (ou régénérez le livrable via le prompt concerné) → **rechargez la page** → revérifiez. Le prompt `13` automatise l'audit, mais **rien ne remplace l'œil sur la page réelle**.

---

## 4. Récapitulatif du pipeline

```
Phase 1 — Cadrage & architecture
  01  Prompt maître (questions une à une) ........ fiche de cadrage + plan + feuille de route
  02  Plan & syllabus ........................... syllabus + arborescence des sections

Phase 2 — Contenu pédagogique
  03  Chapitre (1 par chapitre) ................. HTML bilingue → site/chapitres/
  04  Relecture pédagogique ..................... corrections appliquées au HTML
  06  Glossaire + info-bulles ................... glossaire.html + glossaire-data.js / -tooltip.js
      (+ flashcards si prévues)

Phase 3 — Évaluation & activités
  05  Activités interactives .................... HTML/JS vanilla + i18n dans les chapitres
  07  Banque QCM (CBM) .......................... moteur QCM + correction/ + dashboard/
  08  QCM papier (DOCX) ......................... questions + grille + corrigé → tools/
  11  Atelier fil rouge + templates ............. site/atelier/ + atelier/templates/ + tools/

Phase 4 — Médias & supports, puis audit
  12  Polycopiés (DOCX + PDF) ................... tools/generate_polycopies.py
  09  Fiche NotebookLM .......................... .docx → source NotebookLM
  10  Prompts NotebookLM ........................ médias → assets/media/{podcasts,slides,infographies}
  13  Accessibilité & QA ........................ audit + corrections → VÉRIFIER AU NAVIGATEUR
```

> **À chaque étape :** un seul livrable, validé avant de continuer ; exactitude vérifiée contre les documents de référence ; et un passage au navigateur avant de déclarer l'étape close.

---

> **Auteur du template :** Mohamed EL AFRIT · **Licence :** CC BY 4.0 (contenu et prompts), MIT (code).
