/* =================================================================
   accessibility.js — Confort de lecture & accessibilité
   Template de site de cours — Mohamed EL AFRIT (MIT / CC BY 4.0)

   - Bouton ♿ dans l'en-tête -> petit panneau de réglages
   - Taille du texte (A- / A+) via mise à l'échelle de la racine (--fs-scale)
   - Mode "lecture adaptée" (DYS) : police Atkinson Hyperlegible (déclarée dans
     fonts.css ; le navigateur ne la télécharge que dans ce mode) + interligne /
     espacement renforcés
   - Lien d'évitement "Aller au contenu" (skip-link)
   - Réglages persistants (localStorage), motif identique au thème
   ================================================================= */
(function () {
  var root = document.documentElement;
  var KEY = 'rdc-a11y';
  var SCALES = [0.9, 1.0, 1.1, 1.2, 1.3];

  function load() { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; } }
  function save(s) { try { localStorage.setItem(KEY, JSON.stringify(s)); } catch (e) {} }

  var state = load();
  if (typeof state.scale !== 'number') state.scale = 1.0;
  if (typeof state.dys !== 'boolean') state.dys = false;

  function apply() {
    root.style.setProperty('--fs-scale', String(state.scale));
    if (state.dys) { root.classList.add('a11y-dys'); }
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
        sk.className = 'skip-link'; sk.href = '#' + main.id;
        // Écrit en dur, il restait en français sur les pages anglaises ; il suit aussi une bascule dans la page (data-tr).
        var libelle = function () { sk.textContent = window.T ? T('a11y.allerContenu') : 'Aller au contenu'; };
        libelle();
        document.addEventListener('tpl:langchange', libelle);
        document.body.insertBefore(sk, document.body.firstChild);
      }
    }

    // -- Bouton ♿ dans l'en-tête --
    var hr = document.querySelector('.header-right');
    if (!hr) return;

    var btn = document.createElement('button');
    btn.type = 'button'; btn.className = 'a11y-toggle';
    btn.setAttribute('aria-expanded', 'false');
    btn.innerHTML = '♿'; // ♿

    var panel = document.createElement('div');
    panel.className = 'a11y-panel'; panel.hidden = true;
    panel.setAttribute('role', 'dialog');

    var themeBtn = hr.querySelector('.theme-toggle');
    if (themeBtn) hr.insertBefore(btn, themeBtn); else hr.appendChild(btn);
    document.body.appendChild(panel);

    function refresh() {
      panel.querySelector('.a11y-pct').textContent = Math.round(state.scale * 100) + ' %';
      var sw = panel.querySelector('#a11y-dys');
      sw.classList.toggle('on', state.dys);
      sw.setAttribute('aria-checked', state.dys ? 'true' : 'false');
    }
    // Les libellés viennent de ui-labels.js : écrits en dur, ils laissaient le panneau en français sur une page
    // anglaise. Une page en blocs data-tr les réécrit quand le lecteur change de langue.
    function remplir() {
      btn.setAttribute('aria-label', T('a11y.titre'));
      panel.setAttribute('aria-label', T('a11y.court'));
      panel.innerHTML =
          '<div class="a11y-row a11y-title">' + T('a11y.confort') + '</div>'
        + '<div class="a11y-row"><span class="a11y-label">' + T('a11y.taille') + '</span>'
        + '<span class="a11y-size">'
        + '<button type="button" class="a11y-btn" data-act="dec" aria-label="' + T('a11y.reduire') + '">A−</button>'
        + '<span class="a11y-pct" aria-live="polite">100 %</span>'
        + '<button type="button" class="a11y-btn a11y-btn-plus" data-act="inc" aria-label="' + T('a11y.agrandir') + '">A+</button>'
        + '</span></div>'
        + '<div class="a11y-row"><span class="a11y-label">' + T('a11y.dys') + '</span>'
        + '<button type="button" id="a11y-dys" class="a11y-switch" role="switch" aria-checked="false" aria-label="' + T('a11y.dysActiver') + '"><span></span></button></div>'
        + '<div class="a11y-row a11y-hint">' + T('a11y.dysAide') + '</div>'
        + '<div class="a11y-row"><button type="button" class="a11y-reset" data-act="reset">' + T('a11y.reinitialiser') + '</button></div>';
      refresh();
    }
    remplir();
    document.addEventListener('tpl:langchange', remplir);

    function positionPanel() {
      var r = btn.getBoundingClientRect();
      panel.style.top = (r.bottom + 8) + 'px';
      // De droite à gauche, le bouton est du côté gauche de l'en-tête : aligné sur son bord droit, le panneau sortait de
      // l'écran. Il s'aligne alors sur son bord gauche, sans dépasser l'écran (264 px, la largeur que lui donne la feuille
      // de style ; caché, il n'en a pas encore).
      if (document.documentElement.dir === 'rtl') {
        var large = Math.min(264, window.innerWidth - 16);
        panel.style.right = 'auto';
        panel.style.left = Math.max(8, Math.min(r.left, window.innerWidth - large - 8)) + 'px';
      }
      else { panel.style.left = 'auto'; panel.style.right = Math.max(8, window.innerWidth - r.right) + 'px'; }
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
