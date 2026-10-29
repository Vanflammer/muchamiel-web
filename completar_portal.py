from pathlib import Path
import html, re, shutil, zipfile
from crear_portal import dist, root, classes, head, footer, common_header, script, build_home
from datos_clases import DATA, BUILDS, validate
from macros_clases import MACROS

E=html.escape
def p(s):return '<p>'+E(s)+'</p>'
def entry(id,title,body):return f'<details class="entry" id="{id}"><summary>{E(title)}</summary><div class="detail-body"><a class="permalink" href="#{id}">Enlace directo</a>{body}</div></details>'
def section(id,title,body,opened=False):return f'<details class="section" id="{id}"'+(' open' if opened else '')+f'><summary>{E(title)}</summary><div class="section-body">{body}</div></details>'
def macro_block(m):return p(m['note'])+'<div class="macro"><button type="button" class="copy">Copiar macro</button><pre><code>'+E(m['code'])+'</code></pre></div>'
def write_page(slug,title,color,body):
    folder=dist/slug;folder.mkdir(exist_ok=True)
    (folder/'index.html').write_text(head(title+' · WoW Forever | Muchamiel','Guía de PvP nivel 30 de WoW Forever, con talentos, macros y estrategias.')+f'<body style="--class-color:{color}">'+common_header('../')+'<main>'+body+footer()+'</main><div role="status" class="status"></div><script>'+script+'</script></body></html>',encoding='utf-8')

