/**
 * Ouvre le portail de facturation Stripe : changement de carte,
 * annulation, factures — Stripe gère tout.
 */
import { NextResponse } from "next/server";
import { getStripe, siteUrl } from "@/lib/stripe";
import { createClient } from "@/lib/supabase/server";
import type { Subscription } from "@/lib/types";

export async function POST() {
  const supabase = createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) {
    return NextResponse.json({ error: "Non authentifié" }, { status: 401 });
  }

  const { data: sub } = await supabase
    .from("subscriptions")
    .select("*")
    .eq("user_id", user.id)
    .maybeSingle<Subscription>();

  if (!sub?.stripe_customer_id) {
    return NextResponse.json({ error: "Aucun abonnement Stripe trouvé" }, { status: 400 });
  }

  const stripe = getStripe();
  const session = await stripe.billingPortal.sessions.create({
    customer: sub.stripe_customer_id,
    return_url: `${siteUrl()}/dashboard/billing`,
  });

  return NextResponse.json({ url: session.url });
}
