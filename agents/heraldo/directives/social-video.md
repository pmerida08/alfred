# Directiva: social-video — Generar el vídeo/imagen del contenido

## Objetivo

Convertir un guion o una idea de HERALDO en el material audiovisual real (clip de vídeo corto o imagen) usando el MCP de generación multimedia. Es el paso que cierra el hueco entre "escribo el guion" y "tengo el vídeo".

## Trigger

Pablo pide generar el vídeo/clip/imagen de una pieza, un Short/Reel/TikTok, una portada, un b-roll o "hazme el vídeo de esto".

## Herramienta

**MCP de generación multimedia** (Higgsfield), servidor `d99c12f5-...`:
- `generate_video` — clips de vídeo corto.
- `generate_image` — keyframes, portadas de carrusel, miniaturas.
- `show_plans_and_credits` / `balance` — consultar créditos **antes** de generar.
- Edición: `upscale_video`/`upscale_image`, `reframe` (cambiar aspect ratio), `remove_background`.
- Si no está claro qué modelo usar, `models_explore(action:'recommend')` con el objetivo.

> ⚠️ **Generar consume créditos = dinero real.** Confirmar SIEMPRE con Pablo antes de lanzar: mostrar prompt, modelo, duración/formato y coste aproximado si se conoce.

## Inputs

- Guion o idea de origen (idealmente ya escrito por otra capacidad de HERALDO).
- Perfil (define aspect ratio, estilo, idioma del texto sobreimpreso).
- Formato de salida: vídeo vertical 9:16 (Shorts/Reels/TikTok) por defecto, o imagen.

## Proceso

1. Leer el perfil: aspect ratio, estilo visual, tono.
2. A partir del guion, redactar el/los **prompt(s)** de generación:
   - **Prompt en inglés**; el texto sobreimpreso y el guion, en el idioma del perfil.
   - Un clip = un movimiento de cámara dominante. Prompts cortos = más control.
3. Consultar créditos (`show_plans_and_credits` / `balance`).
4. **Confirmar con Pablo** el prompt, el modelo y el coste. No generar sin OK explícito.
5. Generar (`generate_video` / `generate_image`). Si hace falta, ajustar formato con `reframe`/`upscale`.
6. Descargar el resultado a `.tmp/heraldo/` y copiar el enviable a `.tmp/heraldo_outbox/`.
7. Registrar en Notion (Formato `Guion`/`Carrusel`, `Link` al render, prompt en `Notas`, estado `Borrador`).

## Salida

- Clip(s) o imagen(es) generados, en `.tmp/heraldo/` y en el outbox.
- Registro en Notion con el prompt usado y el link al render.

## Edge cases

- **Sin créditos:** informar y no intentar generar. Ofrecer alternativas (bajar duración, otro modelo más barato).
- **Prompt rechazado / resultado pobre:** iterar el prompt (más concreto, un solo movimiento) antes de reintentar; no quemar créditos a ciegas.
- **Publicación:** HERALDO nunca sube el vídeo a ninguna plataforma. Entrega el fichero; Pablo publica.
- **Media local de Pablo como input:** si aporta una foto/clip propio, usar el widget de subida del MCP (`media_upload_widget`) antes de generar.
