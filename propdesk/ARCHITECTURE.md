# PropDesk — Architecture

Plateforme de gestion de risque et de suivi de performance pour traders sur
prop firm (comptes futures : FundedNext, Topstep, Apex…).

## 1. Stack

| Couche          | Choix                                   | Pourquoi |
|-----------------|-----------------------------------------|----------|
| Framework       | **Next.js 14 (App Router, TypeScript)** | Front + API routes dans un seul déploiement Vercel |
| UI              | **Tailwind CSS**                        | Thème sombre "terminal de trading", responsive |
| Graphiques      | **Recharts**                            | Courbe d'équity |
| BDD + Auth      | **Supabase** (PostgreSQL)               | Auth email/Google + Row Level Security intégrées |
| Paiements       | **Stripe**                              | Abonnement mensuel, essai 7 jours, portail client |
| Tests           | **Vitest**                              | La logique métier (drawdown, consistance…) est en fonctions pures testées |

## 2. Schéma de base de données

Fichier : [`supabase/schema.sql`](supabase/schema.sql) — à exécuter tel quel
dans le SQL Editor de Supabase.

```
auth.users (géré par Supabase Auth)
    │
    ├── profiles        1—1   profil (email, nom)
    ├── subscriptions   1—1   état Stripe (plan free/pro, status, période, essai)
    └── prop_accounts   1—N   paramètres du challenge :
            │                   account_size, drawdown_limit,
            │                   drawdown_type (trailing_eod | static),
            │                   soft_breach_limit, consistency_pct,
            │                   profit_target, target_rrr,
            │                   instrument par défaut (symbol, tick_size, tick_value)
            └── trades  1—N   saisie minimale :
                                direction, entry_price, exit_price, contracts,
                                stop_ticks, opened_at
                                + snapshot tick_size/tick_value du contrat
```

**Principe clé : on ne stocke que les entrées brutes.** P&L, ticks, RRR,
soft breach, consistance, drawdown, équity… sont recalculés à la volée par
`src/lib/calculations.ts`. Aucune donnée dérivée ne peut donc être incohérente.

### Sécurité (RLS)

