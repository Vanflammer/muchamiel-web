"""Capa final del portal: aspecto oficial, cabecera común, tipografía Cinzel y orden práctico.
Se ejecuta después de embellecer_portal.py (trabaja sobre web/dist) y vuelve a empaquetar."""
from pathlib import Path
import re, html
from crear_portal import dist, classes
from completar_portal import package
from datos_clases import DATA
from embellecer_portal import image, race_slug
E = html.escape

CREST = ('<svg class="crest" viewBox="0 0 32 36" aria-hidden="true"><path d="M16 1 30 6v11c0 9-6 15-14 18C8 32 2 26 2 17V6z" '
         'fill="#120d06" stroke="#e8b84a" stroke-width="2"/><path d="M16 7l3.2 7.3 7.8.6-6 5 1.9 7.6L16 23.4 9.1 27.5 11 19.9l-6-5 7.8-.6z" fill="#f4d27a"/></svg>')

CSS = '''
@font-face{font-family:"Cinzel";src:url("{fonts}cinzel.woff2") format("woff2");font-weight:400 900;font-display:swap}
:root{--gold:#f4d27a;--gold-2:#c99a3c;--gold-line:#6b5426;--ink:#06080c}
html{scroll-padding-top:84px}
body{background:radial-gradient(ellipse 70% 40% at 15% 0,#16305a66,transparent),radial-gradient(ellipse 70% 40% at 90% 0,#5a1a2466,transparent),linear-gradient(#07090e,#0a0d14 60%,#07090e);background-attachment:fixed}
header.site{position:sticky;top:0;z-index:30;display:flex;align-items:center;gap:20px;padding:0 max(20px,calc((100vw - 1180px)/2));min-height:64px;background:linear-gradient(#0c111bf5,#06080cf5);border-bottom:1px solid var(--gold-line);box-shadow:0 1px 0 #f3c76a1f,0 10px 28px #000a;flex-wrap:nowrap}
header.site .brand{display:flex;align-items:center;gap:10px;text-decoration:none;white-space:nowrap;line-height:1.1}
header.site .crest{width:28px;height:32px;flex:none;filter:drop-shadow(0 0 8px #e8b84a40)}
.brand-face{width:36px;height:36px;border-radius:50%;border:2px solid #c99a3c;box-shadow:0 0 0 3px #1a1408,0 0 12px #c99a3c55;flex:none;object-fit:cover}
header.site .brand b{display:block;font:700 17px "Cinzel",Georgia,serif;letter-spacing:.08em;color:var(--gold)}
header.site .brand small{display:block;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#a99a7c}
header.site nav{display:flex;gap:2px;flex:1;justify-content:flex-end;overflow-x:auto;scrollbar-width:none}
header.site nav::-webkit-scrollbar{display:none}
header.site nav a{padding:21px 11px;font-size:14px;font-weight:600;color:#d7dce6;text-decoration:none;white-space:nowrap;border-bottom:2px solid transparent}
header.site nav a:hover{color:var(--gold)}
header.site nav a[aria-current]{color:var(--gold);border-bottom-color:var(--gold)}
header.site nav{overflow:visible}
header.site .menu{position:relative;display:flex}
header.site .menu-btn{padding:21px 11px;font-family:inherit;font-size:14px;font-weight:600;color:#d7dce6;background:none;border:0;border-bottom:2px solid transparent;cursor:pointer;white-space:nowrap}
header.site .menu-btn:after{content:"";display:inline-block;margin-left:7px;border:4px solid transparent;border-top-color:currentColor;border-bottom:0;vertical-align:2px}
header.site .menu-btn:hover,header.site .menu-btn.cur{color:var(--gold)}
header.site .menu-btn.cur{border-bottom-color:var(--gold)}
header.site .drop{display:none;position:absolute;top:100%;left:0;z-index:40;min-width:190px;padding:6px 0;background:linear-gradient(#111827,#080b11);border:1px solid var(--gold-line);border-top:2px solid var(--gold);border-radius:0 0 4px 4px;box-shadow:0 14px 30px #000c}
/* Van 16-10: submenús a la derecha con iconos (Clases, Razas, Macros, Profesiones) */header.site .drop,header.site .drop .sub,header.site .drop a,header.site .fly a{text-align:left!important}header.site .drop a,header.site .fly a{font-size:14px!important;line-height:1.4}header.site nav a.nav-cal{position:relative;display:inline-flex;align-items:center;justify-content:center;padding:8px!important;color:#f3c76a}header.site nav a.nav-cal svg{width:28px;height:28px;display:block;transition:transform .15s}header.site nav a.nav-cal:hover svg,header.site nav a.nav-cal[aria-current] svg{transform:scale(1.12);filter:drop-shadow(0 0 6px #f3c76a99)}header.site .nav-cal-tip{position:absolute;top:100%;left:50%;transform:translate(-50%,6px);padding:4px 10px;border:1px solid #c99a3c;border-radius:5px;background:#0b0e15;color:#ffe7a6;font:600 13px/1.3 sans-serif;white-space:nowrap;opacity:0;visibility:hidden;pointer-events:none;transition:opacity .15s;z-index:50}header.site nav a.nav-cal:hover .nav-cal-tip,header.site nav a.nav-cal:focus-visible .nav-cal-tip{opacity:1;visibility:visible}header.site .m-forever,header.site .m-retail{display:contents}header.site .m-forever>a:not(.nav-parche):not(.nav-cal),header.site .m-retail>a:not(.nav-parche):not(.nav-cal){display:inline-flex;align-items:center;align-self:stretch;color:#f3c76a;text-shadow:0 0 10px #e8b84a33}header.site .m-forever>a:not(.nav-parche):not(.nav-cal):hover,header.site .m-retail>a:not(.nav-parche):not(.nav-cal):hover{color:#fff;text-shadow:0 0 12px #f3c76a99}header.site .m-forever>a[aria-current]:not(.nav-parche):not(.nav-cal){color:#fff}html.modo-retail header.site .m-forever{display:none}html:not(.modo-retail) header.site .m-retail{display:none}header.site .modo-sel{display:inline-flex;align-self:center;margin:0 0 0 14px;border:1px solid #c99a3c;border-radius:999px;overflow:hidden;flex:none}header.site{flex-wrap:wrap!important;gap:0!important;padding:8px max(16px,calc((100vw - 1180px)/2)) 0!important;align-items:center}header.site>.brand{order:0}header.site>nav.top-r{order:1;flex:none!important;margin:0 0 0 auto!important;padding:0!important;display:flex;align-items:center;gap:12px;overflow:visible!important;justify-content:flex-end!important;flex-basis:auto!important}header.site>nav.top-r a.live{margin:0!important}header.site .modo-sel{margin:0!important;position:static!important}header.site>nav.main{order:2;flex:1 1 calc(100% - 100px)!important;min-width:0;margin:6px 0 0!important;padding:0!important;justify-content:flex-start!important;flex-wrap:wrap;overflow:visible!important;border-top:1px solid #f3c76a1a}header.site>.lang{order:3;position:static!important;margin:6px 0 0 auto!important;align-self:center}header.site>.brand{padding:7px 14px!important}header.site .nav-br{display:none}@media(max-width:760px){header.site .nav-br{display:block;flex-basis:100%;height:0}}header.site{display:grid!important;grid-template-columns:auto 1fr auto;grid-template-areas:'brand . sel' 'nav nav live';align-items:center;padding-bottom:0!important}header.site>.brand{grid-area:brand}header.site>nav.top-r{grid-area:sel;justify-self:end;margin:0 78px 0 0!important}header.site>.lang{grid-area:sel;justify-self:end;margin:0!important;position:static!important}header.site>nav.live-n{grid-area:live;justify-self:end;align-self:center;display:flex!important;align-items:center;margin:6px 0 0 12px!important;padding:0!important;overflow:visible!important;flex:none!important}header.site>nav.live-n .menu-live{display:flex;align-items:center}header.site>nav.live-n a.live{margin:0!important;padding:5px 12px!important;display:flex!important;align-items:center}header.site>nav.main{grid-area:nav;margin:6px 0 0!important}header.site>.modo-tit{position:absolute;left:50%;top:35px;transform:translate(-50%,-50%);margin:0;white-space:nowrap;pointer-events:none;font:700 20px/1 'Cinzel',Georgia,serif;letter-spacing:.2em;text-transform:uppercase;color:#e8c374;text-shadow:0 0 14px #e8b84a44}html.modo-retail header.site>.modo-tit{font-family:'Marcellus SC','Cinzel',Georgia,serif;font-weight:400;-webkit-text-stroke:.7px currentColor;color:#cfb3ff;text-shadow:0 0 16px #9a5cff88}@media(max-width:1000px){header.site>.modo-tit{display:none}}@media(max-width:600px){header.site{display:flex!important;flex-wrap:wrap!important}header.site>.brand{order:0}header.site>.lang{order:1;margin:0 0 0 auto!important;position:static!important}header.site>nav.top-r{order:2;margin:8px 10px 0 auto!important;flex:none!important}header.site>nav.live-n{order:3;margin:8px auto 0 0!important;align-self:center}header.site>nav.live-n a.live{padding:6px 12px!important}header.site>nav.main{order:4;flex:1 1 100%!important}}@media(max-width:1060px){header.site .nav-br{display:block!important;flex-basis:100%;height:0}}header.site .nav-br2{display:none}@media(max-width:760px){header.site .nav-br2{display:block;flex-basis:100%;height:0}}@media(max-width:390px){header.site{padding-left:10px!important;padding-right:10px!important}header.site>.brand{padding:6px 9px!important}header.site>.lang a{width:26px!important;height:17px!important}}@media(max-width:600px){header.site{position:relative!important}html{scroll-padding-top:12px!important}.quick{top:0!important}}header.site>nav.main .menu-btn,header.site>nav.main>a,header.site>nav.main .m-forever>a,header.site>nav.main .m-retail>a{padding-top:12px!important;padding-bottom:12px!important}header.site>nav.main a.nav-parche{margin-top:6px!important;margin-bottom:6px!important;padding-top:6px!important;padding-bottom:6px!important}header.site>nav.main a.nav-cal{padding-top:8px!important;padding-bottom:8px!important}html{scroll-padding-top:130px!important}.quick{top:112px!important}@media(max-width:760px){html{scroll-padding-top:185px!important}.quick{top:164px!important}}@media(max-width:600px){html{scroll-padding-top:230px!important}.quick{top:210px!important}}@media(max-width:600px){header.site>nav.main{justify-content:center!important}}header.site .modo-sel a{padding:5px 11px!important;font:700 12.5px/1.2 sans-serif!important;letter-spacing:.04em;color:#e8dcc0!important;text-decoration:none;background:transparent}header.site .modo-sel a:hover{background:#f3c76a22}html:not(.modo-retail) header.site .modo-sel .ms-f,html.modo-retail header.site .modo-sel .ms-r{background:linear-gradient(#e8bf55,#a87a24);color:#1a1205!important}header.site .drop .sub{position:relative}header.site .drop .sub>a{padding-right:34px}header.site .drop .sub>a:after{content:"";position:absolute;right:14px;top:50%;margin-top:-5px;border:5px solid transparent;border-right:0;border-left-color:currentColor;opacity:.7}header.site .fly{display:none;position:absolute;left:100%;top:-7px;z-index:41;min-width:220px;padding:6px 0;background:linear-gradient(#111827,#080b11);border:1px solid var(--gold-line);border-left:2px solid var(--gold);border-radius:0 4px 4px 0;box-shadow:14px 14px 30px #000c}header.site .drop .sub:hover>.fly,header.site .drop .sub:focus-within>.fly{display:block}header.site .fly a{display:flex!important;align-items:center;justify-content:flex-start!important;gap:10px;padding:6px 16px!important;white-space:nowrap}header.site .fly-h{margin:6px 16px 2px;padding-top:4px;font:700 11px/1.4 "Cinzel",Georgia,serif;letter-spacing:.14em;text-transform:uppercase}header.site .fly-h+a{margin-top:0}header.site .fly a+.fly-h{margin-top:8px;border-top:1px solid #ffffff1a;padding-top:10px}header.site .fly-ali{color:#5aa2ff}header.site .fly-hor{color:#e2564a}header.site .fly2{display:none;min-width:660px;column-count:3;column-gap:0}header.site .fly2 a{padding-top:5px!important;padding-bottom:5px!important}header.site .drop .sub:hover>.fly2,header.site .drop .sub:focus-within>.fly2{display:block}header.site .fly2 a{break-inside:avoid}header.site .fly img{width:24px;height:24px;border-radius:4px;border:1px solid #000a;box-shadow:0 0 0 1px #f3c76a33;flex:none}@media(max-width:1100px){header.site .fly{display:none!important}header.site .drop .sub>a:after{display:none}header.site .drop .sub>a{padding-right:16px}}
header.site .menu:focus-within .drop,header.site .menu.open .drop{display:block}
@media(hover:hover){header.site .menu:hover .drop{display:block}}
header.site .drop a{display:block;padding:10px 16px;border:0}
header.site .drop a:hover,header.site .drop a[aria-current]{background:#f3c76a14}
header.site nav a.live{margin:12px 0 12px 8px;padding:8px 14px;border:1px solid #e8b84a;border-radius:3px;background:linear-gradient(#5b3c0c,#2d1d05);color:#ffe7a6}
header.site nav a.live:hover{background:linear-gradient(#7a5212,#3d2807)}
.crumbs{font-size:13px;color:#9aa5b8;margin:-12px 0 18px;letter-spacing:.02em}.crumbs a{color:#c9b58a;text-decoration:none}.crumbs a:hover{text-decoration:underline}
h1,h2,h3,.section>summary,.faction h2,.portal-tools strong,.class-card h3,.tree h2,.index strong,.calc-detail h3,.tile strong{font-family:"Cinzel",Georgia,serif;letter-spacing:.02em}
h1{font-weight:700;background:linear-gradient(180deg,#fff4cf 0%,#f4d27a 45%,#b8842c 100%);-webkit-background-clip:text;background-clip:text;color:transparent;text-shadow:none;filter:drop-shadow(0 2px 14px #c99a3c33)}
h1 span{-webkit-text-fill-color:transparent}
h2{color:#f1d58e;font-weight:700}
h3{color:#ead7a8}
.eyebrow{color:#d9b766;letter-spacing:.2em;font-size:12px}
.section{border:1px solid #3b3222;border-radius:6px;background:linear-gradient(180deg,#121823ee,#0c1018ee);margin:0 0 12px;padding:0 22px;box-shadow:inset 0 1px 0 #ffffff08}
.section>summary{color:var(--gold);font-size:20px;font-weight:700;padding:18px 0}
.section[open]>summary{border-bottom:1px solid #3b3222;margin-bottom:14px}
.section>summary:hover{color:#ffe7a6}
.entry{border-color:#33405a;background:#0f1520}
.entry>summary{font-weight:600}
.entry>summary:hover{background:#ffffff06}
button.copy{font:700 13px "Segoe UI",sans-serif;letter-spacing:.04em;color:#fff1c7;background:linear-gradient(#6b4a12,#3a2708);border:1px solid #d9a842;border-radius:3px;padding:8px 14px;cursor:pointer;box-shadow:inset 0 1px 0 #ffffff26,0 2px 6px #0008}
button.copy:hover{background:linear-gradient(#8a611a,#4a320b)}
.quick{position:sticky;top:64px;z-index:10;background:#0a0e15f2;padding:10px 0;margin:18px 0 22px;border-bottom:1px solid #2a2f3a;gap:8px}
.quick a{font-size:14px;border-color:#4b4330;background:#141a25;padding:8px 13px;border-radius:3px}
.quick a:hover{border-color:var(--gold);color:var(--gold)}
.class-banner{padding:24px;border:1px solid #3b3222;border-radius:8px;background:linear-gradient(110deg,color-mix(in srgb,var(--class-color,#c99a3c) 16%,#0d121b),#0b0f17 70%)}
.btn{display:inline-flex;align-items:center;gap:8px;padding:12px 20px;font-weight:700;text-decoration:none;border-radius:3px;letter-spacing:.03em}
.btn.gold{color:#1b1204;background:linear-gradient(#ffe08a,#e2a93a 60%,#b87c1f);border:1px solid #ffe7a6;box-shadow:0 0 0 1px #5a3d0c,0 6px 18px #c99a3c40}
.btn.gold:hover{filter:brightness(1.08)}
.btn.ghost{color:#f4e3b8;border:1px solid #8a6d32;background:#120f0a99}
.btn.ghost:hover{border-color:var(--gold);color:var(--gold)}
.hero{position:relative;text-align:center;padding:56px 20px 46px;margin:0 0 34px;border:1px solid #3b3222;border-radius:10px;overflow:hidden;background:linear-gradient(90deg,#16305acc,#0b0f17 45%,#0b0f17 55%,#5a1a24cc)}
.hero:before{content:"";position:absolute;inset:0;background:url("assets/alliance.png") left center/45% auto no-repeat,url("assets/horde.png") right center/45% auto no-repeat;opacity:.22;mask-image:linear-gradient(90deg,#000,transparent 45%,transparent 55%,#000);-webkit-mask-image:linear-gradient(90deg,#000,transparent 45%,transparent 55%,#000)}
.hero>*{position:relative}
.hero h1{font-size:clamp(46px,8vw,86px);margin:6px 0 8px}
.hero .lead{font-size:19px;color:#dfe5ee;max-width:640px;margin:0 auto 26px}
.hero .actions{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
.hero .hello{margin:22px auto 0;color:#aab4c4;max-width:620px;font-size:15px}
.divider{display:flex;align-items:center;gap:14px;margin:44px 0 6px}
.divider:before,.divider:after{content:"";flex:1;height:1px;background:linear-gradient(90deg,transparent,#8a6d32,transparent)}
.divider h2{margin:0;font-size:26px;text-align:center}
.sub{text-align:center;color:#a9b3c3;margin:6px 0 22px}
.tiles{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.tile{display:block;text-decoration:none;padding:20px;border:1px solid #3b3222;border-radius:8px;background:linear-gradient(160deg,#171d29,#0d1119);transition:border-color .15s,transform .15s}
.tile:hover{border-color:var(--gold);transform:translateY(-2px)}
.tile strong{display:block;color:var(--gold);font-size:18px;margin-bottom:6px}
.tile span{color:#b6c0d0;font-size:14px}
.community-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;align-items:stretch}
.community-grid>*{margin:0}
.class-card{border-radius:8px}
.class-card h3{font-size:24px}
.index a{border-color:#3b3222!important}
footer{border-top:1px solid var(--gold-line)}
@media(max-width:900px){.tiles{grid-template-columns:1fr 1fr}.community-grid{grid-template-columns:1fr}}
@media(max-width:1100px){header.site{flex-wrap:wrap;gap:0;padding:8px 16px 0}header.site nav{flex-basis:100%;justify-content:center;align-items:center;margin:0 -16px;padding:0 10px}header.site nav{flex-wrap:wrap}header.site nav>a{display:inline-flex;align-items:center;align-self:stretch}header.site nav a,header.site .menu-btn{padding:10px 9px}header.site nav a.nav-parche{align-self:center}header.site nav a.live{margin:4px 6px 6px;padding:5px 10px}html{scroll-padding-top:120px}.quick{top:100px}}
@media(max-width:760px){.hero{padding:40px 16px 34px}.hero .lead{font-size:17px}.hero:before{opacity:.14}}
@media(max-width:520px){.tiles{grid-template-columns:1fr}.quick{position:static}}
'''

