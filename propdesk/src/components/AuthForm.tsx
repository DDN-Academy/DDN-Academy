"use client";

/**
 * Formulaire d'authentification partagé login / signup :
 * email + mot de passe, et OAuth Google.
 */
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Suspense, useState } from "react";
import { createClient } from "@/lib/supabase/client";

function GoogleIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" aria-hidden>
      <path
        fill="#4285F4"
        d="M23.5 12.3c0-.9-.1-1.5-.3-2.2H12v4.1h6.5c-.1 1.1-.8 2.7-2.4 3.8l-.02.2 3.5 2.7.2.02c2.2-2 3.5-5 3.5-8.6"
      />
      <path
        fill="#34A853"
        d="M12 24c3.2 0 5.9-1 7.9-2.9l-3.7-2.9c-1 .7-2.4 1.2-4.2 1.2-3.1 0-5.8-2-6.7-4.9l-.2.01-3.6 2.8-.05.1C3.4 21.4 7.4 24 12 24"
      />
      <path
        fill="#FBBC05"
        d="M5.3 14.5c-.25-.7-.4-1.5-.4-2.5s.15-1.8.4-2.5l-.01-.2-3.7-2.8-.1.06C.5 8.2 0 10 0 12s.5 3.8 1.4 5.4l3.9-2.9"
      />
      <path
        fill="#EA4335"
        d="M12 4.6c2.2 0 3.7 1 4.5 1.8l3.3-3.2C17.9 1.2 15.2 0 12 0 7.4 0 3.4 2.6 1.4 6.6l3.8 2.9c1-2.9 3.7-4.9 6.8-4.9"
      />
    </svg>
  );
}

function AuthFormInner({ mode }: { mode: "login" | "signup" }) {
  const supabase = createClient();
  const router = useRouter();
  const params = useSearchParams();
  const next = params.get("next") ?? "/dashboard";

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [info, setInfo] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setInfo(null);
    setLoading(true);
    try {
      if (mode === "signup") {
        const { data, error } = await supabase.auth.signUp({
          email,
          password,
          options: {
            data: { full_name: fullName },
            emailRedirectTo: `${window.location.origin}/auth/callback`,
          },
        });
        if (error) throw error;
        // Si la confirmation d'email est activée, pas de session immédiate
        if (!data.session) {
          setInfo("Compte créé ! Vérifiez votre boîte mail pour confirmer votre adresse.");
          return;
        }
      } else {
        const { error } = await supabase.auth.signInWithPassword({ email, password });
        if (error) throw error;
      }
      router.push(next);
      router.refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Une erreur est survenue.");
    } finally {
      setLoading(false);
    }
  }

  async function handleGoogle() {
    setError(null);
    const { error } = await supabase.auth.signInWithOAuth({
      provider: "google",
      options: {
        redirectTo: `${window.location.origin}/auth/callback?next=${encodeURIComponent(next)}`,
      },
    });
    if (error) setError(error.message);
  }

  return (
    <div className="card w-full max-w-md">
      <h1 className="mb-1 text-xl font-bold">
        {mode === "login" ? "Connexion" : "Créer un compte"}
      </h1>
      <p className="mb-6 text-sm text-fg-muted">
        {mode === "login"
          ? "Reprenez le contrôle de votre challenge."
          : "Gratuit — 1 compte prop firm, 20 trades/mois."}
      </p>

      <button type="button" onClick={handleGoogle} className="btn-ghost w-full">
        <GoogleIcon />
        Continuer avec Google
      </button>

      <div className="my-5 flex items-center gap-3 text-xs text-fg-faint">
        <div className="h-px flex-1 bg-ink-700" />
        ou par email
        <div className="h-px flex-1 bg-ink-700" />
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        {mode === "signup" && (
          <div>
            <label htmlFor="fullName" className="field-label">
              Nom complet
            </label>
            <input
              id="fullName"
              type="text"
              className="field"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              placeholder="Jean Dupont"
              autoComplete="name"
            />
          </div>
        )}
        <div>
          <label htmlFor="email" className="field-label">
            Email
          </label>
          <input
            id="email"
            type="email"
            required
            className="field"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="vous@exemple.com"
            autoComplete="email"
          />
        </div>
        <div>
          <label htmlFor="password" className="field-label">
            Mot de passe
          </label>
          <input
            id="password"
            type="password"
            required
            minLength={8}
            className="field"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="8 caractères minimum"
            autoComplete={mode === "login" ? "current-password" : "new-password"}
          />
        </div>

        {error && <p className="text-sm text-loss">{error}</p>}
        {info && <p className="text-sm text-profit">{info}</p>}

        <button type="submit" disabled={loading} className="btn-primary w-full">
          {loading ? "…" : mode === "login" ? "Se connecter" : "Créer mon compte"}
        </button>
      </form>

      <p className="mt-5 text-center text-sm text-fg-muted">
        {mode === "login" ? (
          <>
            Pas encore de compte ?{" "}
            <Link href="/signup" className="text-accent hover:underline">
              Inscription
            </Link>
          </>
        ) : (
          <>
            Déjà inscrit ?{" "}
            <Link href="/login" className="text-accent hover:underline">
              Connexion
            </Link>
          </>
        )}
      </p>
    </div>
  );
}

export default function AuthForm({ mode }: { mode: "login" | "signup" }) {
  // useSearchParams impose une frontière Suspense en App Router
  return (
    <Suspense>
      <AuthFormInner mode={mode} />
    </Suspense>
  );
}
