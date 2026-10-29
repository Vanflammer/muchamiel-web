"""Apartado «Auras» de WoW Forever (Van, 17-10-2026): auras de ForeverAuras listas para copiar, por clase.
El WeakAuras normal no funciona en Forever; ForeverAuras es su sustituto (CurseForge/Wago Addons).
Los códigos se bajan de Wago al generar la web (lookup + raw/encoded de la última versión); si Wago no responde,
se usa la copia de research/auras-codigos.json. «Muchamiel PvP» es nuestro: tools/auras/pvp.py → research/muchamiel-pvp.txt.
Los códigos van en assets/auras.json (la página los pide al pulsar «Copiar»), no dentro del HTML."""
import html
import json
import re
import time
import urllib.request
from pathlib import Path

from crear_portal import dist

E = html.escape
R = Path(__file__).parent / 'research'
CACHE = R / 'auras-codigos.json'
PVP = R / 'muchamiel-pvp.txt'

# (id de Wago, grupo, descripción, descripción en inglés)
AURAS = [
    ('8mJqQNEgs', 'todas', 'Todas tus reutilizaciones (hechizos y objetos) en una sola barra: los iconos se deslizan hacia el cero. Funciona en combate.',
     'All your cooldowns (spells and items) on a single bar, sliding towards zero. Works in combat.'),
    ('N3trxkQib', 'todas', 'Mejora los marcos de jugador, mascota y objetivo: XP animada, reputación, % de vida y maná, avisos de poca vida y maná, temporizador de golpe y de Disparo automático, munición y medidor de amenaza.',
     'Upgrades the player, pet and target frames: animated XP, reputation, health and mana %, low health and mana warnings, swing and Auto Shot timers, ammo and a threat meter.'),
    ('u8IW9Qg3q', 'todas', 'Una barra de lanzamiento más bonita para tus hechizos.', 'A prettier cast bar for your spells.'),
    ('UR9WERPba', 'todas', 'Pack de barras de lanzamiento con efectos mágicos, una por escuela.', 'Pack of cast bars with magic effects, one per school.'),
    ('ZLZF5RcNY', 'todas', 'Te avisa de los buffs que te faltan.', 'Warns you about the buffs you are missing.'),
    ('jQrGGxiT4', 'todas', 'En mazmorra o banda, avisa de los buffs del grupo que faltan.', 'In dungeons and raids, warns about missing group buffs.'),
    ('D_BjCo0oQ', 'todas', 'Los tres grandes debuffs en el objetivo: Maldición de los elementos, Fuego feérico o Imprudencia, y Hender o Exponer armadura.',
     'The three major debuffs on your target: Curse of the Elements, Faerie Fire or Recklessness, and Sunder or Expose Armor.'),
    ('YsnaO34aQ', 'todas', 'Los debuffs importantes del objetivo; solo sale con enemigos atacables.', 'Your target\'s major debuffs; only shows on attackable enemies.'),
    ('BNHNVYoJN', 'todas', 'Una barra por cada golpe que recibes, con la cantidad, el % de tu vida y el color de la escuela de daño.',
     'One bar for every hit you take, with the amount, the % of your health and the colour of the damage school.'),
    ('dU0YxA6Vx', 'todas', 'Enseña lo que recoges aunque uses botín automático; opcional: número, precio de Auctionator y huecos libres.',
     'Shows what you loot even with auto loot; optional: count, Auctionator price and free bag slots.'),
    ('GqIa5R4w7', 'todas', 'Avisa si te falta el buff de comida de experiencia o si ya no llevas comida.', 'Warns you when your XP food buff is missing or you have run out of food.'),
    ('56iVcdFkm', 'todas', 'Barras de habilidad de armas, defensa y profesiones que se actualizan solas.', 'Weapon, defense and profession skill bars that update on their own.'),
    ('XXzDjgfQx', 'todas', 'Distancia al objetivo en metros.', 'Distance to your target in yards.'),
    ('p7q_rWVGh', 'todas', 'Resalta el cursor del ratón para no perderlo nunca.', 'Highlights your mouse cursor so you never lose it.'),
    ('Rzn6Bgzp1', 'todas', 'Al pasar el ratón por una hierba o un mineral, te dice si puedes recogerlo.', 'Hover a herb or ore and it tells you if you can gather it.'),
    ('qwbJeq41k', 'todas', 'Avisa si se te ha olvidado activar Buscar minerales.', 'Warns you if you forgot to turn on Find Minerals.'),
    ('A-hUk309B', 'todas', 'Reutilización de las bombas de ingeniería.', 'Cooldown of engineering bombs.'),
    ('SLmdhXZpY', 'warrior', 'Tu actitud actual siempre a la vista.', 'Your current stance always in sight.'),
    ('KGAWqY4be', 'warrior', 'Se enciende cuando puedes usar Abrumar.', 'Lights up when Overpower is usable.'),
    ('-T1RCGVoW', 'warrior', 'Se enciende cuando puedes usar Revancha.', 'Lights up when Revenge is usable.'),
    ('PEFqbXRKx', 'warrior', 'Barra curva de ira (o energía) con temporizador de golpe; también para pícaro y druida.',
     'Curved rage (or energy) bar with a swing timer; also for rogues and druids.'),
    ('M9VhbS1jh', 'paladin', 'HUD completo de paladín: maná, reutilizaciones, sello, bendición y aura activos, y aviso de bendición que falta.',
     'Full paladin HUD: mana, cooldowns, active seal, blessing and aura, and a missing-blessing warning.'),
    ('wlBxhVRj9', 'hunter', 'Recordatorios, procs y contador de munición para cazador.', 'Reminders, procs and an ammo counter for hunters.'),
    ('ZubD5kh9A', 'hunter', 'Mordedura de mangosta: se ilumina cuando la puedes usar tras esquivar.', 'Mongoose Bite: lights up when it becomes usable after a dodge.'),
    ('9UI3CwaYh', 'hunter', 'Flechas y balas que te quedan.', 'Arrows and bullets left.'),
    ('NK39Hktel', 'rogue', 'Pack de auras de pícaro de Simonize.', 'Simonize\'s rogue aura pack.'),
    ('RTnVMlqmj', 'rogue', 'Suite completa de auras de pícaro.', 'A full rogue aura suite.'),
    ('MX8RN6DVQ', 'rogue', 'Barra de buffs del pícaro: Sigilo, Sprint, Evasión, Hacer picadillo, Aluvión de acero y más.',
     'Rogue buff bar: Stealth, Sprint, Evasion, Slice and Dice, Blade Flurry and more.'),
    ('j8G2JiT3p', 'rogue', 'Puntos de combo; también para druida felino.', 'Combo points; also for cat druids.'),
    ('WJ17LeX3t', 'priest', 'Palabra de poder: escudo y Alma debilitada en ti, tu objetivo y el grupo. Funciona en combate.',
     'Power Word: Shield and Weakened Soul on you, your target and your group. Works in combat.'),
    ('dOv0uSdrf', 'priest', 'Arco con lo que absorben tus escudos; también vale para mago, brujo y paladín.',
     'An arc showing what your shields absorb; also for mages, warlocks and paladins.'),
    ('Od4lLx-ZB', 'shaman', 'HUD completo de chamán Mejora.', 'Full Enhancement shaman HUD.'),
    ('k7Ekl3GwM', 'shaman', 'Choque de llamas: el debuff y su reutilización en un solo icono, también en combate.', 'Flame Shock: the debuff and its cooldown in one icon, in combat too.'),
    ('2e-DnshTA', 'mage', 'HUD de mago: recordatorios, Explosión de fuego, Nova de escarcha y reutilizaciones.', 'Mage HUD: reminders, Fire Blast, Frost Nova and cooldowns.'),
    ('N13U-73D9', 'mage', 'Todos los libros de mago del mundo y cuáles te faltan, con coordenadas.', 'Every mage book in the world and which ones you are missing, with coordinates.'),
    ('qMEHmJBNx', 'mage', 'Tu gema de maná: si la llevas y cuándo puedes usarla.', 'Your mana gem: whether you have one and when you can use it.'),
    ('K1QPQlbev', 'warlock', 'Contador de fragmentos de alma.', 'Soul Shard counter.'),
    ('r-Axx3fE2', 'druid', 'HUD de druida: recordatorios (Marca de lo Salvaje, Espinas), procs y reutilizaciones de oso y felino.',
     'Druid HUD: reminders (Mark of the Wild, Thorns), procs and bear and cat cooldowns.'),
]
CLASES = [('warrior', 'Guerrero', 'Warrior'), ('paladin', 'Paladín', 'Paladin'), ('hunter', 'Cazador', 'Hunter'), ('rogue', 'Pícaro', 'Rogue'),
          ('priest', 'Sacerdote', 'Priest'), ('shaman', 'Chamán', 'Shaman'), ('mage', 'Mago', 'Mage'), ('warlock', 'Brujo', 'Warlock'), ('druid', 'Druida', 'Druid')]
