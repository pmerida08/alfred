"""
Alfred — Chequeo de salud de la autenticación de Claude Code.

El bot de Telegram ejecuta `claude -p` como subproceso. Ese CLI se autentica con
el login OAuth de la suscripción Pro. El `accessToken` rota cada pocas horas y se
renueva solo con el `refreshToken`; el fallo real (visto el 23-jun-2026) es que el
REFRESH deja de funcionar y la API devuelve `401 Invalid authentication
credentials` a todo, hasta re-loguear.

Por eso este chequeo NO mira `expiresAt` (siempre está "a punto de caducar"): hace
una SONDA real al CLI y avisa por Telegram solo si la autenticación falla de
verdad. El aviso se manda por la API HTTP de Telegram directa, así llega aunque el
CLI esté caído. Efecto secundario útil: si el refresh está sano, la sonda diaria
mantiene el token vivo.

Uso: python execution/check_token_expiry.py
Cron diario vía heartbeat.sh token. Sale 0 siempre que el chequeo se complete.
"""

import json
import os
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).parent.parent
load_dotenv(PROJECT_ROOT / ".env", override=True)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_ALLOWED_USER_ID")
CLAUDE_BIN = (
    os.getenv("CLAUDE_BIN")
    or shutil.which("claude")
    or "/home/pablo/.nvm/versions/node/v20.20.2/bin/claude"
)
PROBE_TIMEOUT = int(os.getenv("TOKEN_PROBE_TIMEOUT", "90"))

FIX = (
    "Arreglo: en el servidor → 'claude' → /login (autoriza en el navegador) "
    "→ sudo systemctl restart alfred.service."
)


def send_telegram(text: str) -> None:
    if not TELEGRAM_BOT_TOKEN or not CHAT_ID:
        print("[token-check] Falta TELEGRAM_BOT_TOKEN o TELEGRAM_ALLOWED_USER_ID en .env", file=sys.stderr)
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": CHAT_ID, "text": text}).encode()
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=data), timeout=20) as resp:
            resp.read()
    except Exception as e:
        print(f"[token-check] Error enviando a Telegram: {e}", file=sys.stderr)


def main() -> None:
    if not Path(CLAUDE_BIN).exists() and not shutil.which(CLAUDE_BIN):
        send_telegram(f"⚠️ Alfred: no encuentro el CLI de Claude ({CLAUDE_BIN}). Revisa la instalación.")
        print(f"[token-check] CLI no encontrado: {CLAUDE_BIN}", file=sys.stderr)
        return

    cmd = [CLAUDE_BIN, "-p", "responde solo: ok", "--output-format", "json", "--dangerously-skip-permissions"]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=PROBE_TIMEOUT, cwd=str(PROJECT_ROOT))
    except subprocess.TimeoutExpired:
        send_telegram(f"🔴 Alfred: el CLI de Claude no respondió en {PROBE_TIMEOUT}s (¿colgado?). {FIX}")
        print("[token-check] sonda: timeout", file=sys.stderr)
        return

    raw = proc.stdout.strip()
    if not raw:
        err = proc.stderr.strip()[:300]
        send_telegram(f"🔴 Alfred: el CLI de Claude no devolvió nada (exit {proc.returncode}). {FIX}\n\n{err}")
        print(f"[token-check] sonda: stdout vacío, stderr={err!r}", file=sys.stderr)
        return

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        print(f"[token-check] sonda: respuesta no-JSON: {raw[:200]!r}", file=sys.stderr)
        return

    status = data.get("api_error_status")
    result = (data.get("result") or "")
    auth_fail = status == 401 or (data.get("is_error") and "authenticate" in result.lower())

    if auth_fail:
        send_telegram(
            f"🔴 Alfred: la autenticación de Claude Code FALLA "
            f"(API {status or 'error'}: {result[:120]}). El bot dará 401 hasta re-loguear.\n\n{FIX}"
        )
        print(f"[token-check] AUTH FAIL: status={status} result={result[:120]!r}", file=sys.stderr)
    elif data.get("is_error"):
        # Error no relacionado con auth: lo dejo en log, sin molestar por Telegram.
        print(f"[token-check] CLI error no-auth: {result[:200]!r}")
    else:
        print("[token-check] OK: autenticación sana.")


if __name__ == "__main__":
    main()
