# Directiva: Generar materiales de candidatura

## Objetivo

Producir una carta de presentación y notas de adaptación del CV para una oferta concreta, guardarlos en Notion como páginas hijo de la candidatura correspondiente.

## Prerequisito

Esta directiva solo se ejecuta después de haber completado `analizar_oferta.md`. No generar materiales sin análisis previo.

## Inputs

- Análisis de la oferta (resultado de `analizar_oferta.md`)
- CV de Pablo: `~/Documentos/Obsidian/Alfred/raw/docs/PabloMeridaVelasco_cvSpanish.pdf`
- Idioma objetivo: mismo que la oferta, salvo indicación de Pablo

## Proceso

### 1. Carta de presentación

**Estructura:**

1. **Párrafo de apertura** (2-3 frases): por qué Pablo encaja con el puesto. Mencionar la empresa por nombre. Sin "Me dirijo a ustedes para...".
2. **Párrafo de experiencia** (3-4 frases): 2-3 logros o proyectos concretos del CV que sean directamente relevantes a los requisitos de la oferta.
3. **Párrafo de motivación** (2-3 frases): qué le atrae del puesto o la empresa específicamente (inferir del contexto de la oferta, no inventar).
4. **Cierre** (1-2 frases): disponibilidad y llamada a la acción directa.

**Reglas:**
- Longitud máxima: 300 palabras.
- No usar frases hechas: "perfil dinámico", "trabajo en equipo", "reto profesional".
- Datos concretos: nombres de tecnologías, años de experiencia, proyectos reales del CV.
- Tono: profesional, directo, sin servilismo.

### 2. Notas de adaptación del CV

Un listado breve de qué ajustar en el CV para esta oferta:
- Qué experiencias o proyectos mover al principio
- Qué keywords de la oferta incorporar (si están respaldadas por experiencia real)
- Qué secciones o items son menos relevantes para esta oferta

Formato: lista con viñetas, máximo 6 puntos.

### 3. Guardar en Notion

1. Buscar la candidatura correspondiente en la BD de Notion.
   - Si no existe, crearla primero con los datos básicos (empresa, puesto, fecha, estado: "Analizada", fit score).
2. Crear dos páginas hijo dentro de la candidatura:
   - **"Carta de presentación"** con el texto generado
   - **"Notas CV"** con la lista de adaptaciones
3. Actualizar el campo estado a "Materiales listos" si existía como "Analizada".

## Edge cases

- **Fit score < 4:** avisar a Pablo antes de generar. Proceder solo si confirma.
- **Empresa sin nombre claro:** usar "su empresa" en la carta, marcar para revisión.
- **CV sin proyectos directamente relevantes:** usar la experiencia más transferible y explicitarlo en las notas CV.
