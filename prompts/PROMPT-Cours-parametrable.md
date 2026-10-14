# Prompt paramétrable — créer un cours complet avec ce template

> **Ce que contient ce document.** Le prompt **réutilisable** pour produire, avec Claude
> Code, le site complet d'un cours — et tout ce qui l'accompagne : évaluations, supports
> formateur, audio, déploiement — à partir de ses propres documents de référence. Il
> réunit ce que les cours précédents de l'auteur ont appris : méthode, conventions,
> écosystème (Yparéo, application Livrables, ElevenLabs, Codex, OVH) et pièges.
>
> **Le principe.** Vous remplissez le **bloc de paramètres** (section 3) ; ce que vous
> laissez vide, Claude le déduit des documents de référence ou vous le demande, **une
> question à la fois**. Ce template est le **gabarit technique** : son moteur, ses outils
> et son déploiement sont repris par `nouveau_cours.py`, pas réécrits. Les cours de
> référence de l'auteur fournissent les moteurs plus avancés quand le cours en a besoin.
>
> **Le point d'entrée.** Dans Claude Code, demander « créer un cours » déclenche la skill
> `creer-cours-template`, qui suit ce document. Les exigences permanentes de l'auteur sont
> dans `CLAUDE.md` (§ 2), recopié dans chaque cours créé.

---

## 1. Mode d'emploi

1. **Remplissez le bloc de paramètres** (section 3). Laissez vide ce que vous ne savez pas
   encore : Claude le demandera.
2. **Demandez à Claude de créer le cours** depuis le template, en collant le bloc rempli
   puis le prompt de la section 4 dans le même message — ou simplement « crée un nouveau
   cours sur … avec le template », et répondez à ses questions.
3. Claude **amorce le cours** : il écrit `cours.json` d'après vos réponses, lance
   `python3 nouveau_cours.py --essai`, vous montre le résultat, puis crée le dossier. Le
   script recopie en local les **secrets communs** (section 2.3), écrit
   `deploiement/destination.json` et le `CLAUDE.md` du cours.
4. **Déposez vos documents de référence** dans `sources/` du nouveau cours (jamais
   versionnés). Claude les lit **tous** avant d'écrire la moindre ligne de contenu.
5. **Répondez aux questions** une à une, et **validez à chaque jalon** « STOP ».

---

## 2. Prérequis

### 2.1 Entrées — les documents de référence (`sources/`, lecture seule)

| Document | Indispensable | Ce que Claude en tire |
|---|---|---|
| **Fiche module** (une par titre RNCP concerné) | si le cours relève d'un titre | compétences, objectifs, plan, exercices, volume horaire, bibliographie |
| **Grille d'évaluation de l'épreuve** | si le cours prépare une épreuve | critères, indicateurs, seuils, niveaux : la cible de tout le cours |
| Règlement des examens · fiche récapitulative · matrice de couverture | si disponibles | modalités, coefficients, seuil de validation, articulation module ↔ épreuve |
| **Fil rouge** : fiches de l'épreuve (apprenant, rattrapage, correcteur) | si le module prépare une épreuve fil rouge | le cas, les attendus, la façon dont le correcteur note |
| Modèles, kits, gabarits à faire remplir | si le module a des livrables sur modèle | les livrables, à adapter au cas |
| Ouvrages, diapositives, articles, normes | non | notions et exemples — **jamais recopiés** : reformulés et cités |

### 2.2 Ressources à portée de main

