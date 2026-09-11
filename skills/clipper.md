# Skill: clipper

**ID:** `clipper`
**Cuándo:** Pablo pasa el link de un directo o VOD y pide cortarlo, sacar clips,
hacer shorts, "córtame esto", "saca los mejores momentos", o hay trabajos
esperando en la cola de Clipper.

Ejecuta la directiva `directives/clipper_shorts.md` sobre la herramienta local
`D:\Proyectos\Clipper` (Python + yt-dlp + ffmpeg, cero dependencias pip, cero
APIs de pago).

1. Analiza el VOD sin descargarlo: subtítulos (`scan`) y picos de energía del
   audio (`peaks`). Un VOD de 2 h son 5 s y 290 KB.
2. Lee los candidatos y elige los momentos que despiertan algo (risa, nostalgia,
   polémica), se entienden sin contexto y tienen remate. 20–45 s cada uno.
3. Elige encuadre (`crop` para charla, `pip` para gameplay con facecam pequeña),
   escribe título y descripción con crédito al creador original.
4. Monta descargando solo el tramo elegido y entrega el mp4 con sus textos.

> También hay interfaz web: `python src/server.py` → http://127.0.0.1:8730.
> Pablo pega el link, la web analiza, y el trabajo queda esperando a que Alfred
> elija los momentos desde el chat.
