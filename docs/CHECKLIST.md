# Checklist de production d'un cours

**Quand l'utiliser :** tout au long de la fabrication d'un cours avec ce template, de la première réunion de cadrage jusqu'à la mise en ligne. Coche chaque case au fur et à mesure pour ne rien oublier. Chaque phase doit être validée avant de passer à la suivante.

> Conseils d'usage
> - Travaille **phase par phase** : ne commence pas à rédiger les chapitres tant que le cadrage et le plan ne sont pas validés.
> - Les cases marquées **🔴 bloquant** ne doivent jamais être livrées non cochées : elles conditionnent la qualité pédagogique ou la conformité juridique.
> - Duplique ce fichier dans le dossier de ton cours (ex. `cours-xyz/CHECKLIST.md`) et garde-le sous Git pour suivre l'avancement.
> - Les placeholders communs du template sont rappelés en bas de page.

---

## Phase 0 — Cadrage validé

- [ ] Sujet du cours défini et formulé en une phrase claire — `{{SUJET_DU_COURS}}` 🔴
- [ ] Public cible identifié (profil, prérequis, attentes) — `{{PUBLIC_CIBLE}}`
- [ ] Niveau visé précisé (débutant / intermédiaire / avancé) — `{{NIVEAU}}`
- [ ] Durée totale et volume horaire estimés — `{{DUREE}}`
- [ ] Langue(s) décidée(s) : français seul **ou** français + anglais — `{{LANGUES}}` 🔴
- [ ] Nombre de chapitres arrêté — `{{NB_CHAPITRES}}`
- [ ] Fil rouge (scénario continu de l'atelier) choisi et résumé — `{{FIL_ROUGE}}`
- [ ] Documents de référence rassemblés, lisibles et fiables — `{{DOCUMENTS_DE_REFERENCE}}` 🔴
- [ ] Auteur et licence(s) fixés (code MIT / contenu CC BY 4.0) — `{{AUTEUR}}`, `{{LICENCE}}`
- [ ] Contraintes recensées (techniques, légales, de marque, de temps) — `{{CONTRAINTES}}`
- [ ] Objectifs pédagogiques généraux rédigés (verbes d'action mesurables)
- [ ] **Exigence d'exactitude posée** : Claude doit analyser en détail les documents AVANT de produire, ne rien inventer, citer ses sources 🔴

> ✅ **Jalon :** le cadrage est figé par écrit et relu. On ne passe au plan qu'une fois ce jalon validé.

---

## Phase 1 — Plan du cours

- [ ] Plan détaillé chapitre par chapitre généré à partir des documents de référence
- [ ] Progression pédagogique vérifiée (du simple au complexe, prérequis respectés)
- [ ] Objectifs spécifiques par chapitre formulés
- [ ] Accroche motivante prévue pour chaque chapitre
- [ ] Sections de chaque chapitre listées (elles alimenteront le sous-menu pliable de la navigation)
- [ ] Répartition des contenus médias par chapitre planifiée (podcast / slides / infographie)
- [ ] Emplacement des activités interactives décidé selon le sujet
- [ ] Couverture vérifiée : tous les objectifs du cadrage sont traités, aucun trou, aucun doublon
- [ ] Plan validé avec le commanditaire / l'équipe pédagogique 🔴

> ✅ **Jalon :** plan figé. Toute modification ultérieure du plan implique de revalider la couverture des objectifs.

---

## Phase 2 — Rédaction des chapitres

Pour **chaque** chapitre :

- [ ] Contenu rédigé à partir des seules sources de référence (rien d'inventé) 🔴
- [ ] Sources citées / traçables dans le texte ou en note
- [ ] Accroche motivante en ouverture
- [ ] Objectifs d'apprentissage affichés en début de chapitre
- [ ] Exemples concrets et cas pratiques intégrés
- [ ] Encadré « À retenir » en fin de section/chapitre
- [ ] Ton clair, direct, qui motive l'étudiant
- [ ] Ancres de sections en place (cohérentes avec le sous-menu de navigation)
- [ ] Chapitre relu (orthographe, grammaire, exactitude factuelle, cohérence avec les autres chapitres) 🔴
- [ ] Longueur et densité homogènes d'un chapitre à l'autre

> ✅ **Jalon :** tous les chapitres rédigés ET relus. La relecture est bloquante : pas de chapitre « brouillon » en production.

---

## Phase 3 — Glossaire et info-bulles

- [ ] Glossaire bilingue constitué (terme + définition + exemple, FR/EN)
- [ ] Termes définis sans circularité, alignés sur les sources de référence
- [ ] Auto-surlignage des termes vérifié dans le texte des chapitres
- [ ] Info-bulles au survol testées (affichage, contenu FR/EN, lien vers la page glossaire)
- [ ] Aucun faux positif gênant (sigles, mots courants surlignés à tort) corrigé
- [ ] Cohérence terme ↔ usage : chaque terme du glossaire apparaît bien au moins une fois dans les chapitres

---

## Phase 4 — QCM d'évaluation (CBM)

- [ ] Banque de questions rédigée, à réponse **unique**
- [ ] Notation CBM en place : certitude Élevée +3/−3, Moyenne +2/−2, Faible +1/0
- [ ] Calcul de la note vérifié : `note/20 = score_brut ÷ (3 × nb_questions) × 20`
- [ ] **Positions des bonnes réponses équilibrées** (ex. ~25 %/25 %/25 %/25 %) 🔴
- [ ] **Distracteurs débiaisés** : la bonne réponse n'est jamais systématiquement la plus longue 🔴
- [ ] Difficulté indiquée à titre **indicatif** seulement
- [ ] Modes **Examen** et **Entraînement** testés
- [ ] Export CSV signé en **SHA-256** vérifié (intégrité, fonctionne hors-ligne) 🔴
- [ ] Page de **Correction** testée (dépôt d'un CSV → résultat correct)
- [ ] **Tableau de bord** testé (agrégation de plusieurs CSV)
- [ ] Aucune réponse fausse présentée comme vraie ; corrigé relu 🔴
- [ ] Réponses fondées sur les documents de référence (rien d'inventé)

> ✅ **Jalon :** équilibrage des positions, débiaisage des distracteurs et exactitude du corrigé contrôlés explicitement.

---

## Phase 5 — Flashcards de révision

- [ ] Jeu de flashcards recto/verso par chapitre
- [ ] Bascule « su / à revoir » fonctionnelle
- [ ] Persistance `localStorage` testée (l'état survit au rechargement)
- [ ] Contenu cohérent avec les chapitres et le glossaire

---

## Phase 6 — Activités interactives

- [ ] Patron(s) choisi(s) **selon le sujet** parmi : assistant de décision pas-à-pas, quiz-classificateur à feedback, calculateur/simulateur, checklist à score, fiches-résumés
- [ ] Logique métier de l'activité vérifiée (résultats justes, cas limites gérés)
- [ ] Feedback pédagogique clair à chaque étape
- [ ] Activité bilingue si `{{LANGUES}}` = FR + EN
- [ ] Activité reliée aux objectifs du chapitre concerné

---

## Phase 7 — Atelier « fil rouge »

- [ ] Scénario continu (`{{FIL_ROUGE}}`) décliné sur l'ensemble des chapitres
- [ ] Livrables attendus définis à chaque étape
- [ ] Templates téléchargeables fournis
- [ ] Corrigé formateur rédigé
- [ ] Cohérence narrative et de difficulté vérifiée d'un bout à l'autre

---

## Phase 8 — Polycopiés de synthèse

- [ ] Polycopié par chapitre généré en **DOCX** (python-docx)
- [ ] Polycopié par chapitre généré en **PDF** (fpdf2)
- [ ] Mise en page relue (titres, listes, tableaux, sauts de page)
- [ ] Contenu fidèle aux chapitres (pas de divergence)
- [ ] Mentions d'auteur et de licence présentes dans les documents

---

## Phase 9 — QCM papier imprimable (DOCX)

- [ ] Page de garde présente
- [ ] Consignes claires
- [ ] Barème CBM expliqué **avec exemples**
- [ ] Questions en **2 colonnes**
- [ ] Grille de réponses fournie
- [ ] Corrigé formateur joint
- [ ] Cohérence avec la banque de questions du QCM en ligne vérifiée
- [ ] Rendu d'impression testé (pas de question coupée entre deux pages)

---

## Phase 10 — Médias et intégration NotebookLM

- [ ] Fiche de cours (DOCX) préparée pour NotebookLM
- [ ] Prompts de génération prêts (infographie / slides / podcast par chapitre)
- [ ] **Podcast** déposé par chapitre et lu dans le lecteur audio personnalisé (lecture, ±10 s, mini-lecteur flottant, pop-out, téléchargement) 🔴
- [ ] **Slides PDF** déposées et affichées en popup plein écran
- [ ] **Infographie** déposée et zoomable en lightbox
- [ ] Médias nommés/rangés selon la convention du template (chemins corrects)
- [ ] Médias vérifiés pour exactitude (cohérents avec le contenu, rien d'inventé)

---

## Phase 11 — Accessibilité

- [ ] Panneau de réglages présent et **persistant**
- [ ] Taille du texte ajustable (A+ / A−)
- [ ] Police « lecture adaptée » (Atkinson Hyperlegible) activable pour la dyslexie
- [ ] Lien « aller au contenu » fonctionnel
- [ ] `prefers-reduced-motion` respecté
- [ ] Contrastes de couleurs suffisants (thème via variables CSS)
- [ ] Navigation au clavier possible (focus visible, ordre logique)
- [ ] Alternatives textuelles pour images et infographies

---

## Phase 12 — Responsive et compatibilité

- [ ] Affichage testé sur mobile, tablette et bureau
- [ ] Navigation latérale et sous-menu pliable utilisables sur petit écran
- [ ] Lecteur audio, popups slides et lightbox utilisables au tactile
- [ ] **Fonctionnement hors-ligne** vérifié (aucune dépendance réseau bloquante) 🔴
- [ ] Testé sur au moins deux navigateurs récents
- [ ] Aucune erreur en console (JavaScript vanilla, pas de framework)

---

## Phase 13 — Cohérence bilingue (si FR + EN)

- [ ] Bascule de langue 🌐 fonctionnelle sur **toutes** les pages 🔴
- [ ] Blocs FR/EN présents et appariés partout (pages, navigation, QCM, ateliers, glossaire)
- [ ] Attribut `data-lang` sur `<html>` pilote bien l'affichage
- [ ] Dictionnaire i18n complet pour l'UI générée en JS (aucune chaîne oubliée)
- [ ] Aucun mélange de langues à l'écran dans une langue donnée
- [ ] Parité de contenu FR ↔ EN (rien n'est traduit à moitié ni manquant)

---

## Phase 14 — Licences et attribution

- [ ] Licence du **code** = MIT, fichier `LICENSE` présent 🔴
- [ ] Licence du **contenu et des prompts** = CC BY 4.0, mention présente 🔴
- [ ] Attribution à l'auteur (`{{AUTEUR}}`) visible (pied de page et/ou page dédiée)
- [ ] Sources tierces créditées (textes, images, polices) ; droits d'usage vérifiés
- [ ] Polices Google Fonts conformes à leurs licences
- [ ] Mentions de licence reportées dans les exports (DOCX/PDF) le cas échéant

---

## Phase 15 — Relecture finale et déploiement

- [ ] Relecture globale de bout en bout (parcours étudiant complet)
- [ ] Tous les liens internes et ancres testés (aucun lien mort)
- [ ] Tous les téléchargements testés (podcasts, slides, polycopiés, templates, CSV)
- [ ] Pieds de page propres et cohérents sur toutes les pages
- [ ] Métadonnées de page renseignées (titre, description, langue)
- [ ] Versionné et committé sous Git
- [ ] Déployé (hébergement statique) et URL de production vérifiée 🔴
- [ ] Vérification post-déploiement : site accessible, médias chargés, bascule de langue OK
- [ ] Checklist archivée avec le cours comme preuve de qualité

> ✅ **Jalon final :** parcours étudiant complet rejoué sur l'environnement de production, sans erreur bloquante.

---

### Placeholders communs rappelés

`{{SUJET_DU_COURS}}` · `{{PUBLIC_CIBLE}}` · `{{NIVEAU}}` · `{{DUREE}}` · `{{LANGUES}}` · `{{DOCUMENTS_DE_REFERENCE}}` · `{{FIL_ROUGE}}` · `{{NB_CHAPITRES}}` · `{{AUTEUR}}` · `{{LICENCE}}` · `{{CONTRAINTES}}`

---

*Template de site de cours — Code sous licence MIT, contenu et prompts sous licence CC BY 4.0. Auteur : Mohamed EL AFRIT.*
