# Index de la bibliothèque de prompts

> **Quand l'utiliser :** au tout début, avant d'écrire le moindre prompt à Claude. C'est la carte du dossier `prompts/`. Lisez-la une fois, puis revenez-y comme aiguillage entre deux étapes.

Ce dossier contient **le prompt paramétrable** de création d'un cours, et **seize prompts de production** qui, enchaînés dans l'ordre, permettent de fabriquer **avec Claude** un site de cours pédagogique complet, hors-ligne et (si on le veut) bilingue FR/EN, à partir du template de ce dépôt.

---

## 0. Le point d'entrée : le prompt paramétrable

**[`PROMPT-Cours-parametrable.md`](PROMPT-Cours-parametrable.md)** — un bloc de paramètres (le cours, les filières, le fil rouge, le TP, les livrables, l'évaluation, les médias, la publication, Git) et la méthode complète : règles de conduite, étape zéro depuis ce template, chaînes de production, **douze phases avec leurs jalons STOP**, contrôles avant mise en ligne, définition de « terminé ».

C'est lui que suit la skill `creer-cours-template` quand on demande à Claude de « créer un cours ». Les prompts ci-dessous en sont les outils, étape par étape.

---

## 1. Philosophie

**On ne génère pas un cours en un seul prompt.** Un cours de qualité — exact, progressif, motivant, accessible, évalué — se construit **étape par étape**, chaque étape s'appuyant sur la précédente.

Cinq principes gouvernent toute la bibliothèque :

1. **Le cadrage d'abord, toujours.** Rien ne se génère tant que le périmètre n'est pas fixé : sujet, public, niveau, durée, langues, documents de référence, fil rouge, nombre de chapitres. C'est le rôle du prompt **`01`**, qui pose les questions **une à une** et produit une **fiche de cadrage** réutilisée par tous les prompts suivants.
2. **Exactitude non négociable.** Chaque prompt qui produit du contenu demande explicitement à Claude d'**analyser en détail les documents de référence AVANT de rédiger**, de **ne rien inventer**, et de **citer ses sources**. En cas de doute ou de lacune, Claude le signale plutôt que de combler par de la fiction.
3. **Un livrable par prompt.** Chaque prompt a une sortie claire et vérifiable (un plan, un chapitre HTML, une banque de QCM, une fiche de capsules…). On valide une étape avant de passer à la suivante.
4. **Le template pilote la forme.** Les prompts connaissent les fonctionnalités du site (bascule FR/EN, composants RDCX, QCM CBM, flashcards, glossaire, capsules audio, polycopiés…) et produisent des sorties qui s'y insèrent directement.
5. **Chaque erreur s'explique.** Toute question à choix dit pourquoi la bonne réponse est juste, pourquoi chacune des autres ne l'est pas, et où approfondir (prompt **`15`**).

**Règle d'or :** commencez **TOUJOURS** par le cadrage (`01`, appelé par le prompt paramétrable). Sauter cette étape, c'est s'exposer à des chapitres incohérents, un fil rouge bancal et des QCM hors-sujet.

---

## 2. Le pipeline recommandé (4 phases)

Suivez l'ordre. Vous pouvez itérer à l'intérieur d'une phase (régénérer un chapitre, retoucher un QCM), mais ne sautez pas une phase en avant sans avoir validé la précédente.

### Phase 1 — Cadrage & architecture
> *On décide quoi enseigner, à qui, comment, et dans quel ordre.*

- **`01`** Cadrage interactif (questions une à une → **fiche de cadrage**, plan du site, feuille de route).
- **`02`** Plan détaillé et syllabus (chapitres, sections, objectifs, progression, ancres).

### Phase 2 — Contenu pédagogique
> *On rédige le cœur du cours, chapitre par chapitre, avec le vocabulaire associé.*

- **`03`** Rédaction d'un chapitre (accroche, objectifs, contenu, exemples, « à retenir »).
- **`04`** Relecture pédagogique d'un chapitre.
- **`06`** Glossaire (termes, définitions, exemples → info-bulles) ; **`06b`** « Où en parle-t-on ? ».

### Phase 3 — Évaluation & activités
> *On vérifie les acquis et on fait pratiquer.*

- **`05`** Activités interactives, choisies **selon le sujet**.
- **`07`** Banque de QCM à notation CBM.
- **`15`** Explications complètes de chaque question à choix, avec renvois « Pour approfondir ».
- **`11`** Atelier « fil rouge » (livrables, modèles téléchargeables, corrigé formateur).

### Phase 4 — Médias, supports, audit
> *On fabrique les supports et les médias, puis on contrôle tout.*

- **`14`** Capsules audio en Eleven v4 (fiche de production, témoin d'abord).
- **`12`** Polycopiés de synthèse (DOCX + PDF).
- **`08`** QCM papier imprimable (DOCX).
- **`09`** et **`10`** Pack NotebookLM (fiche de cours, prompts infographie / slides / podcast).
- **`13`** Accessibilité et contrôle qualité.

---

## 3. Tableau récapitulatif

| N° | Fichier | Objectif | Entrées | Sorties |
|----|---------|----------|---------|---------|
| — | `PROMPT-Cours-parametrable.md` | Créer un cours complet, de l'amorçage à la mise en ligne. | Bloc de paramètres, `sources/` | Le cours, phase par phase, jalons STOP |
| **01** | `01_cadrage_maitre.md` | Cadrer le cours en interrogeant l'auteur **question par question**. | Sujet, documents de référence, réponses | **Fiche de cadrage**, plan du site, feuille de route |
| **02** | `02_plan_syllabus.md` | Bâtir le plan complet : chapitres, sections, objectifs, progression. | Fiche de cadrage, sources | Syllabus + ancres de navigation |
| **03** | `03_chapitre.md` | Rédiger un chapitre prêt à intégrer. | Plan, sources, n° de chapitre | Chapitre HTML (FR, ou FR/EN) |
| **04** | `04_relecture_pedagogique.md` | Relire un chapitre : exactitude, progression, clarté, fidélité aux sources. | Chapitre, sources | Corrections et lacunes signalées |
| **05** | `05_activites_interactives.md` | Concevoir des activités adaptées au sujet. | Cadrage, chapitres, fil rouge | Activités prêtes à monter |
| **06** | `06_glossaire.md` | Produire le glossaire et ses info-bulles. | Chapitres, cadrage | Termes, définitions, exemples |
| **06b** | `06b_glossaire_ou_en_parle_t_on.md` | Relier chaque terme à tous les endroits qui l'emploient. | Glossaire, pages publiées | Badge « Où en parle-t-on ? » et liens précis |
| **07** | `07_qcm_banque.md` | Générer la banque de QCM **notation CBM**. | Chapitres, objectifs | `questions.js` + `corrections.js` |
| **08** | `08_qcm_papier.md` | Produire le QCM papier imprimable. | Banque QCM | DOCX : garde, consignes, barème, questions, grille, corrigé |
| **09** | `09_notebooklm_fiche.md` | Préparer la fiche de cours pour NotebookLM. | Chapitres | Fiche DOCX |
| **10** | `10_notebooklm_18prompts.md` | Les prompts NotebookLM par chapitre. | Fiche | Infographie, slides, podcast |
| **11** | `11_atelier_templates.md` | Construire l'atelier fil rouge. | Fil rouge, plan | Énoncé, livrables, modèles, corrigé |
| **12** | `12_polycopies.md` | Générer les polycopiés DOCX + PDF. | Chapitres | `tools/generate_polycopies.py` et ses sorties |
| **13** | `13_accessibilite_qa.md` | Auditer l'accessibilité et la qualité. | Site assemblé | Corrections, puis vérification au navigateur |
| **14** | `14_capsules_audio.md` | Écrire les capsules audio pour Eleven v4. | Pages, schémas, sources | Fiche `docs/prompts/Capsules_*.md`, témoin désigné |
| **15** | `15_explications_quiz.md` | Expliquer chaque proposition d'un quiz. | Questions, pages, ancres | `pourquoi` + `approfondir` par question |

> **Lecture du tableau :** chaque ligne consomme les sorties des lignes au-dessus d'elle. La **fiche de cadrage** (01) est l'entrée commune à presque tout.

---

## 4. Placeholders communs

Tous les prompts utilisent la notation `{{NOM_DU_PLACEHOLDER}}`. Remplissez-les une fois (idéalement dans la fiche de cadrage produite par `01`, ou dans le bloc de paramètres du prompt paramétrable), puis réutilisez les mêmes valeurs partout.

| Placeholder | Signification | Exemple |
|-------------|---------------|---------|
| `{{SUJET_DU_COURS}}` / `{{TITRE_DU_COURS}}` | Intitulé et thème du cours. | « Réglementation des données personnelles » |
| `{{PUBLIC_CIBLE}}` | À qui s'adresse le cours : prérequis et contraintes. | « Développeurs en alternance, sans formation sécurité » |
| `{{NIVEAU}}` | Niveau de prérequis attendu. | « Débutant / Intermédiaire / Avancé » |
| `{{DUREE}}` | Volume horaire ou durée totale. | « 14 h sur deux jours » |
| `{{LANGUES}}` | `français seul` **OU** `français + anglais`. | « français seul » |
| `{{DOCUMENTS_DE_REFERENCE}}` | Sources faisant autorité, analysées **avant** de rédiger. | « Fiche module, grille d'évaluation, norme X » |
| `{{FIL_ROUGE}}` | Cas pratique continu traversant le cours. | « Projet UrbanHub Smart City » |
| `{{INTERDITS_DU_COURS}}` | Mots et exemples à ne jamais employer (sujet du TP…). | « le sujet du TP, ses chiffres » |
| `{{NB_CHAPITRES}}` | Nombre de chapitres prévus. | « 6 » |
| `{{AUTEUR}}` | Auteur du cours (mentions, crédits, commits). | « Mohamed Amine EL AFRIT » |
| `{{LICENCE}}` | Licence du contenu produit. | « CC BY 4.0 (contenu), MIT (code) » |
| `{{CONTRAINTES}}` | Limites, exclusions, ton, exigences. | « Pas de jargon, hors-ligne, RGAA » |

---

## 5. Démarrage rapide

1. Ouvrez **`PROMPT-Cours-parametrable.md`**, remplissez le bloc de paramètres (laissez vide ce que vous ne savez pas), et demandez à Claude de **créer le cours** depuis le template.
2. Claude amorce le cours (`nouveau_cours.py`), vous fait déposer vos sources, puis pose ses questions **une à une**.
3. Validez chaque jalon « STOP ». Les prompts `01` à `15` servent, phase par phase, à produire chaque livrable.
4. Vérifiez au navigateur à chaque étape, et laissez les vérificateurs dire ce que l'œil ne voit pas.

---

> **Auteur du template :** Mohamed Amine EL AFRIT · Double licence du dépôt : **MIT** pour le code, **CC BY 4.0** pour le contenu et les prompts.
