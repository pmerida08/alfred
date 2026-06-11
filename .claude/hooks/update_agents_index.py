#!/usr/bin/env python3
"""PostToolUse hook: añade un nuevo agente a agents/AGENTS.md cuando se crea su CLAUDE.md.

No-op si la ruta no coincide, si es un meta-agente, o si el agente ya está indexado.
"""
import json
import re
import sys
from pathlib import Path

META_AGENTS = {"explore", "general-purpose", "plan"}


def main() -> int:
    raw = sys.stdin.read()
    if not raw.strip():
        return 0

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return 0

    tool_input = payload.get("tool_input") or {}
    tool_response = payload.get("tool_response") or {}
    file_path = tool_input.get("file_path") or tool_response.get("filePath")
    if not file_path:
        return 0

    match = re.search(r"/agents/([^/]+)/CLAUDE\.md$", file_path)
    if not match:
        return 0

    name = match.group(1)
    if name in META_AGENTS:
        return 0

    agents_md = Path(file_path).parent.parent / "AGENTS.md"
    if not agents_md.exists():
        return 0

    contents = agents_md.read_text(encoding="utf-8")
    if f"[agents/{name}/]" in contents:
        return 0

    if not contents.endswith("\n"):
        contents += "\n"
    contents += f"| {name.upper()} — Pendiente de descripción | [agents/{name}/]({name}/CLAUDE.md) |\n"
    agents_md.write_text(contents, encoding="utf-8")

    print(json.dumps({
        "systemMessage": f"Agente {name} añadido a AGENTS.md. Refina la descripción cuando puedas."
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
