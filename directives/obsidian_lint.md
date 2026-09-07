# Directiva: Obsidian LINT

**Dominio:** Obsidian — Wiki LLM  
**Cuándo:** Pablo pide "lint del wiki", o periódicamente cada 2-4 semanas  
**Autonomía:** Proponer cambios — aplicar solo los que Pablo confirme

---

## Objetivo

Mantener el wiki sano: detectar inconsistencias, páginas huérfanas, información desactualizada y lagunas de conocimiento.

## Vault

`D:\Obsidian\Mi Bóveda\`

---

## Flujo completo

### 1. Leer el SCHEMA y el index.md
`D:\Obsidian\Mi Bóveda\SCHEMA.md` + `D:\Obsidian\Mi Bóveda\index.md`

### 2. Escanear el wiki

Recorrer todas las carpetas del wiki con Glob: `D:\Obsidian\Mi Bóveda\**\*.md`
Excluir: `raw/`, `SCHEMA.md`, `index.md`, `log.md`

### 3. Checks a ejecutar

#### A. Páginas huérfanas
Páginas que no aparecen enlazadas desde ninguna otra página ni desde index.md.
→ Proponer enlazarlas o moverlas a Bandeja/.

#### B. Frontmatter incompleto
Páginas sin `tipo`, `tags`, `created` o `updated`.
→ Proponer completar.

#### C. Contradiciones
Buscar afirmaciones opuestas sobre el mismo tema en páginas distintas.
→ Señalar ambas páginas y proponer resolución.

#### D. Claims potencialmente desactualizados
Páginas con `updated` hace más de 60 días que contienen estados ("activo", "en progreso", "pendiente").
→ Listar para que Pablo verifique si siguen vigentes.

#### E. Conceptos sin página propia
Entidades mencionadas frecuentemente (3+ veces) que no tienen su propia página.
→ Proponer crear páginas para ellas.

#### F. index.md desincronizado
Páginas que existen en el vault pero no aparecen en index.md.
→ Añadir automáticamente.

#### G. Bandeja sin procesar
Si hay ítems en `Bandeja/` con más de 7 días.
→ Notificar a Pablo para procesarlos.

### 4. Generar reporte

Crear un resumen estructurado:

```markdown
## Reporte de Lint — YYYY-MM-DD

### Crítico (requiere atención)
- ...

### Recomendado
- ...

### Sugerencias
- ...

### Estadísticas
- Total páginas: N
- Páginas sin actualizar en 60+ días: N
- Ítems en Bandeja: N
```

### 5. Aplicar cambios

- Cambios automáticos seguros (añadir a index.md, completar frontmatter obvio): aplicar sin preguntar
- Cambios de contenido o restructuración: proponer a Pablo primero

### 6. Registrar en log.md

```markdown
## [YYYY-MM-DD] lint | Health check completo

- Páginas revisadas: N
- Huérfanas encontradas: N
- Desactualizadas: N
- Cambios aplicados: descripción
- Pendientes de Pablo: descripción
```

---

## Edge cases

- **Wiki muy pequeño (<20 páginas):** lint rápido, solo checks A, B y F
- **Muchas contradicciones:** probable señal de que falta una página de síntesis central — sugerirla
