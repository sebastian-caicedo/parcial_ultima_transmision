"""Prueba de humo: confirma que el entorno corre pytest y que la historia de referencia es JSON legible.
Se reemplazará por las pruebas U1–U5 e I1 cuando exista el motor."""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def test_historia_de_referencia_es_json_legible():
    datos = json.loads((RAIZ / "data" / "la_ultima_transmision.json").read_text(encoding="utf-8"))
    assert datos["inicio"] == "E1"
    assert len(datos["escenas"]) == 6
