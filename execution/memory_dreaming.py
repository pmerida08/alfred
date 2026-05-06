"""
Consolidación nocturna de memoria (Dreaming).
Lee notas diarias de los últimos 7 días, extrae hechos relevantes
y los promueve a MEMORY.md y DREAMS.md.
"""

import os
import sys
from datetime import date, timedelta
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).parent.parent
MEMORY_DIR = PROJECT_ROOT / "memory"
MEMORY_FILE = PROJECT_ROOT / "MEMORY.md"
DREAMS_FILE = PROJECT_ROOT / "DREAMS.md"

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")


def read_daily_notes(days: int = 7) -> dict[str, str]:
    """Lee las notas diarias de los últimos N días."""
    notes = {}
    today = date.today()
    for i in range(days):
        day = today - timedelta(days=i)
        path = MEMORY_DIR / f"{day.isoformat()}.md"
        if path.exists():
            notes[day.isoformat()] = path.read_text(encoding="utf-8")
    return notes


def read_memory() -> str:
    """Lee el archivo MEMORY.md actual."""
    if MEMORY_FILE.exists():
        return MEMORY_FILE.read_text(encoding="utf-8")
    return ""


def consolidate_with_claude(notes: dict[str, str], existing_memory: str) -> dict:
    """
    Llama a la API de Anthropic para consolidar las notas.
    Devuelve: { "new_facts": [...], "themes": [...], "dreams_summary": str }
    """
    try:
        import anthropic
    except ImportError:
        print("ERROR: anthropic no instalado. Ejecutar: pip install anthropic", file=sys.stderr)
        sys.exit(1)

    if not ANTHROPIC_API_KEY:
        print("ERROR: ANTHROPIC_API_KEY no encontrado en .env", file=sys.stderr)
        sys.exit(1)

    notes_text = "\n\n---\n\n".join(
        f"### {date}\n{content}" for date, content in sorted(notes.items())
    )

    prompt = f"""Eres el sistema de consolidación de memoria de Alfred, un mayordomo digital personal.

Tienes acceso a las notas diarias de los últimos 7 días y a la memoria permanente actual.
Tu tarea es identificar qué información nueva merece ser promovida a la memoria permanente.

## Notas diarias (últimos 7 días)
{notes_text}

## Memoria permanente actual
{existing_memory}

## Tu tarea

Analiza las notas y responde en este formato JSON exacto:

{{
  "new_facts": [
    "Hecho nuevo que merece ser permanente (no duplicado con la memoria actual)"
  ],
  "themes": [
    "Tema o patrón identificado en las notas de esta semana"
  ],
  "dreams_summary": "Resumen narrativo de 3-5 líneas de lo más relevante de esta semana"
}}

Criterios para promover un hecho:
- Es una decisión de arquitectura o sistema
- Es una preferencia expresada por Pablo
- Es un error cometido que no debe repetirse
- Es un cambio relevante en el ecosistema de herramientas
- NO está ya en la memoria permanente

Sé selectivo. Mejor 2 hechos relevantes que 10 triviales."""

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    import json
    response_text = message.content[0].text
    # Extraer JSON de la respuesta
    start = response_text.find("{")
    end = response_text.rfind("}") + 1
    if start == -1 or end == 0:
        return {"new_facts": [], "themes": [], "dreams_summary": "Sin consolidación — respuesta no parseable."}
    return json.loads(response_text[start:end])


def update_memory(new_facts: list[str]) -> int:
    """Añade nuevos hechos a MEMORY.md. Devuelve el número de hechos añadidos."""
    if not new_facts:
        return 0

    today = date.today().isoformat()
    existing = read_memory()

    additions = "\n".join(f"- {fact}" for fact in new_facts)
    section = f"\n## Promovido el {today}\n\n{additions}\n"

    updated = existing + section
    MEMORY_FILE.write_text(updated, encoding="utf-8")
    return len(new_facts)


def update_dreams(themes: list[str], summary: str, notes_count: int, facts_count: int):
    """Actualiza DREAMS.md con el resultado de la consolidación."""
    today = date.today().isoformat()

    themes_text = "\n".join(f"- {t}" for t in themes) if themes else "- Sin temas identificados."

    entry = f"""
## Consolidación — {today}

**Notas procesadas:** {notes_count}
**Hechos promovidos a MEMORY.md:** {facts_count}

### Temas identificados

{themes_text}

### Resumen narrativo

{summary}

---
"""

    existing = DREAMS_FILE.read_text(encoding="utf-8") if DREAMS_FILE.exists() else "# DREAMS\n"

    # Insertar después del header
    header_end = existing.find("\n---")
    if header_end == -1:
        updated = existing + entry
    else:
        updated = existing[:header_end] + "\n---\n" + entry + existing[header_end + 4:]

    DREAMS_FILE.write_text(updated, encoding="utf-8")


def append_to_today(notes_count: int, facts_count: int):
    """Añade una línea de log a la nota del día."""
    today = date.today()
    path = MEMORY_DIR / f"{today.isoformat()}.md"
    line = f"\n- Dreaming ejecutado: {notes_count} notas procesadas, {facts_count} hechos promovidos.\n"
    if path.exists():
        with open(path, "a", encoding="utf-8") as f:
            f.write(line)
    else:
        path.write_text(f"# Notas — {today.isoformat()}\n{line}", encoding="utf-8")


def main():
    print("Iniciando consolidación nocturna (Dreaming)...")

    notes = read_daily_notes(days=7)
    if not notes:
        print("Sin notas en los últimos 7 días. Nada que consolidar.")
        update_dreams([], "Sin notas en los últimos 7 días.", 0, 0)
        return

    print(f"Notas encontradas: {len(notes)} días")
    existing_memory = read_memory()

    result = consolidate_with_claude(notes, existing_memory)

    facts_count = update_memory(result.get("new_facts", []))
    update_dreams(
        themes=result.get("themes", []),
        summary=result.get("dreams_summary", ""),
        notes_count=len(notes),
        facts_count=facts_count,
    )
    append_to_today(len(notes), facts_count)

    print(f"Consolidación completa: {facts_count} hechos promovidos a MEMORY.md")


if __name__ == "__main__":
    main()
