"""Macros ordenadas (Van, 15-10-2026): «las macros son un puto caos». Una portada de macros (/comunes/) donde se elige la clase,
con las comunes a todas y las raciales de Horda y Alianza, y una página por clase (/macros/<clase>/) con todas sus macros en
tarjetas: qué hace, teclas, código con botón de copiar y contador de caracteres, buscador e índice. Ideas de Icy Veins, Zockify,
Warcraft Tavern, Kami-labs y RankedBoost (estudio del 15-10). Las macros salen de las guías de clase (GPT + MACROS_EXTRA):
aquí solo se mueven y se presentan; en cada guía queda un botón a su página."""
import html
import re

from crear_portal import dist, classes
import oficializar_portal as of

E = html.escape


def entries(sec):
    """Bloques <details class="entry"> de primer nivel dentro de una sección."""
    out, i = [], 0
    body = sec[sec.index('<div class="section-body">'):]
    while True:
        m = re.search(r'<details\b[^>]*\bclass="entry"[^>]*>', body[i:])
        if not m:
            return out
        a, b = of.block(body, i + m.start())
        out.append(body[a:b])
        i = b


def card(e):
    """Tarjeta de una macro: título (con su código, p. ej. C7, si lo lleva), explicación, teclas y código con copiar y longitud."""
    mid = re.search(r'\bid="([^"]+)"', e)[1]
    title = re.search(r'<summary>(.*?)</summary>', e, re.S)[1]
    badge = ''
    m = re.match(r'([A-Z]\d+) · (.*)', title, re.S)
    if m:
        badge, title = f'<span class="mid">{m[1]}</span>', m[2]
    inner = e[e.index('<div class="detail-body">') + len('<div class="detail-body">'):e.rindex('</div></details>')]
    inner = re.sub(r'<a class="permalink"[^>]*>.*?</a>', '', inner, count=1, flags=re.S)

    def largo(m):
        n = len(html.unescape(m[2]))
        return m[1] + f'<span class="mlen{" over" if n > 255 else ""}">{n}/255</span>' + m[0][len(m[1]):]
    inner = re.sub(r'(<div class="macro">)(?:<button[^>]*>[^<]*</button>)?<pre><code>(.*?)</code></pre>', largo, inner, flags=re.S)
    return (f'<article class="mcard" id="{mid}"><div class="mhead">{badge}<h3>{title}</h3>'
            f'<a class="mlink" href="#{mid}" aria-label="Enlace a esta macro" title="Enlace a esta macro">#</a></div>{inner}</article>')


def switch(base, actual=None):
    return '<nav class="mswitch" aria-label="Clases">' + ''.join(
        f'<a href="{base}macros/{slug}/" style="--cc:{color}"' + (' class="on" aria-current="page"' if slug == actual else '') +
        f'><img src="{base}assets/{slug}.jpg" alt="">{name}</a>' for slug, name, _k, color, _d in classes) + '</nav>'


BUSCADOR = ('<div class="mtools"><input type="search" class="msearch" placeholder="Busca por hechizo o nombre (Polymorph, foco, sigilo…)" aria-label="Buscar macro">'
            '<span class="mcount" aria-live="polite"></span></div><p class="mempty" hidden>No hay macros con eso</p>')
JS = r'''<script>(function(){var q=document.querySelector('.msearch');if(!q)return;var cards=[].slice.call(document.querySelectorAll('.mcard')),out=document.querySelector('.mcount'),empty=document.querySelector('.mempty');
function norm(s){return s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'')}
var texts=cards.map(function(c){return norm(c.textContent)});
function f(){var words=norm(q.value.trim()).split(/\s+/).filter(Boolean),n=0;cards.forEach(function(c,i){var ok=words.every(function(w){return texts[i].indexOf(w)>=0});c.hidden=!ok;if(ok)n++});out.textContent=words.length?n+' / '+cards.length:'';empty.hidden=!words.length||n>0}
q.addEventListener('input',f);q.addEventListener('keydown',function(e){if(e.key==='Escape'){q.value='';f()}})})();</script>'''
BUSCADOR_CSS = '''.mtools{width:100%}.msearch{min-width:0;box-sizing:border-box}
.mcount{text-align:center;white-space:nowrap}.mempty{text-align:center;color:#a99a7c}
@media(max-width:420px){.mtools{flex-direction:column}.msearch{flex:none;width:100%}.mcount{min-width:0}}
'''
LEYENDA = ('<p class="mleyenda"><span><b>Normal</b> enemigo bajo el ratón o tu objetivo</span><span><b>Shift</b> tu foco</span>'
           '<span><b>Alt</b> tú mismo</span><span><b>/255</b> largo máximo de una macro</span></p>')


