# Directiva: Resumen diario de email

**Dominio:** Email  
**Cuándo:** 07:00 diario (HEARTBEAT) o cuando Pablo lo solicite  
**Autonomía:** Lectura total — requiere confirmación para enviar

---

## Objetivo

Dar a Pablo un resumen accionable de su bandeja de entrada en menos de 2 minutos de lectura.

## Inputs

- Bandeja de entrada de Gmail (pablomerida03@gmail.com)
- Emails no leídos de las últimas 24 horas

## Pasos

1. Usar MCP Gmail (`search_threads` con query `is:unread newer_than:1d`) — obtener emails no leídos
2. Clasificar por categoría:
   - **Urgente**: requiere respuesta hoy
   - **Importante**: requiere atención esta semana
   - **Informativo**: newsletters, notificaciones, recibos
   - **Spam/basura**: mover directamente
3. Generar resumen en este formato:

```
## Email — [fecha]

**Urgente (N):**
- [Remitente]: [Asunto] — [1 línea de contexto]

**Importante (N):**
- [Remitente]: [Asunto] — [1 línea de contexto]

**Informativo:** N emails (newsletters, notificaciones)
**Ignorado:** N emails movidos a spam
```

4. Marcar como leídos los emails resumidos
5. Mover spam identificado

## Output esperado

Resumen en pantalla. Sin enviar nada. Sin crear borradores salvo que Pablo lo pida.

## Edge cases

- Sin emails nuevos: "Bandeja vacía. Sin novedades."
- Error de API: informar del error, no reintentar automáticamente
- Email ambiguo (urgente vs importante): preferir "Urgente" por precaución
