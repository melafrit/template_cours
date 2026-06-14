# Prompt 08 — QCM papier imprimable (DOCX)

**Quand l'utiliser**
Après avoir validé la banque de questions du QCM (prompt de génération du QCM web).
Ce prompt produit la **version papier imprimable** du même QCM, en **trois fichiers DOCX noir & blanc, compacts** :

1. **`QCM_questions.docx`** — page de garde + consignes + barème CBM **avec exemples chiffrés** + les questions en **2 colonnes** ;
2. **`QCM_grille_reponses.docx`** — la **grille de réponses** (réponse unique A/B/C/D + certitude F/M/É), seul document ramassé ;
3. **`QCM_corrige.docx`** — le **corrigé formateur** (bonne réponse + explication, regroupé par chapitre).

Le tout est généré par un script Python (`tools/generate_qcm_papier.py`, basé sur **python-docx**) à partir d'un fichier de données JSON unique. Le prompt demande à Claude **d'extraire/convertir la banque QCM existante en JSON**, puis **d'écrire le script** et de documenter la commande à lancer.

---

## Placeholders à compléter

- `{{SUJET_DU_COURS}}` — ex. « Réglementation des données et conformité »
- `{{PUBLIC_CIBLE}}` — ex. « étudiants de Master EADL, Bloc 2 »
- `{{NIVEAU}}` — ex. « Master 1 / 2 »
- `{{LANGUES}}` — `français seul` **ou** `français + anglais` (voir note bilingue plus bas)
- `{{NB_QUESTIONS}}` — nombre total de questions (ex. `60`). Idéalement **divisible par 3** pour une grille en 3 blocs équilibrés.
- `{{DUREE_EPREUVE}}` — ex. « 1 h 30 »
- `{{SOUS_TITRE}}` — bandeau institutionnel, ex. « Master EADL — Bloc 2 · 2025-2026 »
- `{{ANNEE}}` — millésime affiché dans les champs de date, ex. `2026`
- `{{BANQUE_QCM}}` — **source des questions** : chemin du fichier de questions du QCM web (ex. `QCM/questions.js` ou `QCM/questions.json`), OU le contenu collé. C'est la **référence d'exactitude** : ne rien réécrire, ne rien réinventer.
- `{{DOCUMENTS_DE_REFERENCE}}` — supports de cours sur lesquels s'appuient les explications du corrigé (pour vérification, **pas** pour inventer du contenu).
- `{{REPERTOIRE_SORTIE}}` — où écrire les fichiers (ex. `QCM/version_papier/`). Par défaut `tools/` est le script, la sortie va dans ce répertoire.
- `{{AUTEUR}}` — ex. « Mohamed EL AFRIT »
- `{{LICENCE}}` — ex. « CC BY-NC-SA 4.0 » (apparaît en pied de page de chaque DOCX)
- `{{CONTRAINTES}}` — ex. « tout en noir & blanc, impression recto-verso, pas plus de N pages, aucune ressource autorisée pendant l'épreuve »

---

## PROMPT À COPIER

> Copiez tout le bloc ci-dessous dans Claude. Remplacez les `{{...}}` au préalable.

