# Cómo puede crecer el contenido de Muchamiel (investigación del 16-10-2026)

Datos públicos mirados el 16-10-2026 entre las 04:45 y las 05:00 (hora peninsular), sin iniciar sesión en nada y sin escribir a nadie. Donde no se ha podido ver un dato, se dice. Las cifras de la competencia son de ese mismo momento.

**Cómo se ha mirado:**
- **YouTube:** páginas públicas del canal (vídeos, shorts, directos, listas) y de vídeos sueltos con curl. YouTube manda desde España a una pantalla de consentimiento. Para saltarla se envió la cookie mínima `SOCS=CAI`, que es el estado sin aceptar las cookies opcionales. No se aceptó nada.
- **Twitch:** su API pública de la web (la misma que usa twitch.tv sin sesión): paneles, título, horario, emisiones guardadas y clips.
- **Comandos del chat:** API pública de Nightbot y de StreamElements.
- **Kick:** API pública del canal.
- **Discord:** API pública de invitaciones (solo da el nombre y el número de miembros).
- **TikTok:** HTML público del perfil.
- **TwitchTracker:** página pública.

## 0. Resumen en 10 líneas

1. **La base es buena.** Muchamiel publica casi un vídeo largo al día, entre 1 y 2 shorts al día y hace directos diarios de 5 a 10 h en Twitch, YouTube y Kick a la vez. YouTube ha pasado de 79,1 K a 80,6 K suscriptores en una semana (+1,5 K) y Twitch de 35,7 K a 36,3 K seguidores (+663).
2. **Lo que mejor le funciona son los nombres conocidos y los conflictos.** XOKAS vs MUCHAMIEL tiene 63 K visitas, BANEAN A XOKAS 58 K, el short DUELO CON PAYO 117 K y el de RUBIUS 111 K. También funcionan las guías de «qué elegir»: la tier list tiene 73 K y tanks y heals 54 K. Lo que menos funciona es la opinión sin gancho: «LO PEOR DE WOW FOREVER… PVP» se queda en 10 K.
3. **El fallo grande es que nada lleva a la web ni junta a la comunidad.**
   - Ninguna descripción de YouTube enlaza la web.
   - Twitch tiene 4 paneles y ninguno es la web, el Discord ni el horario.
   - Hay 2 servidores de Discord con 3 enlaces distintos según el sitio.
4. **Hay comandos rotos o viejos.**
   - `!redes`: el enlace de YouTube está cortado y el Discord ya no existe; en StreamElements el «YouTube» lleva a Twitter.
   - `!torneo` lleva a tbcleague.com (una liga 3c3 antigua).
   - `!drops` dice «alguna movida fea de retail».
   - `!server` dice «spineshatter».
5. **YouTube no tiene ninguna lista de WoW Forever.** Las 18 listas son de Pandaria, SoD y WotLK. Los vídeos no tienen capítulos ni palabras clave.
6. **La competencia en inglés gana con menos texto y más historia.** Pikaboo y Xaryu sacan 70-240 K por vídeo con títulos de 5 a 9 palabras y miniaturas de 2 o 3 palabras con una cara. Venruki traduce sus títulos: en España se ven en castellano.
7. **El torneo del 17-18 da una historia propia.** Hay 5.555 $ para el mejor de cada clase, así que puede ser «el mejor Brujo del torneo». Además está el duelo España vs España con Xokas. Después tocan el vídeo resumen, los shorts de cada duelo y la retransmisión en castellano de la final si las normas lo permiten.
8. **Hay tres fechas clave.**
   - Lunes 19-10 a las 19:00: prueba de estrés gratis para todos.
   - 27-10: reserva de nombres.
   - 5-11 a las 00:00 (hora de España): lanzamiento.
   Cada fecha pide un short, un vídeo, un directo especial y una página de la web con su `!comando`.
9. **Las 5 primeras mejoras cuestan menos de 2 horas en total:** arreglar los comandos, un único Discord, la web en la primera línea de cada descripción, 8 paneles en Twitch y un horario oficial.
10. **No se ha podido ver:** las publicaciones de TikTok, X e Instagram (piden sesión), las estadísticas internas (retención, CTR) ni si los shorts ya tienen puesto un «vídeo relacionado». La web no tiene contador de visitas, así que hoy no se puede medir lo que llega desde los canales.

---

## 1. Datos de partida (16-10-2026)

| Canal | Dato | Fuente |
|---|---|---|
| YouTube @muchamiel | **80,6 K suscriptores**, 3,7 K vídeos (el 09-10 tenía 79,1 K) | https://www.youtube.com/@muchamiel |
| YouTube: vídeos largos | 30 en unas 3 semanas (≈1,4 al día), de 8 a 36 min. Visitas: mediana **26,5 K**, media 31,7 K, de 10 K a 73 K | https://www.youtube.com/@muchamiel/videos |
| YouTube: shorts | 47 visibles. Visitas: mediana **≈27 K**, de 3,7 K a 315 K | https://www.youtube.com/@muchamiel/shorts |
| YouTube: directos | Uno al día, de 3 a 11 h, entre 8,3 K y 42 K visitas (72 K el día que abrió la beta) | https://www.youtube.com/@muchamiel/streams |
| Twitch | **36.326 seguidores** (35.663 el 09-10). Directo diario que empieza entre las 15:20 y las 17:50 UTC (17:20-19:50 en España) y dura de 3,4 a 11 h. Sin horario configurado. 4 paneles (1 es una extensión) | https://www.twitch.tv/muchamiel |
| Twitch (TwitchTracker) | 532 espectadores de media, pico de 1.466, 203 h emitidas y 8.639 seguidores ganados. La página no deja claro el periodo (por defecto suele ser «últimos 30 días»). Puesto 143 entre los canales en castellano | https://twitchtracker.com/muchamiel |
| Twitch: suscriptores | 1.837 según el dato que ya teníamos (STATS en comunidad_portal.py), con 2.000 como meta del sorteo. TwitchTracker no da la cifra actual | — |
| Twitch: clips | El mejor clip del último mes tiene 466 visitas, el segundo 390 y el resto menos de 125. Los hacen los espectadores, con títulos como «tilt» o «Cepillo de dientes» | https://www.twitch.tv/muchamiel/clips |
| Kick | 8.470 seguidores. La última emisión guardada es del 12-10 (de 115 a 544 visitas cada una). No tiene el Discord puesto en el perfil | https://kick.com/muchamiel |
| TikTok @muchamielwow | **14.261 seguidores, 465.954 me gusta, 750 vídeos.** La biografía sigue diciendo «Creador de contenido de WOW CLASSIC» | https://www.tiktok.com/@muchamielwow |
| X @Muchamiel_ | 3.588 seguidores (dato del 09-10; hoy no se ha podido ver sin sesión) | https://x.com/Muchamiel_ |
| Instagram @muchamiel_ | 4.099 seguidores (dato del 09-10; hoy no se ha podido ver) | https://www.instagram.com/muchamiel_/ |
| Discord «Muchamiel» | **1.711 miembros**, 172 conectados (invitación eu3e3zm4fq, la de las descripciones de los directos y la web) | https://discord.gg/eu3e3zm4fq |
| Discord «WOW FOREVER - MUCHAMIEL» | **689 miembros**, 99 conectados. Es la invitación de `!discord` (QateSZqJU8) y la de los vídeos (U8VkN5yXJ8), que estos presentan como «¿quieres vivir de crear contenido?» | https://discord.gg/U8VkN5yXJ8 |
| Web | https://muchamielwow.github.io/ en castellano e inglés: clases, macros de las 9 clases, calculadora, addons, razas, torneo, lanzamiento, reserva de nombres y sorteos. **No tiene contador de visitas** (no se ha encontrado ninguno en el HTML) | https://muchamielwow.github.io/sitemap.xml |

