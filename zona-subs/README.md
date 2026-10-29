# Zona de subs de Muchamiel

https://muchamiel-subs.pages.dev · Solo para subs de Twitch, miembros de YouTube y mecenas de Patreon.

## Cómo funciona
- Se entra con **Discord**, sin contraseñas. La persona autoriza a la aplicación a ver su nombre y sus roles; la web pregunta a Discord si está en el servidor «WOW FOREVER - MUCHAMIEL» (`GUILD_ID`) y si tiene un rol de sub (`ROLE_IDS`). Si lo tiene, abre una sesión de 7 días en una cookie firmada.
- No se guarda el token de Discord ni ninguna contraseña. Solo id, nombre y avatar de Discord, firmados con `SESSION_KEY` (un secreto de Cloudflare).
- Los roles de sub los crea Discord solo al activar las integraciones de Twitch y YouTube (y Patreon, si se usa) en el servidor.

## Qué hay dentro
| Página | Qué hace | Dónde se cambia |
|---|---|---|
| `/` | Portada con las ventajas | `public/index.html` |
| `/vota` | Votación: un voto por persona | La pregunta y las opciones, en `functions/api/_encuesta.js` (cambia el `id` para empezar de cero) |
| `/muro` | Muro de agradecimiento (solo quien se apunta) | `public/muro.html` |
| `/sorteos` | Sorteos para subs y ganadores | `public/sorteos.html` |
| `/entrar`, `/salir` | Entrada y salida | `public/entrar.html`, `functions/salir.js` |

Los datos (votos y muro) están en un almacén KV de Cloudflare (`SUBS_KV`).

## Configuración (`wrangler.toml`)
- `GUILD_ID`: el servidor de Discord.
- `CLIENT_ID`: la aplicación de Discord. **Hoy es una de pruebas de Van**: hay que cambiarla por una de Muchamiel (Discord Developer Portal → Nueva aplicación → OAuth2 → Redirecciones: `https://muchamiel-subs.pages.dev/auth/callback`).
- `ROLE_IDS`: los roles de sub, separados por comas. Para sacar el número de un rol: en Discord, Ajustes → Avanzado → Modo desarrollador; luego, en el servidor, Ajustes → Roles → clic derecho en el rol → Copiar ID.
- `ALLOW_USER_IDS`: personas que entran sin rol, para pruebas (hoy, Van). Vaciar cuando ya no haga falta.

## Publicar un cambio
Desde esta carpeta, con una cuenta de Cloudflare con acceso al proyecto `muchamiel-subs`:
```
npx wrangler@3 pages deploy --branch main
```
Si se crea el proyecto en otra cuenta (la de Muchamiel): `npx wrangler@3 kv namespace create SUBS_KV`, poner el id nuevo en `wrangler.toml`, crear la clave con `npx wrangler@3 pages secret put SESSION_KEY --project-name muchamiel-subs` (un texto largo y aleatorio) y publicar.

## Reglas
- La web pública sigue completa y gratis: aquí va lo de antes, lo extra y lo de la comunidad.
- Nada de datos personales más allá del nombre de Discord, y el muro solo con quien se apunta.
