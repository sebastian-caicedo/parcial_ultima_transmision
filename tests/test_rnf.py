"""Verificación automatizada de RNF02 y RNF03 (docs/02_requerimientos.md, sección 3.5)."""
import random
import re

import pytest

from conftest import DATOS_INVALIDOS
from motor_historias.cargador import cargar_historia
from motor_historias.modelo import HistoriaInvalidaError

# Archivos de tests/datos_invalidos/ con el formato V0N__<texto_esperado>.json (T23)
ARCHIVOS = sorted(DATOS_INVALIDOS.glob("V0[1-9]__*.json"))


@pytest.mark.skipif(not ARCHIVOS, reason="Pendiente T23: archivos en tests/datos_invalidos/")
@pytest.mark.parametrize("archivo", ARCHIVOS, ids=lambda a: a.stem)
def test_RNF02_cada_archivo_invalido_tiene_codigo_e_identificador(archivo):
    codigo, esperado = re.match(r"(V0\d)__(.+)", archivo.stem).groups()
    if codigo == "V01":
        esperado = archivo.name      # sin ID recuperable: se exige el nombre del archivo

    with pytest.raises(HistoriaInvalidaError) as info:
        cargar_historia(archivo)

    assert any(e.codigo == codigo and esperado in str(e) for e in info.value.errores), \
        f"{archivo.name}: se esperaba {codigo} con '{esperado}', se obtuvo {[str(e) for e in info.value.errores]}"


@pytest.mark.skipif(not ARCHIVOS, reason="Pendiente T23: archivos en tests/datos_invalidos/")
def test_RNF02_estan_las_nueve_categorias():
    codigos = {a.stem[:3] for a in ARCHIVOS}
    assert codigos == {f"V0{i}" for i in range(1, 10)}, f"Faltan: {sorted({f'V0{i}' for i in range(1, 10)} - codigos)}"


def test_RNF03_1000_entradas_invalidas_sin_fallos_ni_cambios(sesion):
    """1000 entradas aleatorias (semilla 2026): 0 excepciones y estado idéntico tras cada rechazo."""
    azar = random.Random(2026)
    sesion.elegir("revisar_senal")
    sesion.elegir("continuar")                    # E3 sin conocer el origen
    generadores = [
        lambda: "activar_con_codigo",             # existe pero no habilitada
        lambda: "".join(azar.choices("abcxyz_0123", k=azar.randint(0, 12))),
        lambda: str(azar.randint(-100, 100)),
        lambda: azar.randint(-100, 100),
        lambda: None,
        lambda: "",
        lambda: azar.choice(["E1", "E2", "E4", "revisar_senal", "investigar"]),
    ]
    rechazos = 0
    for _ in range(1000):
        entrada = azar.choice(generadores)()
        antes = (sesion.escena_actual.id, sesion.estado)
        resultado = sesion.elegir(entrada)        # cualquier excepción hace fallar la prueba
        assert not resultado.aceptada
        assert (sesion.escena_actual.id, sesion.estado) == antes
        rechazos += 1
    assert rechazos == 1000
