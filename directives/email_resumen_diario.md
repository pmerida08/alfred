# Directiva: resumen diario del correo

**Cuándo:** 07:00 (HEARTBEAT) o cuando Pablo lo pida.
**Objetivo:** que Pablo sepa en dos minutos qué correo necesita algo de él.

## Pasos

1. `search_threads` con `in:inbox is:unread newer_than:1d`.
2. Clasifica cada hilo:
   - **Urgente:** pide respuesta o acción hoy (una entrevista, una prueba técnica, un cobro).
   - **Importante:** necesita atención esta semana.
   - **Informativo:** alertas, newsletters, notificaciones, recibos. Solo se cuentan.

   Ante la duda entre urgente e importante, urgente. Las respuestas de empresas (etiqueta `Empleo/Respuestas`) y los avisos de cobro nunca van a informativo.
3. Resume:

```
## Correo — [fecha]
**Urgente (N):**
- [Remitente]: [Asunto] — [qué hay que hacer]
**Importante (N):**
- [Remitente]: [Asunto] — [una línea]
**Informativo:** N (alertas, newsletters…)
```

Sin correo nuevo: «Sin correo nuevo.»

## Límites

Solo lectura: no marca como leído (Pablo decide qué ha leído), no mueve a spam, no crea borradores salvo que Pablo lo pida y no envía nada. Ordenar y archivar es cosa de `ordenar_bandeja.md`. Si la API falla, se informa del error sin reintentar.
