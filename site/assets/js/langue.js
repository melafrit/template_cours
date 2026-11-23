/* =================================================================
   langue.js · Le choix de langue du site miroir, et la reprise de la position
   Template de site de cours · Mohamed EL AFRIT (MIT / CC BY 4.0)

   Le site miroir (docs/I18N.md, partie A) : chaque page X.html de la racine,
   écrite dans la langue racine du cours, a ses jumelles <langue>/X.html (en/,
   ar/…), de même structure (même suite de blocs : titres, paragraphes,
   éléments de liste, figures, activités). Le groupe de l'en-tête,
   « FR · EN · عربي », ouvre la jumelle choisie et s'y replace sur le bloc que
   le lecteur avait sous les yeux, à la même fraction de ce bloc : on lit la
   traduction de ce qu'on lisait, sans rien rechercher. Repris du cours
   d'architecture logicielle, étendu à plusieurs langues le 21 novembre 2026.

   - Une langue n'y figure que si la page y existe (window.TPL_MIROIR, écrit
     par outils/generer_langues.py) : chaque traduction se publie lot par lot.
     Le groupe n'apparaît qu'à partir de deux langues.
   - Chaque libellé est écrit dans SA langue (« عربي » pour l'arabe, décision
     de l'auteur du 21 novembre 2026) : c'est elle que le lecteur cherche. La
     langue lue est mise en évidence, et inerte.
   - Le bloc lu : le plus petit des blocs qui coupent la ligne de lecture, juste
     sous l'en-tête fixe. Sa position (rang, fraction) passe à la page suivante
     par le stockage de session, et non par l'adresse : un lien partagé reste net.
   - Le choix est retenu : l'accueil s'ouvre dans la dernière langue choisie ; un
     lien vers une autre page, lui, garde sa langue.
   Chargé par navigation.js sur les pages d'une seule langue (data-langues) : le
   HTML des pages n'a pas à changer. outils/verifier_parite.py garde la même
   suite de blocs dans chaque langue.
   ================================================================= */
(function () {
  'use strict';

  // Les langues du gabarit, dans l'ordre du groupe ; chaque libellé dans sa propre langue.
  var LANGUES = {
    fr: { code: 'FR', lire: 'Lire cette page en français' },
    en: { code: 'EN', lire: 'Read this page in English' },
    ar: { code: 'عربي', lire: 'اقرأ هذه الصفحة بالعربية', dir: 'rtl' }
  };
  var ORDRE = ['fr', 'en', 'ar'];

  var SRC = (document.currentScript && document.currentScript.src) || '';
  var RACINE = SRC.replace(/assets\/js\/[^\/?#]+(?:[?#].*)?$/, '');
  if (!RACINE || RACINE === SRC) return;
  var MIROIR = window.TPL_MIROIR || {};
  var PAGES = MIROIR.pages || {};

  var CLE_BASCULE = 'tpl-bascule';
  var CLE_LANGUE = 'tpl-lang';          // la langue préférée, celle que lit aussi i18n.js

  // Le chemin de la page depuis la racine du site, sans son dossier de langue (« chapitres/01-….html »), et ce
  // dossier s'il y en a un : la page est alors une jumelle.
  function situer() {
    var url = location.href.split('#')[0].split('?')[0];
    if (url.indexOf(RACINE) !== 0) return null;
    var rel = url.slice(RACINE.length);
    if (rel === '' || /\/$/.test(rel)) rel += 'index.html';
    var m = /^([a-z]{2})\//.exec(rel);
    return m && LANGUES[m[1]] ? { rel: rel.slice(3), dossier: m[1] } : { rel: rel, dossier: null };
  }
  var ici = situer();
  if (!ici) return;
  var rel = ici.rel;
  var LANGUE = (document.documentElement.getAttribute('lang') || 'fr').slice(0, 2);
  // La langue de la racine : celle de la liste ; à défaut, celle de la page si elle n'est pas une jumelle.
  var RACINE_LG = MIROIR.racine || (ici.dossier ? 'fr' : LANGUE);

  // L'adresse de la page dans la langue lg, ou null si elle n'y existe pas (encore).
  function adresse(lg) {
    if (lg === RACINE_LG) return RACINE + rel;
    return (PAGES[lg] || []).indexOf(rel) >= 0 ? RACINE + lg + '/' + rel : null;
  }
  var dispo = ORDRE.filter(function (lg) { return lg === LANGUE || adresse(lg); });

  function lire(stockage, cle) { try { return window[stockage].getItem(cle); } catch (e) { return null; } }
  function ecrire(stockage, cle, v) { try { window[stockage].setItem(cle, v); } catch (e) { /* stockage indisponible */ } }
  function effacer(stockage, cle) { try { window[stockage].removeItem(cle); } catch (e) { /* idem */ } }

  // ---------------------------------------------------------------- les blocs d'une page
  // La même liste, dans le même ordre, dans chaque langue : outils/verifier_parite.py y veille.
  // La zone lue : .main-content, ou <main> sur les pages qui n'en ont pas.
  var BALISES = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'dt', 'dd', 'figure', 'table', 'pre', 'blockquote',
                 'summary', 'img', '.rdcx-voice'];
  function blocs(dans) {
    var zone = dans || document.querySelector('.main-content') || document.querySelector('main');
    return zone ? Array.prototype.slice.call(zone.querySelectorAll(BALISES.join(','))) : [];
  }
  // Un bloc rangé dans un élément [data-jumeau] (une entrée du glossaire, que chaque langue trie à sa façon) se
  // retrouve par cette clé commune aux langues, puis par son rang dans l'élément ; les autres, par leur rang.
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
  var prefere = lire('localStorage', CLE_LANGUE);
  if (!ici.dossier && !arrivee && rel === 'index.html' && prefere && prefere !== LANGUE && adresse(prefere)) {
    location.replace(adresse(prefere));
    return;
  }

  // ---------------------------------------------------------------- le groupe de langues
  function aller(lg) {
    var cible = adresse(lg), p = reperer();
    p.vers = new URL(cible, location.href).pathname;
    p.y = window.scrollY;
    p.t = Date.now();
    ecrire('sessionStorage', CLE_BASCULE, JSON.stringify(p));
    ecrire('localStorage', CLE_LANGUE, lg);
    location.href = cible;
  }

  if (dispo.length < 2) return;
  function poser() {
    var place = document.querySelector('.header-right');
    if (!place || place.querySelector('.langue-choix')) return;
    var groupe = document.createElement('div');
    groupe.className = 'langue-choix';
    groupe.setAttribute('role', 'group');
    groupe.setAttribute('aria-label', window.T ? window.T('langue.groupe') : 'Langue');
    dispo.forEach(function (lg) {
      var L = LANGUES[lg], el;
      if (lg === LANGUE) {
        el = document.createElement('span');
        el.className = 'langue-toggle langue-actuelle';
        el.setAttribute('aria-current', 'true');
      } else {
        el = document.createElement('button');
        el.type = 'button';
        el.className = 'langue-toggle';
        el.setAttribute('aria-label', L.lire);
        el.title = L.lire;
        el.addEventListener('click', function () { aller(lg); });
      }
      el.textContent = L.code;
      el.setAttribute('lang', lg);
      if (L.dir) el.setAttribute('dir', L.dir);
      groupe.appendChild(el);
    });
    place.insertBefore(groupe, place.querySelector('.theme-toggle'));
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', poser);
  else poser();
})();
