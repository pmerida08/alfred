# Directiva: Obsidian QUERY

**Dominio:** Obsidian — Wiki LLM  
**Cuándo:** Pablo hace una pregunta sobre algo que podría estar en el wiki, o pide analizar/comparar temas del wiki  
**Autonomía:** Total — leer y archivar sin preguntar

---

## Objetivo

Responder preguntas usando el conocimiento acumulado en el wiki. Si la respuesta es valiosa, archivarla para que no desaparezca.

## Vault

`D:\Obsidian\Mi Bóveda\`

---

## Flujo completo

### 1. Leer el SCHEMA
`D:\Obsidian\Mi Bóveda\SCHEMA.md`

### 2. Leer el index.md
Identificar qué páginas son relevantes para la pregunta.

### 3. Leer las páginas relevantes
- Priorizar las más directamente relacionadas con la pregunta
- Si hay páginas enlazadas desde esas, leerlas también si aportan contexto
- Máximo 10-15 páginas; si se necesitan más, es señal de que el wiki necesita una página de síntesis

### 4. Sintetizar la respuesta

- Responder con citas explícitas: `según [[NombrePágina]]`
- Si hay contradicciones entre páginas: señalarlas explícitamente
- Indicar si la información podría estar desactualizada
- Si la respuesta requiere información que no está en el wiki: decirlo claramente

### 5. Decidir si archivar

Archivar en `Síntesis/` cuando:
- La respuesta requirió leer 3+ páginas y sintetizarlas
- Es una comparativa o análisis no trivial
- Pablo lo pide explícitamente
- La respuesta es un documento (tabla, análisis, plan)

### 6. Si se archiva: crear página en Síntesis/

```markdown
---
tipo: síntesis
tags: [tag1, tag2]
created: YYYY-MM-DD
pregunta: "Pregunta resumida en una línea"
fuentes: [[[Página1]], [[Página2]], [[Página3]]]
---

# Título del análisis

## Pregunta

Formulación exacta de la pregunta.

## Respuesta

Síntesis completa...

## Fuentes consultadas

- [[Página1]] — qué aportó
- [[Página2]] — qué aportó
```

### 7. Actualizar index.md y log.md

Si se archivó síntesis:
```markdown
# En index.md:
- [[Síntesis/TítuloAnálisis]] — descripción | fecha: YYYY-MM-DD

# En log.md:
## [YYYY-MM-DD] query | Pregunta resumida

- Páginas consultadas: [[Pág1]], [[Pág2]]
- Síntesis archivada: [[Síntesis/TítuloAnálisis]]  (omitir si no se archivó)
```

---

## Edge cases

- **Wiki vacío / sin páginas relevantes:** responder desde conocimiento general + sugerir ingest de fuentes sobre el tema
- **Información contradictoria en el wiki:** presentar ambas versiones y sugerir lint
- **Pregunta sobre estado de proyecto:** ir directamente a `Proyectos/[Nombre].md`
- **Pregunta sobre tarea o to-do:** revisar `Bandeja/` y `Proyectos/`
