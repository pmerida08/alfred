# Directiva: canal de Shorts de un nicho

**Objetivo:** elegir nicho → preparar el canal → encontrar vídeos horizontales que
estén rindiendo → sacar de cada uno 3–5 Shorts verticales con subtítulos, gancho,
título y descripción, listos para subir.

**Herramienta:** `D:\Proyectos\Clipper` (`src/buscar.py` + `src/shorts.py`, render con
HyperFrames). Coste 0: yt-dlp, faster-whisper local y HyperFrames en local.
**Quién decide:** yo elijo vídeos y momentos y escribo los textos; Pablo decide el
nicho, el canal y qué se sube. Subir o publicar lo hace siempre Pablo.

> **Antes de nada, el permiso.** `docs/INVESTIGACION.md`: recortar vídeos ajenos y
> subirlos es «contenido no auténtico» (no monetiza) y Content ID se queda los
> ingresos o tumba el vídeo; tres avisos de copyright cierran el canal. Fuentes
> válidas, por orden: **campaña de clipping** (Whop, Vues…; te pagan por vista) →
> **Creative Commons** (`buscar.py --cc`) → creador que permite clips por escrito.
> Si el vídeo elegido no cumple ninguna, se dice antes de cortar.

## 1. Nicho

```bash
cd /d/Proyectos/Clipper
python src/buscar.py nicho "consulta 1" "consulta 2" --dias 30 [--cc]
```

Deja `work/busquedas/<fecha>_<nicho>.md` con la tabla y los picos de audiencia.
Un nicho vale si cumple los criterios de `docs/NICHO.md` (cara hablando, momentos
de 20–60 s que se entienden solos, publican cada semana, permiso). Lanzar 3–4
nichos y comparar: cuántos vídeos con outlier ≥ 2× y cuántos con licencia CC o
campaña. Proponer a Pablo 2 nichos con sus cifras; elige él.

## 2. Canal

El canal es **Sin Relleno** `@sinrellenoyt` (`UCspr4dZnscnMUhmoZWIa8NA`, el antiguo
Echo Sites, teléfono verificado). Desde el 2026-11-14 su nicho es **negocios y
emprendimiento**, con fuente CC **Dinstinto** (`docs/CANAL.md`). El canal viejo
`UCclo_6d1Lgow8BfQ1RDZSGw` volvió a ser el personal de Pablo: no tocarlo.
Segundo canal desde el 2026-11-19: **Leonida Clips** (`UCf9LW3KI_e6cr5w2opQEV_Q`,
identificador `@pmerida`; Studio rechazó los nuevos), clips de streamers jugando a
GTA 6, con banner y avatar de `assets/canal/banner_gta6.py` y registro
`docs/TANDAS_LEONIDA.md`. Solo material con campaña de clipping o permiso escrito.
La tabla de canales vive en la skill `tanda-shorts`.
Adaptarlo a otro nicho = descripción, palabras clave y banner
(`assets/canal/banner_negocios.py`, Pillow, sin créditos). Cambios en el canal
solo con su OK, con Claude in Chrome en su navegador: Studio acepta clics,
escritura y `file_upload` (comprobado el 2026-11-14). El campo de palabras clave
está en Configuración → Canal; se comprueba con el `<meta name="keywords">` de la
página pública, porque TubeAlfred devuelve datos en caché.
Subir por API pide un cliente OAuth de Google Cloud que no existe todavía.

## 3. Elegir el vídeo fuente

```bash
python src/buscar.py canal @canal_del_nicho     # outliers frente a su mediana
```

Buen vídeo fuente: outlier ≥ 2×, ≥ 8 min, conversación a cámara, subtítulos en
el idioma, y picos en el «más reproducido». Cuantos más picos, más Shorts salen.

## 4. Momentos

```bash
python src/shorts.py preparar "<url>"    # work/<id>/momentos.md + transcript.md
```

`momentos.md` trae los picos de audiencia con lo que se dice alrededor. Si el
vídeo no tiene mapa de audiencia, leer `transcript.md` entero. Criterios de un
buen momento: los de la Ruta B de `directives/clipper_shorts.md` (despierta algo,
se entiende sin contexto, tiene remate). Duración 30–60 s. Máximo 5 por vídeo.

