# Prompt 08 · QCM papier imprimable (DOCX)

**Quand l'utiliser**
Après avoir validé la banque du QCM en ligne (prompt 07). Ce prompt en tire la **version papier imprimable**, en
trois fichiers Word **noir et blanc, compacts**, pour chaque langue :

1. **`QCM_questions.<langue>.docx`** : page de garde, consignes, barème CBM avec exemples chiffrés, puis les
   questions en **deux colonnes** ;
2. **`QCM_grille_reponses.<langue>.docx`** : la **grille de réponses** (réponse unique A/B/C/D et certitude
   F/M/É), seul document ramassé ;
3. **`QCM_corrige.<langue>.docx`** : le **corrigé du formateur** (bonne réponse et explication, par chapitre).

**Le script du gabarit les produit** : `tools/generate_qcm_papier.py` (python-docx) lit la banque du QCM en ligne,
`site/QCM/questions.js` et `site/QCM/corrections.js`, et écrit dans `tools/out/`, que Git ignore. Le corrigé reste
ainsi hors de `site/` et n'est jamais publié. Ce prompt ne fait **écrire aucun script** : il fait contrôler la
banque et lancer le script, puis relire les fichiers. C'est la décision de l'auteur du 22 novembre 2026 ; un script
écrit par le prompt aurait écrasé celui du gabarit.

**Une épreuve notée qui a sa propre banque suit un autre chemin.** Si le QCM papier est l'épreuve, et que sa banque
ne se publie pas, ce prompt ne s'applique pas : suivez le module 05 (`prompts/modules/05-evaluations.md`), sur le
modèle du cours CDWFS (`outils/qcm/`). Sa banque se traite comme un secret (CLAUDE.md, § 2) : exclue des recherches
par le `.rgignore` dès sa création, jamais dans `site/` ni dans un dépôt public, et aucune de ses questions dans
l'entraînement.

---

## Ce que le script prend dans la banque

| Ce qui s'imprime | Où le script le lit | S'il manque |
|---|---|---|
| Le titre (page de garde, pieds de page) | `meta.titre` de `questions.js`, `{fr, en}` | « QCM » ou « Quiz » |
| Le bandeau | `meta.formation` (`{fr, en}`) et `meta.annee_academique` | rien |
| La durée | `meta.duree` | « 1 h 30 » |
| L'auteur | `meta.auteur` | le nom écrit dans le script |
| Les énoncés et les propositions | `questions[].enonce` et `questions[].propositions` (quatre, `{fr, en}`) | |
| Le chapitre, qui regroupe le corrigé | `questions[].chapitre` | |
| La bonne réponse et l'explication | `corrections[].bonne_reponse_index` et `corrections[].explication`, appariées par `id` | |

Les consignes imprimées (ressources admises : une calculatrice non connectée et une feuille de notes recto verso),
le barème CBM, ses exemples et la licence (CC BY 4.0) sont écrits dans la fonction `labels()` du script, en
français et en anglais. Le script ne connaît que ces deux langues : un cours en arabe le signale à l'auteur, sans
traduire.

---

## Placeholders à compléter

- `{{SUJET_DU_COURS}}` : ex. « Réglementation des données et conformité »
- `{{NB_QUESTIONS}}` : le nombre de questions attendu dans la banque (ex. `60`), de préférence divisible par 3 pour
  une grille en trois blocs égaux
- `{{DUREE_EPREUVE}}` : ex. « 1 h 30 », à écrire dans `meta.duree` si la banque ne l'a pas
- `{{LANGUES}}` : `fr`, `en` ou `both`
- `{{REGLES_EPREUVE}}` : ce que le règlement de l'épreuve permet (ressources, durée, document ramassé), pour vérifier
  les consignes imprimées
- `{{DOCUMENTS_DE_REFERENCE}}` : les supports sur lesquels s'appuient les explications du corrigé (pour vérifier,
  **pas** pour inventer)
- `{{CONTRAINTES}}` : ex. « recto verso, pas plus de N pages »

---

## PROMPT À COPIER

> Copiez tout le bloc ci-dessous dans Claude. Remplacez les `{{...}}` au préalable.

