# Rédaction d'un chapitre

**Quand l'utiliser** : pour rédiger UN chapitre complet du cours, prêt à coller dans une page HTML du template (accroche, objectifs, sections avec encadrés, exemples reliés au fil rouge, termes de glossaire mis en évidence, encadré « À retenir », et — si le cours est bilingue — la version anglaise en parallèle). À lancer une fois par chapitre, après avoir produit le plan d'ensemble et le squelette du site.

---

## Placeholders à compléter

- `{{SUJET_DU_COURS}}` — intitulé global du cours.
- `{{TITRE_DU_CHAPITRE}}` — titre exact du chapitre à rédiger.
- `{{NUMERO_DU_CHAPITRE}}` — numéro/position du chapitre (ex. `3` sur `8`).
- `{{OBJECTIFS_DU_CHAPITRE}}` — 3 à 6 objectifs pédagogiques visés (ce que l'étudiant saura **faire** à la fin). Laisser vide pour que Claude les propose à partir des sources.
- `{{PLAN_DU_CHAPITRE}}` — liste ordonnée des sections attendues (titres). Laisser vide pour que Claude propose un découpage.
- `{{PUBLIC_CIBLE}}` — à qui s'adresse le cours (ex. étudiants L3, professionnels en reconversion).
- `{{NIVEAU}}` — débutant / intermédiaire / avancé.
- `{{DUREE}}` — temps de lecture/d'étude visé pour ce chapitre (ex. 30 min).
- `{{LANGUES}}` — `français seul` **OU** `français + anglais`.
- `{{FIL_ROUGE}}` — scénario continu du cours et son contexte (personnages, organisation, situation) auquel rattacher les exemples.
- `{{DOCUMENTS_DE_REFERENCE}}` — sources faisant autorité à utiliser (textes, normes, articles, supports fournis). Préciser ce qui prime en cas de contradiction.
- `{{GLOSSAIRE}}` — liste des termes du glossaire (FR/EN) à repérer et mettre en évidence dans le texte. Laisser vide si le glossaire n'est pas encore figé.
- `{{CHAPITRES_VOISINS}}` — ce qui précède et ce qui suit (pour les rappels et les transitions), afin d'éviter les répétitions.
- `{{AUTEUR}}` — auteur du cours.
- `{{LICENCE}}` — licence du contenu (ex. CC BY 4.0).
- `{{CONTRAINTES}}` — contraintes éditoriales (longueur, terminologie imposée, ton, interdits, niveau de détail juridique/technique).

---

## PROMPT À COPIER

> ```
> Tu es ingénieur pédagogique et rédacteur expert du sujet. Tu rédiges UN chapitre
> complet d'un cours en ligne, destiné à être collé tel quel dans une page HTML d'un
> template existant. Travaille avec rigueur, clarté et un ton qui motive l'étudiant.
>
> ───────────────────────────────────────────────────────────────────────────
> CONTEXTE
> ───────────────────────────────────────────────────────────────────────────
> - Cours : {{SUJET_DU_COURS}}
> - Chapitre à rédiger : n°{{NUMERO_DU_CHAPITRE}} — « {{TITRE_DU_CHAPITRE}} »
> - Public cible : {{PUBLIC_CIBLE}} — Niveau : {{NIVEAU}} — Durée visée : {{DUREE}}
> - Langues : {{LANGUES}}
> - Fil rouge du cours : {{FIL_ROUGE}}
> - Chapitres voisins (pour transitions et rappels) : {{CHAPITRES_VOISINS}}
> - Objectifs visés : {{OBJECTIFS_DU_CHAPITRE}}
> - Plan attendu : {{PLAN_DU_CHAPITRE}}
> - Termes de glossaire à mettre en évidence : {{GLOSSAIRE}}
> - Auteur : {{AUTEUR}} — Licence du contenu : {{LICENCE}}
> - Contraintes : {{CONTRAINTES}}
>
> ───────────────────────────────────────────────────────────────────────────
> EXIGENCE D'EXACTITUDE (PRIORITÉ ABSOLUE)
> ───────────────────────────────────────────────────────────────────────────
> 1. AVANT de rédiger, analyse en détail les documents de référence ci-dessous et
>    appuie chaque affirmation factuelle dessus. Ne rien inventer.
>    DOCUMENTS DE RÉFÉRENCE : {{DOCUMENTS_DE_REFERENCE}}
> 2. Cite tes sources de façon précise dans le corps du texte (texte + article/section
>    ou page) à l'aide de l'encadré « référence ». En cas de contradiction entre sources,
>    suis la hiérarchie indiquée dans les contraintes, et signale l'écart.
> 3. Si une information manque, est ambiguë ou périmée, NE COMBLE PAS par une supposition :
>    insère un marqueur visible [À VÉRIFIER : …] et explique ce qui manque.
> 4. Distingue clairement le droit/la règle (ce qui est établi) de l'interprétation ou
>    de la bonne pratique (ce qui est recommandé).
> 5. N'invente aucune jurisprudence, aucun chiffre, aucune citation ni aucune référence
>    légale. Pas de source = pas d'affirmation.
>
> ───────────────────────────────────────────────────────────────────────────
> QUALITÉ PÉDAGOGIQUE
> ───────────────────────────────────────────────────────────────────────────
> - Commence par une ACCROCHE motivante (3–5 phrases) : pourquoi ce chapitre compte
>   concrètement pour l'étudiant, ancrée dans une situation du fil rouge.
> - Énonce les OBJECTIFS sous forme « À la fin, vous saurez… » (verbes d'action).
> - Progression logique : du simple au complexe, du concret à l'abstrait. Phrases courtes.
>   Vouvoiement. Jargon expliqué à la première occurrence.
> - Au moins UN exemple concret par section, rattaché explicitement au FIL ROUGE
>   ({{FIL_ROUGE}}) : situation réaliste, décision à prendre, conséquence.
> - Termine chaque section par une micro-transition vers la suivante.
> - Termine le chapitre par un encadré « À RETENIR » : 4 à 6 points clés actionnables.
> - Longueur indicative cohérente avec la durée visée ; reste dense et utile, sans remplissage.
>
> ───────────────────────────────────────────────────────────────────────────
> MISE EN ÉVIDENCE DES TERMES DE GLOSSAIRE
> ───────────────────────────────────────────────────────────────────────────
> À la PREMIÈRE occurrence d'un terme listé dans {{GLOSSAIRE}}, enveloppe-le ainsi :
>   <span class="glossaire" data-terme="cle-du-terme">terme</span>
> où "cle-du-terme" est un identifiant en minuscules-sans-accents-avec-tirets,
> identique à la clé utilisée dans la page glossaire (le template ajoutera l'info-bulle
> automatiquement). N'enveloppe pas chaque occurrence, seulement la première par section.
>
> ───────────────────────────────────────────────────────────────────────────
> BALISAGE HTML ATTENDU PAR LE TEMPLATE (à produire exactement)
> ───────────────────────────────────────────────────────────────────────────
> Produis du HTML sémantique, sans <html>/<head>/<body>, prêt à coller dans la zone de
> contenu du chapitre. Respecte ces patrons :
>
> • Une <section> par partie, avec une ancre id :
>   <section id="ch{{NUMERO_DU_CHAPITRE}}-sX" aria-labelledby="ch{{NUMERO_DU_CHAPITRE}}-sX-titre">
>     <h2 id="ch{{NUMERO_DU_CHAPITRE}}-sX-titre">Titre de la section</h2>
>     <p>…</p>
>   </section>
>   (l'id "-sX" alimente le sous-menu pliable de la navigation latérale ; numérote X de 1 à N.)
>
> • Accroche en tête de chapitre :
>   <p class="accroche">…</p>
>
> • Bloc objectifs :
>   <div class="objectifs">
>     <h2>Objectifs</h2>
>     <ul><li>À la fin, vous saurez …</li> …</ul>
>   </div>
>
> • Encadrés (callouts) — utilise la bonne variante selon le propos :
>   <aside class="callout callout--info">…</aside>      (information, définition, complément)
>   <aside class="callout callout--conseil">…</aside>   (bonne pratique, astuce méthodo)
>   <aside class="callout callout--attention">…</aside> (piège, erreur fréquente, risque)
>   <aside class="callout callout--reference">          (source / citation précise)
>     <p>Source : … (texte, article/section, date/page).</p>
>   </aside>
>   Chaque callout commence par un <strong> de libellé (ex. <strong>Conseil —</strong> …).
>
> • Exemple « fil rouge » :
>   <aside class="callout callout--exemple" data-fil-rouge="1">
>     <strong>Cas fil rouge —</strong> … situation + décision + conséquence …
>   </aside>
>
> • Encadré « À retenir » en fin de chapitre :
>   <div class="a-retenir">
>     <h2>À retenir</h2>
>     <ul><li>…</li> …</ul>
>   </div>
>
> • Terme de glossaire (1re occurrence) :
>   <span class="glossaire" data-terme="cle-du-terme">terme</span>
>
> ───────────────────────────────────────────────────────────────────────────
> GESTION DU BILINGUE  (appliquer SEULEMENT si {{LANGUES}} = « français + anglais »)
> ───────────────────────────────────────────────────────────────────────────
> Le template masque/affiche les langues via l'attribut data-lang sur <html>. Pour CHAQUE
> bloc de texte visible (titres, paragraphes, listes, libellés et contenu des callouts),
> fournis DEUX versions jumelles, dans cet ordre FR puis EN, avec l'attribut data-tr :
>
>   <h2 data-tr="fr">Titre français</h2>
>   <h2 data-tr="en">English title</h2>
>   <p data-tr="fr">Texte français…</p>
>   <p data-tr="en">English text…</p>
>
> Règles bilingues :
> - L'anglais est une TRADUCTION FIDÈLE et professionnelle, pas un résumé : même sens,
>   même niveau de détail, terminologie du domaine en anglais (équivalents reconnus).
> - Les attributs structurels (id, class, data-terme, data-fil-rouge) restent IDENTIQUES
>   sur les deux versions ; seul data-tr change.
> - Pour un terme de glossaire, traduis le texte affiché mais GARDE la même data-terme :
>     <span class="glossaire" data-terme="cle-du-terme" data-tr="fr">terme</span>
>     <span class="glossaire" data-terme="cle-du-terme" data-tr="en">term</span>
> - Si {{LANGUES}} = « français seul » : n'ajoute AUCUN attribut data-tr, rédige en français.
>
> ───────────────────────────────────────────────────────────────────────────
> FORMAT DE SORTIE
> ───────────────────────────────────────────────────────────────────────────
> 1) D'abord, un bloc de code HTML unique contenant tout le chapitre (accroche +
>    objectifs + sections + callouts + À retenir), prêt à coller. Rien d'autre dans ce bloc.
> 2) Ensuite, HORS du bloc de code, une courte note « Sources & points à vérifier » :
>    la liste des références utilisées et la liste des marqueurs [À VÉRIFIER] restants.
> 3) Enfin, la liste des clés data-terme employées, pour contrôle de cohérence avec le glossaire.
>
> Commence maintenant en analysant les documents de référence, puis rédige le chapitre.
> ```

---

## Conseils

- **Une langue à la fois pour la relecture** : générez d'abord le chapitre, puis vérifiez la version FR seule (bascule 🌐) avant de relire l'EN — les erreurs de traduction se voient mieux séparément.
- **Cohérence des clés** : reprenez exactement les `data-terme` du prompt `glossaire` ; une clé qui ne correspond pas = pas d'info-bulle. La liste finale renvoyée par Claude sert de checklist.
- **Numérotation des sections** : gardez `ch{{NUMERO_DU_CHAPITRE}}-sX` séquentiel (s1, s2, …) — c'est ce qui alimente le sous-menu pliable de la navigation latérale.
- **Fil rouge** : exigez au moins un encadré `callout--exemple` par section ; c'est le liant pédagogique entre chapitres et l'atelier.
- **Sources** : si un document de référence manque, lancez quand même le prompt mais attendez-vous à des marqueurs `[À VÉRIFIER]` — ne les supprimez pas sans les traiter.
- **Découpage** : pour un chapitre long, demandez à Claude le plan d'abord (placeholders `OBJECTIFS`/`PLAN` vides), validez, puis relancez section par section pour garder la densité.
- **Réutilisation** : ce balisage (sections à ancres, callouts, `a-retenir`, blocs `data-tr`) est le même pour tous les chapitres — figez-le une fois, gardez-le stable d'un chapitre à l'autre.
