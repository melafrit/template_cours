# Registre des travaux — template_cours

> Fichier de suivi du gabarit. **À lire en premier** à la reprise du travail ; « ce qui reste à faire » se répond à
> partir de lui. Dernière mise à jour : **2026-10-26**
>
> Ce qui a été fait, session par session et avec ses commits : [`JOURNAL.md`](JOURNAL.md). Ni ce registre ni le
> journal ne partent dans un cours créé (`nouveau_cours.py` ne recopie de la racine que ce que liste `COPIER`) ; un
> cours tient son propre `TODO.md`.

## 📍 Où en est le gabarit (26 octobre)

| Élément | État |
|---|---|
| Site de démonstration | ✅ trois chapitres en blocs `data-tr` (le modèle de secours), sept composants RDCX, QCM, glossaire, flashcards, activités, atelier |
| Méthode | ✅ prompt paramétrable : un tronc et neuf modules (`prompts/modules/`) ; exigences de l'auteur au § 2 de `CLAUDE.md` |
| Bilingue | ✅ site miroir `en/` par défaut (décision du 25 octobre), outillé ; `data-tr` en secours |
| Outils repris du cours d'architecture logicielle | ✅ **tous** : site miroir, interdits, référentiel et fragments, « Où en parle-t-on ? », page Podcasts, polycopié |
| `nouveau_cours.py` | ✅ blocs `podcasts` et `livret` inactifs par défaut (`livret` demande `glossaire`) ; chaque page d'un cours créé garde son sous-titre |
| Contrôles | ✅ huit (`CLAUDE.md` § 6), plus ceux du site miroir, de la série de podcasts et du polycopié — verts au 26 octobre |

## 🆕 Dernières entrées

> ### 🆕 26 octobre — le polycopié, puis sept correctifs
> La chaîne du polycopié du cours de référence, en générique et bilingue (`797e08a`, `31fb7d1`, `4443c55`) : livret
> Word et PDF tiré des pages du site, QR codes cliquables, page « 📘 Polycopié », publication dans `site/livret/`,
> livret de démonstration publié, bloc `livret`. Puis : la page des fiches orpheline, le menu du prompt, le nom
> « Fiches de synthèse », le renvoi au polycopié retiré d'un cours sans livret, les sous-titres écrasés dans un cours
> créé, la fenêtre de la fiche bilingue (`6d413b1` à `28b19c8`). Détail : `JOURNAL.md`, § 6 et 7.
> ### 🆕 25 octobre — la remise à niveau sur les cours de production
> Sécurité (`.rgignore`, hôte masqué), règles de production dans `CLAUDE.md`, licences ; le prompt en tronc et
> modules ; le site miroir par défaut et ses outils ; les interdits ; le référentiel et ses fragments ; « Où en
> parle-t-on ? » ; la page Podcasts ; le libellé du bouton ♿. Détail : `JOURNAL.md`, § 1 à 5.

## 🛠️ Ouvert — dans le gabarit

Relevés le 26 octobre, laissés pour plus tard à la demande de l'auteur :

- **Les fenêtres des diapositives et de l'infographie** (`site/assets/js/media.js`, `buildSlidesModal`,
  `buildImageModal`) ont leurs libellés écrits en dur, en français (« Fermer », « 📊 Slides — chapitre N »,
  « Ouvrir dans un onglet ↗ ») : un lecteur anglophone les lit en français. Les faire passer par `ui-labels.js`,
  comme la fenêtre de la fiche (`28b19c8`, clés `media.chapitre`, `media.ouvrir`, `media.fermer`), puis tester au
  navigateur dans les deux langues.
- **Les titres d'onglet d'un cours monolingue** restent bilingues sur les pages de ressources (« Glossaire —
  Glossary », « Sommaire du cours — Course contents ») : `nouveau_cours.py` ne doit garder que la langue du cours.
- **Les sondes de `media.js`** : il demande les médias absents d'un chapitre (diapositives, infographie), d'où une
  erreur 404 en console à chaque page, sans effet visible. Une liste des médias présents, ou une sonde silencieuse.

Plus mineurs :

- `deploiement/destination.exemple.json` donne pour adresse d'exemple `https://exemple.org/…`, un domaine qui
  n'est pas réservé : passer à `example.org`, comme le livret.
- `demarrer.py` laisse Python deviner le type des fichiers : sous Windows, les WebP partent en
  `application/octet-stream` (sans effet visible). Déclarer `image/webp`.

## 🔗 Ouvert — dans les cours créés depuis le gabarit (hors de ce dépôt)

- **Cours UML · C4 · BPMN · EPC** (`C:\projets\Cours\Cours_UML_C4_EPC_BPMN`, en blocs `data-tr`) : le libellé du
  bouton ♿ (`site/assets/js/accessibility.js`, ligne 69 : correctif `299c203`) ; les sous-titres de ses pages
  activités, atelier, sommaire, glossaire, fiches et de son chapitre 3, écrasés par celui du cours à sa création
  (`c81717f`) ; le passage au site miroir, une fois son français stable.
- **Cours CDWFS** : le seuil d'apparition des sections longues (`animations.js`, `threshold: 0.08` ; correctif
  `f80bd8b`, relevé le 25 octobre) ; un correctif a été lancé le 26 octobre dans une autre session : à vérifier.
- **Cours d'architecture logicielle** (le cours de référence) : deux commentaires de sa chaîne du polycopié à
  corriger ; son registre (`TODO.md`) les détaille.
- **Tout cours créé avant le 25 octobre** n'a ni les outils du site miroir, ni les interdits, ni les fragments, ni
  « Où en parle-t-on ? », ni la page Podcasts, ni le polycopié : chaque module (`prompts/modules/`) dit comment les
  ajouter à un cours existant.

## ❓ À décider avec l'auteur

- L'ordre de la suite : les défauts ouverts du gabarit, la mise à niveau des cours existants, ou un nouveau cours.
- Une recette complète : un cours créé avec tous ses blocs, mené jusqu'au livret publié et à sa version en site
  miroir, pour éprouver l'ensemble de bout en bout.
- Une relecture d'ensemble de la documentation (README, modules, `CLAUDE.md`), après vingt-huit commits en deux
  jours.

## 📌 Conventions

Celles du § 2 de `CLAUDE.md`, en particulier : commits au seul nom de l'auteur, sans mention d'outil ; une question à
la fois, cliquable, la recommandation d'abord ; accord avant de commiter et de pousser — **ce dépôt est public** :
pousser, c'est publier ; secrets jamais lus ; un exemple avant toute série.
