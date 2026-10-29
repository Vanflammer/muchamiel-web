import json, re, html
from crear_portal import dist, classes, socials
from datos_clases import DATA, BUILDS
from completar_portal import package
E=html.escape
SOCIAL_PATHS={
'YouTube':'<rect x="2" y="5" width="20" height="14" rx="4"/><path d="m10 9 6 3-6 3z" fill="#fff"/>',
'Twitch':'<path d="M4 2h18v13l-5 5h-5l-4 4v-4H4z"/><path d="M10 6v7m6-7v7" stroke="#fff" stroke-width="2"/>',
'Kick':'<path d="M3 3h5v6h3V6h3V3h6v6h-3v3h-3v3h3v3h3v3h-6v-3h-3v-3H8v6H3z"/>',
'TikTok':'<path d="M14 2h4c0 4 2 5 5 5v4c-2 0-4-1-5-2v8a7 7 0 1 1-7-7v4a3 3 0 1 0 3 3z"/>',
'X / Twitter':'<path d="M3 2h5l14 20h-5zM20 2h3L4 22H1z"/>',
'Instagram':'<rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="18" cy="6" r="1.3"/>'}
def social_icon(label):return '<svg class="rrss-icon" viewBox="0 0 24 24" aria-hidden="true" fill="currentColor">'+SOCIAL_PATHS[label]+'</svg>'
extra_css='''
body{background:radial-gradient(ellipse at 10% 0,#14305580,transparent 45%),radial-gradient(ellipse at 95% 3%,#631e2780,transparent 45%),#0b0e15}header{background:#0d111ce8;border-bottom:1px solid #bba06455}header strong{color:#e7cb8d}h1{font-family:Georgia,serif;color:#f1d99d;text-shadow:0 2px 28px #b59b5530;font-size:clamp(40px,6vw,68px)}.eyebrow{color:#d6bd85}.welcome{border-bottom:1px solid #c8ac6855;padding-bottom:32px}.community{border:1px solid #9d77d35c;border-radius:12px;background:linear-gradient(145deg,#241b36cc,#111722);box-shadow:0 12px 32px #0004}.class-card{border-radius:10px;background:linear-gradient(140deg,#202837,#10151f);box-shadow:0 8px 20px #0003;padding-right:90px}.class-card:hover{border-color:var(--class-color);box-shadow:0 0 24px color-mix(in srgb,var(--class-color) 15%,transparent)}.class-icon{width:64px;height:64px;position:absolute;right:18px;top:25px;border:2px solid var(--class-color);border-radius:10px;box-shadow:0 0 22px #0009}.class-banner{display:flex;gap:24px;align-items:center;margin:18px 0 28px}.class-banner img{width:96px;height:96px;border-radius:16px;border:2px solid var(--class-color);box-shadow:0 0 44px color-mix(in srgb,var(--class-color) 28%,transparent)}.class-banner h1{margin:0}.rrss-icon{width:19px;height:19px;flex:none;vertical-align:middle;margin-right:7px}.socials a{display:inline-flex;align-items:center;border:1px solid #ffffff20;border-radius:6px;padding:7px 10px;background:#ffffff06}.cta a{display:inline-flex;align-items:center;justify-content:center}.factions{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin:28px 0}.faction{position:relative;border:1px solid #466999;border-radius:12px;overflow:hidden;background:linear-gradient(145deg,#172d48,#101725);padding:22px;box-shadow:0 10px 30px #0004}.faction.horde{border-color:#883f49;background:linear-gradient(145deg,#451d28,#18121c)}.faction-art{width:100%;height:160px;object-fit:contain;filter:drop-shadow(0 5px 14px #0007);margin-bottom:8px}.faction h2{margin:0;font-family:Georgia,serif;font-size:31px;color:#e9cc8f}.race-list{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}.race-list a{display:inline-flex;align-items:center;gap:9px;padding:9px 12px;border:1px solid #ffffff25;border-radius:6px;text-decoration:none;background:#0003}.race-list a:hover{background:#ffffff14}.race-list img{width:28px;height:28px;border-radius:5px}.note{border-radius:10px;background:linear-gradient(130deg,#181f2c,#101620)}.quick a{background:#131c2b}.portal-tools{display:grid;grid-template-columns:1fr 1fr;gap:18px}.portal-tools a{display:block;text-decoration:none;padding:24px;border:1px solid #ad966350;border-radius:10px;background:#171d2b}.portal-tools strong{display:block;font:23px Georgia,serif;color:#e6cb91}.portal-tools p{margin-bottom:0;color:#bac5d8}.entry{border-radius:8px;overflow:hidden}.section>summary{color:#e1c995}footer{margin-top:36px}.art-credit{font-size:12px;color:#91a0b4}@media(max-width:640px){.factions,.portal-tools{grid-template-columns:1fr}.faction-art{height:125px}.class-banner img{width:72px;height:72px}.class-card{padding-right:84px}.class-banner{gap:16px}}
'''
def image(icon,base='assets/'):
    if icon=='race_skyborne':return base+'skyborne.svg'
    return base+icon+'.jpg'
