import { describe, expect, it } from "vitest";
import { etiquettesSignal, indicateursSysteme, peutAnnuler, statutSignal } from "./status";
import { cheminInterne } from "./navigation";
import { etatReceptionTradingView } from "./tradingview";
import { estJoignable } from "./dashboard";
import { messageErreur, detailTexte } from "./api";
import type { Dashboard, Signal } from "./types";

function dash(over: Partial<Dashboard["statut"]> = {}): Dashboard {
  const statut: Dashboard["statut"] = {
    connexion: { ok: true, texte: "Serveur et moteur en ligne" },
    donnees: { ok: true, texte: "Données à jour", age_s: 20, source: "TradingView (webhook)" },
    moteur: { ok: true, etat: "actif", texte: "Surveille le marché", arret: null },
    notifications: { ok: true, active: true, configure: true, echecs_24h: 0, texte: "Opérationnelles", derniere: null },
    ...over,
  };
  return { maintenant: "", rejeu: null, statut, marche: {} as Dashboard["marche"], trading: {} as Dashboard["trading"], incidents: [] };
}

describe("jamais vert sans ok=true", () => {
  it("tout vert seulement si tout est ok", () => {
    const i = indicateursSysteme(dash(), true);
    expect([i.connexion.ton, i.donnees.ton, i.moteur.ton, i.notifications.ton, i.global.ton]).toEqual(["ok", "ok", "ok", "ok", "ok"]);
  });
  it("serveur injoignable : tout rouge, même si les dernières données étaient vertes", () => {
    const i = indicateursSysteme(dash(), false);
    expect([i.connexion.ton, i.donnees.ton, i.moteur.ton, i.notifications.ton, i.global.ton]).toEqual(["bad", "bad", "bad", "bad", "bad"]);
    expect(indicateursSysteme(null, true).connexion.ton).toBe("bad");
  });
  it("données en panne : aucun indicateur ne reste vert", () => {
    const i = indicateursSysteme(dash({ donnees: { ok: false, texte: "barres manquantes", age_s: 900, source: "x" } }), true);
    expect(i.donnees.ton).toBe("bad");
    expect(i.panneCritique).toBe(true);
    for (const t of [i.connexion, i.moteur, i.notifications, i.global]) expect(t.ton).not.toBe("ok");
    expect(i.connexion.texte).toContain("non garanti");
  });
  it("moteur en mode sécurisé / arrêté : panne critique", () => {
    for (const etat of ["securise", "arret", "arrete"]) {
      const i = indicateursSysteme(dash({ moteur: { ok: false, etat, texte: "x", arret: null } }), true);
      expect(i.moteur.ton).toBe("bad");
      expect(i.panneCritique).toBe(true);
      expect(i.donnees.ton).not.toBe("ok");
    }
  });
  it("pause : orange, sans panne critique", () => {
    const i = indicateursSysteme(dash({ moteur: { ok: false, etat: "pause", texte: "En pause", arret: null } }), true);
    expect(i.moteur.ton).toBe("warn");
    expect(i.panneCritique).toBe(false);
    expect(i.global.ton).toBe("warn");
  });
  it("notifications : non configurées / désactivées = orange, échecs = rouge", () => {
    const base = { ok: false, active: true, configure: true, echecs_24h: 0, texte: "", derniere: null };
    expect(indicateursSysteme(dash({ notifications: { ...base, configure: false } }), true).notifications.ton).toBe("warn");
    expect(indicateursSysteme(dash({ notifications: { ...base, active: false } }), true).notifications.ton).toBe("warn");
    expect(indicateursSysteme(dash({ notifications: { ...base, echecs_24h: 2 } }), true).notifications.ton).toBe("bad");
  });
  it("état de moteur inconnu : jamais vert", () => {
    expect(indicateursSysteme(dash({ moteur: { ok: false, etat: "bizarre", texte: "?", arret: null } }), true).moteur.ton).toBe("bad");
  });
});

