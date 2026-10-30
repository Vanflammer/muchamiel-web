"""WoW Forever, juego completo (sale el 4-11-2026, nivel 60 sin límite). Pedido de Van el 15-10-2026:
el menú «WoW Forever Beta» se queda como estaba (nivel 30) y aquí va lo nuevo, con su propio desplegable «WoW Forever».
Datos investigados el 15-10-2026 (ver research/forever-*.md). Lo dudoso se marca como tal en la página."""
import html

E = html.escape
TF = 'https://talentsforever.com/'
BLIZZ_LANZ = 'https://news.blizzard.com/es-es/article/24303862/'
BLIZZ_PACKS = 'https://news.blizzard.com/en-us/article/24302093/'
BLIZZ_CELICOS = 'https://news.blizzard.com/es-es/article/24302071'
BLIZZ_REPASO = 'https://news.blizzard.com/es-es/article/24303313/world-of-warcraft-forever-resumen-de-la-mesa-redonda-repaso-a-fondo'
BLIZZ_LEGADO = 'https://news.blizzard.com/en-us/article/24307383/'
FORO_HORA = 'https://eu.forums.blizzard.com/es/wow/t/80119/1'
WT = 'https://www.warcrafttavern.com/forever/guides/'
ZAML = 'https://wow.zamimg.com/images/wow/icons/large/'
FECHA = '15 de octubre de 2026'


def link(url, text):
    return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{text}</a>'


def fuentes(*items):
    return '<p class="fine">Fuentes: ' + ' · '.join(link(u, E(t)) for t, u in items) + f'. Datos consultados el {FECHA}; pueden cambiar hasta el lanzamiento.</p>'


def nav_forever(actual):
    paginas = [('lanzamiento', 'Lanzamiento'), ('pagar-menos', 'Cuánto cuesta'), ('subir-nivel', 'Subir de nivel'), ('tecnicas', 'Técnicas'), ('oro', 'Ganar oro'),
               ('mazmorras', 'Mazmorras'), ('profesiones', 'Profesiones'), ('legacy', 'Legacy'), ('cambios', 'Notas del parche')]
    return '<div class="quick fnav">' + ''.join(
        f'<a href="../{k}/"' + (' aria-current="page"' if k == actual else '') + f'>{t}</a>' for k, t in paginas) + '</div>'


# ---------- Lanzamiento ----------
FECHAS = [
    ('23 oct, 19:00', 'Se cierra la beta, con 24 horas de fiesta de despedida (en México, a las 11:00; en Chile y Argentina, a las 14:00). Lo que hayas subido en la beta no pasa al juego: todos empiezan de nivel 1. <a href="../fin-beta/">La fiesta</a>.'),
    ('27 oct – 3 nov', 'Reserva de nombres: abre el 27 a las 18:00 (en América, a las 14:00 en México y a las 17:00 en Chile y Argentina). Hasta 3 personajes por cuenta, por orden de llegada. Solo con el pack Heroico, Épico o la Colección. <a href="../reserva-nombres/">Cómo se hace</a>.'),
    ('5 nov, 00:00', '<strong>Lanzamiento</strong> (en México, el 4 a las 17:00; en Chile y Argentina, el 4 a las 20:00). Nivel 60 desde el primer día.'),
    ('9 dic', 'Primeras bandas: Cavernas del Túmulo (10 jugadores), Cima Hyjal (20) y Guarida de Onyxia (40). <a href="../bandas-forever/">Las bandas y cómo entrar en Onyxia</a>.'),
    ('Primavera 2027', 'Dos bandas nuevas (10 y 20), dos mazmorras y una misión legendaria.'),
    ('Verano 2027', 'Una banda clásica renovada, otra nueva, dos mazmorras más y una actualización de profesiones.'),
]
PACKS = [
    ('Suscripción', 'Con la suscripción de WoW o tiempo de juego ya puedes jugar a Forever. No hace falta comprar nada más.'),
    ('Pack Heroico', 'La raza nueva (cielonatos) con su zona, la Isla de Zephras, la reserva de nombres y una montura. Unos 29,99 €.'),
    ('Pack Épico', 'Lo del Heroico más el acceso a la beta y 30 días de tiempo de juego desde el 4 de noviembre. Unos 59,99 €.'),
    ('Colección Warcraft Forever', 'Lo del Épico más Warcraft III: Reforged y la campaña Forsaken Kingdom. Por tiempo limitado. Unos 79,99 €.'),
]
NOVEDADES = [
    ('achievement_character_bloodelf_female', 'Raza nueva: cielonatos', 'Los Skyborne (al principio Blizzard los llamó «célicos»): Formaviento y Orden Eminente. Empiezan en la Isla de Zephras (1-12), que comparten las dos facciones. Hace falta el pack Heroico.'),
    ('inv_misc_map_01', 'Zonas nuevas', 'Riverglades (35-45), Shen\'dralas, el Monte Hyjal renovado a nivel 60 y Dalaran de vuelta en Alterac. Más de 1.000 misiones nuevas.'),
    ('spell_fire_fire', 'Acampada', 'Hogueras para descansar, cocinar y montar puestos de profesión en mitad de la zona.'),
    ('inv_misc_book_09', 'Legacy', 'Progreso de cuenta: ventajas que comparten todos tus personajes. Te lo contamos en su página.'),
    ('inv_misc_gear_08', 'Sin reinos', 'Eliges conjunto de reglas (Normal, JcJ o Rol; Hardcore más adelante) y el juego reparte en capas. Facciones separadas como siempre.'),
    ('inv_misc_coin_01', 'Mano dura con el oro', 'Comprar oro también se castiga (en la beta ya han cerrado unas 3.700 cuentas, y a los sospechosos se les bloquea un tiempo el comercio, el correo y la subasta), el juego avisa al comerciar oro con desconocidos y las bandas por subasta de oro (GDKP) están prohibidas. Sin ficha de WoW ni subidas de nivel.'),
    ('inv_misc_note_01', 'Nombre y apellido', 'Tu personaje lleva nombre y apellido obligatorio, únicos en toda Europa. Por eso compensa la reserva de nombres. En las reglas JcJ, una sola facción por cuenta.'),
    ('inv_misc_bag_10', 'Banco y buscador de grupo', 'El banco pasa a 48 casillas y hay banco de hermandad. El buscador de grupo filtra por idioma y por estilo (aprendiendo, relajado o competitivo), pero no teletransporta.'),
    ('achievement_bg_winwsg', 'JcJ nuevo', 'Honor y rangos del 1 al 14, temporadas en vez de JcJ clasificado y un campo de batalla nuevo de 15 contra 15: las Islas Lanzanegra (niveles 30-60).'),
    ('ability_dualwield', 'Doble especialización', 'Desde el nivel 40 (Blizzard estudia bajarla al 30). Reiniciar talentos sube de precio cada vez y el precio baja cada semana.'),
]


def lanzamiento():
    fechas = ''.join(f'<tr><th>{E(f)}</th><td>{t}</td></tr>' for f, t in FECHAS)
    packs = ''.join(f'<div class="tile"><strong>{E(n)}</strong><span>{E(t)}</span></div>' for n, t in PACKS)
    nov = ''.join(f'<article class="addon"><img src="{ZAML}{i}.jpg" alt=""><div><h3>{E(n)}</h3><p>{E(t)}</p></div></article>' for i, n, t in NOVEDADES)
    return ('<p class="eyebrow">WOW FOREVER · EL JUEGO COMPLETO</p><h1>WoW Forever: el lanzamiento</h1>'
            '<p class="lead">El <strong>4 de noviembre</strong> sale WoW Forever con el nivel máximo en <strong>60 desde el primer día</strong>. '
            'Aquí tienes todo lo que necesitas saber para empezar con buen pie: fechas, qué hace falta para jugar y qué trae de nuevo.</p>'
            + nav_forever('lanzamiento') +
            '<div class="tfo-stats"><div><b data-countdown="2026-11-05">5 nov</b><span>para el lanzamiento</span></div><div><b>Nivel 60</b><span>desde el primer día</span></div>'
            '<div><b>9</b><span>mazmorras nuevas</span></div><div><b>9 dic</b><span>primeras bandas</span></div></div>'
            '<div class="divider"><h2>Fechas clave</h2></div><table class="keys">' + fechas + '</table>'
            f'<p class="fine">Hora peninsular. Blizzard la da como 15:00 PST del 4 de noviembre; en su {link(FORO_HORA, "foro en castellano")} confirman las 00:00 del 5. En México es el 4 a las 17:00, y en Chile y Argentina, el 4 a las 20:00.</p>'
            '<div class="divider"><h2>Qué necesitas para jugar</h2></div><div class="tiles">' + packs + '</div>'
            '<p class="fine">Precios oficiales de la tienda de Battle.net. <a href="../pagar-menos/">Todas las formas de pagar y cuál te sale más barata</a>.</p>'
            '<div class="divider"><h2>Lo nuevo de Forever</h2></div><div class="addons">' + nov + '</div>'
            '<div class="divider"><h2>Prepárate</h2></div><div class="tiles">'
            '<a class="tile" href="../subir-nivel/"><strong>Subir de nivel</strong><span>Zonas, consejos y monturas del 1 al 60.</span></a>'
            '<a class="tile" href="../clases/"><strong>Builds nivel 60</strong><span>Las más populares de cada clase.</span></a>'
            '<a class="tile" href="../mazmorras/"><strong>Mazmorras</strong><span>Todas, con niveles. Nueve son nuevas.</span></a>'
            '<a class="tile" href="../profesiones/"><strong>Profesiones</strong><span>Qué cambia y cuáles elegir.</span></a></div>'
            + fuentes(('Blizzard: lo que trae Forever', BLIZZ_LANZ), ('Blizzard: ediciones', BLIZZ_PACKS), ('Blizzard: cielonatos', BLIZZ_CELICOS),
                      ('Warcraft Tavern', 'https://www.warcrafttavern.com/forever/news/world-of-warcraft-forever-roadmap-beta-launch-date-raids/')))



