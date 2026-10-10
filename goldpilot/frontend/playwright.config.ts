import { defineConfig } from "@playwright/test";
import os from "node:os";
import path from "node:path";

// Tests de bout en bout : backend GoldPilot isolé (SQLite temporaire + données de test fictives) sur le port 8102,
// qui sert le site compilé (lancer `npm run build` avant). Chromium : version 1194 attendue par @playwright/test 1.56.1.
const PORT = Number(process.env.GOLDPILOT_E2E_PORT ?? 8102);
const DIR = process.env.GOLDPILOT_E2E_DIR ?? path.join(os.tmpdir(), "goldpilot-e2e");
process.env.GOLDPILOT_E2E_DIR = DIR;
process.env.GOLDPILOT_E2E_PORT = String(PORT);

export default defineConfig({
  testDir: "./e2e",
  outputDir: path.join(DIR, "resultats"),
  fullyParallel: false,
  workers: 1,
  retries: 0,
  timeout: 45_000,
  expect: { timeout: 8_000 },
  reporter: [["list"]],
  use: {
    baseURL: `http://127.0.0.1:${PORT}`,
    locale: "fr-FR",
    timezoneId: "Europe/Paris",
    trace: "retain-on-failure",
  },
  projects: [
    {
      name: "mobile",
      use: { browserName: "chromium", viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true },
    },
    { name: "desktop", use: { browserName: "chromium", viewport: { width: 1280, height: 900 } } },
  ],
  webServer: {
    command: "bash e2e/start-backend.sh",
    url: `http://127.0.0.1:${PORT}/`,
    reuseExistingServer: false,
    timeout: 60_000,
    stdout: "pipe",
    stderr: "pipe",
  },
});
