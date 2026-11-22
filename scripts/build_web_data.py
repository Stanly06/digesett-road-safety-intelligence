"""Genera web/data.json a partir de los CSV validados del repositorio.

Uso:  python scripts/build_web_data.py
Entradas: data/validation/*.csv (hechos validados), data/reference/*.csv (catálogo,
denominadores y grupo de conductas de alto riesgo). Salida: web/data.json.
"""
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
REF, VAL = ROOT / "data" / "reference", ROOT / "data" / "validation"

def main() -> None:
    f = pd.read_csv(VAL / "FactTrafficViolations_expected.csv", parse_dates=["MonthStartDate"])
    x = pd.read_csv(VAL / "FactRoadFatalities_expected.csv", parse_dates=["MonthStartDate"])
    d = pd.read_csv(REF / "DimInfraction.csv")
    den = pd.read_csv(REF / "denominators.csv")
    hr = pd.read_csv(REF / "high_risk_types.csv")
    y0 = int(f.MonthStartDate.dt.year.min())
    data = {
        "y0": y0,
        "inf": [[int(r.InfractionID), r.InfractionType, None if pd.isna(r.LegalReference) else r.LegalReference, r.InfractionCategory] for r in d.itertuples()],
        "v": [[(r.MonthStartDate.year - y0) * 12 + r.MonthStartDate.month - 1, int(r.InfractionID), int(r.ViolationCount)] for r in f.itertuples()],
        "d": [[int(r.MonthStartDate.year), int(r.MonthStartDate.month), int(r.Fatalities)] for r in x.itertuples()],
        "den": [[int(r.Year), int(r.Population), int(r.VehicleFleet), r.VehicleFleetPrecision] for r in den.itertuples()],
        "hr": [[int(r.InfractionID), r.RiskFactor] for r in hr.itertuples()],
    }
    out = ROOT / "web" / "data.json"
    out.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"web/data.json: {len(data['v'])} filas de infracciones, {len(data['d'])} meses de fallecimientos")

if __name__ == "__main__":
    main()
