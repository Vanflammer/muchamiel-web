"""Páginas extra de guías (Van, 30-10-2026): trucos para empezar (en Subir de nivel), Ganar oro, Mascotas del cazador y Monturas de clase.
Datos en guias/trucos.json, guias/oro.json, guias/mascotas.json y guias/monturas.json (castellano + inglés). Usa los ayudantes de guias_portal."""
import json
from guias_portal import E, ROOT, PARES, TEXTOS_SUELTOS, t, l, fecha, lista, fuentes

ICONO = 'https://wow.zamimg.com/images/wow/icons/large/{}.jpg'
FAC = {'Alianza': ('Alianza', 'Alliance'), 'Horda': ('Horda', 'Horde'), 'Ambas': ('Ambas', 'Both')}
ESTADO = {'forever': ('Confirmado en Forever', 'Confirmed in Forever', 'forever'),
          'beta': ('Visto en la beta', 'Seen in the beta', 'beta'),
          'classic': ('Dato de Classic, sin confirmar', 'Classic data, unconfirmed', 'classic'),
          'nerfeado': ('Recortado en Forever', 'Nerfed in Forever', 'classic')}
CLASE = {'warrior': ('Guerrero', 'Warrior'), 'paladin': ('Paladín', 'Paladin'), 'hunter': ('Cazador', 'Hunter'), 'rogue': ('Pícaro', 'Rogue'),
         'priest': ('Sacerdote', 'Priest'), 'shaman': ('Chamán', 'Shaman'), 'mage': ('Mago', 'Mage'), 'warlock': ('Brujo', 'Warlock'), 'druid': ('Druida', 'Druid')}


def es_en(es, en, lang):
    return es if lang == 'es' else en


def leer(nombre):
    f = ROOT / 'guias' / nombre
    return json.loads(f.read_text(encoding='utf-8')) if f.exists() else None


def estado(x, lang):
    e = ESTADO.get((x or {}).get('estado', ''))
    return f' <span class="tag-estado {e[2]}">{e[0 if lang == "es" else 1]}</span>' if e else ''


def cabecera(eyebrow, titulo, d, lang):
    return (f'<p class="eyebrow">{eyebrow}</p><h1>{titulo}</h1>'
            f'<p class="guia-fecha">{l("actualizado", lang)} {fecha(d["actualizado"], lang)}</p><p class="lead">{t(d.get("intro"), lang)}</p>')


def pie(d, lang):
    return (f'<div class="prepare guia-falta"><h3>{l("falta_t", lang)}</h3>{lista(d.get("pendiente"), lang)}<p>{l("promesa", lang)}</p></div>'
            + fuentes(d.get('fuentes'), lang))


def publicar(page, slug, d, fn, titulo, desc):
    es, en = fn(d, 'es'), fn(d, 'en')
    PARES.append((es, en))
    TEXTOS_SUELTOS[titulo[0]] = titulo[1]
    TEXTOS_SUELTOS[desc[0]] = desc[1]
    page(slug, titulo[0], desc[0], es)


# ---------- Trucos para empezar (va dentro de Subir de nivel) ----------
def trucos_html(lang):
    d = leer('trucos.json')
    if not d or not (d.get('trucos') or d.get('maestros_armas')):
        return ''
    h = f'<div class="divider" id="trucos"><h2>{es_en("Trucos para empezar", "Tips to get started", lang)}</h2></div>'
    if t(d.get('intro'), lang):
        h += f'<p class="guia-centro">{t(d.get("intro"), lang)}</p>'
    if d.get('trucos'):
        h += '<div class="tecs">' + ''.join(
            '<div class="tec xp"><h4>' + (f'<img src="{ICONO.format(E(x["icono"]))}" alt="" width="32" height="32" loading="lazy"> ' if x.get('icono') else '')
            + f'{t(x.get("titulo"), lang)}</h4><p>{t(x.get("texto"), lang)}</p></div>' for x in d['trucos']) + '</div>'
    if d.get('maestros_armas'):
        h += (f'<h3>{es_en("Maestros de armas: dónde aprender cada arma", "Weapon masters: where to learn each weapon", lang)}</h3><table class="keys guia-t">'
              + ''.join(f'<tr><th>{t(x.get("ciudad"), lang)}<br><small>{FAC.get(x.get("faccion"), (x.get("faccion", ""),) * 2)[0 if lang == "es" else 1]} · {E(x.get("npc", ""))}</small></th>'
                        f'<td>{t(x.get("armas"), lang)}<br><small>{t(x.get("donde"), lang)}</small></td></tr>' for x in d['maestros_armas']) + '</table>')
    return h + fuentes(d.get('fuentes'), lang)


