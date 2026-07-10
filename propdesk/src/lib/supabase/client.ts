/**
 * Client Supabase côté NAVIGATEUR (composants "use client").
 * Utilise la clé anon : toutes les requêtes passent par les policies RLS.
 */
import { createBrowserClient } from "@supabase/ssr";

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
  );
}
