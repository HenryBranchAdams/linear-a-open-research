import test from 'node:test';
import assert from 'node:assert/strict';
import {DatabaseSync} from 'node:sqlite';
import {createHash} from 'node:crypto';
import fs from 'node:fs';
import worker from '../dist/server/index.js';
import {reserveSQL} from '../src/db.js';

const origin = 'https://linear-a-open-research.madebyhenry.chatgpt.site';
const DAY = 86400000;
const USER_A = 'private-subject-a';
const USER_B = 'private-subject-b';
const USER_C = 'private-subject-c';
const STEWARD = 'owner';
const handles = {
  [USER_A]: 'Research A',
  [USER_B]: 'Research B',
  [USER_C]: 'Research C',
  [STEWARD]: 'Project Steward',
};
const missions = JSON.parse(fs.readFileSync(new URL('../content/missions.json', import.meta.url), 'utf8'));
const inputManifest = JSON.parse(fs.readFileSync(new URL('../release/input-manifest.json', import.meta.url), 'utf8'));
const inputHashes = new Map(inputManifest.files.map(file => [file.path, file.sha256]));

// Original v1 prompts: archival disposition belongs outside their immutable text.
// Packet ZIPs may be repackaged with a current notice; original input bytes may not.
const historicalPromptHashes = {
  'LA-M001': '605a6b69289e82fe1c1cb07d9e64cf0899fa1805ef978c51d60304274425b33c',
  'LA-M002': '1bf4e57d3757e97df7729fb12a4fa7c83b57bf05a263d6b32121bb76608cc537',
  'LA-M003': '7c2d70fd1638c529b70c0d037fff8337ae066de03c78a80642fb277446662cf9',
  'LA-M004': 'b713957ba55381527754211283e58a6e8026092b2db1f0d8087b0ad28a83aa4e',
  'LA-M005': 'bd8d716350cca7f3580356073147a114f35a4a23aed93d0861a2680f3938fec8',
  'LA-M006': '84401b05434ea9b6735cede5ed6ff20aa8507b54ce27a8df1768f337e98361b7',
  'LA-M007': 'fc9db8ea72be294045db18234d95155b5b754f2d544aff23d9ccd15dc418a57a',
  'LA-M008': '289e3590f5de7aa87da60735ad46d44f3c6a61915f01608ee55f642bfb56a1e7',
};
const sha256 = bytes => createHash('sha256').update(bytes).digest('hex');

function fixture(t) {
  const sqlite = new DatabaseSync(':memory:');
  t.after(() => sqlite.close());
  const migrationDir = new URL('../drizzle/', import.meta.url);
  for (const file of fs.readdirSync(migrationDir).filter(file => file.endsWith('.sql')).sort()) {
    sqlite.exec(fs.readFileSync(new URL(file, migrationDir), 'utf8'));
  }
  const db = {
    prepare(sql) {
      return {
        bind(...args) {
          return {
            async first() { return sqlite.prepare(sql).get(...args) || null; },
            async all() { return {results: sqlite.prepare(sql).all(...args)}; },
            async run() {
              const result = sqlite.prepare(sql).run(...args);
              return {meta: {changes: result.changes}};
            },
          };
        },
      };
    },
    async batch(queries) {
      sqlite.exec('BEGIN');
      try {
        const results = [];
        for (const query of queries) results.push(await query.run());
        sqlite.exec('COMMIT');
        return results;
      } catch (error) {
        sqlite.exec('ROLLBACK');
        throw error;
      }
    },
  };
  return {sqlite, env: {DB: db, STEWARD_EMAIL: 'owner@example.test'}};
}

function authHeaders(who) {
  return who ? {
    'oai-authenticated-user-id': who,
    'oai-authenticated-user-email': who === STEWARD ? 'owner@example.test' : who + '@example.test',
  } : {};
}
const get = (path, env, who) => worker.fetch(
  new Request(origin + path, {headers: authHeaders(who)}), env,
);
const post = (path, fields, env, who = USER_A, requestOrigin = origin) => worker.fetch(
  new Request(origin + path, {
    method: 'POST',
    headers: {
      Origin: requestOrigin,
      'Content-Type': 'application/x-www-form-urlencoded',
      ...authHeaders(who),
    },
    body: new URLSearchParams(fields),
  }), env,
);

async function profile(env, who) {
  assert.equal((await post('/actions/profile', {handle: handles[who]}, env, who)).status, 303);
}

function seedHistoricalClaim(sqlite, mission, user, {state = 'claimed', expires = Date.now() + DAY} = {}) {
  sqlite.prepare('INSERT INTO slots(mission,user,handle,expires,state,note,version) VALUES(?,?,?,?,?,?,?)')
    .run(mission, user, handles[user], expires, state, 'Preserved historical progress', 3);
  sqlite.prepare('INSERT INTO claim_events(id,mission,user,kind,created,note) VALUES(?,?,?,?,?,?)')
    .run('historical:' + mission, mission, user, 'lead', Date.now() - DAY, 'Original reservation');
}

function noPrivateIdentity(text) {
  assert.doesNotMatch(text, /private-subject-[abc]|owner@example\.test|oai-authenticated-user-id|"(?:user|actor|email)"\s*:/);
}

