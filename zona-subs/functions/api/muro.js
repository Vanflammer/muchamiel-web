import {json} from '../_lib.js';

// Muro de agradecimiento: solo sale quien se apunta, y se puede quitar cuando quiera. Guarda id y nombre de Discord.
async function leer(env) {
  return JSON.parse((await env.SUBS_KV.get('muro')) || '[]');
}

export async function onRequestGet({env, data}) {
  const muro = await leer(env);
  return json({nombres: muro.map(x => x.nombre), estoy: muro.some(x => x.id === data.sesion.id)});
}

export async function onRequestPost({request, env, data}) {
  let apuntar = false;
  try { apuntar = !!(await request.json()).apuntar; } catch { /* nada */ }
  let muro = (await leer(env)).filter(x => x.id !== data.sesion.id);
  if (apuntar) muro.push({id: data.sesion.id, nombre: String(data.sesion.nombre).slice(0, 40)});
  muro = muro.slice(-500);
  await env.SUBS_KV.put('muro', JSON.stringify(muro));
  return json({nombres: muro.map(x => x.nombre), estoy: apuntar});
}
