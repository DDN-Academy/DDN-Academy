import { test, expect, MOT_DE_PASSE, connexionApi } from "./outils";

test.describe("Connexion et sécurité", () => {
  test("une page protégée renvoie vers la connexion", async ({ page }) => {
    await page.goto("/historique");
    await expect(page).toHaveURL(/\/connexion\?suite=%2Fhistorique$/);
    await expect(page.getByRole("heading", { level: 1, name: "Connexion" })).toBeVisible();
    // Seul le mot de passe est demandé.
    await expect(page.locator("form input")).toHaveCount(1);
  });

  test("mauvais mot de passe refusé, bon mot de passe accepté", async ({ page }) => {
    await page.goto("/historique");
    await page.getByTestId("champ-mot-de-passe").fill("pas-le-bon");
    await page.getByTestId("bouton-connexion").click();
    await expect(page.getByTestId("erreur-connexion")).toHaveText("Mot de passe incorrect.");
    await page.getByTestId("champ-mot-de-passe").fill(MOT_DE_PASSE);
    await page.getByTestId("bouton-connexion").click();
    await expect(page).toHaveURL(/\/historique$/);
    await expect(page.getByRole("heading", { level: 1, name: "Historique des signaux" })).toBeVisible();
  });

  test("déconnexion puis 401 → retour à la connexion", async ({ connecte: page }) => {
    await page.goto("/");
    await expect(page.getByRole("heading", { level: 1, name: "Accueil" })).toBeVisible();
    await page.getByTestId("bouton-deconnexion").click();
    await expect(page).toHaveURL(/\/connexion$/);
    const r = await page.request.get("/api/dashboard");
    expect(r.status()).toBe(401);
  });

  test("écriture sans en-tête X-GoldPilot → 403", async ({ request }) => {
    await connexionApi(request);
    const r = await request.post("/api/engine/mode", { data: { mode: "pause" } });
    expect(r.status()).toBe(403);
    expect((await r.json()).detail).toBe("en-tête de sécurité manquant");
  });

  test("session expirée en cours d'utilisation → page de connexion", async ({ connecte: page }) => {
    await page.goto("/journal");
    await expect(page.getByRole("heading", { level: 1, name: "Journal" })).toBeVisible();
    await page.context().clearCookies();
    await page.getByTestId("journal-actualiser").click();
    await expect(page).toHaveURL(/\/connexion/);
  });
});