# Plans to try, not simulated win rates or a claim of exhaustive optimal builds.
PLANS={
'Warrior':('Mantén contacto con Hamstring y administra Charge e Intercept. Alterna actitudes con un propósito: cortar, romper miedo o defender. No gastes toda la rage antes de necesitar un interrupt.', 'Las macros de actitud evitan buscar otra barra en una persecución; el foco permite cortar sin cambiar el objetivo de daño. Lleva un escudo accesible y comprueba tus requisitos de Shield Bash.', 'En BG acompaña a quien pueda curarte, interrumpe al caster que amenaza a tu grupo y usa ralentizaciones para proteger aliados. En mundo abierto conserva una herramienta para volver al rival tras su escape.', 'Prioriza un arma apropiada, vida y fuerza/attack power. Compara crítico y acierto con tu equipo real; no sacrifiques toda la supervivencia por una lista de daño PvE.'),
'Paladin':('Con Reprensión, busca ventanas de contacto tras ralentizaciones y controles del rival. Separa Hammer of Justice y Repentance: uno prepara daño, el otro puede darte una cura si no se rompe.', 'Las curas y bendiciones sobre mouseover conservan tu objetivo ofensivo. Alt dirige la ayuda a ti; tener Freedom y Protection en botones propios permite escoger el recurso que necesitas.', 'En BG, Sagrado ofrece una función clara de curas; Reprensión presiona y protege con bendiciones. En mundo abierto conserva maná para sobrevivir y no uses todos los defensivos para una única apertura.', 'Reprensión necesita arma y fuerza con vida suficiente. Sagrado necesita maná e intelecto y un conjunto orientado a curas. Protección compara escudo y supervivencia; no es una recomendación general de daño.'),
'Hunter':('Mantén distancia, administra Concussive Shot y retira tu mascota si la van a matar o controla al objetivo equivocado. Scatter o Intimidation, si los tienes, sirven para crear espacio; no improvises una trampa ignorando sus requisitos.', 'El foco separa control de daño; petpassive/petfollow recupera una mascota expuesta. Las macros de melee son recursos de escape y las trampas siguen siendo decisiones manuales.', 'En BG busca líneas de tiro seguras, protege a los healers con slows y vigila a la mascota. En mundo abierto revisa munición, comida de mascota y entorno antes de comprometer tu escape.', 'Compara arma a distancia, agilidad/attack power, vida y acierto. El equipo y la supervivencia de la mascota importan en Bestias. No equipares una lista de raid a la mejor elección para duelos.'),
'Rogue':('Planifica apertura, control y reinicio. Guarda energía antes de un stun para aprovecharlo; Gouge y Sap no toleran que añadas daño indiscriminadamente. No esperes Blind: queda fuera de este nivel.', 'Stopattack evita que tu siguiente golpe arruine un control. El foco permite Kick sin perder a tu víctima; separar Vanish, Sprint y Preparation evita consumir los tres sin una razón.', 'En BG interrumpe curas y disputa objetivos con apoyo; no conviertas cada apertura en una persecución interminable. En mundo abierto revisa venenos y escape; un reinicio requiere salir de peligro y atender los efectos periódicos.', 'Armas adecuadas a la build primero: dagas para Mutilate y los requisitos de sus ataques. Después compara agilidad, vida, attack power, crítico y acierto sin abandonar supervivencia.'),
'Priest':('Alterna presión con curas, escudo y dispels. Sombra tiene Silence y Mind Flay solo si compras esos talentos; Disciplina propone desgaste y Penance. Evita quedarte sin maná persiguiendo una victoria inmediata.', 'Mouseover acelera escudos, dispels y curas sin perder el enemigo. El foco deja Silence en un objetivo secundario; stopcasting solo se usa cuando aceptarías perder el lanzamiento actual.', 'En BG Disciplina/Sagrado necesitan posición, aliados y protección de interrupciones. Sombra añade daño y control. En mundo abierto no persigas sin maná ni conviertas cada dispel en una pérdida de tu oportunidad de curar.', 'Compara vida, intelecto/maná y poder de hechizos acorde a daño o curas. Espíritu puede ayudar al desgaste, según tu regeneración real. Sombra de nivel 30 no implica Shadowform.'),
'Shaman':('Elige entre presión melee, lanzamientos de Elemental o curas de Restauración. Earth Shock para cortar y Frost Shock para distancia compiten por recursos y tiempos: decide antes de pulsar. Sitúa los tótems con una función concreta.', 'Foco/mouseover permite cortar o purgar sin cambiar tu objetivo principal; las curas con Alt son rápidas sobre ti. Nature’s Swiftness queda separado para decidir qué cura necesita la emergencia.', 'En BG los tótems y Purge suman valor al grupo. Restauración gana utilidad con compañeros; Mejora necesita apoyo para cerrar distancia. En mundo abierto no abandones una zona útil de tótems sin valorar la persecución.', 'Mejora compara armas, fuerza/agilidad, vida y recursos; Elemental compara poder de hechizos e intelecto; Restauración prioriza curas y maná. No extrapoles Chain Lightning ni Lava Burst a nivel 30.'),
'Mage':('Escarcha es la primera propuesta de control: slows, Frost Nova, ventanas de daño y defensas. Guarda Blink para una situación concreta y no superpongas Polymorph con daño periódico que lo rompa.', 'Counterspell al foco evita cambiar el objetivo durante una cura rival. Stopattack ayuda a conservar Polymorph; separar Ice Block y su cancelación evita anular la defensa por una segunda pulsación accidental.', 'En BG controla al enemigo que amenaza a tu grupo y busca espacio para lanzar. En mundo abierto alterna control y recuperación de recursos. Fuego y Arcano carecen de las defensas talentadas de Escarcha de esta guía.', 'Compara vida, intelecto y poder de hechizos; añade acierto/crítico según especialización y equipo. Lleva recursos para agua y recuperación permitidos en cada entorno.'),
'Druid':('Feral alterna presión física, control y curas; Equilibrio propone daño periódico y distancia. Cambiar de forma cuesta recursos: úsalo para una amenaza concreta y mantén maná para sobrevivir.', 'Botones de forma con ! evitan desactivar esa misma forma al repetir la pulsación. Mouseover permite curar aliados manteniendo un enemigo seleccionado. Las macros no convierten habilidades de una forma en ataques utilizables en cualquier otra.', 'En BG Restauración y movilidad aportan apoyo; Feral presiona y Equilibrio controla. En mundo abierto decide cuándo perseguir y cuándo recuperarte. Travel Form mantiene sus restricciones de uso.', 'Feral compara agilidad/fuerza, vida y arma con sus efectos reales en formas. Equilibrio y Restauración necesitan maná y poder de hechizos adecuado. No uses una única lista para todos los papeles.')}