def lanzamiento_inicio():
    # Van 16-10: el lanzamiento en la portada (a prueba): lo mismo que /lanzamiento/ sin título, menú de Forever ni «Prepárate».
    s = lanzamiento()
    lead = s[s.index('<p class="lead">'):s.index('</p>', s.index('<p class="lead">')) + 4]
    s = s[s.index('<div class="tfo-stats">'):s.index('<div class="divider"><h2>Prepárate</h2>')]
    return ('<section class="lanz-inicio" id="lanzamiento"><div class="divider"><h2>WoW Forever: el lanzamiento</h2></div>'
            + lead + s.replace('href="../', 'href="') + '</section>')


# ---------- Cuánto cuesta jugar (Van, 16-10-2026: plan de monetización, con el enlace de afiliado de Instant Gaming) ----------
IG_60 = 'https://www.instant-gaming.com/es/82-comprar-world-of-warcraft-tarjeta-60-dias-pc-mac-battle-net/?igr=muchamiel'
BLIZZ_SUB = 'https://eu.shop.battle.net/es-es/product/world-of-warcraft-subscription'
BLIZZ_FOREVER = 'https://eu.shop.battle.net/es-es/product/world-of-warcraft-forever'


def pagar_menos():
    filas = ''.join(f'<tr><th>{a}</th><td>{b}</td><td>{c}</td></tr>' for a, b, c in [
        ('Suscripción de 1 mes', '12,99 €', 'Se renueva sola cada mes.'),
        ('Suscripción de 3 meses', '11,99 € al mes', 'Se paga cada 3 meses.'),
        ('<b>Suscripción de 6 o 12 meses</b>', '<b>10,99 € al mes</b>', 'La más barata a la larga, con extras de regalo en la tienda. Se paga por adelantado.'),
        ('Tarjeta de 60 días (Blizzard)', '25,98 €', 'Unos 12,99 € al mes. Sin renovación automática.'),
        (f'<b><a href="{IG_60}" target="_blank" rel="noopener noreferrer sponsored">Tarjeta de 60 días en Instant Gaming</a></b>', '<b>24,19 €</b>', 'Unos 12,10 € al mes. Sin renovación automática ni tarjeta bancaria: llega un código y se canjea en Battle.net. Solo para cuentas de Europa.')])
    packs = ''.join(f'<tr><th>{a}</th><td>{b}</td><td>{c}</td></tr>' for a, b, c in [
        ('Pack Heroico', '29,99 €', 'La raza nueva (célicos) con la Isla de Zephras, la reserva de nombres y una montura.'),
        ('Pack Épico', '59,99 €', 'Lo del Heroico, acceso a la beta y 30 días de tiempo de juego.'),
        ('Warcraft Forever Collection', '79,99 €', 'Lo del Épico y Warcraft III: Reforged con la campaña Forsaken Kingdom.')])
    return ('<p class="eyebrow">WOW FOREVER · PRECIOS</p><h1>Cuánto cuesta jugar a WoW Forever (y cómo pagar menos)</h1>'
            '<p class="lead">Para jugar a WoW Forever solo hace falta <strong>suscripción o tiempo de juego</strong>; los packs son opcionales. '
            'Aquí tienes todas las formas de pagarlo, con los precios de hoy, y cuál te sale más barata según cómo juegues.</p>' + nav_forever('pagar-menos') +
            '<div class="divider"><h2>Tiempo de juego: todas las opciones</h2></div><table class="keys"><tr><th>Opción</th><td><strong>Precio</strong></td><td><strong>Cómo es</strong></td></tr>' + filas + '</table>'
            '<div class="divider"><h2>Qué te conviene</h2></div><div class="tiles">'
            '<div class="tile"><strong>Si vas a jugar meses</strong><span>La suscripción de 6 o 12 meses: 10,99 € al mes, lo más barato a la larga.</span></div>'
            f'<a class="tile" href="{IG_60}" target="_blank" rel="noopener noreferrer sponsored"><strong>Si quieres probar sin atarte</strong><span>La tarjeta de 60 días de Instant Gaming: más barata que pagar mes a mes y sin renovación automática.</span></a>'
            f'<a class="tile" href="{IG_60}" target="_blank" rel="noopener noreferrer sponsored"><strong>Si no tienes tarjeta bancaria</strong><span>Un código de tiempo de juego se paga con PayPal u otros métodos y se canjea en Battle.net.</span></a></div>'
            '<div class="divider"><h2>Los packs de WoW Forever (opcionales)</h2></div><table class="keys"><tr><th>Pack</th><td><strong>Precio</strong></td><td><strong>Qué trae</strong></td></tr>' + packs + '</table>'
            '<p>Solo hacen falta si quieres jugar con los <strong>célicos</strong> o <strong>reservar tu nombre</strong> (del 27 de octubre al 3 de noviembre: <a href="../reserva-nombres/">cómo se hace</a>). '
            'El Épico trae 30 días de juego: si ibas a pagar el primer mes igualmente, la diferencia real con el Heroico es de unos 17 €.</p>'
            '<p><strong>¿Quieres probarlo antes?</strong> El miércoles 21 de octubre a las 19:00* se puede jugar gratis unas horas: <a href="../beta-gratis/">cómo entrar</a>. <span class="latam">* México: 15:00 · Chile y Argentina: 18:00.</span></p>'
            '<div class="prepare" style="margin-top:22px"><h3>Antes de comprar</h3><p>Los códigos de tiempo de juego van por región: el de Instant Gaming es para cuentas de Europa. '
            'Si juegas desde Latinoamérica en la región de América, necesitas un código de esa región. Los precios cambian: compruébalos al comprar.</p></div>'
            '<p class="fine">El enlace de Instant Gaming es de afiliado de Muchamiel: si compras con él, Muchamiel se lleva una pequeña comisión y a ti te cuesta lo mismo. '
            'Precios consultados el 16-10-2026 en ' + link(BLIZZ_SUB, 'la tienda de Battle.net (suscripción)') + ', ' + link(BLIZZ_FOREVER, 'la tienda de Battle.net (packs)') + ' e Instant Gaming.</p>')


# ---------- Subir de nivel ----------
CONSEJOS = [
    ('Haz las misiones de cada mazmorra', 'En Forever casi toda la experiencia de una mazmorra está en sus misiones. Recógelas antes de entrar; repetirla sin misiones da muy poco.'),
    ('Agrúpate con gente de tu nivel', 'Ir con personajes de más nivel penaliza la experiencia más que en Classic, y que te «suban» en mazmorras ya no compensa.'),
    ('Aprende Cocina pronto', 'Hacia el nivel 5 sale la misión «The Great Outdoors»: te enseña a montar una hoguera. Y la comida Well Fed da +5 % de experiencia 15 minutos.'),
    ('Desconecta descansando', 'En posada, en ciudad o con el Cozy Sleeping Bag (se consigue con una cadena de misiones), que además da +3 % de experiencia por muerte.'),
    ('Pelea con enemigos de tu nivel', 'Explorar por explorar da poca experiencia. Ve a la zona que te toca y no te desvíes.'),
    ('Recolecta para la montura', 'Una o dos profesiones de recolección y la casa de subastas te pagan la equitación del nivel 40.'),
    ('Ve andando a las mazmorras', 'El buscador de grupo no teletransporta: hay que ir hasta la entrada. Un brujo puede invocar al grupo en la piedra.'),
    ('Alianza: Salón de los Feudales', 'Sus cinco misiones, bajo Forjaz, son un buen empujón entre el 13 y el 18.'),
]
ZONAS = [
    ('1-10', 'Dun Morogh, Bosque de Elwynn, Teldrassil', 'Durotar, Mulgore, Claros de Tirisfal'),
    ('1-12', '★ Isla de Zephras (cielonatos)', '★ Isla de Zephras (cielonatos)'),
    ('10-20', 'Costa Oscura, Loch Modan, Páramos de Poniente', 'Los Baldíos, Bosque de Argénteos'),
    ('15-27', 'Montañas Crestagrana, Sierra Espolón', 'Sierra Espolón, Los Baldíos'),
    ('18-30', 'Vallefresno, Bosque del Ocaso, Los Humedales (★ misiones nuevas)', 'Vallefresno, Laderas de Trabalomas'),
    ('25-35', 'Las Mil Agujas, Laderas de Trabalomas', 'Las Mil Agujas'),
    ('30-45', 'Tierras Altas de Arathi, Desolace, Vega de Tuercespina, Alterac', 'Tierras Altas de Arathi, Desolace, Vega de Tuercespina'),
    ('35-45', '★ Riverglades, Marjal Revolcafango, Tierras Inhóspitas', '★ Riverglades, Marjal Revolcafango, Pantano de las Penas'),
    ('40-50', 'Feralas, Tierras del Interior, Tanaris', 'Feralas, Tierras del Interior, Tanaris'),
    ('45-55', 'Azshara, Las Tierras Devastadas, La Garganta de Fuego', 'Azshara, Las Tierras Devastadas, La Garganta de Fuego'),
    ('48-58', 'Frondavil, Cráter de Un\'Goro, Las Estepas Ardientes', 'Frondavil, Cráter de Un\'Goro, Las Estepas Ardientes'),
    ('51-60', 'Tierras de la Peste, Cuna del Invierno, Silithus, ★ Monte Hyjal (60)', 'Tierras de la Peste, Cuna del Invierno, Silithus, ★ Monte Hyjal (60)'),
]


