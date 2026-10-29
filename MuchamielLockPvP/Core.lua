local addonName, NS = ...
local A = {panels = {}, lastAlerts = {}, elapsed = 0, preview = false}
local modules = {
    {"cooldowns", "Healthstone y racial", "Cantidad de Healthstone y cooldown legible de Will of the Forsaken."},
    {"shards", "Soul Shards", "Cantidad en bolsas; aviso por debajo del umbral."},
    {"pet", "Demonio", "Estado y habilidades de la mascota actual; vida/maná opcionales."},
    {"buffs", "Soul Link, armadura y Nightfall", "Solo efectos que el cliente permita identificar."},
    {"dots", "DoTs y maldiciones del objetivo", "Efectos propios legibles; datos restringidos se indican."},
    {"targetCast", "Casteo del objetivo", "Casteos y canalizaciones con información legible."},
    {"focusCast", "Casteo del foco", "Mismo seguimiento para el foco."},
    {"dr", "DR · complemento externo", "El seguimiento real requiere Forever Simple DR instalado aparte (/fdr)."},
    {"totems", "Tótems visibles", "Detección por nombre en placas visibles; sin cálculo de cooldowns."},
    {"enemyBuffs", "Buffs mágicos para Devour Magic", "Buffs mágicos legibles del rival; destaca prioridades. No garantiza que sean disipables."},
    {"enemyCDs", "Cooldowns y defensivos del rival", "Usos legibles observados, efectos activos y tiempos base/manuales estimados. /mlp rival."},
}
local defaults = {profile = "Duelos", locked = true, scale = 1, fontSize = 13,
    sounds = false, combatOnly = false, petBars = false, shardMinimum = 3,
    alerts = {pet = true, nightfall = true, shards = true, totems = true}, profiles = {}, enemyDurations = {}}
local watchDots = { [172]=true, [348]=true, [980]=true, [702]=true, [1714]=true,
    [1490]=true, [18265]=true, [18223]=true }
local watchBuffNames = { ["Soul Link"]=true, ["Nightfall"]=true, ["Shadow Trance"]=true,
    ["Demon Armor"]=true, ["Demon Skin"]=true }
local petSpells = {"Devour Magic", "Spell Lock", "Seduction", "Sacrifice", "Lash of Pain", "Firebolt"}
local importantTotems = {"tremor", "grounding", "earthbind", "windfury", "searing"}

local function readable(v)
    return not (issecretvalue and issecretvalue(v))
end
local function safe(fn, ...)
    if type(fn) ~= "function" then return nil end
    local ok, value = pcall(fn, ...)
    if ok and readable(value) then return value end
end
local function plain(v)
    if readable(v) and (type(v) == "string" or type(v) == "number") then return tostring(v) end
    return "?"
end
local function copy(t)
    local out = {}
    for k,v in pairs(t) do out[k] = type(v)=="table" and copy(v) or v end
    return out
end
local function profile()
    return MuchamielLockPvPDB.profiles[MuchamielLockPvPDB.profile]
end
local function emit(key, text)
    local db = MuchamielLockPvPDB
    if not db.alerts[key] then return end
    local now = GetTime()
    local alertKey=key=="totems" and key..":"..text or key
    if A.lastAlerts[alertKey] and now-A.lastAlerts[alertKey] < 12 then return end
    A.lastAlerts[alertKey] = now
    UIErrorsFrame:AddMessage(text, 0.85, 0.65, 1)
    if db.sounds then PlaySound(SOUNDKIT.RAID_WARNING, "Master") end
end
local function label(parent, text, size)
    local f = parent:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    f:SetFont(STANDARD_TEXT_FONT, size or 13, "OUTLINE")
    f:SetText(text); f:SetJustifyH("LEFT")
    return f
end
local function button(parent, text, x, y, fn, width)
    local b = CreateFrame("Button", nil, parent, "UIPanelButtonTemplate")
    b:SetSize(width or 160, 24); b:SetPoint("TOPLEFT", x, y); b:SetText(text)
    b:SetScript("OnClick", fn); return b
end
local function checkLabel(b,text)
    local font=b.Text or b.text
    if not font then font=label(b,text,13); font:SetPoint("LEFT",b,"RIGHT",2,0) end
    font:SetText(text)
end

