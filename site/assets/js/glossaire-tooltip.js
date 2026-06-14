/* =================================================================
   glossaire-tooltip.js — Info-bulles de glossaire dans les chapitres
   Template de site de cours — Mohamed EL AFRIT (MIT / CC BY 4.0)

   Repère une liste curatée de termes-clés dans le texte des chapitres
   (1re occurrence de chaque terme, hors titres / liens / code / citations de loi)
   et y attache une info-bulle (terme + définition + exemple + lien vers le glossaire).
   Bilingue : window.GLOSSARY est une liste d'entrées
       { fr:'terme FR', en:'term EN', def:{ fr, en }, ex:{ fr, en } }
   On repère les termes dans la LANGUE COURANTE (entry[lng()]) et on ré-affiche
   tout au changement de langue (« tpl:langchange », voir i18n.js).
   Dépend de window.GLOSSARY (glossaire-data.js).
   ================================================================= */
(function () {
  if (!window.GLOSSARY || !window.GLOSSARY.length) return;
  var sections = document.querySelectorAll('.main-content .content-section');
  if (!sections.length) return;

  // -- i18n : libellés d'interface --
  var S = {
    fr: { seeGlossary: '→ Voir au glossaire' },
    en: { seeGlossary: '→ See in glossary' }
  };
  function lng() { return window.TPLI18N ? TPLI18N.lang() : 'fr'; }
  function t(k) { return (S[lng()] || S.fr)[k] || S.fr[k]; }

  // -- Champs bilingues d'une entrée --
  // term(e) : libellé du terme dans la langue courante ; def(e)/ex(e) : idem
  function term(e) { var v = e[lng()]; return v != null ? v : (e.fr != null ? e.fr : e.en); }
  function defOf(e) { var d = e.def; if (d == null) return ''; if (typeof d === 'object') { var v = d[lng()]; return v != null ? v : (d.fr != null ? d.fr : (d.en != null ? d.en : '')); } return d; }
  function exOf(e) { var x = e.ex; if (x == null) return ''; if (typeof x === 'object') { var v = x[lng()]; return v != null ? v : (x.fr != null ? x.fr : (x.en != null ? x.en : '')); } return x; }

  // Termes-clés à rendre interactifs (distinctifs, à forte valeur pédagogique).
  // Par langue : on repère ces formulations dans le texte de la langue courante.
  // Termes à repérer dans le texte : dérivés du glossaire lui-même (dans la langue
  // courante). Générique — aucune liste codée en dur. Pour ne lier qu'une sélection,
  // ajoutez « curated: true » aux entrées voulues de GLOSSARY et décommentez le filtre.
  function curated() {
    return window.GLOSSARY
      // .filter(function (e) { return e.curated; })   // <- décommentez pour ne lier qu'une sélection
      .map(function (e) { return term(e); })
      .filter(Boolean);
  }

  function norm(s) { return (s || '').toLowerCase().replace(/\s*\(.*?\)\s*/g, ' ').replace(/\s+/g, ' ').trim(); }

  // Index des entrées par libellé normalisé dans la langue courante.
  var byNorm;
  function buildIndex() {
    byNorm = {};
    window.GLOSSARY.forEach(function (e) { var k = norm(term(e)); if (k && !byNorm[k]) byNorm[k] = e; });
  }

  var ALIASES = {
    fr: { 'donnée personnelle': 'donnée à caractère personnel', 'données personnelles': 'donnée à caractère personnel', 'donnée à caractère personnel': 'donnée à caractère personnel' },
    en: {}
  };
  function aliases() { return ALIASES[lng()] || {}; }

  function resolve(phrase) {
    var p = norm(phrase);
    var al = aliases();
    if (al[p]) p = al[p];
    if (byNorm[p]) return byNorm[p];
    for (var i = 0; i < window.GLOSSARY.length; i++) { var f = norm(term(window.GLOSSARY[i])); if ((' ' + f + ' ').indexOf(' ' + p + ' ') >= 0) return window.GLOSSARY[i]; }
    for (var j = 0; j < window.GLOSSARY.length; j++) { if (norm(term(window.GLOSSARY[j])).indexOf(p) >= 0) return window.GLOSSARY[j]; }
    return null;
  }

  function esc(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  function popHtml(e) {
    var d = defOf(e) || ''; if (d.length > 180) d = d.slice(0, 178) + '…';
    var x = exOf(e) || '';
    var other = lng() === 'fr' ? e.en : e.fr; // libellé dans l'autre langue (repère)
    return '<span class="gloss-pop" role="tooltip">'
      + '<span class="gloss-pop-fr">' + esc(term(e)) + '</span>'
      + (other ? '<span class="gloss-pop-en">' + esc(other) + '</span>' : '')
      + '<span class="gloss-pop-def">' + esc(d) + '</span>'
      + (x ? '<span class="gloss-pop-ex">' + esc(x) + '</span>' : '')
      + '<a class="gloss-pop-link" href="../glossaire.html">' + esc(t('seeGlossary')) + '</a></span>';
  }
  function buildRe(ph) {
    var e = ph.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    try { return new RegExp('(^|[^\\p{L}\\p{N}])(' + e + ')(?![\\p{L}\\p{N}])', 'iu'); }
    catch (x) { return new RegExp('(^|[^A-Za-zÀ-ÿ0-9])(' + e + ')(?![A-Za-zÀ-ÿ0-9])', 'i'); }
  }

  function excluded(node) {
    var el = node.parentElement;
    while (el && el !== document.body) {
      var tag = el.tagName;
      if (tag === 'A' || tag === 'BUTTON' || tag === 'CODE' || tag === 'PRE' || tag === 'H1' || tag === 'H2' || tag === 'H3' || tag === 'H4' || tag === 'SCRIPT' || tag === 'STYLE') return true;
      var c = el.classList;
      if (c && (c.contains('gloss') || c.contains('law-ref') || c.contains('takeaways-head') || c.contains('example-box-header') || c.contains('chapter-header'))) return true;
      el = el.parentElement;
    }
    return false;
  }

  // Retire les surlignages existants : remplace chaque <span class="gloss"> par son
  // texte (le terme repéré) et re-fusionne les nœuds de texte adjacents.
  function unwrap() {
    sections.forEach(function (sec) {
      var spans = sec.querySelectorAll('span.gloss');
      for (var i = 0; i < spans.length; i++) {
        var sp = spans[i];
        var first = sp.firstChild; // le 1er nœud est le texte du terme (avant la .gloss-pop)
        var label = (first && first.nodeType === 3) ? first.nodeValue : (sp.textContent || '');
        var parent = sp.parentNode;
        if (!parent) continue;
        parent.replaceChild(document.createTextNode(label), sp);
        parent.normalize();
      }
    });
  }

  // Scanne le texte et attache les info-bulles, pour la langue courante.
  function scan() {
    buildIndex();
    var terms = [];
    curated().forEach(function (ph) { var e = resolve(ph); if (e) terms.push({ ph: ph, e: e }); });
    terms.sort(function (a, b) { return b.ph.length - a.ph.length; });
    if (!terms.length) return;
    var rx = terms.map(function (it) { return { t: it, re: buildRe(it.ph) }; });

    var used = {};
    sections.forEach(function (sec) {
      var walker = document.createTreeWalker(sec, NodeFilter.SHOW_TEXT, null);
      var nodes = [], n;
      while ((n = walker.nextNode())) nodes.push(n);
      nodes.forEach(function (node) {
        if (!node.nodeValue || !node.nodeValue.trim() || excluded(node)) return;
        for (var k = 0; k < rx.length; k++) {
          var item = rx[k]; if (used[item.t.ph]) continue;
          var m = item.re.exec(node.nodeValue);
          if (!m) continue;
          used[item.t.ph] = true;
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
  }

  // -- Rendu initial + ré-affichage au changement de langue --
  scan();
  document.addEventListener('tpl:langchange', function () { unwrap(); scan(); });
})();
