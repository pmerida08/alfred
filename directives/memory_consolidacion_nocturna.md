# Directiva: Consolidación nocturna de memoria (Dreaming)

**Dominio:** Sistema  
**Cuándo:** 23:00 diario (HEARTBEAT)  
**Autonomía:** Total — ejecutar sin preguntar

---

## Objetivo

Consolidar las notas de los últimos 7 días, identificar patrones relevantes y actualizar
`MEMORY.md` y `DREAMS.md` con información que merece ser permanente.

## Inputs

- Notas diarias `memory/YYYY-MM-DD.md` de los últimos 7 días
- `MEMORY.md` actual (para evitar duplicados)

## Pasos

1. Ejecutar `execution/memory_dreaming.py`
   - Lee las notas diarias de los últimos 7 días
   - Extrae: decisiones tomadas, preferencias expresadas, hechos nuevos, errores cometidos
   - Compara con `MEMORY.md` para evitar duplicados
   - Genera consolidación estructurada

2. Actualizar `DREAMS.md`:
   - Registrar la fecha de consolidación
   - Listar los temas identificados
   - Anotar qué se promovió a `MEMORY.md`

3. Si el script identifica hechos nuevos con alta relevancia (decisiones de arquitectura,
   nuevas herramientas, cambios de preferencias), añadirlos a `MEMORY.md`.

4. Guardar en la nota del día (`memory/<hoy>.md`) una línea:
   `- Dreaming ejecutado: [N] notas procesadas, [N] hechos promovidos.`

## Output esperado

- `DREAMS.md` actualizado
- `MEMORY.md` con nuevas entradas si procede
- Sin output en pantalla salvo error

## Edge cases

- Sin notas de los últimos 7 días: registrar en DREAMS.md y salir.
- Error en el script: registrar en `memory/errors.md` y continuar.
- `MEMORY.md` no existe: crearlo vacío y continuar.
