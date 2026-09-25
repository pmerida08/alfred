# Directiva: el wiki de Obsidian

**Vault:** `D:\Obsidian\Mi Bóveda\` (solo en el PC Windows). Sigue el patrón LLM Wiki: Pablo deja fuentes en `raw/` y Alfred mantiene el resto.

Antes de cualquier operación, lee `SCHEMA.md` del vault: tiene la estructura de carpetas, el frontmatter estándar, el formato de `log.md` y el de `index.md`. Esta directiva añade solo lo que el SCHEMA no dice.

`raw/` no se modifica nunca. Toda operación deja una entrada en `log.md` (`## [YYYY-MM-DD] ingest|query|lint|update | descripción`).

## Proyectos

Cada proyecto vive en `Proyectos/<Nombre>/` con `README.md` (estado, objetivo, stack, decisiones abiertas), `log.md` propio y `Notas/`. Al hablar de un proyecto, lee su README (y el log si hace falta historia); cuando cambie algo relevante, actualiza el README y apúntalo en su `log.md`, no solo en el raíz. El estado oficial (activo, pausa…) lo da Atalaya; el README cuenta el porqué. Alfred es la excepción: su memoria vive en el repo (`memory/`), y en el vault solo hay una nota ligera `Proyectos/Alfred.md` para enlazarlo.

## Ingest (añadir una fuente)

1. Lee la fuente: de `raw/`, del chat o de una URL. Si no está en `raw/`, anota en `fuentes` «capturado desde chat YYYY-MM-DD».
2. Mira en `index.md` qué existe ya: se actualiza antes que duplicar.
3. Crea la página principal (normalmente en `Notas/`) con Resumen (2–4 frases), Puntos clave, Conexiones (`[[…]]` con una línea de por qué) y Citas notables si las hay. Una fuente muy larga se reparte en varias páginas temáticas.
4. Actualiza las páginas de las entidades y conceptos que toca (una fuente suele tocar entre 5 y 15) o créalas si merecen página propia; al tocarlas, actualiza `updated`.
5. Si algo contradice lo que ya había, márcalo con `> ⚠️ Contradice [[OtraPágina]]` y díselo a Pablo.
6. Añade la entrada a `index.md` y a `log.md` (páginas creadas y actualizadas).

## Query (responder desde el wiki)

- Parte de `index.md`, lee las páginas relevantes y cita cada afirmación (`según [[Página]]`). Señala contradicciones y datos que pueden estar viejos, y di claramente lo que el wiki no sabe.
- Si hacen falta más de 10–15 páginas, falta una síntesis central: propónla.
- Archiva la respuesta en `Síntesis/` cuando combina 3 o más páginas, es una comparativa o un análisis no trivial, o Pablo lo pide. La página lleva `pregunta` en el frontmatter y las fuentes consultadas con lo que aportó cada una. Añádela a `index.md`.
- Tareas y pendientes: `Bandeja/` y los README de `Proyectos/`.

## Lint (mantenimiento, cada 2–4 semanas o cuando Pablo lo pida)

Recorre el vault (sin `raw/`, `SCHEMA.md`, `index.md` ni `log.md`) y busca:

- Páginas huérfanas (nadie las enlaza).
- Frontmatter incompleto (`tipo`, `tags`, `created`, `updated`).
- Contradicciones entre páginas.
- Páginas con `updated` de hace más de 60 días que hablan de estados («activo», «pendiente»).
- Entidades mencionadas 3 o más veces sin página propia.
- Páginas que no están en `index.md`.
- Ítems de `Bandeja/` con más de 7 días.

Con menos de 20 páginas basta con huérfanas, frontmatter e índice. Aplica sin preguntar lo mecánico (añadir al índice, completar un frontmatter obvio) y propón a Pablo lo que cambie contenido o estructura. Entrega un informe breve (crítico, recomendado, sugerencias, cifras) y regístralo en `log.md`.
