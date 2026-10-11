// Formes JSON exactes renvoyées par le backend (goldpilot/backend/goldpilot/api/app.py).
// Les champs marqués « ? » peuvent être absents selon la version du serveur.

export type SignalStatut = "EN_ATTENTE" | "ACTIF" | "ANNULE" | "EXPIRE" | "CLOTURE";

export interface Simulation {
  entree: number | null;
  entree_ts: string | null;
  stop_actuel: number | null;
  sortie: number | null;
  sortie_ts: string | null;
  raison: string | null;
  r: number | null;
  pnl_usd: number | null;
}

export interface ExecutionDeclaree {
  executee: boolean;
  entree: number | null;
  sortie: number | null;
  contrats: number | null;
  pnl_usd: number | null;
  note: string | null;
}

export interface Signal {
  id: string;
  cree: string | null;
  cree_paris: string;
  mode: "simulation" | "reel" | string;
  valide: boolean;
  version: string;
  contrat: string;
  sens: "LONG" | "SHORT";
  type_entree: string;
  entree: number;
  plage: [number, number];
  stop: number;
  objectif: number | null;
  stop_suiveur_atr: number | null;
  atr: number | null;
  contrats: number;
  risque_usd: number;
  rr: number | null;
  validite: string | null;
  validite_ny: string;
  sortie_max: string;
  justification: string;
  invalidation: string;
  calendrier: string;
  source_prix: string;
  prix_maj: string | null;
  statut: SignalStatut | string;
  raison_statut: string;
  simulation: Simulation;
  execution_declaree: ExecutionDeclaree | null;
  /** Vrai seulement si l'on peut encore ENTRER : statut ouvert, validité non écoulée, prix dans la plage, entrée non interdite. */
  entree_ouverte?: boolean;
  plage_depassee?: boolean;
  entree_interdite?: string | null;
  niveaux?: Niveaux | null;
}

/** Niveaux de contexte de la décision (barres terminées uniquement). Distances en ATR = (prix − niveau) / ATR. */
export interface Niveaux {
  plus_haut_veille?: number | null;
  plus_bas_veille?: number | null;
  plus_haut_seance?: number | null;
  plus_bas_seance?: number | null;
  swing_haut_15m?: number | null;
  swing_bas_15m?: number | null;
  distances_atr?: Record<string, number | null>;
}

export interface EtatComposant {
  ok: boolean;
  texte: string;
}

export interface StatutSysteme {
  connexion: EtatComposant;
  donnees: EtatComposant & { age_s: number | null; source: string };
  moteur: EtatComposant & { etat: string; arret: { raison: string; depuis: string; type?: string } | null };
  notifications: EtatComposant & {
    active: boolean;
    configure: boolean;
    echecs_24h: number;
    derniere: string | null;
    /** Faux si aucun envoi (alerte ou test) n'a jamais été tenté. */
    verifiees?: boolean;
    derniere_tentative?: { statut: string; erreur: string | null; type: string; quand: string } | null;
  };
}

export interface SerieMacro {
  id: string;
  nom: string;
  valeur: number | null;
  unite: string;
  date: string | null;
  variation_5j: number | null;
  url: string;
}

export interface ContexteMacro {
  disponible: boolean;
  maj: string | null;
  source: string;
  note: string;
  probleme: string | null;
  series: SerieMacro[];
}

export interface Marche {
  instrument: string;
  contrat: string;
  tradingview: string;
  tradovate: string;
  prochain_roll: string;
  contrat_suivant: string;
  prix: number | null;
  prix_maj: string | null;
  seance: string;
  regime: string | null;
  ecart_moyenne_atr: number | null;
  prochaine_annonce: { titre: string; quand: string; ny: string } | null;
  contexte_macro?: ContexteMacro;
}

export interface CompteSimule {
  balance: number;
  hwm_eod: number;
  floor: number;
  best_day: number;
  day_pnl: number;
  days: number;
  breached: boolean;
  breach_reason: string;
  day_start_balance: number;
  day: string;
  passed: boolean;
  target: number | null;
}

