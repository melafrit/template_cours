# Journal du gabarit

> Ce qui a été fait sur le gabarit, session par session, avec ses commits. Ce qui reste à faire est dans
> [`TODO.md`](TODO.md), le registre, à lire en premier à la reprise du travail. Les deux fichiers, à la racine, ne
> partent jamais dans un cours créé : `nouveau_cours.py` ne recopie de la racine que ce que liste `COPIER` — alors que
> tout `docs/` part dans chaque cours.
>
> « Décision de l'auteur » signale un choix tranché par l'auteur ; le reste découle des règles de `CLAUDE.md` (§ 2).

---

## 23 novembre 2026 · trois relevés, puis le code sans tirets (`7ac54ec` à `ed03a7e`)

### Les décisions prises sous le mode « enchaîne » (options recommandées)

- Après le lot des outils à trois langues, les relevés du registre qui ne demandent pas l'auteur passent d'abord :
  les capsules de l'accueil pour le générateur, la page courante du menu, les pluriels du glossaire.
- Les pluriels du glossaire entrent dans la liste curatée, comme le documentait déjà le moteur, plutôt que de
  changer la recherche des info-bulles.
- Les tirets du code : les chaînes à la main, puis les commentaires et docstrings par quatre agents, après un
  témoin (`tools.js`), sur une consigne écrite reprise du lot des documents. Les tirets que le code cherche ou
  traite restent.
- Le schéma de la démo n'est pas régénéré (un schéma validé ne se rend pas de nouveau sur un autre poste) ; les MP3
  des podcasts ne sont pas refaits.

### Le travail

- `generer_audio.py` (`7ac54ec`) lit les capsules que l'accueil déclare dans une liste : 18 pistes, 19 317
  caractères, chacune avec son script.
- `navigation.js` (`6301cfc`) pose `aria-current="page"` sur le lien de la page courante (chapitres, ressources,
  accueil, jumelles comprises).
- `glossaire-data.js` (`8808d11`) : quatre pluriels dans `GLOSSARY_CURATED`, l'alias qui se nommait lui-même retiré,
  des commentaires exacts (les données, le squelette d'un cours créé, la skill, ARCHITECTURE). Rien ne change à
  l'écran dans la démo, dont les chapitres n'emploient ces pluriels que dans un composant.
- Les chaînes du code (`69f3230`) : messages du déployeur et des outils, en-têtes des cinq fichiers générés
  (régénérés), titre de la série de podcasts, marque « À TRADUIRE » (reconnue par son début, l'ancienne forme
  comprise), sous-titres du schéma, commentaire du modèle de `config.json`.
- Les commentaires et docstrings (`ed03a7e`) : 269 lignes dans 65 fichiers ; le message du commit dit 64, en
  oubliant le témoin.

### Ce qui a été vérifié

L'essai à blanc du générateur de pistes (les 18 capsules, l'accent sur les seules pistes françaises) ; le menu sur
un chapitre, une ressource, l'accueil et les jumelles anglaise et arabe ; les info-bulles des chapitres ; les
en-têtes régénérés, sans autre écart ; le test du déployeur ; `generer_podcasts.py --essai`, sans republication.
Pour les commentaires, le contrôle automatique de chaque mission (une seule erreur, un faux positif de mon balayeur
sur `qcm-core.js`, vérifié à la main), puis la compilation de tout le Python, `node --check` sur tout le
JavaScript, tous les contrôles du § 6, et la console vide sur l'accueil, un chapitre, le QCM et les activités.

### Ce qui n'est pas fait

Le schéma 1 du chapitre 1 et les MP3 des podcasts gardent leur tiret ; les relevés des agents (accents manquants,
passages périmés, tournures, antithèses) attendent l'auteur. Tout est au registre.

---

## 23 novembre 2026 · les outils à trois langues (`7a9c964` à `11e4b42`)

### Les décisions prises sous le mode « enchaîne » (options recommandées)

- Une piste arabe ne part jamais avec le clone français ni avec l'accent parisien : sans voix déclarée
  (`voix_id_ar`), `generer_audio.py` la laisse en attente. La voix et l'accent de l'arabe restent à décider avec
  l'auteur (module 01, section 4).
- Seules les langues du site comptent comme suffixe d'une piste : « -tp.mp3 » reste une piste française.
- Les liens hreflang sont posés dans les pages de la démo, puisque son adresse publique est connue (elle figure
  déjà au registre) ; un cours créé les perd à sa création et pose les siens sous son adresse.
- Les mots arabes des activités sont ceux des autres moteurs ; ceux qui manquaient au lexique y entrent, à relire
  avec le témoin arabe.
- `xlsx.full.min.js` n'est pas téléchargé : un téléchargement demande l'accord explicite de l'auteur, que le mode
  « enchaîne » ne donne pas.

### Le travail

- `generer_playlist.py` (`7a9c964`) lit les jumelles de `en/` et `ar/` ; la capsule arabe du chapitre 1 entre dans
  la liste de lecture, « à venir ». Sa constante remonte après les imports, et il ne reconnaît plus que les langues
  du site (`274e79d`).
- La chaîne audio (`274e79d`) : `synchroniser_capsules.py` écrit dans la jumelle de `ar/chapitres/` ;
  `generer_audio.py` parcourt `ar/`, reconnaît la langue d'après les clés d'`ACCENTS` et tient la liste des pistes
  en attente de leur voix ; la fiche des capsules reçoit la capsule 7 AR (la transcription de la page, sans
  script) ; `elevenlabs.exemple.json` documente `voix_id_ar` et perd ses six tirets, comme deux messages d'outils.
- `hreflang.py` (`77873d8`) suit la langue racine et les dossiers de langue : 16 groupes, 33 pages (fr 16, en 16,
  ar 1). `nouveau_cours.py` retire ces blocs de chaque page d'un cours créé.
- `tools.js` (`9298ec2`) prend ses libellés dans `ui-labels.js` (`activite.*`, trois langues) ; le score final et
  les guillemets suivent la typographie de chaque langue (“…” et « Score: » en anglais).
- `nouveau_cours.py` (`376208a`) demande les titres de la langue racine ; `texte()` retombe sur le français, puis
  sur la première langue présente. Le test a trouvé en chemin une variable locale qui masquait `texte()`, renommée.
- `cours.exemple.json` (`11e4b42`) : sept tirets, et le commentaire de « public », qui le disait affiché.

### Ce qui a été vérifié