```text
Tu prépares la VERSION PAPIER IMPRIMABLE du QCM en ligne de ce cours, avec le script du gabarit,
tools/generate_qcm_papier.py. Tu n'écris aucun script.

CONTEXTE
- Cours : {{SUJET_DU_COURS}}
- Banque, SEULE source autorisée : site/QCM/questions.js et site/QCM/corrections.js (mêmes id)
- Questions attendues : {{NB_QUESTIONS}} · durée {{DUREE_EPREUVE}} · langues {{LANGUES}}
- Règlement de l'épreuve : {{REGLES_EPREUVE}}
- Explications du corrigé, à vérifier sur : {{DOCUMENTS_DE_REFERENCE}}
- Contraintes : {{CONTRAINTES}}

0. LE BON CHEMIN
Si ce QCM papier est l'épreuve notée et que sa banque ne se publie pas, arrête-toi et dis-le à l'auteur :
ce prompt imprime la banque publiée du QCM en ligne. L'épreuve à banque privée suit le module 05
(prompts/modules/05-evaluations.md).

1. LE CONTRÔLE DE LA BANQUE, avant toute génération
Analyse la banque EN DÉTAIL. Ne réécris aucun énoncé, ne change ni une proposition ni une bonne réponse,
n'invente aucune question. Signale, sans corriger en silence :
- le nombre de questions, comparé à {{NB_QUESTIONS}} ;
- toute question qui n'a pas exactement 4 propositions et une seule bonne réponse, tout id sans sa correction ;
- les positions des bonnes réponses (environ 25 % par lettre) et tout déséquilibre marqué ;
- les bonnes réponses qui sont trop souvent la proposition la plus longue (distracteurs à débiaiser) ;
- toute proposition tronquée, dupliquée ou vide ;
- tout tiret cadratin, ou tiret moyen entre espaces, dans le titre, un énoncé, une proposition ou une
  explication : il se corrige dans la banque ;
- les champs meta que le script imprime (titre, formation, annee_academique, duree, auteur) et leur valeur.
Présente un court rapport (compte par lettre, anomalies). Un problème bloquant se tranche avec l'auteur,
une question à la fois ; sinon, poursuis.

2. LES CONSIGNES IMPRIMÉES
Compare les consignes, le barème et la licence que la fonction labels() du script imprime avec
{{REGLES_EPREUVE}}. Signale tout écart (ressources admises, durée) et propose la retouche ; ne modifie le
script qu'avec l'accord de l'auteur.

3. LA GÉNÉRATION
  python -m pip install python-docx        (s'il manque)
  python tools/generate_qcm_papier.py {{LANGUES}}
Le script écrit dans tools/out/, ignoré par Git, et affiche « OK <fichier> <taille> o » pour chaque fichier.
Relance-le après toute retouche de la banque : un DOCX ne se corrige jamais à la main.

4. LA RELECTURE AVANT IMPRESSION, checklist à rendre remplie
  [ ] Le nombre de questions imprimées est {{NB_QUESTIONS}}.
  [ ] La grille a autant de lignes que de questions, numérotées sans trou.
  [ ] Le barème affiché est Élevée +3/−3 · Moyenne +2/−2 · Faible +1/0, et la formule /20 est juste.
  [ ] L'exemple chiffré sur trois questions donne bien le total annoncé.
  [ ] Tout est en noir et blanc, lisible en photocopie, dans le nombre de pages visé.
  [ ] Aucun énoncé ni aucune proposition n'est coupé en bas de colonne.
  [ ] Aucun tiret cadratin dans les fichiers.
  [ ] Le corrigé n'est PAS distribué aux étudiants (fichier séparé, « réservé au formateur »).

LIVRABLES, dans l'ordre
1. Le rapport de contrôle de la banque.
2. Les écarts entre les consignes imprimées et le règlement, s'il y en a.
3. La commande lancée et sa sortie.
4. La checklist de relecture, remplie.
```

---

## Conseils

- **Le contrôle d'abord.** Le rapport sur la banque (bonnes réponses par lettre, propositions tronquées, bonne
  réponse trop souvent la plus longue) vient **avant** la génération : c'est le moment le moins coûteux pour
  corriger.
- **Une seule source.** La banque du QCM en ligne fait foi : une question se corrige dans `questions.js` ou
  `corrections.js`, puis le script régénère les fichiers.
- **Un nombre de questions divisible par 3** donne une grille en trois blocs égaux ; sinon, le script répartit les
  questions au plus juste.
- **Le PDF pour l'impression.** python-docx ne produit pas de PDF. Pour figer la mise en page, exportez les `.docx`
  en PDF (Word, « Enregistrer sous », ou `libreoffice --headless --convert-to pdf`), un export à la fois, et
  contrôlez la langue que le PDF déclare.
- **La diffusion.** Seuls `QCM_questions` et `QCM_grille_reponses` vont aux étudiants ; `QCM_corrige` reste au
  formateur.
- **La cohérence avec le QCM en ligne.** Le barème CBM, la formule /20 et l'équilibre des réponses sont les mêmes :
  l'étudiant retrouve sur le papier les règles de l'écran.
