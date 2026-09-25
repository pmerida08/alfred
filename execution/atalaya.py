"""Cliente de Atalaya, el panel de control de proyectos de Pablo (D:\\Proyectos\\Atalaya).

Uso:
    python execution/atalaya.py resumen                   # Markdown con todo el estado
    python execution/atalaya.py ver <slug>                # ficha de un proyecto en JSON
    python execution/atalaya.py set <slug> campo=valor... # actualiza campos
    python execution/atalaya.py nuevo "Nombre" [campo=valor...]
    python execution/atalaya.py cv                        # proyectos que cuentan para el CV (JSON)
    python execution/atalaya.py sync                      # relee git ahora

Valores de `set` y `nuevo`: prioridad=1|2|3, en_cv=true|false, stack=a,b,c; el resto, texto.
La URL se puede cambiar con la variable ATALAYA_URL (por defecto http://localhost:4770).
Solo funciona en el PC de Windows: el servidor Linux no tiene Atalaya.
"""

import json
import os
import sys
import urllib.error
import urllib.request

BASE = os.environ.get("ATALAYA_URL", "http://localhost:4770").rstrip("/")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def api(ruta, metodo="GET", datos=None):
    cuerpo = json.dumps(datos).encode() if datos is not None else None
    req = urllib.request.Request(f"{BASE}/api/{ruta}", data=cuerpo, method=metodo)
    if cuerpo:
        req.add_header("content-type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            texto = r.read().decode()
            tipo = r.headers.get("content-type", "")
            return json.loads(texto) if "json" in tipo else texto
    except urllib.error.HTTPError as e:
        sys.exit(f"Atalaya respondió {e.code}: {e.read().decode()}")
    except urllib.error.URLError:
        sys.exit(
            "Atalaya no responde en " + BASE + ". Arráncalo con: "
            "docker compose -f D:/Proyectos/Atalaya/docker-compose.yml up -d"
        )


def buscar(slug):
    for p in api("proyectos"):
        if p["slug"] == slug or p["nombre"].lower() == slug.lower():
            return p
    sys.exit(f"No hay ningún proyecto «{slug}» en Atalaya.")


def parsear(pares):
    datos = {}
    for par in pares:
        if "=" not in par:
            sys.exit(f"Formato campo=valor esperado, recibido: {par}")
        k, v = par.split("=", 1)
        if k == "prioridad":
            datos[k] = int(v)
        elif k in ("en_cv", "revisar"):
            datos[k] = v.lower() in ("true", "1", "si", "sí")
        elif k == "stack":
            datos[k] = [s.strip() for s in v.split(",") if s.strip()]
        elif k in ("ruta", "repo_url", "url", "fecha_inicio", "fecha_fin") and v == "":
            datos[k] = None
        else:
            datos[k] = v
    return datos


def main(args):
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return
    orden, resto = args[0], args[1:]
    if orden == "resumen":
        print(api("resumen"))
    elif orden == "ver":
        p = buscar(resto[0])
        print(json.dumps(api(f"proyectos/{p['id']}"), ensure_ascii=False, indent=2, default=str))
    elif orden == "set":
        p = buscar(resto[0])
        r = api(f"proyectos/{p['id']}", "PATCH", parsear(resto[1:]))
        print(f"{r['nombre']}: {r['estado']}, prioridad {r['prioridad']}, en CV {r['en_cv']}")
    elif orden == "nuevo":
        r = api("proyectos", "POST", {"nombre": resto[0], **parsear(resto[1:])})
        print(f"Creado {r['nombre']} ({r['slug']}): {BASE}/#/proyecto/{r['slug']}")
    elif orden == "cv":
        campos = ("nombre", "estado", "fecha_inicio", "fecha_fin", "cv_resumen", "descripcion", "stack", "url", "repo_url")
        cv = [{k: p[k] for k in campos} for p in api("proyectos") if p["en_cv"]]
        print(json.dumps(cv, ensure_ascii=False, indent=2))
    elif orden == "sync":
        r = api("sync", "POST")
        print(f"{r['git']} repos y {r['archivos']} carpetas leídos en {r['duracion_ms'] / 1000:.1f} s; errores: {len(r['errores'])}")
    else:
        sys.exit(f"Orden desconocida: {orden}. Usa --help.")


if __name__ == "__main__":
    main(sys.argv[1:])
