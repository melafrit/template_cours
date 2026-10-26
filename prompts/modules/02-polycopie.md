# Module 02 — Le polycopié : un livret Word et PDF, relié au site par ses QR codes

> **Quand l'activer.** Quand le cours doit exister aussi en livre : un livret qu'on imprime,
> qu'on annote et qu'on révise hors écran, relié au site par des QR codes.
>
> **Paramètres.** `modules.polycopie.actif`. Le livret anglais suit si le module bilingue
> est actif. Dans `cours.json`, le bloc « livret » amène la chaîne et la page (inactif par
> défaut ; il demande le bloc « glossaire »).
>
> **Place.** Phase 10 du tronc : après les contenus, les évaluations, les compléments et la
> version anglaise ; avant les podcasts, que NotebookLM tire du livret et dont les QR codes
> s'y ajoutent ensuite.
>
> **Seul.** Sur un cours qui existe déjà, donnez ce fichier à Claude dans le dossier du
> cours : il commence par la section 8.

---

## 1. Ce que le module produit

Un **vrai livret de cours**, motivant, à la mise en page professionnelle, pédagogique et
académique : des encadrés, les schémas du cours expliqués, et des **QR codes dans la marge,
au bon endroit**, vers les ressources du site — capsules audio, glossaire, activités,
corrections en ligne, modèles, simulateurs, épisodes du podcast. Il est **au nom de
l'auteur** (`cours.auteur`), avec une présentation brève de lui, une **page de garde
professionnelle comme un livre**, des **mentions légales**, un **mini-sommaire au début de
chaque chapitre**, une **bibliographie**, le **glossaire** et un **index**.

Il existe en **Word** (en local et sur le dépôt, jamais publié) et en **PDF** (le seul
format téléchargeable, uniquement sur le site). Si le cours est bilingue, un **livret
anglais** suit le français.

Sur le site : une page « 📘 Polycopié » (« 📘 Course book » en anglais) qui présente le
livret et le fait télécharger ; son entrée en tête des ressources du menu, avant les
fiches de synthèse par chapitre (« 📄 Fiches de synthèse », bloc « polycopies » : les deux
se cumulent) ; une carte sur l'accueil, si l'auteur la veut.

---

## 2. Le point de départ : la chaîne du gabarit, et son modèle

**Le gabarit fournit l'outillage**, repris en générique et bilingue du cours de
référence. Un cours créé avec le bloc « livret » le reçoit ; un cours créé sans, ou avant,
recopie depuis le gabarit les fichiers du tableau et ajoute l'entrée du menu dans
`course-data.js`.

| Fichier | Rôle |
|---|---|
| `outils/generer_polycopie.py` | compose le livret Word, puis le PDF par Word, dans `Polycopie/` (jamais publié) |
| `outils/polycopie/` | le paquet : sources, libelles, navigateur, lecture, gabarit, ooxml, pictos, images, qr, rendu, pages, word, controles, page |
| `outils/livret.py` | la fiche du livret : ce que le site ne dit pas — pied de couverture, catégorie, année du copyright, **présentation de l'auteur** (le livret refuse de s'écrire sans elle), cas fictif, adresses à nommer, noms gardant leur minuscule, chapitres du témoin |
| `outils/publier_polycopie.py` | contrôle le PDF, le publie dans `site/livret/` avec la vignette de sa couverture et `livret.json`, puis réécrit la page |
| `site/polycopie.html` | la page : fragments `livret-couverture`, `livret-fiche`, `livret-auteur`, écrits par `outils/generer_fragments.py` |
| `site/assets/js/interactions.js` | l'enregistreur : chaque composant RDCX garde sa configuration ; l'adresse `?polycopie=fr` (ou `en`) la dépose dans la page, que Chrome sans interface lit |

