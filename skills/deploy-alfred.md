# Skill: deploy-alfred — Subir cambios a Alfred

## Cuándo se activa

Cuando el usuario confirme que quiere subir cambios a GitHub tras implementar una funcionalidad.

## Proceso completo

### 1. Verificar que hay cambios reales

```bash
git status
git diff --stat
```

Si no hay archivos modificados o nuevos, informar y detener.

### 2. Identificar qué se implementó

- Leer `git diff` y `git status` para ver los archivos cambiados.
- Inferir en una frase corta qué funcionalidad se añadió (ej. "Agente BASILIO para consulta de documentos").
- Determinar a qué rama del dashboard pertenece (ver tabla abajo).

### 3. Actualizar dashboard.html

Editar el array `BRANCHES` en el `<script>` de `dashboard.html`:

- Localizar la rama correcta según la tabla:

| Tipo de cambio | Rama del dashboard |
|---|---|
| Nuevo agente | `Agentes` (n: '06') |
| Nuevo skill | `Código` (n: '03') o `Automatización` (n: '04') |
| Nueva directiva / SOP | `Automatización` (n: '04') |
| Integración con herramienta externa | `Información` (n: '01') |
| Script Python / ejecución | `Automatización` (n: '04') |
| Diseño / frontend | `Diseño` (n: '05') |
| Investigación / análisis | `Investigación` (n: '02') |

- Añadir el nuevo leaf al array `leaves` de la rama correspondiente.
- Actualizar el `<span class="footer-mono">` del footer con los contadores reales:
  - Contar archivos en `directives/` → "X directives"
  - Contar archivos en `execution/` → "Y scripts"
  - Contar entradas en `agents/AGENTS.md` (filas de tabla) → "Z agentes"
  - Contar entradas en `skills/SKILLS.md` (filas de tabla) → "W skills"

### 4. Commit

Incluir todos los archivos modificados en esta sesión más `dashboard.html`:

```bash
git add <archivos_cambiados> dashboard.html
git commit -m "feat: <descripción breve de lo implementado>

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

### 5. Push

```bash
git push origin <rama_actual>
```

### 6. Crear PR y mergear

```bash
gh pr create --title "feat: <descripción>" --body "<resumen>" --base main
gh pr merge <número> --merge --delete-branch
```

## Reglas

- No preguntar por confirmación adicional una vez el usuario dijo que sí.
- Si el push falla por conflictos, informar sin forzar.
- Si ya existe un PR abierto para la rama, usar `gh pr merge` directamente sin crear uno nuevo.
- Después del merge, confirmar con una sola línea: "Subido y mergeado en main."
