"""Apartado WoW Retail (Van, 17-10-2026): /retail/… con su propio menú y aspecto (modo «retail»).
Datos: research/retail.md (agente, 16/17-10-2026, cada dato con fuente). Muchamiel no juega Retail: textos neutros,
recomendaciones solo con fuente. Hace de puerta a Forever (la suscripción incluye los dos).
Se llama desde comunidad_portal.build_pages(); oficializar_portal pone la cabecera con el menú de Retail."""
import html, re
from crear_portal import dist

E = html.escape
IV = 'https://www.icy-veins.com/wow/'
WH = 'https://www.wowhead.com/talent-calc/'
FECHA = '17-10-2026'


ICO = 'https://wow.zamimg.com/images/wow/icons/large/'


def ic(n, cls='r-ic', t=''):
    return f'<img class="{cls}" src="{ICO}{n}.jpg" alt="{E(t, quote=True)}" loading="lazy" width="40" height="40">'


def a(href, txt):
    return f'<a href="{E(href, quote=True)}" target="_blank" rel="noopener noreferrer">{txt}</a>'


def fuentes(*items):
    return '<p class="fine">Fuentes: ' + ' · '.join(a(u, E(t)) for t, u in items) + f'. Consultado el {FECHA}; puede cambiar con cada parche.</p>'


PUERTA = ('<div class="r-puerta"><p class="eyebrow">¿SIN NADA QUE HACER HASTA EL PRÓXIMO PARCHE?</p>'
          '<h2>WoW Forever va incluido en tu suscripción</h2>'
          '<p>Con la misma suscripción de Retail juegas a WoW Forever, el nuevo World of Warcraft de nivel 60 que sale el 5 de noviembre: '
          'zonas nuevas, nueve mazmorras nuevas y una raza nueva. Perfecto para las semanas flojas entre parches.</p>'
          '<div class="actions" style="justify-content:center"><a class="btn gold" href="{base}lanzamiento/">Qué es WoW Forever</a>'
          '<a class="btn ghost" href="{base}#empieza">Empieza en Forever</a></div></div>')

ESTADO = [('spell_shadow_shadowfury', 'Expansión', 'Midnight (salió el 2 de marzo de 2026)'), ('achievement_level_90', 'Nivel máximo', '90'),
          ('inv_misc_note_01', 'Parche en vivo', '12.1.5 (desde el 14 de octubre en Europa)'),
          ('inv_relics_hourglass', 'Temporada', 'Temporada 2 de Míticas+, banda y JcJ (desde el 19 de agosto)'),
          ('inv_misc_spyglass_03', 'Próximo parche', '12.1.7 «Echoes of the Worldcore», en pruebas: Blizzard dice «finales de otoño o principios de invierno»'),
          ('spell_arcane_portaldalaran', 'Después', '12.2 «Eclipse» y la Temporada 3 (sin fecha) · The Last Titan, la siguiente expansión, para 2027')]

SECCIONES = [('clases/', 'inv_sword_04', 'Clases', 'Las 40 especializaciones: rol, cómo van en Míticas+ y en banda, guía y talentos.'),
             ('subir-nivel/', 'achievement_level_80', 'Subir de nivel', 'Del 1 al 90: Chromie Time, la ruta de Midnight y trucos para ir rápido.'),
             ('addons/', 'inv_misc_gear_01', 'Addons', 'Los imprescindibles de Midnight y qué cambió con WeakAuras.'),
             ('mazmorras/', 'inv_misc_key_13', 'Mazmorras M+', 'Las 8 de la temporada, afijos de la semana, recompensas y puntuaciones.'),
             ('banda/', 'achievement_boss_ragnaros', 'Banda', 'El Abismo Venenoso jefe a jefe, Kith\'ix y la guarida de Nymrissa.'),
             ('profesiones/', 'trade_blacksmithing', 'Profesiones', 'Qué cambia en Midnight y en 12.1, y las mejores guías.'),
             ('notas/', 'inv_misc_book_09', 'Notas del parche', 'Lo nuevo de 12.1.5 y lo que viene en 12.1.7 y 12.2.'),
             ('calendario/', 'inv_misc_pocketwatch_01', 'Calendario', 'Parches, temporada y eventos de los próximos meses.')]

SEMANA = [('inv_misc_bag_10', 'Gran Cámara', 'Desde +10 en Míticas+ te da opciones de hasta nivel de objeto 318 (Mito 1/6); el cofre final de una +10 llega a 311.'),
          ('inv_misc_coin_17', 'Blasones', 'Desde la semana del 21 de octubre se quita el tope.'),
          ('spell_priest_void-blast', 'Piedras de veneno', 'Esa misma semana, Orin ofrece «Ascending with Venomstones» para mejorar equipo.'),
          ('achievement_dungeon_gloryofthehero', 'Banda y Kith\'ix', 'El Abismo Venenoso y la banda de un jefe del 12.1.5.')]


def tarjetas(items, cls='r-cards'):
    """(icono, título, texto[, href]) → rejilla de tarjetas con icono."""
    out = ''
    for it in items:
        n, t, d = it[:3]
        tag, href = ('a', f' href="{it[3]}"') if len(it) > 3 else ('div', '')
        out += f'<{tag} class="r-card"{href}>{ic(n)}<span><strong>{E(t)}</strong><span>{d}</span></span></{tag}>'
    return f'<div class="{cls}">{out}</div>'


def tira_clases(base):
    return '<div class="r-strip">' + ''.join(
        f'<a href="{base}retail/clases/#{CLS[nom][0]}" title="{E(nom, quote=True)}" style="--c:{CLS[nom][1]}">{ic(CLS[nom][2], "r-ic", nom)}</a>' for nom, _, _ in CLASES) + '</div>'


def inicio(base):
    return ('<div class="r-hero"><p class="eyebrow">WORLD OF WARCRAFT · MIDNIGHT · RETAIL</p><h1>WoW Retail: empieza aquí</h1>'
            '<p class="lead">Todo lo del World of Warcraft actual en castellano: clases, mazmorras, banda, subir de nivel, addons y calendario, '
            'con los datos de la temporada y siempre con su fuente.</p>' + tira_clases(base) + '</div>'
            '<div class="divider"><h2>Cómo está el juego hoy</h2></div>' + tarjetas([(n, k, E(v)) for n, k, v in ESTADO], 'r-cards r-stats') +
            '<p>La suscripción incluye World of Warcraft hasta el nivel 80, WoW Classic, Mists of Pandaria Classic y WoW Forever; '
            'la expansión Midnight (para llegar a 90 y su contenido) se compra aparte.</p>'
            '<div class="divider"><h2>Secciones</h2></div>' + tarjetas([(n, t, E(d), h) for h, n, t, d in SECCIONES], 'r-cards r-secc') +
            '<div class="divider"><h2>Al llegar a 90, cada semana</h2></div>' + tarjetas([(n, t, E(d)) for n, t, d in SEMANA])
            + PUERTA.format(base=base)
            + fuentes(('Blizzard: notas del 12.1.5', 'https://worldofwarcraft.blizzard.com/news/24304162'),
                      ('Blizzard: empieza la Temporada 2', 'https://news.blizzard.com/en-us/article/24294369/midnight-season-2-is-now-live'),
                      ('Blizzard: lo anunciado en BlizzCon 2026', 'https://news.blizzard.com/en-us/article/24301453/everything-announced-at-blizzcon-2026-opening-ceremony'),
                      ('BlizzardWatch: 12.1.7', 'https://blizzardwatch.com/2026/10/15/wow-midnight-patch-12-1-7-release-date'),
                      ('Icy Veins: Temporada 2', 'https://www.icy-veins.com/wow/midnight-mythic-season-2-guide')))


