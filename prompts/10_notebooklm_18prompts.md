# Prompts NotebookLM (infographie / slides / podcast)

**Quand l'utiliser** — Une fois que les chapitres de votre cours existent (au moins leur plan détaillé ou leur texte rédigé), pour produire dans **NotebookLM** les trois médias de chaque chapitre du template : (a) l'**infographie de synthèse**, (b) les **slides**, (c) le **podcast** (dialogue pédagogique). Ce fichier vous donne un *générateur de prompts* : Claude lit vos chapitres et vous renvoie, pour chacun, 3 prompts NotebookLM autonomes, prêts à coller, dans les limites des champs de NotebookLM : 4 800 caractères pour le podcast, 3 700 pour les slides, retours à la ligne compris.

> Rappel : NotebookLM travaille à partir des **sources** que vous y déposez (vos chapitres, votre fiche de cours DOCX, vos documents de référence). Les prompts ci-dessous *pilotent* la génération (audio, rapport/infographie, présentation) mais ne remplacent pas les sources : déposez d'abord le bon matériel dans le notebook.

---

## Placeholders à compléter

- `{{SUJET_DU_COURS}}` — intitulé complet du cours.
- `{{PUBLIC_CIBLE}}` — à qui s'adresse le cours (ex. étudiants L3, salariés en reconversion).
- `{{NIVEAU}}` — débutant / intermédiaire / avancé.
- `{{LANGUES}}` — `français seul` **ou** `français + anglais`.
- `{{NB_CHAPITRES}}` — nombre de chapitres à traiter.
- `{{LISTE_DES_CHAPITRES}}` — pour chaque chapitre : numéro, titre, et 1–3 lignes de résumé OU le texte/plan complet.
- `{{DOCUMENTS_DE_REFERENCE}}` — sources déposées dans NotebookLM (titres + nature : loi, norme, rapport, manuel…).
- `{{FIL_ROUGE}}` — scénario continu du cours (ex. une coopérative agricole fictive qui numérise ses ventes), à mobiliser dans les exemples.
- `{{AUTEUR}}` — auteur du cours (mention de crédit).
- `{{LICENCE}}` — licence du contenu (ex. CC BY 4.0).
- `{{CHARTE_VISUELLE}}` — *(optionnel)* couleurs, ambiance, ton visuel (ex. « sobre institutionnel, bleu nuit + accent ocre »).
- `{{DUREE_PODCAST}}` — *(optionnel)* durée visée du podcast par chapitre (ex. 8–12 min).
- `{{CONTRAINTES}}` — *(optionnel)* interdits, sensibilités, vocabulaire imposé, registres à éviter.

---

## PROMPT À COPIER (générateur — à donner à Claude)

> Collez ce bloc dans Claude, complétez les placeholders, et fournissez vos chapitres. Claude vous renverra `3 × {{NB_CHAPITRES}}` prompts NotebookLM prêts à l'emploi.

