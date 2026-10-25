# Module 07 — L'école : les cahiers de texte Yparéo et l'import de l'application Livrables

> **Quand l'activer.** Quand le cours se donne dans une école qui tient ses séances dans
> Yparéo et recueille les livrables dans l'application de l'auteur.
>
> **Paramètres.** `modules.ecole` : `ypareo`, `livrables_app` ; les dates réelles dans
> `cours.calendrier` (elles ne servent qu'ici) ; les promotions et matières exactes dans
> `filieres`.
>
> **Place.** Phase 12 du tronc, une fois les séances, les livrables et les évaluations
> arrêtés.
>
> **Seul.** Sur un cours qui existe déjà, donnez ce fichier à Claude dans le dossier du
> cours : il commence par la section 6.

---

## 1. Ce que le module produit

- [si `ypareo`] **Les cahiers de texte** (`docs/generate_cahier_de_texte.py`, un par
  format) : un bloc par séance, « CONTENU DE LA SÉANCE » et « TRAVAIL À FAIRE », en `.txt`
  et `.docx` ; une version « avec accès » (identifiants tirés de `docs/acces.json`) dans un
  dossier ignoré par Git.
- [si `livrables_app`] **Les classeurs d'import** de l'application Livrables
  (`import-application/`, au format de `ecosysteme.doc_import_app`).

---

## 2. Le modèle

Le cours EADL (lecture seule) pour l'import Livrables et Yparéo ; `docs/generate_cahier_de_texte.py`
du gabarit pour les cahiers de texte.

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