test('current public record carries C044, its caveats, original campaign bytes and the GitHub source link', async t => {
  const {env} = fixture(t);
  for (const path of ['/', '/research', '/contribute', '/release', '/questions']) {
    const response = await get(path, env);
    assert.equal(response.status, 200, path);
    const text = await response.text();
    assert.match(text, /campaign 044/i, path);
    assert.match(text, /https:\/\/github\.com\/HenryBranchAdams\/linear-a-open-research/, path);
    assert.doesNotMatch(text, /through investigation 37|The complete Flouda study<\/h3>/i, path);
  }
  const ht31 = await (await get('/findings/ht31', env)).text();
  assert.match(ht31, /material-neutral conventional category/);
  assert.match(ht31, /No unused linguistic validation/);
  const research = await (await get('/research', env)).text();
  assert.match(research, /C045 is available and has not been created/);
  assert.match(research, /No candidate or semantic experiment is active/);
  const publication = await get('/files/research/campaigns/PUBLISHED_FILES.json', env);
  const manifest = await publication.json();
  for (const entry of manifest.files) {
    const response = await get('/files/research/campaigns/' + entry.path, env);
    assert.equal(response.status, 200, entry.path);
    assert.equal(sha256(Buffer.from(await response.arrayBuffer())), entry.sha256, entry.path);
  }
  for (const entry of manifest.excluded) {
    assert.equal((await get('/files/research/campaigns/' + entry.path, env)).status, 404, entry.path);
  }
});

test('public routes, original prompts, input links and packet downloads remain available anonymously', async t => {
  const {env} = fixture(t);
  for (const path of ['/', '/research', '/questions', '/methods', '/discussion', '/contribute', '/release', '/privacy']) {
    const response = await get(path, env);
    assert.equal(response.status, 200, path);
    assert.doesNotMatch(await response.text(), /\{\{[A-Z_]+\}\}/, path);
  }
  const checkedInputs = new Set();
  assert.deepEqual(missions.map(mission => mission.id).sort(), Object.keys(historicalPromptHashes).sort());
  for (const mission of missions) {
    for (const path of ['/questions/' + mission.id, '/questions/' + mission.id + '/submit']) {
      assert.equal((await get(path, env)).status, 200, path);
    }
    const prompt = await get('/prompts/' + mission.id + '.md', env);
    assert.equal(prompt.status, 200, mission.id);
    const text = await prompt.text();
    assert.equal(text, mission.prompt, mission.id);
    assert.equal(sha256(text), historicalPromptHashes[mission.id], mission.id + ' original prompt');
    const packet = await get('/packets/' + mission.id + '.zip', env);
    assert.equal(packet.status, 200, mission.id + ' packet');
    assert.match(packet.headers.get('Content-Type'), /application\/zip/);
    assert.equal(Buffer.from(await packet.arrayBuffer()).subarray(0, 4).toString('hex'), '504b0304');
    for (const file of mission.inputs) {
      if (checkedInputs.has(file)) continue;
      checkedInputs.add(file);
      const response = await get('/files/' + file, env);
      assert.equal(response.status, 200, file);
      assert.ok(inputHashes.has(file), file + ' remains in the published input manifest');
      assert.equal(sha256(Buffer.from(await response.arrayBuffer())), inputHashes.get(file), file);
    }
  }
});

