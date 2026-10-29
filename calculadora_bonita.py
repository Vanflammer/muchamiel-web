"""Calculadora más digna (Van, 15-10-2026): «se ve fea, no tiene las cosas centradas; no se ven las conexiones de talentos».
No toca la lógica de GPT (calculator.js): añade botones de clase con icono, centra y ordena la página, colorea los árboles
con el color de la clase y dibuja las flechas de requisitos (qué talento obliga a cuál) a partir de los datos (`req`)."""
import re, html, json, urllib.parse

LEAD = ('<p class="lead calc-lead">Elige tu clase, reparte los puntos en sus tres ramas y comparte la build con un enlace. '
        'Del nivel 10 al 60, con los puntos extra del Legado. Para quitar un punto, clic derecho o Shift + clic.</p>')

CSS = '''
.calc-page>.eyebrow,.calc-page>h1,.calc-page>.calc-lead,.calc-page>p,.calc-page>h2{text-align:center}
.calc-page>.calc-lead{max-width:760px;margin:0 auto 6px}
.calc-classes{display:flex;flex-wrap:wrap;justify-content:center;gap:10px;margin:22px auto 18px;max-width:1000px}
.calc-classes button{--cc:#c99a3c;display:flex;flex-direction:column;align-items:center;gap:6px;width:96px;padding:12px 6px 10px;border:1px solid #2c3444;border-radius:12px;
 background:linear-gradient(170deg,#171d29,#0b0f16);color:#cfd6e3;font:700 12.5px "Segoe UI",sans-serif;letter-spacing:.02em;cursor:pointer;transition:transform .15s,border-color .15s,box-shadow .15s}
.calc-classes button img{width:46px;height:46px;border-radius:50%;border:2px solid #3a4253;transition:border-color .15s}
.calc-classes button:hover{transform:translateY(-2px);border-color:var(--cc)}
.calc-classes button.on{border-color:var(--cc);color:#fff;box-shadow:0 0 0 1px var(--cc),0 0 22px color-mix(in srgb,var(--cc) 45%,transparent);background:linear-gradient(170deg,color-mix(in srgb,var(--cc) 22%,#171d29),#0b0f16)}
.calc-classes button.on img{border-color:var(--cc)}
.calc-page .calc-toolbar{justify-content:center;align-items:center;gap:10px 14px;max-width:980px;margin:0 auto 12px;padding:14px 18px;border-radius:12px;
 background:linear-gradient(170deg,#141a26,#0b0f16);border:1px solid #3b3222;box-shadow:0 8px 24px #0006}
.calc-page .calc-toolbar label{color:#b6c0d0;font-size:13.5px}
.calc-page .calc-toolbar input[type=number]{width:62px;padding:7px 8px;border-radius:6px;border:1px solid #3a4253;background:#0b0f16;color:#fff;text-align:center;font-weight:700}
.calc-page .calc-toolbar input[type=checkbox]{accent-color:#c99a3c}
.calc-page #count{order:-1;flex-basis:100%;text-align:center;font:900 22px "Cinzel",Georgia,serif;color:var(--gold);margin-bottom:2px}
.calc-page .calc-toolbar button,.calc-page .calc-toolbar #guide-link{padding:8px 14px;border-radius:6px;border:1px solid #4b4330;background:#1a2130;color:#eef2f8;font-weight:600;font-size:13.5px;text-decoration:none;cursor:pointer}
.calc-page .calc-toolbar button:hover,.calc-page .calc-toolbar #guide-link:hover{border-color:var(--gold);color:#ffe7a6}
.calc-page .calc-toolbar #share{background:linear-gradient(#5b3c0c,#2d1d05);border-color:#e8b84a;color:#ffe7a6}
.calc-page .calc-toolbar label[for=class-select],.calc-page #class-select{position:absolute!important;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.calc-page #required-level{font:700 16px "Cinzel",Georgia,serif;color:#ffe7a6;margin:6px 0 4px}
.calc-page>p:not([class]){color:#9aa5b8;font-size:13.5px;max-width:760px;margin-left:auto;margin-right:auto}
.calc-page>details.entry{max-width:980px;margin:10px auto}
.calc-page #message{min-height:1.4em}
.calc-page .trees{gap:16px;margin-top:14px}
.calc-page .tree{position:relative;border:1px solid #2c3444;border-top:3px solid var(--cc,#c99a3c);border-radius:12px;padding:16px 12px 18px;
 background:radial-gradient(ellipse at 50% 0%,color-mix(in srgb,var(--cc,#c99a3c) 14%,transparent),transparent 60%),linear-gradient(170deg,#161c28,#0a0d13)}
.calc-page .tree h2{display:flex;align-items:center;justify-content:center;gap:10px;margin:0 0 14px;color:var(--cc,#f4d27a);font-size:20px}
.calc-page .tree h2 img{width:30px;height:30px;border-radius:6px;border:1px solid var(--cc,#c99a3c)}
.calc-page .talent-grid{position:relative;justify-content:center}
.calc-page .talent-grid>svg.req-lines{position:absolute;inset:0;pointer-events:none;overflow:visible;z-index:0}
.calc-page .talent-grid>.talent{position:relative;z-index:1}
/* Van 15-10: con puntos, encendidos (verde; dorado al máximo); sin puntos, apagados */
.calc-page .talent{transition:border-color .15s,box-shadow .15s,background .15s}
.calc-page .talent:not(.has-pts) img{filter:grayscale(1) brightness(.55);transition:filter .15s}
.calc-page .talent:not(.has-pts){border-color:#323a4a;background:#0a0e15}
.calc-page .talent:not(.has-pts):hover img{filter:grayscale(.4) brightness(.85)}
.calc-page .talent.has-pts{border-color:#3ddc84;background:linear-gradient(170deg,#12301f,#0b1410);box-shadow:0 0 0 1px #3ddc8466,0 0 12px #3ddc8444}
.calc-page .talent.has-pts.maxed{border-color:#f4d27a;background:linear-gradient(170deg,#3a2c0e,#120d05);box-shadow:0 0 0 1px #f4d27a88,0 0 16px #e8b84a66}
.calc-page #detail{display:none}
.calc-tip{display:none;position:fixed;z-index:60;max-width:360px;padding:12px 14px;border:1px solid #c99a3c;border-radius:8px;background:linear-gradient(170deg,#141a26fa,#07090efa);
 box-shadow:0 12px 30px #000c;color:#dfe5ee;font-size:13.5px;line-height:1.45;pointer-events:none}
.calc-tip h3{margin:0 0 4px;font:700 16px "Cinzel",Georgia,serif;color:#ffe7a6}.calc-tip .meta{margin:0 0 8px;color:#9aa5b8;font-size:12.5px}
.calc-tip p{margin:0 0 6px}.calc-tip p.cur{color:#7ee0a0}.calc-tip b{color:#e8b84a}.calc-tip p.cur b{color:#3ddc84}
@media(max-width:700px){.calc-tip{max-width:none}}
.calc-page .calc-detail,.calc-page .calc-share,.calc-page .calc-links{max-width:980px;margin-left:auto;margin-right:auto}
.calc-page .calc-links{justify-content:center}
@media(max-width:700px){.calc-classes button{width:78px;font-size:11.5px}.calc-classes button img{width:38px;height:38px}}
/* Moderador de Muchamiel (15-10): todo más compacto (Van: la barra no flota, baja con la página) */
.calc-page>.calc-lead{font-size:15px;margin-bottom:4px}
.calc-sticky{position:relative;z-index:5;max-width:1000px;margin:10px auto 12px;padding:10px 12px 8px;border:1px solid #3b3222;border-radius:12px;
 background:linear-gradient(170deg,#141a26f7,#0b0f16f7);box-shadow:0 10px 26px #000b;backdrop-filter:blur(4px)}
.calc-sticky .calc-classes{margin:0 auto 8px;gap:6px}
.calc-sticky .calc-classes button{flex-direction:row;width:auto;gap:6px;padding:5px 10px 5px 6px;border-radius:999px;font-size:12.5px}
.calc-sticky .calc-classes button img{width:24px;height:24px;border-width:1px}
.calc-sticky .calc-classes button:hover{transform:none}
.calc-page .calc-sticky .calc-toolbar{margin:0 auto;padding:0;border:0;background:none;box-shadow:none;gap:8px 12px}
.calc-page .calc-sticky #count{flex-basis:auto;order:0;font-size:18px;margin:0 6px 0 0}
.calc-page .calc-sticky .calc-toolbar input[type=number]{width:54px;padding:5px 6px}
.calc-page .calc-sticky .calc-toolbar button,.calc-page .calc-sticky .calc-toolbar #guide-link{padding:6px 11px;font-size:13px}
.calc-page .calc-sticky #required-level{margin:6px 0 0;font-size:13.5px;text-align:center}
.calc-page .calc-sticky #message{position:fixed;z-index:60;left:50%;bottom:18px;transform:translateX(-50%);margin:0;padding:6px 14px;max-width:min(92%,560px);border:1px solid #6b5a2e;border-radius:999px;background:#0b0f16f2;box-shadow:0 6px 18px #000a;font-size:13px;text-align:center;color:#ffe7a6;pointer-events:none;opacity:0;transition:opacity .25s}
.calc-page .calc-sticky #message.on{opacity:1}
.calc-page #required-level{display:none!important}
@media(max-width:700px){.calc-page .calc-sticky{position:relative}}
.calc-page .calc-share-off{position:fixed!important;left:-9999px;top:0;width:300px;opacity:0;pointer-events:none}
.calc-page .calc-lead #guide-link{color:#ffe7a6;font-weight:700;white-space:nowrap}
.calc-page #share{border-color:#6b5a2e;background:#2a200c;color:#ffe7a6}
.calc-page>details.entry{margin-top:18px}
@media(max-width:700px){.calc-sticky{position:static}.calc-sticky .calc-classes button{font-size:0;padding:4px}.calc-sticky .calc-classes button img{width:30px;height:30px}}
'''

