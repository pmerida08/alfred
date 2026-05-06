# Standing Orders — Email

Permisos permanentes de Alfred sobre el dominio de correo de Pablo.

## Autorizado sin preguntar

- Leer emails de la bandeja de entrada
- Clasificar emails por categoría (trabajo, personal, newsletters, spam)
- Generar resúmenes de emails no leídos
- Marcar como leído después de resumir
- Crear borradores de respuesta para revisión de Pablo
- Mover emails a carpetas/etiquetas existentes
- Archivar emails procesados

## Requiere confirmación

- Enviar cualquier email (incluyendo respuestas)
- Eliminar emails permanentemente
- Crear nuevas etiquetas o carpetas
- Acceder a emails más antiguos de 30 días (salvo búsqueda explícita)

## Herramientas autorizadas

- MCP Gmail (conectado directamente en la sesión de Claude Code)
  - `search_threads` — buscar y leer emails
  - `get_thread` — leer un hilo completo
  - `list_drafts` — ver borradores
  - `create_draft` — crear borrador para revisión

## Credenciales

- Gestionadas por el conector MCP — sin configuración adicional necesaria.
