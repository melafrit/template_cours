# Polycopiés de synthèse (DOCX + PDF)

**Quand l'utiliser** — Une fois les chapitres rédigés et stabilisés. Ce prompt génère, **par chapitre**, un polycopié de synthèse académique (mini-sommaire, encadrés colorés, tableau récapitulatif, « à retenir ») exporté simultanément en **DOCX** *et* **PDF** via un script Python unique (`tools/generate_polycopies.py`). Les polycopiés sont les documents que l'étudiant imprime, annote et révise hors écran ; ils doivent rester strictement cohérents avec le contenu du site.

---

## Placeholders à compléter

- `{{SUJET_DU_COURS}}` — intitulé exact du cours.
- `{{PUBLIC_CIBLE}}` — à qui s'adresse le cours.
- `{{NIVEAU}}` — débutant / intermédiaire / avancé.
- `{{LANGUES}}` — *français seul* OU *français + anglais*. Détermine s'il faut produire une version EN de chaque polycopié.
- `{{NB_CHAPITRES}}` — nombre de chapitres à traiter (ou « tous »).
- `{{LISTE_CHAPITRES}}` — titres + numéros des chapitres concernés.
- `{{DOCUMENTS_DE_REFERENCE}}` — chemins/URL des fichiers HTML des chapitres déjà produits + sources primaires (la **source de vérité**).
- `{{FIL_ROUGE}}` — scénario continu du cours (ex. UrbanHub Smart City), à rappeler dans les exemples.
- `{{AUTEUR}}` — auteur (pied de page, page de garde).
- `{{LICENCE}}` — licence du contenu (ex. CC BY 4.0).
- `{{COULEURS_THEME}}` — couleurs du thème du site (primaire, secondaire, accent) en hexadécimal, pour harmoniser les encadrés. Ex. `#1A3A5A`, `#0E7C66`, `#C8442B`.
- `{{POLICE_TITRES}}` / `{{POLICE_TEXTE}}` — polices à imiter (à défaut : Calibri/Arial pour DOCX, Helvetica pour PDF).
- `{{CONTRAINTES}}` — contraintes spécifiques (longueur max par chapitre, charte graphique de l'établissement, accessibilité, etc.).

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
> - Public : {{PUBLIC_CIBLE}} — Niveau : {{NIVEAU}}.
> - Langues : {{LANGUES}}.
>   • Si « français seul » : produis un seul jeu de polycopiés en français.
>   • Si « français + anglais » : produis pour CHAQUE chapitre une version FR et une version EN, fidèles l'une à l'autre, dans des fichiers séparés (suffixes _fr / _en). La version EN traduit le contenu sans le réinventer.
>
> PÉRIMÈTRE
> - Chapitres à traiter : {{NB_CHAPITRES}} — {{LISTE_CHAPITRES}}.
> - Un polycopié = un chapitre = un fichier DOCX + un fichier PDF (par langue).
> - Rappelle le fil rouge dans les exemples : {{FIL_ROUGE}}.
>
> STRUCTURE DE CHAQUE POLYCOPIÉ (blocs, dans cet ordre)
> Produis le contenu sous forme STRUCTURÉE (voir « FORMAT DE SORTIE ») afin que le script Python le mette en page. Pour chaque chapitre :
>
> [BLOC 1 — EN-TÊTE]
>   • Titre du cours, numéro + titre du chapitre, mention « Polycopié de synthèse ».
>   • Ligne d'identité : {{AUTEUR}} — {{LICENCE}} — date de génération (laissée au script).
>
> [BLOC 2 — OBJECTIFS PÉDAGOGIQUES]
>   • 3 à 5 objectifs commençant par un verbe d'action (« Identifier… », « Distinguer… », « Appliquer… »).
>   • Cohérents avec les objectifs affichés dans le chapitre HTML.
>
> [BLOC 3 — MINI-SOMMAIRE]
>   • Liste des sections du chapitre (les mêmes ancres que la navigation latérale du site).
>   • Optionnel : durée de lecture estimée.
>
> [BLOC 4 — SYNTHÈSE STRUCTURÉE]
>   • 2 à 4 sections avec sous-titres reprenant les sections du chapitre.
>   • Texte dense mais clair : phrases courtes, listes à puces quand c'est pertinent.
>   • Mets en valeur les TERMES-CLÉS (gras) — ce sont les termes du glossaire.
>
> [BLOC 5 — ENCADRÉS COLORÉS] (au moins 2, choisis selon le sujet)
>   • DÉFINITION (couleur primaire) : un terme central + sa définition exacte du glossaire.
>   • POINT DE VIGILANCE / PIÈGE À ÉVITER (couleur accent) : erreur fréquente, sanction, risque.
>   • EXEMPLE CONCRET (couleur secondaire) : cas tiré du fil rouge {{FIL_ROUGE}}.
>   • (optionnel) RÉFÉRENCE NORMATIVE : article de loi / norme / standard précis.
>   Chaque encadré a un libellé court et une icône texte (ex. « ⚠ », « ✓ », « § »).
>
> [BLOC 6 — TABLEAU RÉCAPITULATIF]
>   • Un tableau qui synthétise/compare l'essentiel du chapitre (ex. notions vs définitions, obligations vs sanctions, étapes vs livrables, acteurs vs rôles).
>   • 2 à 5 colonnes, 3 à 8 lignes. En-tête de tableau colorée (couleur primaire).
>
> [BLOC 7 — À RETENIR]
>   • Encadré final très visible : 4 à 6 puces, l'essentiel absolu du chapitre.
>   • Une phrase « mémo » mémorisable.
>
> [BLOC 8 — POUR ALLER PLUS LOIN / RÉFÉRENCES]
>   • Sources citées (textes, normes, pages), 2 à 5 entrées max.
>   • Renvoi vers : QCM du chapitre, flashcards, atelier fil rouge.
>
> EXIGENCES DE QUALITÉ PÉDAGOGIQUE
> - Accroche implicite dans les objectifs (montre l'utilité concrète).
> - Progression logique, vocabulaire constant avec le glossaire.
> - Lisibilité : pas de pavés ; privilégie listes, encadrés, tableau.
> - Contraintes à respecter : {{CONTRAINTES}}.
> - Charte : couleurs {{COULEURS_THEME}} ; polices {{POLICE_TITRES}} / {{POLICE_TEXTE}}.
>
> FORMAT DE SORTIE (IMPORTANT — pour alimenter le script Python)
> Ne génère PAS directement de DOCX/PDF. Produis :
> 1. Un fichier de données « content/polycopies/chapXX[_lang].json » par chapitre/langue, suivant EXACTEMENT le schéma JSON ci-dessous (clés stables, le script ne lit que ces clés).
> 2. Le script Python complet « tools/generate_polycopies.py » qui lit ces JSON et écrit, pour chacun, un DOCX et un PDF dans « build/polycopies/ ».
>
> SCHÉMA JSON (une entrée par polycopié) :
> {
>   "lang": "fr",
>   "cours": "{{SUJET_DU_COURS}}",
>   "chapitre_num": "01",
>   "chapitre_titre": "…",
>   "auteur": "{{AUTEUR}}",
>   "licence": "{{LICENCE}}",
>   "theme": { "primaire": "#......", "secondaire": "#......", "accent": "#......" },
>   "objectifs": ["…", "…"],
>   "sommaire": ["Section 1 — …", "Section 2 — …"],
>   "sections": [
>     { "titre": "…", "paragraphes": ["…"], "puces": ["…"] }
>   ],
>   "encadres": [
>     { "type": "definition|vigilance|exemple|reference", "titre": "…", "icone": "§", "texte": "…" }
>   ],
>   "tableau": {
>     "titre": "…",
>     "entetes": ["Colonne 1", "Colonne 2"],
>     "lignes": [["…", "…"]]
>   },
>   "a_retenir": { "puces": ["…"], "memo": "…" },
>   "references": ["…"],
>   "renvois": { "qcm": "…", "flashcards": "…", "atelier": "…" }
> }
>
> SPÉCIFICATION DU SCRIPT « tools/generate_polycopies.py »
> - Dépendances : python-docx (DOCX) et fpdf2 (PDF). En tête de fichier, indique : « pip install python-docx fpdf2 ».
> - CLI (argparse) :
>     --input   dossier des JSON (défaut: content/polycopies)
>     --output  dossier de sortie (défaut: build/polycopies)
>     --only    motif optionnel (ex. "chap01" ou "_en") pour ne traiter qu'une partie
>     --formats docx,pdf (défaut: les deux)
> - Comportement : lit chaque .json, valide les clés requises (lève une erreur claire si manquante), génère docx ET pdf, nomme les fichiers d'après chapitre_num + lang (ex. « poly_chap01_fr.docx »).
> - Mise en page commune DOCX/PDF :
>     • En-tête (BLOC 1) + pied de page « {{AUTEUR}} — {{LICENCE}} — page X » + date de génération automatique.
>     • Titres de section dans la couleur primaire ; termes-clés en gras.
>     • Encadrés : fond/bordure coloré selon "type" (definition=primaire, vigilance=accent, exemple=secondaire, reference=primaire foncé) ; libellé + icône ; texte à l'intérieur.
>     • Tableau : en-tête colorée (couleur primaire, texte blanc), lignes alternées (zébrage léger) pour la lisibilité.
>     • Bloc « À RETENIR » : encadré pleine largeur bien visible en fin de document.
>     • Couleurs lues depuis la clé "theme" (conversion hex -> RGB pour python-docx et fpdf2).
>     • Polices : {{POLICE_TITRES}} / {{POLICE_TEXTE}} (avec repli sûr si la police manque).
>     • Accessibilité : taille de corps ≥ 11 pt, contraste suffisant, pas d'information portée par la seule couleur (toujours un libellé texte).
> - Robustesse : encodage UTF-8 partout ; gère les caractères accentués et « € », « § », « ⚠ » sans planter le PDF ; si fpdf2 manque une glyphe, prévoir un repli ASCII.
> - Le script doit créer le dossier de sortie s'il n'existe pas, logguer chaque fichier écrit, et finir par un récapitulatif (« N polycopiés générés »).
> - Code commenté, fonctions courtes (ex. add_box, add_table, hex_to_rgb), exécutable tel quel.
>
> LIVRABLES ATTENDUS (dans ta réponse)
> A. Pour CHAQUE chapitre demandé : le JSON conforme au schéma, prêt à enregistrer dans content/polycopies/.
> B. Le script complet tools/generate_polycopies.py.
> C. La COMMANDE D'EXÉCUTION exacte et un exemple de sortie attendue.
> D. Une checklist de vérification (cohérence avec le chapitre, terminologie glossaire, sources citées).
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
pip install python-docx fpdf2

# Générer tous les polycopiés (DOCX + PDF) à partir des JSON
python tools/generate_polycopies.py --input content/polycopies --output build/polycopies

# Un seul chapitre, version anglaise, PDF uniquement
python tools/generate_polycopies.py --only chap01_en --formats pdf
```

Sortie attendue (exemple) :

```
[OK] build/polycopies/poly_chap01_fr.docx
[OK] build/polycopies/poly_chap01_fr.pdf
…
3 polycopiés générés (6 fichiers).
```

---

## Conseils

- **Une seule source de vérité.** Génère d'abord les chapitres HTML et le glossaire, puis les polycopiés : ainsi le polycopié ne fait que *condenser* l'existant. Si tu modifies un chapitre, régénère le JSON puis relance le script — pas de double saisie.
- **Sépare contenu et mise en page.** Les JSON portent le contenu, le script porte la charte. On peut restyler tous les polycopiés en changeant uniquement `tools/generate_polycopies.py` ou la clé `theme`.
- **Teste le PDF en premier** sur un chapitre court : fpdf2 est plus capricieux que python-docx sur les accents et les glyphes (`€`, `§`, `⚠`). Validez le repli ASCII avant de lancer toute la série.
- **Garde les encadrés courts.** Un encadré = une idée. S'il déborde sur deux pages, c'est qu'il faut le scinder ou le passer en section.
- **Vérifie la fidélité.** Avant publication, relis chaque polycopié à côté du chapitre : zéro notion nouvelle, mêmes définitions, mêmes chiffres. Les renvois (QCM, flashcards, atelier) doivent pointer vers des ressources qui existent.
- **Bilingue.** Si `{{LANGUES}}` = français + anglais, demandez les deux JSON en une fois pour garantir l'équivalence FR/EN, et nommez clairement les fichiers (`_fr` / `_en`).
- **Versionne `build/` à part.** Mettez `build/polycopies/` dans `.gitignore` si vous ne souhaitez versionner que les sources JSON et le script.
