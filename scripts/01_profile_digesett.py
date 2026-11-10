import pandas as pd, sys, re, unicodedata
D=sys.argv[1] if len(sys.argv)>1 else './data/raw/'
f1=D+'Infracciones-de-Transito-DIGESETT-2018-2026.xlsx'
f2=D+'Fallecimientos-segun-Meses-DIGESETT-2016-2025.xlsx'
pd.set_option('display.width',250,'display.max_columns',30,'display.max_rows',400,'display.max_colwidth',70)
x=pd.ExcelFile(f1); print(x.sheet_names)
df=x.parse(x.sheet_names[0]); print(df.shape); print(df.dtypes)
print(df.isna().sum())
print(df['AÑO'].value_counts(dropna=False).sort_index())
M=list(df.columns[1:13])
# non numeric cells
for c in M:
    bad=df[pd.to_numeric(df[c],errors='coerce').isna() & df[c].notna()]
    if len(bad): print('NONNUM',c,bad[['INFRACCIONES',c,'AÑO']].to_string())
num=df[M].apply(pd.to_numeric,errors='coerce')
print('neg',(num<0).sum().sum(),'zeros',(num==0).sum().sum(),'nulls',num.isna().sum().sum(),'nonint',((num%1)!=0).sum().sum())
print('nulls by year/month');print(num.isna().groupby(df['AÑO']).sum())
print('zeros by year');print((num==0).groupby(df['AÑO']).sum().sum(axis=1))
print('totals by year/month');print(num.groupby(df['AÑO']).sum(min_count=1).assign(TOTAL=lambda d:d.sum(axis=1)))
print('dups full',df.duplicated().sum(),'dups name+year',df.duplicated(['INFRACCIONES','AÑO']).sum())
print(df[df.duplicated(['INFRACCIONES','AÑO'],keep=False)].to_string())
# total-like rows
print(df[df['INFRACCIONES'].astype(str).str.contains('total|TOTAL|Total',na=True)].to_string())
names=df['INFRACCIONES'].astype(str)
print('distinct raw',names.nunique(),'strip',names.str.strip().nunique())
print('lead/trail ws',(names!=names.str.strip()).sum(),'double sp',names.str.contains('  ').sum())
def norm(s):
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
    return re.sub(r'\s+',' ',re.sub(r'[^a-z0-9 ]',' ',s)).strip()
df['norm']=names.map(norm)
print('distinct norm',df['norm'].nunique())
g=df.groupby('norm')['INFRACCIONES'].nunique(); print('norm groups w/ >1 raw variant',(g>1).sum())
for k in g[g>1].index[:40]: print(' ',sorted(df[df.norm==k]['INFRACCIONES'].unique()))
df['art']=names.str.extract(r'\(([^)]*)\)\s*$')[0]
print('no art',df['art'].isna().sum()); print(df[df['art'].isna()]['INFRACCIONES'].unique()[:40])
pres=df.pivot_table(index='INFRACCIONES',columns='AÑO',values=M[0],aggfunc='size',fill_value=0)
pres['n_years']=(pres>0).sum(axis=1)
print(pres['n_years'].value_counts().sort_index())
df['TOTAL']=num.sum(axis=1)
print(pres.join(df.groupby('INFRACCIONES')['TOTAL'].sum()).sort_values('TOTAL',ascending=False).to_string())
print('=== FILE2')
x2=pd.ExcelFile(f2); print(x2.sheet_names)
for s in x2.sheet_names:
    d=x2.parse(s,header=None); print(s,d.shape); print(d.to_string())
