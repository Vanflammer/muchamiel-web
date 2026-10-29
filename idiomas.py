"""Castellano + inglés.
- extraer(): saca todos los textos de web/dist a traducciones/en.json ({"castellano": "inglés"}), conservando lo ya traducido.
- construir(): crea web/dist/en/ con los textos traducidos (lo que falte queda en castellano), hreflang, canonical
  y el selector de idioma con banderas en la cabecera de las dos versiones.
GPT rellena los valores vacíos de traducciones/en.json; después basta con volver a ejecutar comunidad_portal.py."""
from html.parser import HTMLParser
from pathlib import Path
import re, json, html, shutil

ROOT = Path(__file__).resolve().parent
DIST = ROOT / 'web' / 'dist'
JSON = ROOT / 'traducciones' / 'en.json'
SITE = 'https://muchamielwow.github.io/'  # desde el 14-10; antes wow-forever-guia.pages.dev (bloqueos de LaLiga a Cloudflare)
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}
UNIT = {'p', 'li', 'h1', 'h2', 'h3', 'h4', 'summary', 'td', 'th', 'button', 'label', 'q', 'title', 'option', 'figcaption', 'dt', 'dd',
        'caption', 'small', 'strong', 'b', 'span', 'a', 'em', 'i'}
SKIP = {'script', 'style', 'code', 'pre', 'svg', 'noscript'}
ATTRS = ('alt', 'title', 'aria-label', 'placeholder')
META = ('description', 'og:title', 'og:description', 'twitter:title', 'twitter:description', 'og:site_name')
LETRAS = re.compile(r'[A-Za-zÁÉÍÓÚÜÑáéíóúüñ¿¡]{2,}')
MIN_COBERTURA = 0.98  # /en/ solo se genera con la traducción prácticamente completa (y revisada antes de subir)


class Nodo:
    def __init__(self, tag, start='', end=''):
        self.tag, self.start, self.end, self.hijos = tag, start, end, []

    def html(self):
        return self.start + ''.join(h if isinstance(h, str) else h.html() for h in self.hijos) + self.end

    def interior(self):
        return ''.join(h if isinstance(h, str) else h.html() for h in self.hijos)


class Parser(HTMLParser):
    def __init__(self, s):
        super().__init__(convert_charrefs=False)
        self.raiz = Nodo('#doc')
        self.pila = [self.raiz]
        self.feed(s)
        self.close()

    def handle_starttag(self, tag, attrs):
        n = Nodo(tag, self.get_starttag_text())
        self.pila[-1].hijos.append(n)
        if tag not in VOID:
            self.pila.append(n)

    def handle_startendtag(self, tag, attrs):
        self.pila[-1].hijos.append(Nodo(tag, self.get_starttag_text()))

    def handle_endtag(self, tag):
        for i in range(len(self.pila) - 1, 0, -1):
            if self.pila[i].tag == tag:
                self.pila[i].end = f'</{tag}>'
                del self.pila[i:]
                return
        self.pila[-1].hijos.append(f'</{tag}>')

    def handle_data(self, d): self.pila[-1].hijos.append(d)
    def handle_entityref(self, n): self.pila[-1].hijos.append(f'&{n};')
    def handle_charref(self, n): self.pila[-1].hijos.append(f'&#{n};')
    def handle_comment(self, d): self.pila[-1].hijos.append(f'<!--{d}-->')
    def handle_decl(self, d): self.pila[-1].hijos.append(f'<!{d}>')
    def handle_pi(self, d): self.pila[-1].hijos.append(f'<?{d}>')


def arbol(s):
    r = Parser(s).raiz
    if r.html() != s:
        raise ValueError('el HTML no se reconstruye igual')
    return r


def unidades(nodo, out):
    """Recorre el árbol y devuelve (nodo padre, índice o nodo) de cada texto traducible."""
    for i, h in enumerate(nodo.hijos):
        if isinstance(h, str):
            if LETRAS.search(html.unescape(h)) and not h.lstrip().startswith('<'):
                out.append(('texto', nodo, i))
            continue
        out.append(('attr', h, None))
        if h.tag in SKIP:
            continue
        if h.tag in UNIT and '<svg' not in h.interior() and LETRAS.search(html.unescape(re.sub(r'<[^>]+>', '', h.interior()))):
            out.append(('unidad', h, None))
            for sub in recorrer_attrs(h):
                out.append(('attr', sub, None))
        else:
            unidades(h, out)
    return out


def recorrer_attrs(n):
    for h in n.hijos:
        if not isinstance(h, str):
            yield h
            yield from recorrer_attrs(h)


