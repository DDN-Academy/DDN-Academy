import { useEffect, useState, type FormEvent } from "react";
import { Link } from "react-router-dom";
import { api, ApiError } from "../lib/api";
import { useAction, useRessource, useTitre } from "../lib/hooks";
import { useDashboard } from "../lib/dashboard";
import type { Calendrier, JournalLigne, Programme, Reglages, RiskSettings } from "../lib/types";
import { STATUT_REGLE } from "../lib/status";
import { etatReceptionTradingView } from "../lib/tradingview";
import { dateCourte, dateHeure, nombre, pct, usd, versIsoAvecFuseau } from "../lib/format";
import { Badge, Banner, BoutonCopier, Card, Chargement, Erreur, Icon, Kv, Msg } from "../components/ui";

export function Settings() {
  useTitre("Réglages");
  const r = useRessource<Reglages>("/api/settings");
  return (
    <>
      <div className="page-head">
        <h1>Réglages</h1>
      </div>
      <nav className="toc" aria-label="Sections des réglages">
        <a href="#risque">Risque</a>
        <a href="#programme">Programme FundedNext</a>
        <a href="#mode">Mode de trading</a>
        <a href="#compte">Compte réel</a>
        <a href="#tradingview">TradingView</a>
        <a href="#telegram">Telegram</a>
        <a href="#calendrier">Calendrier</a>
        <Link to="/aide">Aide</Link>
      </nav>
      {r.chargement && !r.data ? <Chargement /> : null}
      {r.erreur && !r.data ? <Erreur texte={r.erreur.message} /> : null}
      {r.data ? (
        <>
          <Risque reglages={r.data} recharger={r.recharger} />
          <ProgrammeSection reglages={r.data} recharger={r.recharger} />
          <ModeTrading reglages={r.data} recharger={r.recharger} />
          <CompteReel />
          <TradingView reglages={r.data} />
          <Telegram reglages={r.data} />
          <CalendrierSection />
        </>
      ) : null}
    </>
  );
}

// ------------------------------------------------------------------------------------------- (a) risque
type ChampRisque = { cle: keyof RiskSettings; libelle: string; unite: string; aide: string; pas: string; entier?: boolean };

export const CHAMPS_RISQUE: ChampRisque[] = [
  { cle: "risk_per_trade_usd", libelle: "Risque par trade", unite: "$", pas: "5", aide: "Perte acceptée si le stop est touché. Entre 25 et 500 $ (perte maximale du compte : 1 500 $)." },
  { cle: "daily_loss_stop_usd", libelle: "Perte journalière interne", unite: "$", pas: "10", aide: "Au-delà, plus aucun signal ce jour-là. Au moins égale au risque par trade." },
  { cle: "max_trades_per_day", libelle: "Trades maximum par jour", unite: "trades", pas: "1", entier: true, aide: "Entre 1 et 6." },
  { cle: "max_losses_per_day", libelle: "Pertes maximum par jour", unite: "pertes", pas: "1", entier: true, aide: "Entre 1 et le nombre maximum de trades." },
  { cle: "max_cushion_fraction", libelle: "Part maximale du coussin risquée", unite: "fraction", pas: "0.01", aide: "Part du coussin restant au-dessus du plancher qu'un trade peut risquer. Entre 0,05 et 0,35." },
  { cle: "safety_margin_usd", libelle: "Marge de sécurité au-dessus du plancher", unite: "$", pas: "10", aide: "Montant jamais engagé, retiré du coussin avant tout calcul." },
  { cle: "consistency_lock_fraction", libelle: "Verrouillage de consistance", unite: "fraction", pas: "0.05", aide: "Arrêt du jour quand le profit du jour atteint cette part du plafond de consistance (40 % de l'objectif). Entre 0,3 et 1." },
  { cle: "slippage_allowance_oz", libelle: "Glissement prévu", unite: "$ / once", pas: "0.05", aide: "Ajouté à la distance au stop pour calculer la taille (1 MGC = 10 onces)." },
  { cle: "commission_per_contract_rt", libelle: "Commission par contrat (aller-retour)", unite: "$", pas: "0.1", aide: "Hypothèse : le tarif tout compris FundedNext n'est pas publié." },
  { cle: "max_contracts_personal", libelle: "Plafond personnel de contrats", unite: "MGC", pas: "1", entier: true, aide: "Entre 1 et 30 (limite Flex 50K : 30 micros)." },
];

