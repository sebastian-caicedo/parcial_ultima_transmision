# 1. Fundamentos

## 1.1 Problema

Un colectivo de escritores va a presentar una ficción interactiva en un festival universitario. Los escritores no saben programar, pero quieren agregar escenas y cambiar decisiones sin depender de un desarrollador. Además, la historia necesita reglas: algunas opciones solo aparecen si el lector descubrió cierta información antes.

El problema es construir un **motor que interprete historias escritas en archivos de datos**. El motor debe mostrar en cada escena solo las opciones permitidas por lo que ha pasado, aplicar las consecuencias de cada elección y avisar con claridad cuando un archivo tiene errores, antes de que alguien lo juegue.

## 1.2 Actores

| Actor | Tipo | Qué necesita del sistema |
|---|---|---|
| Escritor (escritora principal) | Usuario principal | Crear y modificar historias editando un archivo, sin tocar el código, y saber qué corregir cuando el archivo tiene errores |
| Lector | Usuario principal | Leer la escena, ver solo las opciones válidas, elegir, reconocer el final y empezar otra partida |
| Diseñador de la experiencia | Interesado | Que las decisiones tengan consecuencias y que haya opciones condicionadas por la información obtenida |
| Coordinadora del festival | Interesada | Que el programa no se cierre inesperadamente y que los errores del contenido se detecten antes del evento |
| Sistema de archivos | Sistema externo | Fuente de los archivos de historia (solo lectura) |

## 1.3 Alcance

**Incluye (versión inicial):**
- Cargar una historia desde un archivo JSON y validarla antes de jugar.
- Mostrar la escena actual y solo las opciones cuyas condiciones se cumplen.
- Aplicar efectos sobre variables booleanas y avanzar al destino de la opción elegida.
- Rechazar entradas inválidas sin alterar la partida.
- Reconocer finales, detectar bloqueos (escena no final sin opciones habilitadas) y reiniciar.
- Funcionar con cualquier historia que cumpla el formato, sin cambios en el motor.

**No incluye:**
- Cuentas de usuario, base de datos, guardado entre ejecuciones, internet, editor visual, audio, imágenes ni lenguaje de expresiones.
- **Retroceso:** hay un conflicto entre la escritora, que quiere poder retroceder siempre, y el diseñador, que quiere decisiones irreversibles. Queda fuera de la versión inicial por acuerdo provisional, y la pregunta de aclaración se registra en Requerimientos.

## 1.4 Riesgos

| ID | Riesgo | Probabilidad / impacto | Mitigación |
|---|---|---|---|
| R1 | Los escritores editan el JSON a mano y pueden introducir errores (destinos inexistentes, IDs repetidos, variables mal escritas) que hagan fallar el programa en pleno festival | Alta / Alto | Validar el archivo completo **antes** de abrir la partida, cubriendo las nueve categorías de error con mensajes que indiquen la causa y el ID afectado. Cada categoría tiene un caso de prueba automatizado con un archivo inválido |
| R2 | Cambio de requisitos a mitad del desarrollo (la solicitud de cambio de la hora 6) que obligue a rehacer partes grandes del código | Alta (es seguro que llega) / Medio | Separar contenido, motor e interfaz para que un cambio quede localizado en una capa. Guardar la versión `v1.0-pre-cambio` antes de tocar nada y hacer análisis de impacto sobre requisitos, modelos y pruebas |

## 1.5 Priorización de atributos de calidad

| Prioridad | Atributo | Por qué | Quién lo pide |
|---|---|---|---|
| 1 | **Confiabilidad** | Si el programa se cae durante el festival, la experiencia fracasa. Además, el motor no debe aceptar una opción no habilitada aunque se envíe su ID directamente (CA02) | Coordinadora |
| 2 | **Modificabilidad del contenido** | Es la razón de existir del sistema: la escritora debe cambiar la historia sin pedir cambios al programa | Escritora |
| 3 | **Claridad de los errores** | Una validación que solo dice "error" no sirve a alguien que no programa. Debe decir qué falló y dónde | Coordinadora y escritora |
| 4 | Mantenibilidad del código | Facilita absorber la solicitud de cambio, pero es interna al equipo y no la pide el cliente | Equipo |
| 5 | Rendimiento | Baja prioridad: las historias son pequeñas (decenas de escenas) y no hay usuarios concurrentes | — |

