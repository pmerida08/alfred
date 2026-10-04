// Datos estáticos del juego. Nada aquí cambia durante la partida.
// Formato Pokémon: [id, nombre, suma de stats base, ratio de captura, evolución]
// evolución: null | [idDestino, nivel] (nivel 0 = Piedra Evolutiva) | [[id1,id2,id3], 0] (Eevee)

const RAW = [
  [1, 'Bulbasaur', 318, 45, [2, 16]], [2, 'Ivysaur', 405, 45, [3, 32]], [3, 'Venusaur', 525, 45],
  [4, 'Charmander', 309, 45, [5, 16]], [5, 'Charmeleon', 405, 45, [6, 36]], [6, 'Charizard', 534, 45],
  [7, 'Squirtle', 314, 45, [8, 16]], [8, 'Wartortle', 405, 45, [9, 36]], [9, 'Blastoise', 530, 45],
  [10, 'Caterpie', 195, 255, [11, 7]], [11, 'Metapod', 205, 120, [12, 10]], [12, 'Butterfree', 395, 45],
  [13, 'Weedle', 195, 255, [14, 7]], [14, 'Kakuna', 205, 120, [15, 10]], [15, 'Beedrill', 395, 45],
  [16, 'Pidgey', 251, 255, [17, 18]], [17, 'Pidgeotto', 349, 120, [18, 36]], [18, 'Pidgeot', 479, 45],
  [19, 'Rattata', 253, 255, [20, 20]], [20, 'Raticate', 413, 127],
  [21, 'Spearow', 262, 255, [22, 20]], [22, 'Fearow', 442, 90],
  [23, 'Ekans', 288, 255, [24, 22]], [24, 'Arbok', 438, 90],
  [25, 'Pikachu', 320, 190, [26, 0]], [26, 'Raichu', 485, 75],
  [27, 'Sandshrew', 300, 255, [28, 22]], [28, 'Sandslash', 450, 90],
  [29, 'Nidoran♀', 275, 235, [30, 16]], [30, 'Nidorina', 365, 120, [31, 0]], [31, 'Nidoqueen', 505, 45],
  [32, 'Nidoran♂', 273, 235, [33, 16]], [33, 'Nidorino', 365, 120, [34, 0]], [34, 'Nidoking', 505, 45],
  [35, 'Clefairy', 323, 150, [36, 0]], [36, 'Clefable', 483, 25],
  [37, 'Vulpix', 299, 190, [38, 0]], [38, 'Ninetales', 505, 75],
  [39, 'Jigglypuff', 270, 170, [40, 0]], [40, 'Wigglytuff', 435, 50],
  [41, 'Zubat', 245, 255, [42, 22]], [42, 'Golbat', 455, 90],
  [43, 'Oddish', 320, 255, [44, 21]], [44, 'Gloom', 395, 120, [45, 0]], [45, 'Vileplume', 490, 45],
  [46, 'Paras', 285, 190, [47, 24]], [47, 'Parasect', 405, 75],
  [48, 'Venonat', 305, 190, [49, 31]], [49, 'Venomoth', 450, 75],
  [50, 'Diglett', 265, 255, [51, 26]], [51, 'Dugtrio', 405, 50],
  [52, 'Meowth', 290, 255, [53, 28]], [53, 'Persian', 440, 90],
  [54, 'Psyduck', 320, 190, [55, 33]], [55, 'Golduck', 500, 75],
  [56, 'Mankey', 305, 190, [57, 28]], [57, 'Primeape', 455, 75],
  [58, 'Growlithe', 350, 190, [59, 0]], [59, 'Arcanine', 555, 75],
  [60, 'Poliwag', 300, 255, [61, 25]], [61, 'Poliwhirl', 385, 120, [62, 0]], [62, 'Poliwrath', 510, 45],
  [63, 'Abra', 310, 200, [64, 16]], [64, 'Kadabra', 400, 100, [65, 36]], [65, 'Alakazam', 500, 50],
  [66, 'Machop', 305, 180, [67, 28]], [67, 'Machoke', 405, 90, [68, 40]], [68, 'Machamp', 505, 45],
  [69, 'Bellsprout', 300, 255, [70, 21]], [70, 'Weepinbell', 390, 120, [71, 0]], [71, 'Victreebel', 490, 45],
  [72, 'Tentacool', 335, 190, [73, 30]], [73, 'Tentacruel', 515, 60],
  [74, 'Geodude', 300, 255, [75, 25]], [75, 'Graveler', 390, 120, [76, 40]], [76, 'Golem', 495, 45],
  [77, 'Ponyta', 410, 190, [78, 40]], [78, 'Rapidash', 500, 60],
  [79, 'Slowpoke', 315, 190, [80, 37]], [80, 'Slowbro', 490, 75],
  [81, 'Magnemite', 325, 190, [82, 30]], [82, 'Magneton', 465, 60],
  [83, "Farfetch'd", 377, 45],
  [84, 'Doduo', 310, 190, [85, 31]], [85, 'Dodrio', 470, 45],
  [86, 'Seel', 325, 190, [87, 34]], [87, 'Dewgong', 475, 75],
  [88, 'Grimer', 325, 190, [89, 38]], [89, 'Muk', 500, 75],
  [90, 'Shellder', 305, 190, [91, 0]], [91, 'Cloyster', 525, 60],
  [92, 'Gastly', 310, 190, [93, 25]], [93, 'Haunter', 405, 90, [94, 40]], [94, 'Gengar', 500, 45],
  [95, 'Onix', 385, 45],
  [96, 'Drowzee', 328, 190, [97, 26]], [97, 'Hypno', 483, 75],
  [98, 'Krabby', 325, 225, [99, 28]], [99, 'Kingler', 475, 60],
  [100, 'Voltorb', 330, 190, [101, 30]], [101, 'Electrode', 490, 60],
  [102, 'Exeggcute', 325, 90, [103, 0]], [103, 'Exeggutor', 530, 45],
  [104, 'Cubone', 320, 190, [105, 28]], [105, 'Marowak', 425, 75],
  [106, 'Hitmonlee', 455, 45], [107, 'Hitmonchan', 455, 45], [108, 'Lickitung', 385, 45],
  [109, 'Koffing', 340, 190, [110, 35]], [110, 'Weezing', 490, 60],
  [111, 'Rhyhorn', 345, 120, [112, 42]], [112, 'Rhydon', 485, 60],
  [113, 'Chansey', 450, 30], [114, 'Tangela', 435, 45], [115, 'Kangaskhan', 490, 45],
  [116, 'Horsea', 295, 225, [117, 32]], [117, 'Seadra', 440, 75],
  [118, 'Goldeen', 320, 225, [119, 33]], [119, 'Seaking', 450, 60],
  [120, 'Staryu', 340, 225, [121, 0]], [121, 'Starmie', 520, 60],
  [122, 'Mr. Mime', 460, 45], [123, 'Scyther', 500, 45], [124, 'Jynx', 455, 45],
  [125, 'Electabuzz', 490, 45], [126, 'Magmar', 495, 45], [127, 'Pinsir', 500, 45], [128, 'Tauros', 490, 45],
  [129, 'Magikarp', 200, 255, [130, 20]], [130, 'Gyarados', 540, 45], [131, 'Lapras', 535, 45],
  [132, 'Ditto', 288, 35],
  [133, 'Eevee', 325, 45, [[134, 135, 136], 0]],
  [134, 'Vaporeon', 525, 45], [135, 'Jolteon', 525, 45], [136, 'Flareon', 525, 45],
  [137, 'Porygon', 395, 45],
  [138, 'Omanyte', 355, 45, [139, 40]], [139, 'Omastar', 495, 45],
  [140, 'Kabuto', 355, 45, [141, 40]], [141, 'Kabutops', 495, 45],
  [142, 'Aerodactyl', 515, 45], [143, 'Snorlax', 540, 25],
  [144, 'Articuno', 580, 3], [145, 'Zapdos', 580, 3], [146, 'Moltres', 580, 3],
  [147, 'Dratini', 300, 45, [148, 30]], [148, 'Dragonair', 420, 45, [149, 55]], [149, 'Dragonite', 600, 45],
  [150, 'Mewtwo', 680, 3], [151, 'Mew', 600, 45],
];