CLASS_ORDER = ['builds', 'macros', 'demonios', 'duelos', 'pvp', 'equipo', 'raciales', 'nivel', 'inicio', 'fuentes']
CLASS_QUICK = [('builds', 'Builds'), ('macros', 'Macros'), ('demonios', 'Demonios'), ('duelos', 'Duelos'), ('pvp', 'BGs y mundo'),
               ('equipo', 'Equipo'), ('raciales', 'Raciales'), ('nivel', 'Habilidades'), ('inicio', 'Por qué macros'), ('fuentes', 'Fuentes')]
WARLOCK_ORDER = ['elegir', 'builds', 'macros', 'variantes', 'demonios', 'duelos', 'pvp', 'reglas', 'validacion', 'equipo', 'nivel', 'fuentes']
NAMES = {slug: name for slug, name, *_ in classes}


def depth_prefix(file):
    n = len(file.relative_to(dist).parts) - 1
    return '../' * n if n else './'


# Logo de la cabecera y el pie: la foto de Muchamiel (Van, 15-10; antes la estrella CREST y «Guía PvP · Muchamiel»).
BRAND = '<img class="brand-face" src="https://static-cdn.jtvnw.net/jtv_user_pictures/193d41e2-6ed4-4f43-b1a7-ba2b0f8f297c-profile_image-300x300.png" alt="" width="36" height="36">'
# Van 15-10: «WoW Muchamiel», sin Forever: juega a varios WoW y la web no debe atarse a uno.
BRAND_TXT = '<span><b>WoW Muchamiel</b></span>'

