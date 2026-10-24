"""SQLite persistence for notes used by the CLI and the MCP server."""

import sqlite3
from contextlib import closing
from pathlib import Path

DB_PATH = Path(__file__).resolve().with_name("notes.db")


def _connect() -> sqlite3.Connection:
    """Open notes.db, create the notes table if needed, and return a row-factory connection."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    return conn


def add_note(content: str) -> dict:
    """Insert a note and return its id, content, and created_at. Raises ValueError if content is empty."""
    content = content.strip()
    if not content:
        raise ValueError("Note content cannot be empty.")

    with closing(_connect()) as conn, conn:
        cursor = conn.execute(
            "INSERT INTO notes (content) VALUES (?)",
            (content,),
        )
        row = conn.execute(
            "SELECT id, content, created_at FROM notes WHERE id = ?",
            (cursor.lastrowid,),
        ).fetchone()
        return dict(row)


def list_notes() -> list[dict]:
    """Return all notes as dicts, newest first."""
    with closing(_connect()) as conn, conn:
        rows = conn.execute(
            "SELECT id, content, created_at FROM notes ORDER BY id DESC"
        ).fetchall()
        return [dict(row) for row in rows]


def delete_note(note_id: int) -> bool:
    """Delete the note with this id. Return True if a row was deleted."""
    with closing(_connect()) as conn, conn:
        cursor = conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        return cursor.rowcount > 0