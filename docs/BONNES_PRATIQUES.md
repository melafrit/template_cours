# Bonnes pratiques

Ce fichier ne liste pas des règles : il donne les **raisons**. Chaque point
vient d'un défaut réellement rencontré en construisant ce template et le cours
dont il est issu. Une règle dont on a oublié le motif finit toujours par être
contournée.

---

## 1. Vérifier, plutôt qu'affirmer

C'est la pratique qui rend toutes les autres possibles.

Trois défauts trouvés dans ce dépôt étaient **invisibles à la relecture** :

- La palette par défaut échouait à cinq contrôles de contraste. Le doré sur
  blanc donnait 2,47:1 pour un minimum de 3, et il colorait des titres. Personne
  ne l'avait vu en deux ans d'usage.
- La barre d'étapes restait en français sur une page passée en anglais. C'est
  l'élément le plus visible d'un chapitre.
- Le générateur audio annonçait « rien à faire » alors que six capsules
  manquaient : il ne savait pas lire la nouvelle façon de déclarer les sources.

Aucun de ces trois ne se voit en lisant le code. Tous les trois se voient en
lançant un vérificateur ou en ouvrant la page.

**En pratique** : après chaque modification d'un moteur, ouvrir la page.
Après chaque modification d'une palette ou d'un libellé, lancer le
vérificateur correspondant. Ce sont quelques secondes.

---

## 2. Le piège du cache, et comment il fait perdre une heure

Un serveur de développement ordinaire n'envoie aucun en-tête de cache. Après
une modification, le navigateur ressert l'ancien JavaScript : on croit la
correction ratée, on la refait, on cherche un défaut qui n'existe pas.

`demarrer.py` envoie `Cache-Control: no-store` pour cette raison. Mais **cela
ne suffit pas toujours** : certains navigateurs gardent malgré tout le script
en mémoire, y compris dans un onglet neuf.

**Le symptôme à reconnaître** : votre fichier contient la correction, mais la
page se comporte comme avant. Avant de suspecter le code, prouvez-le
autrement — par exemple :

```bash
node -e "global.window={}; eval(require('fs').readFileSync('site/assets/js/ui-labels.js','utf8')); console.log(Object.keys(window.UI_LABELS.fr).length)"
```

Si le fichier est bon et la page fausse, **changez de port**. Une nouvelle
origine n'a aucun cache à réutiliser.

---

## 3. Un serveur mono-thread bloque sur un navigateur

`socketserver.TCPServer` traite une requête à la fois. Un navigateur qui garde
sa connexion ouverte bloque alors tout autre client — un second onglet, un
outil de vérification. Le symptôme est un gel, sans message, impossible à
rattacher à sa cause.

`demarrer.py` utilise donc `ThreadingHTTPServer`. Si vous écrivez un autre
outil qui sert des fichiers, faites de même.

---

## 4. Ne jamais éditer un fichier généré

Trois fichiers de ce dépôt sont produits par un script : l'index de playlist,
l'index des sections, et les transcriptions des capsules. Les corriger à la
main donne l'illusion d'avoir résolu le problème — jusqu'à la régénération
suivante, qui écrase tout sans prévenir.

Le cas le plus insidieux est la **transcription d'une capsule**. Elle existe
en deux versions : le script balisé pour la synthèse vocale, et le texte
lisible affiché sous le lecteur. Tenues à la main, elles divergent dès la
première correction — et personne ne s'en aperçoit, parce qu'on ne lit pas la
transcription d'une capsule qu'on vient d'écouter.

**La fiche de production est la source unique.** On corrige là, puis on relance
`outils/synchroniser_capsules.py`.

---

## 5. Rien de propre à une matière dans un moteur

Un moteur qui connaît sa matière rend le template inutilisable pour une autre.

Deux exemples réels, corrigés :

- `glossaire-tooltip.js` portait en dur une liste de notions de protection des
  données et leurs alias. Passés dans les données (`GLOSSARY_CURATED`).
- Le composant de scénario affichait « Conséquence juridique ». Un cours de
  biologie n'a pas de conséquences juridiques : le libellé est devenu une
  option de la page.

**Le test** : si le mot ne s'applique pas à un cours de cuisine, il n'a rien à
faire dans un moteur.

---

## 6. Un squelette ne doit rien garder de la démonstration

`nouveau_cours.py` fabrique les squelettes de chapitre à partir du chapitre
vitrine — ainsi ils ne peuvent pas diverger du moteur réel. Mais **vidés**.

La première version gardait la prose. Un chapitre de cybersécurité serait
arrivé rempli de texte sur le fil rouge et le public cible ; une section
oubliée à la relecture serait partie en ligne en parlant d'autre chose.

