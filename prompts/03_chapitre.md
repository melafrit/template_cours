# Rédaction d'un chapitre

**Quand l'utiliser** : pour rédiger UN chapitre complet du cours, dans la langue racine, prêt à coller dans sa page
du template (accroche, objectifs, sections numérotées, encadrés, exemples reliés au fil rouge, conteneurs des
composants, encadré « À retenir »). À lancer une fois par chapitre, après le plan d'ensemble et le squelette du site.
Les autres langues viennent ensuite, page par page, une fois la racine stable (module `01-langues.md`).

---

## Placeholders à compléter

- `{{SUJET_DU_COURS}}` : intitulé global du cours.
- `{{TITRE_DU_CHAPITRE}}` : titre exact du chapitre à rédiger.
- `{{NUMERO_DU_CHAPITRE}}` : numéro du chapitre et sa place (ex. `3` sur `8`).
- `{{OBJECTIFS_DU_CHAPITRE}}` : 3 à 6 objectifs pédagogiques visés (ce que l'étudiant saura **faire** à la fin).
  Laisser vide pour que Claude les propose à partir des sources.
- `{{PLAN_DU_CHAPITRE}}` : liste ordonnée des sections attendues (titres). Laisser vide pour que Claude propose un
  découpage.
- `{{PUBLIC_CIBLE}}` : à qui s'adresse le cours, par ses prérequis et ses contraintes.
- `{{NIVEAU}}` : débutant, intermédiaire ou avancé.
- `{{DUREE}}` : temps de lecture et d'étude visé pour ce chapitre (ex. 30 min) ; il vient du référentiel
  (`DUREES`), pas d'une page.
- `{{LANGUE_RACINE}}` : la langue du chapitre, la première de `cours.langues` (`fr` ou `en`).
- `{{FIL_ROUGE}}` : scénario continu du cours et son contexte (personnages, organisation, situation) auquel
  rattacher les exemples.
- `{{FILIERES}}` : les filières du cours, s'il en a deux, pour les exemples propres à chacune.
- `{{DOCUMENTS_DE_REFERENCE}}` : sources qui font autorité (textes, normes, articles, supports fournis), et ce qui
  prime en cas de contradiction.
- `{{GLOSSAIRE}}` : les termes du glossaire déjà fixés, pour les employer tels quels. Laisser vide si le glossaire
  n'est pas encore figé.
- `{{CHAPITRES_VOISINS}}` : ce qui précède et ce qui suit, pour les rappels et les transitions, sans répétition.
- `{{CONTRAINTES}}` : contraintes éditoriales (longueur, terminologie imposée, ton, interdits, niveau de détail).

---

## PROMPT À COPIER

> ```
> Tu es ingénieur pédagogique et rédacteur expert du sujet. Tu rédiges UN chapitre
> complet d'un cours en ligne, à coller dans sa page du template. Travaille avec rigueur,
> clarté, et un ton qui motive l'étudiant.
>
> ───────────────────────────────────────────────────────────────────────────
> CONTEXTE
> ───────────────────────────────────────────────────────────────────────────
> - Cours : {{SUJET_DU_COURS}}
> - Chapitre à rédiger : n° {{NUMERO_DU_CHAPITRE}}, « {{TITRE_DU_CHAPITRE}} »
> - Public cible : {{PUBLIC_CIBLE}} ; niveau : {{NIVEAU}} ; durée visée : {{DUREE}}
> - Langue du chapitre : {{LANGUE_RACINE}}
> - Fil rouge du cours : {{FIL_ROUGE}}
> - Filières : {{FILIERES}}
> - Chapitres voisins (pour les transitions et les rappels) : {{CHAPITRES_VOISINS}}
> - Objectifs visés : {{OBJECTIFS_DU_CHAPITRE}}
> - Plan attendu : {{PLAN_DU_CHAPITRE}}
> - Termes du glossaire déjà fixés : {{GLOSSAIRE}}
> - Contraintes : {{CONTRAINTES}}
>
> ───────────────────────────────────────────────────────────────────────────
> EXIGENCE D'EXACTITUDE (PRIORITÉ ABSOLUE)
> ───────────────────────────────────────────────────────────────────────────
> 1. AVANT de rédiger, analyse en détail les documents de référence et appuie chaque
>    affirmation factuelle dessus. N'invente rien.
>    DOCUMENTS DE RÉFÉRENCE : {{DOCUMENTS_DE_REFERENCE}}
> 2. Cite tes sources avec précision (texte, article ou section, page). En cas de
>    contradiction entre sources, suis la hiérarchie des contraintes et signale l'écart.
> 3. Si une information manque, est ambiguë ou périmée, NE COMBLE PAS par une supposition :
>    insère un marqueur visible [À VÉRIFIER : …] qui dit ce qui manque.
> 4. Distingue la règle (ce qui est établi) de l'interprétation ou de la bonne pratique
>    (ce qui est recommandé).
> 5. N'invente aucune jurisprudence, aucun chiffre, aucune citation ni aucune référence.
>    Pas de source, pas d'affirmation.
> 6. Aucun chiffre du cas écrit à la main : il vient du référentiel (outils/referentiel.py),
>    et la page marque sa place par un fragment, <!-- FRAGMENT:nom -->…<!-- /FRAGMENT:nom -->,
>    que outils/generer_fragments.py remplit. Donne la liste des fragments employés.
> 7. Rien ne souffle une réponse : un exemple de méthode porte sur un cas neutre, jamais
>    sur le sujet du TP ni sur celui d'une épreuve (outils/interdits.py).
>
> ───────────────────────────────────────────────────────────────────────────
> QUALITÉ PÉDAGOGIQUE
> ───────────────────────────────────────────────────────────────────────────
> - Commence par une ACCROCHE motivante (3 à 5 phrases) : pourquoi ce chapitre compte
>   concrètement pour l'étudiant, ancrée dans une situation du fil rouge.
> - Énonce les OBJECTIFS avec des verbes d'action observables (« À la fin, vous saurez… »).
> - Progression logique, du simple au complexe et du concret à l'abstrait ; phrases
>   courtes ; vouvoiement ; tout jargon expliqué à sa première apparition.
> - Au moins UN exemple concret par section, rattaché au fil rouge : une situation
>   réaliste, une décision à prendre, sa conséquence. Quand l'exemple diffère d'une filière
>   à l'autre, une version par filière.
> - Une notion difficile se vérifie par un point de contrôle, dont chaque proposition est
>   expliquée (pourquoi la bonne réponse est juste, pourquoi chacune des autres ne l'est
>   pas), avec deux à quatre renvois « Pour approfondir » (prompts/15_explications_quiz.md).
> - Tout schéma a sa lecture élément par élément, pour un débutant : ce qu'il montre,
>   comment le lire, chaque élément et son rôle, ses liens, le piège à éviter.
> - Une capsule audio ouvre le chapitre, et une autre le début de chaque section (décision
>   de l'auteur du 21 novembre 2026). Laisse leurs conteneurs ; leurs scripts s'écrivent
>   ensuite, dans la fiche des capsules (prompts/14_capsules_audio.md).
> - Termine chaque section par une transition brève vers la suivante, et le chapitre par
>   l'encadré « À retenir » : 4 à 6 points clés, actionnables.
> - Longueur cohérente avec la durée visée ; dense et utile, sans remplissage.
>
> ───────────────────────────────────────────────────────────────────────────
> STYLE ET TYPOGRAPHIE
> ───────────────────────────────────────────────────────────────────────────
> - Ni tiret cadratin ni tiret demi-cadratin entre espaces : une incise passe entre virgules ou entre
>   parenthèses, ou devient une phrase. Un titre prend le deux-points, le point médian ou
>   les parenthèses (« Chapitre 1 · Bienvenue »).
> - Aucune marque de texte généré : un seul deux-points par phrase, ni phrase-choc sans
>   verbe, ni questions rhétoriques en cascade, ni antithèse réflexe, ni triade par
>   habitude, ni mot gonflé (« crucial », « véritable », « au cœur de »).
> - En français, une espace insécable avant « : ; ? ! » et à l'intérieur des guillemets
>   « ». Aucune date fixe : « Jour 1 », « séance 2 ».
>
> ───────────────────────────────────────────────────────────────────────────
> LE GLOSSAIRE
> ───────────────────────────────────────────────────────────────────────────
> Ne balise aucun terme : le moteur (glossaire-tooltip.js) repère lui-même la première
> occurrence de chaque terme du glossaire, d'après glossaire-data.js. Emploie les termes
> déjà fixés tels quels, et donne en fin de réponse les termes nouveaux du chapitre, avec
> une définition courte, pour glossaire-data.js.
>
> ───────────────────────────────────────────────────────────────────────────
> LE BALISAGE : CELUI DU CHAPITRE VITRINE
> ───────────────────────────────────────────────────────────────────────────
> Le seul modèle est le chapitre vitrine (site/chapitres/_modele.html dans un cours créé,
> site/chapitres/01-cadrage.html dans le gabarit) : copie sa structure, n'écris rien de
> mémoire. Produis le contenu de <main>, sans <html>, <head> ni <body>, sur ces patrons :
>
> • Une section par partie, son titre numéroté avec une ancre :
>   <section class="content-section" data-sommaire-titre="Titre court">
>     <h2 id="ch{{NUMERO_DU_CHAPITRE}}-s1"><span>1. Titre de la section</span></h2>
>     <p class="lead">…</p>
>     <p>…</p>
>   </section>
>   Les id ch{{NUMERO_DU_CHAPITRE}}-s1, -s2… se suivent : le menu de gauche en tire les
>   sections du chapitre (outils/generer_nav_sections.py).
>
> • Un encadré, dans la variante qui convient (info, tip, warning, danger, legal) :
>   <div class="callout info">
>     <div class="callout-icon">💡</div>
>     <div class="callout-content"><h4>Libellé</h4><p>…</p></div>
>   </div>
>
> • Un exemple propre à une filière, quand il diffère :
>   <div class="exemple-filiere only-<id de la filière>">…</div>
>
> • Les conteneurs des composants, vides, nommés comme dans la vitrine :
>   <div id="capsule-{{NUMERO_DU_CHAPITRE}}"></div>, <div id="check-{{NUMERO_DU_CHAPITRE}}-1"></div>,
>   <div id="schema-{{NUMERO_DU_CHAPITRE}}-1"></div>… Leur contenu va dans l'objet TEXTES de
>   la page (voir plus bas).
>
> • L'encadré « À retenir », en fin de chapitre :
>   <div class="takeaways">
>     <div class="takeaways-head"><span class="ico">🔑</span><h3>À retenir</h3></div>
>     <div class="takeaways-body"><ul><li>…</li></ul></div>
>   </div>
>
> ───────────────────────────────────────────────────────────────────────────
> LES LANGUES
> ───────────────────────────────────────────────────────────────────────────
> Écris le chapitre dans sa langue racine seulement. Ses jumelles (en/, ar/) viennent
> plus tard, une fois la racine stable : outils/creer_jumelle.py prépare chacune, avec la
> même suite de blocs, puis elle se traduit bloc pour bloc (prompts/modules/01-langues.md).
> N'ajoute aucun attribut data-tr : ce modèle ne se crée plus.
>
> ───────────────────────────────────────────────────────────────────────────
> FORMAT DE SORTIE
> ───────────────────────────────────────────────────────────────────────────
> 1) Un bloc de code HTML unique, tout le chapitre (accroche, objectifs, sections,
>    encadrés, conteneurs, « À retenir »), prêt à coller. Rien d'autre dans ce bloc.
> 2) Hors du bloc, une note « Sources et points à vérifier » : les références employées
>    et les marqueurs [À VÉRIFIER] restants.
> 3) La liste des fragments employés, des conteneurs de composants à remplir, et des termes
>    nouveaux pour le glossaire.
>
> Commence par analyser les documents de référence, puis rédige le chapitre.
> ```

---

## Le moteur pédagogique, à utiliser plutôt qu'à réinventer

Un chapitre du template n'est pas qu'un texte. `window.RDCX` fournit sept composants, tous appelés pour de vrai dans
le chapitre vitrine : **copiez depuis là plutôt que d'écrire de mémoire.**

| Composant | Quand l'employer |
|---|---|
| `reveal` | Poser une question AVANT la lecture, pour créer l'attente |
| `checkpoint` | Vérifier après une notion difficile, chaque proposition expliquée |
| `spotError` | Faire relire un document d'un œil critique |
| `match` | Relier deux séries de notions |
| `branch` | Montrer les conséquences d'une décision |
| `hotspots` | Annoter un schéma de points cliquables |
| `voice` | Une capsule audio, avec sa transcription : à l'ouverture du chapitre et au début de chaque section |

**Choisissez selon l'intention, pas selon la nouveauté.** Un `checkpoint` après une notion difficile vaut mieux qu'un
`branch` plaqué là où rien ne se décide. Deux à quatre composants par chapitre suffisent : la vitrine les a tous parce
qu'elle les démontre.

**Ni barre d'étapes ni sommaire dans la page.** Le chapitre se lit d'un bout à l'autre ; ses sections sont les
sous-entrées du chapitre dans le menu de gauche (`nav-sections.js`, régénéré par `outils/generer_nav_sections.py`
d'après les `<h2 id>`). Les composants `RDCX.steps` et `RDCX.sommaire` restent dans le moteur, mais ne s'appellent
plus par défaut : les étudiants trouvaient la page encombrée par deux navigations qui doublaient le menu.

**Tout le contenu des composants passe par un objet `TEXTES`**, avec une entrée par langue et une fonction `monter()`
rejouée sur `tpl:langchange`, comme dans la vitrine. Chaque page y prend sa propre langue.

## Conseils

- **Relisez au navigateur**, dans la langue racine, en clair et en sombre, à 1280 et 375 px, la console vide ; la
  jumelle se relit à son tour quand elle existe.
- **Le glossaire** : comparez les termes nouveaux que rend Claude à `glossaire-data.js` ; un terme absent de la liste
  des termes repérés n'a pas d'info-bulle.
- **Les sections** : gardez les ancres `ch{{NUMERO_DU_CHAPITRE}}-sX` dans l'ordre (s1, s2…), puis relancez
  `python3 outils/generer_nav_sections.py` ; son `--essai` dit si le menu suit les pages.
- **Les chiffres** : relancez `python3 outils/generer_fragments.py` après le collage ; son `--essai` dit s'il manque
  une valeur au référentiel.
- **Le fil rouge** : exigez au moins un exemple relié au cas par section ; c'est le lien entre les chapitres et
  l'atelier.
- **Les sources** : si un document manque, lancez quand même le prompt, mais traitez chaque marqueur
  `[À VÉRIFIER]` avant de publier, sans jamais le supprimer d'office.
- **Le découpage** : pour un chapitre long, demandez d'abord le plan (`OBJECTIFS` et `PLAN` vides), validez-le, puis
  rédigez section par section pour garder la densité.
- **Les contrôles** : `python3 outils/verifier_tirets.py`, `verifier_liens.py` et `verifier_interdits.py` sans écart
  avant de déclarer le chapitre fini.
