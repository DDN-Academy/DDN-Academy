"use client";

/**
 * Shell de l'app authentifiée : sidebar sur desktop, barre en bas sur mobile.
 */
import Link from "next/link";
import { usePathname } from "next/navigation";

const NAV = [
  { href: "/dashboard", label: "Dashboard", icon: "▦" },
  { href: "/dashboard/trades", label: "Trades", icon: "⇄" },
  { href: "/dashboard/accounts", label: "Comptes", icon: "◧" },
  { href: "/dashboard/sizing", label: "Sizing", icon: "⚖" },
  { href: "/dashboard/billing", label: "Abonnement", icon: "✦" },
  { href: "/dashboard/profile", label: "Profil", icon: "◉" },
];

export default function AppShell({
  children,
  email,
  plan,
}: {
  children: React.ReactNode;
  email: string;
  plan: string;
}) {
  const pathname = usePathname();
  const isActive = (href: string) =>
    href === "/dashboard" ? pathname === href : pathname.startsWith(href);

  return (
    <div className="flex min-h-screen">
      {/* Sidebar desktop */}
      <aside className="fixed inset-y-0 left-0 z-20 hidden w-56 flex-col border-r border-ink-700 bg-ink-900/80 backdrop-blur md:flex">
        <div className="px-5 py-5">
          <Link href="/dashboard" className="font-mono text-lg font-bold tracking-tight">
            Prop<span className="text-accent">Desk</span>
          </Link>
        </div>
        <nav className="flex-1 space-y-1 px-3">
          {NAV.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-colors ${
                isActive(item.href)
                  ? "bg-ink-800 font-semibold text-fg"
                  : "text-fg-muted hover:bg-ink-800/60 hover:text-fg"
              }`}
            >
              <span aria-hidden className="w-4 text-center">
                {item.icon}
              </span>
              {item.label}
            </Link>
          ))}
        </nav>
        <div className="border-t border-ink-700 p-4">
          <p className="truncate text-xs text-fg-muted" title={email}>
            {email}
          </p>
          <p className="mt-1 text-xs">
            <span
              className={`rounded px-1.5 py-0.5 font-mono text-[10px] uppercase ${
                plan === "pro" ? "bg-profit/15 text-profit" : "bg-ink-800 text-fg-muted"
              }`}
            >
              {plan === "pro" ? "Pro" : "Gratuit"}
            </span>
          </p>
          <form action="/auth/signout" method="post" className="mt-3">
            <button type="submit" className="text-xs text-fg-faint hover:text-loss">
              Se déconnecter →
            </button>
          </form>
        </div>
      </aside>

      {/* Contenu */}
      <div className="flex-1 pb-20 md:ml-56 md:pb-0">
        <main className="mx-auto max-w-6xl p-4 md:p-8">{children}</main>
      </div>

      {/* Barre de navigation mobile */}
      <nav className="fixed inset-x-0 bottom-0 z-20 flex border-t border-ink-700 bg-ink-900/95 backdrop-blur md:hidden">
        {NAV.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={`flex flex-1 flex-col items-center gap-0.5 py-2 text-[10px] ${
              isActive(item.href) ? "text-accent" : "text-fg-muted"
            }`}
          >
            <span aria-hidden className="text-base leading-none">
              {item.icon}
            </span>
            {item.label}
          </Link>
        ))}
      </nav>
    </div>
  );
}
