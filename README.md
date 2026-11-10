# Dominican Republic Traffic Violations & Road Safety Intelligence Platform

A **Power BI** business intelligence project built on open data from **DIGESETT** (Dominican Republic's traffic and land-transport safety agency): **13.3 million traffic violations** (Jan 2018 – Sep 2026) and **18,785 road deaths** (2016–2025).

**Stack:** Power BI Desktop · Power Query (M) · DAX · PBIP (TMDL + PBIR) · Python for validation

> **Independent portfolio project.** Not an official DIGESETT product. Technical documentation is in Spanish, in [`docs/`](docs/README.md).

<!-- Add screenshots here: docs/assets/overview.png ... -->

---

## Business problem

DIGESETT publishes its data as wide Excel files: one column per month, no indicators, a violations catalog that changes between 2018 (41 types) and 2019 onward (101 types), and unpublished months stored as `0`. Comparing a violation type across years, or comparing a partial year with a full one, produces misleading results.

## Key findings

| Finding | Value |
|---|---|
| Recorded violations, 2025 (highest year) | 2,355,349 |
| Growth 2021 → 2025 (same catalog) | +54.7 % |
| Not wearing a helmet, share of all violations | 27.2 % (31.3 % in 2025) |
| Top 5 / Top 10 violation types, share of total | 58.2 % / 74.8 % |
| Jan–Sep 2026 vs Jan–Sep 2025 | −17.2 % |
| Road deaths, 2025 (highest in 2016–2025) | 2,172 |

Full answers, with observations separated from hypotheses: [Business Questions & Insights](docs/business/02_Business_Questions_and_Insights.md).

## What's built

| Layer | Details |
|---|---|
| **ETL (Power Query)** | Unpivot of 12 month columns; auditable CSV mapping that unifies two violation catalogs (36 of 41 legacy types mapped, 5 kept as their own); removal of unpublished and not-yet-recorded months so a `0` always means zero; a QA query that flags any new unmapped name |
| **Model** | Constellation schema: `FactTrafficViolations` (violation × month) and `FactRoadFatalities` (month) share a conformed `DimDate`; `DimInfraction`; single-direction filters; no calculated columns |
| **DAX** | 60 measures in 5 folders: year-over-year only on comparable months, rolling 3/6/12-month windows that require complete windows, dynamic Top N, Pareto, dynamic titles and partial-period notes |
| **Report** | 5 pages: Executive Overview, Historical Trends, Infraction Analysis, Monthly & Seasonal, Road Safety Insights; institutional header, custom theme, synced slicers |
| **Validation** | Every yearly total and 56 measures reconciled against an independent Python calculation |

## Repository structure

```
├── DIGESETT_Road_Safety_Intelligence.pbip     # open in Power BI Desktop
├── DIGESETT_Road_Safety_Intelligence.Report/  # report definition (PBIR)
├── DIGESETT_Road_Safety_Intelligence.SemanticModel/  # model (TMDL)
├── data/
│   ├── raw/          # DIGESETT source files
│   ├── reference/    # MapInfraction.csv, DimInfraction.csv
│   └── validation/   # control totals
├── powerquery/       # M code, one file per query
├── dax/              # measure library
├── model/            # TMDL scripts
├── theme/            # Power BI theme JSON
├── scripts/          # Python profiling
└── docs/             # documentation (Spanish)
```

## How to run

1. Install Power BI Desktop and open `DIGESETT_Road_Safety_Intelligence.pbip`.
2. *Transform data → Manage parameters → `pRutaDatos`*: set the full path to the `data\` folder, ending in `\`.
3. Refresh. Expected totals: 13,289,441 violations and 18,785 deaths.

## Limitations

- Recorded violations reflect enforcement as well as behavior; a rise does not prove riskier driving.
- Deaths are national monthly totals, with no breakdown by violation, province or vehicle; the charts show both series side by side and make no causal claim.
- No exposure data (vehicles, population, distance), so no rates are calculated.
- Violation categories are the analyst's own grouping, not an official DIGESETT classification.

## Data source

DIGESETT, *Estadísticas de infracciones de tránsito* and *Fallecimientos según meses*, published on [datos.gov.do](https://datos.gov.do/dataset/estadisticas-de-infracciones-de-transito).

## Author

**Stanly Fernández** · Industrial engineer · MBA and Master's in Big Data & Business Intelligence