def build():
    tpl = (dist / 'comunes' / 'index.html').read_text(encoding='utf-8')
    head = tpl[:tpl.index('<body')]
    foot = tpl[tpl.index('<footer'):tpl.index('</footer>') + 9]
    script = re.search(r'<script>function reveal\(\).*?</script>', tpl, re.S)[0]  # copiar macro y abrir el ancla
    (dist / 'macros').mkdir(exist_ok=True)
    cuantas, movidas = {}, {}
    for slug, name, _k, color, _d in classes:
        f = dist / slug / 'index.html'
        s = f.read_text(encoding='utf-8')
        a, b = of.block(s, re.search(r'<details[^>]*\bid="macros"[^>]*>', s).start())
        lista = entries(s[a:b])
        cuantas[slug] = len(lista)
        ids = [re.search(r'\bid="([^"]+)"', e)[1] for e in lista]
        movidas[slug] = set(ids)
        body = (f'<div class="mpage" style="--cc:{color}"><p class="eyebrow">WOW FOREVER · MACROS</p>'
                f'<h1><img class="mface" src="../../assets/{slug}.jpg" alt="">Macros de {name}</h1>'
                f'<p class="lead">{len(lista)} macros para copiar y pegar en el juego, con lo que hace cada una y las teclas que usa. '
                f'Las comunes a todas las clases y las de tu raza están en <a href="../../comunes/">la portada de macros</a>.</p>'
                + switch('../../', slug) + BUSCADOR + LEYENDA +
                '<div class="mgrid">' + ''.join(card(e) for e in lista) + '</div>'
                '<div class="mfin"><a class="btn gold" href="../../comunes/">Macros comunes y raciales</a>'
                f'<a class="btn ghost" href="../../{slug}/">Guía del {name}</a>'
                '<a class="btn ghost" href="../../comunes/#crear">Cómo crear una macro</a></div></div>')
        # Enlaces a otras partes de la guía (builds, otras secciones): a la guía de la clase.
        body = re.sub(r'href="#([^"]+)"', lambda m: m[0] if m[1] in ids else f'href="../../{slug}/#{m[1]}"', body)
        import macros_limpieza  # Van 30-10: sin builds de la beta ni nivel 30 en las notas
        body = macros_limpieza.aplicar(body)
        h = re.sub(r'<title>.*?</title>', f'<title>Macros de {E(name)} para WoW Forever: copiar y pegar | Muchamiel</title>', head, count=1, flags=re.S)
        h = h.replace('</style>', BUSCADOR_CSS + '</style>', 1)
        h = re.sub(r'<meta name="description" content="[^"]*">',
                   f'<meta name="description" content="Las {len(lista)} macros de {E(name)} para WoW Forever, listas para copiar: foco, ratón, control y PvP, con lo que hace cada una.">', h, count=1)
        (dist / 'macros' / slug).mkdir(exist_ok=True)
        (dist / 'macros' / slug / 'index.html').write_text(h + '<body><header></header><main>' + body + foot + '</main>' + script + JS + '</body></html>', encoding='utf-8')
        # En la guía de la clase, la sección queda como un botón a su página.
        sec = s[a:b]
        nuevo = (sec[:sec.index('<div class="section-body">')] + '<div class="section-body"><div class="mlleva">'
                 f'<p>Las {len(lista)} macros del {name} tienen su propia página: tarjetas con lo que hace cada una, botón de copiar y buscador.</p>'
                 f'<a class="btn gold" href="../macros/{slug}/">Ver las macros del {name}</a></div></div></details>')
        s = s[:a] + nuevo + s[b:]
        s = re.sub(r'href="#([A-Za-z]+\d+)"', lambda m: f'href="../macros/{slug}/#{m[1]}"' if m[1] in movidas[slug] else m[0], s)
        f.write_text(s, encoding='utf-8')
    # Enlaces de otras páginas a una macro de una guía → a su nueva página.
    for f in dist.rglob('*.html'):
        if f.relative_to(dist).parts[0] == 'macros':
            continue
        s = f.read_text(encoding='utf-8')
        n = re.sub(r'href="((?:\.\./)*)(\w+)/#([A-Za-z]+\d+)"',
                   lambda m: f'href="{m[1]}macros/{m[2]}/#{m[3]}"' if m[3] in movidas.get(m[2], ()) else m[0], s)
        if n != s:
            f.write_text(n, encoding='utf-8')
    portada(cuantas)


