from pathlib import Path
import re, html, json

root=Path(__file__).resolve().parent
text=(root/'brujo-30-builds-y-macros.md').read_text(encoding='utf-8')
text=text.replace('tus 5 extra','5 extra de Legacy').replace('C + A sin A1','C + A2 + A3').replace('C sin mascotas + S','C sin mascotas + A2 + S')
text=text.replace('especialmente bombas, polvos de sueño, pociones de protección, world buffs y buffs de fogata','especialmente los objetos concretos del reglamento, polvos de sueño, pociones de protección, world buffs y buffs de fogata')
text=text.replace('## Cómo elegir',"Objetos prohibidos en la lista consultada: invocadores de mascotas no equipables (Spider Swarm y Compact Harvester Reaper Kit); Student Fodder; Flash Bomb; Magic Dust; Slumber Sand; Furbolg Medicine Pouch; Truthseeker's Bow; Green Whelp Armor; Goblin Sapper Charge; pociones de protección elemental; buffs y consumibles de eventos festivos; buffs de fogata; buffs temporales de objetivos o misiones del mundo. Dog Whistle figura como ejemplo permitido de invocador equipable. Solo buffs de tu propia clase. La prohibición de Flash Bomb y Sapper no equivale a prohibir todas las granadas.\n\n## Cómo elegir")
sources=[]
def inline(s):
    s=html.escape(s)
    def link(m):
        label,url=m.group(1),html.unescape(m.group(2))
        if (label,url) not in sources:sources.append((label,url))
        return '<a href="'+html.escape(url,quote=True)+'" target="_blank" rel="noopener noreferrer">'+label+'</a>'
    s=re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',link,s)
    s=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s)
    s=re.sub(r'(?<![\w">])([BCDATSR]\d+|DU\d+)(?![\w])',r'<a href="#\1">\1</a>',s)
    return s

def render(lines):
    out=[];i=0
    while i<len(lines):
        s=lines[i].strip()
        if not s:i+=1;continue
        if s.startswith('### '):
            title=s[4:];ident=title.split(' · ')[0];j=i+1
            while j<len(lines) and not lines[j].startswith('### '):j+=1
            out.append(f'<details id="{ident}" class="entry"><summary>{html.escape(title)}</summary><div class="detail-body"><a class="permalink" href="#{ident}">Enlace a {ident}</a>{render(lines[i+1:j])}</div></details>');i=j;continue
        if s.startswith('```'):
            j=i+1;code=[]
            while j<len(lines) and not lines[j].startswith('```'):code.append(lines[j]);j+=1
            out.append('<div class="macro"><button class="copy" type="button">Copiar macro</button><pre><code>'+html.escape('\n'.join(code))+'</code></pre></div>');i=j+1;continue
        if s.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                cells=lines[i].strip().strip('|').split('|')
                if not all(re.fullmatch(r'\s*[-:]+\s*',c) for c in cells):rows.append(cells)
                i+=1
            out.append('<div class="table-wrap"><table>'+''.join('<tr>'+''.join(('<th>' if n==0 else '<td>')+inline(c.strip())+('</th>' if n==0 else '</td>') for c in row)+'</tr>' for n,row in enumerate(rows))+'</table></div>');continue
        if s.startswith('- ') or re.match(r'^\d+\. ',s):
            ordered=bool(re.match(r'^\d+\. ',s));tag='ol' if ordered else 'ul';items=[]
            while i<len(lines) and (re.match(r'^\d+\. ',lines[i].strip()) if ordered else lines[i].strip().startswith('- ')):
                items.append('<li>'+inline(re.sub(r'^(?:- |\d+\. )','',lines[i].strip()))+'</li>');i+=1
            out.append('<'+tag+'>'+''.join(items)+'</'+tag+'>');continue
        para=[]
        while i<len(lines) and lines[i].strip() and not lines[i].startswith(('###','```','|','- ')):
            para.append(lines[i].strip());i+=1
        out.append('<p>'+inline(' '.join(para))+'</p>')
    return ''.join(out)

