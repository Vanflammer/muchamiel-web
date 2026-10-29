from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/'research'/'talents.json').read_text(encoding='utf-8'))

def points(s):return {k.strip():int(v) for item in s.split(';') if item.strip() for k,v in [item.rsplit(':',1)]}
def build(name,allocation,use,limits):return dict(name=name,allocation=[points(s) for s in allocation],use=use,limits=limits)
BUILDS={
'Warrior':[
build('Armas + crítico · 21/5/0',['Deflection:5;Improved Rend:3;Improved Tactical Mastery:5;Improved Overpower:2;Anger Management:1;Deep Wounds:3;Spearing Strike:1;Sweeping Strikes:1','Cruelty:5',''],'Primera comparación para duelos y mundo abierto: movilidad entre actitudes, daño de arma y herramientas de Armas. Sweeping Strikes gana interés con dos objetivos próximos en BG.','Sin Mortal Strike: es un capstone de 31 puntos. Sweeping Strikes no sustituye un efecto de reducción de curas.'),
build('Furia de presión · 0/26/0',['','Cruelty:5;Unbridled Wrath:5;Furious Precision:3;Piercing Howl:1;Blood Craze:3;Enrage:5;Raging Blows:1;Improved Berserker Rage:1;Death Wish:1;Flurry:1',''],'Alternativa ofensiva para perseguir y mantener presión; Piercing Howl ayuda a crear distancia o alcanzarla.','Sin Bloodthirst y solo Flurry 1/5. Death Wish tiene un coste defensivo: no es un botón que debas consumir siempre al abrir.'),
build('Protección de control · 0/0/26',['','','Shield Specialization:5;Iron Will:5;Anticipation:3;Improved Revenge:3;Last Stand:1;Master of Defense:2;Improved Shield Bash:2;Concussion Blow:1;Focused Rage:3;Bastion:1'],'Opción de control y supervivencia con escudo para comparar en objetivos de BG y duelos físicos.','Es una opción de nicho para matar rivales que pueden curarse. No incluye Shield Slam y Bastion queda en 1/5.')],
'Paladin':[
build('Reprensión con fuerza · 5/0/21',['Divine Strength:5','','Benediction:5;Deflection:1;Improved Judgement:2;Conviction:5;Sanctified Judgement:3;Seal of Command:1;Pursuit of Justice:2;Sacred Arbiter:1;Repentance:1'],'Primera prueba para duelos y mundo abierto: daño de arma, movilidad y un control para preparar una cura o ventana de daño.','Sin habilidades de 31 puntos. Repentance puede romperse con daño; no la mezcles automáticamente con ataques.'),
build('Sagrado / Holy Shock · 26/0/0',['Divine Intellect:5;Healing Light:3;Spiritual Focus:2;Unyielding Faith:2;Reverence:3;Purifying Power:2;Illumination:3;Divine Favor:1;Holy Shock:1;Divine Precision:3;Holy Power:1','',''],'Primera comparación de apoyo y curas en BG; permite una variante de daño y cura con Holy Shock.','No convierte una build de curas en una ganadora de duelos. Prioriza maná, vida y decisiones de cura; Holy Power es solo 1/5.'),
build('Protección / control · 0/26/0',['','Toughness:5;Redoubt:5;Precision:3;Guardian\'s Favor:2;Sacred Duty:2;Shield Specialization:3;One-Handed Weapon Specialization:3;Improved Hammer of Justice:1;Templar\'s Bulwark:1;Reckoning:1',''],'Nicho defensivo con escudo: proteger aliados y comparar respuesta a presión física.','Pierde Repentance y Holy Shock. No confundir Templar\'s Bulwark con Holy Shield de la última fila.')],
'Hunter':[
build('Bestias con crítico · 21/5/0',['Endurance Training:5;Deadly Aspects:3;Focused Fire:2;Improved Revive Pet:2;Bestial Swiftness:1;Unleashed Fury:5;Summon Hawk:1;Improved Mend Pet:1;Intimidation:1','Lethal Attacks:5',''],'Primera prueba de duelos y mundo abierto con mascota: daño sostenido y control de Intimidation.','Sin Bestial Wrath. No presupone que la mascota sea inmune a Fear o a control.'),
build('Puntería / Scatter · 5/21/0',['Endurance Training:5','Hawk Eye:3;Lethal Attacks:5;Careful Aim:5;Efficiency:1;Improved Concussive Shot:1;Mortal Shots:4;Trueshot Aura:1;Scatter Shot:1',''],'Comparación de distancia y control; Scatter ayuda a preparar recolocación o una trampa.','La build conserva mascota y no compra Lone Wolf. No añade Sniper Shot, talento de 31 puntos.'),
build('Supervivencia de control · 0/0/26',['','','Improved Tracking:5;Deflection:5;Survivalist:5;Improved Wing Clip:3;Clever Traps:2;Deterrence:1;Counterattack:1;Survival Tactics:2;Strider Kick:1;Resourcefulness:1'],'Alternativa para presión cercana, trampas y control en BG o mundo abierto.','No equivale a una build con todos los talentos de daño a distancia. Counterattack y Strider Kick tienen sus requisitos; comprueba sus tooltips.')],
'Rogue':[
build('Sutileza / Preparation · 4/0/22',['Malice:4','','Camouflage:5;Master of Deception:3;Opportunity:2;Elusiveness:2;Dirty Tricks:2;Initiative:1;Ghostly Strike:1;Premeditation:1;Serrated Blades:3;Preparation:1;Hemorrhage:1'],'Primera candidata de control y recuperación de recursos defensivos: sigilo, preparación de ventanas y reinicios.','Sin capstone de 31 puntos. Preparation no reinicia cualquier habilidad arbitrariamente: revisa la lista de su tooltip.'),
build('Asesinato / Mutilate · 21/5/0',['Malice:5;Ruthlessness:3;Murder:2;Lethality:5;Vile Poisons:4;Cold Blood:1;Mutilate:1','Improved Sinister Strike:2;Improved Eviscerate:3',''],'Comparación de presión con dagas y venenos; Cold Blood queda separado para elegir la ventana.','Mutilate requiere su equipamiento y condiciones. Sin Venom, Preparation ni Blade Flurry.'),
build('Combate / movilidad · 5/21/0',['Malice:5','Improved Sinister Strike:2;Lightning Reflexes:3;Deflection:3;Precision:3;Endurance:2;Improved Sprint:2;Riposte:1;Improved Kick:2;Flawless Execution:1;Dual Wield Specialization:1;Blade Flurry:1',''],'Comparación de presión frontal y Sprint mejorado; Blade Flurry puede servir con dos enemigos próximos.','Sin Adrenaline Rush. No trata el daño frontal como reemplazo del control contra casters.')],
'Priest':[
build('Sombra con utilidad · 5/0/21',['Twin Disciplines:5','','Shadow Focus:3;Blackout:5;Improved Shadow Word: Pain:2;Shadow Reach:2;Improved Psychic Scream:2;Mind Flay:1;Improved Mind Flay:2;Vampiric Embrace:1;Shadow Weaving:2;Silence:1'],'Primera prueba de daño en duelos y mundo abierto; conserva curas y añade Silence con sus talentos.','No tiene Shadowform: capstone de 31 puntos. No uses macros que supongan salir de una forma que no puedes aprender.'),
build('Disciplina / Penance · 26/0/0',['Twin Disciplines:5;Improved Power Word: Shield:3;Holy Precision:3;Martyrdom:2;Meditation:3;Mental Agility:3;Inner Focus:1;Soul Warding:1;Mental Strength:3;Improved Mana Burn:1;Penance:1','',''],'Primera comparación de curas y apoyo en BG; en duelos permite probar desgaste, dispels y Mana Burn.','Pierde Silence y Mind Flay. No gana Power Infusion ni habilidades de 31 puntos.'),
build('Sagrado de apoyo · 0/26/0',['','Holy Specialization:5;Improved Renew:3;Twilight Focus:2;Spell Warding:5;Divine Fury:5;Binding Heal:1;Holy Nova:1;Spiritual Guidance:3;Spirit of Redemption:1',''],'Alternativa de curas con herramientas para grupos y supervivencia mágica.','Spirit of Redemption no se convierte en plan para ganar duelos: no todos los finales de duelo son una muerte. Sin Circle/Prayer de capstone.')],
'Shaman':[
build('Elemental de distancia · 26/0/0',['Concussion:5;Convection:3;Elemental Warding:3;Reverberation:3;Elemental Focus:1;Elemental Alacrity:3;Eye of the Storm:2;Earthbound:1;Elemental Reach:2;Lava Burst:1;Lightning Overload:2','',''],'Primera comparación caster para duelos, BG y mundo abierto: daño a distancia con shocks y control.','Con Lava Burst: desde el parche del 15-10 está en la fila 5. Chain Lightning empieza al 32; no forma parte de este nivel.'),
build('Mejora de presión · 0/26/0',['','Thundering Strikes:5;Ancestral Knowledge:5;Mental Dexterity:3;Improved Ghost Wolf:2;Shamanistic Focus:1;Elemental Weapons:3;Stormstrike:1;Flurry:3;Spirit Weapons:1;Mental Quickness:2',''],'Primera comparación cuerpo a cuerpo y movilidad: daño de arma, shocks y Stormstrike.','No tiene Maelstrom Weapon ni un capstone de 31 puntos. No asumas curas instantáneas ilimitadas.'),
build('Restauración / emergencia · 0/0/26',['','','Improved Healing Wave:5;Totemic Focus:5;Mindfulness:3;Tidal Focus:2;Healing Focus:3;Water Shield:1;Mana Tide Totem:1;Tidal Mastery:4;Nature\'s Swiftness:1;Living Spirit:0;Healing Way:1'],'Primera comparación de curas y soporte en BG, con Nature\'s Swiftness para una emergencia.','Sin Riptide. Curas y tótems no eliminan la necesidad de controlar el alcance y proteger tu escuela de Naturaleza.')],
'Mage':[
build('Escarcha de PvP · 0/0/26',['','','Improved Frostbolt:5;Elemental Precision:1;Permafrost:3;Frostbite:3;Improved Frost Nova:2;Ice Lance:1;Piercing Ice:3;Frost Channeling:1;Ice Block:1;Shatter:3;Cold Snap:1;Fingers of Frost:2'],'Primera prueba de duelos, BG y mundo abierto: slows, freezes, Ice Block y Cold Snap.','Sin Ice Barrier de 31 puntos. Ice Lance, Ice Block y Cold Snap aquí dependen de talentos.'),
build('Fuego con defensa de hielo · 0/21/5',['','Improved Fireball:5;Ignite:5;Flame Throwing:2;Impact:3;Burning Soul:3;Pyroblast:1;Heating Up:1;Blast Wave:1','Improved Frostbolt:5'],'Alternativa de presión y burst con ventanas de control; el primer rango de Frostbolt sigue siendo una decisión manual.','Sin Ice Block ni Cold Snap. Heating Up no implica automáticamente Hot Streak de última fila.'),
build('Arcano de control · 26/0/0',['Arcane Focus:5;Arcane Concentration:5;Magic Absorption:2;Arcane Resilience:2;Arcane Blast:1;Arcane Impact:3;Improved Counterspell:2;Missile Barrage:1;Arcane Meditation:3;Presence of Mind:1;Arcane Mind:1','',''],'Comparación de daño y control con Presence of Mind, Counterspell mejorado y Arcane Blast.','Sin Arcane Power de 31 puntos. No dispone de las defensas talentadas de Escarcha; Arcane Blast exige gestionar maná.')],
'Druid':[
build('Feral con Furor · 0/21/5',['','Ferocity:5;Heart of the Wild:3;Feral Swiftness:2;Brutal Impact:2;Thick Hide:3;Sharpened Claws:2;Savage Fury:2;Feral Charge:1;Leader of the Pack:1','Furor:5'],'Primera comparación de duelos y mundo abierto: movilidad, cambios de forma y presión física.','Sin Shifting Power ni Primal Bite en este reparto; no copies sus macros como si fueran basales.'),
build('Equilibrio de desgaste · 26/0/0',['Improved Wrath:5;Genesis:3;Moonglow:3;Improved Moonfire:2;Nature\'s Majesty:2;Nature\'s Reach:2;Nature\'s Splendor:1;Improved Entangling Roots:2;Insect Swarm:1;Vengeance:2;Nature\'s Grace:1;Eclipse:2','',''],'Comparación caster en duelos y BG: daño periódico, raíces y oportunidades de lanzar.','Sin Moonkin Form de 31 puntos. Sigue necesitando pasar a curas y formas según la presión.'),
build('Restauración con movilidad · 0/5/21',['','Heart of the Wild:5','Nature\'s Focus:5;Naturalist:5;Natural Shapeshifter:3;Reflection:3;Gift of Nature:3;Swiftmend:1;Nature\'s Swiftness:1'],'Primera comparación de curas y movilidad en BG; también sirve para probar duelos de recursos.','Sin Wild Growth de 31 puntos. Swiftmend exige un objetivo con los efectos que su tooltip requiere; no cura por pulsar sin cumplirlos.')]
}

def validate():
    errors=[]
    for cls,builds in BUILDS.items():
        trees=DATA['talents'][cls]['trees']
        for b in builds:
            # Zero entries do not belong to an allocation.
            b['allocation']=[{k:v for k,v in a.items() if v} for a in b['allocation']]
            total=sum(sum(a.values()) for a in b['allocation'])
            if total!=26:errors.append((cls,b['name'],'total',total))
            for tree,a in zip(trees,b['allocation']):
                talents={t['name']:t for t in tree['talents']}
                for name,rank in a.items():
                    if name not in talents:errors.append((cls,b['name'],'unknown',name));continue
                    t=talents[name]
                    if not 0<rank<=t['max']:errors.append((cls,b['name'],'rank',name))
                    lower=sum(v for n,v in a.items() if n in talents and talents[n]['row']<t['row'])
                    if lower<(t['row']-1)*5:errors.append((cls,b['name'],'row',name,lower))
                    if t.get('req') and a.get(t['req'],0)<talents[t['req']]['max']:errors.append((cls,b['name'],'req',name,t['req']))
    return errors
if __name__=='__main__':
    e=validate();print(json.dumps(e,ensure_ascii=False));raise SystemExit(bool(e))