PVP_ES = ('Hecha para esta web. Lo que el rival te tira encima, en grande en el centro de la pantalla y con el tiempo que le queda: '
          'Miedo, Aullido de terror, Espiral de la muerte, Seducción, Alarido psíquico, Grito intimidatorio, Ceguera, Gubia, Golpe en los riñones, '
          'Porrazo, Martillo de justicia, Polimorfia, los silencios de Contrahechizo y Patada, aturdimientos, trampas y raíces. '
          'Debajo, los metros al objetivo en colores (rojo cuerpo a cuerpo, naranja zona muerta de 5 a 8 m, verde alcance de Miedo, amarillo hechizos) y el aviso «ZONA MUERTA». '
          'Contar las reutilizaciones del rival no se puede: Forever ya no deja a los addons leer el registro de combate. En pruebas: si algo no sale, avísanos.')
PVP_EN = ('Made for this site. What your opponent lands on you, big in the middle of the screen with its time left: '
          'Fear, Howl of Terror, Death Coil, Seduction, Psychic Scream, Intimidating Shout, Blind, Gouge, Kidney Shot, '
          'Sap, Hammer of Justice, Polymorph, the Counterspell and Kick silences, stuns, traps and roots. '
          'Below, the yards to your target in colours (red melee, orange dead zone from 5 to 8 yards, green Fear range, yellow spells) and a «DEAD ZONE» warning. '
          "Tracking your opponent's cooldowns is not possible: Forever no longer lets addons read the combat log. In testing: if something does not show, let us know.")


