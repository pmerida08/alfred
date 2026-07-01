# Directiva: content-strategy — El plan macro de qué postear

## Objetivo

Definir la estrategia de contenido de un perfil: pilares, mezcla de formatos, cadencia y un calendario editorial concreto para las próximas semanas. Es el paso previo a producir piezas sueltas.

## Trigger

Pablo pide un plan de contenido, calendario editorial, "qué posteo", pilares o estrategia para una cuenta/red.

## Reutiliza

Skill de Alfred **`content-engine`** para los frameworks de estrategia por plataforma. HERALDO la carga como base y la adapta al perfil.

## Inputs

- Perfil (archivo en `perfiles/`). Si no existe, crearlo primero con la plantilla.
- Objetivo de negocio (crecer, autoridad, leads, ventas) y horizonte (2-4 semanas por defecto).
- Cadencia deseada (posts/semana por plataforma).

## Proceso

1. Leer el perfil: nicho, audiencia, voz, objetivo.
2. Definir **3-5 pilares de contenido** (temas recurrentes que sostienen la cuenta). Cada pilar responde a un dolor o deseo de la audiencia.
3. Asignar una **mezcla de formatos** por plataforma (educativo / historia / opinión / prueba social / promoción) con proporciones (p. ej. 70/20/10).
4. Traducirlo a un **calendario** en tabla: fecha, plataforma, pilar, formato, tema/ángulo, estado `Idea`.
5. Registrar las filas en la BD **HERALDO — Contenido** de Notion (estado `Idea`), vinculadas al perfil.

## Salida

- Tabla de pilares (pilar → a qué dolor responde → formatos típicos).
- Calendario editorial en tabla lista para ejecutar.
- Filas creadas en Notion en estado `Idea`.

## Edge cases

- **Sin perfil definido:** crear el perfil antes de estrategizar; no inventar la voz.
- **Objetivo difuso:** proponer 1-2 objetivos concretos y pedir a Pablo que elija.
- **Multiplataforma:** un pilar puede vivir en varias redes, pero el formato se decide por red.
