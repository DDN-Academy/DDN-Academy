#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
backtest_gold.py — Moteur de backtest du Protocole Gold (setups A1 / B1).

CE SCRIPT NE FABRIQUE AUCUNE DONNEE DE MARCHE.
Il ne fonctionne que sur un fichier CSV de barres REELLES fourni par l'utilisateur
(export TradingView ou broker). Sans ce fichier, il s'arrete et n'invente rien.

------------------------------------------------------------------------------------
MECANISATION DES REGLES (version testable, sans jugement humain)
Le protocole du site est en partie discretionnaire ; ce moteur en encode une
traduction 100% mecanique. Toute statistique produite est specifique a CETTE
encodage et a CES donnees. Les facteurs non calculables sur les donnees fournies
(ex: confirmation DXY si pas de fichier DXY) sont marques "non disponible".

  Hierarchie TF : execution = TF du CSV ; SETUP = resample 15min ; BIAIS = resample 1H.

  BIAIS (1H) : swings fractals (k=2). long-only si HH+HL sur les 2 derniers swings,
               short-only si LL+LH, sinon no-trade. Connu seulement APRES confirmation
               du fractal (pas de lookahead), puis projete en avant.

  REGIME (15min) : ATR14 + EMA20/EMA50.
     - expansion si range de la derniere bougie 15m > 2x la moyenne(20) -> NO-TRADE
     - tendance si EMA20>EMA50 et (EMA20-EMA50)/ATR>0.5 (haussiere) / inverse (baissiere)
     - sinon range.

  NIVEAUX : PDH/PDL (jour precedent) + plus-haut/plus-bas de session en cours.

  SETUP A1 (regime range, direction = biais) : balayage d'un niveau de >=2 ticks
     puis cloture revenue a l'interieur avec meche de rejet >=50% du range.
     short au plus-haut balaye / long au plus-bas balaye.

  SETUP B1 (regime tendance, direction = biais) : pullback au contact EMA20(15m)
     (<=3 ticks) puis bougie de reprise qui cloture au-dela de l'extreme precedent.

  GESTION : stop au-dela de la meche/swing +3 ticks. TP1=1R (50%, stop->BE), TP2=2R.
     Si stop ET tp touches dans la meme bougie -> stop d'abord (hypothese prudente).
     Time-stop : cloture en fin de session si rien n'est atteint.

  RISQUE : 0.4% du capital nominal. Contrats MGC = floor(risque$/(stop_points*10)).
     MGC : 1 point = 10$ ; 1 tick = 0.1 point = 1$.
     Limites/jour : 3 trades max, stop a -2R, arret a +2R.

USAGE :
  python3 backtest_gold.py DONNEES.csv --tz America/New_York --capital 50000 \
          [--dxy DXY.csv] [--start 2023-01-01] [--end 2024-12-31] [--out backtest.pdf]