export const POKEMON = {};
for (const [id, name, bst, catchRate, evo] of RAW) {
  POKEMON[id] = { id, name, bst, catchRate, evo: evo || null, legendary: catchRate <= 3 || id === 151 };
}
export const DEX_SIZE = RAW.length;

// Piedras que consume cada rama de Eevee (solo cambia el texto, la piedra es genérica).
export const EEVEE_STONES = { 134: 'Piedra Agua', 135: 'Piedra Trueno', 136: 'Piedra Fuego' };

// Zonas. `pool` = [idPokémon, peso]. Los legendarios llevan peso muy bajo.
// `gym` = índice en GYMS del gimnasio que hay que ganar para pasar a la zona siguiente.
export const AREAS = [
  { name: 'Ruta 1', sub: 'Pueblo Paleta', hue: 110, pool: [[16, 5], [19, 5]] },
  { name: 'Bosque Verde', sub: 'Ruta 2', hue: 130, pool: [[10, 4], [13, 4], [11, 1.5], [14, 1.5], [16, 3], [19, 3], [25, 0.4]] },
  { name: 'Monte Moon', sub: 'Ruta 3', hue: 270, gym: 0, pool: [[41, 4], [74, 3], [46, 2], [35, 0.7], [27, 2], [21, 3], [39, 1], [56, 2], [138, 0.15], [140, 0.15]] },
  { name: 'Ruta 24 y 25', sub: 'Cabo Celeste', hue: 195, gym: 1, pool: [[23, 3], [43, 3], [69, 3], [63, 1.5], [48, 2], [52, 2], [56, 2], [16, 2], [17, 1.5], [20, 1.5], [54, 1.5], [29, 1.5], [32, 1.5], [1, 0.25], [4, 0.25], [122, 0.2], [133, 0.1]] },
  { name: 'Rutas 6 a 8', sub: 'Ciudad Carmín', hue: 35, gym: 2, pool: [[37, 2], [58, 2], [52, 2], [50, 2], [23, 1.5], [24, 1.5], [27, 2], [28, 1], [43, 1.5], [44, 1], [69, 1.5], [70, 1], [63, 1.5], [64, 0.5], [29, 1], [30, 0.8], [32, 1], [33, 0.8], [7, 0.25]] },
  { name: 'Túnel Roca', sub: 'Ruta 10', hue: 25, pool: [[66, 3], [74, 3], [75, 1.5], [95, 1], [41, 3], [42, 1.5], [96, 2], [97, 0.5], [100, 2], [81, 2], [27, 1.5], [28, 1], [108, 0.3]] },
  { name: 'Torre Pokémon', sub: 'Pueblo Lavanda', hue: 285, gym: 3, pool: [[92, 5], [93, 2.5], [94, 0.3], [104, 3], [105, 1], [109, 2], [88, 2], [41, 2], [42, 1.5], [96, 1.5], [97, 0.5]] },
  { name: 'Central Energía', sub: 'Ruta 10', hue: 55, pool: [[81, 3], [82, 2], [100, 3], [101, 2], [25, 2], [26, 0.5], [125, 0.4], [88, 1.5], [89, 1], [109, 1.5], [110, 1], [145, 0.12]] },
  { name: 'Zona Safari', sub: 'Ciudad Fucsia', hue: 95, gym: 4, pool: [[111, 2.5], [112, 1], [115, 0.5], [128, 1], [123, 0.7], [127, 0.7], [113, 0.4], [102, 2.5], [114, 1.2], [29, 1.5], [30, 1], [32, 1.5], [33, 1], [47, 1.5], [49, 1.5], [84, 2], [85, 1], [46, 1.5], [147, 0.3], [148, 0.1], [83, 0.5], [118, 1.5], [119, 1], [129, 2], [54, 1.5], [55, 1]] },
  { name: 'Silph S.A.', sub: 'Ciudad Azafrán', hue: 320, gym: 5, pool: [[81, 2], [82, 2], [100, 2], [101, 2], [109, 2], [110, 2], [88, 2], [89, 2], [132, 1], [137, 0.3], [106, 0.5], [107, 0.5], [124, 0.3], [63, 1.5], [64, 1], [65, 0.4], [96, 1.5], [97, 1], [92, 1.5], [93, 1], [94, 0.4]] },
  { name: 'Islas Espuma', sub: 'Ruta 20', hue: 200, pool: [[72, 3], [73, 2], [129, 2], [130, 0.4], [98, 2], [99, 1], [116, 2.5], [117, 1], [90, 2], [91, 1], [120, 2], [121, 1], [118, 2], [119, 1], [79, 2], [80, 1], [60, 2], [61, 1], [86, 2], [87, 1.5], [54, 1.5], [55, 1], [131, 0.3], [144, 0.12]] },
  { name: 'Isla Canela', sub: 'Mansión Pokémon', hue: 10, gym: 6, pool: [[58, 2], [59, 1], [37, 2], [38, 1], [77, 2.5], [78, 1.5], [126, 0.5], [109, 2], [110, 2], [88, 2], [89, 1.5], [132, 1], [81, 1.5], [82, 1], [142, 0.15]] },
  { name: 'Calle Victoria', sub: 'Ruta 23', hue: 240, gym: 7, pool: [[22, 2], [20, 2], [24, 2], [28, 2], [67, 2], [68, 0.5], [75, 2], [76, 0.8], [95, 1.5], [112, 1.5], [49, 2], [85, 2], [57, 2], [105, 2], [78, 1.5], [101, 1.5], [42, 2], [18, 1.5], [143, 0.2], [146, 0.12]] },
  { name: 'Cueva Celeste', sub: 'Tras la Liga', hue: 175, needsLeague: true, pool: [[40, 1.5], [42, 2], [97, 1.5], [85, 1.5], [26, 1], [34, 0.5], [31, 0.5], [47, 1.5], [148, 1], [149, 0.2], [112, 1.5], [101, 1.5], [121, 1.5], [55, 1.5], [45, 1.5], [103, 1], [150, 0.1], [151, 0.04]] },
];

