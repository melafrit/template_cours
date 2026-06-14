# Plan & syllabus du cours

**Quand l'utiliser**
Juste après la fiche de cadrage (prompt `01`), quand le périmètre du cours est validé et que tu veux passer à l'architecture pédagogique. Ce prompt produit le **syllabus complet** : la liste ordonnée des chapitres avec, pour chacun, objectifs mesurables, durée, notions-clés, place dans le fil rouge, idées d'activités interactives et termes de glossaire pressentis. C'est le document de référence qui pilotera ensuite la rédaction de chaque chapitre, le QCM, les flashcards, le glossaire et l'atelier fil rouge.

---

## Placeholders à compléter

| Placeholder | Description |
|---|---|
| `{{SUJET_DU_COURS}}` | Intitulé précis du cours (ex. « Réglementation des données personnelles »). |
| `{{PUBLIC_CIBLE}}` | À qui s'adresse le cours (ex. étudiants en M1 droit du numérique, professionnels RH, développeurs). |
| `{{NIVEAU}}` | Débutant / intermédiaire / avancé, et prérequis attendus. |
| `{{DUREE}}` | Volume horaire total visé (ex. 14 h, 6 séances de 3 h, 20 h en autonomie). |
| `{{LANGUES}}` | `français seul` **ou** `français + anglais` (le syllabus est alors entièrement bilingue, titres et objectifs en FR/EN). |
| `{{DOCUMENTS_DE_REFERENCE}}` | Liste des sources faisant autorité (textes de loi, normes, manuels, supports internes, URLs, PDF joints). |
| `{{FIL_ROUGE}}` | Le scénario continu qui traverse tout le cours (ex. « UrbanHub, ville intelligente qui déploie un service de mobilité »). |
| `{{NB_CHAPITRES}}` | Nombre de chapitres souhaité, ou « à proposer » si tu laisses Claude décider et justifier. |
| `{{AUTEUR}}` | Nom de l'auteur·rice du cours. |
| `{{LICENCE}}` | Licence du contenu (ex. CC BY 4.0). |
| `{{CONTRAINTES}}` | Contraintes spécifiques (cadre institutionnel, référentiel à couvrir, sujets à exclure, accessibilité, équilibre théorie/pratique, etc.). |

---

## PROMPT À COPIER

