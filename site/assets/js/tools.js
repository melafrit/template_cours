/* =================================================================
   tools.js — Patrons d'ACTIVITÉS INTERACTIVES réutilisables (bilingues)
   Template de site de cours — Mohamed EL AFRIT (MIT / CC BY 4.0)

   Trois patrons génériques, pilotés par configuration (data { fr, en }),
   à adapter à n'importe quel sujet de cours :
     TPLActivities.decisionWizard(id, cfg)  — assistant de décision pas-à-pas (oui/non -> résultat)
     TPLActivities.checklist(id, cfg)       — checklist à score (N cases cochées -> verdict)
     TPLActivities.classifier(id, cfg)      — quiz de classification (ranger des exemples + feedback)
   Chaque activité se ré-affiche au changement de langue (évènement tpl:langchange).
   Réutilise les classes CSS .rdc-* de components.css.
   ================================================================= */
window.TPLActivities = (function () {
  function lng() { return window.TPLI18N ? TPLI18N.lang() : 'fr'; }
  function L(o) { return (o && typeof o === 'object') ? (o[lng()] || o.fr || o.en || '') : (o || ''); }
  function esc(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  function rich(s) { return esc(s).split('**').map(function (seg, i) { return i % 2 ? '<strong>' + seg + '</strong>' : seg; }).join(''); }
  function UI(k) {
    var d = {
      fr: { restart: '↺ Recommencer', next: 'Suivant ›', yes: 'Oui', no: 'Non', score: 'Score', step: 'Question', of: '/', verdict: 'Résultat' },
      en: { restart: '↺ Restart', next: 'Next ›', yes: 'Yes', no: 'No', score: 'Score', step: 'Question', of: '/', verdict: 'Result' }
    };
    return (d[lng()] || d.fr)[k];
  }
  function head(icon, title) {
    return '<div class="rdc-tool-head"><span class="rdc-tool-ico">' + (icon || '🧩') + '</span><span class="rdc-tool-title">' + esc(L(title)) + '</span></div>';
  }
  function reRender(el, fn) { document.addEventListener('tpl:langchange', function () { if (document.body.contains(el)) fn(); }); }

  /* ---------- 1) Assistant de décision pas-à-pas ---------- */
  // cfg = { icon, title:{fr,en}, steps:[ { q:{fr,en}, result:{ name:{fr,en}, detail:{fr,en} } } ], fallback:{ name, detail } }
  function decisionWizard(id, cfg) {
    var el = document.getElementById(id); if (!el) return;
    el.classList.add('rdc-tool');
    var step = 0;
    function render() {
      var s = cfg.steps[step];
      el.innerHTML = head(cfg.icon || '🧭', cfg.title) + '<div class="rdc-tool-body">'
        + '<div class="rdc-step">' + UI('step') + ' ' + (step + 1) + ' ' + UI('of') + ' ' + cfg.steps.length + '</div>'
        + '<p class="rdc-q">' + rich(L(s.q)) + '</p>'
        + '<div class="rdc-yn"><button type="button" class="rdc-btn rdc-yes">' + UI('yes') + '</button><button type="button" class="rdc-btn">' + UI('no') + '</button></div></div>';
      el.querySelector('.rdc-yes').addEventListener('click', function () { result(cfg.steps[step].result); });
      el.querySelectorAll('.rdc-btn')[1].addEventListener('click', function () { step++; if (step < cfg.steps.length) render(); else result(cfg.fallback); });
    }
    function result(r) {
      el.innerHTML = head(cfg.icon || '🧭', cfg.title) + '<div class="rdc-tool-body"><div class="rdc-result">'
        + '<div class="rdc-tier">' + UI('verdict') + '</div><div class="rdc-amount">' + rich(L(r.name)) + '</div>'
        + '<div class="rdc-ex">' + rich(L(r.detail)) + '</div></div>'
        + '<div class="rdc-tools-row"><button type="button" class="rdc-restart">' + UI('restart') + '</button></div></div>';
      el.querySelector('.rdc-restart').addEventListener('click', function () { step = 0; render(); });
    }
    render();
    reRender(el, function () { step = 0; render(); });
  }

  /* ---------- 2) Checklist à score ---------- */
  // cfg = { icon, title, intro:{fr,en}, items:[{fr,en}], note:{fr,en},
  //         verdicts: [ {min:2, cls:'rdc-tier-2', msg:{fr,en}}, {min:1, cls:'rdc-tier-1', msg:{fr,en}}, {min:0, cls:'', msg:{fr,en}} ] }
  function checklist(id, cfg) {
    var el = document.getElementById(id); if (!el) return;
    el.classList.add('rdc-tool');
    function render() {
      el.innerHTML = head(cfg.icon || '☑️', cfg.title) + '<div class="rdc-tool-body">'
        + (cfg.intro ? '<p class="rdc-q">' + rich(L(cfg.intro)) + '</p>' : '')
        + '<div class="rdc-checks">' + cfg.items.map(function (it, k) { return '<label class="rdc-check"><input type="checkbox" data-i="' + k + '"><span>' + rich(L(it)) + '</span></label>'; }).join('') + '</div>'
        + '<div class="rdc-result rdc-verdict" aria-live="polite"></div>'
        + (cfg.note ? '<p class="rdc-disclaimer">' + rich(L(cfg.note)) + '</p>' : '') + '</div>';
      var verdict = el.querySelector('.rdc-verdict');
      function update() {
        var n = el.querySelectorAll('.rdc-check input:checked').length;
        var v = (cfg.verdicts || []).filter(function (x) { return n >= x.min; }).sort(function (a, b) { return b.min - a.min; })[0];
        verdict.className = 'rdc-result rdc-verdict ' + (v && v.cls || '');
        verdict.innerHTML = v ? rich(L(v.msg)).replace('{n}', n) : '';
      }
      el.querySelectorAll('.rdc-check input').forEach(function (c) { c.addEventListener('change', update); });
      update();
    }
    render();
    reRender(el, render);
  }

  /* ---------- 3) Quiz de classification ---------- */
  // cfg = { icon, title, categories:[{key, label:{fr,en}}], items:[{ ex:{fr,en}, cat:'key', why:{fr,en} }] }
  function classifier(id, cfg) {
    var el = document.getElementById(id); if (!el) return;
    el.classList.add('rdc-tool');
    var i = 0, score = 0;
    var labelOf = {}; cfg.categories.forEach(function (c) { labelOf[c.key] = c.label; });
    function render() {
      if (i >= cfg.items.length) {
        el.innerHTML = head(cfg.icon || '🗂️', cfg.title) + '<div class="rdc-tool-body"><div class="rdc-result"><div class="rdc-amount">' + UI('score') + ' : ' + score + ' ' + UI('of') + ' ' + cfg.items.length + '</div></div>'
          + '<div class="rdc-tools-row"><button type="button" class="rdc-restart">' + UI('restart') + '</button></div></div>';
        el.querySelector('.rdc-restart').addEventListener('click', function () { i = 0; score = 0; render(); });
        return;
      }
      var it = cfg.items[i];
      el.innerHTML = head(cfg.icon || '🗂️', cfg.title) + '<div class="rdc-tool-body">'
        + '<div class="rdc-step">' + (i + 1) + ' ' + UI('of') + ' ' + cfg.items.length + ' · ' + UI('score') + ' ' + score + '</div>'
        + '<p class="rdc-q">«&nbsp;' + rich(L(it.ex)) + '&nbsp;»</p>'
        + '<div class="rdc-opts">' + cfg.categories.map(function (c) { return '<button type="button" class="rdc-opt" data-k="' + c.key + '">' + esc(L(c.label)) + '</button>'; }).join('') + '</div>'
        + '<div class="rdc-feedback" aria-live="polite"></div>'
        + '<div class="rdc-tools-row"><button type="button" class="rdc-next2" hidden>' + UI('next') + '</button></div></div>';
      var opts = el.querySelectorAll('.rdc-opt'), fb = el.querySelector('.rdc-feedback'), next = el.querySelector('.rdc-next2'), done = false;
      opts.forEach(function (b) {
        b.addEventListener('click', function () {
          if (done) return; done = true;
          var ok = b.getAttribute('data-k') === it.cat; if (ok) score++;
          opts.forEach(function (x) { var k = x.getAttribute('data-k'); if (k === it.cat) x.classList.add('is-correct'); else if (x === b) x.classList.add('is-wrong'); x.disabled = true; });
          fb.innerHTML = (ok ? '<span class="fb-ok">✅</span> ' : '<span class="fb-no">❌</span> ') + '<strong>' + esc(L(labelOf[it.cat])) + '.</strong> ' + rich(L(it.why));
          fb.classList.add('show'); next.hidden = false;
        });
      });
      next.addEventListener('click', function () { i++; render(); });
    }
    render();
    reRender(el, function () { i = 0; score = 0; render(); });
  }

  return { decisionWizard: decisionWizard, checklist: checklist, classifier: classifier };
})();
