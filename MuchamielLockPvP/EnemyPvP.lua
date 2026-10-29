-- Only public, readable unit events. No combat-log bypass or private enemy CD API.
local addonName, NS = ...
local E = {records = {}, status = "Sin usos observados", eventCount = 0}
NS.EnemyPvP = E

local catalog = {
 ROGUE = {{"Kick",12},{"Kidney Shot",30},{"Evasion",8},{"Vanish",22},{"Sprint",10},{"Preparation",30}},
 PRIEST = {{"Psychic Scream",14},{"Fear Ward",20},{"Silence",30},{"Penance",30},{"Inner Focus",20}},
 WARRIOR = {{"Berserker Rage",30},{"Intercept",30},{"Shield Bash",12},{"Shield Wall",28},{"Intimidating Shout",22},{"Death Wish",30}},
 SHAMAN = {{"Earth Shock",4},{"Grounding Totem",30},{"Tremor Totem",18},{"Purge",12}},
 MAGE = {{"Counterspell",24},{"Blink",20},{"Ice Block",25},{"Cold Snap",20},{"Frost Nova",10}},
 PALADIN = {{"Hammer of Justice",8},{"Divine Protection",6},{"Blessing of Protection",10},{"Blessing of Freedom",18},{"Lay on Hands",10},{"Repentance",30}},
 HUNTER = {{"Freezing Trap",20},{"Frost Trap",28},{"Feign Death",30},{"Intimidation",30},{"Scatter Shot",30},{"Deterrence",20},{"Rapid Fire",26}},
 WARLOCK = {{"Fear",8},{"Howl of Terror",40},{"Death Coil",42},{"Devour Magic",30},{"Spell Lock",36},{"Seduction",26},{"Sacrifice",16},{"Fel Domination",20}},
 DRUID = {{"Bash",14},{"Dash",26},{"Nature's Grasp",10},{"Nature's Swiftness",30},{"Innervate",40}},
}
local racials = {
 Scourge={"Will of the Forsaken"}, Undead={"Will of the Forsaken"},
 Dwarf={"Stoneform"}, Gnome={"Escape Artist"}, Tauren={"War Stomp"},
 Orc={"Blood Fury"}, Troll={"Berserking"}, Human={"Perception"}, NightElf={"Shadowmeld"},
}
local priority = { ["Fear Ward"]=true,["Will of the Forsaken"]=true,["Berserker Rage"]=true,
 ["Death Wish"]=true,["Ice Block"]=true,["Divine Protection"]=true,["Blessing of Protection"]=true,
 ["Blessing of Freedom"]=true,["Power Word: Shield"]=true,["Renew"]=true,["Rejuvenation"]=true,
 ["Regrowth"]=true,["Evasion"]=true,["Shield Wall"]=true,["Stoneform"]=true,["Deterrence"]=true }

local function clean(v) return not (issecretvalue and issecretvalue(v)) end
local function safe(fn,...)
 if type(fn)~="function" then return nil end
 local ok,v=pcall(fn,...)
 if ok and clean(v) then return v end
end
local function num(v) return clean(v) and type(v)=="number" end
local function str(v) return clean(v) and type(v)=="string" end
local function identity(unit)
 local guid=safe(UnitGUID,unit)
 return str(guid) and guid or nil
end
local function info(spell)
 local data=safe(C_Spell and C_Spell.GetSpellInfo,spell)
 if type(data)=="table" and clean(data) and str(data.name) and num(data.spellID) then return data end
end
local function baseDuration(id,name)
 local db=MuchamielLockPvPDB
 local seconds=db and db.enemyDurations and db.enemyDurations[name]
 if num(seconds) and seconds>0 then return seconds,"manual" end
 local ms=safe(GetSpellBaseCooldown,id)
 if num(ms) and ms>1500 then return ms/1000,"base" end
 return nil,"sin duración"
end
local function member(unit,name)
 local class=safe(function() local _,v=UnitClass(unit); return v end)
 for _,s in ipairs(catalog[class] or {}) do if s[1]==name then return true end end
 -- Pet abilities may be emitted by targetpet/focuspet/nameplates instead of owner.
 for _,s in ipairs(catalog.WARLOCK) do if s[1]==name then return true end end
 local race=safe(function() local _,v=UnitRace(unit); return v end)
 for _,v in ipairs(racials[race] or {}) do if v==name then return true end end
 -- An observed race-specific cast is useful even if race metadata is unavailable.
 for _,names in pairs(racials) do for _,v in ipairs(names) do if v==name then return true end end end
end

function E:bucket(id)
 if not self.records[id] then
  local count,oldest,stamp=0,nil,math.huge
  for key,b in pairs(self.records) do
   count=count+1
   if (b.lastSeen or 0)<stamp then oldest,stamp=key,b.lastSeen or 0 end
  end
  if count>=128 and oldest then self.records[oldest]=nil end
  self.records[id]={}
 end
 self.records[id].lastSeen=GetTime()
 return self.records[id]
end

