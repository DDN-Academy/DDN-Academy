/**
 * ============================================================================
 * PropDesk — Cœur métier : tous les calculs de trading en fonctions PURES.
 * ============================================================================
 * Aucune dépendance à React, Supabase ou au réseau : uniquement des entrées
 * (paramètres du compte + liste de trades) et des sorties calculées.
 * Testé dans calculations.test.ts.
 *
 * Convention : les montants sont en dollars, les prix en points, les stops
 * en ticks. `tick_value` est la valeur d'UN tick pour UN contrat.
 */

import type { PropAccount, Trade, TradeDirection } from "./types";

// ── Helpers numériques ──────────────────────────────────────────────────────

/** Corrige le bruit de virgule flottante (0.30000000000000004 → 0.3). */
function fix(n: number, decimals = 6): number {
  const f = 10 ** decimals;
  return Math.round(n * f) / f;
}

// ── Calculs par trade ───────────────────────────────────────────────────────

export interface TradeInput {
  direction: TradeDirection;
  entry_price: number;
  exit_price: number;
  contracts: number;
  stop_ticks: number;
  tick_size: number;
  tick_value: number;
}

/**
 * Nombre de ticks gagnés (+) ou perdus (−) sur le trade.
 * Long  : (sortie − entrée) / tick_size
 * Short : (entrée − sortie) / tick_size
 */
export function tradeTicks(t: TradeInput): number {
  const move = t.direction === "long" ? t.exit_price - t.entry_price : t.entry_price - t.exit_price;
  return fix(move / t.tick_size, 4);
}

/** P&L du trade en dollars : ticks × valeur du tick × nb de contrats. */
export function tradePnl(t: TradeInput): number {
  return fix(tradeTicks(t) * t.tick_value * t.contracts, 2);
}

/** Risque initial du trade en dollars (stop × valeur tick × contrats). */
export function tradeRisk(t: TradeInput): number {
  return fix(t.stop_ticks * t.tick_value * t.contracts, 2);
}

/**
 * Multiple de risque réalisé (R-multiple) : ticks gagnés ÷ ticks de stop.
 * +2 → le trade a rapporté 2× le risque ; −1 → stop plein touché.
 * C'est le "RRR réel atteint" du trade.
 */
export function tradeRMultiple(t: TradeInput): number {
  return fix(tradeTicks(t) / t.stop_ticks, 2);
}

/** Soft breach : la PERTE du trade dépasse le seuil autorisé par trade. */
export function isSoftBreach(t: TradeInput, softBreachLimit: number): boolean {
  return tradePnl(t) < -softBreachLimit;
}

// ── Règle de consistance ────────────────────────────────────────────────────

/**
 * Le gain de ce trade dépasse-t-il `consistencyPct` % du profit de
 * référence ? Les prop firms évaluent la consistance contre le profit TOTAL
 * du compte au moment du contrôle (payout) : on passe donc ici le profit
 * cumulé actuel, et les violations passées se résorbent quand le profit
 * total augmente. Ne concerne que les trades gagnants et un profit positif.
 */
export function violatesConsistency(
  pnl: number,
  cumulativeProfitAfter: number,
  consistencyPct: number,
): boolean {
  if (pnl <= 0 || cumulativeProfitAfter <= 0) return false;
  return pnl > fix((consistencyPct / 100) * cumulativeProfitAfter, 2);
}

/**
 * Gain maximum autorisé sur le PROCHAIN trade sans violer la consistance.
 * On cherche g tel que g ≤ p × (P + g)  ⇒  g_max = p × P ÷ (1 − p)
 * avec P = profit cumulé actuel et p = consistency_pct / 100.
 * Si P ≤ 0 : tout gain représenterait 100 % du profit → 0.
 * Si p ≥ 1 (100 %) : aucune limite.
 */
export function maxNextTradeGain(cumulativeProfit: number, consistencyPct: number): number {
  const p = consistencyPct / 100;
  if (p >= 1) return Infinity;
  if (cumulativeProfit <= 0) return 0;
  return fix((p * cumulativeProfit) / (1 - p), 2);
}

// ── Position sizing (règle soft breach) ─────────────────────────────────────

export interface SizingResult {
  /** Nombre de contrats max autorisé pour que stop plein < seuil soft breach. */
  maxContracts: number;
  /** Risque réel en dollars avec ce nombre de contrats. */
  riskAtMax: number;
  /** Risque en dollars par contrat. */
  riskPerContract: number;
  /** Gain en dollars si le RRR cible est atteint (avec maxContracts). */
  gainAtTargetRrr: number;
}

