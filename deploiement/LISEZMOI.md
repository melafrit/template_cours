# Déploiement vers OVH

Envoie le site du cours (`site/`) vers l'hébergement OVH, par **SFTP** (ou FTPS / FTP), depuis
n'importe quel poste. Seule dépendance : `paramiko` pour le SFTP
(`python3 -m pip install paramiko`) ; FTP et FTPS n'utilisent que la bibliothèque standard.

## Deux fichiers, deux rôles

| Fichier | Contenu | Versionné ? |
|---|---|---|
| `deploiement/config.json` | **les accès** : hôte, identifiant, mot de passe, protocole | **non** — secret, ignoré par Git |
| `deploiement/destination.json` | **où va CE cours** : son identifiant (`cours`) et son répertoire distant | oui, avec le cours |

`config.json` est **le même pour tous vos cours** : il se recopie d'un cours à l'autre sans être
ouvert ni modifié (`nouveau_cours.py` le fait pour vous, en local). Le **répertoire distant n'y est
jamais lu** : recopiée, cette configuration désignerait encore le dossier du cours précédent, et
le premier envoi du nouveau cours l'aurait écrasé.

`destination.json` est écrit par `nouveau_cours.py` d'après le bloc `publication` de `cours.json`.
À défaut, copiez `destination.exemple.json` et renseignez-le.

## Première fois

```bash
cp deploiement/config.exemple.json deploiement/config.json   # si vous n'en avez pas déjà un
```

Dans `config.json` : `hote`, `identifiant`, `motdepasse`, `protocole` (`sftp` recommandé, port 22).
Les trouver dans votre espace client OVH : **Hébergements → votre hébergement → FTP - SSH**.

Vérifiez ensuite ce qui partirait, sans rien envoyer :

```bash
python3 deploiement/deployer.py --essai
```

## Publier

```bash
python3 deploiement/deployer.py
```

## Les options

| Option | Effet |
|---|---|
| `--essai` | Simulation : se connecte, vérifie le garde-fou, affiche ce qui serait envoyé, n'envoie rien. |
| `--tout` | Ignore le carnet et réenvoie tous les fichiers. |
| `--purge` | Supprime en ligne les fichiers absents du dépôt. Demande confirmation. |
| `--purge-confirme` | Même chose, sans question posée. Pour un lancement non interactif. |
| `--adopter` | Reprend un dossier déjà publié par un autre outil (voir le garde-fou). Jamais avec `--purge`. |

Codes de sortie : `0` réussi, `1` échecs partiels (relancer reprend), `2` connexion impossible,
`3` envoi refusé par le garde-fou.

## Le garde-fou d'identité

Le carnet des envois, `.deploiement-manifeste.json`, est déposé dans le dossier du cours et porte
son identifiant. Avant d'écrire quoi que ce soit, le script vérifie le dossier distant :

| Ce qu'il trouve | Décision |
|---|---|
| dossier absent, vide, ou ne contenant que des protections (`.htaccess`…) | envoi — premier déploiement |
| carnet au nom de ce cours | envoi |
| carnet au nom d'un **autre** cours | **refus**, même avec `--adopter` |
| carnet sans identifiant (ancien déployeur), carnet illisible, fichiers sans carnet | **refus**, sauf `--adopter` |
| un site déjà publié dans un dossier **parent** | **refus** : sa purge effacerait ce cours |

`--adopter` sert à reprendre **votre** cours publié avec un ancien outil. Il ne se combine pas
avec `--purge` : adoptez, vérifiez le site, purgez lors d'un envoi suivant.

## Les protections du serveur

**Jamais envoyés, jamais purgés** : `.htaccess`, `.htpasswd`, `.user.ini`, `.ovhconfig`, et les
motifs de `proteger`. Un mot de passe posé côté serveur survit ainsi à chaque publication.

**Les zones protégées** (`zones_protegees` dans `destination.json` — la correction d'un TP, la
partie formateur) ne partent qu'une fois leur `.htaccess` en ligne. Pour les poser :

```bash
cp docs/acces-zones.exemple.json docs/acces-zones.json      # comptes et zones, ignoré par Git
python3 deploiement/proteger_zones.py --hors-ligne          # construit et contrôle, sans connexion
python3 deploiement/proteger_zones.py                       # pose, relit, vérifie le 401
python3 deploiement/deployer.py                              # le contenu des zones part alors
```

**L'ordre compte** : la protection d'abord, le contenu ensuite. Le déployeur le garantit, en
retenant le contenu d'une zone tant que sa protection n'est pas en ligne.

## Ce qu'il faut savoir

**Le transfert est incrémental.** Le script compare l'empreinte SHA-256 de chaque fichier à celle
du dernier envoi réussi et n'envoie que ce qui a changé. Après le premier envoi, publier une
correction de texte prend quelques secondes.

**Le carnet vit sur le serveur.** C'est ce qui permet de déployer depuis plusieurs postes : le Mac
et le PC lisent le même carnet, aucun ne réexpédie ce que l'autre a déjà déposé. Un carnet local
est tenu en parallèle, mais il ne sert que de secours si le serveur est injoignable. Conséquence
utile : `--essai` se connecte pour lire le vrai carnet, et dit exactement ce qui partirait.

**Une interruption ne coûte rien.** Le carnet est écrit au fil de l'eau : relancer reprend là où
vous en étiez. Il part même **avant** le premier fichier : un premier envoi interrompu laisse un
dossier marqué au nom du cours, que le garde-fou reconnaîtra.

**La liste de ce qui part est celle de Git**, limitée à `site/`. Ce qui est ignoré par Git —
identifiants, PNG sources, fichiers temporaires — ne peut pas partir par accident. **Un fichier
non commité ne part pas** : commitez avant de déployer.

**SFTP par défaut.** L'hébergement mutualisé OVH refuse le FTPS mais ouvre SSH. L'empreinte du
serveur est retenue au premier contact dans `deploiement/known_hosts` (ignoré par Git), puis
exigée : un serveur qui change d'empreinte fait échouer la connexion au lieu de recevoir le mot de
passe.

**`--purge` ne vise que le dossier du cours.** Le script refuse une racine d'hébergement (`/`,
`/www`, `/htdocs`, `/public_html`) et un dossier logé dans un autre cours.

## Après chaque envoi

- `python3 deploiement/deployer.py --essai` doit annoncer « déjà à jour » ;
- les pages modifiées s'ouvrent à l'adresse rappelée en fin d'envoi ;
- une zone protégée répond **401** sans identifiants (`proteger_zones.py` le vérifie).

## Tester le déployeur

```bash
python3 deploiement/tester_deployer.py
```

Hors ligne : un faux serveur en mémoire, des fichiers de configuration temporaires. À lancer après
toute modification de `deployer.py`.

## Si quelque chose bloque

| Symptôme | Piste |
|---|---|
| « envoi refusé » | Lisez la raison : `destination.json` vise sans doute le mauvais dossier. |
| `identifiant ou mot de passe refusé par le serveur SSH` | Identifiant de la section FTP-SSH d'OVH, pas votre e-mail. |
| `500 This security scheme is not implemented` | Le serveur refuse le FTPS : passez `protocole` à `sftp`. |
| La connexion s'établit puis le transfert reste figé (FTP) | Passez `passif` à `false`. |
| `l'empreinte du serveur a changé` | Vérifiez auprès d'OVH **avant** de supprimer `deploiement/known_hosts`. |
| Tout est « inchangé » alors que le serveur est vide | Lancez `--tout`. |
