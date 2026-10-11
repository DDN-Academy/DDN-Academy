import { describe, expect, it } from "vitest";
import { RESULTAT_INCONNU, etatEntree, etiquettesSignal, indicateursSysteme, resultatInconnu, statutSignal } from "./status";
import { detailTexte, messageErreur } from "./api";
import type { Dashboard, Signal } from "./types";

const SIM = { entree: null, entree_ts: null, stop_actuel: null, sortie: null, sortie_ts: null, raison: null, r: null, pnl_usd: null };
const MAINTENANT = new Date("2026-10-09T13:20:00Z");
const sig = (o: Partial<Signal>): Signal =>
  ({ statut: "ACTIF", validite: "2026-10-09T13:30:00Z", validite_ny: "09:30 New York", simulation: SIM, execution_declaree: null, ...o }) as Signal;

describe("fenêtre d'entrée (§11 : jamais un ancien signal présenté comme exploitable)", () => {
  it("ouverte seulement si le serveur le dit et que la validité n'est pas écoulée", () => {
    expect(etatEntree(sig({ entree_ouverte: true }), MAINTENANT)?.ouverte).toBe(true);
    expect(etiquettesSignal(sig({ entree_ouverte: true }), MAINTENANT).map((e) => e.libelle)).toContain("Entrée exploitable maintenant");
  });
  it("fermée : prix hors plage, entrée interdite ou validité écoulée", () => {
    const hors = etatEntree(sig({ entree_ouverte: false, plage_depassee: true }), MAINTENANT);
    expect(hors?.ouverte).toBe(false);
    expect(hors?.raison).toContain("plage");
    expect(etatEntree(sig({ entree_ouverte: false, entree_interdite: "Mode sécurisé" }), MAINTENANT)?.raison).toContain("Mode sécurisé");
    // le serveur disait « ouverte » il y a quelques secondes, mais la validité vient d'expirer côté navigateur
    const tard = new Date("2026-10-09T13:31:00Z");
    expect(etatEntree(sig({ entree_ouverte: true }), tard)?.ouverte).toBe(false);
    const lib = etiquettesSignal(sig({ entree_ouverte: false, plage_depassee: true }), MAINTENANT);
    expect(lib.find((e) => e.cle === "entree")).toEqual({ cle: "entree", libelle: "Entrée fermée — ne plus entrer", ton: "bad" });
  });
  it("ancien serveur sans le champ : prudence sur la validité", () => {
    expect(etatEntree(sig({}), new Date("2026-10-09T14:00:00Z"))?.ouverte).toBe(false);
  });
  it("signal terminé : pas d'étiquette d'entrée", () => {
    expect(etatEntree(sig({ statut: "CLOTURE" }), MAINTENANT)).toBeNull();
    expect(etiquettesSignal(sig({ statut: "EXPIRE" }), MAINTENANT).some((e) => e.cle === "entree")).toBe(false);
  });
  it("le libellé « Actif » ne promet plus « exploitable maintenant »", () => {
    expect(statutSignal("ACTIF").explication).not.toContain("exploitable maintenant (");
  });
  it("exécution déclarée : jamais « réellement exécutée »", () => {
    const l = etiquettesSignal(sig({ statut: "CLOTURE", execution_declaree: { executee: true, entree: 1, sortie: 2, contrats: 1, pnl_usd: 1, note: "" } }));
    const ex = l.find((e) => e.cle === "execution")!.libelle;
    expect(ex).toBe("Exécution déclarée par toi — non confirmée par le courtier");
    expect(ex).not.toContain("réellement");
  });
});

describe("notifications : jamais vertes sans envoi réussi", () => {
  const d = (n: Partial<Dashboard["statut"]["notifications"]>): Dashboard =>
    ({
      maintenant: "",
      rejeu: null,
      statut: {
        connexion: { ok: true, texte: "" },
        donnees: { ok: true, texte: "", age_s: 1, source: "" },
        moteur: { ok: true, etat: "actif", texte: "", arret: null },
        notifications: { ok: false, active: true, configure: true, echecs_24h: 0, texte: "", derniere: null, ...n },
      },
      marche: {},
      trading: {},
      incidents: [],
    }) as unknown as Dashboard;
  it("jamais vérifiées = orange", () => {
    const i = indicateursSysteme(d({ verifiees: false, texte: "Jamais vérifiées" }), true).notifications;
    expect(i.ton).toBe("warn");
    expect(i.titre).toBe("Jamais vérifiées");
  });
  it("dernier envoi en échec = rouge, même sans échec sur 24 h", () => {
    const i = indicateursSysteme(d({ verifiees: true, echecs_24h: 0, texte: "Dernier envoi en échec" }), true).notifications;
    expect(i.ton).toBe("bad");
  });
});

describe("messages d'erreur : jamais « Erreur du serveur (400) » ni de texte anglais", () => {
  it("400 = action refusée", () => {
    expect(messageErreur(400, "signal non annulable")).toBe("Action refusée : signal non annulable");
    expect(messageErreur(400)).not.toContain("Erreur du serveur");
  });
  it("traductions Pydantic", () => {
    expect(detailTexte([{ loc: ["body", "contrats"], type: "int_from_float", msg: "Input should be a valid integer, got a number with a fractional part" }])).toBe(
      "contrats : nombre entier attendu",
    );
    expect(detailTexte([{ loc: ["body", "executee"], type: "bool_parsing", msg: "Input should be a valid boolean" }])).toBe("executee : oui ou non attendu");
    expect(detailTexte([{ loc: ["body"], type: "json_invalid", msg: "JSON decode error" }])).toBe("body : données mal formées");
    expect(detailTexte([{ loc: ["body", "x"], type: "type_inconnu", msg: "Some English message" }])).not.toContain("English");
  });
});

describe("clôture sans données : résultat inconnu", () => {
  const clos = sig({ statut: "CLOTURE", simulation: { ...SIM, entree: 4000, sortie: null, r: null, pnl_usd: null } });
  it("étiquette « Résultat inconnu (données manquantes) » et position simulée clôturée (pas « ouverte »)", () => {
    const l = etiquettesSignal(clos).map((e) => e.libelle);
    expect(resultatInconnu(clos)).toBe(true);
    expect(l).toContain(RESULTAT_INCONNU);
    expect(l).toContain("Position simulée clôturée");
    expect(l).not.toContain("Position simulée ouverte");
  });
  it("un signal clôturé avec un résultat n'est pas marqué inconnu", () => {
    const ok = sig({ statut: "CLOTURE", simulation: { ...SIM, entree: 4000, sortie: 4010, r: 1.2, pnl_usd: 280 } });
    expect(resultatInconnu(ok)).toBe(false);
    expect(etiquettesSignal(ok).map((e) => e.libelle)).not.toContain(RESULTAT_INCONNU);
  });
});