Quatre endroits portaient du contenu, et trois avaient été manqués au premier
essai : la prose des sections, les **objectifs** (qui sont dans l'en-tête, hors
de la plage traitée), la **méta-description** (qui part dans les moteurs de
recherche et les aperçus de partage), et les **titres d'étapes**, qui sont des
attributs et non des blocs `data-tr`.

**Quand on vide quelque chose, on vérifie qu'il est vide** — par une recherche
sur des mots du contenu d'origine, pas par une relecture.

---

## 7. Le bilingue se perd par les bords

Le contenu rédigé se traduit facilement : les blocs sont jumelés, un
vérificateur compte les déséquilibres. Ce qui échappe, ce sont les textes
**fabriqués en JavaScript**.

Trois catégories, et la troisième est la plus traître :

1. Les libellés construits à chaque rendu : ils suivent si le moteur se
   redessine sur `tpl:langchange`.
2. Les libellés écrits **une seule fois** à la construction — « Tout
   afficher », « Précédent », le titre d'un en-tête pliable. Ils restent dans la
   langue du chargement. Il faut les repeindre explicitement.
3. Les **attributs** : `aria-label`, `title`, `alt`, `placeholder`. Ils ne se
   voient pas à l'écran, donc leur oubli ne se remarque jamais — sauf par qui
   utilise un lecteur d'écran.

`outils/verifier_i18n.py` attrape les clés dépareillées et les blocs
déséquilibrés. Il n'attrape pas le point 2 : celui-là se voit en basculant la
langue et en regardant.

---

## 8. Un contrôle qualité qui vit dans le code, pas dans la configuration

Le générateur audio mesure chaque prise avant de la déposer : durée, débit,
silences. Ce qui sort des clous part en quarantaine avec la raison, jamais en
ligne.

Les seuils vivent **dans le script**, pas dans la configuration. Une première
version les avait placés dans le fichier de configuration : une copie faite
avant un recalibrage gardait les anciennes valeurs et rejetait de bonnes
prises, sans que personne comprenne pourquoi.

Une fiche peut toutefois déclarer sa **propre fenêtre de durée** quand elle
s'écarte du format habituel — une capsule de 45 secondes serait rejetée par des
seuils calibrés sur des capsules de deux minutes. Seule la durée s'assouplit :
le débit et les silences restent mesurés à l'identique, parce que ce sont eux
qui révèlent une prise inaudible.

Le motif est général : **un contrôle qu'on peut désactiver par mégarde ne
protège de rien.**

---

## 9. Mesurer sur des données réelles, pas sur une intuition

Avant d'écrire une capsule, on estime sa durée. L'estimation par « à peu près
150 mots par minute » se trompe assez pour faire rejeter des prises.

La bonne méthode : mesurer le débit **sur les prises déjà validées** du projet,
prendre la médiane, et dimensionner le script là-dessus. Sur ce dépôt, la
médiane observée est de 146 mots par minute — et les six capsules générées sont
tombées à quelques secondes de l'estimation.

Même logique pour les seuils de contraste, les tailles d'image, les durées de
section : la donnée existe, il suffit de la lire.

---

## 10. Les commentaires disent le pourquoi

Le code dit déjà ce qu'il fait. Ce qu'il ne dit pas, c'est **le piège qu'on a
rencontré** et la raison du choix.

Un commentaire utile ressemble à :

```python
# Sans SO_REUSEADDR, volontairement : sous Windows cette option autorise à se
# lier à un port DÉJÀ pris, là où Unix le refuse. La sonde répondait « libre »
# pour un port occupé, et le serveur se posait par-dessus un autre.
```

Il empêche la prochaine personne — souvent vous — de « simplifier » en
réintroduisant le défaut.

---

## 11. Ce qui ne doit jamais entrer dans le dépôt

- **Les clés et identifiants.** Clé ElevenLabs, accès FTP. Ils engagent des
  dépenses ou donnent un accès en écriture, et l'historique Git ne s'efface
  pas : ce qu'on y met un jour y reste.
- **Les documents sous droits.** Référentiels, manuels, articles déposés dans
  `sources/`. Citer une source n'est pas la republier : c'est la bibliographie
  qui est versionnée, pas les fichiers.
- **Les noms d'étudiants**, si le cours produit des livrables évalués.

Vérifiable en une commande :

```bash
git check-ignore -v outils/elevenlabs.json deploiement/config.json sources/un-fichier.pdf
```

---

## 12. Dire ce qui n'a pas été fait

Un travail annoncé terminé qui ne l'est pas coûte plus cher qu'un travail
annoncé partiel : on construit dessus, et l'erreur se découvre trois étapes
plus loin.

Cela vaut pour les rendus de Claude comme pour les vôtres. Quand un lot est
livré, dire ce qu'il contient **et ce qu'il ne contient pas encore**.

---

## 13. Un secret se recopie, il ne se lit pas

