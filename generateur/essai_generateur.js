// essai_generateur.js : le contrôle du générateur de prompt, sans navigateur.
//
//     node generateur/essai_generateur.js
//
// Il part des valeurs neutres de valeurs.exemple.js, pour tourner sur tout poste, et vérifie ce que le prompt doit
// dire dans cinq cas : un dossier déjà préparé avec deux filières et des illustrations ; un dossier neuf avec une
// jumelle anglaise ; des valeurs absentes ; la saisie du premier usage réel (le cours MOE, 22 novembre 2026), avec
// ses chemins Windows, ses consignes et ses incohérences ; un Jour 1 lointain. Code 1 au premier écart. À relancer
// après toute retouche de generateur.js (CLAUDE.md, § 6).
'use strict';
const path = require('path');
const fs = require('fs');
const G = require(path.join(__dirname, 'generateur.js'));
const fenetre = {};
new Function('window', fs.readFileSync(path.join(__dirname, 'valeurs.exemple.js'), 'utf8'))(fenetre);
const V = fenetre.VALEURS_HABITUELLES;
const AUJ = new Date(2026, 10, 22);
const ecarts = [];
function exiger(condition, message) { if (!condition) ecarts.push(message); }
function yamlDe(p) { const m = p.match(/~~~yaml\n([\s\S]*?)\n~~~/); return m ? m[1] : ''; }
function horsYaml(p) { return p.replace(/~~~yaml\n[\s\S]*?\n~~~/, ''); }

// 1. Un dossier préparé, deux filières, des illustrations.
const e1 = G.etatInitial(V, AUJ);
e1.cours.titre = 'Gestion de projet (MOE)';
e1.dossier.chemin = 'C:\\projets\\Cours\\Cours_Essai_MOE';
e1.filieres = G.filieresDeLaPaire(V, 'CDWFS et ASRC', 'fr');
e1.modules.complements.illustrations = true;
const p1 = G.construirePrompt(e1, V, AUJ);
exiger(/prompts\/PROMPT-Cours-parametrable\.md/.test(p1), 'le tronc n\'est pas cité');
exiger(/prompts\/modules\/10-codex\.md/.test(p1), 'le module Codex manque, illustrations cochées');
exiger(/codex --version/.test(p1), 'la vérification de Codex manque');
exiger(!/01-langues\.md/.test(p1), 'le module des langues est cité pour un cours en une langue');
exiger(/aucune recherche dans ce dossier tant que son \.rgignore n'exclut pas Doc_Reference\//.test(p1),
       'la garde avant recherche manque');
