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
| 8 | Unidad 4 – Requerimientos | Redactó RF, RNF, errores V01–V09 y preguntas | Cruce con N01–N06 y CA01–CA03 |
| 9 | Unidad 5 – Modelado | | |
| 10 | Unidad 6 – Arquitectura | | |
| 11 | Unidad 7 – Implementación | | |
| 12 | Pruebas automatizadas | | |
| 13 | Solicitud de cambio | | |
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

### 5. Unidad 1 – Fundamentos (`docs/01_fundamentos_y_proceso.md`, sección 1)
- **Qué se pidió:** redactar problema, actores, alcance, dos riesgos con mitigación, priorización de atributos de calidad y una decisión de responsabilidad profesional con la información dada.
- **Qué entregó la IA:** borrador con actores separados en usuarios e interesados, retroceso fuera del alcance, riesgos R1 (errores en el contenido) y R2 (cambio en la hora 6), priorización confiabilidad > modificabilidad > claridad de errores, y la decisión de tratar los archivos de historia como solo lectura (autoría del contenido).
- **Qué se subió:** el documento en `docs/`.
- **Verificación:** contraste con las voces del cliente (sección 1 de la guía) y con los subcriterios de la rúbrica "Problema y calidad".

### 6. Unidad 4 – Requerimientos (`docs/02_requerimientos.md`)
- **Qué se pidió:** RF atómicos con criterio de aceptación para N01–N06, tres RNF medibles, tres preguntas con respuesta o supuesto.
- **Qué entregó la IA:** vocabulario común, 16 RF (RF01–RF16) con criterios que incluyen CA01, CA02 y CA03, tabla de errores V01–V09, trazabilidad necesidad → requisito, tres RNF (modificabilidad, claridad de errores, confiabilidad) con procedimiento y evidencia, y preguntas P1 (retroceso, con acuerdo provisional), P2 (errores múltiples) y P3 (escenas inalcanzables).
- **Qué se subió:** el documento en `docs/`. La sección 3.7 (revisión cruzada) la completa Javier sin IA.
- **Verificación:** cruce de cada necesidad N01–N06 con al menos un RF, comprobación de que CA01–CA03 aparecen literalmente en los criterios, y de que las nueve categorías de error de la sección 5 de la guía están en V01–V09.
