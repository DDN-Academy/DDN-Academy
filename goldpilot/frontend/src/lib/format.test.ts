import { describe, expect, it } from "vitest";
import { decalageMinutes, duree, enR, ilYa, nombre, pct, prix, signe, texteBrut, usd, versIsoAvecFuseau } from "./format";

// Intl fr-FR sépare les milliers par une espace fine insécable (U+202F) ; on normalise pour les comparaisons.
const n = (s: string) => s.replace(/[  ]/g, " ");

describe("formatage français", () => {
  it("virgule décimale et espaces de milliers", () => {
    expect(n(nombre(3583.27))).toBe("3 583,27");
    expect(n(nombre(1234567.891, 1))).toBe("1 234 567,9");
    expect(n(prix(49880.983))).toBe("49 880,98");
  });
  it("signe moins typographique et jamais « −0 »", () => {
    expect(nombre(-1.5, 1)).toBe("−1,5");
    expect(nombre(-0.001, 2)).toBe("0,00");
    expect(signe(0.0807, 3)).toBe("+0,081");
    expect(signe(-0.0193, 3)).toBe("−0,019");
  });
  it("dollars après le nombre", () => {
    expect(n(usd(1500))).toBe("1 500 $");
    expect(n(usd(-221.07, 0, true))).toBe("−221 $");
    expect(n(usd(145.9, 0, true))).toBe("+146 $");
  });
  it("R et pourcentages", () => {
    expect(n(enR(-1.0432))).toBe("−1,04 R");
    expect(n(pct(0.1071))).toBe("10,7 %");
    expect(n(pct(0.0001, 2))).toBe("0,01 %");
  });
  it("valeurs absentes", () => {
    expect(nombre(null)).toBe("—");
    expect(usd(undefined)).toBe("—");
    expect(pct(Number.NaN)).toBe("—");
  });
  it("durées", () => {
    expect(n(duree(42))).toBe("42 s");
    expect(n(duree(-299))).toBe("0 s");
    expect(n(duree(185))).toBe("3 min");
    expect(n(duree(2 * 3600 + 5 * 60))).toBe("2 h 05");
    expect(n(ilYa(12))).toBe("il y a 12 s");
    expect(ilYa(0.2)).toBe("à l'instant");
  });
});

describe("texte des notifications", () => {
  it("retire les balises et décode les entités sans interpréter de HTML", () => {
    expect(texteBrut("<b>SIMULATION</b> stop (barre d&#x27;entrée) &amp; <script>x</script>")).toBe("SIMULATION stop (barre d'entrée) & x");
  });
});

describe("fuseaux horaires", () => {
  it("heure d'été / d'hiver de New York et Paris", () => {
    expect(versIsoAvecFuseau("2026-10-14", "08:30", "America/New_York")).toBe("2026-10-14T08:30:00-04:00");
    expect(versIsoAvecFuseau("2026-12-14", "08:30", "America/New_York")).toBe("2026-12-14T08:30:00-05:00");
    expect(versIsoAvecFuseau("2026-07-01", "14:30", "Europe/Paris")).toBe("2026-07-01T14:30:00+02:00");
    expect(versIsoAvecFuseau("2026-01-15", "14:30", "UTC")).toBe("2026-01-15T14:30:00+00:00");
  });
  it("refuse une saisie invalide", () => {
    expect(versIsoAvecFuseau("2026-13-01", "08:30", "UTC")).toBeNull();
    expect(versIsoAvecFuseau("", "08:30", "UTC")).toBeNull();
    expect(versIsoAvecFuseau("2026-01-01", "8h", "UTC")).toBeNull();
  });
  it("décalage", () => {
    expect(decalageMinutes(Date.UTC(2026, 0, 15, 12), "Europe/Paris")).toBe(60);
  });
});
