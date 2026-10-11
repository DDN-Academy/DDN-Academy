import { Link } from "react-router-dom";
import { api } from "../lib/api";
import { useDashboard } from "../lib/dashboard";
import { useAction, useTitre } from "../lib/hooks";
import { etatEntree, indicateursSysteme, gravite, statutSignal } from "../lib/status";
import { dateHeure, duree, ilYa, nombre, prix, usd, dateCourte } from "../lib/format";
import { Badge, Banner, Card, Chargement, Icon, Kv, Msg, StatusTile } from "../components/ui";
import { SignalCard } from "../components/SignalCard";
import type { Dashboard } from "../lib/types";

export function Home() {
  useTitre("Accueil");
  const d = useDashboard();
  const dash = d.data;
  const ind = indicateursSysteme(dash, d.joignable);
  const fiable = !!dash && d.joignable;
  // Les avertissements du contexte macro (FRED, information seulement) restent au journal, pas sur l'accueil.
  const incidents = dash ? dash.incidents.filter((i) => i.composant !== "contexte") : [];

  return (
    <>
      <div className="page-head">
        <h1>Accueil</h1>
        <span className="meta" data-testid="maj-dashboard" aria-live="off">
          {d.recuA ? `mis à jour ${ilYa(d.ageS)}` : d.chargement ? "chargement…" : "jamais mis à jour"}
          {" · actualisation toutes les 10 s"}
        </span>
      </div>

      {d.chargement && !dash ? <Chargement /> : null}

      <Banner ton={ind.global.ton} titre={ind.global.titre} testid="etat-global" role="status">
        <p>{ind.global.texte}</p>
      </Banner>

      {fiable && incidents.length > 0 ? (
        <section className="card" data-testid="incidents" aria-labelledby="incidents-titre" role="alert">
          <h2 id="incidents-titre">Incidents ouverts ({incidents.length})</h2>
          <ul className="list">
            {incidents.map((i, k) => (
              <li key={k}>
                <div className="row">
                  <Badge ton={gravite(i.gravite).ton}>{gravite(i.gravite).libelle}</Badge>
                  <span className="muted small">depuis {i.depuis}</span>
                </div>
                <div>{i.message}</div>
              </li>
            ))}
          </ul>
          <Link to="/journal?onglet=incidents">Voir tout le journal des incidents</Link>
        </section>
      ) : null}

      {fiable && dash.trading.signal_en_cours ? (
        etatEntree(dash.trading.signal_en_cours)?.ouverte === false ? (
          <Banner ton="bad" titre="Entrée fermée — ne plus entrer" testid="alerte-signal-en-cours">
            <p>
              {etatEntree(dash.trading.signal_en_cours)?.raison}. La position simulée reste suivie jusqu'à sa sortie.{" "}
              <a href="#signal-en-cours">Voir le signal ci-dessous</a>.
            </p>
          </Banner>
        ) : (
          <Banner ton="warn" titre="Un signal est en cours — entrée exploitable maintenant" testid="alerte-signal-en-cours">
            <p>
              <a href="#signal-en-cours">Voir le signal ci-dessous</a> — il reste soumis au bandeau SIMULATION.
            </p>
          </Banner>
        )
      ) : null}

      <Card titre="État du système" testid="carte-systeme" id="systeme">
        <div className="status-list">
          <StatusTile label="Connexion" testid="status-connexion" ton={ind.connexion.ton} valeur={ind.connexion.titre} detail={ind.connexion.texte} />
          <StatusTile
            label="Données de marché"
            testid="status-donnees"
            ton={ind.donnees.ton}
            valeur={ind.donnees.titre}
            detail={
              <>
                {ind.donnees.texte}
                {fiable ? (
                  <>
                    <br />
                    Source : {dash.statut.donnees.source}
                    {dash.statut.donnees.age_s !== null ? ` · dernière barre : ${duree(Math.max(0, dash.statut.donnees.age_s))}` : " · aucune barre reçue"}
                  </>
                ) : null}
              </>
            }
          />
          <StatusTile label="Moteur de stratégie" testid="status-moteur" ton={ind.moteur.ton} valeur={ind.moteur.titre} detail={ind.moteur.texte} />
          <StatusTile
            label="Notifications (Telegram)"
            testid="status-notifications"
            ton={ind.notifications.ton}
            valeur={ind.notifications.titre}
            detail={
              <>
                {ind.notifications.texte}
                {fiable && dash.statut.notifications.derniere ? (
                  <>
                    <br />
                    Dernier envoi réussi : {dateHeure(dash.statut.notifications.derniere)}
                  </>
                ) : null}
              </>
            }
          />
        </div>
      </Card>

      {fiable ? (
        <>
          <Marche dash={dash} />
          <Trading dash={dash} />
        </>
      ) : dash ? (
        <Banner ton="bad" titre="Marché et trading masqués" testid="infos-masquees">
          <p>Le serveur ne répond pas : les derniers prix et signaux reçus ({ilYa(d.ageS)}) ne sont plus fiables et ne sont pas affichés.</p>
        </Banner>
      ) : null}

      <Actions dash={fiable ? dash : null} recharger={d.recharger} />
    </>
  );
}

