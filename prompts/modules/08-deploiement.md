# Module 08 — Le déploiement : la mise en ligne, ses garde-fous et ses contrôles

> **Quand l'activer.** Dès que le cours se publie sur l'hébergement de l'auteur.
>
> **Paramètres.** `modules.deploiement` : `actif`, `url`, `repertoire_distant`,
> `zones_protegees`, `site_protege`.
>
> **Place.** Phase 13 du tronc pour la première mise en ligne ; ensuite, après chaque étape
> publiable, toujours sur un accord distinct de celui du commit.
>
> **Seul.** Sur un cours qui existe déjà, donnez ce fichier à Claude dans le dossier du
> cours : il commence par la section 6.

---

## 1. Ce que le module produit

Le site en ligne à `modules.deploiement.url`, identique au dépôt, au bon endroit, protégé là
où il doit l'être — et un déploiement qu'on peut relancer sans risque.

---

## 2. Le mécanisme du gabarit

- **`deploiement/deployer.py`** : SFTP (l'hébergement mutualisé OVH refuse le FTPS) ;
  envoi incrémental, d'après un carnet déposé sur le serveur au nom du cours ; seuls les
  fichiers de `site/` suivis par Git partent.
- **La destination** vient de `deploiement/destination.json` (cours `cours.slug`,
  répertoire `modules.deploiement.repertoire_distant`), **jamais** de `config.json`, dont le
  répertoire éventuel n'est pas lu.
- **Le garde-fou** refuse un dossier qui appartient à un autre cours, un dossier sans
  carnet ou logé dans un autre cours ; `--adopter` sert seulement à reprendre SON cours,
  publié par un ancien outil.
- **Les protections** (`.htaccess`, `.htpasswd`, `.user.ini`, `.ovhconfig`) ne sont jamais
  écrasées ni purgées ; `deploiement/proteger_zones.py` pose celle des zones.
- **La sortie** ne montre ni l'hôte, ni le port, ni le répertoire distant, ni l'empreinte du
  serveur. Une commande qui en afficherait se filtre avant d'arriver à l'écran.
- Après toute modification du déployeur : `python3 deploiement/tester_deployer.py`.

---

## 3. La méthode, à chaque mise en ligne

1. **Les contrôles du tronc** (« Contrôles avant chaque mise en ligne ») et ceux des
   modules actifs.
2. **L'essai à blanc** : `deployer.py --essai` — destination attendue, garde-fou passé,
   aucun fichier hors de `site/`, la liste de ce qui partirait.
3. **L'accord de l'auteur**, distinct de celui du commit.
4. **Les zones protégées d'abord** : leur protection en ligne, vérifiée en 401 sans
   identifiant, avant leur contenu.
5. **L'envoi.**
6. **Le contrôle en ligne** : `--essai` annonce « déjà à jour » ; les pages modifiées
   répondent 200 depuis le site public, PDF et médias compris, aux tailles du dépôt ; les
   zones protégées répondent 401 sans identifiant.

---

## 4. Le site entièrement protégé (`site_protege: true`)

Tout le site est derrière un mot de passe posé côté serveur (`.htaccess`, `.htpasswd`, hors
dépôt ; Claude n'y touche jamais). Sans identifiants, chaque page, chaque PDF et chaque
piste répondent 401 : le contrôle en ligne devient « 401 partout, sans identifiant », et
l'auteur vérifie le contenu dans son navigateur. **Claude ne s'authentifie jamais.**

---

## 5. Les pièges connus

- **Une destination lue dans `config.json`** publierait dans le dossier d'un autre cours :
  d'où `destination.json` et le garde-fou.
- **Un dossier publié qui ne diffère d'un dossier exclu que par la casse** (`polycopie/` et
  `Polycopie/`) : Windows les confond, le serveur les distingue.
- **Les dossiers de travail** (`docs/`, `outils/`, `sources/`, `Polycopie/`, `Podcasts/`)
  ne partent jamais : seul `site/` se publie.
- **Aucune suppression de fichier distant** sans l'accord explicite de l'auteur : `--purge`
  demande confirmation, et `--purge-confirme`, qui n'en demande pas, ne s'emploie qu'après
  cet accord.

---

## 6. Pour commencer

1. Vérifie `deploiement/destination.json` (cours, répertoire) sans ouvrir `config.json`.
2. Lance les contrôles, puis `deployer.py --essai`, et montre ce qui partirait.
3. Demande l'accord de l'auteur ; protège les zones d'abord ; envoie ; contrôle en ligne.

**Terminé** quand le site public est identique au dépôt, au bon endroit, protégé là où il
doit l'être, et que `--essai` annonce « déjà à jour ».

Sur un cours qui n'a pas été créé depuis le template, les règles de son `CLAUDE.md`
s'appliquent ; à défaut, celles du § 2 du `CLAUDE.md` du template.
