/* =================================================================
   filiere.js — La bascule de filière d'un cours commun à deux filières
   Template de site de cours — Mohamed EL AFRIT (MIT / CC BY 4.0)

   Repris du cours EADL et rendu générique (décision de l'auteur du
   21 novembre 2026) : les filières se déclarent dans course-data.js
   (COURSE.filieres : id, code, palette, nom, court), jamais ici.

   - Le contenu propre à une filière porte la classe only-<id> ; filieres.css,
     généré par outils/generer_filieres.py, masque celui des autres quand
     <html> porte data-filiere="<id>". Sans choix, les deux versions
     s'affichent, étiquetées : c'est la vue du formateur en groupe mixte.
   - Trois lignes en tête de chaque page posent la filière mémorisée avant
     l'affichage (sinon la page clignote) ; un paramètre d'URL l'impose
     (?filiere=eris), pour un lien envoyé à une filière.
   - L'accent de couleur suit la filière : sa palette (palettes.css) remplace
     celle du cours, et revient quand on désélectionne.
   - La bascule va dans l'en-tête ; sous 480 px, en tête du menu ☰ (l'en-tête
     d'un chapitre est déjà plein). Le bandeau « Quelle est votre filière ? »
     reste dans la page tant qu'aucune n'est choisie. Recliquer sur la filière
     active revient aux deux versions.
   - Le choix se retient pour ce cours (clé propre à son adresse : deux cours
     du même site ne se le prêtent pas).
   - API : TPLFILIERE.filiere() · .choisir(id) · .selon({ eadl: …, eris: … }, défaut)
     · .liste() ; évènement « tpl:filiere ».
   Chargé par navigation.js quand le cours déclare au moins deux filières.
   ================================================================= */
