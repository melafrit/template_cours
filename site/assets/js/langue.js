/* =================================================================
   langue.js — Le bouton FR / EN du site miroir, et la reprise de la position
   Template de site de cours — Mohamed EL AFRIT (MIT / CC BY 4.0)

   Le site miroir (docs/I18N.md, partie A) : chaque page française X.html a sa
   jumelle anglaise en/X.html, de même structure (même suite de blocs : titres,
   paragraphes, éléments de liste, figures, activités). Le bouton, en haut à
   droite, ouvre la jumelle et s'y replace sur le bloc que le lecteur avait sous
   les yeux, à la même fraction de ce bloc : on lit la traduction de ce qu'on
   lisait, sans rien rechercher. Repris du cours d'architecture logicielle.

   - Le bouton n'apparaît que si la jumelle existe (window.TPL_LANGUES, écrit
     par outils/generer_langues.py) : la version anglaise se publie lot par lot.
   - Le bloc lu : le plus petit des blocs qui coupent la ligne de lecture, juste
     sous l'en-tête fixe. Sa position (rang, fraction) passe à la page suivante
     par le stockage de session, et non par l'adresse : un lien partagé reste net.
   - Le choix est retenu : l'accueil s'ouvre dans la dernière langue choisie ; un
     lien vers une autre page, lui, garde sa langue.
   Chargé par navigation.js sur les pages d'une seule langue (data-langues) : le
   HTML des pages n'a pas à changer. outils/verifier_parite.py garde la même
   suite de blocs des deux côtés.
   ================================================================= */
