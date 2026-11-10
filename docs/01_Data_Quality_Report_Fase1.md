# Fase 1 — Data Profiling & Data Quality Report

**Proyecto:** Dominican Republic Traffic Violations & Road Safety Intelligence Platform
**Fuente:** DIGESETT (archivos entregados por el autor del proyecto)
**Fecha del perfilado:** 2026-11-09
**Herramienta:** Python (pandas / openpyxl) — script reproducible en `scripts/01_profile_digesett.py`

> Todas las cifras de este documento salen de ejecutar el script sobre los dos archivos. No hay valores estimados.

---

## 1. Inventario de archivos

| # | Archivo | Hoja | Filas de datos | Columnas | Período |
|---|---------|------|---------------:|---------:|---------|
| 1 | `Infracciones-de-Transito-DIGESETT-2018-2026.xlsx` | `INFRACCIONES 2018-2026` | 849 | 14 | 2018 – sep. 2026 |
| 2 | `Fallecimientos-segun-Meses-DIGESETT-2016-2025.xlsx` | `Fallecimientos Segun Meses` | 120 | 3 | 2016 – dic. 2025 |

Ambos archivos tienen una sola hoja, encabezado en la fila 1, sin celdas combinadas, sin filas de título ni de totales.

---

## 2. Archivo 1 — Infracciones

### 2.1 Estructura

| Columna | Tipo | Contenido |
|---------|------|-----------|
| `INFRACCIONES` | texto | Nombre de la infracción, con el artículo o resolución entre paréntesis |
| `ENERO` … `DICIEMBRE` (12 columnas) | entero | Cantidad de infracciones registradas ese mes |
| `AÑO` | entero | Año (2018 – 2026) |

**Formato:** ancho (*wide*). Los meses son columnas, no filas.

**Granularidad real:** **una fila = un tipo de infracción en un año**; cada celda mensual = **tipo de infracción × mes × año**.

Consecuencia para el proyecto: *sí existe* el detalle mensual por tipo de infracción. La "regla crítica" del brief (no fabricar distribución mensual por tipo) no se activa: basta **una sola tabla de hechos** a grano infracción-mes. `FactMonthlyViolations` separada **no es necesaria**; el total mensual se obtiene sumando.

Al despivotar (`Table.UnpivotOtherColumns`) resultan 849 × 12 = **10,188 filas** antes de limpiar.

### 2.2 Cobertura temporal

| Año | Tipos (filas) | Total registrado | Observación |
|-----|--------------:|-----------------:|-------------|
| 2018 | 41 | 812,930 | Catálogo antiguo (41 tipos) |
| 2019 | 101 | 1,003,852 | Catálogo nuevo; 61 tipos en cero de enero a mayo |
| 2020 | 101 | 614,808 | Abril = 2,649 (mínimo de toda la serie) |
| 2021 | 101 | 1,522,201 | |
| 2022 | 101 | 2,026,132 | |
| 2023 | 101 | 1,503,418 | |
| 2024 | 101 | 1,948,238 | |
| 2025 | 101 | 2,355,349 | Máximo anual de la serie |
| 2026 | 101 | 1,502,513 | **Año parcial: ene–sep.** Oct–dic en cero |
| **Total** | **849** | **13,289,441** | |

Totales mensuales por año (suma de todos los tipos):

| Año | Ene | Feb | Mar | Abr | May | Jun | Jul | Ago | Sep | Oct | Nov | Dic |
|-----|----:|----:|----:|----:|----:|----:|----:|----:|----:|----:|----:|----:|
| 2018 | 56,562 | 54,327 | 69,858 | 67,439 | 73,617 | 66,532 | 65,448 | 59,782 | 59,698 | 83,006 | 81,276 | 75,385 |
| 2019 | 78,816 | 68,205 | 79,279 | 93,240 | 87,626 | 90,793 | 96,841 | 93,549 | 86,653 | 62,720 | 79,702 | 86,428 |
| 2020 | 98,884 | 63,203 | 31,332 | 2,649 | 14,921 | 28,325 | 24,953 | 36,071 | 58,331 | 83,637 | 85,785 | 86,717 |
| 2021 | 65,434 | 84,435 | 121,105 | 126,498 | 139,865 | 130,242 | 141,179 | 135,776 | 133,514 | 127,044 | 139,936 | 177,173 |
| 2022 | 176,438 | 161,366 | 169,930 | 156,411 | 156,970 | 164,720 | 175,559 | 176,400 | 156,585 | 178,335 | 162,564 | 190,854 |
| 2023 | 175,042 | 124,203 | 110,157 | 136,176 | 151,200 | 104,185 | 124,859 | 109,774 | 114,968 | 115,370 | 96,601 | 140,883 |
| 2024 | 157,360 | 106,204 | 165,397 | 146,353 | 94,460 | 178,909 | 187,703 | 178,977 | 178,115 | 185,856 | 170,992 | 197,912 |
| 2025 | 207,459 | 175,259 | 195,290 | 191,706 | 194,653 | 195,241 | 233,955 | 218,702 | 202,725 | 195,101 | 167,398 | 177,860 |
| 2026 | 185,471 | 156,277 | 173,523 | 154,858 | 168,998 | 169,137 | 178,037 | 163,036 | 153,176 | 0* | 0* | 0* |

