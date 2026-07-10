import type { Config } from "tailwindcss";

/**
 * PropDesk — dark "trading terminal" theme.
 * Palette centered on near-black surfaces with green/red P&L accents.
 */
const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // Surfaces
        ink: {
          950: "#07090d", // page background
          900: "#0b0e14", // card background
          800: "#121722", // raised surface / inputs
          700: "#1b2230", // borders / dividers
          600: "#2a3448",
        },
        // Text
        fg: {
          DEFAULT: "#e6e9f0",
          muted: "#8b93a7",
          faint: "#5b6478",
        },
        // Accents
        profit: "#2fdc8b",
        loss: "#ff5c5c",
        warn: "#ffb020",
        accent: "#4f8cff",
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "-apple-system", "sans-serif"],
        mono: ["'JetBrains Mono'", "ui-monospace", "SFMono-Regular", "monospace"],
      },
      boxShadow: {
        card: "0 1px 0 0 rgba(255,255,255,0.03) inset, 0 8px 24px rgba(0,0,0,0.35)",
      },
    },
  },
  plugins: [],
};

export default config;
