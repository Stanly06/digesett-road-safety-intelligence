"""Implementación de referencia en pandas de las medidas DAX y de la analítica de la web.
Escrita de forma independiente del JavaScript para poder comparar ambos resultados."""
# Implementación de referencia en pandas, escrita a partir de las fórmulas DAX (independiente del JS)
import pandas as pd, numpy as np
from pathlib import Path
R=str(Path(__file__).resolve().parents[1]/'data')+'/'
f=pd.read_csv(R+'validation/FactTrafficViolations_expected.csv',parse_dates=['MonthStartDate'])
d=pd.read_csv(R+'reference/DimInfraction.csv')
fx=pd.read_csv(R+'validation/FactRoadFatalities_expected.csv',parse_dates=['MonthStartDate'])
f['y']=f.MonthStartDate.dt.year; f['m']=f.MonthStartDate.dt.month; f['MI']=f.y*12+f.m
f=f.merge(d[['InfractionID','InfractionType','InfractionCategory']],on='InfractionID')
fx['y']=fx.MonthStartDate.dt.year; fx['m']=fx.MonthStartDate.dt.month; fx['MI']=fx.y*12+fx.m
pos=f[f.ViolationCount>0].MI; LAST=pos.max(); MINV=pos.min()
YEARS=list(range(2016,2027))
yOf=lambda mi:(mi-1)//12
complete=lambda y: y>=yOf(MINV) and (y<yOf(LAST) or (y==yOf(LAST) and LAST-yOf(LAST)*12==12))
common=lambda mi: max(MINV,fx.MI.min())<=mi<=min(LAST,fx.MI.max())
def dates(ctx):
    ys=[ctx['y']] if ctx.get('y') is not None else YEARS
    ms=[ctx['m']] if ctx.get('m') is not None else range(1,13)
    if ctx.get('q') is not None: ms=[m for m in ms if (m-1)//3+1==ctx['q']]
    return [y*12+m for y in ys for m in ms]
def V(MIs,ctx):
    s=f[f.MI.isin(MIs)]
    if ctx.get('cat') is not None: s=s[s.InfractionCategory==ctx['cat']]
    if ctx.get('type') is not None: s=s[s.InfractionID==ctx['type']]
    return s
T=lambda s: None if len(s)==0 else int(s.ViolationCount.sum())
MWD=lambda s: s.MI.nunique()
def DIV(a,b): return None if a is None or b is None or b==0 else a/b
def yoy(MIs,ctx):
    cur=V(MIs,ctx); c=T(cur)
    py=[x-12 for x in MIs if x<=LAST]; pr=V(py,ctx)
    prev=T(pr) if (MWD(cur)>0 and MWD(cur)==MWD(pr)) else None
    g=DIV(c-prev,prev) if (c is not None and prev is not None) else None
    return c,prev,g
def measures(page,ctx):
    ds=dates(ctx); s=V(ds,ctx); tot=T(s); o={}
    if page in('overview','tendencias','estacionalidad','infracciones'):
        o['total']=tot
    if page in('overview','tendencias','estacionalidad'):
        o['months']=MWD(s) or None; o['avgMonthly']=DIV(tot,MWD(s))
        o['types']=int((s.groupby('InfractionID').ViolationCount.sum()>0).sum()) or None
        if len(s):
            LY=int(s.y.max()); o['latestYear']=LY; o['latestYoY']=yoy(dates({**ctx,'y':LY}),ctx)[2]
        else: o['latestYear']=None; o['latestYoY']=None
        mt=s.groupby('MI').ViolationCount.sum()
        o['maxMonth']=int(mt.max()) if len(mt) else None; o['minMonth']=int(mt.min()) if len(mt) else None
        yv=[T(V([mi for mi in ds if yOf(mi)==y],ctx)) for y in sorted(set(map(yOf,ds))) if complete(y)]
        yv=[v for v in yv if v is not None]; o['avgAnnual']=sum(yv)/len(yv) if yv else None
        # DATESYTD: desde el 1 de enero del año de la última fecha del contexto
        if not ds or min(ds)>LAST: o['ytd']=o['ytdPY']=o['ytdG']=None
        else:
            mx=max(ds); Y=yOf(mx); st=Y*12+1
            v=T(V(list(range(st,mx+1)),ctx)); end=min(mx,LAST); p=T(V(list(range(st-12,end-12+1)),ctx))
            o['ytd']=v; o['ytdPY']=p; o['ytdG']=DIV(v-p,p) if v is not None and p is not None else None
        o['partial']=bool(len(s) and any(not complete(y) for y in s.y.unique()))
    if page=='infracciones' or page=='overview':
        tt=s.groupby('InfractionType').ViolationCount.sum()
        o['topName']=', '.join(sorted(tt[tt==tt.max()].index)) if len(tt) else None
    if page=='infracciones':
        tt=s.groupby('InfractionID').ViolationCount.sum()
        o['topShare']=DIV(tt.max(),tt.sum()) if len(tt) else None
        for k in (5,10):
            if not len(tt): o[f'top{k}']=None; continue
            srt=tt.sort_values(ascending=False); kth=srt.iloc[min(k,len(srt))-1]
            o[f'top{k}']=DIV(srt[srt>=kth].sum(),tt.sum())
        o['types']=int((tt>0).sum()) or None; o['partial']=bool(len(s) and any(not complete(y) for y in s.y.unique()))
    if page=='seguridad-vial':
        fr=fx[fx.MI.isin(ds)]; o['fat']=int(fr.Fatalities.sum()) if len(fr) else None
        o['fatAvg']=fr.Fatalities.mean() if len(fr) else None
        if len(fr):
            LY=int(fr.y.max()); dl=dates({**ctx,'y':LY}); c=fx[fx.MI.isin(dl)].Fatalities; p=fx[fx.MI.isin([x-12 for x in dl])].Fatalities
            o['fatYear']=LY; o['fatYoY']=DIV(c.sum()-p.sum(),p.sum()) if len(c) and len(p) else None
        else: o['fatYear']=None; o['fatYoY']=None
        com=[x for x in ds if common(x)]
        cf=fx[fx.MI.isin(com)]; o['fatCommon']=int(cf.Fatalities.sum()) if len(cf) else None
        o['vioCommon']=T(V(com,{}))
    return o
# Series por año (combo de Tendencias) y medias móviles / MoM
def year_series(ctx):
    ds=dates(ctx); out=[]
    for y in YEARS:
        mis=[x for x in ds if yOf(x)==y]; c,p,g=yoy(mis,ctx)
        if c is not None: out.append([y,c,g,(c-p) if p is not None else None])
    return out
def rolling(mi,w,ctx):
    if T(V([mi],ctx)) is None: return None
    win=V(list(range(mi-w+1,mi+1)),ctx)
    return T(win)/w if MWD(win)==w else None
def mom(mi,ctx):
    c=T(V([mi],ctx)); p=T(V([mi-1],ctx))
    return DIV(c-p,p) if c is not None and p is not None else None

# ---- analítica avanzada (tasas, control, proyección, mezcla) ----
fa=pd.read_csv(R+'validation/FactTrafficViolations_expected.csv',parse_dates=['MonthStartDate'])
xa=pd.read_csv(R+'validation/FactRoadFatalities_expected.csv',parse_dates=['MonthStartDate']).sort_values('MonthStartDate')
den=pd.read_csv(R+'reference/denominators.csv').set_index('Year')
hr=set(pd.read_csv(R+'reference/high_risk_types.csv').InfractionID)
fa['y']=fa.MonthStartDate.dt.year; fa['m']=fa.MonthStartDate.dt.month; xa['y']=xa.MonthStartDate.dt.year; xa['m']=xa.MonthStartDate.dt.month
fa=fa.merge(d[['InfractionID','InfractionCategory']],on='InfractionID')
ANALYTICS={}
vy=fa.groupby('y').ViolationCount.sum(); fy=xa.groupby('y').Fatalities.sum()
ANALYTICS['rate']={y:(fy[y]/den.Population[y]*1e5, fy[y]/den.VehicleFleet[y]*1e4) for y in den.index}
ANALYTICS['vio1k']={y:vy[y]/den.VehicleFleet[y]*1e3 for y in range(2018,2026)}
b=xa[xa.y<=2019].Fatalities.values; mr=np.abs(np.diff(b)).mean(); CL=b.mean(); sig=mr/1.128
ANALYTICS['ctl']=(CL,CL+3*sig,CL-3*sig)
s=xa.Fatalities.values; ANALYTICS['r1']=[(int(xa.y.iloc[i]),int(xa.m.iloc[i])) for i in range(len(s)) if s[i]>CL+3*sig or s[i]<CL-3*sig]
side=np.sign(s-CL); flag=np.zeros(len(s),bool); run=0
for i in range(len(s)):
    run = run+1 if i>0 and side[i]!=0 and side[i]==side[i-1] else (1 if side[i]!=0 else 0)
    if run>=8: flag[i-run+1:i+1]=True
ANALYTICS['r2']=int(flag.sum())
mt=fa.groupby(['y','m']).ViolationCount.sum(); LM=int(fa[fa.y==2026].m.max()); ytd=mt[2026].sum()
est=sorted(ytd/(mt[y][mt[y].index<=LM].sum()/mt[y].sum()) for y in [2018,2019,2021,2022,2023,2024,2025])
ANALYTICS['proj']=(est[0],float(np.median(est)),est[-1])
mix={}
for y,g in fa.groupby('y'):
    t=g.groupby('InfractionID').ViolationCount.sum(); tot=t.sum()
    mix[y]=(t[t.index.isin(hr)].sum()/tot, g[(g.InfractionCategory=='Documentación y registro')&(~g.InfractionID.isin(hr))].ViolationCount.sum()/tot, ((t/tot)**2).sum()*1e4, t.sort_values(ascending=False).iloc[:5].sum()/tot)
ANALYTICS['mix']=mix
