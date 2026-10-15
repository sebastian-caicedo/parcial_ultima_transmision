# 5. Arquitectura

## 5.1 Diagrama de componentes por capas

Diagrama: `docs/diagramas/06_componentes.png` (fuente `06_componentes.puml`).

| Capa | Componente (archivo) | Responsabilidad | Depende de |
|---|---|---|---|
| Interfaz | Consola (`src/motor_historias/consola.py`) | Mostrar escena y opciones habilitadas, leer y filtrar la entrada del lector (RF09), mostrar final, bloqueo y errores de validación, Comando d para deshacer (RF17). Ofrece tres comandos: `jugar`, `validar` y `deshacer` | Carga, Motor |
| Motor (reglas) | Sesión (`sesion.py`) | Opciones habilitadas, elegir, aplicar efectos, avanzar al destino, detectar final y bloqueo, reiniciar, deshacer un nivel (RF02, RF05–RF13, RF17–RF20) | Modelo |
| Motor (reglas) | Modelo de dominio (`modelo.py`) | Historia, Escena, Opción (con la regla `esta_habilitada`), ResultadoElección, ErrorContenido | Nada |
| Carga y validación | Cargador (`cargador.py`) | Leer el archivo, pedir la validación y, si no hay errores, construir la Historia (RF01, RF14) | Validador, Modelo |
| Carga y validación | Validador (`validador.py`) | Detectar V01–V09 y generar mensajes con código, causa e ID (RF15, RF16) | Modelo |
| Contenido | `data/*.json` | Las historias. Las editan los escritores | — |

**Regla de dependencias:** las flechas van solo hacia abajo o hacia el modelo. El motor no importa nada de la interfaz ni de la carga, y no sabe que existen archivos. Por eso las pruebas pueden crear una sesión directamente, sin consola.

## 5.2 Separación entre contenido, reglas e interfaz

| Parte | Dónde vive | Qué pasa si cambia |
|---|---|---|
| **Contenido** (qué dice la historia, qué opciones hay, qué condiciones y efectos tienen) | Solo en `data/*.json` | Ningún archivo de `src/` cambia (RNF01) |
| **Reglas** (cómo se evalúa una condición, cómo se aplica un efecto, qué es un final o un bloqueo) | Solo en `modelo.py` y `sesion.py` | La consola y los JSON no cambian |
| **Interfaz** (cómo se muestra y cómo se elige) | Solo en `consola.py` | El motor y las pruebas del motor no cambian. Se podría cambiar a web sin tocar reglas |

**Cómo se demuestra:** la segunda historia (`data/segunda_historia.json`) se agrega en un commit que no toca `src/`, y se juega con el mismo comando cambiando solo la ruta. La evidencia es `evidencias/rnf/rnf01_diff.txt` y la prueba de integración de la segunda historia.

## 5.3 Decisiones de arquitectura

### ADR-01: Arquitectura en capas con el contenido como datos externos

- **Contexto:** la escritora necesita cambiar escenas y decisiones sin pedir cambios al programa (N01, atributo 2). La guía prohíbe decisiones de código específicas para E1, E2 u otros IDs. Además, en la hora 6 llega un cambio que no conocemos (riesgo R2).
- **Alternativas:**
  1. *Historia escrita en el código* (un `if` por escena). Es rápido para una sola historia, pero cada cambio de contenido exige programar, y viola la regla de la guía.
  2. *Un solo módulo* que lee el JSON, aplica reglas e imprime en consola. Tiene menos archivos, pero no se puede probar el motor sin la consola y cualquier cambio toca todo.
  3. *Capas separadas* (contenido, carga y validación, motor, interfaz) con dependencias en un solo sentido.
- **Elección:** alternativa 3.
- **Consecuencias:**
  - ✅ Una historia nueva no toca el código (RNF01).
  - ✅ El motor se prueba aislado (U1–U5).
  - ✅ El cambio de la hora 6 queda localizado en la capa que corresponda.
  - ❌ Hay más archivos y hay que mantener coherentes los nombres entre capas.

### ADR-02: Validar la historia completa antes de crear la sesión

- **Contexto:** la coordinadora no quiere cierres inesperados (atributo 1) y el escritor necesita saber qué corregir antes de que alguien juegue (N06).
- **Alternativas:**
  1. *Validación perezosa:* revisar cada escena u opción cuando el lector llega a ella. Arranca antes, pero un destino roto se descubre en plena partida y solo si alguien pasa por ahí.
  2. *Detenerse en el primer error:* es más simple, pero el escritor corrige un error, vuelve a cargar y encuentra el siguiente.
  3. *Validación completa previa:* el validador recorre todo el archivo, reporta todos los errores encontrados (supuesto P2) y solo si no hay ninguno se construye la historia y se permite crear una sesión.
- **Elección:** alternativa 3.
- **Consecuencias:**
- 
## 5.4 Validación de la arquitectura con el cambio

La solicitud de la hora 6 solo modificó `sesion.py` y `consola.py`. Modelo, cargador, validador y las historias JSON quedaron intactos, como anticipaba ADR-01 frente al riesgo R2. Se puede comprobar con `git diff v1.0-pre-cambio v2.0-post-cambio --stat -- src/`.
  - ✅ Una historia inválida nunca llega al lector (RF14, CA03).
  - ✅ El motor puede asumir datos válidos: no comprueba destinos ni variables en tiempo de juego, lo que lo simplifica.
  - ✅ El escritor ve todos sus errores de una vez.
  - ❌ Toda la historia se lee y valida al inicio. Con historias de decenas de escenas el costo es despreciable (rendimiento es prioridad 5).
  - ❌ Los errores de juego que no son de contenido (el bloqueo, RF13) siguen necesitando manejo en el motor.
