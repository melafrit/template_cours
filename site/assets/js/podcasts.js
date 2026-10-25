/* =================================================================
   podcasts.js — la page Podcasts (module 03) : la bande des diapositives
   de chaque épisode, et la visionneuse qui les agrandit sur toute la page.
   Template de site de cours — Mohamed EL AFRIT (MIT / CC BY 4.0)

   outils/generer_fragments.py écrit, d'après outils/podcasts.py, sous le
   lecteur d'un épisode dont le diaporama est publié, un conteneur vide :
     <div class="pod-diapos" data-dossier="…/diaporamas/chapitre-1-podcast.fr/"
          data-nombre="14" data-grande="1600x900" data-vignette="320x180"
          data-episode="Épisode 1 — …">
   Ce script y dessine la bande des vignettes (vignette-01.webp…, et
   diapo-01.webp… pour l'agrandissement : deux chiffres au moins, la règle de
   nom_image() dans outils/podcasts.py). La bande se dessine ici, et non dans
   le HTML : sur un site miroir, les deux pages jumelles gardent la même suite
   de blocs quand une langue a ses diapositives et l'autre pas encore.

   Un clic sur une vignette ouvre la visionneuse : un <dialog> modal
   (role="dialog", aria-modal) sur toute la page, la diapositive agrandie, un
   bouton × en haut à droite. Échap ferme ; les flèches ← → passent d'une
   diapositive à l'autre (Début et Fin : la première et la dernière), le doigt
   aussi, d'un glissé ; un clic à côté de la diapositive ferme. Le focus reste
   dans la fenêtre (Tab y tourne) et revient, à la fermeture, à la vignette de
   la diapositive affichée. Les libellés suivent la langue du conteneur : son
   bloc data-tr sur une page bilingue, sinon celle de la page.
   Repris du cours d'architecture logicielle.
   ================================================================= */
