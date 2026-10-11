import { test, expect, seed, apiGet } from "./outils";

// Corrections de la revue : fenêtre d'entrée, niveaux, glissement déclaré, gouvernance de la stratégie,
// état Telegram fiable, journal daté.

test.describe("Revue : affichages honnêtes", () => {
  test("signal ouvert : entrée exploitable + niveaux ; signal à validité écoulée : « Entrée fermée — ne plus entrer »", async ({ connecte: page }) => {
    await page.goto("/");
    const carte = page.getByTestId("carte-trading").getByTestId("signal-card");
    await expect(carte.getByTestId("signal-entree")).toContainText("Entrée exploitable maintenant");
    await expect(carte.getByTestId("signal-niveaux")).toContainText("Plus haut de la veille");
    await expect(carte.getByTestId("signal-niveaux")).toContainText("ATR");
    await expect(page.getByTestId("alerte-signal-en-cours")).toContainText("entrée exploitable maintenant");

    await page.goto("/signal/e2eattente");
    await expect(page.getByTestId("signal-statut")).toContainText("Entrée fermée — ne plus entrer");
    await expect(page.getByTestId("signal-entree")).toContainText("la validité est écoulée");
    await expect(page.getByTestId("champs-alerte")).toContainText("fermée — ne plus entrer");
    await expect(page.getByTestId("signal-statut")).not.toContainText("Entrée exploitable maintenant");
  });

  test("statistiques : glissement déclaré comparé à l'hypothèse, gouvernance et revue périodique", async ({ connecte: page }) => {
    await page.goto("/statistiques");
    const decl = page.getByTestId("execution-declaree");
    await expect(decl).toContainText("déclaré par toi — non confirmé par le courtier");
    await expect(decl.getByTestId("glissement-declare")).toContainText("$/once");
    await expect(decl).toContainText("Glissement supposé");
    await expect(page.getByTestId("verdict-glissement")).toContainText("Au-delà de l'hypothèse");
    const gouv = page.getByTestId("gouvernance-strategie");
    await expect(gouv.getByTestId("version-courante")).toContainText("S1-");
    await expect(gouv.getByTestId("revue-periodique")).toContainText("Revue du");
    await expect(gouv.getByTestId("revue-conclusion")).toContainText("échantillon trop petit");
    await expect(gouv.getByTestId("form-approbation-version")).toHaveCount(0); // approbation : seulement dans Paramètres
  });

  test("nouvelle version non approuvée : arrêt de sécurité, approbation exacte dans Paramètres", async ({ connecte: page }) => {
    seed("version-pending");
    await page.goto("/");
    await expect(page.getByTestId("arret-securite")).toContainText("nouvelle version de stratégie");
    await expect(page.getByTestId("action-reprise-arret")).toHaveCount(0);
    const r = await page.request.post("/api/engine/resume-after-halt", { headers: { "X-GoldPilot": "1" }, data: {} });
    expect(r.status()).toBe(409);
    await page.getByTestId("action-approuver-version").click();
    await expect(page).toHaveURL(/\/reglages#gouvernance$/);
    const gouv = page.getByTestId("gouvernance-strategie");
    await expect(gouv.getByTestId("version-en-attente")).toContainText("S0-ancienne-version-e2e");
    await page.getByTestId("champ-phrase-version").fill("oui");
    await page.getByTestId("bouton-approuver-version").click();
    await expect(gouv.getByTestId("message-action")).toContainText("Recopie exactement");
    await page.getByTestId("champ-phrase-version").fill("J'APPROUVE CETTE VERSION");
    await page.getByTestId("bouton-approuver-version").click();
    await expect(gouv.getByTestId("message-action")).toContainText("Version approuvée");
    await expect(gouv.getByTestId("version-en-attente")).toHaveCount(0);
    await expect(gouv.getByTestId("version-approuvee")).toContainText("approuvée par toi");
    const g = await apiGet<{ en_attente: boolean }>(page.request, "/api/strategy/governance");
    expect(g.en_attente).toBe(false);
    const d = await apiGet<{ statut: { moteur: { arret: unknown } } }>(page.request, "/api/dashboard");
    expect(d.statut.moteur.arret).toBeNull();
  });

  test("Telegram : état des envois inconnu (rouge) quand le serveur ne répond pas", async ({ connecte: page }) => {
    await page.route("**/api/dashboard", (r) => r.abort());
    await page.goto("/reglages");
    const etat = page.getByTestId("etat-envoi-telegram");
    await expect(etat).toContainText("inconnu");
    await expect(etat).toHaveAttribute("data-ton", "bad");
  });

  test("journal du contrôle croisé : heure de New York avec la date", async ({ connecte: page }) => {
    await page.goto("/journal");
    await page.getByTestId("onglet-controle").click();
    await expect(page.getByTestId("journal-controle")).toContainText(/\d{2}\/\d{2}\/\d{4} \d{2}:\d{2} New York/);
  });

  test("refus 400 : message « Action refusée », jamais « Erreur du serveur »", async ({ connecte: page }) => {
    await page.goto("/reglages");
    await page.getByTestId("bouton-detecter-chat").click();
    const msg = page.getByTestId("reglages-telegram").getByTestId("message-action").first();
    await expect(msg).toContainText("Action refusée");
    await expect(msg).not.toContainText("Erreur du serveur");
  });
});
