/* =================================================================
   media.js — Chargement automatique des médias NotebookLM par chapitre
   Cours "Réglementation des données et conformité" — M. EL AFRIT (CC BY-NC-SA 4.0)

   Déposez vos fichiers dans assets/media/{infographies,slides,podcasts}/
   nommés  chapitre-<N>-<type>.<ext>  (ex. chapitre-3-podcast.mp3) :
   ils s'affichent automatiquement sur la page du chapitre correspondant.
   Si un fichier est absent, l'espace réservé est conservé (aucune erreur visible).
   ================================================================= */
(function () {
  var file = (location.pathname.split('/').pop() || '');
  var m = file.match(/^(\d{1,2})-/);          // 01-introduction.html -> 1 ; 06-atelier-... -> 6
  if (!m) return;
  var N = parseInt(m[1], 10);
  var base = '../assets/media/';

  // --- Podcast : lecteur personnalisé (±10 s + progression) + mini-lecteur flottant + pop-out ---
  var pod = document.querySelector('.podcast-section');
  if (pod) {
    var audio = document.createElement('audio');
    audio.preload = 'auto'; // 'auto' (et non 'metadata') : télécharge tout le fichier -> audio entièrement « seekable » même sans support des requêtes HTTP Range (ouverture locale, Safari) -> les boutons ±10 s fonctionnent partout
    [['mp3', 'audio/mpeg'], ['m4a', 'audio/mp4']].forEach(function (f) {
      var s = document.createElement('source');
      s.src = base + 'podcasts/chapitre-' + N + '-podcast.' + f[0];
      s.type = f[1];
      audio.appendChild(s);
    });
    audio.addEventListener('loadedmetadata', function onMeta() {
      audio.removeEventListener('loadedmetadata', onMeta);
      var ph = pod.querySelector('.podcast-placeholder-msg'); if (ph) ph.remove();
      var tEl = pod.querySelector('.podcast-title');
      buildPodcastPlayer(pod, audio, tEl ? tEl.textContent : 'Podcast — chapitre ' + N);
    });
    pod.appendChild(audio);
    audio.load();
  }

  // --- Slides : PDF (généré par NotebookLM) + agrandissement en popup plein écran ---
  var sl = document.querySelector('.slides-section');
  if (sl) {
    var pdfUrl = base + 'slides/chapitre-' + N + '-slides.pdf';
    var vp = sl.querySelector('.slides-viewport');
    var ctrls = sl.querySelector('.slides-controls');
    var openModal = buildSlidesModal(pdfUrl, N);

    var enableSlides = function () {
      if (vp) {
        vp.innerHTML = '';
        var ifr = document.createElement('iframe');
        ifr.className = 'slides-pdf';
        ifr.src = pdfUrl + '#view=FitH';
        ifr.title = 'Slides — chapitre ' + N;
        vp.appendChild(ifr);
        // indice + couche de clic : cliquer le conteneur ouvre la popup
        var hint = document.createElement('div');
        hint.className = 'slides-zoom-hint';
        hint.textContent = '⤢ Agrandir';
        var layer = document.createElement('button');
        layer.type = 'button';
        layer.className = 'slides-click-layer';
        layer.setAttribute('aria-label', 'Agrandir les slides en plein écran');
        layer.addEventListener('click', openModal);
        vp.appendChild(hint);
        vp.appendChild(layer);
      }
      if (ctrls) {
        ctrls.innerHTML = '';
        var bEnl = document.createElement('button');
        bEnl.type = 'button'; bEnl.className = 'chapter-nav-btn'; bEnl.textContent = '⤢ Agrandir';
        bEnl.addEventListener('click', openModal);
        var aOpen = document.createElement('a');
        aOpen.className = 'chapter-nav-btn'; aOpen.href = pdfUrl; aOpen.target = '_blank'; aOpen.rel = 'noopener'; aOpen.textContent = 'Ouvrir ↗';
        ctrls.appendChild(bEnl); ctrls.appendChild(aOpen);
      }
    };

    if (location.protocol === 'http:' || location.protocol === 'https:') {
      // site hébergé : on vérifie l'existence du PDF avant de l'afficher
      fetch(pdfUrl, { method: 'HEAD' }).then(function (r) { if (r.ok) enableSlides(); }).catch(function () {});
    } else {
      // ouverture locale (file://) : impossible de vérifier, on active l'aperçu et la popup
      enableSlides();
    }
  }

  // --- Infographie : remplit la section dédiée si le PNG existe (clic -> popup plein écran) ---
  var infoVp = document.querySelector('.infographie-section .infographie-viewport');
  if (infoVp) {
    var infoUrl = base + 'infographies/chapitre-' + N + '-infographie.png';
    var openImg = buildImageModal();
    var img = document.createElement('img');
    img.className = 'infographie-img';
    img.alt = 'Infographie de synthèse — chapitre ' + N;
    img.style.display = 'none';            // masquée tant que le chargement n'est pas confirmé
    img.onload = function () {
      img.style.display = '';
      infoVp.innerHTML = ''; infoVp.appendChild(img);
      var hint = document.createElement('div');
      hint.className = 'infographie-zoom-hint';
      hint.textContent = '⤢ Agrandir';
      infoVp.appendChild(hint);
    };
    img.onerror = function () { if (img.parentNode) img.parentNode.removeChild(img); }; // garde le placeholder
    img.addEventListener('click', function () { openImg(infoUrl, img.alt); });
    infoVp.appendChild(img);               // DANS le DOM -> se charge réellement (pas de lazy détaché)
    img.src = infoUrl;
  }

  // --- Polycopié : bouton dans la barre de navigation (entre Précédent et Suivant) + popup plein écran ---
  (function () {
    var nav = document.querySelector('.chapter-nav');
    if (!nav) return;
    var polyPdf = '../assets/polycopies/chapitre-' + N + '-polycopie.pdf';
    var polyDocx = '../assets/polycopies/chapitre-' + N + '-polycopie.docx';
    function enable() {
      var openModal = buildPolyModal(polyPdf, polyDocx, N);
      var btn = document.createElement('button');
      btn.type = 'button'; btn.className = 'chapter-nav-btn poly-btn';
      btn.innerHTML = '📄 Polycopié';
      btn.addEventListener('click', openModal);
      var links = nav.querySelectorAll('a, button');
      var last = links[links.length - 1]; // le bouton « Suivant »
      if (last && last.parentNode === nav) nav.insertBefore(btn, last); else nav.appendChild(btn);
    }
    if (location.protocol === 'http:' || location.protocol === 'https:') {
      fetch(polyPdf, { method: 'HEAD' }).then(function (r) { if (r.ok) enable(); }).catch(function () {});
    } else { enable(); }
  })();

  // --- Popup plein écran pour les slides (créée une fois, réutilisée) ---
  function buildSlidesModal(pdfUrl, N) {
    var modal = document.createElement('div');
    modal.className = 'slides-modal';
    modal.hidden = true;
    modal.innerHTML =
        '<button type="button" class="slides-modal-close" aria-label="Fermer">✕</button>'
      + '<div class="slides-modal-bar">'
      + '<span class="slides-modal-title">📊 Slides — chapitre ' + N + '</span>'
      + '<a class="slides-modal-open" href="' + pdfUrl + '" target="_blank" rel="noopener">Ouvrir dans un onglet ↗</a>'
      + '</div>'
      + '<iframe class="slides-modal-frame" title="Slides plein écran — chapitre ' + N + '"></iframe>';
    document.body.appendChild(modal);
    var frame = modal.querySelector('.slides-modal-frame');
    var btnClose = modal.querySelector('.slides-modal-close');
    function close() { modal.hidden = true; frame.src = 'about:blank'; document.body.style.overflow = ''; }
    function open(e) { if (e) e.preventDefault(); frame.src = pdfUrl + '#view=FitH'; modal.hidden = false; document.body.style.overflow = 'hidden'; btnClose.focus(); }
    btnClose.addEventListener('click', close);
    modal.addEventListener('click', function (e) { if (e.target === modal) close(); }); // clic sur le fond
    document.addEventListener('keydown', function (e) { if (!modal.hidden && (e.key === 'Escape' || e.key === 'Esc')) close(); });
    return open;
  }

  // --- Lightbox plein écran pour les infographies (image) ---
  function buildImageModal() {
    var modal = document.createElement('div');
    modal.className = 'img-modal';
    modal.hidden = true;
    modal.innerHTML =
        '<button type="button" class="img-modal-close" aria-label="Fermer">✕</button>'
      + '<div class="img-modal-body"><img class="img-modal-img" alt=""></div>';
    document.body.appendChild(modal);
    var imgEl = modal.querySelector('.img-modal-img');
    var body = modal.querySelector('.img-modal-body');
    var btnClose = modal.querySelector('.img-modal-close');
    function close() { modal.hidden = true; imgEl.src = ''; imgEl.classList.remove('zoomed'); document.body.style.overflow = ''; }
    function open(src, alt) { imgEl.src = src; imgEl.alt = alt || ''; imgEl.classList.remove('zoomed'); modal.hidden = false; document.body.style.overflow = 'hidden'; btnClose.focus(); }
    btnClose.addEventListener('click', close);
    modal.addEventListener('click', function (e) { if (e.target === modal || e.target === body) close(); }); // clic sur le fond
    imgEl.addEventListener('click', function (e) { e.stopPropagation(); imgEl.classList.toggle('zoomed'); }); // clic image = zoom
    document.addEventListener('keydown', function (e) { if (!modal.hidden && (e.key === 'Escape' || e.key === 'Esc')) close(); });
    return open;
  }

  /* ===== Popup polycopié (aperçu PDF + téléchargements PDF/DOCX) ===== */
  function buildPolyModal(pdfUrl, docxUrl, N) {
    var modal = document.createElement('div');
    modal.className = 'slides-modal poly-modal'; modal.hidden = true;
    modal.innerHTML =
        '<button type="button" class="slides-modal-close" aria-label="Fermer">✕</button>'
      + '<div class="slides-modal-bar"><span class="slides-modal-title">📄 Polycopié — chapitre ' + N + '</span>'
      + '<span class="poly-dl">'
      + '<a class="slides-modal-open" href="' + pdfUrl + '" download>⬇ PDF</a>'
      + '<a class="slides-modal-open" href="' + docxUrl + '" download>⬇ DOCX</a>'
      + '<a class="slides-modal-open" href="' + pdfUrl + '" target="_blank" rel="noopener">Ouvrir ↗</a>'
      + '</span></div>'
      + '<iframe class="slides-modal-frame" title="Polycopié — chapitre ' + N + '"></iframe>';
    document.body.appendChild(modal);
    var frame = modal.querySelector('.slides-modal-frame');
    var btnClose = modal.querySelector('.slides-modal-close');
    function close() { modal.hidden = true; frame.src = 'about:blank'; document.body.style.overflow = ''; }
    function open(e) { if (e) e.preventDefault(); frame.src = pdfUrl + '#view=FitH'; modal.hidden = false; document.body.style.overflow = 'hidden'; btnClose.focus(); }
    btnClose.addEventListener('click', close);
    modal.addEventListener('click', function (e) { if (e.target === modal) close(); });
    document.addEventListener('keydown', function (e) { if (!modal.hidden && (e.key === 'Escape' || e.key === 'Esc')) close(); });
    return open;
  }

  /* ===== Lecteur podcast : barre personnalisée + mini-lecteur flottant + pop-out ===== */
  function esc(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  function fmtTime(s) { s = Math.floor(s || 0); if (!isFinite(s) || s < 0) s = 0; var m = Math.floor(s / 60), ss = s % 60; return m + ':' + (ss < 10 ? '0' : '') + ss; }

  function controlBarHtml(withPop) {
    return '<div class="podcast-controls">'
      + '<button type="button" class="pp-btn pp-play" aria-label="Lecture / Pause">▶</button>'
      + '<button type="button" class="pp-btn pp-back" aria-label="Reculer de 10 secondes">⏪<span class="pp-sec">10</span></button>'
      + '<button type="button" class="pp-btn pp-fwd" aria-label="Avancer de 10 secondes"><span class="pp-sec">10</span>⏩</button>'
      + '<div class="pp-progress"><div class="pp-progress-fill"></div></div>'
      + '<span class="pp-time">0:00 / 0:00</span>'
      + '<button type="button" class="pp-btn pp-dl" title="Télécharger l\'épisode (MP3)" aria-label="Télécharger l\'épisode">⬇</button>'
      + (withPop ? '<button type="button" class="pp-btn pp-pop" title="Ouvrir dans une fenêtre indépendante" aria-label="Ouvrir dans une fenêtre indépendante">⧉</button>' : '')
      + '</div>';
  }

  function buildPodcastPlayer(pod, audio, title) {
    var player = pod.querySelector('.podcast-player');
    if (player) player.innerHTML = controlBarHtml(true);

    var mini = document.createElement('div'); mini.className = 'mini-player'; mini.hidden = true;
    mini.innerHTML = '<div class="mini-player-head"><span class="mini-grip">⠿</span><span class="mini-title">🎙️ ' + esc(title) + '</span>'
      + '<button type="button" class="pp-btn mini-pop" title="Fenêtre indépendante" aria-label="Fenêtre indépendante">⧉</button>'
      + '<button type="button" class="pp-btn mini-close" title="Fermer" aria-label="Fermer">✕</button></div>'
      + controlBarHtml(false);
    document.body.appendChild(mini);

    var bars = [];
    if (player) bars.push(player.querySelector('.podcast-controls'));
    bars.push(mini.querySelector('.podcast-controls'));

    function popout() { openPopout(audio.currentSrc, audio.currentTime, title); audio.pause(); mini.hidden = true; }

    bars.forEach(function (bar) {
      bar.querySelector('.pp-play').addEventListener('click', function () { audio.paused ? audio.play() : audio.pause(); });
      bar.querySelector('.pp-back').addEventListener('click', function () { audio.currentTime = Math.max(0, audio.currentTime - 10); });
      bar.querySelector('.pp-fwd').addEventListener('click', function () { audio.currentTime = Math.min(audio.duration || 1e9, audio.currentTime + 10); });
      var prog = bar.querySelector('.pp-progress');
      prog.addEventListener('click', function (e) { var r = prog.getBoundingClientRect(); audio.currentTime = Math.max(0, Math.min(1, (e.clientX - r.left) / r.width)) * (audio.duration || 0); });
      var pop = bar.querySelector('.pp-pop'); if (pop) pop.addEventListener('click', popout);
      var dl = bar.querySelector('.pp-dl'); if (dl) dl.addEventListener('click', function () { var src = audio.currentSrc; if (!src) return; var a = document.createElement('a'); a.href = src; a.download = (src.split('/').pop() || 'podcast.mp3').split('?')[0]; document.body.appendChild(a); a.click(); document.body.removeChild(a); });
    });
    mini.querySelector('.mini-pop').addEventListener('click', popout);
    mini.querySelector('.mini-close').addEventListener('click', function () { mini.hidden = true; });

    audio.addEventListener('play', function () { mini.hidden = false; });

    function sync() {
      var icon = audio.paused ? '▶' : '⏸';
      var pct = audio.duration ? (audio.currentTime / audio.duration * 100) : 0;
      var tx = fmtTime(audio.currentTime) + ' / ' + fmtTime(audio.duration || 0);
      bars.forEach(function (bar) {
        bar.querySelector('.pp-play').textContent = icon;
        bar.querySelector('.pp-progress-fill').style.width = pct + '%';
        bar.querySelector('.pp-time').textContent = tx;
      });
    }
    ['timeupdate', 'play', 'pause', 'loadedmetadata', 'seeked'].forEach(function (ev) { audio.addEventListener(ev, sync); });
    sync();

    makeDraggable(mini, mini.querySelector('.mini-player-head'));
  }

  function openPopout(src, t, title) {
    if (!src) return;
    var url = '../assets/player.html?src=' + encodeURIComponent(src) + '&t=' + Math.floor(t || 0) + '&title=' + encodeURIComponent(title || 'Podcast');
    window.open(url, 'rdc_podcast_player', 'width=430,height=210,menubar=no,toolbar=no,location=no,status=no,resizable=yes,scrollbars=no');
  }

  function makeDraggable(el, handle) {
    var sx = 0, sy = 0, ox = 0, oy = 0, on = false;
    function pt(e) { return e.touches && e.touches[0] ? e.touches[0] : e; }
    function down(e) {
      if (e.target.closest && e.target.closest('button')) return; // ne pas glisser en cliquant un bouton
      var p = pt(e); on = true; sx = p.clientX; sy = p.clientY;
      var r = el.getBoundingClientRect(); ox = r.left; oy = r.top;
      el.style.left = ox + 'px'; el.style.top = oy + 'px'; el.style.right = 'auto'; el.style.bottom = 'auto';
      document.addEventListener('mousemove', move); document.addEventListener('mouseup', up);
      document.addEventListener('touchmove', move, { passive: false }); document.addEventListener('touchend', up);
      if (e.cancelable) e.preventDefault();
    }
    function move(e) {
      if (!on) return; var p = pt(e);
      var nx = ox + (p.clientX - sx), ny = oy + (p.clientY - sy);
      nx = Math.max(0, Math.min(window.innerWidth - el.offsetWidth, nx));
      ny = Math.max(0, Math.min(window.innerHeight - el.offsetHeight, ny));
      el.style.left = nx + 'px'; el.style.top = ny + 'px'; if (e.cancelable) e.preventDefault();
    }
    function up() { on = false; document.removeEventListener('mousemove', move); document.removeEventListener('mouseup', up); document.removeEventListener('touchmove', move); document.removeEventListener('touchend', up); }
    handle.addEventListener('mousedown', down); handle.addEventListener('touchstart', down, { passive: false });
  }
})();
