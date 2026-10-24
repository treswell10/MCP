import sqlite3
from contextlib import closing
from pathlib import Path

DB_PATH = Path(__file__).resolve().with_name("notes.db")


def _connect() -> sqlite3.Connection:
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
    with closing(_connect()) as conn, conn:
        rows = conn.execute(
            "SELECT id, content, created_at FROM notes ORDER BY id DESC"
        ).fetchall()
        return [dict(row) for row in rows]


def delete_note(note_id: int) -> bool:
    with closing(_connect()) as conn, conn:
        cursor = conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        return cursor.rowcount > 0


if __name__ == "__main__":
    import json
    import sys

    usage = "Usage: python notes_db.py add <text> | list | delete <id>"
    if len(sys.argv) < 2:
        raise SystemExit(usage)

    command = sys.argv[1]
    if command == "add":
        if len(sys.argv) < 3:
            raise SystemExit(usage)
        print(json.dumps(add_note(" ".join(sys.argv[2:]))))
    elif command == "list":
        print(json.dumps(list_notes(), indent=2))
    elif command == "delete":
        if len(sys.argv) < 3:
            raise SystemExit(usage)
        print(json.dumps(delete_note(int(sys.argv[2]))))
    else:
        raise SystemExit(usage)