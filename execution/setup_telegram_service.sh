#!/bin/bash
# Instala el bot de Telegram de Alfred como servicio systemd de usuario.
# Ejecutar UNA VEZ en el servidor: bash ~/Documentos/Alfred/execution/setup_telegram_service.sh

set -e

ALFRED_DIR="/home/pablo/Documentos/Alfred"
SERVICE_DIR="$HOME/.config/systemd/user"
SERVICE_FILE="$SERVICE_DIR/alfred-telegram.service"
VENV="$HOME/alfred-venv"
PYTHON="$VENV/bin/python3"

# Usar python del venv si existe, si no el del sistema
if [ ! -f "$PYTHON" ]; then
  PYTHON=$(which python3)
fi

mkdir -p "$SERVICE_DIR"

cat > "$SERVICE_FILE" <<EOF
[Unit]
Description=Alfred - Telegram Bot
After=network.target

[Service]
Type=simple
WorkingDirectory=$ALFRED_DIR
ExecStart=$PYTHON $ALFRED_DIR/execution/telegram_bot.py
Restart=always
RestartSec=10
EnvironmentFile=$ALFRED_DIR/.env

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable alfred-telegram.service
systemctl --user restart alfred-telegram.service

loginctl enable-linger "$USER"

echo ""
echo "✓ Bot de Telegram activo."
echo "  Estado:  systemctl --user status alfred-telegram"
echo "  Logs:    journalctl --user -u alfred-telegram -f"