- RLS activée sur toutes les tables : `auth.uid() = user_id` sur chaque policy.
- **Les limites du plan gratuit sont appliquées dans la base elle-même**
  (policies d'insertion + fonctions `can_create_account` / `can_create_trade`) :
  1 compte et 20 trades/mois même si quelqu'un appelle l'API Supabase à la main.
- `subscriptions` : lecture seule pour le client ; seules les écritures via la
  clé `service_role` (webhook Stripe, côté serveur) sont possibles.

## 3. Arborescence des fichiers

```
propdesk/
├── ARCHITECTURE.md              ← ce document
├── README.md                    ← déploiement pas à pas + étapes humaines
├── .env.example                 ← toutes les variables d'environnement
├── package.json / tsconfig.json / tailwind.config.ts / next.config.mjs
├── supabase/
│   └── schema.sql               ← tables, triggers, RLS, limites de plan
├── src/
│   ├── middleware.ts            ← refresh session + protection /dashboard
│   ├── lib/
│   │   ├── calculations.ts      ← CŒUR MÉTIER (fonctions pures) :
│   │   │                           P&L, ticks, RRR, soft breach, consistance,
│   │   │                           drawdown trailing EOD / fixe, équity,
│   │   │                           win rate, profit factor, position sizing
│   │   ├── calculations.test.ts ← tests unitaires Vitest
│   │   ├── contracts.ts         ← specs des contrats futures (ES, MNQ, GC…)
│   │   ├── types.ts             ← types partagés (Account, Trade, Subscription)
│   │   ├── plans.ts             ← définition des plans free/pro + helpers
│   │   ├── format.ts            ← formatage monnaie/nombres/dates
│   │   ├── stripe.ts            ← client Stripe serveur
│   │   └── supabase/
│   │       ├── client.ts        ← client navigateur
│   │       ├── server.ts        ← client serveur (cookies) + client admin
│   │       └── middleware.ts    ← helper de session partagé
│   ├── components/
│   │   ├── AppShell.tsx         ← navigation latérale / mobile
│   │   ├── EquityChart.tsx      ← courbe d'équity (Recharts)
│   │   ├── FloorGauge.tsx       ← barre distance au floor (vert/orange/rouge)
│   │   ├── StatCard.tsx, Badge.tsx, ui.tsx (Button, Input, Card…)
│   │   ├── TradeForm.tsx        ← saisie minimale + aperçu calculs en direct
│   │   ├── TradesTable.tsx      ← historique avec alertes par trade
│   │   ├── AccountForm.tsx      ← configuration du challenge
│   │   └── SizingCalculator.tsx ← calculateur de position sizing
│   └── app/
│       ├── layout.tsx / globals.css
│       ├── page.tsx             ← landing page
│       ├── (auth)/login, signup, auth/callback, auth/signout
│       ├── dashboard/
│       │   ├── layout.tsx       ← shell authentifié (fetch user + subscription)
│       │   ├── page.tsx         ← TABLEAU DE BORD temps réel
│       │   ├── accounts/        ← liste + création + édition des comptes
│       │   ├── trades/          ← saisie + historique + export CSV (Pro)
│       │   ├── sizing/          ← calculateur de position sizing
│       │   ├── billing/         ← abonnement (upgrade, portail, annulation)
│       │   └── profile/         ← profil utilisateur
│       └── api/stripe/
│           ├── checkout/route.ts  ← création session Checkout (essai 7 j)
│           ├── portal/route.ts    ← portail de facturation Stripe
│           └── webhook/route.ts   ← sync subscriptions (service_role)
```

## 4. Flux principaux

### Authentification
1. `middleware.ts` rafraîchit la session Supabase sur chaque requête et
   redirige les visiteurs non connectés qui visent `/dashboard/*` vers `/login`.
2. Google OAuth : `signInWithOAuth` → `/auth/callback` (échange du code) → `/dashboard`.
3. À l'inscription, un trigger Postgres crée `profiles` + `subscriptions` (plan free).

### Drawdown trailing EOD (le calcul le plus délicat)
- Le floor démarre à `account_size − drawdown_limit`.
- À chaque **clôture de journée**, si l'équity de fin de journée dépasse le
  plus haut EOD précédent, le floor remonte d'autant (ratchet **vers le haut
  uniquement**, jamais vers le bas).
- Le floor cesse de monter une fois arrivé à `account_size` (compte sécurisé),
  comportement standard FundedNext/Topstep.
- Mode `static` : floor fixe à `account_size − drawdown_limit`.

### Règle de consistance
- Un trade (jour de gain) ne doit pas dépasser `consistency_pct` % du profit
  cumulé. Le dashboard affiche le **gain max autorisé sur le prochain trade** :
  `g ≤ p × (profit_cumulé + g)` ⇒ `g_max = p × profit_cumulé ÷ (1 − p)`.

### Stripe
1. `/api/stripe/checkout` crée une session Checkout (mode subscription,
   `trial_period_days: 7`) liée à l'utilisateur via `client_reference_id`.
2. Le webhook (`checkout.session.completed`, `customer.subscription.updated/
   deleted`) écrit dans `subscriptions` avec la clé service_role.
3. Le gating (nb de comptes, trades/mois, export CSV) lit `subscriptions` —
   et il est doublé par les policies RLS côté base.

## 5. Prévu pour la V2 (architecture prête, non codé)

- **Détecteur de biais** : les trades bruts horodatés sont déjà stockés ;
  un module `lib/behavior.ts` pourra analyser revenge trading / overtrading
  sans migration de schéma.
- **Briefing quotidien / rapport hebdo** : cron Vercel + les mêmes fonctions
  pures de `calculations.ts`.
- **Import CSV Tradovate** : mapping vers le même modèle `TradeInput`.
- **Multi-langue** : les libellés UI sont centralisés, prêt pour next-intl.
