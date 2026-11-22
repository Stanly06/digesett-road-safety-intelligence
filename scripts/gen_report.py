import json, os, shutil, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=str(ROOT/'DIGESETT_Road_Safety_Intelligence.Report'/'definition')
shutil.rmtree(OUT+'/pages',ignore_errors=True); os.makedirs(OUT+'/pages')
BG='#1B1E22'; CARD='#272B31'; LINE='#3A4048'; TXT='#F4F5F6'; SUB='#A7AEB6'; Y='#FFC72C'; TEAL='#2A9D8F'; ORG='#F28C28'; RED='#E5383B'
IMG='header_digesett_v2.png'
VS="https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.14.0/schema.json"
PS="https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json"
DISPLAY={'Total Traffic Violations':'Infracciones','Rolling 12M Average':'Media móvil 12 meses','Rolling 3M Average':'Media móvil 3 meses','YoY Growth %':'Variación interanual %',
 'Violations Top N':'Infracciones (Top N)','Cumulative Share Top N':'Participación acumulada','Violations (Common Period)':'Infracciones (período común)','Fatalities (Common Period)':'Fallecimientos (período común)',
 'Total Road Fatalities':'Fallecimientos','Average Monthly Violations':'Promedio mensual','Average Monthly Fatalities':'Promedio mensual de fallecimientos','MoM Growth %':'Variación mensual %',
 'Dynamic Variance Absolute':'Cambio absoluto','Infraction Share %':'Participación %','Selected Metric':'Valor','YearLabel':'Año','MonthNameShort':'Mes','MonthStartDate':'Mes','InfractionCategory':'Categoría',
 'InfractionType':'Tipo de infracción','LegalReference':'Ref. legal','Quarter':'Trimestre','RiskGroup':'Grupo','Fatalities per 100k Inhabitants':'Por 100,000 habitantes','Fatalities per 10k Vehicles':'Por 10,000 vehículos',
 'Index Violations':'Infracciones','Index Fatalities':'Fallecimientos','Index Vehicle Fleet':'Parque vehicular','Index Population':'Población','HHI Index':'HHI','Top 5 Infractions Share %':'Participación del Top 5',
 'Fatalities Control Center':'Media (base 2016–2019)','Fatalities UCL':'Límite superior','Fatalities LCL':'Límite inferior','Fatalities Out of Control':'Fuera de control','Seasonal Index Violations':'Infracciones','Seasonal Index Fatalities':'Fallecimientos','Violations per 1k Vehicles':'Infracciones por 1,000 vehículos'}
def hid(s): return hashlib.md5(s.encode()).hexdigest()[:20]
def lit(v):
    if isinstance(v,bool): return {"expr":{"Literal":{"Value":"true" if v else "false"}}}
    if isinstance(v,(int,float)): return {"expr":{"Literal":{"Value":f"{v}D"}}}
    return {"expr":{"Literal":{"Value":"'"+v.replace("'","''")+"'"}}}
def col(x): return {"solid":{"color":lit(x)}}
def M(name): return {"Measure":{"Expression":{"SourceRef":{"Entity":"_Measures"}},"Property":name}}
def C(t,c): return {"Column":{"Expression":{"SourceRef":{"Entity":t}},"Property":c}}
def proj(f,active=False):
    k=list(f)[0]; ent=f[k]["Expression"]["SourceRef"]["Entity"]; p=f[k]["Property"]
    d={"field":f,"queryRef":f"{ent}.{p}","nativeQueryRef":p}
    if p in DISPLAY: d["displayName"]=DISPLAY[p]
    if active: d["active"]=True
    return d
def container(title=None, bg=True, title_measure=None, border=True):
    o={}
    if title or title_measure:
        o["title"]=[{"properties":{"show":lit(True),"text":({"expr":M(title_measure)} if title_measure else lit(title))}}]
    else: o["title"]=[{"properties":{"show":lit(False)}}]
    if not bg:
        o["background"]=[{"properties":{"show":lit(False)}}]; o["border"]=[{"properties":{"show":lit(False)}}]
    elif not border: o["border"]=[{"properties":{"show":lit(False)}}]
    return o