// Gimnasios: `after` = zona que hay que despejar antes. `fights` = lo que hay que derrotar, en orden.
// hp = multiplicador sobre la vida base de la zona.
const f = (label, sprite, hp = 1) => ({ label, sprite, hp });
export const GYMS = [
  { leader: 'Brock', city: 'Ciudad Plateada', badge: 'Medalla Roca', color: '#a8a878', after: 2, fights: [f('Geodude', 74), f('Onix', 95, 1.4)] },
  { leader: 'Misty', city: 'Ciudad Celeste', badge: 'Medalla Cascada', color: '#4aa3df', after: 3, fights: [f('Staryu', 120), f('Starmie', 121, 1.4)] },
  { leader: 'Teniente Surge', city: 'Ciudad Carmín', badge: 'Medalla Trueno', color: '#f5c518', after: 4, fights: [f('Voltorb', 100), f('Pikachu', 25), f('Raichu', 26, 1.4)] },
  { leader: 'Erika', city: 'Ciudad Azulona', badge: 'Medalla Arcoíris', color: '#5cc85c', after: 6, fights: [f('Victreebel', 71), f('Tangela', 114), f('Vileplume', 45, 1.4)] },
  { leader: 'Koga', city: 'Ciudad Fucsia', badge: 'Medalla Alma', color: '#c44fb0', after: 8, fights: [f('Koffing', 109), f('Muk', 89), f('Koffing', 109), f('Weezing', 110, 1.4)] },
  { leader: 'Sabrina', city: 'Ciudad Azafrán', badge: 'Medalla Pantano', color: '#e0559a', after: 9, fights: [f('Kadabra', 64), f('Mr. Mime', 122), f('Venomoth', 49), f('Alakazam', 65, 1.4)] },
  { leader: 'Blaine', city: 'Isla Canela', badge: 'Medalla Volcán', color: '#ee6a2c', after: 11, fights: [f('Growlithe', 58), f('Ponyta', 77), f('Rapidash', 78), f('Arcanine', 59, 1.4)] },
  { leader: 'Giovanni', city: 'Ciudad Verde', badge: 'Medalla Tierra', color: '#9a7b4f', after: 12, fights: [f('Rhyhorn', 111), f('Dugtrio', 51), f('Nidoqueen', 31), f('Nidoking', 34), f('Rhydon', 112, 1.4)] },
];

