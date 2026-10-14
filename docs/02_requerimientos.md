# 3. Requerimientos

## 3.1 Vocabulario

Estos términos se usan igual en requisitos, diagramas y código.

| Término | Significado |
|---|---|
| **Historia** | Archivo JSON con título, escena de inicio, variables iniciales y escenas |
| **Escena** | Fragmento de texto con un `id`. Puede ser final (sin opciones) o no final (con al menos una opción) |
| **Opción** | Decisión disponible en una escena. Tiene destino, condiciones y efectos |
| **Condición** | Igualdad `variable = valor booleano` que debe cumplirse para habilitar una opción |
| **Efecto** | Asignación `variable = valor booleano` que se aplica al elegir una opción |
| **Estado** | Valores actuales de las variables durante una partida |
| **Sesión (partida)** | Recorrido de un lector: escena actual más estado |
| **Validador** | Componente que revisa la historia antes de abrir una sesión |
| **Opción habilitada** | Opción cuyas condiciones se cumplen todas con el estado actual. Un mapa de condiciones vacío siempre habilita |

## 3.2 Requisitos funcionales

### N01: historias en archivos independientes, con inicio y estado inicial

| ID | Requisito | Criterio de aceptación |
|---|---|---|
| RF01 | El sistema carga una historia desde la ruta de un archivo JSON indicada al ejecutar el programa | Dado `data/la_ultima_transmision.json`, la historia queda cargada con el título "La última transmisión" y 6 escenas |
| RF02 | Al iniciar una sesión, la escena actual es la indicada en `inicio` y el estado es igual al mapa `variables` del archivo | Dada una sesión nueva de la historia de referencia, la escena actual es E1, `conoce_origen = falso` y `confia_en_la_voz = falso` |
| RF03 | El motor ejecuta cualquier historia que cumpla el formato, sin modificar el código fuente | La segunda historia (`data/segunda_historia.json`) se juega hasta un final con el mismo comando, cambiando solo la ruta, y sin cambios en `src/` |

### N02: leer la escena y ver solo decisiones compatibles

| ID | Requisito | Criterio de aceptación |
|---|---|---|
| RF04 | El sistema muestra el texto de la escena actual | En una sesión nueva se muestra el texto de E1 |
| RF05 | El sistema muestra únicamente las opciones habilitadas de la escena actual | **CA01:** tras elegir "Revisar señal" e "Investigar archivo", en E3 se muestran exactamente "Activar con código" y "Cortar comunicación". Si en vez de investigar se elige "Continuar sin investigar", se muestran exactamente "Activar sin verificar" y "Cortar comunicación" |

### N03: elegir produce consecuencias y lleva al destino; los errores de entrada no alteran la partida

| ID | Requisito | Criterio de aceptación |
|---|---|---|
| RF06 | Al elegir una opción habilitada, el sistema aplica todos sus efectos al estado | En E2, elegir "Investigar archivo" deja `conoce_origen = verdadero` |
| RF07 | Al elegir una opción habilitada, la escena actual pasa a ser el destino de la opción | En E2, elegir "Investigar archivo" deja la escena actual en E3 |
| RF08 | El motor rechaza una opción inexistente o no habilitada, informa el motivo y deja intactos la escena y el estado | **CA02:** en E3 sin conocer el origen, enviar directamente al motor el id `activar_con_codigo` se rechaza; la escena sigue en E3 y las variables no cambian. Lo mismo ocurre con un id inexistente (`xyz`) |
| RF09 | La interfaz rechaza entradas que no correspondan a una opción mostrada (texto, vacío, número fuera de rango) y vuelve a pedir la elección sin terminar el programa | Escribir `abc`, dejar vacío o escribir `9` en una escena con 2 opciones muestra un aviso y vuelve a mostrar las mismas opciones |

### N04: recordar lo ocurrido durante la partida

| ID | Requisito | Criterio de aceptación |
|---|---|---|
| RF10 | El estado modificado por los efectos se conserva entre escenas durante toda la sesión, y las condiciones se evalúan siempre contra el estado actual | Con la ruta Revisar señal → Investigar archivo → (E3), la opción "Activar con código" está disponible porque se conserva `conoce_origen = verdadero` desde E2 |

### N05: reconocer el desenlace y volver a empezar sin información anterior

| ID | Requisito | Criterio de aceptación |
|---|---|---|
| RF11 | Al llegar a una escena final, el sistema muestra su texto, indica que la partida terminó y no ofrece opciones de avance | Al elegir "Cortar comunicación" se muestra E6 con la indicación de fin y sin opciones |
| RF12 | El sistema permite reiniciar la sesión, restaurando la escena de inicio y el estado inicial | Tras llegar a E4 (estado con ambas variables en verdadero), reiniciar deja la escena en E1 y ambas variables en falso |
| RF13 | Si en una escena no final ninguna opción queda habilitada, el sistema informa el bloqueo y ofrece reiniciar, sin cerrarse | Con una historia de prueba donde la única opción de una escena exige una variable que nunca es verdadera, al llegar a esa escena se muestra un mensaje de bloqueo y la opción de reiniciar |

### N06: saber por qué un archivo no es válido antes de jugarlo

