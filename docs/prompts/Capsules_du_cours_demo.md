# Capsules d'ouverture — cours de démonstration

**Six capsules à enregistrer** : une par chapitre, dans les deux langues. Elles
se placent en tête de chapitre, avant la première section.

Ce fichier est la **source unique** : le script part d'ici, la transcription
affichée sur la page aussi. Ne modifiez jamais la transcription dans le HTML —
modifiez-la ici, puis relancez `python3 outils/synchroniser_capsules.py`.

## ⚠️ À lire avant de commencer

- **Durée visée : 40 à 70 secondes.** Chaque script fait environ 115 mots
  parlés, soit ~47 s au débit médian de 146 mots par minute. C'est court à
  dessein : une capsule d'ouverture situe, elle n'enseigne pas.
- **Le contrôle qualité du générateur est calibré sur des capsules de 1 à 2
  minutes.** Ces capsules-ci sont plus brèves, la tolérance est donc déclarée
  explicitement pour chacune — sans quoi elles seraient rejetées comme « trop
  courtes ».
- **Réglages ElevenLabs v3 :** votre clone vocal, `Stability` ≈ 0,45,
  `Similarity` 0,80, `Speed` 1,0.
- **Balises rares.** `[pause]` marque une respiration, pas une virgule. Sur
  quarante-cinq secondes, deux suffisent.
- **Les capsules anglaises passent par la même voix.** Un clone français lisant
  l'anglais a un accent : écoutez la première prise avant de générer les deux
  autres. Si le résultat ne convient pas, créez une seconde voix chez
  ElevenLabs et renseignez `voix_id_en` dans `outils/elevenlabs.json`.
- **Format :** MP3, voix seule, sans musique.

## 📋 Récapitulatif — les six fichiers

Tous dans `site/assets/media/voix/`.

| # | Chapitre | Langue | Nom exact du fichier | Durée |
|---|---|---|---|---|
| 1 | 1 — Cadrer son cours | FR | `chapitre-1-capsule-fr.mp3` | ≈ 47 s |
| 2 | 1 — Scoping your course | EN | `chapitre-1-capsule-en.mp3` | ≈ 47 s |
| 3 | 2 — Structurer le contenu | FR | `chapitre-2-capsule-fr.mp3` | ≈ 47 s |
| 4 | 2 — Structuring the content | EN | `chapitre-2-capsule-en.mp3` | ≈ 47 s |
| 5 | 3 — Créer les ressources | FR | `chapitre-3-capsule-fr.mp3` | ≈ 50 s |
| 6 | 3 — Creating the resources | EN | `chapitre-3-capsule-en.mp3` | ≈ 50 s |

---

## Capsule 1 FR — Chapitre 1, « Cadrer son cours »

- **Nom exact du fichier :** `chapitre-1-capsule-fr.mp3`
- **Emplacement exact :** `site/assets/media/voix/chapitre-1-capsule-fr.mp3`
- **Durée visée :** ≈ 47 s (115 mots parlés, tolérance 0 min 35 → 1 min 10)

- [x] Capsule générée et déposée — contrôlée par outils/generer_audio.py

**▶️ Script ElevenLabs**

```
[warmly] Bienvenue dans le chapitre vitrine.

[thoughtful] Il fait deux choses à la fois. Il enseigne quelque chose de réel — les trois décisions qu'il faut prendre avant d'écrire un cours — et il exerce tous les composants du moteur, pour que vous les voyiez fonctionner.

[pause]

[curious] Ces trois décisions sont : pour qui, pour quoi faire, et autour de quoi. Elles se prennent dans cet ordre, parce que chacune restreint le champ de la suivante.

[serious] Et la tentation est toujours la même : ouvrir un traitement de texte et commencer par le début. On produit alors ce qu'on sait, pas ce dont l'apprenant a besoin.

[warmly] Prenez ce chapitre comme un modèle à recopier, autant que comme un chapitre à lire.
```

**📄 Transcription affichée sur la page**

