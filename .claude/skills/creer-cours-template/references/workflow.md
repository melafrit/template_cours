# Pipeline en 4 phases — mappé aux fichiers `prompts/`

Ordre recommandé. On peut itérer **à l'intérieur** d'une phase (régénérer un chapitre, retoucher un QCM), mais on ne saute pas une phase en avant sans avoir **validé** la précédente. La règle reste : **un livrable par prompt**, on valide avant de passer au suivant.

> Le détail de chaque prompt (placeholders, bloc à copier, conseils) est dans le fichier lui-même. L'index complet est `prompts/00_README_prompts.md`. Commencer **toujours** par `01`.

## Phase 1 — Cadrage & architecture

*On décide quoi enseigner, à qui, comment, et dans quel ordre.*

| Fichier | Rôle (une ligne) |
|---|---|
| `prompts/01_cadrage_maitre.md` | **Point d'entrée.** Analyse documentaire, cadrage interactif (questions une à une, options numérotées), puis fiche de cadrage + plan du site + feuille de route. |
| `prompts/02_plan_syllabus.md` | Plan détaillé / syllabus : chapitres, sections, objectifs pédagogiques, progression, ancres de navigation. |

## Phase 2 — Contenu pédagogique

*On rédige le cœur du cours, chapitre par chapitre, avec le vocabulaire associé.*

| Fichier | Rôle (une ligne) |
|---|---|
| `prompts/03_chapitre.md` | Rédige un chapitre **bilingue** prêt à intégrer (accroche, objectifs, contenu, exemples, « à retenir »). Un appel par chapitre. |
| `prompts/04_relecture_pedagogique.md` | Relecture pédagogique d'un chapitre : exactitude, progression, clarté, fidélité aux sources, repérage des lacunes. |
| `prompts/06_glossaire.md` | Produit le glossaire bilingue (termes + définitions + exemples FR/EN) pour l'auto-surlignage et les info-bulles. |

## Phase 3 — Évaluation & activités

*On vérifie les acquis et on fait pratiquer.*

| Fichier | Rôle (une ligne) |
|---|---|
| `prompts/07_qcm_banque.md` | Banque de QCM à **notation CBM** (réponse unique, positions des bonnes réponses équilibrées, distracteurs débiaisés) → `questions.js` + `corrections.js`. |
| `prompts/05_activites_interactives.md` | Conçoit les activités interactives adaptées au sujet (assistant de décision, quiz-classificateur, calculateur, checklist à score, flashcards…). |
| `prompts/11_atelier_templates.md` | Atelier « fil rouge » : énoncé, livrables, templates téléchargeables, corrigé formateur. |

## Phase 4 — Supports & diffusion

*On fabrique les supports imprimables/téléchargeables et on prépare l'écosystème média.*

| Fichier | Rôle (une ligne) |
|---|---|
| `prompts/12_polycopies.md` | Scripts Python des polycopiés de synthèse par chapitre (`python-docx` + `fpdf2` → DOCX + PDF). |
| `prompts/08_qcm_papier.md` | QCM papier imprimable (DOCX) : page de garde, consignes, barème CBM, questions 2 colonnes, grille de réponses, corrigé. |
| `prompts/09_notebooklm_fiche.md` | Fiche de cours (DOCX) à fournir à NotebookLM. |
| `prompts/10_notebooklm_18prompts.md` | Jeu de prompts NotebookLM (infographie / slides / podcast par chapitre). |
| `prompts/13_accessibilite_qa.md` | QA finale : accessibilité (RGAA, panneau de réglages), bascule FR/EN, hors-ligne, intégrité du QCM. |

## Placeholders communs

Renseignés **une fois** (idéalement dans la fiche de cadrage produite par `01`), puis réutilisés à l'identique partout pour garantir la cohérence. Notation `{{NOM}}`.

| Placeholder | Signification | Exemple |
|---|---|---|
| `{{SUJET_DU_COURS}}` | Intitulé et thème du cours. | « Réglementation des données personnelles » |
| `{{PUBLIC_CIBLE}}` | À qui s'adresse le cours, prérequis. | « Étudiants M1, profils non-juristes » |
| `{{NIVEAU}}` | Niveau visé. | « Débutant / Intermédiaire / Avancé » |
| `{{DUREE}}` | Volume horaire ou durée totale. | « 18 h sur 6 séances » |
| `{{LANGUES}}` | `français seul` **OU** `français + anglais`. | « français + anglais » |
| `{{DOCUMENTS_DE_REFERENCE}}` | Sources faisant autorité, à analyser **avant** de rédiger. | « Texte de loi X, rapport Y, normes Z » |
| `{{FIL_ROUGE}}` | Cas pratique continu traversant le cours. | « Projet UrbanHub Smart City » |
| `{{NB_CHAPITRES}}` | Nombre de chapitres prévus. | « 6 » |
| `{{AUTEUR}}` | Auteur·rice (mentions, crédits, commits). | « Mohamed EL AFRIT » |
| `{{LICENCE}}` | Licence du contenu produit. | « CC BY 4.0 (contenu), MIT (code) » |
| `{{CONTRAINTES}}` | Limites, exclusions, ton, exigences. | « Pas de jargon, exemples FR, hors-ligne, RGAA » |

> **Rappels.** Un livrable par prompt ; valider avant d'avancer. La **fiche de cadrage** (sortie de `01`) est l'entrée commune à presque tout : elle pré-remplit les placeholders des prompts suivants. La conserver dans le dépôt (ex. `docs/cadrage.md`) comme mémoire de projet.

> Template de site de cours — **Mohamed EL AFRIT** · code MIT, contenu & prompts CC BY 4.0.
