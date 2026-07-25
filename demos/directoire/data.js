/* ═══════════════════════════════════════════════════════════════════
   LE DIRECTOIRE : SOCLE DE DONNÉES PARTAGÉ
   Utilisé par index.html (site client) ET equipe.html (espace équipe).
   Même origine ⇒ même localStorage ⇒ les deux sites partagent tout.
   Synchronisation temps réel via BroadcastChannel (repli : storage).
   Aucune dépendance externe.
   ═══════════════════════════════════════════════════════════════════ */
(function (global) {
  'use strict';

  /* ---------- OUTILS ---------- */
  const pad = n => String(n).padStart(2, '0');
  const iso = d => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
  const parseISO = s => { const [a, b, c] = s.split('-').map(Number); return new Date(a, b - 1, c); };
  const min2hm = m => `${pad(Math.floor(m / 60))}:${pad(m % 60)}`;
  const hm2min = t => { const [h, m] = t.split(':').map(Number); return h * 60 + m; };
  const uid = () => Math.random().toString(36).slice(2, 10);
  const todayISO = () => iso(new Date());
  const addDays = (s, n) => { const d = parseISO(s); d.setDate(d.getDate() + n); return iso(d); };
  const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

  const JOURS = ['Dimanche', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi'];
  const JC = ['Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam'];
  const MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'];
  const fmtDate = s => { const d = parseISO(s); return `${JOURS[d.getDay()]} ${d.getDate()} ${MOIS[d.getMonth()]}`; };
  const fmtShort = s => { const d = parseISO(s); return `${JC[d.getDay()]} ${d.getDate()}/${pad(d.getMonth() + 1)}`; };
  const makeRef = () => { const c = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'; let s = ''; for (let i = 0; i < 4; i++) s += c[Math.floor(Math.random() * c.length)]; return 'DIR-' + s; };

  const ALLERGENES = ['Gluten', 'Crustacés', 'Œufs', 'Poissons', 'Arachides', 'Soja', 'Lait',
    'Fruits à coque', 'Céleri', 'Moutarde', 'Sésame', 'Sulfites', 'Lupin', 'Mollusques'];

  const LIB = {
    attente: 'En attente', confirmee: 'Confirmée', arrivee: 'Arrivé', installee: 'Installée',
    terminee: 'Terminée', annulee: 'Annulée', absence: 'Absence'
  };
  /* phases de service d'une table occupée */
  const PHASES = { apero: 'Apéritif', entree: 'Entrée', plat: 'Plat', dessert: 'Dessert', addition: 'Addition', nettoyage: 'À nettoyer' };

  /* Emplacements photo du site client. Remplacez-les par vos propres photos
     depuis l'espace équipe, onglet Plus. */
  const PHOTO_SLOTS = [
    { k: 'hero', nom: 'Photo principale (accueil)', hint: 'Vue large, format paysage. Elle occupe tout le haut du site.' },
    { k: 'terrasse', nom: 'La terrasse végétalisée', hint: 'Format paysage, en journée.' },
    { k: 'patio', nom: 'Le patio', hint: 'Format paysage.' },
    { k: 'salle', nom: 'La salle', hint: 'Format paysage, tables dressées.' },
    { k: 'soiree', nom: 'Une soirée', hint: 'Ambiance du soir, concert ou match.' },
    { k: 'equipe', nom: 'La cuisine et l\'équipe', hint: 'Le chef au travail ou la brigade.' }
  ];

  /* ---------- DONNÉES DE DÉMONSTRATION ---------- */
  function seed() {
    const zones = [
      { id: 'z1', nom: 'Terrasse', meteo: true, actif: true },
      { id: 'z2', nom: 'Patio', meteo: false, actif: true },
      { id: 'z3', nom: 'Salle', meteo: false, actif: true }
    ];

    const defs = [
      ['z1', [[1, 2, 14, 20], [2, 2, 30, 18], [3, 4, 47, 17], [4, 4, 65, 19], [5, 2, 83, 22],
              [6, 6, 20, 47], [7, 4, 42, 49], [8, 4, 64, 48], [9, 2, 84, 52], [10, 2, 30, 75]]],
      ['z2', [[11, 2, 20, 26], [12, 4, 48, 24], [13, 4, 76, 29], [14, 6, 32, 62], [15, 2, 68, 65]]],
      ['z3', [[16, 2, 22, 28], [17, 4, 50, 26], [18, 4, 78, 31], [19, 8, 36, 66], [20, 2, 72, 69]]]
    ];
    const tables = [];
    defs.forEach(([z, list]) => list.forEach(([numero, cap, x, y]) => {
      tables.push({ id: 't' + numero, numero, zoneId: z, capMin: Math.max(1, cap - 2), capMax: cap, x, y, active: true, combinable: [] });
    }));
    /* tables voisines de même zone et ≤4 places : combinables */
    tables.forEach((t, i) => {
      const n = tables[i + 1];
      t.combinable = (n && n.zoneId === t.zoneId && t.capMax <= 4 && n.capMax <= 4) ? [n.id] : [];
    });

    const categories = [
      { id: 'c1', nom: 'Pour commencer', ordre: 1 },
      { id: 'c2', nom: 'Les plats', ordre: 2 },
      { id: 'c3', nom: 'Les pizzas', ordre: 3 },
      { id: 'c4', nom: 'Les desserts', ordre: 4 }
    ];
    /* cat, nom, description, prix, allergènes, tags, origine, photo livrée */
    const rawItems = [
      ['c1', 'Burrata & tomates anciennes', "Tomates du maraîcher, burrata crémeuse, basilic, huile d'olive de Provence.", 14, ['Lait'], ['veg'], '', 'photos/p-burrata.jpg'],
      ['c1', 'Carpaccio de daurade', 'Agrumes, huile vierge, fenouil croquant, poivre de Timut.', 16, ['Poissons', 'Sulfites'], []],
      ['c1', 'Beignets de fleurs de courgette', 'Farce ricotta-menthe, coulis de tomate confite.', 13, ['Gluten', 'Œufs', 'Lait'], ['veg', 'maison']],
      ['c1', 'Poulpe grillé à la plancha', 'Pommes de terre écrasées, chorizo doux, paprika fumé.', 17, ['Mollusques'], [], '', 'photos/p-poulpe.jpg'],
      ['c2', "Souris d'agneau confite", 'Sept heures au thym, jus corsé, légumes du soleil.', 26, ['Céleri', 'Sulfites'], ['sig', 'maison'], '', 'photos/p-agneau.jpg'],
      ['c2', 'Risotto de Saint-Jacques', 'Noix snackées, risotto crémeux au parmesan, émulsion iodée.', 28, ['Mollusques', 'Lait', 'Sulfites'], ['sig']],
      ['c2', 'Poisson entier du jour', "Selon la pêche, grillé à l'arête, fenouil braisé, vierge d'agrumes.", 29, ['Poissons'], ['jour'], '', 'photos/p-poisson.jpg'],
      ['c2', 'Linguine aux palourdes', 'Ail, persil plat, pointe de piment, vin blanc.', 22, ['Gluten', 'Mollusques', 'Sulfites'], []],
      ['c2', 'Tagliata de bœuf', 'Roquette, copeaux de parmesan, huile de romarin.', 27, ['Lait'], [], 'France', 'photos/p-tagliata.jpg'],
      ['c3', 'Pizza Directoire', 'Base tomate, burrata, jambon de Parme, roquette, huile de basilic.', 18, ['Gluten', 'Lait'], ['sig'], '', 'photos/p-pizza1.jpg'],
      ['c3', 'Pizza Reine', 'Tomate, mozzarella fior di latte, jambon blanc, champignons frais.', 15, ['Gluten', 'Lait'], [], '', 'photos/p-pizza3.jpg'],
      ['c3', 'Pizza Végétarienne', 'Légumes grillés du moment, pesto maison, mozzarella.', 16, ['Gluten', 'Lait', 'Fruits à coque'], ['veg'], '', 'photos/p-pizza2.jpg'],
      ['c4', 'Tiramisu maison', 'Mascarpone monté, café serré, cacao amer.', 9, ['Gluten', 'Œufs', 'Lait'], ['maison'], '', 'photos/p-tiramisu.jpg'],
      ['c4', 'Tarte au citron meringuée', 'Citron de Menton, meringue brûlée au chalumeau.', 10, ['Gluten', 'Œufs', 'Lait'], ['maison']],
      ['c4', 'Moelleux au chocolat', 'Cœur coulant, glace vanille bourbon.', 10, ['Gluten', 'Œufs', 'Lait'], ['maison']]
    ];
    const items = rawItems.map((r, i) => ({
      id: 'm' + (i + 1), catId: r[0], nom: r[1], desc: r[2], prix: r[3],
      allergenes: r[4], tags: r[5], origine: r[6] || '', epuise: false, ordre: i, photo: r[7] || null
    }));

    const prenoms = ['Julien', 'Sophie', 'Marc', 'Camille', 'Thomas', 'Léa', 'Nicolas', 'Émilie', 'Antoine', 'Claire',
      'Pierre', 'Manon', 'Lucas', 'Sarah', 'Olivier', 'Nathalie', 'Romain', 'Chloé', 'David', 'Aurélie',
      'Vincent', 'Céline', 'Maxime', 'Julie', 'Fabien', 'Laura', 'Guillaume', 'Élodie', 'Sébastien', 'Marine'];
    const noms = ['Martin', 'Bernard', 'Dubois', 'Thomas', 'Robert', 'Richard', 'Petit', 'Durand', 'Leroy', 'Moreau',
      'Simon', 'Laurent', 'Lefebvre', 'Michel', 'Garcia', 'David', 'Bertrand', 'Roux', 'Vincent', 'Fournier',
      'Morel', 'Girard', 'André', 'Mercier', 'Blanc', 'Guerin', 'Boyer', 'Garnier', 'Chevalier', 'Francois'];
    const guests = [];
    for (let i = 0; i < 44; i++) {
      const p = prenoms[i % prenoms.length], n = noms[(i * 7) % noms.length];
      const visites = Math.floor(Math.random() * 9);
      guests.push({
        id: 'g' + (i + 1), nom: `${p} ${n}`,
        tel: `06 ${pad(10 + Math.floor(Math.random() * 80))} ${pad(Math.floor(Math.random() * 100))} ${pad(Math.floor(Math.random() * 100))} ${pad(Math.floor(Math.random() * 100))}`,
        email: `${p.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '')}.${n.toLowerCase()}@exemple.fr`,
        prefs: '', allergies: i % 11 === 0 ? 'Fruits à coque' : '', notes: '',
        tags: visites >= 6 ? ['habitué'] : (i % 13 === 0 ? ['VIP'] : []),
        visites, absences: i % 17 === 0 ? 1 : 0,
        derniereVisite: visites ? addDays(todayISO(), -Math.floor(Math.random() * 90) - 3) : null,
        depenseTotale: visites * (Math.floor(Math.random() * 40) + 45)
      });
    }
    guests[3].tags = ['VIP']; guests[3].notes = 'Table au calme, aime le rosé de Bandol.'; guests[3].visites = 14;
    guests[8].allergies = 'Crustacés (sévère)'; guests[8].tags = ['allergique'];

    const services = [
      { id: 's1', nom: 'Déjeuner', jours: [0, 1, 2, 3, 4, 5, 6], debut: '12:00', fin: '14:30', dernier: '14:00' },
      { id: 's2', nom: 'Dîner', jours: [0, 1, 2, 3, 4, 5, 6], debut: '19:00', fin: '23:30', dernier: '22:30' }
    ];

    const reservations = [];
    for (let d = -9; d <= 12; d++) {
      const date = addDays(todayISO(), d);
      const nb = d < 0 ? Math.floor(Math.random() * 5) + 2 : (d < 4 ? Math.floor(Math.random() * 6) + 3 : Math.floor(Math.random() * 4) + 1);
      for (let k = 0; k < nb; k++) {
        const soir = Math.random() > 0.35;
        const base = soir ? 19 * 60 : 12 * 60, span = soir ? 180 : 105;
        const heure = min2hm(base + Math.floor(Math.random() * (span / 15)) * 15);
        const couverts = [2, 2, 2, 3, 4, 4, 5, 6][Math.floor(Math.random() * 8)];
        const g = guests[Math.floor(Math.random() * guests.length)];
        let statut = d < 0
          ? ['terminee', 'terminee', 'terminee', 'terminee', 'annulee', 'absence'][Math.floor(Math.random() * 6)]
          : (Math.random() > 0.12 ? 'confirmee' : 'attente');
        reservations.push({
          id: uid(), ref: makeRef(), date, heure, couverts, guestId: g.id, tableIds: [],
          statut, phase: null, zonePref: Math.random() > 0.55 ? 'z1' : null,
          allergies: g.allergies || '', occasion: Math.random() > 0.9 ? 'Anniversaire' : '',
          note: '', origine: Math.random() > 0.5 ? 'site' : 'téléphone',
          createdAt: Date.now() - Math.random() * 9e8, assiseA: null
        });
      }
    }

    /* attribution automatique des tables sur les données de démonstration,
       pour que le plan de salle soit réaliste dès la première ouverture */
    const brouillon = {
      version: 3, services, zones, tables,
      reservations, regles: { durees: { '2': 90, '4': 105, '6': 120, '8': 150 }, tampon: 15, cadence: 22, delaiMin: 120, horizon: 60 },
      fermetures: []
    };
    (function attribue() {
      const dureeB = c => { const r = brouillon.regles.durees; return c <= 2 ? r['2'] : c <= 4 ? r['4'] : c <= 6 ? r['6'] : r['8']; };
      const libre = (tid, date, deb, fin) => !reservations.some(r => {
        if (!r.tableIds.includes(tid) || ['annulee', 'absence'].includes(r.statut)) return false;
        const d = hm2min(r.heure), f = d + dureeB(r.couverts) + brouillon.regles.tampon;
        return deb < f && d < fin;
      });
      reservations.forEach(r => {
        if (['annulee', 'absence'].includes(r.statut)) return;
        const deb = hm2min(r.heure), fin = deb + dureeB(r.couverts) + brouillon.regles.tampon;
        let cands = tables.filter(t => t.zoneId === r.zonePref || !r.zonePref);
        if (!cands.length) cands = tables;
        const seule = cands.filter(t => r.couverts >= t.capMin && r.couverts <= t.capMax && libre(t.id, r.date, deb, fin))
          .sort((a, b) => a.capMax - b.capMax)[0];
        if (seule) { r.tableIds = [seule.id]; return; }
        for (const t of cands) {
          if (!libre(t.id, r.date, deb, fin)) continue;
          const c = (t.combinable || []).map(i => tables.find(x => x.id === i))
            .find(x => x && libre(x.id, r.date, deb, fin) && x.capMax + t.capMax >= r.couverts);
          if (c) { r.tableIds = [t.id, c.id]; return; }
        }
      });
      /* quelques tables déjà occupées ce soir, pour une démonstration vivante */
      const auj = todayISO();
      reservations.filter(r => r.date === auj && r.statut === 'confirmee' && r.tableIds.length)
        .slice(0, 2).forEach((r, i) => {
          r.statut = 'installee';
          r.assiseA = Date.now() - (i === 0 ? 42 : 18) * 60000;
        });
    })();

    return {
      version: 3,
      restaurant: {
        nom: 'Le Directoire', slogan: 'Restaurant bord de mer · Fréjus-Plage',
        adresse: '71 Bd de la Libération, 83600 Fréjus', tel: '07 60 82 10 29',
        email: 'contact@le-directoire.fr', instagram: 'ledirectoirefrejus',
        facebook: 'Directoirefrejusplage', note: 4.3, avis: 543
      },
      services, zones, tables,
      menu: { categories, items },
      guests, reservations,
      fermetures: [{ id: uid(), date: addDays(todayISO(), 16), raison: 'Privatisation', message: 'Soirée privée. Réouverture le lendemain.' }],
      regles: { durees: { '2': 90, '4': 105, '6': 120, '8': 150 }, tampon: 15, cadence: 22, delaiMin: 120, horizon: 60 },
      attente: [], journal: [], photos: {},
      parametres: { code: '1789', noteDuJour: '' }
    };
  }

  /* ---------- STOCKAGE + SYNCHRONISATION ---------- */
  const KEY = 'directoire.v3';
  const BACKUP = 'directoire.v3.backup';
  let DB = null;
  const subs = [];
  const chan = ('BroadcastChannel' in global) ? new BroadcastChannel('directoire') : null;

  function valide(d) {
    return d && typeof d === 'object' && d.tables && d.reservations && d.menu && d.menu.items && d.guests && d.services;
  }
  function load() {
    try {
      const raw = localStorage.getItem(KEY);
      if (!raw) return seed();
      const d = JSON.parse(raw);
      if (!valide(d)) throw new Error('schéma invalide');
      return d;
    } catch (e) {
      try {
        const b = JSON.parse(localStorage.getItem(BACKUP));
        if (valide(b)) { console.warn('Données corrompues : restauration de la sauvegarde.'); return b; }
      } catch (_) { }
      console.warn('Données illisibles : réinitialisation.');
      return seed();
    }
  }
  function save(silencieux) {
    try {
      const s = JSON.stringify(DB);
      const ancien = localStorage.getItem(KEY);
      if (ancien) { try { localStorage.setItem(BACKUP, ancien); } catch (_) { } }
      localStorage.setItem(KEY, s);          // écriture après sauvegarde de l'état précédent
    } catch (e) {
      notifier('plein');
      return false;
    }
    if (!silencieux && chan) chan.postMessage({ t: 'sync', from: API.instance });
    subs.forEach(f => { try { f(); } catch (_) { } });
    return true;
  }
  function notifier(type) {
    subs.forEach(f => { try { f(type); } catch (_) { } });
    if (type === 'plein' && global.alert) {
      console.error('Stockage plein : exportez vos données puis réinitialisez.');
    }
  }
  if (chan) chan.onmessage = e => { if (e.data && e.data.t === 'sync' && e.data.from !== API.instance) { DB = load(); subs.forEach(f => { try { f(); } catch (_) { } }); } };
  global.addEventListener('storage', e => { if (e.key === KEY) { DB = load(); subs.forEach(f => { try { f(); } catch (_) { } }); } });

  function log(quoi, qui) {
    DB.journal.unshift({ id: uid(), ts: Date.now(), quoi, qui: qui || 'équipe' });
    DB.journal = DB.journal.slice(0, 400);
  }

  /* ---------- MOTEUR DE DISPONIBILITÉ ---------- */
  function duree(c) { const r = DB.regles.durees; return c <= 2 ? r['2'] : c <= 4 ? r['4'] : c <= 6 ? r['6'] : r['8']; }
  function estFerme(date) { return DB.fermetures.find(f => f.date === date) || null; }
  function servicesDu(date) { const j = parseISO(date).getDay(); return DB.services.filter(s => s.jours.includes(j)); }
  function serviceDe(date, heure) {
    const m = hm2min(heure);
    return servicesDu(date).find(s => m >= hm2min(s.debut) && m <= hm2min(s.fin)) || null;
  }
  function resasActives(date) {
    return DB.reservations.filter(r => r.date === date && !['annulee', 'absence', 'terminee'].includes(r.statut));
  }
  function tableLibre(tid, date, debMin, finMin, ignoreId) {
    return !resasActives(date).some(r => {
      if (r.id === ignoreId || !r.tableIds.includes(tid)) return false;
      const d = hm2min(r.heure), f = d + duree(r.couverts) + DB.regles.tampon;
      return debMin < f && d < finMin;
    });
  }
  function trouveTables(date, heure, couverts, zoneId, ignoreId) {
    const deb = hm2min(heure), fin = deb + duree(couverts) + DB.regles.tampon;
    let cands = DB.tables.filter(t => t.active && (!zoneId || t.zoneId === zoneId));
    cands = cands.filter(t => { const z = DB.zones.find(x => x.id === t.zoneId); return z && z.actif; });
    const seules = cands
      .filter(t => couverts >= t.capMin && couverts <= t.capMax && tableLibre(t.id, date, deb, fin, ignoreId))
      .sort((a, b) => a.capMax - b.capMax);
    if (seules.length) return [seules[0].id];
    for (const t of cands) {
      if (!tableLibre(t.id, date, deb, fin, ignoreId)) continue;
      for (const cid of (t.combinable || [])) {
        const c = cands.find(x => x.id === cid);
        if (!c || !tableLibre(c.id, date, deb, fin, ignoreId)) continue;
        if (t.capMax + c.capMax >= couverts) return [t.id, c.id];
      }
    }
    return null;
  }
  function cadenceOK(date, heure, couverts, ignoreId) {
    const b = Math.floor(hm2min(heure) / 15);
    const tot = resasActives(date)
      .filter(r => r.id !== ignoreId && Math.floor(hm2min(r.heure) / 15) === b)
      .reduce((s, r) => s + r.couverts, 0);
    return tot + couverts <= DB.regles.cadence;
  }
  function creneaux(date, couverts, zoneId) {
    const out = [];
    if (estFerme(date)) return out;
    const mini = Date.now() + DB.regles.delaiMin * 60000;
    servicesDu(date).forEach(s => {
      for (let m = hm2min(s.debut); m <= hm2min(s.dernier); m += 15) {
        const h = min2hm(m);
        const dt = parseISO(date); dt.setHours(Math.floor(m / 60), m % 60, 0, 0);
        let ok = dt.getTime() >= mini;
        if (ok) ok = cadenceOK(date, h, couverts);
        if (ok) ok = !!trouveTables(date, h, couverts, zoneId);
        out.push({ service: s.nom, serviceId: s.id, heure: h, ok });
      }
    });
    return out;
  }
  function jourComplet(date, couverts, zoneId) {
    if (estFerme(date)) return true;
    return !creneaux(date, couverts, zoneId).some(c => c.ok);
  }
  function couvertsDu(date) {
    return DB.reservations.filter(r => r.date === date && !['annulee', 'absence'].includes(r.statut))
      .reduce((s, r) => s + r.couverts, 0);
  }
  function capaciteTotale() { return DB.tables.filter(t => t.active).reduce((s, t) => s + t.capMax, 0); }
  function ouvertMaintenant() {
    const d = new Date(), date = iso(d), m = d.getHours() * 60 + d.getMinutes();
    if (estFerme(date)) return { ouvert: false, txt: "Fermé aujourd'hui" };
    const ss = servicesDu(date);
    for (const s of ss) if (m >= hm2min(s.debut) && m <= hm2min(s.fin)) return { ouvert: true, txt: `Ouvert · ferme à ${s.fin}` };
    const next = ss.find(s => m < hm2min(s.debut));
    return { ouvert: false, txt: next ? `Fermé · ouvre à ${next.debut}` : 'Fermé · ouvre demain' };
  }

  /* ---------- CRÉATION / MODIFICATION DE RÉSERVATION ---------- */
  const enCours = {};   // clés d'idempotence : neutralise le double-clic
  function reserver(o) {
    const cle = o.cle || (o.tel + o.date + o.heure + o.couverts);
    if (enCours[cle]) return { ok: false, msg: 'Demande déjà en cours de traitement.' };
    enCours[cle] = true;
    setTimeout(() => { delete enCours[cle]; }, 4000);

    let g = DB.guests.find(x => x.tel.replace(/\D/g, '') === String(o.tel).replace(/\D/g, ''));
    if (!g) {
      g = { id: uid(), nom: o.nom, tel: o.tel, email: o.email || '', prefs: '', allergies: o.allergies || '', notes: '', tags: [], visites: 0, absences: 0, derniereVisite: null, depenseTotale: 0 };
      DB.guests.push(g);
    } else {
      if (o.nom) g.nom = o.nom;
      if (o.email) g.email = o.email;
      if (o.allergies) g.allergies = o.allergies;
    }
    const ref = makeRef();

    if (o.listeAttente || !o.heure) {
      DB.attente.push({ id: uid(), ref, guestId: g.id, date: o.date, couverts: o.couverts, plage: o.plage || 'Indifférent', createdAt: Date.now() });
      log('Liste d\'attente ' + ref + ' : ' + g.nom, 'client');
      save();
      delete enCours[cle];
      return { ok: true, ref, attente: true };
    }
    if (estFerme(o.date)) { delete enCours[cle]; return { ok: false, msg: 'Le restaurant est fermé ce jour-là.' }; }
    if (!cadenceOK(o.date, o.heure, o.couverts)) { delete enCours[cle]; return { ok: false, msg: 'Ce créneau vient d\'être pris. Choisissez-en un autre.' }; }
    const tables = trouveTables(o.date, o.heure, o.couverts, o.zonePref || null);
    if (!tables) { delete enCours[cle]; return { ok: false, msg: 'Ce créneau vient d\'être pris. Choisissez-en un autre.' }; }

    const r = {
      id: uid(), ref, date: o.date, heure: o.heure, couverts: o.couverts, guestId: g.id, tableIds: tables,
      statut: 'confirmee', phase: null, zonePref: o.zonePref || null, allergies: o.allergies || '',
      occasion: o.occasion || '', note: o.note || '', origine: o.origine || 'site', createdAt: Date.now(), assiseA: null
    };
    DB.reservations.push(r);
    log('Réservation ' + ref + ' : ' + g.nom + ' (' + r.origine + ')', o.origine === 'site' ? 'client' : 'équipe');
    save();
    delete enCours[cle];
    return { ok: true, ref, reservation: r };
  }
  function parRef(ref) { return DB.reservations.find(r => r.ref === String(ref).trim().toUpperCase()) || null; }
  function annuler(ref, motif) {
    const r = parRef(ref);
    if (!r) return { ok: false, msg: 'Aucune réservation trouvée avec cette référence.' };
    if (r.statut === 'annulee') return { ok: false, msg: 'Cette réservation est déjà annulée.' };
    r.statut = 'annulee'; r.tableIds = []; r.motif = motif || '';
    log('Annulation ' + r.ref, motif === 'client' ? 'client' : 'équipe');
    const att = DB.attente.filter(a => a.date === r.date).length;
    save();
    return { ok: true, attente: att };
  }
  function placer(resaId, tableId) {
    const r = DB.reservations.find(x => x.id === resaId), t = DB.tables.find(x => x.id === tableId);
    if (!r || !t) return { ok: false, msg: 'Introuvable.' };
    const deb = hm2min(r.heure), fin = deb + duree(r.couverts) + DB.regles.tampon;
    if (!tableLibre(tableId, r.date, deb, fin, r.id)) return { ok: false, msg: 'Table ' + t.numero + ' déjà occupée sur ce créneau.' };
    if (r.couverts > t.capMax) {
      const c = (t.combinable || []).map(i => DB.tables.find(x => x.id === i))
        .find(x => x && tableLibre(x.id, r.date, deb, fin, r.id) && x.capMax + t.capMax >= r.couverts);
      if (!c) return { ok: false, msg: 'Table trop petite pour ' + r.couverts + ' couverts.' };
      r.tableIds = [t.id, c.id];
      log('Placement ' + r.ref + ' → tables ' + t.numero + '+' + c.numero);
      save();
      return { ok: true, msg: 'Placé sur les tables ' + t.numero + '+' + c.numero };
    }
    r.tableIds = [t.id];
    log('Placement ' + r.ref + ' → table ' + t.numero);
    save();
    return { ok: true, msg: 'Placé sur la table ' + t.numero };
  }
  function statut(resaId, nouveau) {
    const r = DB.reservations.find(x => x.id === resaId);
    if (!r) return;
    const avant = r.statut;
    r.statut = nouveau;
    const g = DB.guests.find(x => x.id === r.guestId);
    if (nouveau === 'installee' && !r.assiseA) r.assiseA = Date.now();
    if (nouveau === 'terminee' && g) { g.visites++; g.derniereVisite = r.date; r.phase = null; }
    if (nouveau === 'absence' && g) { g.absences++; r.tableIds = []; }
    log(LIB[nouveau] + ' : ' + r.ref);
    save();
    return { avant };
  }

  /* ---------- PHOTOS (vraies photos, déposées par le restaurant) ---------- */
  const Photos = {
    /* Deux niveaux, dans l'ordre :
       1. la photo déposée par le restaurant depuis l'espace équipe ;
       2. la photographie livrée avec le site, présente dans le dossier photos/.
       Tout est hébergé avec le site : aucune dépendance à un service extérieur,
       donc aucun emplacement vide, même sans réseau. */
    DEFAUTS: { hero: 'photos/hero.jpg', terrasse: 'photos/terrasse.jpg', patio: 'photos/patio.jpg',
      salle: 'photos/salle.jpg', soiree: 'photos/soiree.jpg', equipe: 'photos/equipe.jpg' },
    /* liste ordonnée des sources à essayer pour un emplacement */
    sources(k) {
      const perso = DB.photos && DB.photos[k];
      const l = [];
      if (perso) l.push(perso);
      if (Photos.DEFAUTS[k]) l.push(Photos.DEFAUTS[k]);
      return l;
    },
    get(k) { return Photos.sources(k)[0] || null; },
    estPerso(k) { return !!(DB.photos && DB.photos[k]); },
    liste() { return PHOTO_SLOTS.map(s => ({ ...s, url: Photos.get(s.k) })); },
    /* lit un fichier image et le redimensionne : localStorage est limité (~5 Mo) */
    lis(file, maxW, q) {
      return new Promise((resolve, reject) => {
        if (!file || !/^image\//.test(file.type)) return reject(new Error('Ce fichier n\'est pas une image.'));
        const fr = new FileReader();
        fr.onerror = () => reject(new Error('Lecture impossible.'));
        fr.onload = () => {
          const img = new Image();
          img.onerror = () => reject(new Error('Image illisible.'));
          img.onload = () => {
            const M = maxW || 1500;
            const ratio = Math.min(1, M / img.width);
            const w = Math.round(img.width * ratio), h = Math.round(img.height * ratio);
            const cv = document.createElement('canvas');
            cv.width = w; cv.height = h;
            cv.getContext('2d').drawImage(img, 0, 0, w, h);
            resolve(cv.toDataURL('image/jpeg', q || 0.82));
          };
          img.src = fr.result;
        };
        fr.readAsDataURL(file);
      });
    },
    set(k, file, maxW) {
      return Photos.lis(file, maxW).then(url => {
        DB.photos = DB.photos || {};
        DB.photos[k] = url;
        if (!save()) { delete DB.photos[k]; throw new Error('Stockage plein : supprimez des photos ou exportez vos données.'); }
        log('Photo mise à jour : ' + k);
        return url;
      });
    },
    supprime(k) { if (DB.photos) { delete DB.photos[k]; log('Photo supprimée : ' + k); save(); } },
    poids() { return Math.round(JSON.stringify(DB.photos || {}).length / 1024); }
  };

  /* ---------- SAUVEGARDE / RESTAURATION ---------- */
  function exporte() { return JSON.stringify(DB, null, 2); }
  function importe(txt) {
    try {
      const o = JSON.parse(txt);
      if (!valide(o)) return { ok: false, msg: 'Fichier invalide : structure non reconnue.' };
      DB = o; save();
      return { ok: true };
    } catch (e) { return { ok: false, msg: 'Fichier illisible (JSON invalide).' }; }
  }
  function reinitialise() { DB = seed(); save(); }

  /* ---------- API PUBLIQUE ---------- */
  const API = {
    instance: uid(),
    get db() { return DB; },
    init() { DB = load(); save(true); return DB; },
    save, log, seed,
    onChange(f) { subs.push(f); },
    /* outils */
    pad, iso, parseISO, min2hm, hm2min, uid, todayISO, addDays, esc, fmtDate, fmtShort, makeRef,
    JOURS, JC, MOIS, ALLERGENES, LIB, PHASES, PHOTO_SLOTS,
    /* moteur */
    duree, estFerme, servicesDu, serviceDe, resasActives, tableLibre, trouveTables, cadenceOK,
    creneaux, jourComplet, couvertsDu, capaciteTotale, ouvertMaintenant,
    /* actions */
    reserver, parRef, annuler, placer, statut,
    /* divers */
    guest(id) { return DB.guests.find(g => g.id === id) || { nom: 'Inconnu', tel: '', tags: [], allergies: '', visites: 0, absences: 0 }; },
    tableNom(ids) { return ids && ids.length ? ids.map(i => { const t = DB.tables.find(x => x.id === i); return t ? t.numero : '?'; }).join('+') : 'non attribuée'; },
    Photos, exporte, importe, reinitialise
  };
  global.D = API;
})(window);
