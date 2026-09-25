# Directiva: FORGE — registro de comidas

## Flujo (automático)

1. Pablo manda una foto al bot de Telegram. **Toda foto se trata como comida**: el bot no distingue la intención.
2. `telegram_bot.py` la descarga y llama a `log_food()` de `execution/food_log.py`.
3. El script pide a Claude Code CLI (`claude -p`, con la suscripción, sin API key) el nombre del plato, las kcal y los gramos de proteína, carbohidratos y grasa.
4. Sube la foto a ImgBB (`IMGBB_API_KEY`) y añade una fila al Sheet.
5. En cada escritura borra las filas de más de 90 días y sus imágenes de ImgBB.
6. El bot contesta con el resumen de macros, o con el error si algo falla.

## Sheet

Spreadsheet `FOOD_LOG_SHEET_ID`, hoja `FOOD_LOG_SHEET_NAME` ("Comidas"; si falta la variable, el script usa "Hoja 1"). Columnas:

`Fecha | Hora | Comida | Calorías | Proteínas (g) | Carbohidratos (g) | Grasas (g) | Notas | Foto | Img ID`

La hoja "Resumen" se regenera con `python execution/setup_food_sheet.py --fix-resumen`. El Sheet está en locale español: al escribir fórmulas por API, separador `;` y funciones en español.

## Consultas

"¿Cuántas calorías llevo hoy?", "proteína de esta semana", "qué comí ayer": leer la hoja y agregar por fecha.

## Edge cases

- Foto ambigua (varios platos, borrosa): el script registra la mejor estimación y lo indica en Notas.
- Faltan variables en `.env` (`GOOGLE_SHEETS_CREDENTIALS_PATH`, `FOOD_LOG_SHEET_ID`, `IMGBB_API_KEY`): el script falla y el bot devuelve el error; decírselo a Pablo con la variable que falta.