class Page:
    def __init__(s,pid,name,filters=None,hidden=False):
        s.pid=pid; s.name=name; s.vis=[]; s.filters=filters; s.hidden=hidden; s.z=0
    def add(s,key,x,y,w,h,visual,vid=None,extra=None,z=None):
        if z is None: s.z+=1000
        zz=s.z if z is None else z
        v={"$schema":VS,"name":vid or hid(s.pid+key),"position":{"x":x,"y":y,"z":zz,"height":h,"width":w,"tabOrder":zz},"visual":visual}
        if extra: v.update(extra)
        s.vis.append(v)
    def write(s):
        d=f"{OUT}/pages/{s.pid}"; os.makedirs(d+'/visuals')
        p={"$schema":PS,"name":s.pid,"displayName":s.name,"displayOption":"FitToPage","height":1080,"width":1920}
        if s.filters: p["filterConfig"]={"filters":s.filters}
        if s.hidden: p["visibility"]="HiddenInViewMode"
        json.dump(p,open(d+'/page.json','w',encoding='utf-8'),indent=2,ensure_ascii=False)
        for v in s.vis:
            os.makedirs(f"{d}/visuals/{v['name']}"); json.dump(v,open(f"{d}/visuals/{v['name']}/visual.json",'w',encoding='utf-8'),indent=2,ensure_ascii=False)
def bool_filter(t,c,name):
    return {"name":hid('f'+name),"field":C(t,c),"type":"Categorical","filter":{"Version":2,"From":[{"Name":"d","Entity":t,"Type":0}],
      "Where":[{"Condition":{"In":{"Expressions":[{"Column":{"Expression":{"SourceRef":{"Source":"d"}},"Property":c}}],"Values":[[{"Literal":{"Value":"true"}}]]}}}]},"howCreated":"User"}
# ---------- visual builders
def textbox(runs_by_par):
    pars=[{"textRuns":[{"value":t,"textStyle":st} for t,st in runs]} for runs in runs_by_par]
    return {"visualType":"textbox","objects":{"general":[{"properties":{"paragraphs":pars}}]},"visualContainerObjects":container(bg=False),"drillFilterOtherVisuals":True}
def card(measure,title,size=30,color=Y,wrap=False):
    o={"labels":[{"properties":{"fontSize":lit(size),"color":col(color),"fontFamily":lit("Segoe UI Semibold")}}],"categoryLabels":[{"properties":{"show":lit(False)}}]}
    if wrap: o["wordWrap"]=[{"properties":{"show":lit(True)}}]
    return {"visualType":"card","query":{"queryState":{"Values":{"projections":[proj(M(measure))]}}},"objects":o,"visualContainerObjects":container(title),"drillFilterOtherVisuals":True}
def note(measure,color=SUB,size=11):
    v=card(measure,None,size,color,wrap=True); v["visualContainerObjects"]=container(bg=False); return v
def chart(vtype,roles,title=None,sort=None,objects=None,title_measure=None):
    qs={r:{"projections":[proj(f,active=(r in('Category','Rows','Columns','Series') )) for f in fs]} for r,fs in roles.items()}
    q={"queryState":qs}
    if sort: q["sortDefinition"]={"sort":[{"field":sort[0],"direction":sort[1]}],"isDefaultSort":False}
    v={"visualType":vtype,"query":q,"visualContainerObjects":container(title,title_measure=title_measure),"drillFilterOtherVisuals":True}
    if objects: v["objects"]=objects
    return v
def slicer(t,c,title,group=None,dropdown=True):
    v={"visualType":"slicer","query":{"queryState":{"Values":{"projections":[proj(C(t,c),True)]}}},
       "objects":{"data":[{"properties":{"mode":lit("Dropdown" if dropdown else "Basic")}}],"header":[{"properties":{"show":lit(False)}}]},
       "visualContainerObjects":container(title),"drillFilterOtherVisuals":True}
    if group: v["syncGroup"]={"groupName":group,"fieldChanges":True,"filterChanges":True}
    return v