JS = r'''(function(){
var msgEl=document.getElementById('message'),msgT;if(msgEl)new MutationObserver(function(){clearTimeout(msgT);if(!msgEl.textContent.trim()){msgEl.classList.remove('on');return}msgEl.classList.add('on');msgT=setTimeout(function(){msgEl.classList.remove('on')},2600)}).observe(msgEl,{childList:true,characterData:true,subtree:true});
function hdr(){var h=document.querySelector('header.site');if(h)document.documentElement.style.setProperty('--hdr',h.offsetHeight+'px')}hdr();window.addEventListener('resize',hdr);
var D=JSON.parse(document.getElementById('talent-data').textContent);
var sel=document.getElementById('class-select'),page=document.querySelector('.calc-page'),box=document.querySelector('.calc-classes');
var col={};D.classes.forEach(function(c){col[c.key]=c.color});
box.querySelectorAll('button').forEach(function(b){b.style.setProperty('--cc',col[b.dataset.cls]);
 b.addEventListener('click',function(){if(sel.value===b.dataset.cls)return;sel.value=b.dataset.cls;sel.dispatchEvent(new Event('change',{bubbles:true}));sync()})});
function sync(){var k=sel.value;box.querySelectorAll('button').forEach(function(b){var on=b.dataset.cls===k;b.classList.toggle('on',on);b.setAttribute('aria-pressed',on)});
 page.style.setProperty('--cc',col[k]);draw()}
var NS='http://www.w3.org/2000/svg';
function draw(){var k=sel.value,trees=(D.talents[k]||{}).trees||[];
 document.querySelectorAll('#trees .tree').forEach(function(tree,i){var t=trees[i];if(!t)return;var h=tree.querySelector('h2');
  if(h&&!h.querySelector('img')&&t.icon){var im=document.createElement('img');im.alt='';im.src='https://wow.zamimg.com/images/wow/icons/medium/'+t.icon+'.jpg';h.prepend(im)}
  var g=tree.querySelector('.talent-grid');if(!g)return;
  g.querySelectorAll('.talent').forEach(function(el){var b=el.querySelector('button.add'),m=/(\d+)\/(\d+)/.exec(b&&b.title||'');el.classList.toggle('has-pts',!!m&&m[1]!=='0')});var svg=g.querySelector('svg.req-lines');
  if(!svg){svg=document.createElementNS(NS,'svg');svg.setAttribute('class','req-lines');svg.setAttribute('aria-hidden','true');g.prepend(svg)}
  while(svg.firstChild)svg.removeChild(svg.firstChild);var gr=g.getBoundingClientRect();
  var defs=document.createElementNS(NS,'defs');['on','off'].forEach(function(s){var m=document.createElementNS(NS,'marker');m.setAttribute('id','ah-'+s+i);m.setAttribute('viewBox','0 0 10 10');m.setAttribute('refX','8');m.setAttribute('refY','5');
   m.setAttribute('markerWidth','5');m.setAttribute('markerHeight','5');m.setAttribute('orient','auto-start-reverse');var p=document.createElementNS(NS,'path');p.setAttribute('d','M0 0L10 5L0 10z');p.setAttribute('fill',s==='on'?'#ffd97a':'#9aa3b5');m.append(p);defs.append(m)});svg.append(defs);
  t.talents.forEach(function(x){if(!x.req)return;var b=g.querySelector('button.add[data-name="'+CSS.escape(x.name)+'"]'),a=g.querySelector('button.add[data-name="'+CSS.escape(x.req)+'"]');if(!a||!b)return;
   var ra=a.getBoundingClientRect(),rb=b.getBoundingClientRect(),m=/(\d+)\/(\d+)/.exec(a.title||''),done=m&&m[1]===m[2]&&m[1]!=='0';
   var ax=ra.left+ra.width/2-gr.left,ay=ra.bottom-gr.top,bx=rb.left+rb.width/2-gr.left,by=rb.top-gr.top,d;
   if(Math.abs(ra.top-rb.top)<4){var y=ra.top+ra.height/2-gr.top;d=bx>ax?'M'+(ra.right-gr.left)+' '+y+'H'+(rb.left-gr.left-2):'M'+(ra.left-gr.left)+' '+y+'H'+(rb.right-gr.left+2)}
   else if(Math.abs(ax-bx)<4){d='M'+ax+' '+ay+'V'+(by-2)}
   else{var y2=ra.top+ra.height/2-gr.top;d='M'+(bx>ax?ra.right-gr.left:ra.left-gr.left)+' '+y2+'H'+bx+'V'+(by-2)}
   var p=document.createElementNS(NS,'path');p.setAttribute('d',d);p.setAttribute('fill','none');p.setAttribute('stroke',done?'#ffd97a':'#9aa3b5');p.setAttribute('stroke-width','3');
   p.setAttribute('stroke-linecap','round');if(done)p.setAttribute('style','filter:drop-shadow(0 0 4px #e8b84a)');p.setAttribute('marker-end','url(#ah-'+(done?'on':'off')+i+')');svg.append(p)})})}
// Van 15-10: el detalle del talento, en ventana emergente junto al talento (sustituye al recuadro de abajo).
var tip=document.createElement('div');tip.className='calc-tip';tip.setAttribute('role','tooltip');document.body.appendChild(tip);
function esc(x){return String(x).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
var FILA=' · fila ',REQ=' · requiere ',PREV=' puntos en filas anteriores',MAXI=' al máximo',RANGO=document.documentElement.lang==='en'?'Rank ':'Rango ',ACT=' · actual';
function showTip(b){if(!b)return;var k=sel.value,i=+b.dataset.tree,tr=((D.talents[k]||{}).trees||[])[i];if(!tr)return;
 var t=tr.talents.find(function(x){return x.name===b.dataset.name});if(!t)return;var m=/(\d+)\/(\d+)/.exec(b.title||''),r=m?+m[1]:0;
 var h='<h3>'+esc(t.name)+' · '+r+'/'+t.max+'</h3><p class="meta">'+esc(tr.name)+FILA+t.row+REQ+((t.row-1)*5)+PREV+(t.req?'; '+esc(t.req)+MAXI:'')+'.</p>';
 (t.desc||[]).forEach(function(d,j){var cur=j+1===r;h+='<p'+(cur?' class="cur"':'')+'><b>'+RANGO+(j+1)+(cur?ACT:'')+':</b> '+esc(d)+'</p>'});
 tip.innerHTML=h;tip.style.display='block';var rb=b.getBoundingClientRect(),tw=tip.offsetWidth,th=tip.offsetHeight,vw=innerWidth,vh=innerHeight;
 if(vw<700){tip.style.left='8px';tip.style.right='8px';tip.style.top='auto';tip.style.bottom='8px';return}
 tip.style.right='auto';tip.style.bottom='auto';var x=rb.right+12;if(x+tw>vw-8)x=rb.left-tw-12;if(x<8)x=8;
 var y=rb.top;if(y+th>vh-8)y=vh-th-8;if(y<8)y=8;tip.style.left=x+'px';tip.style.top=y+'px'}
function hideTip(){tip.style.display='none'}
var trees=document.getElementById('trees'),last=null;
trees.addEventListener('mouseover',function(e){var b=e.target.closest('button.add');if(b){last=b;showTip(b)}});
trees.addEventListener('mouseleave',hideTip);
trees.addEventListener('focusin',function(e){var b=e.target.closest('button.add');if(b){last=b;showTip(b)}});
trees.addEventListener('click',function(e){var b=e.target.closest('button.add, .talent button');if(!b)return;var n=b.dataset.name||(last&&last.dataset.name),i=b.dataset.tree||(last&&last.dataset.tree);
 requestAnimationFrame(function(){var nb=trees.querySelector('button.add[data-tree="'+i+'"][data-name="'+CSS.escape(n||'')+'"]');if(nb){last=nb;showTip(nb)}})});
document.addEventListener('click',function(e){if(!e.target.closest('#trees'))hideTip()});
window.addEventListener('scroll',function(){if(innerWidth>=700)hideTip()},{passive:true});
var pend=0;function later(){if(pend)return;pend=requestAnimationFrame(function(){pend=0;sync()})}
new MutationObserver(later).observe(document.getElementById('trees'),{childList:true,subtree:true,attributes:true,attributeFilter:['title','class']});
sel.addEventListener('change',later);window.addEventListener('resize',later);later();
})();'''