// La Liga: cinco entrenadores seguidos, cada uno es una barra de vida.
export const LEAGUE = {
  leader: 'Liga Pokémon', city: 'Meseta Añil', badge: 'Campeón de la Liga', color: '#c0392b', after: 12, time: 70,
  fights: [f('Lorelei', 131, 3.2), f('Bruno', 68, 3.6), f('Agatha', 94, 4), f('Lance', 149, 4.6), f('Azul', 18, 5.4)],
};

// Nivel máximo según medallas ganadas (0..8).
export const LEVEL_CAP = [15, 25, 35, 45, 55, 65, 75, 85, 100];

// Generadores: entrenadores que luchan por ti. Cuestan ₽ y dan daño por segundo.
export const TRAINERS = [
  { id: 't0', name: 'Cazabichos', desc: 'Caza con su red y su Caterpie.', cost: 25, dps: 0.6 },
  { id: 't1', name: 'Joven', desc: 'Siempre con un Rattata de primera.', cost: 350, dps: 3.6 },
  { id: 't2', name: 'Montañero', desc: 'Sus Geodude no se rinden.', cost: 4900, dps: 21.6 },
  { id: 't3', name: 'Pescador', desc: 'Pesca con la caña buena.', cost: 68600, dps: 130 },
  { id: 't4', name: 'Nadador', desc: 'Ataca desde la orilla.', cost: 960000, dps: 778 },
  { id: 't5', name: 'Cinturón Negro', desc: 'Entrena a pecho descubierto.', cost: 1.34e+07, dps: 4700 },
  { id: 't6', name: 'Psíquico', desc: 'Ni te mira y ya te ha vencido.', cost: 1.9e+08, dps: 28000 },
  { id: 't7', name: 'Científico', desc: 'Prototipos de Silph S.A.', cost: 2.6e+09, dps: 170000 },
  { id: 't8', name: 'Entrenador Experto', desc: 'Equipo completo y bien curtido.', cost: 3.7e+10, dps: 1e+06 },
  { id: 't9', name: 'Líder de Gimnasio', desc: 'Presta sus Pokémon con condiciones.', cost: 5.2e+11, dps: 6e+06 },
  { id: 't10', name: 'Alto Mando', desc: 'Una élite que trabaja para ti.', cost: 7.2e+12, dps: 3.6e+07 },
  { id: 't11', name: 'Campeón', desc: 'El mejor entrenador, a sueldo.', cost: 1e+14, dps: 2.2e+08 },
];
export const TRAINER_GROWTH = 1.15;
// Con estas cantidades, cada entrenador duplica su producción.
export const MILESTONES = [10, 25, 50, 100, 150, 200, 250, 300, 350, 400, 500];

