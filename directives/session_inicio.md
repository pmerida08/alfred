# Directiva: Inicio de sesión

**Dominio:** Sistema
**Cuándo:** Al inicio de cada sesión

---

Desde el 2026-09-25 el arranque ya no requiere leer nada a mano:

- `SOUL.md` y `memory/user.md` entran importados desde `CLAUDE.md`.
- El índice de hechos (`memory/hechos/MEMORY.md`) lo carga la memoria automática de Claude Code en el PC.
- Las notas diarias de hoy y ayer las inyecta el hook `.claude/hooks/notas_recientes.sh`.
- La bandeja de Gmail la pide `.claude/hooks/bandeja_diaria.sh`, solo en la primera sesión del día y solo en Windows.

Los `standing-orders/<dominio>.md` se leen cuando la tarea toca ese dominio, no al arrancar.

## Edge cases

- **Servidor Linux:** no hay memoria automática. Si hace falta un hecho permanente, leer `memory/hechos/MEMORY.md` y el fichero que corresponda.
- **La última nota diaria tiene más de 2 días:** el contexto reciente puede estar incompleto; mirar las notas anteriores si la tarea lo pide.
