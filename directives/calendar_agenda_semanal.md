# Directiva: agenda

**Cuándo:** 08:00 (HEARTBEAT) o cuando Pablo lo pida.
**Objetivo:** que Pablo vea su día y su semana para planificar.

## Pasos

1. `list_events` de hoy a dentro de 7 días.
2. Detecta solapamientos y franjas libres de más de 2 horas.
3. Resume:

```
## Agenda — [día, fecha]
**Hoy:**
- [Todo el día] Evento
- HH:MM–HH:MM Evento (lugar)
- Libre: HH:MM–HH:MM
**Mañana:** …
**Resto de la semana:**
- [día]: N eventos — el más importante
```

Solapamientos marcados con ⚠ y una propuesta para resolverlos. Los eventos de calendarios compartidos, con `[Compartido]`. Día sin eventos: «Día libre».

## Límites

Solo lectura. Crear o mover eventos sigue `standing-orders/calendar.md`. Si la API falla, se informa sin reintentar.
