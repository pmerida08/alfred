# Streakode — generar un lote de contenido

## Objetivo

Añadir ejercicios, problemas o retos a Streakode (`D:\Proyectos\Streakode`) sin API de
pago: Alfred los escribe y los scripts del proyecto los verifican antes de publicarlos.
Formato y reglas de verificación: `docs/CONTENIDO.md` del proyecto.

## Cuándo

- Pablo lo pide ("hazme un lote de Kotlin", "faltan retos").
- Una ruta se queda corta: el resumen de `build-seed` muestra pocos ejercicios de un nivel
  o la ruta no llega a la XP de los logros.
- Sale una versión nueva de un lenguaje o framework (ver "Versiones").

## Inputs

- Ruta y cantidad. Por defecto, 30 ejercicios por lote: 10 de nivel 1 y 20 de nivel 2.
- Temario de Pablo en `D:\Programas\codigos\<Lenguaje>`: priorizar lo que está estudiando.
- Versión de referencia de la ruta (`content/tracks.json`) y lo que ya existe (leer los
  lotes anteriores para no repetir temas ni slugs).

## Proceso

1. `node scripts/build-seed.mjs` y leer la tabla del final: ejercicios por nivel, problemas
   por nivel y XP de cada ruta.
2. Escribir el lote en `content/ejercicios/<ruta>/lote-NN.json`, o añadir problemas en
   `content/problemas/<ruta>.mjs` y retos en `content/desafios/retos.mjs`.
3. Marcar con `verify` todo lo que se pueda ejecutar (JS, TS, Python, Java y Kotlin).
   Para `fill_blank`, `parsons` y `find_bug`, añadir `output` (y `fix` en `find_bug`).
4. Por cada problema o reto nuevo, escribir `content/soluciones/<slug>.py` leyendo solo el
   enunciado.
5. `npm run content`. Si algo falla, **corregir el contenido**: la opción marcada, el
   enunciado o `solve()`. No relajar las comprobaciones para que pase.
6. Si hace falta más variedad de respuestas (menos de 20 distintas en 24 variantes),
   ampliar los rangos de `generate` o combinar dos datos en la respuesta.
7. `npm run db:content` con Supabase local encendido y probar al menos un ejercicio del
   lote en la app (`streakode-dev`, puerto 4730).
8. Commit en el repo del proyecto: `feat(contenido): lote NN de <ruta>`. Sin push.
9. Apuntar en el log del vault (`Proyectos/Streakode/log.md`) qué se añadió.

## Edge cases

- **Frameworks (Angular, React, React Native):** no se ejecutan. Solo afirmaciones de las
  que haya certeza; ante la duda sobre una API reciente, consultar la documentación
  oficial antes de escribir el ejercicio.
- **Novedades que la máquina local no ejecuta** (Java 21+, Python 3.14): marcar `minJava`
  o `minPython`. Salen como omitidos y hay que revisarlos leyendo con más cuidado.
- **Parsons con varios órdenes válidos:** el enunciado fija el orden o se rehace.
- **Kotlin tarda unos 5 s por ejercicio** en verificarse; los resultados se guardan en
  caché y solo se vuelven a ejecutar los que cambian.
- **Borrar contenido ya publicado** borra también los intentos de los usuarios si se hace
  con `db:reset`: preguntar a Pablo antes.

## Versiones

Al salir una versión nueva (Java cada marzo y septiembre, Python cada octubre, Angular dos
veces al año, React Native cada dos meses):

1. Actualizar `language_version` en `content/tracks.json`.
2. Buscar ejercicios que digan "desde Java N" o similar y comprobar que siguen siendo
   ciertos.
3. Añadir un lote con las novedades estables, nunca las que siguen en preview.

## Output

Lote en el repo, `npm run content` en verde, commit local y una línea en el log del vault.
