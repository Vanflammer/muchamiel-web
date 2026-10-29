"""Página «Cambios de la beta» (Van, 15-10-2026): los cambios de cada parche de la beta de WoW Forever por clase, en castellano,
sacados de las notas oficiales de Blizzard (foro «WoW Forever Beta Development Notes»). Al publicar Blizzard un parche nuevo,
se añade arriba en PARCHES. ▲ = mejora, ▼ = nerf, ● = cambio o arreglo. Hechizos y talentos con su nombre del cliente (inglés)."""
import html

E = html.escape
NOTAS = 'https://us.forums.blizzard.com/en/wow/t/wow-forever-beta-development-notes-%E2%80%93-updated-october-8/2360696'
FORO = 'https://us.forums.blizzard.com/en/wow/'

# (fecha, título, resumen, [(texto general)], {clase: [(signo, texto)]})
import iconos_clase
import notas_blizzard
import parche_15oct  # notas del 15-10 (publicadas el 16-10), con su inglés
import parche_26oct  # Van 26-10: repaso final de raciales
PARCHES = [
    parche_26oct.parche(),
    parche_15oct.parche(),
    ('13 y 14 de octubre', 'Economía y mantenimiento', 'Sin cambios de clases. Blizzard estrena las retenciones contra la compra de oro y hace un mantenimiento para pruebas internas.',
     [('●', 'Retenciones económicas temporales: si tu cuenta parece implicada en compraventa de oro por dinero real, se te bloquea un tiempo el comercio, el correo, el banco de hermandad y la subasta mientras lo investigan. Si no hay nada, se quita solo y no deja marca.'),
      ('●', 'Mantenimiento de un par de horas el 14 de octubre para pruebas internas, sin notas de cambios.')], {}),
    ('8 de octubre', 'Más ira, más experiencia y Dalaran', 'Guerreros y druidas ganan más ira al recibir daño, sube la experiencia en mazmorras y llega la Ciudad de Dalaran. Nerfs a las auras y escudos que escalaban de más.',
     [('▲', 'Nueva mazmorra para probar: la Ciudad de Dalaran.'),
      ('▲', 'Experiencia por matar en mazmorras +20 %. Arreglada la penalización de grupo: ahora, como en Classic, cuenta solo tu nivel y no el del más alto del grupo.'),
      ('●', 'Vuelve el botín de Classic: se puede interactuar con criaturas que no soltaron nada. Se pueden cambiar varias armas en el mismo tiempo global (macros de 2 manos a espada y escudo).'),
      ('●', 'El gestor de reutilizaciones admite ya todas las clases, raciales y abalorios.')],
     {'Guerrero y Druida': [('▲', 'Arreglados varios fallos de la ira al recibir daño: un guerrero o druida normal gana más ira. Se recalcula pensando en guerreros que suben de nivel (20-40 % de armadura) y no solo en tanques.')],
      'Druida': [('▲', 'Oso: 100 % más de ira en críticos (era 75 %) y amenaza +50 % (era +30 %).'),
                 ('▼', 'Thorns vuelve al daño de Vanilla y su coeficiente con poder con hechizos baja al 6 % (era 13,3 %).'),
                 ('●', 'Predatory Instincts pasa a llamarse Natural Instinct y además aumenta la sanación con hechizos según el intelecto. Shifting Power no se puede usar con la energía llena.'),
                 ('●', 'Arreglado: ya puede usar pociones de maná en forma de oso o felino, y la forma felina no reduce la vida máxima.')],
      'Cazador': [('▲', 'Disengage reduce el doble de amenaza, como estaba previsto. Unleashed Fury ya aumenta el daño de la mascota.'),
                  ('▲', 'Supervivencia: Expose Prey dura 10 s (eran 5). Arreglada la probabilidad de Improved Wing Clip e Improved Concussive Shot.'),
                  ('▼', 'Entrapment ya tiene rendimientos decrecientes y solo salta al activarse la trampa, no cada tic.')],
      'Mago': [('▼', 'Impact ya no salta con el daño periódico de Flamestrike.'),
               ('●', 'Frostbolt, Fireball y Arcane Missiles: rangos bajos ajustados para que cada rango nuevo sea siempre mejor.')],
      'Paladín': [('▼', 'Retribution Aura vuelve al daño de Vanilla (un 33 % menos) y su coeficiente baja al 6 % (era 13,3 %). Además usaba por error el poder con hechizos del objetivo.'),
                  ('▼', 'Protección: Reckoning pasa a tener 1,5 s de reutilización interna. Seal of Fury ya no devuelve maná sin el talento Improved Seal of Fury, y la recuperación de maná ya no genera amenaza.')],
      'Sacerdote': [('▼', 'Disciplina: Penance hace menos daño y sanación (contaba como canalización de 3 s y es de 2). El rango 1 cuesta un 50 % más de maná.'),
                    ('▲', 'Penance cura más en los rangos 2 y 4. Smite, Lesser Heal y Heal: rangos bajos ajustados.')],
      'Chamán': [('●', 'Flametongue Totem usa la velocidad de ataque correcta con objetivos cambiaformas. Elemental Focus ya no se gasta con Fire Nova. Lightning Bolt: rangos bajos ajustados.')],
      'Brujo': [('●', 'Tu demonio actual queda aturdido mientras invocas otro. Demonic Brand solo genera mucha amenaza con daño de sombras. Shadow Bolt: rangos bajos ajustados.')],
      'Guerrero': [('▼', 'Armas: Deep Wounds ya no escala con el poder de ataque de la mano izquierda (era un fallo). Vuelve a ser obligatorio para llegar a Impale.'),
                   ('▲', 'Demoralizing Shout genera amenaza. Arreglada la vida que da Last Stand.')]}),
    ('1 de octubre', 'Nivel 30 y gran repaso al guerrero', 'Sube el tope al nivel 30, llega la Excavación de los Humedales y el guerrero Furia se rehace casi entero. Menos experiencia de las misiones de mazmorra.',
     [('▲', 'Nivel máximo 30. Nueva mazmorra: Excavación de Whelgar (Humedales). Abren Zahúrda Rajacieno y Uldaman.'),
      ('▼', 'Las misiones de mazmorra dan un 50 % menos de experiencia extra.'),
      ('▼', 'JcJ: el equipo y las fichas de mejora cuestan un 50 % más de honor; el tope de honor sube de 15.000 a 25.000.'),
      ('●', 'Gnomo: Eureka! ya no afecta a efectos periódicos. Las hogueras ya no hacen daño a personajes de menos de nivel 5.')],
     {'Druida': [('▲', 'Oso: 75 % más de ira en críticos. Swipe escala con el poder de ataque. Inmunes a desarmes en cualquier forma.'),
                 ('▼', 'Se elimina Tiger\'s Fury y el talento King of the Jungle.'),
                 ('▲', 'Feral: nuevo talento Shifting Power (convierte maná en 40 de energía, 16 s) e Improved Shifting Power. Primal Bite genera el doble de amenaza.')],
      'Cazador': [('▲', 'Puntería: Sniper Shot llega a 45 m y aumenta el alcance de tus 3 siguientes disparos. Vuelve el modo agresivo de la mascota.'),
                  ('▼', 'Supervivencia: Deflection da 1-5 % de parada (era 2-10 %).')],
      'Mago': [('▼', 'Fuego: Combustion vuelve a 3 cargas (eran 4). Hot Streak pasa a llamarse Heating Up. Los pergaminos de Comprensión no se pueden lanzar en movimiento.')],
      'Paladín': [('▼', 'Protección: Redoubt da 4-20 % de bloqueo (era 6-30 %).'), ('▲', 'Holy Shield sube al 30 % de bloqueo (era 20 %).'),
                  ('▼', 'Reprensión: Champion of the Light convierte un 20/40/60 % del intelecto en daño con hechizos (era 33/66/100 %).')],
      'Sacerdote': [('▲', 'Devouring Plague ya puede ser crítico. Shadow Weaving ya no falla.'),
                    ('▼', 'Disciplina: Inner Focus ya no aumenta el crítico de los efectos periódicos. Shadow Word: Death ya no aprovechaba siempre Early Demise.')],
      'Pícaro': [('●', 'Si Expose Armor falla ya no pierdes los puntos de combo. Sutileza: Setup solo da puntos de combo sobre quien te esquivó o resistió.')],
      'Chamán': [('●', 'Arreglados Totemic Recall (ya devuelve maná) y la duración de Disease Cleansing Totem.')],
      'Brujo': [('▲', 'Hellfire puede ser crítico. Aflicción: Soul Harvest da de verdad su 50/100 % de regeneración de maná. Vuelve el modo agresivo de los demonios.'),
                ('●', 'Drain Soul se interrumpe al lanzar otro hechizo.')],
      'Guerrero': [('▲', '100 % más de ira con los críticos de ataques básicos. Rend y Sunder Armor «marcan» al enemigo al instante.'),
                   ('▲', 'Furia rehecho: talentos nuevos (Lingering Rage, Furious Precision, Gore Drinker), Bloodthirst escala más (45 % del poder de ataque, era 35 %), Whirlwind golpea siempre con las dos armas y Flurry ya no pide Enrage.'),
                   ('▼', 'Dual Wield Specialization ya no da golpe ni más ira a la mano izquierda. Se eliminan Improved Cleave y Boundless Rage. Unbridled Wrath ya no da el doble con armas de 2 manos.'),
                   ('●', 'Protección: Iron Will, Improved Bloodrage y Improved Disarm suben de fila para usarlo como especialización secundaria de JcJ. Se elimina Toughness. Armas: Spearing Strike ya no pide arma de 2 manos.')]}),
    ('24 de septiembre', 'Primer gran ajuste de clases', 'Primeros ajustes de la beta: muchas curas que no podían ser críticas ya lo son, y retoques a paladín, cazador y chamán.',
     [('▲', 'Reespecializar talentos cuesta 1 de plata si no has cambiado hace poco (solo en la beta).'),
      ('●', 'Ya puedes recibir los beneficios de la hoguera sentado, en una silla, tumbado o arrodillado, y lanzar hechizos o fabricar mientras esperas.')],
     {'Druida': [('▲', 'Rejuvenation, Tranquility y Wild Growth pueden ser críticos. Wrath hace un 50 % más de daño base. Thorns escala con el poder con hechizos.'),
                 ('●', 'Mangle pasa a llamarse Primal Bite.')],
      'Cazador': [('▼', 'Mascotas: Furious Howl da un 40 % menos de poder de ataque. Tame Beast ya no funciona con bestias de más nivel que tú.'),
                  ('▲', 'Supervivencia: Lacerating Strikes puede ser crítico. Strider Kick da +30 % de velocidad 3 s.')],
      'Mago': [('▲', 'Fuego: Wake of Fire dura 30 s (eran 20) y Hot Streak 20 s (eran 15). Arcane Missiles solo comprueba la línea de visión al empezar.'),
               ('▼', 'Ignite ya no duplica los aumentos de daño.')],
      'Paladín': [('▲', 'Holy Strike hace más daño en todos los rangos y en Sagrado tiene 10 s de reutilización (eran 12). Holy Power aumenta un 15 % su crítico.'),
                  ('▼', 'Righteous Fury: la amenaza sagrada baja al 60 % (era 90 %). Reprensión: Vengeance acumula 3 (eran 5) y Two-Handed Weapon Specialization da 2/4/6 % (era 3/6/9 %).'),
                  ('▲', 'Sacred Arbiter aumenta Holy Strike un 20 % (era 10 %). Twist of Light abarata un 20 % los sellos.')],
      'Sacerdote': [('▲', 'Renew puede ser crítico. Power Word: Shield puede sustituir a otro escudo si el objetivo no tiene Weakened Soul.'),
                    ('●', 'No-muerto: Dark Sacrifice ya no rompe controles. Gnomo: Contingency Plan puede ser crítico.')],
      'Chamán': [('▼', 'Flametongue Totem ya no se suma con Flametongue Weapon ni con Windfury Totem, y Tranquil Air, Windfury y Grace of Air ya no se suman entre sí aunque los pongan chamanes distintos.'),
                 ('▲', 'Elemental: Lava Burst hace un 10 % más en sus primeros rangos y Elemental Fury sube de fila. Restauración: Riptide puede ser crítico.'),
                 ('▼', 'Mejora: Rage of the Far Seer ya no da velocidad de lanzamiento.')],
      'Brujo': [('▲', 'Voidwalker Sacrifice escala con el 10 % de tu sanación con hechizos.')],
      'Guerrero': [('▲', 'Armas: Bloodthrill salta el doble (4-20 %). Protección: Focused Rage llega antes (cambia de fila con Bastion).'),
                   ('▼', 'Slam pasa a 18 s de reutilización (eran 15); Improved Slam la reduce 1,5/3 s.')]}),
]