# (clase, slug de Forever o None, [(espec, slug_iv, rol, iv_mm, iv_banda, rio_top200, wh_clase, wh_espec)])
CLASES = [
    ('Caballero de la Muerte', None, [('Sangre', 'blood-death-knight-pve-tank-guide', 'Tanque', 'S', 'S', '84 %', 'death-knight', 'blood'),
                                      ('Escarcha', 'frost-death-knight-pve-dps-guide', 'DPS cuerpo a cuerpo', 'A+', 'A', '3 %', 'death-knight', 'frost'),
                                      ('Profano', 'unholy-death-knight-pve-dps-guide', 'DPS cuerpo a cuerpo', 'A', 'S', '1 %', 'death-knight', 'unholy')]),
    ('Cazador de demonios', None, [('Devastación', 'havoc-demon-hunter-pve-dps-guide', 'DPS cuerpo a cuerpo', 'A', 'B', '5 %', 'demon-hunter', 'havoc'),
                                   ('Venganza', 'vengeance-demon-hunter-pve-tank-guide', 'Tanque', 'A+', 'B', '0 %', 'demon-hunter', 'vengeance'),
                                   ('Devorador (nueva)', 'devourer-demon-hunter-pve-dps-guide', 'DPS a distancia', 'A+', 'A', '4 %', 'demon-hunter', 'devourer')]),
    ('Druida', 'druid', [('Equilibrio', 'balance-druid-pve-dps-guide', 'DPS a distancia', 'A', 'A', '0 %', 'druid', 'balance'),
                         ('Feral', 'feral-druid-pve-dps-guide', 'DPS cuerpo a cuerpo', 'S', 'B', '0 %', 'druid', 'feral'),
                         ('Guardián', 'guardian-druid-pve-tank-guide', 'Tanque', 'S', 'A', '17 %', 'druid', 'guardian'),
                         ('Restauración', 'restoration-druid-pve-healing-guide', 'Sanador', 'A+', 'S', '0 %', 'druid', 'restoration')]),
    ('Evocador', None, [('Devastación', 'devastation-evoker-pve-dps-guide', 'DPS a distancia', 'B', 'A+', '0 %', 'evoker', 'devastation'),
                        ('Preservación', 'preservation-evoker-pve-healing-guide', 'Sanador', 'A', 'A', '0 %', 'evoker', 'preservation'),
                        ('Aumento', 'augmentation-evoker-pve-dps-guide', 'Apoyo', 'C', 'B', '0 %', 'evoker', 'augmentation')]),
    ('Cazador', 'hunter', [('Bestias', 'beast-mastery-hunter-pve-dps-guide', 'DPS a distancia', 'A+', 'C', '3 %', 'hunter', 'beast-mastery'),
                           ('Puntería', 'marksmanship-hunter-pve-dps-guide', 'DPS a distancia', 'A', 'A+', '0 %', 'hunter', 'marksmanship'),
                           ('Supervivencia', 'survival-hunter-pve-dps-guide', 'DPS cuerpo a cuerpo', 'A', 'B', '0 %', 'hunter', 'survival')]),
    ('Mago', 'mage', [('Arcano', 'arcane-mage-pve-dps-guide', 'DPS a distancia', 'S+', 'A+', '19 %', 'mage', 'arcane'),
                      ('Fuego', 'fire-mage-pve-dps-guide', 'DPS a distancia', 'B', 'B', '0 %', 'mage', 'fire'),
                      ('Escarcha', 'frost-mage-pve-dps-guide', 'DPS a distancia', 'B', 'A', '0 %', 'mage', 'frost')]),
    ('Monje', None, [('Maestro cervecero', 'brewmaster-monk-pve-tank-guide', 'Tanque', 'A+', 'A', '0 %', 'monk', 'brewmaster'),
                     ('Tejedor de niebla', 'mistweaver-monk-pve-healing-guide', 'Sanador', 'A', 'B', '0 %', 'monk', 'mistweaver'),
                     ('Viajero del viento', 'windwalker-monk-pve-dps-guide', 'DPS cuerpo a cuerpo', 'S', 'A', '1 %', 'monk', 'windwalker')]),
    ('Paladín', 'paladin', [('Sagrado', 'holy-paladin-pve-healing-guide', 'Sanador', 'S', 'B', '95 %', 'paladin', 'holy'),
                            ('Protección', 'protection-paladin-pve-tank-guide', 'Tanque', 'A', 'S', '0 %', 'paladin', 'protection'),
                            ('Reprensión', 'retribution-paladin-pve-dps-guide', 'DPS cuerpo a cuerpo', 'S', 'A+', '5 %', 'paladin', 'retribution')]),
    ('Sacerdote', 'priest', [('Disciplina', 'discipline-priest-pve-healing-guide', 'Sanador', 'B', 'S', '0 %', 'priest', 'discipline'),
                             ('Sagrado', 'holy-priest-pve-healing-guide', 'Sanador', 'B', 'S', '0 %', 'priest', 'holy'),
                             ('Sombra', 'shadow-priest-pve-dps-guide', 'DPS a distancia', 'B', 'A+', '0 %', 'priest', 'shadow')]),
    ('Pícaro', 'rogue', [('Asesinato', 'assassination-rogue-pve-dps-guide', 'DPS cuerpo a cuerpo', 'S+', 'A+', '48 %', 'rogue', 'assassination'),
                         ('Forajido', 'outlaw-rogue-pve-dps-guide', 'DPS cuerpo a cuerpo', 'S', 'B', '0 %', 'rogue', 'outlaw'),
                         ('Sutileza', 'subtlety-rogue-pve-dps-guide', 'DPS cuerpo a cuerpo', 'A+', 'A', '38 %', 'rogue', 'subtlety')]),
    ('Chamán', 'shaman', [('Elemental', 'elemental-shaman-pve-dps-guide', 'DPS a distancia', 'S+', 'B', '94 %', 'shaman', 'elemental'),
                          ('Mejora', 'enhancement-shaman-pve-dps-guide', 'DPS cuerpo a cuerpo', 'A', 'B', '0 %', 'shaman', 'enhancement'),
                          ('Restauración', 'restoration-shaman-pve-healing-guide', 'Sanador', 'S', 'A', '6 %', 'shaman', 'restoration')]),
    ('Brujo', 'warlock', [('Aflicción', 'affliction-warlock-pve-dps-guide', 'DPS a distancia', 'B', 'A', '0 %', 'warlock', 'affliction'),
                          ('Demonología', 'demonology-warlock-pve-dps-guide', 'DPS a distancia', 'A+', 'S', '1 %', 'warlock', 'demonology'),
                          ('Destrucción', 'destruction-warlock-pve-dps-guide', 'DPS a distancia', 'B', 'B', '0 %', 'warlock', 'destruction')]),
    ('Guerrero', 'warrior', [('Armas', 'arms-warrior-pve-dps-guide', 'DPS cuerpo a cuerpo', 'S+', 'A+', '82 %', 'warrior', 'arms'),
                             ('Furia', 'fury-warrior-pve-dps-guide', 'DPS cuerpo a cuerpo', 'A', 'C', '0 %', 'warrior', 'fury'),
                             ('Protección', 'protection-warrior-pve-tank-guide', 'Tanque', 'A', 'A', '0 %', 'warrior', 'protection')]),
]


# clase → (ancla, color oficial de clase, icono)
CLS = {'Caballero de la Muerte': ('caballero-muerte', '#C41E3A', 'classicon_deathknight'), 'Cazador de demonios': ('cazador-demonios', '#A330C9', 'classicon_demonhunter'),
       'Druida': ('druida', '#FF7C0A', 'classicon_druid'), 'Evocador': ('evocador', '#33937F', 'classicon_evoker'), 'Cazador': ('cazador', '#AAD372', 'classicon_hunter'),
       'Mago': ('mago', '#3FC7EB', 'classicon_mage'), 'Monje': ('monje', '#00FF98', 'classicon_monk'), 'Paladín': ('paladin', '#F48CBA', 'classicon_paladin'),
       'Sacerdote': ('sacerdote', '#FFFFFF', 'classicon_priest'), 'Pícaro': ('picaro', '#FFF468', 'classicon_rogue'), 'Chamán': ('chaman', '#0070DD', 'classicon_shaman'),
       'Brujo': ('brujo', '#8788EE', 'classicon_warlock'), 'Guerrero': ('guerrero', '#C69B6D', 'classicon_warrior')}
SPEC_IC = {'blood': 'spell_deathknight_bloodpresence', 'death-knight/frost': 'spell_deathknight_frostpresence', 'unholy': 'spell_deathknight_unholypresence',
           'havoc': 'ability_demonhunter_specdps', 'vengeance': 'ability_demonhunter_spectank', 'devourer': 'classicon_demonhunter_void',
           'balance': 'spell_nature_starfall', 'feral': 'ability_druid_catform', 'guardian': 'ability_racial_bearform', 'druid/restoration': 'spell_nature_healingtouch',
           'devastation': 'classicon_evoker_devastation', 'preservation': 'classicon_evoker_preservation', 'augmentation': 'classicon_evoker_augmentation',
           'beast-mastery': 'ability_hunter_bestialdiscipline', 'marksmanship': 'ability_hunter_focusedaim', 'survival': 'ability_hunter_camouflage',
           'arcane': 'spell_holy_magicalsentry', 'fire': 'spell_fire_firebolt02', 'mage/frost': 'spell_frost_frostbolt02',
           'brewmaster': 'spell_monk_brewmaster_spec', 'mistweaver': 'spell_monk_mistweaver_spec', 'windwalker': 'spell_monk_windwalker_spec',
           'paladin/holy': 'spell_holy_holybolt', 'paladin/protection': 'ability_paladin_shieldofthetemplar', 'retribution': 'spell_holy_auraoflight',
           'discipline': 'spell_holy_powerwordshield', 'priest/holy': 'spell_holy_guardianspirit', 'shadow': 'spell_shadow_shadowwordpain',
           'assassination': 'ability_rogue_deadlybrew', 'outlaw': 'ability_rogue_waylay', 'subtlety': 'ability_stealth',
           'elemental': 'spell_nature_lightning', 'enhancement': 'spell_shaman_improvedstormstrike', 'shaman/restoration': 'spell_nature_magicimmunity',
           'affliction': 'spell_shadow_deathcoil', 'demonology': 'spell_shadow_metamorphosis', 'destruction': 'spell_shadow_rainoffire',
           'arms': 'ability_warrior_savageblow', 'fury': 'ability_warrior_innerrage', 'warrior/protection': 'ability_warrior_defensivestance'}


