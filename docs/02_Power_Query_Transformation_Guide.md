# Fase 2 — Power Query Transformation Guide

**Proyecto:** Dominican Republic Traffic Violations & Road Safety Intelligence Platform
**Motor:** Power Query (M) en Power BI Desktop. Python se usó solo para calcular los totales de control contra los que se valida la carga.

> **Estado:** consultas cargadas y **validadas en Power BI Desktop el 2026-11-09**: todos los totales de la sección 7 coinciden (9,580 filas, 13,289,441 infracciones, 0 ID nulos, 120 filas y 18,785 fallecidos).

---

## 1. Decisiones tomadas (y cómo revertirlas)

| # | Decisión | Qué se hizo | Cómo revertir |
|---|----------|-------------|---------------|
| 1 | Mapear 2018 al catálogo vigente | 36 de 41 nombres de 2018 se asignan a un `InfractionID` vigente; 5 sin equivalente reciben ID propio (201–205) | Editar `MapInfraction.csv` |
| 2 | Ene–may 2019 como "no aplica" | Se eliminan 305 filas en cero de 61 tipos que empiezan a registrar en junio 2019 | En `FactTrafficViolations`, paso `SinNoAplica = SinFuturo` |
| 3 | Categorías propias | 9 grupos en `DimInfraction[InfractionCategory]`, rotulados como elaboración del analista | Editar `DimInfraction.csv` |
| 4 | Fallecimientos 2016–2017 | Se cargan completos (contexto histórico); el cruce con infracciones solo es válido 2018–2025 | Filtrar en `FactRoadFatalities` |

No se usa `Folder.Files` ni `Table.Combine`: la fuente es **un solo archivo por tema**, no archivos anuales. Si DIGESETT pasa a publicar un archivo por año, `stg_Infracciones` se convierte en función y se combina por carpeta.

---

## 2. Estructura de carpetas

```
DIGESETT/
├── data/
│   ├── raw/                 ← los 2 Excel de DIGESETT, sin modificar
│   │   ├── Infracciones-de-Transito-DIGESETT-2018-2026.xlsx
│   │   └── Fallecimientos-segun-Meses-DIGESETT-2016-2025.xlsx
│   ├── reference/           ← tablas de referencia mantenidas a mano
│   │   ├── MapInfraction.csv
│   │   └── DimInfraction.csv
│   └── validation/          ← totales de control (no se cargan al modelo)
├── powerquery/              ← código M (.pq)
├── scripts/                 ← perfilado en Python
└── docs/
```

Los nombres de los Excel en `raw/` deben ser exactamente los de arriba (sin prefijos).

---

## 3. Consultas

| Orden | Consulta | Tipo | ¿Carga al modelo? | Filas esperadas |
|------:|----------|------|-------------------|----------------:|
| 0 | `pRutaDatos` | Parámetro | — | — |
| 1 | `stg_Infracciones` | Staging | No | 10,188 |
| 2 | `MapInfraction` | Staging | No | 145 |
| 3 | `DimInfraction` | Dimensión | **Sí** | 106 |
| 4 | `FactTrafficViolations` | Hechos | **Sí** | 9,580 |
| 5a | `stg_Fallecimientos` | Staging | No | 120 |
| 5b | `FactRoadFatalities` | Hechos | **Sí** | 120 |
| 6 | `qa_InfraccionesSinMapear` | Control | No | **0** |
| 7 | `DimDate` | Dimensión | **Sí** | 4,018 |

`DimDate` se añadió en la Fase 3 (ver `03_Star_Schema_Documentation.md`).

### Flujo

```
Excel infracciones ─► stg_Infracciones ─┬─► FactTrafficViolations ◄─ MapInfraction ◄─ CSV
   (ancho, 849 f.)    (largo, 10,188)   └─► qa_InfraccionesSinMapear
CSV DimInfraction ──► DimInfraction
Excel fallecidos ───► FactRoadFatalities
```

---

## 4. Por qué cada transformación

### 4.1 `Table.UnpivotOtherColumns` — de ancho a largo
El Excel tiene los meses como 12 columnas. En un modelo tabular eso obligaría a escribir 12 medidas (o sumar 12 columnas) e impediría relacionar con una tabla de fechas. Con unpivot queda **una columna de período y una de valor**: una sola medida `SUM` sirve para cualquier corte, y la inteligencia de tiempo funciona.

Se elige `UnpivotOtherColumns` (declaras lo que *no* se despivota) frente a `Unpivot` (declaras las 12 columnas): es más corto y resistente si cambia el nombre de un mes.