function Risque({ reglages, recharger }: { reglages: Reglages; recharger: () => Promise<void> }) {
  const init = () => Object.fromEntries(CHAMPS_RISQUE.map((c) => [c.cle, String(reglages.risque[c.cle] ?? "")])) as Record<keyof RiskSettings, string>;
  const [v, setV] = useState(init);
  const a = useAction();
  useEffect(() => setV(init()), [reglages]);

  async function envoyer(e: FormEvent) {
    e.preventDefault();
    const corps: Record<string, number> = {};
    for (const c of CHAMPS_RISQUE) {
      const n = Number(v[c.cle].replace(",", "."));
      if (v[c.cle].trim() === "" || !Number.isFinite(n)) {
        a.setMessage({ ton: "bad", texte: `${c.libelle} : nombre attendu.` });
        return;
      }
      if (c.entier && !Number.isInteger(n)) {
        a.setMessage({ ton: "bad", texte: `${c.libelle} : nombre entier attendu.` });
        return;
      }
      corps[c.cle] = n;
    }
    const ok = await a.lancer(() => api.put("/api/settings/risk", corps), "Paramètres de risque enregistrés (appliqués aux prochaines décisions).");
    if (ok) await recharger();
  }

  return (
    <Card titre="Risque" id="risque" testid="reglages-risque" sous="Ces limites sont appliquées par le moteur de risque avant chaque signal. Elles restent plus prudentes que les limites FundedNext.">
      <form onSubmit={envoyer} data-testid="form-risque" noValidate>
        <div className="form-grid">
          {CHAMPS_RISQUE.map((c) => (
            <div className="field" key={c.cle}>
              <label htmlFor={`r-${c.cle}`}>{c.libelle}</label>
              <div className="input-unit">
                <input
                  id={`r-${c.cle}`}
                  type="number"
                  inputMode="decimal"
                  step={c.pas}
                  value={v[c.cle]}
                  onChange={(e) => setV({ ...v, [c.cle]: e.target.value })}
                  aria-describedby={`r-${c.cle}-aide`}
                  data-testid={`champ-${c.cle}`}
                />
                <span className="unit">{c.unite}</span>
              </div>
              <span className="hint" id={`r-${c.cle}-aide`}>
                {c.aide}
              </span>
            </div>
          ))}
        </div>
        <div className="row">
          <button type="submit" className="btn primary" disabled={a.enCours} data-testid="bouton-enregistrer-risque">
            Enregistrer
          </button>
          <button type="button" className="btn" onClick={() => setV(init())}>
            Annuler les modifications
          </button>
        </div>
        <Msg message={a.message} />
      </form>
    </Card>
  );
}