SIGNO = {'▲': ('up', 'Mejora'), '▼': ('down', 'Nerf'), '●': ('fix', 'Cambio')}


def li(signo, texto, pre=''):
    cls, tit = SIGNO[signo]
    return f'<li class="{cls}"><span class="sig" title="{tit}">{signo}</span>{pre}{E(texto)}</li>'


# Van 16-10: en cada clase, juntas las mejoras, luego los nerfs y luego los cambios y arreglos (antes iban mezclados).
GRUPOS = [('▲', 'up', 'Mejoras'), ('▼', 'down', 'Nerfs'), ('●', 'fix', 'Cambios y arreglos')]


def agrupados(items, pre=lambda t: ''):
    out = ''
    for signo, cls, nombre in GRUPOS:
        sub = [t for s, t in items if s == signo]
        if sub:
            out += f'<p class="grupo {cls}"><i></i>{nombre}</p><ul class="cambios-lista">' + ''.join(li(signo, t, pre(t)) for t in sub) + '</ul>'
    return out


def cambios(nav_forever):
    out = ''
    for n, (fecha, titulo, resumen, general, clases) in enumerate(PARCHES):
        post = {f: p for p, f in notas_blizzard.POSTS.items()}.get(fecha)  # Van 16-10: notas completas, traducidas
        # Van 16-10: dejar claro que esto es un resumen y llevar de un clic a las notas completas de Blizzard.
        aviso = (f'<p class="es-resumen">Esto es un <b>resumen</b>. Más abajo tienes las <a href="#completas-{post}" data-abre>notas completas de Blizzard</a>, '
                 'traducidas línea a línea.</p>' if post else '')
        bloque = (f'<p class="eyebrow">{E(fecha.upper())}</p><h3>{E(titulo)}</h3><p>{E(resumen)}</p>' + aviso
                  + agrupados(general))
        if clases:
            bloque += '<div class="cambios-clases">' + ''.join(
                f'<div class="cc"><h4>{iconos_clase.con_icono(c, E)}</h4>' + agrupados(items, iconos_clase.icono_raza if c == 'Razas' else (lambda t: '')) + '</div>' for c, items in clases.items()) + '</div>'
        if post:
            bloque += notas_blizzard.bloque(post, f'{NOTAS}/{post}')
        out += f'<details class="parche"{" open" if n < 2 else ""}><summary><b>{E(fecha)}</b> · {E(titulo)}</summary><div class="parche-body">{bloque}</div></details>'
    return ('<p class="eyebrow">WOW FOREVER · BETA</p><h1>Cambios de la beta</h1>'
            '<p class="lead">Lo que Blizzard va cambiando en cada parche de la beta de WoW Forever, por clase y en castellano: '
            '<span class="sig-l up"><i></i>mejoras</span>, <span class="sig-l down"><i></i>nerfs</span> y <span class="sig-l fix"><i></i>cambios y arreglos</span>. '
            'El más reciente, arriba. Cada parche lleva primero un resumen y, debajo, las notas completas de Blizzard traducidas. '
            'La beta acaba el 21 de octubre y el juego sale el 4 de noviembre.</p>' + nav_forever('cambios') + out +
            f'<p class="fine">Fuente: <a href="{NOTAS}" target="_blank" rel="noopener noreferrer">notas de desarrollo oficiales de la beta (Blizzard)</a> y '
            f'<a href="{FORO}" target="_blank" rel="noopener noreferrer">avisos de Blizzard en su foro</a>. Resumimos lo que afecta al juego; los arreglos menores (sonidos, animaciones, textos) se quedan fuera. '
            'Las guías de clase de la beta (nivel 30) pueden no recoger aún todos estos cambios.</p>' + classic_forever())


