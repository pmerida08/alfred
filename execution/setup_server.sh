#!/bin/bash
# Configura Alfred como servicio de usuario en el servidor Linux.
# Ejecutar UNA SOLA VEZ tras clonar/sincronizar el proyecto:
#   bash ~/Documentos/alfred/execution/setup_server.sh

set -e

ALFRED_DIR="/home/pablo/Documentos/Alfred"
SERVICE_DIR="$HOME/.config/systemd/user"
SERVICE_FILE="$SERVICE_DIR/alfred.service"

echo "==> Configurando Alfred en el servidor..."

# Permisos de ejecución
chmod +x "$ALFRED_DIR/execution/alfred_start.sh"
chmod +x "$ALFRED_DIR/execution/heartbeat.sh"

# Crear directorio de servicios de usuario si no existe
mkdir -p "$SERVICE_DIR"

# Crear el servicio systemd
cat > "$SERVICE_FILE" <<EOF
[Unit]
Description=Alfred - Asistente Personal
After=network.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=$ALFRED_DIR/execution/alfred_start.sh

[Install]
WantedBy=default.target
EOF

# Habilitar e iniciar el servicio
systemctl --user daemon-reload
systemctl --user enable alfred.service
systemctl --user start alfred.service

# Asegurar que el servicio arranca sin sesión activa
loginctl enable-linger "$USER"

echo ""
echo "✓ Alfred configurado y corriendo."
echo "  Para conectarte a Alfred:  tmux attach -t alfred"
echo "  Estado del servicio:       systemctl --user status alfred"
echo "  Logs:                      journalctl --user -u alfred -f"
