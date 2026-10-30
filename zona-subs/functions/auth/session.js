import {firmar, cookie, json, lista} from '../_lib.js';

// Recibe el token de Discord del navegador, pregunta a Discord si esa persona está en el servidor de Muchamiel
// y con qué roles, y si tiene uno de sub abre la sesión. El token no se guarda.
export async function onRequestPost({request, env}) {
  let token = '';
  try { token = (await request.json()).token || ''; } catch { /* cuerpo vacío */ }
  if (!/^[A-Za-z0-9._-]{20,200}$/.test(token)) return json({ok: false, motivo: 'token'}, 400);

  const r = await fetch(`https://discord.com/api/v10/users/@me/guilds/${env.GUILD_ID}/member`, {
    headers: {Authorization: `Bearer ${token}`}
  });
  if (r.status === 404) return json({ok: false, motivo: 'no-servidor'}, 403);
  if (!r.ok) return json({ok: false, motivo: 'discord', estado: r.status}, 502);
  const m = await r.json();
  const id = m.user?.id;
  const nombre = m.nick || m.user?.global_name || m.user?.username || 'Sub';
  const roles = m.roles || [];
  const rolesSub = lista(env.ROLE_IDS);
  const permitidos = [...lista(env.ALLOW_USER_IDS), ...lista(env.ADMIN_IDS)];   // 30-10: los administradores (Muchamiel, Van) entran aunque no sean subs
  const esSub = roles.some(x => rolesSub.includes(x));
  if (!esSub && !permitidos.includes(id)) return json({ok: false, motivo: 'no-sub', id, roles}, 403);

  const avatar = m.user?.avatar ? `https://cdn.discordapp.com/avatars/${id}/${m.user.avatar}.png?size=64` : '';
  const valor = await firmar(env, {id, nombre, avatar, prueba: !esSub});
  return json({ok: true, nombre}, 200, {'Set-Cookie': cookie(valor)});
}
