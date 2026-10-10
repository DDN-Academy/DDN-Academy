import { Link, useSearchParams } from "react-router-dom";
import { useRessource, useTitre } from "../lib/hooks";
import type { JournalLigne, JournalType } from "../lib/types";
import { NOTIF_TYPES, gravite, notifStatut, verdict } from "../lib/status";
import { prix, texteBrut } from "../lib/format";
import { Badge, Chargement, Erreur, JsonDetails } from "../components/ui";

const ONGLETS: { cle: JournalType; libelle: string; aide: string }[] = [
  { cle: "decisions", libelle: "Décisions", aide: "Chaque analyse du moteur (toutes les 15 minutes) : résultat, raisons, contexte et contrôles du risque." },
  { cle: "incidents", libelle: "Incidents", aide: "Pannes, données douteuses, arrêts de sécurité, et leur résolution." },
  { cle: "notifications", libelle: "Alertes", aide: "Toutes les notifications Telegram : envoyées, en échec, périmées (plus exploitables) ou désactivées." },
  { cle: "webhooks", libelle: "Webhooks", aide: "Messages reçus de TradingView : acceptés ou refusés, avec la raison." },
  { cle: "controle", libelle: "Contrôle croisé", aide: "Comparaison des franchissements vus par TradingView avec les décisions du moteur (jamais décisionnel)." },
  { cle: "audit", libelle: "Audit", aide: "Toutes les actions : connexions, changements de réglages, modes, déclarations." },
];

const LIMITES = [25, 100, 500];

export function Journal() {
  useTitre("Journal");
  const [params, setParams] = useSearchParams();
  const onglet = (ONGLETS.find((o) => o.cle === params.get("onglet"))?.cle ?? "decisions") as JournalType;
  const limite = LIMITES.includes(Number(params.get("limite"))) ? Number(params.get("limite")) : 100;
  const r = useRessource<{ lignes: JournalLigne[] }>(`/api/journal?type=${onglet}&limit=${limite}`);
  const maj = (k: string, v: string) => {
    const p = new URLSearchParams(params);
    p.set(k, v);
    setParams(p, { replace: true });
  };
  const courant = ONGLETS.find((o) => o.cle === onglet)!;

  return (
    <>
      <div className="page-head">
        <h1>Journal</h1>
        <button type="button" className="btn small" onClick={() => void r.recharger()} data-testid="journal-actualiser">
          Actualiser
        </button>
      </div>
      <div className="chips" role="tablist" aria-label="Type de journal">
        {ONGLETS.map((o) => (
          <button
            key={o.cle}
            type="button"
            role="tab"
            className="chip"
            aria-selected={o.cle === onglet}
            aria-controls="journal-panneau"
            onClick={() => maj("onglet", o.cle)}
            data-testid={`onglet-${o.cle}`}
          >
            {o.libelle}
          </button>
        ))}
      </div>
      <div className="row" style={{ marginBottom: 10 }}>
        <label htmlFor="journal-limite" className="small">
          Lignes
        </label>
        <select id="journal-limite" style={{ width: "auto" }} value={limite} onChange={(e) => maj("limite", e.target.value)} data-testid="journal-limite">
          {LIMITES.map((l) => (
            <option key={l} value={l}>
              {l}
            </option>
          ))}
        </select>
      </div>

      <section className="card" id="journal-panneau" role="tabpanel" aria-label={courant.libelle} data-testid={`journal-${onglet}`}>
        <p className="card-sub" style={{ marginTop: 0 }}>
          {courant.aide}
        </p>
        {r.chargement && !r.data ? <Chargement /> : null}
        {r.erreur ? <Erreur texte={r.erreur.message} /> : null}
        {r.data ? (
          r.data.lignes.length === 0 ? (
            <p className="muted">Aucune ligne.</p>
          ) : (
            <ul className="list">
              {r.data.lignes.map((l, i) => (
                <li key={i} data-testid="ligne-journal">
                  <Ligne type={onglet} l={l} />
                </li>
              ))}
            </ul>
          )
        ) : null}
      </section>
    </>
  );
}