export interface Trading {
  setup: string;
  signal_en_cours: Signal | null;
  dernier_signal: Signal | null;
  derniere_analyse: { heure: string; resultat: string; raisons: string[] } | null;
  strategie: { version: string | null; validee: boolean; verdict: string };
  mode_trading: "simulation" | "reel" | string;
  mode_utilisateur: "actif" | "pause" | string;
  risque: {
    par_trade_usd: number;
    perte_jour_max_usd: number;
    trades_jour_max: number;
    programme: string;
    perte_max_programme: number;
    objectif: number | null;
  };
  compte_simule: CompteSimule | null;
  compte_reel: { solde: number; maj: string; plancher: number | null } | null;
}

export interface Incident {
  gravite: string;
  message: string;
  depuis: string;
  /** Composant source (si le serveur le fournit) : « contexte » = avertissements macro FRED, sans effet sur les signaux. */
  composant?: string;
}

export interface Dashboard {
  maintenant: string;
  rejeu: { horloge: string | null; horloge_paris: string | null } | null;
  statut: StatutSysteme;
  marche: Marche;
  trading: Trading;
  incidents: Incident[];
}

export interface ControleRisque {
  controle: string;
  ok: boolean;
  detail: string;
  bloquant?: boolean;
}

export interface SignalDetail {
  signal: Signal;
  evenements: { heure: string; type: string; detail: Record<string, unknown> | null }[];
  controles_risque: ControleRisque[];
  contexte: Record<string, unknown>;
  alertes: { type: string; statut: string; creee: string; envoyee: string | null; erreur: string | null }[];
}

export type JournalType = "decisions" | "incidents" | "notifications" | "webhooks" | "controle" | "audit";

export type JournalLigne = Record<string, unknown>;

export interface Metriques {
  n: number;
  taux_de_gain?: number;
  gain_moyen_R?: number;
  perte_moyenne_R?: number;
  esperance_R?: number;
  ecart_type_R?: number;
  t?: number;
  profit_factor?: number;
  total_R?: number;
  drawdown_max_R?: number;
  serie_pertes_max?: number;
  serie_gains_max?: number;
  trades_par_mois?: number;
  ic95_bas?: number;
  ic95_haut?: number;
  ic_unilateral95_bas?: number;
  sorties?: Record<string, number>;
}

export interface LigneMC {
  risk_per_trade_usd: number;
  trajectoires: number;
  horizon_jours: number;
  p_reussite: number;
  p_violation: number;
  p_en_cours: number;
  jours_median_reussite: number | null;
  jours_p75_reussite?: number | null;
  p_objectif_releve?: number;
  profit_median: number;
  profit_p05: number;
  trades_moyens: number;
  survie?: Record<string, number>;
  retraits?: { moyenne_payee?: number; mediane_payee?: number; p_au_moins_un?: number };
}

export interface MonteCarlo {
  prix_reference?: number;
  trades_wf?: number;
  jours_wf?: number;
  challenge_wf?: LigneMC[];
  challenge_2022_2025?: LigneMC[];
  challenge_wf_prix_4500?: LigneMC[];
  profil_retenu?: { risque_par_trade_usd: number; regle: string; contrainte_respectee: boolean };
  finance_wf?: LigneMC;
  suspension?: { n_trades: number; dd_median: number; dd_p05: number; dd_p01: number; serie_pertes_p95: number; serie_pertes_p99: number };
}

export interface LigneParGroupe {
  year?: number;
  index?: string;
  side?: string;
  n: number;
  esperance_R: number;
  total_R: number;
  taux_de_gain: number;
}

export interface TestFinal {
  candidat?: string;
  statut?: string;
  exploratoire_base?: Metriques;
  exploratoire_couts_x2?: Metriques;
  exploratoire_couts_fixes?: Metriques;
  exploratoire_par_annee?: LigneParGroupe[];
  exploratoire_par_seance?: LigneParGroupe[];
  exploratoire_par_sens?: LigneParGroupe[];
  controle_resolution_2025?: { periode?: string; barres_15min?: Metriques; execution_5min?: Metriques };
  walk_forward_S1?: Metriques;
}

export interface Famille {
  walk_forward?: { resume?: Metriques };
  production?: string;
  entrainement?: Metriques;
  validation?: Metriques;
  validation_couts_x2_esperance_R?: number;
  fraction_annees_positives?: number;
  fraction_voisins_positifs?: number;
  DSR_200?: number;
  criteres?: Record<string, boolean>;
  eligible?: boolean;
}

