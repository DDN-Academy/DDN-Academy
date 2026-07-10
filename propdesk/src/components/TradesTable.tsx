"use client";

/**
 * Historique des trades avec toutes les colonnes calculées + alertes.
 */
import { useState } from "react";
import { useRouter } from "next/navigation";
import type { ComputedTrade } from "@/lib/calculations";
import { fmtDateTime, fmtMoney, fmtNumber } from "@/lib/format";
import { createClient } from "@/lib/supabase/client";

export default function TradesTable({ trades }: { trades: ComputedTrade[] }) {
  const supabase = createClient();
  const router = useRouter();
  const [deleting, setDeleting] = useState<string | null>(null);

  async function handleDelete(id: string) {
    if (!window.confirm("Supprimer ce trade ?")) return;
    setDeleting(id);
    const { error } = await supabase.from("trades").delete().eq("id", id);
    setDeleting(null);
    if (error) window.alert(error.message);
    else router.refresh();
  }

  if (trades.length === 0) {
    return (
      <div className="card text-center text-sm text-fg-muted">
        Aucun trade enregistré. Saisissez votre premier trade ci-dessus.
      </div>
    );
  }

  // Du plus récent au plus ancien pour l'affichage
  const rows = [...trades].reverse();

  return (
    <div className="card overflow-x-auto p-0">
      <table className="table-terminal min-w-[900px]">
        <thead>
          <tr>
            <th>Date</th>
            <th>Contrat</th>
            <th>Dir.</th>
            <th>Entrée → Sortie</th>
            <th>Qté</th>
            <th>Ticks</th>
            <th>P&amp;L</th>
            <th>RRR réel</th>
            <th>P&amp;L jour</th>
            <th>Dist. floor</th>
            <th>Alertes</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {rows.map((t) => (
            <tr key={t.id}>
              <td className="whitespace-nowrap text-fg-muted">{fmtDateTime(t.opened_at)}</td>
              <td>{t.symbol}</td>
              <td className={t.direction === "long" ? "text-profit" : "text-loss"}>
                {t.direction === "long" ? "▲ L" : "▼ S"}
              </td>
              <td className="whitespace-nowrap">
                {fmtNumber(t.entry_price, 4)} → {fmtNumber(t.exit_price, 4)}
              </td>
              <td>{t.contracts}</td>
              <td className={t.ticks >= 0 ? "text-profit" : "text-loss"}>{fmtNumber(t.ticks)}</td>
              <td className={t.pnl >= 0 ? "font-semibold text-profit" : "font-semibold text-loss"}>
                {fmtMoney(t.pnl, { sign: true })}
              </td>
              <td>{fmtNumber(t.rMultiple)}R</td>
              <td className={t.dayPnl >= 0 ? "text-profit" : "text-loss"}>
                {fmtMoney(t.dayPnl, { sign: true })}
              </td>
              <td>{fmtMoney(t.distanceToFloor)}</td>
              <td className="whitespace-nowrap">
                {t.softBreach && (
                  <span
                    className="mr-1 rounded bg-loss/15 px-1.5 py-0.5 text-[10px] font-bold uppercase text-loss"
                    title="Perte supérieure au seuil soft breach"
                  >
                    Breach
                  </span>
                )}
                {t.consistencyViolation && (
                  <span
                    className="rounded bg-warn/15 px-1.5 py-0.5 text-[10px] font-bold uppercase text-warn"
                    title="Gain supérieur au % de consistance du profit total"
                  >
                    Consist.
                  </span>
                )}
              </td>
              <td>
                <button
                  type="button"
                  onClick={() => handleDelete(t.id)}
                  disabled={deleting === t.id}
                  className="text-fg-faint transition-colors hover:text-loss"
                  title="Supprimer"
                >
                  ✕
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
