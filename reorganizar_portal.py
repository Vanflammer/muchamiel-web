"""Reorganización para todas las clases (09-10-2026, a petición de Van):
- Lo común sale del Brujo: por qué usar macros, cómo leerlas y crearlas → guía de macros (/comunes/).
- Las macros que repetían las comunes (foco, parar acción, abalorio, venda) y las raciales se quitan de las clases.
- Las frases repetidas de modificadores (Normal/Shift/Alt) se sustituyen por etiquetas cortas en cada macro.
- El Brujo queda con la misma estructura que el resto; lo de Muchamiel va en un recuadro propio.
- Habilidades por nivel para las nueve clases (datos de Talents Forever).
- Las reglas del torneo no se copian: cambian a diario, solo se enlaza el reglamento oficial.
Trabaja sobre web/dist recién restaurado desde web/base-gpt (lo llama comunidad_portal.py)."""
import re, html, json
from pathlib import Path
from crear_portal import dist, classes, root
import oficializar_portal as of

E = html.escape
TFO_RULES = 'https://raider.io/events/the-forever-open/rules-regulations-code-of-conduct'
SPELLS = json.loads((root / 'research' / 'talents.json').read_text(encoding='utf-8'))['spellbooks']
ZAM = 'https://wow.zamimg.com/images/wow/icons/medium/'
REPETIDAS = [r'Normal: enemigo bajo el ratón o tu objetivo\.\s*', r'Shift: foco enemigo vivo, sin alternativa si no hay foco válido\.\s*',
             r'Alt: tú\.\s*', r'Normal: aliado vivo bajo el ratón, aliado seleccionado o tú\.\s*', r'Conserva tu objetivo de daño al usar marcos de grupo\.\s*']
LEGEND = ('<p class="legend">Cada macro lleva sus teclas en etiquetas: <b>Shift</b> = tu foco, <b>ratón</b> = la unidad bajo el cursor, <b>Alt</b> = tú. '
          'La macro de fijar foco y las demás comunes están en la <a href="../comunes/">guía de macros</a>, junto con cómo crearlas.</p>')
# Macros del Brujo que ya están en la guía común (o en la página de su raza): id → destino.
QUITAR_BRUJO = {'C4': '../comunes/#G1', 'C18': '../comunes/#G3', 'C19': '../comunes/#G4', 'C20': '../comunes/#G5',
                'R1': '../razas/undead/', 'R5': '../razas/undead/'}
PRIMERA_PERSONA = [('Empezaría probando', 'Empieza probando'), ('Compararía', 'Compara'), ('empezaría comparando', 'empieza comparando'),
                   ('empezaría con', 'empieza con'), ('Las preferencias son mi valoración de las herramientas disponibles', 'Estas preferencias valoran las herramientas disponibles'),
                   ('Mi primera candidata para el torneo:', 'Primera candidata para el torneo:'), ('No sería mi primera elección.', 'No es la primera opción.'),
                   ('Demonio inicial que compararía', 'Demonio inicial a comparar'), ('Primera build que probaría', 'Primera build a probar'),
                   ('Demonio que probaría', 'Demonio a probar'), ('Build que probaría', 'Build a probar'), ('buscaría', 'busca'), ('valoraría', 'valora')]


def bloque(s, sid):
    m = re.search(r'<details\b[^>]*\bid="' + re.escape(sid) + r'"[^>]*>', s)
    return of.block(s, m.start()) if m else None


def quitar(s, sid):
    b = bloque(s, sid)
    return s[:b[0]] + s[b[1]:] if b else s


def cuerpo(s, sid):
    a, b = bloque(s, sid)
    piece = s[a:b]
    i = piece.index('<div class="section-body">') + len('<div class="section-body">')
    return piece[i:piece.rindex('</div>')]


