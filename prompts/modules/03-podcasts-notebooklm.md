# Module 03 — Les podcasts et leurs diaporamas : une série NotebookLM, sa page sur le site

> **Quand l'activer.** Quand le cours gagne à s'écouter : découvrir une partie avant de la
> lire, réviser loin de l'écran, raccrocher un étudiant que l'écrit décourage.
>
> **Paramètres.** `modules.podcasts` : `actif`, `episodes` (0 = à proposer), `diaporamas` ;
> dans `cours.json`, le bloc `podcasts` (à `false` par défaut) amène la page et ses outils.
>
> **Place.** Phase 11 du tronc : après le livret, que NotebookLM prend pour source ; les QR
> codes des épisodes entrent ensuite dans le livret (module 02).
>
> **Seul.** Sur un cours qui existe déjà, donnez ce fichier à Claude dans le dossier du
> cours : il commence par la section 9.

---

## 1. Ce que le module produit

- **Une série d'épisodes enchaînés** — les résumés audio de NotebookLM, deux voix qui
  dialoguent —, un par grande partie du cours : un épisode d'accueil, un par chapitre ou
  par ressource importante (le cas, le TP, les schémas, la Boîte à outils…), un épisode
  final.
- **Un diaporama par épisode** (le *Slide Deck* de NotebookLM) : même titre, même numéro,
  même enchaînement.
- **Les prompts** de la série et des diaporamas, en français (et en anglais si le cours est
  bilingue), dans des fichiers `.md` de `docs/prompts/` : l'auteur les colle dans NotebookLM
  et génère lui-même.
