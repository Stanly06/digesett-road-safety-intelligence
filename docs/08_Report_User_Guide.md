# Guía de uso del reporte

## Dominican Republic Traffic Violations & Road Safety Intelligence Platform

---

## 1. Navegación

Los cinco botones del encabezado llevan a cada página; el de la página actual está en amarillo. En Power BI Desktop se activan con **Ctrl + clic**; en el servicio publicado, con clic.

| Botón | Página |
|---|---|
| Overview | Executive Overview |
| Tendencias | Historical Trends |
| Infracciones | Infraction Analysis |
| Estacionalidad | Monthly & Seasonal |
| Seguridad vial | Road Safety Insights |

## 2. Filtros

| Segmentador | Afecta a | No afecta a |
|---|---|---|
| Año, Mes | Infracciones y fallecimientos | — |
| Categoría, Tipo de infracción | Infracciones | **Fallecimientos** (la fuente no los desglosa por infracción) |
| Top N | Ranking y Pareto | Tarjetas |
| Métrica de la matriz | Matriz de la página 3 | Resto de la página |
| Comparación | Gráfico de cambio absoluto (página 2) | Resto de la página |

Los segmentadores con el mismo nombre están sincronizados entre páginas. Al hacer clic en un elemento de un gráfico (una barra, un sector de la dona), el resto de la página se filtra por él; un segundo clic lo quita.

## 3. Cómo leer los indicadores

| Indicador | Lectura correcta |
|---|---|
| **Variación interanual (último año)** | Compara el último año con datos de la selección contra el anterior, **en los mismos meses**. Para 2026: ene–sep 2026 vs ene–sep 2025 |
| **Promedio mensual** | Total entre los meses que tienen datos, no entre 12 |
| **Promedio anual** | Solo años completos |
| **`2026*`** | Año incompleto (enero–septiembre) |
| **Categoría** | Clasificación propia del analista, no de DIGESETT |
| **Infracciones registradas** | Reflejan conducta **y** fiscalización; un aumento no prueba más imprudencia |
| **Infracciones vs fallecimientos** | Solo período común 2018–2025; dos escalas distintas; sin relación causal |

## 4. Preguntas frecuentes

**¿Por qué 2026 no aparece en los fallecimientos?** La fuente de fallecimientos termina en diciembre de 2025.

**¿Por qué 2016 y 2017 no tienen infracciones?** La fuente de infracciones empieza en enero de 2018.

**¿Por qué algunas variaciones aparecen en blanco?** Porque el período anterior no es comparable (meses distintos con datos) o no existe.

**¿Por qué hay 106 tipos si el catálogo tiene 101?** Cinco infracciones de 2018 no tienen equivalente en el catálogo vigente y se conservan como tipos propios.
