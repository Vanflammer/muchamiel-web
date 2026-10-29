"""Codificar/decodificar cadenas !WA:2! con las librerías originales (LibSerialize + LibDeflate) en Lua 5.1."""
import sys
from pathlib import Path
import lupa.lua51 as L51

D = Path(__file__).parent
lua = L51.LuaRuntime(unpack_returned_tuples=True)
lua.execute(r'''
LibStub = setmetatable({libs={}}, {__call=function(self, name) return self.libs[name] end})
function LibStub:NewLibrary(name, minor) local t = self.libs[name] or {}; self.libs[name] = t; return t end
function LibStub:GetLibrary(name) return self.libs[name] end
''')
for f in ('LibDeflate.lua', 'LibSerialize.lua'):
    lua.execute((D / f).read_text(encoding='utf-8'))
lua.execute(r'''
LD = LibStub("LibDeflate"); LS = LibStub("LibSerialize")
function wa_decode(s)
  local enc = s:match("^!WA:2!(.+)$")
  local comp = LD:DecodeForPrint(enc)
  local raw = LD:DecompressDeflate(comp)
  local ok, t = LS:Deserialize(raw)
  return t
end
function wa_encode(t)
  local raw = LS:Serialize(t)
  local comp = LD:CompressDeflate(raw, {level = 9})
  return "!WA:2!" .. LD:EncodeForPrint(comp)
end
local function key(k)
  if type(k) == "string" and k:match("^[%a_][%w_]*$") then return k end
  return "[" .. (type(k) == "string" and string.format("%q", k) or tostring(k)) .. "]"
end
function dump(v, ind)
  ind = ind or ""
  if type(v) == "table" then
    local keys = {}
    for k in pairs(v) do keys[#keys+1] = k end
    table.sort(keys, function(a, b) return tostring(a) < tostring(b) end)
    local out = {"{\n"}
    for _, k in ipairs(keys) do out[#out+1] = ind .. "  " .. key(k) .. " = " .. dump(v[k], ind .. "  ") .. ",\n" end
    out[#out+1] = ind .. "}"
    return table.concat(out)
  elseif type(v) == "string" then return string.format("%q", v)
  else return tostring(v) end
end
function load_table(src) return assert(loadstring("return " .. src))() end
''')


def decode_to_lua(s):
    return lua.globals().dump(lua.globals().wa_decode(s))


def encode_lua(src):
    return lua.globals().wa_encode(lua.globals().load_table(src))


if __name__ == '__main__':
    if sys.argv[1] == 'dec':
        print(decode_to_lua(Path(sys.argv[2]).read_text(encoding='utf-8').strip()))
    elif sys.argv[1] == 'enc':
        print(encode_lua(Path(sys.argv[2]).read_text(encoding='utf-8')))
