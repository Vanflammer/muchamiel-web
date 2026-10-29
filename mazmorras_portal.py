"""Una página por mazmorra de WoW Forever (Van, 16-10-2026: «cada una con su página, de qué va y los ítems que dan»).
Datos en research/mazmorras.json (los reúnen agentes con fuentes: Blizzard, Wowhead, Icy Veins, Warcraft Tavern, warcraft.wiki.gg).
Lo que no se sabe (jefes y botín de algunas nuevas) no se inventa: la página lo dice. Se llama desde comunidad_portal.build_pages()."""
from pathlib import Path
from urllib.parse import urlparse
import html, json, re
from crear_portal import dist

E = html.escape
DATOS = Path(__file__).parent / 'research' / 'mazmorras.json'
ICONO = 'https://wow.zamimg.com/images/wow/icons/large/{}.jpg'
BOTIN = Path(__file__).parent / 'research' / 'mazmorras-botin.json'  # Van 16-10: botín completo por jefe (estilo AtlasLoot)
MAPAS = Path(__file__).parent / 'research' / 'mazmorras-mapas.json'  # Van 16-10: zona y coordenadas de la entrada
MAPA = 'https://wow.zamimg.com/images/wow/classic/maps/enus/{}/{}.jpg'  # mapas de zona de Classic (Wowhead), zoom = 772x515, original = 1002x668
NOTAS_BETA = 'https://us.forums.blizzard.com/en/wow/t/2360696'  # hilo oficial de notas de la beta (las copias locales de research/notas-beta)
FACCION = {'Alianza': 'fac-ali', 'Horda': 'fac-hor'}


def nivel_min(n):
    return int(re.match(r'\d+', n)[0]) if re.match(r'\d+', n or '') else 99


def cargar():
    """Las mazmorras con datos, ordenadas por nivel."""
    out = [m for m in json.loads(DATOS.read_text(encoding='utf-8')) if m.get('slug') and m.get('es')]
    return sorted(out, key=lambda m: (nivel_min(m.get('nivel')), m['es']))


def mapas():
    try:
        return {m['slug']: m for m in json.loads(MAPAS.read_text(encoding='utf-8'))}
    except Exception:
        return {}


def botines():
    try:
        return json.loads(BOTIN.read_text(encoding='utf-8'))
    except Exception:
        return {}


def objeto(o):
    ico = ICONO.format(o['icono']) if o.get('icono') else ICONO.format('inv_misc_questionmark')
    return (f'<a class="m-it q{o.get("calidad") or 2}" href="{E(o["url"], quote=True)}" target="_blank" rel="noopener noreferrer">'
            f'<img src="{ico}" alt="" loading="lazy"><span>{E(o["nombre"])}</span></a>')


def jefes_con_botin(m, b):
    # Cada jefe en su tarjeta con todo lo que suelta al lado (Van 16-10: «como el Atlas»).
    notas = {j['nombre']: j.get('nota') for j in (m.get('jefes') or [])}
    por_jefe = {j['nombre']: j.get('objetos') or [] for j in b.get('jefes') or []}
    orden = [j['nombre'] for j in (m.get('jefes') or [])] + [n for n in por_jefe if n not in notas]
    s = '<div class="m-jefes2">'
    for k, n in enumerate(orden, 1):
        objs = por_jefe.get(n) or []
        extra = n == 'Botín de la mazmorra'
        s += (f'<section class="m-jefe"><h3>' + ('' if extra else f'<span class="m-num">{k}</span>') + f'{E(n)}</h3>'
              + (f'<p>{E(notas[n])}</p>' if notas.get(n) else '')
              + ('<div class="m-loot">' + ''.join(objeto(o) for o in objs) + '</div>' if objs else '') + '</section>')
    s += '</div>'
    if b.get('origen') == 'classic':
        s += '<p class="fine">Botín de WoW Classic (datos del addon AtlasLoot Classic): Blizzard ha renovado el botín de las mazmorras clásicas en Forever y puede cambiar.</p>'
    s += '<p class="fine">Pasa el ratón por un objeto para ver su ficha; púlsalo para abrirlo en Wowhead.</p>'
    return s


