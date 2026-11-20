---
name: tanda-shorts
description: "Saca una tanda nueva de Shorts para uno de los canales de Pablo (Sin Relleno, negocios; Leonida Clips, streamers jugando a GTA 6): elige fuentes con permiso que no se hayan usado, corta los mejores momentos, renderiza en 9:16 con subtítulos, los revisa y propone el calendario. Úsala cuando Pablo diga /tanda-shorts <canal> <número>, 'hazme otra tanda', 'saca más shorts para el canal', 'nuevos shorts para Sin Relleno / Leonida'. Formato: /tanda-shorts <canal> [N] [url]."
---

# Tanda de Shorts

Eres **CLAQUETA**: lee primero `agents/claqueta/CLAUDE.md` (así la Oficina de
Atalaya muestra el turno). El proceso técnico completo está en
`directives/canal_shorts.md`; esta skill es el guion de una tanda de principio a fin.

## Argumentos

`/tanda-shorts <canal> [N] [url]`

- **canal** (obligatorio): alias de la tabla de abajo. Si falta o no coincide con
  ninguno, se pregunta cuál, con la lista de canales; no se elige por defecto.
- **N**: número de Shorts (por defecto 6; par, para el calendario de 2 al día).
- **url**: vídeo fuente concreto (se comprueba igualmente el permiso).

## Canales