```text
Tu es un ingénieur pédagogique et développeur Python. Tu dois produire la VERSION PAPIER IMPRIMABLE d'un QCM existant, sous forme de trois fichiers Word (.docx) en noir & blanc, compacts, et le script Python qui les génère.

CONTEXTE
- Cours : {{SUJET_DU_COURS}}
- Public : {{PUBLIC_CIBLE}} (niveau {{NIVEAU}})
- Sous-titre / bandeau : {{SOUS_TITRE}}
- Épreuve : {{NB_QUESTIONS}} questions à réponse UNIQUE, durée {{DUREE_EPREUVE}}, année {{ANNEE}}
- Langue des documents : {{LANGUES}}
- Auteur : {{AUTEUR}} — Licence : {{LICENCE}}
- Contraintes : {{CONTRAINTES}}

EXIGENCE D'EXACTITUDE (impératif, à respecter avant toute génération)
1. La banque de questions est la SEULE source autorisée : {{BANQUE_QCM}}.
   Analyse-la EN DÉTAIL avant de produire quoi que ce soit. Ne réécris pas les énoncés, ne modifie pas les propositions, ne change pas la bonne réponse. N'invente aucune question.
2. Vérifie l'intégrité de la banque AVANT de générer et signale (sans corriger silencieusement) tout problème :
   - chaque question a exactement 4 propositions (A, B, C, D) et UNE seule bonne réponse ;
   - les positions des bonnes réponses sont raisonnablement équilibrées (≈ 25 % par lettre) ; signale tout déséquilibre marqué ;
   - la bonne réponse n'est pas systématiquement la proposition la plus longue (distracteurs débiaisés) ; signale les cas suspects ;
   - aucune proposition n'est tronquée, dupliquée, ni vide.
   Présente d'abord un court rapport de contrôle (compte par lettre, anomalies). Demande validation si tu détectes un problème bloquant, sinon poursuis.
3. Les explications du corrigé doivent être exactes et fondées sur : {{DOCUMENTS_DE_REFERENCE}}. Si la banque fournit déjà une explication par question, reprends-la fidèlement ; ne l'enrichis que si c'est exact et utile, sans inventer de référence juridique ou factuelle. En cas de doute, reste sobre.

ÉTAPE 1 — DONNÉES : produire un JSON unique `qcm_content.json`
À partir de {{BANQUE_QCM}}, génère un fichier JSON (UTF-8) qui est un tableau d'objets, un par question, dans l'ordre, au schéma EXACT suivant :
[
  {
    "n": 1,                      // numéro d'ordre (1..{{NB_QUESTIONS}})
    "id": "Q01",                 // identifiant stable
    "chapitre": 1,               // numéro de chapitre (pour le regroupement du corrigé)
    "difficulte": "vert",        // indicatif seulement : vert | orange | rouge (n'influence PAS le barème)
    "enonce": "…",               // texte de la question
    "propositions": ["A…","B…","C…","D…"],   // exactement 4, dans l'ordre d'affichage
    "bonne_index": 0,            // index 0..3 de la bonne proposition
    "explication": "…"           // justification courte pour le corrigé formateur
  }
]
Règles : `bonne_index` est un ENTIER 0..3 (0=A, 1=B, 2=C, 3=D). Échappe correctement les caractères. Ne mets aucune clé hors schéma. Le nombre d'objets doit être exactement {{NB_QUESTIONS}}.

ÉTAPE 2 — SCRIPT : `tools/generate_qcm_papier.py` (python-docx)
Écris un script Python autonome, commenté, qui lit `qcm_content.json` (situé à côté de lui ou dans {{REPERTOIRE_SORTIE}}) et écrit TROIS .docx dans {{REPERTOIRE_SORTIE}} :

A) `QCM_questions.docx`
   - PAGE DE GARDE : intitulé « QCM — ÉPREUVE INDIVIDUELLE », titre du cours, sous-titre + durée + nombre de questions, et une ligne de champs « NOM : ___  PRÉNOM : ___  DATE : __/__/{{ANNEE}} ».
   - CONSIGNES (puces concises) : épreuve individuelle, aucune ressource autorisée (ni Internet, ni IA) ; {{NB_QUESTIONS}} questions à réponse unique ; reporter les réponses sur la GRILLE (seul document ramassé) ; à défaut de certitude indiquée → certitude « Faible » appliquée.
   - BARÈME CBM (Certainty-Based Marking) présenté en TABLEAU :
       Certitude Élevée  → bonne +3 / mauvaise −3
       Certitude Moyenne → bonne +2 / mauvaise −2
       Certitude Faible  → bonne +1 / mauvaise  0
     Formule affichée en gras : « Note /20 = score brut ÷ (3 × {{NB_QUESTIONS}}) × 20 » avec la mention « maximum = 3 × {{NB_QUESTIONS}} ; une note négative est ramenée à 0 ». La difficulté (vert/orange/rouge) est INDICATIVE et n'entre PAS dans le calcul.
   - EXEMPLES CHIFFRÉS (obligatoire) :
       • Bonne réponse en Élevée → +3 ; la même réponse fausse → −3.
       • Bonne en Moyenne → +2 ; fausse → −2.  Bonne en Faible → +1 ; fausse → 0 (aucune pénalité quand on assume un pari).
       • Un MINI-TABLEAU « Exemple de calcul sur 3 questions » : Q1 correcte/Élevée → +3 ; Q2 incorrecte/Moyenne → −2 ; Q3 correcte/Faible → +1 ; Total = +2.
       • Une phrase d'illustration sur l'ensemble : un score brut donné → brut ÷ (3 × {{NB_QUESTIONS}}) × 20 = note /20 (montre le calcul avec un exemple cohérent).
       • Une consigne de stratégie honnête en gras : « Faible si vous devinez, Moyenne si assez sûr, Élevée seulement si vraiment certain — une Élevée erronée coûte −3. »
   - QUESTIONS sur une nouvelle section EN 2 COLONNES : numéro + énoncé en gras léger, puis les 4 propositions « A. / B. / C. / D. » légèrement indentées. Garde l'énoncé solidaire de ses propositions (keep_with_next) pour éviter les coupures laides.
   - PIED DE PAGE : « {{SUJET_DU_COURS}} — QCM — {{AUTEUR}} — {{LICENCE}} ».

B) `QCM_grille_reponses.docx` (seul document ramassé)
   - Bandeau titre (cours + sous-titre) et « QCM — Grille de réponses ».
   - Champs NOM / PRÉNOM / DATE (__/__/{{ANNEE}}).
   - Consignes condensées : réponse UNIQUE (noircir un seul cercle A/B/C/D) ; certitude un seul cercle ○ : F = Faible · M = Moyenne · É = Élevée (à défaut : Faible) ; rappel du barème + formule /20.
   - GRILLE : un grand tableau en 3 blocs côte à côte (si {{NB_QUESTIONS}} est divisible par 3 ; sinon répartis au plus équilibré). Chaque bloc a les colonnes : « N° | A B C D | F M É ». Le corps contient des cercles « ○ » à noircir ; en-têtes grisés, colonnes de certitude légèrement teintées pour les distinguer. Cellules serrées (marges réduites) pour tenir sur une page.
   - PIED DE PAGE : « … — Grille QCM — {{AUTEUR}} — {{LICENCE}} ».

C) `QCM_corrige.docx` (réservé au formateur)
   - En-tête « CORRIGÉ — réservé au formateur », titre + sous-titre, rappel du barème CBM et de la formule /20.
   - Questions REGROUPÉES PAR CHAPITRE (titre « Chapitre N »), dans l'ordre. Pour chaque question : numéro + énoncé, puis « Réponse : <lettre> — <texte de la bonne proposition> » en gras, puis « Explication. <texte> ».
   - PIED DE PAGE : « … — Corrigé QCM (formateur) — {{AUTEUR}} — {{LICENCE}} ».

CONTRAINTES TECHNIQUES (toutes obligatoires)
- Bibliothèque : python-docx uniquement (pas de Word, pas de LibreOffice requis à l'exécution).
- 100 % NOIR & BLANC : aucune couleur, uniquement des gris de remplissage de cellules (ex. en-têtes gris clair) ; pensez « photocopie ».
- COMPACT : marges étroites (≈ 12–13 mm), interligne serré, polices petites (énoncés ≈ 9 pt, propositions ≈ 8,5 pt, pieds de page ≈ 7,5 pt) ; objectif : le moins de pages possible. Respecte {{CONTRAINTES}}.
- Tableaux à LARGEURS FIXES (table layout = fixed, largeurs de colonnes explicites) pour que la grille ne se déforme pas.
- Police par défaut sans empattement lisible (ex. Calibri). Encodage UTF-8 ; gère les accents et caractères spéciaux (« É », « ○ », « − » comme signe moins typographique).
- Chemins construits avec os.path par rapport à l'emplacement du script (robuste quel que soit le répertoire d'appel). Le script écrit dans {{REPERTOIRE_SORTIE}}.
- À la fin, `main()` appelle les trois fonctions de construction et imprime, pour chaque fichier, « OK <nom> <taille> o ».
- Le script doit être idempotent (réexécutable, écrase proprement les sorties) et ne RIEN télécharger.

ÉTAPE 3 — OPTIONS / CLI (souhaitable)
Ajoute un parseur d'arguments (argparse) avec, au minimum :
  --data PATH         chemin du qcm_content.json (défaut : à côté du script)
  --out  DIR          répertoire de sortie (défaut : {{REPERTOIRE_SORTIE}})
  --only {questions,grille,corrige}   (répétable) pour ne générer qu'un sous-ensemble
  --titre / --sous-titre / --duree / --annee   pour surcharger les libellés sans toucher au code
  --blocs N           nombre de blocs de la grille (défaut : 3 si divisible, sinon ajuste)
Documente chaque option dans l'aide (--help) et dans un court bloc de commentaires en tête de fichier.

LIVRABLES ATTENDUS (dans l'ordre)
1. Le rapport de contrôle d'intégrité de la banque (compte des bonnes réponses par lettre + anomalies).
2. Le fichier `qcm_content.json` complet ({{NB_QUESTIONS}} objets, schéma exact).
3. Le script `tools/generate_qcm_papier.py` complet.
4. La COMMANDE exacte à lancer et les dépendances à installer.
5. Une checklist de RELECTURE AVANT IMPRESSION (voir ci-dessous).

COMMANDE (à inclure dans ta réponse, adaptée à {{REPERTOIRE_SORTIE}})
  python -m pip install python-docx
  python tools/generate_qcm_papier.py
  # ou ciblé :
  python tools/generate_qcm_papier.py --only grille --out {{REPERTOIRE_SORTIE}}

CHECKLIST RELECTURE AVANT IMPRESSION (génère-la, prête à cocher)
  [ ] Le nombre de questions imprimées = {{NB_QUESTIONS}}.
  [ ] La grille a autant de lignes que de questions, numérotées sans trou.
  [ ] Le barème affiché = Élevée +3/−3 · Moyenne +2/−2 · Faible +1/0, formule /20 correcte.
  [ ] L'exemple chiffré « 3 questions » donne bien le total annoncé.
  [ ] Tout est en noir & blanc, lisible en photocopie, et tient dans le nombre de pages visé.
  [ ] Aucun énoncé ni proposition n'est coupé en bas de colonne de façon illisible.
  [ ] Le corrigé n'est PAS distribué aux étudiants (fichier séparé, mention « réservé au formateur »).

{{LANGUES}} — SI « français + anglais »
Produis DEUX jeux de fichiers : suffixe `_fr` et `_en` (ex. `QCM_questions_fr.docx` / `QCM_questions_en.docx`). Tous les libellés d'interface (consignes, barème, en-têtes de grille, « Réponse », « Explication », pieds de page) doivent exister dans les deux langues via un petit dictionnaire i18n dans le script ; les énoncés et propositions proviennent des champs traduits de la banque {{BANQUE_QCM}} (n'invente AUCUNE traduction : si une traduction manque, signale-le au lieu de la fabriquer). Ajoute une option CLI `--lang {fr,en,both}` (défaut : both si {{LANGUES}} = français + anglais, sinon fr).
```