def spec_ic(wc, we):
    return SPEC_IC.get(f'{wc}/{we}') or SPEC_IC[we]


def nota(t):
    return f'<span class="r-tier r-{t[0].lower()}">{E(t)}</span>'


def clases(base):
    s = ('<div class="r-hero"><p class="eyebrow">WOW RETAIL · TEMPORADA 2 · 12.1.5</p><h1>Clases de Midnight</h1>'
         '<p class="lead">Las 13 clases y sus 40 especializaciones con su rol, cómo las valoran las guías de referencia en Míticas+ y en banda, '
         'y qué se juega en lo más alto. Cada una con su guía completa y su calculador de talentos.</p></div>'
         '<div class="prepare"><h3>Lo más fuerte ahora mismo</h3><p><strong>Míticas+ (Icy Veins, S+):</strong> Mago Arcano, Pícaro Asesinato, Chamán Elemental y Guerrero Armas. '
         '<strong>En las 200 mejores llaves del mundo</strong> (Raider.IO) casi siempre va Caballero de la Muerte Sangre de tanque, Paladín Sagrado de sanador, '
         'Chamán Elemental, Guerrero Armas y un pícaro. <strong>Banda (Icy Veins, S):</strong> Profano, Restauración de druida, Paladín Protección, Disciplina, Sacerdote Sagrado, '
         'Demonología y Sangre. Son listas del 11-12 de octubre, justo antes del 12.1.5: pueden moverse.</p></div>')
    s += tira_clases(base)
    for nom, forever, specs in CLASES:
        filas = ''.join(f'<tr><th>{ic(spec_ic(wc, we), "r-ic r-ic-s")}{E(e)}</th><td>{E(r)}</td><td>{nota(mm)}</td><td>{nota(bd)}</td><td>{E(rio)}</td>'
                        f'<td>{a(IV + g, "Guía")} · {a(WH + wc + "/" + we, "Talentos")}</td></tr>' for e, g, r, mm, bd, rio, wc, we in specs)
        extra = (f'<p class="r-forever">¿Juegas {E(nom)}? <a href="{base}{forever}/">Así es en WoW Forever →</a></p>' if forever else '')
        an, col, ico = CLS[nom]
        s += (f'<h2 class="r-clsh" id="{an}" style="--c:{col}">{ic(ico)}<span>{E(nom)}</span></h2><div class="r-tabla"><table class="keys r-specs"><tr><th>Especialización</th><td><strong>Rol</strong></td>'
              '<td><strong>Míticas+</strong></td><td><strong>Banda</strong></td><td><strong>Top 200 M+</strong></td><td><strong>Guía y talentos</strong></td></tr>'
              + filas + '</table></div>' + extra)
    s += ('<p class="fine"><strong>Míticas+ y Banda:</strong> tier lists de Icy Veins (Míticas+ del 12-10; banda del 11 y 12-10, tanques del 29-8). '
          '<strong>Top 200 M+:</strong> en cuántos de los 200 mejores runs del mundo de la Temporada 2 aparece cada especialización (Raider.IO, 16-10): es la élite, no el jugador medio. '
          'Las guías son de Icy Veins (en inglés) y los talentos, del calculador de Wowhead.</p>'
          + PUERTA.format(base=base)
          + fuentes(('Icy Veins: Míticas+ DPS', IV + 'mythic-dps-tier-list'), ('Icy Veins: Míticas+ sanadores', IV + 'mythic-healer-tier-list'),
                    ('Icy Veins: Míticas+ tanques', IV + 'mythic-tank-tier-list'), ('Icy Veins: banda DPS', IV + 'dps-rankings-tier-list'),
                    ('Icy Veins: banda sanadores', IV + 'healer-rankings-tier-list'), ('Icy Veins: banda tanques', IV + 'tank-rankings-tier-list'),
                    ('Raider.IO', 'https://raider.io/')))
    return s


MMAS = [('Altar of Fangs', 'Altar de los Colmillos', 'Midnight (nueva en 12.1)', 'Bóvedas de Atal\'Utek, Isla Enroscada (47.2, 68.5)', '30 min'),
        ('Murder Row', 'Murder Row', 'Midnight', 'Lunargenta (57.0, 61.0)', '34 min'),
        ('Den of Nalorakk', 'Guarida de Nalorakk', 'Midnight', 'Zul\'Aman (31.0, 84.0), en la cordillera sur, junto a una cabeza de oso de piedra', '32 min'),
        ('The Blinding Vale', 'Valle Cegador (Valle Enceguecedor)', 'Midnight', 'Harandar (26.8, 78.0)', '30 min'),
        ('Voidscar Arena', 'Arena Lacravacua (Arena Rajavacío)', 'Midnight', 'Alzamiento del Asesino, Tormenta del Vacío (53.7, 34.0)', '30 min'),
        ('Kings\' Rest', 'Reposo de los Reyes', 'Battle for Azeroth', 'Sala de portales de Lunargenta', '33 min'),
        ('Temple of Sethraliss', 'Templo de Sethraliss', 'Battle for Azeroth', 'Sala de portales de Lunargenta', '32 min'),
        ('Ruby Life Pools', 'Estanques de Vida Rubí', 'Dragonflight', 'Sala de portales de Lunargenta', '28 min')]
AFIJOS = [('+2 a +5', 'Guía de Lindormi: marca los enemigos que cuentan para las fuerzas y les baja vida y daño. Ayuda a aprender rutas.'),
          ('+5 a +11', 'Trato de Xal\'atath (cambia cada semana): Ascendente, Ligado al Vacío, Púlsar o Devorar.'),
          ('+7 a +9', 'Reforzada o Tiránica, una cada semana.'),
          ('+10 y más', 'Reforzada y Tiránica a la vez.'),
          ('+12 y más', 'Argucia de Xal\'atath: anula los tratos y cada muerte resta 15 segundos.')]


AF_IC = ['inv_misc_map_01', 'inv_cosmicvoid_orb', 'ability_toughness', 'achievement_boss_archaedas', 'spell_priest_void-blast']
EXP = {'Midnight': ('r-x-mid', 'spell_shadow_shadowfury'), 'Battle for Azeroth': ('r-x-bfa', 'inv_shield_06'), 'Dragonflight': ('r-x-df', 'ability_mount_drake_proto')}


def mazmorras(base):
    cards = ''.join(f'<div class="r-mm {EXP[x.split(" (")[0]][0]}">{ic(EXP[x.split(" (")[0]][1])}<div><span class="r-xb">{E(x)}</span>'
                    f'<strong>{E(es)}</strong><small class="r-en">{E(en)}</small><p>{E(entr)}</p><span class="r-tiempo">⏱ {E(t)}</span></div></div>'
                    for en, es, x, entr, t in MMAS)
    af = ''.join(f'<tr><th>{ic(i, "r-ic r-ic-s")}{E(n)}</th><td>{E(t)}</td></tr>' for i, (n, t) in zip(AF_IC, AFIJOS))
    return ('<div class="r-hero"><p class="eyebrow">WOW RETAIL · MÍTICAS+ · TEMPORADA 2</p><h1>Mazmorras de Míticas+ de la Temporada 2</h1>'
            '<p class="lead">Las 8 mazmorras de la temporada con su entrada y su tiempo, los afijos por nivel de llave, la semana actual, las recompensas y las puntuaciones para estar arriba.</p></div>'
            '<div class="divider"><h2>Las 8 mazmorras</h2></div><div class="r-mms">' + cards + '</div>'
            '<p>Las que no son de Midnight se entran por la <strong>sala de portales de Míticas+</strong>: un portal dorado en Lunargenta (53.3, 66.1), junto a Lindormi y Agmera. '
            'Al completar una +10 a tiempo, ganas un teletransporte permanente a esa mazmorra. Entre paréntesis, el nombre del cliente latinoamericano cuando cambia.</p>'
            '<div class="divider"><h2>Afijos por nivel de llave</h2></div><table class="keys">' + af + '</table>'
            '<p><strong>Esta semana</strong> (desde el 14 de octubre, Europa): Trato de Xal\'atath: Púlsar, Reforzada, Tiránica y Argucia de Xal\'atath.</p>'
            '<div class="divider"><h2>Recompensas y puntuación</h2></div><ul>'
            '<li>El cofre final sube hasta nivel de objeto <strong>311</strong> (Héroe 3/6) en una +10; la Gran Cámara, hasta <strong>318</strong> (Mito 1/6) desde +10. Más allá de +12 no sube.</li>'
            '<li>Logros: <strong>Maestro de piedra angular</strong> con 2.000 de puntuación (montura), <strong>Leyenda</strong> con 3.000 (otra montura) y <strong>Mito</strong> con 3.600 (título y montura, desde el 12.1.5).</li>'
            '<li>Para estar en el 25 % mejor de Europa hace falta unos 3.019 de puntuación; el 10 %, 3.323; el 1 %, 3.744 (Raider.IO, 16-10).</li></ul>'
            '<div class="divider"><h2>Lo que viene: Temporada 3</h2></div>'
            '<p>Blizzard ha adelantado Cavernas de Maisara, Bancal del Magister, Uldaman, Núcleo Pétreo y Catacumbas Putrefactas, más una mazmorra nueva del parche 12.2 «Eclipse». '
            'La lista completa y la fecha aún no son oficiales.</p>'
            + PUERTA.format(base=base)
            + fuentes(('Blizzard: empieza la Temporada 2', 'https://news.blizzard.com/en-us/article/24294369/midnight-season-2-is-now-live'),
                      ('Icy Veins: guía de Míticas+ T2', 'https://www.icy-veins.com/wow/midnight-mythic-season-2-guide'),
                      ('Icy Veins: mazmorras', 'https://www.icy-veins.com/wow/dungeons-guide'), ('Raider.IO', 'https://raider.io/'),
                      ('Blizzard: avance de la Temporada 3', 'https://us.forums.blizzard.com/en/wow/t/2351172')))


