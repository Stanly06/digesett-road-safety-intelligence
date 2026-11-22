"""Prueba de calidad de la versión web.

Compara las medidas que calcula la página (JavaScript) contra qa/reference.py
(pandas, misma lógica DAX escrita de forma independiente) y prueba el filtrado
cruzado con clics reales en un navegador sin interfaz.

Uso:
    pip install -r qa/requirements.txt && python -m playwright install chromium
    python qa/test_web.py            # opcional: QA_CONTEXTS=300 para más combinaciones
Sale con código 1 si hay cualquier diferencia.
"""
import asyncio, functools, http.server, math, os, random, sys, threading
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).parent))
import reference as ref  # noqa: E402
from playwright.async_api import async_playwright  # noqa: E402

N_CTX = int(os.environ.get("QA_CONTEXTS", "150"))
SL = {"overview": ["y", "m", "cat", "type"], "tendencias": ["y", "cat", "type"], "infracciones": ["y", "cat"],
      "estacionalidad": ["y", "cat", "type"], "seguridad-vial": ["y", "m"]}


def serve():
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT / "web"))
    h.log_message = lambda *a: None
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), h)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, f"http://127.0.0.1:{srv.server_address[1]}/index.html"


def close(a, b):
    if a is None or b is None:
        return a is None and b is None
    if isinstance(a, (str, bool)) or isinstance(b, (str, bool)):
        return a == b
    return math.isclose(float(a), float(b), rel_tol=1e-9, abs_tol=1e-9)


def contexts():
    random.seed(7)
    cats = sorted(ref.d.InfractionCategory.unique())
    out = [{"y": None, "m": None, "q": None, "cat": None, "type": None},
           {"y": 2016, "m": None, "q": None, "cat": None, "type": None},
           {"y": 2026, "m": 11, "q": None, "cat": None, "type": None}]
    for _ in range(N_CTX):
        c = {"y": random.choice([None] * 3 + list(range(2016, 2027))), "m": random.choice([None] * 2 + list(range(1, 13))),
             "q": random.choice([None] * 3 + [1, 2, 3, 4]), "cat": random.choice([None] * 2 + cats), "type": None}
        if random.random() < 0.35:
            pool = ref.d[ref.d.InfractionCategory == c["cat"]] if c["cat"] else ref.d
            c["type"] = int(random.choice(list(pool.InfractionID)))
        out.append(c)
    return out


