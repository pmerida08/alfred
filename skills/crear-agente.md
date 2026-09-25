# Skill: crear-agente

**Cuándo:** Pablo quiere un agente nuevo para un dominio ("crea un agente para X"). Basta con nombre, dominio y qué hará; el resto se deduce.

## Qué crear

`agents/<id>/` (id en minúsculas, sin espacios ni acentos; si ya existe, avisar antes de sobrescribir):

- `CLAUDE.md`: el único fichero que se lee al trabajar como el agente. Estructura de los actuales (FORGE, HUNTER…):
  1. Título y un párrafo con qué hace y para quién, y en qué se nota su criterio.
  2. **Tono**, en una o dos líneas.
  3. **Datos**: rutas, IDs de Notion (data source y propiedades con sus valores válidos), scripts. Solo lo que no se deduce.
  4. **Cómo trabaja**: los casos habituales y sus reglas, explicando el porqué cuando no sea obvio.
  5. **Límites**: qué hace sin preguntar y qué necesita confirmación.
  6. Una línea final para apuntar en su memoria.
- `directives/`: solo si hay procesos largos con pasos o trampas propias (como HUNTER). Si cabe en el `CLAUDE.md`, va ahí.
- `memory/` con un `.gitkeep`.

Escríbelo como a un colega competente: qué hace falta saber y por qué, sin mayúsculas de alarma ni reglas que el modelo ya cumple solo (ser conciso, verificar, no inventar).

## Registrar

- Una fila en la tabla «Agentes y dominios» del `CLAUDE.md` raíz.
- Una fila en `agents/AGENTS.md`.

Confirma a Pablo en una línea qué se creó y cómo invocarlo.
