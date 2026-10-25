# Template de site de cours — contrat de travail

<!-- gabarit:debut -->
Ce dépôt sert à **fabriquer des sites de cours** : statiques, hors-ligne,
bilingues FR/EN, sans framework. Ce fichier est lu à chaque ouverture : il dit
ce qu'il faut savoir avant de toucher à quoi que ce soit. `nouveau_cours.py` le
recopie dans chaque cours créé, sans ses passages propres au template : les
exigences de l'auteur (§ 2) s'y appliquent de la même façon.
<!-- gabarit:fin -->

---

## 1. La règle qui prime sur toutes les autres

**Ne jamais inventer de contenu pédagogique.**

Les documents de référence déposés dans `sources/` sont la source de vérité. Ce
qui n'y figure pas est signalé comme absent — jamais comblé par une formulation
plausible. Un cours faux et crédible est le pire résultat possible : l'apprenant
ne peut pas le détecter, et il l'apprend.

Concrètement :

- Lire `sources/` **avant** de poser la moindre question de cadrage.
- Citer la source de chaque affirmation qui en vient (titre, section, page).
- Signaler les lacunes et les contradictions entre sources plutôt que trancher
  en silence.
- Tenir `sources/bibliographie.md` à jour au fur et à mesure, pas à la fin.
- Ne jamais reproduire le texte ni les figures d'un ouvrage : on reformule, on
  cite, on renvoie.

`sources/` est exclu du dépôt — droit d'auteur. Seuls son mode d'emploi et la
bibliographie sont versionnés.

---

## 2. Les exigences de l'auteur

Elles viennent de demandes explicites, faites cours après cours. Elles valent
dans ce dépôt comme dans chaque cours créé, et priment sur les habitudes par
défaut de l'outil.

### Le dialogue

- **Une question à la fois**, posée avec l'outil de question à options
  cliquables (AskUserQuestion) — jamais une liste de questions dans le texte.
  Deux à quatre options, la recommandation en premier.
- **Chaque étape se termine par une question cliquable** sur la suite.
- Tout en français : messages, documents, commits.
- Dire ce qui a été fait **et ce qui ne l'a pas été** ; un test qui échoue se
  rapporte avec sa sortie.
- **Un exemple avant la série** : une transformation répétée — mise en forme,
  liens, QR codes, capsules — se montre d'abord sur un cas ; elle ne se
  généralise qu'après l'accord de l'auteur.
- Quand l'auteur doit déposer des fichiers (audio, PDF exportés d'un autre
  outil), lui donner **le nom exact et le dossier exact** de chacun.
- Ce que l'auteur demande de garder pour plus tard va dans le registre
  **`TODO.md`**, à la racine, daté ; « ce qui reste à faire » se répond à partir
  de lui.

### Git

- Commits au seul nom de l'auteur :
  `Mohamed Amine EL AFRIT <elafrit.mohamed@gmail.com>`. **Jamais** de ligne
  `Co-Authored-By`, jamais de mention d'un outil ou d'une IA — même quand
  l'outil propose une attribution par défaut.
- Vérifier `git config user.name` et `git config user.email` avant chaque
  commit.
- `git add` par chemins explicites, jamais `git add -A` ni `git add .`.
- **Demander avant de commiter et de pousser**, puis, séparément, **avant de
  mettre en ligne**. Un accord vaut pour l'action demandée, pas pour la suivante.
- Un dépôt qui contient de l'évaluation (sujets, corrections, QCM papier) reste
  **privé**. Le template, lui, est public : y pousser, c'est publier.

### Les secrets

- **Ne jamais lire, afficher ni demander** le contenu de
  `outils/elevenlabs.json`, `deploiement/config.json`, `docs/acces.json`,
  `docs/acces-zones.json`, ni d'aucune copie (`*.config.json`). Les scripts s'en
  servent sans que Claude les voie.
- Le fichier **`.rgignore`** les cache aux recherches : l'outil de recherche de
  Claude Code ignore le `.gitignore`, pas ce fichier. Tout nouveau secret s'y
  ajoute. Un filtre de fichiers explicite (`*.json`, `*.{md,json}`) passe outre
  le `.rgignore` : une recherche qui inclut les `.json` exclut les secrets
  nommément (`!**/config.json`…), ou ne se fait pas.
- Pour un nouveau cours, ils se **recopient tels quels**, octet pour octet,
  depuis le template — `nouveau_cours.py` le fait, et seulement si le
  `.gitignore` du cours les exclut. Ils ne vont jamais dans Git.
- Ne jamais s'authentifier soi-même sur le site en ligne avec des identifiants :
  l'auteur teste dans son navigateur.

### Le contenu

- Aucune **date fixe** dans le contenu : « Jour 1 », « séance 2 ». Les dates
  réelles ne servent qu'aux outils de planning.
