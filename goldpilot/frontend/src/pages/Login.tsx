import { useState, type FormEvent } from "react";
import { api, ApiError } from "../lib/api";
import { useTitre } from "../lib/hooks";

export function Login({ onSuccess }: { onSuccess: () => void }) {
  useTitre("Connexion");
  const [mdp, setMdp] = useState("");
  const [erreur, setErreur] = useState<string | null>(null);
  const [enCours, setEnCours] = useState(false);

  async function envoyer(e: FormEvent) {
    e.preventDefault();
    setErreur(null);
    setEnCours(true);
    try {
      await api.post("/api/auth/login", { password: mdp });
      setMdp("");
      onSuccess();
    } catch (err) {
      if (err instanceof ApiError && err.status === 401) setErreur("Mot de passe incorrect.");
      else setErreur(err instanceof ApiError ? err.message : "Erreur inattendue.");
    } finally {
      setEnCours(false);
    }
  }

  return (
    <div className="center-page">
      <main className="card login-card" id="contenu">
        <div className="brand">
          <img src={`${import.meta.env.BASE_URL}icon.svg`} alt="" width={32} height={32} />
          <span>GoldPilot</span>
        </div>
        <h1 style={{ fontSize: "1.2rem" }}>Connexion</h1>
        <p className="muted small">
          Entre le mot de passe de ton site GoldPilot. GoldPilot ne te demandera jamais tes mots de passe TradingView, FundedNext ou
          Tradovate.
        </p>
        <form onSubmit={envoyer} data-testid="form-connexion" noValidate>
          <div className="field">
            <label htmlFor="mdp">Mot de passe GoldPilot</label>
            <input
              id="mdp"
              type="password"
              autoComplete="current-password"
              value={mdp}
              onChange={(e) => setMdp(e.target.value)}
              required
              maxLength={200}
              data-testid="champ-mot-de-passe"
              aria-invalid={erreur ? true : undefined}
              aria-describedby={erreur ? "erreur-connexion" : undefined}
            />
          </div>
          {erreur ? (
            <div className="msg bad" role="alert" id="erreur-connexion" data-testid="erreur-connexion">
              {erreur}
            </div>
          ) : null}
          <button type="submit" className="btn primary" style={{ width: "100%" }} disabled={enCours || mdp.length === 0} data-testid="bouton-connexion">
            {enCours ? "Connexion…" : "Se connecter"}
          </button>
        </form>
        <p className="muted small" style={{ marginTop: 14, marginBottom: 0 }}>
          5 essais maximum par quart d'heure. Mot de passe oublié : un nouveau hachage doit être placé dans ADMIN_PASSWORD_HASH sur le serveur
          (voir la documentation de déploiement).
        </p>
      </main>
    </div>
  );
}
