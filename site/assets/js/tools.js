/* =================================================================
   tools.js — Outils interactifs "métier" (RGPD)
   Cours "Réglementation des données et conformité" — M. EL AFRIT (CC BY-NC-SA 4.0)
   Espace de noms : window.RDCTools
     RDCTools.sanction('id-conteneur');   // simulateur de sanction (art. 83)
   (Autres outils ajoutés au fil des chapitres : base légale, classificateur, AIPD.)
   ================================================================= */
(function () {
  window.RDCTools = window.RDCTools || {};

  function euro(montantE) {
    // formate un montant en euros, lisible (k€, M€, Md€)
    if (montantE >= 1e9) return (montantE / 1e9).toLocaleString('fr-FR', { maximumFractionDigits: 2 }) + ' Md€';
    if (montantE >= 1e6) return (montantE / 1e6).toLocaleString('fr-FR', { maximumFractionDigits: 2 }) + ' M€';
    if (montantE >= 1e3) return (montantE / 1e3).toLocaleString('fr-FR', { maximumFractionDigits: 0 }) + ' k€';
    return Math.round(montantE).toLocaleString('fr-FR') + ' €';
  }

  /* ---------- Simulateur de sanction (art. 83) ---------- */
  var MANQUEMENTS = [
    { t: 2, l: "Non-respect des principes (licéité, finalité, minimisation…) — art. 5" },
    { t: 2, l: "Absence de base légale / consentement non valable — art. 6 & 7" },
    { t: 2, l: "Traitement illicite de données sensibles — art. 9" },
    { t: 2, l: "Atteinte aux droits des personnes (accès, effacement, opposition…) — art. 12-22" },
    { t: 2, l: "Transfert illicite de données hors UE — art. 44-49" },
    { t: 1, l: "Défaut de sécurité du traitement — art. 32" },
    { t: 1, l: "Registre des traitements absent ou incomplet — art. 30" },
    { t: 1, l: "Violation de données non notifiée (CNIL / personnes) — art. 33-34" },
    { t: 1, l: "AIPD non réalisée alors qu'elle est obligatoire — art. 35" },
    { t: 1, l: "DPO non désigné alors qu'il est obligatoire — art. 37" },
    { t: 1, l: "Manquements du sous-traitant / contrat de sous-traitance — art. 28" },
    { t: 1, l: "Privacy by design & by default ignoré — art. 25" }
  ];
  var TIER = {
    2: { cap: 20e6, pct: 4, art: "art. 83.5", lib: "Manquement majeur", ex: "Ex. : Meta — 1,2 Md€ (2023, transferts) ; Google — 150 M€ (2021, cookies)." },
    1: { cap: 10e6, pct: 2, art: "art. 83.4", lib: "Manquement aux obligations", ex: "Ex. : SERGIC — 400 000 € (2019, défaut de sécurité, art. 32)." }
  };

  RDCTools.sanction = function (containerId) {
    var el = document.getElementById(containerId);
    if (!el) return;
    el.classList.add('rdc-tool');

    var opts = MANQUEMENTS.map(function (m, i) { return '<option value="' + i + '">' + m.l + '</option>'; }).join('');
    el.innerHTML =
        '<div class="rdc-tool-head"><span class="rdc-tool-ico">⚖️</span><span class="rdc-tool-title">Simulateur de sanction RGPD</span></div>'
      + '<div class="rdc-tool-body">'
      + '  <label class="rdc-field"><span>Type de manquement</span>'
      + '    <select class="rdc-select" id="' + containerId + '-m">' + opts + '</select></label>'
      + '  <label class="rdc-field"><span>Chiffre d\'affaires annuel mondial</span>'
      + '    <span class="rdc-ca"><input type="number" min="0" step="1" value="50" class="rdc-input" id="' + containerId + '-ca"><span class="rdc-unit">M€</span></span></label>'
      + '  <div class="rdc-presets" role="group" aria-label="Exemples de chiffre d\'affaires">'
      + '    <button type="button" class="rdc-chip" data-ca="2">PME · 2 M€</button>'
      + '    <button type="button" class="rdc-chip" data-ca="200">ETI · 200 M€</button>'
      + '    <button type="button" class="rdc-chip" data-ca="8000">Grand groupe · 8 Md€</button>'
      + '  </div>'
      + '  <div class="rdc-result" aria-live="polite"></div>'
      + '  <p class="rdc-disclaimer">Ce sont des <strong>plafonds maximaux</strong>. La CNIL module le montant réel selon la gravité, la durée, la coopération, etc. (art. 83.2).</p>'
      + '</div>';

    var sel = el.querySelector('#' + containerId + '-m');
    var ca = el.querySelector('#' + containerId + '-ca');
    var res = el.querySelector('.rdc-result');

    function compute() {
      var m = MANQUEMENTS[+sel.value] || MANQUEMENTS[0];
      var info = TIER[m.t];
      var caM = Math.max(0, parseFloat(ca.value) || 0);
      var caE = caM * 1e6;
      var pctE = caE * info.pct / 100;
      var maxE = Math.max(info.cap, pctE);
      var capWins = info.cap >= pctE;
      res.innerHTML =
          '<div class="rdc-tier rdc-tier-' + m.t + '">' + (m.t === 2 ? '🔴' : '🟠') + ' ' + info.lib + ' · <strong>' + info.art + '</strong></div>'
        + '<div class="rdc-amount">Plafond : <strong>' + euro(maxE) + '</strong></div>'
        + '<div class="rdc-detail">le plus élevé de '
        + '<span class="' + (capWins ? 'rdc-win' : '') + '">' + euro(info.cap) + '</span> (plafond fixe) '
        + 'et <span class="' + (!capWins ? 'rdc-win' : '') + '">' + euro(pctE) + '</span> (' + info.pct + ' % du CA)</div>'
        + '<div class="rdc-ex">' + info.ex + '</div>';
    }

    sel.addEventListener('change', compute);
    ca.addEventListener('input', compute);
    el.querySelectorAll('.rdc-chip').forEach(function (c) {
      c.addEventListener('click', function () { ca.value = c.getAttribute('data-ca'); compute(); });
    });
    compute();
  };

  /* ---------- Sélecteur de base légale (art. 6) ---------- */
  RDCTools.baseLegale = function (containerId) {
    var el = document.getElementById(containerId); if (!el) return;
    el.classList.add('rdc-tool');
    var STEPS = [
      { q: "Le traitement est-il imposé par une obligation légale à laquelle l'organisme est soumis ?",
        b: { nom: "Obligation légale", art: "art. 6.1.c", ex: "Ex. : conservation de journaux imposée par un texte, réponse à une réquisition." } },
      { q: "Est-il nécessaire à l'exécution d'un contrat avec la personne concernée (ou à des mesures précontractuelles à sa demande) ?",
        b: { nom: "Contrat", art: "art. 6.1.b", ex: "Ex. : compte usager de l'application de mobilité, abonnement de transport." } },
      { q: "L'organisme est-il une autorité publique agissant dans le cadre d'une mission d'intérêt public ?",
        b: { nom: "Mission d'intérêt public", art: "art. 6.1.e", ex: "Ex. UrbanHub : supervision du trafic par la collectivité — la base principale du fil rouge." } },
      { q: "S'agit-il de sauvegarder la vie ou l'intégrité physique d'une personne (urgence vitale) ?",
        b: { nom: "Intérêts vitaux", art: "art. 6.1.d", ex: "Ex. : situation d'urgence sanitaire mettant en jeu la vie d'une personne." } },
      { q: "La personne peut-elle donner un consentement libre, spécifique, éclairé et univoque (révocable à tout moment) ?",
        b: { nom: "Consentement", art: "art. 6.1.a", ex: "Ex. : cookies non essentiels, newsletter. À éviter pour une autorité publique en position d'autorité." } }
    ];
    var FALLBACK = { nom: "Intérêt légitime", art: "art. 6.1.f", ex: "À mettre en balance avec les droits des personnes (test de proportionnalité). ⚠ Indisponible pour une autorité publique dans l'exercice de ses missions." };
    var step = 0;
    function head() { return '<div class="rdc-tool-head"><span class="rdc-tool-ico">🧭</span><span class="rdc-tool-title">Quelle base légale ? (art. 6)</span></div>'; }
    function render() {
      var s = STEPS[step];
      el.innerHTML = head() + '<div class="rdc-tool-body">'
        + '<div class="rdc-step">Question ' + (step + 1) + ' / ' + STEPS.length + '</div>'
        + '<p class="rdc-q">' + s.q + '</p>'
        + '<div class="rdc-yn"><button type="button" class="rdc-btn rdc-yes">Oui</button>'
        + '<button type="button" class="rdc-btn rdc-no">Non</button></div></div>';
      el.querySelector('.rdc-yes').addEventListener('click', function () { result(STEPS[step].b); });
      el.querySelector('.rdc-no').addEventListener('click', function () { step++; if (step < STEPS.length) render(); else result(FALLBACK); });
    }
    function result(b) {
      el.innerHTML = head() + '<div class="rdc-tool-body"><div class="rdc-result">'
        + '<div class="rdc-tier">Base recommandée</div>'
        + '<div class="rdc-amount">' + b.nom + ' · <strong>' + b.art + '</strong></div>'
        + '<div class="rdc-ex">' + b.ex + '</div></div>'
        + '<div class="rdc-tools-row"><button type="button" class="rdc-restart">↺ Recommencer</button></div></div>';
      el.querySelector('.rdc-restart').addEventListener('click', function () { step = 0; render(); });
    }
    render();
  };

  /* ---------- Classificateur de données (perso / sensible / non perso) ---------- */
  RDCTools.classifier = function (containerId) {
    var el = document.getElementById(containerId); if (!el) return;
    el.classList.add('rdc-tool');
    var CATS = { perso: "Personnelle", sensible: "Sensible (art. 9)", non: "Non personnelle" };
    var ITEMS = [
      { ex: "Une adresse IP, même dynamique", cat: "perso", why: "Identifiant indirect : recoupée avec d'autres informations, elle permet de remonter à une personne (CJUE Breyer)." },
      { ex: "Une plaque d'immatriculation lue par une caméra", cat: "perso", why: "Donnée indirectement identifiante → donnée personnelle." },
      { ex: "Les données de santé d'un usager", cat: "sensible", why: "Catégorie particulière de l'art. 9 : interdiction de principe, protection renforcée." },
      { ex: "L'appartenance syndicale d'un agent", cat: "sensible", why: "Catégorie particulière de l'art. 9." },
      { ex: "Le nombre de véhicules par heure sur un carrefour (agrégé, anonymisé)", cat: "non", why: "Donnée anonyme non rattachable à une personne → hors RGPD (relève p. ex. du Data Act)." },
      { ex: "Un visage filmé puis traité pour identifier la personne", cat: "sensible", why: "Donnée biométrique aux fins d'identification = catégorie particulière (art. 9)." },
      { ex: "Les données génétiques d'une personne", cat: "sensible", why: "Catégorie particulière de l'art. 9." },
      { ex: "La température renvoyée par un capteur, sans lien avec une personne", cat: "non", why: "Donnée non personnelle." },
      { ex: "Un identifiant pseudonymisé (réversible avec une clé)", cat: "perso", why: "La pseudonymisation reste une donnée personnelle : la réidentification demeure possible." }
    ];
    var i = 0, score = 0;
    function head() { return '<div class="rdc-tool-head"><span class="rdc-tool-ico">🗂️</span><span class="rdc-tool-title">Cette donnée est-elle personnelle ?</span></div>'; }
    function render() {
      if (i >= ITEMS.length) {
        el.innerHTML = head() + '<div class="rdc-tool-body"><div class="rdc-result"><div class="rdc-amount">Score : ' + score + ' / ' + ITEMS.length + '</div></div>'
          + '<div class="rdc-tools-row"><button type="button" class="rdc-restart">↺ Recommencer</button></div></div>';
        el.querySelector('.rdc-restart').addEventListener('click', function () { i = 0; score = 0; render(); });
        return;
      }
      var it = ITEMS[i];
      el.innerHTML = head() + '<div class="rdc-tool-body">'
        + '<div class="rdc-step">Exemple ' + (i + 1) + ' / ' + ITEMS.length + ' · Score ' + score + '</div>'
        + '<p class="rdc-q">«&nbsp;' + it.ex + '&nbsp;»</p>'
        + '<div class="rdc-opts">'
        + '<button type="button" class="rdc-opt" data-c="perso">Personnelle</button>'
        + '<button type="button" class="rdc-opt" data-c="sensible">Sensible (art. 9)</button>'
        + '<button type="button" class="rdc-opt" data-c="non">Non personnelle</button></div>'
        + '<div class="rdc-feedback" aria-live="polite"></div>'
        + '<div class="rdc-tools-row"><button type="button" class="rdc-next2" hidden>Suivant ›</button></div></div>';
      var opts = el.querySelectorAll('.rdc-opt');
      var fb = el.querySelector('.rdc-feedback');
      var next = el.querySelector('.rdc-next2');
      var done = false;
      opts.forEach(function (b) {
        b.addEventListener('click', function () {
          if (done) return; done = true;
          var ok = b.getAttribute('data-c') === it.cat; if (ok) score++;
          opts.forEach(function (x) { var c = x.getAttribute('data-c'); if (c === it.cat) x.classList.add('is-correct'); else if (x === b) x.classList.add('is-wrong'); x.disabled = true; });
          fb.innerHTML = (ok ? '<span class="fb-ok">✅ Exact.</span> ' : '<span class="fb-no">❌ Non.</span> ') + '<strong>' + CATS[it.cat] + '.</strong> ' + it.why;
          fb.classList.add('show'); next.hidden = false;
        });
      });
      next.addEventListener('click', function () { i++; render(); });
    }
    render();
  };

  /* ---------- « AIPD obligatoire ? » (art. 35, critères CEPD) ---------- */
  RDCTools.aipd = function (containerId) {
    var el = document.getElementById(containerId); if (!el) return;
    el.classList.add('rdc-tool');
    var CRIT = [
      "Évaluation ou notation (scoring, profilage)",
      "Décision automatisée produisant un effet juridique ou similaire significatif",
      "Surveillance systématique (y compris d'une zone accessible au public)",
      "Données sensibles (art. 9) ou à caractère hautement personnel",
      "Traitement de données à grande échelle",
      "Croisement ou combinaison d'ensembles de données",
      "Personnes vulnérables (enfants, salariés, patients…)",
      "Usage innovant ou nouvelles technologies (IA, IoT, biométrie…)",
      "Le traitement empêche d'exercer un droit ou de bénéficier d'un service / contrat"
    ];
    el.innerHTML = '<div class="rdc-tool-head"><span class="rdc-tool-ico">🔎</span><span class="rdc-tool-title">AIPD obligatoire ? (art. 35)</span></div>'
      + '<div class="rdc-tool-body"><p class="rdc-q">Cochez les critères (CEPD) qui s\'appliquent à votre traitement :</p>'
      + '<div class="rdc-checks">' + CRIT.map(function (c, k) { return '<label class="rdc-check"><input type="checkbox" data-i="' + k + '"><span>' + c + '</span></label>'; }).join('') + '</div>'
      + '<div class="rdc-result rdc-verdict" aria-live="polite"></div>'
      + '<p class="rdc-disclaimer">Règle CEPD : à partir de <strong>2 critères</strong>, le traitement est présumé « susceptible d\'engendrer un risque élevé » → <strong>AIPD requise</strong> (art. 35). Certains cas de l\'art. 35.3 l\'imposent d\'office (ex. surveillance systématique à grande échelle d\'une zone publique).</p></div>';
    var verdict = el.querySelector('.rdc-verdict');
    function update() {
      var n = el.querySelectorAll('.rdc-check input:checked').length, msg, cls;
      if (n >= 2) { msg = '🔴 <strong>AIPD obligatoire</strong> (en principe) — ' + n + ' critères réunis.'; cls = 'rdc-tier-2'; }
      else if (n === 1) { msg = '🟠 <strong>AIPD recommandée</strong> — 1 critère réuni. Documentez votre analyse.'; cls = 'rdc-tier-1'; }
      else { msg = '🟢 <strong>A priori non requise</strong> — aucun critère coché. Conservez une trace de la décision.'; cls = ''; }
      verdict.className = 'rdc-result rdc-verdict ' + cls; verdict.innerHTML = msg;
    }
    el.querySelectorAll('.rdc-check input').forEach(function (c) { c.addEventListener('change', update); });
    update();
  };
})();
