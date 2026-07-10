import type { Metadata } from "next";
import Link from "next/link";
import { redirect } from "next/navigation";
import AccountSelect from "@/components/AccountSelect";
import EquityChart from "@/components/EquityChart";
import FloorGauge from "@/components/FloorGauge";
import StatCard from "@/components/StatCard";
import { computeAccountSnapshot } from "@/lib/calculations";
import { fmtMoney, fmtNumber, fmtPct } from "@/lib/format";
import { createClient } from "@/lib/supabase/server";
import type { PropAccount, Trade } from "@/lib/types";

export const metadata: Metadata = { title: "Dashboard" };
export const dynamic = "force-dynamic";

export default async function DashboardPage({
  searchParams,
}: {
  searchParams: { account?: string };
}) {
  const supabase = createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) redirect("/login");

  const { data: accounts } = await supabase
    .from("prop_accounts")
    .select("*")
    .order("created_at", { ascending: true })
    .returns<PropAccount[]>();

  // Onboarding : pas encore de compte configuré
  if (!accounts || accounts.length === 0) {
    return (
      <div className="card mx-auto mt-10 max-w-md text-center">
        <p className="mb-1 font-mono text-3xl">▦</p>
        <p className="mb-2 text-lg font-semibold">Bienvenue sur PropDesk</p>
        <p className="mb-5 text-sm text-fg-muted">
          Commencez par configurer les règles de votre challenge prop firm : drawdown, soft
          breach, consistance et objectif de profit.
        </p>
        <Link href="/dashboard/accounts/new" className="btn-primary">
          Configurer mon compte
        </Link>
      </div>
    );
  }

  const account = accounts.find((a) => a.id === searchParams.account) ?? accounts[0];

  const { data: trades } = await supabase
    .from("trades")
    .select("*")
    .eq("account_id", account.id)
    .order("opened_at", { ascending: true })
    .returns<Trade[]>();

  const s = computeAccountSnapshot(account, trades ?? []);
  const targetPct = Math.round(s.targetProgress * 100);

  return (
    <div className="space-y-6">
      {/* En-tête */}
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl font-bold">{account.name}</h1>
          <p className="text-sm text-fg-muted">
            {account.firm ?? "Prop firm"} ·{" "}
            {account.drawdown_type === "trailing_eod" ? "drawdown trailing EOD" : "drawdown fixe"}
          </p>
        </div>
        <div className="flex items-center gap-3">
          <AccountSelect
            accounts={accounts.map(({ id, name }) => ({ id, name }))}
            selectedId={account.id}
          />
          <Link href={`/dashboard/trades?account=${account.id}`} className="btn-primary">
            + Saisir un trade
          </Link>
        </div>
      </div>

      {/* Ligne 1 : équity, P&L jour, objectif, consistance */}
      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <StatCard
          label="Équity actuelle"
          value={fmtMoney(s.equity)}
          sub={`Départ : ${fmtMoney(account.account_size)}`}
          tone={s.cumulativeProfit >= 0 ? "profit" : "loss"}
        />
        <StatCard
          label="P&L du jour"
          value={fmtMoney(s.todayPnl, { sign: true })}
          tone={s.todayPnl > 0 ? "profit" : s.todayPnl < 0 ? "loss" : "neutral"}
        />
        <StatCard
          label="Distance à l'objectif"
          value={s.distanceToTarget === 0 ? "OBJECTIF ✓" : fmtMoney(s.distanceToTarget)}
          sub={`${targetPct} % de ${fmtMoney(account.profit_target)}`}
          tone={s.distanceToTarget === 0 ? "profit" : "neutral"}
        />
        <StatCard
          label="Gain max prochain trade"
          value={fmtMoney(s.maxNextGain)}
          sub={`Règle de consistance ${account.consistency_pct} %`}
          tone={s.maxNextGain === 0 && s.cumulativeProfit <= 0 ? "warn" : "neutral"}
        />
      </div>

      {/* Jauge de drawdown */}
      <FloorGauge
        distance={s.distanceToFloor}
        ratio={s.floorRatio}
        floor={s.floor}
        breached={s.breached}
      />

      {/* Courbe d'équity */}
      <EquityChart
        data={s.equityCurve}
        accountSize={account.account_size}
        profitTarget={account.profit_target}
      />

      {/* Ligne 2 : statistiques de performance */}
      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <StatCard
          label="Win rate global"
          value={fmtPct(s.winRateAll)}
          sub={`10 derniers : ${fmtPct(s.winRateLast10)} · 20 derniers : ${fmtPct(s.winRateLast20)}`}
        />
        <StatCard
          label="RRR moyen (gagnants)"
          value={s.avgWinRrr === null ? "—" : `${fmtNumber(s.avgWinRrr)}R`}
          sub={`Cible : ${fmtNumber(account.target_rrr)}R`}
          tone={
            s.avgWinRrr === null ? "neutral" : s.avgWinRrr >= account.target_rrr ? "profit" : "warn"
          }
        />
        <StatCard
          label="Profit factor"
          value={s.profitFactor === null ? "—" : fmtNumber(s.profitFactor)}
          tone={
            s.profitFactor === null ? "neutral" : s.profitFactor >= 1.5 ? "profit" : s.profitFactor >= 1 ? "warn" : "loss"
          }
        />
        <StatCard
          label="Alertes"
          value={`${s.softBreachCount + s.consistencyViolationCount}`}
          sub={`${s.softBreachCount} soft breach · ${s.consistencyViolationCount} consistance`}
          tone={s.softBreachCount > 0 ? "loss" : s.consistencyViolationCount > 0 ? "warn" : "profit"}
        />
      </div>

      <p className="text-xs text-fg-faint">
        {s.trades.length} trade{s.trades.length > 1 ? "s" : ""} · profit cumulé{" "}
        {fmtMoney(s.cumulativeProfit, { sign: true })} · floor{" "}
        {account.drawdown_type === "trailing_eod" ? "recalculé à chaque clôture de journée" : "fixe"}
      </p>
    </div>
  );
}