def _get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 (muchamielwow.github.io)'}), timeout=25).read().decode('utf-8')


def codigos():
    """Última versión de cada aura desde Wago; lo que falle se toma de la copia guardada."""
    cache = json.loads(CACHE.read_text(encoding='utf-8')) if CACHE.exists() else {}
    for i, *_ in AURAS:
        time.sleep(0.6)  # Wago corta (HTTP 429) si se le piden muy seguidas
        try:
            L = json.loads(_get('https://data.wago.io/lookup/wago?id=' + i))
            vs = (L.get('versions') or {}).get('versions') or []
            v = vs[0]['versionString'] if vs else None
            code = _get('https://data.wago.io/api/raw/encoded?id=' + i + ('&version=' + v if v else ''))
            if code.startswith('!WA:2!'):
                cache[i] = {'name': L['name'], 'user': L['user']['name'], 'version': v, 'modified': L['date']['modified'][:10],
                            'thumb': L.get('thumbnail'), 'code': code}
        except Exception as e:
            print('auras: sin conexión con Wago para', i, '→ copia guardada', type(e).__name__)
    CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding='utf-8')
    return cache


def ficha(i, info, desc, extra=''):
    th = info.get('thumb')
    img = (f'<img class="au-th" src="{E(th, quote=True)}" alt="" loading="lazy">' if th else '<div class="au-th au-th0">FA</div>')
    return (f'<article class="au">{img}<div class="au-b"><code class="au-n">{E(info["name"])}</code><code class="au-m">{E(info["user"])} · v{E(info.get("version") or "1")} · {E(info["modified"])}</code>'
            f'<p>{E(desc)}</p>{extra}<div class="au-acc"><button type="button" class="btn gold au-cp" data-aura="{E(i, quote=True)}">Copiar código</button>'
            f'<a class="btn ghost" href="https://wago.io/{E(i, quote=True)}" target="_blank" rel="noopener noreferrer">Ver en Wago</a></div></div></article>')


