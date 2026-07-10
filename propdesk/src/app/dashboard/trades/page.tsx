import type { Metadata } from "next";
import Link from "next/link";
import { redirect } from "next/navigation";
import AccountSelect from "@/components/AccountSelect";
import ExportCsvButton from "@/components/ExportCsvButton";
import TradeForm from "@/components/TradeForm";
import TradesTable from "@/components/TradesTable";
import { computeAccountSnapshot } from "@/lib/calculations";
import { isPro, PLANS } from "@/lib/plans";
import { createClient } from "@/lib/supabase/server";
import type { PropAccount, Subscription, Trade } from "@/lib/types";

export const metadata: Metadata = { title: "Trades" };
export const dynamic = "force-dynamic";

export default async function TradesPage({
  searchParams,
}: {
  searchParams: { account?: string };
}) {
  const supabase = createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) redirect("/login");

  const [{ data: accounts }, { data: subscription }] = await Promise.all([
    supabase
      .from("prop_accounts")
      .select("*")
      .order("created_at", { ascending: true })
      .returns<PropAccount[]>(),
    supabase.from("subscriptions").select("*").eq("user_id", user.id).maybeSingle<Subscription>(),
  ]);

  if (!accounts || accounts.length === 0) {
    return (
      <div className="card mx-auto max-w-md text-center">
        <p className="mb-2 text-lg font-semibold">Configurez d&apos;abord un compte</p>
        <p className="mb-5 text-sm text-fg-muted">
          Les calculs de vos trades dépendent des règles de votre challenge.
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

  const snapshot = computeAccountSnapshot(account, trades ?? []);
  const pro = isPro(subscription);

  // Compteur du plan gratuit : trades saisis ce mois-ci (tous comptes)
  const monthStart = new Date();
  monthStart.setUTCDate(1);
  monthStart.setUTCHours(0, 0, 0, 0);
  const { count: monthCount } = await supabase
    .from("trades")
    .select("*", { count: "exact", head: true })
    .gte("created_at", monthStart.toISOString());

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl font-bold">Trades</h1>
          <p className="text-sm text-fg-muted">{account.name}</p>
        </div>
        <div className="flex items-center gap-3">
          <ExportCsvButton trades={snapshot.trades} accountName={account.name} pro={pro} />
          <AccountSelect
            accounts={accounts.map(({ id, name }) => ({ id, name }))}
            selectedId={account.id}
          />
        </div>
      </div>

      {!pro && (
        <p className="text-xs text-fg-muted">
          Plan gratuit : {monthCount ?? 0} / {PLANS.free.maxTradesPerMonth} trades ce mois-ci —{" "}
          <Link href="/dashboard/billing" className="text-accent hover:underline">
            passer Pro pour l&apos;illimité
          </Link>
        </p>
      )}

      <TradeForm account={account} cumulativeProfit={snapshot.cumulativeProfit} />
      <TradesTable trades={snapshot.trades} />
    </div>
  );
}
