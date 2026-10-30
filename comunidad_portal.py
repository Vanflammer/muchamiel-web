"""Secciones de comunidad: Muchamiel, Noticias (vídeos de YouTube), Sorteos, torneo, directo automático y SEO.
Orden: crear_portal → completar_portal → embellecer_portal → comunidad_portal.py (este llama a oficializar_portal.run()).
Datos consultados el 09-10-2026 en sus perfiles públicos; actualiza STATS y VIDEOS a mano cuando cambien."""
from pathlib import Path
import re, html, json, shutil
import actualizar_talentos  # Van 16-10: talentos al día con talentsforever.com, antes de que datos_clases lea research/talents.json
_AQUI = Path(__file__).parent
try:
    actualizar_talentos.main(['--research', str(_AQUI / 'research' / 'talents.json')])
except Exception as e:
    print('AVISO: no se pudieron bajar los talentos de talentsforever.com; sigo con los de research/talents.json:', e)
from crear_portal import dist, classes
from completar_portal import package
import oficializar_portal as of

E = html.escape
SITE = 'https://muchamielwow.github.io/'  # desde el 14-10; antes wow-forever-guia.pages.dev (bloqueos de LaLiga a Cloudflare)
TWITCH, KICK, YT = 'https://www.twitch.tv/muchamiel', 'https://kick.com/muchamiel', 'https://www.youtube.com/@muchamiel'
YT_SUB = YT + '?sub_confirmation=1'
DISCORD = 'https://discord.gg/U8VkN5yXJ8'
AVATAR = 'https://static-cdn.jtvnw.net/jtv_user_pictures/193d41e2-6ed4-4f43-b1a7-ba2b0f8f297c-profile_image-300x300.png'
TFO_RULES = 'https://raider.io/events/the-forever-open/rules-regulations-code-of-conduct'
FECHA_DATOS = '9 de octubre de 2026'

EMAIL = 'muchamielcc@gmail.com'  # contacto público de su canal de YouTube
# Van 16-10: el correo no se escribe entero en la web (los bots lo recogen); un botón con sobre lo enseña al pulsarlo.
CORREO_DATA = 'data-correo="' + EMAIL.replace('@', '|') + '"'
MAIL_SVG = '<svg class="rrss-icon" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 6.5 8.5-6.5"/></svg>'
PATREON = 'https://www.patreon.com/Muchamiel'
DONAR = 'https://streamelements.com/muchamiel-f842c/tip'  # el mismo enlace de donaciones que usa en Twitch
DISCORD_CREADORES = 'https://discord.gg/U8VkN5yXJ8'
# (marca, sector, año, tipo, enlace, código, descuento, ¿código vigente en sus últimos vídeos?) — sacado de sus descripciones y paneles.
OVERGEAR = 'https://overgear.com/games/wow/coaching?utm_source=youtube&utm_medium=influence&utm_content=muchamiel10&utm_campaign=091026'  # enlace de su vídeo de addons (09-10-2026)
BRANDS = [
    ('Overgear', 'Coaching de WoW: Classic, Forever y Retail', '2026', 'Código y enlace', OVERGEAR, 'MUCHAMIEL10', '10 %', True),
    ('LagZapper', 'Gaming · juega sin lag', '2026', 'Código y enlace', 'https://www.lagzapper.com/?cid=307', 'muchamiel', '35 %', True),
    ('Instant Gaming', 'Videojuegos y tiempo de juego de WoW', '2026', 'Enlace de afiliado', 'https://www.instant-gaming.com/es/?igr=muchamiel', None, None, True),
    ('Eldorado.gg', 'Marketplace gaming', '2026', 'Código', 'https://www.eldorado.gg/', 'MUCHAMIEL', '5 %', True),
    ('Pitido Final', 'Camisetas', '2026', 'Código', 'https://pitidofinal.com/', 'MUCHAMIEL', '15 %', True),
    ('Knoweats', 'Comida saludable a domicilio', '2025–2026', 'Código y enlace', 'https://knoweats.com/?sca_ref=9715047.Q28PkIIwKGDev&utm_source=afiliacion&utm_medium=web&utm_campaign=afiliado-9715047', 'MUCHAMIEL', '20 €', True),
    ('Planeta DeAgostini', 'Coleccionables · Rey Exánime', '2025', 'Vídeo patrocinado', None, None, None, False),
    ('Prozis', 'Nutrición deportiva', '2025', 'Código', None, None, None, False),
    ('Wetaca', 'Comida a domicilio', '2024', 'Código', None, None, None, False),
]
MEDIA = [('79,1 K', 'suscriptores en YouTube'), ('73 M', 'visualizaciones en YouTube'), ('35,6 K', 'seguidores en Twitch'), ('8,4 K', 'seguidores en Kick'),
         ('460 K', 'me gusta en TikTok'), ('14,2 K', 'seguidores en TikTok'), ('20–110 K', 'visitas por vídeo de WoW Forever'), ('A diario', 'directos en Twitch y Kick')]

STATS = dict(yt_subs=83100, yt_goal=100000, tw_subs=1837, tw_goal=2000, tw_followers=35663, kick_followers=8470)  # Kick: API de Kick, 16-10

# Bios copiadas de sus perfiles (09-10-2026).
BIOS = [
    ('Twitch', TWITCH, '35.663 seguidores', 'Hago streams y vídeos de WOW Hardcore, Classic y algo de Retail. Mil gracias por verme y estar aquí apoyando.'),
    ('YouTube', YT, '79,1 K suscriptores · 73 M de visualizaciones', 'World of Warcraft Hardcore, Classic y Retail. Stream todos los días en Kick y Twitch. Mil gracias por verme.'),
    ('Kick', KICK, '8,4 mil seguidores', 'Hago stream de World of Warcraft Classic y de otras cosas que me apetecen. Puedes seguir mis vídeos en YouTube.'),
    ('TikTok', 'https://www.tiktok.com/@muchamielwow', '14,2 K seguidores · 460 K me gusta', 'Creador de contenido de WOW CLASSIC. Hago vídeos y streams en YouTube y Twitch.'),
    ('X / Twitter', 'https://twitter.com/Muchamiel_', '3.588 seguidores · «la red social que más uso»', 'Que la suerte me pille trabajando. El clavo no va a entrar dándole flojo. OSS'),
    ('Instagram', 'https://www.instagram.com/muchamiel_/', '4.099 seguidores', 'World of Warcraft Classic MUCHAMIEL'),
]

# (id, fecha ISO, duración, título original). Tipo: live, video o short.
VIDEOS = {
'live': [
    ('brARJ3NZ9Hw', '2026-10-08', '9:11:52', 'WOW FOREVER BRUJO FULL BIS HOY DUELOS A CD POV WINNER💥TORNEO PVP días 17/18 oct'),
    ('4iE8eD-zY5g', '2026-10-07', '9:41:31', 'WOW FOREVER MEGABASTÓN BRUJO CASI FULL POV WINNER💥TORNEO PVP días 17/18 octubre'),
    ('Kn5kOqsqGIM', '2026-10-06', '', 'WOW FOREVER PONGO AL BRUJO BIS FULL TRYHARD BRUJO WINNER💥TORNEO PVP 17/18 octubre'),
    ('LhlecG7F-64', '2026-10-05', '', 'WOW FOREVER PONGO AL BRUJO BIS FULL TRYHARD BRUJO WINNER💥TORNEO PVP 17/18 octubre'),
    ('pG-gHoh9BSs', '2026-10-04', '', 'WOW FOREVER HOY LVL 30 FULL TRYHARD BRUJO WINNER💥TORNEO PVP'),
    ('AmCPKSYD244', '2026-10-02', '11:00:16', 'SORTEO EPIC EDITION GRATIS💥WOW FOREVER SUBIMOS LVL 30 FULL TRYHARD BRUJO WINNER'),
    ('5IbRn0_oDs0', '2026-09-30', '', 'WOW FOREVER BRUJO WINNER POV TORNEO PVP💥HORDA EN LA BETA💥 17/18 TORNEO PVP'),
    ('tmxvlKgoClk', '2026-09-29', '6:31:36', 'REGALO HOY 2 EPIC EDITION💥WOW FOREVER BRUJO WINNER POV TORNEO PVP'),
    ('ibcEe_3NxIQ', '2026-09-27', '', 'WOW FOREVER BETA PREPARAMOS TORNEO PVP💥HORDA EN LA BETA ¿PERO EL 5 DE NOVIEMBRE?'),
],
'video': [
    ('itFMC7f5rt4', '2026-10-09', '12:53', 'TOP 10 ADDONS que NECESITAS en WOW FOREVER💥'),
    ('BcFuAID0iRQ', '2026-10-08', '9:49', '¿TANKS Y HEALS? EL MAYOR PROBLEMA DE WOW FOREVER💥NERFEO A LAS MAZMORRAS'),
    ('pP8WmdG9Ans', '2026-10-07', '15:35', 'WOW FOREVER: LA MAZMORRA DE DALARAN YA ESTÁ DISPONIBLE💥 VUELVEN LOS ATTUNEMENTS AL WOW'),
    ('HYtu5WQ0I4E', '2026-10-06', '21:53', 'NO TODO VALE!! LA RAZA PERFECTA PARA TU CLASE EN WOW FOREVER💥LO MEJOR PARA PVE Y PVP'),
    ('h6mv-cvZYb8', '2026-10-05', '10:01', 'ASÍ SON LAS PROFESIONES EN WOW FOREVER💥EL NUEVO SISTEMA CAMBIA EL JUEGO POR COMPLETO'),
    ('FMdg_Wu4mTE', '2026-10-04', '33:07', 'BLIZZARD MUESTRA EL FUTURO DE WOW FOREVER💥ESTÁN ESCUCHANDO A LA COMUNIDAD'),
    ('e0AkQGEiQec', '2026-10-03', '29:41', '¿QUÉ CLASE DEBERÍAS JUGAR EN WOW FOREVER?💥GUÍA DEFINITIVA TIER LIST COMPLETA PVE y PVP'),
    ('HGkKjofOtMw', '2026-10-01', '15:05', 'CAMBIOS AL DRUIDA EN WOW FOREVER💥SE CONVIERTE EN UNA DE LAS MEJORES CLASES DEL WOW'),
    ('a4deLbzfgZ8', '2026-10-01', '17:04', 'CAMBIOS AL CAZADOR EN WOW FOREVER💥LA CLASE MÁS FUERTE DE LA BETA, DA MIEDO'),
    ('UxwU5JrtiZM', '2026-09-28', '8:03', 'BLIZZARD SE DESTRUYE A SI MISMA (OTRA VEZ)💥EL PRODUCTOR DEL WOW ACABA ÉL CON SU CARRERA'),
    ('TOzi1RNyxzQ', '2026-09-26', '36:38', 'ME CAMBIO A LA HORDA EN WOW FOREVER BETA POR ESTO'),
    ('iaWFM_seM0E', '2026-09-24', '10:21', 'TU WOW FOREVER ESTÁ MAL CONFIGURADO💥HAZ ESTO Y CAMBIARÁ TU JUEGO ¡SIN ADDONS!'),
    ('7Zql7gj87H0', '2026-09-23', '12:01', 'SE HA DESCUBIERTO UNA NUEVA CLASE EN WOW FOREVER'),
    ('CbUH__IP5us', '2026-09-22', '15:25', 'WOW FOREVER SERÁ HORDA O ALIANZA?💥SIGUE LA GUERRA ENTRE XOKAS Y RUBIUS'),
    ('hsioBUV0IrQ', '2026-09-19', '14:55', 'WOW FOREVER ES MUCHO MÁS CLASSIC DE LO QUE PENSABA💥5 COSAS QUE DEBES VER YA'),
    ('OnOk6zr7UYc', '2026-09-17', '17:28', 'ALEXELCAPO HABLA DE WOW FOREVER💥ASÍ VE EL WOW ALGUIEN QUE NUNCA HA JUGADO'),
    ('J38sFTXV3jo', '2026-09-16', '17:50', 'XOKAS VA A CREAR EL MAYOR EVENTO DE WOW FOREVER IRL💥¿REALITY SHOW DEL WOW?'),
    ('YDL-INZBAi0', '2026-09-16', '29:08', 'WOW FOREVER: QUÉ RAZA ELEGIR PARA PVE y PVP💥LAS RACIALES IMPORTAN MUCHO MÁS AHORA'),
    ('E7ig3exT98c', '2026-09-15', '12:22', 'WOW FOREVER VA A ELIMINAR LOS REINOS💥ASÍ VA A CAMBIAR WORLD OF WARCRAFT PARA SIEMPRE'),
    ('GfDl0W5HLc4', '2026-09-15', '17:42', '¿QUÉ ES WOW FOREVER?💥TODO LO QUE NECESITAS SABER SOBRE ESTE WOW CLASSIC+'),
    ('BZUyHOLiux0', '2026-09-14', '40:06', 'ASÍ SON LOS NUEVOS TALENTOS DE WOW FOREVER💥HAN ELIMINADO LOS HORRIBLES TALENTOS VIEJOS'),
],
'short': [
    ('_VVmKh9mN84', '2026-10-07', '0:24', 'BUG EN WOW FOREVER, LA NUEVA PIEDRA DE HOGAR'),
    ('0eNpCYLXTfE', '2026-10-06', '0:38', 'LA MAYOR CAZADA DE WOW FOREVER'),
    ('PoCbU9G5wC8', '2026-10-06', '', 'SKATE EN BLACKROCK EN WOW FOREVER'),
    ('DqZr5eUVuqg', '2026-10-04', '', 'TIER LIST DE HEALS EN WOW FOREVER (FASE BETA CÁBALA)'),
    ('g9nPQSRMlaI', '2026-10-04', '', 'TIER LIST DE TANKS EN WOW FOREVER (FASE BETA CÁBALA)'),
    ('_pBWomRHSOc', '2026-09-29', '', 'LE TRADEAN A STREAMER 400 OROS EN WOW FOREVER BETA'),
    ('OXiv68a0e88', '2026-09-23', '0:31', 'LA MEJOR ESCENA DE WOW FOREVER, ESTO SI ES MMO'),
    ('1Bv08WuJorE', '2026-09-19', '0:37', 'NO ME LO PUEDO CREER!! COMPRAN ORO EN LA BETA WOW FOREVER'),
    ('MTiyfUS2ldM', '2026-09-18', '0:43', 'RUBIUS ME DICE ESTO, WOW FOREVER VA A SER INCREIBLE'),
]}
# Top 10 de su vídeo «TOP 10 ADDONS que NECESITAS en WOW FOREVER» (09-10-2026), en su orden. Nombres y enlaces comprobados en CurseForge ese día.
# (nombre, slug de CurseForge, icono, para qué, lo que dice Muchamiel)
ADDONS = [
    ('MinimapButtonButton', 'minimapbuttonbutton', 'inv_misc_spyglass_03', 'Interfaz',
     'Recoge todos los botones de addons que rodean el minimapa en un solo botón.', '“¿Estáis cansados de que esto parezca la oreja de un metalero?” Muy necesario para no tenerlo todo petado.'),
    ('Talents Forever', 'talents-forever', 'inv_misc_book_11', 'Talentos',
     'La web talentsforever.com dentro del juego (/tf): planifica tu build sin gastar puntos, prueba las populares y ve qué habilidades aprendes en cada nivel.', 'Un addon superinteresante y superbonito: pruebas tus cositas y le pasas una captura a tu colega.'),
    ('GearQuest Forever', 'gearquest-forever', 'inv_helmet_03', 'Equipo',
     'Clic derecho en cualquier hueco del personaje: las mejores mejoras para tu clase, especialización y nivel (1–60) y de dónde salen.', 'Saber los posibles BiS mientras subes, ranura a ranura. Le falta algo de PvP, pero está en beta.'),
    ('Attune', 'attune', 'inv_misc_key_03', 'Mazmorras y bandas',
     'Las cadenas de misiones y requisitos de cada mazmorra y banda, en verde lo que ya tienes. Renovado para Forever.', 'Uno de mis favoritos de toda la historia. Vuelven los attunements al WoW.'),
    ('DungeonJournal', 'dungeonjournal', 'inv_misc_book_09', 'Mazmorras y misiones',
     'Cada mazmorra con sus jefes, su botín y todas sus misiones: dónde empiezan, dónde se entregan, de qué facción son y su cadena.', 'El mejor addon para esto, de largo. Hazme caso y descárgalo, porque esto es BiS.'),
    ('EllesmereUI', 'ellesmereui', 'inv_misc_gear_08', 'Interfaz completa',
     'Una interfaz entera por módulos: barras, placas de nombre, marcos, misiones, bolsas y más, con un editor visual para moverlo todo. Puedes importar perfiles.', 'El addon definitivo. Parece que estás jugando en 2050. Busca un perfil ya hecho y a partir de ahí lo vas ajustando.'),
    ('Whisper Messenger', 'whisper-messenger', 'inv_letter_15', 'Chat',
     'Los susurros como un chat de mensajería: lista de contactos, conversaciones e historial.', '“¿Queréis un WhatsApp en el WoW?” Para tener a mano al joyero o al encantador que te interesa.'),
    ('SkillUp Forever', 'skillup-forever', 'trade_blacksmithing', 'Profesiones',
     'Probabilidad de subir con cada receta, su coste, rutas para subir la profesión y lista de la compra.', 'Ves los porcentajes y sabes qué te sale más barato para subir tu profesión.'),
    ('Books on Map Forever', 'books-on-map-forever', 'inv_misc_book_07', 'Coleccionables',
     'Los libros de biblioteca de WoW Forever en el mapa y el minimapa; cada uno desaparece al recogerlo. Se canjean en Ventormenta o Entrañas por recompensas.', 'Ves los que te faltan por todo el mapa. Rápido y sencillo.'),
    ('Best in Deck', 'best-in-deck', 'inv_misc_ticket_tarot_furies', 'Para los ratos muertos',
     'Un roguelike de cartas al estilo Slay the Spire en una ventana del juego: mazo, reliquias y pociones por Azeroth.', 'Para los vuelos largos o mientras esperas a la gente en la mazmorra. Muy complicado y muy divertido.'),
]
MESES = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sept', 'oct', 'nov', 'dic']

