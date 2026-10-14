"""U4: los errores de contenido producen rechazo controlado (RF14-RF16, CA03).

Cada caso parte de una copia válida de la historia de referencia y rompe una sola cosa.
"""
import json

import pytest

from conftest import buscar_escena, buscar_opcion
from motor_historias.cargador import cargar_historia, construir_historia
from motor_historias.modelo import HistoriaInvalidaError
from motor_historias.validador import validar


def _quitar_titulo(d): del d["titulo"]
def _quitar_destino(d): del buscar_opcion(d, "E2", "investigar")["destino"]
def _escenas_no_es_lista(d): d["escenas"] = {"E1": {}}
def _inicio_inexistente(d): d["inicio"] = "E0"
def _escena_repetida(d): d["escenas"].append(dict(buscar_escena(d, "E6")))
def _opcion_repetida(d): buscar_opcion(d, "E3", "activar_sin_verificar")["id"] = "cortar"
def _destino_inexistente(d): buscar_opcion(d, "E3", "activar_con_codigo")["destino"] = "E99"
def _variable_no_declarada_efecto(d): buscar_opcion(d, "E2", "investigar")["efectos"] = {"conoce_orgen": True}
def _variable_no_declarada_condicion(d): buscar_opcion(d, "E3", "activar_con_codigo")["condiciones"] = {"sabe": True}
def _no_booleano_condicion(d): buscar_opcion(d, "E3", "activar_con_codigo")["condiciones"]["conoce_origen"] = "si"
def _no_booleano_efecto(d): buscar_opcion(d, "E2", "investigar")["efectos"]["conoce_origen"] = 1
def _no_booleano_variable(d): d["variables"]["conoce_origen"] = "falso"
def _final_con_opciones(d): buscar_escena(d, "E4")["opciones"] = [dict(buscar_opcion(d, "E1", "revisar_senal"))]
def _no_final_sin_opciones(d): buscar_escena(d, "E1")["opciones"] = []


@pytest.mark.parametrize(
    "romper, codigo, texto_esperado",
    [
        (_quitar_titulo, "V02", "titulo"),
        (_quitar_destino, "V02", "destino"),
        (_escenas_no_es_lista, "V02", "escenas"),
        (_inicio_inexistente, "V03", "E0"),
        (_escena_repetida, "V04", "E6"),
        (_opcion_repetida, "V05", "cortar"),
        (_destino_inexistente, "V06", "E99"),
        (_variable_no_declarada_efecto, "V07", "conoce_orgen"),
        (_variable_no_declarada_condicion, "V07", "sabe"),
        (_no_booleano_condicion, "V08", "conoce_origen"),
        (_no_booleano_efecto, "V08", "conoce_origen"),
        (_no_booleano_variable, "V08", "conoce_origen"),
        (_final_con_opciones, "V09", "E4"),
        (_no_final_sin_opciones, "V09", "E1"),
    ],
    ids=lambda v: v.__name__.lstrip("_") if callable(v) else str(v),
)
def test_U4_error_de_contenido_produce_rechazo_controlado(datos_referencia, romper, codigo, texto_esperado):
    romper(datos_referencia)

    with pytest.raises(HistoriaInvalidaError) as info:
        construir_historia(datos_referencia)

    errores = info.value.errores
    assert any(e.codigo == codigo and texto_esperado in str(e) for e in errores), \
        f"Se esperaba {codigo} con '{texto_esperado}', se obtuvo: {[str(e) for e in errores]}"


@pytest.mark.parametrize("contenido", ['{"titulo": "Rota", ', "texto plano", ""], ids=["cortado", "texto", "vacio"])
def test_U4_V01_archivo_ilegible(tmp_path, contenido):
    archivo = tmp_path / "rota.json"
    archivo.write_text(contenido, encoding="utf-8")

    with pytest.raises(HistoriaInvalidaError) as info:
        cargar_historia(archivo)

    error = info.value.errores[0]
    assert error.codigo == "V01" and "rota.json" in str(error)


def test_U4_V01_raiz_no_es_objeto():
    errores = validar([1, 2, 3], "lista.json")
    assert [e.codigo for e in errores] == ["V01"]


def test_U4_V01_archivo_inexistente(tmp_path):
    with pytest.raises(HistoriaInvalidaError) as info:
        cargar_historia(tmp_path / "no_existe.json")
    assert info.value.errores[0].codigo == "V01"


def test_CA03_destino_E99_rechaza_la_carga_sin_sesion(tmp_path, datos_referencia):
    _destino_inexistente(datos_referencia)
    archivo = tmp_path / "copia_E99.json"
    archivo.write_text(json.dumps(datos_referencia, ensure_ascii=False), encoding="utf-8")

    historia = None
    with pytest.raises(HistoriaInvalidaError) as info:
        historia = cargar_historia(archivo)

    assert historia is None
    mensaje = str(info.value)
    for fragmento in ("V06", "E3", "activar_con_codigo", "E99"):
        assert fragmento in mensaje


def test_varios_errores_se_reportan_juntos(datos_referencia):
    """Supuesto P2: se reportan todos los errores en una sola validación."""
    _destino_inexistente(datos_referencia)
    _opcion_repetida(datos_referencia)
    _variable_no_declarada_efecto(datos_referencia)

    codigos = {e.codigo for e in validar(datos_referencia)}
    assert {"V05", "V06", "V07"} <= codigos


def test_historia_de_referencia_es_valida(datos_referencia):
    assert validar(datos_referencia) == []


def test_validar_no_modifica_los_datos(datos_referencia):
    """Decisión de responsabilidad profesional: el contenido es de solo lectura."""
    _destino_inexistente(datos_referencia)
    antes = json.dumps(datos_referencia, sort_keys=True)
    validar(datos_referencia)
    assert json.dumps(datos_referencia, sort_keys=True) == antes
