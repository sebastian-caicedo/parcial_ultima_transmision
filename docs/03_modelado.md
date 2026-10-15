# 4. Modelado

Los diagramas están en `docs/diagramas/`. Cada uno tiene su fuente PlantUML (`.puml`, versionable) y su imagen (`.png`, para el anexo). Usan el vocabulario de la sección 3.1 de Requerimientos y llevan anotados los RF que representan.

| # | Modelo | Archivo | Qué muestra | RF que cubre |
|---|---|---|---|---|
| 1 | Contexto | `01_contexto` | El motor como caja negra y sus intercambios con escritor, lector y sistema de archivos. Los interesados sin interacción directa van en nota | N01–N06 en general |
| 2 | Casos de uso | `02_casos_de_uso` | Nueve casos de uso. Iniciar partida *incluye* cargar historia, que *incluye* validar y el caso Deshacer última decisión. Reconocer final e informar bloqueo *extienden* elegir opción | RF01–RF20 (anotados en cada caso) |
| 3 | Clases del dominio | `03_clases` | Historia → Escena → Opción (composición), Sesión con escena actual y estado, ResultadoElección y ErrorContenido | RF02, RF05–RF08, RF10–RF13, RF15–RF20|
| 4 | Secuencia: elegir una opción | `04_secuencia_elegir` | Recorrido completo de una elección, con los tres caminos de rechazo (entrada inválida en la interfaz, opción inexistente y opción no habilitada en el motor) y la evaluación posterior de final o bloqueo | RF05–RF09, RF11, RF13, RF17, RF20 |
| 5 | Estados de una sesión | `05_estados_sesion` | EnCurso, Finalizada y Bloqueada, con una decisión que se evalúa al iniciar, tras cada elección aceptada y al reiniciar | RF02, RF08, RF11–RF13, RF17–RF19 |

## Decisiones de modelado

- **La validación ocurre antes de que exista la sesión.** Por eso el diagrama de estados empieza con "historia válida cargada": una historia inválida nunca llega a crear una sesión (RF14). Los errores se modelan como `ErrorContenido` agrupados en `HistoriaInvalidaError`.
- **El rechazo de una elección no es una excepción.** `elegir()` devuelve un `ResultadoEleccion` con `aceptada = falso` y el motivo. Así una entrada inválida nunca puede cerrar el programa (RNF03), y la interfaz decide cómo mostrar el aviso.
- **La regla de habilitación vive en `Opcion`** (`esta_habilitada(estado)`). Ni la sesión ni la interfaz conocen IDs concretos como E3 o `activar_codigo`, lo que cumple la exigencia de la guía de evaluar las condiciones desde los datos.
- **Hay dos niveles de validación de la elección**, visibles en la secuencia. La interfaz filtra lo que el lector escribe (RF09) y el motor vuelve a verificar el id recibido (RF08). El segundo control es el que cumple CA02, aunque alguien salte la interfaz.

## Actualización por la solicitud de cambio (hora 6)

Los diagramas 02 a 06 se actualizaron para incluir deshacer (RF17–RF20): caso de uso nuevo del Lector; `Sesion` con el atributo `anterior` y los métodos `deshacer()` y `puede_deshacer()`; en la secuencia, el guardado de `anterior` antes de aplicar efectos; y en los estados, las transiciones `deshacer()` desde EnCurso, Finalizada y Bloqueada. El detalle del impacto está en `docs/05_solicitud_cambio.md`.
