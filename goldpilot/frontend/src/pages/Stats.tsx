import { useState } from "react";
import { Link } from "react-router-dom";
import { useRessource, useTitre } from "../lib/hooks";
import { useDashboard } from "../lib/dashboard";
import type { ContexteMacro, LigneMC, LigneParGroupe, Metriques, Stats as StatsT } from "../lib/types";
import { dateCourte, dateHeure, duree, enR, entier, nombre, pct, usd, signe, estNombre } from "../lib/format";
import { verdict } from "../lib/status";
import { Badge, Banner, Card, Chargement, Erreur, classeSigne } from "../components/ui";
import { EquityChart } from "../components/EquityChart";

export function Stats() {
  useTitre("Statistiques");
  const r = useRessource<StatsT>("/api/stats");
  const dash = useDashboard();
  if (r.chargement && !r.data) return <Chargement />;
  if (r.erreur && !r.data) return <Erreur texte={r.erreur.message} />;
  if (!r.data) return null;
  const s = r.data;
  const prod = s.production;
  return (
    <>
      <div className="page-head">
        <h1>Statistiques</h1>
      </div>
      <nav className="toc" aria-label="Sections de la page">
        <a href="#verdict">Verdict</a>
        <a href="#paper">Suivi papier</a>
        <a href="#execution">Exécution</a>
        <a href="#selection">Sélection</a>
        <a href="#test-final">Test final</a>
        <a href="#montecarlo">Monte-Carlo</a>
        <a href="#macro">Contexte macro</a>
      </nav>

      <section id="verdict" data-testid="verdict-strategie">
        {prod ? (
          <Banner ton={prod.validated ? "ok" : "bad"} titre={prod.validated ? "Stratégie VALIDÉE" : "Stratégie NON VALIDÉE"}>
            <p>{prod.verdict}</p>
            <p className="small" style={{ marginTop: 6 }}>
              Version : {prod.version ?? "—"}
              {estNombre(prod.trades_par_mois_attendus) ? ` · fréquence attendue ≈ ${nombre(prod.trades_par_mois_attendus, 1)} trades par mois` : ""}
            </p>
          </Banner>
        ) : (
          <Banner ton="bad" titre="Aucune stratégie configurée">
            <p>Le fichier de configuration de production est absent : aucun signal ne peut être émis.</p>
          </Banner>
        )}
        <p className="small muted">
          Ce que signifient ces chiffres : « R » = le risque d'un trade (1 R = la perte si le stop initial est touché). Une espérance de +0,08 R
          signifie un gain moyen de 8 % du risque par trade, avant incertitude. L'intervalle « IC95 » donne la plage plausible : s'il contient 0,
          rien ne prouve que la stratégie gagne.
        </p>
      </section>

      <Paper s={s} rejeu={!!dash.data?.rejeu} />
      <Execution s={s} />
      <Selection s={s} />
      <TestFinal s={s} />
      <MonteCarlo s={s} />
      <Macro ctx={dash.data?.marche.contexte_macro} charge={!!dash.data} />
    </>
  );
}

function Tile({ k, v, s, testid }: { k: string; v: string; s?: string; testid?: string }) {
  return (
    <div className="tile" data-testid={testid}>
      <div className="k">{k}</div>
      <div className="v">{v}</div>
      {s ? <div className="s">{s}</div> : null}
    </div>
  );
}

function Paper({ s, rejeu }: { s: StatsT; rejeu: boolean }) {
  const p = s.paper;
  return (
    <Card titre="Suivi papier (signaux simulés clôturés)" id="paper" testid="stats-paper">
      {rejeu ? (
        <p className="small">
          <Badge ton="info">Rejeu historique</Badge> Ces résultats proviennent du rejeu de données passées, pas du marché en temps réel.
        </p>
      ) : null}
      {!p ? (
        <p className="muted">Aucun signal clôturé : pas encore de résultat de suivi papier. Il faudra de nombreux trades avant de pouvoir conclure.</p>
      ) : (
        <>
          <div className="tiles">
            <Tile k="Trades clôturés" v={entier(p.n)} testid="paper-n" />
            <Tile k="Espérance par trade" v={enR(p.esperance_R)} />
            <Tile k="Taux de gain" v={pct(p.taux_de_gain)} />
            <Tile k="Drawdown maximal" v={enR(p.drawdown_max_R)} />
            <Tile k="Total" v={enR(p.total_R)} s={usd(p.pnl_usd, 0, true)} />
          </div>
          {p.n < 30 ? (
            <p className="small muted">
              Avec seulement {p.n} trade(s), ces chiffres ne permettent aucune conclusion statistique (l'incertitude est plus grande que l'effet
              recherché).
            </p>
          ) : null}
          <EquityChart points={p.courbe} titre="Résultat cumulé en R" />
        </>
      )}
    </Card>
  );
}