def mapa(g):
    # Mapa de la zona con la entrada marcada; al pulsarlo se abre en grande con zoom (JS de abajo).
    if not g or not g.get('area_id'):
        return ''
    pin = f'<span class="m-pin" style="left:{g["x"]}%;top:{g["y"]}%"></span>' if g.get('x') is not None and g.get('y') is not None else ''
    pie = (f'Entrada en {E(g.get("zona_en") or "")} ({g["x"]:.1f}, {g["y"]:.1f}).' if pin else f'{E(g.get("zona_en") or "")}: la entrada exacta aún no se ha publicado.')
    return (f'<figure class="m-mapa"><button type="button" class="m-mapa-btn" data-src="{MAPA.format("original", g["area_id"])}" aria-label="Ampliar el mapa">'
            f'<img src="{MAPA.format("zoom", g["area_id"])}" alt="" loading="lazy" width="772" height="515">{pin}<span class="m-lupa">⤢</span></button>'
            f'<figcaption>{pie} Pulsa el mapa para verlo en grande.</figcaption></figure>')


def menu(base):
    # Submenú «Mazmorras» del menú WoW Forever: (enlace, nombre, icono, color).
    return [(base + 'mazmorras/' + m['slug'] + '/', m['es'], '', '') for m in cargar()]


def fuente(u):
    host = urlparse(u).netloc.replace('www.', '')
    return f'<a href="{E(u, quote=True)}" target="_blank" rel="noopener noreferrer">{E(host)}</a>'


