import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parents[1] / "memory" / "chat_history.db"

def _connect():
    DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    return conn

def save_message(role, content):
    with _connect() as conn:
        conn.execute("INSERT INTO messages(role, content) VALUES (?, ?)", (role, content))

def load_history(limit=100):
    with _connect() as conn:
        rows = conn.execute(
            "SELECT role, content FROM messages ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return [{"role": r, "content": c} for r, c in reversed(rows)]

def clear_history():
    with _connect() as conn:
        conn.execute("DELETE FROM messages")
