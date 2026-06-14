# Activités interactives sur mesure

**Quand l'utiliser**
Quand vous voulez ajouter à un (ou plusieurs) chapitre(s) du site-template une ou plusieurs **activités interactives** réellement adaptées au sujet — pas un gadget générique. Claude commence par **proposer** les patrons les plus pertinents pour votre cours, **clarifie** le besoin avec vous (une question à la fois), puis **génère** le contenu/les données de l'activité choisie, prêt à intégrer (HTML/JS vanilla + i18n FR/EN).

À lancer **après** avoir défini le squelette du cours et au moins un chapitre. Idéal en complément du QCM, des flashcards et de l'atelier fil rouge, pour varier les modalités et maximiser l'engagement.

---

## Placeholders à compléter

- `{{SUJET_DU_COURS}}` — intitulé précis du cours (ex. « Réglementation des données et conformité »).
- `{{CHAPITRE_CIBLE}}` — chapitre / section concerné(e) (titre + n°). Indiquez « à proposer » si vous voulez que Claude suggère où placer l'activité.
- `{{OBJECTIF_PEDAGOGIQUE}}` — ce que l'étudiant doit savoir **faire** après l'activité (verbe d'action : décider, classer, calculer, vérifier, mémoriser, synthétiser…).
- `{{PUBLIC_CIBLE}}` — ex. « étudiants Master 2 », « professionnels en formation continue ».
- `{{NIVEAU}}` — débutant / intermédiaire / avancé.
- `{{DUREE}}` — temps visé pour réaliser l'activité (ex. « 5–10 min »).
- `{{LANGUES}}` — `français seul` OU `français + anglais`.
- `{{DOCUMENTS_DE_REFERENCE}}` — fichiers/sources faisant autorité (textes officiels, supports de cours, polycopiés). Claude doit s'y tenir.
- `{{FIL_ROUGE}}` — scénario continu du cours (ex. « UrbanHub Smart City ») pour ancrer l'activité dans le cas pratique, si pertinent.
- `{{NB_ACTIVITES}}` — combien d'activités vous souhaitez au total (ex. 1, ou « 1 par chapitre »).
- `{{CONTRAINTES}}` — limites à respecter (hors-ligne, pas de dépendances externes, accessibilité, durée, ton, neutralité…).
- `{{AUTEUR}}` — auteur du cours.
- `{{LICENCE}}` — licence du contenu (ex. CC BY 4.0).

---

## PROMPT À COPIER

> Copiez tout le bloc ci-dessous dans Claude, après avoir remplacé les `{{...}}`.

```
Tu es ingénieur pédagogique et développeur front-end. Tu m'aides à concevoir une ou
plusieurs ACTIVITÉS INTERACTIVES pour un site de cours statique (HTML/CSS/JavaScript
vanilla, hors-ligne, thématisé par variables CSS, bilingue via une bascule de langue 🌐
avec attribut data-lang sur <html> et un dictionnaire i18n pour l'UI générée en JS).

CONTEXTE DU COURS
- Sujet : {{SUJET_DU_COURS}}
- Chapitre/section cible : {{CHAPITRE_CIBLE}}
- Objectif pédagogique visé : {{OBJECTIF_PEDAGOGIQUE}}
- Public : {{PUBLIC_CIBLE}} — Niveau : {{NIVEAU}} — Durée visée : {{DUREE}}
- Langues : {{LANGUES}}
- Fil rouge du cours : {{FIL_ROUGE}}
- Nombre d'activités souhaité : {{NB_ACTIVITES}}
- Auteur : {{AUTEUR}} — Licence du contenu : {{LICENCE}}
- Contraintes : {{CONTRAINTES}}
- Documents de référence : {{DOCUMENTS_DE_REFERENCE}}

EXIGENCE D'EXACTITUDE (impérative)
- Analyse EN DÉTAIL les documents de référence AVANT toute proposition. N'invente aucune
  règle, aucun chiffre, aucun fait. Si une donnée manque, dis-le et pose la question ;
  ne comble jamais un trou par une supposition.
- Tout contenu (énoncés, bonnes réponses, justifications, seuils de calcul, items de
  checklist) doit être traçable à une source. Cite la source précise (titre + article/
  page/section) à côté de chaque élément sensible.
- Si les documents sont insuffisants pour produire une activité fiable, signale-le
  clairement plutôt que de produire quelque chose d'approximatif.

PATRONS D'ACTIVITÉ DISPONIBLES DANS LE TEMPLATE (tu CHOISIS selon le sujet)
1. Assistant de décision pas-à-pas — l'étudiant répond à une suite de questions et
   l'arbre le mène à une conclusion motivée (« Faut-il X ? Dans ce cas, fais Y »).
   Idéal pour : qualifier une situation, choisir une procédure, appliquer un cadre.
2. Quiz-classificateur à feedback — l'étudiant range des cas/exemples dans les bonnes
   catégories ; feedback immédiat et explicatif à chaque réponse.
   Idéal pour : distinguer des notions proches, typologies, qualifications juridiques.
3. Calculateur / simulateur — saisie de paramètres → résultat chiffré + interprétation
   (barème, montant, délai, score, jauge).
   Idéal pour : barèmes, seuils, échéances, estimations, « et si… ».
4. Checklist à score — liste de critères cochables qui produit un score / un niveau de
   conformité ou de maturité, avec recommandations selon le résultat.
   Idéal pour : auto-évaluation, audit léger, mise en conformité étape par étape.
5. Flashcards de révision — recto/verso, statut « su / à revoir », mémorisation espacée
   légère (persistance localStorage).
   Idéal pour : vocabulaire, définitions, dates, formules, points clés à ancrer.
6. Fiches-résumés interactives — cartes/onglets repliables qui synthétisent l'essentiel
   (« à retenir »), avec révélation progressive.
   Idéal pour : récapituler un chapitre, comparer des notions côte à côte.

DÉROULÉ ATTENDU (respecte cet ordre)

ÉTAPE A — PROPOSITION RAISONNÉE
À partir du sujet, de l'objectif et des documents, recommande les 2 ou 3 patrons LES PLUS
ADAPTÉS (pas tous). Pour chacun : explique en 2–3 phrases pourquoi il sert l'objectif
pédagogique, ce que l'étudiant y gagne en engagement, et donne un exemple concret tiré du
chapitre cible. Termine par une recommandation classée (1er choix, alternatives) et une
estimation de l'effort de réalisation.

ÉTAPE B — CLARIFICATION (questions UNE À LA FOIS)
Avant de produire le contenu, pose-moi tes questions une par une (attends ma réponse
entre chaque). Couvre au minimum :
- le patron retenu (si je n'ai pas tranché) ;
- le périmètre exact (combien de cas/questions/critères, quelles notions) ;
- le niveau de difficulté et le ton ;
- le rôle du fil rouge (l'activité doit-elle se dérouler dans le scénario {{FIL_ROUGE}} ?) ;
- les sources précises à utiliser et celles à exclure ;
- le format de sortie souhaité (voir Étape D).
Ne pose pas plus d'une question à la fois. Reformule brièvement ma réponse avant la
suivante. Quand tu as assez d'informations, annonce que tu passes à la production.

ÉTAPE C — CONCEPTION PÉDAGOGIQUE
Rédige une courte fiche de cadrage : objectif d'apprentissage, consigne pour l'étudiant
(claire et motivante, avec une accroche), critère de réussite, et la place de l'activité
dans la progression du chapitre. Prévois un message « à retenir » de clôture.

ÉTAPE D — PRODUCTION DU CONTENU / DES DONNÉES
Produis l'activité prête à intégrer, en respectant le patron retenu :

- Sépare clairement (a) les DONNÉES de l'activité et (b) le squelette d'intégration.
  Fournis les données dans une structure JS lisible (objet/tableau) et bien commentée,
  facile à brancher sur le composant du template.
- BILINGUE : si {{LANGUES}} = français + anglais, fournis chaque texte visible en FR ET
  en EN (clés `fr`/`en` ou blocs alternés), y compris consignes, questions, options,
  feedbacks, justifications, boutons. Si français seul, ne fournis que le FR mais garde
  une structure prête à accueillir l'anglais plus tard.
- FEEDBACK FORMATIF : pour chaque réponse/branche, donne un retour qui EXPLIQUE le
  pourquoi (et renvoie à la notion / source), pas seulement « correct / incorrect ».
- QUALITÉ DES ITEMS selon le patron :
  • Assistant de décision : arbre explicite (nœud → conditions → branches → conclusion),
    sans impasse, chaque feuille avec une recommandation actionnable et sourcée.
  • Quiz-classificateur : catégories mutuellement exclusives et bien définies ; cas non
    caricaturaux ; au moins un cas « piège » par catégorie ; justification par cas.
  • Calculateur/simulateur : variables d'entrée, formule(s)/règle(s) EXPLICITES et
    sourcées, bornes/validations, interprétation du résultat par paliers, avertissement
    si le calcul est une simplification.
  • Checklist à score : critères non ambigus, pondération justifiée, paliers de score
    avec recommandations différenciées, et rappel que le score est indicatif.
  • Flashcards : recto concis / verso complet ; éviter les formulations ambiguës ;
    une seule idée par carte.
  • Fiches-résumés : hiérarchie claire, « à retenir » saillant, comparaisons en
    parallèle si pertinent.
- ACCESSIBILITÉ : textes clairs et lisibles, pas d'information portée par la seule
  couleur, libellés explicites pour les contrôles, compatible navigation clavier et
  agrandissement du texte. Respecte prefers-reduced-motion (pas d'animation indispensable
  à la compréhension).
- HORS-LIGNE & SANS DÉPENDANCE : aucun appel réseau, aucune librairie externe ; tout doit
  fonctionner en ouvrant le fichier localement.

ÉTAPE E — INTÉGRATION & VÉRIFICATION
- Indique précisément où insérer l'activité dans le chapitre cible (ancre/section) et
  comment l'annoncer à l'étudiant.
- Fournis une CHECKLIST DE RELECTURE : exactitude vérifiée vs sources, parité FR/EN
  complète, feedback présent partout, accessibilité, absence d'impasse/d'ambiguïté,
  cohérence avec le fil rouge, durée réaliste.
- Termine par une note de licence/attribution conforme à {{LICENCE}} ({{AUTEUR}}).

CONTRAINTES DE FORME
- Réponds en français (le contenu de l'activité peut être bilingue selon {{LANGUES}}).
- Ton direct, professionnel, opérationnel ; mais l'activité doit MOTIVER l'étudiant.
- Ne produis PAS tout d'un coup : respecte les étapes A → E et la clarification
  question par question.

Commence MAINTENANT par l'ÉTAPE A (proposition raisonnée), en t'appuyant strictement sur
les documents de référence.
```

---

## Conseils

- **Laissez Claude proposer.** L'intérêt de ce prompt est le choix du patron *selon le sujet* : ne forcez un patron que si vous avez une idée précise. Sinon, lisez l'Étape A et tranchez ensuite.
- **Une activité par objectif.** Une activité qui vise un seul objectif clair engage mieux qu'un patron fourre-tout. Pour couvrir plusieurs objectifs, lancez le prompt plusieurs fois.
- **Ancrez dans le fil rouge** (`{{FIL_ROUGE}}`) dès que possible : un cas concret et continu rend l'activité bien plus motivante qu'un exemple abstrait.
- **Exigez les sources.** Pour les activités à enjeu (calcul de barème, qualification juridique, checklist de conformité), vérifiez systématiquement les justifications et seuils contre `{{DOCUMENTS_DE_REFERENCE}}` avant intégration.
- **Pensez bilingue dès le départ** si le cours est FR/EN : il est plus coûteux de traduire après coup que de demander la parité FR/EN dès la génération.
- **Réutilisez le composant existant.** Demandez à Claude de produire surtout les *données* de l'activité dans la structure attendue par le template, plutôt que de réécrire le composant — c'est plus rapide à intégrer et plus cohérent.
- **Calibrez la difficulté** via `{{NIVEAU}}` et la phase de clarification : prévoyez au moins un cas « piège » par catégorie dans les quiz-classificateurs pour éviter une activité trop facile.
- **Vérifiez l'absence d'impasse** dans les assistants de décision : chaque chemin doit aboutir à une conclusion actionnable.
