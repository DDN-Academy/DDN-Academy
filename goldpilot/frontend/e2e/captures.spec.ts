import path from "node:path";
import { fileURLToPath } from "node:url";
import type { Page } from "@playwright/test";
import { test, expect, seed } from "./outils";

// Captures pleine page (mobile) pour la documentation : `npm run captures` (CAPTURES=1). Données de test FICTIVES.
const DOSSIER = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../docs/captures");
const PAGES: [string, string][] = [
  ["accueil", "/"],
  ["signal", "/signal/e2ecloture"],
  ["historique", "/historique"],
  ["statistiques", "/statistiques"],
  ["journal", "/journal"],
  ["parametres", "/reglages"],
  ["aide", "/aide"],
];

/** Agrandit la fenêtre à la hauteur de la page avant la capture : les éléments fixes (en-tête, barre du bas) restent à leur place. */
async function capturer(page: Page, fichier: string): Promise<void> {
  const h = await page.evaluate(() => document.documentElement.scrollHeight);
  await page.setViewportSize({ width: 390, height: Math.max(844, h) });
  await page.waitForTimeout(300);
  await page.screenshot({ path: fichier, animations: "disabled" });
  await page.setViewportSize({ width: 390, height: 844 });
}

test.describe("Captures d'écran", () => {
  test.skip(!process.env.CAPTURES, "captures seulement avec CAPTURES=1");
  test.beforeEach(({}, info) => {
    test.skip(info.project.name !== "mobile", "captures mobiles uniquement");
  });

  test("connexion", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByTestId("form-connexion")).toBeVisible();
    await capturer(page, path.join(DOSSIER, "connexion.png"));
  });

  test("pages principales", async ({ connecte: page }) => {
    seed("heartbeat-on");
    for (const [nom, url] of PAGES) {
      await page.goto(url);
      await expect(page.locator("h1")).toBeVisible();
      await page.waitForLoadState("networkidle");
      if (nom === "parametres") {
        await page.getByTestId("bouton-voir-pine").click();
        await expect(page.getByTestId("script-pine")).toBeVisible();
      }
      await capturer(page, path.join(DOSSIER, `${nom}.png`));
    }
    seed("heartbeat-off");
  });
});