parts=re.split(r'^## ',text,flags=re.M)[1:]
labels=['Reglas del torneo','Elegir build','13 builds completas','Variantes de talentos','41 macros para copiar','Demonio según rival','Duelos por clase','BGs y mundo abierto','Equipo y referencias BiS','Habilidades por nivel','Prueba antes del torneo']
ids=['reglas','elegir','builds','variantes','macros','demonios','duelos','pvp','equipo','nivel','validacion']
counts=['Apertura y prohibiciones','Comparar estilos','26 puntos en cada reparto','Ajustes antes de fijar build','Comunes, talentos y raciales Undead','Control y supervivencia','Nueve rivales: build, demonio y plan','Builds, aliados y varios enemigos','Listas para contrastar','Qué puedes usar a nivel 30','Lista de comprobación']
assert len(parts)==len(ids)==len(labels)==len(counts)
sections=[]
for part,ident,label in zip(parts,ids,labels):
    title,body=part.split('\n',1)
    sections.append(f'<details id="{ident}" class="section"><summary><span>{label}</span><span class="expand">Abrir</span></summary><div class="section-body">'+render(body.splitlines())+'</div></details>')
sourcehtml='<details id="fuentes" class="section"><summary><span>Fuentes y enlaces</span><span class="expand">Abrir</span></summary><div class="section-body"><p>Información consultada el 9 de octubre de 2026. Las reglas y la beta pueden cambiar.</p><ul>'+''.join('<li><a target="_blank" rel="noopener noreferrer" href="'+html.escape(url,quote=True)+'">'+label+'</a></li>' for label,url in sources)+'</ul></div></details>'
nav=''.join(f'<a href="#{ident}"><strong>{n:02d} · {label}</strong><span>{desc}</span></a>' for n,(ident,label,desc) in enumerate(zip(ids,labels,counts),1))+'<a href="#fuentes"><strong>12 · Fuentes</strong><span>Blizzard, reglas, Wowhead Forever y más</span></a>'
intro='''<section class="intro" id="inicio"><p class="eyebrow">PARA MUCHAMIEL · THE FOREVER OPEN</p><h1>Brujo Forever<br><span>Duelos, BGs y mundo abierto.</span></h1><p class="meta">Undead · Nivel 30 · 26 puntos de talento · Cliente en inglés</p><h2>Por qué merece la pena usar estas macros</h2><p>En PvP, cada cambio de objetivo y cada clic en la barra de la mascota consume atención. Estas macros reúnen órdenes y te permiten elegir el destinatario con el ratón, el foco o una tecla modificadora. El beneficio es reaccionar con menos pasos y cometer menos errores mientras te mueves y vigilas al rival.</p><div class="benefits"><article><h3>Controlar sin perder el objetivo</h3><p>Fear y Seduction al foco, o Devour Magic bajo el ratón: mantienes al rival como objetivo mientras controlas o disipas donde hace falta. Evitas seleccionar, lanzar y volver a seleccionar.</p><a href="#C3">Ver Fear · C3</a></article><article><h3>Proteger tu demonio</h3><p>Retirarlo con una tecla y recuperarlo cuando proceda facilita mantenerlo vivo. En Soul Link, perderlo afecta a tu defensa: su manejo forma parte de tu supervivencia.</p><a href="#C1">Ver retirada · C1</a></article><article><h3>Reaccionar a tiempo</h3><p>La macro de Fear detiene tu lanzamiento actual para intentar el control al pulsarla. El acceso deliberado a escudos y sacrificios evita buscar el botón en un momento de presión.</p><a href="#D4">Ver escudo · D4</a></article><article><h3>No interrumpirte por repetir la tecla</h3><p>Las macros de drenaje evitan reiniciar esa canalización cuando vuelves a pulsar. Puedes concentrarte en posicionarte y observar al enemigo.</p><a href="#C8">Ver Drain Life · C8</a></article></div><div class="note"><strong>Qué esperar de ellas</strong><p>No aumentan el daño por sí solas ni deciden por ti. No eliminan el tiempo global de reutilización, el alcance, el maná ni los requisitos de talentos. Algunas detienen lanzamientos o tienen condiciones concretas: lee su explicación y ensáyalas. Las macros de esta guía todavía necesitan comprobarse dentro de la beta.</p></div><p class="start">Primera prueba sugerida: <a href="#B1">B1 · Soul Link + Corruption instantánea</a>. Aprende primero <a href="#C1">retirar mascota</a>, <a href="#C3">Fear</a>, <a href="#C4">foco</a>, <a href="#C12">Devour Magic</a> y <a href="#D1">Soul Link</a>, según tu demonio y talentos.</p></section>'''
css='''*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:80px}body{margin:0;background:#101015;color:#eeedf2;font:16px/1.65 "Segoe UI",sans-serif}a{color:#c1a4ff;text-decoration:underline;text-underline-offset:3px}a:hover{color:#fff}a:focus-visible,button:focus-visible,summary:focus-visible{outline:3px solid #b6ee8b;outline-offset:5px}header{position:sticky;top:0;background:#101015f2;border-bottom:1px solid #34303e;z-index:5;padding:15px 5%;display:flex;justify-content:space-between;gap:15px}header a{text-decoration:none}header strong{letter-spacing:.04em;color:#b6ee8b}main{max-width:1100px;margin:auto;padding:42px 24px 75px}.eyebrow{color:#b6ee8b;font-size:14px;letter-spacing:.13em;font-weight:700}h1{font-size:clamp(36px,6vw,60px);line-height:1.12;letter-spacing:-.025em;margin:12px 0 20px}h1 span{color:#b6a0d6}h2{font-size:26px;margin-top:32px}h3{font-size:18px;margin:0 0 10px}.intro>p{max-width:880px}.meta{color:#bdb7c9}.benefits{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin:24px 0}.benefits article{padding:22px;background:#1b1824;border-top:2px solid #9370ca}.benefits p{margin:0 0 14px}.note{border-left:3px solid #b6ee8b;padding:17px 22px;background:#18201a}.note p{margin:7px 0 0}.start{padding:16px 0}.index{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:22px 0 40px}.index a{display:flex;flex-direction:column;gap:3px;padding:17px 20px;border:1px solid #42364f;text-decoration:none;background:#19151f}.index a:hover{border-color:#c1a4ff;background:#241c30}.index span{color:#bdb7c9;font-size:14px}.section{border-top:1px solid #4e415b;margin:0 0 10px;scroll-margin-top:80px}summary{cursor:pointer;list-style:none}summary::-webkit-details-marker{display:none}.section>summary{display:flex;justify-content:space-between;gap:16px;font-size:22px;font-weight:650;padding:20px 4px}.expand{font-size:14px;color:#b6a0d6;align-self:center}.section[open]>summary .expand{font-size:0}.section[open]>summary .expand:after{content:"Cerrar";font-size:14px}.section-body{padding:0 4px 28px}.entry{border:1px solid #40364c;margin:12px 0;background:#191620;scroll-margin-top:90px}.entry>summary{padding:17px 20px;font-weight:650}.entry>summary:before{content:"+";margin-right:15px;color:#b6ee8b}.entry[open]>summary:before{content:"−"}.detail-body{padding:0 20px 20px}.permalink{font-size:14px}pre{white-space:pre-wrap;overflow-wrap:anywhere;margin:0;font:14px/1.7 Consolas,monospace;padding:18px}.macro{position:relative;background:#090c10;border:1px solid #323b45;margin:16px 0}.copy{margin:12px 12px 0;padding:9px 15px;color:#101015;background:#b6ee8b;border:0;border-radius:4px;cursor:pointer;font-weight:700;font-size:14px}table{border-collapse:collapse;width:100%;min-width:620px}th,td{padding:14px;text-align:left;vertical-align:top;border-bottom:1px solid #40364c}th{background:#241d2e}.table-wrap{overflow-x:auto;margin:20px 0}li{margin-bottom:9px}footer{border-top:1px solid #34303e;color:#bdb7c9;padding-top:24px;font-size:14px}.status{position:fixed;bottom:20px;right:20px;background:#b6ee8b;color:#101015;padding:10px 18px;z-index:10;border-radius:4px}.status:empty{display:none}@media(max-width:650px){main{padding:25px 18px 50px}.benefits,.index{grid-template-columns:1fr}header{font-size:14px}.section>summary{font-size:20px}.detail-body{padding:0 14px 16px}.entry>summary{padding:15px 14px}pre{font-size:13px;padding:14px}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}'''
js='''function reveal(){const id=decodeURIComponent(location.hash.slice(1));if(!id)return;const el=document.getElementById(id);if(!el)return;let p=el;while(p){if(p.tagName==='DETAILS')p.open=true;p=p.parentElement}requestAnimationFrame(()=>el.scrollIntoView({block:'start'}))}window.addEventListener('hashchange',reveal);reveal();document.addEventListener('click',async e=>{const b=e.target.closest('.copy');if(!b)return;const code=b.parentElement.querySelector('code').textContent;try{if(navigator.clipboard&&window.isSecureContext){await navigator.clipboard.writeText(code)}else{const t=document.createElement('textarea');t.value=code;t.style.position='fixed';t.style.opacity='0';document.body.appendChild(t);t.select();const ok=document.execCommand('copy');t.remove();if(!ok)throw Error('copy')}b.textContent='Copiada';document.getElementById('status').textContent='Macro copiada';setTimeout(()=>{b.textContent='Copiar macro';document.getElementById('status').textContent=''},2200)}catch{b.textContent='Selecciona y copia el texto';const s=window.getSelection(),r=document.createRange();r.selectNodeContents(b.parentElement.querySelector('code'));s.removeAllRanges();s.addRange(r)}});'''
favicon="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='6' fill='%23191620'/%3E%3Cpath d='M9 7h14v4H13v5h8v4h-8v6H9z' fill='%23b6ee8b'/%3E%3C/svg%3E"
page='<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Muchamiel · Brujo Forever | Builds y macros PvP</title><meta name="description" content="Guía para Muchamiel: 13 builds de brujo nivel 30, 41 macros en inglés y consejos para duelos, BGs y mundo abierto. Consulta cada tema y copia las macros."><link rel="icon" type="image/svg+xml" href="'+favicon+'"><style>'+css+'</style></head><body><header><strong>BRUJO / FOREVER</strong><a href="#indice">Índice</a><a href="#inicio">Inicio</a></header><main>'+intro+'<p class="start"><strong>Su personaje es Undead:</strong> <a href="#R1">Will of the Forsaken</a> y <a href="#R5">Cannibalize</a>. Macros para cualquier clase: <a href="#C18">parar acción</a>, <a href="#C19">abalorios</a> y <a href="#C20">venda sobre ti</a>.</p><nav id="indice" aria-label="Temas de la guía"><h2>Elige lo que quieras consultar</h2><div class="index">'+nav+'</div></nav>'+''.join(sections)+sourcehtml+'<footer>Preparado para Muchamiel · 9 de octubre de 2026 · Nivel 30 + 5 puntos de Legacy.<br>Repartos propuestos, comprobados por puntos y requisitos; rendimiento pendiente de práctica. Fuentes de Forever enlazadas en cada tema.</footer></main><div id="status" class="status" role="status" aria-live="polite"></div><script>'+js+'</script></body></html>'
(root/'web'/'dist'/'index.html').write_text(page,encoding='utf-8')
(root/'web'/'dist'/'app.js').write_text(js,encoding='utf-8')
assert page.count('class="copy"')==41
assert len(re.findall(r'<details id="B\d+"',page))==13
targets=set(re.findall(r'\bid="([^"]+)"',page))
for target in re.findall(r'href="#([^"]+)"',page):assert target in targets,target
print(json.dumps({'builds':13,'macros':41,'sources':len(sources),'sections':len(sections)+1,'file':str(root/'web'/'dist'/'index.html')}))
