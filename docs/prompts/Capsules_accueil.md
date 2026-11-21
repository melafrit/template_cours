# Capsules de l'accueil · cours de démonstration

**Neuf capsules en français** sur la page d'accueil (`site/index.html`) : la capsule de bienvenue, toujours
affichée (conteneur `voix-bienvenue`) ; celle de chaque filière, qui n'apparaît qu'une fois la filière choisie
(`voix-bienvenue-eadl`, `voix-bienvenue-eris`) ; puis une capsule en tête de chaque section (`voix-section-1` à
`voix-section-6`). Les mêmes en anglais : `Capsules_accueil_en.md`.

Cette fiche est la **source unique** : `outils/generer_audio.py` y lit les scripts, et la transcription se reporte
dans le script des capsules de `index.html` par `outils/synchroniser_capsules.py`, qui y pose aussi les espaces
insécables du français. Ne modifiez jamais une transcription dans le HTML.

## ⚠️ À lire avant de générer

- **Témoin : la capsule 1.** Son texte est écrit seul, lu et validé par l'auteur avant les huit autres. Sa piste
  est générée seule, écoutée sur le lecteur de la page, avant la série (lot 9).
- **Modèle : Eleven v4**, la voix de l'auteur. Le générateur ajoute « strong Parisian French accent » à chaque
  balise. Lecture posée : « speaking slowly » dans chaque balise, comme les capsules d'accueil du cours d'étude
  d'avant-projet.
- **Sources.** L'accueil (son accroche, ses cartes), le sous-titre du cours (`course-data.js`), les sous-titres
  des trois chapitres, l'atelier (son introduction, ses livrables), la consigne du QCM et le bandeau des filières
  (`ui-labels.js`). Rien d'autre.
- **Écriture pour la voix.** Nombres en lettres dans le script ; « Q.C.M. », « E.A.D.L. », « Éris ». La
  transcription garde l'orthographe d'affichage (« QCM », « EADL », « ERIS », « chapitre 1 »).
- **Génération**, une fois le texte validé : `python outils/generer_audio.py --fichier accueil-capsule-fr.mp3 --temoin`.

## 📋 Récapitulatif · les neuf fichiers

Tous dans `site/assets/media/voix/`. Les noms sont fixés : la page les appelle déjà.

| # | Conteneur | Nom exact du fichier | Affichée | État |
|---|---|---|---|---|
| 1 | `voix-bienvenue` | `accueil-capsule-fr.mp3` | toujours | témoin, texte validé |
| 2 | `voix-bienvenue-eadl` | `accueil-capsule-eadl-fr.mp3` | filière EADL choisie | texte validé |
| 3 | `voix-bienvenue-eris` | `accueil-capsule-eris-fr.mp3` | filière ERIS choisie | texte validé |
| 4 | `voix-section-1` | `accueil-section-1-capsule-fr.mp3` | « Le parcours » | texte validé |
| 5 | `voix-section-2` | `accueil-section-2-capsule-fr.mp3` | « Le fil rouge » | texte validé |
| 6 | `voix-section-3` | `accueil-section-3-capsule-fr.mp3` | « Ce que vous produisez » | texte validé |
| 7 | `voix-section-4` | `accueil-section-4-capsule-fr.mp3` | « L'évaluation » | texte validé |
| 8 | `voix-section-5` | `accueil-section-5-capsule-fr.mp3` | « Ce que démontre ce site » | texte validé |
| 9 | `voix-section-6` | `accueil-section-6-capsule-fr.mp3` | « Avant de commencer » | texte validé |

---

## Capsule 1 · Bienvenue dans le cours-démo (témoin)

- **Nom exact du fichier :** `accueil-capsule-fr.mp3`
- **Emplacement exact :** `site/assets/media/voix/accueil-capsule-fr.mp3` (accueil, conteneur `voix-bienvenue`)
- **Durée visée :** ≈ 1 min 25 (228 mots parlés, tolérance 1 min 05 → 2 min 00)

- [x] Texte lu et validé par l'auteur (21 novembre 2026)
- [ ] Témoin écouté et validé par l'auteur
- [ ] Capsule générée, contrôlée et déposée

**▶️ Script ElevenLabs**

