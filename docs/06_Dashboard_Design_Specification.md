# Especificación de diseño del dashboard

## Dominican Republic Traffic Violations & Road Safety Intelligence Platform

---

## 1. Concepto visual

**"Vía y señalización, con identidad institucional."** El encabezado lleva los colores del escudo de la DIGESETT (verde y naranja) y un detalle de la bandera dominicana; el cuerpo usa un fondo gris asfalto con cifras en amarillo de señalización vial, para que los números destaquen y el reporte se lea como un tablero de control.

> El encabezado usa el logo de DIGESETT con fines de atribución de la fuente. El proyecto es independiente y no oficial, y así se indica en cada página.

---

## 2. Paleta

### Encabezado institucional

| Uso | Color | Origen |
|---|---|---|
| Franja (degradado) | `#0A7A33` → `#064A22` | Verde del escudo DIGESETT, muestreado del logo |
| Línea inferior | `#EB8810` | Naranja del borde del escudo |
| Filete | `#FFFFFF` | Separación entre franja y línea |
| Bandera | `#002D62` · `#CE1126` · blanco | Bandera nacional (versión civil, sin escudo) |
| Título y subtítulo | `#FFFFFF` · `#C9D6E8` | |

### Cuerpo del reporte (tema `DIGESETT_Road_Safety.json`)

| Token | Color | Uso |
|---|---|---|
| Fondo de página | `#1B1E22` | Gris asfalto |
| Tarjetas y visuales | `#272B31` | |
| Bordes y cuadrícula | `#3A4048` | |
| Texto principal | `#F4F5F6` | |
| Texto secundario | `#A7AEB6` | Ejes, leyendas, notas |
| Acento principal | `#FFC72C` | Cifras KPI, serie principal, botón activo (amarillo vial) |
| Serie secundaria | `#2A9D8F` | Medias móviles, variación % |
| Advertencia | `#F28C28` | Avisos de filtros |
| Fallecimientos | `#E5383B` | Exclusivo de la página 5 |

Paleta de series (`dataColors`): `#FFC72C`, `#2A9D8F`, `#F28C28`, `#E5383B`, `#8FA3B8`, `#E9D8A6`, `#6FCF97`, `#C9A227`, `#B56576`, `#6C757D`.

**Regla de color semántico:** los aumentos y descensos de infracciones **no** se pintan como bueno o malo. El rojo se reserva para fallecimientos.

---

## 3. Tipografía

| Elemento | Fuente | Tamaño |
|---|---|---|
| Título de página | Segoe UI Bold / Regular | 22 pt |
| Subtítulo | Segoe UI | 10 pt |
| Valor KPI | Segoe UI Semibold | 30 pt (20 pt en etiquetas de texto) |
| Título de visual | Segoe UI Semibold | 11 pt |
| Ejes y etiquetas | Segoe UI | 9–10 pt |
| Mapas de calor | Segoe UI | 12 pt |

---

## 4. Retícula (lienzo 1920 × 1080, 16:9)

| Zona | Y | Alto | Contenido |
|---|---:|---:|---|
| Encabezado | 0 | 84 | Logo, título, subtítulo, bandera, 5 botones de navegación |
| Segmentadores | 88 | 82 | 2 a 4 desplegables |
| KPI | 176 | 112–128 | 5 tarjetas de 360 px con 18 px de separación |
| Fila principal | 304–320 | 356–400 | 2 visuales |
| Fila secundaria | 680–720 | 312–352 | 2–3 visuales |
| Pie | 1036 | 36 | Nota de período parcial o fuente |

Márgenes laterales de 24 px; separación de 16 px entre visuales.

---

## 5. Páginas

| # | Página | Pregunta que responde | Visuales |
|---|---|---|---|
| 1 | **Executive Overview** | ¿Cuánto, cómo evoluciona y qué domina? | 5 KPI · línea mensual + media móvil 12M · dona por categoría · columnas por año · Top 10 |
| 2 | **Historical Trends** | ¿Qué años cambiaron más? | 5 KPI · combo anual + YoY % · comparación mensual entre años · cambio absoluto (YoY/MoM) · medias móviles 3M/12M · matriz año × mes |
| 3 | **Infraction Analysis** | ¿Qué infracciones concentran el volumen? | 5 KPI · ranking Top N · Pareto · matriz categoría › tipo × año con selector de métrica · tabla de detalle |
| 4 | **Monthly & Seasonal** | ¿Hay meses o trimestres que pesen más? | 5 KPI · mapa de calor año × mes · promedio por mes · variación MoM · trimestres al 100 % |
| 5 | **Road Safety Insights** | ¿Cómo evolucionan los fallecimientos? | 5 KPI · fallecimientos por año · infracciones vs fallecimientos (dos escalas) · nota de lectura · mapa de calor · promedio por mes |

---

## 6. Interactividad

| Elemento | Estado |
|---|---|
| Botones de navegación entre páginas (activo en amarillo) | Construido |
| Segmentadores desplegables sincronizados por grupo (Año, Mes, Categoría, Tipo) | Construido |
| Top N dinámico (3, 5, 10, 15, 20) | Construido |
| Selector de métrica (matriz de la página 3) | Construido |
| Selector de comparación YoY / MoM (página 2) | Construido |
| Títulos y notas dinámicos | Construido |
| Filtro de página: solo meses con datos de infracciones (páginas 1–4) | Construido |
| Drill-through por tipo de infracción | Pendiente (v1.1) |
| Tooltips de página personalizados | Pendiente (v1.1) |
| Bookmarks y botón de restablecer filtros | Pendiente (v1.1) |
| Field parameters | Pendiente (v1.1); hoy se usa una medida `SWITCH` |

---

## 7. Accesibilidad

- Contraste: texto claro sobre `#1B1E22` / `#272B31`; cifras amarillas sobre gris oscuro.
- Ninguna conclusión depende solo del color: los KPI de variación usan flecha y signo.
- Texto alternativo y orden de tabulación: pendiente de revisión en la versión 1.1.
