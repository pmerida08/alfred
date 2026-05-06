# Directiva: Inicio de sesión

**Dominio:** Sistema  
**Cuándo:** Al inicio de cada sesión con Pablo  
**Autonomía:** Total — ejecutar sin preguntar

---

## Objetivo

Cargar el contexto completo de Alfred antes de responder al primer mensaje de Pablo.

## Pasos

1. Leer `SOUL.md` — carácter y tono
2. Leer `memory/user.md` — perfil de Pablo
3. Leer `MEMORY.md` — hechos curados permanentes
4. Leer `memory/<hoy>.md` si existe — notas del día actual
5. Leer `memory/<ayer>.md` si existe — notas del día anterior
6. Leer `standing-orders/<dominio>.md` relevantes para la sesión
7. Leer `HEARTBEAT.md` — verificar si hay tareas pendientes para este momento

## Output esperado

Alfred está listo para responder con contexto completo.
No confirmar la carga salvo que Pablo lo solicite.

## Edge cases

- Si un archivo no existe, ignorarlo y continuar.
- Si hay tareas de HEARTBEAT pendientes para el momento actual, ejecutarlas antes de responder.
- Si la última nota diaria tiene más de 2 días, añadir una nota interna de que el contexto reciente puede estar incompleto.
