import pandas as pd, numpy as np, json
COST_PTS=0.30
# Parametres FIGES de la strategie "Trend Pullback NY"
P=dict(entry_start=15, entry_end=18, exit_h=21, look=16, stop_atr=1.0, trail_atr=1.5,
       ema=200, atrlen=40)

def load15_from_15m(path):
    d=pd.read_csv(path, sep=';'); d.columns=[c.strip().lower() for c in d.columns]
    d['dt']=pd.to_datetime(d['date'], format='%Y.%m.%d %H:%M')
    for c in ['open','high','low','close']: d[c]=pd.to_numeric(d[c])
    return d.sort_values('dt').reset_index(drop=True)

def load15_from_5m(path):
    d=pd.read_csv(path); d.columns=[c.strip().lower() for c in d.columns]
    d['dt']=pd.to_datetime(d['date'])
    d=d.set_index('dt')[['open','high','low','close']].resample('15min').agg(
        {'open':'first','high':'max','low':'min','close':'last'}).dropna().reset_index()
    return d

def prep(d):
    trr=np.maximum(d['high']-d['low'], np.maximum((d['high']-d['close'].shift()).abs(),(d['low']-d['close'].shift()).abs()))
    d['atr']=trr.rolling(P['atrlen']).mean()
    d['ema200']=d['close'].ewm(span=P['ema'],adjust=False).mean()
    d['d']=d['dt'].dt.normalize(); d['h']=d['dt'].dt.hour
    return d

def run(d):
    days=[]
    for dd,g in d.groupby('d', sort=True):
        days.append((dd,g['h'].to_numpy(),g['open'].to_numpy(),g['high'].to_numpy(),
                     g['low'].to_numpy(),g['close'].to_numpy(),g['atr'].to_numpy(),g['ema200'].to_numpy()))
    T=[]
    for (dd,h,o,hi,lo,c,atr,ema) in days:
        n=len(c); pos=None
        for j in range(P['look'], n):
            if h[j]>=P['exit_h'] and pos is not None:
                side,e,st,rsk=pos; T.append((dd,side,e,c[j],rsk)); pos=None; break
            a=atr[j]; em=ema[j]
            if not np.isfinite(a) or a<=0 or not np.isfinite(em): continue
            if pos is None:
                if not (P['entry_start']<=h[j]<P['entry_end']): continue
                hh=hi[j-P['look']:j].max(); ll=lo[j-P['look']:j].min()
                if c[j]>em and hi[j]>hh: e=hh; rsk=P['stop_atr']*a; pos=['L',e,e-rsk,rsk]
                elif c[j]<em and lo[j]<ll: e=ll; rsk=P['stop_atr']*a; pos=['S',e,e+rsk,rsk]
            else:
                side,e,st,rsk=pos
                if side=='L':
                    if lo[j]<=st: T.append((dd,side,e,st,rsk)); pos=None; continue
                    pos[2]=max(st, hi[j]-P['trail_atr']*a)
                else:
                    if hi[j]>=st: T.append((dd,side,e,st,rsk)); pos=None; continue
                    pos[2]=min(st, lo[j]+P['trail_atr']*a)
        if pos is not None:
            side,e,st,rsk=pos; T.append((dd,side,e,c[-1],rsk))
    rows=[]
    for (dd,side,e,x,rsk) in T:
        gross=(x-e) if side=='L' else (e-x)
        net=gross-COST_PTS
        R=net/rsk
        rows.append(dict(date=pd.Timestamp(dd), side=side, pts=net, R=R))
    return pd.DataFrame(rows)

def stats(t, risk_pct=0.004):
    t=t.sort_values('date').reset_index(drop=True)
    n=len(t); wins=t[t['R']>0]; losses=t[t['R']<=0]
    wr=len(wins)/n*100
    gp=t.loc[t['R']>0,'R'].sum(); gl=-t.loc[t['R']<=0,'R'].sum()
    pf=gp/gl if gl>0 else float('inf')
    totR=t['R'].sum()
    # equity en R, drawdown en R
    eq=t['R'].cumsum(); peak=eq.cummax(); dd=eq-peak
    maxdd=dd.min()
    # streaks
    res=(t['R']>0).tolist()
    def stk(seq,v):
        b=cu=0
        for x in seq: cu=cu+1 if x==v else 0; b=max(b,cu)
        return b
    days=t['date'].dt.normalize().nunique()
    return dict(n=n, wr=round(wr,1), pf=round(pf,2), totR=round(totR,1),
        expR=round(totR/n,3), avgW=round(wins['R'].mean(),2), avgL=round(losses['R'].mean(),2),
        maxddR=round(maxdd,1), winstreak=stk(res,True), losestreak=stk(res,False),
        trades_per_day=round(n/days,2), ret_pct=round(totR*risk_pct*100,1))

def yearly(t):
    t=t.copy(); t['y']=t['date'].dt.year
    out=[]
    for y,g in t.groupby('y'):
        gp=g.loc[g['R']>0,'R'].sum(); gl=-g.loc[g['R']<=0,'R'].sum()
        out.append(dict(year=int(y), n=len(g), wr=round((g['R']>0).mean()*100,1),
            pf=round(gp/gl,2) if gl>0 else 9.99, totR=round(g['R'].sum(),1)))
    return out

# ===== 20 ans 15m =====
d=prep(load15_from_15m("data/xau_15m_2004_2025.csv"))
t=run(d)
S=stats(t); Y=yearly(t)
print("===== 20 ANS (15m, 2004-2025) ====="); print(json.dumps(S,indent=0))
print("Train(<=2017):", json.dumps(stats(t[t['date'].dt.year<=2017])))
print("Test (>=2018):", json.dumps(stats(t[t['date'].dt.year>=2018])))
print("\nPar annee:")
for y in Y: print(f"  {y['year']}  n={y['n']:>4}  WR={y['wr']:>4}%  PF={y['pf']:>4}  R={y['totR']:>7}")
# equity curve (mensuelle) pour le site
t2=t.copy(); t2['ym']=t2['date'].dt.to_period('M').astype(str)
eqm=t2.groupby('ym')['R'].sum().cumsum()
print("\nEQUITY_MENSUELLE_R:", json.dumps([[k,round(v,1)] for k,v in eqm.items()]))

# ===== controle independant 5m 2025 =====
d5=prep(load15_from_5m("data/xauusd_5m_2025.csv"))
t5=run(d5)
print("\n===== CONTROLE 5m->15m 2025 ====="); print(json.dumps(stats(t5)))

# sauvegarde JSON pour le site
json.dump(dict(params=P, cost_pts=COST_PTS, all=S, train=stats(t[t['date'].dt.year<=2017]),
    test=stats(t[t['date'].dt.year>=2018]), yearly=Y, ctrl_2025=stats(t5),
    equity_monthly=[[k,round(v,1)] for k,v in eqm.items()]),
    open("data/backtest_results.json","w"), indent=2)
print("\n[OK] results.json ecrit")
