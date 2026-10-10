import { test, expect, seed, apiGet, verifierBandeauSimulation } from "./outils";

interface Dash {
  marche: { tradingview: string; tradovate: string; instrument: string };
  trading: { mode_utilisateur: string };
  statut: { notifications: { active: boolean } };
}

test.describe.configure({ mode: "serial" });

test.describe("Accueil", () => {
  test.afterAll(() => {
    seed("heartbeat-off");
  });

  test("sans signe de vie du moteur, aucun indicateur n'est vert", async ({ connecte: page }) => {
    seed("heartbeat-off");
    await page.goto("/");
    await expect(page.getByTestId("status-connexion")).toContainText("Déconnecté");
    for (const id of ["status-connexion", "status-donnees", "status-moteur", "status-notifications"]) {
      await expect(page.getByTestId(id)).not.toHaveAttribute("data-ton", "ok");
    }
    await expect(page.getByTestId("status-moteur")).toContainText("Arrêté");
    await expect(page.getByTestId("etat-global")).toContainText("Système en panne");
    await expect(page.locator('[data-testid="carte-systeme"] [data-ton="ok"]')).toHaveCount(0);
  });

  test("signe de vie + qualité ok → connexion, données et moteur verts ; notifications non configurées", async ({ connecte: page }) => {
    seed("heartbeat-on");
    await page.goto("/");
    await expect(page.getByTestId("status-connexion")).toHaveAttribute("data-ton", "ok");
    await expect(page.getByTestId("status-donnees")).toHaveAttribute("data-ton", "ok");
    await expect(page.getByTestId("status-moteur")).toHaveAttribute("data-ton", "ok");
    await expect(page.getByTestId("status-moteur")).toContainText("Actif");
    await expect(page.getByTestId("status-notifications")).toHaveAttribute("data-ton", "warn");
    await expect(page.getByTestId("status-notifications")).toContainText("Non configurées");
    await expect(page.getByTestId("status-donnees")).toContainText("Source : TradingView (webhook)");
    await expect(page.getByTestId("etat-global")).toContainText("Système partiellement opérationnel");
    await expect(page.getByTestId("marche-prix")).toContainText("4 036,20");
    await expect(page.getByTestId("maj-dashboard")).toContainText(/mis à jour (à l'instant|il y a \d+\s?s)/);
  });

  test("serveur injoignable → bandeau rouge et aucun vert", async ({ connecte: page }) => {
    seed("heartbeat-on");
    await page.route("**/api/dashboard", (r) => r.abort());
    await page.goto("/");
    await expect(page.getByTestId("bandeau-serveur-injoignable").first()).toContainText("Serveur injoignable");
    await expect(page.locator('[data-testid="carte-systeme"] [data-ton="ok"]')).toHaveCount(0);
    await expect(page.getByTestId("carte-marche")).toHaveCount(0);
  });

  test("mode rejeu (réponse du serveur modifiée) → bandeau REJEU HISTORIQUE permanent", async ({ connecte: page }) => {
    await page.route("**/api/dashboard", async (route) => {
      const r = await route.fetch();
      const d = await r.json();
      d.rejeu = { horloge: "2025-09-03T14:00:00+00:00", horloge_paris: "03/09/2025 16:00 (heure de Paris)" };
      await route.fulfill({ response: r, json: d });
    });
    await page.goto("/");
    await expect(page.getByTestId("bandeau-rejeu")).toContainText("REJEU HISTORIQUE — horloge virtuelle 03/09/2025 16:00 (heure de Paris), rien n'est réel");
    await page.getByTestId("nav-aide").click();
    await expect(page.getByTestId("bandeau-rejeu")).toBeVisible();
  });

  test("blocs marché, trading, incidents et bandeau SIMULATION", async ({ connecte: page }) => {
    const d = await apiGet<Dash>(page.request, "/api/dashboard");
    await page.goto("/");
    await verifierBandeauSimulation(page);
    await expect(page.getByTestId("bandeau-rejeu")).toHaveCount(0); // source TradingView : pas de rejeu
    const instr = page.getByTestId("marche-instrument");
    await expect(instr).toContainText(d.marche.tradingview);
    await expect(instr).toContainText(d.marche.tradovate);
    await expect(page.getByTestId("marche-seance")).not.toBeEmpty();
    await expect(page.getByTestId("marche-regime")).toContainText("tendance haussière (test)");
    await expect(page.getByTestId("marche-annonce")).toContainText("CPI");
    const trading = page.getByTestId("carte-trading");
    await expect(trading.getByTestId("signal-card")).toContainText("Actif");
    await expect(trading.getByTestId("signal-card")).toContainText("Position simulée ouverte");
    await expect(trading.getByTestId("signal-card")).toContainText("Stop-loss");
    await expect(page.getByTestId("statut-strategie")).toContainText("NON VALIDÉE");
    await expect(page.getByTestId("statut-strategie")).toContainText("Mode simulation");
    await expect(trading).toContainText("Risque autorisé et limites");
    await expect(page.getByTestId("etat-compte")).toContainText("Compte simulé");
    await expect(page.getByTestId("etat-compte")).toContainText("données non disponibles");
    await expect(page.getByTestId("incidents")).toContainText("Données en retard de 4 minutes (test)");
  });

  test("suspendre / reprendre les signaux change l'état du serveur", async ({ connecte: page }) => {
    const avant = (await apiGet<Dash>(page.request, "/api/dashboard")).trading.mode_utilisateur;
    await page.goto("/");
    const bouton = page.getByTestId("action-mode");
    await expect(bouton).toHaveText(avant === "pause" ? /Reprendre/ : /Suspendre/);
    await bouton.click();
    const attendu = avant === "pause" ? "actif" : "pause";
    await expect.poll(async () => (await apiGet<Dash>(page.request, "/api/dashboard")).trading.mode_utilisateur).toBe(attendu);
    await expect(bouton).toHaveText(attendu === "pause" ? /Reprendre/ : /Suspendre/);
    await bouton.click();
    await expect.poll(async () => (await apiGet<Dash>(page.request, "/api/dashboard")).trading.mode_utilisateur).toBe(avant);
  });

  test("activer / désactiver les notifications change l'état du serveur", async ({ connecte: page }) => {
    const avant = (await apiGet<Dash>(page.request, "/api/dashboard")).statut.notifications.active;
    await page.goto("/");
    await page.getByTestId("action-notifications").click();
    await expect.poll(async () => (await apiGet<Dash>(page.request, "/api/dashboard")).statut.notifications.active).toBe(!avant);
    await expect(page.getByTestId("action-notifications")).toHaveText(avant ? /Activer les notifications/ : /Désactiver les notifications/);
    await page.getByTestId("action-notifications").click();
    await expect.poll(async () => (await apiGet<Dash>(page.request, "/api/dashboard")).statut.notifications.active).toBe(avant);
  });

  test("tester une notification sans Telegram → message explicite", async ({ connecte: page }) => {
    await page.goto("/");
    await page.getByTestId("action-test-notification").click();
    await expect(page.getByTestId("carte-actions").getByTestId("message-action")).toContainText("Telegram non configuré");
  });
});
