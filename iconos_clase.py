"""Iconos en los resúmenes de Cambios (Van, 16-10: «con iconos es más fácil», «tanto razas como clases»):
el de la clase junto a cada recuadro y el de la raza al principio de cada línea del recuadro Razas."""
from crear_portal import classes

SLUG = {name: f'{slug}.jpg' for slug, name, *_ in classes}
SLUG['Razas'] = 'race_human_male.jpg'
RAZA = {'Tauren': 'race_tauren_male.jpg', 'Enano': 'race_dwarf_male.jpg', 'Célicos': 'skyborne.svg', 'Humano': 'race_human_male.jpg',
        'Orco': 'race_orc_male.jpg', 'No-muerto': 'race_scourge_male.jpg', 'Gnomo': 'race_gnome_male.jpg',
        'Elfo de la noche': 'race_nightelf_male.jpg', 'Trol': 'race_troll_male.jpg'}


def _img(f):
    return f'<img class="ic-clase" src="../assets/{f}" alt="">'


def con_icono(nombre, esc):
    """Nombre de clase (o «Guerrero y Druida», «Razas») con su icono delante; si no es una clase, el nombre tal cual."""
    partes = [p.strip() for p in nombre.split(' y ')]
    if not all(p in SLUG for p in partes):
        return esc(nombre)
    return ''.join(_img(SLUG[p]) for p in partes) + esc(nombre)


def icono_raza(texto):
    """Icono de la raza si la línea empieza por «Raza: …»; si no, nada."""
    raza = texto.split(':', 1)[0]
    return _img(RAZA[raza]) if ':' in texto and raza in RAZA else ''


CSS = (".ic-clase{width:22px;height:22px;border-radius:5px;border:1px solid #6b5a2e;vertical-align:-5px;margin-right:7px}"
       ".cc h4 .ic-clase+.ic-clase{margin-left:-3px}.cambios-lista li .ic-clase{width:20px;height:20px;vertical-align:-4px;margin-right:6px}")
