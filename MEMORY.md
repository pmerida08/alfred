# MEMORY — Hechos curados de Alfred

Este archivo contiene hechos permanentes promovidos desde las notas diarias.
Alfred lo lee al inicio de cada sesión junto con `memory/user.md`.

> Solo se añade aquí lo que supera el umbral de relevancia duradera.
> Las notas temporales van en `memory/YYYY-MM-DD.md`.

---

## Preferencias confirmadas

- Pablo prefiere respuestas directas, sin relleno ni introducción.
- Tono de mayordomo: formal pero sin rigidez.
- Idioma siempre español, términos técnicos en su forma original.
- No interrumpir con actualizaciones intermedias salvo que sea crítico.

## Decisiones de arquitectura

- El sistema Alfred usa DOE: Directives, Orchestration, Execution.
- Los scripts Python viven en `execution/`, los SOPs en `directives/`.
- Archivos temporales siempre en `.tmp/`, nunca en raíz.
- Credenciales solo en `.env`, nunca en código.

## Ecosistema de herramientas

- Email: Gmail (pablomerida03@gmail.com) — conector MCP
- Calendario: Google Calendar — conector MCP
- Notas personales: Obsidian — vault en `D:\Obsidian\Mi Bóveda\`, acceso directo a archivos
- Documentación y tareas: Notion — conector MCP, base de datos "Mis Tareas" (ID: d1668a67-3e64-46ee-a29e-6d98869f8a86)

---

*Última actualización: 2026-05-05*

## Hooks de Claude Code

Los hooks de tipo `UserPromptSubmit` que leen de `sys.stdin` (Python) bloquean todas las sesiones nuevas si Claude Code no cierra stdin. No usar `sys.stdin.read()` ni `json.load(sys.stdin)` en hooks — o eliminarlos directamente.