const s = (v: unknown) => (v === null || v === undefined ? "" : String(v));

function Ligne({ type, l }: { type: JournalType; l: JournalLigne }) {
  const heure = <div className="small muted">{s(l.heure)}</div>;
  switch (type) {
    case "decisions": {
      const raisons = Array.isArray(l.raisons) ? (l.raisons as unknown[]).map(String) : [];
      const res = s(l.resultat);
      return (
        <>
          {heure}
          <div className="row">
            <Badge ton={res === "signal" ? "warn" : res === "refuse" ? "info" : res === "suspendu" ? "bad" : "neutral"}>{libelleResultat(res)}</Badge>
            {l.signal ? <Link to={`/signal/${s(l.signal)}`}>Voir le signal</Link> : null}
          </div>
          <div>{s(l.resume)}</div>
          {raisons.length ? <div className="small">Raisons : {raisons.join(" ; ")}</div> : null}
          <JsonDetails valeur={{ contexte: l.contexte, controles: l.controles, version: l.version }} libelle="Contexte et contrôles (JSON)" />
        </>
      );
    }
    case "incidents": {
      const g = gravite(s(l.gravite));
      return (
        <>
          {heure}
          <div className="row">
            <Badge ton={g.ton}>{g.libelle}</Badge>
            <span className="small">composant : {s(l.composant)}</span>
            <Badge ton={l.resolu ? "neutral" : "bad"}>{l.resolu ? `résolu le ${s(l.resolu)}` : "ouvert"}</Badge>
          </div>
          <div>{s(l.message)}</div>
        </>
      );
    }
    case "notifications": {
      const st = notifStatut(s(l.statut));
      return (
        <>
          {heure}
          <div className="row">
            <strong>{NOTIF_TYPES[s(l.type)] ?? s(l.type)}</strong>
            <Badge ton={st.ton}>{st.libelle}</Badge>
            <span className="small muted">{s(l.essais)} essai(s)</span>
          </div>
          {l.erreur ? <div className="small">Erreur : {s(l.erreur)}</div> : null}
          <details className="json">
            <summary>Texte du message</summary>
            <pre>{texteBrut(s(l.texte))}</pre>
          </details>
        </>
      );
    }
    case "webhooks":
      return (
        <>
          {heure}
          <div className="row">
            <Badge ton={l.accepte ? "ok" : "bad"}>{l.accepte ? "Accepté" : "Refusé"}</Badge>
            <span>type : {s(l.type)}</span>
            <span className="small muted">IP {s(l.ip)}</span>
          </div>
          {l.raison ? <div className="small">{s(l.raison)}</div> : null}
        </>
      );
    case "controle": {
      const v = verdict(s(l.verdict));
      return (
        <>
          {heure}
          <div className="row">
            <Badge ton={v.ton}>{v.libelle}</Badge>
            <span>
              {s(l.sens)} {s(l.contrat)} à {typeof l.prix === "number" ? prix(l.prix) : s(l.prix)}
            </span>
            {l.signal ? <Link to={`/signal/${s(l.signal)}`}>Signal lié</Link> : null}
          </div>
        </>
      );
    }
    default:
      return (
        <>
          {heure}
          <div className="row">
            <strong>{s(l.action).replace(/_/g, " ")}</strong>
            <span className="small muted">par {s(l.acteur)}</span>
          </div>
          <JsonDetails valeur={l.detail} />
        </>
      );
  }
}

function libelleResultat(r: string): string {
  if (r === "aucun_setup") return "Aucun setup";
  if (r === "signal") return "Signal émis";
  if (r === "refuse") return "Setup refusé par le risque";
  if (r === "suspendu") return "Analyse suspendue";
  return r.replace(/_/g, " ");
}
