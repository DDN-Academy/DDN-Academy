# PropDesk

**Plateforme de gestion de risque et de suivi de performance pour traders sur
prop firm** (comptes futures : FundedNext, Topstep, Apex…).

PropDesk aide à respecter les règles du challenge — drawdown trailing EOD,
soft breach par trade, règle de consistance — et à suivre ses performances :
courbe d'équity, win rate, RRR moyen, profit factor, calculateur de position
sizing.

📐 Architecture détaillée : [ARCHITECTURE.md](ARCHITECTURE.md)
🗃️ Schéma de base de données : [supabase/schema.sql](supabase/schema.sql)

---

## Stack

- **Next.js 14** (App Router, TypeScript) — front + API dans un seul déploiement
- **Tailwind CSS** — thème sombre "terminal de trading", responsive mobile/desktop
- **Supabase** — PostgreSQL + Auth (email/mot de passe + Google) + Row Level Security
- **Stripe** — abonnement Pro 15 €/mois avec essai gratuit 7 jours
- **Recharts** — courbe d'équity
- **Vitest** — tests unitaires de la logique métier (`npm test`)

## Fonctionnalités (MVP)

| | Gratuit | Pro (15 €/mois, essai 7 j) |
|---|---|---|
| Comptes prop firm | 1 | Illimités |
| Trades | 20 / mois | Illimités |
| Dashboard temps réel | ✓ | ✓ |
| Calculateur de sizing | ✓ | ✓ |
| Export CSV | — | ✓ |

Les limites du plan gratuit sont appliquées **au niveau de la base de données**
(policies RLS) : impossible de les contourner via l'API.

---

## 🚀 Déploiement pas à pas

### Étape 0 — Prérequis

- Node.js ≥ 18.18 et npm
- Un compte GitHub (pour le déploiement Vercel)

```bash
cd propdesk
npm install
cp .env.example .env.local   # puis remplir les clés au fil des étapes suivantes
```

### Étape 1 — Supabase (base de données + authentification) 🧑‍💻 INTERVENTION HUMAINE

