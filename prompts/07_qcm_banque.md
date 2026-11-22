# Banque de QCM (CBM)

> **Quand l'utiliser** : pour générer la banque de questions du QCM d'évaluation d'un chapitre (ou d'un cours entier) avec notation **CBM** (Certainty-Based Marking). À lancer **après** avoir rédigé le contenu du ou des chapitres concernés, afin que les questions collent exactement à ce qui a été enseigné. Le résultat alimente directement le moteur de QCM du template (modes Examen / Entraînement, export CSV signé, page de correction, tableau de bord).

---

## Placeholders à compléter

- `{{SUJET_DU_COURS}}` : intitulé du cours (ex. « Réglementation des données »).
- `{{CHAPITRE_CIBLE}}` : chapitre(s) ou périmètre couvert(s) par cette banque (ex. « Chapitre 3 · Bases légales du traitement » ou « Tout le cours »).
- `{{PUBLIC_CIBLE}}` : à qui s'adresse le cours (ex. « étudiants Master 1, juristes en formation »).
- `{{NIVEAU}}` : débutant / intermédiaire / avancé.
- `{{NB_QUESTIONS}}` : nombre total de questions à produire (ex. 30).
- `{{LANGUES}}` : `français seul` **OU** `français + anglais`.
- `{{DOCUMENTS_DE_REFERENCE}}` : contenus de chapitre, polycopiés, textes officiels, glossaire… sur lesquels s'appuyer **exclusivement**.
- `{{FIL_ROUGE}}` : scénario continu du cours (ex. « une coopérative agricole fictive qui numérise ses ventes »), pour ancrer certaines questions dans un cas concret.
- `{{REPARTITION_DIFFICULTE}}` : répartition visée (ex. « ~40 % faciles, ~40 % moyennes, ~20 % difficiles »).
- `{{AUTEUR}}` : auteur du cours.
- `{{LICENCE}}` : licence du contenu (ex. « CC BY 4.0 »).
- `{{CONTRAINTES}}` : contraintes spécifiques (terminologie imposée, points à ne pas traiter, nombre de propositions, etc.).

---

## PROMPT À COPIER