CSS = '''
/* Van 16-10: un solo botón de directo; apagado en gris, en directo verde y con «VER ▸» */header.site nav a.live{border-color:#4b5363;background:linear-gradient(#232b38,#151a23);color:#aab4c4;font-weight:800;letter-spacing:.08em}
header.site nav a.live:before{content:"";display:inline-block;width:8px;height:8px;border-radius:50%;background:#6b7587;margin-right:7px;vertical-align:1px}header.site nav a.live:after{content:"";display:inline-block;margin-left:7px;border:4px solid transparent;border-top-color:currentColor;border-bottom:0;vertical-align:2px}.menu-live{align-items:center}.drop-live{left:auto;right:0;min-width:240px;padding:8px 0}.drop-live .live-tit{margin:0;padding:6px 14px 8px;font-size:12.5px;line-height:1.4;color:#aab4c4;border-bottom:1px solid #222a37;max-width:300px}.drop-live .lp-item{display:flex;align-items:center;justify-content:space-between;gap:10px;margin:4px 8px;padding:8px 10px;border-radius:6px;font-weight:700;font-size:13.5px;text-decoration:none;color:#fff;border:1px solid #ffffff33}.drop-live a.lp-item{display:flex!important;align-items:center;justify-content:flex-start!important;gap:10px;min-width:170px;padding:9px 12px!important;margin:4px 8px!important;border-radius:6px!important;font-size:14px}.drop-live a.lp-item.tw,.drop-live a.lp-item.tw:hover{background:#9146ff!important;color:#fff!important}.drop-live a.lp-item.kick,.drop-live a.lp-item.kick:hover{background:#53fc18!important;color:#0b0b0b!important}.drop-live a.lp-item.yt,.drop-live a.lp-item.yt:hover{background:#e62117!important;color:#fff!important}.drop-live a.lp-item:hover{filter:brightness(1.12)}.drop-live .est{order:-1;flex:none;width:12px;height:12px;border-radius:50%;background:#3ddc84;box-shadow:0 0 0 2px #0b1410,0 0 8px #3ddc84}.drop-live a.lp-item.tw{background:#9146ff}.drop-live a.lp-item.kick{background:#53fc18;color:#0b0b0b}.drop-live a.lp-item.yt{background:#e62117}.drop-live a.lp-item:hover{filter:brightness(1.12)}.drop-live .lp-item{background:#2a313d}.drop-live .lp-item.tw{background:#9146ff}.drop-live .lp-item.kick{background:#53fc18;color:#0b0b0b}.drop-live .lp-item.yt{background:#e62117}.drop-live .lp-item.off .est{background:#ff4d4d;box-shadow:0 0 0 2px #0b1410}/* Van 16-10: los de Twitch, Kick y YouTube, como mucho del tamaño del botón OFFLINE y centrados */.menu-live{position:relative}.menu-live>.drop-live{left:0!important;right:0!important;min-width:0!important;width:auto!important;padding:4px 6px!important;box-sizing:border-box}.drop-live a.lp-item{min-width:0!important;justify-content:center!important;gap:7px;margin:4px 0!important;padding:5px 8px!important;font-size:13px;line-height:1.5;border-radius:4px!important}.drop-live .est{width:9px;height:9px}
.is-live header.site nav a.live{border-color:#4dff9a;background:linear-gradient(#1fa855,#0d6b32);color:#fff;animation:livepulse 1.6s infinite}
.is-live header.site nav a.live:before{background:#fff}
@keyframes livepulse{0%,100%{box-shadow:0 0 0 0 #3ddc8488}50%{box-shadow:0 0 0 7px #3ddc8400}}
.live-on{display:inline-flex;align-items:center;gap:5px;margin-left:6px}
.live-on:empty{display:none}
.live-on a.lp,.live-banner a.lp{display:inline-flex;align-items:center;padding:4px 9px!important;margin:0!important;border:0!important;border-radius:4px;font-size:12px!important;font-weight:800;text-decoration:none;letter-spacing:.04em}
.lp.tw{background:#9146ff;color:#fff!important}.lp.off{background:#2a313d!important;color:#8a93a3!important;opacity:.75}.lp.yt{background:#e62117;color:#fff!important}.lp.kick{background:#53fc18;color:#0b0b0b!important}
.live-banner{display:none;align-items:center;gap:14px;flex-wrap:wrap;margin:0 0 22px;padding:14px 18px;border:1px solid #3ddc84;border-radius:8px;background:linear-gradient(90deg,#0d3b22,#0b1410);text-decoration:none}
.is-live .live-banner{display:flex}
.live-banner b{color:#fff;font:700 15px "Cinzel",Georgia,serif;letter-spacing:.06em}
.live-banner b:before{content:"● ";color:#3ddc84}
.live-banner .t{color:#d7f3e2;flex:1;min-width:200px}
.live-banner .go{display:inline-flex;gap:6px}
.tfo{position:relative;margin:34px 0 0;padding:34px 26px;border:1px solid #8a2b2b;border-radius:10px;overflow:hidden;background:linear-gradient(120deg,#3b0d10f2,#120a0d 60%)}
.tfo:before{content:"";position:absolute;inset:0;background:url("{base}assets/horde.png") center/cover;opacity:.16}
.tfo>*{position:relative}
.tfo h2{font-size:clamp(28px,4.6vw,44px);margin:4px 0 8px}
.tfo-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:20px 0}
.tfo-stats div{padding:14px;border:1px solid #ffffff1f;border-radius:8px;background:#0007;text-align:center}
.tfo-stats b{display:block;font:700 24px "Cinzel",Georgia,serif;color:var(--gold)}
.tfo-stats span{font-size:13px;color:#c9b9b9}
.actions{display:flex;gap:10px;flex-wrap:wrap}
.roads{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.road{padding:22px;border:1px solid #3b3222;border-radius:10px;background:linear-gradient(160deg,#171d29,#0d1119)}
.road.tw{border-color:#6441a5aa}.road.yt{border-color:#c4302baa}
.road-top{display:flex;justify-content:space-between;align-items:baseline;gap:10px;flex-wrap:wrap}
.road-top strong{font:700 21px "Cinzel",Georgia,serif;color:var(--gold)}
.road-top span{font-weight:700;color:#fff}
.bar{height:14px;border-radius:7px;background:#ffffff14;overflow:hidden;margin:12px 0;border:1px solid #ffffff1a}
.bar i{display:block;height:100%;border-radius:7px;background:linear-gradient(90deg,#b8842c,#ffd97a)}
.road.tw .bar i{background:linear-gradient(90deg,#6441a5,#b18cff)}
.road.yt .bar i{background:linear-gradient(90deg,#a3201a,#ff5a4e)}
.road p{color:#c3cbd8;margin:6px 0 14px}
.btn.tw{color:#fff;background:#9146ff;border:1px solid #b18cff}.btn.yt{color:#fff;background:#e62117;border:1px solid #ff6b63}.btn.kick{color:#0b0b0b;background:#53fc18;border:1px solid #9dff73}
.btn.donar{color:#1b1204;background:linear-gradient(#7ee0a0,#2fae62);border:1px solid #b6f5cb}
.btn.tw:hover,.btn.yt:hover,.btn.kick:hover,.btn.donar:hover{filter:brightness(1.1)}
.donate-box{display:flex;align-items:center;justify-content:space-between;gap:18px;flex-wrap:wrap;padding:20px 22px;border:1px solid #2fae6288;border-radius:10px;background:linear-gradient(120deg,#0f2a1c,#0d1119)}
.donate-box h3{margin:0 0 6px;color:#b6f5cb}.donate-box p{margin:0;color:#c3cbd8;max-width:640px}
.vgrid{display:flex;flex-wrap:wrap;justify-content:center;gap:16px}
.vgrid>.vcard{flex:1 1 260px;max-width:340px}
.vgrid.shorts>.vcard{flex:1 1 160px;max-width:210px}
.tfo{text-align:center}.tfo p{max-width:780px;margin-left:auto;margin-right:auto}
.tfo .soc-row,.tfo .actions{justify-content:center}
.centrado>.eyebrow,.centrado>h1,.centrado>.lead,.centrado>.sub,.centrado>.fine{text-align:center}
.centrado>.lead{max-width:780px;margin-left:auto;margin-right:auto}
.centrado .actions,.centrado .class-chips{justify-content:center}
.centrado .prepare{max-width:720px;margin:0 auto}
main:has(>.centrado)>.crumbs{text-align:center}
.centrado .tiles,.centrado .brands,.centrado .codes,.centrado .featured,.centrado .prepare{text-align:left}
.vcard{display:block;text-decoration:none;border:1px solid #2c3444;border-radius:8px;overflow:hidden;background:#0f141d;transition:transform .15s,border-color .15s}
.vcard:hover{transform:translateY(-3px);border-color:var(--gold)}
.thumb{position:relative;display:block;aspect-ratio:16/9;background:#000}
.shorts .thumb{aspect-ratio:9/12}
.thumb img{width:100%;height:100%;object-fit:cover;display:block}
.thumb em{position:absolute;right:6px;bottom:6px;padding:1px 6px;border-radius:3px;background:#000c;color:#fff;font:600 12px "Segoe UI",sans-serif;font-style:normal}
.thumb .badge{position:absolute;left:6px;top:6px;padding:2px 7px;border-radius:3px;background:#c81e1e;color:#fff;font:700 11px "Segoe UI",sans-serif;letter-spacing:.06em}
.thumb:after{content:"";position:absolute;left:50%;top:50%;width:52px;height:36px;margin:-18px 0 0 -26px;border-radius:9px;background:#e62117e6 url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M9 7l8 5-8 5z' fill='white'/%3E%3C/svg%3E") center/22px no-repeat;opacity:0;transition:opacity .15s}
.vcard:hover .thumb:after{opacity:1}
.vcard strong{display:block;padding:10px 12px 2px;font-size:14px;line-height:1.35;color:#eef2f8}
.vcard small{display:block;padding:0 12px 12px;color:#8f9bb0;font-size:12px}
.featured{display:grid;grid-template-columns:1.4fr 1fr;gap:18px;align-items:center;padding:18px;border:1px solid #3b3222;border-radius:10px;background:#0f141d;text-decoration:none;margin-bottom:18px}
.featured .thumb{border-radius:6px;overflow:hidden}
.featured h3{font-size:22px;margin:6px 0}
.about{display:grid;grid-template-columns:220px 1fr;gap:28px;align-items:center}/* Van 16-10: los tres botones de redes parejos y centrados; en una columna, todo centrado */.about .actions{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}.about .actions .btn{display:block;text-align:center;white-space:nowrap;padding-left:8px;padding-right:8px;font-size:14px}@media(max-width:820px){.about{justify-items:center;text-align:center}.about .actions{grid-template-columns:1fr;width:100%;max-width:340px;margin-left:auto;margin-right:auto}}
.avatar{width:220px;height:220px;border-radius:50%;border:4px solid #c99a3c;box-shadow:0 0 0 6px #1a1408,0 0 40px #c99a3c55;object-fit:cover}
.bios{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px}
.bio{display:block;padding:18px;border:1px solid #2c3444;border-radius:8px;background:#0f141d;text-decoration:none}
.bio:hover{border-color:var(--gold)}
.bio strong{display:flex;align-items:center;gap:8px;color:var(--gold);font:700 16px "Cinzel",Georgia,serif}
.bio small{display:block;color:#8f9bb0;margin:2px 0 8px}
.bio q{display:block;color:#dfe5ee;font-style:italic}
.cards3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.prize{padding:22px;border:1px solid #3b3222;border-radius:10px;background:linear-gradient(160deg,#1b1810,#0d1119)}
.prize h3{margin:4px 0 8px;color:var(--gold)}
.prize .tag{display:inline-block;padding:2px 8px;border-radius:3px;font:700 11px "Segoe UI",sans-serif;letter-spacing:.08em;background:#2a6b2a;color:#d9ffd9}
.prize .tag.wait{background:#6b4a12;color:#ffe7a6}
.fine{font-size:13px;color:#8f9bb0}
.hero:after{content:"";position:absolute;inset:0;background:radial-gradient(ellipse 60% 70% at center,#07090ef0 35%,#07090e80 70%,transparent)}
.hero>*{z-index:1}
.hero .greet{font:700 clamp(24px,3.6vw,34px) "Cinzel",Georgia,serif;color:#ffe7a6;margin:14px 0 10px;text-shadow:0 2px 12px #000}
.hero .lead{font-size:clamp(17px,2.1vw,20px);line-height:1.6;color:#f3f5f9;max-width:700px;text-shadow:0 1px 8px #000}
.firma{display:inline-flex;align-items:center;gap:10px;margin:6px 0 0;font:700 16px "Cinzel",Georgia,serif;color:#ffe7a6}
.firma img{width:40px;height:40px;border-radius:50%;border:2px solid #c99a3c}
.scroll-cue{display:inline-block;margin-top:8px;font-size:34px;line-height:1;color:var(--gold);text-decoration:none;animation:cue 1.8s infinite}
@keyframes cue{0%,100%{transform:translateY(0)}50%{transform:translateY(6px)}}
.soc-row{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;margin:14px 0 18px}
.soc{display:inline-flex;align-items:center;padding:8px 12px;border-radius:6px;text-decoration:none;font-weight:600;font-size:14px;border:1px solid #ffffff26;background:#0009}
.soc:hover{filter:brightness(1.15)}.soc.tw{background:#9146ff;color:#fff}.soc.yt{background:#e62117;color:#fff}.soc.kick{background:#53fc18;color:#0b0b0b}
.soc.tt{background:#111;color:#fff}.soc.x{background:#000;color:#fff}.soc.ig{background:linear-gradient(45deg,#f58529,#dd2a7b,#8134af);color:#fff}.soc.dc{background:#5865f2;color:#fff}
.soc.mail{background:linear-gradient(#e8bf55,#a87a24);color:#1a1205;border-color:#f3d27a;font-family:inherit;cursor:pointer}.soc.mail svg{width:16px;height:16px;margin-right:6px}
small.en{font:500 .42em "Segoe UI",sans-serif;letter-spacing:0;color:#9aa5b8;-webkit-text-fill-color:#9aa5b8;vertical-align:middle;margin-left:6px}
summary small.en{font-size:.8em}
.mtags{display:flex;flex-wrap:wrap;gap:5px;margin:4px 0 8px}
.mtags span{padding:2px 8px;border-radius:3px;font-size:12px;font-weight:600;background:#1e2738;border:1px solid #3a4760;color:#c9d6ee}
.legend{padding:10px 14px;border-left:3px solid var(--gold);background:#141a25;border-radius:4px}
.spells{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:6px;margin:8px 0 18px}
.spell{display:flex;align-items:center;gap:8px;padding:5px 8px;border:1px solid #2c3444;border-radius:5px;background:#0f141d}
.spell img{width:28px;height:28px;border-radius:4px}.spell b{font-size:13px;font-weight:600}.spell small{margin-left:auto;color:#8f9bb0;font-size:11px;white-space:nowrap}
.spells.later .spell{opacity:.7}
.mm-box{margin:0 0 22px;padding:20px 22px;border:1px solid #b597eb88;border-radius:10px;background:linear-gradient(120deg,#2a1d40,#111622)}
.mm-box h2{margin:0 0 8px;color:#d9c6ff}.mm-box .eyebrow{color:#b597eb;margin:0}
table.keys{border-collapse:collapse;width:100%;margin:10px 0}.keys th,.keys td{padding:9px 12px;border-bottom:1px solid #2c3444;text-align:left;vertical-align:top}.keys th{color:var(--gold);white-space:nowrap;width:1%}
.prepare ol{margin:0;padding-left:22px}.prepare li{margin:6px 0}
.class-chips{position:static!important;border:0!important;background:none!important}
.media-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.media-stats div{padding:16px;border:1px solid #3b3222;border-radius:8px;background:#0f141d;text-align:center}
.media-stats b{display:block;font:700 24px "Cinzel",Georgia,serif;color:var(--gold)}.media-stats span{font-size:13px;color:#aab4c4}
.brands,.codes{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px}
.brand,.code{display:block;padding:16px;border:1px solid #2c3444;border-radius:8px;background:#0f141d;text-decoration:none}
.brand strong,.code strong{display:block;font:700 18px "Cinzel",Georgia,serif;color:var(--gold)}
.brand small,.code small{display:block;color:#aab4c4;margin:2px 0 8px}.brand span,.code span{font-size:13px;color:#dfe5ee}
.code{border-color:#6b5426}.code:hover{border-color:var(--gold)}.code b{color:#ffe7a6;letter-spacing:.04em}
.quick{display:flex;flex-wrap:wrap}.quick a{display:inline-block;border:1px solid #4b4330;border-radius:3px;text-decoration:none;padding:8px 13px;background:#141a25;color:#eef2f8}
.apartados{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:0 0 10px}
.apartado{display:flex;align-items:center;gap:14px;padding:16px;border:1px solid #3b3222;border-radius:10px;background:linear-gradient(160deg,#171d29,#0d1119);text-decoration:none;transition:border-color .15s,transform .15s}
.apartado:hover{border-color:var(--gold);transform:translateY(-2px)}
.apartado img{width:52px;height:52px;border-radius:9px;border:2px solid #c99a3c;flex:none;object-fit:cover}
.apartado strong{display:block;font:700 18px "Cinzel",Georgia,serif;color:var(--gold)}.apartado small{display:block;color:#b6c0d0;font-size:13px;line-height:1.4;margin-top:2px}
.addons{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;text-align:left}
.addon{position:relative;display:flex;gap:16px;align-items:flex-start;padding:18px;border:1px solid #2c3444;border-radius:10px;background:linear-gradient(160deg,#171d29,#0d1119)}
.addon:hover{border-color:var(--gold)}.addon img{width:56px;height:56px;border-radius:9px;border:2px solid #c99a3c;flex:none}
.addon .rank{position:absolute;top:-10px;left:-10px;width:30px;height:30px;border-radius:50%;background:linear-gradient(#ffd97a,#b8842c);color:#1b1204;font:700 15px "Cinzel",Georgia,serif;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 8px #000a}
.addon h3{margin:2px 0 6px;color:var(--gold)}.addon .eyebrow{margin:0}.addon p{margin:0 0 8px;color:#dfe5ee}.addon q{display:block;margin:0 0 12px;color:#c9b58a;font-style:italic}
.sponsor-box{display:flex;align-items:center;justify-content:space-between;gap:18px;flex-wrap:wrap;margin:0 0 10px;padding:20px 22px;border:1px solid #c99a3c88;border-radius:10px;background:linear-gradient(120deg,#2a2210,#0d1119);text-align:left}
.sponsor-box h3{margin:0 0 6px;color:var(--gold)}.sponsor-box p{margin:0;color:#dfe5ee;max-width:680px}.sponsor-box .eyebrow{margin:0}.sponsor-box b{color:#ffe7a6}
@media(max-width:820px){.addons{grid-template-columns:1fr}}
.beta-cta{display:flex;gap:22px;align-items:center;flex-wrap:wrap;margin:26px 0;padding:24px 26px;border:2px solid #3ddc84;border-radius:12px;background:linear-gradient(120deg,#0d3b22,#0b1410 70%);box-shadow:0 0 30px #3ddc8433;text-align:left}
.beta-cta>div{flex:1;min-width:240px}.beta-cta h2,.beta-cta h3{margin:4px 0 8px;color:#b6f5cb}.beta-cta h2{font-size:clamp(24px,3.6vw,34px)}.beta-cta .eyebrow{color:#7ee0a0;margin:0}
.beta-cta p{color:#e6f5ec}.beta-cta.home{text-align:center;justify-content:center}.beta-cta.home>div{max-width:820px;margin:0 auto}.beta-cta.home .mini-pasos{display:inline-block;text-align:left;margin:4px auto 12px}.beta-cta.home .actions{justify-content:center}.beta-cta .soc-row{flex-basis:100%;justify-content:center;margin:4px 0 0}
.beta-face{width:96px;height:96px;border-radius:50%;border:3px solid #3ddc84;box-shadow:0 0 0 5px #0b1410;flex:none}
.mini-pasos{margin:8px 0 14px;padding-left:22px;color:#fff;font-weight:600}.mini-pasos li{margin:4px 0}
.pasos{list-style:none;counter-reset:paso;margin:0;padding:0;display:grid;gap:10px}
.pasos li{counter-increment:paso;position:relative;padding:14px 16px 14px 58px;border:1px solid #2c3444;border-radius:8px;background:#0f141d}
.pasos li:before{content:counter(paso);position:absolute;left:14px;top:12px;width:30px;height:30px;border-radius:50%;background:linear-gradient(#ffd97a,#b8842c);color:#1b1204;font:700 15px "Cinzel",Georgia,serif;display:flex;align-items:center;justify-content:center}
.pasos strong{display:block;color:var(--gold);font-size:16px}.pasos span{color:#dfe5ee}.pasos a{color:#ffe7a6}
.facts{display:grid;grid-template-columns:1fr 1fr;gap:14px}.fact{padding:18px;border-radius:10px;border:1px solid #2fae6288;background:#0f1a14}.fact.wait{border-color:#c99a3c88;background:#1b1810}
.fact h3{margin:0 0 8px;color:#b6f5cb}.fact.wait h3{color:#ffe7a6}.fact ul{margin:0;padding-left:20px}.fact li{margin:6px 0;color:#dfe5ee}
.news-card{position:relative;display:block;padding:22px 24px;border:2px solid #3ddc84;border-radius:12px;background:linear-gradient(120deg,#0d3b22,#0b1410 70%);text-decoration:none;text-align:center;cursor:pointer;transition:box-shadow .2s,transform .2s;margin-bottom:10px}.news-card:hover{transform:translateY(-2px)}.lanz-inicio>.lead{text-align:center;max-width:820px;margin-left:auto;margin-right:auto}
.news-card:hover{box-shadow:0 0 24px #3ddc8444}.news-card.home-reserva{text-align:center;padding-top:30px;margin:0 0 26px;border-color:#c99a3c;background:linear-gradient(120deg,#2a2210,#0b0d12 70%)}.news-card.home-reserva:hover{box-shadow:0 0 24px #e8b84a44}.news-card.home-reserva .eyebrow{color:#e8b84a}.news-card.home-reserva>span:last-child{display:flex;flex-direction:column;align-items:center}.news-card.home-reserva p{max-width:720px;margin-left:auto;margin-right:auto}.news-card.home-reserva .badge-new{background:#8a5a12}.news-card h3{margin:4px 0 6px;font-size:22px;color:#fff}.news-card p{color:#d7f3e2}.news-card .eyebrow{color:#7ee0a0;margin:0}
.badge-new{position:absolute;top:-11px;right:18px;padding:3px 10px;border-radius:4px;background:#c81e1e;color:#fff;font:700 12px "Segoe UI",sans-serif;letter-spacing:.08em}
@media(max-width:700px){.facts{grid-template-columns:1fr}.beta-face{width:72px;height:72px}}
main{overflow-x:clip}''' + __import__('forever_portal').CSS + __import__('guias_portal').CSS + __import__('macros_portal').CSS + '''
footer.site-foot{position:relative;margin:64px calc(50% - 50vw) -72px;padding:44px 0 28px;border-top:1px solid var(--gold-line);font-size:14px;color:#aab4c4;
background:linear-gradient(180deg,#0b0e15f2,#05070bfa),url("{base}assets/horde.png") center 30%/cover;box-shadow:inset 0 1px 0 #f3c76a1f}
footer.site-foot:before{content:"";position:absolute;left:0;right:0;top:0;height:3px;background:linear-gradient(90deg,transparent,#c99a3c,transparent)}
.foot-in{max-width:1160px;margin:0 auto;padding:0 24px}
.foot-grid{display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr 1fr;gap:24px}
.foot-grid h4{margin:4px 0 12px;font:700 13px "Cinzel",Georgia,serif;letter-spacing:.12em;text-transform:uppercase;color:#f4d27a}
.foot-col a{display:block;color:#e8b84a;text-decoration:none;padding:3px 0;font-size:14px}.foot-col a:hover{color:#ffe7a6;text-decoration:underline}
.foot-icons{display:flex;flex-wrap:wrap;gap:8px}
.foot-icons .ico{display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:50%;background:#1a2130;border:1px solid #2f3a4f;color:#cfd6e3;transition:all .15s}
.foot-icons .ico .rrss-icon{width:18px;height:18px;margin:0}
.foot-icons .ico:hover{transform:translateY(-2px);color:#fff}.foot-icons .tw:hover{background:#9146ff}.foot-icons .yt:hover{background:#e62117}.foot-icons .kick:hover{background:#53fc18;color:#0b0b0b}
.foot-icons .tt:hover{background:#111}.foot-icons .x:hover{background:#000}.foot-icons .ig:hover{background:#dd2a7b}.foot-icons .dc:hover{background:#5865f2}
.foot-mini{display:flex;flex-wrap:wrap;gap:4px 0;margin-top:10px!important}.foot-mini a{color:#a99a7c;text-decoration:none;padding:0 10px;border-left:1px solid #3a4253}.foot-mini a:first-child{padding-left:0;border-left:0}.foot-mini a:hover{color:#ffe7a6}
.foot-brand .brand{display:inline-flex;align-items:center;gap:10px;text-decoration:none}.foot-brand .crest{width:28px;height:32px}
.foot-brand .brand b{display:block;font:700 17px "Cinzel",Georgia,serif;color:var(--gold);letter-spacing:.08em}.foot-brand .brand small{display:block;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#a99a7c}
.foot-brand p{margin:12px 0}
.foot-soc{display:flex;flex-wrap:wrap;gap:6px}.foot-soc .soc{padding:6px 9px;font-size:12px}.foot-soc .rrss-icon{width:16px;height:16px;margin-right:5px}
.foot-partners{margin-top:26px;padding:16px;border:1px solid #3b3222;border-radius:10px;background:#0f141d}
.foot-partners h4{margin:0 0 10px;font:700 13px "Cinzel",Georgia,serif;letter-spacing:.1em;color:var(--gold)}
.foot-partners div{display:flex;flex-wrap:wrap;gap:8px}
.foot-partners a{display:inline-flex;align-items:baseline;gap:8px;padding:7px 12px;border:1px solid #4b4330;border-radius:6px;background:#141a25;text-decoration:none;color:#eef2f8}
.foot-partners a:hover{border-color:var(--gold)}.foot-partners small{color:#c9b58a;font-size:12px}.foot-partners a.more{border-style:dashed;color:#c9b58a}
.foot-legal{margin-top:26px;padding-top:14px;border-top:1px solid #222a37;font-size:12px;color:#7f8a9c}.foot-legal p{margin:4px 0}.foot-legal a{color:#a99a7c}
@media(max-width:900px){.apartados{grid-template-columns:1fr 1fr}.foot-grid{grid-template-columns:1fr 1fr}.foot-brand{grid-column:1/-1}}
/* Van 15-10: pie centrado, sin cosas a media línea; patrocinadores en recuadros iguales con el código debajo */
.foot-grid{grid-template-columns:repeat(4,1fr);text-align:center;gap:20px 24px}
.foot-brand{grid-column:1/-1;display:flex;flex-direction:column;align-items:center;max-width:640px;margin:0 auto 8px}.foot-brand p{margin:10px 0 14px}/* Van 16-10: la frase del pie con toque mágico: Cinzel dorada con brillo y adornos */.foot-brand>p{position:relative;max-width:560px;margin:16px auto 18px;padding:14px 22px;font:700 clamp(15px,1.6vw,18px)/1.55 "Cinzel",Georgia,serif;letter-spacing:.04em;text-align:center;background:linear-gradient(90deg,#c8963a,#f7e2a1 30%,#fff4cf 50%,#f7e2a1 70%,#c8963a);background-size:200% auto;-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 0 10px #e8b84a40);animation:pieBrillo 7s linear infinite}.foot-brand>p:before,.foot-brand>p:after{content:"";position:absolute;left:50%;width:min(320px,70%);height:1px;transform:translateX(-50%);background:linear-gradient(90deg,transparent,#e8b84a,transparent)}.foot-brand>p:before{top:0}.foot-brand>p:after{bottom:0}@keyframes pieBrillo{to{background-position:-200% center}}@media(prefers-reduced-motion:reduce){.foot-brand>p{animation:none}}
.foot-icons{justify-content:center;flex-wrap:nowrap;gap:10px}.foot-icons .ico{width:42px;height:42px;border:0;color:#fff;box-shadow:0 3px 10px #0008}.foot-icons .ico .rrss-icon{width:21px;height:21px}.foot-icons .tw,.foot-icons .tw:hover{background:#9146ff}.foot-icons .yt,.foot-icons .yt:hover{background:#e62117}.foot-icons .kick,.foot-icons .kick:hover{background:#53fc18;color:#0b0b0b}.foot-icons .tt,.foot-icons .tt:hover{background:linear-gradient(135deg,#25f4ee,#111 45%,#111 55%,#fe2c55)}.foot-icons .x,.foot-icons .x:hover{background:#000;box-shadow:0 0 0 1px #3a4253,0 3px 10px #0008}.foot-icons .ig,.foot-icons .ig:hover{background:radial-gradient(circle at 30% 107%,#fdf497 0,#fd5949 45%,#d6249f 60%,#285aeb 90%)}.foot-icons .dc,.foot-icons .dc:hover{background:#5865f2}.foot-icons .ico:hover{transform:translateY(-3px) scale(1.06);filter:brightness(1.12)}.foot-icons .tw .rrss-icon path+path{stroke:#9146ff}.foot-icons .yt .rrss-icon path{fill:#e62117}
.foot-partners{text-align:center}.foot-partners h4{margin-bottom:12px}
.foot-partners>div{display:grid;grid-template-columns:repeat(6,1fr);gap:10px}@media(max-width:900px){.foot-partners>div{grid-template-columns:repeat(3,1fr)}}
.foot-partners a{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;min-height:62px;padding:8px 10px;text-align:center}
.foot-partners a small{display:block;font-size:11.5px}
/* Van 16-10: fondo fijo de toda la web, Alianza (Ventormenta) a la izquierda y Horda (Orgrimmar) a la derecha; se funden al centro, donde va el texto */body{background:#05070d!important}body:before,body:after{content:"";position:fixed;top:0;bottom:0;width:62vw;z-index:-1;pointer-events:none;background-size:cover;background-repeat:no-repeat}body:before{left:0;background-image:linear-gradient(rgba(5,8,16,.42),rgba(5,8,16,.62)),url("{base}assets/alliance.png");background-position:35% center;-webkit-mask-image:linear-gradient(90deg,#000 45%,transparent 100%);mask-image:linear-gradient(90deg,#000 45%,transparent 100%)}body:after{right:0;background-image:linear-gradient(rgba(5,8,16,.42),rgba(5,8,16,.62)),url("{base}assets/horde.png");background-position:60% center;-webkit-mask-image:linear-gradient(270deg,#000 45%,transparent 100%);mask-image:linear-gradient(270deg,#000 45%,transparent 100%)}@media(max-width:700px){body:before{display:none}body:after{width:100vw;-webkit-mask-image:none;mask-image:none;background-image:linear-gradient(rgba(5,8,16,.78),rgba(5,8,16,.86)),url("{base}assets/horde.png")}}.avisos{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin:6px 0 18px}.aviso{position:relative;display:flex;flex-direction:column;gap:6px;padding:16px 18px 14px;border:1px solid #24466b;border-left:3px solid #148eff;border-radius:10px;background:linear-gradient(170deg,#0f1a2b,#0a0f18);text-decoration:none;color:#dfe5ee;transition:transform .15s,border-color .15s}.aviso:hover{border-color:#148eff;transform:translateY(-2px)}.aviso-meta{font:700 11px/1.35 "Segoe UI",sans-serif;letter-spacing:.07em;text-transform:uppercase;color:#6fb6ff}.aviso b{color:#fff;font-size:16px;line-height:1.3}.aviso-txt{flex:1;font-size:13.5px;line-height:1.5;color:#aab4c4}.aviso-mas{font-size:13px;font-weight:700;color:#e8b84a}@media(max-width:900px){.avisos{grid-template-columns:1fr}}.foot-icons .mail,.foot-icons .mail:hover{background:linear-gradient(#f3c76a,#c99a3c);color:#14100a;border:0;cursor:pointer;font:inherit}.correo-ver{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:8px 12px;margin:12px auto 0;padding:9px 14px;width:fit-content;border:1px solid #6b5a2e;border-radius:999px;background:#14100a;color:#ffe7a6;font-size:14px}.correo-ver a{color:#ffe7a6;font-weight:700}.correo-ver button{padding:4px 12px;border:1px solid #6b5a2e;border-radius:999px;background:#2a200c;color:#ffe7a6;cursor:pointer;font:inherit;font-size:13px}button.btn[data-correo]{display:inline-flex;align-items:center;gap:8px;cursor:pointer;font:inherit}button.btn[data-correo] .rrss-icon{width:18px;height:18px}.car{position:relative;margin:0 0 26px;border:1px solid #6b5a2e;border-radius:14px;overflow:hidden;box-shadow:0 14px 40px #000a}.car-vista{overflow:hidden}.car-pista{display:flex;transition:transform .6s cubic-bezier(.4,0,.2,1)}.car-slide{flex:0 0 100%;min-height:340px;display:flex;align-items:center;justify-content:center;text-align:center;padding:40px 76px 56px;background-size:cover;background-position:center;text-decoration:none;color:#eef2f8;box-sizing:border-box}.car-txt{max-width:740px}.car-txt .eyebrow{margin:0}.car-txt h2{margin:8px 0 10px;font-size:clamp(26px,3.6vw,40px);color:#ffe7a6}.car-txt p{margin:0 auto 14px;color:#dfe5ee;max-width:640px}.car-slide:hover h2{color:#fff;text-shadow:0 0 18px #f3c76acc}.cs-horda{background-image:linear-gradient(rgba(6,8,14,.68),rgba(6,8,14,.8)),url("{base}assets/horde.png")}.cs-alianza{background-image:linear-gradient(rgba(6,8,14,.66),rgba(6,8,14,.8)),url("{base}assets/alliance.png")}.cs-halloween{background-image:radial-gradient(ellipse at 50% 100%,#ff7a1a66,transparent 65%),linear-gradient(rgba(30,12,4,.72),rgba(8,5,3,.88)),url("{base}assets/warlock.jpg")}.cs-torneo{background-image:linear-gradient(rgba(40,6,8,.72),rgba(10,6,8,.85)),url("{base}assets/horde.png");background-position:center 30%}.cs-blizz{background-image:radial-gradient(ellipse at 50% 0,#148eff55,transparent 60%),linear-gradient(rgba(6,12,24,.8),rgba(5,9,18,.9)),url("{base}assets/alliance.png")}.cs-web{background-image:radial-gradient(ellipse at 50% 100%,#e8b84a40,transparent 60%),linear-gradient(rgba(6,8,14,.78),rgba(6,8,14,.88)),url("{base}assets/horde.png");background-position:center 70%}.car-flecha{position:absolute;top:50%;z-index:2;width:44px;height:44px;margin-top:-22px;border:1px solid #6b5a2e;border-radius:50%;background:#0b0f16cc;color:#ffe7a6;font-size:28px;line-height:1;cursor:pointer}.car-flecha:hover{border-color:#e8b84a}.car-flecha.prev{left:14px}.car-flecha.next{right:14px}.car-puntos{position:absolute;left:0;right:0;bottom:16px;z-index:2;display:flex;justify-content:center;gap:8px}.car-puntos button{width:10px;height:10px;padding:0;border:0;border-radius:5px;background:#ffffff55;cursor:pointer;transition:width .3s,background .3s}.car-puntos button.on{width:28px;background:#e8b84a}.car.solo .car-flecha,.car.solo .car-puntos{display:none}@media(max-width:700px){.car-slide{min-height:300px;padding:28px 18px 52px}.car-flecha{display:none}}@media(prefers-reduced-motion:reduce){.car-pista{transition:none}}.lienzo{margin:14px 0 0;padding:26px 32px 34px;border:1px solid #3b3222;border-radius:16px;background:linear-gradient(180deg,rgba(10,13,21,.88),rgba(7,9,15,.92));box-shadow:0 22px 60px #000b,inset 0 1px 0 #ffffff0a;-webkit-backdrop-filter:blur(3px);backdrop-filter:blur(3px)}@media(max-width:700px){.lienzo{margin-top:8px;padding:16px 14px 24px;border-radius:12px}}/* Van 17-10: modo Retail, tono Midnight (violeta del Vacío) en vez de Alianza/Horda */html.modo-retail body{background:#07050f!important}/* Van 17-10: fondo de Retail, Lunargenta (capital de Midnight; arte oficial de Blizzard teñido de lila con tintar_lunargenta.py) */html.modo-retail body:before{width:100vw;-webkit-mask-image:none;mask-image:none;display:block;background-image:radial-gradient(ellipse at 50% 0,#7b3fd633,transparent 60%),linear-gradient(rgba(7,5,15,.12),rgba(7,5,15,.38) 65%,rgba(7,5,15,.7)),url("{base}assets/lunargenta.jpg");background-position:center top;background-size:cover}@media(max-width:700px){html.modo-retail body:before{background-position:38% top}html.modo-retail body:after{display:none}}html.modo-retail body:after{display:none}html.modo-retail .lienzo{border-color:#4a2f7a;box-shadow:0 22px 60px #000b,0 0 40px #7b3fd622,inset 0 1px 0 #ffffff0a}html.modo-retail .eyebrow{color:#b98cff}@font-face{font-family:"Cinzel Decorative";src:url("{base}assets/fonts/cinzel-decorative-700.woff2") format("woff2");font-weight:700;font-display:swap}@font-face{font-family:"Cinzel Decorative";src:url("{base}assets/fonts/cinzel-decorative-900.woff2") format("woff2");font-weight:900;font-display:swap}@font-face{font-family:"Marcellus SC";src:url("{base}assets/fonts/marcellus-sc.woff2") format("woff2");font-weight:400;font-display:swap}/* Van 17-10: letras de Retail con aire de logo de WoW (Cinzel Decorative en títulos, Marcellus SC en subtítulos) */html.modo-retail main h1{font-family:"Cinzel Decorative",Cinzel,Georgia,serif!important;font-weight:900!important;letter-spacing:.005em;background:linear-gradient(180deg,#fffbe8 0%,#ffe08a 38%,#d9a53f 62%,#8a5a1c 100%);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 2px 0 #1a0d33) drop-shadow(0 0 1px #000) drop-shadow(0 0 22px #9a5cffaa)}html.modo-retail main h2,html.modo-retail main h3,html.modo-retail .r-card strong,html.modo-retail .r-mm strong,html.modo-retail .r-jefe strong,html.modo-retail .r-tl-i b{font-family:"Marcellus SC",Cinzel,Georgia,serif!important;font-weight:400!important;letter-spacing:.03em}html.modo-retail main h2{color:#f3d58c;text-shadow:0 0 14px #8b4fe466}html.modo-retail main h2.r-clsh{color:var(--c);text-shadow:0 0 14px var(--c)}html.modo-retail main h1{font-size:clamp(28px,4.6vw,52px)!important;line-height:1.12;font-variant-ligatures:none;font-feature-settings:"liga" 0,"dlig" 0}html.modo-retail .eyebrow{font-family:"Marcellus SC",sans-serif;letter-spacing:.14em}/* Van 21-10: horas de México, Chile y Argentina tras el asterisco */.latam{display:block;margin-top:6px;font-size:13px;line-height:1.45;color:#9aa6b8}/* Van 15-10: botón suelto al final de una caja, centrado */.prepare .actions{justify-content:center}.addon>div>a.btn,.prize>a.btn,.road>a.btn,.detail-body>a.calc-open{display:flex;width:fit-content;margin-left:auto;margin-right:auto}.cuadra-g{display:flex!important;flex-wrap:wrap;justify-content:center;gap:var(--g)!important}.cuadra-g>*{flex:0 0 calc((100% - (var(--cols) - 1) * var(--g)) / var(--cols));max-width:calc((100% - (var(--cols) - 1) * var(--g)) / var(--cols));min-width:0;box-sizing:border-box}.cuadra-g>.cuadra-sobra{display:none!important}.cuadra-c{justify-content:center;margin-left:auto!important;margin-right:auto!important}.quick,.race-chips,.mtags,.race-classes,.class-chips,.fnav,.soc-row{justify-content:center}.foot-legal{text-align:center}.foot-legal p{text-wrap:balance}.foot-mini{justify-content:center}
@media(max-width:600px){.foot-partners>div{grid-template-columns:1fr 1fr}}
@media(max-width:560px){.apartados{grid-template-columns:1fr}}
@media(max-width:820px){.media-stats{grid-template-columns:1fr 1fr}}
@media(max-width:1260px) and (min-width:1101px){header.site nav a,header.site .menu-btn{padding:21px 7px;font-size:13px}header.site .brand small{display:none}header.site nav a.live{padding:7px 10px}}
@media(max-width:820px){.tfo-stats{grid-template-columns:1fr 1fr}.roads,.cards3,.featured,.about{grid-template-columns:1fr}.avatar{width:160px;height:160px;margin:auto}}
'''

# Van 16-10: contador de visitas sin cookies (Cloudflare Web Analytics, cuenta de Van, sitio muchamielwow.github.io). El token es público.
CONTADOR = "<script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{\"token\": \"a44ebced14ee440689bb5279b40e31e3\"}'></script>"

