# Diccionario de datos

## Dominican Republic Traffic Violations & Road Safety Intelligence Platform

> Todas las tablas y columnas del modelo semántico, con tipo, origen y reglas. Las columnas marcadas como **oculta** no aparecen en la vista de informe.

---

## 1. Archivos de origen

### 1.1 `Infracciones-de-Transito-DIGESETT-2018-2026.xlsx` · hoja `INFRACCIONES 2018-2026`

| Columna | Tipo | Descripción |
|---|---|---|
| `INFRACCIONES` | texto | Nombre de la infracción con su artículo o resolución entre paréntesis |
| `ENERO` … `DICIEMBRE` | entero | Infracciones registradas en el mes (12 columnas) |
| `AÑO` | entero | Año, 2018–2026 |

849 filas · 1 fila = tipo de infracción × año · formato ancho.

### 1.2 `Fallecimientos-segun-Meses-DIGESETT-2016-2025.xlsx` · hoja `Fallecimientos Segun Meses`

| Columna | Tipo | Descripción |
|---|---|---|
| `MES` | texto | Mes en mayúsculas (el mes 11 viene como `NOVIEMBRES`) |
| `FALLECIDOS` | entero | Fallecimientos por accidentes de tránsito en el mes |
| `AÑO` | entero | Año, 2016–2025 |

120 filas · 1 fila = mes · total nacional.

### 1.3 Tablas de referencia (elaboración propia)

| Archivo | Filas | Contenido |
|---|---:|---|
| `data/reference/MapInfraction.csv` | 145 | Nombre original → `InfractionID`, con catálogo de origen, nivel de confianza y nota |
| `data/reference/DimInfraction.csv` | 106 | Catálogo canónico con referencia legal y categoría |

---

## 2. Tablas del modelo

| Tabla | Tipo | Filas | Grano |
|---|---|---:|---|
| `FactTrafficViolations` | Hechos | 9,580 | infracción × mes |
| `FactRoadFatalities` | Hechos | 120 | mes |
| `DimDate` | Dimensión (tabla de fechas marcada) | 4,018 | día (2016-01-01 a 2026-12-31) |
| `DimInfraction` | Dimensión | 106 | infracción canónica |
| `_Measures` | Contenedor de medidas | 0 | — |
| `Top N` | Parámetro desconectado | 5 | valor de N |
| `Metric Selector` | Parámetro desconectado | 5 | métrica |
| `Comparison Selector` | Parámetro desconectado | 2 | tipo de comparación |

---

## 3. `FactTrafficViolations`

| Columna | Tipo | Oculta | Descripción | Regla |
|---|---|---|---|---|
| `MonthStartDate` | fecha | Sí | Primer día del mes | Clave a `DimDate[Date]` |
| `InfractionID` | entero | Sí | Infracción canónica | Clave a `DimInfraction[InfractionID]`; nunca nula |
| `ViolationCount` | entero | Sí | Infracciones registradas | ≥ 0. **0 = cero real**; ausencia de fila = sin dato |

Filas eliminadas en el ETL (todas con valor 0): 303 de oct–dic 2026 (no publicado) y 305 de ene–may 2019 (tipos que aún no se registraban).

---

## 4. `FactRoadFatalities`

| Columna | Tipo | Oculta | Descripción | Regla |
|---|---|---|---|---|
| `MonthStartDate` | fecha | Sí | Primer día del mes | Clave a `DimDate[Date]` |
| `Fatalities` | entero | Sí | Fallecimientos por accidentes de tránsito | ≥ 0; sin desglose por tipo, provincia ni vehículo |

---

## 5. `DimDate`

| Columna | Tipo | Oculta | Descripción | Ejemplo |
|---|---|---|---|---|
| `Date` | fecha | Sí | Clave; fecha continua | 2025-07-01 |
| `Year` | entero | No | Año | 2025 |
| `YearLabel` | texto | No | Año con `*` si está incompleto. Ordenada por `Year` | `2026*` |
| `QuarterNumber` | entero | Sí | Trimestre 1–4 | 3 |
| `Quarter` | texto | No | Trimestre. Ordenada por `QuarterNumber` | `T3` |
| `YearQuarter` | texto | No | Año-trimestre | `2025-T3` |
| `MonthNumber` | entero | Sí | Mes 1–12 | 7 |
| `MonthName` | texto | No | Mes en español. Ordenada por `MonthNumber` | `Julio` |
| `MonthNameShort` | texto | No | Mes abreviado. Ordenada por `MonthNumber` | `Jul` |
| `YearMonth` | texto | No | Año-mes. Ordenada por `YearMonthSort` | `2025-07` |
| `YearMonthSort` | entero | Sí | Orden año-mes | 202507 |
| `MonthStartDate` | fecha | Sí | Primer día del mes | 2025-07-01 |
| `MonthIndex` | entero | Sí | Año × 12 + mes; meses consecutivos | 24307 |
| `HasViolationData` | lógico | No | El mes está dentro de la cobertura de infracciones | TRUE |
| `HasFatalityData` | lógico | No | El mes está dentro de la cobertura de fallecimientos | TRUE |
| `IsCompleteViolationYear` | lógico | No | El año tiene infracciones de enero a diciembre | TRUE |
| `IsCommonPeriod` | lógico | No | Hay datos de ambos hechos en el mes | TRUE |