(function () {
  'use strict';

  var root = document.documentElement;
  var LISTE = ((window.COURSE || {}).filieres || []).filter(function (f) { return f && f.id; });
  if (LISTE.length < 2) { root.removeAttribute('data-filiere'); return; }

  // La palette du cours, gardée par le script de tête avant qu'il ne pose celle d'une filière.
  var ACCENT_COURS = root.getAttribute('data-accent-cours') || root.getAttribute('data-accent') || '';
  var RACINE = '/';
  try { RACINE = new URL(window.TPL_RACINE || './', location.href).pathname; } catch (e) { /* adresse illisible */ }
  var CLE = 'tpl-filiere|' + RACINE;

  function lg() { return (window.TPLI18N && TPLI18N.lang && TPLI18N.lang()) || 'fr'; }
  function L(x) { return (x && typeof x === 'object') ? (x[lg()] || x.fr || x.en || '') : (x || ''); }
  function esc(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;'); }
  function t(cle, defaut) { return window.T ? window.T(cle) : defaut; }
  function trouver(id) { return LISTE.filter(function (f) { return f.id === id; })[0] || null; }
  function filiere() { var id = root.getAttribute('data-filiere'); return trouver(id) ? id : ''; }
  function ecrire(v) { try { if (v) localStorage.setItem(CLE, v); else localStorage.removeItem(CLE); } catch (e) { /* stockage indisponible */ } }

  function appliquer(id, memoriser) {
    var f = trouver(id);
    if (f) {
      root.setAttribute('data-filiere', f.id);
      if (f.palette) root.setAttribute('data-accent', f.palette);
    } else {
      root.removeAttribute('data-filiere');
      if (ACCENT_COURS) root.setAttribute('data-accent', ACCENT_COURS);
    }
    if (memoriser) ecrire(f ? f.id + '|' + (f.palette || '') : '');
    // Une capsule de l'autre filière ne doit pas continuer à parler.
    LISTE.forEach(function (g) {
      Array.prototype.forEach.call(document.querySelectorAll('.only-' + g.id + ' audio'), function (a) {
        if (!a.paused && !a.getClientRects().length) a.pause();
      });
    });
    synchroniser();
    document.dispatchEvent(new CustomEvent('tpl:filiere', { detail: { filiere: filiere() } }));
  }

  function synchroniser() {
    var f = filiere();
    Array.prototype.forEach.call(document.querySelectorAll('[data-choix-filiere]'), function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-choix-filiere') === f ? 'true' : 'false');
    });
    var bandeau = document.getElementById('bandeau-filiere');
    if (bandeau) bandeau.hidden = !!f;
  }

  function boutons(avecNom) {
    return LISTE.map(function (f) {
      var titre = L(f.nom) + (f.rncp ? ' (RNCP ' + f.rncp + ')' : '');
      return '<button type="button" data-choix-filiere="' + esc(f.id) + '" aria-pressed="false" title="' + esc(titre) + '">'
        + (avecNom ? '<span>' + esc(f.code) + '</span><small>' + esc(L(f.court)) + '</small>' : esc(f.code))
        + '</button>';
    }).join('');
  }

  function brancher(zone, retour) {
    Array.prototype.forEach.call(zone.querySelectorAll('[data-choix-filiere]'), function (b) {
      b.addEventListener('click', function () {
        var id = b.getAttribute('data-choix-filiere');
        appliquer(retour && filiere() === id ? '' : id, true);
      });
    });
  }

  // -- La bascule de l'en-tête, et sa copie en tête du menu ☰ pour le téléphone
  function dessinerBascules() {
    var place = document.querySelector('.site-header .header-right');
    if (place && !place.querySelector('.filiere-choix')) {
      var g = document.createElement('div');
      g.className = 'filiere-choix';
      g.setAttribute('role', 'group');
      g.setAttribute('aria-label', t('filiere.groupe', 'Votre filière'));
      g.innerHTML = boutons(false);
      place.insertBefore(g, place.querySelector('.langue-choix') || place.querySelector('.theme-toggle'));
      brancher(g, true);
    }
    var menu = document.querySelector('.sidebar-content');
    if (menu && !menu.querySelector('.filiere-menu')) {
      var m = document.createElement('div');
      m.className = 'filiere-menu';
      m.setAttribute('role', 'group');
      m.setAttribute('aria-label', t('filiere.groupe', 'Votre filière'));
      m.innerHTML = '<div class="filiere-menu-titre">' + esc(t('filiere.groupe', 'Votre filière')) + '</div>'
        + '<div class="filiere-menu-choix">' + boutons(false) + '</div>';
      menu.insertBefore(m, menu.firstChild);
      brancher(m, true);
    }
  }

  // -- Le bandeau « Quelle est votre filière ? », sous le titre de la page, tant qu'aucune n'est choisie
  function dessinerBandeau() {
    if (document.getElementById('bandeau-filiere')) return;
    // Sous l'en-tête de la page, pas en tête de <main> : <main> CONTIENT l'en-tête (leçon du cours EADL).
    var cible = document.querySelector('.landing-header') || document.querySelector('.chapter-header');
    var main = document.querySelector('main');
    if (!cible && !main) return;
    var b = document.createElement('div');
    b.id = 'bandeau-filiere';
    b.className = 'bandeau-filiere';
    b.innerHTML = '<div class="bandeau-filiere-texte"><strong>' + esc(t('filiere.question', 'Quelle est votre filière ?'))
      + '</strong> ' + esc(t('filiere.explication', '')) + '</div>'
      + '<div class="bandeau-filiere-choix">' + boutons(true) + '</div>';
    if (cible) cible.parentNode.insertBefore(b, cible.nextSibling);
    else main.insertBefore(b, main.firstChild);
    brancher(b, false);
  }

  window.TPLFILIERE = {
    filiere: filiere,
    choisir: function (id) { appliquer(id, true); },
    liste: function () { return LISTE.slice(); },
    // Une valeur selon la filière : TPLFILIERE.selon({ eadl: 'a', eris: 'b' }, défaut)
    selon: function (valeurs, defaut) {
      var f = filiere();
      return f && valeurs && valeurs[f] !== undefined ? valeurs[f] : defaut;
    }
  };

  function demarrer() {
    // Une filière posée par le script de tête mais inconnue du cours (un ancien lien, une coquille) s'oublie.
    if (root.getAttribute('data-filiere') && !filiere()) appliquer('', false);
    else if (filiere()) appliquer(filiere(), new URLSearchParams(location.search).get('filiere') === filiere());
    dessinerBascules();
    dessinerBandeau();
    synchroniser();
  }

  // Une page en blocs data-tr change de langue sur place : les libellés suivent.
  document.addEventListener('tpl:langchange', function () {
    Array.prototype.forEach.call(document.querySelectorAll('.filiere-choix, .filiere-menu, #bandeau-filiere'),
      function (el) { el.parentNode.removeChild(el); });
    dessinerBascules();
    dessinerBandeau();
    synchroniser();
  });

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', demarrer);
  else demarrer();
})();
