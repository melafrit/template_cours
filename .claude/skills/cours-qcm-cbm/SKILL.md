---
name: cours-qcm-cbm
description: À utiliser pour créer ou modifier le QCM / quiz / banque de questions à notation CBM (Certainty-Based Marking) d'un site template_cours. Couvre la double entrée synchronisée questions.js + corrections.js (énoncé + 4 propositions bilingues, index de bonne réponse, explication), le barème par certitude (Élevée/Moyenne/Faible), la note /20, l'équité des positions et le débiaisage des distracteurs, ainsi que la mise en garde sur la signature SHA-256 des CSV. Mots-clés FR+EN — « QCM », « quiz », « banque de questions », « question à choix multiples », « barème », « CBM », « certitude », « multiple choice », « question bank », « certainty-based marking », « scoring ».
---

# QCM à notation CBM (Certainty-Based Marking)

Ce module pilote le QCM d'évaluation du template : pages Examen / Entraînement,
export CSV signé, page de correction et tableau de bord. La logique est dans
`site/QCM/qcm-core.js` ; **toi tu ne touches qu'aux deux fichiers de données** :
`site/QCM/questions.js` et `site/QCM/corrections.js`.

## 1. Une question = DEUX entrées synchronisées par le même `id`

Chaque question vit en deux endroits, reliés par un `id` identique (ex. `Q13`).
**Toujours éditer les deux ensemble**, sinon la correction casse.

Dans `QCM/questions.js` → tableau `questions` (ce que voit l'apprenant, **sans** réponse) :

```js
{
  id: 'Q13', chapitre: 2, difficulte: 'orange', // vert|jaune|orange|rouge (indicatif)
  enonce: { fr: "Énoncé ?", en: "Statement?" },
  propositions: [                               // 4 propositions PAR CONVENTION
    { fr: "Proposition A", en: "Option A" },
    { fr: "Proposition B", en: "Option B" },
    { fr: "Proposition C", en: "Option C" },
    { fr: "Proposition D", en: "Option D" }
  ]
}
```

Dans `QCM/corrections.js` → tableau `corrections` (clé + explication, chargée à part) :

```js
{
  id: 'Q13', chapitre: 2, difficulte: 'orange',
  bonne_reponse_index: 1,   // 0..3 : index de la bonne proposition dans le tableau ci-dessus
  explication: { fr: "Pourquoi B est correct.", en: "Why B is correct." }
}
```

Règles invariantes :
- **Réponse UNIQUE** par question, **4 propositions** par convention.
- `bonne_reponse_index` ∈ **0..3** et pointe la proposition correcte (0 = A, 3 = D).
- `id`, `chapitre`, `difficulte` doivent être **identiques** dans les deux fichiers.
- **Toutes les chaînes sont bilingues** `{ fr, en }` (énoncé, 4 propositions, explication) :
  voir la skill **cours-bilingue-i18n** pour la convention `{fr,en}` / `TPLI18N`.

## 2. Barème CBM (défini dans `qcm-core.js`, ne pas recoder)

L'apprenant déclare une **certitude** par question. Le barème est **indépendant de la difficulté** :

| Certitude déclarée | Bonne réponse | Mauvaise réponse |
|---|---|---|
| **Élevée** (certain)   | **+3** | **−3** |
| **Moyenne** (assez sûr)| **+2** | **−2** |
| **Faible** (je devine) | **+1** | **0**  |

Toutes les questions ont le **même poids maximal (3)** : pas de pondération par question.

## 3. Note /20 et synchronisation de `meta`

```
note /20 = score_brut ÷ (3 × nombre_de_questions) × 20,  bornée à [0 ; 20]
```

La note se recalcule **toute seule**. Mais après tout ajout/suppression de question,
mets à jour `meta.nombre_questions` dans `questions.js` (cohérence d'affichage) — ce
nombre doit **toujours égaler** la longueur réelle du tableau `questions` et celle de
`corrections`.

## 4. `difficulte` est indicative — elle n'affecte PAS la note

Valeurs : `vert` | `jaune` | `orange` | `rouge` (= Facile / Moyen / Difficile / Expert).
C'est un repère visuel pour l'apprenant ; le score ne dépend que de la **certitude
déclarée**, jamais de la difficulté affichée. Ne t'en sers donc jamais comme pondération.

## 5. Qualité de rédaction (équité anti-biais)

Issu de `prompts/07_qcm_banque.md` — à respecter pour une banque équitable :

- **Positions équilibrées** : répartis la bonne réponse ~également entre A/B/C/D
  (cible ~25 % chacune). Pas de motif prévisible (ni `A,B,C,D,A,B…`, ni longue série
  identique). Repère existant : `corrections.js` documente l'équilibre des index en tête.
- **Distracteurs plausibles** : erreurs réelles / confusions courantes, jamais d'option
  absurde. Longueur **comparable** entre les 4 propositions (la bonne réponse ne doit
  pas être systématiquement la plus longue ou la plus courte).
- **Pas de béquilles** : interdits « Toutes les réponses ci-dessus » / « Aucune des
  réponses ». Pas d'indice grammatical (accord, article, ponctuation) ni de mot de
  l'énoncé répété uniquement dans la bonne réponse.
- **Bilingue strict** : versions FR et EN équivalentes (même bonne réponse, même ordre
  A/B/C/D, même sens). Explications formatives : pourquoi la bonne réponse, et brièvement
  pourquoi chaque distracteur est faux.

## 6. ⚠️ Mise en garde SIGNATURE (figer la banque pendant un examen)

Le **nombre** et l'**ordre** des questions entrent dans la **signature SHA-256
autonome** des CSV exportés (calculée dans `qcm-core.js`). Modifier la banque (ajout,
suppression, réordonnancement) **invalide les CSV produits avec l'ancienne version** :
ils ne se vérifieront plus à la correction. **Fige la banque pendant toute la durée
d'une session d'examen** ; ne fais évoluer les questions qu'entre deux sessions.

## Pour aller plus loin

- `docs/ARCHITECTURE.md` §4.3 — recette complète « ajouter une question » + table CBM + caveat signature.
- `prompts/07_qcm_banque.md` — règles de conception détaillées (réponse unique, équilibre des positions, débiaisage, auto-vérification) et `prompts/08_qcm_papier.md` pour la version papier.
- Skill **cours-bilingue-i18n** — convention bilingue `{fr,en}` et `TPLI18N` (obligatoire pour toute chaîne).

> Template de site de cours — **Mohamed EL AFRIT** · code MIT, contenu & prompts CC BY 4.0.