RIVALS={
'Warrior':'Su amenaza es mantenerte a melee. Observa Charge/Intercept, Hamstring y el cambio a escudo; un Berserker Rage disponible puede frustrar un miedo. No interpretes una separación breve como un reinicio seguro.',
'Paladin':'Separa sus ventanas de inmunidad, control y curas. Guarda una respuesta para la siguiente cura cuando ya haya gastado una defensa; no inviertas todos tus recursos ofensivos en una inmunidad activa.',
'Hunter':'Distancia y mascota forman dos amenazas. Vigila slows y trampas; una mascota controlada no elimina el daño del cazador. Evita perseguir en línea recta por una zona que haya preparado.',
'Rogue':'La apertura puede encadenar controles; administra tu ruptura y defensa para sobrevivir al tramo peligroso. Los efectos periódicos dificultan reinicios, pero pueden romper tu propio control si los aplicas sin pensar.',
'Priest':'Puede disipar y recuperar vida mientras desgasta tu maná. Decide qué cura cortar en lugar de responder a cada lanzamiento; una presión sin recursos puede favorecer su plan de desgaste.',
'Shaman':'Reconoce tótems y shocks antes de comprometerte. No lances una cura larga frente a un Earth Shock disponible sin preparar espacio o engañar su corte. Prioriza los tótems que realmente interfieran en tu plan.',
'Mage':'Cuenta Blink, raíces y, si su build los tiene, Ice Block/Cold Snap. No gires toda tu ofensiva alrededor de una raíz que puede crear otra separación. Polymorph puede concederle tiempo de recuperación.',
'Warlock':'Respeta Fear, efectos periódicos y la utilidad del demonio. Un Voidwalker, Succubus o Felhunter cambia el plan; no supongas Spell Lock de nivel 36 ni que todas las builds tengan Soul Link.',
'Druid':'Espera cambios de forma, curas y movilidad. Su forma revela opciones inmediatas, no toda su build. No persigas sin recursos mientras se recupera; cortar una cura en forma caster puede abrir una ventana.'}