| Ressource | Emplacement |
|---|---|
| Gabarit technique (moteur, outils, déploiement, ce document) | `{{ecosysteme.gabarit_technique}}` |
| Cours de référence (moteurs avancés, voir l'étape zéro) | `{{ecosysteme.cours_de_reference}}` |
| Format d'import de l'application Livrables | `{{ecosysteme.doc_import_app}}` |
| Épreuves réelles et cadrage des QCM | `{{ecosysteme.epreuves_reelles}}` |

### 2.3 Secrets — fichiers locaux, ignorés par Git, jamais lus

| Fichier | Contenu | D'où il vient |
|---|---|---|
| `outils/elevenlabs.json` | clé API ElevenLabs, identifiant de la voix clonée | recopié tel quel depuis le template par `nouveau_cours.py` |
| `deploiement/config.json` | accès SFTP à l'hébergement (hôte, identifiant, mot de passe, protocole) | recopié tel quel ; son éventuel répertoire distant n'est **jamais lu** |
| `docs/acces.json` | identifiant et mot de passe de consultation du site (pour Yparéo) | propre au cours, déposé par l'auteur |
| `docs/acces-zones.json` | comptes des zones protégées (correction du TP…) | propre au cours |

Le template garde **localement** la copie de référence des deux premiers (jamais sur
GitHub) ; chaque nouveau cours en reçoit une copie octet pour octet. Claude ne les ouvre
pas, ne les affiche pas, ne les demande pas : les scripts s'en servent.

### 2.4 Poste de travail et comptes

Windows 11 (Git Bash, PowerShell) · Python 3.11+ (`paramiko`, `bcrypt`, `python-docx`,
`fpdf2`, `openpyxl`, `Pillow`, `PyMuPDF`) · ffmpeg/ffprobe · Node.js · Microsoft Edge ou
Google Chrome (captures sans interface) · `git` et `gh` authentifiés. Comptes selon les
options retenues : ElevenLabs (**Eleven v4**, voix clonée), Codex ou ChatGPT (images), OVH
(SFTP), GitHub, application Livrables (promotions créées), Yparéo.

---

## 3. Paramètres

Recopiez ce bloc, remplissez-le, et collez-le **avant** le prompt. `""` = à déduire des
sources ou à demander. Une option désactivée (`actif: false`) retire la chaîne de
production correspondante.

~~~yaml
# ─────────────────────────────── LE COURS
cours:
  titre: ""                     # ex. « Conception d'architectures logicielles »
  slug: ""                      # identifiant court, sans accent : nom du dossier, destination.json, carnet distant
  code_module: ""               # ex. FM01
  bloc: ""                      # ex. « Bloc 2 — Concevoir une solution »
  annee: ""                     # ex. 2026-2027
  langues: ["fr"]               # ["fr", "en"] double la rédaction ET l'audio
  palette: ""                   # marine | emeraude | prune | ardoise | bordeaux
  public: ""                    # par ses prérequis et ses contraintes, pas par l'intitulé du diplôme
  formats: []                   # ex. ["2j", "3j"] ; un seul = pas de bascule
  format_impose: ""
  calendrier: {}                # dates réelles : SEULEMENT pour Yparéo et l'application
  horaires: {matin: "09:00-12:30", apres_midi: "13:30-17:00"}
  ton: "vouvoiement chaleureux, registre d'un collègue expérimenté ; peu d'écrit, beaucoup de pratique"

# ─────────────────────────────── LES FILIÈRES (une seule = pas de bascule)
filieres:
  - id: ""                      # ex. "eadl"
    libelle: ""
    titre: ""                   # intitulé du titre RNCP
    rncp: ""
    competences: []             # sinon lues dans la grille
    epreuve: ""                 # ex. EC01
    couleur: ""
    fiche_module: ""            # chemin dans sources/
    grille: ""                  # chemin dans sources/
    promotion_app: ""           # EXACTEMENT « Année › Promotion » de l'application
    matiere_app: ""             # nom exact de la matière dans l'application
groupe_mixte: false             # un seul cours pour plusieurs filières

# ─────────────────────────────── LE FIL ROUGE ET LE TP
fil_rouge:
  nom: ""                       # le cas qui traverse tout le cours
  source: "sources/…"
  projet_par_filiere: {}
  referentiel: ""               # ex. outils/<cas>.py — source unique des chiffres du cas
tp:
  actif: false
  sujet: ""                     # distinct de l'exemple du cours : le cours n'en souffle rien
  correction_protegee: true     # correction/ et correction/formateur/ derrière un mot de passe
interdits: []                   # mots et exemples à ne jamais employer hors du TP (son sujet, ses chiffres…)

# ─────────────────────────────── LES LIVRABLES (dans l'ordre du cours)
livrables:
  - id: ""
    titre: ""
    modele: ""                  # chemin du modèle dans sources/, ou "" s'il est à créer
    format_depot: ""
    version_de_travail: {existe: true, notee: false, obligatoire: false, jour: 1, heure: "12:30"}
    version_finale: {jour: 2, heure: "12:30", note_max: 20, coefficient: 1, grille: true}
malus_version_de_travail: 0

# ─────────────────────────────── L'ÉVALUATION
evaluation:
  qcm_en_ligne: {actif: true, notation: "CBM", questions: 0}
  qcm_papier: {actif: false, questions: 0, propositions: 4, certitude: "", un_par_filiere: false}
  qcm_entrainement: {actif: true, questions_par_filiere: 0}
  points_de_controle: true      # un par section importante
  # Toujours : chaque proposition expliquée, deux à quatre renvois « Pour approfondir »
  # (prompts/15_explications_quiz.md). Ce n'est pas une option.

# ─────────────────────────────── LES MÉDIAS ET COMPLÉMENTS
medias:
  audio:
    actif: true
    modele: "eleven_v4"         # imposé par outils/generer_audio.py
    voix: "clone de l'auteur (outils/elevenlabs.json)"
    accent: "strong Parisian French accent"   # ajouté par le générateur aux pistes françaises
    ton: "pédagogique, académique, professionnel, motivant ; au vouvoiement"
    lecture: "posée — « speaking slowly » dans les balises des capsules explicatives"
    capsules: []                # ex. ["accueil", "ouverture de chapitre", "un par schéma", "TP pas à pas", "ce qui est attendu"]
    temoin_avant_serie: true
  illustrations:
    actif: false
    outil: "Codex"              # AUCUN texte dans l'image
    scenes: []
  schemas:
    actif: true
    explication_element_par_element: true    # toujours
    capsule_par_schema: false
  simulateurs: []
  glossaire: true
  boite_a_outils: {actif: false, fiches: 0}  # fiches d'une page + mini-quiz expliqués (cours de référence)
  encarts_plus_loin: []

# ─────────────────────────────── L'ÉCOSYSTÈME
ecosysteme:
  gabarit_technique: "C:/projets/template_cours"
  cours_de_reference:
    - "C:/projets/Cours/Cours_Architecture_Logicielle"        # Boîte à outils, quiz expliqués, schémas et leurs capsules, correction protégée, audio v4
    - "C:/projets/Cours/Cours_EADL_ERIS_Etude_Avant_Projet"   # correction de TP, générateurs de glossaire et de flashcards, import Livrables, Yparéo, audio v4
    - "C:/projets/Cours/Cours_CDWFS_ASRC_Etude_Avant_Projet"  # groupe mixte et bascule de filière, QCM papier à certitude, fiches mémo
  app_livrables: "https://livrables.elafrit.com/"
  doc_import_app: "C:/projets/Livrables_App_Etudiants/docs/PROMPT-CLASSEUR-IA.md"
  ypareo: true
  page_epreuves: ""
  epreuves_reelles: ""

# ─────────────────────────────── LA PUBLICATION ET GIT
publication:
  url: ""                       # adresse publique du cours
  repertoire_distant: ""        # dossier PROPRE à ce cours → deploiement/destination.json
  zones_protegees: []           # ex. ["correction/", "correction/formateur/"]
  protection: "existante côté serveur (.htaccess / .htpasswd) — jamais écrasée"
git:
  depot: ""                     # ex. melafrit/<Cours>
  prive: true
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
{{cours.bloc}}), destiné à {{cours.public}}, et tout ce qui l'accompagne : évaluations,
supports formateur, cahiers de texte Yparéo, classeurs d'import de l'application
Livrables, déploiement, documentation de reprise — plus les médias activés dans {{medias}}.

