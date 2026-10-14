"""Validador de historias: detecta las categorías de error V01-V09 (RF14-RF16).

Capa de carga y validación (ver docs/04_arquitectura.md).
Recibe los datos ya leídos del JSON y devuelve TODOS los errores encontrados (supuesto P2).
Nunca modifica los datos (decisión de responsabilidad profesional, sección 1.6).
"""
from __future__ import annotations

from typing import Any

from .modelo import ErrorContenido

CAMPOS_HISTORIA = {"titulo": str, "inicio": str, "variables": dict, "escenas": list}
CAMPOS_ESCENA = {"id": str, "texto": str, "final": bool, "opciones": list}
CAMPOS_OPCION = {"id": str, "texto": str, "destino": str, "condiciones": dict, "efectos": dict}

_NOMBRE_TIPO = {str: "texto", bool: "booleano", dict: "mapa", list: "lista"}


def es_booleano(valor: Any) -> bool:
    # En Python, True == 1; se exige el tipo bool exacto.
    return type(valor) is bool


def _tipo_correcto(valor: Any, tipo: type) -> bool:
    return es_booleano(valor) if tipo is bool else isinstance(valor, tipo) and not es_booleano(valor)


def _revisar_campos(objeto: dict, campos: dict[str, type], donde: str, errores: list) -> bool:
    """Agrega V02 por cada campo ausente o de tipo incorrecto. Devuelve True si todo está bien."""
    correcto = True
    for nombre, tipo in campos.items():
        if nombre not in objeto:
            errores.append(ErrorContenido("V02", f"Falta el campo '{nombre}' en {donde}.", donde))
            correcto = False
        elif not _tipo_correcto(objeto[nombre], tipo):
            errores.append(ErrorContenido(
                "V02", f"El campo '{nombre}' en {donde} debe ser de tipo {_NOMBRE_TIPO[tipo]}.", donde))
            correcto = False
    return correcto


def validar(datos: Any, origen: str = "historia") -> list[ErrorContenido]:
    errores: list[ErrorContenido] = []

    # V01: la raíz debe ser un objeto JSON
    if not isinstance(datos, dict):
        return [ErrorContenido("V01", f"Estructura incorrecta en '{origen}': la raíz debe ser un objeto JSON.", origen)]

    # V02 en la raíz: sin la estructura base no se puede revisar lo demás (supuesto P2)
    if not _revisar_campos(datos, CAMPOS_HISTORIA, "la historia", errores):
        return errores

    # V08 en variables iniciales
    variables: dict = datos["variables"]
    for nombre, valor in variables.items():
        if not es_booleano(valor):
            errores.append(ErrorContenido(
                "V08", f"La variable '{nombre}' tiene el valor inicial {valor!r}, que no es booleano.",
                f"variables.{nombre}"))
    declaradas = set(variables)

    # Primera pasada: ids de escena (V04) y escenas bien formadas
    escenas_validas: list[tuple[str, dict]] = []
    ids_escena: set[str] = set()
    for i, escena in enumerate(datos["escenas"]):
        if not isinstance(escena, dict):
            errores.append(ErrorContenido("V02", f"La escena en la posición {i} no es un objeto.", f"escenas[{i}]"))
            continue
        id_escena = escena.get("id") if isinstance(escena.get("id"), str) else f"escenas[{i}]"
        donde = f"la escena '{id_escena}'"
        if not _revisar_campos(escena, CAMPOS_ESCENA, donde, errores):
            if isinstance(escena.get("id"), str):
                ids_escena.add(escena["id"])
            continue
        if id_escena in ids_escena:
            errores.append(ErrorContenido("V04", f"El id de escena '{id_escena}' está repetido.", id_escena))
        ids_escena.add(id_escena)
        escenas_validas.append((id_escena, escena))

    # V03: inicio existente
    if datos["inicio"] not in ids_escena:
        errores.append(ErrorContenido(
            "V03", f"La escena de inicio '{datos['inicio']}' no existe.", "inicio"))

    # Segunda pasada: opciones de cada escena
    for id_escena, escena in escenas_validas:
        opciones = escena["opciones"]

        # V09: cantidad de opciones compatible con 'final'
        if escena["final"] and opciones:
            errores.append(ErrorContenido(
                "V09", f"La escena '{id_escena}' es final pero tiene {len(opciones)} opción(es).", id_escena))
        if not escena["final"] and not opciones:
            errores.append(ErrorContenido(
                "V09", f"La escena '{id_escena}' no es final y no tiene opciones.", id_escena))

        ids_opcion: set[str] = set()
        for j, opcion in enumerate(opciones):
            if not isinstance(opcion, dict):
                errores.append(ErrorContenido(
                    "V02", f"La opción en la posición {j} de la escena '{id_escena}' no es un objeto.",
                    f"{id_escena}.opciones[{j}]"))
                continue
            id_opcion = opcion.get("id") if isinstance(opcion.get("id"), str) else f"opciones[{j}]"
            donde = f"la opción '{id_opcion}' de la escena '{id_escena}'"
            ubicacion = f"{id_escena}.{id_opcion}"
            if not _revisar_campos(opcion, CAMPOS_OPCION, donde, errores):
                continue

            # V05: id de opción repetido dentro de la escena
            if id_opcion in ids_opcion:
                errores.append(ErrorContenido(
                    "V05", f"El id de opción '{id_opcion}' está repetido en la escena '{id_escena}'.", ubicacion))
            ids_opcion.add(id_opcion)

            # V06: destino inexistente
            if opcion["destino"] not in ids_escena:
                errores.append(ErrorContenido(
                    "V06", f"La opción '{id_opcion}' de la escena '{id_escena}' apunta a "
                           f"'{opcion['destino']}', que no existe.", ubicacion))

            # V07 y V08 en condiciones y efectos
            for mapa in ("condiciones", "efectos"):
                for variable, valor in opcion[mapa].items():
                    if variable not in declaradas:
                        errores.append(ErrorContenido(
                            "V07", f"La variable '{variable}' usada en {mapa} de '{id_opcion}' "
                                   f"({id_escena}) no está declarada.", ubicacion))
                    if not es_booleano(valor):
                        errores.append(ErrorContenido(
                            "V08", f"En {mapa} de '{id_opcion}' ({id_escena}), '{variable}' tiene el valor "
                                   f"{valor!r}, que no es booleano.", ubicacion))
    return errores
