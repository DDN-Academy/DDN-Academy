import { test as base, expect, type APIRequestContext, type Locator, type Page } from "@playwright/test";
import { execFileSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

export const MOT_DE_PASSE = "e2e-mot-de-passe-123";
const ICI = path.dirname(fileURLToPath(import.meta.url));
const BACKEND = path.resolve(ICI, "../../backend");

/** Exécute une commande du jeu de données de test (écriture directe dans la base via les modèles GoldPilot). */
export function seed(cmd: "heartbeat-on" | "heartbeat-off" | "pending" | "version-pending" | "sans-donnees"): string {
  const dir = process.env.GOLDPILOT_E2E_DIR;
  if (!dir) throw new Error("GOLDPILOT_E2E_DIR non défini");
  return execFileSync(process.env.PYTHON ?? "python3", [path.join(ICI, "seed.py"), cmd], {
    cwd: BACKEND,
    env: { ...process.env, DATABASE_URL: `sqlite:///${dir}/e2e.db`, PYTHONPATH: BACKEND },
    encoding: "utf8",
  }).trim();
}

/** Adresse IP fictive propre à chaque test (X-Forwarded-For, serveur lancé avec TRUST_PROXY=true) : isole les limites de débit. */
function ipDeTest(): string {
  const r = () => Math.floor(Math.random() * 250) + 1;
  return `10.${r()}.${r()}.${r()}`;
}

export const test = base.extend<{ connecte: Page; erreursConsole: string[] }>({
  extraHTTPHeaders: async ({}, use) => {
    await use({ "X-Forwarded-For": ipDeTest() });
  },
  /** Page déjà connectée (cookie de session obtenu par l'API de connexion). */
  connecte: async ({ page }, use) => {
    await connexionApi(page.request);
    await use(page);
  },
  erreursConsole: async ({ page }, use) => {
    const erreurs: string[] = [];
    page.on("console", (m) => {
      if (m.type() === "error") erreurs.push(m.text());
    });
    page.on("pageerror", (e) => erreurs.push(`pageerror: ${e.message}`));
    await use(erreurs);
  },
});

export { expect };

export async function connexionApi(req: APIRequestContext): Promise<void> {
  const r = await req.post("/api/auth/login", { data: { password: MOT_DE_PASSE }, headers: { "X-GoldPilot": "1" } });
  expect(r.status(), await r.text()).toBe(200);
}

export async function apiGet<T>(req: APIRequestContext, url: string): Promise<T> {
  const r = await req.get(url);
  expect(r.status(), url).toBe(200);
  return (await r.json()) as T;
}

/** Bandeau SIMULATION toujours présent (stratégie non validée). */
export async function verifierBandeauSimulation(page: Page): Promise<void> {
  const b = page.getByTestId("bandeau-simulation");
  await expect(b).toBeVisible();
  await expect(b).toContainText("SIMULATION");
  await expect(b).toContainText("NON VALIDÉE");
}

/** Badge dont le libellé visible est exactement `libelle` (le préfixe pour lecteur d'écran « Information : » est ignoré). */
export function badge(scope: Locator | Page, libelle: string): Locator {
  const echappe = libelle.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  return scope.locator(".badge", { hasText: new RegExp(`(^|: )${echappe}$`) });
}
