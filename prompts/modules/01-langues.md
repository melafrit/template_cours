# Module 01 · Les langues : les pages jumelles du cours, après la langue racine

> **Quand l'activer.** Quand le cours doit exister dans une autre langue que sa langue
> racine : l'anglais pour un public international ou une filière anglophone, l'arabe pour un
> public arabophone.
>
> **Paramètres.** `cours.langues`, la langue racine d'abord (`fr` ou `en`), puis celles des
> jumelles (`["fr", "en"]`, `["fr", "en", "ar"]`). Le module est actif dès que la liste compte
> plus d'une langue. L'arabe ne peut pas encore être la racine : la démonstration n'a pas
> toutes ses pages en arabe.
>
> **Place.** Phase 9 du tronc, une fois la racine stable : contenus, évaluations, compléments
> et audio validés. Les langues se traduisent l'une après l'autre, chacune par lots.
>
> **Seul.** Sur un cours qui existe dans sa langue racine, donnez ce fichier à Claude dans le
> dossier du cours : il commence par la section 10.

---

## 1. Ce que le module produit

Le site **entièrement traduit, en détail**, dans chaque langue de `cours.langues` : chaque
page publique et protégée, chaque schéma et figure, chaque **piste audio** (la voix clonée de
l'auteur, Eleven v4), chaque QCM et ses explications, le glossaire, les flashcards, la
bibliographie, les simulateurs, les activités, et les **documents à télécharger** (Word, PDF,
ZIP, tableurs).

Le groupe de langues **en haut à droite** (« FR · EN · عربي ») rouvre la page jumelle **au
même endroit** : même section, même paragraphe. Pour chaque langue, un **lexique** et un
**guide de style** fixent les termes ; ils servent ensuite au livret (module 02) et aux
podcasts (module 03) de cette langue.

---

## 2. Le modèle : le site miroir

Chaque langue a son dossier sous `site/` (`en/`, `ar/`), où chaque page a sa **jumelle** :
même chemin, même nom de fichier, **même suite de blocs** que la page de la langue racine.
C'est le modèle retenu par l'auteur le 25 octobre 2026, celui de ses cours bilingues, sur
lequel reposent le livret dans chaque langue, la page Podcasts et les balises `hreflang`.
Depuis le 21 novembre 2026, la démonstration est un site miroir et `nouveau_cours.py` ne
fabrique que ce modèle.

Les blocs `data-tr` (les deux langues dans la même page) ne se créent plus. Ils restent
décrits dans `docs/I18N.md`, partie B, pour les cours qui les ont déjà, et un tel cours se
convertit une fois au miroir (`data_tr_vers_miroir.py`).

---

## 3. Les outils, et les modèles de la méthode

**Les outils du miroir sont dans le gabarit** (`docs/I18N.md`, § A.9) : le groupe de langues
(`langue.js`), la liste des pages traduites (`langues-data.js`, écrite par
`generer_langues.py`), la préparation d'une jumelle (`creer_jumelle.py`, avec `--langue ar`
pour l'arabe), la conversion d'un cours en blocs `data-tr` (`data_tr_vers_miroir.py`), les
liens (`liens_langues.py`, `documents_en.py`), les balises (`hreflang.py`) et la parité
(`verifier_parite.py`, qui signale aussi un bloc arabe resté sans lettre arabe). Un cours créé
avant leur arrivée les reprend du gabarit.

**Quatre outils ne savent pas encore l'arabe** : `hreflang.py`, `generer_playlist.py` et
`synchroniser_capsules.py` (registre du gabarit, lot 1), et `generer_audio.py`, qui ne
parcourt que `site/` et `site/en/` et ne reconnaît que les suffixes `-fr` et `-en` ; une piste
arabe y recevrait l'accent parisien des pistes françaises. Pour un cours en arabe, signale-le
à l'auteur au cadrage, et note dans `TODO.md` ce qui en dépend.

**La méthode de l'anglais** a été rodée de bout en bout sur
`C:\projets\Cours\Cours_Architecture_Logicielle` (lots 0 à 8, décisions D97 à D113, puis D118
pour le livret anglais). **Étudie-le avant de concevoir quoi que ce soit, et n'y modifie
jamais rien** : lis ses modules Python sans les importer. Ses fichiers secrets valent ceux du
cours, et ne se lisent jamais.

| À lire | Ce qu'on y trouve |
|---|---|
| `docs\05-Plan-de-traduction-anglaise.md` | le plan par lots, l'inventaire, l'avancement |
| `docs\traduction\lexique.md`, `docs\traduction\guide-de-style.md` | les termes fixés, les écarts harmonisés, le style |
| `docs\01-Decisions-de-conception.md` | D97 à D113 |
| `docs\03-Guide-de-production.md`, § 8 bis | l'ordre de génération des deux langues |
| `outils\traduction_en.py`, `correction_en.py`, les modules `*_en.py`, `verifier_traductions_en.py` | les tables de traduction des générateurs, les modules jumeaux, leur contrôle |
| `outils\generer_audio.py` (options anglaises) | l'audio anglais |

**La méthode de l'arabe** a son témoin dans le gabarit lui-même : le chapitre 1 de la
démonstration, préparé par l'outil puis traduit bloc pour bloc (28 blocs, 0 écart de
parité), avec le contenu de ses composants, les titres du cours, les termes du glossaire, les
cartes de révision et l'épisode 1 du podcast. Ses règles et ses termes sont dans
`docs/LEXIQUE-ar.md`, qui part dans chaque cours.

