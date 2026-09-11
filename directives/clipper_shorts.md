# Directiva: Clipper — VOD a Shorts

**Objetivo:** convertir un directo largo en shorts 9:16 listos para subir, con
título y descripción, sin gastar un euro en APIs.

**Herramienta:** `D:\Proyectos\Clipper` (Python + yt-dlp + ffmpeg, cero deps pip).
**Quién decide:** yo. El código solo hace lo determinista; elegir el momento y
escribir los textos es el trabajo que cobran Opus Clip y Klap, y es mi parte.

> Antes de proponer nada sobre monetización, leer `D:\Proyectos\Clipper\docs\INVESTIGACION.md`.
> Las recopilaciones sin transformar están desmonetizadas por la política de
> contenido no auténtico. El camino elegido es el canal transformativo propio.

## Inputs

Una URL de YouTube, o el id de un trabajo que ya esté esperando en la cola web.

## Proceso

### 1. Analizar

Si Pablo da una URL suelta (sin pasar por la web):

```bash
cd /d/Proyectos/Clipper
python src/clipper.py scan "<url>"        # subtítulos + transcript.md
python src/clipper.py peaks <video_id>    # candidatos por energía -> peaks.md
```

Si el trabajo viene de la interfaz web, ya está analizado:

```bash
python src/alfred.py pendientes
python src/alfred.py ver <job_id>         # rutas de peaks.md y transcript.md
```

Nunca descargar el VOD entero. `scan` baja solo subtítulos (2 h = 5 s y 290 KB) y
`peaks` baja el audio más un proxy a 144p (2 h ≈ 46 MB, ~2 min en total) para
detectar cambios de plano. El vídeo bueno se descarga por tramos al cortar.

Si falla por restricción de edad, repetir con `--cookies chrome`.

### 2. Elegir los momentos

Leer `peaks.md` primero (7 KB). Solo abrir `transcript.md` si los picos no dan
nada bueno o si Pablo pide un tema concreto.

**Un momento sirve si cumple las cuatro:**

1. **Despierta algo** — risa, nostalgia, indignación, sorpresa, ternura. Si al
   leerlo no sientes nada, el espectador tampoco.
2. **Se entiende sin contexto.** Nadie ha visto las 2 h anteriores. Una anécdota
   cerrada gana siempre a una reacción que depende de lo que pasó antes.
3. **Tiene remate.** Empieza, sube y cierra. Un tramo que se corta a media idea
   no retiene aunque el trozo sea gracioso.
4. **Dura 20–45 s.** Menos cuesta cerrar el bucle; más se cae. Excepción:
   un remate muy potente aguanta en 15–20 s si cierra en seco.

**Tipos que funcionan, por orden:** anécdota personal contada entera >
opinión polémica argumentada > reacción con remate verbal > nostalgia
(infancia, juegos viejos, "cuando éramos") > pique o chascarrillo con otro creador.

**Descartar sin dudar:** tramos con `[música]` dominante (es el juego, no él),
lecturas de chat, momentos que solo tienen sentido viendo la pantalla, y todo lo
que sea puramente reaccionar a contenido ajeno (hereda el Content ID del tercero).

**Nunca cruzar un cambio de escena.** Un clip que salta de la cámara al juego (o
entre dos zonas del juego) rompe la atención y parece mal editado. `peaks` ya
detecta los cortes sobre el proxy y da a cada candidato su **rango limpio**:
usar ese rango, no el tramo entero, y no estirarlo más allá de sus extremos.
Los candidatos cuyo tramo limpio baja de 15 s se descartan solos.

**Ojo con los picos:** la energía detecta volumen, no calidad. En gameplay la
banda sonora dispara falsos positivos. Verificar siempre leyendo el texto.

El corte empieza **1–2 s antes** de la primera palabra buena, no en el segundo
exacto del pico, siempre que quepa dentro del rango limpio.

### 3. Elegir el encuadre

