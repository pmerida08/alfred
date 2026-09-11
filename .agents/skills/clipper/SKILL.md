---
name: clipper
description: "Convierte un directo largo de YouTube en Shorts 9:16 editados, con título y descripción listos para subir. Úsala cuando Pablo pase un link de un VOD o directo y pida cortarlo, sacar clips, hacer shorts, 'córtame esto', 'saca los mejores momentos', o cuando haya trabajos esperando en la cola de Clipper. Herramienta local en D:\Proyectos\Clipper — sin APIs de pago."
---

# Clipper — VOD a Shorts

Sigue de principio a fin la directiva `directives/clipper_shorts.md`. Contiene el
proceso completo y, sobre todo, el criterio para elegir los momentos, que es la
única parte que no puede hacer el código.

## Resumen del flujo

1. **Analizar** — `scan` (subtítulos) y `peaks` (energía del audio). Nunca se
   descarga el VOD entero: 2 h se analizan en 5 s y 290 KB.
2. **Elegir** — leer `peaks.md` y quedarse con los momentos que despiertan algo
   (risa, nostalgia, polémica), se entienden sin contexto y tienen remate.
3. **Encuadrar** — `crop` si la cámara ocupa la pantalla, `pip` si es gameplay
   con facecam pequeña.
4. **Escribir** — título de 60 caracteres sin clickbait, descripción con crédito
   al creador original.
5. **Montar y entregar** — el render descarga solo el tramo elegido.

## Reglas que no se saltan

- **La energía no es calidad.** Los picos detectan volumen; en gameplay la banda
  sonora dispara falsos positivos. Verificar siempre leyendo el texto del tramo.
- **Sin contexto no hay clip.** Nadie ha visto las 2 h anteriores.
- **20–45 segundos.** Fuera de ahí no retiene.
- **Crédito al creador original** siempre en la descripción.
- **Máximo 5 clips por VOD.**

## Antes de hablar de dinero

Leer `D:\Proyectos\Clipper\docs\INVESTIGACION.md`. Las recopilaciones sin
transformar están desmonetizadas por la política de contenido no auténtico de
YouTube y el RPM de Shorts es 0,03–0,10 $/1.000 vistas. El camino elegido con
Pablo es el canal transformativo propio, no recortar y subir.
