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

_(Pendiente: comando para jugar una historia.)_

## Pruebas

```bash
python -m pytest -v
```

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
