# Recette du gabarit

**Quand l'utiliser :** à la réception du template — nouveau poste, nouvelle
machine, `git pull` important — et après toute modification du moteur. Comptez
vingt minutes.

Ne pas confondre avec [CHECKLIST.md](CHECKLIST.md), qui accompagne la
**fabrication d'un cours**. Celle-ci vérifie le **contenant** : que le gabarit
fonctionne, et surtout qu'il produit un cours propre.

Les trois tests vont du plus rapide au plus important. Le troisième est le seul
qui vous dise ce que vous recevrez réellement en démarrant un nouveau cours.

---

## 0. Lancer

Depuis le Finder, **double-cliquez `demarrer.command`** — le bit exécutable est
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

## 1. Le site de démonstration — à l'œil

Le site parle de lui-même : son sujet est « concevoir un cours en ligne ».
C'est voulu. Vous lisez le mode d'emploi en testant le contenant.

- [ ] **Accueil** — le bouton « commencer » mène au chapitre 1. Ce lien n'est
      pas écrit dans la page : `navigation.js` le calcule depuis
      `course-data.js`. S'il tombe juste, le mécanisme qui protège les cours
      créés fonctionne. 🔴
- [ ] **Chapitre 1** — la vitrine. Les **sept composants interactifs** y sont
      tous : point d'étape, révélation, chasse à l'erreur, appariement,
      embranchement, points chauds, prise de parole. Plus une capsule audio, un
      schéma et un polycopié.
- [ ] **Chapitres 2 et 3** — structure d'un chapitre rédigé. Le 3 porte le
      podcast.
- [ ] **Glossaire** — survolez un terme souligné dans un chapitre : l'info-bulle
      s'affiche, et le lien « voir dans le glossaire » fonctionne depuis
      `/chapitres/` comme depuis la racine.
- [ ] **Polycopiés** — six PDF. Chacun est testé par une requête HEAD avant
      affichage : un bouton visible est un fichier qui existe.
- [ ] **Activités** — trois patrons réutilisables, douze contrôles.
- [ ] **QCM** — entraînement, correction, tableau de bord.
- [ ] **Pied de page** — « À propos du template » est atteignable.

### Le test qui casse tout d'un coup

- [ ] Basculez **FR/EN** en haut à droite, sur le chapitre 1. Tout doit suivre :
      titres, prose, boutons, **et** les libellés fabriqués en JavaScript — la
      barre d'étapes, les activités, les messages de correction. 🔴

C'est là que l'i18n lâche d'habitude, parce qu'un libellé écrit une fois à la
construction ne se repeint pas tout seul. La barre d'étapes est restée en
français sur une page anglaise pendant des semaines : l'élément le plus visible
du chapitre.

- [ ] **Console vide** (⌥⌘I). Un 404 de favicon suffit à faire perdre
      l'habitude de la regarder.
- [ ] **Thème sombre** et **affichage téléphone** — le menu passe en tiroir.

---

## 2. Les vérificateurs — automatique, trente secondes

    python3 outils/verifier_i18n.py

Quatre contrôles : clés appariées dans les deux langues, clés appelées par les
moteurs, égalité des blocs `data-tr` page par page, concordance des titres entre
le menu et les pages. Doit finir sur **« Bilingue cohérent »**.

    python3 outils/verifier_contraste.py

Les cinq palettes, en thème clair **et** sombre, contre les seuils WCAG :
4,5:1 pour le texte courant, 3:1 pour le grand texte et le non-texte. Doit
passer sans échec — c'est ce test qui a rattrapé deux couleurs illisibles de la
palette marine, en place depuis deux ans.

    python3 outils/verifier_liens.py

Tous les `href` et `src` qui désignent un fichier du site. Doit finir sur
**« Aucun lien mort »**. C'est le contrôle le plus rentable du lot : quatre
familles de liens différentes ont, tour à tour, survécu à la génération en
pointant vers les chapitres de la démonstration.

---

