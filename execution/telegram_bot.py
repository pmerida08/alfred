"""
Alfred — Bot de Telegram.
Recibe mensajes de texto y voz de Pablo, los procesa via Claude Code CLI y responde.
Claude Code CLI tiene acceso a todos los MCP servers (Gmail, Calendar, Notion, etc.)

Uso: python execution/telegram_bot.py
Detener: Ctrl+C
"""

import asyncio
import json
import os
import re
import sys
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).parent.parent
load_dotenv(PROJECT_ROOT / ".env", override=True)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
_allowed_raw = os.getenv("TELEGRAM_ALLOWED_USER_ID", "").strip()
ALLOWED_USER_ID: int | None = int(_allowed_raw) if _allowed_raw else None
TMP_DIR = PROJECT_ROOT / ".tmp"

WHISPER_MODEL = "small"  # opciones: tiny, base, small, medium, large


def strip_markdown(text: str) -> str:
    """Convierte Markdown a texto plano legible para Telegram sin parse_mode."""
    # Bloques de código (``` ... ```)
    text = re.sub(r"```[a-zA-Z]*\n?", "", text)
    text = re.sub(r"```", "", text)
    # Código inline
    text = re.sub(r"`([^`]+)`", r"\1", text)
    # Encabezados (# ## ###)
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    # Negrita e itálica (**text**, __text__, *text*, _text_)
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"__(.+?)__", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"_(.+?)_", r"\1", text)
    # Tachado (~~text~~)
    text = re.sub(r"~~(.+?)~~", r"\1", text)
    # Líneas de tabla: reemplazar separadores y pipes
    lines = text.splitlines()
    clean_lines = []
    for line in lines:
        stripped = line.strip()
        # Fila separadora de tabla (|---|---|)
        if re.match(r"^\|?[\s\-:]+(\|[\s\-:]+)+\|?$", stripped):
            continue
        # Fila de datos de tabla
        if "|" in stripped:
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            clean_lines.append("  ".join(cells))
        else:
            clean_lines.append(line)
    text = "\n".join(clean_lines)
    # Links [texto](url) → texto
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    # Limpiar líneas en blanco múltiples
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def load_whisper_model():
    try:
        import whisper
        print(f"Cargando modelo Whisper '{WHISPER_MODEL}'...")
        model = whisper.load_model(WHISPER_MODEL)
        print("Whisper listo.")
        return model
    except ImportError:
        print("ERROR: whisper no instalado. Ejecutar: pip install openai-whisper", file=sys.stderr)
        sys.exit(1)


def transcribe(whisper_model, audio_path: Path) -> str:
    result = whisper_model.transcribe(str(audio_path), language="es")
    return result["text"].strip()


async def ask_alfred(message: str, session_id: str | None = None) -> tuple[str, str]:
    """
    Llama a Claude Code CLI con el mensaje. Devuelve (respuesta, session_id).
    session_id permite retomar la conversación en el próximo mensaje.
    """
    import platform
    if platform.system() == "Windows":
        claude_bin = r"C:\Users\pablo\.local\bin\claude.exe"
    else:
        claude_bin = "/home/pablo/.nvm/versions/node/v20.20.2/bin/claude"
    cmd = [claude_bin, "-p", message, "--output-format", "json", "--dangerously-skip-permissions"]
    if session_id:
        cmd += ["--resume", session_id]

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=str(PROJECT_ROOT),
    )
    stdout, stderr = await proc.communicate()

    raw = stdout.decode("utf-8").strip()
    if not raw:
        raise RuntimeError(stderr.decode("utf-8") or "Sin respuesta del CLI")

    data = json.loads(raw)
    if data.get("is_error"):
        raise RuntimeError(data.get("result", "Error desconocido"))

    return data["result"], data["session_id"]