function Marche({ dash }: { dash: Dashboard }) {
  const m = dash.marche;
  return (
    <Card titre="État du marché" testid="carte-marche" id="marche">
      <Kv
        items={[
          [
            "Instrument",
            <span data-testid="marche-instrument">
              {m.instrument.replace(/\s*\(.*\)\s*$/, "")}
              <span className="sub">
                TradingView : <code>{m.tradingview}</code> · Tradovate : <code>{m.tradovate}</code>
              </span>
              <span className="sub">
                Prochain changement de contrat (roll) : {dateCourte(m.prochain_roll)} → {m.contrat_suivant}
              </span>
            </span>,
          ],
          [
            "Prix de référence",
            <span data-testid="marche-prix">
              <span className="num">{m.prix !== null ? prix(m.prix) : "indisponible"}</span>
              <span className="sub">{m.prix_maj ? `barre terminée à ${dateHeure(m.prix_maj)} (Paris)` : "aucune barre reçue"}</span>
            </span>,
          ],
          [
            "Session actuelle",
            <span data-testid="marche-seance">
              {m.seance}
              {m.seance === "fermé (jour férié)" || m.seance === "fermé (clôture anticipée)" ? (
                <span className="sub" data-testid="marche-seance-calendrier">
                  Calendrier CME des jours fériés et clôtures anticipées intégré à GoldPilot : dates à vérifier sur le site du CME Group.
                </span>
              ) : null}
            </span>,
          ],
          [
            "Régime identifié",
            <span data-testid="marche-regime">
              {m.regime ?? "non déterminé (aucune analyse)"}
              {m.ecart_moyenne_atr !== null ? <span className="sub">écart à la moyenne de séance : {nombre(m.ecart_moyenne_atr, 2)} ATR</span> : null}
            </span>,
          ],
          [
            "Prochaine annonce importante",
            <span data-testid="marche-annonce">
              {m.prochaine_annonce ? (
                <>
                  {m.prochaine_annonce.titre}
                  <span className="sub">
                    {m.prochaine_annonce.quand} · {m.prochaine_annonce.ny}
                  </span>
                </>
              ) : (
                "aucune dans les 14 prochains jours (calendrier connu)"
              )}
            </span>,
          ],
        ]}
      />
    </Card>
  );
}

