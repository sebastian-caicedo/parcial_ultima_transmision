# 7. Matriz de trazabilidad (versión final, `v2.0-post-cambio`)

Convenciones:
- Modelos: diagramas en `docs/diagramas/` (CU = casos de uso `02`, Cl = clases `03`, Sec = secuencia `04`, Est = estados `05`, Comp = componentes `06`).
- Código: todo en `src/motor_historias/`.
- Pruebas: archivos de `tests/`.

## Requisitos funcionales

| RF | Necesidad | Modelos | Componente / archivo | Evidencia de verificación |
|---|---|---|---|---|
| RF01 Cargar historia desde archivo | N01 | CU Cargar historia; Comp Cargador | `cargador.py` → `cargar_historia()` | `test_integracion.py::test_I1_archivo_real_y_motor_hasta_un_final` |
| RF02 Inicio y estado inicial | N01 | CU Iniciar partida; Cl Sesion; Est estado inicial | `sesion.py` → `Sesion.__init__`, `reiniciar()` | `test_I1_archivo_real_y_motor_hasta_un_final` (escena E1) |
| RF03 Otra historia sin cambiar el motor | N01 | Comp capa Contenido | `data/segunda_historia.json` | `test_integracion.py::test_I2_segunda_historia_funciona_sin_cambiar_el_motor`; `evidencias/rnf/rnf01_resultado.txt` |
| RF04 Mostrar texto de la escena | N02 | CU Leer escena; Sec pasos 1–3 | `consola.py` → `_turno()` | `test_I1_consola_con_entradas_invalidas_llega_al_final` |
| RF05 Solo opciones habilitadas | N02 | Cl `Opcion.esta_habilitada`; Sec pasos 1–2 | `modelo.py`, `sesion.py` → `opciones_habilitadas()` | `test_motor.py::test_U1_*` (CA01) |
| RF06 Aplicar efectos | N03 | CU Elegir opción; Sec paso de efectos | `sesion.py` → `elegir()` | `test_U2_eleccion_valida_aplica_efectos_y_avanza` |
| RF07 Avanzar al destino | N03 | Sec paso de destino; Est EnCurso → Evaluando | `sesion.py` → `elegir()` | `test_U2_*`, `test_los_tres_finales_son_alcanzables` |
| RF08 Rechazar opción inexistente o no habilitada | N03 | Sec alternativas de rechazo; Est autotransición EnCurso | `sesion.py` → `elegir()` | `test_U3_*` (CA02), `test_CA02_activar_sin_verificar_lleva_a_E5` |
| RF09 La interfaz rechaza entradas inválidas | N03 | Sec alternativa RF09; Comp Consola | `consola.py` → `_turno()` | `test_I1_consola_con_entradas_invalidas_llega_al_final` |
| RF10 Conservar el estado durante la partida | N04 | Cl `Sesion.estado` | `sesion.py` | `test_U1_*`, `test_U2_*` |
| RF11 Reconocer el final | N05 | CU Reconocer final; Est Finalizada | `sesion.py` → `esta_en_final()`; `consola.py` | `test_los_tres_finales_son_alcanzables` |
| RF12 Reiniciar | N05 | CU Reiniciar; Est reiniciar() | `sesion.py` → `reiniciar()` | `test_U5_reiniciar_restaura_escena_y_variables` |
| RF13 Informar bloqueo | N05 | CU Informar bloqueo; Est Bloqueada | `sesion.py` → `esta_bloqueada()`; `consola.py` | `test_escena_no_final_sin_opciones_habilitadas_se_reporta_bloqueada` |
| RF14 Validar antes de abrir sesión | N06 | CU Validar historia; Est inicio "historia válida" | `cargador.py` → `construir_historia()` | `test_validador.py::test_CA03_destino_E99_rechaza_la_carga_sin_sesion` |
| RF15 Mensaje con tipo, causa e ID | N06 | Cl `ErrorContenido` | `validador.py` | `test_CA03_*`; `test_rnf.py::test_RNF02_*` |
| RF16 Detectar V01–V09 | N06 | Comp Validador | `validador.py` → `validar()` | `test_U4_*` (14 + 5 variantes); `test_RNF02_estan_las_nueve_categorias` |
| RF17 Deshacer la última elección (cambio) | N07 | CU Deshacer; Cl `Sesion.deshacer`; Est deshacer(); Sec guardar anterior | `sesion.py` → `deshacer()`; `consola.py` comando `d` | `test_U6_deshacer_restaura_*`, `test_U6_deshacer_desde_un_final_vuelve_a_E3`, `test_U6_deshacer_desde_un_bloqueo`, `test_I1_consola_deshacer_desde_el_final` |
| RF18 Un solo nivel (cambio) | N07 | Est nota "sin anterior" | `sesion.py` → `deshacer()` vacía `_anterior` | `test_U6_deshacer_restaura_*` (segundo intento), `test_U6_nueva_eleccion_vuelve_a_habilitar_el_retroceso` |
| RF19 Sin retroceso al inicio; reiniciar borra historial (cambio) | N07 | Est inicio y reiniciar() | `sesion.py` → `__init__`, `reiniciar()` | `test_U6_al_comenzar_no_hay_retroceso`, `test_U5_*` (extendida) |
| RF20 Entrada inválida preserva el historial (cambio) | N07 | Sec notas RF20 | `sesion.py` → `elegir()` | `test_U6_entrada_invalida_preserva_el_historial` (4 variantes) |

## Requisitos no funcionales

| RNF | Modelos | Componente / archivo | Procedimiento | Evidencia |
|---|---|---|---|---|
| RNF01 Modificabilidad (0 líneas en `src/` al agregar historia) | Comp capa Contenido; ADR-01 | `data/` | `python scripts/verificar_rnf.py` (revisa el commit que agregó la segunda historia) | `evidencias/rnf/rnf01_resultado.txt` |
| RNF02 Claridad de errores (9/9 con código y causa, ID cuando sea identificable) | Cl `ErrorContenido`; ADR-02 | `validador.py`, `cargador.py` | `pytest tests/test_rnf.py -k RNF02` | `evidencias/rnf/rnf02_resultado.txt` |
| RNF03 Confiabilidad (1000 entradas, 0 fallos, estado idéntico) | Sec doble filtro | `sesion.py` → `elegir()` | `pytest tests/test_rnf.py -k RNF03` | `evidencias/rnf/rnf03_resultado.txt` |

## Criterios de aceptación de la guía

| Criterio | Prueba |
|---|---|
| CA01 | `test_U1_condiciones_habilitan_solo_opciones_correspondientes[conoce_origen_verdadero]` |
| CA02 | `test_U3_eleccion_invalida_deja_intacto_el_estado[no_habilitada_CA02]`, `test_CA02_activar_sin_verificar_lleva_a_E5` |
| CA03 | `test_CA03_destino_E99_rechaza_la_carga_sin_sesion` |