def etiquetas(code):
    c = html.unescape(code)
    tags = []
    if '/stopcasting' in c: tags.append('Corta tu lanzamiento')
    if '@focus' in c: tags.append('Shift: foco')
    if '@mouseover,help' in c or '@mouseover,exists' in c: tags.append('Ratón: aliado o unidad')
    elif '@mouseover' in c: tags.append('Ratón: enemigo')
    if 'mod:alt,@player' in c: tags.append('Alt: tú')
    elif 'mod:alt' in c: tags.append('Alt: alternativa')
    if 'nochanneling' in c: tags.append('No corta canalizaciones')
    if re.search(r'\[mod:(shift|ctrl)\][^@]', c) and '@focus' not in c: tags.append('Shift/Ctrl: variante')
    if '/petpassive' in c or '/petattack' in c: tags.append('Mascota')
    return ''.join(f'<span>{t}</span>' for t in tags)


def macros_comunes(s):
    """Quita frases repetidas de modificadores y pone etiquetas en cada macro."""
    for pat in REPETIDAS:
        s = re.sub(pat, '', s)
    s = s.replace('<p></p>', '')
    s = re.sub(r'<p class="mtags">.*?</p>', '', s)
    return re.sub(r'(<div class="macro">.*?<code>(.*?)</code>)', lambda m: (f'<p class="mtags">{etiquetas(m[2])}</p>' if etiquetas(m[2]) else '') + m[1], s, flags=re.S)


def niveles(cls):
    sb = SPELLS[cls]
    talents = set(sb.get('talents') or [])
    icons = sb.get('icons') or {}
    rows = sorted((min(v), k, sum(1 for x in v if x <= 30)) for k, v in sb['levels'].items() if v)
    def chip(lvl, name, extra):
        icon = icons.get(name)
        img = f'<img loading="lazy" src="{ZAM}{icon}.jpg" alt="">' if icon else ''
        return f'<span class="spell">{img}<b>{E(name)}</b><small>{extra}</small></span>'
    ya = ''.join(chip(l, n, f'nivel {l}' + (f' · rango {r}' if r > 1 else '') + (' · talento' if n in talents else '')) for l, n, r in rows if l <= 30)
    luego = ''.join(chip(l, n, f'nivel {l}' + (' · talento' if n in talents else '')) for l, n, r in rows if 30 < l <= 60)
    return ('<details class="section" id="nivel"><summary>Habilidades por nivel</summary><div class="section-body">'
            '<p>Lo que tienes a nivel 30 y lo que llega después, según el libro de habilidades de la beta (datos de Talents Forever, 8/10/2026). '
            'Las marcadas como talento solo las tienes si las compras en tu reparto.</p>'
            f'<h3>Disponibles a nivel 30</h3><div class="spells">{ya}</div><h3>Llegan más adelante</h3><div class="spells later">{luego}</div></div></details>')


def clase_comun(s, cls):
    s = macros_comunes(s)
    s = re.sub(r'<p>Crea una macro por bloque en /macro.*?</p>', LEGEND, s, count=1, flags=re.S)
    s = re.sub(r'<p>Sin estas macros tendrías que seleccionar.*?</p>', '', s, flags=re.S)
    s = re.sub(r'<p>La raza del brujo de Muchamiel es Undead\..*?</p>', '<p>Pulsa tu raza para ver sus raciales con su macro. Cada raza tiene las suyas.</p>', s, flags=re.S)
    s = s.replace('<a href="../warlock/#reglas">Reglas y restricciones del torneo</a>', f'<a href="{TFO_RULES}" target="_blank" rel="noopener noreferrer">Reglamento oficial de The Forever Open (cambia a menudo)</a>')
    if 'id="nivel"' not in s:
        a, b = bloque(s, 'raciales')
        s = s[:b] + niveles(cls) + s[b:]
    return s