def subir_nivel():
    consejos = ''.join(f'<li><strong>{E(t)}</strong><span>{E(d)}</span></li>' for t, d in CONSEJOS)
    zonas = ''.join(f'<tr><th>{E(n)}</th><td>{E(a)}</td><td>{E(h)}</td></tr>' for n, a, h in ZONAS)
    return ('<p class="eyebrow">WOW FOREVER · DEL 1 AL 60</p><h1>Subir de nivel en WoW Forever</h1>'
            '<p class="lead">Del 1 al 60 hacen falta los mismos 4.084.700 puntos de experiencia que en Classic, pero Forever cambia cómo se consiguen: '
            'más misiones, mazmorras que se suben con sus misiones, hogueras y monturas más baratas. Estos son los consejos que más tiempo te ahorran.</p>'
            + nav_forever('subir-nivel') +
            '<div class="divider"><h2>8 consejos para subir rápido</h2></div><ol class="pasos">' + consejos + '</ol>'
            '<div class="divider"><h2>Monturas y viajes</h2></div><table class="keys">'
            '<tr><th>Cómo funciona</th><td>En Forever lo caro es aprender a montar, no la montura. La montura se compra aparte y es barata, y la misma montura va lenta o rápida según tu equitación: también valen las de los packs.</td></tr>'
            '<tr><th>Nivel 40</th><td>Equitación lenta (+60 %): 100 de oro. Monturas del vendedor: 20 de oro.</td></tr>'
            '<tr><th>Nivel 60</th><td>Equitación rápida (+100 %): 1.000 de oro. Monturas del vendedor: 200 de oro, aunque con la de 20 ya vas rápido.</td></tr>'
            '<tr><th>Descuento</th><td>Con reputación Honorable con tu facción, más barata. Paladines y brujos consiguen la suya con su misión de clase.</td></tr>'
            '<tr><th>Viajes nuevos</th><td>Barco del puerto de Ventormenta a Auberdine, ruta Menethil–Costasur–Auberdine, barco de Tanaris a Powderfuse Port (Riverglades) y los Valanaar Skydocks a la Isla de Zephras.</td></tr>'
            '</table><p class="fine">No hay monturas voladoras ni escalado de nivel.</p>'
            '<div class="divider"><h2>Zonas por nivel</h2></div><table class="keys zonas"><tr><th>Nivel</th><th>Alianza</th><th>Horda</th></tr>' + zonas + '</table>'
            '<p class="fine">★ = nuevo en Forever. El resto de zonas sigue con los niveles de Classic. Shen\'dralas también es nueva, pero Blizzard aún no ha dado su nivel.</p>'
            '<div class="tiles" style="margin-top:20px"><a class="tile" href="../mazmorras/"><strong>Mazmorras</strong><span>Qué mazmorra toca a cada nivel.</span></a>'
            '<a class="tile" href="../clases/"><strong>Builds nivel 60</strong><span>Y la calculadora para planificar tus talentos.</span></a>'
            '<a class="tile" href="../legacy/"><strong>Legacy</strong><span>Well Rested y Talented aceleran tus siguientes personajes.</span></a></div>'
            + fuentes(('Blizzard: repaso a fondo de Forever', BLIZZ_REPASO), ('AlterTime: precios de la equitación', 'https://www.youtube.com/watch?v=ITS73jZvp1I'), ('Warcraft Tavern: experiencia', WT + 'experience/'), ('Warcraft Tavern: acampada', WT + 'camping/'),
                      ('Warcraft Tavern: monturas', WT + 'riding/'), ('Warcraft Wiki: Forever', 'https://warcraft.wiki.gg/wiki/Forever')))


# ---------- Builds nivel 60 ----------
# (slug, nombre, reparto de specs, [(puntos, spec, url)], habilidades nuevas)
BUILDS = [
    ('warrior', 'Guerrero', 'Arms 27 % · Fury 37 % · Protection 36 %',
     [('7/5/39', 'Protection', 'warrior/60/0502-05-250533120321021351-6'), ('17/34/0', 'Fury', 'warrior/60/30305013002-05253005151010501--6'),
      ('37/11/0', 'Arms', 'warrior/60/30305213132515201-050501--6')],
     'Victory Rush (20), Spearing Strike (25, Arms). Tactical Mastery pasa a ser pasiva (14).'),
    ('paladin', 'Paladín', 'Holy 26 % · Protection 32 % · Retribution 42 %',
     [('8/8/35', 'Retribution', 'paladin/60/50003-503-05225131201331321-6'), ('0/42/7', 'Protection', 'paladin/60/-4530513321301551-502-6'),
      ('36/10/5', 'Holy', 'paladin/60/05320213225131051-5032-05-6')],
     'Holy Strike (6), Seal of Fury (10, sello de tanque). Blessing of Kings y Consecration (20) ya se entrenan.'),
    ('hunter', 'Cazador', 'Beast Mastery 26 % · Marksmanship 27 % · Survival 47 %',
     [('5/11/35', 'Survival', 'hunter/60/5-005005001-500230230250222151-6'), ('5/41/5', 'Marksmanship', 'hunter/60/5-3053552011523051-5-6'),
      ('31/20/0', 'Beast Mastery', 'hunter/60/5120021505101251-00503520005--6')],
     'Sonic Blast (12), Aimed Shot (20, ya se entrena), Lacerate (30), Enchanted Flare (32).'),
    ('rogue', 'Pícaro', 'Assassination 29 % · Combat 25 % · Subtlety 46 %',
     [('18/32/0', 'Combat', 'rogue/60/00530310501-32300320200515231--6'), ('38/11/2', 'Assassination', 'rogue/60/00531310551521051-302303-002-6'),
      ('16/12/23', 'Subtlety', 'rogue/60/30502010401-320302002-332002320021221-6')],
     'Mutilate (30, Assassination), Venom (40, Assassination), Thousand Cuts (Subtlety).'),
    ('priest', 'Sacerdote', 'Discipline 41 % · Holy 20 % · Shadow 39 %',
     [('14/3/34', 'Shadow', 'priest/60/0250030013-3-500322501201302251-6'), ('32/19/0', 'Discipline', 'priest/60/525330031305001001-30515100202--6'),
      ('19/32/0', 'Holy', 'priest/60/0053030013031-03505103030021531--6')],
     'Binding Heal (25), Penance (30), Shadow Word: Death (32), Prayer of Mending (40). Fear Ward y Devouring Plague, ahora para todas las razas.'),
    ('shaman', 'Chamán', 'Elemental 27 % · Enhancement 54 % · Restoration 19 %',
     [('18/33/0', 'Enhancement', 'shaman/60/050533002-052032031005112251--6'), ('0/10/41', 'Restoration', 'shaman/60/-055-5030503315513151-6'),
      ('38/13/0', 'Elemental', 'shaman/60/5505301303123151-055002001--6')],
     'Fire Nova como hechizo (12), Call of the Elements y Totemic Recall (20), Totemic Projection (22), Lava Burst, Rage of the Farseer o Riptide (40, según rama).'),
    ('mage', 'Mago', 'Arcane 25 % · Fire 31 % · Frost 44 %',
     [('0/29/22', 'Fire', 'mage/60/-0055103013013304-00550003310003002-6'), ('0/0/51', 'Frost', 'mage/60/--0555323331321331251-6'),
      ('47/4/0', 'Arcane', 'mage/60/255225223122311531-13--6')],
     'Arcane Blast e Ice Lance (20, por talento), Frostfire Bolt (40), Teleport: Dalaran (50, Alianza).'),
    ('warlock', 'Brujo', 'Affliction 36 % · Demonology 41 % · Destruction 23 %',
     [('40/11/0', 'Affliction', 'warlock/60/05550320035201351-0050203001--6'), ('5/11/35', 'Destruction', 'warlock/60/05-0050203001-2050355103101351-6'),
      ('5/33/13', 'Demonology', 'warlock/60/005-0050233201211031351-20550001-6')],
     'Bane of Havoc (30, Destruction), Incinerate (40, Destruction), Wrack (40, Affliction).'),
    ('druid', 'Druida', 'Balance 25 % · Feral 47 % · Restoration 28 %',
     [('11/5/35', 'Restoration', 'druid/60/05302001-05-5050035103113251-6'), ('9/42/0', 'Feral', 'druid/60/050022-55230202120132012551--6'),
      ('36/0/15', 'Balance', 'druid/60/5032220115501351--505203-6')],
     'Revive (12, resurrección fuera de combate), Ferocious Bite rango 1 (24), Lacerate (25, oso), Primal Bite, Shifting Power y Wild Growth (40). Berserk desaparece el 30-10.'),
]


