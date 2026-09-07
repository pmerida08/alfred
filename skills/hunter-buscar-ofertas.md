# Skill: hunter-buscar-ofertas

**ID:** `hunter-buscar-ofertas`
**Cuándo:** Pablo pide buscar ofertas de empleo, "tráeme ofertas", "búscame curro", o un paquete de candidaturas listo para enviar. Ejecutable en Claude Code y en el bot de Telegram.

Carga HUNTER (`agents/hunter/CLAUDE.md`) y ejecuta la directiva `agents/hunter/directives/buscar_ofertas.md`:

1. Busca en Internet ofertas que encajen con el perfil real de Pablo (lee su CV primero).
2. Filtra duplicados contra Notion (estado "Solicitud enviada").
3. Por cada oferta (3 por defecto): analiza el fit, adapta el CV HTML y escribe la carta de presentación.
4. Registra cada candidatura en Notion (con la URL de la oferta) en estado "Materiales listos".
5. Devuelve al chat la carta y el link de cada oferta, y deja los ficheros (CV HTML + carta) en `.tmp/hunter_outbox/`.

> En Telegram, todo fichero del outbox se adjunta automáticamente al chat al terminar (lo gestiona `execution/telegram_bot.py`).