# Páginas del juego completo (las genera comunidad_portal.forever_pages); (carpeta, texto del menú).
FOREVER_PAGES = [('lanzamiento', 'Lanzamiento'), ('subir-nivel', 'Subir de nivel'), ('elegir-clase', 'Qué clase elegir'), ('tecnicas', 'Técnicas de juego'), ('jcj', 'JcJ y campos de batalla'), ('nivel-60', 'Ya soy 60'), ('faq', 'Preguntas frecuentes'), ('objetos', 'Abalorios y BiS'), ('oro', 'Ganar oro'), ('mascotas', 'Mascotas de cazador'), ('monturas', 'Monturas de clase'), ('builds-60', 'Builds nivel 60'),
                 ('mazmorras', 'Mazmorras'), ('profesiones', 'Profesiones'), ('legacy', 'Legacy'), ('pagar-menos', 'Cuánto cuesta jugar'), ('cambios', 'Notas del parche'), ('auras', 'Auras')]


# Van 16-10: submenús a la derecha (como Wowhead) en Clases, Razas, Macros y Profesiones del menú WoW Forever.
RAZAS_MENU = [None, ('human', 'Humano', 'race_human_male.jpg'), ('dwarf', 'Enano', 'race_dwarf_male.jpg'), ('night-elf', 'Elfo de la noche', 'race_nightelf_male.jpg'),
              ('gnome', 'Gnomo', 'race_gnome_male.jpg'),
              ('skyborne-high-order', 'Skyborne · High Order', 'https://wow.zamimg.com/images/wow/icons/large/race_skyborne_male.jpg'),
              None, ('orc', 'Orco', 'race_orc_male.jpg'), ('undead', 'No-muerto', 'race_scourge_male.jpg'), ('tauren', 'Tauren', 'race_tauren_male.jpg'),
              ('troll', 'Trol', 'race_troll_male.jpg'),
              ('skyborne-windshaper', 'Skyborne · Windshaper', 'https://wow.zamimg.com/images/wow/icons/large/race_skyborne_female.jpg')]
