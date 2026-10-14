# Capsules d'ouverture — cours de démonstration

**Six capsules à enregistrer** : une par chapitre, dans les deux langues. Elles
se placent en tête de chapitre, avant la première section.

Ce fichier est la **source unique** : le script part d'ici, la transcription
affichée sur la page aussi. Ne modifiez jamais la transcription dans le HTML —
modifiez-la ici, puis relancez `python3 outils/synchroniser_capsules.py`.

## ⚠️ À lire avant de commencer

> **Une fiche d'une autre génération.** Ces six capsules de démonstration ont été
> écrites et générées en **Eleven v3** (balises `[warmly]`, `[pause]`). Tout cours
> créé depuis le template génère désormais en **Eleven v4**, avec l'accent retenu par
> l'auteur ajouté par le générateur, sans `[pause]`, témoin d'abord : voir
> `prompts/14_capsules_audio.md`. Cette fiche reste comme exemple du **format** — les
> marqueurs que lit le générateur —, pas du ton. Elle n'est pas recopiée dans un cours
> créé.

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

---

## Podcast 1 FR — Chapitre 1

- **Nom exact du fichier :** `chapitre-1-podcast.fr.mp3`
- **Emplacement exact :** `site/assets/media/podcasts/chapitre-1-podcast.fr.mp3`
- **Durée visée :** ≈ 2 min (290 mots parlés, tolérance 1 min 30 → 2 min 40)

- [x] Podcast généré et déposé — contrôlé par outils/generer_audio.py

**▶️ Script ElevenLabs**

```
[warmly] Quelques minutes pour poser ce que le chapitre 1 va vous demander de décider.

[pause]

[thoughtful] Un cours mal cadré se répare mal. On s'en aperçoit à la troisième séance, quand il est trop tard pour tout reprendre. Le cadrage, c'est ce qu'on fait avant d'écrire la première ligne — et c'est précisément ce qu'on saute, parce qu'on a hâte de produire.

[serious] Trois décisions, dans un ordre qui n'est pas négociable. Pour qui. Pour quoi faire. Autour de quoi.

[curious] Le public d'abord, et cela surprend. On croit souvent qu'un cours part de ses objectifs. Mais tant qu'on ignore qui apprend, on ne peut ni fixer un objectif atteignable, ni juger si un fil rouge parlera. Et attention à la façon de décrire ce public : « étudiants de master » ne décrit personne. Ce qui décide, ce sont les prérequis réellement acquis, le temps disponible, et les contraintes matérielles. C'est la troisième qu'on oublie, et souvent la plus déterminante.

[pause]

[thoughtful] Les objectifs ensuite. Un objectif dit ce que l'apprenant sera capable de faire, pas ce qu'il aura vu ou compris. Le test est simple : si vous ne pouvez pas imaginer l'exercice qui prouverait l'objectif atteint, il est mal écrit — et vous ne pourrez pas évaluer.

[curious] Le fil rouge enfin. Un cas, un projet, un scénario qui traverse tout le cours. Il répond par avance à la question que l'apprenant se pose à chaque chapitre : à quoi cela va-t-il me servir. Et il sert d'arbitre le jour où l'on vous retire une séance.

[warmly] Chacune de ces trois décisions restreint le champ de la suivante. C'est ce qui rend le cadrage utile — et c'est pour cela que les sauter ne fait pas gagner de temps : cela le déplace vers la refonte. Bonne lecture.
```

**📄 Transcription affichée sur la page**

```
Quelques minutes pour poser ce que le chapitre 1 va vous demander de décider. Un cours mal cadré se répare mal : on s'en aperçoit à la troisième séance, quand il est trop tard pour tout reprendre. Trois décisions, dans un ordre qui n'est pas négociable : pour qui, pour quoi faire, autour de quoi. Le public d'abord — tant qu'on ignore qui apprend, on ne peut ni fixer un objectif atteignable, ni juger si un fil rouge parlera. Les objectifs ensuite : un objectif dit ce que l'apprenant sera capable de faire, et si vous ne pouvez pas imaginer l'exercice qui le prouverait, il est mal écrit. Le fil rouge enfin, qui répond à « à quoi cela va-t-il me servir » et sert d'arbitre quand il faut couper. Chacune restreint le champ de la suivante : c'est ce qui rend le cadrage utile.
```

---

## Podcast 2 EN — Chapter 1

- **Nom exact du fichier :** `chapitre-1-podcast.en.mp3`
- **Emplacement exact :** `site/assets/media/podcasts/chapitre-1-podcast.en.mp3`
- **Durée visée :** ≈ 2 min (290 mots parlés, tolérance 1 min 30 → 2 min 40)

- [x] Podcast généré et déposé — contrôlé par outils/generer_audio.py

**▶️ Script ElevenLabs**

```
[warmly] A few minutes to set out what chapter one will ask you to decide.

[pause]

[thoughtful] A badly scoped course is hard to repair. You notice on the third session, when it is too late to start over. Scoping is what you do before writing a single line — and it is exactly what gets skipped, because you are impatient to produce.

[serious] Three decisions, in an order that is not negotiable. For whom. To do what. Around what.

[curious] The audience first, and that surprises people. We often believe a course starts from its objectives. But until you know who is learning, you can neither set a reachable objective nor judge whether a through-line will land. And mind how you describe that audience: "master's students" describes nobody. What decides are the prerequisites actually acquired, the time available, and the practical constraints. The third is the forgotten one, and often the decisive one.

[pause]

[thoughtful] Objectives next. An objective states what the learner will be able to do, not what they will have seen or understood. The test is simple: if you cannot picture the exercise that would prove it reached, it is badly written — and you will not be able to assess.

[curious] The through-line last. A case, a project, a scenario running across the whole course. It answers in advance the question the learner asks at every chapter: what will this be used for. And it acts as the arbiter on the day a session is taken away from you.

[warmly] Each of these three decisions narrows the field of the next. That is what makes scoping useful — and why skipping them does not save time: it moves the time to the rewrite. Enjoy the chapter.
```

**📄 Transcription affichée sur la page**

```
A few minutes to set out what chapter one will ask you to decide. A badly scoped course is hard to repair: you notice on the third session, when it is too late to start over. Three decisions, in an order that is not negotiable: for whom, to do what, around what. The audience first — until you know who is learning, you can neither set a reachable objective nor judge whether a through-line will land. Objectives next: an objective states what the learner will be able to do, and if you cannot picture the exercise that would prove it, it is badly written. The through-line last, answering "what will this be used for" and acting as the arbiter when you must cut. Each one narrows the field of the next: that is what makes scoping useful.
```
