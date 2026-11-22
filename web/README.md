# Web version of the report

Interactive HTML version of the five Power BI pages, built with [Apache ECharts](https://echarts.apache.org/) from the same validated data (`data.json` is generated from `data/validation/` and `data/reference/`).

**Live:** https://stanly06.github.io/digesett/

It exists so the report can be explored without a Power BI account. The `.pbip` project remains the main deliverable.

To open it locally, serve the folder (the page loads `data.json` with `fetch`):

```bash
cd web
python -m http.server 8000
# then open http://localhost:8000
```
