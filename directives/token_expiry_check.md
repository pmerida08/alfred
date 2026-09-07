# Directiva — Sonda de salud de la auth de Claude Code

## Objetivo
Avisar a Pablo por Telegram cuando la autenticación de Claude Code falle, en vez
de que se entere por un `401 Invalid authentication credentials` en mitad de una
petición.

## Contexto
El bot de Telegram (`execution/telegram_bot.py`) ejecuta `claude -p` como
subproceso, que se autentica con el login OAuth de la suscripción Pro
(`~/.claude/.credentials.json`). El `accessToken` **rota cada pocas horas y se
renueva solo** con el `refreshToken` — eso es normal. El fallo real (visto el
23-jun-2026) es que el **refresh deja de funcionar** y la API devuelve 401 a todo
hasta re-loguear.

Por eso NO se vigila `expiresAt` (siempre está "a punto de caducar" → daría spam
diario). Se hace una **sonda real**: una llamada mínima al CLI; si responde 401,
es que el refresh está roto.

## Ejecución
- Script: `execution/check_token_expiry.py`
- Disparador: cron diario → `heartbeat.sh token` (09:00).
- Lógica:
  - Lanza `claude -p "responde solo: ok" --output-format json`.
  - Si `api_error_status == 401` o error de auth → aviso 🔴 por Telegram.
  - Si el CLI no responde / timeout → aviso 🔴 (posible cuelgue).
  - Si OK → solo log en `.tmp/heartbeat.log`, sin molestar.
- El aviso se manda con la **API HTTP de Telegram directa** (no por el CLI), así
  llega aunque el CLI esté caído.
- Efecto secundario útil: si el refresh está sano, la sonda diaria mantiene el
  token vivo.

## Arreglo cuando salta el aviso
En el servidor (interactivo): `claude` → `/login` (autorizar en el navegador)
→ `sudo systemctl restart alfred.service`. No es automatizable: es login a la
cuenta de Pablo. Ver memoria `feedback_claude_oauth_401`.

## Configuración opcional
- `CLAUDE_BIN` en `.env` — ruta al CLI (default: autodetección / ruta del servidor).
- `TOKEN_PROBE_TIMEOUT` en `.env` — segundos máx. de la sonda (default 90).