LIVE_JS = r'''/* Van 16-10: botón para volver arriba en todas las páginas (sale al bajar) */(function(){var en=(document.documentElement.lang||'').indexOf('en')===0,b=document.createElement('button'),s=document.createElement('style');s.textContent='.subir{position:fixed;right:22px;bottom:22px;z-index:60;width:48px;height:48px;border-radius:50%;border:1px solid #f3d27a;background:linear-gradient(#e8bf55,#a87a24);color:#1a1205;font:900 22px/1 Georgia,serif;cursor:pointer;box-shadow:0 4px 16px #000a,0 0 12px #e8b84a55;opacity:0;visibility:hidden;transform:translateY(10px);transition:opacity .25s,transform .25s,visibility .25s}.subir.ver{opacity:1;visibility:visible;transform:none}.subir:hover{filter:brightness(1.12);box-shadow:0 4px 16px #000a,0 0 20px #f3c76a99}.subir:focus-visible{outline:2px solid #fff;outline-offset:3px}@media(max-width:600px){.subir{right:14px;bottom:14px;width:44px;height:44px}}';document.head.appendChild(s);b.type='button';b.className='subir';b.textContent='▲';b.title=en?'Back to top':'Volver arriba';b.setAttribute('aria-label',b.title);b.addEventListener('click',function(){window.scrollTo({top:0,behavior:'smooth'})});document.body.appendChild(b);var f=function(){b.classList.toggle('ver',window.scrollY>500)};window.addEventListener('scroll',f,{passive:true});f()})();
document.addEventListener('click',function(e){var a=e.target.closest('a[data-abre]');if(!a)return;var d=document.getElementById(a.getAttribute('href').slice(1));if(!d)return;e.preventDefault();d.open=true;d.scrollIntoView({behavior:'smooth',block:'start'});history.replaceState(null,'',a.getAttribute('href'))});(function(){var h=location.hash&&document.getElementById(location.hash.slice(1));if(h&&h.tagName==='DETAILS'){h.open=true;for(var p=h.parentElement;p;p=p.parentElement)if(p.tagName==='DETAILS')p.open=true}})();
document.addEventListener('click',function(e){var b=e.target.closest('[data-correo]');if(!b)return;e.preventDefault();var EN=document.documentElement.lang==='en',m=b.getAttribute('data-correo').replace('|','@'),h=b.closest('.foot-icons,.actions,.soc-row')||b,v=h.nextElementSibling;if(v&&v.classList.contains('correo-ver')){v.remove();return}v=document.createElement('p');v.className='correo-ver';v.innerHTML='<span>'+(EN?'Email:':'Correo:')+'</span><a href="mailto:'+m+'">'+m+'</a><button type="button">'+(EN?'Copy':'Copiar')+'</button>';h.after(v);v.querySelector('button').onclick=function(){var t=this;(navigator.clipboard?navigator.clipboard.writeText(m):Promise.reject()).then(function(){t.textContent=EN?'Copied':'Copiado'},function(){t.textContent=m})}});
(function(){
var CH='muchamiel',KEY='mm-live3',root=document.documentElement,EN=root.lang==='en';
var URLS={tw:'https://www.twitch.tv/'+CH,kick:'https://kick.com/'+CH,yt:'https://www.youtube.com/@'+CH+'/live'},NAMES={tw:'Twitch',kick:'Kick',yt:'YouTube'};var BASE=(document.currentScript&&document.currentScript.src||'').replace(/assets\/live\.js.*$/,'');
function store(v){try{sessionStorage.setItem(KEY,JSON.stringify({t:Date.now(),v:v}))}catch(e){}}
function cached(){try{var c=JSON.parse(sessionStorage.getItem(KEY));if(c&&Date.now()-c.t<90000)return c.v}catch(e){}return null}
function chips(v){return ['tw','kick','yt'].map(function(p){var u=p==='yt'?(v.ytUrl||URLS.yt):URLS[p];return '<a class="lp '+p+(v[p]?'':' off')+'" href="'+u+'" target="_blank" rel="noopener noreferrer" title="'+NAMES[p]+(v[p]?(EN?': live':': en directo'):(EN?': offline':': sin directo'))+'">'+NAMES[p]+(v[p]?'':' · offline')+'</a>'}).join('')}
function apply(v){var on=!!(v.tw||v.kick||v.yt);root.classList.toggle('is-live',on);
document.querySelectorAll('a.live').forEach(function(a){a.textContent=on?(EN?'LIVE':'EN DIRECTO'):'OFFLINE';a.title=on?'Live':'Offline'});
document.querySelectorAll('.drop-live').forEach(function(d){d.innerHTML=['tw','kick','yt'].map(function(p){var u=p==='yt'?(v.ytUrl||URLS.yt):URLS[p];return v[p]?'<a class="lp-item '+p+'" href="'+u+'" target="_blank" rel="noopener noreferrer" title="Live"><span>'+NAMES[p]+'</span><b class="est"></b></a>':'<a class="lp-item '+p+' off" href="'+u+'" target="_blank" rel="noopener noreferrer" title="Offline"><span>'+NAMES[p]+'</span><b class="est"></b></a>'}).join('')})}
function txt(u){return fetch(u,{cache:'no-store'}).then(function(r){return r.ok?r.text():''}).catch(function(){return ''})}
function check(){var c=cached();if(c){apply(c);return}
Promise.all([txt('https://decapi.me/twitch/uptime/'+CH),fetch('https://kick.com/api/v2/channels/'+CH+'/livestream',{cache:'no-store'}).then(function(r){return r.ok?r.json():{}}).catch(function(){return {}}),fetch(BASE+'datos/directo.json?v='+Math.floor(Date.now()/6e4),{cache:'no-store'}).then(function(r){return r.ok?r.json():{}}).catch(function(){return {}})]).then(function(r){
var tw=!!r[0]&&!/offline|error|not found|invalid/i.test(r[0]),k=r[1]&&r[1].data?r[1].data:null,y=r[2]||{},v={tw:tw,kick:!!k,yt:!!y.youtube,ytUrl:y.url||'',title:k&&k.session_title||y.titulo||''};
if(tw&&!v.title)return txt('https://decapi.me/twitch/title/'+CH).then(function(t){v.title=t;store(v);apply(v)});store(v);apply(v)})}
document.querySelectorAll('.menu-btn').forEach(function(b){var m=b.parentNode;b.addEventListener('click',function(e){e.stopPropagation();var o=m.classList.toggle('open');b.setAttribute('aria-expanded',o);if(!o)b.blur()})});document.addEventListener('click',function(){document.querySelectorAll('.menu.open').forEach(function(m){m.classList.remove('open');m.firstChild.setAttribute('aria-expanded','false');if(document.activeElement&&m.contains(document.activeElement))document.activeElement.blur()})});
document.querySelectorAll('.menu-live>a.live').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();var m=a.parentNode,o=m.classList.toggle('open');a.setAttribute('aria-expanded',o)})});
check();setInterval(check,120000);
document.querySelectorAll('[data-twitch-followers]').forEach(function(el){txt('https://decapi.me/twitch/followcount/'+CH).then(function(t){var n=parseInt(t,10);if(n>0)el.textContent=String(n).replace(/\B(?=(\d{3})+(?!\d))/g,EN?',':'.')})});document.querySelectorAll('[data-kick-followers]').forEach(function(el){fetch('https://kick.com/api/v2/channels/'+CH,{cache:'no-store'}).then(function(r){return r.ok?r.json():{}}).then(function(d){var n=parseInt(d&&d.followers_count,10);if(n>0)el.textContent=String(n).replace(/\B(?=(\d{3})+(?!\d))/g,EN?',':'.')}).catch(function(){})});
/* Van 30-10: suscriptores de YouTube al día (datos/youtube.json, lo escribe la tarea de GitHub cada 20 min) */document.querySelector('[data-yt-subs]')&&fetch(BASE+'datos/youtube.json?v='+Math.floor(Date.now()/6e5),{cache:'no-store'}).then(function(r){return r.ok?r.json():{}}).then(function(d){var n=+d.subs;if(!(n>0))return;var k=(n/1000).toFixed(1);document.querySelectorAll('[data-yt-subs]').forEach(function(el){el.textContent=EN?k:k.replace('.',',')});document.querySelectorAll('[data-yt-bar]').forEach(function(el){el.style.width=Math.min(100,n/1000)+'%'});document.querySelectorAll('[data-yt-80]').forEach(function(el){el.textContent=n>=90000?(EN?'(done!)':'(¡conseguido!)'):(EN?'(almost!)':'(¡casi!)')})}).catch(function(){});
document.querySelectorAll('[data-countdown]').forEach(function(el){var d=new Date(el.getAttribute('data-countdown')+'T00:00:00'),now=new Date(),days=Math.ceil((d-now)/864e5);
el.textContent=EN?(days>1?days+' days':days===1?'Tomorrow!':days>=-1?'Today!':'Finished'):(days>1?days+' días':days===1?'¡Mañana!':days>=-1?'¡Es hoy!':'Terminado')});
})();'''


def fecha(iso):
    y, m, d = iso.split('-')
    return f'{int(d)} {MESES[int(m) - 1]} {y}'


def limpia(t):
    return re.sub(r'\s*💥\s*', ' · ', t).strip(' ·')


def vcard(v, kind):
    vid, iso, dur, title = v
    url = f'https://www.youtube.com/shorts/{vid}' if kind == 'short' else f'https://www.youtube.com/watch?v={vid}'
    img = f'https://i.ytimg.com/vi/{vid}/' + ('hqdefault.jpg' if kind == 'short' else 'mqdefault.jpg')
    badge = '<b class="badge">DIRECTO</b>' if kind == 'live' else ('<b class="badge">SHORT</b>' if kind == 'short' else '')
    return (f'<a class="vcard" href="{url}" target="_blank" rel="noopener noreferrer"><span class="thumb"><img loading="lazy" src="{img}" alt="">'
            + (f'<em>{dur}</em>' if dur else '') + badge + f'</span><strong>{E(limpia(title))}</strong><small>{fecha(iso)}</small></a>')


SOCIALS = [('Twitch', TWITCH, 'tw'), ('YouTube', YT_SUB, 'yt'), ('Kick', KICK, 'kick'), ('TikTok', 'https://www.tiktok.com/@muchamielwow', 'tt'),
           ('X / Twitter', 'https://twitter.com/Muchamiel_', 'x'), ('Instagram', 'https://www.instagram.com/muchamiel_/', 'ig'), ('Discord', DISCORD, 'dc')]
DISCORD_SVG = '<svg class="rrss-icon" viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M20 5.3A17 17 0 0 0 15.7 4l-.5 1a15.6 15.6 0 0 0-4.4 0l-.5-1A17 17 0 0 0 6 5.3 17.6 17.6 0 0 0 3 17.2 17 17 0 0 0 8.2 20l1.1-1.8a11 11 0 0 1-1.7-.8l.4-.3a12.2 12.2 0 0 0 10 0l.4.3-1.7.8 1.1 1.8a17 17 0 0 0 5.2-2.8A17.6 17.6 0 0 0 20 5.3zM9.3 14.8c-1 0-1.8-.9-1.8-2s.8-2 1.8-2 1.8.9 1.8 2-.8 2-1.8 2zm5.4 0c-1 0-1.8-.9-1.8-2s.8-2 1.8-2 1.8.9 1.8 2-.8 2-1.8 2z"/></svg>'


def socials_row(correo=False):
    from embellecer_portal import social_icon
    out = ''
    for label, url, cls in SOCIALS:
        icon = DISCORD_SVG if label == 'Discord' else social_icon(label).replace('fill="#fff"', 'fill="#0c1017"').replace('stroke="#fff"', 'stroke="#0c1017"')
        out += f'<a class="soc {cls}" href="{url}" target="_blank" rel="noopener noreferrer">{icon}{label}</a>'
    if correo:  # Van 16-10: el correo como una red más, en la misma fila (antes, botón suelto debajo que saltaba de línea)
        out += f'<button type="button" class="soc mail" {CORREO_DATA}>{MAIL_SVG}Correo</button>'
    return '<div class="soc-row">' + out + '</div>'


def tfo(base, page=False):
    more = '' if page else f'<a class="btn ghost" href="{base}torneo/">Todo sobre el torneo</a>'
    return (f'<section class="tfo" id="torneo"><p class="eyebrow">TORNEO PVP · 17 Y 18 DE OCTUBRE</p><h2>The Forever Open 1v1 Tournament</h2>'
            '<div class="tfo-stats"><div><b>100.000 $</b><span>premio total</span></div><div><b>50.000 $</b><span>para el campeón</span></div>'
            '<div><b>5.555 $</b><span>al mejor de cada clase</span></div><div><b data-countdown="2026-10-17">17 oct</b><span>para empezar</span></div></div>'
            '<p>Muchamiel compite con su <strong>Brujo No-muerto</strong> y lleva semanas preparándolo en directo. <strong>Ese fin de semana, ven a animarle</strong>: '
            'cuantos más seamos en el chat, más fuerte pega el Shadow Bolt. Para verle, el botón de directo de arriba te lleva a Twitch, YouTube o Kick.</p>' +  # Van 16-10: sin repetir las redes (ya están en el pie)
           
            f'<div class="actions"><a class="btn gold" href="{TFO_RULES}" target="_blank" rel="noopener noreferrer">Reglamento oficial (raider.io)</a>{more}</div>'
            '<p class="fine">Las reglas cambian a menudo, por eso no las copiamos aquí: consulta siempre el reglamento oficial.</p></section>')


def miles(n):
    return f'{n:,}'.replace(',', '.')


def roads():
    yt, tw = STATS['yt_subs'], STATS['tw_subs']
    yt_txt = f'{yt / 1000:.1f}'.replace('.', ',')
    return ('<div class="roads">'
            f'<div class="road yt"><div class="road-top"><strong>Road to 100K</strong><span><span data-yt-subs>{yt_txt}</span> K / 100 K</span></div>'
            f'<div class="bar"><i data-yt-bar style="width:{yt / STATS["yt_goal"] * 100:.1f}%"></i></div>'
            f'<p>Suscriptores en YouTube. Sorteo de <strong>1 año de WoW a los 90 K</strong> <span data-yt-80>{"(¡conseguido!)" if yt >= 90000 else "(¡casi!)"}</span> y de <strong>otro año a los 100 K</strong>, solo por suscribirte.</p>'
            f'<a class="btn yt" href="{YT_SUB}" target="_blank" rel="noopener noreferrer">Suscribirme en YouTube</a></div>'
            f'<div class="road tw"><div class="road-top"><strong>Road to 2K subs</strong><span>{miles(tw)} / {miles(STATS["tw_goal"])}</span></div>'
            f'<div class="bar"><i style="width:{tw / STATS["tw_goal"] * 100:.1f}%"></i></div>'
            f'<p>Subs en Twitch. Al llegar a 2.000: <strong>sorteo de 1 año de WoW</strong>. Faltan {STATS["tw_goal"] - tw}.</p>'
            f'<a class="btn tw" href="https://www.twitch.tv/subs/muchamiel" target="_blank" rel="noopener noreferrer">Suscribirme en Twitch</a></div>'
            f'</div><p class="fine">Los suscriptores de YouTube se actualizan solos; los subs de Twitch, a mano (cifra del {FECHA_DATOS}).</p>')


CENTRADAS = {'addons', 'torneo', 'noticias', 'sorteos', 'colaboraciones', 'clases', 'calendario'}  # páginas con todo centrado (petición de Van)


def page(slug, title, desc, body):
    tpl = (dist / 'comunes' / 'index.html').read_text(encoding='utf-8')
    head = tpl[:tpl.index('<body')]
    head = re.sub(r'<title>.*?</title>', '<title>' + E(title) + '</title>', head, count=1, flags=re.S)
    head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="' + E(desc, quote=True) + '">', head, count=1)
    footer = tpl[tpl.index('<footer'):tpl.index('</footer>') + 9]
    folder = dist / slug
    folder.mkdir(exist_ok=True)
    if slug in CENTRADAS:
        body = '<div class="centrado">' + body + '</div>'
    (folder / 'index.html').write_text(head + '<body><header></header><main>' + body + footer + '</main></body></html>', encoding='utf-8')


# Prueba de estrés gratis (pedido de Van, 15-10). Fuentes: anuncio oficial de la beta (varias horas abiertas a todo el mundo)
# y la opción «WoW: Forever – Prueba de estrés» del launcher. 19-10: Blizzard la pasó del lunes 19 al miércoles 21 (misma hora, 19:00 CEST; Kaivax, foro).
BNET_APP = 'https://download.battle.net/es-es/?product=bnetdesk'
BNET_CUENTA = 'https://account.battle.net/creation/flow/creation-full'
BLIZZ_BETA = 'https://news.blizzard.com/es-es/article/24304160/la-beta-de-world-of-warcraft-forever-ya-esta-disponible'
BETA_PASOS = [
    ('Crea tu cuenta de Battle.net', f'Es gratis. Si ya tienes una (aunque no juegues desde hace años), te sirve. <a href="{BNET_CUENTA}" target="_blank" rel="noopener noreferrer">Crear cuenta</a>'),
    ('Instala la app de Battle.net', f'Descárgala de la web oficial de Blizzard e inicia sesión con tu cuenta. <a href="{BNET_APP}" target="_blank" rel="noopener noreferrer">Descargar Battle.net</a>'),
    ('Elige World of Warcraft', 'En la lista de juegos de la app, entra en World of Warcraft.'),
    ('Cambia la versión del juego', 'Encima del botón azul, abre el desplegable «Versión del juego» y elige <strong>WoW: Forever – Prueba de estrés</strong>.'),
    ('Pulsa «Preinstalar»', 'Déjalo descargando desde ya. Así el día 21 no pierdes ni un minuto mientras los demás esperan la descarga.'),
    ('El miércoles 21 a las 19:00, a jugar', 'Cuando Blizzard abra los servidores (en México a las 15:00; en Chile y Argentina a las 18:00), el botón cambiará a «Jugar». Elige reino, crea tu personaje y nos vemos en Azeroth.'),
]
BLIZZ_ESTRES = 'https://worldofwarcraft.blizzard.com/es-es/news/24302072'
BLIZZ_ESTRES_FORO = 'https://us.forums.blizzard.com/en/wow/t/wow-forever-stress-test-october-21/2383617'


def beta_page():
    pasos = ''.join(f'<li><strong>{E(t)}</strong><span>{d}</span></li>' for t, d in BETA_PASOS)
    # 16-10: Blizzard publicó la hora (Kaivax, foro, 15-10 21:24 UTC): 19:00 CEST en Europa, unas horas, en los servidores del lanzamiento y con borrado total al cerrar.
    body = ('<p class="eyebrow">NOTICIA · PRUEBA DE ESTRÉS · ACTUALIZADA EL 19 DE OCTUBRE DE 2026</p><h1>Juega gratis a WoW Forever el miércoles 21 de octubre a las 19:00</h1><div class="prepare"><h3>Cambio de fecha</h3><p>Blizzard ha movido la prueba del lunes 19 al <strong>miércoles 21 de octubre</strong>, a la misma hora (19:00, hora peninsular)*. Si ya la tenías preinstalada, no tienes que hacer nada más. <span class="latam">* México: 15:00 · Chile y Argentina: 18:00.</span></p></div>'
            '<p class="lead">El <strong>miércoles 21 de octubre a las 19:00</strong> (hora peninsular)* Blizzard abre WoW Forever a <strong>todo el mundo</strong> durante unas horas, '
            'para una prueba de estrés en los servidores del lanzamiento. No necesitas suscripción ni invitación: basta con una cuenta de World of Warcraft. '
            'Y puedes dejarlo preinstalado desde hoy. <span class="latam">* México: 15:00 · Chile y Argentina: 18:00.</span></p>'
            '<div class="tfo-stats"><div><b data-countdown="2026-10-21">21 oct</b><span>para la prueba</span></div><div><b>19:00</b><span>hora peninsular</span></div>'
            '<div><b>Gratis</b><span>sin suscripción</span></div><div><b>Unas horas</b><span>y luego se borra todo</span></div></div>'
            '<div class="divider"><h2>Qué es una prueba de estrés</h2></div>'
            '<p>Ese día Blizzard <strong>apagará la beta</strong> y abrirá WoW Forever en los <strong>servidores de cada región que usará el día del lanzamiento</strong>, '
            'durante unas horas. Quiere llenarlos de gente para ver cuánto aguantan: pide que crees un personaje, hagas misiones, comercies, hables por el chat '
            'y hagas grupo, para encontrar ahora los fallos que si no saldrían el 4 de noviembre. En la app de Battle.net ya aparece la versión '
            '<strong>«WoW: Forever – Prueba de estrés»</strong>.</p>'
            '<p><strong>Ojo:</strong> al terminar la prueba se <strong>borran todos los personajes</strong>, nombres incluidos, y se vuelve a abrir la beta. '
            'Es para jugar un rato y ayudar, no para empezar tu personaje de verdad.</p>'
            '<div class="divider"><h2>Cómo descargarla paso a paso</h2></div><ol class="pasos">' + pasos + '</ol>'
            '<p class="fine">¿No te sale la opción? Cierra y vuelve a abrir la app de Battle.net para que se actualice, y comprueba que tienes elegida la región de Europa.</p>'
            '<div class="divider"><h2>Lo que sabemos y lo que no</h2></div><div class="facts">'
            '<div class="fact ok"><h3>Confirmado</h3><ul>'
            '<li>Miércoles 21 de octubre a las 19:00, hora peninsular, para Europa (antes era el lunes 19). En México, a las 15:00; en Chile y Argentina, a las 18:00.</li>'
            '<li>Dura unas horas, en los servidores del lanzamiento; mientras tanto, la beta está apagada.</li>'
            '<li>Puede entrar cualquiera con cuenta de WoW, sin suscripción.</li>'
            '<li>Al cerrar se borran todos los personajes de la prueba, nombres incluidos.</li>'
            '<li>La versión «WoW: Forever – Prueba de estrés» ya está en la app de Battle.net y se puede preinstalar.</li>'
            '<li>La beta normal también termina el 21 de octubre y el juego sale el 4 de noviembre.</li></ul></div>'
            '<div class="fact wait"><h3>Aún sin confirmar</h3><ul>'
            '<li>Cuántas horas exactas: Blizzard solo dice «unas horas».</li>'
            '<li>El nivel máximo (en la beta normal es el 30).</li>'
            '<li>Las colas: es una prueba de estrés, así que habrá colas y algo de lag. Paciencia.</li></ul></div></div>'
            '<div class="divider"><h2>¿Juegas con Muchamiel?</h2></div><div class="beta-cta">'
            f'<img class="beta-face" src="{AVATAR}" alt="Muchamiel"><div><h3>¡Nos vemos dentro!</h3>'
            '<p>Muchamiel entrará a jugar con la comunidad. Síguele en directo para saber cuándo empieza y únete al Discord para hacer grupo, '
            'que subir con la peña es otra cosa.</p></div>' + socials_row() + '</div>'
            '<div class="divider"><h2>Llega preparado</h2></div><div class="tiles">'
            '<a class="tile" href="../clases/"><strong>Clases</strong><span>Builds, macros y duelos de las nueve clases.</span></a>'
            '<a class="tile" href="../razas/"><strong>Razas</strong><span>Qué raza elegir y sus raciales.</span></a>'
            '<a class="tile" href="../addons/"><strong>Addons</strong><span>Los imprescindibles para Forever.</span></a>'
            '<a class="tile" href="../comunes/"><strong>Guía de macros</strong><span>Cómo funcionan y cuáles valen para todas.</span></a></div>'
            f'<p class="fine">Fuente: <a href="{BLIZZ_ESTRES}" target="_blank" rel="noopener noreferrer">anuncio oficial de la prueba de estrés (Blizzard)</a>, '
            f'<a href="{BLIZZ_ESTRES_FORO}" target="_blank" rel="noopener noreferrer">aviso de Blizzard en su foro</a> y la propia app de Battle.net.</p>')
    page('beta-gratis', 'Juega gratis a WoW Forever el 21 de octubre a las 19:00: prueba de estrés | Muchamiel',
         'El miércoles 21 de octubre a las 19:00 WoW Forever se abre gratis a todo el mundo durante unas horas, sin suscripción. Qué es la prueba de estrés y cómo preinstalarla en Battle.net.', body)


# Reserva de nombres (Van, 15-10). Fuente principal: anuncio oficial de Blizzard «Crea un nombre verdaderamente tuyo en WoW: Forever».
BLIZZ_NOMBRES = 'https://news.blizzard.com/es-es/article/24304161/crea-un-nombre-verdaderamente-tuyo-en-wow-forever'
RESERVA_PASOS = [
    ('Hazte con una edición que la incluya', 'La reserva viene con el pack Heroico, el Épico o la Colección Warcraft Forever, en la tienda de Battle.net. Con la suscripción sola no se reserva: creas tu personaje el día del lanzamiento.'),
    ('Piensa varias combinaciones', 'Nombre y apellido. Si el que quieres ya está en uso, tener un plan B (y un plan C) te ahorra quedarte en blanco en el momento.'),
    ('El 27 de octubre a las 18:00, entra en Battle.net', 'World of Warcraft → versión WoW: Forever → Jugar. En Europa abre a las 18:00 (hora peninsular); en los servidores de América, a las 14:00 en México y a las 17:00 en Chile y Argentina.'),
    ('Elige bien las reglas', 'Normal, JcJ, Rol o Rol-JcJ (este último, nuevo desde el 22 de octubre). Cambiarlas después cuesta una transferencia de pago, y en las de JcJ solo puedes tener una facción por cuenta.'),
    ('Crea y personaliza tu personaje', 'Raza, clase, aspecto, nombre y apellido. Puedes dejar listos hasta tres personajes. Los nombres se reservan por orden de llegada.'),
    ('El 5 de noviembre, a jugar', 'A las 00:00 hora peninsular (en México, el 4 a las 17:00; en Chile y Argentina, el 4 a las 20:00) tu personaje te estará esperando con su nombre.'),
]


def reserva_page():
    pasos = ''.join(f'<li><strong>{E(t)}</strong><span>{E(d)}</span></li>' for t, d in RESERVA_PASOS)
    body = ('<p class="eyebrow">NOTICIA · RESERVA DE NOMBRES · ACTUALIZADA EL 28 DE OCTUBRE DE 2026</p><h1>Reserva tu nombre en WoW Forever: del 27 de octubre al 3 de noviembre</h1>'
            '<p class="lead">Una semana antes del lanzamiento podrás crear tus personajes y <strong>asegurar su nombre</strong>. En Forever cada personaje lleva '
            '<strong>nombre y apellido</strong>, y la combinación tiene que ser única en toda Europa. Te contamos cómo funciona, quién puede reservar y cómo hacerlo.</p>'
            '<div class="tfo-stats"><div><b data-countdown="2026-10-27">27 oct</b><span>para la reserva</span></div><div><b>3</b><span>personajes por cuenta</span></div>'
            '<div><b>Nombre + apellido</b><span>únicos en la región</span></div><div><b>5 nov</b><span>lanzamiento</span></div></div>'
            '<div class="prepare" style="border-color:#5fd38a"><h3>✅ Ya funciona (desde la noche del 27)</h3><p>La reserva abrió con retraso el martes por la noche, tras unos problemas técnicos. Si te da algún problema, mira esto antes de nada:</p><ul><li><strong>Horda bloqueada en JcJ:</strong> Blizzard está frenando la creación de personajes de la Horda en las reglas JcJ porque hay muchos más que de la Alianza. Es temporal: vuelve a probar más tarde o elige otras reglas.</li><li><strong>«Ese nombre está restringido»:</strong> están bloqueados los nombres de personajes de la historia (Fordring, Proudmoore…). Además, por un fallo, se bloqueaban nombres normales, como los que llevan «con». Blizzard lo arregla con el próximo reinicio de los servidores: si te pasó, vuelve a intentarlo después.</li><li><strong>Los nombres valen para todas las reglas:</strong> si alguien reserva un nombre en Normal, nadie lo puede usar tampoco en JcJ ni en Rol.</li><li><strong>«Estas reglas no están disponibles temporalmente»:</strong> espera un rato y vuelve a probar.</li></ul></div>'
            '<div class="prepare"><h3>Ya hay hora: martes 27 de octubre a las 18:00</h3><p>Blizzard ha publicado la hora de apertura: en Europa, <strong>el martes 27 de octubre a las 18:00</strong> (hora peninsular)*. Y un detalle importante: los <strong>3 personajes son en total</strong>, sumando todas las reglas. Si reservas dos en JcJ, solo te queda uno para Normal o Rol. Ese límite es solo para la reserva. <span class="latam">* En los servidores de América, donde juegan México, Chile y Argentina, abre a otra hora: México 14:00 · Chile y Argentina 17:00 (13:00 de la costa oeste de EE. UU.).</span></p></div>'
            '<div class="prepare"><h3>Novedad del 22 de octubre: también habrá reinos de Rol-JcJ</h3><p>Blizzard ha decidido añadir las reglas de <strong>Rol-JcJ</strong> (reinos de rol con combate entre jugadores en el mundo abierto) para el lanzamiento. Y están trabajando para que <strong>se puedan elegir ya en la reserva de nombres</strong> del 27. En el podcast de JcJ lo veían con dudas, pero han hecho caso a los jugadores.</p></div>'
            '<div class="divider"><h2>Cómo son los nombres en Forever</h2></div>'
            '<p>Como en Forever no hay reinos, los nombres ya no se reparten por reino sino por región, y para que haya sitio para todos cada personaje lleva <strong>dos nombres</strong>: '
            'un nombre y un apellido. Lo que tiene que ser único es <strong>la combinación</strong>: si alguien ya es «Kaelith Martillo», tú puedes ser «Kaelith Rompeolas».</p>'
            '<p>El apellido da mucho juego: puedes ponerle el mismo a todos tus personajes, como una familia (Blizzard pone el ejemplo de Asha, Thalen y Mira Vallebrillante), '
            'o usarlo con tu hermandad. Y si no te gusta verlo encima de la cabeza, puedes ocultarlo: <strong>Esc → Opciones → Placas de nombre → «Mi nombre secundario»</strong>. '
            'En el chat se sigue viendo.</p>'
            '<div class="divider"><h2>Cómo reservar, paso a paso</h2></div><ol class="pasos">' + pasos + '</ol>'
            '<div class="divider"><h2>Lo que no te van a dejar poner</h2></div><div class="facts">'
            '<div class="fact wait"><h3>Normas de nombres</h3><ul>'
            '<li>Tienen que cumplir el código de conducta de nombres del juego.</li>'
            '<li>Nada que suplante a Blizzard o al equipo de World of Warcraft, ni nombres que confundan.</li>'
            '<li>El sistema mira <strong>el nombre completo</strong>: partir una palabra prohibida entre el nombre y el apellido no cuela.</li>'
            '<li>En la beta Blizzard ya ha echado a jugadores por nombres inapropiados. No te la juegues con el que quieres conservar para siempre.</li></ul></div>'
            '<div class="fact ok"><h3>Si tu nombre ya está en uso</h3><ul>'
            '<li>Prueba otro apellido: el nombre puede repetirse si la combinación es distinta.</li>'
            '<li>Usa el generador de nombres aleatorios del juego para inspirarte.</li>'
            '<li>Nadie garantiza un nombre: se reservan por orden de llegada, así que cuanto antes, mejor.</li>'
            '<li>Si no tienes la edición, entra el primer día: los nombres más buscados volarán esa misma noche.</li></ul></div></div>'
            '<div class="divider"><h2>Prepárate mientras tanto</h2></div><div class="tiles">'
            '<a class="tile" href="../lanzamiento/"><strong>El lanzamiento</strong><span>Fechas, ediciones y todo lo nuevo de Forever.</span></a>'
            '<a class="tile" href="../clases/"><strong>Builds de nivel 60</strong><span>Elige clase con cabeza.</span></a>'
            '<a class="tile" href="../calculadora/"><strong>Calculadora</strong><span>Planifica tus talentos.</span></a>'
            '<a class="tile" href="../razas/"><strong>Razas</strong><span>Qué raza le va a tu clase.</span></a></div>'
            f'<p class="fine">Fuente: <a href="{BLIZZ_NOMBRES}" target="_blank" rel="noopener noreferrer">anuncio oficial de Blizzard sobre los nombres en WoW Forever</a>. '
            'Lo de las reglas JcJ y la transferencia de pago, de los datos de la beta. La hora de apertura, del <a href="https://news.blizzard.com/en-us/article/24303866/claim-your-world-of-warcraft-forever-character-names" target="_blank" rel="noopener noreferrer">aviso de Blizzard del 20 de octubre</a>. Lo del Rol-JcJ, del <a href="https://us.forums.blizzard.com/en/wow/t/the-roleplay-pvp-ruleset-is-coming-to-wow-forever/2389502" target="_blank" rel="noopener noreferrer">aviso de Blizzard del 22 de octubre</a>.</p>')
    page('reserva-nombres', 'Reserva de nombres en WoW Forever: fechas y cómo hacerla | Muchamiel',
         'Del 27 de octubre al 3 de noviembre puedes reservar el nombre y apellido de hasta tres personajes de WoW Forever. Quién puede, cómo se hace y qué nombres no se permiten.', body)


