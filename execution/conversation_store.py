"""
Alfred — Almacén de conversaciones SQLite.
Persiste sesiones y mensajes para que el historial sobreviva reinicios del bot.
"""

import sqlite3
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(__file__).parent / "alfred_history.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS conversations (
    id          TEXT PRIMARY KEY,
    chat_id     INTEGER NOT NULL,
    claude_session_id TEXT,
    started_at  TEXT NOT NULL,
    last_active_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS messages (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id     TEXT NOT NULL REFERENCES conversations(id),
    role                TEXT NOT NULL,
    content             TEXT NOT NULL,
    telegram_message_id INTEGER,
    sent_at             TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_conv_chat_id  ON conversations(chat_id, last_active_at DESC);
CREATE INDEX IF NOT EXISTS idx_msg_conv_id   ON messages(conversation_id, sent_at);
CREATE INDEX IF NOT EXISTS idx_msg_content   ON messages(content);
"""


@dataclass
class Conversation:
    id: str
    chat_id: int
    claude_session_id: str | None
    started_at: str
    last_active_at: str


@dataclass
class Message:
    id: int
    conversation_id: str
    role: str
    content: str
    telegram_message_id: int | None
    sent_at: str


@contextmanager
def _conn():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA journal_mode=WAL")
    try:
        yield con
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()


def init_db():
    with _conn() as con:
        con.executescript(SCHEMA)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _short_id() -> str:
    return uuid.uuid4().hex[:8]


# --- Conversations ---

def get_active_conversation(chat_id: int) -> Conversation | None:
    with _conn() as con:
        row = con.execute(
            "SELECT * FROM conversations WHERE chat_id=? ORDER BY last_active_at DESC LIMIT 1",
            (chat_id,),
        ).fetchone()
        return Conversation(**dict(row)) if row else None


def get_or_create_active_conversation(chat_id: int) -> Conversation:
    conv = get_active_conversation(chat_id)
    if conv:
        return conv
    return new_conversation(chat_id)


def new_conversation(chat_id: int) -> Conversation:
    conv = Conversation(
        id=_short_id(),
        chat_id=chat_id,
        claude_session_id=None,
        started_at=_now(),
        last_active_at=_now(),
    )
    with _conn() as con:
        con.execute(
            "INSERT INTO conversations VALUES (?,?,?,?,?)",
            (conv.id, conv.chat_id, conv.claude_session_id, conv.started_at, conv.last_active_at),
        )
    return conv


def update_claude_session(conversation_id: str, claude_session_id: str):
    with _conn() as con:
        con.execute(
            "UPDATE conversations SET claude_session_id=?, last_active_at=? WHERE id=?",
            (claude_session_id, _now(), conversation_id),
        )


def touch_conversation(conversation_id: str):
    with _conn() as con:
        con.execute(
            "UPDATE conversations SET last_active_at=? WHERE id=?",
            (_now(), conversation_id),
        )


def get_recent_conversations(chat_id: int, limit: int = 10) -> list[Conversation]:
    with _conn() as con:
        rows = con.execute(
            "SELECT * FROM conversations WHERE chat_id=? ORDER BY last_active_at DESC LIMIT ?",
            (chat_id, limit),
        ).fetchall()
        return [Conversation(**dict(r)) for r in rows]


# --- Messages ---

def save_message(
    conversation_id: str,
    role: str,
    content: str,
    telegram_message_id: int | None = None,
) -> Message:
    now = _now()
    with _conn() as con:
        cur = con.execute(
            "INSERT INTO messages (conversation_id, role, content, telegram_message_id, sent_at) VALUES (?,?,?,?,?)",
            (conversation_id, role, content, telegram_message_id, now),
        )
        return Message(
            id=cur.lastrowid,
            conversation_id=conversation_id,
            role=role,
            content=content,
            telegram_message_id=telegram_message_id,
            sent_at=now,
        )


def get_conversation_messages(conversation_id: str) -> list[Message]:
    with _conn() as con:
        rows = con.execute(
            "SELECT * FROM messages WHERE conversation_id=? ORDER BY sent_at",
            (conversation_id,),
        ).fetchall()
        return [Message(**dict(r)) for r in rows]


def search_messages(chat_id: int, query: str, limit: int = 5) -> list[tuple[Message, str]]:
    """Busca en el historial. Devuelve lista de (Message, conversation_id)."""
    q = f"%{query.lower()}%"
    with _conn() as con:
        rows = con.execute(
            """
            SELECT m.*, c.id as cid, c.started_at as conv_started
            FROM messages m
            JOIN conversations c ON m.conversation_id = c.id
            WHERE c.chat_id=? AND LOWER(m.content) LIKE ?
            ORDER BY m.sent_at DESC
            LIMIT ?
            """,
            (chat_id, q, limit),
        ).fetchall()
        result = []
        for r in rows:
            d = dict(r)
            msg = Message(
                id=d["id"],
                conversation_id=d["conversation_id"],
                role=d["role"],
                content=d["content"],
                telegram_message_id=d["telegram_message_id"],
                sent_at=d["sent_at"],
            )
            result.append((msg, d["conv_started"]))
        return result


def get_last_n_messages(chat_id: int, n: int = 20, exclude_conversation_id: str | None = None) -> list[Message]:
    """Devuelve los últimos N mensajes del historial (todas las conversaciones)."""
    with _conn() as con:
        query = """
            SELECT m.* FROM messages m
            JOIN conversations c ON m.conversation_id = c.id
            WHERE c.chat_id=?
        """
        params: list = [chat_id]
        if exclude_conversation_id:
            query += " AND m.conversation_id != ?"
            params.append(exclude_conversation_id)
        query += " ORDER BY m.sent_at DESC LIMIT ?"
        params.append(n)
        rows = con.execute(query, params).fetchall()
        return list(reversed([Message(**dict(r)) for r in rows]))
