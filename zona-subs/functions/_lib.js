// Zona de subs de Muchamiel (Van y Claude, 30-10-2026).
// Sesión firmada en una cookie: quien entra con Discord y tiene un rol de sub (Twitch, YouTube o Patreon) en su servidor.
// No se guarda ninguna contraseña ni el token de Discord: solo id, nombre y caducidad, firmados con SESSION_KEY.

const enc = new TextEncoder();
export const COOKIE = 'mz_sub';
const DIAS = 7;

function b64url(bytes) {
  let s = '';
  for (const b of new Uint8Array(bytes)) s += String.fromCharCode(b);
  return btoa(s).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}
function deb64url(s) {
  s = s.replace(/-/g, '+').replace(/_/g, '/');
  return Uint8Array.from(atob(s + '==='.slice((s.length + 3) % 4)), c => c.charCodeAt(0));
}
async function clave(env) {
  return crypto.subtle.importKey('raw', enc.encode(env.SESSION_KEY), {name: 'HMAC', hash: 'SHA-256'}, false, ['sign', 'verify']);
}

export async function firmar(env, datos) {
  const cuerpo = b64url(enc.encode(JSON.stringify({...datos, exp: Date.now() + DIAS * 864e5})));
  const firma = b64url(await crypto.subtle.sign('HMAC', await clave(env), enc.encode(cuerpo)));
  return `${cuerpo}.${firma}`;
}

export async function leerSesion(request, env) {
  const m = (request.headers.get('Cookie') || '').match(new RegExp(`(?:^|;\\s*)${COOKIE}=([^;]+)`));
  if (!m) return null;
  const [cuerpo, firma] = m[1].split('.');
  if (!cuerpo || !firma) return null;
  try {
    const ok = await crypto.subtle.verify('HMAC', await clave(env), deb64url(firma), enc.encode(cuerpo));
    if (!ok) return null;
    const datos = JSON.parse(new TextDecoder().decode(deb64url(cuerpo)));
    return datos.exp > Date.now() ? datos : null;
  } catch {
    return null;
  }
}

export function cookie(valor, maxAge = DIAS * 86400) {
  return `${COOKIE}=${valor}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${maxAge}`;
}

export function json(datos, status = 200, extra = {}) {
  return new Response(JSON.stringify(datos), {status, headers: {'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', ...extra}});
}

export const lista = v => (v || '').split(',').map(x => x.trim()).filter(Boolean);

// Administradores (Muchamiel y quien él quiera): ids de Discord en ADMIN_IDS. Pueden subir guías, crear eventos y cerrar preguntas.
export const esAdmin = (env, sesion) => !!sesion && lista(env.ADMIN_IDS).includes(sesion.id);

// Lee y guarda una lista JSON en KV.
export async function leerKV(env, clave) {
  return JSON.parse((await env.SUBS_KV.get(clave)) || '[]');
}
export async function guardarKV(env, clave, valor) {
  await env.SUBS_KV.put(clave, JSON.stringify(valor));
}
export const nuevoId = () => Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
export const limpio = (s, n) => String(s || '').replace(/[\u0000-\u0008\u000b-\u001f]/g, '').trim().slice(0, n);