```
Bienvenue dans le chapitre vitrine. Il fait deux choses à la fois : il enseigne quelque chose de réel — les trois décisions qu'il faut prendre avant d'écrire un cours — et il exerce tous les composants du moteur, pour que vous les voyiez fonctionner. Ces trois décisions sont : pour qui, pour quoi faire, et autour de quoi. Elles se prennent dans cet ordre, parce que chacune restreint le champ de la suivante. Et la tentation est toujours la même : ouvrir un traitement de texte et commencer par le début. On produit alors ce qu'on sait, pas ce dont l'apprenant a besoin. Prenez ce chapitre comme un modèle à recopier, autant que comme un chapitre à lire.
```

---

## Capsule 2 EN — Chapter 1, “Scoping your course”

- **Nom exact du fichier :** `chapitre-1-capsule-en.mp3`
- **Emplacement exact :** `site/assets/media/voix/chapitre-1-capsule-en.mp3`
- **Durée visée :** ≈ 47 s (115 mots parlés, tolérance 0 min 35 → 1 min 10)

- [x] Capsule générée et déposée — contrôlée par outils/generer_audio.py

**▶️ Script ElevenLabs**

```
[warmly] Welcome to the showcase chapter.

[thoughtful] It does two things at once. It teaches something real — the three decisions to make before writing a course — and it exercises every component of the engine, so you can see them working.

[pause]

[curious] Those three decisions are: for whom, to do what, and around what. They come in that order, because each one narrows the field of the next.

[serious] And the temptation is always the same: open a document and start at the beginning. You then produce what you know, not what the learner needs.

[warmly] Treat this chapter as a model to copy, as much as a chapter to read.
```

**📄 Transcription affichée sur la page**

```
Welcome to the showcase chapter. It does two things at once: it teaches something real — the three decisions to make before writing a course — and it exercises every component of the engine, so you can see them working. Those three decisions are: for whom, to do what, and around what. They come in that order, because each one narrows the field of the next. And the temptation is always the same: open a document and start at the beginning. You then produce what you know, not what the learner needs. Treat this chapter as a model to copy, as much as a chapter to read.
```

---

## Capsule 3 FR — Chapitre 2, « Structurer le contenu »

- **Nom exact du fichier :** `chapitre-2-capsule-fr.mp3`
- **Emplacement exact :** `site/assets/media/voix/chapitre-2-capsule-fr.mp3`
- **Durée visée :** ≈ 47 s (115 mots parlés, tolérance 0 min 35 → 1 min 10)

- [x] Capsule générée et déposée — contrôlée par outils/generer_audio.py

**▶️ Script ElevenLabs**

```
[thoughtful] Structurer, c'est décider dans quel ordre, et par quels morceaux.

[curious] Trois idées suffisent pour ce chapitre. La première : une séquence porte une question, un contenu, et une vérification. C'est presque toujours la vérification qui manque.

[pause]

[serious] La deuxième : découper n'est pas hacher. Une séquence courte doit se suffire à elle-même — si l'apprenant s'arrête là, il doit en ressortir avec quelque chose d'utilisable.

[thoughtful] La troisième, et c'est celle qui surprend le plus : l'ordre juste est celui des prérequis, pas celui de l'importance. On commence par ce qui rend le reste possible, pas par ce qui compte le plus.

[warmly] Le reste en découle.
```

**📄 Transcription affichée sur la page**

```
Structurer, c'est décider dans quel ordre, et par quels morceaux. Trois idées suffisent pour ce chapitre. La première : une séquence porte une question, un contenu, et une vérification — c'est presque toujours la vérification qui manque. La deuxième : découper n'est pas hacher. Une séquence courte doit se suffire à elle-même : si l'apprenant s'arrête là, il doit en ressortir avec quelque chose d'utilisable. La troisième, et c'est celle qui surprend le plus : l'ordre juste est celui des prérequis, pas celui de l'importance. On commence par ce qui rend le reste possible, pas par ce qui compte le plus. Le reste en découle.
```

---

## Capsule 4 EN — Chapter 2, “Structuring the content”

- **Nom exact du fichier :** `chapitre-2-capsule-en.mp3`
- **Emplacement exact :** `site/assets/media/voix/chapitre-2-capsule-en.mp3`
- **Durée visée :** ≈ 47 s (115 mots parlés, tolérance 0 min 35 → 1 min 10)

- [x] Capsule générée et déposée — contrôlée par outils/generer_audio.py

**▶️ Script ElevenLabs**

