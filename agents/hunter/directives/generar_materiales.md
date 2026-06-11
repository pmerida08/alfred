# Directiva: Generar materiales de candidatura

## Objetivo

Producir una carta de presentación y notas de adaptación del CV para una oferta concreta, guardarlos en Notion como páginas hijo de la candidatura correspondiente.

## Prerequisito

Esta directiva solo se ejecuta después de haber completado `analizar_oferta.md`. No generar materiales sin análisis previo.

## Inputs

- Análisis de la oferta (resultado de `analizar_oferta.md`)
- CV de Pablo: `D:\Obsidian\Mi Bóveda\raw\docs\Pablo Mérida Velasco — CV.pdf`
- Template HTML: `D:\Programas\Alfred\agents\hunter\templates\cv_template.html`
- Foto CV: `D:\Obsidian\Mi Bóveda\raw\docs\fotoCv.jpg` (ya referenciada en el template)
- Idioma objetivo: mismo que la oferta, salvo indicación de Pablo

## Proceso

### 0. Idioma de los materiales (REGLA OBLIGATORIA)

Todos los materiales (CV HTML, carta de presentación y notas de adaptación) se generan **en el mismo idioma que la oferta**, salvo que Pablo indique explícitamente otro.

- Oferta en inglés → CV, carta y notas **en inglés**. En el CV HTML, ajustar `<html lang="en">`, los títulos de sección (Profile, Skills, Experience, Featured Projects, Education, Languages & Certifications) y el watermark ("Application prepared with Alfred · Personal AI Agent").
- Oferta en español → todo en español (`<html lang="es">`).
- Detectar el idioma por la **descripción de la oferta**, no por el nombre de la empresa ni por el país.
- No traducir nombres propios de proyectos (Alfred, LifeVault, Estudiante Élite) ni de tecnologías.
- Mantener el teléfono con prefijo internacional (+34) cuando los materiales sean en inglés.

> Aprendido en producción (2026-06-07): el CV de Kyndryl se pidió en inglés porque la oferta estaba en inglés. Aplicar este criterio por defecto a partir de ahora.

### 1. Carta de presentación

**Estructura:**

1. **Párrafo de apertura** (2-3 frases): por qué Pablo encaja con el puesto. Mencionar la empresa por nombre. Sin "Me dirijo a ustedes para...".
2. **Párrafo de experiencia** (3-4 frases): 2-3 logros o proyectos concretos del CV que sean directamente relevantes a los requisitos de la oferta.
3. **Párrafo de motivación** (2-3 frases): qué le atrae del puesto o la empresa específicamente (inferir del contexto de la oferta, no inventar).
4. **Cierre** (1-2 frases): disponibilidad y llamada a la acción directa.

**Reglas:**
- Longitud máxima: 300 palabras.
- No usar frases hechas: "perfil dinámico", "trabajo en equipo", "reto profesional".
- Datos concretos: nombres de tecnologías, años de experiencia, proyectos reales del CV.
- Tono: profesional, directo, sin servilismo.

### 2. Notas de adaptación del CV

Un listado breve de qué ajustar en el CV para esta oferta:
- Qué experiencias o proyectos mover al principio
- Qué keywords de la oferta incorporar (si están respaldadas por experiencia real)
- Qué secciones o items son menos relevantes para esta oferta

Formato: lista con viñetas, máximo 6 puntos.

### 3. CV HTML adaptado

Partiendo del template `D:\Programas\Alfred\agents\hunter\templates\cv_template.html`, generar un CV HTML personalizado para la oferta.

**Qué adaptar en el template:**

| Zona | Qué cambiar |
|------|-------------|
| `.subtitulo` | Ajustar el título si el puesto target tiene una denominación más precisa |
| Párrafo PERFIL | Reescribir orientado a los requisitos clave de la oferta (misma extensión) |
| HABILIDADES | Reordenar skills: las más relevantes para la oferta, primero dentro de su columna |
| EXPERIENCIA bullets | Poner en primer lugar los bullets que más encajan con la oferta |
| PROYECTOS | Reordenar los 4 proyectos: el más relevante arriba-izquierda, el segundo arriba-derecha |

**Reglas de producción:**
- No inventar skills ni experiencias no presentes en el CV original.
- No eliminar secciones ni reducir número de proyectos — solo reordenar.
- El resultado debe caber en una sola página A4 sin scroll.

**Reglas técnicas obligatorias (aprendidas en producción):**

1. **Foto siempre en base64.** Las rutas relativas no funcionan desde todas las ubicaciones. Usar PowerShell para incrustar la foto directamente en el HTML:
   ```powershell
   $b64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes("D:\Obsidian\Mi Bóveda\raw\docs\fotoCv.jpg"))
   ```
   Luego reemplazar `PHOTO_BASE64` del template con el valor obtenido.

2. **Bullets CSS: usar escape Unicode, nunca entidades HTML.** En la propiedad CSS `content:`, las entidades HTML (`&#8226;`) se renderizan como texto literal. Usar siempre `content: "\2022"`.

3. **Layout flex obligatorio.** El body y `.contenido` ya tienen `display: flex; flex-direction: column` en el template. No eliminar — es lo que distribuye las secciones para llenar la página completa sin espacios en blanco.

4. **Escritura del archivo: usar `[System.IO.File]::WriteAllText` con UTF-8 explícito** para preservar acentos y caracteres especiales. No usar `Out-File` por defecto (genera UTF-16).

5. **Links de contacto: siempre `<a href>`, nunca `<span>`.** GitHub, portfolio y LinkedIn deben ser enlaces clicables:
   - GitHub → `https://github.com/pmerida08`
   - Portfolio → `https://pmerida-porfolio.netlify.app`
   - LinkedIn → `https://linkedin.com/in/pablo-merida-velasco`

**Guardar en dos rutas:**
1. `D:\Obsidian\Mi Bóveda\Empleos\CV-{Empresa}-{Puesto}.html` — para abrir en navegador e imprimir
2. `D:\Programas\Alfred\agents\hunter\candidaturas\CV-{Empresa}-{Puesto}.html` — copia local en el proyecto

(sanitizar nombre: sin espacios, sin caracteres especiales, usar guiones; mismo nombre en ambas rutas)

### 4. Guardar en Notion

1. Buscar la candidatura correspondiente en la BD de Notion.
   - Si no existe, crearla primero con los datos básicos (empresa, puesto, fecha, estado: "Analizada", fit score).
2. Crear tres páginas hijo dentro de la candidatura:
   - **"Carta de presentación"** con el texto generado
   - **"Notas CV"** con la lista de adaptaciones
   - **"CV HTML"** con la ruta local del archivo generado: `D:\Obsidian\Mi Bóveda\Empleos\CV-{Empresa}-{Puesto}.html`
3. Actualizar el campo estado a "Materiales listos" si existía como "Analizada".

## Edge cases

- **Fit score < 4:** avisar a Pablo antes de generar. Proceder solo si confirma.
- **Empresa sin nombre claro:** usar "su empresa" en la carta, marcar para revisión.
- **CV sin proyectos directamente relevantes:** usar la experiencia más transferible y explicitarlo en las notas CV.
- **CV HTML no cabe en una página:** reducir márgenes o tamaño de fuente en 0.3pt; nunca eliminar contenido.