describe("statuts des signaux (§11)", () => {
  const sig = (o: Partial<Signal>): Signal =>
    ({
      statut: "CLOTURE",
      simulation: { entree: null, entree_ts: null, stop_actuel: null, sortie: null, sortie_ts: null, raison: null, r: null, pnl_usd: null },
      execution_declaree: null,
      ...o,
    }) as Signal;
  it("vocabulaire exact", () => {
    expect(statutSignal("EN_ATTENTE").libelle).toBe("En attente de déclenchement");
    expect(statutSignal("ACTIF").libelle).toBe("Actif");
    expect(statutSignal("ANNULE").libelle).toBe("Annulé");
    expect(statutSignal("EXPIRE").libelle).toBe("Expiré");
    expect(statutSignal("CLOTURE").libelle).toBe("Clôturé");
    expect(statutSignal("XYZ").libelle).toContain("inconnu");
  });
  it("position simulée et exécution déclarée distinctes", () => {
    const s = sig({ simulation: { entree: 1, entree_ts: null, stop_actuel: 1, sortie: null, sortie_ts: null, raison: null, r: null, pnl_usd: null } });
    expect(etiquettesSignal(s).map((e) => e.libelle)).toEqual(["Clôturé", "Position simulée ouverte"]);
    const ex = sig({ execution_declaree: { executee: true, entree: 1, sortie: 2, contrats: 1, pnl_usd: 10, note: "" } });
    const lib = etiquettesSignal(ex).map((e) => e.libelle);
    expect(lib[1]).toContain("déclarée par toi");
    expect(lib[1]).toContain("non confirmée");
  });
  it("annulation autorisée seulement sans position simulée ouverte", () => {
    expect(peutAnnuler(sig({ statut: "EN_ATTENTE" }))).toBe(true);
    expect(peutAnnuler(sig({ statut: "CLOTURE" }))).toBe(false);
    expect(
      peutAnnuler(sig({ statut: "ACTIF", simulation: { entree: 1, entree_ts: null, stop_actuel: null, sortie: null, sortie_ts: null, raison: null, r: null, pnl_usd: null } })),
    ).toBe(false);
  });
});

describe("divers", () => {
  it("redirection après connexion : chemins internes uniquement", () => {
    expect(cheminInterne("/historique?statut=ACTIF")).toBe("/historique?statut=ACTIF");
    expect(cheminInterne("//evil.example")).toBe("/");
    expect(cheminInterne("/\\evil.example")).toBe("/");
    expect(cheminInterne("https://evil.example")).toBe("/");
    expect(cheminInterne(null)).toBe("/");
  });
  it("TradingView : « connecté » seulement si des webhooks récents sont reçus", () => {
    expect(etatReceptionTradingView("replay", 10, true, 5).ton).toBe("neutral");
    expect(etatReceptionTradingView("tradingview", 0, true, 5).ton).toBe("bad");
    expect(etatReceptionTradingView("tradingview", 3, false, 5).ton).toBe("warn");
    expect(etatReceptionTradingView("tradingview", 3, true, 900).ton).toBe("warn");
    expect(etatReceptionTradingView("tradingview", 3, null, null).ton).toBe("warn");
    expect(etatReceptionTradingView("tradingview", 3, true, 40).ton).toBe("ok");
  });
  it("serveur joignable seulement avec une réponse récente et sans erreur", () => {
    const t = 1_000_000;
    expect(estJoignable(null, t - 5_000, t)).toBe(true);
    expect(estJoignable(null, t - 31_000, t)).toBe(false);
    expect(estJoignable(0, t - 1_000, t)).toBe(false);
    expect(estJoignable(null, null, t)).toBe(false);
  });
  it("messages d'erreur en français", () => {
    expect(messageErreur(429, "trop de tentatives, réessaie dans 15 minutes")).toContain("réessaie dans 15 minutes");
    expect(messageErreur(409, "Refusé : stratégie non validée")).toBe("Refusé : stratégie non validée");
    expect(messageErreur(0)).toContain("Serveur injoignable");
    expect(detailTexte([{ loc: ["body", "solde"], type: "greater_than", ctx: { gt: 0 } }])).toBe("solde : doit être supérieur à 0");
  });
});
