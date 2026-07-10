"use client";

/**
 * Courbe d'équity (Recharts) : équity après chaque trade + ligne du floor.
 */
import {
  Area,
  CartesianGrid,
  Line,
  ComposedChart,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { fmtMoney } from "@/lib/format";

interface Point {
  index: number;
  date: string;
  equity: number;
  floor: number;
}

export default function EquityChart({
  data,
  accountSize,
  profitTarget,
}: {
  data: Point[];
  accountSize: number;
  profitTarget: number;
}) {
  const target = accountSize + profitTarget;
  const min = Math.min(...data.map((d) => Math.min(d.equity, d.floor)));
  const max = Math.max(target, ...data.map((d) => d.equity));
  const pad = Math.max((max - min) * 0.05, 100);

  return (
    <div className="card">
      <p className="mb-4 text-xs font-medium uppercase tracking-wider text-fg-muted">
        Courbe d&apos;équity
      </p>
      <div className="h-64 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={data} margin={{ top: 5, right: 8, bottom: 0, left: 8 }}>
            <defs>
              <linearGradient id="equityFill" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#4f8cff" stopOpacity={0.25} />
                <stop offset="100%" stopColor="#4f8cff" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid stroke="#1b2230" strokeDasharray="3 3" vertical={false} />
            <XAxis
              dataKey="index"
              tick={{ fill: "#5b6478", fontSize: 11 }}
              tickLine={false}
              axisLine={{ stroke: "#1b2230" }}
              label={{ value: "Trades", fill: "#5b6478", fontSize: 11, dy: 12 }}
              height={36}
            />
            <YAxis
              domain={[min - pad, max + pad]}
              tick={{ fill: "#5b6478", fontSize: 11 }}
              tickLine={false}
              axisLine={false}
              tickFormatter={(v: number) => `$${Math.round(v / 100) / 10}k`}
              width={52}
            />
            <Tooltip
              contentStyle={{
                background: "#0b0e14",
                border: "1px solid #1b2230",
                borderRadius: 8,
                fontSize: 12,
                fontFamily: "monospace",
              }}
              labelFormatter={(i) => (Number(i) === 0 ? "Départ" : `Trade #${i}`)}
              formatter={(value: number, name: string) => [
                fmtMoney(value),
                name === "equity" ? "Équity" : "Floor",
              ]}
            />
            {/* Objectif de profit */}
            <ReferenceLine
              y={target}
              stroke="#2fdc8b"
              strokeDasharray="6 4"
              label={{ value: "Objectif", fill: "#2fdc8b", fontSize: 10, position: "insideTopRight" }}
            />
            {/* Floor de drawdown (trailing → en escalier) */}
            <Line
              type="stepAfter"
              dataKey="floor"
              stroke="#ff5c5c"
              strokeDasharray="4 4"
              strokeWidth={1.5}
              dot={false}
              activeDot={false}
              isAnimationActive={false}
            />
            <Area
              type="monotone"
              dataKey="equity"
              stroke="#4f8cff"
              strokeWidth={2}
              fill="url(#equityFill)"
              dot={false}
              isAnimationActive={false}
            />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
