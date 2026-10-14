# Uso de herramientas de IA

La guía del parcial pide identificar las herramientas de IA utilizadas, para qué sirvieron y cómo se verificaron sus resultados. Este archivo registra ese uso punto por punto y se actualiza cada vez que la IA interviene en un artefacto.

**Herramienta:** Claude (Anthropic), modelo Claude Opus 5.5, usado desde claude.ai.
**Responsables del registro:** Sebastián Felipe Caicedo Acosta y Javier Alejandro Carta Lacharme.

## Criterio general

- La IA propone y nosotros decidimos. Ningún resultado se incluye sin leerlo, ejecutarlo o contrastarlo con la guía del parcial.
- El código sugerido solo se acepta si pasa las pruebas automatizadas y al menos un integrante puede explicarlo.
- Los textos del informe se revisan contra la rúbrica y se reescriben en nuestras palabras cuando hace falta.

## Registro por punto

| # | Unidad / artefacto | Uso de la IA | Verificación |
|---|---|---|---|
| 1 | Preparación del repositorio | Propuso estructura de carpetas y plantillas | Contraste con la sección 6 de la guía |
| 2 | Historia de referencia (JSON) | Transcribió las tablas de la guía a JSON | Comparación escena por escena con la guía |
| 3 | Backlog y división del trabajo | Propuso backlog de 36 tareas y reparto | Cada actividad de la sección 4 tiene tarea |
| 4 | Tablero | Generó scripts para crearlo; fallaron | Tablero hecho a mano; scripts descartados |
| 5 | Unidad 1 – Fundamentos | Redactó borrador de problema, riesgos y calidad | Revisión contra rúbrica y voces del cliente |
  | 6 | Unidad 2 – Procesos | Redactó comparación incremental vs. cascada | Revisión contra la sección 4 de la guía |
| 7 | Unidad 3 – Agilidad | | |
| 8 | Unidad 4 – Requerimientos | Redactó RF, RNF, errores V01–V09 y preguntas; revisión cruzada asistida con ChatGPT (Javier) | Cruce con N01–N06 y CA01–CA03; defecto de RNF02 contrastado con RF15 y V01 |
| 9 | Unidad 5 – Modelado | Generó diagramas de clases, secuencia y estados en PlantUML y su explicación | Nombres iguales al vocabulario de requisitos; RF anotados en cada diagrama |
| 10 | Unidad 6 – Arquitectura | Generó diagrama de capas y dos ADR con alternativas | Dependencias en un solo sentido; nombres de archivo iguales al código |
| 11 | Unidad 7 – Implementación | Generó motor, validador, consola y pruebas siguiendo los diagramas 03 y 06 | Ejecución de pytest (45 pasan); juego manual de los tres finales |
| 12 | Pruebas automatizadas | | |
| 13 | Solicitud de cambio | Implementó deshacer en la sesión y la consola, pruebas U6 y análisis de impacto | 57 pruebas pasan; recorrido manual deshaciendo desde un final |
| 14 | README e informe | | |

---

## Detalle por punto

### 1. Preparación del repositorio
- **Qué se pidió:** leer la guía del parcial y preparar lo necesario para empezar: estructura del repositorio, archivos base y forma de trabajo, junto a explicación y archivos a verificar.
- **Qué entregó la IA:** estructura de carpetas (`data/`, `src/`, `tests/`, `docs/`, `evidencias/`, `scripts/`), `.gitignore`, `requirements.txt` (pytest), plantilla de `README.md` con las secciones que exige la guía, este `IA.md` y una prueba de humo `tests/test_humo.py`.
- **Qué se subió:** todo lo anterior en el commit inicial (T01). Después modificamos `IA.md` (simplificamos la tabla y quitamos una sección), `docs/plan_trabajo.md` y `docs/backlog.md`.
- **Verificación:** contraste de la estructura con la lista de la sección 6 de la guía (informe, código, datos, pruebas, evidencias) y ejecución de `python -m pytest` (1 prueba aprobada).

### 2. Historia de referencia `data/la_ultima_transmision.json`
- **Qué se pidió:** el profesor no entregó el archivo JSON, así que se pidió construirlo a partir de las tablas de la sección 2 (escenas y reglas) usando el contrato de la sección 3.
- **Qué entregó la IA:** archivo con 6 escenas, inicio en E1, dos variables en falso y las 6 opciones con sus condiciones y efectos.
- **Qué se subió:** el archivo en `data/`.
- **Verificación:** comparación opción por opción (origen, destino, condición, efectos) contra la tabla de la guía. Se registra como supuesto en el informe que el archivo no fue entregado y se construyó desde la guía.