---

## Conseils

- **Vérifie l'intégrité d'abord.** Exige le rapport de contrôle (répartition des bonnes réponses par lettre, propositions tronquées, bonne réponse trop souvent la plus longue) **avant** de générer : c'est le moment le moins coûteux pour corriger la banque.
- **Garde une seule source de vérité.** Le JSON `qcm_content.json` est dérivé de la banque du QCM web. Quand tu modifies une question, modifie la banque puis **régénère** le JSON et les DOCX — ne corrige jamais un DOCX à la main.
- **Nombre de questions divisible par 3** = grille en 3 blocs propres sur une page. Sinon, ajuste `--blocs` et vérifie l'équilibre.
- **PDF pour l'impression finale.** python-docx ne produit pas de PDF. Pour figer la mise en page, exporte les `.docx` en PDF (Word « Enregistrer sous », ou `libreoffice --headless --convert-to pdf *.docx`). Les versions de référence du dépôt sont les PDF.
- **Le signe moins.** Utilise le vrai signe « − » (U+2212), pas le trait d'union, pour que « −3 » reste lisible et homogène.
- **Diffusion.** Distribue uniquement `QCM_questions` + `QCM_grille_reponses` aux étudiants ; garde `QCM_corrige` côté formateur.
- **Cohérence avec le QCM web.** Le barème CBM, la formule /20 et l'équilibrage des réponses doivent être **identiques** à ceux du QCM en ligne : l'étudiant doit retrouver les mêmes règles sur papier et à l'écran.