\* No es "cero infracciones": es período no reportado.

### 2.3 Completitud y validez

| Prueba | Resultado |
|--------|-----------|
| Celdas nulas | 0 |
| Valores no numéricos en meses | 0 |
| Valores negativos | 0 |
| Valores decimales | 0 |
| Filas duplicadas exactas | 0 |
| Duplicados por (infracción, año) | 0 |
| Filas de "Total" incrustadas | 0 |
| Celdas mensuales en cero | 1,707 de 10,188 (16.8 %) |
| Filas con el año completo en cero | 4 |

Filas con todo el año en cero: *Vehículos de transporte funerario (Art.-96)* 2020; *Responsabilidad del Propietario de Animales (Art.- 226)* 2024; *Cruce sobre Mangueras de Bomberos (Art.-155)* 2026; *Tuercas Puntiagudas (Resol. 015-18 INTRANT)* 2026.

Distribución del valor mensual por celda: mediana 32, P75 551, máximo 70,960 (*No Uso del Casco Protector*, julio 2025). Distribución muy asimétrica: pocas infracciones concentran casi todo el volumen.

### 2.4 Hallazgos de calidad (ordenados por impacto)

#### H1 — Ruptura de catálogo entre 2018 y 2019 · **CRÍTICO**

- 2018 usa **41** nombres; 2019–2026 usa **101**.
- **Ningún** nombre de 2018 coincide textualmente con uno de 2019+ (intersección = 0).
- Cambian redacción *y*, en varios casos, el artículo citado:
  - `Transitar sin casco protector (art. 157)` → `No Uso del Casco Protector (Art.- 251)`
  - `Transitar en vía contraria (art. 252)` → `Transitar en Vía Contraria (Art.- 251)`
  - `Exceso de velocidad (art. 268)` → `Exceso de Velocidad (Art.- 264)` (y existe aparte `Límites Máximos de Velocidad (Art.- 268)`)
  - `Violar luz roja (art. 133)` → `Respeto a las señales del Semáforo (LUZ ROJA) (Art.-133)`
- Algunas de 2018 no tienen equivalente 1-a-1 evidente: `Violar señales de tránsito (art. 132)` y `(art. 138)`, `Obstruir el paso peatonal (art. 237)`, `Vehiculos Retenidos por Transitar sin Documentos`, `Transitar sin Permiso`, `Transitar sin marbete de placa` / `de revista`.

**Impacto:** sin una tabla puente, cualquier ranking, Pareto o YoY por tipo mostrará 2018 como categorías que "desaparecen" y 2019 como categorías que "nacen". El conteo de tipos distintos da 146 en bruto, cuando el catálogo vigente es de 101.

**Tratamiento propuesto (Fase 2):** tabla de mapeo `MapInfraction` (nombre original → `InfractionID` canónico), construida a mano y documentada. Las de 2018 sin equivalente claro se marcan `MappingConfidence = "Sin equivalente"` y **no se fuerzan**. Se conserva siempre el nombre original (`InfractionNameRaw`) para trazabilidad.

#### H2 — Ceros estructurales tratados como ceros reales · **CRÍTICO**

Hay tres situaciones distintas que el archivo representa con el mismo `0`:

| Caso | Dónde | Celdas | Significado real |
|------|-------|-------:|------------------|
| a) Período futuro / no reportado | 2026, oct–dic | 303 (101 × 3) | **Sin dato** |
| b) Categoría aún no registrada | 2019, ene–may: 61 de 101 tipos en cero los cinco meses y con valores desde junio | 305 | **No aplica** (el tipo empieza a registrarse en junio 2019) |
| c) Cero genuino | resto | 1,099 | Mes sin infracciones de ese tipo |

**Impacto:** si (a) y (b) entran como cero, se distorsionan promedio mensual, mínimo mensual, MoM, heatmap y cualquier YoY de 2026.

**Tratamiento propuesto:** en Power Query, eliminar las filas de (a) y (b) tras el unpivot (ausencia de fila = sin dato) y conservar (c) como 0. Para (b), el criterio se documenta como *supuesto*: "tipo con cero continuo ene–may 2019 y registros a partir de junio" — es una inferencia a partir del patrón, no una confirmación de DIGESETT.

