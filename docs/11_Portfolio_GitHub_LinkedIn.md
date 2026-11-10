# Textos para portafolio, GitHub y LinkedIn

---

## 1. Descripción corta del repositorio (GitHub "About")

**EN:** Power BI road-safety intelligence dashboard built on open DIGESETT data (Dominican Republic, 2018–2026): Power Query ETL, star schema, 60 DAX measures, PBIP/TMDL.

**Topics:** `power-bi` `dax` `power-query` `data-modeling` `star-schema` `business-intelligence` `road-safety` `dominican-republic` `pbip` `tmdl`

---

## 2. Tarjeta de proyecto para el portafolio

**Dominican Republic Traffic Violations & Road Safety Intelligence Platform**

Power BI dashboard on 13.3 million traffic violations and 18,785 road deaths recorded by DIGESETT. I cleaned and unified two inconsistent public files in Power Query, built a constellation star schema, and wrote 60 DAX measures that only compare equivalent periods. Every total reconciles with the source.

**Stack:** Power BI · Power Query (M) · DAX · TMDL / PBIR · Python (validation)

---

## 3. Sección "Projects" de LinkedIn

**Título:** Dominican Republic Traffic Violations & Road Safety Intelligence Platform

**Descripción:**
Dashboard de Power BI construido con datos abiertos de la DIGESETT: 13.3 millones de infracciones de tránsito (2018–2026) y 18,785 fallecimientos (2016–2025).

• ETL en Power Query: unpivot de meses, unificación de dos catálogos de infracciones (41 y 101 tipos) con una tabla de mapeo auditable y separación entre cero real y dato no publicado.
• Modelo dimensional en constelación con tabla de fechas, filtros unidireccionales y sin columnas calculadas.
• 60 medidas DAX: variaciones interanuales solo sobre períodos comparables, medias móviles, Top N dinámico, Pareto y títulos dinámicos.
• 5 páginas de análisis con diseño institucional; totales reconciliados con la fuente.

**Habilidades:** Power BI · DAX · Power Query · Data Modeling · Data Visualization

---

## 4. Publicación de LinkedIn (formato hook)

> Una de cada cuatro infracciones de tránsito registradas en República Dominicana es por no usar casco.
>
> Analicé 13.3 millones de infracciones y 18,785 fallecimientos publicados por la DIGESETT y construí un dashboard en Power BI para entenderlos.
>
> Lo que encontré:
>
> 🏍️ El casco representa el 27.2 % de todas las infracciones, y su peso subió de 26 % (2021) a 31 % (2025).
> 📋 Cinco tipos explican el 58 % del total: casco, licencia, seguro, luz roja y cinturón.
> 📈 De 2021 a 2025 las infracciones registradas crecieron 54.7 %.
> 📉 En 2026 van 17.2 % por debajo del mismo tramo de 2025.
> 🕯️ 2025 tuvo 2,172 fallecimientos, el máximo de la serie 2016–2025.
>
> Lo más interesante no fue el gráfico, fue la preparación:
>
> • El catálogo de infracciones cambió en 2019: 41 tipos pasaron a 101. Si no los unificas, las tendencias por tipo salen rotas.
> • Los meses aún no publicados venían como 0. Si los tratas como cero, 2026 parece un desplome.
> • Comparar 2026 (9 meses) con 2025 completo daría −36 %. Comparado con el mismo tramo: −17 %.
>
> Y una advertencia: más infracciones registradas no significa necesariamente más imprudencia. También puede significar más fiscalización.
>
> Stack: Power BI · Power Query · DAX · modelo estrella · PBIP
>
> ¿Qué dato agregarías para medir el riesgo vial de verdad?
>
> #PowerBI #DataAnalytics #BusinessIntelligence #DAX #SeguridadVial #RepúblicaDominicana

---

## 5. Guion de video (2–3 minutos)

| Tiempo | Pantalla | Qué decir |
|---|---|---|
| 0:00–0:15 | Executive Overview | El problema: datos públicos dispersos y difíciles de comparar |
| 0:15–0:45 | Power Query | Unpivot, mapeo de catálogos, cero real vs sin dato |
| 0:45–1:05 | Vista de modelo | Constelación, por qué no se relacionan los hechos |
| 1:05–1:30 | DAX | `Violations PY Comparable`: por qué 2026 da −17 % y no −36 % |
| 1:30–2:15 | Recorrido por las 5 páginas | 3 hallazgos y uso de Top N y selectores |
| 2:15–2:30 | Road Safety Insights | Correlación no es causalidad; qué datos faltan |
