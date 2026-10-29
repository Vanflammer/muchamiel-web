"""Repaso final de raciales antes del lanzamiento (Blizzard, foro «WoW Forever Beta Development Notes», 26-10-2026, 20:35 UTC).
cambios_beta.py lo pone el primero de PARCHES. Los textos nuevos de cada racial van en raciales_15oct.RACIALES_26."""
URL = 'https://us.forums.blizzard.com/en/wow/t/wow-forever-beta-development-notes-updated-october-26/2360696/7'
# (signo, castellano, inglés)
GENERAL = [
    ('●', 'Último repaso de las raciales antes del lanzamiento. Vuelven raciales pensadas para un rol o una clase en lugar de las genéricas. '
          'Las de especialización en armas (espadas del humano, hachas del orco…) no vuelven: no quieren que el botín de las bandas dependa del tipo de arma.',
          'Final racial pass before launch. Role- or class-focused racials come back instead of generic ones. Weapon specialization racials (human swords, orc axes…) '
          'do not return: Blizzard does not want raid loot to depend on weapon type.'),
]
CLASES = {
    ('Razas', 'Races'): [
        ('●', 'Humano: Ruthless baja a +1 % de crítico (era 2 %). Human Spirit sube a +10 % de espíritu (era 5 %).',
              'Human: Ruthless down to +1% critical chance (was 2%). Human Spirit up to +10% Spirit (was 5%).'),
        ('●', 'Enano: se quita Earth Fury (2 % de daño y sanación críticos). Entra Artisan\'s Precision: +1 % de golpe con hechizos y ataques.',
              'Dwarf: Earth Fury (2% critical damage and healing) removed. New: Artisan\'s Precision, +1% hit chance with spells and attacks.'),
        ('●', 'Tauren: Plainsrunning da un 2 % por acumulación, hasta un 60 % de velocidad (era 1 % y 30 %), pero ya no funciona montado. Endurance se queda solo en +5 % de vida.',
              'Tauren: Plainsrunning grants 2% per stack, up to 60% movement speed (was 1% and 30%), but no longer works while mounted. Endurance is now just +5% Health.'),
        ('●', 'Orco: se quita Savage (1 % de crítico). Vuelve Command: +5 % de daño a las mascotas de brujos y cazadores. Blood Fury baja a 2 min de reutilización (eran 3).',
              'Orc: Savage (1% critical chance) removed. Command returns: +5% damage for Warlock and Hunter pets. Blood Fury cooldown down to 2 min (was 3).'),
        ('▲', 'Trol: Berserking dura 15 s (eran 10).', 'Troll: Berserking lasts 15 sec (was 10).'),
        ('▲', 'No-muerto: Touch of the Grave, 15 s de reutilización interna (eran 25).', 'Undead: Touch of the Grave internal cooldown down to 15 sec (was 25).'),
        ('●', 'Célicos: Wind Blessed baja al 2 % de celeridad (era 3 %). Read Ley Line da +50 % de regeneración 15 s; usada en una línea ley, «Attuned» 1 hora al 100 %. '
              'Skysight da +15 % de velocidad 15 s; usada en una convergencia elemental, «Charged» 1 hora al 30 %. Las dos mejoras de 1 hora se mantienen al morir, pero se pierden al entrar en una banda.',
              'Skyborne: Wind Blessed down to 2% haste (was 3%). Read Ley Line grants +50% regeneration for 15 sec; used at a ley line, «Attuned» for 1 hour at 100%. '
              'Skysight grants +15% movement speed for 15 sec; used at an elemental convergence, «Charged» for 1 hour at 30%. Both 1-hour buffs persist through death but are removed upon entering a raid.'),
    ],
}
FECHA = ('26 de octubre', 'October 26')
TITULO = ('Repaso final de las raciales', 'Final racial pass')
RESUMEN = ('A una semana del lanzamiento, Blizzard retoca las raciales: el enano cambia Earth Fury por +1 % de golpe, el orco recupera Command para las mascotas, '
           'el tauren corre más a pie y los célicos pierden algo de celeridad pero ganan mejoras de una hora.',
           'A week before launch, Blizzard tweaks racials: Dwarves swap Earth Fury for +1% hit, Orcs get Command back for pets, '
           'Tauren run faster on foot and Skyborne lose some haste but gain 1-hour buffs.')


def parche():
    """Entrada en el formato de cambios_beta.PARCHES (solo castellano)."""
    return (FECHA[0], TITULO[0], RESUMEN[0], [(s, es) for s, es, _ in GENERAL], {k[0]: [(s, es) for s, es, _ in v] for k, v in CLASES.items()})
