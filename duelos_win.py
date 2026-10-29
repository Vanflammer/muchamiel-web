"""Bilingual matchup objectives and downloadable alpha, after translation."""
from html import escape
from pathlib import Path
import re
import shutil
import zipfile

CLASSES = ('warrior', 'paladin', 'hunter', 'rogue', 'priest', 'shaman', 'mage', 'warlock', 'druid')
# Every row is the player's class; columns follow CLASSES (including mirrors).
# Tactical proposals, not measured results. No ability above level 30 is required.
GOALS = {
 'warrior': [
  ('Ganar los intercambios de arma sin vaciar la ira persiguiendo. Remata cuando su defensivo termine y tú conserves vida e ira.', 'Win weapon trades without draining Rage on chasing. Finish after their defensive ends while you still have health and Rage.'),
  ('Mantener contacto y cortar una cura que importe después de sus protecciones. Tu daño debe superar lo que pueda curarse con el maná restante.', 'Stay in contact and interrupt a meaningful heal after their protections. Your damage must exceed what their remaining Mana can heal.'),
  ('Llegar al cazador y mantenerte en cuerpo a cuerpo sin caer en una trampa. La mascota no debe hacerte perder toda la presión sobre su dueño.', 'Reach the Hunter and stay in melee without walking into a trap. Do not let the pet pull all your pressure away from its owner.'),
  ('Sobrevivir al opener conservando suficiente vida para el intercambio sostenido. Negarle una reapertura limpia vale más que perseguir durante Evasion.', 'Survive the opener with enough health for sustained trades. Denying a clean reopener matters more than chasing through Evasion.'),
  ('Forzar curas caras con contacto sostenido y cortar la cura que evita el remate. Contra Shadow, no perder la carrera de vida por perseguir sin golpear.', 'Force costly heals through sustained contact and interrupt the heal that prevents a kill. Against Shadow, do not lose the health race by chasing without connecting.'),
  ('Llegar sin agotar tus herramientas de contacto y cerrar durante una cura cortada. Si destruyes un tótem, que abra una ventana real de presión.', 'Connect without exhausting your mobility tools and finish during an interrupted heal. Destroy a totem only when it opens a real pressure window.'),
  ('Conseguir una segunda conexión después de Blink, con ira para hacer daño. Gasta el burst cuando ya no pueda anularlo con control o Ice Block.', 'Secure a second connection after Blink with Rage left to deal damage. Commit burst when control or Ice Block can no longer negate it.'),
  ('Convertir la inmunidad a Fear en tiempo efectivo pegando al brujo. Si lleva Soul Link, desgasta su circuito de supervivencia sin regalar casteos al cambiar a la pet.', 'Turn Fear immunity into actual uptime on the Warlock. Against Soul Link, wear down their survival loop without giving free casts by switching to the pet.'),
  ('Castigar la salida de oso para curarse; no gastar toda la ira contra su fase más resistente. La victoria llega cuando no puede resetear y volver con vida.', 'Punish leaving Bear Form to heal; do not spend all your Rage into their toughest phase. Win when they cannot reset and return with health.'),
 ],
 'paladin': [
  ('Sobrevivir al daño sostenido sin curarte por encima de lo necesario. Gana si llegas al siguiente stun con vida y maná mientras él ya no puede sostener el intercambio.', 'Survive sustained damage without overhealing. Win by reaching your next stun with health and Mana while they can no longer sustain the trade.'),
  ('Sacar ventaja de maná sin desperdiciar daño en protecciones. Busca una cura interrumpida por Hammer of Justice cuando el rival ya no pueda estabilizarse.', 'Build a Mana advantage without wasting damage into protections. Use Hammer of Justice to stop a heal when the opponent can no longer stabilize.'),
  ('Acortar la distancia sin perder el maná persiguiendo. Combina contacto y stun para una ventana de daño; cura cuando puedas hacerlo sin regalar una nueva separación.', 'Close distance without draining Mana on chasing. Combine contact and a stun for a damage window; heal without giving away another disengagement.'),
  ('Sobrevivir al opener y negar que cada Vanish reinicie gratis el duelo. Gana el desgaste guardando una respuesta para su siguiente cadena de stuns.', 'Survive the opener and deny free resets from every Vanish. Win attrition by saving an answer for their next stun chain.'),
  ('Crear daño que obligue a curar antes de que sus dispels y Mana Burn te dejen sin recursos. El remate exige presión previa y una cura negada, no solo un stun.', 'Force healing before dispels and Mana Burn drain your resources. A kill needs prior pressure and a denied heal, not just a stun.'),
  ('Evitar que shocks y Purge conviertan cada cura en una pérdida de maná. Fuerza su cura con presión y usa el stun para cerrar cuando no pueda recuperarse.', 'Avoid letting shocks and Purge turn every heal into wasted Mana. Force healing through pressure and stun to finish when they cannot recover.'),
  ('Conectar tras Blink y conservar maná para el siguiente intercambio. Gasta el daño fuerte después de su inmunidad, con una ventana de stun que puedas aprovechar.', 'Connect after Blink and keep Mana for the next trade. Commit heavy damage after immunity with a stun window you can actually use.'),
  ('Acercarte con recursos suficientes para cortar su ciclo de DoTs y curación mediante presión y stun. Si pierdes el desgaste, necesitas una ventana de daño antes de vaciarte.', 'Close with enough resources to disrupt their DoT and healing loop through pressure and stuns. If losing attrition, secure a damage window before running dry.'),
  ('Forzarle a gastar maná en formas y curas mientras tú mantienes reservas. Castiga la cura en forma humanoide en vez de vaciarte pegando al oso.', 'Make them spend Mana on forms and healing while keeping your own reserves. Punish healing in caster form instead of draining yourself into Bear Form.'),
 ],
 'hunter': [
  ('Mantener daño a distancia mientras tus slows y la pet limitan su contacto. Tras Intercept, recuperar distancia sin perder toda la presión es la condición decisiva.', 'Keep dealing ranged damage while slows and your pet limit melee uptime. Recovering distance after Intercept without losing all pressure is decisive.'),
  ('Hacer que gaste maná en curarse y perseguirte, sin regalar contacto sostenido. Usa la trampa para recuperar distancia; remata después de las protecciones.', 'Make them spend Mana on healing and chasing without giving sustained melee uptime. Trap to regain distance; finish after protections.'),
  ('Ganar el intercambio de disparos y pet conservando una salida de la trampa rival. No pierdas tu ventana de daño por reaccionar tarde a Feign Death.', 'Win shot and pet trades while keeping an answer to the enemy trap. Do not lose your damage window by reacting late to Feign Death.'),
  ('Sobrevivir a la apertura y volver a disparar antes de su siguiente control. Evita una reapertura limpia y usa la trampa para recuperar alcance, no para romperla al instante.', 'Survive the opener and resume shooting before their next control. Deny a clean reopener and use a trap to regain range, rather than breaking it immediately.'),
  ('Mantener daño de dueño y pet que le obligue a curar y gastar maná, protegiendo tu distancia. A nivel 30 aún no tienes Viper Sting: el desgaste viene de la presión de daño.', 'Maintain player and pet damage that forces healing and Mana spending while protecting your range. At level 30 you do not have Viper Sting yet: attrition comes from damage pressure.'),
  ('Presionar fuera de su contacto físico y evitar curas gratuitas. Elimina un tótem cuando permita mantener distancia o control; no abandones al chamán para perseguir todos.', 'Pressure outside melee range and deny free healing. Remove a totem when it enables range or control; do not abandon the Shaman to chase every totem.'),
  ('Mantener la pet activa y daño durante sus intentos de control. Aprovecha después de Blink o Ice Block, sin enviar dueño y pet juntos a una misma respuesta.', 'Keep your pet active and deal damage through control attempts. Capitalize after Blink or Ice Block without exposing both you and the pet to one answer.'),
  ('Obligarle a defenderse con presión de disparos y pet antes de que los DoTs te consuman. Conserva una salida de Fear para seguir atacando en la ventana decisiva.', 'Force defensive play through shots and pet pressure before DoTs wear you down. Save a Fear break to keep attacking during the decisive window.'),
  ('Negar un reset completo con presión y pet, y castigar cuando salga de oso a curarse. Guarda recursos para reconectar después de un cambio de forma.', 'Deny a full reset through pressure and your pet, then punish leaving Bear Form to heal. Keep resources to reconnect after a shapeshift.'),
 ],
 'rogue': [
  ('Sacar ventaja con el opener y resetear antes de un intercambio sostenido desfavorable. Reabre con recursos cuando sus respuestas defensivas ya no cubran tu cadena.', 'Gain an advantage in the opener and reset before an unfavorable sustained trade. Reopen with resources when defensives no longer cover your chain.'),
  ('Forzar protecciones sin gastar todo el daño y volver a controlar cuando terminen. Kick a una cura decisiva debe convertir la segunda apertura en un remate.', 'Force protections without spending all your damage and regain control after they end. Kick on a decisive heal should turn the second opener into a kill.'),
  ('Mantener contacto evitando que la trampa y la pet arruinen el reset. Gana durante una cadena de control en la que no consiga recuperar su alcance de disparo.', 'Maintain contact without letting the trap and pet ruin your reset. Win during a control chain that prevents them from regaining shooting range.'),
  ('Negar la apertura gratuita y conservar una respuesta para su Kidney Shot. Remata con ventaja de energía y combo después de su Evasion, sin regalar un reset.', 'Deny a free opener and save an answer to Kidney Shot. Finish with an Energy and combo-point advantage after Evasion without giving away a reset.'),
  ('Encadenar presión y Kick sobre una cura cuando ya haya gastado su escape del control. Contra Shadow, conserva vida para la segunda conexión; no regales daño al resetear.', 'Chain pressure and Kick on a heal after their CC escape is spent. Against Shadow, keep health for a second connection; do not give free damage during resets.'),
  ('Mantener contacto y negar la cura que estabiliza al chamán. Forzar primero su respuesta al stun permite que una segunda cadena, con Kick disponible, sea letal.', 'Stay in contact and deny the heal that stabilizes the Shaman. Force their stun response first so a second chain with Kick ready can be lethal.'),
  ('Provocar Blink sin gastar la cadena completa y reconectar. La ventana ganadora llega después de sus escapes e inmunidad, con energía y control suficientes.', 'Draw Blink without spending your full chain, then reconnect. The winning window comes after escapes and immunity with enough Energy and control left.'),
  ('Forzar su escape de control y sostener una segunda cadena sin que la pet o los DoTs impidan el reset. No confundas una primera apertura fuerte con un remate seguro.', 'Force their CC escape and sustain a second chain without the pet or DoTs denying your reset. A strong first opener is not a guaranteed kill.'),
  ('Castigar la forma humanoide y negar la cura; no gastar todo el burst contra oso. Conserva control para cuando vuelva a salir de su forma defensiva.', 'Punish caster form and deny healing; do not spend all burst into Bear Form. Save control for the next time they leave their defensive form.'),
 ],
 'priest': [
  ('Sobrevivir al contacto manteniendo un margen de vida para curar. Gana el desgaste con daño entre curas; Fear solo crea espacio cuando su inmunidad haya terminado.', 'Survive melee contact with enough health to heal. Win attrition by dealing damage between heals; Fear creates space only after their immunity ends.'),
  ('Eliminar buffs útiles y forzar curas hasta crear ventaja de maná. Remata tras sus protecciones con presión sostenida; no vacíes tus reservas en dispels sin beneficio.', 'Remove useful buffs and force healing to create a Mana advantage. Finish after protections with sustained pressure; do not drain yourself on low-value dispels.'),
  ('Sobrevivir al daño simultáneo de cazador y pet sin vaciarte curando. Crea una pausa real del daño y conviértela en presión, en vez de limitarte a rellenar vida.', 'Survive simultaneous Hunter and pet damage without exhausting healing Mana. Create a real damage pause and turn it into pressure, rather than only refilling health.'),
  ('Aguantar la primera cadena y estabilizarte entre stuns. Guarda una respuesta para la segunda apertura y daña cuando Kick no pueda cerrar tu escuela de curación.', 'Hold through the first chain and stabilize between stuns. Save an answer to the second opener and apply damage when Kick cannot lock your healing school.'),
  ('Obtener ventaja de maná con daño, dispels útiles y Mana Burn solo cuando puedas completarlo. Mantén suficiente vida para no perder mientras intentas ganar recursos.', 'Gain a Mana advantage with damage, useful dispels and Mana Burn only when you can complete it. Keep enough health to survive while gaining resources.'),
  ('Hacer que sus curas y Purge cuesten más que tu mantenimiento. Castea tras una interrupción gastada y usa presión para impedir que el duelo sea solo una guerra de curas.', 'Make their healing and Purge cost more than your upkeep. Cast after an interrupt is spent and pressure so the duel does not become only a healing war.'),
  ('Sobrevivir al burst sin quedarte sin maná y disipar solo lo que abra presión. Contra Counterspell, reserva una cura segura y castiga después de su inmunidad.', 'Survive burst without running out of Mana and dispel only to open pressure. Keep a safe heal against Counterspell and punish after immunity.'),
  ('Hacerle gastar recursos reparando DoTs disipados mientras mantienes daño y tu propia vida. Devour Magic no debe convertir cada buff tuyo en una inversión perdida.', 'Make them spend resources replacing dispelled DoTs while maintaining damage and your health. Do not let Devour Magic turn every buff into wasted resources.'),
  ('Presionar cuando salga a curar y eliminar HoTs que realmente cambien el intercambio. Si gana distancia, no gastes todo el maná persiguiendo un reset que no puedes negar.', 'Pressure when they leave form to heal and remove HoTs that materially affect the trade. Do not drain all Mana chasing a reset you cannot deny.'),
 ],
 'shaman': [
  ('Reducir su contacto y curar en ventanas seguras, conservando maná. Gana si cada reconexión le cuesta más vida de la que tú gastas recuperándote.', 'Limit melee uptime and heal in safe windows while saving Mana. Win if each reconnection costs them more health than you spend recovering.'),
  ('Quitar la ventaja de sus buffs con Purge selectivo y negar una cura con Earth Shock. Guarda daño para después de sus protecciones, en vez de pagar dos veces el mismo intercambio.', 'Remove their buff advantage with selective Purge and deny a heal with Earth Shock. Save damage until after protections instead of paying twice for the same trade.'),
  ('Mantener presión sin recibir disparos y pet gratis durante cada cura. Busca una pausa real para recuperarte y vuelve a presionar antes de que recupere el control de distancia.', 'Maintain pressure without taking free shots and pet damage during every heal. Create a real recovery window and pressure again before they regain range control.'),
  ('Sobrevivir al opener y curarte antes de la siguiente cadena, sin hacerlo dentro de Kick. Tus tótems y slows deben comprar tiempo útil, no solo llenar el suelo.', 'Survive the opener and heal before the next chain without casting into Kick. Totems and slows must buy useful time, not merely cover the ground.'),
  ('Forzarle a curar mientras Purge elimina un buff relevante. Earth Shock a la cura decisiva debe abrir daño, no dejarte sin respuesta mientras él recupera todo.', 'Force healing while Purge removes a relevant buff. Earth Shock on a decisive heal must open damage, not leave you without an answer while they fully recover.'),
  ('Ganar la eficiencia de maná y cortar la cura que decide el intercambio. Ajusta presión a Elemental, Enhancement o Restoration; perseguir tótems sin un objetivo regala iniciativa.', 'Win Mana efficiency and interrupt the heal that decides the trade. Adapt to Elemental, Enhancement or Restoration; chasing totems without a purpose gives away initiative.'),
  ('Convertir Grounding, Purge y Earth Shock en una ventana de daño que puedas aprovechar. Conserva maná para curar después; no gastes todo intentando quitar cada buff.', 'Turn Grounding, Purge and Earth Shock into a damage window you can use. Save Mana to heal afterwards; do not spend everything removing every buff.'),
  ('Mantener Tremor útil y negar casteos decisivos mientras presionas al brujo. Si él destruye tus tótems, aprovecha esos globals; no repongas todos a costa de dejar de dañar.', 'Keep Tremor useful and deny decisive casts while pressuring the Warlock. If they destroy totems, use those globals; do not replace everything at the cost of all damage.'),
  ('Purgar HoTs útiles y castigar la salida de forma con daño o Earth Shock a la cura. Conserva maná para la reconexión; no persigas sin poder impedir su recuperación.', 'Purge useful HoTs and punish leaving form with damage or Earth Shock on a heal. Save Mana to reconnect; do not chase if you cannot deny recovery.'),
 ],
 'mage': [
  ('Hacer daño mientras está ralentizado y recuperar distancia después de Intercept. La ventana ganadora exige guardar una salida para la reconexión, no usar todo en el primer contacto.', 'Deal damage while they are slowed and regain distance after Intercept. A winning window requires an answer to reconnection, not spending everything on first contact.'),
  ('Forzar protecciones con daño sostenible y detener una cura con Counterspell después. No conviertas Polymorph en una cura gratuita justo cuando ya estaba cerca del remate.', 'Force protections with sustainable damage and Counterspell a heal afterwards. Do not turn Polymorph into free healing when they were already close to a kill.'),
  ('Crear una ventana de casteo sin dueño y pet pegándote a la vez. Controla una amenaza y presiona la otra; retoma objetivo tras Feign Death para no perder el remate.', 'Create a casting window without both Hunter and pet hitting you. Control one threat and pressure the other; reacquire after Feign Death to preserve the finish.'),
  ('Sobrevivir al opener y usar Blink para recuperar iniciativa. Fuerza su reconexión y remata cuando ya no pueda cubrir tu daño con otro reset o cadena de stuns.', 'Survive the opener and use Blink to regain initiative. Force reconnection and finish when another reset or stun chain can no longer cover your damage.'),
  ('Forzar una cura importante y cerrarla con Counterspell, con daño listo detrás. Una guerra larga de dispels y curas solo te sirve si tu maná aguanta mejor.', 'Force a meaningful heal and Counterspell it with damage ready to follow. A long dispel and healing war helps only if your Mana lasts longer.'),
  ('Quitar Grounding antes del hechizo decisivo y aprovechar Earth Shock gastado para castear. Usa Counterspell para cerrar una cura, sin vaciarte en intercambios de Purge.', 'Remove Grounding before the decisive spell and cast after Earth Shock is spent. Counterspell a heal without draining yourself into Purge trades.'),
  ('Forzar su interrupción o inmunidad sin entregar las tuyas gratis. Remata con una ventana de casteo y recursos cuando ya no pueda responder con Ice Block.', 'Force their interrupt or immunity without giving yours away. Finish with a casting window and resources when Ice Block can no longer answer.'),
  ('Evitar que los DoTs y la pet cancelen tus resets y abrir una ventana de daño tras Fear. Si Devour Magic deshace el control, separa tus respuestas en vez de gastar todas juntas.', 'Keep DoTs and the pet from denying resets and open a damage window after Fear. If Devour Magic undoes control, stagger your answers rather than spending them together.'),
  ('Forzar cambios de forma y castigar la cura humanoide con Counterspell. Tu control debe comprar daño o recuperación propia; raíces que quita al transformarse no son un remate.', 'Force shapeshifts and Counterspell healing in caster form. Control must buy damage or your recovery; roots they remove by shifting are not a kill window.'),
 ],
 'warlock': [
  ('Sobrevivir a sus reconexiones mientras DoTs y demonio siguen dañando. Ganas cuando ya no pueda mantener contacto y tú conserves vida para seguir presionando.', 'Survive reconnections while DoTs and your demon keep dealing damage. Win when they can no longer maintain contact and you have health left to keep pressure.'),
  ('Mantener DoTs mágicos y desgaste sin vaciarte, y forzar Divine Protection antes del remate. Purify no limpia magia a nivel 30; aprovecha esa presión sin regalar contacto.', 'Maintain magic DoTs and attrition without running dry, and force Divine Protection before the finish. Purify does not remove magic at level 30; use that pressure without giving melee uptime.'),
  ('Mantener daño mientras limitas los disparos libres y controlas la pet cuando sea útil. Reencuentra objetivo tras Feign Death: tu supervivencia debe durar más que su presión.', 'Maintain damage while limiting free shots and controlling the pet when useful. Reacquire after Feign Death: your survival must outlast their pressure.'),
  ('Sobrevivir a la primera cadena y poner presión que dificulte el reset. La segunda apertura no debe pillarte sin respuesta ni con la escuela de Shadow cerrada por Kick.', 'Survive the first chain and apply pressure that makes resetting difficult. Do not face the second opener with no answer or your Shadow school locked by Kick.'),
  ('Forzar que sus curas y dispels cuesten más que reponer tu presión. Contra Discipline, gana por recursos y continuidad; aprovecha una pausa de curas para cerrar.', 'Make their heals and dispels cost more than replacing your pressure. Against Discipline, win through resources and continuity; capitalize on a healing gap to finish.'),
  ('Abrir una ventana de Fear tras eliminar Tremor y evitar que Grounding absorba el control decisivo. Los DoTs deben seguir trabajando mientras él gasta globals en recuperarse.', 'Open a Fear window after removing Tremor and keep Grounding from absorbing decisive control. Let DoTs work while they spend globals recovering.'),
  ('Mantener presión que no desaparezca con cada Remove Lesser Curse y sobrevivir al burst. Fuerza Ice Block, conserva recursos y retoma el daño después de la inmunidad.', 'Maintain pressure that does not vanish with each Remove Lesser Curse and survive burst. Force Ice Block, save resources and resume damage after immunity.'),
  ('Ganar el circuito de vida, maná y demonio. Intercambia dispels y DoTs con eficiencia; un cambio a la pet solo vale si niega más supervivencia que el daño que regalas al dueño.', 'Win the health, Mana and demon resource loop. Trade dispels and DoTs efficiently; switching to the pet is worthwhile only if it denies more survival than the free damage given to its owner.'),
  ('Negar una recuperación completa y presionar cuando salga a curarse. Mantén daño mágico además de efectos que pueda quitar; no gastes todo persiguiendo Travel Form.', 'Deny full recovery and pressure when they leave form to heal. Maintain magic damage alongside effects they can remove; do not spend everything chasing Travel Form.'),
 ],
 'druid': [
  ('Aguantar su contacto en oso y crear espacio real para curarte. Gana si cada reset recupera más vida de la que cuesta en maná y no permite una reconexión gratuita.', 'Hold melee contact in Bear Form and create real space to heal. Win if each reset restores more health than its Mana cost and denies a free reconnection.'),
  ('Ganar eficiencia de maná con formas, presión y curas medidas. Fuerza protecciones antes de comprometer el daño y evita curarte dentro de Hammer of Justice disponible.', 'Win Mana efficiency with forms, pressure and measured healing. Force protections before committing damage and avoid vulnerable healing with Hammer of Justice ready.'),
  ('Llegar con vida al siguiente intercambio y negar disparos cómodos. Si reseteas, controla también la pet; alejarte con ella encima no compra una cura segura.', 'Reach the next trade with health and deny comfortable shooting. When resetting, also control the pet; moving away with it on you does not buy safe healing.'),
  ('Recibir el opener en una forma resistente cuando puedas y negar su reapertura. Castiga tras su control y cura con espacio, sin salir de oso justo para recibir toda la cadena.', 'Take the opener in a durable form when possible and deny a reopener. Punish after their control and heal with space, without leaving Bear Form into the full chain.'),
  ('Forzarle a curar con presión sostenida y guardar maná para cambios de forma. Contra dispels, evita invertir todo en HoTs; castiga su cura cuando tu control pueda negarla.', 'Force healing with sustained pressure and save Mana for shapeshifts. Against dispels, avoid investing everything in HoTs; punish their heal when your control can deny it.'),
  ('Mantener daño sin pagar repetidamente HoTs que Purge elimina. Crea una pausa de Earth Shock para curarte y castiga la cura rival con tu control disponible.', 'Maintain damage without repeatedly paying for HoTs removed by Purge. Heal while Earth Shock is unavailable and punish their healing with your available control.'),
  ('Convertir cambios de forma en contacto útil o una cura segura. Fuerza Blink e inmunidad sin agotar maná; el remate llega cuando ya no pueda separarse de tu daño.', 'Turn shapeshifts into useful contact or safe healing. Force Blink and immunity without exhausting Mana; finish when they can no longer escape your damage.'),
  ('Evitar que cada reset quede anulado por DoTs y demonio. Quitar una maldición no basta: crea una ventana real de curación y vuelve a presionar con recursos.', 'Keep DoTs and the demon from denying every reset. Removing a curse is not enough: create a real healing window and return to pressure with resources.'),
  ('Ganar el gasto de maná en formas y curas y castigar al rival cuando salga a curarse. No persigas cada desplazamiento si permite que tus propias reservas desaparezcan.', 'Win Mana spending on forms and healing and punish leaving form to heal. Do not chase every movement if it drains your own reserves.'),
 ],
}

