# Guía de despliegue y publicación

## Dominican Republic Traffic Violations & Road Safety Intelligence Platform

---

## 1. Abrir el proyecto en otra computadora

1. Instalar Power BI Desktop (gratuito).
2. Clonar o descargar el repositorio.
3. Abrir `DIGESETT_Road_Safety_Intelligence.pbip`.
4. **Transformar datos → Administrar parámetros → `pRutaDatos`**: escribir la ruta de la carpeta `data\` de esa computadora, terminada en `\`.
5. Si pide niveles de privacidad, elegir **Organizacional** para el origen local.
6. **Actualizar**. Validar con la sección 3 de [09_Testing_and_Validation.md](09_Testing_and_Validation.md).

## 2. Actualizar con datos nuevos de DIGESETT

1. Descargar los archivos nuevos de datos.gov.do.
2. Reemplazar los Excel de `data/raw/` **con el mismo nombre**.
3. **Actualizar**.
4. Revisar `qa_InfraccionesSinMapear` (debe dar 0 filas). Si aparece un nombre nuevo, agregarlo a `data/reference/MapInfraction.csv` (y a `DimInfraction.csv` si es una infracción nueva) y volver a actualizar.
5. Revisar que la nota del año parcial y la etiqueta `2026*` cambien solas.

## 3. Repositorio en GitHub

| Incluir | Excluir (ya en `.gitignore` del PBIP) |
|---|---|
| `*.pbip`, `*.Report/`, `*.SemanticModel/definition/` | `*.SemanticModel/.pbi/cache.abf` (datos en caché) |
| `powerquery/`, `dax/`, `model/`, `theme/`, `scripts/`, `docs/` | `.pbi/localSettings.json` |
| `data/raw/`, `data/reference/`, `data/validation/` (datos abiertos) | El `.pbix` antiguo |

Nombre sugerido del repositorio: `digesett-road-safety-intelligence`.

## 4. Publicar en vivo: opciones

Power BI **no permite crear una cuenta con un correo personal**: la documentación de Microsoft indica que el registro requiere una cuenta de trabajo o escuela y que no acepta dominios de correo de consumo (Gmail, Hotmail, Outlook.com). Además, **Publicar en la web** necesita una licencia de Power BI y que el administrador del tenant tenga habilitada esa opción; desde un área de trabajo distinta de "Mi área de trabajo" exige Pro o Premium Per User. El enlace público deja de funcionar si la licencia del creador vence.

| Opción | Costo | Ventaja | Limitación | Recomendación |
|---|---|---|---|---|
| **A. Versión web HTML en GitHub Pages** (como RD Intelligence) | Gratis | En vivo, permanente, sin cuenta Microsoft; interactiva | Es una réplica web del dashboard, no el `.pbix` | ⭐ Principal |
| **B. Video recorrido de 2–3 min** (YouTube / LinkedIn) | Gratis | Muestra la interactividad real de Power BI | No es navegable | ⭐ Complemento obligatorio |
| **C. Capturas, GIF y PDF** en el README | Gratis | Permanente; visible en GitHub | Estático | ⭐ Complemento obligatorio |
| **D. PBIP en GitHub** | Gratis | Cualquiera lo abre en Power BI Desktop | Requiere instalar Desktop | Incluido |
| **E. Prueba de Microsoft 365 E5** (tenant `onmicrosoft.com`) + Publicar en la web | Gratis durante la prueba; pide tarjeta | Enlace real de Power BI | Vence; hay que cancelar antes del cobro; el enlace muere al vencer | Solo para una ventana corta (entrevistas) |
| **F. Comprar Power BI Pro 1–2 meses** | Pago mensual | Enlace real de Power BI | Requiere tenant de trabajo; el enlace muere al dejar de pagar | Si tienes una entrevista concreta |

### Recomendación

Combinar **A + B + C + D**: una versión web permanente en tu sitio de GitHub Pages, un video corto del dashboard real en Power BI, capturas en el README y el PBIP descargable. Así el proyecto se puede ver "en vivo" hoy, sin depender de una licencia, y los entrevistadores ven además el trabajo en Power BI.

### Si eliges la opción E (prueba de Microsoft 365)

1. Crear la prueba de Microsoft 365 E5 con un dominio `onmicrosoft.com` nuevo (pide tarjeta).
2. Entrar a app.powerbi.com con esa cuenta.
3. Como administrador del tenant: **Configuración → Portal de administración → Configuración del inquilino → Exportar y compartir → Publicar en la web → Habilitado**.
4. Desde Power BI Desktop, iniciar sesión con esa cuenta y **Publicar** en "Mi área de trabajo".
5. En el servicio: **Archivo → Insertar informe → Publicar en la web (público)**.
6. Poner un recordatorio para cancelar la prueba antes de la fecha de cobro.

> Publicar en la web hace el informe visible para cualquier persona en internet. Los datos de este proyecto son abiertos, pero el logo es de la institución: mantener la leyenda "Proyecto independiente, no oficial".

## 5. Exportar a PDF (para el README)

**Archivo → Exportar → Exportar a PDF** en Power BI Desktop. Guardar como `docs/assets/DIGESETT_Road_Safety_Intelligence.pdf`.

## 6. Fuentes

- Microsoft Learn · [Publish to web from Power BI](https://learn.microsoft.com/en-us/power-bi/collaborate-share/service-publish-to-web)
- Microsoft Learn · [Power BI Self-Service Licensing and Trial FAQ](https://learn.microsoft.com/en-us/power-bi/fundamentals/service-self-service-sign-up-help)
- Microsoft Q&A · [Best option to publish a Power BI project for a portfolio?](https://learn.microsoft.com/en-us/answers/questions/5437083/best-option-to-publish-a-power-bi-project-for-a-po)