/**
 * Calculateur de position sizing : combien de contrats au max pour un stop
 * donné, sans risquer un soft breach ?
 *   maxContracts = floor(seuil_soft_breach ÷ (stop_ticks × valeur_tick))
 */
export function positionSizing(
  softBreachLimit: number,
  stopTicks: number,
  tickValue: number,
  targetRrr: number,
): SizingResult {
  const riskPerContract = fix(stopTicks * tickValue, 2);
  const maxContracts = riskPerContract > 0 ? Math.floor(softBreachLimit / riskPerContract) : 0;
  const riskAtMax = fix(maxContracts * riskPerContract, 2);
  return {
    maxContracts,
    riskPerContract,
    riskAtMax,
    gainAtTargetRrr: fix(riskAtMax * targetRrr, 2),
  };
}

// ── Trade enrichi + snapshot de compte ──────────────────────────────────────

/** Un trade avec tous ses champs dérivés, dans l'ordre chronologique. */
export interface ComputedTrade extends Trade {
  ticks: number;
  pnl: number;
  risk: number;
  rMultiple: number;
  softBreach: boolean;
  consistencyViolation: boolean;
  /** P&L cumulé de la JOURNÉE du trade, après ce trade. */
  dayPnl: number;
  /** Profit cumulé du compte depuis le début, après ce trade. */
  cumulativeProfit: number;
  /** Équity du compte après ce trade. */
  equityAfter: number;
  /** Floor de drawdown applicable au moment du trade. */
  floorAtTrade: number;
  /** Distance équity → floor après ce trade. */
  distanceToFloor: number;
}

export interface AccountSnapshot {
  account: PropAccount;
  trades: ComputedTrade[];

  // Équity & drawdown
  equity: number;
  /** Floor courant (limite de drawdown). */
  floor: number;
  /** Distance actuelle équity → floor (marge de survie). */
  distanceToFloor: number;
  /** Fraction restante de la marge de drawdown, entre 0 et 1. */
  floorRatio: number;
  /** true si l'équity a touché ou franchi le floor. */
  breached: boolean;

  // Progression
  cumulativeProfit: number;
  todayPnl: number;
  /** Distance restante jusqu'à l'objectif de profit ($). */
  distanceToTarget: number;
  /** Progression vers l'objectif, entre 0 et 1. */
  targetProgress: number;

  // Consistance
  maxNextGain: number;

  // Statistiques
  winRateAll: number | null;
  winRateLast10: number | null;
  winRateLast20: number | null;
  /** RRR moyen réalisé sur les trades gagnants. */
  avgWinRrr: number | null;
  /** R-multiple moyen sur tous les trades. */
  avgRMultiple: number | null;
  profitFactor: number | null;
  softBreachCount: number;
  consistencyViolationCount: number;

  // Courbe d'équity : un point de départ + un point par trade
  equityCurve: { index: number; date: string; equity: number; floor: number }[];
}

