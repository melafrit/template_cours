/* =================================================================
   interactions.js — Moteur d'interactions pédagogiques
   Template de site de cours — Mohamed EL AFRIT (MIT / CC BY 4.0)

   Espace de noms : window.RDCX
     RDCX.checkpoint('id', cfg)  // point de contrôle de fin de section
     RDCX.reveal('id', cfg)      // prédiction puis révélation (effet de génération)
     RDCX.spotError('id', cfg)   // repérage d'erreurs dans un document
     RDCX.match('id', cfg)       // appariement (article ↔ notion)
     RDCX.branch('id', cfg)      // cas à embranchements (apprentissage par l'erreur)
     RDCX.hotspots('id', cfg)    // schéma à zones cliquables
     RDCX.voice('id', cfg)       // capsule audio « voix du formateur »
     RDCX.progress(cfg)          // progression du chapitre (un seul appel par page)
     RDCX.steps(cfg)             // parcours par étapes (un seul appel par page)
     RDCX.sommaire(cfg)          // sommaire collant, rien n'est masqué (un seul appel par page)

   Chaque fabrique reçoit l'id d'un <div> vide et y injecte tout son HTML.
   Elle ne fait rien si le conteneur est absent. Feuille de style associée :
   assets/css/interactions.css (chargée après components.css).
   ================================================================= */