function Trading({ dash }: { dash: Dashboard }) {
  const t = dash.trading;
  const enCours = t.signal_en_cours;
  const dernier = t.dernier_signal && (!enCours || t.dernier_signal.id !== enCours.id) ? t.dernier_signal : null;
  const cs = t.compte_simule;
  return (
    <section className="card" data-testid="carte-trading" aria-labelledby="trading-titre">
      <h2 id="trading-titre">État du trading</h2>

      <div id="signal-en-cours">
        {enCours ? (
          <SignalCard sig={enCours} titre="Signal en cours" />
        ) : (
          <div className="none-setup" data-testid="aucun-setup">
            <Icon name="neutral" />
            <span>{t.setup}</span>
          </div>
        )}
      </div>

      {t.derniere_analyse ? (
        <p className="small muted" style={{ marginTop: 8 }} data-testid="derniere-analyse">
          Dernière analyse ({t.derniere_analyse.heure}) : {t.derniere_analyse.resultat}
          {t.derniere_analyse.raisons?.length ? ` — ${t.derniere_analyse.raisons.join(" ; ")}` : ""}
        </p>
      ) : null}

      <h3 style={{ marginTop: 14 }}>Dernier signal</h3>
      {dernier ? (
        <Link to={`/signal/${dernier.id}`} className="sig-row" data-testid="dernier-signal">
          <span className="sig-title">
            {dernier.sens} {dernier.contrat}
          </span>
          <span className="sig-res">{statutSignal(dernier.statut).libelle}</span>
          <span className="sig-meta">
            {dernier.cree_paris} · entrée {prix(dernier.entree)} · stop {prix(dernier.stop)}
          </span>
        </Link>
      ) : (
        <p className="muted" data-testid="dernier-signal">
          {enCours ? "C'est le signal en cours ci-dessus." : "Aucun signal émis pour l'instant."}
        </p>
      )}

      <h3 style={{ marginTop: 14 }}>Statut de la stratégie</h3>
      <div className="row" style={{ marginBottom: 6 }} data-testid="statut-strategie">
        <Badge ton={t.strategie.validee ? "ok" : "bad"}>{t.strategie.validee ? "Validée" : "NON VALIDÉE"}</Badge>
        <Badge ton={t.mode_trading === "reel" ? "bad" : "warn"}>Mode {t.mode_trading === "reel" ? "réel" : "simulation"}</Badge>
        {t.mode_utilisateur === "pause" ? <Badge ton="warn">Signaux suspendus par toi</Badge> : null}
      </div>
      <p className="small muted">
        {t.strategie.version ? `Version ${t.strategie.version}. ` : ""}
        <Link to="/statistiques">Lire le verdict complet</Link>
      </p>

      <h3 style={{ marginTop: 14 }}>Risque autorisé et limites</h3>
      <Kv
        items={[
          ["Risque par trade", usd(t.risque.par_trade_usd)],
          ["Perte journalière interne", `${usd(t.risque.perte_jour_max_usd)} (arrêt des signaux du jour)`],
          ["Trades par jour", `${t.risque.trades_jour_max} au maximum`],
          ["Programme", t.risque.programme],
          ["Perte maximale du programme", usd(t.risque.perte_max_programme)],
          ["Objectif de profit", t.risque.objectif !== null ? usd(t.risque.objectif) : "aucun (compte financé)"],
        ]}
      />

      <h3 style={{ marginTop: 14 }}>État du compte</h3>
      <div data-testid="etat-compte">
        {t.compte_reel ? (
          <p>
            <Badge ton="info">Compte réel — déclaré par toi</Badge> Solde {usd(t.compte_reel.solde)} (déclaré le {t.compte_reel.maj}).
          </p>
        ) : (
          <p className="small">
            Compte FundedNext : <strong>données non disponibles</strong>. Le système ne peut pas lire ton compte ;{" "}
            <Link to="/reglages#compte">déclare ton solde</Link> si tu veux qu'il en tienne compte.
          </p>
        )}
        {cs ? (
          <>
            <p className="small" style={{ marginBottom: 6 }}>
              <Badge ton="neutral">Compte simulé</Badge> suivi papier des signaux, ce n'est pas ton compte FundedNext.
            </p>
            <Kv
              items={[
                ["Solde simulé", usd(cs.balance)],
                ["Plancher simulé (perte max)", usd(cs.floor)],
                ["Coussin simulé", usd(cs.balance - cs.floor)],
                ["Meilleur jour simulé", usd(cs.best_day)],
                [
                  "État simulé",
                  cs.breached ? `violé : ${cs.breach_reason}` : cs.passed ? "objectif simulé atteint" : `en cours (${cs.days} jour(s) de suivi)`,
                ],
              ]}
            />
          </>
        ) : null}
      </div>
    </section>
  );
}