def race_slug(r):return re.sub('[^a-z0-9]+','-',r.lower()).strip('-')
def factions(base='./'):
    body='<section id="razas"><h2>¿Por la Alianza o por la Horda?</h2><p class="muted">Elige tu raza: raciales, macros y clases disponibles en Forever.</p><div class="factions">'
    for faction in ['Alliance','Horde']:
        label='Alianza' if faction=='Alliance' else 'Horda';slug=faction.lower()
        body+=f'<article class="faction {slug}"><img class="faction-art" src="{base}assets/{slug}.png" alt="Estandarte de la {label}"><h2>Por la {label}</h2><div class="race-list">'
        for race in DATA['racials'][faction]:
            body+=f'<a href="{base}razas/{race_slug(race["race"])}/"><img loading="lazy" src="{image(race["icon"],base+"assets/")}" alt="">{E(race["race"])}</a>'
        body+='</div></article>'
    return body+'</div></section>'
def style_page(s):
    s=re.sub(r'<style id="portal-theme">.*?</style>','',s,flags=re.S).replace(extra_css,'')
    css=extra_css.replace('object-fit:contain','object-fit:cover')+'header{flex-wrap:wrap}.socials a[href*="twitch.tv"]{color:#c49bff}.socials a[href*="youtube.com"]{color:#ff9ca5}.socials a[href*="kick.com"]{color:#a4ed77}'
    return s.replace('</head>','<style id="portal-theme">'+css+'</style></head>',1)
def all_socials(s):
    for label,url in socials:
        pattern=r'(<a\b[^>]*href="'+re.escape(url)+r'"[^>]*>)([^<]+)(</a>)'
        s=re.sub(pattern,lambda m:m[1]+social_icon(label)+m[2]+m[3],s)
    return s.replace('d="m10 9 6 3-6 3z" fill="#fff"','d="m10 9 6 3-6 3z" fill="#0c1017"').replace('d="M10 6v7m6-7v7" stroke="#fff"','d="M10 6v7m6-7v7" stroke="#0c1017"')