JEFES = [('Nek\'zali la Volutadora de Almas', 'Nek\'zali the Soulcoiler', '1'), ('Centinelas sepultados', 'Entombed Sentinels', '2'),
         ('Exploradores perdidos', 'The Lost Explorers', '3'), ('Vashnik el Maligno', 'Vashnik the Malignant', '2'), ('Sszorak', 'Sszorak', '3'),
         ('Los Colmillos Gemelos', 'The Twin Fangs', '1'), ('El Altar en Espiral', 'The Coiled Altar', '4'), ('Ula\'tek', 'Ula\'tek', '4')]


def banda(base):
    jefes = ''.join(f'<div class="r-jefe r-ala{E(al)}"><span class="r-num">{i}</span><div><strong>{E(es)}</strong><small class="r-en">{E(en)}</small>'
                    f'<span class="r-ala">Ala {E(al)}</span></div></div>' for i, (es, en, al) in enumerate(JEFES, 1))
    return ('<div class="r-hero"><p class="eyebrow">WOW RETAIL · BANDA · TEMPORADA 2</p><h1>El Abismo Venenoso</h1>'
            '<p class="lead">La banda de la Temporada 2 de Midnight: dónde está, sus 8 jefes en orden, dificultades y alas del buscador. Más la banda de un jefe del 12.1.5 y la guarida de Nymrissa.</p></div>'
            '<div class="divider"><h2>Dónde y cuándo</h2></div><ul>'
            '<li><strong>Entrada:</strong> Bóvedas de Atal\'Utek, en la Isla Enroscada; el portal está en (47.2, 21.7). Se llega por una de sus tres puertas.</li>'
            '<li><strong>Dificultades:</strong> modo historia, buscador de bandas, normal, heroico y mítico.</li>'
            '<li><strong>Apertura:</strong> normal, heroico, mítico y el ala 1 del buscador desde el 19 de agosto; el resto de alas, una por semana hasta el 9 de septiembre.</li></ul>'
            '<div class="divider"><h2>Los 8 jefes</h2></div><div class="r-jefes">' + jefes + '</div>'
            '<p class="fine">Orden del diario de encuentros; algunas guías dicen que las dos alas centrales se pueden hacer en cualquier orden. '
            'Los nombres en castellano son los que usan las guías en español; pueden variar con el cliente.</p>'
            '<div class="divider"><h2>Más jefes de la temporada</h2></div><ul>'
            '<li><strong>El Desatamiento de Kith\'ix</strong> (12.1.5): banda de un solo jefe bajo el Abismo Venenoso, abierta desde el 14 de octubre en Europa. '
            'Historia, buscador, normal, heroico y mítico (en mítico, grupo de 15 a 25).</li>'
            '<li><strong>Gruta Ligada a la Marea</strong> (Tidebound Grotto): guarida con la jefa Nymrissa, bajo la Isla Enroscada, hasta mítico y para 15-25 jugadores.</li></ul>'
            + PUERTA.format(base=base)
            + fuentes(('Blizzard: empieza la Temporada 2', 'https://news.blizzard.com/en-us/article/24294369/midnight-season-2-is-now-live'),
                      ('Blizzard: notas del 12.1.5', 'https://worldofwarcraft.blizzard.com/news/24304162'),
                      ('Conquest Capped: el Abismo Venenoso', 'https://conquestcapped.com/guides/wow/the-venomous-abyss-raid-overview/'),
                      ('warcraft.wiki.gg', 'https://warcraft.wiki.gg/wiki/Venomous_Abyss'), ('Raider.IO', 'https://raider.io/')))


def subir(base):
    return ('<div class="r-hero"><p class="eyebrow">WOW RETAIL · DEL 1 AL 90</p><h1>Cómo subir de nivel en Midnight</h1>'
            '<p class="lead">La ruta más rápida del 1 al 90: dónde empezar, Chromie Time, el orden de las zonas de Midnight, las mazmorras que más compensan y el modo aventura para los alters.</p></div>'
            '<div class="divider"><h2>Del 1 al 80</h2></div><ul>'
            '<li><strong>Personaje nuevo:</strong> empieza en la Isla del Exilio o en la zona de tu raza; las razas aliadas empiezan en nivel 10.</li>'
            '<li><strong>Chromie Time (10-70):</strong> eliges qué expansión jugar para subir; por defecto, Dragonflight.</li>'
            '<li><strong>Al llegar a 70:</strong> un modo historia rápido de The War Within te pone al día antes de Midnight.</li>'
            '<li>La experiencia necesaria del 1 al 80 se redujo un 43 % con Midnight.</li></ul>'
            '<div class="divider"><h2>Del 80 al 90: la ruta de Midnight</h2></div><div class="r-ruta">'
            '<div><span class="r-num">80-82</span><p>Bosque Canción Eterna</p></div>'
            '<div><span class="r-num">82-88</span><p>Zul\'Aman, Harandar y la cadena de Arator por los Reinos del Este, en el orden que quieras</p></div>'
            '<div><span class="r-num">88-90</span><p>Tormenta del Vacío</p></div></div>'
            '<p>La campaña principal tiene 17 capítulos y te deja casi en 90; el resto, con misiones del mundo. De 80 a 90 se tarda unas 5-7 horas yendo a por ello y unas 10 jugando tranquilo. '
            'Tienes surcacielos desde el principio.</p>'
            '<div class="divider"><h2>Trucos</h2></div><ul>'
            '<li><strong>Mazmorras:</strong> Aguja Brisaveloz (81), Murder Row (83) y Guarida de Nalorakk, Cavernas de Maisara y Valle Cegador (88). Haz cada una una vez, con su misión de campaña activa.</li>'
            '<li><strong>Profundidades:</strong> solo compensan la primera vez, por la misión de primera finalización.</li>'
            '<li><strong>Modo aventura:</strong> al terminar la campaña, tus alters empiezan en Lunargenta y eligen el orden de las zonas, o suben con misiones del mundo y eventos.</li>'
            '<li>Fuego de hogar en Lunargenta, botín automático y la tecla de interactuar; mira los logros de mentor de la banda guerrera (hasta un 25 % más de experiencia).</li></ul>'
            + PUERTA.format(base=base)
            + fuentes(('Icy Veins: subir de nivel en Midnight', 'https://www.icy-veins.com/wow/midnight-leveling-guide'),
                      ('games.gg: guía 1-90', 'https://games.gg/world-of-warcraft/guides/wow-midnight-leveling-guide-level-90/')))


PROFS = [('trade_alchemy', 'Alquimia'), ('trade_blacksmithing', 'Herrería'), ('trade_engraving', 'Encantamiento'), ('trade_engineering', 'Ingeniería'),
         ('inv_inscription_tradeskill01', 'Inscripción'), ('inv_misc_gem_01', 'Joyería'), ('inv_misc_armorkit_17', 'Peletería'), ('trade_tailoring', 'Sastrería'),
         ('trade_herbalism', 'Herboristería'), ('trade_mining', 'Minería'), ('inv_misc_pelt_wolf_01', 'Desuello'), ('inv_misc_food_15', 'Cocina'), ('trade_fishing', 'Pesca')]