test('all eight legacy missions are archived and none offers a new claim', async t => {
  const {env} = fixture(t);
  await profile(env, USER_A);
  for (const mission of missions) {
    assert.equal(mission.archived, true, mission.id);
    assert.equal(mission.ready, false, mission.id);
    assert.ok(typeof mission.archiveNote === 'string' && mission.archiveNote.trim(), mission.id + ' current disposition');
    const page = await (await get('/questions/' + mission.id, env, USER_A)).text();
    assert.match(page, /archiv/i, mission.id);
    assert.doesNotMatch(page, /action=["']\/actions\/(?:claim|renew)["']/, mission.id);
  }
  const status = await (await get('/api/status', env)).json();
  assert.deepEqual(Object.keys(status.missions).sort(), Object.keys(historicalPromptHashes).sort());
  for (const [mission, value] of Object.entries(status.missions)) {
    assert.notEqual(value.state, 'available', mission + ' must not advertise available work');
  }
});

test('archived missions reject lead, replication, renewal and steward external claims without creating records', async t => {
  const {env, sqlite} = fixture(t);
  await profile(env, USER_A);
  await profile(env, STEWARD);
  for (const mission of missions) {
    for (const kind of ['lead', 'replication']) {
      assert.equal((await post('/actions/claim', {mission: mission.id, kind}, env)).status, 400, mission.id + ' ' + kind);
    }
    assert.equal((await post('/actions/renew', {mission: mission.id, note: 'A historical progress note'}, env)).status, 400, mission.id + ' renewal');
    assert.equal((await post('/actions/external-claim', {
      mission: mission.id, handle: 'verified-contributor', note: 'Verified historical issue reference',
    }, env, STEWARD)).status, 400, mission.id + ' external claim');
  }
  assert.equal(sqlite.prepare('SELECT count(*) n FROM slots').get().n, 0);
  assert.equal(sqlite.prepare('SELECT count(*) n FROM claim_events').get().n, 0);
});

test('an owner can release a historical archived claim, but cannot renew it or release another owner’s claim', async t => {
  const {env, sqlite} = fixture(t);
  await profile(env, USER_A);
  await profile(env, USER_B);
  seedHistoricalClaim(sqlite, 'LA-M001', USER_A);
  seedHistoricalClaim(sqlite, 'LA-M002', USER_A, {expires: 1});
  const original = sqlite.prepare('SELECT * FROM slots WHERE mission=?').get('LA-M001');
  assert.equal((await post('/actions/release', {mission: 'LA-M001'}, env, USER_B)).status, 400);
  assert.equal((await post('/actions/renew', {mission: 'LA-M001', note: 'Preserved work does not restart this mission'}, env)).status, 400);
  assert.deepEqual(sqlite.prepare('SELECT * FROM slots WHERE mission=?').get('LA-M001'), original);
  const dashboard = await (await get('/me', env, USER_A)).text();
  assert.match(dashboard, /action=["']\/actions\/release["']/);
  assert.doesNotMatch(dashboard, /action=["']\/actions\/renew["']/);
  for (const mission of ['LA-M001', 'LA-M002']) {
    assert.equal((await post('/actions/release', {mission}, env)).status, 303, mission);
    const slot = sqlite.prepare('SELECT * FROM slots WHERE mission=?').get(mission);
    assert.equal(slot.state, 'available');
    assert.equal(slot.note, 'Preserved historical progress');
    assert.equal((await post('/actions/claim', {mission, kind: 'lead'}, env, USER_B)).status, 400, 'release does not reactivate ' + mission);
  }
  assert.equal(sqlite.prepare("SELECT count(*) n FROM claim_events WHERE kind='release'").get().n, 2);
  assert.equal((await post('/actions/release', {mission: 'LA-M001'}, env)).status, 400, 'duplicate release');
  assert.equal((await post('/actions/release', {mission: 'not-a-known-mission'}, env)).status, 400);
});

test('a historical owner can submit, and expiry or release cannot reopen a submitted result', async t => {
  const {env, sqlite} = fixture(t);
  await profile(env, USER_A);
  await profile(env, USER_B);
  seedHistoricalClaim(sqlite, 'LA-M001', USER_A);
  const body = 'Historical result with source references, rival interpretations and remaining limitations.';
  assert.equal((await post('/actions/submit', {mission: 'LA-M001', body}, env)).status, 303);
  assert.equal(sqlite.prepare('SELECT state FROM slots WHERE mission=?').get('LA-M001').state, 'submitted');
  const submission = sqlite.prepare('SELECT * FROM submissions').get();
  assert.equal(submission.body, body);
  assert.equal(submission.status, 'submitted');
  sqlite.exec('UPDATE slots SET expires=1');
  for (const who of [USER_A, USER_B]) {
    assert.equal((await post('/actions/release', {mission: 'LA-M001'}, env, who)).status, 400);
    assert.equal((await post('/actions/claim', {mission: 'LA-M001', kind: 'lead'}, env, who)).status, 400);
  }
  assert.equal(sqlite.prepare('SELECT state FROM slots WHERE mission=?').get('LA-M001').state, 'submitted');
  assert.deepEqual(sqlite.prepare('SELECT * FROM submissions').get(), submission);
});

test('unclaimed results and a historical replication do not close another contributor’s lead record', async t => {
  const {env, sqlite} = fixture(t);
  for (const who of [USER_A, USER_B, USER_C]) await profile(env, who);
  seedHistoricalClaim(sqlite, 'LA-M003', USER_A);
  sqlite.prepare('INSERT INTO claim_events VALUES(?,?,?,?,?,?)')
    .run('historical-replication', 'LA-M003', USER_B, 'replication', Date.now() - DAY, 'Existing replication declaration');
  const lead = sqlite.prepare('SELECT * FROM slots').get();
  for (const who of [USER_B, USER_C]) {
    assert.equal((await post('/actions/submit', {
      mission: 'LA-M003', body: 'Independent historical result with a source, alternatives and explicit uncertainty.',
    }, env, who)).status, 303);
    assert.deepEqual(sqlite.prepare('SELECT * FROM slots').get(), lead);
  }
  assert.equal(sqlite.prepare('SELECT count(*) n FROM submissions').get().n, 2);
  assert.equal(sqlite.prepare("SELECT count(*) n FROM posts WHERE scope='mission:LA-M003'").get().n, 2);
  assert.equal(sqlite.prepare("SELECT count(*) n FROM claim_events WHERE kind='replication'").get().n, 1);
});

test('archived mission discussions preserve existing threads and still accept replies', async t => {
  const {env, sqlite} = fixture(t);
  await profile(env, USER_A);
  await profile(env, USER_B);
  sqlite.prepare('INSERT INTO posts(id,scope,user,handle,title,body,created) VALUES(?,?,?,?,?,?,?)')
    .run('historical-thread', 'mission:LA-M004', USER_A, handles[USER_A], 'Original source question', 'An existing source observation remains part of the record.', 1);
  const original = sqlite.prepare('SELECT * FROM posts WHERE id=?').get('historical-thread');
  assert.match(await (await get('/questions/LA-M004', env)).text(), /Original source question/);
  assert.equal((await get('/threads/historical-thread', env)).status, 200);
  assert.equal((await post('/actions/post', {
    scope: 'mission:LA-M004', parent: 'historical-thread', body: 'A bounded correction to the historical observation, with its source.',
  }, env, USER_B)).status, 303);
  assert.deepEqual(sqlite.prepare('SELECT * FROM posts WHERE id=?').get('historical-thread'), original);
  assert.equal(sqlite.prepare('SELECT count(*) n FROM posts WHERE parent=?').get('historical-thread').n, 1);
});

test('the contribution intake accepts ideas, sources and corrections for review without creating a mission or claim', async t => {
  const {env, sqlite} = fixture(t);
  await profile(env, USER_A);
  assert.equal((await get('/contribute', env, USER_A)).status, 200);
  for (const mission of ['idea', 'source', 'correction']) {
    assert.equal((await post('/actions/submit', {
      mission, body: 'Exact evidence packet; existing exposure; competing predictions; a finite acquisition path and stopping condition.',
    }, env)).status, 303, mission);
  }
  assert.equal(sqlite.prepare('SELECT count(*) n FROM submissions').get().n, 3);
  assert.equal(sqlite.prepare("SELECT count(*) n FROM submissions WHERE status='submitted'").get().n, 3);
  assert.equal(sqlite.prepare('SELECT count(*) n FROM slots').get().n, 0);
  assert.equal(sqlite.prepare('SELECT count(*) n FROM claim_events').get().n, 0);
});

test('authentication, same-origin protection and steward authorization guard actions that remain available', async t => {
  const {env, sqlite} = fixture(t);
  const fields = {mission: 'source', body: 'A source contribution with an exact citation and material limitations.'};
  assert.equal((await post('/actions/submit', fields, env, null)).status, 401);
  assert.equal((await post('/actions/claim', {mission: 'LA-M001', kind: 'lead'}, env, null)).status, 401);
  await profile(env, USER_A);
  seedHistoricalClaim(sqlite, 'LA-M001', USER_A);
  assert.equal((await post('/actions/submit', fields, env, USER_A, 'https://other.example')).status, 403);
  assert.equal((await post('/actions/release', {mission: 'LA-M001'}, env, USER_A, 'https://other.example')).status, 403);
  assert.equal((await post('/actions/moderate', {target: handles[USER_A], action: 'suspend_handle', note: 'Unauthorized action'}, env)).status, 403);
  assert.equal((await post('/actions/review', {submission: 'missing', status: 'accepted', note: 'Unauthorized review', commit: 'record/example'}, env)).status, 403);
  assert.equal(sqlite.prepare('SELECT count(*) n FROM submissions').get().n, 0);
  assert.equal(sqlite.prepare('SELECT count(*) n FROM moderation').get().n, 0);
  assert.equal(sqlite.prepare('SELECT state FROM slots').get().state, 'claimed');
});

test('public discussion, thread pages, status and steward exports escape content and exclude private identity', async t => {
  const {env, sqlite} = fixture(t);
  await profile(env, USER_A);
  await profile(env, STEWARD);
  seedHistoricalClaim(sqlite, 'LA-M001', USER_A);
  assert.equal((await post('/actions/post', {
    scope: 'general', title: 'Source <img src=x onerror=alert(1)>', body: '<script>alert(1)</script>',
  }, env)).status, 303);
  const postId = sqlite.prepare('SELECT id FROM posts').get().id;
  for (const path of ['/discussion', '/threads/' + postId]) {
    const page = await (await get(path, env)).text();
    assert.match(page, /&lt;script&gt;alert\(1\)&lt;\/script&gt;/);
    assert.doesNotMatch(page, /<script>alert\(1\)<\/script>|<img src=x onerror=alert\(1\)>/);
    noPrivateIdentity(page);
  }
  noPrivateIdentity(await (await get('/api/status', env)).text());
  assert.equal((await get('/api/export', env, USER_A)).status, 403);
  const exported = await get('/api/export', env, STEWARD);
  assert.equal(exported.status, 200);
  noPrivateIdentity(await exported.text());
});

test('database outages preserve public research and downloads while reporting unavailable coordination', async t => {
  const {env} = fixture(t);
  await profile(env, USER_A);
  assert.equal((await get('/api/status', {})).status, 503);
  for (const path of ['/', '/research', '/questions/LA-M001', '/contribute', '/release']) {
    assert.equal((await get(path, {})).status, 200, path);
  }
  const archivedPage = await (await get('/questions/LA-M001', {})).text();
  assert.match(archivedPage, /archiv/i);
  assert.match(archivedPage, /unavailable/i);
  assert.equal(await (await get('/prompts/LA-M001.md', {})).text(), missions.find(mission => mission.id === 'LA-M001').prompt);
  assert.equal((await post('/actions/profile', {handle: 'New Contributor'}, {})).status, 503);
});

test('steward acceptance and negative-result review require a reviewed record reference and preserve submitted state on failure', async t => {
  for (const status of ['accepted', 'negative_result']) {
    await t.test(status, async child => {
      const {env, sqlite} = fixture(child);
      await profile(env, USER_A);
      await profile(env, STEWARD);
      seedHistoricalClaim(sqlite, 'LA-M001', USER_A);
      assert.equal((await post('/actions/submit', {
        mission: 'LA-M001', body: 'A historical result with evidence, reproducible checks and explicit limitations.',
      }, env)).status, 303);
      const submission = sqlite.prepare('SELECT * FROM submissions').get();
      const slot = sqlite.prepare('SELECT * FROM slots').get();
      assert.equal((await post('/actions/review', {
        submission: submission.id, status, note: 'The evidence and strongest rival were reviewed.',
      }, env, STEWARD)).status, 400);
      assert.deepEqual(sqlite.prepare('SELECT * FROM submissions').get(), submission);
      assert.deepEqual(sqlite.prepare('SELECT * FROM slots').get(), slot);
      assert.equal(sqlite.prepare('SELECT count(*) n FROM moderation').get().n, 0);
      assert.equal((await post('/actions/review', {
        submission: submission.id, status, note: 'The evidence and strongest rival were reviewed.', commit: 'release/B2026-10-18-reviewed-result',
      }, env, STEWARD)).status, 303);
      assert.equal(sqlite.prepare('SELECT status FROM submissions').get().status, status);
      assert.equal(sqlite.prepare('SELECT state FROM slots').get().state, 'completed');
      assert.equal((await post('/actions/release', {mission: 'LA-M001'}, env)).status, 400);
      assert.equal((await post('/actions/claim', {mission: 'LA-M001', kind: 'lead'}, env, STEWARD)).status, 400);
    });
  }
});

// The SQL primitive is tested on synthetic in-memory identifiers. No production
// mission is made ready, and these checks are not a multi-connection load test.
test('reservation SQL gives competing reservations one winner and enforces the two-active-claim cap', async t => {
  const {env, sqlite} = fixture(t);
  const now = Date.now();
  const reserve = (mission, user) => env.DB.prepare(reserveSQL)
    .bind(mission, user, handles[user], now + DAY, user, now, now, user, now).run();
  const outcomes = await Promise.all([USER_A, USER_B].map(user => reserve('fixture-future-1', user)));
  assert.deepEqual(outcomes.map(outcome => outcome.meta.changes).sort(), [0, 1]);
  const winner = sqlite.prepare('SELECT user FROM slots').get().user;
  assert.equal((await reserve('fixture-future-2', winner)).meta.changes, 1);
  assert.equal((await reserve('fixture-future-3', winner)).meta.changes, 0);
  assert.equal(sqlite.prepare("SELECT count(*) n FROM slots WHERE user=? AND state='claimed'").get(winner).n, 2);
});

test('reservation SQL permits expired claims to change owners but protects submitted and completed records', async t => {
  const {env, sqlite} = fixture(t);
  const now = Date.now();
  const reserve = (mission, user) => env.DB.prepare(reserveSQL)
    .bind(mission, user, handles[user], now + DAY, user, now, now, user, now).run();
  assert.equal((await reserve('fixture-future-1', USER_A)).meta.changes, 1);
  sqlite.exec('UPDATE slots SET expires=1');
  assert.equal((await reserve('fixture-future-1', USER_B)).meta.changes, 1);
  assert.equal(sqlite.prepare('SELECT user FROM slots').get().user, USER_B);
  sqlite.exec("UPDATE slots SET state='submitted',expires=1");
  assert.equal((await reserve('fixture-future-1', USER_A)).meta.changes, 0);
  assert.equal((await reserve('fixture-future-2', USER_B)).meta.changes, 1);
  assert.equal((await reserve('fixture-future-3', USER_B)).meta.changes, 0, 'submitted records still occupy a claim slot');
  sqlite.prepare("UPDATE slots SET state='completed' WHERE mission=?").run('fixture-future-1');
  assert.equal((await reserve('fixture-future-1', USER_A)).meta.changes, 0);
  assert.equal((await reserve('fixture-future-3', USER_B)).meta.changes, 1, 'completed records no longer occupy the active-claim quota');
});

const structuredContribution = (overrides = {}) => ({
  format: 'contribution-v1', mission: 'source', title: 'A precise source observation',
  body: 'The cited page supplies an exact object reference, with the original reading uncertainty preserved.',
  sources: 'Author, title, page 12, figure 3; https://example.test/source',
  rights: 'yes', ...overrides,
});

async function submitStructured(env, fields = {}, who = USER_A) {
  const response = await post('/actions/submit', structuredContribution(fields), env, who);
  assert.equal(response.status, 303);
  const url = new URL(response.headers.get('Location'), origin);
  assert.match(url.pathname, /^\/contributions\/[a-f0-9-]+$/);
  const id = url.pathname.split('/')[2];
  const detail = await get('/api/contributions/' + id, env);
  assert.equal(detail.status, 200);
  return await detail.json();
}

test('structured contributions create public canonical records, provenance and safe JSON without reserving research', async t => {
  const {env, sqlite} = fixture(t);
  await profile(env, USER_A);
  const title = 'Source <img src=x onerror=alert(1)>';
  const body = 'Evidence <script>alert(1)</script> remains contributor text, with an exact citation.';
  const item = await submitStructured(env, {title, body, credit: 'Research A; catalogue authors credited', license: 'CC-BY-4.0'});
  assert.equal(item.type, 'source');
  assert.equal(item.status, 'submitted');
  assert.equal(item.title, title);
  assert.equal(item.body, body);
  assert.equal(item.fields.license, 'CC-BY-4.0');
  assert.equal(item.fields.exposure, 'Not declared');
  assert.equal(item.handle, handles[USER_A]);
  assert.equal(item.url, origin + '/contributions/' + item.id);
  assert.equal(sqlite.prepare('SELECT count(*) n FROM contribution_records').get().n, 1);
  assert.equal(sqlite.prepare('SELECT count(*) n FROM slots').get().n, 0);
  assert.equal(sqlite.prepare('SELECT count(*) n FROM claim_events').get().n, 0);
  for (const path of ['/contributions/' + item.id, '/contributions', '/discussion']) {
    const response = await get(path, env);
    assert.equal(response.status, 200);
    const html = await response.text();
    assert.match(html, /&lt;script&gt;alert\(1\)&lt;\/script&gt;/);
    assert.doesNotMatch(html, /<script>alert\(1\)<\/script>|<img src=x onerror=alert\(1\)>/);
    noPrivateIdentity(html);
  }
  const thread = await get('/threads/' + item.postId, env);
  assert.equal(thread.status, 303);
  assert.equal(new URL(thread.headers.get('Location'), origin).pathname, '/contributions/' + item.id);
  const publicList = await get('/api/contributions', env);
  assert.equal(publicList.headers.get('Access-Control-Allow-Origin'), '*');
  assert.equal(publicList.headers.get('Access-Control-Allow-Credentials'), null);
  const exported = await publicList.text();
  noPrivateIdentity(exported);
  assert.deepEqual(JSON.parse(exported).items.map(record => record.id), [item.id]);
});

test('structured intake validates rights, sources and related work while keeping review steward-only', async t => {
  const {env, sqlite} = fixture(t);
  assert.equal((await post('/actions/submit', structuredContribution(), env, null)).status, 401);
  await profile(env, USER_A);
  for (const invalid of [
    {rights: ''}, {sources: ''}, {mission: 'correction', target: ''},
    {mission: 'reproduction', target: 'C042', method: ''},
    {license: 'assumed-public-domain'}, {relatedId: 'missing-contribution'},
  ]) {
    assert.equal((await post('/actions/submit', structuredContribution(invalid), env)).status, 400, JSON.stringify(invalid));
  }
  assert.equal((await post('/actions/submit', structuredContribution(), env, USER_A, 'https://external.example')).status, 403);
  assert.equal(sqlite.prepare('SELECT count(*) n FROM submissions').get().n, 0);
  assert.equal(sqlite.prepare('SELECT count(*) n FROM posts').get().n, 0);
  assert.equal(sqlite.prepare('SELECT count(*) n FROM contribution_records').get().n, 0);
  const item = await submitStructured(env);
  assert.equal((await post('/actions/review', {submission: item.id, status: 'accepted', note: 'I reviewed my own work.', commit: 'some-reference'}, env)).status, 403);
  assert.equal((await post('/actions/moderate', {target: item.id, action: 'hide_post', note: 'Unauthorized moderation'}, env)).status, 403);
  assert.equal((await (await get('/api/contributions/' + item.id, env)).json()).status, 'submitted');
});

test('independent reviews stay ordinary contributions and reviewed rationale and references become public safely', async t => {
  const {env, sqlite} = fixture(t);
  for (const who of [USER_A, USER_B, STEWARD]) await profile(env, who);
  const original = await submitStructured(env, {title: 'A source worth checking'});
  const challenge = await submitStructured(env, {
    mission: 'review', title: 'Independent check of the source', target: original.url,
    relatedId: original.id, method: 'Inspected the cited page and compared the retained reading branches.',
  }, USER_B);
  assert.equal(challenge.relatedId, original.id);
  assert.equal(challenge.status, 'submitted');
  const originalHtml = await (await get('/contributions/' + original.id, env)).text();
  assert.ok(originalHtml.includes('/contributions/' + challenge.id));
  assert.match(originalHtml, /Independent check of the source/);
  const related = await (await get('/api/contributions?related=' + original.id, env)).json();
  assert.deepEqual(related.items.map(item => item.id), [challenge.id]);
  const rationale = 'Checked the source. <script>reviewAttack()</script> is quoted text.';
  assert.equal((await post('/actions/review', {submission: original.id, status: 'accepted', note: rationale}, env, STEWARD)).status, 400);
  const reference = 'javascript:alert("not a link")';
  assert.equal((await post('/actions/review', {submission: original.id, status: 'accepted', note: rationale, commit: reference}, env, STEWARD)).status, 303);
  const reviewed = await (await get('/api/contributions/' + original.id, env)).json();
  assert.equal(reviewed.status, 'accepted');
  assert.equal(reviewed.note, rationale);
  assert.equal(reviewed.commit, reference);
  assert.equal(reviewed.reviewHistory.length, 1);
  assert.equal(reviewed.reviewHistory[0].handle, handles[STEWARD]);
  assert.equal(reviewed.reviewHistory[0].status, 'accepted');
  const html = await (await get('/contributions/' + original.id, env)).text();
  assert.match(html, /&lt;script&gt;reviewAttack\(\)&lt;\/script&gt;/);
  assert.doesNotMatch(html, /<script>reviewAttack\(\)<\/script>|href=["']javascript:/);
  assert.match(await (await get('/discussion', env)).text(), /Accepted into the project record/);
  noPrivateIdentity(html);
  noPrivateIdentity(JSON.stringify(reviewed));
  assert.equal(sqlite.prepare('SELECT status FROM submissions WHERE id=?').get(challenge.id).status, 'submitted');
});

test('moderation hides contributions, dependent work and replies across pages, JSON and thread URLs', async t => {
  const {env, sqlite} = fixture(t);
  for (const who of [USER_A, USER_B, STEWARD]) await profile(env, who);
  const parent = await submitStructured(env, {title: 'Parent visibility marker', body: 'Parent-private-after-moderation evidence and source discussion.'});
  const child = await submitStructured(env, {mission: 'review', title: 'Child visibility marker', body: 'Child-private-after-moderation independent evidence check.', target: parent.url, relatedId: parent.id, method: 'Compared source text to the claim.'}, USER_B);
  assert.equal((await post('/actions/post', {scope: 'general', parent: parent.postId, body: 'Visible-reply-before-parent-moderation'}, env, USER_B)).status, 303);
  const parentReply = sqlite.prepare('SELECT id FROM posts WHERE parent=?').get(parent.postId).id;
  assert.equal((await post('/actions/post', {scope: 'general', parent: child.postId, body: 'Hidden-reply-standalone-marker'}, env, USER_B)).status, 303);
  const hiddenReply = sqlite.prepare('SELECT id FROM posts WHERE parent=?').get(child.postId).id;
  assert.equal((await post('/actions/moderate', {target: hiddenReply, action: 'hide_post', note: 'Private moderation report wording'}, env, STEWARD)).status, 303);
  for (const path of ['/contributions/' + child.id, '/api/contributions/' + child.id, '/api/contributions/export']) {
    assert.doesNotMatch(await (await get(path, env)).text(), /Hidden-reply-standalone-marker|Private moderation report wording/);
  }
  assert.equal((await get('/threads/' + hiddenReply, env)).status, 404);
  assert.equal((await post('/actions/moderate', {target: parent.id, action: 'hide_post', note: 'Hide parent and associated public context.'}, env, STEWARD)).status, 303);
  for (const path of [
    '/contributions/' + parent.id, '/contributions/' + child.id,
    '/api/contributions/' + parent.id, '/api/contributions/' + child.id,
    '/threads/' + parent.postId, '/threads/' + child.postId,
    '/threads/' + parentReply, '/threads/' + child.postId + '/extra',
  ]) assert.equal((await get(path, env)).status, 404, path);
  for (const path of ['/contributions', '/discussion', '/journal', '/api/contributions/export']) {
    const response = await get(path, env);
    assert.equal(response.status, 200, path);
    const content = await response.text();
    assert.doesNotMatch(content, /Parent visibility marker|Child visibility marker|Parent-private-after-moderation|Child-private-after-moderation|Visible-reply-before-parent-moderation/);
    noPrivateIdentity(content);
  }
  assert.equal((await post('/actions/post', {scope: 'general', parent: child.postId, body: 'Should not post beneath hidden context'}, env, USER_B)).status, 400);
  assert.equal((await post('/actions/submit', structuredContribution({relatedId: parent.id}), env, USER_B)).status, 400);
  assert.equal((await post('/actions/moderate', {target: parent.id, action: 'restore_post', note: 'Restore reviewed public context.'}, env, STEWARD)).status, 303);
  assert.equal((await get('/contributions/' + child.id, env)).status, 200);
  assert.equal((await get('/threads/' + hiddenReply, env)).status, 404, 'restoring parent does not restore a separately hidden reply');
  assert.equal(sqlite.prepare('SELECT count(*) n FROM submissions').get().n, 2, 'moderation preserves original submitted records');
});

test('the public API permits cross-origin reads and cursor traversal without duplicate records', async t => {
  const {env, sqlite} = fixture(t);
  await profile(env, USER_A);
  const created = [];
  for (let i = 0; i < 3; i++) created.push(await submitStructured(env, {title: 'Source contribution number ' + i}));
  sqlite.exec('UPDATE submissions SET created=1000');
  const response = await worker.fetch(new Request(origin + '/api/contributions?limit=2', {headers: {Origin: 'https://independent-mirror.example'}}), env);
  assert.equal(response.status, 200);
  assert.equal(response.headers.get('Access-Control-Allow-Origin'), '*');
  const first = await response.json();
  assert.equal(first.schemaVersion, 1);
  assert.equal(first.items.length, 2);
  assert.ok(first.nextCursor);
  const second = await (await get('/api/contributions?limit=2&cursor=' + first.nextCursor, env)).json();
  assert.equal(second.items.length, 1);
  assert.equal(second.nextCursor, null);
  assert.deepEqual([...first.items, ...second.items].map(item => item.id), created.map(item => item.id).sort().reverse());
  assert.equal(new Set([...first.items, ...second.items].map(item => item.id)).size, 3);
  for (const path of ['/api/contributions?cursor=not-valid', '/api/contributions?limit=0', '/api/contributions?type=unknown']) {
    const rejected = await get(path, env);
    assert.equal(rejected.status, 400, path);
    assert.match(rejected.headers.get('Content-Type'), /application\/json/);
  }
  assert.equal((await post('/api/contributions', structuredContribution(), env, null)).status, 401, 'public read CORS does not authorize writes');
});

test('anonymous drafts, portable templates and journal reading survive a coordination outage', async t => {
  const {env} = fixture(t);
  for (const runtime of [env, {}]) {
    const hub = await get('/contribute', runtime);
    assert.equal(hub.status, 200);
    const html = await hub.text();
    assert.match(html, /id="contribution-draft"/);
    assert.match(html, /name="sources"/);
    assert.match(html, /data-draft-download="md"/);
    assert.match(html, /data-draft-download="json"/);
    assert.match(html, /github\.com\/HenryBranchAdams\/linear-a-open-research\/issues\/new/);
    const consent = html.match(/<input[^>]+name="rights"[^>]*>/)?.[0];
    assert.ok(consent);
    assert.doesNotMatch(consent, /checked/);
    for (const path of ['/files/CONTRIBUTION_TEMPLATE.md', '/api/contributions/schema', '/journal', '/journal/c044', '/journal/c043', '/journal/c042', '/journal/feed.xml']) {
      assert.equal((await get(path, runtime)).status, 200, path);
    }
  }
  const unavailable = await get('/api/contributions/export', {});
  assert.equal(unavailable.status, 503);
  assert.match((await unavailable.json()).error, /temporarily unavailable/);
  assert.match(await (await get('/journal/c044', {})).text(), /What kind of vessel is drawn on HT31/);
});

test('journal notes cite preserved campaign evidence, share finding discussions and expose a public feed', async t => {
  const {env, sqlite} = fixture(t);
  const entries = JSON.parse(fs.readFileSync(new URL('../content/journal.json', import.meta.url), 'utf8'));
  assert.deepEqual(entries.map(entry => entry.id), ['c044', 'c043', 'c042']);
  const index = await (await get('/journal', env)).text();
  assert.match(index, /No semantic experiment is active/);
  assert.doesNotMatch(index, /C045 (?:has begun|is active|started|is complete)/);
  for (const entry of entries) {
    const page = await get('/journal/' + entry.id, env);
    assert.equal(page.status, 200);
    const html = await page.text();
    assert.ok(html.includes(entry.findingPath));
    for (const source of entry.sources) {
      assert.ok(html.includes('/files/' + source.path), source.path);
      const publicSource = await get('/files/' + source.path, env);
      assert.equal(publicSource.status, 200, source.path);
      assert.equal(sha256(Buffer.from(await publicSource.arrayBuffer())), sha256(fs.readFileSync(new URL('../' + source.path, import.meta.url))), source.path);
    }
  }
  await profile(env, USER_A);
  assert.equal((await post('/actions/post', {scope: 'finding:ht31', title: 'Journal-linked evidence question', body: 'Which exact ceramic object would change this comparison?'}, env)).status, 303);
  for (const path of ['/journal/c044', '/findings/ht31']) {
    assert.match(await (await get(path, env)).text(), /Journal-linked evidence question/);
  }
  assert.equal(sqlite.prepare('SELECT scope FROM posts').get().scope, 'finding:ht31');
  const feed = await get('/journal/feed.xml', env);
  assert.equal(feed.status, 200);
  assert.match(feed.headers.get('Content-Type'), /application\/rss\+xml/);
  const xml = await feed.text();
  assert.equal((xml.match(/<item>/g) || []).length, 3);
  for (const entry of entries) assert.ok(xml.includes(origin + '/journal/' + entry.id));
  assert.doesNotMatch(xml, /<pubDate>/, 'documentation dates must not be represented as new publication timestamps');
});

test('legacy submissions retain dashboard feedback without inventing public contribution links', async t => {
  const {env, sqlite} = fixture(t);
  await profile(env, USER_A);
  sqlite.prepare('INSERT INTO submissions(id,mission,user,handle,body,created,status,note) VALUES(?,?,?,?,?,?,?,?)')
    .run('old-unlinked-submission', 'source', USER_A, handles[USER_A], 'Original historical source submission.', 1, 'needs_work', 'Preserved feedback for the earlier source.');
  const current = await submitStructured(env);
  const html = await (await get('/me', env, USER_A)).text();
  assert.match(html, /Preserved feedback for the earlier source/);
  assert.doesNotMatch(html, /href="\/contributions\/old-unlinked-submission"/);
  assert.ok(html.includes('/contributions/' + current.id));
  assert.equal((await get('/api/contributions/old-unlinked-submission', env)).status, 404);
  assert.equal(sqlite.prepare('SELECT count(*) n FROM contribution_records').get().n, 1);
});
