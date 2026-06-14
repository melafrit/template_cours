/* =================================================================
   glossaire-tooltip.js — Info-bulles de glossaire dans les chapitres
   Cours "Réglementation des données et conformité" — M. EL AFRIT (CC BY-NC-SA 4.0)

   Repère une liste curatée de termes-clés dans le texte des chapitres
   (1re occurrence de chaque terme, hors titres / liens / code / citations de loi)
   et y attache une info-bulle (FR/EN + définition + lien vers le glossaire).
   Dépend de window.GLOSSARY (glossaire-data.js).
   ================================================================= */
(function () {
  if (!window.GLOSSARY || !window.GLOSSARY.length) return;
  var sections = document.querySelectorAll('.main-content .content-section');
  if (!sections.length) return;

  // Termes-clés à rendre interactifs (distinctifs, à forte valeur pédagogique)
  var CURATED = [
    'Cyber Resilience Act', 'clauses contractuelles types', 'responsable de traitement',
    'registre des traitements', "mission d'intérêt public", 'violation de données',
    'privacy by design', 'données sensibles', 'données personnelles', 'donnée personnelle', 'intérêt légitime',
    'vidéoprotection', 'géolocalisation', 'pseudonymisation', 'anonymisation',
    'accountability', 'minimisation', 'sous-traitant', 'base légale', 'profilage',
    'consentement', 'Schrems II', 'SecNumCloud', 'Data Act', 'EBIOS', 'RGPD', 'AIPD',
    'DPO', 'CNIL', 'CEPD', 'ANSSI', 'ENISA', 'AI Act', 'NIS 2', 'SBOM', 'RBAC',
    'DMA', 'DSA', 'DGA', 'biométrie'
  ];

  function norm(s) { return (s || '').toLowerCase().replace(/\s*\(.*?\)\s*/g, ' ').replace(/\s+/g, ' ').trim(); }
  var byNorm = {};
  window.GLOSSARY.forEach(function (e) { var k = norm(e.fr); if (!byNorm[k]) byNorm[k] = e; });
  var ALIASES = { 'donnée personnelle': 'donnée à caractère personnel', 'données personnelles': 'donnée à caractère personnel', 'donnée à caractère personnel': 'donnée à caractère personnel' };

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
  terms.sort(function (a, b) { return b.ph.length - a.ph.length; });
  if (!terms.length) return;

  function esc(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  function popHtml(e) {
    var d = e.def || ''; if (d.length > 180) d = d.slice(0, 178) + '…';
    return '<span class="gloss-pop" role="tooltip">'
      + '<span class="gloss-pop-fr">' + esc(e.fr) + '</span>'
      + (e.en ? '<span class="gloss-pop-en">' + esc(e.en) + '</span>' : '')
      + '<span class="gloss-pop-def">' + esc(d) + '</span>'
      + '<a class="gloss-pop-link" href="../glossaire.html">→ Voir au glossaire</a></span>';
  }
  function buildRe(ph) {
    var e = ph.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    try { return new RegExp('(^|[^\\p{L}\\p{N}])(' + e + ')(?![\\p{L}\\p{N}])', 'iu'); }
    catch (x) { return new RegExp('(^|[^A-Za-zÀ-ÿ0-9])(' + e + ')(?![A-Za-zÀ-ÿ0-9])', 'i'); }
  }
  var rx = terms.map(function (t) { return { t: t, re: buildRe(t.ph) }; });

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
})();