Escribir `work/<id>/shorts.json` (construido con `json.dumps` si hay comillas):

```json
{"canal": "Sin Relleno",
 "clips": [{"slug": "porro-sub21", "inicio": "23:12", "fin": "23:55",
            "gancho": "Se lesionó el día antes del Europeo",
            "encuadre": "cara",
            "titulo": "...", "descripcion": "...", "tags": ["..."]}]}
```

- **gancho:** 3–8 palabras, la promesa del clip; sale arriba los primeros 4–7 s.
- **encuadre:** `cara` (por defecto) decide **plano a plano**: corta el tramo en
  planos con `scdet` de ffmpeg y a cada uno le da su recorte sobre la cara, o el
  fondo desenfocado si es un plano general (cara mayor < 18 % del alto) o hay dos
  personas separadas. `centro`, un número 0–1 (x del recorte) o `fondo` son fijos
  para todo el clip.
- **titulo:** < 60 caracteres, la afirmación fuerte del clip. **descripcion:** una
  línea; la atribución con enlace al original y los hashtags se añaden solos.

## 5. Render

```bash
python src/shorts.py render <id> [--solo slug] [--calidad draft]
```

Por clip: baja solo el tramo, encuadra a 1080×1920 y normaliza a −14 LUFS
(ffmpeg), transcribe palabra a palabra (faster-whisper `small`, sin la censura de
YouTube), genera la composición HyperFrames (subtítulos de 3 palabras con la
palabra activa en amarillo, gancho, punch-ins en las pausas), pasa `lint`,
renderiza y comprueba con ffprobe duración, fotogramas y resolución; si no
cuadra, aborta. ~2–3 min por clip de 45 s en `draft`.

Salida en `out/shorts/<id>/`: `<slug>.mp4` + `<slug>.md` (título, descripción,
tags, medidas) y la carpeta `<slug>/` con el proyecto HyperFrames editable
(`npx hyperframes preview` dentro para retocarlo).

Antes de entregar: hoja de fotogramas (ffmpeg `tile`) de cada clip y mirarla:
subtítulos sin tapar caras, gancho legible, encuadre sobre quien habla.

## 6. Entrega

`SendUserFile` con los mp4 (si pasan de 30 MB, una versión ligera) y los textos
en el mensaje.

**Programar en Studio (solo si Pablo lo pide expresamente).** Calendario por
defecto: 2 Shorts al día a las 18:00 y 23:00 (hora de España), alternando
fuentes y con el más fuerte primero. Con Claude in Chrome:
- `file_upload` no admite más de 10 MB: sacar una versión 1080×1920 a dos pasadas con
  bitrate para ~9,5 MB (`subida/` en la carpeta de entrega; YouTube recomprime igual).
- Studio → `videos/upload?d=ud`: título, descripción (añadir «(licencia CC BY)»
  a la línea de Fuente), «No, no está creado para niños», «Mostrar configuración
  avanzada» → borrar los tags por defecto y poner los de la ficha.
- Visibilidad viene en **Público** con el botón «Publicar»: no pulsarlo. Desplegar
  «Programar», fecha en el calendario, zona «Hora local (GMT+01:00)» y la hora en el
  desplegable (no admite escribirla). Aceptar el aviso «Aún estamos comprobando».
- Comprobar en Contenido → Shorts que todos salen «Programado» con su fecha.
- Si Studio se congela (capturas que caducan), es que hay un render de HyperFrames
  ocupando el equipo: esperar a que acabe. Anotar en `memory/YYYY-MM-DD.md` el vídeo y los slugs para no
repetirlos.

## Edge cases

- **Dos personas lejos en el plano** (entrevista en mesa): ese plano sale con fondo
  desenfocado y los primeros planos siguen recortados. Si todo el tramo es un
  plano fijo y el que importa es uno, poner su x a mano (`"encuadre": 0.3`).
- **Resultados en otro idioma:** `buscar.py` descarta los que declaran otro idioma
  (`--idioma todos` los deja).
- **Sin «más reproducido»:** YouTube solo lo da en vídeos con bastantes vistas; leer
  el transcript.
- **Restricción de edad / 403:** igual que en `directives/clipper_shorts.md`.
