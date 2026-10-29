from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request
from datos_clases import DATA
root=Path(__file__).resolve().parent/'web'/'dist'/'assets'
root.mkdir(exist_ok=True)
urls={slug+'.jpg':'https://wow.zamimg.com/images/wow/icons/large/classicon_'+slug+'.jpg' for slug in ['warrior','paladin','hunter','rogue','priest','shaman','mage','warlock','druid']}
for races in DATA['racials'].values():
    for race in races:
        icon=race['icon']
        urls[icon+'.jpg']='https://wow.zamimg.com/images/wow/icons/large/'+icon+'.jpg'
urls['horde.png']='https://bnetcmsus-a.akamaihd.net/cms/content_entry_media/47/47RYBU87JTGK1790051522465.png'
urls['alliance.png']='https://bnetcmsus-a.akamaihd.net/cms/content_entry_media/7j/7J9HNHWVCNED1790052260790.png'
def fetch(item):
    name,url=item
    try:
        content=urllib.request.urlopen(url,timeout=20).read()
        (root/name).write_bytes(content)
        return name,len(content)
    except Exception as e:return name,str(e)
if __name__=='__main__':
    with ThreadPoolExecutor(max_workers=6) as pool:
        for result in pool.map(fetch,urls.items()):print(result)