Los tres primeros atributos son la base de los tres requisitos no funcionales medibles.

## 1.6 Decisión de responsabilidad profesional

**Decisión:** el motor trata los archivos de historia como **solo lectura**. Nunca los modifica, ni los "autocorrige", ni completa campos faltantes con valores inventados. Cuando encuentra un error, lo reporta y la corrección queda en manos del escritor.

**Por qué:** el contenido es obra del colectivo de escritores. Si el programa corrigiera en silencio, por ejemplo cambiando un destino inexistente por el primero disponible, alteraría la historia sin que el autor lo supiera y podría publicarse en el festival una versión que nadie escribió. Respetar la autoría significa que el software informa y el autor decide.

**Consecuencia:** la validación es más estricta y el escritor tiene que corregir antes de jugar. Lo compensamos con mensajes claros (atributo de calidad 3).

En la misma línea, el motor usa solo la biblioteca estándar de Python, y la única dependencia externa es `pytest` (licencia MIT), solo para pruebas. Eso evita que el producto del cliente dependa de terceros con licencias o mantenimiento inciertos. Además, el uso de herramientas de IA se declara en `IA.md`.

---

# 2. Proceso

## 2.1 Proceso elegido: incremental con Kanban

Desarrollamos en **incrementos pequeños y funcionales**. Cada uno deja algo ejecutable y probado:

1. cargador y validador
2. motor de reglas
3. interfaz de consola
4. cambio solicitado

El flujo de trabajo se gestiona con un **tablero Kanban** (Por hacer / En progreso / Hecho) en GitHub Projects, con un límite de 2 tareas en progreso a la vez.

## 2.2 Comparación con una alternativa: cascada

| Criterio | Cascada | Incremental + Kanban (elegido) |
|---|---|---|
| Momento del código ejecutable | Al final, después de terminar todo el análisis y diseño | Desde el primer incremento (aprox. hora 3) |
| Cambio de la hora 6 | Obliga a volver a fases ya "cerradas" | Entra como un incremento más, sobre una versión estable y etiquetada |
| Riesgo si se acaba el tiempo | Puede no haber nada ejecutable | Siempre hay una versión funcional para entregar |
| Ventaja que perdemos | Documentación completa antes de programar | Los modelos se ajustan a medida que se implementa, lo que exige mantener la coherencia de vocabulario |

**Por qué no Scrum:** sprints, ceremonias y roles no tienen sentido en una ventana de 12 horas con un equipo de dos personas. Kanban conserva lo útil (backlog priorizado, visibilidad del flujo, límite de trabajo en curso) sin esa carga.

## 2.3 Cómo se realizan las actividades del proceso en esta entrega

| Actividad | Cómo y cuándo | Evidencia |
|---|---|---|
| **Especificación** | RF y RNF a partir de N01–N06 y las voces del cliente, con criterios de aceptación, antes del primer incremento. Las dudas sin respuesta se registran como supuestos | Sección de Requerimientos; `docs/backlog.md` |
| **Desarrollo** | Un incremento por vez, cada uno con su tarea en el tablero y commits pequeños | Historial de Git; tablero |
| **Validación** | Pruebas automatizadas (pytest) en cada incremento; criterios CA01–CA03; recorrido manual de los tres finales | `tests/`; `evidencias/pruebas/` |
| **Evolución** | En la hora 6 se etiqueta `v1.0-pre-cambio`, se analiza el impacto de la solicitud, se ajusta el backlog y se implementa como nuevo incremento | Etiquetas de Git; análisis de impacto; matriz de trazabilidad |
