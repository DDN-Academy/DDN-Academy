import type { Metadata } from "next";
import { redirect } from "next/navigation";
import { createClient } from "@/lib/supabase/server";
import ProfileForm from "@/components/ProfileForm";
import type { Profile } from "@/lib/types";

export const metadata: Metadata = { title: "Profil" };

export default async function ProfilePage() {
  const supabase = createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) redirect("/login");

  const { data: profile } = await supabase
    .from("profiles")
    .select("*")
    .eq("id", user.id)
    .maybeSingle<Profile>();

  return (
    <div className="max-w-lg">
      <h1 className="mb-6 text-2xl font-bold">Profil</h1>
      <ProfileForm
        email={user.email ?? ""}
        fullName={profile?.full_name ?? ""}
        createdAt={user.created_at}
        provider={user.app_metadata?.provider ?? "email"}
      />
    </div>
  );
}
