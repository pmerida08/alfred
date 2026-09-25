# Directiva: Atalaya, estado de los proyectos

**Dominio:** Proyectos
**Qué es:** panel de control de todos los proyectos de Pablo, en `D:\Proyectos\Atalaya` (Postgres en Docker + web en http://localhost:4770). Es la **fuente de verdad** de qué proyecto está activo, en pausa, terminado o abandonado, su prioridad, su siguiente paso y si cuenta para el CV.
**Herramienta:** `python execution/atalaya.py` (ver `--help`).
**Autonomía:** leer siempre sin preguntar. Actualizar el siguiente paso, la descripción o las notas tras trabajar en un proyecto, sin preguntar. **Cambiar el estado o el interruptor del CV solo si Pablo lo dice** o lo confirma: son decisiones suyas.

---

## Cuándo usarla

1. **Al hablar de un proyecto o antes de proponer en qué trabajar**: `python execution/atalaya.py resumen`. Da los activos por prioridad, lo que se enfría, las pausas largas y los avisos. Leerlo antes de opinar, no después.
2. **Cuando Pablo quiera empezar algo nuevo**: mirar cuántos activos hay frente al límite (3 por defecto). Si ya está en el límite, decírselo y preguntar qué pausa. El objetivo del panel es que no se acumulen proyectos a medias.
3. **Al terminar una sesión de trabajo en un proyecto**: actualizar el siguiente paso con lo que quede pendiente de verdad:
   `python execution/atalaya.py set <slug> "siguiente_paso=..."`
4. **Proyecto nuevo** (carpeta nueva en `D:\Proyectos`): registrarlo con
   `python execution/atalaya.py nuevo "Nombre" estado=activo "ruta=D:\Proyectos\X" "descripcion=..."`.
   Atalaya también lista las carpetas sin registrar en el resumen.
5. **HUNTER, al adaptar un CV**: `python execution/atalaya.py cv` da los proyectos marcados para el CV con su texto (`cv_resumen`; si está vacío, `descripcion`). Respetar además la regla de proyectos destacados (LifeVault, Alfred, Estudiante Élite).

## Qué no hacer

- No marcar un proyecto como terminado o abandonado por deducción. Si parece muerto, preguntarlo y, si Pablo confirma, cerrarlo con `motivo_cierre`.
- No escribir la actividad a mano: la saca Atalaya de git cada 20 minutos (o con `sync`).
- No duplicar en la memoria de Alfred el estado de los proyectos: se consulta aquí. La ficha de Obsidian (`Proyectos/<Nombre>/`) sigue siendo el sitio del detalle técnico.

## Edge cases

- **Atalaya no responde**: el script lo dice. Arrancarlo con `docker compose -f D:/Proyectos/Atalaya/docker-compose.yml up -d` (Docker Desktop tiene que estar abierto).
- **Servidor Linux / Telegram**: Atalaya solo corre en el PC de Windows. Desde el servidor, decir que no está disponible en vez de improvisar el estado.
- **Proyectos marcados «por confirmar»** (`revisar = true`): su estado lo dedujo Alfred al crear el inventario. Tratarlo como provisional y, si sale el tema, pedir a Pablo que lo confirme.
