# Alfred — Sistema de Asistencia Personal

**Demo interactiva:** [alfred-pa.netlify.app](https://alfred-pa.netlify.app)

Alfred es un sistema de asistencia personal construido sobre Claude Code. Gestiona operaciones diarias: búsqueda de empleo, documentos, nutrición, agenda y memoria persistente entre sesiones.

---

## Arquitectura DOE

El sistema separa tres capas para evitar errores compuestos:

| Capa | Rol | Ubicación |
|------|-----|-----------|
| **D — Directives** | SOPs en Markdown que definen el *qué* | `directives/` |
| **O — Orchestration** | Alfred decide qué ejecutar y en qué orden | `CLAUDE.md` |
| **E — Execution** | Scripts Python deterministas que hacen el *cómo* | `execution/` |

## Agentes especializados

- **HUNTER** — Búsqueda de empleo: analiza ofertas, adapta el CV, genera cartas de presentación y hace seguimiento en Notion.
- **FORGE** — Gym y nutrición: registra sesiones de entrenamiento, log de comidas vía foto (Telegram → Google Sheets), seguimiento de progreso en Notion.
- **BASILIO** — Documentos: extrae información de PDFs, DOCXs y MDs almacenados en Obsidian.
- **HERALDO** — Contenido y redes: estrategia, posts nativos por plataforma y vídeo corto, con la voz de cada cuenta.
- **ADA** — Desarrollo de aplicaciones web y móvil.

## Memoria

Alfred mantiene memoria persistente entre sesiones:

- `memory/YYYY-MM-DD.md` — Notas diarias; un hook carga las de hoy y ayer al arrancar
- `memory/hechos/` — Hechos permanentes, un fichero por hecho (memoria automática de Claude Code)
- `SOUL.md` — Carácter y tono del asistente

## Stack

- [Claude Code](https://claude.ai/code) (agente principal)
- Python (scripts de ejecución)
- Notion, Google Sheets, Obsidian (almacenamiento)
- Telegram (entrada de datos desde móvil)
- Servidor Linux para ejecución 24/7

---

Construido por [Pablo Merida](https://github.com/pmerida08).