function E:observe(unit,spellID)
 if not str(unit) or not num(spellID) then self.status="Evento con datos restringidos"; return end
 if not safe(UnitCanAttack,"player",unit) then return end
 local id=identity(unit)
 local spell=info(spellID)
 if not id or not spell then self.status="Identidad/hechizo no legible"; return end
 if not member(unit,spell.name) then return end
 local duration,source=baseDuration(spellID,spell.name)
 local bucket=self:bucket(id)
 bucket[spell.name]={start=GetTime(),duration=duration,source=source,spellID=spellID}
 self.eventCount=self.eventCount+1
 self.status="Uso detectado: "..spell.name
 -- A witnessed reset invalidates an estimate rather than asserting readiness.
 if spell.name=="Preparation" or spell.name=="Cold Snap" then
  for name,r in pairs(self.records[id]) do
   if name~=spell.name and type(r)=="table" then r.invalid=true end
  end
 end
end

function E:state(unit,name)
 local id=identity(unit)
 local r=id and self.records[id] and self.records[id][name]
 if not r then return "? Desconocido" end
 if r.invalid then return "? Reset observado: comprobar" end
 if not r.duration then return "Uso visto · CD desconocido" end
 local left=r.start+r.duration-GetTime()
 if left>0 then return string.format("~%.0fs (%s)",left,r.source=="manual" and "manual" or "base") end
 return "~Podría estar listo"
end

