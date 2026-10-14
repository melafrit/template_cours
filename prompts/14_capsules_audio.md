# Prompt — capsules audio en Eleven v4

> **Quand l'utiliser** — Pour écrire, ou réécrire, les capsules audio d'un cours :
> ouverture de chapitre, présentation d'un schéma, d'une fiche, d'un TP, « ce qui est
> attendu ». Le prompt produit une **fiche de production** au format que lit
> `outils/generer_audio.py` ; la génération, elle, se lance ensuite, témoin d'abord.

---

## Ce qui est fixé une fois pour toutes

Ces choix ont été faits par l'auteur, à l'écoute de témoins. Ils ne se rediscutent
pas d'une capsule à l'autre.

| Réglage | Valeur | Où il vit |
|---|---|---|
| Modèle | **Eleven v4** | imposé par `outils/generer_audio.py` (`--modele` seulement pour un essai) |
| Voix | le clone vocal de l'auteur | `outils/elevenlabs.json` (local, jamais lu ni affiché) |
| Accent | **« strong Parisian French accent »** sur les pistes françaises | ajouté par le générateur à chaque balise — **jamais écrit dans les scripts** |
| Pistes anglaises | sans accent ajouté (le clone a déjà le sien) ; `voix_id_en` pour une autre voix | `ACCENTS` dans le générateur |
| Ton | pédagogique, académique, professionnel, motivant ; au vouvoiement | ce prompt |
| Rythme | posé ; « speaking slowly » dans les balises d'une capsule explicative | les scripts |
| Contrôle | débit 105 à 190 mots/min en v4, silence ≤ 3,6 s, fenêtre de durée déduite des mots | le générateur, avant tout dépôt |

**Pourquoi l'accent marqué.** Sur deux témoins, la formulation « natural Parisian French
accent » ne s'entendait pas assez ; l'auteur a retenu la formulation marquée. Toutes les
pistes françaises la portent depuis.

**Pourquoi un témoin.** Une série se paie d'avance et s'écoute après : une voix mal réglée
gâche toutes les pistes à la fois. Le générateur refuse une série tant qu'aucun témoin
n'existe pour le modèle (`--serie` pour passer outre, sciemment).

---

## Le format de la fiche — ce que le générateur lit

Une fiche par famille de capsules, dans `docs/prompts/Capsules_<famille>.md`. Pour chaque
capsule, **ces marqueurs exactement** :

````markdown
## Capsule 3 — Le diagramme de composants

**Emplacement.** Page des schémas, conteneur `voix-sch-composants`.

- **Nom exact du fichier :** `schema-composants.mp3`
- **Emplacement exact :** `site/assets/media/voix/schema-composants.mp3`

- [ ] Témoin écouté et validé par l'auteur
- [ ] Capsule générée, contrôlée et déposée

**▶️ Script ElevenLabs**

```
[confident, warm, speaking slowly] Premier paragraphe…

[measured, speaking slowly] Deuxième paragraphe…
```

**📄 Transcription affichée sur la page**

```
Le même texte, sans les balises, avec l'orthographe d'affichage.
```
````

- Le **nom du fichier** est celui que réclame la page (`RDCX.voice`, ou `capsuleSrc` dans
  `TEXTES` pour une page bilingue) : c'est la clé. Une piste anglaise finit par `-en.mp3`.
- La **transcription** se recopie dans la page par `outils/synchroniser_capsules.py` : la
  fiche est la source unique, on ne corrige jamais la transcription dans le HTML.
- Une capsule au format inhabituel peut déclarer sa fenêtre :
  « tolérance 1 min 30 → 2 min 40 ». Le débit et les silences restent contrôlés.

---

## PROMPT À COPIER

