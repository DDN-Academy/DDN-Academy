"use client";

/**
 * Saisie d'un trade — input minimal : entrée, sortie, contrats, direction,
 * stop en ticks, date/heure (pré-remplie). Tout le reste est calculé et
 * affiché EN DIRECT avant même l'enregistrement (P&L, ticks, RRR réel,
 * alertes soft breach / consistance).
 */
import { useRouter } from "next/navigation";
import { useMemo, useState } from "react";
import {
  isSoftBreach,
  maxNextTradeGain,
  tradePnl,
  tradeRMultiple,
  tradeTicks,
} from "@/lib/calculations";
import { CONTRACT_SPECS, getContractSpec } from "@/lib/contracts";
import { fmtMoney, fmtNumber, toDatetimeLocal } from "@/lib/format";
import { createClient } from "@/lib/supabase/client";
import type { PropAccount, TradeDirection } from "@/lib/types";

const CUSTOM = "CUSTOM";

export default function TradeForm({
  account,
  cumulativeProfit,
  onSaved,
}: {
  account: PropAccount;
  /** Profit cumulé actuel du compte (pour l'alerte consistance en direct). */
  cumulativeProfit: number;
  onSaved?: () => void;
}) {
  const supabase = createClient();
  const router = useRouter();

  const accountSymbolKnown = !!getContractSpec(account.default_symbol);
  const [direction, setDirection] = useState<TradeDirection>("long");
  const [entry, setEntry] = useState("");
  const [exit, setExit] = useState("");
  const [contracts, setContracts] = useState("1");
  const [stopTicks, setStopTicks] = useState("");
  const [symbol, setSymbol] = useState(accountSymbolKnown ? account.default_symbol : CUSTOM);
  const [openedAt, setOpenedAt] = useState(() => toDatetimeLocal(new Date()));
  const [notes, setNotes] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  // Specs du contrat sélectionné (fallback : celles du compte)
  const spec = getContractSpec(symbol);
  const tickSize = spec?.tickSize ?? account.default_tick_size;
  const tickValue = spec?.tickValue ?? account.default_tick_value;

  /** Aperçu en direct des calculs dès que la saisie est complète. */
  const preview = useMemo(() => {
    const e = Number(entry);
    const x = Number(exit);
    const c = Number(contracts);
    const s = Number(stopTicks);
    if (!(e > 0 && x > 0 && c > 0 && s > 0)) return null;
    const input = {
      direction,
      entry_price: e,
      exit_price: x,
      contracts: c,
      stop_ticks: s,
      tick_size: tickSize,
      tick_value: tickValue,
    };
    const pnl = tradePnl(input);
    const maxGain = maxNextTradeGain(cumulativeProfit, account.consistency_pct);
    return {
      pnl,
      ticks: tradeTicks(input),
      rMultiple: tradeRMultiple(input),
      softBreach: isSoftBreach(input, account.soft_breach_limit),
      // Alerte consistance en direct : gain supérieur au max autorisé actuel
      consistencyWarning: pnl > 0 && Number.isFinite(maxGain) && pnl > maxGain,
    };
  }, [entry, exit, contracts, stopTicks, direction, tickSize, tickValue, account, cumulativeProfit]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const {
        data: { user },
      } = await supabase.auth.getUser();
      if (!user) throw new Error("Session expirée, reconnectez-vous.");

      const { error } = await supabase.from("trades").insert({
        user_id: user.id,
        account_id: account.id,
        direction,
        entry_price: Number(entry),
        exit_price: Number(exit),
        contracts: Number(contracts),
        stop_ticks: Number(stopTicks),
        symbol: symbol === CUSTOM ? account.default_symbol : symbol,
        tick_size: tickSize,
        tick_value: tickValue,
        opened_at: new Date(openedAt).toISOString(),
        notes: notes.trim() || null,
      });
      if (error) {
        if (error.code === "42501") {
          throw new Error(
            "Plan gratuit : 20 trades par mois. Passez au plan Pro pour des trades illimités.",
          );
        }
        throw error;
      }
      // Réinitialise uniquement les champs du trade, garde le contexte
      setEntry("");
      setExit("");
      setNotes("");
      setOpenedAt(toDatetimeLocal(new Date()));
      onSaved?.();
      router.refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Une erreur est survenue.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="card space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="font-semibold">Nouveau trade</h2>
        {/* Toggle Long / Short */}
        <div className="flex overflow-hidden rounded-lg border border-ink-700">
          <button
            type="button"
            onClick={() => setDirection("long")}
            className={`px-4 py-1.5 text-sm font-semibold transition-colors ${
              direction === "long" ? "bg-profit/20 text-profit" : "text-fg-muted hover:text-fg"
            }`}
          >
            Long ▲
          </button>
          <button
            type="button"
            onClick={() => setDirection("short")}
            className={`px-4 py-1.5 text-sm font-semibold transition-colors ${
              direction === "short" ? "bg-loss/20 text-loss" : "text-fg-muted hover:text-fg"
            }`}
          >
            Short ▼
          </button>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
        <div>
          <label htmlFor="entry" className="field-label">
            Prix d&apos;entrée *
          </label>
          <input
            id="entry"
            required
            type="number"
            step="any"
            min="0"
            className="field font-mono"
            value={entry}
            onChange={(e) => setEntry(e.target.value)}
            placeholder="20000.25"
          />
        </div>
        <div>
          <label htmlFor="exit" className="field-label">
            Prix de sortie *
          </label>
          <input
            id="exit"
            required
            type="number"
            step="any"
            min="0"
            className="field font-mono"
            value={exit}
            onChange={(e) => setExit(e.target.value)}
            placeholder="20010.00"
          />
        </div>
        <div>
          <label htmlFor="contracts" className="field-label">
            Contrats *
          </label>
          <input
            id="contracts"
            required
            type="number"
            min="1"
            step="1"
            className="field font-mono"
            value={contracts}
            onChange={(e) => setContracts(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="stopTicks" className="field-label">
            Stop (ticks) *
          </label>
          <input
            id="stopTicks"
            required
            type="number"
            min="1"
            step="1"
            className="field font-mono"
            value={stopTicks}
            onChange={(e) => setStopTicks(e.target.value)}
            placeholder="40"
          />
        </div>
        <div>
          <label htmlFor="symbol" className="field-label">
            Contrat
          </label>
          <select
            id="symbol"
            className="field"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value)}
          >
            {CONTRACT_SPECS.map((c) => (
              <option key={c.symbol} value={c.symbol}>
                {c.symbol}
              </option>
            ))}
            {!accountSymbolKnown && <option value={CUSTOM}>{account.default_symbol}</option>}
          </select>
        </div>
        <div>
          <label htmlFor="openedAt" className="field-label">
            Date / heure
          </label>
          <input
            id="openedAt"
            type="datetime-local"
            required
            className="field font-mono"
            value={openedAt}
            onChange={(e) => setOpenedAt(e.target.value)}
          />
        </div>
      </div>

      <div>
        <label htmlFor="notes" className="field-label">
          Notes (optionnel)
        </label>
        <input
          id="notes"
          className="field"
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          placeholder="Setup, contexte, état d'esprit…"
        />
      </div>

      {/* Aperçu en direct */}
      {preview && (
        <div
          className={`rounded-lg border p-3 text-sm ${
            preview.softBreach
              ? "border-loss/50 bg-loss/10"
              : preview.consistencyWarning
                ? "border-warn/50 bg-warn/10"
                : "border-ink-700 bg-ink-800/60"
          }`}
        >
          <div className="flex flex-wrap gap-x-6 gap-y-1 font-mono">
            <span>
              P&amp;L :{" "}
              <strong className={preview.pnl >= 0 ? "text-profit" : "text-loss"}>
                {fmtMoney(preview.pnl, { sign: true })}
              </strong>
            </span>
            <span>
              Ticks : <strong>{fmtNumber(preview.ticks)}</strong>
            </span>
            <span>
              RRR réel : <strong>{fmtNumber(preview.rMultiple)}R</strong>
            </span>
          </div>
          {preview.softBreach && (
            <p className="mt-2 font-semibold text-loss">
              ⚠ SOFT BREACH : perte supérieure au seuil de{" "}
              {fmtMoney(account.soft_breach_limit)} par trade !
            </p>
          )}
          {preview.consistencyWarning && (
            <p className="mt-2 font-semibold text-warn">
              ⚠ Consistance : ce gain dépasserait {account.consistency_pct} % de votre profit
              total.
            </p>
          )}
        </div>
      )}

      {error && <p className="text-sm text-loss">{error}</p>}

      <button type="submit" disabled={loading} className="btn-primary w-full sm:w-auto">
        {loading ? "…" : "Enregistrer le trade"}
      </button>
    </form>
  );
}
