# Standing Orders — Archivos locales

Permisos permanentes de Alfred sobre el sistema de archivos del proyecto.

## Autorizado sin preguntar

- Leer cualquier archivo del proyecto `D:/Programas/Alfred/`
- Editar archivos en `memory/`, `directives/`, `execution/`, `standing-orders/`
- Crear archivos nuevos en cualquier carpeta del proyecto
- Escribir y leer archivos en `.tmp/`
- Actualizar `MEMORY.md`, `DREAMS.md`, `HEARTBEAT.md`
- Ejecutar scripts Python existentes en `execution/`

## Requiere confirmación

- Eliminar cualquier archivo (salvo `.tmp/`)
- Modificar `.env`
- Modificar `CLAUDE.md` o `SOUL.md` (cambios de comportamiento del sistema)
- Acceder a rutas fuera de `D:/Programas/Alfred/`

## Notas

- `.tmp/` puede borrarse y regenerarse libremente.
- Los archivos de memoria son siempre seguros de sobreescribir.