## 3. Générer un cours vide — le test qui compte 🔴

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

    contenu de demonstration retire : 26 media(s), 5 fichier(s) remis a l'etat de squelette
    14 page(s) renommee(s) au nom du cours
    7 fichier(s) recousu(s) sur les chapitres declares
    cours.html : 3 carte(s) de chapitre regeneree(s)

Les deux derniers chiffres suivent le nombre de chapitres déclarés : une carte
par chapitre, et un recousage par chapitre plus les quatre pages qui les
citent. Les 26 médias et les 5 squelettes, eux, ne bougent pas.

Puis, sur le cours produit :

    python3 outils/verifier_liens.py --site ../mon-cours/site

Le cours créé embarque son propre lanceur. Ouvrez-le :

    cd ../mon-cours && python3 demarrer.py

- [ ] Le site est **complet et fonctionnel**, et **entièrement vide de
      contenu**. 🔴
- [ ] **Aucune** capsule audio, **aucun** PDF, **aucun** schéma de la
      démonstration.
- [ ] Les chapitres sont des squelettes, appels de composants en commentaire.
- [ ] Le bouton « commencer » de l'accueil mène au premier chapitre déclaré.
- [ ] Le QCM est réduit à deux questions génériques.
- [ ] Le pied de page ne renvoie plus vers « À propos du template ».
- [ ] **L'onglet du navigateur porte le titre de VOTRE cours**, sur chaque
      page — de même que la méta-description, l'auteur des métadonnées et la
      ligne d'auteur du pied de page. 🔴
- [ ] `verifier_liens.py` finit sur « Aucun lien mort ».

**Toute trace du cours « concevoir un cours en ligne » dans `../mon-cours` est
un défaut.** Y compris un titre d'onglet, une méta-donnée, un attribut. La
seule exception est `site/chapitres/_modele.html`, le chapitre vitrine gardé
comme référence : il conserve volontairement ses exemples de composants.

Le contrôle en une ligne, depuis le dossier du cours créé :

    grep -ril "concevoir un cours en ligne" site/ | grep -v _modele

Il ne doit rien retourner.

---

## 4. Deux pièges à connaître

**Le cache du navigateur.** Le serveur envoie `no-store`, et malgré ça un
navigateur peut servir un vieux fichier JavaScript, même dans un onglet neuf.
Si une correction ne s'affiche pas, ne cherchez pas dans le code : relancez sur
un autre port.

    python3 demarrer.py --port 8790

**Les fichiers à secrets sont absents d'un dépôt fraîchement cloné**, et c'est
voulu : `outils/elevenlabs.json` porte votre clé API, `deploiement/config.json`
vos identifiants d'hébergement, `docs/acces.json` ceux du site de cours. Aucun
n'entre au dépôt. Recopiez `outils/elevenlabs.exemple.json` avant de tester la
génération audio, elle échouera sinon.

---

## Si un test échoue

| Symptôme | Où regarder |
|---|---|
| Un lien mène nulle part dans un cours créé | `recoudre_liens()` dans `nouveau_cours.py` |
| Du contenu de la démonstration a survécu | `purger_demo()`, listes `DEMO_DOSSIERS` et `DEMO_FICHIERS` |
| Le titre de la démo reste dans un onglet | `renommer_identite()`, liste `paires` |
| Un libellé reste en français en anglais | `site/assets/js/ui-labels.js`, et l'abonnement à `tpl:langchange` du moteur concerné |
| Une couleur est illisible | `site/assets/css/palettes.css`, puis relancer le vérificateur |
| Le bouton d'un polycopié n'apparaît pas | la convention de nommage : `chapitre-N-polycopie.<langue>.pdf` |
| Une capsule ne se génère pas | `outils/verifier_elevenlabs.py` avant tout le reste |

Un test qui échoue n'est pas une anomalie de recette : c'est un défaut du
gabarit, qui partirait tel quel dans tous les cours suivants. Corrigez-le ici,
pas dans le cours.
