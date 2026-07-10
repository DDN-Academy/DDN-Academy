import type { Metadata } from "next";
import { redirect } from "next/navigation";
import { ManageButton, UpgradeButton } from "@/components/BillingClient";
import { fmtDate } from "@/lib/format";
import { isPro, PLANS } from "@/lib/plans";
import { createClient } from "@/lib/supabase/server";
import type { Subscription } from "@/lib/types";

export const metadata: Metadata = { title: "Abonnement" };
export const dynamic = "force-dynamic";

export default async function BillingPage({
  searchParams,
}: {
  searchParams: { success?: string; canceled?: string };
}) {
  const supabase = createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) redirect("/login");

  const { data: sub } = await supabase
    .from("subscriptions")
    .select("*")
    .eq("user_id", user.id)
    .maybeSingle<Subscription>();

  const pro = isPro(sub);
  const trialing = sub?.status === "trialing";

  return (
    <div className="max-w-2xl">
      <h1 className="mb-6 text-2xl font-bold">Abonnement</h1>

      {searchParams.success && (
        <p className="mb-4 rounded-lg border border-profit/40 bg-profit/10 p-3 text-sm text-profit">
          ✓ Paiement confirmé ! Votre plan Pro s&apos;active en quelques secondes (webhook Stripe).
          Rafraîchissez la page si besoin.
        </p>
      )}
      {searchParams.canceled && (
        <p className="mb-4 rounded-lg border border-warn/40 bg-warn/10 p-3 text-sm text-warn">
          Paiement annulé — vous restez sur votre plan actuel.
        </p>
      )}

      {/* Statut actuel */}
      <div className="card mb-6">
        <p className="text-xs font-medium uppercase tracking-wider text-fg-muted">Plan actuel</p>
        <p className="mt-1 text-xl font-bold">
          {pro ? (
            <span className="text-profit">Pro {trialing && "— essai gratuit"}</span>
          ) : (
            "Gratuit"
          )}
        </p>
        {pro && sub?.trial_end && trialing && (
          <p className="mt-1 text-sm text-fg-muted">
            Fin de l&apos;essai : {fmtDate(sub.trial_end)} — annulable à tout moment avant, sans
            débit.
          </p>
        )}
        {pro && sub?.current_period_end && !trialing && (
          <p className="mt-1 text-sm text-fg-muted">
            {sub.cancel_at_period_end
              ? `Annulation programmée — accès Pro jusqu'au ${fmtDate(sub.current_period_end)}`
              : `Prochain renouvellement : ${fmtDate(sub.current_period_end)}`}
          </p>
        )}
        {pro && (
          <div className="mt-4">
            <ManageButton />
          </div>
        )}
      </div>

      {/* Comparatif des plans */}
      <div className="grid gap-4 sm:grid-cols-2">
        <div className={`card ${!pro ? "ring-1 ring-accent" : ""}`}>
          <h2 className="font-semibold">Gratuit</h2>
          <p className="mb-4 font-mono text-2xl font-bold">{PLANS.free.price}</p>
          <ul className="space-y-2 text-sm text-fg-muted">
            <li>✓ 1 compte prop firm</li>
            <li>✓ 20 trades / mois</li>
            <li>✓ Dashboard temps réel complet</li>
            <li>✓ Calculateur de position sizing</li>
            <li className="text-fg-faint">✗ Export CSV</li>
            <li className="text-fg-faint">✗ Comptes illimités</li>
          </ul>
        </div>
        <div className={`card ${pro ? "ring-1 ring-profit" : ""}`}>
          <h2 className="font-semibold">
            Pro <span className="text-xs font-normal text-fg-muted">essai 7 jours offert</span>
          </h2>
          <p className="mb-4 font-mono text-2xl font-bold">{PLANS.pro.price}</p>
          <ul className="mb-5 space-y-2 text-sm text-fg-muted">
            <li>✓ Comptes prop firm illimités</li>
            <li>✓ Trades illimités</li>
            <li>✓ Export CSV de l&apos;historique</li>
            <li>✓ Dashboard temps réel complet</li>
            <li>✓ Rapports (bientôt)</li>
            <li>✓ Annulation en 2 clics</li>
          </ul>
          {!pro && <UpgradeButton label="Essayer Pro 7 jours gratuits" />}
          {pro && <p className="text-sm font-semibold text-profit">Votre plan actuel ✓</p>}
        </div>
      </div>

      <p className="mt-4 text-xs text-fg-faint">
        Paiements sécurisés par Stripe. Aucune donnée bancaire ne transite par nos serveurs.
      </p>
    </div>
  );
}
