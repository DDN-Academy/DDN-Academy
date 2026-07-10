"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { createClient } from "@/lib/supabase/client";

export default function DeleteAccountButton({
  accountId,
  accountName,
}: {
  accountId: string;
  accountName: string;
}) {
  const supabase = createClient();
  const router = useRouter();
  const [loading, setLoading] = useState(false);

  async function handleDelete() {
    if (
      !window.confirm(
        `Supprimer « ${accountName} » et TOUS ses trades ? Cette action est irréversible.`,
      )
    )
      return;
    setLoading(true);
    const { error } = await supabase.from("prop_accounts").delete().eq("id", accountId);
    setLoading(false);
    if (error) window.alert(error.message);
    else router.refresh();
  }

  return (
    <button type="button" onClick={handleDelete} disabled={loading} className="btn-danger">
      {loading ? "…" : "Suppr."}
    </button>
  );
}