exiger(/ajoute Doc_Reference\/ au \.gitignore et au\s+\.rgignore/.test(p1), 'l\'exclusion des documents manque');
exiger(/Tout fichier de configuration ou de mot de passe trouvé parmi les documents \(\.json, \.env,\s+« mot de passe »/
       .test(p1), 'la règle des fichiers de configuration et de mot de passe manque');
exiger(!/Ces fichiers sont des secrets|Ce fichier est un secret/.test(p1), 'des secrets nommés sans qu\'aucun soit saisi');
exiger(/--essai --ecraser/.test(p1), 'l\'essai avant --ecraser manque');
exiger(/slug: "gestion-de-projet-moe"/.test(p1), 'l\'identifiant n\'est pas déduit du titre');
exiger(/depot: "compte\/Cours_Essai_MOE"/.test(p1), 'le dépôt n\'est pas déduit du dossier');
exiger(/groupe_mixte: true/.test(p1), 'deux filières sans groupe mixte');
exiger(/rncp: "39608"/.test(p1) && /rncp: "39611"/.test(p1), 'les filières habituelles ne sont pas reprises');
exiger(/co_auteur: false/.test(p1), 'la règle des commits au seul nom de l\'auteur manque');
exiger(!/Ce que l'auteur a précisé/.test(p1), 'une section de précisions sans rien à préciser');

// 2. Un dossier neuf, une jumelle anglaise, sans illustrations ; le dossier n'a pas encore son nom.
const e2 = G.etatInitial(V, AUJ);
e2.cours.titre = 'Cours d\'essai';
e2.cours.jumelles.en = true;
e2.dossier.existe = false;
const p2 = G.construirePrompt(e2, V, AUJ);
exiger(/prompts\/modules\/01-langues\.md/.test(p2), 'le module des langues manque avec une jumelle');
exiger(/langues: \["fr", "en"\]/.test(p2), 'les langues ne listent pas la racine puis la jumelle');
exiger(/sources\//.test(p2), 'un dossier neuf ne renvoie pas à sources/');
exiger(/parmi sources\/ \(\.json/.test(p2), 'la règle des secrets manque pour sources/');
exiger(!/10-codex/.test(p2), 'le module Codex est cité sans illustrations');
exiger(/Le dossier du cours : \(à préciser\)\./.test(p2), 'le dossier de base est pris pour le dossier du cours');
exiger(/depot: ""/.test(p2), 'un dépôt est déduit du dossier de base');

// 3. Sans valeurs : la page doit encore produire un prompt complet.
const p3 = G.construirePrompt(G.etatInitial(undefined, AUJ), undefined, AUJ);
exiger(/~~~yaml[\s\S]*~~~/.test(p3), 'sans valeurs, le bloc de paramètres manque');

// 4. Le premier usage réel : chemins Windows (entre guillemets ou non), consignes en prose, deux secrets, une
//    promotion sans « Année › Promotion », un module différent, « Bloc 04 », un Jour 1 le lendemain, un TP sur le
//    fil rouge, et une consigne restée dans un champ court.
const D = 'C:\\projets\\Cours\\Cours_Essai_MOE';
const e4 = G.etatInitial(V, AUJ);
Object.assign(e4.cours, { titre: 'Gestion de projet (MOE)', code_module: 'M02', bloc: 'Bloc 4',
                          dates: '2026-11-23, 2026-12-14' });
e4.dossier.chemin = '"' + D + '\\"';
e4.dossier.secrets = D + '\\Doc_Reference\\elevenlabs.json\n"' + D + '\\Doc_Reference\\Templates\\Mot de passe.txt"';
e4.filieres = G.filieresDeLaPaire(V, 'CDWFS et ASRC', 'fr');
Object.assign(e4.filieres[0], { bloc: 'Bloc 04', module: 'FM02', promotion_app: '2027',
  fiche_module: D + '\\Doc_Reference\\CDWFS\\Fiche FM02.docx',
  grille: '"' + D + '\\Doc_Reference\\CDWFS\\Grille EC08.docx" ; "' + D + '\\Doc_Reference\\CDWFS\\Grille EC09.docx"',
  fil_rouge: 'Novaria Signal' });
Object.assign(e4.filieres[1], { bloc: 'Bloc 04', module: 'FM02', promotion_app: '2026-2027 \u203a ASRC B3',
  page_epreuves: 'https://example.org/epreuves/' });
e4.fil_rouge.source = 'analyser tous les documents et sous-dossiers de "' + D + '\\Doc_Reference\\Fil rouge\\Fil Rouge CDWFS" ' +
  'puis, pour ASRC, la transcription de la réunion de "' + D + '\\Doc_Reference\\Fil rouge\\Fil rouge ASRC"';
e4.consignes.fil_rouge = 'Pour CDWFS, analyse ' + D + '\\Doc_Reference\\Fil rouge\\Fil Rouge CDWFS\\.\nPour ASRC, adapte ce projet.';
e4.consignes.tp = 'Il suit la démarche de ' + D + '\\Doc_Reference\\Fil rouge\\Modele de TP\\, adaptée au fil rouge de chaque filière.';
e4.modules.tp.actif = true;
const p4 = G.construirePrompt(e4, V, AUJ);
const y4 = yamlDe(p4);
const v4 = G.verifications(e4, V, AUJ).map(x => x.page).filter(Boolean).join('\n');
exiger(/Le dossier du cours : C:\/projets\/Cours\/Cours_Essai_MOE\./.test(p4), 'le dossier n\'est pas nettoyé (guillemets, barres)');
exiger(/fiche_module: "Doc_Reference\/CDWFS\/Fiche FM02\.docx"/.test(y4), 'la fiche module n\'est pas relative au dossier');
exiger(/grille: "Doc_Reference\/CDWFS\/Grille EC08\.docx ; Doc_Reference\/CDWFS\/Grille EC09\.docx"/.test(y4),
       'les grilles entre guillemets ne sont pas nettoyées');
exiger(/Ces fichiers sont des secrets, à ne jamais ouvrir, afficher ni citer : Doc_Reference\/elevenlabs\.json et Doc_Reference\/Templates\/Mot de passe\.txt\./
       .test(p4), 'les deux secrets ne sont pas nommés');
exiger(/promotion_app: ""/.test(y4) && /promotion_app: "2026-2027 \u203a ASRC B3"/.test(y4),
       'une promotion sans « Année › Promotion » reste dans le YAML, ou une promotion juste en sort');
exiger(/L'auteur a indiqué « 2027 » \(CDWFS\), alors que/.test(p4), 'la promotion à préciser n\'est pas demandée');
exiger(/Le module du cours \(« M02 »\) et celui des filières CDWFS et ASRC \(« FM02 »\) diffèrent/.test(p4),
       'l\'écart de module n\'est pas signalé, ou pas groupé');
exiger(!/Le bloc du cours/.test(p4), '« Bloc 4 » et « Bloc 04 » sont pris pour deux blocs');
exiger(!/Bloc 04/.test(p4) && (y4.match(/bloc: "Bloc 4"/g) || []).length === 3, '« Bloc 04 » n\'est pas écrit « Bloc 4 »');
exiger(/Le Jour 1 a lieu le lundi 23 novembre 2026, le Jour 2 le lundi 14 décembre 2026\./.test(p4),
       'le calendrier d\'un Jour 1 proche manque');
exiger(/Un point à trancher au cadrage\. Le TP s'applique au fil rouge/.test(p4), 'le TP sur le fil rouge n\'est pas signalé');
exiger(/La page des épreuves s'ouvre et se vérifie/.test(p4), 'la vérification de la page des épreuves manque');
const ordre = ['Le calendrier.', 'Le fil rouge.', 'Le TP.', 'Un point à trancher', 'Les promotions'].map(x => p4.indexOf(x));
exiger(ordre.every((x, i) => x > 0 && (i === 0 || x > ordre[i - 1])), 'les précisions ne suivent pas leur ordre : ' + ordre);
exiger(/   - Le fil rouge\. Pour CDWFS, analyse Doc_Reference\/Fil rouge\/Fil Rouge CDWFS\/\.\n     Pour ASRC, adapte ce projet\./
       .test(p4), 'la consigne ne garde pas son retour à la ligne, ou son chemin n\'est pas relatif');
exiger(!/Pour ASRC, adapte ce projet/.test(y4), 'une consigne est passée dans le YAML');
exiger(/projet_par_filiere:\n    cdwfs: "Novaria Signal"/.test(y4), 'le projet par filière manque');
exiger(/« Sa source » ressemble à une consigne/.test(v4), 'la consigne restée dans un champ court n\'est pas signalée');
exiger(/Promotion à préciser/.test(v4) && /Le Jour 1 a lieu demain/.test(v4) && /« Bloc 0N »/.test(v4),
       'la page ne signale pas la promotion, le Jour 1 ou « Bloc 0N »');
exiger(!/\\/.test(horsYaml(p4)) && !/[A-Z]:\/projets\/Cours\/Cours_Essai_MOE\//i.test(p4),
       'un chemin reste absolu ou garde un antislash');

// 5. Un Jour 1 lointain, une date mal écrite : pas d'urgence dans le prompt, un signalement dans la page.
const e5 = G.etatInitial(V, AUJ);
e5.cours.dates = '2027-03-01';
exiger(!/Le calendrier\./.test(G.construirePrompt(e5, V, AUJ)), 'un Jour 1 lointain est annoncé comme urgent');
e5.cours.dates = '01/03/2027';
exiger(G.verifications(e5, V, AUJ).some(x => /AAAA-MM-JJ/.test(x.page || '')), 'une date mal écrite n\'est pas signalée');

[p1, p2, p3, p4].forEach(function (p, i) {
  exiger(!/[\u2014]| \u2013 /.test(p), 'cas ' + (i + 1) + ' : un tiret cadratin ou demi-cadratin dans le prompt');
  exiger(!/\\/.test(p), 'cas ' + (i + 1) + ' : un antislash dans le prompt (les chemins s\'écrivent avec des barres obliques)');
});

if (ecarts.length) {
  ecarts.forEach(function (e) { console.log('  ✗ ' + e); });
  console.log('Générateur : ' + ecarts.length + ' écart(s)');
  process.exit(1);
}
console.log('Générateur : 5 cas, aucun écart');