RESPONSES={
'Warrior':{'Warrior':'Compara Armas para daño y Protección para reducir presión física. Conserva Disarm para su ventana de arma y no malgastes Overpower fuera de su condición.', 'Paladin':'Hamstring facilita volver tras Freedom cuando termine. Shield Bash debe estar listo para una cura decisiva; no tienes Mortal Strike en este reparto.', 'Hunter':'Escalona Charge e Intercept; no gastes ambas herramientas antes de ver su siguiente salida. Hamstring cuando alcances melee.', 'Rogue':'Sobrevive a la apertura, aplica Rend cuando puedas y vigila que no arruine Intimidating Shout. Disarm puede reducir su ventana de arma.', 'Priest':'Mantén contacto y guarda Shield Bash para una cura relevante. Berserker Rage debe responder al miedo, no consumirse por rutina.', 'Shaman':'Presiona las curas y elimina un tótem solo si su efecto justifica perder contacto. Disarm gana valor frente a Mejora.', 'Mage':'Usa la primera entrada para forzar una salida y reserva la segunda para alcanzarlo de nuevo. No existe Pummel de nivel 38 en esta guía.', 'Warlock':'Berserker Rage y foco sobre el demonio ayudan a ordenar el control. Decide si atacar una mascota expuesta compensa dar tiempo al brujo.', 'Druid':'Hamstring obliga a gestionar formas; reserva una entrada para después de su escape. Corta una cura cuando salga a caster.'},
'Paladin':{'Warrior':'Freedom crea margen frente a slows; Hammer of Justice puede darte una cura o una ofensiva. Compara Protección como variante defensiva.', 'Paladin':'Administra maná y escalona controles para forzar defensas. El duelo puede prolongarse; Reprensión es el primer ensayo ofensivo.', 'Hunter':'Freedom para acercarte en una ventana útil y control al alcanzar. No persigas la mascota dejando que el cazador dispare libre.', 'Rogue':'Protection puede comprar tiempo frente a físico; comprueba sus limitaciones de ataque. Controla y cura antes de volver a presionar.', 'Priest':'Repentance puede preparar una cura o acercamiento si no hay daño que la rompa. Ten presente que puede disipar beneficios.', 'Shaman':'Purge puede quitar tus beneficios. Evita basar la supervivencia en que una bendición vaya a durar; provoca el shock antes de una cura larga.', 'Mage':'Elige cuándo usar Freedom para aprovecharla. No malgastes Hammer of Justice o Repentance sobre una defensa que los impida.', 'Warlock':'Reserva recursos para recuperarte bajo DoTs. Repentance no es un control gratis si Seal o daño pendiente la rompe.', 'Druid':'Busca una ventana de control cuando esté expuesto a tu presión. No vacíes maná por perseguir sus formas; cura en la pausa.'},
'Hunter':{'Warrior':'Concussive Shot y distancia son el primer plan. Reserva control talentado para su segunda entrada; mascota y terreno deben ayudar al escape.', 'Paladin':'Espera Freedom antes de gastar todas tus ralentizaciones. No sigas disparando a una inmunidad mientras necesitas recolocarte.', 'Hunter':'Vigila tanto el cazador como su mascota. Retira la tuya si pierde vida fuera de tu alcance y aprovecha cobertura en mundo abierto.', 'Rogue':'No regales una apertura descuidado. Al recuperar control, crea distancia antes de comprometer un lanzamiento largo; revisa qué trampa puedes usar.', 'Priest':'Mantén presión con la mascota y prepara control para una cura. Scatter puede romperse si la mascota sigue golpeando.', 'Shaman':'Elimina el tótem que afecte a tu control y vuelve al jugador. No consumas toda la distancia antes de decidir cómo cortar una cura.', 'Mage':'Retirar y reenviar mascota ayuda frente a freezes o control. No des por supuesto Bestial Wrath: no está en esta build.', 'Warlock':'Mascota expuesta a Fear necesita seguimiento. Controla al demonio o al brujo según la ventana; procura no romper Scatter con disparos o mascota.', 'Druid':'Presiona cuando cure y vigila sus cambios de forma. Mantén recursos para un segundo acercamiento y no persigas fuera de tu alcance cómodo.'},
'Rogue':{'Warrior':'Armadura y respuestas físicas reducen la eficacia de un intercambio frontal. Sutileza permite comparar control y reinicio; reserva defensas para su presión.', 'Paladin':'Fuerza una defensa antes de gastar tu mejor ofensiva. Mantén Kick para curas; Gouge debe crear tiempo real sin daño que lo rompa.', 'Hunter':'Abre con un plan para no perder contacto. Sprint y control se reservan para el escape; vigila mascota y efectos que impidan Vanish.', 'Rogue':'Es un duelo de apertura y recursos. No gastes Evasion y Vanish por reflejo en el mismo tramo; conserva energía para aprovechar tu control.', 'Priest':'Presión con Kick listo para una cura; observa Psychic Scream y el escudo. Preparar control sobre daño pendiente evita romper tu propio Gouge.', 'Shaman':'Presiona curas y selecciona tótems por efecto. Kick requiere melee: no lo gastes mientras ya ha escapado de tu alcance.', 'Mage':'No consumas Sprint antes de ver Blink o la siguiente raíz. Preparation solo reinicia las habilidades indicadas por su tooltip.', 'Warlock':'Los DoTs dificultan reiniciar y un demonio puede arruinar el control. Kick al lanzamiento relevante; no esperes una limpieza automática con Vanish.', 'Druid':'Impide la cura en su ventana caster y reserva movilidad para el cambio de distancia. No persigas solo mientras sangrados consumen tu vida.'},
'Priest':{'Warrior':'Escudo, curas y miedo deben darte tiempo; no superpongas Psychic Scream con una respuesta a Fear ya disponible. Disciplina es una comparación defensiva.', 'Paladin':'Sombra compara presión y Silence; Disciplina compara desgaste. Mantén maná para curar en vez de gastar todo en dispels.', 'Hunter':'La mascota mantiene presión incluso fuera de tu objetivo. Controla una amenaza para poder curar y no canalices expuesto a ambas.', 'Rogue':'Disciplina es el primer ensayo contra apertura física. Escudo y control deben recuperar la iniciativa; no desperdicies el miedo sin espacio para curar.', 'Priest':'Sombra ofrece Silence para la ventana de cura; Disciplina permite un plan de recursos. Mana Burn necesita tiempo real para lanzar.', 'Shaman':'Provoca o espera Earth Shock antes de una cura crucial. Tótems y Purge reducen el valor de confiar en un único buff defensivo.', 'Mage':'No concedas Counterspell en tu cura decisiva. Usa instantes y control para abrir una ventana; Sombra puede responder con Silence.', 'Warlock':'Vigila demonio y Fear; curar sin espacio bajo presión de DoTs gasta recursos rápidamente. Silence o dispels deben tener un objetivo concreto.', 'Druid':'Presiona o desgasta durante la ventana caster. No gastes todo el maná persiguiendo una forma rápida; prepara control y la siguiente cura.'},
'Shaman':{'Warrior':'Elemental compara distancia; Mejora compara un intercambio físico que exige defensa. Usa Frost Shock para espacio y no malgastes el corte compartiendo recursos.', 'Paladin':'Purge puede quitar beneficios disipables, pero no ignora todas las inmunidades. Reserva Earth Shock para la cura que cambie el intercambio.', 'Hunter':'Busca distancia de lanzamiento o una entrada melee según build. No abandones tus tótems útiles para perseguir una mascota sin resultado.', 'Rogue':'Necesitas sobrevivir antes de lanzar. Mejora es una primera comparación de presión; utiliza control y curas cuando recuperes espacio.', 'Priest':'Purge y Earth Shock ayudan a abrir presión, pero consumir todo en disipar puede vaciarte. Ajusta entre daño y recursos según sus curas.', 'Shaman':'Vigila escuela de Naturaleza y el shock rival. No gastes tu corte en un lanzamiento irrelevante antes de una cura decisiva.', 'Mage':'Elemental compara presión a distancia; no lances toda tu escuela frente a un Counterspell libre. Usa shocks deliberados y tótems con función.', 'Warlock':'Identifica el demonio antes de gastar el control. Earth Shock para Fear o una ventana crítica; no te vacíes purgando beneficios menores.', 'Druid':'Corta la cura cuando esté caster y no consumas todo persiguiendo. Frost Shock crea presión de distancia, pero puede competir con tu siguiente interrupt.'},
'Mage':{'Warrior':'Escarcha: slows, Nova y separación escalonada. Reserva Blink para la siguiente entrada; un freeze no significa que ya hayas ganado distancia.', 'Paladin':'Espera a Freedom antes de comprometer todos los controles. Polymorph puede preparar recuperación si no hay daño que lo rompa.', 'Hunter':'Controla mascota o cazador para lanzar y no te expongas a ambos. Escarcha conserva defensas que Fuego/Arcano no tienen en estos repartos.', 'Rogue':'Escarcha es el primer ensayo defensivo. No consumas Blink e Ice Block en el mismo instante por reflejo; crea una ventana para recuperar control.', 'Priest':'Counterspell debe forzar una oportunidad real de daño. Evita una guerra de recursos si ya no puedes aprovechar tus controles.', 'Shaman':'Reconoce el tótem que interfiere con tu hechizo. Provoca Earth Shock antes de un lanzamiento importante y guarda Counterspell para curas.', 'Mage':'Escarcha permite comparar controles y defensas. No conviertas cada Counterspell en un intento de cortar un instante que ya ocurrió.', 'Warlock':'Retira efectos que impidan tu recuperación si tienes la herramienta válida. Controla demonio o brujo sin romper Polymorph con daño pendiente.', 'Druid':'Presiona en forma caster y administra raíces ante cambios de forma. Reserva una respuesta para la siguiente cura en vez de perseguir sin maná.'},
'Druid':{'Warrior':'Feral compara movilidad y presión física. Cambia de forma con un objetivo y busca espacio para curar; no vacíes el maná con cambios sin efecto.', 'Paladin':'Administra recursos alrededor de sus defensas. Feral puede mantener presión, Equilibrio compara distancia; no añadas daño a un control que quieres conservar.', 'Hunter':'Aprovecha una entrada cuando tenga menos escape; Feral es el primer ensayo. Crea una pausa para curar sin tener mascota y cazador golpeando a la vez.', 'Rogue':'Feral compara defensa física y recuperación tras la apertura. No te quedes caster sin espacio; prepara control para curar.', 'Priest':'Feral presiona su ventana de cura; evita un desgaste que favorezca al que administra mejor maná. No des por permanente un HoT que puede disipar.', 'Shaman':'Earth Shock amenaza curas largas. Usa cambios de distancia para abrir la cura y no bases el plan en buffs que Purge pueda quitar.', 'Mage':'Los cambios de forma pueden ayudarte a gestionar movimiento, con coste de maná. No gastes todas tus entradas antes del siguiente Blink.', 'Warlock':'DoTs y Fear siguen amenazando mientras te desplazas. Cura con espacio y vigila su demonio; la movilidad no elimina efectos periódicos.', 'Druid':'Reconoce cuándo el rival pasa a curar. Feral es el primer ensayo de presión; Equilibrio y Restauración permiten comparar desgaste sin prometer una victoria.'}}

