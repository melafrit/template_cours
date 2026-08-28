# Déploiement vers OVH

Envoie le site du cours vers l'hébergement OVH par FTP, depuis n'importe quel poste.
Aucune dépendance à installer : tout vient de la bibliothèque standard de Python 3,
présent d'origine sur macOS.

## Première fois

```bash
cp deploiement/config.exemple.json deploiement/config.json
```

Ouvrez `config.json` et renseignez les quatre champs du haut : `hote`, `identifiant`,
`motdepasse`, `repertoire_distant`. Les trouver dans votre espace client OVH :
**Hébergements → votre hébergement → FTP - SSH**. L'hôte ressemble à
`ftp.clusterXXX.hosting.ovh.net`.

`config.json` est ignoré par Git. Vos identifiants ne partiront jamais dans le dépôt,
qui est public.

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
| `--essai` | Simulation : affiche ce qui serait envoyé, n'envoie rien. |
| `--tout` | Ignore le carnet et réenvoie tous les fichiers. |
| `--purge` | Supprime en ligne les fichiers absents du dépôt. Demande confirmation. |
| `--purge-confirme` | Même chose, sans question posée. Pour un lancement non interactif. |

## Ce qu'il faut savoir

**Le transfert est incrémental.** Le site pèse plus de 300 Mo, dont l'essentiel en
podcasts et en slides qui ne changent jamais. Le script compare l'empreinte SHA-256 de
chaque fichier à celle du dernier envoi réussi et n'envoie que ce qui a changé. Après le
premier envoi, publier une correction de texte prend quelques secondes.

**Le carnet des envois vit sur le serveur**, dans `.deploiement-manifeste.json`, à la
racine du répertoire du cours. C'est ce qui permet de déployer depuis plusieurs postes :
le Mac et n'importe quelle autre machine lisent le même carnet, donc aucun ne réexpédie
ce que l'autre a déjà déposé. Un carnet local est tenu en parallèle, mais il ne sert que
de secours si le serveur est injoignable.

Conséquence utile : `--essai` se connecte pour lire le vrai carnet. La simulation dit
donc exactement ce qui partirait, au lieu de le deviner.

**Une interruption ne coûte rien.** Le manifeste est écrit au fil de l'eau : si le réseau
tombe au milieu d'un envoi de 300 Mo, relancer reprend là où vous en étiez.

**La liste de ce qui part est celle de Git.** Ce qui est ignoré par Git — identifiants,
PNG sources, fichiers temporaires — ne peut pas partir par accident. Les motifs de
`exclure` retirent ensuite ce qui est suivi mais n'a rien à faire sur un serveur : les
générateurs Python, les fiches de production, ce fichier même.

**FTPS par défaut.** En FTP simple, mot de passe et contenus circulent en clair sur le
réseau. Ne passez `tls` à `false` que si votre hébergement ne propose pas le FTP
sécurisé — et sachez alors ce que vous acceptez.

**`--purge` ne vise que votre répertoire de cours.** Le script refuse de démarrer si
`repertoire_distant` pointe sur `/`, `/www`, `/htdocs` ou `/public_html` : une purge à
la racine effacerait tout ce que ce dépôt ne connaît pas.

## Si quelque chose bloque

| Symptôme | Piste |
|---|---|
| La connexion s'établit puis le transfert reste figé | Passez `passif` à `false`. |
| `530 Login incorrect` | L'identifiant OVH n'est pas votre e-mail : c'est celui de la section FTP. |
| `522 SSL/TLS required` ou l'inverse | Inversez `tls`. |
| Accents cassés dans les noms de fichiers | Le serveur ne gère pas UTF-8. Aucun fichier du dépôt n'a d'accent : signalez-le si cela arrive. |
| Tout est « inchangé » alors que le serveur est vide | Supprimez `.deploiement-manifeste.json` sur le serveur, ou lancez `--tout`. |
