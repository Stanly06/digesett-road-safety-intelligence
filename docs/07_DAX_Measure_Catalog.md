# Catálogo de medidas DAX

## Dominican Republic Traffic Violations & Road Safety Intelligence Platform

> **60 medidas en la tabla `_Measures`, organizadas en 5 carpetas. Fórmulas completas, listas para pegar; también disponibles en `dax/DIGESETT_Measures.dax` y como script TMDL en `model/DIGESETT_measures.tmdl`.**

---

## Principios de diseño

| Principio | Cómo se aplica |
|---|---|
| Una medida base | Todo parte de `Total Traffic Violations` o `Total Road Fatalities`; no se repiten agregaciones |
| Cero ≠ sin dato | Fila con 0 = cero real; ausencia de fila = sin dato. `Months with Data` cuenta meses con filas, no meses del calendario |
| Períodos comparables | `Violations PY Comparable` devuelve blanco si el año actual y el anterior no tienen los mismos meses con datos |
| Sin fechas escritas a mano | El último mes publicado se calcula con `Last Data Month Index` |
| Divisiones seguras | `DIVIDE` en todas las razones |
| Variables | `VAR … RETURN` para evaluar cada expresión una sola vez y documentar la lógica |
| Ventanas por índice | Medias móviles y MoM usan `DimDate[MonthIndex]` (año × 12 + mes), sin depender de días |
| Color neutro | `KPI Color YoY` no pinta los aumentos en rojo: más infracciones registradas no implica más riesgo |

---

## Medidas clave explicadas paso a paso

### `Violations PY Comparable`

1. Toma los meses del contexto actual que tienen datos publicados (`MonthIndex <= Last Data Month Index`).
2. Les resta 12 para obtener los mismos meses del año anterior.
3. Cuenta cuántos de esos meses tienen datos en ambos períodos.
4. Solo si coinciden devuelve el valor del año anterior; si no, blanco.

Resultado: con el año 2026 seleccionado, compara enero–septiembre de 2026 contra enero–septiembre de 2025 (−17.2 %), no contra el año completo (−36.2 %). Para un tipo que empezó a registrarse en junio de 2019, la variación 2020 vs 2019 queda en blanco en lugar de mostrar un crecimiento falso.

### `Rolling 12M Violations`

Suma los 12 meses que terminan en el mes del contexto, pero solo si esa ventana tiene 12 meses con datos. Así la media móvil no arranca en enero de 2018 con un solo mes ni se desploma al llegar a octubre de 2026.

### `Cumulative Infraction Share %` (Pareto)

Calcula una tabla virtual con el total de cada tipo dentro de la selección (`ALLSELECTED`), suma los tipos con total mayor o igual al actual y divide entre el total. Respeta año, categoría y cualquier filtro del usuario.

### `Average Annual Violations`

Promedia el total por año usando solo años con `IsCompleteViolationYear = TRUE`. `KEEPFILTERS` mantiene la selección del usuario: si eligió 2024–2026, promedia solo 2024 y 2025.

---

## 01 Base

| Medida | Descripción | Formato |
|---|---|---|
| `Total Traffic Violations` | Infracciones registradas. Medida base: todas las demás parten de esta. | `#,0` |
| `Number of Infraction Types` | Tipos de infracción con al menos un registro en el contexto actual. | `#,0` |
| `Months with Data` | Meses que tienen filas en la tabla de hechos. Ausencia de fila = sin dato; fila con 0 = cero real. | `#,0` |
| `Average Monthly Violations` | Promedio por mes, dividiendo solo entre los meses que tienen datos. | `#,0` |
| `Average Annual Violations` | Promedio anual usando solo años completos (excluye el año parcial). | `#,0` |
| `Maximum Monthly Violations` | Valor del mes con más infracciones dentro del contexto. | `#,0` |
| `Minimum Monthly Violations` | Valor del mes con menos infracciones (solo meses con datos). | `#,0` |
| `Last Data Month Index` | Índice del último mes con infracciones publicadas, ignorando todos los filtros. | `0  (oculta)` |


### Total Traffic Violations

Infracciones registradas. Medida base: todas las demás parten de esta.

```dax
Total Traffic Violations =
SUM ( FactTrafficViolations[ViolationCount] )
```

### Number of Infraction Types

Tipos de infracción con al menos un registro en el contexto actual.

```dax
Number of Infraction Types =
COUNTROWS (
    FILTER ( VALUES ( DimInfraction[InfractionID] ), [Total Traffic Violations] > 0 )
)
```

