"use client";

/** Sélecteur de compte : recharge la page avec ?account=<id>. */
import { usePathname, useRouter } from "next/navigation";
import type { PropAccount } from "@/lib/types";

export default function AccountSelect({
  accounts,
  selectedId,
}: {
  accounts: Pick<PropAccount, "id" | "name">[];
  selectedId: string;
}) {
  const router = useRouter();
  const pathname = usePathname();

  if (accounts.length <= 1) return null;

  return (
    <select
      className="field w-auto"
      value={selectedId}
      onChange={(e) => router.push(`${pathname}?account=${e.target.value}`)}
      aria-label="Choisir un compte"
    >
      {accounts.map((a) => (
        <option key={a.id} value={a.id}>
          {a.name}
        </option>
      ))}
    </select>
  );
}
