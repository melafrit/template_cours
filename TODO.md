# Registre des travaux — template_cours

> Fichier de suivi du gabarit. **À lire en premier** à la reprise du travail ; « ce qui reste à faire » se répond à
> partir de lui. Dernière mise à jour : **2026-11-06**
>
> Ce qui a été fait, session par session et avec ses commits : [`JOURNAL.md`](JOURNAL.md). Ni ce registre ni le
> journal ne partent dans un cours créé (`nouveau_cours.py` ne recopie de la racine que ce que liste `COPIER`) ; un
> cours tient son propre `TODO.md`.

## 📍 Où en est le gabarit (1er novembre)

| Élément | État |
|---|---|
| Site de démonstration | ✅ trois chapitres en blocs `data-tr` (le modèle de secours), sept composants RDCX, QCM, glossaire, flashcards, activités, atelier |
| Méthode | ✅ prompt paramétrable : un tronc et neuf modules (`prompts/modules/`) ; exigences de l'auteur au § 2 de `CLAUDE.md` |
| Bilingue | ✅ site miroir `en/` par défaut (décision du 25 octobre), outillé ; `data-tr` en secours ; les libellés écrits en dur relevés par les cours passent par `ui-labels.js` (183 clés) |
| Outils repris du cours d'architecture logicielle | ✅ **tous** : site miroir, interdits, référentiel et fragments, « Où en parle-t-on ? », page Podcasts, polycopié |
| Corrections des cours de veille et d'avant-projet | ✅ les corrections génériques, en quatre lots et un correctif (31 octobre et 1er novembre) ; leurs nouveautés attendent la décision de l'auteur (ci-dessous) |
| `nouveau_cours.py` | ✅ blocs `podcasts` et `livret` inactifs par défaut (`livret` demande `glossaire`) ; chaque page d'un cours créé garde son sous-titre ; la liste des médias repart vide |
| Contrôles | ✅ dix (`CLAUDE.md` § 6) : les neuf lançables verts ; le dixième, `verifier_tirets.py` (ajouté le 6 novembre), rouge sur le gabarit lui-même — le lot « gabarit sans tirets » reste à faire. Plus ceux du site miroir, de la série de podcasts et du polycopié |

## 🆕 Dernières entrées

