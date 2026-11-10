// ============================================================================
// FactTrafficViolations  (hechos — CARGAR al modelo)
// Grano   : 1 fila = InfractionID × mes
// Salida esperada: 9,580 filas | 13,289,441 infracciones
//                  (ver data\validation\control_totals_violations.csv)
// ============================================================================
let
    Origen = stg_Infracciones,

    // 1. Asignar el InfractionID canónico.
    //    LeftOuter (no Inner): si aparece un nombre nuevo que no está en el mapeo,
    //    la fila se conserva con ID nulo y la detecta qa_InfraccionesSinMapear.
    //    Con Inner se perdería en silencio.
    Unido = Table.NestedJoin(
        Origen, {"InfractionNameRaw"},
        MapInfraction, {"InfractionNameRaw"},
        "Map", JoinKind.LeftOuter),
    ConID = Table.ExpandTableColumn(Unido, "Map", {"InfractionID"}, {"InfractionID"}),

    // 2. REGLA A — Período no reportado.
    //    El archivo trae 0 en oct-dic 2026 para las 101 infracciones: no es
    //    "cero infracciones", es que el mes aún no se publica.
    //    El corte se calcula (último mes con algún registro > 0), no se escribe
    //    a mano: cuando DIGESETT publique octubre, la consulta se ajusta sola.
    UltimoMes = List.Max(
        Table.SelectRows(ConID, each [ViolationCount] > 0)[MonthStartDate]),
    SinFuturo = Table.SelectRows(ConID, each [MonthStartDate] <= UltimoMes),

    // 3. REGLA B — Tipos que aún no se registraban (SUPUESTO documentado).
    //    En 2019, 61 de los 101 tipos traen 0 de enero a mayo y empiezan a
    //    registrar en junio. Se interpreta como "no aplica", no como cero real.
    //    Es una inferencia a partir del patrón del archivo, no una confirmación
    //    de DIGESETT. Para revertirlo, sustituir este paso por: SinNoAplica = SinFuturo
    EneMay2019 = Table.SelectRows(SinFuturo, each [Year] = 2019 and [MonthNumber] <= 5),
    SumaPorTipo = Table.Group(
        EneMay2019, {"InfractionID"},
        {{"Suma", each List.Sum([ViolationCount]), Int64.Type}}),
    // List.Buffer: fija la lista en memoria para que no se recalcule por cada fila.
    TiposNoAplica = List.Buffer(
        Table.SelectRows(SumaPorTipo, each [Suma] = 0)[InfractionID]),
    SinNoAplica = Table.SelectRows(
        SinFuturo,
        each not ([Year] = 2019 and [MonthNumber] <= 5
                  and List.Contains(TiposNoAplica, [InfractionID]))),

    // Los ceros que quedan (1,099) son ceros genuinos y se conservan:
    // "0 infracciones ese mes" es información; "sin fila" significa "sin dato".

    // 4. Solo claves y medida. El texto vive en DimInfraction (menos memoria,
    //    mejor compresión en VertiPaq). Year y MonthNumber salen de DimDate.
    Resultado = Table.SelectColumns(
        SinNoAplica, {"MonthStartDate", "InfractionID", "ViolationCount"}),
    Tipos = Table.TransformColumnTypes(
        Resultado,
        {{"MonthStartDate", type date}, {"InfractionID", Int64.Type},
         {"ViolationCount", Int64.Type}})
in
    Tipos