```
[warm, encouraging, speaking slowly] Bonjour, et bienvenue dans ce cours-démo. Il vous apprend à concevoir un cours en ligne… et il le fait avec les outils mêmes qu'il vous présente.

[thoughtful, speaking slowly] Vous lisez donc un cours qui explique comment en construire un, pendant que vous construisez le vôtre. C'est son fil rouge : dans l'atelier, chaque chapitre nourrit directement un livrable de votre projet.

[measured, speaking slowly] Le parcours compte trois chapitres, dans l'ordre où un cours se conçoit. Au premier, vous cadrez votre cours : pour qui, pour quoi faire, et autour de quoi. Au deuxième, vous le structurez, dans quel ordre et par quels morceaux. Au troisième, vous créez ses ressources, en choisissant pour chaque intention le bon format : un texte, un audio ou un schéma.

[engaged, speaking slowly] À la fin de l'atelier, vous remettez cinq livrables : une fiche de cadrage, un plan, un chapitre entièrement rédigé, un Q.C.M. et un glossaire. Pris ensemble, ils forment le squelette complet d'un cours prêt à diffuser. Le Q.C.M. noté, lui, vous demande pour chaque question une réponse… et votre degré de certitude.

[serious, measured, speaking slowly] Ce cours est commun à deux filières, E.A.D.L. et Éris. Certains exemples changent selon la vôtre : tant que vous n'avez pas choisi, les deux versions s'affichent.

[warm, encouraging, speaking slowly] Choisissez maintenant votre filière, en haut de la page : une présentation propre à votre parcours vous attend juste en dessous. Ouvrez ensuite le chapitre un, avec l'atelier à côté. Allez, on commence !
```

**📄 Transcription affichée sur la page**

```
Bonjour, et bienvenue dans ce cours-démo. Il vous apprend à concevoir un cours en ligne, et il le fait avec les outils mêmes qu'il vous présente. Vous lisez donc un cours qui explique comment en construire un, pendant que vous construisez le vôtre. C'est son fil rouge : dans l'atelier, chaque chapitre nourrit directement un livrable de votre projet. Le parcours compte trois chapitres, dans l'ordre où un cours se conçoit. Au premier, vous cadrez votre cours : pour qui, pour quoi faire, et autour de quoi. Au deuxième, vous le structurez, dans quel ordre et par quels morceaux. Au troisième, vous créez ses ressources, en choisissant pour chaque intention le bon format : un texte, un audio ou un schéma. À la fin de l'atelier, vous remettez cinq livrables : une fiche de cadrage, un plan, un chapitre entièrement rédigé, un QCM et un glossaire. Pris ensemble, ils forment le squelette complet d'un cours prêt à diffuser. Le QCM noté, lui, vous demande pour chaque question une réponse et votre degré de certitude. Ce cours est commun à deux filières, EADL et ERIS. Certains exemples changent selon la vôtre : tant que vous n'avez pas choisi, les deux versions s'affichent. Choisissez maintenant votre filière, en haut de la page : une présentation propre à votre parcours vous attend juste en dessous. Ouvrez ensuite le chapitre 1, avec l'atelier à côté. Allez, on commence !
```

---

## Capsule 2 · En EADL : votre fil rouge

- **Nom exact du fichier :** `accueil-capsule-eadl-fr.mp3`
- **Emplacement exact :** `site/assets/media/voix/accueil-capsule-eadl-fr.mp3` (accueil, conteneur `voix-bienvenue-eadl`)
- **Durée visée :** ≈ 40 s (108 mots parlés, tolérance 0 min 30 → 1 min 05)

- [x] Texte lu et validé par l'auteur (21 novembre 2026)
- [ ] Capsule générée, contrôlée et déposée

**▶️ Script ElevenLabs**

```
[warm, encouraging, speaking slowly] Vous avez choisi E.A.D.L., la filière Expert en architecture et développement logiciel.

[thoughtful, speaking slowly] Dans ce cours, votre filière change deux choses : la couleur de la page, et certains exemples. Prenez le fil rouge… en E.A.D.L., il peut être une application que les apprenants conçoivent de chapitre en chapitre. Chaque notion d'architecture s'y applique alors à une décision réelle.

[measured, speaking slowly] Les exemples propres à Éris se sont effacés… vous ne lisez plus que ceux de votre filière. Le reste du cours est commun aux deux.

[warm, encouraging, speaking slowly] Vous pouvez changer de filière à tout moment, en haut de la page. Et si vous recliquez sur la vôtre, les deux versions s'affichent de nouveau.
```

**📄 Transcription affichée sur la page**

