"""
FORGE — Setup visual del Google Sheet de nutrición.
Aplica formato, crea hoja de Resumen con estadísticas y limpia datos de prueba.

Uso: python execution/setup_food_sheet.py
"""

import os
import sys
import urllib.request
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).parent.parent
# El .env puede estar en el worktree o en el proyecto raíz (un nivel arriba)
_env = PROJECT_ROOT / ".env"
if not _env.exists():
    _env = PROJECT_ROOT.parent.parent.parent / ".env"  # raíz real desde worktree
load_dotenv(_env, override=True)

from google.oauth2 import service_account
from googleapiclient.discovery import build

CREDENTIALS_PATH = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH")
SHEET_ID = os.getenv("FOOD_LOG_SHEET_ID")
DATA_SHEET = os.getenv("FOOD_LOG_SHEET_NAME", "Hoja 1")
STATS_SHEET = "Resumen"

creds = service_account.Credentials.from_service_account_file(
    CREDENTIALS_PATH,
    scopes=["https://www.googleapis.com/auth/spreadsheets"],
)
service = build("sheets", "v4", credentials=creds, cache_discovery=False)


def get_sheet_gid(title: str) -> int | None:
    spreadsheet = service.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
    for sheet in spreadsheet["sheets"]:
        if sheet["properties"]["title"] == title:
            return sheet["properties"]["sheetId"]
    return None


def rgb(r, g, b):
    return {"red": r / 255, "green": g / 255, "blue": b / 255}


def setup_data_sheet(gid: int):
    """Formatea la hoja de datos de comidas."""
    requests = [
        # Renombrar a "Comidas" si aún se llama "Hoja 1"
        {
            "updateSheetProperties": {
                "properties": {"sheetId": gid, "title": "Comidas"},
                "fields": "title",
            }
        },
        # Cabecera: fondo oscuro + texto blanco negrita
        {
            "repeatCell": {
                "range": {"sheetId": gid, "startRowIndex": 0, "endRowIndex": 1},
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": rgb(30, 41, 59),
                        "textFormat": {
                            "foregroundColor": rgb(255, 255, 255),
                            "bold": True,
                            "fontSize": 10,
                            "fontFamily": "Inter",
                        },
                        "horizontalAlignment": "CENTER",
                        "verticalAlignment": "MIDDLE",
                        "wrapStrategy": "CLIP",
                    }
                },
                "fields": "userEnteredFormat",
            }
        },
        # Altura de la cabecera
        {
            "updateDimensionProperties": {
                "range": {"sheetId": gid, "dimension": "ROWS", "startIndex": 0, "endIndex": 1},
                "properties": {"pixelSize": 36},
                "fields": "pixelSize",
            }
        },
        # Congelar cabecera
        {
            "updateSheetProperties": {
                "properties": {
                    "sheetId": gid,
                    "gridProperties": {"frozenRowCount": 1},
                },
                "fields": "gridProperties.frozenRowCount",
            }
        },
        # Anchos de columna
        *[
            {
                "updateDimensionProperties": {
                    "range": {"sheetId": gid, "dimension": "COLUMNS", "startIndex": i, "endIndex": i + 1},
                    "properties": {"pixelSize": w},
                    "fields": "pixelSize",
                }
            }
            for i, w in enumerate([95, 55, 180, 75, 90, 110, 80, 200, 130, 1])
            #                      Fecha Hora Comida Cal Prot Carbs Grasas Notas Foto ImgID(oculta)
        ],
        # Ocultar columna J (Img ID — interna)
        {
            "updateDimensionProperties": {
                "range": {"sheetId": gid, "dimension": "COLUMNS", "startIndex": 9, "endIndex": 10},
                "properties": {"hiddenByUser": True},
                "fields": "hiddenByUser",
            }
        },
        # Filas de datos: formato base (texto centrado, fuente consistente)
        {
            "repeatCell": {
                "range": {"sheetId": gid, "startRowIndex": 1, "endRowIndex": 1000},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"fontSize": 10, "fontFamily": "Inter"},
                        "verticalAlignment": "MIDDLE",
                        "horizontalAlignment": "CENTER",
                        "wrapStrategy": "WRAP",
                    }
                },
                "fields": "userEnteredFormat",
            }
        },
        # Columna Notas y Comida: alineación izquierda
        *[
            {
                "repeatCell": {
                    "range": {"sheetId": gid, "startRowIndex": 1, "endRowIndex": 1000,
                              "startColumnIndex": col, "endColumnIndex": col + 1},
                    "cell": {
                        "userEnteredFormat": {"horizontalAlignment": "LEFT"}
                    },
                    "fields": "userEnteredFormat.horizontalAlignment",
                }
            }
            for col in [2, 7]  # Comida, Notas
        ],
        # Formato condicional: filas pares fondo gris claro
        {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [{"sheetId": gid, "startRowIndex": 1, "endRowIndex": 1000}],
                    "booleanRule": {
                        "condition": {
                            "type": "CUSTOM_FORMULA",
                            "values": [{"userEnteredValue": "=ISEVEN(ROW())"}],
                        },
                        "format": {"backgroundColor": rgb(241, 245, 249)},
                    },
                },
                "index": 0,
            }
        },
        # Formato condicional: calorías altas (>700) en rojo suave
        {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [{"sheetId": gid, "startRowIndex": 1, "endRowIndex": 1000,
                                "startColumnIndex": 3, "endColumnIndex": 4}],
                    "booleanRule": {
                        "condition": {
                            "type": "NUMBER_GREATER",
                            "values": [{"userEnteredValue": "700"}],
                        },
                        "format": {
                            "backgroundColor": rgb(254, 226, 226),
                            "textFormat": {"foregroundColor": rgb(185, 28, 28), "bold": True},
                        },
                    },
                },
                "index": 1,
            }
        },
        # Filtro en cabecera
        {
            "setBasicFilter": {
                "filter": {
                    "range": {"sheetId": gid, "startRowIndex": 0, "endRowIndex": 1000,
                              "startColumnIndex": 0, "endColumnIndex": 10}
                }
            }
        },
    ]
    service.spreadsheets().batchUpdate(
        spreadsheetId=SHEET_ID, body={"requests": requests}
    ).execute()
    print(f"[OK] Hoja 'Comidas' formateada")


