"""Punto de entrada: python main.py jugar|validar <ruta_historia.json>"""
from __future__ import annotations

import argparse
import sys

from .cargador import cargar_historia
from .consola import InterfazConsola
from .modelo import HistoriaInvalidaError
from .sesion import Sesion


def _configurar_salida() -> None:
    # Evita errores con tildes en consolas de Windows
    for flujo in (sys.stdout, sys.stderr):
        try:
            flujo.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def main(argv: list[str] | None = None) -> int:
    _configurar_salida()
    parser = argparse.ArgumentParser(prog="main.py", description="Motor de historias interactivas")
    sub = parser.add_subparsers(dest="comando", required=True)
    sub.add_parser("jugar", help="Jugar una historia").add_argument("ruta")
    sub.add_parser("validar", help="Validar una historia sin jugarla").add_argument("ruta")
    args = parser.parse_args(argv)

    try:
        historia = cargar_historia(args.ruta)
    except HistoriaInvalidaError as error:
        print(f"La historia '{args.ruta}' no es válida. Errores encontrados ({len(error.errores)}):")
        for e in error.errores:
            print(f"  - {e}")
        return 1

    if args.comando == "validar":
        print(f"Historia válida: '{historia.titulo}' ({len(historia.escenas)} escenas).")
        return 0

    InterfazConsola(Sesion(historia)).ejecutar()
    return 0


if __name__ == "__main__":
    sys.exit(main())
