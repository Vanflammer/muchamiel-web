import {json, leerKV, guardarKV, esAdmin, nuevoId, limpio} from '../_lib.js';

// Preguntas y peticiones del mes: los subs mandan preguntas (se contestan en directo) o piden un aura, una macro o una guía de Forever
// (30-10: idea de Van tras ver el Discord de Kunen; lo más votado se hace).
// KV «preguntas:AAAA-MM»: [{id, tipo, texto, autor, autorId, votos: [ids], respondida}]   tipo: pregunta | aura | macro | guia
const TIPOS = ['pregunta', 'aura', 'macro', 'guia'];
const mes = () => new Date().toISOString().slice(0, 7);

function vista(lista, yo) {
  return lista.map(p => ({id: p.id, tipo: p.tipo || 'pregunta', texto: p.texto, autor: p.autor, votos: p.votos.length, mio: p.votos.includes(yo), respondida: !!p.respondida}))
    .sort((a, b) => (a.respondida - b.respondida) || (b.votos - a.votos));
}

export async function onRequestGet({env, data}) {
  return json({mes: mes(), preguntas: vista(await leerKV(env, `preguntas:${mes()}`), data.sesion.id), admin: esAdmin(env, data.sesion)});
}

export async function onRequestPost({env, request, data}) {
  const b = await request.json().catch(() => ({}));
  const clave = `preguntas:${mes()}`;
  const lista = await leerKV(env, clave);
  const yo = data.sesion;
  if (b.texto) {
    if (lista.filter(p => p.autorId === yo.id).length >= 3) return json({error: 'Máximo 3 por persona al mes'}, 429);
    lista.push({id: nuevoId(), tipo: TIPOS.includes(b.tipo) ? b.tipo : 'pregunta', texto: limpio(b.texto, 280), autor: String(yo.nombre).slice(0, 40), autorId: yo.id, votos: [yo.id], respondida: false});
  } else if (b.voto) {
    const p = lista.find(x => x.id === b.voto);
    if (p) p.votos = p.votos.includes(yo.id) ? p.votos.filter(v => v !== yo.id) : p.votos.concat(yo.id);
  } else if (b.respondida || b.borrar) {
    if (!esAdmin(env, yo)) return json({error: 'solo administradores'}, 403);
    const p = lista.find(x => x.id === (b.respondida || b.borrar));
    if (p && b.respondida) p.respondida = !p.respondida;
    if (p && b.borrar) lista.splice(lista.indexOf(p), 1);
  }
  await guardarKV(env, clave, lista);
  return json({mes: mes(), preguntas: vista(lista, yo.id), admin: esAdmin(env, yo)});
}