PROF_TIRA = '<div class="r-strip r-strip-p">' + ''.join(f'<span title="{n}">' + ic(i, 'r-ic', n) + '</span>' for i, n in PROFS) + '</div>'


def profesiones(base):
    return ('<div class="r-hero"><p class="eyebrow">WOW RETAIL · PROFESIONES</p><h1>Profesiones en Midnight</h1>'
            '<p class="lead">Qué ha cambiado en las profesiones con Midnight y con el parche 12.1, y dónde están las mejores guías para subirlas y hacer oro.</p>' + PROF_TIRA + '</div>'
            '<div class="divider"><h2>Qué cambia en Midnight</h2></div><ul>'
            '<li>Los consumibles tienen <strong>2 calidades</strong> (antes 3); el equipo fabricado sigue con 5.</li>'
            '<li>La Agudeza de artesano pasa a ser <strong>Moxie de artesano por profesión</strong>, sobre todo para comprar recetas.</li>'
            '<li>Árboles de especialización renovados, con la misma idea que en The War Within.</li>'
            '<li>Pedidos de fabricación desde habilidad 15; los pedidos de PNJ dan conocimiento, Moxie, recetas y reactivos.</li>'
            '<li>Bolsa de reactivos para todos, pilas de 1.000 (consumibles, 200).</li>'
            '<li>La <strong>decoración de viviendas</strong> es un mercado nuevo, sobre todo para Joyería e Inscripción.</li></ul>'
            '<div class="divider"><h2>En el parche 12.1</h2></div><ul>'
            '<li><strong>Reinicio único de los puntos de conocimiento</strong> de cada profesión (PNJ Theremis, en Lunargenta).</li>'
            '<li>Recetas nuevas (mucha decoración) y materiales que solo salen en las zonas malditas de la Isla Enroscada; pesca con veneno.</li>'
            '<li>Según Icy Veins, casi todas las recetas nuevas son peores que las de la Temporada 1, salvo mejoras directas como la poción de salud concentrada.</li></ul>'
            '<div class="divider"><h2>Las mejores guías</h2></div><ul>'
            f'<li>{a("https://www.icy-veins.com/wow/professions", "Icy Veins")}: una guía por profesión y guía de oro (inglés).</li>'
            f'<li>{a("https://www.wow-professions.com/midnight/alchemy-guide", "wow-professions.com")}: rutas y puntos de conocimiento por profesión (inglés).</li>'
            '<li>En castellano, en YouTube: Nokzu (una guía por profesión y oro), Jusohr, AlterTime y ElonCS.</li></ul>'
            + PUERTA.format(base=base)
            + fuentes(('Icy Veins: profesiones en Midnight', 'https://www.icy-veins.com/wow/professions'),
                      ('wow-professions.com: reinicio de conocimiento en 12.1', 'https://www.wow-professions.com/news/midnight-patch-12-1-knowledge-point-reset')))


ADDON_IC = ['inv_misc_enggizmos_30', 'achievement_boss_ragnaros', 'achievement_boss_ragnaros', 'inv_relics_hourglass', 'inv_misc_map_01', 'spell_holy_borrowedtime',
            'inv_misc_pocketwatch_01', 'inv_misc_note_01', 'inv_misc_spyglass_03', 'achievement_dungeon_gloryofthehero', 'spell_holy_guardianspirit',
            'inv_misc_gear_01', 'inv_misc_bag_10', 'inv_misc_coin_17', 'inv_misc_map_01']
ADDONS = [('Details!', 'Medidor de daño y sanación', 'https://www.curseforge.com/wow/addons/details'),
          ('BigWigs (+ LittleWigs)', 'Avisos de los jefes en bandas, mazmorras y profundidades', 'https://www.curseforge.com/wow/addons/big-wigs'),
          ('Deadly Boss Mods', 'La alternativa a BigWigs: usa uno de los dos', 'https://www.curseforge.com/wow/addons/deadly-boss-mods'),
          ('Raider.IO', 'Puntuación de Míticas+ en la descripción y en el buscador de grupos', 'https://www.curseforge.com/wow/addons/raiderio'),
          ('Mythic Dungeon Tools', 'Planificar rutas de Míticas+', 'https://www.curseforge.com/wow/addons/mythic-dungeon-tools'),
          ('OmniCD', 'Reutilizaciones del grupo: cortes y defensivos', 'https://www.curseforge.com/wow/addons/omnicd'),
          ('WarpDeplete', 'Temporizador de Míticas+', 'https://www.curseforge.com/wow/addons/warpdeplete'),
          ('Plater / Platynator', 'Placas de nombre (Platynator está hecho para Midnight; parte de los scripts de Plater ya no funcionan)', 'https://www.curseforge.com/wow/addons/plater-nameplates'),
          ('Premade Groups Filter', 'Filtrar el buscador de grupos', 'https://www.curseforge.com/wow/addons/premade-groups-filter'),
          ('Method Raid Tools', 'Asignaciones de banda', 'https://www.curseforge.com/wow/addons/method-raid-tools'),
          ('Cell / VuhDo', 'Marcos de banda para sanadores', 'https://www.curseforge.com/wow/addons/cell'),
          ('ElvUI', 'Interfaz completa (se descarga de tukui.org)', 'https://tukui.org'),
          ('Baganator', 'Bolsas y banco', 'https://www.curseforge.com/wow/addons/baganator'),
          ('Auctionator / TradeSkillMaster', 'Casa de subastas y oro', 'https://www.curseforge.com/wow/addons/auctionator'),
          ('HandyNotes / GatherMate2', 'Notas en el mapa y puntos de recolección', 'https://www.curseforge.com/wow/addons/handynotes')]


def addons(base):
    cards = ''.join(f'<a class="r-card" href="{E(u, quote=True)}" target="_blank" rel="noopener noreferrer">{ic(i)}<span><strong>{E(n)}</strong><span>{E(d)}</span></span></a>'
                    for i, (n, d, u) in zip(ADDON_IC, ADDONS))
    return ('<div class="r-hero"><p class="eyebrow">WOW RETAIL · ADDONS</p><h1>Los mejores addons de Midnight</h1>'
            '<p class="lead">Los 15 addons que más se recomiendan para WoW Midnight en 2026 y lo que cambió con la expansión: WeakAuras ya no funciona en combate.</p></div>'
            '<div class="prepare"><h3>Lo que cambió con Midnight</h3><p>Desde el parche 12.0, los addons ya no pueden leer ni reaccionar a datos de combate en tiempo real. '
            '<strong>WeakAuras solo funciona fuera de combate</strong>, desaparecen Hekili y GTFO, y Blizzard ha metido en la interfaz del juego el gestor de reutilizaciones y la línea temporal de los jefes.</p></div>'
            '<div class="divider"><h2>Los 15 imprescindibles</h2></div><div class="r-cards">' + cards + '</div>'
            '<p>También salen mucho: BugSack (errores), Pawn, Plumber, Leatrix Plus, OmniCC y Bartender4 o Dominos. Para JcJ: Gladius o sArena Reloaded, OmniBar y BigDebuffs.</p>'
            '<p><strong>Cómo instalarlos:</strong> con la app de CurseForge o con Wago, o a mano descomprimiendo cada addon en la carpeta <code>_retail_/Interface/AddOns</code> del juego.</p>'
            + PUERTA.format(base=base)
            + fuentes(('NextTier: addons de Midnight', 'https://nexttier.pro/guide/best-wow-midnight-addons'),
                      ('Conquest Capped: addons de Midnight', 'https://conquestcapped.com/guides/wow/midnight-best-addons/')))


