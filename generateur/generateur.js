/* =================================================================
   generateur.js : le générateur du prompt de lancement d'un cours (lot 8).

   Une page locale, ouverte d'un double clic (file://), jamais publiée, hors de site/ et jamais recopiée dans un
   cours. Elle lit les valeurs habituelles de l'auteur dans valeurs.local.js (ignoré par Git, sans aucun secret) et
   fabrique le prompt de lancement : il renvoie au tronc et aux modules du gabarit par leur chemin, pour rester à jour
   quand ils changent, avec le bloc de paramètres du tronc rempli (décisions de l'auteur du 21 et du 22 novembre
   2026). Un dossier de cours déjà préparé garde ses documents en place, exclus de Git et des recherches.

   Le premier usage réel (le cours de gestion de projet MOE, 22 novembre 2026) a fixé le reste. Les chemins Windows
   passent aux barres obliques et deviennent relatifs au dossier du cours. Les consignes de l'auteur vont en prose,
   jamais dans les valeurs du YAML, où Claude les aurait prises pour des données. Les secrets connus se nomment. Les
   incohérences (promotion, bloc, module) et un Jour 1 proche s'annoncent dans la page et dans le prompt.

   construirePrompt() et verifications() sont des fonctions pures : node peut les tester sans navigateur.
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

  var JOURS = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi'];
  var MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre',
              'novembre', 'décembre'];

  // Un Jour 1 à moins de deux semaines : le prompt fait d'abord demander ce qui doit être prêt.
  var JOURS_AVANT_URGENCE = 14;

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
  function barres(chemin) { return String(chemin == null ? '' : chemin).replace(/\\/g, '/'); }
  // « Copier en tant que chemin », dans l'Explorateur, met le chemin entre guillemets ; Windows les interdit dans un
  // nom de fichier : un champ de chemin peut les perdre sans risque.
  function chemin(s) { return barres(s).replace(/"/g, '').trim(); }
  function nomDuDossier(s) { return chemin(s).replace(/\/+$/, '').split('/').pop(); }
  function joindre(base, suite) {
    base = String(base || '');
    if (!base) return suite;
    return base.replace(/\/*$/, '/') + String(suite || '').replace(/^\/+/, '');
  }
  function liste(texte) {
    if (Array.isArray(texte)) return texte.map(function (x) { return String(x).trim(); }).filter(Boolean);
    return String(texte || '').split(/[,\n;]/).map(function (x) { return x.trim(); }).filter(Boolean);
  }
  function lignes(texte) {
    if (Array.isArray(texte)) return texte.map(function (x) { return String(x).trim(); }).filter(Boolean);
    return String(texte || '').split('\n').map(function (x) { return x.trim(); }).filter(Boolean);
  }
  function enumerer(l) { return l.length < 2 ? l.join('') : l.slice(0, -1).join(', ') + ' et ' + l[l.length - 1]; }
  function texteDans(d, langue) {
    if (d && typeof d === 'object') return d[langue] || d.fr || '';
    return d || '';
  }
  function echapper(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }
  function fusion(base, ajout) {
    if (!ajout || typeof ajout !== 'object' || Array.isArray(ajout)) return ajout === undefined ? base : ajout;
    var r = Array.isArray(base) ? base.slice() : Object.assign({}, base);
    Object.keys(ajout).forEach(function (k) {
      r[k] = base && typeof base[k] === 'object' && !Array.isArray(base[k]) ? fusion(base[k], ajout[k]) : ajout[k];
    });
    return r;
  }

  // Un chemin Windows prend des barres obliques ; un chemin pris dans le dossier du cours lui devient relatif, où
  // qu'il soit dans le texte. Le dossier cité seul reste entier : « ./ » se lirait mal dans une phrase.
  function relatif(s, dossier) {
    var t = barres(s);
    var d = barres(dossier).replace(/\/+$/, '');
    if (!t || !d) return t;
    return t.replace(new RegExp(echapper(d) + '/(?![\\s"\'\u00bb,;:)]|\\.(?:\\s|$)|$)', 'gi'), '');
  }
  function memeChemin(a, b) {
    var n = function (x) { return chemin(x).replace(/\/+$/, '').toLowerCase(); };
    return !!a && n(a) === n(b);
  }
  // Le champ part du dossier de base des cours : tant qu'il n'a pas reçu le nom du dossier, le cours n'en a pas.
  function dossierDuCours(etat, V) {
    var d = chemin((etat.dossier || {}).chemin).replace(/\/+$/, '');
    return d && !memeChemin(d, V.dossier_cours_base) ? d : '';
  }

  // « Bloc 04 » s'écrit « Bloc 4 », comme sur la pastille de l'accueil.
  function normaliserBloc(s) { return String(s || '').replace(/\b(bloc)\s+0+(\d)/gi, '$1 $2'); }
  function numero(s) { var m = String(s || '').match(/(\d+)/); return m ? String(Number(m[1])) : ''; }

  function dateLongue(iso) {
    var m = String(iso || '').match(/^(\d{4})-(\d{2})-(\d{2})$/);
    if (!m) return iso;
    var d = new Date(Number(m[1]), Number(m[2]) - 1, Number(m[3]));
    return JOURS[d.getDay()] + ' ' + Number(m[3]) + ' ' + MOIS[d.getMonth()] + ' ' + m[1];
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
      dossier: { chemin: barres(V.dossier_cours_base), documents: V.dossier_documents || 'Doc_Reference', existe: true,
                 secrets: '' },
      paire: '',
      filieres: [],
      fil_rouge: { nom: '', source: '' },
      consignes: { fil_rouge: '', tp: '', autres: '' },
      interdits: '',
      livrables: '',
      modules: modulesParDefaut(h),
      ecosysteme: copie(V.ecosysteme),
      git: { depot: '' }
    };
  }

  // Un brouillon d'une version plus ancienne de la page reçoit les champs qui lui manquent.
  function completer(etat, v, maintenant) { return fusion(etatInitial(v, maintenant), etat || {}); }

  // Une paire habituelle (« CDWFS et ASRC ») devient des filières à compléter pour ce cours.
  function filieresDeLaPaire(v, paire, langue) {
    var V = valeurs(v);
    return ((V.filieres || {})[paire] || []).map(function (f) {
      return {
        id: f.id || '', code: f.code || '', nom: texteDans(f.nom, langue), court: texteDans(f.court, langue),
        rncp: f.rncp || '', palette: f.palette || '', epreuve: '', bloc: '', module: '', page_epreuves: '',
        fiche_module: '', grille: '', promotion_app: '', matiere_app: '', fil_rouge: ''
      };
    });
  }

  // L'application Livrables nomme ses promotions « Année › Promotion » ; un autre nom ne s'y retrouverait pas.
  function promotionValide(p) { return /\S \u203a \S/.test(String(p || '')); }

  // ---------------------------------------------------------------- les points à vérifier
  // Chacun a son texte pour la page (court) et, quand Claude doit agir, sa consigne pour le prompt.
  function verifications(etat, v, maintenant) {
    etat = completer(etat, v, maintenant);
    var r = [];
    var c = etat.cours, fs = etat.filieres || [];
    var dossier = dossierDuCours(etat, valeurs(v));
    var nom = function (f) { return f.code || f.id; };

    var dates = liste(c.dates);
    if (dates.length) {
      var m = dates[0].match(/^(\d{4})-(\d{2})-(\d{2})$/);
      if (!m) {
        r.push({ page: 'La date « ' + dates[0] + ' » ne suit pas la forme AAAA-MM-JJ.' });
      } else {
        var auj = maintenant || new Date();
        var ecart = Math.round((new Date(Number(m[1]), Number(m[2]) - 1, Number(m[3])) -
                                new Date(auj.getFullYear(), auj.getMonth(), auj.getDate())) / 86400000);
        if (ecart >= 0 && ecart <= JOURS_AVANT_URGENCE) {
          var suite = dates.slice(1).map(function (d, i) { return 'le Jour ' + (i + 2) + ' le ' + dateLongue(d); });
          r.push({
            page: 'Le Jour 1 a lieu ' + (ecart === 0 ? 'aujourd\'hui' : ecart === 1 ? 'demain' : 'dans ' + ecart + ' jours') +
                  ' : le prompt fait d\'abord demander ce qui doit être prêt.',
            prompt: 'Le calendrier. Le Jour 1 a lieu le ' + dateLongue(dates[0]) + (suite.length ? ', ' + suite.join(', ') : '') +
                    '. Demande d\'abord à l\'auteur ce qui doit être prêt pour le Jour 1.',
            calendrier: true
          });
        }
      }
    }

    var tp = etat.modules.tp || {};
    if (tp.actif && /fil rouge/i.test(String(tp.sujet || '') + ' ' + String(etat.consignes.tp || ''))) {
      r.push({ page: 'Le TP porte sur le fil rouge : le prompt fait trancher comment le cours montre la méthode sans souffler les réponses.',
               prompt: 'Un point à trancher au cadrage. Le TP s\'applique au fil rouge du cours, alors que, selon ' +
                       'CLAUDE.md, rien ne souffle une réponse. Propose à l\'auteur comment le cours montre la méthode ' +
                       'sans donner les réponses du TP.' });
    }

    var mauvaises = fs.filter(function (f) { return f.promotion_app && !promotionValide(f.promotion_app); });
    if (mauvaises.length) {
      var dites = mauvaises.map(function (f) { return '« ' + f.promotion_app + ' » (' + nom(f) + ')'; });
      r.push({
        page: 'Promotion à préciser : ' + enumerer(dites) + '. L\'application attend « Année › Promotion », tel que sa liste l\'écrit.',
        prompt: 'Les promotions de l\'application Livrables. L\'auteur a indiqué ' + enumerer(dites) + ', alors que ' +
                'l\'application attend le nom exact « Année › Promotion » de sa liste : demande-le pour chaque ' +
                'filière avant d\'écrire le bloc école.'
      });
    }

    // Le bloc et le module du cours contre ceux des filières : une ligne par valeur différente, filières groupées.
    var ecarts = function (champ, duCours, egaux) {
      var groupes = {};
      fs.forEach(function (f) {
        var val = String(f[champ] || '').trim();
        if (val && String(duCours || '').trim() && !egaux(val, duCours)) (groupes[val] = groupes[val] || []).push(nom(f));
      });
      Object.keys(groupes).forEach(function (val) {
        var qui = groupes[val].length > 1 ? 'des filières ' + enumerer(groupes[val]) : 'de la filière ' + groupes[val][0];
        r.push({ page: 'Le ' + champ + ' du cours (« ' + duCours + ' ») diffère de celui ' + qui + ' (« ' + val + ' »).',
                 prompt: 'Le ' + champ + ' du cours (« ' + duCours + ' ») et celui ' + qui + ' (« ' + val + ' ») ' +
                         'diffèrent : demande à l\'auteur si c\'est voulu, et sinon lequel garder.' });
      });
    };
    ecarts('bloc', c.bloc, function (a, b) { return numero(a) === numero(b); });
    ecarts('module', c.code_module, function (a, b) { return a.toUpperCase() === String(b).trim().toUpperCase(); });
    if (/\bbloc\s+0\d/i.test([c.bloc].concat(fs.map(function (f) { return f.bloc; })).join(' '))) {
      r.push({ page: '« Bloc 0N » s\'écrit « Bloc N » dans le prompt, comme sur la pastille de l\'accueil.' });
    }

    // Une phrase dans un champ court finirait dans le YAML, où Claude la prendrait pour une donnée.
    var longs = [['Fil rouge', etat.fil_rouge.nom], ['Sa source', etat.fil_rouge.source],
                 ['Sujet du TP', tp.actif ? tp.sujet : '']]
      .concat(fs.map(function (f) { return ['Projet fil rouge de ' + nom(f), f.fil_rouge]; }))
      .filter(function (x) { return relatif(x[1], dossier).length > 100; })
      .map(function (x) { return '« ' + x[0] + ' »'; });
    if (longs.length) {
      r.push({ page: (longs.length > 1 ? 'Les champs ' + enumerer(longs) + ' ressemblent à des consignes : écrivez-les'
                                       : 'Le champ ' + longs[0] + ' ressemble à une consigne : écrivez-la') +
                     ' plutôt dans les consignes, en prose ; le YAML ne garde que des valeurs.' });
    }

    if (fs.some(function (f) { return f.page_epreuves; })) {
      r.push({ prompt: 'La page des épreuves s\'ouvre et se vérifie avant d\'être ajoutée.' });
    }
    return r;
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
    var sortie = [];
    Object.keys(x).forEach(function (k) {
      var v = x[k];
      if (Array.isArray(v) && v.length && v[0] && typeof v[0] === 'object') {
        sortie.push(retrait + k + ':');
        v.forEach(function (el) {
          var corps = yaml(el, retrait + '    ').split('\n');
          sortie.push(retrait + '  - ' + corps[0].replace(/^\s+/, ''));
          corps.slice(1).forEach(function (l) { sortie.push(l); });
        });
      } else if (v && typeof v === 'object' && !Array.isArray(v) && Object.keys(v).length) {
        sortie.push(retrait + k + ':');
        sortie.push(yaml(v, retrait + '  '));
      } else {
        sortie.push(retrait + k + ': ' + enLigne(v));
      }
    });
    return sortie.join('\n');
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
    var dossier = dossierDuCours(etat, V);
    var r = function (s) { return relatif(s, dossier); };
    var rc = function (s) { return relatif(chemin(s), dossier); };
    var calendrier = {};
    liste(c.dates).forEach(function (d, i) { calendrier['jour_' + (i + 1)] = d; });
    var dep = m.deploiement || {};
    var projets = {};
    etat.filieres.forEach(function (f) { if (f.fil_rouge) projets[f.id] = r(f.fil_rouge); });
    return {
      cours: {
        titre: c.titre, slug: slug, auteur: V.auteur, code_module: c.code_module, bloc: normaliserBloc(c.bloc),
        annee: c.annee, palette: c.palette, langues: langues(c), public: c.public, formats: liste(c.formats),
        format_impose: c.format_impose, calendrier: calendrier, horaires: c.horaires, ton: c.ton
      },
      filieres: etat.filieres.map(function (f) {
        return { id: f.id, code: f.code, nom: f.nom, court: f.court, rncp: f.rncp, palette: f.palette, competences: [],
                 epreuve: f.epreuve, bloc: normaliserBloc(f.bloc), module: f.module, page_epreuves: f.page_epreuves,
                 fiche_module: rc(f.fiche_module), grille: rc(f.grille),
                 promotion_app: promotionValide(f.promotion_app) ? f.promotion_app : '',
                 matiere_app: f.matiere_app };
      }),
      groupe_mixte: etat.filieres.length > 1,
      fil_rouge: { nom: etat.fil_rouge.nom, source: rc(etat.fil_rouge.source), projet_par_filiere: projets,
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
        tp: { actif: !!m.tp.actif, sujet: r(m.tp.sujet || '') },
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
        gabarit_technique: chemin(etat.ecosysteme.gabarit_technique),
        cours_de_reference: (etat.ecosysteme.cours_de_reference || []).map(chemin),
        app_livrables: etat.ecosysteme.app_livrables || '',
        doc_import_app: chemin(etat.ecosysteme.doc_import_app),
        epreuves_reelles: chemin(etat.ecosysteme.epreuves_reelles)
      },
      git: {
        depot: etat.git.depot || (V.github && dossier ? V.github + '/' + nomDuDossier(dossier) : ''),
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

  // Une consigne de l'auteur garde ses retours à la ligne, en suite de l'élément de liste qui la porte.
  function element(L, texte) {
    var ls = lignes(texte);
    if (!ls.length) return;
    L.push('   - ' + ls[0]);
    ls.slice(1).forEach(function (l) { L.push('     ' + l); });
  }

  function construirePrompt(etat, v, maintenant) {
    etat = completer(etat, v, maintenant);
    var V = valeurs(v);
    var p = parametres(etat, v);
    var gabarit = p.ecosysteme.gabarit_technique || 'le gabarit';
    var dossier = dossierDuCours(etat, V);
    var r = function (s) { return relatif(s, dossier); };
    var rc = function (s) { return relatif(chemin(s), dossier); };
    var docs = rc(etat.dossier.documents).replace(/^\/+|\/+$/g, '') || 'Doc_Reference';
    var actifs = modulesActifs(p);
    var L = [], n = 0;
    var etape = function () { n += 1; return n + '. '; };
    L.push('Crée un nouveau cours avec le template de cours, en suivant son prompt paramétrable.');
    L.push('');
    L.push(etape() + 'Lis d\'abord, dans ' + gabarit + ' :');
    L.push('   - CLAUDE.md, dont les exigences de l\'auteur (§ 2) valent pour ce cours ;');
    L.push('   - prompts/PROMPT-Cours-parametrable.md, le tronc, en entier ;');
    if (actifs.length) {
      L.push('   - les modules actifs, chacun avant sa phase : ' +
             actifs.map(function (x) { return 'prompts/modules/' + x.fichier; }).join(', ') + '.');
    }
    L.push('');
    L.push(etape() + 'Le dossier du cours : ' + (dossier || '(à préciser)') + '.');
    var secrets = lignes(etat.dossier.secrets).map(rc);
    var regleSecrets = function (lieu) {
      if (secrets.length) {
        L.push('   - ' + (secrets.length > 1 ? 'Ces fichiers sont des secrets' : 'Ce fichier est un secret') +
               ', à ne jamais ouvrir, afficher ni citer : ' + enumerer(secrets) + '.');
      }
      L.push('   - Tout fichier de configuration ou de mot de passe trouvé parmi ' + lieu + ' (.json, .env,');
      L.push('     « mot de passe », identifiants, clés) est un secret : ne l\'ouvre pas, et signale-le à l\'auteur.');
      L.push('     Si un modèle protégé doit être déverrouillé, demande-le à l\'auteur.');
    };
    if (etat.dossier.existe) {
      L.push('   Il existe déjà, et ses documents de référence sont dans ' + docs + '/.');
      L.push('   - Ne lance aucune recherche dans ce dossier tant que son .rgignore n\'exclut pas ' + docs + '/ :');
      L.push('     ouvre les documents un par un, par leur chemin.');
      regleSecrets('les documents');
      L.push('   - Ne déplace, ne renomme et ne modifie aucun document.');
      L.push('   - Lis tous les documents, en profondeur, avant la moindre question de cadrage. Les ouvrages se');
      L.push('     reformulent et se citent, sans jamais en reproduire le texte ni les figures.');
      L.push('   - À l\'étape zéro, écris cours.json dans le gabarit, avec « sortie » sur ce dossier, puis lance à la');
      L.push('     racine du gabarit python3 nouveau_cours.py --essai --ecraser, et enfin --ecraser : les documents');
      L.push('     et deploiement/config.json restent en place.');
      L.push('   - Aussitôt après, avant git init et avant toute recherche, ajoute ' + docs + '/ au .gitignore et au');
      L.push('     .rgignore du cours : les ouvrages y sont sous droits, et rien n\'en part dans Git.');
    } else {
      L.push('   Il n\'existe pas encore : nouveau_cours.py le crée. L\'auteur dépose ensuite les documents dans');
      L.push('   sources/, que Git ignore ; lis-les tous, en profondeur, avant la moindre question de cadrage.');
      regleSecrets('sources/');
    }
    L.push('   - Une fois le cours créé, garde ce prompt dans docs/prompts/00-Prompt-de-lancement.md.');
    if (p.modules.complements.illustrations.actif) {
      L.push('');
      L.push(etape() + 'Les illustrations se font avec Codex : vérifie codex --version et codex login status. Sans Codex,');
      L.push('   donne la procédure du module 10 et arrête-toi avant les illustrations.');
    }

    // Le calendrier d'abord, puis les consignes de l'auteur, enfin les points que la page a relevés.
    var verif = verifications(etat, v, maintenant).filter(function (x) { return x.prompt; });
    var cons = etat.consignes;
    var precisions = verif.filter(function (x) { return x.calendrier; }).map(function (x) { return x.prompt; });
    [['Le fil rouge. ', cons.fil_rouge], ['Le TP. ', cons.tp],
     ['Les livrables déjà connus, à structurer au cadrage. ', etat.livrables], ['Autres consignes. ', cons.autres]]
      .forEach(function (x) { if (String(x[1] || '').trim()) precisions.push(x[0] + r(x[1]).trim()); });
    verif.filter(function (x) { return !x.calendrier; }).forEach(function (x) { precisions.push(x.prompt); });
    if (precisions.length) {
      L.push('');
      L.push(etape() + 'Ce que l\'auteur a précisé, à appliquer au cadrage :');
      precisions.forEach(function (x) { element(L, x); });
    }

    L.push('');
    L.push(etape() + 'Applique le tronc avec ces PARAMÈTRES. Un champ vide se déduit des documents');
    L.push('   ou se demande, une question à la fois.');
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
    completer: completer, filieresDeLaPaire: filieresDeLaPaire, parametres: parametres, modulesActifs: modulesActifs,
    verifications: verifications, construirePrompt: construirePrompt, fichierValeurs: fichierValeurs,
    fabriquerSlug: fabriquerSlug, nomDuDossier: nomDuDossier, relatif: relatif, promotionValide: promotionValide
  };
  if (typeof module !== 'undefined' && module.exports) module.exports = API;
  else racine.GENERATEUR = API;
})(this);
