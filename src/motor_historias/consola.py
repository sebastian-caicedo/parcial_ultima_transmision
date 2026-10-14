"""Interfaz de consola (RF04, RF09, RF11, RF13).

Capa de interfaz (ver docs/04_arquitectura.md). Solo muestra y traduce la entrada
del lector a ids de opción; todas las reglas las decide la Sesion.
Recibe funciones de entrada y salida para poder probarla sin teclado.
"""
from __future__ import annotations

from typing import Callable

from .sesion import Sesion

SEPARADOR = "-" * 60


class InterfazConsola:
    def __init__(self, sesion: Sesion,
                 entrada: Callable[[str], str] = input,
                 salida: Callable[[str], None] = print):
        self.sesion = sesion
        self._entrada = entrada
        self._salida = salida

    def ejecutar(self) -> None:
        self._salida(f"\n=== {self.sesion.historia.titulo} ===")
        while True:
            if not self._turno():
                self._salida("Hasta pronto.")
                return

    def _leer(self, mensaje: str) -> str | None:
        try:
            return self._entrada(mensaje).strip().lower()
        except (EOFError, KeyboardInterrupt):
            return None

    def _turno(self) -> bool:
        """Muestra la escena y procesa una entrada. Devuelve False si el lector sale."""
        escena = self.sesion.escena_actual
        self._salida(f"\n{SEPARADOR}\n[{escena.id}] {escena.texto}\n{SEPARADOR}")

        if self.sesion.esta_en_final():
            self._salida("*** FIN DE LA PARTIDA ***")
            return self._menu_cierre()
        if self.sesion.esta_bloqueada():
            self._salida("No hay opciones disponibles con la información actual (historia bloqueada).")
            return self._menu_cierre()

        opciones = self.sesion.opciones_habilitadas()
        for numero, opcion in enumerate(opciones, start=1):
            self._salida(f"  {numero}) {opcion.texto}")
        self._salida("  r) Reiniciar   s) Salir")

        while True:
            texto = self._leer("Elige una opción: ")
            if texto is None or texto == "s":
                return False
            if texto == "r":
                self.sesion.reiniciar()
                self._salida("Partida reiniciada.")
                return True
            if texto.isdigit() and 1 <= int(texto) <= len(opciones):
                resultado = self.sesion.elegir(opciones[int(texto) - 1].id)
                if not resultado.aceptada:
                    self._salida(f"No se pudo elegir: {resultado.motivo}")
                return True
            self._salida(f"Entrada no válida. Escribe un número del 1 al {len(opciones)}, 'r' o 's'.")

    def _menu_cierre(self) -> bool:
        while True:
            texto = self._leer("r) Jugar otra vez   s) Salir: ")
            if texto is None or texto == "s":
                return False
            if texto == "r":
                self.sesion.reiniciar()
                self._salida("Nueva partida.")
                return True
            self._salida("Entrada no válida. Escribe 'r' o 's'.")