// Mejoras de un solo uso. Su coste = factor × recompensa de la zona `area` (así escala con el avance).
// kind: money | xp | team | trainers | click | all | catch
export const UPGRADES = [
  { id: 'u_coin', name: 'Amuleto Moneda', desc: 'Ganas el 50% más de ₽.', kind: 'money', value: 1.5, area: 1, icon: 'amulet-coin' },
  { id: 'u_egg', name: 'Huevo Suerte', desc: 'Tus Pokémon ganan el 50% más de EXP.', kind: 'xp', value: 1.5, area: 2, icon: 'lucky-egg' },
  { id: 'u_band', name: 'Banda Fuerza', desc: 'Tu equipo hace x1,5 de daño.', kind: 'team', value: 1.5, area: 2 },
  { id: 'u_glove', name: 'Guantes Potenciados', desc: 'Tus toques hacen el doble de daño.', kind: 'click', value: 2, area: 3 },
  { id: 'u_bait', name: 'Cebo Premium', desc: 'Capturas un 50% más fáciles.', kind: 'catch', value: 1.5, area: 4 },
  { id: 'u_lens', name: 'Lupa de Reclutador', desc: 'Tus entrenadores hacen x1,5 de daño.', kind: 'trainers', value: 1.5, area: 4 },
  { id: 'u_coin2', name: 'Amuleto Moneda II', desc: 'Doble de ₽.', kind: 'money', value: 2, area: 6, icon: 'amulet-coin' },
  { id: 'u_band2', name: 'Banda Experto', desc: 'Tu equipo hace el doble de daño.', kind: 'team', value: 2, area: 7 },
  { id: 'u_click2', name: 'Puños de Acero', desc: 'Tus toques hacen x2 de daño.', kind: 'click', value: 2, area: 8 },
  { id: 'u_lens2', name: 'Agencia de Entrenadores', desc: 'Tus entrenadores hacen el doble de daño.', kind: 'trainers', value: 2, area: 9 },
  { id: 'u_coin3', name: 'Amuleto Moneda III', desc: 'Doble de ₽.', kind: 'money', value: 2, area: 10, icon: 'amulet-coin' },
  { id: 'u_egg2', name: 'Caramelo Exp. Gratis', desc: 'El doble de EXP.', kind: 'xp', value: 2, area: 11, icon: 'rare-candy' },
  { id: 'u_band3', name: 'Entrenamiento Intensivo', desc: 'Tu equipo hace x2,5 de daño.', kind: 'team', value: 2.5, area: 11 },
  { id: 'u_belt', name: 'Cinturón de Campeón', desc: 'Todo el daño x2.', kind: 'all', value: 2, area: 12 },
  { id: 'u_lens3', name: 'Imperio de Entrenadores', desc: 'Tus entrenadores hacen x3 de daño.', kind: 'trainers', value: 3, area: 13 },
  { id: 'u_belt2', name: 'Aura de Leyenda', desc: 'Todo el daño x3.', kind: 'all', value: 3, area: 13 },
];
export const UPGRADE_COST_FACTOR = 60;