def create_stats_sheet():
    """Crea la hoja Resumen con estadísticas automáticas."""
    gid = get_sheet_gid(STATS_SHEET)
    requests = []

    if gid is None:
        requests.append({
            "addSheet": {
                "properties": {
                    "title": STATS_SHEET,
                    "gridProperties": {"rowCount": 50, "columnCount": 8},
                    "tabColor": rgb(16, 185, 129),
                }
            }
        })
        resp = service.spreadsheets().batchUpdate(
            spreadsheetId=SHEET_ID, body={"requests": requests}
        ).execute()
        gid = resp["replies"][0]["addSheet"]["properties"]["sheetId"]
        requests = []
        print(f"[OK] Hoja 'Resumen' creada (gid={gid})")
    else:
        print(f"[OK] Hoja 'Resumen' ya existe (gid={gid})")

    # El spreadsheet está en locale español: las funciones deben ir en español.
    # Las fechas se guardan como texto "YYYY-MM-DD" → comparaciones texto-vs-texto.
    T   = 'TEXTO(HOY(),"YYYY-MM-DD")'
    WS  = 'TEXTO(HOY()-DIASEM(HOY(),2)+1,"YYYY-MM-DD")'  # lunes de esta semana
    M30 = 'TEXTO(HOY()-30,"YYYY-MM-DD")'

    def hoy(col):
        return f'=SUMAR.SI(Comidas!A:A,{T},Comidas!{col}:{col})'

    def semana(col):
        return f'=SUMAR.SI.CONJUNTO(Comidas!{col}:{col},Comidas!A:A,">="&{WS},Comidas!A:A,"<="&{T})'

    def media30(col):
        return f'=SI.ERROR(REDONDEAR(SUMAR.SI.CONJUNTO(Comidas!{col}:{col},Comidas!A:A,">="&{M30})/30,1),0)'

    # Contenido de la hoja de resumen
    values = [
        # Sección HOY
        ["HOY", "", "", "", "ESTA SEMANA", "", "", ""],
        ["Calorías",          hoy("D"), "", "", "Calorías",          semana("D"), "", ""],
        ["Proteínas (g)",     hoy("E"), "", "", "Proteínas (g)",     semana("E"), "", ""],
        ["Carbohidratos (g)", hoy("F"), "", "", "Carbohidratos (g)", semana("F"), "", ""],
        ["Grasas (g)",        hoy("G"), "", "", "Grasas (g)",        semana("G"), "", ""],
        ["Comidas registradas",
         f"=CONTAR.SI(Comidas!A:A,{T})", "", "",
         "Comidas esta semana",
         f'=CONTAR.SI.CONJUNTO(Comidas!A2:A,">="&{WS},Comidas!A2:A,"<="&{T},Comidas!A2:A,"<>")',
         "", ""],
        ["", "", "", "", "", "", "", ""],
        # Sección MEDIAS DIARIAS (últimos 30 días)
        ["MEDIAS DIARIAS (últimos 30 días)", "", "", "", "", "", "", ""],
        ["Calorías/día",      media30("D"), "", "", "", "", "", ""],
        ["Proteínas/día (g)", media30("E"), "", "", "", "", "", ""],
        ["Total registros",   "=CONTARA(Comidas!A2:A)", "", "", "", "", "", ""],
        # ORDENAR+FILTRAR ordena fechas YYYY-MM-DD lexicográficamente (= cronológicamente)
        ["Primer registro",
         '=SI.ERROR(INDICE(ORDENAR(FILTRAR(Comidas!A2:A,Comidas!A2:A<>""),1,1),1),"—")',
         "", "", "", "", "", ""],
    ]

    service.spreadsheets().values().update(
        spreadsheetId=SHEET_ID,
        range=f"{STATS_SHEET}!A1",
        valueInputOption="USER_ENTERED",
        body={"values": values},
    ).execute()

    # Formatear la hoja de resumen
    fmt_requests = [
        # Fondo general: gris muy claro
        {
            "repeatCell": {
                "range": {"sheetId": gid},
                "cell": {"userEnteredFormat": {
                    "backgroundColor": rgb(248, 250, 252),
                    "textFormat": {"fontFamily": "Inter", "fontSize": 10},
                }},
                "fields": "userEnteredFormat",
            }
        },
        # Títulos de sección (filas 1 y 8): fondo verde oscuro + texto blanco
        *[
            {
                "repeatCell": {
                    "range": {"sheetId": gid, "startRowIndex": r, "endRowIndex": r + 1},
                    "cell": {"userEnteredFormat": {
                        "backgroundColor": rgb(15, 118, 110),
                        "textFormat": {"foregroundColor": rgb(255,255,255), "bold": True, "fontSize": 11},
                        "verticalAlignment": "MIDDLE",
                    }},
                    "fields": "userEnteredFormat",
                }
            }
            for r in [0, 7]
        ],
        # Labels (col A y E de filas de datos): negrita gris oscuro
        {
            "repeatCell": {
                "range": {"sheetId": gid, "startRowIndex": 1, "endRowIndex": 7,
                          "startColumnIndex": 0, "endColumnIndex": 1},
                "cell": {"userEnteredFormat": {
                    "textFormat": {"bold": True, "foregroundColor": rgb(51, 65, 85)},
                }},
                "fields": "userEnteredFormat.textFormat",
            }
        },
        {
            "repeatCell": {
                "range": {"sheetId": gid, "startRowIndex": 1, "endRowIndex": 7,
                          "startColumnIndex": 4, "endColumnIndex": 5},
                "cell": {"userEnteredFormat": {
                    "textFormat": {"bold": True, "foregroundColor": rgb(51, 65, 85)},
                }},
                "fields": "userEnteredFormat.textFormat",
            }
        },
        # Valores (col B y F): verde llamativo + negrita grande
        {
            "repeatCell": {
                "range": {"sheetId": gid, "startRowIndex": 1, "endRowIndex": 7,
                          "startColumnIndex": 1, "endColumnIndex": 2},
                "cell": {"userEnteredFormat": {
                    "textFormat": {"bold": True, "fontSize": 14, "foregroundColor": rgb(5, 150, 105)},
                    "horizontalAlignment": "LEFT",
                }},
                "fields": "userEnteredFormat",
            }
        },
        {
            "repeatCell": {
                "range": {"sheetId": gid, "startRowIndex": 1, "endRowIndex": 7,
                          "startColumnIndex": 5, "endColumnIndex": 6},
                "cell": {"userEnteredFormat": {
                    "textFormat": {"bold": True, "fontSize": 14, "foregroundColor": rgb(37, 99, 235)},
                    "horizontalAlignment": "LEFT",
                }},
                "fields": "userEnteredFormat",
            }
        },
        # Separador visual entre HOY y SEMANA (col D)
        {
            "repeatCell": {
                "range": {"sheetId": gid, "startRowIndex": 0, "endRowIndex": 7,
                          "startColumnIndex": 3, "endColumnIndex": 4},
                "cell": {"userEnteredFormat": {"backgroundColor": rgb(203, 213, 225)}},
                "fields": "userEnteredFormat.backgroundColor",
            }
        },
        # Alturas de fila
        {
            "updateDimensionProperties": {
                "range": {"sheetId": gid, "dimension": "ROWS", "startIndex": 0, "endIndex": 1},
                "properties": {"pixelSize": 40},
                "fields": "pixelSize",
            }
        },
        {
            "updateDimensionProperties": {
                "range": {"sheetId": gid, "dimension": "ROWS", "startIndex": 1, "endIndex": 12},
                "properties": {"pixelSize": 32},
                "fields": "pixelSize",
            }
        },
        # Anchos de columna
        *[
            {
                "updateDimensionProperties": {
                    "range": {"sheetId": gid, "dimension": "COLUMNS", "startIndex": i, "endIndex": i + 1},
                    "properties": {"pixelSize": w},
                    "fields": "pixelSize",
                }
            }
            for i, w in enumerate([160, 100, 20, 20, 160, 100, 20, 20])
        ],
        # Congelar primera fila
        {
            "updateSheetProperties": {
                "properties": {"sheetId": gid, "gridProperties": {"frozenRowCount": 1}},
                "fields": "gridProperties.frozenRowCount",
            }
        },
    ]

    service.spreadsheets().batchUpdate(
        spreadsheetId=SHEET_ID, body={"requests": fmt_requests}
    ).execute()
    print(f"[OK] Hoja 'Resumen' formateada con estadísticas")


