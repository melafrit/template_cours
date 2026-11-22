// essai_generateur.js : le contrôle du générateur de prompt, sans navigateur.
//
//     node generateur/essai_generateur.js
//
// Il part des valeurs neutres de valeurs.exemple.js, pour tourner sur tout poste, et vérifie ce que le prompt doit
// dire dans trois cas : un dossier déjà préparé avec deux filières et des illustrations, un dossier neuf avec une
// jumelle anglaise, et des valeurs absentes. Code 1 au premier écart. À relancer après toute retouche de
// generateur.js (CLAUDE.md, § 6).
'use strict';
const path = require('path');
const fs = require('fs');
const G = require(path.join(__dirname, 'generateur.js'));
const fenetre = {};
new Function('window', fs.readFileSync(path.join(__dirname, 'valeurs.exemple.js'), 'utf8'))(fenetre);
const V = fenetre.VALEURS_HABITUELLES;
const ecarts = [];
function exiger(condition, message) { if (!condition) ecarts.push(message); }

// 1. Un dossier préparé, deux filières, des illustrations.
const e1 = G.etatInitial(V, new Date(2026, 10, 22));
e1.cours.titre = 'Gestion de projet (MOE)';
e1.dossier.chemin = 'C:\\projets\\Cours\\Cours_Essai_MOE';
e1.filieres = G.filieresDeLaPaire(V, 'CDWFS et ASRC', 'fr');
e1.modules.complements.illustrations = true;
const p1 = G.construirePrompt(e1, V);
exiger(/prompts\/PROMPT-Cours-parametrable\.md/.test(p1), 'le tronc n\'est pas cité');
exiger(/prompts\/modules\/10-codex\.md/.test(p1), 'le module Codex manque, illustrations cochées');
exiger(/codex --version/.test(p1), 'la vérification de Codex manque');
exiger(!/01-langues\.md/.test(p1), 'le module des langues est cité pour un cours en une langue');
exiger(/aucune recherche dans ce dossier tant que son \.rgignore n'exclut pas Doc_Reference\//.test(p1),
       'la garde avant recherche manque');
exiger(/ajoute Doc_Reference\/ au \.gitignore et au\s+\.rgignore/.test(p1), 'l\'exclusion des documents manque');
exiger(/\(\.json\) trouvé parmi les documents est un secret/.test(p1), 'la règle des .json manque');
exiger(/--essai --ecraser/.test(p1), 'l\'essai avant --ecraser manque');
exiger(/slug: "gestion-de-projet-moe"/.test(p1), 'l\'identifiant n\'est pas déduit du titre');
exiger(/depot: "compte\/Cours_Essai_MOE"/.test(p1), 'le dépôt n\'est pas déduit du dossier');
exiger(/groupe_mixte: true/.test(p1), 'deux filières sans groupe mixte');
exiger(/rncp: "39608"/.test(p1) && /rncp: "39611"/.test(p1), 'les filières habituelles ne sont pas reprises');
exiger(/co_auteur: false/.test(p1), 'la règle des commits au seul nom de l\'auteur manque');
exiger(!/\\/.test(p1), 'un antislash reste dans le prompt (les chemins s\'écrivent avec des barres obliques)');

// 2. Un dossier neuf, une jumelle anglaise, sans illustrations.
const e2 = G.etatInitial(V, new Date(2026, 10, 22));
e2.cours.titre = 'Cours d\'essai';
e2.cours.jumelles.en = true;
e2.dossier.existe = false;
const p2 = G.construirePrompt(e2, V);
exiger(/prompts\/modules\/01-langues\.md/.test(p2), 'le module des langues manque avec une jumelle');
exiger(/langues: \["fr", "en"\]/.test(p2), 'les langues ne listent pas la racine puis la jumelle');
exiger(/sources\//.test(p2), 'un dossier neuf ne renvoie pas à sources/');
exiger(!/10-codex/.test(p2), 'le module Codex est cité sans illustrations');

// 3. Sans valeurs : la page doit encore produire un prompt complet.
const p3 = G.construirePrompt(G.etatInitial(undefined, new Date(2026, 10, 22)), undefined);
exiger(/~~~yaml[\s\S]*~~~/.test(p3), 'sans valeurs, le bloc de paramètres manque');

[p1, p2, p3].forEach(function (p, i) {
  exiger(!/[\u2014]| \u2013 /.test(p), 'cas ' + (i + 1) + ' : un tiret cadratin ou demi-cadratin dans le prompt');
});

if (ecarts.length) {
  ecarts.forEach(function (e) { console.log('  ✗ ' + e); });
  console.log('Générateur : ' + ecarts.length + ' écart(s)');
  process.exit(1);
}
console.log('Générateur : 3 cas, aucun écart');
