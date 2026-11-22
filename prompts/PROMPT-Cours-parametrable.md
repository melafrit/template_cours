# Prompt paramétrable : créer un cours complet avec ce template

> **Ce que contient ce document.** Le **tronc commun** du prompt réutilisable qui produit,
> avec Claude Code, le site complet d'un cours, et ce qui l'accompagne (évaluations,
> supports formateur, déploiement), à partir de ses propres documents de référence. Les
> options sont des **modules**, un fichier chacun dans `prompts/modules/`, lus seulement
> s'ils sont activés. Le tout réunit ce que les cours précédents de l'auteur ont appris :
> méthode, conventions, écosystème (Yparéo, application Livrables, ElevenLabs, NotebookLM,
> Codex, OVH) et pièges.
>
> **Le principe.** Vous remplissez le **bloc de paramètres** (section 3) ; ce que vous
> laissez vide, Claude le déduit des documents de référence ou vous le demande, **une
> question à la fois**. Ce template est le **gabarit technique** : son moteur, ses outils
> et son déploiement sont repris par `nouveau_cours.py`, pas réécrits. Les cours de
> référence de l'auteur fournissent ce que le gabarit n'a pas encore.
>
> **Le point d'entrée.** Dans Claude Code, demander « créer un cours » déclenche la skill
> `creer-cours-template`, qui suit ce document. Les exigences permanentes de l'auteur sont
> dans `CLAUDE.md` (§ 2), recopié dans chaque cours créé : ce tronc les applique sans les
> répéter.

---

## 1. Mode d'emploi

1. **Remplissez le bloc de paramètres** (section 3), modules compris. Laissez vide ce que
   vous ne savez pas encore : Claude le demandera.
2. **Demandez à Claude de créer le cours** (« crée un nouveau cours sur … avec le
   template »), ou collez le bloc rempli puis le prompt de la section 4 dans le même
   message.
3. Claude **amorce le cours** : il écrit `cours.json`, lance `python3 nouveau_cours.py
   --essai`, vous montre le résultat, puis crée le dossier ; le script recopie en local les
   **secrets communs** (section 2.3), écrit `deploiement/destination.json` et le
   `CLAUDE.md` du cours.
4. **Déposez vos documents de référence** dans `sources/` du nouveau cours (jamais
   versionnés). Claude les lit **tous** avant d'écrire la moindre ligne de contenu.
5. **Répondez aux questions** une à une, et **validez à chaque jalon « STOP »**. Chaque
   module actif s'insère à sa phase (section 4, « Méthode »).

### Les modules

| Module | Fichier, dans `prompts/modules/` | Ce qu'il ajoute | Phase |
|---|---|---|---|
| Bilingue | `01-bilingue.md` | la version anglaise, une fois le français stable | 9 |
| Polycopié | `02-polycopie.md` | le livret Word et PDF, ses QR codes cliquables, sa page sur le site | 10 |
| Podcasts | `03-podcasts-notebooklm.md` | la série NotebookLM, ses diaporamas, sa page sur le site | 11 |
| Audio | `04-audio-elevenlabs.md` | les capsules, à la voix clonée de l'auteur | 8 |
| Évaluations | `05-evaluations.md` | QCM en ligne, papier et d'entraînement, et leur correction publique | 6 |
| TP | `06-tp-correction.md` | le TP et sa correction protégée | 5 |
| École | `07-ypareo-livrables.md` | les cahiers de texte Yparéo, les classeurs d'import de l'application Livrables | 12 |
| Déploiement | `08-deploiement.md` | la mise en ligne, ses garde-fous, ses contrôles | 13 |
| Compléments | `09-complements.md` | schémas, illustrations, simulateurs, glossaire, Boîte à outils, fiches mémo | 7 |

Un module s'utilise aussi **seul**, sur un cours qui existe déjà (lui ajouter un
polycopié, une série de podcasts, sa version anglaise) : donnez le fichier du module à
Claude, dans le dossier du cours. Sa dernière section, « Pour commencer », dit par où
entrer.

---

## 2. Prérequis

### 2.1 Entrées : les documents de référence (`sources/`, lecture seule)

| Document | Indispensable | Ce que Claude en tire |
|---|---|---|
| **Fiche module** (une par titre RNCP concerné) | si le cours relève d'un titre | compétences, objectifs, plan, exercices, volume horaire, bibliographie |
| **Grille d'évaluation de l'épreuve** | si le cours prépare une épreuve | critères, indicateurs, seuils, niveaux : la cible de tout le cours |
| Règlement des examens · fiche récapitulative · matrice de couverture | si disponibles | modalités, coefficients, seuil de validation, articulation module ↔ épreuve |
| **Fil rouge** : fiches de l'épreuve (apprenant, rattrapage, correcteur) | si le module prépare une épreuve fil rouge | le cas, les attendus, la façon dont le correcteur note |
| Modèles, kits, gabarits à faire remplir | si le module a des livrables sur modèle | les livrables, à adapter au cas |
| Ouvrages, diapositives, articles, normes | non | notions et exemples, **jamais recopiés** : reformulés et cités |

### 2.2 Ressources à portée de main

| Ressource | Emplacement |
|---|---|
| Gabarit technique (moteur, outils, déploiement, ce document et ses modules) | `{{ecosysteme.gabarit_technique}}` |
| Cours de référence (ce que le gabarit n'a pas encore, voir l'étape zéro) | `{{ecosysteme.cours_de_reference}}` |
| Format d'import de l'application Livrables | `{{ecosysteme.doc_import_app}}` |
| Épreuves réelles et cadrage des QCM | `{{ecosysteme.epreuves_reelles}}` |

