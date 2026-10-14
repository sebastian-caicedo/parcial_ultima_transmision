# Revisión cruzada de requisitos

**Documento revisado:** `docs/02_requerimientos.md` — sección 3 (Requerimientos)

## Requisito y defecto detectado

Se revisaron los requisitos funcionales y no funcionales del validador. Se encontró una inconsistencia entre **RF15** y **RNF02**:

- **RF15** establece: «Cada error reportado indica su tipo, la causa y el campo o ID involucrado **cuando sea identificable**».
- **RNF02** exige que el **100 % de los nueve archivos inválidos** se rechace con un mensaje que contenga tanto «(a) el código del error» como «(b) el ID o campo involucrado».

La categoría **V01** contempla archivos que no son JSON válido o cuya raíz no es un objeto. Para esos casos puede no existir ningún campo ni ID recuperable. De hecho, el mensaje de ejemplo de V01 indica la línea del fallo, pero no un ID o campo. Por tanto, el criterio de RNF02 exige algo que RF15 considera opcional cuando no puede identificarse, y las pruebas podrían rechazar injustamente un validador correcto.

## Corrección propuesta

Mantener RF15 y ajustar el texto de **RNF02** de esta forma:

> El 100 % de los nueve archivos inválidos de prueba (V01–V09) debe rechazarse con un mensaje que incluya el código del error y la causa. Además, debe identificar el campo o ID involucrado **cuando sea posible**. Para V01, cuando el archivo no permita recuperar un campo o ID, se reportará el nombre del archivo y, en errores de sintaxis, la línea si está disponible.

## Criterio de aceptación verificable

1. Ejecutar el validador con los nueve archivos de `tests/datos_invalidos/` y comprobar que los nueve se rechacen y reporten su código V01–V09 correspondiente.
2. En los errores V02–V09, comprobar que aparezca el campo o ID pertinente cuando sea identificable.
3. En V01, si el JSON es ilegible, comprobar que aparezca el nombre del archivo y el número de línea cuando el analizador lo proporcione; **no exigir un ID inexistente**.
4. Conservar los resultados de la prueba como evidencia y actualizar RNF02 si el equipo acepta la corrección.

## Resultado

**Defecto identificado y corrección propuesta.** La incorporación definitiva de la nueva redacción a `docs/02_requerimientos.md` queda sujeta a la revisión del equipo. Esta observación no implica que el cambio ya haya sido implementado ni probado.

**Uso de IA:** ChatGPT ayudó a contrastar los requisitos y redactar esta observación. El equipo debe verificarla y registrarla en `IA.md` según las reglas del proyecto.
