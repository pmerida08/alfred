"""
Alfred — Aviso de saldo bajo en OpenRouter.

La lectura de tickets de Alacena (y Estancia) gasta saldo de la cuenta de OpenRouter de
Pablo. Si se acaba, Alacena pasa sola a «en mantenimiento», pero es mejor recargar antes:
este chequeo diario mira el saldo y avisa por Telegram cuando baja del umbral.

La clave se lee de OPENROUTER_API_KEY (entorno o .env). En el .env de Alfred la línea está
comentada para que no la use nada más; si es así, se toma de esa línea comentada.

Uso: python execution/check_openrouter_saldo.py [--siempre]
  --siempre  manda el saldo aunque esté por encima del umbral (para probar el aviso).
Cron diario vía heartbeat.sh openrouter. Sale 0 siempre que el chequeo se complete.
"""

import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).parent.parent
load_dotenv(PROJECT_ROOT / ".env", override=True)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_ALLOWED_USER_ID")
UMBRAL = float(os.getenv("OPENROUTER_SALDO_MINIMO", "2"))


def clave_openrouter() -> str | None:
    clave = os.getenv("OPENROUTER_API_KEY")
    if clave:
        return clave.strip()
    env = PROJECT_ROOT / ".env"
    if env.exists():
        m = re.search(r"^\s*#?\s*OPENROUTER_API_KEY\s*=\s*\"?([^\"\s#]+)", env.read_text(encoding="utf-8"), re.M)
        if m:
            return m.group(1)
    return None


def send_telegram(text: str) -> None:
    if not TELEGRAM_BOT_TOKEN or not CHAT_ID:
        print("[openrouter] Falta TELEGRAM_BOT_TOKEN o TELEGRAM_ALLOWED_USER_ID en .env", file=sys.stderr)
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": CHAT_ID, "text": text}).encode()
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=data), timeout=20) as resp:
            resp.read()
    except Exception as e:
        print(f"[openrouter] Error enviando a Telegram: {e}", file=sys.stderr)


def main() -> int:
    siempre = "--siempre" in sys.argv
    clave = clave_openrouter()
    if not clave:
        print("[openrouter] No hay OPENROUTER_API_KEY", file=sys.stderr)
        send_telegram("🔴 No encuentro la clave de OpenRouter para mirar el saldo (Alacena: tickets).")
        return 0
    try:
        req = urllib.request.Request("https://openrouter.ai/api/v1/credits", headers={"Authorization": f"Bearer {clave}"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            datos = json.load(resp)["data"]
    except Exception as e:
        print(f"[openrouter] No se pudo consultar el saldo: {e}", file=sys.stderr)
        send_telegram(f"🔴 No he podido consultar el saldo de OpenRouter ({e}). Si la clave ha caducado, la lectura de tickets de Alacena estará en mantenimiento.")
        return 0

    saldo = float(datos["total_credits"]) - float(datos["total_usage"])
    print(f"[openrouter] Saldo: {saldo:.2f} $ (umbral {UMBRAL:.2f} $)")
    if saldo < UMBRAL or siempre:
        icono = "🟠" if saldo > 0 else "🔴"
        estado = (
            "Con 0 $ la lectura de tickets de Alacena pasa a «en mantenimiento»."
            if saldo > 0
            else "Ya está a 0: la lectura de tickets de Alacena está en mantenimiento."
        )
        send_telegram(
            f"{icono} Saldo de OpenRouter: {saldo:.2f} $ (aviso por debajo de {UMBRAL:.2f} $).\n"
            f"{estado}\nRecarga: https://openrouter.ai/settings/credits"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
