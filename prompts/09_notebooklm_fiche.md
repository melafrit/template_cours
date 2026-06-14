# Fiche de cours pour NotebookLM

**Quand l'utiliser**
Une fois que la structure du cours et les contenus des chapitres existent, pour produire **un document de synthèse unique et dense** (à exporter en `.docx`) que tu déposeras dans **NotebookLM comme source principale**. NotebookLM s'en servira ensuite pour générer automatiquement les **résumés audio (podcasts)**, les **slides** et les **infographies** par chapitre. La qualité de ces générations dépend directement de la fidélité, de la densité et de la structuration de cette fiche : elle doit contenir tout l'essentiel du cours, rien d'inventé, et être organisée pour qu'une IA puisse la « lire » sans contresens.

> À enchaîner ensuite avec le prompt **`10_notebooklm_prompts.md`** (prompts à coller dans NotebookLM pour générer infographie / slides / podcast par chapitre à partir de cette fiche).

---

## Placeholders à compléter

- `{{SUJET_DU_COURS}}` — intitulé exact du cours.
- `{{PUBLIC_CIBLE}}` — à qui s'adresse le cours.
- `{{NIVEAU}}` — débutant / intermédiaire / avancé.
- `{{DUREE}}` — volume horaire ou durée totale.
- `{{LANGUES}}` — `français seul` **ou** `français + anglais`.
- `{{NB_CHAPITRES}}` — nombre de chapitres du cours.
- `{{PLAN_DU_COURS}}` — la liste ordonnée des chapitres et de leurs sections (titres). Colle-la telle quelle.
- `{{DOCUMENTS_DE_REFERENCE}}` — sources faisant autorité (textes du cours déjà rédigés, supports, normes, lois, articles…). **La fiche doit s'appuyer EXCLUSIVEMENT dessus.**
- `{{FIL_ROUGE}}` — le scénario continu (cas fil rouge) qui traverse le cours.
- `{{GLOSSAIRE}}` — la liste des termes clés / définitions déjà fixés pour le cours (pour rester cohérent). Mets `à déduire des documents` si tu n'en as pas encore.
- `{{AUTEUR}}` — auteur du cours.
- `{{LICENCE}}` — licence du contenu (ex. CC BY 4.0).
- `{{CONTRAINTES}}` — limites particulières (longueur cible, vocabulaire à éviter, exclusions, niveau de détail…).

---

## PROMPT À COPIER

> Copie tout le bloc ci-dessous dans Claude, après avoir remplacé les `{{...}}`.

