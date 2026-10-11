import { test, expect, seed, apiGet, badge } from "./outils";

const LIBELLES = ["En attente de déclenchement", "Actif", "Annulé", "Expiré", "Clôturé"];

test.describe("Signaux", () => {
  test("historique : filtres par statut et libellés distincts", async ({ connecte: page }) => {
    await page.goto("/historique");
    const liste = page.getByTestId("liste-signaux");
    for (const l of LIBELLES) await expect(badge(liste, l).first()).toBeVisible();
    const filtres: [string, string][] = [
      ["EN_ATTENTE", "En attente de déclenchement"],
      ["ACTIF", "Actif"],
      ["ANNULE", "Annulé"],
      ["EXPIRE", "Expiré"],
      ["CLOTURE", "Clôturé"],
    ];
    for (const [code, libelle] of filtres) {
      await page.getByTestId(`filtre-${code}`).click();
      await expect(page).toHaveURL(new RegExp(`statut=${code}`));
      await expect(page.getByTestId(`filtre-${code}`)).toHaveAttribute("aria-pressed", "true");
      const lignes = page.getByTestId("ligne-signal");
      await expect(lignes.first()).toBeVisible();
      const n = await lignes.count();
      for (let i = 0; i < n; i++) await expect(badge(lignes.nth(i), libelle)).toBeVisible();
      const api = await apiGet<{ signaux: unknown[] }>(page.request, `/api/signals?limit=50&statut=${code}`);
      expect(n).toBe(api.signaux.length);
    }
    await page.getByTestId("filtre-tous").click();
    await expect(page).not.toHaveURL(/statut=/);
  });

  test("détail : tous les champs §11, contrôles du risque, alertes et exécution déclarée", async ({ connecte: page }) => {
    await page.goto("/signal/e2ecloture");
    await expect(page.getByRole("heading", { level: 1 })).toContainText("Signal LONG MGCZ2026");
    const champs = page.getByTestId("champs-alerte");
    for (const k of [
      "Instrument et contrat",
      "Date et heure",
      "Sens",
      "Entrée",
      "Type d'entrée",
      "Stop-loss",
      "Take-profit",
      "Rendement / risque",
      "Risque estimé",
      "Taille",
      "Validité",
      "Condition d'annulation",
      "Justification",
      "Calendrier économique",
      "Source de prix",
      "Statut",
    ]) {
      await expect(champs.locator("dt", { hasText: k }).first()).toBeVisible();
    }
    await expect(champs).toContainText("3 990,00");
    await expect(champs).toContainText("Pas d'objectif fixe");
    await expect(champs).toContainText("Clôturé — sortie par stop suiveur");
    const ctrl = page.getByTestId("controles-risque");
    await expect(ctrl.getByTestId("ligne-controle")).toHaveCount(4);
    await expect(ctrl).toContainText("non bloquant (information)");
    await expect(page.getByTestId("alertes-envoyees")).toContainText("Envoyée");
    await expect(page.getByTestId("chronologie")).toContainText("Sortie simulée");
    await expect(page.getByTestId("position-simulee")).toContainText("+1,18");
    await expect(page.getByTestId("contexte-decision")).toContainText("tendance haussière (test)");
    await expect(page.getByTestId("signal-statut")).toContainText("Exécution déclarée par toi — non confirmée par le courtier");
    await expect(page.getByTestId("carte-annulation")).toHaveCount(0);
  });

  test("déclarer mon exécution affiche « déclaré par toi — non confirmé par le courtier »", async ({ connecte: page }) => {
    const id = seed("pending");
    await page.goto(`/signal/${id}`);
    const carte = page.getByTestId("carte-declaration");
    await expect(carte).toContainText("Déclaré par toi — non confirmé par le courtier");
    await page.getByTestId("champ-executee-oui").check();
    await page.getByTestId("champ-prix-entree").fill("3900.5");
    await page.getByTestId("champ-prix-sortie").fill("3910");
    await page.getByTestId("champ-contrats").fill("1");
    await page.getByTestId("bouton-declarer").click();
    await expect(carte.getByTestId("message-action")).toContainText("déclarée par toi, non confirmée par le courtier");
    await expect(page.getByTestId("signal-statut")).toContainText("Exécution déclarée par toi — non confirmée par le courtier");
    await expect(page.getByTestId("declaration-existante")).toContainText("+95 $");
  });

  test("annuler un signal en attente", async ({ connecte: page }) => {
    const id = seed("pending");
    await page.goto(`/signal/${id}`);
    await expect(page.getByTestId("signal-statut")).toContainText("En attente de déclenchement");
    page.once("dialog", (d) => void d.accept());
    await page.getByTestId("bouton-annuler-signal").click();
    await expect(page.getByTestId("signal-statut")).toContainText("Annulé");
    await expect(page.getByTestId("carte-annulation")).toHaveCount(0);
    const d = await apiGet<{ signal: { statut: string; raison_statut: string } }>(page.request, `/api/signals/${id}`);
    expect(d.signal.statut).toBe("ANNULE");
    expect(d.signal.raison_statut).toBe("annulé par toi");
  });

  test("une position simulée ouverte ne peut pas être annulée", async ({ connecte: page }) => {
    await page.goto("/signal/e2eactif");
    await expect(page.getByTestId("signal-statut")).toContainText("Actif");
    await expect(page.getByTestId("signal-statut")).toContainText("Position simulée ouverte");
    await expect(page.getByTestId("carte-annulation")).toHaveCount(0);
    const r = await page.request.post("/api/signals/e2eactif/cancel", { headers: { "X-GoldPilot": "1" }, data: {} });
    expect(r.status()).toBe(400);
    expect((await r.json()).detail).toContain("position simulée est déjà ouverte");
  });
});
