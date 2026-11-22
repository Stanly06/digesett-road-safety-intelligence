"""Genera web/index.html a partir de web/index.src.html incrustando el logo como data URI.

Uso:  python scripts/build_web_page.py
"""
import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main() -> None:
    src = (ROOT / "web" / "index.src.html").read_text(encoding="utf-8")
    logo = base64.b64encode((ROOT / "web" / "assets" / "digesett_logo.png").read_bytes()).decode()
    (ROOT / "web" / "index.html").write_text(src.replace("__LOGO__", "data:image/png;base64," + logo), encoding="utf-8")
    print("web/index.html generado")

if __name__ == "__main__":
    main()
