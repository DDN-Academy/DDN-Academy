// Traduction des états du serveur en libellés et couleurs.
// Règle absolue (cahier des charges §14) : un indicateur n'est VERT que si l'API dit ok=true,
// que le serveur répond, et qu'aucun composant critique n'est en panne.

import type { Dashboard, Signal } from "./types";

export type Ton = "ok" | "warn" | "bad" | "neutral" | "info";

// ------------------------------------------------------------------------------------------- signaux
export const STATUTS_SIGNAL: Record<string, { libelle: string; ton: Ton; explication: string }> = {
  EN_ATTENTE: {
    libelle: "En attente de déclenchement",
    ton: "info",
    explication: "Le signal attend que le prix atteigne la zone d'entrée prévue.",
  },
  ACTIF: {
    libelle: "Actif",
    ton: "warn",
    explication:
      "Le signal est ouvert. On ne peut y entrer que si l'étiquette « Entrée exploitable maintenant » est affichée ; " +
      "sinon l'entrée est fermée et seule la position simulée est suivie jusqu'à sa sortie.",
  },
  ANNULE: { libelle: "Annulé", ton: "neutral", explication: "Le signal a été annulé : ne pas entrer." },
  EXPIRE: { libelle: "Expiré", ton: "neutral", explication: "La durée de validité est dépassée : ne pas entrer." },
  CLOTURE: { libelle: "Clôturé", ton: "neutral", explication: "La position simulée est sortie (stop, stop suiveur ou sortie temporelle)." },
};

export const FILTRES_STATUT: { valeur: string; libelle: string }[] = [
  { valeur: "", libelle: "Tous" },
  { valeur: "EN_ATTENTE", libelle: "En attente" },
  { valeur: "ACTIF", libelle: "Actifs" },
  { valeur: "ANNULE", libelle: "Annulés" },
  { valeur: "EXPIRE", libelle: "Expirés" },
  { valeur: "CLOTURE", libelle: "Clôturés" },
];

export function statutSignal(statut: string): { libelle: string; ton: Ton; explication: string } {
  return STATUTS_SIGNAL[statut] ?? { libelle: `Statut inconnu (${statut})`, ton: "neutral", explication: "" };
}

export function signalOuvert(sig: Signal): boolean {
  return sig.statut === "EN_ATTENTE" || sig.statut === "ACTIF";
}

/**
 * Fenêtre d'entrée d'un signal ouvert (cahier §11 : ne jamais présenter un ancien signal comme exploitable).
 * Le serveur fournit `entree_ouverte` ; s'il est absent (ancien serveur), on reste prudent : validité écoulée → fermée.
 */
export function etatEntree(sig: Signal, maintenant: Date = new Date()): { ouverte: boolean; raison: string } | null {
  if (!signalOuvert(sig)) return null;
  const validiteEcoulee = sig.validite ? new Date(sig.validite).getTime() <= maintenant.getTime() : false;
  const raisons: string[] = [];
  if (sig.plage_depassee) raisons.push("le prix est sorti de la plage d'entrée");
  if (sig.entree_interdite) raisons.push(sig.entree_interdite);
  if (validiteEcoulee) raisons.push(`la validité est écoulée (${sig.validite_ny})`);
  const ouverte = sig.entree_ouverte === undefined ? raisons.length === 0 : sig.entree_ouverte && !validiteEcoulee;
  if (ouverte) return { ouverte: true, raison: `Dans la plage d'entrée et la validité (jusqu'à ${sig.validite_ny}).` };
  return { ouverte: false, raison: raisons.length ? raisons.join(" ; ") : "la fenêtre d'entrée est fermée" };
}

export const RESULTAT_INCONNU = "Résultat inconnu (données manquantes)";

/** Signal clôturé sans résultat simulé (ex. « sortie temporelle (sans données) ») : aucun résultat n'est inventé. */
export function resultatInconnu(sig: Signal): boolean {
  return sig.statut === "CLOTURE" && (sig.simulation?.r ?? null) === null;
}

