import { duree } from "./format";

/** Réception jugée vérifiée seulement si TradingView est la source, que des webhooks ont été acceptés et que les données sont fraîches. */
export function etatReceptionTradingView(
  source: string,
  webhooksAcceptes: number,
  donneesOk: boolean | null,
  ageS: number | null,
): { ton: "ok" | "warn" | "bad" | "neutral"; texte: string } {
  if (source !== "tradingview") return { ton: "neutral", texte: `TradingView n'est pas la source de données actuelle (source : ${source}).` };
  if (webhooksAcceptes === 0) return { ton: "bad", texte: "Non connecté : aucun webhook TradingView accepté n'a été reçu." };
  if (donneesOk && ageS !== null && ageS <= 180) return { ton: "ok", texte: `Réception vérifiée : dernière barre reçue il y a ${duree(Math.max(0, ageS))}.` };
  return { ton: "warn", texte: "Des webhooks ont été reçus, mais aucune donnée récente : réception non vérifiée actuellement (marché fermé ou alerte arrêtée ?)." };
}