```
Vous avez choisi EADL, la filière Expert en architecture et développement logiciel. Dans ce cours, votre filière change deux choses : la couleur de la page, et certains exemples. Prenez le fil rouge. En EADL, il peut être une application que les apprenants conçoivent de chapitre en chapitre. Chaque notion d'architecture s'y applique alors à une décision réelle. Les exemples propres à ERIS se sont effacés, et vous ne lisez plus que ceux de votre filière. Le reste du cours est commun aux deux. Vous pouvez changer de filière à tout moment, en haut de la page. Et si vous recliquez sur la vôtre, les deux versions s'affichent de nouveau.
```

---

## Capsule 3 · En ERIS : votre fil rouge

- **Nom exact du fichier :** `accueil-capsule-eris-fr.mp3`
- **Emplacement exact :** `site/assets/media/voix/accueil-capsule-eris-fr.mp3` (accueil, conteneur `voix-bienvenue-eris`)
- **Durée visée :** ≈ 42 s (112 mots parlés, tolérance 0 min 30 → 1 min 05)

- [x] Texte lu et validé par l'auteur (21 novembre 2026)
- [ ] Capsule générée, contrôlée et déposée

**▶️ Script ElevenLabs**

```
[warm, encouraging, speaking slowly] Vous avez choisi Éris, la filière Expert en réseaux, infrastructures et sécurité.

[thoughtful, speaking slowly] Dans ce cours, votre filière change deux choses : la couleur de la page, et certains exemples. Prenez le fil rouge… en Éris, il peut être l'infrastructure d'une entreprise fictive, que les apprenants sécurisent de chapitre en chapitre. Chaque notion s'y applique alors à un équipement ou à une règle.

[measured, speaking slowly] Les exemples propres à E.A.D.L. se sont effacés… vous ne lisez plus que ceux de votre filière. Le reste du cours est commun aux deux.

[warm, encouraging, speaking slowly] Vous pouvez changer de filière à tout moment, en haut de la page. Et si vous recliquez sur la vôtre, les deux versions s'affichent de nouveau.
```

**📄 Transcription affichée sur la page**

```
Vous avez choisi ERIS, la filière Expert en réseaux, infrastructures et sécurité. Dans ce cours, votre filière change deux choses : la couleur de la page, et certains exemples. Prenez le fil rouge. En ERIS, il peut être l'infrastructure d'une entreprise fictive, que les apprenants sécurisent de chapitre en chapitre. Chaque notion s'y applique alors à un équipement ou à une règle. Les exemples propres à EADL se sont effacés, et vous ne lisez plus que ceux de votre filière. Le reste du cours est commun aux deux. Vous pouvez changer de filière à tout moment, en haut de la page. Et si vous recliquez sur la vôtre, les deux versions s'affichent de nouveau.
```

---

## Capsule 4 · Le parcours

- **Nom exact du fichier :** `accueil-section-1-capsule-fr.mp3`
- **Emplacement exact :** `site/assets/media/voix/accueil-section-1-capsule-fr.mp3` (accueil, conteneur `voix-section-1`)
- **Durée visée :** ≈ 55 s (146 mots parlés, tolérance 0 min 40 → 1 min 25)

- [x] Texte lu et validé par l'auteur (21 novembre 2026)
- [ ] Capsule générée, contrôlée et déposée

**▶️ Script ElevenLabs**

```
[thoughtful, speaking slowly] Un cours mal cadré se répare mal : on s'en aperçoit à la troisième séance, quand il est trop tard pour tout reprendre. C'est pourquoi le parcours commence par là.

[measured, speaking slowly] Le chapitre un pose les trois décisions à prendre avant d'écrire la première ligne. Il sert aussi de vitrine… chaque composant du moteur y est exercé au moins une fois.

[measured, speaking slowly] Le chapitre deux part de ce cadrage. Il reste à décider dans quel ordre, et par quels morceaux. C'est là que se joue la différence entre un cours qu'on finit et un cours qu'on abandonne au troisième chapitre.

[measured, speaking slowly] Le chapitre trois choisit les formats. Texte, audio, schéma : chacun a son intention, et les confondre coûte cher, en temps de production comme en attention perdue.

[warm, encouraging, speaking slowly] Chaque carte, ci-dessous, ouvre son chapitre et donne son temps de lecture. Suivez-les dans l'ordre… c'est celui dans lequel un cours se conçoit.
```

**📄 Transcription affichée sur la page**

