/* =================================================================
   generateur.js : le générateur du prompt de lancement d'un cours (lot 8).

   Une page locale, ouverte d'un double clic (file://), jamais publiée, hors de site/ et jamais recopiée dans un
   cours. Elle lit les valeurs habituelles de l'auteur dans valeurs.local.js (ignoré par Git, sans aucun secret) et
   fabrique le prompt de lancement : il renvoie au tronc et aux modules du gabarit par leur chemin, pour rester à jour
   quand ils changent, avec le bloc de paramètres du tronc rempli (décisions de l'auteur du 21 et du 22 novembre
   2026). Un dossier de cours déjà préparé garde ses documents en place, exclus de Git et des recherches.

   construirePrompt() est une fonction pure : node peut la tester sans navigateur.
   ================================================================= */
(function (racine) {
  'use strict';

  var PALETTES = ['marine', 'emeraude', 'prune', 'ardoise', 'bordeaux'];

  // Les modules du gabarit, dans l'ordre de prompts/modules/.
  var MODULES = [
    { cle: 'langues', fichier: '01-langues.md' },
    { cle: 'polycopie', fichier: '02-polycopie.md' },
    { cle: 'podcasts', fichier: '03-podcasts-notebooklm.md' },
    { cle: 'audio', fichier: '04-audio-elevenlabs.md' },
    { cle: 'evaluations', fichier: '05-evaluations.md' },
    { cle: 'tp', fichier: '06-tp-correction.md' },
    { cle: 'ecole', fichier: '07-ypareo-livrables.md' },
    { cle: 'deploiement', fichier: '08-deploiement.md' },
    { cle: 'complements', fichier: '09-complements.md' },
    { cle: 'codex', fichier: '10-codex.md' }
  ];

  // Sans valeurs.local.js : des valeurs neutres, pour que la page s'ouvre quand même.
  var DEFAUTS = {
    auteur: 'Prénom NOM',
    email: 'prenom.nom@exemple.fr',
    github: 'compte',
    hebergement: { url_base: 'https://example.org/teaching/', repertoire_base: '/chemin/vers/teaching/' },
    dossier_cours_base: 'C:/projets/Cours/',
    dossier_documents: 'Doc_Reference',
    ecosysteme: { gabarit_technique: 'C:/projets/Cours/template_cours', cours_de_reference: [], app_livrables: '',
                  doc_import_app: '', epreuves_reelles: '' },
    filieres: {},
    habitudes: {
      palette: 'marine', langues: ['fr'], horaires: { matin: '09:00-12:30', apres_midi: '13:30-17:00' },
      ton: "vouvoiement chaleureux, registre d'un collègue expérimenté ; peu d'écrit, beaucoup de pratique",
      modules: {}
    }
  };

  // ---------------------------------------------------------------- petits outils
  function copie(o) { return o == null ? o : JSON.parse(JSON.stringify(o)); }
  function sansAccents(s) { return String(s || '').normalize('NFD').replace(/[\u0300-\u036f]/g, ''); }
  function fabriquerSlug(s) {
    return sansAccents(s).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
  }
  function anneeScolaire(d) {
    var y = d.getFullYear();
    return d.getMonth() >= 7 ? y + '-' + (y + 1) : (y - 1) + '-' + y;
  }
  function barres(chemin) { return String(chemin || '').replace(/\\/g, '/'); }
  function nomDuDossier(chemin) { return barres(chemin).replace(/\/+$/, '').split('/').pop(); }
  function joindre(base, suite) {
    base = String(base || '');
    if (!base) return suite;
    return base.replace(/\/*$/, '/') + String(suite || '').replace(/^\/+/, '');
  }
  function liste(texte) {
    return String(texte || '').split(/[,\n;]/).map(function (x) { return x.trim(); }).filter(Boolean);
  }
  function texteDans(d, langue) {
    if (d && typeof d === 'object') return d[langue] || d.fr || '';
    return d || '';
  }

  // ---------------------------------------------------------------- les valeurs et l'état
  function valeurs(v) {
    var V = copie(DEFAUTS);
    v = v || {};
    Object.keys(v).forEach(function (k) {
      if (v[k] && typeof v[k] === 'object' && !Array.isArray(v[k]) && V[k] && typeof V[k] === 'object') {
        V[k] = Object.assign({}, V[k], copie(v[k]));
      } else {
        V[k] = copie(v[k]);
      }
    });
    V.habitudes = Object.assign({}, DEFAUTS.habitudes, copie((v || {}).habitudes || {}));
    return V;
  }

  // Les modules et leurs réglages par défaut : ceux du tronc, puis les habitudes de l'auteur.
  function modulesParDefaut(habitudes) {
    var m = {
      polycopie: { actif: false },
      podcasts: { actif: false, episodes: 0, diaporamas: true },
      audio: { actif: true, capsules: '' },
      evaluations: { qcm_en_ligne: true, qcm_papier: false, qcm_entrainement: true, correction_publique: true,
                     points_de_controle: true },
      tp: { actif: false, sujet: '' },
      ecole: { ypareo: true, livrables_app: true, bouton_qcm: true },
      deploiement: { actif: true, url: '', repertoire_distant: '', zones_protegees: '' },
      complements: { schemas: true, illustrations: false, simulateurs: '', glossaire: true, boite_a_outils: false,
                     fiches_memo: false }
    };
    var h = (habitudes && habitudes.modules) || {};
    Object.keys(h).forEach(function (k) { m[k] = Object.assign({}, m[k] || {}, copie(h[k])); });
    return m;
  }

  function etatInitial(v, maintenant) {
    var V = valeurs(v);
    var h = V.habitudes;
    var langues = h.langues && h.langues.length ? h.langues : ['fr'];
    return {
      cours: {
        titre: '', slug: '', code_module: '', bloc: '', annee: anneeScolaire(maintenant || new Date()),
        palette: h.palette || 'marine', racine: langues[0],
        jumelles: { en: langues.indexOf('en') > 0, ar: langues.indexOf('ar') > 0 },
        public: '', formats: '', format_impose: '', dates: '',
        horaires: copie(h.horaires), ton: h.ton
      },
      dossier: { chemin: barres(V.dossier_cours_base), documents: V.dossier_documents || 'Doc_Reference', existe: true },
      paire: '',
      filieres: [],
      fil_rouge: { nom: '', source: '' },
      interdits: '',
      livrables: '',
      modules: modulesParDefaut(h),
      ecosysteme: copie(V.ecosysteme),
      git: { depot: '' }
    };
  }

  // Une paire habituelle (« CDWFS et ASRC ») devient des filières à compléter pour ce cours.
  function filieresDeLaPaire(v, paire, langue) {
    var V = valeurs(v);
    return ((V.filieres || {})[paire] || []).map(function (f) {
      return {
        id: f.id || '', code: f.code || '', nom: texteDans(f.nom, langue), court: texteDans(f.court, langue),
        rncp: f.rncp || '', palette: f.palette || '', epreuve: '', bloc: '', module: '', page_epreuves: '',
        fiche_module: '', grille: '', promotion_app: '', matiere_app: ''
      };
    });
  }

  // ---------------------------------------------------------------- le YAML du bloc de paramètres
  function chaine(s) { return '"' + String(s == null ? '' : s).replace(/\\/g, '\\\\').replace(/"/g, '\\"') + '"'; }
  function scalaire(x) {
    if (typeof x === 'boolean') return x ? 'true' : 'false';
    if (typeof x === 'number') return String(x);
    return chaine(x);
  }
  function enLigne(x) {
    if (Array.isArray(x)) return '[' + x.map(enLigne).join(', ') + ']';
    if (x && typeof x === 'object') {
      return '{' + Object.keys(x).map(function (k) { return k + ': ' + enLigne(x[k]); }).join(', ') + '}';
    }
    return scalaire(x);
  }
  function yaml(x, retrait) {
    retrait = retrait || '';
    var lignes = [];
    Object.keys(x).forEach(function (k) {
      var v = x[k];
      if (Array.isArray(v) && v.length && v[0] && typeof v[0] === 'object') {
        lignes.push(retrait + k + ':');
        v.forEach(function (el) {
          var corps = yaml(el, retrait + '    ').split('\n');
          lignes.push(retrait + '  - ' + corps[0].replace(/^\s+/, ''));
          corps.slice(1).forEach(function (l) { lignes.push(l); });
        });
      } else if (v && typeof v === 'object' && !Array.isArray(v) && Object.keys(v).length) {
        lignes.push(retrait + k + ':');
        lignes.push(yaml(v, retrait + '  '));
      } else {
        lignes.push(retrait + k + ': ' + enLigne(v));
      }
    });
    return lignes.join('\n');
  }

  // ---------------------------------------------------------------- les paramètres, puis le prompt
  function langues(c) {
    var l = [c.racine || 'fr'];
    ['en', 'ar'].forEach(function (x) { if (c.jumelles && c.jumelles[x] && l.indexOf(x) < 0) l.push(x); });
    return l;
  }

  function parametres(etat, v) {
    var V = valeurs(v);
    var c = etat.cours, m = etat.modules, slug = c.slug || fabriquerSlug(c.titre);
    var calendrier = {};
    liste(c.dates).forEach(function (d, i) { calendrier['jour_' + (i + 1)] = d; });
    var dep = m.deploiement || {};
    return {
      cours: {
        titre: c.titre, slug: slug, auteur: V.auteur, code_module: c.code_module, bloc: c.bloc, annee: c.annee,
        palette: c.palette, langues: langues(c), public: c.public, formats: liste(c.formats),
        format_impose: c.format_impose, calendrier: calendrier, horaires: c.horaires, ton: c.ton
      },
      filieres: etat.filieres.map(function (f) {
        return { id: f.id, code: f.code, nom: f.nom, court: f.court, rncp: f.rncp, palette: f.palette, competences: [],
                 epreuve: f.epreuve, bloc: f.bloc, module: f.module, page_epreuves: f.page_epreuves,
                 fiche_module: f.fiche_module, grille: f.grille, promotion_app: f.promotion_app,
                 matiere_app: f.matiere_app };
      }),
      groupe_mixte: etat.filieres.length > 1,
      fil_rouge: { nom: etat.fil_rouge.nom, source: etat.fil_rouge.source, projet_par_filiere: {},
                   referentiel: 'outils/referentiel.py' },
      interdits: liste(etat.interdits),
      livrables: [],
      malus_version_de_travail: 0,
      modules: {
        polycopie: { actif: !!m.polycopie.actif },
        podcasts: { actif: !!m.podcasts.actif, episodes: Number(m.podcasts.episodes) || 0,
                    diaporamas: !!m.podcasts.diaporamas },
        audio: { actif: !!m.audio.actif, capsules: liste(m.audio.capsules) },
        evaluations: {
          qcm_en_ligne: { actif: !!m.evaluations.qcm_en_ligne, notation: 'CBM', questions: 0 },
          qcm_papier: { actif: !!m.evaluations.qcm_papier, questions: 0, propositions: 4, certitude: '',
                        un_par_filiere: false },
          qcm_entrainement: { actif: !!m.evaluations.qcm_entrainement, questions_par_filiere: 0 },
          correction_publique: !!m.evaluations.correction_publique,
          points_de_controle: !!m.evaluations.points_de_controle
        },
        tp: { actif: !!m.tp.actif, sujet: m.tp.sujet || '' },
        ecole: { ypareo: !!m.ecole.ypareo, livrables_app: !!m.ecole.livrables_app, bouton_qcm: !!m.ecole.bouton_qcm },
        deploiement: {
          actif: !!dep.actif,
          url: dep.url || (slug ? joindre(V.hebergement.url_base, slug + '/') : ''),
          repertoire_distant: dep.repertoire_distant || (slug ? joindre(V.hebergement.repertoire_base, slug) : ''),
          zones_protegees: liste(dep.zones_protegees), site_protege: false
        },
        complements: {
          schemas: { actif: !!m.complements.schemas, capsule_par_schema: false },
          illustrations: { actif: !!m.complements.illustrations, outil: 'Codex' },
          simulateurs: liste(m.complements.simulateurs), glossaire: !!m.complements.glossaire,
          boite_a_outils: { actif: !!m.complements.boite_a_outils, fiches: 0 },
          fiches_memo: !!m.complements.fiches_memo, encarts_plus_loin: []
        }
      },
      ecosysteme: {
        gabarit_technique: barres(etat.ecosysteme.gabarit_technique),
        cours_de_reference: (etat.ecosysteme.cours_de_reference || []).map(barres),
        app_livrables: etat.ecosysteme.app_livrables || '',
        doc_import_app: barres(etat.ecosysteme.doc_import_app),
        epreuves_reelles: barres(etat.ecosysteme.epreuves_reelles)
      },
      git: {
        depot: etat.git.depot || (V.github && etat.dossier.chemin ? V.github + '/' + nomDuDossier(etat.dossier.chemin) : ''),
        prive: true,
        auteur: V.auteur + ' <' + V.email + '>',
        co_auteur: false
      }
    };
  }

  // Les modules à lire, d'après les paramètres : un module inactif ne se lit pas.
  function modulesActifs(p) {
    var m = p.modules, c = m.complements;
    var actif = {
      langues: p.cours.langues.length > 1,
      polycopie: m.polycopie.actif,
      podcasts: m.podcasts.actif,
      audio: m.audio.actif,
      evaluations: m.evaluations.qcm_en_ligne.actif || m.evaluations.qcm_papier.actif ||
                   m.evaluations.qcm_entrainement.actif || m.evaluations.points_de_controle,
      tp: m.tp.actif,
      ecole: m.ecole.ypareo || m.ecole.livrables_app,
      deploiement: m.deploiement.actif,
      complements: c.schemas.actif || c.illustrations.actif || c.simulateurs.length > 0 || c.glossaire ||
                   c.boite_a_outils.actif || c.fiches_memo,
      codex: c.illustrations.actif
    };
    return MODULES.filter(function (x) { return actif[x.cle]; });
  }

  function construirePrompt(etat, v) {
    var p = parametres(etat, v);
    var gabarit = p.ecosysteme.gabarit_technique || 'le gabarit';
    var dossier = barres(etat.dossier.chemin).replace(/\/+$/, '');
    var docs = String(etat.dossier.documents || '').replace(/^\/+|\/+$/g, '') || 'Doc_Reference';
    var actifs = modulesActifs(p);
    var L = [];
    L.push('Crée un nouveau cours avec le template de cours, en suivant son prompt paramétrable.');
    L.push('');
    L.push('1. Lis d\'abord, dans ' + gabarit + ' :');
    L.push('   - CLAUDE.md, dont les exigences de l\'auteur (§ 2) valent pour ce cours ;');
    L.push('   - prompts/PROMPT-Cours-parametrable.md, le tronc, en entier ;');
    if (actifs.length) {
      L.push('   - les modules actifs, chacun avant sa phase : ' +
             actifs.map(function (x) { return 'prompts/modules/' + x.fichier; }).join(', ') + '.');
    }
    L.push('');
    L.push('2. Le dossier du cours : ' + (dossier || '(à préciser)') + '.');
    if (etat.dossier.existe) {
      L.push('   Il existe déjà, et ses documents de référence sont dans ' + docs + '/.');
      L.push('   - Ne lance aucune recherche dans ce dossier tant que son .rgignore n\'exclut pas ' + docs + '/ :');
      L.push('     ouvre les documents un par un, par leur chemin.');
      L.push('   - Un fichier de configuration (.json) trouvé parmi les documents est un secret : ne l\'ouvre pas,');
      L.push('     signale-le à l\'auteur.');
      L.push('   - Ne déplace, ne renomme et ne modifie aucun document.');
      L.push('   - Lis tous les documents, en profondeur, avant la moindre question de cadrage.');
      L.push('   - À l\'étape zéro, écris cours.json dans le gabarit, avec « sortie » sur ce dossier, puis lance à la');
      L.push('     racine du gabarit python3 nouveau_cours.py --essai --ecraser, et enfin --ecraser : les documents');
      L.push('     et deploiement/config.json restent en place.');
      L.push('   - Aussitôt après, avant git init et avant toute recherche, ajoute ' + docs + '/ au .gitignore et au');
      L.push('     .rgignore du cours : les ouvrages y sont sous droits, et rien n\'en part dans Git.');
    } else {
      L.push('   Il n\'existe pas encore : nouveau_cours.py le crée. L\'auteur dépose ensuite les documents dans');
      L.push('   sources/, que Git ignore ; lis-les tous, en profondeur, avant la moindre question de cadrage.');
    }
    if (p.modules.complements.illustrations.actif) {
      L.push('');
      L.push('3. Les illustrations se font avec Codex : vérifie codex --version et codex login status. Sans Codex,');
      L.push('   donne la procédure du module 10 et arrête-toi avant les illustrations.');
    }
    L.push('');
    L.push((p.modules.complements.illustrations.actif ? '4' : '3') + '. Applique le tronc avec ces PARAMÈTRES. Un champ vide se déduit des documents');
    L.push('   ou se demande, une question à la fois.');
    if (String(etat.livrables || '').trim()) {
      L.push('   Les livrables déjà connus, à structurer au cadrage : ' + String(etat.livrables).trim().replace(/\s+/g, ' '));
    }
    L.push('');
    L.push('~~~yaml');
    L.push(yaml(p));
    L.push('~~~');
    L.push('');
    L.push('Commence par la phase 0 : ce qui est fourni, ce que tu déduis, ce qui reste ouvert, puis les questions');
    L.push('une à une, avec l\'outil de question à options cliquables.');
    return L.join('\n');
  }

  // Le fichier valeurs.local.js, d'après les valeurs actuelles : la page ne peut pas l'écrire elle-même.
  function fichierValeurs(v) {
    var V = valeurs(v);
    return '/* valeurs.local.js : les valeurs habituelles du générateur. Fichier local, ignoré par Git,\n' +
           '   jamais publié ; aucun secret, aucun mot de passe. Écrit par la page du générateur. */\n' +
           'window.VALEURS_HABITUELLES = ' + JSON.stringify(V, null, 2) + ';\n';
  }

  var API = {
    PALETTES: PALETTES, MODULES: MODULES, DEFAUTS: DEFAUTS, valeurs: valeurs, etatInitial: etatInitial,
    filieresDeLaPaire: filieresDeLaPaire, parametres: parametres, modulesActifs: modulesActifs,
    construirePrompt: construirePrompt, fichierValeurs: fichierValeurs, fabriquerSlug: fabriquerSlug,
    nomDuDossier: nomDuDossier
  };
  if (typeof module !== 'undefined' && module.exports) module.exports = API;
  else racine.GENERATEUR = API;
})(this);