def apply(s, classes):
    """s: HTML de calculadora/index.html (castellano). classes: [(slug, nombre, …)] de crear_portal."""
    a = s.index('<p class="eyebrow">')
    b = s.index('<footer', a)
    keys = {'warrior': 'Warrior', 'paladin': 'Paladin', 'hunter': 'Hunter', 'rogue': 'Rogue', 'priest': 'Priest',
            'shaman': 'Shaman', 'mage': 'Mage', 'warlock': 'Warlock', 'druid': 'Druid'}
    chips = '<div class="calc-classes" role="group" aria-label="Clase">' + ''.join(
        f'<button type="button" data-cls="{keys[slug]}"><img src="../assets/{slug}.jpg" alt="">{name}</button>' for slug, name, *_ in classes) + '</div>'
    body = s[a:b]
    body = re.sub(r'(<h1>.*?</h1>)', lambda m: m[1] + LEAD, body, count=1, flags=re.S)
    # Moderador de Muchamiel (15-10): clases, puntos y reiniciar juntos y siempre a la vista; builds de ejemplo debajo.
    tool0 = tool = re.search(r'<div class="calc-toolbar">.*?</div>', body, re.S)[0]
    req = re.search(r'<p id="required-level"[^>]*>.*?</p>', body, re.S)[0]
    msg = re.search(r'<p class="calc-message" id="message"[^>]*>.*?</p>', body, re.S)[0]
    presets = re.search(r'<details class="entry"><summary>Builds de ejemplo.*?</details>', body, re.S)[0]
    guide = re.search(r'<a id="guide-link"[^>]*>.*?</a>', tool, re.S)[0]
    help_p = re.search(r'<p>Haz clic o toca para añadir\..*?</p>', body, re.S)[0]
    for x in (req, msg, presets, help_p):
        body = body.replace(x, '', 1)
    tool = tool.replace(guide, '', 1).replace('>Copiar enlace<', '>🔗 Compartir build<', 1)
    req = req.replace('<p id="required-level"', '<p hidden id="required-level"', 1)
    body = body.replace(tool0, '<div class="calc-sticky">' + chips + tool + req + msg + '</div>', 1)
    body = body.replace('<div class="calc-share">', '<div id="presets" hidden></div><div class="calc-share">', 1)
    body = body.replace('<div class="calc-share">', '<div class="calc-share calc-share-off" aria-hidden="true">', 1)
    body = body.replace(LEAD, LEAD.replace('</p>', ' ' + guide.replace('>Guía de clase<', '>Ver la guía de la clase →<') + '</p>'), 1)
    body = body.replace('WOW FOREVER · NIVELES 10–60 + LEGACY', 'WOW FOREVER · TALENTOS DEL 10 AL 60 + LEGADO', 1)
    s = s[:a] + '<div class="calc-page">' + body + '</div>' + s[b:]
    s = s.replace('</head>', '<style id="calc-bonita">' + CSS + '</style></head>', 1)
    # Van 15-10: «ya no es para el torneo, es para todo»: sin límite de nivel 30 ni Legado por defecto (cada uno pone lo suyo).
    s = s.replace('id="max-level" type="number" min="10" max="60" value="30"', 'id="max-level" type="number" min="10" max="60" value="60"', 1)
    s = s.replace('<input type="checkbox" id="legacy-check" checked>', '<input type="checkbox" id="legacy-check">', 1)
    s = s.replace('id="legacy-points" type="number" min="0" max="5" value="5"', 'id="legacy-points" type="number" min="0" max="5" value="0"', 1)
    s = s.replace('<script src="calculator.js">', '<script src="calculator.js?v=20261015b">', 1)  # que nadie se quede con el JS viejo en caché
    return s.replace('</body>', '<script>' + JS + '</script></body>', 1)