Reprends ce qui s'applique, adapte ce qui diffère, et dis à l'auteur ce que tu reprends :
chaque reprise est une décision Dnn.

---

## 4. Les décisions

**Déjà prises par l'auteur pour l'arabe** (21 novembre 2026, `docs/LEXIQUE-ar.md`), à
appliquer sans les redemander :

- traduire la fonction, pas les mots : « projet fil rouge » se dit « المشروع التطبيقي »,
  jamais un calque ;
- les variantes du Maghreb quand deux usages existent ;
- le terme français entre parenthèses à sa première apparition dans une page, pour les
  notions du glossaire seulement ;
- les chiffres occidentaux (1, 2, 3), comme dans les autres langues ;
- l'arabe standard moderne, au vouvoiement de politesse que permet le pluriel ;
- les noms propres, les sigles et le code en lettres latines.

**À faire valider**, une question à la fois ; entre parenthèses, le choix retenu sur le
cours de référence quand il existe :

- **L'accent des pistes anglaises** (*clear, well-articulated, professional General American
  accent* ; l'audio français garde son accent parisien marqué).
- **La voix et l'accent des pistes arabes** : rien n'est encore tranché.
- **Les noms dans le code et les schémas** (en anglais).
- **Les termes délicats** : propose les options, avec l'usage des pays de la langue ;
  l'auteur tranche, le lexique enregistre. En arabe, un terme qui manque au lexique s'y
  ajoute avant d'être employé.
- **Le découpage en lots** et leur ordre (section 7).
- **Les zones protégées** (leurs jumelles, protégées exactement comme les pages de la racine).
- **Les documents à télécharger** : lesquels traduire, et leurs noms dans chaque langue.

---

## 5. L'architecture

- **Une jumelle par page et par langue**, même suite de blocs : `verifier_parite.py` contrôle
  les blocs (0 écart exigé), et le groupe de langues repère le bloc lu par son rang. Pour une
  liste que chaque langue trie à sa façon (le glossaire), une **clé commune** à toutes les
  langues (`data-jumeau`).
- **Les jumelles naissent de deux façons** : `creer_jumelle.py <page>` (avec `--langue ar`
  pour l'arabe) prépare la jumelle d'une page, chemins réglés, marquée « À TRADUIRE », le
  texte restant à traduire bloc pour bloc ; `data_tr_vers_miroir.py` coupe en deux, d'un
  coup, chaque page d'un cours en blocs `data-tr`.
- **La liste des pages traduites** (`langues-data.js`, générée) : le menu et le groupe de
  langues n'offrent une langue que là où la jumelle existe. Tant qu'une jumelle manque, le
  lien mène à la page de la racine, marqué `hreflang` ; `liens_langues.py` rebranche tout dès
  qu'elle existe, documents compris (une seule table des noms des documents,
  `documents_en.py`).
