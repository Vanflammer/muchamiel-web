# Traducción al inglés de la guía WoW Forever

`en.json` es un objeto JSON: cada clave es un texto de la web en castellano y su valor es la traducción al inglés.
Un valor vacío significa que falta traducirlo; mientras falte, la web en inglés muestra ese texto en castellano.
La versión en inglés (`/en/`) solo se publica cuando está traducido al menos el 50 %.

## Reglas para quien traduzca

1. **No cambies las claves** ni añadas o quites entradas. Solo rellena los valores. Mantén el orden.
2. **Respeta el HTML** que haya dentro del texto: etiquetas, `href`, `class`, `id`, `src`, `target` y `rel` se copian tal cual. Traduce solo el texto visible y los atributos `title`/`alt`.
3. **No traduzcas** lo que ya está en inglés porque es del juego (el cliente de la beta está en inglés): nombres de hechizos, talentos, objetos, macros (`/cast …`), `Shift`, `Alt`, `Ctrl`, nombres propios (Muchamiel, Twitch, The Forever Open…). En esos casos copia el texto igual.
4. Clases y razas en el inglés del juego: Guerrero → Warrior, Paladín → Paladin, Cazador → Hunter, Pícaro → Rogue, Sacerdote → Priest, Chamán → Shaman, Mago → Mage, Brujo → Warlock, Druida → Druid; Humano → Human, Enano → Dwarf, Elfo de la noche → Night Elf, Gnomo → Gnome, Orco → Orc, No-muerto → Undead, Trol → Troll. Alianza → Alliance, Horda → Horde.
5. Si el texto es «Nombre <small class="en">Name</small>», tradúcelo solo como «Name» (sin la etiqueta small).
6. Cifras al estilo inglés: «100.000 $» → «$100,000»; «79,1 K» → «79.1K»; fechas «8 oct 2026» → «Oct 8, 2026».
7. Tono: el mismo, cercano y gamer, con humor. Adapta los juegos de palabras en vez de traducirlos literalmente.
8. Conserva los espacios del principio y del final (hay textos como `" de "` o `"Clase: "` que se juntan con otros).
9. Guarda en UTF-8 y comprueba que el JSON es válido.