| Situación | Modo |
|---|---|
| Cámara a pantalla completa (charla, just chatting) | `crop` — calidad intacta |
| Plano raro o fuente que no encaja | `blur` |
| Gameplay con facecam pequeña | `pip` + `--cam` del preset, `sub_y` ~420 |
| Dos sujetos / entrevista a dos cámaras | `split` |

Layouts medidos por canal en `presets/canales.json`. Si el canal no está,
medirlo una vez sobre un frame y añadirlo.

**La charla es la mejor fuente.** En los VODs de gameplay suele estar en el primer
cuarto de hora, antes de empezar a jugar. Los VODs completos que los streamers
suben a YouTube incluyen esa charla y traen subtítulos; los de Twitch no.

### 4. Escribir los textos

**Título:** máximo 60 caracteres. La afirmación fuerte del clip, tal cual. Sin
"INCREÍBLE", sin emojis de flechas, sin clickbait hueco. Si el clip cuenta por qué
pasó algo, el título es esa pregunta.

**Descripción:** una línea que repite el gancho, crédito al creador original con
enlace al vídeo completo, y 3–5 hashtags. Plantilla en `presets/meta.md`.

**Gancho en pantalla (`hook`):** 2–6 palabras, la promesa del clip. Va en los
primeros 2,2 s. Saltos de línea con `\n` real en el JSON (no `\N`).

### 5. Montar

Escribir el plan como JSON válido —construirlo con `json.dumps` desde Python, no
a mano, que los acentos y las comillas dan guerra— y lanzarlo:

```bash
python src/alfred.py plan <job_id> <ruta_plan.json>
```

Campos por clip: `start`, `end`, `titulo` (obligatorios), y `descripcion`,
`hook`, `frame`, `cam`, `sub_y`, `zoom`.

Si no hay trabajo en la cola (Pablo dio una URL suelta), cortar directamente:

```bash
python src/clipper.py cut <video_id> --start 12:34 --end 13:06 \
    --name <slug> --frame crop --hook "TEXTO" --zoom
```

El render tarda 1–3 min por clip, casi todo descarga del tramo.

### 6. Entregar

- Si vino por la web: la interfaz ya muestra reproductor, descarga y textos.
  Decirle a Pablo que está listo y resumir qué momentos se eligieron y por qué.
- Si vino por chat: mandar el mp4 con `SendUserFile` y poner título y
  descripción en el mensaje, listos para copiar.

> Los mp4 de más de 30 MB no llegan al móvil. Para previsualizar, generar una
> versión ligera: `ffmpeg -i <clip> -vf scale=608:1080 -crf 30 -preset veryfast <preview>`
> y avisar de que el original en calidad completa está en disco.

## Edge cases

- **Sin subtítulos automáticos** (VODs de Twitch, canales pequeños): avisar a
  Pablo. Haría falta transcribir con faster-whisper, que no está instalado.
- **Restricción de edad:** `--cookies chrome`.
- **yt-dlp da 403 o "SABR streaming":** `yt-dlp -U`. YouTube rompe la descarga
  cada pocos meses y la versión vieja es casi siempre la causa.
- **Los picos salen todos con `[música]`:** el VOD es gameplay puro. Buscar la
  charla inicial en el transcript o pedir otro VOD.
- **Se descartan casi todos los candidatos:** el VOD tiene montaje muy picado.
  Subir `--window` no ayuda; bajar el listón con `--sin-escenas` tampoco es la
  solución, mejor ir a la charla inicial.
- **Pablo pide un lote:** máximo 5 clips por VOD. Más satura y se repiten.

## Salidas

- `work/jobs/<job_id>/clips/*.mp4` (por la web) o `out/<slug>.mp4` (por chat)
- Título y descripción por clip
- Anotar en `memory/YYYY-MM-DD.md` qué VOD se procesó y qué momentos salieron,
  para no repetirlos en el siguiente lote.
