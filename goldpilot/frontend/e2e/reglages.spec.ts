import { test, expect, apiGet } from "./outils";

test.describe("Réglages", () => {
  test("risque invalide → message de l'API ; valeur valide conservée après rechargement", async ({ connecte: page }) => {
    await page.goto("/reglages");
    const carte = page.getByTestId("reglages-risque");
    await page.getByTestId("champ-risk_per_trade_usd").fill("1000");
    await page.getByTestId("bouton-enregistrer-risque").click();
    await expect(carte.getByTestId("message-action")).toContainText("Risque par trade : entre 25 $ et 500 $");
    await page.getByTestId("champ-risk_per_trade_usd").fill("200");
    await page.getByTestId("champ-daily_loss_stop_usd").fill("450");
    await page.getByTestId("bouton-enregistrer-risque").click();
    await expect(carte.getByTestId("message-action")).toContainText("Paramètres de risque enregistrés");
    await page.reload();
    await expect(page.getByTestId("champ-risk_per_trade_usd")).toHaveValue("200");
    await expect(page.getByTestId("champ-daily_loss_stop_usd")).toHaveValue("450");
    const s = await apiGet<{ risque: { risk_per_trade_usd: number } }>(page.request, "/api/settings");
    expect(s.risque.risk_per_trade_usd).toBe(200);
  });

  test("mode réel refusé (stratégie non validée)", async ({ connecte: page }) => {
    await page.goto("/reglages");
    const carte = page.getByTestId("reglages-mode");
    await expect(page.getByTestId("verrou-reel")).toContainText("Mode réel verrouillé");
    await page.getByTestId("champ-phrase-confirmation").fill("JE CONFIRME LE PASSAGE EN REEL");
    await page.getByTestId("bouton-mode-reel").click();
    await expect(carte.getByTestId("message-action").last()).toContainText("critères de validation");
    await expect(page.getByTestId("mode-actuel")).toHaveText(/: Simulation$/);
  });

  test("confirmation FundedNext : référence obligatoire", async ({ connecte: page }) => {
    await page.goto("/reglages");
    const form = page.getByTestId("form-confirmation-fundednext");
    await page.getByTestId("champ-confirmation-fundednext").check();
    await page.getByTestId("champ-reference-fundednext").fill("");
    await page.getByTestId("bouton-enregistrer-confirmation").click();
    await expect(form.getByTestId("message-action")).toContainText("Indique la référence de la réponse écrite de FundedNext");
    await page.getByTestId("champ-reference-fundednext").fill("Ticket E2E-123");
    await page.getByTestId("bouton-enregistrer-confirmation").click();
    await expect(form.getByTestId("message-action")).toContainText("Confirmation FundedNext enregistrée.");
    // Retour à l'état initial.
    await page.getByTestId("champ-confirmation-fundednext").uncheck();
    await page.getByTestId("bouton-enregistrer-confirmation").click();
    await expect(form.getByTestId("message-action")).toContainText("Confirmation FundedNext retirée.");
  });

  test("programme, TradingView (script Pine, jamais « connecté » sans données récentes) et Telegram", async ({ connecte: page }) => {
    await page.goto("/reglages");
    const regles = page.getByTestId("table-regles");
    await expect(regles.getByTestId("ligne-regle").first()).toBeVisible();
    await expect(regles).toContainText(/confirmée|contradictoire|inconnue/);
    await expect(regles).toContainText("vérifié le");
    await expect(page.getByTestId("url-webhook")).toHaveText("http://127.0.0.1:8102/api/webhooks/tradingview");
    const tv = page.getByTestId("reglages-tradingview");
    await expect(tv).toContainText("le plan gratuit ne peut pas envoyer de webhooks");
    await expect(tv).toContainText("double authentification (2FA)");
    await expect(page.getByTestId("etat-tradingview")).not.toContainText("Réception vérifiée");
    await expect(page.getByTestId("etat-tradingview")).toContainText("réception non vérifiée");
    await page.getByTestId("bouton-voir-pine").click();
    await expect(page.getByTestId("script-pine")).toContainText("//@version=6");
    await expect(page.getByTestId("bouton-copier-pine")).toBeVisible();
    const tg = page.getByTestId("reglages-telegram");
    await expect(tg).toContainText("@BotFather");
    await page.getByTestId("bouton-test-notification").click();
    await expect(tg.getByTestId("message-action")).toContainText("Telegram non configuré");
    await page.getByTestId("bouton-detecter-chat").click();
    await expect(tg.getByTestId("message-action").first()).toContainText("TELEGRAM_BOT_TOKEN n'est pas défini");
    await expect(page.getByTestId("liste-evenements")).toContainText("CPI");
  });
});