- **Rien ne souffle une réponse** : un exemple de méthode porte sur un cas
  neutre ; les réponses d'un TP ne vivent que dans sa correction, placée dans
  une zone protégée par mot de passe.
- Les **interdits propres au cours** — mots du sujet de TP, exemples à éviter —
  sont listés dans sa fiche de cadrage et contrôlés par ses générateurs.
- Typographie française : espace insécable avant `: ; ? !` et à l'intérieur des
  guillemets `« »`.
- **Une faute de français** relevée en chemin n'est jamais corrigée en
  silence : elle est proposée à l'auteur, puis corrigée dans un commit séparé —
  et dans l'autre langue si la même erreur s'y trouve.

### La pédagogie

- **Tout schéma a son explication élément par élément**, écrite pour un
  débutant : ce qu'il montre, comment le lire, chaque élément et son rôle, ses
  liens avec les autres pièces, le piège à éviter.
- **Toute question à choix** — point de contrôle, mini-quiz, QCM
  d'entraînement — explique pourquoi la bonne réponse est juste **et pourquoi
  chacune des autres ne l'est pas**, puis donne **deux à quatre renvois**
  « Pour approfondir » vers l'endroit exact du cours, ou vers une référence
  externe vérifiée. Voir `prompts/15_explications_quiz.md`.
- **Liens externes** : `target="_blank" rel="noopener noreferrer"`, signalés aux
  lecteurs d'écran ; chaque adresse est ouverte et vérifiée avant d'être
  ajoutée.

### L'audio

- **Eleven v4** pour toutes les pistes, avec la voix clonée de l'auteur et
  l'**accent parisien marqué** (« strong Parisian French accent », ajouté par
  `outils/generer_audio.py` aux balises des pistes françaises).
- Ton **pédagogique, académique, professionnel et motivant**, au vouvoiement.
  Une capsule explicative définit la notion, lit l'exemple élément par élément,
  relie aux autres pièces, finit par le piège et la phrase à retenir — avec
  « speaking slowly » dans ses balises.
- **Un témoin d'abord**, écouté par l'auteur ; la série ensuite. Voir
  `prompts/14_capsules_audio.md`.

### Les outils externes

- **Un prompt destiné à un autre outil** (NotebookLM, traduction…) se livre dans
  un fichier `.md` de `docs/prompts/`, pas seulement dans la conversation.
  Limites de NotebookLM, espaces et retours à la ligne compris : **4 800
  caractères** pour un prompt d'audio, **3 700** pour un diaporama. La longueur
  se compte par script, avec une marge : à la copie, un retour à la ligne peut
  valoir deux caractères. Une série est enchaînée : chaque épisode rappelle le
  précédent et annonce le suivant. Voir `prompts/10_notebooklm_18prompts.md`.
- **Ce qu'un outil externe produit se relit avant publication** — podcast,
  diaporama, traduction : chiffres ou exemples inventés, propos prêtés aux
  personnages du cas, QR codes factices, coquilles. Chaque export corrigé se
  revérifie en entier : une correction peut se perdre d'un export à l'autre.

### La publication

- `deploiement/destination.json` dit où va **ce** cours ; le déployeur refuse un
  dossier qui appartient à un autre cours, et ne lit jamais le répertoire
  distant de `config.json`.
- Ne partent que les fichiers de `site/` suivis par Git : jamais les sources,
  les outils, la documentation de production ni les secrets.
- Une zone protégée ne reçoit son contenu qu'après sa protection
  (`deploiement/proteger_zones.py`).
- Toute mise en ligne commence par un **essai à blanc** (`--essai`). La sortie
  du déployeur ne montre ni l'hôte, ni le port, ni le répertoire distant ; une
  commande qui en afficherait se filtre avant d'arriver à l'écran.
- Après la mise en ligne, **le site se contrôle en ligne** : les pages
  publiques répondent 200, les zones protégées 401 — sans s'authentifier.

### La vérification

- Ce qui se voit se vérifie au navigateur : thème clair et sombre, 1280 et
  375 px, console vide. Quand l'onglet intégré n'affiche rien, un navigateur
  sans interface (Edge ou Chrome, `--headless`) fait les captures.
- Sous Windows : un correctif se scripte dans un fichier `.py` (pas d'heredoc à
  antislashs), la console se met en UTF-8 (`PYTHONIOENCODING=utf-8`), et aucun
  octet NUL ne doit entrer dans un fichier modifié.
- Un travail confié à des sous-agents part avec une consigne écrite complète, et
  ne s'accepte qu'après un contrôle automatique.

### Les pièges de production

- Les générateurs se lancent **dans l'ordre** (§ 4) : un générateur qui lit la
  sortie d'un autre, lancé trop tôt, fige un état périmé.