def button(text,target,active=False):
    D={"id":"default"}
    return {"visualType":"actionButton","objects":{
        "icon":[{"properties":{"show":lit(False)}}],
        "text":[{"properties":{"show":lit(True)}},{"properties":{"text":lit(text),"fontColor":col(BG if active else TXT),"fontSize":lit(10),"fontFamily":lit("Segoe UI Semibold")},"selector":D}],
        "fill":[{"properties":{"show":lit(True)}},{"properties":{"fillColor":col(Y if active else CARD),"transparency":lit(0)},"selector":D}],
        "outline":[{"properties":{"show":lit(not active)}},{"properties":{"lineColor":col(LINE),"weight":lit(1)},"selector":D}]},
      "visualContainerObjects":{"visualLink":[{"properties":{"show":lit(True),"type":lit("PageNavigation"),"navigationSection":lit(target)}}],
        "title":[{"properties":{"show":lit(False)}}],"background":[{"properties":{"show":lit(False)}}],"border":[{"properties":{"show":lit(False)}}]},
      "drillFilterOtherVisuals":True}
def gradient(measure,lo='#2F343B',hi=Y):
    return [{"properties":{"backColor":{"solid":{"color":{"expr":{"FillRule":{"Input":M(measure),"FillRule":{"linearGradient2":{
        "min":{"color":{"Literal":{"Value":f"'{lo}'"}}},"max":{"color":{"Literal":{"Value":f"'{hi}'"}}},
        "nullColoringStrategy":{"strategy":{"Literal":{"Value":"'asZero'"}}}}}}}}}}},
        "selector":{"data":[{"dataViewWildcard":{"matchingOption":1}}],"metadata":f"_Measures.{measure}"}}]
LBL={"labels":[{"properties":{"show":lit(True),"color":col(TXT),"fontSize":lit(9)}}]}
LEG_B={"legend":[{"properties":{"show":lit(True),"position":lit("Bottom"),"labelColor":col(SUB)}}]}
NOLEG={"legend":[{"properties":{"show":lit(False)}}]}
# ---------- pages
PIDS=[('76bfa875cc4ee3ee95b1','Executive Overview','Resumen'),(hid('p2'),'Historical Trends','Tendencias'),(hid('p3'),'Infraction Analysis','Infracciones'),(hid('p4'),'Monthly & Seasonal','Estacionalidad'),(hid('p5'),'Road Safety Insights','Seguridad vial'),(hid('p6'),'Risk & Control','Riesgo vial')]
HASV=[bool_filter('DimDate','HasViolationData','hv')]
def frame(p,idx,subtitle,slicers):
    p.add('band',0,0,1920,84,{"visualType":"image","objects":{"general":[{"properties":{"imageUrl":{"expr":{"ResourcePackageItem":{"PackageName":"RegisteredResources","PackageType":1,"ItemName":IMG}}}}}],"imageScaling":[{"properties":{"imageScalingType":lit("Fill")}}]},
        "visualContainerObjects":{"title":[{"properties":{"show":lit(False)}}],"background":[{"properties":{"show":lit(False)}}],"border":[{"properties":{"show":lit(False)}}],"padding":[{"properties":{"top":lit(0),"bottom":lit(0),"left":lit(0),"right":lit(0)}}]},"drillFilterOtherVisuals":True},z=0)
    p.add('hdr',112,6,1090,70,textbox([[("DIGESETT",{"fontWeight":"bold","fontSize":"22pt","color":"#FFFFFF"}),("  ·  Road Safety Intelligence",{"fontSize":"22pt","color":"#FFFFFF"})],
        [(subtitle+"  ·  Proyecto independiente, no oficial",{"fontSize":"10pt","color":"#C9D6E8"})]]))
    bx=1180
    for i,(pid,_,short) in enumerate(PIDS):
        p.add(f'nav{i}',bx+i*122,24,116,40,button(short,pid,active=(i==idx)))
    x=24
    for k,(t,c,title,grp,w) in enumerate(slicers):
        p.add(f'sl{k}',x,88,w,82,slicer(t,c,title,grp)); x+=w+16
