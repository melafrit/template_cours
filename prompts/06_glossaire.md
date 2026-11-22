# 06 · Glossaire bilingue + info-bulles

**Quand l'utiliser**
Une fois le plan du cours et les chapitres rédigés (ou en cours de rédaction), pour produire le glossaire bilingue FR/EN du cours et la liste curatée des termes à **auto-surligner** dans le texte des chapitres (info-bulle au survol reliée à la page glossaire). Le glossaire est l'un des piliers pédagogiques du template : il alimente à la fois la page `glossaire.html` (cartes et recherche) et le mécanisme d'info-bulles (`glossaire-data.js` + `glossaire-tooltip.js`).

À lancer **après** la génération des chapitres : on ne peut décider quels termes surligner qu'en connaissant le vocabulaire réellement employé.

---

## Placeholders à compléter

- `{{SUJET_DU_COURS}}` : intitulé exact du cours.
- `{{PUBLIC_CIBLE}}` : à qui s'adresse le cours (ex. étudiants L3, professionnels en reconversion).
- `{{NIVEAU}}` : débutant / intermédiaire / avancé.
- `{{LANGUES}}` : les langues du cours, la racine d'abord (`cours.langues`, par exemple `["fr"]` ou `["fr", "en"]`). Le glossaire est **toujours bilingue FR/EN** dans le template, même dans un cours en français seul : le terme anglais s'affiche sous le terme français, dans la page comme dans la bulle, et la recherche le lit. Conservez donc la colonne EN dans tous les cas ; les définitions et les exemples anglais servent aux jumelles anglaises, et l'arabe, s'il est au programme, s'ajoute avec sa jumelle (`prompts/modules/01-langues.md`).
- `{{NB_TERMES}}` : nombre **minimum** de termes attendus (ex. `60`). Vise plutôt large : un bon glossaire couvre tout le vocabulaire technique du cours.
- `{{DOCUMENTS_DE_REFERENCE}}` : sources faisant autorité (textes de loi, normes, manuels, supports de cours) à analyser pour définir les termes sans rien inventer.
- `{{FIL_ROUGE}}` : scénario continu du cours (entreprise/cas fictif). Sert à ancrer un **exemple concret** par terme.
- `{{NB_CHAPITRES}}` : nombre de chapitres, pour pouvoir rattacher chaque terme au chapitre où il apparaît.
- `{{CONTENU_DES_CHAPITRES}}` : le texte (ou les fichiers HTML) des chapitres déjà rédigés, indispensable pour curater les termes réellement employés.
- `{{AUTEUR}}` : auteur du cours.
- `{{LICENCE}}` : licence du contenu (ex. CC BY-NC-SA 4.0).
- `{{CONTRAINTES}}` : contraintes spécifiques (terminologie imposée, sigles à privilégier, registre de langue, longueur des définitions…).

---

## PROMPT À COPIER

