"""Cargador: lee el archivo, pide la validación y construye la Historia (RF01, RF14).

Capa de carga y validación (ver docs/04_arquitectura.md). El archivo se abre solo en lectura.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .modelo import ErrorContenido, Escena, Historia, HistoriaInvalidaError, Opcion
from .validador import validar


def cargar_historia(ruta: str | Path) -> Historia:
    """Lee y valida un archivo de historia. Lanza HistoriaInvalidaError si hay errores."""
    ruta = Path(ruta)
    try:
        texto = ruta.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise HistoriaInvalidaError([ErrorContenido(
            "V01", f"No se pudo leer el archivo '{ruta.name}': {error}", ruta.name)]) from None
    try:
        datos = json.loads(texto)
    except json.JSONDecodeError as error:
        raise HistoriaInvalidaError([ErrorContenido(
            "V01", f"El archivo '{ruta.name}' no es JSON válido "
                   f"(línea {error.lineno}, columna {error.colno}).", ruta.name)]) from None
    return construir_historia(datos, origen=ruta.name)


def construir_historia(datos: Any, origen: str = "historia") -> Historia:
    """Valida datos ya leídos y, si no hay errores, crea los objetos del dominio."""
    errores = validar(datos, origen)
    if errores:
        raise HistoriaInvalidaError(errores)

    escenas = {}
    for e in datos["escenas"]:
        opciones = tuple(
            Opcion(o["id"], o["texto"], o["destino"], dict(o["condiciones"]), dict(o["efectos"]))
            for o in e["opciones"]
        )
        escenas[e["id"]] = Escena(e["id"], e["texto"], e["final"], opciones)
    return Historia(datos["titulo"], datos["inicio"], dict(datos["variables"]), escenas)