### 4.2 `Text.Trim` + `Text.Clean`
Siete nombres traen espacios sobrantes. `" Transitar Sin Tablilla (Art.-42)"` (2022–2026) y `"Transitar Sin Tablilla (Art.-42)"` (2019–2021) son la misma infracción partida en dos series. Se limpia **antes** del join para que ambos lados coincidan.

### 4.3 Tabla de mapeo en vez de `Table.ReplaceValue` encadenados
Hay 45 nombres que requieren traducción (41 de 2018 + 4 variantes). Hacerlo con reemplazos en M dejaría la lógica de negocio enterrada en el código. En un CSV:
- se revisa en Excel sin abrir Power BI,
- cada cambio queda en el historial de Git,
- lleva columnas de auditoría (`MappingConfidence`, `MappingNote`).

`Table.ReplaceValue` sí se usa donde corresponde: una errata puntual (`NOVIEMBRES`).

### 4.4 `Table.NestedJoin` con `LeftOuter` (y `LeftAnti` para QA)
Con `Inner`, un nombre nuevo sin mapear desaparecería sin aviso y el total bajaría. Con `LeftOuter` la fila sobrevive, y `qa_InfraccionesSinMapear` (`LeftAnti` = "lo que está a la izquierda y no a la derecha") la lista explícitamente.

### 4.5 Regla A — período no reportado (303 filas)
Oct–dic 2026 viene en 0 para los 101 tipos. Se corta en el **último mes con algún registro > 0**, calculado con `List.Max`, no escrito a mano. Cuando actualices el Excel con octubre, el corte avanza solo.

### 4.6 Regla B — "no aplica" en 2019 (305 filas) · supuesto
61 tipos están en 0 de enero a mayo de 2019 y registran desde junio. Se usa `Table.Group` para sumar ene–may por tipo y `List.Buffer` para fijar la lista de IDs con suma 0. **Es una inferencia del patrón, no un dato confirmado por DIGESETT**; debe figurar como supuesto en la documentación final.

Efecto práctico: sin esta regla, el promedio mensual de 2019 de esos tipos se divide entre 12 meses en lugar de 7.

### 4.7 Ceros que sí se conservan (1,099 filas)
"0 infracciones de este tipo este mes" es un dato. La convención del modelo queda: **fila con 0 = cero real; ausencia de fila = sin dato**. Las medidas DAX de la Fase 4 se apoyan en ella.

### 4.8 Hechos solo con claves y medida
`FactTrafficViolations` conserva `MonthStartDate`, `InfractionID`, `ViolationCount`. El texto de la infracción vive una sola vez en `DimInfraction`; año y mes saldrán de `DimDate`. Menos columnas de alta cardinalidad en la tabla grande = mejor compresión y consultas más rápidas.

---

## 5. Mapeos que requieren tu revisión

Los mapeos "Exacta" (101) y "Alta" (33) son equivalencias de concepto directas. Estos son los que conviene que revises:

| Nombre original | Asignado a | Confianza | Nota |
|-----------------|------------|-----------|------|
| `Niños en el asiento delantero (art. 69)` | 10 — Niños menores de 12 años en asiento trasero, sin cinturón o sin asiento especial (Art. 69) | Media | 2018 describe "asiento delantero"; el catálogo vigente describe menores de 12 años en asiento trasero sin cinturón/asiento especial |
| `Transitar sin marbete de placa (art. 189)` | 43 — Transitar sin Marbete (Art. 189 No. 13) | Media | El catálogo vigente no separa marbete de placa y de revista |
| `Transitar sin marbete de revista (art. 189)` | 23 — Transitar sin Revista de Inspección Técnica (Art. 167) | Media | Asignado a Revista de Inspección Técnica por afinidad de concepto |
| `Exceso de velocidad (art. 268)` | 92 — Exceso de Velocidad (Art. 264) | Media | 2018 cita art. 268; el catálogo vigente separa Exceso de Velocidad (264) y Límites Máximos (268) |
| `Prohibición de niños menores de 8 años en motocicletas y de más de dos pasajeros (art. 69)` | 11 — Niños menores de 8 años en MOTOCICLETAS (Art. 78) | Media | 2018 incluye además "más de dos pasajeros" |
| `Vehículos con Exceso de Carga` | 14 — Exceso de Carga (Art. 122) | Media | Podría corresponder también a Vehículos Pesados por Exceso de Carga (Resol. 001-19) |
| `Violar señales de tránsito (art. 132)` | 201 — Violar señales de tránsito (Art. 132, catálogo 2018) | Sin equivalente |  |
| `Violar señales de tránsito (art. 138)` | 202 — Violar señales de tránsito (Art. 138, catálogo 2018) | Sin equivalente |  |
| `Vehiculos Retenidos por Transitar sin Documentos` | 203 — Vehiculos Retenidos por Transitar sin Documentos (s/ref) | Sin equivalente |  |
| `Obstruir el paso peatonal (art. 237)` | 204 — Obstruir el paso peatonal (Art. 237) | Sin equivalente |  |
| `Transitar sin Permiso` | 205 — Transitar sin Permiso (s/ref) | Sin equivalente |  |
| `Aditamentos en las Placas (Art. 189-8)` | 100 — Aditamentos en las Placas (s/ref) | Alta |  |
| `Conducción bajo los efectos de drogas o sustancias controladas (Art.- )` | 91 — Conducción bajo los efectos de drogas o sustancias controladas (Art. 257) | Alta |  |
| `Tomar o Dejar Pasajeros en Zona Prohibida y/o agarrarse de un vehículo en movimiento (Art.- 231` | 70 — Tomar o Dejar Pasajeros en Zona Prohibida y/o agarrarse de un vehículo en movimiento (Art. 231 No. 5) | Alta |  |

