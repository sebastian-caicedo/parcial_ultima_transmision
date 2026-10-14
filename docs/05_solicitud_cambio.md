# 6. Gestión del cambio (hora 6)

Documento recibido: `docs/solicitud_cambio_hora6.pdf` ("Solicitud de cambio del parcial").

## 6.1 Versión de partida

| Versión | Etiqueta Git | Contenido |
|---|---|---|
| Anterior al cambio | `v1.0-pre-cambio` | Requisitos RF01–RF16, modelos 01–06, motor, validador, consola y pruebas U1–U5, I1 (45 aprobadas, 3 pendientes de T23/T24) |
| Posterior al cambio | `v2.0-post-cambio` | Lo anterior + deshacer (RF17–RF20), modelos actualizados y pruebas U6, U5 e I1 extendidas |

## 6.2 Qué pide el cliente

El lector debe poder **deshacer su última decisión**, revirtiendo todas sus consecuencias. Esto **reemplaza el acuerdo provisional P1**, que era no implementar retroceso. Reglas: restauración exacta, un solo nivel, sin retroceso al comenzar ni tras reiniciar, la entrada inválida no altera el historial, y se puede deshacer desde un final.

## 6.3 Nuevos requisitos (necesidad N07: deshacer la última decisión)

| ID | Requisito | Criterio de aceptación |
|---|---|---|
| RF17 | El lector puede deshacer la última elección válida; la sesión vuelve exactamente a la escena y a todas las variables que tenía antes de esa elección, incluso desde una escena final o bloqueada | Desde E2, "Investigar archivo" lleva a E3 con `conoce_origen = verdadero`; deshacer deja la escena en E2 con `conoce_origen = falso`. Desde E4, E5 o E6, deshacer regresa a E3 con los valores previos a esa elección |
| RF18 | El retroceso tiene un solo nivel: después de deshacer, no se permite otro retroceso hasta una nueva elección válida. No se exige rehacer | Tras deshacer en E2, un segundo intento se rechaza con un aviso y no cambia escena ni variables. Al elegir "Continuar sin investigar", E3 muestra "Activar sin verificar" y "Cortar comunicación", y deshacer vuelve a estar disponible |
| RF19 | Al comenzar una sesión no hay retroceso disponible, y reiniciar elimina el historial además de restaurar el estado inicial | En una sesión nueva, deshacer se rechaza. Tras llegar a E4 y reiniciar, deshacer se rechaza y la escena sigue en E1 |
| RF20 | Una opción inexistente o no habilitada no modifica la sesión ni reemplaza el punto de retroceso de la última elección válida | En E3 tras investigar, enviar `activar_sin_verificar` o `xyz` se rechaza; luego deshacer regresa a E2 (deshace "investigar", no la entrada inválida) |

## 6.4 Análisis de impacto

| Artefacto | ¿Cambia? | Qué cambió | Archivo |
|---|---|---|---|
| Alcance (1.3) | Sí | El retroceso sale de "No incluye" | `docs/01_fundamentos_y_procesos.md` |
| Requisitos | Sí | Nueva N07 con RF17–RF20; P1 pasa de "supuesto" a "respondida"; RF12 y RF08 se relacionan con RF19 y RF20 | `docs/02_requerimientos.md` |
| RNF | No | RNF03 sigue cubriendo entradas inválidas; RNF01 y RNF02 no se ven afectados | — |
| Contexto | No | El lector sigue interactuando con el mismo sistema | `01_contexto` |
| Casos de uso | Sí | Nuevo caso "Deshacer última decisión" del Lector | `02_casos_de_uso` |
| Clases | Sí | `Sesion`: atributo `anterior`, métodos `deshacer()` y `puede_deshacer()` | `03_clases` |
| Secuencia | Sí | Al aceptar una elección se guarda `anterior` antes de aplicar efectos; los rechazos no lo tocan | `04_secuencia_elegir` |
| Estados | Sí | Transiciones `deshacer()` desde EnCurso, Finalizada y Bloqueada; reiniciar borra el historial | `05_estados_sesion` |
| Componentes | Sí (menor) | La consola ofrece `d`; la sesión atiende RF17–RF20 | `06_componentes` |
| Motor | Sí | `sesion.py`: `deshacer()`, `puede_deshacer()`; `elegir()` y `reiniciar()` gestionan `anterior` | `src/motor_historias/sesion.py` |
| Interfaz | Sí | Comando `d` en la partida y en el menú de final o bloqueo, visible solo si hay retroceso | `src/motor_historias/consola.py` |
| Modelo, cargador, validador | **No** | El formato de las historias no cambia | — |
| Historias JSON | **No** | Ninguna historia necesita editarse | `data/` |
| Pruebas | Sí | Nueva U6 (con variantes); U5 e I1 extendidas | `tests/test_motor.py`, `tests/test_integracion.py` |
| Backlog y trazabilidad | Sí | T26–T28 y matriz con RF17–RF20 | `docs/backlog.md`, matriz |

**Lectura del impacto:** el cambio quedó **contenido en la capa de motor** (`sesion.py`) y en la interfaz (`consola.py`). El modelo, la carga, la validación y los datos no se tocaron. Esto es lo que buscaba ADR-01 (riesgo R2).

## 6.5 Decisión de diseño

- **Alternativas:**
  1. Pila con todas las elecciones (historial completo).
  2. Guardar las elecciones y "re-jugar" desde el inicio menos la última.
  3. Guardar **una sola copia** de escena y estado antes de cada elección válida.
- **Elección:** alternativa 3. El cliente pidió un solo nivel. La pila agregaba complejidad que no se usa, y re-jugar depende de que los efectos sean deterministas y es más costoso de probar.
- **Consecuencias:**
  - ✅ La implementación es mínima: un atributo y dos métodos.
  - ✅ La regla "un solo nivel" se cumple por construcción, porque al deshacer la copia se vacía.
  - ❌ Si en el futuro se piden varios niveles, habrá que cambiar la copia por una pila. El cambio quedaría solo dentro de `Sesion`.

## 6.6 Evidencia de funcionamiento

| Regla del anexo | Prueba |
|---|---|
| Restauración + un solo nivel + ejemplo del anexo | `test_U6_deshacer_restaura_escena_y_variables_y_consume_el_retroceso` |
| Entrada inválida preserva el historial (variantes) | `test_U6_entrada_invalida_preserva_el_historial` (4 variantes) |
| Nueva elección vuelve a habilitar el retroceso | `test_U6_nueva_eleccion_vuelve_a_habilitar_el_retroceso` |
| Al comenzar no hay retroceso | `test_U6_al_comenzar_no_hay_retroceso` |
| Desde un final regresa a E3 | `test_U6_deshacer_desde_un_final_vuelve_a_E3` (E4, E5, E6) |
| Reiniciar elimina el historial (U5 extendida) | `test_U5_reiniciar_restaura_escena_y_variables` |
| Deshacer desde un final tras cargar el archivo (I1 extendida) | `test_I1_archivo_real_y_motor_hasta_un_final`, `test_I1_consola_deshacer_desde_el_final` |

Resultado de la ejecución: `evidencias/pruebas/resultado_v2.txt`.
