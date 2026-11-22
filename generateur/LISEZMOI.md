# Le générateur de prompt de cours

Une page locale qui fabrique le **prompt de lancement** d'un nouveau cours, à coller dans Claude Code. Le prompt
renvoie au tronc (`prompts/PROMPT-Cours-parametrable.md`) et aux modules actifs (`prompts/modules/`) par leur
chemin, ce qui le garde à jour quand ils changent, et donne le bloc de paramètres du tronc, rempli. Décisions de
l'auteur du 21 et du 22 novembre 2026 (lot 8 du grand chantier).

## L'ouvrir

Double-cliquez sur `generateur/index.html`. La page tourne dans le navigateur, sans serveur ni réseau ; rien ne
quitte le poste. Elle ne se publie jamais (hors de `site/`) et ne part pas dans les cours créés.

## Vos valeurs habituelles

La page lit `generateur/valeurs.local.js` : votre nom et l'adresse des commits, votre compte GitHub, l'adresse et
le répertoire de base des cours en ligne, l'écosystème (le gabarit, les cours de référence, Livrables), vos paires
de filières et vos habitudes (palette, langues, horaires, ton, modules). Ce fichier est **ignoré par Git** ;
**aucun secret** n'y entre (ni clé, ni mot de passe, ni accès à l'hébergement).

- Absent, la page part de valeurs neutres et le dit : copiez `valeurs.exemple.js` en `valeurs.local.js`.
- Pour les changer, remplissez « Vos valeurs habituelles », puis « Enregistrer mes valeurs habituelles ». Le
  navigateur ne peut pas écrire dans ce dossier : le fichier se télécharge, et vous le placez dans `generateur/`, à
  la place de l'ancien.

Le cours en cours de saisie se garde dans ce navigateur, comme un brouillon ; « Recommencer » le vide.

## Un dossier de cours déjà préparé

Cochez « Le dossier existe déjà, avec ses documents » et donnez le nom du dossier des documents (`Doc_Reference` par
défaut). Le prompt demande alors de :

- n'ouvrir les documents qu'un par un, par leur chemin, sans aucune recherche dans le dossier tant que son
  `.rgignore` ne les exclut pas ;
- ne jamais ouvrir les secrets que vous nommez (« Fichiers secrets connus parmi les documents »), ni un fichier de
  configuration ou de mot de passe trouvé parmi eux (`.json`, `.env`, « mot de passe »…), et le signaler ;
- ne déplacer, renommer ni modifier aucun document ;
- créer le cours dans ce dossier avec `nouveau_cours.py --ecraser`, après un essai : les documents et
  `deploiement/config.json` restent en place ;
- exclure aussitôt le dossier des documents de Git et des recherches, avant `git init`.

## Vos consignes

Un champ court garde une valeur (un nom, un chemin) : il va dans le bloc de paramètres. Une phrase va dans l'une
des consignes (le fil rouge, le TP, les autres) : le prompt la reprend telle quelle sous « Ce que l'auteur a
précisé », retours à la ligne compris. Une consigne laissée dans un champ court finirait dans le YAML, où Claude la
prendrait pour une donnée ; la page la signale. Ces règles viennent du premier usage réel du générateur, le cours de
gestion de projet (MOE), le 22 novembre 2026.

## Les chemins

Collez-les tels quels, même entre guillemets, comme les donne « Copier en tant que chemin » dans l'Explorateur. Le
prompt les écrit avec des barres obliques, sans guillemets, et relatifs au dossier du cours quand ils s'y trouvent
(`Doc_Reference/…`). Tant que le champ du dossier ne contient que le dossier de base des cours, le prompt dit le
dossier « à préciser ».

## Les points à vérifier

Au-dessus du prompt, un encadré signale ce qui demande votre regard : une promotion qui n'a pas la forme
« Année › Promotion » de l'application Livrables, un bloc ou un module qui diffère entre le cours et ses filières,
« Bloc 04 » (le prompt écrit « Bloc 4 »), une date mal écrite, un Jour 1 à moins de deux semaines, un TP qui porte
sur le fil rouge, une consigne restée dans un champ court. Ceux qui demandent une décision passent aussi dans le
prompt, et Claude vous les pose au cadrage. Une promotion mal écrite ne part pas dans le YAML.

## Ce que la page ne fait pas

Elle ne crée pas le cours et n'écrit pas `cours.json` : c'est Claude qui le fait, à l'étape zéro du tronc, après le
cadrage. Elle ne remplit pas les livrables : ils se construisent au cadrage, d'après les documents ; un champ libre
permet d'en noter ce qui est déjà connu.

## Les fichiers

| Fichier | Rôle |
|---|---|
| `index.html` | la page et son formulaire |
| `generateur.js` | la fabrication du prompt, une fonction pure que node peut tester |
| `page.js` | l'interface : les champs, le brouillon, les boutons |
| `valeurs.exemple.js` | le modèle des valeurs habituelles, versionné, aux valeurs neutres |
| `valeurs.local.js` | vos valeurs, locales et ignorées par Git |
| `essai_generateur.js` | le contrôle, sans navigateur : `node generateur/essai_generateur.js`, à relancer après toute retouche |
