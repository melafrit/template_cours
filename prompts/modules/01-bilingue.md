# Module 01 — Le bilingue : la version anglaise du cours, après le français

> **Quand l'activer.** Quand le cours doit exister en anglais : un public international, une
> filière anglophone, une diffusion plus large.
>
> **Paramètres.** `modules.bilingue.actif` ; `modules.bilingue.modele` : `"miroir"` (des
> pages anglaises sous `en/`) ou `"data-tr"` (les deux langues dans chaque page).
>
> **Place.** Phase 9 du tronc, une fois le français stable : contenus, évaluations,
> compléments et audio français validés. En modèle « data-tr », les blocs anglais peuvent
> s'écrire au fil des chapitres ; la relecture d'ensemble et l'audio anglais restent en
> phase 9.
>
> **Seul.** Sur un cours qui existe en français, donnez ce fichier à Claude dans le dossier
> du cours : il commence par la section 10.

---

## 1. Ce que le module produit

Le site **entièrement traduit, en détail** : chaque page publique et protégée, chaque
schéma et figure, chaque **piste audio** (la voix clonée de l'auteur, en anglais, Eleven
v4), chaque QCM et ses explications, le glossaire, les flashcards, la bibliographie, les
simulateurs, les activités, et les **documents à télécharger** (Word, PDF, ZIP, tableurs).

Un bouton **FR / EN en haut à droite** rouvre la page jumelle **au même endroit** : même
section, même paragraphe. Un **lexique** et un **guide de style** fixent les termes ; ils
servent ensuite au livret anglais (module 02) et aux podcasts anglais (module 03).

---

## 2. Choisir le modèle

| | Miroir (`en/`) | Blocs jumelés (`data-tr`) |
|---|---|---|
| Où vit l'anglais | une page jumelle par page, même chemin sous `en/` | dans la même page, `<span data-tr="en">` à côté du français |
| Ce que le gabarit fournit | rien encore : les outils viennent du cours d'architecture | tout : `i18n.js`, `ui-labels.js`, `verifier_i18n.py`, `docs/I18N.md` |
| Le bouton FR / EN | ouvre la jumelle au bloc lu, repéré par son rang | bascule sur place, sans recharger |
| Le référencement | `hreflang` page par page, deux adresses | une adresse par page |
| Le contrôle | `verifier_parite.py` : même suite de blocs, 0 écart | `verifier_i18n.py` : blocs équilibrés, clés jumelles |
| Convient à | un cours long, traduit lot par lot une fois le français stable | un cours court, écrit dans les deux langues dès le départ |

Recommandation : le **miroir** pour un cours long — le modèle qui a fonctionné sur le cours
d'architecture —, **data-tr** pour un cours court écrit bilingue d'emblée. Le choix est une
décision Dnn, prise au cadrage (phase 0) : il fixe `langues` dans `cours.json` (`["fr"]`
pour le miroir, l'anglais venant ensuite ; `["fr", "en"]` pour data-tr).

---

## 3. Le modèle : le cours d'architecture logicielle (lecture seule)

Le miroir a été fait de bout en bout sur `C:\projets\Cours\Cours_Architecture_Logicielle`
(lots 0 à 8, décisions D97 à D113, puis D118 pour le livret anglais). **Étudie-le avant de
concevoir quoi que ce soit, et n'y modifie jamais rien** — lis ses modules Python, ne les
importe pas. Ses fichiers secrets valent ceux du cours : ne les lis jamais.

| À lire | Ce qu'on y trouve |
|---|---|
| `docs\05-Plan-de-traduction-anglaise.md` | le plan par lots, l'inventaire, l'avancement |
| `docs\traduction\lexique.md`, `docs\traduction\guide-de-style.md` | les termes fixés, les écarts harmonisés, le style |
| `docs\01-Decisions-de-conception.md` | D97 à D113 |
| `docs\03-Guide-de-production.md`, § 8 bis | l'ordre de génération des deux langues |
| `assets\js\langue.js` | le bouton FR / EN qui garde la position |
| `outils\generer_langues.py`, `liens_langues.py`, `hreflang.py`, `documents_en.py` | la liste des pages traduites, les liens rebranchés, les balises, les noms anglais des documents |
| `outils\verifier_parite.py`, `verifier_traductions_en.py` | les contrôles |
| `outils\traduction_en.py`, `correction_en.py`, les modules `*_en.py` | les tables et les modules jumeaux |
| `outils\generer_audio.py` (options anglaises) | l'audio anglais |

Reprends ce qui s'applique, adapte ce qui diffère (`site/` dans un cours créé depuis le
template), et dis à l'auteur ce que tu reprends : chaque reprise est une décision Dnn.