> ### 🆕 7 novembre — le gabarit sans tirets : le témoin (chapitre 1) et le plan de la série
> Le chapitre vitrine (`01-cadrage.html`, recopié en `_modele.html`) réécrit sans tiret cadratin, de 47 à 0 ; style
> validé par l'auteur (incise → virgule / parenthèses / deux-points ; renvoi « Source — Titre » → « · » ; titres de
> contrôle → deux-points). Deux sources corrigées nettoient tous les chapitres (podcast, « Où en parle-t-on ? ») : le
> total `site/` tombe de 375 à 290. Correctif au passage : `synchroniser_capsules` garde les fins de ligne. `ea1cc23`,
> `55d362a`. Le reste de la série : voir « Le gabarit sans tirets ». Détail : `JOURNAL.md`, section du 7 novembre.
> ### 🆕 7 novembre — la chaîne du polycopié sans tirets du chrome, les capsules à venir (lot fc09f26)
> Repris en générique du cours d'avant-projet (`fc09f26`, D55/D56) : le chrome du livret sans tirets (puces « ◦ » et
> « • », `couper_titre` « Libellé : sujet », mentions, copyright, marge, TOC, index, couverture, capitales qui
> gardent l'accent) et les capsules à venir (QR code à l'adresse prévue, sans durée ; « capsules à venir : N »).
> Témoin avant/après : 17 → 12 tirets, les 5 du chrome `fc09f26` retirés. `9fc7dbc`. Détail : `JOURNAL.md`, section
> du 7 novembre.
> ### 🆕 6 novembre : les exigences nées dans le cours d'étude d'avant-projet (lot « règles »)
> Au § 2 de `CLAUDE.md` : ni tirets cadratins ni marques de texte généré (« Le contenu ») ; un texte enregistré ne
> change pas sans réenregistrer sa piste, sauf la ponctuation de sa transcription, le nom d'une piste fixé avant son
> enregistrement, le quota épuisé au registre (« L'audio ») ; les banques d'une épreuve traitées comme des secrets
> (« Les secrets ») ; la liste de l'essai à blanc comparée à git, `--purge` jamais sans accord (« La publication »).
> Le dixième contrôle, `outils/verifier_tirets.py`, au § 6, à la checklist et au tronc du prompt. Détail :
> `JOURNAL.md`, section du 6 novembre.
> ### 🆕 6 novembre — le menu au clavier et les durées insécables (lot 6)
> Deux corrections génériques de plus, reprises du cours de veille : le menu latéral s'annonce (`aria-expanded`,
> `aria-controls`) et se ferme au clavier (Échap rend le focus au bouton) ; les durées des fragments passent en
> espaces insécables (`6e6179c`). Détail : `JOURNAL.md`, section du 6 novembre.
> ### 🆕 31 octobre et 1er novembre — les corrections des cours de veille et d'avant-projet
> Ce que deux cours créés depuis le gabarit ont corrigé en production, repris en générique, un lot par commit : les
> scénarios sans boutons, « [object Object] », le menu d'une page de QCM, les listes à puce (`9141009`) ; les
> libellés écrits en dur des moteurs (`150f25d`) ; l'info-bulle du glossaire en bulle fixe ou en bandeau, et ses
> homonymes (`518df86`) ; plus d'erreur 404 en console (`0732822`) ; dans le livret, de vraies espaces insécables et
> plus aucune réponse soufflée (`9125f33`). Détail : `JOURNAL.md`, section du 31 octobre et du 1er novembre.
> ### 🆕 26 octobre — le polycopié, puis sept correctifs
> La chaîne du polycopié du cours de référence, en générique et bilingue (`797e08a`, `31fb7d1`, `4443c55`) : livret
> Word et PDF tiré des pages du site, QR codes cliquables, page « 📘 Polycopié », publication dans `site/livret/`,
> livret de démonstration publié, bloc `livret`. Puis : la page des fiches orpheline, le menu du prompt, le nom
> « Fiches de synthèse », le renvoi au polycopié retiré d'un cours sans livret, les sous-titres écrasés dans un cours
> créé, la fenêtre de la fiche bilingue (`6d413b1` à `28b19c8`). Détail : `JOURNAL.md`, section des 25 et
> 26 octobre, § 6 et 7.
> ### 🆕 25 octobre — la remise à niveau sur les cours de production
> Sécurité (`.rgignore`, hôte masqué), règles de production dans `CLAUDE.md`, licences ; le prompt en tronc et
> modules ; le site miroir par défaut et ses outils ; les interdits ; le référentiel et ses fragments ; « Où en
> parle-t-on ? » ; la page Podcasts ; le libellé du bouton ♿. Détail : `JOURNAL.md`, section des 25 et 26 octobre,
> § 1 à 5.

## 🛠️ Ouvert — dans le gabarit

**Le gabarit sans tirets** (D55, en cours) : réécrire sans tiret cadratin tout ce que l'apprenant lit. Le témoin
(chapitre 1, `ea1cc23`) est fait et son style validé ; `outils/verifier_tirets.py` reste rouge, **290 tirets dans
25 fichiers de `site/`**. La suite, en cinq lots (style du témoin, régénération des fichiers générés, `verifier_tirets`
à 0 par lot) :

- **S1 — les moteurs partagés** : `ui-labels.js` (26), `interactions.js` (6), `podcasts.js` (6), `media.js` (2),
  `quiz.js` (1). Priorité : leur chrome s'injecte dans toutes les pages (« Before reading — … », le séparateur
  « titre — texte » des points de schéma). S'y rattache, pour le livret, `outils/polycopie/rendu.py` (ligne 977, le
  même séparateur de points de schéma).