def portada(cuantas):
    """/comunes/: elegir clase, luego las comunes a todas y las raciales; la ayuda para crear macros, al final."""
    f = dist / 'comunes' / 'index.html'
    s = f.read_text(encoding='utf-8')
    secciones = {}
    for m in list(re.finditer(r'<details class="section"[^>]*\bid="([^"]+)"', s)):
        a, b = of.block(s, m.start())
        secciones[m[1]] = s[a:b]
    primera = min(s.index(x) for x in secciones.values())
    ultima = max(s.index(x) + len(x) for x in secciones.values())
    clases = '<div class="mclases">' + ''.join(
        f'<a class="mclase" href="../macros/{slug}/" style="--cc:{color}"><img src="../assets/{slug}.jpg" alt=""><b>{name}</b><small>{cuantas[slug]} macros</small></a>'
        for slug, name, _k, color, _d in classes) + '</div>'
    comunes = secciones['comunes']
    lista = entries(comunes)
    comunes = (comunes[:comunes.index('<div class="section-body">')].replace('<details class="section"', '<details open class="section"', 1)
               + '<div class="section-body">' + BUSCADOR.replace('Busca por hechizo o nombre (Polymorph, foco, sigilo…)', 'Busca entre las comunes (foco, abalorios, vendas…)')
               + '<div class="mgrid">' + ''.join(card(e) for e in lista) + '</div></div></details>')
    raciales = ''.join(secciones[k].replace('<details class="section"', '<details open class="section"', 1) for k in ('horde', 'alliance'))
    ayuda = ''.join(secciones[k] for k in ('por-que', 'esperar', 'teclas', 'crear') if k in secciones)
    medio = ('<div class="divider"><h2>Elige tu clase</h2></div>' + clases + LEYENDA + comunes + raciales +
             '<div class="divider"><h2>Si es tu primera vez con macros</h2></div>' + ayuda)
    s = s[:primera] + medio + s[ultima:]
    s = re.sub(r'<p class="eyebrow">WOW FOREVER · PARA TODAS LAS CLASES</p><h1>[^<]*</h1>',
               '<p class="eyebrow mlead">WOW FOREVER · MACROS</p><h1 class="mlead">Macros de WoW Forever</h1>', s, count=1)
    assert 'Macros de WoW Forever</h1>' in s
    s = re.sub(r'(<h1 class="mlead">Macros de WoW Forever</h1>)<p>.*?</p>',
               r'\1<p class="lead mlead">Elige tu clase para ver todas sus macros, o copia aquí las que sirven a cualquier clase y las raciales de tu raza. '
               r'Cada una explica qué hace y qué teclas usa.</p>', s, count=1, flags=re.S)
    s = re.sub(r'<title>.*?</title>', '<title>Macros de WoW Forever por clase, comunes y raciales | Muchamiel</title>', s, count=1, flags=re.S)
    s = s.replace('</style>', BUSCADOR_CSS + '</style>', 1)
    s = s.replace('</body>', JS + '</body>', 1)
    f.write_text(s, encoding='utf-8')