# None = título de facción (Van 16-10: primero Alianza y luego Horda; High Order es Alianza y Windshaper, Horda, según Blizzard).


def razas_menu(base, ico):
    out, fac = [], iter(('Alianza', 'Horda'))
    for r in RAZAS_MENU:
        out.append((None, next(fac), None, '') if r is None else (base + 'razas/' + r[0] + '/', r[1], ico(r[2]), ''))
    return out


def submenus(base):
    import forever_portal
    ico = lambda i: i if i.startswith('http') else base + 'assets/' + i
    clases = [(base + s + '/', n, base + 'assets/' + s + '.jpg', col) for s, n, _, col, _ in classes]
    return {'clases': clases,
            'razas': razas_menu(base, ico),
            'comunes': [(base + 'macros/' + s + '/', n, base + 'assets/' + s + '.jpg', col) for s, n, _, col, _ in classes],
            'profesiones': [(base + 'profesiones/#' + a, n, i, '') for a, n, i in forever_portal.prof_menu()],
            'mazmorras': __import__('mazmorras_portal').menu(base)}  # Van 16-10: las que ya tienen página, por nivel


# Van 17-10: modos Forever y Retail. Las compartidas toman el último elegido (localStorage «modo»); las demás lo fijan al visitarlas.
MODO_COMPARTIDO = {'muchamiel', 'sorteos', 'colaboraciones', 'zona-subs'}  # Van 24-10: Noticias ya no es compartida: Retail tiene las suyas
RETAIL_NOMBRES = {'clases': 'Clases', 'mazmorras': 'Mazmorras M+', 'banda': 'Banda', 'subir-nivel': 'Subir de nivel', 'profesiones': 'Profesiones',
                  'addons': 'Addons', 'notas': 'Notas del parche', 'calendario': 'Calendario', 'noticias': 'Noticias'}
MODO_JS = ("<script id=\"modo-js\">(function(){var h=document.documentElement,m=h.getAttribute('data-modo');"
           "try{if(m==='auto'){if(localStorage.getItem('modo')==='retail')h.classList.add('modo-retail')}else if(m){localStorage.setItem('modo',m)}}catch(e){}"
           "document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('.modo-sel a');if(a){try{localStorage.setItem('modo',a.getAttribute('data-modo'))}catch(_){}}})})();</script>")