- **S2 — les chapitres** : `02-structurer.html` (37), `03-multimedia.html` (37), sur le modèle du témoin.
- **S3 — les pages de ressources** : `atelier` (40), `activites` (15), `about` (10), `polycopie` (10), `cours` (9),
  `index` (6), `glossaire` (5), `polycopies` (5), `podcasts` (4).
- **S4 — le QCM** : `QCM/index` (17), `corrections.js` (13), `dashboard` (11), `correction` (11), `entrainement` (7),
  `questions.js` (4), `qcm-core.js` (2). ⚠️ La signature SHA-256 des banques : toucher au texte d'une question change
  le CSV signé (skill `cours-qcm-cbm`) — à traiter avec soin.
- **S5 — les données** : `course-data.js` (2), `flashcards-data.js` (4).

Puis, hors du champ de `verifier_tirets.py` (il ne lit que `site/`, html/js/css) : `CLAUDE.md` (30) et `prompts/`
(~440, des `.md`), ce que lisent les futurs cours.

Les deux défauts de `media.js` relevés le 26 octobre sont réglés : les fenêtres des diapositives et de l'infographie
parlent la langue de la page (`150f25d`), et `media.js` ne demande plus que les médias déposés (`0732822`).

À proposer à l'auteur, puis à corriger dans un commit séparé (`CLAUDE.md` § 2, jamais en silence) :

- `site/assets/js/ui-labels.js`, `nav.reinitialiserConfirme` : « Réinitialiser votre progression (chapitres
  terminés) ? » a une espace ordinaire avant le point d'interrogation, là où il faut une insécable.
- Même fichier, en anglais, `controle.placeholder` : « even unsure » pour « even if unsure ».

Relevés le 1er novembre :

- **L'info-bulle du glossaire et la liste de lecture ne suivent pas la bascule de langue d'une page `data-tr`** :
  `glossaire-tooltip.js` lit la langue une fois, au chargement (sa définition reste dans cette langue), et
  `playlist.js` garde ses libellés ; aucun des deux n'écoute `tpl:langchange`. Sans effet en site miroir, où chaque
  page a sa langue ; visible dans la démonstration, qui est en `data-tr`.
- **`verifier_i18n.py` ne reconnaît que l'appel `T('clé')`** : 58 clés passent pour « jamais appelées » (43 au
  26 octobre). 36 sont appelées autrement (le `t(clé, défaut)` de `media.js`, une clé passée en variable ou à une
  fonction d'aide), 6 sont construites par `compteur()` (`erreurs.compte1`…) ; 16 restent à démêler, construites ou
  mortes (`etapes.termine`, `flash.acquis`, `flash.compteARevoir`…). Apprendre ces chemins au contrôle, puis retirer
  les clés mortes avec l'accord de l'auteur.
- **Les titres d'onglet d'un cours monolingue** restent bilingues sur les pages de ressources (« Glossaire —
  Glossary », « Sommaire du cours — Course contents ») : `nouveau_cours.py` ne doit garder que la langue du cours
  (relevé le 26 octobre).

Relayés par le cours de veille (3 novembre), vérifiés sur place le 6 novembre. Les deux premiers sont faits (lot 6,
`6e6179c`) ; les trois autres restent à proposer avant de corriger :

- ✅ **Le menu latéral s'annonce et se ferme au clavier** (`navigation.js`) : `aria-expanded` (vrai sur grand écran,
  sur téléphone seulement quand la colonne est ouverte), `aria-controls`, et Échap qui referme et rend le focus au
  bouton — fait au lot 6, vérifié au navigateur. Cours de veille, `1277986`.
- ✅ **Les durées des fragments sont insécables** (`generer_fragments.py`, `duree()`) : l'insécable entre le nombre
  et l'unité et avant les minutes — fait au lot 6. Cours de veille, `165f574`.