def insertar_trucos(s):
    if 'id="trucos"' in s:
        return s
    es, en = trucos_html('es'), trucos_html('en')
    if not es:
        return s
    PARES.append((es, en))
    ancla = '<div class="divider"><h2>Monturas y viajes</h2></div>'
    return s.replace(ancla, es + ancla, 1) if ancla in s else s


# ---------- Ganar oro ----------
def guia_oro(d, lang):
    h = cabecera(es_en('WOW FOREVER · ORO', 'WOW FOREVER · GOLD', lang), es_en('Ganar oro en WoW Forever', 'Making gold in WoW Forever', lang), d, lang)
    if d.get('reglas'):
        h += f'<div class="divider"><h2>{es_en("Lo básico", "The basics", lang)}</h2></div>' + lista(d['reglas'], lang)
    for tr in d.get('por_nivel') or []:
        h += (f'<div class="divider"><h2>{es_en("Nivel", "Level", lang)} {E(str(tr.get("niveles", "")))}</h2></div><div class="tecs">'
              + ''.join(f'<div class="tec"><h4>{t(m.get("titulo"), lang)}</h4><p class="tec-term">{estado(m, lang)}</p><p>{t(m.get("texto"), lang)}</p></div>'
                        for m in tr.get('metodos') or []) + '</div>')
    if d.get('profesiones'):
        h += (f'<div class="divider"><h2>{es_en("Profesiones que dan oro", "Professions that make gold", lang)}</h2></div><table class="keys guia-t">'
              + ''.join(f'<tr><th>{t(p.get("nombre"), lang)}</th><td>{t(p.get("texto"), lang)}{estado(p, lang)}</td></tr>' for p in d['profesiones']) + '</table>'
              + f'<p class="guia-centro"><a href="../profesiones/#guias-1-300">{es_en("Guías de 1 a 300 de cada profesión", "1 to 300 guides for each profession", lang)}</a></p>')
    if d.get('nerfeado'):
        h += (f'<div class="prepare guia-falta"><h3>{es_en("Lo que ya no sirve en Forever", "What no longer works in Forever", lang)}</h3><ul>'
              + ''.join(f'<li><b>{t(x.get("titulo"), lang)}:</b> {t(x.get("texto"), lang)}</li>' for x in d['nerfeado']) + '</ul></div>')
    return '<section class="guia">' + h + pie(d, lang) + '</section>'


# ---------- Mascotas del cazador ----------
def guia_mascotas(d, lang):
    h = cabecera(es_en('WOW FOREVER · CAZADOR', 'WOW FOREVER · HUNTER', lang), es_en('Mascotas del cazador', 'Hunter pets', lang), d, lang)
    h += f'<p class="guia-centro"><a href="../hunter/">{es_en("Guía completa del cazador", "Full hunter guide", lang)}</a></p>'
    if d.get('basico'):
        h += (f'<div class="divider"><h2>{es_en("Cómo funcionan", "How they work", lang)}</h2></div><div class="tecs">'
              + ''.join(f'<div class="tec"><h4>{t(x.get("titulo"), lang)}</h4><p class="tec-term">{estado(x, lang)}</p><p>{t(x.get("texto"), lang)}</p></div>' for x in d['basico']) + '</div>')
    if d.get('familias'):
        h += (f'<div class="divider"><h2>{es_en("Familias", "Families", lang)}</h2></div><table class="keys guia-t">'
              + ''.join(f'<tr><th>{t(x.get("familia"), lang)}<br><small>{E(x.get("truco", ""))}</small></th><td>{t(x.get("para"), lang)}{estado(x, lang)}'
                        + (f'<br><small>{es_en("Come", "Diet", lang)}: {t(x.get("dieta"), lang)}</small>' if t(x.get('dieta'), lang) else '') + '</td></tr>'
                        for x in d['familias']) + '</table>')
    if d.get('especiales'):
        h += (f'<div class="divider"><h2>{es_en("Mascotas que merece la pena domar", "Pets worth taming", lang)}</h2></div><table class="keys guia-t">'
              + ''.join(f'<tr><th>{E(x.get("nombre", ""))}<br><small>{t(x.get("familia"), lang)} · {es_en("nivel", "level", lang)} {E(str(x.get("nivel", "")))}</small></th>'
                        f'<td>{t(x.get("por_que"), lang)}{estado(x, lang)}<br><small>{t(x.get("donde"), lang)}</small></td></tr>' for x in d['especiales']) + '</table>')
    return '<section class="guia">' + h + pie(d, lang) + '</section>'


