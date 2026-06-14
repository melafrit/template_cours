# 🛠️ tools/ — Générateurs de documents imprimables

**FR** — Scripts Python qui produisent des **documents imprimables** à partir du contenu du cours :
polycopiés de synthèse (DOCX + PDF) et version papier du QCM (DOCX). Tout est **bilingue FR/EN**.

**EN** — Python scripts that produce **printable documents** from the course content:
synthesis handouts (DOCX + PDF) and a paper version of the quiz (DOCX). Everything is **bilingual FR/EN**.

---

## Installation

```bash
pip install -r tools/requirements.txt
```

> `python-docx` (DOCX), `fpdf2` (PDF), `pypdfium2` (optionnel — aperçu PDF).
> Les sorties sont écrites dans **`tools/out/`**.

## 1. Polycopiés de synthèse — `generate_polycopies.py`

Produit, par chapitre, un **polycopié de synthèse** académique (mini‑sommaire, encadrés
colorés, « à retenir ») en **DOCX + PDF**.

```bash
python tools/generate_polycopies.py            # FR + EN
python tools/generate_polycopies.py fr         # français seulement
python tools/generate_polycopies.py en         # english only
```

Le contenu vient de **`tools/polycopies_content.json`** (bilingue). Schéma :

```json
{
  "1": {
    "title": { "fr": "…", "en": "…" },
    "blocks": [
      ["p",        { "fr": "…", "en": "…" }],
      ["h2",       { "fr": "…", "en": "…" }],
      ["callout", "info", { "fr": "Titre", "en": "Title" }, { "fr": "Texte", "en": "Text" }],
      ["takeaways", [ { "fr": "…", "en": "…" }, { "fr": "…", "en": "…" } ]]
    ]
  }
}
```

Types de blocs : `p` (paragraphe), `h2` (sous‑titre), `callout` (`info|tip|warning|danger`),
`takeaways` (encadré « à retenir »). **Adaptez ce fichier** pour votre cours.

## 2. QCM papier — `generate_qcm_papier.py`

Produit la **version imprimable du QCM** depuis la banque du site
(`site/QCM/questions.js` + `corrections.js`, bilingues) :

- `QCM_questions.<lang>.docx` — page de garde + consignes + **barème CBM avec exemples** + questions en 2 colonnes ;
- `QCM_grille_reponses.<lang>.docx` — grille de réponses (N° · A/B/C/D · certitude F/M/É) ;
- `QCM_corrige.<lang>.docx` — corrigé formateur (bonne réponse + explication).

```bash
python tools/generate_qcm_papier.py            # FR + EN
python tools/generate_qcm_papier.py fr
python tools/generate_qcm_papier.py en
```

> **Barème CBM** : Élevée **+3 / −3**, Moyenne **+2 / −2**, Faible **+1 / 0**.
> Note /20 = score brut ÷ (3 × nombre de questions) × 20.

---

*Template de site de cours — Mohamed EL AFRIT — code MIT, contenu CC BY 4.0.*
