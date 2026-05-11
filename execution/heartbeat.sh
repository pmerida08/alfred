#!/bin/bash
# Ejecuta el HEARTBEAT de Alfred para la tarea indicada.
# Uso: heartbeat.sh [email|agenda|dreaming]

set -e

ALFRED_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="$ALFRED_DIR/.tmp"
mkdir -p "$LOG_DIR"

TASK="${1:-}"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
LOG_FILE="$LOG_DIR/heartbeat.log"

if [ -z "$TASK" ]; then
  echo "[$TIMESTAMP] ERROR: Tarea no especificada. Uso: heartbeat.sh [email|agenda|dreaming]" >> "$LOG_FILE"
  exit 1
fi

echo "[$TIMESTAMP] Iniciando HEARTBEAT: $TASK" >> "$LOG_FILE"

cd "$ALFRED_DIR"

# Cargar variables de entorno
if [ -f "$ALFRED_DIR/.env" ]; then
  export $(grep -v '^#' "$ALFRED_DIR/.env" | xargs)
fi

case "$TASK" in
  dreaming)
    # Dreaming usa script Python directo (sin necesidad de Claude CLI)
    source "$ALFRED_DIR/../alfred-venv/bin/activate" 2>/dev/null || true
    python3 "$ALFRED_DIR/execution/memory_dreaming.py" >> "$LOG_FILE" 2>&1
    ;;
  email|agenda)
    # Tareas que requieren Claude CLI
    if ! command -v claude &> /dev/null; then
      echo "[$TIMESTAMP] ERROR: claude CLI no encontrado en PATH" >> "$LOG_FILE"
      exit 1
    fi
    claude --print "HEARTBEAT: $TASK" >> "$LOG_FILE" 2>&1
    ;;
  *)
    echo "[$TIMESTAMP] ERROR: Tarea desconocida: $TASK" >> "$LOG_FILE"
    exit 1
    ;;
esac

echo "[$TIMESTAMP] HEARTBEAT $TASK completado." >> "$LOG_FILE"
