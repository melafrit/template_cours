# Relecture & amélioration pédagogique

**Quand l'utiliser** : tu as déjà un chapitre rédigé (brouillon ou version « presque finie ») et tu veux le faire relire par Claude pour l'améliorer sur la clarté, la motivation, l'exactitude des faits/dates/références, la progression, les exemples et l'équilibre — avant de réécrire. À utiliser après un prompt de génération de chapitre, ou sur un contenu existant que tu veux remettre à niveau. Fonctionne aussi pour un audit qualité avant publication.

---

## Placeholders à compléter

Remplace chaque `{{...}}` par ta valeur avant d'envoyer le prompt.

- `{{SUJET_DU_COURS}}` — intitulé global du cours (ex. « Réglementation des données et conformité »).
- `{{TITRE_CHAPITRE}}` — titre du chapitre relu (ex. « Chapitre 3 — Bases légales du traitement »).
- `{{CONTENU_CHAPITRE}}` — le texte complet du chapitre à relire (colle-le, ou indique le chemin du fichier HTML/Markdown).
- `{{PUBLIC_CIBLE}}` — à qui s'adresse le cours (ex. « étudiants de master, juristes en reconversion »).
- `{{NIVEAU}}` — débutant / intermédiaire / avancé.
- `{{LANGUES}}` — `français seul` **ou** `français + anglais` (déclenche la vérification de cohérence bilingue).
- `{{DOCUMENTS_DE_REFERENCE}}` — sources faisant autorité pour vérifier les faits (textes de loi, articles, normes, supports officiels, chemins de fichiers, URL). **Indispensable pour la vérification d'exactitude.**
- `{{FIL_ROUGE}}` — scénario continu du cours auquel le chapitre doit se rattacher (ex. « UrbanHub Smart City »). Mets `aucun` si non applicable.
- `{{OBJECTIFS_PEDAGOGIQUES}}` — ce que l'étudiant doit savoir/savoir-faire après ce chapitre (si connus ; sinon `à déduire`).
- `{{TON}}` — registre attendu (ex. « professionnel, accessible, qui motive sans infantiliser »).
- `{{CONTRAINTES}}` — limites à respecter (longueur, vocabulaire imposé/interdit, neutralité, accessibilité, terminologie maison, etc.).
- `{{NIVEAU_INTERVENTION}}` — `léger` (corrections ciblées, on garde la voix de l'auteur) / `modéré` / `profond` (réorganisation possible).

---

## PROMPT À COPIER

> ⬇️ Copie tout le bloc ci-dessous dans Claude.

```
RÔLE
Tu es relecteur pédagogique senior et vérificateur de faits pour un cours intitulé « {{SUJET_DU_COURS}} ». Tu relis un chapitre déjà rédigé et tu l'améliores sans en trahir l'intention ni la voix de l'auteur. Tu es exigeant sur l'exactitude : tu ne valides un fait que si tu peux l'appuyer sur les documents de référence.

CHAPITRE À RELIRE
Titre : {{TITRE_CHAPITRE}}
Contenu :
{{CONTENU_CHAPITRE}}

CONTEXTE PÉDAGOGIQUE
- Public cible : {{PUBLIC_CIBLE}}
- Niveau : {{NIVEAU}}
- Langue(s) : {{LANGUES}}
- Objectifs pédagogiques : {{OBJECTIFS_PEDAGOGIQUES}}
- Fil rouge à raccrocher : {{FIL_ROUGE}}
- Ton attendu : {{TON}}
- Contraintes à respecter : {{CONTRAINTES}}
- Niveau d'intervention autorisé : {{NIVEAU_INTERVENTION}}

DOCUMENTS DE RÉFÉRENCE (source de vérité pour la vérification des faits)
{{DOCUMENTS_DE_REFERENCE}}

EXIGENCE D'EXACTITUDE (PRIORITÉ ABSOLUE)
1. AVANT toute réécriture, analyse en détail les documents de référence.
2. Vérifie chaque affirmation factuelle du chapitre : faits, dates, chiffres, noms propres, articles/références de textes, définitions, citations, seuils, sanctions, procédures.
3. Pour chaque point : marque-le ✅ VÉRIFIÉ (conforme aux sources), ⚠️ À VÉRIFIER (plausible mais non confirmé par les sources fournies), ou ❌ ERRONÉ (contredit par les sources).
4. N'invente jamais une source, une date, une référence d'article ou une statistique. Si une info manque dans les documents fournis, ne la « comble » pas : signale-la comme ⚠️ À VÉRIFIER et propose au formateur de la confirmer.
5. Quand tu corriges un fait, cite la source (document + section/article) qui justifie la correction.
6. Distingue clairement ce qui est établi par les sources de ce qui relève de l'interprétation ou de l'exemple pédagogique.

MÉTHODE DE RELECTURE
Évalue le chapitre sur 7 axes, chacun noté de 1 à 5 avec une justification courte :
A. Exactitude (faits/dates/références conformes aux sources)
B. Clarté (phrases, structure, vocabulaire adapté au public et au niveau)
C. Progression (enchaînement logique, du simple au complexe, transitions)
D. Motivation (accroche, intérêt, « pourquoi c'est utile », ton qui engage)
E. Exemples & ancrage (exemples concrets, reliés au fil rouge si pertinent)
F. Équilibre (longueur des sections proportionnée, pas de creux ni de bourrage, pas de redondance)
G. Couverture des objectifs (le chapitre permet-il d'atteindre {{OBJECTIFS_PEDAGOGIQUES}} ?)

VÉRIFICATION BILINGUE (uniquement si {{LANGUES}} = « français + anglais »)
- Vérifie que les versions FR et EN disent la même chose (pas d'info présente d'un côté et absente de l'autre).
- Repère les contresens, faux-amis, terminologie incohérente entre les deux langues.
- Vérifie que les exemples, chiffres et références sont identiques dans les deux versions.
- Signale tout passage non traduit ou traduit machinalement (anglais peu naturel, calques du français).
Si {{LANGUES}} = « français seul », écris « Vérification bilingue : sans objet » et passe à la suite.

LIVRABLE — DEUX TEMPS, DANS CET ORDRE

=== PARTIE 1 : DIAGNOSTIC (NE RÉÉCRIS PAS ENCORE) ===
1. Synthèse en 3-5 phrases : état général du chapitre, points forts, principaux risques.
2. Tableau des notes (axes A à G) : axe | note /5 | justification.
3. Journal de vérification factuelle : tableau « Affirmation | Statut (✅/⚠️/❌) | Source | Correction proposée ».
4. Liste numérotée des corrections proposées, triées par priorité :
   - 🔴 Bloquant (erreur factuelle, contresens, objectif non couvert) ;
   - 🟠 Important (clarté, progression, exemple manquant, déséquilibre) ;
   - 🟡 Confort (style, formulation, micro-améliorations).
   Pour chaque correction : ce qui ne va pas → la modification proposée → pourquoi (bénéfice pédagogique).
5. (Si applicable) Liste des écarts bilingues FR/EN.
6. Questions ouvertes au formateur : points qui demandent une décision ou une source que tu n'as pas (ne réécris pas tant qu'ils bloquent l'exactitude).

PUIS marque une séparation nette : « ----- FIN DU DIAGNOSTIC — VERSION RÉÉCRITE CI-DESSOUS ----- »

=== PARTIE 2 : CHAPITRE RÉÉCRIT ===
- Applique les corrections 🔴 et 🟠 (et les 🟡 si {{NIVEAU_INTERVENTION}} le permet), en respectant le niveau d'intervention autorisé et la voix de l'auteur.
- Conserve la structure de sections (et les ancres/titres) sauf si une réorganisation a été justifiée en Partie 1.
- Garde le format d'origine du contenu (HTML, Markdown, blocs FR/EN alternés) ; ne casse pas le balisage.
- N'introduis aucun fait nouveau non sourcé. Si tu ajoutes un exemple, qu'il soit cohérent avec {{FIL_ROUGE}} et plausible.
- Si {{LANGUES}} = « français + anglais », fournis les deux versions alignées.
- Termine par un « À retenir » de 3 à 5 points clés, et (facultatif) 1-2 questions d'auto-évaluation alignées sur les objectifs.

RÈGLES DE FORME
- Réponds en français (le contenu réécrit suit {{LANGUES}}).
- Sois direct et opérationnel ; pas de remplissage.
- Ne modifie pas silencieusement un fait : toute correction factuelle doit apparaître dans le journal de vérification (Partie 1).
- Si le chapitre est déjà excellent sur un axe, dis-le franchement plutôt que d'inventer des reproches.
```

> ⬆️ Fin du bloc à copier.

---

## Conseils

- **Fournis de vraies sources.** Sans `{{DOCUMENTS_DE_REFERENCE}}` exploitables, la vérification factuelle se limite à « ⚠️ À vérifier » : le prompt est conçu pour ne pas inventer, donc il signalera l'incertitude au lieu de trancher. Colle les textes clés ou donne des chemins/URL précis.
- **Traite la Partie 1 avant la Partie 2.** Lis le diagnostic, valide ou refuse chaque correction, réponds aux « questions ouvertes », puis demande la réécriture finale. Tu gardes la main sur les arbitrages.
- **Calibre `{{NIVEAU_INTERVENTION}}`.** Mets `léger` pour préserver ta plume et ne corriger que l'essentiel ; `profond` seulement si tu acceptes une réorganisation des sections.
- **Itère section par section** pour un long chapitre : tu obtiens un diagnostic plus fin et une réécriture plus fidèle qu'en traitant tout d'un bloc.
- **Bilingue** : lance d'abord la relecture sur le FR (langue de référence), fais valider, puis demande l'alignement EN — tu évites de propager une formulation FR encore instable dans l'anglais.
- **Cohérence avec le glossaire** : demande en complément que les termes du glossaire soient employés de façon constante (orthographe, casse, traduction) pour que l'auto-surlignage et les info-bulles restent fiables.
- **Réutilise le journal de vérification** : conserve-le comme trace qualité (qui a vérifié quoi, contre quelle source) — utile pour la maintenance du cours quand un texte de référence évolue.
