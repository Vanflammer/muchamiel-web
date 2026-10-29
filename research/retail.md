# WoW Retail (actual) — investigación para el apartado de muchamielwow.github.io

Investigado el 16/17-10-2026. Cada dato lleva fuente y fecha. Lo marcado **[SIN CONFIRMAR]** no lo he podido verificar en fuente oficial o hay fuentes que se contradicen.

Nota de método: Archon (archon.gg), Warcraft Logs, u.gg, Wowhead y CurseForge bloquean la lectura automática (Archon pide verificación humana, el resto da 403). Raider.IO sí tiene API pública y la he usado directamente. Icy Veins se ha podido leer con curl. Los datos de Wowhead que salen aquí están tomados de terceros que los citan (lo indico).

---

## 1. Estado actual: expansión, parche y temporada

| Dato | Valor | Fuente (fecha) |
|---|---|---|
| Expansión | **World of Warcraft: Midnight** (11.ª expansión, 2.ª parte de la Saga del Alma del Mundo) | [Wikipedia](https://en.wikipedia.org/wiki/World_of_Warcraft:_Midnight), [warcraft.wiki.gg](https://warcraft.wiki.gg/wiki/World_of_Warcraft:_Midnight) |
| Salida | **2-3-2026** (acceso anticipado 26-2-2026) | idem |
| Nivel máximo | **90** | Wikipedia; Icy Veins, guía de subida de nivel (actualizada 19-5-2026): [icy-veins.com/wow/midnight-leveling-guide](https://www.icy-veins.com/wow/midnight-leveling-guide) |
| Zonas | Bosque Canción Eterna (Eversong Woods), Zul'Aman, Harandar, Tormenta del Vacío (Voidstorm); capital Lunargenta (Silvermoon). En 12.1 se añadió la Isla Enroscada (Coiled Isle) | Wikipedia; Icy Veins |
| Novedades clave | Viviendas (housing), Presa (Prey), nueva especialización **Devorador** (Devourer) de cazador de demonios (DPS a distancia, 3.ª espec.), raza aliada Haranir, surcacielos desde el principio | warcraft.wiki.gg; notas 12.1.5 |
| Parche en vivo | **12.1.5** (sin nombre propio; contenido: capítulo «The Promise of Tomorrow», banda de un jefe *The Unbinding of Kith'ix*, primer Laberinto *Labyrinth of Kindo'jan*, Invasiones aqir en Canción Eterna y Zul'Aman). **Salió el 13-10-2026** (EU 14-10) | [Notas oficiales 12.1.5](https://worldofwarcraft.blizzard.com/news/24304162) (13-10); [BlizzardWatch](https://blizzardwatch.com/2026/10/12/wow-patch-12-1-5-release-date/) (12-10); Raider.IO API (apertura Kith'ix 13-10 US / 14-10 EU) |
| Parche mayor vigente | **12.1 «Curse of Ula'tek»** (La maldición de Ula'tek), 11-8-2026 | [warcraft.wiki.gg Venomous Abyss](https://warcraft.wiki.gg/wiki/Venomous_Abyss); [BlizzardWatch 28-7](https://blizzardwatch.com/2026/07/28/wow-12-1-release-date/) |
| Parches anteriores | 12.0.5 «Lingering Shadows» 21-4-2026; 12.0.7 junio 2026 (16-6 según Icy Veins/BlizzardWatch) **[fecha exacta de 12.0.7 SIN CONFIRMAR]** | [búsqueda; roadmap resumido](https://nohoartsdistrict.com/?p=36691), [Icy Veins](https://www.icy-veins.com/wow/news/wow-players-may-already-have-midnight-season-2s-start-date/) |
| Próximo: 12.1.7 «Echoes of the Worldcore» | En PTR (build 70424, 15-10-2026). Contenido: campaña en Dornogal, modo **Talebound** (RPG de acción PvE independiente), Lorewalking, vuelve Turbulent Timeways, actualizaciones de fiestas. **Fecha: Blizzard solo dice «finales de otoño / principios de invierno»; BlizzardWatch estima 8-12-2026 [ESTIMACIÓN]** | [BlizzardWatch 15-10](https://blizzardwatch.com/2026/10/15/wow-midnight-patch-12-1-7-release-date); [MMO-Champion PTR](https://www.mmo-champion.com/content/14613-Patch-12-1-7-PTR-Build-70424); [foro PTR](https://us.forums.blizzard.com/en/wow/t/midnight-echoes-of-the-worldcore-ptr-development-notes/2383391) |
| Después: 12.2 «Eclipse» | Anunciado en BlizzCon (12/13-9-2026): mazmorra nueva de 3 jefes y banda de 8 jefes en el núcleo del mundo (se espera Xal'atath al final). La Temporada 3 empieza «poco después» de Eclipse. **Sin fecha** | [Blizzard: todo lo anunciado en BlizzCon 2026](https://news.blizzard.com/en-us/article/24301453/everything-announced-at-blizzcon-2026-opening-ceremony); [wow.gg](https://wow.gg/guides/wow-blizzcon-2026) |
| Siguiente expansión | **The Last Titan**, solo avance, objetivo 2027 **[sin fecha]** | idem |
| Temporada actual | **Midnight Temporada 2**: empezó 18-8-2026 (US) / 19-8-2026 04:00 UTC (EU). Fin **sin anunciar**; Icy Veins dice «hasta el final del ciclo 12.1, unos 6 meses»; GGS estima **26-1-2027 [ESTIMACIÓN]** | [Blizzard: Season 2 is now live](https://news.blizzard.com/en-us/article/24294369/midnight-season-2-is-now-live); Raider.IO API `static-data` (consultada 16-10); [Icy Veins M+ S2](https://www.icy-veins.com/wow/midnight-mythic-season-2-guide) (5-8); [ggseason.com](https://ggseason.com/wow/) (8-10) |
| JcJ | **Temporada 2 de JcJ** desde la semana del 18-8 (Arena Training Grounds desde el 11-8). Título Gladiador venenoso (top 0,1 % 3v3). Fin sin anunciar | Blizzard (misma noticia) |
| Temporada 1 (anterior) | M+ T1: 25-3 a 19-8-2026 (EU). Banda T1 (Voidspire / Dreamrift / March on Quel'Danas): 18-3 a 19-8 | Raider.IO API |
| Suscripción / compra | **[SIN CONFIRMAR]** el texto exacto de la tienda («la suscripción incluye niveles 1-80, Midnight se vende aparte»): la tienda de Battle.net pide inicio de sesión y no la he podido leer. Lo que sí consta: las ediciones de Midnight (Base 49,99 $, Heroica 69,99 $, Épica 89,99 $) incluyen The War Within y un impulso a 80 | [Soporte Blizzard](https://eu.support.blizzard.com/en/article/380825); [mein-mmo](https://mein-mmo.de/en/pre-order-wow-midnight-which-edition-is-right-for-me,1521034) |

---

## 2. Mazmorras

### 2.1 Temporada 2 de Míticas+ (vigente) — 8 mazmorras

Fuente de la lista: Blizzard (noticia Temporada 2) y Raider.IO API (16-10-2026, con temporizadores). Ubicaciones: Icy Veins, guía de mazmorras (actualizada 10-8-2026): [icy-veins.com/wow/dungeons-guide](https://www.icy-veins.com/wow/dungeons-guide).

| Inglés | Castellano (visto en) | Expansión | Entrada | Tiempo +llave |
|---|---|---|---|---|
| Altar of Fangs (nueva en 12.1) | **Altar de los Colmillos** (Blizzard es-ES; YouTube) | Midnight | Bóvedas de Atal'Utek, Isla Enroscada (47.2, 68.5) | 30 min |
| Murder Row | **[SIN CONFIRMAR]** «Callejón del Crimen» (wow.gg/es) vs «Frontal de la Muerte» (lo que devolvió la lectura automática de la noticia es-ES de Blizzard; dudoso) | Midnight | Lunargenta (57.0, 61.0) | 34 min |
| Den of Nalorakk | **Guarida de Nalorakk** (Blizzard es-ES; wow.gg/es) | Midnight | Zul'Aman (31.0, 84.0), cordillera sur, junto a una cabeza de oso de piedra | 32 min |
| The Blinding Vale | **Valle Cegador** (Blizzard es-ES) / «El Valle Enceguecedor» (vídeos latinoamericanos, probable es-MX) | Midnight | Harandar (26.8, 78.0) | 30 min |
| Voidscar Arena | **Arena Lacravacua** (Blizzard es-ES) / «Arena Rajavacío» (vídeos latinoamericanos, probable es-MX) | Midnight | Alzamiento del Asesino (Slayer's Rise), Tormenta del Vacío (53.7, 34.0) | 30 min |
| Kings' Rest | Reposo de los Reyes | Battle for Azeroth | Zuldazar (Dazar'alor). Portal en la sala de portales de M+ | 33 min |
| Temple of Sethraliss | Templo de Sethraliss | Battle for Azeroth | Vol'dun. Portal en la sala de portales | 32 min |
| Ruby Life Pools | Estanques de Vida Rubí | Dragonflight | Costas Despertares (Waking Shores). Portal en la sala de portales | 28 min |

- **Sala de portales de M+**: portal dorado en Lunargenta (53.3, 66.1), junto a Lindormi y Agmera; lleva a los portales de las mazmorras que no son de Midnight (Icy Veins, guía M+ T2).
- Teletransporte permanente a cada mazmorra al completar una +10 en tiempo (Icy Veins).
- Ojo: hay dos traducciones al castellano (es-ES de España y es-MX de Latinoamérica). En la web conviene poner el nombre en inglés + es-ES (y es-MX entre paréntesis si difiere). **Recomiendo que alguien con el cliente en es-ES confirme los nombres antes de publicar.**

### 2.2 Todas las mazmorras de Midnight (9)

Icy Veins (10-8-2026), nivel de desbloqueo en normal:

| Mazmorra | Castellano visto | Zona | Nivel |
|---|---|---|---|
| Windrunner Spire | Aguja Brisaveloz | Bosque Canción Eterna (35.5, 78.8) | 81 |
| Murder Row | ver arriba | Lunargenta | 83 |
| Den of Nalorakk | Guarida de Nalorakk | Zul'Aman | 88 |
| Maisara Caverns | Cavernas de Maisara | Zul'Aman (43.9, 39.7) | 88 |
| The Blinding Vale | Valle Cegador | Harandar | 88 |
| Magisters' Terrace | Bancal del Magister | Isla de Quel'Danas (63.0, 15.0) | 90 |
| Nexus-Point Xenas | Punto de Nexo: Xenas | Tormenta del Vacío (64.75, 61.75) | 90 |
| Voidscar Arena | Arena Lacravacua | Tormenta del Vacío | 90 |
| Altar of Fangs | Altar de los Colmillos | Isla Enroscada | 90 |

Nombres en castellano de la temporada 1 tomados de títulos de vídeos de SouzaCarlosTV (YouTube); «Bancal del Magister» es el nombre clásico de TBC **[no comprobado para la versión de Midnight]**.

Temporada 1 de M+ (ya terminada), por Raider.IO: Algeth'ar Academy, Magisters' Terrace, Maisara Caverns, Nexus-Point Xenas, Pit of Saron, Seat of the Triumvirate, Skyreach, Windrunner Spire.

**Temporada 3** (anunciada en BlizzCon; vista previa oficial del 16-9-2026, [foro Blizzard](https://us.forums.blizzard.com/en/wow/t/2351172)): nombra Maisara Caverns, Magisters' Terrace, Uldaman, Stonecore (Núcleo Pétreo) y Underrot (Catacumbas Putrefactas), más una mazmorra nueva de Eclipse (PlayNews la llama «Thraegar Stronghold», BlizzardWatch «Thraegar's Stand» **[SIN CONFIRMAR]**). Las demás fuentes no coinciden en el resto de la lista.

### 2.3 Afijos (Temporada 2)

Fuentes: Icy Veins, guía M+ T2 (5-8-2026); JudgeHype (actualizado 13-8-2026); Raider.IO API de afijos en castellano (16-10-2026).

| Nivel de llave | Afijo |
|---|---|
| +2 a +5 | **Guía de Lindormi** (Lindormi's Guidance, nuevo): marca los enemigos que cuentan para las fuerzas enemigas y les baja vida y daño; ayuda a aprender rutas. Se quita en +6 |
| +5 a +11 | **Trato de Xal'atath** (rota semanalmente uno de cuatro): Ascendente, Ligado al Vacío (Voidbound), Púlsar, Devorar |
| +7 a +9 | **Reforzada** o **Tiránica**, alternando cada semana |
| +10 y más | Reforzada **y** Tiránica a la vez |
| +12 y más | **Argucia de Xal'atath** (Xal'atath's Guile): anula los tratos y cada muerte resta 15 s |

Semana del 16-10-2026 (Raider.IO, región EU): **Trato de Xal'atath: Púlsar + Reforzada + Tiránica + Argucia de Xal'atath**.

Recompensas: el cofre final sube hasta 311 (Héroe 3/6) en +10; la Gran Cámara hasta 318 (Mito 1/6) desde +10. Más allá de +12 no hay más nivel de objeto (Icy Veins; JudgeHype).

Cortes de puntuación M+ en Europa a 16-10-2026 (Raider.IO API): top 0,1 % = 3939; top 1 % = 3744; top 10 % = 3323; top 25 % = 3019. Logros: Maestro de piedra angular (2000, montura Breath of Blight), Leyenda (3000, Breath of Ruin), Mito (3600, título + Timelost Saddle; añadido en 12.1.5).

---

## 3. Bandas actuales

### 3.1 El Abismo Venenoso (The Venomous Abyss) — banda principal T2

- Ubicación: Bóvedas de Atal'Utek, Isla Enroscada (Coiled Isle). Entrada por una de las tres puertas (Ojo de la Serpiente al norte, Colmillo Este u Oeste al sur); portal de la banda en (47.2, 21.7) ([Conquest Capped](https://conquestcapped.com/guides/wow/the-venomous-abyss-raid-overview/)).
- Dificultades: Modo historia, Buscador de bandas, Normal, Heroico, Mítico.
- Apertura (Blizzard, noticia T2): semana del 18-8 → Normal, Heroico, **Mítico** y Buscador ala 1; 25-8 → Modo historia y ala 2; 1-9 → ala 3; 8-9 → ala 4.
- Jefes en orden (Raider.IO API; Conquest Capped), con el nombre en castellano visto en guías de YouTube en español (AlterTime, Jimmyfumi, Yuki Series, Taberna de Mercys):

| # | Inglés | Castellano visto | Ala del buscador |
|---|---|---|---|
| 1 | Nek'zali the Soulcoiler | Nek'zali la Volutadora de Almas | 1 The Soulcoilers |
| 2 | Entombed Sentinels | Centinelas sepultados | 2 The Essence of Venom |
| 3 | The Lost Explorers | Exploradores perdidos | 3 The Serpent Warren |
| 4 | Vashnik the Malignant | Vashnik el Maligno | 2 |
| 5 | Sszorak | Sszorak | 3 |
| 6 | The Twin Fangs | Los Colmillos Gemelos | 1 |
| 7 | The Coiled Altar | El Altar en Espiral | 4 The Tomb of Ula'tek |
| 8 | Ula'tek | Ula'tek | 4 |

Nota: algunas guías dicen que las dos «alas» centrales se pueden hacer en cualquier orden ([Skycoach](https://skycoach.gg/blog/wow/articles/venomous-abyss-raid-guide)); el orden de arriba es el del diario de encuentros según Raider.IO. Logros de tiempo limitado: «A la vanguardia: Ula'tek» (heroico) y «Cutting Edge: Ula'tek» (mítico).

### 3.2 El Desatamiento de Kith'ix (The Unbinding of Kith'ix) — banda de un jefe, 12.1.5

- Abrió el 13-10-2026 US / 14-10-2026 EU (Raider.IO API). En una guarida subterránea bajo el Abismo Venenoso. Dificultades: Historia, Buscador, Normal, Heroico, Mítico (en mítico, grupo flexible de 15-25). Fuente: [notas 12.1.5](https://worldofwarcraft.blizzard.com/news/24304162). Nombre en castellano oficial **[SIN CONFIRMAR]**.

### 3.3 Guaridas (jefes del mundo instanciados)

- **Tidebound Grotto** — jefa Nymrissa Wavecaller, bajo la Isla Enroscada; dificultad hasta mítico y 15-25 jugadores; desde la semana del 11-8 ([Icy Veins, resumen T2](https://www.icy-veins.com/wow/midnight-season-2-guide), 15-10-2026). Raider.IO la trata como «banda» de un jefe.

---

## 4. Clases y especializaciones (13 clases, 40 especializaciones)

Fuentes de clasificación (no opino, solo copio):

- **IV M+** = Icy Veins, tier list de Míticas+ (DPS, sanadores y tanques; las tres «LAST UPDATED 12th of October» 2026, parche 12.1.5): [DPS](https://www.icy-veins.com/wow/mythic-dps-tier-list), [sanadores](https://www.icy-veins.com/wow/mythic-healer-tier-list), [tanques](https://www.icy-veins.com/wow/mythic-tank-tier-list).
- **IV banda** = Icy Veins, tier list de banda: [DPS](https://www.icy-veins.com/wow/dps-rankings-tier-list) (12-10-2026), [sanadores](https://www.icy-veins.com/wow/healer-rankings-tier-list) (11-10-2026), [tanques](https://www.icy-veins.com/wow/tank-rankings-tier-list) (29-8-2026).
- **WH M+ / WH banda** = tier lists de Wowhead del 13-10 (M+ DPS) y 12-10 (banda DPS), **leídas a través de [Leprestore](https://leprestore.com/guides/wow/wow-midnight-season-2-best-class-tier-list-pve-rankings/)** (Wowhead bloquea la lectura directa).
- **RIO top 200** = mi recuento con la API de Raider.IO de los **200 mejores runs del mundo** de la T2 (llaves +22 a +24, consultado 16-10-2026): % de esos runs en los que aparece la espec. Es una foto de la élite, no del jugador medio.
- **Archon / Warcraft Logs: NO consultado** (Archon pide verificación humana; WCL y u.gg devuelven 403). Si se quiere este dato, hay que mirarlo a mano en archon.gg.

Enlaces: guía de Icy Veins (todas comprobadas con respuesta 200 el 16-10-2026) y calculador de talentos de Wowhead (patrón `wowhead.com/talent-calc/<clase>/<espec>`; **no comprobado** porque Wowhead bloquea, pero es el formato estándar). El nombre en castellano de cada especialización es el habitual del cliente es-ES; el de Devorador **[SIN CONFIRMAR]**.

| Clase | Espec. (es) | Rol | IV M+ | IV banda | WH M+ | WH banda | RIO top 200 | Guía Icy Veins | Talentos Wowhead |
|---|---|---|---|---|---|---|---|---|---|
| Caballero de la Muerte | Sangre (Blood) | Tanque | S | S | — | — | 84 % | [guía](https://www.icy-veins.com/wow/blood-death-knight-pve-tank-guide) | [talentos](https://www.wowhead.com/talent-calc/death-knight/blood) |
| Caballero de la Muerte | Escarcha (Frost) | DPS cuerpo a cuerpo | A+ | A | B | B | 3 % | [guía](https://www.icy-veins.com/wow/frost-death-knight-pve-dps-guide) | [talentos](https://www.wowhead.com/talent-calc/death-knight/frost) |
| Caballero de la Muerte | Profano (Unholy) | DPS cuerpo a cuerpo | A | S | A | B | 1 % | [guía](https://www.icy-veins.com/wow/unholy-death-knight-pve-dps-guide) | [talentos](https://www.wowhead.com/talent-calc/death-knight/unholy) |
| Cazador de demonios | Devastación (Havoc) | DPS cuerpo a cuerpo | A | B | B | B | 5 % | [guía](https://www.icy-veins.com/wow/havoc-demon-hunter-pve-dps-guide) | [talentos](https://www.wowhead.com/talent-calc/demon-hunter/havoc) |
| Cazador de demonios | Venganza (Vengeance) | Tanque | A+ | B | — | — | 0 % | [guía](https://www.icy-veins.com/wow/vengeance-demon-hunter-pve-tank-guide) | [talentos](https://www.wowhead.com/talent-calc/demon-hunter/vengeance) |
| Cazador de demonios | Devorador (Devourer) — nueva en Midnight | DPS a distancia | A+ | A | A | B | 4 % | [guía](https://www.icy-veins.com/wow/devourer-demon-hunter-pve-dps-guide) | [talentos](https://www.wowhead.com/talent-calc/demon-hunter/devourer) |
| Druida | Equilibrio (Balance) | DPS a distancia | A | A | B | A | 0 % | [guía](https://www.icy-veins.com/wow/balance-druid-pve-dps-guide) | [talentos](https://www.wowhead.com/talent-calc/druid/balance) |
| Druida | Feral | DPS cuerpo a cuerpo | S | B | A | C | 0 % | [guía](https://www.icy-veins.com/wow/feral-druid-pve-dps-guide) | [talentos](https://www.wowhead.com/talent-calc/druid/feral) |
| Druida | Guardián (Guardian) | Tanque | S | A | — | — | 17 % | [guía](https://www.icy-veins.com/wow/guardian-druid-pve-tank-guide) | [talentos](https://www.wowhead.com/talent-calc/druid/guardian) |
| Druida | Restauración | Sanador | A+ | S | — | — | 0 % | [guía](https://www.icy-veins.com/wow/restoration-druid-pve-healing-guide) | [talentos](https://www.wowhead.com/talent-calc/druid/restoration) |
| Evocador | Devastación | DPS a distancia | B | A+ | B | B | 0 % | [guía](https://www.icy-veins.com/wow/devastation-evoker-pve-dps-guide) | [talentos](https://www.wowhead.com/talent-calc/evoker/devastation) |
| Evocador | Preservación | Sanador | A | A | — | — | 0 % | [guía](https://www.icy-veins.com/wow/preservation-evoker-pve-healing-guide) | [talentos](https://www.wowhead.com/talent-calc/evoker/preservation) |
| Evocador | Aumento (Augmentation) | Apoyo (DPS) | C | B | C | B | 0 % | [guía](https://www.icy-veins.com/wow/augmentation-evoker-pve-dps-guide) | [talentos](https://www.wowhead.com/talent-calc/evoker/augmentation) |
| Cazador | Bestias (Beast Mastery) | DPS a distancia | A+ | C | B | C | 3 % | [guía](https://www.icy-veins.com/wow/beast-mastery-hunter-pve-dps-guide) | [talentos](https://www.wowhead.com/talent-calc/hunter/beast-mastery) |
| Cazador | Puntería (Marksmanship) | DPS a distancia | A | A+ | B | A | 0 % | [guía](https://www.icy-veins.com/wow/marksmanship-hunter-pve-dps-guide) | [talentos](https://www.wowhead.com/talent-calc/hunter/marksmanship) |
| Cazador | Supervivencia (Survival) | DPS cuerpo a cuerpo | A | B | B | C | 0 % | [guía](https://www.icy-veins.com/wow/survival-hunter-pve-dps-guide) | [talentos](https://www.wowhead.com/talent-calc/hunter/survival) |
| Mago | Arcano | DPS a distancia | S+ | A+ | A+ | A | 19 % | [guía](https://www.icy-veins.com/wow/arcane-mage-pve-dps-guide) | [talentos](https://www.wowhead.com/talent-calc/mage/arcane) |
| Mago | Fuego | DPS a distancia | B | B | C | C | 0 % | [guía](https://www.icy-veins.com/wow/fire-mage-pve-dps-guide) | [talentos](https://www.wowhead.com/talent-calc/mage/fire) |
| Mago | Escarcha | DPS a distancia | B | A | C | B | 0 % | [guía](https://www.icy-veins.com/wow/frost-mage-pve-dps-guide) | [talentos](https://www.wowhead.com/talent-calc/mage/frost) |
| Monje | Maestro cervecero (Brewmaster) | Tanque | A+ | A | — | — | 0 % | [guía](https://www.icy-veins.com/wow/brewmaster-monk-pve-tank-guide) | [talentos](https://www.wowhead.com/talent-calc/monk/brewmaster) |
| Monje | Tejedor de niebla (Mistweaver) | Sanador | A | B | — | — | 0 % | [guía](https://www.icy-veins.com/wow/mistweaver-monk-pve-healing-guide) | [talentos](https://www.wowhead.com/talent-calc/monk/mistweaver) |
| Monje | Viajero del viento (Windwalker) | DPS cuerpo a cuerpo | S | A | A | A | 1 % | [guía](https://www.icy-veins.com/wow/windwalker-monk-pve-dps-guide) | [talentos](https://www.wowhead.com/talent-calc/monk/windwalker) |
| Paladín | Sagrado (Holy) | Sanador | S | B | — | — | 95 % | [guía](https://www.icy-veins.com/wow/holy-paladin-pve-healing-guide) | [talentos](https://www.wowhead.com/talent-calc/paladin/holy) |
| Paladín | Protección | Tanque | A | S | — | — | 0 % | [guía](https://www.icy-veins.com/wow/protection-paladin-pve-tank-guide) | [talentos](https://www.wowhead.com/talent-calc/paladin/protection) |
| Paladín | Reprensión (Retribution) | DPS cuerpo a cuerpo | S | A+ | A | B | 5 % | [guía](https://www.icy-veins.com/wow/retribution-paladin-pve-dps-guide) | [talentos](https://www.wowhead.com/talent-calc/paladin/retribution) |
| Sacerdote | Disciplina | Sanador | B | S | — | — | 0 % | [guía](https://www.icy-veins.com/wow/discipline-priest-pve-healing-guide) | [talentos](https://www.wowhead.com/talent-calc/priest/discipline) |
| Sacerdote | Sagrado (Holy) | Sanador | B | S | — | — | 0 % | [guía](https://www.icy-veins.com/wow/holy-priest-pve-healing-guide) | [talentos](https://www.wowhead.com/talent-calc/priest/holy) |
| Sacerdote | Sombra (Shadow) | DPS a distancia | B | A+ | B | A | 0 % | [guía](https://www.icy-veins.com/wow/shadow-priest-pve-dps-guide) | [talentos](https://www.wowhead.com/talent-calc/priest/shadow) |
| Pícaro | Asesinato | DPS cuerpo a cuerpo | S+ | A+ | A+ | A | 48 % | [guía](https://www.icy-veins.com/wow/assassination-rogue-pve-dps-guide) | [talentos](https://www.wowhead.com/talent-calc/rogue/assassination) |
| Pícaro | Forajido (Outlaw) | DPS cuerpo a cuerpo | S | B | A | C | 0 % | [guía](https://www.icy-veins.com/wow/outlaw-rogue-pve-dps-guide) | [talentos](https://www.wowhead.com/talent-calc/rogue/outlaw) |
| Pícaro | Sutileza (Subtlety) | DPS cuerpo a cuerpo | A+ | A | A | B | 38 % | [guía](https://www.icy-veins.com/wow/subtlety-rogue-pve-dps-guide) | [talentos](https://www.wowhead.com/talent-calc/rogue/subtlety) |
| Chamán | Elemental | DPS a distancia | S+ | B | A+ | B | 94 % | [guía](https://www.icy-veins.com/wow/elemental-shaman-pve-dps-guide) | [talentos](https://www.wowhead.com/talent-calc/shaman/elemental) |
| Chamán | Mejora (Enhancement) | DPS cuerpo a cuerpo | A | B | B | B | 0 % | [guía](https://www.icy-veins.com/wow/enhancement-shaman-pve-dps-guide) | [talentos](https://www.wowhead.com/talent-calc/shaman/enhancement) |
| Chamán | Restauración | Sanador | S | A | — | — | 6 % | [guía](https://www.icy-veins.com/wow/restoration-shaman-pve-healing-guide) | [talentos](https://www.wowhead.com/talent-calc/shaman/restoration) |
| Brujo | Aflicción | DPS a distancia | B | A | C | B | 0 % | [guía](https://www.icy-veins.com/wow/affliction-warlock-pve-dps-guide) | [talentos](https://www.wowhead.com/talent-calc/warlock/affliction) |
| Brujo | Demonología | DPS a distancia | A+ | S | A+ | A | 1 % | [guía](https://www.icy-veins.com/wow/demonology-warlock-pve-dps-guide) | [talentos](https://www.wowhead.com/talent-calc/warlock/demonology) |
| Brujo | Destrucción | DPS a distancia | B | B | B | B | 0 % | [guía](https://www.icy-veins.com/wow/destruction-warlock-pve-dps-guide) | [talentos](https://www.wowhead.com/talent-calc/warlock/destruction) |
| Guerrero | Armas (Arms) | DPS cuerpo a cuerpo | S+ | A+ | A+ | A | 82 % | [guía](https://www.icy-veins.com/wow/arms-warrior-pve-dps-guide) | [talentos](https://www.wowhead.com/talent-calc/warrior/arms) |
| Guerrero | Furia (Fury) | DPS cuerpo a cuerpo | A | C | B | C | 0 % | [guía](https://www.icy-veins.com/wow/fury-warrior-pve-dps-guide) | [talentos](https://www.wowhead.com/talent-calc/warrior/fury) |
| Guerrero | Protección | Tanque | A | A | — | — | 0 % | [guía](https://www.icy-veins.com/wow/protection-warrior-pve-tank-guide) | [talentos](https://www.wowhead.com/talent-calc/warrior/protection) |

Notas:

- Para tanques y sanadores no he podido leer la lista de Wowhead (por eso el guion). Según Leprestore, Wowhead no tiene ninguna espec. de DPS en S ni en M+ ni en banda en su revisión de octubre.
- RIO top 200, sin redondeos raros: tanques Sangre 167 runs y Guardián 33; sanadores Paladín Sagrado 189 y Chamán Restauración 11; DPS Elemental 188, Armas 164, Asesinato 95, Sutileza 75, Arcano 37, Devastación 10, Reprensión 9, Devorador 7, Bestias 6, Escarcha CM 5, Profano 2, Viajero del viento 1, Demonología 1. En la élite la composición casi fija es «Sangre + Paladín Sagrado + Elemental + Armas + pícaro».
- Cambios de clase del 12.1.5 (notas oficiales): Devorador (Colapso estelar ya no entra en reutilización al cancelarse), Sutileza (+14 % de daño), Protección de guerrero (+30 % a Ejecutar), Restauración de druida (rediseño de Nature's Bounty), Puntería (se quita Unload y entra Blood Fletching). **Las tier lists son del 11-12 de octubre, justo antes del parche: pueden moverse en las próximas semanas.**

---

## 5. Subir de nivel

Fuente principal: Icy Veins, [Midnight: Leveling, Zone Progression, Adventure Mode](https://www.icy-veins.com/wow/midnight-leveling-guide) (actualizada 19-5-2026).

- **Personaje nuevo**: Isla del Exilio (Exile's Reach) o zona de inicio de su raza; las razas aliadas empiezan en 10 ([fdaytalk](https://www.fdaytalk.com/?p=70286)).
- **Chromie Time en Midnight: niveles 10-70**, con Dragonflight como opción por defecto. Al llegar a 70 hay un **modo historia rápido de The War Within** que pone al día la trama antes de Midnight (Icy Veins). (Otra guía de terceros habla de 10-79: hay discrepancia, me quedo con Icy Veins.)
- La experiencia de 1 a 80 se redujo un 43 % ([games.gg](https://games.gg/world-of-warcraft/guides/wow-midnight-leveling-guide-level-90/), 2-3-2026).
- **Introducción de Midnight**: desde nivel 78.
- **Ruta 80-90** (Icy Veins): Bosque Canción Eterna (80-82) → luego en el orden que quieras: Zul'Aman, Harandar y la cadena de Arator por los Reinos del Este (82-88) → Tormenta del Vacío (88-90). La campaña principal tiene 17 capítulos y deja casi en 90; el resto con misiones del mundo. Total 4 963 065 PX de 80 a 90.
- **Mazmorras para subir**: Aguja Brisaveloz (81), Callejón/Murder Row (83), Guarida de Nalorakk, Cavernas de Maisara y Valle Cegador (88). Consejo: hacer cada una una vez con su misión de campaña activa (games.gg).
- **Profundidades (Delves)**: solo compensan la primera vez (misión de primera finalización); repetirlas da poca PX (Icy Veins).
- **Modo aventura**: al terminar la campaña, los alters empiezan en el Sagrario de la Luz de Lunargenta y eligen el orden de zonas libremente, o suben con misiones del mundo y eventos (Icy Veins).
- **Surcacielos** desde el primer momento, sin desbloqueos.
- **Tiempo típico 80-90**: unas 10 h jugando tranquilo; 5-7 h siguiendo la campaña con prisa (games.gg; [AccountShark](https://accountshark.net/blog/wow-midnight-leveling-guide-80-90-complete)). Récords de unas 2 h (guías de empresas de «boosting», poco fiables).
- Consejos (games.gg): Fuego de hogar en Lunargenta, auto-botín y tecla de interactuar, mirar logros de Mentor de la banda guerrera (hasta +25 % PX), objetos de movimiento (Gunshoes, kits de planeador goblin).

---

## 6. Profesiones

Fuentes: Icy Veins, [Profession Overview for Midnight](https://www.icy-veins.com/wow/professions) (actualizada 11-8-2026); [wow-professions.com, cambios 12.1](https://www.wow-professions.com/news/midnight-patch-12-1-knowledge-point-reset).

Qué cambió en Midnight:
- Los consumibles tienen **2 calidades** (antes 3); el equipo fabricado sigue con 5.
- La Agudeza de artesano (Artisan's Acuity) pasa a ser **Moxie de artesano por profesión** (sirve sobre todo para comprar recetas).
- Árboles de especialización renovados, pero con la misma idea que en The War Within.
- Pedidos de fabricación desde habilidad 15; los pedidos de NPC (Patron) dan conocimiento, Moxie, recetas y reactivos.
- Bolsa de reactivos para todos; pilas de 1000 (consumibles 200).
- **Decoración de viviendas** como mercado nuevo (sobre todo Joyería e Inscripción, según varias guías).

En 12.1 (T2): **reinicio único de puntos de conocimiento por profesión** (NPC Theremis en Lunargenta), recetas nuevas (mucha decoración), materiales nuevos solo en zonas malditas de la Isla Enroscada, y pesca con veneno. Icy Veins avisa de que la mayoría de recetas nuevas son peores que las de la T1, salvo las mejoras directas (poción de salud concentrada de Lunargenta, Vantus Rune: Tides).

Guías buenas: Icy Veins (una por profesión + guía de oro), [wow-professions.com](https://www.wow-professions.com/midnight/alchemy-guide) (rutas y puntos de conocimiento por profesión), Wowhead. En castellano (YouTube): Nokzu (una guía por profesión), Jusohr («Guía definitiva de profesiones»), AlterTime, ElonCS (configuración 12.1).

---

## 7. Addons imprescindibles (Midnight, 2026)

**Contexto importante**: desde el parche 12.0 (enero de 2026) los «Secret Values» (lo que la comunidad llama el «desarme de addons») impiden a los addons leer y reaccionar a datos de combate en tiempo real. **WeakAuras ya no funciona en combate** (solo auras fuera de combate), desaparecen Hekili y GTFO, y Blizzard ha metido en la interfaz base el gestor de reutilizaciones, la línea temporal de jefes, etc. Fuente: [NextTier](https://nexttier.pro/guide/best-wow-midnight-addons) (publicado 4-7, actualizado 4-8-2026), confirmado en general por [Conquest Capped](https://conquestcapped.com/guides/wow/midnight-best-addons/) y otros. Son webs de empresas de «boosting»: lo uso solo para la lista, no para afirmar compatibilidades finas.

Los 15 más recomendados en las guías consultadas y en los vídeos en castellano más vistos (enlaces a CurseForge **no comprobados**: CurseForge bloquea la lectura automática; los nombres de URL son los habituales):

| Addon | Para qué | Enlace |
|---|---|---|
| Details! | Medidor de daño y sanación | https://www.curseforge.com/wow/addons/details |
| BigWigs (+ LittleWigs) | Avisos de jefes en bandas (y mazmorras/profundidades con LittleWigs) | https://www.curseforge.com/wow/addons/big-wigs |
| Deadly Boss Mods (DBM) | Alternativa a BigWigs (usar uno de los dos) | https://www.curseforge.com/wow/addons/deadly-boss-mods |
| Raider.IO | Puntuación M+ en descripciones y buscador de grupos | https://www.curseforge.com/wow/addons/raiderio |
| Mythic Dungeon Tools (MDT) | Planificar rutas de M+ | https://www.curseforge.com/wow/addons/mythic-dungeon-tools |
| OmniCD | Reutilizaciones del grupo (cortes, defensivos) | https://www.curseforge.com/wow/addons/omnicd |
| WarpDeplete | Temporizador de M+ | https://www.curseforge.com/wow/addons/warpdeplete |
| Plater / Platynator | Placas de nombre (Platynator está hecho para la API de Midnight; parte de los scripts de Plater ya no funcionan) | https://www.curseforge.com/wow/addons/plater-nameplates |
| Premade Groups Filter | Filtrar el buscador de grupos | https://www.curseforge.com/wow/addons/premade-groups-filter |
| Method Raid Tools | Asignaciones de banda | https://www.curseforge.com/wow/addons/method-raid-tools |
| Cell / VuhDo | Marcos de banda para sanadores | https://www.curseforge.com/wow/addons/cell |
| ElvUI | Interfaz completa (se descarga de tukui.org, no de CurseForge) | https://tukui.org |
| Baganator | Bolsas y banco | https://www.curseforge.com/wow/addons/baganator |
| Auctionator / TradeSkillMaster | Casa de subastas y oro | https://www.curseforge.com/wow/addons/auctionator |
| HandyNotes / GatherMate2 | Notas en el mapa, puntos de recolección | https://www.curseforge.com/wow/addons/handynotes |

Otros que salen: BugSack (errores), Pawn, Plumber, Leatrix Plus, OmniCC, Bartender4/Dominos; para JcJ, Gladius / sArena Reloaded, OmniBar, BigDebuffs; para viviendas, addons de decoración (vídeo de Phobyac). EllesmereUI aparece en vídeos en castellano como interfaz de un solo addon.

---

## 8. Calendario (17-10-2026 → mediados de enero de 2027)

| Fecha | Qué | Estado / fuente |
|---|---|---|
| 13/14-10 | Sale 12.1.5 (Kith'ix, Laberinto de Kindo'jan, Invasiones aqir) | Oficial (notas 12.1.5; Raider.IO) |
| 18-10 → 1-11 | **Halloween / Halloween de Azeroth (Hallow's End)**; Jinete sin cabeza por el buscador, nivel 10-90 | Ventana anual habitual ([warcraft.wiki.gg](https://warcraft.wiki.gg/wiki/Hallow%27s_End)); **2026 sin anuncio oficial encontrado** |
| Semana del 20/21-10 | Orin ofrece «Ascending with Venomstones» (Venomstones ascendentes) y **se quita el tope de blasones** | Oficial (notas 12.1.5) |
| 1-11 → 3-11 aprox. | Día de los Muertos | Patrón habitual **[SIN CONFIRMAR 2026]** |
| **4-11** | **Lanzamiento de World of Warcraft: Forever** (no es Retail, pero es lo de la web) | BlizzCon 2026 ([GamesRadar](https://www.gamesradar.com/news/live/blizzcon-2026-everything-announced/), [wow.gg](https://wow.gg/guides/wow-blizzcon-2026)) |
| Mediados de noviembre → principios de diciembre | **22.º aniversario de WoW** (en 2025 empezó a mediados de noviembre con bonificación de PX hasta el 7-12) | **[SIN CONFIRMAR 2026]** ([MassivelyOP 2025](https://massivelyop.com/2025/11/17/world-of-warcrafts-21st-anniversary-celebrations-begin-in-retail-and-classic/)) |
| Semana del Día de Acción de Gracias de EE. UU. (26-11) | Generosidad del Peregrino (Pilgrim's Bounty) | Patrón habitual **[SIN CONFIRMAR 2026]** |
| ~8-12 | **12.1.7 «Echoes of the Worldcore»** (Talebound, Dornogal, Turbulent Timeways) | **ESTIMACIÓN** de BlizzardWatch; oficial solo «finales de otoño / principios de invierno» |
| 16-12 → 2-1 | **Festival de Invierno (Feast of Winter Veil)**; regalos desde el 25-12 | Ventana anual habitual ([warcraft.wiki.gg](https://warcraft.wiki.gg/wiki/Feast_of_Winter_Veil)) **[2026 sin confirmar]**; datamining de una montura nueva de Winter Veil en 12.1.7 |
| Mensual | Feria de la Luna Negra (primer domingo de cada mes); Paseo en el tiempo cada pocas semanas | Patrón; consultar el calendario del juego |
| ~26-1-2027 | Posible fin de la T2 | **ESTIMACIÓN** (ggseason.com); Blizzard suele avisar 2-4 semanas antes |
| Sin fecha | 12.2 «Eclipse» y Temporada 3 justo después | Oficial (BlizzCon) sin fecha |

---

## 9. Qué buscan los jugadores hispanos de Retail

Método: búsquedas en YouTube en castellano (16-10-2026), mirando títulos, canal y visualizaciones. No tengo datos de Google Trends ni de búsquedas de Google (no accesibles), así que es una aproximación.

Lo que más visualizaciones tiene (vídeos en castellano sobre Midnight):

| Tema | Ejemplos (canal — vídeo — visitas) |
|---|---|
| **Subir de nivel rápido** | Dalaran Gaming — «La forma más rápida de subir de nivel del 1 al 90…» — 120 000; DiabloManDan — ruta 10-90 — 55 000; Slothgc — 34 000; AlterTime — 80-90 en menos de 2 h — 12 000 |
| **Addons e interfaz** | xenulias — «Los mejores addons para Midnight (+30)» — 62 000; xenulias — «Interfaz completa» — 44 000; SouzaCarlosTV — 35 000; RixarTV, DonPipeloTV, Jusohr… |
| **Equipo / qué hacer al 90 / guía semanal** | xenulias — «Guía de equipo» — 52 000 y T2 42 000; «Qué hacer al llegar a nivel 90» — 34 000; RixarTV — «Equípate fácil… (guía semanal)» — 15 000 |
| **Mejor clase / tier list** | The Comeback Kids — 5 clases más seguras T2 — 57 000; xenulias — mejores clases T2 — 33 000; Saltii — tier list DPS a distancia 12.1.5 — 22 000 |
| **Míticas+** | SouzaCarlosTV — «Todo sobre las Míticas+ en la T2» — 33 000; sus guías de cada mazmorra 12 000-19 000; Tactyks (doblado) — Arena de la Cicatriz del Vacío — 42 000 |
| **Banda** | AlterTime — guía completa del Abismo Venenoso — 16 000; Jimmyfumi (un vídeo por jefe, 6000-12 700); Yuki Series; Taberna de Mercys |
| **Oro** | Nokzu — 3 métodos de oro — 21 000; DANTAES (Farmers de Azeroth) muchos vídeos; «pagar la suscripción con oro» es tema recurrente |
| **Profesiones** | ElonCS — configuración 12.1 — 18 000; Nokzu — Encantamiento — 12 500; AlterTime — 11 400 |
| **Empezar / volver** | Jusohr — «Guía definitiva para empezar en WoW Midnight 2026» — 18 000; xenulias — guía general — 31 000 |
| **Viviendas (housing)** | Bleugwendel 12 500, DiscordianKitty 12 000; el resto pocas visitas |
| **JcJ** | Poco en castellano (Skill Capped doblado 16 000-44 000); guías de clase JcJ con <3000 |

Creadores de Retail en castellano que salen una y otra vez: **xenulias** (el de más visitas: addons, equipo, clases), **SouzaCarlosTV** (M+), **AlterTime** (bandas, nivel, profesiones), **Nokzu** (profesiones y oro), **DANTAES** (oro), Jusohr, RixarTV, Bletzus, Jimmyfumi y Yuki Series (jefes de banda).

Conclusiones para tráfico:
1. Lo que más se busca es **práctico y de «qué hago ahora»**: subir rápido, addons/interfaz, equipo y guía semanal, mejor clase.
2. Las guías por mazmorra y por jefe tienen un público fiel pero menor (5000-20 000 por vídeo).
3. **Hay que usar los nombres en castellano** (y los ingleses, porque mucha gente busca «Murder Row» en inglés).
4. El público latinoamericano usa otros nombres (es-MX: «Valle Enceguecedor», «Arena Rajavacío»). Poner ambos atrae a los dos públicos.
5. Muchamiel aparece en TwitchMetrics como streamer de WoW en castellano centrado en Classic/SoD ([twitchmetrics](https://www.twitchmetrics.net/c/108809839-muchamiel)); el apartado Retail sería para captar público nuevo, no el suyo actual.

---

## 10. Propuesta de estructura del apartado «WoW Retail»

Por tráfico esperado (de más a menos), con el menú pedido:

1. **Portada Retail / «Empieza aquí»**: expansión, parche y temporada actuales en un recuadro (12.1.5, T2, nivel 90), qué hacer al llegar a 90, guía semanal (Gran Cámara, blasones, Venomstones), cuenta atrás al próximo parche. *Página a revisar cada semana.*
2. **Clases** (índice de 13 clases → 40 fichas de espec.): rol, posición en las tier lists con fuente y fecha, enlace a Icy Veins y al calculador de talentos de Wowhead. Además, una página «Mejor clase de la temporada» (es la búsqueda más fuerte).
3. **Subir de nivel**: 1-70 (Chromie Time), 70-80, 80-90 con mapa de zonas, mazmorras para subir, modo aventura para alters, trucos. Tiempo estimado.
4. **Addons**: los 15 imprescindibles explicados en castellano + qué cambió con Midnight (WeakAuras) + cómo instalar (CurseForge/Wago) + paquete de interfaz recomendado.
5. **Mazmorras (Míticas+)**: afijos de la semana, tabla de recompensas por nivel, 8 fichas (nombre en/es-ES/es-MX, entrada, jefes, consejos), sala de portales. Avance de la T3.
6. **Bandas**: Abismo Venenoso (8 jefes, una ficha por jefe con resumen y vídeo en castellano), Kith'ix, guarida de Nymrissa; fechas de apertura y alas del buscador.
7. **Profesiones**: cambios en Midnight y 12.1, para qué sirve cada una, mejores combinaciones para hacer oro, enlaces a guías. (Se puede añadir «Oro» como subpágina: busca mucho.)
8. **Notas del parche**: resumen en castellano de cada parche/arreglo oficial (12.1.5 ahora, 12.1.7 cuando salga) con enlace a la noticia de Blizzard. Se puede reaprovechar el `notas_blizzard.py` de Forever.
9. **Calendario**: eventos y fechas (tabla del apartado 8), marcando «oficial» frente a «estimado».

Extras que dan tráfico y no están en el menú: **Viviendas (housing)** y **JcJ** (poca competencia en castellano, menos búsquedas). Dejarlos para una segunda fase.

---

## Lo que no he podido comprobar

- Texto literal de la tienda de Battle.net sobre la suscripción (1-80 incluido, Midnight aparte): pide inicio de sesión.
- Archon / Warcraft Logs / u.gg (bloqueados): no hay datos de registros de banda; he usado Icy Veins y Wowhead (vía Leprestore) y un recuento propio con Raider.IO.
- Wowhead directamente (403): sus tier lists de tanques y sanadores, y que los enlaces del calculador de talentos funcionen (el formato es el estándar).
- Enlaces de CurseForge (403): los nombres de URL son los habituales, no los he podido abrir.
- Nombres oficiales en castellano: Murder Row, Kith'ix, Devorador, los jefes de la banda (tomados de vídeos) y si «Arena Lacravacua» / «Valle Cegador» son es-ES y «Rajavacío» / «Enceguecedor» son es-MX.
- Fechas 2026 de Halloween de Azeroth, Día de los Muertos, aniversario, Generosidad del Peregrino y Festival de Invierno (pongo las ventanas habituales).
- Fecha de 12.1.7 (solo hay estimación), de 12.2 Eclipse, del fin de la T2 y del inicio de la T3.
- Lista completa de la T3 de M+ (las fuentes no coinciden más allá de 5 mazmorras).
- Fecha exacta de 12.0.7 (16-6 o 30-6).