CHECKS = {
 'warrior': ('Ventana rival: espera a que termine Berserker Rage antes de contar con Fear o incapacitación. Si tiene Death Wish, también da inmunidad a Fear. Respeta Shield Wall y guarda una respuesta para Intercept.', 'Enemy window: wait for Berserker Rage to end before relying on Fear or incapacitation. Death Wish also gives Fear immunity if talented. Respect Shield Wall and keep an answer to Intercept.'),
 'paladin': ('Antes del remate: observa Divine Protection, Blessing of Protection y Hammer of Justice. La protección física no impide todo el daño mágico. A nivel 30 no tiene Divine Shield ni Cleanse; una build de curación exige más presión y gestión de recursos.', 'Before finishing: watch Divine Protection, Blessing of Protection and Hammer of Justice. Physical protection does not stop all magic damage. At level 30 they lack Divine Shield and Cleanse; a healing build demands more pressure and resource management.'),
 'hunter': ('Antes del remate: conserva alcance y objetivo tras Feign Death, identifica la trampa y cuenta la mascota como otra fuente de daño. No confundas controlar al dueño con detener también a la pet.', 'Before finishing: maintain range and reacquire after Feign Death, identify the trap and count the pet as another damage source. Controlling the owner does not automatically stop the pet.'),
 'rogue': ('Antes del remate: identifica Evasion, Vanish y su salida del control. Evasion limita ataques que pueda esquivar; no equivale a inmunidad mágica. Un DoT puede dificultar el reset, pero puede romper tu propio control de daño.', 'Before finishing: identify Evasion, Vanish and their CC escape. Evasion limits attacks they can dodge; it is not magic immunity. A DoT can hinder a reset but can also break your own damage-sensitive CC.'),
 'priest': ('Antes del remate: diferencia Discipline/curación de Shadow. Dispel Magic, Psychic Scream y Mana Burn cambian las prioridades. Contra curas busca una ventana de interrupción o control; contra Shadow, no esperes una guerra de curas idéntica.', 'Before finishing: distinguish Discipline/healing from Shadow. Dispel Magic, Psychic Scream and Mana Burn change priorities. Against healing seek an interrupt or CC window; against Shadow do not assume the same healing war.'),
 'shaman': ('Antes del remate: Grounding puede interceptar un hechizo y Tremor responde a Fear. Destruye manualmente el tótem que estorbe tu plan, no todos por rutina. Cuenta Earth Shock antes de una cura o casteo importante.', 'Before finishing: Grounding can intercept a spell and Tremor counters Fear. Manually destroy the totem blocking your plan, not every totem by habit. Account for Earth Shock before an important heal or cast.'),
 'mage': ('Antes del remate: identifica Blink, Counterspell y, si su build lo lleva, Ice Block/Cold Snap. No descargues el burst en inmunidad. Polymorph puede dar recuperación al objetivo: un reset también puede ayudar al rival.', 'Before finishing: identify Blink, Counterspell and Ice Block/Cold Snap if talented. Do not spend burst into immunity. Polymorph can let its target recover: a reset can help the opponent too.'),
 'warlock': ('Antes del remate: identifica demonio y Soul Link; no todas las builds lo llevan. A nivel 30 el Felhunter tiene Devour Magic, pero no Spell Lock (36); tampoco cuentes Death Coil (42). Matar la pet es una decisión de presión, no una regla automática.', 'Before finishing: identify the demon and Soul Link; not every build has it. At level 30 Felhunter has Devour Magic, but no Spell Lock (36); do not plan around Death Coil (42) either. Killing the pet is a pressure decision, not an automatic rule.'),
 'druid': ('Antes del remate: distingue Feral de caster/curación. Cambiar de forma puede quitar raíces y ralentizaciones, pero cuesta maná. Oso resiste mejor el daño físico; curar en forma humanoide abre una oportunidad. A nivel 30 no cuenta con Cyclone.', 'Before finishing: distinguish Feral from caster/healing. Shapeshifting can remove roots and slows but costs Mana. Bear Form handles physical damage better; healing in caster form opens an opportunity. At level 30 they have no Cyclone.'),
}