| ID | Requisito | Criterio de aceptación |
|---|---|---|
| RF14 | El sistema valida la historia completa antes de abrir una sesión; si hay errores, no se abre ninguna sesión | **CA03:** con una copia de la historia donde una opción apunta a E99, la carga se rechaza y no se abre sesión jugable |
| RF15 | Cada error reportado indica su tipo, la causa y el campo o ID involucrado cuando sea identificable | En el caso de CA03, el mensaje incluye el tipo de error (destino inexistente), el id de la escena, el id de la opción y el valor `E99` |
| RF16 | El validador detecta las nueve categorías de error de la tabla 3.3 | Cada categoría tiene un archivo inválido en `tests/datos_invalidos/` que el validador rechaza con su código de error |

### 3.3 Categorías de error del validador (RF16)

| Código | Error | Ejemplo de mensaje esperado |
|---|---|---|
| V01 | Archivo ilegible o con estructura incorrecta (no es JSON, o la raíz no es un objeto) | `V01 Archivo ilegible: no es JSON válido (línea 4)` |
| V02 | Campo obligatorio ausente o de tipo incorrecto (en historia, escena u opción) | `V02 Falta el campo 'destino' en la opción 'investigar' de la escena 'E2'` |
| V03 | La escena de `inicio` no existe | `V03 La escena de inicio 'E0' no existe` |
| V04 | IDs de escena repetidos | `V04 El id de escena 'E3' está repetido` |
| V05 | IDs de opción repetidos dentro de la misma escena | `V05 El id de opción 'cortar' está repetido en la escena 'E3'` |
| V06 | Destino inexistente | `V06 La opción 'activar_con_codigo' de la escena 'E3' apunta a 'E99', que no existe` |
| V07 | Variable no declarada en condiciones o efectos | `V07 La variable 'conoce_orgen' usada en efectos de 'investigar' (E2) no está declarada` |
| V08 | Valor no booleano en `variables`, condiciones o efectos | `V08 La condición 'conoce_origen' de 'activar_con_codigo' (E3) tiene el valor "si", que no es booleano` |
| V09 | Cantidad de opciones incompatible con `final` (final con opciones, o no final sin opciones) | `V09 La escena 'E4' es final pero tiene 1 opción` |

### 3.4 Trazabilidad necesidad → requisito

| Necesidad | Requisitos |
|---|---|
| N01 | RF01, RF02, RF03 |
| N02 | RF04, RF05 |
| N03 | RF06, RF07, RF08, RF09 |
| N04 | RF10 |
| N05 | RF11, RF12, RF13 |
| N06 | RF14, RF15, RF16 |

## 3.5 Requisitos no funcionales

| ID | Atributo | Requisito medible | Procedimiento de verificación | Evidencia |
|---|---|---|---|---|
| RNF01 | Modificabilidad del contenido | Agregar o modificar una historia requiere **0 líneas cambiadas** en `src/`, y la historia nueva se juega hasta un final con el mismo comando | 1. Agregar `data/segunda_historia.json` en un commit propio. 2. Ejecutar `git show --stat <commit>` y comprobar que no aparece ningún archivo de `src/`. 3. Ejecutar la prueba de integración de la segunda historia | `evidencias/rnf/rnf01_diff.txt` y resultado de la prueba en `evidencias/pruebas/` |
| RNF02 | Claridad de los errores | El **100 %** de los 9 archivos inválidos de prueba (V01–V09) se rechaza con un mensaje que contiene (a) el código del error y (b) el ID o campo involucrado | Prueba parametrizada que carga cada archivo de `tests/datos_invalidos/` y verifica con aserciones que el mensaje contiene el código y el ID esperado. Se cuenta cuántos casos cumplen sobre 9 | `evidencias/rnf/rnf02_resultado.txt` (salida de pytest con 9/9) |
| RNF03 | Confiabilidad | Ante **1000 entradas inválidas generadas al azar** (semilla fija 2026: ids inexistentes, opciones no habilitadas, texto, números fuera de rango, vacíos), el sistema produce **0 excepciones no controladas** y el estado de la sesión queda **idéntico** al anterior en el 100 % de los casos | Prueba automatizada con `random.Random(2026)` que envía las 1000 entradas a la sesión y compara escena y estado antes y después de cada una | `evidencias/rnf/rnf03_resultado.txt` |

## 3.6 Preguntas de aclaración y supuestos

| # | Pregunta al cliente | Respuesta o supuesto registrado |
|---|---|---|
| P1 | La escritora quiere poder retroceder siempre y el diseñador quiere decisiones irreversibles. ¿El retroceso debe estar disponible siempre, solo en escenas que el escritor marque, o nunca? | **Sin respuesta durante la ventana. Acuerdo provisional:** la versión inicial no implementa retroceso; las decisiones son irreversibles dentro de una partida y el lector solo puede reiniciar (RF12). No se presupone la decisión final del cliente; el conflicto queda abierto para una versión posterior |
| P2 | Si un archivo tiene varios errores, ¿el escritor quiere ver solo el primero o todos? | **Supuesto:** se reportan todos los errores encontrados en una sola validación, porque al escritor le ahorra cargas repetidas. Excepción: si el archivo es ilegible o le falta la estructura base (V01, V02 en la raíz), se informa ese error y se detiene la validación, porque no se puede revisar lo demás |
| P3 | ¿Una escena a la que ninguna opción lleva (inalcanzable) debe tratarse como error? | **Supuesto:** no. La guía no exige analizar todos los caminos posibles, y una escena inalcanzable no rompe la partida. Queda fuera de alcance y se menciona como limitación conocida |

## 3.7 Revisión cruzada de requisitos

Revisión hecha por **Javier Alejandro Carta Lacharme** sobre los requisitos redactados por Sebastián.
Revisar en revision_cruzada.md
