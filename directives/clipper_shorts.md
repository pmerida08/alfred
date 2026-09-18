# Directiva: Clipper — VOD a vídeo largo y a Shorts

**Objetivo:** convertir un directo largo en una recopilación horizontal de
20–35 min —o en shorts 9:16— lista para subir, con título y descripción, sin
gastar un euro en APIs.

**Herramienta:** `D:\Proyectos\Clipper` (Python + yt-dlp + ffmpeg, cero deps pip).
**Quién decide:** yo. El código solo hace lo determinista; elegir el momento y
escribir los textos es el trabajo que cobran Opus Clip y Klap, y es mi parte.

> Antes de proponer nada sobre monetización, leer `D:\Proyectos\Clipper\docs\INVESTIGACION.md`.
> Las recopilaciones sin transformar están desmonetizadas por la política de
> contenido no auténtico. El camino elegido es el canal transformativo propio.

## Qué formato — por defecto, horizontal

Medidos los cinco canales de referencia de Pablo (373 vídeos, `docs/CANALES.md`):
los cuatro que funcionan viven del **vídeo horizontal de 20–45 min**, y sus
Shorts rinden 8–10× peor. Las vistas suben con la duración sin excepción
(<10 min → 2.900 medianas; 20–30 min → 128.000; 45 min+ → 209.500).

| | Compilación 16:9 | Short 9:16 |
|---|---|---|
| Cuándo | por defecto | cuando Pablo lo pida, o como derivado del largo |
| Duración | 20–35 min | 45–55 s |
| Coste de montaje | bajo: sin reframe, sin pip, sin zoom, sin subtítulos | alto |
| Ruta | A | B |

Si Pablo no dice formato, es una compilación. Los Shorts salen después, de los
bloques que ya se eligieron.

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

## Ruta A — compilación horizontal

### A1. Elegir los bloques

Aquí **hay que leer el transcript entero**, no los picos. Los picos sirven para
encontrar un chiste suelto; una compilación necesita un **argumento**, y eso solo
se ve leyendo. En un VOD de 2 h son unas 500 líneas: se lee en trozos de 75.

Lo que se busca es una tesis que el streamer desarrolle sin saberlo, y los
bloques que la sostienen en orden. Ejemplo real (GTA 6, `presets/bloques/`):
se abren las reservas → qué trae cada edición → *"si no pagáis, ni rizo ni
greña"* → la Ultimate pieza a pieza → la comparación con Red Dead 2 → Oblivion y
la armadura de caballo de 2006 → remate con Barbie.

Reglas:

- **18–25 bloques de 45–150 s** para llegar a 20–35 min.
- **El orden es editorial, no cronológico.** Si el mejor remate pasó a mitad del
  directo, va al final. El fichero de bloques manda.
- **El primer bloque es el gancho**: lo que hace que alguien se quede, no el
  principio cronológico. Fuera patrocinios y saludos.
- Cada bloque lleva una **nota** que será su capítulo.
- No hace falta que todos sean graciosos. Los que sostienen el argumento valen
  aunque sean planos; lo que retiene es el camino, no el chiste.

Guardar la selección en `D:\Proyectos\Clipper\presets\bloques\<video_id>.txt`
(se versiona: es el único paso con criterio de todo el pipeline).

### A2. Montar

Si el trabajo viene de la web, el plan va por `alfred.py` y el servidor monta solo:

```bash
python src/alfred.py plan <job_id> plan.json
```

con `plan.json` así (el orden de `bloques` es el del montaje):

```json
{"titulo": "...", "descripcion": "...", "tags": "...",
 "edicion": "completa",
 "bloques": [{"start": "3:58", "end": "6:06", "nota": "sale como capítulo"}]}
```

Si viene por chat, a mano:

```bash
cd /d/Proyectos/Clipper
python src/clipper.py compilacion <video_id> \
  --bloques presets/bloques/<video_id>.txt --name <slug>
```

El comando mueve cada corte a la pausa del habla más cercana, fusiona los bloques
contiguos, descarga por tramos, edita, normaliza y concatena. Verifica la
duración con ffprobe tramo a tramo y al final; si no cuadra, aborta.

**La edición por defecto (`completa`) es la medida sobre los canales de
referencia**: quita los silencios con margen 0,45 s (1 corte cada ~7 s, como
EditsRBN), nivela a −14 LUFS y funde las costuras. No subirla ni bajarla sin
motivo. `--cartelas` existe pero va apagado: ninguno de los cinco canales usa
rótulos.