> ````
> Tu es un·e terminologue pédagogique et expert·e du domaine « {{SUJET_DU_COURS}} ». Tu produis le **glossaire bilingue FR/EN** d'un site de cours et la **liste curatée des termes à auto-surligner** dans les chapitres.
>
> CONTEXTE
> - Cours : {{SUJET_DU_COURS}}
> - Public cible : {{PUBLIC_CIBLE}} ; niveau : {{NIVEAU}}
> - Langues : {{LANGUES}} (le glossaire reste TOUJOURS bilingue FR/EN ; terme, définition et exemple s'écrivent dans les deux langues).
> - Nombre de chapitres : {{NB_CHAPITRES}}
> - Fil rouge (cas continu du cours) : {{FIL_ROUGE}}
> - Auteur : {{AUTEUR}} ; licence du contenu : {{LICENCE}}
> - Contraintes : {{CONTRAINTES}}
>
> SOURCES À ANALYSER AVANT TOUTE RÉDACTION (exigence d'exactitude)
> - Documents de référence : {{DOCUMENTS_DE_REFERENCE}}
> - Contenu des chapitres déjà rédigés : {{CONTENU_DES_CHAPITRES}}
>
> MÉTHODE (procède dans cet ordre, et NE rédige pas avant d'avoir terminé l'étape 1)
> 1) ANALYSE. Lis attentivement les documents de référence ET le contenu des chapitres. Repère le vocabulaire technique, les sigles/acronymes, les notions clés, les faux-amis et les termes que {{PUBLIC_CIBLE}} risque de mal comprendre. Note, pour chaque terme, le chapitre où il apparaît en premier.
> 2) SÉLECTION. Établis une liste d'AU MOINS {{NB_TERMES}} termes couvrant tout le cours. Inclus : les concepts centraux, les sigles (toujours développés), les institutions/acteurs, les outils/méthodes, et les notions transverses. Évite les mots du langage courant qui n'apportent rien.
> 3) RÉDACTION. Pour chaque terme, produis une fiche complète (voir « STRUCTURE D'UNE FICHE »).
> 4) CURATION. Désigne le sous-ensemble de termes à AUTO-SURLIGNER dans les chapitres (voir « TERMES À AUTO-SURLIGNER »).
> 5) SORTIES. Génère les trois livrables (voir « LIVRABLES »).
>
> STRUCTURE D'UNE FICHE (chaque champ est obligatoire sauf mention contraire)
> - terme_fr : le terme en français (forme canonique ; si c'est un sigle, garder le sigle et développer entre parenthèses).
> - terme_en : l'équivalent anglais consacré (pas une traduction littérale ; le terme officiel/usuel du domaine).
> - def_fr : définition en français, claire, exacte, autoporteuse, 1 à 3 phrases (environ 30 à 60 mots). Cite l'article/la norme/la source quand il y en a une.
> - def_en : définition en anglais, équivalente (pas forcément mot à mot), 1 à 2 phrases.
> - exemple : UN exemple concret ancré dans le fil rouge {{FIL_ROUGE}} (1 phrase), en français et en anglais. Montre le terme « en situation ».
> - chapitre : le chapitre où le terme apparaît en premier (ex. « Ch.3 »). Optionnel si non rattachable.
> - alias (facultatif) : les autres formes du terme, langue par langue (synonyme, sigle ou forme développée), sans les pluriels réguliers du français et de l'anglais, que les outils déduisent seuls. « Où en parle-t-on ? » les compte, et une page anglaise y cherche ses info-bulles (ex. pour « RGPD », en français, « règlement général sur la protection des données »).
>
> RÈGLES DE QUALITÉ
> - N'invente RIEN. Si une définition n'est pas étayée par les sources, ne l'inclus pas ou signale l'incertitude. Cite tes sources (article de loi, norme, page du manuel) dans def_fr quand c'est pertinent.
> - Définitions neutres, précises, sans jargon inutile ; explique un sigle dès sa première apparition.
> - Les termes EN doivent être les termes RÉELLEMENT employés dans le domaine en anglais (vérifie, ne traduis pas mécaniquement).
> - Trie les fiches par ordre alphabétique du terme_fr (insensible aux accents et à la casse).
> - Cohérence : un même concept = une seule fiche (regroupe les variantes via alias, ne crée pas de doublons).
> - Pas d'exemples hors fil rouge {{FIL_ROUGE}} : l'étudiant doit reconnaître le cas continu du cours.
> - Ni tiret cadratin ni tiret demi-cadratin entre espaces (une incise passe entre virgules ou entre parenthèses), aucune marque de texte généré ; en français, une espace insécable avant « : ; ? ! » et à l'intérieur des guillemets « ».
>
> TERMES À AUTO-SURLIGNER (curation)
> - Sélectionne 30 à 50 termes DISTINCTIFS et à forte valeur pédagogique (concepts centraux, sigles structurants). Ce sont eux qui seront repérés dans le texte des chapitres et munis d'une info-bulle.
> - N'inclus PAS les mots trop courants ou trop génériques (ex. « donnée », « système ») qui surligneraient le texte de façon envahissante.
> - Quand un terme a plusieurs formes fréquentes dans le texte (singulier/pluriel, sigle + forme développée), liste chaque forme : le moteur ne surligne que la 1re occurrence de CHAQUE forme par chapitre.
> - L'ordre de la liste est libre : le moteur essaie lui-même les formes les plus longues d'abord (« clauses contractuelles types » avant « clauses »).
>
> LIVRABLES (produis ces trois blocs, dans cet ordre)
>
> LIVRABLE 1 · Tableau récapitulatif (lisible par un humain), colonnes :
> | Terme FR | Terme EN | Définition FR | Définition EN | Exemple (fil rouge) | Ch. | Auto-surligné ? |
>
> LIVRABLE 2 · Données `glossaire-data.js` (alimente la page glossaire ET les info-bulles).
> Émets EXACTEMENT ce format, prêt à coller dans `assets/js/glossaire-data.js` :
>
> ```js
> /* Données du glossaire : {{SUJET_DU_COURS}}, {{AUTEUR}} ({{LICENCE}}) */
> window.GLOSSARY = [
>   { fr: "RGPD (Règlement général sur la protection des données)",
>     en: "GDPR (General Data Protection Regulation, Regulation 2016/679)",
>     def: { fr: "Règlement (UE) 2016/679 encadrant le traitement des données à caractère personnel des personnes situées dans l'UE.",
>            en: "EU regulation governing the processing of personal data of individuals in the EU." },
>     ex: { fr: "…", en: "…" },
>     alias: { fr: ["règlement général sur la protection des données"] } }
>   /* …une entrée par terme, triées par fr */
> ];
> ```
> Règles du LIVRABLE 2 :
> - `fr` = terme_fr (sigle développé entre parenthèses si pertinent).
> - `en` = terme_en (forme officielle/consacrée).
> - `def` = { fr: def_fr, en: def_en }. L'info-bulle n'en montre que 180 caractères, dans la langue de la page : place l'essentiel en tête.
> - `ex` = { fr, en } : l'exemple, dans les deux langues.
> - `alias` = { fr: [...], en: [...] }, seulement pour un terme qui en a.
> - `exclus` (facultatif) = { fr: [...], en: [...] } : les expressions où le mot ne désigne pas la notion (« mise en service »), réglées avec le prompt `06b`.
> - Le tableau se lit comme du JSON (`outils/glossaire_emplois.py` et le polycopié le lisent ainsi) : chaînes entre guillemets doubles, apostrophes telles quelles, virgules correctes, AUCUN commentaire `//` (un commentaire `/* */` passe).
>
> LIVRABLE 3 · Liste curatée pour `glossaire-tooltip.js`, à la fin de `glossaire-data.js`.
> Émets le tableau `window.GLOSSARY_CURATED` prêt à coller, puis l'objet `window.GLOSSARY_ALIASES` :
>
> ```js
> /* Termes auto-surlignés dans les chapitres (info-bulle au survol) */
> window.GLOSSARY_CURATED = [
>   "clauses contractuelles types", "responsable de traitement",
>   "données à caractère personnel", "consentement", "RGPD", "CNIL"
>   /* …30 à 50 entrées */
> ];
> /* Formes de la liste qui ne se rattachent pas d'elles-mêmes à leur fiche */
> window.GLOSSARY_ALIASES = {
>   "données à caractère personnel": "donnée à caractère personnel"
> };
> ```
> Règles du LIVRABLE 3 :
> - Chaque entrée de `GLOSSARY_CURATED` DOIT correspondre à une fiche du `window.GLOSSARY` (par son `fr`, sans la parenthèse, ou par `GLOSSARY_ALIASES`), sinon elle ne sera pas reliée.
> - Inclus les variantes utiles (ex. 'donnée personnelle' ET 'données personnelles') si elles apparaissent dans le texte : sur une page française, le moteur ne cherche que les formes de la liste.
> - Dans `GLOSSARY_ALIASES`, relie au `fr` de sa fiche (en minuscules, sans la parenthèse) chaque forme de la liste qui pointe vers une autre fiche (ex. « données personnelles » → « donnée à caractère personnel »).
>
> CONTRÔLES AVANT DE RENDRE
> - Au moins {{NB_TERMES}} fiches ; toutes bilingues ; toutes avec un exemple fil rouge.
> - `window.GLOSSARY` est du JS valide et se lit comme du JSON, sans erreur.
> - Chaque terme de `GLOSSARY_CURATED` est résoluble dans `window.GLOSSARY`.
> - Aucune définition non sourcée ; sigles tous développés ; tri alphabétique respecté.
> - Termine par une ligne « Sources utilisées : … » recensant les références mobilisées.
> ````

---

## Conseils

- **Lance ce prompt après les chapitres.** La qualité de la curation dépend du vocabulaire réellement employé : fournis `{{CONTENU_DES_CHAPITRES}}` aussi complet que possible.
- **Structure de données du template (à respecter à la lettre).** La page `glossaire.html` n'a aucun terme écrit à la main : son script dessine une carte par entrée de `window.GLOSSARY`, dans l'ordre du tableau (terme, équivalent dans l'autre langue, définition, exemple, « Où en parle-t-on ? »), avec son ancre `#g-…`, que vise l'info-bulle. `assets/js/glossaire-data.js` est donc la seule source : `window.GLOSSARY = [{ fr, en, def: { fr, en }, ex: { fr, en }, alias?, exclus? }]`, puis `GLOSSARY_CURATED` et `GLOSSARY_ALIASES`. Si tu modifies les noms de champs, mets à jour tous ses lecteurs : `glossaire.html`, `glossaire-tooltip.js`, `outils/glossaire_emplois.py` et le polycopié (`outils/polycopie/sources.py`).
- **Info-bulles = `def` tronquée.** Le script n'affiche que 180 caractères de la définition, dans la langue de la page : place l'essentiel en tête.
- **Cohérence chapitres ↔ glossaire.** Tout sigle/terme introduit dans un chapitre devrait avoir sa fiche ; inversement, tout terme de `GLOSSARY_CURATED` doit se rattacher à une fiche de `window.GLOSSARY`, sinon l'info-bulle ne se branche pas.
- **Ne sur-surligne pas.** Réserve l'auto-surlignage aux termes distinctifs : un texte truffé de surlignages devient illisible et perd son intérêt pédagogique. 30 à 50 termes curatés suffisent largement.
- **Accents et tri.** La recherche de la page ignore la casse et les accents, sur le terme français comme sur le terme anglais ; la page garde l'ordre du tableau, d'où le tri alphabétique des fiches.
- **Régénérer après ajout.** `glossaire-data.js` reste la seule source, que lisent la page et les info-bulles : après un ajout, relance `python3 outils/glossaire_emplois.py`, qui recalcule « Où en parle-t-on ? » (prompt `06b`).