# «Qué cambia de WoW Classic a WoW Forever»: solo lo que Blizzard ha publicado (noticias oficiales y notas de la beta).
FUENTES = {
    'DD': ('Repaso a fondo (panel de la BlizzCon)', 'https://news.blizzard.com/es-es/article/24303313/'),
    'QNE': ('Qué nos espera en WoW Forever', 'https://news.blizzard.com/es-es/article/24303862/'),
    'ED': ('Ediciones de WoW Forever', 'https://news.blizzard.com/en-us/article/24302093/'),
    'RAZA': ('Los célicos', 'https://news.blizzard.com/es-es/article/24302071'),
    'LEG': ('El Legado', 'https://news.blizzard.com/en-us/article/24307383/'),
    'NOM': ('Reserva de nombres', 'https://news.blizzard.com/es-es/article/24304161/'),
    'JCJ': ('Cómo funciona el JcJ', 'https://news.blizzard.com/en-us/article/24303316/how-pvp-progression-in-world-of-warcraft-forever-works'),
    'NOTAS': ('Notas de desarrollo de la beta', NOTAS),
}
# (tema, icono, [(punto, cómo es en Classic o None, cómo es en Forever, fuentes)])
CLASSIC_FOREVER = [
    ('Mundo y reinos', 'inv_misc_map_01', [
        ('Qué es', None, 'Blizzard lo llama una tercera versión del juego, junto a la actual y Classic: no es un modo, ni una temporada, ni otro Classic. La historia va después de Warcraft III y antes del Núcleo de Magma.', 'QNE'),
        ('Reinos', 'Eliges un reino concreto.', 'No hay reinos: eliges un conjunto de reglas (Normal, con JcJ solo si quieres; JcJ; o Rol). Hardcore llegará después del lanzamiento. Solo te agrupas con gente de tus mismas reglas, y Horda y Alianza siguen sin poder agruparse.', 'DD QNE'),
        ('Nombres', 'Nombre único en tu reino.', 'Nombre y segundo nombre (tipo apellido). Lo único es la combinación completa en toda la región; una hermandad puede compartir apellido y puedes ocultarlo en las placas.', 'NOM'),
        ('Más mundo', 'El mapa de 2004.', "Más de 1.000 misiones nuevas del 1 al 60, zonas nuevas (Isla de Zephras, Clarofluvial, Monte Hyjal, Shen'dralas, Garganta Negro Rumor) y retoques visuales en zonas conocidas. Sin voladoras ni escalado por nivel.", 'QNE'),
    ]),
    ('Razas y clases', 'achievement_character_human_male', [
        ('Raza nueva', None, 'Los célicos, en las dos facciones, con formas de druida propias. Vienen en el pack Heroico y superiores.', 'RAZA ED'),
        ('Combinaciones', 'Cada clase, con sus razas de 2004.', 'Combinaciones nuevas como sacerdote gnomo, cazador humano, chamán enano, mago orco, brujo trol o paladín no-muerto, y habrá más.', 'DD QNE'),
        ('Raciales', 'Raciales de Classic, muy desiguales.', 'Cada raza tiene 2 activas y 2 pasivas, con un poder ofensivo parecido entre razas.', 'DD'),
    ]),
    ('Talentos y combate', 'ability_marksmanship', [
        ('Árboles', 'Hitos de 1 punto en 11, 21 y 31.', 'Misma estructura y filas, con un hito nuevo en el 16. Algunos talentos pasan a ser habilidades básicas (Bendición de reyes, Espíritu divino, Marca de lo Salvaje mejorada).', 'DD'),
        ('Golpe y crítico', 'Separados para cuerpo a cuerpo, distancia y hechizos.', 'Unificados: ayuda a híbridos, provocaciones, venenos y trampas.', 'DD'),
        ('Estadísticas', None, 'La habilidad con armas pesa menos, el aumento de sanación da un tercio como daño, las armas de taumaturgo dan daño y sanación a la vez, y hay abalorios que rinden según la zona o el tipo de enemigo.', 'DD'),
        ('Ritmo', None, 'Se mantiene el de Classic: un enemigo normal en solitario tarda unos 10-15 segundos.', 'DD'),
        ('Paladín', 'Sin Golpe Sagrado ni Consagración básicos.', 'Golpe Sagrado al nivel 6, Consagración básica al 20, Sentencia que ya no gasta el sello y sello de tanque con provocación.', 'DD'),
    ]),
    ('Subir de nivel', 'inv_misc_food_15', [
        ('Acampada', None, 'Hogueras con vendedores, reparación, mesas de profesión y beneficios de 1 hora: te sientas un momento y listo.', 'DD NOTAS'),
        ('Comida y descanso', None, 'La comida fabricada da un pequeño extra de experiencia, y el Legado puede subir la experiencia por descanso.', 'DD'),
        ('Mazmorras', None, 'En la beta se ha reajustado la experiencia: más por enemigo, menos por misión de mazmorra, y la penalización de grupo vuelve a ser como en Classic.', 'NOTAS'),
    ]),
    ('Mazmorras y bandas', 'inv_misc_head_dragon_01', [
        ('Mazmorras', 'Las de 2004.', 'Nueve mazmorras nuevas, como el Salón de los Feudales, las Ruinas de Lordaeron o la Ciudad de Dalaran.', 'QNE NOTAS'),
        ('Bandas', None, 'Bandas nuevas: Cima Hyjal (20 jugadores) y Cavernas del Túmulo (10), con conjuntos nuevos. Se desbloquean el 9 de diciembre.', 'QNE'),
        ('Botín', None, 'Los objetos únicos de jefe son azules, los bonus de conjunto mejoran y hay cientos de objetos nuevos.', 'DD'),
        ('Transfiguración', 'No existe.', 'Opcional (se puede apagar). Verdes y azules dan la apariencia a todo el grupo con derecho; los épicos de banda, solo a quien se los queda.', 'DD'),
    ]),
    ('Profesiones', 'trade_engineering', [
        ('Recetas', None, 'Más de 600 recetas nuevas.', 'DD'),
        ('Para la hoguera', None, 'Cada profesión tiene objetos para el campamento (piedra de afilar, estandarte, vela de incienso…); hasta 3 por hoguera, uno por jugador.', 'DD'),
    ]),
    ('Legado (nuevo)', 'inv_misc_book_09', [
        ('Qué es', 'No existe.', 'Progreso de toda la cuenta: 65 desafíos en 6 categorías y tres árboles (Profesiones, Aventura e Ingenio). Al salir, 16 puntos gastables por personaje.', 'LEG'),
        ('Recompensas', None, 'Ventajas como Bien descansado o Cosecha generosa, y cosméticos (montura y cachorro de oso espectral, tabardo).', 'LEG DD'),
    ]),
    ('JcJ', 'inv_bannerpvp_02', [
        ('Rango', 'El rango sale del honor y cae cada semana.', 'Honor y Puntos de rango van por separado; los puntos salen de campos de batalla y misiones JcJ, con tope semanal.', 'JCJ'),
        ('Equipo', None, 'Con honor compras un set azul y uno épico; el épico pide además un sello que exige rango. Rangos del 1 al 14 con tabardos, capas, monturas y armas.', 'JCJ'),
        ('Campo nuevo', None, 'Islas Lanza Negra, 15 contra 15, con puntos y banderas al estilo de la Cuenca de Arathi.', 'QNE'),
    ]),
    ('Interfaz', 'inv_gizmo_02', [
        ('Gráficos', 'Solo los de 2004.', 'Preajuste clásico o moderno, modelos HD o SD y animaciones clásicas en los HD.', 'QNE'),
        ('Comodidad', None, 'Soporte para mando, buscador de grupo y gestor de reutilizaciones con todas las clases, raciales y abalorios.', 'QNE NOTAS'),
    ]),
    ('Acceso', 'inv_misc_coin_02', [
        ('Cómo se juega', 'Incluido con la suscripción.', 'También incluido con la suscripción. Sale el 4 de noviembre (de madrugada del 5 en España); los packs Heroico y Épico añaden célicos, reserva de nombre y cosméticos.', 'ED'),
    ]),
]


