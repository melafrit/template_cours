---
name: cours-supports-imprimables
description: Produit les SUPPORTS IMPRIMABLES du template_cours avec les générateurs Python — le polycopié (tout le cours en un livret Word et PDF à QR codes, outils/generer_polycopie.py), les fiches de synthèse par chapitre (DOCX + PDF) et le QCM papier (DOCX). À utiliser quand on demande des documents à imprimer, distribuer ou réviser hors écran. Mots-clés FR — polycopié, livret, livre du cours, QR code, support imprimable, fiche de synthèse, QCM papier, version papier, imprimer, PDF, DOCX, Word, grille de réponses, corrigé, barème CBM. EN keywords — course book, handout, summary sheet, QR code, printable support, paper quiz, answer grid, marking key, generate documents, print.
---

# Supports imprimables — polycopié, fiches de synthèse & QCM papier (générateurs Python)

Trois générateurs Python transforment le contenu du cours en documents imprimables **bilingues FR/EN**. On **n'écrit jamais les DOCX/PDF à la main** : on édite la source (les pages du site, un JSON ou la banque QCM), puis on relance le script.

## 0. Le polycopié — `outils/generer_polycopie.py` (bloc `livret`, module 02)

Tout le cours en **un livret A4**, tiré des pages du site : garde, mentions, présentation de l'auteur, mini-sommaires, schémas expliqués, activités devenues exercices sur papier, glossaire, index ; des **QR codes cliquables** dans la grande marge, **aucune réponse imprimée**. La méthode complète, ses décisions et ses contrôles : `prompts/modules/02-polycopie.md`.

```bash
python3 outils/generer_polycopie.py --temoin                    # le témoin, validé par l'auteur avant tout
python3 outils/generer_polycopie.py --verrou <fichier>          # le livret français : Polycopie/ (jamais publié)
python3 outils/generer_polycopie.py --anglais --verrou <fichier> # le livret anglais
python3 outils/publier_polycopie.py [--anglais] [--essai]       # → site/livret/ et la page « 📘 Polycopié »
```

Source : les pages du site, `course-data.js`, `glossaire-data.js` et la fiche `outils/livret.py` (présentation de l'auteur, validée par lui, imprimée mot pour mot). Demande Microsoft Word (export PDF, sous verrou : un seul export à la fois) et Chrome ou Edge (photographies, composants).

## Installation

```bash
pip install -r tools/requirements.txt
```

- `python-docx` (DOCX), `fpdf2` (PDF), `pypdfium2` (optionnel — aperçu/rasterisation PDF).
- Les sorties vont dans **`tools/out/`** : dossier **gitignoré et régénérable**, à ne pas versionner.
- Toutes les commandes **sans argument de langue produisent FR **et** EN** (`both` par défaut).

## 1. Fiches de synthèse — `generate_polycopies.py`

Produit, **par chapitre**, une fiche de synthèse académique (mini-sommaire, encadrés colorés, « à retenir ») en **DOCX + PDF** ; au menu, « 📄 Fiches de synthèse », à côté du polycopié complet.

```bash
python tools/generate_polycopies.py          # FR + EN (défaut)
python tools/generate_polycopies.py fr        # français seul
python tools/generate_polycopies.py en        # anglais seul
python tools/generate_polycopies.py both      # FR + EN (explicite)
```

Sorties : `tools/out/chapitre-<n>-polycopie.<lang>.docx` et `.pdf`.

### Source = `tools/polycopies_content.json` (bilingue)

Pour **ajouter ou adapter un polycopié, on ÉDITE ce JSON** — on ne code rien en dur dans le script. Schéma, une entrée par chapitre :

```json
{
  "N": {
    "title": { "fr": "…", "en": "…" },
    "subtitle": { "fr": "…", "en": "…" },
    "blocks": [
      ["p",  { "fr": "…", "en": "…" }],
      ["h2", { "fr": "…", "en": "…" }],
      ["callout", "info", { "fr": "Titre", "en": "Title" }, { "fr": "Texte", "en": "Text" }],
      ["takeaways", [ { "fr": "…", "en": "…" }, { "fr": "…", "en": "…" } ]]
    ]
  }
}
```

Types de blocs :
- `p` — paragraphe (le **gras** se note `**…**` dans le texte) ;
- `h2` — sous-titre de section ;
- `callout` — encadré coloré, 2ᵉ élément = type **`info` | `tip` | `warning` | `danger`**, puis `{titre}` puis `{texte}` ;
- `takeaways` — encadré « À retenir » (liste de puces bilingues).

Règle de fidélité : le polycopié **condense** le chapitre du site, il n'introduit aucune notion, définition, date, chiffre ou exemple absent du chapitre/glossaire (voir `prompts/12_polycopies.md`).

## 2. QCM papier — `generate_qcm_papier.py`

Produit la **version papier du QCM** en lisant directement la **banque du site** : `site/QCM/questions.js` + `site/QCM/corrections.js` (bilingues). C'est la **même banque** que le QCM web — voir la skill **cours-qcm-cbm**.

```bash
python tools/generate_qcm_papier.py           # FR + EN (défaut)
python tools/generate_qcm_papier.py fr
python tools/generate_qcm_papier.py en
```

Trois DOCX par langue dans `tools/out/` :
- **`QCM_questions.<lang>.docx`** — page de garde (NOM / PRÉNOM / DATE) + consignes + **barème CBM avec exemples chiffrés** + questions en **2 colonnes** ;
- **`QCM_grille_reponses.<lang>.docx`** — grille de réponses (N° · A/B/C/D · certitude F/M/É) ; **seul document ramassé** ;
- **`QCM_corrige.<lang>.docx`** — corrigé formateur (bonne réponse + explication), regroupé par chapitre ; **ne pas distribuer aux étudiants**.

### Barème CBM (Certainty-Based Marking) — à reproduire à l'identique du QCM web

| Certitude | Bonne | Mauvaise |
|-----------|-------|----------|
| **Élevée** | **+3** | **−3** |
| **Moyenne** | **+2** | **−2** |
| **Faible** | **+1** | **0** |

**Note /20 = score brut ÷ (3 × N) × 20** (N = nombre de questions ; maximum = 3 × N ; une note négative est ramenée à 0). À défaut de certitude indiquée → « Faible ». La difficulté (vert/orange/rouge) est **indicative** et n'entre **pas** dans le calcul. Utiliser le vrai signe moins « − » (U+2212).

Pour modifier le QCM papier, on **corrige la banque** (`questions.js` / `corrections.js`) puis on **régénère** — jamais le DOCX à la main.

## Pour aller plus loin

- `prompts/modules/02-polycopie.md` — le polycopié : décisions, architecture, pièges, contrôles.
- `tools/README.md` — référence des commandes et du schéma.
- `prompts/12_polycopies.md` — polycopiés : structure pédagogique, exigence d'exactitude, checklist.
- `prompts/08_qcm_papier.md` — QCM papier : contrôle d'intégrité de la banque, mise en page compacte N&B, checklist avant impression.
- Skill **cours-qcm-cbm** — la banque QCM réutilisée ici (questions.js + corrections.js, barème CBM).
- Bilinguisme : `docs/I18N.md` et skill **cours-bilingue-i18n**.

> Template de site de cours — **Mohamed EL AFRIT** · code MIT, contenu & prompts CC BY 4.0.
