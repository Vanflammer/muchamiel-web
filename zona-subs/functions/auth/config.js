import {json} from '../_lib.js';

// Lo que necesita el botón «Entrar con Discord». Así, cambiar de aplicación de Discord es cambiar una variable, sin tocar las páginas.
export function onRequestGet({env, request}) {
  return json({client_id: env.CLIENT_ID || '', redirect: new URL('/auth/callback', request.url).toString()});
}
