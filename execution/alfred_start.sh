#!/bin/bash
# Inicia Alfred en una sesión tmux persistente.
# El servicio systemd llama a este script al arrancar el servidor.

ALFRED_DIR="/home/pablo/Documentos/Alfred"
SESSION="alfred"

if tmux has-session -t "$SESSION" 2>/dev/null; then
  echo "Alfred ya está corriendo en tmux session '$SESSION'."
  exit 0
fi

# Cargar variables de entorno
if [ -f "$ALFRED_DIR/.env" ]; then
  set -a
  source "$ALFRED_DIR/.env"
  set +a
fi

# Activar virtualenv si existe
if [ -f "$HOME/alfred-venv/bin/activate" ]; then
  source "$HOME/alfred-venv/bin/activate"
fi

# Activar venv para el bot
VENV_ACTIVATE="$HOME/alfred-venv/bin/activate"

# Ventana 0: Claude CLI
tmux new-session -d -s "$SESSION" -c "$ALFRED_DIR" -n "claude"
tmux send-keys -t "$SESSION:claude" "claude" Enter

# Ventana 1: Telegram bot
tmux new-window -t "$SESSION" -n "telegram" -c "$ALFRED_DIR"
if [ -f "$VENV_ACTIVATE" ]; then
  tmux send-keys -t "$SESSION:telegram" "source $VENV_ACTIVATE && python3 execution/telegram_bot.py" Enter
else
  tmux send-keys -t "$SESSION:telegram" "python3 execution/telegram_bot.py" Enter
fi

echo "Alfred iniciado. Conectar con: tmux attach -t $SESSION"
echo "  Ventana 'claude'   → Claude CLI"
echo "  Ventana 'telegram' → Telegram bot"
