/* =================================================================
   i18n.js — Bascule de langue bilingue FR/EN (cœur du template)
   Template de site de cours — Mohamed EL AFRIT (MIT / CC BY 4.0)

   CONTRAT (à suivre par les pages et les moteurs) :

   1) CONTENU rédigé (HTML) — blocs jumelés, masqués en CSS :
        <h1 data-tr="fr">Bonjour</h1><h1 data-tr="en">Hello</h1>
        <span data-tr="fr">…</span><span data-tr="en">…</span>
      (le CSS de components.css masque la langue inactive)

   2) ATTRIBUTS traduisibles (aria-label, title, alt, placeholder) :
        <button data-i18n-aria-fr="Lire" data-i18n-aria-en="Play" aria-label="Lire">
        <img  data-i18n-alt-fr="…" data-i18n-alt-en="…" alt="…">
      i18n.js échange l'attribut au changement de langue.

   3) UI générée en JS (nav, QCM, lecteurs…) — chaque moteur définit ses
      libellés et écoute l'évènement de changement de langue :
        var S = { fr:{ play:'Lire' }, en:{ play:'Play' } };
        function t(k){ return (S[TPLI18N.lang()]||S.fr)[k] || S.fr[k]; }
        document.addEventListener('tpl:langchange', reRender);

   API : TPLI18N.lang() · TPLI18N.set('en') · TPLI18N.toggle()
   ================================================================= */
(function () {
  var KEY = 'tpl-lang';
  var DEFAULT = (document.documentElement.getAttribute('lang') || 'fr').slice(0, 2);
  var SUPPORTED = ['fr', 'en'];

  function saved() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function store(l) { try { localStorage.setItem(KEY, l); } catch (e) {} }

  var current = (function () {
    var s = saved();
    if (s && SUPPORTED.indexOf(s) >= 0) return s;
    // sinon : langue du navigateur si supportée, sinon défaut du document
    var nav = (navigator.language || navigator.userLanguage || DEFAULT).slice(0, 2);
    return SUPPORTED.indexOf(nav) >= 0 ? nav : (SUPPORTED.indexOf(DEFAULT) >= 0 ? DEFAULT : 'fr');
  })();

  function applyAttributes(root) {
    var l = current;
    var els = (root || document).querySelectorAll('[data-i18n-aria-fr],[data-i18n-title-fr],[data-i18n-alt-fr],[data-i18n-ph-fr]');
    els.forEach(function (el) {
      var a;
      if ((a = el.getAttribute('data-i18n-aria-' + l)) != null) el.setAttribute('aria-label', a);
      if ((a = el.getAttribute('data-i18n-title-' + l)) != null) el.setAttribute('title', a);
      if ((a = el.getAttribute('data-i18n-alt-' + l)) != null) el.setAttribute('alt', a);
      if ((a = el.getAttribute('data-i18n-ph-' + l)) != null) el.setAttribute('placeholder', a);
    });
  }

  function apply() {
    var root = document.documentElement;
    root.setAttribute('data-lang', current);
    root.setAttribute('lang', current);
    applyAttributes(document);
    document.querySelectorAll('.lang-toggle').forEach(function (b) {
      // le bouton affiche la langue vers laquelle on bascule
      var other = current === 'fr' ? 'EN' : 'FR';
      b.textContent = '🌐 ' + other;
      b.setAttribute('aria-label', current === 'fr' ? 'Switch to English' : 'Passer en français');
      b.setAttribute('aria-pressed', current === 'en' ? 'true' : 'false');
    });
  }

  var TPLI18N = {
    lang: function () { return current; },
    supported: function () { return SUPPORTED.slice(); },
    set: function (l) {
      l = (l || '').slice(0, 2);
      if (SUPPORTED.indexOf(l) < 0 || l === current) return;
      current = l; store(l); apply();
      document.dispatchEvent(new CustomEvent('tpl:langchange', { detail: { lang: current } }));
    },
    toggle: function () { this.set(current === 'fr' ? 'en' : 'fr'); },
    // à appeler après injection dynamique de contenu portant des attributs i18n
    refresh: function (root) { applyAttributes(root); }
  };
  window.TPLI18N = TPLI18N;

  // Applique la langue le plus tôt possible (évite un flash de la mauvaise langue)
  apply();

  // Injecte le bouton de bascule dans l'en-tête (à côté du thème / accessibilité)
  function injectToggle() {
    var hr = document.querySelector('.header-right');
    if (!hr || hr.querySelector('.lang-toggle')) return;
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'lang-toggle';
    btn.addEventListener('click', function () { TPLI18N.toggle(); });
    var theme = hr.querySelector('.theme-toggle');
    if (theme) hr.insertBefore(btn, theme); else hr.appendChild(btn);
    apply();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', injectToggle);
  else injectToggle();
})();
