/**
 * Définition des plans d'abonnement et helpers de gating.
 * ⚠️ Ces limites sont AUSSI appliquées côté base (policies RLS,
 * voir supabase/schema.sql) — ici c'est uniquement pour l'UX.
 */
import type { Subscription } from "./types";

export const PLANS = {
  free: {
    name: "Gratuit",
    maxAccounts: 1,
    maxTradesPerMonth: 20,
    csvExport: false,
    price: "0 €",
  },
  pro: {
    name: "Pro",
    maxAccounts: Infinity,
    maxTradesPerMonth: Infinity,
    csvExport: true,
    price: "15 €/mois",
    trialDays: 7,
  },
} as const;

/** Abonnement Pro actif (payant ou en période d'essai). */
export function isPro(sub: Subscription | null | undefined): boolean {
  return !!sub && sub.plan === "pro" && ["active", "trialing"].includes(sub.status);
}

export function planLimits(sub: Subscription | null | undefined) {
  return isPro(sub) ? PLANS.pro : PLANS.free;
}