/** Étiquettes distinctes du cahier des charges §11 : statut du signal, fenêtre d'entrée, position simulée, exécution déclarée. */
export function etiquettesSignal(sig: Signal, maintenant: Date = new Date()): { cle: string; libelle: string; ton: Ton }[] {
  const out: { cle: string; libelle: string; ton: Ton }[] = [];
  const st = statutSignal(sig.statut);
  out.push({ cle: "statut", libelle: st.libelle, ton: st.ton });
  const entree = etatEntree(sig, maintenant);
  if (entree) {
    out.push(
      entree.ouverte
        ? { cle: "entree", libelle: "Entrée exploitable maintenant", ton: "warn" }
        : { cle: "entree", libelle: "Entrée fermée — ne plus entrer", ton: "bad" },
    );
  }
  const sim = sig.simulation;
  if (sim && sim.entree !== null && sim.entree !== undefined) {
    const close = sig.statut === "CLOTURE" || (sim.sortie !== null && sim.sortie !== undefined);
    out.push({ cle: "simulation", libelle: close ? "Position simulée clôturée" : "Position simulée ouverte", ton: "info" });
  }
  if (resultatInconnu(sig)) out.push({ cle: "resultat", libelle: RESULTAT_INCONNU, ton: "warn" });
  const ex = sig.execution_declaree;
  if (ex) {
    out.push({
      cle: "execution",
      // Cahier §11 : « réellement exécutée » seulement si une source fiable le confirme (aucune connexion courtier ici).
      libelle: ex.executee ? "Exécution déclarée par toi — non confirmée par le courtier" : "Non exécuté — déclaré par toi",
      ton: "neutral",
    });
  }
  return out;
}

export function modeLibelle(mode: string): string {
  return mode === "reel" ? "Réel" : mode === "simulation" ? "Simulation" : mode;
}

/** Un signal peut être annulé seulement s'il est en attente/actif ET qu'aucune position simulée n'est ouverte (règle du serveur). */
export function peutAnnuler(sig: Signal): boolean {
  return (sig.statut === "EN_ATTENTE" || sig.statut === "ACTIF") && (sig.simulation?.entree ?? null) === null;
}

// ------------------------------------------------------------------------------------------- système
export interface Indicateur {
  ton: Ton;
  titre: string;
  texte: string;
}

export interface Indicateurs {
  connexion: Indicateur;
  donnees: Indicateur;
  moteur: Indicateur;
  notifications: Indicateur;
  global: Indicateur;
  panneCritique: boolean;
}

const MOTEUR_TON: Record<string, Ton> = {
  actif: "ok",
  prechauffage: "warn",
  pause: "warn",
  demarrage: "warn",
  securise: "bad",
  arret: "bad",
  arrete: "bad",
};

const MOTEUR_TITRE: Record<string, string> = {
  actif: "Actif",
  prechauffage: "Préchauffage",
  pause: "En pause",
  demarrage: "Démarrage",
  securise: "Mode sécurisé",
  arret: "Arrêt de sécurité",
  arrete: "Arrêté",
};

/** Plafonne un ton : jamais vert si `vertAutorise` est faux. */
function plafonner(ton: Ton, vertAutorise: boolean): Ton {
  return ton === "ok" && !vertAutorise ? "warn" : ton;
}

/**
 * Calcule les quatre indicateurs de la page d'accueil.
 * @param d         dernier tableau de bord reçu (ou null)
 * @param joignable faux si la dernière requête a échoué ou si les données ont plus de 30 s
 */
export function indicateursSysteme(d: Dashboard | null, joignable: boolean): Indicateurs {
  if (!d || !joignable) {
    const inconnu = (titre: string): Indicateur => ({ ton: "bad", titre, texte: "Inconnu : le serveur ne répond pas" });
    return {
      connexion: { ton: "bad", titre: "Déconnecté", texte: "Serveur injoignable : aucun état fiable à afficher" },
      donnees: inconnu("Inconnu"),
      moteur: inconnu("Inconnu"),
      notifications: inconnu("Inconnu"),
      global: { ton: "bad", titre: "Serveur injoignable", texte: "Les états ci-dessous ne sont pas fiables tant que le serveur ne répond pas." },
      panneCritique: true,
    };
  }
  const s = d.statut;
  const etatMoteur = s.moteur.etat;
  const moteurEnPanne = !s.moteur.ok && ["securise", "arret", "arrete"].includes(etatMoteur);
  const panneCritique = !s.connexion.ok || !s.donnees.ok || moteurEnPanne;
  const vert = !panneCritique;

  const connexion: Indicateur = {
    ton: s.connexion.ok ? plafonner("ok", vert) : "bad",
    titre: s.connexion.ok ? "Connecté" : "Déconnecté",
    texte: s.connexion.texte,
  };
  const donnees: Indicateur = {
    ton: s.donnees.ok ? plafonner("ok", vert) : "bad",
    titre: s.donnees.ok ? "À jour" : "Indisponibles",
    texte: s.donnees.texte,
  };
  const tonMoteur = s.moteur.ok ? "ok" : MOTEUR_TON[etatMoteur] === "ok" ? "warn" : (MOTEUR_TON[etatMoteur] ?? "bad");
  const moteur: Indicateur = {
    ton: plafonner(tonMoteur, vert),
    titre: MOTEUR_TITRE[etatMoteur] ?? etatMoteur ?? "Inconnu",
    texte: s.moteur.texte + (s.moteur.arret?.raison ? ` — ${s.moteur.arret.raison}` : ""),
  };
  const n = s.notifications;
  let tonNotif: Ton;
  let titreNotif: string;
  if (n.ok) {
    tonNotif = "ok";
    titreNotif = "Opérationnelles";
  } else if (!n.configure) {
    tonNotif = "warn";
    titreNotif = "Non configurées";
  } else if (!n.active) {
    tonNotif = "warn";
    titreNotif = "Désactivées";
  } else if (n.verifiees === false) {
    tonNotif = "warn";
    titreNotif = "Jamais vérifiées";
  } else {
    tonNotif = "bad";
    titreNotif = "En erreur";
  }
  const notifications: Indicateur = { ton: plafonner(tonNotif, vert), titre: titreNotif, texte: n.texte };

  const tous = [connexion, donnees, moteur, notifications];
  let global: Indicateur;
  if (panneCritique) {
    global = {
      ton: "bad",
      titre: "Système en panne",
      texte: "Un composant critique ne fonctionne pas : aucun signal fiable ne peut être produit.",
    };
  } else if (tous.every((i) => i.ton === "ok")) {
    global = { ton: "ok", titre: "Système opérationnel", texte: "Tous les composants répondent normalement." };
  } else {
    global = { ton: "warn", titre: "Système partiellement opérationnel", texte: "Un ou plusieurs éléments demandent ton attention." };
  }
  if (!vert) {
    // Un élément que l'API déclare « ok » reste orange tant qu'un composant critique est en panne : on le dit.
    const okApi: [Indicateur, boolean][] = [[connexion, s.connexion.ok], [donnees, s.donnees.ok], [moteur, s.moteur.ok], [notifications, n.ok]];
    for (const [i, ok] of okApi) if (ok) i.texte += " (non garanti : un composant critique est en panne)";
  }
  return { connexion, donnees, moteur, notifications, global, panneCritique };
}