```
RÔLE
Tu es ingénieur pédagogique et concepteur de contenus NotebookLM. Tu rédiges des
prompts d'instruction que je collerai ensuite dans NotebookLM pour générer, par
chapitre, trois médias : (a) une infographie de synthèse, (b) des slides, (c) un
podcast (dialogue pédagogique audio). Tu n'écris PAS l'infographie, les slides ni le
podcast eux-mêmes : tu écris les PROMPTS qui les feront produire dans NotebookLM.

CONTEXTE DU COURS
- Sujet : {{SUJET_DU_COURS}}
- Public cible : {{PUBLIC_CIBLE}}
- Niveau : {{NIVEAU}}
- Langues : {{LANGUES}}
- Nombre de chapitres : {{NB_CHAPITRES}}
- Chapitres : {{LISTE_DES_CHAPITRES}}
- Documents de référence (sources NotebookLM) : {{DOCUMENTS_DE_REFERENCE}}
- Fil rouge : {{FIL_ROUGE}}
- Auteur : {{AUTEUR}}  | Licence : {{LICENCE}}
- Charte visuelle (optionnel) : {{CHARTE_VISUELLE}}
- Durée podcast visée (optionnel) : {{DUREE_PODCAST}}
- Contraintes : {{CONTRAINTES}}

EXIGENCE D'EXACTITUDE (impérative)
1. Analyse EN DÉTAIL chaque chapitre fourni et les documents de référence AVANT
   d'écrire quoi que ce soit.
2. N'invente RIEN : aucune donnée, chiffre, citation, article de loi, norme ou date
   qui ne figure pas dans les sources. Si une info manque, écris « [à compléter par
   l'auteur] » plutôt que de combler.
3. Chaque prompt doit ordonner à NotebookLM de s'appuyer UNIQUEMENT sur les sources
   du notebook et de citer/renvoyer aux sources quand c'est pertinent.
4. Cohérence stricte : chaque prompt reste fidèle au périmètre, au vocabulaire et aux
   exemples de SON chapitre. Pas de contenu d'un autre chapitre.

CONTRAINTES DE FORMAT DES PROMPTS PRODUITS
- Pour CHAQUE chapitre, produis EXACTEMENT 3 prompts, dans cet ordre : INFOGRAPHIE,
  SLIDES, PODCAST.
- Chaque prompt est AUTONOME (se suffit à lui-même, sans dépendre des autres) et
  conçu pour fonctionner EN UNE SEULE PASSE dans NotebookLM.
- Longueur maximale de chaque prompt, espaces et retours à la ligne compris :
  PODCAST 4 800 caractères, SLIDES 3 700, INFOGRAPHIE 3 700 (par prudence). Vise
  50 caractères de moins : à la copie, un retour à la ligne peut compter double.
  Compte avec un script, pas à l'œil, et indique entre crochets à la fin de chaque
  prompt son nombre exact de caractères, ex. « [1 830 caractères] ».
- Langue des prompts et des livrables : respecte {{LANGUES}}. Si « français +
  anglais », demande une version FR ET une version EN du livrable (deux passes ou
  deux sections clairement séparées) ; sinon, français seul.
- Style des prompts : impératif, précis, opérationnel. Indique au début de chaque
  prompt le type de sortie attendu de NotebookLM (« Génère un rapport / une
  infographie… », « Génère une présentation… », « Génère un épisode audio… »).
- Mentionne l'auteur et la licence à inclure dans le livrable (crédit discret).

SPÉCIFICATIONS PAR TYPE DE MÉDIA

(a) INFOGRAPHIE DE SYNTHÈSE — le prompt doit demander :
- un visuel de synthèse d'UNE page, lisible d'un coup d'œil ;
- un titre clair + le numéro et le titre du chapitre ;
- les 4 à 7 idées-clés du chapitre, hiérarchisées (du général au détail) ;
- les définitions/notions essentielles, un mini-schéma ou une frise si pertinent
  (étapes, cycle, comparaison avant/après), et 1 exemple concret tiré du fil rouge ;
- un encadré « À retenir » (3 puces max) ;
- respect de la charte visuelle si fournie, sinon « sobre, institutionnel, lisible » ;
- consigne d'accessibilité : contrastes suffisants, pas d'info portée par la seule
  couleur, texte court et concret.

(b) SLIDES — le prompt doit demander :
- une présentation de 8 à 14 diapositives pour le chapitre ;
- structure : 1 diapo titre (chapitre, objectifs d'apprentissage), des diapos de
  contenu (1 idée par diapo, titre d'action + 3–5 puces brèves), 1 diapo « exemple
  fil rouge », 1 diapo « À retenir », 1 diapo de transition/ouverture vers le chapitre
  suivant si pertinent ;
- ton qui motive le public ({{PUBLIC_CIBLE}}, {{NIVEAU}}) : accroche en ouverture ;
- des notes de présentateur courtes sous chaque diapo si NotebookLM le permet ;
- mention crédit auteur + licence sur la dernière diapo.

(c) PODCAST (dialogue pédagogique) — le prompt doit demander :
- un épisode audio en dialogue à deux voix (un animateur curieux + un expert
  pédagogue) centré sur CE chapitre, durée {{DUREE_PODCAST}} si fournie ;
- déroulé : accroche/teaser → objectifs → 3 à 5 points-clés expliqués simplement avec
  analogies et un exemple concret du fil rouge → idées reçues corrigées → « à retenir »
  → mini-récap final → teaser du chapitre suivant ;
- ton chaleureux, clair, vivant, sans jargon inutile (et si jargon nécessaire :
  définir) ; rythme dynamique, phrases courtes ;
- rester strictement fidèle aux sources, ne pas inventer d'exemples non sourcés ;
- crédit auteur + licence à l'oral en clôture.

OÙ DÉPOSER LES FICHIERS GÉNÉRÉS (à rappeler en fin de réponse, pas dans les prompts)
Une fois les médias générés dans NotebookLM puis exportés/téléchargés, donne pour
chaque fichier son nom exact et son dossier exact. N est le numéro du chapitre, sans
zéro, celui qui ouvre le nom de sa page (03-….html -> 3) ; c'est ce que lit media.js :
- Infographie  -> site/assets/media/infographies/chapitre-N-infographie.png
- Slides (PDF) -> site/assets/media/slides/chapitre-N-slides.pdf
- Podcast      -> site/assets/media/podcasts/chapitre-N-podcast.fr.mp3
                  (chapitre-N-podcast.en.mp3 pour l'anglais ; sans suffixe de
                  langue pour un cours monolingue ; .m4a accepté aussi)
Conserve les sources/exports bruts hors du site, dans sources-notebooklm/chapitre-N/.
Nomme tout en minuscules, sans espaces ni accents.

SORTIE ATTENDUE DE TA PART (Claude)
Pour chaque chapitre, dans l'ordre :
### Chapitre N — {titre}
1) PROMPT INFOGRAPHIE
   <le prompt, prêt à coller>  [nombre exact de caractères]
2) PROMPT SLIDES
   <le prompt, prêt à coller>  [nombre exact de caractères]
3) PROMPT PODCAST
   <le prompt, prêt à coller>  [nombre exact de caractères]

Termine par le bloc « OÙ DÉPOSER LES FICHIERS GÉNÉRÉS » récapitulatif.
Enregistre le tout dans un fichier Markdown (docs/prompts/PROMPTS-NotebookLM.md) :
c'est de là que je copierai les prompts.
Ne produis que ces prompts et ce récapitulatif. Pas de commentaire superflu.
```

