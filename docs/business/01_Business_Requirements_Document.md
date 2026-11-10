# Business Requirements Document (BRD)

## Dominican Republic Traffic Violations & Road Safety Intelligence Platform

> **Plataforma de inteligencia de seguridad vial en Power BI, construida con los datos abiertos de infracciones de tránsito y fallecimientos publicados por la DIGESETT.**

---

## Información del documento

| Atributo | Detalle |
|---|---|
| **Proyecto** | Dominican Republic Traffic Violations & Road Safety Intelligence Platform |
| **Tipo de documento** | Business Requirements Document (BRD) |
| **Versión** | 1.0 |
| **Estado** | Aprobado para portafolio · reporte construido y validado en Power BI Desktop |
| **Fecha** | Noviembre 2026 |
| **Tipo de proyecto** | Business Intelligence · caso de estudio de portafolio |
| **Plataforma** | Microsoft Power BI Desktop (formato PBIP / PBIR / TMDL) |
| **Arquitectura de datos** | Power Query (ETL) → modelo dimensional en constelación → medidas DAX → reporte de 5 páginas |
| **Alcance geográfico** | República Dominicana (total nacional) |
| **Fuente** | DIGESETT, publicada en datos.gov.do |
| **Responsable** | Stanly Fernández |
| **Repositorio sugerido** | `digesett-road-safety-intelligence` |

> **Aviso:** proyecto independiente con fines académicos y de portafolio. No es un producto oficial de la DIGESETT ni está avalado por la institución.

---

## Tabla de contenido