Objectif pédagogique unique : que chaque étudiant réussisse l'évaluation du cours en
produisant, pendant le cours, les livrables mêmes que cette évaluation juge.

# RÈGLES DE CONDUITE — NON NÉGOCIABLES (détail : CLAUDE.md, § 2)

1. Langue : tout en français — messages, points d'étape, documents, commits.
2. Paramètres : un paramètre rempli s'applique tel quel ; un paramètre vide se déduit des
   sources ; sinon tu le demandes. Questions UNE À UNE, avec l'outil de question à options
   cliquables (jamais une liste de questions dans le texte), deux à quatre options, ta
   recommandation en premier. Chaque étape se termine par une question cliquable sur la
   suite.
3. Sources : lis TOUS les documents de sources/ avant d'écrire du contenu ; sources/ est en
   lecture seule ; n'invente aucune règle d'examen, compétence, critère, seuil, fait ou
   chiffre ; cite tes sources ; signale les lacunes. Ne reproduis jamais le texte ni les
   figures d'un ouvrage : reformule et cite.
4. Jalons : arrête-toi à chaque « STOP » et attends la validation de l'auteur.
5. Git : dépôt {{git.depot}}, privé ; commits au SEUL nom de {{git.auteur}}, SANS ligne
   « Co-Authored-By » ni mention d'une IA ; git add par chemins explicites ; un commit par
   étape cohérente, en français. DEMANDE avant de commiter et pousser, puis, séparément,
   avant de mettre en ligne.
