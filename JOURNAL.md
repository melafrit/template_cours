# Journal du gabarit

> Ce qui a été fait sur le gabarit, session par session, avec ses commits. Ce qui reste à faire est dans
> [`TODO.md`](TODO.md), le registre, à lire en premier à la reprise du travail. Les deux fichiers, à la racine, ne
> partent jamais dans un cours créé : `nouveau_cours.py` ne recopie de la racine que ce que liste `COPIER` — alors que
> tout `docs/` part dans chaque cours.
>
> « Décision de l'auteur » signale un choix tranché par l'auteur ; le reste découle des règles de `CLAUDE.md` (§ 2).

---

## 6 novembre 2026 : les exigences nées dans le cours d'étude d'avant-projet

Le but : reprendre dans le gabarit les exigences que l'auteur a formulées en produisant le cours d'étude
d'avant-projet (`C:\projets\Cours\Cours_EADL_ERIS_Etude_Avant_Projet`), lu sans être modifié, pour les prochains
cours. **Décision de l'auteur** : les règles d'abord, dans ce lot ; la chaîne du polycopié, le gabarit sans tirets et
les nouveaux blocs ensuite, au registre.

### Ce qui change

- `CLAUDE.md`, § 2. « Le contenu » : ni tirets cadratins ni marques de texte généré (demande de l'auteur du
  3 novembre), avec les conventions des titres. « L'audio » : un texte enregistré ne change pas sans réenregistrer sa
  piste, sauf la ponctuation de sa transcription (décision du 5 novembre) ; le nom d'une piste est fixé avant son
  enregistrement ; quota épuisé, les enregistrements attendent en tête du registre. « Les secrets » : les banques
  d'une épreuve notée. « La publication » : la liste de l'essai à blanc comparée à git ; `--purge` jamais sans
  accord. Au § 6, dix contrôles.
- `outils/verifier_tirets.py` (nouveau) : le tiret cadratin et le « – » entre espaces dans ce que l'apprenant lit
  (texte des pages, chaînes des scripts, `content:` des styles), sans les commentaires ni les messages de console ;
  code 1 s'il en reste. Contre-épreuve sur le cours d'avant-projet : il retrouve exactement les 73 et 60 tirets de
  ses banques de QCM, et aucun dans ses chapitres.
- `prompts/PROMPT-Cours-parametrable.md` : la règle 11 et le contrôle avant mise en ligne. `docs/CHECKLIST.md` : la
  case du contrôle.

### Ce qui reste

Le gabarit n'est pas encore sans tirets : 375 dans 28 fichiers de `site/`, où le contrôle est rouge, environ 440 dans
`prompts/` et 29 dans `CLAUDE.md`. Au registre, avec la chaîne du polycopié, les outils et les nouveaux blocs.

### Pièges appris

- **Une expression régulière qui contient un guillemet trompe un lexeur naïf** : il croit ouvrir une chaîne et
  avale le code jusqu'au guillemet suivant. Le contrôle reconnaît la barre oblique qui ouvre une expression (après un
  opérateur, une parenthèse ou un mot comme `return`).
- **Un message de console n'est pas lu par l'apprenant** : ses chaînes ne comptent pas.

---

## 6 novembre 2026 — le menu au clavier et les durées insécables (lot 6)

Deux corrections génériques de plus, reprises du cours de veille technologique et transmises par sa session, dans un
seul commit après accord de l'auteur. Rien n'est poussé sans son accord (dépôt public).

- `6e6179c` — `navigation.js` : le bouton `.sidebar-toggle` du menu latéral porte `aria-expanded` (vrai sur grand
  écran, où la colonne reste visible ; sur téléphone, vrai seulement quand elle porte `.open`), tenu à jour au clic,
  à la fermeture (voile, clic sur un lien) et au `change` du media query `(max-width: 768px)` ; `aria-controls`
  désigne la colonne, à qui un id `sidebar-nav` est donné au chargement plutôt que d'éditer les douze pages ; Échap
  referme le menu ouvert sur téléphone et rend le focus au bouton. Cours de veille, `1277986`.
  `generer_fragments.py`, `duree()` : l'espace entre le nombre et l'unité, et avant les minutes, devient insécable
  (« 30 min » et « 1 h 20 » se coupaient dans un en-tête de chapitre étroit) ; les quatre pages à durée régénérées.
  Cours de veille, `165f574`.

