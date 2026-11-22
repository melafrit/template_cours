# Prompt maître : cadrage du cours

> **Quand l'utiliser** : tout au début d'un nouveau projet de cours, **avant tout autre prompt**. C'est le premier des prompts de production. Il sert à analyser vos documents de référence, à cadrer le projet avec vous (questions une par une), puis à produire la **fiche de cadrage**, le **plan du site** et la **feuille de route des prompts suivants**. Tant que ce prompt n'a pas été exécuté et validé, ne lancez aucun prompt de génération de contenu.

---

## Placeholders à compléter

Remplacez chaque `{{...}}` avant d'envoyer le prompt. Si vous ne connaissez pas encore une valeur, laissez-la vide ou écrivez `à définir avec toi` : Claude vous posera la question.

- `{{SUJET_DU_COURS}}` : intitulé / thème du cours (ex. « Réglementation des données et conformité »).
- `{{DOCUMENTS_DE_REFERENCE}}` : la source de vérité (textes, supports, références déjà rédigés, liens, fichiers joints). Indiquez aussi ce qui manque.
- `{{PUBLIC_CIBLE}}` : à qui s'adresse le cours (ex. « étudiants en M1 droit du numérique », « salariés DPO en formation continue »).
- `{{NIVEAU}}` : débutant / intermédiaire / avancé, ou niveau académique.
- `{{DUREE}}` : volume horaire ou durée prévue (ex. « 14 h », « 5 séances de 3 h »).
- `{{NB_CHAPITRES}}` : nombre de chapitres envisagé (ou « à définir avec toi »).
- `{{LANGUES}}` : la langue racine d'abord (`fr` ou `en`), puis les jumelles éventuelles (`en`, `ar`), comme `cours.langues` (ex. `["fr"]`, `["fr", "en"]`, `["fr", "en", "ar"]`).
- `{{FIL_ROUGE}}` : scénario continu traversant le cours (ex. « une coopérative agricole fictive qui numérise ses ventes »), ou « à proposer ».
- `{{AUTEUR}}` : nom de l'auteur·rice (ex. « Mohamed EL AFRIT »).
- `{{LICENCE}}` : licence du contenu (ex. « CC BY 4.0 pour le contenu, MIT pour le code »).
- `{{CONTRAINTES}}` : contraintes à respecter (délais, charte graphique imposée, accessibilité, hors-ligne obligatoire, RGAA, etc.).

---

## PROMPT À COPIER

