import json
import sys

from notes_db import add_note, delete_note, list_notes

usage = "Usage: python main.py add <text> | list | delete <id>"
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