export interface Selection {
  genere_utc?: string;
  essais_cette_session?: number;
  essais_comptes_pour_DSR?: number;
  familles?: Record<string, Famille>;
}

export interface Production {
  strategy?: string;
  version?: string;
  validated?: boolean;
  verdict?: string;
  trades_par_mois_attendus?: number;
  seuils_suspension?: { drawdown_R: number; serie_pertes: number };
}

export interface Stats {
  production: Production | null;
  selection: Selection | null;
  test_final: TestFinal | null;
  monte_carlo: MonteCarlo | null;
  execution: {
    signaux: number;
    delai_moteur_median_s: number | null;
    delai_alerte_median_s: number | null;
    delai_alerte_max_s: number | null;
    ecart_entree_simulee_median_atr: number | null;
    execution_declaree?: ExecutionDeclareeStats;
    controle_croise: Record<string, number>;
  };
  paper: {
    n: number;
    esperance_R: number;
    taux_de_gain: number;
    total_R: number;
    drawdown_max_R: number;
    pnl_usd: number;
    courbe: { date: string; R: number }[];
  } | null;
}

export interface RiskSettings {
  risk_per_trade_usd: number;
  max_cushion_fraction: number;
  daily_loss_stop_usd: number;
  max_trades_per_day: number;
  max_losses_per_day: number;
  consistency_lock_fraction: number;
  safety_margin_usd: number;
  slippage_allowance_oz: number;
  commission_per_contract_rt: number;
  max_contracts_personal: number;
}

export interface Regle {
  name: string;
  value: string;
  status: string;
  source: string;
}

export interface Programme {
  key: string;
  label: string;
  phase: string;
  account_size: number;
  profit_target: number | null;
  max_loss: number;
  trailing_eod: boolean;
  lock_balance: number | null;
  daily_loss_limit: number | null;
  consistency_pct: number | null;
  max_micros: number;
  flat_by_ny: string;
  min_benchmark_days: number | null;
  benchmark_min_profit: number | null;
  min_cycle_profit: number | null;
  min_withdrawal: number | null;
  max_withdrawal: number | null;
  reward_share: number | null;
  rules: Regle[];
  user_confirmed: boolean;
  checked_on: string;
  initial_floor: number;
  consistency_cap: number | null;
}

export interface Reglages {
  risque: RiskSettings;
  programme: string;
  programmes: Record<string, Programme>;
  mode_trading: string;
  strategie_validee: boolean;
  confirmation_fundednext: { confirme: boolean; reference: string; date?: string };
  regles_verifiees_le: string;
  tradingview: { url_webhook: string; jeton_defini: boolean; symbole: string; unite: string };
  telegram: { configure: boolean; jeton_defini: boolean };
  source_donnees: string;
}

export interface Calendrier {
  statut: { ok: boolean; maj: string; source: string } | null;
  evenements: { titre: string; impact: string; paris: string; new_york: string; source: string }[];
}

/** Glissement DÉCLARÉ par l'utilisateur ($/once, positif = défavorable) — jamais confirmé par le courtier. */
export interface ExecutionDeclareeStats {
  source: string;
  n_entrees: number;
  n_sorties: number;
  glissement_entree_median_oz: number | null;
  glissement_entree_max_oz: number | null;
  glissement_sortie_median_oz: number | null;
  glissement_sortie_max_oz: number | null;
  ecart_pnl_par_contrat_median_usd: number | null;
  hypothese_glissement_oz: number | null;
  dans_hypothese: boolean | null;
}

export interface RevuePeriodique {
  date: string;
  version: string;
  n: number;
  esperance_R: number | null;
  borne_basse_95_R: number | null;
  drawdown_max_R: number | null;
  serie_pertes_max: number;
  taux_de_gain: number | null;
  reference?: { esperance_R_walk_forward: number | null; esperance_R_2022_2025: number | null; source: string };
  seuils?: { drawdown_R: number; serie_pertes: number } | null;
  conclusion: string;
}

export interface Gouvernance {
  version_courante: string | null;
  version_approuvee: { version: string; approuve_le: string; par: string } | null;
  en_attente: boolean;
  comparaison: unknown;
  revue_periodique: RevuePeriodique | null;
  arret_version?: { raison: string; depuis: string; type: string } | null;
  phrase_confirmation?: string;
}
