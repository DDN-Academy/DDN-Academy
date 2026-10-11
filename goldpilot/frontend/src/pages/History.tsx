import { Link, useSearchParams } from "react-router-dom";
import { useRessource, useTitre } from "../lib/hooks";
import type { Signal } from "../lib/types";
import { FILTRES_STATUT, etiquettesSignal, modeLibelle } from "../lib/status";
import { enR, prix, usd } from "../lib/format";
import { Badge, Card, Chargement, Erreur, classeSigne } from "../components/ui";

const LIMITES = [25, 50, 100, 200, 500];

export function History() {
  useTitre("Historique");
  const [params, setParams] = useSearchParams();
  const statut = params.get("statut") ?? "";
  const limite = LIMITES.includes(Number(params.get("limite"))) ? Number(params.get("limite")) : 50;
  const url = `/api/signals?limit=${limite}${statut ? `&statut=${encodeURIComponent(statut)}` : ""}`;
  const r = useRessource<{ signaux: Signal[] }>(url);
  const maj = (k: string, v: string) => {
    const p = new URLSearchParams(params);
    if (v) p.set(k, v);
    else p.delete(k);
    setParams(p, { replace: true });
  };
  const sigs = r.data?.signaux ?? [];
  const totalR = sigs.reduce((t, s) => t + (s.simulation.r ?? 0), 0);
  const totalUsd = sigs.reduce((t, s) => t + (s.simulation.pnl_usd ?? 0), 0);
  const avecResultat = sigs.filter((s) => s.simulation.r !== null).length;

  return (
    <>
      <div className="page-head">
        <h1>Historique des signaux</h1>
      </div>
      <div className="chips" role="group" aria-label="Filtrer par statut" data-testid="filtres-statut">
        {FILTRES_STATUT.map((f) => (
          <button
            key={f.valeur || "tous"}
            type="button"
            className="chip"
            aria-pressed={statut === f.valeur}
            onClick={() => maj("statut", f.valeur)}
            data-testid={`filtre-${f.valeur || "tous"}`}
          >
            {f.libelle}
          </button>
        ))}
      </div>
      <div className="row" style={{ marginBottom: 10 }}>
        <label htmlFor="limite" className="small">
          Afficher
        </label>
        <select id="limite" value={limite} onChange={(e) => maj("limite", e.target.value)} style={{ width: "auto" }} data-testid="historique-limite">
          {LIMITES.map((l) => (
            <option key={l} value={l}>
              {l} derniers
            </option>
          ))}
        </select>
      </div>

      {r.chargement && !r.data ? <Chargement /> : null}
      {r.erreur ? <Erreur texte={r.erreur.message} /> : null}

      {r.data ? (
        <Card testid="liste-signaux">
          {sigs.length === 0 ? (
            <p className="muted">Aucun signal{statut ? " avec ce statut" : ""}. L'absence de signal est un résultat normal : le système n'émet que si toutes les conditions sont réunies.</p>
          ) : (
            <>
              <p className="small muted">
                {sigs.length} signal(aux) affiché(s) · résultat simulé cumulé sur les {avecResultat} clôturé(s) :{" "}
                <strong className={classeSigne(totalR)}>
                  {enR(totalR)} ({usd(totalUsd, 0, true)})
                </strong>
              </p>
              <ul className="list">
                {sigs.map((s) => (
                  <li key={s.id}>
                    <Link to={`/signal/${s.id}`} className="sig-row" data-testid="ligne-signal">
                      <span className="sig-title">
                        <span className={s.sens === "LONG" ? "pos" : "neg"}>{s.sens === "LONG" ? "▲" : "▼"}</span> {s.sens} {s.contrat}
                      </span>
                      <span className={`sig-res ${classeSigne(s.simulation.r)}`}>
                        {s.simulation.r !== null ? enR(s.simulation.r) : null}
                        <span className="sig-meta" style={{ display: "block", fontWeight: 400 }}>
                          {s.simulation.pnl_usd !== null ? usd(s.simulation.pnl_usd, 0, true) : s.statut === "CLOTURE" ? "résultat inconnu (données manquantes)" : "pas de résultat"}
                        </span>
                      </span>
                      <span className="sig-meta" style={{ gridColumn: "1 / -1" }}>
                        {s.cree_paris} · entrée {prix(s.entree)} · stop {prix(s.stop)} · {s.contrats} contrat(s)
                      </span>
                      <span className="sig-badges">
                        <Badge ton={s.mode === "reel" ? "bad" : "warn"}>{modeLibelle(s.mode)}</Badge>
                        {etiquettesSignal(s).map((e) => (
                          <Badge key={e.cle} ton={e.ton} wrap>
                            {e.libelle}
                          </Badge>
                        ))}
                      </span>
                    </Link>
                  </li>
                ))}
              </ul>
            </>
          )}
        </Card>
      ) : null}
    </>
  );
}
