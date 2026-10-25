# Module 05 — Les évaluations : QCM en ligne, papier et d'entraînement, et leur correction publique

> **Quand l'activer.** Dès que le cours se conclut par une évaluation, ou prépare une
> épreuve. Les points de contrôle, eux, valent pour tout cours.
>
> **Paramètres.** `modules.evaluations` : `qcm_en_ligne`, `qcm_papier`,
> `qcm_entrainement`, `correction_publique`, `points_de_controle`.
>
> **Place.** Phase 6 du tronc, après les contenus et le TP.
>
> **Seul.** Sur un cours qui existe déjà, donnez ce fichier à Claude dans le dossier du
> cours : il commence par la section 7.

---

## 1. Ce que le module produit

- Des **points de contrôle** expliqués, un par section importante.
- [si actif] Le **QCM en ligne** noté (`prompts/07_qcm_banque.md`) : notation CBM (degré de
  certitude), correction signée et tableau de bord du formateur — le moteur du gabarit.
- [si actif] Le **QCM papier** (`prompts/08_qcm_papier.md`) : livrets, corrigé commenté,
  grille.
- [si actif] Le **QCM d'entraînement** : des questions **différentes** du QCM noté, même
  barème.
- [si actif] La page publique **« ✅ Correction des QCM »**, juste après « 🏋️ QCM
  d'entraînement » dans le menu : chaque question du cours, sa réponse et ses explications,
  pour réviser.

**Toujours**, quelle que soit la forme : chaque proposition expliquée — pourquoi la bonne
réponse est juste, pourquoi chacune des autres ne l'est pas — et deux à quatre renvois
« Pour approfondir » vers l'endroit exact du cours ou une référence externe vérifiée
(`prompts/15_explications_quiz.md`). Ce n'est pas une option.

---

## 2. Le modèle

- **Le moteur du gabarit** : `site/QCM/` (QCM, entraînement, correction, tableau de bord),
  `questions.js` et `corrections.js` (mêmes `id`), `tools/generate_qcm_papier.py`.
- **La correction publique**, sur le cours d'architecture logicielle (lecture seule) :
  `QCM/correction-des-qcm.html` et sa jumelle anglaise, écrites par
  `outils/generer_qcm_formateur.py` (476 questions et leurs explications pour grand
  débutant), décisions D96 (la page devient publique) et D107 (sa version anglaise).
- **Le QCM papier à certitude** (Leclercq), sur le cours CDWFS (lecture seule).

---

## 3. Les décisions à faire valider

Une question à la fois.

- **Le nombre de questions** de chaque QCM, et leur répartition par chapitre et par
  difficulté.
- **La notation** (CBM pour le QCM en ligne ; pour le papier, propositions et barème de
  certitude), d'après le règlement et la grille de l'épreuve.
- **Un QCM papier par filière**, ou un seul ?
- **La correction publique** : ce qu'elle reprend (chapitres, fiches, banque
  d'entraînement) ; jamais le QCM papier de l'épreuve, jamais la correction du TP.

---

## 4. La méthode

- **QCM en ligne** : réponse unique, positions de la bonne réponse équilibrées,
  distracteurs débiaisés (même longueur, même registre), explications complètes.
- **QCM papier** : mélange déterministe, audit des biais (position, longueur) ; livret,
  corrigé commenté, grille. **STOP** : l'auteur relit les livrets.
- **QCM d'entraînement** : questions différentes du noté, même barème, chaque proposition
  expliquée.
- **Correction publique** : générée d'après les questions telles que les pages les
  écrivent ; textes adressés aux étudiants (« Pour réviser »).

---

## 5. Les pièges connus

- **Une explication qui ne traite que la bonne réponse** n'apprend rien à celui qui s'est
  trompé : chaque proposition fausse a la sienne.
- **Une question du QCM noté reprise à l'entraînement** fausse la note.
- **Le QCM papier de l'épreuve ne va jamais sur le site**, ni sa banque dans un dépôt
  public.
- **Les identifiants des questions** doivent correspondre entre questions et corrections.

---

## 6. Les contrôles

Positions et longueurs équilibrées (audit) ; chaque proposition expliquée, deux à quatre
renvois qui mènent quelque part (`verifier_liens.py`) ; questions et corrections alignées ;
au navigateur, passer le QCM, exporter, corriger, ouvrir le tableau de bord, console vide.

**Terminé** quand chaque évaluation retenue est en ligne (ou imprimée, pour le papier),
expliquée et relue, et que la correction publique reprend chaque question du site.

---

## 7. Pour commencer

1. Lis le règlement, la grille de l'épreuve et les contenus du cours.
2. Fais l'inventaire des questions existantes (points de contrôle, quiz, banques).
3. Pose les questions de cadrage, **une à une** (section 3).
4. Écris un lot témoin de questions expliquées, fais-le valider, puis la série.

Sur un cours qui n'a pas été créé depuis le template, les règles de son `CLAUDE.md`
s'appliquent ; à défaut, celles du § 2 du `CLAUDE.md` du template.