function A:apply()
    local db, p = MuchamielLockPvPDB, profile()
    for _,m in ipairs(modules) do
        local f, pos = self.panels[m[1]], p.positions[m[1]]
        f:ClearAllPoints(); f:SetPoint("CENTER", UIParent, "CENTER", pos.x, pos.y)
        f:SetScale(db.scale); f:EnableMouse(not db.locked)
        f.text:SetFont(STANDARD_TEXT_FONT, db.fontSize, "OUTLINE")
        f:SetShown(p.enabled[m[1]] and (not db.combatOnly or UnitAffectingCombat("player") or self.preview))
    end
end

local function panel(key, title, n)
    local f = CreateFrame("Frame", nil, UIParent, "BackdropTemplate")
    f:SetSize(290, 88)
    f:SetBackdrop({bgFile="Interface\\Buttons\\WHITE8X8", edgeFile="Interface\\Buttons\\WHITE8X8", edgeSize=1})
    f:SetBackdropColor(0.04,0.03,0.07,0.82); f:SetBackdropBorderColor(0.45,0.28,0.65,0.9)
    f.title = label(f, title, 12); f.title:SetPoint("TOPLEFT", 8, -6)
    f.text = label(f, "Pendiente de datos", 13); f.text:SetPoint("TOPLEFT", 8,-25)
    f.text:SetWidth(274); f.text:SetJustifyV("TOP")
    f:SetMovable(true); f:SetClampedToScreen(true); f:RegisterForDrag("LeftButton")
    f:SetScript("OnDragStart", function(self) if not MuchamielLockPvPDB.locked then self:StartMoving() end end)
    f:SetScript("OnDragStop", function(self)
        self:StopMovingOrSizing()
        local x,y=self:GetCenter(); local ux,uy=UIParent:GetCenter()
        local s=self:GetScale()/UIParent:GetScale()
        profile().positions[key]={x=x*s-ux,y=y*s-uy}
        A:apply()
    end)
    A.panels[key]=f
end