function Execution({ s }: { s: StatsT }) {
  const e = s.execution;
  const cc = Object.entries(e.controle_croise ?? {});
  return (
    <Card titre="Qualité d'exécution" id="execution" testid="stats-execution" sous={`Calculée sur les ${e.signaux} derniers signaux.`}>
      <div className="tiles">
        <Tile k="Délai moteur (médian)" v={e.delai_moteur_median_s !== null ? duree(e.delai_moteur_median_s) : "—"} s="clôture de la barre → signal" />
        <Tile k="Délai d'alerte (médian)" v={e.delai_alerte_median_s !== null ? duree(e.delai_alerte_median_s) : "—"} s={e.delai_alerte_max_s !== null ? `maximum ${duree(e.delai_alerte_max_s)}` : "aucune alerte envoyée"} />
        <Tile
          k="Écart d'entrée simulé (médian)"
          v={e.ecart_entree_simulee_median_atr !== null ? `${signe(e.ecart_entree_simulee_median_atr, 3)} ATR` : "—"}
          s="positif = entrée moins favorable que prévu"
        />
      </div>
      <h3>Contrôle croisé TradingView</h3>
      {cc.length === 0 ? (
        <p className="muted small">Aucun signal miroir reçu de TradingView : contrôle croisé non disponible.</p>
      ) : (
        <div className="row">
          {cc.map(([v, n]) => (
            <Badge key={v} ton={verdict(v).ton}>
              {verdict(v).libelle} : {n}
            </Badge>
          ))}
        </div>
      )}
    </Card>
  );
}

const CRITERES: Record<string, string> = {
  "1_walk_forward_esperance_et_IC_unilateral_bas_>0": "Walk-forward : espérance et borne basse de l'IC unilatéral > 0",
  "2_validation_esperance_>0_et_PF_>=1.10": "Validation : espérance > 0 et profit factor ≥ 1,10",
  "3_couts_x2_validation_>=0": "Validation avec coûts doublés : espérance ≥ 0",
  "4_annees_positives_>=60%": "Années positives ≥ 60 %",
  "5_voisins_positifs_>=70%": "Paramètres voisins positifs ≥ 70 %",
  "6_DSR_200_essais_>=0.90": "Sharpe dégonflé (200 essais) ≥ 0,90",
};

function ic(m?: Metriques): string {
  if (!m || !estNombre(m.ic95_bas) || !estNombre(m.ic95_haut)) return "";
  return `IC95 ${signe(m.ic95_bas, 3)} ; ${signe(m.ic95_haut, 3)}`;
}

