---
name: clipper
description: "Convierte un directo largo de YouTube en una recopilación horizontal de 20-35 min, o en Shorts 9:16, con título y descripción listos para subir. Úsala cuando Pablo pase un link de un VOD o directo y pida cortarlo, sacar clips, hacer una recopilación o unos shorts, 'córtame esto', 'saca los mejores momentos', o cuando haya trabajos esperando en la cola de Clipper. Herramienta local en D:\\Proyectos\\Clipper — sin APIs de pago."
---

# Clipper — VOD a vídeo largo y a Shorts

Sigue de principio a fin la directiva `directives/clipper_shorts.md`. Contiene el
proceso completo y, sobre todo, el criterio para elegir el material, que es la
única parte que no puede hacer el código.

## Qué formato

**Por defecto, recopilación horizontal de 20-35 min.** Medidos los cinco canales
de referencia de Pablo (373 vídeos, `D:\Proyectos\Clipper\docs\CANALES.md`): los
cuatro que funcionan viven del formato largo y sus Shorts rinden 8-10× peor. Las
vistas suben con la duración sin excepción. Los Shorts son el derivado, no el
producto.

## Ruta A — compilación (el producto principal)

1. **Analizar** — `scan` saca los subtítulos. Nunca se descarga el VOD entero.
2. **Elegir los bloques** — leer el **transcript entero**, no los picos. Buscar
   una tesis que el streamer desarrolle sin saberlo y los 18-25 bloques de
   45-150 s que la sostienen. El orden es editorial, no cronológico.
3. **Montar** — `python src/clipper.py compilacion <id> --bloques <fichero> --name <slug>`.
   El comando ajusta los cortes a las pausas del habla, concatena y verifica la
   duración real con ffprobe.
4. **Escribir** — título con el nombre del streamer primero, 15-20 tags,
   descripción con capítulos, créditos y fair use.

## Ruta B — Shorts

`peaks` (energía del audio) → elegir momentos que despierten algo y tengan
remate → encuadrar (`crop` si la cámara ocupa la pantalla, `pip` si es gameplay
con facecam) → `cut`.

## Reglas que no se saltan

- **La energía no es calidad.** Los picos detectan volumen; en gameplay la banda
  sonora dispara falsos positivos. Verificar siempre leyendo el texto del tramo.
- **Sin contexto no hay clip** (Shorts). Nadie ha visto las 2 h anteriores.
- **45-55 s los Shorts** (suelo 25, techo 65); **20-35 min la compilación**.
- **Verificar la duración del render con ffprobe**, no fotogramas sueltos: los
  defectos de temporización no dan error.
- **Crédito al creador original** siempre en la descripción.
- **Máximo 5 Shorts por VOD.**
- Recordar el **doblaje multilingüe** al subir: es gratis y multiplica el alcance.

## Antes de hablar de dinero

Leer `D:\Proyectos\Clipper\docs\INVESTIGACION.md`. Las recopilaciones sin
transformar están desmonetizadas por la política de contenido no auténtico de
YouTube y el RPM de Shorts es 0,03-0,10 $/1.000 vistas. El camino elegido con
Pablo es el canal transformativo propio, no recortar y subir.
