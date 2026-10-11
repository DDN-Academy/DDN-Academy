// Accès à l'API GoldPilot (même origine, cookie de session HttpOnly).
// Toute écriture envoie l'en-tête « X-GoldPilot: 1 » exigé par le serveur (protection CSRF).

export class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.status = status;
    this.name = "ApiError";
  }
}

type Listener = () => void;
const unauthorizedListeners = new Set<Listener>();

/** Appelé quand le serveur répond 401 : l'application renvoie vers la page de connexion. */
export function onUnauthorized(fn: Listener): () => void {
  unauthorizedListeners.add(fn);
  return () => unauthorizedListeners.delete(fn);
}

/** Message en français pour un statut HTTP, complété par le « detail » du serveur s'il existe. */
export function messageErreur(status: number, detail?: unknown): string {
  const d = detailTexte(detail);
  switch (status) {
    case 0:
      return "Serveur injoignable : vérifie ta connexion internet ou l'état du serveur.";
    case 400:
      return d ? `Action refusée : ${d}` : "Action refusée par le serveur.";
    case 401:
      return d ? `Connexion requise : ${d}` : "Connexion requise.";
    case 403:
      return d ? `Accès refusé : ${d}` : "Accès refusé.";
    case 404:
      return d ? `Introuvable : ${d}` : "Élément introuvable.";
    case 409:
      return d || "Action refusée par le serveur.";
    case 422:
      return d ? `Valeurs refusées : ${d}` : "Valeurs refusées par le serveur.";
    case 429:
      return d ? `Trop de requêtes : ${d}` : "Trop de requêtes : patiente un moment puis réessaie.";
    case 502:
      return d || "Service externe injoignable.";
    default:
      return d ? `Erreur du serveur (${status}) : ${d}` : `Erreur du serveur (${status}).`;
  }
}

const CHAMPS: Record<string, string> = {
  password: "mot de passe",
  solde: "solde",
  plus_haut_fin_de_jour: "plus haut solde de fin de journée",
  meilleur_jour: "meilleur jour",
  entree: "prix d'entrée",
  sortie: "prix de sortie",
  contrats: "contrats",
  note: "note",
  titre: "titre",
  quand: "date et heure",
  reference: "référence",
};

/** Le « detail » FastAPI peut être une chaîne ou une liste d'erreurs de validation Pydantic (en anglais). */
export function detailTexte(detail: unknown): string {
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    return detail
      .map((e) => {
        if (e && typeof e === "object") {
          const o = e as { loc?: unknown[]; msg?: string; type?: string; ctx?: Record<string, unknown> };
          const champ = Array.isArray(o.loc) ? String(o.loc[o.loc.length - 1]) : "";
          const nom = CHAMPS[champ] ?? champ;
          return `${nom ? nom + " : " : ""}${traduireValidation(o.type, o.msg, o.ctx)}`;
        }
        return String(e);
      })
      .join(" ; ");
  }
  return "";
}

function traduireValidation(type?: string, msg?: string, ctx?: Record<string, unknown>): string {
  const v = (k: string) => (ctx && ctx[k] !== undefined ? String(ctx[k]) : "?");
  switch (type) {
    case "missing":
      return "champ obligatoire";
    case "greater_than":
      return `doit être supérieur à ${v("gt")}`;
    case "greater_than_equal":
      return `doit être supérieur ou égal à ${v("ge")}`;
    case "less_than":
      return `doit être inférieur à ${v("lt")}`;
    case "less_than_equal":
      return `doit être inférieur ou égal à ${v("le")}`;
    case "string_too_short":
      return `trop court (au moins ${v("min_length")} caractères)`;
    case "string_too_long":
      return `trop long (au plus ${v("max_length")} caractères)`;
    case "float_parsing":
    case "int_parsing":
    case "float_type":
    case "int_type":
    case "finite_number":
      return "nombre attendu";
    case "int_from_float":
      return "nombre entier attendu";
    case "bool_parsing":
    case "bool_type":
      return "oui ou non attendu";
    case "json_invalid":
    case "json_type":
      return "données mal formées";
    case "string_type":
      return "texte attendu";
    case "literal_error":
    case "enum":
      return "valeur non autorisée";
    case "value_error":
      return msg ? msg.replace(/^Value error,\s*/, "") : "valeur invalide";
    case "datetime_parsing":
    case "datetime_from_date_parsing":
      return "date et heure invalides";
    case "extra_forbidden":
      return "champ non autorisé";
    default:
      return "valeur invalide"; // message Pydantic en anglais : jamais affiché tel quel
  }
}

async function request<T>(method: string, url: string, body?: unknown, asText = false): Promise<T> {
  const headers: Record<string, string> = { Accept: asText ? "text/plain" : "application/json" };
  if (method !== "GET") headers["X-GoldPilot"] = "1";
  if (body !== undefined) headers["Content-Type"] = "application/json";
  let resp: Response;
  try {
    resp = await fetch(url, {
      method,
      headers,
      credentials: "same-origin",
      cache: "no-store",
      body: body !== undefined ? JSON.stringify(body) : undefined,
    });
  } catch {
    throw new ApiError(0, messageErreur(0));
  }
  if (!resp.ok) {
    let detail: unknown;
    try {
      detail = (await resp.json())?.detail;
    } catch {
      detail = undefined;
    }
    if (resp.status === 401 && url !== "/api/auth/login") unauthorizedListeners.forEach((fn) => fn());
    throw new ApiError(resp.status, messageErreur(resp.status, detail));
  }
  if (asText) return (await resp.text()) as unknown as T;
  return (await resp.json()) as T;
}

export const api = {
  get: <T>(url: string) => request<T>("GET", url),
  getText: (url: string) => request<string>("GET", url, undefined, true),
  post: <T = { ok: boolean }>(url: string, body?: unknown) => request<T>("POST", url, body ?? {}),
  put: <T = { ok: boolean }>(url: string, body: unknown) => request<T>("PUT", url, body),
};