def builds_60():
    cards = ''
    for slug, nombre, reparto, builds, nuevas in BUILDS:
        filas = ''.join(f'<li><b>{E(p)}</b> {E(s)} {link(TF + u, "Ver build")}</li>' for p, s, u in builds)
        if slug == 'mage':  # 30-10: Blizzard rehízo el árbol del mago el 28-10 (hotfix) y estas builds ya no se pueden hacer tal cual
            filas = '<li>El árbol de talentos del mago cambió el 28 de octubre: las builds de la beta ya no encajan. Mira las de la <a href="../mage/#g-60">guía del mago</a>.</li>'
        if slug == 'druid':  # 31-10: el árbol del druida cambió el 30-10 (hotfix sin nota de Blizzard) y estas builds ya no se pueden hacer tal cual
            filas = '<li>El árbol de talentos del druida cambió el 30 de octubre: las builds de la beta ya no encajan. Mira las de la <a href="../druid/#g-60">guía del druida</a>.</li>'
        cards += (f'<article class="addon build60"><img src="../assets/{slug}.jpg" alt=""><div><p class="eyebrow">{E(reparto)}</p><h3>{E(nombre)}</h3>'
                  f'<ol class="b60">{filas}</ol><p><strong>Nuevo en Forever:</strong> {E(nuevas)}</p>'
                  f'<a class="btn ghost" href="../{slug}/">Guía completa de la clase</a></div></article>')
    return ('<p class="eyebrow">WOW FOREVER · NIVEL 60</p><h1>Builds de nivel 60</h1>'
            '<p class="lead">Las builds de nivel 60 más planificadas de cada clase, con los 51 puntos repartidos. Pulsa «Ver build» para abrirla en el árbol de talentos. '
            'El porcentaje es cuánta gente juega cada rama.</p>' + nav_forever('builds-60') +
            '<div class="addons">' + cards + '</div>'
            '<div class="prepare" style="margin-top:22px"><h3>Antes de copiarlas</h3><p>Son las builds que más planifica la comunidad con los datos de la beta, no una recomendación probada a 60: '
            'nadie ha llegado aún a nivel 60 en Forever. Los talentos pueden cambiar hasta el lanzamiento y el orden se recalcula cada día. '
            'Con el Legado «Con talento» tu primer punto llega a nivel 5 en vez de 10, pero el máximo sigue en 51. La doble especialización llega a nivel 40, y reiniciar talentos sube de precio cada vez (el precio baja cada semana).</p>'
            '<div class="actions"><a class="btn gold" href="../calculadora/">Planifica la tuya en la calculadora</a></div></div>'
            + fuentes(('Talents Forever, datos del cliente de la beta (CC BY 4.0)', TF)))



def builds60_clase(slug):
    # Van 16-10: las builds de nivel 60 de cada clase, al final de su guía (sale del menú la página Builds nivel 60).
    for s, nombre, reparto, builds, nuevas in BUILDS:
        if s != slug:
            continue
        filas = ''.join(f'<li><b>{E(p)}</b> {E(s2)} {link(TF + u, "Ver build")}</li>' for p, s2, u in builds)
        return ('<section class="b60-guia" id="builds-60"><div class="divider"><h2>Builds recomendadas para nivel 60</h2></div>'
                f'<article class="addon build60"><img src="../assets/{slug}.jpg" alt=""><div><p class="eyebrow">{E(reparto)}</p><h3>{E(nombre)} · nivel 60</h3>'
                f'<ol class="b60">{filas}</ol><p><strong>Nuevo en Forever:</strong> {E(nuevas)}</p></div></article>'
                '<p class="fine">Son las builds de nivel 60 que más planifica la comunidad con los datos de la beta (el porcentaje es cuánta gente juega cada rama); '
                'nadie ha llegado aún a 60 en Forever y los talentos pueden cambiar hasta el lanzamiento.</p>'
                '<div class="actions" style="justify-content:center"><a class="btn gold" href="../calculadora/">Planifica la tuya en la calculadora</a></div></section>')
    return ''


# ---------- Mazmorras ----------
# (nivel, nombre, zona, nueva)
MAZMORRAS = [
    ('13-18', 'Salón de los Feudales', 'Bajo Forjaz', True), ('13-19', 'Sima Ígnea', 'Orgrimmar', False),
    ('15-20', 'Ruinas de Lordaeron', 'Entrañas (Horda)', True), ('18-24', 'Minas de la Muerte', 'Páramos de Poniente', False),
    ('19-25', 'Cuevas de los Lamentos', 'Los Baldíos', False), ('23-29', 'Castillo de Colmillo Oscuro', 'Bosque de Argénteos', False),
    ('24-29', 'Excavación de Whelgar', 'Los Humedales', True), ('25-31', 'Cavernas de Brazanegra', 'Vallefresno', False),
    ('26-32', 'Las Mazmorras', 'Ventormenta', False), ('28-33', 'Ciudad de Dalaran', 'Montañas de Alterac', True),
    ('30-36', 'Horado Rajacieno', 'Los Baldíos', False), ('31-37', 'Gnomeregan', 'Dun Morogh', False),
    ('31-45', 'Monasterio Escarlata', 'Claros de Tirisfal', False), ('35-40', 'Ciudad Sumergida', 'Vega de Tuercespina', True),
    ('38-44', 'Zahúrda Rajacieno', 'Los Baldíos', False), ('40-45', "Bastión Krol'dok", 'Riverglades', True),
    ('44-50', 'Uldaman', 'Tierras Inhóspitas', False), ('45-51', "Zul'Farrak", 'Tanaris', False),
    ('48-53', 'Prisión de Alcaz', 'Marjal Revolcafango', True), ('48-54', 'Maraudon', 'Desolace', False),
    ('52-58', "Templo de Atal'Hakkar", 'Pantano de las Penas', False), ('52-60', 'Profundidades de Roca Negra', 'Montaña Roca Negra', False),
    ('55-60', 'La Masacre', 'Feralas', False), ('55-60', 'Bastión Faucenegra', 'Azshara', True),
    ('55-60', 'Cumbre de Roca Negra Inferior', 'Montaña Roca Negra', False), ('58-60', 'Bancal del Creador', "Cráter de Un'Goro", True),
    ('58-60', 'Scholomance', 'Tierras de la Peste del Oeste', False), ('58-60', 'Stratholme', 'Tierras de la Peste del Este', False),
]


def mazmorras():
    import mazmorras_portal  # Van 16-10: el nombre lleva a la página de la mazmorra si ya la tiene
    pag = {m['es']: m['slug'] for m in mazmorras_portal.cargar()}
    nombre = lambda nom: f'<a href="{pag[nom]}/">{E(nom)}</a>' if nom in pag else E(nom)
    filas = ''.join(f'<tr{" class=nueva" if n else ""}><th>{E(lv)}</th><td>{"★ " if n else ""}{nombre(nom)}</td><td>{E(z)}</td></tr>' for lv, nom, z, n in MAZMORRAS)
    return ('<p class="eyebrow">WOW FOREVER · 5 JUGADORES</p><h1>Mazmorras de WoW Forever</h1>'
            '<p class="lead">Todas las mazmorras del lanzamiento con su nivel recomendado. <strong>Nueve son nuevas</strong> y las clásicas traen botín renovado, '
            'con cientos de objetos nuevos.</p>' + nav_forever('mazmorras') +
            '<table class="keys zonas"><tr><th>Nivel</th><th>Mazmorra</th><th>Dónde</th></tr>' + filas + '</table>'
            '<p class="fine">★ = nueva en Forever. Los niveles de las nuevas son los de Blizzard; algunas guías antiguas dan otros rangos.</p>'
            '<div class="divider"><h2>Qué cambia</h2></div><div class="tiles">'
            '<div class="tile"><strong>La experiencia está en las misiones</strong><span>Los monstruos dan menos y las misiones de mazmorra más. Recógelas antes de entrar.</span></div>'
            '<div class="tile"><strong>Botín y transfiguración</strong><span>Cada objeto que cae desbloquea su apariencia para todos los que pueden recogerlo.</span></div>'
            '<div class="tile"><strong>Sin teletransporte</strong><span>El buscador de grupo no te lleva a la puerta, y las piedras de encuentro no invocan: hay que ir andando o con invocación de brujo.</span></div>'
            '<div class="tile"><strong>Sin mapa ni diario</strong><span>Las nuevas no tienen mapa, hay jefes secretos y el botín está oculto hasta que cae por primera vez. Prepárate antes de entrar.</span></div></div>'
            '<div class="divider"><h2>Las nuevas, de cerca</h2></div><table class="keys">'
            '<tr><th>Ciudad de Dalaran</th><td>Compacta. Las dos facciones entran por las alcantarillas; la Horda tiene una cadena de misiones para conseguir la llave.</td></tr>'
            '<tr><th>Excavación de Whelgar</th><td>En los Humedales: hierba alta y emboscadas de raptores.</td></tr>'
            "<tr><th>Bastión Krol'dok</th><td>Ogros, en Riverglades (Claro Fluvial).</td></tr>"
            '<tr><th>Bastión Faucenegra</th><td>Más grande que Profundidades de Roca Negra, en la antigua entrada de Azshara. Pensada para seguir valiendo a nivel 60.</td></tr>'
            '<tr><th>Salón de los Feudales</th><td>Bajo Forjaz, pero no es solo de la Alianza.</td></tr></table>'
            '<div class="divider"><h2>Bandas</h2></div><table class="keys">'
            '<tr><th>Al salir</th><td>Ninguna. Hay tiempo para subir y equiparse.</td></tr>'
            '<tr><th>9 dic</th><td>Cavernas del Túmulo (10 jugadores), Cima Hyjal (20) y Guarida de Onyxia (40). Onyxia conserva su attunement (por personaje); las otras dos se entran sin cadena. <a href="../bandas-forever/">Dónde están y la cadena de Onyxia</a>.</td></tr>'
            '<tr><th>Cómo serán</th><td>Cada fase trae una banda de 10 y otra de 20; las de 40, de vez en cuando. Una sola dificultad y sin grupos mixtos de facción.</td></tr>'
            '<tr><th>Primavera 2027</th><td>Dos bandas nuevas, de 10 y de 20 jugadores, y dos mazmorras más.</td></tr>'
            '<tr><th>Verano 2027</th><td>Una banda clásica renovada, otra nueva y dos mazmorras más.</td></tr></table>'
            + fuentes(('Blizzard: lo que trae Forever', BLIZZ_LANZ), ('Blizzard: repaso a fondo', BLIZZ_REPASO), ('AlterTime: más datos de Blizzard (8-10)', 'https://www.youtube.com/watch?v=VXRsY5iRkLA'),
                      ('AlterTime: attunements', 'https://www.youtube.com/watch?v=1puQ3jJRD_w'), ('Warcraft Tavern: mazmorras', WT + 'dungeons/')))