def fix_existing_rows():
    """Ajusta la altura de filas de datos ya existentes a 120px."""
    gid = get_sheet_gid("Comidas")
    result = service.spreadsheets().values().get(
        spreadsheetId=SHEET_ID, range="Comidas!A:A"
    ).execute()
    n = len(result.get("values", [])) - 1  # excluir encabezado
    if n <= 0:
        return
    service.spreadsheets().batchUpdate(
        spreadsheetId=SHEET_ID,
        body={"requests": [{
            "updateDimensionProperties": {
                "range": {"sheetId": gid, "dimension": "ROWS", "startIndex": 1, "endIndex": 1 + n},
                "properties": {"pixelSize": 120},
                "fields": "pixelSize",
            }
        }]},
    ).execute()
    print(f"[OK] Altura de {n} fila(s) de datos ajustada a 120px")


def _delete_imgbb(img_id: str):
    key = os.getenv("IMGBB_API_KEY", "")
    if not (img_id and key):
        return
    req = urllib.request.Request(
        f"https://api.imgbb.com/1/image/{img_id}?key={key}", method="DELETE"
    )
    try:
        with urllib.request.urlopen(req, timeout=10):
            pass
    except Exception:
        pass


def delete_test_rows(keyword: str):
    """Elimina filas cuyo nombre de comida contenga keyword (case-insensitive)."""
    result = service.spreadsheets().values().get(
        spreadsheetId=SHEET_ID, range=f"{DATA_SHEET}!A:J"
    ).execute()
    rows = result.get("values", [])
    if len(rows) <= 1:
        print("[cleanup] Sin filas de datos")
        return

    gid = get_sheet_gid(DATA_SHEET)
    kw = keyword.lower()
    delete_requests, img_ids = [], []

    for i in range(len(rows) - 1, 0, -1):
        row = rows[i]
        comida = row[2].lower() if len(row) > 2 else ""
        if kw in comida:
            delete_requests.append({
                "deleteDimension": {
                    "range": {
                        "sheetId": gid,
                        "dimension": "ROWS",
                        "startIndex": i,
                        "endIndex": i + 1,
                    }
                }
            })
            if len(row) > 9 and row[9]:
                img_ids.append(row[9])

    if delete_requests:
        service.spreadsheets().batchUpdate(
            spreadsheetId=SHEET_ID, body={"requests": delete_requests}
        ).execute()
        print(f"[OK] {len(delete_requests)} fila(s) eliminada(s) ('{keyword}')")
        for img_id in img_ids:
            _delete_imgbb(img_id)
        if img_ids:
            print(f"[OK] {len(img_ids)} imagen(es) eliminada(s) de ImgBB")
    else:
        print(f"[cleanup] No se encontraron filas con '{keyword}'")


if __name__ == "__main__":
    # Uso: python setup_food_sheet.py [--full] [--fix-resumen] [--cleanup KEYWORD]
    args = sys.argv[1:]

    if "--cleanup" in args:
        idx = args.index("--cleanup")
        keyword = args[idx + 1] if idx + 1 < len(args) else "pizza"
        delete_test_rows(keyword)
    elif "--fix-resumen" in args:
        create_stats_sheet()
        print("\nResumen actualizado.")
    else:
        # Setup completo (defecto)
        data_gid = get_sheet_gid(DATA_SHEET)
        if data_gid is None:
            print(f"ERROR: hoja '{DATA_SHEET}' no encontrada")
            raise SystemExit(1)
        setup_data_sheet(data_gid)
        fix_existing_rows()
        create_stats_sheet()
        print("\nSetup completado.")
