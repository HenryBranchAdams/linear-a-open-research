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
