// ============================================================================
// MapInfraction  (staging — desactivar "Habilitar carga")
// Entrada : data\reference\MapInfraction.csv   (146 nombres originales)
// Función : tabla puente  nombre original -> InfractionID canónico.
// Por qué : 2018 usa 41 nombres y 2019-2026 usa 101; ninguno coincide. Además
//           4 infracciones cambian de escritura entre años. Resolverlo con una
//           tabla de referencia (y no con 40 Table.ReplaceValue encadenados)
//           hace el mapeo auditable, versionable en Git y editable sin tocar M.
// ============================================================================
let
    Origen = Csv.Document(
        File.Contents(pRutaDatos & "reference\MapInfraction.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(
        Encabezados,
        {{"InfractionNameRaw", type text}, {"InfractionID", Int64.Type},
         {"SourceCatalog", type text}, {"MappingConfidence", type text},
         {"MappingNote", type text}}),
    // Misma limpieza que en stg_Infracciones para que el join coincida exactamente.
    Limpio = Table.TransformColumns(
        Tipos, {{"InfractionNameRaw", each Text.Trim(Text.Clean(_)), type text}})
in
    Limpio
