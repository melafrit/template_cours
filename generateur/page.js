/* =================================================================
   page.js : l'interface du générateur (generateur/index.html).

   Chaque champ du formulaire porte data-champ (un chemin dans l'état du cours, « cours.titre ») ou data-valeur (un
   chemin dans les valeurs habituelles, « hebergement.url_base »). À chaque saisie, le prompt se refait, et le
   brouillon se garde dans ce navigateur (localStorage, une commodité : la page marche sans). Les valeurs habituelles,
   elles, vivent dans valeurs.local.js, que la page ne peut pas écrire : « Enregistrer » le télécharge. Les points à
   vérifier (promotion, bloc, module, Jour 1 proche, consigne glissée dans un champ court) s'affichent au-dessus du
   prompt, refaits eux aussi à chaque saisie.
   ================================================================= */
(function () {
  'use strict';
  var G = window.GENERATEUR;
  var CLE = 'generateur-cours:brouillon';
  var V = G.valeurs(window.VALEURS_HABITUELLES);
  // Un brouillon d'une version plus ancienne de la page n'a pas tous les champs : completer() les ajoute.
  var etat = G.completer(lireBrouillon() || G.etatInitial(V, new Date()), V, new Date());

  function lireBrouillon() {
    try {
      var b = JSON.parse(window.localStorage.getItem(CLE) || 'null');
      return b && b.etat ? (b.valeurs && (V = G.valeurs(b.valeurs)), b.etat) : null;
    } catch (e) { return null; }
  }
  function garderBrouillon() {
    try { window.localStorage.setItem(CLE, JSON.stringify({ etat: etat, valeurs: V })); } catch (e) { /* sans stockage */ }
  }

  function lire(o, chemin) {
    return chemin.split('.').reduce(function (x, k) { return x == null ? undefined : x[k]; }, o);
  }
  function ecrire(o, chemin, v) {
    var ks = chemin.split('.');
    for (var i = 0; i < ks.length - 1; i++) {
      if (o[ks[i]] == null) o[ks[i]] = /^\d+$/.test(ks[i + 1]) ? [] : {};
      o = o[ks[i]];
    }
    o[ks[ks.length - 1]] = v;
  }

  // ---------------------------------------------------------------- les filières
  function options() {
    var l = [{ v: '', t: 'Aucune filière' }];
    Object.keys(V.filieres || {}).forEach(function (paire) {
      var membres = V.filieres[paire] || [];
      if (membres.length > 1) l.push({ v: paire, t: paire });
      membres.forEach(function (f) { l.push({ v: paire + '|' + f.id, t: f.code + ' seule' }); });
    });
    return l;
  }
  function choisirFilieres(valeur) {
    etat.paire = valeur;
    if (!valeur) { etat.filieres = []; return; }
    var morceaux = valeur.split('|');
    var toutes = G.filieresDeLaPaire(V, morceaux[0], etat.cours.racine);
    etat.filieres = morceaux[1] ? toutes.filter(function (f) { return f.id === morceaux[1]; }) : toutes;
  }
  var CHAMPS_FILIERE = [
    ['code', 'Sigle'], ['nom', 'Titre RNCP'], ['court', 'Nom court'], ['rncp', 'RNCP'], ['palette', 'Palette'],
    ['epreuve', 'Épreuve (EC…)'], ['bloc', 'Bloc'], ['module', 'Module (FM…)'],
    ['page_epreuves', 'Page des épreuves (https://…)'], ['fiche_module', 'Fiche module (chemin)'],
    ['grille', "Grille d'évaluation (chemin)"], ['promotion_app', 'Promotion exacte (Année › Promotion)'],
    ['matiere_app', 'Matière exacte dans Livrables'], ['fil_rouge', 'Projet fil rouge de la filière (en quelques mots)']
  ];
  function dessinerFilieres() {
    var boite = document.getElementById('filieres');
    boite.innerHTML = '';
    etat.filieres.forEach(function (f, i) {
      var carte = document.createElement('fieldset');
      carte.className = 'filiere';
      var titre = document.createElement('legend');
      titre.textContent = 'Filière ' + (f.code || f.id);
      carte.appendChild(titre);
      CHAMPS_FILIERE.forEach(function (c) {
        var lab = document.createElement('label');
        lab.textContent = c[1];
        var champ;
        if (c[0] === 'palette') {
          champ = document.createElement('select');
          ['', 'marine', 'emeraude', 'prune', 'ardoise', 'bordeaux'].forEach(function (p) {
            var o = document.createElement('option');
            o.value = p;
            o.textContent = p || 'à choisir';
            champ.appendChild(o);
          });
        } else {
          champ = document.createElement('input');
          champ.type = 'text';
        }
        champ.setAttribute('data-champ', 'filieres.' + i + '.' + c[0]);
        lab.appendChild(champ);
        carte.appendChild(lab);
      });
      boite.appendChild(carte);
    });
    relier(boite);
    remplir(boite);
  }

  // ---------------------------------------------------------------- le formulaire
  function remplir(portee) {
    (portee || document).querySelectorAll('[data-champ],[data-valeur]').forEach(function (el) {
      var champ = el.getAttribute('data-champ'), cible = champ ? etat : V;
      var chemin = champ || el.getAttribute('data-valeur');
      var v = lire(cible, chemin);
      if (el.type === 'checkbox') el.checked = !!v;
      else if (el.getAttribute('data-liste') === 'lignes') el.value = (v || []).join('\n');
      else el.value = v == null ? '' : v;
    });
  }
  function relier(portee) {
    (portee || document).querySelectorAll('[data-champ],[data-valeur]').forEach(function (el) {
      if (el.dataset.relie) return;
      el.dataset.relie = '1';
      el.addEventListener(el.type === 'checkbox' || el.tagName === 'SELECT' ? 'change' : 'input', function () {
        var champ = el.getAttribute('data-champ'), cible = champ ? etat : V;
        var chemin = champ || el.getAttribute('data-valeur');
        var v = el.type === 'checkbox' ? el.checked
          : el.getAttribute('data-liste') === 'lignes' ? el.value.split('\n').map(function (x) { return x.trim(); }).filter(Boolean)
          : el.value;
        ecrire(cible, chemin, v);
        if (chemin === 'cours.racine' && etat.paire) { choisirFilieres(etat.paire); dessinerFilieres(); }
        rafraichir();
      });
    });
  }

  // Les valeurs déduites (slug, dépôt, adresse, répertoire) s'affichent en indication tant que le champ est vide.
  function indications() {
    var p = G.parametres(etat, V);
    var ind = {
      'cours.slug': p.cours.slug, 'git.depot': p.git.depot,
      'modules.deploiement.url': p.modules.deploiement.url,
      'modules.deploiement.repertoire_distant': p.modules.deploiement.repertoire_distant
    };
    Object.keys(ind).forEach(function (k) {
      var el = document.querySelector('[data-champ="' + k + '"]');
      if (el) el.placeholder = ind[k] ? 'déduit : ' + ind[k] : '';
    });
  }

  function rafraichir() {
    var maintenant = new Date();
    document.getElementById('prompt').value = G.construirePrompt(etat, V, maintenant);
    var points = G.verifications(etat, V, maintenant).filter(function (x) { return x.page; });
    var boite = document.getElementById('points'), ul = boite.querySelector('ul');
    ul.innerHTML = '';
    points.forEach(function (x) {
      var li = document.createElement('li');
      li.textContent = x.page;
      ul.appendChild(li);
    });
    boite.hidden = !points.length;
    indications();
    garderBrouillon();
  }

  function annoncer(t) {
    var m = document.getElementById('message');
    m.textContent = t;
    window.setTimeout(function () { if (m.textContent === t) m.textContent = ''; }, 4000);
  }

  function telecharger(nom, texte, type) {
    var lien = document.createElement('a');
    lien.href = URL.createObjectURL(new Blob([texte], { type: type + ';charset=utf-8' }));
    lien.download = nom;
    document.body.appendChild(lien);
    lien.click();
    window.setTimeout(function () { URL.revokeObjectURL(lien.href); lien.remove(); }, 0);
  }

  function copier() {
    var zone = document.getElementById('prompt'), texte = zone.value;
    var repli = function () {
      zone.focus();
      zone.select();
      try { document.execCommand('copy'); annoncer('Prompt copié.'); }
      catch (e) { annoncer('Copie impossible : sélectionnez le texte et copiez-le à la main.'); }
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(texte).then(function () { annoncer('Prompt copié.'); }, repli);
    } else {
      repli();
    }
  }

  // Les habitudes que l'on garde d'un cours à l'autre, prises dans le formulaire.
  function valeursAEnregistrer() {
    var h = Object.assign({}, V.habitudes, {
      palette: etat.cours.palette, horaires: etat.cours.horaires, ton: etat.cours.ton,
      langues: G.parametres(etat, V).cours.langues, modules: etat.modules
    });
    var dep = Object.assign({}, h.modules.deploiement, { url: '', repertoire_distant: '', zones_protegees: '' });
    h.modules = Object.assign({}, h.modules, { deploiement: dep, tp: Object.assign({}, h.modules.tp, { sujet: '' }) });
    return Object.assign({}, V, { habitudes: h, ecosysteme: etat.ecosysteme, dossier_documents: etat.dossier.documents });
  }

  function demarrer() {
    if (!window.VALEURS_HABITUELLES) document.getElementById('sans-valeurs').hidden = false;
    var sel = document.getElementById('paire');
    options().forEach(function (o) {
      var el = document.createElement('option');
      el.value = o.v;
      el.textContent = o.t;
      sel.appendChild(el);
    });
    sel.value = etat.paire || '';
    sel.addEventListener('change', function () { choisirFilieres(sel.value); dessinerFilieres(); rafraichir(); });
    relier();
    remplir();
    dessinerFilieres();
    document.getElementById('copier').addEventListener('click', copier);
    document.getElementById('telecharger').addEventListener('click', function () {
      var nom = 'prompt-lancement-' + (G.parametres(etat, V).cours.slug || 'cours') + '.md';
      telecharger(nom, document.getElementById('prompt').value + '\n', 'text/markdown');
      annoncer('Prompt téléchargé : ' + nom + '.');
    });
    document.getElementById('enregistrer').addEventListener('click', function () {
      telecharger('valeurs.local.js', G.fichierValeurs(valeursAEnregistrer()), 'text/javascript');
      annoncer('valeurs.local.js téléchargé : placez-le dans le dossier generateur/, à la place de l\'ancien.');
    });
    document.getElementById('recommencer').addEventListener('click', function () {
      try { window.localStorage.removeItem(CLE); } catch (e) { /* sans stockage */ }
      V = G.valeurs(window.VALEURS_HABITUELLES);
      etat = G.etatInitial(V, new Date());
      sel.value = '';
      remplir();
      dessinerFilieres();
      rafraichir();
      annoncer('Brouillon vidé : la page repart de vos valeurs habituelles.');
    });
    rafraichir();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', demarrer);
  else demarrer();
})();
