// Mode DÉMONSTRATION (build `npm run build:demo`) : le site fonctionne sans serveur, à partir de réponses
// réelles de l'API enregistrées sur le jeu de données FICTIF des tests de bout en bout (e2e/seed.py).
// Aucune requête réseau, aucune action n'est envoyée ; un bandeau permanent le signale.
import fixtures from "../../demo/fixtures.json";
import { ApiError } from "./api";

export const DEMO = import.meta.env.VITE_DEMO === "1";

const F = fixtures as Record<string, unknown>;

function chercher(url: string): unknown {
  if (url in F) return F[url];
  const u = new URL(url, "http://demo.local");
  if (u.pathname === "/api/signals") {
    const statut = u.searchParams.get("statut");
    return F[`/api/signals?limit=50${statut ? `&statut=${statut}` : ""}`];
  }
  if (u.pathname === "/api/journal") return F[`/api/journal?type=${u.searchParams.get("type")}&limit=100`];
  return undefined;
}

export async function demoRequest<T>(method: string, url: string): Promise<T> {
  await new Promise((r) => setTimeout(r, 120)); // laisse apparaître les états de chargement
  if (method === "GET") {
    const v = chercher(url);
    if (v === undefined) throw new ApiError(404, "Démonstration : cette donnée n'existe pas dans le jeu d'exemple.");
    return v as T;
  }
  if (url === "/api/auth/login" || url === "/api/auth/logout") return { ok: true } as T;
  throw new ApiError(
    409,
    "Démonstration : aucune action n'est envoyée (pas de serveur). Sur ton site installé, ce bouton agit réellement.",
  );
}
