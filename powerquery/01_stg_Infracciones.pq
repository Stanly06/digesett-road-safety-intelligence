// ============================================================================
// stg_Infracciones  (staging — desactivar "Habilitar carga")
// Entrada : data\raw\Infracciones-de-Transito-DIGESETT-2018-2026.xlsx
//           849 filas, formato ancho: INFRACCIONES | ENERO..DICIEMBRE | AÑO
// Salida  : formato largo, 1 fila = infracción × mes × año  (10,188 filas)
// ============================================================================
let
    // 1. Leer el libro. El tercer argumento (true) retrasa la inferencia de tipos:
    //    los tipos se fijan explícitamente más abajo, no los adivina Power BI.
    Origen = Excel.Workbook(
        File.Contents(pRutaDatos & "raw\Infracciones-de-Transito-DIGESETT-2018-2026.xlsx"),
        null, true),

    // 2. Navegar por nombre de hoja (no por posición): si agregan hojas, no se rompe.
    Hoja = Origen{[Item = "INFRACCIONES 2018-2026", Kind = "Sheet"]}[Data],
    Encabezados = Table.PromoteHeaders(Hoja, [PromoteAllScalars = true]),

    // 3. Limpiar el texto de la infracción.
    //    Text.Clean quita caracteres de control; Text.Trim quita espacios al inicio/fin.
    //    Hay 7 valores con espacios sobrantes (p. ej. " Transitar Sin Tablilla (Art.-42)")
    //    que, sin esto, se contarían como una infracción distinta.
    NombreLimpio = Table.TransformColumns(
        Encabezados,
        {{"INFRACCIONES", each Text.Trim(Text.Clean(_)), type text}}),

    // 4. UNPIVOT: los 12 meses pasan de columnas a filas.
    //    Se usa UnpivotOtherColumns (y no Unpivot de 12 columnas nombradas) para
    //    declarar qué columnas son identificadores; todo lo demás es un mes.
    //    Por qué: un modelo tabular necesita UNA columna de valor y UNA de período
    //    para poder relacionarse con DimDate y usar inteligencia de tiempo.
    Unpivot = Table.UnpivotOtherColumns(
        NombreLimpio, {"INFRACCIONES", "AÑO"}, "MesNombre", "ViolationCount"),

    // 5. Tipos explícitos. Int64 porque son conteos enteros (verificado: 0 decimales).
    Tipos = Table.TransformColumnTypes(
        Unpivot,
        {{"AÑO", Int64.Type}, {"MesNombre", type text}, {"ViolationCount", Int64.Type}}),

    // 6. Nombre de mes -> número de mes, con una lista fija en español.
    //    No depende de la configuración regional del equipo.
    Meses = {"ENERO","FEBRERO","MARZO","ABRIL","MAYO","JUNIO",
             "JULIO","AGOSTO","SEPTIEMBRE","OCTUBRE","NOVIEMBRE","DICIEMBRE"},
    MesNumero = Table.AddColumn(
        Tipos, "MonthNumber",
        each List.PositionOf(Meses, Text.Upper(Text.Trim([MesNombre]))) + 1, Int64.Type),

    // 7. Clave de período: primer día del mes. El dato es mensual; el día 1 es solo
    //    una convención para relacionar con DimDate, no implica información diaria.
    Fecha = Table.AddColumn(
        MesNumero, "MonthStartDate", each #date([AÑO], [MonthNumber], 1), type date),

    Renombrado = Table.RenameColumns(
        Fecha, {{"INFRACCIONES", "InfractionNameRaw"}, {"AÑO", "Year"}}),
    Resultado = Table.SelectColumns(
        Renombrado,
        {"InfractionNameRaw", "Year", "MonthNumber", "MonthStartDate", "ViolationCount"})
in
    Resultado