def brujo(s):
    s = re.sub(r'<summary><span>(.*?)</span><span class="expand">Abrir</span></summary>', r'<summary>\1</summary>', s)
    for a, b in PRIMERA_PERSONA:
        s = s.replace(a, b)
    intro_a = s.index('<section class="intro" id="inicio">')
    intro_b = s.index('</section>', intro_a) + len('</section>')
    intro = s[intro_a:intro_b]
    beneficios = re.search(r'<div class="benefits">.*?</div>(?=<div class="note">)', intro, re.S)[0]
    empezar = re.search(r'<p class="start">Primera prueba sugerida:.*?</p>', intro, re.S)[0].replace('class="start"', '')
    # Quita intro, línea de Undead e índice; deja cabecera como las demás clases + recuadro de Muchamiel.
    fin = s.index('<details', intro_b)
    cabecera = ('<p class="eyebrow">WOW FOREVER · BETA · NIVEL 30</p><div class="class-banner"><img src="../assets/warlock.jpg" alt=""><h1>Brujo</h1></div>'
                '<p>26 puntos: 21 por nivel y 5 extras de Legacy. Cliente en inglés, explicaciones en español. Propuestas para probar en duelos, BGs y mundo abierto; '
                'no son un ranking de victorias ni todas las distribuciones matemáticamente posibles.</p><div class="quick"></div>'
                '<aside class="mm-box" id="muchamiel"><p class="eyebrow">ESPECIAL</p><h2>El brujo de Muchamiel</h2>'
                '<p>Muchamiel juega <strong>Brujo No-muerto</strong> y prepara The Forever Open en directo. Esta guía nació para él: para su preparación propone empezar por '
                '<a href="#B1">B1 · Soul Link + Corruption instantánea</a> y dominar antes <a href="#C1">retirar mascota</a>, <a href="#C3">Fear</a>, '
                '<a href="#C12">Devour Magic</a> y <a href="#D1">Soul Link</a>. Como No-muerto tiene <a href="../razas/undead/">Will of the Forsaken y Cannibalize</a>.</p>'
                '<p><a href="../muchamiel/">Quién es Muchamiel</a> · <a href="../torneo/">The Forever Open</a></p></aside>')
    s = s[:intro_a] + cabecera + s[fin:]
    # Elegir build y variantes, dentro de Builds; las reglas no se copian.
    elegir, variantes = cuerpo(s, 'elegir'), cuerpo(s, 'variantes')
    for sid in ('elegir', 'variantes', 'reglas', 'validacion'):
        s = quitar(s, sid)
    a, b = bloque(s, 'builds')
    piece = s[a:b]
    piece = piece.replace('<div class="section-body">', '<div class="section-body"><h3>Cuál elegir</h3>' + elegir + empezar, 1)
    piece = piece[:piece.rindex('</div>')] + '<h3>Variantes de talentos</h3>' + variantes + '</div></details>'
    s = s[:a] + piece + s[b:]
    # Macros: fuera las comunes y las raciales; enlaces a su nuevo sitio.
    for mid, dest in QUITAR_BRUJO.items():
        s = quitar(s, mid)
        s = s.replace(f'href="#{mid}"', f'href="{dest}"')
    a, b = bloque(s, 'macros')
    piece = s[a:b]
    n = len(re.findall(r'<details id="[A-Z]\d+" class="entry">', piece))
    piece = re.sub(r'<summary>\d+ macros para copiar</summary>', f'<summary>{n} macros para copiar</summary>', piece)
    piece = re.sub(r'(<div class="section-body">)<p>Abre /macro.*?</p>', r'\1' + LEGEND, piece, count=1, flags=re.S)
    s = s[:a] + piece + s[b:]
    s = macros_comunes(s)
    # «Qué mejoran las macros»: los ejemplos propios del brujo.
    inicio = ('<details class="section" id="inicio"><summary>Qué mejoran las macros</summary><div class="section-body">'
              '<p>Ejemplos del brujo; lo general está en la <a href="../comunes/">guía de macros</a>.</p>' + beneficios + '</div></details>')
    a, b = bloque(s, 'fuentes')
    s = s[:a] + inicio + s[a:]
    # Raciales y habilidades por nivel, como el resto.
    races = [r for f in of.DATA['racials'].values() for r in f if 'Warlock' in r['classes']]
    raciales = ('<details class="section" id="raciales"><summary>Raciales disponibles para esta clase</summary><div class="section-body"><div class="quick">'
                + ''.join(f'<a href="../comunes/#race-{of.race_slug(r["race"])}">{E(r["race"])}</a>' for r in races) + '</div>'
                '<p>Pulsa tu raza para ver sus raciales con su macro. Cada raza tiene las suyas.</p></div></details>')
    nota = '<p>Debes haber aprendido las habilidades de tu demonio; tenerlo invocado no basta.</p>'
    a, b = bloque(s, 'nivel')
    s = s[:a] + raciales + niveles('Warlock').replace('</div></details>', nota + '</div></details>', 1)[::1] + s[b:]
    # Reglas: nada copiado; solo enlace al reglamento vigente.
    s = re.sub(r'<a href="#reglas">[^<]*</a>', f'<a href="{TFO_RULES}" target="_blank" rel="noopener noreferrer">reglamento oficial</a>', s)
    s = re.sub(r'<p>Las reglas especiales de The Forever Open \(build fija.*?</p>',
               f'<p>Las reglas de The Forever Open cambian a menudo: consúltalas siempre en el <a href="{TFO_RULES}" target="_blank" rel="noopener noreferrer">reglamento oficial</a>. No se aplican a BGs ni al mundo abierto.</p>', s, flags=re.S)
    # Pie igual que el resto de clases.
    pie = (dist / 'mage' / 'index.html').read_text(encoding='utf-8')
    pie = pie[pie.index('<footer'):pie.index('</footer>') + 9]
    s = re.sub(r'<footer>.*?</footer>', pie, s, count=1, flags=re.S)
    return s


