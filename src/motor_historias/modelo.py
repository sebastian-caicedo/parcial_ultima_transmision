"""Modelo de dominio: Historia, Escena, Opcion y los objetos de resultado.

Capa de motor (ver docs/04_arquitectura.md). No depende de archivos, consola ni validador.
Los nombres coinciden con el diagrama de clases (docs/diagramas/03_clases.puml).
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Opcion:
    """Decisión disponible en una escena (RF05-RF07)."""

    id: str
    texto: str
    destino: str
    condiciones: dict[str, bool]
    efectos: dict[str, bool]

    def esta_habilitada(self, estado: dict[str, bool]) -> bool:
        """Verdadero si TODAS las condiciones coinciden con el estado.

        Un mapa de condiciones vacío siempre habilita la opción.
        """
        return all(estado.get(variable) == valor for variable, valor in self.condiciones.items())


@dataclass(frozen=True)
class Escena:
    """Fragmento de la historia. Final si no tiene opciones de avance (RF11)."""

    id: str
    texto: str
    final: bool
    opciones: tuple[Opcion, ...]

    def opcion(self, id_opcion: str) -> Opcion | None:
        """Devuelve la opción con ese id, o None si no existe en esta escena."""
        for opcion in self.opciones:
            if opcion.id == id_opcion:
                return opcion
        return None


@dataclass(frozen=True)
class Historia:
    """Historia ya validada: siempre tiene inicio, destinos y variables correctos."""

    titulo: str
    inicio: str
    variables_iniciales: dict[str, bool]
    escenas: dict[str, Escena]

    def escena(self, id_escena: str) -> Escena:
        return self.escenas[id_escena]


@dataclass(frozen=True)
class ResultadoEleccion:
    """Resultado de intentar elegir una opción. Un rechazo no es una excepción (RNF03)."""

    aceptada: bool
    motivo: str = ""


@dataclass(frozen=True)
class ErrorContenido:
    """Error encontrado por el validador (RF15). codigo: V01 a V09."""

    codigo: str
    mensaje: str
    ubicacion: str = ""

    def __str__(self) -> str:
        return f"{self.codigo} {self.mensaje}"


class HistoriaInvalidaError(Exception):
    """Se lanza al cargar una historia con errores. Impide crear la sesión (RF14)."""

    def __init__(self, errores: list[ErrorContenido]):
        self.errores = list(errores)
        super().__init__("\n".join(str(error) for error in self.errores))