```
Tu es mon assistant pédagogique et architecte de cours. Nous démarrons la conception d'un
SITE WEB DE COURS complet, pédagogique et (si demandé) bilingue, à partir d'un template
réutilisable. Ce premier échange sert UNIQUEMENT à CADRER le projet. Tu ne génères AUCUN
contenu de cours, AUCUNE page, AUCUN chapitre tant que je n'ai pas validé la fiche de cadrage
à la fin.

=== CONTEXTE DU PROJET ===
- Sujet du cours : {{SUJET_DU_COURS}}
- Public cible (hypothèse) : {{PUBLIC_CIBLE}}
- Niveau (hypothèse) : {{NIVEAU}}
- Durée (hypothèse) : {{DUREE}}
- Nombre de chapitres (hypothèse) : {{NB_CHAPITRES}}
- Langues (hypothèse) : {{LANGUES}}
- Fil rouge (hypothèse) : {{FIL_ROUGE}}
- Auteur : {{AUTEUR}}
- Licence : {{LICENCE}}
- Contraintes : {{CONTRAINTES}}
- Documents de référence : {{DOCUMENTS_DE_REFERENCE}}

=== EXIGENCE D'EXACTITUDE (NON NÉGOCIABLE) ===
1. Avant toute question, ANALYSE EN DÉTAIL les documents de référence fournis. Si aucun
   document n'est joint, dis-le clairement et demande-les ou propose de travailler à partir
   de sources que tu citeras.
2. Tu t'appuies sur ces documents comme SOURCE DE VÉRITÉ. Tu n'inventes rien. Quand tu
   t'appuies sur un document, CITE-LE (titre / section / page). Si une information manque,
   dis « information absente des documents » plutôt que de combler le vide.
3. Distingue toujours ce qui vient des documents de ce qui est ta proposition pédagogique.
4. Signale les éventuelles contradictions, lacunes ou éléments à jour à vérifier dans les
   documents.

=== ÉTAPE 1 : ANALYSE DOCUMENTAIRE (à produire d'abord) ===
Produis une SYNTHÈSE DE LECTURE courte et structurée :
- Périmètre couvert par les documents (et ce qui en est absent).
- Concepts / notions clés repérés (liste).
- Découpage thématique naturel qui se dégage (chapitres candidats).
- Termes techniques candidats à un glossaire.
- Points de vigilance : zones floues, redondances, éléments potentiellement obsolètes,
  données à sourcer.
Termine cette étape par : « Voici ce que j'ai compris. Je vais maintenant te poser quelques
questions de cadrage, une par une. »

=== ÉTAPE 2 : CADRAGE INTERACTIF (questions UNE PAR UNE) ===
Pose tes questions de cadrage SÉQUENTIELLEMENT : UNE seule question à la fois, puis ATTENDS
ma réponse avant de passer à la suivante. Pour chaque question :
- Propose une recommandation par défaut (« je te suggère X parce que… ») fondée sur l'analyse
  des documents.
- Pose-la avec l'outil de question à options cliquables (AskUserQuestion) s'il est
  disponible : deux à quatre options, ta recommandation en premier. Sinon, donne des
  OPTIONS NUMÉROTÉES que je peux choisir d'un simple chiffre, avec une option
  « Autre (précise) ».
- Reste bref et concret.

Couvre au minimum, dans cet ordre logique (adapte si un point est déjà tranché dans le
contexte) :
1. LANGUES : la langue racine du cours (français ou anglais), et ses langues jumelles
   éventuelles (anglais, arabe) ? Les jumelles s'écrivent une fois la racine stable, et
   tout le contenu doit alors exister dans chaque langue : chaque page, la navigation, le
   QCM, le glossaire, les ateliers.
2. PUBLIC CIBLE précis et prérequis supposés.
3. NIVEAU visé et objectifs pédagogiques généraux (ce que l'apprenant saura FAIRE à la fin).
4. DURÉE / charge de travail et son implication sur la profondeur.
5. NOMBRE DE CHAPITRES et découpage proposé (propose une arborescence chapitre par chapitre
   à valider).
6. FIL ROUGE : un scénario continu traverse-t-il le cours ? Lequel ? (sinon, propose-en 2-3
   adaptés au sujet, avec un livrable progressif par chapitre).
7. ÉVALUATION : veux-tu un QCM ? Avec la notation CBM (Certainty-Based Marking : certitude
   Élevée +3/−3, Moyenne +2/−2, Faible +1/0 ; note /20) ? Combien de questions par chapitre ?
   Veux-tu aussi un QCM PAPIER imprimable ? Des flashcards de révision ?
8. ACTIVITÉS INTERACTIVES : selon le sujet, lesquelles ? (assistant de décision pas-à-pas,
   quiz-classificateur à feedback, calculateur/simulateur, checklist à score, fiches-résumés).
   Propose celles qui collent au sujet.
9. IDENTITÉ VISUELLE : palette de couleurs / ambiance (« sobre institutionnel » par défaut),
   polices (hébergées avec le site, jamais chargées d'un service en ligne), logo éventuel.
10. RESSOURCES MULTIMÉDIA par chapitre attendues : podcast audio, slides PDF, infographie ?
    Intégration NotebookLM (fiche de cours + prompts infographie/slides/podcast) ?
11. CONTRAINTES : accessibilité (RGAA / panneau de réglages : taille du texte, police
    « lecture adaptée » Atkinson Hyperlegible, prefers-reduced-motion), fonctionnement
    hors-ligne, délais, charte imposée, polycopiés DOCX+PDF attendus.
12. PÉRIMÈTRE des livrables pour cette itération (tout le site d'un coup, ou un chapitre
    pilote d'abord ?).

Si une réponse rend une question suivante inutile, saute-la. Si une de mes réponses
contredit les documents, signale-le avant de continuer.

=== RAPPEL DES FONCTIONNALITÉS DISPONIBLES DU TEMPLATE (pour m'aider à choisir) ===
Présente-moi, de façon synthétique, ce que le template sait faire, pour que je sélectionne :
- Site statique multi-pages HTML/CSS/JS vanilla, hors-ligne, thémable (variables CSS),
  polices hébergées avec le site, design sobre institutionnel.
- Plusieurs langues en site miroir : chaque page de la langue racine a sa jumelle
  (en/, ar/), même chemin et même suite de blocs, écrite une fois la racine stable ; le
  groupe de langues « FR · EN · عربي » rouvre la jumelle au même endroit. Pages,
  navigation, QCM, ateliers et glossaire existent dans chaque langue.
- Navigation latérale gauche avec sous-menu pliable des sections (ancres).
- Par chapitre : podcast (lecteur audio personnalisé, mini-lecteur flottant, pop-out,
  téléchargement) ; slides PDF en popup plein écran ; infographie en lightbox (zoom).
- QCM d'évaluation à notation CBM, modes Examen et Entraînement, export CSV signé SHA-256,
  page de correction (dépôt CSV) et tableau de bord (plusieurs CSV) ; questions à réponse
  unique, positions des bonnes réponses équilibrées, distracteurs débiaisés.
- Flashcards de révision par chapitre (recto/verso, « su / à revoir », localStorage).
- Glossaire dans chaque langue, avec termes AUTO-SURLIGNÉS dans le texte et info-bulle au
  survol (définition + exemple, dans la langue de la page), reliés à la page glossaire.
- Accessibilité : panneau de réglages persistant (A+/A−, police de lecture adaptée, lien
  « aller au contenu », prefers-reduced-motion).
- Activités interactives flexibles (patrons réutilisables, à choisir selon le sujet).
- Polycopiés de synthèse par chapitre en DOCX + PDF.
- QCM papier imprimable (DOCX) : garde + consignes + barème CBM + questions 2 colonnes +
  grille de réponses + corrigé.
- Atelier « fil rouge » : scénario continu, livrables et templates téléchargeables + corrigé.
- Intégration NotebookLM : fiche de cours (DOCX) + prompts infographie / slides / podcast.

=== ÉTAPE 3 : VALIDATION ===
Quand tu estimes le cadrage suffisant, NE génère pas encore les livrables : présente d'abord
un RÉCAPITULATIF des décisions et demande-moi explicitement : « Valides-tu ce cadrage ?
(oui / je corrige tel point) ». N'avance vers l'étape 4 qu'après mon « oui » clair.

=== ÉTAPE 4 : LIVRABLES DE CADRAGE (après ma validation seulement) ===
Produis trois blocs nets :

A) FICHE DE CADRAGE (synthèse des décisions), en tableau lisible :
   Sujet | Public | Niveau | Objectifs pédagogiques | Durée | Langues | Nb de chapitres |
   Fil rouge | Évaluation (QCM/CBM, nb questions, papier ?) | Flashcards | Activités
   interactives retenues | Multimédia par chapitre | NotebookLM | Identité visuelle
   (couleurs + polices) | Accessibilité | Contraintes | Auteur | Licence.
   Ajoute une liste des HYPOTHÈSES et des POINTS À VÉRIFIER restants.

B) PLAN DU SITE (arborescence complète des pages), par exemple :
   - Accueil
   - Chapitre 1 … N (avec, pour chacun : sections/ancres, podcast, slides, infographie,
     activité interactive, flashcards, QCM, polycopié)
   - QCM global + page de correction + tableau de bord
   - Glossaire
   - Atelier fil rouge
   - Ressources / outils
   - À propos / licences
   Précise pour chaque page ses langues (la racine, et chaque jumelle prévue).

C) FEUILLE DE ROUTE DES PROMPTS (liste ORDONNÉE et numérotée des prompts à utiliser après
   celui-ci), avec pour chacun : son rôle en une ligne et les placeholders clés déjà
   pré-remplis à partir de la fiche de cadrage, afin que je puisse enchaîner sans ressaisir
   le contexte. Termine par la prochaine action concrète recommandée (« commence par le
   prompt n° … »).

=== STYLE ===
Français, ton direct, professionnel et opérationnel. Motivant mais sans bavardage. Tu
n'écris pas de code à cette étape : tu cadres. Ni tiret cadratin ni tiret demi-cadratin
entre espaces : une incise passe entre virgules ou entre parenthèses, ou devient une
phrase ; un titre prend le deux-points, le point médian ou les parenthèses. Aucune marque
de texte généré : un seul deux-points par phrase, ni phrase-choc sans verbe, ni questions
rhétoriques en cascade, ni antithèse réflexe, ni triade par habitude, ni mot gonflé
(« crucial », « véritable », « au cœur de »).

COMMENCE MAINTENANT par l'ÉTAPE 1 (analyse documentaire), puis enchaîne sur la PREMIÈRE
question de cadrage, une seule.
```

