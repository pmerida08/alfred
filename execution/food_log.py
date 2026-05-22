"""
FORGE — Food Logger
Analiza una foto de comida con visión (Claude Code CLI, suscripción), sube la imagen
a ImgBB y registra los macros en Google Sheets. Limpia registros e imágenes >90 días.

Uso: python execution/food_log.py <ruta_imagen>
"""

import base64
import json
import os
import subprocess
import sys
import urllib.request
import urllib.parse
from datetime import date, datetime, timedelta
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).parent.parent
load_dotenv(PROJECT_ROOT / ".env", override=True)

IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")
GOOGLE_SHEETS_CREDENTIALS_PATH = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH")
FOOD_LOG_SHEET_ID = os.getenv("FOOD_LOG_SHEET_ID")
FOOD_LOG_SHEET_NAME = os.getenv("FOOD_LOG_SHEET_NAME", "Hoja 1")

MEDIA_TYPE_MAP = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
    ".gif": "image/gif",
}

# Índices de columna (0-based)
COL_FECHA = 0
COL_HORA = 1
COL_COMIDA = 2
COL_CALORIAS = 3
COL_PROTEINAS = 4
COL_CARBOS = 5
COL_GRASAS = 6
COL_NOTAS = 7
COL_FOTO = 8      # URL pública de ImgBB
COL_IMG_ID = 9    # ID de imagen en ImgBB (para borrado)


def analyze_food(image_path: Path) -> dict:
    """Identifica la comida en la imagen vía Claude Code CLI (suscripción, sin API key)."""
    prompt = (
        f"Lee la imagen en esta ruta exacta: {image_path.absolute()}\n\n"
        "Analiza la comida que aparece y devuelve un JSON con:\n"
        "- nombre: nombre del plato o comida\n"
        "- calorias: estimación de calorías totales (número entero)\n"
        "- proteinas_g: gramos de proteína (número entero)\n"
        "- carbohidratos_g: gramos de carbohidratos (número entero)\n"
        "- grasas_g: gramos de grasa (número entero)\n"
        "- notas: string corto si algo es incierto, vacío si la estimación es fiable\n\n"
        "Haz tu mejor estimación basándote en porciones típicas.\n"
        "Devuelve SOLO el JSON, sin texto adicional ni bloques de código."
    )

    result = subprocess.run(
        ["claude", "-p", prompt, "--allowedTools", "Read"],
        capture_output=True,
        text=True,
        timeout=60,
    )

    if result.returncode != 0:
        raise RuntimeError(f"claude CLI error: {result.stderr.strip()}")

    raw = result.stdout.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()

    return json.loads(raw)


def upload_photo(image_path: Path) -> tuple[str, str]:
    """
    Sube la imagen a ImgBB.
    Devuelve (img_id, direct_url) — URL directa para usar en =IMAGE().
    """
    with open(image_path, "rb") as f:
        image_b64 = base64.standard_b64encode(f.read()).decode("utf-8")

    name = f"comida_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    data = urllib.parse.urlencode({
        "key": IMGBB_API_KEY,
        "image": image_b64,
        "name": name,
    }).encode("utf-8")

    req = urllib.request.Request("https://api.imgbb.com/1/upload", data=data, method="POST")
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read().decode("utf-8"))

    img_id = result["data"]["id"]
    direct_url = result["data"]["url"]   # https://i.ibb.co/xxx/image.jpg
    return img_id, direct_url


def delete_imgbb_image(img_id: str):
    """Borra una imagen de ImgBB por su ID."""
    url = f"https://api.imgbb.com/1/image/{img_id}?key={IMGBB_API_KEY}"
    req = urllib.request.Request(url, method="DELETE")
    try:
        with urllib.request.urlopen(req, timeout=10):
            pass
    except Exception:
        pass  # Si ya no existe, ignorar


def get_sheets_service():
    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    creds = service_account.Credentials.from_service_account_file(
        GOOGLE_SHEETS_CREDENTIALS_PATH,
        scopes=["https://www.googleapis.com/auth/spreadsheets"],
    )
    return build("sheets", "v4", credentials=creds, cache_discovery=False)


def get_sheet_gid(sheets) -> int:
    spreadsheet = sheets.spreadsheets().get(spreadsheetId=FOOD_LOG_SHEET_ID).execute()
    for sheet in spreadsheet["sheets"]:
        if sheet["properties"]["title"] == FOOD_LOG_SHEET_NAME:
            return sheet["properties"]["sheetId"]
    raise ValueError(f"Hoja '{FOOD_LOG_SHEET_NAME}' no encontrada.")


