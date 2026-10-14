"""Lanzador del motor de historias.

Uso:
    python main.py jugar data/la_ultima_transmision.json
    python main.py validar data/la_ultima_transmision.json
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from motor_historias.__main__ import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