CSS = '''
.mpage h1{display:flex;align-items:center;justify-content:center;gap:14px}.mface{width:54px;height:54px;border-radius:10px;border:2px solid var(--cc);box-shadow:0 0 18px color-mix(in srgb,var(--cc) 45%,transparent)}
.mpage>.lead,.mpage>.eyebrow,main>.mlead{text-align:center}main>p.mlead{max-width:780px;margin-left:auto;margin-right:auto}.mpage>.lead{max-width:760px;margin-left:auto;margin-right:auto}
.mswitch{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;margin:16px auto 14px}
.mswitch a{display:inline-flex;align-items:center;gap:7px;padding:5px 12px 5px 5px;border:1px solid #3b3222;border-radius:999px;background:#121823;color:#e8ecf3;text-decoration:none;font-size:13.5px;font-weight:600}
.mswitch a img{width:26px;height:26px;border-radius:50%;border:1px solid var(--cc)}.mswitch a:hover{border-color:var(--cc)}
.mswitch a.on{border-color:var(--cc);background:color-mix(in srgb,var(--cc) 22%,#121823);color:#fff;box-shadow:0 0 12px color-mix(in srgb,var(--cc) 35%,transparent)}
.mtools{display:flex;justify-content:center;align-items:center;gap:10px;margin:6px auto 10px;max-width:640px}
.msearch{flex:1;padding:11px 16px;border:1px solid #4b4330;border-radius:999px;background:#0f141d;color:#eef2f8;font:inherit}.msearch:focus{outline:none;border-color:var(--gold)}
.mcount{color:#a99a7c;font-size:13px;min-width:56px}
.mleyenda{display:flex;flex-wrap:wrap;justify-content:center;gap:6px 16px;margin:4px 0 18px;font-size:13px;color:#aab4c4}.mleyenda b{color:#ffe7a6;margin-right:4px}
.mgrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;align-items:start}
.mcard{position:relative;padding:14px 16px 12px;border:1px solid #2c3444;border-left:3px solid var(--cc,#c99a3c);border-radius:10px;background:linear-gradient(170deg,#141a26,#0b0f16);scroll-margin-top:90px}
.mcard[hidden]{display:none}.mcard:target{box-shadow:0 0 0 2px var(--gold)}
.mhead{display:flex;align-items:center;gap:8px;margin-bottom:6px}.mhead h3{flex:1;margin:0;font-size:17px;color:#ffe7a6}
.mid{padding:2px 7px;border-radius:5px;background:#2a200c;border:1px solid #6b5a2e;color:#e8b84a;font:700 12px "Segoe UI",sans-serif}
.mlink{color:#6b7587;text-decoration:none;font-weight:700}.mlink:hover{color:var(--gold)}
.mcard>p{margin:4px 0 8px;line-height:1.5;color:#dfe5ee}.mcard .mtags{margin:0 0 8px}
.mcard .macro{position:relative;margin:6px 0 0}.mcard .macro pre{margin:0;padding:12px 14px 24px;padding-right:118px;border-radius:8px;white-space:pre-wrap;word-break:break-word}
.mcard .macro .copy{position:absolute;top:8px;right:8px;z-index:1}
.mlen{position:absolute;right:10px;bottom:6px;font-size:11px;color:#6b7587;z-index:1}.mlen.over{color:#ff6b63}
.mfin{display:flex;flex-wrap:wrap;justify-content:center;gap:10px;margin:26px 0 6px}
.mclases{display:grid;grid-template-columns:repeat(9,minmax(0,1fr));gap:10px;margin:6px 0 14px}
.mclase{display:flex;flex-direction:column;align-items:center;gap:6px;padding:14px 6px 12px;border:1px solid #2c3444;border-top:3px solid var(--cc);border-radius:10px;background:linear-gradient(170deg,#141a26,#0b0f16);text-decoration:none;text-align:center;transition:transform .15s,box-shadow .15s}
.mclase img{width:52px;height:52px;border-radius:10px;border:2px solid var(--cc)}.mclase b{color:var(--cc);font:900 15px "Cinzel",Georgia,serif}.mclase small{color:#a99a7c;font-size:12px}
.mclase:hover{transform:translateY(-3px);box-shadow:0 8px 22px color-mix(in srgb,var(--cc) 30%,transparent)}
.mlleva{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:12px 18px;text-align:center}.mlleva p{margin:0}
@media(max-width:1100px){.mclases{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media(max-width:760px){.mgrid{grid-template-columns:1fr}.mpage h1{font-size:30px}.mface{width:42px;height:42px}}
@media(max-width:420px){.mswitch a{font-size:0;padding:4px;gap:0}.mswitch a img{width:32px;height:32px}}
'''
