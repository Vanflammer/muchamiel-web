"""Más páginas de guías (Van, 30-10-2026): ¿Qué clase elijo?, JcJ y campos de batalla, Ya soy 60, y addons (ruta de subida y más addons).
Datos en guias/elegir-clase.json, jcj.json, nivel60.json, addons-ruta.json y addons-mas.json."""
from guias_portal import E, PARES, t, lista, fuentes
from guias_extra import CLASE, es_en, leer, estado, cabecera, pie, publicar


# ---------- ¿Qué clase elijo? ----------
def guia_elegir(d, lang):
    h = cabecera(es_en('WOW FOREVER · CLASES', 'WOW FOREVER · CLASSES', lang), es_en('¿Qué clase elijo?', 'Which class should I pick?', lang), d, lang)
    if d.get('clases'):
        h += f'<div class="divider"><h2>{es_en("Las nueve clases", "The nine classes", lang)}</h2></div><div class="tecs">'
        for x in d['clases']:
            slug = x.get('slug', '')
            cl = CLASE.get(slug, ('', ''))
            dif = max(0, min(3, int(x.get('dificultad') or 0)))
            sub = max(0, min(5, int(x.get('subir') or 0)))
            h += (f'<div class="tec"><h4><a href="../{E(slug)}/">{cl[0 if lang == "es" else 1]}</a></h4>'
                  f'<p class="tec-term">{es_en("Dificultad", "Difficulty", lang)}: {"●" * dif}{"○" * (3 - dif)} · {es_en("Subir de nivel", "Leveling", lang)}: {"★" * sub}{"☆" * (5 - sub)}</p>'
                  f'<p>{t(x.get("resumen"), lang)}</p><p><b>{es_en("En grupo", "In groups", lang)}:</b> {t(x.get("grupo"), lang)}</p>'
                  f'<p><b>{es_en("En JcJ", "In PvP", lang)}:</b> {t(x.get("jcj"), lang)}</p><p><i>{t(x.get("para_ti_si"), lang)}</i></p></div>')
        h += '</div>'
    tier = d.get('tier') or {}
    for k, tit in (('pve', es_en('Clasificación en mazmorras y bandas', 'Dungeon and raid tier list', lang)), ('pvp', es_en('Clasificación en JcJ', 'PvP tier list', lang))):
        if tier.get(k):
            h += (f'<div class="divider"><h2>{tit}</h2></div><table class="keys guia-t">'
                  + ''.join(f'<tr><th>{E(str(x.get("tier", "")))}</th><td>{E(", ".join(x.get("ramas") or []))}</td></tr>' for x in tier[k]) + '</table>')
    if t(tier.get('nota'), lang):
        h += f'<p class="fine">{t(tier.get("nota"), lang)}</p>'
    if d.get('preguntas'):
        h += (f'<div class="divider"><h2>{es_en("Dudas típicas", "Common questions", lang)}</h2></div>'
              + ''.join(f'<details class="entry"><summary>{t(x.get("pregunta"), lang)}</summary><div class="detail-body"><p>{t(x.get("respuesta"), lang)}</p></div></details>'
                        for x in d['preguntas']))
    return '<section class="guia">' + h + fuentes(d.get('fuentes'), lang) + '</section>'


# ---------- JcJ y campos de batalla ----------
def guia_jcj(d, lang):
    h = cabecera(es_en('WOW FOREVER · JcJ', 'WOW FOREVER · PvP', lang), es_en('JcJ y campos de batalla', 'PvP and battlegrounds', lang), d, lang)
    if d.get('basico'):
        h += (f'<div class="divider"><h2>{es_en("Cómo funciona", "How it works", lang)}</h2></div><div class="tecs">'
              + ''.join(f'<div class="tec"><h4>{t(x.get("titulo"), lang)}</h4><p class="tec-term">{estado(x, lang)}</p><p>{t(x.get("texto"), lang)}</p></div>' for x in d['basico'])
              + '</div>')
    for c in d.get('campos') or []:
        nuevo = f' <span class="tag-nuevo">{es_en("Nuevo", "New", lang)}</span>' if c.get('nuevo') else ''
        h += (f'<div class="divider"><h2>{t(c.get("nombre"), lang)}{nuevo}</h2></div>'
              f'<p class="guia-centro">{E(str(c.get("jugadores", "")))} · {es_en("niveles", "levels", lang)} {E(str(c.get("niveles", "")))}{estado(c, lang)}</p>'
              f'<p>{t(c.get("objetivo"), lang)}</p>' + lista(c.get('consejos'), lang))
    if d.get('mundo'):
        h += f'<div class="divider"><h2>{es_en("JcJ en el mundo abierto", "World PvP", lang)}</h2></div>' + lista(d['mundo'], lang)
    if d.get('cambios'):
        h += f'<div class="divider"><h2>{es_en("Qué cambia respecto a Classic", "What changes from Classic", lang)}</h2></div>' + lista(d['cambios'], lang)
    h += (f'<p class="guia-centro">{es_en("Técnicas de JcJ de cada clase:", "PvP techniques for each class:", lang)} '
          f'<a href="../tecnicas/">{es_en("Técnicas de juego", "Gameplay techniques", lang)}</a></p>')
    return '<section class="guia">' + h + pie(d, lang) + '</section>'