def attrs_traducibles(start):
    res = []
    for a in ATTRS:
        for m in re.finditer(r'\s' + a + r'="([^"]*)"', start):
            res.append((m.start(1), m.end(1), m[1]))
    if start.startswith('<meta'):
        if any(f'"{k}"' in start for k in META):
            m = re.search(r'\scontent="([^"]*)"', start)
            if m:
                res.append((m.start(1), m.end(1), m[1]))
    return [(a, b, v) for a, b, v in res if LETRAS.search(html.unescape(v))]


JS_LIT = re.compile(r"'((?:[^'\\\n]|\\.)*)'")


def es_literal(v):
    return bool(LETRAS.search(v) and not re.search(r'[<>={};]|https?:', v) and not re.fullmatch(r'[a-z0-9_.-]+', v.strip())
                and (' ' in v.strip() or re.search(r'[áéíóúñ¿¡]', v)))


def literales_js(code):
    return [m for m in JS_LIT.finditer(code) if es_literal(m[1])]


def paginas():
    return [f for f in sorted(DIST.rglob('*.html')) if 'en' not in f.relative_to(DIST).parts[:1]]


def scripts():
    return [f for f in sorted(DIST.rglob('*.js')) if 'en' not in f.relative_to(DIST).parts[:1]]


def leer_json():
    try:
        return json.loads(JSON.read_text(encoding='utf-8')) if JSON.exists() else {}
    except (ValueError, OSError):
        return {}  # se está escribiendo justo ahora: se usará en la próxima generación


def extraer():
    viejo = leer_json()
    claves = {}
    for f in paginas():
        r = arbol(f.read_text(encoding='utf-8'))
        for tipo, n, i in unidades(r, []):
            if tipo == 'texto':
                k = n.hijos[i].strip()
            elif tipo == 'unidad':
                k = n.interior().strip()
            else:
                for a, b, v in attrs_traducibles(n.start):
                    claves.setdefault(html.unescape(v).strip(), '')
                if n.tag == 'script' and 'src=' not in n.start and 'ld+json' not in n.start:
                    for m in literales_js(n.interior()):
                        claves.setdefault(m[1], '')
                continue
            claves.setdefault(k, '')
    for f in scripts():
        for m in literales_js(f.read_text(encoding='utf-8')):
            claves.setdefault(m[1], '')
    # en.json es de quien traduce: aquí solo se lee. Los textos nuevos van a en-pendientes.json.
    JSON.parent.mkdir(exist_ok=True)
    if not JSON.exists():
        JSON.write_text(json.dumps({k: '' for k in claves}, ensure_ascii=False, indent=1), encoding='utf-8')
    pendientes = {k: '' for k in claves if k not in viejo}
    (JSON.parent / 'en-pendientes.json').write_text(json.dumps(pendientes, ensure_ascii=False, indent=1), encoding='utf-8')
    hechas = sum(1 for k in claves if viejo.get(k))
    return len(claves), hechas


def traducir_html(s, t):
    r = arbol(s)
    for tipo, n, i in unidades(r, []):
        if tipo == 'texto':
            k = n.hijos[i].strip()
            if t.get(k):
                n.hijos[i] = n.hijos[i].replace(k, t[k])
        elif tipo == 'unidad':
            k = n.interior().strip()
            if t.get(k):
                n.hijos = [n.interior().replace(k, t[k])]
        else:
            for a, b, v in sorted(attrs_traducibles(n.start), reverse=True):
                k = html.unescape(v).strip()
                if t.get(k):
                    n.start = n.start[:a] + html.escape(t[k], quote=True) + n.start[b:]
            if n.tag == 'script' and 'src=' not in n.start and 'ld+json' not in n.start:
                n.hijos = [traducir_js(n.interior(), t)]
    return r.html()


def traducir_js(code, t):
    return JS_LIT.sub(lambda m: "'" + t[m[1]].replace("\\", "\\\\").replace("'", "\\'") + "'" if es_literal(m[1]) and t.get(m[1]) else m[0], code)


FLAG_ES = '<svg viewBox="0 0 30 20" aria-hidden="true"><rect width="30" height="20" fill="#c60b1e"/><rect y="5" width="30" height="10" fill="#ffc400"/></svg>'
FLAG_EN = ('<svg viewBox="0 0 60 30" aria-hidden="true"><clipPath id="uk"><path d="M0 0v30h60V0z"/></clipPath><g clip-path="url(#uk)"><path d="M0 0v30h60V0z" fill="#012169"/>'
           '<path d="M0 0l60 30m0-30L0 30" stroke="#fff" stroke-width="6"/><path d="M0 0l60 30m0-30L0 30" stroke="#C8102E" stroke-width="4"/>'
           '<path d="M30 0v30M0 15h60" stroke="#fff" stroke-width="10"/><path d="M30 0v30M0 15h60" stroke="#C8102E" stroke-width="6"/></g></svg>')