def decorate():
    (dist/'assets'/'skyborne.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="8" fill="#192b42"/><path d="M10 23h32c14 0 13-16 3-16-8 0-10 8-4 10M8 33h40c16 0 10 22-1 16-5-3-3-9 1-9M15 43h16" fill="none" stroke="#c9e1ee" stroke-width="4" stroke-linecap="round"/></svg>',encoding='utf-8')
    # Preserve the existing race tooltips and copy buttons in separate race pages.
    common=(dist/'comunes'/'index.html').read_text(encoding='utf-8')
    for faction,races in DATA['racials'].items():
        for race in races:
            rs=race_slug(race['race']);match=re.search(r'<details class="entry" id="race-'+re.escape(rs)+r'">(.*?)</details>',common,re.S)
            content=match[1] if match else ''
            content=re.sub(r'<summary>.*?</summary>','',content,flags=re.S)
            page_head=common[:common.index('<body')]
            icon=image(race['icon'],'../../assets/')
            intro=f'<body><header><strong>WOW FOREVER / {"HORDA" if faction=="Horde" else "ALIANZA"}</strong><a href="../../">Inicio</a><a href="../">Elegir raza</a></header><main><p class="eyebrow">RACIALES DE FOREVER · BETA</p><div class="class-banner"><img src="{icon}" alt=""><h1>{E(race["race"])}</h1></div><p>Botones propios para escoger el momento de usar cada racial. Los efectos pasivos ya funcionan sin añadirlos a una macro.</p><div class="quick">'
            for slug,name,cls,color,_ in classes:
                if cls in race['classes']:intro+=f'<a href="../../{slug}/">{name}</a>'
            intro+='</div>'
            content=content.replace('<a class="permalink" href="#race-'+rs+'">Enlace directo</a>','')
            folder=dist/'razas'/rs;folder.mkdir(parents=True,exist_ok=True)
            tail=common[common.index('<footer'):]
            (folder/'index.html').write_text(page_head.replace('<title>Macros comunes y raciales','<title>'+E(race['race']))+intro+content+'<p><a href="../../comunes/">Macros comunes para todas las razas</a></p>'+tail,encoding='utf-8')
    race_root=dist/'razas';template=common[:common.index('<body')]
    (race_root/'index.html').write_text(template.replace('<title>Macros comunes y raciales','<title>Razas de la Horda y la Alianza')+'<body><header><strong>WOW FOREVER / RAZAS</strong><a href="../">Inicio</a></header><main><h1>Tu bando. Tu raza.</h1>'+factions('../')+common[common.index('<footer'):],encoding='utf-8')
    for file in dist.rglob('*.html'):
        s=file.read_text(encoding='utf-8');s=all_socials(style_page(s))
        if file==dist/'index.html':
            for slug,name,cls,color,_ in classes:s=s.replace(f'<span class="number">{classes.index((slug,name,cls,color,_))+1:02d} / {cls}</span>',f'<img class="class-icon" src="assets/{slug}.jpg" alt=""><span class="number">{cls}</span>')
            s=s.replace('<section id="clases">',factions()+'<div class="portal-tools"><a href="calculadora/"><strong>✦ Calculadora de talentos</strong><p>Diseña tu build de 26 puntos, carga propuestas y comparte el enlace.</p></a><a href="razas/"><strong>⚑ Razas y raciales</strong><p>Alianza y Horda: entra a las macros de tu raza.</p></a></div><section id="clases">')
        elif file.parent.name in [c[0] for c in classes]:
            slug=file.parent.name
            if 'class="class-banner"' not in s:s=re.sub(r'(<h1>.*?</h1>)',r'<div class="class-banner"><img src="../assets/'+slug+r'.jpg" alt="">\1</div>',s,count=1,flags=re.S)
            if '../calculadora/' not in s:s=s.replace('</header>','<a href="../calculadora/?class='+slug+'">Talentos</a></header>',1)
        if 'class="art-credit"' not in s:s=s.replace('</footer>','<p class="art-credit">Sitio de la comunidad, sin afiliación oficial. Arte e iconos de World of Warcraft: Blizzard Entertainment. Datos de talentos y raciales: <a href="https://talentsforever.com/" target="_blank" rel="noopener noreferrer">Talents Forever</a>, CC BY 4.0.</p></footer>')
        s=s.replace('Diseña tu build de 26 puntos, carga propuestas y comparte el enlace.','Talentos hasta nivel 60, Legacy de 0 a 5 y builds para compartir.').replace('Estandarte de la Alianza','Stormwind · Alianza').replace('Estandarte de la Horda','Orgrimmar · Horda')
        file.write_text(s,encoding='utf-8')

