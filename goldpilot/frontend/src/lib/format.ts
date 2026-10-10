// Mise en forme française : virgule décimale, espace (insécable fine) pour les milliers, « $ » après le nombre.

const NBSP = " ";
const VIDE = "—";

const cache = new Map<string, Intl.NumberFormat>();
function nf(min: number, max: number): Intl.NumberFormat {
  const k = `${min}-${max}`;
  let f = cache.get(k);
  if (!f) {
    f = new Intl.NumberFormat("fr-FR", { minimumFractionDigits: min, maximumFractionDigits: max });
    cache.set(k, f);
  }
  return f;
}

export function estNombre(x: unknown): x is number {
  return typeof x === "number" && Number.isFinite(x);
}

/** 3583.27 → « 3 583,27 » (décimales fixes). */
export function nombre(x: number | null | undefined, decimales = 2): string {
  if (!estNombre(x)) return VIDE;
  const s = nf(decimales, decimales).format(Math.abs(x));
  // Signe moins typographique (U+2212) ; jamais « −0,00 ».
  return x < 0 && /[1-9]/.test(s) ? "−" + s : s;
}

/** Nombre avec signe explicite : +0,08 / −1,04. */
export function signe(x: number | null | undefined, decimales = 2): string {
  if (!estNombre(x)) return VIDE;
  const s = nombre(Math.abs(x), decimales);
  if (s === nombre(0, decimales)) return s;
  return (x < 0 ? "−" : "+") + s;
}

/** Montant en dollars : « 1 500 $ », « −221 $ ». */
export function usd(x: number | null | undefined, decimales = 0, avecSigne = false): string {
  if (!estNombre(x)) return VIDE;
  const s = avecSigne ? signe(x, decimales) : nombre(x, decimales);
  return `${s}${NBSP}$`;
}

/** Résultat en unités de risque : « +0,08 R ». */
export function enR(x: number | null | undefined, decimales = 2, avecSigne = true): string {
  if (!estNombre(x)) return VIDE;
  return `${avecSigne ? signe(x, decimales) : nombre(x, decimales)}${NBSP}R`;
}

/** Proportion (0..1) en pourcentage : 0.1071 → « 10,7 % ». */
export function pct(p: number | null | undefined, decimales = 1): string {
  if (!estNombre(p)) return VIDE;
  return `${nombre(p * 100, decimales)}${NBSP}%`;
}

/** Prix de l'or (2 décimales). */
export function prix(x: number | null | undefined): string {
  return nombre(x, 2);
}

/** Entier avec séparateur de milliers. */
export function entier(x: number | null | undefined): string {
  return nombre(x, 0);
}

/** Durée lisible : 42 s, 3 min, 2 h 05, 3 j 4 h. */
export function duree(secondes: number | null | undefined): string {
  if (!estNombre(secondes)) return VIDE;
  const s = Math.max(0, Math.round(secondes));
  if (s < 60) return `${s}${NBSP}s`;
  const m = Math.floor(s / 60);
  if (m < 60) return `${m}${NBSP}min`;
  const h = Math.floor(m / 60);
  if (h < 48) return `${h}${NBSP}h${NBSP}${String(m % 60).padStart(2, "0")}`;
  const j = Math.floor(h / 24);
  return `${j}${NBSP}j${NBSP}${h % 24}${NBSP}h`;
}

/** « il y a 12 s », « à l'instant ». */
export function ilYa(secondes: number | null | undefined): string {
  if (!estNombre(secondes)) return VIDE;
  if (secondes < 1) return "à l'instant";
  return `il y a ${duree(secondes)}`;
}

/** Date-heure ISO → « 10/09/2025 22:05 » à l'heure de Paris (ou du fuseau demandé). */
export function dateHeure(iso: string | null | undefined, fuseau = "Europe/Paris"): string {
  if (!iso) return VIDE;
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return VIDE;
  return new Intl.DateTimeFormat("fr-FR", {
    timeZone: fuseau,
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(d);
}

/** « 2026-10-09 » → « 09/10/2026 ». */
export function dateCourte(isoDate: string | null | undefined): string {
  if (!isoDate) return VIDE;
  const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(isoDate);
  return m ? `${m[3]}/${m[2]}/${m[1]}` : isoDate;
}

/** Secondes écoulées entre une date ISO et maintenant (null si invalide). */
export function ageSecondes(iso: string | null | undefined, maintenant = Date.now()): number | null {
  if (!iso) return null;
  const t = new Date(iso).getTime();
  return Number.isNaN(t) ? null : (maintenant - t) / 1000;
}

const ENTITES: Record<string, string> = { amp: "&", lt: "<", gt: ">", quot: '"', apos: "'", nbsp: NBSP, "#x27": "'", "#39": "'" };

/** Texte d'une notification Telegram (HTML simple) → texte brut, sans jamais injecter de HTML. */
export function texteBrut(html: string | null | undefined): string {
  if (!html) return "";
  return html
    .replace(/<br\s*\/?>/gi, "\n")
    .replace(/<[^>]*>/g, "")
    .replace(/&(#x[0-9a-f]+|#\d+|[a-z]+);/gi, (m, e: string) => {
      const k = e.toLowerCase();
      if (ENTITES[k] !== undefined) return ENTITES[k];
      if (k.startsWith("#x")) return String.fromCodePoint(parseInt(k.slice(2), 16));
      if (k.startsWith("#")) return String.fromCodePoint(parseInt(k.slice(1), 10));
      return m;
    });
}

/**
 * Date + heure saisies dans un fuseau donné → ISO 8601 avec décalage (ex. « 2026-10-14T08:30:00-04:00 »).
 * Le décalage est calculé par le navigateur (base IANA), changements d'heure compris.
 */
export function versIsoAvecFuseau(date: string, heure: string, fuseau: string): string | null {
  const md = /^(\d{4})-(\d{2})-(\d{2})$/.exec(date);
  const mh = /^(\d{2}):(\d{2})$/.exec(heure);
  if (!md || !mh) return null;
  const [y, mo, d] = [Number(md[1]), Number(md[2]), Number(md[3])];
  const [h, mi] = [Number(mh[1]), Number(mh[2])];
  if (mo < 1 || mo > 12 || d < 1 || d > 31 || h > 23 || mi > 59) return null;
  const naif = Date.UTC(y, mo - 1, d, h, mi);
  // Deux passes : le décalage est celui de l'instant réel, pas de l'instant « naïf ».
  let off = decalageMinutes(naif, fuseau);
  off = decalageMinutes(naif - off * 60000, fuseau);
  const signeOff = off >= 0 ? "+" : "-";
  const a = Math.abs(off);
  const hh = String(Math.floor(a / 60)).padStart(2, "0");
  const mm = String(a % 60).padStart(2, "0");
  return `${md[1]}-${md[2]}-${md[3]}T${mh[1]}:${mh[2]}:00${signeOff}${hh}:${mm}`;
}

/** Décalage (minutes) du fuseau par rapport à UTC à l'instant donné. */
export function decalageMinutes(instantMs: number, fuseau: string): number {
  const parts = new Intl.DateTimeFormat("en-US", {
    timeZone: fuseau,
    hourCycle: "h23",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  }).formatToParts(new Date(instantMs));
  const g = (t: string) => Number(parts.find((p) => p.type === t)?.value);
  const local = Date.UTC(g("year"), g("month") - 1, g("day"), g("hour"), g("minute"));
  return Math.round((local - Math.floor(instantMs / 60000) * 60000) / 60000);
}