### Months with Data

Meses que tienen filas en la tabla de hechos. Ausencia de fila = sin dato; fila con 0 = cero real.

```dax
Months with Data =
COUNTROWS ( SUMMARIZE ( FactTrafficViolations, DimDate[MonthIndex] ) )
```

### Average Monthly Violations

Promedio por mes, dividiendo solo entre los meses que tienen datos.

```dax
Average Monthly Violations =
DIVIDE ( [Total Traffic Violations], [Months with Data] )
```

### Average Annual Violations

Promedio anual usando solo años completos (excluye el año parcial).

```dax
Average Annual Violations =
AVERAGEX (
    CALCULATETABLE (
        VALUES ( DimDate[Year] ),
        KEEPFILTERS ( DimDate[IsCompleteViolationYear] = TRUE () )
    ),
    [Total Traffic Violations]
)
```

### Maximum Monthly Violations

Valor del mes con más infracciones dentro del contexto.

```dax
Maximum Monthly Violations =
MAXX ( SUMMARIZE ( FactTrafficViolations, DimDate[MonthIndex] ), [Total Traffic Violations] )
```

### Minimum Monthly Violations

Valor del mes con menos infracciones (solo meses con datos).

```dax
Minimum Monthly Violations =
MINX ( SUMMARIZE ( FactTrafficViolations, DimDate[MonthIndex] ), [Total Traffic Violations] )
```

### Last Data Month Index

Índice del último mes con infracciones publicadas, ignorando todos los filtros.

```dax
Last Data Month Index =
CALCULATE (
    MAX ( DimDate[MonthIndex] ),
    REMOVEFILTERS (),
    DimDate[HasViolationData] = TRUE ()
)
```

---

## 02 Time Intelligence

| Medida | Descripción | Formato |
|---|---|---|
| `Total Violations YTD` | Acumulado del año hasta el período en contexto. En blanco para meses aún no publicados. | `#,0` |
| `Total Violations YTD PY` | Acumulado del año anterior hasta el mismo mes. Si el año actual es parcial, corta el año anterior en el mismo mes. | `#,0` |
| `YTD Growth %` | Variación del acumulado anual frente al mismo tramo del año anterior. | `0.0%;-0.0%;0.0%` |
| `Total Violations Previous Year` | Mismo período del año anterior, sin ajustar (año completo). Usar como referencia, no para variaciones. | `#,0` |
| `Violations PY Comparable` | Año anterior limitado a los mismos meses que tienen datos hoy. Devuelve blanco si ambos períodos no tienen la misma cantidad de meses con datos. | `#,0` |
| `YoY Absolute Change` | Diferencia frente al mismo período comparable del año anterior. | `+#,0;-#,0;0` |
| `YoY Growth %` | Variación porcentual interanual sobre períodos comparables. | `0.0%;-0.0%;0.0%` |
| `Violations Previous Month` | Mes inmediatamente anterior. Solo se evalúa cuando hay un único mes en contexto. | `#,0` |
| `MoM Absolute Change` | Diferencia frente al mes anterior. | `+#,0;-#,0;0` |
| `MoM Growth %` | Variación porcentual frente al mes anterior. | `0.0%;-0.0%;0.0%` |
| `Rolling 3M Violations` | Suma móvil de 3 meses. En blanco si la ventana no tiene 3 meses con datos. | `#,0` |
| `Rolling 6M Violations` | Suma móvil de 6 meses. En blanco si la ventana no tiene 6 meses con datos. | `#,0` |
| `Rolling 12M Violations` | Suma móvil de 12 meses. En blanco si la ventana no tiene 12 meses con datos. | `#,0` |
| `Rolling 3M Average` | Media móvil de 3 meses. | `#,0` |
| `Rolling 12M Average` | Media móvil de 12 meses: suaviza la estacionalidad. | `#,0` |
| `Annual Share %` | Peso del período en contexto sobre todos los años seleccionados. | `0.0%;-0.0%;0.0%` |
| `Monthly Share %` | Peso del mes dentro de su año. | `0.0%;-0.0%;0.0%` |


### Total Violations YTD

Acumulado del año hasta el período en contexto. En blanco para meses aún no publicados.

```dax
Total Violations YTD =
VAR LastIdx = [Last Data Month Index]
RETURN
    IF (
        MIN ( DimDate[MonthIndex] ) <= LastIdx,
        CALCULATE ( [Total Traffic Violations], DATESYTD ( DimDate[Date] ) )
    )
```

