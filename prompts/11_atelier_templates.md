# Atelier fil rouge + templates

**Quand l'utiliser :** une fois le plan du cours arrêté et le fil rouge défini, pour concevoir l'**atelier fil rouge** (le scénario continu qui traverse tout le cours), avec sa mission, ses livrables, ses critères d'évaluation, les **templates téléchargeables** (DOCX/XLSX) que l'étudiant complète, et un **corrigé formateur**. À lancer après les prompts de structure du cours (plan, chapitres) et en cohérence avec le QCM d'évaluation. Génère à la fois le contenu pédagogique de l'atelier (intégrable dans la page HTML « Atelier ») et les scripts Python qui fabriquent les fichiers téléchargeables.

---

## Placeholders à compléter

- `{{SUJET_DU_COURS}}` : l'intitulé exact du cours (ex. « Réglementation des données et conformité »).
- `{{PUBLIC_CIBLE}}` : à qui s'adresse le cours (ex. « étudiants M1, futurs DPO et chefs de projet data »).
- `{{NIVEAU}}` : débutant / intermédiaire / avancé.
- `{{DUREE}}` : durée totale du cours et/ou temps alloué à l'atelier (ex. « 24 h de cours, atelier ~6 h réparti sur les chapitres »).
- `{{LANGUES}}` : les langues du cours (`cours.langues`), la langue racine d'abord (`["fr"]`, `["fr", "en"]`). L'atelier s'écrit dans la langue racine ; les autres langues viennent ensuite, une fois la racine stable (module `01-langues.md`).
- `{{DOCUMENTS_DE_REFERENCE}}` : la liste précise des sources à analyser (textes de loi, normes, supports de cours, articles). **À analyser AVANT de produire quoi que ce soit.**
- `{{FIL_ROUGE}}` : le scénario continu déjà retenu pour le cours (organisation fictive, contexte, enjeu). Ex. : « une coopérative agricole fictive qui numérise ses ventes et ses stocks ». Si vide, demander à Claude de le proposer puis de le valider avant de continuer.
- `{{NB_CHAPITRES}}` : le nombre de chapitres du cours, pour cadencer les livrables intermédiaires.
- `{{COMPETENCES_VISEES}}` : les compétences/objectifs pédagogiques du cours auxquels l'atelier doit être relié (idéalement repris du plan de cours).
- `{{LIVRABLE_FINAL}}` : le rendu final attendu (ex. « un dossier de conformité », « un plan d'architecture », « un rapport d'audit »). Si vide, Claude le déduit du sujet et du fil rouge.
- `{{MODALITE}}` : individuel / binôme / groupe ; en présentiel / à distance / hybride.
- `{{OUTILS_AUTORISES}}` : outils que l'étudiant peut/doit utiliser (ex. « tableur, traitement de texte ; pas d'IA générative » ou « IA autorisée avec traçabilité »).
- `{{AUTEUR}}` : l'auteur du cours.
- `{{LICENCE}}` : la licence du contenu produit (ex. « CC BY 4.0 »).
- `{{CONTRAINTES}}` : toute contrainte spécifique (volume, accessibilité, conformité d'un référentiel, interdits, etc.).

---

## PROMPT À COPIER

> Copie tout le bloc ci-dessous dans Claude, après avoir remplacé les `{{...}}`.

```
RÔLE
Tu es ingénieur pédagogique et expert du domaine « {{SUJET_DU_COURS}} ». Tu conçois un ATELIER FIL ROUGE : un scénario continu, pratique et réaliste, qui traverse l'ensemble du cours, avec des livrables progressifs, des templates que l'étudiant complète, des critères d'évaluation explicites, et un corrigé formateur. Cet atelier s'intègre dans un site de cours statique (page « Atelier ») et s'accompagne de fichiers téléchargeables (DOCX/XLSX) générés par des scripts Python.

CONTEXTE DU COURS
- Sujet : {{SUJET_DU_COURS}}
- Public : {{PUBLIC_CIBLE}}
- Niveau : {{NIVEAU}}
- Durée : {{DUREE}}
- Langues : {{LANGUES}}
- Nombre de chapitres : {{NB_CHAPITRES}}
- Fil rouge retenu : {{FIL_ROUGE}}
- Compétences visées : {{COMPETENCES_VISEES}}
- Livrable final attendu : {{LIVRABLE_FINAL}}
- Modalité de travail : {{MODALITE}}
- Outils autorisés : {{OUTILS_AUTORISES}}
- Auteur : {{AUTEUR}}
- Licence : {{LICENCE}}
- Contraintes : {{CONTRAINTES}}
- Documents de référence : {{DOCUMENTS_DE_REFERENCE}}

EXIGENCE D'EXACTITUDE (impérative)
1. AVANT de produire l'atelier, analyse EN DÉTAIL les {{DOCUMENTS_DE_REFERENCE}}. Repère les notions, obligations, étapes de raisonnement et livrables-types propres au domaine.
2. N'invente RIEN : faits, chiffres, articles de loi, normes, procédures doivent provenir des documents. Quand tu t'appuies sur une source, CITE-LA précisément (document + section/article).
3. Le scénario fil rouge doit être plausible mais FICTIF : aucune donnée personnelle réelle, aucune organisation réelle nommément ciblée. Si tu inventes des détails de décor (noms de service, chiffres d'exemple), signale-les comme « fictifs ».
4. Si une information manque pour rester exact, indique explicitement l'hypothèse prise plutôt que de combler par une approximation.
5. Si {{FIL_ROUGE}} est vide ou flou, PROPOSE d'abord 2 scénarios candidats (1 ligne chacun), recommande-en un au regard des compétences visées, et attends ma validation avant de continuer.
6. Aucun chiffre du cas n'est écrit à la main dans la page : il vient du référentiel (outils/referentiel.py), et la page marque sa place par un fragment, <!-- FRAGMENT:nom -->…<!-- /FRAGMENT:nom -->, que outils/generer_fragments.py remplit ; le nombre de livrables (val-livrables) en est un. Donne la liste des fragments employés et des chiffres à ajouter au référentiel.

LANGUE
- Écris tout l'atelier dans la langue racine du cours, la première de {{LANGUES}} : la page « Atelier », les consignes, les critères, les templates et le corrigé.
- Les autres langues viennent ensuite, une fois la racine stable (prompts/modules/01-langues.md). La page « Atelier » aura alors sa jumelle (en/atelier.html, ar/atelier.html), préparée par outils/creer_jumelle.py avec la même suite de blocs, puis traduite bloc pour bloc. N'écris donc aucun bloc data-tr ni aucune paire de blocs `lang="fr"` / `lang="en"` : une page ne porte que sa langue. Chaque template traduit en anglais se déclare dans outils/documents_en.py, et outils/liens_langues.py fait pointer vers lui les liens de la jumelle anglaise.

QUALITÉ PÉDAGOGIQUE (à respecter)
- Une ACCROCHE qui donne envie : place l'étudiant en situation professionnelle réaliste, avec un enjeu (« vous venez d'être recruté·e comme… on vous confie… »).
- Des OBJECTIFS clairs : ce que l'étudiant saura FAIRE à la fin de l'atelier.
- Une PROGRESSION : l'atelier se construit chapitre après chapitre ; chaque livrable réutilise le précédent (effet « dossier qui s'épaissit »).
- Des CONSIGNES opérationnelles et non ambiguës, avec des exemples concrets.
- Un ton qui MOTIVE et responsabilise, sans infantiliser.
- Des encarts « À retenir » et des conseils méthodo aux moments clés.
- Aucun tiret cadratin ni demi-cadratin (–) entre espaces n'entre dans ce que tu produis : une incise passe entre virgules ou entre parenthèses, ou devient une phrase. Un titre prend le deux-points, le point médian ou les parenthèses (« Atelier : adapter la grille »). N'emploie aucune marque de texte généré : un seul deux-points par phrase, ni phrase-choc sans verbe, ni questions rhétoriques en cascade, ni antithèse réflexe, ni triade par habitude, ni mot gonflé (« crucial », « véritable », « au cœur de »). Dans la page, mets une espace insécable avant « : ; ? ! » et à l'intérieur des guillemets « », et n'écris aucune date fixe (« Jour 1 », « séance 2 »).

CE QUE TU DOIS PRODUIRE (dans cet ordre)

PARTIE 1 · CAHIER DE L'ATELIER (contenu pédagogique, prêt à intégrer dans la page HTML « Atelier »)
1.1 Titre de l'atelier + accroche/mise en situation (le fil rouge raconté en 4 à 8 lignes).
1.2 Mission globale : ce que l'étudiant doit produire au total, et le LIVRABLE FINAL attendu ({{LIVRABLE_FINAL}}).
1.3 Objectifs pédagogiques de l'atelier, formulés en verbes d'action observables (ex. « identifier… », « rédiger… », « cartographier… », « évaluer… »).
1.4 Tableau de RELIANCE compétences ⇄ livrables : pour chaque compétence de {{COMPETENCES_VISEES}}, indiquer le(s) livrable(s) de l'atelier qui la mobilise(nt) et la valide(nt). Reste honnête : ne prétends pas qu'un livrable couvre une compétence s'il ne la mobilise pas vraiment.
1.5 Découpage en LIVRABLES INTERMÉDIAIRES, un par chapitre (ou regroupés logiquement si {{NB_CHAPITRES}} est grand). Pour CHAQUE livrable :
    - Numéro et titre du livrable + chapitre rattaché.
    - Mise en situation locale (la suite de l'histoire fil rouge).
    - Consigne précise : ce qu'il faut faire, sur quel template, dans quel format.
    - Données/inputs fournis (extraits fictifs, jeux de données d'exemple), minimaux mais suffisants.
    - Temps estimé et modalité ({{MODALITE}}).
    - Critères de réussite spécifiques au livrable (3 à 5, vérifiables).
    - Indices/coups de pouce différenciés (pour aider sans donner la réponse).
1.6 Articulation avec l'ÉVALUATION : explique comment l'atelier complète le QCM (savoir-faire vs connaissances), et si/comment il est noté.
1.7 BARÈME / grille d'évaluation globale (rubric) : 4 à 6 critères, niveaux (ex. Insuffisant / En cours / Acquis / Maîtrisé), descripteurs observables par niveau, points par critère. Les points totalisent la note maximale du livrable (20 dans la démonstration), comme l'exige outils/seances.py, où la grille s'inscrit ensuite.
1.8 Consignes de rendu : format, nommage des fichiers, délai, modalité de dépôt, rappel {{OUTILS_AUTORISES}}, mention {{LICENCE}} et auteur {{AUTEUR}}. Le délai se donne par un jour du cours et une heure, ou par un repère (« le dimanche qui suit le Jour 2 »), jamais par une date fixe ; outils/seances.py tient ces échéances. Le rendu ne porte aucun nom ni prénom d'étudiant, ni dans le texte, ni dans le nom du fichier, ni dans ses métadonnées (anonymat des copies).

PARTIE 2 · TEMPLATES TÉLÉCHARGEABLES (à fabriquer par script)
Pour chaque livrable intermédiaire et pour le livrable final, conçois le TEMPLATE que l'étudiant complète. Choisis le format selon la nature du travail :
- DOCX (python-docx) pour les livrables rédactionnels/structurés (fiches, notes, rapports, registres en prose).
- XLSX (openpyxl) pour les livrables tabulaires/calculés (cartographies, matrices de risque, plans d'action, checklists à score, registres de traitements).
Chaque template doit contenir : page de garde / en-tête (titre du livrable, cours, fil rouge, champs Groupe et Date, sans champ Nom, pour l'anonymat des copies), la consigne rappelée, une STRUCTURE pré-remplie (sections, tableaux, colonnes nommées, listes déroulantes XLSX si utile, formules de calcul si pertinent), des zones à compléter clairement repérées (ex. « [À COMPLÉTER] »), et un pied de page avec mention {{LICENCE}} · {{AUTEUR}}. Soigne l'accessibilité : styles de titres, contrastes, intitulés de colonnes explicites.

Fournis le CODE PYTHON complet, exécutable hors-ligne, qui génère TOUS les templates, organisé ainsi :
- Dépendances en tête (python-docx, openpyxl, et fpdf2 si une version PDF d'aperçu est demandée), avec commande d'installation.
- Une fonction par template, des noms de fichiers clairs (ex. `atelier_livrable_01_cartographie.xlsx`), un dossier de sortie `site/atelier/templates/`, que le cours crée (les étudiants y téléchargent les modèles).
- Si {{LANGUES}} compte plusieurs langues : tire les libellés d'un dictionnaire par langue, sans dupliquer la logique. Le script génère d'abord la langue racine ; les versions traduites (suffixe `_fr` / `_en`) suivent avec les autres langues du cours.
- Code commenté, réutilisable, paramétrable (le scénario et les libellés en variables en haut du fichier).

PARTIE 3 · CORRIGÉ FORMATEUR
3.1 Pour chaque livrable : un EXEMPLE DE TEMPLATE COMPLÉTÉ de qualité « attendue » (corrigé-type), cohérent avec le fil rouge et exact au regard des documents de référence, avec citations des sources.
3.2 Pour chaque livrable : les ERREURS FRÉQUENTES anticipées et comment les repérer/y remédier.
3.3 GRILLE DE NOTATION renseignée (rappel des critères + ce qui distingue un rendu « Acquis » d'un « Maîtrisé »), et conseils de feedback.
3.4 Variante « atelier court » et « atelier approfondi » (comment alléger ou enrichir selon {{DUREE}}).
3.5 Indique quels fichiers du corrigé doivent rester RÉSERVÉS au formateur : ils ne se publient que dans sa zone protégée par mot de passe (site/correction/formateur/, prompts/modules/06-tp-correction.md), jamais dans une page publique.

FORMAT DE SORTIE
- Partie 1 : Markdown clair, structuré par titres, prêt à transposer en HTML dans la langue racine, sur le balisage de la page Atelier du gabarit (site/atelier.html). Indique les balises/ancres suggérées.
- Partie 2 : blocs de code Python complets et commentés, dans des fenêtres de code séparées, avec la liste des fichiers générés.
- Partie 3 : Markdown, avec un repère visuel « 🔒 RÉSERVÉ FORMATEUR » sur les éléments réservés au formateur.

VÉRIFICATIONS FINALES (fais-les avant de rendre)
- Chaque compétence de {{COMPETENCES_VISEES}} est couverte par au moins un livrable (tableau 1.4 sans trou).
- Chaque livrable a un template correspondant ET une entrée dans le corrigé.
- Le barème compte 4 à 6 critères, dont les points totalisent la note maximale.
- Aucune donnée personnelle réelle ; éléments inventés signalés « fictifs ».
- Toutes les affirmations de domaine sont sourcées dans {{DOCUMENTS_DE_REFERENCE}}.
- Le volume respecte {{DUREE}} et {{CONTRAINTES}}.
Termine par une checklist récapitulative « ce que l'enseignant doit relire/adapter ».
```

---

## Conseils

- **Lance ce prompt APRÈS** avoir figé le plan du cours et le fil rouge : l'atelier doit réutiliser exactement le même scénario, les mêmes noms et le même décor que le reste du site, sinon l'étudiant perd le fil.
- **Donne les vrais documents de référence.** La qualité du corrigé (et donc l'exactitude juridique/technique) dépend entièrement de ce que Claude a réellement lu. Sans sources, exige qu'il signale chaque affirmation comme « à vérifier ».
- **Cadence les livrables sur les chapitres.** Un livrable par chapitre crée l'effet « dossier qui s'épaissit » et garde la motivation ; si `{{NB_CHAPITRES}}` est élevé, regroupe pour ne pas surcharger.
- **DOCX pour le rédactionnel, XLSX pour le tabulaire/calculé.** Demande des listes déroulantes et des formules dans les XLSX (matrices de risque, checklists à score) : c'est plus pédagogique et plus rapide à corriger.
- **Sépare bien étudiant et formateur.** Publie les templates vierges et la grille d'évaluation côté étudiant ; garde le corrigé-type dans la zone protégée du formateur (marqueur 🔒, module `06-tp-correction.md`).
- **Bilingue = double tout.** Si le cours est FR/EN, vérifie que les templates et le corrigé existent dans les deux langues et que les libellés de colonnes sont traduits, pas seulement les consignes.
- **Boucle avec le QCM.** Présente clairement le partage des rôles : le QCM mesure les connaissances (CBM), l'atelier mesure le savoir-faire ; ensemble ils couvrent les compétences visées.
- **Teste le code Python** en local avant publication : exécute-le, ouvre les fichiers générés, vérifie l'accessibilité (styles de titres, intitulés de colonnes) et le rendu des pieds de page (licence + auteur).
