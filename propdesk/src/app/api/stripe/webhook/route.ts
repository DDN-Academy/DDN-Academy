/**
 * Webhook Stripe → synchronise la table `subscriptions` (source de vérité
 * du gating free/pro). Écrit avec la clé service_role (bypass RLS).
 *
 * Événements gérés :
 *  - checkout.session.completed        → active le plan Pro
 *  - customer.subscription.updated     → statut, période, annulation planifiée
 *  - customer.subscription.deleted     → retour au plan gratuit
 */
import { NextResponse } from "next/server";
import type Stripe from "stripe";
import { getStripe } from "@/lib/stripe";
import { createAdminClient } from "@/lib/supabase/server";

export const dynamic = "force-dynamic";

function toIso(epoch: number | null | undefined): string | null {
  return epoch ? new Date(epoch * 1000).toISOString() : null;
}

/** Met à jour la ligne subscriptions d'un utilisateur à partir de l'objet Stripe. */
async function syncSubscription(userId: string, sub: Stripe.Subscription) {
  const admin = createAdminClient();
  const isActive = ["active", "trialing"].includes(sub.status);
  const { error } = await admin.from("subscriptions").upsert(
    {
      user_id: userId,
      plan: isActive ? "pro" : "free",
      status: sub.status,
      stripe_customer_id: typeof sub.customer === "string" ? sub.customer : sub.customer.id,
      stripe_subscription_id: sub.id,
      current_period_end: toIso(sub.current_period_end),
      trial_end: toIso(sub.trial_end),
      cancel_at_period_end: sub.cancel_at_period_end,
    },
    { onConflict: "user_id" },
  );
  if (error) throw new Error(`Supabase upsert failed: ${error.message}`);
}

/** Retrouve l'utilisateur Supabase associé à un abonnement Stripe. */
function userIdFromSubscription(sub: Stripe.Subscription): string | null {
  return sub.metadata?.supabase_user_id ?? null;
}

export async function POST(request: Request) {
  const secret = process.env.STRIPE_WEBHOOK_SECRET;
  if (!secret) {
    return NextResponse.json({ error: "STRIPE_WEBHOOK_SECRET non configuré" }, { status: 500 });
  }

  const signature = request.headers.get("stripe-signature");
  if (!signature) {
    return NextResponse.json({ error: "Signature manquante" }, { status: 400 });
  }

  const stripe = getStripe();
  const payload = await request.text();

  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(payload, signature, secret);
  } catch (err) {
    const msg = err instanceof Error ? err.message : "signature invalide";
    return NextResponse.json({ error: `Webhook non vérifié : ${msg}` }, { status: 400 });
  }

  try {
    switch (event.type) {
      case "checkout.session.completed": {
        const session = event.data.object as Stripe.Checkout.Session;
        const userId = session.client_reference_id;
        if (userId && session.subscription) {
          const sub = await stripe.subscriptions.retrieve(
            typeof session.subscription === "string"
              ? session.subscription
              : session.subscription.id,
          );
          await syncSubscription(userId, sub);
        }
        break;
      }

      case "customer.subscription.updated":
      case "customer.subscription.deleted": {
        const sub = event.data.object as Stripe.Subscription;
        let userId = userIdFromSubscription(sub);
        // Fallback : retrouve l'utilisateur via le customer_id déjà stocké
        if (!userId) {
          const admin = createAdminClient();
          const customerId = typeof sub.customer === "string" ? sub.customer : sub.customer.id;
          const { data } = await admin
            .from("subscriptions")
            .select("user_id")
            .eq("stripe_customer_id", customerId)
            .maybeSingle();
          userId = data?.user_id ?? null;
        }
        if (userId) await syncSubscription(userId, sub);
        break;
      }

      default:
        // Événement non géré : on répond 200 pour éviter les retries Stripe
        break;
    }
  } catch (err) {
    const msg = err instanceof Error ? err.message : "erreur interne";
    // 500 → Stripe réessaiera automatiquement
    return NextResponse.json({ error: msg }, { status: 500 });
  }

  return NextResponse.json({ received: true });
}
