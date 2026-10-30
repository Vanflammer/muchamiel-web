"""Van 30-10: notas de las macros del brujo sin las builds de la beta (B1-B13), sin nivel 30 ni duelos/torneo.
Cada par: (texto viejo, castellano nuevo, inglés nuevo). macros_portal lo aplica; guias_portal registra el inglés."""

def B(n):
    return f'<a href="../../warlock/#B{n}">B{n}</a>'

PARES = [
    ('Normal usa Lesser Healthstone, la piedra del rango disponible a nivel 30. Alt la crea.',
     'Normal usa Lesser Healthstone: cambia el nombre por el rango que tengas (a nivel 60, Major Healthstone). Alt la crea.',
     'Normal uses Lesser Healthstone: change the name to the rank you have (Major Healthstone at level 60). Alt creates it.'),
    ('Preparación fuera del duelo, sobre enemigos válidos para obtener fragmentos. Evita reiniciar tu canalización al repetir la tecla; Shift permite cambiarla deliberadamente. No fabrica fragmentos al pulsar: necesitas cumplir las condiciones de Drain Soul. En el torneo respeta la salida autorizada por el administrador; no es una rotación de duelo.',
     'Para hacer fragmentos fuera de combate, sobre enemigos que los den. Evita reiniciar tu canalización al repetir la tecla; Shift permite cambiarla a propósito. No fabrica fragmentos al pulsar: necesitas cumplir las condiciones de Drain Soul.',
     'For making shards out of combat, on enemies that give them. Avoids restarting your channel when you press it again; Shift lets you change it on purpose. Pressing it does not create shards: you must meet Drain Soul\'s conditions.'),
    (f'{B(1)}–{B(4)}. Aplícalo con el demonio activo y vuelve a aplicarlo después de reponer o cambiar de demonio.',
     'Con talentos de Demonología. Aplícalo con el demonio fuera y vuelve a aplicarlo después de invocarlo de nuevo o cambiar de demonio.',
     'With Demonology talents. Apply it with your demon out, and reapply after resummoning or changing demons.'),
    (f'{B(1)}–{B(5)}. Normal manáfago; Shift abisario; Ctrl súcubo. Requiere Master Summoner 2/2 y Fel Domination. Pulsa una vez; si Domination está en enfriamiento invoca con el tiempo normal.',
     'Con talentos de Demonología. Normal manáfago; Shift abisario; Ctrl súcubo. Requiere Master Summoner 2/2 y Fel Domination. Pulsa una vez; si Domination está en enfriamiento invoca con el tiempo normal.',
     'With Demonology talents. Normal: Felhunter; Shift: Voidwalker; Ctrl: Succubus. Requires Master Summoner 2/2 and Fel Domination. Press once; if Domination is on cooldown, summoning uses the normal cast time.'),
    (f'{B(1)}–{B(4)} aprovechan Demonic Brand. En {B(5)} es solo daño directo. Pulsa cuando puedas actuar; no fuerces la apertura.',
     'Con Demonic Brand (Demonología) aprovechas más; sin ese talento es solo daño directo. Pulsa cuando puedas actuar; no fuerces la apertura.',
     'With Demonic Brand (Demonology) you get more out of it; without that talent it is only direct damage. Press when you can act; do not force the opener.'),
    ('Solo funciona con Voidwalker. Requiere Alt para activarse. Sacrifica al demonio: pierdes la protección de Soul Link. Reserva para durante el duelo.',
     'Solo funciona con Voidwalker. Requiere Alt para activarse. Sacrifica al demonio: pierdes la protección de Soul Link. Guárdalo para cuando lo necesites de verdad.',
     'Only works with a Voidwalker. Requires Alt to activate. Sacrifices the demon: you lose Soul Link protection. Save it for when you really need it.'),
    (f'{B(6)}–{B(7)}. {B(13)} y {B(8)} no tienen este talento. Sustituye tu otra Curse, pero no Bane of Agony.',
     'Solo si tienes el talento (Aflicción). Sustituye tu otra Curse, pero no Bane of Agony.',
     'Only if you have the talent (Affliction). Replaces your other Curse, but not Bane of Agony.'),
    (f'Todas pueden lanzar Shadow Bolt; {B(6)}, {B(7)} y {B(13)} pueden aprovechar Nightfall. La macro no detecta el proc ni evita un lanzamiento normal.',
     'Todos los brujos pueden lanzar Shadow Bolt; con Nightfall (Aflicción) le sacas más. La macro no detecta el proc ni evita un lanzamiento normal.',
     'Every warlock can cast Shadow Bolt; with Nightfall (Affliction) you get more out of it. The macro neither detects the proc nor prevents a normal cast.'),
    (f'{B(6)}, {B(7)} y {B(13)}. No existe en tus otras distribuciones.',
     'Solo si tienes el talento (Aflicción).',
     'Only if you have the talent (Affliction).'),
    (f'{B(6)}–{B(7)}. Normal Agony; Shift intenta Amplify Curse primero. Si ambas habilidades comparten GCD en tu build, necesitarás otra pulsación.',
     'Con Amplify Curse (Aflicción). Normal Agony; Shift intenta Amplify Curse primero. Si las dos comparten el tiempo global, necesitarás otra pulsación.',
     'With Amplify Curse (Affliction). Normal: Agony; Shift attempts Amplify Curse first. If both share the global cooldown, you will need another press.'),
    (f'{B(8)}–{B(11)}. Cancela tu lanzamiento para rematar. Gestiona sus fragmentos; no lo uses automáticamente a cada enfriamiento.',
     'Con talentos de Destrucción. Cancela tu lanzamiento para rematar. Gestiona sus fragmentos; no lo uses automáticamente a cada enfriamiento.',
     'With Destruction talents. Cancels your cast to finish the target. Manage its shards; do not automatically use it on cooldown.'),
    (f'{B(9)}–{B(11)} lo combinan con Conflagrate. Mantengo las dos decisiones separadas.',
     'Con Conflagrate (Destrucción) se combinan; las dos decisiones van por separado.',
     'With Conflagrate (Destruction) they combine; the two decisions are kept separate.'),
    (f'{B(9)}–{B(11)}. A nivel 30 tus builds no tienen Shadow and Flame: Conflagrate consume Immolate. Decide cuándo gastar su daño periódico restante.',
     'Con talentos de Destrucción. Sin Shadow and Flame, Conflagrate consume Immolate: decide cuándo gastar su daño periódico restante. Con Shadow and Flame ya no lo gasta.',
     'With Destruction talents. Without Shadow and Flame, Conflagrate consumes Immolate: decide when to spend its remaining periodic damage. With Shadow and Flame it no longer uses it up.'),
    ('Solo si haces la variante de talentos descrita en la guía. Pon el ratón sobre la mascota enemiga y sigue dañando al jugador. No lo incluyo de serie en las builds de duelo.',
     'Solo si tienes el talento. Pon el ratón sobre la mascota enemiga y sigue dañando al jugador.',
     'Only if you have the talent. Mouse over the enemy pet and keep damaging the player.'),
    (f'{B(12)}, o uso deliberado en otras builds que lo aprendan. Solo durante el duelo. Imp da bonus de sombra; invocar otro demonio cancela el efecto con estos 26 puntos.',
     'Con Demonic Sacrifice (Demonología). Imp da bonus de sombra; invocar otro demonio después cancela el efecto.',
     'With Demonic Sacrifice (Demonology). Imp grants a Shadow bonus; summoning another demon afterwards cancels the effect.'),
]

EN = {es: en for _v, es, en in PARES}


def aplicar(s):
    for viejo, nuevo, _en in PARES:
        s = s.replace(viejo, nuevo)
    return s
