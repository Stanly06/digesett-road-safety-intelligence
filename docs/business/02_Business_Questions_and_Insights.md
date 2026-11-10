# Preguntas de negocio, KPI e insights

## Dominican Republic Traffic Violations & Road Safety Intelligence Platform

> **Respuestas en lenguaje ejecutivo a las preguntas de negocio del proyecto, calculadas sobre el modelo validado. Cada respuesta separa lo que los datos muestran (observación) de lo que podría explicarlo (hipótesis por verificar).**

---

## Información del documento

| Atributo | Detalle |
|---|---|
| **Tipo de documento** | Business Questions, KPI Catalog & Insights |
| **Versión** | 1.0 |
| **Fecha de corte de datos** | Infracciones hasta septiembre 2026 · Fallecimientos hasta diciembre 2025 |
| **Origen de las cifras** | Modelo de Power BI validado; recalculadas de forma independiente en Python |
| **Responsable** | Stanly Fernández |

---

## Cómo leer este documento

- **Observación:** lo que muestran los datos, sin interpretación.
- **Hipótesis:** una posible explicación que **no** se puede comprobar con estos archivos. Requiere otra fuente antes de afirmarse.
- **Infracciones registradas** no es lo mismo que conductas de riesgo: el número depende también de cuántos agentes, operativos y controles hubo.
- Las comparaciones por tipo de infracción usan **2021–2025** (años completos con el mismo catálogo). 2018 usa otro catálogo y 2019 tiene 61 tipos que empezaron a registrarse en junio.

---

## Resumen ejecutivo (5 hallazgos)

1. **El volumen casi se triplicó entre 2018 y 2025** (812,930 → 2,355,349). Con el mismo catálogo, de 2021 a 2025 creció **54.7 %**.
2. **El casco concentra más de una de cada cuatro infracciones** (27.2 % del total histórico) y su peso sube: 26.0 % en 2021, **31.3 % en 2025**.
3. **Cinco tipos explican el 58.2 % del total** y diez el **74.8 %**: casco, licencia, seguro, semáforo en rojo y cinturón.
4. **2026 va 17.2 % por debajo** del mismo tramo de 2025 (enero–septiembre), con la caída más fuerte en Documentación y registro (−41.4 %).
5. **Los fallecimientos subieron a 2,172 en 2025**, el máximo de la serie 2016–2025; diciembre es el mes con más fallecimientos en promedio.

---

## BQ-01 · ¿Cuántas infracciones se registraron por año?

| Año | Infracciones | Meses con datos | Promedio mensual |
|---|---:|---:|---:|
| 2018 | 812,930 | 12 | 67,744 |
| 2019 | 1,003,852 | 12 | 83,654 |
| 2020 | 614,808 | 12 | 51,234 |
| 2021 | 1,522,201 | 12 | 126,850 |
| 2022 | 2,026,132 | 12 | 168,844 |
| 2023 | 1,503,418 | 12 | 125,285 |
| 2024 | 1,948,238 | 12 | 162,353 |
| 2025 | **2,355,349** | 12 | **196,279** |
| 2026* | 1,502,513 | 9 | 166,946 |
| **Total** | **13,289,441** | 105 | 126,566 |

\* 2026: enero a septiembre.

**Observación:** 2025 es el año con más infracciones registradas. El promedio anual de los 8 años completos es **1,473,366**.

---

## BQ-02 · ¿En qué años se registraron los mayores cambios?

| Año | Cambio absoluto | Variación |
|---|---:|---:|
| 2019 vs 2018 | +190,922 | +23.5 % |
| 2020 vs 2019 | −389,044 | **−38.8 %** |
| 2021 vs 2020 | +907,393 | **+147.6 %** |
| 2022 vs 2021 | +503,931 | +33.1 % |
| 2023 vs 2022 | −522,714 | **−25.8 %** |
| 2024 vs 2023 | +444,820 | +29.6 % |
| 2025 vs 2024 | +407,111 | +20.9 % |
| 2026 vs 2025 (ene–sep) | −312,477 | −17.2 % |

**Observación:**
- La mayor caída fue en **2020**. Abril de 2020 registró **2,649** infracciones, el mínimo de toda la serie; de marzo a julio de 2020 se registraron 102,180, frente a 447,779 en los mismos meses de 2019.
- El mayor salto fue en **2021** (+147.6 %), en parte por la base baja de 2020.
- **2023** cayó 25.8 % y se recuperó en 2024.
- La comparación 2019 vs 2018 debe leerse con cautela: los catálogos de infracciones son distintos.