---

## 4. Les décisions à faire valider

Une question à la fois ; entre parenthèses, le choix retenu sur le cours de référence.

- **Le modèle** (miroir), section 2.
- **L'accent des pistes anglaises** (*clear, well-articulated, professional General
  American accent* ; l'audio français garde son accent parisien marqué).
- **Les noms dans le code et les schémas** (en anglais).
- **Les termes délicats** : propose les options, avec ce qu'emploient les pays
  anglophones ; l'auteur tranche, le lexique enregistre.
- **Le découpage en lots** et leur ordre (section 7).
- **Les zones protégées** (leurs jumelles protégées exactement comme les françaises).
- **Les documents à télécharger** : lesquels traduire, et leurs noms anglais.

---

## 5. L'architecture à reprendre (modèle miroir)

- **Site miroir sous `en/`** : même chemin, même nom de fichier, **même suite de blocs**
  que la page française. `verifier_parite.py` contrôle les blocs (0 écart exigé) ; le
  bouton repère le bloc lu par son rang. Pour une liste que chaque langue trie à sa façon
  (le glossaire), une **clé commune** aux deux langues (`data-jumeau`).
- **La liste des pages traduites** (générée) : le menu et le bouton n'offrent l'anglais que
  là où la jumelle existe. Tant qu'une jumelle manque, le lien d'une page anglaise mène à la
  page française, marqué `hreflang="fr"` ; un outil de post-traitement rebranche tout dès
  qu'elle existe, documents compris (une seule table des noms anglais des documents).
- **Les générateurs écrivent les deux langues** : l'anglais vient de **modules jumeaux
  `*_en.py`** (mêmes signatures) ou de **tables `{texte français exact : texte anglais}`**,
  en **mode strict** — un texte sans traduction arrête la génération. Mêmes nombres qu'en
  français, écrits à l'anglaise (32,000 ; 99.5% ; 11 p.m.) ; aucun caractère français
  restant hors noms propres. **Les sorties françaises restent identiques à l'octet**,
  vérifiées à chaque lot.
- **Les schémas** : leurs textes passent par des tables de traduction ; la géométrie se
  recalcule sur l'anglais ; une étiquette anglaise n'est jamais plus longue là où la mise en
  page suit la largeur française. Chaque schéma garde sa **lecture élément par élément**,
  traduite.
- **Les balises `hreflang`** (fr, en, x-default, adresses absolues) sur toutes les pages
  publiques jumelles, posées en dernier dans l'ordre de génération ; jamais sur les pages
  protégées.
- **Les zones protégées** : leurs jumelles `en/…` sont protégées **exactement comme les
  françaises** ; à la mise en ligne, la protection d'abord (vérifiée en 401 sans
  identifiant), le contenu ensuite (module 08).
- **Les PDF exportés par Word** : un seul export à la fois (verrou), champs mis à jour,
  langue du PDF posée après l'export (fr-FR, en-US).

En modèle **data-tr**, le moteur du gabarit suffit : blocs jumelés dans le HTML, contenu des
composants dans `TEXTES = { fr, en }` avec `monter()` rejoué sur `tpl:langchange`, libellés
des moteurs dans `ui-labels.js` (`T()`), audio par langue (`chapitre-<N>-capsule-<langue>.mp3`),
contrôle par `verifier_i18n.py` ; le détail est dans `docs/I18N.md`. Les règles des
sections 6 à 9 valent de la même façon.

---

## 6. Les pistes audio

- **Eleven v4**, la voix clonée de l'auteur (la configuration ElevenLabs est secrète : le
  générateur la lit, Claude jamais) ; l'accent retenu (section 4) ; filtre la ligne qui
  affiche l'identifiant de voix.
- **Un témoin d'abord**, écouté et validé par l'auteur, puis la série ; durée et débit
  contrôlés par le générateur (module 04).