# Van 20-10: noticia de las 9 mazmorras (Blizzard, 20-10) + novedades confirmadas de la semana. Fuentes en la propia noticia.
BLIZZ_MAZMORRAS = 'https://news.blizzard.com/en-us/article/24301455/explore-the-new-dungeons-of-world-of-warcraft-forever'
MAZ_NUEVAS = [  # (slug de nuestra página, nombre, niveles, dónde, lo que cuenta Blizzard)
    ('salon-de-los-feudales', 'Salón de los Feudales', '13-18', 'Bajo Forjaz, Dun Morogh',
     'La cripta de los reyes enanos, invadida por lo que parecen enanos Hierro Negro. La Alianza la tiene al lado; la Horda tiene que cruzar territorio enemigo.'),
    ('ruinas-de-lordaeron', 'Ruinas de Lordaeron', '15-20', 'Sobre Entrañas, Claros de Tirisfal',
     'Los Renegados intentan recuperar la ciudad, llena de Plaga y con un nigromante ganando poder. Fácil para la Horda; la Alianza tiene que ir a territorio horda.'),
    ('excavacion-de-whelgar', 'Excavación (Excavation Site)', '24-29', 'Sobre la Excavación de Whelgar, Los Humedales',
     'Una niebla extraña baja de las montañas: más allá de la excavación hay un lugar congelado en el tiempo, con constructos titánicos y fauna peligrosa.'),
    ('ciudad-de-dalaran', 'Ciudad de Dalaran', '28-33', 'Montañas de Alterac',
     'Cae la barrera y la ciudad está llena de magia descontrolada. Necesita cadena de acceso en las dos facciones; se entra por las cloacas y hay varios caminos.'),
    ('ciudad-sumergida', 'Ciudad Sumergida (The Drowned City)', '35-40', "Frente a la costa de Tuercespina, al oeste de Grom'gol",
     'Ruinas trol que han salido del mar, con trols y nagas. Se entra buceando; es al aire libre y se va formando una tormenta hasta el jefe final.'),
    ('bastion-kroldok', "Bastión Krol'dok", '40-45', 'Riverglades',
     'Una fortaleza ogra enorme, con talleres y campamentos, de donde salen los que secuestran viajeros. De noche se oyen cánticos extraños.'),
    ('prision-de-alcaz', 'Prisión de Alcaz', '48-53', 'Isla de Alcaz, Marjal Revolcafango',
     'Por fin se abre la prisión de los rumores (se dijo que tuvo preso al rey Varian Wrynn). Dentro, la Hermandad Defias y los nagas en guerra.'),
    ('bastion-faucenegra', 'Bastión Faucenegra (Blackmaw Hold)', '55-60', 'Azshara',
     'Una gran ciudad de fúrbolgs tras una puerta sellada, luchando contra una corrupción. Mazmorra grande de nivel máximo, con varios caminos y jefes.'),
    ('bancal-del-creador', "Bancal del Creador (Shaper's Terrace)", '58-60', "Colinas del norte del Cráter de Un'Goro",
     "Una instalación titánica sobre Un'Goro, con dinosaurios y pozos de alquitrán. Hay que llevar cristales de poder del cráter y usarlos en las consolas de dentro."),
]


def mazmorras_nuevas_page():
    tiles = ''.join(f'<a class="tile" href="../mazmorras/{s}/"><strong>{E(n)}</strong><span><b>Nivel {E(lv)}</b> · {E(z)}. {E(d)}</span></a>'
                    for s, n, lv, z, d in MAZ_NUEVAS)
    body = ('<p class="eyebrow">NOTICIA · BLIZZARD · 20 DE OCTUBRE DE 2026</p><h1>Las 9 mazmorras nuevas de WoW Forever</h1>'
            '<p class="lead">Blizzard ha presentado las <strong>nueve mazmorras nuevas</strong> de WoW Forever, para grupos de cinco y del <strong>nivel 13 al 60</strong>, '
            'repartidas entre los Reinos del Este y Kalimdor. Aquí las tienes en orden de nivel; pulsa cualquiera para ver sus jefes, botín, misiones y cómo llegar.</p>'
            '<div class="tfo-stats"><div><b>9</b><span>mazmorras nuevas</span></div><div><b>13-60</b><span>niveles</span></div>'
            '<div><b>6 + 3</b><span>Reinos del Este + Kalimdor</span></div><div><b>5</b><span>jugadores por grupo</span></div></div>'
            '<div class="divider"><h2>Las nueve, de menor a mayor nivel</h2></div><div class="tiles">' + tiles + '</div>'
            '<div class="divider"><h2>Más novedades de esta semana</h2></div><ul>'
            '<li><strong>Prueba de estrés gratis: ahora el miércoles 21 a las 19:00.</strong> Blizzard la ha movido del lunes 19. En México, a las 15:00; en Chile y Argentina, a las 18:00. <a href="../beta-gratis/">Cómo entrar</a>.</li>'
            '<li><strong>Mano dura con el oro comprado.</strong> Blizzard ya no va solo a por los vendedores: también castiga a quien compra, y estrena unos '
            '<strong>bloqueos temporales de economía</strong> que impiden comerciar, usar el correo, el banco de hermandad y la casa de subastas a las cuentas sospechosas mientras lo revisan. '
            'En la beta ya ha cerrado cerca de <strong>4.000 cuentas</strong> por comprar o vender oro.</li>'
            '<li><strong>Podcast de PvP (episodio 4).</strong> Los personajes no se podrán pasar entre el modo JcJ y el normal: para cambiar hay que crear otro. '
            'No habrá reinos de rol JcJ al principio, aunque no lo descartan (<strong>actualización del 22 de octubre:</strong> sí los habrá desde el lanzamiento). Y lo de las capas en el JcJ del mundo abierto quieren arreglarlo para el lanzamiento, pero no lo garantizan.</li>'
            '<li><strong>Ojo con los «datamines».</strong> Blizzard avisa de que los gráficos que han salido de los archivos de la beta <strong>no son para esta versión</strong> del juego.</li>'
            '<li><strong>Lo siguiente:</strong> reserva de nombres del 27 de octubre al 3 de noviembre (<a href="../reserva-nombres/">cómo hacerla</a>) y lanzamiento el 5 de noviembre a las 00:00 (en México, el 4 a las 17:00; en Chile y Argentina, el 4 a las 20:00).</li></ul>'
            f'<p class="fine">Fuentes: <a href="{BLIZZ_MAZMORRAS}" target="_blank" rel="noopener noreferrer">Blizzard: las mazmorras nuevas de WoW Forever</a> · '
            f'<a href="{BLIZZ_ESTRES_FORO}" target="_blank" rel="noopener noreferrer">Blizzard: prueba de estrés el 21 de octubre</a> · '
            '<a href="https://www.pcgamer.com/games/world-of-warcraft/wow-forever-has-a-new-kind-of-ban-to-deal-with-real-money-trading/" target="_blank" rel="noopener noreferrer">PC Gamer: los bloqueos de economía</a> · '
            '<a href="https://www.icy-veins.com/wow-forever/news/nearly-4000-accounts-banned-due-to-rmt-wow-forever-beta/" target="_blank" rel="noopener noreferrer">Icy Veins: casi 4.000 cuentas cerradas</a> · '
            '<a href="https://www.icy-veins.com/wow-forever/news/the-pvp-episode-wow-forever-podcast-episode-4/" target="_blank" rel="noopener noreferrer">Icy Veins: el podcast de PvP</a>. '
            'Consultado el 20 de octubre de 2026.</p>')
    page('mazmorras-nuevas', 'Las 9 mazmorras nuevas de WoW Forever: niveles y dónde están | Muchamiel',
         'Las nueve mazmorras nuevas de WoW Forever del nivel 13 al 60, con niveles, zona y lo que cuenta Blizzard de cada una. Más las novedades de la semana.', body)


# Van 22-10: las bandas del 9 de diciembre y la cadena del amuleto de Onyxia (Blizzard, 20-10).
BLIZZ_BANDAS = 'https://worldofwarcraft.blizzard.com/en-us/news/24303009'
CADENA_ALIANZA = [
    'En las <strong>Estepas Ardientes</strong>, Helendis Riverhorn te da «Dragonkin Menace».',
    'Sigue la cadena «The True Masters» (seis misiones) sobre el Vuelo Negro y los orcos Roca Negra.',
    'El Mariscal Maxwell, en la Vigilia de Morgan, te manda a las <strong>Profundidades de Roca Negra</strong> a buscar al Mariscal Windsor (o la prueba de su muerte). Vuelves con «Abandoned Hope».',
    'Dentro de las Profundidades, los enemigos sueltan «A Crumpled Up Note»: llévasela a Windsor, que está en su celda.',
    'En «A Shred of Hope», recupera la información de Windsor que tienen Golem Lord Argelmach y General Angerforge.',
    'Ayuda a Windsor a escapar («Jail Break!») y vuelve con Maxwell.',
    'En las puertas de <strong>Ventormenta</strong>, el Escudero Rower hace venir a Windsor («Stormwind Rendezvous»).',
    'Haz «The Great Masquerade» en Ventormenta con más jugadores.',
    'Bolvar Fordragón te encarga «The Dragon&#39;s Eye».',
    'En la <strong>Cumbre de Roca Negra</strong> (superior), mata al General Drakkisath y quédate su sangre: con ella te dan el <strong>Drakefire Amulet</strong>.',
]
CADENA_HORDA = [
    'En las <strong>Tierras Inhóspitas</strong>, el señor de la guerra Goretooth te da «Blood and Thunder» en Kargath.',
    'Sigue con «Warlord&#39;s Command» en la <strong>Cumbre de Roca Negra inferior</strong>.',
    'Habla con Eitrigg en Orgrimmar y después con Thrall.',
    'En «For the Horde!», vuelve a la Cumbre inferior y tráele a Thrall la cabeza de Rend Puño Negro.',
    'Tras «What the Wind Carries», busca a Rexxar en Desolace («The Champion of the Horde»).',
    'Lleva el testamento de Rexxar a Myranda la Bruja, en las Tierras de la Peste del Oeste, y consigue los ojos de dracónido negro («Oculus Illusions»).',
    'Con el Amulet of Draconic Subversion, busca al draco Emberstrife en el <strong>Marjal Revolcafango</strong>.',
    'Haz las cuatro «The Test of Skulls»: las calaveras de Scryer, Somnus, Chronalis y Axtroz.',
    'Emberstrife te da el amuleto apagado («Ascension...»); llévaselo a Rexxar.',
    'En la <strong>Cumbre de Roca Negra</strong> (superior), quítale la sangre al General Drakkisath y vuelve con Rexxar: te da el <strong>Drakefire Amulet</strong>.',
]


def bandas_page():
    ol = lambda pasos: '<ol class="pasos">' + ''.join(f'<li><span>{p}</span></li>' for p in pasos) + '</ol>'
    body = ('<p class="eyebrow">NOTICIA · BLIZZARD · 20 DE OCTUBRE DE 2026</p><h1>Las bandas de WoW Forever: dónde están y cómo entrar en Onyxia</h1>'
            '<p class="lead">El <strong>9 de diciembre</strong> abren las tres primeras bandas de WoW Forever, todas de <strong>nivel 60</strong>. '
            'Blizzard ha contado dónde está cada una, para cuántos jugadores es y la cadena de misiones que hay que hacer para entrar en Onyxia.</p>'
            '<div class="tfo-stats"><div><b data-countdown="2026-12-09">9 dic</b><span>abren las bandas</span></div><div><b>3</b><span>bandas</span></div>'
            '<div><b>10 · 20 · 40</b><span>jugadores</span></div><div><b>Semanal</b><span>reinicio</span></div></div>'
            '<div class="divider"><h2>Las tres bandas</h2></div><table class="keys">'
            '<tr><th>Cavernas del Túmulo<br><small>10 jugadores · 8 jefes</small></th><td>Escondidas bajo Kalimdor, en el monte Hyjal. Tiene varias entradas: desde Hyjal, desde Cuna del Invierno y desde el Bastión Faucenegra. Sin cadena de acceso.</td></tr>'
            '<tr><th>Cima Hyjal<br><small>20 jugadores · 13 jefes</small></th><td>En lo alto del monte Hyjal, junto al Árbol del Mundo, Nordrassil. Empieza con un guardián antiguo y luego eliges entre varios caminos por la montaña. Sin cadena de acceso.</td></tr>'
            '<tr><th>Guarida de Onyxia<br><small>40 jugadores</small></th><td>En el Marjal Revolcafango. Es el combate de siempre, en tres fases y con mucho fuego: conviene llevar <strong>resistencia al fuego</strong>. Para entrar hace falta el <strong>Drakefire Amulet</strong>.</td></tr></table>'
            '<div class="prepare"><h3>Para entrar en Onyxia: el Drakefire Amulet</h3><p>Lo tiene que llevar <strong>cada jugador</strong> del grupo, en la bolsa (no hace falta ponérselo). '
            'Se consigue con una cadena de misiones distinta para cada facción, y las dos acaban matando al General Drakkisath en la Cumbre de Roca Negra. Empieza pronto: es larga y pasa por varias mazmorras.</p></div>'
            '<div class="divider"><h2>Cadena de la Alianza</h2></div>' + ol(CADENA_ALIANZA) +
            '<div class="divider"><h2>Cadena de la Horda</h2></div>' + ol(CADENA_HORDA) +
            '<p class="fine">Los nombres de las misiones van en inglés, como en el anuncio de Blizzard; en el juego en castellano pueden llamarse de otra forma.</p>'
            '<div class="divider"><h2>Prepárate</h2></div><div class="tiles">'
            '<a class="tile" href="../mazmorras/profundidades-de-roca-negra/"><strong>Profundidades de Roca Negra</strong><span>Media cadena de la Alianza pasa por aquí.</span></a>'
            '<a class="tile" href="../mazmorras/cumbre-de-roca-negra-inferior/"><strong>Cumbre de Roca Negra inferior</strong><span>Parada de la cadena de la Horda.</span></a>'
            '<a class="tile" href="../mazmorras/"><strong>Mazmorras y bandas</strong><span>Todo lo que trae Forever, de un vistazo.</span></a>'
            '<a class="tile" href="../builds-60/"><strong>Builds de nivel 60</strong><span>Prepara tu personaje para las bandas.</span></a></div>'
            f'<p class="fine">Fuente: <a href="{BLIZZ_BANDAS}" target="_blank" rel="noopener noreferrer">Blizzard: las bandas de WoW Forever, tamaños y cómo entrar</a> (20 de octubre de 2026). '
            'Blizzard puede cambiar las fechas. Los nombres de los jefes y las pistas del pódcast, en <a href="../a-medias/">A medias</a>.</p>')
    page('bandas-forever', 'Las bandas de WoW Forever y cómo entrar en Onyxia | Muchamiel',
         'Cavernas del Túmulo, Cima Hyjal y Guarida de Onyxia abren el 9 de diciembre en WoW Forever. Dónde están, para cuántos jugadores y la cadena del Drakefire Amulet de cada facción.', body)


# Van 22-10: la fiesta de fin de la beta (Blizzard, 22-10) en las dos facciones y lo que cuentan los jugadores (elementales en Ventormenta, botín del Núcleo de Magma).
BLIZZ_FIESTA = 'https://us.forums.blizzard.com/en/wow/t/the-wow-forever-beta-celebration-is-underway/2389633'


PODCAST5 = 'https://www.youtube.com/watch?v=uOlxa3xvNq4'
PODCAST6 = 'https://www.youtube.com/watch?v=BVyhnixdPQg'  # 29-10: tecnología (faseo, reinos, comunidades)


def fin_beta_page():
    # Van 22-10: «que entras y solo se ve letras»: apartado con imágenes (jefes, mapas, sets, botín). Datos: Blizzard (zonas y fechas) e Icy Veins (botín y jefes).
    Z = 'https://wow.zamimg.com/images/wow/icons/large/'
    MAPA = 'https://wow.zamimg.com/images/wow/maps/enus/normal/'
    WH = 'https://www.wowhead.com/classic/item='
    css = ('<style>'
           '.fb-hero{position:relative;border:1px solid #6b5426;border-radius:12px;overflow:hidden;padding:34px 26px;margin:6px 0 22px;'
           'background:linear-gradient(100deg,rgba(6,8,12,.94) 35%,rgba(6,8,12,.55)),url(' + MAPA + '12.jpg) center/cover}'
           '.fb-hero h1{margin:.2em 0 .3em}.fb-hero .lead{max-width:720px}'
           '.fb-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:14px 0}.fb-grid.g4{grid-template-columns:repeat(4,1fr)}'
           '.fb-card{display:flex;gap:14px;align-items:flex-start;padding:16px;border:1px solid #2c3444;border-left:3px solid #c99a3c88;border-radius:10px;background:#0f141d}'
           '.fb-card img{width:52px;height:52px;border-radius:8px;border:1px solid #6b5426;flex:none}'
           '.fb-card h3{margin:0 0 .25em;font-size:1.05rem}.fb-card p{margin:0;font-size:.93rem;line-height:1.45}'
           '.fb-boss{border-left-color:#a335ee}.fb-boss img{border-color:#a335ee;box-shadow:0 0 12px #a335ee55}'
           '.fb-mapas{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:14px 0}.fb-mapa.fb-c{grid-column:1/-1;aspect-ratio:auto;min-height:120px;background-size:contain;background-repeat:no-repeat;background-position:center 20%}'
           '.fb-mapa{position:relative;display:block;border-radius:10px;overflow:hidden;border:1px solid #2c3444;aspect-ratio:3/2;background:#0f141d center/cover;text-decoration:none}'
           '.fb-mapa span{position:absolute;left:0;right:0;bottom:0;padding:10px 12px;background:linear-gradient(transparent,rgba(6,8,12,.95));color:#fff;font-weight:700}'
           '.fb-mapa small{display:block;font-weight:400;color:#f4d27a}'
           '.fb-a{border-color:#2f5fa8}.fb-h{border-color:#a8302f}.fb-c{border-color:#c99a3c}'
           '.fb-sets{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:14px 0}'
           '.fb-set{display:flex;gap:12px;align-items:center;padding:12px;border:1px solid #2c3444;border-radius:10px;background:#0f141d}'
           '.fb-set img{width:44px;height:44px;border-radius:8px;flex:none}.fb-set .cl{border:1px solid #6b5426}.fb-set .pz{border:1px solid #a335ee}'
           '.fb-set b{display:block;color:#a335ee}.fb-set span{font-size:.88rem}'
           '.fb-loot{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:14px 0}'
           '.fb-loot a{display:flex;gap:10px;align-items:center;padding:8px 10px;border:1px solid #2c3444;border-radius:8px;background:#0f141d;text-decoration:none}'
           '.fb-loot img{width:36px;height:36px;border-radius:6px;border:1px solid #a335ee;flex:none}'
           '.fb-loot b{color:#a335ee;font-weight:600;font-size:.92rem}.fb-loot .leg img{border-color:#ff8000}.fb-loot .leg b{color:#ff8000}'
           '@media(max-width:900px){.fb-grid,.fb-grid.g4,.fb-loot{grid-template-columns:repeat(2,1fr)}.fb-mapas,.fb-sets{grid-template-columns:repeat(3,1fr)}}'
           '@media(max-width:620px){.fb-grid,.fb-grid.g4,.fb-loot,.fb-sets{grid-template-columns:1fr}.fb-mapas{grid-template-columns:1fr}.fb-hero{padding:24px 16px}}'
           '</style>')
    que = [
        ('inv_sword_39', 'Épicos de cualquier enemigo', 'Todos los enemigos, de cualquier nivel (hasta los lobos de nivel 1 de Villanorte), sueltan objetos <strong>del botín del Núcleo de Magma</strong>, al azar.'),
        ('inv_helmet_09', 'Sets de tier 1', 'Entre ese botín están <strong>los sets de tier 1</strong> de las nueve clases. Con suerte te vistes el set entero.'),
        ('inv_potion_61', 'Elixires muy fuertes', 'También caen elixires que suben muchísimo las estadísticas y el daño.'),
        ('spell_shadow_summoninfernal', 'Infernales del cielo', 'Caen infernales y otros enemigos del cielo, como en la beta del WoW original.'),
        ('spell_fire_elemental_totem', 'Elementales en Ventormenta', 'Los jugadores cuentan que hay elementales atacando Ventormenta.'),
        ('inv_misc_note_01', 'Versión rebajada', 'Los épicos tienen <strong>nivel bajo y menos estadísticas</strong> (están pensados para nivel 30, el tope de la beta). Y nada pasa al juego.'),
    ]
    jefes = [
        ('spell_shadow_shadowfury', 'Lord Kazzak', 'El señor del terror de las Tierras Devastadas, suelto por las zonas de inicio.'),
        ('inv_misc_head_dragon_blue', 'Azuregos', 'El dragón azul de Azshara, ahora donde menos te lo esperas.'),
        ('inv_misc_head_gnoll_01', 'Super Hogger', 'Hogger, el gnoll de Elwynn, en versión gigante.'),
        ('achievement_boss_patchwerk', 'Patchwerk', 'El más peligroso: <strong>sube un nivel cada vez que mata a alguien</strong>. Cuanto más tarde lo matéis, peor.'),
    ]
    zonas = [  # (id del mapa de Wowhead o None, zona, facción, clase css)
        (12, 'Bosque de Elwynn', 'Alianza · humanos', 'fb-a'), (1, 'Dun Morogh', 'Alianza · enanos y gnomos', 'fb-a'), (141, 'Teldrassil', 'Alianza · elfos de la noche', 'fb-a'),
        (14, 'Durotar', 'Horda · orcos y trols', 'fb-h'), (85, 'Claros de Tirisfal', 'Horda · no-muertos', 'fb-h'), (215, 'Mulgore', 'Horda · tauren', 'fb-h'),
        (None, 'Isla de Zephras', 'Cielonatos (las dos facciones)', 'fb-c'),
    ]
    sets = [  # (clase, imagen de la web, set, icono del casco, id del casco)
        ('Guerrero', 'warrior', 'Might', 'inv_helmet_09', 16866), ('Paladín', 'paladin', 'Lawbringer', 'inv_helmet_05', 16854),
        ('Cazador', 'hunter', 'Giantstalker', 'inv_helmet_05', 16846), ('Pícaro', 'rogue', 'Nightslayer', 'inv_helmet_41', 16821),
        ('Sacerdote', 'priest', 'Prophecy', 'inv_helmet_34', 16813), ('Chamán', 'shaman', 'Earthfury', 'inv_helmet_09', 16842),
        ('Mago', 'mage', 'Arcanist', 'inv_helmet_53', 16795), ('Brujo', 'warlock', 'Felheart', 'inv_helmet_08', 16808),
        ('Druida', 'druid', 'Cenarion', 'inv_helmet_09', 16834),
    ]
    botin = [  # (id, nombre, icono, para quién)
        (18842, 'Staff of Dominance', 'inv_staff_13', 'bastón de lanzador'), (18821, 'Quick Strike Ring', 'inv_jewelry_ring_07', 'anillo físico'),
        (17076, "Bonereaver's Edge", 'inv_sword_12', 'espada a dos manos'), (18816, "Perdition's Blade", 'inv_sword_48', 'daga'),
        (18805, 'Core Hound Tooth', 'inv_weapon_shortblade_11', 'daga'), (18832, 'Brutality Blade', 'inv_sword_15', 'espada'),
        (17104, 'Spinal Reaper', 'inv_axe_09', 'hacha a dos manos'), (17103, 'Azuresong Mageblade', 'inv_sword_39', 'espada de lanzador'),
        (17069, "Striker's Mark", 'inv_weapon_bow_08', 'arco'), (17063, 'Band of Accuria', 'inv_jewelry_ring_15', 'anillo físico'),
        (19147, 'Ring of Spell Power', 'inv_jewelry_ring_38', 'anillo de lanzador'), (18814, 'Choker of the Fire Lord', 'inv_jewelry_amulet_05', 'collar de lanzador'),
        (18820, 'Talisman of Ephemeral Power', 'inv_misc_stonetablet_11', 'abalorio de lanzador'), (19137, 'Onslaught Girdle', 'inv_belt_29', 'cinturón de placas'),
        (18809, 'Sash of Whispered Secrets', 'inv_belt_12', 'cinturón de tela'), (19146, 'Wristguards of Stability', 'inv_bracer_04', 'brazales de cuero'),
    ]
    card = lambda i, t, d, extra='': f'<div class="fb-card{extra}"><img src="{Z}{i}.jpg" alt="" loading="lazy"><div><h3>{t}</h3><p>{d}</p></div></div>'
    mapa = lambda z: (f'<div class="fb-mapa {z[3]}" style="background-image:url(' + (f'{MAPA}{z[0]}.jpg' if z[0] else '../assets/skyborne.svg') + f')"><span>{z[1]}<small>{z[2]}</small></span></div>')
    body = (css +
            '<div class="prepare"><h3>La beta ya se ha cerrado</h3><p>Terminó el viernes 23 de octubre. Si jugaste, puedes ver tus estadísticas (misiones, muertes y algunas muy raras) en <a href="https://timewalking.blizzard.com/" target="_blank" rel="noopener noreferrer">la página Timewalking de Blizzard</a>, y crear una imagen para compartirlas. Lo siguiente: la reserva de nombres, el martes 27 a las 18:00; en los servidores de América, a las 14:00 en México y a las 17:00 en Chile y Argentina (<a href="../reserva-nombres/">cómo hacerla</a>).</p></div>'
            '<div class="fb-hero"><p class="eyebrow">EVENTO · BETA DE WOW FOREVER · 22 Y 23 DE OCTUBRE DE 2026</p>'
            '<h1>Fin de la beta: épicos, sets y jefes de mundo</h1>'
            '<p class="lead">Hasta el <strong>viernes 23 de octubre a las 19:00</strong> (hora peninsular)*, Blizzard despide la beta con 24 horas de caos en las zonas de inicio '
            'de <strong>la Alianza y la Horda</strong>: todos los enemigos sueltan épicos del Núcleo de Magma, hay sets de tier 1 y jefes de mundo por todas partes. '
            '<span class="latam">* México: 11:00 · Chile y Argentina: 14:00.</span></p></div>'
            '<div class="tfo-stats"><div><b data-countdown="2026-10-23">23 oct</b><span>se cierra la beta</span></div><div><b>7</b><span>zonas con evento</span></div>'
            '<div><b>4</b><span>jefes de mundo</span></div><div><b>9</b><span>sets de tier 1</span></div></div>'
            '<div class="divider"><h2>Qué está pasando</h2></div><div class="fb-grid">' + ''.join(card(*q) for q in que) + '</div>'
            '<div class="divider"><h2>Jefes de mundo</h2></div>'
            '<p class="sub">Como en el final de otras betas, Blizzard ha llenado el mundo de jefes. Salen por las zonas del evento y no tienen un sitio fijo: si ves mucha gente corriendo hacia un sitio, síguela.</p>'
            '<div class="fb-grid g4">' + ''.join(card(i, t, d, ' fb-boss') for i, t, d in jefes) + '</div>'
            '<div class="divider"><h2>Dónde ir: las 7 zonas</h2></div>'
            '<p class="sub">Las zonas de inicio de todas las razas. Azul, Alianza; rojo, Horda. En la Horda, Durotar es la zona de Orgrimmar.</p>'
            '<div class="fb-mapas">' + ''.join(mapa(z) for z in zonas) + '</div>'
            '<div class="divider"><h2>Los sets de tier 1</h2></div>'
            '<p class="sub">Los nueve sets del Núcleo de Magma, uno por clase, con sus 8 piezas: casco, hombros, pechera, brazales, guantes, cinturón, piernas y botas. Pulsa para verlo en Wowhead.</p>'
            '<div class="fb-sets">' + ''.join(
                f'<a class="fb-set" href="{WH}{hid}" target="_blank" rel="noopener noreferrer"><img class="cl" src="../assets/{img}.jpg" alt="" loading="lazy">'
                f'<img class="pz" src="{Z}{ic}.jpg" alt="" loading="lazy"><span><b>{s}</b>{c}</span></a>' for c, img, s, ic, hid in sets) + '</div>'
            '<div class="divider"><h2>Botín destacado del Núcleo de Magma</h2></div>'
            '<p class="sub">Algunos de los épicos más famosos del Núcleo de Magma. Puede salirte cualquiera del botín de la banda; estos son los más buscados.</p>'
            '<div class="fb-loot">' + ''.join(
                f'<a href="{WH}{i}" target="_blank" rel="noopener noreferrer"><img src="{Z}{ic}.jpg" alt="" loading="lazy"><span><b>{n}</b><br><small>{p}</small></span></a>'
                for i, n, ic, p in botin) + '</div>'
            '<div class="facts"><div class="fact wait"><h3>Ojo</h3><ul>'
            '<li>Blizzard avisa de que en la fiesta habrá objetos y cosas que <strong>no estarán en el juego</strong> después del lanzamiento.</li>'
            '<li>Nada de la beta pasa al juego: el 4 de noviembre todos empiezan de cero.</li></ul></div>'
            '<div class="fact ok"><h3>Cómo entrar</h3><ul>'
            '<li>Hace falta acceso a la beta: viene con el pack Épico y la Colección Warcraft Forever.</li>'
            '<li>Battle.net → World of Warcraft → versión de la beta de WoW Forever → Jugar.</li>'
            '<li>Si no se actualiza, <strong>cierra del todo la app de Battle.net</strong> y vuelve a abrirla: es lo que recomendó Blizzard cuando la beta tardó en volver.</li></ul></div></div>'
            '<div class="divider"><h2>Más novedades de estos días</h2></div><ul>'
            '<li><strong>Habrá reinos de Rol-JcJ.</strong> Blizzard ha decidido añadirlos para el lanzamiento y quiere que ya se puedan elegir en la reserva de nombres del 27. <a href="../reserva-nombres/">La reserva de nombres</a>.</li>'
            '<li><strong>Las bandas del 9 de diciembre</strong>, y la cadena para entrar en Onyxia. <a href="../bandas-forever/">Las bandas</a>.</li>'
            '<li><strong>La acampada</strong>, con los datos oficiales de cada objeto de campamento. <a href="../profesiones/">Profesiones</a>.</li>'
            f'<li><strong>Podcast oficial, episodio 5:</strong> especial de fin de la beta. <a href="{PODCAST5}" target="_blank" rel="noopener noreferrer">Verlo en YouTube</a>.</li></ul>'
            f'<p class="fine">Fuentes: <a href="{BLIZZ_FIESTA}" target="_blank" rel="noopener noreferrer">aviso de Blizzard «The WoW Forever Beta Celebration is Underway»</a> (zonas y horario) · '
            '<a href="https://www.icy-veins.com/wow-forever/news/the-wow-forever-beta-is-going-out-with-murlocs-dropping-molten-core-loot/" target="_blank" rel="noopener noreferrer">Icy Veins: botín del Núcleo de Magma y jefes de mundo</a> · '
            '<a href="https://www.icy-veins.com/wow-forever/news/epics-from-normal-mobs-infernals-from-the-sky-wow-forever-beta-ending-event-starts-now/" target="_blank" rel="noopener noreferrer">Icy Veins: infernales y épicos</a>. '
            'Lo de los elementales de Ventormenta lo cuentan los jugadores. Mapas e iconos: Wowhead. Consultado el 22 de octubre de 2026.</p>')
    page('fin-beta', 'Fin de la beta de WoW Forever: épicos, sets y jefes de mundo | Muchamiel',
         'Hasta el 23 de octubre a las 19:00, todos los enemigos de las zonas de inicio de WoW Forever sueltan épicos del Núcleo de Magma y sets de tier 1, y hay jefes de mundo: Kazzak, Azuregos, Super Hogger y Patchwerk.', body)


