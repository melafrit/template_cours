# Recette du gabarit

**Quand l'utiliser :** à la réception du template (nouveau poste, nouvelle
machine, `git pull` important) et après toute modification du moteur. Comptez
vingt minutes.

Ne pas confondre avec [CHECKLIST.md](CHECKLIST.md), qui accompagne la
**fabrication d'un cours**. Celle-ci vérifie le **contenant** : que le gabarit
fonctionne, et surtout qu'il produit un cours propre.

Les trois tests vont du plus rapide au plus important. Le troisième est le seul
qui vous dise ce que vous recevrez réellement en démarrant un nouveau cours.

---

## 0. Lancer

Depuis le Finder, **double-cliquez `demarrer.command`** : le bit exécutable est
enregistré dans Git, il n'y a pas de `chmod` à faire. En ligne de commande :

    ./demarrer.command      # macOS
    demarrer.bat            # Windows
    python3 demarrer.py     # partout

Le serveur écoute sur `http://localhost:8765/index.html`, sert le dossier
`site/`, et ouvre le navigateur seul. Si le port est occupé il essaie les
suivants : l'URL réelle est affichée dans le terminal. `Ctrl+C` pour arrêter.

Le serveur envoie `Cache-Control: no-store` et répond en parallèle. Ces deux
points ont chacun coûté une séance de débogage : un onglet resté ouvert gelait
tous les autres clients, sans le moindre message.

---

## 1. Le site de démonstration · à l'œil

Le site parle de lui-même : son sujet est « concevoir un cours en ligne ».
C'est voulu. Vous lisez le mode d'emploi en testant le contenant.

- [ ] **Accueil** : le bouton « commencer » mène au chapitre 1. Ce lien n'est
      pas écrit dans la page : `navigation.js` le calcule depuis
      `course-data.js`. S'il tombe juste, le mécanisme qui protège les cours
      créés fonctionne. 🔴
- [ ] **Chapitre 1** : la vitrine. Les **sept composants interactifs** y sont
      tous : point d'étape, révélation, chasse à l'erreur, appariement,
      embranchement, points chauds, prise de parole. Plus une capsule audio, un
      schéma et un polycopié.
- [ ] **Chapitres 2 et 3** : structure d'un chapitre rédigé. Le 3 porte le
      podcast.
- [ ] **Glossaire**. Survolez un terme souligné dans un chapitre : l'info-bulle
      s'affiche, et le lien « voir dans le glossaire » fonctionne depuis
      `/chapitres/` comme depuis la racine.
- [ ] **Polycopiés** : six PDF. Chacun est testé par une requête HEAD avant
      affichage : un bouton visible est un fichier qui existe.
- [ ] **Activités** : trois patrons réutilisables, douze contrôles.
- [ ] **QCM** : entraînement, correction, tableau de bord.
- [ ] **Pied de page** : « À propos du template » est atteignable.

### Le test qui casse tout d'un coup

