# Registre des travaux — template_cours

> Fichier de suivi du gabarit. **À lire en premier** à la reprise du travail ; « ce qui reste à faire » se répond à
> partir de lui. Dernière mise à jour : **2026-11-21**
>
> Ce qui a été fait, session par session et avec ses commits : [`JOURNAL.md`](JOURNAL.md). Ni ce registre ni le
> journal ne partent dans un cours créé (`nouveau_cours.py` ne recopie de la racine que ce que liste `COPIER`) ; un
> cours tient son propre `TODO.md`.

## 🗺️ Le grand chantier · douze lots (cadré le 21 novembre)

Demandé par l'auteur le 21 novembre 2026, d'après l'analyse des cours EADL/ERIS, CDWFS/ASRC et d'architecture
logicielle ; cadré question par question (`JOURNAL.md`, section du 21 novembre). Chaque lot se termine par ses
contrôles, l'accord pour commiter, puis l'accord séparé pour pousser ; l'audio, l'arabe et le polycopié commencent
par un témoin.

| Sujet | Décision de l'auteur |
|---|---|
| Page d'accueil | le modèle du cours d'architecture (bandeau, quatre cartes, capsule, sections numérotées, cartes Polycopié et Podcasts) et les cartes de chapitre illustrées d'EADL, adaptés aux filières |
| Capsules | une au début de chaque section, de l'accueil et des chapitres, en plus des capsules d'accueil et d'ouverture ; par filière quand la section diffère ; une piste par langue |
| Filières | un paramètre du prompt : deux (EADL et ERIS, ou CDWFS et ASRC) ou une seule, à préciser ; la bascule d'EADL (`filiere.js`, `filiere.css`) |
| Langues | un paramètre du prompt : français, anglais, arabe, une à trois ; site miroir à N langues (`en/`, `ar/` de droite à gauche) ; le bouton FR · EN · AR garde la position de lecture |
| Démo | deux filières (EADL et ERIS) et les trois langues |
| École | `outils/seances.py`, source unique du cahier de texte Yparéo (avec ou sans accès), du classeur d'import Livrables (cinq feuilles, d'après `C:/projets/Livrables_App_Etudiants/docs/PROMPT-CLASSEUR-IA.md`) et des sections Livrables et Programme de l'accueil |
| Codex | Claude Code vérifie `codex --version`, puis lance `codex exec` lui-même (dossier dédié, aucun commit côté Codex, conversion et contrôle ensuite) ; sans Codex, la procédure d'installation et de connexion, vérifiée en ligne, puis arrêt ; le kit d'illustration des cours |
| Générateur | une page locale, jamais publiée, hors de `site/`, ouverte d'un double clic ; les valeurs habituelles dans un fichier local ignoré par git ; un prompt de lancement appuyé sur le tronc et les modules du gabarit, avec le dépôt GitHub, le répertoire et l'adresse de déploiement, et des commits au seul nom de l'auteur |
| Prompts | le tronc refondu (pièges avec parade, décisions à ne pas redemander, critères d'acceptation, nouveaux paramètres) ; les modules langues, Codex et école ; les 16 prompts numérotés relus et rangés ; sans tirets cadratins |
| Polycopié | six livrets (trois langues, deux filières), l'arabe de droite à gauche dans Word, un QR « Écouter » par section ; régénérés à la fin |
| Documentation | un README refait, un guide par nouveauté, les modèles de journal de décisions et de CHANGELOG dans chaque cours créé, un contrôle des guides en retard |
| Polices | hébergées dans le gabarit, dont une police arabe (défaut relevé : les pages chargent Google Fonts, contre le § 7) |
| Apports | la correction des QCM expliquée et ses garde-fous (biais de longueur, aucune question de l'épreuve dans l'entraînement) ; Boîte à outils et Modèles pas à pas ; bibliographie vérifiée ; vitesse audio partagée et simulateurs verrouillés |
| Mise en ligne | la démo sur `https://mohamedelafrit.com/teaching/cours_demo`, à la fin, après un essai à blanc |

Les lots, dans l'ordre validé :

- [ ] **1. Fondations** : polices locales ✅ (`a28b685`) ; la démo passée au site miroir ✅ (`59474ee`, `a008dac`)
  et le générateur qui la suit ✅ (`3f50098`), avancés du lot 4 sur décision de l'auteur ; le socle à plusieurs
  langues ✅ (`3d941a7` : le groupe « FR · EN · عربي », la liste `TPL_MIROIR`, le panneau ♿ traduit) ; la mise
  en page de droite à gauche et les outils à plusieurs langues ✅ (`737e23b`) ; le témoin arabe, le chapitre 1 ✅
  (`d301d41`, lexique `docs/LEXIQUE-ar.md`) ; la bascule de filière ✅ (`0f8a846` : `filiere.js` générique,
  `filieres.css` généré, EADL en émeraude et ERIS en prune, le menu ☰ sur téléphone) ; les paramètres
  filières et langues de `cours.json` ✅ (`f3cc344` : une, deux ou aucune filière, l'arabe après la langue
  racine, le tout écrit dans le `course-data.js` du cours créé). Restent : l'arabe comme racine (lot 4) ;
  les outils qui ignorent encore l'arabe (`hreflang.py`, `generer_playlist.py`,
  `synchroniser_capsules.py`) ; la bascule sur les pages du QCM, qui ne chargent pas les données du cours,
  et la liste de lecture par filière du cours EADL, si l'auteur les veut. Relevés en chemin, à traiter dans
  ce lot : `xlsx.full.min.js`, que le tableau de bord du QCM charge d'un CDN, contre le § 7 (l'héberger
  demande l'accord de l'auteur pour le téléchargement) ; la validation de `nouveau_cours.py`, qui exige les
  titres en français même d'un cours de racine anglaise (`titre.fr`, `sous_titre.fr`, titres des
  chapitres) ; les liens hreflang, que `hreflang.py` poserait dans 32 pages maintenant que l'adresse de la démo
  est connue sur ce poste : avant, qu'il sache l'arabe, et que `nouveau_cours.py` efface ses blocs (sinon un cours
  créé hériterait des liens de la démo). D'ici là, `hreflang.py --essai` signale ces 32 pages sur ce poste.