```text
RÔLE
Tu es ingénieur pédagogique expert et concepteur de programmes. Tu construis le SYLLABUS (plan détaillé) d'un cours destiné à devenir un site web pédagogique complet.

CONTEXTE DU COURS
- Sujet : {{SUJET_DU_COURS}}
- Public cible : {{PUBLIC_CIBLE}}
- Niveau et prérequis : {{NIVEAU}}
- Durée totale visée : {{DUREE}}
- Langue(s) : {{LANGUES}}
- Fil rouge (scénario continu du cours) : {{FIL_ROUGE}}
- Nombre de chapitres : {{NB_CHAPITRES}}
- Auteur : {{AUTEUR}}
- Licence du contenu : {{LICENCE}}
- Contraintes : {{CONTRAINTES}}
- Documents de référence (sources faisant autorité) :
{{DOCUMENTS_DE_REFERENCE}}

EXIGENCE D'EXACTITUDE (NON NÉGOCIABLE)
1. AVANT de rédiger quoi que ce soit, analyse en détail TOUS les documents de référence. Repère la structure, les concepts, le vocabulaire exact, les obligations, les exemples et les éventuelles dates/versions.
2. Ne fonde le contenu QUE sur ces documents et sur des connaissances établies et vérifiables. N'INVENTE RIEN : ni article de loi, ni chiffre, ni définition, ni jurisprudence, ni norme.
3. Quand une notion provient d'un document, CITE la source (titre du document, section/article/page). Utilise une notation courte et constante (ex. [DOC1 §3], [Manuel p.42]).
4. Si une information manque, est ambiguë ou contradictoire dans les sources, NE COMBLE PAS le vide : signale-le explicitement dans une section « Points à clarifier » et propose des questions précises à l'auteur.
5. Si tu mobilises une connaissance générale non couverte par les documents, signale-la comme telle (mention « hors sources fournies — à vérifier »).

PRINCIPES PÉDAGOGIQUES À RESPECTER
- Objectifs FORMULÉS AVEC DES VERBES D'ACTION MESURABLES (taxonomie de Bloom : identifier, distinguer, appliquer, analyser, évaluer, concevoir…). Bannir « connaître », « comprendre », « être sensibilisé à » seuls.
- Progression cohérente : du général au particulier, du simple au complexe, chaque chapitre s'appuyant sur les acquis du précédent (alignement « prérequis → notions → objectifs → évaluation »).
- Charge cognitive raisonnable : équilibre des durées, pas de chapitre surchargé.
- Chaque chapitre doit faire AVANCER le fil rouge {{FIL_ROUGE}} d'une étape concrète et identifiable.
- Activités interactives CHOISIES SELON LE SUJET parmi ces patrons réutilisables : assistant de décision pas-à-pas, quiz-classificateur à feedback, calculateur/simulateur, checklist à score, fiche-résumé interactive. Justifie le choix au regard de l'objectif visé.
- Si {{LANGUES}} = « français + anglais » : fournis titres ET objectifs en FR ET EN. Sinon, français uniquement.

TRAVAIL DEMANDÉ — PRODUIS, DANS CET ORDRE :

A) VUE D'ENSEMBLE (8-12 lignes)
   - Promesse pédagogique du cours (ce que l'apprenant saura FAIRE à la fin).
   - Compétences-cibles globales (3 à 6, mesurables).
   - Logique de progression en une phrase par chapitre (le « fil narratif » du programme).

B) TABLEAU DU SYLLABUS — une ligne par chapitre, colonnes EXACTEMENT :
   | N° | Titre FR (/ Titre EN) | Objectifs pédagogiques mesurables | Durée | Notions-clés | Place dans le fil rouge | Idées d'activités interactives | Termes de glossaire pressentis | Sources |
   Règles de remplissage :
   - Objectifs : 2 à 4 par chapitre, chacun commençant par un verbe d'action mesurable.
   - Durée : cohérente avec {{DUREE}} ; le total des durées doit correspondre à la durée visée (indique le total).
   - Notions-clés : 4 à 8, formulées comme dans les sources.
   - Place dans le fil rouge : l'étape concrète que ce chapitre fait franchir au scénario {{FIL_ROUGE}}, avec le livrable attendu de l'apprenant.
   - Activités : 1 à 2 patrons + en une ligne ce que l'apprenant y fait.
   - Termes de glossaire : 3 à 8 termes (FR, + EN si bilingue) candidats à l'auto-surlignage/info-bulle.
   - Sources : références courtes [DOCx §y] justifiant le contenu du chapitre.

C) JUSTIFICATION DE LA PROGRESSION (15-25 lignes)
   - Pourquoi cet ORDRE de chapitres ? Montre la chaîne de prérequis (chapitre N nécessite les acquis de N-1).
   - Comment la difficulté monte-t-elle progressivement ?
   - Comment le fil rouge se construit-il étape par étape jusqu'à un livrable final cohérent ?
   - Comment l'évaluation (QCM, flashcards, atelier) s'aligne-t-elle sur les objectifs ?

D) GLOSSAIRE GLOBAL PRESSENTI
   - Liste consolidée et dédoublonnée de TOUS les termes de glossaire (FR, + EN si bilingue), classés par ordre alphabétique, avec le n° de chapitre où chacun apparaît en premier. (Définitions NON requises ici — elles viendront plus tard.)

E) POINTS À CLARIFIER
   - Toute ambiguïté, manque ou contradiction repérés dans les sources, sous forme de questions précises à {{AUTEUR}}.

FORMAT DE SORTIE
- Markdown propre et directement réutilisable.
- Le tableau du syllabus en vraie syntaxe de tableau Markdown (séparateurs |).
- Pas de remplissage verbeux : du concret, exploitable tel quel pour rédiger ensuite les chapitres.
- Ton professionnel, sobre, orienté action.
```

---

## Conseils

- **Renseigne `{{DOCUMENTS_DE_REFERENCE}}` avec le plus de précision possible** (titres exacts, articles, pages, fichiers joints) : la qualité des citations et la fiabilité du plan en dépendent directement.
- Si tu hésites sur `{{NB_CHAPITRES}}`, écris « à proposer (5 à 8) » : Claude proposera un découpage et le justifiera dans la section C, que tu pourras ajuster.
- **Vérifie d'abord la cohérence des durées** (le total doit retomber sur `{{DUREE}}`) et la **mesurabilité des objectifs** (chaque objectif doit commencer par un verbe d'action testable). Refuse tout objectif en « comprendre / connaître ».
- Conserve la sortie comme **document pivot** : les termes de glossaire (section D) alimenteront le prompt glossaire, les objectifs et notions-clés guideront la rédaction des chapitres et la banque de QCM, la « place dans le fil rouge » nourrira l'atelier.
- Traite la section **« Points à clarifier »** avant de lancer la rédaction des chapitres : c'est là que se cachent les inventions évitées et les arbitrages à faire avec l'auteur.
- En mode bilingue, contrôle que **titres et objectifs** existent bien en FR **et** EN (le site génère des blocs FR/EN alternés ; un objectif manquant dans une langue créera un trou dans le rendu).