def pagina(base, cods):
    pvp = {'name': 'Muchamiel PvP', 'user': 'WoW Muchamiel', 'version': '2.0.0', 'modified': '2026-10-17', 'thumb': None}
    s = ('<p class="eyebrow">WOW FOREVER · ADDONS</p><h1>Auras para ForeverAuras</h1>'
         '<p class="lead">El WeakAuras de siempre no funciona en WoW Forever: el juego corta casi todos los datos de combate a los addons. '
         'Su sustituto es ForeverAuras, y aquí tienes las mejores auras hechas para él, por clase, con un botón para copiar cada código.</p>'
         '<div class="quick"><a href="#pvp">PvP</a><a href="#todas">Para todas las clases</a>'
         + ''.join(f'<a href="#{k}">{E(es)}</a>' for k, es, _ in CLASES) + '</div>'
         '<div class="divider"><h2>Cómo se ponen</h2></div><ol class="au-pasos">'
         f'<li>Instala <a href="https://www.curseforge.com/wow/addons/foreverauras" target="_blank" rel="noopener noreferrer">ForeverAuras</a> '
         '(CurseForge o Wago Addons). No lo tengas a la vez que otro WeakAuras.</li>'
         '<li>Pulsa <strong>Copiar código</strong> en el aura que quieras.</li>'
         '<li>En el juego escribe <code>/fa</code>, pulsa <strong>Importar</strong>, pega con Ctrl+V y vuelve a pulsar <strong>Importar</strong>.</li>'
         '<li>Para moverla, ábrela en <code>/fa</code> y arrástrala por la pantalla.</li></ol>'
         '<p class="fine">¿Todas de una? Mejor no: cada pack tiene su sitio en la pantalla y se pisarían unos a otros. Pon las de tu clase y alguna de las generales.</p>'
         '<div class="divider" id="pvp"><h2>PvP: hecha para esta web</h2></div><div class="au-g">'
         + ficha('muchamiel-pvp', pvp, PVP_ES).replace('<a class="btn ghost" href="https://wago.io/muchamiel-pvp" target="_blank" rel="noopener noreferrer">Ver en Wago</a>', '')
         + '</div>'
         '<div class="divider" id="todas"><h2>Para todas las clases</h2></div><div class="au-g">'
         + ''.join(ficha(i, cods[i], es) for i, g, es, _ in AURAS if g == 'todas' and i in cods) + '</div>')
    for k, es, _ in CLASES:
        lista = [ficha(i, cods[i], d) for i, g, d, _ in AURAS if g == k and i in cods]
        s += (f'<div class="divider au-cl" id="{k}"><h2><img src="{base}assets/{k}.jpg" alt="">{E(es)}</h2></div>'
              + (f'<div class="au-g">{"".join(lista)}</div>' if lista else '<p>Aún no hay auras publicadas para esta clase.</p>'))
    s += ('<p class="fine">Cada aura es de su autor y está publicada en Wago.io; aquí solo la enlazamos con su código. '
          'Los códigos se actualizan cada vez que se regenera la web. ForeverAuras está en beta, igual que el juego: si una deja de ir, mira su página en Wago.</p>')
    return s


