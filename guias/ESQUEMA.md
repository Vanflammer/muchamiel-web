# Formato de las guías (clases y profesiones)

Cada guía es un JSON en UTF-8 que lee `guias_portal.py` para pintar la página en castellano y en inglés con la misma estructura.
Todo texto visible va como `{"es": "...", "en": "..."}`. Los nombres de habilidades, talentos, objetos y recetas van en INGLÉS (el cliente
de Forever está en inglés) dentro del texto en los dos idiomas. Se puede usar `<b>` y `<i>` dentro de los textos, nada más de HTML.

## Reglas de contenido (obligatorias)
- Solo datos de WoW Forever comprobados: notas de Blizzard (`research/notas-beta/*.txt`, news.blizzard.com, foros), `research/talents.json`
  (talentos, libros de hechizos y habilidades por nivel sacados del cliente de la beta) y webs de guías (Icy Veins, Wowhead, Method,
  Warcraft Tavern, Mobalytics, wow.gg, Warcraft Wiki). Si dos fuentes no coinciden, manda Blizzard o el cliente; si no hay forma de saberlo, va a `pendiente`.
- Lo que solo se sabe de WoW Classic (1.12) y Forever no ha cambiado, se puede usar, pero si Forever lo ha tocado (habilidades nuevas,
  niveles distintos, talentos rehechos) manda Forever. Ante la duda, `pendiente`. NO inventar nunca cifras, niveles ni nombres.
- Con palabras propias: ninguna frase copiada de otra web. Sin nombres de youtubers ni creadores en el texto; las webs van en `fuentes`.
- Castellano neutro para España y Latinoamérica: nada de «coger» (usa «elegir», «recoger», «aprender», «tomar»).
- El inglés, natural (no traducción palabra por palabra).
- Tono: claro y directo, para alguien que empieza el día 4 de noviembre. Frases cortas.

## Clase: `guias/clases/<slug>.json`
```json
{
  "slug": "hunter",
  "actualizado": "2026-10-30",
  "resumen": {"es": "2-4 frases: qué es la clase en Forever y para quién es.", "en": "..."},
  "fuertes": [{"es": "...", "en": "..."}],
  "debiles": [{"es": "...", "en": "..."}],
  "ramas": [
    {"nombre": "Beast Mastery", "rol": {"es": "DPS a distancia", "en": "Ranged DPS"},
     "mejor_para": {"es": "Subir de nivel y jugar solo", "en": "Leveling and solo play"},
     "texto": {"es": "2-3 frases.", "en": "..."}}
  ],
  "razas": [{"raza": {"es": "Enano", "en": "Dwarf"}, "faccion": "Alianza", "por_que": {"es": "...", "en": "..."}}],
  "subir": {
    "rama": "Beast Mastery",
    "intro": {"es": "Por qué esta rama para subir y cómo se juega.", "en": "..."},
    "talentos": [{"niveles": "10-14", "puntos": "5/5 Improved Aspect of the Hawk", "nota": {"es": "...", "en": "..."}}],
    "habilidades": [{"nivel": 10, "nombre": "Tame Beast", "nuevo": false, "texto": {"es": "Para qué sirve, una frase.", "en": "..."}}],
    "rotacion": [{"es": "Paso o prioridad 1", "en": "..."}],
    "extra": {"titulo": {"es": "Mascotas que conviene domar", "en": "Pets worth taming"}, "items": [{"es": "...", "en": "..."}]},
    "consejos": [{"es": "...", "en": "..."}],
    "hitos": [{"nivel": "20", "texto": {"es": "Qué cambia a ese nivel", "en": "..."}}]
  },
  "nivel60": {
    "intro": {"es": "Qué se sabe del nivel 60 y qué no.", "en": "..."},
    "ramas": [
      {"nombre": "Marksmanship", "rol": {"es": "DPS a distancia", "en": "Ranged DPS"},
       "estadisticas": [{"es": "Agility hasta X / después Y", "en": "..."}],
       "rotacion": [{"es": "...", "en": "..."}],
       "consumibles": [{"es": "...", "en": "..."}]}
    ],
    "equipo": {"es": "Qué equipo buscar (si no hay datos de Forever, dilo y explica qué estadística priorizar).", "en": "..."}
  },
  "pvp": [{"es": "Consejos de JcJ a nivel 60 (5-8): qué hace la clase en duelos y campos de batalla.", "en": "..."}],
  "profesiones": [{"nombre": {"es": "Ingeniería", "en": "Engineering"}, "por_que": {"es": "...", "en": "..."}}],
  "pendiente": [{"es": "Lo que aún no se sabe y actualizaremos (ej.: equipo de banda de Forever).", "en": "..."}],
  "fuentes": [{"nombre": "Notas de la beta de Blizzard", "url": "https://..."}]
}
```
Tamaños orientativos: `habilidades` 15-30 entradas (las clave del 1 al 60, todas las nuevas de Forever marcadas con `"nuevo": true`);
`talentos` 8-14 tramos que sumen 51 puntos (10→60); `rotacion` 4-8; `consejos` 5-10; `hitos` 5-10; `ramas` 3 (y druida 4 si separas oso/felino);
`razas` 2-4 por facción si aplica; `pvp` 5-8; `profesiones` 2-4; `pendiente` 2-6.