SPEC={'Warrior':'arms','Paladin':'retribution','Hunter':'beast-mastery','Rogue':'subtlety','Priest':'shadow','Shaman':'enhancement','Mage':'frost','Druid':'feral'}
def guide(slug,name,cls,color):
    plan,benefit,bg,gear=PLANS[cls]
    body='<p class="eyebrow">WOW FOREVER · BETA · NIVEL 30</p><h1>'+E(name)+'</h1>'+p('26 puntos: 21 por nivel y 5 extras de Legacy. Cliente en inglés, explicaciones en español. Propuestas para probar en duelos, BGs y mundo abierto; no son un ranking de victorias ni todas las distribuciones matemáticamente posibles.')
    body+='<div class="quick">'+''.join(f'<a href="#{id}">{label}</a>' for id,label in [('inicio','Por qué macros'),('builds','Talentos'),('macros','Macros'),('duelos','Duelos'),('pvp','BGs y mundo'),('equipo','Equipo'),('fuentes','Fuentes')])+'<a href="../comunes/">Comunes y raciales</a></div>'
    body+=section('inicio','Qué mejoran las macros',p(benefit)+p('Sin estas macros tendrías que seleccionar un segundo objetivo, lanzar y volver al anterior. Con foco o mouseover reduces esos pasos y mantienes atención en posición, controles y recursos. No automatizan decisiones, no evitan el GCD ni saltan requisitos de equipo, rango o talentos.')+p(plan),True)
    builds=''
    for i,b in enumerate(BUILDS[cls],1):
        content=p(b['use'])
        for tree,a in zip(DATA['talents'][cls]['trees'],b['allocation']):
            lookup={t['name']:t for t in tree['talents']}
            if a:content+='<p><strong>'+E(tree['name'])+':</strong> '+E('; '.join(f"{n} {rank}/{lookup[n]['max']}" for n,rank in a.items()))+'.</p>'
        content+=p(b['limits'])+'<a href="https://talentsforever.com/" target="_blank" rel="noopener noreferrer">Contrastar en el calculador Forever</a>'
        builds+=entry('B'+str(i),b['name'],content)
    body+=section('builds','Tres builds de 26 puntos',p('Repartos comprobados contra filas, rangos y prerrequisitos del conjunto de datos de beta del 8/10/2026. Las opciones de apoyo y defensa tienen un papel específico; no son equivalentes en daño de duelo.')+builds)
    macros=p('Crea una macro por bloque en /macro y elige el icono ?. Normal usa mouseover cuando el bloque lo indica; Shift usa foco y Alt te selecciona a ti en las curas. Si una tecla ya tiene otra acción asignada, revisa tus atajos. Usa solo los hechizos aprendidos y talentos de tu reparto.')
    for i,m in enumerate(MACROS[cls],1):macros+=entry('M'+str(i),m['title'],macro_block(m))
    body+=section('macros',str(len(MACROS[cls]))+' macros para copiar',macros)
    duel=p('Primera build de ensayo por enfrentamiento. Identifica especialización, raza y equipo del rival: la clase por sí sola no basta. Practica varias rondas antes de cambiar puntos; las decisiones siguientes son propuestas tácticas, no resultados medidos.')
    for other,othername,english,_,_ in classes:
        idx=1 if cls=='Priest' and english in ('Rogue','Warrior','Hunter') else 0
        if cls=='Shaman' and english in ('Rogue','Hunter'):idx=1
        title='Contra '+othername
        text='<p><strong>Primer ensayo:</strong> <a href="#B'+str(idx+1)+'">'+E(BUILDS[cls][idx]['name'])+'</a>.</p>'+p(RIVALS[english])+p(RESPONSES[cls][english])
        duel+=entry('D-'+other,title,text)
    body+=section('duelos','Duelos contra las nueve clases',duel)
    body+=section('pvp','BGs y mundo abierto',p(bg)+p('En BG juega objetivos y coordina controles con el grupo. Antes de gastar una ruptura, distingue el control que debes romper del que puedes soportar. En mundo abierto revisa terreno, aliados y vías de retirada. Las reglas del torneo no se trasladan automáticamente a estos entornos.')+'<a href="../warlock/#reglas">Reglas y restricciones del torneo</a>')
    body+=section('equipo','Equipo y referencia BiS',p(gear)+p('No se ofrece una lista de objetos como BiS universal de duelos: cambia con build, rivales y restricciones. La guía enlazada sirve para comparar mecánicas y equipo de nivel 30; su orientación de daño no determina por sí sola el mejor PvP.')+f'<a href="https://www.wowhead.com/forever/guide/classes/{slug}/{SPEC[cls]}/level-30-dps-overview" target="_blank" rel="noopener noreferrer">Wowhead Forever · {E(name)} nivel 30</a>')
    race_links=[]
    for faction,races in DATA['racials'].items():
        for race in races:
            if cls in race['classes']:race_links.append('<a href="../comunes/#race-'+re.sub('[^a-z0-9]+','-',race['race'].lower()).strip('-')+'">'+E(race['race'])+'</a>')
    body+=section('raciales','Raciales disponibles para esta clase','<div class="quick">'+''.join(race_links)+'</div>'+p('La raza del brujo de Muchamiel es Undead. Cada clase debe usar las raciales de su propia raza; no son botones disponibles para todo el mundo.'))
    body+=section('fuentes','Fuentes y comprobación en la beta',p('Datos del calculador generados el 8/10/2026. Los hotfixes posteriores pueden cambiar requisitos o efectos. Se han comprobado los 26 puntos y las macros de hasta 255 caracteres; no se han ejecutado estas macros dentro del cliente.')+'<ul><li><a href="https://talentsforever.com/" target="_blank" rel="noopener noreferrer">Talents Forever · talentos, spellbooks y raciales</a>. Repartos y presentación adaptados; datos bajo <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener noreferrer">CC BY 4.0</a>.</li><li><a href="https://news.blizzard.com/en-us/article/24304075/create-the-hero-you-want-to-be-in-world-of-warcraft-forever" target="_blank" rel="noopener noreferrer">Blizzard · clases y personalización en Forever</a>.</li><li><a href="https://raider.io/events/the-forever-open/rules-regulations-code-of-conduct" target="_blank" rel="noopener noreferrer">The Forever Open · reglas oficiales</a>.</li></ul>'+p('Antes de competir: prueba alcance, objetivo normal, foco, mouseover, modificadores, rangos aprendidos y talento requerido. Comprueba el tooltip actual de cada habilidad y verifica las restricciones con la organización.'))
    write_page(slug,name,color,body)

