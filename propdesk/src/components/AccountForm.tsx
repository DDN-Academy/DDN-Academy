"use client";

/**
 * Formulaire de configuration d'un compte prop firm (création + édition).
 * Tous les paramètres du challenge saisis ici alimentent ensuite les calculs
 * (drawdown, soft breach, consistance, objectif…).
 */
import { useRouter } from "next/navigation";
import { useState } from "react";
import { CONTRACT_SPECS, getContractSpec } from "@/lib/contracts";
import { createClient } from "@/lib/supabase/client";
import type { DrawdownType, PropAccount } from "@/lib/types";

const CUSTOM = "CUSTOM";

interface FormState {
  name: string;
  firm: string;
  account_size: string;
  drawdown_limit: string;
  drawdown_type: DrawdownType;
  soft_breach_limit: string;
  consistency_pct: string;
  profit_target: string;
  target_rrr: string;
  symbol: string;
  tick_size: string;
  tick_value: string;
}

export default function AccountForm({ account }: { account?: PropAccount }) {
  const supabase = createClient();
  const router = useRouter();

  const knownSymbol = account ? !!getContractSpec(account.default_symbol) : true;
  const [form, setForm] = useState<FormState>({
    name: account?.name ?? "",
    firm: account?.firm ?? "",
    account_size: account ? String(account.account_size) : "50000",
    drawdown_limit: account ? String(account.drawdown_limit) : "2000",
    drawdown_type: account?.drawdown_type ?? "trailing_eod",
    soft_breach_limit: account ? String(account.soft_breach_limit) : "1000",
    consistency_pct: account ? String(account.consistency_pct) : "40",
    profit_target: account ? String(account.profit_target) : "3000",
    target_rrr: account ? String(account.target_rrr) : "2",
    symbol: account ? (knownSymbol ? account.default_symbol : CUSTOM) : "MNQ",
    tick_size: account ? String(account.default_tick_size) : "0.25",
    tick_value: account ? String(account.default_tick_value) : "0.5",
  });
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const set = (key: keyof FormState) => (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) =>
    setForm((f) => ({ ...f, [key]: e.target.value }));

  /** Sélection d'un instrument connu → remplit tick size / value. */
  function handleSymbolChange(e: React.ChangeEvent<HTMLSelectElement>) {
    const symbol = e.target.value;
    const spec = getContractSpec(symbol);
    setForm((f) => ({
      ...f,
      symbol,
      tick_size: spec ? String(spec.tickSize) : f.tick_size,
      tick_value: spec ? String(spec.tickValue) : f.tick_value,
    }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);

    const payload = {
      name: form.name.trim(),
      firm: form.firm.trim() || null,
      account_size: Number(form.account_size),
      drawdown_limit: Number(form.drawdown_limit),
      drawdown_type: form.drawdown_type,
      soft_breach_limit: Number(form.soft_breach_limit),
      consistency_pct: Number(form.consistency_pct),
      profit_target: Number(form.profit_target),
      target_rrr: Number(form.target_rrr),
      default_symbol: form.symbol === CUSTOM ? "CUSTOM" : form.symbol,
      default_tick_size: Number(form.tick_size),
      default_tick_value: Number(form.tick_value),
    };

    // Validation minimale côté client (les CHECK SQL protègent côté base)
    const invalid = Object.entries(payload).find(
      ([k, v]) => typeof v === "number" && (!Number.isFinite(v) || v <= 0) && k !== "firm",
    );
    if (invalid) {
      setError(`Valeur invalide pour « ${invalid[0]} » : doit être un nombre positif.`);
      setLoading(false);
      return;
    }

    try {
      if (account) {
        const { error } = await supabase.from("prop_accounts").update(payload).eq("id", account.id);
        if (error) throw error;
      } else {
        const {
          data: { user },
        } = await supabase.auth.getUser();
        if (!user) throw new Error("Session expirée, reconnectez-vous.");
        const { error } = await supabase
          .from("prop_accounts")
          .insert({ ...payload, user_id: user.id });
        if (error) {
          // 42501 = violation de policy RLS → limite du plan gratuit atteinte
          if (error.code === "42501") {
            throw new Error(
              "Plan gratuit : 1 seul compte prop firm. Passez au plan Pro pour des comptes illimités.",
            );
          }
          throw error;
        }
      }
      router.push("/dashboard/accounts");
      router.refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Une erreur est survenue.");
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="card max-w-2xl space-y-6">
      {/* Identité du compte */}
      <div className="grid gap-4 sm:grid-cols-2">
        <div>
          <label htmlFor="name" className="field-label">
            Nom du compte *
          </label>
          <input
            id="name"
            required
            className="field"
            placeholder="FundedNext 50K"
            value={form.name}
            onChange={set("name")}
          />
        </div>
        <div>
          <label htmlFor="firm" className="field-label">
            Prop firm
          </label>
          <input
            id="firm"
            className="field"
            placeholder="FundedNext, Topstep…"
            value={form.firm}
            onChange={set("firm")}
          />
        </div>
      </div>

      {/* Règles du challenge */}
      <fieldset className="space-y-4">
        <legend className="text-sm font-semibold text-fg">Règles du challenge</legend>
        <div className="grid gap-4 sm:grid-cols-2">
          <div>
            <label htmlFor="account_size" className="field-label">
              Taille du compte ($) *
            </label>
            <input
              id="account_size"
              required
              type="number"
              min="1"
              step="any"
              className="field"
              value={form.account_size}
              onChange={set("account_size")}
            />
          </div>
          <div>
            <label htmlFor="profit_target" className="field-label">
              Objectif de profit ($) *
            </label>
            <input
              id="profit_target"
              required
              type="number"
              min="1"
              step="any"
              className="field"
              value={form.profit_target}
              onChange={set("profit_target")}
            />
          </div>
          <div>
            <label htmlFor="drawdown_limit" className="field-label">
              Limite de drawdown ($) *
            </label>
            <input
              id="drawdown_limit"
              required
              type="number"
              min="1"
              step="any"
              className="field"
              value={form.drawdown_limit}
              onChange={set("drawdown_limit")}
            />
          </div>
          <div>
            <label htmlFor="drawdown_type" className="field-label">
              Type de drawdown *
            </label>
            <select
              id="drawdown_type"
              className="field"
              value={form.drawdown_type}
              onChange={set("drawdown_type")}
            >
              <option value="trailing_eod">Trailing EOD (remonte chaque soir)</option>
              <option value="static">Fixe (ne bouge jamais)</option>
            </select>
          </div>
          <div>
            <label htmlFor="soft_breach_limit" className="field-label">
              Seuil soft breach / trade ($) *
            </label>
            <input
              id="soft_breach_limit"
              required
              type="number"
              min="1"
              step="any"
              className="field"
              value={form.soft_breach_limit}
              onChange={set("soft_breach_limit")}
            />
            <p className="mt-1 text-xs text-fg-faint">Perte maximale autorisée sur un seul trade</p>
          </div>
          <div>
            <label htmlFor="consistency_pct" className="field-label">
              Règle de consistance (%) *
            </label>
            <input
              id="consistency_pct"
              required
              type="number"
              min="1"
              max="100"
              step="any"
              className="field"
              value={form.consistency_pct}
              onChange={set("consistency_pct")}
            />
            <p className="mt-1 text-xs text-fg-faint">
              Aucun trade ne doit dépasser ce % du profit total
            </p>
          </div>
        </div>
      </fieldset>

      {/* Instrument par défaut */}
      <fieldset className="space-y-4">
        <legend className="text-sm font-semibold text-fg">Instrument par défaut</legend>
        <div className="grid gap-4 sm:grid-cols-2">
          <div className="sm:col-span-2">
            <label htmlFor="symbol" className="field-label">
              Contrat *
            </label>
            <select id="symbol" className="field" value={form.symbol} onChange={handleSymbolChange}>
              {CONTRACT_SPECS.map((c) => (
                <option key={c.symbol} value={c.symbol}>
                  {c.label} — tick {c.tickSize} = ${c.tickValue}
                </option>
              ))}
              <option value={CUSTOM}>Autre (personnalisé)</option>
            </select>
          </div>
          <div>
            <label htmlFor="tick_size" className="field-label">
              Tick size (points) *
            </label>
            <input
              id="tick_size"
              required
              type="number"
              min="0"
              step="any"
              className="field"
              value={form.tick_size}
              onChange={set("tick_size")}
              disabled={form.symbol !== CUSTOM}
            />
          </div>
          <div>
            <label htmlFor="tick_value" className="field-label">
              Valeur du tick ($ / contrat) *
            </label>
            <input
              id="tick_value"
              required
              type="number"
              min="0"
              step="any"
              className="field"
              value={form.tick_value}
              onChange={set("tick_value")}
              disabled={form.symbol !== CUSTOM}
            />
          </div>
          <div>
            <label htmlFor="target_rrr" className="field-label">
              RRR cible *
            </label>
            <input
              id="target_rrr"
              required
              type="number"
              min="0.1"
              step="any"
              className="field"
              value={form.target_rrr}
              onChange={set("target_rrr")}
            />
            <p className="mt-1 text-xs text-fg-faint">Utilisé pour les stats et le sizing</p>
          </div>
        </div>
      </fieldset>

      {error && <p className="text-sm text-loss">{error}</p>}

      <div className="flex gap-3">
        <button type="submit" disabled={loading} className="btn-primary">
          {loading ? "…" : account ? "Enregistrer les modifications" : "Créer le compte"}
        </button>
        <button type="button" className="btn-ghost" onClick={() => router.back()}>
          Annuler
        </button>
      </div>
    </form>
  );
}