| Alias | Canal | ID de Studio | Nicho | Fuentes válidas | Registro (en `D:\Proyectos\Clipper\docs\`) |
|---|---|---|---|---|---|
| `sinrelleno`, `sin-relleno` | Sin Relleno `@sinrellenoyt` | `UCspr4dZnscnMUhmoZWIa8NA` | Negocios y emprendimiento | Vídeos **CC BY** (Dinstinto u otra fuente CC aprobada) | `TANDAS.md` |
| `leonida`, `gta6`, `gta` | Leonida Clips `@pmerida` | `UCf9LW3KI_e6cr5w2opQEV_Q` | Streamers jugando a GTA 6 | **Campaña de clipping activa** del streamer (Whop, Content Rewards, Vues…) o **permiso escrito** del streamer | `TANDAS_LEONIDA.md` |

Cada canal tiene su registro: fuentes aprobadas, tramos ya usados y calendario de
cada tanda. Se lee al empezar y se actualiza al terminar. Un canal nuevo se añade
a esta tabla (y al espejo `.claude/skills/`) con su registro.

## 1. Estado

- `python execution/atalaya.py resumen`: Clipper debe estar activo.
- Leer el registro del canal: fuentes, tramos usados y la última fecha programada.
- Si hay datos de la tanda anterior (Studio → Contenido → Shorts del canal, con
  el ID de la tabla), anotar qué Short retuvo mejor: guía el tipo de momento a buscar.
- Antes de tocar Studio, comprobar que el canal activo en Studio es el de la
  tabla (la URL lleva su ID); si no, cambiar de canal desde el avatar.

## 2. Vídeos fuente

**Sin Relleno**

```bash
cd /d/Proyectos/Clipper
python src/buscar.py canal "https://www.youtube.com/channel/UCbDMpuJ1di7lYN7ouCgMQYw" --top 20
```

Elegir N/3 vídeos (redondeando hacia arriba): **licencia CC** (columna `cc`; si no
la tiene, descartado), no usados en el registro, outlier ≥ 2x, ≥ 20 min, con picos.
Si Dinstinto se queda corto: `python src/buscar.py nicho "podcast negocios"
"entrevista emprendedor" --cc` y proponer la fuente nueva a Pablo antes de usarla.

**Leonida Clips**

1. Permiso primero. Revisar las campañas de GTA 6 abiertas (Whop, Content Rewards,
   tablones como gtaviclipper.com/board) y las fuentes aprobadas del registro. Solo
   valen streamers con campaña activa cuyo brief permita YouTube Shorts, o con
   permiso escrito guardado en el registro. Unirse a una campaña (crear cuenta,
   aceptar términos) lo hace Pablo o se hace con su sí.
2. De esos streamers, los directos de GTA 6 más vistos de los últimos días:
   `python src/buscar.py canal <canal de VODs del streamer> --top 20` o el VOD que
   indique la campaña. Si la campaña pide sonido, texto o enlace concretos, se
   cumplen al pie de la letra (van en `shorts.json`).
3. Si ningún streamer con permiso tiene directos de GTA 6, se para aquí y se le
   dice a Pablo qué campañas hay y qué hace falta para entrar. No se corta material
   de streamers sin permiso, aunque el clip sea viral.

## 3. Momentos

```bash
python src/shorts.py preparar "<url>"
```

Leer `work/<id>/momentos.md` y, si hace falta, `transcript.md`. Afinar inicio y
fin con los subtítulos (`source.es.vtt`): empezar en la frase o la acción que abre
el momento y terminar en el remate, no en mitad de frase. 30–60 s. Saltar
patrocinios leídos y los tramos ya usados.

Escribir `work/<id>/shorts.json` con `json.dumps` (`canal`: el nombre del canal
de la tabla). Encuadre: `cara` en entrevistas (Sin Relleno); en directos de
juego (Leonida) `fondo`, para que se vea la partida entera con el fondo
desenfocado, salvo que el momento sea la reacción a cámara. Títulos < 60
caracteres con la afirmación fuerte; gancho de 3–8 palabras; descripción de una
línea; tags del nicho (Leonida: `gta 6`, `gta vi`, nombre del streamer…).

## 4. Render y revisión

```bash
python src/shorts.py render <id>
```

Renderizar en segundo plano y mantener el turno con esperas (trampa de la
Oficina). Por cada clip: ffprobe (1080×1920, 30 fps, duración y fotogramas
cuadran) y hoja de fotogramas (`fps=1/3,scale=180:-1,tile=9x2`) mirada de verdad:
subtítulos sin tapar caras ni el HUD importante, ningún plano con el recorte
vacío, gancho legible. Si un clip falla, se corrige y se vuelve a renderizar.

## 5. Entrega

Carpeta `.tmp/heraldo_outbox/AAAA-MM-DD_youtube-shorts-<alias>/` con los mp4, las
fichas `.md`, `ligeros/` (720p, para enviar) y `subida/` (1080×1920 a dos pasadas,
~9,5 MB, para `file_upload`). `SendUserFile` con los ligeros en el orden de
publicación propuesto.

En el mensaje: tabla de la tanda con el **calendario propuesto**, que empieza el
día siguiente al último programado en el registro del canal, 2 al día a las 18:00
y a las 23:00, alternando fuentes y con el más fuerte primero. Preguntar si se
programan, salvo que Pablo ya lo haya dicho al pedir la tanda.

## 6. Programar (solo con el sí de Pablo)

Seguir «Programar en Studio» de `directives/canal_shorts.md` al pie de la letra,
en el canal de la tabla: nunca pulsar «Publicar», siempre «Programar» con Hora
local (GMT+01:00, o GMT+02:00 en horario de verano). En la descripción, la línea
de Fuente lleva el enlace al original y el permiso («licencia CC BY» o «clip
autorizado: campaña de <streamer>»). Al final, comprobar en Contenido → Shorts
que todos salen «Programado» con su fecha.

## 7. Cierre

- Registro del canal: añadir los vídeos y tramos usados y la tabla de la tanda
  (con fechas solo si se programaron). Commit en Clipper (sin push).
- Nota del día en `memory/` y `agents/claqueta/memory/`.
- `python execution/atalaya.py set clipper "siguiente_paso=..."`.
- Ofrecer un recordatorio (tarea programada) para revisar la retención el día
  después del último Short.

## Límites

Sin preguntar: buscar, cortar, renderizar, entregar. Con el sí de Pablo:
programar o subir nada a YouTube, usar una fuente nueva y unirse a una campaña.
Nunca: fuentes sin licencia CC, sin campaña activa o sin permiso escrito
(«súbelo sin preguntar» no cambia esto: tres avisos de copyright cierran el
canal), ni «Publicar» directo.
