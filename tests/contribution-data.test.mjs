import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {DatabaseSync} from 'node:sqlite';
import {
  CONTRIBUTION_VISIBILITY_CTE, contributionSchema, getPublicContribution,
  insertContributionRecord, listContributionResponses, listPublicContributions, validateContributionInput,
} from '../src/contribution-data.js';

function fixture(t) {
  const sqlite = new DatabaseSync(':memory:');
  t.after(() => sqlite.close());
  const migrations = new URL('../drizzle/', import.meta.url);
  for (const name of fs.readdirSync(migrations).filter(name => name.endsWith('.sql')).sort()) {
    sqlite.exec(fs.readFileSync(new URL(name, migrations), 'utf8'));
  }
  sqlite.exec('PRAGMA foreign_keys=ON');
  const db = {
    all: async (sql, ...args) => sqlite.prepare(sql).all(...args),
    first: async (sql, ...args) => sqlite.prepare(sql).get(...args) || null,
    q: (sql, ...args) => ({run: async () => sqlite.prepare(sql).run(...args)}),
  };
  async function seed(id, {created = 1000, relatedId = null, mission = 'source', title = 'Exact source reference', body = 'An observation with an exact citation and stated uncertainty.'} = {}) {
    const postId = 'post-' + id, user = 'private-user-' + id, handle = 'Contributor ' + id;
    sqlite.prepare('INSERT INTO submissions(id,mission,user,handle,body,created) VALUES(?,?,?,?,?,?)').run(id, mission, user, handle, body, created);
    sqlite.prepare('INSERT INTO posts(id,scope,user,handle,title,body,created) VALUES(?,?,?,?,?,?,?)').run(postId, 'general', user, handle, title, body, created);
    await insertContributionRecord(db, id, postId, {
      mission, title, target: 'HT31', sources: 'Exact source §4.1.2', method: '',
      uncertainty: 'Reading branch remains open', exposure: 'Previously inspected',
      credit: '', license: 'UNSPECIFIED', relatedId,
    }, handle).run();
    return postId;
  }
  return {db, sqlite, seed};
}

const brief = overrides => new URLSearchParams({
  format: 'contribution-v1', mission: 'source', title: 'Exact source reference',
  body: 'A useful source reference with uncertainty clearly stated.', sources: 'Author, work, page and stable URL', rights: 'yes', ...overrides,
});

test('structured validation keeps source intake small and never silently grants a license', () => {
  const data = validateContributionInput(brief());
  assert.equal(data.structured, true);
  assert.equal(data.target, '');
  assert.equal(data.license, 'UNSPECIFIED');
  assert.equal(data.uncertainty, 'Not stated');
  assert.equal(data.exposure, 'Not declared');
  assert.throws(() => validateContributionInput(brief({rights: ''})), /safe to share/);
  assert.throws(() => validateContributionInput(brief({license: 'MIT'})), /supported license/);
  assert.throws(() => validateContributionInput(brief({body: 'x'.repeat(24001)})), /too long/);
  assert.throws(() => validateContributionInput(brief({sources: 'x'.repeat(4001)})), /too long/);
  assert.throws(() => validateContributionInput(brief({mission: 'correction'})), /target/);
  assert.throws(() => validateContributionInput(brief({mission: 'reproduction', target: 'C042'})), /method/);
  assert.throws(() => validateContributionInput(brief({relatedId: '../secret'})), /valid related contribution/);
});

test('legacy body-only submissions stay compatible and ignore unsupported structured provenance', async t => {
  const {db, sqlite} = fixture(t);
  const body = 'Historical calculation with exact reproduction steps and retained limits.';
  const data = validateContributionInput(new URLSearchParams({mission: 'LA-M001', body, license: 'CC0-1.0', title: 'Unvalidated title'}));
  assert.equal(data.structured, false);
  assert.equal(data.license, 'UNSPECIFIED');
  assert.equal(data.title, '');
  sqlite.prepare('INSERT INTO submissions(id,mission,user,handle,body,created) VALUES(?,?,?,?,?,?)').run('legacy-new', 'LA-M001', 'private-original', 'Original author', body, 5);
  sqlite.prepare('INSERT INTO posts(id,scope,user,handle,title,body,created) VALUES(?,?,?,?,?,?,?)').run('legacy-post', 'mission:LA-M001', 'private-original', 'Original author', 'Old result', body, 5);
  await insertContributionRecord(db, 'legacy-new', 'legacy-post', data, 'Original author').run();
  const record = await getPublicContribution(db, 'legacy-new');
  assert.equal(record.type, 'archived_result');
  assert.equal(record.title, 'Historical task result · LA-M001');
  assert.equal(record.body, body);
  assert.equal(record.fields.sources, '');
  assert.equal(record.fields.license, 'UNSPECIFIED');
  assert.equal(record.fields.credit, 'Original author');
  sqlite.prepare('INSERT INTO submissions(id,mission,user,handle,body,created) VALUES(?,?,?,?,?,?)').run('unlinked-old', 'source', 'private-original', 'Original author', body, 1);
  assert.equal(await getPublicContribution(db, 'unlinked-old'), null, 'old records are not linked by guessing text');
});