WARLOCK_IDS = dict(zip(('warrior', 'rogue', 'mage', 'priest', 'hunter', 'paladin', 'shaman', 'druid', 'warlock'), range(1, 10)))

CSS = '''.win-condition{border-left:3px solid #d5aa52;background:rgba(213,170,82,.07);padding:1rem 1.2rem;margin:1rem 0;border-radius:0 8px 8px 0}.win-condition h3{margin:0 0 .5rem;color:#efd294}.win-condition p:last-child{margin-bottom:0}.win-condition .win-check{font-size:.93em;opacity:.9}.win-intro{padding:1rem;border:1px solid rgba(213,170,82,.25);border-radius:8px;margin:1rem 0}.alpha-download ol{padding-left:1.4rem}.alpha-download code{overflow-wrap:anywhere}.alpha-download .btn{margin:.4rem .5rem .4rem 0}'''

def alpha(en):
    def t(es, eng): return eng if en else es
    return ('<details class="section" id="addon-alpha"><summary>Muchamiel Lock PvP · alpha 0.2.0 · Panel del rival</summary><div class="section-body alpha-download">'
        '<p>' + t('Nueva alpha de Van para el brujo de Muchamiel: duelos y BGs. Sustituye a la 0.1.0; esta es la única versión descargable aquí. Incluye seguimiento experimental de usos enemigos, efectos activos, buffs mágicos y tótems visibles. Sintaxis y lógica comprobadas con pruebas simuladas, todavía sin validar dentro de Forever.',
        'Van’s new alpha for Muchamiel’s Warlock: duels and BGs. Replaces 0.1.0; this is the only version downloadable here. Includes experimental enemy cast tracking, active effects, magic buffs and visible totems. Syntax and logic checked with simulated tests, not yet validated inside Forever.') + '</p>'
        '<a class="btn gold" href="/downloads/MuchamielLockPvP-alpha.zip" download>⬇ ' + t('Descargar alpha 0.2.0 · ZIP', 'Download alpha 0.2.0 · ZIP') + '</a>'
        '<a class="btn ghost" href="/downloads/MuchamielLockPvP-README-' + ('en' if en else 'es') + '.txt">' + t('Leer instrucciones completas', 'Read full instructions') + '</a>'
        '<h3>' + t('Ver lo que ha gastado el rival', 'See what the opponent has used') + '</h3><p>'
        + t('Abre <code>/mlp rival</code> o pulsa «CDs del rival» en /mlp. El panel muestra los hechizos prioritarios de la clase del objetivo o foco y su racial según la raza. Solo registra automáticamente los usos cuando recibe un evento legible; no conoce el estado inicial del rival. Los tiempos parten del cooldown base que exponga el cliente o de los segundos que tú configures, y siempre se presentan como estimaciones.',
        'Open <code>/mlp rival</code> or click “CDs del rival” in /mlp. The panel shows priority spells for the target/focus class and racials for their race. It only records casts automatically when a readable event arrives; it does not know the opponent’s initial cooldown state. Timers use the client’s exposed base cooldown or seconds you configure and are always labelled estimates.')
        + '</p>' + enemy_catalog(en) + '<p>'
        + t('Estados: <strong>ACTIVO</strong> = buff identificado ahora; <strong>~Ns</strong> = cooldown estimado tras un uso; <strong>~Podría estar listo</strong> = terminó la estimación, no confirma disponibilidad; <strong>Desconocido</strong> = no hay un uso observado. Un reset detectado invalida las estimaciones anteriores en vez de afirmar que están listos. Para un uso que hayas visto, haz clic en el botón de ese hechizo. Escribe segundos junto a él y pulsa Enter para cambiar su estimación. No pulses por rutina: cada clic marca un uso nuevo.',
        'States: <strong>ACTIVO</strong> = a currently identified buff; <strong>~Ns</strong> = estimated cooldown after a cast; <strong>~Podría estar listo</strong> = the estimate ended, not confirmed readiness; <strong>Desconocido</strong> = no observed cast. A detected reset invalidates previous estimates instead of claiming readiness. Click a spell button to mark a use you actually witnessed. Enter seconds beside it and press Enter to change the estimate. Do not click repeatedly: each click records a new use.')
        + '</p><h3>' + t('Tótems y cosas para disipar', 'Totems and buffs to dispel') + '</h3><p>'
        + t('Tótems: aviso por nombre inglés en placas enemigas visibles, con sonido opcional; detección experimental de Tremor, Grounding, Earthbind, Windfury y Searing. Buffs: muestra hasta tres efectos mágicos legibles del rival, priorizando por ejemplo Fear Ward, escudos y curas periódicas. Es una lista de candidatos para Devour Magic, no una garantía de disipación; las inmunidades a disipar y los datos restringidos requieren comprobación en el cliente.',
        'Totems: English-name alerts on visible enemy nameplates with optional sound; experimental detection of Tremor, Grounding, Earthbind, Windfury and Searing. Buffs: up to three readable enemy magic effects, prioritizing effects such as Fear Ward, shields and healing over time. These are Devour Magic candidates, not guaranteed dispels; dispel immunity and restricted data require client testing.')
        + '</p><h3>' + t('Módulos y DR', 'Modules and DR') + '</h3><p>'
        + t('Cada módulo se activa o desactiva desde /mlp, con perfiles Duelos/BGs y paneles movibles. Las instalaciones nuevas empiezan con rival, buffs mágicos y tótems activos; una actualización conserva tus ajustes. Mantiene DoTs propios, casteos de objetivo/foco, Soul Link/Nightfall, piedras, shards y demonio como opciones. No duplica vida/maná del jugador. Para DR real instala <a href="../addons/#pvp-addons">Forever Simple DR</a> y configura /fdr; no está incluido en este ZIP.',
        'Toggle each module in /mlp, with Duels/BGs profiles and movable panels. New installations enable enemy tracking, magic buffs and totems; updates preserve your settings. Own DoTs, target/focus casts, Soul Link/Nightfall, stones, shards and demon status remain optional. No duplicate player health/Mana. For actual DR, install <a href="../addons/#pvp-addons">Forever Simple DR</a> and configure /fdr; it is not included in this ZIP.')
        + '</p><h3>' + t('Qué sigue pendiente', 'What is still pending') + '</h3><p>'
        + t('Validación en duelos y BGs, detección de usos que la beta no comunique, modificadores de talentos/cargas/cooldowns compartidos, DR integrado, cooldowns de objetos y de tu demonio. No es un tracker completo ni exacto de todos los enemigos. La ausencia de un buff legible tampoco confirma que no haya protección. Ningún módulo lanza hechizos ni selecciona tótems automáticamente.',
        'Duel/BG validation, casts not exposed by beta, talent/charge/shared-cooldown modifiers, integrated DR and item/own demon cooldowns are pending. This is not a complete or exact tracker of all enemies. A lack of readable buffs does not confirm the absence of protection. No module casts spells or targets totems automatically.')
        + '</p><h3>' + t('Instalar en el cliente de Forever', 'Install in the Forever client') + '</h3><ol><li>'
        + t('Descarga y extrae el ZIP. Copia la carpeta <code>MuchamielLockPvP</code> dentro de <code>Interface/AddOns</code> del cliente que uses para Forever.',
        'Download and extract the ZIP. Copy the <code>MuchamielLockPvP</code> folder into <code>Interface/AddOns</code> of your Forever client.')
        + '</li><li>' + t('Comprueba que quede <code>Interface/AddOns/MuchamielLockPvP/MuchamielLockPvP.toc</code>, sin una carpeta duplicada dentro. Reinicia el juego y actívalo en AddOns.',
        'Check that the path is <code>Interface/AddOns/MuchamielLockPvP/MuchamielLockPvP.toc</code>, with no duplicate nested folder. Restart the game and enable it in AddOns.')
        + '</li><li>' + t('Abre <code>/mlp</code>, elige Duelos o BGs y activa lo que quieras. Prueba /mlp rival con Kick, Psychic Scream y una racial en duelos amistosos. Usa <code>/mlp diag</code> para recoger versión, APIs y eventos legibles observados. <code>/mlp reset</code> borra las observaciones; úsalo cuando el contexto del duelo se reinicie.',
        'Open <code>/mlp</code>, choose Duels or BGs and enable your modules. Test /mlp rival with Kick, Psychic Scream and a racial in friendly duels. Use <code>/mlp diag</code> for version, APIs and readable-event counts. <code>/mlp reset</code> clears observations; use it when the duel context resets.')
        + '</li></ol><p>' + t('Para revisar fallos: pásale a Van el resultado de /mlp diag, el error completo y qué estabas haciendo. No des por fiables los avisos para el torneo hasta probarlos en tu cliente. La beta puede restringir datos de forma distinta en BGs.',
        'To report issues, send Van the /mlp diag output, the full error and what you were doing. Test alerts in your client before relying on them in the tournament. Beta data restrictions may differ in BGs.')
        + '</p></div></details>')

