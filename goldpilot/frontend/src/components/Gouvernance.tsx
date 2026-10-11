import { useState, type FormEvent } from "react";
import { api } from "../lib/api";
import { useAction, useRessource } from "../lib/hooks";
import { dateHeure, enR, entier, nombre, pct } from "../lib/format";
import type { Gouvernance, RevuePeriodique } from "../lib/types";
import { Badge, Banner, Card, Erreur, JsonDetails, Kv, Msg } from "./ui";

const PHRASE = "J'APPROUVE CETTE VERSION";

/**
 * Gouvernance de la stratégie (cahier §17) : version en service, version approuvée, comparaison avant remplacement
 * et revue périodique hebdomadaire. Avec `approbation`, affiche le formulaire d'approbation (Paramètres).
 */
export function GouvernanceCarte({ approbation = false }: { approbation?: boolean }) {
  const r = useRessource<Gouvernance>("/api/strategy/governance");
  const a = useAction();
  const [phrase, setPhrase] = useState("");
  const g = r.data;

  async function approuver(e: FormEvent) {
    e.preventDefault();
    if (!g?.version_courante) return;
    if (phrase.trim() !== PHRASE) {
      a.setMessage({ ton: "bad", texte: `Recopie exactement la phrase « ${PHRASE} ».` });
      return;
    }
    const ok = await a.lancer(
      () => api.post("/api/strategy/approve", { version: g.version_courante, confirmation: phrase.trim() }),
      "Version approuvée (enregistrée dans l'audit). Le moteur pourra de nouveau émettre des signaux en simulation.",
    );
    if (ok) {
      setPhrase("");
      await r.recharger();
    }
  }

  return (
    <Card
      titre="Gouvernance de la stratégie"
      id="gouvernance"
      testid="gouvernance-strategie"
      sous="Aucune nouvelle version ne remplace l'ancienne sans comparaison et sans ton approbation explicite. La stratégie n'est jamais modifiée automatiquement."
    >
      {r.erreur && !g ? <Erreur texte={r.erreur.message} /> : null}
      {g ? (
        <>
          {g.en_attente ? (
            <Banner ton="bad" titre="Nouvelle version en attente d'approbation" testid="version-en-attente">
              <p>
                La version en service ({g.version_courante}) diffère de la version approuvée ({g.version_approuvee?.version ?? "aucune"}). Le
                moteur est à l'arrêt de sécurité : aucun signal tant que tu ne l'as pas comparée puis approuvée.
              </p>
            </Banner>
          ) : null}
          <Kv
            items={[
              ["Version en service", <span data-testid="version-courante">{g.version_courante ?? "aucune stratégie configurée"}</span>],
              [
                "Version approuvée",
                g.version_approuvee ? (
                  <span data-testid="version-approuvee">
                    {g.version_approuvee.version}
                    <span className="sub">
                      {g.version_approuvee.par === "utilisateur" ? "approuvée par toi" : "enregistrée à la première mise en service"} le{" "}
                      {dateHeure(g.version_approuvee.approuve_le)}
                    </span>
                  </span>
                ) : (
                  <span data-testid="version-approuvee">pas encore enregistrée (le moteur l'enregistre à son démarrage)</span>
                ),
              ],
              [
                "Comparaison avec la version précédente",
                g.comparaison ? <JsonDetails valeur={g.comparaison} libelle="Voir la comparaison (recherche)" /> : "aucune comparaison fournie par la recherche",
              ],
            ]}
          />
          <Revue revue={g.revue_periodique} />
          {approbation && g.en_attente && g.version_courante ? (
            <form onSubmit={approuver} data-testid="form-approbation-version" noValidate style={{ marginTop: 12 }}>
              <p className="small">
                Avant d'approuver : lis la comparaison ci-dessus et les résultats de recherche (page Statistiques). Approuver ne valide pas la
                stratégie : le mode réel reste verrouillé tant qu'elle n'a pas satisfait les critères.
              </p>
              <div className="field">
                <label htmlFor="phrase-version">
                  Recopie « {PHRASE} » pour approuver la version {g.version_courante}
                </label>
                <input id="phrase-version" type="text" autoComplete="off" value={phrase} onChange={(e) => setPhrase(e.target.value)} data-testid="champ-phrase-version" />
              </div>
              <button type="submit" className="btn danger" disabled={a.enCours} data-testid="bouton-approuver-version">
                Approuver cette version
              </button>
            </form>
          ) : null}
          <Msg message={a.message} />
        </>
      ) : null}
    </Card>
  );
}

function Revue({ revue }: { revue: RevuePeriodique | null }) {
  return (
    <div data-testid="revue-periodique" style={{ marginTop: 12 }}>
      <h3>Revue périodique (chaque samedi)</h3>
      {!revue ? (
        <p className="muted small">Aucune revue pour l'instant : la première est produite par le moteur le samedi suivant sa mise en service.</p>
      ) : (
        <>
          <p className="small">
            <Badge ton="info">Revue du {revue.date}</Badge> version {revue.version} — trades simulés uniquement.
          </p>
          <Kv
            items={[
              ["Trades simulés clôturés", entier(revue.n)],
              ["Espérance par trade", revue.esperance_R !== null ? enR(revue.esperance_R, 3) : "—"],
              ["Borne basse à 95 %", revue.borne_basse_95_R !== null ? enR(revue.borne_basse_95_R, 3) : "—"],
              ["Drawdown maximal", revue.drawdown_max_R !== null ? enR(revue.drawdown_max_R) : "—"],
              ["Plus longue série de pertes", entier(revue.serie_pertes_max)],
              ["Taux de gain", revue.taux_de_gain !== null ? pct(revue.taux_de_gain) : "—"],
              [
                "Référence de la recherche",
                revue.reference
                  ? `walk-forward ${revue.reference.esperance_R_walk_forward !== null ? enR(revue.reference.esperance_R_walk_forward, 3) : "indisponible"} · 2022-2025 ${
                      revue.reference.esperance_R_2022_2025 !== null ? enR(revue.reference.esperance_R_2022_2025, 3) : "indisponible"
                    } (source : ${revue.reference.source})`
                  : "indisponible",
              ],
              [
                "Seuils de suspension",
                revue.seuils ? `drawdown ${nombre(revue.seuils.drawdown_R, 1)} R · ${revue.seuils.serie_pertes} pertes d'affilée` : "non définis",
              ],
            ]}
          />
          <p className="small" data-testid="revue-conclusion">
            {revue.conclusion}
          </p>
        </>
      )}
    </div>
  );
}
