import type { Metadata } from "next";
import Link from "next/link";
import AuthForm from "@/components/AuthForm";

export const metadata: Metadata = { title: "Inscription" };

export default function SignupPage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-6 p-4">
      <Link href="/" className="font-mono text-lg font-bold tracking-tight">
        Prop<span className="text-accent">Desk</span>
      </Link>
      <AuthForm mode="signup" />
    </main>
  );
}