def enemy_catalog(en):
    rows = [
        ('Rogue', 'Kick · Kidney Shot · Evasion · Vanish · Sprint · Preparation'),
        ('Priest', 'Psychic Scream · Fear Ward · Silence · Penance · Inner Focus'),
        ('Warrior', 'Berserker Rage · Intercept · Shield Bash · Shield Wall · Death Wish'),
        ('Shaman', 'Earth Shock · Grounding Totem · Tremor Totem · Purge'),
        ('Mage', 'Counterspell · Blink · Ice Block · Cold Snap · Frost Nova'),
        ('Paladin', 'Hammer of Justice · Divine Protection · Blessing of Protection · Blessing of Freedom'),
        ('Hunter', 'Freezing Trap · Frost Trap · Feign Death · Intimidation · Scatter Shot · Deterrence'),
        ('Warlock', 'Fear · Devour Magic · Seduction · Sacrifice · Fel Domination'),
        ('Druid', "Bash · Dash · Nature’s Grasp · Nature’s Swiftness"),
    ]
    return ('<table><thead><tr><th>' + ('Rival' if not en else 'Opponent') + '</th><th>'
            + ('Catálogo de avisos' if not en else 'Alert catalogue') + '</th></tr></thead><tbody>'
            + ''.join('<tr><td>'+c+'</td><td>'+escape(spells)+'</td></tr>' for c,spells in rows)
            + '</tbody></table><p>' + ('La lista se filtra por nivel cuando el dato es legible. No confirma qué talentos tiene el rival. Las raciales van por raza: Will of the Forsaken en Undead, Stoneform en Dwarf, Escape Artist en Gnome, etc. Evasion no es inmunidad a Fear.' if not en else
            'The list is filtered by level when readable. It does not confirm the opponent’s talents. Racials follow race: Will of the Forsaken for Undead, Stoneform for Dwarf, Escape Artist for Gnome, etc. Evasion is not Fear immunity.') + '</p>')

