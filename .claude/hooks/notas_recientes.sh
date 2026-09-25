#!/usr/bin/env bash
# SessionStart: mete en contexto las notas diarias de hoy y de ayer, para que
# Alfred no tenga que leerlas a mano en cada arranque.
dir="${CLAUDE_PROJECT_DIR:-.}/memory"
hoy=$(date +%F)
ayer=$(date -d yesterday +%F 2>/dev/null || date -v-1d +%F)
for d in "$ayer" "$hoy"; do
  f="$dir/$d.md"
  [ -f "$f" ] && { printf '\n<nota_diaria fecha="%s">\n' "$d"; cat "$f"; printf '\n</nota_diaria>\n'; }
done
exit 0
