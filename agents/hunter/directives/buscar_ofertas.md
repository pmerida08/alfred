# Directiva: buscar ofertas y preparar el paquete

**Objetivo:** encontrar ofertas reales que encajen con Pablo y devolver, por cada una, la carta y el link listos para enviar, con el CV adjunto y la candidatura registrada en Notion.

**Cuándo:** Pablo pide ofertas ("búscame curro", "tráeme ofertas") o salta la búsqueda semanal del HEARTBEAT. Funciona desde Claude Code y desde Telegram.

**Cuántas:** 3 por defecto. Respeta el número y los filtros que dé Pablo (stack, remoto, ciudad, sin experiencia…).

## Pasos

1. **Outbox limpio.** Si `.tmp/hunter_outbox/` tiene ficheros de otra ejecución, muévelos a `.tmp/hunter_outbox_archivo/<fecha>/` (el harness bloquea `Remove-Item` en esa carpeta). Todo lo que quede en el outbox se adjunta en Telegram, así que tiene que estar solo lo de esta búsqueda.
2. **Lee el CV** para saber qué buscar: rol, stack y seniority reales.
3. **Busca.** Fuentes que han funcionado, de más a menos útil:
   - **Tecnoempleo**, con el filtro «Sin experiencia» (`ex=,1,`) cuando Pablo pida ofertas sin experiencia.
   - **API guest de LinkedIn** (`jobs-guest`, geoId de España `105646813`, `f_E=1,2`, última semana). Su filtro «entry level» no es fiable: revisa los años que pide cada oferta.
   - **Indeed** (MCP): busca por ciudad o en inglés; `location: "remote"` en español devuelve vacío.
   - **Jooble** como complemento.

   Abre cada candidata y saca empresa, puesto, requisitos, modalidad y la URL canónica. Descarta las que no tengan URL accesible o descripción suficiente.
4. **Filtra duplicados** según `agents/hunter/CLAUDE.md`. Si una se cae, busca otra para completar el cupo.
5. **Para cada oferta:**
   - Analízala con `analizar_oferta.md`. Con fit < 4 no se preparan materiales; anótala como descartada y busca una sustituta.
   - Prepara CV y carta con `generar_materiales.md`.
   - Regístrala en Notion: `Estado = Materiales listos`, fecha, fit y `URL oferta`.
   - Copia al outbox `CV-{Empresa}-{Puesto}.html`, `Carta-{Empresa}-{Puesto}.html` y `Carta-{Empresa}-{Puesto}.txt` (la de texto sirve para pegar en formularios).
6. **Devuelve el paquete al chat**, un bloque por oferta:

```
═══ Oferta 1/N ═══
Empresa — Puesto · Fit X/10 · Remoto/Híbrido/Presencial
Oferta: <URL>

CARTA DE PRESENTACIÓN
<texto completo de la carta>

CV y carta adjuntos · Registrado en Notion
```

La carta entera y el link van siempre en el texto: Pablo los usa tal cual desde el móvil. En Claude Code, añade además la ruta local del CV. Cierra con una línea: cuántas procesadas, omitidas por duplicado y descartadas por fit.

## Edge cases

- **Sin resultados:** amplía términos o pide a Pablo que afine. Nunca inventes ofertas ni URLs.
- **Todas duplicadas o con fit bajo:** dilo, enseña los análisis y ofrece buscar con otros términos.
- **Desde Telegram:** el móvil no abre rutas locales; el CV llega como adjunto por el outbox.