def notas(base):
    return ('<div class="r-hero"><p class="eyebrow">WOW RETAIL · NOTAS DEL PARCHE</p><h1>Notas del parche de WoW Midnight</h1>'
            '<p class="lead">Lo nuevo del parche en vivo y lo que viene, en castellano. Con el enlace a las notas oficiales de Blizzard.</p></div>'
            '<div class="divider"><h2>12.1.5 (en vivo desde el 14 de octubre)</h2></div><ul>'
            '<li>Capítulo de campaña «The Promise of Tomorrow».</li>'
            '<li><strong>El Desatamiento de Kith\'ix:</strong> banda de un solo jefe bajo el Abismo Venenoso.</li>'
            '<li>Primer <strong>Laberinto</strong>: el Laberinto de Kindo\'jan.</li>'
            '<li><strong>Invasiones aqir</strong> en Bosque Canción Eterna y Zul\'Aman.</li>'
            '<li>Logro <strong>Mito</strong> de Míticas+ (3.600 de puntuación, título y montura).</li>'
            '<li>Desde la semana del 21 de octubre: Orin ofrece «Ascending with Venomstones» y se quita el tope de blasones.</li></ul>'
            '<div class="divider"><h2>Ajustes de clase del 27 de octubre</h2></div>'
            '<p>Llegan con el mantenimiento semanal del <strong>martes 27 de octubre</strong>. En JcE:</p><ul class="r-icl">'
            '<li>' + ic('ability_druid_catform', 'r-ic r-ic-s') + '<strong>Feral</strong> (druida): un 5 % más de daño.</li>'
            '<li>' + ic('spell_nature_healingtouch', 'r-ic r-ic-s') + '<strong>Restauración</strong> (druida): más curación en mazmorras (Verdancy +60 %, Recrecimiento +10 %, Alivio presto mejorado al 40 %).</li>'
            '<li>' + ic('ability_hunter_focusedaim', 'r-ic r-ic-s') + '<strong>Puntería</strong> (cazador): más daño en área (Trick Shots, Disparo explosivo y Descarga).</li>'
            '<li>' + ic('spell_fire_firebolt02', 'r-ic r-ic-s') + '<strong>Fuego</strong> (mago): un 5 % más de daño.</li>'
            '<li>' + ic('ability_stealth', 'r-ic r-ic-s') + '<strong>Sutileza</strong> (pícaro): un 8 % menos de daño; se pasaron con la mejora del 12.1.5.</li>'
            '<li>' + ic('spell_shadow_deathcoil', 'r-ic r-ic-s') + '<strong>Aflicción</strong> (brujo): Aflicción inestable, un 20 % más.</li>'
            '<li>' + ic('spell_shadow_rainoffire', 'r-ic r-ic-s') + '<strong>Destrucción</strong> (brujo): Lluvia de fuego, un 20 % más.</li></ul>'
            '<p><strong>En JcJ:</strong> bajan San&#39;layn (caballero de la muerte profano, −20 % a Golpe vampírico) y el mago de Fuego (−5 %). Suben Devorador (cazador de demonios), Preservación (evocador), Puntería (cazador), '
            'Escarcha con Frostfire (mago), Tejedor de niebla (monje), Sagrado (paladín y sacerdote), Asesinato con Deathstalker (pícaro) y Restauración (chamán).</p>'
            '<p>' + a('https://us.forums.blizzard.com/en/wow/t/class-tuning-incoming-october-27/2390748', 'Lista completa de los ajustes (Blizzard, en inglés)') + '</p>'
            '<div class="divider"><h2>Cambios de clase del 12.1.5</h2></div><ul class="r-icl">'
            '<li>' + ic('classicon_demonhunter_void', 'r-ic r-ic-s') + '<strong>Devorador</strong> (cazador de demonios): Colapso estelar ya no entra en reutilización al cancelarlo.</li>'
            '<li>' + ic('ability_stealth', 'r-ic r-ic-s') + '<strong>Sutileza</strong> (pícaro): un 14 % más de daño.</li>'
            '<li>' + ic('ability_warrior_defensivestance', 'r-ic r-ic-s') + '<strong>Protección</strong> (guerrero): un 30 % más a Ejecutar.</li>'
            '<li>' + ic('spell_nature_healingtouch', 'r-ic r-ic-s') + '<strong>Restauración</strong> (druida): rediseño de Nature\'s Bounty.</li>'
            '<li>' + ic('ability_hunter_focusedaim', 'r-ic r-ic-s') + '<strong>Puntería</strong> (cazador): se quita Unload y entra Blood Fletching.</li></ul>'
            f'<p>{a("https://worldofwarcraft.blizzard.com/news/24304162", "Notas oficiales completas del 12.1.5 (Blizzard, en inglés)")}</p>'
            '<div class="divider"><h2>Lo que viene</h2></div><table class="keys">'
            '<tr><th>12.1.7 «Echoes of the Worldcore»</th><td>En pruebas. Campaña en Dornogal, el modo <strong>Talebound</strong> (un RPG de acción JcE aparte), Lorewalking, vuelven las Turbulent Timeways y novedades de las fiestas. '
            'Blizzard dice «finales de otoño o principios de invierno»; BlizzardWatch calcula el 8 de diciembre.</td></tr>'
            '<tr><th>12.2 «Eclipse»</th><td>Una mazmorra nueva de 3 jefes y una banda de 8 en el núcleo del mundo. Después, la Temporada 3. Sin fecha.</td></tr>'
            '<tr><th>The Last Titan</th><td>La siguiente expansión, prevista para 2027.</td></tr></table>'
            + PUERTA.format(base=base)
            + fuentes(('Blizzard: notas del 12.1.5', 'https://worldofwarcraft.blizzard.com/news/24304162'),
                      ('Blizzard: lo anunciado en BlizzCon 2026', 'https://news.blizzard.com/en-us/article/24301453/everything-announced-at-blizzcon-2026-opening-ceremony'),
                      ('BlizzardWatch: 12.1.7', 'https://blizzardwatch.com/2026/10/15/wow-midnight-patch-12-1-7-release-date'),
                      ('Blizzard: notas de pruebas del 12.1.7', 'https://us.forums.blizzard.com/en/wow/t/midnight-echoes-of-the-worldcore-ptr-development-notes/2383391')))


CAL_IC = ['inv_misc_note_01', 'achievement_halloween_witch_01', 'spell_priest_void-blast', 'inv_misc_wrench_01', 'inv_misc_bone_humanskull_02', 'inv_misc_head_dragon_01',
          'achievement_guildperk_fasttrack_rank2', 'inv_misc_food_wheat_01', 'inv_misc_spyglass_03', 'inv_holiday_christmas_present_01', 'inv_misc_ticket_darkmoon_01',
          'inv_relics_hourglass', 'spell_shadow_shadowfury']
CAL = [('14 oct', '12.1.5 en Europa: Kith\'ix, el Laberinto de Kindo\'jan y las Invasiones aqir', 'Oficial'),
       ('19 oct – 2 nov', 'Halloween de Azeroth (Hallow\'s End): el Jinete sin Cabeza en el buscador, de nivel 10 a 90', 'Oficial'),
       ('Semana del 21 oct', 'Orin ofrece «Ascending with Venomstones» y se quita el tope de blasones', 'Oficial'),
       ('27 oct', 'Ajustes de clase en el mantenimiento semanal (Feral, Fuego, Aflicción y Destrucción suben; Sutileza baja)', 'Oficial'),
       ('1 – 3 nov', 'Día de los Muertos', 'Habitual'),
       ('5 nov, 00:00', 'Sale WoW Forever, incluido en tu suscripción (en México, el 4 a las 17:00; en Chile y Argentina, el 4 a las 20:00)', 'Oficial'),
       ('Mediados de nov', 'Aniversario de WoW, con bonificación de experiencia', 'Habitual'),
       ('Semana del 26 nov', 'Generosidad del Peregrino', 'Habitual'),
       ('Hacia el 8 dic', 'Parche 12.1.7 «Echoes of the Worldcore»', 'Estimado'),
       ('16 dic – 2 ene', 'Festival de Invierno (regalos desde el 25)', 'Habitual'),
       ('Cada mes', 'Feria de la Luna Negra (primer domingo) y Paseo en el tiempo cada pocas semanas', 'Habitual'),
       ('Hacia el 26 ene', 'Posible final de la Temporada 2', 'Estimado'),
       ('Sin fecha', '12.2 «Eclipse» y, justo después, la Temporada 3', 'Oficial, sin fecha')]


def calendario(base):
    filas = ''.join(f'<div class="r-tl-i{" r-tl-forever" if "Forever" in t else ""}">{ic(i)}<div><b>{E(f)}</b> <span class="r-est r-est-{E(e.split(",")[0].lower())}">{E(e)}</span><p>{E(t)}</p></div></div>'
                    for i, (f, t, e) in zip(CAL_IC, CAL))
    return ('<div class="r-hero"><p class="eyebrow">WOW RETAIL · FECHAS</p><h1>Calendario de WoW Retail</h1>'
            '<p class="lead">Parches, temporada y eventos de World of Warcraft de aquí a enero. Marcado si es oficial, si es la fecha de cada año o si es una estimación.</p></div>'
            '<div class="divider"><h2>Próximas fechas</h2></div><div class="r-tl">' + filas + '</div>'
            '<p class="fine"><strong>Habitual:</strong> las fechas de otros años; Blizzard aún no las ha anunciado para 2026. <strong>Estimado:</strong> cálculos de BlizzardWatch o ggseason.com.</p>'
            + PUERTA.format(base=base)
            + fuentes(('Blizzard: notas del 12.1.5', 'https://worldofwarcraft.blizzard.com/news/24304162'),
                      ('BlizzardWatch: 12.1.7', 'https://blizzardwatch.com/2026/10/15/wow-midnight-patch-12-1-7-release-date'),
                      ('warcraft.wiki.gg: Halloween de Azeroth', 'https://warcraft.wiki.gg/wiki/Hallow%27s_End'),
                      ('warcraft.wiki.gg: Festival de Invierno', 'https://warcraft.wiki.gg/wiki/Feast_of_Winter_Veil'), ('ggseason.com', 'https://ggseason.com/wow/')))