EN_README = '''Muchamiel Lock PvP — 0.2.0 alpha
Author: Van. Warlock addon for the WoW Forever beta.
Syntax checked only. Not validated inside the game.

INSTALL
Extract the ZIP and copy MuchamielLockPvP to your Forever client's Interface/AddOns.
Correct path: Interface/AddOns/MuchamielLockPvP/MuchamielLockPvP.toc
Restart the client, enable in AddOns. /mlp opens settings; /mlp diag shows diagnostics.
Separate Duels/BGs profiles. Modules can be toggled; panels can be moved and resized.

CURRENT ALPHA
New enemy panel: /mlp rival, target or focus, catalog for nine classes and racials.
Automatic observations only from readable UNIT_SPELLCAST_SUCCEEDED events.
Timers use exposed GetSpellBaseCooldown metadata or manually configured seconds;
they are estimates, never actual enemy cooldown queries. Unseen = unknown, expired
estimate = possibly ready. Detected Preparation/Cold Snap invalidate prior estimates.
Click a spell only to mark a use you witnessed; edit seconds and press Enter.
/mlp reset clears observations. Restricted events are skipped. English spell names.
Active priority buffs and readable magic-buff candidates for Devour Magic.
No guarantee every magic effect is dispellable or every protective effect is readable.
New installations enable enemy panel, magic buffs and visible totems; upgrades
preserve toggles. DR requires a separate Forever Simple DR install (/fdr).
Readable own target DoTs, target/focus cast text and countdowns, identifiable Soul Link,
armor and Nightfall buffs, Healthstone quantity (not item cooldown), Soul Shards with
low-stock warning, learned racial cooldown when readable, demon state and current
action-bar abilities (not pet cooldowns). Experimental English-name visible totem
detection. Up to three magic-buff candidates, not a comprehensive cooldown tracker.
Optional pet health/Mana. No duplicate player health/Mana display.

PENDING
Real DR integration (the DR panel is only a placeholder; use Forever Simple DR),
Healthstone/pet ability cooldowns, graphical cast bars, native restricted-data display,
unexposed enemy casts, talent/shared cooldown/charge modifiers. Restricted fields are indicated, not
calculated by bypassing restrictions. No automatic casts, targeting or messages.

TEST
Confirm loading and version with /mlp diag. Toggle, move, change profile, /reload and
check settings persistence. Test Kick, Psychic Scream, racial and casts in a friendly duel, then
a BG. Report diagnostic output, full Lua errors and reproduction steps to Van.
Do not rely on tournament alerts before testing them in the actual client.

PATCH REFERENCE
Blizzard's Sep 22 client announcement confirms branch 1.60.1. The Oct 8 notes do not
state a build number. TOC 16001 follows the Forever addons checked; confirm locally.
https://us.forums.blizzard.com/en/wow/t/beta-client-update-september-22/2358655
https://us.forums.blizzard.com/en/wow/t/wow-forever-beta-development-notes-%E2%80%93-updated-october-8/2360696/5
'''

