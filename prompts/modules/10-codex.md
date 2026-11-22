# Module 10 · Codex : les illustrations du cours

> **Quand l'activer.** Quand le cours a des illustrations : les cartes des chapitres et de
> l'accueil, les portraits des personnes du cas, les scènes qui accompagnent un chapitre.
>
> **Paramètres.** `modules.complements.illustrations` : `actif`, et `outil: "Codex"`.
>
> **Place.** Phase 7 du tronc, avec les compléments (module 09), une fois en place les pages
> qui appellent les images : chaque page réserve l'emplacement au nom exact du fichier
> attendu, et une image déposée à ce nom apparaît sans toucher au code.
>
> **Seul.** Sur un cours qui existe déjà, donnez ce fichier à Claude dans le dossier du
> cours : il commence par la section 9.

---

## 1. Ce que le module produit

- **Les illustrations**, en WebP de moins de 350 Ko, dans `site/assets/media/illustrations/`,
  aux noms que les pages attendent déjà. Les cartes de chapitre de l'accueil, par exemple,
  s'appellent `chapitre-<N>-carte.webp`, et `outils/accueil.py` les affiche dès qu'elles
  sont déposées.
- **Le fichier des prompts**, `docs/illustrations/PROMPTS-ILLUSTRATIONS.md` : la charte de
  style (le bloc `STYLE`), les règles de contenu (« Ce qu'aucune image ne montre »), la bible
  des personnages, une fiche par image, les contrôles. Les prompts sont en anglais, où les
  générateurs sont plus fiables ; le contexte est en français.
- **Le message qui lance Codex**, et le récapitulatif que Codex rend à la fin.

---

## 2. Le modèle

`C:\projets\Cours\Cours_EADL_ERIS_Etude_Avant_Projet` a produit ainsi ses 19 illustrations
neuves, quatre portraits puis quinze scènes, après un témoin validé (décision D49, 20 octobre
2026). **Lis-le avant de concevoir quoi que ce soit, et n'y modifie jamais rien** ; ses
fichiers secrets valent ceux du cours, et ne se lisent jamais.

| À lire | Ce qu'on y trouve |
|---|---|
| `docs\illustrations\PROMPTS-ILLUSTRATIONS.md` | la charte, les règles de contenu, la bible et ses « paires à surveiller », les fiches, les contrôles |
| `docs\illustrations\INSTRUCTIONS-CODEX.md` | le message donné à Codex, la conversion, la relecture, la reprise d'une seule image, le plan B |
| `docs\01-Decisions-de-conception.md`, D49 | la relecture : les défauts retenus, les images refaites, celles retouchées au pixel près |
| `outils\convertir_illustrations.py` | la conversion en WebP (recadrage centré, moins de 350 Ko), `--verifier`, `--force` |

Le cours de veille technologique CDWFS/ASRC reprend la même charte et les mêmes personnages
(sa décision D19) : un seul monde, avec les mêmes visages et le même style d'un cours à
l'autre. Le gabarit n'a pas
encore son propre kit d'illustration (registre, lot 5) : d'ici là, reprends celui du cours
EADL, et chaque reprise est une décision Dnn.

---

## 3. Codex sur le poste

Claude Code vérifie d'abord que Codex est là, avec `codex --version`, puis
`codex login status`.

**Sans Codex**, Claude donne la procédure officielle et s'arrête : l'auteur installe et se
connecte lui-même, et Claude ne s'authentifie jamais à sa place. La procédure ci-dessous a
été vérifiée en ligne le 22 novembre 2026, sur le dépôt `openai/codex` et la documentation
d'OpenAI ; revérifie-la avant de la donner.

- **Installer.** Sous Windows, depuis une nouvelle fenêtre PowerShell :
  `powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 | iex"`.
  Avec Node.js, sur tout système : `npm install -g @openai/codex` (c'est ainsi qu'il est
  installé sur le poste de l'auteur, en version 0.163.0). Sur Mac, Homebrew :
  `brew install --cask codex`.
- **Se connecter.** Lancer `codex` et choisir « Sign in with ChatGPT », avec un forfait
  Plus, Pro, Business, Edu ou Enterprise ; `codex login status` dit l'état de la connexion.
- **Mettre à jour.** La commande d'installation, de nouveau ; avec Homebrew,
  `brew upgrade --cask codex`.

La documentation se contredit sur Windows : sa page d'installation demande WSL2, son README
donne l'installateur PowerShell natif. Sur le poste de l'auteur, Codex tourne en natif.

**Les images.** Codex les produit avec sa génération d'images intégrée (`gpt-image-2`), qui
compte dans ses limites d'usage : celles du compte ChatGPT de l'auteur. Dans un message,
`$imagegen` appelle explicitement cette génération ; l'option `-i` joint une image de
référence (un portrait existant, pour garder un visage).

---

## 4. Les décisions à faire valider

Une question à la fois ; entre parenthèses, le choix retenu sur le cours EADL.

- **La liste des images** et leurs noms, ceux que les pages attendent.
- **La charte** : reprendre celle des cours précédents, ou en poser une nouvelle (reprise mot
  pour mot, « un seul monde »).
- **La bible des personnages** : une ligne `CHARACTER` par personne du cas, recopiée mot pour
  mot d'une fiche à l'autre, et les paires de personnes à ne jamais confondre.
- **Les couleurs de filière** dans les images (celles du site : cordons de badge, couvertures
  de dossier, accents).
- **Le témoin** : une image, souvent le premier portrait, qui fixe le style et les visages.

---

## 5. La méthode

1. **Le fichier des prompts**, écrit puis validé (STOP) : charte, règles, bible, fiches,
   contrôles. Rien de ce que liste « Ce qu'aucune image ne montre » ne passe dans une fiche :
   aucun texte lisible, et rien qui souffle une réponse de l'épreuve ou du TP.
2. **Un dossier dédié, hors du dépôt**, qui ne contient que le fichier des prompts, les images
   de référence et un dossier de sortie. Codex y travaille seul : il ne voit ni le dépôt ni ses
   secrets.
3. **Le témoin.** Claude lance Codex lui-même sur une seule image, puis la montre à l'auteur
   (STOP) :

   ```bash
   codex exec -C <dossier dédié> --skip-git-repo-check -s workspace-write \
     -o <dossier dédié>/recapitulatif.md "<le message>"
   ```

   `-C` fixe le dossier de travail, `--skip-git-repo-check` l'autorise hors d'un dépôt Git,
   `-s workspace-write` borne l'écriture à ce dossier, `-o` garde le dernier message de Codex,
   son récapitulatif.
4. **La série**, après l'accord de l'auteur, avec le même message pour toutes les images. Le
   message, sur le modèle de `INSTRUCTIONS-CODEX.md` du cours EADL, dit à Codex :
   - de ne faire que générer et enregistrer des PNG (`$imagegen`), portraits d'abord, en carré
     1024 × 1024, puis scènes, en paysage 1536 × 1024 ;
   - de composer chaque prompt comme le fichier le décrit (bloc `STYLE`, ligne `SCENE`,
     composition), sans changer la description des personnes ;
   - de joindre seulement les références prévues par chaque fiche, jamais un portrait de la
     colonne « Ne jamais joindre » ;
   - d'enregistrer chaque image sous son nom exact, dans le dossier de sortie et nulle part
     ailleurs ;
   - de contrôler chaque image contre sa fiche et contre la bible, trois essais au plus, puis
     de garder le meilleur et de signaler le défaut ;
   - de ne modifier aucun autre fichier et de ne faire aucun commit ;
   - de finir par un tableau récapitulatif (fiche, fichier, essais, références jointes,
     réserves).
5. **La conversion.** Claude recopie les PNG dans `docs/illustrations/sources/` (non
   versionné), puis les convertit en WebP de moins de 350 Ko dans
   `site/assets/media/illustrations/`. La vérification annonce « N/N illustrations en
   place », sans ligne « À REVOIR ».
6. **La relecture**, par Claude puis par l'auteur (STOP) : chaque page qui porte une image,
   en clair et en sombre, à 1280 et 375 px, dans chaque filière. Aucun texte dans l'image, rien
   qui souffle une réponse, des visages reconnaissables d'une image à l'autre, les bonnes
   couleurs de filière, un sujet qui reste lisible une fois l'image recadrée (sinon, un point
   d'intérêt par `object-position`).
7. **Une image à reprendre** se reprend seule, avec un message ciblé : ce qui ne va pas, la
   fiche et les références à joindre, le fichier à écraser, trois essais au plus, aucun autre
   fichier modifié. Puis la conversion repasse : seule l'image plus récente que son WebP est
   reconvertie.

Le plan B du cours EADL, sans Codex, passe par ChatGPT (une seule conversation pour toute la
série, qui garde mieux le style) : il ne se lance que si l'auteur le choisit.

---

## 6. Ce qui est versionné

| Dossier ou fichier | Versionné ? | Pourquoi |
|---|---|---|
| `docs/illustrations/PROMPTS-ILLUSTRATIONS.md` | **Oui** | la source de chaque image, pour la refaire |
| `docs/illustrations/sources/` | Non | des images brutes, lourdes et régénérables |
| `site/assets/media/illustrations/*.webp` | **Oui** | les images publiées |
| le dossier dédié de Codex | Non | hors du dépôt, effacé une fois les images reprises |

---

## 7. Les pièges

- **Codex avait pris l'empreinte de tout le dépôt** pour prouver qu'il n'avait rien changé
  (cours EADL, D49) : le dossier dédié, hors du dépôt, l'en empêche.
- **Deux personnages qui se ressemblent** : une référence d'image trop proche, la même tenue.
  La bible les distingue, et une paire à surveiller ne se joint jamais en référence.
- **Du texte parasite** sur les écrans, les badges, les horloges ou les véhicules : contrôle
  image par image, puis reprise ciblée.
- **Une image qui souffle une réponse**, comme l'architecture que juge l'épreuve : un schéma à
  l'écran reste abstrait, incomplet, et ne répond à rien.
- **Des couleurs de filière confondues** (dans le cours EADL, le cadre du milieu de la
  continuité était violet, la couleur d'ERIS, au lieu de l'indigo de sa fiche) : retouche au
  pixel près, les originaux de Codex gardés à part.
- **Un visage coupé** une fois l'image recadrée dans sa page : un point d'intérêt
  (`object-position`).

---

## 8. Les contrôles

`N/N illustrations en place`, aucune « À REVOIR » ; chaque WebP sous 350 Ko ; le texte
alternatif de chaque image dans sa page, inchangé ; `python3 outils/generer_fragments.py`
relancé, puis son `--essai` à jour, car les cartes de chapitre de l'accueil ne prennent leur
image qu'à la génération ; recette au navigateur (console vide, clair et sombre, 1280 et
375 px, chaque filière).

**Terminé** quand chaque emplacement a son image, relue et validée par l'auteur ; que le
fichier des prompts permet de refaire chacune ; et que les décisions, l'état d'avancement et
`TODO.md` sont à jour.

---

## 9. Pour commencer

1. Vérifie Codex (`codex --version`, `codex login status`) ; sans lui, donne la procédure de
   la section 3 et arrête-toi.
2. Lis le modèle de la section 2, sans rien y modifier.
3. Fais l'inventaire des emplacements d'images du cours, avec leurs noms et leurs dimensions.
4. Pose les questions de cadrage, **une à une** (section 4).
5. Écris le fichier des prompts, fais-le valider, puis lance le témoin.

Sur un cours qui n'a pas été créé depuis le template, les règles de son `CLAUDE.md`
s'appliquent ; à défaut, celles du § 2 du `CLAUDE.md` du template : secrets jamais lus,
commits au seul nom de l'auteur et sans mention d'IA, accord avant de commiter et de
pousser, puis, séparément, avant de mettre en ligne.