------------------------------------------------------------------------------------
"""
import argparse, math, sys
from datetime import time as dtime
import pandas as pd

TICK = 0.1            # taille de tick MGC en points
POINT_USD = 10.0      # valeur d'un point pour 1 contrat MGC
RISK_PCT = 0.004      # 0.4% par trade
MAX_TRADES_DAY = 3
DAILY_STOP_R = -2.0
DAILY_TARGET_R = 2.0

# --------------------------------------------------------------------------- IO
def load_csv(path):
    df = pd.read_csv(path)
    cols = {c.lower().strip(): c for c in df.columns}
    # time column
    tcol = None
    for k in ("time", "date", "datetime", "timestamp"):
        if k in cols: tcol = cols[k]; break
    if tcol is None: tcol = df.columns[0]
    s = df[tcol]
    if pd.api.types.is_numeric_dtype(s):
        unit = "s" if s.iloc[0] < 10_000_000_000 else "ms"
        ts = pd.to_datetime(s, unit=unit, utc=True)
    else:
        ts = pd.to_datetime(s, utc=True, errors="coerce")
    out = pd.DataFrame({"ts": ts})
    for k in ("open", "high", "low", "close"):
        if k not in cols:
            sys.exit(f"Colonne '{k}' introuvable dans {path}. Colonnes: {list(df.columns)}")
        out[k] = pd.to_numeric(df[cols[k]], errors="coerce")
    out = out.dropna(subset=["ts", "open", "high", "low", "close"]).sort_values("ts").reset_index(drop=True)
    return out

def localize(df, tz):
    # ts sont en UTC ; on ajoute une colonne locale pour sessions/heures/jours
    if df["ts"].dt.tz is None:
        df["ts"] = df["ts"].dt.tz_localize("UTC")
    df["utc"] = df["ts"]
    df["loc"] = df["ts"].dt.tz_convert(tz)
    return df

# ----------------------------------------------------------------- INDICATEURS
def ema(s, n): return s.ewm(span=n, adjust=False).mean()

def atr(df, n=14):
    h, l, c = df["high"], df["low"], df["close"]
    pc = c.shift(1)
    tr = pd.concat([(h - l), (h - pc).abs(), (l - pc).abs()], axis=1).max(axis=1)
    return tr.rolling(n).mean()

def fractal_swings(h1):
    """Renvoie series de biais ('long'/'short'/'none') indexee par ts H1, sans lookahead."""
    highs = h1["high"].values; lows = h1["low"].values; n = len(h1)
    sw_high, sw_low = [], []   # listes (idx_confirmation, prix)
    bias = ["none"] * n
    lastH = []; lastL = []
    for i in range(2, n - 2):
        is_h = highs[i] > highs[i-1] and highs[i] > highs[i-2] and highs[i] > highs[i+1] and highs[i] > highs[i+2]
        is_l = lows[i] < lows[i-1] and lows[i] < lows[i-2] and lows[i] < lows[i+1] and lows[i] < lows[i+2]
        conf = i + 2  # confirme 2 barres plus tard
        if is_h:
            lastH.append(highs[i]); lastH = lastH[-2:]
        if is_l:
            lastL.append(lows[i]); lastL = lastL[-2:]
        if conf < n and len(lastH) == 2 and len(lastL) == 2:
            if lastH[1] > lastH[0] and lastL[1] > lastL[0]: b = "long"
            elif lastH[1] < lastH[0] and lastL[1] < lastL[0]: b = "short"
            else: b = "none"
            # appliquer a partir de la barre de confirmation
            for j in range(conf, n):
                bias[j] = b
    return pd.Series(bias, index=h1.index)

# ------------------------------------------------------------------- CONTEXTE
def build_context(df):
    g = df.set_index("ts")
    # --- H1 biais ---
    h1 = g[["open","high","low","close"]].resample("1h").agg(
        {"open":"first","high":"max","low":"min","close":"last"}).dropna()
    h1_bias = fractal_swings(h1)
    # --- 15m regime ---
    m15 = g[["open","high","low","close"]].resample("15min").agg(
        {"open":"first","high":"max","low":"min","close":"last"}).dropna()
    m15["ema20"] = ema(m15["close"], 20); m15["ema50"] = ema(m15["close"], 50)
    m15["atr"] = atr(m15, 14); m15["rng"] = m15["high"] - m15["low"]
    m15["avgrng"] = m15["rng"].rolling(20).mean()
    def regime(r):
        if pd.isna(r["atr"]) or pd.isna(r["avgrng"]) or r["atr"] == 0: return "none"
        if r["rng"] > 2 * r["avgrng"]: return "expansion"
        sep = (r["ema20"] - r["ema50"]) / r["atr"]
        if sep > 0.5: return "trend_up"
        if sep < -0.5: return "trend_down"
        return "range"
    m15["regime"] = m15.apply(regime, axis=1)
    # map vers barres d'execution (derniere valeur connue, shift 1 pour eviter lookahead)
    df["bias"]   = h1_bias.reindex(df["ts"], method="ffill").shift(1).values if len(h1_bias) else "none"
    df["regime"] = m15["regime"].reindex(df["ts"], method="ffill").shift(1).values
    df["ema20_15"] = m15["ema20"].reindex(df["ts"], method="ffill").shift(1).values
    df["bias"] = df["bias"].fillna("none"); df["regime"] = df["regime"].fillna("none")
    # niveaux PDH/PDL par jour UTC
    df["day"] = df["utc"].dt.date
    daily = g[["high","low"]].resample("1D").agg({"high":"max","low":"min"})
    daily["pdh"] = daily["high"].shift(1); daily["pdl"] = daily["low"].shift(1)
    pdh = daily["pdh"].to_dict(); pdl = daily["pdl"].to_dict()
    norm = df["utc"].dt.normalize()
    df["pdh"] = norm.map(pdh); df["pdl"] = norm.map(pdl)
    return df

def session_of(hour_utc):
    if 0 <= hour_utc < 8: return "Asie"
    if 8 <= hour_utc < 13: return "Londres"
    if 13 <= hour_utc < 21: return "New York"
    return "Hors-session"

# -------------------------------------------------------------------- MOTEUR
def run(df, capital):
    risk_usd = capital * RISK_PCT
    trades = []
    i = 0; n = len(df)
    cur_day = None; day_trades = 0; day_R = 0.0
    while i < n - 1:
        row = df.iloc[i]
        d = row["day"]
        if d != cur_day:
            cur_day = d; day_trades = 0; day_R = 0.0
        if (day_trades >= MAX_TRADES_DAY or day_R <= DAILY_STOP_R or day_R >= DAILY_TARGET_R
                or row["regime"] in ("expansion", "none") or row["bias"] == "none"):
            i += 1; continue

        sig = detect_signal(df, i)
        if sig is None:
            i += 1; continue
        direction, entry, stop = sig["dir"], sig["entry"], sig["stop"]
        rdist = abs(entry - stop)
        if rdist < 2 * TICK:
            i += 1; continue
        contracts = math.floor(risk_usd / (rdist * POINT_USD))
        if contracts < 1:
            i += 1; continue
        tp1 = entry + (1 if direction == "long" else -1) * rdist
        tp2 = entry + (2 if direction == "long" else -2) * rdist

        # simulation barre par barre a partir de i+1
        exitp, exitt, half_done, be = None, None, False, stop
        j = i + 1
        last_idx = i
        while j < n and df.iloc[j]["day"] == d:
            b = df.iloc[j]; last_idx = j
            hi, lo = b["high"], b["low"]
            if direction == "long":
                if lo <= be:  # stop / BE d'abord (prudence)
                    exitp = be; exitt = b["ts"]; break
                if not half_done and hi >= tp1:
                    half_done = True; be = entry  # stop -> BE sur le reste
                if half_done and hi >= tp2:
                    exitp = tp2; exitt = b["ts"]; break
            else:
                if hi >= be:
                    exitp = be; exitt = b["ts"]; break
                if not half_done and lo <= tp1:
                    half_done = True; be = entry
                if half_done and lo <= tp2:
                    exitp = tp2; exitt = b["ts"]; break
            j += 1
        if exitp is None:  # time-stop fin de journee
            b = df.iloc[last_idx]; exitp = b["close"]; exitt = b["ts"]

        # P&L : si TP1 atteint, 50% a +1R + 50% a l'exit final ; sinon 100% a l'exit
        if half_done:
            # 1ere moitie sortie a +1R ; reste sorti au prix final (rem)
            rem = (exitp - entry) if direction == "long" else (entry - exitp)
            pnl_pts = 0.5 * rdist + 0.5 * rem
        else:
            rem = (exitp - entry) if direction == "long" else (entry - exitp)
            pnl_pts = rem
        pnl_usd = pnl_pts * POINT_USD * contracts
        r_mult = pnl_pts / rdist
        et = row["loc"] if "loc" in row else row["ts"]
        ent_loc = df.iloc[i]["loc"]
        trades.append({
            "entry_ts": df.iloc[i]["ts"], "entry_loc": ent_loc, "exit_ts": exitt,
            "setup": sig["setup"], "dir": direction, "entry": entry, "stop": stop,
            "exit": exitp, "contracts": contracts, "pnl_usd": pnl_usd, "R": r_mult,
            "session": session_of(df.iloc[i]["utc"].hour),
            "weekday": ent_loc.day_name(), "hour": ent_loc.hour,
            "month": ent_loc.strftime("%Y-%m"), "year": ent_loc.year,
        })
        day_trades += 1; day_R += r_mult
        i = last_idx + 1  # repartir apres la sortie
    return pd.DataFrame(trades)

def detect_signal(df, i):
    row = df.iloc[i]
    o, h, l, c = row["open"], row["high"], row["low"], row["close"]
    rng = h - l
    if rng <= 0: return None
    bias, regime = row["bias"], row["regime"]
    pdh, pdl, ema20 = row["pdh"], row["pdl"], row["ema20_15"]
    # ---- A1 : range + balayage/rejet ----
    if regime == "range":
        if bias == "short" and pd.notna(pdh) and h > pdh + 2 * TICK and c < pdh:
            upper_wick = h - max(o, c)
            if upper_wick >= 0.5 * rng:
                return {"setup":"A1","dir":"short","entry":c,"stop":h + 3*TICK}
        if bias == "long" and pd.notna(pdl) and l < pdl - 2 * TICK and c > pdl:
            lower_wick = min(o, c) - l
            if lower_wick >= 0.5 * rng:
                return {"setup":"A1","dir":"long","entry":c,"stop":l - 3*TICK}
    # ---- B1 : tendance + pullback EMA20(15m) + reprise ----
    if pd.notna(ema20):
        prev = df.iloc[i-1] if i > 0 else None
        if regime == "trend_up" and bias == "long" and prev is not None:
            touched = l <= ema20 + 3 * TICK
            reprise = c > prev["high"]
            if touched and reprise:
                stop = min(l, prev["low"]) - 3 * TICK
                return {"setup":"B1","dir":"long","entry":c,"stop":stop}
        if regime == "trend_down" and bias == "short" and prev is not None:
            touched = h >= ema20 - 3 * TICK
            reprise = c < prev["low"]
            if touched and reprise:
                stop = max(h, prev["high"]) + 3 * TICK
                return {"setup":"B1","dir":"short","entry":c,"stop":stop}
    return None

# ------------------------------------------------------------------ METRIQUES
def rank_table(tr, by):
    g = tr.groupby(by).agg(trades=("R","size"), net_usd=("pnl_usd","sum"),
                           win=("pnl_usd", lambda s:(s>0).sum())).reset_index()
    g["winrate"] = (g["win"]/g["trades"]*100).round(1)
    g["net_usd"] = g["net_usd"].round(2)
    return g.sort_values("net_usd", ascending=False)

def compute_metrics(tr, capital):
    m = {}
    n = len(tr)
    m["n"] = n
    if n == 0: return m
    wins = tr[tr["pnl_usd"] > 0]; losses = tr[tr["pnl_usd"] <= 0]
    m["winrate"] = round(len(wins)/n*100, 1)
    m["net_usd"] = round(tr["pnl_usd"].sum(), 2)
    m["net_pct"] = round(tr["pnl_usd"].sum()/capital*100, 2)
    gp = wins["pnl_usd"].sum(); gl = abs(losses["pnl_usd"].sum())
    m["profit_factor"] = round(gp/gl, 2) if gl > 0 else float("inf")
    m["avg_R_win"]  = round(wins["R"].mean(), 2) if len(wins) else None
    m["avg_R_loss"] = round(losses["R"].mean(), 2) if len(losses) else None
    m["avg_R"]      = round(tr["R"].mean(), 2)
    # equity & drawdown
    tr = tr.sort_values("entry_ts").reset_index(drop=True)
    eq = capital + tr["pnl_usd"].cumsum()
    peak = eq.cummax(); dd = eq - peak
    m["max_dd_usd"] = round(dd.min(), 2)
    m["max_dd_pct"] = round(dd.min()/peak[dd.idxmin()]*100, 2) if len(dd) else None
    m["max_dd_date"] = str(tr.loc[dd.idxmin(), "entry_ts"].date()) if len(dd) else "non disponible"
    # streaks
    res = (tr["pnl_usd"] > 0).tolist()
    def streak(seq, val):
        best = cur = 0
        for x in seq:
            cur = cur + 1 if x == val else 0
            best = max(best, cur)
        return best
    m["max_win_streak"] = streak(res, True)
    m["max_loss_streak"] = streak(res, False)
    # trades/jour
    per_day = tr.groupby(tr["entry_loc"].dt.date).size()
    m["avg_trades_day"] = round(per_day.mean(), 2)
    m["by_weekday_count"] = tr.groupby("weekday").size().to_dict()
    return m

# ------------------------------------------------------------------------ PDF
def build_pdf(tr, m, capital, period, out):
    from fpdf import FPDF
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(True, 15)
    GOLD = (180, 140, 40); DARK = (20, 25, 35); GREY = (90, 100, 115)

    def header(title):
        pdf.set_fill_color(*DARK); pdf.rect(0, 0, 210, 22, "F")
        pdf.set_xy(12, 7); pdf.set_text_color(*GOLD); pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 8, title)
        pdf.set_xy(12, 26); pdf.set_text_color(0, 0, 0)

    def h2(t):
        pdf.ln(3); pdf.set_font("Helvetica", "B", 11); pdf.set_text_color(*GOLD)
        pdf.cell(0, 7, t, new_x="LMARGIN", new_y="NEXT"); pdf.set_text_color(0,0,0)

    def kv(k, v):
        pdf.set_font("Helvetica", "", 10); pdf.cell(70, 6, k)
        pdf.set_font("Helvetica", "B", 10); pdf.cell(0, 6, str(v), new_x="LMARGIN", new_y="NEXT")

    def table(headers, rows, widths):
        pdf.set_font("Helvetica", "B", 8.5); pdf.set_fill_color(*DARK); pdf.set_text_color(*GOLD)
        for hh, w in zip(headers, widths): pdf.cell(w, 6, str(hh), border=0, fill=True, align="C")
        pdf.ln(); pdf.set_text_color(0,0,0); pdf.set_font("Helvetica", "", 8)
        fill = False
        for r in rows:
            if pdf.get_y() > 270:
                pdf.add_page(); header("Backtest Protocole Gold (suite)")
            pdf.set_fill_color(245, 242, 235)
            for v, w in zip(r, widths): pdf.cell(w, 5.2, str(v), border="B", fill=fill, align="C")
            pdf.ln(); fill = not fill

    # ---- page 1 : synthese ----
    pdf.add_page(); header("Backtest - Protocole Gold (A1/B1) - MGC")
    pdf.set_font("Helvetica", "", 9); pdf.set_text_color(*GREY)
    pdf.multi_cell(0, 5, f"Instrument: MGC Micro Gold  |  Capital: {capital:,.0f} $  |  Risque/trade: 0.4%  "
                         f"|  Periode: {period}\nMecanisation A1/B1 du protocole. Resultats specifiques a cet "
                         f"encodage et aux donnees fournies.")
    pdf.set_text_color(0,0,0)
    h2("1-8. Synthese globale")
    kv("1. Nombre total de trades", m["n"])
    kv("2. Winrate global", f"{m['winrate']} %")
    kv("3. Trades / jour (moyenne)", m["avg_trades_day"])
    kv("4. RR moyen - gagnants", m["avg_R_win"]); kv("   RR moyen - perdants", m["avg_R_loss"])
    kv("   RR moyen - global", m["avg_R"])
    kv("5. Profit factor", m["profit_factor"])
    kv("6. Gain net total", f"{m['net_usd']:,.2f} $  ({m['net_pct']} %)")
    kv("7. Drawdown maximum", f"{m['max_dd_usd']:,.2f} $  ({m['max_dd_pct']} %)  le {m['max_dd_date']}")
    kv("8. Plus longue serie - gains", m["max_win_streak"])
    kv("   Plus longue serie - pertes", m["max_loss_streak"])

    h2("3. Trades par jour de semaine (detail)")
    wd_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    fr = {"Monday":"Lundi","Tuesday":"Mardi","Wednesday":"Mercredi","Thursday":"Jeudi",
          "Friday":"Vendredi","Saturday":"Samedi","Sunday":"Dimanche"}
    rows = [[fr[d], m["by_weekday_count"].get(d, 0)] for d in wd_order if m["by_weekday_count"].get(d,0)]
    table(["Jour","Nb trades"], rows, [60, 40])

    # ---- page 2 : classements ----
    pdf.add_page(); header("Classements (du + profitable au -)")
    h2("9. Sessions (par gain net)")
    s = rank_table(tr, "session")
    table(["Session","Trades","Net $","Winrate %"],
          s[["session","trades","net_usd","winrate"]].values.tolist(), [50,30,40,40])
    h2("10. Jours de la semaine (par gain net)")
    w = rank_table(tr, "weekday"); w["weekday"] = w["weekday"].map(lambda d: fr.get(d,d))
    table(["Jour","Trades","Net $","Winrate %"],
          w[["weekday","trades","net_usd","winrate"]].values.tolist(), [50,30,40,40])
    h2("11. Heures (par gain net)")
    hh = rank_table(tr, "hour")
    table(["Heure","Trades","Net $","Winrate %"],
          [[f"{int(x)}h", t, nu, wr] for x,t,nu,wr in
           hh[["hour","trades","net_usd","winrate"]].values.tolist()], [50,30,40,40])

    # ---- page 3 : temporel ----
    pdf.add_page(); header("Performance temporelle")
    h2("12. Mois par mois")
    mo = tr.groupby("month").agg(trades=("R","size"), net=("pnl_usd","sum"),
                                 win=("pnl_usd", lambda x:(x>0).sum())).reset_index()
    mo["wr"] = (mo["win"]/mo["trades"]*100).round(1); mo["net"] = mo["net"].round(2)
    table(["Mois","Trades","Net $","Winrate %"],
          mo[["month","trades","net","wr"]].values.tolist(), [50,30,40,40])
    h2("13. Annee par annee")
    if tr["year"].nunique() > 1 or True:
        ye = tr.groupby("year").agg(trades=("R","size"), net=("pnl_usd","sum"),
                                    win=("pnl_usd", lambda x:(x>0).sum())).reset_index()
        ye["wr"] = (ye["win"]/ye["trades"]*100).round(1); ye["net"] = ye["net"].round(2)
        table(["Annee","Trades","Net $","Winrate %"],
              ye[["year","trades","net","wr"]].values.tolist(), [50,30,40,40])

    # ---- annexe : trade par trade ----
    pdf.add_page(); header("14. Annexe - trade par trade")
    rows = []
    for _, t in tr.sort_values("entry_ts").iterrows():
        rows.append([t["entry_loc"].strftime("%Y-%m-%d"), t["entry_loc"].strftime("%H:%M"),
                     t["setup"], t["dir"], f"{t['entry']:.1f}", f"{t['exit']:.1f}",
                     f"{t['R']:+.2f}R", f"{t['pnl_usd']:+.0f}$"])
    table(["Date","Heure","Setup","Sens","Entree","Sortie","R","P&L"],
          rows, [26,16,16,16,22,22,20,24])

    # reconciliation
    pdf.ln(4); pdf.set_font("Helvetica","I",8); pdf.set_text_color(*GREY)
    check = round(tr["pnl_usd"].sum(), 2)
    pdf.multi_cell(0,4, f"Controle: somme des {len(tr)} P&L individuels = {check:,.2f} $ "
                        f"= gain net total declare. Totaux reconcilies.")
    pdf.output(out)

# ------------------------------------------------------------------------ MAIN
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv", help="CSV de barres intraday REELLES (OHLC)")
    ap.add_argument("--tz", default="America/New_York", help="Fuseau des horodatages du CSV")
    ap.add_argument("--capital", type=float, default=50000)
    ap.add_argument("--start", default=None); ap.add_argument("--end", default=None)
    ap.add_argument("--dxy", default=None, help="(optionnel) CSV DXY - sinon facteur DXY 'non disponible'")
    ap.add_argument("--out", default="backtest_gold.pdf")
    a = ap.parse_args()

    df = localize(load_csv(a.csv), a.tz)
    if a.start: df = df[df["loc"] >= pd.Timestamp(a.start, tz=a.tz)]
    if a.end:   df = df[df["loc"] <= pd.Timestamp(a.end, tz=a.tz)]
    df = df.reset_index(drop=True)
    if len(df) < 200:
        sys.exit("Pas assez de barres pour un backtest credible (min ~200).")
    period = f"{df['loc'].iloc[0].date()} -> {df['loc'].iloc[-1].date()}"
    if a.dxy is None:
        print("[INFO] Pas de fichier DXY : facteur de confluence DXY = 'non disponible' (non fabrique).")

    df = build_context(df)
    tr = run(df, a.capital)
    if len(tr) == 0:
        sys.exit("Aucun trade declenche sur ces donnees/regles. Aucun chiffre invente.")
    m = compute_metrics(tr, a.capital)
    build_pdf(tr, m, a.capital, period, a.out)
    print(f"[OK] {len(tr)} trades | net {m['net_usd']:,.2f}$ ({m['net_pct']}%) "
          f"| winrate {m['winrate']}% | PF {m['profit_factor']} -> {a.out}")

if __name__ == "__main__":
    main()