### Total Violations YTD PY

Acumulado del año anterior hasta el mismo mes. Si el año actual es parcial, corta el año anterior en el mismo mes.

```dax
Total Violations YTD PY =
VAR LastIdx = [Last Data Month Index]
VAR EndIdx = MIN ( MAX ( DimDate[MonthIndex] ), LastIdx )
VAR StartIdx = MAX ( DimDate[Year] ) * 12 + 1
RETURN
    IF (
        MIN ( DimDate[MonthIndex] ) <= LastIdx,
        CALCULATE (
            [Total Traffic Violations],
            REMOVEFILTERS ( DimDate ),
            DimDate[MonthIndex] >= StartIdx - 12
                && DimDate[MonthIndex] <= EndIdx - 12
        )
    )
```

### YTD Growth %

Variación del acumulado anual frente al mismo tramo del año anterior.

```dax
YTD Growth % =
VAR Cur = [Total Violations YTD]
VAR Prev = [Total Violations YTD PY]
RETURN
    IF ( NOT ISBLANK ( Cur ) && NOT ISBLANK ( Prev ), DIVIDE ( Cur - Prev, Prev ) )
```

### Total Violations Previous Year

Mismo período del año anterior, sin ajustar (año completo). Usar como referencia, no para variaciones.

```dax
Total Violations Previous Year =
CALCULATE ( [Total Traffic Violations], SAMEPERIODLASTYEAR ( DimDate[Date] ) )
```

### Violations PY Comparable

Año anterior limitado a los mismos meses que tienen datos hoy. Devuelve blanco si ambos períodos no tienen la misma cantidad de meses con datos.

```dax
Violations PY Comparable =
VAR LastIdx = [Last Data Month Index]
VAR CurMonths =
    FILTER ( VALUES ( DimDate[MonthIndex] ), DimDate[MonthIndex] <= LastIdx )
VAR PYMonths =
    SELECTCOLUMNS ( CurMonths, "MonthIndex", DimDate[MonthIndex] - 12 )
VAR MonthsCur = [Months with Data]
VAR MonthsPY =
    CALCULATE (
        [Months with Data],
        REMOVEFILTERS ( DimDate ),
        TREATAS ( PYMonths, DimDate[MonthIndex] )
    )
VAR ValuePY =
    CALCULATE (
        [Total Traffic Violations],
        REMOVEFILTERS ( DimDate ),
        TREATAS ( PYMonths, DimDate[MonthIndex] )
    )
RETURN
    IF ( MonthsCur > 0 && MonthsCur = MonthsPY, ValuePY )
```

### YoY Absolute Change

Diferencia frente al mismo período comparable del año anterior.

```dax
YoY Absolute Change =
VAR Cur = [Total Traffic Violations]
VAR Prev = [Violations PY Comparable]
RETURN
    IF ( NOT ISBLANK ( Cur ) && NOT ISBLANK ( Prev ), Cur - Prev )
```

### YoY Growth %

Variación porcentual interanual sobre períodos comparables.

```dax
YoY Growth % =
VAR Cur = [Total Traffic Violations]
VAR Prev = [Violations PY Comparable]
RETURN
    IF ( NOT ISBLANK ( Cur ) && NOT ISBLANK ( Prev ), DIVIDE ( Cur - Prev, Prev ) )
```

### Violations Previous Month

Mes inmediatamente anterior. Solo se evalúa cuando hay un único mes en contexto.

```dax
Violations Previous Month =
VAR CurIdx = MAX ( DimDate[MonthIndex] )
RETURN
    IF (
        HASONEVALUE ( DimDate[MonthIndex] ),
        CALCULATE (
            [Total Traffic Violations],
            REMOVEFILTERS ( DimDate ),
            DimDate[MonthIndex] = CurIdx - 1
        )
    )
```

### MoM Absolute Change

Diferencia frente al mes anterior.

```dax
MoM Absolute Change =
VAR Cur = [Total Traffic Violations]
VAR Prev = [Violations Previous Month]
RETURN
    IF ( NOT ISBLANK ( Cur ) && NOT ISBLANK ( Prev ), Cur - Prev )
```

### MoM Growth %

Variación porcentual frente al mes anterior.

```dax
MoM Growth % =
VAR Cur = [Total Traffic Violations]
VAR Prev = [Violations Previous Month]
RETURN
    IF ( NOT ISBLANK ( Cur ) && NOT ISBLANK ( Prev ), DIVIDE ( Cur - Prev, Prev ) )
```

