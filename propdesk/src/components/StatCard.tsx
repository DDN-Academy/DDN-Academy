/** Petite carte de statistique du dashboard. */
export default function StatCard({
  label,
  value,
  sub,
  tone = "neutral",
}: {
  label: string;
  value: string;
  sub?: string;
  tone?: "neutral" | "profit" | "loss" | "warn";
}) {
  const toneClass = {
    neutral: "text-fg",
    profit: "text-profit",
    loss: "text-loss",
    warn: "text-warn",
  }[tone];

  return (
    <div className="card p-4">
      <p className="text-xs font-medium uppercase tracking-wider text-fg-muted">{label}</p>
      <p className={`mt-1 font-mono text-xl font-bold ${toneClass}`}>{value}</p>
      {sub && <p className="mt-0.5 text-xs text-fg-faint">{sub}</p>}
    </div>
  );
}
