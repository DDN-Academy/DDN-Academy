import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: {
    default: "PropDesk — Gestion de risque pour traders prop firm",
    template: "%s · PropDesk",
  },
  description:
    "Respectez les règles de votre challenge prop firm : drawdown trailing, soft breach, consistance. Suivez vos performances en temps réel.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr">
      <body className="min-h-screen font-sans">{children}</body>
    </html>
  );
}
