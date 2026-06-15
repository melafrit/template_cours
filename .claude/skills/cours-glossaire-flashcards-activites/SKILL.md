---
name: cours-glossaire-flashcards-activites
description: À déclencher pour ajouter du contenu INTERACTIF bilingue à un site template_cours — termes de glossaire (info-bulles auto dans les chapitres), flashcards de révision par chapitre, ou activités interactives pilotées par config. Mots-clés FR+EN — "glossaire", "info-bulle", "tooltip", "flashcards", "cartes de révision", "activité interactive", "checklist", "assistant de décision", "glossary", "flashcard", "interactive activity", "decision wizard", "classifier".
---

# Contenu interactif d'un site template_cours

Trois briques interactives, toutes **bilingues** (objets `{ fr, en }`), pilotées par des **données JS** (`window.XXX = …`) que des moteurs lisent. Le `**gras**` Markdown est rendu partout. Tout se ré-affiche sur l'évènement `tpl:langchange` (voir la skill **cours-bilingue-i18n** pour le contrat i18n et `TPLI18N`).

Détail des recettes dans `docs/ARCHITECTURE.md` §4.4 (glossaire) et §4.5 (activités) ; ordre d'inclusion des scripts au §3.

---

## 1) GLOSSAIRE — un terme = une info-bulle partout

**Une seule édition** fait apparaître le terme **à la fois** dans la grille de `glossaire.html` **et** en info-bulle dans le texte des chapitres.

Ajouter une entrée au tableau `window.GLOSSARY` dans `assets/js/glossaire-data.js` :

```js
{ fr: "terme français", en: "english term",
  def: { fr: "Définition FR.", en: "Definition EN." },
  ex:  { fr: "Exemple FR.",    en: "Example EN." } }
```

- `def` et `ex` sont obligatoires en `{fr,en}` ; la def est tronquée à ~180 car. dans l'info-bulle (intégrale au glossaire).
- `glossaire.html` régénère sa grille filtrable (recherche FR+EN, compteur, suit la bascule de langue).
- `glossaire-tooltip.js` surligne **la 1re occurrence** du terme **dans la langue courante**, hors titres (`h1`–`h4`), liens (`a`/`button`), code (`code`/`pre`) et encarts spéciaux (`.law-ref`, `.gloss`, etc.) ; il re-scanne au changement de langue. Aucune liste codée en dur : les termes dérivent de `GLOSSARY` lui-même.

**ALIASES** — variantes orthographiques → entrée canonique. À régler dans l'objet `ALIASES` de `glossaire-tooltip.js` (par langue), p. ex. `'données personnelles' → 'donnée à caractère personnel'`. Utile pour rattacher pluriels/synonymes à une seule entrée.

**curated:true (optionnel)** — pour ne lier en info-bulle qu'**une sélection** de termes : ajouter `curated: true` aux entrées voulues, puis **décommenter le filtre** dans la fonction `curated()` de `glossaire-tooltip.js`. Sans ça, tous les termes du glossaire sont candidats.

Inclusion (page de chapitre) : `glossaire-data.js` **avant** `glossaire-tooltip.js`.

---

## 2) FLASHCARDS — cartes de révision par chapitre

Ajouter une clé de chapitre à `window.RDC_FLASHCARDS` dans `assets/js/flashcards-data.js` (clé = numéro du chapitre, en chaîne) :

```js
"6": [
  { front: { fr: "Question / notion ?", en: "Question / notion?" },
    back:  { fr: "Réponse **avec gras**.", en: "Answer **with bold**." },
    ref:   "art. 5" }        // ref : chaîne (peut être "" si inutile)
]
```

- `front` et `back` sont des objets `{fr,en}` ; `**gras**` rendu. `ref` reste **une chaîne** (référence affichée au dos).

Instancier en bas de la page de chapitre, après tous les `src` (et `flashcards.js` chargé avant) :

```js
new FlashcardDeck('flash-ch6', (window.RDC_FLASHCARDS || {})['6'] || [], 'ch6');
```

- 3e argument = **clé de deck** : sert à mémoriser « su / à revoir » dans `localStorage` (`rdc-flash-<clé>`). Une clé unique par chapitre.
- Ajouter le conteneur dans le HTML : `<div id="flash-ch6"></div>`.

Le deck gère recto/verso, navigation, mélange, barre de progression et se relabellise au changement de langue — rien d'autre à coder.

---

## 3) ACTIVITÉS — `window.TPLActivities` (3 fabriques pilotées par config)

Schéma commun : un `<div id="…"></div>` dans la page + un appel JS qui le remplit. Libellés en `{fr,en}`, `**gras**` supporté, ré-affichage auto sur `tpl:langchange`. Charger `assets/js/tools.js` dans la page ; les activités réutilisent les classes CSS `.rdc-*` de `components.css`. Modèle complet des 3 patrons : `activites.html`.

**`decisionWizard(id, cfg)`** — pas-à-pas : **Oui** → résultat de l'étape ; **Non** → étape suivante ; `fallback` si Non partout.
```js
TPLActivities.decisionWizard('mon-wizard', {
  icon: '🧭', title: { fr: "…", en: "…" },
  steps: [
    { q: { fr: "Question 1 ?", en: "Question 1?" },
      result: { name: { fr: "Résultat", en: "Result" }, detail: { fr: "Détail", en: "Detail" } } }
  ],
  fallback: { name: { fr: "Sinon…", en: "Otherwise…" }, detail: { fr: "…", en: "…" } }
});
```

**`checklist(id, cfg)`** — cases à cocher → verdict selon le **nombre** coché. `{n}` est remplacé par le compte ; les `verdicts` sont évalués du `min` le plus haut au plus bas (mettre le seuil le plus élevé en premier).
```js
TPLActivities.checklist('ma-checklist', {
  icon: '☑️', title: { fr: "…", en: "…" }, intro: { fr: "Cochez :", en: "Tick:" },
  items: [ { fr: "Item 1", en: "Item 1" }, { fr: "Item 2", en: "Item 2" } ],
  verdicts: [
    { min: 2, cls: 'rdc-tier-1', msg: { fr: "🟢 OK — {n}/2.", en: "🟢 OK — {n}/2." } },
    { min: 0, cls: '',           msg: { fr: "⚪ {n}/2.",        en: "⚪ {n}/2." } }
  ]
  // note: { fr, en } optionnel (disclaimer sous l'activité)
});
```

**`classifier(id, cfg)`** — ranger des exemples dans des catégories ; feedback immédiat + score final. Chaque item pointe une `cat` (la `key` d'une catégorie) ; `why` explique.
```js
TPLActivities.classifier('mon-quiz', {
  icon: '🗂️', title: { fr: "…", en: "…" },
  categories: [ { key: 'good', label: { fr: "Bon", en: "Good" } },
                { key: 'bad',  label: { fr: "Mauvais", en: "Bad" } } ],
  items: [ { ex: { fr: "Exemple", en: "Example" }, cat: 'good',
             why: { fr: "Parce que…", en: "Because…" } } ]
});
```

---

> Voir aussi `docs/ARCHITECTURE.md` §4.4/§4.5 et la skill **cours-bilingue-i18n** (formes de données `{fr,en}`, `data-tr`, `TPLI18N`, ré-affichage sur `tpl:langchange`).

> Template de site de cours — **Mohamed EL AFRIT** · code MIT, contenu & prompts CC BY 4.0.
