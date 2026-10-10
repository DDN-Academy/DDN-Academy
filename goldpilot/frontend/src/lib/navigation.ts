/**
 * N'accepte qu'un chemin interne au site pour la redirection après connexion
 * (protection contre les redirections ouvertes : « //site », « /\site », schémas…).
 */
export function cheminInterne(p: string | null | undefined): string {
  if (!p || typeof p !== "string") return "/";
  if (!p.startsWith("/") || p.startsWith("//") || p.includes("\\") || /[\u0000-\u001f]/.test(p)) return "/";
  if (p.startsWith("/connexion")) return "/";
  return p;
}