Vérifié : les huit contrôles lançables du § 6 verts ; `node --check` et `py_compile` ; les durées contrôlées octet
par octet (« 1 h 20 », « 25 min »). Au navigateur (serveur local, un chapitre) : à 1280 px
`aria-expanded` vaut « true » et la console est vide ; à 375 px l'ouverture le passe à « true », Échap le repasse à
« false », ferme le menu et **rend le focus au bouton** ; thème sombre lisible. L'accord du bilan d'un QCM, relayé le
même jour, ne demandait rien — le gabarit n'a pas ce moteur et ne pose aucun mot pluriel après un nombre.

---

## 31 octobre et 1er novembre 2026 — les corrections des cours de veille et d'avant-projet

Le but : reprendre dans le gabarit, en générique, ce que deux cours créés depuis lui ont corrigé en production — le
cours de veille technologique (`C:\projets\Cours\Cours_CDWFS_ASRC_Veille_Techno`) et le cours d'étude d'avant-projet
(`C:\projets\Cours\Cours_EADL_ERIS_Etude_Avant_Projet`), lus sans être modifiés. **Décision de l'auteur** : les
corrections génériques en quatre lots, un commit par lot après son accord ; les nouveautés des cours au registre, à
décider. À sa demande, un correctif s'y est ajouté : les erreurs 404 de la console. Cinq commits, puis celui de ce
journal ; aucune mise en ligne (le gabarit ne se déploie jamais).

### 1. Les défauts avérés — `9141009`, 31 octobre

- **Les scénarios à embranchements des chapitres 1 et 3 n'avaient aucun bouton** : ils passaient `options`, alors que
  `RDCX.branch` lit `choix`. Le moteur accepte les deux, les chapitres passent `choix` — le chapitre 1 devient
  `_modele.html` dans chaque cours créé, et c'est de lui qu'on copie.
- **« [object Object] »** : l'info-bulle et les flashcards lisaient comme une chaîne une définition `{ fr, en }` ; la
  carte retournée suit maintenant la bascule de langue.
- `navigation.js` compte la racine du site depuis `TPL_RACINE` : le menu d'une page rangée plus bas (`QCM/`) menait à
  côté. Défaut latent dans le gabarit, dont aucune page de QCM n'a de menu.
- Les listes d'objectifs et « À retenir » sont en flux normal à toutes les largeurs (la règle ne valait que sous
  768 px) ; un encadré qui cite une longue adresse ne déborde plus.
- `media.js` ne cherche plus les fiches d'un cours qui n'a pas le bloc « polycopies ».
- Les outils corrigés par le cours de veille, en générique : `synchroniser_capsules.py` (toutes les capsules d'une
  fiche sans séparateurs `---`, la durée « ≈ 1 min 10 », la jumelle du site miroir), `glossaire_emplois.py` (plus de
  renvoi vers une page exclue de la mise en ligne), `generer_audio.py` (les pistes des jumelles de `site/en/`, que le
  générateur ne parcourait pas).
- `generer_fragments.py` : sous Windows, une page en fins de ligne CRLF passait toujours pour « à mettre à jour », et
  la réécrire aurait mêlé les deux fins de ligne.

### 2. Les libellés écrits en dur — `150f25d`, 31 octobre

- `interactions.js` : une quarantaine de libellés français écrits en dur (compteurs accordés au nombre, bilans,
  en-tête replié, schéma à déposer, reprise de lecture), plus quatre que le cours avait laissés, passent par
  `ui-labels.js`. De même les derniers de `flashcards.js`, `accessibility.js` (« Aller au contenu ») et `playlist.js`.
- `media.js` : le lecteur de podcast, les diapositives, l'infographie, leurs fenêtres et le lecteur persistant ; ce
  qui ne se reconstruit pas suit la bascule de langue. Le défaut du registre sur ces fenêtres est réglé.
