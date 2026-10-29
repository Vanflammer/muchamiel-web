"""Additional Forever PvP addons, localized after the main translation pass."""
from html import escape


def section(en=False):
    def t(es, eng):
        return eng if en else es

    cards = [
        ('Dino Nameplates Forever', 'dino-nameplates-forever', 'ability_warrior_challange',
         t('Placas · jugadores y unidades visibles', 'Nameplates · players and visible units'),
         t('Adaptación de KuiNameplates específica para Forever, con descargas durante la beta. Una opción para mejorar la lectura de las barras enemigas; activa las placas de mascotas y tótems en la UI del juego.',
           'A KuiNameplates adaptation specifically for Forever, with downloads during beta. An option for clearer enemy health bars; enable pet and totem nameplates in the game UI.'),
         t('Usa un solo addon de placas a la vez para evitar solapamientos. La versión Forever no garantiza avisos de voz ni detección de todos los cooldowns.',
           'Use only one nameplate addon at a time to avoid overlapping displays. The Forever version does not guarantee voice alerts or detection of every cooldown.')),
        ('BetterBlizzPlates', 'betterblizzplates', 'spell_shadow_charm',
         t('Placas · las de Blizzard, mejoradas', "Nameplates · Blizzard's, improved"),
         t('Las placas de vida de Blizzard de siempre con muchas más opciones y ajustes sencillos: resaltar objetivo y foco, iconos de clase, auras y avisos. Preparado para WoW Forever y con millones de descargas.',
           'The standard Blizzard nameplates with many more features and easy settings: highlight target and focus, class icons, auras and alerts. WoW Forever ready, with millions of downloads.'),
         t('Elige uno: BetterBlizzPlates o Dino Nameplates, no los dos a la vez. Ábrelo con /bbp y empieza por un perfil de PvP.',
           'Pick one: BetterBlizzPlates or Dino Nameplates, not both at once. Open it with /bbp and start from a PvP profile.')),
        ('Forever Simple Cast', 'forever-simple-cast', 'spell_holy_flashheal',
         t('Duelos · barras de casteo', 'Duels · cast bars'),
         t('Barras de casteo para ti, objetivo, foco, mascota y placas, con ajustes de presentación. Útil para ver las curas y casteos del rival sin depender de marcos de arena.',
           'Cast bars for you, target, focus, pet and nameplates, with display settings. Useful for seeing enemy heals and casts without relying on arena frames.'),
         t('Coloca objetivo y foco cerca del centro. Las barras de casteo no equivalen a un historial de hechizos instantáneos ni a un contador de todos los cooldowns del rival.',
           'Position target and focus near the centre. Cast bars are not an instant-spell history or a tracker of every enemy cooldown.')),
        ('Warlock HUD', 'warlock-hud', 'spell_shadow_shadowbolt',
         t('Brujo · habilidades y DoTs', 'Warlock · abilities and DoTs'),
         t('Panel específico para Forever: DoTs del objetivo, Nightfall, Healthstone, raciales, buffs y Soul Shards. No depende de marcos de arena.',
           'A dedicated Forever HUD: target DoTs, Nightfall, Healthstone, racials, buffs and Soul Shards. It does not depend on arena frames.'),
         t('Abre /whud. Ajusta los iconos y coloca las filas con Edit Mode. Comprueba los temporizadores en un duelo antes de competir.',
           'Open /whud. Adjust the icons and position rows with Edit Mode. Check timers in a duel before competing.')),
        ('Forever Simple DR', 'forever-simple-dr', 'spell_shadow_possession',
         t('Duelos · DR del objetivo', 'Duels · target DR'),
         t('Muestra DR en el objetivo y las placas enemigas: siguiente control al 50 %, al 25 % o inmunidad, y tiempo de reinicio. Sigue objetivo, foco y placas visibles; los tiempos estimados aparecen en gris.',
           'Shows DR on your target and enemy nameplates: next CC at 50%, 25% or immunity, plus reset time. Tracks target, focus and visible nameplates; estimated timings appear grey.'),
         t('Abre /fdr y activa Blizzard data → Turn on. Usa /fdr unlock para colocar el panel. En BGs hay más restricciones de datos; no todos los tiempos son exactos.',
           'Open /fdr and enable Blizzard data → Turn on. Use /fdr unlock to position the bar. BGs have additional data restrictions; not all timers are exact.')),
        ('TrinketMenu Forever Edition', 'trinketmenu-forever-edition', 'inv_jewelry_talisman_07',
         t('Equipo · cambiar abalorios', 'Gear · swap trinkets'),
         t('Una barrita con tus dos abalorios equipados: pasa el ratón por encima y salen los de tus bolsas para cambiarlos con un clic. El TrinketMenu de siempre, rehecho para Forever.',
           'A small bar with your two equipped trinkets: hover over it and the ones in your bags pop out so you can swap them with one click. The classic TrinketMenu, rebuilt for Forever.'),
         t('Para cambiar el abalorio de PvP o el que está en enfriamiento sin abrir el personaje ni las bolsas.',
           'Swap your PvP trinket or the one on cooldown without opening your character panel or bags.')),
        ('ForeverAuras', 'foreverauras', 'spell_shadow_detectinvisibility',
         t('Personalización · alternativa a WeakAuras', 'Customization · WeakAuras alternative'),
         t('Adaptación de WeakAuras para Forever, aún en desarrollo durante la beta. Permite crear paneles de iconos y avisos dentro de lo que expone el cliente.',
           'A WeakAuras adaptation for Forever, still under development during beta. Create icon displays and alerts within the information exposed by the client.'),
         t('Abre /fa o /foreverauras. Una aura de Classic o Retail no queda validada por importarla: prueba sus condiciones y avisos en Forever.',
           'Open /fa or /foreverauras. Importing a Classic or Retail aura does not validate it: test its triggers and alerts in Forever.')),
        ('Gladius Reloaded', 'gladius-reloaded', 'achievement_arena_2v2_1',
         t('Marcos de arena · comprobar el modo', 'Arena frames · check the mode'),
         t('Existe un archivo marcado Forever. El autor anuncia DR, casteos, abalorios y cooldowns, pero el diseño es de marcos de arena: no se confirma aquí su funcionamiento en duelos ni BGs.',
           'A file is tagged Forever. The author advertises DR, casts, trinkets and cooldowns, but it is designed around arena frames: duel and BG support is not confirmed here.'),
         t('Para duelos, empieza con Forever Simple DR y barras de objetivo/foco. No instales Gladius esperando que muestre automáticamente al rival de un duelo.',
           'For duels, start with Forever Simple DR and target/focus bars. Do not install Gladius expecting it to automatically show a duel opponent.')),
    ]
    out = '<section id="pvp-addons"><div class="divider"><h2>' + t('Addons PvP', 'PvP addons') + '</h2></div>'
    out += '<p class="sub">' + t('Opciones con versión Forever y descargas durante la beta, para duelos, BGs y mundo abierto. Las descargas indican interés, no garantizan cada función en todos los modos. Selección de Van; funciones contrastadas con sus autores el 9 de octubre de 2026, sin prueba directa en el cliente. No son recomendaciones atribuidas a Muchamiel.',
        'Options with a Forever release and downloads during beta, for duels, BGs and world PvP. Downloads indicate interest, not a guarantee that every feature works in every mode. Selected by Van; features checked against the authors’ pages on Oct 9, 2026, without direct client testing. These recommendations are not attributed to Muchamiel.') + '</p><div class="addons">'
    for name, slug, icon, category, description, setup in cards:
        out += (f'<article class="addon"><img loading="lazy" src="https://wow.zamimg.com/images/wow/icons/large/{icon}.jpg" alt="">'
                f'<div><p class="eyebrow">{escape(category)}</p><h3>{name}</h3><p>{escape(description)}</p><p>{escape(setup)}</p>'
                f'<a class="btn ghost" href="https://www.curseforge.com/wow/addons/{slug}" target="_blank" rel="noopener noreferrer">'
                + t('Ver y descargar en CurseForge', 'View and download on CurseForge') + '</a></div></article>')
    out += '</div><div class="prepare"><h3>' + t('Configuración recomendada para duelos', 'Recommended duel setup') + '</h3><p>'
    out += t('Brujo: Warlock HUD + Forever Simple DR. Añade ForeverAuras si quieres personalizar otros avisos. Descarga siempre el archivo marcado Forever y comprueba el conjunto en duelos antes del torneo.',
             'Warlock: Warlock HUD + Forever Simple DR. Add ForeverAuras if you want to customize other alerts. Always download the file tagged Forever and test the combination in duels before the tournament.') + '</p></div>'
    out += '<div class="divider"><h2>' + t('Placas de vida: mascotas y tótems enemigos', 'Nameplates: enemy pets and totems') + '</h2></div><div class="prepare"><p>'
    out += t('Sin addon: Esc → Options y busca nameplates. Activa Enemy Nameplates, Enemy Pets, Enemy Totems y Always Show Nameplates si están disponibles. Stacking Nameplates separa las barras. V alterna las placas enemigas con los atajos predeterminados.',
             'Without an addon: Esc → Options and search for nameplates. Enable Enemy Nameplates, Enemy Pets, Enemy Totems and Always Show Nameplates if available. Stacking Nameplates separates the bars. V toggles enemy nameplates with default keybindings.') + '</p><p>'
    out += t('Si las casillas no aparecen, prueba estos ajustes de Blizzard en el chat, uno por uno. Son ajustes de su UI; no se han comprobado directamente en esta beta.',
             'If the checkboxes are missing, try these Blizzard settings in chat, one at a time. These are UI settings; they have not been tested directly in this beta.')
    out += '</p><pre><code>/console nameplateShowEnemies 1\n/console nameplateShowEnemyPets 1\n/console nameplateShowEnemyTotems 1\n/console nameplateShowAll 1\n/console nameplateMotion 1</code></pre><p>'
    out += t('Estas opciones muestran barras, no avisos de voz ni cooldowns. La detección automática de Tremor/Grounding y hechizos enemigos requiere comprobar qué permite la API de Forever. ForeverTotems gestiona los tótems del propio chamán, no los del rival.',
             'These options show bars, not voice alerts or cooldowns. Automatic Tremor/Grounding and enemy spell detection requires checking what the Forever API allows. ForeverTotems manages the shaman’s own totems, not the opponent’s.')
    out += '</p><a href="https://github.com/Resike/BlizzardInterfaceResources/blob/master/Resources/CVars.lua" target="_blank" rel="noopener noreferrer">' + t('Referencia de los ajustes de Blizzard', 'Blizzard settings reference') + '</a></div></section>'
    return out


def install(dist):
    for prefix, en in [('', False), ('en/', True)]:
        path = dist / prefix / 'addons/index.html'
        if en and not path.exists():
            continue  # /en/ aún sin generar (traducción pendiente)
        source = path.read_text(encoding='utf-8')
        if 'id="pvp-addons"' in source:
            continue
        marker = '<div class="divider"><h2>' + ('How to install them' if en else 'Cómo instalarlos') + '</h2></div>'
        if marker not in source:
            # Insert before the shared footer if the existing translation differs.
            marker = '<footer'
        if marker not in source:
            raise ValueError('Addons insertion point missing')
        source = source.replace(marker, section(en) + marker, 1)
        quick = ('<div class="actions"><a class="btn gold" href="#pvp-addons">' +
                 ('PvP addons: duels, DR and nameplates' if en else 'Addons PvP: duelos, DR y placas') +
                 '</a></div>')
        source = source.replace('<a class="featured"', quick + '<a class="featured"', 1)
        path.write_text(source, encoding='utf-8')