- [ ] **2. Bloc école** : `seances.py`, cahier de texte Yparéo, classeur d'import Livrables, fragments Programme et
  Échéances ; pour l'accueil, les boutons des épreuves de chaque filière (`BOUTONS` de `outils/accueil.py`), la
  pastille « diplôme, bloc et module », et un cours créé qui reçoit ses boutons de `cours.json`. Décisions de
  l'auteur (22 novembre) : « avec ou sans accès » veut dire les deux (le cahier avec et sans les identifiants du
  site, et la voie de l'application Livrables, colonne Contenu de ses séances, quand l'auteur n'a pas accès à
  Yparéo) ; le programme sur l'accueil ; un seul format, la bascule de format attendant un cours qui en déclare
  deux ; les dates réelles et les promotions dans `outils/sessions.py`, versionné dans un cours, fictif dans le
  gabarit ; une version de travail obligatoire et non notée ; le programme de démonstration (deux jours, quatre
  séances) ; la carte Durée en jours. Fait : `seances.py`, `programme.py`, le programme et les échéances de
  l'accueil, un programme vide dans un cours créé (`088a1a8`) ; `sessions.py` et le cahier de texte, texte et
  Word, avec et sans identifiants, qui remplace l'ancien générateur (`0211023`) ; le classeur d'import Livrables
  (cinq feuilles, un par promotion, la colonne Contenu reprise du cahier) et, à côté, les réglages que l'import ne
  porte pas (`b4426fb`). Décision de l'auteur pour le classeur : le QCM noté de la démo en « Exercice / TP »,
  rendu par son fichier CSV, car le type « QCM » de l'application corrige une grille d'après un corrigé à lettres
  fixes. La pastille et les boutons des épreuves de l'accueil, d'après `FILIERES` de `seances.py`, sur le modèle
  du cours EADL (`7914eb8`) ; la démonstration n'en déclare aucune (décision de l'auteur). Le bloc `ecole` de
  `cours.json` (`4deb980`) : un cours créé reçoit ses boutons, les épreuves de ses filières et ses sessions ; le
  modèle porte Livrables, le QCM et une session d'exemple fictive, que le script signale (décisions de l'auteur).
  La documentation, GUIDE (section 2 ter) et CHECKLIST (phase 14 bis) (`15b456b`). Reste l'arabe, qui attend
  l'accueil arabe (lot 4). Relevé en chemin, à trancher avec l'auteur : la page du QCM demande d'envoyer le
  CSV au formateur « par e-mail », alors que les consignes du classeur demandent de le déposer dans
  l'application Livrables.