```
Un cours mal cadré se répare mal : on s'en aperçoit à la troisième séance, quand il est trop tard pour tout reprendre. C'est pourquoi le parcours commence par là. Le chapitre 1 pose les trois décisions à prendre avant d'écrire la première ligne. Il sert aussi de vitrine, car chaque composant du moteur y est exercé au moins une fois. Le chapitre 2 part de ce cadrage. Il reste à décider dans quel ordre, et par quels morceaux. C'est là que se joue la différence entre un cours qu'on finit et un cours qu'on abandonne au troisième chapitre. Le chapitre 3 choisit les formats. Texte, audio, schéma : chacun a son intention, et les confondre coûte cher, en temps de production comme en attention perdue. Chaque carte, ci-dessous, ouvre son chapitre et donne son temps de lecture. Suivez-les dans l'ordre, celui dans lequel un cours se conçoit.
```

---

## Capsule 5 · Le fil rouge

- **Nom exact du fichier :** `accueil-section-2-capsule-fr.mp3`
- **Emplacement exact :** `site/assets/media/voix/accueil-section-2-capsule-fr.mp3` (accueil, conteneur `voix-section-2`)
- **Durée visée :** ≈ 51 s (137 mots parlés, tolérance 0 min 40 → 1 min 25)

- [x] Texte lu et validé par l'auteur (21 novembre 2026)
- [ ] Capsule générée, contrôlée et déposée

**▶️ Script ElevenLabs**

```
[curious, speaking slowly] À chaque chapitre, un apprenant se pose la même question : à quoi cela va-t-il me servir ? Le fil rouge y répond par avance.

[thoughtful, speaking slowly] Un fil rouge est un cas, un projet ou un scénario qui traverse tout le cours. Celui de ce cours-démo, c'est le vôtre… vous construisez un cours en lisant un cours qui explique comment en construire un.

[measured, speaking slowly] L'idée tient en une phrase. Choisissez un sujet que vous maîtrisez, et transformez-le, pas à pas, en un mini-cours en ligne cohérent. L'atelier vous accompagne : chaque chapitre y nourrit directement un livrable de votre projet.

[engaged, speaking slowly] Selon votre filière, un exemple vous montre à quoi ressemblerait un fil rouge dans votre métier : une application à concevoir en E.A.D.L., l'infrastructure d'une entreprise à sécuriser en Éris.

[warm, encouraging, speaking slowly] Ouvrez l'atelier dès maintenant… et gardez-le à côté de vous, chapitre après chapitre.
```

**📄 Transcription affichée sur la page**

```
À chaque chapitre, un apprenant se pose la même question : à quoi cela va-t-il me servir ? Le fil rouge y répond par avance. Un fil rouge est un cas, un projet ou un scénario qui traverse tout le cours. Celui de ce cours-démo, c'est le vôtre, puisque vous construisez un cours en lisant un cours qui explique comment en construire un. L'idée tient en une phrase. Choisissez un sujet que vous maîtrisez, et transformez-le, pas à pas, en un mini-cours en ligne cohérent. L'atelier vous accompagne : chaque chapitre y nourrit directement un livrable de votre projet. Selon votre filière, un exemple vous montre à quoi ressemblerait un fil rouge dans votre métier : une application à concevoir en EADL, l'infrastructure d'une entreprise à sécuriser en ERIS. Ouvrez l'atelier dès maintenant, et gardez-le à côté de vous, chapitre après chapitre.
```

---

## Capsule 6 · Ce que vous produisez

- **Nom exact du fichier :** `accueil-section-3-capsule-fr.mp3`
- **Emplacement exact :** `site/assets/media/voix/accueil-section-3-capsule-fr.mp3` (accueil, conteneur `voix-section-3`)
- **Durée visée :** ≈ 57 s (151 mots parlés, tolérance 0 min 40 → 1 min 25)

- [x] Texte lu et validé par l'auteur (21 novembre 2026)
- [ ] Capsule générée, contrôlée et déposée

**▶️ Script ElevenLabs**

```
[confident, warm, speaking slowly] À la fin de l'atelier, vous aurez fabriqué un vrai cours, prêt à être diffusé. Il tient en cinq livrables.

[measured, speaking slowly] D'abord, une fiche de cadrage : le public cible, les prérequis, trois à cinq objectifs mesurables, et le fil rouge. Puis un plan, qui découpe le cours en modules et en séquences, avec la durée estimée de chacune.

[measured, speaking slowly] Ensuite, un chapitre entièrement rédigé : une séquence complète, illustrée, avec une accroche et un « à retenir ». Enfin, un Q.C.M. de cinq questions, chacune avec sa bonne réponse et sa justification, et un glossaire de dix termes, chacun avec sa définition et, si possible, un exemple.

[thoughtful, speaking slowly] Le format est libre… un document, un PDF, ou quelques pages sur le modèle de ce site. Ce qui compte, c'est la cohérence entre les cinq.

[warm, encouraging, speaking slowly] L'atelier détaille chaque livrable et ses critères de réussite… commencez par la fiche de cadrage, en même temps que le chapitre un.
```

