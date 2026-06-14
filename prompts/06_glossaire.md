# 06 — Glossaire bilingue + info-bulles

**Quand l'utiliser**
Une fois le plan du cours et les chapitres rédigés (ou en cours de rédaction), pour produire le glossaire bilingue FR/EN du cours et la liste curatée des termes à **auto-surligner** dans le texte des chapitres (info-bulle au survol reliée à la page glossaire). Le glossaire est l'un des piliers pédagogiques du template : il alimente à la fois la page `glossaire.html` (recherche + filtre alphabétique) et le mécanisme d'info-bulles (`glossaire-data.js` + `glossaire-tooltip.js`).

À lancer **après** la génération des chapitres : on ne peut décider quels termes surligner qu'en connaissant le vocabulaire réellement employé.

---

## Placeholders à compléter

- `{{SUJET_DU_COURS}}` — intitulé exact du cours.
- `{{PUBLIC_CIBLE}}` — à qui s'adresse le cours (ex. étudiants L3, professionnels en reconversion).
- `{{NIVEAU}}` — débutant / intermédiaire / avancé.
- `{{LANGUES}}` — `français seul` **ou** `français + anglais`. Le glossaire est **toujours bilingue FR/EN** dans le template (le terme et la définition EN servent aux info-bulles et à la recherche), même si l'interface est en français : conservez donc la colonne EN dans tous les cas.
- `{{NB_TERMES}}` — nombre **minimum** de termes attendus (ex. `60`). Vise plutôt large : un bon glossaire couvre tout le vocabulaire technique du cours.
- `{{DOCUMENTS_DE_REFERENCE}}` — sources faisant autorité (textes de loi, normes, manuels, supports de cours) à analyser pour définir les termes sans rien inventer.
- `{{FIL_ROUGE}}` — scénario continu du cours (entreprise/cas fictif). Sert à ancrer un **exemple concret** par terme.
- `{{NB_CHAPITRES}}` — nombre de chapitres, pour pouvoir rattacher chaque terme au chapitre où il apparaît.
- `{{CONTENU_DES_CHAPITRES}}` — le texte (ou les fichiers HTML) des chapitres déjà rédigés, indispensable pour curater les termes réellement employés.
- `{{AUTEUR}}` — auteur du cours.
- `{{LICENCE}}` — licence du contenu (ex. CC BY-NC-SA 4.0).
- `{{CONTRAINTES}}` — contraintes spécifiques (terminologie imposée, sigles à privilégier, registre de langue, longueur des définitions…).

---

## PROMPT À COPIER

