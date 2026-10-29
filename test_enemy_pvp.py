"""Exercise actual Lua with readable, restricted, missed and reset event fixtures."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'tmp/lua-test-runtime'))
from lupa.lua51 import LuaRuntime

lua = LuaRuntime(unpack_returned_tuples=True)
lua.execute('''
NS={}; now=100; hostile=true; enemyClass='ROGUE'; race='Scourge'; level=30
guid='rogue-1'; auras={}; spells={}; durations={}; captured=nil
MuchamielLockPvPDB={enemyDurations={}}
secret=setmetatable({}, {__eq=function() error('secret comparison') end})
function issecretvalue(v) return rawequal(v,secret) end
function GetTime() return now end
function UnitCanAttack(_,unit) return hostile and unit~='player' end
function UnitGUID(unit) return guid end
function UnitClass(unit) return enemyClass,enemyClass end
function UnitRace(unit) return race,race end
function UnitLevel(unit) return level end
function GetSpellBaseCooldown(id) return durations[id] end
C_Spell={GetSpellInfo=function(id) return spells[id] end}
C_UnitAuras={GetAuraDataByIndex=function(_,i,_) return auras[i] end}
function CreateFrame()
 return {RegisterEvent=function() end,SetScript=function(_,_,fn) captured=fn end}
end
''')
source = Path(__file__).resolve().parent.parent / 'MuchamielLockPvP/EnemyPvP.lua'
lua.execute('local loader = assert(loadstring(...)); loader("MuchamielLockPvP", NS)', source.read_text(encoding='utf-8'))
lua.execute('''
local E=NS.EnemyPvP
assert(E:state('target','Kick')=='? Desconocido')
spells[1766]={name='Kick',spellID=1766}; durations[1766]=10000
captured(nil,'UNIT_SPELLCAST_SUCCEEDED','target','cast-guid',1766)
assert(E:state('target','Kick'):find('~10s',1,true))
now=111
assert(E:state('target','Kick')=='~Podría estar listo')
guid='other-rogue'; assert(E:state('target','Kick')=='? Desconocido')
guid='rogue-1'; now=200
MuchamielLockPvPDB.enemyDurations.Kick=7
E:manual('target','Kick'); assert(E:state('target','Kick'):find('~7s (manual)',1,true))
spells[14185]={name='Preparation',spellID=14185}; durations[14185]=600000
E:observe('target',14185)
assert(E:state('target','Kick')=='? Reset observado: comprobar')
hostile=false; E:clear(); E:observe('target',1766)
assert(E:state('target','Kick')=='? Desconocido')
hostile=true
E:observe('target',secret); assert(E.status=='Evento con datos restringidos')
durations[1766]=secret; MuchamielLockPvPDB.enemyDurations.Kick=nil
E:observe('target',1766); assert(E:state('target','Kick')=='Uso visto · CD desconocido')
auras={{name='Decorative buff',spellId=1,dispelName=nil,isStealable=false},
 {name='Renew',spellId=139,dispelName='Magic',isStealable=false},
 {name='Evasion',spellId=5277,dispelName=nil,isStealable=false}}
local d=E:dispelText('target')
assert(d:find('Renew',1,true)); assert(not d:find('Decorative buff',1,true)); assert(not d:find('Evasion',1,true))
auras={{name=secret,dispelName=secret,isStealable=secret}}
assert(E:dispelText('target')=='Buffs con datos restringidos')
auras={}; enemyClass='WARLOCK'; race='Orc'
local list=table.concat(E:spellList('target'),'|')
assert(list:find('Devour Magic',1,true)); assert(not list:find('Spell Lock',1,true))
assert(not list:find('Death Coil',1,true)); assert(list:find('Blood Fury',1,true))
E:clear(); assert(E:state('target','Kick')=='? Desconocido')
''')
print('Lua 5.1 fixtures passed: observed casts, unknown state, expiry, identity, manual duration, reset, hostile filter, secret fields, dispel filter, level/race catalog.')

# Smoke-test addon initialization, both settings windows and their update callbacks.
lua.execute('''
frames={}; SlashCmdList={}; UISpecialFrames={}; STANDARD_TEXT_FONT='test'
SOUNDKIT={RAID_WARNING=1}; tinsert=table.insert; hostile=true; guid='ui-rogue'; auras={}
enemyClass='ROGUE'; race='Scourge'
local methods={}
function methods:SetScript(k,fn) self.scripts[k]=fn end
function methods:RegisterEvent(k) self.events[k]=true end
function methods:SetText(v) self.textValue=v end
function methods:GetText() return self.textValue or '' end
function methods:SetChecked(v) self.checked=v end
function methods:GetChecked() return self.checked end
function methods:SetShown(v) self.shown=v end
function methods:IsShown() return self.shown~=false end
function methods:HasFocus() return false end
function methods:GetScale() return 1 end
function methods:GetCenter() return 0,0 end
local function widget()
 return setmetatable({scripts={},events={}}, {__index=function(_,k)
  return methods[k] or function() end
 end})
end
function methods:CreateFontString() return widget() end
function CreateFrame(kind,name,parent,template)
 local f=widget(); f.kind=kind; f.frameName=name
 f.TitleText=widget(); f.Text=widget(); frames[#frames+1]=f
 return f
end
UIParent=widget(); UIErrorsFrame=widget(); GameTooltip=widget()
function UnitClass(unit) return unit=='player' and 'Warlock' or enemyClass, unit=='player' and 'WARLOCK' or enemyClass end
function UnitExists() return true end
function UnitAffectingCombat() return false end
function GetBuildInfo() return '1.60.1','test',nil,16001 end
function InCombatLockdown() return false end
''')
core = source.parent / 'Core.lua'
lua.execute('local loader = assert(loadstring(...)); loader("MuchamielLockPvP", NS)', core.read_text(encoding='utf-8'))
lua.execute('''
for _,f in ipairs(frames) do
 if f.events.ADDON_LOADED then f.scripts.OnEvent(f,'ADDON_LOADED','MuchamielLockPvP') end
end
assert(SlashCmdList.MUCHAMIELLOCKPVP)
assert(MuchamielLockPvPDB.profiles.Duelos.enabled.enemyCDs)
SlashCmdList.MUCHAMIELLOCKPVP('')
SlashCmdList.MUCHAMIELLOCKPVP('rival')
SlashCmdList.MUCHAMIELLOCKPVP('diag')
for _,f in ipairs(frames) do if f.scripts.OnUpdate then f.scripts.OnUpdate(f,.3) end end
for _,f in ipairs(frames) do
 if f.textValue=='Kick · ? Desconocido' and f.scripts.OnClick then f.scripts.OnClick(f) end
end
assert(NS.EnemyPvP:state('target','Kick')=='Uso visto · CD desconocido')
SlashCmdList.MUCHAMIELLOCKPVP('reset')
assert(NS.EnemyPvP:state('target','Kick')=='? Desconocido')
''')
print('Mock UI smoke test passed: addon load, saved settings, main/rival windows, panel refresh, manual-use button and reset command.')