# Van 22-10: «una sección de cosas nuevas a medias, así no liamos a la gente». Todo lo que no está confirmado del todo, con su etiqueta.
# Fuentes: pódcast oficial 5 (22-10), anuncios de Blizzard y guías que sacan datos de la beta. Al confirmarse algo, sale de aquí y va a su página.
A_MEDIAS = [  # (nivel, icono, título, texto, fuente)
    ('juego', 'inv_misc_book_09', 'Libros del mundo y la Investigación del mago',
     'Los libros que encuentras por el mundo se entregan a un bibliotecario (en la Torre de los Magos de Ventormenta para la Alianza y en Entrañas para la Horda) y dan experiencia. Por tramos de libros se eligen recompensas: primero un collar (aguante y espíritu, o agilidad y aguante), luego un anillo, '
     'y hacia el nivel 40 un arco, un escudo de sanador o una mano izquierda de fuego. No está claro cuántos libros pide cada tramo. '
     'El mago aprende además a <strong>investigar</strong> una vez al día con una pluma ligera y saca pergaminos; subiéndolo hay premios, entre ellos un arma para el mago cuerpo a cuerpo.',
     'Visto en la beta'),
    ('pista', 'inv_misc_bag_10', 'Un banco para toda la cuenta',
     'Blizzard estudia un banco compartido entre tus personajes, como el de la banda guerrera de Retail, para pasarte cosas sin usar el correo. Lo ve posible «en un futuro relativamente cercano», sin prometerlo.',
     'Entrevista a Blizzard'),
    ('pista', 'spell_nature_lightningshield', 'El chamán tanque',
     'El equipo dice que también lo quiere y que lo hablan a menudo, pero no hay fecha ni diseño.',
     'Entrevista a Blizzard'),
    ('confirmado', 'ability_mount_whitedirewolf', 'Monturas en los datos que no son de Forever',
     'En la beta aparecieron en los archivos una manada de lobos espectrales, una tortuga marina verde, un gallo carmesí, mascotas y conjuntos de transfiguración. Blizzard ha aclarado que <strong>no son para Forever</strong>. La tienda aparece desactivada en la creación de personajes.',
     'Blizzard · datos de la beta'),
    ('rumor', 'inv_misc_map_01', 'El Cráter de Azshara, rehecho',
     'En los datos del mapa el Cráter de Azshara aparece rehecho y casi terminado: lo más probable es que sea el Bastión Faucenegra, aunque podría ser un campo de batalla. También hay terreno nuevo al sur de Uldum y Gilneas completa.',
     'Datos del juego'),
    ('pista', 'achievement_bg_killxenemies_generalsroom', 'Ejércitos de 80 a 120 jugadores',
     'Tras las batallas enormes de la beta (Orgrimmar, Vallefresno), Blizzard estudia unir varios grupos en un «ejército» de 80 a 120 personas para eventos de hermandad, rol o JcJ. También que el servidor detecte las peleas grandes de JcJ en el mundo y les dé más potencia. Nada anunciado: hoy el máximo sigue siendo una banda de 40.',
     'Pódcast oficial, episodio 6'),
    ('pista', 'inv_misc_fish_02', 'Eventos para más adelante',
     'Ideas que barajan: más eventos de JcJ grandes, concursos de pesca, algo como la Luna de Sangre, la arena de Mak&#39;gora y ferias de temporada como la de la Luna Negra. Los jefes de mundo y los eventos de comunidad podrían adaptarse al nuevo sistema de fases. Sin fechas.',
     'Pódcast oficial, episodio 6'),
    ('juego', 'spell_frost_frostblast', 'Magos: Lanza de Hielo con 8 s de reutilización y talentos cambiados',
     'Han aparecido en el juego sin nota de Blizzard: <strong>Lanza de Hielo tiene ahora 8 segundos de reutilización</strong> (antes se podía encadenar), así que da para una por cada congelación. '
     'Talentos: <strong>Incineración</strong> pasa a 5 rangos y sube hasta un 10 % el crítico de Lanza de Fuego, Lanza de Hielo, Explosión Arcana y Agostar (antes 6 %); <strong>Masa crítica</strong> baja a 3 rangos y hasta un 6 % (antes 10 %); '
     '<strong>Precisión</strong> (antes Precisión elemental) da 2/4/6 % de golpe a <strong>todos</strong> los hechizos; desaparece <strong>Foco arcano</strong>; <strong>Acelerante</strong> (antes Bola de fuego mejorada) también acorta el lanzamiento de Ira arcana; '
     'y <strong>Frost Blast</strong> ya no se puede aprender. Varios talentos cambian de fila.',
     'Versión del juego del 28 de octubre (servidores de lanzamiento). Blizzard no ha publicado notas · recopilado por <a href="https://foreverchanges.pro/patch-notes" target="_blank" rel="noopener noreferrer">ForeverChanges</a>'),
    ('juego', 'spell_nature_ravenform', 'Cazadores: menos poder de ataque y raíces que comparten rendimientos decrecientes',
     '<strong>Aspecto del halcón</strong>: 15/22/30/38/47 de poder de ataque a distancia según el rango (antes, casi el doble). <strong>Aura de disparo certero</strong>: 15/22/30/40 (antes 30/40/50/75). '
     'Las raíces de Contraataque, Trampa enredadora y Corte de ala mejorado comparten ahora rendimientos decrecientes con Seccionar mejorado (guerrero) y Mordedura de escarcha (mago): cuantas más seguidas, menos duran.',
     'Versión del juego del 28 de octubre (servidores de lanzamiento). Blizzard no ha publicado notas · recopilado por <a href="https://foreverchanges.pro/patch-notes" target="_blank" rel="noopener noreferrer">ForeverChanges</a>'),
    ('juego', 'trade_engineering', 'Objetos: planeador y elixir',
     '<strong>Planeador goblin ultraligero</strong>: 5 minutos de reutilización (antes 3). <strong>Elixir de sabiduría</strong>: 3 de intelecto durante 30 minutos (antes 6 durante una hora). La <strong>gema corrupta</strong> pide nivel 60.',
     'Versión del juego del 28 de octubre (servidores de lanzamiento). Blizzard no ha publicado notas · recopilado por <a href="https://foreverchanges.pro/patch-notes" target="_blank" rel="noopener noreferrer">ForeverChanges</a>'),
    ('pista', 'inv_misc_head_dragon_01', 'Los jefes de las bandas nuevas',
     'Blizzard confirma <strong>más de 20 jefes nuevos</strong> entre las Cavernas del Túmulo (8) y Cima Hyjal (13), pero no ha dicho sus nombres. En el pódcast admiten que algunos nombres ya se ven en el sistema de Legado. '
     'Pistas que dieron: en las Cavernas, un jefe en el que te das una mejora de daño con un precio (si te pasas, mueres) y <strong>una pareja de arañas</strong>; '
     'en Hyjal, un <strong>dios salvaje no-muerto con forma de crocolisco</strong> poseído (primero el cuerpo, luego el espíritu, y vuelta a empezar) y un jefe de «terror corporal».',
     'Pódcast oficial, episodio 5'),
    ('rumor', 'inv_misc_book_09', 'Los nombres que circulan',
     'Salen de una demo de la BlizzCon y de los archivos de la beta. Cavernas del Túmulo: Deepscar Matriarch, Khalith the Dreadspinner, Amethrax, Ravus y Darlissa, Elder Tangleclaw, Well of Sorrow, Del&#39;lynar Songwood y Sonya Darkhallow. '
     'Cima Hyjal: Bandalar, Ancient of Decay, Time-Lost Battalion, Sylvestris Dusksong, Old Gloomlurker, Gharalis the Abyssal, Kathris the Haunted, Anara Chillwind, Elder Minderel, Tracker Stillwind, Council of Thorns, Nythus the Dreambound y The Wild King. '
     'Pueden cambiar antes de diciembre.',
     'Conquest Capped y Quissy (datos de la beta)'),
    ('pista', 'spell_fire_incinerate', 'Un Núcleo de Magma «renovado»',
     'Para el verano de 2027 Blizzard anuncia una «banda clásica renovada», sin decir cuál. En el pódcast, al preguntarles por el Núcleo de Magma, no quisieron dar detalles, pero dejaron caer que no será quedarse quieto pegando a Golemagg: '
     'tendrá algo más. Sin fecha ni confirmación de que sea esa banda.',
     'Pódcast oficial, episodio 5 · Blizzard: hoja de ruta'),
    ('confirmado', 'inv_sword_39', 'La misión legendaria de primavera',
     'Confirmada para la primavera de 2027, junto a dos bandas nuevas (10 y 20) y dos mazmorras. Blizzard no ha dicho qué arma será ni para qué clase.',
     'Blizzard: hoja de ruta'),
    ('pista', 'inv_misc_key_03', 'Mansiones y portales escondidos',
     'En el pódcast, Blizzard adelantó que hay <strong>mansiones</strong> y <strong>portales de instancias</strong> escondidos por el mundo que serán contenido «en el futuro», sin decir cuándo ni qué. '
     'Icy Veins los ha buscado en la beta: una mansión enorme nueva en la <strong>Mansión Mistmantle</strong> (Bosque del Ocaso); portales de mazmorra en <strong>Bael Modan</strong> (Los Baldíos), en la <strong>Excavación Rustmaul</strong> (Las Mil Agujas), '
     'junto a <strong>Farholde Keep</strong> (Riverglades) y en la <strong>granja enana de Los Humedales</strong>; <strong>un portal de banda</strong> dentro del Bancal del Creador (Un&#39;Goro); una zona nueva cerrada en Windshear Crag (Sierra Espolón); '
     'restos del Enclave Escarlata de Season of Discovery en Nuevo Avalon (Tierras de la Peste del Este); y <strong>Gilneas</strong>, rodeada de tiburones y huargen de nivel 63. Ninguno se puede usar aún.',
     'Pódcast oficial, episodio 5 · <a href="https://www.icy-veins.com/wow-forever/news/wow-forever-is-hiding-instance-portals-nobody-can-enter-yet/" target="_blank" rel="noopener noreferrer">Icy Veins</a> (beta)'),
    ('pista', 'inv_misc_gem_01', '¿Joyería e Inscripción?',
     'En la beta hay un aprendiz de joyero en Dalaran y un escriba en Durotar que te dicen que vuelvas más adelante, y la habilidad de Inscripción ya sale en la hoja de personaje. Blizzard no lo ha anunciado.',
     'Cliente de la beta'),
    ('confirmado', 'achievement_bg_killxenemies_generalsroom', 'Reinos Hardcore',
     'Blizzard ha dicho que llegarán, pero más adelante y sin fecha. Al lanzamiento habrá Normal, JcJ, Rol y Rol-JcJ.',
     'Blizzard'),
    ('pista', 'spell_fire_fire', 'Las hogueras harán menos daño',
     'En la beta la gente usaba las hogueras para matar a otros jugadores. Dicen que lo van a revisar sin quitarles todo el daño. No han dicho cómo quedará.',
     'Pódcast oficial, episodio 5'),
    ('pista', 'inv_misc_bag_10', 'Botín de misiones para todo el grupo',
     'Se lo pidieron en el pódcast: que los objetos de misión salgan para todo el grupo. Respuesta: «nunca digas nunca». Ya lo han mejorado algo y no descartan ajustarlo más.',
     'Pódcast oficial, episodio 5'),
    ('pista', 'inv_misc_map_01', 'Jugar con gente de América',
     'No al lanzamiento: Europa y América van separadas. No lo descartan para más adelante, pero tiene complicaciones técnicas. Dentro de Europa sí eliges tu idioma preferido en las opciones.',
     'Pódcast oficial, episodio 5'),
    ('pista', 'inv_misc_key_03', 'Algo parecido a una sintonización en las bandas nuevas',
     'Onyxia sigue con su cadena de siempre, por personaje. Las Cavernas del Túmulo y Cima Hyjal no tendrán una sintonización que te impida entrar, pero sí «algo parecido» que habrá que descubrir investigando para tener la experiencia completa. '
     'Y para más adelante: «no hay un mundo en el que no hagamos sintonizaciones», cada banda a su manera.',
     'Pódcast oficial, episodio 3'),
    ('pista', 'spell_shadow_shadowfury', 'Jefes de mundo: ¿instanciados o no?',
     'En Season of Discovery los metieron en instancias. Para Forever no lo han decidido: quieren recuperar la pelea por un recurso escaso, sin prometer nada.',
     'Pódcast oficial, episodio 4'),
    ('pista', 'achievement_bg_killxenemies_generalsroom', 'Eventos de JcJ en el mundo',
     'Les gustaría traer eventos de Season of Discovery como la Batalla por Vallefresno o la Luna de Sangre de Tuercespina. Las torres de las Tierras de la Peste del Este y la guerra de Silithus <strong>no estarán al lanzamiento</strong>; querrían rehacerlas más adelante.',
     'Pódcast oficial, episodio 4'),
    ('pista', 'inv_sword_39', 'Arena de duelos y desafíos entre grupos',
     'Ya existe una arena de duelos en un cráter del monte Hyjal (se usó en el torneo), con vendedores y quizá un PNJ que reinicia recargas, pero «no está lista». Podría abrirse en un parche futuro o por temporadas, como la Feria de la Luna Negra. '
     'Los desafíos de grupo contra grupo en campos de batalla (sin honor) llegarían «poco después» del lanzamiento.',
     'Pódcast oficial, episodio 4'),
    ('pista', 'inv_misc_note_01', 'Arenas y JcJ puntuado',
     'Muy reacios: no quieren arenas como en Burning Crusade ni estadísticas solo de JcJ. Prefieren peleas de 10 contra 10 y 15 contra 15. No lo descartan del todo.',
     'Pódcast oficial, episodio 4'),
    ('pista', 'inv_misc_map_01', 'Zonas nuevas y zonas «de mazmorra abierta»',
     'Quieren ir a <strong>Gilneas, Uldum y Quel&#39;Thalas</strong> (salieron en la BlizzCon), sin fecha. También hablan de zonas como Stromgarde, convertidas en zonas abiertas de nivel alto, y de entradas de mazmorra en zonas altas: '
     '«puede que ya haya una y nadie la haya encontrado».',
     'Pódcast oficial, episodios 1 y 3'),
    ('pista', 'inv_misc_bag_10', 'Botín y recetas ocultos',
     'Los objetos no aparecen en los archivos hasta que alguien los consigue: nadie sabe aún qué suelta cada jefe. Y habrá recetas raras sin descubrir, por ejemplo de bombas de Ingeniería, que solo saldrán farmeando.',
     'Pódcast oficial, episodios 4 y 5'),
    ('confirmado', 'inv_misc_head_dragon_blue', 'Modelos nuevos de los cielonatos',
     'Tras las críticas a sus modelos, llegarán unos nuevos en la primera gran actualización, a principios de 2027. Habrá entrada de blog.',
     'Pódcast oficial, episodio 3'),
    ('pista', 'inv_misc_book_09', 'Doble especialización',
     'Ahora se activa a nivel 40. Están hablando de si cambiar ese nivel.',
     'Pódcast oficial, episodio 3'),
    ('pista', 'inv_misc_gem_01', 'Sacerdotes cielonatos en la Horda',
     'Los cielonatos de la Horda no pueden ser sacerdotes. Lo piden mucho y la respuesta fue «nunca digas nunca».',
     'Pódcast oficial, episodio 1'),
]
A_MEDIAS_NIVEL = {
    'juego': ('EN EL JUEGO · SIN NOTA OFICIAL', '#4f7fd0'),
    'confirmado': ('CONFIRMADO, SIN DETALLES', '#3d9a5b'),
    'pista': ('PISTA DE BLIZZARD', '#c99a3c'),
    'rumor': ('RUMOR · DATOS DE LA BETA', '#a8302f'),
}


def a_medias_page():
    Z = 'https://wow.zamimg.com/images/wow/icons/large/'
    css = ('<style>'
           '.am-ley{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin:10px 0 18px}'
           '.am-tag{display:inline-block;padding:3px 9px;border-radius:999px;font-size:.72rem;font-weight:700;letter-spacing:.04em;color:#06080c}'
           '.am-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin:14px 0}'
           '.am-card{display:flex;gap:14px;align-items:flex-start;padding:16px;border:1px solid #2c3444;border-left:4px solid var(--am);border-radius:10px;background:#0f141d}'
           '.am-card img{width:52px;height:52px;border-radius:8px;border:1px solid #6b5426;flex:none}'
           '.am-card h3{margin:.35em 0 .3em;font-size:1.05rem}.am-card p{margin:0;font-size:.93rem;line-height:1.5}'
           '.am-card .am-src{margin-top:8px;font-size:.8rem;opacity:.75}'
           '@media(max-width:760px){.am-grid{grid-template-columns:1fr}}'
           '</style>')
    tag = lambda n: f'<span class="am-tag" style="background:{A_MEDIAS_NIVEL[n][1]}">{A_MEDIAS_NIVEL[n][0]}</span>'
    cards = ''.join(f'<div class="am-card" style="--am:{A_MEDIAS_NIVEL[n][1]}"><img src="{Z}{i}.jpg" alt="" loading="lazy"><div>{tag(n)}<h3>{t}</h3><p>{d}</p>'
                    f'<p class="am-src">Fuente: {f}</p></div></div>' for n, i, t, d, f in A_MEDIAS)
    body = (css + '<p class="eyebrow">NOTICIAS · ACTUALIZADO EL 29 DE OCTUBRE DE 2026</p><h1>A medias: lo que aún no es seguro</h1>'
            '<p class="lead">Aquí va todo lo de WoW Forever que <strong>todavía no está confirmado del todo</strong>: pistas que ha soltado Blizzard, cosas anunciadas sin detalles y lo que sale de los archivos de la beta. '
            'Así no lo mezclamos con lo seguro. Cuando Blizzard lo confirme, pasa a su página.</p>'
            '<div class="am-ley">' + tag('juego') + tag('confirmado') + tag('pista') + tag('rumor') + '</div>'
            '<div class="am-grid">' + cards + '</div>'
            '<div class="divider"><h2>Y esto ya es seguro: lo dijeron en el pódcast</h2></div><ul>'
            '<li><strong>Mazmorras sin mapa ni diario</strong>, y sin piedras de encuentro que invoquen: el viaje es parte de la mazmorra.</li>'
            '<li><strong>Las mazmorras dan un 20 % más de experiencia por enemigo</strong>, pero repetirlas en bucle no será lo más rápido: quieren que salgas al mundo.</li>'
            '<li><strong>Más de mil misiones nuevas</strong>, sobre todo a partir de Riverglades (nivel 40).</li>'
            '<li><strong>Vuelve el rango 14</strong> con su armadura. El Valle de Alterac dará menos honor y los demás campos de batalla bastante más, para que compense rotarlos.</li>'
            '<li><strong>Los grupos hechos se enfrentan a grupos hechos</strong>: si vas solo o con pocos amigos no deberías caer contra uno.</li>'
            '<li><strong>En los reinos JcJ no protegerán a los de nivel bajo</strong> de los de nivel 60: solo intervienen si hay trampas.</li>'
            '<li><strong>Sin buffs de mundo dentro de las bandas.</strong> Los consumibles clásicos siguen todos, y las resistencias cuentan.</li>'
            '<li><strong>Mano dura con el oro comprado</strong>: en la beta cerraron más de 2.100 cuentas de compradores y unas 1.600 de vendedores y bots.</li></ul>'
            '<div class="divider"><h2>Pódcast 6 (29 de octubre): cómo funcionan los servidores</h2></div><ul>'
            '<li><strong>Sin reinos de los de antes:</strong> eliges reglas (Normal, JcJ, Rol o Rol-JcJ) y a jugar. Puedes jugar con amigos de toda Europa; América sigue aparte.</li>'
            '<li><strong>Menos saltos de fase al cruzar de zona:</strong> en la beta la gente desaparecía al pasar de una zona a otra. Lo han mejorado mucho al final de la beta y habrá más arreglos para el lanzamiento, aunque avisan de que algún cambio de «mundo» seguirá pasando.</li>'
            '<li><strong>Unirte a un grupo ya no te cambia de mundo de golpe:</strong> te sale un aviso y eliges cuándo pasar.</li>'
            '<li><strong>Te ponen con gente conocida:</strong> el juego intenta meterte en la misma fase que tu hermandad, tus amigos y la gente con la que ya has jugado, para que haya comunidad. El idioma del cliente también cuenta.</li>'
            '<li><strong>Zonas con gente, pero sin agobios:</strong> en la beta Páramos de Poniente y Los Baldíos se llenaron demasiado y bajaron el tope. El primer día habrá más gente nueva en Durotar que en Orgrimmar.</li>'
            '<li><strong>Equilibrio de facciones:</strong> buscan cerca del 50 % en cada tipo de reglas. Si una facción se pasa del límite, <strong>pueden bloquear la creación de personajes</strong> de esa facción.</li>'
            '<li><strong>JcJ y JcE siguen separados</strong>, cada uno con su economía.</li>'
            '<li><strong>Ignorar a alguien no lo saca de tu mundo</strong>: solo dejas de leerle.</li>'
            '<li><strong>Sin casas (housing)</strong> en Forever.</li>'
            '<li><strong>El lanzamiento no trae eventos grandes nuevos:</strong> primero que todo funcione, y el contenido llegará poco a poco. Rehicieron el sistema de eventos tras los problemas de la Batalla por Vallefresno.</li>'
            '<li><strong>El pódcast descansa la semana del lanzamiento</strong> y vuelve dos semanas después con un episodio de historia.</li></ul>'
            '<div class="divider"><h2>Curiosidades vistas en la beta</h2></div>'
            '<p>Cosas que se han visto jugando la beta. Pueden cambiar al lanzamiento y algunos nombres aún no los sabemos en castellano.</p><ul>'
            '<li><strong>Mascota secreta en Entrañas:</strong> con un personaje de la Horda, compra comida para babosas en el Apothecarium, busca el cieno excitable de la piscina verde y báilale (/bailar) varias veces hasta que se haga amigo. Te da una misión y aprendes la mascota, que es para toda la cuenta.</li>'
            '<li><strong>La antorcha del Bosque del Ocaso:</strong> junto a los cadáveres de la Guardia Nocturna que hay por la zona se activa una misión que te da la antorcha.</li>'
            '<li><strong>Ranas cantoras en la Isla de Zephras</strong> (la zona inicial de los célicos): seleccionas una de las cinco ranas, escribes /cantar y al final aparece una que te regala una mascota. Guiño a Zelda.</li>'
            '<li><strong>Atajo al Marjal Revolcafango:</strong> en el norte del Desierto de Sal (Las Mil Agujas) hay una subzona nueva, con un árbol quemado y unos tablones que bordean el mapa, que lleva al Marjal sin cruzar Los Baldíos.</li>'
            '<li><strong>Casa de subastas del mercado negro:</strong> como la de Retail. En la beta salió una montura tortuga desde unos 3.000 de oro, y solo se la lleva una persona.</li>'
            '<li><strong>Cadena del Mártir</strong> (pechera, la sueltan bichos de las Cavernas de Brazanegra): si mueres con ella puesta, hace daño sagrado a los enemigos que tengas cerca.</li>'
            '<li><strong>Pala de saqueatumbas</strong> (la suelta Dextren en las Mazmorras de Ventormenta, 20 usos): para cavar tumbas en Cerro del Cuervo y en el cementerio del Monasterio Escarlata. Sobre todo da musgo de tumba.</li>'
            '<li><strong>Ojo con el mortero goblin:</strong> al recargarlo con Ingeniería puede salir mal, mandarte por los aires y matarte.</li>'
            '<li><strong>Fingir muerte puede matarte:</strong> si dejas que dure hasta el final, el cazador muere de verdad.</li>'
            '<li><strong>Iconos de raza clásicos:</strong> si eliges los modelos clásicos, el icono de la raza también es el antiguo.</li>'
            '<li><strong>Tormentas de verdad:</strong> con la lluvia hay truenos y relámpagos que iluminan la zona.</li>'
            '<li><strong>La isla de los GM</strong> se ve en el horizonte desde Teldrassil gracias a la nueva distancia de visión. No se puede llegar.</li>'
            '<li><strong>Un goblin junto a una arena vacía</strong> en Riverglades dice que aún no funciona. Blizzard sigue sin querer arenas como en Burning Crusade.</li></ul>'
            '<div class="divider"><h2>Lo seguro, aquí</h2></div><div class="tiles">'
            '<a class="tile" href="../bandas-forever/"><strong>Las bandas</strong><span>Lo confirmado de las tres bandas y la cadena de Onyxia.</span></a>'
            '<a class="tile" href="../calendario/"><strong>Calendario</strong><span>Todas las fechas oficiales.</span></a>'
            '<a class="tile" href="../lanzamiento/"><strong>El lanzamiento</strong><span>Lo que trae Forever el 4 de noviembre.</span></a>'
            '<a class="tile" href="../noticias/"><strong>Noticias</strong><span>Lo último, con fuentes.</span></a></div>'
            f'<p class="fine">Fuentes: pódcast oficial de WoW Forever, episodios '
            '<a href="https://www.youtube.com/watch?v=m49-jvGPCkA" target="_blank" rel="noopener noreferrer">1</a> · <a href="https://www.youtube.com/watch?v=uDRcv_w85j8" target="_blank" rel="noopener noreferrer">2</a> · <a href="https://www.youtube.com/watch?v=LwOWAf06YPg" target="_blank" rel="noopener noreferrer">3</a> · <a href="https://www.youtube.com/watch?v=bzaMA5fZ1tE" target="_blank" rel="noopener noreferrer">4</a> · '
            f'<a href="{PODCAST5}" target="_blank" rel="noopener noreferrer">5</a> · <a href="{PODCAST6}" target="_blank" rel="noopener noreferrer">6</a> (septiembre y octubre de 2026) · '
            f'<a href="{BLIZZ_BANDAS}" target="_blank" rel="noopener noreferrer">Blizzard: las bandas</a> · '
            '<a href="https://conquestcapped.com/guides/wow-forever/wow-forever-barrow-deeps-guide/" target="_blank" rel="noopener noreferrer">Conquest Capped: Cavernas del Túmulo</a> · '
            '<a href="https://quissy.tv/forever/raids/hyjal-summit/" target="_blank" rel="noopener noreferrer">Quissy: Cima Hyjal</a>.</p>')
    page('a-medias', 'A medias: lo que aún no es seguro de WoW Forever | Muchamiel',
         'Pistas de Blizzard, anuncios sin detalles y datos de la beta de WoW Forever, separados de lo confirmado: jefes de las bandas nuevas, Núcleo de Magma renovado, legendaria, Hardcore y más.', body)


# Van 26-10: noticia del repaso final de raciales (Blizzard, 26-10, notas de desarrollo). Los textos de cada racial, en raciales_15oct.RACIALES_26.
RAC26 = [  # (imagen, raza, facción, [(signo, texto)])
    ('race_human_male.jpg', 'Humano', 'Alianza', [('▼', 'Ruthless: +1 % de crítico (era 2 %).'), ('▲', 'Human Spirit: +10 % de espíritu (era 5 %).')]),
    ('race_dwarf_male.jpg', 'Enano', 'Alianza', [('▼', 'Se quita Earth Fury (2 % de daño y sanación críticos).'), ('▲', 'Nueva: Artisan&#39;s Precision, +1 % de golpe con hechizos y ataques.')]),
    ('race_orc_male.jpg', 'Orco', 'Horda', [('▼', 'Se quita Savage (1 % de crítico).'), ('▲', 'Vuelve Command: +5 % de daño a las mascotas de brujos y cazadores.'), ('▲', 'Blood Fury: 2 min de reutilización (eran 3).')]),
    ('race_tauren_male.jpg', 'Tauren', 'Horda', [('▲', 'Plainsrunning: 2 % por acumulación, hasta un 60 % de velocidad (era 30 %).'), ('▼', 'Plainsrunning ya no funciona montado. Endurance se queda solo en +5 % de vida.')]),
    ('race_troll_male.jpg', 'Trol', 'Horda', [('▲', 'Berserking dura 15 s (eran 10).')]),
    ('race_scourge_male.jpg', 'No-muerto', 'Horda', [('▲', 'Touch of the Grave: 15 s de reutilización interna (eran 25).')]),
    ('skyborne.svg', 'Célicos', 'Las dos facciones', [('▼', 'Wind Blessed: 2 % de celeridad (era 3 %).'),
        ('●', 'Read Ley Line: +50 % de regeneración 15 s; usada en una línea ley, «Attuned» 1 hora al 100 %. No se puede usar con Innervate.'),
        ('●', 'Skysight: +15 % de velocidad 15 s; usada en una convergencia elemental, «Charged» 1 hora al 30 %.'),
        ('●', 'Las dos mejoras de 1 hora se mantienen aunque mueras, pero se pierden al entrar en una banda.')]),
]


