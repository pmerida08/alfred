---
description: Busca ofertas de empleo que encajen con el perfil de Pablo y genera el paquete de candidatura (CV + carta) por cada una vía HUNTER
argument-hint: [nº de ofertas y/o filtros, p. ej. "3 remoto IA"]
---

Eres Alfred. Delega esta búsqueda de empleo en HUNTER.

1. Carga el contexto de HUNTER: lee `agents/hunter/CLAUDE.md` e `agents/hunter/IDENTITY.md`.
2. Ejecuta de principio a fin la directiva `agents/hunter/directives/buscar_ofertas.md`.

Criterios pedidos por Pablo (número de ofertas, stack, modalidad remoto/híbrido/presencial, ubicación, seniority): $ARGUMENTS

Si no se indica número, procesa **3 ofertas** por defecto. Por cada oferta: analiza el fit, adapta el CV HTML, escribe la carta, regístrala en Notion con la URL de la oferta y deja los ficheros (CV + carta) en `.tmp/hunter_outbox/`. Devuelve al chat la carta y el link de cada oferta.
