# Directiva — Aviso de saldo bajo en OpenRouter

## Objetivo
Que Pablo recargue OpenRouter antes de que se acabe el saldo. La lectura de tickets de
Alacena (y las imágenes de Estancia) lo gastan; si llega a 0, Alacena enseña «en
mantenimiento» en vez de leer tickets.

## Ejecución
- Script: `execution/check_openrouter_saldo.py`
- Disparador: cron diario → `heartbeat.sh openrouter` (09:05, servidor).
- Lógica: consulta `GET https://openrouter.ai/api/v1/credits`; si el saldo
  (`total_credits − total_usage`) baja de `OPENROUTER_SALDO_MINIMO` (2 $ por defecto),
  avisa por Telegram con la API HTTP directa. Por encima del umbral, solo deja el saldo en
  `.tmp/heartbeat.log`.
- Para probar el aviso: `python execution/check_openrouter_saldo.py --siempre`.

## Cuando salta el aviso
Recargar en https://openrouter.ai/settings/credits. Si Alacena ya está en mantenimiento,
vuelve sola en cuanto hay saldo (el mantenimiento por falta de saldo no se guarda). Si se
apagó a mano desde el panel (Planes → Lectura de tickets), hay que volver a activarla allí.

## Configuración
- `OPENROUTER_API_KEY` (en `.env`; la línea puede estar comentada, el script la lee igual).
- `OPENROUTER_SALDO_MINIMO` opcional, en dólares.
