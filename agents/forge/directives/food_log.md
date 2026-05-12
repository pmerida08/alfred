# Directiva: FORGE — Registro de Comidas

## Propósito

Registrar automáticamente los macros de cada comida que Pablo fotografíe por Telegram.
Los datos se almacenan en Google Sheets con ventana móvil de 90 días.

## Flujo automático (vía Telegram)

1. Pablo envía una foto de una comida al bot de Telegram.
2. El bot descarga la imagen y llama a `execution/food_log.py`.
3. El script analiza la imagen con Claude Vision (Haiku) y estima:
   - Nombre del plato
   - Calorías (kcal)
   - Proteínas (g)
   - Carbohidratos (g)
   - Grasas (g)
4. El resultado se escribe en Google Sheets (hoja "Comidas").
5. Se eliminan automáticamente los registros con más de 90 días de antigüedad.
6. El bot confirma el registro con un resumen de texto.

## Estructura del Google Sheet

Hoja: `Comidas` dentro del spreadsheet de Alfred.

| Fecha      | Hora  | Comida          | Calorías | Proteínas (g) | Carbohidratos (g) | Grasas (g) | Notas |
|------------|-------|-----------------|----------|---------------|-------------------|------------|-------|
| 2026-05-12 | 13:45 | Pollo con arroz | 620      | 48            | 65                | 12         |       |

## Variables de entorno necesarias (.env)

```
GOOGLE_SHEETS_CREDENTIALS_PATH=/ruta/a/service_account.json
FOOD_LOG_SHEET_ID=<id_del_spreadsheet>
FOOD_LOG_SHEET_NAME=Comidas
```

## Setup de Google Sheets (primera vez)

1. En Google Cloud Console: activar la API de Google Sheets.
2. Crear una cuenta de servicio → descargar el JSON de credenciales.
3. Crear un Google Spreadsheet en la carpeta "Alfred" de Google Drive.
4. Compartir el spreadsheet con el email de la cuenta de servicio (editor).
5. Copiar el ID del spreadsheet (parte de la URL) en `FOOD_LOG_SHEET_ID`.
6. Poner la ruta al JSON en `GOOGLE_SHEETS_CREDENTIALS_PATH`.

## Dependencias Python

```
pip install google-api-python-client google-auth anthropic python-dotenv
```

## Consultas manuales que puede manejar FORGE

- "¿Cuántas calorías llevo hoy?" → leer Google Sheets, sumar filas del día
- "¿Cuántas proteínas esta semana?" → agregar por semana
- "Muéstrame lo que comí ayer" → filtrar por fecha

Para consultas manuales FORGE lee el spreadsheet directamente usando el script o vía MCP de Google si está disponible.

## Retención de datos

La limpieza de 90 días se ejecuta automáticamente en cada escritura.
No requiere tarea cron separada.
