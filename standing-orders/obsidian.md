# Standing Orders — Obsidian

Permisos permanentes de Alfred sobre la vault de Obsidian de Pablo.

## Vault

- **Ruta:** `D:\Obsidian\Mi Bóveda\`
- **Formato:** Markdown con frontmatter YAML
- **Convención de tags:** `tags: [tag1, tag2]` en el frontmatter

## Autorizado sin preguntar

- Leer cualquier archivo `.md` de la vault
- Buscar notas por nombre, contenido o tag
- Crear notas nuevas siguiendo el formato del vault (frontmatter + markdown)
- Añadir contenido al final de notas existentes
- Actualizar el frontmatter (tags, fecha) de notas existentes

## Requiere confirmación

- Eliminar o mover notas
- Modificar el cuerpo de una nota existente (salvo añadir al final)
- Crear subcarpetas nuevas

## Herramientas

- Acceso directo a archivos: Read, Write, Edit, Glob
- Sin API ni plugin necesario

## Formato de nota nueva

```markdown
---
tags: [tag1, tag2]
fecha: YYYY-MM-DD
---

# Título

Contenido...
```
