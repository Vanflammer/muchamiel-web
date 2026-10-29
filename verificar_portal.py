from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote
import json,re,zipfile
from datos_clases import BUILDS,validate
ROOT=Path(__file__).resolve().parent/'web'/'dist'
class Page(HTMLParser):
    def __init__(self,s):super().__init__();self.ids=[];self.links=[];self.feed(s)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        for k in ['href','src']:
            if k in a:self.links.append(a[k])
pages={f:Page(f.read_text(encoding='utf-8')) for f in ROOT.rglob('*.html')}
errors=[]
for file,page in pages.items():
    if len(page.ids)!=len(set(page.ids)):errors.append((str(file),'duplicate ids'))
    for link in page.links:
        u=urlsplit(link)
        if u.scheme or u.netloc:continue
        target=(ROOT/unquote(u.path).lstrip('/')).resolve() if u.path.startswith('/') else (file.parent/unquote(u.path)).resolve() if u.path else file
        if target.is_dir():target=target/'index.html'
        if not target.exists():errors.append((str(file.relative_to(ROOT)),link,'missing'))
        elif u.fragment and not u.fragment.startswith('%7B') and target in pages and unquote(u.fragment) not in pages[target].ids:errors.append((str(file.relative_to(ROOT)),link,'missing anchor'))
s=(ROOT/'calculadora'/'index.html').read_text(encoding='utf-8')
d=json.loads(re.search(r'<script type="application/json" id="talent-data">(.*?)</script>',s,re.S)[1])
BUILDS.update(d['presets'])
errors.extend(validate())
print(json.dumps({'pages':len(pages),'classes':len(d['classes']),'presets':sum(len(a) for a in d['presets'].values()),'errors':errors},ensure_ascii=False,indent=2))
with zipfile.ZipFile(ROOT.parent.parent/'Muchamiel-WoW-Forever-Web.zip') as z:
    assert z.testzip() is None
    assert 'wow-forever/calculadora/calculator.js' in z.namelist()
    print('ZIP íntegro; calculadora incluida.')
raise SystemExit(bool(errors))
