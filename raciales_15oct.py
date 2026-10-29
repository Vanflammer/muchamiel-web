"""Raciales reescritas a mano con las notas de la beta del 15-10 (Van, 16-10-2026). Los textos de Razas y Macros salen de
Talents Forever (datos del 8-10) y vienen ya metidos en las páginas de base-gpt. Se cambia el bloque «nombre</h3><p>texto</p>»
de cada racial, nunca el nombre suelto: Sword/Mace/Axe Specialization también son talentos del Guerrero.
Cuando Talents Forever actualice sus datos, comprobar y quitar lo que sobre."""
import html
import re

# (nombre viejo, texto viejo, nombre nuevo, texto nuevo)
RACIALES = [
    ('Endurance', 'Total Health increased by 5% and chance to hit increased by 1%.',
     'Endurance', 'Total Health increased by 5% and critical damage and healing increased by 2%.'),
    ('Plainsrunning', 'Gain 1% increased movement speed every 5 sec spent moving, up to a maximum of 30% increase. Taking damage or standing still will reduce this effect.',
     'Plainsrunning', 'Gain 1% increased movement speed every 5 sec spent moving, up to a maximum of 30% increase. Taking damage, standing still or moving less than a minimum distance per second will reduce this effect. Also increases mounted movement speed by 3%.'),
    ('Cultivation', 'Instant. Cultivate a nearby herb, growing a duplicate you can harvest without requiring Herbalism skill. Each herb may only be cultivated once. In play it goes on a 1 hour cooldown, though its tooltip shows none.',
     'Cultivation', 'Instant, 15 min cooldown. Cultivate a nearby herb, growing a duplicate you can harvest without requiring Herbalism skill. Each herb may only be cultivated once.'),
    ('War Stomp', '0.5 sec cast, 2 min cooldown. Stuns up to 5 enemies within 8 yds for 2 sec.',
     'War Stomp', '0.5 sec cast, 90 sec cooldown. Stuns up to 5 enemies within 8 yds for 2 sec.'),
    ('Mace Specialization', 'Increases your critical strike chance with all spells and attacks by 1% while you have a mace or two-handed mace equipped.',
     'Earth Fury', 'Critical damage and healing increased by 2%.'),
    ('Find Treasure', 'Instant. Allows the dwarf to sense nearby treasure, making it appear on the minimap.  Lasts until canceled.',
     'Find Treasure', 'Instant. Allows the dwarf to sense nearby treasure, making it appear on the minimap. Also grants a chance to find additional items in most chests. Lasts until canceled.'),
    ('Wind Blessed', 'Increases your spellcasting, melee, and ranged Haste by 1%.',
     'Wind Blessed', 'Increases your spellcasting, melee, and ranged Haste by 3%.'),
    ('Skysight', '0.5 sec cast, 2 min cooldown. Attempt to draw power from a convergence of elements and receive its blessing, increasing your movement and mounted movement speeds by 10%. Lasts 30 sec if no elemental convergence is nearby, and 15 min if one is found.',
     'Skysight', '0.5 sec cast, 2 min cooldown, castable while moving. Attempt to draw power from a convergence of elements and receive its blessing, increasing your movement and mounted movement speeds by 10%. Lasts 30 sec if no elemental convergence is nearby, and 15 min if one is found.'),
    ('Read Ley Line', '2 sec cast, 2 min cooldown. Attempt to tap into the power of a nearby ley line, increasing your Health and Mana regeneration by 100%. Lasts 15 sec if no ley line is nearby, and 15 min if one is found.',
     'Read Ley Line', '2 sec cast, 2 min cooldown, castable while moving. Attempt to tap into the power of a nearby ley line, increasing your Health and Mana regeneration by 100%. Lasts 30 sec if no ley line is nearby, and 15 min if one is found.'),
    ('Walk on Air', 'Instant, 2 min cooldown. Glide downward through the air for 10 sec while controlling your direction of travel.',
     'Walk on Air', 'Instant, 90 sec cooldown. Glide downward through the air for 10 sec while controlling your direction of travel.'),
    ('Sword Specialization', 'Increases your critical strike chance with all spells and attacks by 2% while you have a sword or two-handed sword equipped.',
     'Ruthless', 'Increases your critical strike chance by 2%.'),
    ('Axe Specialization', 'Increases your critical strike chance with all spells and abilities by 1% while you have an axe or a two-handed axe equipped.',
     'Savage', 'Increases your critical strike chance by 1%.'),
    ('Blood Fury', 'Instant, 2 min cooldown. Increases Attack Power and Spell Power by 10% for 15 sec.',
     'Blood Fury', 'Instant, 3 min cooldown. Increases Attack Power and Spell Power by 10% for 15 sec.'),
    ('Shatter Curse', 'Instant, 3 min cooldown. Instantly removes and grants immunity to all Curses and Banes, and reduces all Magical damage taken by 15% for 8 sec.',
     'Shatter Curse', 'Instant, 3 min cooldown. Instantly removes all Curses and Banes, and reduces all Magical damage taken by 5% for 8 sec.'),
    ('Will of the Forsaken', 'Instant, 2 min cooldown. Instantly removes all Charm, Fear and Sleep effects.',
     'Will of the Forsaken', 'Instant, 2 min cooldown. Instantly removes all Charm, Fear and Sleep effects. Not usable while under Scatter Shot.'),
    ('Touch of the Grave', 'Your spells and attacks with a damage part have a chance (10% for casters, 5% for melee) to drain Health from the target, up to 5% of your maximum Health. 1 sec internal cooldown. Does not break crowd control.',
     'Touch of the Grave', 'Your spells and attacks with a damage part have a chance (30% for casters, 20% for Paladins, Rogues and Warriors) to drain Health from the target, up to 5% of your maximum Health. 25 sec internal cooldown. Does not scale with Shadow damage increases, and using a lower rank of a spell no longer reduces it. Does not break crowd control.'),
    ('Eureka!', "Instant, 2 min cooldown. Your next 3 non-periodic damaging abilities cost 10% less (Mana, Rage or Energy) and deal 10% more damage. For Priests, your next 3 non-periodic damaging or healing abilities cost 10% less Mana and do 10% more damage or healing. Periodic effects get nothing from it; a channeled spell is not periodic. The Mage's own tooltip is the one that leaves out non-periodic.",
     'Eureka!', 'Instant, 2 min cooldown. For 8 sec, your non-periodic damaging abilities cost 10% less (Mana, Rage or Energy) and deal 10% more damage; for Priests, also healing and Power Word: Shield. Works while stealthed or invisible.'),
    ('Quickness', 'Dodge chance increased by 1% and movement speed increased by 2%. Night Elf Rogues and Druids are harder to detect in Stealth as if they were 1 level higher.',
     'Quickness', 'Dodge chance increased by 1% and movement speed increased by 2%; this stacks with other movement speed increases. Night Elf Rogues and Druids are harder to detect in Stealth as if they were 1 level higher.'),
    ('Regeneration', 'Health regeneration rate increased by 10%. In addition, 10% of total Health regeneration will continue during combat.',
     'Regeneration', 'Health regeneration rate increased by 20%. In addition, 20% of total Health regeneration will continue during combat.'),
]


