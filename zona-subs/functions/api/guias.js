import {json, leerKV, guardarKV, esAdmin, nuevoId, limpio} from '../_lib.js';

// Guías: salen aquí primero y pasan a la web pública en la fecha «publica» (la recoge /api/publicas).
// KV «guias»: [{id, titulo, resumen, contenido (markdown), publica (AAAA-MM-DD), creada}]

export async function onRequestGet({env, request}) {
  const id = new URL(request.url).searchParams.get('id');
  const guias = await leerKV(env, 'guias');
  if (id) {
    const g = guias.find(x => x.id === id);
    return g ? json(g) : json({error: 'no existe'}, 404);
  }
  return json(guias.map(({contenido, ...resto}) => resto).sort((a, b) => b.creada.localeCompare(a.creada)));
}

// Solo administradores: crear o editar (con id) y borrar ({id, borrar: true}).
export async function onRequestPost({env, request, data}) {
  if (!esAdmin(env, data.sesion)) return json({error: 'solo administradores'}, 403);
  const b = await request.json().catch(() => ({}));
  let guias = await leerKV(env, 'guias');
  if (b.borrar) {
    guias = guias.filter(x => x.id !== b.id);
  } else {
    const g = {
      id: b.id || nuevoId(),
      titulo: limpio(b.titulo, 120),
      resumen: limpio(b.resumen, 300),
      contenido: limpio(b.contenido, 60000),
      publica: /^\d{4}-\d{2}-\d{2}$/.test(b.publica || '') ? b.publica : new Date(Date.now() + 3 * 864e5).toISOString().slice(0, 10),
      creada: (guias.find(x => x.id === b.id) || {}).creada || new Date().toISOString()
    };
    if (!g.titulo || !g.contenido) return json({error: 'faltan título o contenido'}, 400);
    guias = guias.filter(x => x.id !== g.id).concat(g);
  }
  await guardarKV(env, 'guias', guias);
  return json({ok: true});
}
