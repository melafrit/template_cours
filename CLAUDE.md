# Template de site de cours — contrat de travail

Ce dépôt sert à **fabriquer des sites de cours** : statiques, hors-ligne,
bilingues FR/EN, sans framework. Ce fichier est lu à chaque ouverture : il dit
ce qu'il faut savoir avant de toucher à quoi que ce soit.

---

## 1. La règle qui prime sur toutes les autres

**Ne jamais inventer de contenu pédagogique.**

Les documents de référence déposés dans `sources/` sont la source de vérité. Ce
qui n'y figure pas est signalé comme absent — jamais comblé par une formulation
plausible. Un cours faux et crédible est le pire résultat possible : l'apprenant
ne peut pas le détecter, et il l'apprend.

Concrètement :

- Lire `sources/` **avant** de poser la moindre question de cadrage.
- Citer la source de chaque affirmation qui en vient (titre, section, page).
- Signaler les lacunes et les contradictions entre sources plutôt que trancher
  en silence.
- Tenir `sources/bibliographie.md` à jour au fur et à mesure, pas à la fin.

`sources/` est exclu du dépôt — droit d'auteur. Seuls son mode d'emploi et la
bibliographie sont versionnés.

---

## 2. Démarrer un cours

```bash
cp cours.exemple.json cours.json     # puis le remplir
python3 nouveau_cours.py --essai     # ce qu'il ferait, sans rien écrire
python3 nouveau_cours.py             # crée le cours dans le dossier « sortie »
```

Le script met en place la mécanique — arborescence, charte, navigation,
squelettes, outils. **Il ne rédige aucun contenu.** Le contenu vient ensuite,
par la skill `creer-cours-template`, qui conduit le cadrage en posant ses
questions **une à une** et ne produit rien avant validation explicite.

Le chapitre vitrine est conservé sous `site/chapitres/_modele.html` : c'est le
seul endroit où les composants sont appelés pour de vrai. **Copier depuis là**
plutôt qu'écrire de mémoire.

---

## 3. Ce qui ne se modifie pas à la main

Ces fichiers sont **générés**. Les éditer, c'est perdre le travail à la
prochaine régénération.

| Fichier | Produit par | Source réelle |
|---|---|---|
| `site/assets/js/playlist-data.js` | `outils/generer_playlist.py` | les pages et les fichiers audio |
| `site/assets/js/nav-sections.js` | idem | les titres `<h2>` des chapitres |
| transcriptions des capsules | `outils/synchroniser_capsules.py` | `docs/prompts/Capsules_*.md` |

Une capsule vit à deux endroits — le script balisé et la transcription lisible.
Tenues à la main, elles divergent dès la première correction, et personne ne
s'en aperçoit : on ne lit pas la transcription d'une capsule qu'on vient
d'écouter. **La fiche est la source unique.**

---

## 4. Le contrat bilingue

Trois mécanismes, selon la nature du texte.

**Contenu rédigé** — blocs jumelés dans le HTML, le CSS masque la langue
inactive :

```html
<span data-tr="fr">Bonjour</span><span data-tr="en">Hello</span>
```

**Interface fabriquée en JavaScript** — dictionnaire unique
`site/assets/js/ui-labels.js`, appelé par `T('cle')`. Ne jamais écrire un
libellé en dur dans un moteur : un dictionnaire éparpillé est un dictionnaire
dont on oublie une clé.

**Contenu des composants d'une page** — objet `TEXTES = { fr, en }` dans la
page, et une fonction `monter()` qui vide les conteneurs puis remonte, rejouée
sur `tpl:langchange`. Les moteurs `RDCX` reçoivent des chaînes et ignorent le
bilingue : c'est ce qui les garde simples. Modèle complet dans `_modele.html`.

**Audio bilingue** : un seul appel `RDCX.voice`, mais une source par langue,
déclarée dans `TEXTES` sous `capsuleSrc`. Convention de nommage :
`chapitre-<N>-capsule-<langue>.mp3`. Sans le suffixe, l'auditeur anglophone
entend du français.

---

## 5. Vérifier

Trois contrôles, à lancer souvent. Ils attrapent ce que l'œil ne voit pas.

```bash
python3 outils/verifier_i18n.py       # clés dépareillées, blocs data-tr déséquilibrés
python3 outils/verifier_contraste.py  # palettes lisibles en clair ET en sombre
python3 demarrer.py                   # le site, sans cache
```

`demarrer.py` sert `site/` et envoie `Cache-Control: no-store`. C'est
volontaire : avec un serveur ordinaire, le navigateur ressert l'ancien
JavaScript après une modification, et l'on cherche un défaut qui n'existe pas.

**Si un changement JavaScript ne semble pas prendre**, changez de port plutôt
que de recharger : certains navigateurs gardent le script en cache malgré
l'en-tête.

---

## 6. Conventions à ne pas enfreindre

- **Statique et hors-ligne.** HTML, CSS et JavaScript nus. Aucun framework,
  aucune dépendance à un CDN, aucun appel réseau au chargement.
- **Charte commune, accent par cours.** La teinte se choisit dans `cours.json`
  parmi les palettes de `palettes.css`, toutes vérifiées en contraste. Ne pas
  inventer une couleur sans relancer `verifier_contraste.py`.
- **Rien de propre à une matière dans un moteur.** Les termes du glossaire, les
  libellés métier, les listes de notions vivent dans les données. Un moteur qui
  parle d'une matière rend le template inutilisable pour les autres.
- **Accessibilité.** Texte alternatif sur chaque image, transcription sous
  chaque capsule, contraste vérifié, navigation au clavier. Ce n'est pas une
  faveur faite à une minorité : cela rend la ressource utilisable dans plus de
  situations.
- **Jamais de secret dans le dépôt.** Clé API ElevenLabs, identifiants FTP,
  documents sous droits : tous exclus par `.gitignore`. L'historique Git ne
  s'efface pas.
- **Ne jamais attribuer le contenu à une IA.** Le cours est signé par son
  auteur.
- **Anonymat des copies.** Si le cours produit des livrables étudiants, aucun
  nom ni prénom : ni dans le texte, ni dans le nom de fichier, ni dans les
  métadonnées.

---

## 7. Où chercher le détail

| Question | Fichier |
|---|---|
| Comment fabriquer un cours, pas à pas | `docs/GUIDE.md` |
| Rôle de chaque fichier et de chaque moteur | `docs/ARCHITECTURE.md` |
| Le bilingue en profondeur | `docs/I18N.md` |
| Les pratiques et leurs raisons | `docs/BONNES_PRATIQUES.md` |
| Ce qu'il reste à faire avant de livrer | `docs/CHECKLIST.md` |
| Les prompts de production | `prompts/` |
| Les skills et le pipeline | `.claude/skills/README.md` |

---

## 8. Comment travailler ici

- **Vérifier plutôt qu'affirmer.** Ce dépôt fournit des vérificateurs : les
  lancer coûte quelques secondes et évite des heures.
- **Une modification, une vérification.** Un moteur retouché se teste au
  navigateur, pas seulement à la relecture.
- **Dire ce qui a été fait et ce qui ne l'a pas été.** Un travail annoncé
  terminé qui ne l'est pas coûte plus cher qu'un travail annoncé partiel.
- **Les commentaires expliquent le pourquoi**, pas le comment. Le code dit déjà
  ce qu'il fait ; ce qu'il ne dit pas, c'est le piège qu'on a rencontré et la
  raison du choix.
