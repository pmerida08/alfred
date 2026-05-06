# Directiva: Nota rápida en Obsidian

**Dominio:** Obsidian  
**Cuándo:** Cuando Pablo pida guardar algo en Obsidian, o Alfred detecte información que merece persistir como nota  
**Autonomía:** Total — crear y leer sin preguntar

---

## Objetivo

Crear o actualizar notas en la vault de Obsidian de Pablo.

## Vault

`D:\Obsidian\Mi Bóveda\`

## Pasos — Crear nota nueva

1. Determinar título y tags apropiados según el contenido
2. Crear el archivo `D:\Obsidian\Mi Bóveda\<Título>.md` con este formato:

```markdown
---
tags: [tag1, tag2]
fecha: YYYY-MM-DD
---

# Título

Contenido...
```

3. Confirmar creación con la ruta del archivo.

## Pasos — Leer o buscar notas

1. Usar Glob para encontrar archivos: `D:\Obsidian\Mi Bóveda\**\*.md`
2. Leer el archivo con Read
3. Devolver el contenido formateado

## Pasos — Añadir a nota existente

1. Leer la nota actual con Read
2. Añadir el contenido al final con Edit
3. No modificar el frontmatter salvo que se pida explícitamente

## Edge cases

- Si el título ya existe: preguntar si añadir al final o crear nota nueva con fecha.
- Si Pablo no especifica tags: inferirlos del contenido.
- Nombres de archivo: usar el mismo texto que el título H1, sin caracteres especiales problemáticos.
