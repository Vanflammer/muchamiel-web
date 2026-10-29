from pathlib import Path
import re
root=Path(__file__).resolve().parent
p=root/'brujo-30-builds-y-macros.md';s=p.read_text(encoding='utf-8')
s=s.replace('Las 39 caben','Las 41 caben')
s=s.replace('Contra Warrior, Rogue y Druid respeta sus derechos de apertura;','En el torneo, contra Warrior, Rogue y Druid respeta sus derechos de apertura;')
newmacros='''### C24 · BG y mundo abierto: Fear bajo el ratón

Controla a un segundo enemigo sin cambiar tu objetivo de daño. Normal usa un enemigo vivo bajo el ratón; si no lo hay, intenta tu objetivo. Shift usa exclusivamente un foco enemigo vivo. Cancela tu lanzamiento actual: úsala cuando quieras priorizar el control. No detecta inmunidades, rendimientos decrecientes ni decide qué enemigo debes controlar. Complementa C3, no necesitas asignar las dos si una ya cubre tu forma de jugar.

```text
#showtooltip Fear
/stopcasting
/cast [mod:shift,@focus,harm,nodead][nomod,@mouseover,harm,nodead][nomod,harm,nodead] Fear
```

### C25 · BG y grupo: Devour defensivo al aliado

Con Felhunter y Devour Magic aprendida. Intenta disipar un efecto mágico a un aliado vivo bajo el ratón; si no hay uno válido, te apunta a ti. Puedes usar el marco de un compañero sin dejar de tener al enemigo seleccionado. Es una alternativa defensiva a C12: no purga enemigos. No elimina efectos de cualquier tipo ni funciona sin alcance, disponibilidad y objetivo válido. Gastarlo en un aliado puede dejarte sin ese recurso para ti durante su enfriamiento.

```text
#showtooltip Devour Magic
/cast [@mouseover,help,nodead][@player] Devour Magic
```

'''
s=s.replace('### D1 · Soul Link',newmacros+'### D1 · Soul Link')
section='''## BGs y PvP en mundo abierto

Esta guía también está pensada para jugar con otros enemigos y aliados alrededor. Mantiene el presupuesto de nivel 30 y 26 puntos: las decisiones siguientes son propuestas para practicar, no un ranking demostrado. Si subes de nivel o cambia tu presupuesto, hay que revisar talentos, rangos y habilidades; no añadas automáticamente las habilidades excluidas al 30.

Las reglas especiales de The Forever Open (build fija por fase, apertura, distancia inicial, salida por fragmentos y lista de objetos) se aplican a ese torneo. No las presentes como reglas generales de BGs o mundo abierto. Aquí respetas las reglas del juego y cualquier evento concreto en el que participes. Las restricciones normales de los hechizos y objetos siguen vigentes.

| Situación | Build que probaría | Plan y macros |
|---|---|---|
| Mundo abierto solo; sobrevivir a encuentros imprevistos | B1, comparada con B2 | Proteger demonio y Soul Link; C1, D1 y D2. C3 o C24 para controlar mientras te recolocas. B1 ofrece Corruption instantánea; B2 exige más tiempo de lanzamiento. |
| BG; desgaste y presión sobre varios enemigos | B6, o B7 si prefieres su inversión en aguante | C5, C6 y A3 permiten aplicar daño con mouseover sin cambiar el objetivo. Elige a quién controlar antes de repartir DoTs; no marques con daño al objetivo que vuestro equipo quiere mantener controlado. |
| BG o grupo; sobrevivir y apoyar con el demonio | B1 | Usa Felhunter para practicar C25 sobre un aliado y C12 para purgar o limpiarte. Conserva C1 para sacarlo de presión. Soul Link exige cuidar tu propia posición y la del demonio. |
| Grupo con compañeros que crean ventanas de lanzamiento | B9; compara B10 según tus pruebas | Concentrar daño con Immolate, Conflagrate y Shadowburn cuando haya una oportunidad. C24 puede controlar a un segundo enemigo. No copies el plan de burst si tu posición te impide terminar lanzamientos. |

**Con varios objetivos:** fija como foco al enemigo que quieres controlar con C4. Comprueba el foco antes de pulsar Shift. Mouseover puede ser el personaje o un marco válido; si no hay uno, revisa qué alternativa usa cada macro. No repartas daño por inercia: ayuda al objetivo que vuestro grupo quiere eliminar y protege al compañero bajo presión.

**Con compañeros:** C25 está dedicado a disipar aliados o a ti mismo. C12 permite también purgar enemigos y C21 intenta limpiar tu demonio. Los tres gastan la misma habilidad de la mascota: la macro no crea usos ni enfriamientos independientes. Elegir quién recibe Devour es una decisión de juego, no una automatización.

**Control y supervivencia:** C3/C24, C13 y C14 ofrecen destinatarios distintos según lo que quieras controlar. Seduction necesita especial cuidado con los DoTs y el daño de la mascota. C18 detiene la acción de tu personaje y C1 retira el demonio, pero ninguna borra el daño periódico que ya aplicaste. C20 sirve para una ventana de venda y C23 para la piedra: el daño recibido y las restricciones del objeto siguen contando.

**Undead en mundo abierto:** R1 rompe Charm, Fear o Sleep cuando haga falta; no protege frente al siguiente control. R5 puede servir después de una pelea con un cadáver válido y una posición segura. No confundas Cannibalize con una curación instantánea: canalizar te obliga a valorar el riesgo de otra pelea. Las pasivas funcionan sin botón.

**Entre peleas:** prepara fragmentos con C22 cuando corresponda, crea tu piedra con C15, repón demonio y armadura y comprueba tus grimorios. Life Tap ayuda a gestionar maná, pero debes decidir cuánta vida puedes gastar antes de exponerte de nuevo. Drain Life y Drain Mana no sustituyen moverte a una posición segura.

**Primeros botones para aprender:** C1/C2, C3 o C24, C4, C5/C6, C12 o C25 con manáfago, C20/C23 y R1. Añade las herramientas de tu build después. No hace falta aprender 41 botones a la vez: varios bloques son alternativas para la misma acción o dependen de talentos y objetos que quizá no uses.

'''
s=s.replace('## Equipo: empezar a prepararlo para duelos',section+'## Equipo: empezar a prepararlo para duelos')
assert len(re.findall(r'```text',s))==41
for c in re.findall(r'```text\n(.*?)\n```',s,re.S):assert len(c)<=255
p.write_text(s,encoding='utf-8')
p=root/'crear_web.py';s=p.read_text(encoding='utf-8').replace('39','41')
s=s.replace("'Demonio según rival','Equipo", "'Demonio según rival','BGs y mundo abierto','Equipo")
s=s.replace("'demonios','equipo'", "'demonios','pvp','equipo'")
s=s.replace("'Control y supervivencia','Listas", "'Control y supervivencia','Builds, aliados y varios enemigos','Listas")
s=s.replace('10 · Fuentes','11 · Fuentes').replace('Tu guía de duelos.','Duelos, BGs y mundo abierto.').replace('En un duelo, cada cambio','En PvP, cada cambio')
s=s.replace('Builds y macros de duelos','Builds y macros PvP').replace('reglas de The Forever Open. Consulta','consejos para duelos, BGs y mundo abierto. Consulta')
s=s.replace("parts=re.split(r'^## ',text,flags=re.M)[1:]", "parts=re.split(r'^## ',text,flags=re.M)[1:]")
s=s.replace('sections=[]','assert len(parts)==len(ids)==len(labels)==len(counts)\nsections=[]')
p.write_text(s,encoding='utf-8')
p=root/'web'/'PARA-PEDRO.txt';s=p.read_text(encoding='utf-8').replace('39 macros','41 macros').replace('reglas del torneo, demonios','duelos, BGs, mundo abierto, reglas del torneo, demonios');p.write_text(s,encoding='utf-8')
print('Actualizado PvP: 41 macros, nueva sección BGs y mundo abierto.')