# Van 24-10: Retail con sus propias noticias (antes el menú llevaba a las de Forever). De más nueva a más antigua; cada una con su enlace oficial.
NOTICIAS = [  # (fecha, icono, título, texto, enlace o ruta interna)
    ('29 oct', 'spell_shadow_raisedead', 'Demo de «Historias de leyenda» (Talebound), del 30 de octubre al 1 de noviembre',
     'Una demo en el reino de pruebas que se puede jugar <strong>sin suscripción</strong>: tres relatos de terror (Darkhaven, Greenthistle Wood y la expedición de Greywake), tres dificultades (Normal, Veterano y Heroico) y tres clases propias (Slayer, Inquisitor y Witch), todas con doble salto, esquiva y bloqueo. Algunos talentos aún pueden cambiar.', 'https://worldofwarcraft.blizzard.com/news/24313107'),
    ('27 oct', 'inv_misc_wrench_01', 'Ajustes de clase en el mantenimiento',
     'Suben Feral, Fuego, Aflicción y Destrucción, y Restauración de druida cura más en mazmorras; Sutileza baja un 8 %. En JcJ, más cambios.', 'notas/'),
    ('23 oct', 'spell_priest_void-blast', 'Cómic animado «Singularity»',
     'Arator Windrunner se adentra en el Vacío con su mentor, Umbric, buscando pistas de sus padres desaparecidos. Con la voz de Yuri Lowenthal; también se puede descargar en PDF.', 'https://worldofwarcraft.blizzard.com/news/24313104'),
    ('23 oct', 'inv_misc_gear_01', 'Arreglos de la semana',
     'Blizzard sigue publicando arreglos casi a diario: invocaciones del brujo que atacaban a enemigos lejanos, un efecto del chamán Mejora que no salía, el Laberinto de Kindo&#39;jan…', 'https://us.forums.blizzard.com/en/wow/t/world-of-warcraft-midnight-hotfixes-october-23/2382684'),
    ('22 oct', 'inv_misc_spyglass_03', '12.1.7 «Echoes of the Worldcore» sigue en pruebas',
     'El reino de pruebas se ha actualizado con más arreglos. Blizzard sigue sin dar fecha: «finales de otoño o principios de invierno».', 'https://us.forums.blizzard.com/en/wow/t/midnight-echoes-of-the-worldcore-ptr-development-notes/2383391'),
    ('21 oct', 'inv_misc_coin_17', 'Ofertas de otoño, hasta el 2 de noviembre',
     'Midnight a mitad de precio, descuentos para subir un personaje, hasta un 30 % en servicios del juego y hasta un 40 % en algunas transfiguraciones.', 'https://worldofwarcraft.blizzard.com/news/24313103'),
    ('19 oct', 'achievement_halloween_witch_01', 'Halloween de Azeroth, del 19 de octubre al 2 de noviembre',
     'Este año, con cubos de caramelos por Quel&#39;Thalas, sustos en tu barrio (las casas), vendedores con decoración nueva para tu casa y logros nuevos. El Jinete sin Cabeza vuelve al buscador.', 'https://worldofwarcraft.blizzard.com/news/24310656'),
    ('19 oct', 'achievement_boss_kingymiron_01', 'Una semana más para «Let Me Solo Him: Kindo&#39;jan»',
     'Por los fallos del Laberinto en la primera semana del 12.1.5, el logro legendario se puede conseguir hasta el mantenimiento de la semana del 27 de octubre.', 'https://us.forums.blizzard.com/en/wow/t/fabled-let-me-solo-him-kindojan-achievement-extended-an-additional-week/2387015'),
    ('19 oct', 'ability_hunter_beastcall', 'Pack de Rexxar en la tienda, hasta el 8 de noviembre',
     'La apariencia de Rexxar, un trofeo para tu casa y Misha y Huffer como mascotas de combate del cazador.', 'https://shop.battle.net/product/world-of-warcraft-champion-of-the-wilds-pack'),
]


def noticias(base):
    enlace = lambda h: (f'<a href="{base}retail/{h}">Ver más</a>' if not h.startswith('http') else a(h, 'Fuente oficial'))
    filas = ''.join(f'<div class="r-tl-i">{ic(i)}<div><b>{E(f)}</b> · <strong>{t}</strong><p>{d} {enlace(h)}</p></div></div>' for f, i, t, d, h in NOTICIAS)
    return ('<div class="r-hero"><p class="eyebrow">WOW RETAIL · NOTICIAS</p><h1>Noticias de WoW Midnight</h1>'
            '<p class="lead">Lo último de World of Warcraft Midnight en castellano: parches, ajustes de clase, eventos y ofertas. Cada noticia, con su enlace oficial de Blizzard.</p></div>'
            '<div class="divider"><h2>Lo último</h2></div><div class="r-tl">' + filas + '</div>'
            '<div class="divider"><h2>Más de Retail</h2></div>'
            + tarjetas([('inv_misc_book_09', 'Notas del parche', 'Lo nuevo del 12.1.5 y lo que viene.', base + 'retail/notas/'),
                        ('inv_misc_pocketwatch_01', 'Calendario', 'Parches, temporada y eventos.', base + 'retail/calendario/'),
                        ('inv_misc_key_13', 'Mazmorras M+', 'Afijos de la semana y recompensas.', base + 'retail/mazmorras/'),
                        ('inv_sword_04', 'Clases', 'Cómo va cada especialización.', base + 'retail/clases/')])
            + PUERTA.format(base=base)
            + fuentes(('Blizzard: WoW Weekly del 23 de octubre', 'https://worldofwarcraft.blizzard.com/news/24313106'),
                      ('Blizzard: avisos en el foro', 'https://us.forums.blizzard.com/en/wow/groups/blizzard-tracker/posts')))


# (subcarpeta, función, título, descripción)
PAGINAS = [
    ('', inicio, 'WoW Retail (Midnight) en castellano: clases, Míticas+, banda y guías | Muchamiel',
     'Todo lo de World of Warcraft Midnight en castellano: parche 12.1.5, Temporada 2, clases, mazmorras de Míticas+, banda, subir de nivel, addons y calendario.'),
    ('clases', clases, 'Mejores clases de WoW Midnight Temporada 2: tier list de las 40 especializaciones | Muchamiel',
     'Las 40 especializaciones de WoW Midnight con su rol, tier list de Míticas+ y banda, lo que se juega en las mejores llaves, guía y talentos.'),
    ('mazmorras', mazmorras, 'Míticas+ Temporada 2 de WoW Midnight: mazmorras, afijos y recompensas | Muchamiel',
     'Las 8 mazmorras de Míticas+ de la Temporada 2 de Midnight: entradas, tiempos, afijos de la semana, recompensas y puntuaciones.'),
    ('banda', banda, 'El Abismo Venenoso: banda de WoW Midnight, jefes y alas | Muchamiel',
     'La banda de la Temporada 2 de Midnight: el Abismo Venenoso, sus 8 jefes, dificultades y alas del buscador; Kith\'ix y la guarida de Nymrissa.'),
    ('subir-nivel', subir, 'Cómo subir de nivel rápido en WoW Midnight del 1 al 90 | Muchamiel',
     'Guía para subir del 1 al 90 en WoW Midnight: Chromie Time, ruta de zonas, mazmorras, modo aventura y trucos.'),
    ('profesiones', profesiones, 'Profesiones en WoW Midnight: cambios y mejores guías | Muchamiel',
     'Qué cambia en las profesiones de WoW Midnight y en el parche 12.1, y las mejores guías para subirlas y hacer oro.'),
    ('noticias', noticias, 'Noticias de WoW Midnight: parches, ajustes de clase y eventos | Muchamiel',
     'Lo último de WoW Midnight en castellano: ajustes de clase, parche 12.1.7, Halloween de Azeroth, ofertas y cómic animado, con enlace oficial.'),
    ('addons', addons, 'Mejores addons de WoW Midnight en 2026 | Muchamiel',
     'Los 15 addons imprescindibles de WoW Midnight y qué cambió con WeakAuras en la expansión.'),
    ('notas', notas, 'Notas del parche 12.1.5 de WoW Midnight en castellano | Muchamiel',
     'Lo nuevo del parche 12.1.5 de WoW Midnight, cambios de clase y lo que viene en 12.1.7 y 12.2 Eclipse.'),
    ('calendario', calendario, 'Calendario de WoW Retail: parches, temporada y eventos | Muchamiel',
     'Fechas de WoW Midnight de aquí a enero: parches, fin de temporada, Halloween de Azeroth, aniversario y Festival de Invierno.'),
]

