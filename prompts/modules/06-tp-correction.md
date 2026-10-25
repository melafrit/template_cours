# Module 06 — Le TP et sa correction protégée

> **Quand l'activer.** Quand le cours fait produire un travail guidé dont les réponses ne
> doivent pas circuler : un TP pas à pas, un projet, une étude.
>
> **Paramètres.** `modules.tp` : `actif`, `sujet` ; les zones protégées se déclarent dans
> `modules.deploiement.zones_protegees`.
>
> **Place.** Phase 5 du tronc, après les contenus : le cours enseigne la méthode, le TP
> l'applique à un autre objet.
>
> **Seul.** Sur un cours qui existe déjà, donnez ce fichier à Claude dans le dossier du
> cours : il commence par la section 7.

---

## 1. Ce que le module produit

- **La page du TP** : l'énoncé, les étapes, ce qui est attendu, les modèles à remplir.
- **La correction**, derrière un mot de passe : `site/correction/` pour les étudiants (quand
  l'auteur la leur ouvre), `site/correction/formateur/` pour le formateur (barème, grilles,
  corrigé commenté), avec ses capsules si le module audio est actif.

---

## 2. Le modèle

- **Le gabarit** : les zones protégées du déployeur (`deploiement/proteger_zones.py`), les
  comptes dans `docs/acces-zones.json` (secret ; modèle : `docs/acces-zones.exemple.json`).
- **Le cours d'architecture logicielle** (lecture seule) : la correction du TP et ses
  capsules, l'espace formateur, le contrôle des interdits (`outils/verifier_tp.py`).
- **Le cours EADL** (lecture seule) : un projet au lieu d'un TP, trois zones protégées par
  langue, un site entièrement protégé.

---

## 3. Les décisions à faire valider

Une question à la fois.

- **Le sujet du TP** (`modules.tp.sujet`) : un autre objet que l'exemple du cours, pour que
  le cours n'en souffle rien.
- **Les zones** : correction étudiante, espace formateur, et qui reçoit quels identifiants.
- **Le moment où la correction s'ouvre** aux étudiants.

---

## 4. La méthode

1. **Les interdits** : le sujet du TP, ses chiffres et ses mots n'apparaissent que sur les
   pages du TP et dans la correction ; ils entrent dans `interdits`, contrôlés par les
   générateurs sur toutes les pages publiques.
2. **La page du TP** : énoncé, étapes, attendus, modèles adaptés au cas.
3. **La correction** : réponses, corrigé commenté, barème adossé à la grille officielle.
4. **La protection d'abord** : `deploiement/proteger_zones.py` pose la protection en ligne
   **avant** le premier envoi de la correction ; le déployeur retient les fichiers d'une
   zone tant qu'elle n'est pas protégée.

---

## 5. Les pièges connus

- **Un exemple de méthode qui ressemble au sujet du TP** souffle la réponse : il porte sur
  un cas neutre.
- **Un QR code, un renvoi ou une capsule publique vers la correction** l'ouvrent à tous :
  aucun ne doit y mener depuis les pages publiques ou le livret.
- **Claude ne s'authentifie jamais sur le site en ligne** : la protection se vérifie par un
  401 sans identifiant ; l'auteur teste l'accès dans son navigateur.
- **Les fichiers d'accès** (`docs/acces-zones.json`) ne se lisent jamais : les scripts s'en
  servent.

---

## 6. Les contrôles

Aucun interdit sur les pages publiques ; aucun lien public vers la correction ; la zone
répond 401 sans identifiant, en ligne, avant que son contenu parte ; l'auteur confirme
l'accès avec les identifiants.

**Terminé** quand le TP est en ligne, sa correction protégée et vérifiée en 401, et que les
décisions, l'état d'avancement et `TODO.md` sont à jour.

---

## 7. Pour commencer

1. Lis la fiche du fil rouge, la grille et les modèles de `sources/`.
2. Propose le sujet du TP et ce qui le distingue de l'exemple du cours.
3. Pose les questions de cadrage, **une à une** (section 3).
4. Écris la page du TP, puis la correction ; la protection en ligne avant tout envoi.

Sur un cours qui n'a pas été créé depuis le template, les règles de son `CLAUDE.md`
s'appliquent ; à défaut, celles du § 2 du `CLAUDE.md` du template.
