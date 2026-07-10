/**
 * Crée une session Stripe Checkout pour l'abonnement Pro
 * (mensuel, essai gratuit de 7 jours) et redirige l'utilisateur.
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

  const priceId = process.env.STRIPE_PRICE_ID_PRO;
  if (!priceId) {
    return NextResponse.json({ error: "STRIPE_PRICE_ID_PRO non configuré" }, { status: 500 });
  }

  const stripe = getStripe();

  // Réutilise le customer Stripe existant si l'utilisateur en a déjà un
  const { data: sub } = await supabase
    .from("subscriptions")
    .select("*")
    .eq("user_id", user.id)
    .maybeSingle<Subscription>();

  // Un seul essai gratuit par client : pas de nouvel essai si déjà consommé
  const alreadyTrialed = !!sub?.trial_end;

  const session = await stripe.checkout.sessions.create({
    mode: "subscription",
    customer: sub?.stripe_customer_id ?? undefined,
    customer_email: sub?.stripe_customer_id ? undefined : (user.email ?? undefined),
    client_reference_id: user.id,
    line_items: [{ price: priceId, quantity: 1 }],
    subscription_data: {
      ...(alreadyTrialed ? {} : { trial_period_days: 7 }),
      metadata: { supabase_user_id: user.id },
    },
    allow_promotion_codes: true,
    success_url: `${siteUrl()}/dashboard/billing?success=1`,
    cancel_url: `${siteUrl()}/dashboard/billing?canceled=1`,
  });

  return NextResponse.json({ url: session.url });
}