> ````
> Tu es un·e terminologue pédagogique et expert·e du domaine « {{SUJET_DU_COURS}} ». Tu produis le **glossaire bilingue FR/EN** d'un site de cours et la **liste curatée des termes à auto-surligner** dans les chapitres.
>
> CONTEXTE
> - Cours : {{SUJET_DU_COURS}}
> - Public cible : {{PUBLIC_CIBLE}} — Niveau : {{NIVEAU}}
> - Langues : {{LANGUES}} (le glossaire reste TOUJOURS bilingue FR/EN : terme + définition dans les deux langues).
> - Nombre de chapitres : {{NB_CHAPITRES}}
> - Fil rouge (cas continu du cours) : {{FIL_ROUGE}}
> - Auteur : {{AUTEUR}} — Licence du contenu : {{LICENCE}}
> - Contraintes : {{CONTRAINTES}}
>
> SOURCES À ANALYSER AVANT TOUTE RÉDACTION (exigence d'exactitude)
> - Documents de référence : {{DOCUMENTS_DE_REFERENCE}}
> - Contenu des chapitres déjà rédigés : {{CONTENU_DES_CHAPITRES}}
>
> MÉTHODE — procède dans cet ordre et NE rédige pas avant d'avoir terminé l'étape 1 :
> 1) ANALYSE. Lis attentivement les documents de référence ET le contenu des chapitres. Repère le vocabulaire technique, les sigles/acronymes, les notions clés, les faux-amis et les termes que {{PUBLIC_CIBLE}} risque de mal comprendre. Note, pour chaque terme, le chapitre où il apparaît en premier.
> 2) SÉLECTION. Établis une liste d'AU MOINS {{NB_TERMES}} termes couvrant tout le cours. Inclus : les concepts centraux, les sigles (toujours développés), les institutions/acteurs, les outils/méthodes, et les notions transverses. Évite les mots du langage courant qui n'apportent rien.
> 3) RÉDACTION. Pour chaque terme, produis une fiche complète (voir « STRUCTURE D'UNE FICHE »).
> 4) CURATION. Désigne le sous-ensemble de termes à AUTO-SURLIGNER dans les chapitres (voir « TERMES À AUTO-SURLIGNER »).
> 5) SORTIES. Génère les trois livrables (voir « LIVRABLES »).
>
> STRUCTURE D'UNE FICHE (chaque champ est obligatoire sauf mention contraire)
> - terme_fr : le terme en français (forme canonique ; si c'est un sigle, garder le sigle et développer entre parenthèses).
> - terme_en : l'équivalent anglais consacré (pas une traduction littérale ; le terme officiel/usuel du domaine).
> - def_fr : définition en français, claire, exacte, autoporteuse, 1 à 3 phrases (≈ 30–60 mots). Cite l'article/la norme/la source quand il y en a une.
> - def_en : définition en anglais, équivalente (pas forcément mot à mot), 1 à 2 phrases.
> - exemple : UN exemple concret ancré dans le fil rouge {{FIL_ROUGE}} (1 phrase). Montre le terme « en situation ».
> - chapitre : le chapitre où le terme apparaît en premier (ex. « Ch.3 »). Optionnel si non rattachable.
> - lettre : la première lettre (majuscule, sans accent : É→E) pour le filtre alphabétique.
> - mots_cles : liste de synonymes / variantes / formes fléchies / développé du sigle, en minuscules sans accent superflu, pour la recherche et la résolution des info-bulles (ex. pour « RGPD » : « rgpd reglement general protection donnees gdpr »).
>
> RÈGLES DE QUALITÉ
> - N'invente RIEN. Si une définition n'est pas étayée par les sources, ne l'inclus pas ou signale l'incertitude. Cite tes sources (article de loi, norme, page du manuel) dans def_fr quand c'est pertinent.
> - Définitions neutres, précises, sans jargon inutile ; explique un sigle dès sa première apparition.
> - Les termes EN doivent être les termes RÉELLEMENT employés dans le domaine en anglais (vérifie, ne traduis pas mécaniquement).
> - Trie les fiches par ordre alphabétique du terme_fr (insensible aux accents et à la casse).
> - Cohérence : un même concept = une seule fiche (regroupe les variantes via mots_cles, ne crée pas de doublons).
> - Pas d'exemples hors fil rouge {{FIL_ROUGE}} : l'étudiant doit reconnaître le cas continu du cours.
>
> TERMES À AUTO-SURLIGNER (curation)
> - Sélectionne 30 à 50 termes DISTINCTIFS et à forte valeur pédagogique (concepts centraux, sigles structurants). Ce sont eux qui seront repérés dans le texte des chapitres et munis d'une info-bulle.
> - N'inclus PAS les mots trop courants ou trop génériques (ex. « donnée », « système ») qui surligneraient le texte de façon envahissante.
> - Quand un terme a plusieurs formes fréquentes dans le texte (singulier/pluriel, sigle + forme développée), liste chaque forme : le moteur ne surligne que la 1re occurrence de CHAQUE forme par chapitre.
> - Ordonne la liste curatée des termes les PLUS LONGS aux plus courts (pour que « clauses contractuelles types » soit testé avant « clauses »).
>
> LIVRABLES — produis ces trois blocs, dans cet ordre :
>
> LIVRABLE 1 — Tableau récapitulatif (lisible par un humain), colonnes :
> | Terme FR | Terme EN | Définition FR | Définition EN | Exemple (fil rouge) | Ch. | Auto-surligné ? |
>
> LIVRABLE 2 — Données `glossaire-data.js` (alimente la page glossaire ET les info-bulles).
> Émets EXACTEMENT ce format, prêt à coller dans `assets/js/glossaire-data.js` :
>
> ```js
> /* Données du glossaire — {{SUJET_DU_COURS}} — {{AUTEUR}} ({{LICENCE}}) */
> window.GLOSSARY = [
>   {
>     "fr": "RGPD (Règlement général sur la protection des données)",
>     "en": "GDPR — General Data Protection Regulation (Regulation 2016/679)",
>     "def": "Règlement (UE) 2016/679 encadrant le traitement des données à caractère personnel des personnes situées dans l'UE. EN: EU regulation governing the processing of personal data of individuals in the EU.",
>     "term": "rgpd reglement general protection donnees gdpr 2016/679"
>   }
>   // …une entrée par terme, triées par "fr"
> ];
> ```
> Règles du LIVRABLE 2 :
> - `fr` = terme_fr (sigle développé entre parenthèses si pertinent).
> - `en` = terme_en (forme officielle/consacrée).
> - `def` = def_fr puis, dans la MÊME chaîne, la version anglaise préfixée « EN: » (c'est ce qui s'affiche dans l'info-bulle ; vise ≤ 180 caractères utiles pour la partie visible).
> - `term` = mots_cles concaténés en une seule chaîne minuscule (sigle + forme développée + synonymes), utilisée par la recherche du glossaire et la résolution des info-bulles.
> - JSON valide : guillemets doubles, virgules correctes, échappe les apostrophes/guillemets si besoin, AUCUN commentaire à l'intérieur des objets.
>
> LIVRABLE 3 — Liste curatée pour `glossaire-tooltip.js`.
> Émets le tableau `CURATED` prêt à coller, du terme le plus long au plus court :
>
> ```js
> // Termes auto-surlignés dans les chapitres (info-bulle au survol) — du plus long au plus court
> var CURATED = [
>   'clauses contractuelles types', 'responsable de traitement',
>   'données à caractère personnel', 'consentement', 'RGPD', 'CNIL'
>   // …30 à 50 entrées
> ];
> ```
> Règles du LIVRABLE 3 :
> - Chaque entrée de `CURATED` DOIT correspondre à une fiche du `window.GLOSSARY` (via `fr` ou via `term`), sinon elle ne sera pas reliée.
> - Inclus les variantes utiles (ex. 'donnée personnelle' ET 'données personnelles') si elles apparaissent dans le texte.
> - Termine par une courte note listant les éventuels alias à ajouter au mécanisme (formes du texte qui pointent vers une autre fiche, ex. « données personnelles » → « donnée à caractère personnel »).
>
> CONTRÔLES AVANT DE RENDRE
> - Au moins {{NB_TERMES}} fiches ; toutes bilingues ; toutes avec un exemple fil rouge.
> - `window.GLOSSARY` est du JS valide et parse sans erreur.
> - Chaque terme de `CURATED` est résoluble dans `window.GLOSSARY`.
> - Aucune définition non sourcée ; sigles tous développés ; tri alphabétique respecté.
> - Termine par une ligne « Sources utilisées : … » recensant les références mobilisées.
> ````

---

## Conseils

- **Lance ce prompt après les chapitres.** La qualité de la curation dépend du vocabulaire réellement employé : fournis `{{CONTENU_DES_CHAPITRES}}` aussi complet que possible.
- **Structure de données du template (à respecter à la lettre).** La page `glossaire.html` attend, par entrée, un bloc `.glossary-entry[data-term][data-letter]` contenant : `.entry-fr`, `.entry-en`, `.entry-chapter` (optionnel), un `.entry-def` avec à l'intérieur un `.def-en` (préfixé « EN: »), et un `.entry-example` optionnel avec un libellé `.lbl` (ex. « Exemple {{FIL_ROUGE}} »). Le fichier `assets/js/glossaire-data.js` en est l'image JS : `window.GLOSSARY = [{ fr, en, def, term }]` où `def` regroupe FR + « EN: … » dans une seule chaîne. Si tu modifies les noms de champs, mets à jour les deux fichiers ET `glossaire-tooltip.js`.
- **Info-bulles = `def` tronquée.** Le script n'affiche qu'environ 180 caractères de `def` dans la bulle : place l'essentiel de la définition FR en tête, avant la partie « EN: ».
- **Cohérence chapitres ↔ glossaire.** Tout sigle/terme introduit dans un chapitre devrait avoir sa fiche ; inversement, tout terme `CURATED` doit exister dans `window.GLOSSARY`, sinon l'info-bulle ne se branche pas.
- **Ne sur-surligne pas.** Réserve l'auto-surlignage aux termes distinctifs : un texte truffé de surlignages devient illisible et perd son intérêt pédagogique. 30–50 termes curatés suffisent largement.
- **Accents et tri.** Les `data-letter` et le tri ignorent les accents (É→E). Veille à des `term` en minuscules sans accents superflus pour que la recherche fonctionne au clavier.
- **Régénérer après ajout.** Si tu enrichis le glossaire plus tard, régénère `glossaire-data.js` depuis `glossaire.html` (source de vérité) pour garder les deux synchronisés.
