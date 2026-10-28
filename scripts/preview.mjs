// Local preview only. Production uses the managed Worker and its existing DB.
import http from 'node:http';
import fs from 'node:fs';
import {pathToFileURL} from 'node:url';
import {execFileSync} from 'node:child_process';
import {DatabaseSync} from 'node:sqlite';

if (!fs.existsSync('dist/server/index.js')) execFileSync(process.execPath, ['scripts/build.mjs'], {stdio: 'inherit'});
const sqlite = new DatabaseSync(':memory:');
for (const file of fs.readdirSync('drizzle').filter(file => file.endsWith('.sql'))) sqlite.exec(fs.readFileSync(`drizzle/${file}`, 'utf8'));
const env = {DB: {prepare(sql) {return {bind(...args) {return {
  async first() {return sqlite.prepare(sql).get(...args) || null;},
  async all() {return {results: sqlite.prepare(sql).all(...args)};},
  async run() {return {meta: {changes: sqlite.prepare(sql).run(...args).changes}};}
};}};}, async batch(queries) {sqlite.exec('BEGIN'); try {const results = []; for (const query of queries) results.push(await query.run()); sqlite.exec('COMMIT'); return results;} catch (error) {sqlite.exec('ROLLBACK'); throw error;}}}};

http.createServer(async (request, response) => {
  try {
    const previewUrl = new URL(request.url, 'http://preview.local');
    if (previewUrl.pathname.startsWith('/__preview/')) {
      const sizes = {desktop: [1440, 900, .88], tablet: [768, 1024, .78], mobile: [390, 844, 1]};
      const name = previewUrl.pathname.split('/')[2];
      if (!sizes[name]) {response.writeHead(404); response.end(); return;}
      const [width, height, scale] = sizes[name];
      const allowed = ['/', '/research', '/methods', '/contribute', '/questions', '/questions/LA-M001', '/findings/ht34', '/findings/ht31', '/findings/capacity', '/findings/akrotiri', '/findings/cord-function', '/release', '/privacy', '/discussion', '/journal', '/journal/c044', '/journal/c043', '/journal/c042', '/contributions'];
      const page = allowed.includes(previewUrl.searchParams.get('page')) ? previewUrl.searchParams.get('page') : '/';
      const noScript = previewUrl.searchParams.has('nojs');
      response.writeHead(200, {'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store'});
      response.end(`<!doctype html><html lang="en"><head><meta charset="utf-8"><title>${name} layout preview</title><style>body{margin:0;background:#ddd;font:16px/1.5 Arial}p{margin:12px;text-align:center}.frame{width:${width*scale}px;height:${height*scale}px;margin:0 auto}iframe{display:block;border:0;background:white;width:${width}px;height:${height}px;transform:scale(${scale});transform-origin:top left}</style></head><body><p>Local layout review · ${width} × ${height} CSS pixels${noScript?' · JavaScript disabled':''}</p><div class="frame"><iframe title="${name} research preview" src="${page}" ${noScript?'sandbox="allow-same-origin"':''}></iframe></div></body></html>`);
      return;
    }
    const filename = 'dist/server/index.js';
    const {default: worker} = await import(`${pathToFileURL(process.cwd() + '/' + filename).href}?v=${fs.statSync(filename).mtimeMs}`);
    const chunks = []; for await (const chunk of request) chunks.push(chunk);
    const headers = new Headers(request.headers);
    headers.delete('oai-authenticated-user-id'); headers.delete('oai-authenticated-user-email');
    const req = new Request(`http://${request.headers.host}${request.url}`, {method: request.method, headers, ...(!['GET', 'HEAD'].includes(request.method) ? {body: Buffer.concat(chunks), duplex: 'half'} : {})});
    const result = await worker.fetch(req, env);
    response.writeHead(result.status, Object.fromEntries(result.headers));
    response.end(request.method === 'HEAD' ? undefined : Buffer.from(await result.arrayBuffer()));
  } catch (error) {response.writeHead(500, {'Content-Type': 'text/plain'}); response.end('Preview could not render this page.'); console.error(error.message);}
}).listen(Number(process.env.PORT || 4173), '0.0.0.0', () => console.log('Research preview ready. Local coordination database is empty.'));
