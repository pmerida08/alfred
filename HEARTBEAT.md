# HEARTBEAT — Tareas periódicas de Alfred

Cada vez que Alfred recibe un HEARTBEAT, lee esta tabla y ejecuta lo que corresponda
al momento actual. Si no hay nada para ese momento, responde: "OK".

---

## Tareas activas

| Frecuencia        | Hora  | Tarea                          | Directiva                                        |
|-------------------|-------|--------------------------------|--------------------------------------------------|
| Diario            | 07:00 | Resumen de emails              | `directives/email_resumen_diario.md`             |
| Diario            | 08:00 | Agenda del día                 | `directives/calendar_agenda_semanal.md`          |
| Diario            | 23:00 | Consolidación nocturna         | `directives/memory_consolidacion_nocturna.md`    |
| Cada sesión       | —     | Carga de contexto inicial      | `directives/session_inicio.md`                   |

---

## Cómo ejecutar

1. Leer la fila correspondiente al momento actual
2. Leer la directiva indicada
3. Ejecutar los pasos definidos en la directiva
4. Si hay error, registrar en `memory/errors.md`

## Cómo añadir una tarea

1. Crea o usa una directiva en `directives/`
2. Añade una fila a la tabla con frecuencia, hora y ruta de directiva
3. Alfred la ejecutará en el próximo HEARTBEAT correspondiente

---

## Log de ejecuciones recientes

| Fecha      | Hora  | Tarea                  | Estado    |
|------------|-------|------------------------|-----------|
| 2026-05-05 | —     | Setup inicial Alfred   | Completado |