```text
RÔLE
Tu es concepteur d'évaluations pédagogiques, spécialiste de l'évaluation par certitude (Certainty-Based Marking, CBM) et de la psychométrie des QCM. Tu produis des banques de questions équitables, exemptes de biais de réponse, parfaitement alignées sur le contenu enseigné.

MISSION
Générer une banque de {{NB_QUESTIONS}} questions à réponse UNIQUE pour le QCM du cours « {{SUJET_DU_COURS}} », périmètre : {{CHAPITRE_CIBLE}}.
Public : {{PUBLIC_CIBLE}}. Niveau : {{NIVEAU}}. Langues : {{LANGUES}}.

EXIGENCE D'EXACTITUDE (NON NÉGOCIABLE)
1. Analyse EN DÉTAIL les documents de référence ci-dessous AVANT de rédiger la moindre question.
2. N'invente RIEN : chaque bonne réponse et chaque explication doivent être justifiables par les documents. Aucune connaissance externe non sourcée.
3. Pour chaque question, indique la source interne (titre de section, page, ou ancre du chapitre) d'où provient la bonne réponse.
4. Si une notion est ambiguë ou absente des documents, NE crée PAS de question dessus : signale-la dans la section « Points à clarifier » plutôt que de combler par une supposition.

DOCUMENTS DE RÉFÉRENCE
{{DOCUMENTS_DE_REFERENCE}}

CONTEXTE ET FIL ROUGE
Ancre une partie des questions (≈ 1 sur 4) dans le scénario fil rouge suivant, pour évaluer l'application concrète et non seulement la mémorisation : {{FIL_ROUGE}}.
Contraintes supplémentaires : {{CONTRAINTES}}.

================================================================
RÈGLES DE CONCEPTION (CBM + ÉQUITÉ) : À RESPECTER STRICTEMENT
================================================================

A. FORMAT DES QUESTIONS
- Réponse UNIQUE : exactement 4 propositions (A, B, C, D), dont UNE SEULE correcte, sauf indication contraire dans {{CONTRAINTES}}.
- Énoncé clair, autoportant, sans double négation, sans « Toutes les réponses ci-dessus » ni « Aucune des réponses ».
- Une seule idée évaluée par question. Pas de question piège purement lexicale.
- Couvre l'ensemble du périmètre {{CHAPITRE_CIBLE}} : répartis les questions sur les différentes sections, sans surreprésenter un point mineur.
- Typographie des énoncés, des propositions et des explications, en français comme en anglais : ni tiret cadratin ni tiret moyen entre espaces (une incise passe entre virgules ou entre parenthèses) ; en français, une espace insécable avant « : ; ? ! » et à l'intérieur des guillemets « ». Évite aussi les marques de texte généré (plus d'un deux-points par phrase, phrase-choc sans verbe, antithèse réflexe, mot gonflé).

B. NIVEAUX COGNITIFS
- Mélange les niveaux : mémorisation (définitions), compréhension, et APPLICATION (mise en situation, souvent via le fil rouge).
- Vise au moins un tiers de questions d'application/analyse, pas seulement du par-cœur.

C. DIFFICULTÉ (INDICATIVE SEULEMENT, elle n'affecte PAS le barème)
- Attribue à chaque question un indice de difficulté, la couleur qu'emploie le moteur du QCM : « vert » (facile), « jaune » (moyen), « orange » (difficile) ou « rouge » (expert).
- Respecte au mieux la répartition visée : {{REPARTITION_DIFFICULTE}}.
- Rappelle dans la sortie que cet indice est purement indicatif : en CBM, le score dépend de la certitude déclarée, pas de la difficulté affichée.

D. ÉQUITÉ DES POSITIONS DE BONNES RÉPONSES (CONTRAINTE FORTE)
- Répartis les bonnes réponses ~également entre A, B, C et D (cible : ~25 % chacune).
- Écart maximal toléré entre la position la plus fréquente et la moins fréquente : 1 occurrence quand {{NB_QUESTIONS}} n'est pas multiple de 4, sinon répartition exactement égale.
- N'utilise JAMAIS de motif régulier prévisible (pas de A,B,C,D,A,B,C,D… ni de longue série identique). Mélange l'ordre.

E. DÉBIAISAGE DES DISTRACTEURS (CONTRAINTE FORTE)
- Les 3 distracteurs doivent être PLAUSIBLES : erreurs réelles, confusions courantes, demi-vérités. N'écris jamais d'option absurde ou manifestement hors-sujet.
- LONGUEUR comparable : la bonne réponse ne doit JAMAIS être systématiquement la plus longue ni la plus détaillée. Égalise le nombre de mots des 4 propositions (écart max ~25 %). La bonne réponse doit être tantôt la plus courte, tantôt la plus longue, tantôt au milieu, sans corrélation avec la justesse.
- Pas d'indice grammatical : accord (genre/nombre), article (« un/une », « a/an »), ponctuation et style identiques pour les 4 options, afin qu'aucune ne « sonne » plus correcte.
- Pas de recouvrement : les 4 options doivent être mutuellement exclusives ; pas deux options synonymes.
- Pas de mot de l'énoncé répété uniquement dans la bonne réponse (évite l'« indice par appariement de mots »).

F. BARÈME CBM (À RAPPELER DANS LA SORTIE, NE PAS RECALCULER PAR QUESTION)
- L'étudiant déclare sa certitude pour chaque question :
  • Élevée  → +3 si correct, −3 si faux
  • Moyenne → +2 si correct, −2 si faux
  • Faible  → +1 si correct,  0 si faux
- Note finale /20 = score_brut ÷ (3 × nombre_de_questions) × 20 ; une note négative est ramenée à 0.
- Le concepteur n'a donc PAS à pondérer les questions : toutes ont le même poids maximal (3). La difficulté n'entre pas dans le calcul.

{{#SI LANGUES = français + anglais}}
G. BILINGUE FR/EN
- Fournis CHAQUE question intégralement en français ET en anglais : énoncé, 4 propositions, explication.
- Les deux versions doivent être strictement équivalentes (même bonne réponse, même ordre A/B/C/D, même sens). Traduction professionnelle, pas littérale.
{{/SI}}

================================================================
STRUCTURE DE DONNÉES À PRODUIRE (FORMAT ATTENDU PAR LE TEMPLATE)
================================================================

Produis DEUX blocs JSON SÉPARÉS, pour que le QCM puisse être affiché sans révéler les réponses, et la correction chargée à part :

1) BLOC « questions » (sans réponses ni explications), ce que voit l'étudiant. Il va dans le tableau questions de site/QCM/questions.js :

[
  {
    "id": "Q01",
    "chapitre": 1,
    "difficulte": "vert|jaune|orange|rouge",
    "enonce": { "fr": "…."{{#SI EN}}, "en": "…."{{/SI}} },
    "propositions": [
      { "fr": "…."{{#SI EN}}, "en": "…."{{/SI}} },
      { "fr": "…."{{#SI EN}}, "en": "…."{{/SI}} },
      { "fr": "…."{{#SI EN}}, "en": "…."{{/SI}} },
      { "fr": "…."{{#SI EN}}, "en": "…."{{/SI}} }
    ]
  }
]

2) BLOC « corrections » (clés alignées sur les "id"), chargé séparément. Il va dans le tableau corrections de site/QCM/corrections.js :

[
  {
    "id": "Q01",
    "chapitre": 1,
    "difficulte": "vert|jaune|orange|rouge",
    "bonne_reponse_index": 0,
    "source": "<référence interne précise>",
    "explication": {
      "fr": "Pourquoi cette réponse est correcte ET pourquoi chacun des 3 distracteurs est faux (1 phrase par distracteur), puis les renvois « Pour approfondir »."{{#SI EN}},
      "en": "…"{{/SI}}
    }
  }
]

Les champs "id", "chapitre" et "difficulte" sont identiques dans les deux blocs. "bonne_reponse_index" est un entier, l'index de la bonne proposition : 0 = A, 1 = B, 2 = C, 3 = D. Les pages du QCM ne lisent pas "source", qui sert à la relecture.

Règles sur les explications : pédagogiques, bienveillantes, orientées « pourquoi ». Elles expliquent la bonne réponse ET réfutent brièvement chaque distracteur, pour que la correction soit formative. Elles finissent par deux à quatre renvois « Pour approfondir », vers l'endroit exact du cours (chapitre, section) ou vers une référence externe vérifiée (prompts/15_explications_quiz.md). Ces renvois s'écrivent en prose : les pages du QCM affichent l'explication en texte brut, sans lien.

================================================================
AUTO-VÉRIFICATION OBLIGATOIRE (à effectuer AVANT de rendre la sortie)
================================================================
Après avoir rédigé les {{NB_QUESTIONS}} questions, VÉRIFIE et corrige si besoin, puis produis un « Rapport d'équilibre » :

1. Comptage des positions : nombre de bonnes réponses en A / B / C / D, et pourcentage. Confirme que l'écart respecte la règle D ; sinon, REDISTRIBUE en réordonnant des options (et mets à jour les corrections) jusqu'à conformité.
2. Test de longueur : pour CHAQUE question, indique la longueur (en mots) des 4 options et signale tout cas où la bonne réponse serait la plus longue. Corrige les cas problématiques. Donne le pourcentage de questions où la bonne réponse est la plus longue (doit rester proche de 25 %, jamais ≥ 50 %).
3. Vérif. d'unicité : confirme qu'aucune question n'a 0 ou ≥ 2 réponses correctes.
4. Vérif. anti-indice : confirme l'absence de biais grammatical et de répétition de mots de l'énoncé dans la seule bonne réponse.
5. Répartition de difficulté : compare le réalisé à {{REPARTITION_DIFFICULTE}}.
6. Couverture : liste les sections de {{CHAPITRE_CIBLE}} effectivement couvertes.
{{#SI EN}}7. Parité FR/EN : confirme que chaque question existe dans les deux langues avec la même bonne réponse.{{/SI}}

Si une vérification échoue, CORRIGE avant de livrer : ne livre jamais une banque non conforme.

================================================================
SORTIE FINALE (dans cet ordre)
================================================================
1. Rappel d'1 ligne du barème CBM et de la formule de note /20.
2. BLOC JSON « questions ».
3. BLOC JSON « corrections ».
4. Rapport d'équilibre (points 1 à 7 ci-dessus, en clair).
5. Section « Points à clarifier » : notions ambiguës ou absentes des documents, questions écartées et pourquoi.

Méta-données à inclure en tête : cours « {{SUJET_DU_COURS}} », périmètre {{CHAPITRE_CIBLE}}, auteur {{AUTEUR}}, licence {{LICENCE}}.
N'utilise aucune connaissance non présente dans les documents de référence. Cite tes sources internes pour chaque bonne réponse.
```