// Mejoras de toque (niveles infinitos).
export const CLICK_UPGRADES = [
  { id: 'glove', name: 'Entrenamiento de Toque', desc: '+ daño base por toque.', cost: 30, growth: 1.38 },
  { id: 'tech', name: 'Técnica de Combate', desc: 'Cada toque suma un % de tu daño por segundo.', cost: 1500, growth: 1.7, max: 50 },
];

// Mejoras permanentes que se compran con Caramelos Raros.
export const PERKS = [
  { id: 'p_iris', name: 'Amuleto Iris', desc: 'Los shinies aparecen el doble de a menudo.', cost: 30, icon: 'shiny-charm' },
  { id: 'p_xp', name: 'Caramelo Eterno', desc: '+50% de EXP, para siempre.', cost: 20, icon: 'rare-candy' },
  { id: 'p_money', name: 'Cartera Sin Fondo', desc: '+50% de ₽, para siempre.', cost: 20, icon: 'amulet-coin' },
  { id: 'p_auto', name: 'Gimnasio Automático', desc: 'El modo automático de gimnasios disponible desde el inicio.', cost: 15 },
  { id: 'p_start', name: 'Fondo Inicial', desc: 'Empiezas cada aventura con 2.000 ₽.', cost: 10 },
  { id: 'p_stone', name: 'Cantera de Piedras', desc: 'Las Piedras Evolutivas cuestan la mitad.', cost: 15, icon: 'moon-stone' },
  { id: 'p_away', name: 'Campamento Cómodo', desc: 'Progreso sin conexión al 80% (en vez de 50%).', cost: 25, icon: 'exp-share' },
];
export const MASTER_BALL_CANDY_COST = 20;

// Bolas: probabilidad = ratio/255 × multiplicador. Los legendarios usan una tabla fija.
export const BALLS = [
  { id: 'poke', name: 'Poké Ball', mult: 1, price: 1, icon: 'poke-ball' },
  { id: 'great', name: 'Super Ball', mult: 1.5, price: 4, icon: 'great-ball' },
  { id: 'ultra', name: 'Ultra Ball', mult: 2, price: 12, icon: 'ultra-ball' },
  { id: 'master', name: 'Master Ball', mult: 999, price: 0, icon: 'master-ball' },
];
export const LEGENDARY_CATCH = { poke: 0.04, great: 0.08, ultra: 0.15, master: 1 };