function E:spellList(unit)
 local class=safe(function() local _,v=UnitClass(unit); return v end)
 local level=safe(UnitLevel,unit)
 local list={}
 for _,s in ipairs(catalog[class] or {}) do
  if not num(level) or level<1 or level>=s[2] then list[#list+1]=s[1] end
 end
 local race=safe(function() local _,v=UnitRace(unit); return v end)
 for _,s in ipairs(racials[race] or {}) do list[#list+1]=s end
 -- Include casts actually observed, even if a beta spellbook changed.
 local id=identity(unit)
 for name,r in pairs(id and self.records[id] or {}) do
  local found=false; for _,v in ipairs(list) do if v==name then found=true end end
  if not found and type(r)=="table" then list[#list+1]=name end
 end
 return list
end

function E:active(unit)
 local out,restricted={},false
 if not C_UnitAuras or not C_UnitAuras.GetAuraDataByIndex then return out,true end
 for i=1,40 do
  local ok,a=pcall(C_UnitAuras.GetAuraDataByIndex,unit,i,"HELPFUL")
  if not ok or not clean(a) then restricted=true; break end
  if not a then break end
  if not str(a.name) then restricted=true
  elseif priority[a.name] then
   local time=""
   if num(a.expirationTime) and a.expirationTime>0 then time=string.format(" %.0fs",math.max(0,a.expirationTime-GetTime())) end
   out[#out+1]=a.name.." ACTIVO"..time
  end
 end
 return out,restricted
end

function E:dispelText(unit)
 if not safe(UnitCanAttack,"player",unit) then return "Selecciona un enemigo" end
 if not C_UnitAuras or not C_UnitAuras.GetAuraDataByIndex then return "API de auras no disponible" end
 local high,other,restricted={},{},false
 for i=1,40 do
  local ok,a=pcall(C_UnitAuras.GetAuraDataByIndex,unit,i,"HELPFUL")
  if not ok or not clean(a) then restricted=true; break end
  if not a then break end
  if not str(a.name) or not clean(a.dispelName) or not clean(a.isStealable) then restricted=true
  elseif a.dispelName=="Magic" or a.isStealable==true then
   local dest=priority[a.name] and high or other
   dest[#dest+1]=(priority[a.name] and "★ " or "")..a.name
  end
 end
 local lines={}
 for _,list in ipairs({high,other}) do for _,v in ipairs(list) do if #lines<3 then lines[#lines+1]=v end end end
 if #lines==0 then return restricted and "Buffs con datos restringidos" or "Sin buffs mágicos identificados" end
 lines[#lines+1]="Devour Magic: prueba si es disipable"
 return table.concat(lines,"\n")
end

function E:text(unit)
 if not safe(UnitCanAttack,"player",unit) then return "Selecciona un rival · /mlp rival" end
 local active,restricted=self:active(unit)
 local lines={}
 for i=1,math.min(2,#active) do lines[#lines+1]=active[i] end
 local list=self:spellList(unit)
 local id=identity(unit)
 for _,name in ipairs(list) do
  if id and self.records[id] and self.records[id][name] and #lines<3 then lines[#lines+1]=name..": "..self:state(unit,name) end
 end
 if #lines==0 then lines[1]=restricted and "Efectos con datos restringidos" or "CDs desconocidos: sin usos observados" end
 lines[#lines+1]="Todos los CDs: /mlp rival"
 return table.concat(lines,"\n")
end

function E:clear() self.records={}; self.status="Seguimiento reiniciado" end

-- A click records a use the player actually witnessed. It never casts or targets.
function E:manual(unit,name)
 if not safe(UnitCanAttack,"player",unit) then return false end
 local id=identity(unit); if not id then return false end
 local spell=info(name)
 local duration,source=baseDuration(spell and spell.spellID,name)
 self:bucket(id)[name]={start=GetTime(),duration=duration,source=source,manual=true}
 return true
end

function E:menu()
 if self.frame then self.frame:SetShown(not self.frame:IsShown()); return end
 local f=CreateFrame("Frame","MuchamielLockPvPRival",UIParent,"BasicFrameTemplateWithInset")
 f:SetSize(650,600); f:SetPoint("CENTER"); f:SetFrameStrata("DIALOG")
 f.TitleText:SetText("Rival · usos observados y tiempos estimados")
 tinsert(UISpecialFrames,"MuchamielLockPvPRival")
 f:SetMovable(true); f:EnableMouse(true); f:RegisterForDrag("LeftButton")
 f:SetScript("OnDragStart",f.StartMoving); f:SetScript("OnDragStop",f.StopMovingOrSizing)
 self.frame=f
 local note=f:CreateFontString(nil,"OVERLAY","GameFontHighlightSmall")
 note:SetPoint("TOPLEFT",16,-35); note:SetWidth(615); note:SetJustifyH("LEFT")
 note:SetText("No visto ≠ disponible. Tiempos base/manuales: talentos, resets y cargas pueden cambiarlos. Clic en un hechizo = marcar un uso visto; el número a su lado fija segundos de estimación.")
 local focus=CreateFrame("CheckButton",nil,f,"UICheckButtonTemplate")
 focus:SetPoint("TOPLEFT",14,-77); focus.Text:SetText("Usar foco en lugar de objetivo")
 local rows={}
 for i=1,12 do
  local b=CreateFrame("Button",nil,f,"UIPanelButtonTemplate")
  b:SetSize(485,27); b:SetPoint("TOPLEFT",16,-116-(i-1)*32)
  local edit=CreateFrame("EditBox",nil,f,"InputBoxTemplate")
  edit:SetSize(90,25); edit:SetPoint("LEFT",b,"RIGHT",16,0); edit:SetAutoFocus(false); edit:SetNumeric(true)
  b:SetScript("OnClick",function(self)
   if self.spell then E:manual(focus:GetChecked() and "focus" or "target",self.spell) end
  end)
  edit:SetScript("OnEnterPressed",function(self)
   if b.spell then
    local n=tonumber(self:GetText())
    MuchamielLockPvPDB.enemyDurations[b.spell]=(n and n>0 and n<=3600) and n or nil
   end
   self:ClearFocus()
  end)
  rows[i]={button=b,edit=edit}
 end
 local status=f:CreateFontString(nil,"OVERLAY","GameFontHighlightSmall")
 status:SetPoint("BOTTOMLEFT",16,49); status:SetWidth(610); status:SetJustifyH("LEFT")
 local clear=CreateFrame("Button",nil,f,"UIPanelButtonTemplate")
 clear:SetPoint("BOTTOMLEFT",16,16); clear:SetSize(170,25); clear:SetText("Reiniciar observaciones")
 clear:SetScript("OnClick",function() E:clear() end)
 local dr=CreateFrame("Button",nil,f,"UIPanelButtonTemplate")
 dr:SetPoint("LEFT",clear,"RIGHT",12,0); dr:SetSize(200,25); dr:SetText("Configurar Forever Simple DR")
 dr:SetScript("OnClick",function()
  if SlashCmdList and SlashCmdList.FOREVERSIMPLEDR then SlashCmdList.FOREVERSIMPLEDR("")
  else print("DR: instala Forever Simple DR y abre /fdr. Esta alpha no fabrica DR.") end
 end)
 local elapsed=0
 f:SetScript("OnUpdate",function(_,dt)
  elapsed=elapsed+dt; if elapsed<.25 then return end; elapsed=0
  local unit=focus:GetChecked() and "focus" or "target"
  local list=E:spellList(unit)
  for i,row in ipairs(rows) do
   local name=list[i]
   row.button.spell=name; row.button:SetShown(name~=nil); row.edit:SetShown(name~=nil)
   if name then
    row.button:SetText(name.." · "..E:state(unit,name))
    if not row.edit:HasFocus() then row.edit:SetText(tostring(MuchamielLockPvPDB.enemyDurations[name] or "")) end
   end
  end
  local active,restricted=E:active(unit)
  status:SetText((#active>0 and table.concat(active," · ") or (restricted and "Auras restringidas" or "Sin defensivos identificados")).."\n"..E.status)
 end)
end

local f=CreateFrame("Frame")
pcall(f.RegisterEvent,f,"UNIT_SPELLCAST_SUCCEEDED")
f:SetScript("OnEvent",function(_,event,unit,_,spellID)
 if not MuchamielLockPvPDB then return end
 local ok=pcall(function() E:observe(unit,spellID) end)
 if not ok then E.status="Evento no compatible; seguimiento limitado" end
end)