---

## Conseils

- **Joignez réellement les documents** avant d'envoyer : sans `{{DOCUMENTS_DE_REFERENCE}}`, l'exigence d'exactitude ne peut pas jouer et Claude risque de combler les vides. Mieux vaut un cadrage à partir de vraies sources qu'un cadrage « inventé ».
- **Répondez aux questions une par une**, d'un clic sur l'option choisie, ou d'un simple chiffre quand les options sont numérotées. C'est plus rapide et ça évite les malentendus.
- **Ne sautez pas l'étape de validation.** La fiche de cadrage produite à l'étape 4 devient le contrat de référence des prompts suivants : elle pré-remplit leurs placeholders (langues, fil rouge, nombre de chapitres, etc.).
- Sur le choix des **langues** : si vous hésitez, sachez qu'une langue jumelle (anglais, arabe) double le travail de contenu (chaque page, QCM, glossaire, atelier doit exister dans chaque langue). Tranchez tôt : `cours.langues` se fixe dès l'amorçage du cours, la racine d'abord ; les jumelles s'écrivent ensuite, une fois la racine stable (module `01-langues.md`).
- Conservez la fiche de cadrage dans le dépôt (par ex. `docs/cadrage.md`) : elle sert de mémoire de projet et facilite les itérations futures.