# ---------- Profesiones ----------
# Van 15-10: «muy pobre». Rehecha: por qué importan, las 12 una a una, la pesca a fondo y qué elegir según lo que quieras hacer.
# Lo general de cada profesión es como en Classic; lo propio de Forever sale de research/forever-subir-nivel.md (beta, puede cambiar).
POR_QUE = [
    ('inv_misc_coin_01', 'Dinero de verdad', 'En Forever lo caro es la equitación: 100 de oro a nivel 40 y 1.000 a nivel 60. Recolectar mientras subes y vender en la subasta es la forma más directa de pagarla sin farmear.'),
    ('trade_alchemy', 'Bandas y PvP', 'Las primeras bandas abren el 9 de diciembre. Frascos, pociones, encantamientos, bombas y comida marcan la diferencia, y quien los fabrica no depende de nadie.'),
    ('spell_fire_fire', 'La acampada', 'Cada profesión tiene tres objetos de campamento: el primero se aprende con 20 de habilidad (la hoguera básica de Cocina, con 1) y los mejores salen de planos que sueltan los jefes de mazmorra. Junto a la hoguera dan beneficios de una hora.'),
    ('inv_misc_book_09', 'Legacy', '18 de los 65 puntos de Legacy salen de las profesiones (150, 225 y 300 en las seis de fabricación), y tienen un árbol entero de ventajas para toda la cuenta.'),
    ('inv_misc_bag_10', 'Recompensas propias', 'Vuelven los Waylaid Supplies: cajas de encargo que dan experiencia, dinero y premios. Y al llegar a 300 te llevas un título para toda la cuenta.'),
    ('inv_misc_food_15', 'Ir sobrado', 'Vendas para no parar a comer, comida que da experiencia, tus propios consumibles… Subir con profesiones es más rápido y más cómodo.'),
]
# (icono, nombre, nombre del juego, qué hace, va con, ideal para)
RECOLECCION = [
    ('trade_herbalism', 'Herboristería', 'Herbalism', 'Recoges plantas por todo el mundo. Las ves en el minimapa y se venden siempre bien. En la acampada aporta una vela de incienso que da intelecto.', 'Alquimia y Primeros auxilios (las pociones de sanación llevan hierbas)', 'Quien quiera pociones y frascos, y dinero fácil mientras sube.'),
    ('trade_mining', 'Minería', 'Mining', 'Sacas mineral y piedra de las vetas y lo fundes en lingotes. Las vetas buenas son muy codiciadas.', 'Herrería e Ingeniería', 'Guerreros y paladines (Herrería) y cualquiera que vaya a hacer PvP (Ingeniería).'),
    ('inv_misc_pelt_wolf_01', 'Desuello', 'Skinning', 'Despellejas a las bestias que matas: cuero y pieles. Casi no te desvías, porque ya las estás matando.', 'Peletería', 'Cazadores, druidas y pícaros, y la mejor para ganar dinero subiendo.'),
]
FABRICACION = [
    ('trade_alchemy', 'Alquimia', 'Alchemy', 'Pociones de maná, elixires y, a nivel alto, frascos y transmutaciones. En Forever ya no hace las pociones de sanación: pasan a Primeros auxilios. En la acampada coloca un laboratorio de alquimia.', 'Herboristería', 'Bandas: frascos y elixires para ti y tu grupo. Muy rentable.'),
    ('trade_blacksmithing', 'Herrería', 'Blacksmithing', 'Armas y armadura de malla y placas, piedras de afilar y contrapesos. En la acampada pone una piedra de afilar que da poder de ataque.', 'Minería', 'Guerreros y paladines, sobre todo tanques.'),
    ('trade_engraving', 'Encantamiento', 'Enchanting', 'Encantas el equipo (más estadísticas para siempre) y desencantas lo que no te sirve para sacar materiales.', 'Sastrería', 'Quien quiera equipo al máximo; muy buscada en bandas.'),
    ('trade_engineering', 'Ingeniería', 'Engineering', 'Bombas, granadas, artilugios, gafas y trastos. Mantiene sus especializaciones gnómica y goblin.', 'Minería', 'PvP sin discusión: aturdir con una granada gana duelos.'),
    ('trade_leatherworking', 'Peletería', 'Leatherworking', 'Armadura de cuero y malla, kits de armadura y bolsas especiales. Su bastidor para pieles de campamento es necesario para sus recetas más avanzadas.', 'Desuello', 'Cazadores, druidas, pícaros y chamanes.'),
    ('trade_tailoring', 'Sastrería', 'Tailoring', 'Armadura de tela y, sobre todo, bolsas: todo el mundo las compra. La tela sale de los enemigos humanoides. En la acampada planta un estandarte de facción que da espíritu.', 'Encantamiento', 'Magos, brujos y sacerdotes.'),
]
SECUNDARIAS = [
    ('inv_misc_food_15', 'Cocina', 'Cooking', 'En Forever casi toda la comida da un 5 % más de experiencia por enemigo, además de estadísticas (visto en la beta). Y la Cocina es la base de la acampada: su lumbre pasa a ser la hoguera básica, y los cocineros fabrican hogueras mejoradas en las que caben de 5 a 10 objetos.', 'Todo el mundo, desde el nivel 5.'),
    ('spell_holy_sealofsacrifice', 'Primeros auxilios', 'First Aid', 'La gran novedad: en Forever fabrica las pociones de sanación, que ya no son de Alquimia. Además de vendas, hace cataplasmas contra enfermedades, torniquetes contra sangrados y antídotos. Mira su sección más abajo.', 'Todo el mundo, y más que nunca las clases sin curación propia (guerreros y pícaros).'),
    ('trade_fishing', 'Pesca', 'Fishing', 'Mira la sección siguiente: da para mucho.', 'Todo el mundo, en los ratos muertos.'),
]
# Primeros auxilios en Forever (cliente de la beta, recogido por Wowhead / Icy Veins / Zockify el 15-10). (poción, habilidad · componentes)
POCIONES = [
    ('Minor Healing Potion', '55 · Empty Vial, Mild Spices, Peacebloom'),
    ('Lesser Healing Potion', '85 · Empty Vial, 2 Mild Spices, Briarthorn'),
    ('Healing Potion', '135 · Leaded Vial, Hot Spices, Bruiseweed'),
    ('Greater Healing Potion', '155 (manual) · Leaded Vial, 3 Hot Spices, Liferoot'),
    ('Superior Healing Potion', '215 (manual) · Crystal Vial, Soothing Spices, Sungrass'),
    ('Major Healing Potion', '275 (manual) · Crystal Vial, 3 Soothing Spices, Golden Sansam'),
]
PA_NUEVO = [
    ('spell_nature_nullifydisease', 'Cataplasmas', 'Curan enfermedades. Cuatro rangos (Simple, Clever, Superior y Powerful). No se usan en combate.'),
    ('ability_rogue_rupture', 'Torniquetes', 'Detienen los sangrados. Tres rangos (Woolen, Leather y Surgical). No se usan en combate.'),
    ('spell_nature_nullifypoison', 'Antídotos', 'Contra venenos, con rangos nuevos hasta el Powerful Anti-Venom. Estos sí se usan en combate.'),
    ('inv_misc_bandage_12', 'Dense Runecloth Bandage', 'Venda nueva a 300 de habilidad: cura 3.400 en 8 segundos. Se hace con dos Heavy Runecloth Bandage.'),
    ('spell_fire_fire', 'Para la acampada', 'First Aid Kit (aguante para los que se sientan cerca; no se suma a Palabra de poder: entereza), Toxin Study (140) y Plague Doctor\x27s Laboratory (300).'),
]
# Objetos de acampada por profesión (AlterTime, vídeo YxRg2cUuLOM, beta, ~4-10-2026). (profesión, rango 1, rango 2, rango 3)
CAMPAMENTO = [
    ('Cocina', 'Hoguera básica: caben 3 objetos', 'Hoguera de oficial: caben 5, y su Festín de cocinitas da aguante', 'Hoguera de experto: caben 10'),
    ('Primeros auxilios', 'Equipo de primeros auxilios: más aguante (no se suma a Entereza)', 'Estudio de toxinas: pociones de sanación y antídotos', 'Laboratorio del doctor de la peste: pociones y cataplasmas'),
    ('Pesca', 'Cuenco con pescado: +8 % a todas las estadísticas (no se suma a Bendición de reyes)', 'Expositor de pesca: pescar peces inusuales', 'Cabaña de pesca: peces poco comunes'),
    ('Alquimia', 'Pozo de maná: más regeneración de maná', 'Fermentador: crear componentes', 'Laboratorio de alquimia: recetas avanzadas'),
    ('Herrería', 'Rueda de afilar: más fuerza (no se suma al tótem Fuerza de la Tierra)', 'Yunque para usar en el campamento', 'Forja del maestro: recetas avanzadas'),
    ('Encantamiento', 'Laúd encantado: más armadura, estadísticas y resistencias (no se suma a Marca de lo Salvaje)', 'Recuperador arcano: desencantar con más provecho', 'Forja arcana: recetas avanzadas'),
    ('Ingeniería', 'Robot de componentes: vende componentes', 'Robot de reparaciones: vende y repara', 'Banco de trabajo de anarquista: recetas avanzadas'),
    ('Peletería', 'Tienda de campaña: experiencia de descanso (hasta un 5 % de nivel)', 'Bastidor para pieles: crear componentes', 'Máquina de coser: recetas avanzadas'),
    ('Sastrería', 'Estandarte de facción: más espíritu (no se suma a Espíritu divino)', 'Rueca: crear componentes', 'Telar: recetas avanzadas'),
    ('Herboristería', 'Vela de incienso: más intelecto (no se suma a Intelecto Arcano)', 'Invernadero: plantas semillas y crecen hierbas', 'Hibridador de semillas: multiplica y combina semillas'),
    ('Minería', 'Magnetita: más poder de ataque cuerpo a cuerpo (no se suma a Bendición de poderío)', 'Jardín de piedra: genera mena con el tiempo', 'Fundición de magma: recetas avanzadas'),
    ('Desuello', 'Silla de campamento: +2 % de golpe crítico', 'Guía de campo: rastrear bestias', 'Banco de trabajo de trampero: te da una trampa'),
]
ELEGIR = [
    ('Subir rápido y ganar dinero', 'Herboristería + Minería, o Desuello + otra de recolección. Más Cocina y Primeros auxilios.'),
    ('PvP y duelos', 'Ingeniería + Minería. Granadas, redes y artilugios ganan duelos que con la build sola se pierden.'),
    ('Bandas (PvE)', 'Alquimia + Herboristería para tus frascos, o la de fabricación de tu armadura con su recolección.'),
    ('Clases de tela', 'Sastrería + Encantamiento: la tela te cae sola y desencantas lo que no usas.'),
    ('Cuero y malla', 'Peletería + Desuello (cazador, druida, pícaro, chamán).'),
    ('Placas', 'Herrería + Minería (guerrero y paladín).'),
    ('Sin curación propia', 'Guerreros y pícaros: Primeros auxilios bien subido, porque te da tus propias pociones de sanación, vendas y antídotos.'),
    ('Si no sabes', 'Empieza con dos de recolección: no gastan dinero, dan dinero y a nivel 60 cambias una por su fabricación.'),
]


