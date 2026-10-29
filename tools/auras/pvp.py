"""Paquete «Muchamiel PvP» para ForeverAuras (v2, 17-10: lo que te tiran encima + distancia), hecho a partir de dos auras de Forever que funcionan:
- Rogue Buff Bar (MX8RN6DVQ): icono con disparador secretAura (ve buffs del objetivo en combate) dentro de un grupo con blizzardFlow.
- UntrueUI Range Checker (XXzDjgfQx): texto con disparador Range Check (metros mín.-máx. al objetivo) y colores por condición.
Salida: research/muchamiel-pvp.txt (cadena !WA:2!) y research/muchamiel-pvp.lua (para revisar). Uso: python tools/auras/pvp.py"""
import json
from pathlib import Path
from wa import lua

D = Path(__file__).parent
R = D.parent.parent / 'research'
codes = json.load(open(R / 'auras-codigos.json', encoding='utf-8'))
G = lua.globals()
G.TPL_BUFF = codes['MX8RN6DVQ']['code']
G.TPL_RANGE = codes['XXzDjgfQx']['code']

# Van 17-10: lo que el rival te tira encima (debuffs en ti), en grande y con su tiempo. Contar sus reutilizaciones NO se puede:
# Forever (como Midnight) ya no da el registro de combate a los addons y los lanzamientos enemigos son secretos en combate.
# (nombre en pantalla, ids de hechizo del debuff en ti; ids de Classic)
BUFFS = [
    ('Miedo', [5782, 6213, 6215]),
    ('Aullido de terror', [5484, 17928]),
    ('Espiral de la muerte', [6789, 17925, 17926]),
    ('Seducción', [6358]),
    ('Alarido psíquico', [8122, 8124, 10888, 10890]),
    ('Grito intimidatorio', [5246]),
    ('Ceguera', [2094]),
    ('Gubia', [1776, 1777, 8629, 11285, 11286]),
    ('Golpe en los riñones', [408, 8643]),
    ('Golpe bajo', [1833]),
    ('Porrazo', [6770, 2070, 11297]),
    ('Martillo de justicia', [853, 5588, 5589, 10308]),
    ('Polimorfia', [118, 12824, 12825, 12826, 28270, 28271, 28272]),
    ('Silencio de Contrahechizo', [18469]),
    ('Silencio de Patada', [18425]),
    ('Silencio', [15487]),
    ('Aturdimiento de Carga', [7922]),
    ('Aturdimiento de Interceptar', [20253, 20614, 20615]),
    ('Golpe conmocionador', [12809]),
    ('Azote', [5211, 6798, 8983]),
    ('Abalanzarse', [9005, 9823, 9827]),
    ('Disparo de dispersión', [19503]),
    ('Trampa congelante', [3355, 14308, 14309]),
    ('Picadura de dracoleón', [19386, 24132, 24133]),
    ('Nova de escarcha', [122, 865, 6131, 10230]),
    ('Raíces enredadoras', [339, 1062, 5195, 5196, 9852, 9853]),
]
lua_buffs = '{' + ','.join('{name=%s, ids={%s}}' % (json.dumps(n, ensure_ascii=False), ','.join('"%d"' % i for i in ids)) for n, ids in BUFFS) + '}'