def fuentes(claves):
    return ' · '.join(f'<a href="{FUENTES[k][1]}" target="_blank" rel="noopener noreferrer">{E(FUENTES[k][0])}</a>' for k in claves.split())


def classic_forever():
    out = ''
    for tema, icono, filas in CLASSIC_FOREVER:
        out += (f'<div class="cf-bloque"><h3><img src="https://wow.zamimg.com/images/wow/icons/large/{icono}.jpg" alt="">{E(tema)}</h3><dl class="cf-lista">'
                + ''.join(f'<div class="cf-fila"><dt>{E(t)}</dt><dd>'
                          + (f'<p class="cf-c"><b>Classic</b> {E(c)}</p>' if c else '')
                          + f'<p class="cf-f"><b>Forever</b> {E(f)}</p><p class="cf-src">{fuentes(src)}</p></dd></div>' for t, c, f, src in filas)
                + '</dl></div>')
    return ('<h2 id="classic-a-forever" class="cf-titulo">Qué cambia de WoW Classic a WoW Forever</h2>'
            '<p class="lead">Si vienes de Classic, esto es lo que te vas a encontrar distinto. Todo sale de lo que ha publicado Blizzard; '
            'lo que aún no ha confirmado (doble especialización, banco, ficha de WoW, capas…) no lo ponemos.</p>'
            f'<div class="cf-grid">{out}</div>')


