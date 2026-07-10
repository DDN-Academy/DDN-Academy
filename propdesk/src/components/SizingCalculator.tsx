"use client";

/**
 * Calculateur de position sizing basé sur la règle soft breach :
 * l'utilisateur entre un stop en ticks → l'app affiche le nombre de
 * contrats max, le risque réel et le gain si le RRR cible est atteint.
 */
import { useMemo, useState } from "react";
import { positionSizing } from "@/lib/calculations";
import { CONTRACT_SPECS, getContractSpec } from "@/lib/contracts";
import { fmtMoney, fmtNumber } from "@/lib/format";
import type { PropAccount } from "@/lib/types";

export default function SizingCalculator({ account }: { account: PropAccount }) {
  const accountSymbolKnown = !!getContractSpec(account.default_symbol);
  const [symbol, setSymbol] = useState(accountSymbolKnown ? account.default_symbol : "CUSTOM");
  const [stopTicks, setStopTicks] = useState("40");
  const [rrr, setRrr] = useState(String(account.target_rrr));

  const spec = getContractSpec(symbol);
  const tickValue = spec?.tickValue ?? account.default_tick_value;

  const result = useMemo(() => {
    const s = Number(stopTicks);
    const r = Number(rrr);
    if (!(s > 0 && r > 0)) return null;
    return positionSizing(account.soft_breach_limit, s, tickValue, r);
  }, [stopTicks, rrr, tickValue, account.soft_breach_limit]);

  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <div className="card space-y-4">
        <h2 className="font-semibold">Paramètres</h2>
        <div>
          <label htmlFor="sizing-symbol" className="field-label">
            Contrat
          </label>
          <select
            id="sizing-symbol"
            className="field"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value)}
          >
            {CONTRACT_SPECS.map((c) => (
              <option key={c.symbol} value={c.symbol}>
                {c.label} — tick = ${c.tickValue}
              </option>
            ))}
            {!accountSymbolKnown && (
              <option value="CUSTOM">
                {account.default_symbol} — tick = ${account.default_tick_value}
              </option>
            )}
          </select>
        </div>
        <div>
          <label htmlFor="sizing-stop" className="field-label">
            Stop loss (ticks)
          </label>
          <input
            id="sizing-stop"
            type="number"
            min="1"
            step="1"
            className="field font-mono"
            value={stopTicks}
            onChange={(e) => setStopTicks(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="sizing-rrr" className="field-label">
            RRR cible
          </label>
          <input
            id="sizing-rrr"
            type="number"
            min="0.1"
            step="any"
            className="field font-mono"
            value={rrr}
            onChange={(e) => setRrr(e.target.value)}
          />
        </div>
        <p className="text-xs text-fg-faint">
          Seuil soft breach du compte : {fmtMoney(account.soft_breach_limit)} par trade — formule :
          ⌊seuil ÷ (stop × valeur du tick)⌋
        </p>
      </div>

      <div className="card flex flex-col justify-center">
        {result === null ? (
          <p className="text-center text-sm text-fg-muted">
            Entrez un stop en ticks pour calculer la taille de position.
          </p>
        ) : result.maxContracts === 0 ? (
          <p className="text-center font-semibold text-loss">
            Stop trop large : même 1 contrat dépasserait le seuil de soft breach (
            {fmtMoney(result.riskPerContract)} de risque par contrat).
          </p>
        ) : (
          <dl className="space-y-5 text-center">
            <div>
              <dt className="text-xs font-medium uppercase tracking-wider text-fg-muted">
                Contrats max autorisés
              </dt>
              <dd className="font-mono text-5xl font-bold text-accent">{result.maxContracts}</dd>
            </div>
            <div className="grid grid-cols-3 gap-2">
              <div>
                <dt className="text-xs text-fg-muted">Risque / contrat</dt>
                <dd className="font-mono text-sm">{fmtMoney(result.riskPerContract)}</dd>
              </div>
              <div>
                <dt className="text-xs text-fg-muted">Risque réel total</dt>
                <dd className="font-mono text-sm text-loss">{fmtMoney(result.riskAtMax)}</dd>
              </div>
              <div>
                <dt className="text-xs text-fg-muted">Gain si {fmtNumber(Number(rrr))}R</dt>
                <dd className="font-mono text-sm text-profit">
                  {fmtMoney(result.gainAtTargetRrr, { sign: true })}
                </dd>
              </div>
            </div>
          </dl>
        )}
      </div>
    </div>
  );
}