function Actions({ dash, recharger }: { dash: Dashboard | null; recharger: () => Promise<void> }) {
  const a = useAction();
  const pause = dash?.trading.mode_utilisateur === "pause";
  const notifOn = dash?.statut.notifications.active ?? true;
  const arret = dash?.statut.moteur.arret ?? null;
  const go = async (fn: () => Promise<unknown>, ok: string) => {
    await a.lancer(fn, ok);
    await recharger();
  };
  return (
    <Card titre="Actions" testid="carte-actions" id="actions">
      <div className="actions">
        <button
          type="button"
          className="btn"
          disabled={!dash || a.enCours}
          data-testid="action-mode"
          onClick={() =>
            go(
              () => api.post("/api/engine/mode", { mode: pause ? "actif" : "pause" }),
              pause ? "Génération des signaux reprise." : "Génération des signaux suspendue.",
            )
          }
        >
          <Icon name={pause ? "play" : "pause"} />
          {pause ? "Reprendre les signaux" : "Suspendre les signaux"}
        </button>
        <button
          type="button"
          className="btn"
          disabled={!dash || a.enCours}
          data-testid="action-notifications"
          onClick={() =>
            go(() => api.post("/api/notifications/toggle", { active: !notifOn }), notifOn ? "Notifications désactivées." : "Notifications activées.")
          }
        >
          <Icon name="bell" />
          {notifOn ? "Désactiver les notifications" : "Activer les notifications"}
        </button>
        <button
          type="button"
          className="btn"
          disabled={!dash || a.enCours}
          data-testid="action-test-notification"
          onClick={() => go(() => api.post("/api/notifications/test"), "Notification de test envoyée : vérifie ton téléphone.")}
        >
          <Icon name="send" />
          Tester une notification
        </button>
        <Link to="/historique" className="btn" data-testid="action-historique">
          <Icon name="list" />
          Historique
        </Link>
        <Link to="/reglages" className="btn" data-testid="action-parametres">
          <Icon name="settings" />
          Paramètres
        </Link>
      </div>
      {arret && arret.type === "version" ? (
        <div style={{ marginTop: 12 }}>
          <Banner ton="bad" titre="Arrêt de sécurité : nouvelle version de stratégie" testid="arret-securite">
            <p>
              {arret.raison} (depuis {dateHeure(arret.depuis)}). Aucun signal tant que tu n'as pas comparé puis approuvé cette version.
            </p>
          </Banner>
          <Link to="/reglages#gouvernance" className="btn danger" data-testid="action-approuver-version">
            Comparer et approuver la version (Paramètres)
          </Link>
        </div>
      ) : arret ? (
        <div style={{ marginTop: 12 }}>
          <Banner ton="bad" titre="Arrêt de sécurité" testid="arret-securite">
            <p>
              {arret.raison} (depuis {dateHeure(arret.depuis)}). La reprise est manuelle : analyse d'abord les statistiques et le journal.
              Après la reprise, les seuils (drawdown, série de pertes) sont recomptés à partir des trades clôturés après ce moment.
            </p>
          </Banner>
          <button
            type="button"
            className="btn danger"
            data-testid="action-reprise-arret"
            disabled={a.enCours}
            onClick={() => {
              if (window.confirm("Reprendre après l'arrêt de sécurité ? Le moteur pourra de nouveau émettre des signaux.")) {
                void go(() => api.post("/api/engine/resume-after-halt"), "Arrêt de sécurité levé.");
              }
            }}
          >
            Reprendre après l'arrêt de sécurité
          </button>
        </div>
      ) : null}
      <Msg message={a.message} />
    </Card>
  );
}
