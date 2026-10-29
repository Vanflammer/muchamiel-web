import {json, esAdmin} from '../_lib.js';

export function onRequestGet({env, data}) {
  const {nombre, avatar, prueba} = data.sesion;
  return json({nombre, avatar, prueba: !!prueba, admin: esAdmin(env, data.sesion)});
}
