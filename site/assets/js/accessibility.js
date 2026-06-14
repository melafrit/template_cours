/* =================================================================
   accessibility.js — Confort de lecture & accessibilité
   Cours "Réglementation des données et conformité" — M. EL AFRIT (CC BY-NC-SA 4.0)

   - Bouton ♿ dans l'en-tête -> petit panneau de réglages
   - Taille du texte (A- / A+) via mise à l'échelle de la racine (--fs-scale)
   - Mode "lecture adaptée" (DYS) : police Atkinson Hyperlegible (chargée à la
     demande) + interligne / espacement renforcés
   - Lien d'évitement "Aller au contenu" (skip-link)
   - Réglages persistants (localStorage), motif identique au thème
   ================================================================= */
(function () {
  var root = document.documentElement;
  var KEY = 'rdc-a11y';
  var SCALES = [0.9, 1.0, 1.1, 1.2, 1.3];
  var ATKINSON = 'https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&display=swap';

  function load() { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; } }
  function save(s) { try { localStorage.setItem(KEY, JSON.stringify(s)); } catch (e) {} }

  var state = load();
  if (typeof state.scale !== 'number') state.scale = 1.0;
  if (typeof state.dys !== 'boolean') state.dys = false;

  var atkinsonLoaded = false;
  function ensureAtkinson() {
    if (atkinsonLoaded || document.querySelector('link[data-atkinson]')) { atkinsonLoaded = true; return; }
    var l = document.createElement('link');
    l.rel = 'stylesheet'; l.href = ATKINSON; l.setAttribute('data-atkinson', '');
    document.head.appendChild(l); atkinsonLoaded = true;
  }

  function apply() {
    root.style.setProperty('--fs-scale', String(state.scale));
    if (state.dys) { root.classList.add('a11y-dys'); ensureAtkinson(); }
    else { root.classList.remove('a11y-dys'); }
  }
  apply(); // applique dès le chargement du script (limite le "flash")

  function nearestIndex() {
    var best = 0, bd = Infinity;
    for (var i = 0; i < SCALES.length; i++) {
      var d = Math.abs(SCALES[i] - state.scale);
      if (d < bd) { bd = d; best = i; }
    }
    return best;
  }

  function build() {
    // -- Lien d'évitement vers le contenu --
    if (!document.querySelector('.skip-link')) {
      var main = document.querySelector('main.main-content') || document.querySelector('main')
        || document.querySelector('[role="main"]') || document.querySelector('.main-wrapper')
        || document.querySelector('.landing-section') || document.querySelector('section');
      if (main) {
        if (!main.id) main.id = 'main-content';
        var sk = document.createElement('a');
        sk.className = 'skip-link'; sk.href = '#' + main.id; sk.textContent = 'Aller au contenu';
        document.body.insertBefore(sk, document.body.firstChild);
      }
    }

    // -- Bouton ♿ dans l'en-tête --
    var hr = document.querySelector('.header-right');
    if (!hr) return;

    var btn = document.createElement('button');
    btn.type = 'button'; btn.className = 'a11y-toggle';
    btn.setAttribute('aria-label', "Réglages d'accessibilité et de lecture");
    btn.setAttribute('aria-expanded', 'false');
    btn.innerHTML = '♿'; // ♿

    var panel = document.createElement('div');
    panel.className = 'a11y-panel'; panel.hidden = true;
    panel.setAttribute('role', 'dialog');
    panel.setAttribute('aria-label', 'Réglages de lecture');
    panel.innerHTML =
        '<div class="a11y-row a11y-title">Confort de lecture</div>'
      + '<div class="a11y-row"><span class="a11y-label">Taille du texte</span>'
      + '<span class="a11y-size">'
      + '<button type="button" class="a11y-btn" data-act="dec" aria-label="Réduire le texte">A−</button>'
      + '<span class="a11y-pct" aria-live="polite">100 %</span>'
      + '<button type="button" class="a11y-btn a11y-btn-plus" data-act="inc" aria-label="Agrandir le texte">A+</button>'
      + '</span></div>'
      + '<div class="a11y-row"><span class="a11y-label">Lecture adaptée (DYS)</span>'
      + '<button type="button" id="a11y-dys" class="a11y-switch" role="switch" aria-checked="false" aria-label="Activer la lecture adaptée"><span></span></button></div>'
      + '<div class="a11y-row a11y-hint">Police « Atkinson Hyperlegible » + espacement renforcé.</div>'
      + '<div class="a11y-row"><button type="button" class="a11y-reset" data-act="reset">↺ Réinitialiser</button></div>';

    var themeBtn = hr.querySelector('.theme-toggle');
    if (themeBtn) hr.insertBefore(btn, themeBtn); else hr.appendChild(btn);
    document.body.appendChild(panel);

    function refresh() {
      panel.querySelector('.a11y-pct').textContent = Math.round(state.scale * 100) + ' %';
      var sw = panel.querySelector('#a11y-dys');
      sw.classList.toggle('on', state.dys);
      sw.setAttribute('aria-checked', state.dys ? 'true' : 'false');
    }
    refresh();

    function positionPanel() {
      var r = btn.getBoundingClientRect();
      panel.style.top = (r.bottom + 8) + 'px';
      panel.style.right = Math.max(8, window.innerWidth - r.right) + 'px';
    }
    function openPanel() { positionPanel(); panel.hidden = false; btn.setAttribute('aria-expanded', 'true'); }
    function closePanel() { panel.hidden = true; btn.setAttribute('aria-expanded', 'false'); }

    btn.addEventListener('click', function (e) { e.stopPropagation(); if (panel.hidden) openPanel(); else closePanel(); });
    document.addEventListener('click', function (e) { if (!panel.hidden && !panel.contains(e.target) && e.target !== btn) closePanel(); });
    document.addEventListener('keydown', function (e) { if (!panel.hidden && (e.key === 'Escape' || e.key === 'Esc')) { closePanel(); btn.focus(); } });
    window.addEventListener('resize', function () { if (!panel.hidden) positionPanel(); });

    panel.addEventListener('click', function (e) {
      var t = e.target.closest('[data-act], .a11y-switch');
      if (!t) return;
      if (t.id === 'a11y-dys') { state.dys = !state.dys; }
      else {
        var act = t.getAttribute('data-act');
        if (act === 'inc') { state.scale = SCALES[Math.min(SCALES.length - 1, nearestIndex() + 1)]; }
        else if (act === 'dec') { state.scale = SCALES[Math.max(0, nearestIndex() - 1)]; }
        else if (act === 'reset') { state.scale = 1.0; state.dys = false; }
      }
      apply(); save(state); refresh();
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', build);
  else build();
})();
