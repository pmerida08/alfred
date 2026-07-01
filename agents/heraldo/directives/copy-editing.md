# Directiva: copy-editing — Te pule lo que escribiste

## Objetivo

Editar un texto ya escrito para mejorar claridad, ritmo, concisión y corrección, **respetando la voz del autor**. Pulir, no reescribir de cero.

## Trigger

Pablo pega un texto y pide "púlelo", "mejóralo", "revísalo", "acorta esto" o "corrige".

## Reutiliza

Skill de Alfred **`brand-voice`** para mantener la voz al editar. Si además huele a IA, encadenar con `humanise-text`.

## Inputs

- El texto a editar.
- Perfil/voz de referencia (si aplica).
- Objetivo de la edición (acortar, aclarar, subir el tono, corregir).

## Proceso

1. Leer el texto entero antes de tocar nada. Identificar la intención y la voz.
2. Editar por capas:
   - **Estructura:** ¿el orden sirve al mensaje? ¿el hook está al principio?
   - **Concisión:** cortar redundancias, muletillas y frases que no aportan.
   - **Ritmo:** alternar longitud de frase; romper párrafos densos.
   - **Claridad:** una idea por frase; sustituir jerga innecesaria.
   - **Corrección:** ortografía, tildes, puntuación, concordancia.
3. Preservar la voz: no imponer un estilo ajeno al autor.
4. Entregar la versión pulida y, si Pablo lo pide, un **diff resumido** de los cambios de peso.

## Salida

- Texto pulido listo para usar.
- Opcional: lista breve de los cambios importantes y por qué.

## Edge cases

- **Texto que necesita reescritura profunda, no edición:** avisar y ofrecer reescribir (deriva a `copywriting`).
- **Voz muy marcada:** conservar giros propios aunque sean "incorrectos" si son intencionados y funcionan.
- **Contenido en otro idioma:** editar en ese idioma, sin traducir salvo petición.