CSS = '''
.r-puerta{margin:34px 0 10px;padding:26px 22px;text-align:center;border:1px solid #c99a3c;border-radius:12px;background:linear-gradient(120deg,#2a1a3f,#0d0b16 70%)}
.r-puerta h2{margin:6px 0 10px}.r-puerta p{max-width:720px;margin-left:auto;margin-right:auto}
.r-tabla{overflow-x:auto}.r-specs td,.r-specs th{white-space:nowrap}.r-specs td:last-child{white-space:normal}
.r-tier{display:inline-block;min-width:30px;padding:2px 8px;border-radius:5px;font-weight:800;text-align:center;color:#120c02}
.r-s{background:#ff8000}.r-a{background:#a335ee;color:#fff}.r-b{background:#0070dd;color:#fff}.r-c{background:#1eff00}.r-d{background:#9d9d9d}
.r-en{display:block;font-weight:400;font-size:12.5px;color:#a9b3c4}
.r-forever{margin:8px 0 0;text-align:right;font-size:14px}
.r-est{display:inline-block;padding:2px 8px;border-radius:5px;font-size:12.5px;font-weight:700;white-space:nowrap}
.r-est-oficial{background:#1f6f43;color:#fff}.r-est-habitual{background:#3a4560;color:#fff}.r-est-estimado{background:#7a5a12;color:#fff}
.r-hero{position:relative;margin:4px -32px 22px;padding:34px 32px 26px;text-align:center;border-top:1px solid #4a2f7a;border-bottom:1px solid #4a2f7a;overflow:hidden;
 background:radial-gradient(ellipse at 50% 0,#8b4fe455,transparent 65%),radial-gradient(ellipse at 15% 100%,#3a1d7a66,transparent 60%),radial-gradient(ellipse at 85% 100%,#1d3f7a55,transparent 60%),linear-gradient(#120b22,#0a0714)}
.r-hero:after{content:"";position:absolute;left:10%;right:10%;bottom:0;height:1px;background:linear-gradient(90deg,transparent,#c99a3c,transparent)}
.r-hero h1{text-shadow:0 0 28px #8b4fe4aa}.r-hero .lead{max-width:760px;margin-left:auto;margin-right:auto}
.r-ic{width:40px;height:40px;flex:none;border-radius:7px;border:1px solid #000;box-shadow:0 0 0 1px #c99a3c88,0 4px 10px #0009}
.r-ic-s{width:26px;height:26px;border-radius:5px;vertical-align:middle;margin:0 9px 0 0}
.r-strip{display:flex;flex-wrap:wrap;justify-content:center;gap:9px;margin:18px auto 6px;max-width:680px}
.r-strip a,.r-strip span{display:block;border-radius:8px;transition:transform .15s,box-shadow .15s}
.r-strip a:hover{transform:translateY(-3px) scale(1.08);box-shadow:0 0 14px var(--c)}.r-strip a .r-ic{box-shadow:0 0 0 2px var(--c),0 4px 10px #0009}
.r-cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px;margin:8px 0 18px}
.r-card{display:flex;gap:14px;align-items:flex-start;padding:14px 16px;border:1px solid #3a2a5c;border-radius:10px;background:linear-gradient(160deg,#1a1230,#0d0a18);text-decoration:none;color:#dfe5ee;transition:border-color .15s,transform .15s}
a.r-card:hover{border-color:#b98cff;transform:translateY(-2px)}
.r-card strong{display:block;color:#ffe7a6;font-size:16px;margin:1px 0 4px}.r-card>span>span{display:block;font-size:13.5px;line-height:1.5;color:#b7bfd0}
.r-stats .r-card strong{font-size:12px;letter-spacing:.07em;text-transform:uppercase;color:#b98cff}.r-stats .r-card>span>span{font-size:14.5px;color:#eef2f8}
.r-cls{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;margin:18px auto 8px}
.r-cls a{display:flex;align-items:center;gap:10px;padding:9px 10px;border:1px solid #2c2440;border-left:3px solid var(--c);border-radius:8px;background:#110d1e;color:var(--c);text-decoration:none;font-size:14px;transition:background .15s}
.r-cls a:hover{background:#1e1636}.r-cls .r-ic{width:32px;height:32px}
.r-clsh{display:flex;align-items:center;gap:12px;margin:34px 0 10px;padding:0 0 8px;border-bottom:2px solid var(--c);color:var(--c);scroll-margin-top:90px}
.r-clsh .r-ic{box-shadow:0 0 0 2px var(--c),0 0 16px var(--c)}
.r-mms{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px;margin:8px 0 14px}
.r-mm{display:flex;gap:14px;padding:16px;border:1px solid #3a2a5c;border-top:3px solid var(--x);border-radius:10px;background:linear-gradient(160deg,#1a1230,#0d0a18)}
.r-mm strong{display:block;color:#ffe7a6;font-size:17px;margin-top:6px}.r-mm p{margin:8px 0;font-size:13.5px;color:#b7bfd0}
.r-x-mid{--x:#a970ff}.r-x-bfa{--x:#e8b84a}.r-x-df{--x:#e0573c}
.r-xb{display:inline-block;padding:2px 8px;border-radius:999px;font-size:11.5px;font-weight:700;background:color-mix(in srgb,var(--x) 22%,transparent);color:var(--x)}
.r-tiempo{font-size:13px;font-weight:700;color:#dfe5ee}
.r-jefes{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px;margin:8px 0 14px}
.r-jefe{display:flex;gap:12px;align-items:center;padding:12px 14px;border:1px solid #3a2a5c;border-radius:10px;background:linear-gradient(160deg,#1a1230,#0d0a18)}
.r-jefe strong{display:block;color:#ffe7a6}
.r-num{display:inline-flex;align-items:center;justify-content:center;min-width:40px;height:40px;padding:0 8px;flex:none;border-radius:999px;font-weight:800;color:#120c02;background:linear-gradient(#e8bf55,#a87a24);box-shadow:0 0 12px #e8b84a55}
.r-ala{display:inline-block;margin-top:5px;padding:1px 8px;border-radius:999px;font-size:12px;font-weight:700;background:#2b1f47;color:#c9a6ff}
.r-ruta{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:8px 0 14px;counter-reset:r}
.r-ruta>div{display:flex;flex-direction:column;align-items:center;text-align:center;gap:8px;padding:18px 14px;border:1px solid #3a2a5c;border-radius:10px;background:linear-gradient(160deg,#1a1230,#0d0a18)}
.r-ruta p{margin:0;color:#dfe5ee}
.r-icl{list-style:none;padding:0}.r-icl li{display:flex;align-items:center;flex-wrap:wrap;gap:4px;margin:8px 0}.r-icl .r-ic-s{margin-right:6px}
.r-tl{position:relative;margin:10px 0 16px;padding-left:22px;border-left:2px solid #4a2f7a}
.r-tl-i{position:relative;display:flex;gap:14px;align-items:flex-start;margin:0 0 14px;padding:12px 14px;border:1px solid #3a2a5c;border-radius:10px;background:linear-gradient(160deg,#1a1230,#0d0a18)}
.r-tl-i:before{content:"";position:absolute;left:-30px;top:22px;width:12px;height:12px;border-radius:50%;background:#b98cff;box-shadow:0 0 10px #b98cff}
.r-tl-i b{color:#ffe7a6}.r-tl-i p{margin:5px 0 0;color:#dfe5ee}
.r-tl-forever{border-color:#c99a3c;background:linear-gradient(160deg,#2a1f0c,#120d05)}.r-tl-forever:before{background:#e8b84a;box-shadow:0 0 12px #e8b84a}
.r-specs th{vertical-align:middle}
@media(max-width:700px){.r-hero{margin:4px -14px 18px;padding:24px 14px 20px}.r-ruta{grid-template-columns:1fr}.r-strip .r-ic{width:34px;height:34px}}
'''


def build():
    tpl = (dist / 'comunes' / 'index.html').read_text(encoding='utf-8')
    head = tpl[:tpl.index('<body')].replace('</head>', '<style>' + CSS + '</style></head>', 1)
    foot = tpl[tpl.index('<footer'):tpl.index('</footer>') + 9]
    for sub, fn, title, desc in PAGINAS:
        d = dist / 'retail' / sub if sub else dist / 'retail'
        base = '../../' if sub else '../'
        h = re.sub(r'<title>.*?</title>', '<title>' + E(title) + '</title>', head, count=1, flags=re.S)
        h = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="' + E(desc, quote=True) + '">', h, count=1)
        d.mkdir(parents=True, exist_ok=True)
        (d / 'index.html').write_text(h + '<body><header></header><main>' + fn(base) + foot + '</main></body></html>', encoding='utf-8')