# ---------- Monturas de clase ----------
def guia_monturas(d, lang):
    h = cabecera(es_en('WOW FOREVER · MONTURAS', 'WOW FOREVER · MOUNTS', lang), es_en('Monturas de clase', 'Class mounts', lang), d, lang)
    if d.get('general'):
        h += f'<div class="divider"><h2>{es_en("Equitación en Forever", "Riding in Forever", lang)}</h2></div>' + lista(d['general'], lang)
    if d.get('reputacion'):
        h += f'<div class="divider" id="reputacion"><h2>{es_en("Descuento por reputación", "Reputation discount", lang)}</h2></div>' + lista(d['reputacion'], lang)
    for m in d.get('monturas') or []:
        cl = CLASE.get(m.get('clase', ''), ('', ''))
        h += (f'<div class="divider"><h2>{t(m.get("titulo"), lang)}</h2></div><p class="guia-centro">'
              + (f'<a href="../{E(m["clase"])}/">{cl[0 if lang == "es" else 1]}</a> · ' if cl[0] else '') + f'{es_en("nivel", "level", lang)} {E(str(m.get("nivel", "")))}{estado(m, lang)}</p>')
        if t(m.get('requisitos'), lang):
            h += f'<p><b>{es_en("Requisitos", "Requirements", lang)}:</b> {t(m.get("requisitos"), lang)}</p>'
        if m.get('pasos'):
            h += lista(m['pasos'], lang, 'ol')
        if t(m.get('coste'), lang):
            h += f'<p><b>{es_en("Coste", "Cost", lang)}:</b> {t(m.get("coste"), lang)}</p>'
    return '<section class="guia">' + h + pie(d, lang) + '</section>'


PAGINAS = [
    ('oro', 'oro.json', guia_oro,
     ('Cómo ganar oro en WoW Forever: métodos por nivel y lo que ya no sirve | Muchamiel', 'How to make gold in WoW Forever: methods by level and what no longer works | Muchamiel'),
     ('Guía para ganar oro en WoW Forever: qué hacer en cada tramo de nivel, qué profesiones dan más y qué métodos de Classic ha recortado Blizzard.',
      'WoW Forever gold guide: what to do at each level range, which professions make the most and which Classic methods Blizzard has nerfed.')),
    ('mascotas', 'mascotas.json', guia_mascotas,
     ('Mascotas del cazador en WoW Forever: familias, trucos y dónde domar las mejores | Muchamiel', 'WoW Forever hunter pets: families, abilities and where to tame the best ones | Muchamiel'),
     ('Guía de mascotas del cazador en WoW Forever: cómo se doman y se cuidan, el truco de cada familia y las mascotas especiales que merece la pena domar.',
      'WoW Forever hunter pet guide: how to tame and look after them, each family\'s ability and the special pets worth taming.')),
    ('monturas', 'monturas.json', guia_monturas,
     ('Monturas de clase en WoW Forever: brujo y paladín (misiones de 40 y 60) | Muchamiel', 'WoW Forever class mounts: warlock and paladin (level 40 and 60 quests) | Muchamiel'),
     ('Cómo conseguir las monturas de clase del brujo y del paladín en WoW Forever: requisitos, pasos y coste, y la equitación en Forever.',
      'How to get the warlock and paladin class mounts in WoW Forever: requirements, steps and cost, plus riding in Forever.')),
]


def build(page):
    for slug, fichero, fn, titulo, desc in PAGINAS:
        d = leer(fichero)
        if d:
            publicar(page, slug, d, fn, titulo, desc)
    import guias_extra2  # qué clase elegir, JcJ, ya soy 60
    guias_extra2.build(page)