def main():
    if not TELEGRAM_BOT_TOKEN:
        print("ERROR: TELEGRAM_BOT_TOKEN no encontrado en .env", file=sys.stderr)
        sys.exit(1)

    try:
        from telegram import Update
        from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
    except ImportError:
        print("ERROR: python-telegram-bot no instalado. Ejecutar: pip install python-telegram-bot", file=sys.stderr)
        sys.exit(1)

    TMP_DIR.mkdir(exist_ok=True)
    whisper_model = load_whisper_model()
    chat_sessions: dict[int, str] = {}  # chat_id → session_id de Claude Code

    async def is_authorized(update: Update) -> bool:
        user_id = update.effective_user.id if update.effective_user else None
        if ALLOWED_USER_ID is None:
            # Sin restricción configurada: logear el ID para facilitar la configuración
            print(f"[AVISO] TELEGRAM_ALLOWED_USER_ID no configurado. Mensaje de user_id={user_id}")
            return True
        if user_id != ALLOWED_USER_ID:
            print(f"[BLOQUEADO] Intento de acceso de user_id={user_id}")
            await update.message.reply_text("No autorizado.")
            return False
        return True

    async def keep_typing(chat, stop_event: asyncio.Event):
        while not stop_event.is_set():
            await chat.send_action("typing")
            await asyncio.sleep(4)

    async def reply_to(update: Update, user_text: str):
        chat_id = update.effective_chat.id
        session_id = chat_sessions.get(chat_id)

        stop_typing = asyncio.Event()
        typing_task = asyncio.create_task(keep_typing(update.message.chat, stop_typing))

        try:
            response, new_session_id = await ask_alfred(user_text, session_id)
            chat_sessions[chat_id] = new_session_id
        except Exception as e:
            response = f"Error: {e}"
        finally:
            stop_typing.set()
            typing_task.cancel()

        # Telegram limita mensajes a 4096 caracteres
        response = strip_markdown(response)
        for i in range(0, max(len(response), 1), 4096):
            await update.message.reply_text(response[i:i + 4096])

    async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await is_authorized(update): return
        chat_sessions.pop(update.effective_chat.id, None)
        await update.message.reply_text("Alfred operativo.")

    async def cmd_reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await is_authorized(update): return
        chat_sessions.pop(update.effective_chat.id, None)
        await update.message.reply_text("Conversación reiniciada.")

    async def cmd_new(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await is_authorized(update): return
        chat_sessions.pop(update.effective_chat.id, None)
        await update.message.reply_text("Sesión nueva. Contexto borrado.")

    async def cmd_compact(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await is_authorized(update): return
        chat_id = update.effective_chat.id
        session_id = chat_sessions.get(chat_id)
        if not session_id:
            await update.message.reply_text("No hay sesión activa. Escribe algo primero.")
            return

        stop_typing = asyncio.Event()
        typing_task = asyncio.create_task(keep_typing(update.message.chat, stop_typing))
        try:
            _, new_session_id = await ask_alfred("/compact", session_id)
            chat_sessions[chat_id] = new_session_id
            await update.message.reply_text("Sesión compactada. El contexto se ha resumido.")
        except Exception as e:
            await update.message.reply_text(f"Error al compactar: {e}")
        finally:
            stop_typing.set()
            typing_task.cancel()

    async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await is_authorized(update): return
        await reply_to(update, update.message.text)

    async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await is_authorized(update): return
        voice = update.message.voice

        audio_path = TMP_DIR / f"voice_{update.message.message_id}.ogg"
        try:
            file = await context.bot.get_file(voice.file_id)
            await file.download_to_drive(audio_path)
            text = transcribe(whisper_model, audio_path)
            print(f"[voz transcrita] {text}")
            await reply_to(update, text)
        finally:
            if audio_path.exists():
                audio_path.unlink()

    app = (
        ApplicationBuilder()
        .token(TELEGRAM_BOT_TOKEN)
        .read_timeout(60)
        .write_timeout(60)
        .connect_timeout(30)
        .build()
    )
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("reset", cmd_reset))
    app.add_handler(CommandHandler("new", cmd_new))
    app.add_handler(CommandHandler("compact", cmd_compact))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))

    print("Alfred — Telegram bot iniciado. Ctrl+C para detener.")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
