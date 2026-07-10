/**
 * Barre de progression "distance au floor" — la jauge de survie du compte.
 * Vert : > 50 % de marge restante · Orange : 20–50 % · Rouge : < 20 %.
 */
import { fmtMoney } from "@/lib/format";

export default function FloorGauge({
  distance,
  ratio,
  floor,
  breached,
}: {
  distance: number;
  ratio: number; // 0..1
  floor: number;
  breached: boolean;
}) {
  const pct = Math.round(ratio * 100);
  const color = breached || ratio < 0.2 ? "bg-loss" : ratio < 0.5 ? "bg-warn" : "bg-profit";
  const textColor =
    breached || ratio < 0.2 ? "text-loss" : ratio < 0.5 ? "text-warn" : "text-profit";

  return (
    <div className="card">
      <div className="mb-2 flex items-baseline justify-between">
        <p className="text-xs font-medium uppercase tracking-wider text-fg-muted">
          Distance au floor de drawdown
        </p>
        <p className={`font-mono text-lg font-bold ${textColor}`}>
          {breached ? "BREACH" : fmtMoney(distance)}
        </p>
      </div>
      <div
        className="h-3 overflow-hidden rounded-full bg-ink-800"
        role="progressbar"
        aria-valuenow={pct}
        aria-valuemin={0}
        aria-valuemax={100}
      >
        <div
          className={`h-full rounded-full transition-all duration-500 ${color}`}
          style={{ width: `${Math.max(2, pct)}%` }}
        />
      </div>
      <div className="mt-2 flex justify-between text-xs text-fg-faint">
        <span>Floor : {fmtMoney(floor)}</span>
        <span>{pct} % de marge restante</span>
      </div>
      {breached && (
        <p className="mt-3 rounded-lg border border-loss/50 bg-loss/10 p-2 text-sm font-semibold text-loss">
          ⚠ L&apos;équity a touché la limite de drawdown — compte en breach selon vos règles.
        </p>
      )}
    </div>
  );
}
