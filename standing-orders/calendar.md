# Standing Orders — Calendario

Permisos permanentes de Alfred sobre Google Calendar de Pablo.

## Autorizado sin preguntar

- Leer eventos del día actual y los próximos 7 días
- Generar agenda diaria y semanal
- Verificar disponibilidad para una franja horaria
- Crear eventos de duración ≤ 30 minutos en franjas libres
- Añadir recordatorios a eventos existentes

## Requiere confirmación

- Crear eventos de más de 30 minutos
- Modificar o eliminar eventos existentes
- Crear eventos con invitados externos
- Cualquier acción sobre calendarios compartidos

## Herramientas autorizadas

- MCP Google Calendar (conectado directamente en la sesión de Claude Code)
  - `list_events` — leer eventos
  - `list_calendars` — ver calendarios disponibles
  - `create_event` — crear eventos (con restricciones de standing order)
  - `update_event` — modificar eventos (requiere confirmación)
  - `suggest_time` — sugerir franjas libres

## Credenciales

- Gestionadas por el conector MCP — sin configuración adicional necesaria.