Volumen de 2018 por nivel de confianza: Alta 738,348 (90.8 %) · Media 32,877 (4.0 %) · Sin equivalente 41,705 (5.1 %).

**Limitación a declarar:** aun con el mapeo, 2018 tiene 41 tipos frente a 101. Las comparaciones 2018 vs. 2019+ por tipo son válidas solo para los tipos que existen en ambos catálogos; a nivel de total sí son comparables.

---

## 6. Implementación en Power BI Desktop

1. Crea la estructura de carpetas de la sección 2 y copia los archivos.
2. Power BI Desktop → **Inicio > Transformar datos**.
3. **Administrar parámetros > Nuevo parámetro**: nombre `pRutaDatos`, tipo Texto, valor = ruta de tu carpeta `data` **terminada en `\`** (ej. `C:\PowerBI\DIGESETT\data\`).
4. Para cada archivo `.pq`, en orden 01 → 06: **Nuevo origen > Consulta en blanco**, luego **Editor avanzado**, pega el contenido completo y renombra la consulta con el nombre exacto del archivo (sin el prefijo numérico).
5. Si aparece el aviso de **niveles de privacidad**, marca los orígenes como *Organizacional* (son todos archivos locales).
6. Clic derecho sobre `stg_Infracciones`, `MapInfraction` y `qa_InfraccionesSinMapear` → desmarca **Habilitar carga**.
7. **Cerrar y aplicar**.

## 7. Validación (cierra la Fase 2)

En el editor de Power Query, selecciona cada consulta y compara:

| Consulta | Comprobación | Valor esperado |
|----------|--------------|---------------:|
| `stg_Infracciones` | Filas | 10,188 |
| `qa_InfraccionesSinMapear` | Filas | 0 |
| `DimInfraction` | Filas / `InfractionID` únicos | 106 / 106 |
| `FactTrafficViolations` | Filas | 9,580 |
| `FactTrafficViolations` | Suma `ViolationCount` | 13,289,441 |
| `FactTrafficViolations` | `InfractionID` nulos | 0 |
| `FactTrafficViolations` | Fecha mín. / máx. | 2018-01-01 / 2026-09-01 |
| `FactRoadFatalities` | Filas / suma | 120 / 18,785 |

Por año (`data/validation/control_totals_violations.csv`):

| Año | Filas | Infracciones | Tipos |
|-----|------:|-------------:|------:|
| 2018 | 492 | 812,930 | 41 |
| 2019 | 907 | 1,003,852 | 101 |
| 2020 | 1,212 | 614,808 | 101 |
| 2021 | 1,212 | 1,522,201 | 101 |
| 2022 | 1,212 | 2,026,132 | 101 |
| 2023 | 1,212 | 1,503,418 | 101 |
| 2024 | 1,212 | 1,948,238 | 101 |
| 2025 | 1,212 | 2,355,349 | 101 |
| 2026 | 909 | 1,502,513 | 101 |

El total de infracciones **no cambia** con la limpieza (13,289,441 antes y después): las 608 filas eliminadas valían 0. Esa es la prueba de que no se perdió información.
