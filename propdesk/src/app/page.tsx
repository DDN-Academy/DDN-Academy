import Link from "next/link";

/** Landing page publique. */
export default function LandingPage() {
  return (
    <main className="mx-auto max-w-5xl px-4">
      {/* Header */}
      <header className="flex items-center justify-between py-6">
        <span className="font-mono text-lg font-bold tracking-tight">
          Prop<span className="text-accent">Desk</span>
        </span>
        <nav className="flex items-center gap-3">
          <Link href="/login" className="btn-ghost">
            Connexion
          </Link>
          <Link href="/signup" className="btn-primary">
            Commencer gratuitement
          </Link>
        </nav>
      </header>

      {/* Hero */}
      <section className="py-16 text-center md:py-24">
        <p className="mb-4 inline-block rounded-full border border-ink-700 bg-ink-900 px-3 py-1 text-xs text-fg-muted">
          Pour les traders FundedNext, Topstep, Apex &amp; co.
        </p>
        <h1 className="mx-auto max-w-3xl text-4xl font-extrabold leading-tight md:text-5xl">
          Ne perdez plus jamais un challenge à cause d&apos;une{" "}
          <span className="text-loss">règle oubliée</span>
        </h1>
        <p className="mx-auto mt-5 max-w-2xl text-fg-muted">
          PropDesk surveille votre drawdown trailing, vos soft breaches et votre règle de
          consistance en temps réel — pendant que vous vous concentrez sur le trading.
        </p>
        <div className="mt-8 flex flex-wrap items-center justify-center gap-3">
          <Link href="/signup" className="btn-primary px-6 py-3">
            Créer mon compte gratuit
          </Link>
          <Link href="/login" className="btn-ghost px-6 py-3">
            J&apos;ai déjà un compte
          </Link>
        </div>
        <p className="mt-3 text-xs text-fg-faint">
          Gratuit : 1 compte, 20 trades/mois · Pro 15 €/mois, essai 7 jours
        </p>
      </section>

      {/* Features */}
      <section className="grid gap-4 pb-16 md:grid-cols-3">
        {[
          {
            icon: "◱",
            title: "Drawdown trailing EOD",
            text: "Le floor est recalculé à chaque clôture de journée, exactement comme votre prop firm. Jauge verte / orange / rouge en permanence.",
          },
          {
            icon: "⚠",
            title: "Alerte soft breach",
            text: "Chaque trade est vérifié contre votre seuil de perte max. Le calculateur de sizing vous dit combien de contrats prendre AVANT d'entrer.",
          },
          {
            icon: "％",
            title: "Règle de consistance",
            text: "PropDesk affiche en direct le gain max autorisé sur votre prochain trade pour rester sous les X % du profit total.",
          },
          {
            icon: "⇄",
            title: "Saisie en 10 secondes",
            text: "Entrée, sortie, contrats, stop. C'est tout. P&L, ticks, RRR réel, équity et distances sont calculés automatiquement.",
          },
          {
            icon: "▦",
            title: "Stats qui comptent",
            text: "Win rate (global, 10 et 20 derniers), RRR moyen vs cible, profit factor, courbe d'équity avec floor et objectif.",
          },
          {
            icon: "✦",
            title: "Vos données protégées",
            text: "Isolation par utilisateur au niveau base de données (row level security). Export CSV de tout votre historique en plan Pro.",
          },
        ].map((f) => (
          <div key={f.title} className="card">
            <p className="mb-2 font-mono text-2xl text-accent" aria-hidden>
              {f.icon}
            </p>
            <h2 className="mb-1 font-semibold">{f.title}</h2>
            <p className="text-sm text-fg-muted">{f.text}</p>
          </div>
        ))}
      </section>

      {/* CTA final */}
      <section className="card mb-16 text-center">
        <h2 className="text-2xl font-bold">Votre prochain payout commence par la discipline</h2>
        <p className="mx-auto mt-2 max-w-xl text-sm text-fg-muted">
          Configurez les règles de votre challenge en 2 minutes et laissez PropDesk faire le
          garde-fou.
        </p>
        <div className="mt-6">
          <Link href="/signup" className="btn-primary px-6 py-3">
            Commencer gratuitement
          </Link>
        </div>
      </section>

      <footer className="border-t border-ink-700 py-8 text-center text-xs text-fg-faint">
        © {new Date().getFullYear()} PropDesk — Le trading de futures comporte un risque de perte
        important. PropDesk est un outil de suivi, pas un conseil en investissement.
      </footer>
    </main>
  );
}
