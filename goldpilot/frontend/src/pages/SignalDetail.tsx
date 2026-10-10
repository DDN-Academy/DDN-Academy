import { useState, type FormEvent } from "react";
import { Link, useParams } from "react-router-dom";
import { api } from "../lib/api";
import { useAction, useRessource, useTitre } from "../lib/hooks";
import type { SignalDetail as Detail, Signal } from "../lib/types";
import { EVENEMENTS_SIGNAL, NOTIF_TYPES, notifStatut, peutAnnuler, statutSignal, verdict } from "../lib/status";
import { dateHeure, enR, nombre, prix, usd } from "../lib/format";
import { Badge, Card, Chargement, Erreur, JsonDetails, Kv, Msg, classeSigne } from "../components/ui";
import { SignalCard, texteSortie, typeEntree } from "../components/SignalCard";

export function SignalDetail() {
  const { id } = useParams();
  useTitre("Détail du signal");
  const r = useRessource<Detail>(id ? `/api/signals/${encodeURIComponent(id)}` : null);
  if (r.chargement && !r.data) return <Chargement />;
  if (r.erreur && !r.data) return <Erreur texte={r.erreur.message} />;
  if (!r.data) return null;
  const { signal: s, evenements, controles_risque, contexte, alertes } = r.data;
  const st = statutSignal(s.statut);
  const sortie = texteSortie(s);

  return (
    <>
      <div className="page-head">
        <h1>
          Signal {s.sens} {s.contrat}
        </h1>
        <Link to="/historique" className="meta">
          ← Historique
        </Link>
      </div>

      <SignalCard sig={s} lienDetail={false} />

      <Card titre="Toutes les informations de l'alerte" testid="champs-alerte" id="champs">
        <p className="card-sub">{st.explication}</p>
        <Kv
          items={[
            ["Instrument et contrat", s.contrat],
            ["Date et heure", s.cree_paris],
            ["Sens", s.sens],
            ["Entrée", `${prix(s.entree)} (plage ${prix(s.plage[0])} – ${prix(s.plage[1])})`],
            ["Type d'entrée", typeEntree(s.type_entree)],
            ["Stop-loss", prix(s.stop)],
            ["Take-profit", `${sortie.valeur} — ${sortie.detail}`],
            ["Rendement / risque", s.rr !== null ? nombre(s.rr, 2) : "non défini (pas d'objectif fixe)"],
            ["Risque estimé", usd(s.risque_usd)],
            ["Taille", `${s.contrats} contrat(s) Micro Gold (risque par contrat = distance au stop + glissement prévu, × 10 onces, + commission)`],
            ["ATR (15 min)", s.atr !== null ? nombre(s.atr, 2) : "—"],
            ["Validité", `jusqu'à ${s.validite_ny}`],
            ["Sortie au plus tard", s.sortie_max],
            ["Condition d'annulation", s.invalidation],
            ["Justification", s.justification],
            ["Calendrier économique", s.calendrier],
            ["Source de prix", `${s.source_prix} — mise à jour ${dateHeure(s.prix_maj)} (Paris)`],
            ["Mode", s.mode === "reel" ? "réel" : "simulation"],
            ["Stratégie", `${s.version}${s.valide ? "" : " — NON VALIDÉE"}`],
            ["Statut", `${st.libelle}${s.raison_statut ? ` — ${s.raison_statut}` : ""}`],
            ["Référence", <code>{s.id}</code>],
          ]}
        />
      </Card>

      <Card titre="Position simulée" testid="position-simulee" id="simulation">
        {s.simulation.entree === null ? (
          <p className="muted">Aucune entrée simulée (le prix n'a pas déclenché l'entrée, ou le signal a été annulé / a expiré).</p>
        ) : (
          <Kv
            items={[
              ["Entrée simulée", `${prix(s.simulation.entree)} — ${dateHeure(s.simulation.entree_ts)}`],
              ["Stop actuel", prix(s.simulation.stop_actuel)],
              ["Sortie simulée", s.simulation.sortie !== null ? `${prix(s.simulation.sortie)} — ${dateHeure(s.simulation.sortie_ts)}` : "position simulée encore ouverte"],
              ["Raison de sortie", s.simulation.raison ?? "—"],
              [
                "Résultat simulé",
                <span className={classeSigne(s.simulation.r)}>
                  {enR(s.simulation.r)} ({usd(s.simulation.pnl_usd, 0, true)})
                </span>,
              ],
            ]}
          />
        )}
        <p className="small muted" style={{ marginTop: 8, marginBottom: 0 }}>
          Simulation : exécution supposée aux prix du flux, avec glissement et commission estimés. Ce n'est pas un ordre réel.
        </p>
      </Card>

      <Card titre="Chronologie" testid="chronologie" id="chronologie">
        {evenements.length === 0 ? (
          <p className="muted">Aucun événement.</p>
        ) : (
          <ol className="timeline">
            {evenements.map((e, i) => (
              <li key={i}>
                <div className="t">{e.heure}</div>
                <div>
                  <strong>{EVENEMENTS_SIGNAL[e.type] ?? e.type}</strong> {resumeEvenement(e.type, e.detail)}
                </div>
                <JsonDetails valeur={e.detail} />
              </li>
            ))}
          </ol>
        )}
      </Card>

      <Card titre="Contrôles du risque" testid="controles-risque" id="controles" sous="Chaque contrôle obligatoire doit être satisfait pour qu'un signal soit émis.">
        {controles_risque.length === 0 ? (
          <p className="muted">Aucun contrôle enregistré pour ce signal.</p>
        ) : (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Contrôle</th>
                  <th>Résultat</th>
                  <th>Détail</th>
                </tr>
              </thead>
              <tbody>
                {controles_risque.map((c, i) => (
                  <tr key={i} data-testid="ligne-controle">
                    <td>
                      {c.controle}
                      {c.bloquant === false ? <div className="small muted">non bloquant (information) : {c.ok ? "OK" : "KO"}</div> : null}
                    </td>
                    <td>
                      <Badge ton={c.bloquant === false ? "info" : c.ok ? "ok" : "bad"}>
                        {c.bloquant === false ? "Info" : c.ok ? "OK" : "KO"}
                      </Badge>
                    </td>
                    <td>{c.detail}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>

      <Card titre="Alertes envoyées" testid="alertes-envoyees" id="alertes">
        {alertes.length === 0 ? (
          <p className="muted">Aucune alerte liée à ce signal.</p>
        ) : (
          <ul className="list">
            {alertes.map((a, i) => (
              <li key={i}>
                <div className="row">
                  <strong>{NOTIF_TYPES[a.type] ?? a.type}</strong>
                  <Badge ton={notifStatut(a.statut).ton}>{notifStatut(a.statut).libelle}</Badge>
                </div>
                <div className="small muted">
                  créée {a.creee}
                  {a.envoyee ? ` · envoyée ${a.envoyee}` : " · non envoyée"}
                </div>
                {a.erreur ? <div className="small">Erreur : {a.erreur}</div> : null}
              </li>
            ))}
          </ul>
        )}
      </Card>

      <Card titre="Contexte de la décision" testid="contexte-decision" id="contexte">
        <Contexte contexte={contexte} />
      </Card>

      <DeclarationExecution key={s.id} sig={s} onSaved={r.recharger} />
      <Annulation key={`a-${s.id}`} sig={s} onDone={r.recharger} />
    </>
  );
}

function resumeEvenement(type: string, d: Record<string, unknown> | null): string {
  if (!d) return "";
  const n = (k: string) => (typeof d[k] === "number" ? (d[k] as number) : null);
  switch (type) {
    case "cree":
      return `— ${d.contrats ?? "?"} contrat(s), risque ${usd(n("risque"))}`;
    case "plage_depassee":
    case "entree_simulee":
      return `— prix ${prix(n("prix"))}`;
    case "sortie_simulee":
      return `— prix ${prix(n("prix"))}, ${String(d.raison ?? "")}, ${enR(n("r"))}`;
    case "stop_deplace":
      return `— de ${prix(n("avant"))} à ${prix(n("apres"))}`;
    case "annule":
      return d.raison ? `— ${String(d.raison)}` : d.par === "utilisateur" ? "— par toi" : "";
    case "controle_croise":
      return d.verdict ? `— ${verdict(String(d.verdict)).libelle}` : "";
    default:
      return "";
  }
}

const CONTEXTE_LIBELLES: Record<string, string> = {
  regime: "Régime",
  z: "Écart à la moyenne de séance (ATR)",
  session_mean: "Moyenne de séance",
  atr: "ATR (15 min)",
  franchissement: "Franchissement du seuil",
  rang_volatilite_veille: "Rang de volatilité de la veille",
  prix: "Prix à la décision",
  contrat: "Contrat",
};

function Contexte({ contexte }: { contexte: Record<string, unknown> }) {
  const cles = Object.keys(contexte ?? {});
  if (cles.length === 0) return <p className="muted">Contexte non enregistré.</p>;
  return (
    <>
      <Kv
        items={cles.map((k) => {
          const v = contexte[k];
          let t: string;
          if (k === "franchissement" && typeof v === "number") t = v > 0 ? "à la hausse" : v < 0 ? "à la baisse" : "aucun";
          else if (k === "rang_volatilite_veille" && typeof v === "number") t = `${nombre(v * 100, 0)} %`;
          else if (typeof v === "number") t = nombre(v, 2);
          else t = typeof v === "string" ? v : JSON.stringify(v);
          return [CONTEXTE_LIBELLES[k] ?? k, t];
        })}
      />
      <JsonDetails valeur={contexte} />
    </>
  );
}

function DeclarationExecution({ sig, onSaved }: { sig: Signal; onSaved: () => Promise<void> }) {
  const ex = sig.execution_declaree;
  const [executee, setExecutee] = useState<"oui" | "non">(ex ? (ex.executee ? "oui" : "non") : "oui");
  const [entree, setEntree] = useState(ex?.entree != null ? String(ex.entree) : "");
  const [sortie, setSortie] = useState(ex?.sortie != null ? String(ex.sortie) : "");
  const [contrats, setContrats] = useState(ex?.contrats != null ? String(ex.contrats) : "");
  const [note, setNote] = useState(ex?.note ?? "");
  const a = useAction();

  const num = (s: string) => (s.trim() === "" ? null : Number(s.replace(",", ".")));

  async function envoyer(e: FormEvent) {
    e.preventDefault();
    const corps = {
      executee: executee === "oui",
      entree: executee === "oui" ? num(entree) : null,
      sortie: executee === "oui" ? num(sortie) : null,
      contrats: executee === "oui" ? num(contrats) : null,
      note,
    };
    for (const v of [corps.entree, corps.sortie, corps.contrats]) {
      if (v !== null && !Number.isFinite(v)) {
        a.setMessage({ ton: "bad", texte: "Un des nombres saisis est invalide." });
        return;
      }
    }
    const ok = await a.lancer(() => api.post(`/api/signals/${sig.id}/execution`, corps), "Déclaration enregistrée (déclarée par toi, non confirmée par le courtier).");
    if (ok) await onSaved();
  }

  return (
    <Card titre="Déclarer mon exécution" testid="carte-declaration" id="declaration">
      <p className="small">
        <Badge ton="neutral" wrap>
          Déclaré par toi — non confirmé par le courtier
        </Badge>
      </p>
      <p className="small muted">
        GoldPilot n'est pas relié à Tradovate : il ne peut pas savoir si tu as passé l'ordre ni à quel prix. Ce que tu saisis ici sert
        uniquement à ton suivi.
      </p>
      {ex ? (
        <p className="small" data-testid="declaration-existante">
          Déjà déclaré : {ex.executee ? `exécuté — entrée ${prix(ex.entree)}, sortie ${prix(ex.sortie)}, ${ex.contrats ?? "?"} contrat(s)` : "non exécuté"}
          {ex.pnl_usd !== null ? `, résultat ${usd(ex.pnl_usd, 0, true)} (calculé, hors commissions)` : ""}.
        </p>
      ) : null}
      <form onSubmit={envoyer} data-testid="form-declaration" noValidate>
        <fieldset className="field" style={{ border: 0, padding: 0, margin: "0 0 12px" }}>
          <legend className="label" style={{ fontWeight: 600, marginBottom: 4 }}>
            As-tu exécuté ce signal sur ton compte ?
          </legend>
          <div className="radio-row">
            <label>
              <input type="radio" name="executee" value="oui" checked={executee === "oui"} onChange={() => setExecutee("oui")} data-testid="champ-executee-oui" />
              Oui
            </label>
            <label>
              <input type="radio" name="executee" value="non" checked={executee === "non"} onChange={() => setExecutee("non")} data-testid="champ-executee-non" />
              Non
            </label>
          </div>
        </fieldset>
        {executee === "oui" ? (
          <div className="form-grid">
            <div className="field">
              <label htmlFor="ex-entree">Prix d'entrée réel</label>
              <input id="ex-entree" type="number" inputMode="decimal" step="0.1" min="0" value={entree} onChange={(e) => setEntree(e.target.value)} data-testid="champ-prix-entree" />
            </div>
            <div className="field">
              <label htmlFor="ex-sortie">Prix de sortie réel</label>
              <input id="ex-sortie" type="number" inputMode="decimal" step="0.1" min="0" value={sortie} onChange={(e) => setSortie(e.target.value)} data-testid="champ-prix-sortie" />
              <span className="hint">Laisse vide si la position est encore ouverte.</span>
            </div>
            <div className="field">
              <label htmlFor="ex-contrats">Nombre de contrats MGC</label>
              <input id="ex-contrats" type="number" inputMode="numeric" step="1" min="1" max="30" value={contrats} onChange={(e) => setContrats(e.target.value)} data-testid="champ-contrats" />
            </div>
          </div>
        ) : null}
        <div className="field">
          <label htmlFor="ex-note">Note (facultatif)</label>
          <textarea id="ex-note" maxLength={500} value={note} onChange={(e) => setNote(e.target.value)} data-testid="champ-note" />
        </div>
        <button type="submit" className="btn primary" disabled={a.enCours} data-testid="bouton-declarer">
          Enregistrer ma déclaration
        </button>
        <Msg message={a.message} />
      </form>
    </Card>
  );
}

function Annulation({ sig, onDone }: { sig: Signal; onDone: () => Promise<void> }) {
  const a = useAction();
  if (!peutAnnuler(sig)) return null;
  return (
    <Card titre="Annuler ce signal" testid="carte-annulation" id="annulation">
      <p className="small muted">Le signal passera au statut « Annulé » et ne sera plus suivi. Action enregistrée dans l'audit.</p>
      <button
        type="button"
        className="btn danger"
        disabled={a.enCours}
        data-testid="bouton-annuler-signal"
        onClick={async () => {
          if (!window.confirm("Annuler ce signal ?")) return;
          const ok = await a.lancer(() => api.post(`/api/signals/${sig.id}/cancel`), "Signal annulé.");
          if (ok) await onDone();
        }}
      >
        Annuler ce signal
      </button>
      <Msg message={a.message} />
    </Card>
  );
}
