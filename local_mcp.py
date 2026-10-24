from fastmcp import FastMCP
from notes_db import (
    add_note as save_note,
    delete_note as remove_note,
    list_notes as fetch_notes,
)

mcp = FastMCP("notes")


@mcp.tool
def add_note(content: str) -> dict:
    """Save a note and return its ID, content, and creation time."""
    return save_note(content)


@mcp.tool
def list_notes() -> list[dict]:
    """List saved notes, newest first."""
    return fetch_notes()


@mcp.tool
def delete_note(note_id: int) -> bool:
    """Delete a note by ID. Return false if no note had that ID."""
    return remove_note(note_id)


if __name__ == "__main__":
    mcp.run()