**Hipótesis por verificar:**
- 2020: coincide en el tiempo con las restricciones de movilidad por la pandemia de COVID-19.
- 2023: los archivos no explican la caída; podría reflejar cambios en operativos, personal o en el registro. Hace falta información institucional.

---

## BQ-03 · ¿Cuáles son las infracciones más frecuentes?

**Total histórico (2018 – sep. 2026):**

| # | Infracción | Registros | % del total |
|---:|---|---:|---:|
| 1 | No uso del casco protector | 3,615,508 | 27.2 % |
| 2 | Transitar sin licencia o vencida | 1,145,463 | 8.6 % |
| 3 | Transitar sin seguro o vencido | 1,127,712 | 8.5 % |
| 4 | Respeto a las señales del semáforo (luz roja) | 1,081,755 | 8.1 % |
| 5 | No uso del cinturón de seguridad | 770,078 | 5.8 % |
| 6 | Exceso de velocidad | 644,330 | 4.8 % |
| 7 | Transitar sin luces | 423,425 | 3.2 % |
| 8 | Falta o pérdida de medidas de seguridad | 385,266 | 2.9 % |
| 9 | Transitar en vía contraria | 381,626 | 2.9 % |
| 10 | Uso del celular o dispositivos electrónicos | 371,358 | 2.8 % |

**Observación:** el casco protector es, por amplio margen, la infracción más registrada: triplica a la segunda. Su peso anual pasó de 24.8 % (2019) a **31.3 %** (2025).

---

## BQ-04 · ¿Qué porcentaje del total representan las 5 y las 10 principales?

| Grupo | Participación |
|---|---:|
| Infracción principal (casco) | 27.2 % |
| Top 5 | **58.2 %** |
| Top 10 | **74.8 %** |
| Tipos con registros | 106 (101 vigentes + 5 de 2018 sin equivalente) |

**Observación:** el registro de infracciones está muy concentrado. Una campaña o un análisis centrado en 5 tipos cubre más de la mitad del volumen.

---

## BQ-05 · ¿Qué meses concentran más infracciones?

**Promedio por mes del año (2018 – sep. 2026)** y **peso del mes dentro de su año (promedio 2021–2025)**:

| Mes | Promedio | Peso en el año | Peso si todos los días pesaran igual |
|---|---:|---:|---:|
| Enero | 133,496 | 8.31 % | 8.49 % |
| Febrero | **110,387** | **6.93 %** | 7.67 % |
| Marzo | 123,986 | 8.09 % | 8.49 % |
| Abril | 119,481 | 8.15 % | 8.22 % |
| Mayo | 120,257 | 8.02 % | 8.49 % |
| Junio | 125,343 | 8.22 % | 8.22 % |
| Julio | 136,504 | 9.16 % | 8.49 % |
| Agosto | 130,230 | 8.68 % | 8.49 % |
| Septiembre | 127,085 | 8.38 % | 8.22 % |
| Octubre | 128,884 | 8.53 % | 8.49 % |
| Noviembre | 123,032 | 7.91 % | 8.22 % |
| Diciembre | **141,652** | **9.63 %** | 8.49 % |

**Observación:**
- **Diciembre** y **julio** son los meses con más infracciones en promedio y los únicos que pesan claramente más de lo que les corresponde por número de días.
- **Febrero** es el más bajo. Parte de la diferencia se explica porque tiene menos días, pero aun así queda por debajo de lo esperado (6.93 % frente a 7.67 %).

---

## BQ-06 · ¿Existen patrones estacionales?

**Peso de cada trimestre en el año (2018–2025, excluyendo 2020):**

| Trimestre | Peso promedio |
|---|---:|
| T1 (ene–mar) | 23.0 % |
| T2 (abr–jun) | 24.9 % |
| T3 (jul–sep) | 25.9 % |
| T4 (oct–dic) | 26.1 % |

**Mes con más infracciones en cada año:** octubre (2018), julio (2019, 2025), enero (2020, 2023, 2026), diciembre (2021, 2022, 2024).

**Observación:** hay una **estacionalidad leve**: el segundo semestre pesa algo más que el primero y diciembre destaca en varios años. Pero el mes pico cambia de un año a otro, así que no hay un patrón fijo y fuerte. 2020 se excluye porque la caída de abril–julio deforma cualquier promedio.

**Hipótesis por verificar:** el peso de diciembre y julio podría relacionarse con más tránsito en fiestas y vacaciones o con operativos especiales en esas fechas. Los archivos no permiten separar ambas cosas.