function Selection({ s }: { s: StatsT }) {
  const sel = s.selection;
  if (!sel?.familles) {
    return (
      <Card titre="Sélection (backtest 2011-2021)" id="selection">
        <p className="muted">Résultats de sélection indisponibles sur ce serveur.</p>
      </Card>
    );
  }
  return (
    <Card
      titre="Sélection (backtest 2011-2021)"
      id="selection"
      testid="stats-selection"
      sous={`Critères fixés avant les tests. ${sel.essais_cette_session ?? "?"} configurations testées dans cette session, ${sel.essais_comptes_pour_DSR ?? "?"} essais comptés pour la correction des tests multiples.${sel.genere_utc ? ` Généré le ${dateHeure(sel.genere_utc)}.` : ""}`}
    >
      {Object.entries(sel.familles).map(([nom, f]) => {
        const wf = f.walk_forward?.resume;
        return (
          <div key={nom} style={{ marginBottom: 16 }}>
            <h3 className="row">
              Famille {nom} <Badge ton={f.eligible ? "ok" : "bad"}>{f.eligible ? "éligible" : "non éligible"}</Badge>
            </h3>
            <div className="tiles">
              <Tile k="Walk-forward : espérance" v={enR(wf?.esperance_R, 3)} s={ic(wf)} />
              <Tile k="Walk-forward : trades" v={entier(wf?.n)} s={wf ? `profit factor ${nombre(wf.profit_factor, 2)}` : undefined} />
              <Tile k="Validation : espérance" v={enR(f.validation?.esperance_R, 3)} s={ic(f.validation)} />
              <Tile k="Validation, coûts ×2" v={enR(f.validation_couts_x2_esperance_R, 3)} />
            </div>
            {f.criteres ? (
              <div className="table-wrap">
                <table>
                  <caption>Critères de validation pré-enregistrés</caption>
                  <thead>
                    <tr>
                      <th>Critère</th>
                      <th>Résultat</th>
                    </tr>
                  </thead>
                  <tbody>
                    {Object.entries(f.criteres).map(([k, ok]) => (
                      <tr key={k}>
                        <td>{CRITERES[k] ?? k.replace(/_/g, " ")}</td>
                        <td>
                          <Badge ton={ok ? "ok" : "bad"}>{ok ? "satisfait" : "non satisfait"}</Badge>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : null}
          </div>
        );
      })}
      <p className="small muted">Rapport complet : research/output/selection/selection.md</p>
    </Card>
  );
}

function TableMetriques({ lignes, caption }: { lignes: [string, Metriques | undefined][]; caption: string }) {
  const ls = lignes.filter((l): l is [string, Metriques] => !!l[1]);
  if (ls.length === 0) return null;
  return (
    <div className="table-wrap">
      <table data-testid="table-scenarios">
        <caption>{caption}</caption>
        <thead>
          <tr>
            <th>Scénario</th>
            <th className="n">Trades</th>
            <th className="n">Gain %</th>
            <th className="n">Espérance</th>
            <th className="n">IC95</th>
            <th className="n">Profit factor</th>
            <th className="n">Total</th>
            <th className="n">Drawdown max</th>
            <th className="n">Pertes d'affilée max</th>
          </tr>
        </thead>
        <tbody>
          {ls.map(([nom, m]) => (
            <tr key={nom}>
              <td>{nom}</td>
              <td className="n">{entier(m.n)}</td>
              <td className="n">{pct(m.taux_de_gain)}</td>
              <td className={`n ${classeSigne(m.esperance_R)}`}>{enR(m.esperance_R, 3)}</td>
              <td className="n">{estNombre(m.ic95_bas) && estNombre(m.ic95_haut) ? `${signe(m.ic95_bas, 3)} ; ${signe(m.ic95_haut, 3)}` : "non calculé"}</td>
              <td className="n">{nombre(m.profit_factor, 2)}</td>
              <td className="n">{enR(m.total_R, 1)}</td>
              <td className="n">{enR(m.drawdown_max_R, 1)}</td>
              <td className="n">{entier(m.serie_pertes_max)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function TableGroupes({ lignes, titre, cle }: { lignes?: LigneParGroupe[]; titre: string; cle: (l: LigneParGroupe) => string }) {
  if (!lignes?.length) return null;
  return (
    <div className="table-wrap">
      <table>
        <caption>{titre}</caption>
        <thead>
          <tr>
            <th></th>
            <th className="n">Trades</th>
            <th className="n">Gain %</th>
            <th className="n">Espérance</th>
            <th className="n">Total</th>
          </tr>
        </thead>
        <tbody>
          {lignes.map((l, i) => (
            <tr key={i}>
              <td>{cle(l)}</td>
              <td className="n">{entier(l.n)}</td>
              <td className="n">{pct(l.taux_de_gain)}</td>
              <td className={`n ${classeSigne(l.esperance_R)}`}>{enR(l.esperance_R, 3)}</td>
              <td className={`n ${classeSigne(l.total_R)}`}>{enR(l.total_R, 1)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function TestFinal({ s }: { s: StatsT }) {
  const t = s.test_final;
  if (!t) {
    return (
      <Card titre="Test final (2022-2025)" id="test-final">
        <p className="muted">Résultats du test final indisponibles sur ce serveur.</p>
      </Card>
    );
  }
  const c25 = t.controle_resolution_2025;
  return (
    <Card titre="Test final 2022-2025" id="test-final" testid="stats-test-final" sous={`Candidat ${t.candidat ?? "?"} — statut : ${t.statut ?? "?"}.`}>
      <p className="small">
        Ce test est <strong>exploratoire</strong> : aucune famille n'ayant satisfait les critères, il ne peut pas confirmer la stratégie. Il
        sert à mesurer la dégradation hors échantillon et la sensibilité aux coûts.
      </p>
      <TableMetriques
        caption="Résultats par scénario de coûts"
        lignes={[
          ["Walk-forward 2011-2021 (référence)", t.walk_forward_S1],
          ["2022-2025, coûts de base", t.exploratoire_base],
          ["2022-2025, coûts doublés", t.exploratoire_couts_x2],
          ["2022-2025, coûts fixes", t.exploratoire_couts_fixes],
          ["2025, barres 15 min", c25?.barres_15min],
          ["2025, exécution 5 min", c25?.execution_5min],
        ]}
      />
      {c25?.periode ? <p className="small muted">Contrôle de résolution 2025 : {c25.periode}.</p> : null}
      <TableGroupes lignes={t.exploratoire_par_annee} titre="Par année (coûts de base)" cle={(l) => String(l.year ?? "?")} />
      <TableGroupes lignes={t.exploratoire_par_seance} titre="Par séance (coûts de base)" cle={(l) => l.index ?? "?"} />
      <TableGroupes lignes={t.exploratoire_par_sens} titre="Par sens (coûts de base)" cle={(l) => l.side ?? "?"} />
      <p className="small muted">Rapport complet : research/output/final/final.md</p>
    </Card>
  );
}

const SCENARIOS_MC: { cle: "challenge_wf" | "challenge_2022_2025" | "challenge_wf_prix_4500"; libelle: string }[] = [
  { cle: "challenge_wf", libelle: "Trades walk-forward 2011-2021" },
  { cle: "challenge_2022_2025", libelle: "Trades 2022-2025" },
  { cle: "challenge_wf_prix_4500", libelle: "Walk-forward, or à 4 500 $" },
];

function MonteCarlo({ s }: { s: StatsT }) {
  const mc = s.monte_carlo;
  const [sc, setSc] = useState<(typeof SCENARIOS_MC)[number]["cle"]>("challenge_wf");
  if (!mc) {
    return (
      <Card titre="Monte-Carlo du challenge" id="montecarlo">
        <p className="muted">Simulations Monte-Carlo indisponibles sur ce serveur.</p>
      </Card>
    );
  }
  const lignes: LigneMC[] = mc[sc] ?? [];
  const h = lignes[0]?.horizon_jours;
  return (
    <Card
      titre="Monte-Carlo du challenge FundedNext"
      id="montecarlo"
      testid="stats-montecarlo"
      sous={`Tirages aléatoires des trades passés pour estimer la probabilité de réussir ou de violer le challenge${h ? ` en ${h} jours de trading` : ""}.`}
    >
      <div className="chips" role="group" aria-label="Jeu de trades utilisé">
        {SCENARIOS_MC.filter((x) => mc[x.cle]?.length).map((x) => (
          <button key={x.cle} type="button" className="chip" aria-pressed={sc === x.cle} onClick={() => setSc(x.cle)}>
            {x.libelle}
          </button>
        ))}
      </div>
      <div className="table-wrap">
        <table data-testid="table-montecarlo">
          <caption>Probabilités par niveau de risque par trade</caption>
          <thead>
            <tr>
              <th className="n">Risque / trade</th>
              <th className="n">P(réussite)</th>
              <th className="n">P(violation)</th>
              <th className="n">P(toujours en cours)</th>
              <th className="n">Jours médians si réussite</th>
              <th className="n">Profit médian</th>
              <th className="n">Profit 5 % pire</th>
            </tr>
          </thead>
          <tbody>
            {lignes.map((l) => (
              <tr key={l.risk_per_trade_usd} style={mc.profil_retenu?.risque_par_trade_usd === l.risk_per_trade_usd ? { fontWeight: 700 } : undefined}>
                <td className="n">
                  {usd(l.risk_per_trade_usd)}
                  {mc.profil_retenu?.risque_par_trade_usd === l.risk_per_trade_usd ? " (retenu)" : ""}
                </td>
                <td className="n">{pct(l.p_reussite, 2)}</td>
                <td className="n">{pct(l.p_violation, 2)}</td>
                <td className="n">{pct(l.p_en_cours, 1)}</td>
                <td className="n">{l.jours_median_reussite !== null ? entier(l.jours_median_reussite) : "—"}</td>
                <td className={`n ${classeSigne(l.profit_median)}`}>{usd(l.profit_median, 0, true)}</td>
                <td className={`n ${classeSigne(l.profit_p05)}`}>{usd(l.profit_p05, 0, true)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="small muted">
        {lignes[0] ? `${entier(lignes[0].trajectoires)} trajectoires par niveau. ` : ""}
        Les probabilités sont des estimations sous l'hypothèse que les trades futurs ressemblent aux trades passés ; elles ne garantissent rien.
      </p>
      {mc.profil_retenu ? (
        <p className="small">
          <strong>Profil retenu :</strong> {usd(mc.profil_retenu.risque_par_trade_usd)} par trade — règle : {mc.profil_retenu.regle}
          {mc.profil_retenu.contrainte_respectee ? " (contrainte respectée)" : " (contrainte NON respectée)"}.
        </p>
      ) : null}
      {mc.finance_wf ? (
        <p className="small">
          <strong>Compte financé (simulation sur {mc.finance_wf.horizon_jours} jours) :</strong> profit médian {usd(mc.finance_wf.profit_median, 0, true)}, 5 % pire{" "}
          {usd(mc.finance_wf.profit_p05, 0, true)}, P(violation) {pct(mc.finance_wf.p_violation, 2)}
          {mc.finance_wf.retraits?.p_au_moins_un !== undefined ? `, P(au moins un retrait) ${pct(mc.finance_wf.retraits.p_au_moins_un)}` : ""}.
        </p>
      ) : null}
      {mc.suspension ? (
        <p className="small">
          <strong>Seuils d'arrêt automatique</strong> (sur {mc.suspension.n_trades} trades simulés) : drawdown 1 % pire {enR(mc.suspension.dd_p01, 1)}, série de
          pertes 99 % {entier(mc.suspension.serie_pertes_p99)}. Au-delà, le moteur s'arrête et attend ta reprise manuelle.
        </p>
      ) : null}
    </Card>
  );
}

/** Décimales publiées par FRED : 4 pour l'indice dollar DTWEXBGS, 2 pour les taux. */
export function decimalesMacro(id: string): number {
  return id === "DTWEXBGS" ? 4 : 2;
}

function Macro({ ctx, charge }: { ctx: ContexteMacro | undefined; charge: boolean }) {
  return (
    <Card titre="Contexte macro" id="macro" testid="contexte-macro">
      <p className="small">
        <Badge ton="info" wrap>
          {ctx?.note ?? "Information de contexte uniquement : non utilisée par la stratégie ni par le moteur de risque."}
        </Badge>
      </p>
      {!charge ? (
        <p className="muted">Chargement du tableau de bord…</p>
      ) : !ctx ? (
        <p className="muted" data-testid="macro-indisponible">
          Contexte macro non fourni par ce serveur.
        </p>
      ) : !ctx.disponible ? (
        <p data-testid="macro-indisponible">
          <Badge ton="warn">Indisponible</Badge> {ctx.probleme ?? "Source injoignable ou non configurée."}
          {ctx.maj ? <span className="small muted"> Dernière mise à jour réussie : {dateHeure(ctx.maj)}.</span> : null}
        </p>
      ) : ctx.probleme ? (
        <p data-testid="macro-probleme">
          <Badge ton="warn">Partiel</Badge> {ctx.probleme}
        </p>
      ) : null}
      {ctx && ctx.series?.length ? (
        <>
          <p className="small muted" style={{ marginBottom: 4 }}>
            Source : {ctx.source}
            {ctx.maj ? ` — mis à jour le ${dateHeure(ctx.maj)} (heure de Paris)` : ""}
            {!ctx.disponible ? " — valeurs possiblement anciennes" : ""}
          </p>
          <ul className="list" data-testid="table-macro">
            {ctx.series.map((x) => (
              <li key={x.id}>
                <div>
                  <a href={x.url} target="_blank" rel="noopener noreferrer">
                    {x.nom}
                  </a>{" "}
                  <span className="small muted">({x.id})</span>
                </div>
                <div>
                  <strong className="num">{estNombre(x.valeur) ? nombre(x.valeur, decimalesMacro(x.id)) : "—"}</strong>{" "}
                  <span className="small">{x.unite}</span>
                </div>
                <div className="small muted">
                  Valeur du {dateCourte(x.date)} · variation sur 5 jours ouvrés :{" "}
                  {estNombre(x.variation_5j) ? `${signe(x.variation_5j, decimalesMacro(x.id))} ${x.unite === "%" ? "point(s) de %" : "point(s) d'indice"}` : "non calculée"}
                </div>
              </li>
            ))}
          </ul>
        </>
      ) : null}
      <p className="small muted" style={{ marginTop: 8, marginBottom: 0 }}>
        Ces séries aident à comprendre l'environnement de l'or (taux réels, dollar…). Elles ne déclenchent aucun signal. Voir aussi{" "}
        <Link to="/aide">l'aide</Link>.
      </p>
    </Card>
  );
}