def common():
    base=[
    dict(title='Fijar foco / Alt borrar',note='Ratón sobre una unidad o unidad seleccionada. Alt borra el foco. Conserva el foco para las macros de Shift.',code='/clearfocus [mod:alt]\n/focus [nomod,@mouseover,exists,nodead][nomod,exists,nodead]'),
    dict(title='Volver al último enemigo',note='Recupera el último objetivo enemigo. No selecciona automáticamente al más peligroso.',code='/targetlastenemy'),
    dict(title='Detener lanzamiento y ataques',note='Botón de parada manual para dejar de golpear un control o cancelar un lanzamiento. No afecta a efectos periódicos ya aplicados.',code='/stopcasting\n/stopattack'),
    dict(title='Trinket superior / Shift inferior',note='13 y 14 son las dos ranuras de trinket. Solo activa un objeto con uso disponible; no decide cuándo romper control y no sustituye sus requisitos.',code='#showtooltip\n/use [mod:shift] 14; 13'),
    dict(title='Venda sobre aliado / Alt sobre ti',note='Necesitas Heavy Silk Bandage aprendida y en las bolsas. Alt te dirige la venda; normal usa aliado bajo el ratón, seleccionado o tú. Daño o acciones pueden interrumpirla; respeta Recently Bandaged y las reglas del entorno.',code='#showtooltip Heavy Silk Bandage\n/stopcasting\n/use [mod:alt,@player][@mouseover,help,nodead][help,nodead][@player] Heavy Silk Bandage')]
    body='<p class="eyebrow">WOW FOREVER · PARA TODAS LAS CLASES</p><h1>Macros comunes y raciales</h1>'+p('Foco, parada manual y objetos reducen cambios de objetivo y clics. Cada racial pertenece a una raza; las ventajas pasivas no necesitan macro. Comprueba las reglas de consumibles y objetos del torneo antes de usarlos.')
    body+=section('comunes','Cinco macros comunes',''.join(entry('G'+str(i),m['title'],macro_block(m)) for i,m in enumerate(base,1)),True)
    active={'Blood Fury','Shatter Curse','Will of the Forsaken','Cannibalize','War Stomp','Berserking','Rapid Regeneration','Walk on Air','Skysight','Perception','Will to Survive','Stoneform','Shadowmeld','Escape Artist','Arcane Surge','Gift of the Naaru'}
    for faction,races in DATA['racials'].items():
        entries=''
        for race in races:
            rid='race-'+re.sub('[^a-z0-9]+','-',race['race'].lower()).strip('-')
            text=p('Clases: '+', '.join(race['classes'])+'.')
            for ability,desc,icon in race['abilities']:
                text+='<h3>'+E(ability)+'</h3>'+p(desc)
                if ability in active or any(marker in desc for marker in ('Instant', 'Channeled', 'sec cast')):
                    code='#showtooltip '+ability+'\n/cast '+ability
                    text+=macro_block(dict(note='Botón independiente: decide cuándo usarlo y no lo encadenes con todos tus defensivos.',code=code))
            if race['race']=='Undead':text+=p('Will of the Forsaken rompe los controles indicados en el tooltip; no concede una inmunidad adicional que este no describa. Cannibalize requiere cadáver válido y se interrumpe: resulta más práctico para recuperarte en mundo abierto o BG que como plan de duelo.')
            entries+=entry(rid,race['race'],text)
        body+=section(faction.lower(),faction+' · raciales de Forever',entries)
    body+=p('Fuente de tooltips: Talents Forever, datos de beta del 8/10/2026. Texto original en inglés para contrastar con el cliente. Uso bajo CC BY 4.0; selección de macros y presentación adaptadas.')+'<a href="https://talentsforever.com/" target="_blank" rel="noopener noreferrer">Consultar talentos y raciales Forever</a> · <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener noreferrer">Licencia CC BY 4.0</a>'
    write_page('comunes','Macros comunes y raciales','#afe67d',body)