def raciales26_page():
    css = ('<style>.rc-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin:14px 0}'
           '.rc{display:flex;gap:14px;align-items:flex-start;padding:16px;border:1px solid #2c3444;border-left:3px solid #c99a3c88;border-radius:10px;background:#0f141d}'
           '.rc img{width:64px;height:64px;border-radius:10px;border:1px solid #6b5426;flex:none;object-fit:cover;background:#0b0f16}'
           '.rc h3{margin:0 0 .2em}.rc small{color:#f4d27a}.rc ul{margin:.5em 0 0;padding-left:0;list-style:none}.rc li{margin:.25em 0;font-size:.93rem}'
           '.rc .up{color:#5fd38a}.rc .dn{color:#e06a5f}.rc .eq{color:#c99a3c}.rc.full{grid-column:1/-1}'
           '@media(max-width:760px){.rc-grid{grid-template-columns:1fr}}</style>')
    sg = {'▲': 'up', '▼': 'dn', '●': 'eq'}
    cards = ''.join(f'<div class="rc{" full" if i == len(RAC26) - 1 else ""}"><img src="../assets/{img}" alt="" loading="lazy"><div><h3>{raza}</h3><small>{fac}</small><ul>'
                    + ''.join(f'<li><b class="{sg[s]}">{s}</b> {x}</li>' for s, x in cambios) + '</ul></div></div>'
                    for i, (img, raza, fac, cambios) in enumerate(RAC26))
    body = (css + '<p class="eyebrow">NOTICIA · BLIZZARD · 26 DE OCTUBRE DE 2026</p><h1>Cambian las raciales de WoW Forever a una semana del lanzamiento</h1>'
            '<p class="lead">Blizzard ha hecho el <strong>último repaso de las raciales</strong> antes del 4 de noviembre. Vuelven raciales pensadas para un rol o una clase en lugar de las genéricas de la beta, '
            'y retoca las que daban ventaja de más. Las de especialización en armas (espadas del humano, hachas del orco…) <strong>no vuelven</strong>: no quieren que el botín de las bandas dependa del tipo de arma.</p>'
            '<div class="tfo-stats"><div><b>7</b><span>razas cambian</span></div><div><b>+1 %</b><span>golpe del enano</span></div><div><b>60 %</b><span>velocidad del tauren</span></div><div><b>27 oct</b><span>reserva de nombres</span></div></div>'
            '<div class="divider"><h2>Raza a raza</h2></div><div class="rc-grid">' + cards + '</div>'
            '<p class="sub">▲ mejora · ▼ empeora · ● cambia. Elfos de la noche y gnomos no cambian. El 27 de octubre Blizzard añadió al aviso los cambios del orco (Blood Fury), el trol y el no-muerto, que se les habían olvidado.</p>'
            '<div class="prepare"><h3>¿Te cambia la raza que elegir?</h3><p>Mañana, martes 27 a las 18:00 (hora peninsular)*, se abre la reserva de nombres y la creación de personajes. '
            'Si dudabas de raza, míralo antes: el enano gana golpe, que siempre se agradece al principio, y el orco vuelve a ser la raza de los brujos y cazadores con mascota. '
            '<span class="latam">* En los servidores de América: México 14:00 · Chile y Argentina 17:00.</span></p></div>'
            '<div class="divider"><h2>Más</h2></div><div class="tiles">'
            '<a class="tile" href="../razas/"><strong>Razas</strong><span>Todas las raciales, ya al día.</span></a>'
            '<a class="tile" href="../cambios/"><strong>Notas del parche</strong><span>Todos los cambios, por clase.</span></a>'
            '<a class="tile" href="../reserva-nombres/"><strong>Reserva de nombres</strong><span>Cómo hacerla mañana.</span></a>'
            '<a class="tile" href="../a-medias/"><strong>A medias</strong><span>Lo que aún no es seguro.</span></a></div>'
            '<p class="fine">Fuente: <a href="https://us.forums.blizzard.com/en/wow/t/wow-forever-beta-development-notes-updated-october-26/2360696/7" target="_blank" rel="noopener noreferrer">Blizzard: notas de desarrollo de WoW Forever, 26 de octubre</a>.</p>')
    page('raciales-forever', 'Cambian las raciales de WoW Forever antes del lanzamiento | Muchamiel',
         'Repaso final de raciales de WoW Forever (26 y 27 de octubre): humano, enano, orco, tauren, trol, no-muerto y célicos cambian a una semana del lanzamiento. Raza a raza, en castellano.', body)


# Van 29-10: «Día 1 en WoW Forever». Fuentes: guías de Blizzard del 28-10 (jugadores nuevos) y 29-10 (los que vuelven) y las páginas de la web.
BLIZZ_NUEVOS = 'https://worldofwarcraft.blizzard.com/en-us/news/24315280'
BLIZZ_VUELVEN = 'https://worldofwarcraft.blizzard.com/en-us/news/24315643'


def dia1_page():
    body = ('<p class="eyebrow">GUÍA · LANZAMIENTO · JUEVES 5 DE NOVIEMBRE</p><h1>Día 1 en WoW Forever: qué hacer antes y en las primeras horas</h1>'
            '<p class="lead">WoW Forever sale el <strong>jueves 5 de noviembre a las 00:00</strong> (hora peninsular)*. Aquí tienes lo que conviene dejar listo antes y lo que te ahorrará tiempo en las primeras horas, con lo que ha publicado Blizzard esta semana. '
            '<span class="latam">* México: miércoles 4 a las 17:00 · Chile y Argentina: miércoles 4 a las 20:00.</span></p>'
            '<div class="tfo-stats"><div><b data-countdown="2026-11-05">5 nov</b><span>sale Forever</span></div><div><b>1-60</b><span>niveles</span></div>'
            '<div><b>+1.000</b><span>misiones nuevas</span></div><div><b>9</b><span>mazmorras nuevas</span></div></div>'
            '<div class="divider"><h2>Antes de que salga (el miércoles)</h2></div><ol class="pasos">'
            '<li><strong>Instálalo ya</strong><span>Battle.net → World of Warcraft → en «Versión del juego», WoW: Forever → Instalar. Actualiza también los controladores de la tarjeta gráfica.</span></li>'
            '<li><strong>Suscripción o tiempo de juego activos</strong><span>Forever va incluido en la suscripción. Los packs solo añaden extras (célicos, reserva de nombres, montura…). <a href="../pagar-menos/">Cuánto cuesta y cómo pagar menos</a>.</span></li>'
            '<li><strong>Prepara los addons</strong><span>Deja instalados los que vayas a usar (interfaz, misiones, subasta). <a href="../addons/">Los addons para Forever</a>. Si jugaste la beta o la prueba de estrés, guarda las carpetas <code>WTF</code> e <code>Interface</code> y cópialas en la instalación nueva para no rehacer tu interfaz.</span></li>'
            '<li><strong>Elige clase, raza y talentos</strong><span>Con las raciales nuevas del 26 y 27 de octubre ya puedes decidir. <a href="../clases/">Clases</a> · <a href="../raciales-forever/">Raciales nuevas</a> · <a href="../calculadora/">Calculadora</a>.</span></li>'
            '<li><strong>Quedad con los amigos</strong><span>Para jugar juntos, hermandad, mazmorras y bandas, tenéis que estar en las <strong>mismas reglas</strong> (Normal, JcJ, Rol o Rol-JcJ) y la <strong>misma facción</strong>.</span></li></ol>'
            '<div class="divider"><h2>Al entrar por primera vez: Clásico o Mejorado</h2></div>'
            '<p>La primera vez que entras, el juego te pide elegir un estilo. Blizzard aconseja <strong>Mejorado</strong> si dudas. Se cambia después en Opciones → Sistema → Preajuste.</p>'
            '<table class="keys"><tr><th>Ajuste</th><td><strong>Clásico</strong></td><td><strong>Mejorado</strong></td></tr>'
            '<tr><th>Modelos</th><td>Los de siempre (SD)</td><td>Alta definición (HD)</td></tr>'
            '<tr><th>Objetivos de misión en el mapa</th><td>No</td><td>Sí</td></tr>'
            '<tr><th>Una sola bolsa</th><td>No</td><td>Sí</td></tr>'
            '<tr><th>Transfiguración</th><td>No</td><td>Sí</td></tr>'
            '<tr><th>Teclas de movimiento</th><td>Girar la cámara</td><td>Desplazamiento lateral</td></tr>'
            '<tr><th>Interfaz</th><td>La clásica</td><td>Centrada</td></tr></table>'
            '<div class="divider"><h2>Las primeras horas</h2></div><div class="facts">'
            '<div class="fact ok"><h3>Hazlo desde el nivel 1</h3><ul>'
            '<li><strong>Recolecta</strong> (minería, herboristería o desuello): es lo que más dinero da al principio, y la equitación sale cara (100 de oro a nivel 40). <a href="../profesiones/">Profesiones</a>.</li>'
            '<li><strong>Cocina y Primeros auxilios</strong> en todos tus personajes: la cocina es la base de la hoguera (mejoras de una hora) y en Forever los Primeros auxilios hacen las pociones de sanación.</li>'
            '<li><strong>Vuelve al instructor</strong> de tu clase cada dos niveles y aprende las rutas de vuelo.</li>'
            '<li><strong>Fija tu piedra de hogar</strong> en la posada donde más vayas a estar.</li></ul></div>'
            '<div class="fact wait"><h3>Errores típicos</h3><ul>'
            '<li><strong>Revivir con el Ángel de la Resurrección</strong> del cementerio: estropea el equipo y te deja muy débil un rato. Mejor corre hasta tu cuerpo.</li>'
            '<li><strong>Vender los materiales</strong> que luego vas a necesitar: guárdalos en el banco.</li>'
            '<li><strong>Tirar de varios enemigos a la vez</strong> mientras aprendes la clase.</li>'
            '<li><strong>No leer las misiones:</strong> muchas pistas están en el texto.</li></ul></div></div>'
            '<h3>Teclas que vas a usar todo el rato</h3><table class="keys">'
            '<tr><th>L</th><td>Registro de misiones</td></tr><tr><th>M</th><td>Mapa del mundo</td></tr><tr><th>P</th><td>Libro de hechizos (arrástralos a tus barras)</td></tr>'
            '<tr><th>C</th><td>Personaje</td></tr><tr><th>K</th><td>Profesiones</td></tr><tr><th>Esc</th><td>Menú y opciones (teclas, barras, interfaz)</td></tr></table>'
            '<div class="divider"><h2>Lo nuevo que vas a encontrar</h2></div><ul>'
            '<li><strong>Combinaciones nuevas de raza y clase:</strong> humano cazador, enano chamán y gnomo sacerdote en la Alianza; orco mago, trol brujo y no-muerto paladín en la Horda.</li>'
            '<li><strong>Los célicos</strong> empiezan en la Isla de Zephras (niveles 1 a 12) y necesitan el pack Heroico o superior.</li>'
            '<li><strong>Zonas nuevas:</strong> el monte Hyjal, Shen\'dralas, Riverglades y la Isla de Zephras. <a href="../subir-nivel/">Cómo subir de nivel</a>.</li>'
            '<li><strong>El Legado:</strong> ventajas para toda tu cuenta. <a href="../legacy/">Cómo funciona</a>.</li>'
            '<li><strong>Nuevo campo de batalla, las Islas Lanza Negra:</strong> 15 contra 15, de nivel 30 a 60, frente al Marjal Revolcafango. Gana el primero que llega a 2.000 puntos.</li>'
            '<li><strong>Las 9 mazmorras nuevas</strong>, del nivel 13 al 60: <a href="../mazmorras-nuevas/">dónde está cada una</a>. Las bandas abren el 9 de diciembre: <a href="../bandas-forever/">cómo entrar en Onyxia</a>.</li></ul>'
            '<div class="prepare"><h3>Si no puedes entrar</h3><p>Si te pide recuperar la cuenta, usa «¿No puedes iniciar sesión?» en la web de Battle.net. Si te la han robado, cambia la contraseña de tu correo y de Battle.net y añade el autenticador de Battle.net. '
            'Las primeras horas de un lanzamiento suele haber colas: paciencia, y no reinstales nada.</p></div>'
            f'<p class="fine">Fuentes: <a href="{BLIZZ_NUEVOS}" target="_blank" rel="noopener noreferrer">Blizzard: guía para jugadores nuevos</a> (28 de octubre) · '
            f'<a href="{BLIZZ_VUELVEN}" target="_blank" rel="noopener noreferrer">Blizzard: guía para los que vuelven</a> (29 de octubre) y las páginas de esta web.</p>')
    page('dia-1', 'Día 1 en WoW Forever: qué hacer antes y en las primeras horas | Muchamiel',
         'Todo para el lanzamiento de WoW Forever (jueves 5 de noviembre a las 00:00): qué dejar listo antes, Clásico o Mejorado, qué hacer en las primeras horas y los errores típicos.', body)


# Van 29-10: lo que dijo Blizzard esta semana (entrevista a IGN y pódcast 6). Con nuestras palabras.


def novedades29_page():
    body = ('<p class="eyebrow">NOTICIAS · 29 DE OCTUBRE DE 2026</p><h1>Blizzard: un parche grande cada 4 meses, y lo que viene después</h1>'
            '<p class="lead">A una semana del lanzamiento, Blizzard ha contado en una entrevista y en el pódcast oficial cómo será el ritmo de Forever, a dónde puede ir y cómo funcionarán los servidores. Esto es lo importante.</p>'
            '<div class="tfo-stats"><div><b>4 meses</b><span>entre parches grandes</span></div><div><b>3</b><span>parches al año</span></div><div><b>4 meses</b><span>cada temporada JcJ</span></div><div><b>2</b><span>configuraciones de talentos</span></div></div>'
            '<div class="divider"><h2>El ritmo: un parche grande cada 4 meses</h2></div><ul>'
            '<li><strong>Unos 4 meses (17 semanas) entre parches grandes</strong>, unas tres veces al año. En Season of Discovery iban cada 8-10 semanas y les pareció demasiado rápido.</li>'
            '<li><strong>Dentro de cada parche se irán abriendo cosas</strong> al mes, a los dos o a los tres meses, para que no salga todo el primer día.</li>'
            '<li><strong>Las temporadas de JcJ también durarán 4 meses.</strong></li>'
            '<li>Encaja con el calendario que ya conocemos: bandas el 9 de diciembre y la primera gran actualización a principios de 2027. <a href="../calendario/">Calendario</a>.</li></ul>'
            '<div class="divider"><h2>A dónde puede ir Forever</h2></div><ul>'
            '<li><strong>El camino clásico:</strong> Núcleo de Magma, Guarida Alanegra y Ahn&#39;Qiraj llegarán, pero más espaciados que en Classic.</li>'
            '<li><strong>Sitios nuevos que «encajan»</strong>, como Riverglades: ahí irán también mazmorras y bandas futuras.</li>'
            '<li><strong>Cosas muy distintas</strong>, como los célicos y la Isla de Zephras.</li>'
            '<li><strong>El Portal Oscuro, Rasganorte y Pandaria existen</strong>, y podrían hacer visitas cortas (una mazmorra o una misión que te lleve y te traiga), <strong>pero no pronto</strong>. Siempre se volverá a los Reinos del Este y Kalimdor.</li>'
            '<li><strong>Sin casas</strong> (housing) en Forever.</li>'
            '<li><strong>Dos configuraciones de talentos</strong> les parecen suficientes de momento.</li></ul>'
            '<div class="divider"><h2>Los servidores, según el pódcast 6</h2></div><ul>'
            '<li><strong>Sin reinos:</strong> eliges reglas y juegas con gente de toda Europa.</li>'
            '<li><strong>Menos cambios de fase forzados:</strong> al unirte a un grupo ya no te mueven de golpe; te sale un aviso y tienes un rato para elegir cuándo.</li>'
            '<li><strong>Te juntan con tu comunidad:</strong> el juego intenta ponerte con tu hermandad, tus amigos y la gente con la que ya has jugado.</li>'
            '<li><strong>Al cruzar de zona aún puede desaparecer gente</strong>, aunque lo han mejorado. El primer día habrá mucha más gente en Durotar que en Orgrimmar y lo irán ajustando.</li>'
            '<li><strong>Batallas enormes de JcJ:</strong> estudian que el servidor las detecte y les dé más capacidad. Lo que viste al final de la beta es lo que habrá al lanzamiento.</li>'
            '<li>Más detalles y lo que aún es idea: <a href="../a-medias/">A medias</a>.</li></ul>'
            '<div class="tiles"><a class="tile" href="../dia-1/"><strong>Día 1 en Forever</strong><span>Qué hacer antes y en las primeras horas.</span></a>'
            '<a class="tile" href="../a-medias/"><strong>A medias</strong><span>Lo que aún no es seguro y los cambios sin anunciar.</span></a>'
            '<a class="tile" href="../calendario/"><strong>Calendario</strong><span>Todas las fechas oficiales.</span></a></div>'
            '<p class="fine">Fuentes: entrevista de IGN a Kris Zierhut y Tim Jones (Blizzard), 29 de octubre · '
            '<a href="https://www.youtube.com/watch?v=BVyhnixdPQg" target="_blank" rel="noopener noreferrer">pódcast oficial, episodio 6</a> · '
            '<a href="https://www.wowhead.com/news=383635" target="_blank" rel="noopener noreferrer">Wowhead</a>.</p>')
    page('novedades-29-octubre', 'Blizzard: un parche grande cada 4 meses en WoW Forever | Muchamiel',
         'Lo que contó Blizzard el 29 de octubre: parches cada 4 meses, temporadas JcJ de 4 meses, a dónde puede ir Forever y cómo funcionarán los servidores.', body)


# Van 30-10: página pública de la zona de subs. El botón no lleva a ningún sitio hasta que Muchamiel active las integraciones
# de Discord (los roles de sub) y lo confirme: entonces se pone SUBS_ABIERTA = True y se vuelve a generar. Abierta el 30-10-2026.
SUBS_ABIERTA = True
SUBS_URL = 'https://muchamiel-subs.pages.dev'


def zona_subs_page():
    boton = (f'<a class="btn gold" href="{SUBS_URL}" rel="noopener">Entrar con Discord</a>' if SUBS_ABIERTA else
             '<span class="btn ghost" aria-disabled="true" style="opacity:.6;cursor:not-allowed">Muy pronto</span>')
    body = ('<p class="eyebrow">COMUNIDAD · PARA QUIEN APOYA EL CANAL</p><h1>⭐ Zona de subs</h1>'
            '<p class="lead">Una parte de la web solo para subs de Twitch, miembros de YouTube y mecenas de Patreon. Las guías, macros y la calculadora siguen <strong>gratis para todos</strong>; aquí va lo de antes, lo extra y lo de la comunidad.</p>'
            f'<p>{boton}</p>'
            + ('' if SUBS_ABIERTA else '<p class="fine">La estamos terminando: se abre en cuanto el Discord tenga los roles de sub.</p>')
            + '<div class="tiles">'
            '<div class="tile"><strong>📘 Guías antes que nadie</strong><span>Lo nuevo sale ahí unos días antes que en la web.</span></div>'
            '<div class="tile"><strong>🪄 Creador de macros</strong><span>Elige clase y hechizo, marca opciones (ratón, foco, modificadores…) y copia, en el idioma de tu juego.</span></div>'
            '<div class="tile"><strong>📅 Eventos con Muchamiel</strong><span>Bandas, mazmorras y JcJ con la comunidad: apúntate con tu rol.</span></div>'
            '<div class="tile"><strong>🗳️ Votaciones y preguntas</strong><span>Decide la próxima guía y pregunta lo que quieras: lo más votado se contesta en directo.</span></div>'
            '<div class="tile"><strong>💛 Muro de agradecimiento</strong><span>Si quieres, tu nombre en la web.</span></div>'
            '<div class="tile"><strong>⭐ Canal #subs</strong><span>Charla privada en el Discord y avisos antes que nadie.</span></div></div>'
            '<div class="divider"><h2>Cómo se entra</h2></div><ol>'
            '<li>Sé sub en <a href="https://www.twitch.tv/muchamiel" target="_blank" rel="noopener noreferrer">Twitch</a> (con Prime Gaming es gratis cada mes), miembro en YouTube o mecenas en Patreon.</li>'
            '<li>Únete al <a href="https://discord.gg/U8VkN5yXJ8" target="_blank" rel="noopener noreferrer">Discord de Muchamiel</a> y conecta tu Twitch o tu YouTube en Discord (Ajustes de usuario → Conexiones): te da el rol solo.</li>'
            '<li>Pulsa «Entrar con Discord». Sin contraseñas: Discord solo nos dice tu nombre y si tienes el rol.</li></ol>')
    page('zona-subs', 'Zona de subs de Muchamiel: guías antes, creador de macros y eventos',
         'La zona de Muchamiel para subs de Twitch, miembros de YouTube y Patreon: guías antes que nadie, creador de macros, eventos con la comunidad y votaciones.', body)


# Calendario (Van, 16-10-2026): todas las fechas clave de WoW Forever en orden, solo con datos que ya están en la web.
# Origen de cada fecha: torneo (carrusel y página /torneo/), prueba de estrés (carrusel, /beta-gratis/ y research/prueba-estres-hora.md),
# fin de beta y reserva, lanzamiento y bandas (FECHAS de forever_portal y research/forever-lanzamiento.md).
# Las del lanzamiento no se copian: salen de forever_portal.FECHAS, así una fecha se cambia en un solo sitio.
CALENDARIO_BETA = [
    ('22 y 23 oct', 'Fiesta de despedida de la beta: 24 horas de evento en las zonas de inicio, hasta el viernes 23 a las 19:00. <a href="../fin-beta/">Qué hay</a>.'),
    ('21 oct, 19:00', 'Prueba de estrés gratis (Blizzard la pasó del 19 al 21): WoW Forever se abre a todo el mundo unas horas, sin suscripción, en los servidores del lanzamiento. <a href="../beta-gratis/">Cómo entrar</a>.'),
]


def calendario_filas():
    from forever_portal import FECHAS
    filas = list(CALENDARIO_BETA)
    for f, t in FECHAS:
        filas.append((f, t if '<a ' in t else t + ' <a href="../lanzamiento/">El lanzamiento</a>.'))
    return filas


def calendario_page():
    filas = ''.join(f'<tr><th>{E(f)}</th><td>{t}</td></tr>' for f, t in calendario_filas())
    body = ('<p class="eyebrow">WOW FOREVER · FECHAS CLAVE</p><h1>Calendario de WoW Forever</h1>'
            '<p class="lead">Todas las fechas de WoW Forever en orden, desde el torneo de la beta hasta el lanzamiento y lo que llega después. '
            'Cada una con su enlace, para que no se te escape ninguna.</p>'
            '<div class="divider"><h2>Fechas clave</h2></div><table class="keys">' + filas + '</table>'
            '<p class="fine">Hora peninsular. Prueba de estrés del 21: en México a las 15:00; en Chile y Argentina a las 18:00. Fin de la beta, el 23 a las 19:00: en México a las 11:00; en Chile y Argentina a las 14:00. ''Lanzamiento: en la península, las 00:00 del 5; en México, el 4 a las 17:00; en Chile y Argentina, el 4 a las 20:00. '
            'Blizzard puede cambiar las fechas.</p>')
    page('calendario', 'Calendario de WoW Forever: todas las fechas clave | Muchamiel',
         'Todas las fechas de WoW Forever en orden: la prueba de estrés gratis y el fin de la beta (21), '
         'la reserva de nombres (27 de octubre al 3 de noviembre) y el lanzamiento (4 de noviembre).', body)