### 2.3 Secrets : fichiers locaux, ignorés par Git, jamais lus

| Fichier | Contenu | D'où il vient |
|---|---|---|
| `outils/elevenlabs.json` | clé API ElevenLabs, identifiant de la voix clonée | recopié tel quel depuis le template par `nouveau_cours.py` |
| `deploiement/config.json` | accès SFTP à l'hébergement (hôte, identifiant, mot de passe, protocole) | recopié tel quel ; son éventuel répertoire distant n'est **jamais lu** |
| `docs/acces.json` | identifiant et mot de passe de consultation du site (pour Yparéo) | propre au cours, déposé par l'auteur |
| `docs/acces-zones.json` | comptes des zones protégées (correction du TP…) | propre au cours |

Le template garde **localement** la copie de référence des deux premiers (jamais sur
GitHub) ; chaque nouveau cours en reçoit une copie octet pour octet. Claude ne les ouvre
pas, ne les affiche pas, ne les demande pas : les scripts s'en servent. Le `.rgignore` du
cours les cache aux recherches ; un filtre de fichiers qui inclut les `.json` passe outre,
et ne s'emploie jamais sans les exclure nommément.

### 2.4 Poste de travail et comptes

Windows 11 (Git Bash, PowerShell) · Python 3.11+ (`paramiko`, `bcrypt`, `python-docx`,
`fpdf2`, `openpyxl`, `Pillow`, `PyMuPDF`, `segno`, `pywin32`) · Microsoft Word (export PDF
du polycopié) · ffmpeg/ffprobe · Node.js · Microsoft Edge ou Google Chrome (captures sans
interface) · `git` et `gh` authentifiés. Comptes selon les modules : ElevenLabs (**Eleven
v4**, voix clonée), NotebookLM, Codex ou ChatGPT (images), OVH (SFTP), GitHub, application
Livrables (promotions créées), Yparéo.

### 2.5 Ce que le cours livre, et à quoi on le reconnaît

| Sortie | Emplacement | Critère d'acceptation |
|---|---|---|
| Le site | `site/` | S'ouvre sans erreur de console, en clair et en sombre, à 1280 et 375 px ; bascules de langue et de filière ; contrôles du § 6 de `CLAUDE.md` sans écart |
| Le référentiel du cas | `outils/referentiel.py` | Source unique des chiffres ; `generer_fragments.py --essai` n'a rien à faire |
| Le programme | `outils/seances.py`, `outils/sessions.py` | Leurs deux contrôles finissent sans écart ; aucune date ailleurs que dans les sessions |
| Les évaluations | `site/QCM/`, points de contrôle des chapitres | Chaque proposition expliquée, deux à quatre renvois ; `verifier_liens.py` sans lien mort |
| Les capsules audio (module 04) | `site/assets/media/voix/`, fiches `docs/prompts/Capsules_*.md` | Témoin écouté par l'auteur ; contrôle de qualité passé ; transcriptions synchronisées |
| Le polycopié (module 02) | `Polycopie/`, `site/livret/` | QR codes relus et cliquables, langue déclarée (`/Lang`) ; le livret publié est celui de `Polycopie/` |
| Le cahier de texte (module 07) | `docs/Cahier_de_texte*.txt` et `.docx` | Un bloc par séance ; la version avec identifiants reste sur le poste |
| L'import Livrables (module 07) | `docs/Import_Livrables_<session>.xlsx` et ses réglages | Accepté par l'aperçu sans refus ni doublon ; réglages faits à la main |
| La mise en ligne (module 08) | `deploiement/` | Essai à blanc comparé à git ; pages publiques en 200, zones protégées en 401 |
| La reprise | `README.md`, `docs/00` à `02`, `TODO.md` | Un repreneur relance tout sans l'auteur |

---

## 3. Paramètres

Recopiez ce bloc, remplissez-le, et collez-le **avant** le prompt. `""` = à déduire des
sources ou à demander. Un module `actif: false` ne laisse aucune trace dans le cours : ni
page, ni entrée de menu, ni générateur.

~~~yaml
# ─────────────────────────────── LE COURS
cours:
  titre: ""                     # ex. « Conception d'architectures logicielles »
  slug: ""                      # identifiant court, sans accent : nom du dossier, destination.json, carnet distant
  auteur: ""                    # nom imprimé : pieds de page, polycopié, crédits des podcasts
  code_module: ""               # ex. FM01
  bloc: ""                      # ex. « Bloc 2 · Concevoir une solution »
  annee: ""                     # ex. 2026-2027
  palette: ""                   # marine | emeraude | prune | ardoise | bordeaux
  langues: ["fr"]               # la racine d'abord (fr ou en), puis les jumelles à venir : ["fr", "en", "ar"] → cours.json
  public: ""                    # par ses prérequis et ses contraintes, pas par l'intitulé du diplôme
  formats: []                   # ex. ["2j", "3j"] ; un seul = pas de bascule
  format_impose: ""
  calendrier: {}                # dates réelles : SEULEMENT pour Yparéo et l'application (→ cours.json, ecole.sessions)
  horaires: {matin: "09:00-12:30", apres_midi: "13:30-17:00"}
  ton: "vouvoiement chaleureux, registre d'un collègue expérimenté ; peu d'écrit, beaucoup de pratique"