**📄 Transcription affichée sur la page**

```
À la fin de l'atelier, vous aurez fabriqué un vrai cours, prêt à être diffusé. Il tient en cinq livrables. D'abord, une fiche de cadrage : le public cible, les prérequis, 3 à 5 objectifs mesurables, et le fil rouge. Puis un plan, qui découpe le cours en modules et en séquences, avec la durée estimée de chacune. Ensuite, un chapitre entièrement rédigé : une séquence complète, illustrée, avec une accroche et un « à retenir ». Enfin, un QCM de 5 questions, chacune avec sa bonne réponse et sa justification, et un glossaire de 10 termes, chacun avec sa définition et, si possible, un exemple. Le format est libre, que ce soit un document, un PDF, ou quelques pages sur le modèle de ce site. Ce qui compte, c'est la cohérence entre les cinq. L'atelier détaille chaque livrable et ses critères de réussite. Commencez par la fiche de cadrage, en même temps que le chapitre 1.
```

---

## Capsule 7 · L'évaluation

- **Nom exact du fichier :** `accueil-section-4-capsule-fr.mp3`
- **Emplacement exact :** `site/assets/media/voix/accueil-section-4-capsule-fr.mp3` (accueil, conteneur `voix-section-4`)
- **Durée visée :** ≈ 49 s (131 mots parlés, tolérance 0 min 40 → 1 min 25)

- [x] Texte lu et validé par l'auteur (21 novembre 2026)
- [ ] Capsule générée, contrôlée et déposée

**▶️ Script ElevenLabs**

```
[curious, speaking slowly] Dans ce cours, le Q.C.M. noté vous demande deux choses pour chaque question : une réponse, et votre degré de certitude.

[measured, speaking slowly] Le barème suit cette certitude. Une bonne réponse rapporte trois points si vous en étiez certain, deux si vous en étiez assez sûr, un si vous deviniez. Une erreur, elle, coûte trois points avec une certitude élevée, deux avec une certitude moyenne… et rien si vous aviez dit que vous deviniez.

[thoughtful, speaking slowly] Le calcul récompense donc la lucidité : mieux vaut annoncer un doute que parier à l'aveugle. La correction, elle, est expliquée question par question.

[engaged, speaking slowly] Avant le Q.C.M., deux outils vous entraînent. Dans les chapitres, des points de contrôle vérifient votre lecture et expliquent chaque réponse. À la fin de chaque chapitre, des flashcards reprennent l'essentiel.

[warm, encouraging, speaking slowly] Utilisez-les… avant de passer le Q.C.M.
```

**📄 Transcription affichée sur la page**

```
Dans ce cours, le QCM noté vous demande deux choses pour chaque question : une réponse, et votre degré de certitude. Le barème suit cette certitude. Une bonne réponse rapporte 3 points si vous en étiez certain, 2 si vous en étiez assez sûr, 1 si vous deviniez. Une erreur, elle, coûte 3 points avec une certitude élevée, 2 avec une certitude moyenne, et rien si vous aviez dit que vous deviniez. Le calcul récompense donc la lucidité : mieux vaut annoncer un doute que parier à l'aveugle. La correction, elle, est expliquée question par question. Avant le QCM, deux outils vous entraînent. Dans les chapitres, des points de contrôle vérifient votre lecture et expliquent chaque réponse. À la fin de chaque chapitre, des flashcards reprennent l'essentiel. Utilisez-les avant de passer le QCM.
```

---

## Capsule 8 · Ce que démontre ce site

- **Nom exact du fichier :** `accueil-section-5-capsule-fr.mp3`
- **Emplacement exact :** `site/assets/media/voix/accueil-section-5-capsule-fr.mp3` (accueil, conteneur `voix-section-5`)
- **Durée visée :** ≈ 55 s (146 mots parlés, tolérance 0 min 40 → 1 min 25)

- [x] Texte lu et validé par l'auteur (21 novembre 2026)
- [ ] Capsule générée, contrôlée et déposée

**▶️ Script ElevenLabs**