/** Clé de journée (date locale AAAA-MM-JJ) d'un timestamp ISO. */
export function dayKey(iso: string): string {
  const d = new Date(iso);
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${y}-${m}-${day}`;
}

/**
 * Calcule l'état complet d'un compte à partir de ses paramètres et de ses
 * trades. C'est LA fonction appelée par le dashboard.
 *
 * Drawdown trailing EOD : le floor démarre à account_size − drawdown_limit,
 * puis remonte (ratchet, jamais vers le bas) à chaque clôture de journée où
 * l'équity de fin de journée fait un nouveau plus haut EOD. Le floor est
 * plafonné à account_size (comportement FundedNext/Topstep : une fois le
 * drawdown "consommé" par les gains, le floor s'arrête au solde initial).
 */
export function computeAccountSnapshot(account: PropAccount, rawTrades: Trade[]): AccountSnapshot {
  // Ordre chronologique strict
  const sorted = [...rawTrades].sort(
    (a, b) => new Date(a.opened_at).getTime() - new Date(b.opened_at).getTime(),
  );

  const staticFloor = fix(account.account_size - account.drawdown_limit, 2);

  let equity = account.account_size;
  let cumulativeProfit = 0;
  let highestEod = account.account_size; // plus haut d'équity en clôture de journée
  let floor = staticFloor;
  let currentDay: string | null = null;
  let dayPnl = 0;
  let breached = false;

  const computed: ComputedTrade[] = [];
  const equityCurve: AccountSnapshot["equityCurve"] = [];

  for (const trade of sorted) {
    const day = dayKey(trade.opened_at);

    // Changement de journée → clôture EOD de la journée précédente :
    // le floor trailing remonte si l'équity EOD a fait un nouveau plus haut.
    if (currentDay !== null && day !== currentDay) {
      if (account.drawdown_type === "trailing_eod" && equity > highestEod) {
        highestEod = equity;
        floor = Math.min(fix(highestEod - account.drawdown_limit, 2), account.account_size);
      }
      dayPnl = 0;
    }
    currentDay = day;

    const pnl = tradePnl(trade);
    const ticks = tradeTicks(trade);
    equity = fix(equity + pnl, 2);
    cumulativeProfit = fix(cumulativeProfit + pnl, 2);
    dayPnl = fix(dayPnl + pnl, 2);
    if (equity <= floor) breached = true;

    computed.push({
      ...trade,
      ticks,
      pnl,
      risk: tradeRisk(trade),
      rMultiple: tradeRMultiple(trade),
      softBreach: isSoftBreach(trade, account.soft_breach_limit),
      // Rempli après la boucle : évalué contre le profit cumulé FINAL
      consistencyViolation: false,
      dayPnl,
      cumulativeProfit,
      equityAfter: equity,
      floorAtTrade: floor,
      distanceToFloor: fix(equity - floor, 2),
    });
  }

  // Consistance : chaque trade est évalué contre le profit total ACTUEL du
  // compte (comme le fait la prop firm au moment du payout). Un trade qui
  // violait la règle hier peut redevenir conforme quand le profit grandit.
  for (const t of computed) {
    t.consistencyViolation = violatesConsistency(t.pnl, cumulativeProfit, account.consistency_pct);
  }

  // Courbe d'équity : point initial + un point par trade
  equityCurve.push({ index: 0, date: "", equity: account.account_size, floor: staticFloor });
  computed.forEach((t, i) =>
    equityCurve.push({
      index: i + 1,
      date: dayKey(t.opened_at),
      equity: t.equityAfter,
      floor: t.floorAtTrade,
    }),
  );

  // P&L du jour : uniquement si le dernier trade date d'aujourd'hui
  const todayKey = dayKey(new Date().toISOString());
  const todayPnl = computed
    .filter((t) => dayKey(t.opened_at) === todayKey)
    .reduce((s, t) => fix(s + t.pnl, 2), 0);

  // Statistiques
  const winRate = (list: ComputedTrade[]): number | null => {
    if (list.length === 0) return null;
    return fix((list.filter((t) => t.pnl > 0).length / list.length) * 100, 1);
  };
  const winners = computed.filter((t) => t.pnl > 0);
  const losers = computed.filter((t) => t.pnl < 0);
  const grossWin = winners.reduce((s, t) => s + t.pnl, 0);
  const grossLoss = Math.abs(losers.reduce((s, t) => s + t.pnl, 0));

  const distanceToFloor = fix(equity - floor, 2);

  return {
    account,
    trades: computed,
    equity,
    floor,
    distanceToFloor,
    floorRatio: Math.max(0, Math.min(1, distanceToFloor / account.drawdown_limit)),
    breached: breached || equity <= floor,
    cumulativeProfit,
    todayPnl,
    distanceToTarget: Math.max(0, fix(account.profit_target - cumulativeProfit, 2)),
    targetProgress: Math.max(0, Math.min(1, cumulativeProfit / account.profit_target)),
    maxNextGain: maxNextTradeGain(cumulativeProfit, account.consistency_pct),
    winRateAll: winRate(computed),
    winRateLast10: winRate(computed.slice(-10)),
    winRateLast20: winRate(computed.slice(-20)),
    avgWinRrr:
      winners.length > 0
        ? fix(winners.reduce((s, t) => s + t.rMultiple, 0) / winners.length, 2)
        : null,
    avgRMultiple:
      computed.length > 0
        ? fix(computed.reduce((s, t) => s + t.rMultiple, 0) / computed.length, 2)
        : null,
    profitFactor:
      grossLoss > 0 ? fix(grossWin / grossLoss, 2) : winners.length > 0 ? Infinity : null,
    softBreachCount: computed.filter((t) => t.softBreach).length,
    consistencyViolationCount: computed.filter((t) => t.consistencyViolation).length,
    equityCurve,
  };
}
