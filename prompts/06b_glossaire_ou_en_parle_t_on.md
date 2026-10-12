# 06 b — Glossaire : « Où en parle-t-on ? »

**Quand l'utiliser**
Une fois le glossaire produit (prompt `06`) et les pages du cours écrites — chapitres, fiches, cas fil rouge, TP, révisions. Ce prompt ajoute, sur chaque terme du glossaire, la liste de **tous les endroits du cours qui l'emploient**, avec un lien qui mène **précisément** à l'endroit, le mot surligné. L'étudiant passe ainsi d'un mot à tout ce que le cours en dit.

À lancer **en fin de production** : la liste se calcule en lisant les pages publiées. Le générateur se relance ensuite après chaque retouche d'une page.

---

## Placeholders à compléter

- `{{SUJET_DU_COURS}}` — intitulé exact du cours.
- `{{PARTIES_DU_SITE}}` — les parties du site, dans l'ordre du cours (ex. `chapitres, Boîte à outils, cas fil rouge, TP, flashcards, QCM d'entraînement, accueil, programme, bibliographie`).
- `{{PAGES_A_EXCLURE}}` — les pages que la fenêtre ne cite pas, en plus du glossaire (ex. une carte qui n'est qu'une liste de noms).
- `{{EXEMPLES_DOUBLE_SENS}}` — quelques mots du glossaire qui sont aussi des mots courants, s'ils sont déjà connus (ex. « Service » dans « mise en service », « Module » pour le module du cours).

---

## PROMPT À COPIER

> ````
> # Glossaire : « Où en parle-t-on ? »
>
> ## Contexte
> Le site du cours « {{SUJET_DU_COURS}} » a une page Glossaire, produite par le générateur du glossaire
> (source unique). Chaque terme y montre sa définition, son équivalent anglais, le chapitre où il est
> introduit et sa fiche.
>
> ## Ce que je veux
> Sur chaque terme du glossaire, un badge « Où en parle-t-on ? (N endroits) », à côté des autres badges.
> Il ouvre une fenêtre qui liste tous les endroits du cours où le terme est employé ; chaque ligne mène
> précisément à son endroit.
>
> ## Règles
> 1. Périmètre : tout le site publié — {{PARTIES_DU_SITE}}. Exclus : la page du glossaire, {{PAGES_A_EXCLURE}},
>    et les PDF (on ne peut pas y viser un endroit précis ; leur contenu reprend les pages web).
> 2. Un endroit : une section (titre h2 ou h3 qui porte une ancre, encadré « À retenir », référence de la
>    bibliographie), une carte de flashcards, une question du QCM. Le texte avant la première ancre forme
>    le haut de la page. Ajouter une ancre là où une partie longue n'en a pas — dans les générateurs des
>    pages, jamais dans du HTML généré.
> 3. Précision : une ligne par endroit (« Chapitre 4 › 3. Le couplage », « Fiche F1-06 › L'essentiel »),
>    avec le nombre d'emplois. Le clic ouvre la page au premier emploi dans l'endroit, déplie le bloc
>    replié qui le contient et surligne le terme (adresse de la forme page?g=terme#ancre), avec un bandeau
>    de retour au glossaire. Flashcards : le lien ouvre la carte à son numéro. QCM : la question s'affiche
>    seule, sans toucher à la série en cours de l'étudiant.
> 4. Un emploi = le terme, ses pluriels et ses formes déclarées (alias, sigles), entre deux limites de mot.
>    Relever dans les pages les formes que le glossaire ne connaît pas encore (« SLI », « manœuvre
>    inverse »…) et les déclarer. Écarter les emplois qui ne désignent pas la notion
>    ({{EXEMPLES_DOUBLE_SENS}}) : une expression, ou une fiche entière où le mot a un autre sens d'un bout à
>    l'autre. Ces exclusions vivent dans la source du glossaire ; rien ne les signale sur la page.
> 5. Ne comptent pas : le code, les schémas, les boutons, la navigation, ce qui est masqué, et ce que les
>    scripts dessinent après coup (quiz des fiches, transcriptions audio, exercices), sauf les flashcards
>    et le QCM, lus dans leurs données. Dans le QCM, seul l'énoncé compte : surligner une proposition
>    soufflerait la réponse.
> 6. La fenêtre : titre « « Terme » dans le cours — N endroits » ; lignes rangées par partie, puis dans
>    l'ordre du cours ; fermeture par ✕, Échap ou clic à côté ; focus gardé dans la fenêtre et rendu au
>    badge ; plein écran sur téléphone ; thème clair et sombre. Un terme employé nulle part n'a pas de badge.
> 7. Rien à la main : le générateur du glossaire calcule les listes ; le script de surlignage applique
>    exactement la même règle que le décompte. Le contrôle (--essai) dit quand les listes ont vieilli, et
>    signale une exclusion qui ne sert plus et une page publiée qu'il ne lit pas.
> 8. Hors périmètre : les info-bulles des chapitres et le glossaire de l'annexe ne changent pas.
>
> ## Méthode
> - Lis d'abord le générateur du glossaire, la page du glossaire et la façon dont chaque type de page est produit.
> - Ne me pose que les questions qui restent ouvertes pour ce cours, une à la fois, cliquables.
> - Relis le contexte des termes les plus employés et des mots courants : propose les exclusions et les alias manquants.
> - Montre-moi trois termes avant de généraliser : un terme central très employé, un terme rare, un terme à double sens.
> - Ouvre au moins quinze endroits variés dans le navigateur : le nombre annoncé doit égaler le nombre surligné.
>   Vérifie aussi la fenêtre sur téléphone et en thème sombre, puis lance les contrôles du projet.
> - Mets à jour la documentation (décisions, guide de production : le glossaire se génère en dernier).
> - À la fin, propose-moi de commiter et pousser, puis demande-moi si je veux déployer.
> ````

---

## Implémentation de référence

Cours « Conception d'architectures logicielles » (dépôt `Cours_Architecture_Logicielle`, décision D70) :

- `outils/glossaire_emplois.py` — le découpage des pages en endroits, les formes, le décompte ;
- `outils/glossaire_cours.py` — `ALIASES` et `EXCLUSIONS` (une expression, ou `"@F4-14"` pour une fiche entière) ;
- `outils/generer_glossaire.py` — écrit `assets/js/glossaire-emplois.js` et `assets/js/glossaire-formes.js` ;
- `assets/js/glossaire-renvoi.js` — le surlignage à l'arrivée, chargé par `navigation.js` quand l'adresse porte `?g=` ;
- `glossaire.html` — le badge et la fenêtre ; `assets/js/flashcards.js` et `QCM/qcm-entrainement.js` — les liens vers une carte ou une question.
