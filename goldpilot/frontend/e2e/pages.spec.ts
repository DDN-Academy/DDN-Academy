import { test, expect, seed, verifierBandeauSimulation } from "./outils";

const PAGES: [string, string][] = [
  ["/", "Accueil"],
  ["/signal/e2ecloture", "Signal LONG MGCZ2026"],
  ["/historique", "Historique des signaux"],
  ["/statistiques", "Statistiques"],
  ["/journal", "Journal"],
  ["/reglages", "Réglages"],
  ["/aide", "Aide"],
];

test.describe("Pages", () => {
  test("aucune erreur console, un h1 et le bandeau SIMULATION sur chaque page", async ({ connecte: page, erreursConsole }) => {
    seed("heartbeat-on");
    for (const [url, titre] of PAGES) {
      await page.goto(url);
      await expect(page.locator("h1")).toHaveCount(1);
      await expect(page.locator("h1")).toContainText(titre);
      await verifierBandeauSimulation(page);
      await page.waitForLoadState("networkidle");
    }
    seed("heartbeat-off");
    expect(erreursConsole).toEqual([]);
  });

  test("navigation : barre du bas sur mobile, barre du haut sur ordinateur", async ({ connecte: page }, info) => {
    await page.goto("/");
    const mobile = info.project.name === "mobile";
    await page.getByTestId(mobile ? "nav-statistiques" : "nav-statistiques-haut").click();
    await expect(page.locator("h1")).toHaveText("Statistiques");
    await expect(page.getByTestId("nav-statistiques")).toBeVisible({ visible: mobile });
    await expect(page.getByTestId("nav-statistiques-haut")).toBeVisible({ visible: !mobile });
    await page.getByTestId("nav-aide").click();
    await expect(page.locator("h1")).toHaveText("Aide");
    await expect(page.getByTestId("aide-glossaire")).toBeVisible();
    const largeur = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    expect(largeur).toBeLessThanOrEqual(0);
  });

  test("journal : tous les onglets s'affichent avec leur contenu", async ({ connecte: page }) => {
    await page.goto("/journal");
    const attendus: [string, string][] = [
      ["decisions", "Signal émis"],
      ["incidents", "Données en retard de 4 minutes (test)"],
      ["notifications", "Échec d'envoi"],
      ["webhooks", "jeton invalide"],
      ["controle", "Concordant"],
      ["audit", "connexion"],
    ];
    for (const [onglet, texte] of attendus) {
      await page.getByTestId(`onglet-${onglet}`).click();
      await expect(page.getByTestId(`onglet-${onglet}`)).toHaveAttribute("aria-selected", "true");
      const panneau = page.getByTestId(`journal-${onglet}`);
      await expect(panneau).toContainText(texte);
      await expect(panneau.getByTestId("ligne-journal").first()).toBeVisible();
    }
    await page.getByTestId("onglet-decisions").click();
    const det = page.getByTestId("journal-decisions").locator("details").first();
    await det.locator("summary").click();
    await expect(det.locator("pre")).toContainText("controles");
    await page.getByTestId("journal-limite").selectOption("25");
    await expect(page).toHaveURL(/limite=25/);
  });

  test("statistiques : verdict NON VALIDÉE, Monte-Carlo, suivi papier, exécution et contexte macro", async ({ connecte: page }) => {
    await page.goto("/statistiques");
    await expect(page.getByTestId("verdict-strategie")).toContainText("Stratégie NON VALIDÉE");
    await expect(page.getByTestId("table-montecarlo").locator("tbody tr").first()).toBeVisible();
    await expect(page.getByTestId("table-scenarios")).toContainText("IC95");
    await expect(page.getByTestId("paper-n")).toContainText("1");
    await expect(page.getByTestId("stats-paper").locator("svg")).toBeVisible();
    await expect(page.getByTestId("stats-execution")).toContainText("Concordant : 1");
    const macro = page.getByTestId("contexte-macro");
    await expect(macro).toContainText("Information de contexte uniquement");
    await expect(page.getByTestId("macro-probleme")).toContainText("DGS10");
    await expect(page.getByTestId("table-macro")).toContainText("121,3456");
    await expect(page.getByTestId("table-macro")).toContainText("−0,07");
    await expect(page.getByTestId("table-macro")).toContainText("non calculée");
  });
});
