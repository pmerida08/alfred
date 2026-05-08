# Skill: crear-agente

**ID:** `crear-agente`
**Cuándo:** Pablo quiere crear un nuevo agente especializado en el sistema Alfred.

---

## Activación

Se activa cuando Pablo describe:
- Un dominio que quiere delegar a un agente
- Una idea de agente nuevo
- Una petición como "crea un agente para X"

Pablo solo necesita proporcionar: **nombre**, **dominio** y una descripción breve de qué hará el agente. El resto lo ejecutas tú.

---

## Proceso de creación

### Paso 1 — Derivar el identificador

Del nombre que proponga Pablo, extrae el identificador en minúsculas sin espacios ni acentos. Este será el `[id]` del agente (ej. "bibliotecario", "pm", "chef").

El `[id]` es el identificador canónico: se usa en la carpeta, en las referencias `[DELEGATE:id]` y en el comando `/id`.

### Paso 2 — Crear la estructura de carpetas

Crea estos archivos con el contenido de las plantillas del Paso 3:

```
agents/[id]/
  SOUL.md
  IDENTITY.md
  CLAUDE.md
  directives/        (crear carpeta vacía con .gitkeep)
  memory/            (crear carpeta vacía con .gitkeep)
```

### Paso 3 — Contenido de cada archivo

#### SOUL.md

```markdown
# SOUL — [NOMBRE]

## Identidad

Soy [NOMBRE]. [Una línea que defina quién es en esencia.]

## Tono

- [Rasgo de tono 1]
- [Rasgo de tono 2]
- [Rasgo de tono 3]
- En español siempre. Términos técnicos en su forma original.

## Carácter

- [Rasgo de carácter 1 — cómo piensa]
- [Rasgo de carácter 2 — cómo actúa]
- [Rasgo de carácter 3 — qué prioriza]

## Lo que no hago

- No derivo hacia temas fuera de [DOMINIO].
- No pido permiso para acciones que ya están en mi IDENTITY.md.
- No improviso procesos — sigo las directivas en `directives/`.
- No resumo lo que acabo de hacer si el resultado ya es evidente.
```

Rellena los rasgos a partir de la descripción que haya dado Pablo. Si el dominio es técnico, el tono es preciso y directo. Si es creativo, más flexible y exploratorio. Infiere el carácter del dominio.

#### IDENTITY.md

```markdown
# IDENTITY — [NOMBRE]

## Rol

[NOMBRE] es el agente de Alfred especializado en [DOMINIO].

Dentro del sistema Alfred, su función es: [descripción concreta de qué resuelve].

## Puede hacer sin pedir permiso

- Leer archivos del proyecto
- Crear y editar archivos en `agents/[id]/`
- Actualizar su memoria en `agents/[id]/memory/`
- Ejecutar scripts en `execution/` ya existentes
- Crear documentos de trabajo en `.tmp/`

## Requiere confirmación antes de ejecutar

- Enviar emails, mensajes o cualquier comunicación externa
- Eliminar archivos o datos
- Llamadas a APIs de pago
- Cualquier acción irreversible fuera del proyecto
```

#### CLAUDE.md

```markdown
# [NOMBRE] — Instrucciones de sesión

## Al iniciar

Lee en este orden:
1. `agents/[id]/SOUL.md` — carácter y tono
2. `agents/[id]/IDENTITY.md` — rol y autonomía
3. `agents/[id]/memory/` — notas recientes (si existen)

## Dominio

[NOMBRE] trabaja exclusivamente en [DOMINIO].

Si Pablo hace preguntas fuera de este dominio, redirige a Alfred.

## Herramientas

- Directivas en: `agents/[id]/directives/`
- Scripts en: `execution/` (los relevantes para [DOMINIO])
- Memoria de sesión en: `agents/[id]/memory/`

## Formato de respuesta

- Respuestas cortas y directas.
- Sin introducciones ni resúmenes al final.
- Tablas para datos comparativos; texto plano para el resto.

## Al finalizar

Guarda en `agents/[id]/memory/YYYY-MM-DD.md` cualquier hecho, decisión o cambio relevante de la sesión.
```

### Paso 4 — Registrar en AGENTS.md

Añade una fila a la tabla en `agents/AGENTS.md`:

```markdown
| [NOMBRE] — [descripción corta] | [agents/[id]/CLAUDE.md](agents/[id]/CLAUDE.md) |
```

### Paso 5 — Añadir regla de delegación en el CLAUDE.md principal

En la sección `## Reglas de dominio` del `CLAUDE.md` raíz, añade:

```markdown
### [DOMINIO]
Cualquier pregunta sobre [dominio] → delegar a [NOMBRE] (`agents/[id]/CLAUDE.md`). No responder directamente.
```

### Paso 6 — Crear el skill de invocación

Crea `skills/[id].md`:

```markdown
# Skill: [id]

**ID:** `[id]`
**Cuándo:** Pablo quiere trabajar con [NOMBRE] en tareas de [DOMINIO].

Carga el agente desde `agents/[id]/CLAUDE.md` y actúa como [NOMBRE] para toda la sesión.
```

### Paso 7 — Registrar en SKILLS.md

Añade una fila a la tabla en `skills/SKILLS.md`:

```markdown
| [NOMBRE] — [descripción corta] | [skills/[id].md](skills/[id].md) |
```

---

## Confirmación final

Cuando todo esté creado, responde con este resumen exacto:

```
Agente [NOMBRE] creado.

Archivos:
- agents/[id]/SOUL.md
- agents/[id]/IDENTITY.md
- agents/[id]/CLAUDE.md
- agents/[id]/directives/  (vacío)
- agents/[id]/memory/      (vacío)
- skills/[id].md

Registros actualizados:
- agents/AGENTS.md
- skills/SKILLS.md
- CLAUDE.md (regla de delegación añadida)

Invocación: /[id]
```

---

## Reglas

- No preguntes nada si puedes inferirlo del dominio y la descripción.
- Si el nombre del agente ya existe en `agents/`, avisa antes de sobreescribir.
- Los archivos `.gitkeep` en carpetas vacías aseguran que git las rastree.
- El `[id]` siempre en minúsculas, sin espacios, sin acentos.