- **Les générateurs écrivent toutes les langues** : l'anglais vient de **modules jumeaux
  `*_en.py`** (mêmes signatures) ou de **tables `{texte de la racine : traduction}`**, en
  **mode strict**, où un texte sans traduction arrête la génération. Mêmes nombres que dans la
  racine, écrits à la façon de la langue (32,000 ; 99.5% ; 11 p.m. en anglais ; « 30 د » pour
  une durée en arabe). **Les sorties de la racine restent identiques à l'octet**, vérifiées à
  chaque lot.
- **Les schémas** : leurs textes passent par des tables de traduction ; la géométrie se
  recalcule sur la traduction ; une étiquette traduite n'est jamais plus longue là où la mise
  en page suit la largeur de la racine. Un schéma arabe se lit de droite à gauche, sa
  première étape à droite, comme ses points (le schéma du chapitre 1, au registre). Chaque
  schéma garde sa **lecture élément par élément**, traduite.
- **L'arabe, de droite à gauche** : `dir="rtl"` sur la page, des propriétés logiques plutôt
  que la gauche et la droite (le gabarit les a converties le 21 novembre 2026), les polices
  Noto Naskh et Noto Sans Arabic après les polices latines, un interligne plus ample, ni
  lettres espacées ni italique, le code de gauche à droite, les translations du menu mobile et
  de la liste de lecture retournées.
- **Les balises `hreflang`** (chaque langue et `x-default`, en adresses absolues) sur toutes
  les pages publiques jumelles, posées en dernier dans l'ordre de génération, jamais sur les
  pages protégées.
- **Les zones protégées** : leurs jumelles sont protégées **exactement comme les pages de la
  racine** ; à la mise en ligne, la protection d'abord (vérifiée en 401 sans identifiant), le
  contenu ensuite (module 08).
- **Les PDF exportés par Word** : un seul export à la fois (verrou), champs mis à jour, langue
  du PDF posée après l'export, celle de son livret (fr-FR, en-US).

---

## 6. Les pistes audio

- **Eleven v4**, la voix clonée de l'auteur (la configuration ElevenLabs est secrète : le
  générateur la lit, Claude jamais) ; l'accent retenu pour chaque langue (section 4) ; filtre
  la ligne qui affiche l'identifiant de voix.
- **Un témoin d'abord** dans chaque langue, écouté et validé par l'auteur, puis la série ;
  durée et débit contrôlés par le générateur (module 04).
- **Une piste par langue**, nommée `chapitre-<N>-capsule-<langue>.mp3` : sans le suffixe,
  l'auditeur d'une autre langue entend la racine. La capsule arabe du chapitre 1
  (`chapitre-1-capsule-ar.mp3`) est déjà appelée par sa page ; le générateur ne la produit qu'avec la
  voix choisie pour l'arabe (`voix_id_ar`), jamais avec le clone français ni l'accent parisien.
- Les fiches traduites vivent à côté de celles de la racine, avec le suffixe de leur langue
  (`docs/prompts/Capsules_accueil_en.md`), jamais dans un sous-dossier, que les outils ne
  lisent pas. Elles gardent **les mêmes marqueurs** : mêmes faits, même ordre, autant de paragraphes et
  de balises de jeu (« speaking slowly » dans chacune), longueur à 10 % près ; nombres et
  sigles écrits pour la voix (« S.A.D. »), la transcription les écrivant normalement. La
  transcription arabe vit dans la fiche comme les autres : `synchroniser_capsules.py` la reporte
  dans la jumelle de `ar/`.
- **Un texte enregistré ne se change jamais sans réenregistrer la piste** ; un écart se note
  dans `TODO.md`.

---

## 7. La méthode : des lots

Commence par **inventorier tout le site** (pages, générateurs, audio, schémas, documents,
zones protégées, volumes en mots et en caractères audio), puis propose un plan par langue,
par exemple :

- **0** fondations : groupe de langues, scripts, contrôles, lexique, guide de style ;
- **1** une page témoin complète : un chapitre, ses schémas, ses activités, son audio ;
- **2** les autres chapitres ; **3** les pages communes ; **4** les fiches et annexes ;
- **5** les QCM et leurs corrections expliquées ; **6** les zones protégées ;
- **7** les documents à télécharger ; **8** les finitions (`hreflang`, harmonisation des
  termes, recette complète, documentation).