local function auraLines(unit, filter, selectAura)
    if not C_UnitAuras or not C_UnitAuras.GetAuraDataByIndex then return "API de auras no disponible" end
    local lines, restricted = {}, false
    for i=1,40 do
        local ok, aura=pcall(C_UnitAuras.GetAuraDataByIndex, unit, i, filter)
        if not ok then return "Datos restringidos / API no compatible" end
        if not readable(aura) then return "Datos restringidos" end
        if not aura then break end
        if not readable(aura.name) or not readable(aura.spellId) then restricted=true
        elseif selectAura(aura) then
            local time=""
            if readable(aura.expirationTime) and type(aura.expirationTime)=="number" and aura.expirationTime>0 then
                time=string.format("  %.1fs", math.max(0,aura.expirationTime-GetTime()))
            elseif not readable(aura.expirationTime) then time="  tiempo restringido" end
            lines[#lines+1]=aura.name..time
            if #lines>=3 then break end
        end
    end
    if #lines==0 then return restricted and "Datos restringidos" or "Sin efectos detectados" end
    return table.concat(lines,"\n")
end
local function cooldownText(name)
    if not C_Spell or not C_Spell.GetSpellInfo then return name..": API no disponible" end
    local info=safe(C_Spell.GetSpellInfo, name)
    if not info or not readable(info.spellID) then return name..": no disponible" end
    local learned=safe(IsPlayerSpell, info.spellID)
    if not learned then return name..": no aprendido" end
    local data=safe(C_Spell.GetSpellCooldown,info.spellID)
    if not data or not readable(data.startTime) or not readable(data.duration) then return name..": cooldown restringido" end
    local left=math.max(0,data.startTime+data.duration-GetTime())
    return name..(left>1.5 and string.format(": %.0fs",left) or ": disponible")
end
local function castText(unit)
    local function get(fn)
        if not fn then return nil end
        local ok, name, _, _, start, finish = pcall(fn,unit)
        if not ok then return "API no compatible" end
        if not readable(name) then return "Casteo con datos restringidos" end
        if not name then return nil end
        if readable(finish) and type(finish)=="number" then return name..string.format("  %.1fs",math.max(0,finish/1000-GetTime())) end
        return name.."  tiempo restringido"
    end
    return get(UnitCastingInfo) or get(UnitChannelInfo) or "Sin casteo visible"
end

function A:update()
    local db,p=MuchamielLockPvPDB,profile()
    self:apply()
    if self.preview then
        for _,m in ipairs(modules) do self.panels[m[1]].text:SetText("VISTA PREVIA · datos de ejemplo\nArrastra si el panel está desbloqueado") end
        return
    end
    local function set(key, value) if p.enabled[key] then self.panels[key].text:SetText(value) end end
    if p.enabled.cooldowns then
        local hs=0
        for _,id in ipairs({5512,5511,5509,5510,9421}) do hs=hs+(safe(C_Item and C_Item.GetItemCount or GetItemCount,id,false) or 0) end
        set("cooldowns", "Healthstone: "..hs.." en bolsas\n"..cooldownText("Will of the Forsaken"))
    end
    if p.enabled.shards then
        local count=safe(C_Item and C_Item.GetItemCount or GetItemCount,6265,false)
        set("shards", "Soul Shards: "..plain(count).."\nUmbral de aviso: "..db.shardMinimum)
        if count and count<db.shardMinimum and UnitAffectingCombat("player") then emit("shards","Pocas Soul Shards") end
    end
    if p.enabled.pet then
        if not UnitExists("pet") then set("pet","Sin demonio activo"); if UnitAffectingCombat("player") then emit("pet","Sin demonio activo") end
        elseif safe(UnitIsDead,"pet") then set("pet","Demonio muerto"); emit("pet","Demonio muerto")
        else
            local lines={plain(safe(UnitName,"pet"))}
            local found={}
            for i=1,10 do
                local ok,name,_,isToken,_,_,_,_,spellID=pcall(GetPetActionInfo,i)
                if ok and readable(name) and name then
                    if readable(isToken) and isToken then name=_G[name] or name end
                    for _,want in ipairs(petSpells) do if name==want then found[#found+1]=want end end
                end
            end
            lines[#lines+1]=#found>0 and table.concat(found," · ") or "Sin habilidades identificadas"
            if db.petBars then lines[#lines+1]="Vida "..plain(safe(UnitHealth,"pet")).." · Maná "..plain(safe(UnitPower,"pet",0)) end
            set("pet", table.concat(lines,"\n"))
        end
    end
    if p.enabled.buffs then
        set("buffs", auraLines("player","HELPFUL",function(a)
            if a.name=="Nightfall" or a.name=="Shadow Trance" then emit("nightfall","Nightfall activo") end
            return watchBuffNames[a.name]
        end))
    end
    if p.enabled.dots then
        set("dots", UnitExists("target") and auraLines("target","HARMFUL|PLAYER",function(a)
            return watchDots[a.spellId] or a.name=="Corruption" or a.name=="Immolate"
                or a.name:find("Curse",1,true) or a.name:find("Bane",1,true) or a.name=="Siphon Life"
        end) or "Selecciona un objetivo")
    end
    if p.enabled.targetCast then set("targetCast",castText("target")) end
    if p.enabled.focusCast then set("focusCast",castText("focus")) end
    if p.enabled.enemyBuffs then set("enemyBuffs",NS.EnemyPvP:dispelText("target")) end
    if p.enabled.enemyCDs then set("enemyCDs",NS.EnemyPvP:text("target")) end
    if p.enabled.dr then set("dr","DR automático pendiente de integrar\nComplemento: Forever Simple DR (/fdr)") end
    if p.enabled.totems then
        local lines={}
        if C_NamePlate and C_NamePlate.GetNamePlates then
            local plates=safe(C_NamePlate.GetNamePlates)
            for _,plate in ipairs(plates or {}) do
                local unit=plate.namePlateUnitToken
                local name=unit and safe(UnitName,unit)
                if type(name)=="string" and safe(UnitCanAttack,"player",unit) then
                    local lower=name:lower()
                    for _,word in ipairs(importantTotems) do
                        if lower:find("totem",1,true) and lower:find(word,1,true) then
                            lines[#lines+1]=name; emit("totems",name); break
                        end
                    end
                end
                if #lines>=3 then break end
            end
        end
        set("totems",#lines>0 and table.concat(lines,"\n") or "Sin tótems identificados en placas\nDetección por nombre · experimental")
    end
end

function A:menu()
    if self.options then self.options:SetShown(not self.options:IsShown()); return end
    local f=CreateFrame("Frame","MuchamielLockPvPOptions",UIParent,"BasicFrameTemplateWithInset")
    f:SetSize(610,730); f:SetPoint("CENTER"); f:SetFrameStrata("DIALOG")
    f.TitleText:SetText("Muchamiel Lock PvP · alpha 0.2.0 · /mlp")
    f:SetMovable(true); f:EnableMouse(true); f:RegisterForDrag("LeftButton")
    f:SetScript("OnDragStart",f.StartMoving); f:SetScript("OnDragStop",f.StopMovingOrSizing)
    tinsert(UISpecialFrames,"MuchamielLockPvPOptions")
    self.options=f
    local note=label(f,"Módulos configurables. Datos restringidos no se estiman como exactos.",12)
    note:SetPoint("TOPLEFT",18,-38)
    local checkboxes={}
    local function refresh()
        for key,b in pairs(checkboxes) do b:SetChecked(profile().enabled[key]) end
    end
    button(f,"Perfil: Duelos",18,-65,function() MuchamielLockPvPDB.profile="Duelos"; refresh(); A:update() end,180)
    button(f,"Perfil: BGs",208,-65,function() MuchamielLockPvPDB.profile="BGs"; refresh(); A:update() end,180)
    for i,m in ipairs(modules) do
        local key,title,desc=m[1],m[2],m[3]
        local b=CreateFrame("CheckButton",nil,f,"UICheckButtonTemplate")
        b:SetPoint("TOPLEFT",16,-95-(i-1)*34); b:SetChecked(profile().enabled[key])
        checkLabel(b,title); b:SetScript("OnClick",function(self) profile().enabled[key]=self:GetChecked() and true or false; A:update() end)
        b:SetScript("OnEnter",function(self) GameTooltip:SetOwner(self,"ANCHOR_RIGHT"); GameTooltip:SetText(desc,1,1,1,1,true); GameTooltip:Show() end)
        b:SetScript("OnLeave",function() GameTooltip:Hide() end)
        checkboxes[key]=b
    end
    local function toggle(text,key,x,y)
        local b=CreateFrame("CheckButton",nil,f,"UICheckButtonTemplate")
        b:SetPoint("TOPLEFT",x,y); checkLabel(b,text); b:SetChecked(MuchamielLockPvPDB[key])
        b:SetScript("OnClick",function(self) MuchamielLockPvPDB[key]=self:GetChecked() and true or false; A:update() end)
    end
    toggle("Bloquear paneles","locked",16,-480); toggle("Sonidos","sounds",305,-480)
    toggle("Solo en combate","combatOnly",16,-512); toggle("Vida/maná de pet","petBars",305,-512)
    button(f,"Tamaño −",18,-550,function() MuchamielLockPvPDB.scale=math.max(.6,MuchamielLockPvPDB.scale-.1); A:apply() end,120)
    button(f,"Tamaño +",148,-550,function() MuchamielLockPvPDB.scale=math.min(1.8,MuchamielLockPvPDB.scale+.1); A:apply() end,120)
    button(f,"Texto −",278,-550,function() MuchamielLockPvPDB.fontSize=math.max(10,MuchamielLockPvPDB.fontSize-1); A:apply() end,120)
    button(f,"Texto +",408,-550,function() MuchamielLockPvPDB.fontSize=math.min(22,MuchamielLockPvPDB.fontSize+1); A:apply() end,120)
    button(f,"Vista previa",18,-584,function() A.preview=not A.preview; A:update() end)
    button(f,"CDs del rival",208,-654,function() NS.EnemyPvP:menu() end,180)
    button(f,"Tótems/pets: mostrar",208,-584,function()
        if InCombatLockdown() then print("Muchamiel Lock PvP: cambia las placas fuera de combate."); return end
        for _,key in ipairs({"nameplateShowEnemies","nameplateShowEnemyPets","nameplateShowEnemyTotems","nameplateShowAll"}) do pcall(SetCVar,key,1) end
        print("Muchamiel Lock PvP: placas activadas; revisa Options si un ajuste no está disponible.")
    end,220)
    button(f,"Avisos individuales",18,-616,function()
        if A.alertMenu then A.alertMenu:SetShown(not A.alertMenu:IsShown()); return end
        local w=CreateFrame("Frame",nil,f,"BasicFrameTemplateWithInset")
        w:SetSize(360,240); w:SetPoint("CENTER"); w:SetFrameStrata("FULLSCREEN_DIALOG")
        w.TitleText:SetText("Avisos · todos opcionales")
        A.alertMenu=w
        for i,item in ipairs({{"pet","Demonio muerto/ausente"},{"nightfall","Nightfall"},{"shards","Pocas Soul Shards"},{"totems","Tótems identificados"}}) do
            local key,text=item[1],item[2]
            local b=CreateFrame("CheckButton",nil,w,"UICheckButtonTemplate")
            b:SetPoint("TOPLEFT",16,-36-(i-1)*32); checkLabel(b,text); b:SetChecked(MuchamielLockPvPDB.alerts[key])
            b:SetScript("OnClick",function(self) MuchamielLockPvPDB.alerts[key]=self:GetChecked() and true or false end)
        end
        button(w,"Umbral shards −",16,-182,function() MuchamielLockPvPDB.shardMinimum=math.max(0,MuchamielLockPvPDB.shardMinimum-1); print("Umbral shards: "..MuchamielLockPvPDB.shardMinimum) end,150)
        button(w,"Umbral shards +",182,-182,function() MuchamielLockPvPDB.shardMinimum=math.min(50,MuchamielLockPvPDB.shardMinimum+1); print("Umbral shards: "..MuchamielLockPvPDB.shardMinimum) end,150)
    end,180)
    local status=label(f,"Perfil activo: "..MuchamielLockPvPDB.profile.." · /mlp diag para diagnóstico",12)
    status:SetPoint("BOTTOMLEFT",18,26)
    f:SetScript("OnShow",function() refresh(); status:SetText("Perfil activo: "..MuchamielLockPvPDB.profile.." · /mlp diag para diagnóstico") end)
end

local events=CreateFrame("Frame")
events:RegisterEvent("ADDON_LOADED")
events:SetScript("OnEvent",function(_,event,name)
    if name~=addonName then return end
    local _,class=UnitClass("player")
    if class~="WARLOCK" then print("Muchamiel Lock PvP: este addon es para brujo."); return end
    MuchamielLockPvPDB=MuchamielLockPvPDB or copy(defaults)
    for k,v in pairs(defaults) do if MuchamielLockPvPDB[k]==nil then MuchamielLockPvPDB[k]=type(v)=="table" and copy(v) or v end end
    for _,name in ipairs({"Duelos","BGs"}) do
        local p=MuchamielLockPvPDB.profiles[name] or {enabled={},positions={}}
        p.enabled=p.enabled or {}; p.positions=p.positions or {}
        for i,m in ipairs(modules) do
            local key=m[1]
            if p.enabled[key]==nil then p.enabled[key]=key=="enemyCDs" or key=="enemyBuffs" or key=="totems" end
            p.positions[key]=p.positions[key] or {x=(i%2==1 and -155 or 155),y=180-math.floor((i-1)/2)*94}
        end
        MuchamielLockPvPDB.profiles[name]=p
    end
    if not MuchamielLockPvPDB.profiles[MuchamielLockPvPDB.profile] then MuchamielLockPvPDB.profile="Duelos" end
    for i,m in ipairs(modules) do panel(m[1],m[2],i) end
    SLASH_MUCHAMIELLOCKPVP1="/mlp"
    SlashCmdList.MUCHAMIELLOCKPVP=function(msg)
        if msg=="rival" then NS.EnemyPvP:menu()
        elseif msg=="reset" then NS.EnemyPvP:clear(); print("Observaciones del rival reiniciadas")
        elseif msg=="diag" then
            local version,build,_,interface=GetBuildInfo()
            print("Muchamiel Lock PvP alpha 0.2.0 · "..plain(version).." / "..plain(build).." / "..plain(interface))
            print("Auras: "..tostring(C_UnitAuras~=nil).." · C_Spell: "..tostring(C_Spell~=nil).." · Nameplates: "..tostring(C_NamePlate~=nil))
            print("Base CD: "..tostring(type(GetSpellBaseCooldown)=="function").." · eventos legibles observados: "..NS.EnemyPvP.eventCount)
        else A:menu() end
    end
    events:SetScript("OnUpdate",function(_,dt)
        A.elapsed=A.elapsed+dt
        if A.elapsed>=0.25 then
            A.elapsed=0
            local ok,err=pcall(function() A:update() end)
            if not ok and not A.reported then A.reported=true; print("Muchamiel Lock PvP: error de compatibilidad: "..plain(err)) end
        end
    end)
    print("Muchamiel Lock PvP alpha 0.2.0 cargado. /mlp abre módulos; /mlp rival abre CDs. Necesita validación en Forever.")
end)
