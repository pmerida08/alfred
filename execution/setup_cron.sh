#!/bin/bash
# Configura los cron jobs de Alfred en el servidor.
# Ejecutar UNA VEZ en el servidor: bash setup_cron.sh

ALFRED_DIR="$(cd "$(dirname "$0")/.." && pwd)"
HEARTBEAT="$ALFRED_DIR/execution/heartbeat.sh"

chmod +x "$HEARTBEAT"

# Leer crontab actual y añadir las líneas de Alfred si no existen
CRONTAB_CURRENT=$(crontab -l 2>/dev/null || echo "")
MARKER="# Alfred HEARTBEAT"

if echo "$CRONTAB_CURRENT" | grep -q "$MARKER"; then
  echo "Los cron jobs de Alfred ya están configurados."
  exit 0
fi

CRONTAB_NEW="$CRONTAB_CURRENT

$MARKER
0 7  * * * $HEARTBEAT email          >> $ALFRED_DIR/.tmp/heartbeat.log 2>&1
0 8  * * * $HEARTBEAT agenda         >> $ALFRED_DIR/.tmp/heartbeat.log 2>&1
0 9  * * * $HEARTBEAT token          >> $ALFRED_DIR/.tmp/heartbeat.log 2>&1
0 12 * * 0 $HEARTBEAT buscar_trabajo >> $ALFRED_DIR/.tmp/heartbeat.log 2>&1
0 23 * * * $HEARTBEAT dreaming       >> $ALFRED_DIR/.tmp/heartbeat.log 2>&1
"

echo "$CRONTAB_NEW" | crontab -

echo "Cron jobs configurados:"
crontab -l | grep -A4 "$MARKER"