// ------------------------------------------------------------------------------------------- (b) programme
function ProgrammeSection({ reglages, recharger }: { reglages: Reglages; recharger: () => Promise<void> }) {
  const [choix, setChoix] = useState(reglages.programme);
  const a = useAction();
  useEffect(() => setChoix(reglages.programme), [reglages.programme]);
  const p: Programme | undefined = reglages.programmes[choix];
  return (
    <Card titre="Programme FundedNext" id="programme" testid="reglages-programme" sous={`Règles vérifiées le ${dateCourte(reglages.regles_verifiees_le)} sur les pages officielles. À reconfirmer dans ton espace FundedNext.`}>
      <form
        data-testid="form-programme"
        onSubmit={async (e) => {
          e.preventDefault();
          const ok = await a.lancer(() => api.put("/api/settings/program", { programme: choix }), "Programme enregistré.");
          if (ok) await recharger();
        }}
      >
        <div className="field">
          <label htmlFor="programme">Ton programme</label>
          <select id="programme" value={choix} onChange={(e) => setChoix(e.target.value)} data-testid="champ-programme">
            {Object.values(reglages.programmes).map((x) => (
              <option key={x.key} value={x.key}>
                {x.label}
              </option>
            ))}
          </select>
        </div>
        <button type="submit" className="btn primary" disabled={a.enCours || choix === reglages.programme} data-testid="bouton-enregistrer-programme">
          {choix === reglages.programme ? "Programme actif" : "Utiliser ce programme"}
        </button>
        <Msg message={a.message} />
      </form>
      {p ? (
        <>
          <div style={{ marginTop: 14 }}>
            <Kv
              items={[
                ["Phase", p.phase === "challenge" ? "Challenge" : "Compte financé"],
                ["Taille du compte", usd(p.account_size)],
                ["Objectif de profit", p.profit_target !== null ? usd(p.profit_target) : "aucun"],
                ["Perte maximale", `${usd(p.max_loss)}${p.trailing_eod ? " sous le plus haut solde de fin de journée" : ""}`],
                ["Plancher initial", usd(p.initial_floor)],
                ["Verrouillage du plancher", p.lock_balance !== null ? usd(p.lock_balance) : "—"],
                ["Limite journalière", p.daily_loss_limit !== null ? usd(p.daily_loss_limit) : "aucune"],
                ["Consistance", p.consistency_pct !== null ? `aucun jour > ${pct(p.consistency_pct, 0)} de l'objectif (${usd(p.consistency_cap)})` : "aucune"],
                ["Contrats maximum", `${p.max_micros} micros`],
                ["Positions fermées avant", `${p.flat_by_ny} New York`],
                ...(p.phase === "funded"
                  ? ([
                      ["Retraits", `${p.min_benchmark_days ?? "?"} jours ≥ ${usd(p.benchmark_min_profit)} ; ${usd(p.min_withdrawal)} à ${usd(p.max_withdrawal)} par cycle ; part ${pct(p.reward_share, 0)}`],
                    ] as [string, string][])
                  : []),
                ["Profil confirmé par toi", p.user_confirmed ? "oui" : "non"],
              ]}
            />
          </div>
          <h3 style={{ marginTop: 14 }}>Règles et leur statut</h3>
          <p className="small muted">Une règle incertaine (contradictoire ou inconnue) bloque les trades potentiellement non conformes en mode réel.</p>
          <ul className="list" data-testid="table-regles">
            {p.rules.map((rg, i) => (
              <li key={i} data-testid="ligne-regle">
                <div className="row">
                  <strong>{rg.name}</strong>
                  <Badge ton={STATUT_REGLE[rg.status] ?? "warn"}>{rg.status}</Badge>
                </div>
                <div>{rg.value}</div>
                <div className="small muted">
                  <a href={rg.source} target="_blank" rel="noopener noreferrer">
                    page officielle
                  </a>{" "}
                  · vérifié le {dateCourte(p.checked_on)}
                </div>
              </li>
            ))}
          </ul>
        </>
      ) : null}
    </Card>
  );
}

// ------------------------------------------------------------------------------------------- (c) mode de trading
const PHRASE = "JE CONFIRME LE PASSAGE EN REEL";