# Van 26-10: repaso final de raciales de Blizzard (26-10-2026). Se aplica DESPUÉS de RACIALES, sobre los textos ya cambiados.
RACIALES_26 = [
    ('Ruthless', 'Increases your critical strike chance by 2%.',
     'Ruthless', 'Increases your critical strike chance by 1%.'),
    ('Human Spirit', 'Spirit increased by 5%.',
     'Human Spirit', 'Spirit increased by 10%.'),
    ('Earth Fury', 'Critical damage and healing increased by 2%.',
     "Artisan's Precision", 'Increases your chance to hit with spells and attacks by 1%.'),
    ('Endurance', 'Total Health increased by 5% and critical damage and healing increased by 2%.',
     'Endurance', 'Total Health increased by 5%.'),
    ('Plainsrunning', 'Gain 1% increased movement speed every 5 sec spent moving, up to a maximum of 30% increase. Taking damage, standing still or moving less than a minimum distance per second will reduce this effect. Also increases mounted movement speed by 3%.',
     'Plainsrunning', 'Gain 2% increased movement speed every 5 sec spent moving, up to a maximum of 60% increase. Taking damage, standing still or moving less than a minimum distance per second will reduce this effect. Does not increase mounted movement speed.'),
    ('Savage', 'Increases your critical strike chance by 1%.',
     'Command', 'Damage dealt by Hunter and Warlock pets increased by 5%.'),
    ('Wind Blessed', 'Increases your spellcasting, melee, and ranged Haste by 3%.',
     'Wind Blessed', 'Increases your spellcasting, melee, and ranged Haste by 2%.'),
    ('Skysight', '0.5 sec cast, 2 min cooldown, castable while moving. Attempt to draw power from a convergence of elements and receive its blessing, increasing your movement and mounted movement speeds by 10%. Lasts 30 sec if no elemental convergence is nearby, and 15 min if one is found.',
     'Skysight', '0.5 sec cast, 2 min cooldown, castable while moving. Increases your movement speed by 15% for 15 sec. If used at an elemental convergence, also grants Charged for 1 hour: while Charged, Skysight increases movement speed by 30%. Charged persists through death.'),
    ('Read Ley Line', '2 sec cast, 2 min cooldown, castable while moving. Attempt to tap into the power of a nearby ley line, increasing your Health and Mana regeneration by 100%. Lasts 30 sec if no ley line is nearby, and 15 min if one is found.',
     'Read Ley Line', '2 sec cast, 2 min cooldown, castable while moving. Increases your Health and Mana regeneration by 50% for 15 sec. Cannot be used while Innervate is active. If used at a ley line, also grants Attuned for 1 hour: while Attuned, Read Ley Line increases regeneration by 100%. Attuned persists through death.'),
    # 27-10: añadidos de Blizzard al mismo aviso (orco, trol, no-muerto) y aclaración de los célicos
    ('Blood Fury', 'Instant, 3 min cooldown. Increases Attack Power and Spell Power by 10% for 15 sec.',
     'Blood Fury', 'Instant, 2 min cooldown. Increases Attack Power and Spell Power by 10% for 15 sec.'),
    ('Berserking', 'Instant, 3 min cooldown. Increases your spellcasting and attack speed by 10% for 10 sec.',
     'Berserking', 'Instant, 3 min cooldown. Increases your spellcasting and attack speed by 10% for 15 sec.'),
    ('Touch of the Grave', 'Your spells and attacks with a damage part have a chance (30% for casters, 20% for Paladins, Rogues and Warriors) to drain Health from the target, up to 5% of your maximum Health. 25 sec internal cooldown. Does not scale with Shadow damage increases, and using a lower rank of a spell no longer reduces it. Does not break crowd control.',
     'Touch of the Grave', 'Your spells and attacks with a damage part have a chance (30% for casters, 20% for Paladins, Rogues and Warriors) to drain Health from the target, up to 5% of your maximum Health. 15 sec internal cooldown. Does not scale with Shadow damage increases, and using a lower rank of a spell no longer reduces it. Does not break crowd control.'),
    ('Skysight', '0.5 sec cast, 2 min cooldown, castable while moving. Increases your movement speed by 15% for 15 sec. If used at an elemental convergence, also grants Charged for 1 hour: while Charged, Skysight increases movement speed by 30%. Charged persists through death.',
     'Skysight', '0.5 sec cast, 2 min cooldown, castable while moving. Increases your movement speed by 15% for 15 sec. If used at an elemental convergence, also grants Charged for 1 hour: while Charged, Skysight increases movement speed by 30%. Charged persists through death and is removed upon entering a raid.'),
    ('Read Ley Line', '2 sec cast, 2 min cooldown, castable while moving. Increases your Health and Mana regeneration by 50% for 15 sec. Cannot be used while Innervate is active. If used at a ley line, also grants Attuned for 1 hour: while Attuned, Read Ley Line increases regeneration by 100%. Attuned persists through death.',
     'Read Ley Line', '2 sec cast, 2 min cooldown, castable while moving. Increases your Health and Mana regeneration by 50% for 15 sec. Cannot be used while Innervate is active. If used at a ley line, also grants Attuned for 1 hour: while Attuned, Read Ley Line increases regeneration by 100%. Attuned persists through death and is removed upon entering a raid.'),
]


def aplicar(s):
    """Cambia en la página los bloques de raciales; devuelve (página, número de bloques cambiados)."""
    n = 0
    for vn, vt, nn, nt in RACIALES + RACIALES_26:
        for esc in (lambda t: html.escape(t, quote=False), html.escape):
            a, b = f'{vn}</h3><p>{esc(vt)}</p>', f'{nn}</h3><p>{esc(nt)}</p>'
            if a in s:
                n += s.count(a)
                s = s.replace(a, b)
    # Las descripciones de las páginas de raza nombran sus raciales: las renombradas, también ahí.
    nuevos = {vn: nn for vn, _, nn, _ in RACIALES + RACIALES_26 if vn != nn}
    for k in list(nuevos):  # cadenas: Mace Specialization → Earth Fury → Artisan's Precision
        while nuevos[k] in nuevos:
            nuevos[k] = nuevos[nuevos[k]]
    s = re.sub(r'content="Raciales de [^"]*"', lambda m: re.sub('|'.join(map(re.escape, nuevos)), lambda x: nuevos[x[0]], m[0]), s)
    return s, n
