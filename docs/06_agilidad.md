# 2.4 Agilidad

## Backlog y tablero

- **Backlog:** `docs/backlog.md`, con 37 tareas (T01–T37), unidad, prioridad y responsable. Cada tarea es una issue del repositorio.
- **Tablero:** GitHub Projects con columnas *Todo*, *In Progress* y *Done*, y un responsable por tarjeta.
- **Evidencia de evolución:** captura inicial (`evidencias/tablero/tablero_inicial.jpg`) y captura final (`evidencias/tablero/tablero_final.png`). Las issues se cierran desde los commits con `closes #N`, así que cada tarjeta enlaza el commit que la terminó.
- **Cambios del backlog durante el parcial:**
  - T04 y T06 se reasignaron de Javier a Sebastián.
  - Se cerró una issue duplicada de T14 (#14).
  - Con la solicitud de la hora 6 se agregó **T37** (actualizar requisitos, alcance y casos de uso), y T26–T28 pasaron a prioridad inmediata.

## Prácticas ágiles aplicadas

| Práctica | Cómo se aplicó | Evidencia |
|---|---|---|
| **Kanban con límite de trabajo en curso** | Máximo 2 tareas *In Progress* por integrante. Una tarea solo pasa a *Done* si cumple la definición de terminado | Tablero, capturas inicial y final |
| **Integración continua local: pruebas automatizadas en cada incremento y commits pequeños vinculados a tareas** | Antes de cada push se ejecuta `python -m pytest`. Cada commit lleva el ID de la tarea (T19–T22, T26–T27…) y, cuando aplica, `closes #N` | `evidencias/pruebas/resultado_v1.txt`, `resultado_v2.txt`; historial de Git |

**Por qué estas dos:** el trabajo es asincrónico y en pareja con disponibilidad desigual. El tablero permite ver qué falta sin reunirse, y las pruebas en cada incremento permitieron recibir el cambio de la hora 6 sobre una versión estable y etiquetada (`v1.0-pre-cambio`).

## Alternativa descartada: programación en pareja

Exige que los dos integrantes trabajen al mismo tiempo sobre el mismo código. En este parcial, 100 % virtual y asincrónico, con horarios distintos, habría bloqueado el avance. Se reemplazó por la **revisión cruzada asíncrona** de requisitos (`docs/revision_cruzada.md`), que sí permitió detectar un defecto real en RNF02.

## Definición de terminado

Una tarea está terminada cuando:
1. Su resultado está en el repositorio (commit en `main`).
2. Si es código, `python -m pytest` pasa completo y no rompe pruebas existentes.
3. Si es un artefacto del informe, usa el vocabulario de la sección 3.1 (escena, opción, condición, efecto, estado, sesión).
4. La tarjeta está en *Done*.
5. Si se usó IA, quedó registrada en `IA.md`.

## Aprendizaje y acción de mejora

- **Aprendizaje:** al inicio se perdió cerca de una hora intentando crear el tablero con scripts que no funcionaban en Windows. Además, varios commits hechos desde la web de GitHub quedaron sin ID de tarea ("Add files via upload", "Diagramas"), lo que dificulta relacionar el historial con el tablero.
- **Acción de mejora:** en el próximo proyecto, (1) verificar en la preparación las herramientas en el sistema operativo real de ambos integrantes antes de automatizar, y (2) acordar desde el primer commit la convención `Txx: descripción (closes #N)` y no subir archivos por la web sin editar el mensaje.