La clé ElevenLabs, la voix clonée, les accès à l'hébergement sont les mêmes pour
tous les cours de l'auteur. Les ressaisir à chaque cours, c'est les faire
transiter par une conversation, un message, un presse-papiers — autant d'endroits
d'où ils ne repartent jamais.

Ils se **recopient donc tels quels**, octet pour octet, du template vers le cours
(`nouveau_cours.py` le fait), et seulement si le `.gitignore` du cours les exclut.
Claude ne les ouvre pas : les scripts s'en servent. Une recherche dans le dépôt
les exclut explicitement — un `grep` sur tout le dossier affiche aussi ce qu'il y
a dans un fichier de secrets.

Pour vérifier qu'une copie est fidèle sans la lire, on compare les empreintes :

```bash
sha256sum ../template_cours/outils/elevenlabs.json outils/elevenlabs.json
```

---

## 14. Une configuration recopiée ne doit pas décider où l'on publie

Le premier déployeur lisait le répertoire distant dans la même configuration que
le mot de passe. Recopiée pour un nouveau cours, elle désignait le dossier du
cours précédent : le premier envoi l'aurait écrasé, la première purge l'aurait
vidé — et les étudiants l'auraient découvert avant l'auteur.

La destination vit donc à part, dans `deploiement/destination.json`, versionné
avec le cours et écrit à sa création. Et le carnet déposé sur le serveur porte
l'identifiant du cours : le déployeur refuse d'écrire dans un dossier marqué au
nom d'un autre, dans un dossier occupé sans carnet, ou dans un dossier logé à
l'intérieur d'un autre cours. Le garde-fou se teste hors ligne
(`deploiement/tester_deployer.py`) : un faux serveur, aucun risque.

Le motif est général : **ce qui se recopie d'un projet à l'autre ne doit porter
que ce qui est vraiment commun.**

---

## 15. La protection d'abord, le contenu ensuite

La correction d'un TP vit derrière un mot de passe. Publiée une minute avant sa
protection, elle a été vue — ou peut l'avoir été, ce qui revient au même.

Le déployeur retient donc le contenu d'une zone protégée tant que son
`.htaccess` n'est pas en ligne, et ne remplace ni ne purge jamais un `.htaccess`,
un `.htpasswd`, un `.user.ini` ou un `.ovhconfig` posé côté serveur.
`deploiement/proteger_zones.py` pose la protection, la relit, et vérifie que la
zone répond 401 sans identifiants.

---

## 16. Un témoin avant la série

Une série de capsules se paie d'avance et s'écoute après. Une voix mal réglée,
un accent qui ne s'entend pas, un débit trop rapide : toutes les pistes partent
avec le même défaut.

On génère donc **une** prise témoin, à côté (`--temoin`), que l'auteur écoute sur
la page ; la série ne part qu'ensuite. Le générateur refuse une série tant
qu'aucun témoin n'existe pour le modèle. C'est ainsi qu'ont été tranchés le modèle
(Eleven v4), l'accent (la formulation « marquée », la « naturelle » ne
s'entendant pas) et la lecture posée des capsules explicatives.

L'accent, comme les seuils de contrôle, vit **dans le générateur**, pas dans la
configuration (§ 8) : une configuration ancienne ne doit pas faire repartir une
prise sans accent.

---

## 17. Une explication démonte aussi l'erreur

Une explication qui ne dit que pourquoi la bonne réponse est juste laisse
l'étudiant seul avec son erreur. Or c'est la proposition qu'il a choisie qu'il
faut démonter : l'idée fausse qui la rendait tentante, et pourquoi elle ne tient
pas ici.

Chaque question à choix porte donc une raison par proposition écartée, et deux à
quatre renvois vers **l'endroit exact** qui répond — la section, le schéma, la
fiche —, jamais « le chapitre 3 ». `outils/verifier_liens.py` contrôle chaque
renvoi, fichier **et** ancre : un renvoi vers la bonne page mais la mauvaise
section ne se voit qu'en cliquant.

---

## 18. Une adresse externe s'ouvre avant d'être citée

Une adresse recopiée de mémoire, ou devinée d'après le titre d'un article, mène
une fois sur deux à une page d'erreur — ou pire, à une autre page. Chaque lien
externe s'ouvre donc avant d'être ajouté, s'affiche dans un nouvel onglet
(`target="_blank" rel="noopener noreferrer"`) et se signale aux lecteurs d'écran.

---

## 19. Vérifier sans écran

L'onglet de navigateur intégré à l'outil ne s'affiche pas toujours. Un navigateur
sans interface (Edge ou Chrome lancé en `--headless`, piloté par le protocole de
débogage) fait alors les captures et les parcours automatiques : cliquer chaque
proposition d'un quiz, mesurer un contraste, vérifier qu'une ancre est visible.
Ce qui compte, c'est que la vérification ait lieu, pas l'outil qui la fait.