S_YEAR=('DimDate','Year','Año','Year',220); S_MONTH=('DimDate','MonthName','Mes','Month',240)
S_CAT=('DimInfraction','InfractionCategory','Categoría (clasificación propia)','Category',380); S_TYPE=('DimInfraction','InfractionType','Tipo de infracción','Type',560)
pages=[]
# ===== PAGE 1
p=Page(PIDS[0][0],PIDS[0][1],HASV); pages.append(p)
frame(p,0,"Infracciones de tránsito registradas en República Dominicana · Fuente: DIGESETT (datos.gov.do)",[S_YEAR,S_MONTH,S_CAT,S_TYPE])
kp=[('Total Traffic Violations','Infracciones registradas',30,Y,False),('Latest Year YoY Label','Variación interanual (último año)',20,TXT,True),('Average Monthly Violations','Promedio mensual',30,Y,False),('Top Infraction Name','Principal tipo de infracción',17,TXT,True),('Number of Infraction Types','Tipos con registros',30,Y,False)]
for i,(m_,t,s,c_,w_) in enumerate(kp): p.add(f'k{i}',24+i*378,176,360,128,card(m_,t,s,c_,w_))
p.add('line',24,320,1180,356,chart('lineChart',{"Category":[C('DimDate','MonthStartDate')],"Y":[M('Total Traffic Violations'),M('Rolling 12M Average')]},sort=(C('DimDate','MonthStartDate'),'Ascending'),objects=LEG_B,title_measure='Dynamic KPI Title'),vid='2c9d1cba940611b4261b')
p.add('donut',1220,320,676,356,chart('donutChart',{"Category":[C('DimInfraction','InfractionCategory')],"Y":[M('Total Traffic Violations')]},"Participación por categoría",objects={"legend":[{"properties":{"show":lit(True),"position":lit("Right"),"labelColor":col(SUB)}}],"labels":[{"properties":{"show":lit(True),"labelStyle":lit("Percent of total"),"color":col(TXT)}}]}))
p.add('colyear',24,692,700,340,chart('clusteredColumnChart',{"Category":[C('DimDate','YearLabel')],"Y":[M('Total Traffic Violations')]},"Infracciones por año",sort=(C('DimDate','YearLabel'),'Ascending'),objects=LBL))
p.add('top10',740,692,1156,340,chart('clusteredBarChart',{"Category":[C('DimInfraction','InfractionType')],"Y":[M('Violations Top N')]},"Top 10 tipos de infracción",sort=(M('Violations Top N'),'Descending'),objects=LBL))
p.add('note',24,1038,1872,34,note('Partial Period Note'))
# ===== PAGE 2
p=Page(PIDS[1][0],PIDS[1][1],HASV); pages.append(p)
frame(p,1,"Evolución histórica 2018–2026 · variaciones calculadas sobre períodos comparables",[S_YEAR,S_CAT,S_TYPE,('Comparison Selector','Comparison','Comparación',None,260)])
kp=[('Total Traffic Violations','Infracciones registradas',30,Y,False),('Average Annual Violations','Promedio anual (años completos)',30,Y,False),('Latest Year YoY Label','Variación interanual (último año)',20,TXT,True),('Total Violations YTD','Acumulado del año (YTD)',30,Y,False),('YTD Growth %','Variación YTD vs. año anterior',30,TXT,False)]
for i,(m_,t,s,c_,w_) in enumerate(kp): p.add(f'k{i}',24+i*378,176,360,112,card(m_,t,s,c_,w_))
p.add('combo',24,304,928,360,chart('lineClusteredColumnComboChart',{"Category":[C('DimDate','YearLabel')],"Y":[M('Total Traffic Violations')],"Y2":[M('YoY Growth %')]},"Evolución anual y variación interanual (%)",sort=(C('DimDate','YearLabel'),'Ascending'),objects=LEG_B))
p.add('cmp',968,304,928,360,chart('lineChart',{"Category":[C('DimDate','MonthNameShort')],"Series":[C('DimDate','YearLabel')],"Y":[M('Total Traffic Violations')]},"Comparación mensual entre años",sort=(C('DimDate','MonthNameShort'),'Ascending'),objects=LEG_B))
p.add('yoyabs',24,680,560,352,chart('clusteredColumnChart',{"Category":[C('DimDate','MonthStartDate')],"Y":[M('Dynamic Variance Absolute')]},"Cambio absoluto mensual según comparación seleccionada",sort=(C('DimDate','MonthStartDate'),'Ascending')))
p.add('trend',600,680,620,352,chart('lineChart',{"Category":[C('DimDate','MonthStartDate')],"Y":[M('Rolling 3M Average'),M('Rolling 12M Average')]},"Tendencia: medias móviles de 3 y 12 meses",sort=(C('DimDate','MonthStartDate'),'Ascending'),objects=LEG_B))
p.add('mx',1236,680,660,352,chart('pivotTable',{"Rows":[C('DimDate','YearLabel')],"Columns":[C('DimDate','MonthNameShort')],"Values":[M('Total Traffic Violations')]},"Matriz año × mes",objects={"values":[{"properties":{"fontSize":lit(8)}}],"columnHeaders":[{"properties":{"fontSize":lit(8)}}],"rowHeaders":[{"properties":{"fontSize":lit(8)}}]}))
p.add('note',24,1038,1872,34,note('Partial Period Note'))
# ===== PAGE 3
p=Page(PIDS[2][0],PIDS[2][1],HASV); pages.append(p)
frame(p,2,"Ranking, concentración y evolución por tipo de infracción · categorías: clasificación propia del analista",[S_YEAR,S_CAT,('Top N','N','Top N',None,180),('Metric Selector','Metric','Métrica de la matriz',None,300)])
kp=[('Top Infraction Name','Principal tipo de infracción',17,TXT,True),('Top Infraction Share %','Participación del principal',30,Y,False),('Top 5 Infractions Share %','Concentración Top 5',30,Y,False),('Top 10 Infractions Share %','Concentración Top 10',30,Y,False),('Number of Infraction Types','Tipos con registros',30,Y,False)]
for i,(m_,t,s,c_,w_) in enumerate(kp): p.add(f'k{i}',24+i*378,176,360,112,card(m_,t,s,c_,w_))
p.add('rank',24,304,860,400,chart('clusteredBarChart',{"Category":[C('DimInfraction','InfractionType')],"Y":[M('Violations Top N')]},"Ranking de infracciones (Top N dinámico)",sort=(M('Violations Top N'),'Descending'),objects=LBL))
p.add('pareto',900,304,996,400,chart('lineClusteredColumnComboChart',{"Category":[C('DimInfraction','InfractionType')],"Y":[M('Violations Top N')],"Y2":[M('Cumulative Share Top N')]},"Pareto: infracciones y participación acumulada",sort=(M('Violations Top N'),'Descending'),objects=LEG_B))
p.add('mx',24,720,1160,312,chart('pivotTable',{"Rows":[C('DimInfraction','InfractionCategory'),C('DimInfraction','InfractionType')],"Columns":[C('DimDate','YearLabel')],"Values":[M('Selected Metric')]},None,title_measure='Selected Metric Label',objects={"values":[{"properties":{"fontSize":lit(9)}}],"columnHeaders":[{"properties":{"fontSize":lit(9)}}],"rowHeaders":[{"properties":{"fontSize":lit(9)}}]}))
p.add('tbl',1200,720,696,312,chart('tableEx',{"Values":[C('DimInfraction','InfractionType'),C('DimInfraction','LegalReference'),M('Total Traffic Violations'),M('Infraction Share %'),M('YoY Growth %')]},"Detalle por tipo",sort=(M('Total Traffic Violations'),'Descending'),objects={"values":[{"properties":{"fontSize":lit(9)}}],"columnHeaders":[{"properties":{"fontSize":lit(9)}}]}))
p.add('note',24,1038,1872,34,note('Partial Period Note'))
# ===== PAGE 4
p=Page(PIDS[3][0],PIDS[3][1],HASV); pages.append(p)
frame(p,3,"Patrones mensuales y estacionales · solo períodos con datos publicados",[S_YEAR,S_CAT,S_TYPE])
kp=[('Maximum Monthly Violations','Mes más alto',30,Y,False),('Minimum Monthly Violations','Mes más bajo',30,Y,False),('Average Monthly Violations','Promedio mensual',30,Y,False),('Months with Data','Meses con datos',30,Y,False),('Latest Year YoY Label','Variación interanual (último año)',20,TXT,True)]
for i,(m_,t,s,c_,w_) in enumerate(kp): p.add(f'k{i}',24+i*378,176,360,112,card(m_,t,s,c_,w_))
p.add('heat',24,304,1100,400,chart('pivotTable',{"Rows":[C('DimDate','YearLabel')],"Columns":[C('DimDate','MonthNameShort')],"Values":[M('Total Traffic Violations')]},"Mapa de calor: infracciones por año y mes",
   objects={"values":gradient('Total Traffic Violations')+[{"properties":{"fontSize":lit(12)}}],"columnHeaders":[{"properties":{"fontSize":lit(12)}}],"rowHeaders":[{"properties":{"fontSize":lit(12)}}],"subTotals":[{"properties":{"rowSubtotals":lit(False),"columnSubtotals":lit(False)}}]}))
