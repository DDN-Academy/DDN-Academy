import type { Metadata } from "next";
import Link from "next/link";
import { redirect } from "next/navigation";
import AccountSelect from "@/components/AccountSelect";
import SizingCalculator from "@/components/SizingCalculator";
import { createClient } from "@/lib/supabase/server";
import type { PropAccount } from "@/lib/types";

export const metadata: Metadata = { title: "Position sizing" };
export const dynamic = "force-dynamic";

export default async function SizingPage({
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

  if (!accounts || accounts.length === 0) {
    return (
      <div className="card mx-auto max-w-md text-center">
        <p className="mb-2 text-lg font-semibold">Configurez d&apos;abord un compte</p>
        <p className="mb-5 text-sm text-fg-muted">
          Le calculateur utilise le seuil de soft breach de votre challenge.
        </p>
        <Link href="/dashboard/accounts/new" className="btn-primary">
          Configurer mon compte
        </Link>
      </div>
    );
  }

  const account = accounts.find((a) => a.id === searchParams.account) ?? accounts[0];

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl font-bold">Calculateur de position sizing</h1>
          <p className="text-sm text-fg-muted">
            Combien de contrats sans risquer un soft breach — {account.name}
          </p>
        </div>
        <AccountSelect
          accounts={accounts.map(({ id, name }) => ({ id, name }))}
          selectedId={account.id}
        />
      </div>
      <SizingCalculator account={account} />
    </div>
  );
}
