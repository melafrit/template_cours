# Module 09 — Les compléments : schémas, illustrations, simulateurs, glossaire, Boîte à outils, fiches mémo

> **Quand l'activer.** Selon la matière : des schémas pour un cours de conception, des
> simulateurs pour un cours de calcul, une Boîte à outils pour un cours de méthode, des
> fiches mémo pour réviser. Le glossaire vaut pour presque tous.
>
> **Paramètres.** `modules.complements` : `schemas`, `illustrations`, `simulateurs`,
> `glossaire`, `boite_a_outils`, `fiches_memo`, `encarts_plus_loin`.
>
> **Place.** Phase 7 du tronc, après les contenus et les évaluations ; le glossaire se pose
> dès la phase 3 et se complète ici.
>
> **Seul.** Sur un cours qui existe déjà, donnez ce fichier à Claude dans le dossier du
> cours : il commence par la section 8.

---

## 1. Les fragments générés : aucun chiffre écrit à la main

Le référentiel du cas, `outils/referentiel.py`, porte **tous** les chiffres du cas
(`VALEURS`, `DUREES`, des fragments composés) et une fonction `verifier()` ; un chiffre ne
s'écrit jamais à la main dans une page. La page marque l'endroit —
`<!-- FRAGMENT:val-places -->12 000<!-- /FRAGMENT:val-places -->` — et
`outils/generer_fragments.py` y écrit la valeur, dans la langue de la page ou du bloc
`data-tr` qui l'entoure ; il fournit aussi `nb-chapitres` et `nb-chapitres-lettres`, d'après
`course-data.js`. Son `--essai` signale un fragment périmé, inconnu ou sans valeur ; il fait
partie des contrôles avant mise en ligne. Les schémas, les fiches et le livret puisent aux
mêmes sources. Sur le cours d'architecture logicielle (lecture seule), le même principe
porte aussi les séances, les personnages, les étapes du TP : de quoi s'inspirer pour les
fragments composés.

---

## 2. Les schémas

- **Tirés du référentiel** quand ils portent des chiffres ; sur un exemple neutre dès qu'ils
  toucheraient à une réponse.
- **Chacun a sa lecture élément par élément**, écrite pour un débutant : ce qu'il montre,
  comment le lire, chaque élément et son rôle, ses liens avec les autres pièces, le piège à
  éviter. Sur le cours de référence : `outils/lectures_schemas.py` (D115).
- [si `capsule_par_schema`] **Une capsule par schéma**, sur le même plan que sa lecture
  (module 04).
- **Un schéma déjà rendu par PlantUML ne se rend jamais de nouveau sur un autre poste** que
  celui qui l'a produit : les polices du poste changent le dessin. Dans le gabarit :
  `outils/generer_schemas_demo.py` et `outils/convertir_schemas.py` (une image par langue,
  `chapitre-<N>-schema-1-<slug>.<langue>.webp`).

---

## 3. Les illustrations (`illustrations.actif`)

Une fiche par image (fichier, dimensions, page, contexte, scène, composition) ; une charte de
style en anglais ; **aucun texte dans l'image** ; les personnages décrits mot pour mot d'une
fiche à l'autre ; conversion en WebP, emplacements posés d'avance. L'outil
(`illustrations.outil`, Codex) génère ; l'auteur valide. **STOP** : relecture en planche
contact.

---

## 4. Les simulateurs et les encarts

- **Les simulateurs** (`simulateurs`, ou ta proposition) : un calcul que l'étudiant
  manipule (charge, coûts, disponibilité, score de risque…), adossé au référentiel ; les
  libellés dans `ui-labels.js`.
- **Les encarts « Pour aller plus loin »** (`encarts_plus_loin`) : une référence externe
  vérifiée, ouverte avant d'être ajoutée, en nouvel onglet (`target="_blank"
  rel="noopener noreferrer"`).

---

## 5. Le glossaire (`glossaire`)

Chaque terme : sa définition, son chapitre d'introduction, un exemple ; des termes vedettes ;
les info-bulles du moteur (`glossaire-tooltip.js`). Puis **« Où en parle-t-on ? »** : pour
chaque terme, les pages qui l'emploient (`prompts/06_glossaire.md`,
`prompts/06b_glossaire_ou_en_parle_t_on.md`) ; sur le cours de référence,
`outils/generer_glossaire.py` et `outils/glossaire_emplois.py`, qui excluent les pages qui
n'expliquent aucune notion (une table des matières, la page du polycopié, celle des
podcasts). Avant d'y poser des QR codes (module 02), vérifier comment une adresse ouvre un
terme précis.

---

## 6. La Boîte à outils et les fiches mémo

- **La Boîte à outils** (`boite_a_outils`) : des fiches d'une page, chacune avec sa
  définition, à quoi elle sert, un exemple, et un mini-quiz expliqué ; sur le cours de
  référence, `outils/generer_boite_a_outils.py`, et une annexe Word et PDF.
- **Les fiches mémo** (`fiches_memo`) : des fiches d'une page, pour réviser ; sur le cours de
  référence, `outils/generer_fiches_memo.py` ; elles entrent en pleine page dans le livret,
  sans réponse imprimée (module 02).

---

## 7. Les contrôles

Les fragments à jour (aucun chiffre du cas écrit à la main) ; chaque schéma avec sa lecture ;
aucun texte dans les illustrations ; chaque lien externe ouvert et vérifié ;
`verifier_liens.py` sans écart, renvois du glossaire compris ; au navigateur, simulateurs et
info-bulles qui marchent, clair et sombre, 1280 et 375 px, console vide.

**Terminé** quand chaque complément retenu est en ligne et contrôlé, et que les décisions,
l'état d'avancement et `TODO.md` sont à jour.

---

## 8. Pour commencer

1. Lis le référentiel du cas, les contenus et les compléments déjà présents.
2. Propose, complément par complément, ce qui servirait ce cours — et ce qui ne le servirait
   pas : un bloc jamais rempli qui traîne dans le menu donne un cours inachevé.
3. Pose les questions de cadrage, **une à une**.
4. Un témoin par sorte de complément (un schéma et sa lecture, une fiche, un simulateur),
   validé, puis la série.

Sur un cours qui n'a pas été créé depuis le template, les règles de son `CLAUDE.md`
s'appliquent ; à défaut, celles du § 2 du `CLAUDE.md` du template.
