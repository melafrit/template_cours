/* =================================================================
   media.js — Chargement automatique des médias NotebookLM par chapitre
   Template de site de cours — Mohamed EL AFRIT (MIT / CC BY 4.0)

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
  // La racine du site vient d'i18n.js : une page anglaise jumelle (en/chapitres/) est un cran plus bas.
  var base = (window.TPL_RACINE || '../') + 'assets/media/';
  /* Les libellés viennent de ui-labels.js, dans la langue de la page (repli français sans dictionnaire). Écrits en dur,
     ils restaient en français pour un lecteur anglophone. Ce qui ne se reconstruit pas à la bascule de langue — les
     diapositives, l'infographie, leurs fenêtres, le lecteur persistant — repose ses libellés sur « tpl:langchange ». */
  function t(cle, defaut) { return window.T ? T(cle) : defaut; }
  function duChapitre() { return ' — ' + t('media.chapitre', 'chapitre') + ' ' + N; }

  // --- Podcast : lecteur personnalisé (±10 s + progression) + mini-lecteur flottant + pop-out ---
    var pod = document.querySelector('.podcast-section');
    if (pod) {
      /* Le podcast existe par langue : chapitre-<N>-podcast.<langue>.mp3, avec
         repli sur le nom sans suffixe pour un cours monolingue. Sans cela, un
         lecteur passe en anglais continuerait d'entendre le francais. */
      var audioPod = null;

      function languePod() {
        return (window.TPLI18N && TPLI18N.lang && TPLI18N.lang()) || 'fr';
      }

      function chargerPodcast() {
        if (audioPod) {
          try { audioPod.pause(); } catch (e) {}
          if (audioPod.parentNode) audioPod.parentNode.removeChild(audioPod);
        }
        /* On VIDE la barre du lecteur, on ne la SUPPRIME pas :
           buildPodcastPlayer y insere ses controles et ne fait rien si
           l'element a disparu. Le lecteur restait alors invisible, sans
           erreur — l'audio etait charge, mais rien ne s'affichait. */
        var barre = pod.querySelector('.podcast-player');
        if (barre) barre.innerHTML = '';

        audioPod = document.createElement('audio');
        audioPod.preload = 'auto';
        var lg = languePod();
        var noms = ['-podcast.' + lg + '.mp3', '-podcast.mp3',
                    '-podcast.' + lg + '.m4a', '-podcast.m4a'];
        noms.forEach(function (suffixe) {
          var s = document.createElement('source');
          s.src = base + 'podcasts/chapitre-' + N + suffixe;
          s.type = suffixe.indexOf('.m4a') > -1 ? 'audio/mp4' : 'audio/mpeg';
          audioPod.appendChild(s);
        });
        audioPod.addEventListener('loadedmetadata', function onMeta() {
          audioPod.removeEventListener('loadedmetadata', onMeta);
          var ph = pod.querySelector('.podcast-placeholder-msg');
          if (ph) ph.remove();
          var tEl = pod.querySelector('.podcast-title');
          buildPodcastPlayer(pod, audioPod,
            tEl ? tEl.textContent : t('media.podcast', 'Podcast') + duChapitre());
        });
        pod.appendChild(audioPod);
        audioPod.load();
      }

      chargerPodcast();
      document.addEventListener('tpl:langchange', chargerPodcast);
    }

  // --- Slides : PDF (généré par NotebookLM) + agrandissement en popup plein écran ---
  var sl = document.querySelector('.slides-section');
  if (sl) {
    var pdfUrl = base + 'slides/chapitre-' + N + '-slides.pdf';
    var vp = sl.querySelector('.slides-viewport');
    var ctrls = sl.querySelector('.slides-controls');
    var openModal = buildSlidesModal(pdfUrl, N);

    var enableSlides = function () {
      var ifr = null, hint = null, layer = null, bEnl = null, aOpen = null;
      if (vp) {
        vp.innerHTML = '';
        ifr = document.createElement('iframe');
        ifr.className = 'slides-pdf';
        ifr.src = pdfUrl + '#view=FitH';
        vp.appendChild(ifr);
        // indice + couche de clic : cliquer le conteneur ouvre la popup
        hint = document.createElement('div');
        hint.className = 'slides-zoom-hint';
        layer = document.createElement('button');
        layer.type = 'button';
        layer.className = 'slides-click-layer';
        layer.addEventListener('click', openModal);
        vp.appendChild(hint);
        vp.appendChild(layer);
      }
      if (ctrls) {
        ctrls.innerHTML = '';
        bEnl = document.createElement('button');
        bEnl.type = 'button'; bEnl.className = 'chapter-nav-btn';
        bEnl.addEventListener('click', openModal);
        aOpen = document.createElement('a');
        aOpen.className = 'chapter-nav-btn'; aOpen.href = pdfUrl; aOpen.target = '_blank'; aOpen.rel = 'noopener';
        ctrls.appendChild(bEnl); ctrls.appendChild(aOpen);
      }
      function libeller() {
        if (ifr) ifr.title = t('media.slides', 'Slides') + duChapitre();
        if (hint) hint.textContent = t('media.agrandir', '⤢ Agrandir');
        if (layer) layer.setAttribute('aria-label', t('media.slidesPleinEcran', 'Agrandir les slides en plein écran'));
        if (bEnl) bEnl.textContent = t('media.agrandir', '⤢ Agrandir');
        if (aOpen) aOpen.textContent = t('media.ouvrir', 'Ouvrir ↗');
      }
      libeller();
      document.addEventListener('tpl:langchange', libeller);
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
    img.style.display = 'none';            // masquée tant que le chargement n'est pas confirmé
    var hintInfo = null;
    var libellerInfo = function () {
      img.alt = t('media.infographie', 'Infographie de synthèse') + duChapitre();
      if (hintInfo) hintInfo.textContent = t('media.agrandir', '⤢ Agrandir');
    };
    libellerInfo();
    document.addEventListener('tpl:langchange', libellerInfo);
    img.onload = function () {
      img.style.display = '';
      infoVp.innerHTML = ''; infoVp.appendChild(img);
      hintInfo = document.createElement('div');
      hintInfo.className = 'infographie-zoom-hint';
      infoVp.appendChild(hintInfo);
      libellerInfo();
    };
    img.onerror = function () { if (img.parentNode) img.parentNode.removeChild(img); }; // garde le placeholder
    img.addEventListener('click', function () { openImg(infoUrl, img.alt); });
    infoVp.appendChild(img);               // DANS le DOM -> se charge réellement (pas de lazy détaché)
    img.src = infoUrl;
  }

  // --- Fiche de synthèse du chapitre : bouton dans la barre de navigation (entre Précédent et Suivant) + popup
  //     plein écran. « Polycopié » désigne le livret complet (polycopie.html) ---
  (function () {
    var nav = document.querySelector('.chapter-nav');
    if (!nav) return;
    /* Les fiches de synthèse par chapitre n'existent que si le menu les annonce
       (bloc « polycopies » de cours.json) : sans elles, la sonde HEAD ne faisait
       qu'ajouter un 404 par chapitre dans la console. */
    var avecFiches = window.COURSE && (window.COURSE.resources || []).some(function (r) {
      return r.href === 'polycopies.html';
    });
    if (!avecFiches) return;
      /* Le polycopie existe par langue : « chapitre-2-polycopie.fr.pdf ». Sans
         le suffixe, le fichier n'etait jamais trouve et le bouton n'apparaissait
         pas — un defaut silencieux, puisqu'un bouton absent ne se remarque pas. */
      function langue() {
        return (window.TPLI18N && TPLI18N.lang && TPLI18N.lang()) || 'fr';
      }
      function chemin() {
        return (window.TPL_RACINE || '../') + 'assets/polycopies/chapitre-' + N + '-polycopie.' + langue() + '.pdf';
      }

      function poser() {
        var ancien = nav.querySelector('.poly-btn');
        if (ancien) ancien.parentNode.removeChild(ancien);
        // la fenêtre se refait dans la langue de la page : l'ancienne s'en va, sans quoi elles s'empileraient
        var vieille = document.querySelector('.poly-modal');
        if (vieille) vieille.parentNode.removeChild(vieille);
        var openModal = buildPolyModal(chemin(), N);
        var btn = document.createElement('button');
        btn.type = 'button'; btn.className = 'chapter-nav-btn poly-btn';
        btn.innerHTML = window.T ? T('media.polycopie') : '📄 Fiche de synthèse';
        btn.addEventListener('click', openModal);
        var links = nav.querySelectorAll('a, button');
        var last = links[links.length - 1];
        if (last && last.parentNode === nav) nav.insertBefore(btn, last); else nav.appendChild(btn);
      }

      function tenter() {
        if (location.protocol === 'http:' || location.protocol === 'https:') {
          fetch(chemin(), { method: 'HEAD' })
            .then(function (r) {
              var b = nav.querySelector('.poly-btn');
              if (r.ok) poser();
              else if (b) b.parentNode.removeChild(b);
            })
            .catch(function () {});
        } else { poser(); }
      }

      tenter();
      document.addEventListener('tpl:langchange', tenter);
    })();

  // --- Popup plein écran pour les slides (créée une fois, réutilisée) ---
  function buildSlidesModal(pdfUrl, N) {
    var modal = document.createElement('div');
    modal.className = 'slides-modal';
    modal.hidden = true;
    modal.innerHTML =
        '<button type="button" class="slides-modal-close">✕</button>'
      + '<div class="slides-modal-bar">'
      + '<span class="slides-modal-title"></span>'
      + '<a class="slides-modal-open" href="' + pdfUrl + '" target="_blank" rel="noopener"></a>'
      + '</div>'
      + '<iframe class="slides-modal-frame"></iframe>';
    document.body.appendChild(modal);
    var frame = modal.querySelector('.slides-modal-frame');
    var btnClose = modal.querySelector('.slides-modal-close');
    function libeller() {
      btnClose.setAttribute('aria-label', t('media.fermer', 'Fermer'));
      modal.querySelector('.slides-modal-title').textContent = '📊 ' + t('media.slides', 'Slides') + duChapitre();
      modal.querySelector('.slides-modal-open').textContent = t('media.ouvrirOnglet', 'Ouvrir dans un onglet ↗');
      frame.title = t('media.slidesPleinEcranTitre', 'Slides plein écran') + duChapitre();
    }
    libeller();
    document.addEventListener('tpl:langchange', libeller);
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
        '<button type="button" class="img-modal-close">✕</button>'
      + '<div class="img-modal-body"><img class="img-modal-img" alt=""></div>';
    document.body.appendChild(modal);
    var imgEl = modal.querySelector('.img-modal-img');
    var body = modal.querySelector('.img-modal-body');
    var btnClose = modal.querySelector('.img-modal-close');
    function libeller() { btnClose.setAttribute('aria-label', t('media.fermer', 'Fermer')); }
    libeller();
    document.addEventListener('tpl:langchange', libeller);
    function close() { modal.hidden = true; imgEl.src = ''; imgEl.classList.remove('zoomed'); document.body.style.overflow = ''; }
    function open(src, alt) { imgEl.src = src; imgEl.alt = alt || ''; imgEl.classList.remove('zoomed'); modal.hidden = false; document.body.style.overflow = 'hidden'; btnClose.focus(); }
    btnClose.addEventListener('click', close);
    modal.addEventListener('click', function (e) { if (e.target === modal || e.target === body) close(); }); // clic sur le fond
    imgEl.addEventListener('click', function (e) { e.stopPropagation(); imgEl.classList.toggle('zoomed'); }); // clic image = zoom
    document.addEventListener('keydown', function (e) { if (!modal.hidden && (e.key === 'Escape' || e.key === 'Esc')) close(); });
    return open;
  }

  /* ===== Popup de la fiche de synthèse (aperçu PDF + téléchargement PDF) ===== */
  function buildPolyModal(pdfUrl, N) {
    // Refaite à chaque changement de langue (voir poser()) : elle lit ses libellés à sa construction.
    var chapitre = ' — ' + t('media.chapitre', 'chapitre') + ' ' + N;
    var modal = document.createElement('div');
    modal.className = 'slides-modal poly-modal'; modal.hidden = true;
    modal.innerHTML =
        '<button type="button" class="slides-modal-close" aria-label="' + t('media.fermer', 'Fermer') + '">✕</button>'
      + '<div class="slides-modal-bar"><span class="slides-modal-title">'
      + t('media.polycopie', '📄 Fiche de synthèse') + chapitre + '</span>'
      + '<span class="poly-dl">'
      + '<a class="slides-modal-open" href="' + pdfUrl + '" download>⬇ PDF</a>'
      + '<a class="slides-modal-open" href="' + pdfUrl + '" target="_blank" rel="noopener">'
      + t('media.ouvrir', 'Ouvrir ↗') + '</a>'
      + '</span></div>'
      + '<iframe class="slides-modal-frame" title="' + t('media.fiche', 'Fiche de synthèse') + chapitre + '"></iframe>';
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
      + '<button type="button" class="pp-btn pp-play">▶</button>'
      + '<button type="button" class="pp-btn pp-back">⏪<span class="pp-sec">10</span></button>'
      + '<button type="button" class="pp-btn pp-fwd"><span class="pp-sec">10</span>⏩</button>'
      + '<div class="pp-progress"><div class="pp-progress-fill"></div></div>'
      + '<span class="pp-time">0:00 / 0:00</span>'
      + '<button type="button" class="pp-btn pp-dl">⬇</button>'
      + (withPop ? '<button type="button" class="pp-btn pp-pop">⧉</button>' : '')
      + '</div>';
  }

  /* Les libellés d'une barre de contrôle, posés après sa construction : la barre du podcast se refait à chaque
     changement de langue, celle du lecteur persistant non — il les repose lui-même (LECTEUR). */
  function libellerBarre(bar) {
    if (!bar) return;
    function poser(sel, aria, titre) {
      var b = bar.querySelector(sel);
      if (!b) return;
      b.setAttribute('aria-label', aria);
      if (titre) b.title = titre;
    }
    poser('.pp-play', t('media.lecturePause', 'Lecture / Pause'));
    poser('.pp-back', t('media.reculer', 'Reculer de 10 secondes'));
    poser('.pp-fwd', t('media.avancer', 'Avancer de 10 secondes'));
    poser('.pp-dl', t('media.telecharger', "Télécharger l'épisode"), t('media.telechargerTitre', "Télécharger l'épisode (MP3)"));
    poser('.pp-pop', t('media.fenetre', 'Ouvrir dans une fenêtre indépendante'),
          t('media.fenetre', 'Ouvrir dans une fenêtre indépendante'));
  }

  /* Câble une barre de contrôle (.podcast-controls) sur un élément <audio>. */
  function brancherBarre(bar, get, onPopout) {
    if (!bar) return;
    bar.querySelector('.pp-play').addEventListener('click', function () {
      var a = get(); if (!a) return;
      if (a.paused) { var p = a.play(); if (p && p.catch) p.catch(function () {}); } else a.pause();
    });
    bar.querySelector('.pp-back').addEventListener('click', function () { var a = get(); if (a) a.currentTime = Math.max(0, a.currentTime - 10); });
    bar.querySelector('.pp-fwd').addEventListener('click', function () { var a = get(); if (a) a.currentTime = Math.min(a.duration || 1e9, a.currentTime + 10); });
    var prog = bar.querySelector('.pp-progress');
    prog.addEventListener('click', function (e) {
      var a = get(); if (!a) return;
      var r = prog.getBoundingClientRect();
      a.currentTime = Math.max(0, Math.min(1, (e.clientX - r.left) / r.width)) * (a.duration || 0);
    });
    var pop = bar.querySelector('.pp-pop'); if (pop && onPopout) pop.addEventListener('click', onPopout);
    var dl = bar.querySelector('.pp-dl');
    if (dl) dl.addEventListener('click', function () {
      var a = get(); var src = a && a.currentSrc; if (!src) return;
      var lien = document.createElement('a');
      lien.href = src; lien.download = (src.split('/').pop() || 'audio.mp3').split('?')[0];
      document.body.appendChild(lien); lien.click(); document.body.removeChild(lien);
    });
  }

  function peindreBarre(bar, a) {
    if (!bar || !a) return;
    var pct = a.duration ? (a.currentTime / a.duration * 100) : 0;
    bar.querySelector('.pp-play').textContent = a.paused ? '▶' : '⏸';
    bar.querySelector('.pp-progress-fill').style.width = pct + '%';
    bar.querySelector('.pp-time').textContent = fmtTime(a.currentTime) + ' / ' + fmtTime(a.duration || 0);
  }

  /* ------------------------------------------------------------------
     Lecteur persistant — un seul pour toute la page.
     Le podcast et les capsules de voix s'y branchent : dès qu'un audio
     démarre, la barre apparaît et suit la lecture pendant qu'on fait
     défiler la page. Un seul son à la fois : démarrer une capsule met le
     podcast en pause, et réciproquement.
     Sur écran large c'est un panneau flottant que l'on déplace ; sous
     768 px il se dock en bas de la fenêtre sur toute la largeur, sans
     recouvrir la page (le corps reçoit une marge basse de sa hauteur).
     ------------------------------------------------------------------ */
  var LECTEUR = (function () {
    var el = null, bar = null, titreEl = null, courant = null;
    var attaches = [];

    function mobile() { return window.matchMedia('(max-width: 768px)').matches; }

    function creer() {
      el = document.createElement('div');
      el.className = 'mini-player';
      el.hidden = true;
      el.innerHTML =
          '<div class="mini-player-head">'
        + '<span class="mini-grip" aria-hidden="true">⠿</span>'
        + '<span class="mini-title"></span>'
        + '<button type="button" class="pp-btn mini-pop">⧉</button>'
        + '<button type="button" class="pp-btn mini-close">✕</button>'
        + '</div>'
        + controlBarHtml(false);
      document.body.appendChild(el);
      bar = el.querySelector('.podcast-controls');
      titreEl = el.querySelector('.mini-title');
      libeller();
      document.addEventListener('tpl:langchange', libeller);

      brancherBarre(bar, function () { return courant; });
      el.querySelector('.mini-pop').addEventListener('click', function () {
        if (!courant) return;
        openPopout(courant.currentSrc, courant.currentTime, titreEl.textContent);
        courant.pause(); cacher();
      });
      /* Fermer arrête le son : laisser une lecture invisible se poursuivre
         serait le pire des deux mondes. */
      el.querySelector('.mini-close').addEventListener('click', function () {
        if (courant) courant.pause();
        cacher();
      });
      makeDraggable(el, el.querySelector('.mini-player-head'), mobile);
      window.addEventListener('resize', majMarge);
    }

    // Le lecteur persistant ne se reconstruit pas : ses libellés se reposent à chaque changement de langue.
    function libeller() {
      if (!el) return;
      var pop = el.querySelector('.mini-pop'), fermer = el.querySelector('.mini-close');
      pop.title = t('media.fenetreCourt', 'Fenêtre indépendante');
      pop.setAttribute('aria-label', t('media.fenetre', 'Ouvrir dans une fenêtre indépendante'));
      fermer.title = t('media.fermerLecteur', 'Fermer le lecteur');
      fermer.setAttribute('aria-label', t('media.fermerLecteur', 'Fermer le lecteur'));
      libellerBarre(bar);
    }

    /* Docké en bas sur mobile, il masquerait la fin de la page : on rend au
       corps exactement la hauteur qu'il occupe. */
    function majMarge() {
      if (!el) return;
      if (el.hidden || !mobile()) {
        document.body.classList.remove('a-lecteur');
        document.documentElement.style.removeProperty('--rdc-lecteur-h');
        return;
      }
      document.documentElement.style.setProperty('--rdc-lecteur-h', el.offsetHeight + 'px');
      document.body.classList.add('a-lecteur');
    }

    function cacher() {
      if (!el) return;
      el.hidden = true;
      majMarge();
    }

    function montrer(a, titre) {
      if (!el) creer();
      courant = a;
      titreEl.textContent = titre || 'Audio';
      /* Le glissement a pu laisser des styles en ligne : sur mobile la barre
         doit revenir au bas de l'écran. */
      if (mobile()) { el.style.left = ''; el.style.top = ''; el.style.right = ''; el.style.bottom = ''; }
      el.hidden = false;
      peindreBarre(bar, a);
      majMarge();
    }

    function attacher(a, titre) {
      if (!a || attaches.indexOf(a) > -1) return;
      attaches.push(a);
      a.addEventListener('play', function () {
        for (var i = 0; i < attaches.length; i++) {
          if (attaches[i] !== a && !attaches[i].paused) attaches[i].pause();
        }
        montrer(a, typeof titre === 'function' ? titre() : titre);
      });
      ['timeupdate', 'play', 'pause', 'loadedmetadata', 'seeked', 'ended'].forEach(function (ev) {
        a.addEventListener(ev, function () { if (courant === a) peindreBarre(bar, a); });
      });
    }

    return { attacher: attacher, cacher: cacher };
  })();
  window.RDC_LECTEUR = LECTEUR;

  function buildPodcastPlayer(pod, audio, title) {
    var player = pod.querySelector('.podcast-player');
    if (player) {
      player.innerHTML = controlBarHtml(true);
      var bar = player.querySelector('.podcast-controls');
      libellerBarre(bar);
      brancherBarre(bar, function () { return audio; }, function () {
        openPopout(audio.currentSrc, audio.currentTime, title);
        audio.pause(); LECTEUR.cacher();
      });
      ['timeupdate', 'play', 'pause', 'loadedmetadata', 'seeked'].forEach(function (ev) {
        audio.addEventListener(ev, function () { peindreBarre(bar, audio); });
      });
      peindreBarre(bar, audio);
    }
    LECTEUR.attacher(audio, '🎙️ ' + title);
  }

  function openPopout(src, t, title) {
    if (!src) return;
    var url = (window.TPL_RACINE || '../') + 'assets/player.html?src=' + encodeURIComponent(src) + '&t=' + Math.floor(t || 0) + '&title=' + encodeURIComponent(title || 'Podcast');
    window.open(url, 'rdc_podcast_player', 'width=430,height=210,menubar=no,toolbar=no,location=no,status=no,resizable=yes,scrollbars=no');
  }

  function makeDraggable(el, handle, bloque) {
    var sx = 0, sy = 0, ox = 0, oy = 0, on = false;
    function pt(e) { return e.touches && e.touches[0] ? e.touches[0] : e; }
    function down(e) {
      // Docké en bas de l'écran, le lecteur mobile ne se déplace pas : le glissement
      // entrerait en concurrence avec le défilement du doigt.
      if (bloque && bloque()) return;
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