- **Un seul export à la fois** quand un script pilote une application (Word, un
  navigateur sans interface) : deux exports simultanés se marchent dessus. Un
  PDF exporté se contrôle, langue déclarée comprise (`/Lang`), que l'export ne
  pose pas toujours.
- **Un schéma validé ne se rend pas de nouveau sur un autre poste** (PlantUML,
  Mermaid…) : la version de l'outil et les polices changent le rendu. On le
  régénère là où il a été validé, ou on le fait revalider.
- **Aucun nom ne diffère d'un autre par la seule casse** (`Polycopie/` et
  `polycopie/`) : Windows les confond, le serveur les distingue — une exclusion
  ou un lien juste en local devient faux en ligne.

### Le journal du cours

- Chaque choix structurant devient une décision numérotée (D01, D02… : la
  question, le choix, la raison) dans `docs/01-Decisions-de-conception.md` ;
  l'état d'avancement se tient dans `docs/02-Etat-d-avancement.md`.

---

<!-- gabarit:debut -->
## 3. Démarrer un cours

```bash
cp cours.exemple.json cours.json     # puis le remplir
python3 nouveau_cours.py --essai     # ce qu'il ferait, sans rien écrire
python3 nouveau_cours.py             # crée le cours dans le dossier « sortie »
```

Le script met en place la mécanique — arborescence, charte, navigation,
squelettes, outils, déployeur, `CLAUDE.md`, `deploiement/destination.json` — et
recopie en local les secrets communs (§ 2). **Il ne rédige aucun contenu.** Le
contenu vient ensuite, par la skill `creer-cours-template`, qui suit
`prompts/PROMPT-Cours-parametrable.md` et ses modules (`prompts/modules/`) :
cadrage d'abord, questions **une à une**, rien de produit avant validation
explicite.

---

<!-- gabarit:fin -->

## 4. Ce qui ne se modifie pas à la main

Ces fichiers sont **générés**. Les éditer, c'est perdre le travail à la
prochaine régénération.

| Fichier | Produit par | Source réelle |
|---|---|---|
| `site/assets/js/playlist-data.js` | `outils/generer_playlist.py` | les pages et les fichiers audio |
| `site/assets/js/nav-sections.js` | `outils/generer_nav_sections.py` | les titres `<h2 id>` des chapitres |
| transcriptions des capsules | `outils/synchroniser_capsules.py` | `docs/prompts/Capsules_*.md` |

**L'ordre compte.** `generer_playlist.py` indexe les pages et les fichiers
audio réels : il passe après `synchroniser_capsules.py` et `generer_audio.py`.
`generer_nav_sections.py` se relance après tout ajout, retrait ou renommage de
section — `nouveau_cours.py` le lance à la création du cours.

Une capsule vit à deux endroits — le script balisé et la transcription lisible.
Tenues à la main, elles divergent dès la première correction, et personne ne
s'en aperçoit : on ne lit pas la transcription d'une capsule qu'on vient
d'écouter. **La fiche est la source unique.**

---

## 5. Le contrat bilingue

Trois mécanismes, selon la nature du texte.

**Contenu rédigé** — blocs jumelés dans le HTML, le CSS masque la langue
inactive :

```html
<span data-tr="fr">Bonjour</span><span data-tr="en">Hello</span>
```

**Interface fabriquée en JavaScript** — dictionnaire unique
`site/assets/js/ui-labels.js`, appelé par `T('cle')`. Ne jamais écrire un
libellé en dur dans un moteur : un dictionnaire éparpillé est un dictionnaire
dont on oublie une clé.

**Contenu des composants d'une page** — objet `TEXTES = { fr, en }` dans la
page, et une fonction `monter()` qui vide les conteneurs puis remonte, rejouée
sur `tpl:langchange`. Les moteurs `RDCX` reçoivent des chaînes et ignorent le
bilingue : c'est ce qui les garde simples. Modèle complet dans `_modele.html`.

**Audio bilingue** : un seul appel `RDCX.voice`, mais une source par langue,
déclarée dans `TEXTES` sous `capsuleSrc`. Convention de nommage :
`chapitre-<N>-capsule-<langue>.mp3`. Sans le suffixe, l'auditeur anglophone
entend du français — et la piste reçoit l'accent parisien des pistes françaises.

---

## 6. Vérifier

Cinq contrôles, à lancer souvent. Ils attrapent ce que l'œil ne voit pas.

```bash
python3 outils/verifier_i18n.py       # clés dépareillées, blocs data-tr déséquilibrés
python3 outils/verifier_contraste.py  # palettes lisibles en clair ET en sombre
python3 outils/verifier_liens.py      # href, src et renvois « Pour approfondir » qui ne mènent nulle part
python3 outils/generer_nav_sections.py --essai  # le menu suit-il les <h2 id> des chapitres ?
python3 demarrer.py                   # le site, sans cache
```