---

## BQ-07 · ¿Qué categorías aumentaron o disminuyeron?

> Las categorías son una **clasificación propia del analista** (9 grupos), no de DIGESETT.

| Categoría | 2021 | 2025 | Var. 2021→2025 | Var. 2024→2025 | Peso 2021 | Peso 2025 |
|---|---:|---:|---:|---:|---:|---:|
| Protección personal | 497,773 | 838,266 | +68.4 % | +23.5 % | 32.7 % | **35.6 %** |
| Documentación y registro | 291,698 | 618,927 | **+112.2 %** | +35.7 % | 19.2 % | **26.3 %** |
| Condiciones del vehículo y luces | 101,007 | 209,555 | +107.5 % | +14.7 % | 6.6 % | 8.9 % |
| Señales y semáforos | 190,716 | 179,194 | −6.0 % | +5.3 % | 12.5 % | 7.6 % |
| Circulación y maniobras | 137,889 | 178,174 | +29.2 % | +15.9 % | 9.1 % | 7.6 % |
| Estacionamiento y uso de la vía | 126,686 | 175,561 | +38.6 % | **+43.6 %** | 8.3 % | 7.5 % |
| Velocidad y conducción de riesgo | 155,485 | 129,425 | **−16.8 %** | **−16.8 %** | 10.2 % | 5.5 % |
| Peatones y animales | 1,343 | 13,393 | +897.2 % | +14.2 % | 0.1 % | 0.6 % |
| Carga y pasajeros | 19,604 | 12,854 | **−34.4 %** | **−26.4 %** | 1.3 % | 0.5 % |
| **Total** | 1,522,201 | 2,355,349 | **+54.7 %** | +20.9 % | | |

**Tipos con mayor aumento absoluto 2021→2025:** casco (+342,321), licencia (+186,120), seguro (+108,412), transitar sin luces (+60,011).

**Tipos con mayor descenso absoluto 2021→2025:** exceso de velocidad (−26,084; −28.2 %), señales o marcas no autorizadas (−22,627), uso de ciclovías (−9,202), uso del celular (−8,879; −17.2 %).

**2026 frente a ene–sep 2025:** Documentación y registro −41.4 %, Protección personal −17.9 %, Velocidad +5.2 %, Circulación y maniobras +29.8 %.

**Observación:** el crecimiento se concentra en **protección personal** (casco, cinturón) y **documentación** (licencia, seguro). Velocidad y conducción de riesgo bajó en registros, aunque eso no permite afirmar que haya menos exceso de velocidad en las vías.

**Hipótesis por verificar:** el aumento de documentación y casco es compatible con operativos de control de motocicletas y de documentos; la baja en velocidad podría depender del equipamiento de medición disponible. Ambas requieren datos de operativos.

---

## BQ-08 · ¿Cómo evolucionaron los indicadores entre 2018 y 2026?

| Indicador | Valor |
|---|---|
| Crecimiento 2018 → 2025 | +189.7 % (crecimiento anual compuesto 16.4 %) · *catálogos distintos* |
| Crecimiento 2021 → 2025 (mismo catálogo) | +54.7 % |
| Mes con más infracciones | Julio 2025: 233,955 |
| Mes con menos infracciones | Abril 2020: 2,649 |
| Peso del casco | 24.8 % (2019) → 31.3 % (2025) |
| Promedio móvil de 12 meses | Tendencia creciente desde 2021, con descenso en 2023 y en 2026 |

**Observación:** tras la caída de 2020, el registro de infracciones creció en cuatro de los cinco años siguientes. 2026 rompe esa tendencia en el tramo publicado.

---

## BQ-09 · ¿Cómo evolucionaron los fallecimientos y en qué meses se concentran?

| Año | Fallecimientos | Variación |
|---|---:|---:|
| 2016 | 1,993 | — |
| 2017 | 1,588 | −20.3 % |
| 2018 | 1,427 | −10.1 % |
| 2019 | 2,095 | **+46.8 %** |
| 2020 | 1,732 | −17.3 % |
| 2021 | 1,867 | +7.8 % |
| 2022 | 1,795 | −3.9 % |
| 2023 | 1,952 | +8.7 % |
| 2024 | 2,164 | +10.9 % |
| 2025 | **2,172** | +0.4 % |

**Promedio mensual por mes del año (2016–2025):** diciembre **175.8**, julio 166.3, octubre 163.9, marzo 163.7 · los más bajos: abril 143.8 y septiembre 144.2.