### Rolling 3M Violations

Suma móvil de 3 meses. En blanco si la ventana no tiene 3 meses con datos.

```dax
Rolling 3M Violations =
VAR CurIdx = MAX ( DimDate[MonthIndex] )
VAR MonthsInWindow =
    CALCULATE (
        [Months with Data],
        REMOVEFILTERS ( DimDate ),
        DimDate[MonthIndex] > CurIdx - 3
            && DimDate[MonthIndex] <= CurIdx
    )
RETURN
    IF (
        MonthsInWindow = 3 && NOT ISBLANK ( [Total Traffic Violations] ),
        CALCULATE (
            [Total Traffic Violations],
            REMOVEFILTERS ( DimDate ),
            DimDate[MonthIndex] > CurIdx - 3
                && DimDate[MonthIndex] <= CurIdx
        )
    )
```

### Rolling 6M Violations

Suma móvil de 6 meses. En blanco si la ventana no tiene 6 meses con datos.

```dax
Rolling 6M Violations =
VAR CurIdx = MAX ( DimDate[MonthIndex] )
VAR MonthsInWindow =
    CALCULATE (
        [Months with Data],
        REMOVEFILTERS ( DimDate ),
        DimDate[MonthIndex] > CurIdx - 6
            && DimDate[MonthIndex] <= CurIdx
    )
RETURN
    IF (
        MonthsInWindow = 6 && NOT ISBLANK ( [Total Traffic Violations] ),
        CALCULATE (
            [Total Traffic Violations],
            REMOVEFILTERS ( DimDate ),
            DimDate[MonthIndex] > CurIdx - 6
                && DimDate[MonthIndex] <= CurIdx
        )
    )
```

### Rolling 12M Violations

Suma móvil de 12 meses. En blanco si la ventana no tiene 12 meses con datos.

```dax
Rolling 12M Violations =
VAR CurIdx = MAX ( DimDate[MonthIndex] )
VAR MonthsInWindow =
    CALCULATE (
        [Months with Data],
        REMOVEFILTERS ( DimDate ),
        DimDate[MonthIndex] > CurIdx - 12
            && DimDate[MonthIndex] <= CurIdx
    )
RETURN
    IF (
        MonthsInWindow = 12 && NOT ISBLANK ( [Total Traffic Violations] ),
        CALCULATE (
            [Total Traffic Violations],
            REMOVEFILTERS ( DimDate ),
            DimDate[MonthIndex] > CurIdx - 12
                && DimDate[MonthIndex] <= CurIdx
        )
    )
```

### Rolling 3M Average

Media móvil de 3 meses.

```dax
Rolling 3M Average =
DIVIDE ( [Rolling 3M Violations], 3 )
```

### Rolling 12M Average

Media móvil de 12 meses: suaviza la estacionalidad.

```dax
Rolling 12M Average =
DIVIDE ( [Rolling 12M Violations], 12 )
```

### Annual Share %

Peso del período en contexto sobre todos los años seleccionados.

```dax
Annual Share % =
DIVIDE (
    [Total Traffic Violations],
    CALCULATE ( [Total Traffic Violations], ALLSELECTED ( DimDate ) )
)
```

### Monthly Share %

Peso del mes dentro de su año.

```dax
Monthly Share % =
DIVIDE (
    [Total Traffic Violations],
    CALCULATE (
        [Total Traffic Violations],
        REMOVEFILTERS ( DimDate ),
        VALUES ( DimDate[Year] )
    )
)
```

---

## 03 Infraction Analysis

| Medida | Descripción | Formato |
|---|---|---|
| `Infraction Share %` | Participación sobre el total de las infracciones seleccionadas. | `0.0%;-0.0%;0.0%` |
| `Infraction Ranking` | Posición del tipo de infracción respetando los filtros del usuario. | `0` |
| `Category Ranking` | Posición de la categoría respetando los filtros del usuario. | `0` |
| `Cumulative Infraction Share %` | Participación acumulada ordenando de mayor a menor (línea del Pareto). | `0.0%;-0.0%;0.0%` |
| `Top N Value` | Valor elegido en el segmentador Top N (10 por defecto). | `0` |
| `Violations Top N` | Infracciones solo para los tipos dentro del Top N dinámico. Usar como valor del gráfico. | `#,0` |
| `Top 5 Infractions Share %` | Porcentaje del total que concentran los 5 tipos principales. | `0.0%;-0.0%;0.0%` |
| `Top 10 Infractions Share %` | Porcentaje del total que concentran los 10 tipos principales. | `0.0%;-0.0%;0.0%` |
| `Top Infraction Name` | Nombre del tipo de infracción con más registros en el contexto. | `texto` |
| `Top Infraction Share %` | Participación del tipo de infracción principal. | `0.0%;-0.0%;0.0%` |
| `Contribution to YoY Growth %` | Puntos porcentuales que aporta el elemento a la variación interanual del total seleccionado. | `0.0%;-0.0%;0.0%` |


