# Kanto Idle

Juego incremental de Pokémon (fan game, sin ánimo de lucro), pensado para jugar en el móvil como PWA: se instala en la pantalla de inicio y funciona sin conexión.

## Cómo se juega

- **Tocar** al Pokémon salvaje le hace daño. Al derrotarlo ganas ₽ y EXP, y se intenta capturar (si aún no lo tienes).
- **Entrenadores** (pestaña Mejoras): se compran con ₽ y luchan solos. Cada 10, 25, 50, 100... que tengas de un tipo, su producción se duplica.
- **Equipo** (hasta 6 Pokémon): suben de nivel con cada victoria y multiplican el daño de todo lo demás. El nivel máximo lo marcan las medallas.
- **Zonas** (14, de la Ruta 1 a la Cueva Celeste): hay que derrotar 25 Pokémon para despejarlas. Cada zona tiene más vida y paga más.
- **Gimnasios y Liga**: combates con límite de tiempo. Dan medalla (más nivel máximo y más plazas de equipo) y abren zonas.
- **Pokédex**: 151 especies + shinies (1/1024 por aparición). Cada una da un bonus permanente de daño.
- **Nueva aventura** (prestige): reinicias a cambio de Caramelos Raros (+3% de daño cada uno, para siempre) y mejoras permanentes. Tras la Liga hay pisos infinitos en la Cueva Celeste.
- **Sin conexión**: los entrenadores y el equipo siguen luchando (50% de eficacia, hasta 8 h). No capturan.

## Estructura

```
public/            lo que se publica (arrastrar esta carpeta a Netlify)
  js/data.js       datos: Pokémon, zonas, gimnasios, entrenadores, mejoras, logros
  js/engine.js     reglas y fórmulas, sin DOM (por eso se puede simular en Node)
  js/ui.js         interfaz; el DOM se actualiza en sitio (en el móvil, un botón que se
                   reemplaza entre el toque y la suelta pierde el clic)
  js/main.js       bucle de juego, guardado, progreso offline, pantalla encendida
  sw.js            service worker (caché y modo sin conexión)
tools/sim.mjs      simulador de equilibrio: un jugador automático recorre el juego
tools/e2e*.mjs     pruebas en navegador (Playwright, viewport de móvil)
tools/icons.mjs    genera los iconos PWA
```

## Equilibrio (por qué los números son así)

El juego sigue el patrón clásico: los **costes crecen exponencialmente** (x1,15 por entrenador comprado) y la producción solo linealmente, y los hitos de x2 compensan. La **vida de los enemigos crece x3,1 por zona** y la **recompensa x2,3**, de modo que cada zona exige más poder del que da la anterior: ese desfase es lo que marca el ritmo. Tres capas de multiplicadores (nivel del equipo, Pokédex/logros/Caramelos, mejoras únicas) llevan al jugador de x1 a x10⁶ de poder.

`node tools/sim.mjs 2 12 1` simula 1 aventura con 2 toques/s. Resultado con los valores actuales: Liga a los ~65 min con un jugador perfecto (74 min sin tocar nada); una persona real tardará bastante más. Todos los parámetros están en `CFG` de `engine.js` y se pueden probar sin editar nada: `node tools/sim.mjs 2 12 1 '{"hpGrowth":3.4}'`.

## Desplegar en Netlify

**Opción A (la más rápida):** entra en https://app.netlify.com/drop y arrastra la carpeta `public` (o el zip que genera `tools/zip.sh`). Te da una URL `https://algo.netlify.app`.

**Opción B (se actualiza solo con cada push):** Netlify → *Add new site* → *Import from Git* → este repositorio. *Base directory*: `games/kanto-idle`. Sin comando de build. `netlify.toml` ya define `public` como carpeta de publicación y las cabeceras.

Cuando cambies archivos del juego, sube `VERSION` en `public/sw.js` para que los móviles refresquen la caché.

## Instalar en el móvil

Abre la URL en Chrome (Android) → menú → *Instalar aplicación*. En iPhone: Safari → Compartir → *Añadir a pantalla de inicio*.

## Aviso

Pokémon y sus nombres pertenecen a Nintendo, Game Freak y The Pokémon Company. Este proyecto es un homenaje de fans, no está afiliado a ellos y no se vende. Los sprites son de [PokeAPI/sprites](https://github.com/PokeAPI/sprites).
