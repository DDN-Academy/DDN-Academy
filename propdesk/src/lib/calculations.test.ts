/**
 * Tests unitaires du cœur métier — `npm test`
 * Scénarios calqués sur un challenge type FundedNext 50K :
 * drawdown trailing EOD 2000 $, soft breach 1000 $/trade, consistance 40 %,
 * objectif 3000 $.
 */
import { describe, expect, it } from "vitest";
import {
  computeAccountSnapshot,
  isSoftBreach,
  maxNextTradeGain,
  positionSizing,
  tradePnl,
  tradeRMultiple,
  tradeTicks,
  violatesConsistency,
} from "./calculations";
import type { PropAccount, Trade, TradeDirection } from "./types";

// ── Fixtures ────────────────────────────────────────────────────────────────

const account: PropAccount = {
  id: "acc-1",
  user_id: "user-1",
  name: "FundedNext 50K",
  firm: "FundedNext",
  account_size: 50000,
  drawdown_limit: 2000,
  drawdown_type: "trailing_eod",
  soft_breach_limit: 1000,
  consistency_pct: 40,
  profit_target: 3000,
  target_rrr: 2,
  default_symbol: "MNQ",
  default_tick_size: 0.25,
  default_tick_value: 0.5,
  created_at: "",
  updated_at: "",
};

let seq = 0;
/** Trade MNQ (tick 0.25 / 0.50 $) — helper de fixture. */
function mnq(opts: {
  direction?: TradeDirection;
  entry: number;
  exit: number;
  contracts?: number;
  stopTicks?: number;
  openedAt: string;
}): Trade {
  seq += 1;
  return {
    id: `t-${seq}`,
    user_id: "user-1",
    account_id: "acc-1",
    direction: opts.direction ?? "long",
    entry_price: opts.entry,
    exit_price: opts.exit,
    contracts: opts.contracts ?? 2,
    stop_ticks: opts.stopTicks ?? 40,
    symbol: "MNQ",
    tick_size: 0.25,
    tick_value: 0.5,
    opened_at: opts.openedAt,
    notes: null,
    created_at: opts.openedAt,
  };
}

// ── Calculs par trade ───────────────────────────────────────────────────────

describe("calculs par trade", () => {
  it("P&L et ticks — long gagnant", () => {
    // Long MNQ 20000 → 20025 = +100 ticks, 2 contrats à 0.50 $ = +100 $
    const t = mnq({ entry: 20000, exit: 20025, openedAt: "2026-07-01T10:00:00Z" });
    expect(tradeTicks(t)).toBe(100);
    expect(tradePnl(t)).toBe(100);
  });

  it("P&L et ticks — short gagnant", () => {
    // Short 20050 → 20000 = +200 ticks, 2 contrats = +200 $
    const t = mnq({ direction: "short", entry: 20050, exit: 20000, openedAt: "2026-07-01T10:00:00Z" });
    expect(tradeTicks(t)).toBe(200);
    expect(tradePnl(t)).toBe(200);
  });

  it("P&L — long perdant", () => {
    const t = mnq({ entry: 20000, exit: 19990, openedAt: "2026-07-01T10:00:00Z" }); // −40 ticks
    expect(tradeTicks(t)).toBe(-40);
    expect(tradePnl(t)).toBe(-40);
  });

  it("évite le bruit de virgule flottante", () => {
    // 0.1 + 0.2 ≠ 0.30000000000000004
    const t = mnq({ entry: 20000.1, exit: 20000.35, contracts: 1, openedAt: "2026-07-01T10:00:00Z" });
    expect(tradeTicks(t)).toBe(1);
    expect(tradePnl(t)).toBe(0.5);
  });

  it("R-multiple réalisé (RRR réel)", () => {
    // +80 ticks avec stop 40 ticks → RRR réel = 2
    const t = mnq({ entry: 20000, exit: 20020, stopTicks: 40, openedAt: "2026-07-01T10:00:00Z" });
    expect(tradeRMultiple(t)).toBe(2);
    // Stop plein touché → −1 R
    const loser = mnq({ entry: 20000, exit: 19990, stopTicks: 40, openedAt: "2026-07-01T10:00:00Z" });
    expect(tradeRMultiple(loser)).toBe(-1);
  });

  it("soft breach : perte strictement supérieure au seuil", () => {
    // 10 contrats × 250 ticks × 0.50 $ = −1250 $ → breach (seuil 1000)
    const breach = mnq({ entry: 20000, exit: 19937.5, contracts: 10, openedAt: "2026-07-01T10:00:00Z" });
    expect(isSoftBreach(breach, 1000)).toBe(true);
    // Perte de exactement 1000 $ → pas un breach (limite autorisée)
    const at = mnq({ entry: 20000, exit: 19950, contracts: 10, openedAt: "2026-07-01T10:00:00Z" });
    expect(tradePnl(at)).toBe(-1000);
    expect(isSoftBreach(at, 1000)).toBe(false);
  });
});

