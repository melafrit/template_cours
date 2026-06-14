/* =================================================================
   navigation.js — Arbre de navigation bilingue, thème, progression
   Template de site de cours — Mohamed EL AFRIT (MIT / CC BY 4.0)

   Générique : les données du cours viennent de window.COURSE (course-data.js),
   bilingue : les titres/libellés sont des objets { fr, en } ; l'arbre se
   ré-affiche sur l'évènement « tpl:langchange » (voir i18n.js).
   ================================================================= */
(function () {
  var COURSE = window.COURSE || { chapters: [], resources: [] };
  var path = window.location.pathname;
  var inChapters = /\/chapitres\//.test(path);
  var base = inChapters ? '../' : './';
  var currentFile = path.split('/').pop() || 'index.html';
  var totalCh = COURSE.chapters.length;

  function lang() { return window.TPLI18N ? TPLI18N.lang() : 'fr'; }
  // L(x) : x peut être une chaîne ou un objet { fr, en }
  function L(x) { return (x && typeof x === 'object') ? (x[lang()] || x.fr || x.en || '') : (x || ''); }
  function esc(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

  var UI = {
    fr: { chapters: 'Chapitres', resources: 'Ressources', home: 'Accueil du cours',
          reset: '↺ Réinitialiser ma progression', resetTitle: 'Effacer les chapitres marqués comme terminés',
          confirmReset: 'Réinitialiser votre progression (chapitres terminés) ?',
          secToggle: 'Afficher ou masquer les sections',
          doneMark: 'Marquer ce chapitre comme terminé', doneUnmark: '✓ Chapitre terminé — cliquez pour annuler' },
    en: { chapters: 'Chapters', resources: 'Resources', home: 'Course home',
          reset: '↺ Reset my progress', resetTitle: 'Clear chapters marked as done',
          confirmReset: 'Reset your progress (completed chapters)?',
          secToggle: 'Show or hide sections',
          doneMark: 'Mark this chapter as done', doneUnmark: '✓ Chapter done — click to undo' }
  };
  function t(k) { return (UI[lang()] || UI.fr)[k]; }

  // -- Suivi de progression (chapitres terminés, localStorage) --
  var DONE_KEY = 'tpl-done';
  function getDone() { try { return JSON.parse(localStorage.getItem(DONE_KEY)) || {}; } catch (e) { return {}; } }
  function setDone(m) { localStorage.setItem(DONE_KEY, JSON.stringify(m)); }
  function isDone(f) { return !!getDone()[f]; }
  function markDone(f, v) { var d = getDone(); if (v) d[f] = true; else delete d[f]; setDone(d); }

  var tree = document.getElementById('nav-tree');

  function renderTree() {
    if (!tree) return;
    var done = getDone();
    var doneCount = COURSE.chapters.filter(function (c) { return done[c.file]; }).length;
    var html = '<li class="nav-section-label">' + t('chapters') + ' <span class="nav-progress" id="nav-progress">' + doneCount + '/' + totalCh + '</span></li>';
    html += '<li class="nav-progressbar"><span id="nav-progressbar-fill" style="width:' + Math.round(doneCount / Math.max(1, totalCh) * 100) + '%"></span></li>';
    COURSE.chapters.forEach(function (ch) {
      var active = ch.file === currentFile ? ' active' : '';
      var d = done[ch.file] ? ' done' : '';
      var secs = (window.RDC_SECTIONS && window.RDC_SECTIONS[ch.num]) || [];
      var isCur = ch.file === currentFile;
      html += '<li class="nav-item' + (secs.length ? ' has-sub' : '') + (isCur && secs.length ? ' open' : '') + '">';
      html += '<div class="nav-row"><a class="nav-link' + active + d + '" data-file="' + ch.file + '" href="' + base + 'chapitres/' + ch.file + '"><span class="nav-num">' + (done[ch.file] ? '✓' : ch.num) + '</span><span class="nav-label">' + esc(L(ch.title)) + '</span></a>';
      if (secs.length) html += '<button type="button" class="nav-toggle" aria-label="' + t('secToggle') + '" aria-expanded="' + (isCur ? 'true' : 'false') + '">▸</button>';
      html += '</div>';
      if (secs.length) {
        html += '<ul class="nav-sub">';
        secs.forEach(function (s) { html += '<li><a class="nav-sublink" href="' + base + 'chapitres/' + ch.file + '#' + s.id + '">' + esc(L(s.t)) + '</a></li>'; });
        html += '</ul>';
      }
      html += '</li>';
    });
    html += '<li class="nav-section-label">' + t('resources') + '</li>';
    (COURSE.resources || []).forEach(function (r) {
      html += '<li class="nav-item"><a class="nav-link" href="' + base + r.href + '"><span class="nav-ico">' + (r.ico || '') + '</span><span class="nav-label">' + esc(L(r.label)) + '</span></a></li>';
    });
    html += '<li class="nav-section-label">&nbsp;</li>';
    html += '<li class="nav-item"><a class="nav-link" href="' + base + 'index.html"><span class="nav-ico">🏠</span><span class="nav-label">' + t('home') + '</span></a></li>';
    html += '<li class="nav-reset"><button type="button" id="nav-reset-btn" title="' + t('resetTitle') + '">' + t('reset') + '</button></li>';
    tree.innerHTML = html;
    tree.querySelectorAll('.nav-toggle').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault(); e.stopPropagation();
        var li = btn.closest('.nav-item');
        btn.setAttribute('aria-expanded', li.classList.toggle('open') ? 'true' : 'false');
      });
    });
    var resetBtn = document.getElementById('nav-reset-btn');
    if (resetBtn) resetBtn.addEventListener('click', function () { if (confirm(t('confirmReset'))) { setDone({}); location.reload(); } });
  }

  // Défilement fiable vers la section ciblée par une ancre (#chN-sM)
  if (location.hash) {
    window.addEventListener('load', function () {
      setTimeout(function () {
        var el; try { el = document.getElementById(decodeURIComponent(location.hash.slice(1))); } catch (e) { return; }
        if (el) window.scrollTo(0, Math.max(0, el.getBoundingClientRect().top + window.scrollY - 80));
      }, 60);
    });
  }

  function refreshNavProgress() {
    var done = getDone();
    var doneCount = COURSE.chapters.filter(function (c) { return done[c.file]; }).length;
    var np = document.getElementById('nav-progress'); if (np) np.textContent = doneCount + '/' + totalCh;
    var fill = document.getElementById('nav-progressbar-fill'); if (fill) fill.style.width = Math.round(doneCount / Math.max(1, totalCh) * 100) + '%';
    document.querySelectorAll('.nav-link[data-file]').forEach(function (a) {
      var f = a.getAttribute('data-file'); var num = a.querySelector('.nav-num');
      if (done[f]) { a.classList.add('done'); if (num) num.textContent = '✓'; }
      else { a.classList.remove('done'); var ch = COURSE.chapters.find(function (c) { return c.file === f; }); if (num && ch) num.textContent = ch.num; }
    });
  }

  // -- Thème clair/sombre --
  var THEME_KEY = 'tpl-theme';
  var root = document.documentElement;
  var savedTheme = localStorage.getItem(THEME_KEY);
  if (savedTheme) root.setAttribute('data-theme', savedTheme);
  else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) root.setAttribute('data-theme', 'dark');
  function syncThemeIcon() {
    var dark = root.getAttribute('data-theme') === 'dark';
    document.querySelectorAll('.theme-toggle').forEach(function (b) { b.textContent = dark ? '☀️' : '🌙'; });
  }
  syncThemeIcon();
  document.querySelectorAll('.theme-toggle').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var dark = root.getAttribute('data-theme') === 'dark';
      root.setAttribute('data-theme', dark ? 'light' : 'dark');
      localStorage.setItem(THEME_KEY, dark ? 'light' : 'dark');
      syncThemeIcon();
    });
  });

  // -- Sidebar mobile --
  var sidebar = document.querySelector('.sidebar');
  var stoggle = document.querySelector('.sidebar-toggle');
  if (stoggle && sidebar) {
    var overlay = document.querySelector('.sidebar-overlay');
    if (!overlay) { overlay = document.createElement('div'); overlay.className = 'sidebar-overlay'; document.body.appendChild(overlay); }
    var close = function () { sidebar.classList.remove('open'); overlay.classList.remove('show'); };
    stoggle.addEventListener('click', function () { sidebar.classList.toggle('open'); overlay.classList.toggle('show'); });
    overlay.addEventListener('click', close);
    sidebar.addEventListener('click', function (e) { if (e.target.closest('a') && window.innerWidth <= 768) close(); });
  }

  // -- Barre de progression de lecture --
  var bar = document.querySelector('.sidebar-progress-bar');
  var main = document.querySelector('.main-content');
  if (bar && main) {
    var update = function () {
      var total = main.scrollHeight - window.innerHeight;
      var pct = total > 0 ? Math.min(100, Math.max(0, (window.scrollY - main.offsetTop) / total * 100)) : 0;
      bar.style.width = pct + '%';
    };
    window.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    update();
  }

  // -- Complétion de chapitre (pages de chapitre seulement) --
  var doneWrap = null;
  function renderChapterDone() {
    if (!(inChapters && /^\d{1,2}-/.test(currentFile))) return;
    var pag = document.querySelector('.chapter-pagination');
    if (!pag) return;
    if (!doneWrap) { doneWrap = document.createElement('div'); doneWrap.className = 'chapter-done'; pag.parentNode.insertBefore(doneWrap, pag); }
    var d = isDone(currentFile);
    doneWrap.innerHTML = '<button type="button" class="btn ' + (d ? 'btn-primary' : 'btn-ghost') + '" id="ch-done-btn">' + (d ? t('doneUnmark') : t('doneMark')) + '</button>';
    doneWrap.querySelector('#ch-done-btn').addEventListener('click', function () { markDone(currentFile, !isDone(currentFile)); renderChapterDone(); refreshNavProgress(); });
    if ('IntersectionObserver' in window && !renderChapterDone._io) {
      renderChapterDone._io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) { if (e.isIntersecting && !isDone(currentFile)) { markDone(currentFile, true); renderChapterDone(); refreshNavProgress(); renderChapterDone._io.disconnect(); } });
      }, { threshold: 0.4 });
      renderChapterDone._io.observe(pag);
    }
  }

  // -- Rendu initial + ré-affichage au changement de langue --
  renderTree();
  renderChapterDone();
  document.addEventListener('tpl:langchange', function () { renderTree(); renderChapterDone(); });
})();