def header(base, current, calc_query=''):
    # Lo propio de WoW Forever va en un desplegable: más adelante habrá uno por versión del juego.
    # Van 16-10 (noche): la Calculadora sale de los desplegables y va arriba como «Calculadora de talentos».
    calc = ('calculadora', base + 'calculadora/' + calc_query, 'Calculadora')
    juego = [('clases', base + 'clases/', 'Clases'), ('razas', base + 'razas/', 'Razas'),
             ('comunes', base + 'comunes/', 'Macros'), ('addons', base + 'addons/', 'Addons')]
    # Van 15-10: la Calculadora sale del desplegable de la beta y va como apartado propio.
    # Van 15-10: «Cambios» (notas de la beta y Classic → Forever) también con enlace propio arriba.
    # Van 17-10: la Calculadora vuelve dentro del desplegable de WoW Forever (fuera descolocaba el menú).
    items = [('cambios', base + 'cambios/', 'Notas del parche'),
             ('noticias', base + 'noticias/', 'Noticias')]  # Van 30-10: fuera «Torneo 100.000 $» del menú (el torneo ya pasó; la página sigue)
    # Para que quepa todo, lo de Muchamiel va en su desplegable (Van pidió «Patrocinadores» en lugar de «Marcas»).
    mucha = [('muchamiel', base + 'muchamiel/', 'Quién es Muchamiel'), ('sorteos', base + 'sorteos/', 'Sorteos'), ('zona-subs', base + 'zona-subs/', '⭐ Zona de subs'),
             ('colaboraciones', base + 'colaboraciones/', 'Patrocinadores')]
    # 15-10: el juego completo (4-11, nivel 60) tiene su desplegable; lo de la beta (nivel 30) queda como estaba en «WoW Forever Beta».
    # Van 16-10: orden de Van; Lanzamiento va en la portada y la Calculadora es apartado propio («Calculadora de talentos»).
    pag = dict(FOREVER_PAGES)
    forever = [('clases', base + 'clases/', 'Clases'), (calc[0], calc[1], 'Calculadora de talentos'), ('razas', base + 'razas/', 'Razas'), ('comunes', base + 'comunes/', 'Macros'),
               ('addons', base + 'addons/', 'Addons'), ('auras', base + 'auras/', 'Auras')] + [(k, base + k + '/', pag[k]) for k in ('profesiones', 'mazmorras', 'subir-nivel', 'legacy', 'pagar-menos')]  # Van 16-10: Builds 60 va al final de cada guía de clase; Calendario (16-10 noche)
    # Van 16-10: «Notas del parche» como botón azul Blizzard (clase nav-parche); el resto, en dorado (CSS NAV_VIDA en comunidad_portal).
    link = lambda key, href, label: (f'<a href="{href}"' + (' class="nav-parche"' if key in ('cambios', 'r-notas') else '')
                                     + (' aria-current="page"' if key == current else '') + f'>{label}</a>')
    menu = lambda label, items: (f'<div class="menu"><button type="button" class="menu-btn' + (' cur' if any(key == current for key, *_ in items) else '')
                                 + f'" aria-expanded="false" aria-haspopup="true">{label}</button><div class="drop">' + ''.join(link(*i) for i in items) + '</div></div>')
    nav = ''  # Van 15-10: «Inicio» hacía lo mismo que el logo; el logo lleva a la portada
    subs = submenus(base)
    fly = lambda key, href, label: (link(key, href, label) if not subs.get(key) else '<div class="sub">' + link(key, href, label) + f'<div class="fly{" fly2" if len(subs[key]) > 12 else ""}">' + ''.join(
        (f'<p class="fly-h {"fly-ali" if n == "Alianza" else "fly-hor"}">{n}</p>' if h is None else
         f'<a href="{h}">' + (f'<img src="{i}" alt="" loading="lazy">' if i else '') + '<span' + (f' style="color:{c}"' if c else '') + f'>{n}</span></a>') for h, n, i, c in subs[key]) + '</div></div>')
    menu_fly = lambda label, items: (f'<div class="menu"><button type="button" class="menu-btn' + (' cur' if any(key == current for key, *_ in items) else '')
                                     + f'" aria-expanded="false" aria-haspopup="true">{label}</button><div class="drop">' + ''.join(fly(*i) for i in items) + '</div></div>')
    # Van 17-10: el calendario, fuera del desplegable y justo a la izquierda de «WoW Forever»: solo un icono; al pasar el ratón sale «Calendario».
    calicon = lambda key, href: (f'<a class="nav-cal" href="{href}" aria-label="Calendario"' + (' aria-current="page"' if current == key else '') + '>'
            '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<rect x="3" y="4.5" width="18" height="16.5" rx="2.5"/><path d="M3 9.5h18M8 2.5v4M16 2.5v4"/><path d="M7.5 13.5h2M11 13.5h2M14.5 13.5h2M7.5 17h2M11 17h2"/></svg>'
            '<span class="nav-cal-tip">Calendario</span></a>')
    # Van 17-10: dos modos (Forever y Retail) con su propio menú; lo demás es compartido. El CSS enseña el del modo de la página
    # (html.modo-retail); en las compartidas, el último elegido (MODO_JS).
    r = base + 'retail/'
    retail = [('r-inicio', r, 'Empieza aquí'), ('r-clases', r + 'clases/', 'Clases'), ('r-mazmorras', r + 'mazmorras/', 'Mazmorras M+'),
              ('r-banda', r + 'banda/', 'Banda'), ('r-subir-nivel', r + 'subir-nivel/', 'Subir de nivel'), ('r-profesiones', r + 'profesiones/', 'Profesiones'),
              ('r-addons', r + 'addons/', 'Addons')]
    nav += ('<div class="m-forever">' + calicon('calendario', base + 'calendario/') + menu_fly('WoW Forever', forever)  # Van 16-10: fuera «WoW Forever Beta»
            + link(*items[0]) + '<i class="nav-br"></i>' + ''.join(link(*x) for x in items[1:]) + '</div>'  # Van 17-10: el Torneo es de Forever
            + '<div class="m-retail">' + calicon('r-calendario', r + 'calendario/') + menu('WoW Retail', retail) + link('r-notas', r + 'notas/', 'Notas del parche') + '<i class="nav-br"></i>' + link('r-noticias', r + 'noticias/', 'Noticias') + '</div>')
    # Van 17-10: lo de Muchamiel, fuera del desplegable (con la cabecera en dos filas hay sitio)
    nav += ''.join(link(*i) for i in items[3:]) + ''.join(('<i class="nav-br2"></i>' if k == 'sorteos' else '') + link(k, h, 'Muchamiel' if k == 'muchamiel' else l) for k, h, l in mucha)
    # Van 16-10: el botón de directo abre un desplegable con Twitch, Kick y YouTube; la red donde no emite sale deshabilitada (live.js).
    live = ('<div class="menu menu-live"><a class="live" href="https://www.twitch.tv/muchamiel" role="button" aria-haspopup="true" aria-expanded="false">OFFLINE</a>'
            '<div class="drop drop-live">'
            '<a class="lp-item tw off" href="https://www.twitch.tv/muchamiel" target="_blank" rel="noopener noreferrer" title="Offline"><span>Twitch</span><b class="est"></b></a>'
            '<a class="lp-item kick off" href="https://kick.com/muchamiel" target="_blank" rel="noopener noreferrer" title="Offline"><span>Kick</span><b class="est"></b></a>'
            '<a class="lp-item yt off" href="https://www.youtube.com/@muchamiel" target="_blank" rel="noopener noreferrer" title="Offline"><span>YouTube</span><b class="est"></b></a></div></div>'
            '')  # Van 16-10: sin etiquetas Twitch/Kick al lado: el botón lleva al directo
    sel = (f'<div class="modo-sel" role="group" aria-label="Versión del juego"><a class="ms-f" href="{base}" data-modo="forever">Forever</a>'
           f'<a class="ms-r" href="{base}retail/" data-modo="retail">Retail</a></div>')
    # Van 17-10: cabecera en dos filas. Arriba: logo a la izquierda; directo y selector Forever|Retail a la derecha.
    # Abajo: los menús y las banderas (idiomas.py las mete justo antes de </header>).
    return (f'<header class="site"><a class="brand" href="{base}">{BRAND}{BRAND_TXT}</a>'
            '<p class="modo-tit" aria-hidden="true"><span class="m-forever">World of Warcraft · Forever</span><span class="m-retail">World of Warcraft · Midnight</span></p>'  # Van 17-10: dónde estás
            f'<nav class="top-r" aria-label="Directo y versión del juego">{sel}</nav><nav class="live-n" aria-label="Directo">{live}</nav>'
            f'<nav class="main" aria-label="Secciones del portal">{nav}</nav></header>')