// ── Règle de consistance ────────────────────────────────────────────────────

describe("règle de consistance", () => {
  it("détecte un trade qui pèse plus de X % du profit cumulé", () => {
    // Gain 500 sur profit cumulé 1000 = 50 % > 40 % → violation
    expect(violatesConsistency(500, 1000, 40)).toBe(true);
    // Gain 400 sur 1000 = 40 % pile → autorisé
    expect(violatesConsistency(400, 1000, 40)).toBe(false);
    // Les pertes ne violent jamais la consistance
    expect(violatesConsistency(-500, 1000, 40)).toBe(false);
    // Profit cumulé négatif → règle pas encore applicable
    expect(violatesConsistency(500, -200, 40)).toBe(false);
  });

  it("gain max autorisé sur le prochain trade : g = p·P/(1−p)", () => {
    // P = 1200 $, p = 40 % → 0.4×1200/0.6 = 800 $
    expect(maxNextTradeGain(1200, 40)).toBe(800);
    // Vérification : 800 ≤ 40 % × (1200 + 800) = 800 ✓
    expect(violatesConsistency(800, 2000, 40)).toBe(false);
    expect(violatesConsistency(801, 2001, 40)).toBe(true);
    // Aucun profit encore → 0
    expect(maxNextTradeGain(0, 40)).toBe(0);
    expect(maxNextTradeGain(-500, 40)).toBe(0);
    // 100 % → pas de limite
    expect(maxNextTradeGain(1000, 100)).toBe(Infinity);
  });
});

// ── Position sizing ─────────────────────────────────────────────────────────

describe("position sizing (règle soft breach)", () => {
  it("nombre de contrats max = floor(seuil / (stop × valeur tick))", () => {
    // Seuil 1000 $, stop 40 ticks sur MNQ (0.50 $/tick) → 1000/20 = 50 contrats
    const r = positionSizing(1000, 40, 0.5, 2);
    expect(r.maxContracts).toBe(50);
    expect(r.riskPerContract).toBe(20);
    expect(r.riskAtMax).toBe(1000);
    expect(r.gainAtTargetRrr).toBe(2000);
  });

  it("arrondit toujours vers le bas", () => {
    // Seuil 1000 $, stop 30 ticks ES (12.50 $/tick) = 375 $/contrat → 2 contrats
    const r = positionSizing(1000, 30, 12.5, 3);
    expect(r.maxContracts).toBe(2);
    expect(r.riskAtMax).toBe(750);
    expect(r.gainAtTargetRrr).toBe(2250);
  });
});

// ── Snapshot de compte : équity, drawdown trailing, stats ───────────────────

