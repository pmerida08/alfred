# Perfil — Streakode (TikTok)

> Cuenta de marca de Streakode en TikTok. La voz definida aquí manda sobre cualquier idea o directiva.
> Creado el 30/09/2026 con lo decidido en la sesión de arranque.

## Identidad

- **Cuenta / marca:** @streakode — https://www.tiktok.com/@streakode (cuenta de empresa; sin verificación de empresa)
- **Plataforma(s):** TikTok
- **Nicho:** programación en píldoras: retos de «¿qué imprime esto?» y trampas de cada lenguaje, con Streakode como la app donde se practica un minuto al día.
- **Objetivo:** llevar gente a probar la app (`streakode.com`, «Pruébalo sin cuenta» en /probar) y medir si se quedan. Prioridad del proyecto: retención antes que más funciones.

## Audiencia

- **A quién le hablo:** gente que aprende a programar o programa a diario en español (estudiantes, bootcamps, juniors) y devs a los que les gusta picarse con un quiz.
- **Qué le quita el sueño:** olvidar lo aprendido, no tener constancia, las trampas del lenguaje que caen en entrevistas y exámenes.
- **Nivel:** de principiante a intermedio. El quiz tiene que poder intentarlo un junior y sorprender a alguien con años.

## Voz y tono

- **Tono:** terminal, seco y con un punto de pique («parece fácil»). Explica en una frase, sin sermones.
- **Persona:** marca; se dirige al espectador de tú. **Sin voz ni cara (decisión de Pablo, 30/09): solo pantalla y texto.** Todo lo que haya que decir va en texto en pantalla; nada de guiones con locución.
- **Idioma:** español.
- **Estética fija:** look «terminal» (fondo #0B1210, verde #3DFFA2, ámbar #FACC15 para el fallo, todo en Geist Mono), el cursor `_` del logo como protagonista, música «Mrsn - Code Chill» (Pixabay, sin Content ID).

## Pilares de contenido

1. **Adivina el output** — serie fija, numerada, un lenguaje por episodio. Ejercicio real de la app (nivel 2, con trampa), salida comprobada ejecutándolo. Estructura: pregunta → 4 opciones y cuenta atrás → el cursor cae en la trampa (ámbar) → salta a la buena → explicación → arreglo → «¿Acertaste?» → logo.
2. **Trampas por lenguaje** — el error común de cada lenguaje explicado en 20 s (Python, JS, Java, Kotlin…).
3. **Build in public** — cómo va Streakode con cifras reales de /admin, honesto (también lo que no funciona), contado con capturas y texto en pantalla.
4. **Producto** — novedades de la app y «pruébalo sin cuenta».

## Do's & Don'ts

**Sí:**
- Gancho en el primer fotograma: la pregunta y el código ya en pantalla.
- Ejercicios reales de Streakode; la salida se comprueba ejecutando el código antes de publicar.
- Descripción: «¿Acertaste a la primera? 👇» + la trampa en una frase + «Un ejercicio así cada día en streakode.com/tiktok» + 5 hashtags.
- Portada: el fotograma con el «3» amarillo de la cuenta atrás.
- Comentario fijado pidiendo el lenguaje del siguiente episodio.
- Ajustes: Todos, divulgación «Tu marca», sin marca de IA, no añadir música de TikTok.

**No:**
- Cifras o afirmaciones sin dato («casi todo el mundo falla»).
- Canciones de tendencia (la cuenta de empresa solo tiene biblioteca comercial; la música ya va en el vídeo).
- Emojis decorativos en pantalla; en la descripción, solo el 👇.
- Publicar desde Alfred: publica siempre Pablo.

## Ejemplos de referencia

- TikTok 01, presentación «El cursor que lo hace todo» (30/09).
- TikTok 02, «Adivina el output #1 · JavaScript»: `[10, 9, 1].sort()` → `1,10,9` (30/09).

## Cadencia

- **Frecuencia objetivo:** 4 vídeos/semana (3 de «adivina el output» + 1 de otro pilar), en tandas que HERALDO entrega los lunes. Revisión a las 2 semanas con tiempo medio de visualización y % visto entero; si retiene, subir a 5–7.
- **Mejores horarios:** 19:00–22:00 (hipótesis; confirmar con las estadísticas de la cuenta).

## Enlaces y medición

Cada enlace lleva su etiqueta para que `/admin` → Origen de Streakode diga qué vídeo trae gente (detalle en `D:\Proyectos\Streakode\docs\ORIGEN.md`).

**La cuenta no tiene enlace pulsable en la bio** (13/10/2026): la app no deja pasarla a cuenta de empresa y la web solo edita usuario, nombre y 80 caracteres de descripción. Las guías (no oficiales) dicen que el campo de web exige cuenta de empresa o ~1.000 seguidores; la cuenta tiene 1. Por eso **no usar «link en la bio»** en vídeos ni descripciones mientras no exista el campo, y llevar a la gente con una dirección corta que se escriba:

- **Dirección única para todo (bio en texto, cierre de los vídeos, comentario fijado):** `streakode.com/tiktok`. Redirige a `/probar` ya etiquetado (`utm_campaign=pantalla`), en producción desde el 13/10/2026 (PR #39). No es pulsable: la lee y la escribe la persona.
- **Bio (propuesta, la edita Pablo):** `Un ejercicio de código al día. streakode.com/tiktok` (51 de 80 caracteres).
- **Por episodio (para medir cada vídeo), en el cierre y en el comentario fijado:** `streakode.com/t/<lenguaje><n>` con `<n>` el número de la serie: `js1`, `py2`, `java3`, `kt4`, `react5`, `ng6`, `rn7`. TypeScript no tiene código propio: va con `js<n>` (ruta JavaScript / TypeScript), como el #18. Lleva a la prueba de ese lenguaje y `/admin` lo cuenta como `adivina-<lenguaje>-<nn>`. Vídeos que no son de la serie: `streakode.com/t/<nombre>` (`/t/racha` en el 06 Protectores, `/t/nivel` en el 07 Test de nivel, `/t/hopper` en el 05, que se publicó antes con `streakode.com` a secas). Tabla completa en `D:\Proyectos\Streakode\docs\ORIGEN.md`.
- Los enlaces con UTM completos (`/probar/<ruta>?utm_source=…`) solo sirven donde se pueden pulsar (LinkedIn, mensajes), no en TikTok.
- No se mide el clic, solo quien contesta la prueba o crea cuenta; los clics salen de las estadísticas de TikTok.

## Producción

- Plantilla de la serie: `.tmp/heraldo/streakode-output-serie/` (comp.html + ep.js por episodio, onetake). 0 créditos.
- Vídeos de producto (13/10): 05 Hopper, 06 Protectores, 07 Test de nivel, en `.tmp/heraldo/streakode-producto/` (README con los pasos y el motor en `.tmp/onetake_engine/`). Las tarjetas replican la app con sus colores reales y los textos salen de los strings de la app; fondo, rótulos (Geist Mono) y cierre son los de la cuenta. Cierre: «Pruébalo sin cuenta · 21 días de Pro». Descripción de producto: qué cambia en una frase + `streakode.com/tiktok` + 5 hashtags, sin emojis; comentario fijado con una pregunta.
