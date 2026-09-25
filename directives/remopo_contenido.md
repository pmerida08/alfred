# Directiva: Contenido de una convocatoria en Remopo

**Dominio:** Remopo (`D:\Proyectos\Remopo`), plataforma de oposiciones de Pablo.
**Cuándo:** una petición «Pídela» en el panel `/admin`, o cuando Pablo pida preparar una convocatoria.
**Autonomía:** redactar contenido, validarlo y cargarlo en la base **local** sin preguntar. Cargar en la nube, generar audio con un servicio de pago o escribir al usuario que lo pidió: **preguntar antes**.

---

## Objetivo

Que una convocatoria tenga su temario literal, temas redactados sobre la norma vigente, preguntas con la cita que las respalda y el formato de su examen. Un error cuesta la confianza del usuario. Los clientes de la competencia se quejan sobre todo de temarios desactualizados y de errores que no se corrigen (`docs/PLAN.md` §2 bis).

## Entradas

- La ficha de la convocatoria (`/c/<slug>`): boletín de las bases y anuncio del BOE.
- **Las bases completas.** Sin ellas no se empieza: el temario sale de su anexo, no de otra convocatoria parecida.
- Los temas que ya existen en `content/temas/`. Los que tienen `comun: true` se pueden reutilizar.

## Pasos

1. **Leer las bases** y sacar:
   - Los epígrafes **literales** del anexo, en orden y con su bloque (común o específico).
   - El formato del examen: número de preguntas y de reserva, opciones, minutos, penalización y nota de aprobado. También los ejercicios prácticos.
   - Los datos de la ficha: plazas, grupo o subgrupo **real** (el del BOE es una estimación), sistema, turno, titulación y fechas.
2. **Casar cada epígrafe con el banco.** Si ya existe un tema común que cubre el epígrafe entero y es del mismo nivel (C2 no es A1), se reutiliza. Si cubre solo una parte, se escribe un tema nuevo: nunca estirar uno que se queda corto.
3. **Redactar los temas nuevos** en `content/temas/<slug>.json`, con la misma estructura que los de Legajo:
   - `cuerpo_md` en el Markdown del temario: `##` apartados, listas, tablas y avisos `> **Para el examen:** …`.
   - Solo sobre la legislación consolidada del BOE vigente el día del examen. Texto con la API `https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/<BOE-A-…>/texto`.
   - `normativa`: cada norma con su referencia (BOE nº y fecha) y sus reformas relevantes.
   - `revisado_en`: la fecha de hoy. Si se corrige un tema ya publicado, añadir una entrada a `cambios` con `{fecha, texto}`: el usuario la verá.
   - `slug` con sufijo de nivel o ámbito (`-c2-local-and`, `-c1-age`…), porque el mismo tema cambia de profundidad según el grupo.
4. **Preguntas**: al menos 25 por tema, con 4 opciones (o las que marquen las bases) y una sola correcta.
   - Cada una con `ref` (artículo exacto) y `why` (por qué es esa y no las otras).
   - Solo sobre lo que dice el epígrafe. Nada de preguntas de relleno de otro tema.
   - Las primeras de cada tema, de un solo concepto y sin trampas. Las trampas van después. En Streakode, empezar difícil hizo abandonar a la gente.
   - Se añaden **siempre al final** del tema: la clave es `<slug>:<n>` y el progreso de los usuarios depende de ella.
5. **Convocatoria** en `content/convocatorias/<slug>.json`. Si ya existía en el catálogo del BOE, usar **su mismo slug** para no duplicarla. Incluir `examen`, `ficha`, `ejercicios`, `enlaces`, `temas` (con el epígrafe literal) y `supuestos` si hay ejercicio práctico.
6. **Validar y cargar en local**: `npm run content` (debe salir ✓) y `npm run db:content`. Revisar la ficha y un test en `http://localhost:4760`.
7. **Audio**: el de Legajo se generó con edge-tts, que **no tiene licencia comercial**. Para temas nuevos, no generar audio hasta que Pablo decida el servicio (propuesta: Azure AI Speech, la misma voz Elvira). Mientras, el tema va sin audio.
8. **Cerrar la petición** en `/admin` (estado «hecha») y **redactar** el aviso al usuario. Lo envía Pablo, o Alfred con su OK expreso.

## Edge cases

- **No se encuentran las bases** (enlace roto, boletín sin texto): marcar la petición «en-curso», avisar a Pablo y no inventar el temario a partir de otra convocatoria.
- **Una norma cambia después de publicar** (reforma, nueva ley): marcar `a_revisar`, corregir y añadir una entrada a `cambios`. Si el examen es antes de que entre en vigor, se estudia la norma vigente ese día y se dice en el tema (como la Ley 4/2026 en Legajo).
- **Reportes de usuarios**: se contestan en 72 h como máximo. Si el usuario tiene razón, se corrige la pregunta (misma clave), se vuelve a poner `activa` y se registra en `cambios`.
- **Exámenes oficiales de años anteriores**: sirven para calibrar la dificultad y el estilo. Si se reproduce alguna pregunta, citar la convocatoria de origen.