# ─────────────────────────────── LES FILIÈRES (une seule, ou aucune : pas de bascule) → cours.json, « filieres »
filieres:
  - id: ""                      # ex. "eadl" : nomme la classe only-<id> du contenu propre à la filière
    code: ""                    # le sigle affiché, ex. "EADL"
    nom: ""                     # intitulé du titre RNCP
    court: ""                   # son nom court
    rncp: ""
    palette: ""                 # la teinte quand l'étudiant a choisi sa filière (mêmes valeurs que cours.palette)
    competences: []             # sinon lues dans la grille
    epreuve: ""                 # ex. EC01
    bloc: ""                    # ex. « Bloc 1 » : avec le module, la pastille de l'accueil, « EADL, Bloc 1, module FM04 »
    module: ""                  # ex. FM04
    page_epreuves: ""           # adresse de la page des épreuves du bloc, ouverte avant d'être ajoutée
                                # (→ cours.json, filieres[].epreuves : le bouton « Épreuves du <bloc> » de l'accueil)
    fiche_module: ""            # chemin dans sources/
    grille: ""                  # chemin dans sources/
    promotion_app: ""           # EXACTEMENT « Année › Promotion » de l'application (→ cours.json, ecole.sessions)
    matiere_app: ""             # nom exact de la matière dans l'application (→ cours.json, ecole.sessions)
groupe_mixte: false             # un seul cours pour plusieurs filières

# ─────────────────────────────── LE FIL ROUGE
fil_rouge:
  nom: ""                       # le cas qui traverse tout le cours
  source: "sources/…"
  projet_par_filiere: {}
  referentiel: "outils/referentiel.py"   # source unique des chiffres du cas, écrits dans les pages par generer_fragments.py
interdits: []                   # mots et exemples à ne jamais employer hors de leur place (sujet du TP, épreuve…)

# ─────────────────────────────── LES LIVRABLES (dans l'ordre du cours)
livrables:
  - id: ""
    titre: ""
    modele: ""                  # chemin du modèle dans sources/, ou "" s'il est à créer
    format_depot: ""
    version_de_travail: {existe: true, notee: false, obligatoire: false, jour: 1, heure: "12:30"}
    version_finale: {jour: 2, heure: "12:30", note_max: 20, coefficient: 1, grille: true}
malus_version_de_travail: 0

# ─────────────────────────────── LES MODULES (un fichier chacun dans prompts/modules/)
modules:
  bilingue:                     # 01 : les pages jumelles d'une autre langue, une fois la racine stable
    actif: false
    modele: "miroir"            # pages jumelles sous en/ ; "data-tr" (blocs jumelés) en secours : voir le module
  polycopie:                    # 02 : le livret Word et PDF
    actif: false                # (cours.json : le bloc « livret » amène la chaîne et la page ; il demande le glossaire)
  podcasts:                     # 03 : NotebookLM
    actif: false
    episodes: 0                 # 0 = à proposer (le cours de référence en compte 12)
    diaporamas: true            # un diaporama par épisode
                                # (cours.json : le bloc « podcasts » amène la page et ses outils)
  audio:                        # 04 : ElevenLabs
    actif: true
    capsules: []                # ex. ["accueil", "ouverture de chapitre", "un par schéma", "TP pas à pas"]
  evaluations:                  # 05
    qcm_en_ligne: {actif: true, notation: "CBM", questions: 0}
    qcm_papier: {actif: false, questions: 0, propositions: 4, certitude: "", un_par_filiere: false}
    qcm_entrainement: {actif: true, questions_par_filiere: 0}
    correction_publique: true   # la page « Correction des QCM », juste après l'entraînement
    points_de_controle: true    # un par section importante
  tp:                           # 06
    actif: false
    sujet: ""                   # distinct de l'exemple du cours : le cours n'en souffle rien
  ecole:                        # 07 (→ cours.json, « ecole »)
    ypareo: true
    livrables_app: true         # son adresse : ecosysteme.app_livrables
    bouton_qcm: true            # un bouton « QCM d'évaluation » sur l'accueil, vers le QCM du site
  deploiement:                  # 08
    actif: true
    url: ""                     # adresse publique du cours
    repertoire_distant: ""      # dossier PROPRE à ce cours → deploiement/destination.json
    zones_protegees: []         # ex. ["correction/", "correction/formateur/"]
    site_protege: false         # tout le site derrière un mot de passe, posé côté serveur
  complements:                  # 09
    schemas: {actif: true, capsule_par_schema: false}
    illustrations: {actif: false, outil: "Codex"}
    simulateurs: []
    glossaire: true
    boite_a_outils: {actif: false, fiches: 0}
    fiches_memo: false
    encarts_plus_loin: []

# ─────────────────────────────── L'ÉCOSYSTÈME
ecosysteme:
  gabarit_technique: "C:/projets/Cours/template_cours"
  cours_de_reference:
    - "C:/projets/Cours/Cours_Architecture_Logicielle"        # site miroir en/, polycopié FR/EN à QR codes cliquables, page Podcasts, Boîte à outils, quiz expliqués et leur correction publique, schémas et leurs lectures, fragments générés, correction protégée, audio v4
    - "C:/projets/Cours/Cours_EADL_ERIS_Etude_Avant_Projet"   # deux filières, site entièrement protégé, version anglaise, correction de TP, générateurs de glossaire et de flashcards, import Livrables, Yparéo, audio v4
    - "C:/projets/Cours/Cours_CDWFS_ASRC_Etude_Avant_Projet"  # groupe mixte et bascule de filière, QCM papier à certitude, fiches mémo
  app_livrables: "https://livrables.elafrit.com/"
  doc_import_app: "C:/projets/Livrables_App_Etudiants/docs/PROMPT-CLASSEUR-IA.md"
  epreuves_reelles: ""

# ─────────────────────────────── GIT
git:
  depot: ""                     # ex. melafrit/<Cours>
  prive: true                   # toujours, dès qu'il contient de l'évaluation
  auteur: "Mohamed Amine EL AFRIT <elafrit.mohamed@gmail.com>"
  co_auteur: false              # jamais de ligne Co-Authored-By, jamais de mention d'une IA
