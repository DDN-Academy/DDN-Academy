import { useEffect, useMemo, useRef, useState } from "react";
import { dateCourte, enR, nombre } from "../lib/format";

/** Courbe de résultat cumulé en R (une seule série → pas de légende ; le titre la nomme). */
export function EquityChart({ points, titre }: { points: { date: string; R: number }[]; titre: string }) {
  const [survol, setSurvol] = useState<number | null>(null);
  // La largeur du dessin suit celle du conteneur : le texte garde sa taille réelle sur téléphone.
  const boite = useRef<HTMLElement>(null);
  const [W, setW] = useState(640);
  useEffect(() => {
    const el = boite.current;
    if (!el || typeof ResizeObserver === "undefined") return;
    const ro = new ResizeObserver((e) => setW(Math.max(260, Math.round(e[0].contentRect.width))));
    ro.observe(el);
    return () => ro.disconnect();
  }, [points.length === 0]);
  const H = 220;
  const m = { g: 44, d: 12, h: 12, b: 26 };
  const geo = useMemo(() => {
    const ys = [0, ...points.map((p) => p.R)];
    let min = Math.min(...ys);
    let max = Math.max(...ys);
    if (max - min < 1) {
      max += 0.5;
      min -= 0.5;
    }
    const pad = (max - min) * 0.08;
    min -= pad;
    max += pad;
    const n = points.length;
    // Abscisse 0 = point de départ (0 R) ; puis un pas par trade clôturé.
    const x = (i: number) => m.g + (n === 0 ? 0 : (i / n) * (W - m.g - m.d));
    const y = (v: number) => m.h + ((max - v) / (max - min)) * (H - m.h - m.b);
    const ticks = niceTicks(min, max, 4);
    const d = [`M${x(0)},${y(0)}`, ...points.map((p, i) => `L${x(i + 1)},${y(p.R)}`)].join(" ");
    return { x, y, ticks, d, n };
  }, [points, W]);

  if (points.length === 0) return <p className="muted">Aucun trade simulé clôturé pour l'instant.</p>;
  const sel = survol !== null ? points[survol] : points[points.length - 1];
  const selIdx = survol !== null ? survol : points.length - 1;

  return (
    <figure style={{ margin: 0 }} ref={boite}>
      <figcaption className="sr-only">{titre}</figcaption>
      <div className="chart-tip" aria-live="polite">
        Trade n° {selIdx + 1} ({dateCourte(sel.date)}) : cumul {enR(sel.R)}
      </div>
      <svg
        className="chart"
        viewBox={`0 0 ${W} ${H}`}
        role="img"
        aria-label={`${titre} : ${points.length} trades, cumul final ${enR(points[points.length - 1].R)}`}
        onMouseLeave={() => setSurvol(null)}
        onMouseMove={(e) => {
          const r = (e.currentTarget as SVGSVGElement).getBoundingClientRect();
          const px = ((e.clientX - r.left) / r.width) * W;
          const i = Math.round(((px - m.g) / (W - m.g - m.d)) * geo.n) - 1;
          setSurvol(Math.max(0, Math.min(points.length - 1, i)));
        }}
      >
        {geo.ticks.map((t) => (
          <g key={t}>
            <line className={t === 0 ? "zero-line" : "grid-line"} x1={m.g} x2={W - m.d} y1={geo.y(t)} y2={geo.y(t)} />
            <text x={m.g - 6} y={geo.y(t) + 4} textAnchor="end">
              {nombre(t, Math.abs(t) < 10 && t % 1 !== 0 ? 1 : 0)}
            </text>
          </g>
        ))}
        <text x={m.g} y={H - 6}>
          départ
        </text>
        <text x={W - m.d} y={H - 6} textAnchor="end">
          trade n° {points.length}
        </text>
        <path className="series" d={geo.d} />
        <line className="cross" x1={geo.x(selIdx + 1)} x2={geo.x(selIdx + 1)} y1={m.h} y2={H - m.b} />
        <circle className="dot" cx={geo.x(selIdx + 1)} cy={geo.y(sel.R)} r={5} />
      </svg>
      <details className="json">
        <summary>Voir les valeurs sous forme de tableau</summary>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Trade</th>
                <th>Date</th>
                <th className="n">Cumul</th>
              </tr>
            </thead>
            <tbody>
              {points.map((p, i) => (
                <tr key={i}>
                  <td>{i + 1}</td>
                  <td>{dateCourte(p.date)}</td>
                  <td className="n">{enR(p.R)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </details>
    </figure>
  );
}

function niceTicks(min: number, max: number, count: number): number[] {
  const span = max - min;
  const raw = span / count;
  const mag = Math.pow(10, Math.floor(Math.log10(raw)));
  const step = [1, 2, 2.5, 5, 10].map((k) => k * mag).find((s) => span / s <= count + 1) ?? mag * 10;
  const out: number[] = [];
  for (let v = Math.ceil(min / step) * step; v <= max + 1e-9; v += step) out.push(Math.round(v * 1e6) / 1e6);
  return out;
}
