"""Notas completas de cada parche de la beta, tal cual las publica Blizzard (hilo de notas de desarrollo, Kaivax), para el
desplegable «Notas completas» de /cambios/ (Van, 16-10-2026). Se leen del texto del foro guardado en
research/notas-beta/<post>.txt y se convierten en una lista de (nivel, texto en inglés). La traducción al castellano va en
notas_es/<post>.txt, una línea por elemento y en el mismo orden (las comprueba cambios_beta al generar)."""
import re
from pathlib import Path

DIR = Path(__file__).with_name('research') / 'notas-beta'
ES = Path(__file__).with_name('notas_es')
# post del hilo → fecha del parche en PARCHES
POSTS = {'1': '24 de septiembre', '4': '1 de octubre', '5': '8 de octubre', '6': '15 de octubre'}


def limpia(t):
    t = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', t)          # enlaces markdown → texto
    t = t.replace('\\~', '~').replace('\\_', '_').replace('\\*', '*')
    t = re.sub(r'\*\*|__|(?<!\w)\*(?!\s)|(?<!\s)\*(?!\w)', '', t)
    t = t.replace('§', '').replace('·', '').strip()
    return re.sub(r'\s+', ' ', t)


def elementos(post):
    """[(nivel, texto)] del post: nivel 0 = título de apartado, 1.. = punto de lista."""
    out = []
    for linea in (DIR / f'{post}.txt').read_text(encoding='utf-8').splitlines():
        if not linea.strip() or set(linea.strip()) <= set('-*_ '):
            continue
        m = re.match(r'^(\s*)((?:[*\-]\s+)+)(.*)$', linea)
        if m:
            nivel = len(m[1].replace('\t', '    ')) // 2 + len(re.findall(r'[*\-]', m[2]))
            texto = limpia(m[3])
            if texto:
                out.append((max(1, nivel), texto))
            continue
        texto = limpia(linea)
        if not texto or re.match(r'^(Kaivax|Today, we|CHANGE LOG|Change Log)\b', texto, re.I):
            continue
        out.append((0, texto) if len(texto) < 60 and not texto.endswith('.') else (1, texto))
    return out


def traduccion(post):
    f = ES / f'{post}.txt'
    return [l.rstrip('\n') for l in f.read_text(encoding='utf-8').splitlines()] if f.exists() else None


def _e(t):
    import html
    return html.escape(t)


def bloque(post, enlace):
    """Desplegable «Notas completas» del parche (castellano). Vacío si falta la traducción o no cuadra línea a línea."""
    en, es = elementos(post), traduccion(post)
    if not es or len(es) != len(en):
        print(f'notas completas {post}: traducción', 'ausente' if not es else f'con {len(es)} líneas y hacen falta {len(en)}')
        return ''
    filas = ''
    for (nivel, t_en), t_es in zip(en, es):
        if nivel == 0:
            filas += f'<h4>{_e(t_es)}</h4>'
        else:
            nota = ' nota' if t_en.lower().startswith('developers') else ''
            filas += f'<p class="nc n{min(nivel, 4)}{nota}">{_e(t_es)}</p>'
    return (f'<details class="completas" id="completas-{post}"><summary>Notas completas de Blizzard</summary><div class="nc-body">' + filas +
            f'<p class="fine">Traducción íntegra de las notas oficiales, en el mismo orden. Los nombres de hechizos y talentos van en inglés, como en el juego. '
            f'<a href="{enlace}" target="_blank" rel="noopener noreferrer">Original de Blizzard (en inglés)</a>.</p></div></details>')


def pares():
    """{castellano: inglés} con el mismo escapado que la página, para traducciones/en.json (la versión inglesa = el original)."""
    d = {}
    for post in POSTS:
        en, es = elementos(post), traduccion(post)
        if es and len(es) == len(en):
            for (_, t_en), t_es in zip(en, es):
                d.setdefault(_e(t_es), _e(t_en))
    d['Notas completas de Blizzard'] = 'Blizzard&#x27;s full patch notes'
    return d


CSS = '''
.es-resumen{margin:4px 0 12px;padding:8px 14px;border-left:3px solid #e8b84a;border-radius:6px;background:#1a1408;color:#ffe7a6;font-size:14.5px}.es-resumen a{color:#ffe7a6;font-weight:700}.completas{scroll-margin-top:90px;margin:14px 0 4px;border:1px solid #1d4a7a;border-left:4px solid #148eff;border-radius:8px;background:#04070d}
.completas>summary{cursor:pointer;padding:12px 16px;font:900 15px "Cinzel",Georgia,serif;color:#4fb4ff;list-style:none;text-align:center}
.completas>summary::-webkit-details-marker{display:none}.completas>summary:before{content:"▸ ";color:#148eff}.completas[open]>summary:before{content:"▾ "}
.nc-body{padding:0 18px 14px}.nc-body h4{margin:16px 0 6px;padding-bottom:4px;border-bottom:1px solid #16324f;font:900 15px "Cinzel",Georgia,serif;color:#8fd0ff}
.nc-body p.nc{position:relative;margin:3px 0;padding-left:16px;font-size:14.5px;line-height:1.5;color:#4fb4ff}
.nc-body p.nc:before{content:"•";position:absolute;left:3px;color:#148eff}
.nc-body p.n2{margin-left:18px}.nc-body p.n3{margin-left:36px}.nc-body p.n4{margin-left:54px}
.nc-body p.nota{font-style:italic;color:#8fb8dc}.nc-body p.nota:before{content:"✎"}
@media(max-width:600px){.nc-body{padding:0 10px 12px}.nc-body p.n2{margin-left:10px}.nc-body p.n3{margin-left:20px}.nc-body p.n4{margin-left:30px}}
'''
