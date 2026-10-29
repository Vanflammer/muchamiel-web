const CHANNEL = 'UCLKDtwQj4YDatBOQPkOlDlA';
const FEED = `https://www.youtube.com/feeds/videos.xml?channel_id=${CHANNEL}`;
const PATH = '/api/youtube-feed';
const HOUR = 3600;

export function validFeed(xml) {
  return xml.length < 250000 && xml.includes(`<yt:channelId>${CHANNEL}</yt:channelId>`) &&
    /<entry>/.test(xml) && /<yt:videoId>[A-Za-z0-9_-]{11}<\/yt:videoId>/.test(xml);
}

function response(xml, updated, state, status = 200) {
  return new Response(xml, {status, headers: {
    'Content-Type': 'application/atom+xml; charset=utf-8',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Expose-Headers': 'X-Feed-Updated, X-Feed-State',
    'Cache-Control': state === 'fresh' ? 'public, max-age=300' : 'public, max-age=60',
    'X-Content-Type-Options': 'nosniff',
    'X-Feed-Updated': updated,
    'X-Feed-State': state
  }});
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (url.pathname !== PATH) return env.ASSETS.fetch(request);
    if (request.method !== 'GET' && request.method !== 'HEAD') {
      return new Response('Method not allowed', {status: 405, headers: {Allow: 'GET, HEAD'}});
    }
    // Query parameters never alter the channel or the cache key.
    const cacheKey = new Request(`${url.origin}${PATH}`);
    const cached = await caches.default.match(cacheKey);
    const updated = cached?.headers.get('X-Feed-Updated');
    if (cached && updated && Date.now() - Date.parse(updated) < HOUR * 1000) {
      const result = response(await cached.text(), updated, 'fresh');
      return request.method === 'HEAD' ? new Response(null, result) : result;
    }
    try {
      const upstream = await fetch(FEED, {
        headers: {Accept: 'application/atom+xml'},
        signal: AbortSignal.timeout(8000)
      });
      if (!upstream.ok) throw new Error('Feed unavailable');
      const xml = await upstream.text();
      if (!validFeed(xml)) throw new Error('Invalid feed');
      const now = new Date().toISOString();
      const result = response(xml, now, 'fresh');
      // Keep a day of last-known-good data while refreshing it after one hour.
      const stored = response(xml, now, 'fresh');
      stored.headers.set('Cache-Control', 'public, max-age=86400');
      ctx.waitUntil(caches.default.put(cacheKey, stored));
      return request.method === 'HEAD' ? new Response(null, result) : result;
    } catch {
      if (cached) {
        const result = response(await cached.text(), updated, 'stale');
        return request.method === 'HEAD' ? new Response(null, result) : result;
      }
      const fallback = await env.ASSETS.fetch(new Request(`${url.origin}/assets/youtube-fallback.xml`));
      if (fallback.ok) {
        const xml = await fallback.text();
        if (validFeed(xml)) {
          const result = response(xml, '', 'fallback');
          return request.method === 'HEAD' ? new Response(null, result) : result;
        }
      }
      return new Response('YouTube feed temporarily unavailable', {status: 503,
        headers: {'Access-Control-Allow-Origin': '*', 'Cache-Control': 'no-store'}});
    }
  }
};
