# Module 07 — L'école : les cahiers de texte Yparéo et l'import de l'application Livrables

> **Quand l'activer.** Quand le cours se donne dans une école qui tient ses séances dans
> Yparéo et recueille les livrables dans l'application de l'auteur.
>
> **Paramètres.** `modules.ecole` : `ypareo`, `livrables_app` ; les dates réelles dans
> `cours.calendrier` (elles ne servent qu'ici, et vont dans `outils/sessions.py`) ; les
> promotions et matières exactes dans `filieres`.
>
> **Place.** Phase 12 du tronc, une fois les séances, les livrables et les évaluations
> arrêtés.
>
> **Seul.** Sur un cours qui existe déjà, donnez ce fichier à Claude dans le dossier du
> cours : il commence par la section 6.

---

## 1. Ce que le module produit

- [si `ypareo`] **Le cahier de texte** (`outils/generer_cahier_de_texte.py`, d'après
  `outils/seances.py` et `outils/sessions.py`) : un bloc par séance, « CONTENU DE LA
  SÉANCE » (sous-titre et objectifs de chaque chapitre, lus dans sa page ; l'atelier) et
  « TRAVAIL À FAIRE » (le travail, ce qu'il faut rendre et quand, le support), en `.txt` et
  `.docx`. « Avec ou sans accès » veut dire les deux (décision de l'auteur du 22 novembre
  2026) : la version sans identifiants sort toujours, `docs/Cahier_de_texte.*` ; celle qui
  porte les identifiants du site sort aussi quand `docs/acces.json` existe,
  `docs/Cahier_de_texte_avec_identifiants.*`, que le `.gitignore` et le `.rgignore`
  écartent. Sans accès à Yparéo, le même texte part dans l'application Livrables (feuille
  Séances, colonne Contenu). `--essai` signale un cahier périmé.
- [si `livrables_app`] **Les classeurs d'import** de l'application Livrables
  (`import-application/`, au format de `ecosysteme.doc_import_app`).

---

## 2. Le modèle

Le cours EADL (lecture seule) pour l'import Livrables et Yparéo ; dans le gabarit,
`outils/seances.py` (le programme, sans date), `outils/sessions.py` (les dates et les
promotions) et `outils/generer_cahier_de_texte.py`.

---

## 3. Les décisions à faire valider

Une question à la fois.

- **Les promotions et les matières**, écrites EXACTEMENT comme dans l'application.
- **Les échéances** des livrables (versions de travail et finales) et leur notation.
- **Ce qui se règle à la main** après l'import (les réglages d'un QCM, notamment).

---

## 4. La méthode

**Les cahiers de texte** : un bloc par séance réelle, d'après le découpage validé ; aucune
date dans le contenu du cours, mais les dates réelles ici ; la version « avec accès » ne
quitte jamais le poste.

**Les classeurs d'import** :

- cinq feuilles aux en-têtes exacts (Matières, Séances, Livrables, Critères, Ressources),
  séparateur « › » (U+203A) « Année › Promotion › Matière » ; promotions et matières
  EXACTEMENT celles de `filieres` ;
- des consignes détaillées (5 à 10 phrases), des grilles de critères qui totalisent la note
  maximale et s'adossent à la grille officielle, des ressources par séance.

**STOP** : l'auteur importe et vérifie l'aperçu.

---

## 5. Les pièges connus

- **Deux matières NOUVELLES dans un même fichier** : seule la première reçoit ses séances
  — un fichier par promotion.
- **Réimporter un livrable décoche « facultatif »**.
- **Un livrable s'identifie par (matière, séance, titre)** : changer l'un, c'est en créer un
  autre.
- **Pas de bonus négatif** ; **une note non saisie n'entre pas dans la moyenne**.
- **Les réglages d'un QCM se font à la main** après l'import.
- **`docs/acces.json` ne se lit jamais** : le générateur s'en sert, et refuse une valeur
  restée « a-remplir ».

---

## 6. Pour commencer

1. Lis le découpage en séances, les livrables et les évaluations validés.
2. Vérifie dans l'application les noms exacts des promotions et des matières (l'auteur les
   donne).
3. Pose les questions de cadrage, **une à une** (section 3).
4. Produis un cahier de texte et un classeur témoins, fais-les vérifier, puis le reste.

**Terminé** quand chaque format a son cahier de texte, chaque promotion son classeur, et
que l'auteur a importé et vérifié l'aperçu.

Sur un cours qui n'a pas été créé depuis le template, les règles de son `CLAUDE.md`
s'appliquent ; à défaut, celles du § 2 du `CLAUDE.md` du template.
