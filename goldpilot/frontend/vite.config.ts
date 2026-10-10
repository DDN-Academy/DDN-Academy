/// <reference types="vitest" />
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Le site est servi par FastAPI à la même origine que l'API (pas de CORS, URL relatives « /api/... »).
// En développement (`npm run dev`), Vite relaie /api vers le backend local (port 8101 par défaut).
const backend = process.env.GOLDPILOT_BACKEND ?? "http://127.0.0.1:8101";

export default defineConfig({
  plugins: [react()],
  base: "/",
  build: {
    outDir: "dist",
    emptyOutDir: true,
    sourcemap: false,
    target: "es2020",
    // Politique de sécurité du backend : script-src 'self' → aucun script en ligne.
    modulePreload: { polyfill: false },
    assetsInlineLimit: 0,
  },
  server: {
    proxy: { "/api": { target: backend, changeOrigin: false } },
  },
  test: {
    environment: "node",
    include: ["src/**/*.test.ts"],
  },
});