Jerarquía **Calendario**: `Year` › `Quarter` › `MonthName`. No existen columnas de día ni de semana: la fuente es mensual.

---

## 6. `DimInfraction`

| Columna | Tipo | Oculta | Descripción |
|---|---|---|---|
| `InfractionID` | entero | Sí | Clave sustituta. 1–101 = catálogo vigente (orden del archivo 2025); 201–205 = solo 2018 |
| `InfractionType` | texto | No | Nombre limpio de la infracción |
| `LegalReference` | texto | No | Artículo o resolución (`Art. 251`, `Resol. 001-19 INTRANT`); nulo en 3 casos sin referencia en la fuente |
| `InfractionCategory` | texto | No | **Clasificación propia del analista** (9 grupos) |
| `CatalogStatus` | texto | No | `Catálogo vigente (2019–2026)` o `Solo 2018 (sin equivalente)` |

Jerarquía **Infracción**: `InfractionCategory` › `InfractionType`.

### Categorías

| Categoría | Tipos | Ejemplos |
|---|---:|---|
| Protección personal | 4 | Casco protector, cinturón de seguridad, niños en asiento trasero o en motocicleta |
| Documentación y registro | 18 | Licencia, seguro, placa, marbete |
| Circulación y maniobras | 18 | Vía contraria, giros, rebases |
| Condiciones del vehículo y luces | 16 | Transitar sin luces, luces LED, medidas de seguridad |
| Señales y semáforos | 11 | Luz roja, señales de tránsito |
| Estacionamiento y uso de la vía | 11 | Estacionamiento prohibido, obstruir el tránsito |
| Velocidad y conducción de riesgo | 11 | Exceso de velocidad, uso del celular, conducir en estado de embriaguez |
| Carga y pasajeros | 11 | Exceso de pasajeros, carga |
| Peatones y animales | 6 | Circulación de peatones, deberes hacia los peatones, animales en la vía |

---

## 7. `MapInfraction` (staging, no se carga)

| Columna | Descripción |
|---|---|
| `InfractionNameRaw` | Nombre exactamente como viene en el Excel (tras `Trim` y `Clean`) |
| `InfractionID` | ID canónico asignado |
| `SourceCatalog` | `Catálogo vigente` (101) · `Catálogo 2018` (41) · `Variante de escritura` (3) |
| `MappingConfidence` | `Exacta` (101) · `Alta` (33) · `Media` (6) · `Sin equivalente` (5) |
| `MappingNote` | Justificación del mapeo cuando no es directo |

---

## 8. Tablas de parámetros

| Tabla | Columnas | Valores | Uso |
|---|---|---|---|
| `Top N` | `N` | 3, 5, 10, 15, 20 | Segmentador del ranking y del Pareto (10 por defecto) |
| `Metric Selector` | `Metric`, `MetricOrder` (oculta) | Infracciones · Promedio mensual · Acumulado YTD · Variación interanual % · Participación % | Matriz de la página 3 |
| `Comparison Selector` | `Comparison`, `ComparisonOrder` (oculta) | Interanual (YoY) · Mensual (MoM) | Cambio absoluto de la página 2 |

---

## 9. Consultas de staging y control (no se cargan)

| Consulta | Salida | Propósito |
|---|---|---|
| `pRutaDatos` | texto | Ruta a la carpeta `data\` |
| `stg_Infracciones` | 10,188 filas | Excel de infracciones despivotado |
| `stg_Fallecimientos` | 120 filas | Excel de fallecimientos limpio |
| `MapInfraction` | 145 filas | Tabla puente de nombres |
| `qa_InfraccionesSinMapear` | **0 filas** esperadas | Detecta nombres nuevos sin mapear |