def card(icon, titulo, cuerpo, extra='', ancla=''):
    return f'<article class="prof"' + (f' id="{ancla}"' if ancla else '') + f'><img src="{ZAML}{icon}.jpg" alt=""><div><h3>{titulo}</h3><p>{cuerpo}</p>{extra}</div></article>'


def prof_id(en):
    return 'prof-' + en.lower().replace(' ', '-')


def prof_menu():
    # Van 16-10: submenú «Profesiones» del menú WoW Forever (ancla, nombre, icono).
    return [(prof_id(x[2]), x[1], ZAML + x[0] + '.jpg') for x in RECOLECCION + FABRICACION + SECUNDARIAS]


def profesiones():
    por_que = ''.join(card(i, E(t), E(d)) for i, t, d in POR_QUE)
    prof = lambda lst: ''.join(card(i, f'{E(n)} <small class="en">{E(en)}</small>', E(d),
                                    f'<p class="meta"><b>Va con:</b> {E(va)}<br><b>Ideal para:</b> {E(para)}</p>', prof_id(en)) for i, n, en, d, va, para in lst)
    sec = ''.join(card(i, f'{E(n)} <small class="en">{E(en)}</small>', E(d), f'<p class="meta"><b>Para:</b> {E(para)}</p>', prof_id(en)) for i, n, en, d, para in SECUNDARIAS)
    elegir = ''.join(f'<tr><th>{E(a)}</th><td>{E(b)}</td></tr>' for a, b in ELEGIR)
    return ('<p class="eyebrow">WOW FOREVER · PROFESIONES</p><h1>Profesiones en WoW Forever</h1>'
            '<p class="lead">En WoW Forever las profesiones no son un extra: son <strong>la mitad del juego</strong>. Pagan tus monturas, te equipan para las bandas y el PvP, '
            'dan vida a la acampada y suman puntos de Legacy para toda tu cuenta. Siguen las 12 de siempre (dos principales y las tres secundarias, con el máximo en 300), '
            'pero con más de 600 recetas nuevas. Aquí tienes qué hace cada una y cuáles te convienen.</p>' + nav_forever('profesiones') +
            '<div class="divider"><h2>Por qué son vitales</h2></div><div class="profs">' + por_que + '</div>'
            '<div class="divider"><h2>Recolección</h2></div><p class="sub">Sacan materiales del mundo. No cuestan dinero: lo dan.</p><div class="profs">' + prof(RECOLECCION) + '</div>'
            '<div class="divider"><h2>Fabricación</h2></div><p class="sub">Convierten los materiales en equipo y consumibles. Cada una va de la mano de una de recolección.</p><div class="profs">' + prof(FABRICACION) + '</div>'
            '<div class="divider"><h2>Secundarias: apréndelas todas</h2></div><p class="sub">No ocupan hueco de profesión principal. Cocina, Primeros auxilios y Pesca las puede tener cualquiera, a la vez.</p><div class="profs">' + sec + '</div>'
            '<div class="divider"><h2>Primeros auxilios: la gran novedad</h2></div>'
            '<p class="sub">En Forever, <strong>las pociones de sanación se fabrican con Primeros auxilios</strong>, no con Alquimia. Así cualquier personaje, sea de la clase que sea, puede hacerse sus propias pociones.</p>'
            '<table class="keys"><tr><th>Poción</th><td><strong>Habilidad · componentes</strong></td></tr>' + ''.join(f'<tr><th>{E(p)}</th><td>{E(c)}</td></tr>' for p, c in POCIONES) + '</table>'
            '<p class="fine">Todas comparten 2 minutos de reutilización. Las especias (Mild, Hot y Soothing Spices) se compran en los vendedores de comercio; las hierbas, con Herboristería o en la subasta. Las tres últimas recetas se aprenden con manuales.</p>'
            '<div class="profs">' + ''.join(card(i, E(t), E(d)) for i, t, d in PA_NUEVO) + '</div>'
            '<div class="divider"><h2>La pesca, a fondo</h2></div><div class="pesca">'
            f'<img src="{ZAML}trade_fishing.jpg" alt=""><div>'
            '<p>La pesca es la profesión más infravalorada del WoW, y en Forever todavía más, porque la Cocina pesa más que nunca. Esto es lo que te da:</p><ul>'
            '<li><strong>Comida buena y barata.</strong> Casi toda la comida con mejores efectos sale de pescado. Pescas, cocinas en tu hoguera y te ahorras la subasta.</li>'
            '<li><strong>Dinero.</strong> El pescado de nivel alto se vende muy bien a quien sube Cocina o prepara bandas.</li>'
            '<li><strong>Sorpresas.</strong> Además de peces salen cofres, objetos raros y materiales que no caen de otra forma.</li>'
            '<li><strong>Los ratos muertos.</strong> Mientras esperas al grupo, al barco o a que reaparezca algo, pescas. Es lo más relajante del juego.</li>'
            '<li><strong>Legacy.</strong> La ventaja «Maestro del cebo» da hasta un 50 % de probabilidad de un pez extra al pescar con cebo, para toda tu cuenta.</li></ul>'
            '<p><strong>Cómo empezar:</strong> apréndela con el instructor de pesca de cualquier ciudad, compra una caña en el vendedor de suministros y busca agua de tu nivel: '
            'en zonas de nivel alto, con poca habilidad, se te escapan los peces. Los señuelos suben tu habilidad durante un rato.</p></div></div>'
            '<div class="divider"><h2>Qué pone cada profesión en la acampada</h2></div>'
            '<p class="sub">Hacia el nivel 5 unas misiones te enseñan la acampada. Con Cocina montas la hoguera; los demás añadís un objeto cada uno. Siéntate (o fabrica) un minuto junto al fuego y te llevas los beneficios durante una hora. '
            'Cada objeto tiene tres rangos: el primero se aprende con 20 de habilidad (la hoguera básica de Cocina, con 1) y cada rango incluye lo del anterior. Busca el campamento que te convenga: con un personaje de fuerza, el del herrero.</p>'
            '<p class="sub"><strong>Datos oficiales de Blizzard (21 de octubre), rango 1 a nivel 60:</strong> botiquín, hasta +56 de aguante; pozo de maná, hasta 29 de maná cada 5 s; rueda de afilar, hasta +34 de fuerza; laúd encantado, hasta +260 de armadura, +13 a todas las estadísticas y +22 a todas las resistencias; vela de incienso, hasta +25 de intelecto; estandarte de facción, hasta +32 de espíritu (solo para tu facción). Los objetos de 140 de habilidad o más salen de mazmorras y bandas. <strong>Ojo en los reinos JcJ:</strong> los enemigos pueden encontrar tu campamento y estropeártelo, así que elige bien dónde montarlo.</p>'
            '<table class="keys camp"><tr><th>Profesión</th><td><strong>Rango 1</strong></td><td><strong>Rango 2</strong></td><td><strong>Rango 3</strong></td></tr>' + ''.join(f'<tr><th>{E(p)}</th><td>{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td></tr>' for p, a, b, c in CAMPAMENTO) + '</table>'
            '<div class="divider"><h2>El Favor del Mercader</h2></div><div class="pesca merc">'
            f'<img src="{ZAML}inv_misc_coin_02.jpg" alt=""><div>'
            '<p>Es la moneda y la reputación nuevas de las profesiones, y engancha durante toda la subida:</p><ul>'
            '<li><strong>Cajones saqueados.</strong> Los suelta cualquier enemigo y también se compran en la subasta. Cada uno pide materiales concretos (mena, tela, cuero, hierbas, polvos…): lo llenas desde la bolsa.</li>'
            '<li><strong>Campamentos de comercio.</strong> Los entregas en los campamentos de profesiones: cerca del Cruce para la Horda y en las Montañas Crestagrana para la Alianza. La primera misión da 50 de Favor y cada cajón, unos 5 más.</li>'
            '<li><strong>Intendentes de cada profesión.</strong> Con el Favor compras recetas: equipo para subir (de nivel 12 a 50), bolsas, encantamientos nuevos… Hay páginas y páginas para cada profesión.</li>'
            '<li><strong>Materiales olvidados.</strong> Muchas recetas nuevas usan materiales de Classic que antes no valían nada, así que vuelven a venderse.</li>'
            '<li><strong>Título de cuenta.</strong> El certificado de la profesión desbloquea su título para todos tus personajes (para mostrarlo hace falta 300 de habilidad).</li></ul></div></div>'
            '<div class="divider"><h2>Lo nuevo de Forever</h2></div><table class="keys">'
            '<tr><th>+600 recetas</th><td>Útiles mientras subes, no solo a nivel 60.</td></tr>'
            '<tr><th>Acampada</th><td>Cada profesión tiene tres objetos de campamento: el primero se aprende con 20 de habilidad (con los instructores o con los PNJ que presentan la acampada) y los avanzados con planos que sueltan jefes de mazmorra. '
            'En una hoguera básica caben tres objetos, uno por jugador, con una hora de reutilización compartida; las hogueras mejoradas de los cocineros admiten de 5 a 10. Para recibir los beneficios hay que sentarse junto al fuego; son variantes de los de clase y no se suman a ellos.</td></tr>'
            '<tr><th>Comida</th><td>Casi todos los platos dan ahora un 5 % más de experiencia por enemigo, además de estadísticas (visto en la beta).</td></tr>'
            '<tr><th>Ventana nueva</th><td>Buscador de recetas y un hueco propio para una bolsa de componentes.</td></tr>'
            '<tr><th>Waylaid Supplies</th><td>Vuelven las cajas de encargo de Season of Discovery: entregas materiales y te llevas experiencia, dinero y recompensas.</td></tr>'
            '<tr><th>Manuales</th><td>Manuales de recolección en las zonas de inicio para empezar desde el primer día.</td></tr>'
            '<tr><th>Títulos</th><td>Llegar a 300 en una profesión da un título para toda la cuenta.</td></tr>'
            '<tr><th>Legacy</th><td>Árbol de profesiones: Horas extra (+20 % de probabilidad de subir), Cosecha abundante (más materiales escasos), Regateo (−10 % en vendedores), '
            'Maestro cocinero, Maestro del cebo, Estudio dedicado y Bonificaciones de rendimiento (más Favor del Mercader).</td></tr>'
            '<tr><th>Magos</th><td>Tienen además un sistema propio de Investigación, aparte de las profesiones.</td></tr>'
            '<tr><th>¿Joyería e Inscripción?</th><td>En la beta hay pistas: un aprendiz de joyero en Dalaran que te dice que vuelvas más adelante, un escriba en Durotar igual y la habilidad de Inscripción ya aparece en la hoja de personaje. Blizzard no lo ha anunciado: si llegan, será en 2027.</td></tr></table>'
            '<div class="divider"><h2>¿Cuáles elijo?</h2></div><table class="keys">' + elegir + '</table>'
            '<div class="prepare" style="margin-top:22px"><h3>Consejos para no arrepentirte</h3><ol>'
            '<li>Aprende tus dos principales en cuanto llegues a la primera ciudad y recolecta desde el nivel 1: luego no apetece volver atrás.</li>'
            '<li>No subas una de fabricación pronto si vas justo de dinero: guarda los materiales o véndelos y súbela con calma a partir del 40.</li>'
            '<li>Cocina y Primeros auxilios, siempre. Cuestan poco y se notan cada día.</li>'
            '<li>Piensa en tu cuenta: con el Legacy compensa que tus personajes tengan profesiones distintas y se fabriquen cosas entre ellos.</li></ol></div>'
            '<p class="fine">Lo propio de Forever sale de Blizzard y del cliente de la beta, y puede cambiar hasta el lanzamiento. '
            'Blizzard prepara otra actualización de profesiones para el verano de 2027. Lo demás funciona como en Classic.</p>'
            + fuentes(('Blizzard: la acampada (21-10)', 'https://worldofwarcraft.blizzard.com/en-us/news/24301516'), ('Blizzard: repaso a fondo de Forever (acampada y profesiones)', BLIZZ_REPASO), ('Blizzard: Legacy', BLIZZ_LEGADO),
                      ('Datos del cliente de la beta: Primeros auxilios (Icy Veins)', 'https://www.icy-veins.com/wow-forever/news/healing-potions-now-crafted-by-first-aid-in-wow-forever/'),
                      ('AlterTime: campamentos', 'https://www.youtube.com/watch?v=YxRg2cUuLOM'), ('AlterTime: Favor del Mercader', 'https://www.youtube.com/watch?v=eXl3dQa7QVo'),
                      ('AlterTime: joyería e inscripción', 'https://www.youtube.com/watch?v=MwVjNZmAGpA')))


