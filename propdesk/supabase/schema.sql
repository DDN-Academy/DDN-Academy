-- ============================================================================
-- PropDesk — Schéma de base de données Supabase (PostgreSQL)
-- ============================================================================
-- À exécuter dans : Dashboard Supabase > SQL Editor > New query > coller > Run
--
-- Tables :
--   profiles       — profil utilisateur (miroir de auth.users)
--   prop_accounts  — paramètres du challenge prop firm (drawdown, consistance…)
--   trades         — trades saisis (input minimal, le reste est calculé)
--   subscriptions  — état de l'abonnement Stripe (écrit par le webhook)
--
-- Sécurité :
--   * Row Level Security activée sur TOUTES les tables : chaque utilisateur
--     ne voit et ne modifie que ses propres lignes.
--   * Les limites du plan gratuit (1 compte, 20 trades/mois) sont appliquées
--     AU NIVEAU BASE via les policies d'insertion — impossible de les
--     contourner même en appelant l'API Supabase directement.
--   * La table subscriptions n'est modifiable que par la clé service_role
--     (webhook Stripe) ; les clients ne peuvent que la lire.
-- ============================================================================

-- ── Types énumérés ──────────────────────────────────────────────────────────
create type public.drawdown_type as enum ('trailing_eod', 'static');
create type public.trade_direction as enum ('long', 'short');
create type public.plan_type as enum ('free', 'pro');

-- ============================================================================
-- 1. PROFILES
-- ============================================================================
create table public.profiles (
  id          uuid primary key references auth.users (id) on delete cascade,
  email       text not null,
  full_name   text,
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);

alter table public.profiles enable row level security;

create policy "profiles: read own"
  on public.profiles for select
  using (auth.uid() = id);

create policy "profiles: update own"
  on public.profiles for update
  using (auth.uid() = id)
  with check (auth.uid() = id);

-- Création automatique du profil à l'inscription (email ou Google)
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer set search_path = public
as $$
begin
  insert into public.profiles (id, email, full_name)
  values (
    new.id,
    new.email,
    coalesce(new.raw_user_meta_data ->> 'full_name', new.raw_user_meta_data ->> 'name')
  )
  on conflict (id) do nothing;

  -- Chaque nouvel utilisateur démarre sur le plan gratuit
  insert into public.subscriptions (user_id, plan, status)
  values (new.id, 'free', 'active')
  on conflict (user_id) do nothing;

  return new;
end;
$$;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

-- ============================================================================
-- 2. SUBSCRIPTIONS (déclarée avant prop_accounts/trades car les policies
--    de limites du plan gratuit s'appuient dessus)
-- ============================================================================
create table public.subscriptions (
  user_id                 uuid primary key references auth.users (id) on delete cascade,
  plan                    public.plan_type not null default 'free',
  status                  text not null default 'active', -- active | trialing | past_due | canceled …
  stripe_customer_id      text unique,
  stripe_subscription_id  text unique,
  current_period_end      timestamptz,
  trial_end               timestamptz,
  cancel_at_period_end    boolean not null default false,
  created_at              timestamptz not null default now(),
  updated_at              timestamptz not null default now()
);

alter table public.subscriptions enable row level security;

-- Les clients lisent leur abonnement ; seules les écritures service_role
-- (webhook Stripe) sont possibles — aucune policy insert/update côté client.
create policy "subscriptions: read own"
  on public.subscriptions for select
  using (auth.uid() = user_id);

-- L'utilisateur est-il Pro (abonnement actif ou en période d'essai) ?
create or replace function public.is_pro(uid uuid)
returns boolean
language sql
security definer set search_path = public
stable
as $$
  select exists (
    select 1 from public.subscriptions
    where user_id = uid
      and plan = 'pro'
      and status in ('active', 'trialing')
  );
$$;

