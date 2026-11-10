// ============================================================================
// DimDate  (dimensión — CARGAR al modelo y "Marcar como tabla de fechas" con [Date])
// Grano   : 1 fila = 1 día, años completos.  Esperado: 4,018 filas
//           (2016-01-01 a 2026-12-31)
//
// ¿Por qué diaria si los datos son mensuales?
//   Las funciones de inteligencia de tiempo de DAX (DATESYTD, SAMEPERIODLASTYEAR,
//   DATEADD) exigen una columna de fechas CONTIGUA, sin huecos, que cubra años
//   completos. Una tabla con solo el día 1 de cada mes no cumple ese contrato.
//   Los hechos se enlazan por el primer día del mes; los días 2-31 nunca tienen
//   datos. NO se expone ningún atributo de día (ni día de semana, ni número de
//   día): el usuario no puede bajar a un nivel que la fuente no tiene.
//
// El rango y los indicadores de cobertura se calculan a partir de los hechos:
// cuando se actualicen los Excel, la tabla se extiende sola.
// ============================================================================
let
    // 1. Cobertura real de cada tabla de hechos
    // Se lee de las consultas de staging (no de las tablas cargadas) para que
    // DimDate no dependa del orden de carga del modelo.
    MesesConDatos = Table.SelectRows(stg_Infracciones, each [ViolationCount] > 0)[MonthStartDate],
    MinInf = List.Min(MesesConDatos),
    MaxInf = List.Max(MesesConDatos),
    MinFal = List.Min(stg_Fallecimientos[MonthStartDate]),
    MaxFal = List.Max(stg_Fallecimientos[MonthStartDate]),

    // 2. Años completos: del 1 de enero del primer año al 31 de diciembre del último
    Inicio = #date(Date.Year(List.Min({MinInf, MinFal})), 1, 1),
    Fin    = #date(Date.Year(List.Max({MaxInf, MaxFal})), 12, 31),
    Fechas = List.Dates(Inicio, Duration.Days(Fin - Inicio) + 1, #duration(1, 0, 0, 0)),
    Base   = Table.TransformColumnTypes(
                 Table.FromList(Fechas, Splitter.SplitByNothing(), {"Date"}),
                 {{"Date", type date}}),

    // 3. Atributos de calendario (nombres en español, independientes de la
    //    configuración regional del equipo)
    MesesLargos = {"Enero","Febrero","Marzo","Abril","Mayo","Junio",
                   "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"},
    MesesCortos = {"Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"},

    Anio      = Table.AddColumn(Base, "Year", each Date.Year([Date]), Int64.Type),
    MesNum    = Table.AddColumn(Anio, "MonthNumber", each Date.Month([Date]), Int64.Type),
    MesNombre = Table.AddColumn(MesNum, "MonthName", each MesesLargos{[MonthNumber] - 1}, type text),
    MesCorto  = Table.AddColumn(MesNombre, "MonthNameShort", each MesesCortos{[MonthNumber] - 1}, type text),
    TrimNum   = Table.AddColumn(MesCorto, "QuarterNumber", each Date.QuarterOfYear([Date]), Int64.Type),
    Trim      = Table.AddColumn(TrimNum, "Quarter", each "T" & Text.From([QuarterNumber]), type text),
    AnioTrim  = Table.AddColumn(Trim, "YearQuarter",
                    each Text.From([Year]) & "-T" & Text.From([QuarterNumber]), type text),
    AnioMes   = Table.AddColumn(AnioTrim, "YearMonth",
                    each Text.From([Year]) & "-" & Text.PadStart(Text.From([MonthNumber]), 2, "0"), type text),
    AnioMesSort = Table.AddColumn(AnioMes, "YearMonthSort", each [Year] * 100 + [MonthNumber], Int64.Type),
    InicioMes = Table.AddColumn(AnioMesSort, "MonthStartDate", each Date.StartOfMonth([Date]), type date),

    // 4. MonthIndex: número de mes consecutivo (2016-01 = 24193, 2016-02 = 24194...).
    //    Permite calcular ventanas móviles y MoM con aritmética simple
    //    (MonthIndex - 1, MonthIndex - 11...) sin depender de funciones de tiempo.
    MesIndice = Table.AddColumn(InicioMes, "MonthIndex", each [Year] * 12 + [MonthNumber], Int64.Type),

    // 5. Indicadores de cobertura — base para "no comparar períodos parciales con completos"
    TieneInf = Table.AddColumn(MesIndice, "HasViolationData",
                   each [MonthStartDate] >= MinInf and [MonthStartDate] <= MaxInf, type logical),
    TieneFal = Table.AddColumn(TieneInf, "HasFatalityData",
                   each [MonthStartDate] >= MinFal and [MonthStartDate] <= MaxFal, type logical),
    // Un año de infracciones es "completo" si tiene datos de enero a diciembre.
    AnioCompleto = Table.AddColumn(TieneFal, "IsCompleteViolationYear",
                   each [Year] >= Date.Year(MinInf)
                        and ([Year] < Date.Year(MaxInf)
                             or ([Year] = Date.Year(MaxInf) and Date.Month(MaxInf) = 12)),
                   type logical),
    // Período en el que AMBOS hechos tienen datos: único tramo válido para verlos juntos.
    Comun = Table.AddColumn(AnioCompleto, "IsCommonPeriod",
                   each [HasViolationData] and [HasFatalityData], type logical),
    // Etiqueta de año para ejes: "2026*" avisa que el año es parcial.
    EtiquetaAnio = Table.AddColumn(Comun, "YearLabel",
                   each if [Year] = Date.Year(MaxInf) and Date.Month(MaxInf) < 12
                        then Text.From([Year]) & "*" else Text.From([Year]), type text)
in
    EtiquetaAnio