```
RÔLE
Tu es ingénieur pédagogique et rédacteur technique. Tu produis une FICHE DE COURS DE SYNTHÈSE, dense et fidèle, destinée à être déposée dans NotebookLM comme SOURCE UNIQUE. NotebookLM générera ensuite, à partir de ce seul document, des podcasts, des slides et des infographies, chapitre par chapitre. La fiche doit donc contenir tout l'essentiel du cours, dans un ordre clair, sans rien qui ne figure pas dans les documents de référence.

CONTEXTE DU COURS
- Sujet : {{SUJET_DU_COURS}}
- Public cible : {{PUBLIC_CIBLE}}
- Niveau : {{NIVEAU}}
- Durée : {{DUREE}}
- Langue(s) de rédaction : {{LANGUES}}
- Nombre de chapitres : {{NB_CHAPITRES}}
- Plan du cours (chapitres et sections) : {{PLAN_DU_COURS}}
- Fil rouge (cas continu) : {{FIL_ROUGE}}
- Glossaire / termes clés de référence : {{GLOSSAIRE}}
- Auteur : {{AUTEUR}}
- Licence : {{LICENCE}}
- Contraintes : {{CONTRAINTES}}

DOCUMENTS DE RÉFÉRENCE (source de vérité)
{{DOCUMENTS_DE_REFERENCE}}

EXIGENCE D'EXACTITUDE (impérative, avant toute rédaction)
1. Lis et ANALYSE EN DÉTAIL l'intégralité des documents de référence AVANT de rédiger quoi que ce soit.
2. Ne rédige RIEN qui ne soit appuyé sur ces documents. N'invente aucun chiffre, aucune date, aucune citation, aucun article de loi, aucun nom propre, aucune définition.
3. Si une information utile manque dans les sources, ne la fabrique pas : écris explicitement « [À compléter par l'auteur] » à cet endroit. Ne comble jamais un trou par une supposition.
4. Quand une affirmation repose sur une source précise (texte de loi, norme, page, document nommé), indique la source entre crochets, p. ex. « [RGPD, art. 5] » ou « [Doc. 2, §3] ». Reste sobre mais traçable.
5. Reprends fidèlement la terminologie du {{GLOSSAIRE}} et des documents : mêmes définitions, mêmes mots clés, pour éviter toute dérive de sens lors des générations NotebookLM.
6. Avant de produire la fiche, dresse une courte LISTE DES ZONES D'INCERTITUDE ou de contradiction entre les sources, puis demande-moi de trancher si c'est bloquant ; sinon, signale-les en note dans le texte.

CONSIGNES DE RÉDACTION POUR NOTEBOOKLM
- Écris une PROSE pleine, autosuffisante et explicite. NotebookLM lit du texte : évite les listes télégraphiques trop sèches, les renvois du type « voir slide 4 », les abréviations non explicitées, les tableaux complexes, les notes de bas de page. Privilégie des phrases complètes qui se comprennent isolément.
- Sois DENSE mais CLAIR : chaque idée importante doit apparaître formulée explicitement au moins une fois, car NotebookLM ne « devine » pas l'implicite.
- Structure FORTE et RÉGULIÈRE : des titres hiérarchisés et identiques d'un chapitre à l'autre, pour que NotebookLM puisse générer un livrable cohérent PAR CHAPITRE.
- Définis chaque terme technique à sa première apparition, en une phrase.
- Donne des exemples CONCRETS et, dès que possible, rattache-les au fil rouge {{FIL_ROUGE}} : cela rend les podcasts et slides vivants et incarnés.
- Reste neutre et factuel ; pas de marketing, pas de « nous pensons que ». Ton pédagogique, précis, professionnel.
- Pas d'éléments interactifs, de liens hypertexte, d'images : du texte structuré uniquement (ce document sera converti en .docx).

GESTION DES LANGUES
- Si {{LANGUES}} = « français seul » : rédige toute la fiche en français.
- Si {{LANGUES}} = « français + anglais » : rédige la fiche EN FRANÇAIS, et ajoute pour CHAQUE chapitre un court encadré final « Key terms (EN) » donnant la traduction anglaise des termes clés et une phrase de résumé en anglais. Ne traduis pas tout le corps en double (ce serait trop long pour NotebookLM) ; concentre l'anglais sur le vocabulaire et le résumé.

STRUCTURE EXACTE DU DOCUMENT À PRODUIRE

# Fiche de cours pour NotebookLM — {{SUJET_DU_COURS}}

## 0. Notice d'utilisation (1/2 page)
- Indique : auteur {{AUTEUR}}, licence {{LICENCE}}, public {{PUBLIC_CIBLE}}, niveau {{NIVEAU}}, durée {{DUREE}}.
- Phrase d'usage : « Ce document est conçu comme source unique pour NotebookLM afin de générer podcasts, slides et infographies par chapitre. »
- Avertissement : la fiche est un condensé fidèle des documents de référence ; en cas de doute, se reporter aux sources originales.

## 1. Vue d'ensemble du cours (1 page max)
- Résumé du cours en un paragraphe.
- 3 à 6 OBJECTIFS PÉDAGOGIQUES GÉNÉRAUX (verbes d'action : comprendre, savoir faire, être capable de…).
- Présentation du FIL ROUGE {{FIL_ROUGE}} : le contexte, les personnages/acteurs, l'enjeu, et comment il reviendra dans chaque chapitre.
- Carte mentale TEXTUELLE du cours : énumère les {{NB_CHAPITRES}} chapitres et, pour chacun, la promesse en une phrase (« À la fin de ce chapitre, l'apprenant saura… »).

## 2. Glossaire transversal
- Reprends/consolide {{GLOSSAIRE}}. Pour chaque terme : définition courte (1 phrase) + 1 exemple bref ancré dans le sujet ou le fil rouge.
- Classe par ordre alphabétique. C'est la référence terminologique commune à tout le document.

## 3 → (2 + {{NB_CHAPITRES}}). UN BLOC PAR CHAPITRE
Pour CHAQUE chapitre du {{PLAN_DU_COURS}}, produis EXACTEMENT cette structure, avec les mêmes intitulés de sous-titres :

### Chapitre N — [Titre]
**En une phrase.** Ce que ce chapitre apprend, formulé simplement.

**Objectifs du chapitre.** 2 à 4 objectifs précis et vérifiables.

**Pourquoi c'est important.** L'accroche : enjeu réel, risque ou bénéfice concret pour le public cible.

**L'essentiel à retenir.** Le cœur du chapitre en prose dense : les notions, mécanismes, règles, étapes ou raisonnements clés, expliqués clairement et dans l'ordre logique. C'est la partie la plus longue. Couvre toutes les sections listées dans le plan pour ce chapitre.

**Définitions clés.** Les termes propres à ce chapitre, chacun défini en une phrase (cohérent avec le glossaire).

**Exemples concrets.** Au moins deux exemples, dont un AU MOINS rattaché au fil rouge {{FIL_ROUGE}}, montrant l'application réelle des notions.

**Le fil rouge dans ce chapitre.** Ce qui arrive au cas fil rouge à cette étape, et le livrable/décision que l'apprenant produirait ici.

**Erreurs fréquentes / points de vigilance.** 2 à 4 pièges courants et comment les éviter.

**À retenir (3 à 5 puces).** Phrases mémorisables, autoportantes, idéales pour des slides.

**Pistes de visualisation pour NotebookLM.** 2 à 3 suggestions de schémas/infographies que ce chapitre se prête à illustrer (ex. « frise des étapes », « tableau comparatif X vs Y », « arbre de décision »). Décris-les en mots, sans les dessiner.

[Si {{LANGUES}} = français + anglais] **Key terms (EN).** Traduction des termes clés + un résumé du chapitre en une à deux phrases en anglais.

## Dernière section — Synthèse finale et fil rouge bouclé
- Résumé du parcours complet en un paragraphe.
- Reprise du fil rouge {{FIL_ROUGE}} du début à la fin : ce qui a été décidé/produit à chaque étape, et l'état final.
- Les 8 à 12 messages clés de tout le cours, en puces (« si vous ne deviez retenir que… »).
- Mention finale : auteur {{AUTEUR}}, licence {{LICENCE}}.

CONTRÔLE QUALITÉ AVANT DE RENDRE (vérifie puis liste en fin de réponse ce que tu as vérifié)
- Tous les {{NB_CHAPITRES}} chapitres sont présents, dans l'ordre du plan, avec la structure identique imposée.
- Aucune affirmation non sourcée ; les inventions potentielles ont été remplacées par « [À compléter par l'auteur] ».
- La terminologie est cohérente entre le glossaire et chaque chapitre.
- Le fil rouge apparaît dans chaque chapitre et est bouclé à la fin.
- Le texte est en prose autosuffisante, sans renvois externes, lisible « à voix haute » (adapté au podcast).
- Le respect de {{CONTRAINTES}} (longueur, vocabulaire, exclusions) est assuré.

FORMAT DE SORTIE
- Rends le document complet en Markdown propre (titres #, ##, ###, gras, puces simples), prêt à être collé puis exporté en .docx.
- N'ajoute aucun commentaire hors du document, SAUF : (a) la liste des zones d'incertitude demandée plus haut, et (b) la checklist de contrôle qualité, toutes deux placées TOUT À LA FIN, sous un séparateur « --- NOTES POUR L'AUTEUR (à retirer avant dépôt dans NotebookLM) --- ».
```