- Une capsule absente annonce « bientôt disponible » et ne promet sa transcription que si la page en donne une (le
  cours d'avant-projet) ; le nom du fichier attendu passe en infobulle.
- `ui-labels.js` : 68 clés de plus dans chaque langue, 182 en tout, appariées.

### 3. L'info-bulle du glossaire — `518df86`, 31 octobre

Les mécanismes du cours d'architecture logicielle, tels que le cours de veille les a repris :

- Sur ordinateur, la bulle se pose en position fixe sous son mot (au-dessus faute de place) et reste dans la
  fenêtre ; Échap l'écarte (WCAG 1.4.13). Sur téléphone et tablette, un bandeau au bas de l'écran, avec sa croix.
- En site miroir, une page `en/` cherche les termes par leur forme anglaise.
- Un mot du glossaire employé dans un autre sens porte la classe `hors-glossaire` : l'info-bulle et « Où en
  parle-t-on ? » le sautent.

Complété pour le gabarit : les `exclus` d'une entrée valent aussi sur les pages françaises (défaut resté ouvert dans
le cours) ; sur une page `data-tr`, un terme identique dans les deux langues ne prend plus sa bulle dans le bloc
masqué ; la recette du glossaire d'`ARCHITECTURE.md`, périmée, est réécrite.

### 4. Les erreurs 404 de la console — `0732822`, 1er novembre

L'auteur en a demandé la cause et le remède. `media.js` demandait au serveur chaque média possible d'un chapitre — le
podcast sous ses quatre noms, les diapositives, l'infographie, la fiche — et chaque absent laissait une erreur 404.
`outils/generer_medias.py` (nouveau) écrit `site/assets/js/media-data.js`, la liste des médias réellement déposés ;
`media.js` ne demande que ce qu'elle contient (sans elle, il sonde comme avant). `nouveau_cours.py` et
`generer_podcasts.py` la régénèrent, son `--essai` devient le neuvième contrôle du § 6 de `CLAUDE.md`. Le défaut du
registre sur les sondes de `media.js` est réglé.

### 5. Le polycopié — `9125f33`, 1er novembre

- **Le livret n'avait aucune espace insécable** : `NBSP` valait une espace ordinaire dans `rendu.py` et `pages.py`,
  le caractère U+00A0 s'étant perdu en route. Il s'écrit désormais par son échappement ; la typographie s'étend aux
  numéros, aux heures et aux unités, et à la page « 📘 Polycopié » du site.
- **Rien ne souffle une réponse sur le papier** (décision D41 du cours de veille) : une association mélange ses deux
  colonnes, sa clé ne se devine plus ; un scénario n'imprime que sa première étape ; les contrôles du livret suivent.
- La fiche du livret (`outils/livret.py`) reçoit la mention d'édition, la palette et le **site protégé** : ses QR
  codes se vérifient alors dans le dépôt, sans s'authentifier, et le livret dit où trouver ses accès ; un site qui
  refuse les robots s'ouvre par Chrome sans interface.
- Un tableau en tête d'encadré, sans ligne blanche au-dessus ; une table des matières resserrée ; le fragment
  `val-<clé>-lettres`, un chiffre du référentiel écrit en lettres.

### Comment ce travail a été vérifié

- Les contrôles du § 6 (huit, puis neuf), verts à chaque lot ; `node --check` des scripts et `py_compile` des
  modules modifiés ; fins de ligne gardées, aucun octet NUL.
- Au navigateur, les lots 1 à 3 et le correctif des 404 : en français et en anglais, à 1280 et 375 px, en clair et en
  sombre ; la console vide sur les trois chapitres, revérifiée dans des onglets neufs.
- Un cours créé par `nouveau_cours.py` dans un dossier temporaire, supprimé ensuite : sa liste des médias part vide,
  le scénario de `_modele.html` a ses trois boutons ; la console des chapitres est vide, sauf celle de
  `_modele.html`, où manque le schéma de la démonstration (au registre).
- Le livret : vingt-trois tests du lot 4 ; deux témoins comparés, avant et après — même texte, 216 espaces insécables
  au lieu de zéro, seul l'ordre des associations change ; un PDF témoin complet par Word : 15 pages, 0 écart,
  16 QR codes relus et cliquables.

### Pièges appris

- **Une espace insécable s'écrit par son échappement** (`"\u00a0"`), jamais en caractère : un éditeur, un copier-coller
  ou un outil de reprise la change en espace ordinaire sans que rien ne se voie.
- **Un script de correctif s'arrête sans rien écrire quand son ancre manque** : celle de `ui-labels.js` contenait une
  insécable, invisible à l'écran ; le script l'a dit au lieu d'écrire à côté.
- **Sous Windows, le dépôt est en CRLF** (`core.autocrlf`), les cours en LF : comparer avec
  `diff --strip-trailing-cr`, et qu'un générateur qui réécrit une page garde ses fins de ligne.
