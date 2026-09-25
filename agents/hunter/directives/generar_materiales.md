# Directiva: generar CV y carta para una oferta

**Objetivo:** un CV HTML y una carta adaptados a una oferta ya analizada (`analizar_oferta.md`), que pasen un filtro ATS y que Pablo pueda enviar sin retocar.

**Inputs:** el análisis de la oferta, el CV base, `templates/cv_template.html`, `templates/carta_template.html` y `templates/fotoCv-web.jpg`.

## Idioma

Todo (CV, carta y notas) en el idioma de la **descripción de la oferta**, no del país ni de la empresa, salvo que Pablo pida otro.

En inglés: `<html lang="en">`; títulos de sección Profile, Skills, Experience, Featured Projects, Education, Languages & Certifications; teléfono con +34; fecha en formato inglés; `Re:` en la carta; marca de agua "Application prepared with Alfred · Personal AI Agent". Los nombres de proyectos y tecnologías no se traducen.

## Carta

Cuatro párrafos, hasta 300 palabras:

1. Por qué Pablo encaja, nombrando la empresa. Sin «Me dirijo a ustedes para…».
2. Dos o tres proyectos o logros reales del CV que respondan a los requisitos de la oferta.
3. Qué le atrae del puesto o de la empresa, sacado de la oferta, no inventado.
4. Disponibilidad y cierre directo.

Nada de frases hechas («perfil dinámico», «trabajo en equipo», «reto profesional»): tecnologías, proyectos y datos concretos. Tono profesional, sin servilismo.

Se entrega en texto plano y en HTML A4 desde `carta_template.html`, sustituyendo `SUBTITULO`, `CIUDAD_FECHA`, `EMPRESA`, `PUESTO`, `SALUDO`, `PARRAFOS` (un `<p>` por párrafo) y `DESPEDIDA`. Lleva la misma cabecera y la misma regla de marca de agua que el CV, para que los dos se lean como un paquete.

## CV

Parte de `cv_template.html` y adapta:

- `.subtitulo`: la denominación del puesto si hay una más precisa.
- Perfil: reescrito hacia los requisitos clave, con la misma extensión.
- Habilidades: dentro de cada categoría, primero las que pide la oferta.
- Experiencia: primero los bullets que más encajan.
- Proyectos: reordenados por relevancia, el más relevante primero.

No se inventan skills ni experiencias, no se quitan secciones ni proyectos (solo se reordenan) y tiene que caber en una página A4; si no cabe, baja márgenes o fuente 0,3 pt antes que quitar contenido.

**Marca de agua** «Candidatura preparada con Alfred»: solo cuando el **título del puesto** es explícitamente de IA (AI Engineer, AI Automation, Ingeniero de IA Generativa, Agentic AI, Especialista en IA…); ahí el propio CV demuestra que Pablo construye agentes. En cualquier otro puesto, o en caso de duda, quita el `<div class="watermark">` y su CSS del CV y de la carta.

### Reglas técnicas (cada una salió de un fallo real)

Medido con el evaluador de Aplico y el informe de TopCV (sep 2026): el CV genérico pasó de 37/100 a 97/100 aplicándolas.

1. **Foto en base64 y siempre la optimizada** (`fotoCv-web.jpg`, 300×300, ~10 KB), sustituyendo `PHOTO_BASE64`. La original de `raw/docs` pesa 525 KB e infla el CV. El HTML final ronda los 25 KB; por encima de 100 KB, se coló la original.
2. **Una sola columna.** El ATS lee línea a línea y en rejilla entrelaza columnas («IA & AUTOMATIZACIÓNLENGUAJES & FRAMEWORKS»). Habilidades: una línea por categoría (`<p><span class="skill-cat">Cat:</span> A · B · C</p>`); proyectos apilados en `.proyectos-lista`; educación, una línea por entrada.
3. **Puesto, empresa y fechas en una sola línea** de texto dentro de `.job-cabecera`, nunca en contenedores separados con `space-between`: el parser no los asocia y cuenta «0 años de experiencia».
4. **Cada proyecto con su fecha** en `.proyecto-nombre`; sin ellas el ATS ve un hueco desde junio de 2025.
5. **`letter-spacing` de los títulos de sección ≤ 0,5 px.** Con 1,6 px el ATS leía «E X P E R I E N C I A», no reconocía la sección y no contaba ningún empleo.
6. **Sin emoji en el contacto:** el parser no reconocía el teléfono ni el email, y cada emoji añade ~32 KB al PDF. La separación la pone el `::after` con «·» de la plantilla.
7. **Enlaces de contacto como `<a href>`:** GitHub `https://github.com/pmerida08`, portfolio `https://pmerida-portfolio.netlify.app`, LinkedIn `https://linkedin.com/in/pablo-merida-velasco`.
8. **Bullets CSS con escape Unicode** (`content: "\2022"`); las entidades HTML salen como texto literal.
9. **Se mantiene el layout flex** de `body` y `.contenido` (reparte las secciones en la página) y `min-height: 297mm`, nunca `height` + `overflow: hidden`, que corta texto sin avisar.
10. **Escritura en UTF-8 explícito** (`[System.IO.File]::WriteAllText` o Python con `encoding="utf-8"`); `Out-File` genera UTF-16.

Para comprobar que cabe en una página, renderiza a PDF con Chrome headless.

## Dónde se guarda

- `D:\Obsidian\Mi Bóveda\Empleos\CV-{Empresa}-{Puesto}.html` y `Carta-{Empresa}-{Puesto}.html`.
- Copia con el mismo nombre en `agents/hunter/candidaturas/`.
- Nombres sin espacios ni caracteres especiales, con guiones.

## Notion

Crea o actualiza la candidatura (`Estado = Materiales listos`, fecha, fit, URL de la oferta) y tres páginas hijo: «Carta de presentación» (texto, con la ruta del HTML al final), «Notas CV» (hasta 6 viñetas: qué se reordenó, qué keywords reales se metieron, qué pesa menos) y «CV HTML» (la ruta del archivo).

## Edge cases

- **Fit < 4:** avisar antes de generar y seguir solo si Pablo confirma.
- **Empresa sin nombre claro:** «su empresa» en la carta, y señalarlo para revisión.
- **Ningún proyecto encaja directamente:** usa la experiencia más transferible y dilo en las notas.