def pagina(m, todas, geo=None, bot=None):
    i = next(k for k, x in enumerate(todas) if x['slug'] == m['slug'])
    jefes = m.get('jefes') or []
    botin = m.get('botin') or []
    misiones = m.get('misiones') or []
    s = ('<p class="eyebrow">MAZMORRA · NIVEL ' + E(m.get('nivel') or '') + '</p>'
         f'<h1>{E(m["es"])} <small class="en">{E(m.get("en") or "")}</small></h1>'
         + ('<p class="m-nueva">★ Nueva en WoW Forever</p>' if m.get('nueva') else '')
         + f'<p class="lead">{E(m.get("resumen") or "")}</p>'
         '<div class="tfo-stats m-fichas">'
         f'<div><b>{E(m.get("nivel") or "?")}</b><span>nivel recomendado</span></div>'
         f'<div><b>{E(str(m["nivel_min"])) if m.get("nivel_min") else "?"}</b><span>nivel mínimo</span></div>'
         f'<div><b>{len(jefes) if jefes else "?"}</b><span>jefes</span></div>'
         f'<div><b class="m-zona">{E(m.get("zona") or "?")}</b><span>zona</span></div></div>')
    if m.get('acceso'):
        s += f'<div class="divider"><h2>Cómo llegar</h2></div><p>{E(m["acceso"])}</p>' + mapa(geo)
    if m.get('cambios_forever'):
        s += f'<div class="divider"><h2>Qué cambia en Forever</h2></div><p>{E(m["cambios_forever"])}</p>'
    s += '<div class="divider"><h2>Jefes y botín</h2></div>' if bot and any(j.get('objetos') for j in bot.get('jefes') or []) else '<div class="divider"><h2>Jefes</h2></div>'
    if bot and any(j.get('objetos') for j in bot.get('jefes') or []):
        s += jefes_con_botin(m, bot)
    elif jefes:
        s += '<ol class="m-jefes">' + ''.join(f'<li><b>{E(j["nombre"])}</b>' + (f'<span>{E(j["nota"])}</span>' if j.get('nota') else '') + '</li>' for j in jefes) + '</ol>'
    else:
        s += '<p class="m-aviso">Blizzard todavía no ha publicado sus jefes. Los pondremos en cuanto se sepan.</p>'
    s += '<div class="divider"><h2>Botín destacado</h2></div>'
    if botin:
        s += '<div class="m-botin">'
        for b in botin:
            href = b.get('wowhead') or (f'https://www.wowhead.com/forever/item={b["id"]}' if b.get('id') else '')
            ico = ICONO.format(b['icono']) if b.get('icono') else ICONO.format('inv_misc_questionmark')
            q = b.get('calidad') or 2
            dentro = (f'<img src="{ico}" alt="" loading="lazy"><span><b class="q{q}">{E(b["nombre"])}</b>'
                      f'<small>{E(b.get("tipo") or "")}' + (f' · {E(b["para"])}' if b.get('para') else '') + '</small>'
                      + (f'<small class="m-de">{E(b["jefe"])}</small>' if b.get('jefe') else '') + '</span>')
            s += (f'<a class="m-obj" href="{E(href, quote=True)}" target="_blank" rel="noopener noreferrer">{dentro}</a>' if href
                  else f'<div class="m-obj">{dentro}</div>')
        s += '</div><p class="fine">Pulsa un objeto para ver su ficha completa en Wowhead.</p>'
    else:
        s += '<p class="m-aviso">El botín de esta mazmorra aún no se ha publicado. Lo añadiremos en cuanto Blizzard lo enseñe.</p>'
    if misiones:
        s += ('<div class="divider"><h2>Misiones</h2></div><table class="keys m-mis"><tr><th>Misión</th><td><strong>Facción</strong></td><td><strong>Dónde se recoge</strong></td></tr>'
              + ''.join(f'<tr><th>{E(x["nombre"])}</th><td><span class="{FACCION.get(x.get("faccion"), "fac-amb")}">{E(x.get("faccion") or "")}</span></td><td>{E(x.get("donde") or "")}</td></tr>' for x in misiones)
              + '</table>')
    if m.get('consejos'):
        s += '<div class="divider"><h2>Consejos</h2></div><ul class="m-consejos">' + ''.join(f'<li>{E(c)}</li>' for c in m['consejos']) + '</ul>'
    ant, sig = (todas[i - 1] if i else None), (todas[i + 1] if i + 1 < len(todas) else None)
    s += ('<div class="m-nav">' + (f'<a class="btn ghost" href="../{ant["slug"]}/">← {E(ant["es"])}</a>' if ant else '<span></span>')
          + '<a class="btn gold" href="../">Todas las mazmorras</a>'
          + (f'<a class="btn ghost" href="../{sig["slug"]}/">{E(sig["es"])} →</a>' if sig else '<span></span>') + '</div>')
    if m.get('fuentes'):
        s += '<p class="fine">Fuentes: ' + ' · '.join(dict.fromkeys(fuente(u if u.startswith('http') else NOTAS_BETA) for u in m['fuentes'])) + '. Datos de la beta de WoW Forever: pueden cambiar hasta el lanzamiento.</p>'
    return s