**Observación:**
- 2025 es el año con más fallecimientos de la serie; el mes más alto fue diciembre de 2025 (**215**).
- Desde 2023 los fallecimientos suben cada año: de 1,795 (2022) a 2,172 (2025), +21.0 %.
- Diciembre es el mes con más fallecimientos en promedio, igual que en infracciones.
- El salto de 2018 a 2019 (+46.8 %) es muy grande y debería verificarse con la fuente (posible cambio de metodología o de cobertura).

---

## BQ-10 · ¿Se mueven juntas las infracciones y los fallecimientos?

| Comparación (2018–2025) | Correlación de Pearson |
|---|---:|
| Anual (8 años) | r = 0.61 |
| Mensual (96 meses) | r = 0.49 |

**Observación:** existe una asociación positiva moderada: los años y meses con más infracciones registradas tienden a tener más fallecimientos.

**Lo que esto NO significa:**
- No indica que más infracciones *causen* más fallecimientos, ni que más fiscalización los aumente.
- Ambas series pueden crecer por factores comunes que no están en los datos: más vehículos, más población, más kilómetros recorridos.
- Con 8 años, la correlación anual es muy inestable.

Por eso el reporte muestra ambas series en un gráfico de dos escalas, sin línea de tendencia ni coeficiente, y con una nota de lectura.

---

## BQ-11 · ¿Cómo va 2026 frente al mismo tramo de 2025?

| Indicador | ene–sep 2025 | ene–sep 2026 | Variación |
|---|---:|---:|---:|
| Infracciones | 1,814,990 | 1,502,513 | **−17.2 %** |
| Promedio mensual | 201,666 | 166,946 | −17.2 % |

**Observación:** el reporte compara 2026 solo contra los mismos 9 meses de 2025. Compararlo con el año completo 2025 daría una caída engañosa de −36.2 %.

---

## BQ-12 · ¿Qué datos adicionales harían falta para evaluar el riesgo vial?

| Dato | Para qué serviría | Posible fuente |
|---|---|---|
| Parque vehicular por año y tipo | Tasas por 10,000 vehículos; separar crecimiento del parque de cambio de conducta | DGII |
| Población por año y provincia | Tasas por 100,000 habitantes | ONE |
| Accidentes y lesionados | Medir siniestralidad, no solo mortalidad | INTRANT / Observatorio de Seguridad Vial |
| Fallecidos por provincia, vehículo, edad y sexo | Focalizar campañas | INTRANT / OPSEVI |
| Operativos, agentes y horas de fiscalización | Distinguir "más infracciones" de "más controles" | DIGESETT |
| Ubicación y hora de las infracciones | Mapas de puntos críticos | DIGESETT |
| Multas pagadas y su monto | Efectividad del régimen sancionador | DIGESETT / INTRANT |
| Definición oficial de "fallecido" | Comparabilidad con otras fuentes y países | DIGESETT |

---

## Mapa de preguntas, KPI y visuales

| ID | KPI / medida | Página | Visual |
|---|---|---|---|
| BQ-01 | `Total Traffic Violations` | Executive Overview | Columnas por año, tarjeta |
| BQ-02 | `YoY Growth %`, `Dynamic Variance Absolute` | Historical Trends | Combo anual, cambio absoluto |
| BQ-03 | `Infraction Ranking`, `Violations Top N` | Infraction Analysis | Ranking Top N |
| BQ-04 | `Top 5 / Top 10 Infractions Share %`, `Cumulative Share Top N` | Infraction Analysis | Tarjetas, Pareto |
| BQ-05 | `Average Monthly Violations` | Monthly & Seasonal | Promedio por mes, mapa de calor |
| BQ-06 | `Total Traffic Violations` por trimestre, `MoM Growth %` | Monthly & Seasonal | 100 % apilado por trimestre, MoM |
| BQ-07 | `Selected Metric`, `YoY Growth %` | Infraction Analysis | Matriz categoría × año |
| BQ-08 | `Rolling 12M Average`, `Average Annual Violations` | Historical Trends | Medias móviles |
| BQ-09 | `Total Road Fatalities`, `Fatalities YoY %` | Road Safety Insights | Columnas, mapa de calor |
| BQ-10 | `Violations (Common Period)`, `Fatalities (Common Period)` | Road Safety Insights | Combo de dos escalas |
| BQ-11 | `Latest Year YoY Label`, `YTD Growth %` | Executive Overview, Historical Trends | Tarjetas |
| BQ-12 | — | Road Safety Insights | Nota de lectura |
