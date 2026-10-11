import { Link } from "react-router-dom";
import type { Niveaux, Signal } from "../lib/types";
import { etatEntree, etiquettesSignal, modeLibelle } from "../lib/status";
import { enR, entier, nombre, prix, usd } from "../lib/format";
import { Badge, classeSigne } from "./ui";

/** Texte honnête pour la sortie : la stratégie S1 n'a pas d'objectif fixe (stop suiveur + sortie temporelle). */
export function texteSortie(sig: Signal): { valeur: string; detail: string } {
  if (sig.objectif !== null && sig.objectif !== undefined) {
    return { valeur: prix(sig.objectif), detail: "take-profit fixe" };
  }
  const suiveur = sig.stop_suiveur_atr ? `stop suiveur à ${nombre(sig.stop_suiveur_atr, 1)} ATR` : "stop suiveur";
  return { valeur: "Pas d'objectif fixe", detail: `${suiveur}, sortie au plus tard ${sig.sortie_max}` };
}

export function typeEntree(t: string): string {
  if (t === "market") return "Immédiate (au marché)";
  if (t === "limit") return "Conditionnelle (ordre limite)";
  if (t === "stop") return "Conditionnelle (ordre stop)";
  return t;
}

const NIVEAUX_LIBELLES: [keyof Omit<Niveaux, "distances_atr">, string][] = [
  ["plus_haut_veille", "Plus haut de la veille"],
  ["plus_bas_veille", "Plus bas de la veille"],
  ["plus_haut_seance", "Plus haut de la séance"],
  ["plus_bas_seance", "Plus bas de la séance"],
  ["swing_haut_15m", "Dernier sommet 15 min"],
  ["swing_bas_15m", "Dernier creux 15 min"],
];

/** Niveaux de contexte de la décision (contrat C4) : barres terminées uniquement, distance en ATR depuis le prix de décision. */
export function NiveauxSignal({ niveaux }: { niveaux: Niveaux | null | undefined }) {
  if (!niveaux) return null;
  const lignes = NIVEAUX_LIBELLES.filter(([k]) => niveaux[k] !== null && niveaux[k] !== undefined);
  if (lignes.length === 0) return null;
  return (
    <div data-testid="signal-niveaux" style={{ marginTop: 10 }}>
      <div className="small" style={{ fontWeight: 600 }}>Niveaux de prix au moment de la décision</div>
      <ul className="small" style={{ margin: "4px 0 0", paddingLeft: 18 }}>
        {lignes.map(([k, lib]) => {
          const dist = niveaux.distances_atr?.[k];
          return (
            <li key={k}>
              {lib} : {prix(niveaux[k] as number)}
              {dist !== null && dist !== undefined ? ` (prix ${dist >= 0 ? "+" : ""}${nombre(dist, 2)} ATR)` : ""}
            </li>
          );
        })}
      </ul>
    </div>
  );
}

export function SignalCard({ sig, titre, lienDetail = true }: { sig: Signal; titre?: string; lienDetail?: boolean }) {
  const long = sig.sens === "LONG";
  const sortie = texteSortie(sig);
  const sim = sig.simulation;
  return (
    <article className={`card signal-card ${long ? "long" : "short"}`} data-testid="signal-card" aria-label={`Signal ${sig.sens} ${sig.contrat}`}>
      {titre ? <p className="card-sub" style={{ marginTop: 0 }}>{titre}</p> : null}
      <div className="signal-head">
        <span className={`side ${long ? "long" : "short"}`} data-testid="signal-sens">
          {long ? "▲ LONG" : "▼ SHORT"}
        </span>
        <span className="sig-title">{sig.contrat}</span>
        <Badge ton={sig.mode === "reel" ? "bad" : "warn"} testid="signal-mode">
          {modeLibelle(sig.mode)}
        </Badge>
      </div>
      <div className="row" style={{ marginBottom: 10 }} data-testid="signal-statut">
        {etiquettesSignal(sig).map((e) => (
          <Badge key={e.cle} ton={e.ton} wrap>
            {e.libelle}
          </Badge>
        ))}
      </div>
      {(() => {
        const e = etatEntree(sig);
        if (!e) return null;
        return (
          <p className={`small entree-${e.ouverte ? "ouverte" : "fermee"}`} data-testid="signal-entree" role={e.ouverte ? undefined : "alert"}>
            <strong>{e.ouverte ? "Entrée exploitable maintenant" : "Entrée fermée — ne plus entrer"}</strong> : {e.raison}
            {e.ouverte ? "" : ". Si tu es déjà en position, garde ton stop ; la position simulée reste suivie."}
          </p>
        );
      })()}
      <div className="levels">
        <div className="level">
          <div className="k">Entrée</div>
          <div className="v">{prix(sig.entree)}</div>
          <div className="s">
            plage {prix(sig.plage[0])} – {prix(sig.plage[1])}
          </div>
        </div>
        <div className="level">
          <div className="k">Stop-loss</div>
          <div className="v">{prix(sig.stop)}</div>
          <div className="s">{sim.stop_actuel !== null && sim.stop_actuel !== sig.stop ? `stop actuel ${prix(sim.stop_actuel)}` : "stop initial"}</div>
        </div>
        <div className="level">
          <div className="k">Sortie</div>
          <div className="v" style={{ fontSize: sig.objectif ? undefined : "0.95rem" }}>
            {sortie.valeur}
          </div>
          <div className="s">{sortie.detail}</div>
        </div>
        <div className="level">
          <div className="k">Taille</div>
          <div className="v">{entier(sig.contrats)} MGC</div>
          <div className="s">risque {usd(sig.risque_usd)}</div>
        </div>
      </div>
      <dl className="kv">
        <dt>Type d'entrée</dt>
        <dd>{typeEntree(sig.type_entree)}</dd>
        <dt>Validité</dt>
        <dd>jusqu'à {sig.validite_ny}</dd>
        <dt>Rendement / risque</dt>
        <dd>{sig.rr !== null && sig.rr !== undefined ? nombre(sig.rr, 2) : "non défini (pas d'objectif fixe)"}</dd>
        <dt>Émis le</dt>
        <dd>{sig.cree_paris}</dd>
        {sim.r !== null && sim.r !== undefined ? (
          <>
            <dt>Résultat simulé</dt>
            <dd className={classeSigne(sim.r)}>
              {enR(sim.r)} ({usd(sim.pnl_usd, 0, true)})
            </dd>
          </>
        ) : null}
      </dl>
      <NiveauxSignal niveaux={sig.niveaux} />
      {lienDetail ? (
      <p style={{ marginTop: 12, marginBottom: 0 }}>
        <Link to={`/signal/${sig.id}`} className="btn small" data-testid="lien-detail-signal">
          Voir le détail complet
        </Link>
      </p>
      ) : null}
    </article>
  );
}
