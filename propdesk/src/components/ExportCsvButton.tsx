"use client";

/**
 * Export CSV de l'historique — réservé au plan Pro.
 * Généré côté client à partir des trades déjà calculés.
 */
import Link from "next/link";
import type { ComputedTrade } from "@/lib/calculations";

function csvEscape(v: string | number | null): string {
  const s = v === null ? "" : String(v);
  return /[",\n;]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
}

export default function ExportCsvButton({
  trades,
  accountName,
  pro,
}: {
  trades: ComputedTrade[];
  accountName: string;
  pro: boolean;
}) {
  if (!pro) {
    return (
      <Link href="/dashboard/billing" className="btn-ghost text-xs" title="Réservé au plan Pro">
        Export CSV <span className="text-warn">Pro</span>
      </Link>
    );
  }

  function handleExport() {
    const header = [
      "date",
      "symbol",
      "direction",
      "entry_price",
      "exit_price",
      "contracts",
      "stop_ticks",
      "ticks",
      "pnl_usd",
      "risk_usd",
      "rrr_realise",
      "pnl_jour",
      "profit_cumule",
      "equity",
      "distance_floor",
      "soft_breach",
      "violation_consistance",
      "notes",
    ];
    const lines = trades.map((t) =>
      [
        t.opened_at,
        t.symbol,
        t.direction,
        t.entry_price,
        t.exit_price,
        t.contracts,
        t.stop_ticks,
        t.ticks,
        t.pnl,
        t.risk,
        t.rMultiple,
        t.dayPnl,
        t.cumulativeProfit,
        t.equityAfter,
        t.distanceToFloor,
        t.softBreach ? "oui" : "non",
        t.consistencyViolation ? "oui" : "non",
        t.notes ?? "",
      ]
        .map(csvEscape)
        .join(","),
    );
    const csv = [header.join(","), ...lines].join("\n");
    const blob = new Blob([`﻿${csv}`], { type: "text/csv;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `propdesk-${accountName.toLowerCase().replace(/\s+/g, "-")}-${new Date().toISOString().slice(0, 10)}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  }

  return (
    <button type="button" onClick={handleExport} className="btn-ghost text-xs">
      ⇩ Export CSV
    </button>
  );
}