#### H3 — Año 2026 parcial · **ALTO**

Datos hasta septiembre. Las medidas DAX deberán comparar 2026 contra **el mismo tramo ene–sep** del año anterior (YTD alineado) y marcar visualmente el año como incompleto. Referencia: ene–sep 2025 = 1,814,990 vs. ene–sep 2026 = 1,502,513.

#### H4 — Inconsistencias de nombre dentro del catálogo 2019–2026 · **MEDIO**

Tres infracciones cambian de escritura entre años, lo que parte su serie en dos:

| Infracción | Variantes | Años |
|------------|-----------|------|
| Tablilla | `Transitar Sin Tablilla (Art.-42)` / `" Transitar Sin Tablilla (Art.-42)"` (espacio inicial) | 2019–2021 / 2022–2026 |
| Drogas | `…sustancias controladas (Art.- 257)` / `…(Art.- )` (artículo vacío) | 2019, 2022–2026 / 2020–2021 |
| Tomar o dejar pasajeros | `…(Art.- 231 No. 5)` / `…(Art.- 231 ` (truncado) | 2019, 2022–2026 / 2020–2021 |
| Aditamentos en placas | `Aditamentos en las Placas (Art. 189-8)` / `Aditamentos en las Placas` | 2019 / 2020–2026 |

Además: 7 valores con espacios al inicio o final; un paréntesis sin abrir en `Uso del Celular … Art.- 221)`; errata `Conservación delas Vías`; formato del artículo no uniforme (`Art.-67`, `Art.- 67`, `art. 67`, `Art. 225`).

**Tratamiento:** `Text.Trim` + `Text.Clean` y resolución vía la misma tabla de mapeo de H1.

#### H5 — El artículo no sirve como clave · **MEDIO**

Varios tipos distintos citan el mismo artículo (p. ej. Art. 251: casco, vía contraria, túneles y pasos a desnivel; Art. 170: luces y medidas de seguridad; Art. 239: freno de emergencia e inicio de la marcha). Algunas citan resoluciones INTRANT en vez de artículos, y 8 nombres no traen referencia legal. **La clave debe ser un `InfractionID` sustituto**, no el artículo.

#### H6 — No existe categoría ni severidad en la fuente · **MEDIO**

El archivo solo trae el nombre. `InfractionCategory` (p. ej. Documentación, Protección personal, Velocidad, Señalización) tendría que ser una **clasificación propia del analista**, rotulada como tal en el dashboard y en el diccionario de datos. `Severity` no se creará salvo que se localice una clasificación oficial.

#### H7 — Variaciones abruptas a verificar · **INFORMATIVO**

Observaciones (no conclusiones):
- Abril 2020: 2,649 infracciones, frente a 98,884 en enero 2020.
- 2023: −25.8 % frente a 2022 (1,503,418 vs. 2,026,132), con recuperación en 2024.
- Mayo 2024: 94,460, entre 146,353 (abril) y 178,909 (junio).
- Octubre 2019: 62,720, entre 86,653 y 79,702.

Hipótesis a contrastar con fuentes externas antes de escribirlas como insight: restricciones de movilidad 2020; cambios en intensidad de fiscalización u operativos; posibles vacíos de reporte. El archivo no permite distinguir entre ellas.

---

## 3. Archivo 2 — Fallecimientos

### 3.1 Estructura

| Columna | Tipo | Contenido |
|---------|------|-----------|
| `MES` | texto | Nombre del mes en mayúsculas |
| `FALLECIDOS` | entero | Fallecimientos registrados en el mes |
| `AÑO` | entero | 2016 – 2025 |

**Formato:** largo (ya normalizado). **Granularidad:** mes × año, total nacional. Sin provincia, tipo de vehículo, sexo ni edad.

### 3.2 Cobertura y validez

| Año | Meses | Total | Mín. mensual | Máx. mensual |
|-----|------:|------:|-------------:|-------------:|
| 2016 | 12 | 1,993 | 134 | 205 |
| 2017 | 12 | 1,588 | 113 | 156 |
| 2018 | 12 | 1,427 | 78 | 187 |
| 2019 | 12 | 2,095 | 145 | 197 |
| 2020 | 12 | 1,732 | 83 | 188 |
| 2021 | 12 | 1,867 | 127 | 176 |
| 2022 | 12 | 1,795 | 113 | 184 |
| 2023 | 12 | 1,952 | 139 | 185 |
| 2024 | 12 | 2,164 | 155 | 212 |
| 2025 | 12 | 2,172 | 149 | 215 |