- **Une liste générée se périme** : `media-data.js`, comme `nav-sections.js`, a son `--essai` au § 6.
- **Le volet du navigateur intégré, masqué, ne défile pas et n'a pas le focus** : ce qui en dépend se vérifie
  autrement (un élément placé à des coordonnées choisies, un navigateur sans interface).
- **Un correctif copié d'un cours se relit ligne à ligne** : le cours de veille avait laissé quatre libellés en dur et
  n'appliquait pas `exclus.fr` ; le gabarit les a réglés au passage.

### Ce qui n'a pas été repris

Les nouveautés des deux cours — bloc « filières », illustrations, bouton « Copier », indice de longueur dans les
chapitres, page du glossaire, et pour le livret un glossaire réduit, des encadrés et des pages de notes… — sont au
registre, à décider avec l'auteur. Les exclusions plancher du déployeur du cours d'avant-projet sont sans objet dans
le gabarit.

---

## 26 octobre 2026 — un commit venu du cours de veille

- `d80a2ed` — fait depuis la session du cours de veille, avec l'accord de l'auteur : les chapitres n'ont plus ni
  barre d'étapes ni sommaire dans la page, leurs sections passent dans le menu de gauche, comme dans le cours
  d'architecture logicielle (`prompts/03_chapitre.md`, `GUIDE.md`, `RECETTE.md`, les trois chapitres).

---

## 25 et 26 octobre 2026 — le gabarit remis à niveau sur les cours de production

Le but : que le gabarit fournisse tout ce que le cours d'architecture logicielle
(`C:\projets\Cours\Cours_Architecture_Logicielle`, le cours de référence, en lecture seule) a construit en production,
en générique et bilingue, pour que chaque nouveau cours en parte. Vingt-huit commits, tous poussés ; aucune mise en
ligne (le gabarit ne se déploie jamais).

### 1. Sécurité et règles de production — 25 octobre

- `fb3b6f6` — `.rgignore` : l'outil de recherche ignore le `.gitignore` mais respecte ce fichier ; les secrets y sont
  listés, et `nouveau_cours.py` le recopie dans chaque cours. `deployer.py` n'affiche plus ni hôte, ni port, ni
  répertoire distant, ni empreinte. `outils/generer_nav_sections.py` (nouveau) écrit `nav-sections.js` d'après les
  `<h2 id>` des chapitres : un cours créé gardait les sections de la démonstration dans son menu.
- `e7a3f81` — `CLAUDE.md` § 2 reçoit les règles apprises en production : un exemple avant la série, les noms exacts
  des fichiers à déposer, le registre `TODO.md`, `git config` vérifié, les fautes de français proposées et jamais
  corrigées en silence, les limites de NotebookLM (4 800 caractères pour l'audio, 3 700 pour les diaporamas), l'essai
  à blanc avant tout envoi.
- `dacdb85` — licences MIT / CC BY 4.0 partout ; exemples neutres dans les prompts ; le panneau ♿ des pages du QCM
  réparé (`ui-labels.js` y manquait) ; `acces.exemple.json` ne porte plus l'adresse d'un cours réel.

### 2. Le prompt paramétrable : un tronc et neuf modules — 25 octobre

- `27fd5ff` — `prompts/PROMPT-Cours-parametrable.md` devient le tronc : un bloc de paramètres avec sa section
  `modules:`, dix règles, quinze phases et leurs jalons STOP, la définition de « terminé ». `prompts/modules/` a un
  fichier par option, chacun utilisable seul sur un cours existant : 01 bilingue, 02 polycopié, 03 podcasts
  NotebookLM, 04 audio, 05 évaluations, 06 TP, 07 Yparéo et Livrables, 08 déploiement, 09 compléments.

### 3. Le bilingue tranché — 25 octobre

- `09991da` — **Décision de l'auteur** : un cours bilingue se fait en **site miroir** (une page anglaise jumelle de
  chaque page, sous `en/`, écrite une fois le français stable) ; les blocs `data-tr` restent le **modèle de secours**,
  pour un cours court écrit bilingue d'emblée. `docs/I18N.md` réécrit (partie A miroir, partie B `data-tr`) ;
  `cours.exemple.json` part de `langues: ["fr"]`. La démonstration du gabarit reste en blocs `data-tr`.