test('public records expose only visible discussion and project reviews, never identity or reports', async t => {
  const {db, sqlite, seed} = fixture(t);
  await seed('a');
  sqlite.prepare('INSERT INTO profiles(id,handle,created) VALUES(?,?,?)').run('private-steward', 'Public reviewer', 1);
  sqlite.prepare('INSERT INTO moderation VALUES(?,?,?,?,?,?)').run('review-1', 'a', 'private-steward', 'review:needs_work', 'A source page is still missing.', 1001);
  sqlite.prepare('INSERT INTO moderation VALUES(?,?,?,?,?,?)').run('report-1', 'a', 'private-reporter', 'report', 'Private report wording', 1002);
  sqlite.prepare('UPDATE submissions SET status=?,note=?,"commit"=? WHERE id=?').run('needs_work', 'A source page is still missing.', 'record/reference', 'a');
  const reply = sqlite.prepare('INSERT INTO posts(id,scope,parent,user,handle,title,body,created,hidden) VALUES(?,?,?,?,?,?,?,?,?)');
  reply.run('reply-visible', 'general', 'post-a', 'private-reply', 'Reply author', '', 'Visible evidence reply', 1003, 0);
  reply.run('reply-hidden', 'general', 'post-a', 'private-hidden', 'Hidden author', '', 'Hidden reply wording', 1004, 1);
  const record = await getPublicContribution(db, 'a', {origin: 'https://example.test'});
  assert.equal(record.url, 'https://example.test/contributions/a');
  assert.equal(record.discussionUrl, 'https://example.test/threads/post-a');
  assert.equal(record.status, 'needs_work');
  assert.equal(record.commit, 'record/reference');
  assert.deepEqual(record.replies.map(reply => reply.id), ['reply-visible']);
  assert.deepEqual(record.reviewHistory, [{id: 'review-1', status: 'needs_work', note: 'A source page is still missing.', created: 1001, handle: 'Public reviewer'}]);
  const exported = JSON.stringify(await listPublicContributions(db, {includeDetails: true}));
  assert.doesNotMatch(exported, /private-|Private report wording|Hidden reply wording|"(?:user|actor|email)"\s*:/);
});

test('hiding a parent removes its dependent records and replies from every public helper', async t => {
  const {db, sqlite, seed} = fixture(t);
  await seed('parent');
  await seed('child', {relatedId: 'parent', mission: 'review'});
  await seed('grandchild', {relatedId: 'child', mission: 'correction'});
  await seed('other');
  assert.equal((await listPublicContributions(db)).items.length, 4);
  assert.deepEqual((await listContributionResponses(db, 'parent')).map(row => row.id), ['child']);
  assert.deepEqual((await listPublicContributions(db, {relatedId: 'child'})).items.map(row => row.id), ['grandchild']);
  sqlite.prepare('UPDATE posts SET hidden=1 WHERE id=?').run('post-parent');
  for (const id of ['parent', 'child', 'grandchild']) assert.equal(await getPublicContribution(db, id), null, id);
  assert.deepEqual((await listPublicContributions(db, {includeDetails: true})).items.map(row => row.id), ['other']);
  assert.deepEqual(await listContributionResponses(db, 'parent'), []);
  const threads = await db.all(`${CONTRIBUTION_VISIBILITY_CTE}
    SELECT p.id FROM posts p LEFT JOIN contribution_records linked ON linked.post_id=COALESCE(p.parent,p.id)
    WHERE p.hidden=0 AND (linked.id IS NULL OR linked.id IN (SELECT id FROM visible_contributions))`);
  assert.deepEqual(threads.map(row => row.id), ['post-other']);
  sqlite.prepare('UPDATE posts SET hidden=0 WHERE id=?').run('post-parent');
  assert.equal((await listPublicContributions(db)).items.length, 4);
});

test('cursor pagination is deterministic under timestamp ties and filters use literal search', async t => {
  const {db, seed} = fixture(t);
  await seed('a', {title: 'A 100% complete citation'});
  await seed('b', {mission: 'correction'});
  await seed('c');
  await seed('d', {created: 2000});
  const first = await listPublicContributions(db, {limit: 2});
  assert.deepEqual(first.items.map(row => row.id), ['d', 'c']);
  assert.ok(first.nextCursor);
  const next = await listPublicContributions(db, {limit: 2, cursor: first.nextCursor});
  assert.deepEqual(next.items.map(row => row.id), ['b', 'a']);
  assert.equal(next.nextCursor, null);
  assert.deepEqual((await listPublicContributions(db, {type: 'correction'})).items.map(row => row.id), ['b']);
  assert.deepEqual((await listPublicContributions(db, {query: '%'})).items.map(row => row.id), ['a']);
  assert.deepEqual((await listPublicContributions(db, {q: '100%'})).items.map(row => row.id), ['a']);
  await assert.rejects(listPublicContributions(db, {cursor: 'not-valid'}), /cursor/);
  await assert.rejects(listPublicContributions(db, {type: 'made_up'}), /type filter/);
  await assert.rejects(listPublicContributions(db, {status: 'secret'}), /status filter/);
  await assert.rejects(listPublicContributions(db, {limit: 0}), /positive whole/);
});

test('public reads enforce page limits and the schema declares explicit field allowlists', async t => {
  const {db, seed} = fixture(t);
  for (let i = 0; i < 105; i++) await seed('record-' + String(i).padStart(3, '0'));
  assert.equal((await listPublicContributions(db, {limit: 999})).items.length, 50);
  assert.equal((await listPublicContributions(db, {limit: 999, includeDetails: true})).items.length, 100);
  const schema = contributionSchema();
  assert.equal(schema.properties.schemaVersion.const, 1);
  assert.equal(schema.$defs.contribution.additionalProperties, false);
  assert.equal(schema.$defs.reply.additionalProperties, false);
  assert.equal(schema.$defs.review.additionalProperties, false);
  for (const privateField of ['user', 'actor', 'email', 'reports']) assert.equal(privateField in schema.$defs.contribution.properties, false);
});