(function () {
  'use strict';

  var EN = /^en/i.test(document.documentElement.getAttribute('lang') || '');
  var SRC = (document.currentScript && document.currentScript.src) || '';
  var RACINE = SRC.replace(/assets\/js\/[^\/?#]+(?:[?#].*)?$/, '');
  if (!RACINE || RACINE === SRC) return;

  var CLE_BASCULE = 'tpl-bascule';
  var CLE_LANGUE = 'tpl-lang';          // la langue préférée, celle que lit aussi i18n.js

  // Le chemin de la page depuis la racine du site, sans le préfixe de langue : « chapitres/01-….html ».
  function cheminRelatif() {
    var url = location.href.split('#')[0].split('?')[0];
    if (url.indexOf(RACINE) !== 0) return null;
    var rel = url.slice(RACINE.length);
    if (rel === '' || /\/$/.test(rel)) rel += 'index.html';
    return rel.indexOf('en/') === 0 ? rel.slice(3) : rel;
  }
  var rel = cheminRelatif();
  if (rel === null) return;
  var dispo = window.TPL_LANGUES || [];
  var jumelle = EN ? RACINE + rel : (dispo.indexOf(rel) >= 0 ? RACINE + 'en/' + rel : null);

  function lire(stockage, cle) { try { return window[stockage].getItem(cle); } catch (e) { return null; } }
  function ecrire(stockage, cle, v) { try { window[stockage].setItem(cle, v); } catch (e) { /* stockage indisponible */ } }
  function effacer(stockage, cle) { try { window[stockage].removeItem(cle); } catch (e) { /* idem */ } }

  // ---------------------------------------------------------------- les blocs d'une page
  // La même liste, dans le même ordre, en français et en anglais : outils/verifier_parite.py y veille.
  // La zone lue : .main-content, ou <main> sur les pages qui n'en ont pas.
  var BALISES = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'dt', 'dd', 'figure', 'table', 'pre', 'blockquote',
                 'summary', 'img', '.rdcx-voice'];
  function blocs(dans) {
    var zone = dans || document.querySelector('.main-content') || document.querySelector('main');
    return zone ? Array.prototype.slice.call(zone.querySelectorAll(BALISES.join(','))) : [];
  }
  // Un bloc rangé dans un élément [data-jumeau] (une entrée du glossaire, que chaque langue trie à sa façon) se
  // retrouve par cette clé commune aux deux langues, puis par son rang dans l'élément ; les autres, par leur rang.
  function jumeau(el) { return el.closest('[data-jumeau]'); }
  // Le contenu d'un <details> fermé n'est pas affiché, mais certains navigateurs lui donnent quand même des
  // dimensions : seul son <summary> compte alors.
  function visible(el) {
    for (var d = el.closest('details'); d; d = d.parentElement && d.parentElement.closest('details')) {
      var s = el.closest('summary');
      if (!d.open && !(s && s.parentElement === d)) return false;
    }
    return el.getClientRects().length > 0;
  }
  function ligneDeLecture() {
    var h = document.querySelector('.site-header');
    return (h ? h.getBoundingClientRect().bottom : 0) + 12;
  }
  // Les sections glissent en apparaissant (animations.js) : à la mesure, on les veut à leur place.
  function toutAfficher() {
    Array.prototype.forEach.call(document.querySelectorAll('.reveal'), function (el) { el.classList.add('visible'); });
  }

  function reperer() {
    toutAfficher();
    var ligne = ligneDeLecture(), liste = blocs(), lu = -1, hauteur = Infinity, suivant = -1;
    for (var i = 0; i < liste.length; i++) {
      if (!visible(liste[i])) continue;
      var r = liste[i].getBoundingClientRect();
      if (r.top <= ligne && r.bottom > ligne) {
        if (r.height < hauteur) { lu = i; hauteur = r.height; }      // le plus petit bloc : le plus précis
      } else if (suivant < 0 && r.top > ligne) {
        suivant = i;
      }
    }
    var k = lu >= 0 ? lu : suivant, f = 0;
    if (k < 0) return { k: -1, f: 0 };
    if (lu >= 0) {
      var b = liste[lu].getBoundingClientRect();
      f = (ligne - b.top) / Math.max(1, b.height);
    }
    var p = { k: k, f: f }, j = jumeau(liste[k]);
    if (j) { p.cle = j.getAttribute('data-jumeau'); p.balise = j.tagName; p.r = blocs(j).indexOf(liste[k]); }
    return p;
  }

  function defiler(y) {
    var html = document.documentElement, avant = html.style.scrollBehavior;
    html.style.scrollBehavior = 'auto';                     // un saut, pas un défilement doux
    window.scrollTo(0, Math.max(0, y));
    html.style.scrollBehavior = avant;
  }

  function replacer(p) {
    toutAfficher();
    var el = null;
    if (p.cle) {
      var j = null;
      Array.prototype.some.call(document.querySelectorAll('[data-jumeau]'), function (x) {   // même clé, même balise :
        return x.getAttribute('data-jumeau') === p.cle && (!p.balise || x.tagName === p.balise) && (j = x);  // l'article
      });                                                                                   // ou sa ligne d'index
      if (j) { var dedans = blocs(j); el = dedans[p.r] || dedans[0] || j; }
    }
    el = el || blocs()[p.k];
    if (!el) { defiler(p.y || 0); return; }
    // On ouvre les <details> qui cachent le bloc ; le <summary> d'un <details> replié le laisse replié.
    var s = el.closest('summary'), haut = s ? s.parentElement.parentElement : null;
    var d = s ? haut && haut.closest('details') : el.closest('details');
    for (; d; d = d.parentElement && d.parentElement.closest('details')) d.open = true;
    if (!visible(el)) return;
    var r = el.getBoundingClientRect();
    defiler(window.scrollY + r.top + p.f * r.height - ligneDeLecture());
  }

  // ---------------------------------------------------------------- l'arrivée après une bascule
  var arrivee = null;
  try { arrivee = JSON.parse(lire('sessionStorage', CLE_BASCULE) || 'null'); } catch (e) { arrivee = null; }
  if (arrivee && arrivee.vers === location.pathname && Date.now() - arrivee.t < 20000) {
    effacer('sessionStorage', CLE_BASCULE);
    var refaire = function () { replacer(arrivee); };
    // après le dessin des activités, puis après les images et les polices, qui déplacent encore la mise en page
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', refaire);
    else refaire();
    if (document.readyState === 'complete') setTimeout(refaire, 350);
    else window.addEventListener('load', function () { refaire(); setTimeout(refaire, 350); });
  } else {
    arrivee = null;
  }

  // ---------------------------------------------------------------- le choix retenu
  if (!EN && !arrivee && rel === 'index.html' && jumelle && lire('localStorage', CLE_LANGUE) === 'en') {
    location.replace(jumelle);
    return;
  }

  // ---------------------------------------------------------------- le bouton
  if (!jumelle) return;
  function poser() {
    var place = document.querySelector('.header-right');
    if (!place || place.querySelector('.langue-toggle')) return;
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'langue-toggle';
    b.textContent = EN ? 'FR' : 'EN';
    b.setAttribute('lang', EN ? 'fr' : 'en');
    // Le libellé est dans la langue de destination : c'est elle que le lecteur cherche.
    var libelle = EN ? 'Lire cette page en français' : 'Read this page in English';
    b.setAttribute('aria-label', libelle);
    b.title = libelle;
    place.insertBefore(b, place.querySelector('.theme-toggle'));
    b.addEventListener('click', function () {
      var p = reperer();
      p.vers = new URL(jumelle, location.href).pathname;
      p.y = window.scrollY;
      p.t = Date.now();
      ecrire('sessionStorage', CLE_BASCULE, JSON.stringify(p));
      ecrire('localStorage', CLE_LANGUE, EN ? 'fr' : 'en');
      location.href = jumelle;
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', poser);
  else poser();
})();
