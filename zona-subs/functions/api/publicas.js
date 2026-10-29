import {json, leerKV} from '../_lib.js';

// Abierta (sin sesión): las guías cuya fecha de salida pública ya ha llegado, para pasarlas a la web pública.
export async function onRequestGet({env}) {
  const hoy = new Date().toISOString().slice(0, 10);
  const guias = (await leerKV(env, 'guias')).filter(g => g.publica <= hoy);
  return json(guias.map(({id, titulo, resumen, contenido, publica}) => ({id, titulo, resumen, contenido, publica})));
}
