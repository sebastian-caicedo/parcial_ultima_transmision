"""Datos compartidos por las pruebas."""
import copy
import json
from pathlib import Path

import pytest

from motor_historias.cargador import cargar_historia
from motor_historias.sesion import Sesion

RAIZ = Path(__file__).resolve().parent.parent
HISTORIA_REFERENCIA = RAIZ / "data" / "la_ultima_transmision.json"
SEGUNDA_HISTORIA = RAIZ / "data" / "segunda_historia.json"
DATOS_INVALIDOS = Path(__file__).resolve().parent / "datos_invalidos"

_DATOS = json.loads(HISTORIA_REFERENCIA.read_text(encoding="utf-8"))


@pytest.fixture
def datos_referencia():
    """Copia independiente del JSON de referencia, para modificarla en cada prueba."""
    return copy.deepcopy(_DATOS)


@pytest.fixture
def sesion():
    """Sesión nueva sobre la historia de referencia cargada desde el archivo real."""
    return Sesion(cargar_historia(HISTORIA_REFERENCIA))


def buscar_opcion(datos, id_escena, id_opcion):
    escena = next(e for e in datos["escenas"] if e["id"] == id_escena)
    return next(o for o in escena["opciones"] if o["id"] == id_opcion)


def buscar_escena(datos, id_escena):
    return next(e for e in datos["escenas"] if e["id"] == id_escena)