CSS = notas_blizzard.CSS + iconos_clase.CSS + '''
.parche{margin:0 0 14px;border:1px solid #2c3444;border-radius:12px;background:linear-gradient(170deg,#141a26,#0a0d13);overflow:hidden}
.parche>summary{cursor:pointer;padding:16px 20px;font:700 18px "Cinzel",Georgia,serif;color:var(--gold);list-style:none}
.parche>summary::-webkit-details-marker{display:none}
.parche>summary:before{content:"▸ ";color:#c99a3c}.parche[open]>summary:before{content:"▾ "}
.parche>summary b{color:#ffe7a6}
.parche-body{padding:0 20px 18px}.parche-body>h3{margin:2px 0 6px;color:#ffe7a6}.parche-body>.eyebrow{margin:0}
/* Van 16-10: iconos del propio WoW en vez de triángulos: Blessing of Might (mejora), Curse of Weakness (nerf), llave de ingeniería (cambio) */
.cambios-lista{list-style:none;margin:8px 0 12px;padding:0}.cambios-lista li{position:relative;padding:5px 0 5px 32px;color:#dfe5ee;line-height:1.5}
.cambios-lista .sig,.sig-l i{display:inline-block;width:20px;height:20px;font-size:0;border-radius:4px;background:center/cover no-repeat;vertical-align:-5px}
.cambios-lista .sig{position:absolute;left:0;top:6px}
.cambios-lista li.up .sig,.sig-l.up i,.grupo.up i{background-image:url(https://wow.zamimg.com/images/wow/icons/medium/spell_holy_fistofjustice.jpg);box-shadow:0 0 0 1px #3ddc84,0 0 6px #3ddc8466}
.cambios-lista li.down .sig,.sig-l.down i,.grupo.down i{background-image:url(https://wow.zamimg.com/images/wow/icons/medium/spell_shadow_curseofmannoroth.jpg);box-shadow:0 0 0 1px #ff6b63,0 0 6px #ff6b6366}
.cambios-lista li.fix .sig,.sig-l.fix i,.grupo.fix i{background-image:url(https://wow.zamimg.com/images/wow/icons/medium/inv_misc_wrench_01.jpg);box-shadow:0 0 0 1px #9aa5b8}
.grupo{margin:10px 0 2px;font:700 12px "Segoe UI",sans-serif;letter-spacing:.08em;text-transform:uppercase}.grupo i{display:inline-block;width:16px;height:16px;margin-right:7px;border-radius:3px;background:center/cover no-repeat;vertical-align:-3px}.grupo.up{color:#3ddc84}.grupo.down{color:#ff6b63}.grupo.fix{color:#9aa5b8}.cc .grupo:first-of-type{margin-top:4px}.cambios-lista{margin-top:2px!important}
/* Van 16-10: el icono va solo en el título del grupo; en cada línea, una viñeta discreta */
.cambios-lista .sig{display:none}.cambios-lista li{padding-left:18px!important}.cambios-lista li:before{content:"•";position:absolute;left:4px;top:5px;font-weight:700}.cambios-lista li.up:before{color:#3ddc84}.cambios-lista li.down:before{color:#ff6b63}.cambios-lista li.fix:before{color:#9aa5b8}
.sig-l{font-weight:700;white-space:nowrap}.sig-l i{margin-right:6px}.sig-l.up{color:#3ddc84}.sig-l.down{color:#ff6b63}.sig-l.fix{color:#9aa5b8}
.cambios-clases{display:grid;grid-template-columns:1fr;gap:12px}  /* Van 16-10: una sola columna, razas y luego clases */
.cc{padding:12px 14px;border:1px solid #2c3444;border-radius:8px;background:#0f141d}.cc h4{margin:0 0 4px;font:700 15px "Cinzel",Georgia,serif;color:var(--gold)}
.cc .cambios-lista{margin:0}
@media(max-width:600px){.cambios-clases{grid-template-columns:1fr}.parche>summary{font-size:16px}}
.cf-titulo{margin:38px 0 6px}
.cf-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:14px}
.cf-bloque{padding:14px 18px;border:1px solid #2c3444;border-radius:12px;background:linear-gradient(170deg,#141a26,#0a0d13)}
.cf-bloque h3{display:flex;align-items:center;gap:10px;margin:0 0 8px;color:#ffe7a6}.cf-bloque h3 img{width:30px;height:30px;border-radius:6px;border:1px solid #6b5a2e}
.cf-lista{margin:0}.cf-fila{padding:8px 0;border-top:1px solid #222a37}.cf-fila:first-child{border-top:0}
.cf-fila dt{font-weight:700;color:var(--gold);margin-bottom:3px}.cf-fila dd{margin:0}
.cf-fila p{margin:2px 0;line-height:1.5}.cf-c{color:#9aa5b8}.cf-f{color:#dfe5ee}
.cf-fila p b{display:inline-block;min-width:62px;font-size:12px;letter-spacing:.04em;text-transform:uppercase}.cf-c b{color:#8a93a3}.cf-f b{color:#3ddc84}
.cf-src{font-size:12px;color:#7d8798}.cf-src a{color:#9aa5b8}
@media(max-width:600px){.cf-grid{grid-template-columns:1fr}.cf-bloque{padding:12px 14px}}
'''