- [x] **3. Page d'accueil**, avec les fiches de ses capsules de section. Redemandée par l'auteur le
  21 novembre, avec un troisième modèle, le cours de veille technologique (`Cours_EADL_Veille_Techno`), et
  traitée avant le bloc école. L'accueil ✅ (`0910118` : français et anglais, `outils/accueil.py`, couleurs du
  bandeau contrôlées, accueil des cours créés) ; ses capsules ✅, en français (`93728b3`) et en anglais
  (`0d3d1df`) : chaque fois le témoin puis les huit autres textes validés, deux fiches
  (`docs/prompts/Capsules_accueil.md`, `Capsules_accueil_en.md`), transcriptions reportées dans les pages par
  `synchroniser_capsules.py`. Ce qui en dépend ailleurs : l'enregistrement des dix-huit pistes et leur place dans
  la liste de lecture (lot 9) ; l'accueil arabe (lot 4) ; les illustrations des cartes (lot 5) ; les boutons des
  épreuves et la pastille (lot 2, faits : `7914eb8`). Relevés en chemin (la
  faute « police lecture adaptée » est corrigée sur décision de l'auteur, `0d10e75`) : l'espace insécable devant
  « : », posée sur l'accueil et dans ses transcriptions, absente des autres pages ; le lien de l'auteur, en pied
  de chaque page, qui mène à « # » ; le texte d'exemple de `public.parcours` (`cours.exemple.json`), qui porte
  un tiret cadratin, et son commentaire, qui le dit affiché sur l'accueil alors qu'aucune page ne l'affiche.
- [ ] **4. Démo en trois langues** : le passage au site miroir est fait (avancé au lot 1, `59474ee`), et le
  chapitre 1 est en arabe (le témoin, `d301d41`). Restent : la relecture de ce témoin par un lecteur
  arabophone ; les quinze autres pages en arabe ; la transcription arabe de la capsule 1, écrite dans la page, à
  reporter dans la fiche des capsules quand `synchroniser_capsules.py` saura l'arabe ; les fiches des capsules
  de section des chapitres.
- [ ] **5. Codex** : le kit, puis les illustrations des cartes de chapitre et de l'accueil ; le schéma arabe du
  chapitre 1 (`chapitre-1-schema-1-trois-decisions.ar.webp`, la première décision à droite, comme ses points).
- [ ] **6. Apports** : correction des QCM et garde-fous, Boîte à outils, Modèles pas à pas, bibliographie, petits
  moteurs.
- [ ] **7. Prompts** : tronc, modules, bibliothèque. Les prompts 01, 03, 05 et 13 décrivent encore la bascule 🌐
  des blocs `data-tr` comme celle de la démo.
- [ ] **8. Générateur de prompt.**
- [ ] **9. Enregistrement audio** : `verifier_elevenlabs.py` d'abord, témoins, séries, quota suivi au registre ;
  la capsule arabe du chapitre 1 (`chapitre-1-capsule-ar.mp3`, nom déjà appelé par la page) ; les dix-huit
  capsules de l'accueil, textes validés (témoins `accueil-capsule-fr.mp3` et `accueil-capsule-en.mp3`), et leur
  place dans la liste de lecture (`generer_playlist.py` n'indexe que les chapitres).
- [ ] **10. Polycopié** : six livrets, témoin d'abord.
- [ ] **11. Documentation** et son contrôle. `GUIDE.md`, `CHECKLIST.md`, `ARCHITECTURE.md` et le skill bilingue
  décrivent encore la bascule 🌐 comme celle de la démo.
- [ ] **12. Mise en ligne** de la démo : la première ✅ le 22 novembre, à la demande de l'auteur, sur
  `https://mohamedelafrit.com/teaching/cours_demo/` (120 fichiers, sans purge ; `destination.json` gardé local,
  exclu par `.git/info/exclude` ; essai à blanc comparé à Git ; 19 adresses à 200 et console vide en ligne).
  Restent : un nouvel envoi après chaque lot (essai à blanc, accord) ; les liens hreflang (lot 1) ; la question des
  zones protégées, puisque le corrigé du QCM et le tableau de bord sont en accès libre, comme sur GitHub.

## 📍 Où en est le gabarit (1er novembre)

| Élément | État |
|---|---|
| Site de démonstration | ✅ trois chapitres en site miroir depuis le 21 novembre (le français à la racine, l'anglais sous `en/`), sept composants RDCX, QCM, glossaire, flashcards, activités, atelier |
| Méthode | ✅ prompt paramétrable : un tronc et neuf modules (`prompts/modules/`) ; exigences de l'auteur au § 2 de `CLAUDE.md` |
| Bilingue | ✅ site miroir `en/` (décision du 25 octobre), outillé, seul modèle que crée `nouveau_cours.py` depuis le 21 novembre ; `data-tr` décrit pour les cours qui l'ont déjà ; les libellés écrits en dur relevés par les cours passent par `ui-labels.js` (183 clés) |
| Outils repris du cours d'architecture logicielle | ✅ **tous** : site miroir, interdits, référentiel et fragments, « Où en parle-t-on ? », page Podcasts, polycopié |
| Corrections des cours de veille et d'avant-projet | ✅ les corrections génériques, en quatre lots et un correctif (31 octobre et 1er novembre) ; leurs nouveautés attendent la décision de l'auteur (ci-dessous) |
| `nouveau_cours.py` | ✅ blocs `podcasts` et `livret` inactifs par défaut (`livret` demande `glossaire`) ; chaque page d'un cours créé garde son sous-titre ; la liste des médias repart vide ; les filières et les langues de `cours.json` (21 novembre) |
| Contrôles | ✅ dix (`CLAUDE.md` § 6) : les neuf lançables verts ; le dixième, `verifier_tirets.py` (ajouté le 6 novembre), rouge sur le gabarit lui-même — le lot « gabarit sans tirets » reste à faire. Plus ceux du site miroir, de la série de podcasts et du polycopié |

## 🆕 Dernières entrées

> ### 🆕 22 novembre · lot 2, la documentation
> Le GUIDE décrit l'école pas à pas (section 2 ter) et la CHECKLIST lui consacre une phase (14 bis).
> `15b456b`. Le lot 2 est fait, hors l'arabe, qui attend le lot 4.
> ### 🆕 22 novembre · lot 2, le bloc école de cours.json
> Un cours créé reçoit de `cours.json` ses boutons (Livrables, QCM), les épreuves de ses filières et ses
> sessions (promotion, matière, dates réelles). Le modèle porte une session d'exemple fictive, que le script
> signale. `4deb980`. Restent la documentation (GUIDE, CHECKLIST) et l'arabe.
> ### 🆕 22 novembre · lot 2, la pastille et les boutons des épreuves
> Une filière qui prépare l'épreuve d'un bloc la déclare dans `FILIERES` (`outils/seances.py`) : l'accueil
> ajoute à sa pastille « EADL, Bloc 1, module FM04 » et un bouton vers la page de ses épreuves. La démo n'en
> déclare aucune. `7914eb8`. Reste le bloc `ecole` de `cours.json`.
> ### 🆕 22 novembre · lot 2, le classeur Livrables
> `outils/generer_classeur_livrables.py` écrit le classeur d'import (cinq feuilles, un par promotion) et, à
> côté, les réglages que l'import ne porte pas, relus dans le guide et le code de l'application. Le QCM noté
> de la démo passe en « Exercice / TP ». `b4426fb`. Restent les boutons des épreuves, la pastille et le bloc
> `ecole`.
> ### 🆕 22 novembre · lot 2, le cahier de texte Yparéo
> `outils/sessions.py` porte les seules dates du dépôt ; `outils/generer_cahier_de_texte.py` écrit le cahier
> en texte et en Word, avec et sans les identifiants du site, et remplace l'ancien générateur. `0211023`.
> Reste le classeur Livrables.
> ### 🆕 22 novembre · lot 2, le programme sur l'accueil
> `outils/seances.py`, source unique du bloc école et sans aucune date, porte les séances, le travail et les
> livrables ; l'accueil en tire son programme, ses échéances et la durée en jours. Sept décisions de l'auteur,
> dont le programme de démonstration. `088a1a8`. Restent le cahier de texte et le classeur Livrables.
> ### 🆕 22 novembre · la démo en ligne
> Sur `https://mohamedelafrit.com/teaching/cours_demo/`, à la demande de l'auteur : essai à blanc d'abord,
> 120 fichiers envoyés sans purge, contrôlés en ligne. En chemin, un mot de passe cité en exemple dans un
> commentaire du générateur de cahier de texte, public depuis août, remplacé par un exemple neutre (`0ac89d7`).
> ### 🆕 21 novembre · lot 3 terminé, les capsules anglaises de l'accueil
> Les neuf capsules traduites des textes français validés, témoin d'abord, dans les formulations anglaises
> de la démonstration, et reportées dans `en/index.html`. Le lot 3 est fermé ; ce qui en dépend passe aux
> lots 2, 4, 5 et 9. `0d3d1df`. Détail : `JOURNAL.md`, section du 21 novembre.
> ### 🆕 21 novembre · lot 3, les capsules de l'accueil
> Neuf textes en français, le témoin d'abord, tous validés par l'auteur : la bienvenue, une capsule par
> filière, une par section. `synchroniser_capsules.py` reporte leurs transcriptions dans l'accueil. Restent
> l'anglais et l'enregistrement. `93728b3` ; la faute « police lecture adaptée », `0d10e75`.
> ### 🆕 21 novembre · lot 3, la page d'accueil
> Celle des cours d'architecture et d'avant-projet : un bandeau sombre, ses boutons et ses cartes, les
> capsules d'accueil et de section, les cartes des chapitres, un bouton flottant. Ses couleurs restent lisibles
> dans chaque palette et pour chaque filière ; un cours créé reçoit la même structure, à rédiger. `0910118`.
> Détail : `JOURNAL.md`, section du 21 novembre.
> ### 🆕 21 novembre · lot 1, les filières et les langues d'un cours
> `cours.json` déclare les filières d'un cours (une, deux ou aucune) et ses langues (le français, l'anglais,
> l'arabe après la langue racine) ; `nouveau_cours.py` les valide et les écrit dans le `course-data.js` du
> cours créé, titres et libellés arabes compris. `f3cc344`. Détail : `JOURNAL.md`, section du 21 novembre.
> ### 🆕 21 novembre · lot 1, la bascule de filière
> Celle du cours EADL, rendue générique : les filières se déclarent dans `course-data.js`, `filiere.js` pose
> la bascule (le menu ☰ sur téléphone) et le bandeau, `filieres.css` (généré) masque l'autre filière ; EADL en
> émeraude, ERIS en prune ; un témoin dans « Le fil rouge » du chapitre 1, en trois langues. `0f8a846`. Détail :
> `JOURNAL.md`, section du 21 novembre.
> ### 🆕 21 novembre · lot 1, le témoin arabe et la mise en page de droite à gauche
> Le chapitre 1 existe en arabe, page retournée, interface et glossaire en arabe, d'après le lexique arrêté par
> l'auteur (`docs/LEXIQUE-ar.md`). La feuille de style suit le sens de lecture, sans rien changer au français ;
> les outils savent l'arabe ; une capsule ou un schéma attendu ne provoque plus d'erreur 404. `737e23b`,
> `d301d41`. Détail : `JOURNAL.md`, section du 21 novembre.
> ### 🆕 21 novembre · lot 1, le socle à plusieurs langues
> Le site miroir connaît trois langues : la liste `TPL_MIROIR` (la langue racine, puis les pages de chaque
> dossier de langue), le groupe « FR · EN · عربي » de l'en-tête (décisions de l'auteur), `dir="rtl"` pour l'arabe,
> et le panneau ♿ enfin traduit. `3d941a7`. Détail : `JOURNAL.md`, section du 21 novembre.
> ### 🆕 21 novembre · lot 1, la démo en site miroir, et le générateur qui la suit
> Décisions de l'auteur : convertir la démo avant le témoin arabe, et un générateur qui ne crée plus que des cours
> en site miroir. Les 16 pages ont leur jumelle anglaise sous `en/` (0 écart de parité, titres et descriptions
> traduits) ; `nouveau_cours.py` fait naître chaque page dans la langue racine, et corrige quatre défauts plus
> anciens (les squelettes s'annonçaient « Chapitre 1 : Cadrer son cours »). `59474ee`, `a008dac`, `3f50098`.
> Détail : `JOURNAL.md`, section du 21 novembre.
> ### 🆕 21 novembre · lot 1, les polices hébergées avec le site
> Les pages ne chargent plus rien de Google : 16 fichiers woff2 et leurs six licences OFL dans `site/assets/fonts/`,
> déclarés dans `fonts.css`, dont deux polices arabes pour la suite du lot. `demarrer.py` sert les woff2 et les WebP
> avec leur type. `a28b685`. Détail : `JOURNAL.md`, section du 21 novembre.
> ### 🆕 21 novembre · les objectifs toujours affichés, une seule copie du gabarit, le grand chantier cadré
> L'en-tête de chapitre pliable est retiré : les objectifs restent toujours affichés (`7591b19`). Le gabarit n'a
> plus qu'une copie de travail, `C:\projets\Cours\template_cours`, où les secrets de l'autre copie sont rangés sans
> être ouverts ; le chemin du prompt est corrigé (`95afe78`). Puis le cadrage, question par question, d'un chantier
> en douze lots (ci-dessus). Détail : `JOURNAL.md`, section du 21 novembre.
> ### 🆕 21 novembre · le gabarit sans tirets, lot S3 : les pages de ressources
> 104 tirets retirés des neuf pages de ressources, ponctuation seule ; le sous-titre du cours corrigé dans
> `course-data.js`, d'où la page du polycopié le reprend. 175 → 69 dans `site/`. `617017d`. Détail : `JOURNAL.md`,
> section du 21 novembre.
> ### 🆕 21 novembre · le gabarit sans tirets, lot S2 : les chapitres 2 et 3
> 74 tirets retirés de `02-structurer.html` et `03-multimedia.html` avec les choix du témoin ; les transcriptions des
> capsules enregistrées ne changent que de ponctuation, dans la fiche. 249 → 175 dans `site/`. `14a944c`. Détail :
> `JOURNAL.md`, section du 21 novembre.
> ### 🆕 21 novembre · le gabarit sans tirets, lot S1 : les moteurs partagés
> `ui-labels.js`, `interactions.js`, `podcasts.js`, `media.js`, `quiz.js` et le séparateur des points de schéma du
> livret, sans tiret : 290 → 249 dans `site/`. Les choix du cours de veille EADL (D36), validés par l'auteur sur le
> tableau des remplacements. `e8ea658`. Détail : `JOURNAL.md`, section du 21 novembre.
> ### 🆕 21 novembre · le prompt 15 sans tiret, `--ecraser` prudent
> Le prompt 15 ne prescrit plus le tiret cadratin pour une incise (virgules ou parenthèses ; renvois « § 3 · Titre »),
> et `nouveau_cours.py --ecraser` garde en place les fichiers locaux d'un cours (secrets, carnets d'envoi,
> destination, quarantaine), qu'il supprimait. `a1a6a45`, `ad2c4a7`. Détail : `JOURNAL.md`, section du 21 novembre.
> ### 🆕 21 novembre · deux correctifs repris du cours de veille EADL
> Le texte posé sur les fonds primaires reste lisible en thème sombre (`--on-primary`, `--primary-hover` ; vérificateur
> de contraste qui suit les `var()`), et le cahier de texte se produit sans identifiants (`--sans-acces --site
> ADRESSE`). `8a7d0db`, `7710d98`. Détail : `JOURNAL.md`, section du 21 novembre.
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
(chapitre 1, `ea1cc23`) est fait et son style validé ; `outils/verifier_tirets.py` reste rouge, **97 tirets dans
12 fichiers de `site/`** (69 après les lots S1 à S3 ; la conversion de la démo au site miroir, le 21 novembre, a
dédoublé les pages du QCM et leurs dictionnaires). La suite, en cinq lots (style du témoin, régénération des fichiers générés, `verifier_tirets`
à 0 par lot) :

- ✅ **S1 · les moteurs partagés** (fait le 21 novembre, `e8ea658`) : `ui-labels.js` (26), `interactions.js` (6), `podcasts.js` (6), `media.js` (2),
  `quiz.js` (1). Priorité : leur chrome s'injecte dans toutes les pages (« Before reading — … », le séparateur
  « titre — texte » des points de schéma). S'y rattache, pour le livret, `outils/polycopie/rendu.py` (ligne 977, le
  même séparateur de points de schéma).