1. [Resumen ejecutivo](#1-resumen-ejecutivo)
2. [Problema de negocio](#2-problema-de-negocio)
3. [Objetivo de negocio](#3-objetivo-de-negocio)
4. [Metas del proyecto](#4-metas-del-proyecto)
5. [Usuarios y partes interesadas](#5-usuarios-y-partes-interesadas)
6. [Dominios analíticos](#6-dominios-analíticos)
7. [Preguntas de negocio](#7-preguntas-de-negocio)
8. [KPI de alto nivel](#8-kpi-de-alto-nivel)
9. [Requisitos funcionales](#9-requisitos-funcionales)
10. [Requisitos no funcionales](#10-requisitos-no-funcionales)
11. [Requisitos de actualización de datos](#11-requisitos-de-actualización-de-datos)
12. [Entregables](#12-entregables)
13. [Alcance](#13-alcance)
14. [Supuestos](#14-supuestos)
15. [Restricciones y limitaciones](#15-restricciones-y-limitaciones)
16. [Criterios de éxito](#16-criterios-de-éxito)
17. [Fases del proyecto](#17-fases-del-proyecto)
18. [Trazabilidad de requisitos](#18-trazabilidad-de-requisitos)
19. [Próximos pasos](#19-próximos-pasos)

---

# 1. Resumen ejecutivo

La DIGESETT publica en el portal de datos abiertos del Estado dominicano las infracciones de tránsito registradas por mes y tipo (2018–2026) y los fallecimientos por accidentes de tránsito por mes (2016–2025). Los archivos llegan en formato ancho (un mes por columna), con un catálogo de infracciones que cambia entre años y sin indicadores calculados.

Este proyecto convierte esos archivos en una **plataforma analítica en Power BI** que permite responder, con cifras verificables, cuántas infracciones se registran, cómo evolucionan, cuáles concentran el volumen, qué patrones mensuales existen y cómo se comportan los fallecimientos en el mismo período.

El resultado es un reporte de **5 páginas**, un modelo dimensional con **2 tablas de hechos y 2 dimensiones**, **60 medidas DAX** y un proceso de validación que reconcilia cada total con la fuente original (13,289,441 infracciones y 18,785 fallecimientos).

---

# 2. Problema de negocio

| Problema | Consecuencia |
|---|---|
| Los datos se publican en Excel, en formato ancho y sin indicadores | Para conocer una variación interanual o una tendencia hay que calcularla a mano |
| El catálogo de infracciones de 2018 (41 tipos) no coincide con el de 2019–2026 (101 tipos) | Comparar un tipo de infracción entre años produce series rotas |
| Los meses no publicados aparecen como `0` | Un análisis directo trata "sin dato" como "cero infracciones" y distorsiona promedios y variaciones |
| 2026 está incompleto (enero–septiembre) | Compararlo contra años completos exagera la caída |
| Infracciones y fallecimientos están en archivos distintos, con granularidad y cobertura distintas | Es fácil cruzarlos de forma engañosa o sugerir causalidad |

---

# 3. Objetivo de negocio

Ofrecer una vista única, interactiva y metodológicamente correcta de las infracciones de tránsito y los fallecimientos registrados en República Dominicana, para apoyar el análisis de tendencias, la priorización de campañas de prevención y la identificación de los datos que faltan para evaluar el riesgo vial.

---

# 4. Metas del proyecto

| # | Meta | Estado |
|---|---|---|
| M1 | Consolidar y limpiar los dos archivos de DIGESETT en Power Query, sin edición manual de la fuente | Cumplida |
| M2 | Unificar el catálogo de infracciones 2018 y 2019–2026 con una tabla de mapeo auditable | Cumplida (36 de 41 tipos de 2018 mapeados; 5 sin equivalente) |
| M3 | Diseñar un modelo estrella que no mezcle granularidades | Cumplida |
| M4 | Construir indicadores de tiempo que no comparen períodos parciales contra completos | Cumplida |
| M5 | Publicar un reporte de 5 páginas con navegación, segmentadores y diseño institucional | Cumplida en Power BI Desktop |
| M6 | Documentar decisiones, supuestos y validaciones | Cumplida (este paquete de documentos) |
| M7 | Publicar el reporte en vivo | Pendiente (requiere cuenta Power BI; ver guía de despliegue) |

---

# 5. Usuarios y partes interesadas

| Usuario | Necesidad | Páginas principales |
|---|---|---|
| Directivos y analistas de seguridad vial | Visión general, tendencia, principales infracciones | Executive Overview, Historical Trends |
| Equipos de planificación de operativos | Meses y tipos con más registros | Monthly & Seasonal, Infraction Analysis |
| Comunicación y prevención | Infracciones a priorizar en campañas (casco, licencia, seguro, semáforo) | Infraction Analysis |
| Investigadores, periodistas y ciudadanía | Cifras verificables y contexto de fallecimientos | Road Safety Insights |
| Reclutadores y entrevistadores (portafolio) | Evidencia de modelado, DAX, Power Query y diseño | Todo el proyecto y la documentación |

---

# 6. Dominios analíticos

| Dominio | Fuente | Grano | Cobertura |
|---|---|---|---|
| Infracciones de tránsito registradas | DIGESETT · Infracciones de Tránsito 2018–2026 | tipo de infracción × mes | ene-2018 a sep-2026 (105 meses) |
| Fallecimientos por accidentes de tránsito | DIGESETT · Fallecimientos según Meses 2016–2025 | mes, total nacional | ene-2016 a dic-2025 (120 meses) |
| Período común | — | mes | ene-2018 a dic-2025 (96 meses) |

---

# 7. Preguntas de negocio

Las respuestas con cifras están en [02_Business_Questions_and_Insights.md](02_Business_Questions_and_Insights.md).

| ID | Pregunta | Página |
|---|---|---|
| BQ-01 | ¿Cuántas infracciones se registraron por año? | Executive Overview, Historical Trends |
| BQ-02 | ¿En qué años se registraron los mayores cambios? | Historical Trends |
| BQ-03 | ¿Cuáles son las infracciones más frecuentes? | Executive Overview, Infraction Analysis |
| BQ-04 | ¿Qué porcentaje del total representan las 5 y las 10 infracciones principales? | Infraction Analysis |
| BQ-05 | ¿Qué meses concentran más infracciones? | Monthly & Seasonal |
| BQ-06 | ¿Existen patrones estacionales? | Monthly & Seasonal |
| BQ-07 | ¿Qué categorías aumentaron o disminuyeron? | Infraction Analysis |
| BQ-08 | ¿Cómo evolucionaron los indicadores entre 2018 y 2026? | Historical Trends |
| BQ-09 | ¿Cómo evolucionaron los fallecimientos y en qué meses se concentran? | Road Safety Insights |
| BQ-10 | ¿Se mueven juntas las infracciones y los fallecimientos? | Road Safety Insights |
| BQ-11 | ¿Cómo se comporta 2026 frente al mismo tramo de 2025? | Executive Overview, Historical Trends |
| BQ-12 | ¿Qué datos adicionales harían falta para evaluar el riesgo vial? | Road Safety Insights |

---

# 8. KPI de alto nivel

| KPI | Medida DAX | Definición |
|---|---|---|
| Infracciones registradas | `Total Traffic Violations` | Suma de infracciones en el contexto de filtro |
| Variación interanual | `YoY Growth %` | Contra el mismo tramo de meses del año anterior; en blanco si los tramos no son comparables |
| Variación acumulada del año | `YTD Growth %` | Acumulado del año contra el mismo tramo del año anterior |
| Promedio mensual | `Average Monthly Violations` | Total entre meses **con datos** (no entre 12) |
| Promedio anual | `Average Annual Violations` | Solo años completos |
| Concentración Top 5 / Top 10 | `Top 5 Infractions Share %` / `Top 10 Infractions Share %` | Peso de los 5 o 10 tipos principales |
| Infracción principal | `Top Infraction Name` | Tipo con más registros en el contexto |
| Fallecimientos | `Total Road Fatalities` | Total nacional mensual |
| Variación de fallecimientos | `Fatalities YoY %` | Contra el mismo período del año anterior |

El catálogo completo está en [07_DAX_Measure_Catalog.md](../07_DAX_Measure_Catalog.md).

---

# 9. Requisitos funcionales

| ID | Requisito | Estado |
|---|---|---|
| RF-01 | Consolidar los archivos de DIGESETT con Power Query desde una ruta parametrizada | Cumplido |
| RF-02 | Transformar los meses de columnas a filas (unpivot) | Cumplido |
| RF-03 | Asignar un ID canónico a cada infracción con una tabla de mapeo, conservando el nombre original | Cumplido |
| RF-04 | Distinguir cero real de período sin dato | Cumplido |
| RF-05 | Detectar nombres nuevos sin mapear (consulta de control) | Cumplido |
| RF-06 | Tabla de fechas marcada, con indicadores de cobertura y de año incompleto | Cumplido |
| RF-07 | Variaciones interanuales sobre tramos comparables | Cumplido |
| RF-08 | Medias móviles de 3, 6 y 12 meses solo con ventanas completas | Cumplido |
| RF-09 | Ranking, Top N dinámico y Pareto que respeten los filtros | Cumplido |
| RF-10 | Títulos, etiquetas y avisos dinámicos (año parcial, filtros no aplicables a fallecimientos) | Cumplido |
| RF-11 | Selector de métrica y de tipo de comparación | Cumplido |
| RF-12 | Navegación entre páginas y segmentadores sincronizados | Construido; pendiente prueba de interacción |
| RF-13 | Drill-through por tipo de infracción, tooltips personalizados, bookmarks y botón de restablecer filtros | Pendiente (versión 1.1) |
| RF-14 | Publicación en vivo | Pendiente (licencia) |

---

# 10. Requisitos no funcionales

| ID | Requisito | Cómo se cumple |
|---|---|---|
| RNF-01 | Exactitud | Totales reconciliados con la fuente por año y en total (ver [09_Testing_and_Validation.md](../09_Testing_and_Validation.md)) |
| RNF-02 | Trazabilidad | Nombre original de cada infracción conservado; mapeos con nivel de confianza y nota |
| RNF-03 | Reproducibilidad | Todo el ETL en Power Query; un solo parámetro de ruta; proyecto en PBIP versionable con Git |
| RNF-04 | Rendimiento | Modelo de ~14 mil filas en modo Importación, claves enteras, sin columnas calculadas |
| RNF-05 | Honestidad analítica | Sin relaciones causales; categorías propias rotuladas como tales; avisos de período parcial |
| RNF-06 | Accesibilidad visual | Contraste alto sobre fondo oscuro; colores neutros para aumentos y descensos (más infracciones no se pintan como "malo") |
| RNF-07 | Mantenibilidad | Medidas documentadas en carpetas; la cobertura se calcula de los datos, sin fechas escritas a mano |

---

# 11. Requisitos de actualización de datos

| Aspecto | Definición |
|---|---|
| Frecuencia de la fuente | Variable; DIGESETT publica archivos acumulados |
| Procedimiento | Reemplazar los Excel en `data/raw/` con el mismo nombre y pulsar **Actualizar** |
| Ajustes automáticos | Último mes con datos, año incompleto, período común y etiquetas `2026*` se recalculan solos |
| Control | `qa_InfraccionesSinMapear` debe devolver 0 filas; si no, agregar el nombre nuevo a `MapInfraction.csv` |

---

# 12. Entregables

| Entregable | Ubicación |
|---|---|
| Proyecto Power BI (PBIP) | `DIGESETT_Road_Safety_Intelligence.pbip` |
| Código Power Query | `powerquery/*.pq` |
| Modelo y medidas (TMDL) | `model/*.tmdl` |
| Biblioteca DAX | `dax/DIGESETT_Measures.dax` |
| Tema de Power BI | `theme/DIGESETT_Road_Safety.json` |
| Tablas de referencia y totales de control | `data/reference/`, `data/validation/` |
| Script de perfilado | `scripts/01_profile_digesett.py` |
| Documentación | `docs/` |

---

# 13. Alcance

**Incluido:** infracciones registradas por tipo y mes; fallecimientos por mes; tendencias, variaciones, concentración, estacionalidad; categorías de elaboración propia; diseño institucional.

**Excluido:** accidentes y lesionados; desagregación por provincia, vehículo, sexo o edad; tasas por población o parque vehicular; severidad de las infracciones; montos de multas; pronósticos.

---

# 14. Supuestos

| ID | Supuesto | Impacto si es falso |
|---|---|---|
| S-01 | Los `0` de oct–dic 2026 son meses no publicados | Ninguno: al publicarse, el corte avanza solo |
| S-02 | En ene–may 2019, los 61 tipos en cero continuo aún no se registraban ("no aplica") | Los promedios mensuales de 2019 de esos tipos cambiarían; se revierte en un paso de M |
| S-03 | El mapeo 2018 → catálogo vigente es una equivalencia de concepto hecha por el analista | Las series por tipo de 2018 cambiarían; los totales no |
| S-04 | Las categorías (9 grupos) son una clasificación propia | Solo cambia la agrupación, no los totales |

---

# 15. Restricciones y limitaciones

- La fuente no define "fallecido" (en el lugar del hecho o en un plazo posterior).
- Infracciones registradas ≠ conductas de riesgo: el volumen depende también de la intensidad de la fiscalización.
- No hay denominadores de exposición; no se calculan tasas.
- La publicación en vivo requiere una cuenta de trabajo o escuela de Microsoft; Power BI no acepta correos personales (Gmail, Outlook.com).

---

# 16. Criterios de éxito

| Criterio | Resultado |
|---|---|
| Totales del modelo = totales de la fuente | 13,289,441 infracciones y 18,785 fallecimientos: **coinciden** |
| Medidas validadas contra cálculo independiente | 56 de 56 medidas originales **coinciden**; 4 medidas de presentación revisadas en pantalla |
| Ningún período parcial comparado con uno completo | `YoY Growth %` de 2026 compara ene–sep contra ene–sep |
| Reporte de 5 páginas funcional | Construido y revisado en Power BI Desktop |
| Documentación completa | Este paquete |

---

# 17. Fases del proyecto

| Fase | Contenido | Estado |
|---|---|---|
| 1 | Perfilado de datos | Completa |
| 2 | Preparación y limpieza (Power Query) | Completa y validada |
| 3 | Modelo dimensional | Completa y validada |
| 4 | Medidas DAX | Completa y validada |
| 5 | Diseño y tema | Completa |
| 6 | Visualizaciones y filtros | Completa; interactividad avanzada pendiente |
| 7 | Validación de indicadores, relaciones y rendimiento | Completa para datos y medidas; pendiente prueba de interacción |
| 8 | Documentación y portafolio | Completa; publicación en vivo pendiente |

---

# 18. Trazabilidad de requisitos

| Pregunta | KPI / medida | Visual | Validación |
|---|---|---|---|
| BQ-01 | `Total Traffic Violations` | Columnas por año | Totales por año = fuente |
| BQ-02 | `YoY Growth %`, `YoY Absolute Change` | Combo anual, cambio absoluto | Cálculo independiente en Python |
| BQ-03, BQ-04 | `Infraction Ranking`, `Top 5/10 Infractions Share %` | Ranking, Pareto | 58.2 % y 74.8 % coinciden |
| BQ-05, BQ-06 | `Average Monthly Violations`, `MoM Growth %` | Mapa de calor, promedio por mes, trimestres | Revisado contra datos |
| BQ-07 | `YoY Growth %` por categoría | Matriz categoría × año | Cálculo independiente |
| BQ-09, BQ-10 | `Total Road Fatalities`, `Fatalities YoY %` | Página Road Safety | 18,785 = fuente |
| BQ-11 | `Latest Year YoY %`, `YTD Growth %` | Tarjetas | −17.2 % coincide |

---

# 19. Próximos pasos

1. Publicar el reporte en vivo (ver [10_Deployment_and_Publishing_Guide.md](../10_Deployment_and_Publishing_Guide.md)).
2. Versión 1.1: drill-through, tooltips de página, bookmarks, botón de restablecer filtros y field parameters.
3. Sustituir el logo provisional por el archivo oficial en alta resolución.
4. Incorporar parque vehicular (DGII) y población (ONE) para calcular tasas por 10,000 vehículos o 100,000 habitantes.