LANG_CSS = ('.lang{display:flex;gap:6px;margin-left:10px;align-items:center}.lang a{display:inline-flex;width:30px;height:20px;border-radius:3px;overflow:hidden;'
            'outline:1px solid #ffffff30;opacity:.55;transition:opacity .15s}.lang a:hover,.lang a.on{opacity:1}.lang a.on{outline:2px solid var(--gold)}'
            '.lang svg{width:100%;height:100%;display:block}@media(max-width:1100px){.lang{position:absolute;top:12px;right:16px}header.site{position:sticky}}')


def ruta(f, base):
    rel = f.relative_to(base)
    return '' if rel.name == 'index.html' and len(rel.parts) == 1 else ('/'.join(rel.parts[:-1]) + '/' if rel.name == 'index.html' else None)


def selector(s, path, lang):
    s = re.sub(r'<div class="lang">.*?</div>', '', s, flags=re.S)
    sel = (f'<div class="lang"><a href="/{path}" hreflang="es" title="Español"' + (' class="on"' if lang == 'es' else '') + f'>{FLAG_ES}</a>'
           f'<a href="/en/{path}" hreflang="en" title="English"' + (' class="on"' if lang == 'en' else '') + f'>{FLAG_EN}</a></div>')
    s = s.replace('</header>', sel + '</header>', 1)  # 17-10: tras el selector Forever|Retail
    s = re.sub(r'<style id="lang-css">.*?</style>', '', s, flags=re.S)
    s = s.replace('</head>', f'<style id="lang-css">{LANG_CSS}</style></head>', 1)
    s = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">', '', s)
    alt = (f'<link rel="alternate" hreflang="es" href="{SITE}{path}"><link rel="alternate" hreflang="en" href="{SITE}en/{path}">'
           f'<link rel="alternate" hreflang="x-default" href="{SITE}{path}">')
    return s.replace('</head>', alt + '</head>', 1)


def cobertura():
    t = json.loads(JSON.read_text(encoding='utf-8')) if JSON.exists() else {}
    return t, (sum(1 for v in t.values() if v) / len(t) if t else 0)


def construir():
    total, hechas = extraer()
    t, cov = leer_json(), (hechas / total if total else 0)
    en = DIST / 'en'
    if en.exists():
        shutil.rmtree(en)
    if cov < MIN_COBERTURA:
        return total, hechas, False
    for f in list(DIST.rglob('*')):
        if f.is_dir() or f.relative_to(DIST).parts[0] == 'en':
            continue
        dest = en / f.relative_to(DIST)
        dest.parent.mkdir(parents=True, exist_ok=True)
        if f.suffix == '.html':
            s = traducir_html(f.read_text(encoding='utf-8'), t)
            s = s.replace('<html lang="es"', '<html lang="en"', 1).replace('content="es_ES"', 'content="en_US"')
            path = ruta(f, DIST) or ''
            s = s.replace(f'href="{SITE}{path}"', f'href="{SITE}en/{path}"').replace(f'content="{SITE}{path}"', f'content="{SITE}en/{path}"')
            # En inglés sobra el nombre del juego en pequeño: ya es el mismo.
            s = re.sub(r'\s*<small class="en">[^<]*</small>', '', s)
            s = re.sub(r'<span class="number">[^<]*</span>', '', s)
            s = re.sub(r'(<b>([^<]+)</b>)<small>\2</small>', r'\1', s)
            if f.name == '404.html':
                s = re.sub(r'(href|src)="/(?!en/|/)', r'\1="/en/', s).replace('url("/assets', 'url("/en/assets')
            dest.write_text(s, encoding='utf-8')
        elif f.suffix == '.js':
            dest.write_text(traducir_js(f.read_text(encoding='utf-8'), t), encoding='utf-8')
        elif f.name not in ('sitemap.xml', 'robots.txt'):
            shutil.copyfile(f, dest)
    for base, lang in ((DIST, 'es'), (en, 'en')):
        for f in base.rglob('*.html'):
            if lang == 'es' and f.relative_to(DIST).parts[0] == 'en':
                continue
            path = ruta(f, base)
            if path is None:
                continue
            f.write_text(selector(f.read_text(encoding='utf-8'), path, lang), encoding='utf-8')
    return total, hechas, True


if __name__ == '__main__':
    total, hechas = extraer()
    print(f'{total} textos en {JSON.relative_to(ROOT)}; traducidos: {hechas}')
