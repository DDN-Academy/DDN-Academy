import { NavLink, Outlet, Link } from "react-router-dom";
import { Banner, Icon } from "./ui";
import { useDashboard } from "../lib/dashboard";
import { ilYa } from "../lib/format";

const NAV = [
  { to: "/", libelle: "Accueil", icone: "home" as const, testid: "nav-accueil", end: true },
  { to: "/historique", libelle: "Historique", icone: "list" as const, testid: "nav-historique", end: false },
  { to: "/statistiques", libelle: "Stats", icone: "chart" as const, testid: "nav-statistiques", end: false },
  { to: "/journal", libelle: "Journal", icone: "journal" as const, testid: "nav-journal", end: false },
  { to: "/reglages", libelle: "Réglages", icone: "settings" as const, testid: "nav-reglages", end: false },
];

export function Layout({ onLogout }: { onLogout: () => void }) {
  const d = useDashboard();
  const dash = d.data;
  // Par sécurité, le bandeau SIMULATION reste affiché tant que le serveur n'a pas confirmé
  // à la fois une stratégie validée ET le mode réel.
  const reel = !!dash && d.joignable && dash.trading.strategie.validee && dash.trading.mode_trading === "reel";
  return (
    <div className="app">
      <a className="skip-link" href="#contenu">
        Aller au contenu
      </a>
      <header className="topbar">
        <div className="topbar-inner">
          <Link to="/" className="brand" data-testid="nav-logo">
            <img src={`${import.meta.env.BASE_URL}icon.svg`} alt="" width={28} height={28} />
            <span>GoldPilot</span>
          </Link>
          <nav className="topnav" aria-label="Navigation principale">
            {NAV.map((n) => (
              <NavLink key={n.to} to={n.to} end={n.end} data-testid={`${n.testid}-haut`}>
                {n.libelle === "Stats" ? "Statistiques" : n.libelle}
              </NavLink>
            ))}
          </nav>
          <div className="topbar-actions">
            <NavLink to="/aide" className="icon-btn" data-testid="nav-aide" aria-label="Aide">
              <Icon name="help" />
            </NavLink>
            <button type="button" className="icon-btn" onClick={onLogout} data-testid="bouton-deconnexion" aria-label="Se déconnecter">
              <Icon name="logout" />
            </button>
          </div>
        </div>
      </header>

      <main id="contenu" tabIndex={-1}>
        {import.meta.env.VITE_DEMO === "1" ? (
          <Banner ton="info" titre="DÉMONSTRATION — données fictives" testid="bandeau-demo" className="compact">
            <p>
              Aperçu du site GoldPilot sans serveur : les signaux, prix et journaux sont des exemples de test, rien n'est réel et
              aucun bouton n'envoie d'action. Le vrai site fonctionnera sur ton serveur (procédure : docs/05).
            </p>
          </Banner>
        ) : null}
        {!d.joignable && !d.chargement ? (
          <Banner ton="bad" titre="Serveur injoignable" testid="bandeau-serveur-injoignable" role="alert">
            <p>
              {d.erreur ? d.erreur.message : "Aucune réponse du serveur."}{" "}
              {d.recuA ? `Dernière réponse ${ilYa(d.ageS)} : les informations affichées ne sont plus fiables.` : ""}
            </p>
          </Banner>
        ) : null}
        {dash?.rejeu ? (
          <Banner
            ton="info"
            titre={`REJEU HISTORIQUE — horloge virtuelle ${dash.rejeu.horloge_paris ?? "inconnue"}, rien n'est réel`}
            testid="bandeau-rejeu"
            className="compact"
          >
            <p>Données XAUUSD passées rejouées : aucun prix ni signal ne correspond au marché actuel.</p>
          </Banner>
        ) : null}
        {!reel ? (
          <Banner ton="warn" titre="SIMULATION — ne pas exécuter sur le compte" testid="bandeau-simulation" className="banner-sim compact">
            <p>
              Stratégie {dash && !dash.trading.strategie.validee ? "NON VALIDÉE" : "non confirmée en réel"} : signaux pour le suivi papier
              uniquement. <Link to="/statistiques">Pourquoi ?</Link>
            </p>
          </Banner>
        ) : null}
        <Outlet />
      </main>

      <nav className="tabbar" aria-label="Navigation principale (mobile)">
        {NAV.map((n) => (
          <NavLink key={n.to} to={n.to} end={n.end} data-testid={n.testid}>
            <Icon name={n.icone} />
            <span>{n.libelle}</span>
          </NavLink>
        ))}
      </nav>
    </div>
  );
}