- ✅ **S2 · les chapitres** (fait le 21 novembre, `14a944c`) : `02-structurer.html` (37), `03-multimedia.html` (37), sur le modèle du témoin.
- ✅ **S3 · les pages de ressources** (fait le 21 novembre, `617017d`) : `atelier` (40), `activites` (15), `about` (10), `polycopie` (10), `cours` (9),
  `index` (6), `glossaire` (5), `polycopies` (5), `podcasts` (4).
- **S4 — le QCM** : `QCM/index` (17), `corrections.js` (13), `dashboard` (11), `correction` (11), `entrainement` (7),
  `questions.js` (4), `qcm-core.js` (2). ⚠️ La signature SHA-256 des banques : toucher au texte d'une question change
  le CSV signé (skill `cours-qcm-cbm`), à traiter avec soin. Depuis le 21 novembre, les quatre pages du QCM ont
  leur jumelle sous `en/`, aux mêmes tirets ; le squelette du QCM qu'écrit `nouveau_cours.py` en a aussi
  (« QCM — … »).
- **S5 · les données** : `course-data.js` fait au lot S3 (`617017d`) ; reste `flashcards-data.js` (4).

Puis, hors du champ de `verifier_tirets.py` (il ne lit que `site/`, html/js/css) : `CLAUDE.md` (30) et `prompts/`
(~440, des `.md`), ce que lisent les futurs cours. `prompts/15_explications_quiz.md` est déjà fait (21 novembre,
`a1a6a45`) : sa règle prescrivait le tiret.

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

