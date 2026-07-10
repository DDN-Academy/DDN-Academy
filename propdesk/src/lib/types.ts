/**
 * Types partagés — miroir des tables Supabase (voir supabase/schema.sql).
 */

export type DrawdownType = "trailing_eod" | "static";
export type TradeDirection = "long" | "short";
export type PlanType = "free" | "pro";

export interface Profile {
  id: string;
  email: string;
  full_name: string | null;
  created_at: string;
  updated_at: string;
}

export interface PropAccount {
  id: string;
  user_id: string;
  name: string;
  firm: string | null;
  account_size: number;
  drawdown_limit: number;
  drawdown_type: DrawdownType;
  soft_breach_limit: number;
  consistency_pct: number; // ex : 40 (en %)
  profit_target: number;
  target_rrr: number;
  default_symbol: string;
  default_tick_size: number;
  default_tick_value: number;
  created_at: string;
  updated_at: string;
}

export interface Trade {
  id: string;
  user_id: string;
  account_id: string;
  direction: TradeDirection;
  entry_price: number;
  exit_price: number;
  contracts: number;
  stop_ticks: number;
  symbol: string;
  tick_size: number;
  tick_value: number;
  opened_at: string; // ISO
  notes: string | null;
  created_at: string;
}

export interface Subscription {
  user_id: string;
  plan: PlanType;
  status: string;
  stripe_customer_id: string | null;
  stripe_subscription_id: string | null;
  current_period_end: string | null;
  trial_end: string | null;
  cancel_at_period_end: boolean;
  created_at: string;
  updated_at: string;
}