`demarrer.py` sert `site/` et envoie `Cache-Control: no-store`. C'est
volontaire : avec un serveur ordinaire, le navigateur ressert l'ancien
JavaScript après une modification, et l'on cherche un défaut qui n'existe pas.

**Si un changement JavaScript ne semble pas prendre**, changez de port plutôt
que de recharger : certains navigateurs gardent le script en cache malgré
l'en-tête.

Après toute modification du déployeur : `python3 deploiement/tester_deployer.py`
(hors ligne, faux serveur).

<!-- gabarit:debut -->
Ces contrôles mesurent ce qui est mesurable : des clés, des contrastes, des
chemins.
Ils ne disent rien du seul défaut qui compte vraiment ici — **un cours créé qui
hérite du contenu de la démonstration**. Cela ne se voit qu'en générant :

```bash
python3 nouveau_cours.py --essai      # dit ce qu'il ferait, n'écrit rien
```

Après toute modification du moteur ou du générateur, déroulez
`docs/RECETTE.md` en entier. Son troisième test est le seul qui dise ce que
l'utilisateur recevra réellement.

<!-- gabarit:fin -->
---

## 7. Conventions à ne pas enfreindre

- **Statique et hors-ligne.** HTML, CSS et JavaScript nus. Aucun framework,
  aucune dépendance à un CDN, aucun appel réseau au chargement.
- **Copier depuis le chapitre vitrine.** `site/chapitres/_modele.html` est le seul
  endroit où tous les composants sont appelés pour de vrai, avec le motif
  bilingue : on copie depuis là plutôt qu'écrire de mémoire.
- **Charte commune, accent par cours.** La teinte se choisit dans `cours.json`
  parmi les palettes de `palettes.css`, toutes vérifiées en contraste. Ne pas
  inventer une couleur sans relancer `verifier_contraste.py`.
- **Rien de propre à une matière dans un moteur.** Les termes du glossaire, les
  libellés métier, les listes de notions vivent dans les données. Un moteur qui
  parle d'une matière rend le template inutilisable pour les autres.
- **Accessibilité.** Texte alternatif sur chaque image, transcription sous
  chaque capsule, contraste vérifié, navigation au clavier. Ce n'est pas une
  faveur faite à une minorité : cela rend la ressource utilisable dans plus de
  situations.
- **Jamais de secret dans le dépôt.** Clé API ElevenLabs, accès à
  l'hébergement, mots de passe des zones protégées, documents sous droits : tous
  exclus par `.gitignore`. L'historique Git ne s'efface pas.
- **Ne jamais attribuer le contenu à une IA.** Le cours est signé par son
  auteur.
- **Anonymat des copies.** Si le cours produit des livrables étudiants, aucun
  nom ni prénom : ni dans le texte, ni dans le nom de fichier, ni dans les
  métadonnées.

---

## 8. Où chercher le détail

| Question | Fichier |
|---|---|
| Créer un cours de bout en bout, avec ses paramètres | `prompts/PROMPT-Cours-parametrable.md` |
| Ajouter une option : anglais, polycopié, podcasts, audio… | `prompts/modules/` (un fichier par option, utilisable seul) |
| Comment fabriquer un cours, pas à pas | `docs/GUIDE.md` |
| Rôle de chaque fichier et de chaque moteur | `docs/ARCHITECTURE.md` |
| Le bilingue en profondeur | `docs/I18N.md` |
| Les pratiques et leurs raisons | `docs/BONNES_PRATIQUES.md` |
| Ce qu'il reste à faire avant de livrer | `docs/CHECKLIST.md` |
| Vérifier que le gabarit lui-même fonctionne | `docs/RECETTE.md` |
| Écrire les capsules audio (Eleven v4) | `prompts/14_capsules_audio.md` |
| Expliquer chaque proposition d'un quiz | `prompts/15_explications_quiz.md` |
| Publier, protéger une zone | `deploiement/LISEZMOI.md` |
| Les prompts de production | `prompts/` |
| Les skills et le pipeline | `.claude/skills/README.md` |

---

## 9. Comment travailler ici

- **Vérifier plutôt qu'affirmer.** Ce dépôt fournit des vérificateurs : les
  lancer coûte quelques secondes et évite des heures.
- **Une modification, une vérification.** Un moteur retouché se teste au
  navigateur, pas seulement à la relecture.
- **Dire ce qui a été fait et ce qui ne l'a pas été.** Un travail annoncé
  terminé qui ne l'est pas coûte plus cher qu'un travail annoncé partiel.
- **Les commentaires expliquent le pourquoi**, pas le comment. Le code dit déjà
  ce qu'il fait ; ce qu'il ne dit pas, c'est le piège qu'on a rencontré et la
  raison du choix.
