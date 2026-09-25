"""Genera un QR que apunta a un archivo, local o de Google Drive.

Uso:
    python execution/qr_archivo.py <origen> [opciones]

<origen> puede ser:
    - un enlace de Drive (https://drive.google.com/file/d/<id>/..., ?id=<id>, docs.google.com/...)
    - un ID de archivo de Drive
    - una ruta a un archivo del PC

Modos para archivos del PC:
    (por defecto)  lo sube a "Mi unidad" con gws y hace el QR del enlace
    --lan          no sube nada: lo sirve por la wifi local hasta Ctrl+C
                   (el móvil tiene que estar en la misma red)

Opciones:
    --publico       da permiso "cualquiera con el enlace puede ver" (sin esto,
                    el enlace solo abre con tu cuenta de Google)
    --carpeta ID    carpeta de Drive donde subir el archivo
    --salida RUTA   PNG de salida (por defecto .tmp/qr/<nombre>.png)
    --puerto N      puerto para --lan (por defecto 8765)

Drive va con el CLI `gws` (ya autenticado como Pablo); el QR se genera en local con segno.
"""

import argparse
import http.server
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import urllib.parse
from pathlib import Path

import segno

RAIZ = Path(__file__).resolve().parent.parent
SALIDA_DEFECTO = RAIZ / ".tmp" / "qr"

PATRONES_DRIVE = [
    r"/d/([A-Za-z0-9_-]{20,})",          # /file/d/<id>/, /document/d/<id>/...
    r"[?&]id=([A-Za-z0-9_-]{20,})",      # open?id=<id>, uc?id=<id>
    r"/folders/([A-Za-z0-9_-]{20,})",    # carpetas
]


# ---------- Drive (vía gws) ----------

def gws(*args: str) -> dict:
    exe = shutil.which("gws")
    if not exe:
        sys.exit("No encuentro el CLI `gws`. Instálalo: npm i -g @googleworkspace/cli")
    res = subprocess.run([exe, *args], capture_output=True, text=True, encoding="utf-8")
    if res.returncode != 0:
        sys.exit(f"gws falló ({res.returncode}):\n{res.stderr.strip() or res.stdout.strip()}")
    # gws puede escribir avisos antes del JSON (p. ej. "Using keyring backend")
    salida = res.stdout
    inicio = salida.find("{")
    return json.loads(salida[inicio:]) if inicio >= 0 else {}


def id_de_drive(origen: str) -> str | None:
    for patron in PATRONES_DRIVE:
        m = re.search(patron, origen)
        if m:
            return m.group(1)
    if re.fullmatch(r"[A-Za-z0-9_-]{25,}", origen) and not Path(origen).exists():
        return origen
    return None


def metadatos(file_id: str) -> dict:
    return gws("drive", "files", "get", "--params", json.dumps({
        "fileId": file_id,
        "fields": "id,name,mimeType,webViewLink",
        "supportsAllDrives": True,
    }))


def subir(ruta: Path, carpeta: str | None) -> str:
    args = ["drive", "+upload", str(ruta)]
    if carpeta:
        args += ["--parent", carpeta]
    subido = gws(*args)
    if "id" not in subido:
        sys.exit(f"La subida no devolvió un ID: {subido}")
    return subido["id"]


def hacer_publico(file_id: str) -> None:
    gws("drive", "permissions", "create",
        "--params", json.dumps({"fileId": file_id, "supportsAllDrives": True}),
        "--json", json.dumps({"role": "reader", "type": "anyone"}))


# ---------- LAN ----------

def ip_local() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))  # no envía nada; solo elige la interfaz
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


def servir_lan(ruta: Path, puerto: int, png: Path) -> None:
    nombre_url = urllib.parse.quote(ruta.name)
    url = f"http://{ip_local()}:{puerto}/{nombre_url}"

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            if urllib.parse.unquote(self.path.lstrip("/")) != ruta.name:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header("Content-Type", "application/octet-stream")
            self.send_header("Content-Length", str(ruta.stat().st_size))
            self.send_header("Content-Disposition",
                             f"attachment; filename*=UTF-8''{nombre_url}")
            self.end_headers()
            with ruta.open("rb") as f:
                shutil.copyfileobj(f, self.wfile)

        def log_message(self, fmt, *args):
            print(f"  descarga desde {self.client_address[0]}: {fmt % args}")

    generar_qr(url, png, en_terminal=True)
    print(f"\nSirviendo {ruta.name} en {url}")
    print("El móvil tiene que estar en la misma wifi. Ctrl+C para parar.\n")
    with http.server.ThreadingHTTPServer(("0.0.0.0", puerto), Handler) as srv:
        try:
            srv.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor parado: el QR ya no funciona.")


# ---------- QR ----------

def generar_qr(url: str, png: Path, en_terminal: bool = False) -> None:
    qr = segno.make(url, error="m")
    png.parent.mkdir(parents=True, exist_ok=True)
    qr.save(png, scale=10, border=2)
    print(f"QR guardado en {png}")
    if en_terminal:
        qr.terminal(compact=True)


def ruta_png(salida: str | None, nombre: str) -> Path:
    if salida:
        return Path(salida).resolve()
    limpio = re.sub(r'[<>:"/\\|?*]+', "_", Path(nombre).stem) or "qr"
    return SALIDA_DEFECTO / f"{limpio}.png"


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description="QR para un archivo local o de Google Drive.")
    p.add_argument("origen", help="ruta local, enlace de Drive o ID de Drive")
    p.add_argument("--lan", action="store_true", help="servir el archivo local por la wifi en vez de subirlo")
    p.add_argument("--publico", action="store_true", help="cualquiera con el enlace puede verlo")
    p.add_argument("--carpeta", help="ID de carpeta de Drive para la subida")
    p.add_argument("--salida", help="ruta del PNG")
    p.add_argument("--puerto", type=int, default=8765)
    a = p.parse_args()

    file_id = id_de_drive(a.origen)
    ruta = Path(a.origen).expanduser()

    if file_id is None:
        if not ruta.is_file():
            sys.exit(f"No es un archivo ni un enlace de Drive reconocible: {a.origen}")
        ruta = ruta.resolve()
        if a.lan:
            servir_lan(ruta, a.puerto, ruta_png(a.salida, ruta.name))
            return
        print(f"Subiendo {ruta.name} a Drive...")
        file_id = subir(ruta, a.carpeta)
    elif a.lan:
        sys.exit("--lan solo tiene sentido con un archivo del PC.")

    if a.publico:
        hacer_publico(file_id)

    meta = metadatos(file_id)
    url = meta.get("webViewLink") or f"https://drive.google.com/file/d/{file_id}/view"
    print(f"Archivo: {meta.get('name', file_id)}")
    print(f"Enlace:  {url}")
    if not a.publico:
        print("Aviso: sin --publico el enlace solo abre con una cuenta que ya tenga acceso.")
    generar_qr(url, ruta_png(a.salida, meta.get("name", file_id)))


if __name__ == "__main__":
    main()