def install(dist):
    assert set(GOALS) == set(CLASSES)
    assert all(len(row) == 9 and all(len(pair) == 2 for pair in row) for row in GOALS.values())
    total = 0
    for en in (False, True):
        root = dist / 'en' if en else dist
        if en and not root.exists():
            continue  # /en/ aún sin generar (traducción pendiente)
        for own in CLASSES:
            file = root / own / 'index.html'
            s = file.read_text(encoding='utf-8')
            if 'id="duel-win-css"' in s:
                raise ValueError('Win conditions already installed; rebuild from source')
            intro = ('<div class="win-intro"><strong>' + ('Cómo ganar este duelo' if not en else 'How to win this duel') + '</strong><p>'
                + ('Win condition = la situación que necesitas crear para cerrar el duelo: recursos, distancia, control y respuesta defensiva gastada. Planes propuestos por Van para nivel 30 y 26 puntos (21 + 5 de legado); usa solo habilidades y talentos que tengas. Adapta al spec, raza y equipo del rival. No son resultados medidos ni victorias garantizadas. Respeta los límites y consumibles del reglamento vigente.' if not en else
                   'Win condition = the situation you need to create to finish the duel: resources, range, control and a spent defensive answer. Tactical proposals by Van for level 30 with 26 points (21 + 5 Legacy); use only abilities and talents you actually have. Adapt to enemy spec, race and gear. These are not measured outcomes or guaranteed wins. Respect the current rules on boundaries and consumables.')
                + '</p><p>' + ('Habilidades por nivel: ' if not en else 'Abilities by level: ')
                + f'<a href="https://talentsforever.com/{own}/abilities" target="_blank" rel="noopener noreferrer">Talents Forever</a> · '
                + ('Referencia de beta consultada el 9 de octubre de 2026.' if not en else 'Beta reference checked on Oct 9, 2026.') + '</p></div>')
            pattern = r'(<details\b[^>]*id="duelos"[^>]*>\s*<summary>.*?</summary>\s*<div class="section-body">)'
            s, count = re.subn(pattern, lambda m: m[1] + intro, s, count=1, flags=re.S)
            assert count == 1, (file, 'duelos missing')
            for i, enemy in enumerate(CLASSES):
                entry = f'DU{WARLOCK_IDS[enemy]}' if own == 'warlock' else f'D-{enemy}'
                block = (f'<aside class="win-condition" id="win-{enemy}" data-win-condition="{own}-{enemy}"><h3>'
                    + ('Condición de victoria' if not en else 'Win condition') + '</h3><p>'
                    + escape(GOALS[own][i][int(en)]) + '</p><p class="win-check">'
                    + escape(CHECKS[enemy][int(en)]) + '</p></aside>')
                pattern = rf'(<details\b[^>]*id="{entry}"[^>]*>\s*<summary>.*?</summary>\s*<div class="detail-body">\s*<a class="permalink"[^>]*>.*?</a>)'
                s, count = re.subn(pattern, lambda m: m[1] + block, s, count=1, flags=re.S)
                assert count == 1, (file, entry)
                total += 1
            s = s.replace('</head>', '<style id="duel-win-css">' + CSS + '</style></head>', 1)
            if own == 'warlock':
                marker = re.search(r'<details\b[^>]*id="duelos"', s)
                assert marker
                s = s[:marker.start()] + alpha(en) + s[marker.start():]
                # Add the new section to the existing local navigation if present.
                s = s.replace('<a href="#duelos">', '<a href="#addon-alpha">Addon alpha</a><a href="#duelos">', 1)
                if not en:
                    s = s.replace('href="../../addons/#pvp-addons"', 'href="../addons/#pvp-addons"')
            file.write_text(s, encoding='utf-8')
    downloads = dist / 'downloads'
    downloads.mkdir(exist_ok=True)
    source = Path(__file__).resolve().parent / 'MuchamielLockPvP'  # 29-10: copia dentro de la carpeta, para generar en la nube
    if not source.exists():
        source = Path(__file__).resolve().parent.parent / 'MuchamielLockPvP'
    # Assemble a clean ZIP from the actual alpha, keeping the correct folder depth.
    with zipfile.ZipFile(downloads / 'MuchamielLockPvP-alpha.zip', 'w', zipfile.ZIP_DEFLATED) as z:
        for p in sorted(source.iterdir()):
            if p.is_file():
                z.write(p, 'MuchamielLockPvP/' + p.name)
    shutil.copyfile(source / 'LEEME.md', downloads / 'MuchamielLockPvP-README-es.txt')
    (downloads / 'MuchamielLockPvP-README-en.txt').write_text(EN_README, encoding='utf-8')
    print(f'Win conditions: {total} localized matchups; alpha packaged for download.')
