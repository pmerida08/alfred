# Explore — Instrucciones de uso

**subagent_type:** `Explore`

## Propósito

Búsqueda rápida y localización de código en el codebase. Lee extractos de archivos; no analiza el contenido completo.

## Cuándo usar

- Localizar archivos por patrón (ej. `src/**/*.tsx`)
- Buscar símbolos, keywords o definiciones
- Responder "¿dónde está definido X?" o "¿qué archivos referencian Y?"

## Cuándo NO usar

- Revisión de código en profundidad → ADA
- Análisis cross-file o de consistencia → ADA
- Investigación con múltiples herramientas → General Purpose

## Parámetro breadth

- `quick` — búsqueda única y directa
- `medium` — exploración moderada
- `very thorough` — múltiples ubicaciones y convenciones de nombres
