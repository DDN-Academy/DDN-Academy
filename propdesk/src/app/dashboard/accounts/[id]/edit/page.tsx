import type { Metadata } from "next";
import { notFound } from "next/navigation";
import AccountForm from "@/components/AccountForm";
import { createClient } from "@/lib/supabase/server";
import type { PropAccount } from "@/lib/types";

export const metadata: Metadata = { title: "Modifier le compte" };

export default async function EditAccountPage({ params }: { params: { id: string } }) {
  const supabase = createClient();
  const { data: account } = await supabase
    .from("prop_accounts")
    .select("*")
    .eq("id", params.id)
    .maybeSingle<PropAccount>();

  if (!account) notFound();

  return (
    <div>
      <h1 className="mb-2 text-2xl font-bold">Modifier « {account.name} »</h1>
      <p className="mb-6 text-sm text-fg-muted">
        Les calculs de tous les trades existants sont recalculés avec les nouvelles règles.
      </p>
      <AccountForm account={account} />
    </div>
  );
}