- `deploiement/destination.exemple.json` donne pour adresse d'exemple `https://exemple.org/…`, un domaine qui
  n'est pas réservé : passer à `example.org`, comme le livret.

## 🧩 Candidats repris des cours, à décider avec l'auteur

**Le 21 novembre, l'auteur a retenu dans le grand chantier** (ci-dessus) : les filières, les illustrations par Codex,
l'école (séances, Yparéo, Livrables), la Boîte à outils, les Modèles pas à pas, la correction des QCM et ses
garde-fous, la bibliographie, la vitesse audio partagée et les simulateurs verrouillés. Les autres candidats restent
ci-dessous.

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
- **`generer_playlist.py --essai`**, et des titres sans `&nbsp;` dans la liste de lecture. Constaté le 21 novembre :
  appelé avec `--essai`, l'outil réécrit sa liste, faute de connaître l'option.
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
- **Cours d'étude d'avant-projet** (`C:\projets\Cours\Cours_EADL_ERIS_Etude_Avant_Projet`) : son mode d'emploi de
  l'import (`import-application/README.md`, réglage 2) fait cocher « facultatif » sur les versions de travail
  pour les sortir de la moyenne. Dans l'application, cette case (« Livrable bonus, facultatif ») les rend non dues,
  et un étudiant qui ne les rend pas sort du compteur des manquants ; la moyenne, elle, ne compte que les
  livrables notés (relevé le 22 novembre dans le guide et le code de l'application). À proposer à l'auteur, dans
  son dépôt.
- **Tout cours créé avant le 25 octobre** n'a ni les outils du site miroir, ni les interdits, ni les fragments, ni
  « Où en parle-t-on ? », ni la page Podcasts, ni le polycopié : chaque module (`prompts/modules/`) dit comment les
  ajouter à un cours existant. **Tout cours créé avant le 1er novembre** n'a pas les corrections des lots 1 à 4 ni
  la liste des médias : `JOURNAL.md` les détaille fichier par fichier.

## ❓ À décider avec l'auteur

L'ordre de la suite, la recette complète et la relecture de la documentation sont tranchés par le grand chantier
(lots 11 et 12). Restent :

- le répertoire distant de la démo, au lot 12 (l'adresse publique est décidée) ;
- la typographie française des pages : une espace ordinaire précède souvent le deux-points, qui peut alors commencer
  une ligne à 375 px (relevé au chapitre 1) ; à proposer avant de corriger (§ 2) ;
- à faire par l'auteur : supprimer la seconde copie `C:\projets\template_cours`, qui ne garde plus que deux anciens
  fichiers ElevenLabs et un cache de polycopié.

## 📌 Conventions

Celles du § 2 de `CLAUDE.md`, en particulier : commits au seul nom de l'auteur, sans mention d'outil ; une question à
la fois, cliquable, la recommandation d'abord ; accord avant de commiter et de pousser — **ce dépôt est public** :
pousser, c'est publier ; secrets jamais lus ; un exemple avant toute série.