### Infraction Share %

Participación sobre el total de las infracciones seleccionadas.

```dax
Infraction Share % =
DIVIDE (
    [Total Traffic Violations],
    CALCULATE ( [Total Traffic Violations], ALLSELECTED ( DimInfraction ) )
)
```

### Infraction Ranking

Posición del tipo de infracción respetando los filtros del usuario.

```dax
Infraction Ranking =
IF (
    ISINSCOPE ( DimInfraction[InfractionType] )
        && NOT ISBLANK ( [Total Traffic Violations] ),
    RANKX (
        ALLSELECTED ( DimInfraction[InfractionType] ),
        [Total Traffic Violations],
        ,
        DESC,
        DENSE
    )
)
```

### Category Ranking

Posición de la categoría respetando los filtros del usuario.

```dax
Category Ranking =
IF (
    ISINSCOPE ( DimInfraction[InfractionCategory] )
        && NOT ISBLANK ( [Total Traffic Violations] ),
    RANKX (
        ALLSELECTED ( DimInfraction[InfractionCategory] ),
        [Total Traffic Violations],
        ,
        DESC,
        DENSE
    )
)
```

### Cumulative Infraction Share %

Participación acumulada ordenando de mayor a menor (línea del Pareto).

```dax
Cumulative Infraction Share % =
VAR Cur = [Total Traffic Violations]
VAR AllTypes =
    ADDCOLUMNS (
        ALLSELECTED ( DimInfraction[InfractionType] ),
        "@Violations", [Total Traffic Violations]
    )
VAR Cumulative =
    SUMX ( FILTER ( AllTypes, [@Violations] >= Cur ), [@Violations] )
RETURN
    IF (
        ISINSCOPE ( DimInfraction[InfractionType] ) && NOT ISBLANK ( Cur ),
        DIVIDE ( Cumulative, SUMX ( AllTypes, [@Violations] ) )
    )
```

### Top N Value

Valor elegido en el segmentador Top N (10 por defecto).

```dax
Top N Value =
SELECTEDVALUE ( 'Top N'[N], 10 )
```

### Violations Top N

Infracciones solo para los tipos dentro del Top N dinámico. Usar como valor del gráfico.

```dax
Violations Top N =
IF ( [Infraction Ranking] <= [Top N Value], [Total Traffic Violations] )
```

### Top 5 Infractions Share %

Porcentaje del total que concentran los 5 tipos principales.

```dax
Top 5 Infractions Share % =
VAR Types = VALUES ( DimInfraction[InfractionType] )
VAR TopTypes = TOPN ( 5, Types, [Total Traffic Violations], DESC )
RETURN
    DIVIDE (
        SUMX ( TopTypes, [Total Traffic Violations] ),
        SUMX ( Types, [Total Traffic Violations] )
    )
```

### Top 10 Infractions Share %

Porcentaje del total que concentran los 10 tipos principales.

```dax
Top 10 Infractions Share % =
VAR Types = VALUES ( DimInfraction[InfractionType] )
VAR TopTypes = TOPN ( 10, Types, [Total Traffic Violations], DESC )
RETURN
    DIVIDE (
        SUMX ( TopTypes, [Total Traffic Violations] ),
        SUMX ( Types, [Total Traffic Violations] )
    )
```

### Top Infraction Name

Nombre del tipo de infracción con más registros en el contexto.

```dax
Top Infraction Name =
CONCATENATEX (
    TOPN ( 1, VALUES ( DimInfraction[InfractionType] ), [Total Traffic Violations], DESC ),
    DimInfraction[InfractionType],
    ", "
)
```

### Top Infraction Share %

Participación del tipo de infracción principal.

```dax
Top Infraction Share % =
VAR Types = VALUES ( DimInfraction[InfractionType] )
RETURN
    DIVIDE (
        MAXX ( Types, [Total Traffic Violations] ),
        SUMX ( Types, [Total Traffic Violations] )
    )
```