## Profesión: `guias/profesiones/<slug>.json`
```json
{
  "slug": "alchemy",
  "nombre": {"es": "Alquimia", "en": "Alchemy"},
  "tipo": "fabricacion",
  "actualizado": "2026-10-30",
  "resumen": {"es": "Qué hace y para quién es.", "en": "..."},
  "pareja": {"es": "Con qué recolección va (Herbalism).", "en": "..."},
  "forever": [{"es": "Lo que cambia o es nuevo en Forever.", "en": "..."}],
  "tramos": [{"desde": 1, "hasta": 60, "receta": "Minor Healing Potion", "cuantas": "unas 60",
              "materiales": {"es": "1 Peacebloom, 1 Silverleaf, 1 Empty Vial", "en": "..."},
              "nota": {"es": "Dónde aprender o dónde están los materiales.", "en": "..."}}],
  "entrenadores": [{"es": "Aprendiz 1-75, Oficial 50-150, Experto 125-225 (nivel 20), Artesano 200-300 (nivel 35): dónde está cada uno.", "en": "..."}],
  "lo_mejor": [{"es": "Recetas u objetos que más valen (para ti o para vender).", "en": "..."}],
  "consejos": [{"es": "...", "en": "..."}],
  "pendiente": [{"es": "...", "en": "..."}],
  "fuentes": [{"nombre": "...", "url": "https://..."}]
}
```
`tipo`: `recoleccion`, `fabricacion` o `secundaria`. En recolección, `tramos` son zonas/nodos por nivel de habilidad (`receta` = qué recoger,
`materiales` = dónde). Si Forever cambia el tope o los rangos, manda Forever (y si no se sabe, `pendiente`).

Antes de terminar: `python -c "import json;json.load(open('RUTA',encoding='utf-8'))"` tiene que pasar.

## Clase: apartado «Cómo se juega» (`"tecnicas"`, añadido el 30-10)
Lo que no dicen los talentos: cómo se juega con las manos. Cada técnica con su **nombre técnico en inglés** (el que usan los jugadores
expertos y las guías: kiting, strafing, swing timer, stutter-step, jump-turn / jump shot, line of sight (LoS), pillar humping, juke,
interrupt, CC chain, diminishing returns, spell pushback, dead zone, pet control, threat, positioning…) y explicada en castellano con
los botones y habilidades concretas de la clase en Forever (nombres de habilidad en inglés). Solo lo que funciona en Forever
(si una mecánica depende de algo que Forever cambió, dilo; si no se sabe, no la pongas).
```json
"tecnicas": {
  "pvp": [{"termino": "Hamstring kiting / stutter-step", "titulo": {"es": "Pegar y salir con el arma lenta", "en": "Hit and step out with a slow weapon"},
           "texto": {"es": "Cómo se hace, paso a paso, y cuándo sirve (3-6 frases).", "en": "..."}}],
  "pve": [{"termino": "Positioning", "titulo": {"es": "...", "en": "..."}, "texto": {"es": "...", "en": "..."}}],
  "teclas": [{"es": "Consejo de teclas o macros para hacerlo cómodo (ej.: girar con el ratón, no con el teclado).", "en": "..."}]
}
```
5-8 en `pvp`, 4-6 en `pve`, 3-5 en `teclas`. Más detalle que una lista: que alguien que no sabe lo pueda hacer leyendo.

## Glosario general: `guias/tecnicas.json`
```json
{"actualizado": "2026-10-30", "intro": {"es": "...", "en": "..."},
 "grupos": [{"titulo": {"es": "Moverse (kiting)", "en": "Movement (kiting)"},
             "items": [{"termino": "Strafe kiting", "alias": {"es": "Correr de lado", "en": "Strafing"},
                        "texto": {"es": "Qué es, cómo se hace (teclas), para qué clases.", "en": "..."}, "clases": ["mage", "hunter"]}]}],
 "fuentes": [{"nombre": "...", "url": "https://..."}]}
```
