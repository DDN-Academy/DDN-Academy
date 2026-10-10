import { useCallback, useEffect, useRef, useState } from "react";
import { api, ApiError } from "./api";

export interface Ressource<T> {
  data: T | null;
  erreur: ApiError | null;
  chargement: boolean;
  /** Horodatage (ms) de la dernière réponse réussie. */
  recuA: number | null;
  recharger: () => Promise<void>;
}

/**
 * Charge une ressource GET ; si `intervalleMs` est donné, la recharge périodiquement
 * (seulement quand la page est visible). En cas d'échec, `data` garde la dernière valeur
 * mais `erreur` est renseignée : à l'appelant de ne PAS présenter ces données comme actuelles.
 */
export function useRessource<T>(url: string | null, intervalleMs?: number): Ressource<T> {
  const [data, setData] = useState<T | null>(null);
  const [erreur, setErreur] = useState<ApiError | null>(null);
  const [chargement, setChargement] = useState<boolean>(url !== null);
  const [recuA, setRecuA] = useState<number | null>(null);
  const urlRef = useRef(url);
  urlRef.current = url;

  const recharger = useCallback(async () => {
    const u = urlRef.current;
    if (!u) return;
    try {
      const r = await api.get<T>(u);
      if (urlRef.current !== u) return;
      setData(r);
      setErreur(null);
      setRecuA(Date.now());
    } catch (e) {
      if (urlRef.current !== u) return;
      setErreur(e instanceof ApiError ? e : new ApiError(0, "Erreur inattendue."));
    } finally {
      if (urlRef.current === u) setChargement(false);
    }
  }, []);

  useEffect(() => {
    setChargement(url !== null);
    setData(null);
    setErreur(null);
    if (!url) return;
    void recharger();
    if (!intervalleMs) return;
    const id = window.setInterval(() => {
      if (document.visibilityState === "visible") void recharger();
    }, intervalleMs);
    const surVisible = () => {
      if (document.visibilityState === "visible") void recharger();
    };
    document.addEventListener("visibilitychange", surVisible);
    return () => {
      window.clearInterval(id);
      document.removeEventListener("visibilitychange", surVisible);
    };
  }, [url, intervalleMs, recharger]);

  return { data, erreur, chargement, recuA, recharger };
}

/** Horloge locale qui avance chaque seconde (pour « mis à jour il y a N s »). */
export function useMaintenant(pasMs = 1000): number {
  const [t, setT] = useState(() => Date.now());
  useEffect(() => {
    const id = window.setInterval(() => setT(Date.now()), pasMs);
    return () => window.clearInterval(id);
  }, [pasMs]);
  return t;
}

/** Exécute une action d'écriture et mémorise le message de succès ou d'erreur à afficher. */
export function useAction() {
  const [enCours, setEnCours] = useState(false);
  const [message, setMessage] = useState<{ ton: "ok" | "bad"; texte: string } | null>(null);
  const lancer = useCallback(async (fn: () => Promise<unknown>, succes: string): Promise<boolean> => {
    setEnCours(true);
    setMessage(null);
    try {
      await fn();
      setMessage({ ton: "ok", texte: succes });
      return true;
    } catch (e) {
      setMessage({ ton: "bad", texte: e instanceof ApiError ? e.message : "Erreur inattendue." });
      return false;
    } finally {
      setEnCours(false);
    }
  }, []);
  return { enCours, message, setMessage, lancer };
}

export function useTitre(titre: string) {
  useEffect(() => {
    document.title = `${titre} — GoldPilot`;
  }, [titre]);
}
