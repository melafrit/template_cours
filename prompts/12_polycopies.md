# Polycopiés de synthèse (DOCX + PDF)

> **Un livret complet plutôt qu'un polycopié par chapitre ?** Le module
> [`modules/02-polycopie.md`](modules/02-polycopie.md) produit le livre entier du cours
> (page de garde, mini-sommaires, QR codes cliquables vers le site, glossaire, index), en
> Word et en PDF, avec sa page sur le site. Ce prompt-ci reste pour des synthèses courtes,
> chapitre par chapitre.

**Quand l'utiliser** : une fois les chapitres rédigés et stabilisés. Ce prompt génère, **par chapitre**, un polycopié de synthèse académique (mini-sommaire, encadrés colorés, tableau récapitulatif, « à retenir ») ; son contenu va dans `tools/polycopies_content.json`, que le script du gabarit, `tools/generate_polycopies.py`, exporte simultanément en **DOCX** *et* **PDF**. Les polycopiés sont les documents que l'étudiant imprime, annote et révise hors écran ; ils doivent rester strictement cohérents avec le contenu du site.

---

## Placeholders à compléter

- `{{SUJET_DU_COURS}}` : intitulé exact du cours.
- `{{PUBLIC_CIBLE}}` : à qui s'adresse le cours.
- `{{NIVEAU}}` : débutant / intermédiaire / avancé.
- `{{LANGUES}}` : *français seul* OU *français + anglais* (les deux langues que connaît le script). Détermine s'il faut produire une version EN de chaque polycopié.
- `{{NB_CHAPITRES}}` : nombre de chapitres à traiter (ou « tous »).
- `{{LISTE_CHAPITRES}}` : titres + numéros des chapitres concernés.
- `{{DOCUMENTS_DE_REFERENCE}}` : chemins/URL des fichiers HTML des chapitres déjà produits + sources primaires (la **source de vérité**).
- `{{FIL_ROUGE}}` : scénario continu du cours (ex. une coopérative agricole fictive qui numérise ses ventes), à rappeler dans les exemples.
- `{{AUTEUR}}` : auteur, que le pied de page imprime ; le script l'écrit lui-même (`LABELS` de `tools/generate_polycopies.py`), à vérifier plutôt qu'à saisir.
- `{{LICENCE}}` : licence du contenu (ex. CC BY 4.0), dans le même pied de page.
- `{{COULEURS_THEME}}` : couleurs du thème du site (primaire, secondaire, accent) en hexadécimal, seulement pour retoucher la charte du script (bleu nuit et doré, une couleur par type d'encadré). Ex. `#1A3A5A`, `#0E7C66`, `#C8442B`.
- `{{POLICE_TITRES}}` / `{{POLICE_TEXTE}}` : polices à imiter, pour la même retouche (le script emploie Calibri pour le DOCX, Arial pour le PDF).
- `{{CONTRAINTES}}` : contraintes spécifiques (longueur max par chapitre, charte graphique de l'établissement, accessibilité, etc.).

---

## PROMPT À COPIER

> ```
> RÔLE
> Tu es ingénieur pédagogique et secrétaire de rédaction. Tu produis des polycopiés de synthèse imprimables, fidèles au contenu existant, pour le cours « {{SUJET_DU_COURS}} ».
>
> EXIGENCE D'EXACTITUDE (NON NÉGOCIABLE)
> 1. Avant toute rédaction, ANALYSE EN DÉTAIL les documents de référence : {{DOCUMENTS_DE_REFERENCE}}.
> 2. Le polycopié est une SYNTHÈSE FIDÈLE du chapitre correspondant : n'introduis AUCUNE notion, définition, chiffre, date, article de loi ou exemple qui ne figure pas déjà dans le chapitre ou ses sources primaires.
> 3. N'invente rien. Si une information manque pour compléter un bloc, écris « [À COMPLÉTER : … ] » plutôt que d'inventer.
> 4. Cite tes sources : chaque affirmation factuelle sensible (chiffre, texte de loi, jurisprudence, norme) renvoie à sa source dans la liste de références en fin de polycopié.
> 5. Réutilise EXACTEMENT la terminologie du glossaire du cours : mêmes termes, mêmes définitions.
>
> PUBLIC / NIVEAU / LANGUES
> - Public : {{PUBLIC_CIBLE}} ; niveau : {{NIVEAU}}.
> - Langues : {{LANGUES}}.
>   • Si « français seul » : produis un seul jeu de polycopiés en français ; le script se lance alors avec l'argument fr.
>   • Si « français + anglais » : produis pour CHAQUE chapitre une version FR et une version EN, fidèles l'une à l'autre, dans la même entrée ; chaque texte porte ses deux langues ({"fr": "…", "en": "…"}) et le script en tire un fichier par langue. La version EN traduit le contenu sans le réinventer.
>
> PÉRIMÈTRE
> - Chapitres à traiter : {{NB_CHAPITRES}} ({{LISTE_CHAPITRES}}).
> - Un polycopié = un chapitre = un fichier DOCX + un fichier PDF (par langue).
> - Rappelle le fil rouge dans les exemples : {{FIL_ROUGE}}.
>
> STRUCTURE DE CHAQUE POLYCOPIÉ (blocs, dans cet ordre)
> Produis le contenu sous forme STRUCTURÉE (voir « FORMAT DE SORTIE ») afin que le script Python le mette en page. Pour chaque chapitre :
>
> [BLOC 1 · EN-TÊTE]
>   • Le titre du chapitre et un sous-titre, qui peut porter le titre du cours ; le numéro du chapitre et la mention « Polycopié de synthèse » viennent du script.
>   • Le pied de page ({{AUTEUR}}, {{LICENCE}} et, dans le PDF, le numéro de page) vient aussi du script ; aucune date.
>
> [BLOC 2 · OBJECTIFS PÉDAGOGIQUES]
>   • 3 à 5 objectifs commençant par un verbe d'action (« Identifier… », « Distinguer… », « Appliquer… »).
>   • Cohérents avec les objectifs affichés dans le chapitre HTML.
>
> [BLOC 3 · MINI-SOMMAIRE]
>   • Le script le tire des titres de section (blocs « h2 ») : donne-leur les titres des sections du chapitre, dans leur ordre.
>   • Optionnel : durée de lecture estimée, dans le sous-titre.
>
> [BLOC 4 · SYNTHÈSE STRUCTURÉE]
>   • 2 à 4 sections avec sous-titres reprenant les sections du chapitre.
>   • Texte dense mais clair : phrases courtes, paragraphes brefs (le script n'a de puces que dans « À retenir »).
>   • Mets en valeur les TERMES-CLÉS en gras (**…**) : ce sont les termes du glossaire.
>
> [BLOC 5 · ENCADRÉS COLORÉS] (au moins 2, choisis selon le sujet)
>   • DÉFINITION (encadré info) : un terme central + sa définition exacte du glossaire.
>   • POINT DE VIGILANCE / PIÈGE À ÉVITER (encadré warning ou danger) : erreur fréquente, sanction, risque.
>   • EXEMPLE CONCRET (encadré tip) : cas tiré du fil rouge {{FIL_ROUGE}}.
>   • (optionnel) RÉFÉRENCE NORMATIVE (bloc lawref) : article de loi / norme / standard précis.
>   Chaque encadré a un libellé court, son titre, qui le désigne sans compter sur la seule couleur.
>
> [BLOC 6 · TABLEAU RÉCAPITULATIF]
>   • Un tableau qui synthétise/compare l'essentiel du chapitre (ex. notions vs définitions, obligations vs sanctions, étapes vs livrables, acteurs vs rôles).
>   • 2 à 5 colonnes, 3 à 8 lignes. Le script colore l'en-tête et alterne les lignes.
>
> [BLOC 7 · À RETENIR]
>   • Encadré final très visible : 4 à 6 puces, l'essentiel absolu du chapitre.
>   • Une phrase « mémo » mémorisable, en dernière puce.
>
> [BLOC 8 · POUR ALLER PLUS LOIN / RÉFÉRENCES]
>   • Sources citées (textes, normes, pages), 2 à 5 entrées max.
>   • Renvoi vers : QCM du chapitre, flashcards, atelier fil rouge.
>
> EXIGENCES DE QUALITÉ PÉDAGOGIQUE
> - Accroche implicite dans les objectifs (montre l'utilité concrète).
> - Progression logique, vocabulaire constant avec le glossaire.
> - Lisibilité : pas de pavés ; privilégie paragraphes courts, encadrés, tableau.
> - Typographie : ni tiret cadratin ni tiret demi-cadratin entre espaces (une incise passe entre virgules ou entre parenthèses) ; en français, une espace insécable avant « : ; ? ! » et à l'intérieur des guillemets « » ; aucune date fixe.
> - Contraintes à respecter : {{CONTRAINTES}}.
> - Charte : celle du script ; {{COULEURS_THEME}}, {{POLICE_TITRES}} et {{POLICE_TEXTE}} ne servent qu'à la retoucher, sur demande de l'auteur.
>
> FORMAT DE SORTIE (IMPORTANT, pour alimenter le script Python)
> Ne génère PAS directement de DOCX/PDF, et ne réécris pas le script : « tools/generate_polycopies.py » existe dans le gabarit, et le site attend ses fichiers sous leurs noms. Produis :
> 1. Pour chaque chapitre, son entrée de « tools/polycopies_content.json », dont la clé est le numéro du chapitre, suivant EXACTEMENT le schéma JSON ci-dessous (clés stables, le script ne lit que ces clés).
> 2. Rien d'autre : le script lit ce fichier et écrit, pour chaque chapitre et chaque langue, un DOCX et un PDF dans « site/assets/polycopies/ ».
>
> SCHÉMA JSON (une entrée par chapitre ; chaque texte en {"fr": "…", "en": "…"}, ou une simple chaîne en français seul) :
> {
>   "1": {
>     "title": { "fr": "…", "en": "…" },
>     "subtitle": { "fr": "Polycopié de synthèse", "en": "Summary handout" },
>     "blocks": [
>       ["p", { "fr": "…", "en": "…" }],
>       ["h2", { "fr": "1. …", "en": "1. …" }],
>       ["callout", "info", { "fr": "Titre", "en": "Title" }, { "fr": "Texte", "en": "Text" }],
>       ["lawref", { "fr": "Référence", "en": "Reference" }, { "fr": "Texte cité", "en": "Quoted text" }],
>       ["table", [{ "fr": "Colonne 1", "en": "Column 1" }, { "fr": "Colonne 2", "en": "Column 2" }],
>                 [[{ "fr": "…", "en": "…" }, { "fr": "…", "en": "…" }]]],
>       ["takeaways", [{ "fr": "…", "en": "…" }, { "fr": "…", "en": "…" }]]
>     ]
>   }
> }
> Les types de blocs : « p » (un paragraphe, le gras en **…**), « h2 » (un titre de section, repris au mini-sommaire), « callout » (un encadré info, tip, warning ou danger, son titre puis son texte), « lawref » (une référence normative puis le texte cité), « table » (les en-têtes puis les lignes), « takeaways » (les puces de « À retenir »).
> Chaque bloc de la structure y prend sa place : BLOC 1 dans « title » et « subtitle », BLOCS 2, 4 et 8 en « h2 » et « p », BLOC 3 dans les « h2 », BLOC 5 en « callout » ou « lawref », BLOC 6 en « table », BLOC 7 en « takeaways ».
>
> SPÉCIFICATION DU SCRIPT « tools/generate_polycopies.py » (celui du gabarit, à ne pas réécrire)
> - Dépendances : python-docx (DOCX), fpdf2 (PDF), pypdfium2 en option ; « pip install -r tools/requirements.txt ».
> - Appel : « python3 tools/generate_polycopies.py » pour les deux langues, avec « fr » ou « en » pour une seule.
> - Entrée : « tools/polycopies_content.json », toutes ses entrées à chaque passage.
> - Sorties : « site/assets/polycopies/chapitre-<n>-polycopie.<langue>.pdf », que le site sert, et le « .docx » du même nom dans « tools/out/ », jamais publié ; une ligne « OK » par chapitre et par langue.
> - Mise en page : bandeau de titre, mini-sommaire tiré des « h2 », encadrés colorés selon leur type, tableau à en-tête colorée et lignes alternées, « À retenir » encadré, pied de page ; charte bleu nuit et doré, Calibri pour le DOCX, Arial pour le PDF.
> - Une autre charte se demande à l'auteur, puis se règle dans les constantes du script (NAVY, GOLD, CALLOUT, LABELS), jamais dans le contenu.
>
> LIVRABLES ATTENDUS (dans ta réponse)
> A. Pour CHAQUE chapitre demandé : son entrée JSON conforme au schéma, prête à placer dans tools/polycopies_content.json.
> B. Aucun script : celui du gabarit reste tel quel.
> C. La COMMANDE D'EXÉCUTION exacte et un exemple de sortie attendue.
> D. Une checklist de vérification (cohérence avec le chapitre, terminologie glossaire, sources citées, chiffres du cas repris des pages, à revérifier après toute retouche de outils/referentiel.py).
>
> CONTRÔLE FINAL AVANT DE RÉPONDRE
> - Chaque bloc (1 à 8) est présent pour chaque chapitre.
> - Aucune information inventée ; tout est traçable au chapitre/source.
> - Terminologie strictement alignée sur le glossaire.
> - Si {{LANGUES}} inclut l'anglais : versions FR et EN équivalentes et complètes.
> ```

---

## Commande d'exécution (rappel)

```bash
# Installer les dépendances (une fois)
pip install -r tools/requirements.txt

# Générer tous les polycopiés (DOCX + PDF), en français et en anglais, d'après tools/polycopies_content.json
python3 tools/generate_polycopies.py

# Une seule langue, le français
python3 tools/generate_polycopies.py fr

# Puis la liste des médias, sans laquelle le site ne propose pas une fiche nouvelle
python3 outils/generer_medias.py
```

Sortie attendue (exemple) :

```
OK [fr] chapitre 1 : … o (pdf) … o (docx)
OK [fr] chapitre 2 : … o (pdf) … o (docx)
…
OK [en] chapitre 3 : … o (pdf) … o (docx)
```

---

## Conseils

- **Une seule source de vérité.** Génère d'abord les chapitres HTML et le glossaire, puis les polycopiés : ainsi le polycopié ne fait que *condenser* l'existant. Si tu modifies un chapitre, reprends son entrée du JSON puis relance le script, sans jamais retoucher un DOCX ou un PDF à la main.
- **Sépare contenu et mise en page.** Le JSON porte le contenu, le script porte la charte. On peut restyler tous les polycopiés en changeant uniquement les constantes de `tools/generate_polycopies.py` (`NAVY`, `GOLD`, `CALLOUT`, `LABELS`).
- **Teste le PDF en premier** sur un chapitre court : fpdf2 est plus capricieux que python-docx sur les accents et les glyphes (`€`, `§`, `⚠`). Le script les écrit avec la police Arial du poste (`C:\Windows\Fonts`), sans repli ASCII ; relisez ce PDF avant d'écrire les autres chapitres.
- **Garde les encadrés courts.** Un encadré = une idée. S'il déborde sur deux pages, c'est qu'il faut le scinder ou le passer en section.
- **Vérifie la fidélité.** Avant publication, relis chaque polycopié à côté du chapitre : zéro notion nouvelle, mêmes définitions, mêmes chiffres. Les renvois (QCM, flashcards, atelier) doivent pointer vers des ressources qui existent.
- **Bilingue.** Si `{{LANGUES}}` = français + anglais, chaque texte porte ses deux langues dans la même entrée : l'équivalence FR/EN se relit bloc par bloc, et le script nomme lui-même les fichiers (`.fr`, `.en`).
- **Les polycopiés se publient avec le site.** Le script les écrit dans `site/assets/polycopies/`, et seuls les fichiers de `site/` suivis par Git partent en ligne. Relancez ensuite `outils/generer_medias.py` : `media.js` ne propose que les médias de sa liste.
