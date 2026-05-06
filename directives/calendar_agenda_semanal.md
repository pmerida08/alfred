# Directiva: Agenda semanal

**Dominio:** Calendario  
**Cuándo:** 08:00 diario (lunes especialmente) o cuando Pablo lo solicite  
**Autonomía:** Solo lectura — no crear ni modificar eventos sin confirmación

---

## Objetivo

Dar a Pablo una vista clara de su semana (hoy + próximos 7 días) para que pueda planificar.

## Inputs

- Google Calendar de Pablo
- Rango: hoy al día +7

## Pasos

1. Usar MCP Google Calendar (`list_events` con rango hoy + 7 días) — obtener eventos
2. Organizar por día
3. Identificar:
   - Conflictos (solapamientos)
   - Franjas libres de más de 2 horas
   - Eventos sin descripción o sin localización
4. Generar resumen en este formato:

```
## Agenda — [día, fecha]

**Hoy:**
- HH:MM — HH:MM: [Evento] ([localización si existe])
- HH:MM — HH:MM: [Evento]
- Franja libre: HH:MM — HH:MM

**Mañana:**
- [mismo formato]

**Resto de la semana:**
- [día]: [N eventos] — [evento más importante]
```

5. Si hay conflictos, marcarlos con ⚠ y sugerir resolución.

## Output esperado

Vista de agenda en pantalla. Sin modificar nada en el calendario.

## Edge cases

- Día sin eventos: "Sin eventos — día libre."
- Evento de todo el día: mostrarlo primero con la etiqueta `[Todo el día]`
- Calendario compartido con eventos de otros: mostrarlos con `[Compartido]`
- Error de API: informar, no reintentar automáticamente