### Contribution to YoY Growth %

Puntos porcentuales que aporta el elemento a la variación interanual del total seleccionado.

```dax
Contribution to YoY Growth % =
DIVIDE (
    [YoY Absolute Change],
    CALCULATE ( [Violations PY Comparable], ALLSELECTED ( DimInfraction ) )
)
```

---

## 04 Dynamic & UX

| Medida | Descripción | Formato |
|---|---|---|
| `Selected Year Label` | Texto con el año o rango de años que tiene datos en la selección. | `texto` |
| `Selected Month Label` | Mes seleccionado, o "Todos los meses". | `texto` |
| `Selected Infraction Label` | Infracción o categoría seleccionada, o "Todas las infracciones". | `texto` |
| `Partial Period Note` | Aviso cuando la selección incluye un año incompleto. Vacío si todos los años están completos. | `texto` |
| `Dynamic KPI Title` | Título dinámico para encabezados de página y visuales. | `texto` |
| `YoY Label` | Variación interanual con flecha, lista para una tarjeta. | `texto` |
| `KPI Color YoY` | Color para formato condicional. Aumento y descenso usan colores neutros: más infracciones registradas no implica más conductas de riesgo. | `texto` |
| `Dynamic Variance %` | Variación según el segmentador de comparación (interanual o mensual). | `0.0%;-0.0%;0.0%` |
| `Dynamic Variance Absolute` | Diferencia absoluta según el segmentador de comparación. | `+#,0;-#,0;0` |
| `Dynamic Comparison Label` | Nombre de la comparación activa. | `texto` |
| `Selected Metric` | Medida elegida en el segmentador de métricas. El formato cambia según la métrica. | `#,0` |
| `Selected Metric Label` | Nombre de la métrica activa. | `texto` |
| `Dynamic Tooltip` | Resumen en una frase para tooltips. | `texto` |


### Selected Year Label

Texto con el año o rango de años que tiene datos en la selección.

```dax
Selected Year Label =
VAR Years = CALCULATETABLE ( VALUES ( DimDate[Year] ), FactTrafficViolations )
VAR MinY = MINX ( Years, DimDate[Year] )
VAR MaxY = MAXX ( Years, DimDate[Year] )
RETURN
    SWITCH (
        TRUE (),
        ISBLANK ( MinY ), "Sin datos",
        MinY = MaxY, FORMAT ( MinY, "0" ),
        FORMAT ( MinY, "0" ) & "–" & FORMAT ( MaxY, "0" )
    )
```

### Selected Month Label

Mes seleccionado, o "Todos los meses".

```dax
Selected Month Label =
SELECTEDVALUE ( DimDate[MonthName], "Todos los meses" )
```

### Selected Infraction Label

Infracción o categoría seleccionada, o "Todas las infracciones".

```dax
Selected Infraction Label =
SWITCH (
    TRUE (),
    HASONEVALUE ( DimInfraction[InfractionType] ), SELECTEDVALUE ( DimInfraction[InfractionType] ),
    HASONEVALUE ( DimInfraction[InfractionCategory] ), SELECTEDVALUE ( DimInfraction[InfractionCategory] ),
    "Todas las infracciones"
)
```

### Partial Period Note

Aviso cuando la selección incluye un año incompleto. Vacío si todos los años están completos.

```dax
Partial Period Note =
VAR LastIdx = [Last Data Month Index]
VAR LastYear = INT ( DIVIDE ( LastIdx - 1, 12 ) )
VAR LastMonthName =
    CALCULATE (
        MAX ( DimDate[MonthName] ),
        REMOVEFILTERS (),
        DimDate[MonthIndex] = LastIdx
    )
VAR IncludesPartial =
    NOT ISEMPTY (
        CALCULATETABLE (
            FactTrafficViolations,
            KEEPFILTERS ( DimDate[IsCompleteViolationYear] = FALSE () )
        )
    )
RETURN
    IF (
        IncludesPartial,
        "* " & LastYear & ": datos de enero a " & LOWER ( LastMonthName ) & ". Las variaciones comparan el mismo tramo del año anterior.",
        ""
    )
```

### Dynamic KPI Title

Título dinámico para encabezados de página y visuales.

```dax
Dynamic KPI Title =
"Infracciones de tránsito · " & [Selected Year Label]
    & IF ( HASONEVALUE ( DimDate[MonthName] ), " · " & [Selected Month Label] )
    & IF ( ISFILTERED ( DimInfraction ), " · " & [Selected Infraction Label] )
```

