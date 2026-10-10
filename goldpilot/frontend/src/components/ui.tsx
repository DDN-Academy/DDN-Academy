import { useState, type ReactNode } from "react";
import type { Ton } from "../lib/status";

// ------------------------------------------------------------------ icônes (SVG en ligne, aucune police externe)
type IconName =
  | "home"
  | "list"
  | "chart"
  | "journal"
  | "settings"
  | "help"
  | "logout"
  | "ok"
  | "warn"
  | "bad"
  | "info"
  | "neutral"
  | "copy"
  | "download"
  | "bell"
  | "pause"
  | "play"
  | "send";

const PATHS: Record<IconName, ReactNode> = {
  home: <path d="M3 10.5 12 3l9 7.5V20a1 1 0 0 1-1 1h-5v-6h-6v6H4a1 1 0 0 1-1-1z" />,
  list: <path d="M8 6h13M8 12h13M8 18h13M3.5 6h.01M3.5 12h.01M3.5 18h.01" />,
  chart: <path d="M3 3v18h18M7 15l4-4 3 3 6-7" />,
  journal: <path d="M6 3h11a2 2 0 0 1 2 2v16H6a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2zM8 8h7M8 12h7M8 16h4" />,
  settings: (
    <>
      <circle cx="12" cy="12" r="3" />
      <path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z" />
    </>
  ),
  help: (
    <>
      <circle cx="12" cy="12" r="9" />
      <path d="M9.5 9a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .9-1 1.6v.6M12 17h.01" />
    </>
  ),
  logout: <path d="M15 4h4a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1h-4M10 16l-4-4 4-4M6 12h10" />,
  ok: (
    <>
      <circle cx="12" cy="12" r="9" />
      <path d="m8 12.5 2.7 2.7L16.5 9" />
    </>
  ),
  warn: (
    <>
      <path d="M12 3.5 2.5 20h19z" />
      <path d="M12 10v4.5M12 17.3h.01" />
    </>
  ),
  bad: (
    <>
      <circle cx="12" cy="12" r="9" />
      <path d="m9 9 6 6M15 9l-6 6" />
    </>
  ),
  info: (
    <>
      <circle cx="12" cy="12" r="9" />
      <path d="M12 11v5.5M12 7.7h.01" />
    </>
  ),
  neutral: (
    <>
      <circle cx="12" cy="12" r="9" />
      <path d="M8 12h8" />
    </>
  ),
  copy: (
    <>
      <rect x="9" y="9" width="11" height="11" rx="2" />
      <path d="M5 15V5a1 1 0 0 1 1-1h9" />
    </>
  ),
  download: <path d="M12 4v11M7 10l5 5 5-5M5 20h14" />,
  bell: <path d="M6 16V11a6 6 0 1 1 12 0v5l1.5 2h-15zM10 20.5a2 2 0 0 0 4 0" />,
  pause: <path d="M9 5v14M15 5v14" />,
  play: <path d="M7 4.5v15l12-7.5z" />,
  send: <path d="M21 3 3 10.5l7 2.5 2.5 7zM10 13l11-10" />,
};

export function Icon({ name, title }: { name: IconName; title?: string }) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={2}
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden={title ? undefined : true}
      role={title ? "img" : undefined}
      aria-label={title}
      focusable="false"
    >
      {PATHS[name]}
    </svg>
  );
}

export function TonIcon({ ton }: { ton: Ton }) {
  return <Icon name={ton === "ok" ? "ok" : ton === "warn" ? "warn" : ton === "bad" ? "bad" : ton === "info" ? "info" : "neutral"} />;
}

const TON_SR: Record<Ton, string> = { ok: "OK", warn: "Attention", bad: "Problème", info: "Information", neutral: "Neutre" };

// ------------------------------------------------------------------ éléments
export function Badge({ ton, children, testid, wrap }: { ton: Ton; children: ReactNode; testid?: string; wrap?: boolean }) {
  return (
    <span className={`badge ${ton}${wrap ? " wrap" : ""}`} data-testid={testid} data-ton={ton}>
      <TonIcon ton={ton} />
      <span className="sr-only">{TON_SR[ton]} : </span>
      {children}
    </span>
  );
}