```
Tu écris les scripts audio de capsules pour le cours {{TITRE_DU_COURS}}, lus par la voix
clonée de l'auteur en Eleven v4. Tu produis une fiche de production au format exact décrit
dans prompts/14_capsules_audio.md.

CAPSULES À ÉCRIRE : {{LISTE_DES_CAPSULES}} (pour chacune : la page, le conteneur, le nom
exact du fichier, ce qu'elle doit faire comprendre).

SOURCES : le contenu de la page ou du schéma concerné, et les documents de sources/. Tu
n'inventes aucun fait, aucun chiffre, aucun exemple : tu reformules pour l'oreille ce que
le cours dit déjà. Les interdits du cours s'appliquent : {{INTERDITS_DU_COURS}}.

LE TON. Professionnel et académique : des définitions exactes, le vocabulaire du métier, un
raisonnement articulé. Motivant et engageant : on s'adresse à l'étudiant, on lui montre
l'enjeu — son métier, son TP, l'épreuve — et on lui donne envie d'aller plus loin.
Pédagogique : une progression claire, un exemple concret, la nuance qui fait la
différence, une phrase à retenir. Au vouvoiement, toujours. Pas de familiarité, pas
d'emphase creuse.

LE PLAN D'UNE CAPSULE EXPLICATIVE (schéma, notion, fiche) :
1. L'accroche : un enjeu professionnel, un constat ou une question.
2. La définition, précise.
3. La lecture de l'exemple ÉLÉMENT PAR ÉLÉMENT : chaque partie, son rôle, comment la lire.
4. Les liens avec les autres pièces du cours.
5. Le piège le plus fréquent.
6. La phrase à retenir.
Une capsule d'ouverture de chapitre, plus courte, situe : ce que le chapitre permet de
faire, pourquoi maintenant, comment il s'articule avec le TP.

LA MISE EN VOIX (Eleven v4) :
- Une balise de jeu en anglais au début de chaque paragraphe, courte et professionnelle :
  [confident, warm], [measured], [thoughtful], [engaged], [curious], [serious, measured],
  [encouraging], [warm, encouraging]. Une seconde balise est permise une fois, devant la
  chute d'un paragraphe. Pas de balise ludique, pas de [emphasis], plus de [pause] : la v4
  rythme par la ponctuation.
- Capsule explicative : « speaking slowly » dans chaque balise
  ([thoughtful, speaking slowly]) — l'auteur veut une lecture posée.
- N'écris JAMAIS l'accent dans les balises : le générateur ajoute « strong Parisian French
  accent » aux pistes françaises.
- Deux à quatre points de suspension « … » par script, aux respirations utiles ; des
  phrases courtes ; un paragraphe par idée.
- Écrire pour l'oreille : nombres en lettres (« quatre mille places ») ; sigles épelés
  pointés quand ils s'épellent (« T.P. », « A.P.I. ») ; mots étrangers écrits comme ils se
  prononcent si besoin. La TRANSCRIPTION, elle, garde l'orthographe d'affichage (« TP »,
  « 4 000 »).

LA LONGUEUR : {{DUREE_VISEE}} — compte les mots parlés (balises exclues) : environ 160 à
175 mots par minute en v4 avec « speaking slowly », 175 à 190 sans.

VARIER : chaque capsule a sa propre accroche ; le lien au métier, au TP ou à l'épreuve ne
revient pas sous la même formule d'une capsule à l'autre.

LIVRE : la fiche complète (en-tête « À lire avant de générer », récapitulatif des fichiers
avec durée visée, puis une section par capsule avec les marqueurs exacts). Indique laquelle
servira de TÉMOIN : celle qui exerce le plus la voix (la plus longue, la plus dense).
```

---

## Ensuite : générer

```bash
python3 outils/verifier_elevenlabs.py                       # clé, voix, Eleven v4, quota
python3 outils/generer_audio.py --essai                     # ce qui partirait, et le coût
python3 outils/generer_audio.py --fichier <témoin>.mp3 --temoin   # le témoin, à côté
```

**STOP — l'auteur écoute le témoin** (`outils/quarantaine/temoins/eleven_v4/`). Puis :

```bash
python3 outils/generer_audio.py --chapitre 1                # la série, chapitre par chapitre
python3 outils/synchroniser_capsules.py                     # transcriptions dans les pages
python3 outils/generer_playlist.py                          # index de la playlist
```

- Une prise **rejetée** attend dans `outils/quarantaine/` avec sa raison : on l'écoute ; si
  elle convient, on la déplace à la main, sinon on corrige le script et on régénère.
- Une prise **trop rapide** (plus de 190 mots/min) se reprend une fois ; si elle le reste,
  « speaking slowly » s'ajoute à chaque balise de son script.
- Rien n'est écrasé sans `--force` ; une piste remplacée se garde hors du site
  (`archives/`, jamais publié) si l'auteur veut pouvoir comparer.

## Conseils

- Faites écouter le témoin **sur le lecteur de la page**, pas seulement dans un lecteur
  audio : c'est là qu'on entend si la capsule colle à ce qu'on voit.
- Une capsule par schéma vaut mieux qu'une longue capsule qui les survole tous.
- Si la voix ou le modèle changent, réécoutez un témoin avant de régénérer quoi que ce soit.