### 3. Backlog y división del trabajo
- **Qué se pidió:** organizar el trabajo y repartirlo de forma que un integrante tuviera tareas más acotadas.
- **Qué entregó la IA:** `docs/backlog.md` (36 tareas con unidad, prioridad y responsable) y `docs/plan_trabajo.md` (tareas por fase y borrador de definición de terminado).
- **Qué se subió:** ambos archivos con ajustes nuestros. T04 y T06 se reasignaron a Sebastián.
- **Verificación:** revisión de que cada actividad de la tabla de la sección 4 de la guía tuviera al menos una tarea.

### 4. Tablero
- **Qué se pidió:** se pidió ayuda con la creacion del tablero.
- **Qué entregó la IA:** scripts `crear_tablero.sh` y `crear_tablero.ps1` que crean etiquetas, issues y el tablero.
- **Qué se subió:** Se creó el tablero manualmente; solo quedaron las etiquetas que el script alcanzó a crear.
- **Verificación:** revisión visual del tablero (tareas, responsables y estados) y captura inicial en `evidencias/tablero/`.

### 5. Unidad 1 – Fundamentos (`docs/01_fundamentos_y_procesos.md`, sección 1)
- **Qué se pidió:** redactar problema, actores, alcance, dos riesgos con mitigación, priorización de atributos de calidad y una decisión de responsabilidad profesional con la información dada.
- **Qué entregó la IA:** borrador con actores separados en usuarios e interesados, retroceso fuera del alcance, riesgos R1 (errores en el contenido) y R2 (cambio en la hora 6), priorización confiabilidad > modificabilidad > claridad de errores, y la decisión de tratar los archivos de historia como solo lectura (autoría del contenido).
- **Qué se subió:** el documento en `docs/`.
- **Verificación:** contraste con las voces del cliente (sección 1 de la guía) y con los subcriterios de la rúbrica "Problema y calidad".

### 6. Unidad 4 – Requerimientos (`docs/02_requerimientos.md`)
- **Qué se pidió:** RF atómicos con criterio de aceptación para N01–N06, tres RNF medibles, tres preguntas con respuesta o supuesto.
- **Qué entregó la IA:** vocabulario común, 16 RF (RF01–RF16) con criterios que incluyen CA01, CA02 y CA03, tabla de errores V01–V09, trazabilidad necesidad → requisito, tres RNF (modificabilidad, claridad de errores, confiabilidad) con procedimiento y evidencia, y preguntas P1 (retroceso, con acuerdo provisional), P2 (errores múltiples) y P3 (escenas inalcanzables).
- **Qué se subió:** el documento en docs/. La sección 3.7 resume la revisión cruzada de Javier; el detalle está en docs/revision_cruzada.md.
- **Verificación:** cruce de cada necesidad N01–N06 con al menos un RF, comprobación de que CA01–CA03 aparecen literalmente en los criterios, y de que las nueve categorías de error de la sección 5 de la guía están en V01–V09.

### 7. Revisión cruzada de requisitos – Javier (`docs/revision_cruzada.md`)
- **Herramienta:** ChatGPT (OpenAI).
- **Qué se pidió:** contrastar los requisitos de `docs/02_requerimientos.md` para encontrar una ambigüedad o defecto y redactar la observación.
- **Qué entregó la IA:** apoyo para detectar una inconsistencia entre RF15 (pide el ID o campo "cuando sea identificable") y RNF02 (lo exigía en el 100 % de los casos, incluido V01, donde un archivo ilegible no tiene ID recuperable), y redacción de la corrección propuesta.
- **Qué se subió:** `docs/revision_cruzada.md` (commit de Javier). La corrección se aplicó en la fila RNF02 y en la sección 3.7 de `docs/02_requerimientos.md`.
- **Verificación:** se comprobó contra el texto de RF15, el ejemplo de mensaje de V01 en la tabla 3.3 y el criterio de RNF02 que la contradicción existía; se aceptó la corrección y se ajustó el procedimiento de verificación de RNF02 para exigir el nombre del archivo en V01.
  