No tocar `--sin-ajuste` salvo que Pablo lo pida: sin el ajuste, la mayoría de los
cortes entran a mitad de frase.

Los capítulos salen en `out/<slug>.capitulos.txt` con las marcas reales.

### A2b. Capa de énfasis (opcional, en prueba)

Zooms, rótulos y congelados, decididos por Alfred desde el transcript igual que
los bloques. **Sin pegatinas ni efectos de sonido**: se probaron el 16/09 y
Pablo los descartó. **Es una apuesta, no un requisito**: los canales de
referencia no usan nada de esto. Se valida midiendo la retención en Studio
contra el COD1 y el Lobezno, que salieron sin énfasis. Si no mejora, se quita.

Una línea por efecto, con el **segundo del VOD** (el reloj del transcript). En el
plan va como lista `"enfasis": [...]`; por chat, en un fichero y con
`--enfasis presets/enfasis/<video_id>.txt`:

```
1:44:22.5  zoom 1.3 @0.46,0.42        # golpe de zoom a la cara
1:52:10    texto "EL CHAT MIENTE"     # rótulo con rebote, abajo
2:03:10    congelar "NO ES VERDAD"    # imagen congelada + rótulo
2:11:30    censura dur=0.6            # silencia la voz, sin pitido
2:12:00    temblor
```

Criterio:
- **Poco y en los remates.** Uno cada 1-2 min como mucho; si todo es énfasis,
  nada lo es. El zoom va en la frase que es la tesis o en la reacción, no en
  cualquier grito.
- El `@x,y` del zoom se elige mirando un fotograma del tramo: la cámara no
  está en el mismo sitio en charla que en gameplay.
- La censura cae ~0,15 s más tarde de lo escrito y los subtítulos automáticos
  ya bailan: darle margen por delante y `dur` de sobra.
- Los efectos no hacen el vídeo "transformativo" para YouTube
  (`docs/INVESTIGACION.md`): no venderlo como solución a la monetización.
- Antes del montaje completo, revisar con `--solo N` (solo ese tramo, en
  `out/<slug>_tramos_N.mp4`): extraer fotogramas en los instantes de los
  efectos y comprobar duración y fotogramas con ffprobe.

### A3. Textos

Plantilla medida sobre 285 títulos en `docs/CANALES.md` §6:

- **Título:** nombre del streamer **siempre primero**, verbo en mayúsculas,
  objeto, y `*Mejores Momentos*` si encaja. El gancho puede ser el remate del
  vídeo, no el principio.
- **Tags:** 15–20, saturando variantes del nombre + el tema.
- **Descripción:** fecha del directo y una línea de qué pasa → capítulos → aviso
  de canal no oficial con todas las redes del streamer → disclaimer de fair use.
- **Categoría:** Gaming o Entertainment.

Recordarle a Pablo que active el **doblaje multilingüe** al subir (YouTube
Studio → Subtítulos → pistas de audio). Es gratis y es lo que separa a
StarzyEdits —9,9 vistas por suscriptor— del resto.

## Ruta B — Shorts 9:16

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
4. **Dura 45–55 s.** Medido sobre 35 Shorts de los canales de clips que ya
   funcionan: mediana 34 s y los tres mayores éxitos en 53–56 s; la franja
   0–20 s es la que peor rinde. Suelo 25 s, techo 65 s. Datos en
   `D:\Proyectos\Clipper\docs\DURACION.md`.

**Tipos que funcionan, por orden:** los clips que revientan en esos canales son
**opinión o revelación con postura**, no golpes de gracia sueltos — "desmiente
cuánto le pagó X", "reacciona a los precios de Y", "critica duramente Z".
Después: anécdota personal contada entera > nostalgia > pique con otro creador.

**Estructura del clip:** gancho (qué se va a contar) → desarrollo con su opinión
→ remate. **No cortar en cuanto llega el chiste:** lo que retiene es el camino
hasta él, y por eso hacen falta 45–55 s y no 15.

**Descartar sin dudar:** tramos con `[música]` dominante (es el juego, no él),
lecturas de chat, momentos que solo tienen sentido viendo la pantalla, y todo lo
que sea puramente reaccionar a contenido ajeno (hereda el Content ID del tercero).

