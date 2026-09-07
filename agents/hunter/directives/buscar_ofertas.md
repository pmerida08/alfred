# Directiva: Buscar ofertas y generar paquete de candidatura

## Objetivo

Buscar en Internet ofertas de empleo que encajen con el perfil de Pablo, generar para cada una el paquete completo (análisis, CV HTML adaptado y carta de presentación), registrarlo en Notion y **devolver al chat los materiales listos para enviar** (carta, link de la oferta y CV).

Esta es la directiva "todo en uno". Reutiliza `analizar_oferta.md` y `generar_materiales.md` como subprocesos; no los reescribe.

## Trigger

Pablo pide buscar ofertas, encontrar trabajo, "búscame curro", "tráeme ofertas", o similar. Ejecutable desde Claude Code y desde el bot de Telegram.

## Inputs

- CV de Pablo: `D:\Obsidian\Mi Bóveda\raw\docs\Pablo Mérida Velasco — CV.pdf` (leer al inicio, no asumir de memoria)
- Nº de ofertas a procesar: **3 por defecto**. Si Pablo indica otro número o un criterio ("solo IA", "remoto", "en Madrid"), respetarlo.
- Filtros opcionales de Pablo: stack, modalidad (remoto/híbrido/presencial), ubicación, seniority.

## Proceso

### 0. Preparar el outbox (SIEMPRE primero)

Vaciar y recrear la carpeta `D:\Programas\Alfred\.tmp\hunter_outbox\`. Es el buzón de salida: todo fichero que HUNTER deje ahí se adjunta automáticamente al chat de Telegram al terminar. Limpiarla al inicio evita reenviar materiales de ejecuciones anteriores.

```powershell
$outbox = "D:\Programas\Alfred\.tmp\hunter_outbox"
if (Test-Path $outbox) { Remove-Item "$outbox\*" -Force -ErrorAction SilentlyContinue }
New-Item -ItemType Directory -Force -Path $outbox | Out-Null
```

### 1. Leer el CV

Leer el PDF completo. Extraer stack real, proyectos y seniority para definir qué buscar. No inventar perfil.

### 2. Buscar ofertas en Internet

Usar `WebSearch` con consultas derivadas del perfil real de Pablo (full-stack / Python / IA generativa / junior, según el CV). Combinar términos del perfil con portales de empleo.

- Lanzar varias consultas (p. ej. el rol + "ofertas", el stack + "trabajo remoto España", el rol en portales como LinkedIn, InfoJobs, Tecnoempleo).
- Para cada candidata, abrir la oferta (`WebFetch`) y extraer: empresa, puesto, descripción, requisitos, ubicación/modalidad, **URL canónica de la oferta**.
- Descartar las que no tengan URL accesible o descripción suficiente para analizar.
- Seleccionar las N mejores por encaje aparente con el perfil (N = nº pedido, 3 por defecto).

### 3. Filtrar duplicados (OBLIGATORIO)

Antes de procesar, consultar la BD de Notion (ver `IDENTITY.md`). Para cada oferta candidata, si ya existe una candidatura con misma empresa+puesto en estado `"Solicitud enviada"`, **omitirla** y buscar otra para completar el cupo. Informar brevemente de las omitidas.

### 4. Por cada oferta seleccionada

Ejecutar en orden, reutilizando las directivas existentes:

1. **Analizar** — seguir `analizar_oferta.md`: requisitos, cruce con CV, fit score 1-10.
   - Si fit score < 4: no generar materiales para esa oferta; anotarla como descartada con el motivo y, si es posible, buscar una sustituta.
2. **Generar materiales** — seguir `generar_materiales.md`:
   - **Idioma:** mismo que la oferta (regla obligatoria de `generar_materiales.md`).
   - Carta de presentación (≤300 palabras, sin frases hechas).
   - CV HTML adaptado y guardado en las dos rutas habituales (`D:\Obsidian\Mi Bóveda\Empleos\` y `agents/hunter/candidaturas/`), con foto en base64.
3. **Registrar en Notion** — crear/actualizar la candidatura: empresa, puesto, fecha, fit score, **URL de la oferta**, estado `"Materiales listos"`. Crear las páginas hijo (Carta de presentación, Notas CV, CV HTML con su ruta).
4. **Copiar al outbox** — dejar en `D:\Programas\Alfred\.tmp\hunter_outbox\` los ficheros enviables de esta oferta:
   - El CV: `CV-{Empresa}-{Puesto}.html`
   - La carta en texto plano: `Carta-{Empresa}-{Puesto}.txt` (para copiar y pegar en formularios)
   - La carta en HTML imprimible: `Carta-{Empresa}-{Puesto}.html`

   Sanitizar nombres igual que en `generar_materiales.md` (sin espacios ni caracteres especiales, guiones).

### 5. Devolver el paquete al chat

Tras procesar todas, responder en el chat con un bloque por oferta. Este texto es lo que Pablo lee y usa para enviar:

```
═══ Oferta 1/N ═══
Empresa — Puesto · Fit X/10 · [Remoto/Híbrido/Presencial]
Oferta: <URL de la oferta>

CARTA DE PRESENTACIÓN
<texto completo de la carta, listo para copiar y pegar>

CV y carta: adjuntos (CV-Empresa-Puesto.html · Carta-Empresa-Puesto.html)
Registrado en Notion ✓
```

- Incluir **siempre** el link de la oferta y el texto íntegro de la carta en el chat (Pablo los reenvía directamente).
- Mencionar que el CV va adjunto. En Telegram los `.html` y `.txt` del outbox se envían como documentos automáticamente tras este mensaje. En Claude Code, enlazar además la ruta local clicable del HTML.
- Cerrar con un resumen de una línea: cuántas procesadas, cuántas omitidas (duplicadas) y cuántas descartadas (fit bajo).

## Salidas

1. Materiales en disco (CV HTML en las dos rutas habituales).
2. Candidaturas registradas en Notion en estado `"Materiales listos"` con la URL de la oferta.
3. Ficheros en `.tmp\hunter_outbox\` (CV + carta por oferta) → adjuntados en Telegram.
4. Mensaje de chat con carta + link por oferta.

## Edge cases

- **No se encuentran ofertas con la búsqueda:** ampliar términos o pedir a Pablo que afine el criterio. No inventar ofertas ni URLs.
- **URL de oferta caduca o sin acceso:** descartar y buscar otra; nunca registrar una candidatura sin URL real.
- **Todas las candidatas son duplicadas (ya enviadas):** informar y ofrecer buscar con otros términos.
- **Fit score < 4 en todas:** presentar el análisis pero no generar materiales hasta que Pablo confirme.
- **Ejecución desde Telegram:** no usar enlaces de fichero locales como entregable principal (el móvil no los abre); el CV llega como documento adjunto vía outbox y la carta+link van en el texto.
- **Outbox no vacío de una ejecución previa fallida:** el paso 0 lo limpia siempre; no asumir que está vacío.