p.add('avgm',1140,304,756,400,chart('clusteredColumnChart',{"Category":[C('DimDate','MonthNameShort')],"Y":[M('Average Monthly Violations')]},"Promedio de infracciones por mes del año",sort=(C('DimDate','MonthNameShort'),'Ascending'),objects=LBL))
p.add('mom',24,720,1100,312,chart('clusteredColumnChart',{"Category":[C('DimDate','MonthStartDate')],"Y":[M('MoM Growth %')]},"Variación mensual (MoM %)",sort=(C('DimDate','MonthStartDate'),'Ascending')))
p.add('qtr',1140,720,756,312,chart('hundredPercentStackedColumnChart',{"Category":[C('DimDate','YearLabel')],"Series":[C('DimDate','Quarter')],"Y":[M('Total Traffic Violations')]},"Distribución por trimestre (% del año)",sort=(C('DimDate','YearLabel'),'Ascending'),objects=LEG_B))
p.add('note',24,1038,1872,34,note('Partial Period Note'))
# ===== PAGE 5
p=Page(PIDS[4][0],PIDS[4][1]); pages.append(p)
frame(p,4,"Fallecimientos por accidentes de tránsito 2016–2025 · total nacional mensual · sin relación causal implícita con las infracciones",[S_YEAR,S_MONTH])
kp=[('Total Road Fatalities','Fallecimientos registrados',30,RED,False),('Average Monthly Fatalities','Promedio mensual de fallecimientos',30,TXT,False),('Latest Year Fatalities YoY Label','Variación interanual (último año)',20,TXT,True),('Fatalities (Common Period)','Fallecimientos 2018–2025 (período común)',30,TXT,False),('Violations (Common Period)','Infracciones 2018–2025 (período común)',30,Y,False)]
for i,(m_,t,s,c_,w_) in enumerate(kp): p.add(f'k{i}',24+i*378,176,360,112,card(m_,t,s,c_,w_))
p.add('faty',24,304,620,360,chart('clusteredColumnChart',{"Category":[C('DimDate','YearLabel')],"Y":[M('Total Road Fatalities')]},"Fallecimientos por año",sort=(C('DimDate','YearLabel'),'Ascending'),objects={**LBL,"dataPoint":[{"properties":{"fill":col(RED)}}]}))
p.add('both',660,304,700,360,chart('lineChart',{"Category":[C('DimDate','YearLabel')],"Y":[M('Index Violations'),M('Index Fatalities')]},"Infracciones y fallecimientos · índice 2018 = 100 (misma escala)",sort=(C('DimDate','YearLabel'),'Ascending'),objects={**LEG_B,**LBL,"dataPoint":[{"properties":{"fill":col(Y)},"selector":{"metadata":"_Measures.Index Violations"}},{"properties":{"fill":col(RED)},"selector":{"metadata":"_Measures.Index Fatalities"}}]}))
p.add('txt',1376,304,520,360,textbox([[("Cómo leer esta página",{"fontWeight":"bold","fontSize":"13pt","color":Y})],
  [("• Las infracciones registradas miden también la intensidad de la fiscalización, no solo la conducta de los conductores.",{"fontSize":"10pt","color":TXT})],
  [("• Los fallecimientos son totales nacionales por mes: la fuente no los desglosa por tipo de infracción, provincia ni tipo de vehículo.",{"fontSize":"10pt","color":TXT})],
  [("• Ver ambas series juntas no implica causalidad.",{"fontSize":"10pt","color":TXT})],
  [("• Las tasas por habitante y por vehículo están en la página Riesgo vial (población del Banco Mundial y parque vehicular de la DGII).",{"fontSize":"10pt","color":TXT})],
  [("• Datos que ayudarían: accidentes y lesionados por provincia, tipo de vehículo, hora y vía; kilómetros recorridos.",{"fontSize":"10pt","color":SUB})]]),extra=None)