CALC_CSS='''
.calc-toolbar{position:sticky;top:0;z-index:5;display:flex;gap:12px;flex-wrap:wrap;align-items:center;background:#101724f5;padding:16px;border:1px solid #a88d5655;border-radius:9px}.calc-toolbar select,.calc-toolbar button,.calc-share input{font:inherit;background:#253247;color:#fff;border:1px solid #65728b;border-radius:5px;padding:9px 12px}.calc-toolbar button{cursor:pointer}.calc-count{font-weight:700;color:#e6cf91;font-size:20px}.trees{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;margin:24px 0}.tree{background:linear-gradient(160deg,#243246,#101622);border:1px solid #8b774945;border-radius:10px;padding:15px}.tree h2{font:22px Georgia,serif;color:#ebd4a1}.talent-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));grid-auto-rows:105px;gap:7px}.talent{border:1px solid #5b6882;border-radius:6px;background:#0c121d;position:relative;padding:5px;text-align:center;min-width:0}.talent.locked{border-style:dashed;opacity:.6}.talent.maxed{border-color:#e4c46e}.talent button{cursor:pointer;color:#fff;background:transparent;border:0}.talent .add{width:100%;padding:0;font:11px/1.2 "Segoe UI",sans-serif;display:flex;flex-direction:column;align-items:center;gap:3px}.talent img{width:34px;height:34px;border-radius:4px}.talent .rank{font:13px Consolas,monospace;color:#c6e7a4}.talent .minus{position:absolute;bottom:3px;right:2px;font-size:20px;line-height:20px;padding:0 5px}.talent button:focus-visible{outline:2px solid #afe67d}.calc-detail{border:1px solid #9e865955;border-radius:10px;background:#171e2b;padding:20px}.calc-detail h3{color:#e7d29e;margin-top:0}.calc-message{min-height:28px;color:#f5c78f}.calc-share{margin:22px 0}.calc-share input{width:100%}.calc-links{display:flex;gap:14px;flex-wrap:wrap}.calc-presets{display:flex;gap:8px;flex-wrap:wrap}.calc-presets button{padding:10px;background:#232f42;border:1px solid #7b6b45;color:#eee;border-radius:6px;cursor:pointer}@media(max-width:1000px){.trees{grid-template-columns:1fr}.talent-grid{max-width:450px;margin:auto;grid-auto-rows:105px}.tree h2{text-align:center}}@media(max-width:540px){.calc-toolbar{position:static}.calc-count{font-size:17px}.tree{padding:12px}.talent .add{font-size:11px}}
'''