Chaque lot suit le même circuit : production (agents en parallèle quand c'est utile, avec une
consigne écrite et un vérificateur), contrôles, présentation du lot, témoin audio, reste de
l'audio, commit sur l'accord de l'auteur, mise en ligne sur un accord distinct, question sur
la suite.

---

## 8. Les règles et les pièges

- **L'anglais** : anglais américain, ton de la racine (le vouvoiement devient « you »),
  typographie anglaise (pas d'espace avant « : »), titres en **Title Case**.
- **L'arabe** : les règles de `docs/LEXIQUE-ar.md` (section 4). Les capitales espacées des
  titres et des étiquettes reviennent à un espacement normal, sinon les lettres se détachent.
  Le navigateur retourne de lui-même les chevrons ‹ ›, qui sont des caractères miroirs, mais
  pas les flèches → ←, qui s'inversent à la main dans les libellés. La pile à chasse fixe
  passe par Noto Sans Arabic, sinon une police système espace mal les lettres.
- **Les règles du cours valent dans chaque langue** : aucune date fixe, le sujet du TP
  seulement sur ses pages, **aucune réponse du TP hors de la correction protégée**, chaque
  schéma expliqué, liens externes en nouvel onglet et vérifiés dans la langue de la page.
- **Une faute relevée dans la racine pendant la traduction ne se corrige jamais en silence** :
  propose-la (regroupée, cliquable, plusieurs choix possibles) ; acceptée, elle part dans un
  commit séparé, et la traduction suit.
- **Un schéma déjà rendu ne se rend jamais de nouveau sur un autre poste** (PlantUML mesure
  le texte avec les polices du poste) : rends les traductions à part.
- **Les sorties de la racine ne bougent pas** : une génération qui change un octet de la
  racine est une régression.
- **Un lot de finitions** harmonise les écarts de termes relevés en route ; le lexique les
  consigne au fil des lots.

---

## 9. Les contrôles, à chaque lot

Parité des blocs (0 écart), blocs arabes compris ; aucun lien cassé ; aucun chiffre du TP
hors des pages du TP ; tables de traduction complètes et cohérentes ; fragments et menus à
jour (`generer_nav_sections.py --essai`, `generer_langues.py --essai`) ; `hreflang` ; sorties
de la racine identiques ; recette au navigateur (console vide, aucun débordement à 375 px,
groupe de langues qui retombe sur le même bloc, à l'aller et au retour, page arabe retournée
de droite à gauche, en clair et en sombre) ; après chaque mise en ligne, le site public
vérifié (200 pour les pages publiques, 401 sans identifiant pour les zones protégées).

**Terminé** quand chaque page, chaque piste, chaque QCM et chaque document a sa version dans
chaque langue, contrôlée ; que le groupe de langues retombe au même endroit partout ; et que
le plan de traduction, le lexique, les décisions, l'état d'avancement et `TODO.md` sont à
jour.

---

## 10. Pour commencer

1. Lis le dépôt du cours (structure, générateurs, `docs\`, `TODO.md`), `docs/I18N.md` du
   gabarit, `docs/LEXIQUE-ar.md` pour l'arabe, et les modèles de la section 3. Un cours créé
   avant les outils du miroir les reprend du gabarit (`site/assets/js/langue.js`,
   `langues-data.js`, `navigation.js`, `i18n.js`, et les outils du § A.9).
2. Fais l'inventaire chiffré du site à traduire. Un cours en blocs `data-tr` se convertit
   d'abord, une fois (`data_tr_vers_miroir.py --essai`, puis sans).
3. Pose les questions de cadrage, **une à une** (section 4).
4. Propose le plan par lots, puis attends l'accord de l'auteur pour lancer le lot 0.

Sur un cours qui n'a pas été créé depuis le template, les règles de son `CLAUDE.md`
s'appliquent ; à défaut, celles du § 2 du `CLAUDE.md` du template : secrets jamais lus,
commits au seul nom de l'auteur et sans mention d'IA, accord avant de commiter et de
pousser, puis, séparément, avant de mettre en ligne.