p.add('fheat',24,680,1100,352,chart('pivotTable',{"Rows":[C('DimDate','YearLabel')],"Columns":[C('DimDate','MonthNameShort')],"Values":[M('Total Road Fatalities')]},"Mapa de calor: fallecimientos por año y mes",
   objects={"values":gradient('Total Road Fatalities',hi=RED)+[{"properties":{"fontSize":lit(12)}}],"columnHeaders":[{"properties":{"fontSize":lit(12)}}],"rowHeaders":[{"properties":{"fontSize":lit(12)}}],"subTotals":[{"properties":{"rowSubtotals":lit(False),"columnSubtotals":lit(False)}}]}))
p.add('favg',1140,680,756,352,chart('clusteredColumnChart',{"Category":[C('DimDate','MonthNameShort')],"Y":[M('Average Monthly Fatalities')]},"Promedio de fallecimientos por mes del año",sort=(C('DimDate','MonthNameShort'),'Ascending'),objects={**LBL,"dataPoint":[{"properties":{"fill":col(RED)}}]}))
p.add('warn',24,1036,1872,36,textbox([[("Fuente: DIGESETT · datos.gov.do · Fallecimientos 2016–2025 · Infracciones 2018–sep. 2026 · Elaboración propia",{"fontSize":"9pt","color":SUB})]]))