6. Secrets : outils/elevenlabs.json, deploiement/config.json, docs/acces.json,
   docs/acces-zones.json restent locaux et ignorés par Git ; ne les ouvre jamais, ne les
   affiche jamais, ne les demande jamais ; une recherche dans le dépôt les exclut. Ne
   t'authentifie jamais toi-même sur le site en ligne.
7. Ton : {{cours.ton}}.
8. Aucune date fixe dans le contenu : « Jour 1 », « séance 2 »… Les dates de
   {{cours.calendrier}} ne servent qu'à Yparéo et à l'import Livrables.
9. Vocabulaire stable : « chapitre » (unité de contenu), « séance » (demi-journée réelle),
   « livrable », « version de travail », « version finale ». Un QCM noté est un livrable.
10. Rien ne souffle une réponse : exemples de méthode sur un cas NEUTRE ; [[SI tp.actif]]
    rien du sujet du TP ({{tp.sujet}}) ni de ses chiffres hors du TP ; ses réponses ne
    vivent que dans sa correction, en zone protégée ; [[FIN]] interdits : {{interdits}}.
11. Toute question à choix explique pourquoi la bonne réponse est juste ET pourquoi
    chacune des autres ne l'est pas, avec deux à quatre renvois « Pour approfondir » vers
    l'endroit exact du cours ou une référence externe vérifiée
    (prompts/15_explications_quiz.md).
12. Tout schéma a son explication élément par élément, pour un débutant.
13. Liens externes : target="_blank" rel="noopener noreferrer", signalés aux lecteurs
    d'écran ; chaque adresse ouverte et vérifiée avant d'être ajoutée.
14. Typographie française : espaces insécables avant : ; ? ! et dans « ».
15. Poste Windows : correctifs scriptés dans des fichiers .py (pas d'heredoc à
    antislashs) ; console en UTF-8 ; inventaires en Python ; aucun octet NUL.
16. Vérifie ce que tu livres : node --check, exécution des générateurs,
    outils/verifier_i18n.py, outils/verifier_contraste.py, outils/verifier_liens.py,
    captures au navigateur (clair, sombre, chaque filière, 1280 et 375 px, console vide ;
    navigateur sans interface si l'onglet intégré n'affiche rien).
17. Journal : docs/02-Etat-d-avancement.md à jour à chaque étape ; chaque choix structurant
    en décision Dnn (question, retenu, pourquoi) dans docs/01-Decisions-de-conception.md.
18. Travail en parallèle : un sous-agent reçoit une consigne écrite complète (dans
    docs/prompts/) et son travail ne s'accepte qu'après un contrôle automatique.

# ÉTAPE ZÉRO — PARTIR DU TEMPLATE

1. Écris cours.json d'après les paramètres (slug, titres, auteur, palette, langues,
   chapitres provisoires, blocs, publication), lance python3 nouveau_cours.py --essai,
   montre le résultat, puis crée le cours (dossier à part, jamais dans le template).
   Vérifie dans la sortie : secrets recopiés et ignorés par Git, destination.json écrit au
   nom de {{cours.slug}}, CLAUDE.md présent. Initialise le dépôt Git, crée
   docs/00-Lisez-moi.md, docs/01-Decisions-de-conception.md, docs/02-Etat-d-avancement.md.