120 filas = 10 años × 12 meses, sin huecos, sin nulos, sin duplicados (mes, año), sin negativos.

### 3.3 Hallazgos

| ID | Hallazgo | Severidad | Tratamiento |
|----|----------|-----------|-------------|
| F1 | El mes 11 está escrito `NOVIEMBRES` en las 10 ocurrencias | Bajo | `Table.ReplaceValue` → `NOVIEMBRE` |
| F2 | Cobertura distinta a infracciones: empieza en 2016 y termina en 2025 | Alto | Período común analizable: **2018–2025**. 2016–2017 solo como contexto; 2026 sin dato de fallecidos |
| F3 | Valores idénticos en meses consecutivos: 2021 sep = 167, **oct = nov = dic = 162**; 2019 oct = nov = 194; 2023 oct = nov = 176; 2020 jun = jul = 123 | Medio | No se corrige. Tres meses iguales seguidos en 2021 es poco probable por azar: se marca como *dato a verificar con la fuente* |
| F4 | El archivo no define "fallecido" (en el lugar del hecho vs. hasta 30 días después) ni el alcance institucional | Alto | Documentar como limitación; buscar la nota metodológica en datos.gov.do antes de comparar con otras fuentes |
| F5 | No hay denominador de exposición (parque vehicular, población, km recorridos) | Alto | **No se calcularán tasas** en esta versión |

---

## 4. Compatibilidad entre los dos archivos

| Aspecto | Infracciones | Fallecimientos | ¿Compatibles? |
|---------|--------------|----------------|---------------|
| Grano temporal | mes | mes | Sí |
| Grano de categoría | tipo de infracción | — | No (fallecidos no tiene tipo) |
| Período | 2018 – sep. 2026 | 2016 – 2025 | Solape 2018–2025 (96 meses) |
| Geografía | nacional | nacional | Sí |

**Conclusión de modelado:** dos tablas de hechos independientes que se relacionan **solo a través de `DimDate`** (dimensión conformada, grano mensual). Nunca relación directa hecho-a-hecho. Un filtro por tipo de infracción **no debe** filtrar fallecimientos, y el reporte deberá dejarlo explícito.

**Advertencia analítica:** que ambas series puedan graficarse juntas por mes no implica relación causal. Las infracciones registradas miden actividad de fiscalización tanto como conducta de los conductores.

---

## 5. Qué análisis permite cada dataset

| Análisis solicitado | ¿Viable? | Nota |
|---------------------|----------|------|
| Total, YoY, MoM, YTD, medias móviles | Sí | Con manejo de 2026 parcial y ceros estructurales |
| Heatmap año × mes, estacionalidad | Sí | 2018–2025 completos; 2026 ene–sep |
| Ranking, Top N, Pareto por tipo | Sí | Comparables sin mapeo desde 2019; 2018 requiere `MapInfraction` |
| Evolución mensual *por tipo* | Sí | El grano lo permite |
| Donut por categoría | Condicionado | Requiere clasificación propia (H6) |
| Severidad | No | Sin fuente oficial |
| Fallecimientos por mes y año | Sí | 2016–2025 |
| Fallecimientos por provincia, lesionados, accidentes | No | No están en los archivos |
| Tasas de mortalidad / accidentalidad | No | Sin denominador |
| Infracciones vs. fallecimientos | Solo descriptivo | 2018–2025, sin inferencia causal |

---

## 6. Decisiones que quedan abiertas para la Fase 2

1. **Mapeo 2018 → catálogo 2019+:** ¿se mapean las 41 infracciones de 2018 (con nivel de confianza) o 2018 se usa solo para totales y los análisis por tipo arrancan en 2019?
2. **Enero–mayo 2019:** ¿se acepta el supuesto de "no aplica" para los 61 tipos en cero?
3. **Categorías:** ¿se crea una clasificación propia de ~8 grupos, rotulada como elaboración del analista?
4. **Fallecimientos 2016–2017:** ¿se cargan como contexto histórico o se recorta a 2018+?

---

## 7. Resumen de puntuación de calidad

| Dimensión | Infracciones | Fallecimientos |
|-----------|--------------|----------------|
| Completitud (nulos) | Alta — 0 nulos, pero ceros que encubren "sin dato" | Alta |
| Validez (tipos, rangos) | Alta | Alta |
| Unicidad | Alta | Alta |
| Consistencia de categorías | **Baja** — ruptura 2018/2019 y 4 nombres inestables | Media — errata en un mes |
| Cobertura temporal | Media — 2026 parcial | Media — no llega a 2026 |
| Documentación / metadatos | Baja — sin definiciones | Baja — sin definición de "fallecido" |
