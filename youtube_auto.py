"""Integración después de idiomas: texto nuevo localizado sin tocar el diccionario."""
from pathlib import Path
import shutil, json, re

ROOT = Path(__file__).resolve().parent

def install(dist):
    shutil.copyfile(ROOT / 'youtube/videos.js', dist / 'assets/videos.js')
    shutil.copyfile(ROOT / 'youtube/worker.mjs', dist / '_worker.js')
    shutil.copyfile(ROOT / 'research/muchamiel-feed.xml', dist / 'assets/youtube-fallback.xml')
    (dist / 'datos').mkdir(exist_ok=True)  # 29-10: la tarea de GitHub la renueva cada 20 min
    shutil.copyfile(ROOT / 'research/muchamiel-feed.xml', dist / 'datos/youtube-feed.xml')
    (dist / '_routes.json').write_text(json.dumps({
        'version': 1, 'include': ['/api/youtube-feed'], 'exclude': []
    }), encoding='utf-8')
    for prefix in ['', 'en/']:
        for slug in ['', 'noticias/']:
            file = dist / prefix / slug / 'index.html'
            if not file.exists():
                continue
            source = file.read_text(encoding='utf-8')
            if 'data-youtube-latest' in source:
                continue
            base = '../' * len(file.relative_to(dist).parts[:-1]) or './'
            en = bool(prefix)
            note = ('Latest channel uploads, including videos, Shorts and streams.' if en else
                    'Últimas publicaciones del canal: vídeos, Shorts y directos.')
            status = f'<p class="fine" data-youtube-status aria-live="polite">{note}</p>'
            if not slug:
                # The final home grid is the curated fallback for live loading.
                start = source.rfind('<div class="vgrid">')
                if start < 0:
                    raise ValueError('Home video grid missing')
                source = source[:start] + source[start:].replace('<div class="vgrid">',
                    '<div class="vgrid" data-youtube-latest data-limit="4">', 1)
                end = source.index('</div>', start) + len('</div>')
                source = source[:end] + status + source[end:]
            else:
                start = source.index('<div class="divider">')
                title = 'Latest channel videos' if en else 'Últimos vídeos del canal'
                # Reuse archive cards as a no-JS/offline fallback.
                match = re.search(r'<div class="vgrid">(.*?)</div>', source, re.S)
                cards = re.findall(r'<a class="vcard".*?</a>', match[1], re.S)[:6]
                section = (f'<section class="youtube-latest"><div class="divider"><h2>{title}</h2></div>'
                    '<div class="vgrid" data-youtube-latest data-limit="12">' + ''.join(cards) + '</div>' + status + '</section>')
                source = source[:start] + section + source[start:]
            source = source.replace('</body>', f'<script src="{base}assets/videos.js" defer></script></body>', 1)
            file.write_text(source, encoding='utf-8')

if __name__ == '__main__':
    install(ROOT / 'web/dist')