def ensure_headers(sheets):
    result = (
        sheets.spreadsheets().values()
        .get(spreadsheetId=FOOD_LOG_SHEET_ID, range=f"{FOOD_LOG_SHEET_NAME}!A1:J1")
        .execute()
    )
    if not result.get("values"):
        headers = [[
            "Fecha", "Hora", "Comida", "Calorías",
            "Proteínas (g)", "Carbohidratos (g)", "Grasas (g)",
            "Notas", "Foto", "Img ID",
        ]]
        sheets.spreadsheets().values().append(
            spreadsheetId=FOOD_LOG_SHEET_ID,
            range=f"{FOOD_LOG_SHEET_NAME}!A1",
            valueInputOption="RAW",
            body={"values": headers},
        ).execute()


def append_row(sheets, data: dict, direct_url: str, img_id: str):
    now = datetime.now()
    row = [[
        now.strftime("%Y-%m-%d"),
        now.strftime("%H:%M"),
        data.get("nombre", ""),
        data.get("calorias", ""),
        data.get("proteinas_g", ""),
        data.get("carbohidratos_g", ""),
        data.get("grasas_g", ""),
        data.get("notas", ""),
        f'=IMAGE("{direct_url}")',   # previsualización directa en la celda
        img_id,
    ]]
    result = sheets.spreadsheets().values().append(
        spreadsheetId=FOOD_LOG_SHEET_ID,
        range=f"{FOOD_LOG_SHEET_NAME}!A1",
        valueInputOption="USER_ENTERED",
        body={"values": row},
        includeValuesInResponse=True,
    ).execute()

    # Ajustar altura de la nueva fila a 120px para que la imagen sea visible
    updated_range = result.get("updates", {}).get("updatedRange", "")
    if updated_range:
        import re
        match = re.search(r"(\d+)$", updated_range)
        if match:
            row_index = int(match.group(1)) - 1  # 0-indexed
            sheet_gid = get_sheet_gid(sheets)
            sheets.spreadsheets().batchUpdate(
                spreadsheetId=FOOD_LOG_SHEET_ID,
                body={"requests": [{
                    "updateDimensionProperties": {
                        "range": {
                            "sheetId": sheet_gid,
                            "dimension": "ROWS",
                            "startIndex": row_index,
                            "endIndex": row_index + 1,
                        },
                        "properties": {"pixelSize": 120},
                        "fields": "pixelSize",
                    }
                }]},
            ).execute()


def cleanup_old_records(sheets):
    """Elimina filas con >90 días y borra las imágenes de ImgBB asociadas."""
    cutoff = (date.today() - timedelta(days=90)).isoformat()

    result = (
        sheets.spreadsheets().values()
        .get(spreadsheetId=FOOD_LOG_SHEET_ID, range=f"{FOOD_LOG_SHEET_NAME}!A:J")
        .execute()
    )
    all_rows = result.get("values", [])
    if len(all_rows) <= 1:
        return

    sheet_gid = get_sheet_gid(sheets)
    delete_requests = []
    img_ids_to_delete = []

    for i in range(len(all_rows) - 1, 0, -1):  # de abajo arriba, skip encabezado
        row = all_rows[i]
        row_date = row[COL_FECHA] if len(row) > COL_FECHA else ""
        if row_date and row_date < cutoff:
            delete_requests.append({
                "deleteDimension": {
                    "range": {
                        "sheetId": sheet_gid,
                        "dimension": "ROWS",
                        "startIndex": i,
                        "endIndex": i + 1,
                    }
                }
            })
            if len(row) > COL_IMG_ID and row[COL_IMG_ID]:
                img_ids_to_delete.append(row[COL_IMG_ID])

    if delete_requests:
        sheets.spreadsheets().batchUpdate(
            spreadsheetId=FOOD_LOG_SHEET_ID,
            body={"requests": delete_requests},
        ).execute()
        print(f"[cleanup] {len(delete_requests)} fila(s) eliminada(s) (anteriores a {cutoff})")

    for img_id in img_ids_to_delete:
        delete_imgbb_image(img_id)
    if img_ids_to_delete:
        print(f"[cleanup] {len(img_ids_to_delete)} imagen(es) eliminada(s) de ImgBB")


def log_food(image_path: Path) -> dict:
    """Pipeline completo: analizar → subir foto → registrar → limpiar."""
    data = analyze_food(image_path)

    # Subida de foto opcional: si falla, registrar igualmente sin foto
    img_id, view_url = "", ""
    try:
        img_id, view_url = upload_photo(image_path)
        data["foto_url"] = view_url
    except Exception as e:
        print(f"[food_log] Foto no subida ({e}), registrando sin imagen")

    sheets = get_sheets_service()
    ensure_headers(sheets)
    append_row(sheets, data, view_url, img_id)
    cleanup_old_records(sheets)
    return data


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python execution/food_log.py <ruta_imagen>")
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Error: archivo no encontrado — {path}")
        sys.exit(1)

    result = log_food(path)
    print(json.dumps(result, ensure_ascii=False, indent=2))
