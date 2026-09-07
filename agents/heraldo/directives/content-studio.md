# Directiva: content-studio — Carruseles y posts en lote

## Objetivo

Producir contenido en volumen a partir de una idea o pilar: carruseles completos (portada + slides + caption) y tandas de posts listos para programar.

## Trigger

Pablo pide un carrusel, una tanda de posts, "prepárame 5 posts sobre X", contenido "en lote" o "para la semana".

## Reutiliza

Skill de Alfred **`content-engine`** (estructura de carruseles y series) y, para las plataformas de destino, **`crosspost`** cuando la tanda debe salir en varias redes.

## Inputs

- Idea/pilar de partida (o una fila `Idea` del calendario).
- Perfil y plataforma(s).
- Cantidad: nº de posts o nº de slides del carrusel.

## Proceso

1. Leer el perfil (voz, pilares, do's & don'ts).
2. **Si es carrusel:**
   - Portada con gancho de una línea (la que decide el swipe).
   - 5-10 slides, una idea por slide, progresión lógica (problema → desarrollo → resolución).
   - Slide final con CTA claro.
   - Caption que aporta contexto y refuerza el CTA.
3. **Si es tanda de posts:**
   - N posts autónomos alrededor del pilar, cada uno con su propio hook, sin repetir ángulo.
   - Variar formato (opinión, lista, historia, dato) dentro de la tanda.
4. Pasar toda la tanda por `humanise-text` antes de entregar.
5. Guardar los ficheros enviables en `.tmp/heraldo_outbox/` (un `.md`/`.txt` por pieza; carrusel como lista numerada de slides).
6. Registrar cada pieza en Notion (estado `Borrador`).

## Salida

- Carrusel (portada + slides + caption) o tanda de posts, en bloques listos para copiar.
- Ficheros en `.tmp/heraldo_outbox/`.
- Piezas en Notion en estado `Borrador`.

## Edge cases

- **Idea insuficiente para N slides:** proponer menos slides antes que rellenar con paja.
- **Carrusel de LinkedIn (PDF):** entregar el contenido slide a slide indicando que va como documento/PDF; HERALDO no maqueta el diseño (eso es de un skill de diseño).
- **Tanda multiplataforma:** no copiar y pegar; reescribir por plataforma vía `social-content`.