CSS = '''
.m-nueva{display:inline-block;margin:0 0 14px;padding:4px 12px;border:1px solid #c99a3c;border-radius:999px;color:#ffe7a6;font-weight:700;font-size:13px;letter-spacing:.06em}
.m-fichas .m-zona{font-size:17px;line-height:1.3}
.m-jefes{margin:0;padding-left:26px;display:flex;flex-direction:column;gap:8px}.m-jefes li{padding-left:4px}.m-jefes b{color:#ffe7a6}.m-jefes span{display:block;color:#c3ccdb;font-size:14.5px}
.m-botin{display:flex;flex-wrap:wrap;justify-content:center;gap:10px}.m-botin>.m-obj{flex:0 1 calc(33.333% - 7px);min-width:250px;box-sizing:border-box}
.m-obj{display:flex;gap:12px;align-items:flex-start;padding:12px;border:1px solid #2c3444;border-radius:8px;background:#0f141d;text-decoration:none;color:inherit;transition:border-color .2s,box-shadow .2s}
a.m-obj:hover{border-color:#c99a3c;box-shadow:0 0 14px #e8b84a33}
.m-obj img{width:40px;height:40px;border-radius:5px;border:1px solid #000;box-shadow:0 0 0 1px #f3c76a44;flex:none}
.m-obj b{display:block;font-size:15px}.m-obj small{display:block;color:#aeb8c8;font-size:13px}.m-obj .m-de{color:#8994a7}
.q2{color:#1eff00}.q3{color:#4a9eff}.q4{color:#c27bff}.q5{color:#ff8000}
.m-mis td{font-size:14px}.fac-ali{color:#5aa2ff;font-weight:700}.fac-hor{color:#e2564a;font-weight:700}.fac-amb{color:#ffe7a6;font-weight:700}
.m-consejos{display:flex;flex-direction:column;gap:6px}
.m-aviso{padding:14px 16px;border:1px dashed #c99a3c88;border-radius:8px;color:#e6dcc4;text-align:center}
.m-nav{display:grid;grid-template-columns:1fr auto 1fr;gap:10px;align-items:center;margin:30px 0 10px}.m-nav>:first-child{justify-self:start}.m-nav>:last-child{justify-self:end}
@media(max-width:700px){.m-nav{grid-template-columns:1fr}.m-nav>*{justify-self:center!important}}
table.zonas td a{color:#ffe7a6}
.m-jefes2{display:flex;flex-direction:column;gap:12px}.m-jefe{padding:14px 16px;border:1px solid #2c3444;border-left:3px solid #c99a3c;border-radius:8px;background:#0f141d}
.m-jefe h3{margin:0 0 4px;display:flex;align-items:center;gap:10px;color:#ffe7a6;font-size:18px}.m-jefe p{margin:0 0 8px;color:#c3ccdb;font-size:14.5px}
.m-num{display:inline-flex;align-items:center;justify-content:center;min-width:28px;height:28px;border-radius:50%;background:#c99a3c;color:#120c02;font:800 14px/1 sans-serif}
.m-loot{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:6px}
.m-it{display:flex;align-items:center;gap:8px;padding:5px 8px;border-radius:6px;background:#141b28;text-decoration:none;font-size:14px;line-height:1.25}.m-it:hover{background:#1d2638}
.m-it img{width:28px;height:28px;border-radius:4px;border:1px solid #000;flex:none}.m-it.q2 span{color:#1eff00}.m-it.q3 span{color:#4a9eff}.m-it.q4 span{color:#c27bff}.m-it.q5 span{color:#ff8000}.m-it.q1 span{color:#fff}
.m-mapa{margin:14px auto 6px;max-width:772px}.m-mapa figcaption{text-align:center;color:#aeb8c8;font-size:13.5px;margin-top:6px}
.m-mapa-btn{position:relative;display:block;width:100%;padding:0;border:2px solid #c99a3c;border-radius:8px;overflow:hidden;cursor:zoom-in;background:#000;line-height:0}
.m-mapa-btn img{width:100%;height:auto;display:block}
.m-pin{position:absolute;width:22px;height:22px;margin:-11px 0 0 -11px;border-radius:50%;background:#ff3b30;border:3px solid #fff;box-shadow:0 0 0 3px #0008,0 0 14px #ff3b30;animation:mpin 1.6s infinite}
@keyframes mpin{0%,100%{transform:scale(1)}50%{transform:scale(1.25)}}
.m-lupa{position:absolute;right:8px;bottom:8px;padding:4px 9px;border-radius:6px;background:#000b;color:#ffe7a6;font:700 16px/1.2 sans-serif}
.m-lb{position:fixed;inset:0;z-index:100;background:#000e;display:flex;flex-direction:column}
.m-lb-bar{display:flex;justify-content:center;gap:8px;padding:10px}.m-lb-bar button{min-width:44px;height:40px;border:1px solid #c99a3c;border-radius:6px;background:#1a2132;color:#ffe7a6;font:700 20px/1 sans-serif;cursor:pointer}
.m-lb-in{flex:1;overflow:auto;cursor:grab;touch-action:pan-x pan-y pinch-zoom}.m-lb-in.arr{cursor:grabbing}
.m-lb-map{position:relative;margin:0 auto;line-height:0}.m-lb-map img{width:100%;height:auto;display:block;user-select:none;-webkit-user-drag:none}
'''