# ---------- Ya soy 60 ----------
def guia_n60(d, lang):
    h = cabecera(es_en('WOW FOREVER · NIVEL 60', 'WOW FOREVER · LEVEL 60', lang), es_en('Ya soy 60: qué hacer', 'Level 60: what to do now', lang), d, lang)
    if d.get('pasos'):
        h += (f'<div class="divider"><h2>{es_en("En este orden", "In this order", lang)}</h2></div><ol>'
              + ''.join(f'<li><b>{t(x.get("titulo"), lang)}</b>{estado(x, lang)}<br>{t(x.get("texto"), lang)}</li>' for x in d['pasos']) + '</ol>')
    if d.get('mazmorras'):
        h += f'<div class="divider"><h2>{es_en("Mazmorras de nivel 60", "Level 60 dungeons", lang)}</h2></div>' + lista(d['mazmorras'], lang)
    if d.get('reputaciones'):
        h += (f'<div class="divider"><h2>{es_en("Reputaciones que importan", "Reputations that matter", lang)}</h2></div><table class="keys guia-t">'
              + ''.join(f'<tr><th>{t(x.get("nombre"), lang)}<br><small>{t(x.get("donde"), lang)}</small></th>'
                        f'<td>{t(x.get("por_que"), lang)}{estado(x, lang)}<br><small>{t(x.get("como"), lang)}</small></td></tr>' for x in d['reputaciones']) + '</table>')
    if d.get('accesos'):
        h += (f'<div class="divider"><h2>{es_en("Para entrar en las bandas", "Raid requirements", lang)}</h2></div><table class="keys guia-t">'
              + ''.join(f'<tr><th>{t(x.get("banda"), lang)}</th><td>{t(x.get("requisito"), lang)}{estado(x, lang)}</td></tr>' for x in d['accesos']) + '</table>')
    h += (f'<p class="guia-centro">{es_en("Equipo y abalorios:", "Gear and trinkets:", lang)} <a href="../objetos/">{es_en("Abalorios, objetos clave y BiS", "Trinkets, key items and BiS", lang)}</a>'
          f' · <a href="../bandas-forever/">{es_en("Las bandas", "The raids", lang)}</a></p>')
    return '<section class="guia">' + h + pie(d, lang) + '</section>'


# ---------- Preguntas frecuentes (!faq) ----------
def guia_faq(d, lang):
    h = cabecera(es_en('WOW FOREVER · DUDAS', 'WOW FOREVER · FAQ', lang), es_en('Preguntas frecuentes', 'Frequently asked questions', lang), d, lang)
    h += '<div class="quick guia-nav">' + ''.join(f'<a href="#f{i}">{t(g.get("titulo"), lang)}</a>' for i, g in enumerate(d.get('grupos') or [])) + '</div>'
    for i, g in enumerate(d.get('grupos') or []):
        h += f'<div class="divider" id="f{i}"><h2>{t(g.get("titulo"), lang)}</h2></div>'
        for q in g.get('preguntas') or []:
            url = q.get('url', '')
            ext = ' target="_blank" rel="noopener noreferrer"' if url.startswith('http') else ''
            mas = f' <a href="{E(url, quote=True)}"{ext}>{es_en("Más", "More", lang)} →</a>' if url else ''
            h += f'<details class="entry"><summary>{t(q.get("p"), lang)}</summary><div class="detail-body"><p>{t(q.get("r"), lang)}{mas}</p></div></details>'
    return '<section class="guia">' + h + '</section>'