async def main() -> int:
    srv, url = serve()
    fails = checks = 0

    def chk(name, got, exp):
        nonlocal fails, checks
        checks += 1
        if not close(got, exp):
            fails += 1
            if fails <= 30:
                print("FAIL", name, "web=", got, "ref=", exp)

    async with async_playwright() as p:
        exe = os.environ.get("CHROME_PATH")
        br = await p.chromium.launch(executable_path=exe, args=["--no-sandbox"]) if exe else await p.chromium.launch()
        pg = await br.new_page(viewport={"width": 1600, "height": 1000})
        local_echarts = os.environ.get("QA_ECHARTS_FILE")  # opcional: copia local de echarts.min.js si no hay acceso al CDN
        if local_echarts:
            async def route(r):
                if "echarts" in r.request.url:
                    await r.fulfill(path=local_echarts)
                elif r.request.url.startswith("http://127.0.0.1"):
                    await r.continue_()
                else:
                    await r.abort()
            await pg.route("**/*", route)
        errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)))
        await pg.goto(url + "#overview")
        await pg.wait_for_function("window.__ready===true", timeout=60000)

        # 1) medidas por página y por combinación de filtros
        for ctx in contexts():
            for page, sl in SL.items():
                c = {k: (ctx.get(k) if k in sl else None) for k in ["y", "m", "cat", "type"]}
                c["q"] = ctx.get("q")
                web = await pg.evaluate("([p,c])=>measures(p,c)", [page, c])
                for k, v in ref.measures(page, c).items():
                    chk(f"{page} {c} {k}", web.get(k), v)
            c = {k: ctx.get(k) for k in ["y", "cat", "type", "q"]}
            c["m"] = None
            web = await pg.evaluate("""(c)=>{const E=ENGINE,ds=E.dates(c);return E.years().map(y=>{const mis=ds.filter(mi=>E.yOf(mi)===y),v=E.T(E.sel(mis,c)),r=E.yoy(mis,c);return v==null?null:[y,v,r.g,r.abs]}).filter(Boolean)}""", c)
            exp = ref.year_series(c)
            chk(f"year_series {c} len", len(web), len(exp))
            for a, b in zip(web, exp):
                for i in range(4):
                    chk(f"year_series {c} {a[0]}", a[i], b[i])
            mis = [mi for mi in ref.dates(c) if ref.T(ref.V([mi], c)) is not None][:24]
            r = await pg.evaluate("([mis,c])=>mis.map(mi=>[ENGINE.rolling(mi,12,c),ENGINE.rolling(mi,3,c),ENGINE.mom(mi,c).g])", [mis, c])
            for mi, (a, b, g) in zip(mis, r):
                chk(f"r12 {mi}", a, ref.rolling(mi, 12, c)); chk(f"r3 {mi}", b, ref.rolling(mi, 3, c)); chk(f"mom {mi}", g, ref.mom(mi, c))

        # 2) analítica avanzada
        A = await pg.evaluate("window.__analytics()")
        R = ref.ANALYTICS
        for r in A["rate"]:
            if r["f"] is None:
                continue
            chk(f"per100k {r['y']}", r["per100k"], R["rate"][r["y"]][0]); chk(f"per10k {r['y']}", r["per10kVeh"], R["rate"][r["y"]][1])
            if r["vioPer1kVeh"] is not None:
                chk(f"vio1k {r['y']}", r["vioPer1kVeh"], R["vio1k"][r["y"]])
        for k, a, b in zip(["CL", "UCL", "LCL"], [A["ctl"]["CL"], A["ctl"]["UCL"], A["ctl"]["LCL"]], R["ctl"]):
            chk(k, a, b)
        chk("control rule 1", str(sorted(map(tuple, A["ctl"]["r1"]))), str(sorted(R["r1"])))
        chk("control rule 2", A["ctl"]["r2"], R["r2"])
        for k, a, b in zip(["min", "med", "max"], [A["proj"]["min"], A["proj"]["med"], A["proj"]["max"]], R["proj"]):
            chk("proj " + k, a, b)
        for m in A["mix"]:
            hr, doc, hhi, t5 = R["mix"][m["y"]]
            chk(f"hr {m['y']}", m["hr"], hr); chk(f"doc {m['y']}", m["doc"], doc); chk(f"hhi {m['y']}", m["hhi"], hhi); chk(f"top5 {m['y']}", m["top5"], t5)

        # 3) filtrado cruzado con clics reales
        nf = lambda v: "—" if v is None else f"{round(v):,}"

        async def click(cid, s, i):
            await pg.evaluate(f"document.getElementById('{cid}').scrollIntoView({{block:'center'}})")
            x, y = await pg.evaluate("""([cid,s,i])=>{const c=echarts.getInstanceByDom(document.getElementById(cid));const L=c.getModel().getSeriesByIndex(s).getData().getItemLayout(i);const r=document.getElementById(cid).getBoundingClientRect();
              if(L.cx!==undefined){const a=(L.startAngle+L.endAngle)/2,rr=(L.r0+L.r)/2;return [r.left+L.cx+rr*Math.cos(a),r.top+L.cy+rr*Math.sin(a)];}
              return [r.left+L.x+L.width/2,r.top+L.y+L.height/2];}""", [cid, s, i])
            await pg.mouse.click(x, y); await pg.wait_for_timeout(250)

        txt = lambda i: pg.inner_text("#" + i)
        await pg.goto(url + "#overview"); await pg.wait_for_timeout(500)
        await click("o-year", 0, 7)
        chk("click año 2025", await txt("o-k1"), nf(ref.measures("overview", {"y": 2025})["total"]))
        await click("o-year", 0, 7)
        chk("segundo clic limpia", await pg.evaluate("window.__sel()"), None)
        await pg.goto(url + "#estacionalidad"); await pg.wait_for_timeout(500)
        await pg.click('#s-heat td[data-y="2020"][data-m="4"]'); await pg.wait_for_timeout(250)
        chk("celda abr 2020", await txt("s-k1"), nf(ref.measures("estacionalidad", {"y": 2020, "m": 4})["maxMonth"]))
        await pg.goto(url + "#seguridad-vial"); await pg.wait_for_timeout(500)
        await click("r-year", 0, 3)
        chk("fallecimientos 2019", await txt("r-k1"), nf(ref.measures("seguridad-vial", {"y": 2019})["fat"]))
        for page in ["hallazgos", "riesgo", "calidad", "tendencias", "infracciones"]:
            await pg.goto(url + "#" + page); await pg.wait_for_timeout(400)
        chk("errores de JavaScript", len(errors), 0)
        await br.close()
    srv.shutdown()
    print(f"checks={checks} fails={fails}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