---

## Conseils

- **Lance ce prompt chapitre par chapitre** plutôt que sur tout le cours d'un coup : les questions sont plus précises et l'auto-vérification de l'équilibre reste fiable. Tu peux ensuite concaténer les banques.
- **Vérifie le rapport d'équilibre** : c'est le garde-fou anti-biais. Si la part de questions où « la bonne réponse est la plus longue » dépasse ~25 %, ou si une position (A/B/C/D) est sur-représentée, redemande une passe de correction ciblée.
- **Sépare bien les deux blocs JSON** lors de l'intégration : le bloc `questions` ne doit contenir aucune réponse, le bloc `corrections` est chargé par les pages Entraînement, Correction et Tableau de bord. C'est ce qui permet l'export CSV signé en SHA-256 et la correction hors-ligne.
- **Pour 30 questions, vise ~25 % par position** (idéalement 7/8/8/7). Au-delà de 40 questions, scinde en deux séries pour garder une relecture humaine raisonnable.
- **Demande une seconde passe « adversariale »** : « Pour chaque question, un étudiant pourrait-il deviner la bonne réponse sans connaître le cours (longueur, grammaire, mot répété, option la plus prudente) ? Corrige les cas trouvés. » C'est le test le plus efficace contre les biais résiduels.
- **Garde la difficulté indicative** : ne l'utilise jamais comme pondération. En CBM, c'est la certitude déclarée par l'étudiant qui module le score, pas le concepteur.