~~~

---

## 4. Le prompt paramétrable

Collez-le juste après le bloc de paramètres rempli. Les passages `[[SI x]] … [[FIN]]` ne
s'appliquent que si le paramètre `x` est actif ; `{{x}}` désigne la valeur d'un paramètre.

~~~text
# MISSION

Tu es à la fois l'ingénieur pédagogique et le développeur de ce cours. À partir des
documents de sources/ et des PARAMÈTRES ci-dessus, construis avec le template de cours le
site web statique complet du cours « {{cours.titre}} » ({{cours.code_module}},
{{cours.bloc}}), destiné à {{cours.public}}, et ce qu'y ajoutent ses MODULES actifs.

Objectif pédagogique unique : que chaque étudiant réussisse l'évaluation du cours en
produisant, pendant le cours, les livrables mêmes que cette évaluation juge.

# RÈGLES DE CONDUITE, NON NÉGOCIABLES

Toutes les exigences de CLAUDE.md, § 2, s'appliquent : dialogue, Git, secrets, contenu,
pédagogie, audio, outils externes, publication, vérification, pièges de production,
journal. Celles qui reviennent à chaque étape :

1. Questions UNE À UNE, avec l'outil de question à options cliquables (jamais une liste
   dans le texte), ta recommandation en premier ; chaque étape finit par une question
   cliquable sur la suite. Tout en français : messages, documents, commits.
2. Un paramètre rempli s'applique tel quel ; vide, il se déduit des sources ; sinon tu le
   demandes.
3. Sources : lis TOUS les documents de sources/ avant d'écrire du contenu ; n'invente
   aucune règle d'examen, compétence, critère, seuil, fait ou chiffre ; cite tes sources ;
   signale les lacunes ; ne reproduis jamais le texte ni les figures d'un ouvrage.
4. Jalons : arrête-toi à chaque « STOP ». Toute série (pages, capsules, QR codes,
   traductions) commence par un exemple ou un témoin, validé par l'auteur.
5. Git : dépôt {{git.depot}}, privé ; commits au SEUL nom de {{git.auteur}} (git config
   vérifié avant chaque commit), SANS ligne « Co-Authored-By » ni mention d'une IA ; git
   add par chemins explicites. DEMANDE avant de commiter et pousser, puis, séparément,
   avant de mettre en ligne.
6. Secrets (section 2.3) : jamais ouverts, affichés ni demandés ; le .rgignore les cache
   aux recherches ; tu ne t'authentifies jamais toi-même sur le site en ligne.
7. Ton : {{cours.ton}}. Aucune date fixe dans le contenu (« Jour 1 », « séance 2 »).
   Vocabulaire stable : chapitre (unité de contenu), séance (demi-journée réelle),
   livrable, version de travail, version finale ; un QCM noté est un livrable.
8. Rien ne souffle une réponse : exemples de méthode sur un cas NEUTRE ; interdits :
   {{interdits}}, dans outils/interdits.py dès le cadrage, contrôlés par
   outils/verifier_interdits.py. [[SI modules.tp.actif]] Rien du sujet du TP
   ({{modules.tp.sujet}}) ni de ses chiffres hors du TP. [[FIN]]
9. Toute question à choix explique pourquoi la bonne réponse est juste ET pourquoi
   chacune des autres ne l'est pas, avec deux à quatre renvois « Pour approfondir »
   (prompts/15_explications_quiz.md). Tout schéma a sa lecture élément par élément, pour
   un débutant.
10. Journal à chaque étape : docs/02-Etat-d-avancement.md ; chaque choix structurant en
    décision Dnn (question, retenu, pourquoi) dans docs/01-Decisions-de-conception.md ;
    ce que l'auteur garde pour plus tard dans TODO.md.
11. Ni tirets cadratins ni marques de texte généré, en français comme en anglais, titres
    compris (CLAUDE.md, § 2, « Le contenu ») : outils/verifier_tirets.py sans écart.
12. Avant chaque chaîne de production, relis les pièges déjà rencontrés et leur parade
    (section 6 de ce document). Un piège nouveau s'y ajoute, dans le tronc du gabarit, sur
    accord de l'auteur.

# ÉTAPE ZÉRO : PARTIR DU TEMPLATE

