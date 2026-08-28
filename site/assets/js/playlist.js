/* =================================================================
   playlist.js — panneau de lecture, à droite de la page
   Cours "Réglementation des données et conformité"
   Auteur : Mohamed EL AFRIT — CC BY-NC-SA 4.0

   Rassemble les pistes audio de tous les chapitres. Celui qu'on lit est
   déplié ; les autres restent pliés, mais leurs pistes se jouent sans
   quitter la page — un fichier audio n'a pas besoin de son chapitre.

   Lancée depuis le panneau, la lecture enchaîne toute seule sur la piste
   suivante, jusqu'au bout du chapitre. Elle s'arrête là : poursuivre dans
   le chapitre voisin ferait entendre un cours que l'on n'est pas en train
   de lire.

   S'appuie sur le lecteur persistant de media.js (window.RDC_LECTEUR) :
   une seule barre, un seul son à la fois, ici comme ailleurs.
   L'index des pistes vient de playlist-data.js, fichier généré.
   ================================================================= */
(function () {
  'use strict';

  var DONNEES = window.RDC_PLAYLIST;
  if (!DONNEES) return;

  var ICONES = { podcast: '🎙️', voix: '🎧', ouverture: '▸' };
  var CLE_OUVERT = 'rdc-playlist-ouverte';

  function chapitreCourant() {
    var f = location.pathname.split('/').pop() || '';
    var m = f.match(/^(\d{1,2})-/);
    if (m) return String(parseInt(m[1], 10));
    // Une page hors chapitre se reconnaît à sa propre entrée « page ».
    var cles = Object.keys(DONNEES);
    for (var i = 0; i < cles.length; i++) {
      if ((DONNEES[cles[i]].page || '').split('/').pop() === f) return cles[i];
    }
    return null;
  }

  // Rang d'affichage : « ordre » s'il est déclaré, le numéro de chapitre sinon.
  // Sans lui, une clé non numérique se comparerait en NaN et sortirait n'importe où.
  function rang(n) {
    var o = DONNEES[n] && DONNEES[n].ordre;
    return o == null ? Number(n) : o;
  }

  function base() {
    // Les chemins de l'index partent de la racine du site ; les pages de
    // chapitre sont un cran plus bas.
    return /\/chapitres\//.test(location.pathname) ? '../' : '';
  }

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  /* ---------------------------------------------------------------
     Construction du panneau
     --------------------------------------------------------------- */
  function construire() {
    var courant = chapitreCourant();
    var numeros = Object.keys(DONNEES).sort(function (a, b) { return rang(a) - rang(b); });

    var total = 0, dispo = 0;
    numeros.forEach(function (n) {
      DONNEES[n].pistes.forEach(function (p) { total++; if (p.present) dispo++; });
    });

    var html = ''
      + '<div class="pl-tete">'
      + '  <span class="pl-titre">' + T('playlist.titre') + '</span>'
      + '  <span class="pl-compte">' + dispo + ' / ' + total + '</span>'
      + '  <button type="button" class="pl-fermer" aria-label="' + T('playlist.fermer') + '">✕</button>'
      + '</div>'
      + '<div class="pl-corps">';

    numeros.forEach(function (n) {
      var ch = DONNEES[n];
      var ouvert = (n === courant);
      var pretes = ch.pistes.filter(function (p) { return p.present; }).length;
      html += ''
        + '<section class="pl-chapitre' + (ouvert ? ' est-ouvert' : '') + '" data-ch="' + n + '">'
        + '  <button type="button" class="pl-ch-tete" aria-expanded="' + (ouvert ? 'true' : 'false') + '">'
        + '    <span class="pl-ch-chevron" aria-hidden="true">▸</span>'
        + '    <span class="pl-ch-num">' + esc(DONNEES[n].num == null ? n : DONNEES[n].num) + '</span>'
        + '    <span class="pl-ch-titre">' + esc(ch.titre) + '</span>'
        + '    <span class="pl-ch-compte">' + pretes + '</span>'
        + '  </button>'
        + '  <ul class="pl-pistes"' + (ouvert ? '' : ' hidden') + '>';
      ch.pistes.forEach(function (p, i) {
        var absente = !p.present;
        html += ''
          + '<li class="pl-piste' + (absente ? ' est-absente' : '') + '"'
          + ' data-ch="' + n + '" data-i="' + i + '">'
          + '  <button type="button" class="pl-jouer"' + (absente ? ' disabled' : '')
          + '     aria-label="' + esc(absente ? T('playlist.aEnregistrer') : 'Lire : ' + p.titre) + '">'
          + (absente ? '·' : '▶') + '</button>'
          + '  <span class="pl-type" aria-hidden="true">' + (ICONES[p.type] || '') + '</span>'
          + '  <span class="pl-piste-titre">' + esc(p.titre) + '</span>'
          + '  <span class="pl-duree">' + esc(p.duree || '') + '</span>'
          + '</li>';
      });
      html += '  </ul></section>';
    });

    html += '</div>';

    var panneau = document.createElement('aside');
    panneau.className = 'rdc-playlist';
    panneau.setAttribute('aria-label', '' + T('playlist.titre') + ' du cours');
    panneau.innerHTML = html;
    document.body.appendChild(panneau);
    return panneau;
  }

  /* ---------------------------------------------------------------
     Lecture
     --------------------------------------------------------------- */
  function Lecture(panneau) {
    // Audio de secours, pour les pistes qui n'appartiennent pas à cette page.
    var externe = document.createElement('audio');
    externe.preload = 'none';
    externe.className = 'pl-audio';
    document.body.appendChild(externe);
    if (window.RDC_LECTEUR && window.RDC_LECTEUR.attacher) {
      window.RDC_LECTEUR.attacher(externe, function () { return externe.dataset.titre || 'Audio'; });
    }

    var encours = null;          // {ch, i, audio}
    var auto = false;            // vrai si la lecture vient du panneau

    function audioDeLaPage(piste) {
      if (!piste.ancre) return null;
      var boite = document.getElementById(piste.ancre);
      return boite ? boite.querySelector('audio') : null;
    }

    function marquer() {
      panneau.querySelectorAll('.pl-piste.est-active').forEach(function (li) {
        li.classList.remove('est-active');
        var b = li.querySelector('.pl-jouer');
        if (b) b.textContent = '▶';
      });
      if (!encours) return;
      var sel = '.pl-piste[data-ch="' + encours.ch + '"][data-i="' + encours.i + '"]';
      var li = panneau.querySelector(sel);
      if (li) {
        li.classList.add('est-active');
        var b = li.querySelector('.pl-jouer');
        if (b) b.textContent = encours.audio && !encours.audio.paused ? '⏸' : '▶';
        // garder la piste en vue quand l'enchaînement descend la liste
        var corps = panneau.querySelector('.pl-corps');
        var r = li.getBoundingClientRect(), rc = corps.getBoundingClientRect();
        if (r.top < rc.top || r.bottom > rc.bottom) {
          li.scrollIntoView({ block: 'nearest' });
        }
      }
    }

    function suivante(ch, i) {
      var pistes = DONNEES[ch].pistes;
      for (var k = i + 1; k < pistes.length; k++) {
        if (pistes[k].present) return k;
      }
      return -1;                 // fin du chapitre : on s'arrête là
    }

    function jouer(ch, i, parAuto) {
      var piste = DONNEES[ch].pistes[i];
      if (!piste || !piste.present) return;

      if (encours && encours.audio && encours.audio !== audioDeLaPage(piste)) {
        try { encours.audio.pause(); } catch (e) { /* rien */ }
      }

      var a = audioDeLaPage(piste);
      if (!a) {
        a = externe;
        var url = base() + piste.src;
        if (externe.getAttribute('src') !== url) {
          externe.setAttribute('src', url);
          externe.load();
        }
        externe.dataset.titre = (ICONES[piste.type] || '') + ' ' + piste.titre;
      }
      encours = { ch: ch, i: i, audio: a };
      auto = true;
      brancherFin(a);
      var p = a.play();
      if (p && p.catch) p.catch(function () { /* geste utilisateur requis */ });
      marquer();
      if (!parAuto) fermerSiEtroit();
    }

    var branches = [];
    function brancherFin(a) {
      if (branches.indexOf(a) > -1) return;
      branches.push(a);
      a.addEventListener('ended', function () {
        if (!auto || !encours || encours.audio !== a) return;
        var k = suivante(encours.ch, encours.i);
        if (k < 0) { auto = false; encours = null; marquer(); return; }
        jouer(encours.ch, k, true);
      });
      a.addEventListener('play', marquer);
      a.addEventListener('pause', marquer);
    }

    // Une lecture lancée ailleurs (bouton de la page, barre du lecteur) coupe
    // l'enchaînement : l'étudiant a repris la main.
    document.addEventListener('play', function (e) {
      if (!encours || e.target !== encours.audio) { auto = false; }
    }, true);

    return { jouer: jouer, marquer: marquer,
             etat: function () { return encours; },
             basculer: function (ch, i) {
               if (encours && encours.ch === ch && encours.i === i && encours.audio) {
                 if (encours.audio.paused) { encours.audio.play(); } else { encours.audio.pause(); }
                 marquer();
                 return;
               }
               jouer(ch, i, false);
             } };
  }

  /* ---------------------------------------------------------------
     Ouverture / fermeture (tiroir sous 1400 px)
     --------------------------------------------------------------- */
  var etroit = window.matchMedia('(max-width: 1399px)');

  function fermerSiEtroit() {
    if (etroit.matches) basculerPanneau(false);
  }

  var panneauRef = null, voileRef = null, boutonRef = null;

  function basculerPanneau(ouvrir) {
    if (!panneauRef) return;
    var etat = (ouvrir === undefined) ? !panneauRef.classList.contains('est-ouverte') : ouvrir;
    panneauRef.classList.toggle('est-ouverte', etat);
    // Le corps porte l'état : au-delà de 1400 px, c'est lui qui réserve la
    // colonne de droite et décale la barre de lecture.
    document.body.classList.toggle('avec-playlist', etat);
    if (voileRef) voileRef.classList.toggle('show', etat && etroit.matches);
    if (boutonRef) boutonRef.setAttribute('aria-expanded', etat ? 'true' : 'false');
    try { localStorage.setItem(CLE_OUVERT, etat ? '1' : '0'); } catch (e) { /* rien */ }
  }

  function poserBouton() {
    var hote = document.querySelector('.header-right') || document.querySelector('.site-header');
    if (!hote) return null;
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'playlist-toggle';
    b.setAttribute('aria-label', T('playlist.basculer'));
    b.setAttribute('aria-expanded', 'false');
    b.innerHTML = '<span aria-hidden="true">♪</span>';
    b.addEventListener('click', function () { basculerPanneau(); });
    hote.appendChild(b);
    return b;
  }

  /* ---------------------------------------------------------------
     Mise en route
     --------------------------------------------------------------- */
  function init() {
    if (document.querySelector('.rdc-playlist')) return;
    panneauRef = construire();
    boutonRef = poserBouton();

    voileRef = document.querySelector('.playlist-overlay');
    if (!voileRef) {
      voileRef = document.createElement('div');
      voileRef.className = 'playlist-overlay';
      document.body.appendChild(voileRef);
    }
    voileRef.addEventListener('click', function () { basculerPanneau(false); });

    var lecture = Lecture(panneauRef);

    panneauRef.querySelector('.pl-fermer')
      .addEventListener('click', function () { basculerPanneau(false); });

    panneauRef.addEventListener('click', function (e) {
      var tete = e.target.closest('.pl-ch-tete');
      if (tete) {
        var sec = tete.closest('.pl-chapitre');
        var liste = sec.querySelector('.pl-pistes');
        var ouvert = liste.hidden;
        liste.hidden = !ouvert;
        sec.classList.toggle('est-ouvert', ouvert);
        tete.setAttribute('aria-expanded', ouvert ? 'true' : 'false');
        return;
      }
      var bouton = e.target.closest('.pl-jouer');
      if (bouton && !bouton.disabled) {
        var li = bouton.closest('.pl-piste');
        lecture.basculer(li.dataset.ch, parseInt(li.dataset.i, 10));
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && etroit.matches) basculerPanneau(false);
    });

    // Au-dessus de 1400 px, le panneau occupe sa colonne : on rouvre comme
    // l'étudiant l'avait laissé. En dessous c'est un tiroir posé sur la page,
    // avec son voile : le rouvrir au chargement ferait arriver sur un écran
    // assombri qu'on n'a pas demandé. Il démarre donc toujours fermé.
    var memo = null;
    try { memo = localStorage.getItem(CLE_OUVERT); } catch (e) { /* rien */ }
    basculerPanneau(etroit.matches ? false : memo !== '0');

    if (etroit.addEventListener) {
      etroit.addEventListener('change', function () {
        if (voileRef) voileRef.classList.toggle(
          'show', etroit.matches && panneauRef.classList.contains('est-ouverte'));
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else { init(); }
})();
