---
name: cours-bilingue-i18n
description: À utiliser dès qu'on ajoute ou modifie du CONTENU, des ATTRIBUTS ou un MOTEUR JS dans un site template_cours et qu'il faut le maintenir bilingue FR/EN. Couvre les blocs jumeaux data-tr, les attributs data-i18n-*-fr/en, le motif des moteurs ({fr,en} + tpl:langchange) et l'API window.TPLI18N. Mots-clés FR+EN — "bilingue", "i18n", "bascule FR/EN", "traduction", "data-tr", "bilingual content", "language toggle", "translate", "internationalization".
---

# Cours bilingue FR/EN (i18n)

Tout site `template_cours` est **bilingue FR/EN sans build** : HTML/CSS/JS vanilla, hors-ligne. La
langue active est portée par `data-lang` sur `<html>`, la langue inactive est **masquée en CSS**
(jamais retirée du DOM), un bouton 🌐 injecté bascule, le choix tient dans `localStorage`.

**Règle absolue : toute nouvelle chaîne affichée doit exister dans les DEUX langues.** Si le texte
change quand on bascule la langue, il est bilingue ; un id / fichier / index / ancre / icône / href
reste une chaîne neutre.

## Les 3 mécanismes — et quand utiliser chacun

### 1) CONTENU rédigé en HTML → blocs jumeaux `data-tr`
Pour tout texte visible écrit en dur (titres, paragraphes, cartes, libellés de boutons-liens). On
écrit le contenu **deux fois**, dans deux éléments **frères** (même parent), balisage cohérent :

```html
<h1 data-tr="fr">Concevoir un cours</h1><h1 data-tr="en">Designing a course</h1>

<p>
  <span data-tr="fr">Texte FR, <strong>gras</strong> autorisé.</span>
  <span data-tr="en">English text, <strong>bold</strong> allowed.</span>
</p>
```

Aucun JS à écrire. Le masquage vient d'une règle de `assets/css/components.css` :

```css
html[data-lang="fr"] [data-tr="en"] { display: none !important; }
html[data-lang="en"] [data-tr="fr"] { display: none !important; }
```

La bascule est purement visuelle → instantanée, hors-ligne. Les blocs `data-tr` statiques **n'ont
pas besoin** d'écouter le moindre évènement.

### 2) ATTRIBUTS traduisibles → paires `data-i18n-<attr>-fr` / `-en`
Un attribut ne peut pas être « jumelé » comme un élément : on déclare **les deux valeurs en
attributs** et `i18n.js` **échange l'attribut réel** à la bascule. Quatre attributs gérés :

| Attribut cible | Paire à déclarer |
|---|---|
| `aria-label` | `data-i18n-aria-fr` / `data-i18n-aria-en` |
| `title` | `data-i18n-title-fr` / `data-i18n-title-en` |
| `alt` (images) | `data-i18n-alt-fr` / `data-i18n-alt-en` |
| `placeholder` | `data-i18n-ph-fr` / `data-i18n-ph-en` |

Mettre **aussi une valeur par défaut** dans l'attribut réel (no-JS / premier rendu) :

```html
<input data-i18n-ph-fr="Rechercher un terme…" data-i18n-ph-en="Search a term…"
       placeholder="Rechercher un terme…"
       data-i18n-aria-fr="Rechercher dans le glossaire"
       data-i18n-aria-en="Search the glossary"
       aria-label="Rechercher dans le glossaire">
<img src="schema.svg" data-i18n-alt-fr="Schéma de progression"
     data-i18n-alt-en="Progression diagram" alt="Schéma de progression">
```

### 3) UI générée en JS → libellés `{ fr:{…}, en:{…} }` + `t()` + ré-affichage
Quand l'interface est **construite par du JS** (nav, QCM, lecteurs média, flashcards, activités), il
n'y a pas de double bloc à masquer. Motif standard : un dictionnaire indexé par langue, un accesseur
avec **repli sur `fr`**, un ré-affichage sur `tpl:langchange`.

```js
function lang() { return window.TPLI18N ? TPLI18N.lang() : 'fr'; }
var UI = {
  fr: { chapters: 'Chapitres', resources: 'Ressources' },
  en: { chapters: 'Chapters',  resources: 'Resources'  }
};
function t(k) { return (UI[lang()] || UI.fr)[k]; }   // repli sur fr si clé absente

renderTree();
document.addEventListener('tpl:langchange', function () { renderTree(); });
```

Pour les **données** `{ fr, en }`, on résout à l'affichage avec un helper `L()` (tolère une chaîne
simple, replie `fr → en → ''`) — voir `navigation.js` / `flashcards.js` :

```js
function L(x){ return (x && typeof x === 'object') ? (x[lang()] || x.fr || x.en || '') : (x || ''); }
```

## API publique `window.TPLI18N`

Seul point d'entrée. **N'écrivez jamais `data-lang` ni `tpl-lang` à la main.**

| Méthode | Effet |
|---|---|
| `TPLI18N.lang()` | langue active : `'fr'` ou `'en'`. |
| `TPLI18N.supported()` | copie de `['fr','en']`. |
| `TPLI18N.set('en')` | force une langue (ignore valeur non supportée / inchangée), persiste, ré-applique, **émet `tpl:langchange`**. |
| `TPLI18N.toggle()` | bascule FR↔EN. |
| `TPLI18N.refresh(root)` | ré-applique les **attributs** i18n sur un sous-arbre, après injection HTML dynamique. |

`i18n.js` injecte le bouton 🌐 dans `.header-right` (juste avant `.theme-toggle` si présent),
persiste la clé `localStorage['tpl-lang']`, choisit la langue initiale (localStorage → langue
navigateur → `lang` du document → `fr`), et **DOIT être chargé EN PREMIER** dans chaque page (avant
tout moteur, pour que `TPLI18N` existe et éviter un flash de la mauvaise langue).

## Après une injection HTML dynamique
Si vous ajoutez au DOM du HTML porteur d'attributs i18n (`data-i18n-*`), appelez ensuite
**`TPLI18N.refresh(root)`** sur le sous-arbre injecté, sinon ces attributs ne seront traduits qu'au
prochain changement de langue. (Les blocs `data-tr` injectés, eux, sont gérés par le CSS sans appel.)

## Pour aller plus loin
- Formes exactes des données `{fr,en}` (course-data, nav-sections, glossaire, flashcards, QCM) :
  `references/data-shapes.md`.
- Convention complète, checklist, ajout d'une 3e langue : `docs/I18N.md`.
- Contrat bilingue, ordre des scripts, recettes : `docs/ARCHITECTURE.md` (§2.1, §2.3, §3).
- Moteur de référence (API, bouton, attributs, évènement) : `site/assets/js/i18n.js` ;
  UI générée bilingue : `site/assets/js/navigation.js`, `flashcards.js`, `QCM/qcm-core.js`.

> Template de site de cours — **Mohamed EL AFRIT** · code MIT, contenu & prompts CC BY 4.0.