2. Le moteur du template couvre : navigation et sections, bilingue, composants RDCX
   (checkpoint expliqué, reveal, spotError, match, branch, hotspots, voice, steps),
   glossaire à info-bulles, flashcards, QCM CBM avec correction et tableau de bord,
   polycopiés, QCM papier, playlist, audio Eleven v4, déploiement SFTP avec garde-fou et
   zones protégées.
3. Ce qu'il ne couvre pas se reprend des cours de référence ({{ecosysteme.cours_de_reference}})
   sans le réécrire, en l'adaptant à site/ et aux libellés T() : bascule de filière et de
   format, référentiel du cas et fragments générés, simulateurs, Boîte à outils (fiches,
   mini-quiz expliqués, annexe Word/PDF), correction de TP protégée et ses capsules,
   cahiers de texte Yparéo, import Livrables, QCM papier à certitude (Leclercq),
   vérificateur de liens par ancres de glossaire. Chaque reprise est une décision Dnn.

# CONTEXTE PÉDAGOGIQUE

- Public : {{cours.public}}.
- Filières : {{filieres}} — compétences, épreuve, couleur, fiche module et grille de
  chacune.
[[SI groupe_mixte]]
- Groupe mixte : un seul site, bascule de filière en tête de page (choix mémorisé), zones
  propres à une filière marquées ; sans filière choisie (vue formateur), toutes les
  versions s'affichent, étiquetées. Tronc commun identique ; seuls changent l'objet
  étudié, les exemples, les capsules et la grille. [[FIN]]
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
   des résultats de référence calculés par le référentiel. [[SI tp.actif]] Le TP porte
   sur un autre objet ({{tp.sujet}}) : le cours enseigne la méthode, jamais ses
   réponses. [[FIN]]
5. La liste des médias et compléments retenus, et leurs emplacements.

# ARCHITECTURE ET CONVENTIONS (celles du template)

- Site statique sans framework ni build, dans site/ : index.html, cours.html,
  chapitres/NN-*.html, glossaire.html, activites.html, atelier.html, QCM/… Seul site/ se
  publie.
- Contenu rédigé en blocs data-tr ; contenu des composants dans TEXTES = { fr, en } et
  monter() rejoué sur tpl:langchange ; libellés des moteurs dans ui-labels.js (T()) —
  jamais en dur.
- Copier depuis site/chapitres/_modele.html, le seul endroit où tous les composants sont
  appelés pour de vrai.
- Chaque chapitre : capsule d'ouverture, sections numérotées (h2 id), composants RDCX là où
  une notion se joue, point de contrôle expliqué en fin de section, schéma expliqué élément
  par élément, « à retenir », flashcards.
- Accessibilité : clavier, aria, .sr-only, contrastes vérifiés dans les deux thèmes,
  lisible à 375 px, transcription sous chaque capsule, texte alternatif sur chaque image.
- Les fichiers générés (playlist-data.js, nav-sections.js, transcriptions) ne s'éditent
  jamais à la main.

# CHAÎNES DE PRODUCTION

Référentiel : {{fil_rouge.referentiel}} porte TOUS les chiffres du cas et un verifier() ;
un chiffre ne s'écrit jamais à la main dans une page.

Contenu : un chapitre à la fois (prompts/03_chapitre.md), relu (04), puis glossaire (06,
06b), activités (05), atelier (11). Chaque question à choix reçoit son explication
complète (15).

[[SI evaluation.qcm_en_ligne.actif]]
QCM en ligne (prompts/07) : notation CBM, réponse unique, positions équilibrées,
distracteurs débiaisés, explications complètes. [[FIN]]
[[SI evaluation.qcm_papier.actif]]
QCM papier (prompts/08) : {{evaluation.qcm_papier}} ; mélange déterministe, audit des
biais ; livret, corrigé commenté, grille. STOP : relecture des livrets. [[FIN]]
[[SI evaluation.qcm_entrainement.actif]]
QCM d'entraînement : {{evaluation.qcm_entrainement.questions_par_filiere}} questions par
filière, DIFFÉRENTES du QCM noté, même barème, chaque proposition expliquée. [[FIN]]

