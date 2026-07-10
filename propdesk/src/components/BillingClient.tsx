"use client";

/** Boutons d'action Stripe : upgrade (Checkout) et gestion (portail). */
import { useState } from "react";

export function UpgradeButton({ label = "Passer au plan Pro" }: { label?: string }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleUpgrade() {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/stripe/checkout", { method: "POST" });
      const data = await res.json();
      if (!res.ok || !data.url) throw new Error(data.error ?? "Erreur Stripe");
      window.location.href = data.url;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Une erreur est survenue.");
      setLoading(false);
    }
  }

  return (
    <div>
      <button type="button" onClick={handleUpgrade} disabled={loading} className="btn-primary w-full">
        {loading ? "Redirection vers Stripe…" : label}
      </button>
      {error && <p className="mt-2 text-sm text-loss">{error}</p>}
    </div>
  );
}

export function ManageButton() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handlePortal() {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/stripe/portal", { method: "POST" });
      const data = await res.json();
      if (!res.ok || !data.url) throw new Error(data.error ?? "Erreur Stripe");
      window.location.href = data.url;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Une erreur est survenue.");
      setLoading(false);
    }
  }

  return (
    <div>
      <button type="button" onClick={handlePortal} disabled={loading} className="btn-ghost w-full">
        {loading ? "Redirection…" : "Gérer mon abonnement (carte, annulation, factures)"}
      </button>
      {error && <p className="mt-2 text-sm text-loss">{error}</p>}
    </div>
  );
}