# ===== PAGE 6 · Riesgo vial
p=Page(PIDS[5][0],PIDS[5][1]); pages.append(p)
frame(p,5,"Tasas por habitante y por vehículo, control estadístico de fallecimientos, composición y proyección",[])
p.add('intro',24,96,1872,70,textbox([[("Totales nacionales: esta página no responde a filtros. ",{"fontSize":"10pt","color":TXT,"fontWeight":"bold"}),("Población: Banco Mundial (WDI SP.POP.TOTL). Parque vehicular: DGII, al 31 de diciembre (2017–2022 redondeado a miles). Alto riesgo: factores de riesgo de la OMS y maniobras peligrosas. Las tasas describen; no explican causas.",{"fontSize":"10pt","color":SUB})],
  [("",{"fontSize":"9pt","color":SUB})]]))
kp=[('Fatalities per 100k Inhabitants (Latest Year)','Fallecimientos por 100,000 habitantes',30,RED,False),('Fatalities per 10k Vehicles (Latest Year)','Fallecimientos por 10,000 vehículos',30,TXT,False),('Violations per 1k Vehicles (Latest Year)','Infracciones por 1,000 vehículos',30,Y,False),('High Risk Share % (Latest Year)','Infracciones de alto riesgo (%)',30,Y,False),('Projected Year-End Violations','Proyección de cierre del año parcial',30,TXT,False)]
for i,(m_,t,s_,c_,w_) in enumerate(kp): p.add(f'k{i}',24+i*378,176,360,100,card(m_,t,s_,c_,w_))
p.add('sub1',24,276,1100,26,note('Latest Year Rates Label'))
p.add('sub2',1536,276,360,26,note('Projection Range Label'))
p.add('rates',24,304,600,360,chart('lineClusteredColumnComboChart',{"Category":[C('DimDate','YearLabel')],"Y":[M('Fatalities per 100k Inhabitants')],"Y2":[M('Fatalities per 10k Vehicles')]},"Tasas de fallecimientos por año",sort=(C('DimDate','YearLabel'),'Ascending'),objects={**LEG_B,**LBL,"dataPoint":[{"properties":{"fill":col(RED)},"selector":{"metadata":"_Measures.Fatalities per 100k Inhabitants"}},{"properties":{"fill":col('#F4A7A8')},"selector":{"metadata":"_Measures.Fatalities per 10k Vehicles"}}]}))
p.add('index',640,304,600,360,chart('lineChart',{"Category":[C('DimDate','YearLabel')],"Y":[M('Index Violations'),M('Index Fatalities'),M('Index Vehicle Fleet'),M('Index Population')]},"Crecimiento comparado · índice 2018 = 100",sort=(C('DimDate','YearLabel'),'Ascending'),objects={**LEG_B,"dataPoint":[{"properties":{"fill":col(Y)},"selector":{"metadata":"_Measures.Index Violations"}},{"properties":{"fill":col(RED)},"selector":{"metadata":"_Measures.Index Fatalities"}},{"properties":{"fill":col(TEAL)},"selector":{"metadata":"_Measures.Index Vehicle Fleet"}},{"properties":{"fill":col('#8FA3B8')},"selector":{"metadata":"_Measures.Index Population"}}]}))
p.add('mix',1256,304,640,360,chart('hundredPercentStackedColumnChart',{"Category":[C('DimDate','YearLabel')],"Series":[C('DimInfraction','RiskGroup')],"Y":[M('Total Traffic Violations')]},"Composición: alto riesgo vs. documentación vs. resto",sort=(C('DimDate','YearLabel'),'Ascending'),objects=LEG_B))
p.add('ctl',24,680,1240,352,chart('lineChart',{"Category":[C('DimDate','MonthStartDate')],"Y":[M('Total Road Fatalities'),M('Fatalities Control Center'),M('Fatalities UCL'),M('Fatalities LCL'),M('Fatalities Out of Control')]},"Gráfico de control (I) de fallecimientos mensuales · límites con base 2016–2019",sort=(C('DimDate','MonthStartDate'),'Ascending'),
  objects={**LEG_B,"dataPoint":[{"properties":{"fill":col(RED)},"selector":{"metadata":"_Measures.Total Road Fatalities"}},{"properties":{"fill":col('#A7AEB6')},"selector":{"metadata":"_Measures.Fatalities Control Center"}},{"properties":{"fill":col('#6C757D')},"selector":{"metadata":"_Measures.Fatalities UCL"}},{"properties":{"fill":col('#6C757D')},"selector":{"metadata":"_Measures.Fatalities LCL"}},{"properties":{"fill":col('#FFFFFF')},"selector":{"metadata":"_Measures.Fatalities Out of Control"}}],
   "lineStyles":[{"properties":{"strokeWidth":lit(1)}},{"properties":{"lineStyle":lit("dashed")},"selector":{"metadata":"_Measures.Fatalities UCL"}},{"properties":{"lineStyle":lit("dashed")},"selector":{"metadata":"_Measures.Fatalities LCL"}},{"properties":{"lineStyle":lit("dotted")},"selector":{"metadata":"_Measures.Fatalities Control Center"}},{"properties":{"showMarker":lit(True),"markerSize":lit(6),"strokeWidth":lit(0)},"selector":{"metadata":"_Measures.Fatalities Out of Control"}}]}))
p.add('hhi',1280,680,616,352,chart('lineClusteredColumnComboChart',{"Category":[C('DimDate','YearLabel')],"Y":[M('HHI Index')],"Y2":[M('Top 5 Infractions Share %')]},"Concentración de la fiscalización (HHI y Top 5)",sort=(C('DimDate','YearLabel'),'Ascending'),objects=LEG_B))
p.add('note',24,1038,1872,34,textbox([[("Fuentes: DIGESETT (datos.gov.do), Banco Mundial (WDI), DGII (Informe Parque Vehicular) · Elaboración propia · La proyección es una estimación con el patrón estacional de años completos (sin 2020)",{"fontSize":"9pt","color":SUB})]]))
for p in pages: p.write()
json.dump({"$schema":"https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.1.0/schema.json","pageOrder":[x[0] for x in PIDS],"activePageName":PIDS[0][0]},open(OUT+'/pages/pages.json','w'),indent=2)
print(sum(len(p.vis) for p in pages),'visuals')