Le livret se tire des pages du site, sans rien recopier : les chapitres de
`course-data.js` dans leur ordre ; leurs composants (checkpoint, reveal, match, spotError,
branch, hotspots, voice) devenus exercices sur papier, chacun corrigé en ligne derrière
son QR code ; le glossaire de `glossaire-data.js` en fin de livret, dans la marge (la
définition à la première rencontre du terme) et dans l'index. Les QR codes portent
l'« url » de `deploiement/destination.json` ; sans elle, une adresse d'exemple, et la
vérification en ligne n'a pas lieu.

**Étendre le vocabulaire.** Un composant nouveau du moteur s'ajoute à l'enregistreur
(`interactions.js`, la liste des sortes), puis à `rendu.Rendu.activite` ; un encadré
nouveau, à `lecture.py` (sa classe CSS) et à `rendu.STYLES_ENCADRES` ; un libellé, à
`libelles.py`, dans les deux langues. **Un schéma à zones** dont les titres sont numérotés
(« 1. Le public ») garde son image telle quelle, et l'encadré de lecture reprend ses
numéros : c'est le rendu le plus propre. Sinon chaque zone reçoit une pastille numérotée,
posée dans le blanc le plus proche de son point.

**Ce que le gabarit n'a pas** et que le modèle montre : la bibliographie, les fiches mémo
en pleine page, l'étude de cas et le TP pas à pas, les filières, le manifeste des QR codes.

**Le modèle : le cours d'architecture logicielle (lecture seule).** Ce travail a été fait
de bout en bout sur `C:\projets\Cours\Cours_Architecture_Logicielle` (décisions D114 à
D122). **Étudie-le pour ce que le gabarit n'a pas, et n'y modifie jamais rien** — pas même
un `__pycache__` : lis ses modules Python, ne les importe pas. Ses fichiers secrets valent
ceux du cours : ne les lis jamais.

