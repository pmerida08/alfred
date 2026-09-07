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
# Buzón de salida de HUNTER: los ficheros que deje aquí (CV, cartas) se
# adjuntan al chat tras la respuesta de texto y luego se borran.
HUNTER_OUTBOX = TMP_DIR / "hunter_outbox"

WHISPER_MODEL = "small"  # opciones: tiny, base, small, medium, large


def strip_markdown(text: str) -> str:
    """Convierte Markdown a texto plano legible para Telegram sin parse_mode."""
    text = re.sub(r"```[a-zA-Z]*\n?", "", text)
    text = re.sub(r"```", "", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"__(.+?)__", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"_(.+?)_", r"\1", text)
    text = re.sub(r"~~(.+?)~~", r"\1", text)
    lines = text.splitlines()
    clean_lines = []
    for line in lines:
        stripped = line.strip()
        if re.match(r"^\|?[\s\-:]+(\|[\s\-:]+)+\|?$", stripped):
            continue
        if "|" in stripped:
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            clean_lines.append("  ".join(cells))
        else:
            clean_lines.append(line)
    text = "\n".join(clean_lines)
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
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
    Si session_id ya no existe en Claude (sesión expirada), reintenta sin --resume.
    """
    import platform
    if platform.system() == "Windows":
        claude_bin = r"C:\Users\pablo\.local\bin\claude.exe"
    else:
        claude_bin = "/home/pablo/.nvm/versions/node/v20.20.2/bin/claude"

    async def _call(sid: str | None) -> tuple[str, str]:
        cmd = [claude_bin, "-p", message, "--output-format", "json", "--dangerously-skip-permissions"]
        if sid:
            cmd += ["--resume", sid]

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(PROJECT_ROOT),
        )
        stdout, stderr = await proc.communicate()

        raw = stdout.decode("utf-8").strip()
        if not raw:
            err = stderr.decode("utf-8").strip()
            print(f"[alfred] CLI falló — returncode={proc.returncode}, stderr={err!r}", file=sys.stderr)
            raise RuntimeError(err or f"Sin respuesta del CLI (exit {proc.returncode})")

        data = json.loads(raw)
        if data.get("is_error"):
            raise RuntimeError(data.get("result", "Error desconocido"))

        return data["result"], data["session_id"]

    try:
        return await _call(session_id)
    except Exception as e:
        # Si la sesión de Claude expiró, reintentar sin --resume
        if session_id and ("session" in str(e).lower() or "not found" in str(e).lower()):
            print(f"[alfred] Sesión {session_id} expirada, iniciando nueva.", file=sys.stderr)
            return await _call(None)
        raise


async def send_outbox_files(update) -> None:
    """Envía como documentos los ficheros que HUNTER haya dejado en el outbox y los borra.

    Decoupla el bot de la skill: cualquier respuesta puede traer adjuntos sin que
    el bot tenga que parsear el texto. Solo actúa si hay ficheros pendientes.
    """
    if not HUNTER_OUTBOX.exists():
        return
    files = sorted(p for p in HUNTER_OUTBOX.iterdir() if p.is_file())
    for f in files:
        try:
            with f.open("rb") as fh:
                await update.message.reply_document(document=fh, filename=f.name)
        except Exception as e:
            print(f"[outbox] error enviando {f.name}: {e}", file=sys.stderr)
        finally:
            try:
                f.unlink()
            except Exception:
                pass


def _format_dt(iso: str) -> str:
    """Formatea timestamp ISO a 'DD/MM/YY HH:MM'."""
    try:
        dt = __import__("datetime").datetime.fromisoformat(iso)
        return dt.strftime("%d/%m/%y %H:%M")
    except Exception:
        return iso[:16]


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

    sys.path.insert(0, str(PROJECT_ROOT))
    from execution import conversation_store as store
    store.init_db()

    TMP_DIR.mkdir(exist_ok=True)
    whisper_model = load_whisper_model()

    async def is_authorized(update: Update) -> bool:
        user_id = update.effective_user.id if update.effective_user else None
        if ALLOWED_USER_ID is None:
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
        conv = store.get_or_create_active_conversation(chat_id)

        store.save_message(conv.id, "user", user_text, update.message.message_id)

        stop_typing = asyncio.Event()
        typing_task = asyncio.create_task(keep_typing(update.message.chat, stop_typing))

        try:
            response, new_session_id = await ask_alfred(user_text, conv.claude_session_id)
            store.update_claude_session(conv.id, new_session_id)
        except Exception as e:
            response = f"Error: {e}"
            new_session_id = None
        finally:
            stop_typing.set()
            typing_task.cancel()

        store.save_message(conv.id, "assistant", response)

        response = strip_markdown(response)
        for i in range(0, max(len(response), 1), 4096):
            await update.message.reply_text(response[i:i + 4096])

        await send_outbox_files(update)

    async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await is_authorized(update): return
        chat_id = update.effective_chat.id
        conv = store.new_conversation(chat_id)
        print(f"[alfred] /start — nueva conversación {conv.id}")
        await update.message.reply_text("Alfred operativo.")

    async def cmd_reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await is_authorized(update): return
        chat_id = update.effective_chat.id
        conv = store.new_conversation(chat_id)
        print(f"[alfred] /reset — nueva conversación {conv.id}")
        await update.message.reply_text("Conversación reiniciada.")

    async def cmd_new(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await is_authorized(update): return
        chat_id = update.effective_chat.id
        conv = store.new_conversation(chat_id)
        print(f"[alfred] /new — nueva conversación {conv.id}")
        await update.message.reply_text(f"Sesión nueva [{conv.id}]. Contexto borrado.")

    async def cmd_compact(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await is_authorized(update): return
        chat_id = update.effective_chat.id
        conv = store.get_active_conversation(chat_id)
        if not conv or not conv.claude_session_id:
            await update.message.reply_text("No hay sesión activa. Escribe algo primero.")
            return

        stop_typing = asyncio.Event()
        typing_task = asyncio.create_task(keep_typing(update.message.chat, stop_typing))
        try:
            _, new_session_id = await ask_alfred("/compact", conv.claude_session_id)
            store.update_claude_session(conv.id, new_session_id)
            await update.message.reply_text("Sesión compactada. El contexto se ha resumido.")
        except Exception as e:
            await update.message.reply_text(f"Error al compactar: {e}")
        finally:
            stop_typing.set()
            typing_task.cancel()

    async def cmd_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Lista las últimas conversaciones con su ID y fecha."""
        if not await is_authorized(update): return
        chat_id = update.effective_chat.id

        # Nº opcional como argumento: /history 5
        limit = 5
        if context.args:
            try:
                limit = max(1, min(int(context.args[0]), 20))
            except ValueError:
                pass

        convs = store.get_recent_conversations(chat_id, limit=limit)
        if not convs:
            await update.message.reply_text("Sin historial todavía.")
            return

        active = store.get_active_conversation(chat_id)
        lines = [f"Ultimas {len(convs)} conversaciones:\n"]
        for c in convs:
            marker = " <activa>" if active and c.id == active.id else ""
            msgs = store.get_conversation_messages(c.id)
            n = len(msgs)
            lines.append(f"[{c.id}] {_format_dt(c.started_at)}  ({n} mensajes){marker}")
        await update.message.reply_text("\n".join(lines))

    async def cmd_recall(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Busca en el historial. Uso: /recall <texto>"""
        if not await is_authorized(update): return
        if not context.args:
            await update.message.reply_text("Uso: /recall <texto a buscar>")
            return

        chat_id = update.effective_chat.id
        query = " ".join(context.args)
        results = store.search_messages(chat_id, query, limit=5)

        if not results:
            await update.message.reply_text(f'Sin resultados para "{query}".')
            return

        lines = [f'Encontrado "{query}" en {len(results)} mensaje(s):\n']
        for msg, conv_started in results:
            role_label = "Tu" if msg.role == "user" else "Alfred"
            snippet = msg.content[:200].replace("\n", " ")
            if len(msg.content) > 200:
                snippet += "..."
            lines.append(
                f"[{msg.conversation_id}] {_format_dt(msg.sent_at)} — {role_label}:\n{snippet}\n"
            )
        await update.message.reply_text("\n".join(lines))

    async def cmd_buscar_trabajo(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Lanza la búsqueda de empleo de HUNTER. Uso: /buscar_trabajo [filtros]"""
        if not await is_authorized(update): return
        print("[alfred] /buscar_trabajo")
        prompt = (
            "Busca ofertas de empleo que encajen con mi perfil y genérame el paquete "
            "de candidatura por cada una (delega en HUNTER, directiva buscar_ofertas)."
        )
        extra = " ".join(context.args).strip() if context.args else ""
        if extra:
            prompt += f" Criterios: {extra}."
        await reply_to(update, prompt)

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

    async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await is_authorized(update): return

        photo = update.message.photo[-1]
        image_path = TMP_DIR / f"food_{update.message.message_id}.jpg"

        stop_typing = asyncio.Event()
        typing_task = asyncio.create_task(keep_typing(update.message.chat, stop_typing))

        try:
            file = await context.bot.get_file(photo.file_id)
            await file.download_to_drive(image_path)

            sys.path.insert(0, str(PROJECT_ROOT))
            from execution.food_log import log_food
            data = await asyncio.get_event_loop().run_in_executor(None, log_food, image_path)

            response = (
                f"Registrado en Google Sheets.\n\n"
                f"{data.get('nombre', 'Comida')}\n"
                f"Calorias: {data.get('calorias', '?')} kcal\n"
                f"Proteinas: {data.get('proteinas_g', '?')} g\n"
                f"Carbohidratos: {data.get('carbohidratos_g', '?')} g\n"
                f"Grasas: {data.get('grasas_g', '?')} g"
            )
            if data.get("notas"):
                response += f"\nNota: {data['notas']}"

        except Exception as e:
            response = f"Error al registrar la comida: {e}"
            print(f"[food_log error] {e}")
        finally:
            stop_typing.set()
            typing_task.cancel()
            if image_path.exists():
                image_path.unlink()

        await update.message.reply_text(response)

    app = (
        ApplicationBuilder()
        .token(TELEGRAM_BOT_TOKEN)
        .read_timeout(60)
        .write_timeout(60)
        .connect_timeout(30)
        .build()
    )
    app.add_handler(CommandHandler("start",   cmd_start))
    app.add_handler(CommandHandler("reset",   cmd_reset))
    app.add_handler(CommandHandler("new",     cmd_new))
    app.add_handler(CommandHandler("compact", cmd_compact))
    app.add_handler(CommandHandler("history", cmd_history))
    app.add_handler(CommandHandler("recall",  cmd_recall))
    app.add_handler(CommandHandler("buscar_trabajo", cmd_buscar_trabajo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("Alfred — Telegram bot iniciado. Ctrl+C para detener.")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
