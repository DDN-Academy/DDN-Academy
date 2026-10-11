import { useCallback, useEffect, useState } from "react";
import { BrowserRouter, HashRouter, Link, Navigate, Route, Routes, useLocation, useNavigate } from "react-router-dom";
import { api, ApiError, onUnauthorized } from "./lib/api";
import { DashboardProvider } from "./lib/dashboard";
import { cheminInterne } from "./lib/navigation";
import { Layout } from "./components/Layout";
import { Banner } from "./components/ui";
import { Login } from "./pages/Login";
import { Home } from "./pages/Home";
import { SignalDetail } from "./pages/SignalDetail";
import { History } from "./pages/History";
import { Stats } from "./pages/Stats";
import { Journal } from "./pages/Journal";
import { Settings } from "./pages/Settings";
import { Help } from "./pages/Help";

type Auth = "verif" | "ok" | "non" | "injoignable";

function Racine() {
  const [auth, setAuth] = useState<Auth>("verif");
  const nav = useNavigate();
  const loc = useLocation();

  const verifier = useCallback(async () => {
    try {
      await api.get("/api/auth/me");
      setAuth("ok");
    } catch (e) {
      setAuth(e instanceof ApiError && e.status === 401 ? "non" : "injoignable");
    }
  }, []);

  useEffect(() => {
    void verifier();
  }, [verifier]);
  useEffect(() => onUnauthorized(() => setAuth("non")), []);

  if (auth === "verif") {
    return (
      <div className="center-page">
        <p className="loading" role="status">
          Chargement de GoldPilot…
        </p>
      </div>
    );
  }
  if (auth === "injoignable") {
    return (
      <div className="center-page">
        <div className="login-card">
          <Banner ton="bad" titre="Serveur injoignable" testid="bandeau-serveur-injoignable" role="alert">
            <p>Impossible de joindre le serveur GoldPilot. Vérifie ta connexion internet, puis réessaie.</p>
          </Banner>
          <button type="button" className="btn primary" onClick={() => void verifier()}>
            Réessayer
          </button>
        </div>
      </div>
    );
  }
  if (auth === "non") {
    if (loc.pathname !== "/connexion") {
      const suite = cheminInterne(loc.pathname + loc.search);
      return <Navigate to={`/connexion${suite !== "/" ? `?suite=${encodeURIComponent(suite)}` : ""}`} replace />;
    }
    return (
      <Login
        onSuccess={() => {
          setAuth("ok");
          nav(cheminInterne(new URLSearchParams(loc.search).get("suite")), { replace: true });
        }}
      />
    );
  }

  const deconnexion = async () => {
    try {
      await api.post("/api/auth/logout");
    } catch {
      /* même en cas d'erreur, on revient à la connexion */
    }
    setAuth("non");
    nav("/connexion", { replace: true });
  };

  return (
    <DashboardProvider>
      <Routes>
        <Route path="/connexion" element={<Navigate to="/" replace />} />
        <Route element={<Layout onLogout={() => void deconnexion()} />}>
          <Route index element={<Home />} />
          <Route path="signal/:id" element={<SignalDetail />} />
          <Route path="historique" element={<History />} />
          <Route path="statistiques" element={<Stats />} />
          <Route path="journal" element={<Journal />} />
          <Route path="reglages" element={<Settings />} />
          <Route path="aide" element={<Help />} />
          <Route path="*" element={<Introuvable />} />
        </Route>
      </Routes>
    </DashboardProvider>
  );
}

function Introuvable() {
  return (
    <div className="card">
      <h1>Page introuvable</h1>
      <p>
        Cette adresse n'existe pas. <Link to="/">Retour à l'accueil</Link>
      </p>
    </div>
  );
}

export function App() {
  // Démonstration hébergée comme page statique : routes dans le fragment d'URL (#/historique…).
  const Router = import.meta.env.VITE_DEMO === "1" ? HashRouter : BrowserRouter;
  return (
    <Router>
      <Racine />
    </Router>
  );
}