CSS = '''
.au-pasos li{margin:6px 0}
.au-g{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px;margin:8px 0 18px}
.au{display:flex;flex-direction:column;border:1px solid #3b3222;border-radius:10px;overflow:hidden;background:linear-gradient(160deg,#171d29,#0d1119)}
.au-th{display:block;width:100%;aspect-ratio:16/9;object-fit:cover;background:#0b0f16;border-bottom:1px solid #3b3222}
.au-th0{display:flex;align-items:center;justify-content:center;font:700 34px/1 Cinzel,serif;color:#e8b84a;background:radial-gradient(circle,#2a200c,#0b0f16)}
.au-b{display:flex;flex-direction:column;flex:1;padding:14px 16px}
/* nombre y autor van en <code> para que idiomas.py no los traduzca (cambian con cada versión de Wago) */
.au-n{display:block;margin:0 0 4px;font-size:17px;font-weight:700;line-height:1.3;font-family:inherit;color:#ffe7a6;background:none;padding:0}
.au-m{display:block;margin:0 0 8px;font-size:12.5px;font-family:inherit;color:#8f9bb0;background:none;padding:0}
.au-b p{font-size:14px;line-height:1.5}
.au-acc{display:flex;flex-wrap:wrap;gap:8px;margin-top:auto;padding-top:8px}
.au-acc .btn{font-size:14px;padding:8px 14px;cursor:pointer}
.au-txt{width:100%;height:90px;margin-top:8px;font:12px/1.3 monospace;background:#0b0f16;color:#dfe5ee;border:1px solid #6b5a2e;border-radius:6px}
.au-cp.ok{background:linear-gradient(#4fd17a,#1f8a45)!important;color:#06140b!important}
.au-cl h2{display:inline-flex;align-items:center;gap:10px}.au-cl h2 img{width:34px;height:34px;border-radius:6px;border:1px solid #6b5a2e}
'''
JS = '''<script>(function(){var datos=null;
function pedir(){return datos?Promise.resolve(datos):fetch(document.getElementById('au-json').href).then(function(r){return r.json()}).then(function(j){datos=j;return j})}
function clasico(t){var a=document.createElement('textarea');a.value=t;a.setAttribute('readonly','');a.style.position='fixed';a.style.top='-1000px';document.body.appendChild(a);a.select();var ok=false;try{ok=document.execCommand('copy')}catch(e){}a.remove();return ok}
function copiar(t){if(navigator.clipboard&&window.isSecureContext){return navigator.clipboard.writeText(t).catch(function(){if(!clasico(t))throw 0})}return clasico(t)?Promise.resolve():Promise.reject(0)}
function aMano(b,t){var c=b.closest('.au-b'),x=c.querySelector('textarea.au-txt');if(!x){x=document.createElement('textarea');x.className='au-txt';x.readOnly=true;c.appendChild(x)}x.value=t;x.focus();x.select()}
document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.au-cp');if(!b)return;var txt=b.getAttribute('data-txt')||b.textContent;b.setAttribute('data-txt',txt);var code='';
pedir().then(function(j){code=j[b.getAttribute('data-aura')];return copiar(code)}).then(function(){b.classList.add('ok');b.textContent=document.getElementById('au-ok').textContent;setTimeout(function(){b.classList.remove('ok');b.textContent=txt},2200)})
.catch(function(){if(code){aMano(b,code);b.textContent=document.getElementById('au-man').textContent}else{b.textContent=document.getElementById('au-err').textContent}})})})();</script>'''


def build():
    cods = codigos()
    todos = {i: cods[i]['code'] for i, *_ in AURAS if i in cods}
    if PVP.exists():
        todos['muchamiel-pvp'] = PVP.read_text(encoding='utf-8').strip()
    (dist / 'assets').mkdir(parents=True, exist_ok=True)
    (dist / 'assets' / 'auras.json').write_text(json.dumps(todos, ensure_ascii=False), encoding='utf-8')
    tpl = (dist / 'comunes' / 'index.html').read_text(encoding='utf-8')
    head = tpl[:tpl.index('<body')].replace('</head>', '<style>' + CSS + '</style></head>', 1)
    head = re.sub(r'<title>.*?</title>', '<title>Auras para ForeverAuras (WeakAuras de WoW Forever) por clase | Muchamiel</title>', head, count=1, flags=re.S)
    head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Las mejores auras para ForeverAuras, el WeakAuras de WoW Forever: por clase, '
                  'con el código listo para copiar y cómo importarlas. Más un pack PvP con el control que te tiran y la zona muerta.">', head, count=1)
    foot = tpl[tpl.index('<footer'):tpl.index('</footer>') + 9]
    base = '../'
    d = dist / 'auras'
    d.mkdir(parents=True, exist_ok=True)
    (d / 'index.html').write_text(head + '<body><header></header><main>' + pagina(base, cods) + f'<a id="au-json" href="{base}assets/auras.json" hidden></a><span id="au-ok" hidden>¡Copiado!</span><span id="au-err" hidden>Error: ábrela en Wago</span><span id="au-man" hidden>Pulsa Ctrl+C para copiarlo</span>' + JS + foot + '</main></body></html>', encoding='utf-8')
    print('auras:', len(todos), 'códigos')
