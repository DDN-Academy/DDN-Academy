import { createContext, useContext, type ReactNode } from "react";
import { useMaintenant, useRessource, type Ressource } from "./hooks";
import type { Dashboard } from "./types";

/** Rafraîchissement du tableau de bord : toutes les 10 s (cahier des charges §14). */
export const INTERVALLE_MS = 10_000;
/** Au-delà de ce délai sans réponse réussie, les états affichés ne sont plus considérés comme fiables. */
export const PERIME_APRES_S = 30;

interface Ctx extends Ressource<Dashboard> {
  /** Le serveur a répondu récemment (dernière requête réussie et < 30 s). */
  joignable: boolean;
  /** Secondes depuis la dernière réponse réussie. */
  ageS: number | null;
  maintenant: number;
}

const DashboardCtx = createContext<Ctx | null>(null);

export function estJoignable(erreurStatus: number | null, recuA: number | null, maintenant: number): boolean {
  if (recuA === null) return false;
  if (erreurStatus !== null) return false;
  return (maintenant - recuA) / 1000 <= PERIME_APRES_S;
}

export function DashboardProvider({ children }: { children: ReactNode }) {
  const r = useRessource<Dashboard>("/api/dashboard", INTERVALLE_MS);
  const maintenant = useMaintenant();
  const ageS = r.recuA === null ? null : Math.max(0, (maintenant - r.recuA) / 1000);
  const joignable = estJoignable(r.erreur ? r.erreur.status : null, r.recuA, maintenant);
  return <DashboardCtx.Provider value={{ ...r, joignable, ageS, maintenant }}>{children}</DashboardCtx.Provider>;
}

export function useDashboard(): Ctx {
  const c = useContext(DashboardCtx);
  if (!c) throw new Error("DashboardProvider manquant");
  return c;
}