- [ ] Basculez **FR/EN** en haut à droite, sur le chapitre 1. Tout doit suivre :
      titres, prose, boutons, **et** les libellés fabriqués en JavaScript (la
      barre d'étapes, les activités, les messages de correction). 🔴

C'est là que l'i18n lâche d'habitude, parce qu'un libellé écrit une fois à la
construction ne se repeint pas tout seul. La barre d'étapes est restée en
français sur une page anglaise pendant des semaines : l'élément le plus visible
du chapitre.

- [ ] **Console vide** (⌥⌘I). Un 404 de favicon suffit à faire perdre
      l'habitude de la regarder.
- [ ] **Thème sombre** et **affichage téléphone** : le menu passe en tiroir.
- [ ] **Sections longues sur téléphone** : à 375 px, la plus longue section du cours
      apparaît dès qu'on y arrive en défilant (aucun bloc ne reste vide).

---

## 2. Les vérificateurs · automatique, trente secondes

    python3 outils/verifier_i18n.py

Quatre contrôles : clés appariées dans les deux langues, clés appelées par les
moteurs, égalité des blocs `data-tr` page par page, concordance des titres entre
le menu et les pages. Doit finir sur **« Bilingue cohérent »**.

    python3 outils/verifier_contraste.py

Les cinq palettes, en thème clair **et** sombre, contre les seuils WCAG :
4,5:1 pour le texte courant, 3:1 pour le grand texte et le non-texte. Doit
passer sans échec : c'est ce test qui a rattrapé deux couleurs illisibles de la
palette marine, en place depuis deux ans.

    python3 outils/verifier_liens.py

Tous les `href` et `src` qui désignent un fichier du site, et les renvois
« Pour approfondir » des points de contrôle (fichier **et** ancre). Doit finir
sur **« Aucun lien mort »**. C'est le contrôle le plus rentable du lot : quatre
familles de liens différentes ont, tour à tour, survécu à la génération en
pointant vers les chapitres de la démonstration.

    python3 deploiement/tester_deployer.py

Le garde-fou d'identité, les protections du serveur et les zones protégées,
rejoués hors ligne contre un faux serveur : aucune connexion, aucun envoi. Doit
finir sur **« Tous les cas sont conformes »**.

    python3 outils/generer_audio.py --essai --force

La chaîne audio sans dépense, si `outils/elevenlabs.json` est en place : modèle
**eleven_v4**, accent sur les pistes françaises seulement (« sans accent ajouté »
sur les anglaises), la capsule arabe du chapitre 1 en attente (de son script, puis
de sa voix `voix_id_ar`), et le rappel du témoin avant toute série.

- [ ] Au chapitre 1, répondez faux au point de contrôle : l'explication nomme la
      bonne réponse, dit **pourquoi chaque autre proposition** ne convient pas,
      marque « votre choix », et propose des renvois « Pour approfondir » (le
      lien Wikipédia s'ouvre dans un nouvel onglet). En anglais aussi.

---

## 3. Générer un cours vide · le test qui compte 🔴

Tous les défauts sérieux de ce dépôt se sont logés ici : un cours créé héritait
des médias de la démonstration, de sa prose, de ses liens. Rien de tout cela ne
se voit en lisant le gabarit. Il faut générer.

    cp cours.exemple.json cours.json
    python3 nouveau_cours.py --essai

- [ ] **Le script doit refuser**, en nommant `slug` et `auteur` restés sur les
      valeurs du modèle. C'est le premier contrôle : le générateur n'invente
      rien, pas même un nom de dossier. 🔴

Renseignez ces deux champs dans `cours.json`, puis :

    python3 nouveau_cours.py --essai      # n'écrit rien, dit ce qu'il ferait
    python3 nouveau_cours.py

Le cours atterrit dans `../mon-cours`. **Avec les trois chapitres du modèle,
la sortie doit annoncer :**

    arborescence copiée (16 entrées)
    langues-data.js : aucune page traduite pour l'instant
    CLAUDE.md écrit : les exigences de l'auteur s'appliquent à ce cours
    contenu de démonstration retiré : 21 média(s), 13 fichier(s) remis à l'état de squelette
    bloc école : 2 bouton(s), 0 filière(s) avec épreuves, 1 session(s)
    14 page(s) renommée(s) au nom du cours
    5 fichier(s) recousu(s) sur les chapitres déclarés
    cours.html : 3 carte(s) de chapitre régénérée(s)
    filieres.css : 2 filière(s), à jour
    deploiement/destination.json écrit (cours « … »)
    outils/elevenlabs.json     copié en local, ignoré par Git (contenu non affiché)
    deploiement/config.json    copié en local, ignoré par Git (contenu non affiché)

Les chiffres des recousages et des cartes suivent le nombre de chapitres
déclarés : une carte par chapitre, et un recousage par chapitre plus les deux
pages qui les citent (sommaire, chapitre vitrine). L'accueil, lui, naît avec ses
liens. Les 21 médias (dont les deux fiches de capsules de la démonstration) et les
13 squelettes (dont l'accueil, ses boutons, son programme et ses sessions,
l'atelier et les activités, vidés de leur démonstration), eux, ne bougent pas.
La ligne de `filieres.css` suit les filières de `cours.json` : « à jour » avec
celles du modèle (ce sont celles de la démonstration), « écrit » avec d'autres.
Une seule filière, ou aucune, ne donne pas de bascule.
Les deux dernières lignes disent « absent du template » si vos secrets n'y sont
pas : c'est le cas d'un dépôt fraîchement cloné (§ 4).

Puis, sur le cours produit :

    python3 outils/verifier_liens.py --site ../mon-cours/site

Et, pour les secrets, sans les ouvrir :

    cd ../mon-cours && git init -q
    git check-ignore -v outils/elevenlabs.json deploiement/config.json   # deux lignes attendues
    sha256sum ../template_cours/outils/elevenlabs.json outils/elevenlabs.json   # empreintes identiques

- [ ] Les deux secrets sont **ignorés par Git** dans le cours créé, et leurs
      empreintes égales à celles du template. 🔴
- [ ] `CLAUDE.md` du cours porte son titre et **aucun** passage propre au
      template (`grep -c "gabarit:" CLAUDE.md` rend 0).
- [ ] `deploiement/destination.json` porte le slug du cours et le répertoire de
      `cours.json` (bloc `publication`), ou la valeur du modèle, que le
      déployeur refusera tant qu'elle n'est pas remplacée.
- [ ] `python3 deploiement/tester_deployer.py` finit sur « Tous les cas sont
      conformes ».
- [ ] **Aucun dossier `site/en/` ni `site/ar/`** dans le cours, et
      `site/assets/js/langues-data.js` ne nomme aucune page : les jumelles du
      cours viennent ensuite, avec `outils/creer_jumelle.py`. Chaque page déclare
      la langue racine (`<html lang="fr" data-lang="fr" data-langues="fr">`). 🔴

Le cours créé embarque son propre lanceur. Ouvrez-le :

    cd ../mon-cours && python3 demarrer.py

- [ ] Le site est **complet et fonctionnel**, et **entièrement vide de
      contenu**. 🔴
- [ ] **Aucune** capsule audio, **aucun** PDF, **aucun** schéma de la
      démonstration.
- [ ] Les chapitres sont des squelettes, appels de composants en commentaire.
- [ ] Le bouton « commencer » de l'accueil mène au premier chapitre déclaré.
- [ ] L'accueil a la structure de celui de la démonstration (bandeau, capsules,
      sections numérotées, cartes des chapitres, bouton flottant), le titre et le
      sous-titre de `cours.json`, des consignes « À rédiger » à la place de la
      prose, et pas de section « Ce que démontre ce site ». Son bandeau a les deux boutons du
      bloc école du modèle, « Déposer mes livrables » et « QCM d'évaluation »,
      écrits dans `outils/accueil.py`. Sa pastille dit « À rédiger : le public du
      cours », sans bloc ni bouton d'épreuves : les filières du modèle n'en
      déclarent pas, et `outils/seances.py` part avec `FILIERES = {}`.
- [ ] Le programme et les échéances de l'accueil disent « À rédiger dans
      `outils/seances.py` » : le cours part sans séance ni livrable, et
      `python3 outils/seances.py` le dit cohérent ; `outils/sessions.py` reçoit
      la session d'exemple du modèle (`promo-2027`), dont le script rappelle,
      avant la création, qu'elle garde des valeurs fictives ;
      `python3 outils/generer_cahier_de_texte.py` répond qu'il
      n'y a encore aucune séance à mettre au cahier, et
      `python3 outils/generer_classeur_livrables.py` aucune à mettre au classeur.
- [ ] Les filières de `cours.json` (EADL et ERIS dans l'exemple) donnent la bascule
      de l'en-tête et le bandeau « Quelle est votre filière ? » ; une filière
      choisie prend sa palette. Avec `"filieres": []`, ni bascule ni bandeau.
- [ ] Le QCM est réduit à deux questions génériques.
- [ ] Le pied de page ne renvoie plus vers « À propos du template ».
- [ ] **L'onglet du navigateur porte le titre de VOTRE cours**, sur chaque
      page, de même que la méta-description, l'auteur des métadonnées et la
      ligne d'auteur du pied de page. 🔴
- [ ] `verifier_liens.py` finit sur « Aucun lien mort ».

- [ ] L'en-tête porte le **nom court** du cours et son pictogramme, le pied de
      page **sa** licence ; chaque chapitre a ses boutons « ← Précédent » et
      « Suivant → » vers les chapitres déclarés, titres compris.
- [ ] Console vide sur un chapitre squelette, sans aucune erreur 404 : la
      liste des médias (`media-data.js`) part vide, et `media.js` ne demande
      rien ; ni barre d'étapes ni sommaire dans la page, les sections du
      chapitre en sous-entrées dans le menu de gauche.

**Toute trace du cours « concevoir un cours en ligne » dans `../mon-cours` est
un défaut.** Y compris un titre d'onglet, une méta-donnée, un attribut, le nom
de l'en-tête, un titre de chapitre dans une pagination. La seule exception est
`site/chapitres/_modele.html`, le chapitre vitrine gardé comme référence : il
conserve volontairement ses exemples de composants.

Le contrôle en une ligne, depuis le dossier du cours créé :

    grep -rilE "concevoir un cours|design a course|Ce que démontre|Concevez votre propre|format d'évaluation|cours-démo|Structurer le contenu|Cadrer son cours|Créer les ressources|hreflang=.x-default" site/ | grep -v _modele

Il ne doit rien retourner. La dernière forme, `hreflang=.x-default`, attrape un bloc
`hreflang` resté de la démonstration, qui annoncerait ses adresses.

### 3 bis. Le même cours, en anglais

Un cours dont la langue racine est l'anglais part des jumelles anglaises de
la démonstration, remontées à la racine (`miroir.remonter`). Mettez
`"langues": ["en"]` dans `cours.json`, régénérez (`--ecraser`), puis :

    grep -rho '<html[^>]*>' --include=*.html site | sort | uniq -c   # lang="en" et data-langues="en" partout
    grep -rilE "Designing an online course|Scoping your course|Structuring the content|Creating the resources|What this site demonstrates|demo course|hreflang=.x-default" site/ | grep -v _modele

- [ ] Chaque page est en anglais et le déclare ; aucun bouton de langue. 🔴
- [ ] Le contrôle des traces ne retourne rien. Seuls les dictionnaires des
      scripts du QCM gardent du français : ils portent les deux langues, et le
      moteur y prend l'anglais.
- [ ] `verifier_liens.py` finit sur « Aucun lien mort » : les pages remontées
      mènent bien aux fichiers partagés.

---

## 4. Deux pièges à connaître

**Le cache du navigateur.** Le serveur envoie `no-store`, et malgré ça un
navigateur peut servir un vieux fichier JavaScript, même dans un onglet neuf.
Si une correction ne s'affiche pas, ne cherchez pas dans le code : relancez sur
un autre port.

    python3 demarrer.py --port 8790

**Les fichiers à secrets sont absents d'un dépôt fraîchement cloné**, et c'est
voulu : `outils/elevenlabs.json` porte votre clé API et votre voix,
`deploiement/config.json` vos accès à l'hébergement, `docs/acces.json` ceux du
site de cours. Aucun n'entre au dépôt. Sur votre poste, le template en garde la
**copie de référence** : `nouveau_cours.py` la recopie dans chaque nouveau cours.
Sur un poste neuf, déposez-les une fois dans le template (à partir des modèles
`*.exemple.json`), jamais dans une conversation.

**Le template ne se déploie pas.** Il n'a pas de `deploiement/destination.json` :
le déployeur refuse donc d'envoyer quoi que ce soit depuis ici. C'est voulu : son
site de démonstration n'a rien à faire sur votre hébergement, et votre
`config.json` vise un serveur où vivent de vrais cours.

---

## Si un test échoue

| Symptôme | Où regarder |
|---|---|
| Un lien mène nulle part dans un cours créé | `recoudre_liens()` dans `nouveau_cours.py` |
| Un lien « abîmé » (son début a disparu) | une substitution par motif dont le remplacement commence par un chiffre : `\1` suivi de `01-…` devient un octal ; écrire `\g<1>` ou une fonction |
| Un cours garde des pages de la démonstration sous `en/` ou `ar/`, ou une page dans une autre langue que sa racine | la langue racine dans `main()` : `promouvoir_jumelles()`, `DOSSIERS_LANGUE`, et `data-langues` lu par `i18n.js` |
| Du contenu de la démonstration a survécu | `purger_demo()`, listes `DEMO_DOSSIERS` et `DEMO_FICHIERS` |
| Le titre de la démo reste dans un onglet | `renommer_identite()`, liste `paires` |
| Un libellé reste en français en anglais | `site/assets/js/ui-labels.js`, et l'abonnement à `tpl:langchange` du moteur concerné |
| Une couleur est illisible | `site/assets/css/palettes.css`, puis relancer le vérificateur |
| Le bouton d'un polycopié n'apparaît pas | la convention de nommage : `chapitre-N-polycopie.<langue>.pdf` |
| Une capsule ne se génère pas | `outils/verifier_elevenlabs.py` avant tout le reste |
| Une série audio est refusée | aucun témoin pour le modèle : `outils/generer_audio.py --temoin --limite 1`, écouté d'abord |
| Un secret n'a pas été recopié | `SECRETS_LOCAUX` dans `nouveau_cours.py`, et le `.gitignore` du template (le motif doit y figurer) |
| Le déployeur refuse d'envoyer | lire la raison : `destination.json`, puis `garde_identite()` dans `deploiement/deployer.py` ; `tester_deployer.py` rejoue chaque cas hors ligne |
| Un renvoi « Pour approfondir » est signalé | l'ancre visée n'existe pas dans la page cible : `renvoi_casse()` dans `outils/verifier_liens.py` |

Un test qui échoue n'est pas une anomalie de recette : c'est un défaut du
gabarit, qui partirait tel quel dans tous les cours suivants. Corrigez-le ici,
pas dans le cours.
