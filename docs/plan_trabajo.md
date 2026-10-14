# Plan de trabajo y división de tareas

**Integrantes**
- **SC**: Sebastián Felipe Caicedo Acosta
- **JC**: Javier Alejandro Carta Lacharme

## Criterio de reparto

SC asume las tareas de mayor carga técnica: motor, validador, pruebas, requisitos, arquitectura y cambio.

JC asume tareas acotadas, de verificación o de contenido. Cada una tiene una entrada clara, un resultado concreto y se puede hacer en 20 a 40 minutos.

## Tareas por fase

| Fase | SC (Sebastián) | JC (Javier) |
|---|---|---|
| 0. Preparación | Crear repo, subir estructura, crear tablero y backlog | Aceptar invitación al repo, clonar, ejecutar `pytest` vacío; tomar **captura inicial del tablero** |
| 1. Fundamentos y proceso | Problema, actores, alcance; priorización de calidad; proceso y alternativa | **Dos riesgos con mitigación**; **decisión de responsabilidad profesional** (datos/autoría/dependencias) |
| 2. Requerimientos | RF atómicos con criterio de aceptación (N01–N06); 3 RNF medibles; preguntas/supuestos | **Revisión cruzada de los RF**: buscar una ambigüedad o defecto y registrarlo con su corrección |
| 3. Modelado y arquitectura | Clases, secuencia, estados; diagrama de capas; 2 decisiones de arquitectura | **Diagrama de contexto** y **casos de uso** (a partir de una plantilla PlantUML que se le entrega) |
| 4. Implementación v1 | Cargador, validador, motor, consola; pruebas U1–U5 e I1 | **Segunda historia** (≥3 escenas, 1 condición, 1 efecto); **archivos JSON inválidos** para cada error de validación (copiar el válido y romper una cosa) |
| Hora 6 | `git tag v1.0-pre-cambio`; análisis de impacto | Descargar y guardar la solicitud de cambio en `docs/` |
| 5. Cambio | Implementar el cambio + prueba U6; actualizar trazabilidad | Actualizar el backlog en el tablero y mover tarjetas |
| 6. Verificación y entrega | Informe y anexo; ejecución de RNF; `git tag v2.0-post-cambio` | **Recorrer los 3 finales con capturas**; ejecutar el README en limpio; **captura final del tablero**; exportar `git log`; armar y probar el ZIP |
| Video | Grabar la parte técnica (pruebas, arquitectura, cambio) | Grabar los 3 finales, la segunda historia y el error de destino E99 |

## Definición de terminado (borrador)

Una tarea está terminada cuando:
1. Su resultado está en el repositorio (commit en `main`).
2. Si es código, las pruebas pasan (`pytest`) y no rompe pruebas existentes.
3. Si es un artefacto del informe, usa el mismo vocabulario que requisitos y código (escena, opción, condición, efecto, sesión).
4. La tarjeta se movió a "Hecho" en el tablero.
5. Si se usó IA, quedó registrada en `IA.md`.