def patch_js(path):
    """calculator.js de GPT: por defecto nivel 60 y Legado desactivado con 0 puntos (Van, 15-10). Lo guardado con la clave
    antigua (v1, cuando el defecto era 30 + 5 de Legado) solo aporta las builds; nivel y Legado se guardan ya en v2."""
    js = path.read_text(encoding='utf-8')
    R = [
        ('let level=30,legacy=5,useLegacy=true,', 'let level=60,legacy=0,useLegacy=false,'),
        ("'Enlace copiado.'", "'Enlace copiado: pégalo en el chat.'"),
        ("localStorage.setItem('forever-talents-v1',", "localStorage.setItem('forever-talents-v2',"),
        ("const saved=JSON.parse(localStorage.getItem('forever-talents-v1')||'null');if(saved){Object.assign(cache,saved.cache||{});"
         "level=Math.max(10,Math.min(60,Number(saved.level)||30));legacy=Math.max(0,Math.min(5,Number(saved.legacy)||0));useLegacy=!!saved.useLegacy;",
         "const v2=JSON.parse(localStorage.getItem('forever-talents-v2')||'null'),saved=v2||JSON.parse(localStorage.getItem('forever-talents-v1')||'null');"
         "if(saved){Object.assign(cache,saved.cache||{});if(v2){level=Math.max(10,Math.min(60,Number(saved.level)||60));"
         "legacy=Math.max(0,Math.min(5,Number(saved.legacy)||0));useLegacy=!!saved.useLegacy;}"),
    ]
    for a, b in R:
        assert a in js, 'calculator.js cambió: ' + a[:50]
        js = js.replace(a, b, 1)
    path.write_text(js, encoding='utf-8')


def guide_links(s, slug, data):
    """Guía de cada clase: en cada build de ejemplo, botón que abre la calculadora con esa build cargada (Van, 15-10).
    Son builds de 26 puntos: nivel 30 + 5 de Legado. Mismo formato de enlace que «Copiar enlace» de la calculadora."""
    cls = next(c for c in data['classes'] if c['slug'] == slug)
    for i, b in enumerate(data['presets'].get(cls['key'], []), 1):
        m = re.search(rf'<details (?:class="entry" id="B{i}"|id="B{i}" class="entry")><summary>[^<]*</summary><div class="detail-body">', s)
        if not m:
            continue
        a = m[0]
        h = urllib.parse.quote(json.dumps({'c': cls['key'], 'l': 30, 'g': 5, 'e': True, 'a': b['allocation']}, separators=(',', ':'), ensure_ascii=False), safe="!'()*-._~")
        s = s.replace(a, a + f'<a class="btn calc-open" href="../calculadora/?class={slug}#{h}">Abrir en la calculadora con los puntos puestos</a>', 1)
    return s
