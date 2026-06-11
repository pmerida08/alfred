# Directiva: Analizar oferta de trabajo

## Objetivo

Evaluar el encaje entre el perfil de Pablo y una oferta de trabajo concreta, produciendo un análisis accionable y un fit score justificado.

## Inputs

- Oferta de trabajo: texto completo, URL o descripción proporcionada por Pablo
- CV de Pablo: `D:\Obsidian\Mi Bóveda\raw\docs\Pablo Mérida Velasco — CV.pdf`

## Proceso

### 0. Verificar si ya se candidató

Antes de cualquier análisis, consultar la BD de Notion buscando una candidatura con empresa y puesto coincidentes cuyo estado sea `"Solicitud enviada"`.

- Si existe → **no analizar**. Responder: `"Ya enviaste candidatura a [Empresa] para [Puesto] el [fecha]. La omito."` y detener el proceso.
- Si no existe → continuar con el análisis.

### 1. Leer el CV

Antes de cualquier análisis, leer el CV completo. No usar memoria de sesiones anteriores.

### 2. Extraer requisitos de la oferta

Identificar y separar:
- **Hard skills obligatorias** (must-have): lenguajes, frameworks, herramientas específicas
- **Hard skills deseables** (nice-to-have): mencionadas como plus o valoradas
- **Experiencia requerida**: años, tipo de proyectos, sector
- **Soft skills explícitas**: las que la oferta menciona directamente
- **Contexto de la empresa**: tamaño, sector, producto o servicio

### 3. Cruzar con el perfil de Pablo

Para cada requisito, determinar: cumple / cumple parcialmente / no cumple.

### 4. Calcular fit score

| Dimensión | Peso | Criterio |
|-----------|------|---------|
| Stack técnico | 40% | % de hard skills obligatorias cubiertas |
| Experiencia | 35% | Relevancia y años de experiencia relativa |
| Soft skills | 25% | Coincidencia con las explicitadas en la oferta |

Escala final 1–10. Redondear al entero más cercano.

### 5. Producir el análisis

Formato de salida:

```
## [Empresa] — [Puesto]

**Fit score: X/10**

### Puntos fuertes
- [skill/experiencia que encaja con la oferta]

### Gaps
- [requisito que Pablo no cumple o cumple parcialmente]

### Qué destacar en la candidatura
- [aspecto concreto a enfatizar en carta o CV]

### Recomendación
[Una frase: si vale la pena candidatar y por qué]
```

## Edge cases

- **Oferta en inglés:** el análisis se produce en español salvo que Pablo indique lo contrario.
- **Oferta sin requisitos técnicos claros:** basar la puntuación en experiencia y contexto del puesto.
- **Oferta demasiado genérica:** indicarlo y pedir a Pablo que añada más contexto si lo tiene.
- **Fit score < 4:** indicar explícitamente que el encaje es bajo antes de generar materiales.
