/* =================================================================
   glossaire-tooltip.js — Info-bulles de glossaire dans les chapitres
   Template de site de cours — Mohamed EL AFRIT (MIT / CC BY 4.0)

   Repère une liste curatée de termes-clés dans le texte des chapitres
   (1re occurrence de chaque terme, hors titres / liens / code / citations de loi)
   et y attache une info-bulle (FR/EN + définition + lien vers le glossaire).
   Dépend de window.GLOSSARY (glossaire-data.js).
   Sur une page anglaise (site miroir, en/), les mêmes termes se cherchent par
   leur forme anglaise, et la bulle mène au glossaire anglais.
   ================================================================= */
(function () {
  if (!window.GLOSSARY || !window.GLOSSARY.length) return;
  var sections = document.querySelectorAll('.main-content .content-section');
  if (!sections.length) return;

  /* Les termes rendus interactifs viennent des données du cours, jamais du
     moteur : une liste de notions codée ici rendrait le template inutilisable
     pour toute autre matière. Voir GLOSSARY_CURATED dans glossaire-data.js. */
  var CURATED = window.GLOSSARY_CURATED || [];

  /* La langue de la page. Sur une page anglaise, chaque entrée curatée se cherche
     par sa forme anglaise : le champ en, sans sa parenthèse, et alias.en ; les
     expressions de exclus.en (« pull request ») ne comptent pas. Une bulle par
     entrée et par page : ses formes anglaises sont plusieurs. Sur une page
     française, une bulle par forme de GLOSSARY_CURATED, hors des expressions
     de exclus.fr — la règle de outils/glossaire_emplois.py, dans les deux langues. */
  var LANGUE = (window.TPLI18N && TPLI18N.lang && TPLI18N.lang()) || 'fr';
  var ANGLAIS = LANGUE === 'en';

  function norm(s) { return (s || '').toLowerCase().replace(/\s*\(.*?\)\s*/g, ' ').replace(/\s+/g, ' ').trim(); }
  var byNorm = {};
  window.GLOSSARY.forEach(function (e) { var k = norm(e.fr); if (!byNorm[k]) byNorm[k] = e; });
  var ALIASES = window.GLOSSARY_ALIASES || {};

  function resolve(phrase) {
    var p = norm(phrase);
    if (ALIASES[p]) p = ALIASES[p];
    if (byNorm[p]) return byNorm[p];
    for (var i = 0; i < window.GLOSSARY.length; i++) { var f = norm(window.GLOSSARY[i].fr); if ((' ' + f + ' ').indexOf(' ' + p + ' ') >= 0) return window.GLOSSARY[i]; }
    for (var j = 0; j < window.GLOSSARY.length; j++) { if ((window.GLOSSARY[j].term || '').indexOf(p) >= 0) return window.GLOSSARY[j]; }
    return null;
  }

  var terms = [];
  CURATED.forEach(function (ph) { var e = resolve(ph); if (e) terms.push({ ph: ph, e: e }); });
  /* Le pluriel régulier d'une forme anglaise, sur son dernier mot (« operator » → « operators », « query » →
     « queries ») : les chapitres anglais emploient souvent le pluriel, que la liste française écrit à la main
     (« objectifs pédagogiques »). Ni sigle, ni chiffre, ni locution à mot-outil (« need to know »), ni
     finale qui ne se met pas au pluriel (-ing, -ly…) : une version simplifiée de la règle de
     outils/glossaire_emplois.py (pluriels_en), sans ses pluriels irréguliers. */
  var MOTS_OUTILS_EN = /\b(of|for|to|in|on|with|by|from|and|or|as|at|the|a|an)\b/i;
  function plurielAnglais(f) {
    var m = /^(.*?)([A-Za-z]+)$/.exec(f);
    if (!m || MOTS_OUTILS_EN.test(f) || /^[A-Z0-9]+$/.test(m[2]) || /(ing|ly|able|ible|less|ss)$/i.test(m[2])) return '';
    var mot = m[2];
    if (/(s|x|z|ch|sh)$/i.test(mot)) return m[1] + mot + 'es';
    if (/[^aeiou]y$/i.test(mot)) return m[1] + mot.slice(0, -1) + 'ies';
    return m[1] + mot + 's';
  }
  // Les formes anglaises des entrées curatées, chacune liée à son entrée (cle) : une bulle par entrée.
  function formesAnglaises(liste) {
    var vues = {}, out = [];
    liste.forEach(function (t) {
      var e = t.e, deja = {};
      if (vues[e.fr]) return;
      vues[e.fr] = true;
      [e.en].concat((e.alias && e.alias.en) || []).forEach(function (f) {
        f = String(f || '').replace(/\s*\(.*?\)\s*/g, ' ').replace(/\s+/g, ' ').trim();
        [f, plurielAnglais(f)].forEach(function (g) {
          if (!g || deja[g.toLowerCase()]) return;
          deja[g.toLowerCase()] = true;
          out.push({ ph: g, e: e, cle: 'entree:' + e.fr });
        });
      });
    });
    return out;
  }
  if (ANGLAIS) terms = formesAnglaises(terms);
  terms.sort(function (a, b) { return b.ph.length - a.ph.length; });
  if (!terms.length) return;

  /* Le lien vers le glossaire depend de l'endroit d'ou l'on parle : « ../ »
     depuis /chapitres/, « ./ » depuis la racine. Il etait ecrit en dur pour
     les chapitres, et pointait au-dessus du site sur toute page racine. */
  var BASE_GLOSSAIRE = (/\/chapitres\//.test(location.pathname) ? '../' : './') + 'glossaire.html';
  /* Une page anglaise jumelle (site miroir, en/) renvoie au glossaire anglais s'il
     existe, sinon au glossaire français : la liste des pages traduites
     (langues-data.js) le dit, lue au moment où la bulle s'affiche. */
  // L'ancre d'un terme dans le glossaire, comme la calculent sa page et outils/glossaire_emplois.py.
  function ancre(fr) {
    var s = String(fr || '').toLowerCase().replace(/œ/g, 'oe').replace(/æ/g, 'ae');
    try { s = s.normalize('NFD').replace(/[̀-ͯ]/g, ''); } catch (e) {}
    return 'g-' + s.replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
  }
  function lienGlossaire() {
    var decl = (document.documentElement.getAttribute('data-langues') || '').split(/[\s,]+/);
    if (!window.TPL_RACINE || decl.length !== 1 || decl[0] !== 'en') return BASE_GLOSSAIRE;
    var traduit = (window.TPL_LANGUES || []).indexOf('glossaire.html') >= 0;
    return window.TPL_RACINE + (traduit ? 'en/' : '') + 'glossaire.html';
  }

  function esc(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  function popHtml(e) {
    // def est bilingue ({ fr, en }) dans glossaire-data.js : lue comme une chaîne, la bulle affichait
    // « [object Object] ». La langue de la page choisit ; une chaîne seule (cours d'une langue) reste lue.
    var lg = (window.TPLI18N && TPLI18N.lang && TPLI18N.lang()) || 'fr';
    var d = typeof e.def === 'string' ? e.def : ((e.def && (e.def[lg] || e.def.fr || e.def.en)) || '');
    if (d.length > 180) d = d.slice(0, 178) + '…';
    // Le terme de la page en tête (.gloss-pop-fr), son équivalent dessous (.gloss-pop-en) : sur une page
    // anglaise, le terme anglais d'abord, puis le français. Les classes nomment des places, pas des langues.
    var tete = ANGLAIS ? (e.en || e.fr) : e.fr, autre = ANGLAIS ? e.fr : e.en;
    return '<span class="gloss-pop" role="tooltip">'
      + '<span class="gloss-pop-fr">' + esc(tete) + '</span>'
      + (autre ? '<span class="gloss-pop-en" lang="' + (ANGLAIS ? 'fr' : 'en') + '">' + esc(autre) + '</span>' : '')
      + '<span class="gloss-pop-def">' + esc(d) + '</span>'
      + '<a class="gloss-pop-link" href="' + lienGlossaire() + '#' + ancre(e.fr) + '">' + T('glossaire.voir') + '</a>'
      // La croix ne sert qu'au bandeau du téléphone (voir plus bas) : la feuille de style la masque ailleurs.
      + '<button type="button" class="gloss-pop-close" aria-label="' + esc(T('glossaire.fermerBulle')) + '">✕</button></span>';
  }
  function buildRe(ph) {
    var e = ph.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    try { return new RegExp('(^|[^\\p{L}\\p{N}])(' + e + ')(?![\\p{L}\\p{N}])', 'iu'); }
    catch (x) { return new RegExp('(^|[^A-Za-zÀ-ÿ0-9])(' + e + ')(?![A-Za-zÀ-ÿ0-9])', 'i'); }
  }
  // Les expressions où le mot ne désigne pas la notion (exclus.fr ou exclus.en d'une entrée), dans la langue de la page.
  function buildExclus(e, lg) {
    var x = (e.exclus && e.exclus[lg]) || [];
    if (!x.length) return null;
    var corps = x.map(function (s) { return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }).join('|');
    try { return new RegExp('(^|[^\\p{L}\\p{N}])(' + corps + ')(?![\\p{L}\\p{N}])', 'giu'); }
    catch (err) { return new RegExp('(^|[^A-Za-zÀ-ÿ0-9])(' + corps + ')(?![A-Za-zÀ-ÿ0-9])', 'gi'); }
  }
  var rx = terms.map(function (t) { return { t: t, re: buildRe(t.ph), ex: buildExclus(t.e, ANGLAIS ? 'en' : 'fr') }; });
  // La première occurrence d'un terme dans un texte, hors des expressions écartées (même forme que re.exec).
  function premiere(item, v) {
    if (!item.ex) return item.re.exec(v);
    var zones = [], z, m;
    item.ex.lastIndex = 0;
    while ((z = item.ex.exec(v))) { zones.push([z.index + z[1].length, z.index + z[0].length]); }
    var g = new RegExp(item.re.source, item.re.flags + 'g');
    while ((m = g.exec(v))) {
      var a = m.index + m[1].length, b = a + m[2].length;
      if (!zones.some(function (zz) { return a < zz[1] && b > zz[0]; })) return m;
      g.lastIndex = b;
    }
    return null;
  }

  function excluded(node) {
    var el = node.parentElement;
    while (el && el !== document.body) {
      var tag = el.tagName;
      if (tag === 'A' || tag === 'BUTTON' || tag === 'CODE' || tag === 'PRE' || tag === 'H1' || tag === 'H2' || tag === 'H3' || tag === 'H4' || tag === 'SCRIPT' || tag === 'STYLE') return true;
      var c = el.classList;
      /* hors-glossaire : un homonyme que la page balise elle-même (la « requête »
         HTTP d'une API n'est pas la requête de recherche du glossaire) ; sans lui, la
         bulle donnerait la mauvaise définition. glossaire_emplois.py le saute aussi. */
      if (c && (c.contains('gloss') || c.contains('hors-glossaire') || c.contains('law-ref') || c.contains('takeaways-head') || c.contains('example-box-header') || c.contains('chapter-header'))) return true;
      /* Une page en blocs data-tr porte les deux langues : un terme qui s'écrit de même dans l'autre (« syllabus »,
         « QCM ») prenait sa bulle dans le bloc masqué, et le lecteur n'en voyait aucune. */
      var tr = el.getAttribute('data-tr');
      if (tr && tr !== LANGUE) return true;
      el = el.parentElement;
    }
    return false;
  }

  var used = {};
  sections.forEach(function (sec) {
    var walker = document.createTreeWalker(sec, NodeFilter.SHOW_TEXT, null);
    var nodes = [], n;
    while ((n = walker.nextNode())) nodes.push(n);
    nodes.forEach(function (node) {
      if (!node.nodeValue || !node.nodeValue.trim() || excluded(node)) return;
      for (var k = 0; k < rx.length; k++) {
        var item = rx[k], cle = item.t.cle || item.t.ph; if (used[cle]) continue;
        var m = premiere(item, node.nodeValue);
        if (!m) continue;
        used[cle] = true;
        var idx = m.index + m[1].length, matched = m[2];
        var before = node.nodeValue.slice(0, idx), after = node.nodeValue.slice(idx + matched.length);
        var span = document.createElement('span');
        span.className = 'gloss'; span.setAttribute('tabindex', '0');
        span.innerHTML = esc(matched) + popHtml(item.t.e);
        var frag = document.createDocumentFragment();
        if (before) frag.appendChild(document.createTextNode(before));
        frag.appendChild(span);
        if (after) frag.appendChild(document.createTextNode(after));
        node.parentNode.replaceChild(frag, node);
        return; // un seul terme par nœud de texte
      }
    });
  });

  /* DEUX FAÇONS D'OUVRIR LA BULLE — mécanismes repris du cours d'architecture
     logicielle. Posée en absolu sous son mot, la bulle restait prisonnière de
     son conteneur : dans un tableau à défilement horizontal,
     elle était rognée — réduite à la largeur du mot à 375 px, coupée au bord
     du tableau à 1024 et 1280 px —, et près du bord droit elle faisait
     défiler toute la page de côté.

     EN BANDEAU, jusqu'à 768 px et sur tout écran sans survol (tablette, écran
     tactile), quelle que soit sa largeur : components.css l'ouvre en bandeau
     fixe au bas de l'écran, pleine largeur, quel que soit l'endroit du mot.
     Le survol ne l'y ouvre pas : sur un écran tactile, il reste collé au
     dernier mot touché, et la bulle ne se refermait plus. Elle s'ouvre au
     toucher ou au focus (classe est-ouvert), et se ferme par sa croix, par
     Échap, d'un toucher ailleurs ou quand le focus la quitte.

     EN BULLE, sur un écran à souris : le survol et le focus l'ouvrent en CSS,
     comme avant, et placer() la pose en position fixe sous le mot (au-dessus
     faute de place), gardée dans la fenêtre. Échap l'écarte (classe
     est-masque) sans que le pointeur ni le focus bougent — critère WCAG
     1.4.13 ; elle revient quand le pointeur ou le focus quitte le mot puis y
     revient, ou d'un clic sur le mot.

     La condition du bandeau est écrite deux fois, ici et dans components.css :
     les deux doivent rester identiques. */
  var BANDEAU = window.matchMedia('(max-width: 768px), (hover: none), (pointer: coarse)');
  var ouvert = null;        // le mot dont la bulle est ouverte en bandeau
  var tenu = null;          // le mot refermé à la main qui garde le focus : il ne rouvre pas sa bulle de lui-même
  var etaitOuvert = false;  // le mot touché avait-il déjà sa bulle ouverte ? Un second toucher la referme.
  var dehors = false;       // un toucher commencé hors du mot ouvert et de sa bulle
  var MARGE = 8;            // la bulle de grand écran reste à 8 px des bords de la fenêtre
  var ECART = 6;            // entre le mot et sa bulle ; le pont ::before de components.css le couvre

  function dans(el, sel) { return el && el.closest ? el.closest(sel) : null; }

  // Le bas de l'en-tête fixe : ni le bandeau ni la bulle ne poussent le mot, ni ne se glissent, dessous.
  function plafond() {
    var entete = document.querySelector('.site-header');
    return entete ? entete.getBoundingClientRect().bottom : 0;
  }

  /* ---- Le bandeau ---- */

  function ouvrir(g) {
    if (ouvert === g) return;
    if (ouvert) ouvert.classList.remove('est-ouvert');
    ouvert = g;
    g.classList.add('est-ouvert');
    // Après le défilement que le navigateur fait lui-même vers un élément qui reçoit le focus.
    requestAnimationFrame(function () { if (ouvert === g) degager(g); });
  }

  function fermer() {
    var g = ouvert;
    if (!g) return;
    ouvert = null;
    g.classList.remove('est-ouvert');
    var actif = document.activeElement;
    if (actif && g.contains(actif)) {
      tenu = g;
      // Le focus ne reste pas dans une bulle masquée : il revient au mot, et l'on reprend la lecture de là.
      if (actif !== g) g.focus({ preventScroll: true });
    }
  }

  /* Le bandeau ne doit pas cacher le mot qui l'a ouvert : un mot touché ou
     atteint au clavier en bas de l'écran disparaîtrait dessous, focus
     compris. La page remonte juste assez, sans pousser le mot sous l'en-tête. */
  function degager(g) {
    var pop = g.querySelector('.gloss-pop');
    if (!pop) return;
    var mot = g.getBoundingClientRect(), haut = pop.getBoundingClientRect().top;
    var d = Math.min(mot.bottom + 8 - haut, mot.top - plafond() - 8);
    if (d > 0) window.scrollBy(0, d);
  }

  /* ---- La bulle de grand écran ---- */

  /* Le mot est-il caché : sous l'en-tête fixe, sous le bas de la fenêtre, ou
     hors de la partie visible d'un conteneur qui le rogne (un tableau qu'on a
     fait défiler) ? Posée en absolu, la bulle disparaissait avec lui ; fixe,
     elle resterait seule à l'écran, attachée à rien. */
  function cache(g, entete) {
    var a = g.getBoundingClientRect();
    if (a.bottom <= entete || a.top >= document.documentElement.clientHeight) return true;
    for (var el = g.parentElement; el && el !== document.body; el = el.parentElement) {
      var st = getComputedStyle(el);
      if (st.overflowX === 'visible' && st.overflowY === 'visible') continue;
      var b = el.getBoundingClientRect();
      if (!b.width && !b.height) continue;
      if (a.right <= b.left || a.left >= b.right || a.bottom <= b.top || a.top >= b.bottom) return true;
    }
    return false;
  }

  /* Repris du cours d'architecture logicielle : la bulle en position fixe,
     calculée à l'ouverture à partir du mot dans la fenêtre, gardée dans la
     fenêtre, retournée au-dessus du mot quand la place manque dessous. Elle
     reste dans le DOM sous son mot : le survol de la bulle la garde ouverte. */
  function placer(g) {
    var pop = g.querySelector('.gloss-pop');
    if (!pop || BANDEAU.matches) return;
    var s = pop.style, de = document.documentElement;
    /* Mesure à blanc, la bulle posée en (0, 0) : le coin relevé est celui de
       son bloc conteneur. C'est le coin de la fenêtre, sauf sous un ancêtre
       transformé — une section le temps de sa révélation (animations.js) —,
       qui retient un élément fixe : on retranche ce décalage. */
    s.position = 'fixed'; s.left = '0px'; s.top = '0px';
    s.display = 'block'; s.visibility = 'hidden';
    var o = pop.getBoundingClientRect(), r = g.getBoundingClientRect();
    var entete = plafond(), ciel = entete + MARGE, bas = de.clientHeight - MARGE;
    // clientWidth et non innerWidth : la bulle ne passe pas sous la barre de défilement verticale.
    var x = Math.max(MARGE, Math.min(r.left, de.clientWidth - o.width - MARGE));
    var y = r.bottom + ECART, dessus = false;
    if (y + o.height > bas) {
      if (r.top - ECART - o.height >= ciel) { y = r.top - ECART - o.height; dessus = true; }
      // Ni dessous ni dessus : elle tient dans la fenêtre, quitte à couvrir le mot, qu'elle répète en tête.
      else y = Math.max(ciel, bas - o.height);
    }
    s.left = Math.round(x - o.left) + 'px';
    s.top = Math.round(y - o.top) + 'px';
    pop.classList.toggle('au-dessus', dessus);
    s.display = '';
    s.visibility = cache(g, entete) ? 'hidden' : '';
  }

  /* Une bulle ouverte suit son mot : défilement de la page ou d'un tableau
     (capture : le défilement d'un élément ne remonte pas), redimensionnement,
     fin de la révélation d'une section, qui la déplace et rend la bulle à la
     fenêtre. */
  var prevu = 0;
  function replacer() {
    prevu = 0;
    if (BANDEAU.matches) return;
    document.querySelectorAll('.gloss:hover, .gloss:focus-within').forEach(function (g) {
      if (!g.classList.contains('est-masque')) placer(g);
    });
  }
  function replacerBientot() { if (!prevu) prevu = requestAnimationFrame(replacer); }
  window.addEventListener('scroll', replacerBientot, true);
  window.addEventListener('resize', replacerBientot);
  document.addEventListener('transitionend', replacerBientot);

  function masquer(g) {
    g.classList.add('est-masque');
    var actif = document.activeElement;
    // Le focus ne reste pas dans une bulle masquée : il revient au mot, comme au bandeau.
    if (actif && actif !== g && g.contains(actif)) g.focus({ preventScroll: true });
  }

  /* ---- Les écouteurs ---- */

  /* Un écouteur sur chaque mot, et non un seul sur le document : Safari
     sur iPhone n'envoie pas le clic d'un toucher sur un élément qui n'en
     écoute aucun. */
  function surClic(e) {
    var g = e.currentTarget;
    if (!BANDEAU.matches) {
      // Un clic sur le mot rouvre la bulle qu'Échap avait écartée : c'est une demande explicite.
      if (g.classList.contains('est-masque') && !dans(e.target, '.gloss-pop')) { g.classList.remove('est-masque'); placer(g); }
      return;
    }
    if (dans(e.target, '.gloss-pop-close')) fermer();
    else if (!dans(e.target, '.gloss-pop')) {      // le lien de la bulle suit son cours
      if (etaitOuvert && ouvert === g) fermer();
      else { tenu = null; ouvrir(g); }
    }
    etaitOuvert = false;
  }
  // Le pointeur qui arrive du dehors sur le mot (ou sur sa bulle) rouvre une bulle écartée, et la place.
  function surEntree(e) {
    if (BANDEAU.matches) return;
    var g = e.currentTarget;
    g.classList.remove('est-masque');
    placer(g);
  }
  document.querySelectorAll('.gloss').forEach(function (g) {
    g.addEventListener('click', surClic);
    g.addEventListener('mouseenter', surEntree);
  });

  /* Toucher ailleurs ferme le bandeau ; faire défiler la page, non : un
     toucher qui devient un défilement finit en pointercancel, pas en
     pointerup. On lit la page, le bandeau reste. */
  document.addEventListener('pointerdown', function (e) {
    var dedans = !!(ouvert && ouvert.contains(e.target));
    dehors = !!ouvert && !dedans;
    etaitOuvert = dedans && !dans(e.target, '.gloss-pop');
  }, true);
  document.addEventListener('pointercancel', function () { dehors = false; etaitOuvert = false; }, true);
  document.addEventListener('pointerup', function (e) {
    if (dehors && ouvert && !ouvert.contains(e.target)) fermer();
    dehors = false;
  }, true);

  /* Au clavier. Bandeau : le focus ouvre la bulle, la quitter la referme.
     Bulle : le focus venu du dehors rouvre une bulle écartée — celui qui va
     du mot à son lien, ou qui y revient, non — et la place. */
  document.addEventListener('focusin', function (e) {
    var g = dans(e.target, '.gloss');
    if (!g) return;
    if (BANDEAU.matches) { if (g !== tenu) ouvrir(g); return; }
    if (!(e.relatedTarget && g.contains(e.relatedTarget))) g.classList.remove('est-masque');
    placer(g);
  });
  document.addEventListener('focusout', function (e) {
    var g = dans(e.target, '.gloss');
    if (!g || (e.relatedTarget && g.contains(e.relatedTarget))) return;
    if (tenu === g) tenu = null;
    if (ouvert === g) fermer();
  });
  // Échap ferme le bandeau ; sur grand écran, il écarte les bulles ouvertes au survol ou au focus.
  document.addEventListener('keydown', function (e) {
    if (!(e.key === 'Escape' || e.key === 'Esc' || e.keyCode === 27)) return;
    if (ouvert) { fermer(); return; }
    if (BANDEAU.matches) return;
    document.querySelectorAll('.gloss:hover, .gloss:focus-within').forEach(function (g) {
      if (!g.classList.contains('est-masque')) masquer(g);
    });
  });

  /* Une rotation, un redimensionnement, une souris branchée sur une tablette font
     passer d'un mode à l'autre : l'état suit, et chaque mode efface les traces de
     l'autre — la position calculée d'une bulle n'a rien à faire dans le bandeau.
     L'impression, non : Chrome met la page au format du papier, franchit le seuil et
     le signale ; un mot qui avait le focus sur grand écran ouvrait alors son bandeau
     le temps de l'impression. */
  var impression = false;
  window.addEventListener('beforeprint', function () { impression = true; });
  window.addEventListener('afterprint', function () { impression = false; });
  function changement() {
    if (impression) return;
    tenu = null;
    document.querySelectorAll('.gloss').forEach(function (g) {
      g.classList.remove('est-masque');
      var pop = g.querySelector('.gloss-pop');
      if (pop) { pop.removeAttribute('style'); pop.classList.remove('au-dessus'); }
    });
    if (!BANDEAU.matches) {
      if (ouvert) ouvert.classList.remove('est-ouvert');
      ouvert = null;
      replacer();
      return;
    }
    var g = dans(document.activeElement, '.gloss');
    if (g) ouvrir(g);
  }
  if (BANDEAU.addEventListener) BANDEAU.addEventListener('change', changement);
  else if (BANDEAU.addListener) BANDEAU.addListener(changement);
})();
