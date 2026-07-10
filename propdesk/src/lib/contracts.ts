/**
 * Spécifications des contrats futures les plus courants en prop firm.
 * tickSize  : variation minimale de prix (en points)
 * tickValue : valeur en dollars d'un tick, PAR CONTRAT
 */

export interface ContractSpec {
  symbol: string;
  label: string;
  tickSize: number;
  tickValue: number;
}

export const CONTRACT_SPECS: ContractSpec[] = [
  { symbol: "MNQ", label: "Micro Nasdaq 100 (MNQ)", tickSize: 0.25, tickValue: 0.5 },
  { symbol: "NQ", label: "E-mini Nasdaq 100 (NQ)", tickSize: 0.25, tickValue: 5 },
  { symbol: "MES", label: "Micro S&P 500 (MES)", tickSize: 0.25, tickValue: 1.25 },
  { symbol: "ES", label: "E-mini S&P 500 (ES)", tickSize: 0.25, tickValue: 12.5 },
  { symbol: "MYM", label: "Micro Dow (MYM)", tickSize: 1, tickValue: 0.5 },
  { symbol: "YM", label: "E-mini Dow (YM)", tickSize: 1, tickValue: 5 },
  { symbol: "M2K", label: "Micro Russell 2000 (M2K)", tickSize: 0.1, tickValue: 0.5 },
  { symbol: "RTY", label: "E-mini Russell 2000 (RTY)", tickSize: 0.1, tickValue: 5 },
  { symbol: "MGC", label: "Micro Gold (MGC)", tickSize: 0.1, tickValue: 1 },
  { symbol: "GC", label: "Gold (GC)", tickSize: 0.1, tickValue: 10 },
  { symbol: "MCL", label: "Micro Crude Oil (MCL)", tickSize: 0.01, tickValue: 1 },
  { symbol: "CL", label: "Crude Oil (CL)", tickSize: 0.01, tickValue: 10 },
  { symbol: "M6E", label: "Micro EUR/USD (M6E)", tickSize: 0.0001, tickValue: 1.25 },
  { symbol: "6E", label: "Euro FX (6E)", tickSize: 0.00005, tickValue: 6.25 },
];

export function getContractSpec(symbol: string): ContractSpec | undefined {
  return CONTRACT_SPECS.find((c) => c.symbol === symbol);
}
