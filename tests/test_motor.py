"""Pruebas unitarias del motor: U1, U2, U3, U5, finales y bloqueo."""
import pytest

from motor_historias.cargador import construir_historia
from motor_historias.sesion import Sesion


def textos(opciones):
    return sorted(o.texto for o in opciones)


# ---------- U1: condiciones habilitan solo las opciones correspondientes (RF05, CA01) ----------
@pytest.mark.parametrize(
    "eleccion_en_e2, esperadas",
    [
        ("investigar", ["Activar con código", "Cortar comunicación"]),            # CA01
        ("continuar", ["Activar sin verificar", "Cortar comunicación"]),
    ],
    ids=["conoce_origen_verdadero", "conoce_origen_falso"],
)
def test_U1_condiciones_habilitan_solo_opciones_correspondientes(sesion, eleccion_en_e2, esperadas):
    assert sesion.elegir("revisar_senal").aceptada
    assert sesion.elegir(eleccion_en_e2).aceptada

    assert sesion.escena_actual.id == "E3"
    assert len(sesion.opciones_habilitadas()) == 2
    assert textos(sesion.opciones_habilitadas()) == sorted(esperadas)


def test_U1_condiciones_vacias_siempre_habilitan(sesion):
    assert [o.id for o in sesion.opciones_habilitadas()] == ["revisar_senal"]


# ---------- U2: elección válida aplica efectos y avanza (RF06, RF07, RF10) ----------
def test_U2_eleccion_valida_aplica_efectos_y_avanza(sesion):
    sesion.elegir("revisar_senal")
    resultado = sesion.elegir("investigar")

    assert resultado.aceptada
    assert sesion.escena_actual.id == "E3"
    assert sesion.estado == {"conoce_origen": True, "confia_en_la_voz": False}


# ---------- U3: opción inexistente o no habilitada deja intacto el estado (RF08, CA02) ----------
@pytest.mark.parametrize(
    "entrada",
    ["activar_con_codigo", "xyz", "", None, 3, "ACTIVAR_SIN_VERIFICAR"],
    ids=["no_habilitada_CA02", "inexistente", "vacia", "none", "numero", "mayusculas"],
)
def test_U3_eleccion_invalida_deja_intacto_el_estado(sesion, entrada):
    sesion.elegir("revisar_senal")
    sesion.elegir("continuar")          # E3 sin conocer el origen
    escena_antes, estado_antes = sesion.escena_actual.id, sesion.estado

    resultado = sesion.elegir(entrada)

    assert not resultado.aceptada
    assert resultado.motivo
    assert sesion.escena_actual.id == escena_antes == "E3"
    assert sesion.estado == estado_antes


def test_U3_eleccion_en_escena_final_es_rechazada(sesion):
    for id_opcion in ("revisar_senal", "continuar", "cortar"):
        sesion.elegir(id_opcion)
    estado_antes = sesion.estado

    assert not sesion.elegir("cortar").aceptada
    assert sesion.escena_actual.id == "E6"
    assert sesion.estado == estado_antes


def test_CA02_activar_sin_verificar_lleva_a_E5(sesion):
    sesion.elegir("revisar_senal")
    sesion.elegir("continuar")
    assert sesion.elegir("activar_sin_verificar").aceptada
    assert sesion.escena_actual.id == "E5"


# ---------- U5: reiniciar restaura escena y variables iniciales (RF12) ----------
def test_U5_reiniciar_restaura_escena_y_variables(sesion):
    for id_opcion in ("revisar_senal", "investigar", "activar_con_codigo"):
        assert sesion.elegir(id_opcion).aceptada
    assert sesion.escena_actual.id == "E4"
    assert sesion.estado == {"conoce_origen": True, "confia_en_la_voz": True}

    sesion.reiniciar()

    assert sesion.escena_actual.id == "E1"
    assert sesion.estado == {"conoce_origen": False, "confia_en_la_voz": False}
    assert not sesion.esta_en_final()


# ---------- Finales (RF11) ----------
@pytest.mark.parametrize(
    "ruta, final_esperado",
    [
        (["revisar_senal", "investigar", "activar_con_codigo"], "E4"),
        (["revisar_senal", "continuar", "activar_sin_verificar"], "E5"),
        (["revisar_senal", "continuar", "cortar"], "E6"),
    ],
    ids=["rescate", "eco", "silencio"],
)
def test_los_tres_finales_son_alcanzables(sesion, ruta, final_esperado):
    for id_opcion in ruta:
        assert sesion.elegir(id_opcion).aceptada
    assert sesion.escena_actual.id == final_esperado
    assert sesion.esta_en_final()
    assert sesion.opciones_habilitadas() == []


# ---------- Bloqueo durante la partida (RF13) ----------
def test_escena_no_final_sin_opciones_habilitadas_se_reporta_bloqueada():
    datos = {
        "titulo": "Bloqueo", "inicio": "A", "variables": {"llave": False},
        "escenas": [
            {"id": "A", "texto": "Inicio", "final": False, "opciones": [
                {"id": "ir", "texto": "Ir", "destino": "B", "condiciones": {}, "efectos": {}}]},
            {"id": "B", "texto": "Puerta", "final": False, "opciones": [
                {"id": "abrir", "texto": "Abrir", "destino": "C",
                 "condiciones": {"llave": True}, "efectos": {}}]},
            {"id": "C", "texto": "Fin", "final": True, "opciones": []},
        ],
    }
    sesion = Sesion(construir_historia(datos))
    sesion.elegir("ir")

    assert sesion.esta_bloqueada()
    assert not sesion.esta_en_final()
    sesion.reiniciar()
    assert sesion.escena_actual.id == "A" and not sesion.esta_bloqueada()