def build_pages():
    base = '../'
    beta_page()
    reserva_page()
    mazmorras_nuevas_page()
    bandas_page()
    fin_beta_page()
    a_medias_page()
    raciales26_page()
    dia1_page()
    novedades29_page()
    zona_subs_page()
    calendario_page()
    import forever_portal
    import guias_portal  # Van 30-10: guías de 1 a 300 de cada profesión (/profesiones/<slug>/)
    guias_portal.build(page, dist)
    forever_portal.build(page)  # juego completo (4-11, nivel 60): desplegable «WoW Forever»
    import mazmorras_portal
    mazmorras_portal.build()  # Van 16-10: una página por mazmorra (/mazmorras/<slug>/)
    import retail_portal
    retail_portal.build()  # Van 17-10: apartado WoW Retail (/retail/)
    import auras_portal
    auras_portal.build()  # Van 17-10: auras de ForeverAuras por clase (/auras/)
    import macros_portal
    macros_portal.build()  # Van 15-10: portada de macros (elegir clase + comunes + raciales) y una página por clase
    # Noticias
    feat = VIDEOS['video'][-2]  # ¿Qué es WoW Forever?
    body = ('<p class="eyebrow">YOUTUBE · BETA DE WOW FOREVER</p><h1>Noticias de WoW Forever</h1>'
            '<p class="lead">Todo lo que Muchamiel ha contado de WoW Forever durante la beta y el camino al torneo de 100.000 $. Pulsa una miniatura para verlo en YouTube.</p>'
            '<div class="divider ultima"><h2>Última hora</h2></div>'  # Van 15-10: lo primero de Noticias (clase propia para que youtube_auto meta su bloque después)
            '<a class="news-card" href="../reserva-nombres/"><span class="badge-new">YA VA</span><span><p class="eyebrow">RESERVA DE NOMBRES · HASTA EL 3 DE NOVIEMBRE</p>'
            '<h3>La reserva de nombres ya funciona</h3><p>Abrió con retraso el martes por la noche. Qué hacer si la Horda te sale bloqueada en JcJ o te dice que el nombre está restringido.</p>'
            '</span></a>'
            '<a class="news-card" href="../novedades-29-octubre/"><span class="badge-new">NUEVO</span><span><p class="eyebrow">BLIZZARD · 29 DE OCTUBRE</p>'
            '<h3>Un parche grande cada 4 meses, y a dónde puede ir Forever</h3><p>Temporadas JcJ de 4 meses, visitas cortas a Rasganorte o Pandaria algún día (no pronto) y cómo funcionarán los servidores.</p>'
            '</span></a>'
            '<a class="news-card" href="../a-medias/"><span class="badge-new">NUEVO</span><span><p class="eyebrow">SIN NOTA OFICIAL · 28 DE OCTUBRE</p>'
            '<h3>Cambios sin anunciar: Lanza de Hielo con 8 s de reutilización y cazadores con menos poder de ataque</h3><p>Han aparecido en el juego sin notas de Blizzard: magos, cazadores y algunos objetos. Los tienes en «A medias» hasta que Blizzard los confirme.</p>'
            '</span></a>'
            '<a class="news-card" href="../dia-1/"><span class="badge-new">NUEVO</span><span><p class="eyebrow">GUÍA · JUEVES 5 DE NOVIEMBRE</p>'
            '<h3>Día 1 en WoW Forever: qué hacer antes y en las primeras horas</h3><p>Instalación, Clásico o Mejorado, qué hacer desde el nivel 1, los errores típicos y todo lo nuevo que te vas a encontrar.</p>'
            '</span></a>'
            '<a class="news-card" href="../raciales-forever/"><span class="badge-new">NUEVO</span><span><p class="eyebrow">BLIZZARD · 26 DE OCTUBRE</p>'
            '<h3>Cambian las raciales a una semana del lanzamiento</h3><p>Humano, enano, orco, tauren, trol, no-muerto y célicos: qué gana y qué pierde cada raza en el repaso final de Blizzard.</p>'
            '</span></a>'
            '<a class="news-card" href="../a-medias/"><span class="badge-new">NUEVO</span><span><p class="eyebrow">PISTAS Y RUMORES · SIN CONFIRMAR</p>'
            '<h3>A medias: lo que aún no es seguro</h3><p>Los jefes de las bandas nuevas, el Núcleo de Magma renovado, dónde están los portales escondidos y más, separado de lo confirmado y con su etiqueta. Con lo que contó el pódcast oficial.</p>'
            '</span></a>'
            '<a class="news-card" href="../fin-beta/"><span><p class="eyebrow">BETA · TERMINADA EL 23 DE OCTUBRE</p>'
            '<h3>Fiesta de despedida de la beta: ataques y épicos en las dos facciones</h3><p>24 horas de evento en las zonas de inicio de la Alianza y de la Horda, con elementales en Ventormenta y botín del Núcleo de Magma. Más: reinos de Rol-JcJ y el podcast de fin de beta.</p>'
            '</span></a>'
            '<a class="news-card" href="../bandas-forever/"><span class="badge-new">NUEVO</span><span><p class="eyebrow">BLIZZARD · BANDAS · 9 DE DICIEMBRE</p>'
            '<h3>Las bandas de Forever y cómo entrar en Onyxia</h3><p>Cavernas del Túmulo, Cima Hyjal y Onyxia: dónde están, para cuántos y la cadena del Drakefire Amulet de cada facción.</p>'
            '</span></a>'
            '<a class="news-card" href="../mazmorras-nuevas/"><span><p class="eyebrow">BLIZZARD · 20 DE OCTUBRE</p>'
            '<h3>Las 9 mazmorras nuevas de WoW Forever</h3><p>Del nivel 13 al 60: dónde está cada una y qué cuenta Blizzard. Más las novedades de la semana: mano dura con el oro comprado y el podcast de PvP.</p>'
            '</span></a>'
            '<a class="news-card" href="../reserva-nombres/"><span class="badge-new">NUEVO</span><span><p class="eyebrow">RESERVA DE NOMBRES · 27 OCT – 3 NOV</p>'
            '<h3>Reserva tu nombre en WoW Forever</h3><p>Nombre y apellido únicos en toda Europa, hasta tres personajes por cuenta, y ahora también en reinos de Rol-JcJ. Quién puede reservar y cómo hacerlo.</p>'
            '</span></a>'
            '<a class="news-card" href="../beta-gratis/"><span class="badge-new">NUEVO</span><span><p class="eyebrow">PRUEBA DE ESTRÉS · MIÉRCOLES 21 DE OCTUBRE · 19:00</p>'
            '<h3>Nueva fecha: juega gratis a WoW Forever el miércoles 21 a las 19:00</h3><p>Unas horas en los servidores del lanzamiento, sin suscripción; al acabar se borra todo. Te contamos cómo preinstalarla hoy mismo en Battle.net, paso a paso.</p>'
            '</span></a>'
            '<div class="divider" id="avisos"><h2>Avisos oficiales de Blizzard</h2></div>'
            '<p class="sub">Lo último que publica Blizzard en su foro sobre WoW Forever: mantenimientos, notas de parche y anuncios. Se actualiza solo; los mensajes van en inglés, tal cual los escribe Blizzard.</p>'
            '<div class="avisos" data-avisos data-n="6"><p class="fine">Cargando los avisos de Blizzard…</p></div>'
            '<div class="divider top-shorts"><h2>Últimos shorts</h2></div><div class="vgrid shorts">' + ''.join(vcard(v, 'short') for v in sorted(VIDEOS['short'], key=lambda v: v[1], reverse=True)[:3]) + '</div>'  # Van 15-10: 3 últimos shorts encima de los vídeos largos
            '<div class="divider"><h2>Empieza por aquí</h2></div>'
            f'<a class="featured" href="https://www.youtube.com/watch?v={feat[0]}" target="_blank" rel="noopener noreferrer"><span class="thumb"><img loading="lazy" src="https://i.ytimg.com/vi/{feat[0]}/hqdefault.jpg" alt=""><em>{feat[2]}</em></span>'
            f'<span><p class="eyebrow">PARA EMPEZAR</p><h3>{E(limpia(feat[3]))}</h3><p>Qué es WoW Forever y por qué está revolucionando el Classic. Si llegas nuevo, empieza por aquí.</p></span></a>'
            '<div class="divider"><h2>Noticias y guías</h2></div><div class="vgrid">' + ''.join(vcard(v, 'video') for v in VIDEOS['video']) + '</div>'
            '<div class="divider"><h2>Directos rumbo al torneo</h2></div><p class="sub">El Brujo «winner» preparando The Forever Open, sesión a sesión.</p><div class="vgrid">' + ''.join(vcard(v, 'live') for v in VIDEOS['live']) + '</div>'
            '<div class="divider"><h2>Shorts</h2></div><div class="vgrid shorts">' + ''.join(vcard(v, 'short') for v in VIDEOS['short']) + '</div>'
            f'<div class="actions" style="justify-content:center;margin:30px 0"><a class="btn yt" href="{YT_SUB}" target="_blank" rel="noopener noreferrer">Suscribirme al canal</a><a class="btn ghost" href="{YT}/videos" target="_blank" rel="noopener noreferrer">Todos sus vídeos</a></div>')
    page('noticias', 'Noticias de WoW Forever y torneo The Forever Open | Muchamiel',
         'Vídeos y noticias de WoW Forever de Muchamiel: beta, clases, razas, profesiones y la preparación del torneo The Forever Open de 100.000 $ (17 y 18 de octubre).', body)
    # Sorteos
    body = ('<p class="eyebrow">SORTEOS EN MARCHA</p><h1>Sorteos de Muchamiel</h1>'
            '<p class="lead">WoW gratis por apoyar al canal. Cada meta que se alcanza, se sortea. Así de sencillo.</p>' + roads() +
            '<div class="divider"><h2>Qué se sortea</h2></div><div class="cards3">'
            + ('<div class="prize"><span class="tag">META CONSEGUIDA</span><h3>1 año de WoW</h3><p>Su YouTube ya ha pasado de los <strong>90.000 suscriptores</strong>. Muchamiel anunciará en directo cuándo lo sortea.</p>' if STATS['yt_subs'] >= 90000 else '<div class="prize"><span class="tag">EN MARCHA</span><h3>1 año de WoW</h3><p>Al llegar a <strong>90.000 suscriptores en YouTube</strong>. Solo tienes que suscribirte.</p>')
            + f'<a class="btn yt" href="{YT_SUB}" target="_blank" rel="noopener noreferrer">Suscribirme</a></div>'
            '<div class="prize"><span class="tag">EN MARCHA</span><h3>Otro año de WoW</h3><p>Al llegar a <strong>100.000 suscriptores en YouTube</strong>. El gran objetivo del canal: Road to 100K.</p>'
            f'<a class="btn yt" href="{YT_SUB}" target="_blank" rel="noopener noreferrer">Suscribirme</a></div>'
            '<div class="prize"><span class="tag">EN MARCHA</span><h3>1 año de WoW</h3><p>Al llegar a <strong>2.000 subs en Twitch</strong>. Si tienes Amazon Prime, tu sub de Prime Gaming es gratis cada mes: úsala aquí.</p>'
            '<a class="btn tw" href="https://www.twitch.tv/subs/muchamiel" target="_blank" rel="noopener noreferrer">Suscribirme</a></div></div>'
            '<div class="divider"><h2>Sorteos en directo</h2></div>'
            '<p class="sub">Durante la beta ha regalado ediciones Epic de WoW Forever en directo. Los próximos se anuncian en el stream: activa las notificaciones para no perderte ninguno.</p>'
            '<div class="vgrid">' + vcard(VIDEOS['live'][5], 'live') + vcard(VIDEOS['live'][7], 'live') + '</div>'
            f'<div class="actions" style="margin:22px 0"><a class="btn tw" href="{TWITCH}" target="_blank" rel="noopener noreferrer">Seguir en Twitch</a><a class="btn kick" href="{KICK}" target="_blank" rel="noopener noreferrer">Seguir en Kick</a></div>'
            '<div class="divider"><h2>Apoyo directo</h2></div><div class="donate-box"><div><h3>Donar a Muchamiel</h3>'
            '<p>El mismo enlace de donaciones que tiene en su Twitch. Si no puedes suscribirte con tarjeta, dona 5 € y te regala la sub (palabra suya).</p></div>'
            f'<a class="btn donar" href="{DONAR}" target="_blank" rel="noopener noreferrer">Donar</a></div>'
            '<p class="fine">Las condiciones, fechas y ganadores de cada sorteo los anuncia Muchamiel en sus canales; esta página solo los recopila.</p>')
    page('sorteos', 'Sorteos de Muchamiel: WoW gratis, Road to 100K y Road to 2K subs',
         'Sorteos activos de Muchamiel: 1 año de WoW a los 90K y otro año a los 100K suscriptores en YouTube, y 1 año de WoW a los 2.000 subs de Twitch.', body)
    # Muchamiel
    bios = ''.join(f'<a class="bio" href="{u}" target="_blank" rel="noopener noreferrer"><strong>{E(n)}</strong><small>{E(c)}</small><q>{E(b)}</q></a>' for n, u, c, b in BIOS)
    bios += f'<a class="bio" href="{DISCORD}" target="_blank" rel="noopener noreferrer"><strong>Discord</strong><small>La comunidad</small><q>Únete al servidor para hablar de WoW, torneos y directos.</q></a>'
    bios += f'<a class="bio" href="{PATREON}" target="_blank" rel="noopener noreferrer"><strong>Patreon</strong><small>Apoyo mensual</small><q>Para quien quiera apoyar su contenido cada mes.</q></a>'
    bios += f'<a class="bio" href="{DONAR}" target="_blank" rel="noopener noreferrer"><strong>Donaciones</strong><small>StreamElements, como en su Twitch</small><q>Si no puedes suscribirte con tarjeta, dona 5 € y te regala la sub.</q></a>'
    bios += '<a class="bio" href="../colaboraciones/"><strong>Para marcas</strong><small>Colaboraciones y contacto</small><q>Con quién ha trabajado, sus números y cómo contactarle.</q></a>'
    body = ('<p class="eyebrow">EL STREAMER DETRÁS DE LA GUÍA</p>'
            f'<div class="about"><img class="avatar" src="{AVATAR}" alt="Muchamiel"><div><h1>Muchamiel</h1>'
            '<p class="lead">Streamer y creador de contenido de World of Warcraft: Hardcore, Classic, algo de Retail y, ahora, WoW Forever. En directo todos los días en Twitch y Kick.</p>'
            f'<div class="actions"><a class="btn tw" href="{TWITCH}" target="_blank" rel="noopener noreferrer">Twitch · <span data-twitch-followers>{miles(STATS["tw_followers"])}</span> seguidores</a>'
            f'<a class="btn yt" href="{YT_SUB}" target="_blank" rel="noopener noreferrer">YouTube · 79,1 K suscriptores</a>'
            f'<a class="btn kick" href="{KICK}" target="_blank" rel="noopener noreferrer">Kick · <span data-kick-followers>{miles(STATS["kick_followers"])}</span> seguidores</a></div></div></div>'  # Van 16-10: seguidores de Kick y sin «Donar» aquí
            '<div class="divider"><h2>La versión oficial (más o menos)</h2></div>'
            '<p>Muchamiel lleva subiendo vídeos de WoW desde 2016 y ya suma más de <strong>73 millones de visualizaciones</strong>, que se dice pronto y se farmea despacio.</p>'  # Van 16-10: fuera lo del «brujo más malo de España» (no es verdad)
            '<p>Si no está jugando un torneo, está retransmitiendo uno: Go Again, la TBC League, Bronzebeard… y ahora <strong>The Forever Open</strong>, con 100.000 $ en juego. '
            'Su método de entrenamiento es científico: duelos a CD, BiS completo y horas de directo hasta que la rotación sale sola.</p>'
            '<p>Su filosofía cabe en un tuit (literalmente, es su bio de X): <em>«Que la suerte me pille trabajando. El clavo no va a entrar dándole flojo. OSS»</em>.</p>'
            '<div class="divider"><h2>Con sus propias palabras</h2></div><p class="sub">Lo que pone Muchamiel en cada una de sus redes.</p><div class="bios">' + bios + '</div>'
            '<div class="divider"><h2>Échale una mano</h2></div>' + roads())
    page('muchamiel', 'Quién es Muchamiel: streamer de WoW Classic y WoW Forever',
         'Muchamiel, streamer de World of Warcraft en Twitch, Kick y YouTube: de The Forever Open a WoW Forever. Sus redes, sus descripciones y cómo apoyarle.', body)
    # Clases
    body = ('<p class="eyebrow">LAS NUEVE CLASES</p><h1>Clases</h1>'
            '<p class="lead">Elige tu clase: guía completa para subir del 1 al 60 con los talentos punto a punto, cómo se juega, nivel 60, JcJ y macros listas para copiar. '
            '¿No sabes cuál? Mira <a href="../elegir-clase/">qué clase elegir</a>.</p>' + clases_grid(base) +
            '<div class="tiles" style="margin-top:24px"><a class="tile" href="../razas/"><strong>Razas</strong><span>Raciales de cada raza con su macro.</span></a>'
            '<a class="tile" href="../calculadora/"><strong>Calculadora</strong><span>Prueba tu reparto de talentos.</span></a>'
            '<a class="tile" href="../comunes/"><strong>Guía de macros</strong><span>Cómo funcionan y cuáles valen para todas.</span></a></div>')  # Van 16-10: fuera «El brujo de Muchamiel"
    page('clases', 'Clases de WoW Forever: guías completas de las nueve clases | Muchamiel',
         'Guías completas de las nueve clases de WoW Forever: Guerrero, Paladín, Cazador, Pícaro, Sacerdote, Chamán, Mago, Brujo y Druida, del 1 al 60.', body)
    # Torneo
    chips =''.join(f'<a class="class-chip" href="../{slug}/"><img src="../assets/{slug}.jpg" alt="">{E(name)}</a>' for slug, name, *_ in classes)
    body = ('<p class="eyebrow">THE FOREVER OPEN</p><h1>The Forever Open</h1>'
            '<p class="lead">El torneo 1v1 de duelos a nivel 30 de la beta de WoW Forever. Aquí tienes premios, fechas y cómo seguir a Muchamiel; las reglas, siempre en la web oficial.</p>'
            + tfo(base, page=True) +
            '<div class="divider"><h2>Prepárate</h2></div><div class="prepare"><ol>'
            '<li>Carga tus 26 puntos exactos en el árbol del cliente y comprueba que tienes las habilidades aprendidas.</li>'
            '<li>Prueba cada macro en el juego: foco, ratón, modificadores y enfriamientos.</li>'
            '<li>Juega varias rondas contra cada clase con equipo y consumibles parecidos a los del torneo.</li>'
            '<li>Apunta por qué pierdes (burst, control, maná, interrupciones o falta de daño) y ajusta la build.</li>'
            f'<li>Antes de competir, vuelve a leer el <a href="{TFO_RULES}" target="_blank" rel="noopener noreferrer">reglamento oficial</a>: cambia a menudo.</li></ol></div>'
            '<div class="divider"><h2>La guía de tu clase</h2></div><p class="sub">Builds de 26 puntos, macros y duelos contra las nueve clases.</p>'
            f'<div class="quick class-chips">{chips}</div>'
            '<div class="divider"><h2>Muchamiel preparando el torneo</h2></div><div class="vgrid">' + ''.join(vcard(v, 'live') for v in VIDEOS['live'][:3]) + '</div>'
            '<div class="actions" style="justify-content:center;margin:22px 0"><a class="btn ghost" href="../noticias/">Más vídeos y noticias</a></div>')
    page('torneo', 'The Forever Open 1v1 Tournament: premios, fechas y directo | Muchamiel',
         'The Forever Open, el torneo 1v1 de WoW Forever con 100.000 $ en premios, 17 y 18 de octubre. Sigue a Muchamiel en directo y consulta el reglamento oficial.', body)
    # Addons (su vídeo del top 10, patrocinado por Overgear)
    vid = VIDEOS['video'][0]
    cards = ''.join(
        f'<article class="addon"><span class="rank">{n}</span><img src="{ZAML}{icon}.jpg" alt=""><div><p class="eyebrow">{E(cat)}</p><h3>{E(name)}</h3>'
        f'<p>{E(what)}</p><q>{E(says)}</q><a class="btn ghost" href="https://www.curseforge.com/wow/addons/{slug}" target="_blank" rel="noopener noreferrer">Descargar en CurseForge</a></div></article>'
        for n, (name, slug, icon, cat, what, says) in enumerate(ADDONS, 1))
    body = ('<p class="eyebrow">WOW FOREVER · INTERFAZ</p><h1>Addons</h1>'
            '<p class="lead">Los 10 addons que Muchamiel recomienda para WoW Forever: nada de los tres típicos de siempre, sino addons nuevos, muchos hechos para Forever. '
            'Todos están en CurseForge con versión para WoW Forever.</p>'
            f'<a class="featured" href="https://www.youtube.com/watch?v={vid[0]}" target="_blank" rel="noopener noreferrer"><span class="thumb"><img loading="lazy" src="https://i.ytimg.com/vi/{vid[0]}/hqdefault.jpg" alt=""><em>{vid[2]}</em></span>'
            f'<span><p class="eyebrow">EL VÍDEO</p><h3>{E(limpia(vid[3]))}</h3><p>Muchamiel los enseña uno a uno dentro del juego. Aquí tienes la lista con los enlaces.</p></span></a>'
            '<div class="sponsor-box"><div><p class="eyebrow">PATROCINA EL VÍDEO</p><h3>Overgear</h3>'
            '<p>Coaching de WoW (Classic, Forever y Retail), PvE y PvP: aprendes builds, talentos y a jugar mejor sin dar tu cuenta a nadie. '
            'Con el código <b>MUCHAMIEL10</b> tienes un 10 % de descuento.</p></div>'
            f'<a class="btn gold" href="{OVERGEAR}" target="_blank" rel="sponsored noopener noreferrer">Ir a Overgear</a></div>'
            '<div class="divider"><h2>Ya vienen de serie</h2></div><div class="tiles">'
            '<div class="tile"><strong>Barras de acción</strong><span>Escape → Modo edición: mueves y ajustas las barras como con Bartender.</span></div>'
            '<div class="tile"><strong>Medidor de daño</strong><span>El cliente ya trae su medidor, como un Details básico.</span></div>'
            '<div class="tile"><strong>Misiones en el mapa</strong><span>Activa los objetivos de misión en el mapa y tienes lo esencial de Questie.</span></div></div>'
            '<p class="fine">Si prefieres los de toda la vida (Bartender, Details, Questie), puedes seguir instalándolos.</p>'
            f'<div class="divider"><h2>El top 10 de Muchamiel</h2></div><div class="addons">{cards}</div>'
            '<div class="divider"><h2>Cómo instalarlos</h2></div><div class="prepare"><ol>'
            '<li>Con la app de CurseForge: elige WoW Forever, busca el addon e instálalo. Se actualizan solos.</li>'
            '<li>A mano: descarga el .zip de la versión <strong>Forever</strong> y descomprímelo en la carpeta <code>Interface\\AddOns</code> de tu WoW Forever.</li>'
            '<li>En el juego, abre la lista de addons en la pantalla de personajes. Si alguno sale como desactualizado, marca «Cargar addons desactualizados».</li>'
            '<li>¿Te falta alguno? Muchamiel pide que dejéis vuestros favoritos en los comentarios del vídeo.</li></ol></div>')
    page('addons', 'Los 10 mejores addons para WoW Forever | Muchamiel',
         'Los 10 addons que recomienda Muchamiel para WoW Forever: Talents Forever, GearQuest, Attune, DungeonJournal, EllesmereUI, SkillUp y más, con enlace a CurseForge.', body)
    # Colaboraciones (para marcas)
    activos = ''.join(f'<a class="code" href="{u}" target="_blank" rel="sponsored noopener noreferrer"><strong>{E(n)}</strong><small>{E(cat)}</small>'
                      + (f'<span>Código <b>{E(c)}</b>' + (f' · {E(d)}' if d else '') + '</span>' if c else '<span>Enlace de afiliado</span>') + '</a>'
                      for n, cat, _, _, u, c, d, act in BRANDS if act)
    marcas = ''.join(f'<div class="brand"><strong>{E(n)}</strong><small>{E(cat)}</small><span>{E(tipo)} · {E(y)}</span></div>' for n, cat, y, tipo, *_ in BRANDS)
    stats = ''.join(f'<div><b>{v}</b><span>{E(k)}</span></div>' for v, k in MEDIA)
    body = ('<p class="eyebrow">PARA MARCAS</p><h1>Colaboraciones</h1>'
            '<p class="lead">Muchamiel crea contenido de World of Warcraft para una comunidad hispanohablante que le ve a diario en directo y en YouTube. '
            'Si tu marca quiere llegar a ellos, aquí tienes sus números, con quién ha trabajado ya y cómo contactar.</p>'
            '<div class="actions" style="justify-content:center"><a class="btn gold" href="#contacto">Cómo contactar</a></div>'
            f'<div class="divider"><h2>Sus números</h2></div><div class="media-stats">{stats}</div><p class="fine">Cifras públicas del {FECHA_DATOS}.</p>'
            '<div class="divider"><h2>Marcas con las que ha trabajado</h2></div><p class="sub">Han aparecido en su canal con código, enlace o vídeo patrocinado.</p>'
            f'<div class="brands">{marcas}</div>'
            '<div class="divider"><h2>Formatos</h2></div><div class="tiles">'
            '<div class="tile"><strong>Mención en directo</strong><span>Twitch y Kick, todos los días, con enlace en el chat.</span></div>'
            '<div class="tile"><strong>Código y enlace</strong><span>En la descripción de sus vídeos y en los paneles de sus canales.</span></div>'
            '<div class="tile"><strong>Vídeo patrocinado</strong><span>Integración en vídeos de YouTube, como su colaboración con Planeta DeAgostini.</span></div>'
            '<div class="tile"><strong>Sorteos y eventos</strong><span>Sorteos con la comunidad y torneos como la TBC League.</span></div></div>'
            '<div class="divider"><h2>Códigos para la comunidad</h2></div><p class="sub">Los que usa en sus últimos vídeos. Comprueba en la web de cada marca que sigan vigentes.</p>'
            f'<div class="codes">{activos}</div>'
            '<div class="divider" id="contacto"><h2>Cómo contactar</h2></div>'
            '<p class="sub">Lo más rápido es un mensaje privado en cualquiera de sus redes. Si prefieres el correo, pulsa «Correo» y te lo enseñamos.</p>'
            + socials_row(correo=True) +
            '<div class="divider"><h2>Apoyo directo</h2></div><div class="tiles">'
            f'<a class="tile" href="{PATREON}" target="_blank" rel="noopener noreferrer"><strong>Patreon</strong><span>Apoya su contenido cada mes.</span></a>'
            f'<a class="tile" href="{DONAR}" target="_blank" rel="noopener noreferrer"><strong>Donar</strong><span>El enlace de donaciones de su Twitch (StreamElements).</span></a>'
            '<a class="tile" href="https://www.twitch.tv/subs/muchamiel" target="_blank" rel="noopener noreferrer"><strong>Sub en Twitch</strong><span>Con Prime Gaming es gratis cada mes.</span></a>'
            f'<a class="tile" href="{DISCORD_CREADORES}" target="_blank" rel="noopener noreferrer"><strong>¿Quieres crear contenido?</strong><span>«¿Quieres vivir de crear contenido de videojuegos? Háblame por Discord.»</span></a></div>')
    page('colaboraciones', 'Colaboraciones y patrocinios de Muchamiel: marcas y contacto',
         'Marcas que han trabajado con Muchamiel (LagZapper, Instant Gaming, Knoweats, Planeta DeAgostini…), sus números en Twitch, YouTube y Kick y su contacto para marcas.', body)
    # 404
    tpl = (dist / 'comunes' / 'index.html').read_text(encoding='utf-8')
    head = re.sub(r'<title>.*?</title>', '<title>Página no encontrada · WoW Forever</title>', tpl[:tpl.index('<body')], count=1, flags=re.S)
    head = head.replace('<meta name="description"', '<meta name="robots" content="noindex"><meta name="description"', 1)
    head = re.sub(r'(<meta name="description" content=")[^"]*', r'\1La página que buscas no existe. Vuelve a la guía de WoW Forever de la comunidad de Muchamiel.', head, count=1)  # Van 30-10: sin nivel 30
    (dist / '404.html').write_text(head.replace('href="../', 'href="/').replace('src="../', 'src="/') +
                                   '<body><header></header><main><section class="hero"><p class="eyebrow">ERROR 404</p><h1>Te has perdido en Azeroth</h1>'
                                   '<p class="lead">Esta página no existe (o se la ha llevado un pícaro en sigilo).</p><div class="actions"><a class="btn gold" href="/">Volver al inicio</a></div></section></main></body></html>',
                                   encoding='utf-8')


ZAML = 'https://wow.zamimg.com/images/wow/icons/large/'
APARTADOS = [
    ('lanzamiento/', ZAML + 'inv_misc_tournaments_banner_human.jpg', 'WoW Forever: el lanzamiento', 'Sale el 4 de noviembre con nivel 60: fechas, builds, mazmorras y Legacy.'),
    ('clases/', 'assets/warlock.jpg', 'Clases', 'Las nueve clases: del 1 al 60, cómo se juega, nivel 60 y macros.'),
    ('razas/', 'assets/race_orc_male.jpg', 'Razas', 'Alianza y Horda: raciales de cada raza con su macro.'),
    ('calculadora/', ZAML + 'inv_misc_book_11.jpg', 'Calculadora', 'Talentos del nivel 10 al 60 con Legacy. Comparte tu build.'),
    ('comunes/', ZAML + 'inv_inscription_scroll.jpg', 'Guía de macros', 'Por qué usarlas, cómo crearlas y las comunes a todas las clases.'),
    ('addons/', ZAML + 'trade_engineering.jpg', 'Addons', 'El top 10 de Muchamiel para WoW Forever, con enlace de descarga.'),
    ('noticias/', ZAML + 'inv_scroll_03.jpg', 'Noticias', 'Los vídeos de Muchamiel sobre WoW Forever, con miniaturas.'),
    ('sorteos/', ZAML + 'inv_misc_gift_05.jpg', 'Sorteos', 'WoW gratis: Road to 100K en YouTube y Road to 2K subs en Twitch.'),
    ('muchamiel/', AVATAR, 'Muchamiel', 'El streamer detrás de la guía: sus redes, su lema y cómo apoyarle.'),
    ('cambios/', ZAML + 'inv_misc_note_06.jpg', 'Cambios de la beta', 'Nerfs y mejoras de cada parche, por clase y en castellano.'),
    ('colaboraciones/', ZAML + 'inv_misc_coin_01.jpg', 'Patrocinadores', 'Las marcas que colaboran con Muchamiel, sus números y contacto.'),
]


def clases_grid(base):
    return '<div class="classes">' + ''.join(
        f'<a class="class-card" style="--class-color:{color}" href="{base}{slug}/"><img class="class-icon" src="{base}assets/{slug}.jpg" alt="">'
        f'<span class="number">{cls}</span><h3>{E(name)}</h3><p>{E(tag)}</p><span class="enter">Builds · Macros · Estrategias</span></a>'
        for slug, name, cls, color, tag in classes) + '</div>'



# Carrusel de la portada (Van, 16-10): lo más importante sin bajar. carrusel.js lo mueve y quita lo caducado (data-hasta).
def carrusel(latest):
    v = latest[0]
    slide = lambda href, fondo, hasta, ojo, titulo, txt, boton, extra='', ext=False: (
        f'<a class="car-slide {fondo}" href="{href}"' + (f' data-hasta="{hasta}"' if hasta else '') + extra
        + (' target="_blank" rel="noopener noreferrer"' if ext else '') + f'><div class="car-txt"><p class="eyebrow">{ojo}</p><h2 data-car-titulo>{titulo}</h2>'
        f'<p data-car-txt>{txt}</p></div></a>')  # Van 16-10: sin botón, se pulsa la diapositiva entera
    slides = [
        slide('mazmorras/', 'cs-halloween', '2026-11-01', 'HALLOWEEN · 31 DE OCTUBRE', 'Las mazmorras más siniestras de Forever',
              'Scholomance, Stratholme, el Castillo de Colmillo Oscuro y el Monasterio Escarlata: dónde están, a qué nivel y qué te espera dentro. Feliz Halloween.', 'Ver las mazmorras'),
        slide('novedades-29-octubre/', 'cs-alianza', '2026-11-12', 'BLIZZARD · 29 DE OCTUBRE', 'Un parche grande cada 4 meses',
              'Lo que ha contado Blizzard del futuro de Forever y de sus servidores.', 'Leer'),
        slide('a-medias/', 'cs-alianza', '2026-11-05', 'SIN NOTA OFICIAL · 28 DE OCTUBRE', 'Lanza de Hielo con 8 s de reutilización',
              'Cambios a magos, cazadores y objetos que han salido en el juego sin anunciar.', 'Ver los cambios'),
        slide('dia-1/', 'cs-alianza', '2026-11-12', 'GUÍA · JUEVES 5 DE NOVIEMBRE', 'Día 1 en WoW Forever',
              'Qué dejar listo antes, Clásico o Mejorado y qué hacer en las primeras horas.', 'Ver la guía'),
        slide('reserva-nombres/', 'cs-alianza', '2026-11-04', 'RESERVA DE NOMBRES · HASTA EL 3 DE NOVIEMBRE', 'La reserva de nombres ya funciona',
              'Abrió con retraso el martes. Si la Horda te sale bloqueada o el nombre restringido, aquí te explicamos por qué.', 'Ver la reserva'),
        slide('raciales-forever/', 'cs-blizz', '2026-11-05', 'BLIZZARD · 26 DE OCTUBRE', 'Cambian las raciales',
              'Repaso final antes del lanzamiento: siete razas cambian, raza a raza.', 'Ver los cambios'),
        slide('fin-beta/', 'cs-alianza', '2026-10-24', 'FIN DE LA BETA · HASTA EL VIERNES 23 · 19:00', 'Ataques y épicos en las dos facciones',
              'Blizzard despide la beta con 24 horas de evento en las zonas de inicio de la Alianza y de la Horda, con botín del Núcleo de Magma. Última ocasión de entrar.', 'Qué hay'),
        slide('bandas-forever/', 'cs-blizz', '2026-12-10', 'BANDAS · 9 DE DICIEMBRE', 'Cómo entrar en Onyxia',
              'Las tres primeras bandas de Forever y la cadena del Drakefire Amulet, paso a paso para cada facción.', 'Ver las bandas'),
        slide('beta-gratis/', 'cs-horda', '2026-10-22', 'MIÉRCOLES 21 DE OCTUBRE · 19:00 · GRATIS', '¿Quieres jugar conmigo en la beta?',
              'WoW Forever se abre gratis unas horas para todo el mundo, sin suscripción. Déjala preinstalada y nos vemos dentro.', 'Cómo descargarla'),
        # Van 16-10: el último parche de la beta, a Cambios (hasta que acabe la beta).
        slide('cambios/', 'cs-blizz', '2026-10-22', 'NUEVO PARCHE DE LA BETA · 15 DE OCTUBRE', 'Raciales rehechas, varitas quietas y talentos nuevos',
              'Cambian las raciales de casi todas las razas, las varitas piden estar quieto y llegan Frost Blast, Arcane Wrath y Elemental Mastery. Todo por clase y en castellano.', 'Ver los cambios'),
        slide('reserva-nombres/', 'cs-alianza', '2026-11-04', 'RESERVA DE NOMBRES · 27 OCT – 3 NOV', 'Reserva el nombre de tu personaje',
              'Nombre y apellido únicos en toda Europa, hasta tres personajes por cuenta, una semana antes del lanzamiento.', 'Cómo reservar mi nombre'),
        slide('noticias/#avisos', 'cs-blizz', None, 'ÚLTIMO AVISO DE BLIZZARD', 'Avisos oficiales de Blizzard',
              'Mantenimientos, notas de parche y anuncios de WoW Forever, al momento.', 'Ver los avisos', ' data-aviso-car'),
        slide(f'https://www.youtube.com/watch?v={v[0]}', 'cs-video', None, 'ÚLTIMO VÍDEO DEL CANAL', E(limpia(v[3])),
              'Míralo en YouTube y suscríbete para no perderte ninguno.', 'Ver el vídeo',
              f' style="background-image:linear-gradient(rgba(6,8,14,.84),rgba(6,8,14,.9)),url(https://i.ytimg.com/vi/{v[0]}/maxresdefault.jpg)"', True),
        slide('comunes/', 'cs-web', None, 'NOVEDADES DE LA WEB', 'Macros por clase y calculadora de talentos',
              'Copia las macros de tu clase con un clic y planifica tu build del 10 al 60 con el Legado.', 'Ver las macros'),
    ]
    return ('<section class="car" data-car aria-roledescription="carrusel" aria-label="Lo más nuevo">'
            '<div class="car-vista"><div class="car-pista">' + ''.join(slides) + '</div></div>'
            '<button type="button" class="car-flecha prev" aria-label="Anterior">‹</button><button type="button" class="car-flecha next" aria-label="Siguiente">›</button>'
            '<div class="car-puntos"></div></section>')

