# Directiva: QR de un archivo

**Dominio:** Utilidades
**Cuándo:** Pablo pide un QR para compartir un archivo ("hazme un QR de este PDF", "QR de este enlace de Drive")
**Script:** `execution/qr_archivo.py`

---

## Objetivo

Un PNG con un QR que, al escanearlo, abre o descarga el archivo. Un QR no puede llevar el archivo dentro (le caben ~3 KB), así que siempre apunta a una URL.

## Elegir el modo

| Situación | Comando |
|---|---|
| El archivo ya está en Drive | `python execution/qr_archivo.py "<enlace o ID>"` |
| Archivo del PC que tiene que durar / compartirse con cualquiera | `python execution/qr_archivo.py "<ruta>" --publico` (lo sube a Mi unidad) |
| Pasarlo al móvil ahora mismo, sin subir nada | `python execution/qr_archivo.py "<ruta>" --lan` |

Opciones: `--carpeta <ID>` (subir a una carpeta concreta), `--salida <png>` (por defecto `.tmp/qr/<nombre>.png`), `--puerto` (LAN, 8765).

## Reglas

- **`--publico` hace el archivo visible para cualquiera con el enlace.** Si Pablo no ha dicho que es para otras personas, preguntar antes de usarlo. Sin `--publico` el QR solo abre con su cuenta.
- El modo `--lan` solo funciona mientras el script está en marcha y con el móvil en la misma wifi. Sirve únicamente ese archivo (cualquier otra ruta da 404). La primera vez Windows puede pedir permiso en el firewall.
- Subir a Drive crea una copia nueva cada vez: no repetir la subida del mismo archivo, reutilizar el enlace.
- Entregar el PNG con `SendUserFile`, junto con el enlace en texto.

## Dependencias

- CLI `gws` autenticado como Pablo (scope `drive`). Comprobar con `gws auth status`.
- `pip install segno` (genera el QR; sin dependencias).
- Solo en el PC Windows: en el servidor Linux no está `gws` configurado.