function ModeTrading({ reglages, recharger }: { reglages: Reglages; recharger: () => Promise<void> }) {
  const fn = reglages.confirmation_fundednext;
  const [confirme, setConfirme] = useState(fn.confirme);
  const [reference, setReference] = useState(fn.reference ?? "");
  const [phrase, setPhrase] = useState("");
  const aFn = useAction();
  const aMode = useAction();
  useEffect(() => {
    setConfirme(fn.confirme);
    setReference(fn.reference ?? "");
  }, [fn.confirme, fn.reference]);
  const reel = reglages.mode_trading === "reel";

  return (
    <Card titre="Mode de trading" id="mode" testid="reglages-mode">
      <p className="row">
        Mode actuel : <Badge ton={reel ? "bad" : "warn"} testid="mode-actuel">{reel ? "Réel" : "Simulation"}</Badge>
      </p>
      {!reglages.strategie_validee ? (
        <Banner ton="bad" titre="Mode réel verrouillé" testid="verrou-reel">
          <p>
            La stratégie n'a pas satisfait les critères de validation fixés avant les tests. Le serveur refuse le passage en réel tant qu'une
            validation prospective (suivi papier en conditions réelles) ne l'a pas confirmée. <Link to="/statistiques">Voir les résultats</Link>.
          </p>
        </Banner>
      ) : null}
      <p className="small">
        Le passage en réel exige trois conditions vérifiées par le serveur : stratégie validée, confirmation écrite de FundedNext déclarée
        ci-dessous, et la phrase de confirmation exacte. Même en réel, tu exécutes toi-même chaque trade : GoldPilot ne passe aucun ordre.
      </p>

      <h3>Confirmation écrite de FundedNext</h3>
      <p className="small muted">
        Les règles FundedNext interdisent les « signaux externes » ; l'usage d'un outil d'alerte personnel n'est pas confirmé par écrit. Demande
        au support FundedNext une confirmation écrite, puis déclare-la ici.
      </p>
      <form
        data-testid="form-confirmation-fundednext"
        noValidate
        onSubmit={async (e) => {
          e.preventDefault();
          const ok = await aFn.lancer(
            () => api.put("/api/settings/fundednext-confirmation", { confirme: confirme, reference }),
            confirme ? "Confirmation FundedNext enregistrée." : "Confirmation FundedNext retirée.",
          );
          if (ok) await recharger();
        }}
      >
        <div className="field">
          <label className="check">
            <input type="checkbox" checked={confirme} onChange={(e) => setConfirme(e.target.checked)} data-testid="champ-confirmation-fundednext" />
            <span>J'ai reçu de FundedNext une réponse écrite autorisant l'usage de cet outil d'alerte personnel sur mon compte.</span>
          </label>
        </div>
        <div className="field">
          <label htmlFor="fn-ref">Référence de la réponse (numéro de ticket, date de l'e-mail…)</label>
          <input id="fn-ref" type="text" maxLength={200} value={reference} onChange={(e) => setReference(e.target.value)} data-testid="champ-reference-fundednext" />
        </div>
        {fn.date ? <p className="small muted">Dernière déclaration : {dateHeure(fn.date)}.</p> : null}
        <button type="submit" className="btn" disabled={aFn.enCours} data-testid="bouton-enregistrer-confirmation">
          Enregistrer la déclaration
        </button>
        <Msg message={aFn.message} />
      </form>

      <h3 style={{ marginTop: 16 }}>Changer de mode</h3>
      {reel ? (
        <button
          type="button"
          className="btn"
          data-testid="bouton-mode-simulation"
          disabled={aMode.enCours}
          onClick={async () => {
            const ok = await aMode.lancer(() => api.put("/api/settings/trading-mode", { mode: "simulation", confirmation: "" }), "Retour en simulation.");
            if (ok) await recharger();
          }}
        >
          Revenir en simulation
        </button>
      ) : (
        <form
          data-testid="form-mode-reel"
          noValidate
          onSubmit={async (e) => {
            e.preventDefault();
            const ok = await aMode.lancer(() => api.put("/api/settings/trading-mode", { mode: "reel", confirmation: phrase }), "Mode réel activé.");
            if (ok) await recharger();
          }}
        >
          <div className="field">
            <label htmlFor="phrase">Phrase de confirmation</label>
            <input id="phrase" type="text" autoComplete="off" value={phrase} onChange={(e) => setPhrase(e.target.value)} data-testid="champ-phrase-confirmation" />
            <span className="hint">
              Recopie exactement : <code>{PHRASE}</code>
            </span>
          </div>
          <button type="submit" className="btn danger" disabled={aMode.enCours} data-testid="bouton-mode-reel">
            Demander le passage en réel
          </button>
        </form>
      )}
      <Msg message={aMode.message} />
    </Card>
  );
}

// ------------------------------------------------------------------------------------------- (d) compte réel
function CompteReel() {
  const d = useDashboard();
  const cr = d.data?.trading.compte_reel ?? null;
  const [solde, setSolde] = useState("");
  const [hwm, setHwm] = useState("");
  const [best, setBest] = useState("");
  const [note, setNote] = useState("");
  const a = useAction();
  const num = (s: string) => (s.trim() === "" ? null : Number(s.replace(",", ".")));

  return (
    <Card titre="Compte réel FundedNext" id="compte" testid="reglages-compte">
      <Banner ton="info" titre="Le système ne peut pas lire ton compte FundedNext">
        <p>
          Aucune API officielle ne lui donne accès à ton solde. Déclare-le ici (idéalement chaque jour avant la séance) : sans déclaration du
          jour, le moteur applique une hypothèse prudente.
        </p>
      </Banner>
      <p className="small">
        Dernière déclaration : {cr ? `${usd(cr.solde)} le ${cr.maj}` : "aucune"}.
      </p>
      <form
        data-testid="form-compte"
        noValidate
        onSubmit={async (e) => {
          e.preventDefault();
          const corps = { solde: num(solde), plus_haut_fin_de_jour: num(hwm), meilleur_jour: num(best), note };
          if (corps.solde === null) {
            a.setMessage({ ton: "bad", texte: "Le solde est obligatoire." });
            return;
          }
          if ([corps.solde, corps.plus_haut_fin_de_jour, corps.meilleur_jour].some((x) => x !== null && !Number.isFinite(x))) {
            a.setMessage({ ton: "bad", texte: "Un des nombres saisis est invalide." });
            return;
          }
          const ok = await a.lancer(() => api.post("/api/account", corps), "État du compte enregistré (déclaré par toi).");
          if (ok) {
            setSolde("");
            setHwm("");
            setBest("");
            setNote("");
            await d.recharger();
          }
        }}
      >
        <div className="form-grid">
          <div className="field">
            <label htmlFor="c-solde">Solde actuel</label>
            <div className="input-unit">
              <input id="c-solde" type="number" inputMode="decimal" step="0.01" value={solde} onChange={(e) => setSolde(e.target.value)} data-testid="champ-solde" />
              <span className="unit">$</span>
            </div>
          </div>
          <div className="field">
            <label htmlFor="c-hwm">Plus haut solde de fin de journée</label>
            <div className="input-unit">
              <input id="c-hwm" type="number" inputMode="decimal" step="0.01" value={hwm} onChange={(e) => setHwm(e.target.value)} data-testid="champ-plus-haut" />
              <span className="unit">$</span>
            </div>
            <span className="hint">Sert à calculer ton plancher de perte maximale (affiché par FundedNext).</span>
          </div>
          <div className="field">
            <label htmlFor="c-best">Meilleur jour (profit)</label>
            <div className="input-unit">
              <input id="c-best" type="number" inputMode="decimal" step="0.01" min="0" value={best} onChange={(e) => setBest(e.target.value)} data-testid="champ-meilleur-jour" />
              <span className="unit">$</span>
            </div>
            <span className="hint">Pour la règle de consistance (40 %).</span>
          </div>
          <div className="field">
            <label htmlFor="c-note">Note (facultatif)</label>
            <input id="c-note" type="text" maxLength={300} value={note} onChange={(e) => setNote(e.target.value)} data-testid="champ-note-compte" />
          </div>
        </div>
        <button type="submit" className="btn primary" disabled={a.enCours} data-testid="bouton-enregistrer-compte">
          Enregistrer l'état du compte
        </button>
        <Msg message={a.message} />
      </form>
    </Card>
  );
}

// ------------------------------------------------------------------------------------------- (e) TradingView
function TradingView({ reglages }: { reglages: Reglages }) {
  const tv = reglages.tradingview;
  const d = useDashboard();
  const wh = useRessource<{ lignes: JournalLigne[] }>("/api/journal?type=webhooks&limit=50");
  const [script, setScript] = useState<string | null>(null);
  const [erreurScript, setErreurScript] = useState<string | null>(null);
  const acceptes = (wh.data?.lignes ?? []).filter((l) => l.accepte);
  const refuses = (wh.data?.lignes ?? []).filter((l) => !l.accepte);
  const etat = wh.data
    ? etatReceptionTradingView(reglages.source_donnees, acceptes.length, d.joignable ? (d.data?.statut.donnees.ok ?? null) : null, d.joignable ? (d.data?.statut.donnees.age_s ?? null) : null)
    : null;

  async function chargerScript(): Promise<string | null> {
    if (script) return script;
    try {
      const t = await api.getText("/api/setup/pine");
      setScript(t);
      setErreurScript(null);
      return t;
    } catch (e) {
      setErreurScript(e instanceof ApiError ? e.message : "Erreur inattendue.");
      return null;
    }
  }

  async function telecharger() {
    const t = await chargerScript();
    if (!t) return;
    const url = URL.createObjectURL(new Blob([t], { type: "text/plain;charset=utf-8" }));
    const lien = document.createElement("a");
    lien.href = url;
    lien.download = "goldpilot_bridge.pine";
    document.body.appendChild(lien);
    lien.click();
    lien.remove();
    window.setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  return (
    <Card titre="TradingView" id="tradingview" testid="reglages-tradingview">
      <div data-testid="etat-tradingview">
        {etat ? (
          <Banner ton={etat.ton} titre={etat.ton === "ok" ? "Webhooks reçus" : etat.ton === "neutral" ? "Non utilisé" : "Non connecté"}>
            <p>
              {etat.texte}
              {acceptes[0] ? ` Dernier webhook accepté : ${String(acceptes[0].heure)}.` : ""}
              {refuses[0] ? ` Dernier refus : ${String(refuses[0].heure)} (${String(refuses[0].raison)}).` : ""}
            </p>
          </Banner>
        ) : wh.erreur ? (
          <Erreur texte={wh.erreur.message} />
        ) : (
          <Chargement texte="Vérification de la réception…" />
        )}
      </div>
      <p className="small">
        Il n'existe pas d'API TradingView pour connecter ton compte : GoldPilot reçoit les prix grâce à un script Pine qui envoie une alerte
        (webhook) à chaque minute. On ne te demande jamais ton mot de passe TradingView.
      </p>
      <div className="field">
        <span className="label">Adresse du webhook (à coller dans l'alerte)</span>
        <div className="copy-field">
          <code data-testid="url-webhook">{tv.url_webhook}</code>
          <BoutonCopier texte={tv.url_webhook} testid="copier-url-webhook" />
        </div>
      </div>
      <Kv
        items={[
          ["Symbole du graphique", <code>{tv.symbole}</code>],
          ["Unité de temps", tv.unite],
          ["Jeton secret", tv.jeton_defini ? "défini sur le serveur (TV_WEBHOOK_TOKEN), jamais affiché ici" : "NON défini sur le serveur : les webhooks seront refusés"],
          ["Source de données du serveur", reglages.source_donnees],
        ]}
      />
      <h3 style={{ marginTop: 14 }}>Mise en place, étape par étape</h3>
      <ol className="steps">
        <li>
          Abonnement TradingView <strong>payant</strong> (Essential ou supérieur) : le plan gratuit ne peut pas envoyer de webhooks.
        </li>
        <li>
          Active la <strong>double authentification (2FA)</strong> sur TradingView : elle est obligatoire pour les webhooks.
        </li>
        <li>
          Souscris aux <strong>données temps réel CME/COMEX</strong> dans TradingView : sans elles, les prix ont 10 minutes de retard et le
          serveur les refuse.
        </li>
        <li>
          Ouvre le graphique <code>{tv.symbole}</code> en unité <strong>1 minute</strong>.
        </li>
        <li>Ouvre l'éditeur Pine, colle le script ci-dessous, enregistre-le puis ajoute-le au graphique.</li>
        <li>Dans les paramètres de l'indicateur, saisis le jeton secret (la valeur de TV_WEBHOOK_TOKEN définie sur le serveur).</li>
        <li>
          Crée une alerte : condition « GoldPilot Bridge » → « Tout appel de la fonction alert() » ; dans Notifications, coche « URL du webhook
          » et colle l'adresse ci-dessus.
        </li>
        <li>
          Vérifie dans <Link to="/journal?onglet=webhooks">Journal › Webhooks</Link> que des messages « Accepté » arrivent chaque minute
          pendant les heures de marché.
        </li>
        <li>
          Note la <strong>date d'expiration</strong> de l'alerte : sauf sur les plans Premium et Ultimate, TradingView arrête une alerte
          au bout de 2 mois. Recrée-la avant cette date (et à chaque changement d'échéance du contrat).
        </li>
        <li>À chaque changement de contrat (roll), refais l'alerte sur le nouveau contrat indiqué sur la page d'accueil.</li>
      </ol>
      <p className="small muted">Le script n'a pas pu être testé sur TradingView depuis l'environnement de développement : seule la réception constatée dans le journal fait foi.</p>
      <div className="row">
        <button type="button" className="btn" onClick={() => void chargerScript()} data-testid="bouton-voir-pine">
          Afficher le script Pine
        </button>
        <button type="button" className="btn" onClick={() => void telecharger()} data-testid="bouton-telecharger-pine">
          <Icon name="download" />
          Télécharger
        </button>
        {script ? <BoutonCopier texte={script} libelle="Copier le script" testid="bouton-copier-pine" /> : null}
      </div>
      {erreurScript ? <div className="msg bad">{erreurScript}</div> : null}
      {script ? (
        <pre className="code" data-testid="script-pine" tabIndex={0} aria-label="Script Pine GoldPilot Bridge">
          {script}
        </pre>
      ) : null}
    </Card>
  );
}

// ------------------------------------------------------------------------------------------- (f) Telegram
function Telegram({ reglages }: { reglages: Reglages }) {
  const tg = reglages.telegram;
  const d = useDashboard();
  const detect = useAction();
  const test = useAction();
  const [convs, setConvs] = useState<{ chat_id: string; nom: string }[] | null>(null);
  const n = d.data?.statut.notifications;
  return (
    <Card titre="Notifications Telegram" id="telegram" testid="reglages-telegram">
      <div className="row" style={{ marginBottom: 10 }} data-testid="etat-telegram">
        <Badge ton={tg.jeton_defini ? "ok" : "bad"}>{tg.jeton_defini ? "Jeton du bot défini" : "Jeton du bot absent"}</Badge>
        <Badge ton={tg.configure ? "ok" : "bad"}>{tg.configure ? "Identifiant de conversation défini" : "Identifiant de conversation absent"}</Badge>
        {n ? <Badge ton={n.ok ? "ok" : "warn"}>{n.texte}</Badge> : null}
      </div>
      <p className="small">Telegram est gratuit. Les secrets restent sur le serveur : ils ne sont jamais saisis ni affichés sur ce site.</p>
      <ol className="steps">
        <li>
          Dans Telegram, ouvre <strong>@BotFather</strong>, envoie <code>/newbot</code> et choisis un nom : il te donne un jeton.
        </li>
        <li>
          Place ce jeton dans la variable <code>TELEGRAM_BOT_TOKEN</code> du serveur, puis redémarre le service.
        </li>
        <li>Ouvre la conversation avec ton nouveau bot et envoie-lui un message (par exemple « bonjour »).</li>
        <li>Clique sur « Détecter mon identifiant » ci-dessous.</li>
        <li>
          Place la valeur trouvée dans <code>TELEGRAM_CHAT_ID</code> sur le serveur, puis redémarre le service.
        </li>
        <li>Clique sur « Tester une notification » : tu dois recevoir un message sur ton téléphone.</li>
      </ol>
      <div className="row">
        <button
          type="button"
          className="btn"
          disabled={detect.enCours}
          data-testid="bouton-detecter-chat"
          onClick={async () => {
            setConvs(null);
            await detect.lancer(async () => {
              const r = await api.post<{ conversations: { chat_id: string; nom: string }[] }>("/api/notifications/detect-chat");
              setConvs(r.conversations);
            }, "Recherche terminée.");
          }}
        >
          Détecter mon identifiant
        </button>
        <button
          type="button"
          className="btn"
          disabled={test.enCours}
          data-testid="bouton-test-notification"
          onClick={() => void test.lancer(() => api.post("/api/notifications/test"), "Notification de test envoyée : vérifie ton téléphone.")}
        >
          <Icon name="send" />
          Tester une notification
        </button>
      </div>
      <Msg message={detect.message} />
      {convs !== null ? (
        convs.length === 0 ? (
          <p className="small" data-testid="resultat-detection">
            Aucun message trouvé : envoie d'abord un message à ton bot, puis réessaie.
          </p>
        ) : (
          <ul className="list" data-testid="resultat-detection">
            {convs.map((c) => (
              <li key={c.chat_id} className="row">
                <code>{c.chat_id}</code> <span>{c.nom}</span> <BoutonCopier texte={c.chat_id} />
              </li>
            ))}
          </ul>
        )
      ) : null}
      {convs && convs.length > 0 ? (
        <p className="small">
          Copie l'identifiant ci-dessus dans <code>TELEGRAM_CHAT_ID</code> sur le serveur : le site ne peut pas modifier cette variable lui-même.
        </p>
      ) : null}
      <Msg message={test.message} />
    </Card>
  );
}

// ------------------------------------------------------------------------------------------- (g) calendrier
const FUSEAUX = [
  { v: "Europe/Paris", l: "Heure de Paris" },
  { v: "America/New_York", l: "Heure de New York" },
  { v: "America/Chicago", l: "Heure de Chicago (CME)" },
  { v: "UTC", l: "UTC" },
];

function CalendrierSection() {
  const r = useRessource<Calendrier>("/api/calendar");
  const [titre, setTitre] = useState("");
  const [date, setDate] = useState("");
  const [heure, setHeure] = useState("");
  const [fuseau, setFuseau] = useState("Europe/Paris");
  const a = useAction();
  return (
    <Card titre="Calendrier économique" id="calendrier" testid="reglages-calendrier" sous="Les entrées sont bloquées autour des annonces à fort impact.">
      {r.chargement && !r.data ? <Chargement /> : null}
      {r.erreur ? <Erreur texte={r.erreur.message} /> : null}
      {r.data ? (
        <>
          <p className="small">
            {r.data.statut ? (
              <>
                <Badge ton={r.data.statut.ok ? "ok" : "warn"}>{r.data.statut.ok ? "Calendrier à jour" : "Mise à jour en échec"}</Badge> Source :{" "}
                {r.data.statut.source} — {dateHeure(r.data.statut.maj)}
              </>
            ) : (
              <Badge ton="warn">État de mise à jour inconnu (pas encore rafraîchi par le moteur)</Badge>
            )}
          </p>
          {r.data.evenements.length === 0 ? (
            <p className="muted">Aucune annonce à venir connue.</p>
          ) : (
            <ul className="list" data-testid="liste-evenements">
              {r.data.evenements.map((e, i) => (
                <li key={i}>
                  <div className="row">
                    <strong>{e.titre}</strong>
                    <Badge ton={e.impact === "fort" ? "warn" : "neutral"}>impact {e.impact}</Badge>
                  </div>
                  <div className="small muted">
                    {e.paris} · {e.new_york} ·{" "}
                    {/^https?:\/\//.test(e.source) ? (
                      <a href={e.source} target="_blank" rel="noopener noreferrer">
                        source
                      </a>
                    ) : (
                      e.source
                    )}
                  </div>
                </li>
              ))}
            </ul>
          )}
        </>
      ) : null}
      <h3 style={{ marginTop: 14 }}>Ajouter une annonce à fort impact</h3>
      <form
        data-testid="form-evenement"
        noValidate
        onSubmit={async (e) => {
          e.preventDefault();
          const quand = versIsoAvecFuseau(date, heure, fuseau);
          if (!quand) {
            a.setMessage({ ton: "bad", texte: "Indique une date et une heure valides." });
            return;
          }
          const ok = await a.lancer(() => api.post("/api/calendar", { titre: titre.trim(), quand }), `Annonce ajoutée (${quand}).`);
          if (ok) {
            setTitre("");
            await r.recharger();
          }
        }}
      >
        <div className="field">
          <label htmlFor="ev-titre">Titre</label>
          <input id="ev-titre" type="text" minLength={3} maxLength={200} value={titre} onChange={(e) => setTitre(e.target.value)} data-testid="champ-evenement-titre" />
        </div>
        <div className="form-grid">
          <div className="field">
            <label htmlFor="ev-date">Date</label>
            <input id="ev-date" type="date" value={date} onChange={(e) => setDate(e.target.value)} data-testid="champ-evenement-date" />
          </div>
          <div className="field">
            <label htmlFor="ev-heure">Heure</label>
            <input id="ev-heure" type="time" value={heure} onChange={(e) => setHeure(e.target.value)} data-testid="champ-evenement-heure" />
          </div>
          <div className="field">
            <label htmlFor="ev-fuseau">Fuseau horaire</label>
            <select id="ev-fuseau" value={fuseau} onChange={(e) => setFuseau(e.target.value)} data-testid="champ-evenement-fuseau">
              {FUSEAUX.map((f) => (
                <option key={f.v} value={f.v}>
                  {f.l}
                </option>
              ))}
            </select>
          </div>
        </div>
        <button type="submit" className="btn primary" disabled={a.enCours} data-testid="bouton-ajouter-evenement">
          Ajouter l'annonce
        </button>
        <Msg message={a.message} />
      </form>
      <p className="small muted">Nombre d'annonces affichées : {r.data ? nombre(r.data.evenements.length, 0) : "—"} (60 au maximum).</p>
    </Card>
  );
}
