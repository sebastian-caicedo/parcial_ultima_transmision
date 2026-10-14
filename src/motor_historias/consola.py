"""Interfaz de consola (RF04, RF09, RF11, RF13, RF17).

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
        self._salida(self._linea_comandos())

        while True:
            texto = self._leer("Elige una opción: ")
            if texto is None or texto == "s":
                return False
            if texto in ("r", "d"):
                return self._comando(texto)
            if texto.isdigit() and 1 <= int(texto) <= len(opciones):
                resultado = self.sesion.elegir(opciones[int(texto) - 1].id)
                if not resultado.aceptada:
                    self._salida(f"No se pudo elegir: {resultado.motivo}")
                return True
            self._salida(f"Entrada no válida. Escribe un número del 1 al {len(opciones)} o una letra del menú.")

    def _linea_comandos(self) -> str:
        comandos = "  r) Reiniciar   s) Salir"
        if self.sesion.puede_deshacer():
            comandos += "   d) Deshacer última decisión"
        return comandos

    def _comando(self, texto: str) -> bool:
        """Ejecuta 'r' (reiniciar) o 'd' (deshacer). Siempre continúa la partida."""
        if texto == "r":
            self.sesion.reiniciar()
            self._salida("Partida reiniciada.")
        else:
            resultado = self.sesion.deshacer()
            self._salida("Última decisión deshecha." if resultado.aceptada
                         else f"No se pudo deshacer: {resultado.motivo}")
        return True

    def _menu_cierre(self) -> bool:
        self._salida(self._linea_comandos())
        while True:
            texto = self._leer("Elige: ")
            if texto is None or texto == "s":
                return False
            if texto in ("r", "d"):
                return self._comando(texto)
            self._salida("Entrada no válida. Escribe una letra del menú.")
