import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import worker, {validFeed} from './worker.mjs';

const xml = await readFile(new URL('../research/muchamiel-feed.xml', import.meta.url), 'utf8');
assert(validFeed(xml));
assert(!validFeed('<html>Not a feed</html>'));
assert(!validFeed(xml.replaceAll('UCLKDtwQj4YDatBOQPkOlDlA', 'UCxxxxxxxxxxxxxxxxxxxxxx')));
let stored, calls = 0, failure = false;
globalThis.caches = {default: {
  async match() { return stored?.clone(); },
  async put(_key, response) { stored = response; }
}};
globalThis.fetch = async (url) => {
  calls++;
  assert.equal(url, 'https://www.youtube.com/feeds/videos.xml?channel_id=UCLKDtwQj4YDatBOQPkOlDlA');
  if (failure) throw new Error('offline');
  return new Response(xml);
};
const env = {ASSETS: {async fetch(request) {
  return request.url.endsWith('youtube-fallback.xml') ? new Response(xml) : new Response('static');
}}};
const pending = [];
const ctx = {waitUntil(promise) { pending.push(promise); }};
const request = new Request('https://example.com/api/youtube-feed');
let result = await worker.fetch(request, env, ctx);
await Promise.all(pending);
assert.equal(result.status, 200);
assert.equal(result.headers.get('X-Feed-State'), 'fresh');
assert.equal(result.headers.get('Access-Control-Allow-Origin'), '*');
assert.equal(await result.text(), xml);
result = await worker.fetch(request, env, ctx);
assert.equal(calls, 1);
assert.equal(result.headers.get('Cache-Control'), 'public, max-age=300');
result = await worker.fetch(new Request(request.url, {method:'HEAD'}), env, ctx);
assert.equal(await result.text(), '');
result = await worker.fetch(new Request(request.url, {method:'POST'}), env, ctx);
assert.equal(result.status, 405);
stored.headers.set('X-Feed-Updated', new Date(Date.now()-7200000).toISOString());
failure = true;
result = await worker.fetch(request, env, ctx);
assert.equal(result.headers.get('X-Feed-State'), 'stale');
assert.equal(await result.text(), xml);
stored = undefined;
result = await worker.fetch(request, env, ctx);
assert.equal(result.headers.get('X-Feed-State'), 'fallback');
assert.equal(await result.text(), xml);
result = await worker.fetch(new Request('https://example.com/warlock/'), env, ctx);
assert.equal(await result.text(), 'static');
console.log('OK: canal, XML, caché, CORS, GET/HEAD, fallo de origen, copia de reserva y páginas estáticas.');
