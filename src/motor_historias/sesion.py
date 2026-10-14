"""Sesión de juego: estado de una partida y reglas de elección.

Capa de motor (ver docs/04_arquitectura.md). Sigue el diagrama de secuencia
docs/diagramas/04_secuencia_elegir.puml y el de estados 05_estados_sesion.puml.
No contiene ningún id concreto de escena ni de opción: todo sale de la Historia.
"""
from __future__ import annotations

from .modelo import Escena, Historia, Opcion, ResultadoEleccion


class Sesion:
    def __init__(self, historia: Historia):
        self._historia = historia
        self._escena: Escena
        self._estado: dict[str, bool]
        self.reiniciar()

    # ----- Consultas -----
    @property
    def historia(self) -> Historia:
        return self._historia

    @property
    def escena_actual(self) -> Escena:
        return self._escena

    @property
    def estado(self) -> dict[str, bool]:
        """Copia del estado: quien la lea no puede modificar la partida."""
        return dict(self._estado)

    def opciones_habilitadas(self) -> list[Opcion]:
        """Solo las opciones cuyas condiciones se cumplen (RF05, RF10)."""
        return [opcion for opcion in self._escena.opciones if opcion.esta_habilitada(self._estado)]

    def esta_en_final(self) -> bool:
        """RF11."""
        return self._escena.final

    def esta_bloqueada(self) -> bool:
        """Escena no final sin ninguna opción habilitada (RF13)."""
        return not self._escena.final and not self.opciones_habilitadas()

    # ----- Comandos -----
    def elegir(self, id_opcion: object) -> ResultadoEleccion:
        """Aplica la opción si existe y está habilitada (RF06, RF07).

        Cualquier otro caso se rechaza sin cambiar escena ni estado (RF08, CA02).
        """
        if not isinstance(id_opcion, str):
            return ResultadoEleccion(False, "La elección debe ser el id de una opción.")
        if self._escena.final:
            return ResultadoEleccion(False, "La partida terminó: no hay opciones de avance.")

        opcion = self._escena.opcion(id_opcion)
        if opcion is None:
            return ResultadoEleccion(
                False, f"La opción '{id_opcion}' no existe en la escena '{self._escena.id}'."
            )
        if not opcion.esta_habilitada(self._estado):
            return ResultadoEleccion(
                False, f"La opción '{id_opcion}' no está habilitada con la información actual."
            )

        self._estado.update(opcion.efectos)
        self._escena = self._historia.escena(opcion.destino)
        return ResultadoEleccion(True)

    def reiniciar(self) -> None:
        """Vuelve a la escena de inicio con las variables iniciales (RF12)."""
        self._escena = self._historia.escena(self._historia.inicio)
        self._estado = dict(self._historia.variables_iniciales)
