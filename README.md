# La última transmisión: motor de historias interactivas

Parcial práctico de Ingeniería de Software, Universidad Tecnológica de Bolívar.

## Integrantes

- Sebastián Felipe Caicedo Acosta
- Javier Alejandro Carta Lacharme

## Versiones requeridas

- Python 3.10 o superior (probado en Python 3.14 en Windows)
- pytest 8 o superior (única dependencia externa, solo para pruebas; licencia MIT)

## Instalación

```bash
git clone https://github.com/sebastian-caicedo/parcial_ultima_transmision.git
cd parcial_ultima_transmision
python -m pip install -r requirements.txt
```

## Ejecución

```bash
# Jugar una historia
python main.py jugar data/la_ultima_transmision.json

# Validar una historia sin jugarla (muestra todos los errores con su código V01-V09)
python main.py validar data/la_ultima_transmision.json

# Jugar otra historia con el mismo motor
python main.py jugar data/segunda_historia.json
```

Durante la partida: escribe el número de la opción, `r` para reiniciar, `d` para deshacer la última decisión (un solo nivel; aparece solo cuando hay algo que deshacer) o `s` para salir.

## Pruebas

```bash
python -m pytest                    # todas las pruebas
python scripts/verificar_rnf.py     # verifica RNF01-RNF03 y guarda evidencias en evidencias/rnf/
```

| Archivo | Qué cubre |
|---|---|
| `tests/test_motor.py` | U1, U2, U3, U5, U6 (deshacer), CA01, CA02, tres finales, bloqueo |
| `tests/test_validador.py` | U4 (V01–V09), CA03, errores múltiples, el validador no modifica los datos |
| `tests/test_integracion.py` | I1 (archivo real + motor + consola, incluido deshacer desde un final), comando validar, segunda historia |
| `tests/test_rnf.py` | RNF02 (archivos de `tests/datos_invalidos/`) y RNF03 (1000 entradas aleatorias) |

Resultados guardados: `evidencias/pruebas/resultado_v1.txt` (antes del cambio), `resultado_v2.txt` (después del cambio), `resultado_final.txt`.

## Rutas para demostrar cada final

| Final | Elecciones (números en consola) |
|---|---|
| E4 Rescate | 1 Revisar señal → 1 Investigar archivo → 1 Activar con código |
| E5 El eco | 1 Revisar señal → 2 Continuar sin investigar → 1 Activar sin verificar |
| E6 Silencio | 1 Revisar señal → 2 Continuar sin investigar → 2 Cortar comunicación |

Para ver cómo una condición cambia las opciones: en E2 elige "Investigar archivo" y en E3 aparece "Activar con código"; luego escribe `d`, elige "Continuar sin investigar" y en E3 aparece "Activar sin verificar".

## Formato de contenido (para escritores)

Una historia es un archivo `.json` en `data/` con esta estructura. Se usa el contrato de referencia de la guía, sin cambios.

| Elemento | Campos |
|---|---|
| Historia | `titulo` (texto), `inicio` (id de la escena inicial), `variables` (mapa de nombre → `true`/`false`), `escenas` (lista) |
| Escena | `id` (único), `texto`, `final` (`true`/`false`), `opciones` (lista; vacía si es final, al menos una si no lo es) |
| Opción | `id` (único dentro de la escena), `texto`, `destino` (id de escena existente), `condiciones` (mapa variable → valor que debe tener), `efectos` (mapa variable → valor que se asigna) |

Reglas:
- `condiciones` vacío (`{}`) = la opción siempre aparece. Con varias condiciones, deben cumplirse todas.
- `efectos` vacío = no cambia ninguna variable.
- Solo se usan variables declaradas en `variables` y solo valores `true` o `false` (sin comillas).

Ejemplo de opción:
```json
{"id": "investigar", "texto": "Investigar archivo", "destino": "E3",
 "condiciones": {}, "efectos": {"conoce_origen": true}}
```

Antes de publicar una historia, valídala con `python main.py validar <archivo>`. El programa nunca modifica el archivo; solo indica qué corregir.

## Estructura del repositorio

```
data/          Historias en JSON (la de referencia y la segunda historia)
src/           Código fuente del motor (modelo, sesión, validador, cargador, consola)
tests/         Pruebas automatizadas y archivos JSON inválidos (tests/datos_invalidos/)
docs/          Documentación por unidad, diagramas (docs/diagramas/), backlog y solicitud de cambio
evidencias/    Capturas del tablero, resultados de pruebas y de RNF
scripts/       verificar_rnf.py (verificación de los requisitos no funcionales)
IA.md          Registro del uso de herramientas de IA
```

## Versiones

- `v1.0-pre-cambio`: versión guardada en la hora 6, antes de la solicitud de cambio.
- `v2.0-post-cambio`: versión final entregada, con deshacer (RF17–RF20).

## Limitaciones conocidas

- Deshacer tiene un solo nivel y no existe rehacer (según la solicitud del cliente).
- No se detectan escenas inalcanzables ni historias sin ningún camino a un final (supuesto P3); un bloqueo se informa durante la partida.
- No hay guardado de partidas entre ejecuciones (fuera del alcance de la guía).
- Solo interfaz de consola.

## Uso de IA

Ver [IA.md](IA.md).
