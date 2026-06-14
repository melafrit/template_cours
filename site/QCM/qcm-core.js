/* =================================================================
   qcm-core.js — Logique partagée du QCM (QCM, correction, dashboard)
   Cours "Réglementation des données et conformité" — M. EL AFRIT (CC BY-NC-SA 4.0)

   Barème CBM strict (Certainty-Based Marking), indépendant de la difficulté :
     Certitude Élevée  : bonne réponse +3 / mauvaise −3
     Certitude Moyenne : bonne réponse +2 / mauvaise −2
     Certitude Faible  : bonne réponse +1 / mauvaise  0
   Note /20 = score brut ÷ (3 × nombre de questions) × 20, bornée à [0 ; 20].
   ================================================================= */
window.QCMCore = (function () {
  function lng() { return window.TPLI18N ? TPLI18N.lang() : 'fr'; }
  var SALT = 'TPL_QCM_SALT';
  var CSV_VERSION = 'TPL-QCM v1';
  var LETTERS = ['A', 'B', 'C', 'D', 'E', 'F'];

  // Barème CBM (points par certitude). Libellés/indices bilingues { fr, en }.
  var CBM = {
    elevee:  { ok: 3, no: -3, label: { fr: 'Élevée',  en: 'High' },   hint: { fr: 'certain',    en: 'certain' } },
    moyenne: { ok: 2, no: -2, label: { fr: 'Moyenne', en: 'Medium' }, hint: { fr: 'assez sûr',  en: 'fairly sure' } },
    faible:  { ok: 1, no: 0,  label: { fr: 'Faible',  en: 'Low' },    hint: { fr: 'je devine',  en: 'guessing' } }
  };
  var CERT_ORDER = ['faible', 'moyenne', 'elevee'];
  var DIFF_COLOR = { vert: '#2f8f5b', jaune: '#c9a227', orange: '#d2762a', rouge: '#c0392b' };
  var DIFF_LABEL = { vert: { fr: 'Facile', en: 'Easy' }, jaune: { fr: 'Moyen', en: 'Medium' }, orange: { fr: 'Difficile', en: 'Hard' }, rouge: { fr: 'Expert', en: 'Expert' } };
  function certLabel(cert) { var c = CBM[cert]; return c ? (c.label[lng()] || c.label.fr) : cert; }
  function certHint(cert) { var c = CBM[cert]; return c ? (c.hint[lng()] || c.hint.fr) : ''; }
  function diffLabel(d) { var x = DIFF_LABEL[d]; return x ? (x[lng()] || x.fr) : d; }

  /* ---------- SHA-256 autonome (compatible file://) ---------- */
  function sha256(ascii) {
    function rr(n, x) { return (x >>> n) | (x << (32 - n)); }
    var H = [0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19];
    var K = [0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2];
    var i, j, w = [], a, b, c, d, e, f, g, h, t1, t2, bytes = [], l;
    for (i = 0; i < ascii.length; i++) {
      var cc = ascii.charCodeAt(i);
      if (cc < 128) bytes.push(cc);
      else if (cc < 2048) { bytes.push(192 | (cc >> 6), 128 | (cc & 63)); }
      else { bytes.push(224 | (cc >> 12), 128 | ((cc >> 6) & 63), 128 | (cc & 63)); }
    }
    l = bytes.length; bytes.push(0x80);
    while (bytes.length % 64 !== 56) bytes.push(0);
    var bl = l * 8;
    for (i = 7; i >= 0; i--) bytes.push((bl / Math.pow(2, i * 8)) & 0xff);
    for (j = 0; j < bytes.length; j += 64) {
      for (i = 0; i < 16; i++) w[i] = (bytes[j + i * 4] << 24) | (bytes[j + i * 4 + 1] << 16) | (bytes[j + i * 4 + 2] << 8) | (bytes[j + i * 4 + 3]);
      for (i = 16; i < 64; i++) { var s0 = rr(7, w[i-15]) ^ rr(18, w[i-15]) ^ (w[i-15] >>> 3); var s1 = rr(17, w[i-2]) ^ rr(19, w[i-2]) ^ (w[i-2] >>> 10); w[i] = (w[i-16] + s0 + w[i-7] + s1) | 0; }
      a=H[0];b=H[1];c=H[2];d=H[3];e=H[4];f=H[5];g=H[6];h=H[7];
      for (i = 0; i < 64; i++) { var S1=rr(6,e)^rr(11,e)^rr(25,e); var ch=(e&f)^(~e&g); t1=(h+S1+ch+K[i]+w[i])|0; var S0=rr(2,a)^rr(13,a)^rr(22,a); var maj=(a&b)^(a&c)^(b&c); t2=(S0+maj)|0; h=g;g=f;f=e;e=(d+t1)|0;d=c;c=b;b=a;a=(t1+t2)|0; }
      H[0]=(H[0]+a)|0;H[1]=(H[1]+b)|0;H[2]=(H[2]+c)|0;H[3]=(H[3]+d)|0;H[4]=(H[4]+e)|0;H[5]=(H[5]+f)|0;H[6]=(H[6]+g)|0;H[7]=(H[7]+h)|0;
    }
    var out = '';
    for (i = 0; i < 8; i++) for (j = 7; j >= 0; j--) out += ((H[i] >>> (j * 4)) & 0xf).toString(16);
    return out;
  }

  /* ---------- Note ---------- */
  function maxRaw(n) { return 3 * n; }
  function note20(raw, n) { return Math.max(0, Math.min(20, raw / maxRaw(n) * 20)); }

  /* ---------- Mélange (Fisher-Yates) -> tableau d'indices permutés ---------- */
  function shuffledIndices(len) {
    var a = [], i;
    for (i = 0; i < len; i++) a.push(i);
    for (i = len - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }

  /* ---------- Signature (mêmes données côté QCM et côté correction) ---------- */
  function signatureBase(meta, answers) {
    var head = [meta.Nom, meta.Prenom, meta.Email, meta.DateDebut, meta.DateFin, meta.DureeSec, meta.NbQuestions, SALT];
    var body = answers.map(function (a) {
      return [a.ordre, a.id, (a.permutation || []).join('|'), a.indexOriginal, a.certitude].join('|');
    });
    return head.concat(body).join('||');
  }
  function signature(meta, answers) { return sha256(signatureBase(meta, answers)); }

  /* ---------- Construction du CSV (3 sections + certitude) ---------- */
  function buildCsv(meta, answers) {
    var sig = signature(meta, answers);
    var L = [];
    L.push('# ' + CSV_VERSION);
    L.push('# SECTION: METADATA');
    L.push('Cle;Valeur');
    ['Nom','Prenom','Email','DateDebut','DateFin','DureeSec','NbQuestions'].forEach(function (k) { L.push(k + ';' + csvCell(meta[k])); });
    L.push('');
    L.push('# SECTION: REPONSES');
    L.push('Ordre;QuestionId;Difficulte;Chapitre;Permutation;LettreChoisie;IndexOriginalChoisi;Certitude');
    answers.forEach(function (a) {
      L.push([a.ordre, a.id, a.difficulte, a.chapitre, (a.permutation || []).join('|'), a.lettre, a.indexOriginal, a.certitude].map(csvCell).join(';'));
    });
    L.push('');
    L.push('# SECTION: SIGNATURE');
    L.push('Cle;Valeur');
    L.push('SHA256;' + sig);
    return { csv: '﻿' + L.join('\r\n') + '\r\n', signature: sig };
  }
  function csvCell(v) { var s = (v === null || v === undefined) ? '' : String(v); return /[";\r\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; }

  /* ---------- Lecture du CSV ---------- */
  function parseCsv(text) {
    text = text.replace(/^﻿/, '');
    var lines = text.split(/\r?\n/);
    var section = '', meta = {}, answers = [], sigVal = '';
    var repHeader = null;
    for (var i = 0; i < lines.length; i++) {
      var line = lines[i];
      if (line === '' ) continue;
      if (line.charAt(0) === '#') {
        if (/METADATA/.test(line)) section = 'meta';
        else if (/REPONSES/.test(line)) section = 'rep';
        else if (/SIGNATURE/.test(line)) section = 'sig';
        continue;
      }
      var cells = splitCsvLine(line);
      if (section === 'meta') { if (cells[0] === 'Cle') continue; meta[cells[0]] = cells[1]; }
      else if (section === 'rep') {
        if (!repHeader) { repHeader = cells; continue; }
        var o = {};
        repHeader.forEach(function (h, idx) { o[h] = cells[idx]; });
        answers.push({
          ordre: o.Ordre, id: o.QuestionId, difficulte: o.Difficulte, chapitre: o.Chapitre,
          permutation: (o.Permutation || '').split('|').filter(function (x) { return x !== ''; }),
          lettre: o.LettreChoisie, indexOriginal: o.IndexOriginalChoisi, certitude: o.Certitude
        });
      } else if (section === 'sig') { if (cells[0] === 'SHA256') sigVal = cells[1]; }
    }
    return { metadata: meta, answers: answers, signature: sigVal };
  }
  function splitCsvLine(line) {
    var out = [], cur = '', q = false, i;
    for (i = 0; i < line.length; i++) {
      var ch = line[i];
      if (q) { if (ch === '"') { if (line[i+1] === '"') { cur += '"'; i++; } else q = false; } else cur += ch; }
      else { if (ch === '"') q = true; else if (ch === ';') { out.push(cur); cur = ''; } else cur += ch; }
    }
    out.push(cur); return out;
  }

  /* ---------- Vérification de la signature ---------- */
  function verify(parsed) {
    var meta = {
      Nom: parsed.metadata.Nom, Prenom: parsed.metadata.Prenom, Email: parsed.metadata.Email,
      DateDebut: parsed.metadata.DateDebut, DateFin: parsed.metadata.DateFin,
      DureeSec: parsed.metadata.DureeSec, NbQuestions: parsed.metadata.NbQuestions
    };
    var ans = parsed.answers.map(function (a) {
      return { ordre: a.ordre, id: a.id, permutation: a.permutation, indexOriginal: a.indexOriginal, certitude: a.certitude };
    });
    return signature(meta, ans) === (parsed.signature || '').toLowerCase();
  }

  /* ---------- Scoring CBM ---------- */
  function scoreSubmission(parsed, corrections) {
    var key = {};
    corrections.forEach(function (c) { key[c.id] = c; });
    var raw = 0, nbCorrect = 0, nbAnswered = 0;
    var calib = { good: 0, over: 0, under: 0, eleveeTotal: 0, faibleTotal: 0, moyenneTotal: 0 };
    var per = [];
    parsed.answers.forEach(function (a) {
      var corr = key[a.id] || {};
      var answered = a.indexOriginal !== '' && a.indexOriginal !== undefined && a.indexOriginal !== null && a.certitude;
      var idx = answered ? parseInt(a.indexOriginal, 10) : null;
      var ok = answered && idx === corr.bonne_reponse_index;
      var cert = a.certitude || 'moyenne';
      var pts = 0;
      if (answered) {
        nbAnswered++;
        pts = CBM[cert][ok ? 'ok' : 'no'];
        if (ok) nbCorrect++;
        if (cert === 'elevee') { calib.eleveeTotal++; ok ? calib.good++ : calib.over++; }
        else if (cert === 'faible') { calib.faibleTotal++; if (ok) calib.under++; }
        else calib.moyenneTotal++;
      }
      raw += pts;
      per.push({ id: a.id, chapitre: a.chapitre, difficulte: a.difficulte, certitude: a.certitude || '',
                 answered: answered, ok: ok, points: pts, indexOriginal: idx, bonne: corr.bonne_reponse_index });
    });
    var n = corrections.length || parsed.answers.length;
    return { raw: raw, n: n, note: note20(raw, n), maxRaw: maxRaw(n),
             nbCorrect: nbCorrect, nbAnswered: nbAnswered, calib: calib, per: per };
  }

  /* ---------- Utilitaires ---------- */
  function normalizeForFilename(s) {
    return (s || '').normalize ? (s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^A-Za-z0-9]/g, '') : (s || '').replace(/[^A-Za-z0-9]/g, '');
  }
  function mention(note) {
    if (lng() === 'en') {
      if (note >= 16) return 'Excellent'; if (note >= 14) return 'Very good';
      if (note >= 12) return 'Good'; if (note >= 10) return 'Pass'; return 'Insufficient';
    }
    if (note >= 16) return 'Très bien'; if (note >= 14) return 'Bien';
    if (note >= 12) return 'Assez bien'; if (note >= 10) return 'Passable'; return 'Insuffisant';
  }
  function fmt(n) { return (Math.round(n * 100) / 100).toString().replace('.', lng() === 'en' ? '.' : ','); }

  /* ---------- Rappel du barème (HTML, réutilisé par les pages) — bilingue ---------- */
  function baremeHtml() {
    if (lng() === 'en') {
      return '<table class="bareme-table"><thead><tr><th>Your certainty</th><th>✅ Correct</th><th>❌ Wrong</th></tr></thead><tbody>'
        + '<tr><td><strong>High</strong> <span class="bareme-muted">(certain)</span></td><td class="bareme-pos">+3</td><td class="bareme-neg">−3</td></tr>'
        + '<tr><td><strong>Medium</strong> <span class="bareme-muted">(fairly sure)</span></td><td class="bareme-pos">+2</td><td class="bareme-neg">−2</td></tr>'
        + '<tr><td><strong>Low</strong> <span class="bareme-muted">(guessing)</span></td><td class="bareme-pos">+1</td><td>0</td></tr>'
        + '</tbody></table>'
        + '<p class="bareme-note"><strong>Certainty-based marking (strict CBM).</strong> Score /20 = raw score ÷ (3 × number of questions) × 20. Difficulty (question colour) is <em>indicative</em> and does not change the score. '
        + '<strong>Honest strategy:</strong> "Low" if you guess, "Medium" if fairly sure, "High" only if you are truly certain — a wrong high-certainty answer costs −3.</p>';
    }
    return '<table class="bareme-table"><thead><tr><th>Votre certitude</th><th>✅ Bonne réponse</th><th>❌ Mauvaise réponse</th></tr></thead><tbody>'
      + '<tr><td><strong>Élevée</strong> <span class="bareme-muted">(certain)</span></td><td class="bareme-pos">+3</td><td class="bareme-neg">−3</td></tr>'
      + '<tr><td><strong>Moyenne</strong> <span class="bareme-muted">(assez sûr)</span></td><td class="bareme-pos">+2</td><td class="bareme-neg">−2</td></tr>'
      + '<tr><td><strong>Faible</strong> <span class="bareme-muted">(je devine)</span></td><td class="bareme-pos">+1</td><td>0</td></tr>'
      + '</tbody></table>'
      + '<p class="bareme-note"><strong>Notation par degré de certitude (CBM strict).</strong> Note /20 = score brut ÷ (3 × nombre de questions) × 20. La difficulté (couleur des questions) est <em>indicative</em> et ne change pas le score. '
      + '<strong>Stratégie honnête :</strong> « Faible » si vous devinez, « Moyenne » si assez sûr, « Élevée » seulement si vous êtes vraiment certain — car une certitude élevée erronée coûte −3.</p>';
  }

  return {
    baremeHtml: baremeHtml, lng: lng,
    certLabel: certLabel, certHint: certHint, diffLabel: diffLabel,
    SALT: SALT, CSV_VERSION: CSV_VERSION, LETTERS: LETTERS, CBM: CBM, CERT_ORDER: CERT_ORDER,
    DIFF_COLOR: DIFF_COLOR, DIFF_LABEL: DIFF_LABEL,
    sha256: sha256, maxRaw: maxRaw, note20: note20, shuffledIndices: shuffledIndices,
    signatureBase: signatureBase, signature: signature, buildCsv: buildCsv, parseCsv: parseCsv,
    verify: verify, scoreSubmission: scoreSubmission, normalizeForFilename: normalizeForFilename,
    mention: mention, fmt: fmt
  };
})();