[[SI medias.audio.actif]]
Audio (prompts/14_capsules_audio.md) : Eleven v4, voix clonée de l'auteur, accent
« {{medias.audio.accent}} » ajouté par le générateur aux pistes françaises, ton
{{medias.audio.ton}}, lecture {{medias.audio.lecture}}. Une fiche par famille de capsules
dans docs/prompts/Capsules_*.md, avec les marqueurs exacts « **Nom exact du fichier :** »,
« **▶️ Script ElevenLabs** », « **📄 Transcription affichée sur la page** » ;
capsules : {{medias.audio.capsules}}. outils/verifier_elevenlabs.py d'abord (clé, voix,
v4, quota), puis outils/generer_audio.py --essai. STOP : un TÉMOIN (--temoin), écouté par
l'auteur sur la page, AVANT toute série. Le générateur contrôle débit (105 à 190 mots/min
en v4), durée (déduite des mots) et silences (≤ 3,6 s), met en quarantaine ce qui sort des
clous, n'écrase jamais sans --force ; puis synchronisation des transcriptions et
generer_playlist.py. Une prise trop rapide : une reprise, puis « speaking slowly ». [[FIN]]

[[SI medias.illustrations.actif]]
Illustrations ({{medias.illustrations.outil}}) : une fiche par image (fichier,
dimensions, page, contexte, scène, composition), charte de style en anglais, AUCUN texte
dans l'image, personnages décrits mot pour mot d'une fiche à l'autre ; conversion WebP,
emplacements posés d'avance. STOP : relecture en planche contact. [[FIN]]

[[SI medias.schemas.actif]]
Schémas : tirés du référentiel quand ils portent des chiffres ; explication élément par
élément sous chaque schéma ; [[SI medias.schemas.capsule_par_schema]] une capsule par
schéma, sur le même plan ; [[FIN]] sur un exemple neutre dès qu'ils toucheraient à une
réponse. [[FIN]]
Simulateurs : {{medias.simulateurs}} (ou ta proposition). Glossaire (définition, chapitre
d'introduction, termes vedette, « Où en parle-t-on ? »). [[SI medias.boite_a_outils.actif]]
Boîte à outils : {{medias.boite_a_outils.fiches}} fiches d'une page, avec mini-quiz
expliqués, reprise du cours de référence. [[FIN]]

[[SI tp.actif]]
TP : énoncé et attendus sur la page du TP ; correction dans site/correction/ (étudiants)
et site/correction/formateur/ (formateur), déclarées dans publication.zones_protegees ;
comptes dans docs/acces-zones.json ; deploiement/proteger_zones.py pose la protection
AVANT le premier envoi de la correction (le déployeur retient la zone sinon). [[FIN]]

[[SI ecosysteme.ypareo]]
Cahiers de texte Yparéo (docs/generate_cahier_de_texte.py, un par format) : un bloc par
séance, « CONTENU DE LA SÉANCE » et « TRAVAIL À FAIRE », en .txt et .docx ; version « avec
accès » (identifiants depuis docs/acces.json) dans un dossier ignoré par Git. [[FIN]]

Application Livrables (import-application/, format de {{ecosysteme.doc_import_app}}) :
- cinq feuilles aux en-têtes exacts (Matières, Séances, Livrables, Critères, Ressources),
  séparateur « › » (U+203A) « Année › Promotion › Matière » ; promotions et matières
  EXACTEMENT celles de {{filieres}} ;
- consignes détaillées (5 à 10 phrases), grilles de critères qui totalisent la note
  maximale et s'adossent à la grille officielle, ressources par séance ;
- pièges constatés : deux matières NOUVELLES dans un même fichier → seule la première
  reçoit ses séances (un fichier par promotion) ; réimporter un livrable décoche
  « facultatif » ; un livrable s'identifie par (matière, séance, titre) ; pas de bonus
  négatif ; une note non saisie n'entre pas dans la moyenne ; les réglages d'un QCM se
  font à la main après import. STOP : l'auteur importe et vérifie l'aperçu.

Déploiement (deploiement/deployer.py) vers {{publication.url}} : la destination vient de
deploiement/destination.json (cours {{cours.slug}}, répertoire
{{publication.repertoire_distant}}), JAMAIS de config.json ; SFTP (l'hébergement mutualisé
OVH refuse le FTPS) ; envoi incrémental par carnet déposé sur le serveur, au nom du cours ;
seuls les fichiers de site/ suivis par Git ; garde-fou : refus d'un dossier qui appartient
à un autre cours, d'un dossier sans carnet ou logé dans un autre cours (--adopter
seulement pour reprendre SON cours publié par un ancien outil) ; protections
(.htaccess, .htpasswd, .user.ini, .ovhconfig) jamais écrasées ni purgées. Après chaque
envoi : --essai annonce « déjà à jour », les pages modifiées s'ouvrent, une zone protégée
répond 401 sans identifiants.

