import type { Metadata } from "next";
import AccountForm from "@/components/AccountForm";

export const metadata: Metadata = { title: "Nouveau compte" };

export default function NewAccountPage() {
  return (
    <div>
      <h1 className="mb-2 text-2xl font-bold">Nouveau compte prop firm</h1>
      <p className="mb-6 text-sm text-fg-muted">
        Reprenez les règles exactes de votre challenge — elles pilotent toutes les alertes.
      </p>
      <AccountForm />
    </div>
  );
}