- Les scripts anglais vivent à côté des français (`docs/prompts/en/`), avec **les mêmes
  marqueurs** : mêmes faits, même ordre, autant de paragraphes et de balises de jeu
  (« speaking slowly » dans chacune), longueur à 10 % près ; nombres et sigles écrits pour
  la voix (« S.A.D. »), la transcription les écrit normalement.
- **Un texte enregistré ne se change jamais sans réenregistrer la piste** ; un écart se
  note dans `TODO.md`.

---

## 7. La méthode : des lots

Commence par **inventorier tout le site** (pages, générateurs, audio, schémas, documents,
zones protégées, volumes en mots et en caractères audio), puis propose un plan, par
exemple :

- **0** fondations : bouton, scripts bilingues, contrôles, lexique, guide de style ;
- **1** une page témoin complète : un chapitre, ses schémas, ses activités, son audio ;
- **2** les autres chapitres ; **3** les pages communes ; **4** les fiches et annexes ;
- **5** les QCM et leurs corrections expliquées ; **6** les zones protégées ;
- **7** les documents à télécharger ; **8** les finitions (`hreflang`, harmonisation des
  termes, recette complète, documentation).

Chaque lot suit le même circuit : production (agents en parallèle quand c'est utile, avec
une consigne écrite et un vérificateur) → contrôles → présentation du lot → témoin audio →
reste de l'audio → commit sur l'accord de l'auteur → mise en ligne sur un accord distinct →
question sur la suite.

---

## 8. Les règles et les pièges

- **Anglais américain**, ton du français (le vouvoiement devient « you »), typographie
  anglaise (pas d'espace avant « : »), titres en **Title Case**.
- Les règles du cours valent aussi en anglais : aucune date fixe, le sujet du TP seulement
  sur ses pages, **aucune réponse du TP hors de la correction protégée**, chaque schéma
  expliqué, liens externes en nouvel onglet et vérifiés.
- **Une faute relevée dans le français pendant la traduction ne se corrige jamais en
  silence** : propose-la (regroupée, cliquable, plusieurs choix possibles) ; acceptée, elle
  part dans un commit séparé, et la traduction suit.
- **Un schéma français déjà rendu ne se rend jamais de nouveau sur un autre poste**
  (PlantUML mesure le texte avec les polices du poste) : rends les anglais à part.
- **Les sorties françaises ne bougent pas** : une génération bilingue qui change un octet du
  français est une régression.
- **Un lot de finitions** harmonise les écarts de termes relevés en route ; le lexique les
  consigne au fil des lots.

---

## 9. Les contrôles, à chaque lot

Parité des blocs (0 écart) en miroir, ou `verifier_i18n.py` sans écart en data-tr ; aucun
lien cassé ; aucun chiffre du TP hors des pages du TP ; tables de traduction complètes et
cohérentes ; fragments et menus à jour (`generer_nav_sections.py --essai`) ; `hreflang` ;
sorties françaises identiques ; recette au navigateur (console vide, aucun débordement à
375 px, bouton FR / EN qui retombe sur le même bloc, à l'aller et au retour) ; après chaque
mise en ligne, le site public vérifié (200 pour les pages publiques, 401 sans identifiant
pour les zones protégées).

**Terminé** quand chaque page, chaque piste, chaque QCM et chaque document a sa version
anglaise, contrôlée ; que le bouton retombe au même endroit partout ; et que le plan de
traduction, le lexique, les décisions, l'état d'avancement et `TODO.md` sont à jour.

---

## 10. Pour commencer

1. Lis le dépôt du cours (structure, générateurs, `docs\`, `TODO.md`) et le modèle de la
   section 3.
2. Fais l'inventaire chiffré du site à traduire.
3. Pose les questions de cadrage, **une à une** (section 4).
4. Propose le plan par lots, puis attends l'accord de l'auteur pour lancer le lot 0.

Sur un cours qui n'a pas été créé depuis le template, les règles de son `CLAUDE.md`
s'appliquent ; à défaut, celles du § 2 du `CLAUDE.md` du template : secrets jamais lus,
commits au seul nom de l'auteur et sans mention d'IA, accord avant de commiter et de
pousser, puis, séparément, avant de mettre en ligne.
