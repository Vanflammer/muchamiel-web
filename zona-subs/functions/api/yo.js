import {json} from '../_lib.js';

export function onRequestGet({data}) {
  const {nombre, avatar, prueba} = data.sesion;
  return json({nombre, avatar, prueba: !!prueba});
}
