import {json, leerKV, guardarKV, esAdmin, nuevoId, limpio} from '../_lib.js';

// Eventos (bandas, mazmorras, JcJ con Muchamiel): los subs se apuntan como tanque (T), sanador (H) o daño (D) mientras queden plazas.
// KV «eventos»: [{id, titulo, cuando (ISO con hora), descripcion, plazas: {T,H,D}, apuntados: [{id, nombre, rol}]}]
const ROLES = ['T', 'H', 'D'];

function vista(e, yo) {
  const cuenta = Object.fromEntries(ROLES.map(r => [r, e.apuntados.filter(a => a.rol === r).length]));
  return {...e, cuenta, mio: (e.apuntados.find(a => a.id === yo) || {}).rol || null};
}

export async function onRequestGet({env, data}) {
  const ahora = Date.now() - 6 * 3600e3;  // se ven hasta 6 horas después de empezar
  const ev = (await leerKV(env, 'eventos')).filter(e => Date.parse(e.cuando) > ahora).sort((a, b) => a.cuando.localeCompare(b.cuando));
  return json({eventos: ev.map(e => vista(e, data.sesion.id)), admin: esAdmin(env, data.sesion)});
}

export async function onRequestPost({env, request, data}) {
  const b = await request.json().catch(() => ({}));
  let ev = await leerKV(env, 'eventos');
  const yo = data.sesion;

  if (b.admin) {  // crear, editar o borrar (solo administradores)
    if (!esAdmin(env, yo)) return json({error: 'solo administradores'}, 403);
    if (b.borrar) ev = ev.filter(e => e.id !== b.id);
    else {
      const viejo = ev.find(e => e.id === b.id);
      const e = {
        id: b.id || nuevoId(), titulo: limpio(b.titulo, 100), descripcion: limpio(b.descripcion, 600),
        cuando: limpio(b.cuando, 40),
        plazas: Object.fromEntries(ROLES.map(r => [r, Math.max(0, Math.min(40, parseInt(b.plazas?.[r]) || 0))])),
        apuntados: viejo ? viejo.apuntados : []
      };
      if (!e.titulo || isNaN(Date.parse(e.cuando))) return json({error: 'faltan título o fecha'}, 400);
      ev = ev.filter(x => x.id !== e.id).concat(e);
    }
    await guardarKV(env, 'eventos', ev);
    return json({ok: true});
  }

  const e = ev.find(x => x.id === b.id);
  if (!e) return json({error: 'no existe'}, 404);
  e.apuntados = e.apuntados.filter(a => a.id !== yo.id);
  if (b.rol) {
    if (!ROLES.includes(b.rol)) return json({error: 'rol'}, 400);
    if (e.apuntados.filter(a => a.rol === b.rol).length >= e.plazas[b.rol]) return json({error: 'No quedan plazas de ese rol'}, 409);
    e.apuntados.push({id: yo.id, nombre: String(yo.nombre).slice(0, 40), rol: b.rol});
  }
  await guardarKV(env, 'eventos', ev);
  return json({ok: true, evento: vista(e, yo.id)});
}