---

## Conseils

- **Déposez d'abord les bonnes sources** dans NotebookLM (chapitres + fiche de cours DOCX + documents de référence). La qualité des trois médias dépend directement de ce qui est dans le notebook : un prompt parfait sur des sources pauvres donnera un média pauvre.
- **Un notebook par cours, généré chapitre par chapitre.** Lancez les prompts un à la fois et vérifiez chaque sortie avant de passer au suivant ; NotebookLM est plus fiable sur des demandes ciblées que sur une consigne monolithique.
- **Limites de NotebookLM** : 4 800 caractères pour le podcast, 3 700 pour les slides, retours à la ligne compris. Si un prompt approche la limite, demandez à Claude de le resserrer plutôt que de couper à l'aveugle.
- **Bilingue** : pour `français + anglais`, générez de préférence FR et EN en deux passes séparées (deux fichiers distincts), c'est plus propre que de mélanger les deux langues dans un même média. Côté template, le sélecteur de langue 🌐 pointera vers la version adéquate.
- **Vérification factuelle obligatoire** : NotebookLM peut paraphraser de travers. Relisez chiffres, dates, articles de loi et citations avant publication — surtout sur un cours réglementaire.
- **Accessibilité** : pour l'infographie en lightbox du template, prévoyez un texte alternatif décrivant le contenu, et vérifiez les contrastes. Pour le podcast, NotebookLM ne fournit pas toujours de transcription : pensez à en générer une (utile pour le glossaire auto-surligné et pour l'accessibilité).
- **Nommage et rangement** : respectez strictement `chapitre-N-…` (N sans zéro : `chapitre-3-slides.pdf`) et l'arborescence `site/assets/media/...` ; c'est ce que `media.js` attend pour relier podcast, slides (popup PDF) et infographie (lightbox) à chaque chapitre. Un autre nom, et le média ne s'affiche pas — sans message d'erreur.
- **Crédit et licence** : laissez la mention `{{AUTEUR}}` + `{{LICENCE}}` discrète mais présente sur chaque média (dernière diapo, coin d'infographie, clôture audio).
