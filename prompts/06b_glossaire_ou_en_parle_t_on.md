# 06 b · Glossaire : « Où en parle-t-on ? »

**Quand l'utiliser**
Une fois le glossaire produit (prompt `06`) et les pages du cours écrites (chapitres, fiches, cas fil rouge, TP,
révisions). Sous chaque terme du glossaire, la liste « Où en parle-t-on ? » mène à **tous les endroits du cours qui
l'emploient**, avec le nombre d'emplois. Ce prompt la rend juste pour le cours : les bonnes formes de chaque terme,
les emplois d'un autre sens écartés, les bonnes pages exclues.

À lancer **en fin de production** : la liste se calcule en lisant les pages publiées. Le générateur se relance
ensuite après chaque retouche d'une page.

> **Le mécanisme est celui du gabarit.** `outils/glossaire_emplois.py` compte les emplois, section par section et
> dans chaque langue (français, anglais, arabe), puis écrit `site/assets/js/glossaire-emplois.js`. La page
> `glossaire.html` les affiche sous chaque terme, en liste dépliable, avec une ancre par terme (`#g-…`) que vise
> l'info-bulle des chapitres. Le cours l'adapte par ses données, sans le réécrire : les champs `alias` et `exclus`
> de `glossaire-data.js`, la liste `EXCLUES` du générateur, la balise `hors-glossaire` des pages. La version plus
> riche du cours d'architecture logicielle (fenêtre, surlignage à l'arrivée, flashcards et QCM comptés) est décrite
> à la fin ; le gabarit ne l'a pas encore.

---

## Placeholders à compléter

- `{{SUJET_DU_COURS}}` : intitulé exact du cours.
- `{{PAGES_A_EXCLURE}}` : les pages que la liste ne cite pas, en plus de celles qu'exclut déjà le générateur (le
  glossaire, la page « À propos », la correction et le tableau de bord du QCM, les pages Podcasts et Polycopié, les
  zones protégées) ; ex. une carte qui n'est qu'une liste de noms.
- `{{EXEMPLES_DOUBLE_SENS}}` : quelques mots du glossaire qui sont aussi des mots courants, s'ils sont déjà connus
  (ex. « Service » dans « mise en service », « Module » pour le module du cours).

---

## PROMPT À COPIER

