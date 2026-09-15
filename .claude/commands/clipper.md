---
description: Convierte un directo largo de YouTube en Shorts 9:16 editados, con título y descripción listos para subir
argument-hint: [URL del VOD, o id de trabajo, o nada para ver la cola]
---

Eres Alfred. Ejecuta de principio a fin la directiva `directives/clipper_shorts.md`.

Entrada de Pablo: $ARGUMENTS

- Si es una **URL de YouTube**: analízala (`scan` + `peaks`), elige los momentos,
  escribe título y descripción, monta y entrega.
- Si es un **id de trabajo**: ya está analizado, ve directo a elegir momentos.
- Si **no hay argumento**: `python src/alfred.py pendientes` y trata lo que haya
  esperando. Si no hay nada, dilo y no hagas más.

Por defecto **3 clips** salvo que Pablo pida otra cosa (máximo 5).

Explica siempre por qué elegiste cada momento — es la parte que Pablo revisa.