def package():
    instructions='''WOW FOREVER — COMUNIDAD DE MUCHAMIEL

Entrada general con selector de las nueve clases, redes oficiales y metas de la comunidad.
Guías PvP nivel 30: builds de 26 puntos, macros en inglés, duelos, BGs y mundo abierto.
Incluye diez páginas de razas (Alianza/Horda) y calculadora de las nueve clases.
La calculadora admite nivel máximo de 10 a 60 y entre 0 y 5 puntos de Legacy,
muestra el nivel necesario del reparto y permite compartirlo por enlace.

INSTALACIÓN EN EL SERVIDOR DE CASA (PEDRO)
1. Descomprimir el ZIP y subir la carpeta wow-forever al directorio público.
2. Servir index.html como documento de índice de cada carpeta.
3. Entrada por IP: http://IP-PUBLICA/wow-forever/ (o HTTPS si está configurado).
4. Conservar clases, comunes, razas, calculadora, assets y todos los archivos JS.
No necesita base de datos, compilación ni dependencias.

NOMBRE Y DOMINIO
La portada y título del navegador son WoW Forever, no Brujo.
La ruta y carpeta son wow-forever. El dominio público no se ha cambiado:
Pedro deberá configurar el nombre definitivo, DNS y servidor si se decide usar uno.
No se presupone que wowforever.com u otro nombre esté disponible ni sea propiedad del usuario.
Para compartir sin mostrar burdelito.com: evitar redirecciones a ese dominio,
enlaces absolutos internos, recursos suyos o canonical con ese nombre.
Probar la dirección IP desde una red externa y conservar otros sitios existentes.
Un enlace por IP no garantiza que nadie pueda relacionar la IP con otros dominios.

REVISIÓN
Abrir portada, elegir clase, abrir talento y copiar macro. Revisar móvil.
1837/2000 es una cifra manual facilitada por el usuario el 9/10/2026.
La meta de YouTube es 100000; no se inventa un contador actual.
Condiciones y vigencia del sorteo se consultan en el canal.
Macros y estrategias requieren práctica en el cliente de beta.

Enlaces: /wow-forever/warlock/#B1, /wow-forever/mage/#macros, etc.
Antes de compartir: verificar el enlace definitivo desde fuera de casa.
'''
    (root/'web'/'PARA-PEDRO.txt').write_text(instructions,encoding='utf-8')
    delivery=root/'entrega-web'/'wow-forever'
    shutil.copytree(dist,delivery,dirs_exist_ok=True)
    with zipfile.ZipFile(root/'Muchamiel-WoW-Forever-Web.zip','w',zipfile.ZIP_DEFLATED) as z:
        for f in sorted(delivery.rglob('*')):
            if f.is_file():z.write(f,Path('wow-forever')/f.relative_to(delivery))
        z.write(root/'web'/'PARA-PEDRO.txt','PARA-PEDRO.txt')

if __name__=='__main__':
    assert not validate(),validate()
    for cls,macros in MACROS.items():
        for m in macros:assert len(m['code'])<=255,(cls,m['title'])
    build_home()
    for slug,name,cls,color,_ in classes:
        if cls!='Warlock':guide(slug,name,cls,color)
    common()
    w=dist/'warlock'/'index.html';s=w.read_text(encoding='utf-8')
    s=re.sub(r'<title>.*?</title>','<title>Brujo · WoW Forever | Muchamiel</title>',s)
    s=s.replace('<strong>BRUJO / FOREVER</strong>','<strong>WOW FOREVER / BRUJO</strong>')
    if '../comunes/' not in s:s=s.replace('</header>','<a href="../comunes/">Comunes y raciales</a></header>',1)
    w.write_text(s,encoding='utf-8')
    package()
    print('Portada WoW Forever, nueve clases, comunes y paquete para Pedro preparados.')