(function () {
  window.RDCX = window.RDCX || {};
  var RDCX = window.RDCX;

  /* ----------------------------------------------------------------
     Utilitaires communs
     ---------------------------------------------------------------- */
  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  function rich(s) { // **gras** -> <strong>, le reste échappé (même règle que flashcards.js)
    return esc(s).split('**').map(function (seg, i) { return i % 2 ? '<strong>' + seg + '</strong>' : seg; }).join('');
  }
  function para(s) { // texte multiligne -> paragraphes
    var lines = String(s == null ? '' : s).split(/\n+/);
    var out = '';
    lines.forEach(function (l) { if (l.replace(/\s/g, '')) out += '<p>' + rich(l) + '</p>'; });
    return out;
  }
  function byId(id) { return id ? document.getElementById(id) : null; }
  function each(list, fn) { Array.prototype.forEach.call(list, fn); }
  function seq(n) { var a = [], i; for (i = 0; i < n; i++) a.push(i); return a; }
  function shuffle(a) {
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }
  function mount(node, variante) { node.classList.add('rdcx'); node.classList.add(variante); }
  function focusNode(n) { if (n) { try { n.focus(); } catch (e) {} } }
  function loadJSON(key) { try { return JSON.parse(localStorage.getItem(key)) || {}; } catch (e) { return {}; } }
  function saveJSON(key, v) { try { localStorage.setItem(key, JSON.stringify(v)); } catch (e) {} }
  function nowId(p) { return p + '-' + Math.random().toString(36).slice(2, 8); }

  // Émission d'un événement personnalisé, avec repli document.createEvent
  // pour les moteurs qui ne savent pas construire un CustomEvent.
  function emet(nom, detail) {
    var ev;
    try {
      ev = new CustomEvent(nom, { detail: detail, bubbles: true, cancelable: false });
    } catch (e) {
      ev = document.createEvent('CustomEvent');
      ev.initCustomEvent(nom, true, false, detail);
    }
    document.dispatchEvent(ev);
  }

  // Exécute fn une fois le document analysé (les fabriques appelées plus bas
  // dans la page ont alors terminé d'injecter leur HTML).
  function quandPret(fn) {
    if (document.readyState === 'interactive' || document.readyState === 'complete') {
      setTimeout(fn, 0);
      return;
    }
    document.addEventListener('DOMContentLoaded', function () { setTimeout(fn, 0); });
  }

  // En-tête commun : icône + titre (+ compteur / étape à droite)
  function head(ico, titre, asideHTML) {
    return '<div class="rdcx-head">'
      + '<span class="rdcx-ico" aria-hidden="true">' + esc(ico) + '</span>'
      + '<span class="rdcx-title">' + rich(titre) + '</span>'
      + (asideHTML ? '<span class="rdcx-aside">' + asideHTML + '</span>' : '')
      + '</div>';
  }

  // Numéro de la section .content-section qui contient le conteneur (pour « relisez la section 3 »)
  function sectionNum(node) {
    var p = node;
    while (p && p !== document.body) {
      if (p.classList && p.classList.contains('content-section')) {
        var h = p.querySelector('h2');
        var m = h ? String(h.textContent).match(/^\s*(\d+)/) : null;
        return m ? m[1] : '';
      }
      p = p.parentNode;
    }
    return '';
  }

  var LETTRES = ['A', 'B', 'C', 'D', 'E', 'F'];

  // Explication complète d'une question à choix. Une explication qui ne dit que
  // pourquoi la bonne réponse est juste laisse l'étudiant seul avec son erreur :
  // c'est pourtant la proposition qu'il a choisie qu'il faut démonter.
  // q.pourquoi suit l'ordre des propositions : pourquoi chacune des autres ne
  // convient pas (la case de la bonne réponse reste vide). q.approfondir :
  // [[libellé, adresse], …], deux à quatre renvois vers l'endroit exact du cours
  // qui répond. Une adresse du cours (#ancre ou page .html relative) s'ouvre dans
  // le même onglet ; une adresse externe (https://) dans un nouvel onglet,
  // signalé aux lecteurs d'écran. Toute autre forme d'adresse est écartée.
  function lienExplication(l) {
    var t = l && (l.t || l[0]), u = l && (l.u || l[1]);
    if (!t || !u) return '';
    if (/^https:\/\/[^\s"'<>]+$/.test(u)) {
      return '<a href="' + esc(u) + '" target="_blank" rel="noopener noreferrer">' + rich(t)
        + '<span class="rdcx-ext" aria-hidden="true">↗</span><span class="sr-only"> '
        + esc(T('lien.nouvelOnglet')) + '</span></a>';
    }
    if (/^(#[\w-]+|(\.\.\/|\.\/)?[\w.\/-]+\.html(#[\w-]+)?)$/.test(u)) return '<a href="' + esc(u) + '">' + rich(t) + '</a>';
    return '';
  }
  function autresPropositions(q, choisi) {
    var p = q.pourquoi || [], items = '';
    (q.options || []).forEach(function (o, k) {
      if (k === q.correct || !p[k]) return;
      var lettre = esc(LETTRES[k] || (k + 1));
      items += '<li' + (k === choisi ? ' class="is-choisi"' : '') + '>'
        + '<span class="rdcx-fb-lettre" aria-hidden="true">' + lettre + '</span>'
        + '<span><span class="sr-only">' + esc(T('controle.proposition')) + ' ' + lettre + esc(T('controle.deuxPoints')) + '</span>' + rich(p[k])
        + (k === choisi ? ' <strong class="rdcx-fb-vous">' + esc(T('controle.votreChoix')) + '</strong>' : '') + '</span></li>';
    });
    return items ? '<p class="rdcx-fb-titre">' + esc(T('controle.pourquoiPas')) + '</p><ul class="rdcx-fb-autres">' + items + '</ul>' : '';
  }
  function pourApprofondir(liens) {
    var out = (liens || []).map(lienExplication).filter(Boolean);
    return out.length ? '<p class="rdcx-fb-liens"><span class="rdcx-fb-titre">' + esc(T('controle.approfondir')) + '</span> '
      + out.join('<span class="rdcx-fb-sep" aria-hidden="true"> · </span>') + '</p>' : '';
  }

  /* ----------------------------------------------------------------
     1. Point de contrôle de fin de section
        cfg = { titre, questions:[ { q, options:[…], correct, explication,
                                     pourquoi:[…], approfondir:[[libellé, adresse], …] } ] }
        pourquoi et approfondir sont facultatifs (voir autresPropositions,
        pourApprofondir) — mais attendus : prompts/15_explications_quiz.md.
     ---------------------------------------------------------------- */
  RDCX.checkpoint = function (containerId, cfg) {
    var box = byId(containerId); if (!box) return;
    cfg = cfg || {};
    var QS = cfg.questions || [];
    if (!QS.length) return;
    mount(box, 'rdcx-checkpoint');

    var titre = cfg.titre || T('controle.titre');
    var i = 0, score = 0, emis = false;

    function question(auto) {
      var q = QS[i] || {};
      var options = (q.options || []).map(function (o, k) {
        return '<button type="button" class="rdcx-opt" data-k="' + k + '">'
          + '<span class="rdcx-opt-letter" aria-hidden="true">' + esc(LETTRES[k] || (k + 1)) + '</span>'
          + '<span class="rdcx-opt-txt">' + rich(o) + '</span></button>';
      }).join('');

      box.innerHTML = head('✅', titre, 'Question ' + (i + 1) + ' / ' + QS.length)
        + '<div class="rdcx-body">'
        + '  <p class="rdcx-q" tabindex="-1">' + rich(q.q) + '</p>'
        + '  <div class="rdcx-opts" role="group" aria-label="' + T('controle.propositions') + '">' + options + '</div>'
        + '  <div class="rdcx-fb" aria-live="polite"></div>'
        + '  <div class="rdcx-actions"><button type="button" class="rdcx-btn rdcx-btn-main rdcx-next" hidden>'
        + (i === QS.length - 1 ? T('etapes.voirResultat') : T('controle.suivante')) + '</button></div>'
        + '</div>';

      var opts = box.querySelectorAll('.rdcx-opt');
      var fb = box.querySelector('.rdcx-fb');
      var next = box.querySelector('.rdcx-next');
      var repondu = false;

      each(opts, function (b) {
        b.addEventListener('click', function () {
          if (repondu) return; repondu = true;
          var k = parseInt(b.getAttribute('data-k'), 10);
          var ok = k === q.correct;
          if (ok) score++;
          each(opts, function (x) {
            var xk = parseInt(x.getAttribute('data-k'), 10);
            if (xk === q.correct) x.classList.add('is-correct');
            else if (x === b) x.classList.add('is-wrong');
            x.disabled = true;
          });
          // Avec les raisons de chaque proposition, la lettre de la bonne réponse est
          // nommée : la liste qui suit parle des autres, par leur lettre.
          var bonne = q.pourquoi ? ' — ' + esc(T('controle.bonneReponse')) + ' ' + esc(LETTRES[q.correct] || (q.correct + 1)) : '';
          fb.innerHTML = '<p class="rdcx-fb-why">'
            + (ok ? '<span class="rdcx-fb-ok">' + esc(T('controle.exact')) + '</span> '
                  : '<span class="rdcx-fb-no">' + esc(T('controle.non')) + bonne + '.</span> ')
            + rich(q.explication || '') + '</p>'
            + autresPropositions(q, k) + pourApprofondir(q.approfondir);
          fb.classList.add('is-shown');
          next.hidden = false;
          // Dernière question répondue : le parcours par étapes (RDCX.steps) est prévenu.
          if (i === QS.length - 1 && !emis) {
            emis = true;
            emet('rdcx:checkpoint', { id: containerId, score: score, total: QS.length });
          }
        });
      });

      next.addEventListener('click', function () { i++; if (i < QS.length) question(true); else resultat(); });
      if (auto) focusNode(box.querySelector('.rdcx-q'));
    }

    function resultat() {
      var parfait = score === QS.length;
      var n = sectionNum(box);
      var msg = parfait
        ? T('controle.acquis')
        : (n ? T('controle.relireSection') + ' ' + n + ' ' + T('controle.avantDeContinuer') : T('controle.relireCette'));
      box.innerHTML = head('✅', titre, T('controle.termine'))
        + '<div class="rdcx-body">'
        + '  <div class="rdcx-score' + (parfait ? ' is-parfait' : '') + '" tabindex="-1" aria-live="polite">'
        + '    <span class="rdcx-score-n">' + score + ' / ' + QS.length + '</span>'
        + '    <span class="rdcx-score-msg">' + esc(msg) + '</span>'
        + '  </div>'
        + '  <div class="rdcx-actions"><button type="button" class="rdcx-btn rdcx-restart">' + T('controle.recommencer') + '</button></div>'
        + '</div>';
      // Un nouveau passage réarme l'émission : le score corrigé remonte au parcours.
      box.querySelector('.rdcx-restart').addEventListener('click', function () { i = 0; score = 0; emis = false; question(true); });
      focusNode(box.querySelector('.rdcx-score'));
    }

    question(false);
  };

  /* ----------------------------------------------------------------
     2. Prédiction avant révélation (effet de génération)
        cfg = { question, indice, reponse, pourquoi, champ:"texte"|"choix", options:[…] }
     ---------------------------------------------------------------- */
  RDCX.reveal = function (containerId, cfg) {
    var box = byId(containerId); if (!box) return;
    cfg = cfg || {};
    mount(box, 'rdcx-reveal');

    var choix = cfg.champ === 'choix' && (cfg.options || []).length;
    var idQ = nowId('rdcx-q');
    var idF = nowId('rdcx-f');
    var champ;

    if (choix) {
      champ = '<div class="rdcx-choices" role="group" aria-labelledby="' + idQ + '">'
        + (cfg.options || []).map(function (o, k) {
            return '<label class="rdcx-choice"><input type="radio" name="' + idF + '" value="' + k + '">'
              + '<span>' + rich(o) + '</span></label>';
          }).join('')
        + '</div>';
    } else {
      champ = '<label class="rdcx-lbl" for="' + idF + '">' + T('controle.votreHypothese') + '</label>'
        + '<textarea class="rdcx-textarea" id="' + idF + '" rows="3" '
        + 'placeholder="Écrivez ce que vous pensez — même incertain : c\'est l\'essai qui fait apprendre."></textarea>';
    }

    box.innerHTML = head('🤔', T('controle.avantDeLire'))
      + '<div class="rdcx-body">'
      + '  <p class="rdcx-q" id="' + idQ + '" tabindex="-1">' + rich(cfg.question) + '</p>'
      + (cfg.indice ? '  <p class="rdcx-hint">💡 Indice : ' + rich(cfg.indice) + '</p>' : '')
      + '  <div class="rdcx-engage">' + champ + '</div>'
      + '  <div class="rdcx-actions"><button type="button" class="rdcx-btn rdcx-btn-main rdcx-show" disabled '
      + 'aria-describedby="' + idQ + '">' + T('controle.reveler') + '</button>'
      + '<span class="rdcx-note">Répondez d\'abord — même approximativement.</span></div>'
      + '  <div class="rdcx-out" tabindex="-1" aria-live="polite"></div>'
      + '</div>';

    var btn = box.querySelector('.rdcx-show');
    var note = box.querySelector('.rdcx-note');
    var out = box.querySelector('.rdcx-out');

    function reponseSaisie() {
      if (choix) {
        var r = box.querySelector('.rdcx-choices input:checked');
        return r ? (cfg.options || [])[parseInt(r.value, 10)] : '';
      }
      var t = box.querySelector('.rdcx-textarea');
      return t ? t.value.replace(/^\s+|\s+$/g, '') : '';
    }
    function verrou() {
      var ok = !!reponseSaisie();
      btn.disabled = !ok;
      if (note) note.hidden = ok;
    }

    if (choix) each(box.querySelectorAll('.rdcx-choices input'), function (r) { r.addEventListener('change', verrou); });
    else {
      var ta = box.querySelector('.rdcx-textarea');
      ta.addEventListener('input', verrou);
      ta.addEventListener('keydown', function (e) {
        if ((e.key === 'Enter' || e.keyCode === 13) && (e.ctrlKey || e.metaKey) && !btn.disabled) { e.preventDefault(); btn.click(); }
      });
    }

    btn.addEventListener('click', function () {
      var mienne = reponseSaisie();
      if (!mienne) return;
      btn.disabled = true;
      each(box.querySelectorAll('.rdcx-engage input, .rdcx-engage textarea'), function (f) { f.disabled = true; });
      out.innerHTML =
          '<div class="rdcx-compare">'
        + '  <div class="rdcx-col-mine"><span class="rdcx-col-head">' + T('controle.votreReponse') + '</span><div class="rdcx-col-txt">' + rich(mienne) + '</div></div>'
        + '  <div class="rdcx-col-good"><span class="rdcx-col-head">' + T('controle.laReponse') + '</span><div class="rdcx-col-txt">' + rich(cfg.reponse) + '</div></div>'
        + '</div>'
        + (cfg.pourquoi ? '<div class="rdcx-why"><strong>Pourquoi&nbsp;:</strong> ' + rich(cfg.pourquoi) + '</div>' : '');
      out.classList.add('is-shown');
      focusNode(out);
    });

    verrou();
  };

  /* ----------------------------------------------------------------
     3. Repérage d'erreur dans un document
        cfg = { consigne, intro, fragments:[ { t, faux, pourquoi } ], conclusion }
     ---------------------------------------------------------------- */
  RDCX.spotError = function (containerId, cfg) {
    var box = byId(containerId); if (!box) return;
    cfg = cfg || {};
    var FR = cfg.fragments || [];
    if (!FR.length) return;
    mount(box, 'rdcx-spot');

    var total = 0;
    FR.forEach(function (f) { if (f.faux) total++; });
    var trouves = 0;
    var base = nowId('rdcx-spot');

    var doc = FR.map(function (f, k) {
      return '<li class="rdcx-frag-item">'
        + '<button type="button" class="rdcx-frag" data-k="' + k + '">' + rich(f.t) + '</button>'
        + '<div class="rdcx-frag-why" id="' + base + '-why' + k + '" role="status" hidden></div>'
        + '</li>';
    }).join('');

    box.innerHTML = head('🔍', T('erreurs.titre'),
        '<span class="rdcx-count" aria-live="polite">0 / ' + total + ' erreur' + (total > 1 ? 's' : '') + ' trouvée' + (total > 1 ? 's' : '') + '</span>')
      + '<div class="rdcx-body">'
      + '  <p class="rdcx-consigne">' + rich(cfg.consigne) + '</p>'
      + (cfg.intro ? '  <p class="rdcx-intro">' + rich(cfg.intro) + '</p>' : '')
      + '  <ul class="rdcx-doc">' + doc + '</ul>'
      + '  <div class="rdcx-fb" aria-live="polite"></div>'
      + '  <div class="rdcx-final" hidden tabindex="-1"></div>'
      + '</div>';

    var cnt = box.querySelector('.rdcx-count');
    var fb = box.querySelector('.rdcx-fb');
    var fin = box.querySelector('.rdcx-final');

    each(box.querySelectorAll('.rdcx-frag'), function (b) {
      var k = parseInt(b.getAttribute('data-k'), 10);
      var f = FR[k] || {};
      var why = b.parentNode.querySelector('.rdcx-frag-why');
      var minuteur = null;

      b.addEventListener('click', function () {
        if (f.faux) {
          if (b.classList.contains('is-faux')) return;
          b.classList.add('is-faux');
          why.innerHTML = '<span class="rdcx-fb-no">⚠ Erreur.</span> ' + rich(f.pourquoi || '');
          why.hidden = false;
          b.setAttribute('aria-describedby', why.id);
          trouves++;
          cnt.textContent = trouves + ' / ' + total + ' erreur' + (total > 1 ? 's' : '') + ' trouvée' + (total > 1 ? 's' : '');
          fb.innerHTML = '';
          if (trouves === total) {
            fin.innerHTML = '<span class="rdcx-fb-ok">🎯 Toutes les erreurs sont repérées.</span> '
              + rich(cfg.conclusion || T('erreurs.bilan'));
            fin.hidden = false;
            focusNode(fin);
          }
        } else {
          b.classList.remove('is-ok');
          if (minuteur) clearTimeout(minuteur);
          // relance de l'animation : forcer un reflow avant de remettre la classe
          void b.offsetWidth;
          b.classList.add('is-ok');
          minuteur = setTimeout(function () { b.classList.remove('is-ok'); }, 1200);
          fb.innerHTML = '<span class="rdcx-fb-neutre">Celui-ci est correct.</span> Cherchez ailleurs.';
        }
      });
    });
  };

  /* ----------------------------------------------------------------
     4. Appariement (clic gauche puis clic droite — utilisable au clavier)
        cfg = { consigne, colonneGauche, colonneDroite, paires:[ { g, d, ex } ] }
     ---------------------------------------------------------------- */
  RDCX.match = function (containerId, cfg) {
    var box = byId(containerId); if (!box) return;
    cfg = cfg || {};
    var P = cfg.paires || [];
    if (!P.length) return;
    mount(box, 'rdcx-match');

    var total = P.length;

    function build() {
      var ordre = shuffle(seq(total));
      var gauche = P.map(function (p, k) {
        return '<div class="rdcx-item-wrap">'
          + '<button type="button" class="rdcx-item rdcx-item-g" data-k="' + k + '" aria-pressed="false">' + rich(p.g) + '</button>'
          + '<p class="rdcx-item-ex" hidden></p></div>';
      }).join('');
      var droite = ordre.map(function (k) {
        return '<button type="button" class="rdcx-item rdcx-item-d" data-k="' + k + '" aria-pressed="false">' + rich(P[k].d) + '</button>';
      }).join('');

      box.innerHTML = head('🔗', T('match.consigne'),
          '<span class="rdcx-count" aria-live="polite">0 / ' + total + ' paires trouvées</span>')
        + '<div class="rdcx-body">'
        + '  <p class="rdcx-consigne">' + rich(cfg.consigne || T('match.aide')) + '</p>'
        + '  <div class="rdcx-match-grid">'
        + '    <div class="rdcx-col"><h4 class="rdcx-colhead">' + rich(cfg.colonneGauche || 'Colonne A') + '</h4>' + gauche + '</div>'
        + '    <div class="rdcx-col"><h4 class="rdcx-colhead">' + rich(cfg.colonneDroite || 'Colonne B') + '</h4>' + droite + '</div>'
        + '  </div>'
        + '  <div class="rdcx-fb" aria-live="polite"></div>'
        + '  <div class="rdcx-actions"><button type="button" class="rdcx-btn rdcx-restart">↺ Recommencer</button></div>'
        + '</div>';

      var cnt = box.querySelector('.rdcx-count');
      var fb = box.querySelector('.rdcx-fb');
      var selG = null, selD = null, faits = 0;

      function deselect(b) { if (b) { b.classList.remove('is-sel'); b.setAttribute('aria-pressed', 'false'); } }
      function select(b) { b.classList.add('is-sel'); b.setAttribute('aria-pressed', 'true'); }

      function secousse(b) {
        b.classList.remove('is-shake');
        void b.offsetWidth;
        b.classList.add('is-shake');
        setTimeout(function () { b.classList.remove('is-shake'); }, 500);
      }

      function evalue() {
        if (!selG || !selD) return;
        var g = selG, d = selD;
        selG = null; selD = null;
        if (g.getAttribute('data-k') === d.getAttribute('data-k')) {
          var k = parseInt(g.getAttribute('data-k'), 10);
          [g, d].forEach(function (b) {
            deselect(b);
            b.classList.remove('is-shake'); // une secousse en cours ne doit pas colorer une bonne paire
            b.classList.add('is-done');
            b.disabled = true;
            b.removeAttribute('aria-pressed');
          });
          var ex = g.parentNode.querySelector('.rdcx-item-ex');
          ex.innerHTML = '↔ <strong>' + rich(P[k].d) + '</strong>' + (P[k].ex ? ' — <em>' + rich(P[k].ex) + '</em>' : '');
          ex.hidden = false;
          faits++;
          cnt.textContent = faits + ' / ' + total + ' paires trouvées';
          fb.innerHTML = faits === total
            ? '<span class="rdcx-fb-ok">🎯 Toutes les paires sont trouvées.</span>'
            : '<span class="rdcx-fb-ok">✅ Bonne association.</span>';
        } else {
          secousse(g); secousse(d);
          deselect(g); deselect(d);
          fb.innerHTML = '<span class="rdcx-fb-no">❌ Ces deux-là ne vont pas ensemble.</span> Réessayez.';
        }
      }

      each(box.querySelectorAll('.rdcx-item'), function (b) {
        b.addEventListener('click', function () {
          if (b.disabled) return;
          var droiteCol = b.classList.contains('rdcx-item-d');
          var courant = droiteCol ? selD : selG;
          if (courant === b) { deselect(b); if (droiteCol) selD = null; else selG = null; return; }
          deselect(courant);
          select(b);
          if (droiteCol) selD = b; else selG = b;
          evalue();
        });
      });

      box.querySelector('.rdcx-restart').addEventListener('click', function () { build(); focusNode(box.querySelector('.rdcx-item-g')); });
    }

    build();
  };

  /* ----------------------------------------------------------------
     5. Cas à embranchements (on n'empêche pas d'avancer, on explique)
        cfg = { titre, intro, etapes:[ { situation, question, choix:[ { t, bon, consequence } ] } ], conclusion }
     ---------------------------------------------------------------- */
  RDCX.branch = function (containerId, cfg) {
    var box = byId(containerId); if (!box) return;
    cfg = cfg || {};
    var E = cfg.etapes || [];
    if (!E.length) return;
    mount(box, 'rdcx-branch');

    var titre = cfg.titre || 'Cas pratique';
    var i = 0, parcours = [];

    function etape(auto) {
      var e = E[i] || {};
      var choix = (e.choix || []).map(function (c, k) {
        return '<button type="button" class="rdcx-opt" data-k="' + k + '">'
          + '<span class="rdcx-opt-letter" aria-hidden="true">' + esc(LETTRES[k] || (k + 1)) + '</span>'
          + '<span class="rdcx-opt-txt">' + rich(c.t) + '</span></button>';
      }).join('');

      box.innerHTML = head('🧭', titre, T('etapes.etape') + ' ' + (i + 1) + ' ' + T('etapes.sur') + ' ' + E.length)
        + '<div class="rdcx-body">'
        + (i === 0 && cfg.intro ? '  <p class="rdcx-intro">' + rich(cfg.intro) + '</p>' : '')
        + '  <div class="rdcx-situation">' + rich(e.situation) + '</div>'
        + '  <p class="rdcx-q" tabindex="-1">' + rich(e.question) + '</p>'
        + '  <div class="rdcx-opts" role="group" aria-label="' + T('scenario.decisions') + '">' + choix + '</div>'
        + '  <div class="rdcx-conseq" aria-live="polite"></div>'
        + '  <div class="rdcx-actions"><button type="button" class="rdcx-btn rdcx-btn-main rdcx-next" hidden>'
        + (i === E.length - 1 ? 'Conclure ›' : T('etapes.suivante')) + '</button></div>'
        + '</div>';

      var opts = box.querySelectorAll('.rdcx-opt');
      var cq = box.querySelector('.rdcx-conseq');
      var next = box.querySelector('.rdcx-next');
      var fait = false;

      each(opts, function (b) {
        b.addEventListener('click', function () {
          if (fait) return; fait = true;
          var c = (e.choix || [])[parseInt(b.getAttribute('data-k'), 10)] || {};
          each(opts, function (x) { x.disabled = true; if (x !== b) x.classList.add('is-pale'); });
          b.classList.add(c.bon ? 'is-correct' : 'is-wrong');
          cq.innerHTML = '<span class="rdcx-conseq-lbl">' + (c.bon ? '✅ ' : '⚠ ') + (cfg.libelleConsequence || T('scenario.consequence')) + '</span>'
            + '<div class="rdcx-conseq-txt">' + rich(c.consequence || '') + '</div>';
          cq.classList.add('is-shown');
          cq.classList.add(c.bon ? 'is-bon' : 'is-risque');
          parcours.push({ q: e.question, t: c.t, bon: !!c.bon });
          next.hidden = false;
        });
      });

      next.addEventListener('click', function () { i++; if (i < E.length) etape(true); else fin(); });
      if (auto) focusNode(box.querySelector('.rdcx-q'));
    }

    function fin() {
      var bons = 0;
      parcours.forEach(function (p) { if (p.bon) bons++; });
      var recap = parcours.map(function (p, k) {
        return '<li class="rdcx-recap-item' + (p.bon ? ' is-bon' : ' is-risque') + '">'
          + '<span class="rdcx-recap-num">' + T('etapes.etape') + ' ' + (k + 1) + '</span>'
          + '<span class="rdcx-recap-txt">' + rich(p.t) + '</span></li>';
      }).join('');

      box.innerHTML = head('🧭', titre, 'Bilan')
        + '<div class="rdcx-body">'
        + '  <div class="rdcx-final" tabindex="-1">' + rich(cfg.conclusion || '') + '</div>'
        + '  <h4 class="rdcx-recap-head">' + T('scenario.vosDecisions') + ' <span class="rdcx-recap-score">' + bons + ' / ' + parcours.length + ' sans risque</span></h4>'
        + '  <ul class="rdcx-recap">' + recap + '</ul>'
        + '  <p class="rdcx-note">Ce cas n\'est pas noté : il sert à mesurer les conséquences de chaque décision.</p>'
        + '  <div class="rdcx-actions"><button type="button" class="rdcx-btn rdcx-restart">' + T('scenario.rejouer') + '</button></div>'
        + '</div>';
      box.querySelector('.rdcx-restart').addEventListener('click', function () { i = 0; parcours = []; etape(true); });
      focusNode(box.querySelector('.rdcx-final'));
    }

    etape(false);
  };

  /* ----------------------------------------------------------------
     6. Schéma à zones cliquables (x / y en % — positionnement responsive)
        cfg = { src, alt, legende, points:[ { x, y, titre, texte } ] }
     ---------------------------------------------------------------- */
  RDCX.hotspots = function (containerId, cfg) {
    var box = byId(containerId); if (!box) return;
    cfg = cfg || {};
    var PTS = cfg.points || [];
    mount(box, 'rdcx-hotspots');

    var src = String(cfg.src || '');
    var nom = src.split('/').pop() || src;
    var base = nowId('rdcx-hs');

    function borne(v) { var n = parseFloat(v); if (isNaN(n)) n = 50; return Math.max(0, Math.min(100, n)); }

    var pins = '', pops = '';
    PTS.forEach(function (p, k) {
      var x = borne(p.x), y = borne(p.y);
      // les positions passent par des variables CSS (et non par left/top en ligne) :
      // la feuille de style peut ainsi reprendre la main sur petit écran
      var ancre = 'style="--rdcx-x:' + (x <= 50 ? x : 100 - x) + '%;--rdcx-y:' + (y <= 55 ? y : 100 - y) + '%"';
      pins += '<button type="button" class="rdcx-hs-pt" data-k="' + k + '" style="left:' + x + '%;top:' + y + '%"'
        + ' id="' + base + '-pt' + k + '" aria-expanded="false" aria-controls="' + base + '-pop' + k + '"'
        + ' aria-label="Point ' + (k + 1) + ' : ' + esc(p.titre) + '"><span aria-hidden="true">' + (k + 1) + '</span></button>';
      pops += '<div class="rdcx-hs-pop ' + (x <= 50 ? 'is-left' : 'is-right') + ' ' + (y <= 55 ? 'is-below' : 'is-above') + '"'
        + ' id="' + base + '-pop' + k + '" ' + ancre + ' hidden>'
        + '<span class="rdcx-hs-pop-title">' + (k + 1) + '. ' + rich(p.titre) + '</span>'
        + '<span class="rdcx-hs-pop-txt">' + rich(p.texte) + '</span>'
        + '<button type="button" class="rdcx-hs-close" data-k="' + k + '" aria-label="Fermer l\'info-bulle">✕</button>'
        + '</div>';
    });

    var liste = PTS.map(function (p, k) {
      return '<li class="rdcx-hs-li"><span class="rdcx-hs-li-num" aria-hidden="true">' + (k + 1) + '</span>'
        + '<span><strong>' + rich(p.titre) + '</strong> — ' + rich(p.texte) + '</span></li>';
    }).join('');

    // Pas d'en-tête de bloc : le schéma et sa liste parlent d'eux-mêmes.
    box.innerHTML =
        '<div class="rdcx-body">'
      + '  <figure class="rdcx-hs-figure">'
      + '    <div class="rdcx-hs-stage">'
      + '      <img class="rdcx-hs-img" src="' + esc(src) + '" alt="' + esc(cfg.alt || 'Schéma du cours') + '">'
      + pins + pops
      + '    </div>'
      + (cfg.legende ? '    <figcaption class="rdcx-hs-cap">' + rich(cfg.legende) + '</figcaption>' : '')
      + '  </figure>'
      + '  <ol class="rdcx-hs-list">' + liste + '</ol>'
      + '</div>';

    var stage = box.querySelector('.rdcx-hs-stage');
    var img = box.querySelector('.rdcx-hs-img');
    var pts = box.querySelectorAll('.rdcx-hs-pt');
    var bulles = box.querySelectorAll('.rdcx-hs-pop');
    var souris = false;

    function fermeTout() {
      each(bulles, function (b) { b.hidden = true; });
      each(pts, function (b) { b.setAttribute('aria-expanded', 'false'); b.classList.remove('is-open'); });
    }
    function ouvre(k) {
      fermeTout();
      bulles[k].hidden = false;
      pts[k].setAttribute('aria-expanded', 'true');
      pts[k].classList.add('is-open');
    }

    stage.addEventListener('mousedown', function () { souris = true; setTimeout(function () { souris = false; }, 0); });

    each(pts, function (b, k) {
      b.addEventListener('click', function () {
        if (bulles[k].hidden) ouvre(k); else fermeTout();
      });
      b.addEventListener('focus', function () { if (!souris) ouvre(k); });
      b.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' || e.keyCode === 27) { fermeTout(); focusNode(b); }
      });
    });
    each(box.querySelectorAll('.rdcx-hs-close'), function (b) {
      b.addEventListener('click', function () {
        var k = parseInt(b.getAttribute('data-k'), 10);
        fermeTout(); focusNode(pts[k]);
      });
    });

    // Image absente : cadre de remplacement, la liste textuelle reste affichée
    img.addEventListener('error', function () {
      fermeTout();
      each(pts, function (b) { b.parentNode.removeChild(b); });
      each(bulles, function (b) { b.parentNode.removeChild(b); });
      stage.classList.add('is-missing');
      stage.innerHTML = '<div class="rdcx-hs-missing">'
        + '<span class="rdcx-hs-missing-ico" aria-hidden="true">🖼️</span>'
        + '<span class="rdcx-hs-missing-t">Schéma à déposer</span>'
        + '<span class="rdcx-hs-missing-f">Fichier attendu : <code>' + esc(nom) + '</code></span>'
        + '<span class="rdcx-hs-missing-p">Chemin : <code>' + esc(src) + '</code></span>'
        + '<span class="rdcx-hs-missing-n">Les points du schéma restent lisibles ci-dessous.</span>'
        + '</div>';
    });
  };

  /* ----------------------------------------------------------------
     7. Capsule audio « voix du formateur »
        cfg = { src, titre, duree, transcription }
     ---------------------------------------------------------------- */
  RDCX.voice = function (containerId, cfg) {
    var box = byId(containerId); if (!box) return;
    cfg = cfg || {};
    mount(box, 'rdcx-voice');

    var src = String(cfg.src || '');
    var nom = src.split('/').pop() || src;
    var idT = nowId('rdcx-tr');

    function mmss(s) {
      s = Math.max(0, Math.floor(s || 0));
      var m = Math.floor(s / 60), r = s % 60;
      return m + ':' + (r < 10 ? '0' : '') + r;
    }

    box.innerHTML =
        '<div class="rdcx-voice-row">'
      + '  <button type="button" class="rdcx-voice-play" aria-label="' + T('lecteur.lire') + '">▶</button>'
      + '  <div class="rdcx-voice-main">'
      + '    <div class="rdcx-voice-meta">'
      + '      <span class="rdcx-voice-ico" aria-hidden="true">🎧</span>'
      + '      <span class="rdcx-voice-titre">' + rich(cfg.titre || 'Capsule audio') + '</span>'
      + '      <span class="rdcx-voice-duree">' + esc(cfg.duree || '') + '</span>'
      + '    </div>'
      + '    <div class="rdcx-voice-bar" role="slider" tabindex="0" aria-label="' + T('lecteur.progression') + '"'
      + ' aria-valuemin="0" aria-valuemax="100" aria-valuenow="0" aria-valuetext="0 %"><div class="rdcx-voice-fill"></div></div>'
      + '  </div>'
      + '  <span class="rdcx-voice-time">0:00</span>'
      + '</div>'
      + '<div class="rdcx-voice-state" aria-live="polite"></div>'
      + '<div class="rdcx-voice-tools">'
      + '  <button type="button" class="rdcx-voice-toggle" aria-expanded="false" aria-controls="' + idT + '">' + T('lecteur.transcriptionAfficher') + '</button>'
      + '</div>'
      + '<div class="rdcx-voice-transcript" id="' + idT + '" hidden>' + para(cfg.transcription) + '</div>';

    var play = box.querySelector('.rdcx-voice-play');
    var bar = box.querySelector('.rdcx-voice-bar');
    var fill = box.querySelector('.rdcx-voice-fill');
    var temps = box.querySelector('.rdcx-voice-time');
    var duree = box.querySelector('.rdcx-voice-duree');
    var etat = box.querySelector('.rdcx-voice-state');
    var bascule = box.querySelector('.rdcx-voice-toggle');
    var texte = box.querySelector('.rdcx-voice-transcript');

    bascule.addEventListener('click', function () {
      var ouvert = texte.hidden;
      texte.hidden = !ouvert;
      bascule.setAttribute('aria-expanded', ouvert ? 'true' : 'false');
      bascule.textContent = ouvert ? T('lecteur.transcriptionMasquer') : T('lecteur.transcriptionAfficher');
    });
    if (!String(cfg.transcription || '').replace(/\s/g, '')) bascule.hidden = true;

    var audio = document.createElement('audio');
    audio.preload = 'metadata';
    audio.className = 'rdcx-voice-audio';
    box.appendChild(audio);

    function pct() {
      if (!audio.duration || !isFinite(audio.duration)) return 0;
      return Math.max(0, Math.min(100, audio.currentTime / audio.duration * 100));
    }
    function peint() {
      var p = pct();
      fill.style.width = p + '%';
      bar.setAttribute('aria-valuenow', Math.round(p));
      bar.setAttribute('aria-valuetext', mmss(audio.currentTime) + (isFinite(audio.duration) ? ' sur ' + mmss(audio.duration) : ''));
      temps.textContent = mmss(audio.currentTime);
    }
    function deplace(ratio) {
      if (!audio.duration || !isFinite(audio.duration)) return;
      audio.currentTime = Math.max(0, Math.min(audio.duration, ratio * audio.duration));
      peint();
    }

    play.addEventListener('click', function () {
      if (audio.paused) { var p = audio.play(); if (p && p.catch) p.catch(function () {}); }
      else audio.pause();
    });
    audio.addEventListener('play', function () { play.textContent = '⏸'; play.setAttribute('aria-label', T('lecteur.pause')); box.classList.add('is-playing'); });
    audio.addEventListener('pause', function () { play.textContent = '▶'; play.setAttribute('aria-label', T('lecteur.lire')); box.classList.remove('is-playing'); });
    audio.addEventListener('ended', function () { play.textContent = '▶'; box.classList.remove('is-playing'); });
    audio.addEventListener('timeupdate', peint);
    audio.addEventListener('loadedmetadata', function () {
      if (isFinite(audio.duration)) duree.textContent = mmss(audio.duration);
      peint();
    });

    bar.addEventListener('click', function (e) {
      var r = bar.getBoundingClientRect();
      if (r.width) deplace((e.clientX - r.left) / r.width);
    });
    bar.addEventListener('keydown', function (e) {
      var k = e.key, pas = 5;
      if (k === 'ArrowRight' || k === 'ArrowUp') { audio.currentTime = Math.min(audio.duration || 0, audio.currentTime + pas); }
      else if (k === 'ArrowLeft' || k === 'ArrowDown') { audio.currentTime = Math.max(0, audio.currentTime - pas); }
      else if (k === 'Home') { audio.currentTime = 0; }
      else if (k === 'End') { audio.currentTime = Math.max(0, (audio.duration || 0) - 0.2); }
      else return;
      e.preventDefault();
      peint();
    });

    // Fichier absent : état « capsule à enregistrer », la transcription reste consultable
    audio.addEventListener('error', function () {
      box.classList.add('is-missing');
      play.disabled = true;
      bar.setAttribute('aria-disabled', 'true');
      bar.removeAttribute('tabindex');
      temps.textContent = '';
      duree.textContent = cfg.duree ? cfg.duree + ' (prévu)' : '';
      etat.innerHTML = '<span class="rdcx-voice-missing">🎙 Capsule à enregistrer — fichier attendu : <code>' + esc(nom) + '</code></span>';
    });

    /* Le lecteur persistant de media.js accueille aussi les capsules : une fois
       lancée, la capsule reste pilotable pendant qu'on fait défiler la page, et
       elle met le podcast en pause plutôt que de se superposer à lui. */
    if (window.RDC_LECTEUR && window.RDC_LECTEUR.attacher) {
      // Le titre est posé en textContent : rien à échapper, seuls les marqueurs
      // de gras de rich() sont à retirer.
      var titrePlat = String(cfg.titre || 'Capsule audio').replace(/\*\*/g, '');
      window.RDC_LECTEUR.attacher(audio, '🎧 ' + titrePlat);
    }

    // src posé en dernier : tous les écouteurs (dont 'error') sont déjà en place
    audio.src = src;
  };

  /* ----------------------------------------------------------------
     8. Progression du chapitre (objectifs cochables + barre + reprise)
        cfg = { chapitre, objectifs:[…] } — un seul appel par page
     ---------------------------------------------------------------- */
  function chapitreCourant() {
    var f = (location.pathname.split('/').pop() || '');
    var m = f.match(/^(\d{1,2})-/);
    return m ? String(parseInt(m[1], 10)) : '';
  }

  function objectifsCochables(chap, liste) {
    var boite = document.querySelector('.chapter-objectives');
    if (!boite) return;
    var ul = boite.querySelector('ul');
    if (!ul && liste && liste.length) {
      ul = document.createElement('ul');
      ul.innerHTML = liste.map(function (o) { return '<li>' + rich(o) + '</li>'; }).join('');
      boite.appendChild(ul);
    }
    if (!ul) return;
    var items = ul.querySelectorAll('li');
    if (!items.length) return;

    ul.classList.add('rdcx-obj');
    var cle = 'rdc-obj-' + chap;
    var etat = loadJSON(cle);

    var compte = document.createElement('p');
    compte.className = 'rdcx-obj-count';
    compte.setAttribute('aria-live', 'polite');
    boite.appendChild(compte);

    function majCompte() {
      var n = 0;
      each(items, function (li, k) { if (etat[k] === true) n++; });
      compte.textContent = n + ' / ' + items.length + ' objectif' + (items.length > 1 ? 's' : '') + ' coché' + (items.length > 1 ? 's' : '')
        + (n === items.length ? ' — chapitre maîtrisé.' : '');
      compte.className = 'rdcx-obj-count' + (n === items.length ? ' is-complet' : '');
    }

    each(items, function (li, k) {
      var cb = document.createElement('input');
      cb.type = 'checkbox';
      cb.className = 'rdcx-obj-cb';
      cb.checked = etat[k] === true;
      var txt = document.createElement('span');
      txt.className = 'rdcx-obj-txt';
      txt.innerHTML = li.innerHTML;
      var lbl = document.createElement('label');
      lbl.className = 'rdcx-obj-lbl';
      lbl.appendChild(cb);
      lbl.appendChild(txt);
      li.innerHTML = '';
      li.appendChild(lbl);
      cb.addEventListener('change', function () {
        etat[k] = cb.checked;
        saveJSON(cle, etat);
        majCompte();
      });
    });

    majCompte();
  }

  function parcoursSections(chap) {
    var secs = document.querySelectorAll('.content-section');
    var total = secs.length;
    if (total < 2) return;

    var cle = 'rdc-pos-' + chap;
    var memo = loadJSON(cle);
    var vu = parseInt(memo.i, 10) || 0;

    var barre = document.createElement('div');
    barre.className = 'rdcx-progress';
    barre.innerHTML =
        '<div class="rdcx-progress-track" role="progressbar" aria-label="Progression dans le chapitre"'
      + ' aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><div class="rdcx-progress-fill"></div></div>'
      + '<span class="rdcx-progress-label">Section 1 / ' + total + '</span>';
    if (!document.querySelector('.sidebar')) barre.classList.add('is-full');
    document.body.appendChild(barre);

    var piste = barre.querySelector('.rdcx-progress-track');
    var jauge = barre.querySelector('.rdcx-progress-fill');
    var etiquette = barre.querySelector('.rdcx-progress-label');

    var entete = document.querySelector('.site-header');
    var marge = (entete ? entete.offsetHeight : 64) + 24;
    var courant = -1; // -1 : force un premier rendu complet (libellé + ARIA) au chargement

    function calcule() {
      var c = 0, k, r;
      for (k = 0; k < total; k++) {
        r = secs[k].getBoundingClientRect();
        if (!r.height && !r.width) continue; // section masquée (parcours par étapes) : elle ne compte pas
        if (r.top <= marge) c = k + 1;
      }
      var fin = secs[total - 1].getBoundingClientRect();
      var bas = (window.pageYOffset || document.documentElement.scrollTop || 0) + window.innerHeight;
      if ((fin.height || fin.width) && bas >= (document.documentElement.scrollHeight || 0) - 8) c = total;
      if (c === courant) return;
      courant = c;
      var pct = Math.round(c / total * 100);
      jauge.style.width = pct + '%';
      piste.setAttribute('aria-valuenow', pct);
      piste.setAttribute('aria-valuetext', 'Section ' + Math.max(c, 1) + ' sur ' + total);
      etiquette.textContent = 'Section ' + Math.max(c, 1) + ' / ' + total;
      if (c > vu) { vu = c; saveJSON(cle, { i: c }); }
    }

    var attente = false;
    function planifie() {
      if (attente) return;
      attente = true;
      window.requestAnimationFrame(function () { attente = false; calcule(); });
    }
    window.addEventListener('scroll', planifie);
    window.addEventListener('resize', planifie);
    calcule();

    // « Reprendre où vous en étiez » — proposition, jamais un saut imposé
    if (vu >= 2 && vu <= total && !location.hash) {
      var cible = secs[vu - 1];
      var h2 = cible.querySelector('h2');
      var repere = document.createElement('div');
      repere.className = 'rdcx-resume';
      repere.innerHTML = '<span class="rdcx-resume-ico" aria-hidden="true">↩</span>'
        + '<button type="button" class="rdcx-resume-link">Reprendre où vous en étiez — section ' + vu
        + (h2 ? ' : « ' + esc(String(h2.textContent).replace(/^\s*\d+\.\s*/, '')) + ' »' : '') + '</button>'
        + '<button type="button" class="rdcx-resume-close" aria-label="Masquer la proposition de reprise">✕</button>';
      var ancre = document.querySelector('.chapter-header');
      if (ancre && ancre.parentNode) ancre.parentNode.insertBefore(repere, ancre.nextSibling);
      else if (secs[0].parentNode) secs[0].parentNode.insertBefore(repere, secs[0]);
      repere.querySelector('.rdcx-resume-link').addEventListener('click', function () {
        if (cible.scrollIntoView) cible.scrollIntoView({ behavior: 'smooth', block: 'start' });
        var t = h2 || cible;
        t.setAttribute('tabindex', '-1');
        setTimeout(function () { focusNode(t); }, 400);
        repere.parentNode.removeChild(repere);
      });
      repere.querySelector('.rdcx-resume-close').addEventListener('click', function () {
        repere.parentNode.removeChild(repere);
      });
    }
  }

  RDCX.progress = function (cfg) {
    cfg = cfg || {};
    if (RDCX._progressFait) return;
    RDCX._progressFait = true;
    var chap = String(cfg.chapitre || chapitreCourant() || '0');
    objectifsCochables(chap, cfg.objectifs);
    parcoursSections(chap);
  };

  /* ----------------------------------------------------------------
     9. Parcours par étapes (RDCX.steps)
        cfg = { chapitre } — un seul appel par page, aucune liste à tenir :
        les étapes sont découvertes dans le DOM.

          <section class="content-section" data-step
                   data-step-titre="Champ d'application"
                   data-step-titre-en="Scope"
                   data-step-duree="4 min"> … </section>

        data-step-titre-en : l'intitulé anglais d'une page en blocs data-tr
        (même règle pour data-sommaire-titre-en, plus bas).

        Les sections sans attribut data-step (en-tête, ressources, accroche)
        ne font pas partie du parcours et restent toujours visibles.
        Les étapes masquées restent dans le DOM : impression, ancres du menu
        latéral et recherche du navigateur continuent de fonctionner.
     ---------------------------------------------------------------- */

  // « 2 min », « 1 h 30 », « 45 » → nombre de minutes (0 si indéchiffrable)
  function minutesDe(txt) {
    var s = String(txt == null ? '' : txt).toLowerCase();
    var hm = s.match(/(\d+)\s*h\s*(\d+)/);
    if (hm) return parseInt(hm[1], 10) * 60 + parseInt(hm[2], 10);
    var n = 0;
    var h = s.match(/(\d+)\s*h/);
    var m = s.match(/(\d+)\s*(?:min|mn)/);
    if (h) n += parseInt(h[1], 10) * 60;
    if (m) n += parseInt(m[1], 10);
    if (!h && !m) { var b = s.match(/(\d+)/); if (b) n = parseInt(b[1], 10); }
    return n > 0 ? n : 0;
  }

  function dureeTexte(n) {
    if (n <= 0) return '';
    if (n < 60) return n + ' min';
    var h = Math.floor(n / 60), r = n % 60;
    return h + ' h' + (r ? ' ' + (r < 10 ? '0' + r : r) : '');
  }

  /* Un intitulé porté par un attribut a sa version anglaise à côté :
     data-step-titre="…" data-step-titre-en="…". Les blocs data-tr ne couvrent
     pas les attributs : sans elle, la vue anglaise gardait l'intitulé français.
     Une page d'une seule langue (site miroir) n'a que data-step-titre, dans sa
     langue. */
  function attrLangue(el, nom) {
    var lg = (window.TPLI18N && TPLI18N.lang && TPLI18N.lang()) || 'fr';
    var t = el.getAttribute(nom + '-' + lg);
    return t && t.replace(/\s/g, '') ? t : el.getAttribute(nom);
  }
  // Le texte d'un titre dans la langue affichée : son bloc data-tr s'il en a.
  function texteAffiche(el) {
    var lg = (window.TPLI18N && TPLI18N.lang && TPLI18N.lang()) || 'fr';
    var s = el.querySelector('[data-tr="' + lg + '"]');
    return String((s || el).textContent);
  }

  // Titre de l'étape : data-step-titre, sinon le h2 débarrassé de sa numérotation
  function titreEtape(sec, k) {
    var t = attrLangue(sec, 'data-step-titre');
    if (t && t.replace(/\s/g, '')) return t;
    var h = sec.querySelector('h2');
    if (h) return texteAffiche(h).replace(/^\s*\d+\.\s*/, '').replace(/^\s+|\s+$/g, '');
    return T('etapes.etape') + ' ' + (k + 1);
  }

  function dansUnChamp(el) {
    if (!el) return false;
    var tag = String(el.tagName || '').toLowerCase();
    if (tag === 'input' || tag === 'textarea' || tag === 'select') return true;
    if (el.isContentEditable) return true;
    // le curseur de la capsule audio consomme déjà les flèches
    return !!(el.getAttribute && el.getAttribute('role') === 'slider');
  }

  RDCX.steps = function (cfg) {
    cfg = cfg || {};
    var secs = document.querySelectorAll('.content-section[data-step]');
    var N = secs.length;
    if (!N) return;                // page sans parcours : la fabrique ne fait rien
    if (RDCX._stepsFait) return;   // un seul parcours par page
    RDCX._stepsFait = true;

    var chap = String(cfg.chapitre || chapitreCourant() || '0');
    var clePos = 'rdc-step-' + chap;       // étape courante        { i: 3 }
    var cleFait = 'rdc-stepdone-' + chap;  // étapes validées       { "3": { v, s, t, r } }
    var cleMode = 'rdc-stepmode-' + chap;  // mode de lecture       { mode: 'etapes' | 'tout' }

    var k;
    var titres = [], durees = [];
    for (k = 0; k < N; k++) {
      titres.push(titreEtape(secs[k], k));
      durees.push(minutesDe(secs[k].getAttribute('data-step-duree')));
    }

    var faits = loadJSON(cleFait);
    var resultats = {};            // { <étape> : { <id du point de contrôle> : { s, t } } }
    for (k = 0; k < N; k++) if (faits[k] && faits[k].r) resultats[k] = faits[k].r;

    var i = parseInt(loadJSON(clePos).i, 10);
    if (isNaN(i) || i < 0 || i > N) i = 0;   // i === N : écran de fin
    var continu = loadJSON(cleMode).mode === 'tout';
    var pret = false;

    /* ---------- construction du fil, de la barre de navigation et de l'écran de fin ---------- */
    var dots = '';
    for (k = 0; k < N; k++) {
      dots += '<li class="rdcx-steps-dot-li">'
        + '<button type="button" class="rdcx-steps-dot" data-i="' + k + '">'
        + '<span class="rdcx-steps-dot-n" aria-hidden="true">' + (k + 1) + '</span></button></li>';
    }

    var fil = document.createElement('nav');
    fil.className = 'rdcx-steps';
    fil.setAttribute('aria-label', 'Parcours du chapitre');
    fil.innerHTML =
        '<div class="rdcx-steps-bar">'
      + '  <ol class="rdcx-steps-dots">' + dots + '</ol>'
      + '  <div class="rdcx-steps-meta">'
      + '    <span class="rdcx-steps-pos" aria-live="polite"></span>'
      + '    <span class="rdcx-steps-reste"></span>'
      + '  </div>'
      + '  <button type="button" class="rdcx-steps-mode">' + T('etapes.tout') + '</button>'
      + '</div>'
      + '<div class="rdcx-steps-continu" hidden>'
      + '  <span class="rdcx-steps-continu-txt">' + T('etapes.lectureContinue') + '</span>'
      + '  <button type="button" class="rdcx-steps-retour">' + T('etapes.retour') + '</button>'
      + '</div>';
    secs[0].parentNode.insertBefore(fil, secs[0]);

    var nav = document.createElement('div');
    nav.className = 'rdcx-steps-nav';
    nav.innerHTML =
        '<button type="button" class="rdcx-btn rdcx-steps-prec">' + T('etapes.precedent') + '</button>'
      + '<span class="rdcx-steps-nav-pos"></span>'
      + '<button type="button" class="rdcx-btn rdcx-btn-main rdcx-steps-suiv">'
      + '<span class="rdcx-steps-suiv-lbl">' + T('etapes.suivant') + '</span>'
      + '<span class="rdcx-steps-suiv-titre"></span></button>';

    var fin = document.createElement('section');
    fin.className = 'rdcx rdcx-steps-fin';
    fin.setAttribute('tabindex', '-1');
    fin.hidden = true;
    secs[N - 1].parentNode.insertBefore(fin, secs[N - 1].nextSibling);

    /* ---------- état ---------- */
    function estFait(n) { var f = faits[n]; return !!(f && f.v); }
    function scoreDe(n) {
      var f = faits[n] || {};
      return { s: parseInt(f.s, 10) || 0, t: parseInt(f.t, 10) || 0 };
    }
    function resteMin() {
      var n = 0, j;
      for (j = 0; j < N; j++) if (!estFait(j)) n += durees[j];
      return n;
    }
    function indexEtape(node) {
      var p = node, j;
      while (p && p !== document.body) {
        for (j = 0; j < N; j++) if (secs[j] === p) return j;
        p = p.parentNode;
      }
      return -1;
    }
    // Une étape sans point de contrôle est simplement marquée vue.
    function marqueVue(n) {
      if (!pret || n < 0 || n >= N) return;
      if (estFait(n)) return;
      if (secs[n].querySelector('.rdcx-checkpoint')) return;
      faits[n] = { v: 1, s: 0, t: 0 };
      saveJSON(cleFait, faits);
    }

    /* ---------- rendu ---------- */
    function rendSections() {
      var j;
      for (j = 0; j < N; j++) {
        if (continu || j === i) secs[j].classList.remove('rdcx-step-off');
        else secs[j].classList.add('rdcx-step-off');
      }
    }

    function rendFil() {
      fil.className = 'rdcx-steps' + (continu ? ' is-continu' : '');
      fil.querySelector('.rdcx-steps-bar').hidden = continu;
      fil.querySelector('.rdcx-steps-continu').hidden = !continu;
      each(fil.querySelectorAll('.rdcx-steps-dot'), function (b, j) {
        var f = estFait(j), r = scoreDe(j);
        var partiel = r.t && r.s < r.t;
        b.className = 'rdcx-steps-dot'
          + (f ? ' is-done' : '')
          + (partiel ? ' is-partiel' : '')
          + (j === i && !continu ? ' is-current' : '');
        b.querySelector('.rdcx-steps-dot-n').textContent = f ? '✓' : (j + 1);
        b.setAttribute('title', (j + 1) + '. ' + titres[j] + (durees[j] ? ' — ' + dureeTexte(durees[j]) : ''));
        b.setAttribute('aria-label', T('etapes.etape') + ' ' + (j + 1) + ' : ' + titres[j]
          + (f ? ' ' + T('controle.valide') : '') + (r.t ? ' — ' + r.s + ' ' + T('etapes.surN') + ' ' + r.t : ''));
        if (j === i && !continu) b.setAttribute('aria-current', 'step');
        else b.removeAttribute('aria-current');
      });
      fil.querySelector('.rdcx-steps-pos').textContent =
        i >= N ? T('etapes.chapitreTermine')
               : (T('etapes.etape') + ' ' + (i + 1) + ' ' + T('etapes.sur') + ' ' + N);
      var reste = resteMin();
      fil.querySelector('.rdcx-steps-reste').textContent = reste ? T('etapes.reste') + ' ' + dureeTexte(reste) : '';
      /* Ces libelles sont ecrits a la construction de la barre : sans cette
         reecriture ils resteraient dans la langue du chargement. */
      var bMode = fil.querySelector('.rdcx-steps-mode');
      if (bMode) bMode.textContent = continu ? T('etapes.retour') : T('etapes.tout');
      var bRet = fil.querySelector('.rdcx-steps-retour');
      if (bRet) bRet.textContent = T('etapes.retour');
    }

    function rendNav() {
      if (continu || i >= N) {
        if (nav.parentNode) nav.parentNode.removeChild(nav);
        return;
      }
      var sec = secs[i];
      sec.parentNode.insertBefore(nav, sec.nextSibling);
      var dernier = (i === N - 1);
      var suiv = nav.querySelector('.rdcx-steps-suiv');
      var titreSuiv = suiv.querySelector('.rdcx-steps-suiv-titre');
      var prec = nav.querySelector('.rdcx-steps-prec');
      prec.disabled = (i === 0);
      prec.textContent = T('etapes.precedent');
      nav.querySelector('.rdcx-steps-nav-pos').textContent =
        T('etapes.etape') + ' ' + (i + 1) + ' ' + T('etapes.sur') + ' ' + N;
      suiv.className = 'rdcx-btn rdcx-btn-main rdcx-steps-suiv' + (dernier ? ' is-fin' : '');
      suiv.querySelector('.rdcx-steps-suiv-lbl').textContent = dernier ? T('etapes.terminer') : T('etapes.suivant');
      titreSuiv.textContent = dernier ? '' : ((i + 2) + '. ' + titres[i + 1]);
      titreSuiv.hidden = dernier;
    }

    function rendFin() {
      if (continu || i < N) { fin.hidden = true; fin.innerHTML = ''; return; }
      var j, valides = 0, s = 0, t = 0, revoir = [], r;
      for (j = 0; j < N; j++) {
        if (estFait(j)) valides++;
        r = scoreDe(j);
        s += r.s; t += r.t;
        if (r.t && r.s < r.t) revoir.push(j);
      }
      var complet = (valides === N) && !revoir.length;
      var liste = revoir.map(function (j) {
        var x = scoreDe(j);
        return '<li class="rdcx-steps-revoir-li">'
          + '<button type="button" class="rdcx-steps-revoir-lien" data-i="' + j + '">'
          + '<span class="rdcx-steps-revoir-num">' + T('etapes.etape') + ' ' + (j + 1) + '</span>'
          + '<span class="rdcx-steps-revoir-txt">' + esc(titres[j]) + '</span>'
          + '<span class="rdcx-steps-revoir-score">' + x.s + ' / ' + x.t + '</span></button></li>';
      }).join('');

      fin.innerHTML = head('🏁', '' + T('etapes.chapitreTermine') + ' — ' + valides + ' / ' + N, 'Bilan')
        + '<div class="rdcx-body">'
        + '  <div class="rdcx-score' + (complet ? ' is-parfait' : '') + '">'
        + '    <span class="rdcx-score-n">' + valides + ' / ' + N + '</span>'
        + '    <span class="rdcx-score-msg">' + esc(valides === N
              ? 'étapes validées — le chapitre est parcouru en entier.'
              : 'étapes validées — les autres restent ouvertes.') + '</span>'
        + '  </div>'
        + (t
            ? '  <p class="rdcx-steps-cumul">Points de contrôle du chapitre : <strong>' + s + ' / ' + t + '</strong> bonnes réponses.</p>'
            : '  <p class="rdcx-steps-cumul">' + T('etapes.sansControle') + '</p>')
        + (revoir.length
            ? '  <h4 class="rdcx-steps-revoir-head">' + T('etapes.aRevoir') + '</h4>'
              + '  <ul class="rdcx-steps-revoir">' + liste + '</ul>'
            : '  <p class="rdcx-steps-cumul">' + T('etapes.aucuneARevoir') + '</p>')
        + '  <div class="rdcx-actions">'
        + '    <button type="button" class="rdcx-btn rdcx-btn-main rdcx-steps-reprise">' + T('etapes.revenirPremiere') + '</button>'
        + '  </div>'
        + '</div>';
      fin.hidden = false;
      each(fin.querySelectorAll('.rdcx-steps-revoir-lien'), function (b) {
        b.addEventListener('click', function () { va(parseInt(b.getAttribute('data-i'), 10), true); });
      });
      fin.querySelector('.rdcx-steps-reprise').addEventListener('click', function () { va(0, true); });
    }

    function rend() { rendSections(); rendNav(); rendFin(); rendFil(); }

    /* La barre d'etapes est fabriquee en JavaScript : elle ne peut pas etre
       jumelee en data-tr comme le contenu redige. Sans ce redessin, elle
       resterait en francais sur une page passee en anglais — et c'est
       l'element le plus visible d'une page de chapitre. */
    document.addEventListener('tpl:langchange', rend);

    /* ---------- navigation ---------- */
    function va(n, deplacer) {
      if (isNaN(n)) return;
      i = Math.max(0, Math.min(N, n));
      saveJSON(clePos, { i: i });
      marqueVue(i);
      rend();
      if (!deplacer) return;
      var cible = (i >= N) ? fin : secs[i];
      if (cible.scrollIntoView) cible.scrollIntoView({ behavior: 'smooth', block: 'start' });
      var foc = (i >= N) ? fin : (secs[i].querySelector('h2') || secs[i]);
      foc.setAttribute('tabindex', '-1');
      setTimeout(function () { focusNode(foc); }, 400);
    }

    function mode(tout) {
      continu = !!tout;
      saveJSON(cleMode, { mode: continu ? 'tout' : 'etapes' });
      rend();
      if (continu) return;
      var cible = (i >= N) ? fin : secs[i];
      if (cible.scrollIntoView) cible.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    each(fil.querySelectorAll('.rdcx-steps-dot'), function (b) {
      b.addEventListener('click', function () {
        if (continu) { continu = false; saveJSON(cleMode, { mode: 'etapes' }); }
        va(parseInt(b.getAttribute('data-i'), 10), true);
      });
    });
    fil.querySelector('.rdcx-steps-mode').addEventListener('click', function () { mode(true); });
    fil.querySelector('.rdcx-steps-retour').addEventListener('click', function () { mode(false); });
    nav.querySelector('.rdcx-steps-prec').addEventListener('click', function () { va(i - 1, true); });
    nav.querySelector('.rdcx-steps-suiv').addEventListener('click', function () { va(i + 1, true); });

    // Flèches gauche / droite — jamais quand le focus est dans un champ de saisie
    document.addEventListener('keydown', function (e) {
      if (continu || e.defaultPrevented) return;
      if (e.ctrlKey || e.altKey || e.metaKey || e.shiftKey) return;
      if (dansUnChamp(document.activeElement)) return;
      var droite = e.key ? (e.key === 'ArrowRight') : (e.keyCode === 39);
      var gauche = e.key ? (e.key === 'ArrowLeft') : (e.keyCode === 37);
      if (!droite && !gauche) return;
      e.preventDefault();
      va(droite ? i + 1 : i - 1, true);
    });

    // Point de contrôle terminé : l'étape qui le contient est validée quand
    // tous ses points de contrôle ont été traités.
    document.addEventListener('rdcx:checkpoint', function (e) {
      var d = (e && e.detail) || {};
      var el = byId(d.id);
      if (!el) return;
      var n = indexEtape(el);
      if (n < 0) return;
      var r = resultats[n] || (resultats[n] = {});
      r[d.id] = { s: parseInt(d.score, 10) || 0, t: parseInt(d.total, 10) || 0 };
      var attendus = secs[n].querySelectorAll('.rdcx-checkpoint').length;
      var vus = 0, s = 0, t = 0, id;
      for (id in r) {
        if (!Object.prototype.hasOwnProperty.call(r, id)) continue;
        vus++; s += r[id].s; t += r[id].t;
      }
      faits[n] = { v: (vus >= attendus || estFait(n)) ? 1 : 0, s: s, t: t, r: r };
      saveJSON(cleFait, faits);
      rendFil();
      if (i >= N) rendFin();
    });

    // Ancre explicite (menu latéral, lien direct) : elle prime sur la reprise mémorisée
    function versAncre(deplacer) {
      if (continu) return;
      var h = location.hash;
      if (!h || h.length < 2) return;
      var cible = document.getElementById(h.slice(1));
      if (!cible) return;
      var n = indexEtape(cible);
      if (n < 0 || n === i) return;
      va(n, deplacer);
    }
    window.addEventListener('hashchange', function () { versAncre(true); });

    /* ---------- premier rendu : on affiche l'étape, sans faire défiler la page ---------- */
    rend();
    versAncre(false);
    quandPret(function () {
      pret = true;
      marqueVue(i);
      rendFil();
    });
  };

  /* ----------------------------------------------------------------
     10. Sommaire collant (RDCX.sommaire)
        cfg = { titre } — un seul appel par page, aucune liste à tenir :
        les sections sont découvertes dans le DOM.

          <section class="content-section" data-sommaire-titre="L'énoncé">
            <h2 id="ch8-s1">1. L'énoncé</h2> … </section>

        Toute .content-section porteuse d'un <h2 id="…"> devient une entrée ;
        la barre s'insère juste avant la première d'entre elles.

        Différence essentielle avec RDCX.steps : RIEN N'EST MASQUÉ. Toutes les
        sections restent affichées, la page se lit d'un bout à l'autre et la
        recherche du navigateur retrouve tout. La barre se contente de conduire
        au bon endroit et de signaler où l'on se trouve.
     ---------------------------------------------------------------- */

  // Libellé d'une entrée : data-sommaire-titre (ou sa version anglaise), sinon le h2 sans sa numérotation
  function titreSommaire(sec, h2, k) {
    var t = attrLangue(sec, 'data-sommaire-titre');
    if (t && t.replace(/\s/g, '')) return t;
    var s = texteAffiche(h2).replace(/^\s*\d+\.\s*/, '').replace(/^\s+|\s+$/g, '');
    return s || ('Section ' + (k + 1));
  }

  RDCX.sommaire = function (cfg) {
    cfg = cfg || {};

    /* ---------- découverte des sections ---------- */
    var secs = [], h2s = [], titres = [];
    each(document.querySelectorAll('.content-section'), function (sec) {
      var h = sec.querySelector('h2[id]');
      if (!h || !h.id) return;
      secs.push(sec); h2s.push(h);
    });
    var N = secs.length;
    if (!N) return;                     // aucune section éligible : la fabrique ne fait rien
    if (!secs[0].parentNode) return;
    if (RDCX._sommaireFait) return;     // un seul sommaire par page
    RDCX._sommaireFait = true;

    var k;
    for (k = 0; k < N; k++) {
      titres.push(titreSommaire(secs[k], h2s[k], k));
      // marge de défilement : un saut d'ancre ne glisse plus le titre sous la barre
      h2s[k].classList.add('rdcx-sommaire-ancre');
    }

    var titre = String(cfg.titre || 'Sommaire');

    /* ---------- construction de la barre ---------- */
    var items = '';
    for (k = 0; k < N; k++) {
      items += '<li class="rdcx-sommaire-li">'
        + '<a class="rdcx-sommaire-lien" href="#' + esc(h2s[k].id) + '" data-i="' + k + '">'
        + '<span class="rdcx-sommaire-num" aria-hidden="true">' + (k + 1) + '</span>'
        + '<span class="rdcx-sommaire-txt">' + esc(titres[k]) + '</span></a></li>';
    }

    var barre = document.createElement('nav');
    barre.className = 'rdcx-sommaire';
    barre.setAttribute('aria-label', titre);
    barre.innerHTML =
        '<div class="rdcx-sommaire-bar">'
      + '  <span class="rdcx-sommaire-titre">' + rich(titre) + '</span>'
      + '  <ol class="rdcx-sommaire-liste">' + items + '</ol>'
      + '</div>';
    secs[0].parentNode.insertBefore(barre, secs[0]);

    var liste = barre.querySelector('.rdcx-sommaire-liste');
    var liens = barre.querySelectorAll('.rdcx-sommaire-lien');

    /* ---------- repères de position ---------- */
    function enteteH() {
      var e = document.querySelector('.site-header');
      return e ? e.offsetHeight : 64;
    }
    // Bas de ce qui masque le haut de la page : l'en-tête fixe du site, ou la
    // barre elle-même une fois collée dessous. La tolérance de 24 px est plus
    // large que le dégagement de 8 px visé par un clic (voir va()) : un titre
    // qui vient de se poser sous la barre compte pour atteint, sans dépendre
    // d'un arrondi sous-pixel.
    function limite() {
      var b = barre.getBoundingClientRect().bottom;
      return Math.max(enteteH(), b > 0 ? b : 0) + 24;
    }

    /* ---------- surlignage de l'entrée courante ---------- */
    var courant = -1;
    var verrou = 0;   // horodatage jusqu'auquel un défilement piloté fige le surlignage

    // La pastille active reste visible quand la liste est resserrée et défile.
    function amene(a) {
      if (!a || !liste) return;
      if (liste.scrollHeight <= liste.clientHeight + 2) return;
      var haut = a.offsetTop;
      if (haut < liste.scrollTop) liste.scrollTop = haut;
      else if (haut + a.offsetHeight > liste.scrollTop + liste.clientHeight) {
        liste.scrollTop = haut + a.offsetHeight - liste.clientHeight;
      }
    }

    function surligne(n) {
      if (n === courant) return;
      courant = n;
      each(liens, function (a, j) {
        if (j === n) { a.classList.add('is-current'); a.setAttribute('aria-current', 'true'); }
        else { a.classList.remove('is-current'); a.removeAttribute('aria-current'); }
      });
      amene(liens[n]);
    }

    function calcule() {
      if (Date.now() < verrou) return;
      var marge = limite();
      var trouve = -1, premier = -1, j, r;
      for (j = 0; j < N; j++) {
        r = secs[j].getBoundingClientRect();
        if (!r.height && !r.width) continue;   // section masquée : elle ne compte pas
        if (premier < 0) premier = j;
        if (r.top <= marge) trouve = j;
      }
      // Bas de page atteint : la dernière section éligible l'emporte, même trop
      // courte pour franchir la limite.
      var bas = (window.pageYOffset || document.documentElement.scrollTop || 0) + window.innerHeight;
      if (bas >= (document.documentElement.scrollHeight || 0) - 8) {
        for (j = N - 1; j >= 0; j--) {
          r = secs[j].getBoundingClientRect();
          if (r.height || r.width) { trouve = j; break; }
        }
      }
      if (trouve < 0) trouve = premier;
      if (trouve >= 0) surligne(trouve);
    }

    // Temporisation par MINUTERIE, jamais par requestAnimationFrame : un onglet
    // qui ne compose plus d'image (arrière-plan, fenêtre partagée) n'appelle
    // jamais rAF et le surlignage resterait figé.
    var minuteur = null;
    function planifie() {
      if (minuteur) return;
      minuteur = setTimeout(function () { minuteur = null; calcule(); }, 120);
    }

    /* ---------- navigation ---------- */
    var doux = 'scrollBehavior' in document.documentElement.style;

    // Hauteur qu'aura la barre une fois collée. On la mesure au besoin en
    // posant la classe le temps d'une lecture (aucun rendu intermédiaire n'est
    // peint) : viser la hauteur déployée ferait atterrir le titre trop bas et
    // le surlignage désignerait la section précédente.
    function hauteurCollee() {
      if (barre.classList.contains('is-stuck')) return barre.offsetHeight;
      barre.classList.add('is-stuck');
      var h = barre.offsetHeight;
      barre.classList.remove('is-stuck');
      return h;
    }

    function va(n) {
      var h = h2s[n];
      if (!h) return;
      // on vise juste sous l'en-tête et la barre : le titre reste lisible
      var y = (window.pageYOffset || document.documentElement.scrollTop || 0)
            + h.getBoundingClientRect().top - enteteH() - hauteurCollee() - 8;
      y = Math.max(0, Math.round(y));
      if (doux) window.scrollTo({ top: y, behavior: 'smooth' });
      else window.scrollTo(0, y);
      h.setAttribute('tabindex', '-1');
      try { h.focus({ preventScroll: true }); } catch (e) { focusNode(h); }
      // L'URL suit la lecture sans déclencher de « hashchange » : aucun autre
      // composant de la page (dont RDCX.steps) n'est perturbé.
      if (window.history && window.history.replaceState) {
        try { window.history.replaceState(null, '', '#' + h.id); } catch (e2) {}
      }
      verrou = Date.now() + 700;   // le temps du défilement, le surlignage suit le clic
      surligne(n);
    }

    each(liens, function (a) {
      a.addEventListener('click', function (e) {
        if (e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) return;  // ouverture en onglet
        e.preventDefault();
        va(parseInt(a.getAttribute('data-i'), 10));
      });
    });

    /* ---------- collage sous l'en-tête : même sentinelle que le fil des étapes ---------- */
    if (typeof RDCX._collant === 'function') RDCX._collant(barre, 'rdcx-sommaire-sentinel');

    window.addEventListener('scroll', planifie, { passive: true });
    window.addEventListener('resize', planifie);
    window.addEventListener('hashchange', planifie);
    window.addEventListener('load', planifie);
    calcule();
    quandPret(calcule);
  };
})();

/* =================================================================
   Fil des étapes — collage sous l'en-tête + barre de progression
   Complément autonome : n'entre pas dans RDCX.steps, se branche
   simplement sur le fil une fois qu'il a été rendu.
   Auteur : Mohamed EL AFRIT — MIT / CC BY 4.0
   ================================================================= */
(function () {
  'use strict';

  function headerPx() {
    var v = getComputedStyle(document.documentElement).getPropertyValue('--header-height');
    var n = parseFloat(v);
    return isNaN(n) ? 64 : (v.indexOf('rem') > -1 ? n * 16 : n);
  }

  // Collage sous l'en-tête : une sentinelle vide est glissée juste avant
  // l'élément et bascule la classe .is-stuck dès qu'il vient buter dessous.
  // Exposée en RDCX._collant : le sommaire (RDCX.sommaire) réutilise
  // exactement cette mécanique plutôt que d'en écrire une seconde.
  function collant(el, classeSentinel) {
    if (!el || !el.parentNode) return;

    var sentinel = document.createElement('div');
    sentinel.className = classeSentinel || 'rdcx-steps-sentinel';
    sentinel.setAttribute('aria-hidden', 'true');
    el.parentNode.insertBefore(sentinel, el);

    if (window.IntersectionObserver) {
      new IntersectionObserver(function (entries) {
        el.classList.toggle('is-stuck', !entries[0].isIntersecting);
      }, { rootMargin: '-' + (headerPx() + 1) + 'px 0px 0px 0px', threshold: 0 })
        .observe(sentinel);
    } else {                                   // repli sans IntersectionObserver
      var onScroll = function () {
        el.classList.toggle('is-stuck',
          sentinel.getBoundingClientRect().top < headerPx());
      };
      window.addEventListener('scroll', onScroll, { passive: true });
      onScroll();
    }
  }
  window.RDCX = window.RDCX || {};
  window.RDCX._collant = collant;

  function brancher(fil) {
    if (!fil || fil.getAttribute('data-collant') === '1') return;
    fil.setAttribute('data-collant', '1');

    /* --- barre de progression, en dernier enfant du fil --- */
    var line = document.createElement('div');
    line.className = 'rdcx-steps-line';
    var fill = document.createElement('span');
    fill.className = 'rdcx-steps-line-fill';
    line.appendChild(fill);
    fil.appendChild(line);

    var pos = fil.querySelector('.rdcx-steps-pos');
    function majProgression() {
      if (!pos) return;
      var t = pos.textContent || '';
      var m = t.match(/(\d+)\s*\/\s*(\d+)/);
      var pct = m ? (parseInt(m[1], 10) / parseInt(m[2], 10)) * 100
                  : (/termin/i.test(t) ? 100 : 0);
      fill.style.width = Math.max(0, Math.min(100, pct)) + '%';
    }
    majProgression();
    if (pos && window.MutationObserver) {
      new MutationObserver(majProgression)
        .observe(pos, { childList: true, characterData: true, subtree: true });
    }

    /* --- détection du collage via une sentinelle --- */
    collant(fil, 'rdcx-steps-sentinel');
  }

  function chercher() {
    var fil = document.querySelector('.rdcx-steps');
    if (fil) { brancher(fil); return true; }
    return false;
  }

  // RDCX.steps est appelé depuis la page, donc après ce script : on attend le fil.
  function init() {
    if (chercher()) return;
    if (!window.MutationObserver) return;
    var mo = new MutationObserver(function () { if (chercher()) mo.disconnect(); });
    mo.observe(document.body, { childList: true, subtree: true });
    setTimeout(function () { mo.disconnect(); }, 8000);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else { init(); }
})();

/* ============================================================
   En-tête de chapitre pliable
   ------------------------------------------------------------
   Avant le bandeau d'étapes s'empilaient l'en-tête, les objectifs, le podcast,
   les slides, l'infographie, l'encadré d'accroche et la capsule d'ouverture :
   2 171 px mesurés sur le chapitre 1, soit 2,4 écrans de préambule avant la
   première ligne de cours. On replie tout cela derrière un seul bouton.

   Le titre et sa ligne de méta restent toujours visibles : ils identifient la
   page. Replié par défaut, l'état est ensuite mémorisé par chapitre.

   Rien n'est écrit dans les pages : le repli est monté ici, pour les huit
   chapitres à la fois. Sans JavaScript, tout reste affiché — le contenu n'est
   jamais dépendant du script.
   ============================================================ */
(function () {
  'use strict';

  var CLE = 'rdc-entete-';
  /* Bornes de la zone : on s'arrête au premier bloc de contenu. Le bandeau
     d'étapes s'insère lui-même avant la première .content-section, donc hors
     de la zone, quel que soit l'ordre d'exécution des scripts.

     Les sentinelles de collage sont visées par préfixe, et non nommées une à une :
     enfermée dans un conteneur hidden, une sentinelle n'a plus de rectangle, son
     top vaut 0, et la barre qu'elle pilote se croit collée en permanence. */
  /* [data-hors-repli] permet à une page de sortir un bloc du repli : la zone
     s'arrête à lui. Utilisé par la soutenance vidéo, dont l'échéance ne doit
     pas se retrouver cachée derrière un bouton. */
  var BORNE = '.content-section, [class^="rdcx-steps"], [class^="rdcx-sommaire"], [data-hors-repli]';
  var IGNORE = { SCRIPT: 1, TEMPLATE: 1, STYLE: 1, LINK: 1, NOSCRIPT: 1 };

  /* Clé de mémorisation : le numéro pour un chapitre, le nom de fichier sinon.
     Renvoyer 0 pour toute page hors chapitre les ferait partager le même état. */
  function numero() {
    var f = location.pathname.split('/').pop() || '';
    var m = f.match(/^(\d{1,2})-/);
    return m ? parseInt(m[1], 10) : (f || 'page');
  }

  function lire(n) {
    try { return localStorage.getItem(CLE + n); } catch (e) { return null; }
  }
  function ecrire(n, v) {
    try { localStorage.setItem(CLE + n, v); } catch (e) { /* navigation privée */ }
  }

  /* Ce que la zone contient réellement : le libellé du bouton l'annonce, sinon
     replier revient à cacher des ressources sans dire lesquelles. */
  function inventaire(corps) {
    var vu = [];
    function si(sel, mot) { if (corps.querySelector(sel)) vu.push(mot); }
    si('.chapter-objectives', 'Objectifs');
    si('.podcast-section', 'Podcast');
    si('.slides-section', 'Slides');
    si('.infographie-section', 'Infographie');
    // .rdcx-voice est posée par RDCX.voice ; le conteneur statique #voix-N-N, lui,
    // est toujours là. On teste les deux pour ne pas dépendre de l'ordre des scripts.
    si('.rdcx-voice, [id^="voix-"]', "Capsule d'ouverture");
    return vu;
  }

  function monter() {
    var entete = document.querySelector('.chapter-header');
    if (!entete || entete.getAttribute('data-pliable') === '1') return false;
    var parent = entete.parentNode;
    if (!parent) return false;

    /* --- rassembler : les objectifs (dans l'en-tête) puis les frères suivants --- */
    var aReplier = [];
    var obj = entete.querySelector('.chapter-objectives');
    if (obj) aReplier.push(obj);
    var n = entete.nextElementSibling;
    while (n) {
      if (n.matches && n.matches(BORNE)) break;
      if (!IGNORE[n.tagName]) aReplier.push(n);
      n = n.nextElementSibling;
    }
    if (!aReplier.length) return false;
    entete.setAttribute('data-pliable', '1');

    /* --- le corps repliable --- */
    var corps = document.createElement('div');
    corps.className = 'rdcx-entete-corps';
    corps.id = 'rdcx-entete-corps';
    parent.insertBefore(corps, entete.nextSibling);
    for (var i = 0; i < aReplier.length; i++) corps.appendChild(aReplier[i]);

    /* --- le bouton, dernier élément de l'en-tête --- */
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'rdcx-entete-btn';
    btn.setAttribute('aria-controls', corps.id);
    var detail = inventaire(corps).join(' · ');
    btn.innerHTML =
        '<span class="rdcx-entete-chevron" aria-hidden="true">▸</span>'
      + '<span class="rdcx-entete-titre">'
      + (entete.getAttribute('data-repli-titre') || T('entete.replier'))
      + '</span>'
      + (detail ? '<span class="rdcx-entete-detail">' + detail + '</span>' : '');
    entete.appendChild(btn);

    function poser(ouvert, memoriser) {
      corps.hidden = !ouvert;
      btn.setAttribute('aria-expanded', ouvert ? 'true' : 'false');
      if (memoriser) ecrire(numero(), ouvert ? '1' : '0');
    }

    /* Replié par défaut : l'étudiant arrive sur le contenu, pas sur le préambule. */
    poser(lire(numero()) === '1', false);

    btn.addEventListener('click', function () {
      poser(corps.hidden, true);
    });

    /* Un lien pointant dans la zone repliée la rouvre, sinon il ne mène nulle part. */
    function ouvrirSiCible() {
      var h = location.hash;
      if (h && h.length > 1 && corps.hidden) {
        var c = null;
        try { c = corps.querySelector(h); } catch (e) { c = null; }
        if (c) { poser(true, true); c.scrollIntoView(); }
      }
    }
    window.addEventListener('hashchange', ouvrirSiCible);
    ouvrirSiCible();

    /* Le titre du bouton est ecrit une fois : sans cet abonnement, il resterait
       dans la langue du chargement alors que tout le reste de la page a bascule. */
    document.addEventListener('tpl:langchange', function () {
      var ti = btn.querySelector('.rdcx-entete-titre');
      if (ti) ti.textContent = entete.getAttribute('data-repli-titre')
                            || (window.T ? window.T('entete.replier') : ti.textContent);
    });

    return true;
  }

  function init() {
    if (monter()) return;
    if (!window.MutationObserver) return;
    var mo = new MutationObserver(function () { if (monter()) mo.disconnect(); });
    mo.observe(document.body, { childList: true, subtree: true });
    setTimeout(function () { mo.disconnect(); }, 8000);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else { init(); }
})();

/* -----------------------------------------------------------------
   Pour le polycopié (outils/polycopie) : chaque fabrique de contenu garde
   la configuration qu'elle a reçue, dans la langue affichée — ce que la
   page calcule (textes, .map…) et qu'un lecteur du source ne verrait pas.
   Ouverte avec ?polycopie (ou ?polycopie=en), la page l'écrit en JSON dans
   <script type="application/json" id="rdcx-donnees">, que Chrome sans
   interface rend au générateur (--dump-dom).
   ----------------------------------------------------------------- */
(function () {
  var RDCX = window.RDCX || {};
  var donnees = window.RDCX_DONNEES = {};
  ['checkpoint', 'reveal', 'spotError', 'match', 'branch', 'hotspots', 'voice'].forEach(function (sorte) {
    var fabrique = RDCX[sorte];
    if (typeof fabrique !== 'function') return;
    RDCX[sorte] = function (id, cfg) {
      donnees[id] = { sorte: sorte, config: cfg };
      return fabrique.apply(this, arguments);
    };
  });
  var demande = /[?&]polycopie(?:=([a-z]{2}))?(?:&|$)/.exec(location.search);
  if (!demande) return;
  document.addEventListener('DOMContentLoaded', function () {
    if (demande[1] && window.TPLI18N && TPLI18N.lang() !== demande[1]) TPLI18N.set(demande[1]);
  });
  window.addEventListener('load', function () {
    var s = document.createElement('script');
    s.type = 'application/json';
    s.id = 'rdcx-donnees';
    s.textContent = JSON.stringify({ langue: window.TPLI18N ? TPLI18N.lang() : '', composants: donnees })
      .replace(/</g, '\\u003c');
    document.body.appendChild(s);
  });
})();