def block(s, start):
    """Devuelve (inicio, fin) del <details> que empieza en start, contando los anidados."""
    depth, i = 0, start
    for m in re.finditer(r'<details\b|</details>', s[start:]):
        depth += 1 if m.group(0) == '<details' else -1
        if depth == 0:
            return start, start + m.end()
    raise ValueError('details sin cerrar')


def reorder_sections(s, order, open_id=None):
    found = {}
    for m in re.finditer(r'<details\b[^>]*>', s):
        tag = m.group(0)
        if 'class="section"' not in tag:
            continue
        sid = re.search(r'\bid="([^"]+)"', tag)[1]
        if any(a <= m.start() < b for a, b in found.values()):
            continue
        found[sid] = block(s, m.start())
    if not found:
        return s
    spans = sorted(found.values())
    first, last = spans[0][0], spans[-1][1]
    if s[first:last].count('<details') != sum(s[a:b].count('<details') for a, b in spans):
        raise ValueError('hay contenido entre secciones')
    pieces = {sid: s[a:b] for sid, (a, b) in found.items()}
    ids = [i for i in order if i in pieces] + [i for i, _ in sorted(found.items(), key=lambda kv: kv[1]) if i not in order]
    out = []
    for sid in ids:
        piece = re.sub(r'^(<details\b[^>]*?) open(?=[ >])', r'\1', pieces[sid])
        if sid == open_id:
            piece = re.sub(r'^<details\b', '<details open', piece)
        out.append(piece)
    return s[:first] + ''.join(out) + s[last:]


def set_style(s, base):
    s = re.sub(r'<style id="oficial-theme">.*?</style>', '', s, flags=re.S)
    css = CSS.replace('{fonts}', base + 'assets/fonts/').replace('url("assets/', 'url("' + base + 'assets/')
    preload = f'<link rel="preload" href="{base}assets/fonts/cinzel.woff2" as="font" type="font/woff2" crossorigin>'
    s = re.sub(r'<link rel="preload" href="[^"]*cinzel\.woff2"[^>]*>', '', s)
    return s.replace('</head>', preload + '<style id="oficial-theme">' + css + '</style></head>', 1)


def crumbs(base, trail):
    parts = [f'<a href="{base}">Inicio</a>'] + [f'<a href="{h}">{E(t)}</a>' if h else f'<span>{E(t)}</span>' for t, h in trail]
    return '<nav class="crumbs" aria-label="Estás en">' + ' › '.join(parts) + '</nav>'


def set_crumbs(s, html_crumbs):
    s = re.sub(r'<nav class="crumbs".*?</nav>', '', s, flags=re.S)
    return s.replace('<main>', '<main>' + html_crumbs, 1)


def cut(s, pattern):
    m = re.search(pattern, s, re.S)
    if not m:
        raise ValueError('no encuentro ' + pattern)
    return m.group(0), s[:m.start()] + s[m.end():]


def home(s):
    if 'class="hero"' in s:
        return s
    main_start, main_end = s.index('<main>') + 6, s.index('<footer')
    body = s[main_start:main_end]
    community, body = cut(body, r'<aside class="community">.*?</aside>')
    razas, body = cut(body, r'<section id="razas">.*?</section>')
    clases, body = cut(body, r'<section id="clases">.*?</section>')
    sorteo, body = cut(body, r'<section class="note" aria-label="Metas de la comunidad">.*?</section>')
    directo, body = cut(body, r'<section class="note"><strong>Forever también se juega en directo</strong>.*?</section>')
    clases = clases.replace('<h2>¿Qué clase juegas?</h2><p class="muted">Macros en inglés, explicaciones en español. Entra directamente a la guía que quieras.</p>',
                            '<div class="divider"><h2>Elige tu clase</h2></div><p class="sub">Builds de 26 puntos, macros listas para copiar y cómo ganar cada duelo.</p>')
    razas = razas.replace('<h2>¿Por la Alianza o por la Horda?</h2><p class="muted">Elige tu raza: raciales, macros y clases disponibles en Forever.</p>',
                          '<div class="divider"><h2>¿Alianza u Horda?</h2></div><p class="sub">Raciales de cada raza, con su macro y las clases que puede jugar.</p>')
    hero = ('<section class="hero"><p class="eyebrow">GUÍA PVP · NIVEL 30 + LEGACY</p><h1>WoW Forever</h1>'
            '<p class="lead">Builds, macros y duelos para las nueve clases: todo lo que necesitas para tus duelos, BGs y el mundo abierto.</p>'
            '<div class="actions"><a class="btn gold" href="#clases">Elegir clase</a><a class="btn ghost" href="calculadora/">Calculadora de talentos</a></div>'
            '<p class="hello">¡Buenas, Muchamiel y comunidad! Vengas de Twitch, YouTube o Kick, bienvenido a Azeroth.</p></section>')
    tiles = ('<div class="divider"><h2>Herramientas</h2></div><p class="sub">Menos clics, más atención al combate.</p><div class="tiles">'
             '<a class="tile" href="calculadora/"><strong>Calculadora</strong><span>Talentos hasta nivel 60 y Legacy de 0 a 5. Comparte tu build con un enlace.</span></a>'
             '<a class="tile" href="comunes/"><strong>Macros comunes</strong><span>Foco, abalorios, vendas y las raciales de cada raza.</span></a>'
             '<a class="tile" href="warlock/#reglas"><strong>Reglas del torneo</strong><span>The Forever Open: apertura y prohibiciones.</span></a>'
             '<a class="tile" href="warlock/"><strong>El brujo de Muchamiel</strong><span>13 builds, 41 macros y duelos contra las nueve clases.</span></a></div>')
    comunidad = ('<div class="divider"><h2>Comunidad</h2></div><p class="sub">Si la guía te ayuda, pásate por el directo.</p>'
                 '<div class="community-grid">' + community + sorteo + '</div>' + directo)
    new = hero + clases + tiles + razas + comunidad
    return s[:main_start] + new + s[main_end:]


def class_page(s, slug):
    s = reorder_sections(s, CLASS_ORDER, open_id='builds')
    quick = '<div class="quick">' + ''.join(f'<a href="#{i}">{l}</a>' for i, l in CLASS_QUICK if f'id="{i}"' in s) + f'<a href="../calculadora/?class={slug}">Calculadora</a></div>'
    return re.sub(r'<div class="quick">.*?</div>', quick, s, count=1, flags=re.S)