- **Le livret coupe les dates « AAAA-MM-JJ »** : le modèle de date porte des traits d'union insécables, et dans une
  colonne étroite Word coupait au milieu (« AAAA-MM-J », puis « J »). Rendre ordinaires les tirets de ce seul modèle
  dans le livret (`polycopie/rendu.py` : `MODELE_DATE`, `TIRET_INSECABLE`) et comparer les deux tirets à l'identique
  dans `polycopie/controles.py` (`_norm`). Cours de veille, D49, `bcc373f` — à vérifier à la reprise.
- **Un fragment peut vivre dans un bloc d'une autre langue** : `generer_fragments.py`, `contextes()`, pourrait suivre
  aussi l'attribut `lang` d'un élément (une copie modèle en anglais dans une page française), plus seulement
  `data-tr` ; le `lang` de `<html>` reste ignoré, à dessein. Cours de veille, D51, `553f2b1` — à vérifier à la
  reprise.
- **« Où en parle-t-on ? » ne lit ni les exercices ni les corrections** : `glossaire_emplois.py` ne compte pas un
  terme employé seulement dans les données d'un exercice (script de page) ou dans une page de correction ; il paraît
  alors inemployé. À documenter, ou à corriger, avant d'arbitrer un terme. Cours de veille, relevé le 1er novembre.

Un point relayé le 3 novembre ne demande rien : l'accord du bilan d'un QCM d'entraînement. Le gabarit n'a pas ce
moteur, et son propre bilan (`qcm-core.js`, `entrainement.html`, dashboard) ne pose aucun mot pluriel après un nombre
(vérifié le 6 novembre). Si ce défaut apparaît un jour, le motif est celui des compteurs `x.compte1` / `x.compteN`.

Plus mineurs :

- Dans un cours créé, `chapitres/_modele.html` demande le schéma de la démonstration
  (`chapitre-1-schema-1-trois-decisions.fr.webp`), retiré avec `site/assets/media/schemas/` : le composant affiche
  « image attendue », comme voulu, mais la console garde une erreur 404. Garder les images de la vitrine, ou faire
  passer les schémas par la liste des médias (`media-data.js`).
- `deploiement/destination.exemple.json` donne pour adresse d'exemple `https://exemple.org/…`, un domaine qui
  n'est pas réservé : passer à `example.org`, comme le livret.
- `demarrer.py` laisse Python deviner le type des fichiers : sous Windows, les WebP partent en
  `application/octet-stream` (sans effet visible). Déclarer `image/webp`.

## 🧩 Candidats repris des cours, à décider avec l'auteur

Relevés le 31 octobre dans le cours de veille technologique (`C:\projets\Cours\Cours_CDWFS_ASRC_Veille_Techno`) et
le cours d'étude d'avant-projet (`C:\projets\Cours\Cours_EADL_ERIS_Etude_Avant_Projet`). Ce sont des nouveautés, pas
des défauts : chacune demande l'accord de l'auteur et, le plus souvent, un bloc de `nouveau_cours.py`.

Pour le site :

- **Un bloc « filières »**, pour un cours suivi par deux publics : la bascule de filière (`filiere.js`,
  `filiere.css`) ; tant que l'apprenant n'a pas choisi, les deux versions s'affichent.
- **L'indice de longueur dans les chapitres** : les contrôles du gabarit le mesurent dans les banques de QCM, pas dans
  les points de contrôle ni dans les scénarios (`RDCX.checkpoint`, `RDCX.branch`) ; le cours de veille le fait
  (`generer_correction_qcm.py`, `indice_chapitres`, sa décision D42).
