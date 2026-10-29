"""Lunargenta (arte oficial de Blizzard, página de Midnight) teñida de lila oscuro para el fondo de Retail."""
import sys
from PIL import Image, ImageOps, ImageEnhance
src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert('RGBA')
im = im.resize((1920, round(1920 * im.height / im.width)), Image.LANCZOS)
fondo = Image.new('RGBA', im.size, (11, 8, 22, 255))
# lo transparente/blanquecino de los bordes se funde en el morado oscuro
gris = ImageOps.grayscale(im.convert('RGB'))
lila = ImageOps.colorize(gris, black=(8, 4, 20), mid=(92, 52, 160), white=(226, 196, 255))
lila = Image.blend(lila, im.convert('RGB'), 0.18)  # un poco del oro original en las cúpulas
lila = ImageEnhance.Contrast(lila).enhance(1.15)
alfa = im.getchannel('A')
# los bordes del dibujo son casi blancos: se apagan para que no quede un halo claro
from PIL import ImageChops
claro = gris.point(lambda v: 255 if v < 235 else max(0, 255 - (v - 235) * 12))
alfa = ImageChops.multiply(alfa, claro)
fondo.paste(lila.convert('RGBA'), (0, 0), alfa)
fondo.convert('RGB').save(out, 'JPEG', quality=82, optimize=True, progressive=True)
print(fondo.size)
