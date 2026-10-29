import {cookie} from './_lib.js';

export function onRequest({request}) {
  return new Response(null, {status: 302, headers: {Location: new URL('/entrar', request.url).toString(), 'Set-Cookie': cookie('', 0)}});
}