- **Les illustrations** : un emplacement réservé tant que l'image n'est pas produite (`.illu`, « Illustration à
  venir », cours de veille) ; des cartes de chapitre illustrées (cours d'avant-projet).
- **Un bouton « Copier »** sous les prompts donnés à l'apprenant (`copier.js`, cours de veille).
- **`generer_playlist.py --essai`**, et des titres sans `&nbsp;` dans la liste de lecture.
- **La page du glossaire** du cours de veille (`glossaire-page.js`, `glossaire.css`) et ses sections dans le menu de
  gauche (`data-menu-sections`).
- **Les durées de lecture calculées** (D54, `165f574`) : `outils/durees_lecture.py` compte les mots des
  `content-section` des chapitres français (hors scripts, boutons, `sr-only`, SVG et blocs d'une autre filière),
  150 mots/min, arrondi, au moins 1 min, puis `referentiel.DUREES = durees()`. Le gabarit écrit `DUREES` à la main
  (`{"1": 30, …}`) et `nouveau_cours.py` le vide pour un cours créé. Les noms de filière (`only-cdwfs`, `only-asrc`)
  sont propres au cours — à lire dans la configuration, ou à retirer si le gabarit n'a pas de filières.

Nouveaux générateurs, repris du cours de veille (2 et 3 novembre), à décider :

- **Des corrigés en composants** (D51, D52) : `outils/corriges_composants.py` rend des blocs Markdown structurés
  (en-tête, encadré du dépôt, sommaire, l'essentiel, journal, source notée critère par critère, synthèse d'IA triée,
  étapes, document, diapositive 16:9, question du jury…) ; `outils/publier_corrections_livrables.py` les publie dans
  une zone protégée (fragments remplis, typographie française hors `lang="en"`) ; `corriges.css` n'emploie que la
  charte. Leçon générique déjà bonne à savoir : une page hors gabarit qui masque du texte avec `.sr-only` doit porter
  la règle elle-même, `interactions.css` n'y étant pas chargé (`publier_correction_eb.py`, `6516128`). Candidat à un
  bloc « corrigés ».
- **Les modèles des livrables** (D22, D53, `7963aac`) : `outils/generer_modeles.py` et `outils/modeles_fr.py`
  fabriquent les modèles Word et Excel en français et en anglais, contrôlés (intitulés exacts, aucun nom, propriétés
  vides, pas de mode de compatibilité) ; `--livrable` ne refabrique qu'un livrable, car refabriquer change les dates
  internes et renverrait tous les fichiers au serveur. Le gabarit n'a pas de générateur de modèles. Candidat à un
  bloc « modèles ».

Pour le polycopié (la fiche du cours de veille, `outils/livret.py`, en montre les clés) :

- un glossaire réduit aux termes que le livret emploie (`glossaire`) ; les pages du cas et des livrables autour des
  chapitres (`parties`) ; des phrases qui ne valent qu'à l'écran (`ecran_seul`) ; un livret par filière
  (`filieres`) ;
- une présentation de l'auteur proposée, que seul le témoin imprime tant qu'elle n'est pas validée
  (`presentation_a_valider`) ;
- de nouveaux types d'encadrés, des pages de notes, des QR codes vers les réponses des points de contrôle et vers
  les flashcards ;
- les interdits du cours contrôlés dans le texte du livret (`controles.regles`, ses `motifs`) — le module 02 promet
  déjà ce contrôle —, et des contrôles du PDF.

Relevés le 6 novembre dans le cours d'étude d'avant-projet, après le lot « règles » (`JOURNAL.md`) :

- ✅ **La chaîne du polycopié** — fait au lot `9fc7dbc` (7 novembre, cf. `JOURNAL.md`) : les capsules à venir (D56),
  `couper_titre` « Libellé : sujet », les capitales qui gardent l'accent, les puces « ◦ » au second niveau, et les
  libellés du livret (mentions, copyright, marge, TOC, index, couverture) sans tirets. Restent, au lot « gabarit sans
  tirets », le chrome que `fc09f26` ne touchait pas (légende de podcast, puces de schéma) et le corps des pages.
- **Les outils** : le report des transcriptions par la ponctuation seule, qui refuse si un mot change ; la liste de
  l'essai à blanc reconstituée depuis git ; le relevé des tirets des banques du QCM, remis à l'auteur.
- **L'évaluation** : des banques d'entraînement distinctes de celles de l'épreuve, comparées automatiquement (le
  module 05 tire aujourd'hui le QCM papier de la banque publiée du site).
- **Les blocs** : la correction protégée par filière, avec une capsule par partie ; la bibliographie publiée et
  vérifiée ; la Boîte à outils (fiches méthode, quiz, modèles, capsules) ; les modèles pas à pas (captures annotées) ;
  la méthode des séries par lots (témoin, lots confiés à des agents, intégration, recette, mise en ligne).

Non repris :

- Les exclusions plancher du déployeur du cours d'avant-projet (`*.md`, prises archivées) : sans objet dans le
  gabarit, qui ne suit aucun `.md` sous `site/` et range ses témoins audio dans `outils/quarantaine/` ; le déployeur
  n'envoie déjà que les fichiers de `site/` suivis par Git.
- Le correctif anglais de `lecture.py` (le rapport de section) : il porte sur un composant propre au cours.

Gardés en note, pour le jour où ces générateurs viendraient au gabarit (il n'a ni l'un ni l'autre) : les livrets
papier sur deux colonnes (D56 du cours de veille, `generer_evaluations_papier.py`) et la marque `{fr:…}` des QCM
anglais, rendue `<span lang="fr">` (`qcm/qcm_commun.py`).

## 🔗 Ouvert — dans les cours créés depuis le gabarit (hors de ce dépôt)

- **Cours de veille technologique** (`C:\projets\Cours\Cours_CDWFS_ASRC_Veille_Techno`) : sa liste « Remontées pour le
  gabarit » (`TODO.md`) peut se mettre à jour — dix de ses treize remontées sont dans le gabarit ; restent la bascule
  de filière, `generer_playlist.py --essai` et l'indice de longueur, candidats ci-dessus. Dans son dépôt, avec
  l'accord de l'auteur.
- **Cours UML · C4 · BPMN · EPC** (`C:\projets\Cours\Cours_UML_C4_EPC_BPMN`, en blocs `data-tr`) : le libellé du
  bouton ♿ (`site/assets/js/accessibility.js`, ligne 69 : correctif `299c203`) ; les sous-titres de ses pages
  activités, atelier, sommaire, glossaire, fiches et de son chapitre 3, écrasés par celui du cours à sa création
  (`c81717f`) ; le passage au site miroir, une fois son français stable.
- **Cours CDWFS** : le seuil d'apparition des sections longues (`animations.js`, `threshold: 0.08` ; correctif
  `f80bd8b`, relevé le 25 octobre) ; un correctif a été lancé le 26 octobre dans une autre session : à vérifier.
- **Cours d'architecture logicielle** (le cours de référence) : deux commentaires de sa chaîne du polycopié à
  corriger ; son registre (`TODO.md`) les détaille.
- **Tout cours créé avant le 25 octobre** n'a ni les outils du site miroir, ni les interdits, ni les fragments, ni
  « Où en parle-t-on ? », ni la page Podcasts, ni le polycopié : chaque module (`prompts/modules/`) dit comment les
  ajouter à un cours existant. **Tout cours créé avant le 1er novembre** n'a pas les corrections des lots 1 à 4 ni
  la liste des médias : `JOURNAL.md` les détaille fichier par fichier.

## ❓ À décider avec l'auteur

- L'ordre de la suite : les défauts ouverts du gabarit, les candidats des cours, la mise à niveau des cours
  existants, ou un nouveau cours.
- Une recette complète : un cours créé avec tous ses blocs, mené jusqu'au livret publié et à sa version en site
  miroir, pour éprouver l'ensemble de bout en bout.
- Une relecture d'ensemble de la documentation (README, modules, `CLAUDE.md`), qui a beaucoup changé depuis le
  25 octobre.

## 📌 Conventions

Celles du § 2 de `CLAUDE.md`, en particulier : commits au seul nom de l'auteur, sans mention d'outil ; une question à
la fois, cliquable, la recommandation d'abord ; accord avant de commiter et de pousser — **ce dépôt est public** :
pousser, c'est publier ; secrets jamais lus ; un exemple avant toute série.
