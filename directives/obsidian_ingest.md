# Directiva: Obsidian INGEST

**Dominio:** Obsidian — Wiki LLM  
**Cuándo:** Pablo añade una fuente a `raw/` y pide procesarla, o pega un artículo/contenido para guardar  
**Autonomía:** Total — crear y actualizar páginas sin preguntar

---

## Objetivo

Integrar una nueva fuente en el wiki de forma que el conocimiento quede estructurado, enlazado y recuperable. Una sola fuente puede tocar 5-15 páginas.

## Vault

`D:\Obsidian\Mi Bóveda\`

---

## Flujo completo

### 1. Leer el SCHEMA
Antes de empezar: `D:\Obsidian\Mi Bóveda\SCHEMA.md`

### 2. Leer la fuente
- Si está en `raw/`: leer el archivo directamente
- Si Pablo la ha pegado en el chat: usar ese contenido
- Si es una URL: usar WebFetch para obtener el contenido

### 3. Identificar los elementos clave
Extraer:
- **Tema principal** → ¿va en Notas/, Proyectos/ o Áreas/?
- **Entidades** → personas, proyectos, herramientas, conceptos mencionados
- **Conexiones** → ¿qué páginas del wiki existente se relacionan?
- **Contradicciones** → ¿algo contradice conocimiento ya almacenado?

Consultar `index.md` para ver qué páginas ya existen.

### 4. Crear página principal de la fuente

Crear `Notas/[Título].md` (o carpeta apropiada) con este formato:

```markdown
---
tipo: nota
tags: [tag1, tag2]
created: YYYY-MM-DD
updated: YYYY-MM-DD
fuentes: [nombre-archivo-en-raw o URL]
---

# Título

## Resumen

2-4 frases capturando la idea central.

## Puntos clave

- Punto 1
- Punto 2
- Punto 3

## Conexiones

- [[PáginaRelacionada1]] — cómo se conecta
- [[PáginaRelacionada2]] — cómo se conecta

## Citas notables

> "Cita relevante" — Fuente
```

### 5. Actualizar páginas de entidades/conceptos existentes

Para cada entidad o concepto identificado:
- Buscar si ya existe su página en el wiki
- Si existe: añadir referencia a la nueva fuente y actualizar si hay info nueva
- Si no existe y merece página propia: crearla en `Notas/` con el formato estándar
- Actualizar el campo `updated` en el frontmatter

### 6. Actualizar index.md

Añadir la nueva nota en la sección correcta:
```markdown
- [[Notas/TítuloNota]] — descripción en una línea | fuente: nombre
```

### 7. Añadir entrada al log.md

```markdown
## [YYYY-MM-DD] ingest | Título de la fuente

- Fuente: nombre del archivo o URL
- Páginas creadas: [[NuevaPágina1]], [[NuevaPágina2]]
- Páginas actualizadas: [[PáginaExistente1]]
- Notas: observaciones relevantes del proceso
```

---

## Edge cases

- **Fuente muy larga:** dividir en múltiples páginas temáticas, no todo en una
- **Contenido ya existente:** verificar con index.md — actualizar en lugar de duplicar
- **Contradicción con wiki existente:** marcar con `> ⚠️ Contradice [[OtraPágina]]` y notificar a Pablo
- **Sin fuente en raw/:** procesar igualmente; anotar en fuentes: "capturado desde chat YYYY-MM-DD"

---

## Tipos de páginas del wiki

| Tipo | Cuándo crear |
|---|---|
| `nota` | Artículos, clips, fuentes procesadas |
| `concepto` | Ideas o temas que merecen página propia |
| `proyecto` | Iniciativas con objetivo y estado |
| `área` | Ámbitos de vida continuos |
| `síntesis` | Respuestas o análisis archivados |
| `persona` | Personas relevantes mencionadas frecuentemente |