(function () {
  'use strict';

  var conteneurs = document.querySelectorAll('.pod-diapos[data-dossier]');
  if (!conteneurs.length) return;

  var LIB = {
    fr: {
      bande: 'Diapositives — {e}',
      vignette: 'Agrandir la diapositive {i} sur {n}',
      gauche: 'Faire défiler les diapositives vers la gauche',
      droite: 'Faire défiler les diapositives vers la droite',
      fenetre: 'Visionneuse des diapositives — {e}',
      fermer: 'Fermer la visionneuse',
      prec: 'Diapositive précédente',
      suiv: 'Diapositive suivante',
      compteur: 'Diapositive {i} sur {n}',
      alt: 'Diapositive {i} sur {n} — {e}',
      aide: '← → pour changer de diapositive · Échap pour fermer'
    },
    en: {
      bande: 'Slides — {e}',
      vignette: 'Enlarge slide {i} of {n}',
      gauche: 'Scroll the slides left',
      droite: 'Scroll the slides right',
      fenetre: 'Slide viewer — {e}',
      fermer: 'Close the slide viewer',
      prec: 'Previous slide',
      suiv: 'Next slide',
      compteur: 'Slide {i} of {n}',
      alt: 'Slide {i} of {n} — {e}',
      aide: '← → to change slides · Esc to close'
    }
  };

  function langueDe(el) {
    var bloc = el.closest('[data-tr]');
    if (bloc) return bloc.getAttribute('data-tr') === 'en' ? 'en' : 'fr';
    return /^en/i.test(document.documentElement.getAttribute('lang') || '') ? 'en' : 'fr';
  }
  function f(modele, v) {
    return modele.replace(/\{(\w+)\}/g, function (_, k) { return v[k] != null ? v[k] : ''; });
  }
  function taille(s) {
    var m = /^(\d+)x(\d+)$/.exec(s || '');
    return m ? [parseInt(m[1], 10), parseInt(m[2], 10)] : null;
  }
  function nom(sorte, i, n) {
    var largeur = Math.max(2, String(n).length), s = String(i);
    while (s.length < largeur) s = '0' + s;
    return sorte + '-' + s + '.webp';
  }

  // ---------------------------------------------------------------- les bandes
  var bandes = [];
  Array.prototype.forEach.call(conteneurs, function (c) {
    var n = parseInt(c.getAttribute('data-nombre'), 10);
    if (!(n > 0)) return;
    var ep = {
      dossier: c.getAttribute('data-dossier'), n: n, titre: c.getAttribute('data-episode') || '',
      grande: taille(c.getAttribute('data-grande')), vignette: taille(c.getAttribute('data-vignette')),
      lang: langueDe(c), boutons: []
    };
    var T = LIB[ep.lang];
    var cadre = document.createElement('div');
    cadre.className = 'pod-bande-cadre';
    var liste = document.createElement('ol');
    liste.className = 'pod-bande';
    liste.setAttribute('aria-label', f(T.bande, { e: ep.titre }));
    for (var i = 1; i <= n; i++) {
      var li = document.createElement('li');
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'pod-vignette';
      b.setAttribute('aria-label', f(T.vignette, { i: i, n: n }));
      var img = document.createElement('img');
      img.src = ep.dossier + nom('vignette', i, n);
      img.alt = '';
      img.loading = 'lazy';
      img.decoding = 'async';
      if (ep.vignette) { img.width = ep.vignette[0]; img.height = ep.vignette[1]; }
      var num = document.createElement('span');
      num.className = 'pod-vignette-n';
      num.setAttribute('aria-hidden', 'true');
      num.textContent = String(i);
      b.appendChild(img);
      b.appendChild(num);
      li.appendChild(b);
      liste.appendChild(li);
      b.addEventListener('click', ouvrirDepuis(ep, i - 1));
      ep.boutons.push(b);
    }
    // Les flèches de défilement servent la souris ; au clavier, Tab parcourt déjà les vignettes, une à une.
    var gauche = fleche('pod-defiler-gauche', '‹', T.gauche), droite = fleche('pod-defiler-droite', '›', T.droite);
    cadre.appendChild(gauche);
    cadre.appendChild(liste);
    cadre.appendChild(droite);
    c.appendChild(cadre);
    ep.liste = liste;
    function bornes() {                    // une flèche n'apparaît que s'il reste à défiler de son côté
      var max = liste.scrollWidth - liste.clientWidth - 8;
      gauche.hidden = liste.scrollLeft <= 8;
      droite.hidden = liste.scrollLeft >= max;
    }
    gauche.addEventListener('click', function () { defiler(liste, -1); });
    droite.addEventListener('click', function () { defiler(liste, 1); });
    liste.addEventListener('scroll', bornes, { passive: true });
    window.addEventListener('resize', bornes);
    bandes.push(bornes);
    bornes();
  });
  // Une bande masquée (l'autre langue d'une page bilingue) n'a pas de largeur : ses flèches se recalculent quand
  // elle paraît.
  document.addEventListener('tpl:langchange', function () { bandes.forEach(function (b) { b(); }); });

  function fleche(classe, signe, libelle) {
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'pod-defiler ' + classe;
    b.tabIndex = -1;
    b.setAttribute('aria-hidden', 'true');
    b.title = libelle;
    b.textContent = signe;
    return b;
  }
  function defiler(liste, sens) {
    var pas = Math.max(160, liste.clientWidth * 0.8) * sens;
    if (typeof liste.scrollBy === 'function') liste.scrollBy({ left: pas, behavior: 'smooth' });
    else liste.scrollLeft += pas;
  }
  function ouvrirDepuis(ep, i) {
    return function () { ouvrir(ep, i); };
  }

  // ---------------------------------------------------------------- la visionneuse
  var fenetre = null, image, episodeEl, compteur, aide, btnFermer, btnPrec, btnSuiv;
  var courant = null, indice = 0, ouverte = false, natif = false, x0 = null, glisse = false;

  function construire() {
    fenetre = document.createElement('dialog');
    fenetre.className = 'pod-visionneuse';
    fenetre.setAttribute('role', 'dialog');
    fenetre.setAttribute('aria-modal', 'true');
    fenetre.innerHTML =
        '<div class="pod-v-tete">'
      +   '<p class="pod-v-titre"><span class="pod-v-episode"></span>'
      +   '<span class="pod-v-compteur" aria-live="polite"></span></p>'
      +   '<button type="button" class="pod-v-fermer"><span aria-hidden="true">×</span></button>'
      + '</div>'
      + '<div class="pod-v-scene">'
      +   '<button type="button" class="pod-v-nav pod-v-prec"><span aria-hidden="true">‹</span></button>'
      +   '<img class="pod-v-image" alt="">'
      +   '<button type="button" class="pod-v-nav pod-v-suiv"><span aria-hidden="true">›</span></button>'
      + '</div>'
      + '<p class="pod-v-aide"></p>';
    document.body.appendChild(fenetre);
    image = fenetre.querySelector('.pod-v-image');
    episodeEl = fenetre.querySelector('.pod-v-episode');
    compteur = fenetre.querySelector('.pod-v-compteur');
    aide = fenetre.querySelector('.pod-v-aide');
    btnFermer = fenetre.querySelector('.pod-v-fermer');
    btnPrec = fenetre.querySelector('.pod-v-prec');
    btnSuiv = fenetre.querySelector('.pod-v-suiv');

    btnFermer.addEventListener('click', fermer);
    btnPrec.addEventListener('click', function () { aller(indice - 1); });
    btnSuiv.addEventListener('click', function () { aller(indice + 1); });
    // Échap sur un <dialog> natif : l'événement « cancel » ; on ferme nous-mêmes, pour rendre le focus.
    fenetre.addEventListener('cancel', function (e) { e.preventDefault(); fermer(); });
    // Un clic à côté de la diapositive (le fond, la scène) ferme ; pas la fin d'un glissé.
    var scene = fenetre.querySelector('.pod-v-scene');
    fenetre.addEventListener('click', function (e) {
      if (glisse) { glisse = false; return; }
      if (e.target === fenetre || e.target === scene) fermer();
    });
    scene.addEventListener('pointerdown', function (e) {
      glisse = false;
      x0 = e.pointerType === 'mouse' ? null : e.clientX;
    });
    scene.addEventListener('pointercancel', function () { x0 = null; });
    scene.addEventListener('pointerup', function (e) {
      if (x0 === null) return;
      var dx = e.clientX - x0;
      x0 = null;
      if (Math.abs(dx) > 50) { glisse = true; aller(indice + (dx < 0 ? 1 : -1)); }
    });
    document.addEventListener('keydown', clavier);
  }

  function libeller(T, ep) {               // les libellés de la fenêtre, dans la langue de l'épisode ouvert
    fenetre.setAttribute('aria-label', f(T.fenetre, { e: ep.titre }));
    btnFermer.setAttribute('aria-label', T.fermer);
    btnFermer.title = T.fermer;
    btnPrec.setAttribute('aria-label', T.prec);
    btnSuiv.setAttribute('aria-label', T.suiv);
    aide.textContent = T.aide;
  }

  function ouvrir(ep, i) {
    if (!fenetre) construire();
    courant = ep;
    episodeEl.textContent = ep.titre;
    libeller(LIB[ep.lang], ep);
    btnPrec.hidden = btnSuiv.hidden = ep.n < 2;
    aller(i);
    document.documentElement.classList.add('pod-v-ouverte');
    if (typeof fenetre.showModal === 'function') {
      if (!fenetre.open) fenetre.showModal();
      natif = true;
    } else {
      fenetre.setAttribute('open', '');
      natif = false;
    }
    ouverte = true;
    btnFermer.focus();
  }

  function aller(i) {
    if (!courant || i < 0 || i >= courant.n) return;
    indice = i;
    var n = courant.n, T = LIB[courant.lang];
    image.src = courant.dossier + nom('diapo', i + 1, n);
    if (courant.grande) { image.width = courant.grande[0]; image.height = courant.grande[1]; }
    image.alt = f(T.alt, { i: i + 1, n: n, e: courant.titre });
    compteur.textContent = f(T.compteur, { i: i + 1, n: n });
    // aria-disabled plutôt que disabled : un bouton désactivé perdrait le focus, qui sortirait de la fenêtre.
    btnPrec.setAttribute('aria-disabled', i === 0 ? 'true' : 'false');
    btnSuiv.setAttribute('aria-disabled', i === n - 1 ? 'true' : 'false');
    precharger(i - 1);
    precharger(i + 1);
  }

  function precharger(i) {
    if (!courant || i < 0 || i >= courant.n) return;
    var im = new Image();
    im.src = courant.dossier + nom('diapo', i + 1, courant.n);
  }

  function fermer() {
    if (!ouverte) return;
    ouverte = false;
    if (natif && fenetre.open) fenetre.close();
    else fenetre.removeAttribute('open');
    document.documentElement.classList.remove('pod-v-ouverte');
    // Le focus revient à la vignette de la diapositive affichée, que la bande montre, sans bouger la page.
    var cible = courant && courant.boutons[indice];
    if (!cible) return;
    try { cible.focus({ preventScroll: true }); } catch (e) { cible.focus(); }
    var liste = courant.liste, r = cible.getBoundingClientRect(), rl = liste.getBoundingClientRect();
    if (r.left < rl.left || r.right > rl.right) liste.scrollLeft += (r.left - rl.left) - (rl.width - r.width) / 2;
  }

  function focusables() {
    return [btnFermer, btnPrec, btnSuiv].filter(function (b) { return !b.hidden; });
  }

  function clavier(e) {
    if (!ouverte) return;
    switch (e.key) {
      case 'Escape': case 'Esc':
        e.preventDefault(); fermer(); break;
      case 'ArrowLeft': case 'Left':
        e.preventDefault(); aller(indice - 1); break;
      case 'ArrowRight': case 'Right':
        e.preventDefault(); aller(indice + 1); break;
      case 'Home':
        e.preventDefault(); aller(0); break;
      case 'End':
        e.preventDefault(); aller(courant.n - 1); break;
      case 'Tab': {
        // Le focus tourne dans la fenêtre : après le dernier bouton, le premier, et inversement.
        var liste = focusables(), k = liste.indexOf(document.activeElement);
        e.preventDefault();
        var j = e.shiftKey ? (k <= 0 ? liste.length - 1 : k - 1) : (k < 0 || k === liste.length - 1 ? 0 : k + 1);
        liste[j].focus();
        break;
      }
    }
  }
})();
