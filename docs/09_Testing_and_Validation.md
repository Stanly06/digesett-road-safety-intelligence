# Pruebas y validación

## Dominican Republic Traffic Violations & Road Safety Intelligence Platform

> Resultados reales de las pruebas ejecutadas en Power BI Desktop (9 y 10 de noviembre de 2026) contra cálculos independientes en Python sobre los archivos originales.

---

## 1. Resumen

| Bloque | Pruebas | Resultado |
|---|---:|---|
| Carga y transformación (Power Query) | 8 | ✅ 8 de 8 |
| Modelo y relaciones | 8 | ✅ 8 de 8 |
| Medidas DAX | 56 medidas validadas con valores esperados | ✅ todas coinciden |
| Medidas de presentación | 4 | 🟡 revisadas en pantalla; sin cálculo independiente |
| Visuales | 99 visuales en 5 páginas | ✅ cargan sin errores |
| Interacción (navegación, sincronización, Top N) | 6 | ⬜ pendiente |

---

## 2. Power Query

| # | Prueba | Esperado | Obtenido |
|---|---|---:|---:|
| PQ-01 | Filas de `stg_Infracciones` | 10,188 | 10,188 |
| PQ-02 | `qa_InfraccionesSinMapear` | 0 | 0 |
| PQ-03 | Filas de `FactTrafficViolations` | 9,580 | 9,580 |
| PQ-04 | Suma de `ViolationCount` | 13,289,441 | 13,289,441 |
| PQ-05 | `InfractionID` nulos | 0 | 0 |
| PQ-06 | Rango de fechas de infracciones | 2018-01-01 a 2026-09-01 | 2018-01-01 a 2026-09-01 |
| PQ-07 | Filas / suma de `FactRoadFatalities` | 120 / 18,785 | 120 / 18,785 |
| PQ-08 | Filas de `DimInfraction` | 106 | 106 |

La limpieza no cambia el total (13,289,441 antes y después): las 608 filas eliminadas valían 0.

## 3. Modelo

| # | Prueba | Resultado |
|---|---|---|
| MO-01 | Filas de `DimDate` | 4,018 ✅ |
| MO-02 | 3 relaciones 1:* unidireccionales | ✅ |
| MO-03 | `DimDate` marcada como tabla de fechas | ✅ |
| MO-04 | Fecha y hora automáticas desactivadas | ✅ |
| MO-05 | Totales por año (infracciones y fallecimientos) = fuente | ✅ (tabla abajo) |
| MO-06 | Filtrar por categoría no altera fallecimientos | ✅ por diseño (sin relación); revisado en el modelo |
| MO-07 | Sin filas en blanco por claves huérfanas | ✅ (`InfractionID` nulos = 0) |
| MO-08 | Columnas ordenadas (meses, trimestres, `YearLabel`) | ✅ |

| Año | Infracciones | Fallecimientos | Tipos | Filas |
|---|---:|---:|---:|---:|
| 2016 | — | 1,993 | — | — |
| 2017 | — | 1,588 | — | — |
| 2018 | 812,930 | 1,427 | 41 | 492 |
| 2019 | 1,003,852 | 2,095 | 101 | 907 |
| 2020 | 614,808 | 1,732 | 101 | 1,212 |
| 2021 | 1,522,201 | 1,867 | 101 | 1,212 |
| 2022 | 2,026,132 | 1,795 | 101 | 1,212 |
| 2023 | 1,503,418 | 1,952 | 101 | 1,212 |
| 2024 | 1,948,238 | 2,164 | 101 | 1,212 |
| 2025 | 2,355,349 | 2,172 | 101 | 1,212 |
| 2026 | 1,502,513 | — | 101 | 909 |

## 4. Medidas DAX (valores verificados)

| Medida | Contexto | Esperado | Power BI |
|---|---|---:|---:|
| `Violations PY Comparable` | 2026 | 1,814,990 | 1,814,990 |
| `YoY Growth %` | 2026 | −17.22 % | −17.22 % |
| `YoY Growth %` | 2021 | +147.59 % | +147.59 % |
| `Average Monthly Violations` | 2026 | 166,945.9 | 166,945.9 |
| `Number of Infraction Types` | 2020 | 100 | 100 |
| `Maximum / Minimum Monthly Violations` | 2020 | 98,884 / 2,649 | 98,884 / 2,649 |
| `Top 5 Infractions Share %` | 2025 | 63.87 % | 63.87 % |
| `Total Violations YTD PY` | 2026 | 1,814,990 | 1,814,990 |
| `Average Annual Violations` | todo | 1,473,366.0 | 1,473,366.0 |
| `Top Infraction Name` | todo | No Uso del Casco Protector | ✅ |
| `Top Infraction Share %` | todo | 27.21 % | 27.21 % |
| `Top 5 / Top 10 Infractions Share %` | todo | 58.25 % / 74.85 % | 58.25 % / 74.85 % |
| `Rolling 3M Violations` | sep-2026 | 494,249 | 494,249 |
| `Rolling 12M Violations` | sep-2026 | 2,042,872 | 2,042,872 |
| `Rolling 3M Violations` | feb-2018 (ventana incompleta) | blanco | blanco |
| `MoM Growth %` / `MoM Absolute Change` | sep-2026 | −6.05 % / −9,860 | −6.05 % / −9,860 |
| `MoM Growth %` | oct-2026 (sin dato) | blanco | blanco |
| `YoY Growth %` casco | 2020 | −28.35 % | −28.35 % |
| `YoY Growth %` tipo que empezó en jun-2019 | 2020 | blanco | blanco |
| `Violations (Common Period)` | todo | 11,786,928 | 11,786,928 |
| `Fatalities (Common Period)` | todo | 15,204 | 15,204 |
| `Fatalities YoY %` | 2025 | +0.37 % | +0.37 % |
| `Average Monthly Fatalities` | todo | 156.542 | 156.542 |
| `Infraction Ranking` / `Cumulative Infraction Share %` | top 6 | 1–6 / 27.2 %…63.1 % | ✅ |
| `Partial Period Note` | 2024 | vacío | vacío |
| `Dynamic KPI Title` | 2025 + Protección personal | "Infracciones de tránsito · 2025 · Protección personal" | ✅ |
| `Infraction Filter Warning` | con filtro de infracción | aviso | ✅ |

## 5. Pruebas pendientes (checklist)

- [ ] Ctrl + clic en cada botón de navegación lleva a la página correcta (5 × 5).
- [ ] Elegir un año en una página lo mantiene en las demás (sincronización).
- [ ] Top N = 5 deja 5 barras en el ranking y el Pareto.
- [ ] Selector de métrica cambia valores y formato de la matriz.
- [ ] Selector de comparación cambia el gráfico de cambio absoluto.
- [ ] Filtrar una categoría en la página 5 muestra el aviso y no cambia los fallecimientos.
- [ ] Performance Analyzer: ningún visual por encima de 500 ms.
- [ ] Revisión con Best Practice Analyzer (Tabular Editor).

## 6. Cómo repetir la validación

1. Ejecutar `scripts/01_profile_digesett.py` para el perfilado.
2. Comparar con `data/validation/control_totals_violations.csv`.
3. En la vista de consultas DAX de Power BI, ejecutar `SUMMARIZECOLUMNS` por año con `[Total Traffic Violations]` y `[Total Road Fatalities]`.