def home(s):
    """Inicio: saludo, todos los apartados arriba, el torneo y lo último. El contenido vive en su página."""
    a, b = s.index('<main>') + len('<main>'), s.index('<footer')
    banner = f'<a class="live-banner" href="{TWITCH}" target="_blank" rel="noopener noreferrer"><b>MUCHAMIEL EN DIRECTO</b><span class="t">Entra a verlo en Twitch</span><span class="go"></span></a>'
    # Saludo en boca de Muchamiel: «¡Qué pasa, pililas!» lo propuso Van; «mil gracias por…» es la frase de sus bios.
    hero = ('<section class="hero"><p class="eyebrow">GUÍAS · NOTICIAS · DIRECTOS</p><h1>WoW Forever</h1><p class="greet">¡Qué pasa, pililas!</p>'
            '<p class="lead">Vengáis de Twitch, de YouTube o de Kick, bienvenidos a mi web de WoW Forever: todo para el lanzamiento del 4 de noviembre, '
            'builds, macros y duelos para las nueve clases, y las noticias del juego para que lleguéis con todo preparado. Mil gracias por estar aquí. ¿Por dónde empezamos?</p>'
            f'<p class="firma"><img src="{AVATAR}" alt="">Muchamiel</p></section>')
    cards = '<nav class="apartados" id="apartados" aria-label="Apartados de la web">' + ''.join(
        f'<a class="apartado" href="{href}"><img src="{img}" alt=""><span><strong>{E(t)}</strong><small>{E(d)}</small></span></a>' for href, img, t, d in APARTADOS) + '</nav>'
    latest = sorted(VIDEOS['video'] + VIDEOS['live'], key=lambda v: v[1], reverse=True)[:4]
    kinds = {v[0]: k for k, vs in VIDEOS.items() for v in vs}
    news = ('<div class="divider"><h2>Lo último</h2></div><div class="vgrid">' + ''.join(vcard(v, kinds[v[0]]) for v in latest) +
            '</div><div class="actions" style="justify-content:center;margin-top:18px"><a class="btn ghost" href="noticias/">Ver todas las noticias</a></div>')
    beta = ('<section class="beta-cta home" id="beta-gratis"><div>'
            '<p class="eyebrow">MIÉRCOLES 21 DE OCTUBRE · 19:00 · GRATIS PARA TODO EL MUNDO</p><h2>¿Quieres jugar conmigo en la beta?</h2>'
            '<p>El miércoles 21 a las 19:00* WoW Forever se abre gratis unas horas para todos, aunque no tengáis suscripción. Dejadla preinstalada ya y nos vemos dentro. <span class="latam">* México: 15:00 · Chile y Argentina: 18:00.</span></p>'
            '<ol class="mini-pasos"><li>Cuenta de Battle.net gratis</li><li>App de Battle.net → World of Warcraft</li>'
            '<li>Versión «WoW: Forever – Prueba de estrés» → Preinstalar</li></ol>'
            f'<div class="actions"><a class="btn gold" href="beta-gratis/">Cómo descargarla paso a paso</a>'
            f'<a class="btn ghost" href="{BNET_APP}" target="_blank" rel="noopener noreferrer">Descargar Battle.net</a></div></div></section>')
    # Van 15-10: aviso de la reserva de nombres también en la portada, bajo el de la beta gratis.
    reserva = ('<a class="news-card home-reserva" href="reserva-nombres/"><span class="badge-new">27 OCT – 3 NOV</span><span><p class="eyebrow">RESERVA DE NOMBRES</p>'
               '<h3>Reserva el nombre de tu personaje</h3><p>Nombre y apellido únicos en toda Europa y hasta tres personajes por cuenta, una semana antes del lanzamiento. Te contamos quién puede y cómo hacerlo.</p>'
               '</span></a>')
    # Van 16-10: los últimos avisos de Blizzard sobre Forever, también en la portada (avisos.js + datos/avisos-blizzard.json).
    avisos = ('<div class="divider"><h2>Últimos avisos de Blizzard</h2></div><div class="avisos" data-avisos data-n="3"><p class="fine">Cargando los avisos de Blizzard…</p></div>'
              '<div class="actions" style="justify-content:center;margin-bottom:10px"><a class="btn ghost" href="noticias/#avisos">Ver todos los avisos</a></div>')
    # Van 16-10: la beta y la reserva pasan al carrusel, lo primero de la portada.
    import forever_portal  # Van 16-10: el lanzamiento, tras el saludo (a prueba: «a ver si me gusta»)
    # Van 16-10: «Empieza aquí» (plan de crecimiento): el camino del que llega nuevo, en 6 pasos.
    pasos = [('clases/', '1 · Elige tu clase', 'Las 9 clases, qué hace cada una y su guía.'),
             ('razas/', '2 · Elige tu raza', 'Alianza u Horda, y las raciales de cada una.'),
             ('calculadora/', '3 · Planifica tus talentos', 'La calculadora del 10 al 60 con Legado.'),
             ('comunes/', '4 · Copia tus macros', 'Todas, por clase, con botón de copiar.'),
             ('addons/', '5 · Instala los addons', 'Los imprescindibles y los de PvP.'),
             ('subir-nivel/', '6 · Sube del 1 al 60', 'Zonas, consejos y mazmorras por nivel.')]
    empieza = ('<section class="empieza" id="empieza"><div class="divider"><h2>¿Nuevo en WoW Forever? Empieza aquí</h2></div><div class="tiles">'
               + ''.join(f'<a class="tile" href="{h}"><strong>{E(t)}</strong><span>{E(d)}</span></a>' for h, t, d in pasos) + '</div></section>')
    return s[:a] + carrusel(latest) + hero + empieza + forever_portal.lanzamiento_inicio() + avisos + cards + news + s[b:]  # Van 30-10: fuera el bloque del torneo (nivel 30, ya pasó)

SEO = {
    '': ('WoW Forever: guías, builds, noticias y lanzamiento | Muchamiel', 'La web de WoW Forever de Muchamiel: lanzamiento del 4 de noviembre, builds de nivel 60, subir de nivel, mazmorras, guías de las nueve clases, macros y noticias.'),
    'calculadora': ('Calculadora de talentos WoW Forever (nivel 10–60 + Legacy) | Muchamiel', 'Calculadora de talentos de WoW Forever para las nueve clases, del nivel 10 al 60 y con Legacy de 0 a 5 puntos. Comparte tu build con un enlace.'),
    'comunes': ('Macros de WoW Forever por clase, comunes y raciales | Muchamiel', 'Todas las macros de WoW Forever: elige tu clase, copia las comunes a todas las clases y las raciales de Horda y Alianza, y aprende a crearlas.'),
    'clases': ('Clases de WoW Forever: guías completas de las nueve clases | Muchamiel', 'Guías completas de las nueve clases de WoW Forever: subir del 1 al 60 con talentos punto a punto, cómo se juega, nivel 60, JcJ y macros.'),
    'razas': ('Razas de WoW Forever: raciales de Alianza y Horda | Muchamiel', 'Todas las razas de WoW Forever, Alianza y Horda, con sus raciales, macros y las clases que pueden jugar.'),
}
for slug, name, cls, color, tagline in classes:
    SEO[slug] = (f'Guía de {name} en WoW Forever: subir del 1 al 60, talentos y nivel 60 | Muchamiel',  # Van 30-10: guía completa
                 f'Guía completa de {name} ({cls}) en WoW Forever: talentos punto a punto para subir del 1 al 60, habilidades por nivel, rotación, razas, nivel 60, JcJ y macros. {tagline}.')


def seo(s, file):
    rel = file.relative_to(dist)
    path = '' if rel.parts[0] == 'index.html' else '/'.join(rel.parts[:-1]) + '/'
    section = rel.parts[0] if len(rel.parts) > 1 else ''
    if rel.name == '404.html':
        return s
    title = desc = None
    if path in ('', 'calculadora/', 'comunes/', 'razas/') or (section in SEO and len(rel.parts) == 2):
        title, desc = SEO[path.rstrip('/') if path else '']
    elif section == 'razas':
        race = of.RACES[rel.parts[1]]
        es = of.RACE_ES[race['race']]
        label = race['race'] if es in race['race'] else f'{race["race"]} ({es})'
        title = f'{label} en WoW Forever: raciales y macros | Muchamiel'
        desc = f'Raciales de {race["race"]} en WoW Forever con su macro: ' + ', '.join(a[0] for a in race['abilities']) + '. Clases: ' + ', '.join(race['classes']) + '.'
    if title:
        s = re.sub(r'<title>.*?</title>', '<title>' + E(title) + '</title>', s, count=1, flags=re.S)
        s = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="' + E(desc, quote=True) + '">', s, count=1)
    title = html.unescape(re.search(r'<title>(.*?)</title>', s, re.S)[1])
    desc = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', s)[1])
    url = SITE + path
    tags = (f'<link rel="canonical" href="{url}"><meta name="theme-color" content="#0b0e15"><meta name="robots" content="index,follow,max-image-preview:large">'
            f'<meta property="og:type" content="website"><meta property="og:site_name" content="WoW Forever · Muchamiel"><meta property="og:locale" content="es_ES">'
            f'<meta property="og:title" content="{E(title, quote=True)}"><meta property="og:description" content="{E(desc, quote=True)}"><meta property="og:url" content="{url}">'
            f'<meta property="og:image" content="{SITE}assets/og.jpg"><meta property="og:image:width" content="1920"><meta property="og:image:height" content="1080">'
            f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:site" content="@Muchamiel_"><meta name="twitter:title" content="{E(title, quote=True)}">'
            f'<meta name="twitter:description" content="{E(desc, quote=True)}"><meta name="twitter:image" content="{SITE}assets/og.jpg">')
    ld = []
    if path == '':
        ld.append({'@context': 'https://schema.org', '@type': 'WebSite', 'name': 'WoW Forever · Muchamiel', 'url': SITE, 'inLanguage': 'es'})
    if path in ('', 'muchamiel/'):
        ld.append({'@context': 'https://schema.org', '@type': 'Person', 'name': 'Muchamiel', 'url': SITE + 'muchamiel/', 'image': AVATAR,
                   'description': 'Streamer y creador de contenido de World of Warcraft en Twitch, Kick y YouTube.',
                   'sameAs': [TWITCH, YT, KICK, 'https://www.tiktok.com/@muchamielwow', 'https://twitter.com/Muchamiel_', 'https://www.instagram.com/muchamiel_/']})
    if path == 'reserva-nombres/':
        ld.append({'@context': 'https://schema.org', '@type': 'NewsArticle', 'headline': 'Reserva tu nombre en WoW Forever: del 27 de octubre al 3 de noviembre',
                   'datePublished': '2026-10-15', 'dateModified': '2026-10-15', 'inLanguage': 'es', 'image': SITE + 'assets/og.jpg', 'mainEntityOfPage': url,
                   'author': {'@type': 'Organization', 'name': 'Comunidad de Muchamiel'}, 'about': 'Reserva anticipada de nombres de World of Warcraft: Forever'})
    if path == 'beta-gratis/':
        ld.append({'@context': 'https://schema.org', '@type': 'NewsArticle', 'headline': 'Juega gratis a WoW Forever el miércoles 21 de octubre a las 19:00',
                   'datePublished': '2026-10-15', 'dateModified': '2026-10-16', 'inLanguage': 'es', 'image': SITE + 'assets/og.jpg', 'mainEntityOfPage': url,
                   'author': {'@type': 'Organization', 'name': 'Comunidad de Muchamiel'}, 'about': 'Prueba de estrés gratuita de la beta de World of Warcraft: Forever'})
    if path == 'noticias/':
        items = [{'@type': 'VideoObject', 'name': limpia(t), 'uploadDate': d, 'thumbnailUrl': f'https://i.ytimg.com/vi/{i}/hqdefault.jpg',
                  'contentUrl': f'https://www.youtube.com/watch?v={i}', 'embedUrl': f'https://www.youtube.com/embed/{i}', 'description': limpia(t)}
                 for i, d, _, t in VIDEOS['video'] + VIDEOS['live']]
        ld.append({'@context': 'https://schema.org', '@type': 'ItemList', 'itemListElement': [dict(position=n, **{'@type': 'ListItem', 'item': it}) for n, it in enumerate(items, 1)]})
    tags += ''.join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False).replace('</', '<\\/') + '</script>' for x in ld)
    s = re.sub(r'<!--seo-->.*?<!--/seo-->', '', s, flags=re.S)
    return s.replace('</head>', '<!--seo-->' + tags + '<!--/seo--></head>', 1)


def footer(base):
    """Pie fijo, igual en todas las páginas (estilo banda de raider.io): columnas, redes, colaboradores y créditos."""
    from embellecer_portal import social_icon
    ext = lambda h: ' target="_blank" rel="noopener noreferrer"' if h.startswith('http') else ''
    col = lambda t, items: f'<div class="foot-col"><h4>{t}</h4>' + ''.join(f'<a href="{h}"{ext(h)}>{E(l)}</a>' for l, h in items) + '</div>'
    icons = ''.join(f'<a class="ico {c}" href="{u}" target="_blank" rel="noopener noreferrer" aria-label="{l}" title="{l}">'
                    + (DISCORD_SVG if l == 'Discord' else social_icon(l).replace('fill="#fff"', 'fill="#0b0e15"').replace('stroke="#fff"', 'stroke="#0b0e15"')) + '</a>'
                    for l, u, c in SOCIALS)
    partners = ''.join(f'<a href="{u}" target="_blank" rel="sponsored noopener noreferrer"><b>{E(n)}</b>' + (f'<small>Código {E(c)}</small>' if c else '') + '</a>'
                       for n, cat, y, tipo, u, c, d, act in BRANDS if act)
    return ('<footer class="site-foot"><div class="foot-in"><div class="foot-grid">'
            f'<div class="foot-brand"><a class="brand" href="{base}">{of.BRAND}{of.BRAND_TXT}</a>'
            '<p>La guía de la comunidad de Muchamiel para WoW Forever: lanzamiento, builds, macros, calculadora y noticias para las nueve clases.</p>'
            f'<div class="foot-icons">{icons}<button type="button" class="ico mail" {CORREO_DATA} aria-label="Correo" title="Correo">{MAIL_SVG}</button></div></div>'
            + col('WoW Forever', [('Lanzamiento', base + 'lanzamiento/'), ('Subir de nivel', base + 'subir-nivel/'), ('Mazmorras', base + 'mazmorras/'), ('Profesiones', base + 'profesiones/'), ('Legacy', base + 'legacy/'), ('Calendario', base + 'calendario/')])
            + col('Guía de la beta', [('Clases', base + 'clases/'), ('Razas', base + 'razas/'), ('Calculadora', base + 'calculadora/'), ('Guía de macros', base + 'comunes/'), ('Addons', base + 'addons/')])
            + col('Comunidad', [('Noticias', base + 'noticias/'), ('Sorteos', base + 'sorteos/'), ('Quién es Muchamiel', base + 'muchamiel/'),
                                ('Directo en Twitch', TWITCH), ('Donar a Muchamiel', DONAR)])
            + col('Patrocinadores', [('Colaboraciones', base + 'colaboraciones/'), ('Contacto profesional', base + 'colaboraciones/#contacto'), ('Patreon', PATREON), ('Discord', DISCORD)])
            + f'</div><div class="foot-partners"><h4>Colaboran con Muchamiel</h4><div>{partners}</div></div>'
            '<div class="foot-legal"><p>© 2026 Comunidad de Muchamiel · Guía no oficial, hecha por y para la comunidad. Datos de la beta consultados el 9 de octubre de 2026; '
            'builds y macros son propuestas para practicar.</p>'
            '<p>World of Warcraft, Warcraft y Blizzard Entertainment son marcas comerciales o registradas de Blizzard Entertainment, Inc. Arte e iconos: Blizzard Entertainment. '
            'Datos de talentos y raciales: <a href="https://talentsforever.com/" target="_blank" rel="noopener noreferrer">Talents Forever</a> '
            '(<a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener noreferrer">CC BY 4.0</a>).</p>'
            f'<p class="foot-mini"><a href="{base}colaboraciones/">Colaboraciones</a><a href="{base}colaboraciones/#contacto">Contacto</a>'
            f'<a href="/sitemap.xml">Mapa del sitio</a></p></div></div></footer>')


# Letra «épica» (Van 15-10, opción 2 de la prueba): Cinzel más gruesa (900) con contorno oscuro y brillo dorado.
EPIC = (# Van 16-10: el menú con vida: apartados en dorado WoW, desplegables en claro y «Notas del parche» como botón azul Blizzard.
        'header.site nav>a:not(.live):not(.nav-parche),header.site .menu-btn{color:#f3c76a;text-shadow:0 0 10px #e8b84a33}'
        'header.site nav>a:not(.live):not(.nav-parche):hover,header.site .menu-btn:hover{color:#fff;text-shadow:0 0 12px #f3c76a99}'
        'header.site nav>a[aria-current]:not(.nav-parche),header.site .menu-btn.cur{color:#fff}'
        'header.site .drop a{color:#e8ecf3;text-shadow:none}header.site .drop a:hover,header.site .drop a[aria-current]{color:#f3c76a}'
        'header.site nav a.nav-parche{margin:12px 6px!important;padding:7px 13px!important;border:1px solid #6fc0ff!important;border-radius:5px;'
        'background:linear-gradient(#2a9bff,#0b5fc4);color:#fff;font-weight:800;text-shadow:0 1px 1px #0008;box-shadow:0 0 14px #148eff66}'
        'header.site nav a.nav-parche:hover{background:linear-gradient(#4fb0ff,#1373e0);color:#fff}'
        'header.site nav a.nav-parche[aria-current]{box-shadow:0 0 0 2px #fff6,0 0 16px #148eff99}'
        'h1{font-weight:900!important;filter:drop-shadow(0 1px 0 #3a2508) drop-shadow(0 0 1px #000) drop-shadow(0 3px 10px #000) drop-shadow(0 0 18px #e8b84a55)!important}'
        'h2,h3,.section>summary,.faction h2,.class-card h3,.tree h2,.tile strong,.apartado strong,.addon h3,.brand b{font-weight:900}'
        'h2,.divider h2,.section>summary{text-shadow:0 1px 0 #3a2508,0 2px 6px #000,0 0 14px #e8b84a40}'
        # Van 15-10: las cajas que no llevan a ningún sitio no deben parecer botones.
        'div.tile{cursor:default;border-left:3px solid #c99a3c88}div.tile:hover{border-color:#3b3222;border-left-color:#c99a3c88;transform:none}'
        '.addon:not(:has(a)):hover{border-color:#2c3444}'
        # El menú se queda con su letra (con Cinzel no cabe) y se aprieta entre 1101 y 1420 px: con dos desplegables se salía a 1280 y 1150.
        '@media(max-width:1640px) and (min-width:1101px){header.site nav a,header.site .menu-btn{padding:21px 6px;font-size:13px}header.site nav a.live{padding:7px 9px}}'
        '@media(max-width:1300px) and (min-width:1101px){header.site nav a,header.site .menu-btn{padding:21px 4px;font-size:12px}header.site .menu-btn:after{margin-left:4px}}'
        '@media(max-width:1300px) and (min-width:1101px){header.site .brand small{display:none}}'
        '@media(max-width:1200px) and (min-width:1101px){header.site nav a,header.site .menu-btn{padding:21px 3px;font-size:11.5px}header.site nav a.live{padding:6px 7px}}')


def extras(s, file):
    base = of.depth_prefix(file) if file.name != '404.html' else '/'
    s = re.sub(r'<style id="comunidad-css">.*?</style>', '', s, flags=re.S)
    s = s.replace('</head>', '<style id="comunidad-css">' + CSS.replace('{base}', base) + EPIC + '</style></head>', 1)
    s = re.sub(r'font:700 (\d+px) "Cinzel"', r'font:900 \1 "Cinzel"', s)
    s = re.sub(r'<script src="[^"]*assets/live\.js" defer></script>', '', s)
    s = re.sub(r'href="((?:\.\./)*|\./|/)#clases"', r'href="\1clases/"', s)
    s = re.sub(r'<footer\b.*?</footer>', footer(base), s, count=1, flags=re.S)
    if 'class="lienzo"' not in s:  # Van 16-10: todo el contenido en un panel; con el fondo de imagen, el texto suelto «flotaba»
        s = re.sub(r'(<main>)(.*?)(<footer\b)', r'\1<div class="lienzo">\2</div>\3', s, count=1, flags=re.S)
    return s.replace('</body>', CONTADOR + f'<script src="{base}assets/live.js" defer></script><script src="{base}assets/cuadra.js" defer></script>' + (f'<script src="{base}assets/avisos.js" defer></script>' if 'data-avisos' in s or 'data-aviso-car' in s else '') + (f'<script src="{base}assets/carrusel.js" defer></script>' if 'data-car' in s else '') + '</body>', 1)


def sitemap():
    urls = [''] + sorted('/'.join(f.relative_to(dist).parts[:-1]) + '/' for f in dist.rglob('index.html') if f.parent != dist)
    prio = {'': '1.0', 'noticias/': '0.9', 'calculadora/': '0.9'}
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
        f'  <url><loc>{SITE}{u}</loc><lastmod>2026-10-09</lastmod><priority>{prio.get(u, "0.7")}</priority></url>\n' for u in urls) + '</urlset>\n'
    (dist / 'sitemap.xml').write_text(xml, encoding='utf-8')
    (dist / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n', encoding='utf-8')


# Macros pedidas por Van después de la entrega de GPT: (clase, id tras el que va, id nuevo, título, explicación, etiquetas, macro).
MACROS_EXTRA = [
    ('warlock', 'C7', 'C7b', 'Elements o, con Shift, Weakness',
     'Las dos maldiciones en un botón: normal, Curse of the Elements; con Shift, Curse of Weakness. Solo una Curse por objetivo: la nueva reemplaza a la otra.',
     ['Shift: variante'], '#showtooltip\n/cast [mod:shift] Curse of Weakness; Curse of the Elements'),
    ('warlock', 'D2', 'D2b', 'Todos los demonios en un botón',
     'Normal: manáfago. Shift: abisario. Ctrl: súcubo. Alt: diablillo. Sin Fel Domination, con el tiempo de invocación normal; si llevas el talento, usa D2.',
     ['Shift/Ctrl/Alt: variante'], '#showtooltip\n/cast [mod:alt] Summon Imp; [mod:shift] Summon Voidwalker; [mod:ctrl] Summon Succubus; Summon Felhunter'),
]


VARITA_TXT = ('Dispara con la varita sin apagarla: con «!» no se cancela si vuelves a pulsar. Ideal para rematar o para gastar los ratos sin maná. '
              'Si el objetivo no es válido, no hace nada.')
VARITA = '#showtooltip Shoot\n/cast !Shoot'
# Van 15-10: macro de varita para las tres clases que la llevan, y en la guía de macros comunes.
MACROS_EXTRA += [
    ('priest', 'M18', 'M19', 'Varita sin apagarla', VARITA_TXT, ['Auto-repetición'], VARITA),
    ('mage', 'M17', 'M18', 'Varita sin apagarla', VARITA_TXT, ['Auto-repetición'], VARITA),
    ('comunes', 'G5', 'G6', 'Varita sin apagarla (Sacerdote, Mago y Brujo)', VARITA_TXT, ['Auto-repetición'], VARITA),
]

# Van 17-10: control de la mascota con el ratón (Cazador y Brujo): mover a un punto (= Ctrl+3, el botón Mover de la barra de mascota),
# quieta/sígueme y las habilidades del demonio sobre el enemigo bajo el ratón.
QUIETA_TXT = ('Normal: la mascota se queda quieta donde está (para que no se coma un control o no tire a un grupo). '
              'Shift: vuelve contigo. Las dos en un botón.')
QUIETA = '/petstay [nomod]\n/petfollow [mod:shift]'
MOVER_TXT = ('Hace lo mismo que Ctrl+3 (el botón «Mover» de la barra de la mascota): sale la peana en el suelo y haces clic donde quieras que vaya. '
             'Así la tienes en el botón que quieras, junto a las demás.')
MOVER = '/petmoveto'
MACROS_EXTRA += [
    ('hunter', 'M2', 'M2b', 'Mascota quieta o conmigo', QUIETA_TXT, ['Shift: variante', 'Mascota'], QUIETA),
    ('hunter', 'M2b', 'M2c', 'Mover la mascota a un punto', MOVER_TXT, ['Ratón: suelo', 'Mascota'], MOVER),
    ('warlock', 'C2', 'C2b', 'Demonio quieto o contigo', QUIETA_TXT, ['Shift: variante', 'Mascota'], QUIETA),
    ('warlock', 'C2b', 'C2c', 'Mover el demonio a un punto', MOVER_TXT, ['Ratón: suelo', 'Mascota'], MOVER),
    ('warlock', 'C2c', 'C2d', 'Spell Lock: enemigo bajo el ratón u objetivo',
     'El manáfago corta el lanzamiento del enemigo que tengas bajo el ratón, sin cambiar de objetivo; si no hay ninguno, al objetivo. Necesita el manáfago fuera.',
     ['Ratón: enemigo', 'Mascota'], '#showtooltip Spell Lock\n/cast [@mouseover,harm,nodead][harm,nodead] Spell Lock'),
    ('warlock', 'C13', 'C13b', 'Seduction: enemigo bajo el ratón u objetivo',
     'La súcubo seduce al enemigo que tengas bajo el ratón sin cambiar de objetivo; si no hay ninguno, al objetivo. La pone en pasivo para que no lo rompa.',
     ['Ratón: enemigo', 'Mascota'], '#showtooltip Seduction\n/petpassive\n/cast [@mouseover,harm,nodead][harm,nodead] Seduction'),
]


def macros_extra():
    for cls, after, new, title, txt, tags, macro in MACROS_EXTRA:
        f = dist / cls / 'index.html'
        s = f.read_text(encoding='utf-8')
        i = re.search(rf'<details[^>]*\bid="{after}"', s).start()
        j = of.block(s, i)[1]
        letra = cls == 'warlock'  # el Brujo numera en el título («C7 · …»); las demás clases y la guía, no
        entry = (f'<details id="{new}" class="entry"><summary>' + (f'{new} · ' if letra else '') + f'{E(title)}</summary><div class="detail-body">'
                 f'<a class="permalink" href="#{new}">' + (f'Enlace a {new}' if letra else 'Enlace directo') + '</a>'
                 f'<p>{E(txt)}</p><p class="mtags">' + ''.join(f'<span>{E(t)}</span>' for t in tags) + '</p>'
                 f'<div class="macro"><button class="copy" type="button">Copiar macro</button><pre><code>{E(macro)}</code></pre></div></div></details>')
        s = s[:j] + entry + s[j:]
        s = re.sub(r'<summary>(\d+) macros para copiar</summary>', lambda m: f'<summary>{int(m[1]) + 1} macros para copiar</summary>', s, count=1)
        f.write_text(s, encoding='utf-8')
    # La varita del Brujo (C17, de GPT) pasa a la versión con «!», igual que las demás.
    f = dist / 'warlock' / 'index.html'
    s = f.read_text(encoding='utf-8')
    a = s.index('<details id="C17" ')
    b = of.block(s, a)[1]
    bloque = s[a:b]
    bloque = re.sub(r'<p>Uso manual\..*?</p>', f'<p>{E(VARITA_TXT)}</p>', bloque, count=1, flags=re.S).replace('/cast Shoot</code>', '/cast !Shoot</code>')
    f.write_text(s[:a] + bloque + s[b:], encoding='utf-8')


def run():
    # Siempre desde la entrega limpia de GPT: así cada cambio se aplica una sola vez.
    base = dist.parent / 'base-gpt'
    from datos_clases import BUILDS, validate
    errores = validate()
    if errores:  # una build de ejemplo con un talento que ya no existe o en otra fila: hay que rehacerla en datos_clases.py
        print('AVISO, builds de ejemplo que no cuadran con los talentos nuevos:', errores)
    if actualizar_talentos.ULTIMO:
        actualizar_talentos.aplicar(actualizar_talentos.ULTIMO, base / 'calculadora' / 'index.html',
                                    presets={c: b for c, b in BUILDS.items() if c != 'Warlock'}, con_fecha=False)
    shutil.rmtree(dist)
    shutil.copytree(base, dist)
    shutil.copyfile(dist / 'assets' / 'horde.png', dist / 'assets' / 'og.jpg')
    (dist / 'assets' / 'live.js').write_text(LIVE_JS, encoding='utf-8')
    shutil.copyfile(Path(__file__).with_name('cuadra.js'), dist / 'assets' / 'cuadra.js')
    shutil.copyfile(Path(__file__).with_name('avisos.js'), dist / 'assets' / 'avisos.js')  # Van 16-10: avisos de Blizzard
    shutil.copyfile(Path(__file__).with_name('carrusel.js'), dist / 'assets' / 'carrusel.js')  # Van 16-10: carrusel de la portada
    shutil.copyfile(Path(__file__).with_name('idioma_macros.js'), dist / 'assets' / 'idioma-macros.js')  # 30-10: macros en el idioma del cliente
    shutil.copyfile(Path(__file__).with_name('hechizos_idiomas.json'), dist / 'assets' / 'hechizos-idiomas.json')  # nombres oficiales de Forever (wago.tools, build 1.60.1.70685)
    import avisos_blizzard
    avisos_blizzard.run(dist)
    import youtube_directo  # Van 16-10: ¿en directo en YouTube? (lo actualiza la tarea de GitHub)
    youtube_directo.run(dist)  # Van 15-10: filas completas y centradas en toda la web
    import reorganizar_portal
    reorganizar_portal.run()
    macros_extra()
    build_pages()
    of.run()  # cabecera, estilo, orden e iconos (también en las páginas nuevas)
    for file in sorted(dist.rglob('*.html')):
        s = file.read_text(encoding='utf-8')
        if file == dist / '404.html':
            s = re.sub(r'<header\b.*?</header>', of.header('/', ''), s, count=1, flags=re.S)
            s = s.replace('href="../', 'href="/').replace('src="../', 'src="/').replace('href="./', 'href="/').replace('src="./', 'src="/').replace('url("./', 'url("/')
        if 'class="macro"' in s and 'idioma-macros.js' not in s and (dist / 'en') not in file.parents:  # 30-10: selector de idioma de las macros
            s = s.replace('</body>', '<script src="/assets/idioma-macros.js" defer></script></body>', 1)
        if file == dist / 'index.html':
            s = home(s)
        if file == dist / 'calculadora' / 'index.html':  # Van 15-10: fuera el párrafo de instrucciones de la calculadora
            s = re.sub(r'<p>Diseña tu reparto entre las tres ramas\..*?</p>', '', s, count=1, flags=re.S)
            import calculadora_bonita
            s = calculadora_bonita.apply(s, classes)
            calculadora_bonita.patch_js(dist / 'calculadora' / 'calculator.js')  # Van 15-10: calculadora centrada, botones de clase y flechas de requisitos
        if file.parent.parent == dist and file.name == 'index.html' and file.parent.name in {c[0] for c in classes}:
            import forever_portal  # Van 16-10: builds de nivel 60 al final de la guía de la clase
            import guias_portal  # Van 30-10: con guía completa, las builds de 60 van dentro de ella
            if not guias_portal.cargar_clase(file.parent.name):
                s = s.replace('<footer', forever_portal.builds60_clase(file.parent.name) + '<footer', 1)
            import calculadora_bonita  # Van 15-10: las builds de ejemplo abren la calculadora con los puntos puestos
            s = calculadora_bonita.guide_links(s, file.parent.name, json.loads(re.search(r'id="talent-data"[^>]*>(.*?)</script>', (dist.parent / 'base-gpt' / 'calculadora' / 'index.html').read_text(encoding='utf-8'), re.S)[1]))
        import raciales_15oct  # Van 16-10: raciales según las notas de la beta del 15-10 (Razas y Macros)
        s = raciales_15oct.aplicar(s)[0]
        s = reorganizar_portal.castellano(s, file)
        s = extras(s, file)
        s = seo(s, file)
        s = raciales_15oct.aplicar(s)[0]  # otra vez tras seo(): las descripciones de las páginas de raza
        import guias_portal  # Van 30-10: guía completa de la clase arriba y la beta debajo; guías de profesiones en su página
        if file.parent.parent == dist and file.name == 'index.html' and file.parent.name in {c[0] for c in classes}:
            s = guias_portal.insertar_clase(s, file.parent.name)[0]
        if file == dist / 'profesiones' / 'index.html':
            s = guias_portal.insertar_prof_index(s)
        if file == dist / 'addons' / 'index.html':
            import guias_extra2  # Van 30-10: más addons y addons de ruta de subida
            s = guias_extra2.insertar_addons(s)
        if file == dist / 'subir-nivel' / 'index.html':
            s = guias_portal.insertar_subir(s)
        file.write_text(s, encoding='utf-8')
    import guias_portal
    print(f"Guías: {guias_portal.registrar_en()} textos en inglés registrados")
    import idiomas
    total, hechas, en = idiomas.construir()
    print(f'Inglés: {hechas}/{total} textos traducidos' + (' → /en/ publicado' if en else ' → /en/ aún no (falta traducir)'))
    sitemap()
    import youtube_auto
    youtube_auto.install(dist)
    import addons_pvp
    addons_pvp.install(dist)
    # Van 30-10: fuera los duelos de nivel 30 (duelos_win) con el resto de la beta
    if actualizar_talentos.ULTIMO:  # la fecha de los datos en «generados el …» (es) y «generated on …» (en)
        for f in (dist / 'calculadora' / 'index.html', dist / 'en' / 'calculadora' / 'index.html'):
            if f.exists():
                actualizar_talentos.aplicar(actualizar_talentos.ULTIMO, f)


if __name__ == '__main__':
    run()
    package()
    print('Comunidad, noticias, sorteos, directo y SEO listos.')