describe("computeAccountSnapshot", () => {
  it("compte vierge : équity = taille du compte, floor initial", () => {
    const s = computeAccountSnapshot(account, []);
    expect(s.equity).toBe(50000);
    expect(s.floor).toBe(48000);
    expect(s.distanceToFloor).toBe(2000);
    expect(s.floorRatio).toBe(1);
    expect(s.breached).toBe(false);
    expect(s.winRateAll).toBeNull();
    expect(s.profitFactor).toBeNull();
    expect(s.maxNextGain).toBe(0); // aucun profit → 0
  });

  it("le floor trailing EOD remonte à la clôture de journée (ratchet)", () => {
    const trades = [
      // Jour 1 : +500 $ → EOD 50500
      mnq({ entry: 20000, exit: 20125, contracts: 2, openedAt: "2026-07-01T14:00:00Z" }),
      // Jour 2 : le floor doit être passé à 50500 − 2000 = 48500
      mnq({ entry: 20000, exit: 20010, contracts: 2, openedAt: "2026-07-02T14:00:00Z" }),
    ];
    const s = computeAccountSnapshot(account, trades);
    expect(s.trades[0].floorAtTrade).toBe(48000); // jour 1 : floor initial
    expect(s.trades[1].floorAtTrade).toBe(48500); // jour 2 : ratchet appliqué
    expect(s.equity).toBe(50540);
  });

  it("le floor ne redescend JAMAIS, même après une journée perdante", () => {
    const trades = [
      mnq({ entry: 20000, exit: 20125, contracts: 2, openedAt: "2026-07-01T14:00:00Z" }), // +500
      mnq({ entry: 20000, exit: 19900, contracts: 2, openedAt: "2026-07-02T14:00:00Z" }), // −400
      mnq({ entry: 20000, exit: 20005, contracts: 2, openedAt: "2026-07-03T14:00:00Z" }), // +20
    ];
    const s = computeAccountSnapshot(account, trades);
    // Jour 3 : EOD jour 2 = 50100 < plus haut EOD 50500 → floor reste 48500
    expect(s.trades[2].floorAtTrade).toBe(48500);
  });

  it("le floor trailing est plafonné à la taille du compte", () => {
    const big = [
      // Jour 1 : +2500 $ → EOD 52500 ; floor brut = 50500 mais plafonné à 50000
      mnq({ entry: 20000, exit: 20625, contracts: 2, openedAt: "2026-07-01T14:00:00Z" }),
      mnq({ entry: 20000, exit: 20010, contracts: 2, openedAt: "2026-07-02T14:00:00Z" }),
    ];
    const s = computeAccountSnapshot(account, big);
    expect(s.trades[1].floorAtTrade).toBe(50000);
  });

  it("drawdown fixe : le floor ne bouge pas", () => {
    const fixedAccount: PropAccount = { ...account, drawdown_type: "static" };
    const trades = [
      mnq({ entry: 20000, exit: 20125, contracts: 2, openedAt: "2026-07-01T14:00:00Z" }),
      mnq({ entry: 20000, exit: 20010, contracts: 2, openedAt: "2026-07-02T14:00:00Z" }),
    ];
    const s = computeAccountSnapshot(fixedAccount, trades);
    expect(s.trades[1].floorAtTrade).toBe(48000);
  });

  it("détecte le franchissement du floor (breach)", () => {
    const trades = [
      // −2200 $ d'un coup : 20 contrats × 220 ticks × 0.50 $
      mnq({ entry: 20000, exit: 19945, contracts: 20, openedAt: "2026-07-01T14:00:00Z" }),
    ];
    const s = computeAccountSnapshot(account, trades);
    expect(s.equity).toBe(47800);
    expect(s.breached).toBe(true);
    expect(s.floorRatio).toBe(0);
  });

  it("P&L journalier cumulé et profit cumulé", () => {
    const trades = [
      mnq({ entry: 20000, exit: 20050, contracts: 2, openedAt: "2026-07-01T13:00:00Z" }), // +200
      mnq({ entry: 20000, exit: 19975, contracts: 2, openedAt: "2026-07-01T15:00:00Z" }), // −100
      mnq({ entry: 20000, exit: 20025, contracts: 2, openedAt: "2026-07-02T13:00:00Z" }), // +100
    ];
    const s = computeAccountSnapshot(account, trades);
    expect(s.trades[0].dayPnl).toBe(200);
    expect(s.trades[1].dayPnl).toBe(100); // 200 − 100, même journée
    expect(s.trades[2].dayPnl).toBe(100); // nouvelle journée : repart de 0
    expect(s.cumulativeProfit).toBe(200);
    expect(s.distanceToTarget).toBe(2800);
  });

  it("statistiques : win rate, profit factor, RRR moyen", () => {
    const trades = [
      mnq({ entry: 20000, exit: 20020, stopTicks: 40, openedAt: "2026-07-01T13:00:00Z" }), // +80t = 2R, +80$
      mnq({ entry: 20000, exit: 19990, stopTicks: 40, openedAt: "2026-07-01T14:00:00Z" }), // −40t = −1R, −40$
      mnq({ entry: 20000, exit: 20030, stopTicks: 40, openedAt: "2026-07-01T15:00:00Z" }), // +120t = 3R, +120$
      mnq({ entry: 20000, exit: 19990, stopTicks: 40, openedAt: "2026-07-01T16:00:00Z" }), // −40t = −1R, −40$
    ];
    const s = computeAccountSnapshot(account, trades);
    expect(s.winRateAll).toBe(50);
    expect(s.avgWinRrr).toBe(2.5); // (2 + 3) / 2
    expect(s.avgRMultiple).toBe(0.75); // (2 − 1 + 3 − 1) / 4
    expect(s.profitFactor).toBe(2.5); // 200 / 80
  });

  it("compte les soft breaches et violations de consistance", () => {
    // Profit total final : 2000 + 100 − 1100 = 1000 $ ; seuil 40 % = 400 $
    const trades = [
      // +2000 > 400 → violation de consistance (pèse 200 % du profit total)
      mnq({ entry: 20000, exit: 20100, contracts: 10, openedAt: "2026-07-01T13:00:00Z" }),
      // +100 ≤ 400 → conforme
      mnq({ entry: 20000, exit: 20025, contracts: 2, openedAt: "2026-07-01T14:00:00Z" }),
      // −1100 → soft breach (seuil 1000 $)
      mnq({ entry: 20000, exit: 19945, contracts: 10, openedAt: "2026-07-01T15:00:00Z" }),
    ];
    const s = computeAccountSnapshot(account, trades);
    expect(s.consistencyViolationCount).toBe(1);
    expect(s.trades[0].consistencyViolation).toBe(true);
    expect(s.trades[1].consistencyViolation).toBe(false);
    expect(s.softBreachCount).toBe(1);
    expect(s.trades[2].softBreach).toBe(true);
  });

  it("courbe d'équity : point initial + un point par trade", () => {
    const trades = [
      mnq({ entry: 20000, exit: 20050, contracts: 2, openedAt: "2026-07-01T13:00:00Z" }),
    ];
    const s = computeAccountSnapshot(account, trades);
    expect(s.equityCurve).toHaveLength(2);
    expect(s.equityCurve[0].equity).toBe(50000);
    expect(s.equityCurve[1].equity).toBe(50200);
  });

  it("les trades sont traités par ordre chronologique même reçus en désordre", () => {
    const trades = [
      mnq({ entry: 20000, exit: 20010, contracts: 2, openedAt: "2026-07-02T14:00:00Z" }),
      mnq({ entry: 20000, exit: 20125, contracts: 2, openedAt: "2026-07-01T14:00:00Z" }), // +500, jour 1
    ];
    const s = computeAccountSnapshot(account, trades);
    expect(s.trades[0].opened_at).toBe("2026-07-01T14:00:00Z");
    expect(s.trades[1].floorAtTrade).toBe(48500); // ratchet du jour 1 bien appliqué
  });
});
