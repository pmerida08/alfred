#!/usr/bin/env bash
# SessionStart (solo en el PC Windows): pide ordenar la bandeja de Gmail en la
# primera sesión del día. El resto de sesiones del día arrancan sin ese paso.
case "$(uname -s)" in MINGW*|MSYS*|CYGWIN*) ;; *) echo '{}'; exit 0 ;; esac
sello="${CLAUDE_PROJECT_DIR:-.}/.tmp/.bandeja_ultima"
hoy=$(date +%F)
if [ "$(cat "$sello" 2>/dev/null)" = "$hoy" ]; then echo '{}'; exit 0; fi
mkdir -p "$(dirname "$sello")" && echo "$hoy" > "$sello"
echo '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"Primera sesion del dia: antes de responder a Pablo, ordena su bandeja de Gmail segun directives/ordenar_bandeja.md (solo etiquetar y archivar). Resume el resultado en una o dos lineas y luego atiende su peticion."}}'
