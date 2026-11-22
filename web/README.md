# Web version of the report

Interactive HTML version of the five Power BI pages: same slicers, KPIs and visuals per page, with the DAX measures re-implemented in JavaScript. Built with [Apache ECharts](https://echarts.apache.org/) from the same validated data (`data.json` is generated from `data/validation/` and `data/reference/`).

**Live:** https://stanly06.github.io/digesett/

It exists so the report can be explored without a Power BI account. The `.pbip` project remains the main deliverable.

To open it locally, serve the folder (the page loads `data.json` with `fetch`):

```bash
cd web
python -m http.server 8000
# then open http://localhost:8000
```

## Quality check

The JavaScript measures were tested against an independent pandas implementation of the same DAX logic: 27,513 checks over 268 filter combinations (year, month, category, type) with 0 differences. Default values match the Power BI report (13,289,441 violations, −17.2% 2026 vs 2025, 58.2% Top 5, 18,785 deaths, +0.4% 2025 vs 2024).