### YoY Label

Variación interanual con flecha, lista para una tarjeta.

```dax
YoY Label =
VAR Growth = [YoY Growth %]
RETURN
    SWITCH (
        TRUE (),
        ISBLANK ( Growth ), "Sin período comparable",
        Growth > 0, "▲ " & FORMAT ( Growth, "+0.0%" ) & " vs. año anterior",
        Growth < 0, "▼ " & FORMAT ( Growth, "0.0%" ) & " vs. año anterior",
        "= 0.0% vs. año anterior"
    )
```

### KPI Color YoY

Color para formato condicional. Aumento y descenso usan colores neutros: más infracciones registradas no implica más conductas de riesgo.

```dax
KPI Color YoY =
VAR Growth = [YoY Growth %]
RETURN
    SWITCH (
        TRUE (),
        ISBLANK ( Growth ), "#8A8F98",
        Growth > 0, "#F28C28",
        Growth < 0, "#2A9D8F",
        "#8A8F98"
    )
```

### Dynamic Variance %

Variación según el segmentador de comparación (interanual o mensual).

```dax
Dynamic Variance % =
SWITCH (
    SELECTEDVALUE ( 'Comparison Selector'[ComparisonOrder], 1 ),
    2, [MoM Growth %],
    [YoY Growth %]
)
```

### Dynamic Variance Absolute

Diferencia absoluta según el segmentador de comparación.

```dax
Dynamic Variance Absolute =
SWITCH (
    SELECTEDVALUE ( 'Comparison Selector'[ComparisonOrder], 1 ),
    2, [MoM Absolute Change],
    [YoY Absolute Change]
)
```

### Dynamic Comparison Label

Nombre de la comparación activa.

```dax
Dynamic Comparison Label =
SELECTEDVALUE ( 'Comparison Selector'[Comparison], "Interanual (YoY)" )
```

### Selected Metric

Medida elegida en el segmentador de métricas. El formato cambia según la métrica.

```dax
Selected Metric =
SWITCH (
    SELECTEDVALUE ( 'Metric Selector'[MetricOrder], 1 ),
    1, [Total Traffic Violations],
    2, [Average Monthly Violations],
    3, [Total Violations YTD],
    4, [YoY Growth %],
    5, [Infraction Share %]
)
```

### Selected Metric Label

Nombre de la métrica activa.

```dax
Selected Metric Label =
SELECTEDVALUE ( 'Metric Selector'[Metric], "Infracciones" )
```

### Dynamic Tooltip

Resumen en una frase para tooltips.

```dax
Dynamic Tooltip =
VAR Cur = [Total Traffic Violations]
RETURN
    IF (
        NOT ISBLANK ( Cur ),
        [Selected Infraction Label] & " · " & [Selected Year Label] & ": "
            & FORMAT ( Cur, "#,0" ) & " infracciones registradas. " & [YoY Label] & "."
    )
```

---

## 05 Road Safety

| Medida | Descripción | Formato |
|---|---|---|
| `Total Road Fatalities` | Fallecimientos registrados (total nacional mensual). No se desglosa por tipo de infracción. | `#,0` |
| `Average Monthly Fatalities` | Promedio mensual de fallecimientos. | `#,0.0` |
| `Fatalities Previous Year` | Fallecimientos del mismo período del año anterior. | `#,0` |
| `Fatalities YoY %` | Variación interanual de fallecimientos. | `0.0%;-0.0%;0.0%` |
| `Violations (Common Period)` | Infracciones solo en los meses donde también hay datos de fallecimientos. | `#,0` |
| `Fatalities (Common Period)` | Fallecimientos solo en los meses donde también hay datos de infracciones. | `#,0` |
| `Infraction Filter Warning` | Aviso cuando hay un filtro de infracción activo: ese filtro no afecta a los fallecimientos. | `texto` |


### Total Road Fatalities

Fallecimientos registrados (total nacional mensual). No se desglosa por tipo de infracción.

```dax
Total Road Fatalities =
SUM ( FactRoadFatalities[Fatalities] )
```

### Average Monthly Fatalities

Promedio mensual de fallecimientos.

```dax
Average Monthly Fatalities =
AVERAGEX (
    SUMMARIZE ( FactRoadFatalities, DimDate[MonthIndex] ),
    [Total Road Fatalities]
)
```

### Fatalities Previous Year

