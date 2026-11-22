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
- ne jamais ouvrir un fichier de configuration (`.json`) trouvé parmi eux, et le signaler ;
- ne déplacer, renommer ni modifier aucun document ;
- créer le cours dans ce dossier avec `nouveau_cours.py --ecraser`, après un essai : les documents et
  `deploiement/config.json` restent en place ;
- exclure aussitôt le dossier des documents de Git et des recherches, avant `git init`.

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