# MÉTHODE — PHASES ET JALONS

Phase 0  Paramètres : récapitule ce qui est fourni, déduit, et encore ouvert ; questions
         une à une. STOP.
Phase 1  Conception (section « Concevoir le cours »). STOP.
Phase 2  Étape zéro (template, cours.json, nouveau_cours.py), référentiel du cas et table
         de vérité des résultats de référence (docs/02). STOP.
Phase 3  Squelette, navigation, bascules éventuelles, glossaire.
Phase 4  Contenus : chapitres, un par un. STOP après le premier chapitre (ton, densité,
         explications des quiz), puis à la fin.
Phase 5  TP et sa correction protégée ; modèles adaptés ; corrigés formateur.
Phase 6  Évaluations (QCM en ligne, papier, entraînement), toutes expliquées. STOP.
Phase 7  Audio : fiches, témoin, STOP, série. [[SI medias.audio.actif]]
Phase 8  Illustrations : fiches, message Codex, relecture. [[SI medias.illustrations.actif]]
Phase 9  Yparéo et import Livrables. STOP.
Phase 10 Déploiement : destination vérifiée, zones protégées d'abord, --essai, puis envoi
         (après accord explicite) et vérifications en ligne.
Phase 11 Documentation de reprise : README, docs/00 à 04, DEMARRER-ICI.md retiré.

# CONTRÔLES AVANT CHAQUE MISE EN LIGNE

Référentiel cohérent · verifier_i18n, verifier_contraste, verifier_liens (renvois compris)
sans écart · node --check · aucun octet NUL · captures clair/sombre, chaque filière, 1280
et 375 px, console vide · interdits absents des pages publiques · deployer.py --essai :
destination attendue, garde-fou passé, aucun fichier hors de site/.

# DÉFINITION DE « TERMINÉ »

- Un étudiant de chaque filière suit tous les chapitres, produit ses livrables et
  s'entraîne à l'évaluation sans lien cassé, sans chiffre incohérent, sans réponse
  soufflée — et chaque erreur de quiz lui explique pourquoi, et où relire.
- Le formateur dispose de ses corrigés, évaluations, cahiers de texte et classeurs
  d'import, et sait ce qu'il doit régler à la main dans l'application.
- Le site en ligne est identique au dépôt, au bon endroit, protégé là où il doit l'être,
  et tout se régénère avec la documentation seule.
~~~

---

## 5. Adapter le prompt au type de module

| Type de module | Ce qui change surtout | Conseils |
|---|---|---|
| **Gestion de projet, pilotage, budget** | Livrables documentaires sur modèles (charte, WBS, planning, budget) | Simulateurs de calcul (charge, planning, valeur acquise) ; les mêmes personnes du cas d'un module à l'autre |
| **Architecture, conception** | Schémas, décisions, dossier d'architecture | Schémas expliqués élément par élément, une capsule par schéma ; Boîte à outils de fiches ; TP sur un autre objet que l'exemple du cours |
| **Développement** (front, back, API, tests) | Livrables en code (dépôt Git), revues de code | Exercices « repérer l'erreur » sur du code ; grilles adossées aux critères de l'épreuve |
| **Infrastructure, cloud, sécurité** | Schémas d'architecture, procédures, rapports d'audit | Simulateurs de disponibilité, de coûts, de capacité |
| **Communication, veille, soutenance** | Rapports, présentations, oral | Capsules plus nombreuses ; grilles d'oral ; exercices à embranchements |