def warlock_page(s):
    s = reorder_sections(s, WARLOCK_ORDER)
    nav, s = cut(s, r'<nav id="indice".*?</nav>')
    links = re.findall(r'<a href="#([^"]+)"><strong>\d+ · (.*?)</strong><span>(.*?)</span></a>', nav)
    rank = {sid: n for n, sid in enumerate(WARLOCK_ORDER)}
    links.sort(key=lambda l: rank.get(l[0], 99))
    cards = ''.join(f'<a href="#{sid}"><strong>{n:02d} · {t}</strong><span>{d}</span></a>' for n, (sid, t, d) in enumerate(links, 1))
    nav = re.sub(r'<div class="index">.*?</div>', '<div class="index">' + cards + '</div>', nav, flags=re.S)
    # El índice va justo debajo de la presentación, antes de la explicación larga.
    return s.replace('<h2>Por qué merece la pena usar estas macros</h2>', nav + '<h2>Por qué merece la pena usar estas macros</h2>', 1)


RACE_ES = {'Human': 'Humano', 'Dwarf': 'Enano', 'Night Elf': 'Elfo de la noche', 'Gnome': 'Gnomo', 'Orc': 'Orco',
           'Undead': 'No-muerto', 'Tauren': 'Tauren', 'Troll': 'Trol', 'Skyborne (High Order)': 'Skyborne', 'Skyborne (Windshaper)': 'Skyborne'}
ZAM = 'https://wow.zamimg.com/images/wow/icons/medium/'
RACES = {}
for _faction, _races in DATA['racials'].items():
    for _r in _races:
        RACES[race_slug(_r['race'])] = dict(_r, faction=_faction)
ABILITY_ICON = {a[0]: a[2] for r in RACES.values() for a in r['abilities']}
CLASS_KEY = {cls: (slug, name) for slug, name, cls, *_ in classes}

RACE_CSS = '''
.race-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(118px,1fr));gap:10px;margin-top:18px}
.race-tile{display:flex;flex-direction:column;align-items:center;gap:5px;padding:14px 8px 12px;text-align:center;text-decoration:none;border:1px solid #ffffff1f;border-radius:8px;background:#00000059;transition:border-color .15s,transform .15s,background .15s}
.race-tile:hover{border-color:var(--gold);background:#ffffff0d;transform:translateY(-2px)}
.race-tile .race{width:64px;height:64px;border-radius:10px;border:2px solid #c99a3c;box-shadow:0 4px 14px #000a}
.faction.horde .race-tile .race{border-color:#c4543f}
.faction.alliance .race-tile .race{border-color:#4f86c9}
.race-tile b{font:700 15px "Cinzel",Georgia,serif;color:var(--gold);line-height:1.2}
.race-tile small{color:#98a3b6;font-size:12px;line-height:1.2}
.race-classes{display:flex;flex-wrap:wrap;justify-content:center;gap:3px;margin-top:4px}
.race-classes img{width:18px;height:18px;border-radius:3px;border:1px solid #0008}
.race-chips{display:flex;flex-wrap:wrap;gap:8px}
.race-chip{display:inline-flex;align-items:center;gap:9px;padding:7px 12px 7px 7px;border:1px solid #4b4330;border-radius:6px;background:#141a25;text-decoration:none}
.race-chip:hover{border-color:var(--gold);color:var(--gold)}
.race-chip img,.class-chip img{width:30px;height:30px;border-radius:5px}
.quick a.class-chip{display:inline-flex;align-items:center;gap:8px;padding:5px 12px 5px 5px}
h3.ability{display:flex;align-items:center;gap:12px;margin-top:22px}
h3.ability img{width:40px;height:40px;border-radius:6px;border:1px solid #c99a3c;box-shadow:0 2px 8px #0009}
summary .sum-icon{width:28px;height:28px;border-radius:5px;vertical-align:middle;margin-right:10px}
@media(max-width:520px){.race-grid{grid-template-columns:repeat(2,1fr)}}
'''


def race_icon(r, base):
    # Skyborne no tiene icono local: retrato oficial del CDN de Wowhead (High Order masculino, Windshaper femenino).
    if r['icon'] == 'race_skyborne':
        return 'https://wow.zamimg.com/images/wow/icons/large/race_skyborne_' + ('male' if 'High Order' in r['race'] else 'female') + '.jpg'
    return image(r['icon'], base + 'assets/')


def race_tiles(faction, base):
    tiles = ''
    for r in DATA['racials'][faction]:
        slug = race_slug(r['race'])
        sub = r['race'] if RACE_ES[r['race']] != r['race'] else ''
        if r['race'].startswith('Skyborne'):
            sub = re.search(r'\((.*)\)', r['race'])[1]
        icons = ''.join(f'<img src="{base}assets/{CLASS_KEY[c][0]}.jpg" alt="{E(CLASS_KEY[c][1])}" title="{E(CLASS_KEY[c][1])}">' for c in r['classes'])
        tiles += (f'<a class="race-tile" href="{base}razas/{slug}/"><img class="race" src="{race_icon(r, base)}" alt="">'
                  f'<b>{E(RACE_ES[r["race"]])}</b>' + (f'<small>{E(sub)}</small>' if sub else '') + f'<span class="race-classes">{icons}</span></a>')
    return '<div class="race-grid">' + tiles + '</div>'


def race_icons(s, file, base):
    rel = file.relative_to(dist).parts
    section = rel[0] if len(rel) > 1 else ''
    s = re.sub(r'<style id="race-icons">.*?</style>', '', s, flags=re.S)
    s = s.replace('</head>', '<style id="race-icons">' + RACE_CSS + '</style></head>', 1)
    # Portada y /razas/: fichas grandes por raza, con las clases que puede jugar.
    for faction in ['Alliance', 'Horde']:
        s = re.sub(r'(<article class="faction ' + faction.lower() + r'">.*?</h2>)(<div class="race-list">.*?</div>|<div class="race-grid">.*?</div>)(</article>)',
                   lambda m: m[1] + race_tiles(faction, base) + m[3], s, flags=re.S)
    # Sección «Raciales» de cada clase: iconos que llevan a la página de la raza.
    def chip(m):
        r = RACES[m[1]]
        label = r['race'].replace('(', '').replace(')', '') if r['race'].startswith('Skyborne') else RACE_ES[r['race']]
        return f'<a class="race-chip" href="../razas/{m[1]}/"><img src="{race_icon(r, base)}" alt="">{E(label)}</a>'
    s = re.sub(r'<div class="quick">((?:<a href="\.\./comunes/#race-[a-z-]+">[^<]+</a>)+)</div>',
               lambda m: '<div class="race-chips">' + re.sub(r'<a href="\.\./comunes/#race-([a-z-]+)">[^<]+</a>', chip, m[1]) + '</div>', s)
    s = re.sub(r'<a class="race-chip" href="\.\./razas/([a-z-]+)/"><img[^>]*>[^<]*</a>', chip, s)
    # Macros comunes: icono de la raza en cada desplegable.
    s = re.sub(r'<img class="sum-icon" src="[^"]*" alt="">', '', s)
    s = re.sub(r'(<details class="entry" id="race-([a-z-]+)"><summary>)',
               lambda m: m[1] + f'<img class="sum-icon" src="{race_icon(RACES[m[2]], base)}" alt="">', s)
    if section == 'razas' and len(rel) == 3:
        s = re.sub(r'(?:\.\./)*assets/skyborne\.svg', race_icon(RACES[rel[1]], base), s)
    # Raciales: icono de cada habilidad (mismo CDN de Wowhead que la calculadora).
    s = re.sub(r'<h3>([^<]+)</h3>', lambda m: (f'<h3 class="ability"><img loading="lazy" src="{ZAM}{ABILITY_ICON[html.unescape(m[1])]}.jpg" alt="">{m[1]}</h3>'
                                               if html.unescape(m[1]) in ABILITY_ICON else m[0]), s)
    # Páginas de raza: clases con su icono.
    if section == 'razas' and len(rel) == 3:
        s = re.sub(r'<a href="\.\./\.\./([a-z]+)/">([^<]+)</a>', lambda m: (f'<a class="class-chip" href="../../{m[1]}/"><img src="../../assets/{m[1]}.jpg" alt="">{m[2]}</a>'
                                                                         if m[1] in NAMES else m[0]), s)
    return s


