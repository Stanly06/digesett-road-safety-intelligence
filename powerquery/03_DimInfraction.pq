// ============================================================================
// DimInfraction  (dimensión — CARGAR al modelo)
// Entrada : data\reference\DimInfraction.csv   (106 filas)
//   101 infracciones del catálogo vigente 2019-2026 (ID 1-101)
//     5 infracciones de 2018 sin equivalente claro   (ID 201-205)
// Nota    : InfractionCategory es una clasificación PROPIA del analista
//           (9 grupos); no proviene de DIGESETT. Debe rotularse así en el reporte.
// ============================================================================
let
    Origen = Csv.Document(
        File.Contents(pRutaDatos & "reference\DimInfraction.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(
        Encabezados,
        {{"InfractionID", Int64.Type}, {"InfractionType", type text},
         {"LegalReference", type text}, {"InfractionCategory", type text},
         {"CatalogStatus", type text}}),
    // Vacío -> null: distingue "sin referencia legal en la fuente" de un texto vacío.
    RefNula = Table.ReplaceValue(
        Tipos, "", null, Replacer.ReplaceValue, {"LegalReference"})
in
    RefNula
