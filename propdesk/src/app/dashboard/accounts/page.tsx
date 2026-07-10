import type { Metadata } from "next";
import Link from "next/link";
import { redirect } from "next/navigation";
import { createClient } from "@/lib/supabase/server";
import { isPro, PLANS } from "@/lib/plans";
import { fmtMoney } from "@/lib/format";
import type { PropAccount, Subscription } from "@/lib/types";
import DeleteAccountButton from "@/components/DeleteAccountButton";

export const metadata: Metadata = { title: "Comptes prop firm" };

export default async function AccountsPage() {
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

  const pro = isPro(subscription);
  const atLimit = !pro && (accounts?.length ?? 0) >= PLANS.free.maxAccounts;

  return (
    <div>
      <div className="mb-6 flex flex-wrap items-center justify-between gap-3">
        <h1 className="text-2xl font-bold">Comptes prop firm</h1>
        {atLimit ? (
          <Link href="/dashboard/billing" className="btn-ghost">
            Plan gratuit : 1 compte max — passer Pro
          </Link>
        ) : (
          <Link href="/dashboard/accounts/new" className="btn-primary">
            + Nouveau compte
          </Link>
        )}
      </div>

      {!accounts || accounts.length === 0 ? (
        <div className="card text-center">
          <p className="mb-2 text-lg font-semibold">Aucun compte configuré</p>
          <p className="mb-5 text-sm text-fg-muted">
            Configurez les règles de votre challenge (drawdown, soft breach, consistance) pour
            activer le tableau de bord.
          </p>
          <Link href="/dashboard/accounts/new" className="btn-primary">
            Configurer mon premier compte
          </Link>
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2">
          {accounts.map((a) => (
            <div key={a.id} className="card">
              <div className="mb-3 flex items-start justify-between">
                <div>
                  <h2 className="font-semibold">{a.name}</h2>
                  <p className="text-xs text-fg-muted">{a.firm ?? "—"}</p>
                </div>
                <span className="rounded bg-ink-800 px-2 py-0.5 font-mono text-[10px] uppercase text-fg-muted">
                  {a.drawdown_type === "trailing_eod" ? "Trailing EOD" : "DD fixe"}
                </span>
              </div>
              <dl className="mb-4 grid grid-cols-2 gap-x-4 gap-y-2 text-sm">
                <div>
                  <dt className="text-xs text-fg-faint">Taille</dt>
                  <dd className="font-mono">{fmtMoney(a.account_size)}</dd>
                </div>
                <div>
                  <dt className="text-xs text-fg-faint">Drawdown</dt>
                  <dd className="font-mono">{fmtMoney(a.drawdown_limit)}</dd>
                </div>
                <div>
                  <dt className="text-xs text-fg-faint">Soft breach / trade</dt>
                  <dd className="font-mono">{fmtMoney(a.soft_breach_limit)}</dd>
                </div>
                <div>
                  <dt className="text-xs text-fg-faint">Consistance</dt>
                  <dd className="font-mono">{a.consistency_pct} %</dd>
                </div>
                <div>
                  <dt className="text-xs text-fg-faint">Objectif</dt>
                  <dd className="font-mono">{fmtMoney(a.profit_target)}</dd>
                </div>
                <div>
                  <dt className="text-xs text-fg-faint">Instrument</dt>
                  <dd className="font-mono">{a.default_symbol}</dd>
                </div>
              </dl>
              <div className="flex gap-2">
                <Link href={`/dashboard?account=${a.id}`} className="btn-primary flex-1">
                  Dashboard
                </Link>
                <Link href={`/dashboard/accounts/${a.id}/edit`} className="btn-ghost">
                  Modifier
                </Link>
                <DeleteAccountButton accountId={a.id} accountName={a.name} />
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