- `b63ac8c`, `c0a0280`, `3fe888f` — les outils du site miroir : `langue.js` (le bouton FR / EN ouvre la jumelle et s'y
  replace sur le bloc lu), `langues-data.js` et `generer_langues.py`, `creer_jumelle.py`, `data_tr_vers_miroir.py`
  (refuse de tourner dans le gabarit), `miroir.py`, `liens_langues.py`, `hreflang.py`, `verifier_parite.py` ;
  `i18n.js` calcule la racine du site (`TPL_RACINE`). Les intitulés d'étapes et de sommaire, des attributs, ont leur
  version anglaise (`data-step-titre-en`, `data-sommaire-titre-en`).

### 4. Les outils de contrôle et de cohérence — 25 octobre

- `8d3b003` — **les interdits** : `outils/interdits.py` (vide dans le gabarit, rempli dès le cadrage) et
  `outils/verifier_interdits.py`, qui cherche les mots, nombres et motifs interdits hors de leur place.
- `6322c02`, `4475561`, `03e61ba` — **le référentiel et ses fragments** : `outils/referentiel.py`, source unique des
  chiffres du cours, et `outils/generer_fragments.py`, qui réécrit le contenu entre les marqueurs
  `<!-- FRAGMENT:nom -->` dans la langue de la page ou du bloc. Le sommaire de la démonstration annonçait cinq
  chapitres pour trois : il affiche désormais, calculés, « 3 chapitres · ~1 h 20 » (correction validée par l'auteur).
- `3a0a019`, `00b245e` — **« Où en parle-t-on ? »** : `outils/glossaire_emplois.py` compte où le cours emploie chaque
  terme du glossaire et écrit `glossaire-emplois.js` ; chaque terme a son ancre (`#g-…`) et l'info-bulle y mène.

### 5. La page Podcasts — 25 octobre

- `dab3026`, `5d68f5e`, `42c2a37` — `outils/podcasts.py` (la source des épisodes, dans les deux langues),
  `outils/generer_podcasts.py` (les dépôts de `Podcasts/`, jamais versionnés, en MP3 mono à 64 kbit/s et diapositives
  WebP), la page `site/podcasts.html`, sa visionneuse (`podcasts.js`), l'encadré « Le podcast du chapitre »
  (fragment `podcast-N`). Bloc `podcasts` de `nouveau_cours.py`, inactif par défaut. La démonstration a un épisode.
- `299c203` — le bouton ♿ était annoncé aux lecteurs d'écran par la chaîne brute « ' + T('a11y.titre') + ' » ; son
  libellé vient de `ui-labels.js`.

### 6. Le polycopié — 26 octobre

- `797e08a` — la chaîne du polycopié : tout le cours en un livret A4, Word puis PDF par Word, tiré des pages du site
  (page de garde, mentions, présentation de l'auteur, mini-sommaires, schémas expliqués, activités devenues exercices
  sur papier, glossaire, index ; dans la marge, des QR codes cliquables ; aucune réponse imprimée).
  `outils/generer_polycopie.py` et le paquet `outils/polycopie/` (quatorze modules), la fiche `outils/livret.py`,
  `outils/publier_polycopie.py` (contrôle, publication dans `site/livret/`, vignette, `livret.json`), la page
  `site/polycopie.html` et ses fragments `livret-couverture`, `livret-fiche`, `livret-auteur`. L'enregistreur
  ajouté à `interactions.js` garde la configuration des composants RDCX, que Chrome sans interface lit.
  - **Décisions de l'auteur** : le témoin d'abord, validé avant le livret complet ; le livret devient un bloc à part,
    « livret », et sa page « 📘 Polycopié » ouvre les ressources du menu ; les polycopiés par chapitre restent,
    sous le nom « 📄 Fiches de synthèse ».
  - Le livret de démonstration est publié : 23 pages en français, 23 en anglais, 31 et 29 QR codes, relus et
    cliquables, 0 anomalie. Ses QR codes portent `https://example.org/cours/`, un domaine réservé aux exemples (RFC
    2606) — d'abord `exemple.org`, qui ne l'est pas.
  - Les pastilles numérotées d'un schéma à zones se posent dans le blanc le plus proche de leur point, avec une
    marge d'un demi-rayon ; des titres de zones numérotés (« 1. Le public ») évitent les pastilles.
  - Une image pas encore produite est signalée (« schéma absent », « image absente ») au lieu de faire échouer la
    génération ; sans glossaire, la page du polycopié s'écrit, le livret refuse de se composer.
- `31fb7d1` — le bloc `livret` de `nouveau_cours.py` : inactif par défaut, il demande le bloc `glossaire` ; la fiche
  du livret part vide (l'auteur y écrit sa présentation), le livret de démonstration est retiré.
- `4443c55` — la documentation : module 02 (ce que la chaîne fournit, comment étendre son vocabulaire, ce que le
  cours de référence montre en plus), `CLAUDE.md`, `ARCHITECTURE.md`, `CHECKLIST.md`, les README, le prompt et la
  skill des supports imprimables.

### 7. Les correctifs qui ont suivi — 26 octobre

Chacun validé par l'auteur, dans son commit :

- `6d413b1` — sans le bloc « polycopies », `site/polycopies.html` restait orpheline : elle part avec son bloc.
- `2376eef` — le prompt et le module 03 rangent « 📘 Polycopié » et « 🎙️ Podcasts » dans les ressources du menu,
  comme le gabarit (le cours de référence les met juste après « Accueil du cours »).
- `508464c`, `c61f256` — la page des fiches et le bouton des chapitres disent « Fiche(s) de synthèse » /
  « Summary sheet(s) » : « Polycopié » ne désigne plus que le livret complet.
- `eca5d61` — la page des fiches renvoie au polycopié pour ce que le papier reprend ; ce renvoi est encadré de
  `<!-- livret:debut -->` … `<!-- livret:fin -->`, que `nouveau_cours.py` retire d'un cours sans livret.
- `c81717f` — le sous-titre du cours, destiné à l'accueil, remplaçait celui de **toutes** les pages d'un cours créé
  (chapitres, ressources, sommaire et son fragment). Il ne va plus qu'à l'accueil ; les squelettes de chapitre et les
  pages vidées reçoivent un « À rédiger », le glossaire une phrase générique.
- `28b19c8` — la fenêtre de la fiche de synthèse parle la langue de la page (clés `media.fiche`, `media.chapitre`,
  `media.ouvrir`, `media.fermer`) et ne s'empile plus à chaque changement de langue.

### Comment ce travail a été vérifié

- Les contrôles de `CLAUDE.md` § 6, verts à chaque commit : `verifier_i18n.py`, `verifier_contraste.py`,
  `verifier_liens.py`, `generer_nav_sections.py --essai`, `verifier_interdits.py`, `generer_fragments.py --essai`,
  `glossaire_emplois.py --essai`, `podcasts.py`, `publier_polycopie.py --essai` ; `node --check` des scripts
  modifiés ; aucun octet NUL.
- `nouveau_cours.py` essayé sur des cours créés en français seul, en bilingue, sans livret, sans fiches, et sur un
  livret sans glossaire (refusé), puis converti en site miroir ; un livret publié simulé ; la chaîne du polycopié
  lancée dans un cours créé. **Chaque cours d'essai a été supprimé aussitôt** : il contient des copies des secrets.
- Au navigateur : la page du polycopié en français et en anglais, à 375 px, en clair et en sombre ; la fenêtre de la
  fiche en deux langues ; chaque erreur de console revérifiée dans un onglet neuf.

### Pièges appris

- **`docs/` part dans chaque cours** : ce qui ne concerne que le gabarit va à la racine (ce journal, `TODO.md`) ou
  entre `<!-- gabarit:debut -->` et `<!-- gabarit:fin -->`.
- **Un passage qui dépend d'un bloc facultatif** doit pouvoir partir avec lui : des repères (`livret:debut`) ou un
  fichier listé dans `BLOCS`.
- **Une adresse d'exemple** est sur `example.org`, `example.com` ou `example.net`, jamais sur un domaine qui peut
  appartenir à quelqu'un.
- **La console d'un onglet garde les messages de ses visites précédentes** : une erreur se revérifie dans un onglet
  neuf avant d'être crue.
- **Un correctif scripté s'écrit dans un fichier `.py`**, pas dans un document « heredoc » du terminal, qui peut
  altérer les barres obliques inverses.
- Le serveur local sert les WebP en `application/octet-stream` sous Windows : sans effet, les navigateurs les
  affichent.

### Le cours de référence

Lu, jamais modifié ni importé. Deux commentaires de sa chaîne du polycopié ne disent pas ce que fait le code
(`ooxml.py` : `relativeFrom="paragraph"` pour `line` ; `controles.textes_docx` dit exclure le texte des champs et le
garde) : corrigés dans la copie du gabarit, notés dans le registre du cours pour y être corrigés.
