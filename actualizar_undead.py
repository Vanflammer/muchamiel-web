from pathlib import Path
import re
root=Path(__file__).resolve().parent
p=root/'brujo-30-builds-y-macros.md';s=p.read_text(encoding='utf-8')
s=s.replace('Cliente en inglés. Preparado','Brujo Undead. Cliente en inglés. Preparado')
s=s.replace('Las 35 caben','Las 39 caben')
s=s.replace('Solo si tu personaje es Undead y tiene la racial aprendida.','Undead. Elimina Charm, Fear y Sleep: úsala cuando ya estés afectado, no como inmunidad preventiva. En Forever ya no concede inmunidad después, según el [resumen oficial de Blizzard](https://news.blizzard.com/en-us/article/24303313/world-of-warcraft-forever-deep-dive-panel-recap). No elimina por sí sola stuns, roots ni slows. Mantén este botón separado de Fear y de tu abalorio: así decides qué recurso gastar y no intentas consumir ambos a la vez. Verifica en la beta sus interacciones de enfriamiento con tu abalorio concreto.')
start=s.index('### R2 ·');end=s.index('La sintaxis de los paquetes comunes',start)
s=s[:start]+'''### R5 · Undead: Cannibalize sin reiniciar

Undead de cualquier clase con la racial aprendida. Recupera hasta 35% de vida y maná con el canal completo, según [Blizzard: raciales Forever](https://news.blizzard.com/en-us/article/24304075/create-the-hero-you-want-to-be-in-world-of-warcraft-forever). Necesita un cadáver válido próximo; no crea uno y un duelo normalmente termina sin matar al rival. Es una opción de recuperación cuando realmente hay un cadáver, no una curación garantizada durante cada duelo. Comprueba el uso permitido y la disponibilidad con la organización. El daño, el movimiento y otras acciones pueden cortar la canalización. Shift permite intentar una nueva canalización deliberadamente.

```text
#showtooltip Cannibalize
/cast [mod:shift][nochanneling] Cannibalize
```

Underwater Breathing y Touch of the Grave son pasivas: no necesitan ni admiten una macro que las active. No combines Cannibalize con Life Tap en el mismo botón: gastar vida o ejecutar otra acción puede interferir con la recuperación que querías hacer.

'''+s[end:]
extra='''### C18 · Todas las clases: parar tu acción

Botón de emergencia para detener tu lanzamiento o canalización y dejar de atacar con tu personaje. No retira la mascota: C1 hace eso. Útil si quieres detener tu daño antes de mantener un control; no elimina DoTs que ya hayas aplicado. No lo pulses por rutina.

```text
/stopcasting
/stopattack
```

### C19 · Todas las clases: elegir abalorio activo

Normal usa la ranura superior (13); Shift la inferior (14). Solo funciona si el objeto equipado tiene una habilidad de uso disponible y está permitido en el torneo. No asume que tengas un medallón ni que cualquier abalorio elimine control. Revisa qué llevas en cada ranura antes del duelo. Separa este botón de R1 para no gastar dos recursos por accidente.

```text
#showtooltip
/stopcasting
/use [mod:shift] 14; 13
```

### C20 · Todas las clases: venda sobre ti

Con First Aid suficiente y Heavy Silk Bandage en las bolsas. Mantiene tu objetivo enemigo y usa la venda sobre ti. Si utilizas otra venda, cambia el nombre por el nombre exacto en inglés de tu objeto y comprueba su requisito. Necesitas una ventana sin daño que corte la curación; no evita Recently Bandaged ni otras restricciones. Comprueba que el objeto está permitido en las reglas vigentes.

```text
#showtooltip Heavy Silk Bandage
/stopcasting
/use [@player] Heavy Silk Bandage
```

### C21 · Brujo con manáfago: limpiar a tu demonio

Alternativa a C12 que apunta expresamente a tu mascota para intentar disipar un efecto mágico disipable. Necesita Felhunter con Devour Magic y una situación válida para usarlo; no limpia cualquier control ni garantiza salvarlo. Evita tener que seleccionar al demonio y regresar al rival.

```text
#showtooltip Devour Magic
/cast [@pet,exists,nodead] Devour Magic
```

### C22 · Brujo: Drain Soul para fragmentos

Preparación fuera del duelo, sobre enemigos válidos para obtener fragmentos. Evita reiniciar tu canalización al repetir la tecla; Shift permite cambiarla deliberadamente. No fabrica fragmentos al pulsar: necesitas cumplir las condiciones de Drain Soul. En el torneo respeta la salida autorizada por el administrador; no es una rotación de duelo.

```text
#showtooltip Drain Soul
/cast [mod:shift,harm,nodead][nochanneling,harm,nodead] Drain Soul
```

### C23 · Brujo: piedra de salud de emergencia

Alternativa a C15 para quien prefiera un botón exclusivamente defensivo. Detiene tu lanzamiento e intenta usar Lesser Healthstone, que debes haber creado y llevar en las bolsas. No la crea ni supera sus restricciones. También sirve a otra clase que lleve esa piedra; cambia el nombre si llevas una piedra de otro rango.

```text
#showtooltip Lesser Healthstone
/stopcasting
/use Lesser Healthstone
```

'''
s=s.replace('### D1 · Soul Link',extra+'### D1 · Soul Link')
assert len(re.findall(r'```text',s))==39
for code in re.findall(r'```text\n(.*?)\n```',s,re.S):assert len(code)<=255
p.write_text(s,encoding='utf-8')
p=root/'crear_web.py';s=p.read_text(encoding='utf-8').replace('35','39')
s=s.replace('Nivel 30 · 26 puntos de talento · Cliente en inglés','Undead · Nivel 30 · 26 puntos de talento · Cliente en inglés')
s=s.replace('Comunes, talentos y raciales','Comunes, talentos y raciales Undead')
s=s.replace("'<nav id=", "'<nav id=")
s=s.replace("+intro+'<nav", "+intro+'<p class=\"start\"><strong>Su personaje es Undead:</strong> <a href=\"#R1\">Will of the Forsaken</a> y <a href=\"#R5\">Cannibalize</a>. Macros para cualquier clase: <a href=\"#C18\">parar acción</a>, <a href=\"#C19\">abalorios</a> y <a href=\"#C20\">venda sobre ti</a>.</p><nav")
p.write_text(s,encoding='utf-8')
p=root/'web'/'PARA-PEDRO.txt';s=p.read_text(encoding='utf-8').replace('35 macros','39 macros').replace('GUÍA BRUJO FOREVER','GUÍA BRUJO UNDEAD FOREVER')
p.write_text(s,encoding='utf-8')
print('Actualizada guía Undead: 39 macros; bloques <=255 caracteres.')