Dans tous les cas : un **cas fil rouge** chiffré dans un référentiel unique, des
**livrables progressifs** (version de travail puis finale), une **évaluation au format de
l'épreuve**, des **quiz qui expliquent chaque proposition**, et des exemples de méthode
sur un **cas neutre** quand ils toucheraient à une réponse.

---

## 6. Annexe — un bloc rempli, pour un cours fictif

Un modèle de remplissage, à comparer au vôtre. Le cours, ses chemins et son dépôt sont
fictifs.

~~~yaml
cours:
  titre: "Sécurité des applications web"
  slug: "securite-applications-web"
  code_module: "FM03"
  bloc: "Bloc 3 — Sécuriser une application"
  annee: "2026-2027"
  langues: ["fr"]
  palette: "ardoise"
  public: "développeurs en alternance, à l'aise avec HTTP et une API REST, sans formation sécurité ; deux jours en présentiel"
  formats: ["2j"]
  format_impose: "2j"
  calendrier: {jour_1: "<date réelle>", jour_2: "<date réelle>"}
  horaires: {matin: "09:00-12:30", apres_midi: "13:30-17:00"}
  ton: "vouvoiement chaleureux, registre d'un collègue expérimenté ; peu d'écrit, beaucoup de pratique"
filieres:
  - {id: dev, libelle: DEV, titre: "<intitulé du titre>", rncp: "<RNCPxxxxx>", competences: [], epreuve: "<ECxx>",
     couleur: "#3B5BDB", fiche_module: "sources/<fiche>.docx", grille: "sources/<grille>.docx",
     promotion_app: "2026-2027 › <Promotion>", matiere_app: "<matière exacte>"}
groupe_mixte: false
fil_rouge: {nom: "<le cas du cours>", source: "sources/fil-rouge/", projet_par_filiere: {}, referentiel: "outils/cas.py"}
tp: {actif: true, sujet: "<un autre objet que l'exemple du cours>", correction_protegee: true}
interdits: ["<mots du sujet du TP>"]
livrables:
  - {id: "01", titre: "Analyse de risques", modele: "", format_depot: ".docx",
     version_de_travail: {existe: true, notee: false, obligatoire: true, jour: 1, heure: "17:00"},
     version_finale: {jour: 2, heure: "17:00", note_max: 20, coefficient: 2, grille: true}}
  - {id: "qcm", titre: "QCM de fin de module", modele: "", format_depot: "en ligne",
     version_de_travail: {existe: false},
     version_finale: {jour: 2, heure: "15:00", note_max: 20, coefficient: 1, grille: false}}
malus_version_de_travail: 2
evaluation:
  qcm_en_ligne: {actif: true, notation: "CBM", questions: 30}
  qcm_papier: {actif: false}
  qcm_entrainement: {actif: true, questions_par_filiere: 30}
  points_de_controle: true
medias:
  audio: {actif: true, modele: "eleven_v4", accent: "strong Parisian French accent",
          capsules: ["accueil", "ouverture de chapitre", "TP pas à pas"], temoin_avant_serie: true}
  illustrations: {actif: false}
  schemas: {actif: true, explication_element_par_element: true, capsule_par_schema: true}
  simulateurs: ["score de risque"]
  glossaire: true
  boite_a_outils: {actif: false}
ecosysteme:
  gabarit_technique: "C:/projets/template_cours"
  app_livrables: "https://livrables.elafrit.com/"
  ypareo: true
publication:
  url: "https://exemple.org/teaching/securite-web/2026-2027/"
  repertoire_distant: "/www/teaching/securite-web/2026-2027"
  zones_protegees: ["correction/", "correction/formateur/"]
git:
  depot: "<compte>/<Cours_Securite_Web>"
  prive: true
  auteur: "Mohamed Amine EL AFRIT <elafrit.mohamed@gmail.com>"
  co_auteur: false
~~~