def calculator():
    from crear_portal import head, footer, common_header
    folder=dist/'calculadora';folder.mkdir(exist_ok=True)
    talents={cls:{'trees':DATA['talents'][cls]['trees']} for _,_,cls,_,_ in classes}
    # Import the completed warlock proposals so its calculator has presets too.
    source=(dist/'warlock'/'index.html').read_text(encoding='utf-8')
    warlock=[]
    for bid,content in re.findall(r'<details id="(B\d+)" class="entry">(.*?)</details>',source,re.S):
        title=re.search(r'<summary>(.*?)</summary>',content,re.S)
        allocation=[]
        for tree in talents['Warlock']['trees']:
            line=re.search(r'<strong>'+re.escape(tree['name'])+r':</strong>(.*?)</p>',content,re.S)
            ranks={}
            if line:
                plain=html.unescape(re.sub('<[^>]+>','',line[1]))
                for name,rank in re.findall(r'([^;]+?)\s+(\d+)/\d+',plain):ranks[name.strip()]=int(rank)
            allocation.append(ranks)
        if title and sum(sum(a.values()) for a in allocation)==26:warlock.append(dict(name=html.unescape(title[1]),allocation=allocation))
    presets=dict(BUILDS);presets['Warlock']=warlock
    payload={'classes':[{'slug':s,'name':n,'key':c,'color':co} for s,n,c,co,_ in classes],'talents':talents,'presets':presets}
    body='''<p class="eyebrow">WOW FOREVER · NIVEL 30 + LEGACY</p><h1>Calculadora de talentos</h1><p>Diseña tu reparto entre las tres ramas. Límite de <strong>26 puntos</strong>: 21 del nivel 30 y 5 extras. Se respetan filas, rangos y prerrequisitos de la beta.</p><div class="calc-toolbar"><label for="class-select">Clase</label><select id="class-select"></select><span class="calc-count" id="count" aria-live="polite"></span><button id="reset" type="button">Reiniciar</button><button id="share" type="button">Copiar enlace</button><a id="guide-link" href="../">Guía de clase</a></div><p>Haz clic o toca para añadir. Shift + clic, clic derecho o el botón − para quitar. Puedes consultar un talento bloqueado; el mensaje indica qué requisito falta.</p><div id="presets" class="calc-presets"></div><p class="calc-message" id="message" role="status"></p><div class="trees" id="trees"></div><div class="calc-detail" id="detail" aria-live="polite"><h3>Inspecciona un talento</h3><p>Al pulsarlo verás aquí su efecto, rango y prerrequisito.</p></div><div class="calc-share"><label for="build-url">Enlace a tu build</label><input id="build-url" readonly></div><h2>Contrasta el reparto</h2><p>Estos son calculadores de <strong>Forever</strong>. Los datos locales fueron generados el 8/10/2026; revisa los hotfixes y el tooltip del juego antes de competir.</p><div class="calc-links"><a id="external-calc" href="https://talentsforever.com/" target="_blank" rel="noopener noreferrer">Talents Forever · calculador de esta clase</a><a href="https://wowforever.gg/en/talents/" target="_blank" rel="noopener noreferrer">WoW Forever GG · talentos</a></div><p>Los repartos se recuerdan en este navegador cuando su almacenamiento está disponible. El enlace guarda la clase y los puntos para compartirlos. Esta calculadora no aplica cambios al juego.</p><p>Datos adaptados de <a href="https://talentsforever.com/" target="_blank" rel="noopener noreferrer">Talents Forever</a>, licencia <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener noreferrer">CC BY 4.0</a>. Arte e iconos: Blizzard Entertainment. Sitio de la comunidad, sin afiliación oficial.</p>'''
    body=body.replace('WOW FOREVER · NIVEL 30 + LEGACY','WOW FOREVER · NIVELES 10–60 + LEGACY').replace('Límite de <strong>26 puntos</strong>: 21 del nivel 30 y 5 extras.','Edita el nivel máximo hasta 60 y activa hasta 5 puntos extra de Legacy. Por defecto: nivel 30 + 5 Legacy = <strong>26 puntos</strong>.')
    body=body.replace('<span class="calc-count"', '<label for="max-level">Nivel máximo</label><input id="max-level" type="number" min="10" max="60" value="30" style="width:75px;font:inherit;padding:8px"><label><input type="checkbox" id="legacy-check" checked> Legacy</label><label for="legacy-points">Puntos extra</label><input id="legacy-points" type="number" min="0" max="5" value="5" style="width:65px;font:inherit;padding:8px"><span class="calc-count"')
    body=body.replace('<div id="presets"', '<p id="required-level" class="calc-count" aria-live="polite"></p><div id="presets"')
    body=body.replace('<div class="calc-links">','<div class="calc-links"><a href="https://www.wowhead.com/forever/talent-calc" target="_blank" rel="noopener noreferrer">Wowhead · calculadora Forever</a>')
    s=head('Calculadora de talentos · WoW Forever','Calculadora de las nueve clases hasta nivel 60, con Legacy de 0 a 5 y builds para compartir.')+'<body>'+common_header('../')+'<main>'+body+footer()+'</main><script type="application/json" id="talent-data">'+json.dumps(payload,ensure_ascii=False).replace('</','<\\/')+'</script><script src="calculator.js"></script></body></html>'
    body=body.replace('<div id="presets" class="calc-presets"></div>','<details class="entry"><summary>Builds de ejemplo de nivel 30</summary><div class="detail-body"><div id="presets" class="calc-presets"></div></div></details>')
    # Rebuild the body after the final UI transformation.
    s=s[:s.index('<body>')]+'<body>'+common_header('../')+'<main>'+body+footer()+'</main><script type="application/json" id="talent-data">'+json.dumps(payload,ensure_ascii=False).replace('</','<\\/')+'</script><script src="calculator.js"></script></body></html>'
    calc_extra='.calc-toolbar input[type="number"]{background:#253247;color:#fff;border:1px solid #65728b;border-radius:5px}.calc-toolbar{flex-wrap:wrap}.calc-toolbar a{color:#d8c08a}#trees{scroll-margin-top:170px}'
    s=s.replace('</style>',extra_css+CALC_CSS+calc_extra+'</style>');s=all_socials(s)
    (folder/'index.html').write_text(s,encoding='utf-8')

if __name__=='__main__':
    # Run completar_portal.py first: this decorates a fresh, undecorated output.
    decorate();calculator();package()
    print('Tema Horda/Alianza, iconos, diez razas y calculadora preparados.')
