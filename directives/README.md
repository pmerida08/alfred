# Directivas

Una directiva es un SOP en Markdown para una tarea que se repite: qué se quiere conseguir, qué hace falta y qué trampas hay. Si una tarea se repite y no tiene directiva, se crea.

## Cómo escribir una

- **Cabecera:** objetivo en una frase, cuándo se usa y qué script de `execution/` ejecuta, si lo hay.
- **Pasos:** solo los que no son obvios o tienen un orden que importa. Lo que el modelo haría bien por su cuenta no se escribe.
- **Datos:** rutas, IDs, comandos, formatos exactos de salida.
- **Edge cases y trampas:** lo que ya salió mal alguna vez y cómo evitarlo, con el porqué. Es la parte que más vale.
- **Límites:** qué necesita confirmación de Pablo.

Tono de colega: normas explicadas, sin mayúsculas de alarma ni «OBLIGATORIO». Si un paso depende de otra directiva, se enlaza en vez de copiarlo.

Nombre: `<dominio>_<accion>.md` (p. ej. `email_resumen_diario.md`), o solo `<dominio>.md` si cubre todo un área (`obsidian.md`, `atalaya.md`). Las directivas propias de un agente van en `agents/<id>/directives/`.