**Sus vídeos de WoW Forever que mejor y peor van (16-10):**
- **Arriba:** ¿QUÉ CLASE DEBERÍAS JUGAR…? TIER LIST (73 K) · XOKAS vs MUCHAMIEL ¿QUIÉN ES EL MEJOR JUGADOR DE ESPAÑA? (63 K) · BANEAN A XOKAS… (58 K) · ¿TANKS Y HEALS?… (54 K) · BLIZZARD DESTRUYE AL GNOMO (54 K).
- **Abajo:** LO PEOR DE WOW FOREVER… PVP (10 K) · ME OBLIGAN A HACERME OTRO PJ… (12 K) · ¿QUÉ ES WOW FOREVER? BLIZZARD CUENTA TODA LA VERDAD (15 K).
- **Shorts arriba:** 2000 LVLS 20 ACABAN CON UN DRAGÓN ÉLITE (315 K) · RAID DE RUBIUS Y XOKAS (145 K) · SI BLIZZARD HACE CASO A LOS RETAILERS (134 K) · SNOOPDOGG… (130 K) · DUELO CON PAYO (117 K).
- **Shorts de duelos contra profesionales:** Jaytii 8,7 K, Whaazz 20 K, Aphane 19 K. El de Payo saca 117 K.

**Conclusión:** gana lo que tiene un nombre que la gente conoce, un espectáculo visual o una decisión del jugador («qué clase/raza elijo»). El duelo contra un campeón que el público hispano no conoce no arrastra si el título no explica quién es.

---

## 2. Diagnóstico por canal

### Twitch (36,3 K seguidores)
**Qué hace bien:**
- Directo diario y largo: 203 h en el periodo de TwitchTracker.
- Comandos en el título (`!SORTEO`, `!PLUS`, `!addons`) y metas claras (2.000 suscriptores = sorteo de 1 año).
- Emite a la vez en YouTube y en Kick.
- Ya existe `!web`.

**Qué falla:**
- **Paneles.** Tiene 4, sin la web, el Discord, el horario, los códigos de marcas ni el equipo. Los demás tienen entre 6 y 14: Payo 10 (con Discord, YouTube y Twitter), Pikaboo 10 (con «My Macros I Use!» y su armería), Xokas 14 (con Discord y empresa), Venruki 10, Shobek 8, Xaryu 7 y Savix 6.
- **No tiene horario configurado.** De los 7 canales mirados, solo Xokas lo tiene (todos los días a las 16:00 UTC, «mandangón»).
- **El título es muy largo y lo que importa va al final.** El de hoy: «!SORTEO NO VA EL WOW - 2 DÍAS PARA EL TORNEO SOY UNA BESTIA - WOW FOREVER BRUJO💥!PLUS💥TORNEO PVP días 17/18 oct | MUCHAMIEL» (≈125 caracteres). En el móvil solo se ve el principio.
- **Comandos rotos o viejos** en Nightbot (lista completa en el punto 4.1): `!redes`, `!torneo`, `!drops`, `!server`, `!wa`, `!guia`, `!sod`, `!racelock`, `!hardcore`… En StreamElements, `!redes` manda «youtube» a Twitter.
- **Clips casi muertos.** El mejor clip del mes tiene 466 visitas. Payo tiene uno con 36.179, Pikaboo uno con 33.604 y Xokas uno con 18.141. Nadie del canal convierte los momentos en clips con buen título.
- **Riesgo con Twitch:** el comando `!kick` dice «suscríbete en Kick, que es donde más ayudas». Las normas de emisión simultánea de Twitch, según la prensa (no se pudo abrir la página oficial), piden no mandar a los espectadores de Twitch a la emisión de otra plataforma. Conviene quitarlo del chat de Twitch y dejarlo solo en Kick.

### YouTube (80,6 K suscriptores)
**Qué hace bien:**
- Ritmo muy alto: un vídeo largo al día, entre 1 y 2 shorts al día y el directo guardado.
- Temas del momento y miniaturas con cara, Xokas y el logo de Forever.
- Pide la suscripción con un sorteo («1 AÑO A LOS 90K, OTRO AÑO A LOS 100K»).

**Qué falla:**
- **Descripciones.** Tienen Twitch, Kick, redes y Discord, pero **no la web**. El vídeo del exploit (15-10) tampoco lleva el Discord de la comunidad, solo el de «vivir de crear contenido». Los vídeos no tienen **capítulos** y la ficha no tiene **palabras clave**.
- **Listas.** No hay ninguna de WoW Forever. Las 18 son antiguas: Pandaria, SoD, WotLK, «directos»…
- **Directos de 5 a 10 h sin capítulos.** Nadie que llegue después encuentra «el duelo contra X».
- **Títulos.** Todo en mayúsculas, con 💥 y dos frases (≈80-95 caracteres). En móvil se cortan. Los que funcionan llevan un nombre o una pregunta en las primeras palabras.
- **Miniaturas.** Están bien, pero con dos bloques de texto (arriba y abajo), dos caras y el logo. Xaryu y Pikaboo usan 2 o 3 palabras y una sola cara. Ver la comparación más abajo.
- **Shorts.** En la descripción llevan enlaces, pero YouTube los hizo no clicables en los shorts. Ahora hay que usar el campo «vídeo relacionado» (Search Engine Journal y Social Media Today; lo comentan también vidIQ y Opus). No se ha podido ver si sus shorts ya lo tienen.

### Kick (8,5 K seguidores)
- **Bien:** emite lo mismo y tiene `!kick` y la ruleta para suscripciones de Kick.
- **Mal:**
  - La última emisión guardada es del 12-10, cuando en Twitch hay emisiones del 13 al 15. O no guarda las emisiones o no emitió.
  - El perfil no tiene el Discord.
  - La biografía dice «World of Warcraft Classic».
  - Las emisiones guardadas tienen pocas visitas (de 115 a 544).
- **Prioridad baja:** basta con que la biografía y los enlaces estén al día.

### TikTok (14,3 K seguidores, 466 K me gusta, 750 vídeos)
- **Bien:** volumen alto (750 vídeos) y una media de unos 620 me gusta por vídeo.
- **Mal:**
  - La biografía dice «WOW CLASSIC» y no WoW Forever.
  - No se ha podido ver si tiene la web enlazada ni qué publica ahora (TikTok no enseña la lista sin el navegador completo).
  - En proporción, tiene pocos seguidores para los me gusta que acumula: el contenido gusta, pero no lleva a seguir. Falta una serie que se repita.

### X (3,6 K) e Instagram (4,1 K)
- Datos del 09-10; hoy no se han podido abrir sin sesión.
- Él dice que X es «la red social que más uso».
- No hay datos de frecuencia. Lo mínimo: anclar en X la publicación del torneo o del lanzamiento con la web, y en Instagram poner la web en la biografía.