1. Créez un compte sur [supabase.com](https://supabase.com) puis **New project**
   (choisissez une région proche de vos utilisateurs, notez le mot de passe DB).
2. Dans **SQL Editor → New query**, collez tout le contenu de
   [`supabase/schema.sql`](supabase/schema.sql) et cliquez **Run**.
   → crée les tables `profiles`, `prop_accounts`, `trades`, `subscriptions`,
   les triggers et toutes les policies RLS.
3. Dans **Project Settings → API**, récupérez et mettez dans `.env.local` :
   - `Project URL` → `NEXT_PUBLIC_SUPABASE_URL`
   - `anon public` → `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - `service_role` → `SUPABASE_SERVICE_ROLE_KEY` ⚠️ secrète, jamais côté client
4. **Auth email** : Authentication → Providers → Email est activé par défaut.
   (Optionnel : désactivez "Confirm email" pour tester plus vite.)
5. **Auth Google** 🧑‍💻 :
   1. [console.cloud.google.com](https://console.cloud.google.com) → créez un
      projet → **APIs & Services → Credentials → Create OAuth client ID**
      (type *Web application*).
   2. "Authorized redirect URI" : `https://<votre-ref>.supabase.co/auth/v1/callback`
      (affichée dans Supabase → Authentication → Providers → Google).
   3. Copiez le **Client ID** et le **Client Secret** dans Supabase →
      Authentication → Providers → Google → Enable.
6. **URLs de redirection** : Authentication → URL Configuration →
   - Site URL : `http://localhost:3000` (puis votre domaine en prod)
   - Redirect URLs : ajoutez `http://localhost:3000/auth/callback` et
     `https://votre-domaine.com/auth/callback`

### Étape 2 — Stripe (paiements) 🧑‍💻 INTERVENTION HUMAINE

1. Créez un compte sur [stripe.com](https://stripe.com) (restez en **mode Test**
   pour l'instant).
2. **Produit** : Product catalog → **Add product** :
   - Nom : `PropDesk Pro`
   - Prix : `15,00 €` / mois, récurrent
   - Copiez le **Price ID** (`price_…`) → `STRIPE_PRICE_ID_PRO`
3. **Clés API** : Developers → API keys :
   - `Secret key` (`sk_test_…`) → `STRIPE_SECRET_KEY`
   - `Publishable key` (`pk_test_…`) → `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`
4. **Webhook** : Developers → Webhooks → **Add endpoint** :
   - URL : `https://votre-domaine.com/api/stripe/webhook`
     (en local : `stripe listen --forward-to localhost:3000/api/stripe/webhook`
     avec la [CLI Stripe](https://stripe.com/docs/stripe-cli))
   - Événements : `checkout.session.completed`,
     `customer.subscription.updated`, `customer.subscription.deleted`
   - Copiez le **Signing secret** (`whsec_…`) → `STRIPE_WEBHOOK_SECRET`
5. **Portail client** : Settings → Billing → Customer portal → **Activate**
   (permet à vos clients d'annuler / changer de carte eux-mêmes).

### Étape 3 — Lancer en local

```bash
npm run dev        # http://localhost:3000
npm test           # tests unitaires de la logique métier
npm run build      # vérification production
```

Parcours de test complet : inscription → configuration d'un compte
(50 000 $ / DD 2 000 $ / soft breach 1 000 $ / consistance 40 % / objectif
3 000 $) → saisie de quelques trades → dashboard → upgrade Pro avec la carte
de test Stripe `4242 4242 4242 4242` (n'importe quelle date future / CVC).

### Étape 4 — Vercel (hébergement) 🧑‍💻 INTERVENTION HUMAINE

1. Poussez ce dossier dans un dépôt GitHub.
2. Créez un compte sur [vercel.com](https://vercel.com) → **Add New → Project**
   → importez le dépôt.
   - **Root Directory : `propdesk`** (si le dossier n'est pas à la racine du dépôt)
   - Framework : Next.js (auto-détecté)
3. Dans **Settings → Environment Variables**, ajoutez TOUTES les variables de
   `.env.example` avec leurs vraies valeurs, dont
   `NEXT_PUBLIC_SITE_URL=https://votre-domaine.com`.
4. **Deploy**. Ensuite :
   - mettez à jour l'URL du webhook Stripe avec l'URL Vercel définitive ;
   - ajoutez l'URL Vercel dans les Redirect URLs Supabase (étape 1.6).

### Étape 5 — Nom de domaine 🧑‍💻 INTERVENTION HUMAINE

1. Achetez un domaine (Namecheap, OVH, Cloudflare…).
2. Vercel → Settings → Domains → ajoutez le domaine et suivez les
   instructions DNS (CNAME → `cname.vercel-dns.com`).
3. Mettez à jour `NEXT_PUBLIC_SITE_URL`, la Site URL Supabase et l'endpoint
   webhook Stripe avec le domaine final.

### Étape 6 — Passage en paiements réels 🧑‍💻 INTERVENTION HUMAINE

1. Stripe → activez votre compte (KYC : identité, IBAN).
2. Basculez en **mode Live** : recréez le produit/prix, récupérez les clés
   live (`sk_live_…`, `pk_live_…`, nouveau `whsec_…`) et remplacez-les dans
   Vercel.
3. Faites un vrai paiement de bout en bout (vous pouvez vous rembourser
   depuis le dashboard Stripe), vérifiez que la ligne `subscriptions` passe
   bien en `pro / trialing`.

---

## ✅ Récapitulatif des étapes nécessitant une intervention humaine

1. **Supabase** : création du compte + projet, exécution de `schema.sql`,
   récupération des 3 clés, configuration Google OAuth (console Google Cloud),
   URLs de redirection.
2. **Stripe** : création du compte, produit + prix Pro, clés API, endpoint
   webhook + signing secret, activation du portail client.
3. **Vercel** : création du compte, import du dépôt GitHub, saisie des
   variables d'environnement, déploiement.
4. **Nom de domaine** : achat + configuration DNS + mise à jour des URLs
   (Vercel, Supabase, Stripe, `NEXT_PUBLIC_SITE_URL`).
5. **Paiements réels** : KYC Stripe, bascule des clés test → live, test d'un
   paiement réel de bout en bout.

---

## Sécurité

- **Aucune clé en dur** : tout passe par les variables d'environnement
  (`.env.local` est ignoré par git).
- **RLS partout** : chaque utilisateur ne peut lire/écrire que ses lignes ;
  les limites du plan gratuit sont des policies SQL.
- La clé `service_role` n'est utilisée que dans le webhook Stripe (serveur).
- Le webhook Stripe vérifie la **signature** de chaque événement.
- Déconnexion en POST, redirections OAuth restreintes aux chemins internes.

## Structure du code

Voir [ARCHITECTURE.md](ARCHITECTURE.md). L'essentiel :

- `src/lib/calculations.ts` — tous les calculs (P&L, drawdown trailing,
  consistance, sizing, stats) en fonctions pures **testées** (`npm test`).
- `src/app/dashboard/*` — pages authentifiées (dashboard, trades, comptes,
  sizing, abonnement, profil).
- `src/app/api/stripe/*` — checkout, portail, webhook.
- `supabase/schema.sql` — la base complète, RLS incluse.

## V2 (architecture prête)

Détecteur de biais comportementaux, briefing quotidien, rapport hebdo PDF,
import CSV Tradovate, multi-langue FR/EN — voir la section dédiée dans
[ARCHITECTURE.md](ARCHITECTURE.md).