# ---------- Legacy ----------
ARBOLES = [  # nombres del cliente en castellano (AlterTime) y valores con la ventaja al máximo (Talents Forever)
    ('Aventura', ['Buen descanso (Well Rested): el descanso se acumula un 20 % más rápido y su tope sube un 20 % (4 % por punto).',
                  'Con talento (Talented): tu primer punto de talento a nivel 5 en vez de 10. El máximo sigue en 51.',
                  'Abono de transporte (Frequent Flier): vuelos un 50 % más baratos y un 20 % más rápidos.',
                  'Emoción de la aventura (Thrill of Adventure): recuperas un 5 % de vida y maná al rematar a un enemigo en el mundo.',
                  'Guía de campo y Medicina de campo (Field Guide, Field Medicine): acampada y vendas más rápidas.',
                  'Alerta máxima (High Alert): detectas mejor a los enemigos en sigilo.']),
    ('Ingenio', ['Cuestión de honor (For Great Honor): +10 % de honor.', 'Diplomacia (Diplomat): +10 % de reputación.', 'Refuerzo (Reinforce): −40 % de desgaste al morir.',
                 'Gastronomía y Permanencia (Gourmand, Permanence): la comida y los beneficios de grupo y de la acampada duran más.',
                 'Ahorro de componentes (Reagent Economy): tus hechizos de clase dejan de pedir componentes de vendedor. Pide 11 puntos en el árbol.',
                 'Este muerto está muy vivo (The Quick and the Dead): más rápido muerto y hechizos gratis un rato al resucitar.']),
    ('Profesiones', ['Horas extra (Working Overtime): +20 % de probabilidad de subir habilidad (4 % por punto).',
                     'Cosecha abundante (Bountiful Harvest): más materiales escasos con Minería, Herboristería y Desuello.',
                     'Regateo (Bartering): −10 % en los vendedores.', 'Maestro cocinero y Maestro del cebo: platos y peces extra.',
                     'Estudio dedicado (Dedicated Study): +1 a tu profesión más baja (en la beta, una vez cada 24 horas).',
                     'Bonificaciones de rendimiento (Performance Bonus): a veces, el doble de Favor del Mercader al entregar cajones.']),
]


