// ============================================================================
// FactRoadFatalities  (hechos — CARGAR al modelo)
// Grano   : 1 fila = mes (total nacional).  Esperado: 120 filas | 18,785
// La lógica vive en stg_Fallecimientos para que DimDate pueda leer la cobertura
// desde el staging sin depender de una tabla cargada.
// ============================================================================
let
    Origen = stg_Fallecimientos
in
    Origen