Fallecimientos del mismo período del año anterior.

```dax
Fatalities Previous Year =
CALCULATE ( [Total Road Fatalities], SAMEPERIODLASTYEAR ( DimDate[Date] ) )
```

### Fatalities YoY %

Variación interanual de fallecimientos.

```dax
Fatalities YoY % =
VAR Cur = [Total Road Fatalities]
VAR Prev = [Fatalities Previous Year]
RETURN
    IF ( NOT ISBLANK ( Cur ) && NOT ISBLANK ( Prev ), DIVIDE ( Cur - Prev, Prev ) )
```

### Violations (Common Period)

Infracciones solo en los meses donde también hay datos de fallecimientos.

```dax
Violations (Common Period) =
CALCULATE (
    [Total Traffic Violations],
    KEEPFILTERS ( DimDate[IsCommonPeriod] = TRUE () )
)
```

### Fatalities (Common Period)

Fallecimientos solo en los meses donde también hay datos de infracciones.

```dax
Fatalities (Common Period) =
CALCULATE (
    [Total Road Fatalities],
    KEEPFILTERS ( DimDate[IsCommonPeriod] = TRUE () )
)
```

### Infraction Filter Warning

Aviso cuando hay un filtro de infracción activo: ese filtro no afecta a los fallecimientos.

```dax
Infraction Filter Warning =
IF (
    ISFILTERED ( DimInfraction ),
    "El filtro de infracción no aplica a los fallecimientos: la fuente no los desglosa por tipo de infracción."
)
```

---

## 04 Dynamic & UX

| Medida | Descripción | Formato |
|---|---|---|
| `Latest Year YoY %` | Variación interanual del último año con datos dentro de la selección (comparación sobre el mismo tramo de meses). | `0.0%;-0.0%;0.0%` |
| `Latest Year YoY Label` | Texto para tarjeta: variación del último año con datos frente al anterior. | `texto` |


### Latest Year YoY %

Variación interanual del último año con datos dentro de la selección (comparación sobre el mismo tramo de meses).

```dax
Latest Year YoY % =
VAR LatestYear =
    MAXX ( CALCULATETABLE ( VALUES ( DimDate[Year] ), FactTrafficViolations ), DimDate[Year] )
RETURN
    CALCULATE ( [YoY Growth %], DimDate[Year] = LatestYear )
```

### Latest Year YoY Label

Texto para tarjeta: variación del último año con datos frente al anterior.

```dax
Latest Year YoY Label =
VAR LatestYear =
    MAXX ( CALCULATETABLE ( VALUES ( DimDate[Year] ), FactTrafficViolations ), DimDate[Year] )
VAR Growth = [Latest Year YoY %]
RETURN
    IF (
        ISBLANK ( Growth ),
        "Sin período comparable",
        IF ( Growth >= 0, "▲ ", "▼ " ) & FORMAT ( Growth, "+0.0%;-0.0%" )
            & " · " & LatestYear & " vs. " & LatestYear - 1
    )
```

---

## 03 Infraction Analysis

| Medida | Descripción | Formato |
|---|---|---|
| `Cumulative Share Top N` | Participación acumulada limitada a los tipos del Top N (línea del Pareto). | `0.0%;-0.0%;0.0%` |


### Cumulative Share Top N

Participación acumulada limitada a los tipos del Top N (línea del Pareto).

```dax
Cumulative Share Top N =
IF ( [Infraction Ranking] <= [Top N Value], [Cumulative Infraction Share %] )
```

---

## 05 Road Safety

| Medida | Descripción | Formato |
|---|---|---|
| `Latest Year Fatalities YoY Label` | Texto para tarjeta: variación de fallecimientos del último año con datos frente al anterior. | `texto` |


### Latest Year Fatalities YoY Label

Texto para tarjeta: variación de fallecimientos del último año con datos frente al anterior.

```dax
Latest Year Fatalities YoY Label =
VAR LatestYear =
    MAXX ( CALCULATETABLE ( VALUES ( DimDate[Year] ), FactRoadFatalities ), DimDate[Year] )
VAR Growth = CALCULATE ( [Fatalities YoY %], DimDate[Year] = LatestYear )
RETURN
    IF (
        ISBLANK ( Growth ),
        "Sin período comparable",
        IF ( Growth >= 0, "▲ ", "▼ " ) & FORMAT ( Growth, "+0.0%;-0.0%" )
            & " · " & LatestYear & " vs. " & LatestYear - 1
    )
```

---
