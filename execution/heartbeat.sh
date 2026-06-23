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

# Cargar variables de entorno.
# Ignora líneas de comentario, líneas vacías y comentarios inline (" #...").
# No-fatal: un .env con formato raro no debe abortar el HEARTBEAT (set -e).
if [ -f "$ALFRED_DIR/.env" ]; then
  export $(grep -v '^#' "$ALFRED_DIR/.env" | grep -v '^$' | sed 's/[[:space:]]#.*//' | xargs) 2>/dev/null || true
fi

# Python del virtualenv de Alfred (fallback al python3 del sistema).
# Se usa el binario directo en vez de 'source activate' para no depender de
# rutas relativas frágiles.
ALFRED_PY="python3"
for cand in "$HOME/alfred-venv/bin/python3" "$ALFRED_DIR/../alfred-venv/bin/python3"; do
  if [ -x "$cand" ]; then ALFRED_PY="$cand"; break; fi
done

case "$TASK" in
  dreaming)
    # Dreaming usa script Python directo (sin necesidad de Claude CLI)
    "$ALFRED_PY" "$ALFRED_DIR/execution/memory_dreaming.py" >> "$LOG_FILE" 2>&1
    ;;
  token)
    # Sonda de salud de la auth de Claude Code. El script invoca el CLI y, si la
    # autenticación falla (401), avisa por Telegram con la API HTTP directa (no
    # depende del CLI para el aviso).
    "$ALFRED_PY" "$ALFRED_DIR/execution/check_token_expiry.py" >> "$LOG_FILE" 2>&1
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
