# Journal du gabarit

> Ce qui a été fait sur le gabarit, session par session, avec ses commits. Ce qui reste à faire est dans
> [`TODO.md`](TODO.md), le registre, à lire en premier à la reprise du travail. Les deux fichiers, à la racine, ne
> partent jamais dans un cours créé : `nouveau_cours.py` ne recopie de la racine que ce que liste `COPIER` — alors que
> tout `docs/` part dans chaque cours.
>
> « Décision de l'auteur » signale un choix tranché par l'auteur ; le reste découle des règles de `CLAUDE.md` (§ 2).

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