def run():
    assert (dist / 'assets' / 'fonts' / 'cinzel.woff2').exists(), 'falta assets/fonts/cinzel.woff2'
    for file in sorted(dist.rglob('*.html')):
        rel = file.relative_to(dist).parts
        s = file.read_text(encoding='utf-8')
        base = depth_prefix(file)
        section = rel[0] if len(rel) > 1 else ''
        current, calc_q = {'': 'inicio', 'calculadora': 'calculadora', 'razas': 'razas', 'comunes': 'comunes', 'macros': 'comunes', 'noticias': 'noticias',
                           'sorteos': 'sorteos', 'zona-subs': 'muchamiel', 'muchamiel': 'muchamiel', 'torneo': 'torneo', 'colaboraciones': 'colaboraciones', 'addons': 'addons', 'beta-gratis': 'noticias', 'reserva-nombres': 'noticias', 'mazmorras-nuevas': 'noticias', 'bandas-forever': 'noticias', 'fin-beta': 'noticias', 'a-medias': 'noticias', 'raciales-forever': 'noticias', 'dia-1': 'noticias', 'novedades-29-octubre': 'noticias', 'calendario': 'calendario',**{k: k for k, _ in FOREVER_PAGES},
                           'clases': 'clases'}.get(section, 'clases'), ''
        if section in NAMES:
            calc_q = '?class=' + section
        if section == 'retail':  # Van 17-10: apartado WoW Retail
            sub = rel[1] if len(rel) > 2 else ''
            current = 'r-' + (sub or 'inicio')
        modo = 'retail' if section == 'retail' else ('auto' if section in MODO_COMPARTIDO else 'forever')
        s = s.replace('<html lang="es"', f'<html lang="es" data-modo="{modo}"' + (' class="modo-retail"' if modo == 'retail' else ''), 1)
        if 'id="modo-js"' not in s:
            s = s.replace('<head>', '<head>' + MODO_JS, 1)
        s = re.sub(r'<header\b.*?</header>', header(base, current, calc_q), s, count=1, flags=re.S)
        s = set_style(s, base)
        if section == '':
            s = home(s)
        elif section == 'retail':
            s = set_crumbs(s, crumbs(base, [('WoW Retail', None if not sub else base + 'retail/')] + ([(RETAIL_NOMBRES.get(sub, sub), None)] if sub else [])))
        elif section in NAMES:
            s = class_page(s, section)
            s = set_crumbs(s, crumbs(base, [('Clases', base + 'clases/'), (NAMES[section], None)]))
        elif section == 'razas':
            trail = [('Razas', None)] if len(rel) == 2 else [('Razas', '../'), (RACES[rel[1]]['race'], None)]
            s = set_crumbs(s, crumbs(base, trail))
        elif section == 'macros':
            s = set_crumbs(s, crumbs(base, [('Macros', base + 'comunes/'), (NAMES.get(rel[1], rel[1]) if len(rel) > 2 else 'Macros', None)]))
        elif section == 'comunes':
            s = set_crumbs(s, crumbs(base, [('Macros', None)]))
        elif section == 'calculadora':
            s = set_crumbs(s, crumbs(base, [('Calculadora de talentos', None)]))
        elif section in dict(FOREVER_PAGES):
            s = set_crumbs(s, crumbs(base, [('WoW Forever', None if section == 'lanzamiento' else base + 'lanzamiento/')] + ([] if section == 'lanzamiento' else [(dict(FOREVER_PAGES)[section], None)])))
        elif section == 'mazmorras-nuevas':
            s = set_crumbs(s, crumbs(base, [('Noticias', base + 'noticias/'), ('Las 9 mazmorras nuevas', None)]))
        elif section == 'bandas-forever':
            s = set_crumbs(s, crumbs(base, [('Noticias', base + 'noticias/'), ('Las bandas y Onyxia', None)]))
        elif section == 'novedades-29-octubre':
            s = set_crumbs(s, crumbs(base, [('Noticias', base + 'noticias/'), ('Parches cada 4 meses', None)]))
        elif section == 'dia-1':
            s = set_crumbs(s, crumbs(base, [('Noticias', base + 'noticias/'), ('Día 1 en Forever', None)]))
        elif section == 'raciales-forever':
            s = set_crumbs(s, crumbs(base, [('Noticias', base + 'noticias/'), ('Cambian las raciales', None)]))
        elif section == 'a-medias':
            s = set_crumbs(s, crumbs(base, [('Noticias', base + 'noticias/'), ('A medias', None)]))
        elif section == 'fin-beta':
            s = set_crumbs(s, crumbs(base, [('Noticias', base + 'noticias/'), ('Fin de la beta', None)]))
        elif section == 'reserva-nombres':
            s = set_crumbs(s, crumbs(base, [('Noticias', base + 'noticias/'), ('Reserva de nombres', None)]))
        elif section == 'beta-gratis':
            s = set_crumbs(s, crumbs(base, [('Noticias', base + 'noticias/'), ('Prueba de estrés: 21 de octubre a las 19:00', None)]))
        elif section in ('addons', 'noticias', 'sorteos', 'muchamiel', 'torneo', 'colaboraciones', 'clases'):
            s = set_crumbs(s, crumbs(base, [({'noticias': 'Noticias', 'sorteos': 'Sorteos', 'muchamiel': 'Muchamiel', 'torneo': 'The Forever Open',
                                               'colaboraciones': 'Colaboraciones', 'clases': 'Clases', 'addons': 'Addons'}[section], None)]))
        s = race_icons(s, file, base)
        file.write_text(s, encoding='utf-8')


if __name__ == '__main__':
    run()
    package()
    print('Portal oficializado y empaquetado.')