`synchroniser_capsules.py --essai` lit la capsule arabe et laisse la page arabe à jour ; un essai sur une copie
montre qu'une retouche de la fiche n'atteint que la jumelle arabe, fins de ligne gardées, et qu'une seconde passe
ne change rien. `generer_audio.py --essai` signale la piste arabe sans script ; sur une copie, avec une
configuration factice, elle attend sa voix, puis part sans accent ajouté quand la voix est déclarée, et les pistes
françaises gardent l'accent parisien. `hreflang.py` pose 33 blocs, puis ne trouve plus rien à faire. Cinq essais
de création de cours, supprimés ensuite : racines française et anglaise sans aucun bloc ni adresse de la démo ;
racine anglaise sans titre français acceptée et titrée en anglais ; racine française inchangée ; racine anglaise
sans titre anglais refusée, la clé nommée. La page des activités, en français et en anglais (et l'arabe simulé),
console vide dans un onglet neuf, capture à 375 px en thème sombre. Tous les contrôles du § 6 sont verts, et le
générateur de prompt passe ses cinq cas.

### Ce qui n'est pas fait

Le téléchargement de `xlsx.full.min.js` (accord de l'auteur) ; les commentaires à tirets des outils (94 lignes)
et du site (145 lignes), au registre. Juste après ce lot, préalable au lot 9 : `generer_audio.py` voit les
dix-huit capsules de l'accueil, déclarées dans une liste (`src: V + '…'`) qu'il ne lisait pas ; son essai à
blanc les compte (18 pistes, 19 317 caractères), chacune avec son script, l'accent parisien sur les seules
pistes françaises.

---

## 23 novembre 2026 · les derniers relevés des documents (`09f459a`, `2370e9c`)

### Les décisions prises sous le mode « enchaîne » (options recommandées)

- Les messages des outils suivent la règle des messages à l'auteur : plus de tiret.
- La feuille « Mode d'emploi » des questions d'oral devient générique, sans rien inventer.
- Les transcriptions des deux podcasts de la fiche des capsules prennent le deux-points de leur phrase voisine
  (l'exception du 5 novembre : la ponctuation d'une transcription peut changer, ses mots non).

### Le travail

- 36 tirets dans les messages de 19 outils, de `demarrer.py` au déployeur (`09f459a`). L'état d'un générateur
  s'écrit « …, à jour », comme `generer_filieres.py` le faisait déjà ; une durée absente devient « n.d. » ; un titre
  d'épisode prend « · ». Aucun outil ni aucun test ne lit ces messages : vérifié avant.
- `docs/generate_questions_oral.py` (`2370e9c`) : le choix des questions passe par la colonne Thème, la notation par
  la ligne de grille que vise chaque question ; plus de « phase 3 », de « questions 13 ou 14 », de « dossier PIA », de
  « chapitre 8 » ni de page « Soutenance vidéo ». L'antithèse d'un exemple et le commentaire en double partent aussi.
- La fiche des capsules (`f305154`) : « Le public d'abord : tant qu'on ignore… », « The audience first: until… ».

### Ce qui a été vérifié

Les outils touchés tournent et compilent (`generer_medias.py`, `generer_nav_sections.py`, `generer_langues.py`,
`glossaire_emplois.py`, `verifier_parite.py`, `verifier_i18n.py`, `verifier_interdits.py`, `synchroniser_capsules.py`,
`generer_fragments.py`, `podcasts.py`, `hreflang.py`) ; le test du déployeur passe (« Tous les cas sont conformes »).
Le script de l'oral, lancé vers le dossier temporaire, produit un classeur sans aucune trace de l'autre cours ni
tiret ; le fichier d'essai a été supprimé. La fiche des capsules se relit toujours.

### Ce qui n'est pas fait

Les autres marques de texte généré (au registre), les commentaires de `nouveau_cours.py`, les lignes 23 et 24 de la
fiche des capsules.

---

## 23 novembre 2026 · les documents à jour et sans tirets (`7b8a1ef`, `d3eeddc`)

### Les décisions de l'auteur

- **Les documents, à jour et sans tirets**, témoin d'abord : `CLAUDE.md`, validé (22 novembre), puis la série par
  cinq agents, contrôlée.
- **« Enchaîne sans me demander de valider »** (22 novembre au soir) : à chaque décision, l'option recommandée est
  retenue et annoncée, les commits partent sans question, jusqu'à ce que l'auteur redemande des questions. Les règles
  de sûreté de `CLAUDE.md` restent (secrets, purge, authentification).

### Les décisions prises sous ce mode (options recommandées)

- Les textes que `nouveau_cours.py` écrit dans un cours (valeurs d'exemple des squelettes de chapitre, en-têtes des
  fichiers de données) sans tiret (`b7ced50`), puis leurs accents et apostrophes, à part (`094d453`).
- Les passages périmés repris (`d3eeddc`), puis les fautes relevées par les agents, à part (`782131c`).
- La recette suit la sortie réelle du générateur : 21 médias retirés, depuis que les DOCX des fiches ont quitté le
  site (`a88811e`).

### Le travail

- `CLAUDE.md` (29 tirets), l'en-tête que `nouveau_cours.py` écrit dans le `CLAUDE.md` d'un cours.
- `docs/` (GUIDE, CHECKLIST, I18N, ARCHITECTURE, RECETTE, BONNES_PRATIQUES, le script des questions d'oral, les
  exemples JSON), `deploiement/destination.exemple.json`, les neuf fichiers des skills, les textes et messages de
  `nouveau_cours.py` : environ 390 tirets, chacun remplacé par la ponctuation que le sens demande. Les cinq agents
  avaient une consigne écrite complète (style du témoin, exceptions, interdits, méthode, rapport) ; le contrôle
  automatique comparait chaque fichier à sa version commitée (nombre de lignes, lignes touchées, mots inchangés hors
  ponctuation, fins de ligne, blocs enregistrés de la fiche des capsules, compilation, en-têtes YAML) ; chaque
  changement a été relu.
- Les squelettes que reçoit un cours créé : le bloc TEXTES des chapitres, les fiches de synthèse, le QCM, les
  flashcards, le glossaire, dont le français était écrit sans accents (« Question posee », « Polycopie de
  synthese », « terme a definir ») ; cinq messages de la création aussi.
- Les passages périmés : le GUIDE (cadrage, options cliquables, site miroir, seize prompts, atelier, bouton des
  langues), ARCHITECTURE (site miroir, arborescence réelle, `quiz.js`, API de `i18n.js`), BONNES_PRATIQUES, le
  prompt 11, les skills (ordre du tronc, glossaire, six mécanismes), la CHECKLIST (ordre des phases, vouvoiement).

### Ce qui a été vérifié

Le contrôle automatique passe ; ses alertes, relues, étaient sans gravité. `verifier_tirets.py` reste vert sur le
gabarit. Un cours d'essai, généré dans le dossier temporaire avec une configuration à part (le `cours.json` du cours
MOE n'a pas été touché) : aucun tiret dans ses 45 fichiers publiés, ni dans son `CLAUDE.md` (« # Titre du cours ·
contrat de travail ») ni dans `DEMARRER-ICI.md` ; ses squelettes accentués ; `verifier_i18n.py`, `verifier_liens.py`,
`verifier_parite.py` passent ; puis le cours d'essai, qui portait une copie locale des secrets, a été supprimé. La
fiche des capsules se relit toujours (`synchroniser_capsules.py --essai`, `generer_audio.py --essai`). Les en-têtes
YAML des skills se relisent, et Claude Code les a rechargés.

### Ce qui n'est pas fait

Les autres marques de texte généré relevées (antithèses, phrases sans verbe, mots gonflés), la feuille « Mode
d'emploi » du script des questions d'oral, venue d'un autre cours, les messages des outils à tirets, les deux
transcriptions de podcast de la fiche des capsules : tous au registre.

### Pièges appris

- **Un texte d'exemple que le générateur écrit part dans chaque cours** : un tiret ou une faute y devient celui de
  tous les cours créés, et `verifier_tirets.py`, qui ne lit que le `site/` du gabarit, ne le voit pas. Seul un cours
  d'essai le montre.
- **Un compte attendu dans la recette suit le gabarit** : six DOCX sortis du site ont fait passer « 27 médias » à 21
  sans qu'aucun contrôle le signale. La génération l'a montré.
- **Un message changé ici et cité là** : deux agents en parallèle, l'un sur `nouveau_cours.py`, l'autre sur la
  recette qui cite sa sortie ; la citation se recale après coup, sur la vraie sortie.
- **Un « : » dans l'en-tête YAML d'une skill** casse sa description : dans l'en-tête, un tiret devient une virgule,
  des parenthèses ou « · ».

---

## 22 novembre 2026 · lot S4, le QCM sans tirets (`1df056e`)

### Les décisions de l'auteur

- **Le lot S4, témoin d'abord** : la page d'examen du QCM, en français et sa jumelle anglaise, et l'explication de
  Q01, alignée sur la phrase validée du chapitre 1 ; puis la série sur les 61 tirets restants.
- **Les cases vides prennent un mot** : « aucune » ou « none » pour une certitude absente, « n.d. » ou « n/a » pour une
  durée ; un lecteur d'écran le lit mieux qu'un tiret.
- **La faute « encouragez à assumer »**, relevée en chemin : « encouragez-les à assumer », dans un commit à part
  (`0b18516`).

### Le travail

- Les pages d'examen, de correction, du tableau de bord et d'entraînement, et leurs jumelles : « · » dans les titres,
  descriptions et bandeaux d'auteur ; le deux-points dans les titres de carte et les messages de signature. Les deux
  dictionnaires de chaque page vivent dans chacune des jumelles : chaque passage s'y applique deux fois.
- Le tableau de bord reçoit deux clés, `noCert` et `noDur`, en français et en anglais, au lieu d'un tiret écrit en dur.
- La banque : son titre, la question sur la durée de conservation (« (quinze minutes) », comme au chapitre 3), dix
  explications au deux-points ou à la virgule, alignées sur les chapitres quand la phrase y existe.
- `qcm-core.js` (la stratégie du barème), deux flashcards (lot S5, qui rejoignent la virgule de leur version arabe),
  le squelette du QCM de `nouveau_cours.py` (« QCM · titre »).

### Ce qui a été vérifié

`verifier_tirets.py` est vert pour la première fois : aucun tiret dans `site/` (91 au début du lot). Les contrôles du
projet passent (i18n, parité, liens, glossaire, fragments, médias) ; les données du QCM se relisent. Au navigateur,
avec des copies signées par le vrai moteur et déposées sur les pages : la correction (« Signature valide : fichier
authentique », « Certitude : aucune », « Certainty: none »), le tableau de bord (« n.d. », « n/a », l'info-bulle
« Q01 · 100% de réussite (1/1) », le détail d'une copie) ; les pages d'examen et d'entraînement ; la console vide dans
un onglet neuf ; 375 px sans débordement, thème sombre.

### Ce qui n'est pas fait

`CLAUDE.md` (29 tirets) et `docs/` (260 dans 11 fichiers) gardent les leurs. Les commentaires du code aussi, que
personne ne lit sur le site.

### Pièges appris

- **Une jumelle garde les deux dictionnaires** : la page anglaise porte encore le français, et inversement ; un même
  libellé se corrige deux fois par page, dans le bon ordre quand la chaîne est identique (`noCert: '—'`).
- **Un tiret écrit en dur dans un moteur** échappe au dictionnaire : il devient une clé, pour se traduire.

---

## 22 novembre 2026 · lot 7, les quatre points tranchés (`ab70c18`)

### Les décisions de l'auteur

- **Le prompt 08 sert le script du gabarit** (`tools/generate_qcm_papier.py`) au lieu d'en faire écrire un autre,
  qui l'aurait écrasé. Une épreuve à banque privée suit le module 05, sur le modèle du cours CDWFS.
- **Le prompt 06b s'aligne sur le gabarit**, sa liste dépliable ; la fenêtre du cours d'architecture logicielle
  reste décrite comme référence, et son portage va au lot 6.
- **Les fiches de synthèse** : tous leurs tirets corrigés, témoin d'abord (la fiche du chapitre 1, validée) ; leurs
  DOCX ne se publient plus ; la correspondance des huit blocs du prompt 12 avec les six types du script est validée
  telle quelle.
- **La signature du QCM** : les mises en garde corrigées d'après l'essai.
- **Le lien de la page anglaise des fiches**, relevé en chemin, corrigé avant le commit.

### Le travail

- `prompts/08_qcm_papier.md` réécrit : le contrôle de la banque, les consignes imprimées comparées au règlement, la
  génération par le script, la checklist ; une étape 0 renvoie une épreuve à banque privée au module 05. Le module
  05, le GUIDE et le sommaire des prompts suivent. Les libellés de `tools/generate_qcm_papier.py` passent au point
  médian, aux parenthèses ou au deux-points.
- `prompts/06b_glossaire_ou_en_parle_t_on.md` réécrit : il fait adapter le mécanisme du gabarit par ses données
  (`alias`, `exclus`, `EXCLUES`, `hors-glossaire`). La docstring de `glossaire_emplois.py` dit l'arabe, que le code
  traitait déjà.
- `tools/generate_polycopies.py` et `tools/polycopies_content.json` sans tiret ; les DOCX écrits dans `tools/out/`,
  les six retirés du dépôt ; `generer_medias.py` ne liste plus que les PDF. La page Polycopiés (français et anglais),
  ARCHITECTURE, le prompt 12, `tools/README.md` et la skill des supports imprimables suivent ; ces deux derniers se
  trompaient déjà de dossier.
- Les mises en garde sur la signature : la skill `cours-qcm-cbm` (§ 6), ARCHITECTURE (§ 4.3), la skill bilingue
  (`data-shapes.md`) et la note du lot S4.
- `site/en/polycopies.html` cherche ses PDF dans `../assets/polycopies/`.

### Ce qui a été vérifié

L'essai de la signature, sur le vrai moteur et la vraie banque de la démo, avec une copie parfaite : telle quelle,
valide et 20/20 ; falsifiée, rejetée ; énoncé reformulé et banque réordonnée, valide et 20/20 ; une bonne réponse
changée, valide et 15,56 ; une question ajoutée, valide et 18 ; une question retirée, valide et 17,5. Les fiches
régénérées : aucun tiret dans les six PDF ni dans les six DOCX, la langue déclarée juste (`/Lang`), une page chacune.
Le script du QCM papier régénère ses six fichiers. Les contrôles du projet passent (i18n, liens, parité, médias,
glossaire, fragments, menus, langues) ; `verifier_tirets.py` garde les 91 tirets connus du lot S4. Au navigateur :
les deux pages Polycopiés, leur phrase, leurs liens (200), la console vide dans un onglet neuf ; le bouton du
chapitre 1, en français et en anglais.

### Ce qui n'est pas fait

Les tirets que la banque de la démo garde (son titre, des explications) passent encore dans le QCM papier (lot S4).
Les six DOCX restent en ligne jusqu'à une purge, avec l'accord de l'auteur. Le mot coupé des fiches en PDF
(« contrainte » puis « s matérielles ») est relevé, pas corrigé. Le cours MOE, créé avant ces points, a les anciennes
versions.

### Pièges appris

- **Une mise en garde se vérifie par un essai** : celle de la signature disait le contraire du code, et freinait à
  tort le lot S4.
- **Un chemin construit par morceaux dans un script échappe à la conversion en site miroir** : `outils/miroir.py` ne
  réécrit que les chaînes d'un seul tenant, terminées par une extension. La page anglaise des fiches cherchait ses
  PDF dans `en/assets/`.
- **`git rm` refuse un fichier modifié** : une régénération avait touché les DOCX, refaits ailleurs ; d'où
  `git rm -f`.

---

## 22 novembre 2026 · le générateur après son premier usage (`bba8c23`)

### Les décisions de l'auteur

- **Le prompt complet du cours MOE**, demandé d'après le premier prompt sorti de la page : corrigé à la main et
  livré (chemins relatifs, FM02 et Bloc 4, promotion à demander, consignes en prose, deux secrets nommés, Jour 1 au
  23 novembre 2026).
- **Corriger le générateur** d'après ce premier usage, témoin d'abord.

### Les défauts relevés

Le prompt que l'auteur a obtenu de la page portait cinq défauts. Ses chemins étaient absolus, à antislashs. Ses
consignes sur le fil rouge et le TP étaient tombées dans des valeurs du YAML. La règle des secrets se limitait aux
`.json`, alors qu'un fichier de mot de passe se trouvait parmi les documents. La promotion « 2027 » n'est pas un nom
que l'application Livrables reconnaît. Le cours disait « M02 » et ses filières « FM02 », avec « Bloc 04 » contre
« Bloc 4 ».

### Le travail

- `generateur/generateur.js` : les chemins nettoyés (barres obliques, guillemets ôtés) et relatifs au dossier du
  cours ; le dossier de base seul dit « à préciser » ; `verifications()`, une fonction pure, relève les points à
  vérifier, chacun avec son texte pour la page et, s'il demande une décision, sa consigne pour le prompt ; les
  consignes de l'auteur sous « Ce que l'auteur a précisé », retours à la ligne gardés ; les secrets nommés ; la règle
  des fichiers de configuration et de mot de passe, pour un dossier préparé comme pour `sources/`.
- `index.html` et `page.js` : les champs des consignes (fil rouge, TP, autres), du projet fil rouge par filière et des
  secrets ; l'encadré « À vérifier » au-dessus du prompt ; le prompt replié à la largeur de sa zone ; un brouillon
  d'une version plus ancienne complété au chargement.
- `essai_generateur.js` : cinq cas au lieu de trois, dont la saisie du premier usage et un Jour 1 lointain.
- `generateur/LISEZMOI.md` : les consignes, les chemins, les points à vérifier.

### Ce qui a été vérifié

Le contrôle passe (cinq cas). Sept défauts introduits exprès dans une copie du moteur sont tous attrapés. Le témoin,
la saisie de l'auteur rangée dans les nouveaux champs, redonne le prompt corrigé à la main, à une différence près :
« M02 » n'est plus remplacé en silence, le prompt fait demander lequel garder. Telle que l'auteur l'avait tapée, la
saisie déclenche six signalements. Au navigateur, la saisie a été refaite champ par champ ; la console reste vide, en
clair et en sombre, à 1280 et 375 px sans débordement. Le brouillon déjà présent dans l'onglet a été mis de côté,
puis remis.

### Ce qui n'est pas fait

Les boutons Copier et Télécharger, inchangés, n'ont pas été retestés. Le générateur ne reformule pas les libellés de
l'auteur (les simulateurs restent tels que saisis). Les deux secrets du cours MOE restent à retirer de ses documents
par l'auteur.

### Pièges appris

- **Une consigne dans un champ court devient une donnée** : dans le YAML, Claude la lit comme une valeur, et ses
  chemins à antislashs s'y doublent. La page sépare les deux et signale une phrase restée dans un champ court.
- **« Copier en tant que chemin » met des guillemets** : Windows les interdit dans un nom de fichier, un champ de
  chemin peut donc les perdre sans risque.
- **Corriger en silence, c'est trancher à la place de l'auteur** : « M02 » contre « FM02 » peut être une faute de
  frappe ou un choix. Le prompt pose la question au lieu de choisir.

---

## 22 novembre 2026 · lot 8, le générateur de prompt (`632e9b8`)

### Les décisions de l'auteur

- **La page produit le prompt de lancement** : il renvoie au tronc et aux modules actifs par leur chemin, avec le
  bloc de paramètres rempli ; Claude écrit `cours.json` à l'étape zéro.
- **Les valeurs habituelles préremplies** : identité et Git, hébergement, écosystème, filières et habitudes.
- **Un dossier déjà préparé garde ses documents** : le formulaire demande leur dossier (`Doc_Reference` par défaut),
  que le prompt fait exclure de Git et des recherches. L'exemple de l'auteur : son prochain cours,
  `Cours_CDWFS_ASRC_Gestion_de_Projet_MOE`.
- **Le témoin validé** avant la série.

### Le travail

- `generateur/index.html` et `page.js` : le formulaire, le prompt refait à chaque saisie, la copie, le
  téléchargement, le brouillon gardé dans le navigateur, l'enregistrement des valeurs habituelles (un fichier
  téléchargé, puisque la page ne peut pas écrire dans son dossier).
- `generateur/generateur.js` : la fabrication du prompt, une fonction pure ; `valeurs.exemple.js`, versionné ;
  `valeurs.local.js`, préparé pour l'auteur et ignoré par Git ; `essai_generateur.js`, le contrôle.
- `CLAUDE.md` (sections réservées au gabarit), le GUIDE, le README des prompts et le mode d'emploi du tronc le
  documentent.

### Ce qui a été vérifié

Le contrôle passe (trois cas : un dossier préparé avec deux filières et Codex, un dossier neuf avec une jumelle, des
valeurs absentes). Au navigateur : les valeurs chargées, les filières proposées (paires et filières seules), le
prompt refait et copié, la console vide, en clair et en sombre, à 1280 et 375 px. Les données des filières CDWFS et
ASRC viennent du cours d'étude d'avant-projet CDWFS/ASRC (intitulés et RNCP).

### Ce qui n'est pas fait

Le premier usage réel, sur le cours de gestion de projet (MOE). Le secret trouvé dans ses documents, à retirer par
l'auteur.

### Pièges appris

- **Avant sa création, un cours n'a pas de `.rgignore`** : une recherche dans un dossier préparé pourrait lire un
  secret posé parmi les documents. Le prompt interdit toute recherche tant que les documents ne sont pas exclus.
- **Un clic de test se trompe de bouton** : un premier essai a téléchargé le prompt au lieu de le copier. Les boutons
  d'une page se visent par leur référence, pas par des coordonnées.

---

## 22 novembre 2026 · lot 7 terminé, les prompts numérotés (`da73639`)

### Les décisions de l'auteur

- **Le prompt 03 en témoin**, validé avant la série.
- **Les prompts avant le générateur**, puis, à sa question sur le générateur de prompt, **son cadrage dès maintenant**
  pendant que les agents finissaient. Première réponse : la page produit le prompt de lancement, qui renvoie au tronc
  et aux modules par leur chemin, avec le bloc de paramètres rempli.

### Le travail

- `prompts/03_chapitre.md` (le témoin) : le balisage du chapitre vitrine au lieu d'un balisage que le gabarit
  n'emploie pas, le glossaire sans balisage, la langue racine seule, les exigences de l'auteur.
- Les seize autres, confiés à cinq agents avec une consigne écrite (`consigne-prompts.md`, dans le bloc-notes de la
  session) : chaque tiret réécrit dans sa phrase, chaque passage contraire au gabarit réaligné après vérification dans
  le code, chaque fait invérifiable laissé et signalé.
- `prompts/modules/01-langues.md` : deux erreurs, héritées de l'ancien module et relevées par l'agent du prompt 14,
  corrigées (`generer_audio.py` sans arabe ; les fiches traduites à côté des françaises).

### Ce qui a été vérifié

Les dix-sept prompts : aucun tiret cadratin ni tiret demi-cadratin entre espaces, blocs de code équilibrés, aucun
octet NUL, fins de ligne cohérentes, `git diff --check` propre ; `data-tr` ne reste que dans des phrases qui
l'interdisent. Les faits sur lesquels les agents se sont appuyés ont été revérifiés : le format des données du QCM,
ses quatre difficultés, la note bornée à 0, `tools/generate_qcm_papier.py`, la signature du CSV, `generer_audio.py`
et le rangement des fiches.

### Ce qui n'est pas fait

Les relevés du lot, inscrits au registre : quatre points à trancher, et des documents et des défauts à reprendre. Une
faute (« attends rien », sans « n' ») a disparu du prompt 11 avec la phrase qui la portait, réécrite parce qu'elle
contredisait `CLAUDE.md` (elle disait de ne pas attendre la validation de l'auteur) : signalée à l'auteur.

### Pièges appris

- **Un module validé peut garder une erreur de l'ancien texte** : `docs/prompts/en/` venait du module « bilingue » et
  avait passé le témoin. Seul le code dit où les outils lisent.

---

## 22 novembre 2026 · lot 7, les modules (`63de114`)

### Les décisions de l'auteur

- **Le module 01 renommé `01-langues.md`** : il couvre le français, l'anglais et l'arabe, et `modules.bilingue`
  disparaît au profit de `cours.langues`. Le témoin (le module réécrit) a été validé avant la série.

### Le travail

- `prompts/modules/01-langues.md` (renommé par `git mv`) : le site miroir dans chaque langue, la méthode de
  l'arabe (le chapitre 1 de la démonstration en témoin, `docs/LEXIQUE-ar.md`), les six règles de l'arabe
  appliquées sans les redemander, la mise en page de droite à gauche, les pièges de l'arabe. La voix arabe reste à
  trancher, et trois outils qui ne savent pas encore l'arabe sont signalés. Six fichiers qui nommaient l'ancien
  module suivent.
- `prompts/modules/10-codex.md`, nouveau : Codex vérifié sur le poste, ou sa procédure officielle, vérifiée en
  ligne le 22 novembre sur le dépôt `openai/codex` et la documentation d'OpenAI, puis l'arrêt ; un dossier dédié
  hors du dépôt ; le témoin ; le message, sur le modèle du cours EADL ; la conversion en WebP ; la relecture ; la
  reprise d'une image ; les pièges de sa décision D49. Il rejoint le tronc, le README des prompts et le module 09.
- Le module 07 relu (ses paramètres), et les 53 tirets cadratins des modules 02 à 09 réécrits.

### Ce qui a été vérifié

Aucun tiret cadratin dans le tronc ni dans les dix modules ; plus aucun renvoi à `01-bilingue.md` ;
`cours.exemple.json` reste un JSON valide. Les commandes de Codex viennent de son aide installée (0.163.0) et de sa
documentation officielle ; la documentation se contredit sur Windows (WSL2 ou PowerShell natif), et le module le
dit.

### Ce qui n'est pas fait

Les dix-sept prompts numérotés ; les tirets de `CLAUDE.md` et de `docs/I18N.md`, hors du lot 7.

### Pièges appris

- **Un `git add` qui nomme un chemin disparu échoue en entier** : après le `git mv`, l'ancien nom du module n'existait
  plus, rien n'a été ajouté, et, la sortie d'erreur masquée, le commit est parti avec le seul renommage. Il a été
  complété avant d'être poussé. La parade consiste à lire `git diff --cached --stat` avant chaque commit.

---

## 22 novembre 2026 · lot 7, le tronc refondu (`16b0418`)

### Les décisions de l'auteur

- **Le générateur de prompt après le lot 7.** L'auteur le cherchait ; il n'existe pas encore (lot 8). Les prompts
  passent d'abord, pour que le générateur assemble un tronc et des modules à jour.
- **Le tronc d'abord, un témoin avant la série** : la section des pièges, validée, puis le reste.

### Le travail

- `prompts/PROMPT-Cours-parametrable.md` :
  - la section 6, 27 pièges déjà rencontrés et leur parade, en sept groupes (le poste, les secrets, l'audio, le
    navigateur, l'application Livrables, le contenu, l'arabe) ; l'annexe passe en section 7 ;
  - la section 2.5, ce que le cours livre et le critère d'acceptation de chaque sortie ;
  - les paramètres : les langues, les filières au format de `cours.json` (code, nom, palette, bloc, module, page
    des épreuves), le bouton du QCM, et ce qui part dans le bloc école ;
  - dans le prompt, les décisions déjà prises, chacune datée, une règle qui renvoie aux pièges, l'étape zéro et la
    définition de « terminé » mises à jour ;
  - ses 25 tirets cadratins réécrits.

### Ce qui a été vérifié

Les pièges viennent du tableau du prompt de cours d'étude d'avant-projet et des « Pièges appris » du journal ; aucun
n'est inventé, et ceux qui ne touchent que le moteur du gabarit sont écartés. Les décisions sont datées d'après le
registre et le journal. Aucun autre fichier n'emploie les anciens noms de paramètres. Aucun tiret cadratin.

### Ce qui n'est pas fait

Les modules (langues, Codex, école relu) et les prompts numérotés.

### Pièges appris

- **Une version plus longue n'est pas plus récente** : le tronc des cours EADL et CDWFS (536 lignes) date du
  11 octobre et précède celui du gabarit, qui l'a généralisé. Une version se date par son historique (`git log`).

---

## 22 novembre 2026 · lot 2, la documentation (`15b456b`)

### Les décisions de l'auteur

- **Le texte validé** avant le commit.

### Le travail

- `docs/GUIDE.md` : l'amorce dit ce que `nouveau_cours.py` écrit du bloc école ; la section 2 ter décrit le
  programme sans date, les sessions, le cahier de texte, le classeur Livrables et ses réglages, puis l'import par
  l'auteur, avec un tableau des commandes ; le récapitulatif du pipeline les reprend.
- `docs/CHECKLIST.md` : `seances.py` et `sessions.py` parmi les vérificateurs, et une phase 14 bis de huit cases,
  dont deux bloquantes (aucune date dans le contenu, le cahier avec identifiants qui reste sur le poste).

### Ce qui a été vérifié

Aucun tiret cadratin dans le texte ajouté, aucun lien mort. Les titres des anciennes phases de la CHECKLIST gardent
leur tiret, qui relève du lot de réécriture des documents ; la nouvelle phase prend le point médian.

### Ce qui n'est pas fait

L'arabe du lot 2, qui attend l'accueil arabe (lot 4).

---

## 22 novembre 2026 · lot 2, le bloc école de cours.json (`4deb980`)

### Les décisions de l'auteur

- **Épreuves, boutons et sessions** : le bloc école de `cours.json` remplit les trois dans un cours créé.
- **Le modèle tout rempli** : l'adresse de Livrables, le bouton du QCM et une session d'exemple aux valeurs fictives,
  à remplacer.

### Le travail

- `cours.exemple.json` : le bloc `ecole` (`livrables`, `bouton_qcm`, `sessions`), et dans chaque filière `bloc`,
  `module` et `epreuves`, décrits dans le commentaire.
- `nouveau_cours.py` : la validation du bloc (promotion « Année › Promotion », dates lisibles, ouvrées et dans
  l'ordre, couleur, adresses, bouton du QCM sans bloc `qcm`) ; l'écriture de `BOUTONS`, `FILIERES`, `LIENS` et
  `SESSIONS` en littéraux Python lisibles, une clé par ligne quand la ligne serait trop longue ; l'avertissement
  d'une session restée sur l'exemple, qui ne bloque pas. Une configuration sans bloc `ecole` se comporte comme avant.
- `outils/generer_cahier_de_texte.py` : sans adresse de Livrables, le cahier ne cite pas l'application.
- La recette, `CLAUDE.md` (§ 3), le module 07 et l'étape zéro du prompt suivent.

### Ce qui a été vérifié

Trois cours générés : boutons Livrables et QCM, session d'exemple écrite et signalée, et, dans le cours à une
filière, les épreuves EADL déclarées dans `cours.json`, avec leur pastille et leur bouton. Quatre configurations de
plus refusées (séparateur de promotion, week-end, bouton du QCM sans bloc, adresse d'épreuves). Une création depuis
le gabarit réel. La réécriture des définitions sur les blocs de plusieurs lignes de la démo. Le cahier et le
classeur de la démo, inchangés.

### Ce qui n'est pas fait

La documentation du lot 2 (GUIDE, CHECKLIST) et l'arabe.

### Pièges appris

- **Une session d'exemple qui bloquerait la création** ferait échouer la recette, qui part du modèle : le script
  avertit sans refuser.
- **sed et les échappements Unicode** : `\u26a0` passé par sed est devenu `26a0`. Un correctif se scripte en
  Python (§ 2).

---

## 22 novembre 2026 · lot 2, la pastille et les boutons des épreuves (`7914eb8`)

### Les décisions de l'auteur

- **Rien dans la démonstration** : elle ne prépare aucune épreuve réelle (lot 3), et son accueil ne change pas. Un
  cours qui déclare ses épreuves reçoit la pastille et un bouton par filière.
- **Le témoin validé**, un cours d'essai aux épreuves du cours EADL, puis la série.

### Le travail

- `FILIERES` (`outils/seances.py`) : pour chaque filière, son bloc, son module et la page de ses épreuves (adresse,
  titre, détail, langue). Son contrôle vaut avant même le programme.
- `outils/accueil.py` : le fragment `accueil-pastille`, à la suite du texte de la pastille, et un bouton « Épreuves
  du Bloc 1 » par filière, après ceux de `BOUTONS`. La filière se marque sur le lien lui-même, comme dans le cours
  EADL, et la langue de la page des épreuves devient un `hreflang`.
- `outils/generer_filieres.py` : sans filière choisie, une barre sépare deux mentions accolées en ligne (la règle du
  cours EADL).
- Les accueils de la démo et le squelette reçoivent le fragment. La pastille du squelette dit « À rédiger : le
  public du cours ».

### Ce qui a été vérifié

Le cours d'essai, en clair et en sombre, à 1280 et 375 px, avec et sans filière choisie, console vide ; sa page
anglaise, identique à celle du cours EADL (« Bloc 1 assessments », `hreflang="fr"`). La démo, inchangée en français
et en anglais, sans ressource manquante. Trois cours générés, sans bloc ni bouton d'épreuves. Le contrôle de
`FILIERES`, sur quatre fautes (filière inconnue, page introuvable, titre absent, tiret cadratin).

### Ce qui n'est pas fait

Le bloc `ecole` de `cours.json`, qui remplira `FILIERES` à la création d'un cours.

### Pièges appris

- **Une enveloppe `<span class="only-…">` autour d'un bouton** aurait reçu la barre que `filieres.css` pose entre
  deux mentions accolées. La filière se marque donc sur le lien.
- **Choisir une filière par script laisse sa palette** : pour une capture sans filière, vider le stockage et
  recharger la page.

---

## 22 novembre 2026 · lot 2, le classeur Livrables (`b4426fb`)

### Les décisions de l'auteur

- **Le témoin validé** (le classeur de la démonstration et ses réglages), puis la série : `nouveau_cours.py`, la
  documentation, les essais.
- **Le QCM noté de la démonstration en « Exercice / TP »**, rendu par son fichier CSV. Le type « QCM » de
  l'application corrige une grille d'après un corrigé à lettres fixes, et le QCM du site mélange questions et
  propositions.

### Le travail

- `outils/generer_classeur_livrables.py` : les cinq feuilles aux en-têtes exacts de l'application, un classeur par
  session de `outils/sessions.py`, donc par promotion. La colonne Contenu des séances reprend le cahier de texte
  (`texte_seance()`) ; les liens viennent de `deploiement/destination.json` et restent vides sans adresse. Le
  générateur refuse une description hors de trois à six phrases, des consignes hors de cinq à dix, une grille hors
  de quatre à six critères ou qui ne totalise pas la note maximale, une séance inconnue, une échéance avant sa
  séance, un « = » en tête de cellule. `--essai` compare les valeurs des cellules.
- À côté du classeur, `docs/Import_Livrables_<session>_reglages.txt` : les créations que l'aperçu doit annoncer, la
  case des fichiers joints, la version de travail jamais notée et jamais cochée « facultatif », la note du QCM du
  site, le réimport qui ne supprime rien. Chaque phrase a été vérifiée dans le guide et le code de l'application.
- `outils/seances.py` : la description de la matière, les consignes, le format et la page de chaque livrable, les
  ressources. Les textes ont été vérifiés contre l'atelier et le QCM du site, barème compris.
- `nouveau_cours.py` : un cours créé part sans description ni ressources, et ne reçoit pas le classeur de la
  démonstration. Le module 07, `CLAUDE.md`, `ARCHITECTURE.md` et la recette suivent.

### Ce qui a été vérifié

Le classeur de la démonstration : 1 matière, 4 séances, 3 livrables, 6 critères pour 20 points, 6 ressources,
aucune formule ; une seconde génération ne change rien. Un clone sans adresse : liens et ressources vides, et une
remarque qui ne bloque pas. Trois cours générés depuis une copie sans secret, et une création depuis le gabarit
réel : ni classeur ni cahier recopiés, et un classeur qui répond « aucune séance ». Contrôles verts, sauf les
91 tirets du lot S4 et les 32 pages de `hreflang.py`.

### Ce qui n'est pas fait

L'import réel dans l'application, que fait l'auteur. L'écart entre la page du QCM (envoi du CSV par e-mail) et les
consignes du classeur (dépôt dans l'application), inscrit au registre.

### Pièges appris

- **« Livrable bonus, facultatif » rend un livrable non dû** : une version de travail obligatoire ne la coche pas.
  La moyenne de l'application ne compte que les livrables notés.
- **Un rendu est un lien par défaut** : un fichier demande la case « Autoriser les fichiers joints », que l'import
  ne porte pas.
- **openpyxl relit une chaîne vide comme une case vide** : `--essai` voyait périmé un classeur tout juste écrit.

---

## 22 novembre 2026 · lot 2, le cahier de texte Yparéo (`0211023`)

### Les décisions de l'auteur

- **Le témoin validé** (le cahier de la démonstration, en texte et en Word), puis la série : le remplacement de
  l'ancien générateur, `nouveau_cours.py`, la documentation.

### Le travail

- `outils/sessions.py` : la date de chaque jour, la promotion, la matière ; les dates de la démonstration sont
  fictives (lundi 11 et mardi 12 janvier 2027). Son contrôle refuse un jour sans date, un week-end, des dates dans
  le désordre, une promotion sans « › ».
- `outils/generer_cahier_de_texte.py` : un bloc par séance, la ligne datée de la séance, ses chapitres, CONTENU DE
  LA SÉANCE (le sous-titre et les objectifs de chaque chapitre, lus dans sa page ; l'atelier) et TRAVAIL À FAIRE (le
  travail, ce qu'il faut rendre avec sa date réelle, le dépôt sur Livrables, le support). En `.txt`, en fins de
  ligne Windows et avec les espaces insécables, et en `.docx`. La version avec identifiants sort quand
  `docs/acces.json` existe ; `.gitignore` et `.rgignore` l'écartent. `--essai` signale un cahier périmé, sans
  échouer sur un cahier absent (les cahiers ne sont jamais versionnés).
- `docs/generate_cahier_de_texte.py` retiré : il gardait des restes d'un autre cours.
- `nouveau_cours.py` : des sessions vides dans un cours créé, qui ne reçoit pas les cahiers de la démonstration.

### Ce qui a été vérifié

Le cahier de la démonstration : quatre séances, la version de travail au lundi 17 h 00, le dossier final au dimanche
17 janvier 2027 à 23 h 59, aucun tiret cadratin, 69 fins de ligne Windows ; le Word, un titre par séance. Trois cours
générés : sessions vides et cohérentes, un cahier qui répond « aucune séance », aucune copie de la démonstration.
Contrôles verts, sauf les 91 tirets du lot S4.

### Ce qui n'est pas fait

La version avec identifiants, faute de `docs/acces.json` dans le gabarit ; le classeur Livrables.

### Pièges appris

- **`lower()` sur une phrase entière** écrivait « le qcm » : seule la première lettre se baisse.
- **Un contrôle de péremption sur des fichiers jamais versionnés** échouerait sur chaque clone neuf : un cahier absent
  n'est pas périmé.

---

## 22 novembre 2026 · lot 2, le programme sur l'accueil (`088a1a8`)

### Les décisions de l'auteur

- **« Avec ou sans accès »** veut dire les deux : le cahier de texte avec et sans les identifiants du site (le sens
  qu'il a dans tous les cours de l'auteur), et une voie sans Yparéo, par la colonne Contenu des séances de
  l'application Livrables.
- **Le programme vit sur l'accueil**, pas sur une page à part.
- **Un seul format** dans la démonstration : le modèle sait en décrire plusieurs, la bascule viendra avec un cours
  qui en déclare deux.
- **Les dates réelles et les promotions dans `outils/sessions.py`**, versionné dans un cours (son dépôt est privé),
  fictif dans le gabarit public.
- **Une version de travail obligatoire et non notée** : due, rappelée, signalée manquante, hors de la moyenne
  (« facultatif » veut dire bonus dans l'application).
- **Le programme de démonstration** : deux jours, quatre séances, la version de travail le Jour 1 à 17 h 00, le QCM
  noté le Jour 2, le dossier final le dimanche qui suit, noté sur la grille des six critères de l'atelier.
- **La carte Durée en jours** (« 2 jours »), comme dans les cours de l'auteur.

### L'analyse

Celle des cours d'étude d'avant-projet, de CDWFS/ASRC, d'architecture et de veille, et de la documentation de
l'application Livrables. Le cours d'avant-projet est le plus abouti : son `seances.py` nourrit le site, trois
cahiers de texte et un classeur par promotion, sans date. Architecture apporte le déroulé minuté et un échéancier
qui lit les coefficients ; CDWFS/ASRC, les séances sans chapitre et la mise à jour ciblée. L'application attend
cinq feuilles, des en-têtes exacts, le séparateur « › », l'heure locale ; l'import ne supprime jamais rien, et le
titre d'un livrable est une clé.

### Le travail

- `outils/seances.py` : séances, travail, livrables, repères, et `verifier()` ; textes en français et en anglais
  à la source.
- `outils/programme.py` : les fragments `programme`, `echeances`, `duree-cours`, `nb-seances` ;
  `generer_fragments.py` contrôle le programme avant d'écrire.
- L'accueil : le programme dans « Le parcours », les échéances dans « Ce que vous produisez » (pas de nouvelle
  section : les noms des capsules, fixés par numéro, auraient bougé) ; sur téléphone, une carte par séance.
- `nouveau_cours.py` : un programme vide dans un cours créé, dont les pages disent « à rédiger ».

### Ce qui a été vérifié

Au navigateur, à 1280 et 375 px, en clair et en sombre ; contrôles verts, parité comprise ; trois cours générés,
programme vide et cohérent, aucun lien mort ; la sortie de `nouveau_cours.py` conforme à la recette.

### Pièges appris

- **`text-transform: capitalize`** met une majuscule après un trait d'union (« Après-Midi ») : `::first-letter`
  ne touche que la première lettre.
- **Un contrôle qui bloque tout** : sans tolérance pour un programme vide, `verifier()` aurait empêché un cours créé
  d'écrire le moindre fragment.

---

## 22 novembre 2026 · la démo en ligne, et un mot de passe retiré d'un commentaire (`0ac89d7`)

### Les décisions de l'auteur

- **La mise en ligne tout de suite**, essai à blanc d'abord, plutôt qu'à la fin du chantier (lot 12).
- **Le dossier distant** : celui qui répond à `https://mohamedelafrit.com/teaching/cours_demo/`, donné par
  l'auteur. `deploiement/destination.json` reste local (exclu par `.git/info/exclude`) : le dépôt est public.
- **L'envoi sans les liens hreflang** : posés dans le gabarit, ils passeraient dans chaque cours créé.
- **Le mot de passe** cité en exemple dans un commentaire n'est plus en service, ou était fictif : remplacé par un
  exemple neutre.

### Le travail

- L'essai à blanc : connexion SFTP, dossier distant à créer, aucun carnet sur le serveur, 120 fichiers, soit
  exactement les fichiers de `site/` suivis par Git (premier envoi).
- L'envoi : 120 fichiers, 12 Mo, sans `--purge`.
- `docs/generate_cahier_de_texte.py` : l'exemple du commentaire de la ligne 139, relevé par l'analyse du bloc école,
  public depuis `63be61c` (28 août 2026). L'historique de Git le garde ; seul le fait qu'il ne serve plus le rend
  inoffensif.

### Ce qui a été vérifié

En ligne, sans s'authentifier : 19 adresses à 200 (accueil, pages anglaises, chapitre 1 arabe, QCM, styles,
scripts, polices, polycopié) ; au navigateur, l'accueil en ligne sans erreur ni ressource manquante ; un nouvel essai
à blanc : « 120 inchangés, 0 à envoyer ».

### Ce qui n'est pas fait

Les liens hreflang (lot 1) ; aucune zone protégée : le corrigé du QCM et le tableau de bord sont en accès libre.

### Pièges appris

- **Un masquage qui ne connaît que les guillemets droits** laisse passer une chaîne entre guillemets français : la
  vérification d'un secret se fait sans l'afficher du tout (sa longueur, le commit qui l'a introduite).

---

## 21 novembre 2026 · lot 3 terminé, les capsules anglaises de l'accueil (`0d3d1df`)

### Les décisions de l'auteur

- **Le témoin anglais validé, puis les huit autres traductions** : la règle « un exemple avant la série » vaut pour
  une traduction comme pour une capsule.

### Le travail

- `docs/prompts/Capsules_accueil_en.md` : chaque capsule traduit son texte français validé. Là où la démonstration
  avait déjà une formulation anglaise (sous-titres des chapitres, atelier, barème du QCM, accueil anglais), elle
  est reprise mot pour mot. Prononciation « E.A.D.L. », « Eris », comme les capsules anglaises du cours d'étude
  d'avant-projet ; orthographe américaine, comme le site ; pas d'accent ajouté sur les pistes anglaises.
- `synchroniser_capsules.py` reporte les transcriptions et les durées dans `en/index.html`, sans espaces
  insécables : la typographie française ne vaut que pour une page française.

### Ce qui a été vérifié

Au navigateur, la page anglaise annonce « 1:25 (planned) » et ouvre chaque transcription ; aucune ressource en
erreur ; parité intacte ; une seconde synchronisation ne change rien.

### Ce qui n'est pas fait

L'enregistrement des dix-huit pistes et leur place dans la liste de lecture (lot 9), l'accueil arabe (lot 4).

---

## 21 novembre 2026 · lot 3, les capsules de l'accueil (`93728b3`) et une faute corrigée (`0d10e75`)

### Les décisions de l'auteur

- **« Police de lecture adaptée »** au lieu de « police lecture adaptée », faute relevée en chemin : corrigée dans
  l'accueil et dans `prompts/01_cadrage_maitre.md`, dans un commit à part. L'anglais était juste.
- **Le témoin, puis la série** : le texte de la capsule de bienvenue validé seul, puis les huit autres d'un coup.

### Le travail

- `docs/prompts/Capsules_accueil.md` : neuf capsules en français, au format que lit `generer_audio.py` (noms
  fixés, durées visées, tolérances). La bienvenue (≈ 1 min 25), une capsule par filière (≈ 40 s), une par section
  (50 à 57 s). Chaque phrase vient d'une page de la démonstration ; la prononciation suit celle du cours d'étude
  d'avant-projet (« E.A.D.L. », « Éris »), et chaque balise porte « speaking slowly ».
- `outils/synchroniser_capsules.py` reporte aussi les capsules de l'accueil : la transcription et la durée vont
  dans le script de la page, à l'entrée qui appelle chaque fichier ; une page française y reçoit ses espaces
  insécables, la fiche gardant des espaces simples.
- `nouveau_cours.py` retire cette fiche d'un cours créé, comme celle des chapitres de la démonstration.

### Ce qui a été vérifié

Au navigateur, la capsule de bienvenue annonce « 1:25 (prévu) » et ouvre sa transcription ; les six capsules de
section aussi. Le générateur lit les neuf scripts et leurs tolérances. Contrôles verts, parité comprise, sauf les
91 tirets du lot S4 ; un cours créé n'a aucune fiche de capsules de la démonstration.

### Ce qui n'est pas fait

Les capsules anglaises (leur fiche), l'enregistrement (lot 9), leur place dans la liste de lecture.

---

## 21 novembre 2026 · lot 3, la page d'accueil (`0910118`)

### Les décisions de l'auteur

- **La page d'accueil des cours d'architecture et d'étude d'avant-projet** (« il manque encore la page d'accueil du
  cours », avec trois captures) : elle passe avant le bloc école. Le cours de veille technologique s'ajoute aux
  modèles analysés.
- **Les deux boutons blancs de la démonstration** : le dépôt sur Livrables, l'application de tous ses cours, et le QCM
  de la démonstration. Celle-ci ne prépare aucune épreuve réelle : un bouton « Épreuves du Bloc 1 » l'aurait annoncé.
- **L'exemple français validé**, puis la série : l'anglais, `nouveau_cours.py`, la documentation.

### L'analyse

Les trois accueils ont la même structure : un bandeau sombre (pastille, titre et son mot coloré, accroche, trois
boutons, quatre cartes), une capsule d'accueil, des sections numérotées, un bouton flottant (sauf celui de veille).
Celui d'avant-projet est le plus complet (contenu et capsules par filière, cartes de chapitre illustrées) ; celui
d'architecture garde son bandeau sombre dans les deux thèmes ; celui de veille, le plus récent, tire tout des
données. Leurs défauts : l'accent de filière réutilisé sur le bandeau sombre (1,56 pour 1 sur les étiquettes, en
EADL), 46 tirets cadratins sur l'accueil d'architecture, les adresses écrites dans la page, « Programme » masqué
sous 768 px, un bouton flottant qui couvre les boutons du bandeau à 375 px.

### Le travail

- `site/index.html` et sa jumelle `en/` : le bandeau, les capsules d'accueil et de filière, six sections ouvertes
  chacune par sa capsule (le parcours, le fil rouge, ce que vous produisez, l'évaluation, ce que démontre ce site,
  avant de commencer), le polycopié et les podcasts, le bouton flottant. Leur prose vient des pages de la
  démonstration ; neuf noms de pistes sont fixés.
- `outils/accueil.py` : les fragments `accueil-boutons` (les adresses vivent dans ses données) et
  `cartes-chapitres` (titre, durée, sous-titre du chapitre, illustration déposée ou emoji).
- `palettes.css` : `--hero-1` à `--hero-3` et `--hero-accent`, mêmes valeurs dans les deux thèmes, calculés pour
  4,6 pour 1 au moins ; `verifier_contraste.py` les mesure.
- Le menu ☰ replié sur l'accueil à toutes les largeurs (la bascule de filière y vit sur téléphone) ; le bouton
  flottant qui attend, sur téléphone, que « Commencer » quitte l'écran ; le monogramme du logo, qui s'empilait.
- Le nombre de livrables au référentiel, pour l'accueil et l'atelier.
- `nouveau_cours.py` : l'accueil d'un cours créé, même structure, consignes à rédiger, sans « Ce que démontre ce
  site » ; `BOUTONS = []`.

### Ce qui a été vérifié

Au navigateur, à 1280 et 375 px, en clair et en sombre, sans filière puis avec EADL (le bandeau passe en émeraude,
la capsule d'ERIS se cache) ; la bascule de langue garde la position de lecture (le même titre à la même hauteur).
Aucune ressource en erreur sur l'accueil. Contrôles verts, parité comprise, sauf les 91 tirets du lot S4. Trois
cours générés : la structure attendue, ni prose de la démonstration, ni lien mort.

### Ce qui n'est pas fait

La fiche des capsules de l'accueil (leurs textes), leur place dans la liste de lecture, l'accueil arabe, les
illustrations des cartes, les boutons des épreuves (bloc école).

### Pièges appris

- **Un panneau de navigateur masqué fausse les essais** : l'observateur d'intersection et le défilement doux n'y
  avancent qu'aux captures d'écran. Un bouton qui « ne se cache pas » et une position de lecture « perdue » étaient
  des artefacts du test ; un saut immédiat (`behavior: 'instant'`) et une capture avant la mesure les ont levés.
- **Un observateur peut livrer plusieurs états d'un coup** : c'est le dernier qui compte, et l'état de départ se lit
  tout de suite, sans attendre le premier rappel.
- **`auto-fill` garde une colonne vide** au bout d'une rangée de trois cartes ; `auto-fit` la referme.

---

## 21 novembre 2026 · lot 1, les filières et les langues d'un cours (`f3cc344`)

### Les décisions de l'auteur

- **Les filières et les langues, deux paramètres du lancement** (décidé au cadrage) : un cours commun à deux
  filières ou réservé à une seule ; une à trois langues parmi le français, l'anglais et l'arabe.
- **Cette étape en dernière partie du lot 1**, choisie comme suite : le générateur de prompt (lot 8) en aura besoin.
- **La page d'accueil, redemandée** en fin d'étape, avec un troisième modèle (le cours de veille technologique) :
  elle passe avant le bloc école.

### Le travail

- `cours.json` a la clé `filieres` (identifiant, sigle, palette, numéro RNCP, nom et intitulé court par langue),
  commentée dans `cours.exemple.json` avec EADL et ERIS ; `langues` accepte l'arabe après la langue racine.
- `nouveau_cours.py` valide chaque filière (identifiant unique en minuscules, sigle, palette connue, nom et intitulé
  court dans la langue racine) et refuse l'arabe comme racine tant que la démonstration n'a pas toutes ses pages en
  arabe (lot 4), avec un seul motif.
- Le `course-data.js` du cours créé reçoit ses filières, et une filière seule aussi : l'accueil pourra la nommer,
  sans bascule. Les titres arabes de `cours.json` et les libellés arabes des ressources (ceux de la démonstration,
  d'après le lexique) s'y écrivent quand le cours déclare l'arabe. `filieres.css` suit.
- Le résumé du lancement nomme les filières. La ligne de sortie de `generer_filieres.py` perd son tiret cadratin.
  La recette annonce la ligne de `filieres.css` et contrôle la bascule.

### Ce qui a été vérifié

Sur une copie du gabarit sans secret, trois cours générés : français, anglais et arabe à deux filières, français à
une filière, anglais sans filière. Pour chacun, node lit `course-data.js` sans erreur, `filieres.css` est à jour, et
il n'y a ni lien mort, ni dossier de langue, ni trace d'EADL ou d'ERIS hors des données. Quatre configurations
fautives sont refusées avec leur motif (racine arabe, palette inconnue, identifiant en double, nom absent). Au
navigateur, sur le cours d'essai, la bascule et le bandeau apparaissent ; ERIS choisi passe l'accent en prune, et le
choix suit sur le chapitre squelette, sans erreur. Les contrôles du gabarit sont verts, sauf les 91 tirets du
lot S4.

### Ce qui n'est pas fait

Les pages jumelles d'un cours ne naissent pas au lancement : elles viennent ensuite, avec `creer_jumelle.py`, en
anglais comme en arabe. L'arabe comme racine attend le lot 4.

### Relevé en chemin

- Un cours de racine anglaise doit encore donner ses titres en français, que la validation exige : à corriger.
- Le texte d'exemple de `public.parcours`, affiché sur l'accueil, porte un tiret cadratin : à traiter avec la page
  d'accueil.

### Pièges appris

- **La sortie attendue dépend des données** : avec les filières du modèle, qui sont celles de la démonstration,
  `filieres.css` est déjà « à jour » dans le cours créé ; il n'est « écrit » qu'avec d'autres filières.

---

## 21 novembre 2026 · lot 1, la bascule de filière (`0f8a846`)

### Les décisions de l'auteur

- **La bascule du cours EADL, rendue générique** (décidé au cadrage) : aucun nom de filière dans un moteur.
- **EADL en émeraude, ERIS en prune** : les palettes vérifiées les plus proches des couleurs du cours EADL.
- **Sur téléphone, la bascule en tête du menu ☰** : l'en-tête d'un chapitre est déjà plein à 375 px.
- **Le témoin** : un exemple propre à chaque filière dans « Le fil rouge » du chapitre 1, texte validé avant d'être
  posé, puis traduit en anglais et en arabe.

### Le travail

- Les filières se déclarent dans `course-data.js` : identifiant, sigle, palette, numéro RNCP, nom et intitulé court
  en trois langues (ceux du cours EADL). Une seule filière, ou aucune : pas de bascule.
- `filiere.js`, chargé par `navigation.js` dès deux filières : la bascule, sa copie dans le menu, le bandeau
  « Quelle est votre filière ? », le choix retenu, l'accent pris dans la palette de la filière, l'API `TPLFILIERE`.
- `filieres.css`, généré par `outils/generer_filieres.py` : un sélecteur CSS ne peut pas comparer la filière de la
  page à la classe d'un bloc, les règles s'écrivent donc pour les filières du cours. Sans choix, les deux versions
  s'affichent, étiquetées de la couleur de leur palette.
- Trois lignes en tête des 33 pages posent la filière mémorisée avant l'affichage, ou celle d'un lien
  (`?filiere=eris`).
- `nouveau_cours.py` donne à un cours créé un `filieres.css` vide, et des squelettes sans les blocs du témoin.

### Ce qui a été vérifié

Au navigateur : les deux exemples étiquetés sous le bandeau, sans choix ; EADL choisi, l'autre exemple masqué,
l'accent en émeraude, le choix retenu, posé avant l'affichage au rechargement, suivi en anglais et en arabe ; la
désélection rend la couleur du cours ; le lien impose ERIS ; à 375 px, la bascule est dans le menu et l'en-tête ne
déborde pas. Contrôles verts ; un cours généré n'a aucune trace d'EADL ni d'ERIS hors de `_modele.html`.

### Ce qui n'est pas fait

Les pages du QCM ne chargent pas les données du cours : elles n'ont pas de bascule, seulement la couleur de la
filière. La liste de lecture par filière du cours EADL n'est pas reprise. Les filières de `cours.json` viendront avec
les paramètres, la dernière partie du lot 1.

### Pièges appris

- **Le stockage local est partagé par tous les cours d'un même site** : un choix de filière gardé sous une clé fixe
  passerait d'un cours à l'autre sur mohamedelafrit.com. La clé porte l'adresse de la racine du cours.
- **Une palette choisie après coup se voit** : le script de tête retient la palette avec la filière, et la pose avant
  l'affichage ; sinon la page passait d'une couleur à l'autre.

---

## 21 novembre 2026 · lot 1, le témoin arabe et la mise en page de droite à gauche (`737e23b`, `d301d41`)

### Les décisions de l'auteur

- **Les chiffres occidentaux** (1, 2, 3) dans les pages arabes : les numéros restent les mêmes d'une langue à
  l'autre.
- **Traduire la fonction, pas les mots.** À la question des termes techniques, l'auteur a répondu par l'exemple :
  « projet fil rouge », utilisé pour illustrer les notions du cours, se dit « المشروع التطبيقي ». Le calque que je
  proposais (« الخيط الناظم ») est écarté. Un lexique a été proposé terme par terme, avant toute traduction.
- **Les variantes du Maghreb** quand deux usages existent : « المطبوعة », « المكتسبات القبلية »,
  « الهدف البيداغوجي », « التقويم الإجمالي ».
- **Le terme français entre parenthèses** à sa première apparition dans une page, pour les notions du glossaire.

Le tout est consigné dans `docs/LEXIQUE-ar.md`, qui part dans chaque cours.

### La mise en page et les outils (`737e23b`)

- Les 114 déclarations qui nommaient la gauche ou la droite deviennent des propriétés logiques, égales aux
  anciennes en français et en anglais. Restent physiques les points d'un schéma (des coordonnées dans l'image), les
  boutons « défiler à gauche / à droite » et les centrages.
- Un bloc pour l'arabe : Noto Naskh et Noto Sans Arabic après les polices latines, qui gardent les mots en lettres
  latines ; un interligne plus ample ; ni lettres espacées ni italique ; le code de gauche à droite ; les
  translations du menu mobile et de la liste de lecture retournées.
- Une capsule ou un schéma attendu ne se demande plus au serveur : la liste des médias connaît `voix/` et
  `schemas/`. Le registre relevait cette erreur 404 sur `_modele.html` dans les cours créés.
- Les outils savent l'arabe : jumelles (`creer_jumelle.py --langue ar`), liens, parité (avec un contrôle des blocs
  restés sans lettre arabe), menu, fragments (« 30 د »), encadré du podcast, « Où en parle-t-on ? ».
- « Question » et les libellés de `quiz.js` étaient écrits en dur : ils passent par `ui-labels.js`, qui reçoit la
  table arabe (191 clés).

### Le témoin (`d301d41`)

Le chapitre 1 en arabe, préparé par l'outil puis traduit bloc pour bloc : 28 blocs, 0 écart de parité. S'y
ajoutent le contenu des composants, les titres du cours, les termes du glossaire, les cartes de révision et
l'épisode 1 du podcast. Le lien « Pour approfondir » mène à la page arabe de Wikipédia sur la taxonomie de Bloom,
« تصنيف بلوم لأهداف التعلم », ouverte et vérifiée (le titre court, « تصنيف بلوم », n'est qu'une redirection cassée).

### Ce qui a été vérifié

Au navigateur, à 1280 et 375 px, en clair et en sombre : la page arabe retournée (menu, puces, bordures,
pagination, menu mobile, panneau ♿), l'interface et les bulles du glossaire en arabe, la lecture adaptée avec une
police arabe lisible, le groupe « FR · EN · عربي » sur les trois versions du chapitre, la console vide. Le français
et l'anglais sont inchangés, mesures prises sur sept pages. Les contrôles sont verts (`verifier_tirets.py` à 91,
lot S4).

### Choix pris en chemin, à revoir si l'auteur le souhaite

Sur téléphone, la pastille du logo laisse sa place au groupe de langues : avec trois langues, l'en-tête d'un
chapitre dépassait de près de 100 px à 375 px, et le logo passait sous le bouton ♿. Le menu ☰ mène aussi à
l'accueil, et les boutons gardent leurs 44 px.

### Pièges appris

- **L'espacement des lettres délie l'arabe** : les titres et les étiquettes en capitales espacées doivent revenir à
  un espacement normal sur une page arabe.
- **Les chevrons ‹ › sont des caractères miroirs**, que le navigateur retourne de lui-même ; les flèches → ← ne le
  sont pas, et s'inversent à la main dans les libellés arabes.
- **Une police à chasse fixe sans arabe** laisse le navigateur choisir une police système qui espace mal les
  lettres : la pile à chasse fixe des pages arabes passe par Noto Sans Arabic.

---

## 21 novembre 2026 · lot 1, le socle à plusieurs langues (`3d941a7`)

Le site miroir ne connaissait que le français à la racine et l'anglais sous `en/`. **Décisions de l'auteur** : un
groupe de langues côte à côte dans l'en-tête, la langue lue mise en évidence, plutôt qu'un menu ou un bouton qui
passe à la suivante ; et « عربي » pour l'arabe, le nom de la langue dans sa propre écriture.

- `langues-data.js` devient `window.TPL_MIROIR` : la langue racine (celle de l'accueil), puis, pour chaque autre
  langue, les pages qui y ont leur jumelle. `generer_langues.py` la déduit des dossiers de langue de `site/`.
- `langue.js` pose le groupe. Une langue n'y figure que si la page y existe, et le groupe n'apparaît qu'à partir de
  deux langues ; chaque libellé est écrit dans sa langue, la langue lue est cerclée et inerte. La reprise du
  paragraphe lu ne change pas, et l'accueil se rouvre dans la dernière langue choisie, quelle qu'elle soit.
- `i18n.js` connaît l'arabe et pose `dir` sur la page (`rtl` pour l'arabe). Les blocs `data-tr`, eux, restent
  français et anglais.
- `navigation.js`, `glossaire-tooltip.js` et `podcasts.js` suivent la langue de la page : le menu d'une jumelle
  marque une page restée dans la langue racine, une bulle de glossaire cherche les termes dans la langue de la
  page.
- Le panneau ♿ prend ses libellés dans `ui-labels.js`. Écrits en dur, ils restaient en français sur une page
  anglaise (relevé le matin même, à la vérification des polices).
- Les outils qui lisent la liste suivent (`creer_jumelle.py`, `data_tr_vers_miroir.py`, `hreflang.py`), ainsi que
  `docs/I18N.md`, `docs/ARCHITECTURE.md` et le § 4 de `CLAUDE.md`.

### Ce qui a été vérifié

Au navigateur, le groupe « FR · EN » s'affiche sur le chapitre 1 ; EN rouvre la jumelle sur le même paragraphe, à la
même hauteur ; le panneau ♿ et le glossaire parlent anglais sur la page anglaise ; l'accueil s'ouvre dans la langue
choisie ; à 375 px en sombre, l'en-tête tient sans débordement ; la console reste vide. Les contrôles sont verts
(`verifier_tirets.py` à 91, lot S4), et un cours généré part avec une liste vide et aucun lien mort.

### Ce qui reste pour l'arabe

L'arabe n'entre dans le groupe qu'avec sa première page. Viennent ensuite la mise en page de droite à gauche, le
témoin (le chapitre 1 en arabe), puis les outils Python à N langues (jumelles, parité, liens, `hreflang`, menu).

---

## 21 novembre 2026 · lot 1, la démo en site miroir et le générateur qui la suit (`59474ee`, `a008dac`, `3f50098`)

### Deux décisions de l'auteur

- **Le témoin arabe se fera sur la démo convertie.** Le site miroir à N langues demande des pages miroir, et les 16
  pages de la démo étaient en blocs `data-tr`. La conversion, prévue au lot 4, est avancée ; l'accueil du lot 3 se
  bâtira directement dans le modèle final.
- **`nouveau_cours.py` ne crée plus que des cours en site miroir.** Les blocs `data-tr` restent décrits et outillés
  pour les cours qui les ont déjà (UML · C4 · BPMN · EPC). Garder leur création aurait demandé de refondre chaque page
  avec sa jumelle, et l'arabe n'y serait pas entré.

### La conversion (`59474ee`, `a008dac`)

`data_tr_vers_miroir.py` et `creer_jumelle.py` refusaient de tourner dans le gabarit : le verrou est levé. L'outil
composait le titre d'un chapitre avec un tiret cadratin, il prend maintenant le deux-points. Les 16 pages sont
devenues 16 pages françaises et 16 jumelles anglaises, sans aucun écart de parité. Les titres d'onglet et les
descriptions restés en français dans les jumelles sont traduits d'après une table validée par l'auteur ; la
description du sommaire annonçait « 5 chapitres » pour trois, ce que corrige un commit à part (`a008dac`). Au
navigateur, le bouton EN du chapitre 1 ouvre la jumelle sur le paragraphe lu, à la même hauteur, et le bouton FR y
ramène.

### Le générateur (`3f50098`)

Généré depuis la démo convertie, un cours recevait les 16 jumelles anglaises de la démo, déclarées en français, et
gardait des textes de la démo : le générateur cherchait des blocs bilingues qui n'existent plus. Il fait maintenant
naître chaque page dans la langue racine, la première de « langues ». Un cours anglais part des jumelles anglaises,
remontées à la racine par `miroir.remonter()`, l'inverse de `reloger()` (aller-retour exact sur les 16 pages). Aucune
jumelle n'est recopiée, la liste des pages traduites part vide, et les autres langues viennent ensuite avec
`creer_jumelle.py`.

Le même cours d'essai, généré depuis le commit d'avant la conversion, a montré quatre défauts plus anciens, corrigés
du même coup :

- les trois squelettes s'annonçaient « Chapitre 1 : Cadrer son cours / Scoping your course », parce que le titre était
  cherché mot pour mot et que le témoin sans tirets (`ea1cc23`, 7 novembre) l'avait changé ;
- le sous-titre du sommaire gardait une phrase de la démo (« vous saurez concevoir un cours en ligne ») ;
- le badge « Chapitre vitrine » restait sur les squelettes ;
- l'en-tête « Objectifs du chapitre » devenait un repère de paragraphe.

### Ce qui a été vérifié

La recette du § 3 a tourné sur trois cours d'essai, générés depuis une copie du gabarit sans secrets (les seuls
fichiers suivis ou non ignorés) : un cours français, un cours anglais, un cours français et anglais. On n'y trouve
aucune trace de la démo ni aucun lien mort ; chaque page est dans la langue racine, sans dossier `en/`, `CLAUDE.md` n'a
aucun passage du gabarit et le déployeur est conforme ; au navigateur, le cours français s'affiche sans erreur ni 404.
La recette suit le changement : sortie attendue, contrôle des dossiers de langue, et un § 3 bis qui teste désormais un
cours anglais.

### Relevé en chemin

- `verifier_tirets.py` passe de 69 à 97, parce que les pages du QCM existent en deux langues avec leurs dictionnaires.
  Le squelette du QCM qu'écrit le générateur a aussi ses tirets. Ils reviennent au lot S4.
- `generer_playlist.py` n'a pas d'option `--essai` : appelé ainsi, il réécrit sa liste (contenu identique ici, la
  copie du dépôt a été remise telle quelle).
- Plusieurs prompts et guides décrivent encore la bascule 🌐 comme celle de la démo ; ils seront revus aux lots 7 et
  11.

### Pièges appris

- **Un texte cherché mot pour mot cesse d'être trouvé sans bruit** quand on le réécrit ailleurs : le titre du chapitre
  vitrine a changé le 7 novembre, et les squelettes ont gardé l'ancien pendant deux semaines. Le générateur remplace
  désormais la balise entière, et la recette du § 3 se repasse après toute retouche du chapitre vitrine.
- **Une recherche qui inclut les `.json` doit exclure les secrets nommément** (`CLAUDE.md`, § 2) : une commande qui
  l'oubliait a été refusée, à raison.

---

## 21 novembre 2026 · lot 1, les polices hébergées avec le site (`a28b685`)

Première partie du lot 1 du grand chantier, après l'accord de l'auteur pour le téléchargement (22 fichiers, leur
source et leur poids annoncés avant). Les pages chargeaient leurs polices depuis Google Fonts, et `accessibility.js`
y cherchait Atkinson Hyperlegible en mode lecture adaptée, contre le § 7 de `CLAUDE.md`.

- `site/assets/fonts/` : 16 fichiers woff2 pris à l'API de Google Fonts, en sous-ensembles latin et latin-ext pour
  Sora, Source Serif 4, JetBrains Mono et Atkinson Hyperlegible, arabe pour Noto Naskh Arabic et Noto Sans Arabic
  (876 Ko, dont 253 Ko d'arabe). Chaque fichier est contrôlé contre la taille annoncée par le serveur et la signature
  woff2. Les six licences SIL OFL 1.1, qu'elles demandent de joindre, sont dans `licences/`.
- `site/assets/css/fonts.css` : un `@font-face` par fichier, avec la plage Unicode de Google Fonts et
  `font-display: swap`. Chaque page le charge avant `main.css`.
- `accessibility.js` ne charge plus rien ; le navigateur ne télécharge Atkinson que lorsque le mode DYS l'emploie.
- `demarrer.py` déclare `font/woff2` et `image/webp`, que Python ne connaît pas sous Windows (point du registre clos).
- README, ARCHITECTURE, CHECKLIST et `prompts/01_cadrage_maitre.md` ne renvoient plus à Google Fonts. Le prompt de
  cadrage l'aurait fait remettre dans un cours créé.

### Ce qui a été vérifié

Au navigateur, sur le chapitre 1, l'accueil et la correction du QCM : aucune requête hors du site, polices servies
par `/assets/fonts/` avec leur type, Atkinson locale en mode DYS, console vide, 1280 px en clair et 375 px en sombre.
Les contrôles du § 6 passent ; `verifier_tirets.py` reste à 69 (lots S4 et S5). Une page latine télécharge 310 Ko de
polices, comme avant chez Google.

### Relevé en chemin

- Le panneau ♿ garde ses libellés en dur, en français, et une page anglaise l'affiche donc en français. À traiter
  avec les langues, dans ce lot.
- Le tableau de bord du QCM charge `xlsx.full.min.js` depuis un CDN, contre le § 7. L'héberger demande l'accord de
  l'auteur pour le téléchargement.
- Les polices arabes sont déclarées, mais aucune page ne les emploie encore.

---

## 21 novembre 2026 · les objectifs toujours affichés, une seule copie du gabarit, le grand chantier cadré

### Les objectifs toujours affichés (`7591b19`)

**Demande de l'auteur** : les objectifs d'un chapitre restent toujours affichés. Le module « En-tête de chapitre
pliable » d'`interactions.js` repliait par défaut les objectifs, le podcast, les slides et la capsule derrière le
bandeau « Objectifs et ressources du chapitre ». Il est retiré, avec sa section d'`interactions.css`, ses six clés
`entete.*` par langue dans `ui-labels.js`, l'attribut `data-hors-repli` des capsules des trois chapitres et cinq
mentions de la documentation. Vérifié sur les trois chapitres, en français et en anglais, à 1280 et 375 px, en clair
et en sombre ; console vide. Le cours de veille garde ce module, si un cours en a besoin un jour.

### Une seule copie du gabarit (`95afe78`)

Le dépôt avait deux copies de travail au même commit : `C:\projets\Cours\template_cours`, où tout le travail depuis
le 26 octobre a été commité, et `C:\projets\template_cours`, qui ne recevait que des mises à jour mais gardait les
secrets. **Décision de l'auteur** : une seule copie, `C:\projets\Cours\template_cours`. Les secrets y sont déplacés
sans être ouverts (`outils/elevenlabs.json`, la version du 11 novembre, et `deploiement/config.json`), ignorés par
git et cachés par `.rgignore`. Le prompt paramétrable désignait l'autre copie, et son chemin est corrigé. L'autre
copie reste à supprimer par l'auteur.

### Le cadrage du grand chantier

**Demande de l'auteur** : une page d'accueil comme dans les cours, une documentation complète, des prompts optimisés,
un générateur de prompt pour lancer un nouveau cours (audio, cahiers de texte, import Livrables, illustrations par
Codex), un polycopié. Trois analyses en lecture seule des cours EADL/ERIS, CDWFS/ASRC et d'architecture logicielle
(secrets, banques d'épreuve et correction protégée jamais ouverts ; les trois dépôts vérifiés intacts ensuite), puis
treize questions, une à une. Les décisions de l'auteur et le plan en douze lots sont au registre (`TODO.md`, « Le
grand chantier »). Les points saillants :

- deux filières par défaut (EADL et ERIS, ou CDWFS et ASRC), ou une seule, au choix dans le prompt ;
- trois langues possibles, dont l'arabe, en site miroir à N langues, et une démo qui les montre toutes ;
- une capsule au début de chaque section, de l'accueil comme des chapitres ;
- la source unique des séances pour Yparéo et Livrables ;
- Codex lancé par Claude Code ;
- un générateur local, jamais publié ;
- six livrets.

### Ce que l'analyse a relevé en plus

- Les pages du gabarit chargent leurs polices depuis Google, contre le § 7 de `CLAUDE.md` : à corriger au lot 1.
- Dans le gabarit public, un `deploiement/destination.json` serait suivi par git et publierait le chemin du serveur.
  Il restera local.
- La typographie : une espace ordinaire précède souvent le deux-points, qui peut alors commencer une ligne à 375 px
  (chapitre 1). À proposer à l'auteur.

### Piège appris

- **Deux copies d'un même dépôt divergent en silence** : les secrets étaient dans l'une, le travail dans l'autre, et
  le prompt désignait la première. Un gabarit n'a qu'une copie de travail.

---

## 21 novembre 2026 · le gabarit sans tirets, lot S3 : les pages de ressources (`617017d`)

Les 104 tirets des neuf pages de ressources : `atelier` (40), `activites` (15), `about` (10), `polycopie` (10), `cours`
(9), `index` (6), `glossaire` (5), `polycopies` (5) et `podcasts` (4). Ponctuation seule, avec les choix du témoin :
deux-points pour un titre de section (« Checklist : mon chapitre est-il prêt à publier ? »), point médian pour un pied
de page ou un « Source · Titre » (« Le code · MIT », « Chapitre 1 · Cadrer son cours »), parenthèses ou point-virgule
pour une incise. Un titre d'onglet bilingue prend la barre oblique des chapitres (« Glossaire / Glossary »). Les mots des
dix fichiers sont identiques, contrôle fait mot à mot. `verifier_tirets.py` passe de 175 à 69 tirets dans `site/`.
Deux tableaux (l'atelier, puis les huit autres pages) ont été montrés à l'auteur avant application.

Le sous-titre du cours, que la page du polycopié reprend dans un bloc généré, se corrige à sa source :
`site/assets/js/course-data.js` (les deux tirets du lot S5) ; `generer_fragments.py` réécrit le bloc.

### Ce qui a été vérifié

- Les mots des dix fichiers, identiques ; `verifier_tirets.py` à 69 ; `generer_fragments` (le bloc du polycopié
  réécrit), `generer_nav_sections`, `glossaire_emplois`, `generer_playlist` et `generer_medias` à jour ;
  `verifier_i18n.py`, `verifier_liens.py` et `verifier_contraste.py` verts.
- Au navigateur, les neuf pages en français et en anglais : aucun tiret visible (texte et attributs), titres d'onglet
  à la barre oblique, console vide. Les libellés que les scripts ne montrent qu'à l'usage (verdicts de la checklist,
  liste « Où en parle-t-on ? » du glossaire) sont relus dans le code, pas à l'écran.

---

## 21 novembre 2026 · le gabarit sans tirets, lot S2 : les chapitres 2 et 3 (`14a944c`)

Les 74 tirets de `02-structurer.html` et `03-multimedia.html` (37 chacun), avec les choix du témoin : deux-points pour
un titre (onglet, podcast, point de contrôle, plan de l'exercice, légende de schéma), point médian pour un renvoi
« Pour approfondir » et pour le pied de page, virgule, parenthèses ou deux-points pour une incise. Seule la
ponctuation change : les mots des pages sont identiques, contrôle fait mot à mot. `verifier_tirets.py` passe de 249 à
175 tirets dans `site/`, ces deux chapitres à 0. Le tableau des remplacements a été montré à l'auteur avant
application.

Quatre phrases appartiennent aux transcriptions des capsules enregistrées des chapitres 2 et 3 (FR et EN). Comme au
témoin, seule leur ponctuation change, dans la fiche (`docs/prompts/Capsules_du_cours_demo.md`, blocs « Transcription
affichée ») ; `synchroniser_capsules.py` les reporte dans les pages, les scripts enregistrés ne changent pas.

### Piège rencontré

Les renvois français portent des espaces insécables (après « § » et « Chapitre », avant « ? ») : un remplacement
écrit avec des espaces ordinaires ne les trouve pas. Le script s'arrête avant d'écrire (un fichier n'est écrit que si
toutes ses paires ont été trouvées), puis repart avec les bons caractères.

### Ce qui a été vérifié

- Les mots des deux pages et de la fiche, identiques avant et après ; `verifier_tirets.py` à 175 ;
  `generer_fragments`, `generer_nav_sections`, `glossaire_emplois`, `generer_playlist` et `generer_medias` à jour ;
  `verifier_i18n.py`, `verifier_liens.py` et `verifier_contraste.py` verts.
- Au navigateur, les deux chapitres en français et en anglais : aucun tiret visible (texte et attributs), titre du
  point de contrôle et légende du schéma au deux-points, console vide.
- Pas fait : le livret du gabarit n'est pas régénéré.

---

## 21 novembre 2026 · le gabarit sans tirets, lot S1 : les moteurs partagés (`e8ea658`)

Les chaînes que l'apprenant lit dans les moteurs partagés, dont le chrome s'injecte dans toutes les pages :
`ui-labels.js` (26), `interactions.js` (6), `podcasts.js` (6), `media.js` (2) et `quiz.js` (1), plus le séparateur des
points de schéma du livret (`outils/polycopie/rendu.py`). `verifier_tirets.py` passe de 290 à 249 tirets dans `site/`,
ces cinq moteurs à 0. Les commentaires du code ne changent pas.

Pour les quatre moteurs que le cours de veille EADL partage avec le gabarit, ses choix déjà validés (D36 du cours) :
une incise entre virgules (« Avant de lire, que pensez-vous ? »), un deux-points (« Lecture continue : toutes les
étapes sont affichées. »), des parenthèses pour ce qui s'ajoute à un libellé (« (votre choix) », « (validée) »,
« (chapitre maîtrisé) »), le point médian entre deux éléments (« Chapitre terminé · 5 / 6 », « Podcast · chapitre
3 »). Pour `podcasts.js`, que le cours n'a pas, le point médian (« Diapositives · {e} »). Les points de schéma
deviennent « Titre : texte », sur la page comme dans le livret (espace insécable avant le deux-points en français).
Le tableau des 42 remplacements a été montré à l'auteur avant application.

### Ce qui a été vérifié

- `verifier_tirets.py` : 249 tirets dans 20 fichiers (les cinq moteurs à 0) ; `verifier_i18n.py`, `verifier_liens.py`
  et `verifier_contraste.py` verts ; la syntaxe des cinq scripts (`node --check`) et de `rendu.py`.
- Au navigateur, chapitre vitrine, en français et en anglais : aucun tiret visible (texte, titres, libellés pour
  lecteurs d'écran, textes de saisie) ; le retour d'un point de contrôle affiche « (votre choix) » et « Non · la
  bonne réponse est B » ; console vide.
- Pas vérifié : le livret n'a pas été régénéré (une ligne changée dans `rendu.py`).

---

## 21 novembre 2026 · deux défauts relevés par le cours de veille EADL

### Le prompt 15 ne prescrit plus le tiret cadratin (`a1a6a45`)

Sa règle typographique demandait « tiret cadratin pour une incise », contraire à l'exigence du 3 novembre 2026
(`CLAUDE.md`, « Le contenu ») : une incise passe maintenant entre virgules ou entre parenthèses. Ses exemples, que le
contenu généré imiterait, suivent le style validé au témoin (D55) : renvoi « § 3 · Le couplage » et « Auteur · titre »,
titre au deux-points, incise entre parenthèses. Plus aucun tiret dans le fichier ; c'est le premier fichier de
`prompts/` traité, avant le lot prévu par la série « Le gabarit sans tirets ».

### `--ecraser` garde les fichiers locaux du cours (`ad2c4a7`, décision de l'auteur)

Sur un dossier existant, `nouveau_cours.py --ecraser` supprimait en entier chaque dossier recopié, puis recopiait le
gabarit sans ses fichiers locaux : secrets, carnets d'envoi, destination, quarantaine des prises, cahiers de texte et
réglages locaux disparaissaient sans être remplacés (le cours de veille EADL y a perdu `deploiement/known_hosts`). La
liste `LOCAUX`, qui sert aussi aux exclusions de la copie, dit ce qui appartient au cours : ces fichiers passent le
temps de la copie dans un abri caché de la sortie elle-même, puis reviennent à leur chemin, nommés sans être ouverts ;
`--essai` les liste. Le reste du dossier est bien remplacé.

### Ce qui a été vérifié

- Sur un cours d'essai créé hors du gabarit (secrets réels exclus de l'essai, fichiers locaux factices) : sans
  `--ecraser`, la création refuse le dossier non vide ; `--ecraser --essai` liste les sept fichiers locaux ;
  `--ecraser` les garde intacts, supprime un fichier ajouté au cours sous `site/`, et ne laisse aucun abri. Le cours
  d'essai a été supprimé.
- Le prompt 15 : aucun tiret cadratin ni tiret moyen.

---

## 21 novembre 2026 · deux correctifs repris du cours de veille EADL

Nés le 20 novembre dans le cours « Veille technologique et innovation » (EADL), reportés à la demande de l'auteur.

### Le texte posé sur les fonds primaires, en thème sombre (`8a7d0db`)

En thème sombre, `--primary` s'éclaircit et le blanc posé dessus tombe sous 4,5 pour 1 (2,89 pour 1 en ardoise).
Deux variables de `main.css`, `--on-primary` et `--primary-hover`, laissent le thème clair à l'identique et donnent en
sombre la couleur inverse et un survol plus clair ; `components.css` s'en sert pour les boutons, les badges, le numéro
du chapitre actif et le lecteur audio. Les dégradés vers `--primary` (en-têtes de tableau, logo, bandeau d'accueil)
prennent en sombre un fond `--primary-dark`. `verifier_contraste.py` suit désormais les `var()`, ignore les
commentaires et contrôle ces paires dans les cinq palettes. Les trois fichiers du gabarit étaient identiques à ceux du
cours avant sa correction (D56 du cours) : le correctif s'applique tel quel, sans les feuilles du QCM propres au cours.

### Le cahier de texte sans identifiants (`7710d98`)

`python3 docs/generate_cahier_de_texte.py --sans-acces --site ADRESSE` produit le cahier avant que `docs/acces.json`
existe : la ligne des accès dit « Identifiant et mot de passe : communiqués par le formateur. » L'adresse vient de
`--site`, sinon de la constante `SITE` du classeur d'import (`import-application/generer_import.py`) quand le cours en
a un ; celle du QCM, de `--qcm`, sinon `QCM/index.html` du site. Sans fichier d'accès, le message propose l'option.
Adapté au gabarit : le cours lisait l'adresse dans son classeur d'import, que le gabarit n'a pas. Le module 07 le dit.

### Ce qui a été vérifié

- `verifier_contraste.py` : les cinq palettes conformes en clair et en sombre.
- Au navigateur (chapitre vitrine et accueil) : thème clair inchangé, blanc sur `--primary` à 11,65 pour 1 ; en sombre,
  `--on-primary` sur `--primary` à 5,37 pour 1, logo blanc sur `--primary-dark` à 6,90 pour 1 ; console vide.
- Le cahier de texte, écrit hors du gabarit : refus clair sans adresse ; avec `--site`, la ligne « communiqués par le
  formateur », aucun mot de passe, l'adresse complétée de sa barre finale ; adresse du QCM par défaut et explicite ;
  sans fichier d'accès, le message propose l'option. `docs/acces.json` n'a jamais été ouvert.

---

## 7 novembre 2026 — le gabarit sans tirets : le témoin (chapitre 1) et le plan de la série

Deuxième étape des exigences du cours d'avant-projet (D55), après le polycopié : réécrire sans tiret cadratin tout ce
que l'apprenant lit (`site/`, puis `CLAUDE.md` et `prompts/`). Un témoin d'abord, validé par l'auteur, puis une série
par lots ; à la fin, `outils/verifier_tirets.py` vert sur `site/`.

### Le témoin (`ea1cc23`)

Le chapitre vitrine (`site/chapitres/01-cadrage.html`, recopié en `_modele.html` dans chaque cours), de 47 tirets à 0.
Les choix de style, validés par l'auteur (règles D55) :

- une incise d'aparté passe entre virgules ou en parenthèses, une incise explicative prend un deux-points ; un titre
  de contrôle ou de figure prend un deux-points (que `couper_titre` lit) ; un renvoi « Source — Titre » prend le point
  médian « · » ; le compteur de slides « — / — » devient « · / · » ; une ligne de pied « Titre — Auteur » prend
  le « · ».
- Deux sources corrigées, qui nettoient tous les chapitres d'un coup : la légende de podcast « Épisode N — Titre »
  (`outils/podcasts.py`) et le libellé « Où en parle-t-on ? » « Chapitre N — Titre » (`outils/glossaire_emplois.py`)
  prennent le deux-points ; `glossaire-emplois.js`, `playlist-data.js` et les fragments régénérés.
- La transcription de la capsule (audio déjà enregistré) ne change que de ponctuation (le tiret-incise devient des
  parenthèses), dans sa fiche ; le script enregistré reste la référence (règle audio du § 2).

Le total `site/` tombe de 375 à 290.

### Un correctif trouvé en chemin (`55d362a`)

`outils/synchroniser_capsules.py` écrivait toujours en LF, convertissant une page CRLF sous Windows. Il garde
désormais les fins de ligne de la page, comme `generer_fragments` depuis le lot 1 (testé : CRLF reste CRLF, LF reste
LF).

### Ce qui a été vérifié

`01-cadrage.html` à 0 tiret (`verifier_tirets`), console vide, FR et EN au navigateur ; les huit contrôles du § 6
verts ; le sens et les nombres inchangés.

### Piège appris

- **Dé-tirer une page ne suffit pas à vider son rendu** : les moteurs partagés (`ui-labels.js`, `interactions.js`)
  injectent leur propre chrome (« Before reading — … », le séparateur « — texte » des points de schéma). La série
  doit inclure les moteurs et les données partagées, pas seulement les pages.

### La série, à faire

Les 290 tirets de `site/` en cinq lots (moteurs partagés ; chapitres ; pages de ressources ; QCM, avec la mise en
garde sur la signature SHA-256 des banques ; données), puis `CLAUDE.md` et `prompts/` (hors `verifier_tirets`). Détail
des lots : `TODO.md`, « Le gabarit sans tirets ».

---

## 7 novembre 2026 — la chaîne du polycopié : le chrome sans tirets, les capsules à venir (lot fc09f26)

Repris en générique du cours d'étude d'avant-projet (son commit `fc09f26`, décisions D55 et D56), choix de l'auteur
« tout fc09f26 en un lot » ; un seul commit après accord, un témoin avant/après.

- `9fc7dbc` — le chrome du livret sans tirets : la puce de 2e niveau « – » devient « ◦ » (`gabarit.py`) et la puce
  d'objectif « – » devient « • » (`pages.py`) ; `couper_titre()` lit « Libellé : sujet » là où le code coupait sur le
  tiret cadratin (`rendu.py`), et accepte l'espace insécable — fine ou non — avant le deux-points du français, ainsi
  que « Checkpoint: listening », sans couper « 9:00 » ; mentions, copyright et texte de la marge sans tirets
  (`libelles.py`, dans les deux langues) ; la table des matières et l'index en « (mettre à jour les champs) », la
  couverture en « titre · sous-titre » (`pages.py`) ; le surtitre des ouvertures en capitales dans le texte même
  (`.upper()` au lieu de la casse de Word, qui ôte l'accent de « LES MODÈLES »).
- Les capsules à venir (D56) : une capsule écrite mais pas encore enregistrée imprime son QR code à l'adresse où sa
  piste sera déposée (vérifiée contre sa fiche de production `docs/prompts/`, convention
  `chapitre-<N>-capsule-<langue>.mp3`), sans durée — celle de la page n'est qu'estimée ; `generer_polycopie.py
  --essai` compte « capsules à venir : N », qui tombe à 0 quand toutes les pistes sont là. `rendu.py`, `qr.py`,
  `generer_polycopie.py`.
- Écarté, propre au cours : `www.peoplecert.org` (sa bibliographie) et les composants de `lecture.py`, que le gabarit
  n'a pas.

### Comment ce lot a été vérifié

Un témoin du livret (chapitre 1) composé avant et après, sans Word (`--temoin --sans-pdf --hors-ligne`), et ses
tirets comptés dans le texte du Word : 17 avant, 12 après ; les 5 retirés sont exactement le chrome de `fc09f26`
(copyright, marge, table des matières, index), et la puce de niveau 2 passe bien à « ◦ ». Douze tests unitaires
(`couper_titre` et `capsule_prevue`), « capsules à venir : 0 » (les pistes de la démo existent), « règles du livret :
0 écart », les huit contrôles du § 6 verts.

### Ce qui reste

Les 12 tirets encore dans le témoin ne sont pas de ce lot : 7 viennent du corps des pages de démo, et 5 d'un chrome
que `fc09f26` ne touche pas — la légende de podcast « Épisode N — Titre » (`outils/podcasts.py`, hors
`outils/polycopie/`) et les puces de schéma « titre — texte » (`rendu.py`). Tout cela au lot « gabarit sans tirets ».

### Piège appris

- **Le corps du livret reprend le texte des pages** : tant que les pages gardent leurs tirets, le livret aussi. Un
  lot « livret sans tirets » n'enlève que le chrome du générateur ; le reste suit la réécriture du site.

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
