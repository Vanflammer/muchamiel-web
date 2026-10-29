"""Notas de la beta del 15 de octubre de 2026 (Kaivax, foro de Blizzard, publicadas el 16-10 a las 00:15 UTC), en castellano
y en inglés. cambios_beta.py la pone la primera de PARCHES; el inglés se vuelca en traducciones/en.json (añadir_en)."""
# (signo, castellano, inglés)
GENERAL = [
    ('●', 'Varitas y Auto Shot del cazador: hay que estar quieto 0,5 s antes de disparar, como en las primeras versiones de WoW.',
          'Wands and the Hunter\'s Auto Shot: you must stand still for 0.5 sec before shooting, as in early versions of WoW.'),
    ('●', 'Muchas auras y gritos pasan a afectar a toda la banda: Battle Shout, Trueshot Aura, Leader of the Pack, Moonkin Aura y los tótems Grace of Air, Strength of Earth, Windfury y Flametongue.',
          'Many auras and shouts become raid-wide: Battle Shout, Trueshot Aura, Leader of the Pack, Moonkin Aura and the Grace of Air, Strength of Earth, Windfury and Flametongue totems.'),
    ('▲', 'Nuevo tutorial para jugadores nuevos y opción «Ataque automático / Disparo automático» para que el cazador cambie solo entre uno y otro (también con mando).',
          'New tutorial for new players and an “Auto Attack/Auto Shot” option so Hunters switch between them automatically (gamepad too).'),
    ('●', 'Las criaturas recuperan vida fuera de combate. Los pergaminos activan el tiempo global. Draught of Predatory Senses pasa a ser poción de combate, con menos duración.',
          'Creatures regenerate health out of combat. Scrolls trigger the global cooldown. Draught of Predatory Senses becomes a combat potion with a shorter duration.'),
    ('●', 'Dalaran: la Horda ya no es bienvenida en la ciudad y la atacan nada más verla. La mazmorra de la Ciudad de Dalaran sigue siendo accesible.',
          'Dalaran: the Horde is no longer welcome in the city and is attacked on sight. The City of Dalaran dungeon is still accessible.'),
    ('▲', 'Las Marcas de Honor de campo de batalla se acumulan hasta 30 (eran 20).', 'Battleground Marks of Honor stack up to 30 (was 20).'),
    ('●', 'Legado: Bartering ya no descuenta el entrenamiento ni las reparaciones. The Quick and the Dead afecta a más hechizos de sacerdote.',
          'Legacy: Bartering no longer discounts training and repairs. The Quick and the Dead affects more Priest spells.'),
    ('●', 'Interfaz: nuevos marcos de unidad, columna de nivel equipable en la subasta, más opciones de texto de combate, y menos placas de nombre de enemigos situados muy por encima o por debajo de ti.',
          'Interface: new unit frames, an equippable level column in the Auction House, more combat text options, and fewer nameplates for enemies far above or below you.'),
]
CLASES = {
    ('Razas', 'Races'): [
        ('▲', 'Tauren: Endurance da un 2 % de daño y sanación críticos (era 1 % de golpe). Plainsrunning suma un 3 % de velocidad montado, pero ya no se mantiene a base de pasitos. Cultivation baja a 15 min (era 60) y War Stomp a 90 s (eran 2 min).',
              'Tauren: Endurance grants 2% critical damage and healing (was 1% hit). Plainsrunning also grants 3% mounted speed, but stutter-stepping no longer keeps it up. Cultivation down to 15 min (was 60) and War Stomp to 90 sec (was 2 min).'),
        ('●', 'Enano: Mace Specialization pasa a ser Earth Fury (2 % de daño y sanación críticos). Find Treasure puede dar objetos extra en los cofres.',
              'Dwarf: Mace Specialization becomes Earth Fury (2% critical damage and healing). Find Treasure can find extra items in chests.'),
        ('▲', 'Célicos: Wind Blessed sube al 3 % de celeridad (era 1 %). Skysight y Read Leyline se lanzan en movimiento. Walk on Air baja a 90 s (eran 2 min). Más Convergencias Elementales y Líneas Ley por el mundo.',
              'Skyborne: Wind Blessed up to 3% haste (was 1%). Skysight and Read Leyline castable while moving. Walk on Air down to 90 sec (was 2 min). More Elemental Convergences and Leylines around the world.'),
        ('●', 'Humano: Sword Specialization pasa a ser Ruthless (2 % de probabilidad de crítico).', 'Human: Sword Specialization becomes Ruthless (2% critical strike chance).'),
        ('▼', 'Orco: Axe Specialization pasa a ser Savage (1 % de crítico). Blood Fury sube a 3 min (eran 2). Shatter Curse ya no da inmunidad: disipa maldiciones y Banes y reduce el daño mágico un 5 % (era 15 %).',
              'Orc: Axe Specialization becomes Savage (1% crit). Blood Fury up to 3 min (was 2). Shatter Curse no longer grants immunity: it dispels Curses and Banes and reduces magic damage taken by 5% (was 15%).'),
        ('▼', 'No-muerto: sin Will of the Forsaken bajo Scatter Shot. Touch of the Dead: 30 % de probabilidad para lanzadores y 20 % para paladines, pícaros y guerreros, con 25 s de reutilización interna, y ya no escala con aumentos de sombras.',
              'Undead: no Will of the Forsaken under Scatter Shot. Touch of the Dead: 30% chance for casters and 20% for Paladins, Rogues and Warriors, with a 25 sec internal cooldown, and no longer scales with Shadow increases.'),
        ('●', 'Gnomo: Eureka! pasa a ser un beneficio de 8 s sin cargas, con el mismo efecto, y ahora también vale para Power Word: Shield. Además, ya funciona bien en sigilo y con invisibilidad (antes fallaba).',
              'Gnome: Eureka! becomes an 8 sec buff with no charges and the same effect, now also for Power Word: Shield. It also works properly in stealth and invisibility now (it was bugged).'),
        ('▲', 'Elfo de la noche: Quickness se acumula con otros aumentos de velocidad.', 'Night Elf: Quickness stacks with other movement speed increases.'),
        ('▲', 'Trol: Regeneration sube al 20 % (era 10 %).', 'Troll: Regeneration up to 20% (was 10%).'),
    ],
    ('Druida', 'Druid'): [
        ('▲', 'Faerie Fire genera amenaza en forma de oso. Furor conserva la energía que tenías en forma felina aunque pases a oso.',
              'Faerie Fire generates threat in Bear Form. Furor keeps the Energy you had in Cat Form even if you shift to Bear.'),
        ('●', 'Moonkin Aura da solo crítico de hechizos y Leader of the Pack solo crítico cuerpo a cuerpo y a distancia; las dos llegan a toda la banda. Shred se aprende al nivel 20 (era 22).',
              'Moonkin Aura grants only spell crit and Leader of the Pack only melee and ranged crit; both are raid-wide. Shred is learned at level 20 (was 22).'),
        ('▼', 'Omen of Clarity ya no salta con Faerie Fire en formas. Varios Insect Swarm ya no acumulan la reducción de golpe.',
              'Omen of Clarity no longer procs from Faerie Fire in forms. Multiple Insect Swarms no longer stack the hit reduction.'),
        ('●', 'Arreglado: los rangos altos de Rejuvenation ya no impiden que otro druida ponga la suya, y algunos talentos ferales se aplican bien al entrar al juego.',
              'Fixed: high ranks of Rejuvenation no longer block other Druids\' Rejuvenation, and some Feral talents now apply correctly on login.'),
    ],
    ('Cazador', 'Hunter'): [
        ('▼', 'Auto Shot exige estar quieto 0,5 s antes de disparar (sigue disparando mientras lanzas Aimed Shot o Sniper Shot).',
              'Auto Shot requires standing still for 0.5 sec before firing (it still fires while casting Aimed Shot or Sniper Shot).'),
        ('▲', 'Las trampas de fuego escalan con el poder de ataque y puedes tener una de fuego y otra de hielo a la vez. Las mascotas aprovechan Expertise y heredan tu mejor crítico.',
              'Fire traps scale with Attack Power and you can have one Fire and one Ice trap at once. Pets benefit from Expertise and inherit your higher crit chance.'),
        ('▼', 'Mascotas: Dismember (crocolisco) reduce la sanación un 25 % durante 6 s cada 15 s (era 50 %, 10 s, cada 6 s). Sonic Blast (murciélago) 30 % durante 20 s cada 60 s (era 60 %, 30 s, cada 30 s). Mine! (ave de presa) 3 s cada 90 s (era 4 s cada 60 s).',
              'Pets: Dismember (Crocolisk) reduces healing by 25% for 6 sec every 15 sec (was 50%, 10 sec, every 6 sec). Sonic Blast (Bat) 30% for 20 sec every 60 sec (was 60%, 30 sec, every 30 sec). Mine! (Bird of Prey) 3 sec every 90 sec (was 4 sec every 60 sec).'),
        ('▲', 'Bestias: Summon Hawk aparece y se queda en el objetivo, e Improved Mend Pet ya abarata Mend Pet. Puntería: Trueshot Aura a toda la banda y Sniper Shot aprovecha más talentos.',
              'Beast Mastery: Summon Hawk spawns on and sticks to the target, and Improved Mend Pet now lowers Mend Pet\'s cost. Marksmanship: Trueshot Aura is raid-wide and Sniper Shot benefits from more talents.'),
        ('●', 'Supervivencia: Strider Kick se puede usar desarmado. Resourcefulness reduce su coste y salta con críticos de habilidades cuerpo a cuerpo y a distancia (no con trampas).',
              'Survival: Strider Kick usable while disarmed. Resourcefulness reduces its cost and procs on melee and ranged ability crits (not traps).'),
    ],
    ('Mago', 'Mage'): [
        ('▲', 'Nuevo hechizo Frost Blast (nivel 24): 1,5 s de lanzamiento, daño de escarcha y ralentiza un 40 %, con los talentos de Frostbolt. Sustituye al truco de usar Frostbolt de rango 1.',
              'New spell Frost Blast (level 24): 1.5 sec cast, Frost damage and a 40% slow, using Frostbolt\'s talents. It replaces the Rank 1 Frostbolt trick.'),
        ('●', 'Arcano: Arcane Blast rehecho: 1,5 s, y cada lanzamiento te da un 15 % del intelecto como daño con hechizos durante 15 s, hasta 4 veces, con un 40 % menos de daño y de coeficiente. Missile Barrage pasa a la primera fila con 2 puntos.',
              'Arcane: Arcane Blast redesigned: 1.5 sec, and each cast grants 15% of your Intellect as spell damage for 15 sec, up to 4 times, with 40% less damage and coefficient. Missile Barrage moves to the first row as a 2-point talent.'),
        ('▲', 'Arcano: nuevo talento de medalla de oro Arcane Wrath (16 puntos): daño parecido a Fireball con 3,5 s de lanzamiento, más daño según el 5 % de tu maná máximo, y 6 s de reutilización.',
              'Arcane: new 16-point gold medal talent Arcane Wrath: Fireball-like damage with a 3.5 sec cast, plus damage based on 5% of your maximum Mana, 6 sec cooldown.'),
        ('●', 'Fuego: Wake of Fire vuelve a ser Improved Fire Blast (+8/15 m de alcance). Critical Mass llega a 5 puntos (10 %). Fire Power rehecho: 1/2/3 % más de daño de fuego por cada efecto de fuego tuyo en el objetivo, hasta un 12 %. Fire Blast da una carga extra de Heating Up.',
              'Fire: Wake of Fire reverts to Improved Fire Blast (+8/15 yd range). Critical Mass goes up to 5 points (10%). Fire Power redesigned: 1/2/3% more Fire damage per Fire effect of yours on the target, up to 12%. Fire Blast grants an extra Heating Up charge.'),
        ('●', 'Escarcha: Ice Lance contra congelados +200 % (era +300 %). Cone of Cold ralentiza más y durante más tiempo a los 4 primeros objetivos. Winter\'s Chill rehecho: tus Frostbolt, Frost Blast e Ice Lance potenciados pueden aplicarlo, y hace que tu siguiente Cone of Cold pegue más (hasta 5 acumulaciones).',
              'Frost: Ice Lance vs frozen targets +200% (was +300%). Cone of Cold slows the first 4 targets more and for longer. Winter\'s Chill redesigned: your Frostbolt, Frost Blast and empowered Ice Lance can apply it, making your next Cone of Cold hit harder (up to 5 stacks).'),
    ],
    ('Paladín', 'Paladin'): [
        ('●', 'Blessing of Salvation y su versión mayor pasan a ser Salvation y Mass Salvation, compatibles con las bendiciones. Nuevo Revoke para quitársela a un miembro del grupo.',
              'Blessing of Salvation and its Greater version become Salvation and Mass Salvation, compatible with blessings. New Revoke to remove it from a group member.'),
        ('▼', 'Consecration: coeficiente por tic 0,042 (era 0,095). Arreglado Seal of Righteousness, que aprovechaba casi el doble del daño con hechizos. Retribución: Champion of the Light da un 10/20/30 % del intelecto (era 20/40/60 %).',
              'Consecration: 0.042 coefficient per tick (was 0.095). Fixed Seal of Righteousness getting almost double benefit from spell damage. Retribution: Champion of the Light grants 10/20/30% of Intellect (was 20/40/60%).'),
        ('▲', 'Righteous Fury: amenaza del daño sagrado al 90 % (era 60 %). Power Word: Shield ya no pisa Seal of Fury.',
              'Righteous Fury: Holy damage threat at 90% (was 60%). Power Word: Shield no longer overwrites Seal of Fury.'),
        ('●', 'Protección: Reckoning vuelve a acumular hasta 4 cargas que salen en tu siguiente golpe, como en Classic Era. Shield Specialization devuelve un 4 % de maná (era 6 %).',
              'Protection: Reckoning stores up to 4 charges again, released on your next swing as in Classic Era. Shield Specialization restores 4% Mana (was 6%).'),
        ('▼', 'Sagrado: arreglado Infusion of Light, que daba un 50 % más de daño a Holy Shock contra enemigos.',
              'Holy: fixed Infusion of Light giving Holy Shock 50% more damage against enemies.'),
    ],
    ('Sacerdote', 'Priest'): [
        ('▲', 'Devouring Plague baja a 24 s de reutilización (era 1 min). Vampiric Embrace a 30 s (era 1 min) y ya no se puede resistir.',
              'Devouring Plague cooldown down to 24 sec (was 1 min). Vampiric Embrace to 30 sec (was 1 min) and it can no longer be resisted.'),
        ('▼', 'Shadow Word: Death sube a 18 s de reutilización (eran 12).', 'Shadow Word: Death cooldown up to 18 sec (was 12).'),
        ('▲', 'Sombra: nuevo talento Dark Inspiration (fila 4): Mind Blast y Mind Flay completo dan un 3-15 % de espíritu a tu grupo durante 10 s. Improved Mind Flay: cada tic pega un 10/20 % más que el anterior. Devouring Contagion salta a 2 objetivos. Fuera Improved Fade y Shadow Infinity.',
              'Shadow: new talent Dark Inspiration (row 4): Mind Blast and a full Mind Flay give your party 3-15% Spirit for 10 sec. Improved Mind Flay: each tick hits 10/20% harder than the last. Devouring Contagion spreads to 2 targets. Improved Fade and Shadow Infinity removed.'),
        ('●', 'Disciplina: Mental Strength sube a la fila 2 y da un 2-10 % de intelecto. Power in Light aumenta Smite y Penance si el objetivo tiene Holy Fire o Shadow Word: Pain. Twin Disciplines ya afecta a Shadow Word: Death, Mind Flay, Starshards y Penance.',
              'Discipline: Mental Strength moves to row 2 and grants 2-10% Intellect. Power in Light increases Smite and Penance if the target has Holy Fire or Shadow Word: Pain. Twin Disciplines now affects Shadow Word: Death, Mind Flay, Starshards and Penance.'),
        ('●', 'Arreglado: los rangos altos de Renew ya no impiden que otro sacerdote ponga la suya.', 'Fixed: high ranks of Renew no longer block other Priests\' Renew.'),
    ],
    ('Pícaro', 'Rogue'): [
        ('▼', 'Los venenos ya no saltan contra quien te ataca. Sap ya no activa efectos de arma. Ya no se puede cambiar de especialización para rellenar la energía.',
              'Poisons no longer proc against attackers. Sap no longer triggers weapon procs. You can no longer swap specs to refill Energy.'),
        ('▲', 'Asesinato: Cold Blood se gasta bien cuando Mutilate hace crítico.', 'Assassination: Cold Blood is correctly consumed when Mutilate crits.'),
    ],
    ('Chamán', 'Shaman'): [
        ('▲', 'Chain Lightning cuesta un 35 % menos de maná. Grace of Air ya es compatible con Windfury y Flametongue (estos dos siguen siendo excluyentes), y los cuatro tótems llegan a toda la banda.',
              'Chain Lightning costs 35% less Mana. Grace of Air no longer conflicts with Windfury and Flametongue (those two still do), and all four totems are raid-wide.'),
        ('▼', 'Fire Nova: mucho menos daño base, coeficiente 0,143 (era 0,214) y mucho menos coste. Grounding Totem se destruye tras redirigir un hechizo.',
              'Fire Nova: much lower base damage, 0.143 coefficient (was 0.214) and much lower cost. Grounding Totem is destroyed after redirecting a spell.'),
        ('●', 'Elemental: vuelve Elemental Mastery como talento de 31 puntos (‑0,5 s a Lightning Bolt y Lava Burst y Chain Lightning sin reutilización durante 15 s, cada 3 min). Lava Burst baja a la fila 5 como talento de 21 puntos, con rango 4. Fuera Call of Thunder; Earthbound pasa a la fila 4.',
              'Elemental: Elemental Mastery returns as the 31-point talent (−0.5 sec on Lightning Bolt and Lava Burst and no Chain Lightning cooldown for 15 sec, every 3 min). Lava Burst moves to row 5 as the 21-point talent, with a rank 4. Call of Thunder removed; Earthbound moves to row 4.'),
        ('●', 'Mejora: Stormstrike cuesta un 8 % del maná base (eran 125 fijos) y su efecto ya no se gasta si el hechizo falla. Restauración: nuevo rango de Mana Tide Totem al nivel 38; Water Shield salta con cualquier crítico de hechizo.',
              'Enhancement: Stormstrike costs 8% of base Mana (was a flat 125) and its debuff is no longer consumed if the spell misses. Restoration: new Mana Tide Totem rank at level 38; Water Shield procs from any spell crit.'),
    ],
    ('Brujo', 'Warlock'): [
        ('▲', 'Aflicción: Shadow Mastery sube a un 2-10 % de daño de sombras (era 1-5 %). Malediction pasa a ser Grim Reach (+10/20 % de alcance a Aflicción), y Destructive Reach hace lo mismo con Destrucción.',
              'Affliction: Shadow Mastery up to 2-10% Shadow damage (was 1-5%). Malediction becomes Grim Reach (+10/20% Affliction range), and Destructive Reach does the same for Destruction.'),
        ('●', 'Arreglado: ya puedes lanzar Soul Link a tu demonio, y el Incubus ya no se invoca gratis con la ventaja de Legado Reagent Economy.',
              'Fixed: you can cast Soul Link on your pet again, and the Incubus is no longer free to summon with the Reagent Economy Legacy perk.'),
    ],
    ('Guerrero', 'Warrior'): [
        ('▲', 'Battle Shout llega a toda la banda. Slam ya no sufre retroceso al recibir daño. Overpower funciona contra enemigos de mucho menos nivel.',
              'Battle Shout is raid-wide. Slam is no longer subject to spell pushback. Overpower works against much lower level enemies.'),
        ('●', 'Furia: Lingering Rage ya no corta la regeneración de vida tras el combate, e Improved Berserker Rage quita las ralentizaciones. Armas: Sword Specialization ya no salta con Shield Bash ni Shield Slam.',
              'Fury: Lingering Rage no longer stops health regeneration after combat, and Improved Berserker Rage removes movement impairing effects. Arms: Sword Specialization no longer procs from Shield Bash or Shield Slam.'),
    ],
}
FECHA = ('15 de octubre', 'October 15')
TITULO = ('Raciales rehechas, varitas quietas y talentos nuevos', 'Reworked racials, standing-still wands and new talents')
RESUMEN = ('Gran parche: cambian las raciales de casi todas las razas, varitas y Auto Shot obligan a estar quieto medio segundo, el Mago estrena Frost Blast y Arcane Wrath, '
           'el Chamán recupera Elemental Mastery y el Sacerdote Sombra gana Dark Inspiration. Muchas auras pasan a afectar a toda la banda.',
           'A big patch: almost every race\'s racials change, wands and Auto Shot require standing still for half a second, Mages get Frost Blast and Arcane Wrath, '
           'Shamans get Elemental Mastery back and Shadow Priests gain Dark Inspiration. Many auras become raid-wide.')


def parche():
    """Entrada en el formato de cambios_beta.PARCHES (solo castellano)."""
    return (FECHA[0], TITULO[0], RESUMEN[0], [(s, es) for s, es, _ in GENERAL], {k[0]: [(s, es) for s, es, _ in v] for k, v in CLASES.items()})


def ingles():
    """{texto castellano: texto inglés} de todo lo de este parche, para las claves de traducción."""
    d = {FECHA[0]: FECHA[1], FECHA[0].upper(): FECHA[1].upper(), TITULO[0]: TITULO[1], RESUMEN[0]: RESUMEN[1]}
    for s, es, en in GENERAL + [x for v in CLASES.values() for x in v]:
        d[es] = en
    for k in CLASES:
        d[k[0]] = k[1]
    return d
