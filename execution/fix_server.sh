#!/usr/bin/env bash
# fix_server.sh — Diagnóstico y reparación del Claude CLI en el servidor Linux
# Ejecutar en el servidor: bash /home/pablo/Documentos/Alfred/execution/fix_server.sh

set -euo pipefail

CLAUDE_BIN="/home/pablo/.nvm/versions/node/v20.20.2/bin/claude"
CLAUDE_SETTINGS="$HOME/.claude/settings.json"
PROJECT_DIR="/home/pablo/Documentos/Alfred"

echo "====== DIAGNÓSTICO ALFRED ======"
echo ""

# 1. Verificar que el binario existe
echo "▸ Binario Claude CLI: $CLAUDE_BIN"
if [[ ! -f "$CLAUDE_BIN" ]]; then
    echo "  ✗ NO EXISTE. Buscando otras versiones..."
    find "$HOME/.nvm/versions" -name "claude" -type f 2>/dev/null | head -5 || echo "  No se encontró ningún binario claude."
    echo ""
    echo "  → Solución: actualizar la ruta en execution/telegram_bot.py"
    echo "    Instalación: npm install -g @anthropic-ai/claude-code"
    echo ""
else
    echo "  ✓ Existe"
fi

echo ""

# 2. Versión
echo "▸ Versión del CLI:"
"$CLAUDE_BIN" --version 2>&1 || echo "  ✗ Fallo al obtener versión"
echo ""

# 3. Verificar settings globales
echo "▸ Settings globales ($CLAUDE_SETTINGS):"
if [[ -f "$CLAUDE_SETTINGS" ]]; then
    cat "$CLAUDE_SETTINGS"
else
    echo "  (no existe)"
fi
echo ""

# 4. Añadir bypassPermissionsModeAccepted si falta
echo "▸ Aplicando bypassPermissionsModeAccepted..."
if [[ -f "$CLAUDE_SETTINGS" ]]; then
    # Verificar si ya está presente
    if python3 -c "import json,sys; d=json.load(open('$CLAUDE_SETTINGS')); sys.exit(0 if d.get('bypassPermissionsModeAccepted') else 1)" 2>/dev/null; then
        echo "  ✓ Ya está configurado"
    else
        # Fusionar la clave existente con bypassPermissionsModeAccepted=true
        python3 - <<'PYEOF'
import json, os
path = os.path.expanduser("~/.claude/settings.json")
with open(path) as f:
    data = json.load(f)
data["bypassPermissionsModeAccepted"] = True
with open(path, "w") as f:
    json.dump(data, f, indent=2)
print("  ✓ Añadido bypassPermissionsModeAccepted: true")
PYEOF
    fi
else
    mkdir -p "$(dirname "$CLAUDE_SETTINGS")"
    echo '{"bypassPermissionsModeAccepted": true}' > "$CLAUDE_SETTINGS"
    echo "  ✓ Creado settings.json con bypassPermissionsModeAccepted: true"
fi
echo ""

# 5. Test rápido del CLI
echo "▸ Test rápido del CLI (timeout 30s):"
TEST_OUT=$(timeout 30 "$CLAUDE_BIN" -p "responde solo con: OK" \
    --output-format json \
    --dangerously-skip-permissions \
    2>&1) || true

if [[ -z "$TEST_OUT" ]]; then
    echo "  ✗ stdout vacío — posible problema de autenticación"
    echo ""
    echo "  → Ejecutar: $CLAUDE_BIN login"
    echo "    (abre navegador para autenticarse)"
else
    echo "  Respuesta: $TEST_OUT"
    if echo "$TEST_OUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print('  ✓ JSON válido — result:', d.get('result','?')[:80])" 2>/dev/null; then
        echo ""
        echo "  ✓ CLI funcionando correctamente"
    else
        echo "  ⚠ Respuesta no es JSON válido"
    fi
fi
echo ""

# 6. Reiniciar servicio
echo "▸ Reiniciando alfred.service..."
sudo systemctl restart alfred.service && echo "  ✓ Servicio reiniciado" || echo "  ✗ Error al reiniciar"
echo ""

echo "▸ Últimas líneas del log:"
journalctl -u alfred.service -n 20 --no-pager
echo ""
echo "====== FIN DEL DIAGNÓSTICO ======"