def legacy():
    arboles = ''.join(f'<div class="fact"><h3>{E(n)}</h3><ul>' + ''.join(f'<li>{E(x)}</li>' for x in items) + '</ul></div>' for n, items in ARBOLES)
    return ('<p class="eyebrow">WOW FOREVER · PROGRESO DE CUENTA</p><h1>Legacy</h1>'
            '<p class="lead">El Legacy es lo más nuevo de Forever: <strong>ventajas que comparten todos los personajes de tu cuenta</strong>. '
            'Ganas puntos con retos en cualquier personaje y cada uno los gasta en sus propios árboles. Así, cada personaje nuevo sube más rápido que el anterior.</p>'
            + nav_forever('legacy') +
            '<div class="tfo-stats"><div><b>65+</b><span>puntos que se pueden ganar</span></div><div><b>16</b><span>puntos por personaje al salir</span></div>'
            '<div><b>3</b><span>árboles</span></div><div><b>Tecla Y</b><span>se abre con tu primer punto</span></div></div>'
            '<div class="divider"><h2>Cómo se ganan los puntos</h2></div><table class="keys">'
            '<tr><th>Clases (27)</th><td>Llegar por primera vez a nivel 25, 45 y 60 con cada clase.</td></tr>'
            '<tr><th>Profesiones (18)</th><td>Llegar a 150, 225 y 300 en Alquimia, Herrería, Encantamiento, Ingeniería, Peletería y Sastrería.</td></tr>'
            '<tr><th>JcJ (12)</th><td>Rangos 3, 7, 10, 13 y 14; exaltado con las cuatro reputaciones de campos de batalla; semanas 4, 7 y 10 de la temporada.</td></tr>'
            '<tr><th>Mazmorras (3)</th><td>Completar todas las mazmorras de nivel 15-25, todas las de 26-45 y todas las de 46-60.</td></tr>'
            '<tr><th>Bandas (3)</th><td>Matar a Onyxia, a los 13 jefes de Cima Hyjal y a los 8 de las Cavernas del Túmulo.</td></tr>'
            '<tr><th>Aventura (2)</th><td>Completar el mapa del mundo y la cadena de Lord Valthalak.</td></tr></table>'
            '<p class="fine">Son 65 puntos al salir (12 más cuando llegue Hardcore). Un solo personaje puede ganar 29, pero solo puedes gastar 16 por personaje, así que elige. Las profesiones de recolección y la Cocina no dan puntos. Los puntos se pueden reiniciar (en la beta costaba 10 de oro; sin confirmar para el lanzamiento).</p>'
            '<p class="fine">Recompensas por los puntos que ganas, los gastes o no: con 15, el juguete Replica Ironforge Air Rifle; con 25, la mascota Spectral Bear Cub; con 40, el Spectral Bear Tabard; con 55, la montura épica Reins of the Spectral Bear. Se recogen con el posadero Wiley en Trinquete. Sin los 12 retos de JcJ te quedas en 53, sin la montura. Visto en la beta: Blizzard no ha publicado la lista.</p>'
            '<div class="divider"><h2>Los tres árboles</h2></div><div class="facts tres">' + arboles + '</div>'
            '<div class="prepare" style="margin-top:22px"><h3>Por dónde empezar</h3><p>Con tu primer personaje, <strong>Horas extra</strong>: subes antes las profesiones, que además dan más puntos. '
            'Con los siguientes, <strong>Con talento</strong> y <strong>Buen descanso</strong> son las que más se notan al subir. Para JcJ, <strong>Cuestión de honor</strong>; si farmeas, <strong>Cosecha abundante</strong>.</p>'
            '<div class="actions"><a class="btn gold" href="../calculadora/">La calculadora ya incluye el Legacy</a></div></div>'
            + fuentes(('Blizzard: el Legado', BLIZZ_LEGADO), ('Blizzard: repaso a fondo de Forever', BLIZZ_REPASO), ('Talents Forever: Legacy', TF + 'legacy')))


import cambios_beta
PAGINAS = [
    ('cambios', lambda: cambios_beta.cambios(nav_forever), 'Cambios de la beta de WoW Forever: nerfs y mejoras por clase | Muchamiel',
     'Todos los cambios de cada parche de la beta de WoW Forever por clase y en castellano: mejoras, nerfs y arreglos, según las notas oficiales de Blizzard.'),
    ('lanzamiento', lanzamiento, 'WoW Forever: fecha y hora de lanzamiento, ediciones y novedades | Muchamiel',
     'WoW Forever sale el 4 de noviembre (00:00 del 5 en España) con nivel 60 desde el primer día. Fechas clave, reserva de nombres, ediciones y todo lo nuevo.'),
    ('pagar-menos', pagar_menos, 'Cuánto cuesta jugar a WoW Forever y cómo pagar menos | Muchamiel',
     'Precios de WoW Forever: suscripción de 1, 3, 6 y 12 meses, tarjeta de 60 días y packs Heroico, Épico y Colección. Cuál te sale más barata según cómo juegues.'),
    ('subir-nivel', subir_nivel, 'Guía para subir de nivel en WoW Forever del 1 al 60 | Muchamiel',
     'Cómo subir rápido del 1 al 60 en WoW Forever: consejos, zonas por nivel, monturas, acampada y viajes nuevos.'),
    ('builds-60', builds_60, 'Builds de nivel 60 de WoW Forever para las nueve clases | Muchamiel',
     'Las builds de nivel 60 más populares de cada clase en WoW Forever, con sus 51 puntos de talento y las habilidades nuevas de cada clase.'),
    ('mazmorras', mazmorras, 'Mazmorras de WoW Forever: niveles y las 9 nuevas | Muchamiel',
     'Todas las mazmorras de WoW Forever con su nivel: las nueve nuevas (Salón de los Feudales, Ciudad de Dalaran, Bancal del Creador…) y el calendario de bandas.'),
    ('profesiones', profesiones, 'Profesiones en WoW Forever: qué cambia y cuáles elegir | Muchamiel',
     'Profesiones de WoW Forever: más de 600 recetas nuevas, objetos de campamento, Legacy de profesiones y cuáles elegir para subir y para PvP.'),
    ('legacy', legacy, 'Legacy de WoW Forever: ventajas de cuenta y cómo ganar puntos | Muchamiel',
     'Qué es el Legacy de WoW Forever, cómo se ganan sus puntos y las ventajas de sus tres árboles: Aventura, Ingenio y Profesiones.'),
]

CSS = cambios_beta.CSS + '''
.profs{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}
.prof{display:flex;gap:14px;align-items:flex-start;padding:18px;border:1px solid #2c3444;border-left:3px solid #c99a3c88;border-radius:8px;background:#0f141d}
.camp td{font-size:14px}.merc{border-color:#c99a3c88;background:linear-gradient(120deg,#2a2210,#0b1018 70%)}.merc>img{border-color:#c99a3c}.merc strong{color:#ffe7a6}@media(max-width:700px){table.camp,table.camp tbody,table.camp tr,table.camp th,table.camp td{display:block;width:auto!important}table.camp tr{border-bottom:1px solid #3b3222;padding:6px 0}table.camp tr:first-child{display:none}}.prof h3 small.en{font-size:.62em}.prof img{width:48px;height:48px;border-radius:8px;border:2px solid #c99a3c;flex:none}.prof h3{margin:0 0 6px;color:var(--gold);font-size:18px}
.prof p{margin:0 0 8px;color:#dfe5ee}.prof .meta{margin:0;font-size:13.5px;color:#b6c0d0}.prof .meta b{color:#ffe7a6}
.pesca{display:flex;gap:20px;align-items:flex-start;padding:22px 24px;border:1px solid #3a6b8a;border-radius:12px;background:linear-gradient(120deg,#0d2233,#0b1018 70%)}
.pesca>img{width:72px;height:72px;border-radius:12px;border:2px solid #6fb3d9;flex:none}.pesca ul{padding-left:20px;margin:8px 0 12px}.pesca li{margin:7px 0}.pesca strong{color:#bfe3f7}
@media(max-width:600px){.pesca{flex-direction:column}.profs{grid-template-columns:1fr}}
.fnav{justify-content:center;gap:6px;margin:0 0 22px}.fnav a[aria-current]{border-color:var(--gold);color:var(--gold)}
table.zonas th{white-space:nowrap}table.zonas tr.nueva td{color:#ffe7a6}
.build60 img{object-fit:cover}.b60{margin:6px 0 10px;padding-left:20px}.b60 li{margin:5px 0}.b60 b{display:inline-block;min-width:66px;color:#ffe7a6}
.b60 a{margin-left:6px;font-size:13px;color:#c9b58a}.facts.tres{grid-template-columns:repeat(3,1fr)}
@media(max-width:900px){.facts.tres{grid-template-columns:1fr}}
@media(max-width:600px){table.keys{table-layout:fixed;min-width:0}table.keys th,table.keys td{white-space:normal;overflow-wrap:anywhere;padding:8px 7px}table.keys th{width:32%}table.zonas{font-size:13px}table.zonas th{width:22%}table.zonas tr:first-child th{width:auto}}
'''


def build(page):
    for slug, fn, title, desc in PAGINAS:
        page(slug, title, desc, fn())