```
[thoughtful] Structuring means deciding in which order, and in what pieces.

[curious] Three ideas are enough for this chapter. The first: a sequence carries a question, some content, and a check. It is almost always the check that goes missing.

[pause]

[serious] The second: breaking up is not chopping up. A short sequence must stand on its own — if the learner stops there, they must leave with something usable.

[thoughtful] The third, and this is the one that surprises most: the right order is that of prerequisites, not of importance. You start with what makes the rest possible, not with what matters most.

[warmly] The rest follows.
```

**📄 Transcription affichée sur la page**

```
Structuring means deciding in which order, and in what pieces. Three ideas are enough for this chapter. The first: a sequence carries a question, some content, and a check — it is almost always the check that goes missing. The second: breaking up is not chopping up. A short sequence must stand on its own: if the learner stops there, they must leave with something usable. The third, and this is the one that surprises most: the right order is that of prerequisites, not of importance. You start with what makes the rest possible, not with what matters most. The rest follows.
```

---

## Capsule 5 FR — Chapitre 3, « Créer les ressources »

- **Nom exact du fichier :** `chapitre-3-capsule-fr.mp3`
- **Emplacement exact :** `site/assets/media/voix/chapitre-3-capsule-fr.mp3`
- **Durée visée :** ≈ 50 s (122 mots parlés, tolérance 0 min 35 → 1 min 10)

- [x] Capsule générée et déposée — contrôlée par outils/generer_audio.py

**▶️ Script ElevenLabs**

```
[thoughtful] Trois formats, trois intentions.

[curious] Le texte sert à ce qu'on relit : une définition, une procédure, un chiffre exact. L'audio sert à ce qui se transmet par la voix : une intention, une nuance, un encouragement. Le schéma sert à ce qui ne se dit pas en une phrase.

[pause]

[serious] Le piège est de choisir d'après l'outil dont on dispose, et non d'après ce qu'on veut obtenir. On a un micro, donc on enregistre. Une définition dite à l'oral se perd : il faudrait la réécouter, et personne ne réécoute.

[thoughtful] Retenez surtout ceci : deux formats qui se répètent valent moins qu'un seul bien choisi.
```

**📄 Transcription affichée sur la page**

```
Trois formats, trois intentions. Le texte sert à ce qu'on relit : une définition, une procédure, un chiffre exact. L'audio sert à ce qui se transmet par la voix : une intention, une nuance, un encouragement. Le schéma sert à ce qui ne se dit pas en une phrase. Le piège est de choisir d'après l'outil dont on dispose, et non d'après ce qu'on veut obtenir : on a un micro, donc on enregistre. Une définition dite à l'oral se perd — il faudrait la réécouter, et personne ne réécoute. Retenez surtout ceci : deux formats qui se répètent valent moins qu'un seul bien choisi.
```

---

## Capsule 6 EN — Chapter 3, “Creating the resources”

- **Nom exact du fichier :** `chapitre-3-capsule-en.mp3`
- **Emplacement exact :** `site/assets/media/voix/chapitre-3-capsule-en.mp3`
- **Durée visée :** ≈ 50 s (122 mots parlés, tolérance 0 min 35 → 1 min 10)

- [x] Capsule générée et déposée — contrôlée par outils/generer_audio.py

**▶️ Script ElevenLabs**

```
[thoughtful] Three formats, three intentions.

[curious] Text is for what gets re-read: a definition, a procedure, an exact figure. Audio is for what carries in a voice: an intention, a nuance, an encouragement. A diagram is for what no single sentence can hold.

[pause]

[serious] The trap is choosing from the tool you happen to own, rather than from what you want to achieve. You have a microphone, so you record. A definition delivered by voice is lost: you would have to listen again, and nobody listens again.

[thoughtful] Above all, remember this: two formats that repeat each other are worth less than one well chosen.
```

**📄 Transcription affichée sur la page**

```
Three formats, three intentions. Text is for what gets re-read: a definition, a procedure, an exact figure. Audio is for what carries in a voice: an intention, a nuance, an encouragement. A diagram is for what no single sentence can hold. The trap is choosing from the tool you happen to own, rather than from what you want to achieve: you have a microphone, so you record. A definition delivered by voice is lost — you would have to listen again, and nobody listens again. Above all, remember this: two formats that repeat each other are worth less than one well chosen.
```