- **Une page « 🎙️ Podcasts »** : pour chaque épisode, son lecteur, son résumé (ce qu'il
  couvre, ce qu'il faut retenir), son diaporama à faire défiler et à télécharger, une
  visionneuse plein écran ; un encadré « Le podcast du chapitre » dans les pages du cours ;
  une ligne sur la page du polycopié ; un QR code par épisode dans le livret.

---

## 2. Le modèle : le cours d'architecture logicielle (lecture seule)

Fait de bout en bout sur `C:\projets\Cours\Cours_Architecture_Logicielle` : douze épisodes,
douze diaporamas (150 diapositives), décisions D121 (cadrage) et D122 (mise en ligne, QR
codes dans le livret). **Lis sans rien modifier** ; ne lis jamais ses fichiers secrets.

| À lire | Ce qu'on y trouve |
|---|---|
| `docs\prompts\PROMPTS-NotebookLM-Podcasts.md` et `…-EN.md` | les douze prompts des épisodes, leur mode d'emploi |
| `docs\prompts\PROMPTS-NotebookLM-Slides.md` et `…-EN.md` | les douze prompts des diaporamas |
| `docs\03-Guide-de-production.md`, § 8 ter | les noms des fichiers à déposer, la commande, l'ordre |
| `outils\podcasts.py`, `outils\podcasts_en.py` | la source unique des textes de la page, contrôlée |
| `outils\generer_podcasts.py` | la conversion, les diapositives, les pages, les encadrés |
| `podcasts.html`, `en\podcasts.html`, `assets\js\podcasts.js` | la page et sa visionneuse |

> **Le gabarit fournit déjà l'outillage**, repris de ce cours, en générique et bilingue :
> `outils/podcasts.py`, la source des épisodes (titres, résumés, points à retenir, page
> liée, voix, dans les deux langues) ; `outils/generer_podcasts.py`, le convertisseur (MP3,
> PDF, diapositives WebP) ; `site/podcasts.html` et `assets/js/podcasts.js`, la page et sa
> visionneuse ; l'encadré « Le podcast du chapitre » (fragment `podcast-N`). La page et
> les encadrés sont des fragments, écrits par `outils/generer_fragments.py`. Le cours de
> référence reste le modèle des prompts, de la relecture et des décisions : ne recopie
> pas son code.

---

## 3. Les décisions à faire valider

Une question à la fois ; entre parenthèses, le choix retenu sur le cours de référence.

- **Le découpage de la série** (douze épisodes : accueil, le cas, les six chapitres, le TP
  pas à pas, les schémas, la Boîte à outils, « et maintenant ? »).
- **Les voix** (NotebookLM d'abord ; la voix clonée de l'auteur plus tard, épisode par
  épisode — voir la section 7).
- **La place** (« 🎙️ Podcasts » parmi les ressources du menu, après « 📘 Polycopié », qui
  les ouvre ; le cours de référence les met tous deux en tête du menu, juste après
  « Accueil du cours » ; une carte sur l'accueil, à côté de celle du polycopié).
- **Les renvois** (un encadré par chapitre et par page de ressource, une ligne sur la page
  du polycopié, un QR code à l'ouverture de chaque partie du livret).
- **La mention** (une ligne en pied de page : voix générées par IA).
- **Le texte de chaque épisode** (un résumé — ce qu'il couvre, ce qu'il faut retenir —,
  écrit d'après son prompt, que l'auteur vérifie à l'écoute).
- **L'anglais**, si le cours est bilingue (la page jumelle tout de suite, ses épisodes
  « à venir » tant qu'ils ne sont pas générés).
- **Les diaporamas** (sous chaque lecteur, à faire défiler ; le PDF à télécharger ; un clic
  agrandit une diapositive dans une fenêtre sur toute la page, fermée par un bouton × en
  haut à droite ; PDF publiés tels quels).
- **Le thème visuel** de la série, identique d'un diaporama à l'autre (l'univers du cas, les
  couleurs de la charte du site).

---

## 4. Écrire les prompts

**Les épisodes — 4 800 caractères au plus**, espaces et retours à la ligne compris.

- **En-tête** : « Épisode n sur N d'une série de podcasts pédagogiques en français, tirée du
  polycopié « titre », écrit par l'auteur (cursus, bloc) » ; le public ; le ton —
  chaleureux, clair, enthousiaste, jamais condescendant ; les deux voix dialoguent, se
  relancent et reformulent.
- **DÉROULÉ OBLIGATOIRE** : (1) une accroche attirante et motivante ; (2) rappeler l'objet
  du cours et son auteur ; (3) rappeler l'épisode précédent — au premier, présenter la série
  et son fil conducteur ; (4) annoncer le contenu ; (5) le détail : chaque notion définie
  simplement, puis illustrée par plusieurs exemples du cas, simplifiés pour des débutants,
  concrets et motivants ; (6) résumer les points clés ; (7) remercier les auditeurs, ouvrir
  une perspective et faire le lien avec l'épisode suivant.
- **Le premier épisode** fait l'introduction générale : comment travailler avec le
  polycopié et le site, pourquoi la matière compte aujourd'hui (sur le cours de référence :
  l'architecture à l'ère de l'IA). **Le dernier** donne des conseils pour continuer.
- **RÈGLES** : s'appuyer sur le livret et ses chiffres, n'inventer ni chiffre ni citation ;
  expliquer chaque terme technique à sa première apparition, avec une image du quotidien ;
  des exemples tirés du cas, jamais du sujet de l'épreuve ni de celui du TP (les interdits
  du cours) ; aucune réponse aux exercices, aux QCM ni au TP ; aucune adresse web lue, sauf
  le nom du site.
- **CONTENU** : la partie du livret, section par section, avec ses exemples ; puis
  **À RETENIR**.

**Les diaporamas — 3 700 caractères au plus.**

- **En-tête** : « Diaporama n/N, compagnon de l'épisode n des podcasts du cours « titre »,
  de l'auteur, d'après son polycopié » ; le public ; le but (présenter brièvement toutes les
  notions de la partie).
- **STYLE** : très esthétique, pédagogique et professionnel ; un thème attirant et
  motivant, identique pour toute la série (l'univers du cas, les couleurs de la charte,
  une typographie moderne) ; chaque diapositive illustrée (illustration, schéma,
  pictogrammes, tuiles chiffrées) ; des titres accrocheurs ; un bandeau discret
  « Épisode n/N » ; 10 à 14 diapositives, une idée par diapositive, cinq puces courtes au
  plus, aucun paragraphe ; chaque notion : une définition simple, puis un exemple du cas.
- **RÈGLES** : celles des épisodes.
- **DIAPOSITIVES** : le titre ; « Dans l'épisode précédent » ; l'accroche et le programme ;
  une diapositive par notion ; « À retenir » ; « Merci de votre attention », une
  perspective, « Dans le prochain épisode ».

**Le compte** se fait par script, jamais à l'œil : retours à la ligne compris, chacun
compté pour deux (à la copie, un retour peut valoir deux caractères), avec une marge —
4 750 et 3 650. Le nombre exact s'affiche sous chaque prompt et dans le tableau du fichier.

**Le mode d'emploi**, en tête de chaque fichier : un notebook, avec pour source le PDF du
livret ; *Studio* → *Résumé audio* → *Personnaliser* : format « Approfondissement », la
langue, la durée la plus longue ; *Diaporama* → *Personnaliser* : format présentation
(*Presenter Slides*), la langue, la longueur par défaut ; générer dans l'ordre, nommer
« Épisode n — titre » ; régénérer un épisode qui s'écarte de sa consigne.

---

## 5. Relire ce que NotebookLM produit

- **Chaque diaporama, diapositive par diapositive**, sur des planches de contrôle, avant
  toute publication. Sur le cours de référence, dix erreurs relevées : des propos et des
  attentes prêtés aux personnages du cas, un chiffre inventé, des exemples inventés, une
  décision mal tracée, de faux QR codes dessinés, des coquilles.
- L'auteur corrige dans NotebookLM (la révision d'une diapositive : le crayon à côté du
  titre) puis réexporte ; **chaque export se revérifie en entier** : une révision peut se
  perdre d'un export à l'autre.
- **Les épisodes** : l'auteur les écoute ; un épisode qui s'écarte de sa consigne (réponse
  donnée, chiffre inventé) se régénère avec le même prompt. Les résumés de la page se
  vérifient à l'écoute.

---

## 6. Publier

- **Les noms exacts.** Donne à l'auteur, épisode par épisode, le nom de chaque fichier et
  son dossier : les épisodes bruts dans `Podcasts/fr/` (et `Podcasts/en/`), extension
  d'origine gardée, sous le nom déclaré dans `outils/podcasts.py` — l'épisode d'un
  chapitre se nomme `chapitre-<N>-podcast`, le fichier que joue aussi le lecteur du
  chapitre ; les diaporamas au même nom, en `.pdf`. Ces dossiers ne sont **jamais
  versionnés** (`/Podcasts/` dans le `.gitignore`), **ni déployés** (hors de `site/`).
- **Le générateur** (`outils/generer_podcasts.py`, fourni par le gabarit ; `--essai` d'abord) :
  il convertit chaque épisode en MP3 publié (mono, 64 kbit/s, 44,1 kHz, étiquettes ID3 ;
  seulement si le MP3 manque ou si le brut est plus récent) ; copie chaque diaporama ; rend
  ses diapositives en WebP (1 600 px) et en vignettes (320 px) ; relance
  `generer_fragments.py`, qui réécrit la page et les encadrés ; signale un fichier mal
  nommé, sans le convertir. Rien ne s'écrit qui ne change.
- **Les textes** (titre, résumé, à retenir, page liée, voix) vivent dans une source unique,
  contrôlée (`outils/podcasts.py`) ; quand un épisode passe à la voix de l'auteur, sa source le dit, et la mention
  du pied de page suit.
- **Ce qui part en ligne est ce qui est versionné** : les MP3 et les WebP publiés le sont.
- **Ensuite seulement**, les QR codes des épisodes dans le livret (module 02) : la chaîne
  du polycopié vérifie que chaque adresse répond, la page doit donc être en ligne avant.

---

## 7. Les pièges connus

- **Les limites des champs de NotebookLM** : 4 800 caractères pour l'audio, 3 700 pour le
  diaporama, retours à la ligne compris. Un prompt trop long se resserre, il ne se coupe pas
  à l'aveugle.
- **NotebookLM invente** : chiffres, exemples, propos des personnages, faux QR codes. Rien
  ne se publie sans relecture.
- **Le poids** : sur le cours de référence, 77,6 Mo pour douze épisodes en MP3 64 kbit/s, et
  156 Mo pour douze diaporamas publiés tels quels. Prévoir l'hébergement.
- **La voix clonée** : les résumés audio de NotebookLM n'emploient que leurs voix
  intégrées. La voix de l'auteur passe par ElevenLabs (module 04), épisode par épisode :
  le plus sûr, des scripts écrits d'après le livret puis dits à deux voix, dont la sienne ;
  sinon GenFM d'ElevenLabs ; le plus fragile, changer après coup la voix d'un animateur
  NotebookLM. Vérifier les nouveautés de NotebookLM avant de trancher, et dire sur la page
  que la voix est générée par IA.
- **PyMuPDF ne lit pas le WebP** : les planches de contrôle passent par Pillow.

---

## 8. Les contrôles

- Chaque prompt sous sa limite, compté par script ; le tableau des longueurs à jour.
- Chaque fichier déposé reconnu : le tableau du générateur dit, épisode par épisode, ce qui
  est en ligne et ce qui manque.
- `python3 outils/podcasts.py` sans défaut (chaque épisode complet dans les deux langues,
  chaque encadré à sa place) ; `generer_podcasts.py --essai` sans rien à faire.
- La page : lecteurs, diapositives, visionneuse (×, Échap, flèches), console vide, 1280 et
  375 px ; la parité et les liens si le cours est bilingue.
- Après la mise en ligne : MP3, PDF et WebP en 200, depuis le site public.

**Terminé** quand les épisodes et les diaporamas de chaque langue générée sont relus,
publiés et reliés — page, menu, encadrés, livret — ; et que les décisions, l'état
d'avancement, le guide de production et `TODO.md` sont à jour.

---

## 9. Pour commencer

1. Lis le dépôt du cours et le modèle de la section 2 ; vérifie que le livret existe (le
   module 02 le produit) : c'est la source de NotebookLM. Sur un cours créé sans le bloc
   `podcasts`, reprends du gabarit `site/podcasts.html`, `assets/js/podcasts.js`,
   `outils/podcasts.py`, `outils/generer_podcasts.py`, les styles `.pod-*` de
   `components.css` et l'entrée « 🎙️ Podcasts » du menu, puis vide sa liste d'épisodes.
2. Propose le découpage de la série, épisode par épisode, avec la partie du livret de
   chacun.
3. Pose les questions de cadrage, **une à une** (section 3).
4. Écris un prompt témoin (un épisode et son diaporama), fais-le valider, puis la série,
   dans un fichier `.md` par langue et par sorte.

Sur un cours qui n'a pas été créé depuis le template, les règles de son `CLAUDE.md`
s'appliquent ; à défaut, celles du § 2 du `CLAUDE.md` du template : secrets jamais lus,
commits au seul nom de l'auteur et sans mention d'IA, accord avant de commiter et de
pousser, puis, séparément, avant de mettre en ligne.