### Discord (1.711 + 689 miembros)
- **Bien:** dos comunidades vivas (172 y 99 conectados a las 5 de la mañana).
- **Mal:** están partidas.
  - `!discord` y las descripciones de los vídeos llevan a «WOW FOREVER - MUCHAMIEL» (689).
  - Los directos y la web llevan a «Muchamiel» (1.711).
  - `!redes` lleva a una invitación que ya no existe.
  - La descripción del servidor pequeño tiene los enlaces pegados («…twitch.tv/muchamielhttps://www.youtube…»).
  - **Hay que elegir uno** (o dejar claro cuál es para la comunidad y cuál para creadores) y usar el mismo enlace en todas partes.

### Web (muchamielwow.github.io)
- **Bien:** hay contenido que nadie en castellano tiene junto: macros de las 9 clases, calculadora de talentos, addons de su vídeo, razas, torneo, lanzamiento, reserva de nombres y versión en inglés.
- **Mal:**
  - Solo la enlaza `!web`. No aparece en paneles, descripciones, biografías, pantalla del directo ni comentarios fijados.
  - No tiene contador de visitas, así que no se sabe qué funciona.

---

## 3. Qué hacen distinto los que crecen (datos del 16-10)

| Creador | Twitch (seguidores, paneles, horario) | Título del directo (16-10) | YouTube reciente |
|---|---|---|---|
| **Xaryu** | 866 K · 7 paneles (patrocinadores, propinas, YouTube, Amazon, tienda, guía de nivel) · sin horario | «!DROPS, HOSTING $100k !TOURNY THIS WEEKEND \| 7 MORE DAYS OF FOREVER BETA»: 2 comandos y la cuenta atrás delante | 3 vídeos en 9 h. Mezcla vídeos propios con «Xaryu Reacts to…» sobre vídeos de otros y entrevistas de Blizzard (240 K, 184 K, 136 K). Shorts de frases con 802 K, 254 K y 159 K |
| **Pikaboo** | 669 K · 10 paneles, entre ellos **«My Macros I Use!»** y armería · sin horario | «WOW FOREVER BETA HUGE 100k DUEL TOURNY?? YESSSSSSS! MULTISTREAMING! !wallet !vetra #ad !youtube» | Unos 2 al día, de 71 K a 208 K. Títulos con historia y nombres («Ziqo Just Lost to the "Worst Class"…», «Sodapoppin Says Priest Takes No Skill…»). Miniaturas de 2 o 3 palabras («NO WAY…», «THE CABAL») |
| **Payo** | 458 K · 10 paneles (Discord, YouTube, Twitter, guía de nivel) · sin horario | «NEW !GRIEF UNLOCKED !BANNED AND !TIRED \| 100K$ !TOURNEY PREP…»: los comandos cuentan la historia | Uno al día, de 32 K a 215 K. Títulos cortos en tipo frase («I Found the Most TOXIC Item in WoW Forever»). Su mejor clip tiene 36 K visitas |
| **Venruki** | 377 K · 10 paneles · sin horario | «WOW FOREVER BETA! \| UPDATE TODAY? \| $100,000 TOURNEY THIS WEEKEND» | **Títulos traducidos**: desde España se ven en castellano («Probé a mi mago contra todas las clases en WoW para siempre», 46-102 K). Shorts de 133 K a 514 K |
| **Savix** | 375 K · 6 paneles · sin horario | «1 MORE DAYS & ITS DUELING TOURNAMENT TIME»: cuenta atrás | Serie documental **«Meet …»** (Swifty, Soda, Ahmpy, Jokerd, Xaryu): de 157 K a 328 K, contenido que dura |
| **Xokas** (hispano) | 4,43 M · 14 paneles · **el único con horario** (todos los días a las 16:00 UTC) | Emojis como separador y la historia del día con comandos (`!BANEADO`, `!ZAZZA`) | Su canal principal no es de WoW. Su mejor clip del mes de WoW tiene 12,7 K visitas («UN DRAGÓN») |
| **Pequeños hispanos (LATAM)** del directorio de WoW en castellano a las 04:50 | dulcegema_ 7,6 K (gremio «ForeverLATAM», +50 streamers), zerstgaming 7,5 K, android_mercys 6,3 K | Comandos útiles en el título: «!MACROS !ENANO», «Guías !aflic !demo !destro», «!addons» | — |

Fuentes: https://www.twitch.tv/xaryu · https://www.twitch.tv/pikabooirl · https://www.twitch.tv/payo · https://www.twitch.tv/venruki · https://www.twitch.tv/savix · https://www.twitch.tv/elxokas · https://www.youtube.com/@Xaryu · https://www.youtube.com/@pikabooirl · https://www.youtube.com/channel/UCQ-czOmPo1JYi1wKFi7wY8w (Payo) · https://www.youtube.com/@venruki · https://www.youtube.com/c/Savixirl · https://www.twitch.tv/directory/category/world-of-warcraft (filtro de idioma: castellano).

**Lo que se repite en los que crecen:**
1. **El título del directo cuenta una historia corta** y luego pone 1 o 2 comandos.
2. **Hay paneles útiles** (macros, armería, Discord) además de los de dinero.
3. **Títulos de YouTube en tipo frase**, con un nombre propio y una tensión.
4. **Miniaturas de 2 o 3 palabras**, una cara y un elemento del juego.
5. **Reacciones y entrevistas**: Xaryu reacciona a vídeos de otros creadores y de Blizzard.
6. **Series que se repiten** («Meet …» de Savix).
7. **Títulos en varios idiomas** (Venruki).

**Miniaturas comparadas** (4 de Muchamiel, 4 de Xaryu y 4 de Pikaboo, vistas el 16-10):
- **Muchamiel:** 2 bloques de texto de 3 a 4 palabras, Xokas y él, y el logo. Se leen bien en grande, pero en pequeño compiten tres cosas.
- **Pikaboo:** cara en primer plano y 2 palabras («NO WAY…»).
- **Xaryu:** cara con emoción, imagen del juego y 0 a 3 palabras.

---

## 4. Las 15 mejoras de más impacto y menos esfuerzo (en orden)

| # | Mejora | Por qué (dato o ejemplo) | Esfuerzo | Cómo medirla |
|---|---|---|---|---|
| 1 | **Arreglar los comandos rotos y crear los de la web** (`!redes`, `!torneo`, `!discord`, `!drops`, `!server`; nuevos `!macros`, `!talentos`, `!nombres`, `!lanzamiento`, `!codigos`). Textos en el punto 8.5 | `!redes` lleva a un Discord que ya no existe y a un enlace de YouTube cortado. `!torneo` lleva a una liga 3c3 antigua. Los streamers LATAM del directorio ponen `!MACROS` y `!aflic` en el título; Pikaboo tiene un panel de macros | 30 min (Nightbot) | Visitas a /macros/warlock/ y /torneo/ con el contador del punto 14. Uso de los comandos en el panel de Nightbot |
| 2 | **Un único Discord** y el mismo enlace en todas partes (comandos, paneles, descripciones, Kick, web) | Hay 1.711 y 689 miembros con 3 invitaciones distintas. Quien entra al pequeño desde un vídeo no ve los avisos del grande | 15 min elegir + 15 min cambiar enlaces | Miembros del servidor elegido cada lunes (la API pública da `approximate_member_count`) |
| 3 | **La web en la primera línea de cada descripción de YouTube**, con el enlace a la página concreta del vídeo (addons → /addons/, razas → /razas/…). Plantilla en el punto 8.3 | Hoy no aparece en ninguna descripción. Los vídeos largos suman unos 950 K visitas en 3 semanas: aunque solo pulse un pequeño porcentaje, sería la mayor fuente de visitas de la web | 2 min por vídeo, o una vez con la plantilla por defecto de YouTube Studio | Visitas a la web desde youtube.com (contador del punto 14) |
| 4 | **8 paneles en Twitch**: Web y guías · Macros del Brujo · Discord · YouTube · Horario · Códigos y marcas · Propinas · Normas del chat. Sin panel de Kick (ver el riesgo en el punto 2) | Él tiene 4. Los que crecen tienen entre 6 y 14 (Pikaboo, Payo y Venruki 10; Xokas 14) y ponen herramientas, no solo dinero | 1 h (las imágenes pueden ser texto sobre fondo plano) | Clics en los paneles: Twitch no los cuenta, pero sí las visitas a la web con `?ref=twitch` |
| 5 | **Horario oficial en Twitch** (Panel de control › Preferencias › Canal › Programación) **y el mismo horario en la web y en el panel** | Xokas es el único de los 7 que lo tiene. Twitch enseña el horario a cada uno en su hora (technipages, streamscheme), lo que ayuda con el público LATAM: hoy empieza a las 17:30 en España, que son las 09:30 en México y las 12:30 en Argentina | 15 min | Espectadores de media en TwitchTracker, comparando las 4 semanas de antes y de después |
| 6 | **Listas de WoW Forever en YouTube**: «Guías WoW Forever», «Brujo PvP», «Noticias y cambios», «Directos WoW Forever», «Shorts WoW Forever», «Torneo The Forever Open». Y poner la de guías en la página principal | No tiene ninguna lista de Forever (las 18 son de Pandaria, SoD y WotLK). Con una lista, quien termina un vídeo pasa al siguiente sin buscar | 45 min | Tiempo de visualización desde «listas» en YouTube Studio (no se ve desde fuera) |
| 7 | **«Vídeo relacionado» en cada short** que lleve al vídeo largo del mismo tema (o al directo del día) | En los shorts los enlaces de la descripción no se pueden pulsar desde el 31-08-2023. El campo «vídeo relacionado» es la vía que queda (Search Engine Journal, Social Media Today, vidIQ). Sus shorts tienen una mediana de 27 K visitas que hoy no llevan a nada | 1 min por short (YouTube Studio en el ordenador) | Visitas al vídeo largo desde «Shorts» en YouTube Studio |
| 8 | **Shorts con nombre o espectáculo en las primeras palabras**, y en los de duelos decir quién es el rival («x16 CAMPEÓN DEL MUNDO» ya va bien; añadir «el mejor del mundo», «R1»…) | Los que llevan nombre (Payo 117 K, Rubius 111 K, Snoop 130 K) o espectáculo (dragón 315 K) multiplican por 4 la mediana. Duelos contra rivales que el público no conoce: 8,7 a 20 K | 0 (cambiar la costumbre al titular) | Mediana de visitas de los shorts por semana |
| 9 | **Título del directo con la historia del día en los primeros 40 caracteres** y como mucho 2 comandos. Ejemplos en el punto 8.1 | Hoy empieza por «!SORTEO NO VA EL WOW -…» y llega a 125 caracteres. Xaryu, Savix y Payo ponen la cuenta atrás o la historia delante | 2 min al día | Espectadores en los primeros 30 min y seguidores por directo |
| 10 | **Pruebas A/B de miniatura y título** en cada vídeo largo (YouTube permite probar hasta 3). Probar «2-3 palabras + una cara» frente a lo de ahora | Herramienta oficial de YouTube: gana la versión con más tiempo de visualización (https://support.google.com/youtube/answer/16391400). Xaryu y Pikaboo usan miniaturas de 2 o 3 palabras y sacan 70-240 K | 10 min más por vídeo | El resultado de la prueba en YouTube Studio |
| 11 | **Capítulos en los vídeos de más de 10 min y en los directos guardados** (al menos 3 marcas, la primera en 00:00) | Ayuda oficial de YouTube sobre capítulos (https://support.google.com/youtube/answer/9884579). Sus directos de 5 a 10 h con 20 K visitas no tienen ni un capítulo | 5 min por vídeo, 10 por directo (o que lo haga un moderador) | Retención y visitas del directo guardado a los 7 días |
| 12 | **Rescatar los clips**: `!clip` en el chat, que un moderador les ponga título, el clip de la semana en Discord y pasarlos a vertical con el editor de Twitch para shorts y TikTok | Su mejor clip del mes tiene 466 visitas; Payo 36 K y Pikaboo 33 K. El editor de Twitch convierte en vertical y pone marca de agua con el nombre (Tubefilter, 05-2023) | 10 min al día (un moderador) | Visitas a los clips del mes; shorts que salen de clips |
| 13 | **Títulos y descripciones traducidos al inglés** (y doblaje automático si YouTube lo ofrece al canal) en las guías que duran: tier list, razas, addons, macros | Venruki traduce los suyos y desde España se ven en castellano (46-102 K). YouTube: doblaje automático (https://support.google.com/youtube/answer/15569972). La web ya tiene versión /en/ | 5 min por vídeo | Visitas por país o idioma del público en YouTube Studio |
| 14 | **Contador de visitas en la web**, sin cookies (por ejemplo GoatCounter u otro parecido; la decisión es de Van), y `?ref=twitch`, `?ref=yt`, `?ref=tiktok`, `?ref=kick` en los enlaces | Hoy no se puede medir nada de lo anterior. Un contador sin cookies no necesita aviso de cookies | 30 min (lo hacemos nosotros) | Es la propia medida |
| 15 | **El público LATAM**: horario en dos husos (España / México / Argentina), una colaboración o una partida con streamers del gremio «ForeverLATAM» (+50 streamers según el título de dulcegema_) y `!horario` | A las 04:50 de España el directorio de WoW en castellano lo llenaban streamers latinoamericanos (dulcegema_, zerstgaming, android_mercys…). Su directo de las 17:30 son las 09:30 en México | 1 h para la colaboración | Público por país (Twitch Analytics y YouTube Studio) |

**Extras de esfuerzo bajo y algo menos de impacto:**
- **Biografías:** TikTok («WOW CLASSIC» → «WoW Forever · Brujo · guías en muchamielwow.github.io»), Kick («Classic» → «Forever» + Discord) e Instagram (la web).
- **Una serie fija:** «Conoce a…» como la «Meet…» de Savix (157-328 K). Entrevistas a jugadores hispanos de WoW (Shobek en castellano, Xokas, rivales del torneo), una por quincena.
- **Reacciones al estilo de Xaryu** a vídeos de Blizzard o de creadores en inglés, explicadas en castellano. Muchamiel ya lo hace con Alexelcapo («ALEXELCAPO HABLA DE WOW FOREVER»).

---

## 5. Aprovechar el momento

### 5.1 Torneo The Forever Open (sábado 17 y domingo 18-10)

**Lo que dicen las normas** (https://raiderio.com/events/the-forever-open/rules-regulations-code-of-conduct):
- Clasificación el 17 (rondas suizas por grupos) y final el 18: 36 jugadores, eliminación doble y final al mejor de 5.
- **Es obligatorio emitir tu punto de vista** en la clasificación y en la final, en Twitch, YouTube o Kick.
- Hay **50.000 $ para el campeón y 5.555 $ para el mejor de cada una de las 9 clases**.
- La emisión oficial va por twitch.tv/xaryu y twitch.tv/esfandtv. **Otros streamers pueden retransmitirla** si cumplen las normas del torneo y de la plataforma.

**Antes (hoy 16 y mañana por la mañana):**
- **Short:** «Mañana juego un torneo de 100.000 $ con el Brujo» (guion 1 del punto 8.4).
- **Publicación fijada en X y en la comunidad de YouTube** con la hora, el enlace al directo y https://muchamielwow.github.io/torneo/.
- **`!torneo` arreglado** → /torneo/ (hoy lleva a tbcleague.com).
- **Título del directo:** «MAÑANA TORNEO 100.000 $ · ÚLTIMO ENTRENO BRUJO» y `!torneo`.

**Durante:**
- **Título fijo con el resultado al momento:** «TORNEO 100.000 $ EN DIRECTO · RONDA 3 · 2-0 · BRUJO».
- **Un moderador hace clip de cada duelo** con el título «Ronda N vs CLASE (nombre)».
- **X:** publicación de 1 línea por ronda. Es la red que más usa y aquí sirve como marcador.
- **Si queda eliminado**, retransmitir en castellano la emisión oficial («la final en español con Muchamiel»), si las normas de plataforma y torneo lo permiten. En castellano no hay otra opción oficial a la vista.

**Después (19-21 oct):**
- **Vídeo largo:** «Así fue mi torneo de 100.000 $ con el Brujo» (los mejores duelos, con capítulos por ronda).
- **Si queda mejor Brujo:** «SOY EL MEJOR BRUJO DEL TORNEO (5.555 $)».
- **Si cruza con Xokas:** «XOKAS vs MUCHAMIEL EN EL TORNEO». Su vídeo de este tema ya sacó 63 K.
- **Entre 5 y 8 shorts**, uno por duelo, con el rival explicado.
- **Web:** página del torneo con sus resultados y enlaces a los clips.

### 5.2 Prueba de estrés gratis (lunes 19-10, 19:00 hora de España)
Es gratis para todo el mundo: sin suscripción ni beta. Los personajes se borran al acabar. Datos en research/prueba-estres-hora.md (fuente: anuncio de Blizzard y foro EU).
- **Domingo noche o lunes por la mañana:** short «WoW Forever GRATIS hoy a las 19:00: así se entra» y página /beta-gratis/ de la web con `!gratis`.
- **Lunes:** directo «WOW FOREVER GRATIS HOY · OS ENSEÑO A EMPEZAR». Es la mejor ocasión para quien no ha jugado nunca, así que conviene ir a lo básico: clase, raza, macros, addons.

### 5.3 Reserva de nombres (27-10 a 3-11, solo con pack)
Fuentes: Blizzard Watch y playnews.gg.
- **Short y página /reserva-nombres/** con `!nombres`: «Cómo reservar tu nombre (y qué pack hace falta)».
- **Directo:** «Reservamos nombres y hermandad».

### 5.4 Lanzamiento (miércoles 4-11 15:00 PST = **jueves 5-11 a las 00:00 en España**)
Fuentes: playnews.gg y el foro de Blizzard en castellano citado en research/forever-lanzamiento.md.

**Antes (26-10 a 4-11):**
- **Una guía al día** que lleve a la web: «Qué clase jugar» (versión de lanzamiento), «Mejor raza por clase», «Macros del Brujo», «Addons imprescindibles», «Cómo subir del 1 al 60 rápido» y «Profesiones».
- **Cuenta atrás** en los títulos («5 DÍAS PARA WOW FOREVER», como hacía en la beta: «4 DÍAS PARA LA BETA 51 DÍAS PARA WOW FOREVER»).

**La noche del lanzamiento:**
- **Directo desde las 22:00 del 4-11** («ABRE WOW FOREVER A LAS 00:00 · MARATÓN»), con horario anunciado y alertas en Discord.
- **Short a las 00:30:** «La cola del primer minuto».

**Primera semana:**
- **Vídeo diario:** «Primer día», «Mi Brujo nivel X», «Lo que nadie te dice de…» y «Errores de principiante».
- **Shorts de 3 tipos:** momentos del directo, consejos de 30 s que llevan a la web (vídeo relacionado) y comparaciones beta/lanzamiento.
- **Web:** «Empieza aquí» en la portada (clase → raza → macros → addons → subir nivel) y `!empieza`.

**Después (semanas 3-6):** contenido que dura y una serie fija.
- Primer 60.
- Mazmorras (9, de Salón de los Feudales a Bancal del Creador).
- Campo de batalla 15c15.
- Preparación de las bandas de diciembre (Cavernas del Túmulo, Cima Hyjal, Onyxia; del 9 al 12-12 según Blizzard).

### 5.5 Cómo ayuda la web
- **Un comando por página:**

  | Comando | Página |
  |---|---|
  | `!web` | portada |
  | `!macros` | /macros/warlock/ |
  | `!talentos` | /calculadora/ |
  | `!addons` | /addons/ (el vídeo, también en la web) |
  | `!razas` | /razas/ |
  | `!torneo` | /torneo/ |
  | `!gratis` | /beta-gratis/ |
  | `!nombres` | /reserva-nombres/ |
  | `!lanzamiento` | /lanzamiento/ |
  | `!codigos` | /colaboraciones/ |
  | `!sorteo` | /sorteos/ |

- **Temporizador de Nightbot** cada 20 minutos que alterne `!web`, `!macros` y `!discord`.
- **En el directo:** una línea fija abajo con «muchamielwow.github.io», o un QR pequeño en la pantalla de pausa.
- **En YouTube:** la web en la primera línea de la descripción, comentario fijado con el enlace a la página del tema y tarjeta final hacia la lista de guías.
- **Del vídeo a la web y vuelta:** cada página de la web enlaza el vídeo que la explica (ya pasa con addons) y el vídeo enlaza la página. Así uno alimenta al otro.

---

## 6. Plan de 6 semanas (19-10 a 29-11-2026)

**Semana 1 (19-25 oct): resaca del torneo y prueba gratis**
- **Lunes:** comandos arreglados (punto 8.5), Discord único elegido, 8 paneles y horario en Twitch.
- **Lunes:** short y directo de la prueba de estrés gratis (19:00).
- **Martes:** vídeo «Así fue mi torneo de 100.000 $» con capítulos, y de 5 a 8 shorts de duelos con su vídeo relacionado.
- **Miércoles:** plantilla de descripción por defecto en YouTube Studio con la web arriba.
- **Miércoles:** crear las 6 listas de WoW Forever y reordenar las antiguas.
- **Jueves:** el último día completo de beta fue el 21. Vídeo «Lo que cambia de la beta al lanzamiento».
- **Viernes:** primera prueba A/B de miniatura (2-3 palabras + cara frente a la de ahora).
- **Domingo 25:** España cambia a horario de invierno. Revisar el horario de Twitch y la tabla de husos.
- **Web:** contador de visitas puesto y página del torneo con resultados.

**Semana 2 (26 oct-1 nov): preparar el lanzamiento**
- **27-10:** short, página y directo de reserva de nombres; `!nombres`.
- **Guías diarias:**
  - Qué clase jugar (versión de lanzamiento).
  - Mejor raza.
  - Macros del Brujo.
  - Cómo subir del 1 al 60.
  - Profesiones.
- **Cuenta atrás** en el título de cada directo.
- **Primera colaboración LATAM** (partida o tertulia con alguien de ForeverLATAM).
- **Primer «Conoce a…»** (entrevista de 20 min en el directo, que luego se edita en vídeo).
- **Web:** «Empieza aquí» en la portada.

**Semana 3 (2-8 nov): lanzamiento**
- **2-3 nov:** «Todo lo que necesitas para el día 1» (vídeo, short y página).
- **4-11, 22:00:** directo maratón de lanzamiento (apertura a las 00:00 del 5).
- **5-8 nov:** un vídeo diario del día 1, 2 y 3, y entre 2 y 3 shorts al día de momentos del directo.
- **Discord:** canal «busco grupo» y alertas de directo.
- **Medir:** suscriptores de YouTube (meta del sorteo: 90 K) y seguidores de Twitch al día.

**Semana 4 (9-15 nov): subir de nivel y mazmorras**
- **Serie «Mazmorras de WoW Forever»:** una por vídeo o short con su página en la web (/mazmorras/).
- **Primer 60** (cuando llegue): vídeo y short.
- **Título traducido al inglés** en las 3 guías con más visitas.
- **Revisar:** qué miniatura ganó en las pruebas A/B y aplicarlo.

**Semana 5 (16-22 nov): nivel 60 y JcJ**
- **Campo de batalla 15c15**, duelos del Brujo al 60 y «Brujo JcJ al 60: talentos y macros» (vídeo y página).
- **Segundo «Conoce a…».**
- **Clip de la semana** elegido en Discord, convertido en short.
- **Sorteo** ligado a la meta (2.000 suscriptores de Twitch o 90 K de YouTube) con `!sorteo` al día.

**Semana 6 (23-29 nov): repaso y preparar diciembre**
- **Repasar los números** de las 6 semanas (tabla del punto 7) y quedarse con lo que funcionó.
- **Preparar las bandas de diciembre:** Cavernas del Túmulo, Hyjal y Onyxia (vídeo y página).
- **Ordenar las listas** y la página principal de YouTube.
- **Decidir la serie fija de diciembre.**

### Rutina semanal fija (desde la semana 2)

| Día | Directo (Twitch + YouTube + Kick) | YouTube largo | Shorts / TikTok | X / Discord / web |
|---|---|---|---|---|
| Lunes | 17:30-02:00 · «Lunes de novedades» (parches, noticias) | Noticias y cambios de la semana | 2 (momento del directo + noticia en 30 s) | Publicación en X con el vídeo · `!web` en el temporizador |
| Martes | Directo normal (subir nivel, mazmorras) | Guía (clase, raza, profesión…) con su página en la web | 2 | Página nueva o actualizada en la web |
| Miércoles | **Día de duelos/JcJ** con los espectadores | Mejores duelos de la semana con capítulos | 2 (un duelo con el rival explicado) | Clip de la semana en Discord |
| Jueves | Directo normal | Reacción o «Conoce a…» (cada 2 semanas) | 2 | Publicación en X |
| Viernes | **Directo con invitado** (LATAM u otro creador) | Tier list / «lo mejor de la semana» | 2 | Encuesta en Discord o X para el vídeo siguiente |
| Sábado | Directo largo (mazmorras o JcJ) | — (descanso de edición) | 1-2 | — |
| Domingo | Corto o libre | Resumen de la semana (opcional) | 1 (avance de la semana) | Horario de la semana en X, Discord y web |

**Horario de referencia** (hay que confirmarlo con él), con la tabla de husos:

| Hora en España | México (CDMX, UTC-6) | Colombia (UTC-5) | Argentina (UTC-3) |
|---|---|---|---|
| 17:30 (hasta el 25-10, horario de verano UTC+2) | 09:30 | 10:30 | 12:30 |
| 17:30 (desde el 26-10, horario de invierno UTC+1) | 10:30 | 11:30 | 13:30 |

---

## 7. Cómo medir (tabla para rellenar cada lunes)

| Métrica | Dónde | Hoy (16-10) |
|---|---|---|
| Suscriptores de YouTube | página del canal | 80,6 K |
| Mediana de visitas de los últimos 7 vídeos largos | página Vídeos | ≈26,5 K (últimas 3 semanas) |
| Mediana de visitas de los últimos 10 shorts | página Shorts | ≈21,5 K (últimos 10); ≈27 K (47 visibles) |
| Seguidores de Twitch | twitch.tv / TwitchTracker | 36.326 |
| Espectadores de media en Twitch (30 días) | TwitchTracker | 532 (periodo sin confirmar) |
| Suscriptores de Twitch | panel de Twitch (él) | 1.837 (STATS) |
| Seguidores de Kick | kick.com | 8.470 |
| Seguidores de TikTok | perfil | 14.261 |
| Miembros del Discord único | invitación (API) | 1.711 / 689 |
| Visitas a la web y de dónde vienen | contador (punto 14) | sin medir |
| Visitas de los clips del mes | twitch.tv/muchamiel/clips | 466 el mejor |

---

## 8. Material listo para usar

### 8.1 Diez títulos de directo (historia en los primeros 40 caracteres y como mucho 2 comandos)
1. `TORNEO 100.000 $ HOY · BRUJO EN DIRECTO 💥 !torneo`
2. `¿SOY EL MEJOR BRUJO DEL TORNEO? 💥 RONDA A RONDA · !torneo`
3. `WOW FOREVER GRATIS HOY A LAS 19:00 · OS ENSEÑO A EMPEZAR 💥 !gratis`
4. `RESERVAMOS NOMBRES EN WOW FOREVER 💥 !nombres !web`
5. `7 DÍAS PARA WOW FOREVER · PREPARO MI BRUJO 💥 !macros`
6. `ABRE WOW FOREVER A LAS 00:00 · MARATÓN DE LANZAMIENTO 💥 !web`
7. `DÍA 1 DE WOW FOREVER · DEL 1 AL 60 SIN PARAR 💥 !talentos`
8. `MIÉRCOLES DE DUELOS · RETA AL BRUJO 💥 !duelos !macros`
9. `PRIMERA MAZMORRA DE WOW FOREVER CON VOSOTROS 💥 !discord`
10. `BRUJO JcJ AL 60 · ¿EL MÁS FUERTE DE WOW FOREVER? 💥 !macros`

(`!duelos` y `!gratis` hay que crearlos; textos en el punto 8.5.)

### 8.2 Diez títulos de vídeo de YouTube (tipo frase o pregunta, nombre o tensión al principio, ≤70 caracteres)
1. `Así fue mi torneo de 100.000 $ con el Brujo 💥 The Forever Open`
2. `XOKAS vs MUCHAMIEL en el torneo de 100.000 $` (solo si cruzan)
3. `WoW Forever GRATIS el lunes: cómo entrar en la prueba de estrés`
4. `Qué clase jugar en WoW Forever (tier list de lanzamiento)`
5. `La mejor raza para cada clase en WoW Forever (versión final)`
6. `Las macros de Brujo que uso en WoW Forever (copiar y pegar)`
7. `Del 1 al 60 en WoW Forever: la ruta más rápida`
8. `10 errores que vas a cometer el primer día de WoW Forever`
9. `He probado las 9 mazmorras de WoW Forever: de peor a mejor`
10. `Brujo JcJ al 60 en WoW Forever: talentos, macros y addons`

Para las pruebas A/B: el mismo vídeo con una miniatura de 2 o 3 palabras («YA ES GRATIS», «MEJOR BRUJO», «DÍA 1») frente a la de dos bloques de ahora.

### 8.3 Plantilla de descripción de vídeo
```
👉 [Lo del vídeo, en la web]: https://muchamielwow.github.io/[pagina]/?ref=yt
Guías, macros, calculadora de talentos y addons de WoW Forever: https://muchamielwow.github.io/?ref=yt

¿QUIERES MESES DE WOW GRATIS? SORTEOS SOLO POR SUSCRIBIRTE → https://www.youtube.com/@muchamiel?sub_confirmation=1
[meta del sorteo: 1 año a los 90 K, otro año a los 100 K]

⏱️ CAPÍTULOS
00:00 [Introducción]
01:15 [Tema 1]
04:30 [Tema 2]
09:00 [Conclusión]

➡️ DIRECTOS TODOS LOS DÍAS DESDE LAS 17:30 (hora de España) · horario: https://muchamielwow.github.io/muchamiel/?ref=yt
TWITCH: https://www.twitch.tv/muchamiel
KICK: https://kick.com/muchamiel

➡️ COMUNIDAD (DISCORD): https://discord.gg/[el único elegido]

➡️ REDES
TIKTOK: https://www.tiktok.com/@muchamielwow
X: https://x.com/Muchamiel_
INSTAGRAM: https://www.instagram.com/muchamiel_/

🎁 CÓDIGOS: https://muchamielwow.github.io/colaboraciones/?ref=yt
[código del patrocinador del vídeo, si lo hay]

#WoWForever #WorldofWarcraft #wow
```
Nota: YouTube Studio deja guardar esto como descripción por defecto (Configuración › Valores de subida predeterminados). En los shorts, en lugar de enlaces, se usa el campo «vídeo relacionado».

### 8.4 Cinco guiones cortos de short/TikTok (25-45 s, vertical)

**1. «Mañana juego por 100.000 $»** (antes del torneo)
- 0-3 s, cara a cámara: «Mañana me juego 100.000 dólares con este Brujo.»
- 3-15 s, imagen del Brujo: «Duelos 1 contra 1 al nivel 30. Solo pasan 4 de cada clase a la final.»
- 15-25 s: «Y hay premio para el mejor Brujo del torneo.»
- 25-30 s: «Si queréis verlo, en directo desde la mañana. Sígueme para el resultado.»
- Texto en pantalla: «¿EL MEJOR BRUJO?» · Vídeo relacionado: el directo del torneo.

**2. «WoW Forever gratis hoy»** (19-10)
- 0-3 s: «WoW Forever es gratis HOY, sin suscripción.»
- 3-20 s, grabación de pantalla: «Battle.net → menú de versiones → "Forever Stress Test" → crear personaje.»
- 20-30 s: «A las 19:00 en España. Los personajes se borran, así que pruébalo sin miedo.»
- 30-35 s: «La guía para empezar, en el enlace.»
- Vídeo relacionado: «Qué clase jugar».

**3. «Duelo contra el campeón del mundo»** (después del torneo, con cada duelo)
- 0-2 s, texto: «x16 CAMPEÓN DEL MUNDO vs MI BRUJO».
- 2-25 s: el duelo con el sonido del juego, cortado al momento clave.
- 25-30 s, su reacción en cámara.
- Texto final: «¿Quién gana? Mira el final.» · Vídeo relacionado: el vídeo del torneo.

**4. «La macro que tienes que tener»** (serie de consejos, 1 por semana)
- 0-3 s: «Si juegas Brujo en WoW Forever y no tienes esta macro, pierdes duelos.»
- 3-20 s: enseña la macro en pantalla y qué hace.
- 20-30 s: «Las 37 macros del Brujo, para copiar y pegar, en el enlace del canal y con !macros en el directo.»
- Vídeo relacionado: «Las macros de Brujo que uso».

**5. «Abre WoW Forever»** (madrugada del 5-11)
- 0-3 s: la cola o la pantalla de carga a las 00:00: «Así ha abierto WoW Forever.»
- 3-20 s: lo primero que ve: zona inicial, gente, caos.
- 20-30 s: «Estoy en directo toda la noche subiendo el Brujo. ¿Qué clase has elegido?»
- Vídeo relacionado: el directo del lanzamiento.

### 8.5 Comandos del chat (Nightbot), listos para pegar

**Arreglar** (hay que sustituir `[DISCORD]` por la invitación elegida):
```
!redes   → YouTube: https://www.youtube.com/@muchamiel · TikTok: https://www.tiktok.com/@muchamielwow · X: https://x.com/Muchamiel_ · Instagram: https://www.instagram.com/muchamiel_/ · Discord: [DISCORD] · Web: https://muchamielwow.github.io/?ref=twitch
!discord → Entra en la comunidad: [DISCORD] (avisos de directo, grupos y sorteos)
!torneo  → The Forever Open (17-18 oct): duelos 1c1 al 30, 100.000 $. Mis duelos, normas y resultados: https://muchamielwow.github.io/torneo/?ref=twitch
!drops   → [poner la información real de los drops de WoW Forever, si los hay en el canal; si no, borrar el comando]
!server  → [reino de WoW Forever cuando se sepa; mientras tanto: «En WoW Forever ya no hay reinos como antes, todo en la web: https://muchamielwow.github.io/lanzamiento/?ref=twitch»]
```
**Nuevos:**
```
!web         → Guías, macros, calculadora de talentos y addons de WoW Forever: https://muchamielwow.github.io/?ref=twitch
!macros      → Las 37 macros de mi Brujo para copiar y pegar: https://muchamielwow.github.io/macros/warlock/?ref=twitch (y de las otras 8 clases en la web)
!talentos    → Calculadora de talentos de WoW Forever: https://muchamielwow.github.io/calculadora/?ref=twitch
!addons      → Mis addons de WoW Forever (vídeo + lista con enlaces): https://muchamielwow.github.io/addons/?ref=twitch
!razas       → Mejor raza para cada clase: https://muchamielwow.github.io/razas/?ref=twitch
!gratis      → WoW Forever gratis el lunes 19-10 a las 19:00 (prueba de estrés, sin suscripción): https://muchamielwow.github.io/beta-gratis/?ref=twitch
!nombres     → Reserva de nombres del 27-10 al 3-11 (solo con pack): https://muchamielwow.github.io/reserva-nombres/?ref=twitch
!lanzamiento → WoW Forever abre el 5-11 a las 00:00 (hora de España): https://muchamielwow.github.io/lanzamiento/?ref=twitch
!codigos     → Códigos de descuento de mis colaboraciones: https://muchamielwow.github.io/colaboraciones/?ref=twitch
!sorteo      → [texto actual del sorteo] · Bases y ganadores: https://muchamielwow.github.io/sorteos/?ref=twitch
!horario     → Directo todos los días desde las 17:30 en España (10:30 México, 11:30 Colombia, 13:30 Argentina desde el 26-10). Horario: https://www.twitch.tv/muchamiel/schedule
!duelos      → Miércoles de duelos: susúrrame en el juego con tu clase y nivel, y por orden de llegada en el chat.
!clip        → ¿Momentazo? Pulsa el botón de clip (Alt+X) y ponle título. El mejor de la semana sale en el canal.
```
**Temporizador de Nightbot** (cada 20 min con al menos 10 líneas de chat): alternar `!web`, `!macros`, `!discord` y `!horario`.
**Quitar del chat de Twitch:** `!kick` (que siga en el chat de Kick). Riesgo explicado en el punto 2.
**Borrar o revisar los viejos:** `!wa`, `!guia`, `!sod`, `!racelock`, `!hardcore`, `!retos`, `!ruleta` (si ya no se usa), `!guildtbc`, `!elune`, `!caga`. En StreamElements, `!redes` (lleva YouTube a Twitter); mejor dejar un solo bot de comandos.

### 8.6 Plantilla de horario (panel de Twitch, Discord, X y web)
```
🗓️ DIRECTOS DE MUCHAMIEL — WoW Forever
Todos los días · España 17:30 · México 10:30 · Colombia 11:30 · Argentina 13:30
(horario de invierno, desde el 26-10)

LUN  Novedades y parches
MAR  Subir nivel / mazmorras
MIÉ  ⚔️ DUELOS CON VOSOTROS
JUE  Directo + «Conoce a…» (cada 2 semanas)
VIE  🤝 Invitado
SÁB  Directo largo (mazmorras / JcJ)
DOM  Corto o descanso

📅 ESPECIALES
SÁB 17 y DOM 18-10 · Torneo The Forever Open (100.000 $)
LUN 19-10 · 19:00 · WoW Forever GRATIS (prueba de estrés)
MAR 27-10 · Reserva de nombres
MIÉ 4-11 · 22:00 · MARATÓN DE LANZAMIENTO (abre a las 00:00 del 5-11)

Twitch · YouTube · Kick — muchamielwow.github.io
```

---

## 9. Lo que no se ha podido mirar

- **TikTok:** la lista de vídeos, la frecuencia, las visitas por vídeo, los fijados y el enlace de la biografía. Solo se ven seguidores, me gusta, número de vídeos y la biografía.
- **X e Instagram:** nada actual sin sesión (se usan los datos del 09-10).
- **Estadísticas internas:** CTR, retención, tráfico por fuente y público por país en YouTube y Twitch. Solo las ve él.
- **Si sus shorts tienen ya un «vídeo relacionado»:** no sale en el HTML público.
- **El periodo exacto de las cifras de TwitchTracker:** la página no lo indica; StreamsCharts devolvió 403.
- **La página oficial de normas de emisión simultánea de Twitch** (help.twitch.tv da error). Lo citado viene de prensa (Esports.gg, HotHardware, Digital Music News, Restream) y hay versiones contradictorias sobre el chat combinado.
- **La hora de inicio de las rondas del torneo:** las normas no la dan.
- **Los ingresos y los suscriptores actuales de Twitch:** el 1.837 viene de nuestro STATS, sin fecha de fuente comprobada hoy.
- **Las miniaturas de Shorts y TikTok,** y los textos completos de los títulos de TikTok.
- **Pikaboo en YouTube:** se usó @pikabooirl, porque @Pikaboo es otro canal. Savix: c/Savixirl. Payo: por el id de canal de su panel de Twitch.

---

## 10. Fuentes

**Canales de Muchamiel (16-10-2026):**
- https://www.youtube.com/@muchamiel (/videos, /shorts, /streams, /playlists)
- https://www.youtube.com/watch?v=tfOKp7i8N1Y (descripción del vídeo largo del 15-10)
- https://www.youtube.com/watch?v=hUpXTYEp-JU (descripción del directo del 15-10)
- https://www.twitch.tv/muchamiel (paneles, título, emisiones guardadas y clips, consultados con la API pública de la web de Twitch)
- https://twitchtracker.com/muchamiel
- https://kick.com/muchamiel (API pública /api/v2/channels/muchamiel y /videos)
- https://www.tiktok.com/@muchamielwow
- https://discord.gg/eu3e3zm4fq · https://discord.gg/U8VkN5yXJ8 · https://discord.gg/QateSZqJU8 (API pública de invitaciones)
- Comandos: https://api.nightbot.tv/1/channels/t/muchamiel y la lista pública de comandos de StreamElements del canal muchamiel-f842c
- https://muchamielwow.github.io/ y https://muchamielwow.github.io/sitemap.xml

**Comparación:**
- https://www.twitch.tv/xaryu · https://www.youtube.com/@Xaryu
- https://www.twitch.tv/pikabooirl · https://www.youtube.com/@pikabooirl
- https://www.twitch.tv/payo · https://www.youtube.com/channel/UCQ-czOmPo1JYi1wKFi7wY8w
- https://www.twitch.tv/venruki · https://www.youtube.com/@venruki
- https://www.twitch.tv/savix · https://www.youtube.com/c/Savixirl
- https://www.twitch.tv/elxokas · https://www.youtube.com/@elxokas
- https://www.twitch.tv/directory/category/world-of-warcraft (streams en castellano: dulcegema_, zerstgaming, android_mercys…)

**Fechas de WoW Forever y torneo:**
- https://raiderio.com/events/the-forever-open/rules-regulations-code-of-conduct
- https://www.warcrafttavern.com/forever/guides/beta/
- https://www.playnews.gg/en/release-dates/world-of-warcraft-forever-launch-time-11-p-m-on-4-november-names-from-27-october
- https://blizzardwatch.com/2026/10/07/early-name-reservation-wow-forever/
- https://vandal.elespanol.com/noticia-amp/2026286021/xokas-expulsado-de-la-beta-de-world-of-warcraft-forever-el-streamer-fue-baneado-en-directo/
- research/prueba-estres-hora.md y research/forever-lanzamiento.md (con sus fuentes de Blizzard)

**Buenas prácticas:**
- Pruebas A/B de títulos y miniaturas (YouTube): https://support.google.com/youtube/answer/16391400
- Capítulos (YouTube): https://support.google.com/youtube/answer/9884579
- Doblaje automático (YouTube): https://support.google.com/youtube/answer/15569972
- Vídeo relacionado en Shorts y enlaces no clicables: https://www.searchenginejournal.com/youtube-adds-shorts-links-limits-links-elsewhere/495463 · https://www.socialmediatoday.com/news/youtube-previews-new-option-to-link-shorts-clips-to-longer-video-uploads/690603/ · https://vidiq.com/blog/post/youtube-related-links-connect-shorts-long-videos/
- Shorts a partir de vídeos propios («Editar como short»): https://9to5google.com/?p=516467 · https://lindseygamble.com/blog/youtube-gives-creators-the-ability-to-create-shorts-from-existing-long-form-videos
- Editor de clips verticales de Twitch: https://tubefilter.com/2023/05/12/twitch-tells-streamers-to-share-their-clips-on-youtube-shorts/ · https://streamlabs.com/content-hub/post/how-to-upload-twitch-clips-to-youtube-shorts/
- Emisión simultánea en Twitch (prensa; la página oficial no cargó): https://esports.gg/news/gaming/twitch-multiplatform-streaming-officially-allowed · https://hothardware.com/news/twitch-streamers-allowed-to-simulcast · https://www.digitalmusicnews.com/2023/10/22/twitch-now-allows-users-to-simulcast-on-any-platform-or-service/ · https://restream.io/blog/twitch-multistreaming-rules-explained.md
- Horario de Twitch: https://www.technipages.com/twitch-tv-how-to-configure-a-stream-schedule/ · https://www.streamscheme.com/stream-schedule-widget/