### 9. Unidad 5 – Modelado: clases, secuencia y estados – Sebastián (`docs/03_modelado.md`, `docs/diagramas/03_*`, `04_*`, `05_*`)
- **Herramienta:** Claude (Anthropic).
- **Qué se pidió:** los diagramas de clases del dominio, secuencia de elegir una opción y estados de una sesión, pequeños y legibles, coherentes con los requisitos.
- **Qué entregó la IA:** fuentes PlantUML (`.puml`) y sus imágenes (`.png`) de los tres diagramas, más `docs/03_modelado.md` con la tabla de modelos, los RF que cubre cada uno y cuatro decisiones de modelado: validación antes de crear la sesión, rechazo de elecciones sin excepciones (`ResultadoEleccion`), regla de habilitación dentro de `Opcion` y doble filtro de la elección (interfaz y motor).
- **Qué se subió:** los seis archivos en `docs/diagramas/` y `docs/03_modelado.md`.
- **Verificación:** revisión de que las clases y mensajes usen los términos de la sección 3.1 de requisitos (historia, escena, opción, condición, efecto, estado, sesión); que cada RF anotado exista en `docs/02_requerimientos.md`; que la secuencia incluya el rechazo de CA02 (opción no habilitada enviada directamente al motor); y que los estados incluyan final (RF11), bloqueo (RF13) y reinicio (RF12). Las imágenes se regeneraron desde los `.puml` para confirmar que el texto fuente y la imagen coinciden.

### 10. Unidad 6 – Arquitectura – Sebastián (`docs/04_arquitectura.md`, `docs/diagramas/06_componentes.*`)
- **Herramienta:** Claude (Anthropic).
- **Qué se pidió:** diagrama de componentes o capas con responsabilidades y relaciones, dos decisiones de arquitectura con contexto, alternativas, elección y consecuencias, y la justificación de la separación entre contenido, reglas e interfaz.
- **Qué entregó la IA:** diagrama PlantUML de cuatro capas (interfaz, motor, carga y validación, contenido), tabla de responsabilidades por archivo, tabla de separación, ADR-01 (capas con contenido como datos) y ADR-02 (validación completa antes de crear la sesión).
- **Qué se subió:** `docs/04_arquitectura.md` y `docs/diagramas/06_componentes.puml` / `.png`.
- **Verificación:** se comprobó que cada componente del diagrama corresponda a una clase del diagrama de clases (03) y a los RF que atiende, que ninguna flecha vaya del motor hacia la interfaz o la carga, y que las alternativas de cada ADR sean opciones reales para este caso. La separación se verificará con la segunda historia (RNF01).

### 11. Unidad 7 – Implementación v1 – Sebastián (`src/`, `main.py`, `tests/`)
- **Herramienta:** Claude (Anthropic).
- **Qué se pidió:** implementar el motor según los requisitos y los diagramas de clases y capas, con las pruebas U1–U5 e I1.
- **Qué entregó la IA:** `modelo.py`, `sesion.py`, `validador.py`, `cargador.py`, `consola.py`, `__main__.py`, `main.py`, `pytest.ini` y cuatro archivos de pruebas (U1–U5, I1, CA01–CA03, RNF02, RNF03).
- **Qué se subió:** todo lo anterior; se eliminó `tests/test_humo.py`.
- **Verificación:** ejecución local de `python -m pytest` (resultado en `evidencias/pruebas/resultado_v1.txt`); recorrido manual de los tres finales con `python main.py jugar`; búsqueda de IDs de escena en `src/` para confirmar que no hay reglas específicas de la historia.

### 13. Solicitud de cambio (hora 6) – Sebastián (`docs/05_solicitud_cambio.md`, `sesion.py`, `consola.py`, pruebas)
- **Herramienta:** Claude (Anthropic).
- **Qué se pidió:** leer el anexo de la hora 6 e implementar el cambio con su análisis de impacto, requisitos, modelos y pruebas.
- **Qué entregó la IA:** `deshacer()` y `puede_deshacer()` en `Sesion`, comando `d` en la consola, prueba U6 con variantes, U5 e I1 extendidas, diagramas 03–06 actualizados y el documento de impacto con RF17–RF20.
- **Qué se subió:** todo lo anterior, después de etiquetar `v1.0-pre-cambio`.
- **Verificación:** se confirmó contra cada regla del anexo (tabla 6.6 del documento) que exista una prueba; ejecución de `python -m pytest` (57 aprobadas, en `evidencias/pruebas/resultado_v2.txt`); juego manual deshaciendo desde E5 y comprobando que el segundo deshacer se rechaza; `git diff v1.0-pre-cambio -- src/motor_historias/modelo.py src/motor_historias/validador.py src/motor_historias/cargador.py` vacío.
