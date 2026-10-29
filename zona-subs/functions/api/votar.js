import {json} from '../_lib.js';
import {ENCUESTA} from './_encuesta.js';

// Un voto por persona y encuesta, guardado en KV como votos:<encuesta>:<id de Discord>.
// La lista de KV tarda unos segundos en ver los votos nuevos: el voto propio se cuenta aparte, siempre al día.
async function resultados(env, id, mio) {
  const cuenta = ENCUESTA.opciones.map(() => 0);
  const propia = `votos:${ENCUESTA.id}:${id}`;
  let cursor;
  do {
    const r = await env.SUBS_KV.list({prefix: `votos:${ENCUESTA.id}:`, cursor});
    for (const k of r.keys) {
      if (k.name === propia) continue;
      const v = Number(k.metadata?.op);
      if (v >= 0 && v < cuenta.length) cuenta[v]++;
    }
    cursor = r.list_complete ? null : r.cursor;
  } while (cursor);
  if (mio !== null && mio >= 0 && mio < cuenta.length) cuenta[mio]++;
  return cuenta;
}

export async function onRequestGet({env, data}) {
  const v = await env.SUBS_KV.get(`votos:${ENCUESTA.id}:${data.sesion.id}`);
  const mio = v === null ? null : Number(v);
  return json({...ENCUESTA, mio, cuenta: await resultados(env, data.sesion.id, mio)});
}

export async function onRequestPost({request, env, data}) {
  let op = -1;
  try { op = Number((await request.json()).opcion); } catch { /* nada */ }
  if (!Number.isInteger(op) || op < 0 || op >= ENCUESTA.opciones.length) return json({ok: false}, 400);
  await env.SUBS_KV.put(`votos:${ENCUESTA.id}:${data.sesion.id}`, String(op), {metadata: {op}});
  return json({ok: true, mio: op, cuenta: await resultados(env, data.sesion.id, op)});
}