```
[confident, warm, speaking slowly] Ce site joue deux rôles. Il vous enseigne à concevoir un cours… et il montre, page après page, ce que le gabarit sait faire.

[measured, speaking slowly] Il parle trois langues : le français et l'anglais sur tout le site, l'arabe sur le chapitre un, de droite à gauche. Quand vous changez de langue, vous retrouvez le passage que vous lisiez.

[measured, speaking slowly] Il sert deux filières, et il donne à chaque chapitre ses médias : une capsule audio et sa transcription, des schémas interactifs, un lecteur de podcasts.

[thoughtful, speaking slowly] Le Q.C.M. est noté par degré de certitude, avec sa correction et son tableau de bord. Le glossaire surligne ses termes dans le texte : survolez-en un, une info-bulle donne sa définition et un exemple. Des flashcards et des activités interactives complètent l'ensemble.

[warm, encouraging, speaking slowly] Enfin, le panneau d'accessibilité règle la taille du texte, la police et le mouvement… pour que chacun lise dans de bonnes conditions.
```

**📄 Transcription affichée sur la page**

```
Ce site joue deux rôles. Il vous enseigne à concevoir un cours, et il montre, page après page, ce que le gabarit sait faire. Il parle trois langues : le français et l'anglais sur tout le site, l'arabe sur le chapitre 1, de droite à gauche. Quand vous changez de langue, vous retrouvez le passage que vous lisiez. Il sert deux filières, et il donne à chaque chapitre ses médias : une capsule audio et sa transcription, des schémas interactifs, un lecteur de podcasts. Le QCM est noté par degré de certitude, avec sa correction et son tableau de bord. Le glossaire surligne ses termes dans le texte : survolez-en un, une info-bulle donne sa définition et un exemple. Des flashcards et des activités interactives complètent l'ensemble. Enfin, le panneau d'accessibilité règle la taille du texte, la police et le mouvement, pour que chacun lise dans de bonnes conditions.
```

---

## Capsule 9 · Avant de commencer

- **Nom exact du fichier :** `accueil-section-6-capsule-fr.mp3`
- **Emplacement exact :** `site/assets/media/voix/accueil-section-6-capsule-fr.mp3` (accueil, conteneur `voix-section-6`)
- **Durée visée :** ≈ 51 s (135 mots parlés, tolérance 0 min 40 → 1 min 25)

- [x] Texte lu et validé par l'auteur (21 novembre 2026)
- [ ] Capsule générée, contrôlée et déposée

**▶️ Script ElevenLabs**

```
[warm, encouraging, speaking slowly] Quatre conseils avant de vous lancer.

[measured, speaking slowly] Commencez par le chapitre un. Il pose les trois décisions à prendre avant d'écrire, et il sert de vitrine : chaque composant y est exercé.

[measured, speaking slowly] Ouvrez l'atelier en parallèle… chaque chapitre y nourrit directement un livrable de votre projet.

[measured, speaking slowly] Réglez l'affichage à votre convenance : le thème sombre, la taille du texte et la police se règlent en haut de page, dans le panneau d'accessibilité.

[thoughtful, speaking slowly] Et révisez avant le Q.C.M. : les flashcards de chaque chapitre reprennent l'essentiel.

[engaged, speaking slowly] Deux supports vous suivent hors de l'écran. Le polycopié réunit tout le cours en un seul livret, à lire hors ligne ; ses Q.R. codes vous ramènent au bon endroit du site. Les podcasts, eux, vous font découvrir un chapitre avant de le lire, ou le réviser loin de l'écran… dans le train, en marchant.
```

**📄 Transcription affichée sur la page**

```
Quatre conseils avant de vous lancer. Commencez par le chapitre 1. Il pose les trois décisions à prendre avant d'écrire, et il sert de vitrine : chaque composant y est exercé. Ouvrez l'atelier en parallèle, car chaque chapitre y nourrit directement un livrable de votre projet. Réglez l'affichage à votre convenance : le thème sombre, la taille du texte et la police se règlent en haut de page, dans le panneau d'accessibilité. Et révisez avant le QCM : les flashcards de chaque chapitre reprennent l'essentiel. Deux supports vous suivent hors de l'écran. Le polycopié réunit tout le cours en un seul livret, à lire hors ligne ; ses QR codes vous ramènent au bon endroit du site. Les podcasts, eux, vous font découvrir un chapitre avant de le lire, ou le réviser loin de l'écran, dans le train ou en marchant.
```