// ------------------------------------------------------------------------------------------- journal
export const NOTIF_STATUTS: Record<string, { libelle: string; ton: Ton }> = {
  a_envoyer: { libelle: "En file d'attente", ton: "info" },
  envoye: { libelle: "Envoyée", ton: "ok" },
  echec: { libelle: "Échec d'envoi", ton: "bad" },
  perime: { libelle: "Périmée (non envoyée)", ton: "warn" },
  desactive: { libelle: "Désactivée (non envoyée)", ton: "neutral" },
};

export function notifStatut(s: string): { libelle: string; ton: Ton } {
  return NOTIF_STATUTS[s] ?? { libelle: s, ton: "neutral" };
}

export const NOTIF_TYPES: Record<string, string> = {
  signal: "Nouveau signal",
  declenche: "Signal déclenché",
  plage: "Prix hors plage d'entrée",
  stop: "Stop déplacé",
  sortie: "Sortie de position",
  expire: "Signal expiré",
  annule: "Signal annulé",
  annonce: "Annonce économique",
  roll: "Changement de contrat (roll)",
  systeme: "Alerte système",
  test: "Test",
};

export const VERDICTS: Record<string, { libelle: string; ton: Ton }> = {
  concordant: { libelle: "Concordant", ton: "ok" },
  discordant: { libelle: "Discordant", ton: "bad" },
  decision_absente: { libelle: "Décision du moteur absente", ton: "warn" },
  "en attente": { libelle: "En attente de comparaison", ton: "neutral" },
  non_confirme_par_tradingview: { libelle: "Non confirmé par TradingView", ton: "warn" },
};

export function verdict(v: string): { libelle: string; ton: Ton } {
  return VERDICTS[v] ?? { libelle: v, ton: "neutral" };
}

export const EVENEMENTS_SIGNAL: Record<string, string> = {
  cree: "Signal créé",
  plage_depassee: "Prix sorti de la plage d'entrée",
  entree_interdite: "Entrée interdite (ne plus entrer)",
  entree_simulee: "Entrée simulée",
  sortie_simulee: "Sortie simulée",
  stop_deplace: "Stop suiveur déplacé",
  expire: "Signal expiré",
  annule: "Signal annulé",
  execution_declaree: "Exécution déclarée par toi",
  controle_croise: "Contrôle croisé TradingView",
};

export const GRAVITES: Record<string, { libelle: string; ton: Ton }> = {
  critique: { libelle: "Critique", ton: "bad" },
  alerte: { libelle: "Alerte", ton: "warn" },
  avertissement: { libelle: "Avertissement", ton: "warn" },
  info: { libelle: "Information", ton: "info" },
};

export function gravite(g: string): { libelle: string; ton: Ton } {
  return GRAVITES[g] ?? { libelle: g, ton: "warn" };
}

export const STATUT_REGLE: Record<string, Ton> = { "confirmée": "ok", contradictoire: "warn", inconnue: "bad" };
