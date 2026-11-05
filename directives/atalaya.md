# Directiva: Atalaya, estado de los proyectos

**Dominio:** Proyectos
**Qué es:** panel de control de todos los proyectos de Pablo. El código está en `D:\Proyectos\Atalaya`; corre en el servidor Linux (Postgres + web en Docker, http://192.168.1.200:4770) y en el PC se usa como http://localhost:4770 (el lanzador reenvía al servidor). Es la **fuente de verdad** de qué proyecto está activo, en pausa, terminado o abandonado, su prioridad, su siguiente paso y si cuenta para el CV.
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
6. **Pablo pide arrancar o abrir un proyecto** («arráncame Remopo», «ábreme Streakode»): `python execution/atalaya.py iniciar <slug>`. Abre una consola con el comando de arranque y el navegador cuando responde. Necesita el lanzador, que arranca solo al iniciar sesión (tarea programada «Atalaya - lanzador»); si no responde, relanzarlo con `Start-ScheduledTask -TaskName 'Atalaya - lanzador'`. El comando y la URL de cada proyecto se guardan en Atalaya (`comando_inicio`, `url_local`) y se editan con `set`.

## Qué no hacer

- No marcar un proyecto como terminado o abandonado por deducción. Si parece muerto, preguntarlo y, si Pablo confirma, cerrarlo con `motivo_cierre`.
- No escribir la actividad a mano: la saca Atalaya de git cada 20 minutos (o con `sync`).
- No duplicar en la memoria de Alfred el estado de los proyectos: se consulta aquí. La ficha de Obsidian (`Proyectos/<Nombre>/`) sigue siendo el sitio del detalle técnico.

## Edge cases

- **Atalaya no responde en el PC**: o el lanzador no está en marcha (`Start-ScheduledTask -TaskName 'Atalaya - lanzador'`) o el servidor está apagado (`curl http://192.168.1.200:4770/api/salud`). En el servidor se levanta con `cd ~/Documentos/Atalaya && docker compose up -d`.
- **Servidor Linux / Telegram**: Atalaya corre ahí mismo, así que `resumen`, `ver`, `set`, `nuevo` y `cv` funcionan igual. La actividad de git la lee el PC: si está apagado, el resumen lo avisa y los días sin actividad son de la última lectura, y `sync` falla con ese aviso. `iniciar` no funciona desde el servidor (abre ventanas en el PC).
- **Código de Atalaya**: se edita en el PC; Syncthing lo copia al servidor (carpeta «Atalaya», solo PC → servidor, sin `node_modules` ni `.git`). Cambios en `public/` o `server/`: `docker restart atalaya-app` en el servidor; en `package.json` o el `Dockerfile`: `docker compose up -d --build`. Si cambia el lanzador (`lanzador/`), reiniciarlo en el PC.
- **Proyectos marcados «por confirmar»** (`revisar = true`): su estado lo dedujo Alfred al crear el inventario. Tratarlo como provisional y, si sale el tema, pedir a Pablo que lo confirme.
