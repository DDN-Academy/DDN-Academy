/**
 * Layout authentifié : récupère l'utilisateur + son abonnement côté serveur
 * (le middleware garantit déjà qu'un utilisateur est connecté).
 */
import { redirect } from "next/navigation";
import AppShell from "@/components/AppShell";
import { createClient } from "@/lib/supabase/server";
import { isPro } from "@/lib/plans";
import type { Subscription } from "@/lib/types";

export default async function DashboardLayout({ children }: { children: React.ReactNode }) {
  const supabase = createClient();

  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) redirect("/login");

  const { data: subscription } = await supabase
    .from("subscriptions")
    .select("*")
    .eq("user_id", user.id)
    .maybeSingle<Subscription>();

  return (
    <AppShell email={user.email ?? ""} plan={isPro(subscription) ? "pro" : "free"}>
      {children}
    </AppShell>
  );
}
