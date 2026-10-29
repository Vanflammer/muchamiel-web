import {leerSesion} from './_lib.js';

// Todo está cerrado salvo la puerta (entrar), el inicio de sesión y los estilos.
const ABIERTO = [/^\/entrar(\.html)?$/, /^\/auth\//, /^\/assets\//, /^\/favicon/, /^\/robots\.txt$/];

export async function onRequest(context) {
  const {request, env, next, data} = context;
  const ruta = new URL(request.url).pathname;
  if (ABIERTO.some(r => r.test(ruta))) return next();
  const sesion = await leerSesion(request, env);
  if (!sesion) {
    if (ruta.startsWith('/api/')) return new Response('No has entrado', {status: 401});
    return Response.redirect(new URL('/entrar', request.url).toString(), 302);
  }
  data.sesion = sesion;
  const res = await next();
  const r = new Response(res.body, res);
  r.headers.set('Cache-Control', 'private, no-store');
  return r;
}