GUIA = '''<details class="section" id="por-que" open><summary>Por qué importan las macros</summary><div class="section-body">
<p>En PvP cada cambio de objetivo y cada clic cuestan atención. Una macro junta varias órdenes en una tecla y te deja elegir a quién va dirigido el hechizo: el enemigo bajo el ratón, tu foco o tú. Reaccionas con menos pasos y cometes menos errores mientras te mueves y vigilas al rival.</p>
<div class="benefits">
<article><h3>Controlar sin perder el objetivo</h3><p>Interrumpe, controla o disipa a tu foco o al enemigo bajo el ratón sin soltar a tu objetivo de daño. Te ahorras seleccionar, lanzar y volver a seleccionar.</p></article>
<article><h3>Curar sin soltar al enemigo</h3><p>Con el ratón sobre los marcos de grupo curas a un aliado sin cambiar de objetivo; con Alt te curas a ti.</p></article>
<article><h3>Reaccionar a tiempo</h3><p>Las macros de control empiezan cortando lo que estés lanzando, así el control sale en cuanto pulsas.</p></article>
<article><h3>No cortar canalizaciones</h3><p>Las de drenajes y canalizaciones no se reinician si vuelves a pulsar sin querer.</p></article>
</div></div></details>
<details class="section" id="esperar"><summary>Qué esperar de ellas</summary><div class="section-body">
<p>No aumentan el daño por sí solas ni deciden por ti. No eliminan el tiempo global de reutilización, el alcance, el maná ni los requisitos de talentos. Algunas cortan lanzamientos o tienen condiciones concretas: lee la explicación de cada una y ensáyalas antes de competir. Están comprobadas en longitud (255 caracteres), no dentro del cliente.</p></div></details>
<details class="section" id="teclas"><summary>Cómo leer cada macro</summary><div class="section-body">
<p>Todas las macros de la guía siguen el mismo patrón, así que en cada una solo verás unas etiquetas cortas:</p>
<table class="keys"><tr><th>Normal</th><td>El enemigo bajo el ratón o, si no hay, tu objetivo.</td></tr><tr><th>Shift</th><td>Tu foco. Si no hay un foco enemigo vivo, no hace nada.</td></tr><tr><th>Alt</th><td>Tú mismo, en curas y disipaciones.</td></tr><tr><th>Ratón sobre un marco</th><td>El aliado de ese marco, sin cambiar tu objetivo de daño.</td></tr></table>
<p>Para que Shift funcione necesitas un foco: usa la macro común <a href="#G1">Fijar foco / Alt borrar</a>.</p></div></details>
<details class="section" id="crear"><summary>Cómo crear una macro</summary><div class="section-body"><ol>
<li>Escribe <code>/macro</code> en el chat (o Esc → Macros) y pulsa <b>Nueva</b>.</li>
<li>Ponle un nombre y elige el icono <b>?</b>: con <code>#showtooltip</code> mostrará el del hechizo.</li>
<li>Pega el texto con «Copiar macro» y arrástrala a tu barra.</li>
<li>Revisa en Opciones → Atajos que Shift, Ctrl y Alt no tengan otra acción asignada en esas teclas.</li>
<li>El cliente está en inglés: no traduzcas los nombres de los hechizos.</li></ol></div></details>'''


