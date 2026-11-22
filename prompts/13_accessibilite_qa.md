# Accessibilité & contrôle qualité

**Quand l'utiliser :** à la toute fin de la production, une fois que toutes les pages, le QCM, les ateliers, le glossaire et les médias sont en place. Ce prompt lance une **passe d'audit complète puis de correction** du site-template : accessibilité (WCAG), responsive mobile, cohérence des pages jumelles de chaque langue, liens, intégrité du QCM et vérification des médias. À relancer après chaque correction majeure, et juste avant publication.

---

## Placeholders à compléter

- `{{SUJET_DU_COURS}}` : intitulé du cours (ex. « Réglementation des données »).
- `{{LANGUES}}` : les langues du site, la racine d'abord, comme dans `cours.langues` (`["fr"]`, `["fr", "en"]` ou `["fr", "en", "ar"]`).
- `{{RACINE_DU_SITE}}` : chemin/dossier racine du site à auditer (ex. `./site/` ou `.`).
- `{{LISTE_DES_PAGES}}` : liste des fichiers HTML à contrôler (ex. `index.html`, `chapitres/01-cadrage.html`, … `QCM/index.html`, `QCM/correction/index.html`, `QCM/dashboard/index.html`, `glossaire.html`, et leurs jumelles sous `en/` et `ar/`).
- `{{NIVEAU_WCAG}}` : niveau cible, par défaut `WCAG 2.1 AA`.
- `{{NB_CHAPITRES}}` : nombre de chapitres (pour vérifier que chaque chapitre a podcast, slides, infographie, flashcards, QCM, polycopié).
- `{{NB_QUESTIONS_QCM}}` : nombre total de questions du QCM (pour vérifier l'intégrité de la banque).
- `{{NAVIGATEURS_CIBLES}}` : ex. `Chrome, Firefox, Safari, Edge` (versions récentes).
- `{{POINTS_DE_RUPTURE}}` : largeurs responsive à tester (ex. `375px (mobile), 768px (tablette), 1280px (desktop)`).
- `{{AUTEUR}}` : Mohamed EL AFRIT.
- `{{LICENCE}}` : MIT (code) + CC BY 4.0 (contenu).
- `{{CONTRAINTES}}` : contraintes spécifiques (ex. site 100 % hors-ligne, aucun framework, aucune dépendance réseau, RGAA si requis…).

---

## PROMPT À COPIER

> Tu es **auditeur qualité et accessibilité numérique** (référentiels WCAG/RGAA) chargé de la **recette finale** d'un site de cours statique avant publication.
>
> ### Contexte
> - Cours : **{{SUJET_DU_COURS}}**. Auteur : **{{AUTEUR}}**. Licence : **{{LICENCE}}**.
> - Langues du site : **{{LANGUES}}**.
> - Site **statique multi-pages**, HTML/CSS/JavaScript **vanilla**, **aucun framework**, conçu pour fonctionner **100 % hors-ligne** (aucune requête réseau à l'exécution). Contraintes : **{{CONTRAINTES}}**.
> - Racine : `{{RACINE_DU_SITE}}`. Pages à contrôler : `{{LISTE_DES_PAGES}}`.
> - Niveau d'accessibilité visé : **{{NIVEAU_WCAG}}**.
> - Fonctionnalités présentes : un site miroir (chaque page écrite dans une seule langue, déclarée par `lang` sur `<html>`, avec `dir="rtl"` en arabe ; ses jumelles sous `en/` et `ar/`, avec la même suite de blocs ; le groupe de langues « FR · EN · عربي » de l'en-tête, qui rouvre la jumelle au bloc lu ; le dictionnaire `ui-labels.js` pour l'interface fabriquée en JavaScript) ; navigation latérale gauche avec sous-menu pliable d'ancres ; par chapitre un podcast (lecteur audio custom), des slides PDF en popup, une infographie en lightbox ; un QCM à notation CBM avec export CSV signé SHA-256 ; des flashcards ; un glossaire dans chaque langue, dont les termes sont repérés d'eux-mêmes à leur première occurrence, avec info-bulles ; un panneau de réglages d'accessibilité (taille du texte, police « lecture adaptée » Atkinson Hyperlegible, lien d'évitement, respect de `prefers-reduced-motion`), persistant en `localStorage`.
>
> ### Exigence d'exactitude (impérative)
> 1. **N'invente rien.** Avant tout diagnostic, **lis réellement** le code de `{{RACINE_DU_SITE}}` : HTML, CSS, JS. Chaque constat doit citer **le fichier, la ligne (ou le sélecteur/la fonction)** concernés.
> 2. **Ne signale pas de faux positifs.** Si tu n'es pas sûr qu'un point est défaillant, vérifie dans le code ; à défaut, classe-le en « à vérifier manuellement » avec la procédure exacte de test.
> 3. **Ne casse rien.** Toute correction doit préserver le fonctionnement hors-ligne, l'absence de framework et la parité des pages jumelles (une correction d'une page se reporte dans ses jumelles). Pas de dépendance réseau ajoutée.
>
> ### Étape A · Audit (produire un rapport AVANT de corriger)
> Inspecte le site et remplis une **checklist datée**. Pour chaque item : statut `✅ Conforme` / `⚠️ À vérifier` / `❌ Non conforme`, avec preuve (fichier + ligne) et impact (bloquant / majeur / mineur).
>
> **1. Accessibilité WCAG ({{NIVEAU_WCAG}})**
> - **Contrastes** : ratio texte/fond ≥ 4.5:1 (≥ 3:1 pour grand texte et composants d'interface). Teste les couleurs des variables CSS du thème, en clair et en sombre, les états `:hover`/`:focus`, les liens dans le texte, les badges de difficulté/certitude du QCM, les info-bulles du glossaire, le mode « lecture adaptée ».
> - **Navigation clavier** : tout est atteignable et activable au clavier (Tab/Maj+Tab/Entrée/Espace/Échap/flèches). Ordre de tabulation logique. **Focus visible** partout (pas de `outline:none` non remplacé). Pas de piège au clavier. Vérifie en priorité : groupe de langues, sous-menu pliable, lecteur audio (lecture, ±10 s, mini-lecteur déplaçable, pop-out, téléchargement), popups slides, **lightbox infographie** (focus piégé dans la modale + fermeture Échap + retour du focus au déclencheur), flashcards (retournement), panneau de réglages, options du QCM.
> - **Sémantique & ARIA** : un seul `<h1>` par page, hiérarchie de titres sans saut, landmarks (`header`/`nav`/`main`/`footer`), `lang` correct sur `<html>` de chaque page (et `dir="rtl"` sur une page arabe). Modales = `role="dialog"` + `aria-modal="true"` + `aria-label`. Boutons = vrais `<button>`. États `aria-expanded` sur le sous-menu et le panneau de réglages, `aria-pressed` sur les bascules, `aria-current` sur la langue lue du groupe de langues. Live region pour les retours du QCM. **Lien d'évitement** « Aller au contenu » présent et fonctionnel.
> - **Alternatives** : `alt` pertinent sur toutes les images (infographies incluses) ; `alt=""` pour les images décoratives ; libellés accessibles sur les boutons-icônes (♿, lecteur audio, fermeture des modales) et sur ceux du groupe de langues, chacun dans sa langue (attribut `lang`) ; contrôles audio étiquetés ; champs de formulaire (dépôt CSV) avec `<label>` lié.
> - **Mouvement réduit** : `@media (prefers-reduced-motion: reduce)` neutralise/atténue animations, transitions et défilements automatiques (carrousels, retournement de flashcards, ouverture des modales).
> - **Zoom & redimensionnement** : contenu utilisable à **200 %** de zoom et à 320 px de large sans perte d'information ni défilement horizontal à deux dimensions.
> - **Indépendance à la couleur** : l'information (bonne/mauvaise réponse, terme du glossaire surligné, état « su/à revoir ») n'est jamais portée par la **seule** couleur.
>
> **2. Responsive / mobile.** Teste aux points de rupture **{{POINTS_DE_RUPTURE}}** : pas de débordement horizontal ; navigation latérale repliée en menu accessible sur petit écran ; **cibles tactiles ≥ 44×44 px** ; popups slides, lightbox, lecteur audio et flashcards utilisables au tactile ; tableaux du QCM/tableau de bord lisibles (scroll maîtrisé). Vérifie la présence d'un `<meta name="viewport">` correct (sans bloquer le zoom utilisateur).
>
> **3. Cohérence des langues** (si `{{LANGUES}}` compte plusieurs langues)
> - **Parité de contenu** : chaque page de la racine a sa jumelle dans chaque langue, sous `en/` ou `ar/`, avec la même suite de blocs (titres, paragraphes, éléments de liste, figures, composants et conteneurs) ; `outils/verifier_parite.py` le contrôle (0 écart exigé), refuse une jumelle encore marquée « À TRADUIRE » et signale à part un texte resté dans la langue racine (mots accentués d'une page anglaise, titre d'onglet inchangé, bloc arabe sans lettre arabe). Aucun « TODO » ni texte non traduit.
> - **Mécanisme** : le groupe de langues « FR · EN · عربي » ouvre la jumelle choisie et s'y replace sur le bloc lu, à l'aller et au retour ; il n'offre une langue que là où la jumelle existe, d'après `langues-data.js` (`outils/generer_langues.py --essai` dit si la liste est à jour) ; le dictionnaire `ui-labels.js` couvre **toute** l'UI générée en JS (boutons, messages, libellés du QCM, des flashcards, des info-bulles), ses clés contrôlées par `outils/verifier_i18n.py` ; repère les chaînes en dur non traduites.
> - **Persistance & cohérence** : la langue choisie est retenue (l'accueil s'ouvre dans la dernière langue choisie, un lien vers une autre page garde sa langue) ; titres de page, `lang` du document, glossaire et info-bulles suivent la langue de la page, et une page arabe se lit de droite à gauche ; les liens d'une jumelle mènent aux jumelles qui existent (`outils/liens_langues.py`), et les balises `hreflang` sont à jour (`outils/hreflang.py --essai`).
> - Si `{{LANGUES}}` ne compte qu'une langue : vérifie qu'aucun résidu d'une autre langue ne traîne et que le groupe de langues est absent (il n'apparaît qu'à partir de deux langues).
>
> **4. Liens & navigation**
> - **Aucun lien mort** (interne ou ancre) : chaque `href` cible un fichier/une ancre existante ; les ancres du sous-menu pliable pointent vers des `id` réels. Vérifie les liens du fil rouge, des ressources, des téléchargements (polycopiés et livret en PDF, CSV de modèle, médias).
> - **Cohérence inter-pages** : menu identique partout, page active correctement marquée (`aria-current="page"`), fils d'Ariane cohérents.
> - **Liens externes** (s'il y en a) : `target="_blank" rel="noopener noreferrer"`, signalés aux lecteurs d'écran ; le site doit rester fonctionnel hors-ligne (aucune dépendance réseau bloquante).
>
> **5. Intégrité du QCM (CBM).** La banque doit contenir **{{NB_QUESTIONS_QCM}}** questions.
> - **Une seule bonne réponse** par question ; clé de correction cohérente avec les propositions.
> - **Explications** : chaque question dit pourquoi la bonne réponse est juste et pourquoi chacune des autres ne l'est pas, avec deux à quatre renvois « Pour approfondir » vers l'endroit exact du cours (`prompts/15_explications_quiz.md`).
> - **Notation CBM** correcte : Élevée +3/−3, Moyenne +2/−2, Faible +1/0 ; note /20 = `score_brut ÷ (3 × nb_questions) × 20`. Vérifie la **formule dans le code** et sur des cas limites (tout juste / tout faux / non répondu).
> - **Équilibrage des positions** de la bonne réponse (proche de l'uniforme, ex. ~25 % par position pour 4 choix) : calcule la distribution réelle et signale tout biais.
> - **Distracteurs débiaisés** : la bonne réponse n'est pas systématiquement la **plus longue** ni reconnaissable par un indice de forme ; pas de doublons, pas de proposition tronquée, pas de coquille.
> - **Modes** Examen / Entraînement présents et distincts ; **export CSV** généré et **signé en SHA-256** ; la **page de correction** (dépôt d'un CSV) et le **tableau de bord** (plusieurs CSV) lisent le format, **vérifient la signature** et recalculent la note de façon identique. Teste un CSV falsifié → la signature doit être invalidée. Tout doit marcher **hors-ligne**.
>
> **6. Médias & ressources.** Pour chacun des **{{NB_CHAPITRES}}** chapitres :
> - **Podcast** : fichier audio présent, chemin correct, lecteur fonctionnel (lecture, ±10 s, mini-lecteur flottant déplaçable, pop-out, téléchargement), contrôles étiquetés et au clavier.
> - **Slides PDF** : fichier présent, popup plein écran s'ouvre/ferme (Échap), focus géré, fallback de téléchargement.
> - **Infographie** : image présente, lightbox/zoom fonctionnelle, `alt` descriptif.
> - **Polycopié** du chapitre téléchargeable en PDF (le site ne propose pas le DOCX) ; **flashcards** chargées. Le QCM papier, écrit dans `tools/out/`, ne se publie pas et n'entre pas dans cet audit.
> - Vérifie l'**absence de fichiers manquants** (404 locaux), de chemins cassés, de poids média aberrant, et l'absence de référence à une URL réseau requise au chargement.
>
> **7. Hygiène technique**
> - Console **sans erreur JS** au chargement et à l'interaction sur `{{NAVIGATEURS_CIBLES}}`.
> - HTML valide (pas d'`id` dupliqués, ce qui compte pour les ancres), CSS sans règles mortes flagrantes, `localStorage` sans collision de clés (réglages d'accessibilité, langue, flashcards).
> - Encodage UTF-8 partout (pas de caractères cassés, dans aucune langue).
>
> ### Étape B · Correction
> Après avoir présenté le rapport, **corrige les anomalies** par ordre de priorité (bloquant → majeur → mineur). Pour chaque correction :
> - applique le **diff minimal** dans le bon fichier (HTML/CSS/JS), sans introduire de framework ni de dépendance réseau ; un fichier généré (`nav-sections.js`, `langues-data.js`, `media-data.js`, un fragment…) se corrige dans sa source, puis son générateur se relance (`CLAUDE.md`, § 4) ;
> - **n'altère ni le sens pédagogique, ni la parité des pages jumelles, ni l'exactitude du QCM** ;
> - n'écris aucun tiret cadratin, ni tiret demi-cadratin entre espaces, dans les corrections comme dans le rapport (`outils/verifier_tirets.py` contrôle ce qui se publie) ;
> - explique en une phrase **le critère WCAG/règle** corrigé et **pourquoi**.
>
> ### Format de sortie attendu
> 1. **Tableau de bord d'audit** : compteur Conforme / À vérifier / Non conforme par rubrique (1 à 7).
> 2. **Tableau détaillé** des anomalies : `# | Rubrique | Gravité | Fichier:ligne | Constat | Correction proposée | Critère WCAG`.
> 3. **Corrections appliquées** (diffs) et liste des **points à vérifier manuellement** (avec procédure de test précise : lecteur d'écran, navigation clavier, zoom 200 %, etc.).
> 4. **Verdict final** : « Prêt à publier » ou « Bloquants restants » + liste courte des actions restantes.
>
> Commence **maintenant** par lire le code du site, puis produis l'**Étape A** avant toute modification.

---

## Conseils

- **Toujours l'audit avant la correction.** Faire valider le rapport (ou le lire) avant de laisser Claude modifier le code évite les corrections destructrices.
- **Teste réellement le clavier et le zoom à 200 %** : ce sont les écarts WCAG les plus fréquents sur ce type de site (modales, lecteur audio, lightbox, sous-menu pliable).
- **Pour les contrastes**, vérifie les *états* (`:focus`, `:hover`) et le mode « lecture adaptée », pas seulement l'état par défaut.
- **QCM** : fais recalculer la note CBM sur des cas limites et fais **falsifier un CSV** pour confirmer que la signature SHA-256 rejette l'altération.
- **Les langues** : une jumelle restée en partie dans la langue racine (titre d'onglet compris) et les chaînes JS en dur non traduites sont les pièges classiques ; `outils/verifier_parite.py` en signale une partie, demande la liste exhaustive.
- Relance ce prompt **après chaque correction majeure** et une dernière fois **juste avant publication** ; conserve le rapport daté comme preuve de recette.
- Si tu vises aussi le **RGAA**, ajoute-le dans `{{CONTRAINTES}}` et demande la correspondance des critères.
