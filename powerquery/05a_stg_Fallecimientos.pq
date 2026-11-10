// ============================================================================
// stg_Fallecimientos  (staging — desactivar "Habilitar carga")
// Entrada : data\raw\Fallecimientos-segun-Meses-DIGESETT-2016-2025.xlsx
//           120 filas, formato largo: MES | FALLECIDOS | AÑO
// Grano   : 1 fila = mes (total nacional). Sin tipo, provincia ni causa.
// Salida esperada: 120 filas | 18,785 fallecidos | 2016-01 a 2025-12
// Importante: se relaciona SOLO con DimDate. Nunca con FactTrafficViolations
//             ni con DimInfraction (no existe ese detalle en la fuente).
// ============================================================================
let
    Origen = Excel.Workbook(
        File.Contents(pRutaDatos & "raw\Fallecimientos-segun-Meses-DIGESETT-2016-2025.xlsx"),
        null, true),
    Hoja = Origen{[Item = "Fallecimientos Segun Meses", Kind = "Sheet"]}[Data],
    Encabezados = Table.PromoteHeaders(Hoja, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(
        Encabezados,
        {{"MES", type text}, {"FALLECIDOS", Int64.Type}, {"AÑO", Int64.Type}}),
    MesLimpio = Table.TransformColumns(
        Tipos, {{"MES", each Text.Upper(Text.Trim(_)), type text}}),

    // Errata de la fuente: el mes 11 viene como "NOVIEMBRES" en los 10 años.
    // Replacer.ReplaceValue sustituye el valor COMPLETO de la celda (no subcadenas),
    // así que no hay riesgo de tocar otros textos.
    Noviembre = Table.ReplaceValue(
        MesLimpio, "NOVIEMBRES", "NOVIEMBRE", Replacer.ReplaceValue, {"MES"}),

    Meses = {"ENERO","FEBRERO","MARZO","ABRIL","MAYO","JUNIO",
             "JULIO","AGOSTO","SEPTIEMBRE","OCTUBRE","NOVIEMBRE","DICIEMBRE"},
    MesNumero = Table.AddColumn(
        Noviembre, "MonthNumber", each List.PositionOf(Meses, [MES]) + 1, Int64.Type),
    // Si un mes no se reconoce, List.PositionOf devuelve -1 -> MonthNumber = 0
    // -> #date falla con error visible. Es intencional: mejor error que dato mal fechado.
    Fecha = Table.AddColumn(
        MesNumero, "MonthStartDate", each #date([AÑO], [MonthNumber], 1), type date),
    Resultado = Table.SelectColumns(
        Table.RenameColumns(Fecha, {{"FALLECIDOS", "Fatalities"}}),
        {"MonthStartDate", "Fatalities"})
in
    Resultado