def guia(s):
    s = s.replace('<p class="eyebrow">WOW FOREVER · PARA TODAS LAS CLASES</p><h1>Macros comunes y raciales</h1>', '<p class="eyebrow">WOW FOREVER · PARA TODAS LAS CLASES</p><h1>Guía de macros</h1>')
    s = s.replace('<summary>Cinco macros comunes</summary>', '<summary>Macros comunes para todas las clases</summary>')
    s = re.sub(r'<details class="section" id="comunes" open>', '<details class="section" id="comunes">', s)
    i = s.index('<details class="section" id="comunes"')
    s = s[:i] + GUIA + s[i:]
    return macros_comunes(s)


CLASE_ES = {cls: name for slug, name, cls, *_ in classes}


def raza_es(race):
    return race if race.startswith('Skyborne') else of.RACE_ES[race]


def doble(es, en):
    """Castellano grande + nombre del juego (inglés) pequeño, como en las fichas."""
    return E(es) if es == en or en.startswith(es) else f'{E(es)} <small class="en">{E(en)}</small>'


def castellano(s, file):
    """Clases y razas en castellano con el nombre en inglés del juego en pequeño (la beta está en inglés)."""
    rel = file.relative_to(dist).parts
    s = re.sub(r'Clases: ((?:[A-Z][a-z]+(?:, )?)+)\.', lambda m: 'Clases: ' + ', '.join(CLASE_ES.get(c.strip(), c.strip()) for c in m[1].split(',')) + '.', s)
    s = re.sub(r'(<summary>DU\d+ · )([A-Z][a-z]+)(</summary>)', lambda m: m[1] + doble(CLASE_ES.get(m[2], m[2]), m[2]) + m[3], s)
    s = s.replace('<summary>Horde · raciales de Forever</summary>', '<summary>Horda · raciales de Forever</summary>').replace('<summary>Alliance · raciales de Forever</summary>', '<summary>Alianza · raciales de Forever</summary>')
    s = re.sub(r'(<details class="entry" id="race-([a-z-]+)"><summary>(?:<img[^>]*>)?)([^<]+)(</summary>)',
               lambda m: m[1] + doble(raza_es(of.RACES[m[2]]['race']), of.RACES[m[2]]['race']) + m[4], s)
    if len(rel) == 3 and rel[0] == 'razas':
        r = of.RACES[rel[1]]['race']
        s = s.replace(f'<h1>{E(r)}</h1>', f'<h1>{doble(raza_es(r), r)}</h1>', 1)
        s = s.replace(f'<span>{E(r)}</span></nav>', f'<span>{E(raza_es(r))}</span></nav>', 1)
    return s


def run():
    for slug, name, cls, *_ in classes:
        f = dist / slug / 'index.html'
        s = f.read_text(encoding='utf-8')
        if slug == 'warlock':
            continue
        f.write_text(clase_comun(s, cls), encoding='utf-8')
    f = dist / 'warlock' / 'index.html'
    f.write_text(brujo(f.read_text(encoding='utf-8')), encoding='utf-8')
    f = dist / 'comunes' / 'index.html'
    f.write_text(guia(f.read_text(encoding='utf-8')), encoding='utf-8')
    for f in (dist / 'razas').rglob('index.html'):
        f.write_text(macros_comunes(f.read_text(encoding='utf-8')), encoding='utf-8')
