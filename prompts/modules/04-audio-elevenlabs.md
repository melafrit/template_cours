# Module 04 — L'audio : les capsules du cours, à la voix clonée de l'auteur

> **Quand l'activer.** Presque toujours : une capsule d'ouverture par chapitre, une par
> schéma ou par fiche, le TP pas à pas, « ce qui est attendu ». L'étudiant entend l'auteur
> lui présenter ce qu'il va lire.
>
> **Paramètres.** `modules.audio` : `actif`, `capsules` (les familles de capsules
> retenues).
>
> **Place.** Phase 8 du tronc, une fois les textes des pages stables ; l'audio anglais vient
> avec le module 01, en phase 9.
>
> **Seul.** Sur un cours qui existe déjà, donnez ce fichier à Claude dans le dossier du
> cours : il commence par la section 7.

---

## 1. Ce que le module produit

Des **capsules audio** dites par la **voix clonée de l'auteur** (ElevenLabs, **Eleven
v4**), avec leur **transcription** sous chaque lecteur, et la **playlist** de tout le cours.
Une fiche de production par famille de capsules, dans `docs/prompts/Capsules_*.md`, est la
**source unique** : le script dit à la voix et la transcription affichée en découlent.

---

## 2. Ce qui est fixé (CLAUDE.md, § 2)

- **Eleven v4** pour toutes les pistes, la voix clonée de l'auteur (`outils/elevenlabs.json`,
  secret : le générateur le lit, Claude jamais).
- **L'accent** : « strong Parisian French accent » pour les pistes françaises, ajouté par le
  générateur aux balises de jeu ; pour les pistes anglaises, l'accent retenu avec le module
  01 (sur le cours de référence : *clear, well-articulated, professional General American
  accent*).
- **Le ton** : pédagogique, académique, professionnel et motivant, au vouvoiement ; une
  lecture posée, « speaking slowly » dans les balises des capsules explicatives.
- **La forme d'une capsule explicative** : elle définit la notion, lit l'exemple élément par
  élément, relie aux autres pièces, finit par le piège et la phrase à retenir.
- **Un témoin d'abord**, écouté par l'auteur sur la page, la série ensuite. Voir
  `prompts/14_capsules_audio.md`.

---

## 3. Les décisions à faire valider

Une question à la fois.

- **Les familles de capsules** (`modules.audio.capsules`) : accueil, ouverture de chapitre,
  une par schéma, une par fiche, TP pas à pas, « ce qui est attendu »…
- **La durée visée** par famille (le contrôle qualité déduit la fenêtre de chaque piste de
  ses mots).
- **Le témoin** : quelle capsule, sur quelle page.

---

## 4. La méthode

1. **Les fiches** (`prompts/14_capsules_audio.md`) : une par famille, dans
   `docs/prompts/Capsules_*.md`, avec les marqueurs exacts « **Nom exact du fichier :** »,
   « **▶️ Script ElevenLabs** », « **📄 Transcription affichée sur la page** ». Le nom du
   fichier attendu par la page sert de clé : `chapitre-<N>-capsule-<langue>.mp3`, avec le
   suffixe de langue (sans lui, l'auditeur anglophone entend du français).
2. **Les contrôles d'abord** : `outils/verifier_elevenlabs.py` (clé, voix, modèle v4,
   quota), puis `outils/generer_audio.py --essai` (ce qui serait généré, sans dépenser).
3. **Le témoin** : `generer_audio.py --temoin --limite 1` produit une prise à côté, dans
   `outils/quarantaine/temoins/`, sans rien déposer ni remplacer. L'auteur l'écoute. **STOP.**
   Tant qu'aucun témoin n'existe pour le modèle, une série est refusée.
4. **La série**, chapitre par chapitre (`--chapitre N`). Le générateur contrôle chaque prise
   — débit (105 à 190 mots par minute en v4), durée déduite des mots, silences (3,6 s au
   plus) — et met en quarantaine ce qui sort des clous, avec la raison ; il n'écrase rien
   sans `--force`. Une prise trop rapide : une reprise, puis « speaking slowly ».
5. **Après la série** : `outils/synchroniser_capsules.py` (les transcriptions des pages,
   d'après les fiches), puis `outils/generer_playlist.py` (l'index de toutes les pistes).

---

## 5. Les pièges connus

- **Un texte enregistré ne se change jamais sans réenregistrer la piste** : la
  transcription et le son divergeraient sans que personne l'entende. Un écart se note dans
  `TODO.md`.
- **Une capsule partie en ligne à 67 mots par minute au lieu de 145** : le même texte étiré
  sur le double du temps, faute d'un réglage. D'où le contrôle de chaque prise.
- **La ligne qui affiche l'identifiant de voix** se filtre de toute sortie montrée.
- **L'ordre des générateurs** : la playlist indexe les fichiers audio réels, elle passe
  après la génération et la synchronisation (CLAUDE.md, § 4).

---

## 6. Les contrôles

Chaque capsule attendue par une page existe, au bon nom ; sa transcription est celle de la
fiche ; la playlist est régénérée ; aucune prise en quarantaine n'est restée sans
décision ; au navigateur, chaque lecteur joue, le mini-lecteur suit, la console est vide.

**Terminé** quand chaque capsule retenue est en ligne, écoutée au moins en témoin par
l'auteur, et que les fiches, l'état d'avancement et `TODO.md` sont à jour.

---

## 7. Pour commencer

1. Lis les fiches existantes de `docs/prompts/` et `prompts/14_capsules_audio.md`.
2. Fais l'inventaire des capsules que les pages réclament, et de celles qui existent.
3. Pose les questions de cadrage, **une à une** (section 3).
4. Écris la fiche d'une famille, lance les contrôles, puis le témoin ; attends l'écoute de
   l'auteur avant toute série.

Sur un cours qui n'a pas été créé depuis le template, les règles de son `CLAUDE.md`
s'appliquent ; à défaut, celles du § 2 du `CLAUDE.md` du template.
