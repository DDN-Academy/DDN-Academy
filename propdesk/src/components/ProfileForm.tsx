"use client";

import { useState } from "react";
import { createClient } from "@/lib/supabase/client";
import { fmtDate } from "@/lib/format";

export default function ProfileForm({
  email,
  fullName: initialName,
  createdAt,
  provider,
}: {
  email: string;
  fullName: string;
  createdAt: string;
  provider: string;
}) {
  const supabase = createClient();
  const [fullName, setFullName] = useState(initialName);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSave(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setSaved(false);
    setError(null);
    const {
      data: { user },
    } = await supabase.auth.getUser();
    if (!user) return;
    const { error } = await supabase
      .from("profiles")
      .update({ full_name: fullName || null })
      .eq("id", user.id);
    setLoading(false);
    if (error) setError(error.message);
    else setSaved(true);
  }

  return (
    <div className="card space-y-5">
      <form onSubmit={handleSave} className="space-y-4">
        <div>
          <label className="field-label">Email</label>
          <input className="field opacity-60" value={email} disabled />
          <p className="mt-1 text-xs text-fg-faint">
            Connexion via {provider === "google" ? "Google" : "email / mot de passe"}
          </p>
        </div>
        <div>
          <label htmlFor="fullName" className="field-label">
            Nom complet
          </label>
          <input
            id="fullName"
            className="field"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            placeholder="Votre nom"
          />
        </div>
        {error && <p className="text-sm text-loss">{error}</p>}
        {saved && <p className="text-sm text-profit">Profil enregistré ✓</p>}
        <button type="submit" disabled={loading} className="btn-primary">
          {loading ? "…" : "Enregistrer"}
        </button>
      </form>
      <p className="border-t border-ink-700 pt-4 text-xs text-fg-faint">
        Membre depuis le {fmtDate(createdAt)}
      </p>
    </div>
  );
}
