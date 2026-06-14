# Index de la bibliothèque de prompts

> **Quand l'utiliser :** au tout début, avant d'écrire le moindre prompt à Claude. C'est la carte du dossier `prompts/`. Lisez-la une fois, puis revenez-y comme aiguillage entre deux étapes.

Ce dossier contient **13 prompts** qui, enchaînés dans l'ordre, permettent de fabriquer **avec Claude** un site de cours pédagogique complet, hors-ligne et bilingue (FR/EN), à partir du template de ce dépôt.

---

## 1. Philosophie

**On ne génère pas un cours en un seul prompt.** Un cours de qualité — exact, progressif, motivant, accessible, évalué — se construit **étape par étape**, chaque étape s'appuyant sur la précédente.

Quatre principes gouvernent toute la bibliothèque :

1. **Le cadrage d'abord, toujours.** Rien ne se génère tant que le périmètre n'est pas fixé : sujet, public, niveau, durée, langues, documents de référence, fil rouge, nombre de chapitres. C'est le rôle du prompt **`01`**, qui pose les questions **une à une** et produit une **fiche de cadrage** réutilisée par tous les prompts suivants.
2. **Exactitude non négociable.** Chaque prompt qui produit du contenu demande explicitement à Claude d'**analyser en détail les documents de référence AVANT de rédiger**, de **ne rien inventer**, et de **citer ses sources**. En cas de doute ou de lacune, Claude le signale plutôt que de combler par de la fiction.
3. **Un livrable par prompt.** Chaque prompt a une sortie claire et vérifiable (un plan, un chapitre HTML, une banque de QCM, un atelier, un script Python…). On valide une étape avant de passer à la suivante.
4. **Le template pilote la forme.** Les prompts connaissent les fonctionnalités du site (bascule FR/EN, podcast, slides PDF, infographie, QCM CBM, flashcards, glossaire auto-surligné, accessibilité, ateliers fil rouge, polycopiés DOCX/PDF, NotebookLM…) et produisent des sorties qui s'y insèrent directement, sans bricolage.

**Règle d'or :** commencez **TOUJOURS** par `01_cadrage`. Sa sortie alimente tout le reste. Sauter cette étape, c'est s'exposer à des chapitres incohérents, un fil rouge bancal et des QCM hors-sujet.

---

## 2. Le pipeline recommandé (4 phases)

Suivez l'ordre. Vous pouvez itérer à l'intérieur d'une phase (régénérer un chapitre, retoucher un QCM), mais ne sautez pas une phase en avant sans avoir validé la précédente.

### Phase 1 — Cadrage & architecture
> *On décide quoi enseigner, à qui, comment, et dans quel ordre.*

- **`01`** Cadrage interactif (questions une à une → **fiche de cadrage**).
- **`02`** Plan détaillé du cours (chapitres, sections, objectifs pédagogiques, progression).
- **`03`** Fil rouge & scénario continu (le cas pratique qui traverse tout le cours).

### Phase 2 — Contenu pédagogique
> *On rédige le cœur du cours, chapitre par chapitre, avec le vocabulaire associé.*

- **`04`** Rédaction d'un chapitre (HTML bilingue : accroche, objectifs, contenu, exemples, « à retenir »).
- **`05`** Glossaire bilingue (termes + définitions + exemples → auto-surlignage et info-bulles).
- **`06`** Fiches-résumés / synthèses de chapitre (« à retenir » structuré, prêt pour polycopiés).

### Phase 3 — Évaluation & activités
> *On vérifie les acquis et on fait pratiquer.*

- **`07`** Banque de QCM à notation CBM (réponse unique, positions équilibrées, distracteurs débiaisés).
- **`08`** Flashcards de révision (recto/verso par chapitre).
- **`09`** Activités interactives (assistant de décision, quiz-classificateur, calculateur, checklist à score…) — choisies **selon le sujet**.
- **`10`** Atelier « fil rouge » (livrables, templates téléchargeables, corrigé formateur).

### Phase 4 — Production des supports & diffusion
> *On fabrique les supports imprimables/téléchargeables et on prépare l'écosystème média.*

- **`11`** Polycopiés de synthèse (scripts Python : `python-docx` + `fpdf2` → DOCX + PDF).
- **`12`** QCM papier imprimable (DOCX : page de garde, consignes, barème CBM, questions 2 colonnes, grille, corrigé).
- **`13`** Pack NotebookLM (fiche de cours DOCX + prompts pour infographie / slides / podcast par chapitre).

---

## 3. Tableau récapitulatif

