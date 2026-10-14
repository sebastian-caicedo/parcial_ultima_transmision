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
        # Cambio hora 6 (RF17-RF20): copia de escena y estado ANTES de la última
        # elección válida. Un solo nivel: None significa que no hay retroceso disponible.
        self._anterior: tuple[Escena, dict[str, bool]] | None = None
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

    def puede_deshacer(self) -> bool:
        """Hay una elección válida que todavía no se ha deshecho (RF18, RF19)."""
        return self._anterior is not None

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

        # Solo una elección válida reemplaza el punto de retroceso (RF20)
        self._anterior = (self._escena, dict(self._estado))
        self._estado.update(opcion.efectos)
        self._escena = self._historia.escena(opcion.destino)
        return ResultadoEleccion(True)

    def deshacer(self) -> ResultadoEleccion:
        """Revierte la última elección válida: escena y TODAS las variables (RF17).

        Un solo nivel: después de deshacer no hay otro retroceso hasta una nueva
        elección válida (RF18). Funciona también desde un final o un bloqueo.
        """
        if self._anterior is None:
            return ResultadoEleccion(False, "No hay una decisión que deshacer.")
        self._escena, estado = self._anterior
        self._estado = dict(estado)
        self._anterior = None
        return ResultadoEleccion(True)

    def reiniciar(self) -> None:
        """Vuelve a la escena de inicio con las variables iniciales y borra el historial (RF12, RF19)."""
        self._escena = self._historia.escena(self._historia.inicio)
        self._estado = dict(self._historia.variables_iniciales)
        self._anterior = None
