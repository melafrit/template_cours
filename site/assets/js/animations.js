/* =================================================================
   animations.js — Révélations au défilement, lecteur podcast, slides, encarts
   Cours "Réglementation des données et conformité" — M. EL AFRIT (CC BY-NC-SA 4.0)
   ================================================================= */
(function () {
  // -- Révélation au défilement --
  const reveals = document.querySelectorAll('.reveal, .content-section, .concept-card, .chapter-card, .eval-item, .tip');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); } });
    }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });
    reveals.forEach(el => { el.classList.add('reveal'); io.observe(el); });
  } else {
    reveals.forEach(el => el.classList.add('visible'));
  }

  // -- Génération des barres de waveform podcast --
  document.querySelectorAll('.podcast-waveform').forEach(wf => {
    const n = 48;
    for (let i = 0; i < n; i++) {
      const bar = document.createElement('span');
      bar.className = 'bar';
      const h = 20 + Math.abs(Math.sin(i * 0.6)) * 70 + (i % 3) * 6;
      bar.style.height = Math.min(100, h) + '%';
      wf.appendChild(bar);
    }
  });

  // -- Bouton play podcast (anime la waveform ; lit l'audio s'il existe) --
  document.querySelectorAll('.podcast-play-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const section = btn.closest('.podcast-section');
      const audio = section ? section.querySelector('audio.podcast-audio') : null;
      const playing = btn.dataset.playing === '1';
      if (audio) { playing ? audio.pause() : audio.play(); }
      btn.dataset.playing = playing ? '0' : '1';
      btn.textContent = playing ? '▶' : '⏸';
      const wf = section ? section.querySelector('.podcast-waveform') : null;
      if (wf) wf.querySelectorAll('.bar').forEach((b, i) => {
        b.style.transition = 'opacity .3s';
        b.style.opacity = playing ? '0.5' : (0.5 + Math.abs(Math.sin(i)) * 0.5).toFixed(2);
      });
    });
  });

  // -- Encarts d'exemple repliables --
  document.querySelectorAll('.example-box-header').forEach(h => {
    h.addEventListener('click', () => h.closest('.example-box').classList.toggle('open'));
  });

  // -- Galerie de slides (navigation entre images) --
  document.querySelectorAll('.slides-section').forEach(section => {
    const imgs = JSON.parse(section.dataset.slides || '[]');
    if (!imgs.length) return;
    let i = 0;
    const view = section.querySelector('.slides-viewport');
    const counter = section.querySelector('.slides-counter');
    const draw = () => {
      view.innerHTML = `<img src="${imgs[i]}" alt="Slide ${i + 1}" loading="lazy">`;
      if (counter) counter.textContent = `${i + 1} / ${imgs.length}`;
    };
    const prev = section.querySelector('.slides-prev');
    const next = section.querySelector('.slides-next');
    if (prev) prev.addEventListener('click', () => { i = (i - 1 + imgs.length) % imgs.length; draw(); });
    if (next) next.addEventListener('click', () => { i = (i + 1) % imgs.length; draw(); });
    draw();
  });
})();