export function Banner({
  ton,
  titre,
  children,
  testid,
  className,
  role,
}: {
  ton: Ton;
  titre: ReactNode;
  children?: ReactNode;
  testid?: string;
  className?: string;
  role?: "alert" | "status";
}) {
  return (
    <div className={`banner ${ton}${className ? " " + className : ""}`} data-testid={testid} role={role}>
      <span className="banner-icon">
        <TonIcon ton={ton} />
      </span>
      <div>
        <strong>{titre}</strong>
        {children ? <div>{children}</div> : null}
      </div>
    </div>
  );
}

export function StatusTile({
  label,
  ton,
  valeur,
  detail,
  testid,
}: {
  label: string;
  ton: Ton;
  valeur: string;
  detail?: ReactNode;
  testid: string;
}) {
  return (
    <div className={`status ${ton}`} data-testid={testid} data-ton={ton}>
      <span className="dot">
        <TonIcon ton={ton} />
      </span>
      <div style={{ minWidth: 0 }}>
        <div className="label">{label}</div>
        <div className="value">
          <span className="sr-only">{TON_SR[ton]} : </span>
          {valeur}
        </div>
        {detail ? <div className="detail">{detail}</div> : null}
      </div>
    </div>
  );
}

export function Card({ titre, sous, children, testid, id, actions }: { titre?: ReactNode; sous?: ReactNode; children: ReactNode; testid?: string; id?: string; actions?: ReactNode }) {
  return (
    <section className="card" data-testid={testid} id={id} aria-labelledby={id && titre ? `${id}-titre` : undefined}>
      {titre ? (
        <h2 id={id ? `${id}-titre` : undefined}>
          <span>{titre}</span>
          {actions}
        </h2>
      ) : null}
      {sous ? <p className="card-sub">{sous}</p> : null}
      {children}
    </section>
  );
}

export function Msg({ message }: { message: { ton: "ok" | "bad"; texte: string } | null }) {
  if (!message) return null;
  return (
    <div className={`msg ${message.ton}`} role={message.ton === "bad" ? "alert" : "status"} data-testid="message-action">
      {message.texte}
    </div>
  );
}

export function Chargement({ texte = "Chargement…" }: { texte?: string }) {
  return (
    <p className="loading" role="status">
      {texte}
    </p>
  );
}

export function Erreur({ texte }: { texte: string }) {
  return (
    <Banner ton="bad" titre="Impossible de charger ces informations" role="alert">
      <p>{texte}</p>
    </Banner>
  );
}

export function JsonDetails({ valeur, libelle = "Détails (JSON)" }: { valeur: unknown; libelle?: string }) {
  if (valeur === null || valeur === undefined) return null;
  if (typeof valeur === "object" && Object.keys(valeur as object).length === 0) return null;
  return (
    <details className="json">
      <summary>{libelle}</summary>
      <pre>{JSON.stringify(valeur, null, 2)}</pre>
    </details>
  );
}

export function BoutonCopier({ texte, libelle = "Copier", testid }: { texte: string; libelle?: string; testid?: string }) {
  const [etat, setEtat] = useState<"" | "ok" | "ko">("");
  return (
    <button
      type="button"
      className="btn small"
      data-testid={testid}
      onClick={async () => {
        try {
          await navigator.clipboard.writeText(texte);
          setEtat("ok");
        } catch {
          setEtat("ko");
        }
        window.setTimeout(() => setEtat(""), 2500);
      }}
    >
      <Icon name="copy" />
      {etat === "ok" ? "Copié" : etat === "ko" ? "Copie impossible : sélectionne le texte" : libelle}
    </button>
  );
}

export function Kv({ items }: { items: [ReactNode, ReactNode][] }) {
  return (
    <dl className="kv">
      {items.map(([k, v], i) => (
        <div key={i} style={{ display: "contents" }}>
          <dt>{k}</dt>
          <dd>{v}</dd>
        </div>
      ))}
    </dl>
  );
}

/** Classe CSS pour colorer un résultat positif / négatif (le signe est toujours écrit en plus). */
export function classeSigne(x: number | null | undefined): string {
  if (typeof x !== "number" || !Number.isFinite(x) || x === 0) return "";
  return x > 0 ? "pos" : "neg";
}
