/**
 * Formatage des nombres, montants et dates (affichage FR, montants en $ —
 * les comptes prop firm futures sont libellés en dollars US).
 */

export function fmtMoney(n: number, opts: { sign?: boolean } = {}): string {
  if (!Number.isFinite(n)) return "∞";
  const abs = Math.abs(n).toLocaleString("en-US", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
  const sign = n < 0 ? "−" : opts.sign && n > 0 ? "+" : "";
  return `${sign}$${abs}`;
}

export function fmtNumber(n: number, decimals = 2): string {
  if (!Number.isFinite(n)) return "∞";
  return n.toLocaleString("en-US", {
    minimumFractionDigits: 0,
    maximumFractionDigits: decimals,
  });
}

export function fmtPct(n: number | null, decimals = 1): string {
  if (n === null || !Number.isFinite(n)) return "—";
  return `${n.toFixed(decimals)} %`;
}

export function fmtDateTime(iso: string): string {
  return new Date(iso).toLocaleString("fr-FR", {
    day: "2-digit",
    month: "2-digit",
    year: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function fmtDate(iso: string): string {
  return new Date(iso).toLocaleDateString("fr-FR", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}

/** Valeur pour <input type="datetime-local"> à partir d'un Date. */
export function toDatetimeLocal(d: Date): string {
  const pad = (x: number) => String(x).padStart(2, "0");
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
}
