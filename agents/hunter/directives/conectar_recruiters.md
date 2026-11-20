# Conectar con IT Recruiters en LinkedIn

**Objetivo:** ampliar la red de Pablo con recruiters de perfiles tech en España enviando 20 invitaciones sin nota por día laborable. Lo ordenó Pablo el 2026-11-19 («haz eso todos los días»); no hace falta pedir confirmación en cada ejecución.

## Herramienta

Claude in Chrome sobre Brave (sesión de LinkedIn de Pablo). Si `list_connected_browsers` no lo muestra, Brave está cerrado o le falta abrir el panel lateral de la extensión: no se puede hacer nada, se apunta en la nota del día y se termina.

## Pasos

1. Elegir la búsqueda del día, rotando por día de la semana para no agotar los mismos resultados:
   - lunes: `IT Recruiter`
   - martes: `Technical Recruiter`
   - miércoles: `Tech Recruiter`
   - jueves: `Talent Acquisition IT`
   - viernes: `IT Recruiter` empezando en la página 3
2. Abrir `https://www.linkedin.com/search/results/people/?keywords=<búsqueda>&geoUrn=%5B%22105646813%22%5D&page=<n>` (filtro España). Comprobar en la captura que el filtro «Ubicaciones» está aplicado; si no, quitar `geoUrn` y quedarse solo con perfiles cuya ubicación ponga España.
3. Con `find`, localizar los enlaces «Invita a <nombre> a conectar». Para cada uno: clic → esperar **2 s** → «Enviar sin nota» → esperar 2 s. Con 1 s de espera alguna invitación se pierde.
4. Saltar perfiles que no sean de recruiting/talent acquisition, los que ya estén en «Pendiente» y los que solo tengan «Seguir» o «Mensaje».
5. Al acabar la página, pasar a la siguiente hasta sumar 20. Nunca más de 20 en un día.
6. Verificar al final con `find` de «Pendiente» en cada página usada; contar solo las confirmadas.
7. Cerrar la pestaña.

## Paradas

- Si LinkedIn muestra un aviso de límite semanal de invitaciones, un CAPTCHA, una verificación de identidad o pide email para conectar: parar en seco, no reintentar ni resolver nada, y avisar a Pablo en la nota del día.
- Nunca añadir nota, nunca enviar mensajes, nunca retirar invitaciones.

## Registro

- `agents/hunter/memory/YYYY-MM-DD.md`: búsqueda usada, páginas y la lista de nombres (empresa) confirmados.
- `memory/YYYY-MM-DD.md`: una línea con el número enviado o el motivo de la parada.