| À lire | Ce qu'on y trouve |
|---|---|
| `docs\06-Plan-du-polycopie.md` | toutes les décisions, le témoin, l'avancement ; la présentation de l'auteur validée (§ 3) |
| `docs\01-Decisions-de-conception.md` | D114 (cadrage) à D122 (QR codes du podcast), dont D117 (page, menu, accueil), D118 (livret anglais), D120 (QR codes cliquables) |
| `docs\03-Guide-de-production.md` | le polycopié dans l'ordre de génération |
| `outils\generer_polycopie.py` et le paquet `outils\polycopie\` | la chaîne : sources, libelles, lecture, gabarit, ooxml, images, pictos, qr, rendu, pages, word, controles |
| `outils\publier_polycopie.py` | la publication du PDF et la fiche de téléchargement |
| `polycopie.html`, `en\polycopie.html`, `assets\js\navigation.js`, l'accueil | la page, le menu, la carte |
| `deploiement\deployer.py` | l'exclusion du dossier de travail `Polycopie/*` |
| `livret\`, `en\livret\` | les livrets publiés : 226 et 222 pages, 368 et 369 QR codes |

Reprends ce qui s'applique, adapte ce qui diffère — structure du site (`site/` dans un cours
créé depuis le template), ressources, langues, filières — et dis à l'auteur ce que tu
reprends : chaque reprise est une décision Dnn.

---

## 3. Les décisions à faire valider

Une question à la fois ; entre parenthèses, le choix retenu sur le cours de référence.

- **Format** (A4 portrait, marges en miroir, grande marge extérieure pour les QR codes et
  les notes).
- **Titre** (celui du cours) et **sous-titre pédagogique** ; pied de couverture (cursus et
  bloc).
- **Présentation de l'auteur** : pars de celle du cours de référence
  (`docs\06-Plan-du-polycopie.md`, § 3), adapte-la, **montre-la en entier dans la
  question** ; corrigée par l'auteur, elle s'imprime ensuite mot pour mot.
- **Mentions légales** (« © année, nom de l'auteur — Tous droits réservés » ; usage
  personnel et pédagogique des étudiants autorisé, toute autre reproduction ou diffusion
  soumise à l'accord écrit de l'auteur ; Première édition ; l'année n'apparaît que dans le
  copyright ; cas d'étude fictif ; marques à leurs propriétaires).
- **Couleur** (la charte du site, **lisible en noir et blanc** : chaque encadré se
  reconnaît à son pictogramme, son libellé et son filet, jamais à la seule couleur).
- **Contenu** (les chapitres en entier, chacun ouvert par son mini-sommaire ; l'étude de
  cas ; le TP pas à pas **sans sa correction** ; les ressources propres au cours — guide de
  schémas, catalogue d'une Boîte à outils, une ou deux lignes par fiche : sa définition,
  puis à quoi elle sert ; les fiches mémo en pleine page ; bibliographie, glossaire,
  index).
- **Réponses** (seulement en ligne : **aucune réponse imprimée** ; chaque série d'exercices
  ou de QCM porte un QR code vers sa correction en ligne ; **jamais** la correction
  protégée du TP, vers laquelle aucun QR code ne mène).
- **QR codes** (dans la marge extérieure, à côté du paragraphe qu'ils servent, une courte
  légende dessous ; **aucune adresse imprimée** ; **chaque QR code et sa légende sont aussi
  des liens cliquables** vers la même adresse, dans le PDF et dans le Word, sans changer
  l'aspect imprimé). Montre d'abord un exemple de quelques pages, puis généralise.
- **Schémas** (ceux du site, chacun suivi de sa **lecture élément par élément** pour un
  débutant ; s'il en manque une, propose de l'ajouter aussi sur le site, dans chaque
  langue).
- **Bibliographie** (celle du site ; si le site n'en a pas, propose-la par rubriques, chaque
  référence vérifiée — auteur, titre, éditeur, édition, ISBN ou adresse officielle — et
  fais-la valider avant qu'elle entre dans le livret).
- **Sur le site** (la page « 📘 Polycopié » : couverture, bouton de téléchargement, PDF,
  pages, poids, langue ; ce que contient le livret ; ses QR codes ; comment l'imprimer ;
  l'auteur — la page du gabarit a tout cela ; entrée de menu en tête des ressources ; carte
  sur l'accueil, qui mène à la page et non au PDF).
- **Podcasts**, si le module 03 est actif (un QR code « PODCAST » à l'ouverture de chaque
  partie, vers l'épisode qui la raconte ; posé une fois les épisodes publiés).
- **Production** (un **témoin** d'abord, validé par l'auteur ; puis le **livret
  français** ; puis l'**anglais**).

Selon le cours, deux décisions de plus :

- **Plusieurs filières** : un livret commun, à blocs étiquetés, ou un livret par filière ?
  Un QR code peut ouvrir une page directement dans la bonne filière (`?filiere=` dans
  l'adresse, si le site le comprend).
- **Site entièrement protégé** (`modules.deploiement.site_protege`) : un QR code scanné
  ouvre d'abord la demande d'identifiants ; le mode d'emploi du livret le dit, et dit où
  l'étudiant trouve les siens (le cahier de texte) ; **aucun identifiant n'est imprimé**.

---

## 4. L'architecture (celle du gabarit, à adapter)

- **Une chaîne, pensée pour durer** : `outils/generer_polycopie.py` (options `--temoin`,
  `--anglais`, `--essai`, `--sans-pdf`, `--hors-ligne`, `--apercus`, `--images`,
  `--verrou`, `--sortie` ; le cours de référence y ajoute `--manifeste`) et un paquet
  `outils/polycopie/` : lecture des
  pages du site (le contenu de `<main>`) en blocs Word — intertitres, paragraphes, listes,
  tableaux, figures, encadrés, activités, capsules, termes du glossaire ; un lien vers une
  autre partie du livret devient un renvoi « (p. n) » ; libellés dans les deux langues. Les
  chiffres viennent des mêmes sources que le site.
- **Word** écrit par python-docx et de l'OOXML : marges en miroir (intérieure 2,2 cm,
  extérieure 5,2 cm, haut 2,2, bas 2,4) ; en-tête : titre du livre (pages paires), titre
  du chapitre (pages impaires, champ `STYLEREF`) ; numéro de page au coin extérieur ;
  polices **installées sur le poste** (Cambria 10,5 pt, titres Segoe UI Semibold, marge
  Segoe UI 7–8 pt, code Consolas 9 pt). Mini-sommaires en champs `PAGEREF` vers des
  signets, **dans l'ordre des pages** ; table des matières en champ `TOC` ; index par
  champs `XE` + `INDEX`.
- **La marge** : chaque QR code est une zone de texte ancrée sur la ligne de son
  paragraphe (`wp:anchor`, `positionH outsideMargin`, `positionV line`) ; QR codes générés
  par `segno` (correction M, 2,2 cm environ) ; une zone du glossaire porte le terme et sa
  définition sous le QR code. Après mise en page, Word range la marge page par page : aucun
  chevauchement, aucun débordement.
- **Les liens** : le QR code porte un `a:hlinkClick` (dans `wp:docPr` et `pic:cNvPr`), sa
  légende un `w:hyperlink`, tous deux vers la même adresse externe ; les fiches mémo,
  remplacées dans le PDF, y reçoivent leurs liens après l'export.
- **Export par Word** (COM, `pywin32`) **sous un verrou** (création exclusive, supprimé
  même en cas d'erreur ; un seul export à la fois sur le poste) : tous les champs mis à
  jour deux fois, schémas trop larges ajustés, Word enregistré avec ses champs à jour, PDF
  exporté avec ses signets ; puis **la langue du PDF** (`/Lang` fr-FR ou en-US) et son
  titre posés dans le PDF.
- **Schémas** : les SVG du site, photographiés en PNG haute définition par Chrome sans
  interface.
- **Fiches mémo** (cours de référence) : dans le Word, une image pleine page ; dans le PDF, la page est
  remplacée par la fiche vectorielle du site, dont les réponses imprimées s'effacent au
  profit du QR code de la fiche en ligne.
- **Publication** : `outils/publier_polycopie.py [--anglais] [--essai] [--pdf <chemin>]`
  contrôle le PDF (titre, langue, nombre de pages, poids), le copie dans `site/livret/`,
  rend la vignette de la couverture, écrit `livret.json` et réécrit la fiche de
  téléchargement de la page (ses fragments). Le nom proposé au téléchargement suit la
  langue du livret : `Polycopie-<titre>.pdf`, `Course-book-<titre>.pdf`.
- **Dossier de travail `Polycopie/`**, hors du site publié : jamais déployé ; seuls les
  Word y sont versionnés (le témoin, les PDF de travail et `_cache/` sont ignorés). Si le
  cours est bilingue, la page anglaise propose le livret anglais ; tant qu'il n'est pas
  publié, le français, marqué `hreflang="fr"`.

---

## 5. Les règles du cours, qui valent dans le livret

Celles des décisions du cours (lis-les), et au moins : aucune date fixe hors copyright ; le
sujet du TP n'apparaît que dans la partie TP ; les interdits du cours se contrôlent dans le
livret comme sur le site ; **aucune réponse imprimée** ; chaque schéma expliqué élément par
élément ; adresses vérifiées (réponse 200 ; un site qui refuse les robots se vérifie dans
le navigateur) ; mêmes chiffres que le site ; typographie de la langue (espaces insécables
du français, « (p. 112) » insécable ; en anglais, pas d'espace avant « : »).

**Une faute relevée dans le français du site ne se corrige jamais en silence** :
propose-la (regroupée, cliquable, plusieurs choix possibles) ; acceptée, elle part dans un
commit séparé.

---

## 6. Les pièges connus

- **Le dossier publié ne s'appelle jamais `polycopie/`** : Windows ne distingue pas la
  casse, ce serait le dossier de travail `Polycopie/`. Le cours de référence publie dans
  `livret/` et `en/livret/`.
- **Un schéma déjà rendu par PlantUML ne se rend jamais de nouveau sur un autre poste** que
  celui qui l'a produit : les polices changent le dessin.
- **Un seul export Word à la fois** : deux exports simultanés se marchent dessus — d'où le
  verrou.
- **Word écrit toujours « en »** comme langue du PDF : la langue et le titre se posent
  après l'export.
- **Les champs** (`PAGEREF`, `TOC`, `INDEX`) se mettent à jour deux fois : la table des
  matières déplace les pages, une seule passe laisse des numéros faux. Le contrôle cherche
  les champs mal calculés.
- **Le glossaire rendu par script** : vérifie comment une adresse ouvre un terme précis
  (identifiant d'ancre, paramètre de l'index) avant d'y poser des QR codes.
- **PyMuPDF ne lit pas le WebP** : les planches de contrôle qui en contiennent passent par
  Pillow.
- **Une image pas encore produite** (une adresse vide, comme dans un squelette de chapitre)
  ne s'imprime pas : la génération la signale (« schéma absent du site », « image absente
  du site »). Un livret à publier n'en signale aucune.

---

## 7. Les contrôles, à chaque livret

- **Le Word** s'ouvre. **Le PDF** : nombre de pages, signets, langue, titre ; **chaque page
  rendue en PNG (PyMuPDF) et relue à l'œil** — marges, QR codes à leur place, en-têtes,
  mini-sommaires et leurs pages, encadrés, schémas nets (signale toute image sous 240
  points par pouce), rien qui déborde.
- **Chaque QR code décodé dans le PDF** : son adresse absolue, sa réponse ; **chaque QR
  code et sa légende couverts par un lien de même adresse** ; un manifeste JSON des QR
  codes.
- **Rien qui ne doive pas y être** : aucun champ mal calculé, aucune réponse imprimée (pas
  même tête-bêche), aucune date, aucun interdit.
- **Sur le site** : liens, menus à jour, parité des pages jumelles et `hreflang` si le cours
  est bilingue, recette au navigateur à 1280 et 375 px (console vide, aucun débordement).
- **Après la mise en ligne** : page et PDF en 200, tailles identiques au dépôt ; sur un site
  protégé, 401 sans identifiants — sans jamais t'authentifier.

**Terminé** quand le livret de chaque langue est publié sans anomalie aux contrôles ; que la
page, le menu et la carte de l'accueil y mènent ; et que le plan du polycopié, les
décisions, l'état d'avancement, le guide de production et `TODO.md` sont à jour.

---

## 8. Pour commencer

1. Lis le dépôt du cours (structure, pages, générateurs, `docs\`, `TODO.md`), la chaîne
   du gabarit et le modèle de la section 2 ; si le cours n'a pas la chaîne, recopie-la
   depuis le gabarit.
2. Fais l'inventaire chiffré de ce que le livret contiendra : chapitres et sections,
   schémas (avec ou sans lecture), capsules audio, activités et QCM, ressources, fiches
   mémo, termes du glossaire, références, documents du TP, épisodes du podcast. Recompte
   sur le dépôt : un chiffre recopié d'un document date.
3. Pose les questions de cadrage, **une à une** (section 3).
4. Propose le plan — témoin, livret français, livret anglais, page du site —, puis attends
   l'accord de l'auteur pour lancer le témoin.

Sur un cours qui n'a pas été créé depuis le template, les règles de son `CLAUDE.md`
s'appliquent ; à défaut, celles du § 2 du `CLAUDE.md` du template : secrets jamais lus,
commits au seul nom de l'auteur et sans mention d'IA, accord avant de commiter et de
pousser, puis, séparément, avant de mettre en ligne.