> ````
> # Glossaire : « Où en parle-t-on ? »
>
> ## Contexte
> Le site du cours « {{SUJET_DU_COURS}} » est né du gabarit. Sa page Glossaire est dessinée par son script d'après
> glossaire-data.js (source unique). Sous chaque terme employé, la liste dépliable « Où en parle-t-on ? » est
> calculée section par section par outils/glossaire_emplois.py, qui écrit site/assets/js/glossaire-emplois.js.
>
> ## Ce que je veux
> Que chaque liste soit juste pour ce cours : chaque emploi du terme compté, aucun emploi d'un autre sens, aucune
> page qui ne doit pas y figurer. Le mécanisme du gabarit reste tel quel ; tu l'adaptes par ses données, sans
> réécrire ni la page du glossaire ni le générateur.
>
> ## Règles
> 1. Périmètre : les pages publiées du site, dans chaque langue. Le générateur exclut déjà le glossaire, la page
>    « À propos », la correction et le tableau de bord du QCM, les pages Podcasts et Polycopié, les zones protégées
>    et ce que le déployeur ne publie pas. Ajoute à EXCLUES : {{PAGES_A_EXCLURE}}.
> 2. Un endroit : une section, c'est-à-dire un titre h2 ou h3 qui porte un id. Le texte avant la première ancre
>    forme le haut de la page. Là où une partie longue n'a pas d'ancre, ajoute-la dans la source de la page (la
>    page elle-même, ou le générateur qui l'écrit), jamais dans du HTML généré.
> 3. Un emploi : l'intitulé du terme sans sa parenthèse, ses alias et leurs pluriels, entre deux limites de mot.
>    Relève dans les pages les formes que le glossaire ne connaît pas encore (un sigle, un synonyme) et déclare-les
>    dans alias, langue par langue. En arabe, faute de règle de pluriel, chaque autre forme s'y écrit.
> 4. Un autre sens : les expressions où le mot ne désigne pas la notion ({{EXEMPLES_DOUBLE_SENS}}) vont dans le
>    champ exclus du terme. Un homonyme isolé se balise dans la page, <span class="hors-glossaire">…</span> : il
>    n'a alors ni info-bulle ni emploi. Rien ne signale ces exclusions sur la page.
> 5. Ne comptent pas : le code, les schémas, les boutons, la navigation, ce qui est masqué, les blocs de l'autre
>    langue.
> 6. Rien à la main : glossaire-emplois.js est généré. Relance python3 outils/glossaire_emplois.py après toute
>    retouche d'une page ; avec --essai, il dit si les listes ont vieilli.
> 7. Hors périmètre : la page du glossaire, son affichage et les info-bulles des chapitres ne changent pas. Une
>    fenêtre, un surlignage à l'arrivée ou des liens vers les flashcards et le QCM relèvent du gabarit ; ils ne se
>    construisent pas dans ce cours.
>
> ## Méthode
> - Lis d'abord le générateur, la page du glossaire et la façon dont chaque type de page est produit.
> - Ne me pose que les questions qui restent ouvertes pour ce cours, une à la fois, cliquables.
> - Relis le contexte des termes les plus employés et des mots courants : propose les exclusions et les alias
>   manquants.
> - Montre-moi trois termes avant de généraliser : un terme central très employé, un terme rare, un terme à double
>   sens.
> - Ouvre au moins quinze lignes variées dans le navigateur : chaque lien mène à sa section, et le nombre annoncé
>   égale le nombre d'emplois que tu y comptes. Vérifie aussi la page sur téléphone et en thème sombre, puis lance
>   les contrôles du projet (glossaire_emplois.py --essai, verifier_liens.py).
> - Mets à jour la documentation (décisions, guide de production : « Où en parle-t-on ? » se régénère après toute
>   retouche d'une page).
> - À la fin, propose-moi de commiter et pousser, puis demande-moi si je veux déployer.
> ````

---

## La version complète, dans le cours d'architecture logicielle

Le cours « Conception d'architectures logicielles » (dépôt `Cours_Architecture_Logicielle`, décision D70) va plus
loin. Un badge « Où en parle-t-on ? (N endroits) » ouvre une fenêtre. Le clic sur une ligne ouvre la page au premier
emploi, déplie le bloc qui le contient et surligne le terme (`page?g=terme#ancre`), avec un bandeau de retour au
glossaire. Les cartes de flashcards et les questions du QCM d'entraînement comptent aussi ; leur lien ouvre la carte
ou la question seule.

- `outils/glossaire_emplois.py` et `outils/glossaire_emplois_en.py` : le découpage des pages en endroits, les
  formes, le décompte ;
- `outils/glossaire_cours.py` : `ALIASES` et `EXCLUSIONS` (une expression, ou `"@F4-14"` pour une fiche entière) ;
- `outils/generer_glossaire.py` : écrit `assets/js/glossaire-emplois.js` et `assets/js/glossaire-formes.js` ;
- `assets/js/glossaire-renvoi.js` : le surlignage à l'arrivée, chargé par `navigation.js` quand l'adresse porte
  `?g=` ;
- `glossaire.html` : le badge et la fenêtre ; `assets/js/flashcards.js` et `QCM/qcm-entrainement.js`, les liens vers
  une carte ou une question.

Le gabarit ne l'a pas encore : son portage est inscrit au lot 6 du registre du gabarit (décision de l'auteur du
22 novembre 2026). Un cours qui la voudrait avant ce portage en parle d'abord à l'auteur, car la construire dans un
seul cours le ferait diverger du gabarit.
