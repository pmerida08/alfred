"""
Alfred — Búsqueda de empleo semanal (HEARTBEAT del domingo).

El cron dispara esto cada domingo a las 12:00 vía `heartbeat.sh buscar_trabajo`.
Ejecuta la directiva `buscar_ofertas` con el CLI de Claude en modo headless,
captura el texto resultante (cartas + links de las ofertas) y lo PUSHEA a
Telegram; luego envía como documentos los ficheros que HUNTER dejó en
`.tmp/hunter_outbox/` (CV HTML + cartas) y los borra.

A diferencia del flujo normal del bot, aquí nadie está respondiendo a un mensaje:
el envío a Telegram se hace con la API HTTP directa (urllib), igual que
`check_token_expiry.py`, para no depender de que el bot esté vivo ni de paquetes
extra en el venv del servidor.

Uso: python execution/hunter_weekly.py
Sale 0 siempre que el chequeo se complete (errores se avisan por Telegram).
"""

import json
import os
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
import uuid
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
# La búsqueda completa (web search + análisis + CV HTML + Notion por cada oferta)
# tarda varios minutos. Margen amplio para no cortarla a medias.
PROBE_TIMEOUT = int(os.getenv("HUNTER_WEEKLY_TIMEOUT", "900"))
OUTBOX = PROJECT_ROOT / ".tmp" / "hunter_outbox"

PROMPT = (
    "HEARTBEAT buscar_trabajo (domingo 12:00). Delega en HUNTER y ejecuta de "
    "principio a fin la directiva agents/hunter/directives/buscar_ofertas.md "
    "(3 ofertas por defecto). Devuelve en tu respuesta la carta y el link de cada "
    "oferta; deja los ficheros (CV + carta) en .tmp/hunter_outbox/."
)


def _api(method: str) -> str:
    return f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/{method}"


def send_message(text: str) -> None:
    """Envía texto a Telegram, troceado a 4096 caracteres."""
    if not TELEGRAM_BOT_TOKEN or not CHAT_ID:
        print("[hunter-weekly] Falta TELEGRAM_BOT_TOKEN o TELEGRAM_ALLOWED_USER_ID en .env", file=sys.stderr)
        return
    for i in range(0, max(len(text), 1), 4096):
        chunk = text[i:i + 4096]
        data = urllib.parse.urlencode({"chat_id": CHAT_ID, "text": chunk}).encode()
        try:
            with urllib.request.urlopen(urllib.request.Request(_api("sendMessage"), data=data), timeout=30) as resp:
                resp.read()
        except Exception as e:
            print(f"[hunter-weekly] Error enviando texto a Telegram: {e}", file=sys.stderr)


def send_document(path: Path) -> None:
    """Envía un fichero como documento a Telegram (multipart/form-data con urllib)."""
    if not TELEGRAM_BOT_TOKEN or not CHAT_ID:
        return
    boundary = uuid.uuid4().hex
    pre = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="chat_id"\r\n\r\n{CHAT_ID}\r\n'
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="document"; filename="{path.name}"\r\n'
        f"Content-Type: application/octet-stream\r\n\r\n"
    ).encode()
    post = f"\r\n--{boundary}--\r\n".encode()
    body = pre + path.read_bytes() + post
    req = urllib.request.Request(_api("sendDocument"), data=body)
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            resp.read()
    except Exception as e:
        print(f"[hunter-weekly] Error enviando documento {path.name}: {e}", file=sys.stderr)


def flush_outbox() -> int:
    """Envía y borra los ficheros del outbox de HUNTER. Devuelve cuántos envió."""
    if not OUTBOX.exists():
        return 0
    files = sorted(p for p in OUTBOX.iterdir() if p.is_file())
    for f in files:
        send_document(f)
        try:
            f.unlink()
        except Exception:
            pass
    return len(files)


def _is_quota_error(text: str) -> bool:
    """True si el error del CLI es por límite de uso de Claude, no un fallo real."""
    t = (text or "").lower()
    return any(k in t for k in (
        "session limit", "usage limit", "rate limit", "hit your limit",
        "out of credit", "límite de uso", "resets",
    ))


def report_failure(detail: str) -> None:
    """Avisa de un fallo distinguiendo 'sin cuota de Claude' de un error de verdad."""
    detail = (detail or "").strip()
    if _is_quota_error(detail):
        send_message(
            "🟡 Alfred: no he podido buscar empleo porque Claude está sin cuota de uso "
            "ahora mismo. No es un fallo del sistema; reintenta con /buscar_trabajo "
            f"cuando se resetee.\n\n{detail[:300]}"
        )
    else:
        send_message(f"🔴 Alfred: la búsqueda de empleo falló.\n\n{detail[:500]}")


def main() -> None:
    if not Path(CLAUDE_BIN).exists() and not shutil.which(CLAUDE_BIN):
        send_message(f"⚠️ Alfred: no encuentro el CLI de Claude ({CLAUDE_BIN}) para la búsqueda de empleo del domingo.")
        print(f"[hunter-weekly] CLI no encontrado: {CLAUDE_BIN}", file=sys.stderr)
        return

    cmd = [CLAUDE_BIN, "-p", PROMPT, "--output-format", "json", "--dangerously-skip-permissions"]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=PROBE_TIMEOUT, cwd=str(PROJECT_ROOT))
    except subprocess.TimeoutExpired:
        send_message(f"🔴 Alfred: la búsqueda de empleo del domingo no terminó en {PROBE_TIMEOUT}s y se cortó.")
        print("[hunter-weekly] timeout", file=sys.stderr)
        flush_outbox()
        return

    raw = proc.stdout.strip()
    if not raw:
        err = proc.stderr.strip()
        report_failure(f"(exit {proc.returncode}) {err}")
        print(f"[hunter-weekly] stdout vacío, stderr={err[:300]!r}", file=sys.stderr)
        return

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        # Sin JSON parseable mando el crudo recortado para no perder el trabajo hecho.
        send_message(raw[:4000])
        flush_outbox()
        print(f"[hunter-weekly] respuesta no-JSON: {raw[:200]!r}", file=sys.stderr)
        return

    result = (data.get("result") or "").strip()
    if data.get("is_error") or not result:
        report_failure(result)
        print(f"[hunter-weekly] is_error/result vacío: {result[:200]!r}", file=sys.stderr)
        return

    # Texto (cartas + links) primero, ficheros después: el mismo orden que en el bot.
    send_message(result)
    n = flush_outbox()
    print(f"[hunter-weekly] OK: enviado resumen + {n} fichero(s) del outbox.")


if __name__ == "__main__":
    main()