PAGINAS = [
    ('faq', 'faq.json', guia_faq,
     ('Preguntas frecuentes de WoW Forever: lanzamiento, precio, clases y más | Muchamiel', 'WoW Forever FAQ: launch, price, classes and more | Muchamiel'),
     ('Respuestas cortas a lo que más se pregunta de WoW Forever: cuándo sale, cuánto cuesta, qué clase hacer, cómo subir rápido, monturas, oro y addons.',
      'Short answers to the most common WoW Forever questions: release time, price, which class to play, fast leveling, mounts, gold and addons.')),
    ('elegir-clase', 'elegir-clase.json', guia_elegir,
     ('¿Qué clase elijo en WoW Forever? Comparativa de las 9 clases y clasificación | Muchamiel',
      'Which class should I pick in WoW Forever? The 9 classes compared, with tier lists | Muchamiel'),
     ('Las nueve clases de WoW Forever comparadas: dificultad, cómo suben de nivel, qué hacen en grupo y en JcJ, y para quién es cada una.',
      'The nine WoW Forever classes compared: difficulty, how they level, what they do in groups and PvP, and who each one is for.')),
    ('jcj', 'jcj.json', guia_jcj,
     ('JcJ en WoW Forever: honor, campos de batalla y Darkspear Islands | Muchamiel', 'WoW Forever PvP: honor, battlegrounds and Darkspear Islands | Muchamiel'),
     ('Cómo funciona el JcJ en WoW Forever: reinos, honor, campos de batalla (con el nuevo Darkspear Islands), consejos de cada uno y JcJ en el mundo abierto.',
      'How PvP works in WoW Forever: realms, honor, battlegrounds (including the new Darkspear Islands), tips for each and world PvP.')),
    ('nivel-60', 'nivel60.json', guia_n60,
     ('Ya soy 60 en WoW Forever: qué hacer, reputaciones y accesos a bandas | Muchamiel', 'Level 60 in WoW Forever: what to do, reputations and raid requirements | Muchamiel'),
     ('Qué hacer al llegar a nivel 60 en WoW Forever: el orden recomendado, las mazmorras, las reputaciones que importan y cómo entrar en las bandas.',
      'What to do when you hit level 60 in WoW Forever: the recommended order, dungeons, the reputations that matter and how to get into raids.')),
]


def build(page):
    for slug, fichero, fn, titulo, desc in PAGINAS:
        d = leer(fichero)
        if d:
            publicar(page, slug, d, fn, titulo, desc)


# ---------- Addons ----------
FOREVER_ADDON = {'si': ('Funciona en Forever', 'Works in Forever', 'forever'), 'beta': ('Probado en la beta', 'Tested in the beta', 'beta'),
                 'no': ('Sin versión de Forever', 'No Forever version', 'classic'), 'desconocido': ('Sin confirmar', 'Unconfirmed', 'classic')}


def tag_addon(x, lang):
    e = FOREVER_ADDON.get(x.get('forever', ''))
    return f' <span class="tag-estado {e[2]}">{e[0 if lang == "es" else 1]}</span>' if e else ''


def enlace(x):
    return f'<a href="{E(x.get("url", ""), quote=True)}" target="_blank" rel="noopener noreferrer">{E(x.get("nombre", ""))}</a>' if x.get('url') else E(x.get('nombre', ''))


def addons_ruta_html(lang):
    d = leer('addons-ruta.json')
    if not d or not d.get('addons'):
        return ''
    h = (f'<div class="divider" id="addons-ruta"><h2>{es_en("Addons que te guían misión a misión", "Addons that guide you quest by quest", lang)}</h2></div>'
         f'<p class="guia-centro">{t(d.get("intro"), lang)}</p><table class="keys guia-t">'
         + ''.join(f'<tr><th>{enlace(x)}<br><small>{t(x.get("precio"), lang)}</small></th><td>{t(x.get("que_hace"), lang)}{tag_addon(x, lang)}'
                   + (f'<br><small>{t(x.get("nota"), lang)}</small>' if t(x.get('nota'), lang) else '') + '</td></tr>' for x in d['addons']) + '</table>')
    if t(d.get('consejo'), lang):
        h += f'<p><b>{es_en("Nuestro consejo", "Our advice", lang)}:</b> {t(d.get("consejo"), lang)}</p>'
    return h


def addons_mas_html(lang):
    d = leer('addons-mas.json')
    if not d or not d.get('grupos'):
        return ''
    h = (f'<div class="divider" id="mas-addons"><h2>{es_en("Más addons recomendados para Forever", "More recommended addons for Forever", lang)}</h2></div>'
         f'<p class="guia-centro">{t(d.get("intro"), lang)}</p>')
    for g in d['grupos']:
        h += (f'<h3>{t(g.get("titulo"), lang)}</h3><table class="keys guia-t">'
              + ''.join(f'<tr><th>{enlace(x)}</th><td>{t(x.get("que_hace"), lang)}{tag_addon(x, lang)}</td></tr>' for x in g.get('addons') or []) + '</table>')
    return h + fuentes(d.get('fuentes'), lang)


def insertar_addons(s):
    """Página de addons: más addons y los de ruta de subida, antes del pie."""
    es, en = '', ''
    if 'id="mas-addons"' not in s:
        es, en = es + addons_mas_html('es'), en + addons_mas_html('en')
    if 'id="addons-ruta"' not in s:
        es, en = es + addons_ruta_html('es'), en + addons_ruta_html('en')
    if not es or '<footer' not in s:
        return s
    es, en = f'<section class="guia">{es}</section>', f'<section class="guia">{en}</section>'
    PARES.append((es, en))
    return s.replace('<footer', es + '<footer', 1)


def insertar_ruta_subir(s):
    if 'id="addons-ruta"' in s:
        return s
    es, en = addons_ruta_html('es'), addons_ruta_html('en')
    if not es:
        return s
    PARES.append((es, en))
    ancla = '<div class="divider"><h2>Monturas y viajes</h2></div>'
    return s.replace(ancla, es + ancla, 1) if ancla in s else s
