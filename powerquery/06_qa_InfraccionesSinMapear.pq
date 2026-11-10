// ============================================================================
// qa_InfraccionesSinMapear  (control de calidad — desactivar "Habilitar carga")
// Debe devolver 0 filas. Si devuelve alguna, hay un nombre en el Excel que no
// existe en MapInfraction.csv (p. ej. tras actualizar el archivo de DIGESETT):
// agregarlo al CSV antes de publicar.
// ============================================================================
let
    Unido = Table.NestedJoin(
        stg_Infracciones, {"InfractionNameRaw"},
        MapInfraction, {"InfractionNameRaw"},
        "Map", JoinKind.LeftAnti),
    Resumen = Table.Group(
        Unido, {"InfractionNameRaw"},
        {{"Filas", each Table.RowCount(_), Int64.Type},
         {"Infracciones", each List.Sum([ViolationCount]), Int64.Type},
         {"PrimerAño", each List.Min([Year]), Int64.Type},
         {"UltimoAño", each List.Max([Year]), Int64.Type}})
in
    Resumen
