# Module 07 — L'école : les cahiers de texte Yparéo et l'import de l'application Livrables

> **Quand l'activer.** Quand le cours se donne dans une école qui tient ses séances dans
> Yparéo et recueille les livrables dans l'application de l'auteur.
>
> **Paramètres.** `modules.ecole` : `ypareo`, `livrables_app` ; les dates réelles dans
> `cours.calendrier` (elles ne servent qu'ici, et vont dans `outils/sessions.py`) ; les
> promotions et matières exactes dans `filieres`. Dans `cours.json`, ils s'écrivent dans
> le bloc `ecole` (l'adresse de Livrables, le bouton du QCM, une session par promotion
> avec sa promotion et sa matière exactes et ses dates réelles) et, pour chaque filière,
> dans `bloc`, `module` et `epreuves`. `nouveau_cours.py` les reporte dans
> `outils/accueil.py`, `outils/seances.py` et `outils/sessions.py` du cours créé.
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
- [si une filière prépare l'épreuve d'un bloc] **La pastille et les boutons des épreuves**
  de l'accueil : `FILIERES` de `outils/seances.py` déclare pour chaque filière son bloc,
  son module et la page de ses épreuves ; l'accueil ajoute à sa pastille « EADL, Bloc 1,
  module FM04 » et un bouton « Épreuves du Bloc 1 » par filière (`outils/accueil.py`, sur
  le modèle du cours EADL). La démonstration n'en déclare aucune (décision de l'auteur du
  22 novembre 2026).
- [si `livrables_app`] **Le classeur d'import** de l'application Livrables
  (`outils/generer_classeur_livrables.py`, au format de `ecosysteme.doc_import_app`) : un
  classeur par session de `outils/sessions.py`, donc par promotion,
  `docs/Import_Livrables_<session>.xlsx`, et à côté `docs/Import_Livrables_<session>_reglages.txt`,
  les réglages que l'import ne porte pas. Les séances, les livrables, la grille, la
  description de la matière et les ressources viennent de `outils/seances.py` ; la colonne
  Contenu reprend le cahier de texte ; les liens viennent de `deploiement/destination.json`
  et restent vides, jamais inventés, tant que l'adresse du site n'y est pas. `--essai`
  signale un classeur périmé. Ni le classeur ni ses réglages ne sont versionnés.

---

## 2. Le modèle

Le cours EADL (lecture seule) pour l'import Livrables et Yparéo ; dans le gabarit,
`outils/seances.py` (le programme, sans date), `outils/sessions.py` (les dates et les
promotions), `outils/generer_cahier_de_texte.py` et `outils/generer_classeur_livrables.py`.
Pour l'application elle-même, son `docs/PROMPT-CLASSEUR-IA.md` (le format) et son
`docs/GUIDE-ENSEIGNANT.md` (ce que font ses cases).

---

## 3. Les décisions à faire valider

Une question à la fois.

- **Les promotions et les matières**, écrites EXACTEMENT comme dans l'application.
- **Les épreuves de chaque filière** : son bloc, son module, l'adresse de la page de ses
  épreuves (ouverte et vérifiée avant d'être ajoutée) et sa langue.
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
- une description de la matière (3 à 6 phrases), des consignes détaillées (5 à 10
  phrases), des grilles de 4 à 6 critères qui totalisent la note maximale et s'adossent à
  la grille officielle, des ressources par séance ; le générateur refuse d'écrire un
  classeur qui s'en écarte ;
- un QCM passé sur le site du cours se dépose en « Exercice / TP », rendu par son fichier
  CSV ; le type « QCM » est réservé au QCM que l'application corrige elle-même.

**STOP** : l'auteur importe et vérifie l'aperçu.

---

## 5. Les pièges connus

- **Deux matières NOUVELLES dans un même fichier** : seule la première reçoit ses séances
  — un fichier par promotion.
- **Réimporter un livrable décochait « facultatif »** : le code de l'application, relu le
  22 novembre 2026, laisse désormais la case en place. Vérifiez-la après un réimport.
- **« Livrable bonus, facultatif » rend un livrable non dû** : ceux qui ne l'ont pas rendu
  sortent du compteur des manquants. Une version de travail obligatoire et non notée ne
  la coche pas ; on ne lui saisit simplement aucune note.
- **Un rendu est un lien** tant que « Autoriser les fichiers joints » n'est pas cochée, et
  l'import ne porte pas cette case : le fichier de réglages la rappelle.
- **Le type « QCM » corrige une grille d'après un corrigé à lettres fixes** : il ne
  convient pas au QCM du site, qui mélange questions et propositions.
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