1. Écris cours.json d'après les paramètres : les langues (la racine d'abord, puis les
   jumelles à venir, par exemple ["fr", "en"]), les filières (avec leur bloc, leur module
   et la page de leurs épreuves) et le bloc école (l'adresse de Livrables, le bouton du
   QCM, une session par promotion avec sa promotion et sa matière exactes et ses dates
   réelles). Lance python3 nouveau_cours.py --essai, montre le résultat, puis crée le
   cours (dossier à part, jamais dans le template). Vérifie dans la sortie : secrets
   recopiés et ignorés par Git, .rgignore présent, destination.json au nom de
   {{cours.slug}}, CLAUDE.md présent, menu des sections régénéré, bloc école écrit
   (boutons de l'accueil, épreuves des filières, sessions ; le script signale une session
   restée sur l'exemple). Initialise le dépôt Git ; crée docs/00-Lisez-moi.md,
   docs/01-Decisions-de-conception.md, docs/02-Etat-d-avancement.md et TODO.md.
2. Le moteur du template couvre : navigation et menu des sections généré, site miroir à
   plusieurs langues (bouton des langues qui garde la position de lecture, jumelles,
   liens, hreflang, parité, voir docs/I18N.md) et blocs data-tr en secours, bascule de
   filière, accueil (pastille, boutons, programme et échéances tirés de outils/seances.py),
   composants RDCX (checkpoint expliqué, reveal, spotError, match, branch, hotspots, voice,
   steps), glossaire à info-bulles, flashcards, QCM CBM avec correction et tableau de
   bord, QCM papier, playlist, audio Eleven v4, cahier de texte et classeur Livrables,
   déploiement SFTP avec garde-fou et zones protégées.
3. Le reste se reprend des cours de référence ({{ecosysteme.cours_de_reference}}), sans
   le réécrire (chaque module dit quoi), en l'adaptant à site/ et aux libellés T() ;
   chaque reprise est une décision Dnn. Un cours de référence se lit et ne se modifie
   jamais : lis ses modules Python sans les importer (pas même un __pycache__ chez lui) ;
   ses secrets valent ceux de ce cours.

# DÉCISIONS DÉJÀ PRISES, À APPLIQUER SANS LES REDEMANDER

L'auteur les a tranchées sur ses cours précédents. Elles valent pour tout cours créé avec
ce template, sauf avis contraire de sa part dans les PARAMÈTRES.

- Les langues : un site miroir, la langue racine d'abord, chaque jumelle écrite une fois la
  racine stable, sous en/ ou ar/ (25 octobre et 21 novembre 2026). L'arabe s'écrit de
  droite à gauche, avec le lexique docs/LEXIQUE-ar.md, et ne peut pas encore être la
  racine.
- Les filières : deux (EADL et ERIS, CDWFS et ASRC) ou une seule, avec la bascule du cours
  EADL ; sans filière choisie, chaque version s'affiche, étiquetée (21 novembre 2026).
- L'accueil : celui du gabarit, avec son bandeau toujours sombre, sa pastille, ses boutons,
  ses quatre cartes et ses sections numérotées. Une filière qui prépare l'épreuve d'un bloc
  y reçoit « EADL, Bloc 1, module FM04 » et un bouton vers la page de ses épreuves
  (22 novembre 2026).
- Les capsules : une au début de chaque section, de l'accueil comme des chapitres, en plus
  des capsules d'accueil et d'ouverture ; une par filière quand la section diffère ; une
  piste par langue (21 novembre 2026).
- Le programme : outils/seances.py, sans aucune date, est la source du programme et des
  échéances de l'accueil, du cahier de texte et du classeur Livrables. Les dates réelles ne
  vivent que dans outils/sessions.py, une session par promotion (22 novembre 2026).
- Le cahier de texte sort avec et sans les identifiants du site ; celui qui les porte ne
  quitte jamais le poste (22 novembre 2026).
- Les versions de travail sont obligatoires et non notées. Dans l'application, on ne leur
  saisit aucune note, et on ne coche jamais « Livrable bonus, facultatif » (22 novembre
  2026).
- Un QCM passé sur le site se dépose dans l'application en « Exercice / TP », rendu par son
  fichier CSV signé ; sa note vient du tableau de bord du QCM (22 novembre 2026).
- Chaque promotion a son classeur d'import Livrables : deux matières nouvelles dans un même
  classeur se prennent pour des doublons (constaté le 27 septembre 2026).
- Les illustrations : Codex, que Claude Code lance lui-même (codex --version, puis codex
  exec) dans un dossier dédié, sans commit côté Codex, avant de convertir et de contrôler
  les images ; sans Codex, Claude donne la procédure d'installation, vérifiée en ligne, et
  s'arrête (21 novembre 2026).

# CONTEXTE PÉDAGOGIQUE

- Public : {{cours.public}}.
- Filières : {{filieres}}, avec les compétences, l'épreuve, le bloc, le module, la
  palette, la fiche module et la grille de chacune.
[[SI groupe_mixte]]
- Groupe mixte : un seul site, bascule de filière en tête de page (choix mémorisé ;
  ?filiere= dans l'adresse ouvre une page dans la bonne filière), zones propres à une
  filière marquées ; sans filière choisie (vue formateur), toutes les versions
  s'affichent, étiquetées. Tronc commun identique ; seuls changent l'objet étudié, les
  exemples, les capsules et la grille. [[FIN]]
- Formats : {{cours.formats}} ; format imposé : {{cours.format_impose}}. Une séance = une
  demi-journée ({{cours.horaires}}) ; un chapitre = une unité de contenu.
- Évaluation : lis-la dans le règlement, la grille et les fiches du fil rouge ; le cours
  entraîne la MÉTHODE de l'épreuve sur le cas du cours, et prévient que le corpus de
  l'épreuve sera nouveau.

# CONCEVOIR LE COURS (Phase 1, avant tout contenu)

À partir des sources, propose puis fais valider (STOP) :
1. Une note d'analyse : ce qu'impose chaque document ; compétences et critères par
   filière ; seuils ; lacunes et contradictions des sources.
2. Le découpage en chapitres (un chapitre = une question à laquelle l'étudiant répond en
   produisant une partie de livrable) et leur répartition en séances pour chaque format.
3. La progression des livrables {{livrables}} : versions de travail et finales,
   échéances, notation, coefficients.
4. Le fil rouge {{fil_rouge.nom}} : un cas chiffré dans {{fil_rouge.referentiel}}, avec
   des résultats de référence calculés par le référentiel. [[SI modules.tp.actif]] Le TP
   porte sur un autre objet ({{modules.tp.sujet}}) : le cours enseigne la méthode, jamais
   ses réponses. [[FIN]]
5. Les modules retenus : ce que chacun ajoute (pages, entrées de menu, générateurs) et sa
   place dans les phases.

# ARCHITECTURE ET CONVENTIONS (celles du template)

- Site statique sans framework ni build, dans site/ : index.html, cours.html,
  chapitres/NN-*.html, glossaire.html, activites.html, atelier.html, QCM/… Seul site/ se
  publie.
- Le bilingue (docs/I18N.md) : par défaut, des pages en français, puis leur jumelle
  anglaise sous en/ une fois le français stable (module 01) ; en secours, des blocs
  data-tr, le contenu des composants dans TEXTES = { fr, en } et monter() rejoué sur
  tpl:langchange. Dans les deux cas, les libellés des moteurs vivent dans ui-labels.js
  (T()), jamais en dur.
- Copier depuis site/chapitres/_modele.html, le seul endroit où tous les composants sont
  appelés pour de vrai.
- Chaque chapitre : capsule d'ouverture, sections numérotées (h2 id), composants RDCX là
  où une notion se joue, point de contrôle expliqué en fin de section, schéma expliqué
  élément par élément, « à retenir », flashcards.
- Menu, dans le même ordre pour chaque langue : « Accueil du cours » en tête ; ensuite les
  chapitres, puis les ressources de `course-data.js`
  [[SI modules.polycopie.actif]], « 📘 Polycopié » en tête des ressources [[FIN]]
  [[SI modules.podcasts.actif]], « 🎙️ Podcasts » parmi elles [[FIN]] ;
  « 🏋️ QCM d'entraînement » [[SI modules.evaluations.correction_publique]],
  suivi aussitôt de « ✅ Correction des QCM » (page publique : chaque question, sa
  réponse, ses explications ; jamais la correction protégée du TP) [[FIN]].
- Accessibilité : clavier, aria, .sr-only, contrastes vérifiés dans les deux thèmes,
  lisible à 375 px, transcription sous chaque capsule, texte alternatif sur chaque image.
- Les fichiers générés (playlist-data.js, nav-sections.js, transcriptions, fragments) ne
  s'éditent jamais à la main ; les générateurs se lancent dans l'ordre (CLAUDE.md, § 4).

# LES MODULES

Pour chaque module actif de {{modules}}, lis son fichier dans prompts/modules/ AVANT sa
phase, et applique-le : décisions à faire valider (une question à la fois), méthode,
pièges, contrôles, STOP. Un module inactif ne laisse aucune trace : ni page, ni entrée de
menu, ni générateur.

# MÉTHODE : PHASES ET JALONS

Phase 0   Paramètres : ce qui est fourni, déduit, encore ouvert ; questions une à une. STOP.
Phase 1   Conception (section « Concevoir le cours »). STOP.
Phase 2   Étape zéro, référentiel du cas et table de vérité des résultats de référence
          (docs/02). STOP.
Phase 3   Squelette, navigation, bascules éventuelles, glossaire.
Phase 4   Contenus en français, un chapitre à la fois (prompts/03_chapitre.md, relu avec
          prompts/04_relecture_pedagogique.md). STOP après le premier chapitre (ton,
          densité, explications des quiz), puis à la fin.
Phase 5   TP et sa correction protégée ................................... module 06
Phase 6   Évaluations, toutes expliquées. STOP ............................. module 05
Phase 7   Compléments : schémas, simulateurs, glossaire, Boîte à outils .... module 09
Phase 8   Audio : fiches, témoin, STOP, série .............................. module 04
Phase 9   Version anglaise, une fois le français stable .................... module 01
Phase 10  Polycopié : témoin, STOP, livret français, puis anglais .......... module 02
Phase 11  Podcasts et diaporamas, puis leurs QR codes dans le livret ....... module 03
Phase 12  Yparéo et import Livrables. STOP ................................. module 07
Phase 13  Déploiement : essai à blanc, accord, envoi, contrôle en ligne .... module 08
Phase 14  Documentation de reprise : README, docs/00 à 04, DEMARRER-ICI.md retiré.

Une phase dont le module est inactif se saute. L'ordre est celui qui a fonctionné sur le
cours de référence : l'anglais traduit un français stable ; le livret reprend les pages des
deux langues ; NotebookLM tire les podcasts du livret, dont les QR codes annoncent ensuite
les épisodes. Une mise en ligne suit chaque étape publiable, toujours sur accord
(module 08).

# CONTRÔLES AVANT CHAQUE MISE EN LIGNE

Référentiel cohérent, generer_fragments.py --essai sans écart · verifier_i18n,
verifier_contraste, verifier_liens (renvois compris)
sans écart · generer_nav_sections.py --essai : menu à jour · node --check · aucun octet
NUL · captures clair/sombre, chaque filière, 1280 et 375 px, console vide ·
verifier_interdits.py et verifier_tirets.py sans écart · contrôles propres à chaque module actif · deployer.py
--essai : destination attendue, garde-fou passé, aucun fichier hors de site/.

# DÉFINITION DE « TERMINÉ »

- Un étudiant de chaque filière suit tous les chapitres, produit ses livrables et
  s'entraîne à l'évaluation sans lien cassé, sans chiffre incohérent, sans réponse
  soufflée, et chaque erreur de quiz lui explique pourquoi, et où relire.
- Chaque sortie du tableau 2.5 remplit son critère d'acceptation.
- Chaque module actif a rempli sa propre définition de « terminé ».
- Le formateur dispose de ses corrigés, évaluations, cahiers de texte et classeurs
  d'import, et sait ce qu'il doit régler à la main dans l'application.
- Le site en ligne est identique au dépôt, au bon endroit, protégé là où il doit l'être,
  et tout se régénère avec la documentation seule.
~~~

---

## 5. Adapter le prompt à la matière

| Type de cours | Ce qui change surtout | Conseils |
|---|---|---|
| **Gestion de projet, pilotage, budget** | Livrables documentaires sur modèles (charte, WBS, planning, budget) | Simulateurs de calcul (charge, planning, valeur acquise) ; les mêmes personnes du cas d'un cours à l'autre |
| **Architecture, conception** | Schémas, décisions, dossier d'architecture | Schémas expliqués élément par élément, une capsule par schéma ; Boîte à outils de fiches ; TP sur un autre objet que l'exemple du cours |
| **Développement** (front, back, API, tests) | Livrables en code (dépôt Git), revues de code | Exercices « repérer l'erreur » sur du code ; grilles adossées aux critères de l'épreuve |
| **Infrastructure, cloud, sécurité** | Schémas d'architecture, procédures, rapports d'audit | Simulateurs de disponibilité, de coûts, de capacité |
| **Communication, veille, soutenance** | Rapports, présentations, oral | Capsules plus nombreuses ; grilles d'oral ; exercices à embranchements ; podcasts |

Dans tous les cas : un **cas fil rouge** chiffré dans un référentiel unique, des
**livrables progressifs** (version de travail puis finale), une **évaluation au format de
l'épreuve**, des **quiz qui expliquent chaque proposition**, et des exemples de méthode
sur un **cas neutre** quand ils toucheraient à une réponse.

---

## 6. Pièges déjà rencontrés, et leur parade

Relevés dans les cours de l'auteur et dans le journal du gabarit (`JOURNAL.md`, « Pièges appris »). Claude les relit
avant chaque chaîne de production. Un piège nouveau s'ajoute ici avec sa parade, dans le gabarit, pour que le cours
suivant en profite.

**Le poste et les correctifs**

| Symptôme | Cause | Parade |
|---|---|---|
| Des fichiers corrompus par des octets NUL | Un correctif passé par un heredoc de Git Bash, avec des antislashs | Écrire le correctif dans un fichier `.py`, puis vérifier qu'aucun octet NUL n'entre dans le fichier modifié |
| Un correctif annoncé réussi qui n'a rien changé | Son texte d'ancrage avait changé, parfois d'une espace insécable invisible | Exiger que chaque passage tombe exactement une fois, sinon n'écrire aucun fichier |
| Des fins de ligne mélangées après une retouche | Le dépôt est en CRLF sous Windows (`core.autocrlf`) | Réécrire chaque fichier avec ses fins de ligne d'origine ; comparer avec `diff --strip-trailing-cr` |
| Une espace insécable redevenue ordinaire | Un éditeur ou un copier-coller l'a remplacée sans que rien ne se voie | Dans le code, l'écrire par son échappement (`" "`), jamais en caractère |
| Une page générée qui contredit sa source | Un générateur lancé avant celui dont il lit la sortie | Suivre l'ordre des générateurs (`CLAUDE.md`, § 4), puis leur `--essai` |
| Le travail dans une copie du dépôt, les secrets dans une autre | Deux copies de travail du même dépôt | Une seule copie de travail par cours |
| Un envoi FTPS refusé (« 500 This security scheme is not implemented ») | L'hébergement mutualisé d'OVH | SFTP, par `paramiko` : c'est ce que fait le déployeur du gabarit |

**Les secrets**

| Symptôme | Cause | Parade |
|---|---|---|
| Un secret affiché dans la sortie d'un outil | Un masquage qui ne connaissait que les guillemets droits | Vérifier un secret sans l'afficher du tout, par sa longueur ou par le commit qui l'a introduit |
| Un secret trouvé par une recherche | Un filtre de fichiers explicite (`*.json`) passe outre le `.rgignore` | Exclure les secrets nommément, ou ne pas chercher |
| Erreur 401 d'ElevenLabs | Une clé révoquée ou mal copiée | Une nouvelle clé, déposée dans `outils/elevenlabs.json`, jamais dans la conversation |

**L'audio**

| Symptôme | Cause | Parade |
|---|---|---|
| Une capsule étirée à 67 mots par minute mise en ligne (cours ERIS) | Aucun contrôle de la piste | Contrôler le débit, la durée et les silences, et mettre en quarantaine une piste hors tolérance |
| Une capsule commune générée deux fois | Deux emplacements pour un seul fichier | Dédoublonner par nom de fichier |
| Les pistes des deux filières mélangées dans la liste de lecture | Une liste non filtrée | Filtrer par le suffixe du nom de fichier |

**Le navigateur**

| Symptôme | Cause | Parade |
|---|---|---|
| Des captures blanches, un bouton qui ne se cache pas, une position de lecture perdue | Le volet du navigateur intégré est masqué, et l'observateur d'intersection comme le défilement doux n'y avancent qu'aux captures | Prendre une capture avant de mesurer, sauter sans défilement doux (`behavior: 'instant'`), ou passer par un navigateur sans interface (Edge ou Chrome, `--headless`) |
| Une erreur de console qui n'existe plus | La console d'un onglet garde les messages de ses visites précédentes | Revérifier dans un onglet neuf avant d'y croire |
| Un choix de filière qui passe d'un cours à l'autre | Le stockage local est partagé par tous les cours d'un même site | Une clé qui porte l'adresse de la racine du cours |

**L'application Livrables**

| Symptôme | Cause | Parade |
|---|---|---|
| Une matière sans séances ni livrables après l'import (cours ASRC) | Deux matières nouvelles dans un même classeur, que l'application prend pour des doublons | Un classeur par promotion |
| Un livrable de plus après un réimport | Le titre d'un livrable sert de clé, et l'import ne supprime rien | Ne jamais renommer un livrable importé ; sinon, retirer l'ancien à la main |
| Une version de travail obligatoire comptée comme non due | La case « Livrable bonus, facultatif » cochée | Ne pas la cocher, et ne lui saisir aucune note |
| L'étudiant ne peut rendre qu'un lien | « Autoriser les fichiers joints » n'est pas cochée, et l'import ne porte pas cette case | La cocher à la main sur chaque livrable qui attend un fichier |

**Le contenu**

| Symptôme | Cause | Parade |
|---|---|---|
| « 3 livrables » sur l'accueil au lieu de quatre (cours EADL) | Le QCM oublié dans un compte fait à la main | Compter le QCM parmi les livrables ; chaque chiffre du cours vient du référentiel ou de `outils/seances.py`, écrit par un fragment |
| Une courbe illisible sur téléphone | Un SVG réduit, aux textes minuscules | Une `viewBox` adaptée et des textes grossis par media query |
| Deux personnages illustrés qui se ressemblent | Une référence d'image trop proche, la même tenue | Une bible des personnages distinctive, jamais de référence ressemblante |
| Une adresse d'exemple qui mène chez quelqu'un | Un domaine inventé pour l'exemple | `example.org`, `example.com` ou `example.net`, rien d'autre |

**L'arabe**

| Symptôme | Cause | Parade |
|---|---|---|
| Des lettres arabes détachées les unes des autres | Les capitales espacées des titres et des étiquettes (`letter-spacing`) | Revenir à un espacement normal sur une page arabe |
| Des flèches à l'envers dans les libellés arabes | Le navigateur retourne les chevrons ‹ ›, qui sont des caractères miroirs, mais pas les flèches → ← | Inverser les flèches à la main dans les libellés arabes |
| Un code mal espacé sur une page arabe | Une police à chasse fixe sans glyphes arabes, remplacée par une police système | Une pile à chasse fixe qui passe par Noto Sans Arabic |

---

## 7. Annexe : un bloc rempli, pour un cours fictif

Un modèle de remplissage, à comparer au vôtre. Le cours, ses chemins et son dépôt sont
fictifs.

~~~yaml
cours:
  titre: "Sécurité des applications web"
  slug: "securite-applications-web"
  auteur: "<Prénom NOM>"
  code_module: "FM03"
  bloc: "Bloc 3 · Sécuriser une application"
  annee: "2026-2027"
  palette: "ardoise"
  langues: ["fr"]
  public: "développeurs en alternance, à l'aise avec HTTP et une API REST, sans formation sécurité ; deux jours en présentiel"
  formats: ["2j"]
  format_impose: "2j"
  calendrier: {jour_1: "<date réelle>", jour_2: "<date réelle>"}
  horaires: {matin: "09:00-12:30", apres_midi: "13:30-17:00"}
  ton: "vouvoiement chaleureux, registre d'un collègue expérimenté ; peu d'écrit, beaucoup de pratique"
filieres:
  - {id: dev, code: DEV, nom: "<intitulé du titre>", court: "<nom court>", rncp: "<RNCPxxxxx>", palette: "ardoise",
     competences: [], epreuve: "<ECxx>", bloc: "Bloc 3", module: "FM03",
     page_epreuves: "https://example.org/<épreuves du bloc 3>/",
     fiche_module: "sources/<fiche>.docx", grille: "sources/<grille>.docx",
     promotion_app: "2026-2027 › <Promotion>", matiere_app: "<matière exacte>"}
groupe_mixte: false
fil_rouge: {nom: "<le cas du cours>", source: "sources/fil-rouge/", projet_par_filiere: {}, referentiel: "outils/cas.py"}
interdits: ["<mots du sujet du TP>"]
livrables:
  - {id: "01", titre: "Analyse de risques", modele: "", format_depot: ".docx",
     version_de_travail: {existe: true, notee: false, obligatoire: true, jour: 1, heure: "17:00"},
     version_finale: {jour: 2, heure: "17:00", note_max: 20, coefficient: 2, grille: true}}
  - {id: "qcm", titre: "QCM de fin de module", modele: "", format_depot: "en ligne",
     version_de_travail: {existe: false},
     version_finale: {jour: 2, heure: "15:00", note_max: 20, coefficient: 1, grille: false}}
malus_version_de_travail: 2
modules:
  bilingue: {actif: false}
  polycopie: {actif: true}
  podcasts: {actif: true, episodes: 8, diaporamas: true}
  audio: {actif: true, capsules: ["accueil", "ouverture de chapitre", "TP pas à pas"]}
  evaluations:
    qcm_en_ligne: {actif: true, notation: "CBM", questions: 30}
    qcm_papier: {actif: false}
    qcm_entrainement: {actif: true, questions_par_filiere: 30}
    correction_publique: true
    points_de_controle: true
  tp: {actif: true, sujet: "<un autre objet que l'exemple du cours>"}
  ecole: {ypareo: true, livrables_app: true, bouton_qcm: true}
  deploiement:
    actif: true
    url: "https://example.org/teaching/securite-web/2026-2027/"
    repertoire_distant: "/www/teaching/securite-web/2026-2027"
    zones_protegees: ["correction/", "correction/formateur/"]
    site_protege: false
  complements:
    schemas: {actif: true, capsule_par_schema: true}
    illustrations: {actif: false}
    simulateurs: ["score de risque"]
    glossaire: true
    boite_a_outils: {actif: false}
    fiches_memo: true
ecosysteme:
  gabarit_technique: "C:/projets/Cours/template_cours"
  app_livrables: "https://livrables.elafrit.com/"
git:
  depot: "<compte>/<Cours_Securite_Web>"
  prive: true
  auteur: "Mohamed Amine EL AFRIT <elafrit.mohamed@gmail.com>"
  co_auteur: false
~~~