// Logros: dan +2% de daño global cada uno. `test` recibe el estado y la función de utilidades.
export const ACHIEVEMENTS = [
  { id: 'a_k1', name: 'Primeros pasos', desc: 'Derrota 100 Pokémon.', test: (s) => s.stats.kills >= 100 },
  { id: 'a_k2', name: 'Domador', desc: 'Derrota 1.000 Pokémon.', test: (s) => s.stats.kills >= 1000 },
  { id: 'a_k3', name: 'Exterminador', desc: 'Derrota 10.000 Pokémon.', test: (s) => s.stats.kills >= 10000 },
  { id: 'a_k4', name: 'Plaga', desc: 'Derrota 100.000 Pokémon.', test: (s) => s.stats.kills >= 100000 },
  { id: 'a_c1', name: 'Dedos ágiles', desc: 'Toca 500 veces.', test: (s) => s.stats.clicks >= 500 },
  { id: 'a_c2', name: 'Dedos de acero', desc: 'Toca 10.000 veces.', test: (s) => s.stats.clicks >= 10000 },
  { id: 'a_d1', name: 'Coleccionista', desc: 'Registra 25 Pokémon.', test: (s, u) => u.dexCount(s) >= 25 },
  { id: 'a_d2', name: 'Pokédex a medias', desc: 'Registra 75 Pokémon.', test: (s, u) => u.dexCount(s) >= 75 },
  { id: 'a_d3', name: 'Pokédex de Kanto', desc: 'Registra los 151 Pokémon.', test: (s, u) => u.dexCount(s) >= 151 },
  { id: 'a_s1', name: 'Destello', desc: 'Captura tu primer shiny.', test: (s, u) => u.shinyCount(s) >= 1 },
  { id: 'a_s2', name: 'Cazador de brillos', desc: 'Ten 10 shinies.', test: (s, u) => u.shinyCount(s) >= 10 },
  { id: 'a_s3', name: 'Constelación', desc: 'Ten 50 shinies.', test: (s, u) => u.shinyCount(s) >= 50 },
  { id: 'a_b1', name: 'Una medalla', desc: 'Gana tu primera medalla.', test: (s) => s.stats.gymsWon >= 1 },
  { id: 'a_b2', name: 'Las ocho', desc: 'Consigue las 8 medallas.', test: (s) => s.badges.length >= 8 || s.stats.leagueWins >= 1 },
  { id: 'a_l1', name: 'Campeón', desc: 'Vence a la Liga Pokémon.', test: (s) => s.stats.leagueWins >= 1 },
  { id: 'a_m1', name: 'Ahorrador', desc: 'Gana 1 millón de ₽ en total.', test: (s) => s.stats.lifeMoney >= 1e6 },
  { id: 'a_m2', name: 'Magnate', desc: 'Gana 1.000 millones de ₽ en total.', test: (s) => s.stats.lifeMoney >= 1e9 },
  { id: 'a_m3', name: 'Rocket de Fortuna', desc: 'Gana 1 billón de ₽ en total.', test: (s) => s.stats.lifeMoney >= 1e12 },
  { id: 'a_t1', name: 'Reclutador', desc: 'Contrata 100 entrenadores.', test: (s, u) => u.trainerCount(s) >= 100 },
  { id: 'a_t2', name: 'Agencia', desc: 'Contrata 500 entrenadores.', test: (s, u) => u.trainerCount(s) >= 500 },
  { id: 'a_lg1', name: 'Pájaro raro', desc: 'Captura un Pokémon legendario.', test: (s, u) => u.legendCount(s) >= 1 },
  { id: 'a_lg2', name: 'Las tres aves', desc: 'Captura a Articuno, Zapdos y Moltres.', test: (s) => !!(s.owned[144] && s.owned[145] && s.owned[146]) },
  { id: 'a_lg3', name: 'Genética legendaria', desc: 'Captura a Mewtwo.', test: (s) => !!s.owned[150] },
  { id: 'a_e1', name: 'Metamorfosis', desc: 'Evoluciona 10 Pokémon.', test: (s) => s.stats.evolved >= 10 },
  { id: 'a_p1', name: 'Nueva aventura', desc: 'Reinicia la aventura por primera vez.', test: (s) => s.prestiges >= 1 },
  { id: 'a_p2', name: 'Veterano', desc: 'Reinicia la aventura 5 veces.', test: (s) => s.prestiges >= 5 },
];
export const ACHIEVEMENT_BONUS = 0.02;

// Pokémon inicial a elegir.
export const STARTERS = [1, 4, 7];
