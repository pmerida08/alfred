# Directiva: Registrar solicitud enviada

## Objetivo

Actualizar el estado de una candidatura en Notion cuando Pablo confirme que ha enviado el CV a una empresa, y proporcionar la lista actualizada de candidaturas pendientes de envío.

## Trigger

Pablo dice que ha enviado el CV, mandado la solicitud, o similar expresión que confirme que ha candidatado a una oferta ya registrada.

## Proceso

### 1. Identificar la candidatura

- Buscar en la BD de Notion la entrada correspondiente por empresa y/o puesto.
- Si hay ambigüedad (varias entradas de la misma empresa), preguntar a Pablo cuál.

### 2. Actualizar en Notion

BD: `HUNTER — Candidaturas` — `collection://98bf6038-74db-4f77-9222-99b8e8932d06`

Modificar los campos (nombres exactos del esquema):
- **Estado** → `"Enviada"`
- **Fecha candidatura** → fecha de hoy

Si la candidatura no existe aún en Notion (Pablo la ha mandado sin pasar por HUNTER), crearla con los datos conocidos y estado `"Enviada"`.

### 3. Confirmar a Pablo

Una sola línea: empresa, puesto y fecha de envío registrada.

## Estados del ciclo de candidatura

| Estado | Significado |
|--------|-------------|
| `No aceptan solicitudes` | La oferta ya no admite candidaturas |
| `Materiales listos` | Carta y CV generados, pendiente de envío |
| `Enviada` | Pablo ha enviado la candidatura |
| `En proceso` | Hay respuesta de la empresa (entrevista, prueba) |
| `Rechazada` | Candidatura rechazada o sin respuesta |
| `Oferta recibida` | La empresa ha hecho una oferta |

Estos son los únicos valores válidos del select `Estado`. Cualquier otro nombre hace fallar la escritura.

## Edge cases

- **Empresa sin entrada en Notion:** crearla directamente con estado `"Solicitud enviada"`. Pedir a Pablo empresa, puesto y fecha si no los tiene.
- **Varias ofertas de la misma empresa:** confirmar el puesto concreto antes de actualizar.
- **Pablo dice "ya mandé las de ayer":** actualizar todas las que estén en `"Materiales listos"` del día anterior, previa confirmación de la lista.
- **Notion rechaza la escritura ("workspace has used all of its free blocks"):** el plan gratuito está lleno. NO dar la candidatura por registrada. Anotar los datos en `agents/hunter/memory/YYYY-MM-DD.md` marcados como PENDIENTE DE REGISTRAR y avisar a Pablo de que debe liberar bloques o cambiar de plan.
