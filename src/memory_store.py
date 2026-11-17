
import sqlite3
import re
from pathlib import Path

DB = Path(__file__).resolve().parents[1] / "memory" / "chat_history.db"


def _connect():
    DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS personal_memory (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    """)

    return conn


def save_message(role, content):
    with _connect() as conn:
        conn.execute(
            "INSERT INTO messages(role, content) VALUES (?, ?)",
            (role, content)
        )


def load_history(limit=100):
    with _connect() as conn:
        rows = conn.execute(
            "SELECT role, content FROM messages ORDER BY id DESC LIMIT ?",
            (limit,)
        ).fetchall()

    return [{"role": r, "content": c} for r, c in reversed(rows)]


def clear_history():
    with _connect() as conn:
        conn.execute("DELETE FROM messages")


def save_fact(key, value):
    with _connect() as conn:
        conn.execute("""
            INSERT OR REPLACE INTO personal_memory(key, value)
            VALUES (?, ?)
        """, (key, value))


def load_facts():
    with _connect() as conn:
        rows = conn.execute(
            "SELECT key, value FROM personal_memory"
        ).fetchall()

    return dict(rows)


def remember_from_message(message):
    patterns = {
        "name": r"\bmy name is ([A-Za-z][A-Za-z ]*)",
        "favourite programming language":
            r"\bmy favourite programming language is ([A-Za-z+#. ]+)",
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, message, re.IGNORECASE)

        if match:
            value = match.group(1).strip().rstrip(" .!?")
            if value:
                save_fact(key, value)


def format_memory():
    facts = load_facts()

    if not facts:
        return "No personal information has been saved yet."

    return "\n".join(
        f"- {key}: {value}" for key, value in facts.items()
    )
