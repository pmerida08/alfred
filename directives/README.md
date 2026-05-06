# Directives — SOPs del sistema Alfred

## ¿Qué es una directiva?

Un SOP (Standard Operating Procedure) en Markdown que define **el qué y el por qué** de una tarea.

Alfred lee la directiva correspondiente antes de ejecutar cualquier proceso no trivial.

## Estructura de una directiva

```markdown
# Nombre del proceso

## Objetivo
Qué se quiere conseguir.

## Inputs
Qué información o archivos necesita el proceso.

## Herramientas
Qué scripts de `execution/` se usan y en qué orden.

## Pasos
1. Paso uno
2. Paso dos
...

## Edge cases
Situaciones especiales y cómo manejarlas.

## Output esperado
Qué debe existir o haber ocurrido al terminar.
```

## Convenciones de nombres

`<dominio>_<accion>.md` — ejemplos:
- `email_resumen_diario.md`
- `calendar_reunion_semanal.md`
- `notion_sincronizar_tareas.md`

## Regla clave

Si no existe directiva para algo, Alfred la crea antes de ejecutar.
