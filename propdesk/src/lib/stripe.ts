/** Client Stripe côté serveur — jamais importé côté client. */
import Stripe from "stripe";

let stripeClient: Stripe | null = null;

export function getStripe(): Stripe {
  if (!stripeClient) {
    const key = process.env.STRIPE_SECRET_KEY;
    if (!key) throw new Error("STRIPE_SECRET_KEY manquante dans les variables d'environnement.");
    stripeClient = new Stripe(key, { apiVersion: "2024-06-20" });
  }
  return stripeClient;
}

export function siteUrl(): string {
  return process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3000";
}