# Visor del mapa en grande: + y − (o la rueda), arrastrar para moverse, Esc o ✕ para cerrar.
VISOR = """<script>(function(){var z=1;function cerrar(o){o.remove();document.body.style.overflow=''}
document.addEventListener('click',function(e){var b=e.target.closest('.m-mapa-btn');if(!b)return;var p=b.querySelector('.m-pin'),o=document.createElement('div');o.className='m-lb';
o.innerHTML='<div class="m-lb-bar"><button type="button" data-z="-1" aria-label="Alejar">−</button><button type="button" data-z="1" aria-label="Acercar">+</button><button type="button" data-c aria-label="Cerrar">✕</button></div><div class="m-lb-in"><div class="m-lb-map"><img alt="" src="'+b.dataset.src+'">'+(p?p.outerHTML:'')+'</div></div>';
document.body.appendChild(o);document.body.style.overflow='hidden';z=1;var m=o.querySelector('.m-lb-map'),i=o.querySelector('.m-lb-in');
function zoom(d){var cx=(i.scrollLeft+i.clientWidth/2)/m.offsetWidth,cy=(i.scrollTop+i.clientHeight/2)/m.offsetHeight;z=Math.min(4,Math.max(1,z+d*0.5));m.style.width=(z*100)+'%';i.scrollLeft=cx*m.offsetWidth-i.clientWidth/2;i.scrollTop=cy*m.offsetHeight-i.clientHeight/2}
m.style.width='100%';m.style.maxWidth='none';
o.addEventListener('click',function(ev){var t=ev.target;if(t.dataset.z)zoom(+t.dataset.z);else if(t.hasAttribute('data-c')||t===i)cerrar(o)});
i.addEventListener('wheel',function(ev){ev.preventDefault();zoom(ev.deltaY<0?1:-1)},{passive:false});
var ar=null;i.addEventListener('mousedown',function(ev){ar=[ev.clientX,ev.clientY,i.scrollLeft,i.scrollTop];i.classList.add('arr');ev.preventDefault()});
window.addEventListener('mousemove',function(ev){if(ar){i.scrollLeft=ar[2]-(ev.clientX-ar[0]);i.scrollTop=ar[3]-(ev.clientY-ar[1])}});
window.addEventListener('mouseup',function(){ar=null;i.classList.remove('arr')});
document.addEventListener('keydown',function k(ev){if(ev.key==='Escape'){cerrar(o);document.removeEventListener('keydown',k)}})})})();</script>"""


# Fichas de Wowhead al pasar el ratón por un objeto (su script público; reconoce los enlaces /forever/ y /classic/).
TOOLTIPS = '<script>const whTooltips={colorLinks:false,iconizeLinks:false,renameLinks:false};</script><script src="https://wow.zamimg.com/js/tooltips.js" defer></script>'


def build():
    todas = cargar()
    tpl = (dist / 'comunes' / 'index.html').read_text(encoding='utf-8')
    head = tpl[:tpl.index('<body')].replace('</head>', '<style>' + CSS + '</style></head>', 1)
    foot = tpl[tpl.index('<footer'):tpl.index('</footer>') + 9]
    geo, bots = mapas(), botines()
    for m in todas:
        h = re.sub(r'<title>.*?</title>', f'<title>{E(m["es"])} ({E(m.get("en") or "")}) en WoW Forever: jefes, botín y misiones | Muchamiel</title>', head, count=1, flags=re.S)
        h = re.sub(r'<meta name="description" content="[^"]*">',
                   f'<meta name="description" content="{E(m["es"])} en WoW Forever, nivel {E(m.get("nivel") or "")}: de qué va, cómo llegar, jefes, botín destacado, misiones y consejos.">', h, count=1)
        d = dist / 'mazmorras' / m['slug']
        d.mkdir(parents=True, exist_ok=True)
        (d / 'index.html').write_text(h + '<body><header></header><main>' + pagina(m, todas, geo.get(m['slug']), bots.get(m['slug'])) + foot + '</main>' + VISOR + TOOLTIPS + '</body></html>', encoding='utf-8')
    return {m['es']: m['slug'] for m in todas}
