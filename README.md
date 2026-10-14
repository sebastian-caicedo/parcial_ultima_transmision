# La última transmisión: motor de historias interactivas

Parcial práctico de Ingeniería de Software, Universidad Tecnológica de Bolívar.

## Integrantes

- Sebastián Felipe Caicedo Acosta
- Javier Alejandro Carta Lacharme

## Versiones requeridas

- Python 3.10 o superior
- pytest 8 o superior (ver `requirements.txt`)

## Instalación

```bash
git clone <URL_DEL_REPOSITORIO>
cd <carpeta_del_repositorio>
python -m venv .venv
# Windows: .venv\Scripts\activate    Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
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

Durante la partida: escribe el número de la opción, `r` para reiniciar o `s` para salir.

## Pruebas

```bash
python -m pytest
```

Configuración en `pytest.ini`. Archivos:

| Archivo | Qué cubre |
|---|---|
| `tests/test_motor.py` | U1, U2, U3, U5, CA01, CA02, tres finales, bloqueo |
| `tests/test_validador.py` | U4 (V01–V09), CA03, errores múltiples |
| `tests/test_integracion.py` | I1 (archivo real + motor + consola), comando validar, segunda historia |
| `tests/test_rnf.py` | RNF02 (archivos de `tests/datos_invalidos/`) y RNF03 (1000 entradas aleatorias) |

## Rutas para demostrar cada final

| Final | Elecciones (números en consola) |
|---|---|
| E4 Rescate | 1 Revisar señal → 1 Investigar archivo → 1 Activar con código |
| E5 El eco | 1 Revisar señal → 2 Continuar sin investigar → 1 Activar sin verificar |
| E6 Silencio | 1 Revisar señal → 2 Continuar sin investigar → 2 Cortar comunicación |
## Formato de contenido

_(Pendiente: explicación del contrato JSON para la escritora.)_

## Rutas para demostrar cada final

| Final | Elecciones |
|---|---|
| E4 Rescate | _(pendiente)_ |
| E5 El eco | _(pendiente)_ |
| E6 Silencio | _(pendiente)_ |

## Estructura del repositorio

```
data/          Historias en JSON (la de referencia y la segunda historia)
src/           Código fuente del motor
tests/         Pruebas automatizadas y archivos JSON inválidos para validación
docs/          Plan de trabajo, backlog, diagramas, solicitud de cambio
evidencias/    Capturas de tablero, resultados de pruebas y de RNF
scripts/       Utilidades (creación del tablero)
IA.md          Registro del uso de herramientas de IA
```

## Versiones

- `v1.0-pre-cambio`: versión guardada en la hora 6, antes de la solicitud de cambio.
- `v2.0-post-cambio`: versión final entregada.

## Limitaciones conocidas

_(Pendiente.)_

## Uso de IA

Ver [IA.md](IA.md).
