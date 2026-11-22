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

## Interactivity

Like Power BI, clicking a bar, point, donut slice, heatmap cell, matrix row or table row cross-filters the KPI cards and the other visuals on the page; the selected element stays highlighted. Click it again, click an empty area, or use the "Selección" chip to clear it. Slicers are synced across pages, and each page only applies the slicers it shows.

## Quality check

The JavaScript measures were tested against an independent pandas implementation of the same DAX logic: 23,091 checks over 268 filter combinations (year, month, quarter, category, type) with 0 differences, plus 20 end-to-end click tests in a headless browser. Default values match the Power BI report (13,289,441 violations, −17.2% 2026 vs 2025, 58.2% Top 5, 18,785 deaths, +0.4% 2025 vs 2024).
