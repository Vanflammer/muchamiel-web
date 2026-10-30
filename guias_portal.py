"""Guías completas de clase (1-60, nivel 60, JcJ) y de profesiones (1-300). Van, 30-10-2026.
Los datos están en guias/clases/<slug>.json y guias/profesiones/<slug>.json (formato en guias/ESQUEMA.md), en castellano e inglés.
Cada guía se pinta dos veces con la misma estructura (es y en) y los pares se guardan en traducciones/en.json, así /en/ sale
traducido sin pasar por la cola de pendientes. Para actualizar una guía: editar su JSON (y su «actualizado») y regenerar."""
from pathlib import Path
import html, json, re

E = html.escape
ROOT = Path(__file__).resolve().parent
DIR_CLASES = ROOT / 'guias' / 'clases'
DIR_PROF = ROOT / 'guias' / 'profesiones'
PARES = []  # (html es, html en) de todo lo pintado en esta generación

MESES = {'es': ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'],
         'en': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']}

L = {
    'resumen': ('Resumen', 'Overview'), 'subir': ('Subir del 1 al 60', 'Leveling 1-60'), 'n60': ('Nivel 60', 'Level 60'),
    'pvp': ('JcJ', 'PvP'), 'prof': ('Profesiones', 'Professions'), 'falta': ('Lo que falta', 'Still to come'),
    'beta': ('Beta (nivel 30)', 'Beta (level 30)'), 'macros': ('Macros', 'Macros'),
    'fuertes': ('Lo mejor', 'Strengths'), 'debiles': ('Lo peor', 'Weaknesses'), 'ramas': ('Las ramas', 'The specs'),
    'razas': ('Razas recomendadas', 'Recommended races'), 'talentos': ('Talentos, punto a punto', 'Talents, point by point'),
    'habilidades': ('Habilidades clave por nivel', 'Key abilities by level'), 'rotacion': ('Cómo matar mientras subes', 'How to kill while leveling'),
    'consejos': ('Consejos', 'Tips'), 'hitos': ('Niveles importantes', 'Key levels'), 'nuevo': ('Nuevo', 'New'),
    'estad': ('Estadísticas', 'Stats'), 'rot60': ('Rotación', 'Rotation'), 'consum': ('Consumibles', 'Consumables'), 'equipo': ('Equipo', 'Gear'),
    'pvp_t': ('JcJ a nivel 60', 'PvP at level 60'), 'prof_t': ('Profesiones para esta clase', 'Professions for this class'),
    'falta_t': ('Lo que aún no se sabe', 'What we don\'t know yet'),
    'promesa': ('Esta guía se actualiza cada vez que Blizzard publica cambios. Lo que aún falta lo añadimos en cuanto se sepa, y la fecha de arriba te dice cuándo la tocamos por última vez.',
                'This guide is updated every time Blizzard publishes changes. Whatever is still missing goes in as soon as it is known, and the date at the top tells you when we last touched it.'),
    'actualizado': ('Actualizado el', 'Updated'), 'fuentes': ('Fuentes', 'Sources'), 'rama_subir': ('Rama para subir', 'Leveling spec'),
    'beta_t': ('Archivo de la beta (nivel 30): builds, macros y duelos', 'Beta archive (level 30): builds, macros and duels'),
    'beta_p': ('Lo que preparamos para la beta, con 26 puntos. Sigue valiendo para los duelos de nivel bajo y para entender cada enfrentamiento.',
               'What we prepared for the beta, with 26 points. Still useful for low-level duels and to understand each matchup.'),
    'calc': ('Planifica tu build en la calculadora', 'Plan your build in the calculator'),
    'tramos': ('De 1 a 300, paso a paso', 'From 1 to 300, step by step'), 'forever': ('Lo que cambia en Forever', 'What changes in Forever'),
    'entren': ('Entrenadores', 'Trainers'), 'lomejor': ('Lo que más vale', 'What is worth the most'), 'pareja': ('Con qué profesión va', 'What to pair it with'),
    'habilidad': ('Habilidad', 'Skill'), 'volver_prof': ('Todas las profesiones', 'All professions'),
    'guias_prof': ('Guías de 1 a 300', 'Guides from 1 to 300'),
    'guias_prof_p': ('Paso a paso, con materiales y dónde conseguirlos. Las actualizamos con cada cambio de Blizzard.',
                     'Step by step, with materials and where to get them. We update them with every Blizzard change.'),
    'recoleccion': ('Recolección', 'Gathering'), 'fabricacion': ('Fabricación', 'Crafting'), 'secundaria': ('Secundaria', 'Secondary'),
}


def t(x, lang):
    if isinstance(x, dict):
        return x.get(lang) or x.get('es') or ''
    return x or ''


def l(k, lang):
    return L[k][0 if lang == 'es' else 1]


def fecha(iso, lang):
    a, m, d = (int(p) for p in iso.split('-'))
    return f'{d} de {MESES["es"][m - 1]} de {a}' if lang == 'es' else f'{MESES["en"][m - 1]} {d}, {a}'


def link(url, text):
    return f'<a href="{E(url, quote=True)}" target="_blank" rel="noopener noreferrer">{text}</a>'


def lista(items, lang, tag='ul'):
    items = [i for i in (items or []) if t(i, lang)]
    return f'<{tag}>' + ''.join(f'<li>{t(i, lang)}</li>' for i in items) + f'</{tag}>' if items else ''


def fuentes(items, lang):
    items = [f for f in (items or []) if f.get('url')]
    if not items:
        return ''
    return f'<p class="fine">{l("fuentes", lang)}: ' + ' · '.join(link(f['url'], E(f.get('nombre') or f['url'])) for f in items) + '.</p>'


def cargar(carpeta):
    out = {}
    for f in sorted(carpeta.glob('*.json')):
        try:
            out[f.stem] = json.loads(f.read_text(encoding='utf-8'))
        except ValueError as e:
            print(f'  ! {f.name} no es JSON válido: {e}')
    return out


# ---------- Clases ----------
def guia_clase(d, lang, builds60=''):
    s = d.get('subir') or {}
    n60 = d.get('nivel60') or {}
    nav = [('g-resumen', 'resumen'), ('g-subir', 'subir'), ('g-60', 'n60'), ('g-pvp', 'pvp'), ('g-prof', 'prof'), ('g-falta', 'falta'), ('beta', 'beta')]
    h = (f'<section class="guia" id="guia"><p class="guia-fecha">{l("actualizado", lang)} {fecha(d["actualizado"], lang)}</p>'
         '<div class="quick guia-nav">' + ''.join(f'<a href="#{a}">{l(k, lang)}</a>' for a, k in nav) +
         f'<a href="../calculadora/?class={d["slug"]}">{"Calculadora" if lang == "es" else "Calculator"}</a></div>')
    # Resumen
    h += f'<div class="divider" id="g-resumen"><h2>{l("resumen", lang)}</h2></div><p class="lead">{t(d.get("resumen"), lang)}</p>'
    if d.get('fuertes') or d.get('debiles'):
        h += (f'<div class="facts"><div class="fact"><h3>{l("fuertes", lang)}</h3>{lista(d.get("fuertes"), lang)}</div>'
              f'<div class="fact wait"><h3>{l("debiles", lang)}</h3>{lista(d.get("debiles"), lang)}</div></div>')
    if d.get('ramas'):
        h += f'<h3>{l("ramas", lang)}</h3><table class="keys guia-t">' + ''.join(
            f'<tr><th>{E(t(r["nombre"], lang))}</th><td><b>{t(r.get("rol"), lang)}</b> · <i>{t(r.get("mejor_para"), lang)}</i><br>{t(r.get("texto"), lang)}</td></tr>'
            for r in d['ramas']) + '</table>'
    if d.get('razas'):
        fac = {'Alianza': ('Alianza', 'Alliance'), 'Horda': ('Horda', 'Horde'), 'Ambas': ('Ambas', 'Both')}
        h += f'<h3>{l("razas", lang)}</h3><table class="keys guia-t">' + ''.join(
            f'<tr><th>{t(r.get("raza"), lang)} <small>({fac.get(r.get("faccion"), (r.get("faccion", ""),) * 2)[0 if lang == "es" else 1]})</small></th>'
            f'<td>{t(r.get("por_que"), lang)}</td></tr>' for r in d['razas']) + '</table>'
    # Subir
    h += f'<div class="divider" id="g-subir"><h2>{l("subir", lang)}</h2></div>'
    if s.get('rama'):
        h += f'<p class="guia-rama"><span>{l("rama_subir", lang)}: <b>{E(s["rama"])}</b></span></p>'
    if s.get('intro'):
        h += f'<p>{t(s["intro"], lang)}</p>'
    if s.get('talentos'):
        h += f'<h3>{l("talentos", lang)}</h3><table class="keys guia-t">' + ''.join(
            f'<tr><th>{E(str(x.get("niveles", "")))}</th><td><b>{E(x.get("puntos", ""))}</b>' + (f'<br>{t(x.get("nota"), lang)}' if t(x.get('nota'), lang) else '') + '</td></tr>'
            for x in s['talentos']) + '</table>'
    if s.get('habilidades'):
        h += f'<h3>{l("habilidades", lang)}</h3><table class="keys guia-t">' + ''.join(
            f'<tr{" class=nueva" if x.get("nuevo") else ""}><th>{E(str(x.get("nivel", "")))}</th><td><b>{E(x.get("nombre", ""))}</b>'
            + (f' <span class="tag-nuevo">{l("nuevo", lang)}</span>' if x.get('nuevo') else '') + f'<br>{t(x.get("texto"), lang)}</td></tr>'
            for x in s['habilidades']) + '</table>'
    if s.get('rotacion'):
        h += f'<h3>{l("rotacion", lang)}</h3>' + lista(s['rotacion'], lang, 'ol')
    if (s.get('extra') or {}).get('items'):
        h += f'<h3>{t(s["extra"].get("titulo"), lang)}</h3>' + lista(s['extra']['items'], lang)
    if s.get('consejos'):
        h += f'<h3>{l("consejos", lang)}</h3>' + lista(s['consejos'], lang)
    if s.get('hitos'):
        h += f'<h3>{l("hitos", lang)}</h3><table class="keys guia-t">' + ''.join(
            f'<tr><th>{E(str(x.get("nivel", "")))}</th><td>{t(x.get("texto"), lang)}</td></tr>' for x in s['hitos']) + '</table>'
    # Nivel 60
    h += f'<div class="divider" id="g-60"><h2>{l("n60", lang)}</h2></div>'
    if n60.get('intro'):
        h += f'<p>{t(n60["intro"], lang)}</p>'
    for r in n60.get('ramas') or []:
        filas = ''.join(f'<tr><th>{l(k, lang)}</th><td>{lista(r.get(c), lang)}</td></tr>'
                        for k, c in (('estad', 'estadisticas'), ('rot60', 'rotacion'), ('consum', 'consumibles')) if r.get(c))
        h += f'<h3>{E(t(r.get("nombre", ""), lang))} · {t(r.get("rol"), lang)}</h3><table class="keys guia-t">{filas}</table>'
    if n60.get('equipo'):
        h += f'<h3>{l("equipo", lang)}</h3><p>{t(n60["equipo"], lang)}</p>'
    h += builds60
    # JcJ, profesiones, lo que falta
    if d.get('pvp'):
        h += f'<div class="divider" id="g-pvp"><h2>{l("pvp_t", lang)}</h2></div>' + lista(d['pvp'], lang)
    if d.get('profesiones'):
        h += f'<div class="divider" id="g-prof"><h2>{l("prof_t", lang)}</h2></div><table class="keys guia-t">' + ''.join(
            f'<tr><th>{t(p.get("nombre"), lang)}</th><td>{t(p.get("por_que"), lang)}</td></tr>' for p in d['profesiones']) + '</table>'
    h += (f'<div class="prepare guia-falta" id="g-falta"><h3>{l("falta_t", lang)}</h3>{lista(d.get("pendiente"), lang)}'
          f'<p>{l("promesa", lang)}</p></div>' + fuentes(d.get('fuentes'), lang) + '</section>')
    return h


def insertar_clase(s, slug):
    """Mete la guía completa en la página de la clase (versión castellana) y deja lo de la beta debajo como archivo."""
    datos = cargar_clase(slug)
    if not datos or '<div class="class-banner">' not in s:
        return s, False
    import forever_portal
    b60 = '' if (datos.get('nivel60') or {}).get('sin_builds_beta') else forever_portal.builds60_clase(slug)
    es, en = guia_clase(datos, 'es', b60), guia_clase(datos, 'en', b60)
    PARES.append((es, en))
    beta = (f'<div class="divider" id="beta"><h2>{l("beta_t", "es")}</h2></div><p class="fine">{l("beta_p", "es")}</p>')
    PARES.append((beta, f'<div class="divider" id="beta"><h2>{l("beta_t", "en")}</h2></div><p class="fine">{l("beta_p", "en")}</p>'))
    s = s.replace('WOW FOREVER · BETA · NIVEL 30', 'WOW FOREVER · GUÍA DE CLASE', 1)
    i = s.index('<div class="class-banner">')
    j = s.index('</div>', i) + len('</div>')
    s = s[:j] + es + beta + s[j:]
    s = s.replace('<details open class="section" id="builds">', '<details class="section" id="builds">', 1)
    return s, True


_CACHE = {}


def cargar_clase(slug):
    if 'clases' not in _CACHE:
        _CACHE['clases'] = cargar(DIR_CLASES) if DIR_CLASES.exists() else {}
    return _CACHE['clases'].get(slug)


# ---------- Profesiones ----------
def guia_prof(d, lang):
    tipo = d.get('tipo', 'fabricacion')
    h = (f'<p class="eyebrow">{"PROFESIONES · GUÍA DE 1 A 300" if lang == "es" else "PROFESSIONS · 1 TO 300 GUIDE"}</p>'
         f'<h1>{t(d.get("nombre"), "es" if lang == "es" else "en")}</h1>'
         f'<p class="guia-fecha">{l(tipo, lang)} · {l("actualizado", lang)} {fecha(d["actualizado"], lang)}</p>'
         f'<p class="lead">{t(d.get("resumen"), lang)}</p>')
    if d.get('pareja'):
        h += f'<p><b>{l("pareja", lang)}:</b> {t(d["pareja"], lang)}</p>'
    if d.get('forever'):
        h += f'<div class="divider"><h2>{l("forever", lang)}</h2></div>' + lista(d['forever'], lang)
    if d.get('tramos'):
        h += f'<div class="divider"><h2>{l("tramos", lang)}</h2></div><table class="keys guia-t tramos">' + ''.join(
            f'<tr><th>{x.get("desde")}-{x.get("hasta")}</th><td><b>{E(x.get("receta", ""))}</b>'
            + (f' <span class="cuantas">{E(t(x.get("cuantas"), lang) if isinstance(x.get("cuantas"), dict) else str(x.get("cuantas")))}</span>' if x.get('cuantas') else '')
            + (f'<br>{t(x.get("materiales"), lang)}' if t(x.get('materiales'), lang) else '')
            + (f'<br><small>{t(x.get("nota"), lang)}</small>' if t(x.get('nota'), lang) else '') + '</td></tr>'
            for x in d['tramos']) + '</table>'
    if d.get('entrenadores'):
        h += f'<h3>{l("entren", lang)}</h3>' + lista(d['entrenadores'], lang)
    if d.get('lo_mejor'):
        h += f'<h3>{l("lomejor", lang)}</h3>' + lista(d['lo_mejor'], lang)
    if d.get('consejos'):
        h += f'<h3>{l("consejos", lang)}</h3>' + lista(d['consejos'], lang)
    h += (f'<div class="prepare guia-falta"><h3>{l("falta_t", lang)}</h3>{lista(d.get("pendiente"), lang)}<p>{l("promesa", lang)}</p></div>'
          + fuentes(d.get('fuentes'), lang)
          + f'<div class="actions" style="justify-content:center"><a class="btn ghost" href="../">{l("volver_prof", lang)}</a></div>')
    return '<section class="guia guia-prof">' + h + '</section>'


ORDEN_PROF = ['herbalism', 'mining', 'skinning', 'alchemy', 'blacksmithing', 'enchanting', 'engineering', 'leatherworking', 'tailoring',
              'cooking', 'first-aid', 'fishing']


def profesiones():
    datos = cargar(DIR_PROF) if DIR_PROF.exists() else {}
    return [(k, datos[k]) for k in ORDEN_PROF if k in datos] + [(k, v) for k, v in datos.items() if k not in ORDEN_PROF]


def build(page, dist):
    """Una página por profesión en /profesiones/<slug>/ (las de clase se meten en insertar_clase)."""
    for slug, d in profesiones():
        es_n, en_n = t(d.get('nombre'), 'es'), t(d.get('nombre'), 'en')
        titulo = (f'Guía de {es_n} en WoW Forever: de 1 a 300 paso a paso | Muchamiel', f'WoW Forever {en_n} guide: 1 to 300 step by step | Muchamiel')
        desc = (f'Cómo subir {es_n} ({en_n}) de 1 a 300 en WoW Forever: qué hacer en cada tramo, materiales, entrenadores y lo que cambia en Forever.',
                f'How to level {en_n} from 1 to 300 in WoW Forever: what to make at each step, materials, trainers and what changes in Forever.')
        es, en = guia_prof(d, 'es'), guia_prof(d, 'en')
        PARES.append((es, en))
        PARES.append(('<title>' + E(titulo[0]) + '</title>', '<title>' + E(titulo[1]) + '</title>'))
        TEXTOS_SUELTOS[titulo[0]] = titulo[1]
        TEXTOS_SUELTOS[desc[0]] = desc[1]
        (dist / 'profesiones' / slug).mkdir(parents=True, exist_ok=True)
        page('profesiones/' + slug, titulo[0], desc[0], es)


TEXTOS_SUELTOS = {}


def tarjetas_prof(lang='es'):
    """Rejilla con las guías de 1 a 300, para la página general de profesiones."""
    lista_p = profesiones()
    if not lista_p:
        return ''
    h = (f'<div class="divider" id="guias-1-300"><h2>{l("guias_prof", lang)}</h2></div><p class="guia-centro">{l("guias_prof_p", lang)}</p>'
         '<div class="guia-profs">' + ''.join(
             f'<a class="tile" href="{slug}/"><strong>{t(d.get("nombre"), lang)}</strong><span>{l(d.get("tipo", "fabricacion"), lang)}</span></a>'
             for slug, d in lista_p) + '</div>')
    return h


def insertar_prof_index(s):
    es, en = tarjetas_prof('es'), tarjetas_prof('en')
    if not es or 'id="guias-1-300"' in s:
        return s
    PARES.append((es, en))
    m = re.search(r'<div class="quick fnav">.*?</div>', s, re.S)
    if m:
        return s[:m.end()] + es + s[m.end():]
    return s


# ---------- Traducción ----------
def registrar_en():
    """Guarda en traducciones/en.json los pares castellano → inglés de las guías (misma estructura en los dos idiomas)."""
    import idiomas
    nuevos = dict(TEXTOS_SUELTOS)
    for es, en in PARES:
        ue, un = [], []
        for arbol_, out in ((idiomas.arbol(es), ue), (idiomas.arbol(en), un)):
            for tipo, n, i in idiomas.unidades(arbol_, []):
                if tipo == 'texto':
                    out.append(n.hijos[i].strip())
                elif tipo == 'unidad':
                    out.append(n.interior().strip())
        if len(ue) != len(un):
            print(f'  ! guía con estructura distinta en es/en ({len(ue)} / {len(un)}): no se registra')
            continue
        for a, b in zip(ue, un):
            if a and b:
                nuevos[a] = b  # también los iguales (nombres de rama): si no, quedan como pendientes
    if not nuevos:
        return 0
    actual = idiomas.leer_json()
    cambios = 0
    for k, v in nuevos.items():
        if k == v and actual.get(k):
            continue  # no pisar una traducción hecha a mano con el mismo texto
        if actual.get(k) != v:
            actual[k] = v
            cambios += 1
    if cambios:
        idiomas.JSON.write_text(json.dumps(actual, ensure_ascii=False, indent=1), encoding='utf-8')
    return cambios


CSS = '''
.guia-fecha{display:inline-block;margin:4px 0 12px;padding:3px 10px;border:1px solid #c99a3c66;border-radius:999px;font-size:13px;color:#ffe7a6}
.guia-nav{justify-content:center}.guia .lead{margin-top:6px}.guia h3{margin-top:26px}
.guia table.guia-t th{white-space:nowrap;vertical-align:top;color:#ffe7a6}.guia table.guia-t td{line-height:1.55}
.guia table.guia-t tr.nueva th{color:#9be29b}.tag-nuevo{display:inline-block;margin-left:6px;padding:1px 7px;border-radius:3px;font:700 11px "Segoe UI",sans-serif;
letter-spacing:.06em;background:#2a6b2a;color:#d9ffd9;vertical-align:1px}
.guia table.guia-t td ul{margin:0;padding-left:18px}.guia ol,.guia ul{line-height:1.6}.guia-rama span{display:inline-block;padding:6px 12px;border-radius:8px;background:#151b26;border:1px solid #2c3444}
.guia .fact h3{margin-top:0}.guia-falta{margin-top:30px}.guia-falta p{color:#cfd6e2}
.tramos .cuantas{color:#b6c0d0;font-size:13px}.tramos small{color:#9aa6b8}
.guia-centro{text-align:center}.guia-profs{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:10px;margin:10px 0 24px}
@media(max-width:600px){.guia table.guia-t th{white-space:normal;width:30%}}
'''
