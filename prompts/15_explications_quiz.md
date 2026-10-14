# Prompt — expliquer chaque proposition d'un quiz

> **Quand l'utiliser** — Pour toute question à choix du cours : points de contrôle des
> chapitres (`RDCX.checkpoint`), mini-quiz de fiches, QCM d'entraînement. À lancer dès
> qu'une question est écrite, ou en lot sur des questions existantes.

---

## L'exigence

Pour chaque question, l'étudiant doit lire :

1. **pourquoi la bonne réponse est la bonne** — l'explication (`explication`) ;
2. **pourquoi chacune des autres ne l'est pas** — une raison par proposition écartée
   (`pourquoi`) ;
3. **où approfondir** — deux à quatre renvois vers l'endroit exact du cours qui répond,
   ou vers une référence externe vérifiée (`approfondir`).

**Pourquoi.** Une explication qui ne parle que de la bonne réponse laisse l'étudiant seul
avec son erreur : c'est pourtant la proposition qu'il a choisie qu'il faut démonter. Et un
renvoi vers « le chapitre 3 » ne sert à rien : il faut la section, le schéma, la fiche.

## Le format attendu par le moteur

```js
{ q: "Énoncé…", options: ["A…", "B…", "C…", "D…"], correct: 1,
  explication: "Pourquoi B est juste.",
  pourquoi: ["Pourquoi A ne convient pas.", "", "Pourquoi C…", "Pourquoi D…"],
  approfondir: [["§ 3 — Le couplage", "#ch4-s3"],
                ["Glossaire — couplage", "../glossaire.html"],
                ["Martin Fowler — « Strangler Fig » (en anglais)", "https://martinfowler.com/bliki/StranglerFigApplication.html"]] }
```

- `pourquoi` suit **l'ordre des propositions** ; la case de la bonne réponse reste **vide**.
- `approfondir` : `[libellé, adresse]`. Une adresse du cours (`#ancre`, `page.html`,
  `page.html#ancre`, relative) s'ouvre dans le même onglet ; une adresse `https://` dans
  un nouvel onglet, signalé aux lecteurs d'écran. Toute autre forme est écartée.
- Dans une page bilingue, les deux tableaux vivent dans `TEXTES.fr` et `TEXTES.en`
  (`checkP1`, `checkA1`…), comme dans `site/chapitres/_modele.html`.
- Dans le pied de l'explication, le moteur nomme la bonne réponse par sa lettre et marque
  « votre choix » dans la liste : rien à écrire pour cela.

---

## PROMPT À COPIER

```
Tu complètes les explications des questions à choix du cours {{TITRE_DU_COURS}}.

QUESTIONS : {{QUESTIONS}} (pour chacune : l'énoncé, les propositions, la bonne réponse,
l'explication existante, la page ou la fiche où elle se trouve).

SOURCES : la page ou la fiche de la question, le chapitre qui enseigne la notion, et les
documents de sources/. Tes explications doivent s'accorder avec elles et avec
l'explication existante — ne jamais les contredire. Aucun fait, aucun chiffre nouveau :
seulement ceux de la question ou du cours. Les interdits du cours s'appliquent :
{{INTERDITS_DU_COURS}}.

POUR CHAQUE PROPOSITION ÉCARTÉE (« pourquoi ») :
- Une phrase, deux au plus ; 50 à 330 caractères (viser 100 à 220).
- Nommer l'idée fausse qui la rend tentante, et pourquoi elle ne tient pas ici. Jamais
  « C'est faux. » ; ne pas recopier la proposition mot pour mot en ouverture.
- Le vocabulaire du cours ; clair pour un débutant ; au vouvoiement si besoin ; un exemple
  tiré du fil rouge quand il éclaire.
- Typographie : guillemets « » ; jamais le guillemet droit " dans un texte ; tiret
  cadratin — pour une incise ; espaces insécables avant : ; ? ! et dans « ».

POUR LES RENVOIS (« approfondir ») — deux à quatre, choisis pour CETTE question :
1. D'abord l'endroit de la page qui répond, quand il existe (section, encadré, schéma).
2. Puis l'endroit du cours où la notion s'enseigne : une section de chapitre
   (« Chapitre 4, § 3 — Le couplage » → ../chapitres/04-….html#ch4-s3), un schéma, une
   fiche voisine, un simulateur, le glossaire.
3. Au plus UNE référence externe par question, seulement parmi les adresses déjà
   vérifiées de la bibliographie du cours ; libellé « Auteur — titre (en anglais) » si la
   ressource n'est pas en français. N'invente ni ne devine jamais une adresse.
Seules les ancres qui existent réellement dans les pages sont permises : relève-les avant
d'écrire (les id des h2, h3 et figures).

VÉRIFIE avant de rendre : chaque « pourquoi » a autant d'entrées que de propositions, la
case de la bonne réponse est vide, les autres non ; chaque renvoi pointe un fichier et une
ancre qui existent (python3 outils/verifier_liens.py le contrôle) ; aucune adresse
externe nouvelle sans l'avoir ouverte.

LIVRE : les données prêtes à coller, question par question, puis la liste des questions
dont l'énoncé ou la réponse te paraît ambigu — signale-les, ne les modifie pas.
```

---

## Exemple de ton

Question : « Une équipe de trois développeurs doit livrer une première version en quatre
mois. Quel style de départ est le plus raisonnable ? » — A microservices, un par
fonction / **B monolithe modulaire** / C monolithe sans découpage interne / D un service
par table de la base.

- **A** — « Chaque service se déploie seul, possède sa base et dialogue par le réseau :
  pannes partielles, supervision distribuée, cohérence des données, un déploiement par
  service. À trois, les quatre mois y passeraient. »
- **C** — « Le piège le plus tentant : même avantage de départ — un seul déploiement —,
  mais sans frontières, tout finit par appeler tout. C'est la « grosse boule de boue », où
  la moindre modification casse un voisin. »
- **D** — « C'est découper selon les données au lieu du métier : réserver une place
  toucherait la place, l'usager et le paiement, trois services qui s'appelleraient en
  chaîne à chaque requête. C'est le monolithe distribué. »

## En lot, avec des sous-agents

Pour des centaines de questions, un lot par famille, confié à des sous-agents en
parallèle :

- une **consigne écrite complète** par lot (ce prompt, les ancres valides, la
  bibliographie, le format de sortie, les interdits, l'exemple de ton) ;
- des **données à part** (un fichier par famille), fusionnées par le générateur des pages,
  qui vérifie l'alignement sur les énoncés (début de l'énoncé, nombre de propositions,
  case vide), les longueurs, les renvois (fichier et ancre) et les interdits ;
- un énoncé modifié plus tard fait **refuser la génération** tant que son explication n'a
  pas été revue.

Le cours d'architecture logicielle de l'auteur en donne un modèle complet :
`outils/quiz_fiches/` et `outils/generer_boite_a_outils.py`.