---

## Conseils

- **Nourris bien `{{DOCUMENTS_DE_REFERENCE}}`.** La fiche ne vaut que ce que valent les sources : colle les textes de chapitres déjà rédigés plutôt que de simples titres. Si le cours est volumineux, fais générer la fiche **chapitre par chapitre** (un appel par chapitre, en gardant la même structure) puis recolle l'ensemble.
- **Garde un glossaire stable.** Renseigner `{{GLOSSAIRE}}` évite que NotebookLM redéfinisse les termes à sa façon dans les podcasts/slides. C'est le même vocabulaire qui doit alimenter le glossaire auto-surligné du site.
- **Densité vs. longueur NotebookLM.** Si tes générations partent dans tous les sens, c'est souvent que la fiche est trop longue ou trop touffue : resserre via `{{CONTRAINTES}}` (ex. « 1 à 2 pages par chapitre maximum »).
- **Privilégie la prose à voix haute.** NotebookLM excelle quand le texte se lit comme un script : phrases complètes, transitions explicites, peu de tableaux. Les « Pistes de visualisation » servent surtout aux infographies et aux slides.
- **Export `.docx`.** Une fois la fiche validée, convertis-la (voir le prompt des polycopiés `08_polycopie_docx.md` ou un simple copier-coller dans un traitement de texte) avant de la déposer comme source dans NotebookLM.
- **Bilingue.** En mode `français + anglais`, le bloc « Key terms (EN) » suffit pour que NotebookLM produise un podcast/des slides exploitables en anglais sans alourdir la source ; pour un rendu 100 % anglais, génère une seconde fiche entièrement en anglais à partir du même plan.