| N° | Fichier | Objectif | Entrées | Sorties |
|----|---------|----------|---------|---------|
| **01** | `01_cadrage.md` | Définir le périmètre du cours en interrogeant l'utilisateur **question par question**. | `{{SUJET_DU_COURS}}`, `{{DOCUMENTS_DE_REFERENCE}}`, réponses de l'utilisateur | **Fiche de cadrage** (sujet, public, niveau, durée, langues, fil rouge, nb chapitres, contraintes) |
| **02** | `02_plan_detaille.md` | Bâtir le plan complet : chapitres, sections, objectifs, progression. | Fiche de cadrage, `{{DOCUMENTS_DE_REFERENCE}}` | Plan détaillé + arborescence des sections (ancres de navigation) |
| **03** | `03_fil_rouge.md` | Concevoir le scénario continu qui relie tous les chapitres. | Fiche de cadrage, plan, `{{FIL_ROUGE}}` | Scénario fil rouge + jalons par chapitre |
| **04** | `04_chapitre.md` | Rédiger un chapitre **bilingue** prêt à intégrer au site. | Plan, `{{DOCUMENTS_DE_REFERENCE}}`, n° de chapitre | Chapitre HTML (FR/EN) : accroche, objectifs, contenu, exemples, « à retenir » |
| **05** | `05_glossaire.md` | Produire le glossaire bilingue auto-surligné. | Chapitres rédigés, fiche de cadrage | Termes + définitions + exemples (FR/EN), prêts pour info-bulles |
| **06** | `06_fiches_resume.md` | Synthétiser chaque chapitre en fiche « à retenir ». | Chapitres rédigés | Fiches-résumés structurées (FR/EN) |
| **07** | `07_qcm_cbm.md` | Générer la banque de questions QCM **notation CBM**. | Chapitres, objectifs, `{{NB_CHAPITRES}}` | Banque QCM (réponse unique, positions équilibrées, distracteurs débiaisés) |
| **08** | `08_flashcards.md` | Créer les flashcards recto/verso par chapitre. | Chapitres, glossaire | Jeu de flashcards (FR/EN) |
| **09** | `09_activites_interactives.md` | Concevoir des activités interactives adaptées au sujet. | Fiche de cadrage, chapitres, fil rouge | 1+ activités (assistant, quiz-classificateur, calculateur, checklist…) |
| **10** | `10_atelier_fil_rouge.md` | Construire l'atelier pratique du fil rouge. | Scénario fil rouge, plan | Énoncé + livrables + templates téléchargeables + corrigé |
| **11** | `11_polycopies.md` | Générer les scripts Python des polycopiés DOCX + PDF. | Fiches-résumés, chapitres | Scripts `python-docx` + `fpdf2` → DOCX + PDF par chapitre |
| **12** | `12_qcm_papier.md` | Produire le QCM papier imprimable. | Banque QCM (07) | DOCX : garde + consignes + barème CBM + questions 2 col. + grille + corrigé |
| **13** | `13_pack_notebooklm.md` | Préparer l'intégration NotebookLM. | Chapitres, plan | Fiche de cours DOCX + prompts infographie / slides / podcast par chapitre |

> **Lecture du tableau :** chaque ligne consomme les sorties des lignes au-dessus d'elle. La **fiche de cadrage** (01) est l'entrée commune à presque tout. C'est pourquoi on ne la saute jamais.

---

## 4. Placeholders communs

Tous les prompts utilisent la notation `{{NOM_DU_PLACEHOLDER}}`. Remplissez-les une fois (idéalement dans la fiche de cadrage produite par `01`), puis réutilisez les mêmes valeurs partout pour garantir la cohérence.

| Placeholder | Signification | Exemple |
|-------------|---------------|---------|
| `{{SUJET_DU_COURS}}` | Intitulé et thème du cours. | « Réglementation des données personnelles » |
| `{{PUBLIC_CIBLE}}` | À qui s'adresse le cours. | « Étudiants en master, profils non-juristes » |
| `{{NIVEAU}}` | Niveau de prérequis attendu. | « Débutant / Intermédiaire / Avancé » |
| `{{DUREE}}` | Volume horaire ou durée totale. | « 18 h réparties sur 6 séances » |
| `{{LANGUES}}` | `français seul` **OU** `français + anglais`. | « français + anglais » |
| `{{DOCUMENTS_DE_REFERENCE}}` | Sources faisant autorité à analyser **avant** de rédiger. | « Texte de loi X, rapport Y, normes Z » |
| `{{FIL_ROUGE}}` | Cas pratique continu traversant le cours. | « Projet UrbanHub Smart City » |
| `{{NB_CHAPITRES}}` | Nombre de chapitres prévus. | « 6 » |
| `{{AUTEUR}}` | Auteur·rice du cours (mentions, crédits). | « Mohamed EL AFRIT » |
| `{{LICENCE}}` | Licence du contenu produit. | « CC BY 4.0 (contenu), MIT (code) » |
| `{{CONTRAINTES}}` | Limites, exclusions, ton, exigences spécifiques. | « Pas de jargon, exemples français, hors-ligne » |

> **Astuce :** gardez votre fiche de cadrage ouverte à côté de chaque prompt. Quand un prompt demande `{{FIL_ROUGE}}` ou `{{NB_CHAPITRES}}`, copiez la valeur depuis la fiche — pas de mémoire approximative.

---

## 5. Démarrage rapide

1. Ouvrez **`01_cadrage.md`**, copiez le prompt, complétez `{{SUJET_DU_COURS}}` et `{{DOCUMENTS_DE_REFERENCE}}`, lancez-le dans Claude.
2. Répondez aux questions **une à une**. Récupérez la **fiche de cadrage** générée — c'est votre socle.
3. Enchaînez `02` puis `03` pour figer plan et fil rouge.
4. Déroulez les phases 2 → 4 dans l'ordre, en validant chaque livrable avant le suivant.
5. Intégrez les sorties dans le site-template ; régénérez ponctuellement un livrable si besoin sans tout reprendre.

---

> **Auteur du template :** {{AUTEUR}} · **Licence :** {{LICENCE}}.
> Double licence du dépôt : **MIT** pour le code, **CC BY 4.0** pour le contenu et les prompts.
