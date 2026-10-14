"""I1: lectura de un archivo real + motor + consola, hasta un final."""
import pytest

from conftest import HISTORIA_REFERENCIA, SEGUNDA_HISTORIA
from motor_historias.__main__ import main
from motor_historias.cargador import cargar_historia
from motor_historias.consola import InterfazConsola
from motor_historias.sesion import Sesion


def test_I1_archivo_real_y_motor_hasta_un_final():
    historia = cargar_historia(HISTORIA_REFERENCIA)
    sesion = Sesion(historia)

    assert historia.titulo == "La última transmisión"
    assert len(historia.escenas) == 6
    assert sesion.escena_actual.id == "E1"

    for id_opcion in ("revisar_senal", "investigar", "activar_con_codigo"):
        assert sesion.elegir(id_opcion).aceptada

    assert sesion.escena_actual.id == "E4"
    assert sesion.esta_en_final()

    # Extensión del cambio (RF17): deshacer desde el final regresa a E3 con los valores previos
    assert sesion.deshacer().aceptada
    assert sesion.escena_actual.id == "E3"
    assert sesion.estado == {"conoce_origen": True, "confia_en_la_voz": False}
    assert not sesion.deshacer().aceptada            # un solo nivel


def _jugar_por_consola(ruta, entradas):
    """Ejecuta la consola real con entradas simuladas y devuelve lo que imprimió."""
    entradas = iter(entradas)
    salida = []
    sesion = Sesion(cargar_historia(ruta))
    InterfazConsola(sesion, entrada=lambda _: next(entradas), salida=salida.append).ejecutar()
    return sesion, "\n".join(salida)


def test_I1_consola_con_entradas_invalidas_llega_al_final():
    # E1: "abc" y "9" son inválidas (RF09); luego 1, 1 (investigar), 1 (activar con código) -> E4
    sesion, texto = _jugar_por_consola(HISTORIA_REFERENCIA, ["abc", "9", "1", "1", "1", "s"])

    assert texto.count("Entrada no válida") == 2
    assert "FIN DE LA PARTIDA" in texto
    assert sesion.escena_actual.id == "E4"


def test_I1_consola_deshacer_desde_el_final():
    # 1,1,1 -> E4 ; d -> E3 ; 2 (cortar) -> E6 ; s
    sesion, texto = _jugar_por_consola(HISTORIA_REFERENCIA, ["1", "1", "1", "d", "2", "s"])

    assert "Última decisión deshecha." in texto
    assert sesion.escena_actual.id == "E6"


def test_comando_validar_reporta_errores(tmp_path, capsys):
    archivo = tmp_path / "mala.json"
    archivo.write_text('{"titulo": "x"}', encoding="utf-8")

    codigo_salida = main(["validar", str(archivo)])

    assert codigo_salida == 1
    assert "V02" in capsys.readouterr().out


def test_comando_validar_historia_correcta(capsys):
    assert main(["validar", str(HISTORIA_REFERENCIA)]) == 0
    assert "Historia válida" in capsys.readouterr().out


@pytest.mark.skipif(not SEGUNDA_HISTORIA.exists(), reason="Pendiente T24: data/segunda_historia.json")
def test_I2_segunda_historia_funciona_sin_cambiar_el_motor():
    """RF03 / RNF01: otra historia se juega con el mismo motor hasta un final."""
    historia = cargar_historia(SEGUNDA_HISTORIA)
    sesion = Sesion(historia)

    # Recorrido automático: siempre la primera opción habilitada, máximo 50 pasos
    for _ in range(50):
        if sesion.esta_en_final() or sesion.esta_bloqueada():
            break
        assert sesion.elegir(sesion.opciones_habilitadas()[0].id).aceptada

    assert sesion.esta_en_final()
    assert len(historia.escenas) >= 3
    assert any(o.condiciones for e in historia.escenas.values() for o in e.opciones), "Falta una condición"
    assert any(o.efectos for e in historia.escenas.values() for o in e.opciones), "Falta un efecto"
