/* =================================================================
   flashcards.js — Cartes de révision active (mémorisation)
   Cours "Réglementation des données et conformité" — M. EL AFRIT (CC BY-NC-SA 4.0)
   Usage :
     new FlashcardDeck('id-conteneur', [
       { front:'Question / notion', back:'Définition **avec gras**', ref:'art. 5' }, …
     ], 'cle-deck');   // cle-deck : pour mémoriser "su / à revoir" (localStorage)
   ================================================================= */
(function () {
  function esc(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  function rich(s) { // **gras** -> <strong>, le reste échappé
    return esc(s).split('**').map(function (seg, i) { return i % 2 ? '<strong>' + seg + '</strong>' : seg; }).join('');
  }

  function FlashcardDeck(containerId, cards, key) {
    this.el = document.getElementById(containerId);
    this.cards = cards || [];
    this.key = 'rdc-flash-' + (key || containerId);
    this.order = this.cards.map(function (_, i) { return i; });
    this.pos = 0;
    this.flipped = false;
    this.known = this.load();
    if (this.el && this.cards.length) this.build();
  }

  FlashcardDeck.prototype.load = function () { try { return JSON.parse(localStorage.getItem(this.key)) || {}; } catch (e) { return {}; } };
  FlashcardDeck.prototype.persist = function () { try { localStorage.setItem(this.key, JSON.stringify(this.known)); } catch (e) {} };
  FlashcardDeck.prototype.countKnown = function () { var n = 0; for (var k in this.known) if (this.known[k]) n++; return n; };

  FlashcardDeck.prototype.build = function () {
    var self = this;
    this.el.classList.add('flashcards');
    this.el.innerHTML =
        '<div class="flashcard" tabindex="0" role="button" aria-label="Carte de révision : cliquer pour retourner">'
      + '  <div class="flashcard-face flashcard-front"><span class="flashcard-tag">Question</span><div class="flashcard-text"></div><span class="flashcard-hint">↺ Cliquer pour retourner</span></div>'
      + '  <div class="flashcard-face flashcard-back"><span class="flashcard-tag">Réponse</span><div class="flashcard-text"></div><span class="flashcard-ref"></span></div>'
      + '</div>'
      + '<div class="flashcard-bar">'
      + '  <div class="flashcard-known-bar"><span></span></div>'
      + '  <div class="flashcard-status"></div>'
      + '</div>'
      + '<div class="flashcard-controls">'
      + '  <button type="button" class="fc-btn fc-prev" aria-label="Carte précédente">‹</button>'
      + '  <button type="button" class="fc-btn fc-revoir">À revoir ↻</button>'
      + '  <button type="button" class="fc-btn fc-su">✓ Je savais</button>'
      + '  <button type="button" class="fc-btn fc-next" aria-label="Carte suivante">›</button>'
      + '</div>'
      + '<div class="flashcard-tools">'
      + '  <button type="button" class="fc-link fc-shuffle">🔀 Mélanger</button>'
      + '  <button type="button" class="fc-link fc-reset">↺ Réinitialiser mes réponses</button>'
      + '</div>';

    this.card = this.el.querySelector('.flashcard');
    this.frontText = this.el.querySelector('.flashcard-front .flashcard-text');
    this.backText = this.el.querySelector('.flashcard-back .flashcard-text');
    this.refEl = this.el.querySelector('.flashcard-ref');
    this.statusEl = this.el.querySelector('.flashcard-status');
    this.knownBar = this.el.querySelector('.flashcard-known-bar span');

    this.card.addEventListener('click', function () { self.flip(); });
    this.card.addEventListener('keydown', function (e) { if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); self.flip(); } });
    this.el.querySelector('.fc-prev').addEventListener('click', function () { self.go(-1); });
    this.el.querySelector('.fc-next').addEventListener('click', function () { self.go(1); });
    this.el.querySelector('.fc-su').addEventListener('click', function () { self.mark(true); });
    this.el.querySelector('.fc-revoir').addEventListener('click', function () { self.mark(false); });
    this.el.querySelector('.fc-shuffle').addEventListener('click', function () { self.shuffle(); });
    this.el.querySelector('.fc-reset').addEventListener('click', function () { self.reset(); });

    this.render();
  };

  FlashcardDeck.prototype.current = function () { return this.cards[this.order[this.pos]]; };

  FlashcardDeck.prototype.render = function () {
    var c = this.current(); if (!c) return;
    this.flipped = false;
    this.card.classList.remove('is-flipped');
    this.frontText.innerHTML = rich(c.front);
    this.backText.innerHTML = rich(c.back);
    this.refEl.innerHTML = c.ref ? rich(c.ref) : '';
    this.refEl.style.display = c.ref ? '' : 'none';
    var idx = this.order[this.pos];
    var state = this.known[idx] === true ? 'su' : (this.known[idx] === false ? 'revoir' : '');
    this.statusEl.textContent = 'Carte ' + (this.pos + 1) + ' / ' + this.cards.length
      + (state === 'su' ? ' · ✓ su' : state === 'revoir' ? ' · ↻ à revoir' : '');
    this.statusEl.className = 'flashcard-status' + (state ? ' is-' + state : '');
    var pct = Math.round(this.countKnown() / this.cards.length * 100);
    this.knownBar.style.width = pct + '%';
  };

  FlashcardDeck.prototype.flip = function () { this.flipped = !this.flipped; this.card.classList.toggle('is-flipped', this.flipped); };
  FlashcardDeck.prototype.go = function (d) { this.pos = (this.pos + d + this.cards.length) % this.cards.length; this.render(); };
  FlashcardDeck.prototype.mark = function (ok) { this.known[this.order[this.pos]] = ok; this.persist(); if (this.pos < this.cards.length - 1) this.go(1); else this.render(); };

  FlashcardDeck.prototype.shuffle = function () {
    for (var i = this.order.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = this.order[i]; this.order[i] = this.order[j]; this.order[j] = t;
    }
    this.pos = 0; this.render();
  };

  FlashcardDeck.prototype.reset = function () { this.known = {}; this.persist(); this.render(); };

  window.FlashcardDeck = FlashcardDeck;
})();