**Nunca cruzar un cambio de escena.** Un clip que salta de la cámara al juego (o
entre dos zonas del juego) rompe la atención y parece mal editado. `peaks` ya
detecta los cortes sobre el proxy y da a cada candidato su **rango limpio**:
usar ese rango, no el tramo entero, y no estirarlo más allá de sus extremos.
Los candidatos cuyo tramo limpio baja de 25 s se descartan solos.

En directos de **charla** hay que pasarle `--cam` a `peaks`: el streamer navega por
webs y la pantalla compartida cambia cada pocos segundos. Mirando el frame entero
salen ~146 cortes y no queda ni un tramo largo; mirando solo la caja de la facecam
salen ~32, que son los cambios de plano de verdad. El detector es guía, no árbitro:
cruzar un cambio de *contenido en pantalla* mientras él sigue hablando es normal y
se ve bien; lo que no se cruza es un cambio de *plano*.

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

### 3b. Animación

`--anim mixto` va por defecto y no hay que tocarlo casi nunca: saca los cambios de
plano de las pausas del habla y da un plano nuevo cada 3–6,5 s. Un clip de 50 s con
plano fijo no aguanta.

- `--fuerza` (por defecto 0,11) sube o baja cuánto cierra cada golpe. Más de 0,18
  sobre una cara ya parece un fallo de reproducción.
- `--anim suave` para material donde el zoom moleste (una pantalla con texto que
  haya que leer). `--anim none` solo si Pablo lo pide.

### 3c. Subtítulos, palabrotas y overlays

**`--whisper` siempre que el clip tenga palabrotas.** Los auto-subs de YouTube
las tapan con `[ __ ]` y no dejan la palabra: sin transcribir el audio no se
puede poner `m*****`. Cuesta ~1 min por clip y además corrige los errores de los
auto-subs.

**Overlays** (`--overlay "8-13:chat,50-54:risa.png"`):

- `chat` solo donde está reaccionando a alguien del chat. De adorno estorba, y
  nunca sobre un plano `cam` a pantalla completa porque tapa la cara.
- Las imágenes salen de `assets/`. 2–3 s en pantalla, no más.

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
`hook`, `frame`, `cam`, `sub_y`, `zoom`, `anim`, `fuerza`, `overlay`,
`whisper` (con `modelo`). En la cola web el render solo pasa lo que venga en el
plan: si el clip lleva palabrotas hay que poner `"whisper": true` ahí, no basta
con acordarse al cortar a mano.

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
>
> Una compilación de 30 min pesa ~400 MB: **no mandarla nunca por chat**. Dar la
> ruta, los capítulos y los textos.

## Edge cases

- **Sin subtítulos automáticos** (VODs de Twitch, canales pequeños): avisar a
  Pablo. Haría falta transcribir con faster-whisper, que no está instalado.
- **Restricción de edad: no se puede clipear.** Las cookies pasan el muro para
  leer metadatos, pero con sesión iniciada YouTube exige un PO token para el
  medio y devuelve 403. Avisar a Pablo y pedirle otro VOD; no perder tiempo
  probando navegadores. (En Windows además Chrome, Brave y Edge cifran sus
  cookies y solo Firefox es legible.)
- **yt-dlp da 403 o "SABR streaming":** `yt-dlp -U`. YouTube rompe la descarga
  cada pocos meses y la versión vieja es casi siempre la causa.
- **Los picos salen todos con `[música]`:** el VOD es gameplay puro. Buscar la
  charla inicial en el transcript o pedir otro VOD.
- **Se descartan casi todos los candidatos:** el VOD tiene montaje muy picado.
  Subir `--window` no ayuda; bajar el listón con `--sin-escenas` tampoco es la
  solución, mejor ir a la charla inicial.
- **Pablo pide un lote:** máximo 5 clips por VOD. Más satura y se repiten.

- **Pablo pide una compilación y el VOD dura menos de 25 min:** no da para el
  formato largo. Proponer juntar dos o tres directos del mismo tema, que es lo
  que hace EditsRBN con sus series, o hacer Shorts.

## Salidas

- Compilación: `out/<slug>.mp4` + `out/<slug>.capitulos.txt` +
  selección en `presets/bloques/<video_id>.txt`
- Shorts: `work/jobs/<job_id>/clips/*.mp4` (por la web) o `out/<slug>.mp4`
- Título y descripción por pieza
- Anotar en `memory/YYYY-MM-DD.md` qué VOD se procesó y qué momentos salieron,
  para no repetirlos en el siguiente lote.