-- ============================================================================
-- 3. PROP_ACCOUNTS — paramètres du challenge
-- ============================================================================
create table public.prop_accounts (
  id                 uuid primary key default gen_random_uuid(),
  user_id            uuid not null references auth.users (id) on delete cascade,
  name               text not null,                        -- ex : "FundedNext 50K"
  firm               text,                                 -- ex : "FundedNext", "Topstep"
  account_size       numeric(14,2) not null check (account_size > 0),        -- ex : 50000
  drawdown_limit     numeric(14,2) not null check (drawdown_limit > 0),      -- ex : 2000
  drawdown_type      public.drawdown_type not null default 'trailing_eod',
  soft_breach_limit  numeric(14,2) not null check (soft_breach_limit > 0),   -- ex : 1000 (perte max/trade)
  consistency_pct    numeric(5,2)  not null check (consistency_pct > 0 and consistency_pct <= 100), -- ex : 40
  profit_target      numeric(14,2) not null check (profit_target > 0),       -- ex : 3000
  target_rrr         numeric(6,2)  not null default 2 check (target_rrr > 0),-- RRR cible pour les stats
  default_symbol     text not null default 'MNQ',          -- instrument par défaut
  default_tick_size  numeric(12,6) not null default 0.25 check (default_tick_size > 0),
  default_tick_value numeric(12,4) not null default 0.5  check (default_tick_value > 0), -- $ par tick par contrat
  created_at         timestamptz not null default now(),
  updated_at         timestamptz not null default now()
);

create index prop_accounts_user_idx on public.prop_accounts (user_id);

alter table public.prop_accounts enable row level security;

-- Limite plan gratuit : 1 seul compte prop firm
create or replace function public.can_create_account(uid uuid)
returns boolean
language sql
security definer set search_path = public
stable
as $$
  select public.is_pro(uid)
      or (select count(*) from public.prop_accounts where user_id = uid) < 1;
$$;

create policy "prop_accounts: read own"
  on public.prop_accounts for select
  using (auth.uid() = user_id);

create policy "prop_accounts: insert own within plan limits"
  on public.prop_accounts for insert
  with check (auth.uid() = user_id and public.can_create_account(auth.uid()));

create policy "prop_accounts: update own"
  on public.prop_accounts for update
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

create policy "prop_accounts: delete own"
  on public.prop_accounts for delete
  using (auth.uid() = user_id);

-- ============================================================================
-- 4. TRADES — saisie minimale, tout le reste est calculé côté app
-- ============================================================================
create table public.trades (
  id           uuid primary key default gen_random_uuid(),
  user_id      uuid not null references auth.users (id) on delete cascade,
  account_id   uuid not null references public.prop_accounts (id) on delete cascade,
  direction    public.trade_direction not null,
  entry_price  numeric(14,4) not null check (entry_price > 0),
  exit_price   numeric(14,4) not null check (exit_price > 0),
  contracts    integer not null check (contracts > 0),
  stop_ticks   integer not null check (stop_ticks > 0),
  symbol       text not null,
  -- Snapshot des specs du contrat AU MOMENT du trade : si l'utilisateur
  -- change l'instrument par défaut du compte plus tard, l'historique
  -- reste correct.
  tick_size    numeric(12,6) not null check (tick_size > 0),
  tick_value   numeric(12,4) not null check (tick_value > 0),
  opened_at    timestamptz not null default now(),
  notes        text,
  created_at   timestamptz not null default now()
);

create index trades_user_idx    on public.trades (user_id);
create index trades_account_idx on public.trades (account_id, opened_at);

alter table public.trades enable row level security;

-- Limite plan gratuit : 20 trades par mois calendaire (UTC)
create or replace function public.can_create_trade(uid uuid)
returns boolean
language sql
security definer set search_path = public
stable
as $$
  select public.is_pro(uid)
      or (
        select count(*) from public.trades
        where user_id = uid
          and created_at >= date_trunc('month', now())
      ) < 20;
$$;

create policy "trades: read own"
  on public.trades for select
  using (auth.uid() = user_id);

create policy "trades: insert own within plan limits"
  on public.trades for insert
  with check (
    auth.uid() = user_id
    and public.can_create_trade(auth.uid())
    -- Le trade doit pointer vers un compte appartenant à l'utilisateur
    and exists (
      select 1 from public.prop_accounts a
      where a.id = account_id and a.user_id = auth.uid()
    )
  );

create policy "trades: update own"
  on public.trades for update
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

create policy "trades: delete own"
  on public.trades for delete
  using (auth.uid() = user_id);

-- ============================================================================
-- 5. updated_at automatique
-- ============================================================================
create or replace function public.touch_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

create trigger profiles_touch      before update on public.profiles      for each row execute function public.touch_updated_at();
create trigger prop_accounts_touch before update on public.prop_accounts for each row execute function public.touch_updated_at();
create trigger subscriptions_touch before update on public.subscriptions for each row execute function public.touch_updated_at();
