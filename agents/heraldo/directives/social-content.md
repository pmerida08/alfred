# Directiva: social-content — Una idea, nativa en IG, X y LinkedIn

## Objetivo

Coger UNA idea y adaptarla de forma **nativa** a cada plataforma (X, LinkedIn, Instagram), reescribiéndola en el formato y ritmo que cada una premia. Nunca copiar y pegar el mismo texto.

## Trigger

Pablo da una idea/mensaje y pide "sácalo para todas las redes", "adáptalo a X y LinkedIn", "versión para cada red".

## Reutiliza

Skill de Alfred **`crosspost`** (distribución multiplataforma sin duplicar) apoyada en **`content-engine`**. HERALDO las carga y aplica la voz del perfil.

## Inputs

- La idea/mensaje núcleo.
- Perfil (voz, audiencia).
- Plataformas destino (por defecto X, LinkedIn, Instagram).

## Proceso

1. Leer el perfil y destilar la **idea núcleo** en una frase.
2. Reescribir por plataforma:
   - **X:** hook seco en la 1ª línea; si da para hilo, estructurarlo; brevedad y ritmo.
   - **LinkedIn:** primera línea que corta antes del "ver más"; desarrollo con historia o aporte concreto; salto de línea generoso; cierre con pregunta o CTA suave.
   - **Instagram:** caption con gancho + contexto; si encaja, versión carrusel (derivar a `content-studio`).
3. Mantener la idea, cambiar la forma: cada versión debe leerse como escrita para esa red.
4. Pasar cada versión por `humanise-text`.
5. Guardar en `.tmp/heraldo_outbox/` y registrar en Notion (una fila por plataforma o una fila con las tres versiones, según prefiera Pablo).

## Salida

- Tres versiones nativas (X / LinkedIn / Instagram) en bloques separados, listas para copiar.
- Ficheros en outbox y registro en Notion.

## Edge cases

- **Idea que solo encaja en una red:** decirlo y no forzar las otras.
- **TikTok/YouTube en el mix:** derivar esa versión a guion de vídeo corto (no es texto de feed).
- **Límites de caracteres:** respetar el de X; en LinkedIn cuidar el corte del "ver más".