lua.execute(r'''
local function copy(t) if type(t) ~= "table" then return t end local r = {} for k, v in pairs(t) do r[k] = copy(v) end return r end
local n = 0
local function uid() n = n + 1 return string.format("MuchaPvP%03d", n) end
local function clean(t) t.url = nil; t.wagoID = nil; t.source = nil; t.uid = uid(); t.semver = "2.0.0"; t.version = 2 end

function build(buffs)
  local B = wa_decode(TPL_BUFF)
  local R = wa_decode(TPL_RANGE)
  local out = {c = {}, m = "d", s = B.s, v = B.v}

  -- 0) Grupo padre normal (del Range Checker): contiene la fila de iconos y los textos
  local top = copy(R.d)
  clean(top); top.id = "Muchamiel PvP"; top.controlledChildren = {}; top.xOffset = 0; top.yOffset = 140
  top.load = {class = {multi = {}}, size = {multi = {}}, spec = {multi = {}}, talent = {multi = {}}}
  -- 1) Subgrupo de buffs del objetivo (iconos en fila, centrados)
  local g = copy(B.d)
  clean(g); g.id = "Muchamiel PvP - Lo que te han tirado"; g.controlledChildren = {}; g.xOffset = 0; g.yOffset = 0; g.parent = top.id
  top.controlledChildren[1] = g.id
  out.c[1] = g
  g.load = {class = {multi = {}}, size = {multi = {}}, spec = {multi = {}}, talent = {multi = {}}}
  local icon = B.c[1]
  for i, b in ipairs(buffs) do
    local a = copy(icon)
    clean(a); a.id = "Muchamiel PvP - " .. b.name; a.parent = g.id
    a.load = {class = {multi = {}}, size = {multi = {}}, spec = {multi = {}}, talent = {multi = {}}}
    a.height = 54; a.width = 54; a.conditions = {}
    local trg = a.triggers[1].trigger
    trg.unit = "player"; trg.debuffType = "HARMFUL"; trg.auraRankSpellIDs = copy(b.ids); trg.auraspellids = {}
    trg.useExactSpellId = true; trg.secretUseRankSpellIDs = true; trg.secretUseSpellIDs = false
    a.triggers.activeTriggerMode = -10
    -- glow fijo para que se vea de un vistazo
    table.insert(a.subRegions, {type = "subglow", glow = true, glowType = "Pixel", glowColor = {1, 0.15, 0.15, 1}, glowLines = 8, glowFrequency = 0.25, glowLength = 10, glowThickness = 2, glowXOffset = 0, glowYOffset = 0, glowScale = 1, glowBorder = false, useGlowColor = true})
    g.controlledChildren[#g.controlledChildren + 1] = a.id
    out.c[#out.c + 1] = a
  end
  out.d = top

  -- 2) Distancia al objetivo: metros con colores por franja + aviso de zona muerta
  local txt = copy(R.c[1])
  local function franja(op, val, col) return {check = {op = op, trigger = 1, value = tostring(val), variable = "range"}, changes = {{property = "color", value = col}}} end
  local metros = copy(txt)
  clean(metros); metros.id = "Muchamiel PvP - Metros"; metros.parent = top.id
  metros.displayText = "%1.minRange-%1.maxRange m"; metros.fontSize = 22; metros.xOffset = 0; metros.yOffset = -60
  metros.color = {0.75, 0.75, 0.75, 1}
  metros.conditions = {
    franja("<=", 30, {1, 0.9, 0.3, 1}),      -- hechizos (30 m)
    franja("<=", 20, {0.3, 1, 0.4, 1}),      -- Miedo / Espiral de la muerte (20 m)
    franja("<=", 8, {1, 0.5, 0, 1}),         -- zona muerta del cazador (5-8 m)
    franja("<=", 5, {1, 0.1, 0.1, 1}),       -- cuerpo a cuerpo
  }
  local aviso = copy(txt)
  clean(aviso); aviso.id = "Muchamiel PvP - Zona muerta"; aviso.parent = top.id
  aviso.displayText = "ZONA MUERTA"; aviso.fontSize = 18; aviso.xOffset = 0; aviso.yOffset = -85
  aviso.color = {1, 0.5, 0, 1}; aviso.alpha = 0
  aviso.conditions = {
    {check = {op = "<=", trigger = 1, value = "8", variable = "range"}, changes = {{property = "alpha", value = 1}}},
    {check = {op = "<=", trigger = 1, value = "5", variable = "range"}, changes = {{property = "alpha", value = 0}}},
  }
  for _, t in ipairs({metros, aviso}) do
    -- solo el disparador de distancia (el original traía otros)
    t.triggers = {[1] = copy(txt.triggers[1]), activeTriggerMode = -10}
    t.load = {class = {multi = {}}, size = {multi = {}}, spec = {multi = {}}, talent = {multi = {}}}
    top.controlledChildren[#top.controlledChildren + 1] = t.id
    out.c[#out.c + 1] = t
  end
  return out
end
''')
data = G.build(lua.eval(lua_buffs))
s = G.wa_encode(data)
(R / 'muchamiel-pvp.txt').write_text(s, encoding='utf-8')
(R / 'muchamiel-pvp.lua').write_text(G.dump(data), encoding='utf-8')
back = G.wa_decode(s)
print('longitud', len(s), '| hijos', len(back.c), '| grupo', back.d.id)
